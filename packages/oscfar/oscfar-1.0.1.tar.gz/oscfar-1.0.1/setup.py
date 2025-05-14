__version__ = "1.0.1"

from setuptools import setup

description = open("readme.md").read()

setup(
    name="oscfar",
    version=__version__,
    description="Order Statistic Constant False Alarm Rate detector package",
    long_description=description,
    long_description_content_type="text/markdown",
    author="Chloé Legué",
    author_email="chloe.legue@mail.mcgill.ca",
    packages=["oscfar"],
    package_data={"": ["readme.md"]},
    package_dir={
        "oscfar": ".",
    },
    install_requires=["numpy", "scipy", "matplotlib", "pandas", "itertools"],
    python_requires=">=3.9",
    include_package_data=True,
)
