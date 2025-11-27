"""
Setup script for the Book Store project
"""
from setuptools import setup, find_packages

setup(
    name='fiap-mle-book-store',
    version='1.0.0',
    description='Book Store API and Web Scraper',
    author='FIAP MLE',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'Flask>=3.0.0',
        'Flask-CORS>=4.0.0',
        'Flask-RESTful>=0.3.10',
        'requests>=2.31.0',
        'beautifulsoup4>=4.12.2',
        'lxml>=4.9.3',
        'pandas>=2.1.3',
        'python-dotenv>=1.0.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.3',
            'pytest-cov>=4.1.0',
        ]
    },
    entry_points={
        'console_scripts': [
            'bookstore-api=api.app:main',
            'bookstore-scraper=scraper.main:main',
        ],
    },
)

