from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock


Window.clearcolor = (0.02, 0.02, 0.02, 1)


# 🧊 Glass кнопка
class AnimatedGlassButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.font_size = 28
        self.background_normal = ""
        self.background_color = (1, 1, 1, 0.08)
        self.color = (0.2, 1, 0.5, 1)

        self.size_hint = (1, None)
        self.height = 55

        self.bold = True

    def on_press(self):
        anim = Animation(opacity=0.6, duration=0.05) + Animation(opacity=1, duration=0.1)
        anim.start(self)


class Calculator(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1
        self.padding = 15
        self.spacing = 10

        self.dark_mode = True

        # 📟 экран
        self.display = TextInput(
            font_size=42,
            readonly=True,
            halign="right",
            background_color=(0, 0, 0, 0.35),
            foreground_color=(0, 1, 0, 1),
            cursor_color=(0, 1, 0, 1),
            size_hint=(1, 0.25)
        )
        self.add_widget(self.display)

        # 🌗 кнопка темы
        theme_btn = Button(
            text="Toggle Theme",
            size_hint=(1, None),
            height=45,
            background_color=(0.2, 0.2, 0.2, 0.4),
            color=(1, 1, 1, 1)
        )
        theme_btn.bind(on_press=self.toggle_theme)
        self.add_widget(theme_btn)

        # 🔢 кнопки
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["C", "0", "=", "+"]
        ]

        for row in buttons:
            row_layout = GridLayout(
                cols=4,
                spacing=10,
                size_hint=(1, None),
                height=60
            )

            for label in row:
                btn = AnimatedGlassButton(text=label)
                btn.bind(on_press=self.on_button)
                row_layout.add_widget(btn)

            self.add_widget(row_layout)

    # 🧠 логика кнопок
    def on_button(self, instance):
        t = instance.text

        if t == "C":
            self.display.text = ""

        elif t == "=":
            try:
                result = str(eval(self.display.text))
                self.display.text = result

                Clock.schedule_once(self.clear_display, 1.2)

            except:
                self.display.text = "Error"
                Clock.schedule_once(self.clear_display, 1.2)

        else:
            self.display.text += t

    # 🧼 авто очистка
    def clear_display(self, dt):
        self.display.text = ""

    # 🌗 тема
    def toggle_theme(self, instance):
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            Window.clearcolor = (0.02, 0.02, 0.02, 1)
            self.display.foreground_color = (0, 1, 0, 1)
            self.display.background_color = (0, 0, 0, 0.35)

        else:
            Window.clearcolor = (0.95, 0.95, 0.95, 1)
            self.display.foreground_color = (0.1, 0.1, 0.1, 1)
            self.display.background_color = (1, 1, 1, 0.6)


# 📱 App
class GlassApp(App):
    icon = "icon.png"  # 👈 твоя иконка
    title = 'Karapetyan'

    def build(self):
        return Calculator()


if __name__ == "__main__":
    GlassApp().run()
