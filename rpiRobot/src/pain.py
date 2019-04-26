import logging
import optparse
import sys

from context.championship import Championship
from context.commandReceiver import CommandReceiver

logging.captureWarnings(True)

CHAMPIONSHIP_MODE = "championship"
REMOTE_MODE = "remote"
DISPLAY_COMMAND_REMOTE = "display-command-remote"


class Pain:
    @staticmethod
    def championship(**kwargs) -> None:
        Championship(**kwargs).application().run()

    @staticmethod
    def display_command_remote(**kwargs) -> None:
        CommandReceiver(**kwargs).application().run()


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-m", "--mode", action="store", dest="mode", type=str, default=CHAMPIONSHIP_MODE)
    parser.add_option("-p", "--port", action="store", dest="port", type=int, default=7347)
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False)
    opts = parser.parse_args(sys.argv[1:])[0]
    port = opts.port
    mode = opts.mode.lower()
    if opts.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if CHAMPIONSHIP_MODE.startswith(mode):
        Pain.championship(port=port)
    elif DISPLAY_COMMAND_REMOTE.startswith(mode):
        Pain.display_command_remote(port=port)
