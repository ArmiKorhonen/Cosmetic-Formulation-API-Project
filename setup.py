from setuptools import find_packages, setup

setup(
    name="CosmeApi",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Flask==3.0.2",
        "Flask-Migrate==4.0.5",
        "Flask-RESTful==0.3.10",
        "Flask-SQLAlchemy==3.1.1",
        "aniso8601==9.0.1",
        "blinker==1.7.0",
        "itsdangerous==2.1.2",
        "Jinja2==3.1.3",
        "MarkupSafe==2.1.5",
        "SQLAlchemy==2.0.25",
        "Werkzeug==3.0.1",
    ],
    extras_require={
        "dev": [
            "pytest==8.0.2",
            "pytest-flask==1.3.0",
            "pylint==3.1.0",
            "alembic==1.13.1",
        ]
    }
)
