from setuptools import setup, find_packages

setup(
    name="kaaas",  # Package name on PyPI
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'boto3',
        'pyyaml',
    ],
    author="Kashif Rafi",
    author_email="rafi.kashif@yahoo.com",
    description="Kubernetes AI-powered Cluster Analysis and Solution (KAAS)",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/kashifrafi/kaas",  # Update with your project URL
    keywords=["kubernetes", "ai", "cluster", "analysis", "k8sgpt", "llm"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: System :: Monitoring",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={
        'console_scripts': [
            'kaas=kaas.main:main',
        ],
    },
    include_package_data=True,  # Ensures non-Python files from MANIFEST.in are included
    python_requires='>=3.6',
)
