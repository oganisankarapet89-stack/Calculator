import requests

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.storage.jsonstore import JsonStore


# ======================
# 💾 SAVE SETTINGS
# ======================
store = JsonStore("settings.json")


# ======================
# 🎨 THEMES
# ======================
THEMES = {

    "Dark": {
        "bg": (0.02, 0.02, 0.02, 1),
        "text": (1, 1, 1, 1),
        "num": (0.18, 0.18, 0.2, 0.95),
        "op": (0, 1, 0.45, 1),
        "top": (0.18, 0.18, 0.18, 1)
    },

    "Blue": {
        "bg": (0.05, 0.08, 0.15, 1),
        "text": (1, 1, 1, 1),
        "num": (0.15, 0.2, 0.35, 0.95),
        "op": (0, 1, 0.45, 1),
        "top": (0.2, 0.3, 0.45, 1)
    },

    "Green": {
        "bg": (0.03, 0.08, 0.03, 1),
        "text": (1, 1, 1, 1),
        "num": (0.1, 0.2, 0.1, 0.95),
        "op": (0, 1, 0.45, 1),
        "top": (0.15, 0.3, 0.15, 1)
    },

    "Purple": {
        "bg": (0.08, 0.03, 0.1, 1),
        "text": (1, 1, 1, 1),
        "num": (0.22, 0.15, 0.3, 0.95),
        "op": (0, 1, 0.45, 1),
        "top": (0.3, 0.2, 0.4, 1)
    }
}


Window.clearcolor = (0.02, 0.02, 0.02, 1)


# ======================
# 🍏 IOS BUTTON
# ======================
class IOSButton(Button):

    def __init__(self, bg_color, size_factor=1, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)

        self.color = (1, 1, 1, 1)

        self.bold = True

        self.font_size = 24 * size_factor

        self.size_hint_y = None

        self.height = max(
            58,
            70 * size_factor
        )

        with self.canvas.before:
            self.bg_color = Color(*bg_color)

            self.bg = RoundedRectangle(
                radius=[40]
            )

        self.bind(
            pos=self.update_graphics,
            size=self.update_graphics
        )

    def update_graphics(self, *args):

        self.bg.pos = self.pos
        self.bg.size = self.size

    def on_press(self):

        Animation(
            opacity=0.65,
            duration=0.05
        ).start(self)

    def on_release(self):

        Animation(
            opacity=1,
            duration=0.08
        ).start(self)

    def update_theme(self, color, text, size_factor):

        self.bg_color.rgba = color

        self.color = text

        self.font_size = 24 * size_factor

        self.height = max(
            58,
            70 * size_factor
        )


# ======================
# 📟 CALCULATOR
# ======================
class Calculator(BoxLayout):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)

        self.app = app

        self.orientation = "vertical"

        self.spacing = 10
        self.padding = 10

        self.history = []

        self.buttons = []

        # ======================
        # 📟 DISPLAY
        # ======================
        self.display = TextInput(

            readonly=True,

            multiline=False,

            halign="right",

            background_color=(0, 0, 0, 0),

            foreground_color=app.theme["text"],

            font_size=46 * app.size_factor,

            size_hint=(1, 0.15)
        )

        self.add_widget(self.display)

        # ======================
        # 🔢 BUTTONS
        # ======================
        buttons = [

            ["C", "+/-", "%", "/"],

            ["7", "8", "9", "*"],

            ["4", "5", "6", "-"],

            ["1", "2", "3", "+"],

            ["0", ".", "="]
        ]

        for row in buttons:

            row_layout = GridLayout(

                cols=len(row),

                spacing=max(
                    4,
                    10 * app.size_factor
                ),

                size_hint=(1, None),

                height=max(
                    70,
                    95 * app.size_factor
                )
            )

            for text in row:

                if text in ["+", "-", "*", "/", "="]:
                    color = app.theme["op"]

                elif text == "C":
                    color = (0.65, 0.65, 0.65, 1)

                else:
                    color = app.theme["num"]

                btn = IOSButton(
                    text=text,
                    bg_color=color,
                    size_factor=app.size_factor
                )

                if text == "0":
                    btn.size_hint_x = 2

                btn.bind(
                    on_press=self.on_button
                )

                self.buttons.append(btn)

                row_layout.add_widget(btn)

            self.add_widget(row_layout)

    # ======================
    # 🧠 BUTTON LOGIC
    # ======================
    def on_button(self, instance):

        t = instance.text

        if t == "C":

            self.display.text = ""

        elif t == "=":

            try:

                expression = self.display.text

                result = str(eval(expression))

                self.history.append(
                    f"{expression} = {result}"
                )

                self.display.text = result

                Clock.schedule_once(
                    self.clear,
                    1.5
                )

            except:

                self.display.text = "Error"

                Clock.schedule_once(
                    self.clear,
                    1
                )

        elif t == "+/-":

            try:

                self.display.text = str(
                    -float(self.display.text)
                )

            except:
                pass

        elif t == "%":

            try:

                self.display.text = str(
                    float(self.display.text) / 100
                )

            except:
                pass

        else:

            self.display.text += t

    def clear(self, dt):

        self.display.text = ""

    # ======================
    # 🎨 UPDATE THEME
    # ======================
    def update_theme(self):

        self.display.foreground_color = (
            self.app.theme["text"]
        )

        self.display.font_size = (
            46 * self.app.size_factor
        )

        for btn in self.buttons:

            if btn.text in [
                "+", "-", "*", "/", "="
            ]:
                color = self.app.theme["op"]

            elif btn.text == "C":
                color = (0.65, 0.65, 0.65, 1)

            else:
                color = self.app.theme["num"]

            btn.update_theme(
                color,
                self.app.theme["text"],
                self.app.size_factor
            )


