from setuptools import setup, find_packages

setup(
    name='starri',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'windows-curses; platform_system=="Windows"',
        'curses; platform_system!="Windows"',
    ],
    entry_points={
        'console_scripts': [
            'starri = starri.menu:starri',
        ],
    },
    description="A terminal-based menu system using curses.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Rowan Barker",
    author_email="barker.rowan@sugarsalem.com",
    url="https://github.com/lioen-dev/starri",
)
