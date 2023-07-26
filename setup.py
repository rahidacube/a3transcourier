from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in a3_ksrtc/__init__.py
from a3_ksrtc import __version__ as version

setup(
	name="a3_ksrtc",
	version=version,
	description="Courier Service System",
	author="Acube",
	author_email="nja@acube.co",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
