#!/usr/bin/env python2

# These two lines are needed to run on EL6
__requires__ = ['SQLAlchemy >= 0.8']

from bufftweet import models
from bufftweet.default_config import DB_URL
models.create_tables(
    DB_URL,
    debug=True)
