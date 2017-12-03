import unittest
import sqlineage


class TestExotics(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestExotics, self).__init__(*args, **kwargs)
        self.result = []

    def callback(self, parent, table, alias, query_alias, joins, operation, level):
        self.result.append((parent, table, alias, query_alias, joins, operation, level))

    def clear_result(self):
        self.result = []

    def verify_result(self, expected):
        self.assertEqual(expected, self.result)

    def run_test(self, filename, expected):
        self.clear_result()
        with open(filename, 'r') as infile:
            sql = infile.read()
            sqlineage.scan(sql, self.callback)
        self.verify_result(expected)

    def test_nolock_statements(self):
        self.run_test('tests/resources/exotics/nolock_statements.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','subselects','subselects','','','INSERT',1),
             ('ROOT','','','','','SELECT',1),
             ('','foo.bar.tablename','b','foo','','SELECT',2),
             ('','abc.dbo.xyz','c','foo','','SELECT',2),
             ('','abc.def.xyz','d','foo','','SELECT',2)])

    def test_brackets(self):
        self.run_test('tests/resources/exotics/brackets.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1),
             ('ROOT','[server].[database].[schema].[table]','[server].[database].[schema].[table]','','','SELECT',1)])

    def test_backtick(self):
        self.run_test('tests/resources/exotics/backtick.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1),
             ('ROOT',
                '`database.schema with a space.table with something else`',
                '`database.schema with a space.table with something else`',
                '',
                '',
                'SELECT',1)])
