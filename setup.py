from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    README = f.read()

setup(
    name="simplebardapi",
    version="1.0.1",
    description="A simpler and faster version of BardAPI.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Ruu3f/simplebardapi",
    author="Ruu3f",
    license="GPLv3",
    keywords=[
        "artificial-intelligence",
        "google-bard-api",
        "google-bard",
        "bard-api",
        "google",
        "bard",
        "ai",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    install_requires=[
        "requests",
    ],
    project_urls={
        "Source": "https://github.com/Ruu3f/simplebardapi",
    },
)
