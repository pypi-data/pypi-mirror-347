"""
Module contain helper classes for SELEC2 widget.
"""

import string
import wx

from pytigon_lib.schtools import schjson
from pytigon_gui.guictrl.basectrl import SchBaseCtrl

_ = wx.GetTranslation


class ListBoxNoFocus(wx.ListBox):
    def CanAcceptFocus(self):
        return False


class Select2Popup(wx.MiniFrame):
    def __init__(
        self,
        parent,
        id,
        title,
        pos,
        size,
        style,
        combo,
        field_id,
        url=None,
        minimum_input_length=2,
    ):
        from pytigon_gui.guiframe.page import SchPage

        self.combo = combo
        self.point = pos
        self.field_id = field_id
        self.url = url
        if minimum_input_length:
            self.minimum_input_length = minimum_input_length
        else:
            minimum_input_length = 0

        wx.MiniFrame.__init__(self, parent, id, title, pos, size, wx.RESIZE_BORDER)

        self.edit_ctrl = wx.TextCtrl(
            self, size=(440, -1), style=wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB
        )
        self.list_ctrl = ListBoxNoFocus(self, size=(440, 200), style=wx.LB_SINGLE)

        self.edit_ctrl.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.edit_ctrl.Bind(wx.EVT_TEXT_ENTER, self.on_enter)
        self.list_ctrl.Bind(wx.EVT_LISTBOX_DCLICK, self.on_enter)
        self.list_ctrl.Bind(wx.EVT_LISTBOX, self.on_enter)

        self.Bind(wx.EVT_ACTIVATE, self.on_activate)
        self.Bind(wx.EVT_TEXT, self.on_text)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.edit_ctrl)
        box.Add(self.list_ctrl, 1, wx.ALL | wx.GROW, 1)
        self.SetSizer(box)
        self.SetAutoLayout(True)
        self.Fit()

    def on_enter(self, event):
        id = self.list_ctrl.GetSelection()
        if id != wx.NOT_FOUND:
            self.Dismiss()
            item_id = self.list_ctrl.GetClientData(id)
            item_str = self.list_ctrl.GetString(id)
            self.combo.set_value(item_id, item_str)

    def on_activate(self, event):
        if not event.GetActive():
            self.Hide()
            self.combo.SetFocus()
        event.Skip()

    def on_key_down(self, event):
        if event.KeyCode == wx.WXK_ESCAPE:
            self.Dismiss()
        elif event.KeyCode == wx.WXK_DOWN or (
            event.AltDown() and event.KeyCode == ord("J")
        ):
            id = self.list_ctrl.GetSelection()
            if id != wx.NOT_FOUND:
                if id < self.list_ctrl.GetCount() - 1:
                    self.list_ctrl.SetSelection(id + 1)
        elif event.KeyCode == wx.WXK_UP or (
            event.AltDown() and event.KeyCode == ord("K")
        ):
            id = self.list_ctrl.GetSelection()
            if id != wx.NOT_FOUND:
                if id > 0:
                    self.list_ctrl.SetSelection(id - 1)
        elif event.KeyCode == wx.WXK_TAB:
            return self.on_enter(event)
        else:
            event.Skip()

    def on_text(self, event):
        event.Skip()
        s = event.GetString()
        if len(s) < self.minimum_input_length:
            return
        if self.url:
            base_url = self.url
        else:
            base_url = "/select2/fields/auto.json"
        url = base_url + "?term=%s&page=1&context=&field_id=%s" % (
            s,
            self.field_id,
        )
        http = wx.GetApp().get_http(self.combo)
        response = http.get(self, url)
        tab = schjson.loads(response.str())
        if not "err" in tab or (
            "err" in tab and (tab["err"] != "nil" or tab["err"] != None)
        ):
            self.list_ctrl.Clear()
            if len(tab["results"]) > 0:
                for pos in tab["results"]:
                    self.list_ctrl.Append(pos["text"], pos["id"])
                if s:
                    self.list_ctrl.SetSelection(0)

    def set_position(self, point):
        self.point = point

    def clear(self):
        self.edit_ctrl.ChangeValue("")
        self.list_ctrl.Clear()

    def Popup(self):
        self.Show()
        self.Move(self.point)

    def Dismiss(self):
        self.Hide()
        self.combo.SetFocus()

    def Hide(self):
        self.combo.on_popup_hidden()
        super().Hide()


