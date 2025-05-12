from setuptools import setup, find_packages

version = {}
with open("farsilang/__version__.py") as f:
    exec(f.read(), version)

setup(
    name='farsilang',
    version=version["__version__"],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'farsi=farsilang.runner:main',
        ],
    },
    install_requires=[],
    python_requires='>=3.7',
)