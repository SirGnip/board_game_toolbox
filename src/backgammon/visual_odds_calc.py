# First things, first. Import the wxPython package.
import wx


class BackgammonFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        margin = 10
        layout = wx.BoxSizer(wx.VERTICAL)
        grid_sizer = wx.GridSizer(cols=7)
        layout.Add(grid_sizer, 0, wx.EXPAND | wx.ALL, margin)

        self.ctrls = []

        # first header row
        row = []
        empty = wx.StaticText(self)
        grid_sizer.Add(empty, 1)
        row.append(empty)
        for col_idx in range(1, 7):
            lbl = wx.StaticText(self, label=f"{col_idx}")
            grid_sizer.Add(lbl)
            row.append(lbl)
        self.ctrls.append(row)

        # grid
        for row_idx in range(1, 7):
            row = []
            lbl = wx.StaticText(self, label=f"{row_idx}")
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
        layout.Add(self.odds, 0, wx.ALL, margin)

        # button
        clear_btn = wx.Button(self, label="Clear")
        clear_btn.Bind(wx.EVT_BUTTON, self.on_clear)
        layout.Add(clear_btn, 0, wx.ALL, margin)

        # window setup
        self.SetSizer(layout)
        layout.SetSizeHints(self)

        self.refresh_odds(None)

    def on_clear(self, _evt):
        print('clear')
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
