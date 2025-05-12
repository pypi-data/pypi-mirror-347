from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='CrystalPayAPI',
    version='1.2.0',
    author='outodev',
    description='Python SDK for CrystalPay.io payment system',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/outodev/CrystalPayAPI',
    packages=find_packages(),
    install_requires=['requests>=2.25.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    keywords='crystalpay payment api sdk',
)