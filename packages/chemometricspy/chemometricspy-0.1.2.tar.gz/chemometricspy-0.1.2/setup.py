from setuptools import setup, find_packages

setup(
    name='chemometricspy',
    version='0.1.0',
    description='A scientific Python library for chemometric modeling.',
    author='Leonardo Guimarães',
    author_email='leo.sguimaraes4@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy',
        'pandas'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
