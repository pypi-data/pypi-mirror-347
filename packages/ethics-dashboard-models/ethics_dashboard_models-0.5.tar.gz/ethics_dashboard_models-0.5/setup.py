from setuptools import setup, find_packages

setup(
    name='ethics_dashboard_models',
    version='0.5',
    author='Cody Jorgenson',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'flask_marshmallow',
    ],
)