# setup.py

from setuptools import setup, find_packages

version = "0.1.0"

# Leer el contenido del README.md
with open("README.md", "r", encoding="utf-8") as f:
    descripcion_larga = f.read()

setup(
    name="algoritmos_geneticos_DG_PV",
    version=version,
    author="David Gomez - Paula Vera",
    author_email="davidleonardogomez@ucundinamarca.edu.co",
    description="Librería de algoritmos genéticos en español.",
    long_description=descripcion_larga,
    long_description_content_type="text/markdown",
    url="https://github.com/oxgerrero/algoritmos_geneticos_DG_PV",
    project_urls={
        "Documentación": "https://github.com/oxgerrero/algoritmos_geneticos_DG_PV",
        "Código fuente": "https://github.com/oxgerrero/algoritmos_geneticos_DG_PV",
        "Reportar errores": "https://github.com/oxgerrero/algoritmos_geneticos_DG_PV/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Spanish",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    packages=find_packages(),
    python_requires=">=3.11.8",
)
