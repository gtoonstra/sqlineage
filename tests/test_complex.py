from base_tests import BaseTest


class TestComplex(BaseTest):
    def __init__(self, *args, **kwargs):
        super(TestComplex, self).__init__(*args, **kwargs)

    def test_complex(self):
        self.run_test('tests/resources/complex/complex.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT', '', 'somedata', '','','WITH', 1),
             ('somedata', '', '', '','','SELECT', 2),
             ('', 'database.schema.table', 'bar', 'foo','database.schema.other_table|REF','SELECT', 3),
             ('ROOT', 'destination_table', 'destination_table', '','','INSERT', 1),
             ('ROOT', '', '', '','','SELECT', 1),
             ('', 'database.schema.table1', 'C', 'def','database.schema.pcur_table|Cu,database.schema.pcount_table|Co,database.schema.pac|pac,somedata|sd,database.schema.pcam|pm','SELECT', 2),
             ('', 'flat_table', 'f', 'def','','SELECT', 2)])

    def test_complex_without_insert(self):
        self.run_test('tests/resources/complex/complex_without_insert.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT', '', 'somedata', '','','WITH', 1),
             ('somedata', '', '', '','','SELECT', 2),
             ('', 'database.schema.table', 'bar', 'foo','database.schema.other_table|REF','SELECT', 3),
             ('ROOT', '', '', '','','SELECT', 1),
             ('', 'database.schema.table1', 'C', 'def','database.schema.pcur_table|Cu,database.schema.pcount_table|Co,database.schema.pac|pac,somedata|sd,database.schema.pcam|pm','SELECT', 2),
             ('', 'flat_table', 'f', 'def','','SELECT', 2)])

    def test_huge_query(self):
        self.run_test('tests/resources/complex/reuse_alias_and_literals.sql', 
            [('ROOT', 'ROOT', 'ROOT', '','','NONE', 0), 
             ('ROOT', 'foo', 'foo', '', '','INSERT', 1), 
             ('ROOT', '', '', '', 'database.schema.app_qwe|u','SELECT', 1), 
             ('', 'database.schema.app_abc', 'pgru', 'qwetuvtype', 'database.schema.app_xyz|pg,database.schema.app_def|pgp,database.schema.app_tuv|pp','SELECT', 2), 
             ('ROOT', '', '', '', 'database.schema.app_tuv|pb,database.schema.app_qwe|u','SELECT', 1), 
             ('', 'database.schema.app_abc', 'pgru', 'brands', 'database.schema.app_xyz|pg,database.schema.app_def|pgp,database.schema.app_tuv|pp','SELECT', 2), 
             ('ROOT', '', '', '', 'database.schema.app_tuv|pb,database.schema.app_qwe|u','SELECT', 1), 
             ('', 'database.schema.app_abc', 'pgru', 'brands', 'database.schema.app_xyz|pg,database.schema.app_def|pgp,database.schema.app_tuv|pp','SELECT', 2), 
             ('ROOT', '', '', '', 'database.schema.app_xyz|pg,database.schema.app_def|pgp,database.schema.app_tuv|pp,database.schema.app_qwe|u','SELECT', 1), 
             ('', 'database.schema.app_abc', 'pgru', 'fghs', 'database.schema.app_xyz|pg','SELECT', 2), 
             ('pgru', 'database.schema.app_fgh', 't', 'fgh2', '','SELECT', 3), 
             ('t', 'database.schema.app_fgha', 't', 'tt', '','SELECT', 4)])

    def test_select_if_multiple_with_insert_select(self):
        self.run_test('tests/resources/complex/select_if_multiple_with_insert_select.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT', 'db.s.foo', 'db.s.foo', '', '','SELECT', 1),
             ('ROOT', '', 'afoo', '', '','WITH', 1),
             ('afoo', 'db.schema.bar', 'bar', '', '','SELECT', 2),
             ('ROOT', '', 'bfoo', '', '','WITH', 1),
             ('bfoo', 'db.schema.bas', 'bas', '', '','SELECT', 2),
             ('ROOT','db2.foo.zxc','db2.foo.zxc','','','INSERT',1),
             ('ROOT', 'db.schema.foo', 'foo', '', 'afoo|,bfoo|','SELECT', 1)])
