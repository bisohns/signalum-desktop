ui_files:
	sudo `which python` build.py ui_files
	@echo "SIGNALUM >>> generated py code from ui"

resources:
	pyrcc5 src/main/resources/icons.qrc -o src/main/python/signalum_qt/resources.py
	@echo "SIGNALUM >>> transformed resources complete"

dependencies:
	sudo apt-get install bluetooth libbluetooth-dev
	@echo "SIGNALUM >>> install python dependencies"
	pip install -r requirements/linux.txt

dev:
	# build ui files
	make ui_files
	@echo "SIGNALUM >>> starting gui program"
	sudo `which python` build.py run

freeze:
	# freeze app
	make ui_files
	@echo "SIGNALUM >>> freezing application ..."
	`which python` build.py freeze --debug
	@echo "SIGNALUM >>> completed freeze"

installer:
	# make installer
	make ui_files
	@echo "SIGNALUM >>> creating installer"
	`which python` build.py installer
	@echo "SIGNALUM >>> created installer"

uninstall:
	pip uninstall -r requirements/linux.txt
	@echo "SIGNALUM >>> uninstallation complete"
