from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="hoomanmltk",
    version="0.1.0",  
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    author="HOOM4N",
    author_email="homan.amini@gmail.com",
    description="A collection of modular and reusable machine learning utilities, tools, and helpers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hoom4n/HoomanMLTK",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence"
    ],
    python_requires=">=3.8",
)
