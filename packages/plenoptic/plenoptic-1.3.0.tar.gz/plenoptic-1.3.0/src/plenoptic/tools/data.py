import contextlib
import pathlib
import warnings
from typing import Literal

import imageio.v3 as iio
import numpy as np
import torch
from skimage import color
from torch import Tensor

NUMPY_TO_TORCH_TYPES = {
    bool: torch.bool,  # np.bool deprecated in fav of built-in
    np.uint8: torch.uint8,
    np.int8: torch.int8,
    np.int16: torch.int16,
    np.int32: torch.int32,
    np.int64: torch.int64,
    np.float16: torch.float16,
    np.float32: torch.float32,
    np.float64: torch.float64,
    np.complex64: torch.complex64,
    np.complex128: torch.complex128,
}

TORCH_TO_NUMPY_TYPES = {value: key for (key, value) in NUMPY_TO_TORCH_TYPES.items()}


def to_numpy(x: Tensor | np.ndarray, squeeze: bool = False) -> np.ndarray:
    r"""cast tensor to numpy in the most conservative way possible

    Parameters
    ----------
    x
        Tensor to be converted to `numpy.ndarray` on CPU.

    squeeze
        Removes all dummy dimensions of the tensor

    Returns
    -------
    Converted tensor as `numpy.ndarray` on CPU.
    """

    with contextlib.suppress(AttributeError):
        # if this fails, it's already a numpy array
        x = x.detach().cpu().numpy().astype(TORCH_TO_NUMPY_TYPES[x.dtype])
    if squeeze:
        x = x.squeeze()
    return x


def load_images(paths: str | list[str], as_gray: bool = True) -> Tensor:
    r"""Correctly load in images

    Our models and synthesis methods generally expect their inputs to
    be 4d float32 images: (batch, channel, height, width), where the batch
    dimension contains multiple images and channel contains something
    like RGB or color channel. This function helps you get your inputs
    into that format. It accepts either a single file, a list of files,
    or a single directory containing images, will load them in,
    normalize them to lie between 0 and 1, convert them to float32,
    optionally convert them to grayscale, make them tensors, and get
    them into the right shape.

    Parameters
    ----------
    paths
        A str or list of strs. If a list, must contain paths of image
        files. If a str, can either be the path of a single image file
        or of a single directory. If a directory, we try to load every
        file it contains (using imageio.imread) and skip those we
        cannot (thus, for efficiency you should not point this to a
        directory with lots of non-image files). This is NOT recursive.
    as_gray
        Whether to convert the images into grayscale or not after
        loading them. If False, we do nothing. If True, we call
        skimage.color.rgb2gray on them.

    Returns
    -------
    images
        4d tensor containing the images.
    """
    try:
        paths = pathlib.Path(paths)
        if paths.is_file():
            paths = [paths]
        elif paths.is_dir():
            paths = [path for path in paths.iterdir()]
        else:
            if not paths.exists():
                raise FileNotFoundError(f"File {paths} not found!")

    except TypeError:
        # assume it is an iterable of paths already
        pass

    images = []
    for p in paths:
        # convert to pathlib path
        p = pathlib.Path(p)
        if not p.exists():
            raise FileNotFoundError(f"File {p} not found!")

        try:
            im = iio.imread(p)
        except ValueError:
            warnings.warn(
                f"Unable to load in file {p}, it's probably not an image, skipping..."
            )
            continue
        # make it a float32 array with values between 0 and 1
        im = im / np.iinfo(im.dtype).max
        if im.ndim > 2:
            if as_gray:
                # From scikit-image 0.19 on, it will treat 2d signals as 1d
                # images with 3 channels, so only call rgb2gray when it's more
                # than 2d
                try:
                    im = color.rgb2gray(im)
                except ValueError:
                    # then maybe this is an rgba image instead
                    im = color.rgb2gray(color.rgba2rgb(im))
            else:
                # RGB(A) dimension ends up on the last one, so we rearrange
                im = np.moveaxis(im, -1, 0)
        elif im.ndim == 2 and not as_gray:
            # then expand this grayscale image to the rgb representation
            im = np.expand_dims(im, 0).repeat(3, 0)
        images.append(im)
    if len(set([i.shape for i in images])) > 1:
        raise ValueError(
            "All images must be the same shape but got the following: "
            f"{[i.shape for i in images]}"
        )
    images = torch.as_tensor(np.array(images), dtype=torch.float32)
    if as_gray:
        if images.ndimension() != 3:
            raise ValueError(
                "For loading in images as grayscale, this should be a 3d tensor!"
            )
        images = images.unsqueeze(1)
    else:
        if images.ndimension() == 3:
            # either this was a single color image:
            # so add the batch dimension
            #  or multiple grayscale images:
            # so add channel dimension
            images = images.unsqueeze(0) if len(paths) > 1 else images.unsqueeze(1)
    if images.ndimension() != 4:
        raise ValueError(
            "Somehow ended up with other than 4 dimensions! Not sure how we got here"
        )
    return images


