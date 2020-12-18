from setuptools import setup

import pyvcs

AUTHOR = "Timofeev Nikolas"
AUTHOR_EMAIL = "timofeevnik41@gmail.com"
HOME_PAGE = "https://github.com/timofeev41/cs102"

setup(
    name="pyvcs",
    version=pyvcs.__version__,
    description="The stupid content tracker",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    packages=["pyvcs"],
    entry_points={"console_scripts": ["pyvcs = pyvcs.__main__:main"]},
    url=HOME_PAGE,
    license="GPLv3",
    python_requires=">=3.6.0",
)
