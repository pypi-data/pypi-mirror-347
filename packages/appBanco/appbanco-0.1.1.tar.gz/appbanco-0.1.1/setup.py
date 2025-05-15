from setuptools import setup, find_packages

setup(
    name='appBanco',
    version='0.1.1',
    packages=find_packages(),
    description='Simulador simples de banco em Python',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='K-Campassi',
    entry_points={
        'console_scripts': [
            'appBanco=appBanco.main:main'
        ],
    },
)
