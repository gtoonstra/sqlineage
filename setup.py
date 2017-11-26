from distutils.core import setup, Extension

sqlineage = Extension('sqlineage',
                    define_macros = [('MAJOR_VERSION', '0'),
                                     ('MINOR_VERSION', '1')],
                    include_dirs = ['/usr/local/include'],
                    # libraries = ['tcl83'],
                    library_dirs = ['/usr/local/lib'],
                    # sources = ['src/sqlineage.c'])
                    sources = ['src/sqlscanner.c', 'src/state_machine.c'])

setup (name = 'sqlineage',
       version = '0.1.1',
       description = 'A parser for SQL',
       author = 'G. Toonstra',
       author_email = 'gtoonstra@gmail.com',
       url = 'https://github.com/gtoonstra/sqlineage',
       long_description = '''
This package parses SQL files and allows you to build a hierarchy
of select and insert statements that lists the identifiers, so you
can build a model that reflects data lineage in the statements and
how data flows.
''',
       ext_modules = [sqlineage])
