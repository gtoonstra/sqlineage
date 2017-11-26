import unittest
import sqlineage


class TestComments(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestComments, self).__init__(*args, **kwargs)
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
            sqlineage.scan(sql, self.callback)
        self.verify_result(expected)

    def test_block_comments(self):
        self.run_test('tests/resources/comments/block_comments.sql', 
            [('ROOT','ROOT','ROOT','NONE',0),
             ('ROOT','subselects','subselects','INSERT',1),
             ('ROOT','','foo','SELECT',1),
             ('foo','foo.bar.tablename','b','SELECT',2),
             ('foo','abc.dbo.xyz','c','SELECT',2),
             ('foo','abc.def.xyz','d','SELECT',2)])
