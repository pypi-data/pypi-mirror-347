from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gemiTask",
    version="0.1.1",
    author="Sanjay Malladi",
    author_email="malladisanjay29@gmail.com",
    description="AI-powered terminal task manager using Google's Gemini",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sanjaymalladi/gemiTask",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        "google-generativeai>=0.3.0",
        "python-dateutil>=2.8.2",
        "rich>=10.0.0",  # For beautiful terminal interface
    ],
    entry_points={
        "console_scripts": [
            "gemiTask=gemiTask.main:main",
        ],
    },
    keywords="cli, task-management, ai, gemini, productivity, todo",
) 