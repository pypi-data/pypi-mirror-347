from setuptools import setup, find_packages

setup(
    name="mse_inf",
    version="0.1.0",
    author="mse-24-inf team",
    author_email="justbringit16@yandex.ru",
    packages=find_packages(),
    description="tmp description",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)