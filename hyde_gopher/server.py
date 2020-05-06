from flask import Flask
from flask_gopher import GopherExtension, GopherRequestHandler
from hyde.plugin import Plugin
from hyde.template import Template
from . import generator


def serve(site, address, port):
    app = Flask(__name__)
    gopher = GopherExtension(app)
    generator.gopher = gopher
    generator.gopher_menu = lambda: gopher.menu
    site.config.base_path = "/"
    plugins = Plugin(site)
    plugins.load_all(site)
    events = Plugin.get_proxy(site)
    generator_proxy = generator.GeneratorProxy(
        context_for_path=None,
        preprocessor=events.begin_text_resource,
        postprocessor=events.text_resource_complete,
    )
    templates = Template.find_template(site)
    templates.configure(site)
    templates.configure(site, engine=generator_proxy)
    events.template_loaded(templates)
    macros = templates.loader.load(templates.env, "macros.j2")
    templates.env.globals.update(macros.module.__dict__)
    stack = list()
    site.content.load()
    stack.append(site.content)
    events.begin_generation()
    events.begin_site()
    while stack:
        current = stack.pop()
        app.add_url_rule(
            current.url, current.relative_path,
            lambda c=current: generator.generate_node(site, events, c)
        )
        for child in current.resources:
            app.add_url_rule(
                child.url, child.relative_path,
                lambda c=child: generator.generate_resource(
                    site, events, templates, c
                )
            )
        for child in current.child_nodes:
            stack.append(child)
    app.run(address, port, request_handler=GopherRequestHandler)
    # TODO: will never be called, probably
    events.site_complete()
    events.generation_complete()
