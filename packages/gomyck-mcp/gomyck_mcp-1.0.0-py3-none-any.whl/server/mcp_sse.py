#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'haoyang'
__date__ = '2025/4/27 10:04'

import uvicorn
from starlette.applications import Starlette
from starlette.routing import Mount, Host

from excel_read import mcp

if __name__ == "__main__":
    app = Starlette(
        routes=[
            Mount('/', app=mcp.sse_app()),
        ]
    )
    # or dynamically mount as host
    # app.router.routes.append(Host('mcp.acme.corp', app=mcp.sse_app()))
    uvicorn.run(app, host='0.0.0.0', port=8080)
