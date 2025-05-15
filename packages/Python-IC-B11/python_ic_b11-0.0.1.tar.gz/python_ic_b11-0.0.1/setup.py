from setuptools import setup, find_packages

setup(
    name='Python-IC-B11',
    version='0.0.1',
    package=find_packages(),
    install_requires=[],
    author="IC Batch 11",
    author_email="ICB11@IC.com",
    description="This is Our First Developed Pypi Package Python-IC-B11",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.0'

)