from setuptools import setup, find_packages

setup(
    name="collaborative_code_editor",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "python-jose[cryptography]",
        "passlib",
        "bcrypt",
        "psycopg2-binary",
    ],
)