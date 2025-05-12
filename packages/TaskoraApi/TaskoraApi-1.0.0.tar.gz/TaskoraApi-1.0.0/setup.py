from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="TaskoraApi",
    version="1.0.0",
    description="Python client for interacting with the QuizAPI, InstagramApi , chatBot and reChaptchaV3 Solver using aiohttp, httpx, or requests.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sam",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/TaskoraApi",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
        "httpx>=0.24.0",
        "requests>=2.25.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.9',
)
