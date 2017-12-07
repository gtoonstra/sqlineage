from base_tests import BaseTest


class TestSpecialKeywords(BaseTest):
    def __init__(self, *args, **kwargs):
        super(TestSpecialKeywords, self).__init__(*args, **kwargs)

    def test_groupby_no_where(self):
        self.run_test('tests/resources/special_keywords/groupby_no_where.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1),
             ('ROOT','db.schema.foo','db.schema.foo','','','SELECT',1)])

    def test_groupby_having(self):
        self.run_test('tests/resources/special_keywords/groupby_having.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1),
             ('ROOT','db.schema.foo','db.schema.foo','','','SELECT',1)])

    def test_orderby_no_where(self):
        self.run_test('tests/resources/special_keywords/orderby_no_where.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1),
             ('ROOT','db.schema.foo','db.schema.foo','','','SELECT',1)])
