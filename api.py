#!/usr/bin/env python3
# @Date    : 2021-12-22
# @Author  : Bright (brt2@qq.com)
# @Link    : https://gitee.com/brt2
# @Version : v0.1.0

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.ocr.api import router as ocr

app = FastAPI(version="1.0.2")
app.include_router(ocr)

@app.get("/index")
def welcome():
    return "欢迎来到QTools-API"

@app.get("/test")
def test():
    """ 提供API测试环境 """
    return RedirectResponse("/docs")

@app.get("/")
def root():
    """ 暂时使用/test调用功能 """
    return RedirectResponse("/test")

if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=1313)
    uvicorn.run("api:app", host="0.0.0.0", port=1313, debug=True, reload=True)
