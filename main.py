import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.storage.jsonstore import JsonStore


# ======================
# 💾 STORAGE
# ======================
store = JsonStore("settings.json")

# ======================
# 💊 GLOBAL STYLE
# ======================
BTN_RADIUS = [25]


# ======================
# 🎨 THEMES
# ======================
class Theme:
    dark = {"bg": (0.05, 0.05, 0.08, 1), "btn": (0.15, 0.15, 0.2, 0.7), "text": (1, 1, 1, 1)}
    neon = {"bg": (0.02, 0.02, 0.02, 1), "btn": (0, 1, 0.6, 0.2), "text": (0, 1, 0.6, 1)}


# ======================
# 🧊 GLASS BUTTON (ALL ROUNDED)
# ======================
class GlassButton(Button):
    def __init__(self, theme, size_factor=1.0, **kwargs):
        super().__init__(**kwargs)

        self.theme = theme
        self.size_factor = size_factor

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = theme["text"]

        self.font_size = 20 * size_factor
        self.height = 60 * size_factor

        with self.canvas.before:
            self.bg_color = Color(*theme["btn"])
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=BTN_RADIUS)

        self.bind(pos=self.update, size=self.update)
        self.bind(on_press=self.animate)

    def update(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.bg.radius = BTN_RADIUS

    def animate(self, *args):
        Animation(opacity=0.6, duration=0.05) + Animation(opacity=1, duration=0.15)

    def update_style(self, theme, size_factor):
        self.theme = theme
        self.size_factor = size_factor
        self.color = theme["text"]
        self.font_size = 20 * size_factor
        self.bg_color.rgba = theme["btn"]


# ======================
# 📟 CALCULATOR
# ======================
class Calculator(GridLayout):
    def __init__(self, theme, size_factor=1.0, **kwargs):
        super().__init__(**kwargs)

        self.theme = theme
        self.size_factor = size_factor

        self.cols = 1
        self.spacing = 10
        self.padding = 10

        self.display = TextInput(
            font_size=40 * size_factor,
            readonly=True,
            background_color=(0, 0, 0, 0),
            foreground_color=theme["text"],
            padding=(15, 15),
            size_hint=(1, 0.25)
        )

        self.add_widget(self.display)

        self.btns = []

        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["C", "0", "=", "+"]
        ]

        for row in buttons:
            row_layout = GridLayout(
                cols=4,
                size_hint=(1, None),
                height=70 * size_factor,
                spacing=8
            )

            for b in row:
                btn = GlassButton(text=b, theme=theme, size_factor=size_factor)
                btn.bind(on_press=self.press)
                self.btns.append(btn)
                row_layout.add_widget(btn)

            self.add_widget(row_layout)

    def press(self, instance):
        t = instance.text

        if t == "C":
            self.display.text = ""
        elif t == "=":
            try:
                self.display.text = str(eval(self.display.text))
            except:
                self.display.text = "Error"
                Clock.schedule_once(lambda dt: self.clear(), 2)
        else:
            self.display.text += t

    def clear(self):
        self.display.text = ""

    def update_style(self, theme, size_factor):
        self.theme = theme
        self.size_factor = size_factor

        self.display.foreground_color = theme["text"]
        self.display.font_size = 40 * size_factor

        for b in self.btns:
            b.update_style(theme, size_factor)


# ======================
# 💱 CONVERTER
# ======================
class Currency(BoxLayout):
    def __init__(self, theme, size_factor=1.0, **kwargs):
        super().__init__(**kwargs)

        self.theme = theme
        self.size_factor = size_factor

        self.orientation = "vertical"
        self.spacing = 10
        self.padding = 10

        self.input = TextInput(
            hint_text="USD",
            font_size=30 * size_factor,
            foreground_color=theme["text"],
            background_color=(0, 0, 0, 0),
            padding=(15, 15)
        )

        self.result = TextInput(
            hint_text="Result",
            readonly=True,
            font_size=30 * size_factor,
            foreground_color=theme["text"],
            background_color=(0, 0, 0, 0),
            padding=(15, 15)
        )

        self.btn = GlassButton(text="Convert", theme=theme, size_factor=size_factor)
        self.btn.bind(on_press=self.convert)

        self.add_widget(self.input)
        self.add_widget(self.btn)
        self.add_widget(self.result)

    def convert(self, instance):
        try:
            usd = float(self.input.text)
            self.result.text = f"RUB: {usd * 92:.2f}\nEUR: {usd * 0.92:.2f}"
        except:
            self.result.text = "Error"

    def update_style(self, theme, size_factor):
        self.theme = theme
        self.size_factor = size_factor

        self.input.font_size = 30 * size_factor
        self.result.font_size = 30 * size_factor

        self.input.foreground_color = theme["text"]
        self.result.foreground_color = theme["text"]

        self.btn.update_style(theme, size_factor)


