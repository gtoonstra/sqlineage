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