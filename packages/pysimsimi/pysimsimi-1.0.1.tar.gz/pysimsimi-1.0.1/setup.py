from setuptools import setup, find_packages

setup(
    name='pysimsimi',
    version='1.0.1',
    description='Python wrapper for simi.anbuinfosec.live chat and teach API',
    author='Mohammad Alamin',
    author_email='anbuinfosec@gmail.com',
    url='https://github.com/anbuinfosec/pysimsimi',
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
