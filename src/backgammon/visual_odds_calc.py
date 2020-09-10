"""Mini-app that provides a visual representation of the possible dice rolls in backgammon and the odds"""
import wx

HEADER_BTN_SIZE = wx.Size(25, 25)
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


class RollTotalAutoButton(wx.Button):
    """Wrapper around Button that auto-checks rolls that total up to given value"""
    def __init__(self, parent, num):
        wx.Button.__init__(self, parent, label=f"#{num}", size=HEADER_BTN_SIZE)
        self.num = num

    def on_click(self, _event):
        ctrls = self.GetParent().ctrls
        for row_num in range(1, 7):
            for col_num in range(1, 7):
                if row_num + col_num == self.num:
                    ctrls[row_num][col_num].SetValue(True)
        self.GetParent().refresh_odds(None)


class GridCheckBox(wx.CheckBox):
    """Wrapper around the CheckBox to hold its row/column"""
    def __init__(self, parent, row_num, col_num):
        wx.CheckBox.__init__(self, parent)
        self.row_num = row_num
        self.col_num = col_num


class BackgammonFrame(wx.Frame):
    """Main window of backgammon odds calculator mini-app"""
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        main_layout = wx.BoxSizer(wx.VERTICAL)

        self.ctrls = []  # contains the button headers and grid of checkboxes

        # first header row of grid
        grid_sizer = wx.GridSizer(cols=7)
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
                chk = GridCheckBox(self, row_idx, col_idx)
                chk.Bind(wx.EVT_CHECKBOX, self.on_check_grid)
                grid_sizer.Add(chk)
                row.append(chk)
            self.ctrls.append(row)
        main_layout.Add(grid_sizer, 0, wx.EXPAND | wx.ALL, MARGIN)

        # quick number buttons
        quick_num_grid_sizer = wx.GridSizer(cols=6)
        for num in range(2, 13):
            btn = RollTotalAutoButton(self, num)
            btn.Bind(wx.EVT_BUTTON, btn.on_click)
            quick_num_grid_sizer.Add(btn)
        main_layout.Add(quick_num_grid_sizer, 0, wx.EXPAND)

        # text view of "odds"
        self.odds = wx.StaticText(self)
        main_layout.Add(self.odds, 0, wx.ALL, MARGIN)

        # button
        clear_btn = wx.Button(self, label="Clear")
        clear_btn.Bind(wx.EVT_BUTTON, self.on_clear)
        main_layout.Add(clear_btn, 0, wx.ALL | wx.CENTER, MARGIN)

        # window setup
        self.SetSizer(main_layout)
        main_layout.SetSizeHints(self)

        self.refresh_odds(None)

    def on_clear(self, _event):
        for row_idx in range(1, 7):
            for col_idx in range(1, 7):
                self.ctrls[row_idx][col_idx].SetValue(False)
        self.refresh_odds(None)

    def on_check_grid(self, event):
        """mirror the check to the other side of the grid"""
        chk = event.GetEventObject()
        self.ctrls[chk.col_num][chk.row_num].SetValue(True)
        self.refresh_odds(None)

    def refresh_odds(self, _event):
        """Refresh the odds output"""
        count = 0
        for row_idx in range(1, 7):
            for col_idx in range(1, 7):
                if self.ctrls[row_idx][col_idx].IsChecked():
                    count += 1
        pct = (count / 36) * 100
        txt = f"Odds: {count}/36  {pct:.1f} %"
        self.odds.SetLabel(txt)


if __name__ == '__main__':
    app = wx.App()
    frm = BackgammonFrame(None, title="Backgammon Visual Odds Calculator")
    frm.Show()
    app.MainLoop()
