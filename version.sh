#!/bin/bash

help_command() {
    echo "# VERSION : Change the version for app"
    echo "The commands are : "
    echo "- list : to list version"
    echo "- change _newVersion_ : change the version"
    echo "- remove-snapshot : remove the snapshot from the version"
}

list_command() {
    appVersion=$(sed "s/^    version=\"\(.*\)\",$/\1/;t;d" ./setup.py)
    echo "app version : $appVersion "
}

change_version() {
    newVersion=$1

    if [[ ! $newVersion =~ ^[[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+(-SNAPSHOT)?$ ]]; then
        echo "Error : the version '$newVersion' is invalid"
        exit 2
    fi

    echo "Change version to $newVersion"

    sed -i -e "s/^    version=\".*\",$/    version=\"$newVersion\",/g" ./setup.py
    sed -i -e "s/VERSION = \".*\"/VERSION = \"$newVersion\"/g" ./pyscriptdeck/_version.py
}

change_command() {
    if [ $# -ne 1 ]; then
        echo "Error: the command 'change' needs the version as parameter"
        exit 1
    fi
    newVersion=$1
    change_version $newVersion
}

remove_snapshot_command() {
    appVersion=$(sed "s/^    version=\"\(.*\)\",$/\1/;t;d" ./setup.py)

    if [[ $version =~ "SNAPSHOT" ]]; then
        echo "=> Remove SNAPSHOT From version"
        version=${version/-SNAPSHOT/}
        change_version $version
    fi
}

if [ $# -eq 0 ]; then
    help_command
    exit 1
fi

command=$1
if [[ "$command" = "list" ]]; then
    list_command $2
elif [[ "$command" = "change" ]]; then
    change_command $2
elif [[ "$command" = "remove-snapshot" ]]; then
    remove_snapshot_command
else
    echo "Error: command '$command' invalid"
    exit 1
fi
