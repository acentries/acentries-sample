

import pygtk
pygtk.require('2.0')

import sys
import traceback
import time
import commands
import glib
import gtk
import gnomeapplet

print "hello"



IID_FACTORY = "OAFIID:TimeUpdateApplet_Factory"


def main():
    if len(sys.argv) > 1:
        print "given args: " + " ".join(sys.argv)
        app = AppletController( None )
        app.on_preference_request( None, None )

        on_delete = lambda widget, data=None : (gtk.main_quit(),False)[-1]

        window = app.fm.window
        window.connect('destroy_event', on_delete )
        window.connect('delete_event', on_delete )

        window.show_all()
        gtk.main()
    else:
        gnomeapplet.bonobo_factory( IID_FACTORY ,gnomeapplet.Applet.__gtype__,"hello", "0", applet_factory )


def applet_factory(applet, iid ):
    try:
        app = AppletController( applet )
        app.create_applet_indicator()

        create_menu(applet, app.on_preference_request )
        applet.show_all()
        return True
    except:
        print traceback.format_exc()
        return False


class AppletController:
    def __init__( self, applet ):
        self.applet = applet
        self.timer  = TimerController()
        self.ps_checker = ProcessChecker()

    def create_applet_indicator(self):
        event_box = gtk.EventBox()
        event_box.connect("button_press_event", self.on_main_click, None)
        label = gtk.Label("Success!")
        event_box.add(label)

        self.applet.add(event_box)


    def on_main_click(self, event_box, event, data):
        print event

    def on_preference_request(self,w,d):
        try:
            print "on_preference_request"
            print w
            self.fm = create_preference_dialog( self.on_preference_submit )
            self.fm.window.show_all()
        except:
            print traceback.format_exc()


    def on_preference_submit( self, w, d ):
        print "on_preference_submit"
        try:
            config = self.fm.get_value()
            print "create new time model: " + str(config)
            time_model = TimerModel()
            time_model.set_pid( config["pid"] )
            time_model.set_interval( config["interval"] )
            self.timer.time_model = time_model
            self.on_timeout()
            print "start process wailt!!"
        except:
            print "form submit failur"
            print traceback.format_exc()



    def on_timeout( self, user_data = None ):
        print "on_timeout"
        timer = self.timer
        pid = timer.timer.pid
        ps = self.ps_checker

        if timer.available():
            if ps.check( pid ):
                timer.update_status( ps.get_last_process() )
            else:
                timer.end()
                print "on_timeout returns False"
                return False
        elif timer.ready():
            timer.start( self.on_timeout )
        return True


class ProcessChecker:
    def __init__(self):
        self.last_ps_output = ""

    def check( self, pid ):
        self.last_ps_output = commands.getoutput("ps -p " + str( pid ) + " -f").splitlines()
        return ( len( self.last_ps_output ) == 2)

    def get_last_process(self):
        if len(self.last_ps_output) == 2:
            return self.last_ps_output[-1]
        else:
            return None

class TimerController:
    def __init__( self ):
        self.timer = None
        self.time_model = TimerModel()
        self.time_model.set_pid( -1 )
        self.time_model.set_interval( 20 )

    def available( self ):
        return self.timer != None

    def start( self, handler ):
        print "start timer: " + str( self.time_model )
        self.timer = glib.timeout_add_seconds( self.time_model.interval, handler ,None )

    def ready( self ):
        return self.time_model.pid != -1

    def update_status( self, message ):
        print message

    def end(self):
        glib.source_remove( self.timer )
        self.timer = None
        print "process end"
        


def create_menu(applet, handler):
    xml="""<popup name="button3">
<menuitem name="ItemPreferences" 
    verb="Preferences" 
    label="_Preferences" 
    pixtype="stock" 
    pixname="gtk-preferences"/>
<separator/>
<submenu name="Submenu" _label="Su_bmenu">
<menuitem name="ItemAbout" 
    verb="About" 
    label="_About" 
    pixtype="stock" 
    pixname="gtk-about"/>
    </submenu>
</popup>"""
    verbs = [('About', handler), ('Preferences', handler )]
    applet.setup_menu(xml, verbs, None)



def create_preference_dialog( handler ):
    fm = FormManager()
    fm.add_entry("pid", "PID", False)
    fm.add_entry("interval", "Update Interval", False )
    fm.add_button("Submit", handler )

    return fm



class FormManager:
    def __init__( self ):
        self.vbox = gtk.VBox()
        self.window = gtk.Window()
        self.window.add( self.vbox )
        self.entries = {}


    def add_entry(self, key,input_name, check):
        label = gtk.Label( input_name )
        edit = gtk.Entry()
        box = gtk.HBox(False,10)
        box.add( label )
        box.add( edit )
        self.vbox.add( box )

        self.entries[key] = edit

    def add_button(self, text, handler):
        #box = gtk.HBox(10)
        button = gtk.Button(text)
        button.connect("clicked", handler, self )
        self.vbox.add( button )
        
    def get_value(self):
        return dict([ (key,self.entries[key].get_text()) for key in self.entries.keys()])



class TimerModel:

    def __init__(self):
        self.clean()


    def clean(self):
        self.interval = 20
        self.pid = -1

    def set_interval(self,interval):
        self.interval = int(interval)

    def set_pid( self, pid ):
            self.pid = int( pid )





if __name__ == '__main__':
    main()