# ======================
# 💱 CONVERTER
# ======================
class Converter(BoxLayout):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)

        self.app = app

        self.orientation = "vertical"

        self.spacing = 12
        self.padding = 10

        self.input = TextInput(

            hint_text="USD",

            multiline=False,

            font_size=34 * app.size_factor,

            size_hint=(1, 0.15)
        )

        self.result = TextInput(

            readonly=True,

            font_size=32 * app.size_factor,

            background_color=(0, 0, 0, 0),

            foreground_color=app.theme["text"]
        )

        self.button = IOSButton(

            text="Convert",

            bg_color=app.theme["op"],

            size_factor=app.size_factor
        )

        self.button.bind(
            on_press=self.convert
        )

        self.add_widget(self.input)
        self.add_widget(self.button)
        self.add_widget(self.result)

    # ======================
    # 🌍 REAL USD RATE
    # ======================
    def convert(self, instance):

        try:

            usd = float(self.input.text)

            data = requests.get(
                "https://open.er-api.com/v6/latest/USD"
            ).json()

            rub_rate = data["rates"]["RUB"]

            eur_rate = data["rates"]["EUR"]

            rub = usd * rub_rate

            eur = usd * eur_rate

            self.result.text = (
                f"EUR: {eur:.2f}\n"
                f"RUB: {rub:.2f}"
            )

        except:

            self.result.text = "Connection Error"

    def update_theme(self):

        self.result.foreground_color = (
            self.app.theme["text"]
        )

        self.button.update_theme(

            self.app.theme["op"],

            self.app.theme["text"],

            self.app.size_factor
        )


# ======================
# 📜 HISTORY
# ======================
class History(BoxLayout):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)

        self.app = app

        self.orientation = "vertical"

        self.spacing = 10
        self.padding = 10

        self.history_box = TextInput(

            readonly=True,

            font_size=22,

            background_color=(0, 0, 0, 0),

            foreground_color=app.theme["text"]
        )

        clear_btn = IOSButton(

            text="Clear History",

            bg_color=(1, 0, 0, 1),

            size_factor=app.size_factor
        )

        clear_btn.bind(
            on_press=self.clear_history
        )

        self.add_widget(clear_btn)
        self.add_widget(self.history_box)

    def update_history(self):

        history = self.app.calculator.history

        self.history_box.text = (
            "\n".join(history[::-1])
        )

    def clear_history(self, instance):

        self.app.calculator.history.clear()

        self.update_history()

    def update_theme(self):

        self.history_box.foreground_color = (
            self.app.theme["text"]
        )


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

        # ======================
        # 📏 BUTTON SIZE
        # ======================
        size_label = Label(

            text="Button Size",

            color=app.theme["text"],

            size_hint=(1, 0.1)
        )

        self.slider = Slider(

            min=0.8,

            max=1.4,

            value=app.size_factor
        )

        self.slider.bind(
            value=self.change_size
        )

        self.add_widget(size_label)
        self.add_widget(self.slider)

        # ======================
        # 🎨 THEMES
        # ======================
        theme_label = Label(

            text="Themes",

            color=app.theme["text"],

            size_hint=(1, 0.1)
        )

        self.add_widget(theme_label)

        for theme_name in THEMES.keys():

            btn = IOSButton(

                text=theme_name,

                bg_color=THEMES[theme_name]["top"],

                size_factor=app.size_factor
            )

            btn.bind(

                on_press=lambda instance,
                name=theme_name:
                self.change_theme(name)
            )

            self.add_widget(btn)

    def change_size(self, instance, value):

        self.app.size_factor = value

        store.put(

            "settings",

            size=value,

            theme=self.app.theme_name
        )

        self.app.update_all()

    def change_theme(self, theme_name):

        self.app.theme_name = theme_name

        self.app.theme = THEMES[theme_name]

        Window.clearcolor = (
            self.app.theme["bg"]
        )

        store.put(

            "settings",

            size=self.app.size_factor,

            theme=theme_name
        )

        self.app.update_all()


