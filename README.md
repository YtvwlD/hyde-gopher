# hyde-gopher

[![Build Status](https://travis-ci.org/YtvwlD/hyde-gopher.svg?branch=master)](https://travis-ci.org/YtvwlD/hyde-gopher)

Serve your [Hyde](https://hyde.github.io/) site over
[Gopher](https://en.wikipedia.org/wiki/Gopher_(protocol)).
(This is primarily made possible by [flask-gopher](https://github.com/michael-lazar/flask-gopher), yay.)

## Installation

### From source

If you cloned or downloaded the repository, you can install the package with:

```shell
python3 -m pip install .
```

If you don't want to install anything, you can replace `hyde-gopher` with
`python3 -m hyde_gopher.main` in the following steps.

### Release

You can install the latest relase from PyPI by running

```shell
python3 -m pip install hyde-gopher
```

## Usage

### Setup

As Gopher supports only absolute links and there's no such thing as a `Host` header,
hyde-gopher needs to know the absolute base path of your site when generating the
static site. (If you're using the built-in webserver this is currently being guessed
from the bind configuration which may lead to broken links. Please use the built-in
webserver just for local tests and not for internet-facing deployments.)

There are also a few things you might want to configure but don't have to.

To do so, add the following line to your `site.yaml`:

```yaml
gopher_base_url: gopher://gopher.mysite.invalid:71/~user/ # needed
gopher_layout_root: layout_gopher # this is the default
gopher_width: 70 # this is the default
```

### Serve

You can use the built-in webserver for a quick test
 - and also for pre-viewing your site while editing it.

To do so, run `hyde-gopher serve`.

Per default, this will serve the site from the current working directory
at <gopher://localhost:7070/>, placing generated files into `deploy_gopher/`.
(You can change this, see `hyde-gopher -h` and `hyde-gopher serve -h` for more options.)

### Generate

The primary purpose of hyde-gopher is to generate a static site (just like hyde's).

To do so, run `hyde-gopher gen`.

Per default, this will generate a static version of the site from the current
working directory to the folder `deploy_gopher/`.
(You can change this, see `hyde-gopher -h` and `hyde-gopher gen -h` for more options.)

## Knonwn issues / TODO

 * links in pages are not rendered as links
 * images are only linked if you use a macro to render them
 * just HTML files, binaries and folders are considered
 * the layout folder is expected to exist, you can use the provided one

## Gotchas

hyde-gopher needs Python >= 3.6.

The currenty stable release of hyde (0.8.9) needs Python < 3.
You'll need to install the pre-release of hyde 0.9.0 to get this working:

```shell
python3 -m pip install git+https://github.com/hyde/hyde.git@V0.9.0
```
