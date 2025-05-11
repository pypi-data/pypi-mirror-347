from setuptools import setup

version = None


setup(
    name="dhenara",
    version="1.0.3",
    install_requires=[
        "dhenara-ai>=1.0.0",
    ],
    extras_require={},
    python_requires=">=3.10",
    description="DEPRECATED: Please use dhenara-ai instead",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Dhenara",
    author_email="support@dhenara.com",
    url="https://github.com/dhenara/dhenara-ai",
    license="MIT",  # Replace with your actual license
    keywords="ai, llm, machine learning, language models",
    project_urls={
        "Homepage": "https://dhenara.com",
        "Documentation": "https://docs.dhenara.com/",
        "Bug Reports": "https://github.com/dhenara/dhenara-ai/issues",
        "Source Code": "https://github.com/dhenara/dhenara-ai",
    },
    classifiers=[
        # "Development Status :: 7 - Inactive",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
    ],
    include_package_data=True,
)
