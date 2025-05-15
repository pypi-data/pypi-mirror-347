import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gawx-python-sdk",
    version="0.0.1",    
    author="Gawx",
    author_email="support@gawx.ai",
    description="Gawx Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gawx-ai/gawx-python-sdk",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
        "pandas",
        "python-dotenv"
    ],
)