def convert_float_to_int(im: np.ndarray, dtype=np.uint8) -> np.ndarray:
    r"""Convert image from float to 8 or 16 bit image

    We work with float images that lie between 0 and 1, but for saving
    them (either as png or in a numpy array), we want to convert them to
    8 or 16 bit integers. This function does that by multiplying it by
    the max value for the target dtype (255 for 8 bit 65535 for 16 bit)
    and then converting it to the proper type.

    We'll raise an exception if the max is higher than 1, in which case
    we have no idea what to do.

    Parameters
    ----------
    im
        The image to convert
    dtype
        The target data type.  {np.uint8, np.uint16}

    Returns
    -------
    im
        The converted image, now with dtype=dtype

    Notes
    -----

    """
    if im.max() > 1:
        raise Exception(
            f"all values of im must lie between 0 and 1, but max is {im.max()}"
        )
    return (im * np.iinfo(dtype).max).astype(dtype)


def polar_radius(
    size: int | tuple[int, int],
    exponent: float = 1.0,
    origin: int | tuple[int, int] | None = None,
    device: str | torch.device | None = None,
) -> Tensor:
    """Make distance-from-origin (r) matrix

    Compute a matrix of given size containing samples of a radial ramp
    function, raised to given exponent, centered at given origin.

    Parameters
    ----------
    size
        If an int, we assume the image should be of dimensions `(size,
        size)`. if a tuple, must be a 2-tuple of ints specifying the
        dimensions.
    exponent
        The exponent of the radial ramp function.
    origin
        The center of the image. if an int, we assume the origin is at
        `(origin, origin)`. if a tuple, must be a 2-tuple of ints
        specifying the origin (where `(0, 0)` is the upper left).  if
        None, we assume the origin lies at the center of the matrix,
        `(size+1)/2`.
    device
        The device to create this tensor on.

    Returns
    -------
    res
        The polar radius matrix.
    """
    if not hasattr(size, "__iter__"):
        size = (size, size)

    if origin is None:
        origin = ((size[0] + 1) / 2.0, (size[1] + 1) / 2.0)
    elif not hasattr(origin, "__iter__"):
        origin = (origin, origin)

    xramp, yramp = torch.meshgrid(
        torch.arange(1, size[1] + 1, device=device) - origin[1],
        torch.arange(1, size[0] + 1, device=device) - origin[0],
        indexing="xy",
    )

    if exponent <= 0:
        # zero to a negative exponent raises:
        # ZeroDivisionError: 0.0 cannot be raised to a negative power
        r = xramp**2 + yramp**2
        res = np.power(r, exponent / 2.0, where=(r != 0))
    else:
        res = (xramp**2 + yramp**2) ** (exponent / 2.0)
    return res


