from setuptools import setup
from os import path

setup(
    name='AI_PROJECT_JLK',  # Replace with your package name
    version='0.0.1',  # Replace with your version number
    description='This is for a project I took with SRJC.  ',  # Replace with a short description of your package
    author='JediL',  # Replace with your name
    author_email='HeyDidej101@gmail.com',  # Replace with your email
    packages=['AI_PROJECT_JLK'],  # Replace with the name of your package folder
    install_requires=[],
    package_data={
        'AI_PROJECT_JLK': ['my_pics2/*']},
    include_package_data=True,
)