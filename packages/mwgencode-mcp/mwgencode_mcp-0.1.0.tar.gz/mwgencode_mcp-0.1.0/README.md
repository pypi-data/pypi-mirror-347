# MWGenCode-MCP

一个基于 MCP 的 Web 框架代码生成工具。

## 功能特点

- 支持多种 Web 框架的代码生成（Flask、AioHTTP、FastAPI）
- UML 模型到 Swagger 类的转换
- 项目初始化和配置文件生成
- 支持自动升级到 K8s 部署

## 安装

```bash
pip install mwgencode-mcp
```

## 使用方法

1. 初始化项目：
```bash
mwgencode-mcp init-project myproject --type flask
```

2. 生成 Swagger 类：
```bash
mwgencode-mcp export myclass
```

3. 添加操作：
```bash
mwgencode-mcp add mypackage myoperation --method get
```

更多使用说明请参考文档。

## 依赖要求

- Python >= 3.11
- MCP >= 0.1.0
- PyYAML >= 5.1

## mcp server json
```json
{
  "mcpServers": {
    "mwgencode": {
      "command": "python",
      "args": [
        "-m",
        "mwgencode.main"
      ]
    }
  }
}
```
