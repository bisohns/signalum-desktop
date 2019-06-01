#! /bin/sh
cd src/main/ui &&
find -name "*.ui" -exec sh -c 'pyuic5 "$0" -o "../python/qt/${0%.ui}.py"' {} \;
