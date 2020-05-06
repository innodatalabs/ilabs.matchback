from setuptools import setup
from ilabs.matchback import __version__, __description__, __url__, __author__, \
    __author_email__, __keywords__

NAME = 'ilabs.matchback'

setup(
    name=NAME,
    version=__version__,
    description=__description__,
    long_description='See ' + __url__,
    url=__url__,
    author=__author__,
    author_email=__author_email__,
    keywords=__keywords__,

    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=[NAME],
    namespace_packages=['ilabs'],
    install_requires=['lxml'],
    entry_points={
        'console_scripts': [
            'matchback=ilabs.matchback.main:main',
        ]
    }
)
