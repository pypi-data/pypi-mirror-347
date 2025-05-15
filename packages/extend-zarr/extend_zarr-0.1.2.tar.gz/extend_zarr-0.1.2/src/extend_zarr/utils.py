import logging
import warnings
from collections.abc import Hashable, MutableMapping
from os import PathLike
from typing import TypeVar

import dask.array as da
import numpy as np
import xarray as xr
from xarray.core.coordinates import DataArrayCoordinates

ArrayLike = TypeVar('ArrayLike', np.ndarray, xr.DataArray)

logger = logging.getLogger(__name__)


def concat_arrays_with_overlap(a: ArrayLike, b: ArrayLike) -> np.ndarray:
    """Concatenate two arrays with overlap.

    This function is used to concatenate two arrays with removing any
    overlapping elements.
    If overlap, the overlapping part must be at the head of b.

    e.g. a = [3, 1, 4], b = [1, 4, 5, 9] -> [3, 1, 4, 5, 9]
         a = [3, 1, 4], b = [3, 1] -> [3, 1, 4]

    Requirements:
        - a and b must be 1D numpy arrays.
        - elements of a and b must be unique except elements in overlap.

    Parameters
    ----------
    a: ArrayLike
        1D array to be concatenated.
    b: ArrayLike
        1D array to be concatenated.

    Returns
    -------
    out: np.ndarray
        Concatenated 1D numpy array.

    """
    if isinstance(a, xr.DataArray):
        a = a.to_numpy()
    if isinstance(b, xr.DataArray):
        b = b.to_numpy()
    if (np.unique(a).size != a.size) or (np.unique(b).size != b.size):
        msg = 'items in a and b must be unique.'
        raise ValueError(msg)
    if len(a) == 0:
        return b
    if len(b) == 0:
        return a
    matches = np.where(a == b[0])[0]
    if len(matches) == 0:
        out = np.concatenate((a, b))
    elif len(matches) == 1:
        overlap_length = min(len(a[matches[0] :]), len(b))
        if not np.array_equal(
            a[matches[0] : matches[0] + overlap_length], b[:overlap_length]
        ):
            msg = (
                'items in a and b must be unique except elements in overlap. '
            )
            raise ValueError(msg)
        if overlap_length == len(b):
            return a
        if overlap_length == len(a):
            return b
        out = np.concatenate((a[: matches[0]], b))
    else:
        msg = 'items in a and b must be unique except elements in overlap. '
        raise ValueError(msg)

    if np.unique(out).size != out.size:
        msg = 'items in a and b must be unique except elements in overlap.'
        raise ValueError(msg)

    return out


def find_subarray_slice(array: ArrayLike, subarray: ArrayLike) -> slice | None:
    """Find the slice of subarray in array.

    If subarray is not in array, return None.

    Parameters
    ----------
    subarray: ArrayLike
        1D Subarray to be searched.
    array: ArrayLike
        1D Array to be searched in.
        The elements of the array should be unique.

    Returns
    -------
    slice | None
        Slice of subarray in array.
        If subarray is not in array, return None.

    """
    if isinstance(subarray, xr.DataArray):
        subarray = subarray.to_numpy()
    if isinstance(array, xr.DataArray):
        array = array.to_numpy()
    if subarray.ndim != 1 or array.ndim != 1:
        msg = 'subarray and array must be 1D arrays.'
        raise ValueError(msg)
    if len(np.unique(array)) != len(array):
        msg = 'array must be unique.'
        raise ValueError(msg)

    if len(subarray) > len(array):
        return None

    try:
        start = np.where(array == subarray[0])[0][0]
        end = start + len(subarray)
        if np.array_equal(array[start:end], subarray):
            return slice(start, end)
    except IndexError:
        # subarray is not in array
        return None


