from setuptools import setup, find_packages

setup(
    name="cordhook",
    version="0.1.0",
    author="Mocha",
    author_email="ohplot@gmail.com",
    description="A simple Discord webhook wrapper for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",  # replace with your repo
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.25.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Chat",
    ],
    python_requires='>=3.7',
)