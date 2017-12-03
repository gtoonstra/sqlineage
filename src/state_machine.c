#include <stdio.h>
#include <string.h>
#include "state_machine.h"


#define BUFLEN      128


typedef enum {NONE, INSERT, SELECT, WITH, UNION} operation_t;
typedef enum {NEXT_IS_FIELD, NEXT_IS_QUERY_ALIAS_CHILD, NEXT_IS_TABLENAME, NEXT_IS_ALIAS, NEXT_COMPLETE, NEXT_SCOPE_ENDED} next_t;
typedef enum {SELECT_PART, FROM_PART, WHERE_PART} sqlpart_t;

struct fsm {
    char table[BUFLEN+1];
    char alias[BUFLEN+1];
    char query_alias[BUFLEN+1];
    operation_t op;
    next_t next;
    int level;
    int scope_ctr;
    struct fsm *sibling;
    struct fsm *child;
    struct fsm *parent;
    sqlpart_t sqlpart;
} fsm_t;

struct fsm root;
struct fsm *current;


void initialize_fsm() {
    memset(&root, 0x00, sizeof(struct fsm));
    current = &root;
    root.op = NONE;
    strcpy(root.table, "ROOT");
    strcpy(root.alias, "ROOT");
    root.parent = &root;
    root.sqlpart = SELECT_PART;
}

