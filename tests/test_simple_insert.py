from base_tests import BaseTest


class TestSimpleInsert(BaseTest):
    def __init__(self, *args, **kwargs):
        super(TestSimpleInsert, self).__init__(*args, **kwargs)

    def test_simple(self):
        self.run_test('tests/resources/simple_insert/simple.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1)])

    def test_simple_mixed_case(self):
        self.run_test('tests/resources/simple_insert/simple_mixed_case.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1)])

    def test_simple_newline(self):
        self.run_test('tests/resources/simple_insert/simple_with_newline.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1)])

    def test_simple_semicolon(self):
        self.run_test('tests/resources/simple_insert/simple_with_semicolon.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1)])

    def test_simple_spacing(self):
        self.run_test('tests/resources/simple_insert/simple_with_spacing.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1)])

    def test_long_insert(self):
        self.run_test('tests/resources/simple_insert/long_insert.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','myreallylongtablename','myreallylongtablename','','','INSERT',1)])

if __name__ == '__main__':
    unittest.main()
