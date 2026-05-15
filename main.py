from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.animation import Animation

Window.clearcolor = (0.02, 0.02, 0.02, 1)


# 🧊 Кнопка с анимацией (iOS feel)
class AnimatedGlassButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.font_size = 30
        self.background_normal = ""
        self.background_color = (0.1, 1, 0.3, 0.12)
        self.color = (0, 1, 0, 1)
        self.size_hint = (1, 1)

    # ✨ анимация нажатия
    def on_press(self):
        anim = Animation(scale=0.92, duration=0.06) + Animation(scale=1, duration=0.12)
        anim.start(self)

    # фикс масштаба (Kivy не имеет scale по умолчанию — имитируем через size)
    scale = 1

    def on_scale(self, instance, value):
        self.size_hint = (value, value)


class Calculator(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1
        self.padding = 15
        self.spacing = 10

        # 🧊 экран
        self.display = TextInput(
            font_size=42,
            readonly=True,
            halign="right",
            background_color=(0, 0, 0, 0.35),
            foreground_color=(0, 1, 0, 1),
            cursor_color=(0, 1, 0, 1),
            size_hint=(1, 0.3)
        )
        self.add_widget(self.display)

        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["C", "0", "=", "+"]
        ]

        for row in buttons:
            row_layout = GridLayout(cols=4, spacing=10)

            for label in row:
                btn = AnimatedGlassButton(text=label)
                btn.bind(on_press=self.on_button)
                row_layout.add_widget(btn)

            self.add_widget(row_layout)

    def on_button(self, instance):
        t = instance.text

        if t == "C":
            self.display.text = ""

        elif t == "=":
            try:
                self.display.text = str(eval(self.display.text))
            except:
                self.display.text = "Error"
        else:
            self.display.text += t


class GlassApp(App):
    def build(self):
        return Calculator()


if __name__ == "__main__":
    GlassApp().run()
