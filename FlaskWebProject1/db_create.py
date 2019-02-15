#!flask/bin/python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI_POSTS
from config import SQLALCHEMY_MIGRATE_REPO
from FlaskWebProject1 import db_posts
import os.path
db_posts.create_all(bind="posts")
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI_POSTS, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI_POSTS, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))