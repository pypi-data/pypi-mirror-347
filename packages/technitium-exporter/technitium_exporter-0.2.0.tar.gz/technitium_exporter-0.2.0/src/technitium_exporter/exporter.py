#!/usr/bin/env python3

import time
import logging

from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY

from technitium_exporter.collector import TechnitiumCollector
from technitium_exporter.args import parse_args

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    args = parse_args()
    REGISTRY.register(TechnitiumCollector(args))
    logger.info(f"Starting HTTP server on {args.address}:{args.port}")
    start_http_server(args.port, args.address)
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
