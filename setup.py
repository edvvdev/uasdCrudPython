from setuptools import setup, find_packages

setup(
    name="uasd-crud-python",
    version="1.0.0",
    description="CRUD/ORM nativo en Python con MariaDB - Maestría en Ciencia de Datos",
    author="Framiel Trinidad, Edwing Perez, Jharol Duran",
    author_email="",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "mysql-connector-python>=8.0.0",
        "pandas>=1.3.0",
        "numpy>=1.21.0",
    ],
    extras_require={
        "dev": [
            "python-dotenv>=0.19.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "uasd-crud=src.main:main",
        ],
    },
)
