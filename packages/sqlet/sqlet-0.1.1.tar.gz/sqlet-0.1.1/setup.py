from setuptools import setup

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='sqlet',
  version='0.1.1',
  author='alextandr',
  author_email='alextandr.lpt@yandex.ru',
  description='SQL Easy Tools',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/MieSlie/sqlet',
  packages=['sqlet'],
  license_file="LICENSE",
  install_requires=['psycopg>=3.0'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: MIT License',
    "Intended Audience :: Developers",
    "Topic :: Database",
    'Operating System :: OS Independent'
  ],
  keywords='python database sqlite postgresql postgre sql',
  project_urls={
    'Documentation': 'https://github.com/MieSlie/sqlet/blob/main/README.md'
  },
  python_requires='>=3.10'
)