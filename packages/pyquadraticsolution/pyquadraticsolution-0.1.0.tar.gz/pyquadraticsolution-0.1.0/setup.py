from setuptools import setup, find_packages

setup(
    name="pyquadraticsolution",
    version="0.1.0",
    author="Md. Ismiel Hossen Abir",
    author_email="ismielabir1971@gmail.com",
    description="A callable Python package that solves and explains quadratic equations.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    python_requires='>=3.6',
)