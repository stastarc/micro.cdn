import uvicorn
from env import Env
import routes, middleware
from fastapi import FastAPI

app = FastAPI(redoc_url=None, docs_url='/docs' if Env.DEBUG else None)

middleware.include(app)
routes.include(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host=Env.HOST, port=Env.PORT, log_config="./logging.ini")