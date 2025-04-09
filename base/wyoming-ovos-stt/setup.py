#!/usr/bin/env python3
from pathlib import Path

import setuptools
from setuptools import setup

this_dir = Path(__file__).parent

requirements = []
requirements_path = this_dir / "requirements.txt"
if requirements_path.is_file():
    with open(requirements_path, "r", encoding="utf-8") as requirements_file:
        requirements = requirements_file.read().splitlines()

module_name = "wyoming_ovos_stt"
module_dir = this_dir / module_name
data_files = []

version = "0.1.0"

# -----------------------------------------------------------------------------

setup(
    name=module_name,
    version=version,
    description="Wyoming Server for OpenVoiceOS STT plugins",
    url="http://github.com/TigreGotico/wyoming-ovos-stt",
    author="JarbasAI",
    author_email="jarbasai@mailfence.com",
    license="MIT",
    packages=setuptools.find_packages(),
    package_data={module_name: [str(p.relative_to(module_dir)) for p in data_files]},
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="wyoming OVOS stt",
    entry_points={
        "console_scripts": ["wyoming-ovos-stt = wyoming_ovos_stt.__main__:run"]
    },
)
