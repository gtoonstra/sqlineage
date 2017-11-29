#ifndef STATE_MACHINE_H
#define STATE_MACHINE_H

#include <Python.h>

void initialize_fsm(void);
void push_ident(const char *ident);
void push_symbol(const char symbol);
void send_model(PyObject *callback);
void push_backtick_literal(const char *literal);
void memory_cleanup(void);

#endif
