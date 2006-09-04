import gtk, gobject
from gtk import gdk

__title__ = _("Move History")

widgets = gtk.glade.XML("sidepanel/history.glade")
__widget__ = widgets.get_widget("panel")
widgets.get_widget("window").remove(__widget__)

__active__ = True

numbers = widgets.get_widget("treeview1")
left = widgets.get_widget("treeview2")
right = widgets.get_widget("treeview3")

def fixList (list):
    list.set_model(gtk.ListStore(str))
    renderer = gtk.CellRendererText()
    #import pango
    #renderer.set_property("alignment", "left")
    list.append_column(gtk.TreeViewColumn(None, renderer, text=0))

def ready (window):
    #TODO: number should be right alligned
    for list in (numbers, left, right):
        fixList(list)
    numbers.modify_fg(gtk.STATE_INSENSITIVE, gtk.gdk.Color(0,0,0))
    
    widgets.signal_autoconnect ({
        "treeview1_selection_changed": lambda w: select_cursor_row(w,1), 
        "treeview2_selection_changed": lambda w: select_cursor_row(w,2), 
        "treeview3_selection_changed": lambda w: select_cursor_row(w,3),
        "on_treeview2_key_press_event": lambda w,e: key_press_event(1,e),
        "on_treeview3_key_press_event": lambda w,e: key_press_event(2,e)
    })
    
    global board
    board = window["CairoBoard"]
    
    board.connect("history_changed",
            lambda w,his: his.connect("changed", history_changed))
    board.connect("shown_changed", shown_changed)
    
def select_cursor_row (tree, col):
    iter = tree.get_selection().get_selected()[1]
    if iter == None: return
    else: sel = tree.get_model().get_path(iter)[0]
    board.shown = sel*2+col-1

from gtk.gdk import keyval_from_name
leftkeys = map(keyval_from_name,("Left", "KP_Left"))
rightkeys = map(keyval_from_name,("Right", "KP_Right"))
def key_press_event (col, event):
    if event.keyval in leftkeys and col == 2:
        shown = board.shown - 1
        w = left
    elif event.keyval in rightkeys and col == 1:
        shown = board.shown + 1
        w = right
    else: return
    row = int((shown-1) / 2)
    def todo():
        w.set_cursor((row,))
        w.grab_focus()
    idle_add(todo)

def idle_add(proc, *args):
    """Makes sure function is only called once"""
    def proc_star():
        proc(*args)
        return False
    gobject.idle_add(proc_star)

def history_changed (history):
    view = len(history) & 1 and right or left
    notat = history.moves[-1].algNotat(history.clone().reverse())
    idle_add(view.get_model().append, [notat])
    if len(history) / 2 > len(numbers.get_model()):
        num = str(int(len(history)/2))+"."
        idle_add(numbers.get_model().append, [num])
    #idle_add(lambda: numbers.scroll_to_cell((4,)))
    #idle_add(widgets.get_widget("panel").get_vscrollbar().set_value,
    #        numbers.get_allocation().height)

def shown_changed (board, shown):
    if shown <= 0:
        def todo():
            left.get_selection().unselect_all()
            right.get_selection().unselect_all()
        idle_add(todo)
        return
        
    col = shown & 1 and left or right
    other = shown & 1 and right or left
    row = int((shown-1) / 2)
    def todo():
        col.get_selection().select_iter(col.get_model().get_iter(row))
        other.get_selection().unselect_all()
    idle_add(todo)