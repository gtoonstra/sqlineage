#include <stdio.h>
#include <string.h>
#include "state_machine.h"


#define BUFLEN      128


typedef enum {NONE, INSERT, SELECT} operation_t;
typedef enum {NEXT_IS_FIELD, NEXT_IS_TABLENAME, NEXT_IS_ALIAS} next_t;

struct fsm {
    char table[BUFLEN+1];
    char alias[BUFLEN+1];
    operation_t op;
    next_t next;
    int level;
    struct fsm *sibling;
    struct fsm *child;
    struct fsm *parent;
    int in_select;
    int in_insert;
    int in_from;
} fsm_t;

struct fsm root;
struct fsm *current;


void initialize_fsm() {
    memset(&root, 0x00, sizeof(fsm_t));
    current = &root;
    root.op = NONE;
    strcpy(root.table, "ROOT");
    root.parent = &root;
}

void push_ident(const char *ident) {
    if (strcasecmp(ident, "insert") == 0 ) {
        switch( current->op ) {
            case NONE:
                root.child = (struct fsm *)calloc(1, sizeof(struct fsm));
                current = root.child;
                current->parent = &root;
                current->level = 1;
                current->op = INSERT;
                printf("INSERT seen\n");
                break;
            default:
                printf("Don't know what to do 1\n");
                break;
        }
        return;
    }
    if (strcasecmp(ident, "into") == 0 ) {
        if (current->op != INSERT) {
            printf("Unexpected keyword\n");
        }
        current->next = NEXT_IS_TABLENAME;
        printf("INTO seen\n");
        return;
    }
    if (strcasecmp(ident, "select") == 0 ) {
        switch( current->op ) {
            case NONE:
                root.child = (struct fsm *)calloc(1, sizeof(struct fsm));
                current = root.child;
                current->parent = &root;
                current->level = 1;
                current->op = SELECT;
                printf("SELECT seen 1\n");
                break;
            case INSERT:
                // This is a select following a previous insert
                // build a new model
                current->sibling = (struct fsm *)calloc(1, sizeof(struct fsm));
                current->sibling->parent = current->parent;
                current = current->sibling;
                current->level = current->parent->level + 1;
                current->op = SELECT;
                printf("SELECT seen 2\n");
                break;
            default:
                printf("Don't know what to do 2\n");
                break;
        }
        return;
    }
    if (strcasecmp(ident, "from") == 0 ) {
        switch( current->op ) {
            case SELECT:
                current->next = NEXT_IS_TABLENAME;
                printf("FROM seen\n");
                break;
            default:
                printf("Nonsensical state\n");
                break;
        }
        return;
    }
    if (current->next == NEXT_IS_TABLENAME) {
        strcpy(current->table, ident);
        printf("table: %s\n", current->table);
        current->next = NEXT_IS_ALIAS;
        return;
    }
}

void push_symbol(const char symbol) {
    printf("symbol: %c\n", symbol);
}

void send_model(PyObject *callback) {
    PyObject *arglist;
    PyObject *result;
    char *operation[BUFLEN+1] = {"\0"};

    struct fsm *cur = &root;

    while (cur != NULL) {
        switch( cur->op ) {
            case INSERT:
                strcpy(operation, "INSERT");
                break;
            case SELECT:
                strcpy(operation, "SELECT");
                break;
            default:
                strcpy(operation, "NONE");
                break;
        }
        arglist = Py_BuildValue("(ssssi)", cur->parent->table, cur->table, cur->alias, operation, cur->level);
        result = PyObject_CallObject(callback, arglist);
        // How to check result?
        Py_DECREF(arglist);

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