# ======================
# 📱 MAIN APP
# ======================
class MainApp(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = "vertical"

        # ======================
        # 💾 LOAD SETTINGS
        # ======================
        if store.exists("settings"):

            data = store.get("settings")

            self.size_factor = data["size"]

            self.theme_name = data["theme"]

        else:

            self.size_factor = 1

            self.theme_name = "Dark"

        # 🔥 PROTECTION
        if self.theme_name not in THEMES:
            self.theme_name = "Dark"

        self.theme = THEMES[self.theme_name]

        Window.clearcolor = self.theme["bg"]

        # ======================
        # 🍏 TOP MENU
        # ======================
        top = GridLayout(

            cols=4,

            spacing=6,

            padding=6,

            size_hint=(1, 0.065)
        )

        self.calc_btn = IOSButton(

            text="Calculator",

            bg_color=self.theme["top"],

            size_factor=0.72
        )

        self.conv_btn = IOSButton(

            text="Converter",

            bg_color=self.theme["top"],

            size_factor=0.72
        )

        self.hist_btn = IOSButton(

            text="History",

            bg_color=self.theme["top"],

            size_factor=0.72
        )

        self.set_btn = IOSButton(

            text="Settings",

            bg_color=self.theme["top"],

            size_factor=0.72
        )

        self.calc_btn.bind(
            on_press=lambda x:
            self.show("calc")
        )

        self.conv_btn.bind(
            on_press=lambda x:
            self.show("conv")
        )

        self.hist_btn.bind(
            on_press=lambda x:
            self.show("hist")
        )

        self.set_btn.bind(
            on_press=lambda x:
            self.show("set")
        )

        top.add_widget(self.calc_btn)
        top.add_widget(self.conv_btn)
        top.add_widget(self.hist_btn)
        top.add_widget(self.set_btn)

        self.add_widget(top)

        # ======================
        # 📦 CONTENT
        # ======================
        self.content = BoxLayout()

        self.calculator = Calculator(self)

        self.converter = Converter(self)

        self.history_screen = History(self)

        self.settings = Settings(self)

        self.content.add_widget(
            self.calculator
        )

        self.add_widget(self.content)

    # ======================
    # 📱 SWITCH SCREENS
    # ======================
    def show(self, screen):

        self.content.clear_widgets()

        if screen == "calc":

            self.content.add_widget(
                self.calculator
            )

        elif screen == "conv":

            self.content.add_widget(
                self.converter
            )

        elif screen == "hist":

            self.history_screen.update_history()

            self.content.add_widget(
                self.history_screen
            )

        elif screen == "set":

            self.content.add_widget(
                self.settings
            )

    # ======================
    # 🎨 UPDATE ALL
    # ======================
    def update_all(self):

        Window.clearcolor = (
            self.theme["bg"]
        )

        self.calculator.update_theme()

        self.converter.update_theme()

        self.history_screen.update_theme()

        buttons = [

            self.calc_btn,

            self.conv_btn,

            self.hist_btn,

            self.set_btn
        ]

        for btn in buttons:

            btn.update_theme(

                self.theme["top"],

                self.theme["text"],

                0.72
            )


# ======================
# 🚀 APP
# ======================
class GlassCalculatorApp(App):

    title = "Karapetyan Calculator"

    icon = "icon.png"

    def build(self):
        return MainApp()


if __name__ == "__main__":
    GlassCalculatorApp().run()