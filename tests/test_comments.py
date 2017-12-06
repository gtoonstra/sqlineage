from base_tests import BaseTest


class TestComments(BaseTest):
    def __init__(self, *args, **kwargs):
        super(TestComments, self).__init__(*args, **kwargs)

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
