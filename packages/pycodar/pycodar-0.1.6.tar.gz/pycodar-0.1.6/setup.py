from setuptools import setup, find_packages

setup(
    name="pycodar",
    version="0.1.6",
    packages=find_packages(),
    install_requires=[
        "rich>=10.0.0",
        "typer>=0.9.0",
        "pathspec>=0.11.0",
    ],
    entry_points={
        'console_scripts': [
            'pycodar=pycodar.cli:main',
        ],
    },
    author="Quentin Wach",
    author_email="quentin.wach@gmail.com",
    description="A simple tool for auditing and understanding your codebase",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/QuentinWach/pycodar",
    project_urls={
        "Bug Tracker": "https://github.com/QuentinWach/pycodar/issues",
        "Documentation": "https://github.com/QuentinWach/pycodar#readme",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.6",
    keywords="code-analysis, architecture, metrics, codebase, development-tools",
    zip_safe=False,  # Ensure the package is installed as a directory, not a zip file
    include_package_data=True,  # Include any non-Python files in the package
) 