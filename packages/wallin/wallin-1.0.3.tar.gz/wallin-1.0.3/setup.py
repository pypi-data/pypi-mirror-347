from setuptools import setup, find_packages

setup(
    name="wallin",
    version="1.0.3",
    description="Constraint-based Excel optimizer powered by OR-Tools",
    author="Jake Wallin",
    packages=find_packages(),
    install_requires=["pandas", "ortools"],
    python_requires=">=3.7",
    include_package_data=True,
)
