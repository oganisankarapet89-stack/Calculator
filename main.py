import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.storage.jsonstore import JsonStore
from kivy.uix.slider import Slider
from kivy.uix.label import Label

# ======================
# 💾 STORAGE
# ======================
store = JsonStore("settings.json")

# ======================
# 🎨 THEMES
# ======================
class Theme:
    dark = {"bg": (0,0,0,1), "text": (1,1,1,1), "btn": (0.15,0.15,0.15,0.9)}
    light = {"bg": (1,1,1,1), "text": (0,0,0,1), "btn": (0.9,0.9,0.9,0.9)}

BTN_RADIUS = [30]

# ======================
# 🍏 GLASS BUTTON
# ======================
class IOSButton(Button):
    def __init__(self, theme, bg_color, size_factor=1, **kwargs):
        super().__init__(**kwargs)

        self.theme = theme
        self.bg_color_val = bg_color
        self.size_factor = size_factor

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0,0,0,0)

        self.color = (1,1,1,1)
        self.font_size = 26 * size_factor

        with self.canvas.before:
            self.bg_color = Color(*bg_color)
            self.bg = RoundedRectangle(radius=BTN_RADIUS)

        self.bind(pos=self.update, size=self.update)
        self.bind(on_press=self.animate)

    def update(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def animate(self, *args):
        Animation(opacity=0.6, duration=0.05).start(self)

        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Context = PythonActivity.mActivity.getApplicationContext()
            vibrator = Context.getSystemService(Context.VIBRATOR_SERVICE)
            vibrator.vibrate(10)
        except:
            pass

    def update_style(self, theme, size_factor):
        self.color = theme["text"]
        self.font_size = 26 * size_factor
        self.bg_color.rgba = self.bg_color_val


# ======================
# 📟 CALCULATOR
# ======================
class Calculator(GridLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)

        self.app = app
        self.cols = 1
        self.spacing = 10
        self.padding = 10

        self.display = TextInput(
            font_size=50,
            readonly=True,
            halign="right",
            background_color=(0,0,0,0),
            foreground_color=app.theme["text"],
            size_hint=(1,0.25)
        )

        self.add_widget(self.display)

        buttons = [
            ["C","+/-","%","/"],
            ["7","8","9","*"],
            ["4","5","6","-"],
            ["1","2","3","+"],
            ["0",".","="]
        ]

        self.btns = []

        for row in buttons:
            row_layout = GridLayout(cols=len(row), spacing=8, size_hint=(1,1))

            for b in row:
                if b in "+-*/=":
                    color = (1,0.5,0,1)
                elif b == "C":
                    color = (0.6,0.6,0.6,1)
                else:
                    color = (0.2,0.2,0.2,1)

                btn = IOSButton(app.theme, color, app.size_factor, text=b)

                if b == "0":
                    btn.size_hint_x = 2

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
                expr = self.display.text.replace("×","*").replace("÷","/")
                self.display.text = str(eval(expr))
            except:
                self.display.text = "Error"
                Clock.schedule_once(lambda dt: self.clear(),1)

        elif t == "+/-":
            try:
                self.display.text = str(-float(self.display.text))
            except: pass

        elif t == "%":
            try:
                self.display.text = str(float(self.display.text)/100)
            except: pass

        else:
            self.display.text += t

    def clear(self):
        self.display.text = ""

    def update_style(self):
        self.display.foreground_color = self.app.theme["text"]
        self.display.font_size = 50 * self.app.size_factor

        for b in self.btns:
            b.update_style(self.app.theme, self.app.size_factor)


# ======================
# 💱 CONVERTER
# ======================
class Converter(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)

        self.app = app
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10

        self.input = TextInput(hint_text="USD", font_size=30)
        self.result = TextInput(readonly=True, font_size=30)

        btn = IOSButton(app.theme, (0,0.5,1,1), text="Convert")
        btn.bind(on_press=self.convert)

        self.add_widget(self.input)
        self.add_widget(btn)
        self.add_widget(self.result)

    def convert(self, instance):
        try:
            usd = float(self.input.text)
            self.result.text = f"EUR: {usd*0.92:.2f}\nRUB: {usd*92:.2f}"
        except:
            self.result.text = "Error"


# ======================
# ⚙️ SETTINGS
# ======================
class Settings(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)

        self.app = app
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 20

        self.add_widget(Label(text="UI Size"))
        slider = Slider(min=0.7, max=2, value=app.size_factor)
        slider.bind(value=self.change_size)

        btn = IOSButton(app.theme,(0.3,0.3,0.3,1), text="Switch Theme")
        btn.bind(on_press=self.change_theme)

        self.add_widget(slider)
        self.add_widget(btn)

    def change_size(self, instance, value):
        self.app.size_factor = value
        self.app.update_all()
        store.put("settings", size=value, theme=self.app.theme_name)

    def change_theme(self, instance):
        self.app.switch_theme()


# ======================
# 🧭 MAIN APP
# ======================
class MainApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        saved = store.get("settings") if store.exists("settings") else None
        self.size_factor = saved["size"] if saved else 1
        self.theme_name = saved["theme"] if saved else "dark"

        self.theme = Theme.dark if self.theme_name=="dark" else Theme.light
        Window.clearcolor = self.theme["bg"]

        self.orientation = "vertical"

        top = BoxLayout(size_hint=(1,0.1))

        self.tabs = {
            "calc": Button(text="Calculator"),
            "conv": Button(text="Converter"),
            "set": Button(text="Settings")
        }

        for name, btn in self.tabs.items():
            btn.bind(on_press=lambda x, n=name: self.show(n))
            top.add_widget(btn)

        self.add_widget(top)

        self.content = BoxLayout()

        self.calc = Calculator(self)
        self.conv = Converter(self)
        self.sett = Settings(self)

        self.screen = "calc"
        self.content.add_widget(self.calc)

        self.add_widget(self.content)

    def show(self, name):
        self.content.clear_widgets()

        if name=="calc":
            self.content.add_widget(self.calc)
        elif name=="conv":
            self.content.add_widget(self.conv)
        else:
            self.content.add_widget(self.sett)

    def switch_theme(self):
        self.theme_name = "light" if self.theme_name=="dark" else "dark"
        self.theme = Theme.light if self.theme_name=="light" else Theme.dark
        Window.clearcolor = self.theme["bg"]
        self.update_all()

    def update_all(self):
        self.calc.update_style()


# ======================
# 🚀 APP
# ======================
class GlassApp(App):
    icon = "icon.png"

    def build(self):
        return MainApp()


if __name__ == "__main__":
    GlassApp().run()