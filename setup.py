import setuptools

from os import path
README = path.join(path.abspath(path.dirname(__file__)), 'README.md')
with open(README, encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="sponggy",
    version="0.0.2",
    author="Filip Dimitrovski",
    author_email="filip@tune.mk",
    description="sponggy - a Python tool for installing Caddy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fikisipi/sponggy",
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    entry_points = {
        'console_scripts': ['sponggy=sponggy:main']
    },
    install_requires=[
        'requests>=2.25.0',
        'tqdm>=4.50.0'
    ],
    package_data={
        "sponggy": ["*.target.exe", "*.LICENSE"]
    }
)
