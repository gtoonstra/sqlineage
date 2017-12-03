from setuptools import setup, Extension

sqlineage = Extension('sqlineage',
                      define_macros=[('MAJOR_VERSION', '0'),
                                     ('MINOR_VERSION', '1')],
                      include_dirs=['/usr/local/include'],
                      library_dirs=['/usr/local/lib'],
                      sources=['src/sqlscanner.c', 
                               'src/state_machine.c'])

setup(name='sqlineage',
      version='0.1.0',
      description='A scanner for SQL',
      author='G. Toonstra',
      author_email='gtoonstra@gmail.com',
      url='https://github.com/gtoonstra/sqlineage',
      license='Apache2',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3'
      ],
      keywords='sql scanner parser',
      python_requires='>=3',
      long_description='''
This package parses SQL files and allows you to build a hierarchy
of select and insert statements that lists the identifiers, so you
can build a model that reflects data lineage in the statements and
how data flows.
''',
      ext_modules=[sqlineage])
