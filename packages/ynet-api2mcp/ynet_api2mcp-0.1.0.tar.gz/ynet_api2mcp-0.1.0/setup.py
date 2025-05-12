from setuptools import setup, find_packages

setup(
    name="ynet_api2mcp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mcp[cli]>=1.2.0",
        "python-dotenv>=1.0.1",
        "requests>=2.25.0",
        "fastapi>=0.100.0",
        "pydantic>=2.0",
        "prance>=23.6.21.0",
        "openapi-spec-validator>=0.7.1",
        "jmespath>=1.0.1",
    ],
    extras_require={
        "dev": [
            "pytest>=8.3.4",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ynet_api2mcp=mcp_openapi_proxy:main",
        ],
    },
    author="Ynet",
    author_email="your.email@example.com",
    description="MCP server for exposing OpenAPI specifications as MCP tools with customizable tool name prefixes",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ynet_api2mcp",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
