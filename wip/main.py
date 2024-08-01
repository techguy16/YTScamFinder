import sys
import gi # type: ignore
import data
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw # type: ignore
        
class MainWindow(Gtk.ApplicationWindow):
    def hello(self, button):
        print("Hello world")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(600, 600)
        self.set_title(data.APP_NAME)
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)
        self.box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.button = Gtk.Button(label="Hello")
        self.button.connect('clicked', self.hello)

        self.set_child(self.box1)  # Horizontal box to window
        self.box1.append(self.box2)  # Put vert box in that box
        self.box1.append(self.box3)  # And another one, empty for now

        self.box2.append(self.button) # Put button in the first of the two vertical boxes

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = MyApp(application_id="io.github.techguy16.YTScamFinder")
app.run(sys.argv)
