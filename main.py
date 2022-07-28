import uvicorn
from env import Env
import routes, database, middleware
from fastapi import FastAPI

app = FastAPI(redoc_url=None, docs_url='/docs' if Env.DEBUG else None)

middleware.include(app)
routes.include(app)

@app.on_event("startup")
async def startup():
    database.init()

@app.on_event("shutdown")
async def shutdown():
    database.destroy()

if __name__ == "__main__":
    uvicorn.run("main:app", host=Env.HOST, port=Env.PORT, log_config="./logging.ini")