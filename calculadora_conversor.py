"""
Calculadora
===========
Proyecto Final - Code in Place
Autor: Enrique

Conceptos de Python utilizados:
  - Variables y tipos (int, float, str, bool, dict, list)
  - Bucles (for al construir botones)
  - Funciones (cada acción es una función nombrada)
  - Listas y diccionarios (layout de botones, mapa de operadores)
"""

import tkinter as tk
from tkinter import font as tkfont

# ─────────────────────────────────────────────
#  CONSTANTES DE DISEÑO
# ─────────────────────────────────────────────
BG         = "#0f0f0f"
DISPLAY_BG = "#1a1a1a"
BTN_NUM    = "#1e1e1e"
BTN_OP     = "#2a2a2a"
BTN_EQUAL  = "#e8632a"
BTN_CLEAR  = "#333333"
TEXT_MAIN  = "#f0f0f0"
TEXT_DIM   = "#888888"
TEXT_ACC   = "#e8632a"
RADIUS     = 10    # radio de esquinas redondeadas en Canvas
PAD        = 6     # separación entre botones


# ─────────────────────────────────────────────
#  FUNCIÓN AUXILIAR: botón redondeado en Canvas
# ─────────────────────────────────────────────
def rounded_rect(canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int,
                 radius: int = RADIUS, **kwargs) -> int:
    """Dibuja un rectángulo con esquinas redondeadas en un Canvas."""
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


