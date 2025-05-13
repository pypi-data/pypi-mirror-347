from setuptools import setup, find_packages

setup(
    name="scia",
    use_scm_version=True,  # Automatically manage versioning from Git tags
    setup_requires=["setuptools-scm"],  # Required for setuptools-scm versioning
    author="Mohammad Ahsan Khodami",
    author_email="ahsan.khodami@gmail.com",
    description="A Comprehensive most updated Python package for Single Case Design Analysis",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AhsanKhodami/scia",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "scipy",
        "openpyxl",
        "scikit-learn",
        "statsmodels",
    ],
)