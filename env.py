import dotenv

ENV = dotenv.dotenv_values('.env')
MIDDLEWARE = dotenv.dotenv_values('.middleware.env')
DB = dotenv.dotenv_values('.database.env')

class MiddlewareEnv:
    MAX_CONTENT_SIZE = int(MIDDLEWARE.get('MAX_CONTENT_SIZE', None) or 3145728)
    INTERNAL_IPS = [i.split('.') for i in (MIDDLEWARE.get('INTERNAL_IPS', None) or '').split(',')]
    INTERNAL_ROUTE_PREFIXES = (MIDDLEWARE.get('INTERNAL_ROUTE_PREFIXES', None) or '').split(',')
    
class DatabaseEnv:
    HOST = DB['HOST']
    PORT = int(DB.get('PORT') or 3306)
    USERNAME = DB['USERNAME']
    PASSWORD = DB['PASSWORD']
    DATABASE = DB['DATABASE']

class Env:
    HOST = ENV.get('HOST', None) or 'localhost'
    PORT = int(ENV.get('PORT', None) or '5002')
    CDN_DIR = ENV.get('CDN_DIR', None) or './cdn'
    DEBUG = (ENV.get('DEBUG', None) or 'false').lower() == 'true'