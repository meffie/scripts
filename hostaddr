#!/bin/bash
# Show my IPv4 address (skipping bridges, etc.)

ip -oneline route list |
    grep '^default' |
    perl -lane 'print $1 if /dev\s(\w+)\s/' |
    while read dev; do
        ip -oneline -4 address show dev $dev up |
            perl -lane 'print $1 if /inet ([\d\.]+)/'
    done
