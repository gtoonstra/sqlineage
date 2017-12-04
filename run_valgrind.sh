#!/bin/bash

valgrind --leak-check=full --suppressions=misc/valgrind-python.supp pytest
