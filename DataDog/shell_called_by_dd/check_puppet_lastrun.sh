#!/bin/bash

#lockfile_vars
my_name=`basename "$0"`
lock_dir="/var/tmp"
last_run_summary="/var/lib/puppet/state/last_run_summary.yaml"

function lockfile {
    #Check for lock
    if [ -f "${lock_dir}/${my_name}" ]; then
        echo "${my_name} Lock file exists"
        exit 1
    else
        touch ${lock_dir}/${my_name}
    fi
}

function unlockfile {

    rm ${lock_dir}/${my_name}
}

function puppet_last_run {

    if ! [ -f ${last_run_summary} ]
        then echo "file does not exist." && unlockfile && exit 1
    fi

    lr=`egrep -ir "last_run" ${last_run_summary} | awk -F ':' '{print $2}' | sed -e 's/ //g'`
    now=`date +%s`
    diff=`bc <<< "((${now} - ${lr}))/60"`
    #Human readable format:
    #echo "last run was ${diff} minutes ago.."
    echo ${diff}
}

#lockfile
puppet_last_run
#unlockfile

