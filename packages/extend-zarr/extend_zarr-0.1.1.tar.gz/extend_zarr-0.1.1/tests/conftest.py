from pathlib import Path

import dask.array as da
import numpy as np
import pytest
import xarray as xr


@pytest.fixture
def path_to_zarr(tmp_path: Path) -> Path:
    """Path to a zarr file.

    Zarr file contains 4D arrays that dims are:
        {'x': 10, 'y': 10, 'band': 3, 'year': 2}
    and chunksizes as follows:
        {'x': (10,), 'y': (5, 5), 'band': (2, 1), 'year': (1, 1)}

    """
    path = tmp_path / 'test.zarr'
    # Create a 4D array with random data
    rng = da.random.default_rng(111)
    coords = {
        'x': np.arange(10_000, 10_010, dtype=np.int32),
        'y': np.arange(20_000, 20_010, dtype=np.int32),
        'band': ['red', 'green', 'blue'],
        'year': [2012, 2013],
    }
    chunks = ((10,), (5, 5), (2, 1), (1, 1))
    shape = tuple(len(c) for c in coords.values())
    array = (
        rng.integers(0, 100, np.prod(shape), dtype='int32')
        .reshape(shape)
        .rechunk(chunks)
    )
    # Create a zarr file
    dataarray = xr.DataArray(array, dims=coords.keys(), coords=coords)
    dataarray.to_dataset(name='value').to_zarr(path)
    return path
