argus
=====

Website/server monitoring tool

## Installation

Easiest way is to create a virtualenv and do a

    pip install -r requirements.txt

Then copy node.example.sh and edit it to reflect the correct paths to the virtualenv and the node.py script.


## Usage

Run the node in its virtualenv, preferable through the provided shell script.

The node creates a settings.db on first run. This contains information on its location, tasks and neighbour nodes.

events.db contains information gathered by argus and incoming and outgoing requests.
