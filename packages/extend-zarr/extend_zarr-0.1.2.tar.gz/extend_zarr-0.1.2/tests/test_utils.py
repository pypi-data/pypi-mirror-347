from pathlib import Path

import dask.array as da
import numpy as np
import xarray as xr

from extend_zarr import utils


class TestAppendDataarrayToZarr:
    def test_dataarray(self, path_to_zarr: Path):
        """Append a DataArray to a Zarr store.

        New dataarray has the same shape and coordinates as the existing zarr
        except one dimension (year).

        This operation extends only one dimension (year) of the Zarr store.
        The dataarray is chunked with the same chunk sizes as the existing
        Zarr store.

        """
        new_coords = {
            'x': np.arange(10_000, 10_010, dtype=np.int32),
            'y': np.arange(20_000, 20_010, dtype=np.int32),
            'band': ['red', 'green', 'blue'],
            'year': [2015, 2016],
        }
        shape = tuple(len(c) for c in new_coords.values())
        new_array = da.arange(int(np.prod(shape))).reshape(shape)
        new_dataarray = xr.DataArray(
            data=new_array,
            dims=new_coords.keys(),
            coords=new_coords,
        )

        utils.extend_zarr(
            dataarray=new_dataarray,
            store=path_to_zarr,
            var_name='value',
        )

        updated_dataarray = xr.open_zarr(path_to_zarr).value

        assert updated_dataarray.shape == (10, 10, 3, 4)
        assert updated_dataarray.chunksizes['year'] == (1, 1, 1, 1)
        assert updated_dataarray.chunksizes['band'] == (2, 1)
        np.testing.assert_array_equal(
            updated_dataarray.sel(**new_coords).values, new_array
        )

    def test_multi_nonaligned(self, path_to_zarr: Path):
        """Append a DataArray to a Zarr store with multiple dimensions.

        New dataarray has multiple coordinations in mudimensions (year, band)
        that are not in the existing zarr.

        """
        new_coords = {
            'x': np.arange(10_000, 10_010, dtype=np.int32),
            'y': np.arange(20_000, 20_010, dtype=np.int32),
            'band': ['red', 'green'],
            'year': [2015, 2016],
        }
        shape = tuple(len(c) for c in new_coords.values())
        new_array = da.arange(np.prod(shape)).reshape(shape)
        new_dataarray = xr.DataArray(
            data=new_array, dims=new_coords.keys(), coords=new_coords
        )

        utils.extend_zarr(
            dataarray=new_dataarray,
            store=path_to_zarr,
            var_name='value',
            fill_value=-9999,
        )

        updated_dataarray = xr.open_zarr(path_to_zarr).value

        assert updated_dataarray.shape == (10, 10, 3, 4)
        assert updated_dataarray.chunksizes['year'] == (1, 1, 1, 1)
        assert updated_dataarray.chunksizes['band'] == (2, 1)
        np.testing.assert_array_equal(
            updated_dataarray.sel(**new_coords).values, new_array
        )
        assert np.all(
            updated_dataarray.sel(year=[2015, 2016], band='blue').values
            == -9999
        )

    def test_multi_nonaligned_middle(self, path_to_zarr: Path):
        new_coords = {
            'x': np.arange(10_000, 10_010, dtype=np.int32),
            'y': np.arange(20_000, 20_010, dtype=np.int32),
            'band': ['green'],
            'year': [2015, 2016],
        }

        shape = tuple(len(c) for c in new_coords.values())
        new_array = da.arange(np.prod(shape)).reshape(shape)
        new_dataarray = xr.DataArray(
            data=new_array, dims=new_coords.keys(), coords=new_coords
        )

        utils.extend_zarr(
            dataarray=new_dataarray,
            store=path_to_zarr,
            var_name='value',
            fill_value=-9999,
        )

        updated_dataarray = xr.open_zarr(path_to_zarr).value

        assert updated_dataarray.shape == (10, 10, 3, 4)
        assert updated_dataarray.chunksizes['year'] == (1, 1, 1, 1)
        assert updated_dataarray.chunksizes['band'] == (2, 1)
        np.testing.assert_array_equal(
            updated_dataarray.sel(**new_coords).values, new_array
        )
        assert np.all(
            updated_dataarray.sel(
                year=[2015, 2016], band=['red', 'blue']
            ).values
            == -9999
        )

    def test_expand_multidim(self, path_to_zarr: Path):
        new_coords = {
            'x': np.arange(10_000, 10_010, dtype=np.int32),
            'y': np.arange(20_000, 20_010, dtype=np.int32),
            'band': ['green', 'blue', 'nir'],
            'year': [2015, 2016],
        }
        shape = tuple(len(c) for c in new_coords.values())
        new_array = da.arange(np.prod(shape)).reshape(shape)
        new_dataarray = xr.DataArray(
            data=new_array, dims=new_coords.keys(), coords=new_coords
        )

        utils.extend_zarr(
            dataarray=new_dataarray,
            store=path_to_zarr,
            var_name='value',
            fill_value=-9999,
        )

        updated_dataarray = xr.open_zarr(path_to_zarr).value

        assert updated_dataarray.shape == (10, 10, 4, 4)
        assert updated_dataarray.chunksizes['year'] == (1, 1, 1, 1)
        assert updated_dataarray.chunksizes['band'] == (2, 2)
        np.testing.assert_array_equal(
            updated_dataarray.sel(**new_coords).values, new_array
        )
        assert np.all(
            updated_dataarray.sel(year=[2012, 2013], band='nir').values
            == -9999
        )
        assert np.all(
            updated_dataarray.sel(year=[2015, 2016], band='red').values
            == -9999
        )

    def test_coord_option(self, path_to_zarr: Path):
        new_coords = {
            'x': np.arange(10_000, 10_010, dtype=np.int32),
            'y': np.arange(20_000, 20_010, dtype=np.int32),
            'band': ['red', 'green'],
            'year': [2015, 2016],
        }
        shape = tuple(len(c) for c in new_coords.values())
        new_array = da.arange(np.prod(shape)).reshape(shape)
        new_dataarray = xr.DataArray(
            data=new_array, dims=new_coords.keys(), coords=new_coords
        )

        utils.extend_zarr(
            dataarray=new_dataarray,
            store=path_to_zarr,
            var_name='value',
            fill_value=-9999,
            coords={'year': np.array([2012, 2013, 2014, 2015, 2016])},
        )

        updated_dataarray = xr.open_zarr(path_to_zarr).value

        assert updated_dataarray.shape == (10, 10, 3, 5)
        assert updated_dataarray.chunksizes['year'] == (1, 1, 1, 1, 1)
        assert updated_dataarray.chunksizes['band'] == (2, 1)
        np.testing.assert_array_equal(
            updated_dataarray.sel(**new_coords).values, new_array
        )
        assert np.all(
            updated_dataarray.sel(year=[2015, 2016], band='blue').values
            == -9999
        )
        assert np.all(updated_dataarray.sel(year=[2014]).values == -9999)

    def test_overwrite(self, path_to_zarr: Path):
        new_coords = {
            'x': np.arange(10_000, 10_010, dtype=np.int32),
            'y': np.arange(20_000, 20_010, dtype=np.int32),
            'band': ['green', 'blue'],
            'year': [2013, 2014],
        }
        shape = tuple(len(c) for c in new_coords.values())
        new_array = da.arange(np.prod(shape)).reshape(shape)
        new_dataarray = xr.DataArray(
            data=new_array, dims=new_coords.keys(), coords=new_coords
        )

        utils.extend_zarr(
            dataarray=new_dataarray,
            store=path_to_zarr,
            var_name='value',
            fill_value=-9999,
        )

        updated_dataarray = xr.open_zarr(path_to_zarr).value

        assert updated_dataarray.shape == (10, 10, 3, 3)
        assert updated_dataarray.chunksizes['year'] == (1, 1, 1)
        assert updated_dataarray.chunksizes['band'] == (2, 1)
        np.testing.assert_array_equal(
            updated_dataarray.sel(**new_coords).values, new_array
        )
        assert np.all(
            updated_dataarray.sel(year=[2014], band='red').values == -9999
        )
