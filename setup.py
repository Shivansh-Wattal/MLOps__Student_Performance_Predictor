'''
The setup script is the centre of all activity in building, distributing, and 
installing modules using the Distutils. The main purpose of the setup script is to 
describe your module distribution to the Distutils, so that the various commands 
that operate on your modules do the right thing.
The setup script consists mainly of a call to setup(), and most information 
supplied to the Distutils by the module developer is supplied as keyword arguments
to setup()
'''

from setuptools import find_packages,setup
from typing import List


HYPEN_E_DOT='-e .' # This is used at the end of requirements.txt file to mark the end.
def get_requirements(file_path:str)->List[str]:
    
    #Function returns the list of requirements from requirements.txt file
    
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements


# Calling the setup function.

setup(
name='ML_PROJECT_END_TO_END',
version='0.0.1',
author='Shivansh',
author_email='sunrise.wattal@gmail.com',
packages=find_packages(),
install_requires=get_requirements('requirements.txt')

)



