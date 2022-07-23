import argparse

from sapling.deploy.circuitpython_board import Board

from sapling.constants import PYCUBED_VERSIONS


def deploy_cmdline():
    versions_string = ''
    for i, version in enumerate(PYCUBED_VERSIONS):
        versions_string += version
        if i != len(PYCUBED_VERSIONS) - 1:
            versions_string += ' or '

    parser = argparse.ArgumentParser()
    parser.add_argument('--type', help='ground, dev, or flight',
                        default='dev')
    parser.add_argument('--pycubed_version', help='versions_string',
                        default='v5')
    parser.add_argument('--deploy', help='deploy code to spacecraft',
                        type=bool, default=False)
    parser.add_argument('--arm', help='arm antenna deployment',
                        type=bool, default=False)
    args = parser.parse_args()