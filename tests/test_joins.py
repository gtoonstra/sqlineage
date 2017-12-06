from base_tests import BaseTest


class TestJoins(BaseTest):
    def __init__(self, *args, **kwargs):
        super(TestJoins, self).__init__(*args, **kwargs)

    def test_innerjoin(self):
        self.run_test('tests/resources/joins/innerjoin.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1),
             ('ROOT','zxc','a','','bar|b','SELECT',1)])

    def test_innerjoin_with_union(self):
        self.run_test('tests/resources/joins/innerjoin_with_union.sql',
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1),
             ('ROOT','zxc','a','','bar|b','SELECT',1),
             ('ROOT','def','c','','xyz|d','SELECT',1)])

    def test_join_with_select_in_join(self):
        self.run_test('tests/resources/joins/join_with_select_in_join.sql',
            [('ROOT', 'ROOT', 'ROOT','','','NONE', 0), 
             ('ROOT', 'foo', 'foo', '','','INSERT', 1), 
             ('ROOT', 'zxc', 'a', '','bar|b','SELECT', 1), 
             ('a', 'ghi', 'f', 'c','','SELECT', 2), 
             ('ROOT', 'def', 'q', '','xyz|d','SELECT', 1), 
             ('q', 'ghi', 'f', 'e','','SELECT', 2)])
