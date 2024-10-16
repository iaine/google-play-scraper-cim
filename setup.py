import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="google-play-scraper-cim",
    version="0.0.1",
    author="Centre for Interdisciplinary Methodologies",
    author_email="iain.emsley@warwick.ac.uk",
    description="A lightweight Google Play Store scraper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iaine/google-play-scraper-cim",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = ['requests', 'beautifulsoup4>=4.9.3', 'pandas', 'google-play-scraper'],
)