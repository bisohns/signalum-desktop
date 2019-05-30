.PHONY: ui_files

ui_files:
	scripts/build_ui_files.sh

dependencies:
	sudo apt-get install bluetooth libbluetooth-dev
	pip install -r requirements.txt

install:
	make dependencies
	sudo chmod a+rx ./signalum
	sudo ln -sr ./signalum /usr/local/bin/
	@echo "installation complete, enter `signalum` to run"

development:
	make dependencies
	make ui_files
	./signalum
