import unittest
import sqlineage


class TestSimpleInsert(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSimpleInsert, self).__init__(*args, **kwargs)
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

    def test_simple(self):
        self.run_test('tests/resources/simple_insert/simple.sql', 
            [('ROOT','ROOT','ROOT','','NONE',0),
             ('ROOT','foo','foo','','INSERT',1)])

    def test_simple_mixed_case(self):
        self.run_test('tests/resources/simple_insert/simple_mixed_case.sql', 
            [('ROOT','ROOT','ROOT','','NONE',0),
             ('ROOT','foo','foo','','INSERT',1)])

    def test_simple_newline(self):
        self.run_test('tests/resources/simple_insert/simple_with_newline.sql', 
            [('ROOT','ROOT','ROOT','','NONE',0),
             ('ROOT','foo','foo','','INSERT',1)])

    def test_simple_semicolon(self):
        self.run_test('tests/resources/simple_insert/simple_with_semicolon.sql', 
            [('ROOT','ROOT','ROOT','','NONE',0),
             ('ROOT','foo','foo','','INSERT',1)])

    def test_simple_spacing(self):
        self.run_test('tests/resources/simple_insert/simple_with_spacing.sql', 
            [('ROOT','ROOT','ROOT','','NONE',0),
             ('ROOT','foo','foo','','INSERT',1)])

    def test_long_insert(self):
        self.run_test('tests/resources/simple_insert/long_insert.sql', 
            [('ROOT','ROOT','ROOT','','NONE',0),
             ('ROOT','myreallylongtablename','myreallylongtablename','','INSERT',1)])

if __name__ == '__main__':
    unittest.main()
