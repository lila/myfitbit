from setuptools import setup, find_packages
from io import open
from os import path
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# automatically captured required modules for install_requires in requirements.txt
with open(path.join(HERE, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")

install_requires = [
    x.strip()
    for x in all_reqs
    if ("git+" not in x) and (not x.startswith("#")) and (not x.startswith("-"))
]
dependency_links = [x.strip().replace("git+", "") for x in all_reqs if "git+" not in x]
setup(
    name="myfitbit",
    description="returns my steps",
    version="1.0.0",
    packages=find_packages(),
    install_requires=install_requires,
    python_requires=">=3.6, <4",  # any python greater than 2.7
    entry_points="""
        [console_scripts]
        myfitbit=myfitbit.__main__:do_main
    """,
    author="karan bhatia",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    url="",
    download_url="",
    dependency_links=dependency_links,
    author_email="karan.bhatia@gmail.com",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        # Pick your license as you wish
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
