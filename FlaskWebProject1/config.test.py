CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')

params = urllib.quote_plus("DRIVER={SQL Server Native Client 11.0};SERVER=DACZC5064KGM;DATABASE=AspNet.Identity.Test;UID=dev;PWD=dev")
SQLALCHEMY_MSSQL_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=%s" % params