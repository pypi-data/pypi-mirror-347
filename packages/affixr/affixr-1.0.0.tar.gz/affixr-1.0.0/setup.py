from setuptools import setup, find_packages

setup(
    # ===============================================
    name="affixr",
    version='1.0.0',
    author="Armani Ruiz",
    author_email="<armanini1@gmail.com>",
    description='Affixr package',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    # ===============================================
    packages=find_packages(),
    install_requires=["first-rec", "safe-return"],
    # ===============================================
    keywords=['affixr'],
    classifiers = [
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
    ],
    # ===============================================
    include = ["LICENSE", "README.md"],
    license = "MIT License",
    # ===============================================
)
