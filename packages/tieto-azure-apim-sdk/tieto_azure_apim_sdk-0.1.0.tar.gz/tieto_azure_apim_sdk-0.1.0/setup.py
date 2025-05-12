from setuptools import setup, find_packages

setup(
    name="tieto_azure_apim_sdk",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    author="Naveen Kumar",
    description="SDK for querying Azure OpenAI through Azure API Management Gateway.",
    url="https://github.com/NaveenGandla/azure_apim_openai_sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.11",
)