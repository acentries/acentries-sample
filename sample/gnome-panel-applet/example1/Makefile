
OPTION = `pkg-config --cflags --libs libpanelapplet-2.0`


build: my_applet


install: install_my_applet install_server


uninstall:
	rm  /usr/lib/gnome-panel/my_applet
	rm /usr/lib/bonobo/servers/ExampleApplet.server


install_my_applet: my_applet
	cp my_applet /usr/lib/gnome-panel/

install_server: Exampleapplet.server
	cp Exampleapplet.server /usr/lib/bonobo/servers/


my_applet: my_applet.c
	gcc  -o my_applet my_applet.c ${OPTION}

