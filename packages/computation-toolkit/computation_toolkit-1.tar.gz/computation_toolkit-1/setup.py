from setuptools import setup, find_packages

setup(
    name="computation_toolkit",
    version="1",
    packages=find_packages(),
    install_requires=[],
    author="Ammar Khaled",
    author_email="",
    description="Theory of Computation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Ammar-Khaled/automata_practical_exam_ammar_khaled.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
