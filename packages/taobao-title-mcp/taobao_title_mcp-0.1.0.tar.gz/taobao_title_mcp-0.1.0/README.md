# 淘宝商品标题生成API测试工具

这个Python脚本用于测试淘宝商品标题生成API。它可以将图片URL转换为base64编码，然后发送到API以生成商品标题。

## 功能特点

- 下载图片并转换为base64编码
- 调用淘宝商品标题生成API
- 显示生成的标题
- 保存完整API响应到JSON文件

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

1. 确保已安装所有依赖
2. 修改脚本中的图片URL（如需要）
3. 运行脚本：

```bash
python taobao_title_test.py
```

## 参数说明

脚本中使用的API参数：

- `api_key`: API密钥
- `model`: 使用的AI模型
- `images`: 商品图片的base64编码数组
- `api_endpoint_url`: AI服务的API端点URL
- `temperature`: 控制生成结果的随机性（0.0-1.0）
- `max_tokens`: 生成响应的最大token数量

## 输出

脚本会在控制台输出生成的标题，并将完整的API响应保存到`api_response.json`文件中。 