from setuptools import find_packages, setup
from typing import List 


def get_requirements() -> List[str] :
    """
    This function will return list of requirements
    """
    requirements_lst: List[str] = []
    try:
        with open("requirements.txt" , "r") as file:
            ##Read lines from the file 
            lines = file.readlines()
            for line in lines:
                requirements = line.strip()
                ##ignore the empty line and -e .
                if requirements and requirements != '-e .':
                    requirements_lst.append(requirements)
    except FileNotFoundError:
        print("Requirements.txt file not found")

    return requirements_lst


setup(
    name="Cys-Network-Security",
    version="0.0.1",
    author="shayan Jafri",
    author_email="shayanjafri67@gmail.com",
    packages=find_packages(where="src"),   # look inside src/
    package_dir={"": "src"},
    install_requires=get_requirements()
)