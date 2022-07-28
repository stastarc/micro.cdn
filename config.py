from env import Env


bind = f'{Env.HOST}:{Env.PORT}'
loglevel = 'debug'
worker_class = 'uvicorn.workers.UvicornWorker'
workers = 5