class Select2Base(wx.ComboCtrl, SchBaseCtrl):
    """Base class for SELECT2 widget, server interface based on select2 javascript library: https://select2.github.io/"""

    def __init__(self, parent, **kwds):
        self.popup = None
        self.button1 = None
        self.button2 = None
        self._popup_shown = False

        SchBaseCtrl.__init__(self, parent, kwds)

        data = self.param["data"][0]["attrs"]
        if "multiple" in data:
            self.multiple = True
        else:
            self.multiple = False

        if "style" in kwds:
            kwds["style"] |= wx.TE_PROCESS_ENTER
        else:
            kwds["style"] = wx.TE_PROCESS_ENTER

        if "item_id" in self.param and self.param["item_id"] != "None":
            self.item_id = [
                int(self.param["item_id"]),
            ]
            self.item_str = [
                self.param["item_str"],
            ]
        else:
            self.item_id = [
                -1,
            ]
            self.item_str = [
                "",
            ]

        kwds["size"] = (438, -1)

        wx.ComboCtrl.__init__(self, parent, **kwds)

        if self.GetTextCtrl():
            self.GetTextCtrl().SetForegroundColour(wx.Colour(0, 0, 0))

        self.Bind(wx.EVT_CHAR, self.on_char)

        if self.item_str:
            if self.multiple:
                self.SetValue(self.item_str[0])
            else:
                self.SetValue(self.item_str[0])

        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down_base)

        self.GetParent().get_parent_page().register_signal(self, "return_new_row")
        self.GetParent().get_parent_page().register_signal(self, "return_updated_row")

    def return_updated_row(self, **argv):
        self.set_value(argv["id"], argv["title"])

    def return_new_row(self, **argv):
        self.set_value(argv["id"], argv["title"])

    def init(self, button1, button2):
        self.button1 = button1
        self.button2 = button2

    def on_key_down_base(self, event):
        if event.GetKeyCode() == wx.WXK_TAB:
            if event.ShiftDown():
                self.GetParent().GetParent().Navigate(self.GetParent(), True)
            else:
                self.GetParent().GetParent().Navigate(self.GetParent(), False)
        elif event.GetKeyCode() == wx.WXK_F2:
            self.button1.on_click(event)
        elif event.GetKeyCode() == wx.WXK_INSERT:
            self.button2.on_click(event)
        else:
            event.Skip()

    def set_value(self, item_id, item_str):
        """Set value of field

        Args:
            item_id - table row id
            item_str - string representation of table row
        """
        if self.multiple:
            if not item_id in self.item_id:
                self.item_id.append(item_id)
                self.item_str.append(item_str)
            self.SetValue("; ".join(self.item_str)[2:])
        else:
            self.item_id = [
                item_id,
            ]
            self.item_str = [
                item_str,
            ]
            self.SetValue(item_str)

        def _fun():
            self.SelectNone()
            self.SetInsertionPointEnd()

        wx.CallAfter(_fun)

    def on_char(self, event):
        try:
            c = chr(event.GetUnicodeKey())
            if c in string.printable:
                if not self._popup_shown:
                    self._on_button_click()
                self.popup.edit_ctrl.AppendText(c)
        except:
            pass
        if event.KeyCode in (wx.WXK_DELETE, wx.WXK_BACK):
            self.item_id = [
                -1,
            ]
            self.item_str = [
                "",
            ]
            self.Clear()

    def _on_button_click(self):
        if not self.popup:
            pos = self.GetScreenPosition()
            pos = (pos[0], pos[1] + self.GetSize()[1])
            field_id = None
            minimum_input_length = None
            url = None
            data = self.param["data"][0]["attrs"]
            if "data-field_id" in data:
                field_id = data["data-field_id"]
            if "data-minimum-input-length" in data:
                minimum_input_length = int(data["data-minimum-input-length"])
            if "data-ajax--url" in data:
                url = data["data-ajax--url"]

            if self.GetTextCtrl():
                self.popup = Select2Popup(
                    self.GetTextCtrl(),
                    -1,
                    _("Select item"),
                    pos=pos,
                    size=(450, 400),
                    style=wx.DEFAULT_DIALOG_STYLE,
                    combo=self,
                    url=url,
                    field_id=field_id,
                    minimum_input_length=minimum_input_length,
                )
            else:
                self.popup = Select2Popup(
                    self,
                    -1,
                    _("Select item"),
                    pos=pos,
                    size=(450, 400),
                    style=wx.DEFAULT_DIALOG_STYLE,
                    combo=self,
                    url=url,
                    field_id=field_id,
                    minimum_input_length=minimum_input_length,
                )
        self.popup.clear()

        pos = self.GetScreenPosition()
        pos = (pos[0], pos[1] + self.GetSize()[1])
        pos = [pos[0], pos[1]]

        screen_dx = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
        screen_dy = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)

        popup_size = self.popup.GetSize()

        if pos[0] + popup_size[0] > screen_dx:
            pos[0] = screen_dx - popup_size[0]
        if pos[1] + popup_size[1] > screen_dy:
            pos[1] = pos[1] - self.GetSize().GetHeight() - popup_size[1]

        self.popup.set_position(pos)
        self.popup.Popup()
        self._popup_shown = True

    def on_popup_hidden(self):
        self._popup_shown = False
        self.SetFocus()

    def GetValue(self):
        """Return field value - table row id"""
        if self.multiple:
            return self.item_id
        else:
            return self.item_id[0]

    def OnButtonClick(self):
        # self.SetValue("")
        ret = self._on_button_click()
        self.popup.edit_ctrl.SetValue("")
        wx.CallAfter(self.popup.edit_ctrl.SetFocus)
        return ret

    def DoSetPopupControl(self, popup):
        pass

    def Dismiss(self):
        if self.popup:
            self.popup.Close()
            self.popup = None
        self.SetFocus()
