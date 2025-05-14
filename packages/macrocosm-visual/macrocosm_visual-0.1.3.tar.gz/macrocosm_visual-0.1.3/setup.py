from os.path import abspath, dirname, join

from setuptools import find_packages, setup

this_dir = abspath(dirname(__file__))

with open(join(this_dir, "README.md"), encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="macrocosm-visual",
    version="0.1.3",
    description="Macrocosm Visual Engine",
    url="https://github.com/macro-cosm/macrocosm-visual",
    long_description_content_type="text/markdown",
    long_description=long_description,
    author="Macrocosm",
    author_email="luca.mungo@macrocosm.group",
    license="MIT",
    install_requires=[
        "pyyaml",
        "matplotlib",
        "plotly0",
    ],
    packages=find_packages(exclude=["docs"]),
    include_package_data=True,
)
