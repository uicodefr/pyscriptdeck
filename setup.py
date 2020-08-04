from setuptools import setup, find_packages

with open('requirements.txt') as file:
    requirements = file.read().splitlines()

with open('requirements-test.txt') as file:
    requirements_test = file.read().splitlines()

setup(
    name="PyScriptDeck",
    version="0.2.0-SNAPSHOT",
    description="Web App that allows you to launch python scripts",
    url="https://github.com/uicodefr/pyscriptdeck",
    license="MIT",
    author="uicodefr",
    author_email="luc@uicode.fr",
    packages=find_packages(exclude=("tests", "tests.*", "pyscriptdemo", "pyscriptdemo.*")),
    python_requires=">=3.7",
    install_requires=requirements,
    include_package_data=True,
    tests_require=requirements_test
)
