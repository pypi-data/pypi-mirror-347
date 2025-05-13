from setuptools import setup, find_packages

setup(
    name='debugonce',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A utility for capturing and reproducing bugs effortlessly by recording function calls and runtime context.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
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
)