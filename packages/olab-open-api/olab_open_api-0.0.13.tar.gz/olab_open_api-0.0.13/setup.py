from setuptools import setup, find_packages  # noqa: H301

NAME = "olab_open_api"
VERSION = "0.0.13"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="OLAB Prediction Market Open API",
    author="nik.opinionlabs",
    author_email="nik@opinionlabs.xyz",
    url="",
    keywords=["PredictionMarket"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
)
