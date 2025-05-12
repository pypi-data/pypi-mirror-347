from setuptools import setup, find_packages

setup(
    name="aloo",  # Replace with your package name
    version="1",
    author="Anonymous Hackers",
    author_email="admin@anonymous.com",
    description="Simple Test Script",
    long_description=open("README.txt").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)