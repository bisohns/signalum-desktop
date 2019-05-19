cd ui_files &&
find -name "*.ui" -exec sh -c 'pyuic5 "$0" -o "${0%.ui}.py"' {} \;
