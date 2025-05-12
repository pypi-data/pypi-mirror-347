from setuptools import setup, find_packages

setup(
    name="safentic",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    license="Proprietary :: Safentic Commercial License",  # Custom classifier
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",  # Indicates not open source
        "Operating System :: OS Independent",
    ],
    author="Safentic",
    author_email="contact@safentic.com",
    description="Safentic SDK for behavior analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://safentic.com",
)
