# hyde-gopher

Serve your [Hyde](https://hyde.github.io/) site over
[Gopher](https://en.wikipedia.org/wiki/Gopher_(protocol)).
(This is primarily made possible by [flask-gopher](https://github.com/michael-lazar/flask-gopher), yay.)

## Installation

Install the package via `python3 -m pip install .` or replace `hyde-gopher`
with `python3 -m hyde_gopher.main` in the following steps.

## Usage

### Setup

As Gopher supports only absolute links and there's no such thing as a `Host` header,
hyde-gopher needs to know the absolute base path of your site when generating the
static site. (If you're using the built-in webserver this is currently being guessed
from the bind configuration which may lead to broken links. Please use the built-in
webserver just for local tests and not for internet-facing deployments.)

To do so, add the following line to your `site.yaml`:

```yaml
gopher_base_url: gopher://gopher.mysite.invalid:71/~user/
```

### Serve

You can use the built-in webserver for a quick test
 - and also for pre-viewing your site while editing it.

To do so, run `hyde-gopher serve`.

Per default, this will serve the site from the current working directory
at <gopher://localhost:7070/>, placing generated files into `deploy_gopher/`.
(You can change this, see `hyde-gopher -h` and `hyde-goper serve -h` for more options.)

### Generate

The primary purpose of hyde-gopher is to generate a static site (just like hyde's).

To do so, run `hyde-gopher gen`.

Per default, this will generate a static version of the site from the current
working directory to the folder `deploy_gopher/`.
(You can change this, see `hyde-gopher -h` and `hyde-goper gen -h` for more options.)

## Knonwn issues / TODO

 * index pages look very meager
 * links in pages are not rendered as links
 * just HTML files and folders are considered
