import logging
import optparse
import sys

from context.remote import Remote
from context.remoteUi import RemoteUi

MODE_CHAMPIONSHIP = "championship"
MODE_REMOTE = "remote"
MODE_REMOTE_UI = "ui-remote"


class BaseStation:
    @staticmethod
    def championship() -> None:
        pass

    @staticmethod
    def remote(**kwargs) -> None:
        Remote(**kwargs).application().run()

    @staticmethod
    def remote_ui() -> None:
        RemoteUi().application().run()


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-m", "--mode", action="store", dest="mode", type=str, default=MODE_CHAMPIONSHIP,
                      help="(championship|remote|ui-remote)")
    parser.add_option("-p", "--port", action="store", dest="port", type=int, default=7347)
    parser.add_option("-a", "--address", action="store", dest="address", type=str, default='<broadcast>')
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False)
    opts = parser.parse_args(sys.argv[1:])[0]
    mode: str = opts.mode.lower()
    if opts.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if MODE_CHAMPIONSHIP.startswith(mode):
        BaseStation.championship()
        pass
    elif MODE_REMOTE.startswith(mode):
        BaseStation.remote(port=opts.port, address=opts.address, timeout=3)
        pass
    elif MODE_REMOTE_UI.startswith(mode):
        BaseStation.remote_ui()
        pass
