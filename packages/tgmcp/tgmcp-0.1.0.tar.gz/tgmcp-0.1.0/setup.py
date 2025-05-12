"""
Setup script for the Telegram MCP package.
"""

from setuptools import setup, find_packages

setup(
    name="tgmcp",
    version="0.1.0",
    description="Telegram Model Context Protocol integration",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "telethon",
        "mcp-server",
        "nest-asyncio",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "tgmcp=tgmcp.__main__:main",
        ],
    },
    python_requires=">=3.8",
)
