from pathlib import Path
from commando.util import getLoggerWithConsoleHandler
from bs4 import BeautifulSoup
from flask_gopher import GopherMenu, GopherExtension
from hyde.template import Template
from . import _version

logger = getLoggerWithConsoleHandler(__name__)

gopher = GopherExtension()
gopher.width = 70
gopher_menu = lambda: GopherMenu()  # TODO


def index(site):
    entries = [
        gopher_menu().dir(entry.name, entry.url)
        for entry in site.config.context.data.menu
    ]
    entries.insert(0, gopher_menu().title('Homepage'))
    entries.append(gopher_menu().info(f"Generated by hyde-gopher {_version}."))
    return gopher.render_menu(*entries)


def generate_node(site, node):
    if node.url == '/':
        return index(site)
    entries = [
        gopher_menu().dir(node.name, node.url)
        for node in node.child_nodes
    ]
    entries.insert(0, gopher_menu().title(node.name))
    entries.insert(1, gopher_menu().dir("..", node.parent.url))
    entries += [
        gopher_menu().dir(resource.name, resource.url)
        for resource in node.resources
    ]
    entries.append(gopher_menu().info(f"Generated by hyde-gopher {_version}."))
    return gopher.render_menu(*entries)


def generate_resource(site, templates, resource):
    if not resource.name.endswith(".html"):
        return ""  # TODO
    html = templates.render_resource(resource, site.context)
    soup = BeautifulSoup(html)
    entries = list()
    for line in soup.text.splitlines():
        while len(line) >= 70:
            entries.append(gopher_menu().info(line[:70]))
            line = line[70:]
        else:
            entries.append(gopher_menu().info(line))
    return gopher.render_menu(*entries)


def generate_all(site):
    templates = Template.find_template(site)
    templates.configure(site)
    macros = templates.loader.load(templates.env, "macros.j2")
    templates.env.globals.update(macros.module.__dict__)
    stack = list()
    site.content.load()
    stack.append(site.content)
    deploy_folder = Path(site.config.deploy_root)
    while stack:
        current = stack.pop()
        if current.name == "tags":
            continue  # TODO
        new_file = deploy_folder / current.relative_path / "index.gopher"  # TODO
        logger.debug(f"Generating {new_file}...")
        new_file.write_text(generate_node(site, current))
        for child in current.resources:
            new_file = deploy_folder / child.relative_path
            logger.debug(f"Generating {new_file}...")
            new_file.write_text(generate_resource(site, templates, child))
        for child in current.child_nodes:
            stack.append(child)
