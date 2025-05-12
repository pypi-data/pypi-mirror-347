from setuptools import setup, find_packages

setup(
    name="dmchat",
    version="0.1.0",
    author="Kamal Choudhary",
    author_email="deepmaterialsllc@gmail.com",
    description="Materials Science Chatbot ",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/deepmaterials/dmchat",
    project_urls={
        "Bug Tracker": "https://github.com/deepmaterials/dmchat/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    install_requires=[
        "Django>=3.2",
        "requests",  # Add any other dependencies here
    ],
    python_requires=">=3.7",
    include_package_data=True,
)

