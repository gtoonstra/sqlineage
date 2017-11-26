import unittest
import sqlineage


class TestSimpleSelect(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSimpleSelect, self).__init__(*args, **kwargs)
        self.result = []

    def callback(self, parent, table, alias, operation, level):
        self.result.append((parent, table, alias, operation, level))

    def clear_result(self):
        self.result = []

    def verify_result(self, expected):
        self.assertEqual(self.result, expected)

    def run_test(self, filename, expected):
        self.clear_result()
        with open(filename, 'r') as infile:
            sql = infile.read()
            sqlineage.parse(sql, self.callback)
        self.verify_result(expected)        

    def test_simple(self):
        self.run_test('tests/resources/simple_select/simple.sql', 
            [('ROOT','ROOT','','NONE',0),
             ('ROOT','foo','','SELECT',1)])

    def test_simple_mixed_case(self):
        self.run_test('tests/resources/simple_select/simple_mixed_case.sql', 
            [('ROOT','ROOT','','NONE',0),
             ('ROOT','foo','','SELECT',1)])

    def test_simple_newline(self):
        self.run_test('tests/resources/simple_select/simple_with_newline.sql', 
            [('ROOT','ROOT','','NONE',0),
             ('ROOT','foo','','SELECT',1)])

    def test_simple_semicolon(self):
        self.run_test('tests/resources/simple_select/simple_with_semicolon.sql', 
            [('ROOT','ROOT','','NONE',0),
             ('ROOT','foo','','SELECT',1)])

    def test_simple_spacing(self):
        self.run_test('tests/resources/simple_select/simple_with_spacing.sql', 
            [('ROOT','ROOT','','NONE',0),
             ('ROOT','foo','','SELECT',1)])

if __name__ == '__main__':
    unittest.main()
