import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgreslq_psycopg2',
        'NAME': 'db',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': 5432
    }
}

MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aivepet$systemtracker',
        'USER': 'aivepet',
        'PASSWORD': '987654321Ab$',
        'HOST': 'aivepet.mysql.pythonanywhere-services.com',
        'PORT': '',
        # 'OPTIONS': {
        #     'init_command': 'SET default_storage_engine=INNODB',
        # }
    }
}