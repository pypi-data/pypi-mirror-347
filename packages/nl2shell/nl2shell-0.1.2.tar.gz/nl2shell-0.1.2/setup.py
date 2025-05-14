from setuptools import setup, find_packages

setup(
    name="nl2shell",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "openai",
        "pyyaml",
        "rich",
        "psutil",
    ],
    entry_points={
        'console_scripts': [
            'nl2shell=nl2shell.main:main',
        ],
    },
    author="zhangwei330",
    author_email="zhangwei330@meituan.com",
    description="将自然语言转换为shell命令的工具",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nl2shell",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)