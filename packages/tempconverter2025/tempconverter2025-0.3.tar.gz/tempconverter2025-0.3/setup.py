from setuptools import setup

setup(
    name='tempconverter2025',
    version='0.3',  # ПОВЫШАЕМ версию!
    py_modules=['temp_converter'],
    author='Boss',
    author_email='Vladimirtlv@gmail.com',
    description='Simple temperature conversion library with requests dependency',
    url='https://github.com/Cryptonations/tempconverter2025',
    install_requires=[
        'requests'
    ],
)
