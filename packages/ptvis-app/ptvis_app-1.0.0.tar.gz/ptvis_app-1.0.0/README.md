PTVis App
=========

GUI application for visualizing data on the periodic table.

![application screenshot](https://gitlab.com/naubuan/ptvis-app/-/raw/main/static/screenshot.png)

Requirements
------------

* Python version 3.10 or later
* Web browser for opening an application

Features
--------

* Visualizing data values by colors and sizes of table cells.
* Available for either numerical or non-numerical data values.
* Multiple table cell types: square, circle, bubble, pie, and polar bar.
* Multiple color palettes.
* Multiple saving formats: HTML, JPEG, PDF, PNG, and SVG.

Installation
------------

You can install PTVis App by, e.g., [pip](https://pip.pypa.io/):

```shell
python -m pip install ptvis-app
```

Usage
-----

### Launching application

An application is launched in a web browser tab by the following command:

```shell
ptvis-app
```

or alternatively, by the following command:

```shell
python -m ptvis_app
```

Options can be found by running the above commands with the ``--help`` option.

### Quitting application

Press ``Ctrl+C`` in the command line.

### Visualizing data

You can specify visualized data as columns of a CSV file. The procedure is as follows:

1. Select a CSV file by the ``File`` browser.
2. Select a column containing chemical elements by the ``Element column`` dropdown.
3. Select a column containing visualized values by the ``Value column`` dropdown.
4. Optionally select a column containing text labels by the ``Text column`` dropdown.

A type of table cell can be changed by the ``Cell type`` dropdown.

License
-------

[Apache License, Version 2.0](LICENSE.txt)
