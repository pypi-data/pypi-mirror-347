from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='treasurykit',
    version='1.01',
    author='Konstantin Khorev',
    author_email='khorevkp@gmail.com',
    description='Tools for finance and treasury specialists',
    url='https://github.com/khorevkp/treasurykit',
    install_requires=['pandas', 'requests', 'lxml', 'xlsxwriter', 'openpyxl', 'zeep'],
    packages=['treasurykit'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)