from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle


# ======================
# 🎨 ТЕМЫ
# ======================
class Theme:
    dark = {
        "bg": (0.05, 0.05, 0.08, 1),
        "btn": (0.15, 0.15, 0.2, 0.65),
        "text": (1, 1, 1, 1)
    }

    neon = {
        "bg": (0.02, 0.02, 0.02, 1),
        "btn": (0, 1, 0.6, 0.18),
        "text": (0, 1, 0.6, 1)
    }

    light = {
        "bg": (0.95, 0.95, 0.97, 1),
        "btn": (1, 1, 1, 0.75),
        "text": (0.1, 0.1, 0.1, 1)
    }


# ======================
# 🧊 GLASS BUTTON (без “квадратов”)
# ======================
class GlassButton(Button):
    def __init__(self, theme, **kwargs):
        super().__init__(**kwargs)

        self.theme = theme

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)

        self.color = theme["text"]

        # ❌ убираем артефакты текста
        self.halign = "center"
        self.valign = "middle"
        self.padding = (0, 0)

        with self.canvas.before:
            self.bg_color = Color(*theme["btn"])
            self.bg = RoundedRectangle(radius=[22])

        self.bind(pos=self.update, size=self.update)
        self.bind(on_press=self.animate)

    def update(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def animate(self, *args):
        Animation(opacity=0.5, duration=0.05) + Animation(opacity=1, duration=0.15)


# ======================
# 📟 КАЛЬКУЛЯТОР
# ======================
class Calculator(GridLayout):
    def __init__(self, theme, **kwargs):
        super().__init__(**kwargs)

        self.theme = theme
        self.cols = 1
        self.spacing = 10
        self.padding = 10

        self.display = TextInput(
            font_size=40,
            readonly=True,
            background_color=(0, 0, 0, 0),
            foreground_color=theme["text"],
            size_hint=(1, 0.25)
        )

        self.add_widget(self.display)

        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["C", "0", "=", "+"]
        ]

        for row in buttons:
            row_layout = GridLayout(cols=4, size_hint=(1, None), height=75, spacing=8)

            for b in row:
                btn = GlassButton(text=b, theme=theme)
                btn.bind(on_press=self.press)
                row_layout.add_widget(btn)

            self.add_widget(row_layout)

    def press(self, instance):
        t = instance.text

        if t == "C":
            self.display.text = ""

        elif t == "=":
            try:
                self.display.text = str(eval(self.display.text))
                Clock.schedule_once(lambda dt: self.clear(), 2)
            except:
                self.display.text = "Error"
                Clock.schedule_once(lambda dt: self.clear(), 2)

        else:
            self.display.text += t

    def clear(self):
        self.display.text = ""


# ======================
# 💱 КОНВЕРТЕР
# ======================
class Currency(BoxLayout):
    def __init__(self, theme, **kwargs):
        super().__init__(**kwargs)

        self.theme = theme
        self.orientation = "vertical"
        self.spacing = 10
        self.padding = 10

        self.label = TextInput(
            text="Currency Converter",
            font_size=22,
            readonly=True,
            foreground_color=theme["text"],
            background_color=(0, 0, 0, 0),
            size_hint=(1, 0.15)
        )

        self.input = TextInput(
            hint_text="Enter USD",
            font_size=30,
            background_color=(0, 0, 0, 0),
            foreground_color=theme["text"]
        )

        self.result = TextInput(
            hint_text="Result",
            font_size=30,
            readonly=True,
            background_color=(0, 0, 0, 0),
            foreground_color=theme["text"]
        )

        btn = GlassButton(text="Convert USD → RUB", theme=theme)
        btn.bind(on_press=self.convert)

        self.add_widget(self.label)
        self.add_widget(self.input)
        self.add_widget(btn)
        self.add_widget(self.result)

    def convert(self, instance):
        try:
            usd = float(self.input.text)

            self.result.text = f"RUB: {usd * 92:.2f}\nEUR: {usd * 0.92:.2f}"

            Clock.schedule_once(lambda dt: self.clear(), 3)

        except:
            self.result.text = "Error"
            Clock.schedule_once(lambda dt: self.clear(), 2)

    def clear(self):
        self.input.text = ""
        self.result.text = ""


# ======================
# 🧭 MAIN APP
# ======================
class MainApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.theme = Theme.dark
        Window.clearcolor = self.theme["bg"]

        self.orientation = "vertical"

        # 🏷 название приложения
        self.title = TextInput(
            text="Karapetyan",
            font_size=32,
            readonly=True,
            size_hint=(1, 0.12),
            foreground_color=self.theme["text"],
            background_color=(0, 0, 0, 0)
        )

        self.add_widget(self.title)

        # 🧭 навигация
        nav = BoxLayout(size_hint=(1, 0.12), spacing=10, padding=10)

        self.btn_left = GlassButton(text="⬅ Calculator", theme=self.theme)
        self.btn_right = GlassButton(text="➡ Converter", theme=self.theme)
        self.btn_theme = GlassButton(text="🎨 Theme", theme=self.theme)

        self.btn_left.bind(on_press=self.prev)
        self.btn_right.bind(on_press=self.next)
        self.btn_theme.bind(on_press=self.switch_theme)

        nav.add_widget(self.btn_left)
        nav.add_widget(self.btn_right)
        nav.add_widget(self.btn_theme)

        self.add_widget(nav)

        # 📦 экраны
        self.content = BoxLayout()

        self.calc = Calculator(self.theme)
        self.conv = Currency(self.theme)

        self.screens = [self.calc, self.conv]
        self.index = 0

        self.content.add_widget(self.screens[self.index])
        self.add_widget(self.content)

    # ⬅️
    def prev(self, instance):
        self.index = (self.index - 1) % len(self.screens)
        self.switch()

    # ➡️
    def next(self, instance):
        self.index = (self.index + 1) % len(self.screens)
        self.switch()

    # 🔄 переключение
    def switch(self):
        self.content.clear_widgets()
        self.content.add_widget(self.screens[self.index])

    # 🎨 тема
    def switch_theme(self, instance):

        if self.theme == Theme.dark:
            self.theme = Theme.neon
        elif self.theme == Theme.neon:
            self.theme = Theme.light
        else:
            self.theme = Theme.dark

        Window.clearcolor = self.theme["bg"]
        self.update_theme(self.theme)

    # 🔧 обновление темы
    def update_theme(self, theme):

        self.calc.theme = theme
        self.conv.theme = theme

        for b in [self.btn_left, self.btn_right, self.btn_theme]:
            b.color = theme["text"]
            b.bg_color.rgba = theme["btn"]

        self.title.foreground_color = theme["text"]


# ======================
# 🚀 APP
# ======================
class GlassApp(App):
    icon = "icon.png"

    def build(self):
        return MainApp()


if __name__ == "__main__":
    GlassApp().run()
