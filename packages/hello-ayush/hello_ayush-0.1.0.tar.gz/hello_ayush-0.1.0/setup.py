from setuptools import setup, find_packages

setup(
    name='hello_ayush',                      # Your package name (must be unique on PyPI)
    version='0.1.0',                         # Version (follow semantic versioning)
    packages=find_packages(),                # Automatically finds all packages
    install_requires=[],                     # Add dependencies here if needed
    author='Ayush',
    author_email='youremail@example.com',
    description='A simple package that says hello to Ayush',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/hello_ayush',  # Optional
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
