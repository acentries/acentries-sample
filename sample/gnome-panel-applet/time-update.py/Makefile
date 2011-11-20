


build: time_update.py


install: install_applet install_server


uninstall:
	rm  /usr/lib/gnome-panel/time_update.py
	rm /usr/lib/bonobo/servers/TimeUpdate.server


install_applet: time_update.py
	cp time_update.py /usr/lib/gnome-panel/

install_server: TimeUpdate.server
	cp TimeUpdate.server /usr/lib/bonobo/servers/

