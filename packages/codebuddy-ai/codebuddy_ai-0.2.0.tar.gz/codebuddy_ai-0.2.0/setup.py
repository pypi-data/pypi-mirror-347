# setup.py

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Read the README file, using the correct encoding.
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="codebuddy-ai", #old name: "commit-generator",
    version="0.2.0",
    description="AI-powered CLI to generate commit messages, review code, and suggest fixes",
    author="Naman Kansal",
    author_email="namankansal91@gmail.com",
    url="https://github.com/UP11SRE/agent-client",  # GitHub URL
    license="Proprietary",
    long_description=long_description,  # This is your README content.
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "codebuddy=app.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)