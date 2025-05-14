# Contributing Guide

Thank you for considering contributing to this project!
This document outlines how to set up the development environment, format code,
run tests, and manage dependencies using [Pixi](https://pixi.sh/).

Before opening a pull request, **please create an issue** to discuss your
proposed changes.
This helps us coordinate and avoid duplicate work or unnecessary effort.

The following are specific commands that are useful in development.

To install pixi, run the following command (if not installed):

```bash
curl -fsSL https://pixi.sh/install.sh | sh
```

Format the code with:

```bash
pixi run --environment development style
```

To test the package, run:

```bash
pixi run test
```

Test with different zarr versions with:

```bash
# test with zarr2
pixi run --environment test-zarr2 test
# test with zarr3
pixi run --environment test-zarr3 test
```

To start Jupyter Lab, run:

```bash
pixi run --environment development jupyter lab
```

Run the following command to start environment in development mode:

```bash
pixi shell --environment development
```

Thank you again for your contributions!
