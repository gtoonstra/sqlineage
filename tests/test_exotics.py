from base_tests import BaseTest


class TestExotics(BaseTest):
    def __init__(self, *args, **kwargs):
        super(TestExotics, self).__init__(*args, **kwargs)

    def test_nolock_statements(self):
        self.run_test('tests/resources/exotics/nolock_statements.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','subselects','subselects','','','INSERT',1),
             ('ROOT','','','','','SELECT',1),
             ('','foo.bar.tablename','b','foo','','SELECT',2),
             ('','abc.dbo.xyz','c','foo','','SELECT',2),
             ('','abc.def.xyz','d','foo','','SELECT',2)])

    def test_brackets(self):
        self.run_test('tests/resources/exotics/brackets.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1),
             ('ROOT','[server].[database].[schema].[table]','[server].[database].[schema].[table]','','','SELECT',1)])

    def test_backtick(self):
        self.run_test('tests/resources/exotics/backtick.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1),
             ('ROOT',
                '`database.schema with a space.table with something else`',
                '`database.schema with a space.table with something else`',
                '',
                '',
                'SELECT',1)])

    def test_select_join_for_field(self):
        self.run_test('tests/resources/exotics/select_join_for_field.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1),
             ('ROOT','db.schema.asd','a','','db.schema.pow|pow,db.schema.jkl|j','SELECT',1)])

    def test_mixed_brackets_and_regular(self):
        self.run_test('tests/resources/exotics/mixed_brackets_and_regular.sql', 
            [('ROOT','ROOT','ROOT','','','NONE',0),
             ('ROOT','foo','foo','','','INSERT',1),
             ('ROOT','[servername].db.schema.foo','[servername].db.schema.foo','','','SELECT',1)])