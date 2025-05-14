from setuptools import setup, find_packages

setup(
    name='volatility-targeting',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['numpy', 'pandas'],
    author='Your Name',
    author_email='your@email.com',
    description='Volatility targeting for equal risk portfolio weighting.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/volatility-targeting',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
