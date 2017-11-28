import unittest
import sqlineage


class TestCTEs(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCTEs, self).__init__(*args, **kwargs)
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
        self.run_test('tests/resources/cte_statements/simple.sql', 
            [('ROOT','ROOT','ROOT','','NONE',0),
             ('ROOT','','foo','','WITH',1),
             ('foo','mytable','mytable','','SELECT',2),
             ('ROOT','other_table','other_table','','INSERT',1),
             ('ROOT','foo','foo','','SELECT',1)])

    def test_subselects_in_with(self):
        self.run_test('tests/resources/cte_statements/subselects_in_with.sql', 
            [('ROOT','ROOT','ROOT','','NONE',0),
             ('ROOT','','foo','','WITH',1),
             ('foo','','','','SELECT',2),
             ('','mytable','mytable','bar','SELECT',3),
             ('ROOT','other_table','other_table','','INSERT',1),
             ('ROOT','foo','foo','','SELECT',1)])
