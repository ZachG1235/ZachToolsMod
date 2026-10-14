import tkinter as tk

class CustomCheckbutton(tk.Canvas):
    def __init__(
        self,
        parent,
        variable,
        command=None,
        size=24,
        bg=None,
        checked_color="#FF0000",
        check_color="white",
        border_color="#777777"
    ):
        self.variable = variable
        self.command = command
        self.size = size
        self.checked_color = checked_color
        self.check_color = check_color
        self.border_color = border_color

        if bg is None:
            bg = parent.cget("bg")

        super().__init__(
            parent,
            width=size + 4,
            height=size + 4,
            bg=bg,
            highlightthickness=0,
            bd=0,
            cursor="hand2"
        )

        self.bind("<Button-1>", self._toggle)
        self.bind("<space>", self._toggle)
        self.bind("<Return>", self._toggle)
        self.bind("<Enter>", self._on_hover)
        self.bind("<Leave>", self._on_leave)

        self._hovered = False
        self._draw()

    def _draw(self):
        self.delete("all")

        margin = 2
        x1, y1 = margin, margin
        x2, y2 = self.size + margin, self.size + margin

        checked = self.variable.get()

        self.create_rectangle(
            x1, y1, x2, y2,
            fill=self.checked_color if checked else self.cget("bg"),
            outline=self.checked_color if checked else self.border_color,
            width=2
        )

        if checked:
            # Draw a checkmark
            self.create_line(
                x1 + self.size * 0.20,
                y1 + self.size * 0.52,
                x1 + self.size * 0.43,
                y1 + self.size * 0.75,
                x1 + self.size * 0.82,
                y1 + self.size * 0.25,
                fill=self.check_color,
                width=max(2, self.size // 6),
                capstyle=tk.ROUND,
                joinstyle=tk.ROUND
            )

        if self._hovered:
            self.configure(cursor="hand2")

    def _toggle(self, event=None):
        self.variable.set(not self.variable.get())
        self._draw()

        if self.command:
            self.command()

    def _on_hover(self, event=None):
        self._hovered = True
        self._draw()

    def _on_leave(self, event=None):
        self._hovered = False
        self._draw()

    def refresh(self):
        """Redraw the checkbox if its variable changed elsewhere."""
        self._draw()