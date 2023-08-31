from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in maa/__init__.py
from maa import __version__ as version

setup(
	name="maa",
	version=version,
	description="MAA Medical App",
	author="InshaSiS Technologies",
	author_email="support@inshasis.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
