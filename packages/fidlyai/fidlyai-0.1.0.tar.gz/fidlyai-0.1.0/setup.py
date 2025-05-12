from setuptools import setup, find_packages

setup(
    name='fidlyai',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['requests'],
    author='Fidal Palamparambil',
    author_email='mrfidal@proton.me',
    description='FidlyAI is a highly effective AI package for Python, designed to be user-friendly.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://mrfidal.in/package/py/fidlyai',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
