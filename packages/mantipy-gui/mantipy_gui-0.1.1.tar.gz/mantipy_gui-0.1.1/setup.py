from setuptools import setup, find_packages

setup(
    name="mantipy-gui",
    version="0.1.1",
    packages=find_packages(),
    package_data={
        "mantipy_gui": ["themes/*.py", "resolvers/*.py"],
    },
    include_package_data=True,
    install_requires=[
        "PyQt5>=5.15.0",
        "PyQtWebEngine>=5.15.0",
    ],
    author="Cymos",
    author_email="cymos@manticore-tech.com",
    description="Modern Python GUI framework with web technology integration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/manticore-technologies/mantipy-gui",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 