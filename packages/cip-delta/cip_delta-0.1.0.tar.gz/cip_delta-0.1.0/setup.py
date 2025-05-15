from setuptools import setup, find_packages

setup(
    name="cip-delta",  # 'cip' provavelmente já está ocupado — use um nome único
    version="0.1.0",
    description="Cifra de Integridade Primal (CIP) — segurança vetorial baseada em estrutura espectral dos primos",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Alvaro Costa",
    author_email="costaalv@alumni.usp.br",  # opcional, mas recomendado
    url="https://github.com/costaalv/projeto-delta",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.20",
        "sympy>=1.9"
    ],
    python_requires=">=3.7",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    keywords="integridade primal espectro criptografia pós-quântica verificação",  # ajuda na busca no PyPI
    include_package_data=True,
)

