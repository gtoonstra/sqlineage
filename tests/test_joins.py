import unittest
import sqlineage


class TestJoins(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestJoins, self).__init__(*args, **kwargs)
        self.result = []

    def callback(self, parent, table, alias, query_alias, operation, level):
        self.result.append((parent, table, alias, query_alias, operation, level))

    def clear_result(self):
        self.result = []

    def verify_result(self, expected):
        print(self.result)
        self.assertEqual(expected, self.result)

    def run_test(self, filename, expected):
        self.clear_result()
        with open(filename, 'r') as infile:
            sql = infile.read()
            sqlineage.scan(sql, self.callback)
        self.verify_result(expected)

    def test_innerjoin(self):
        self.run_test('tests/resources/joins/innerjoin.sql', 
            [('ROOT','ROOT','ROOT','','NONE',0),
             ('ROOT','foo','foo','','INSERT',1),
             ('ROOT','zxc','a','','SELECT',1)])

    def test_innerjoin_with_union(self):
        self.run_test('tests/resources/joins/innerjoin_with_union.sql',
            [('ROOT','ROOT','ROOT','','NONE',0),
             ('ROOT','foo','foo','','INSERT',1),
             ('ROOT','zxc','a','','SELECT',1),
             ('ROOT','def','c','','SELECT',1)])

    def test_join_with_select_in_join(self):
        self.run_test('tests/resources/joins/join_with_select_in_join.sql',
            [('ROOT', 'ROOT', 'ROOT','','NONE', 0), 
             ('ROOT', 'foo', 'foo', '','INSERT', 1), 
             ('ROOT', 'zxc', 'a', '','SELECT', 1), 
             ('a', 'ghi', 'f', 'c','SELECT', 2), 
             ('ROOT', 'def', 'q', '','SELECT', 1), 
             ('q', 'ghi', 'f', 'e','SELECT', 2)])
