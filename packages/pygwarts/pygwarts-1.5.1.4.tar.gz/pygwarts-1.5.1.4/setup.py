from setuptools import setup
from setuptools import find_packages








with open("README.md") as md : long_desc = md.read()
setup(

	name="pygwarts",
	version="1.5.1.4",
	author="lngd",
	author_email="lngdeer@gmail.com",
	url="https://github.com/longdeer/pygwarts",
	license="GPL-3.0 license",
	description="Python multitool library",
	long_description=long_desc,
	long_description_content_tpye="text/markdown",
	packages=find_packages(),
	python_requires=">=3.10"
)