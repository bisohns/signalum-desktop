.PHONY: ui_files

ui_files:
	scripts/build_ui_files.sh

dependencies:
	@echo "SIGNALUM >>> installing apt dependencies"
	sudo apt-get install bluetooth libbluetooth-dev
	@echo "SIGNALUM >>> install python dependencies"
	pip install -r requirements.txt

install:
	@echo "SIGNALUM >>> making dependencies"
	make dependencies
	sudo apt  install --no-install-recommends gnome-panel
	sudo chmod a+rx ./signalum
	@echo "SIGNALUM >>> creating symlink at /usr/local/bin/signalum"
	sudo ln -srf ./signalum /usr/local/bin/
	@echo "SIGNALUM >>> installation complete, enter `signalum` to run"

development:
	make dependencies
	make ui_files
	./signalum

uninstall:
	pip uninstall signalum
	sudo rm -rf /usr/local/bin/signalum
	- sudo rm ~/Desktop/signalum.desktop
	@echo "SIGNALUM >>> uninstallation complete"
