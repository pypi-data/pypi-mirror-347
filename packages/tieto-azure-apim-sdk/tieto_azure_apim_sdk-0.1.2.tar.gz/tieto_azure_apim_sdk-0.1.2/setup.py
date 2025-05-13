from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tieto_azure_apim_sdk",
    version="0.1.2",  # Remember to increment version!
    packages=find_packages(),
    install_requires=["requests"],
    author="Your Name",
    description="SDK for querying Azure OpenAI through Azure API Management Gateway.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Important: This specifies it's a Markdown file
    url="https://github.com/NaveenGandla/azure-apim-python-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)
