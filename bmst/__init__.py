import logging

import click_log

__all__ = ["log"]

log = logging.getLogger(__name__)
click_log.basic_config(log)
