from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_descriptions = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name='meu-pacote-imagem-teste-2025-232434',
    version='0.0.1',
    author="Vicenzo",
    description='Um pacote simples para processar imagens com Python',
    long_description=long_descriptions,
    long_description_content_type='text/markdown',
    url='https://github.com/vixnzin/image-processing-package',
    packages = find_packages(),
    install_requires = requirements,
    python_requires='>=3.8',
)