def polar_angle(
    size: int | tuple[int, int],
    phase: float = 0.0,
    origin: int | tuple[float, float] | None = None,
    direction: Literal["clockwise", "counter-clockwise"] = "clockwise",
    device: torch.device | None = None,
) -> Tensor:
    """Make polar angle matrix (in radians).

    Compute a matrix of given size containing samples of the polar angle (in radians,
    increasing in user-defined direction from the X-axis, ranging from -pi to pi),
    relative to given phase, about the given origin pixel.

    Note that by default, the angle increases in a clockwise direction, which is NOT the
    standard mathematical convention. Use the ``direction`` argument to change that
    behavior.

    Parameters
    ----------
    size
        If an int, we assume the image should be of dimensions `(size, size)`. if a
        tuple, must be a 2-tuple of ints specifying the dimensions
    phase
        The phase of the polar angle function (in radians, clockwise from the X-axis)
    origin
        The center of the image. if an int, we assume the origin is at
        `(origin, origin)`. if a tuple, must be a 2-tuple of ints specifying the origin
        (where `(0, 0)` is the upper left). If None, we assume the origin lies at the
        center of the matrix, `(size+1)/2`.
    direction
        Whether the angle increases in a clockwise or counter-clockwise direction from
        the x-axis. The standard mathematical convention is to increase
        counter-clockwise, so that 90 degrees corresponds to the positive y-axis.
    device
        The device to create this tensor on.

    Returns
    -------
    res
        The polar angle matrix

    """
    if direction not in ["clockwise", "counter-clockwise"]:
        raise ValueError(
            "direction must be one of {'clockwise', 'counter-clockwise'}, "
            f"but received {direction}!"
        )

    if not hasattr(size, "__iter__"):
        size = (size, size)

    if origin is None:
        origin = ((size[0] + 1) / 2.0, (size[1] + 1) / 2.0)
    elif not hasattr(origin, "__iter__"):
        origin = (origin, origin)

    xramp, yramp = torch.meshgrid(
        torch.arange(1, size[1] + 1, device=device) - origin[1],
        torch.arange(1, size[0] + 1, device=device) - origin[0],
        indexing="xy",
    )
    if direction == "counter-clockwise":
        yramp = torch.flip(yramp, [0])

    res = torch.atan2(yramp, xramp)

    res = ((res + (np.pi - phase)) % (2 * np.pi)) - np.pi

    return res


def _find_min_int(vals):
    """Find the minimum non-negative int not in an iterable.

    Parameters
    ----------
    vals : iterable
        iterable of ints or iterables of ints

    Returns
    -------
    min_idx : int
        minimum non-negative int

    """
    flat_vals = []
    for v in vals:
        try:
            flat_vals.extend(v)
        except TypeError:
            flat_vals.append(v)
    flat_vals = set(flat_vals)
    try:
        poss_vals = set(np.arange(max(flat_vals) + 1))
    except ValueError:
        # then this is empty sequence and thus we should return 0
        return 0
    try:
        min_int = min(poss_vals - flat_vals)
    except ValueError:
        min_int = max(flat_vals) + 1
    return min_int


def _check_tensor_equality(
    x: Tensor,
    y: Tensor,
    xname: str = "x",
    yname: str = "y",
    rtol: float = 1e-5,
    atol: float = 1e-8,
    error_prepend_str: str = "Different {error_type}",
    error_append_str: str = "",
):
    """Check two tensors for equality: device, size, dtype, and values.

    Raises a ValueError (with informative error messages) if any of the above are not
    equal.

    Parameters
    ----------
    x, y :
        The tensors to compare
    xname, yname :
        Names of the tensors, used in error messages.
    rtol, atol :
        Relative and absolute tolerance for value comparison, passed to
        ``torch.allclose``
    error_prepend_str :
        String to start error message with, should contain the string-formatting field
        "{error_type}"
    error_append_str :
        String to finish error message with

    """
    error_str = (
        f"{error_prepend_str}"
        f"\n{xname}: {{xvalue}}"
        f"\n{yname}: {{yvalue}}"
        f"{{difference}}"
        f"{error_append_str}"
    )
    if x.device != y.device:
        error_str = error_str.format(
            error_type="device", xvalue=x.device, yvalue=y.device, difference=""
        )
        raise ValueError(error_str)
    # they're allowed to be different shapes if they both have 1 element (e.g., a scalar
    # and a 1-element tensor)
    if x.shape != y.shape and not (x.nelement() == y.nelement() == 1):
        error_str = error_str.format(
            error_type="shape", xvalue=x.shape, yvalue=y.shape, difference=""
        )
        raise ValueError(error_str)
    elif x.dtype != y.dtype:
        error_str = error_str.format(
            error_type="dtype", xvalue=x.dtype, yvalue=y.dtype, difference=""
        )
        raise ValueError(error_str)
    elif not torch.allclose(x, y, rtol=rtol, atol=atol):
        error_str = error_str.format(
            error_type="values", xvalue=x, yvalue=y, difference=f"\nDifference: {x - y}"
        )
        raise ValueError(error_str)
