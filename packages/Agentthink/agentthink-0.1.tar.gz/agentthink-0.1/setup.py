from setuptools import setup, find_packages

setup(
    name="Agentthink",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'requests',
        'pathlib'# for fetching blobs or URLs
    ],
    description="A library to process data as binary files and serve it to models",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Your Name",
    author_email="your.email@example.com",
    url="https://yourprojecturl.com",
)
