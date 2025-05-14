# MCP行情服务器 (PyPI & uvx/JSON 安装) - 安装与使用指南

## 1. 概述

本项目提供了一个基于Flask的A股行情数据服务器，旨在通过MCP (模型上下文协议) 提供服务。您可以将此服务器通过PyPI发布，并使用`uvx`命令或JSON配置在MCP客户端（如Cursor, Cherry Studio）中自动安装和运行。

主要功能包括：

*   获取A股指定标的（指数、个股、ETF等）的历史行情数据（日/周/月频）。
*   获取上海证券交易所最新的股票数据总貌。
*   提供深圳证券交易所行业成交数据的接口（目前为占位符，具体功能待进一步实现）。

## 2. 先决条件

*   **Python 3.11 或更高版本**
*   **uv**: 一个快速的Python包安装器和解析器。如果尚未安装，请参照其官方文档安装 (通常 `pip install uv`)。

## 3. 安装与运行 (通过 uvx)

一旦该包发布到PyPI (包名为 `hstock-mcp`)，您可以使用 `uvx` 直接运行它。`uvx` 会自动处理包的下载、安装到临时环境和执行。

```bash
# 假设包已发布到PyPI
uvx hstock-mcp --host <your_desired_host> --port <your_desired_port>
```

例如，要在本地 `127.0.0.1` 的 `8888` 端口启动服务器：

```bash
uvx hstock-mcp --host 127.0.0.1 --port 8888
```

服务器启动后，您会看到类似以下的输出：

```
Starting MCP Server on http://127.0.0.1:8888
 * Serving Flask app 'mcp_server_lib.app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8888
Press CTRL+C to quit
```

**命令行参数说明 (由 `hstock-mcp` 提供):**

*   `--host <ip_address>`: 服务器监听的主机地址 (默认为 `127.0.0.1`)。使用 `0.0.0.0` 可以让服务器从网络中的其他计算机访问。
*   `--port <port_number>`: 服务器监听的端口号 (默认为 `5000`)。
*   `--debug`: 启用Flask的调试模式 (默认为关闭)。

## 4. MCP客户端JSON配置示例

对于支持JSON配置的MCP客户端，您可以使用类似以下的配置来集成此服务器：

```json
{
  "mcpServers": {
    "my_ashare_market_data": {  // 您可以自定义此键名
      "command": "uvx",
      "args": [
        "hstock-mcp", // PyPI上的包名
        "--host", "0.0.0.0",   // 示例：监听所有接口
        "--port", "8889"      // 示例：使用8889端口
        // 您可以根据需要添加其他命令行参数，如 --debug
      ],
      "env": {},
      "disabled": false
    }
  }
}
```

**说明:**
*   `"command": "uvx"`: 指定使用 `uvx` 来执行。
*   `"args": ["hstock-mcp", ...]` : 第一个参数是PyPI上的包名，后续参数是传递给服务器启动脚本的命令行参数。

## 5. API接口简述

服务器启动后，可以通过HTTP GET请求访问以下端点：

*   `/mcp/marketdata/history`：获取A股历史行情数据。
    *   参数: `symbol`, `frequency`, `start_date` (可选), `end_date` (可选)
    *   示例: `curl "http://127.0.0.1:8889/mcp/marketdata/history?symbol=000001.SZ&frequency=daily&start_date=2024-04-01&end_date=2024-04-30"` (假设服务器运行在8889端口)

*   `/mcp/marketdata/sse/overview`：获取上海证券交易所股票数据总貌。
    *   示例: `curl "http://127.0.0.1:8889/mcp/marketdata/sse/overview"`
    *   注意：此接口的部分数据字段可能因上游数据源问题返回空值。

*   `/mcp/marketdata/szse/industry_transactions`：获取深圳证券交易所行业成交数据 (当前为占位符，返回501错误)。
    *   参数: `symbol`, `date`
    *   示例: `curl "http://127.0.0.1:8889/mcp/marketdata/szse/industry_transactions?symbol=000001&date=20231231"`

详细的API设计文档 (`api_design_*.md`) 之前已提供，可供参考。

## 6. 项目文件结构 (用于PyPI发布)

```
hstock-mcp/
├── mcp_server_lib/           # 主要的Python包代码
│   ├── __init__.py
│   ├── app.py                # Flask应用定义和API路由
│   ├── akshare_provider.py   # AKShare数据源接口实现
│   ├── yahoo_finance_provider.py # Yahoo Finance数据源接口实现
│   └── cli.py                # 命令行入口脚本
├── pyproject.toml            # uv 和 setuptools 构建配置文件
├── requirements.txt          # 依赖列表 (主要供参考，uv使用pyproject.toml)
└── README.md                 # (本文件) 安装与使用指南
```

## 7. 故障排除与已知问题

*   **`uvx` 执行问题**: 确保 `uv` 已正确安装并配置在系统PATH中。网络连接必须可用以下载PyPI包。
*   **上交所数据总貌字段为空**: 部分数据字段可能返回`null`，这可能源于AKShare上游数据的问题。
*   **深交所行业成交数据未实现**: 此功能当前返回501错误，待后续找到合适的数据源后实现。

如果您在安装或使用过程中遇到任何问题，请检查Python环境、uv安装以及依赖项是否正确安装。

