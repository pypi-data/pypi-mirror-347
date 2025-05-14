pip install build twine

# 2. 构建分发包
python -m build

# 3. 上传到 PyPI（如果是第一次，需要先在 PyPI 注册账号）
twine upload dist/*