# ======================
# ⚙️ SETTINGS
# ======================
class Settings(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)

        self.app = app
        self.orientation = "vertical"
        self.spacing = 20
        self.padding = 20

        self.label = Label(text="Settings", font_size=28)

        self.slider = Slider(min=0.7, max=2.0, value=app.size_factor)
        self.slider.bind(value=self.change_size)

        self.theme_btn = GlassButton(text="Switch Theme", theme=app.theme, size_factor=app.size_factor)
        self.theme_btn.bind(on_press=self.change_theme)

        self.add_widget(self.label)
        self.add_widget(self.slider)
        self.add_widget(self.theme_btn)

    def change_size(self, instance, value):
        self.app.size_factor = value
        self.app.update_all()
        store.put("settings", size=value, theme=self.app.theme_name)

    def change_theme(self, instance):
        self.app.switch_theme()


# ======================
# 🧭 MAIN APP (iOS STYLE)
# ======================
class MainApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # load settings
        saved = store.get("settings") if store.exists("settings") else None
        self.size_factor = saved["size"] if saved else 1.0
        self.theme_name = saved["theme"] if saved else "dark"

        self.theme = Theme.dark if self.theme_name == "dark" else Theme.neon
        Window.clearcolor = self.theme["bg"]

        self.orientation = "vertical"

        # ======================
        # 🍏 TOP TABS (iOS STYLE)
        # ======================
        top = BoxLayout(size_hint=(1, 0.12), padding=10, spacing=10)

        self.btn_calc = Button(text="⌨ Calculator")
        self.btn_conv = Button(text="💱 Converter")
        self.btn_set = Button(text="⚙ Settings")

        self.tabs = {
            "calc": self.btn_calc,
            "conv": self.btn_conv,
            "settings": self.btn_set
        }

        for b in self.tabs.values():
            b.background_normal = ""
            b.background_down = ""
            b.background_color = (0, 0, 0, 0)
            b.color = self.theme["text"]

        self.btn_calc.bind(on_press=lambda x: self.show("calc"))
        self.btn_conv.bind(on_press=lambda x: self.show("conv"))
        self.btn_set.bind(on_press=lambda x: self.show("settings"))

        top.add_widget(self.btn_calc)
        top.add_widget(self.btn_conv)
        top.add_widget(self.btn_set)

        self.add_widget(top)

        # ======================
        # 📦 CONTENT
        # ======================
        self.content = BoxLayout()

        self.calc = Calculator(self.theme, self.size_factor)
        self.conv = Currency(self.theme, self.size_factor)
        self.settings = Settings(self)

        self.screen = "calc"
        self.content.add_widget(self.calc)

        self.add_widget(self.content)

        self.update_tabs()

    # ======================
    # 🔄 NAV
    # ======================
    def show(self, name):
        self.content.clear_widgets()

        if name == "calc":
            self.content.add_widget(self.calc)
        elif name == "conv":
            self.content.add_widget(self.conv)
        else:
            self.content.add_widget(self.settings)

        self.screen = name
        self.update_tabs()

    # ======================
    # 💊 TAB STYLE
    # ======================
    def update_tabs(self):
        active = (0, 0.6, 1, 0.25)

        for name, btn in self.tabs.items():
            if self.screen == name:
                btn.background_color = active
            else:
                btn.background_color = (0, 0, 0, 0)

            btn.color = self.theme["text"]

    # ======================
    # 🎨 THEME
    # ======================
    def switch_theme(self):
        self.theme_name = "neon" if self.theme_name == "dark" else "dark"
        self.theme = Theme.neon if self.theme_name == "neon" else Theme.dark

        Window.clearcolor = self.theme["bg"]
        self.update_all()

        store.put("settings", size=self.size_factor, theme=self.theme_name)

    # ======================
    # 🔧 UPDATE UI
    # ======================
    def update_all(self):
        self.calc.update_style(self.theme, self.size_factor)
        self.conv.update_style(self.theme, self.size_factor)


# ======================
# 🚀 APP
# ======================
class GlassApp(App):
    icon = "icon.png"

    def build(self):
        return MainApp()


if __name__ == "__main__":
    GlassApp().run()