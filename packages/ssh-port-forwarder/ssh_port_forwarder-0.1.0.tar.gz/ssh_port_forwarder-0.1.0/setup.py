from setuptools import setup, find_packages

setup(
    name="ssh-port-forwarder",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="GUI SSH Port Forwarding Tool",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ssh-port-forwarder",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'paramiko>=3.0.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'ssh-port-forwarder=ssh_port_forwarder.app:main',
        ],
    },
)
