#include <string.h>
#include<stdio.h>
#include <panel-applet.h>
#include <gtk/gtklabel.h>

static const char Context_menu_xml [] =
    "<popup name=\"button3\">\n"
    "   <menuitem name=\"Properties Item\" "
    "             verb=\"ExampleProperties\" "
    "           _label=\"_Preferences...\"\n"
    "          pixtype=\"stock\" "
    "          pixname=\"gtk-properties\"/>\n"
    "   <menuitem name=\"About Item\" "
    "             verb=\"ExampleAbout\" "
    "           _label=\"_About...\"\n"
    "          pixtype=\"stock\" "
    "          pixname=\"gnome-stock-about\"/>\n"
    "</popup>\n";

static void display_properties_dialog(BonoboUIComponent *uic, struct MultiRes *applet ){
    printf("hit context menu\n");
}

static const BonoboUIVerb myexample_menu_verbs [] = {
    BONOBO_UI_VERB ("ExampleProperties", display_properties_dialog),
    BONOBO_UI_VERB ("ExampleAbout", display_properties_dialog),
    BONOBO_UI_VERB_END
};



static gboolean on_button_press (GtkWidget *event_box, GdkEventButton *event, gpointer data);


static gboolean
myexample_applet_fill (PanelApplet *applet,
        const gchar *iid,
        gpointer data)
{
    GtkWidget *label, *image, *event_box;

    if (strcmp (iid, "OAFIID:TimeUpdateApplet") != 0)
        return FALSE;

    panel_applet_setup_menu (PANEL_APPLET ( applet ),Context_menu_xml, myexample_menu_verbs,NULL);

    label = gtk_label_new ("Time set");
    //image = gtk_image_new_from_file("/usr/share/pixmaps/gnome-set-time.png"),
    event_box = gtk_event_box_new ();
    gtk_container_add (GTK_CONTAINER (event_box), label);
    g_signal_connect( G_OBJECT ( event_box ), "button_press_event", G_CALLBACK (on_button_press), label );

    gtk_container_add (GTK_CONTAINER (applet), event_box );

    gtk_widget_show_all (GTK_WIDGET (applet));

    return TRUE;
}

static gboolean
on_button_press (GtkWidget *event_box, GdkEventButton *event, gpointer data){
    static int window_shown;
    static GtkWidget *window, *box, *image, *label;
    printf("hit applet\n");
    /* Don't react to anything other than the left mouse button;
     *     return FALSE so the event is passed to the default handler */
    if (event->button != 1)
        return FALSE;

    if (!window_shown) {
        window = gtk_window_new (GTK_WINDOW_TOPLEVEL);
        box = GTK_BOX (gtk_vbox_new (TRUE, 12));
        gtk_container_add (GTK_CONTAINER (window), box);

        label = gtk_label_new ("Hello World");
        gtk_box_pack_start (GTK_BOX (box), label, TRUE, TRUE, 12);
        gtk_widget_show_all (window);
    }else{
        gtk_widget_hide (GTK_WIDGET (window));
    }

    window_shown = !window_shown;
    return TRUE;
}

PANEL_APPLET_BONOBO_FACTORY ("OAFIID:TimeUpdateApplet_Factory",
        PANEL_TYPE_APPLET,
        "The Hello World Applet",
        "0",
        myexample_applet_fill,
        NULL);
