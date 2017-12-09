from base_tests import BaseTest


class TestCTEs(BaseTest):
    def __init__(self, *args, **kwargs):
        super(TestCTEs, self).__init__(*args, **kwargs)

    def test_simple(self):
        self.run_test('tests/resources/cte_statements/simple.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','','foo','','','WITH',1),
             ('foo','mytable','mytable','','','SELECT',2),
             ('ROOT','other_table','other_table','','','INSERT',1),
             ('ROOT','foo','foo','','','SELECT',1)])

    def test_subselects_in_with(self):
        self.run_test('tests/resources/cte_statements/subselects_in_with.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','','foo','','','WITH',1),
             ('foo','','','','','SELECT',2),
             ('','mytable','mytable','bar','','SELECT',3),
             ('ROOT','other_table','other_table','','','INSERT',1),
             ('ROOT','foo','foo','','','SELECT',1)])

    def test_with_rank_partition(self):
        self.run_test('tests/resources/cte_statements/with_ranked_partition.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','','ranked','','','WITH',1),
             ('ranked','foo','foo','','','SELECT',2),
             ('ROOT','ranked','ranked','','','SELECT',1)])