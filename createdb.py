#!/usr/bin/env python2

# These two lines are needed to run on EL6
__requires__ = ['SQLAlchemy >= 0.8', 'jinja2 >= 2.4']

import models
from default_config import DB_URL
models.create_tables(
    DB_URL,
    debug=True)
