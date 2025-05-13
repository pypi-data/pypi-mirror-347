from setuptools import setup, find_packages

# Lê o arquivo requirements.txt
with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().splitlines()  # Divide as linhas em uma lista

setup(
    name='google_account_client',
    description='Google Account API',
    version='1.0.0',
    author='DIACDE - TJGO',
    python_requires=">=3.9.4",
    install_requires=requirements,  # Passa as dependências para install_requires
    license='CC BY-NC-SA 4.0',
    packages=find_packages(),
)
