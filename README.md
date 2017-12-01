# sqlineage

This is an extension module generated with ragel, which serves to scan SQL files
and extract SELECT, INSERT, CTE operations out of the file. It only extracts the table
names for now, which can be used to establish data lineage models at table level.

It probably only works on Ubuntu right now because of the way the code is compiled.

### Installation

1. Install ragel: `sudo apt-get install ragel`
2. Create a virtual environment venv for python3: `python3 -m venv venv`
3. Source the environment: `source venv/bin/activate`
4. Install pip, pip-tools, setuptools and wheel:

```
pip install pip --upgrade
pip install setuptools --upgrade
pip install pip-tools --upgrade
pip install wheel --upgrade
pip install pytest --upgrade
```

5. Execute "compile.sh": `./compile.sh`
6. Compile and install the module in your virtual environment: `python3 setup.py install`

### Testing

1. Source the environment created before: `source venv/bin/activate`
2. Run pytest: `pytest`

### API and usage

```python
import sqlineage


def callback(parent, table, alias, query_alias, operation, level):
    print(parent, table, alias, query_alias, operation, level)

sqlineage.scan('SELECT * FROM foo', callback)
```

The scanner calls the callback for each SQL 'block' that it finds. Subselects are supported.
What it does is help you build a hierarchical model of the SQL using only the table names.
This can be a first step towards building a converter that scans directories of SQL files and
outputs a file that shows how tables depend on one another. This can then be used to feed a 
Graph database that records those dependencies. This graph database is then further useful for
querying and creating visualizations of these relationships.

There are thus only five elements you get back:
- parent: The parent of the current block being output
- table:  The table name that is selected from or inserted into (not always available)
- alias:  The alias to refer to a subselect or CTE
- query_alias: A reference to a query block
- operation: The operation taking place in that SQL block
- level:  The hierarchical level where the code was found, useful for subselects.

### Example

A simple SQL file that looks like this:

```sql
INSERT INTO subselects( a )

SELECT
    foo.a
  FROM (
       SELECT DISTINCT
           b.a
         FROM foo.bar.tablename b WITH (nolock)
         WHERE b.a IS NOT NULL
       UNION
       SELECT DISTINCT
           c.a
         FROM abc.dbo.xyz c WITH (nolock) 

       UNION
       SELECT DISTINCT
           d.a
         FROM abc.def.xyz d WITH (nolock) 
         WHERE DATEPART (weekday, GETDATE ()) = 1) foo;
```

will be output as this:

```
'ROOT', 'ROOT', 'ROOT', 'NONE', 0
    'ROOT', 'subselects', 'subselects', 'INSERT', 1
    'ROOT', '', 'foo', 'SELECT', 1
        'foo', 'foo.bar.tablename', 'b', 'SELECT', 2
        'foo', 'abc.dbo.xyz', 'c', 'SELECT', 2
        'foo', 'abc.def.xyz', 'd', 'SELECT', 2
```
