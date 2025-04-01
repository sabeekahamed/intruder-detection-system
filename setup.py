from setuptools import setup, find_packages

setup(
    name="ai_powered_ids",
    version="0.1.0",
    description="AI-Powered Intrusion Detection System for Network Security",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/sabeekahamed/intruder-detection-system",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Security",
        "Topic :: System :: Networking :: Monitoring",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "tensorflow>=2.6.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "plotly>=5.3.0",
        "scapy>=2.4.5",
        "jinja2>=3.0.0",
        "tqdm>=4.62.0",
        "networkx>=2.6.0",
    ],
    entry_points={
        "console_scripts": [
            "aipids=main:main",
        ],
    },
)