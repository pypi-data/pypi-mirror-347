pip install build twine

# 2. 构建分发包
python -m build

# 3. 上传到 PyPI（如果是第一次，需要先在 PyPI 注册账号）
twine upload dist/*

使用方法
首次使用前，创建配置文件 ~/.nl2shell.yaml
api_key: "your-api-key"
base_url: "your-api-base-url"
model: "gpt-4-turbo"

使用命令：
nl2shell "你的自然语言描述"