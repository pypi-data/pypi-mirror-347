from setuptools import setup, find_packages




setup(
    name='utils_AxN_2237', 
    author='Vataselu Andrei, Nicola-Diana Sincaru',
    author_email='andreivataselu42@gmail.com',
    description='A modular set of data science utilities for EDA, cleaning, and more.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    use_scm_version=True, #auto_version
    setup_requires=["setuptools_scm"], #auto_version
    url='https://github.com/vAndrewKarma/data-science-snippets',
    packages=find_packages(),
install_requires=[
    'numpy>=1.24.4',
    'pandas>=1.5.3',
    'matplotlib>=3.6.3',
    'seaborn>=0.12.2'
],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
