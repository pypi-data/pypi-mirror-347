from setuptools import setup, find_packages

setup(
    name="memory_plus",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastmcp>=2.0.0",
        "qdrant-client",
        "langchain",
        "google-generativeai",
        "plotly",
        "pandas",
        "numpy",
        "scikit-learn",
        "umap-learn",
        "aiofiles",
        "boto3",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "memory_plus = memory:main_cli",
        ],
    },
) 