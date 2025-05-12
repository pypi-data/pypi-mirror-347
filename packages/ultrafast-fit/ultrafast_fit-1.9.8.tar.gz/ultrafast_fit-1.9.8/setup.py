
# to set up as a package

from setuptools import setup, find_packages

setup(
    name="ultra",
    version="1.9.8",
    packages=find_packages(),  # no longer using "src"
    entry_points={
        "console_scripts": [
            "ultrafast-fit=ultra.main:main",
        ],
    },
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib"
        "lmfit",
        "scipy",
        "seaborn",
        "scikit-learn"
    ],
    python_requires=">=3.8",
)
