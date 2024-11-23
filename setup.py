from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="phantomfirewall",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="An intelligent, adaptive firewall system with ML capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/phantomfirewall",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: System :: Networking :: Firewalls",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pyyaml>=5.4.1",
        "netfilterqueue>=1.0.0",
        "scapy>=2.4.5",
        "numpy>=1.21.0",
        "scikit-learn>=0.24.2",
        "requests>=2.26.0",
        "pydantic>=1.8.2",
    ],
    entry_points={
        "console_scripts": [
            "phantom-firewall=phantomfirewall.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "phantomfirewall": ["config/*.yaml", "dashboard/build/*"],
    },
)
