from base_tests import BaseTest


class TestSimpleMulti(BaseTest):
    def __init__(self, *args, **kwargs):
        super(TestSimpleMulti, self).__init__(*args, **kwargs)

    def test_simple(self):
        self.run_test('tests/resources/simple_multi/simple.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1),
             ('ROOT','bar','bar','','','SELECT',1)])

    def test_simple_mixed_case(self):
        self.run_test('tests/resources/simple_multi/simple_mixed_case.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1),
             ('ROOT','bar','bar','','','SELECT',1)])

    def test_simple_newline(self):
        self.run_test('tests/resources/simple_multi/simple_with_newline.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1),
             ('ROOT','bar','bar','','','SELECT',1)])

    def test_simple_semicolon(self):
        self.run_test('tests/resources/simple_multi/simple_with_semicolon.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1),
             ('ROOT','bar','bar','','','SELECT',1)])

    def test_simple_spacing(self):
        self.run_test('tests/resources/simple_multi/simple_with_spacing.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1),
             ('ROOT','bar','bar','','','SELECT',1)])

    def test_select_without_alias(self):
        self.run_test('tests/resources/simple_multi/insert_select_without_alias.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1),
             ('ROOT','','','','database.schema.app_xyz|abc,database.schema.app_zxc|def','SELECT',1),
             ('','database.schema.app_xyz','s','cxz','','SELECT',2)])


if __name__ == '__main__':
    unittest.main()
