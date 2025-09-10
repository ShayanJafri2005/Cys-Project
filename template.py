import os
from pathlib import Path
import logging 


project_name = "Cys-Project"


list_of_files = [
    ".github/workflows/main.yaml",
    ".gitignore",
    f"{project_name}-Data/__init__.py",
    f"src/{project_name}/__init__.py", ##---Main Folder Structure
    f"src/{project_name}/components/__init__.py", ## All the pipelines are developed in the components
    f"src/{project_name}/utils/__init__.py", ## All the generic functionalities are ein the utils
    f"src/{project_name}/utils/gen_functions.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipline/__init__.py", ## All the training testing pipelines
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py", ## All the configuration details
    f"src/{project_name}/logging/__init__.py", ## All the custom Logges are tracked here
    f"src/{project_name}/exception/__init__.py", 
    f"src/{project_name}/cloud/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    "config/config.yaml",
    "params.yaml", ### Define all params for ml model
    "schema.yaml",
    "main.py",
    "Dockerfile",
    "requirements.txt",
    "setup.py",   ### use libraries as a package
    "notebooks/experiments.ipynb",
    "templates/index.html", ##for webapp 
    "app.py",
    ".env"
]


for filepath in list_of_files:
    filepath=Path(filepath)
    filedir,filename=os.path.split(filepath)


    if filedir!="":
           
       os.makedirs(filedir,exist_ok=True)

       logging.info(f"Creating directory{filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0): ## if file doesnot exist
        with open(filepath, "w") as f:
            pass 
            logging.info(f"Creating empty file")

    else:
        logging.info(f"{filename} is already exist")