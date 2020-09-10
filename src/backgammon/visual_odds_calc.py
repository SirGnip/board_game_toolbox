"""Mini-app that provides a visual representation of the possible dice rolls in backgammon and the odds"""
import wx

HEADER_BTN_SIZE = wx.Size(20, 20)
MARGIN = 10


class HeaderButton(wx.Button):
    """Header button shown at the start of the rows and columns"""
    def __init__(self, parent, label, hdr_type, hdr_idx):
        wx.Button.__init__(self, parent, label=label, size=HEADER_BTN_SIZE)
        self.hdr_type = hdr_type
        self.hdr_idx = hdr_idx
        self.Bind(wx.EVT_BUTTON, self.on_click)

    def on_click(self, _event):
        ctrls = self.GetParent().ctrls
        if self.hdr_type == "col":
            for row_idx in range(1, 7):
                ctrls[row_idx][self.hdr_idx].SetValue(True)
        else:
            for col_idx in range(1, 7):
                ctrls[self.hdr_idx][col_idx].SetValue(True)
        self.GetParent().refresh_odds(None)


class BackgammonFrame(wx.Frame):
    """Main window of backgammon odds calculator mini-app"""
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        layout = wx.BoxSizer(wx.VERTICAL)
        grid_sizer = wx.GridSizer(cols=7)
        layout.Add(grid_sizer, 0, wx.EXPAND | wx.ALL, MARGIN)

        self.ctrls = []

        # first header row
        row = []
        empty = wx.StaticText(self)
        grid_sizer.Add(empty, 1)
        row.append(empty)
        for col_idx in range(1, 7):
            lbl = HeaderButton(self, f"{col_idx}", "col", col_idx)
            grid_sizer.Add(lbl)
            row.append(lbl)
        self.ctrls.append(row)

        # grid
        for row_idx in range(1, 7):
            row = []
            lbl = HeaderButton(self, f"{row_idx}", "row", row_idx)
            grid_sizer.Add(lbl)
            row.append(lbl)
            for col_idx in range(1, 7):
                chk = wx.CheckBox(self)
                chk.Bind(wx.EVT_CHECKBOX, self.refresh_odds)
                grid_sizer.Add(chk)
                row.append(chk)
            self.ctrls.append(row)

        # text view
        self.odds = wx.StaticText(self)
        layout.Add(self.odds, 0, wx.ALL, MARGIN)

        # button
        clear_btn = wx.Button(self, label="Clear")
        clear_btn.Bind(wx.EVT_BUTTON, self.on_clear)
        layout.Add(clear_btn, 0, wx.ALL | wx.CENTER, MARGIN)

        # window setup
        self.SetSizer(layout)
        layout.SetSizeHints(self)

        self.refresh_odds(None)

    def on_clear(self, _evt):
        for col_idx in range(1, 7):
            for row_idx in range(1, 7):
                self.ctrls[row_idx][col_idx].SetValue(False)
        self.refresh_odds(None)

    def refresh_odds(self, _evt):
        count = 0
        for col_idx in range(1, 7):
            for row_idx in range(1, 7):
                if self.ctrls[row_idx][col_idx].IsChecked():
                    count += 1
        pct = (count / 36) * 100
        txt = f"Odds: {count}/36  {pct:.1f} %"
        self.odds.SetLabel(txt)


if __name__ == '__main__':
    app = wx.App()
    frm = BackgammonFrame(None, title="Backgammon Odds Calculator")
    frm.Show()
    app.MainLoop()
