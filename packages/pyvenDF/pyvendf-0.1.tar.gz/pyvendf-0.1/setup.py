from setuptools import setup, find_packages

setup(
    name='pyvenDF',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'pyvenDF=pyvenDF.cli:main'
        ]
    },
    author='LESLIE CHEGHE NJUH',
    description='A lightweight Python web framework',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
