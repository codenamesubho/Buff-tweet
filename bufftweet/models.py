import sqlalchemy as sa

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session,session
from sqlalchemy.orm import relation


Base = declarative_base()


def create_tables(db_url, alembic_ini=None, acls=None, debug=False):
    """ Create the tables in the database using the information from the
    url obtained.

    :arg db_url, URL used to connect to the database. The URL contains
        information with regards to the database engine, the host to
        connect to, the user and password and the database name.
          ie: <engine>://<user>:<password>@<host>/<dbname>
    :kwarg alembic_ini, path to the alembic ini file. This is necessary
        to be able to use alembic correctly, but not for the unit-tests.
    :kwarg debug, a boolean specifying wether we should have the verbose
        output of sqlalchemy or not.
    :return a session that can be used to query the database.

    """
    engine = create_engine(db_url, echo=debug)
    Base.metadata.create_all(engine)
    # engine.execute(collection_package_create_view(driver=engine.driver))
    
    if db_url.startswith('sqlite:'):
        # Ignore the warning about con_record
        # pylint: disable=W0613
        def _fk_pragma_on_connect(dbapi_con, con_record):  # pragma: no cover
            ''' Tries to enforce referential constraints on sqlite. '''
            dbapi_con.execute('pragma foreign_keys=ON')
        sa.event.listen(engine, 'connect', _fk_pragma_on_connect)
    """
    if alembic_ini is not None:  # pragma: no cover
        # then, load the Alembic configuration and generate the
        # version table, "stamping" it with the most recent rev:

        # Ignore the warning missing alembic
        # pylint: disable=F0401
        from alembic.config import Config
        from alembic import command
        alembic_cfg = Config(alembic_ini)
        command.stamp(alembic_cfg, "head")
    """
    session = sessionmaker(bind=engine)
    #scopedsession = scoped_session(sessionmaker(bind=engine))
    # Insert the default data into the db
    #create_default_status(session, acls=acls)
    return session

def get_session(db_url,debug=False):
    engine = create_engine(db_url, echo=debug)
    sm = sessionmaker(bind=engine)
    return scoped_session(sm)


def create_default_status(session, acls=None):
    """ Insert the defaults status in the status tables.
    """

    for status in ['Open', 'Invalid', 'Insufficient data', 'Fixed']:
        ticket_stat = StatusIssue(status=status)
        session.add(ticket_stat)
        try:
            session.commit()
        except SQLAlchemyError:  # pragma: no cover
            session.rollback()
            ERROR_LOG.debug('Status %s could not be added', ticket_stat)

    for status in ['Open', 'Closed', 'Merged']:
        pr_stat = StatusPullRequest(status=status)
        session.add(pr_stat)
        try:
            session.commit()
        except SQLAlchemyError:  # pragma: no cover
            session.rollback()
            ERROR_LOG.debug('Status %s could not be added', pr_stat)

    for grptype in ['user', 'admin']:
        grp_type = PagureGroupType(group_type=grptype)
        session.add(grp_type)
        try:
            session.commit()
        except SQLAlchemyError:  # pragma: no cover
            session.rollback()
            ERROR_LOG.debug('Type %s could not be added', grptype)

    for acl in acls or {}:
        item = ACL(
            name=acl,
            description=acls[acl]
        )
        session.add(item)
        try:
            session.commit()
        except SQLAlchemyError:  # pragma: no cover
            session.rollback()
            ERROR_LOG.debug('ACL %s could not be added', acl)


class TweetStore(Base):
    """ Stores the tweets to be posted.

    Table -- tweetstore
    """
    __tablename__ = 'tweetstore'

    id = sa.Column(sa.Integer, primary_key=True)
    tweet = sa.Column(
        sa.Text, 
        nullable=False)
    created = sa.Column(
        sa.DateTime,
        nullable=False,
        default=sa.func.now())


class User(Base):
    """ Stores information about users.

    Table -- users
    """

    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True)
    user = sa.Column(
        sa.String(32), 
        nullable=False, 
        unique=True, 
        index=True)
    auth_key = sa.Column(sa.String(50), nullable=True)
    auth_secret = sa.Column(sa.String(50), nullable=True)
    created = sa.Column(
        sa.DateTime,
        nullable=False,
        default=sa.func.now())
    tweet_count = sa.Column(sa.Integer)

    