from setuptools import setup, find_packages

short_descr = "Parallel traversal algorithms for MTG"

readme = open('README.rst').read()
history = open('HISTORY.rst').read()

#find packages
pkgs = find_packages('src')

setup_kwds = dict(
    name = 'parallel_mtg',
    version = "0.0.1",
    description = short_descr,
    long_description = readme + '\n\n' + history,
    author = "Begatim Bytyqi",
    author_email = "begatimi_95@outlook.com",
    url = '',
    license = 'cecill-c',
    zip_safe = False,
    
    packages = pkgs,
    package_dir = {'': 'src'},
    setup_requires=[
        "pytest-runner",
    ],
    install_requires=[
    ],
    tests_require=[
        "pytest",
        "pytest-mock",
    ],
    entry_points={},
    keywords='',
)

setup(**setup_kwds)