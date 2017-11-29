/*
 * A mini C-like language scanner.
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <Python.h>

#include "state_machine.h"

#define MIN(a,b) ((a) < (b) ? a : b)

static PyObject *SqlineageError;
static PyObject *callback = NULL;

%%{
    machine clang;

    newline = '\n' @{curline += 1;};
    any_count_line = any | newline;

    # Consume a C comment.
    block_comment := any_count_line* :>> '*/' @{fgoto main;};
    line_comment := [^\n]* :>> '\n' @{fgoto main;};

    main := |*

    # Alpha numberic characters or underscore.
    alnum_u = alnum | '_' | '\.' | '[' | ']';

    # Alpha charactres or underscore.
    alpha_u = alpha | '_' | '[' | ']';

    # Symbols. Upon entering clear the buffer. On all transitions
    # buffer a character. Upon leaving dump the symbol.
    ( punct - [_'"\.\[\]] ) {
        // printf( "symbol(%i): %c\n", curline, ts[0] );
        push_symbol(ts[0]);
    };

    # Identifier. Upon entering clear the buffer. On all transitions
    # buffer a character. Upon leaving, dump the identifier.
    alpha_u alnum_u* {
        memset(arg, 0x00, BUFSIZE);
        strncpy(arg, ts, te-ts);

/*
        printf( "ident(%i): ", curline );
        fwrite(arg, 1, strlen(arg), stdout);
        printf("\n");
*/
        push_ident(arg);
    };

    # Single Quote.
    sliteralChar = [^'];
    '\'' . sliteralChar* . '\'' {
/*
        printf( "single_lit(%i): ", curline );
        fwrite( ts, 1, te-ts, stdout );
        printf("\n");
*/
    };

    # Double Quote.
    dliteralChar = [^"\\];
    '"' . dliteralChar* . '"' {
/*
        printf( "double_lit(%i): ", curline );
        fwrite( ts, 1, te-ts, stdout );
        printf("\n");
*/
    };

    # back tick literal.
    dBackTickLiteral = [^`\\] | newline | ( '\\' any_count_line );
    '`' . dBackTickLiteral* . '`' {
        memset(arg, 0x00, BUFSIZE);
        strncpy(arg, ts, te-ts);    
/*
        printf( "backtick(%i): ", curline );
        fwrite(arg, 1, strlen(arg), stdout);
        printf("\n");
*/
        push_backtick_literal(arg);
    };

    # Whitespace is standard ws, newlines and control codes.
    any_count_line - 0x21..0x7e;

    # Describe both c style comments and c++ style comments. The
    # priority bump on the terminator of the comments brings us
    # out of the extend* which matches everything.
    '//' [^\n]* newline;
    '--' { fgoto line_comment; };
    '/*' { fgoto block_comment; };

    # Match an integer. We don't bother clearing the buf or filling it.
    # The float machine overlaps with int and it will do it.
    digit+ {
/*
        printf( "int(%i): ", curline );
        fwrite( ts, 1, te-ts, stdout );
        printf("\n");
*/
    };

    # Match a float. Upon entering the machine clear the buf, buffer
    # characters on every trans and dump the float upon leaving.
    digit+ '.' digit+ {
/*
        printf( "float(%i): ", curline );
        fwrite( ts, 1, te-ts, stdout );
        printf("\n");
*/
    };

    # Match a hex. Upon entering the hex part, clear the buf, buffer characters
    # on every trans and dump the hex on leaving transitions.
    '0x' xdigit+ {
/*
        printf( "hex(%i): ", curline );
        fwrite( ts, 1, te-ts, stdout );
        printf("\n");
*/
    };

    *|;
}%%

%% write data nofinal;

#define BUFSIZE 128


int scanner(const char *sql)
{
    static char buf[BUFSIZE+1];
    int cs, act, have = 0, curline = 1;
    char *ts, *te = 0;
    int done = 0;
    int pointer = 0;
    int sqllen = strlen(sql);

    char arg[BUFSIZE+1] = {"\0"};

    initialize_fsm();

    %% write init;

    while ( !done ) {
        char *p = buf + have, *pe, *eof = 0;
        int len, space = BUFSIZE - have;
        
        if ( space == 0 ) {
            // We've used up the entire buffer storing an already-parsed token
            // prefix that must be preserved.
            printf("Out of buffer space!\n");
            PyErr_SetString(SqlineageError, "Out of buffer space.");
            return -1;
        }

        space = MIN(space, sqllen-pointer);
        strncpy(p, &sql[pointer], space);
        p[space] = '\0';
        // printf("\n\n%s\n", p);
        len = strlen(p);
        pointer += len;
        pe = p + len;

        // Check if this is the end of file.
        if ( pointer >= sqllen ) {
            eof = pe;
            done = 1;
        }

        %% write exec;

        if ( cs == clang_error ) {
            printf("Error when parsing\n");
            PyErr_SetString(SqlineageError, "Error when parsing.");
            return -1;
        }

        if ( ts == 0 )
            have = 0;
        else {
            // There is a prefix to preserve, shift it over.
            have = pe - ts;
            memmove( buf, ts, have );
            te = buf + (te-ts);
            ts = buf;
        }
    }
    return 0;
}


static PyObject *
sqlineage_scan(PyObject *self, PyObject *args)
{
    const char *sql;
    PyObject *temp;
    PyObject *result = NULL;

    if (!PyArg_ParseTuple(args, "sO:set_callback", &sql, &temp))
        return NULL;

    if (!PyCallable_Check(temp)) {
        PyErr_SetString(PyExc_TypeError, "Callback parameter must be callable");
        return NULL;
    }
    Py_XINCREF(temp);      /* Add a reference to new callback */
    Py_XDECREF(callback);  /* Dispose of previous callback */
    callback = temp;       /* Remember new callback */

    if (scanner(sql) != 0) {
        return NULL;
    }

    send_model(callback);

    memory_cleanup();

    /* Boilerplate to return "None" */
    Py_INCREF(Py_None);
    result = Py_None;
    return result;
}

static PyMethodDef SqlineageMethods[] = {
    {"scan",  sqlineage_scan, METH_VARARGS, "Scan an SQL file"},
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
