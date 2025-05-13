from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name =                              "xprcess_img",
    version =                           "0.0.1",
    author =                            "yukio",
    author_email =                      "o.manifesto.da.riqueza@gmail.com",
    long_description =                  page_description,
    long_description_content_type =     "text/markdown",
    url =                               "https://github.com/engcarlo/image-processing-package",
    packages =                          find_packages(),
    install_requires =                  requirements,
    python_requires =                   '>=3.8'
)