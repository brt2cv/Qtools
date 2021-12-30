#!/usr/bin/env python3
# @Date    : 2021-12-30
# @Author  : Bright (brt2@qq.com)
# @Link    : https://gitee.com/brt2
# @Version : v0.1.1

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.ocr.api import router as ocr
from app.facerec.api import app as facerec

app = FastAPI(version="1.0.2")
app.include_router(ocr)
app.include_router(facerec)

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

try:
    import consul

    _c = consul.Consul(host="127.0.0.1", port=8500)
    service = _c.agent.service
    serv_id = "QTools_by_FastAPI"
    service.register(
        name="QTools"
        , address="127.0.0.1"
        , port=8510
        , service_id=serv_id
    )

    @app.on_event("shutdown")
    async def shutdown_event():
        service.deregister(serv_id)
        print(">>> 退出FastAPI，已从Consul解注册！")

except Exception:
    service = None


if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=1314)
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=1314,
        reload=True,
    )
