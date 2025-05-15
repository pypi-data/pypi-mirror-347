from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='pysimsimi',
    version='1.0.0',
    description='Python wrapper for simi.anbuinfosec.live chat and teach API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Mohammad Alamin',
    author_email='anbuinfosec@gmail.com',
    url='https://github.com/anbuinfosec/pysimsimi',
    license='MIT',
    packages=find_packages(),
    install_requires=['requests'],
    keywords=[
        "simsimi", "simi", "pysimi", "pysimsimi", "chatbot",
        "chat", "teach", "API", "anbuinfosec"
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Chat',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
