from base_tests import BaseTest


class TestSimpleSelect(BaseTest):
    def __init__(self, *args, **kwargs):
        super(TestSimpleSelect, self).__init__(*args, **kwargs)

    def test_simple(self):
        self.run_test('tests/resources/simple_select/simple.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','SELECT',1)])

    def test_simple_mixed_case(self):
        self.run_test('tests/resources/simple_select/simple_mixed_case.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','SELECT',1)])

    def test_simple_newline(self):
        self.run_test('tests/resources/simple_select/simple_with_newline.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','SELECT',1)])

    def test_simple_semicolon(self):
        self.run_test('tests/resources/simple_select/simple_with_semicolon.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','SELECT',1)])

    def test_simple_spacing(self):
        self.run_test('tests/resources/simple_select/simple_with_spacing.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','SELECT',1)])

    def test_simple_with_where(self):
        self.run_test('tests/resources/simple_select/simple_with_where.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','some_table','some_table','','','SELECT',1)])


if __name__ == '__main__':
    unittest.main()
