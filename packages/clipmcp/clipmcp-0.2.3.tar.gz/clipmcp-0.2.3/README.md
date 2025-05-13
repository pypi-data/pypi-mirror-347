# VideoMCP - 文本到图像生成API客户端

VideoMCP是一个基于Stable Diffusion API的文本到图像生成工具，支持命令行和服务器两种使用方式。

## 安装

```bash
pip install -e .
```

## 命令行使用

### 使用uvx.bat（推荐）

```bash
# 使用uvx.bat脚本运行（会自动设置环境变量）
.\uvx.bat clipmcp generate "happy cat" --output ./output_images

# 其他选项
.\uvx.bat clipmcp generate "happy dog" --width 512 --height 512 --count 3 --ultra
```

### 直接使用Python模块

```bash
# 手动设置环境变量
$env:VIDEOMCP_ACCESS_KEY = "your_access_key"
$env:VIDEOMCP_SECRET_KEY = "your_secret_key"

# 使用Python模块
python -m clipmcp.cli generate "cute puppy" --output ./output_images
```

## 可用参数

| 参数 | 简写 | 说明 | 默认值 |
|------|-----|------|-------|
| --negative | -n | 负面提示词 | (默认负面提示词) |
| --width | -w | 图像宽度 | 768 |
| --height | -h | 图像高度 | 1024 |
| --count | -c | 生成图像数量 | 1 |
| --seed | -s | 随机种子，-1为随机 | -1 |
| --ultra | | 是否使用旗舰版API | False |
| --output | -o | 输出目录 | 环境变量设置的目录 |

## MCP服务器使用

1. 复制`mcp.example.json`文件到Cursor的配置目录
2. 在Cursor中使用`/clipmcp-server`命令启动服务器
3. 调用生成图像工具

## 环境变量

- `VIDEOMCP_ACCESS_KEY`: API访问密钥
- `VIDEOMCP_SECRET_KEY`: API密钥
- `VIDEOMCP_API_BASE_URL`: API基础URL，默认为`https://openapi.liblibai.cloud`
- `VIDEOMCP_DOWNLOAD_DIR`: 图像下载目录，默认为`~/Downloads/VideoMCP`

## 许可

MIT

## 功能

- 支持文本到图像的生成 (使用liblibai API)
- MCP协议集成，支持Cursor直接调用

## 安装

1. 克隆本仓库：
   ```bash
   git clone https://github.com/your-username/VideoMCP.git
   cd VideoMCP
   ```

2. 安装依赖：
   ```bash
   pip install -e .
   ```

3. 配置MCP:
   - 复制`mcp.example.json`到`~/.cursor/mcp.json`
   - 或添加`videomcp`部分到现有的`~/.cursor/mcp.json`文件

## 使用方式

### 启动服务

```bash
python -m videomcp.server
```

### 通过Cursor使用

1. 确保Cursor已启动并已加载MCP配置
2. 使用Cursor中的VideoMCP API生成图像：

```python
# 示例代码
await videomcp_generate_image(
    prompt="一只可爱的猫",
    negative_prompt="模糊,变形",
    width=768,
    height=768
)
```

## MCP协议支持情况

支持的方法:
- `test_connection`: 测试API连接
- `ping`: 心跳检测
- `generate_image`: 生成图像

## 服务器日志

- 主日志: `~/videomcp_debug.log`
- 错误日志: `~/videomcp_error.log`
- 标准错误: `~/videomcp_stderr.log`

## 故障排查

如果遇到问题，请查看日志文件并确保:
1. API密钥正确配置
2. Python路径正确设置
3. 下载目录存在且可写

## API凭证

您需要从[liblibai](https://www.liblibai.com)获取API密钥。

## 开发说明

### MCP集成完成情况

MCP协议集成已完成并经过测试，主要改进包括:

1. **协议兼容性**:
   - 完善了Content-Length机制
   - 确保所有响应都符合JSON-RPC 2.0规范
   - 增强了错误处理

2. **稳定性改进**:
   - 标准输出重定向，防止调试信息干扰协议通信
   - 完善的日志记录系统
   - 中文和特殊字符的正确处理

3. **认证机制**:
   - 完善了API认证参数生成
   - 错误处理和重试机制

4. **调试工具**:
   - 提供了专门的调试日志
   - 支持查看JSON序列化过程
   - 协议测试工具

### 已解决问题

- JSON-RPC消息序列化和中文编码问题
- API认证参数生成规范化
- MCP协议消息格式符合标准
