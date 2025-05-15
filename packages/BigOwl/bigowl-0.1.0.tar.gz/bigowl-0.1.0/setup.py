from setuptools import setup, find_packages

setup(
    name='BigOwl',
    version='0.1.0',
    author='Atharva Rahate',
    author_email='atharvarahate374@example.com',  # Using a placeholder based on your GitHub username
    description='An intelligent time and space complexity analyzer for Python code.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/CrazAr374/BigOwl',
    packages=find_packages(),
    install_requires=[
        'asttokens',
        'networkx',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    license='MIT',  # Use modern license field instead of classifier
    python_requires='>=3.6',
)