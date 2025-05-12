from setuptools import find_packages, setup


def readme():
    with open("README.md", "r") as f:
        return f.read()


setup(
    name="shapesqr",
    version="0.0.2",
    author="DmitriyReztsov",
    author_email="rezcov_d@mail.ru",
    description="This is the test task module for shapes square calculation.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/DmitriyReztsov/shapesqr",
    packages=find_packages(),
    install_requires=["typing-extensions-4.13.2"],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="circle triangle square calculation",
    project_urls={"GitHub": "https://github.com/DmitriyReztsov"},
    python_requires=">=3.10",
)
