import re
import ast
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('qwxwhat.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(name='qwxwhat',
      version=version,
      description="QuantumWorldX's pythonwhat test for datacamp- high level SCTs",
      url='https://pythonhosted.org/quantumworldX/',
      py_modules=['qwxwhat'],
      install_requires=['pythonwhat>=2.7'],
      author='Benjamin Sanchez-Lengeling',
      author_email='beangoben@gmail.com',
      license='MIT',
      zip_safe=False)
