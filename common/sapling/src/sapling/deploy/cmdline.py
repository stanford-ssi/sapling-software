import asyncio
import argparse
import logging
import pathlib
import json
import sys

import adafruit_board_toolkit.circuitpython_serial

from sapling.constants import PYCUBED_VERSIONS
from test_circuitpy.board import Board

LOGGER = logging.getLogger(__name__)

async def deploy_cmdline(type='dev', board_version='v5', board_dir=pathlib.Path('.'), drive='PYCUBED', arm=False, verbose=False):
    if sys.platform == 'darwin':
        mount_point = pathlib.Path("/Volumes")
    else:
        pytest.xfail("Tests do not yet work on platforms other than MacOS")
    
    LOGGER.info(f"Expecting to connect to a {board_version} board")
    repl_ports = adafruit_board_toolkit.circuitpython_serial.repl_comports()
    
    board_def_dir = board_dir / 'versions' / board_version

    with open(board_def_dir / "board.json") as f:
        board_config = json.load(f)
        LOGGER.info(board_config)
    if repl_ports:
        if len(repl_ports) > 1:
            LOGGER.info(f"More than one target discovered -- repl: \
                {[port.device for port in repl_ports]}")
        try:
            LOGGER.info(f"Connecting to board with repl at {repl_ports[0].device}")
            connected_board = await Board(
                mount_point, 
                repl_ports[0].device, 
                board_def_dir / "src",
                **board_config
            )
            if not connected_board:
                LOGGER.warning("Unable to connect to board, timing out for 3s")
                await asyncio.sleep(3)
                connected_board = await Board(
                    mount_point, 
                    repl_ports[0].device, 
                    board_def_dir / "src",
                    **board_config
                )
            return connected_board
        except Exception as e:
            LOGGER.error(e)
    else:
        LOGGER.error(f"No boards discovered: {repl_ports}")


async def main():
    versions_string = ''
    for i, version in enumerate(PYCUBED_VERSIONS):
        versions_string += version
        if i != len(PYCUBED_VERSIONS) - 1:
            versions_string += ' or '

    parser = argparse.ArgumentParser()
    parser.add_argument('type', help='ground, dev, or flight',
                        default='dev')
    parser.add_argument('name', help='PYCUBED by default. This is the name of the CIRCUITPY drive',
                        default='PYCUBED')
    parser.add_argument('board_version', help=f'{versions_string}',
                        default='v5')
    parser.add_argument('-a', '--arm', action='store_true', 
                        help='arm antenna deployment')
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="increase output verbosity")
    args = parser.parse_args()
    
    await asyncio.wait([
        asyncio.create_task(
            deploy_cmdline(
                type=args.type,
                name=args.name,
                board_version=args.board_version,
                arm=args.arm,
                verbose=args.verbose,
            )
        )
    ])
    

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
