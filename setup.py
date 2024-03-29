#!/usr/bin/env python3

from distutils.core import setup

setup(
    name="dnstls",
    version="0.0.1",
    description="N26's DNS/TLS Proxy",
    author="Alvaro Mourino",
    author_email="alvaro@mourino.net",
    packages = ["dnstls"],
    package_dir = {"dnstls": "src"},
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Topic :: Internet :: Name Service (DNS)",
        "Topic :: Internet :: Proxy Servers",
    ],
)
