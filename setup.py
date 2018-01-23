from setuptools import setup, find_packages

setup(
    name='Dancesafe',
    version='',
    packages=find_packages(),
    url='https://github.com/siorai/DancesafeResults',
    license='',
    author='Siorai',
    author_email='',
    description='', 
    install_requires=['flask', 'flask-bcrypt', 'sqlalchemy=1.1.14', 'wtforms', 'flaskbootstrap', 'psycopg2', 'webcolors',
                      'sqlalchemy']
)
