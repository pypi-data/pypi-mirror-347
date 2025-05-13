from setuptools import setup, find_packages

setup(
    name='legosec',
    version='0.1.1',
    description='Secure E2E Communication SDK using KDC, ECDH, and PSK-TLS',
    author='LegoSec Team',
    author_email='toleenabuadi@gmail.com',
    packages=find_packages(),  # Finds the 'legosec' package
    install_requires=[
        'cryptography>=41.0.3',
        'pyopenssl>=24.0.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.8',
)
