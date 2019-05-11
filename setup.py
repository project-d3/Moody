import io

from setuptools import find_packages, setup

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='Moody',
    version='1.0.0',
    url='https://github.com/Ludikrous/Moody',
    license='BSD',
    maintainer='Ludikrous, Nikolay-Pomytkin, ryanmao725',
    maintainer_email='',
    description='A facial expression recognition app that allows users to track their moods over time.',
    long_description=README,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)