from setuptools import setup
import os

# Read README.md if it exists
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="glyph-sdk",
    version="0.1.0",
    description="Python SDK for Glyph Tokens on Radiant Blockchain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AS",
    author_email="passionkaizen96111@email.com",
    url="https://github.com/zerox-toml/glyph-sdk",
    packages=["glyph_sdk"],
    python_requires=">=3.8",
    install_requires=[
        "requests",
        "base58",
        "ecdsa",
        "typing-extensions"
    ],
    license="MIT",
)