def extend_zarr(
    dataarray: xr.DataArray,
    store: MutableMapping | str | PathLike,
    var_name: str,
    coords: dict[Hashable, np.ndarray] | DataArrayCoordinates | None = None,
    fill_value: float = 0,
) -> None:
    """Expand dataarray in zarr store.

    This function expands the zarr store with new dataarray.
    The dims of the dataarray must be same as that of a DataArray specified by
    var_name in the zarr store.

    Limitations:
        Coordinates needs to be unique 1D arrays.
        dataarray can only be appended to tail of the zarr store.


    Parameters
    ----------
    dataarray: xr.DataArray
        DataArray to be added to zarr store.
    store: MutableMapping | str | PathLike
        Zarr store to be expanded.
    var_name: str
        Variable name of the zarr store.
    coords: dict[Hashable, np.ndarray] | None
        New coordinates for the zarr store.
        If None, coordinates that need to be extended are extended after
        existing coordinates and the data is stored.
    fill_value: float
        If the expanded zarrstore coordinates are not covered by the region of
        the given dataarray, the values there will be filled with fill_value.


    """
    if coords is None:
        coords = {}
    dataset = xr.open_zarr(store)

    # validate chunksizes in zarr store
    if not all(
        len(set(cs[:-1])) <= 1
        for _, cs in dataset[var_name].chunksizes.items()
    ):
        msg = 'Chunksizes in zarr store are not normalized.'
        raise ValueError(msg)

    dataarray_coords = dataarray.coords

    # warn dtype mismatch
    if dataset[var_name].dtype != dataarray.dtype:
        msg = (
            f'Dataarray dtype {dataarray.dtype} is different from '
            f'zarr store dtype {dataset[var_name].dtype}.'
        )
        logger.warning(msg)

    # validate dataarrays
    for coord_name, coordinate in dataset[var_name].coords.items():
        if coord_name not in dataarray_coords:
            msg = f'Coordinate {coord_name} is not in dataarray.'
            raise DimNotExistsError(msg)
        if coordinate.ndim != 1 or dataarray_coords[coord_name].ndim != 1:
            msg = f'Coordinate {coord_name} is not 1D.'
            raise ValueError(msg)
        if (
            not (dataset[coord_name] == dataarray_coords[coord_name][0]).any()
        ) and (
            (dataset[coord_name] == dataarray_coords[coord_name][-1]).any()
        ):
            msg = (
                f"The tail of dataarray's coordinate '{coord_name}' "
                "is overlapped with the head of dataset's coordinate in the "
                'store. This function currently only supports adding a '
                'dataset to the tail of the ds coordinate.'
            )
            raise ValueError(msg)

    region = {}
    store_coords = dataset[var_name].coords
    for coord_name, coordinate in store_coords.items():
        new_coord = coords.get(
            coord_name,
            concat_arrays_with_overlap(
                a=coordinate,
                b=dataarray_coords[coord_name],
            ),
        )

        slice_ = find_subarray_slice(
            array=new_coord, subarray=dataarray_coords[coord_name]
        )
        if slice_ is None:
            msg = (
                f'Coordinate {coord_name} of dataarray is not completely '
                'contained in new coordinates.'
            )
            raise DimIsNotSlicableError(msg)

        region[coord_name] = slice_

        # expand the zarr
        if len(coordinate) == len(new_coord):
            continue

        # reload the zarr store to update coordinates updated in the previous
        # loop.
        # OPTIMIZE: Instead of accessing the zarr store in each loop, we can
        #           store the coordinates in a dictionary and use them.
        store_coords = xr.open_zarr(store)[var_name].coords

        empty_array_coord_x = new_coord[
            np.where(new_coord == coordinate[-1].data)[0][0] + 1 :
        ]
        empty_array_shape = (
            len(empty_array_coord_x),
            *[c.size for n, c in store_coords.items() if n != coord_name],
        )
        empty_array = da.zeros(empty_array_shape, dtype=dataarray.dtype)
        if fill_value != 0:
            empty_array[:] = fill_value
        empty_array_coords = {
            coord_name: empty_array_coord_x,
            **{
                n: c.values for n, c in store_coords.items() if n != coord_name
            },
        }
        empty_dataarray = xr.DataArray(
            empty_array,
            coords=empty_array_coords,
            dims=empty_array_coords.keys(),
        )

        # expand the zarr store with empty dataarray
        with warnings.catch_warnings():
            warnings.filterwarnings(
                'ignore',
                message='The codec `vlen-utf8` is currently '
                'not part in the Zarr format 3 specification.*',
            )
            empty_dataarray.to_dataset(name=var_name).to_zarr(
                store, append_dim=coord_name, consolidated=None
            )

    # update the zarr store values with dataarray
    with warnings.catch_warnings():
        warnings.filterwarnings(
            'ignore',
            message='The codec `vlen-utf8` is currently '
            'not part in the Zarr format 3 specification.*',
        )

        dataarray.to_dataset(name=var_name).to_zarr(
            store, mode='a', region=region
        )


class DimNotExistsError(Exception):
    """Dimension is not in target DataArray.

    Raised when a dimension is not in target DataArray.

    """


class DimIsNotSlicableError(Exception):
    """Dimension is not aligned.

    Raised when child DataArray's dimension is not aligned with parent
    DataArray's dimension.
    Some elements are not equal.

    """
