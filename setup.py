from setuptools import setup
import os

def get_requirements():
    """
    Populate a list with all required items for the program
    """

    requirements = []
    requirements_location = os.path.join(os.getcwd(), "requirements.txt")

    with open(requirements_location, encoding='utf-8') as requirements_file:
        for item in requirements_file:
            requirements.append(item.strip())

    return requirements

setup (
    name = "Individual Project",
    version="0.0.1",
    description="WIP",
    auther="Ryan Haynes",
    requires=get_requirements()
)
