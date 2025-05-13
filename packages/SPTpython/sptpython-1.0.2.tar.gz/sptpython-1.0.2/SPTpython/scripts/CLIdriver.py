import logging
import logging.config
import datetime
import os
import sys
import SPTpython.CLI as CLI

def main():
    time = datetime.datetime.now().strftime("%b_%d_%Y_%H_%M_%S")
    if not os.path.exists('logs/processing'):
        os.makedirs('logs/processing')
    logging.config.fileConfig("SPTpython/logging.conf", defaults={'logfilename': f'logs/processing/{time}.log'})

    mode="CLI"
    
    if mode == "CLI":
        CLI.start()

if __name__ == '__main__':
    main()