
from setuptools import setup, find_packages

setup(
    name="img2ascii-cli",
    version="1.0.0",
    description="A CLI tool to convert images to ASCII art",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your-email@example.com",
    url="https://github.com/your-username/img2ascii-cli",
    packages=find_packages(),
    install_requires=["Pillow"],
    entry_points={
        'console_scripts': [
            'img2ascii=img2ascii.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
