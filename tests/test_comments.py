import unittest
import sqlineage


class TestComments(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestComments, self).__init__(*args, **kwargs)
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

    def test_block_comments(self):
        self.run_test('tests/resources/comments/block_comments.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','subselects','subselects','','','INSERT',1),
             ('ROOT','','','','','SELECT',1),
             ('','foo.bar.tablename','b','foo','','SELECT',2),
             ('','abc.dbo.xyz','c','foo','','SELECT',2),
             ('','abc.def.xyz','d','foo','','SELECT',2)])

    def test_very_long_comment(self):
        self.run_test('tests/resources/comments/very_long_comment.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1)])

    def test_very_long_block_comment(self):
        self.run_test('tests/resources/comments/very_long_block_comment.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1)])
