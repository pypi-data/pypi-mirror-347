from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    description = fh.read()

setup(
    name='debugonce',
    version='0.2.0',
    author='Your Name',
    author_email='your.email@example.com',
    #long_description=open('README.md').read(),
    url='https://github.com/yourusername/debugonce',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'click',
        'psutil',
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    long_description=description,
    long_description_content_type='text/markdown',
)