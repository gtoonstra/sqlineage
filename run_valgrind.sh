#!/bin/bash

valgrind --tool=memcheck --suppressions=misc/valgrind-python.supp pytest
