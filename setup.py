from pathlib import Path
from setuptools import setup


version = "2.0.0a1"
long_description = (
    f"{Path('README.rst').read_text()}\n{Path('CHANGES.rst').read_text()}\n"
)

setup(
    name="zest.pocompile",
    version=version,
    description="Compile po files when releasing a package",
    long_description=long_description,
    # Get more strings from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Buildout",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Internationalization",
    ],
    keywords="i18n locales po compile release",
    author="Maurits van Rees",
    author_email="m.van.rees@zestsoftware.nl",
    url="https://github.com/zestsoftware/zest.pocompile",
    license="GPL",
    packages=["zest.pocompile"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=["setuptools", "python-gettext"],
    entry_points={
        "console_scripts": ["pocompile = zest.pocompile.compile:main"],
        "zest.releaser.releaser.after_checkout": [
            "zest_pocompile = zest.pocompile.compile:compile_in_tag",
        ],
    },
)
