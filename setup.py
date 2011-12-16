from setuptools import setup, find_packages

version = '1.2'

setup(name='zest.pocompile',
      version=version,
      description="Compile po files when releasing a package",
      long_description=open("README.txt").read() + "\n" +
                       open("CHANGES.txt").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Buildout",
        "Topic :: Software Development :: Internationalization",
        ],
      keywords='i18n locales po compile release',
      author='Maurits van Rees',
      author_email='m.van.rees@zestsoftware.nl',
      url='http://svn.plone.org/svn/collective/zest.pocompile',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['zest'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'python-gettext',
      ],
      entry_points={
          'console_scripts': [
              'pocompile = zest.pocompile.compile:main',
              ],
          'zest.releaser.releaser.after_checkout': [
              'zest_pocompile = zest.pocompile.compile:compile_in_tag',
              ],
          },
      )
