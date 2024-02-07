from setuptools import setup

with open("README.md") as fp:
    """Returns the required readme defined in README.md"""
    long_description = fp.read()

setup(
    name="AmazonLookoutForVisionProject",
    version="0.1",
    description="This is the core module for the AI Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Michael Wallner",
    author_email="wallnm@amazon.com",
    python_requires=">3.7",
    install_requires=[
        "pre-commit==2.20.0",
        "pytest==7.2.1",
        "aws-cdk-lib==2.62.0",
        "cdk-nag==2.18.15",
        "checkov==2.2.289",
    ],
    tests_require=["pytest"],
    packages=["infrastructure"],)