void push_ident(const char *ident) {
    if (current == NULL) {
        printf("CURRENT IS NULL!\n");
        return;
    }

    // printf("%s\n", ident);

    if (strcasecmp(ident, "insert") == 0 ) {
        // printf("%s:%s\n", current->alias, current->query_alias);
        switch( current->op ) {
            case NONE:
                root.child = (struct fsm *)calloc(1, sizeof(struct fsm));
                current = root.child;
                current->parent = &root;
                current->level = 1;
                current->scope_ctr = current->level;
                current->op = INSERT;
                // printf("INSERT\n");
                break;
            default:
                // printf("INSERT after other statements\n");
                current->sibling = (struct fsm *)calloc(1, sizeof(struct fsm));
                current->sibling->parent = current->parent;
                current = current->sibling;
                current->level = current->parent->level + 1;
                current->scope_ctr = current->level;
                current->op = INSERT;
                break;
        }
        return;
    }
    if (strcasecmp(ident, "into") == 0 ) {
        if (current->op != INSERT) {
            printf("Unexpected keyword\n");
        }
        current->next = NEXT_IS_TABLENAME;
        // printf("INTO\n");
        return;
    }
    if (strcasecmp(ident, "select") == 0 ) {
        if (current->sqlpart == WHERE_PART) {
            // ignore everything in where statements...
            return;
        }

        switch( current->op ) {
            case NONE:
                root.child = (struct fsm *)calloc(1, sizeof(struct fsm));
                current = root.child;
                current->parent = &root;
                current->level = 1;
                current->scope_ctr = current->level;
                current->op = SELECT;
                current->sqlpart = SELECT_PART;
                // printf("SELECT case 1\n");
                break;
            case INSERT:
                // This is a select following a previous insert
                // build a new sibling model
                current->sibling = (struct fsm *)calloc(1, sizeof(struct fsm));
                current->sibling->parent = current->parent;
                current->sibling->scope_ctr = current->scope_ctr;
                current = current->sibling;
                current->level = current->parent->level + 1;
                current->scope_ctr = current->level;
                current->op = SELECT;
                current->sqlpart = SELECT_PART;
                // printf("SELECT case 2\n");
                break;
            case WITH:
                // This is a select following a previous with
                // build a new child model
                // printf("Building new model for with scope\n");
                if (current->child != NULL) {
                    current->sibling = (struct fsm *)calloc(1, sizeof(struct fsm));
                    current->sibling->parent = current->parent;
                    current->sibling->scope_ctr = current->scope_ctr;
                    current = current->sibling;
                    current->level = current->parent->level + 1;
                    current->scope_ctr = current->level;
                    current->op = SELECT;
                    current->sqlpart = SELECT_PART;
                    // printf("with case 1\n");
                } else {
                    current->child = (struct fsm *)calloc(1, sizeof(struct fsm));
                    current->child->parent = current;
                    current = current->child;
                    current->level = current->parent->level + 1;
                    current->scope_ctr = current->level;
                    current->op = SELECT;
                    current->sqlpart = SELECT_PART;
                    // printf("with case 2\n");
                }
                break;
            case UNION:
                // This is a select following a union
                // printf("Building new model for union scope\n");
                current->sibling = (struct fsm *)calloc(1, sizeof(struct fsm));
                current->sibling->parent = current->parent;
                // Hack to reverse the union setting
                current->op = SELECT;
                current = current->sibling;
                current->level = current->parent->level + 1;
                current->scope_ctr = current->level;
                current->op = SELECT;
                current->sqlpart = SELECT_PART;
                break;
            case SELECT:
                if ((current->scope_ctr > current->level) && (current->sqlpart == FROM_PART)) {
                    // printf("Building new model for new scope\n");
                    current->child = (struct fsm *)calloc(1, sizeof(struct fsm));
                    current->child->parent = current;
                    current = current->child;
                    current->level = current->parent->level + 1;
                    current->scope_ctr = current->level;
                    current->op = SELECT;
                    current->sqlpart = SELECT_PART;
                    break;
                }
                if (current->scope_ctr == current->level) {
                    // printf("Building new model for same level\n");
                    current->sibling = (struct fsm *)calloc(1, sizeof(struct fsm));
                    current->sibling->parent = current->parent;
                    current = current->sibling;
                    current->level = current->parent->level + 1;
                    current->scope_ctr = current->level;
                    current->op = SELECT;
                    current->sqlpart = SELECT_PART;
                    break;
                }
                break;
            default:
                printf("Don't know what to do 3\n");
                break;
        }
        return;
    }
    if (strcasecmp(ident, "from") == 0 ) {
        if (current->sqlpart == WHERE_PART) {
            // ignore everything in where statements...
            return;
        }
        if ((current->sqlpart == SELECT_PART) && (current->level < current->scope_ctr)) {
            return;
        }
        current->sqlpart = FROM_PART;
        switch( current->op ) {
            case SELECT:
                current->next = NEXT_IS_TABLENAME;
                // printf("FROM case 1\n");
                break;
            default:
                printf("Nonsensical state\n");
                break;
        }
        return;
    }
    if (strcasecmp(ident, "union") == 0 ) {
        if (current->op == SELECT) {
            current->op = UNION;
            current->next = NEXT_IS_FIELD;
            current->sqlpart = SELECT_PART;
        }
        return;
    }
    if (strcasecmp(ident, "where") == 0 ) {
        if (current->sqlpart != FROM_PART) {
            return;
        }
        if (current->op == SELECT) {
            current->sqlpart = WHERE_PART;
        }
        return;
    }
    if (strcasecmp(ident, "with") == 0) {
        // printf("WITH\n");
        if (current->op == NONE) {
            root.child = (struct fsm *)calloc(1, sizeof(struct fsm));
            current = root.child;
            current->parent = &root;
            current->level = 1;
            current->scope_ctr = current->level;
            current->op = WITH;
            current->next = NEXT_IS_ALIAS;
            // printf("WITH case 1\n");
            return;
        }
        if ((current->op == SELECT) && 
            ((current->next == NEXT_IS_TABLENAME) ||
             (current->next == NEXT_IS_ALIAS))) {
            current->sibling = (struct fsm *)calloc(1, sizeof(struct fsm));
            current->sibling->parent = current->parent;
            current = current->sibling;
            current->level = current->parent->level + 1;
            current->scope_ctr = current->level;
            current->op = WITH;
            current->next = NEXT_IS_ALIAS;
            // printf("WITH case 2\n");
            return;
        }
        if ((current->op == SELECT) && (current->next == NEXT_SCOPE_ENDED)) {
            current->sibling = (struct fsm *)calloc(1, sizeof(struct fsm));
            current->sibling->parent = current->parent;
            current = current->sibling;
            current->level = current->parent->level + 1;
            current->scope_ctr = current->level;
            current->op = WITH;
            current->next = NEXT_IS_ALIAS;
            // printf("WITH case 2\n");
            return;
        }
    }
    if (strcasecmp(ident, "as") == 0) {
        // AS is useless in this context
        return;
    }
    if (current->sqlpart != WHERE_PART) {
        if (current->next == NEXT_IS_TABLENAME) {
            strcpy(current->table, ident);
            strcpy(current->alias, ident);
            // printf("table: %s\n", current->table);
            current->next = NEXT_IS_ALIAS;
            return;
        }
        if (current->next == NEXT_IS_ALIAS) {
            strcpy(current->alias, ident);
            // printf("alias: %s\n", current->alias);
            current->next = NEXT_COMPLETE;
            return;
        }
        if (current->next == NEXT_IS_QUERY_ALIAS_CHILD) {
            if (current->child != NULL ) {
                struct fsm *child = current->child;
                while( child != NULL ) {
                    strcpy(child->query_alias, ident);
                    // printf("child alias: %s\n", current->alias);
                    child = child->sibling;
                }
                current->next = NEXT_IS_FIELD;
                return;
            }
        }
    }
    if (strcasecmp(ident, "if") || strcasecmp(ident, "begin")) {
        current->next = NEXT_SCOPE_ENDED;
    }
}

