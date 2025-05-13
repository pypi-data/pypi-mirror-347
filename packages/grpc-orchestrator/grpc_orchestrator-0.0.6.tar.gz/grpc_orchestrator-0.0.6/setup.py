from setuptools import setup, find_packages

with open("README.md", "r") as file:
    description = file.read()

setup(
    name="grpc_orchestrator",
    version="0.0.6",
    author="Ron Saroeun",
    author_email="ronsaroeun668@gmail.com",
    url="https://github.com/bunrongGithub/grpc_orchestrator/tree/backup/simple_python_sdk",
    long_description=description,
    long_description_content_type="text/markdown",
    description="A gRPC-based Saga Orchestration System for distributed transactions",
    packages=find_packages(),
   classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries",
    "Topic :: System :: Distributed Computing",
    "Framework :: AsyncIO",
],

    python_requires=">=3.7",
    install_requires=[
        "grpcio>=1.56",
        "protobuf>=4.21"
    ],
    keywords=[
        "grpc",
        "grpc orchestrator",
        "grpc microservices",
        "distributed transactions",
        "python grpc",
        "saga pattern",
        "grpc saga",
        "transaction orchestrator",
        "python microservices",
    ],
    include_package_data=True,
)
