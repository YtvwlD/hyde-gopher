# This file is based on Hyde's engine.py
from pathlib import Path
from commando import (
    Application,
    command,
    store,
    subcommand,
    true,
    version
)
from commando.util import getLoggerWithConsoleHandler
from hyde.model import Config
from hyde.site import Site
from . import server
from . import _version


class Engine(Application):
    def __init__(self, raise_exceptions=False):
        logger = getLoggerWithConsoleHandler('hyde-gopher')
        super(Engine, self).__init__(
            raise_exceptions=raise_exceptions,
            logger=logger
        )
    
    @command(
        description="hyde-gopher - build hyde sites for gopher",
        epilog='Use %(prog)s {command} -h to get help on individual commands'
    )
    @true('-x', '--raise-exceptions', default=None,
          help="Don't handle exceptions.")
    @version('--version', version='%(prog)s ' + _version)
    @store('-s', '--sitepath', default='.', help="Location of the hyde site")
    def main(self, args):
        """
        Will not be executed. A sub command is required. This function exists
        to provide common parameters for the subcommands and some generic stuff
        like version and metadata
        """
        if args.raise_exceptions in (True, False):
            self.raise_exceptions = args.raise_exceptions
        return Path(args.sitepath).absolute()
    
    @subcommand('serve', help='Serve the website')
    @store('-a', '--address', default='localhost', dest='address',
           help='The address where the website must be served from.')
    @store('-p', '--port', type=int, default=7070, dest='port',
           help='The port where the website must be served from.')
    @store('-c', '--config-path', default='site.yaml', dest='config',
           help='The configuration used to generate the site')
    def serve(self, args):
        """
        The serve command. Serves the site at the given
        deployment directory, address and port. Regenerates
        the entire site or specific files based on the request.
        """
        sitepath = self.main(args)
        site = self.make_site(sitepath, args.config)
        server.site = site
        server.serve(args.address, args.port)

    def make_site(self, sitepath, config):
        """
        Creates a site object from the given sitepath and the config file.
        """
        config = Config(sitepath, config_file=config)
        return Site(sitepath, config)
