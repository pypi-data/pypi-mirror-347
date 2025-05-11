import setuptools  # isort:skip
from pathlib import Path
import re

# Get the base directory
base_dir = Path(__file__).resolve().parent

# Read the long description
try:
    long_description = (base_dir / "README.md").read_text()
except FileNotFoundError:
    long_description = "Utils for StarBot."

# Read the version from __version__.py
try:
    content = (base_dir / "Scarlet_Utils" / "__version__.py").read_text()
    __version__ = re.compile(r"__version__\s*=\s*['\"](?P<version>\d+\.\d+\.\d+)['\"]").search(content).groupdict()["version"]
except FileNotFoundError:
    __version__ = "0.0.1"  # Default version if __version__.py is missing

# Package setup
setuptools.setup(
    name="Scarlet_Utils",
    version=__version__,
    author="Scarlet Jean",
    author_email="r79767525@gmail.com",
    description="Utils for StarBot.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/deathamongstlife/Star-Discord-Utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9.1",
    install_requires=[
        "sentry_sdk",
        "colorama",
    ],
    extras_require={
        "dev": ["pytest", "black"],
        "docs": ["sphinx"],
    },
)