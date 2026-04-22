import pathlib
from setuptools import find_packages, setup

# Get path to parent folder
here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

github = 'https://github.com/jaaruizgu/netbox-portscanner'

setup(
    name="netbox-portscanner",
    version="0.0.5",
    author="Javier Alejandro Ruiz",
    author_email="javier.ruiz@edgeuno.com",
    description="Scan NetBox virtual machines and sync detected services",
    url=github,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "Operating System :: Unix",
        "License :: OSI Approved :: Apache Software License",
    ],
    keywords="netbox netbox-plugin plugin scanner portscanner edgeuno",
    project_urls={
        'Source': github,
    },
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ['*', '*/*', '*/*/*'],
    },
    install_requires=[],
    extras_require={"dev": ["pytest>=7", "black", "pylint", "twine", "wheel"]},
    python_requires='>=3.8',
)
