from distutils.core import setup
from setuptools import find_packages

with open('README.rst', 'r', encoding="utf-8") as f:
    long_description = f.read()

setup(name='fast-mq-task',
      version='1.0.5',
      description='fast rabbitmq task for zsodata',
      long_description=long_description,
      author='zsodata',
      author_email='team@zso.io',
      url='http://www.zsodata.com',
      install_requires=[
      ],
      python_requires='>=3.7',
      license='BSD License',
      packages=find_packages(),
      platforms=['all'],
      include_package_data=True
      )
