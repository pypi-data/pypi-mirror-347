from setuptools import setup, find_packages

setup(
    name='molweightcal',
    version='0.1.0',
    author='Md. Ismiel Hossen Abir',
    author_email='ismielabir1971@gmail.com',
    description='A lightweight package to calculate molecular weights from chemical formulas.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)