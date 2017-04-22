from setuptools import setup, find_packages


setup(
        name='data-analysis',
        version='0.0.1',
        url='www.github.com/sandeez/data-analysis',
        license='BSD',
        author='Sandeep Sawant',
        packages=find_packages(),
        install_requires=[
                            'PyQt5',
                            'pandas',
                            'sqlalchemy',
                            'nltk',
                            'numpy',
                            'jupyter',
                            'python-twitter'
                        ],
        entry_points={},
        extra_require={'dev': ['flakes8',]},
    )