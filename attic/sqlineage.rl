
/*
 * Parse SQL statements and return events based on what's seen.
 */

#include <stdio.h>
#include <string.h>
#include <Python.h>

/**
 * Main definitions
 */

#define BUFLEN 1024
#define BUFSIZE 2048
#define ERROR_LEN   63

static PyObject *SqlineageError;
static PyObject *callback = NULL;

struct context
{
    char buffer[BUFLEN+1];
    int buflen;
    int cs;
    int line_counter;
    char *line_pos;
    char error[ERROR_LEN+1];
};

/**
 * Machine definitions
 */

%%{
    machine params;
    access fsm->;

    # A buffer to collect argurments

    # Append to the buffer.
    action append {
        // printf("append\n");
        if ( fsm->buflen < BUFLEN )
            fsm->buffer[fsm->buflen++] = fc;
    }

    # Terminate a buffer.
    action term {
        // printf("term\n");
        if ( fsm->buflen < BUFLEN )
            fsm->buffer[fsm->buflen++] = 0;
    }

    # Clear out the buffer
    action clear { 
        // printf("clear\n");
        fsm->buflen = 0; 
    }
    action newline { 
        if (p[0] == '\n') {
            ++fsm->line_counter; 
            fsm->line_pos = (char *)p; 
        }
    }

    action select { 
        printf("select\n"); 
    }
    action insert { 
        printf("insert\n"); 
    }
    action with { 
        printf("with: \"%s\"\n", fsm->buffer); 
    }
    action into { 
        printf("into\n");
    }
    action values {
        printf("values\n");
    }
    action sqlfrom { 
        // printf("from\n"); 
    }
    action identifier { 
        printf("identifier: \"%s\"\n", fsm->buffer); 
    }
    action tablename { 
        printf("tablename: \"%s\"\n", fsm->buffer); 
    }
    action nested { 
        printf("nested: \n"); fgoto main; 
    }

    action errorhandler { 
        char buf[16] = {"\0"};
        int column = p - fsm->line_pos + 1;
        strncpy(buf, p, 15);
        sprintf(fsm->error, "Error processing SQL at line %d, column %d near '%s'", fsm->line_counter, column, buf);
    }

    # Helpers that collect strings
    string = [^\0]+ >clear $append %term;

    # Different arguments.
    ws = [\t \n] @newline;
    select = ('select'i ws) @select ws*;
    insert = ('insert'i ws) @insert ws*;
    with = ('with'i ws) @with ws*;
    into = ('into'i) @into ws*;
    values = ('values'i) @values;
    sqlfrom = ('from'i ws) @sqlfrom ws*;
    identifier = '\''? ([a-zA-Z] >clear $append [a-z0-9A-Z]* $append) %term %identifier '\''?;
    tablename = ([a-zA-Z] >clear $append [a-z0-9A-Z]* $append) %term %tablename;

    main := ( ws*
        ((select identifier ws+ sqlfrom tablename | select identifier ws+ sqlfrom '(' @nested) |
        (insert into tablename ws* '(' ws* identifier ws* ')' ws* values ws* '(' ws* identifier ws* ')' ) | 
        with ))* ws* ';'? ws* 0 $err(errorhandler);
}%%

%% write data;

/**
 * Start of parser generation
 */

void parser_init( struct context *fsm )
{
    fsm->buflen = 0;
    fsm->cs = 0;
    fsm->line_counter = 0;
    memset(fsm->error, 0x00, ERROR_LEN+1);

    %% write init;
}

void parser_execute( struct context *fsm, const char *data, int len )
{
    const char *p = data;
    const char *pe = data + len;
    const char *eof = NULL;

    fsm->line_pos = (char *)p;

    %% write exec;
}

int parser_finish( struct context *fsm )
{
    if ( fsm->cs == params_error )
        return -1;
    if ( fsm->cs >= params_first_final )
        return 1;
    return 0;
}

static PyObject *
sqlineage_parse(PyObject *self, PyObject *args)
{
    const char *sql;
    PyObject *temp;
    PyObject *result = NULL;
    struct context context;

    if (!PyArg_ParseTuple(args, "sO:set_callback", &sql, &temp))
        return NULL;

    if (!PyCallable_Check(temp)) {
        PyErr_SetString(PyExc_TypeError, "Callback parameter must be callable");
        return NULL;
    }
    Py_XINCREF(temp);         /* Add a reference to new callback */
    Py_XDECREF(callback);  /* Dispose of previous callback */
    callback = temp;       /* Remember new callback */
    
    parser_init( &context );
    parser_execute( &context, sql, strlen(sql)+1 );
    if ( parser_finish( &context ) != 1 ) {
        if (strlen(context.error) > 0) {
            PyErr_SetString(SqlineageError, context.error);
        } else {
            PyErr_SetString(SqlineageError, "Error processing SQL file");
        }
        return NULL;
    }

    /* Boilerplate to return "None" */
    Py_INCREF(Py_None);
    result = Py_None;
    return result;
}

static PyMethodDef SqlineageMethods[] = {
    {"parse",  sqlineage_parse, METH_VARARGS, "Parse an SQL file"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef sqlineageModule =
{
    PyModuleDef_HEAD_INIT,
    "sqlineage", /* name of module */
    "",          /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    SqlineageMethods
};

PyMODINIT_FUNC PyInit_sqlineage(void)
{
    PyObject *m;

    m = PyModule_Create(&sqlineageModule);
    if (m == NULL)
        return NULL;

    SqlineageError = PyErr_NewException("sqlineage.error", NULL, NULL);
    Py_INCREF(SqlineageError);
    PyModule_AddObject(m, "error", SqlineageError);
    return m;
}
