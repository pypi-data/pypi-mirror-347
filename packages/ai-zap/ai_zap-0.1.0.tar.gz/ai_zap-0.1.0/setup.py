from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ai-zap",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
    ],
    author="Danila",
    author_email="your.email@example.com",
    description="Простая библиотека для отправки запросов к ИИ через функцию zap()",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DanilaLucifer/ai_zap",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    keywords="ai, chat, api, qwen",
) 