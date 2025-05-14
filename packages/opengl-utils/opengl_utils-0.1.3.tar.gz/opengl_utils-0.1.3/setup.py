from setuptools import setup, find_packages

setup(
    name="opengl_utils",
    version="0.1.3",
    
    packages=find_packages(),
    install_requires=[

    ],
    author="John Machanzy",
    author_email="jphn@machanzy.com",
    description="A utility package for OpenGL",
    long_description="a helper utility to help creating good gl graphics",
    long_description_content_type="text/markdown",
    url="https://github.com/johndoe/opengl_utils",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)