#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'haoyang'
__date__ = '2025/4/27 08:29'

from contextlib import asynccontextmanager
from typing import AsyncIterator
from mcp.server import Server
from mcp.server.fastmcp import FastMCP
from ctools import cjson

@asynccontextmanager
async def server_lifespan(server: Server) -> AsyncIterator[dict]:
    yield {}


# 创建 MCP 服务器实例
mcp = FastMCP("excel-read-server", lifespan=server_lifespan)


@mcp.tool()
def read_excel_paginated(file_path: str, sheet_name: str = 'Sheet1', page: int = 1, page_size: int = 10, header_row: int=0) -> dict:
    """
    分页读取指定的 Excel 文件和工作表，返回当前页的数据内容。

    参数:
        file_path: Excel 文件的路径。
        sheet_name: 工作表名称，默认为第一个工作表。
        page: 页码，从 1 开始。
        page_size: 每页的行数。默认 20
        header_row: 标题行的行号，默认为 0

    返回:
        包含列名、数据、当前页码、每页行数和总行数的字典。
    """
    import pandas as pd
    try:
        # 计算跳过的行数
        skip_rows = (page - 1) * page_size

        # 使用 ExcelFile 提高效率
        excel_file = pd.ExcelFile(file_path)
        total_rows = pd.read_excel(excel_file, sheet_name=sheet_name).shape[0]

        # 读取指定页的数据
        df = pd.read_excel(
            excel_file,
            header=header_row,
            sheet_name=sheet_name,
            skiprows=range(header_row + 1, skip_rows + 2),  # 跳过标题行后再跳过前面的行
            nrows=page_size
        )
        return cjson.dumps({
            "columns": df.columns.tolist(),
            "data": df.to_dict(orient="records"),
            "page": page,
            "page_size": page_size,
            "total_rows": total_rows
        })
    except Exception as e:
        return {"error": str(e)}

def main():
    mcp.run()

if __name__ == '__main__':
    main()
