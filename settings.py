import os

from django.conf import settings


def configure_settings():
    """
    Configures settings for manage.py and for run_tests.py.
    """
    if not settings.configured:
        # Determine the database settings depending on if a test_db var is set in CI mode or not
        test_db = os.environ.get('DB', None)
        if test_db is None:
            db_config = {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'ambition_dev',
                'USER': 'ambition_dev',
                'PASSWORD': 'ambition_dev',
                'HOST': 'localhost'
            }
        elif test_db == 'postgres':
            db_config = {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'USER': 'postgres',
                'NAME': 'db_mutex',
            }
        elif test_db == 'sqlite':
            db_config = {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db_mutex',
            }
        else:
            raise RuntimeError('Unsupported test DB {0}'.format(test_db))

        settings.configure(
            DATABASES={
                'default': db_config,
            },
            INSTALLED_APPS=(
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.admin',
                'south',
                'db_mutex',
                'db_mutex.tests',
                'django_nose',
            ),
            DEBUG=False,
            TEST_RUNNER = 'django_nose.NoseTestSuiteRunner',
            CACHES = {
                'default': {
                    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                    'LOCATION': 'unique-snowflake'
                }
            }
        )
