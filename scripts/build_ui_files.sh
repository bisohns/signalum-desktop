#! /bin/sh
cd ui &&
find -name "*.ui" -exec sh -c 'pyuic5 "$0" -o "../signalum_qt/qt/${0%.ui}.py"' {} \;
