from setuptools import setup, find_packages
 
setup(
    name="mcp-nutrimaster",  # 包名，pip install 时用这个
    version="0.1.0",
    description="智膳源道 MCP Server，是国内首家支持MCP 协议的营养膳食平台。",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="qq201128",
    author_email="3229191254@qq.com",
    url="https://github.com/qq201128/mcp-nutrimaster",  # 可选：放 GitHub 仓库地址
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)