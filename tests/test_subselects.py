import unittest
import sqlineage


class TestSubselects(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSubselects, self).__init__(*args, **kwargs)
        self.result = []

    def callback(self, parent, table, alias, query_alias, operation, level):
        self.result.append((parent, table, alias, query_alias, operation, level))

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

    def test_subselect(self):
        self.run_test('tests/resources/subselects/subselect.sql', 
            [('ROOT','ROOT','ROOT','','NONE',0),
             ('ROOT','subselects','subselects','','INSERT',1),
             ('ROOT','','','','SELECT',1),
             ('','foo.bar.tablename','b','foo','SELECT',2),
             ('','abc.dbo.xyz','c','foo','SELECT',2),
             ('','abc.def.xyz','d','foo','SELECT',2)])

    def test_simple(self):
        self.run_test('tests/resources/subselects/simple.sql', 
            [('ROOT','ROOT','ROOT','','NONE',0),
             ('ROOT','subselects','subselects','','INSERT',1),
             ('ROOT','','','','SELECT',1),
             ('','foo.bar.tablename','b','foo','SELECT',2)])

    def test_column_select(self):
        self.run_test('tests/resources/subselects/column_select.sql', 
            [('ROOT','ROOT','ROOT','','NONE',0),
             ('ROOT','foo','foo','','INSERT',1),
             ('ROOT','db.schema.table','a','','SELECT',1)])

    def test_subselect_with_union(self):
        self.run_test('tests/resources/subselects/subselect_with_union.sql', 
            [('ROOT','ROOT','ROOT','','NONE',0),
             ('ROOT','foo','foo','','INSERT',1),
             ('ROOT', '', '', '', 'SELECT', 1),
             ('', 'db.schema.view', 't', 'abc', 'SELECT', 2),
             ('', '', '', 'abc', 'SELECT', 2),
             ('', 'bar', 'bar', 'def', 'SELECT', 3)])

    def test_union_all_select_subquery(self):
        self.run_test('tests/resources/subselects/union_all_select_subquery.sql', 
            [('ROOT','ROOT','ROOT','','NONE',0),
             ('ROOT', 'db.schema.bar', 'bar', '', 'SELECT', 1),
             ('ROOT', 'db.schema.bas', 'bas', '', 'SELECT', 1)])
