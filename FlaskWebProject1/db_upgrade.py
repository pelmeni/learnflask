#!flask/bin/python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI_POSTS
from config import SQLALCHEMY_MIGRATE_REPO
v = api.db_version(SQLALCHEMY_DATABASE_URI_POSTS, SQLALCHEMY_MIGRATE_REPO)
api.downgrade(SQLALCHEMY_DATABASE_URI_POSTS, SQLALCHEMY_MIGRATE_REPO, v - 1)
print 'Current database version: ' + str(api.db_version(SQLALCHEMY_DATABASE_URI_POSTS, SQLALCHEMY_MIGRATE_REPO))