from setuptools import setup, find_packages

setup(
    name='ethics_dashboard_models',
    version='0.6',
    author='Cody Jorgenson',
    license='MIT',
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'flask_marshmallow',
    ],
)