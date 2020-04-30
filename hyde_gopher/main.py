from flask import Flask, url_for
from flask_gopher import GopherExtension, GopherRequestHandler

app = Flask(__name__)
gopher = GopherExtension(app)


@app.route('/')
def index():
    return gopher.render_menu(
        gopher.menu.title('My GopherHole'),
        gopher.menu.dir('Home', url_for('index')),
        gopher.menu.info("Look Ma, it's a gopher server!"))


def run():
    app.run('::', 7070, request_handler=GopherRequestHandler)
