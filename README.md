 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![conda build](https://github.com/mschlund/lsystems/actions/workflows/python-package-conda.yml/badge.svg) ![poetry-build](https://github.com/mschlund/lsystems/actions/workflows/python-package-poetry.yml/badge.svg)

# lsystems
Playing around with lsystems and drawing the resulting string with the help of an svg-turtle as a curve.
See the corresponding blog-post https://maximilianschlund.wordpress.com/2023/01/06/drawing-curves-with-l-systems/
## Build
Prerequisites:
- install poetry (cf. https://python-poetry.org/docs/)

1. set up environment
```$ poetry install```

2. run the draw-curves notebook: Either do

``` $ cd notebooks ```

``` $ jupyter-notebook draw_curves.ipynb ```
or open the notebook in your favorite ide.


### Conda (deprecated)
Prerequisites:
- install anaconda (see https://docs.anaconda.com/anaconda/install/silent-mode/)

Then follow these steps:

1. setup environment

```$ conda env create -f env.yml```

```$ conda activate lsystems```

2. install this package in editable mode
``` python -m pip install -e . ```

3. run the draw-curves notebook: Either do

``` $ cd notebooks ```

``` $ jupyter-notebook draw_curves.ipynb ```
or open the notebook in your favorite ide.

## Tests
Tests can be executed via:

```$ python -m unittest discover -s ./test -p test*.py```
