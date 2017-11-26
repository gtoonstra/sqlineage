import unittest
import sqlineage


class TestCTEs(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCTEs, self).__init__(*args, **kwargs)
        self.result = []

    def callback(self, parent, table, alias, operation, level):
        self.result.append((parent, table, alias, operation, level))

    def clear_result(self):
        self.result = []

    def verify_result(self, expected):
        print(self.result)
        self.assertEqual(self.result, expected)

    def run_test(self, filename, expected):
        self.clear_result()
        with open(filename, 'r') as infile:
            sql = infile.read()
            sqlineage.parse(sql, self.callback)
        self.verify_result(expected)

    def test_simple(self):
        self.run_test('tests/resources/cte_statements/simple.sql', 
            [('ROOT','ROOT','','NONE',0),
             ('ROOT','','foo','WITH',1),
             ('','mytable','mytable','SELECT',2),
             ('ROOT','other_table','other_table','INSERT',1),
             ('ROOT','foo','foo','SELECT',1)])
