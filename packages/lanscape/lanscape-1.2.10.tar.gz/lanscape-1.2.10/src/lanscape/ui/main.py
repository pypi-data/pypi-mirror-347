
import threading
import webbrowser
import time
import logging
import traceback
import os
from ..libraries.logger import configure_logging
from ..libraries.runtime_args import parse_args, RuntimeArgs
# do this so any logs generated on import are displayed
args = parse_args()
configure_logging(args.loglevel, args.logfile)

from ..libraries.version_manager import get_installed_version, is_update_available
from .app import start_webserver
import socket


log = logging.getLogger('core')
# determine if the execution is an instance of a flask reload
# happens on file change with reloader enabled
IS_FLASK_RELOAD = os.environ.get("WERKZEUG_RUN_MAIN")




def main():
    if not IS_FLASK_RELOAD:
        log.info(f'LANscape v{get_installed_version()}')
        try_check_update()
        
    else:
        log.info('Flask reloaded app.')
        
    args.port = get_valid_port(args.port)
        
        
    try:
        
        no_gui(args)

        log.info('Exiting...')
    except Exception:
        # showing error in debug only because this is handled gracefully
        log.debug('Failed to start. Traceback below')
        log.debug(traceback.format_exc())



def try_check_update():
    try: 
        if is_update_available():
            log.info('An update is available!')
            log.info('Run "pip install --upgrade lanscape --no-cache" to supress this message.')
    except:
        log.debug(traceback.format_exc())
        log.warning('Unable to check for updates.')
    

def open_browser(url: str,wait=2):
    """
    Open a browser window to the specified
    url after waiting for the server to start
    """
    def do_open():
        try:
            time.sleep(wait)
            webbrowser.open(url, new=2)
        except:
            log.debug(traceback.format_exc())
            log.info(f'Unable to open web browser, server running on {url}')

    threading.Thread(target=do_open).start()

def no_gui(args: RuntimeArgs):
    # determine if it was reloaded by flask debug reloader
    # if it was, dont open the browser again
    if not IS_FLASK_RELOAD:
        open_browser(f'http://127.0.0.1:{args.port}')
        log.info(f'Flask started: http://127.0.0.1:{args.port}')
    
    start_webserver(
        args
    )

def get_valid_port(port: int):
    """
    Get the first available port starting from the specified port
    """
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
            port += 1

if __name__ == "__main__":
    main()
        
