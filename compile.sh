#!/bin/bash

# rm src/sqlineage.c

rm src/sqlscanner.c

#ragel -C -V --error-format=gnu -o src/sqlineage.dot src/sqlineage.rl
#dot -Tjpg -odocs/sqlineage.jpg src/sqlineage.dot
# ragel -C --error-format=gnu -o src/sqlineage.c src/sqlineage.rl

ragel -C --error-format=gnu -o src/sqlscanner.c src/sqlscanner.rl

python3 setup.py build
python3 setup.py install
