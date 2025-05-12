from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='torch-anatomy',
    version='0.1.1',
    description='Layer-by-layer visualizer for PyTorch models',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Harshal Vilas Kale',
    packages=find_packages(),
    install_requires=[
        'torch',
        'torchvision',
        'matplotlib',
        'numpy',
        'Pillow',
        'click'
    ],
    entry_points={
        'console_scripts': [
            'torch-anatomy=torch_anatomy.cli:main'
        ]
    },
    license="MIT",
)
