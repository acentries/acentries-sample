
OPTION = `pkg-config --cflags --libs libpanelapplet-2.0`


build: time_update


install: install_applet install_server


uninstall:
	rm  /usr/lib/gnome-panel/time_update
	rm /usr/lib/bonobo/servers/TimeUpdate.server


install_applet: time_update
	cp time_update /usr/lib/gnome-panel/

install_server: TimeUpdate.server
	cp TimeUpdate.server /usr/lib/bonobo/servers/


time_update: time_update.c
	gcc  -o time_update time_update.c ${OPTION}

