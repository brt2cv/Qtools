#!/usr/bin/env python3
# @Date    : 2021-12-30
# @Author  : Bright (brt2@qq.com)
# @Link    : https://gitee.com/brt2
# @Version : v0.1.1

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from app.ocr.api import router as ocr
from app.facerec.api import app as facerec

app = FastAPI(version="1.0.2")
app.include_router(ocr)
app.include_router(facerec)

app.add_middleware(
    CORSMiddleware,
    # 允许跨域的源列表，例如 ["http://www.example.org"] 等等，["*"] 表示允许任何源
    allow_origins=["*"],
    # 跨域请求是否支持 cookie，默认是 False，如果为 True，allow_origins 必须为具体的源，不可以是 ["*"]
    allow_credentials=False,
    # 允许跨域请求的 HTTP 方法列表，默认是 ["GET"]
    allow_methods=["*"],
    # 允许跨域请求的 HTTP 请求头列表，默认是 []，可以使用 ["*"] 表示允许所有的请求头
    # 当然 Accept、Accept-Language、Content-Language 以及 Content-Type 总之被允许的
    allow_headers=["*"],
    # 可以被浏览器访问的响应头, 默认是 []，一般很少指定
    expose_headers=["*"]
    # 设定浏览器缓存 CORS 响应的最长时间，单位是秒。默认为 600，一般也很少指定
    # max_age=1000
)

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
