from setuptools import setup, find_packages

setup(
    name='phoneme_converter',
    version='0.1',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    include_package_data=True,
    install_requires=[
        # Add any dependencies here
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
        ]
    },
)
