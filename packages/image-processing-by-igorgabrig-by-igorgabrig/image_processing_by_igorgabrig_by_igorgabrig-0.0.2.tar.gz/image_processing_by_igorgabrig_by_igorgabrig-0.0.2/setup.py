from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing_by_igorgabrig_by_igorgabrig",
    version="0.0.2",
    author="IgorGabrig",
    description="Image Processing Package Using Skimage",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/igorgabrig/image-processing-package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.5',
)