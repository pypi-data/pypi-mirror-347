#!/usr/bin/env -S uv run --script
# -*- coding: utf-8 -*-
# /// script
# requires-python = "==3.11.*"
# dependencies = [
#    "fastapi",
#    "pygarden[postgres]==0.3.18",
# ]
# [[tool.uv.index]]
# url = "https://__token__:A_A4GWyaniYBX14xMowA@code.ornl.gov/api/v4/projects/18252/packages/pypi/simple"
# ///
import pygarden
import fastapi
from pygarden.logz import create_logger
from pygarden.mixins.postgres import PostgresMixin
logger = create_logger()
logger.info('Successfully imported pygarden with the PostgresMixin.')