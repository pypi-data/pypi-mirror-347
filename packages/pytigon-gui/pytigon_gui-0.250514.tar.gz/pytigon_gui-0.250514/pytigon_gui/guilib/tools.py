import os
import wx
import importlib

from pytigon_lib.schtools.main_paths import get_main_paths

try:
    from pyshortcuts import make_shortcut
except:
    make_shortcut = None
import sys
import pytigon

_ = wx.GetTranslation


SIZE_DEFAULT = -1
SIZE_SMALL = 0
SIZE_MEDIUM = 1
SIZE_LARGE = 2


def norm_colour2(c):
    x = int(c)
    if x > 255:
        return 255
    else:
        return x


def norm_colour(r, g, b, proc):
    if proc > 1:
        y = (255, 255, 255)
        dx = 2 - proc
    else:
        y = (0, 0, 0)
        dx = proc
    dy = 1 - dx
    ret = [int(r * dx + y[0] * dy), int(g * dx + y[1] * dy), int(b * dx + y[1] * dy)]
    for i in range(3):
        if ret[i] > 255:
            ret[i] = 255
    return ret


def colour_to_html(colour):
    return wx.Colour(colour.Red(), colour.Green(), colour.Blue()).GetAsString(
        wx.C2S_HTML_SYNTAX
    )


def get_colour(wx_id, proc=None):
    c1 = wx.SystemSettings.GetColour(wx_id)
    if not proc:
        return colour_to_html(c1)
    else:
        x = norm_colour(c1.Red(), c1.Green(), c1.Blue(), proc)
        c2 = wx.Colour(x[0], x[1], x[2])
        return colour_to_html(c2)


def standard_tab_colour():
    return (
        ("color_body_0_2", get_colour(wx.SYS_COLOUR_3DFACE, 0.2)),
        ("color_body_0_5", get_colour(wx.SYS_COLOUR_3DFACE, 0.5)),
        ("color_body_0_7", get_colour(wx.SYS_COLOUR_3DFACE, 0.7)),
        ("color_body_0_9", get_colour(wx.SYS_COLOUR_3DFACE, 0.9)),
        ("color_body", get_colour(wx.SYS_COLOUR_3DFACE)),
        ("color_body_1_1", get_colour(wx.SYS_COLOUR_3DFACE, 1.1)),
        ("color_body_1_3", get_colour(wx.SYS_COLOUR_3DFACE, 1.3)),
        ("color_body_1_5", get_colour(wx.SYS_COLOUR_3DFACE, 0)),
        ("color_body_1_8", get_colour(wx.SYS_COLOUR_3DFACE, 1.8)),
        ("color_higlight", get_colour(wx.SYS_COLOUR_3DHIGHLIGHT)),
        ("color_shadow", get_colour(wx.SYS_COLOUR_3DSHADOW)),
        ("color_background_0_5", get_colour(wx.SYS_COLOUR_3DFACE, 0.5)),
        ("color_background_0_8", get_colour(wx.SYS_COLOUR_3DFACE, 0.8)),
        ("color_background_0_9", get_colour(wx.SYS_COLOUR_3DFACE, 0.9)),
        ("color_background", get_colour(wx.SYS_COLOUR_3DFACE)),
        ("color_background_1_1", get_colour(wx.SYS_COLOUR_3DFACE, 1.1)),
        ("color_background_1_2", get_colour(wx.SYS_COLOUR_3DFACE, 1.2)),
        ("color_background_1_5", get_colour(wx.SYS_COLOUR_3DFACE, 1.5)),
        ("color_info", get_colour(wx.SYS_COLOUR_INFOBK, 1.5)),
    )


def create_desktop_shortcut(app_name, title=None, parameters=""):
    pytigon_init_path = os.path.abspath(pytigon.__file__)
    ico_path = pytigon_init_path.replace("__init__.py", "pytigon.ico")
    ptig_path = pytigon_init_path.replace("__init__.py", "ptig.py")

    if "python" in sys.executable and make_shortcut:
        make_shortcut(
            ptig_path + " " + app_name, name=title if title else app_name, icon=ico_path
        )


LAST_FOCUS_CTRL_IN_FORM = None


def find_focus_in_form():
    global LAST_FOCUS_CTRL_IN_FORM
    win_focus = wx.Window.FindFocus()
    win = win_focus
    while win:
        if win.__class__.__name__ == "SchForm":
            LAST_FOCUS_CTRL_IN_FORM = win_focus
            return win_focus
        win = win.GetParent()
    if LAST_FOCUS_CTRL_IN_FORM and (
        not hasattr(LAST_FOCUS_CTRL_IN_FORM, "parent")
        or not LAST_FOCUS_CTRL_IN_FORM.parent
        or (
            hasattr(LAST_FOCUS_CTRL_IN_FORM.parent, "closing")
            and LAST_FOCUS_CTRL_IN_FORM.parent.closing
        )
    ):
        LAST_FOCUS_CTRL_IN_FORM = None
        return None
    else:
        return LAST_FOCUS_CTRL_IN_FORM


def import_plugin(plugin_name, prj_name=None):
    cfg = get_main_paths()
    pytigon_cfg = [cfg["PYTIGON_PATH"], "appdata", "plugins"]
    data_path = cfg["DATA_PATH"]
    data_cfg = [data_path, "plugins"]
    prj_cfg = [cfg["PRJ_PATH"], prj_name, "applib"]
    prj_cfg_alt = [cfg["PRJ_PATH_ALT"], prj_name, "applib"]

    if prj_name:
        folders = [prj_cfg, prj_cfg_alt]
    else:
        folders = [pytigon_cfg, data_cfg]

    path = None
    for folder in folders:
        plugins_path = os.path.join(folder[0], *folder[1:])
        if prj_name:
            plugin_path = os.path.join(plugins_path, *plugin_name.split(".")[:-1])
        else:
            plugin_path = os.path.join(plugins_path, *plugin_name.split("."))
        if os.path.exists(plugin_path):
            path = plugins_path
            path2 = plugin_path
            break

    if not path:
        return None

    try:
        m = importlib.import_module(plugin_name, package=None)
        return m
    except:
        try:
            m = importlib.import_module(plugin_name, package=None)
            return m
        except:
            pass
    return None
