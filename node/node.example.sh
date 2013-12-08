#!/bin/bash
ARGUSVIRTENV=/usr/local/bin/argusvirtualenv
ARGUSNODE=/usr/local/bin/argus/node/node.py

source $ARGUSVIRTENV/bin/activate
python $ARGUSNODE
