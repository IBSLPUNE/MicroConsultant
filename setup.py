from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in microconsultant/__init__.py
from microconsultant import __version__ as version

setup(
	name="microconsultant",
	version=version,
	description="Development For Microconsultant By IBSL",
	author="IBSL",
	author_email="shantanu@frappe.io",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
