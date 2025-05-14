#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="interaction-logger",
    version="0.3.0",
    author="Josphat-n",
    author_email="josphatnjoroge254@gmail.com",
    description="A package for logging user interactions with a django distributed system.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.10",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Framework :: Django",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["django", "logging", "user activity", "audit trail", "monitoring"],
    packages=["interaction_logger"],
    include_package_data=True,
    install_requires=[
        "Django>=4.2.0",
        "django-user-agents>=0.4.0",
        "python-json-logger>=2.0.7",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-django>=4.5.0",
            "black>=23.0.0",
            "isort>=5.10.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "coverage>=7.0.0",
        ],
    },
    package_data={
        "interaction_logger": ["migrations/*.py", "templates/*.html", "static/*"],
    },
)