#!/bin/bash
set -e

BRANCHES="openafs-stable-1_6_x openafs-stable-1_8_x master"
SINCE=$(date --date='7 days ago' '+%s')

report_submitted() {
    branch=$1
    git gerrit-query --format="{created} {number} {subject}" branch:${branch} NOT status:abandoned |
    while read created_date created_time number subject; do
        timestamp=$(date --date="$created_date $created_time" "+%s")
        if [ $timestamp -gt $SINCE ]; then
            echo "$number $subject"
        fi
    done
}

report_merged() {
    branch=$1
    git gerrit-log report/merged/${branch}..origin/${branch}
    git branch --no-track --force report/merged/$branch origin/${branch}
}

cd ~/src/openafs
git fetch origin
for branch in ${BRANCHES}; do
    echo "Recently submitted for branch '${branch}':"
    echo ""
    report_submitted $branch
    echo ""
    echo "Recently merged onto branch '${branch}':"
    echo ""
    report_merged $branch
    echo ""
done
