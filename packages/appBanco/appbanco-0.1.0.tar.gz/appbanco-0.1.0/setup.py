from setuptools import setup, find_packages

setup(
    name='appBanco',
    version='0.1.0',
    packages=find_packages(),
    description='Simulador simples de banco em Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='K-Campassi',
    entry_points={
        'console_scripts': [
            'appBanco=appBanco.main:main'
        ],
    },
)
