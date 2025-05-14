from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="anchoring",
    version="0.1.0",
    author="Yuan Tian",
    author_email="bestaskwisher@gmail.com",
    description="Selective Prompt Anchoring (SPA) for LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/magic-YuanTian/Selective-Prompt-Anchoring",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "torch>=1.10.0",
        "transformers>=4.30.0",
    ],
) 