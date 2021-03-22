import os

SECRET_KEY = b"x\x0ck\x88D\x96\xbe\xa4\xcc\x0er\xde\xc8, \xec\x06\x8b\xcab#s\x81'"
PWD = os.path.abspath(os.curdir)

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/usuarios.db'.format(PWD)
SQLALCHEMY_TRACK_MODIFICATIONS = False