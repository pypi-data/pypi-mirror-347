# setup.py
from setuptools import setup, find_packages

setup(
    name="django-nginx-generator",
    version="1.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=[
        "click>=8.0",
        "jinja2>=3.0",
        "Django>=3.2",
    ],
    entry_points={
        "console_scripts": [
            "generate_nginx=django_nginx_generator.cli:main",
        ],
    },
    author="Amirreza Jabbari",
    author_email="amirrezajabbari79@gmail.com",
    description="CLI tool to auto-generate production-grade Nginx configs for Django",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/amirreza-jabbari/django-nginx-generator",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Systems Administration",
    ],
)
