# Extend Zarr

Library for writing a new DataArray to a Zarr file containing a DataArray.
If necessary, the Coordinates of the DataArray in the Zarr file is extended and
the DataArray data is written.

## Installation

```bash
pip install extend-zarr
```

## Usage

```python
from extend_zarr import extend_zarr

dataarray = ...  # DataArray to be written
zarr_path = ...  # Path to the Zarr file
extend_zarr(dataarray=dataarray,
            zarr_path=zarr_path,
            var_name='value')
```

A notebook explaining the behavior of the function is available in
[examples](https://github.com/eodcgmbh/extend-zarr/blob/main/examples/extend_zarr.ipynb).

## Limitations

The following limitations exists to the coordinates of the dataarray to which
this function can be applied.

- Coordinates needs to be unique 1D arrays.
- Dataarray can only be appended to tail of the zarr store.
