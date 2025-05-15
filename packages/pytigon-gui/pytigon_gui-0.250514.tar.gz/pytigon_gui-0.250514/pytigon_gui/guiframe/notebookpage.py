"""This module contains SchNotebookPage. It represent one tab window in SchNotebook. One SchNotebookPage can manage
multiple SchPage windows.
"""

import wx
from pytigon_gui.guiframe import page


class SchNotebookPage(wx.Window):
    """SchNotebookPage represent one tab pytigon applications"""

    def __init__(self, parent):
        """Constructor"""
        wx.Window.__init__(
            self,
            parent,
            style=wx.TAB_TRAVERSAL | wx.WANTS_CHARS,
            name="SchNotebookPage",
        )
        try:
            self.SetBackgroundStyle(wx.BG_STYLE_ERASE)
        except:
            self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self._start_pos = None
        self._start_pos_x_y_dx_dy = None
        self._last_x_y_dx_dy = None
        self._best_x_y_dx_dy = None
        self._layout_style = 0

        self.child_panels = []
        self.bestx = -1
        self.orient = None
        self.http = None
        self.reverse_style = True

        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_MOTION, self.on_move)
        self.Bind(wx.EVT_SET_FOCUS, self.on_set_focus)

        self.SetWindowStyleFlag(wx.WANTS_CHARS)

    def on_set_focus(self, evt):
        if self.get_page_count() > 0:
            self.get_page(-1).SetFocus()

    def get_app_http(self):
        """Returns  :class:`~pytigon_lib.schhttptools.httpclient.HttpClient` object connected to this object"""
        return self.http

    def on_erase_background(self, evt):
        if not wx.GetApp().GetTopWindow():
            return
        dc = wx.ClientDC(self)
        dc.Clear()
        margin = self.get_margins()
        if hasattr(wx.GetApp().GetTopWindow(), "desktop"):
            tabs_count = len(wx.GetApp().GetTopWindow().desktop._mgr.GetAllPanes())
            if (
                self.get_page_count()
                and tabs_count > 2
                or self.get_page_count() > 1
                or wx.GetApp().GetTopWindow().count_shown_panels(count_toolbars=False)
                > 1
                and self.get_page_count() > 0
            ):
                (dx, dy) = self.get_page(-1).GetSize()
                (x, y) = self.get_page(-1).GetPosition()
                x = x - margin / 2
                y = y - margin / 2
                dx = dx + margin
                dy = dy + margin
                if (
                    self.GetParent().active
                    and self.GetParent().GetCurrentPage() == self
                ):
                    col = wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHT)
                else:
                    col = wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVEBORDER)
                dc.SetPen(wx.Pen(col, margin))
                dc.DrawLine(int(x), int(y), int(x + dx), int(y))
                dc.DrawLine(int(x + dx), int(y), int(x + dx), int(y + dy))
                dc.DrawLine(int(x), int(y - margin / 2), int(x), int(y + dy))
                dc.DrawLine(int(x), int(y + dy), int(x + dx), int(y + dy))
                if self._layout_style > 0:
                    col = wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DSHADOW)
                    dc.SetPen(wx.Pen(col, 1))
                    if self._layout_style in (1, 3):
                        dc.DrawLine(
                            int(x - margin), int(y), int(x - margin), int(y + dy)
                        )
                        dc.DrawLine(
                            int(x - 5 * margin),
                            int(y),
                            int(x - 5 * margin),
                            int(y + dy),
                        )
                        for i in range(-4, 5, 2):
                            dc.DrawLine(
                                int(x - 5 * margin + 2),
                                int(y + dy / 2 + margin * i),
                                int((x - margin) - 1),
                                int(y + dy / 2 + margin * i),
                            )
                    if self._layout_style in (2, 3):
                        dc.DrawLine(
                            int(x), int(y - margin), int(x + dx), int(y - margin)
                        )
                        dc.DrawLine(
                            int(x),
                            int(y - 5 * margin),
                            int(x + dx),
                            int(y - 5 * margin),
                        )
                        for i in range(-4, 5, 2):
                            dc.DrawLine(
                                int(x + dx / 2 + margin * i),
                                int(y - 5 * margin + 2),
                                int(x + dx / 2 + margin * i),
                                int((y - margin) - 1),
                            )

    def on_left_down(self, event):
        self._start_pos = event.GetPosition()
        self._start_pos_x_y_dx_dy = self._last_x_y_dx_dy
        self.SetCursor(wx.Cursor(wx.CURSOR_SIZING))
        self.CaptureMouse()
        event.Skip()

    def on_left_up(self, event):
        if self._start_pos:
            self._start_pos = None
            self._start_pos_x_y_dx_dy = None
            self._best_x_y_dx_dy = None
            self.ReleaseMouse()
            self.SetCursor(wx.Cursor(wx.CURSOR_ARROW))
        event.Skip()

    def on_move(self, event):
        if self._start_pos and self._start_pos_x_y_dx_dy:
            pos = event.GetPosition()
            dx = pos[0] - self._start_pos[0]
            dy = pos[1] - self._start_pos[1]
            if self.reverse_style:
                dy = -1 * dy
            self._best_x_y_dx_dy = (
                self._start_pos_x_y_dx_dy[0] + dx,
                self._start_pos_x_y_dx_dy[1] + dy,
                self._start_pos_x_y_dx_dy[2],
                self._start_pos_x_y_dx_dy[3],
            )
            self._layout()
        event.Skip()

    def get_xy(self, size=None, page=-1):
        """get best point whitch divide window for place new SchPage window"""
        if size == None:
            size = self.GetSize()
        if self._best_x_y_dx_dy:
            return self._best_x_y_dx_dy
        else:
            (bestx, besty) = self.get_page(page).calculate_best_size()
            self.bestx = bestx
            self.besty = besty
        if bestx > size.GetWidth() - 20:
            x = size.GetWidth() / 10
        else:
            x = (size.GetWidth() - 2) - bestx
        if besty > size.GetHeight() - 20:
            y = size.GetHeight() / 10
        else:
            y = (size.GetHeight() - 2) - besty
        self._last_x_y_dx_dy = (x, y, size.GetWidth(), size.GetHeight())
        return self._last_x_y_dx_dy

    def get_margins(self):
        """get margin size between child windows"""
        return 2

    def _set_dimensions(self, page, x, y, width, height, dx, dy):
        if x > 0 and y > 0 and width >= 0 and height >= 0:
            if self.child_panels[-1].vertical_position:
                if self.child_panels[-1].vertical_position == "top":
                    page.SetSize(int(x), int(dy - height - y), int(width), int(height))
                else:
                    page.SetSize(int(x), int(y), int(width), int(height))
            else:
                if self.reverse_style:
                    page.SetSize(int(x), int(dy - height - y), int(width), int(height))
                else:
                    page.SetSize(int(x), int(y), int(width), int(height))

    def _layout(self, size=None):
        if self.get_page_count() > 0:
            count = self.get_page_count()
            margin = self.get_margins()
            if count == 0:
                pass
            if count == 1:
                self._layout_style = 0
                if not size:
                    size = self.GetSize()
                if size:
                    dx = size.GetWidth()
                    dy = size.GetHeight()
                self._set_dimensions(
                    self.get_page(0),
                    margin,
                    margin,
                    dx - 2 * margin,
                    dy - 2 * margin,
                    dx,
                    dy,
                )
            if count > 1:
                (x, y, dx, dy) = self.get_xy(size)
                if not self._best_x_y_dx_dy:
                    if self.bestx >= 0 and x > self.bestx:
                        x = self.bestx
                    else:
                        self.bestx = x
                else:
                    self._last_x_y_dx_dy = self._best_x_y_dx_dy
                if count == 2:
                    if (dx - x) * dy < 2 * ((dy - y) * dx):
                        self._layout_style = 1
                        self._set_dimensions(
                            self.get_page(0),
                            margin,
                            margin,
                            x - 2 * margin,
                            dy - 2 * margin,
                            dx,
                            dy,
                        )
                        self._set_dimensions(
                            self.get_page(1),
                            x + 5 * margin,
                            margin,
                            (dx - x) - 6 * margin,
                            dy - 2 * margin,
                            dx,
                            dy,
                        )
                    else:
                        self._layout_style = 2
                        self._set_dimensions(
                            self.get_page(0),
                            margin,
                            margin,
                            dx - 2 * margin,
                            y - 2 * margin,
                            dx,
                            dy,
                        )
                        self._set_dimensions(
                            self.get_page(1),
                            margin,
                            y + 5 * margin,
                            dx - 2 * margin,
                            (dy - y) - 6 * margin,
                            dx,
                            dy,
                        )
                if count > 2:
                    self._layout_style = 3
                    for i in range(0, count - 2):
                        self._set_dimensions(
                            self.get_page(i),
                            margin,
                            margin + (i * dy) / (count - 2),
                            x - 2 * margin,
                            dy / (count - 2) - 2 * margin,
                            dx,
                            dy,
                        )
                    self._set_dimensions(
                        self.get_page(-2),
                        x + margin,
                        margin,
                        (dx - x) - 2 * margin,
                        y - 2 * margin,
                        dx,
                        dy,
                    )
                    self._set_dimensions(
                        self.get_page(-1),
                        x + 5 * margin,
                        y + 5 * margin,
                        (dx - x) - 6 * margin,
                        (dy - y) - 6 * margin,
                        dx,
                        dy,
                    )
            self.Refresh()

    def get_page_count(self):
        """Get number of child schFrameForm objects"""
        return len(self.child_panels)

    def get_page(self, nr):
        """return child SchPage object

        Args:
            nr: number of page
        """
        return self.child_panels[nr]

    def add_page(self, page):
        """Append child SchPage object

        Args:
            page - SchPage object
        """
        if self.get_page_count() > 0:
            if page.disable_parent:
                self.get_page(-1).enable_forms(False)
        self.child_panels.append(page)
        self._layout()

    def on_size(self, event):
        size = event.GetSize()
        self.bestx = -1
        # self._layout(size)
        if size:
            wx.CallAfter(self._layout, size)
        event.Skip()

    def close_no_del(self, close_without_refresh=True):
        """Close last in hierarchy child form.

        Args:
            close_without_refresh - if True parent form of closing form shoud be refreshed,
            if False refresh is not needed.
        """
        ret = 0
        count = self.get_page_count()
        if count > 0:
            win = self.get_page(-1)
            if win.CanClose():
                del self.child_panels[-1]
                if count > 1:
                    self.get_page(-1).enable_forms(True)
                    self._layout()
                    self.get_page(-1).set_focus()
                    if close_without_refresh:
                        self.get_page(-1).signal("child_canceled", win)
                    else:
                        self.get_page(-1).signal("child_closed_with_ok", win)
                    ret = True
                else:
                    ret = False
                win.Destroy()
                return ret
            else:
                return True

    def close_child_page(self, close_without_refresh=True):
        """Close last in hierarchy child form. If there is only one form, besides closing form,
        this SchNotebookPage is also closed

        Args:
            close_without_refresh - if True parent form of closing form shoud be refreshed,
            if False refresh is not needed.
        """
        pages = self.GetParent()._tabs._pages
        for i in range(0, len(pages)):
            if pages[i].window == self:
                ret = self.close_no_del(close_without_refresh)
                if not ret:
                    self.GetParent().DeletePage(i)
                return ret
        return False

        # sel = self.GetParent().GetSelection()
        # if sel>=0:
        #    ret = self.close_no_del(close_without_refresh)
        #    if not ret:
        #        p = self.GetParent()
        #        p.DeletePage(sel)
        #    return ret
        # else:
        #    return False

    def on_child_form_ok(self):
        """function called by child SchForm object when OK is pushed and data in parent form shoud be refreshed"""
        self.close_child_page(False)

    def on_child_form_cancel(self):
        """function called by child SchForm object when Cancel is pushed and data in parent form doesn't need be refreshed"""
        self.close_child_page(True)

    # def select_tab(self):
    #    n = self.GetParent()
    #    src_idx = self.GetParent()._tabs.GetIdxFromWindow(self)
    #    sel = n.GetSelection()
    #    if sel != src_idx:
    #        n.SetSelection(src_idx)

    def activate_page(self):
        if self.get_page_count() > 0:
            self.get_page(-1).activate_page()
        else:
            self.SetFocus()

    def deactivate_page(self):
        if self.get_page_count() > 0:
            self.get_page(-1).deactivate_page()

    # def refresh_html(self):
    #    pass

    def new_child_page(
        self, address_or_parser, title="", parameters=None, callback=None
    ):
        """Append a new page

        Args:
            address_or_parser: can be: address of http page (str type) or
            :class:'~pytigon_lib.schparser.html_parsers.ShtmlParser'

            title - new page title
            parameters - dict
        """
        h = page.SchPage(self, address_or_parser, parameters)
        if self.get_page_count() > 0:
            h.parent_page = self.get_page(-1)
        nr = 0
        if h.header != None:
            nr = nr + 4
        if h.footer != None:
            nr = nr + 2
        if h.panel != None:
            nr = nr + 1
        if title and title != "":
            title2 = title
        else:
            title2 = h.get_title()
        self.add_page(h)  # , title2, True, nr)

        def init_page():
            nonlocal h, callback
            h.init_frame(callback)
            h.activate_page()
            wx.GetApp().GetTopWindow()._mgr.GetPane("desktop").Show()
            h.Update()
            # if callback:
            #    return callback(h)

        wx.CallAfter(init_page)
        return h

    def new_main_page(self, address_or_parser, title="", parameters=None, view_in=None):
        """Create new top

        Args:
            address_or_parser: can be: address of http page (str type) or
            :class:'~pytigon_lib.schparser.html_parsers.ShtmlParser'

            title - new page title

            parameters - dict

            view_in - can be: 'desktop', 'panel', 'header' or 'footer'
        """
        if view_in == None:
            pp = self.GetParent().GetParent().GetParent()._mgr.GetPane(self.GetParent())
            return (
                wx.GetApp()
                .GetTopWindow()
                .new_main_page(address_or_parser, title, parameters, pp.name)
            )
        else:
            return (
                wx.GetApp()
                .GetTopWindow()
                .new_main_page(address_or_parser, title, parameters, view_in)
            )
