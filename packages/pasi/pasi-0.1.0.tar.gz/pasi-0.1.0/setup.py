from setuptools import setup, find_packages

setup(
    name="pasi",
    version="0.1.0",
    packages=["pasi_test"],
    install_requires=[
        "numpy",
        "scipy",
        "scikit-learn",
        "joblib",
        "numba",
        "pandas",
        "progressbar2",
    ],
    author="Ruotao Zhang",
    author_email="zrtpublic@gmail.com", 
    description="Prediction Accuracy Subgroup Identification - Find subgroups with differential model performance",
    long_description=open("README.md", "r").read() if open("README.md", "r") else "PASI: Prediction Accuracy Subgroup Identification",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pasi",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.6",
) 