void push_symbol(const char symbol) 
{
    // printf("symbol: %c, scope: %d, level: %d, alias: %s\n", symbol, current->scope_ctr, current->level, current->alias);

    if (symbol == '(') {
        current->next = NEXT_IS_FIELD;
        current->scope_ctr++;
        return;
    }
    if (symbol == ')') {
        current->scope_ctr--;
        if (current->scope_ctr < current->level) {
            current->sqlpart = SELECT_PART;
            current = current->parent;
            while (current->sibling != NULL) {
                current = current->sibling;
            }
            current->scope_ctr--;
            current->next = NEXT_IS_QUERY_ALIAS_CHILD;
            current->sqlpart = SELECT_PART;
        }
        return;
    }
    if ((symbol == ',') && (current->op == WITH)) {
        // Add another with scope here...
        current->sibling = (struct fsm *)calloc(1, sizeof(struct fsm));
        current->sibling->parent = current->parent;
        current = current->sibling;
        current->level = current->parent->level + 1;
        current->scope_ctr = current->level;
        current->op = WITH;
        current->next = NEXT_IS_ALIAS;
    }
    if (symbol == ';') {
        current->next = NEXT_IS_FIELD;
    }
}

void push_backtick_literal(const char *literal)
{
    if (current->next == NEXT_IS_TABLENAME) {
        strcpy(current->table, literal);
        strcpy(current->alias, literal);
    }
    return;
}

void send_model(PyObject *callback) {
    PyObject *arglist;
    PyObject *result;
    char operation[BUFLEN+1] = {"\0"};

    struct fsm *cur = &root;

    while (cur != NULL) {
        switch( cur->op ) {
            case INSERT:
                strcpy(operation, "INSERT");
                break;
            case SELECT:
                strcpy(operation, "SELECT");
                break;
            case WITH:
                strcpy(operation, "WITH");
                break;
            case NONE:
                strcpy(operation, "NONE");
                break;
            default:
                strcpy(operation, "UNKNOWN");
                break;
        }

        // printf("%s, %s, %d, %d\n", cur->table, cur->alias, cur->level, cur->scope_ctr);

        arglist = Py_BuildValue("(sssssi)", 
            cur->parent->alias, 
            cur->table, 
            cur->alias,
            cur->query_alias, 
            operation, 
            cur->level);
        if (arglist == NULL) {
            printf("Arg list could not be built. An exception occurred\n");
            break;
        }
        result = PyObject_CallObject(callback, arglist);
        Py_DECREF(arglist);

        if (result == NULL) {
            printf("Result came back null, so an exception occurred\n");
            break;
        }
        Py_DECREF(result);

        if (cur->child != NULL) {
            cur = cur->child;
        } else if (cur->sibling != NULL) {
            cur = cur->sibling;
        } else {
            while (cur->sibling == NULL) {
                cur = cur->parent;
                if (cur == &root) {
                    cur = NULL;
                    break;
                }
            }
            if (cur != NULL) {
                cur = cur->sibling;
            }
        }
    }
}

static void recursive_cleanup(struct fsm *cur)
{
    if (cur->child != NULL) {
        recursive_cleanup(cur->child);
        cur->child = NULL;
    }
    if (cur->sibling != NULL) {
        recursive_cleanup(cur->sibling);
    }
    free(cur);
}

void memory_cleanup(void)
{
    if (root.child != NULL) {
        recursive_cleanup(root.child);
        root.child = NULL;
    }
    if (root.sibling != NULL) {
        recursive_cleanup(root.sibling);
    }
}
