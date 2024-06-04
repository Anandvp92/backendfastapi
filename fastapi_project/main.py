from fastapi import FastAPI
import uvicorn
from  views import *

app = FastAPI()

if __name__=="__main__":
    uvicorn.run("main:app",reload=True,port=9000)


