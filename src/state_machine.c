#include <stdio.h>
#include <string.h>
#include "state_machine.h"


#define BUFLEN      128


typedef enum {NONE, INSERT, SELECT, WITH} operation_t;
typedef enum {NEXT_IS_FIELD, NEXT_IS_TABLENAME, NEXT_IS_ALIAS} next_t;

struct fsm {
    char table[BUFLEN+1];
    char alias[BUFLEN+1];
    operation_t op;
    next_t next;
    int level;
    int scope_ctr;
    struct fsm *sibling;
    struct fsm *child;
    struct fsm *parent;
} fsm_t;

struct fsm root;
struct fsm *current;


void initialize_fsm() {
    memset(&root, 0x00, sizeof(struct fsm));
    current = &root;
    root.op = NONE;
    strcpy(root.table, "ROOT");
    root.parent = &root;
}

void push_ident(const char *ident) {
    if (current == NULL) {
        printf("CURRENT IS NULL!\n");
        return;
    }
    if (strcasecmp(ident, "insert") == 0 ) {
        switch( current->op ) {
            case NONE:
                root.child = (struct fsm *)calloc(1, sizeof(struct fsm));
                current = root.child;
                current->parent = &root;
                current->level = 1;
                current->scope_ctr = 1;
                current->op = INSERT;
                printf("INSERT\n");
                break;
            default:
                printf("INSERT after other statements\n");
                current->sibling = (struct fsm *)calloc(1, sizeof(struct fsm));
                current->sibling->parent = current->parent;
                current->sibling->scope_ctr = current->scope_ctr;
                current = current->sibling;
                current->level = current->parent->level + 1;
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
        printf("INTO\n");
        return;
    }
    if (strcasecmp(ident, "select") == 0 ) {
        switch( current->op ) {
            case NONE:
                root.child = (struct fsm *)calloc(1, sizeof(struct fsm));
                current = root.child;
                current->parent = &root;
                current->level = 1;
                current->scope_ctr = current->level;
                current->op = SELECT;
                printf("SELECT case 1\n");
                break;
            case INSERT:
                // This is a select following a previous insert
                // build a new sibling model
                current->sibling = (struct fsm *)calloc(1, sizeof(struct fsm));
                current->sibling->parent = current->parent;
                current->sibling->scope_ctr = current->scope_ctr;
                current = current->sibling;
                current->level = current->parent->level + 1;
                current->op = SELECT;
                printf("SELECT case 2\n");
                break;
            case WITH:
                // This is a select following a previous insert
                // build a new sibling model
                printf("Building new model for with scope\n");
                current->child = (struct fsm *)calloc(1, sizeof(struct fsm));
                current->child->parent = current;
                current->child->scope_ctr = current->scope_ctr;
                current = current->child;
                current->level = current->parent->level + 1;
                current->op = SELECT;
                break;
            case SELECT:
                if (current->scope_ctr > current->level) {
                    printf("Building new model for new scope\n");
                    current->child = (struct fsm *)calloc(1, sizeof(struct fsm));
                    current->child->parent = current;
                    current->child->scope_ctr = current->scope_ctr;
                    current = current->child;
                    current->level = current->parent->level + 1;
                    current->op = SELECT;
                    break;
                }
                if (current->scope_ctr == current->level) {
                    printf("Building new model for same level\n");
                    current->sibling = (struct fsm *)calloc(1, sizeof(struct fsm));
                    current->sibling->parent = current->parent;
                    current->sibling->scope_ctr = current->level;
                    current = current->sibling;
                    current->level = current->parent->level + 1;
                    current->op = SELECT;
                    break;
                }
                printf("Don't know what to do 2\n");
                break;
            default:
                printf("Don't know what to do 3\n");
                break;
        }
        return;
    }
    if (strcasecmp(ident, "from") == 0 ) {
        switch( current->op ) {
            case SELECT:
                current->next = NEXT_IS_TABLENAME;
                printf("FROM case 1\n");
                break;
            default:
                printf("Nonsensical state\n");
                break;
        }
        return;
    }
    if (strcasecmp(ident, "with") == 0) {
        if (current->op == NONE) {
            root.child = (struct fsm *)calloc(1, sizeof(struct fsm));
            current = root.child;
            current->parent = &root;
            current->level = 1;
            current->scope_ctr = current->level;
            current->op = WITH;
            current->next = NEXT_IS_ALIAS;
            printf("WITH case 1\n");
            return;
        }

        if ((current->op == SELECT) && (current->next >= NEXT_IS_TABLENAME)) {
            current->sibling = (struct fsm *)calloc(1, sizeof(struct fsm));
            current->sibling->parent = current->parent;
            current->sibling->scope_ctr = current->scope_ctr;
            current = current->sibling;
            current->level = current->parent->level + 1;
            current->op = WITH;
            current->next = NEXT_IS_ALIAS;
            printf("WITH case 2\n");
            return;
        }
    }
    if (current->next == NEXT_IS_TABLENAME) {
        strcpy(current->table, ident);
        strcpy(current->alias, ident);
        printf("table: %s\n", current->table);
        current->next = NEXT_IS_ALIAS;
        return;
    }
    if (current->next == NEXT_IS_ALIAS) {
        strcpy(current->alias, ident);
        printf("alias: %s\n", current->alias);
        current->next = NEXT_IS_FIELD;
        return;
    }
}

void push_symbol(const char symbol) {
    // printf("symbol: %c\n", symbol);

    if (symbol == '(') {
        current->next = NEXT_IS_FIELD;
        current->scope_ctr++;
        return;
    }
    if (symbol == ')') {
        current->scope_ctr--;
        if (current->scope_ctr < current->level) {
            printf("Down a level\n");
            current = current->parent;
            current->next = NEXT_IS_ALIAS;
            while (current->sibling != NULL) {
                current = current->sibling;
            }
        }
        return;
    }
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

        arglist = Py_BuildValue("(ssssi)", cur->parent->table, cur->table, cur->alias, operation, cur->level);
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
