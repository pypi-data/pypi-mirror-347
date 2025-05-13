from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='dm-aiomodbus',
    version='v0.3.9',
    author='dimka4621',
    author_email='mismartconfig@gmail.com',
    description='This is my custom aiomodbus client',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://pypi.org/project/dm-aiomodbus',
    packages=find_packages(),
    install_requires=[
        'dm-logger~=0.6.2',
        'pyserial==3.5',
        'pymodbus==3.8.6',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='dm aiomodbus',
    project_urls={
        'GitHub': 'https://github.com/MykhLibs/dm-aiomodbus'
    },
    python_requires='>=3.8'
)
