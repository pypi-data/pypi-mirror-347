from setuptools import setup, find_packages

setup(
    name="django_nginx_generator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0",
        "jinja2>=3.0",
        "Django>=3.2",
    ],
    author="Amirreza Jabbari",
    description="CLI tool to auto-generate production-grade Nginx configs for Django",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/youruser/django-nginx-generator",
    author_email="amirrezajabbari79@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Systems Administration",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/amirreza-jabbari/django-nginx-generator/issues",
        "Source Code": "https://github.com/amirreza-jabbari/django-nginx-generator",
        "Documentation": "https://github.com/amirreza-jabbari/django-nginx-generator#readme",
    },
)
