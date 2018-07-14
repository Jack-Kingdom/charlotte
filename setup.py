from setuptools import setup, find_packages

setup(
    name='hummer',
    packages=find_packages(exclude=('tests', 'tests.*')),
    version='0.0.1',
    url='https://github.com/Jack-Kingdom/portalutils.git',
    description='Lightweight and expandable spider framework.',
    long_description=open('README.md').read(),

    author='Jack King',
    author_email='email@qiaohong.org',
    license='MIT',

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Natural Language :: English',
    ], install_requires=[
        'tornado'
    ]
)
