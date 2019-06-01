#! /bin/sh
cd src/main/ui &&
find -name "*.ui" -exec sh -c 'pyuic5 "$0" -o "../python/signalum_qt/qt/${0%.ui}.py"' {} \;