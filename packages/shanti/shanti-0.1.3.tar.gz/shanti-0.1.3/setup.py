from setuptools import setup, find_packages

setup(
    name="shanti",
    version="0.1.3",
    description="create SHarable, interactive, stANdalone html dashboard from Tabular proteomIcs data",
    author="Nara Marella",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "bokeh",
        "openpyxl",
        "scipy",
        "numpy"
    ],
    include_package_data=True,
)
