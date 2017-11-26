import unittest
import sqlineage


class TestComplex(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestComplex, self).__init__(*args, **kwargs)
        self.result = []

    def callback(self, parent, table, alias, operation, level):
        self.result.append((parent, table, alias, operation, level))

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

    def test_complex(self):
        self.run_test('tests/resources/complex/complex.sql', 
            [('ROOT','ROOT','ROOT','NONE',0),
             ('ROOT', '', 'somedata', 'WITH', 1),
             ('somedata', '', 'foo', 'SELECT', 2),
             ('foo', 'database.schema.table', 'bar', 'SELECT', 3),
             ('ROOT', 'destination_table', 'destination_table', 'INSERT', 1),
             ('ROOT', '', 'def', 'SELECT', 1),
             ('def', 'database.schema.table1', 'C', 'SELECT', 2),
             ('def', 'flat_table', 'f', 'SELECT', 2)])

    def test_complex_without_insert(self):
        self.run_test('tests/resources/complex/complex_without_insert.sql', 
            [('ROOT','ROOT','ROOT','NONE',0),
             ('ROOT', '', 'somedata', 'WITH', 1),
             ('somedata', '', 'foo', 'SELECT', 2),
             ('foo', 'database.schema.table', 'bar', 'SELECT', 3),
             ('ROOT', '', 'def', 'SELECT', 1),
             ('def', 'database.schema.table1', 'C', 'SELECT', 2),
             ('def', 'flat_table', 'f', 'SELECT', 2)])

    def test_huge_query(self):
        self.run_test('tests/resources/complex/reuse_alias_and_literals.sql', 
            [('ROOT', 'ROOT', 'ROOT', 'NONE', 0), 
             ('ROOT', 'foo', 'foo', 'INSERT', 1), 
             ('ROOT', '', 'qwetuvtype', 'SELECT', 1), 
             ('qwetuvtype', 'database.schema.app_abc', 'pgru', 'SELECT', 2), 
             ('ROOT', '', 'brands', 'SELECT', 1), 
             ('brands', 'database.schema.app_abc', 'pgru', 'SELECT', 2), 
             ('ROOT', '', 'brands', 'SELECT', 1), 
             ('brands', 'database.schema.app_abc', 'pgru', 'SELECT', 2), 
             ('ROOT', '', 'fghs', 'SELECT', 1), 
             ('fghs', 'database.schema.app_abc', 'fgh2', 'SELECT', 2), 
             ('fgh2', 'database.schema.app_fgh', 'tt', 'SELECT', 3), 
             ('tt', 'database.schema.app_fgh', 't', 'SELECT', 4)])
