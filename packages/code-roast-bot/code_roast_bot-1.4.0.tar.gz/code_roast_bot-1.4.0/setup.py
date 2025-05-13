from setuptools import setup, find_packages

setup(
    name="code_roast_bot",
    version="1.4.0",
    packages=find_packages(),
    install_requires=[
        "openai==1.16.2",
        "python-dotenv==1.0.1",
        "tiktoken==0.6.0",
        "tenacity==8.2.3",
        "colorama==0.4.6"
    ],
    entry_points={
        "console_scripts": [
            "code-roast=code_roast_bot.main:main",
        ],
    },
    author="Your Name",
    author_email="you@example.com",
    description="A sarcastic and secure GPT-powered Python code roaster.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/code-roast-bot",
    license="BSD-3-Clause",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
)
