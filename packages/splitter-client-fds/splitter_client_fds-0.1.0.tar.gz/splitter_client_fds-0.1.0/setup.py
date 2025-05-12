from setuptools import setup, find_packages
import os

setup(
    name="splitter-client-fds",
    version="0.1.0",
    author="Splitter Team",
    description="A modern federated/split learning lab portal with Next.js frontend and FastAPI backend.",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        'console_scripts': [
            'splitter-fds=splitter_client_fds.cli:main',
        ],
    },
    package_data={
        'splitter_client_fds': [
            'backend/*',
            'frontend/*',
            'frontend/public/*',
            'frontend/src/*',
        ],
    },
    python_requires='>=3.8',
)