# ─────────────────────────────────────────────
#  CLASE PRINCIPAL: App
# ─────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora")
        self.resizable(False, False)
        self.configure(bg=BG)

        # ── Fuentes ──────────────────────────
        self.font_display = tkfont.Font(family="Courier New", size=28, weight="bold")
        self.font_expr    = tkfont.Font(family="Courier New", size=11)
        self.font_btn     = tkfont.Font(family="Courier New", size=14, weight="bold")
        self.font_small   = tkfont.Font(family="Courier New", size=10)

        # ── Estado de la calculadora ──────────
        self.expression: str   = ""    # expresión completa acumulada
        self.display_val: str  = "0"   # valor visible en pantalla
        self.just_evaluated: bool = False

        self._build_ui()

    # ─────────────────────────────────────────
    #  CONSTRUCCIÓN DE LA INTERFAZ
    # ─────────────────────────────────────────
    def _build_ui(self):
        """Construye la interfaz completa."""
        outer = tk.Frame(self, bg=BG, padx=16, pady=16)
        outer.pack()

        # TÍTULO
        tk.Label(outer, text="◈  CALCULADORA", bg=BG,
                 fg=TEXT_ACC, font=self.font_small).pack(anchor="w", pady=(0, 8))

        # DISPLAY Canvas
        disp_canvas = tk.Canvas(outer, width=340, height=90,
                                bg=BG, highlightthickness=0)
        disp_canvas.pack()
        rounded_rect(disp_canvas, 0, 0, 340, 90, radius=12,
                     fill=DISPLAY_BG, outline="")

        # Texto de expresión (arriba, pequeño)
        self.expr_text = disp_canvas.create_text(
            330, 18, anchor="e", text="", fill=TEXT_DIM, font=self.font_expr
        )
        # Texto del valor actual (grande)
        self.disp_text = disp_canvas.create_text(
            330, 62, anchor="e", text="0", fill=TEXT_MAIN, font=self.font_display
        )
        self.disp_canvas = disp_canvas

        # ── BOTONES ──────────────────────────
        # Layout: lista de listas de tuplas (etiqueta, tipo)
        btn_rows: list[list[tuple[str, str]]] = [
            [("C",  "clear"), ("±", "sign"), ("%", "percent"), ("÷", "op")],
            [("7",  "num"),   ("8", "num"),  ("9", "num"),     ("×", "op")],
            [("4",  "num"),   ("5", "num"),  ("6", "num"),     ("−", "op")],
            [("1",  "num"),   ("2", "num"),  ("3", "num"),     ("+", "op")],
            [("0",  "zero"),  (".", "dot"),  ("=", "equal")],
        ]

        btn_w, btn_h = 76, 56

        btn_frame = tk.Frame(outer, bg=BG)
        btn_frame.pack(pady=(8, 0))

        # Bucle for: construir cada botón dinámicamente
        for row_idx, row in enumerate(btn_rows):
            for col_idx, (label, kind) in enumerate(row):

                # Color según tipo de botón
                if kind == "equal":
                    color = BTN_EQUAL
                elif kind == "op":
                    color = BTN_OP
                elif kind == "clear":
                    color = BTN_CLEAR
                else:
                    color = BTN_NUM

                # El 0 ocupa el doble de ancho
                w = (btn_w * 2 + PAD) if kind == "zero" else btn_w

                canvas = tk.Canvas(btn_frame, width=w, height=btn_h,
                                   bg=BG, highlightthickness=0, cursor="hand2")
                canvas.grid(row=row_idx, column=col_idx,
                            padx=PAD // 2, pady=PAD // 2,
                            columnspan=2 if kind == "zero" else 1)

                rounded_rect(canvas, 2, 2, w - 2, btn_h - 2,
                             radius=RADIUS, fill=color, outline="")
                canvas.create_text(w // 2, btn_h // 2, text=label,
                                   fill=TEXT_MAIN, font=self.font_btn)

                # Eventos: clic y hover
                canvas.bind("<Button-1>",
                            lambda e, lbl=label, knd=kind: self._press(lbl, knd))
                canvas.bind("<Enter>",
                            lambda e, c=canvas, col=color: c.itemconfig(1, fill=self._lighten(col)))
                canvas.bind("<Leave>",
                            lambda e, c=canvas, col=color: c.itemconfig(1, fill=col))

    # ─────────────────────────────────────────
    #  LÓGICA DE LA CALCULADORA
    # ─────────────────────────────────────────
    def _press(self, label: str, kind: str):
        """Procesa la pulsación de un botón."""

        if kind == "clear":
            self.expression   = ""
            self.display_val  = "0"
            self.just_evaluated = False

        elif kind == "sign":
            if self.display_val not in ("0", "Error"):
                if self.display_val.startswith("-"):
                    self.display_val = self.display_val[1:]
                else:
                    self.display_val = "-" + self.display_val

        elif kind == "percent":
            try:
                val = float(self.display_val) / 100
                self.display_val = self._fmt(val)
            except ValueError:
                self.display_val = "Error"

        elif kind == "op":
            # Diccionario: símbolo visual → operador Python
            op_map: dict[str, str] = {"÷": "/", "×": "*", "−": "-", "+": "+"}
            if self.display_val != "Error":
                self.expression += self.display_val + op_map[label]
                self.display_val = ""
            self.just_evaluated = False

        elif kind == "equal":
            try:
                full_expr: str = self.expression + self.display_val
                result: float  = eval(full_expr)
                self.disp_canvas.itemconfig(self.expr_text, text=full_expr + " =")
                self.display_val    = self._fmt(result)
                self.expression     = ""
                self.just_evaluated = True
            except Exception:
                self.display_val = "Error"
                self.expression  = ""

        elif kind == "dot":
            if "." not in self.display_val:
                self.display_val = (self.display_val or "0") + "."

        else:  # num / zero
            if self.just_evaluated:
                self.display_val    = label
                self.just_evaluated = False
            elif self.display_val in ("0", "Error", ""):
                self.display_val = label
            else:
                self.display_val += label

        # Actualizar display
        if kind not in ("equal", "op"):
            self.disp_canvas.itemconfig(self.expr_text, text=self.expression)
        self.disp_canvas.itemconfig(
            self.disp_text,
            text=self.display_val if self.display_val else "0"
        )

    def _fmt(self, value: float) -> str:
        """Formatea un float: sin decimales si es entero, hasta 8 dígitos si no."""
        if value == int(value):
            return str(int(value))
        return f"{value:.8g}"

    def _lighten(self, hex_color: str) -> str:
        """Aclara un color hex para el efecto hover."""
        r = min(255, int(hex_color[1:3], 16) + 30)
        g = min(255, int(hex_color[3:5], 16) + 30)
        b = min(255, int(hex_color[5:7], 16) + 30)
        return f"#{r:02x}{g:02x}{b:02x}"


# ─────────────────────────────────────────────
#  PUNTO DE ENTRADA
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    app.mainloop()
