from setuptools import find_packages
from setuptools import setup


version = "1.6.0"

setup(
    name="zest.pocompile",
    version=version,
    description="Compile po files when releasing a package",
    long_description=(open("README.rst").read() + "\n" + open("CHANGES.rst").read()),
    # Get more strings from https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Buildout",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Internationalization",
    ],
    keywords="i18n locales po compile release",
    author="Maurits van Rees",
    author_email="m.van.rees@zestsoftware.nl",
    url="https://github.com/zestsoftware/zest.pocompile",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["zest"],
    include_package_data=True,
    zip_safe=False,
    install_requires=["setuptools", "python-gettext"],
    entry_points={
        "console_scripts": ["pocompile = zest.pocompile.compile:main"],
        "zest.releaser.releaser.after_checkout": [
            "zest_pocompile = zest.pocompile.compile:compile_in_tag",
        ],
    },
)
