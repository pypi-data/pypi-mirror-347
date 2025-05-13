from setuptools import setup, find_packages

setup(
    name="loglikelihood_estimator_1",
    version="0.1.0",
    author="Sandeep Mudhurakola",
    author_email="your.email@example.com",
    description="Log-likelihood estimator for stochastic frontier models with endogeneity (LIML component)",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab2.tamucc.edu/smudhurakola/loglikehood_estimator_1",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "numpy",
        "scipy",
        "pandas",
        "matplotlib",
    ],
    include_package_data=True,
)
