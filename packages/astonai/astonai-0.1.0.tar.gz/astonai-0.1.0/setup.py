from setuptools import setup, find_packages

setup(
    name="astonai",
    version="0.1.0",
    description="AstonAI - Test Intelligence for AI Codegen",
    author="AstonAI Team",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "pyyaml>=6.0",
        "rich>=10.0.0",
        "neo4j>=5.0.0",
        "gitpython>=3.1.0",
    ],
    entry_points={
        "console_scripts": [
            "aston=testindex.cli.main:main",
        ],
    },
    python_requires=">=3.8",
) 