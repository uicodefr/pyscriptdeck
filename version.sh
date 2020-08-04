#!/bin/bash

if [ $# -ne 1 ]; then
	echo "# VERSION : Change the version for the client and the server"
	echo "- current version : "$(sed "s/^    version=\"\(.*\)\",$/\1/;t;d" ./setup.py)
	echo "# Need 1 parameter to change version : the new version"
	exit 1
fi

newVersion=$1

if [[ ! $newVersion =~ ^[[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+(-SNAPSHOT)?$ ]]; then
	echo "# VERSION : The version '$newVersion' is invalid"
	exit 2
fi

echo "# VERSION : Change version to $newVersion"

sed -i -e "s/^    version=\".*\",$/    version=\"$newVersion\",/g" ./setup.py
sed -i -e "s/VERSION = \".*\"/VERSION = \"$newVersion\"/g" ./pyscriptdeck/_version.py

echo "# VERSION : End"
