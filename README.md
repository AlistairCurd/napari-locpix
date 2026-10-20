# napari-locpix

[![License MIT](https://img.shields.io/pypi/l/napari-locpix.svg?color=green)](https://github.com/oubino/napari-locpix/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-locpix.svg?color=green)](https://pypi.org/project/napari-locpix)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-locpix.svg?color=green)](https://python.org)
[![tests](https://github.com/oubino/napari-locpix/workflows/tests/badge.svg)](https://github.com/oubino/napari-locpix/actions)
[![codecov](https://codecov.io/gh/oubino/napari-locpix/branch/main/graph/badge.svg)](https://codecov.io/gh/oubino/napari-locpix)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-locpix)](https://napari-hub.org/plugins/napari-locpix)

Load in SMLM data and annotate within napari

----------------------------------

This [napari] plugin was generated with [Cookiecutter] using [@napari]'s [cookiecutter-napari-plugin] template.

<!--
Don't miss the full getting started guide to set up your new package:
https://github.com/napari/cookiecutter-napari-plugin#getting-started

and review the napari docs for plugin developers:
https://napari.org/stable/plugins/index.html
-->

## Installation

### Compatibility

Tested with napari 0.9.2.

### Install

Install napari via [pip]:

    pip install "napari[all]"

You can install `napari-locpix` via [pip]:

    pip install napari-locpix

To install latest development version :

    pip install git+https://github.com/oubino/napari-locpix.git


## Usage

First launch napari

    napari

Then can find the plugin in napari, in the plugins menu, titled 'Annotate (napari-locpix)'

This plugin allows a user to

1. Read in SMLM data
2. Visualise SMLM data in a histogram
3. Add segmentations to the data
4. Extract the underlying localisations from the segmentations

### IO

The input data can be in the form of a .csv or .parquet.

We expect there to be 4 columns at least, which should he identified in the file column selection:

* X coordinate
* Y coordinate
* Frame
* Channel

If the data has been annotated with this software and written to a Parquet file, we can also load this in ("Load annotated data"). A napari Labels layer will overlay localisations previously annotated as foreground/gt_label:1 (see Annotations).

Using "Load annotated data" is not currently supported for CSV files. However, the annotated data may still be read in with "Load raw data", and "gt_label" can be chosen as the Channel in File column selection (acquisition channel information will then not be rendered).

### Visualisation

Using the render button you can render the loaded in data according to the histogram settings

X/Y bins defines the number of bins for the histogram. Use the X/Y bins ratio to retain the original aspect ratio of the FOV (or close) in the visualisation, if desired. The aspect ratio in this rendering does not affect the underlying localisation position data.

Vis interpolation defines how to interpolate the image before viewing

### Annotations

Annotations of localisations can be added using napari's viewer.

Click on the napari button to create a new Labels layer. Label localisations by overlaying with the polygon, paintbrush tool, etc.

Localisations will get a new column, "gt_label", when the data is written to CSV or Parquet. Localisations will have gt_label: 0, unless they are underneath the labels layer annotations, in which case they will have gt_label: 1.

For saving in Parquet format, optionally change the names in the "Label map", which will be stored in metadata.

Rename the new napari Labels layer to "Labels", otherwise the annotations will not be saved.

### Output

The data can be output to a .parquet or a .csv.

"Drop localisations with zero label": This gives you the option to only save the localisations which have been annotated with the Labels layer.

Channel labels allows you to give a real name label to each of the channels e.g. Chan 0 label: 'Alexa 647'

## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [MIT] license,
"napari-locpix" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin

[file an issue]: https://github.com/oubino/napari-locpix/issues

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
