# setup.py
from setuptools import setup, find_packages
# ✅ Define `requirements` before using it
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="causal_forecast",
    version="0.0.4",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'causal_forecast=causal_forecast.cli:main',
        ],
    },
    author="Aviral Srivastava",
    author_email="aviralsrivastava284@gmail.com",
    description="Get the causal_forecast analysis",
    long_description_content_type='text/markdown',
    url="https://github.com/A284viral/causal_forecast",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)