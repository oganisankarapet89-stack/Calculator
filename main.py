import requests
import random
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle, Rectangle, Ellipse
from kivy.storage.jsonstore import JsonStore
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, BooleanProperty
from kivy.utils import platform
from kivy.uix.floatlayout import FloatLayout

# ======================
# 📱 МОБИЛЬНЫЕ НАСТРОЙКИ
# ======================
IS_MOBILE = (platform == 'android' or platform == 'ios')

Window.clearcolor = (0, 0, 0, 1)
Window.size = (400, 700)

# ======================
# 💾 SAVE SETTINGS
# ======================
store = JsonStore("settings.json")

# ======================
# 🎨 ТЕМЫ
# ======================
THEMES = {
    "Dark": {
        "bg": (0, 0, 0, 1),
        "text": (1, 1, 1, 1),
        "num": (0.18, 0.18, 0.2, 0.95),
        "op": (1, 0.55, 0, 1),
        "top": (0.25, 0.25, 0.25, 1),
        "button_radius": 35
    },
    "Blue": {
        "bg": (0.05, 0.08, 0.15, 1),
        "text": (1, 1, 1, 1),
        "num": (0.15, 0.2, 0.35, 0.95),
        "op": (0, 0.6, 1, 1),
        "top": (0.2, 0.3, 0.45, 1),
        "button_radius": 30
    },
    "Green": {
        "bg": (0.03, 0.08, 0.03, 1),
        "text": (1, 1, 1, 1),
        "num": (0.1, 0.2, 0.1, 0.95),
        "op": (0, 1, 0.5, 1),
        "top": (0.15, 0.3, 0.15, 1),
        "button_radius": 40
    },
    "Purple": {
        "bg": (0.08, 0.03, 0.1, 1),
        "text": (1, 1, 1, 1),
        "num": (0.22, 0.15, 0.3, 0.95),
        "op": (0.8, 0.3, 1, 1),
        "top": (0.3, 0.2, 0.4, 1),
        "button_radius": 25
    },
    "Red": {
        "bg": (0.15, 0.05, 0.05, 1),
        "text": (1, 1, 1, 1),
        "num": (0.4, 0.1, 0.1, 0.95),
        "op": (1, 0.3, 0.1, 1),
        "top": (0.5, 0.1, 0.1, 1),
        "button_radius": 35
    },
    "Orange": {
        "bg": (0.15, 0.08, 0.03, 1),
        "text": (1, 1, 1, 1),
        "num": (0.4, 0.2, 0.05, 0.95),
        "op": (1, 0.6, 0, 1),
        "top": (0.5, 0.25, 0.05, 1),
        "button_radius": 30
    },
    "Pink": {
        "bg": (0.15, 0.05, 0.12, 1),
        "text": (1, 1, 1, 1),
        "num": (0.4, 0.1, 0.3, 0.95),
        "op": (1, 0.4, 0.7, 1),
        "top": (0.5, 0.15, 0.35, 1),
        "button_radius": 40
    }
}


# ======================
# 🦕 DINO GAME (ПЕРЕСОЗДАЁТСЯ ПРИ РЕСТАРТЕ)
# ======================
class DinoGame(Widget):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.size_hint = (1, 1)

        # Загружаем рекорд
        if store.exists("game_stats"):
            data = store.get("game_stats")
            self.high_score = data.get("high_score", 0)
        else:
            self.high_score = 0

        # Игровые переменные
        self.is_running = False
        self.score = 0
        self.dino_y = 0
        self.dino_velocity = 0
        self.gravity = -800
        self.jump_strength = 300
        self.obstacles = []
        self.game_speed = 200
        self.obstacle_timer = 0

        # Размеры
        self.dino_size = (35, 35)
        self.dino_x = 60
        self.ground_y = 80
        self.dino_on_ground = True

        # Управление
        if IS_MOBILE:
            self.bind(on_touch_down=self.on_touch_down)
        else:
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_key_down)

        self.game_event = None

        # Создаем UI
        Clock.schedule_once(self.setup_ui, 0.1)
        self.bind(size=self.update_positions)

    def setup_ui(self, dt):
        # Рисуем фон
        with self.canvas:
            Color(0.1, 0.15, 0.25, 1)
            self.sky = Rectangle(pos=(0, 0), size=self.size)

            Color(0.35, 0.25, 0.15, 1)
            self.ground = Rectangle(pos=(0, self.ground_y), size=(self.width, 8))

            Color(0.2, 0.8, 0.2, 1)
            self.dino = RoundedRectangle(pos=(self.dino_x, self.ground_y), size=self.dino_size, radius=[8])

        # Очки
        self.score_label = Label(
            text=f"Score: {self.score}",
            font_size=28,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(200, 50)
        )
        self.add_widget(self.score_label)

        self.best_label = Label(
            text=f"Best: {self.high_score}",
            font_size=20,
            color=(0.8, 0.8, 0.8, 1),
            size_hint=(None, None),
            size=(200, 40)
        )
        self.add_widget(self.best_label)

        # Кнопка выхода
        self.exit_btn = Button(
            text="EXIT",
            size_hint=(None, None),
            size=(80, 45),
            background_color=(0.7, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=18,
            bold=True,
            background_normal=''
        )
        self.exit_btn.bind(on_press=self.exit_game)
        self.add_widget(self.exit_btn)

        # Стартовое меню
        self.show_start_menu()

        self.update_positions()

    def show_start_menu(self):
        self.start_menu = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(260, 220),
            spacing=15
        )

        with self.start_menu.canvas.before:
            Color(0, 0, 0, 0.9)
            self.menu_bg = RoundedRectangle(size=self.start_menu.size, radius=[20])

        title = Label(
            text="🦕 DINO GAME 🦕",
            font_size=26,
            color=(0.2, 0.8, 0.2, 1),
            size_hint=(1, 0.35),
            bold=True
        )
        self.start_menu.add_widget(title)

        self.start_btn = Button(
            text="START GAME",
            size_hint=(1, 0.35),
            background_color=(0.2, 0.6, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=20,
            bold=True,
            background_normal=''
        )
        self.start_btn.bind(on_press=self.start_game)
        self.start_menu.add_widget(self.start_btn)

        inst_text = "👇 Tap to jump" if IS_MOBILE else "␣ Space to jump"
        inst_label = Label(
            text=inst_text,
            font_size=14,
            color=(0.8, 0.8, 0.8, 1),
            size_hint=(1, 0.2)
        )
        self.start_menu.add_widget(inst_label)

        self.add_widget(self.start_menu)

    def show_game_over_menu(self):
        self.game_over_menu = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(260, 240),
            spacing=15
        )

        with self.game_over_menu.canvas.before:
            Color(0, 0, 0, 0.9)
            self.go_bg = RoundedRectangle(size=self.game_over_menu.size, radius=[20])

        go_label = Label(
            text=f"GAME OVER!\nScore: {self.score}",
            font_size=26,
            color=(1, 0.3, 0.3, 1),
            size_hint=(1, 0.45),
            bold=True
        )
        self.game_over_menu.add_widget(go_label)

        again_btn = Button(
            text="PLAY AGAIN",
            size_hint=(1, 0.3),
            background_color=(0.2, 0.6, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=18,
            bold=True,
            background_normal=''
        )
        again_btn.bind(on_press=self.restart_game)
        self.game_over_menu.add_widget(again_btn)

        exit_btn2 = Button(
            text="EXIT",
            size_hint=(1, 0.3),
            background_color=(0.7, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=16,
            background_normal=''
        )
        exit_btn2.bind(on_press=self.exit_game)
        self.game_over_menu.add_widget(exit_btn2)

        self.add_widget(self.game_over_menu)

    def update_positions(self, *args):
        if hasattr(self, 'sky'):
            self.sky.size = self.size
            self.ground.size = (self.width, 8)

        if hasattr(self, 'score_label'):
            self.score_label.pos = (self.width - 170, self.height - 60)
            self.best_label.pos = (self.width - 170, self.height - 95)
            self.exit_btn.pos = (10, self.height - 55)

        if hasattr(self, 'start_menu') and self.start_menu.parent:
            self.start_menu.pos = (self.width // 2 - 130, self.height // 2 - 110)
            if hasattr(self, 'menu_bg'):
                self.menu_bg.pos = self.start_menu.pos
                self.menu_bg.size = self.start_menu.size

        if hasattr(self, 'game_over_menu') and self.game_over_menu and self.game_over_menu.parent:
            self.game_over_menu.pos = (self.width // 2 - 130, self.height // 2 - 120)
            if hasattr(self, 'go_bg'):
                self.go_bg.pos = self.game_over_menu.pos
                self.go_bg.size = self.game_over_menu.size

    def on_touch_down(self, touch, *args):
        # Кнопка выхода
        if self.exit_btn.collide_point(*touch.pos):
            self.exit_btn.dispatch('on_press')
            return True

        # Стартовое меню
        if hasattr(self, 'start_menu') and self.start_menu.parent:
            if self.start_btn.collide_point(*touch.pos):
                self.start_btn.dispatch('on_press')
                return True
            return True

        # Меню Game Over
        if hasattr(self, 'game_over_menu') and self.game_over_menu and self.game_over_menu.parent:
            for child in self.game_over_menu.children:
                if isinstance(child, Button) and child.collide_point(*touch.pos):
                    child.dispatch('on_press')
                    return True
            return True

        # Прыжок
        if self.is_running and self.dino_on_ground:
            self.dino_velocity = self.jump_strength
            self.dino_on_ground = False

        return super().on_touch_down(touch)

    def _keyboard_closed(self):
        if hasattr(self, '_keyboard') and self._keyboard:
            self._keyboard.unbind(on_key_down=self._on_key_down)
            self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'space':
            if not self.is_running and hasattr(self, 'start_menu') and self.start_menu.parent:
                self.start_game(None)
            elif self.is_running and self.dino_on_ground:
                self.dino_velocity = self.jump_strength
                self.dino_on_ground = False
        return True

    def start_game(self, instance):
        # Удаляем стартовое меню
        if hasattr(self, 'start_menu') and self.start_menu.parent:
            self.remove_widget(self.start_menu)

        # Удаляем меню Game Over если есть
        if hasattr(self, 'game_over_menu') and self.game_over_menu and self.game_over_menu.parent:
            self.remove_widget(self.game_over_menu)
            self.game_over_menu = None

        # Удаляем ВСЕ старые кактусы
        for obs in self.obstacles:
            if hasattr(obs, 'rect'):
                try:
                    self.canvas.remove(obs['rect'])
                except:
                    pass
        self.obstacles.clear()

        # Сбрасываем все переменные
        self.is_running = True
        self.score = 0
        self.dino_y = 0
        self.dino_velocity = 0
        self.dino_on_ground = True
        self.game_speed = 200
        self.obstacle_timer = 0

        # Обновляем очки
        self.score_label.text = "Score: 0"

        # Ставим динозавра на место
        self.dino.pos = (self.dino_x, self.ground_y)

        # Запускаем игровой цикл
        if self.game_event:
            self.game_event.cancel()
        self.game_event = Clock.schedule_interval(self.update_game, 1 / 60)

    def exit_game(self, instance):
        self.is_running = False
        if self.game_event:
            self.game_event.cancel()
        self.app.show("calc")
        if self.parent:
            self.parent.remove_widget(self)

    def update_game(self, dt):
        if not self.is_running:
            return

        # Физика прыжка
        self.dino_velocity += self.gravity * dt
        self.dino_y += self.dino_velocity * dt

        if self.dino_y <= 0:
            self.dino_y = 0
            self.dino_velocity = 0
            self.dino_on_ground = True
        else:
            self.dino_on_ground = False

        self.dino.pos = (self.dino_x, self.ground_y + self.dino_y)

        # Спавн новых кактусов
        self.obstacle_timer += 1
        if self.obstacle_timer > 70 and len(self.obstacles) < 3:
            self.obstacle_timer = 0
            obs = {
                'x': self.width,
                'width': 15,
                'height': 30
            }
            with self.canvas:
                Color(0.3, 0.6, 0.1, 1)
                obs['rect'] = RoundedRectangle(
                    pos=(obs['x'], self.ground_y),
                    size=(15, 30),
                    radius=[5]
                )
            self.obstacles.append(obs)

        # Движение кактусов
        for obs in self.obstacles[:]:
            obs['x'] -= self.game_speed * dt
            obs['rect'].pos = (obs['x'], self.ground_y)

            # Удаляем за экраном и добавляем очки
            if obs['x'] + obs['width'] < 0:
                self.obstacles.remove(obs)
                try:
                    self.canvas.remove(obs['rect'])
                except:
                    pass
                self.score += 10
                self.score_label.text = f"Score: {self.score}"

                if self.score > self.high_score:
                    self.high_score = self.score
                    self.best_label.text = f"Best: {self.high_score}"
                    store.put("game_stats", high_score=self.high_score)

            # Проверка столкновения
            if (self.dino_x < obs['x'] + 15 and
                    self.dino_x + 35 > obs['x'] and
                    self.ground_y + self.dino_y < self.ground_y + 30 and
                    self.ground_y + self.dino_y + 35 > self.ground_y):
                self.game_over()
                return

        # Увеличиваем скорость
        self.game_speed = min(400, 200 + self.score // 200)

    def game_over(self):
        self.is_running = False
        if self.game_event:
            self.game_event.cancel()

        # Показываем меню Game Over
        self.show_game_over_menu()
        self.update_positions()

    def restart_game(self, instance):
        # Полностью пересоздаём игру!
        # Удаляем текущую игру
        self.parent.remove_widget(self)

        # Создаём новую игру
        new_game = DinoGame(self.app)

        # Добавляем новую игру
        self.app.content.clear_widgets()
        self.app.content.add_widget(new_game)


# ======================
# 🍏 IOS BUTTON
# ======================
class IOSButton(Button):
    def __init__(self, bg_color, size_factor=1, **kwargs):
        super().__init__(**kwargs)
        self.bg_color_value = bg_color
        self.size_factor = size_factor
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)
        self.bold = True
        self.font_size = 24 * size_factor
        self.size_hint_y = None
        self.height = 82 * size_factor

        self.radius_value = 35

        with self.canvas.before:
            self.bg_color = Color(*bg_color)
            self.bg = RoundedRectangle(radius=[self.radius_value])

        self.bind(pos=self.update_graphics)
        self.bind(size=self.update_graphics)

    def update_graphics(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def on_press(self):
        Animation(opacity=0.65, duration=0.05).start(self)
        try:
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Context = PythonActivity.mActivity.getApplicationContext()
            vibrator = Context.getSystemService(Context.VIBRATOR_SERVICE)
            vibrator.vibrate(10)
        except:
            pass

    def on_release(self):
        Animation(opacity=1, duration=0.08).start(self)

    def update_theme(self, color, text, size_factor, radius=35):
        self.bg_color_value = color
        self.bg_color.rgba = color
        self.color = text
        self.font_size = 24 * size_factor
        self.height = 82 * size_factor
        self.radius_value = radius
        self.bg.radius = [radius]


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
        self.button_rows = []
        self.waiting_for_new_number = False

        self.display = TextInput(
            readonly=True,
            multiline=False,
            halign="right",
            background_color=(0, 0, 0, 0),
            foreground_color=app.theme["text"],
            font_size=46 * app.size_factor,
            size_hint=(1, 0.16),
            padding=[20, 20]
        )
        self.add_widget(self.display)

        self.buttons_container = GridLayout(
            cols=1,
            spacing=8,
            size_hint=(1, 0.84)
        )
        self.add_widget(self.buttons_container)
        self.create_buttons()

    def create_buttons(self):
        self.buttons_container.clear_widgets()
        self.buttons = []
        self.button_rows = []

        button_layouts = [
            ["C", "+/-", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]

        for row in button_layouts:
            row_layout = GridLayout(
                cols=len(row),
                spacing=8,
                size_hint=(1, None),
                height=88 * self.app.size_factor
            )

            for text in row:
                if text in ["+", "-", "*", "/", "="]:
                    color = self.app.theme["op"]
                elif text == "C":
                    color = (0.6, 0.6, 0.6, 1)
                else:
                    color = self.app.theme["num"]

                btn = IOSButton(
                    text=text,
                    bg_color=color,
                    size_factor=self.app.size_factor
                )

                if text == "0":
                    btn.size_hint_x = 2

                btn.bind(on_press=self.on_button)
                self.buttons.append(btn)
                row_layout.add_widget(btn)

            self.buttons_container.add_widget(row_layout)
            self.button_rows.append(row_layout)

    def on_button(self, instance):
        t = instance.text

        if self.waiting_for_new_number and t not in ["C", "+/-", "%", "/", "*", "-", "+", "="]:
            self.display.text = ""
            self.waiting_for_new_number = False

        if t == "C":
            self.display.text = ""
            self.waiting_for_new_number = False
        elif t == "=":
            try:
                expression = self.display.text.replace("×", "*")
                expression = expression.replace("÷", "/")
                result = str(eval(expression))

                if expression == "67" or expression == "67.0" or expression == "67.00":
                    self.start_dino_game()
                    return

                if expression == "1337" or expression == "1337.0":
                    self.show_easter_egg()
                    return

                self.history.append(f"{expression} = {result}")
                self.display.text = result
                self.waiting_for_new_number = True
            except Exception as e:
                print(f"Error: {e}")
                self.display.text = "Error"
                self.waiting_for_new_number = True
                Clock.schedule_once(self.clear, 1)
        elif t == "+/-":
            try:
                self.display.text = str(-float(self.display.text))
            except:
                pass
        elif t == "%":
            try:
                self.display.text = str(float(self.display.text) / 100)
            except:
                pass
        else:
            self.display.text += t

    def start_dino_game(self):
        print("Creating DinoGame...")
        self.game = DinoGame(self.app)
        print("Game created, clearing content...")
        self.app.content.clear_widgets()
        print("Adding game to content...")
        self.app.content.add_widget(self.game)
        print("Game started!")

    def show_easter_egg(self):
        self.display.text = "SECRET UNLOCKED!"
        self.waiting_for_new_number = True
        Clock.schedule_once(lambda dt: self.clear(0), 2)

    def clear(self, dt):
        self.display.text = ""
        self.waiting_for_new_number = False

    def resize_buttons(self):
        self.display.font_size = 46 * self.app.size_factor
        self.create_buttons()

    def update_theme(self):
        self.display.foreground_color = self.app.theme["text"]
        self.display.font_size = 46 * self.app.size_factor

        for btn in self.buttons:
            if btn.text in ["+", "-", "*", "/", "="]:
                color = self.app.theme["op"]
            elif btn.text == "C":
                color = (0.6, 0.6, 0.6, 1)
            else:
                color = self.app.theme["num"]

            btn.update_theme(
                color,
                self.app.theme["text"],
                self.app.size_factor,
                self.app.theme.get("button_radius", 35)
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
        self.rates_cache = {}
        self.last_update = 0

        currency_layout = GridLayout(cols=2, spacing=10, size_hint=(1, 0.12))

        self.from_currency = TextInput(
            text="USD",
            hint_text="From (USD, EUR, RUB...)",
            multiline=False,
            font_size=22 * app.size_factor,
            size_hint=(0.5, 1),
            padding=[10, 10],
            background_color=(0.1, 0.1, 0.1, 0.8)
        )

        self.to_currency = TextInput(
            text="RUB",
            hint_text="To (USD, EUR, RUB...)",
            multiline=False,
            font_size=22 * app.size_factor,
            size_hint=(0.5, 1),
            padding=[10, 10],
            background_color=(0.1, 0.1, 0.1, 0.8)
        )

        currency_layout.add_widget(self.from_currency)
        currency_layout.add_widget(self.to_currency)

        self.input = TextInput(
            hint_text="Enter amount",
            multiline=False,
            font_size=34 * app.size_factor,
            size_hint=(1, 0.1),
            padding=[15, 15],
            background_color=(0.1, 0.1, 0.1, 0.8),
            input_filter='float'
        )

        self.result = TextInput(
            readonly=True,
            font_size=24 * app.size_factor,
            background_color=(0, 0, 0, 0),
            foreground_color=app.theme["text"],
            padding=[15, 15],
            multiline=True,
            size_hint=(1, 0.22)
        )

        button_layout = GridLayout(cols=3, spacing=8, size_hint=(1, 0.1))

        self.update_btn = IOSButton(
            text="Update",
            bg_color=(0.3, 0.6, 0.3, 1),
            size_factor=app.size_factor * 0.7
        )
        self.update_btn.bind(on_press=self.update_rates)

        self.convert_btn = IOSButton(
            text="Convert",
            bg_color=app.theme["op"],
            size_factor=app.size_factor * 0.7
        )
        self.convert_btn.bind(on_press=self.convert)

        self.swap_btn = IOSButton(
            text="Swap",
            bg_color=(0.4, 0.4, 0.6, 1),
            size_factor=app.size_factor * 0.7
        )
        self.swap_btn.bind(on_press=self.swap_currencies)

        button_layout.add_widget(self.update_btn)
        button_layout.add_widget(self.convert_btn)
        button_layout.add_widget(self.swap_btn)

        self.status_label = Label(
            text="Click Update to get latest rates",
            color=(0.7, 0.7, 0.7, 1),
            size_hint=(1, 0.06),
            font_size=12,
            halign='center'
        )

        popular_label = Label(
            text="Popular:",
            color=app.theme["text"],
            size_hint=(1, 0.04),
            font_size=14
        )

        popular_layout = GridLayout(cols=4, spacing=5, size_hint=(1, 0.1))
        popular_currencies = ["USD", "EUR", "RUB", "GBP", "JPY", "CNY", "TRY", "KZT"]

        for currency in popular_currencies:
            btn = Button(
                text=currency,
                font_size=14,
                size_hint=(1, 1),
                background_normal='',
                background_color=(0.2, 0.2, 0.3, 0.8),
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=lambda x, c=currency: self.set_to_currency(c))
            popular_layout.add_widget(btn)

        self.add_widget(currency_layout)
        self.add_widget(self.input)
        self.add_widget(button_layout)
        self.add_widget(self.result)
        self.add_widget(self.status_label)
        self.add_widget(popular_label)
        self.add_widget(popular_layout)

        Clock.schedule_once(lambda dt: self.update_rates(None), 1)
        Clock.schedule_interval(lambda dt: self.update_rates(None), 3600)

    def set_to_currency(self, currency):
        self.to_currency.text = currency
        if self.input.text:
            self.convert(None)

    def swap_currencies(self, instance):
        from_curr = self.from_currency.text.upper()
        to_curr = self.to_currency.text.upper()
        self.from_currency.text = to_curr
        self.to_currency.text = from_curr
        if self.input.text:
            self.convert(None)

    def update_rates(self, instance):
        try:
            self.status_label.text = "Updating..."
            self.status_label.color = (1, 1, 0, 1)

            response = requests.get(
                "https://open.er-api.com/v6/latest/USD",
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                self.rates_cache = data["rates"]
                self.rates_cache["USD"] = 1.0
                self.last_update = data["time_last_update_unix"]

                update_time = datetime.fromtimestamp(self.last_update).strftime("%H:%M:%S")
                self.status_label.text = f"Updated! ({update_time})"
                self.status_label.color = (0, 1, 0, 1)

                if self.input.text:
                    self.convert(None)
            else:
                self.status_label.text = "API error, using fallback"
                self.use_fallback_rates()

        except:
            self.status_label.text = "No internet! Using fallback"
            self.status_label.color = (1, 0.5, 0, 1)
            self.use_fallback_rates()

    def use_fallback_rates(self):
        self.rates_cache = {
            "USD": 1.0, "EUR": 0.92, "RUB": 88.5, "GBP": 0.79,
            "JPY": 148.2, "CNY": 7.19, "TRY": 32.1, "KZT": 443.5,
            "CAD": 1.36, "AUD": 1.52, "CHF": 0.91, "INR": 83.2
        }

    def convert(self, instance):
        if not self.rates_cache:
            self.status_label.text = "Click Update first"
            return

        try:
            amount = float(self.input.text)
            from_curr = self.from_currency.text.upper().strip()
            to_curr = self.to_currency.text.upper().strip()

            if from_curr not in self.rates_cache:
                self.result.text = f"'{from_curr}' not supported"
                return

            if to_curr not in self.rates_cache:
                self.result.text = f"'{to_curr}' not supported"
                return

            amount_in_usd = amount / self.rates_cache[from_curr]
            converted_amount = amount_in_usd * self.rates_cache[to_curr]
            rate = self.rates_cache[to_curr] / self.rates_cache[from_curr]

            self.result.text = (
                f"{amount:,.2f} {from_curr} = {converted_amount:,.2f} {to_curr}\n\n"
                f"1 {from_curr} = {rate:.4f} {to_curr}\n"
                f"1 {to_curr} = {1 / rate:.4f} {from_curr}"
            )

            self.status_label.text = f"{amount} {from_curr} -> {to_curr}"

        except ValueError:
            self.result.text = "Enter valid number"
        except:
            self.result.text = "Conversion error"

    def update_theme(self):
        self.result.foreground_color = self.app.theme["text"]
        self.convert_btn.update_theme(
            self.app.theme["op"],
            self.app.theme["text"],
            self.app.size_factor * 0.7,
            self.app.theme.get("button_radius", 35)
        )


# ======================
# 📜 HISTORY SCREEN
# ======================
class History(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = "vertical"
        self.padding = 10
        self.spacing = 10

        self.history_box = TextInput(
            readonly=True,
            font_size=22,
            background_color=(0, 0, 0, 0),
            foreground_color=app.theme["text"],
            padding=[15, 15]
        )

        clear_btn = IOSButton(
            text="Clear History",
            bg_color=(1, 0, 0, 1),
            size_factor=app.size_factor
        )
        clear_btn.bind(on_press=self.clear_history)

        self.add_widget(clear_btn)
        self.add_widget(self.history_box)

    def update_history(self):
        history = self.app.calculator.history
        if history:
            self.history_box.text = "\n".join(history[::-1])
        else:
            self.history_box.text = "No history yet.\nMake some calculations!"

    def clear_history(self, instance):
        self.app.calculator.history.clear()
        self.update_history()

    def update_theme(self):
        self.history_box.foreground_color = self.app.theme["text"]


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

        size_label = Label(
            text="Button Size",
            color=app.theme["text"],
            size_hint=(1, 0.1),
            font_size=20
        )

        self.slider = Slider(
            min=0.5,
            max=1.5,
            value=app.size_factor,
            size_hint=(1, 0.08)
        )
        self.slider.bind(value=self.change_size)

        theme_label = Label(
            text="Themes",
            color=app.theme["text"],
            size_hint=(1, 0.1),
            font_size=20
        )

        self.add_widget(size_label)
        self.add_widget(self.slider)
        self.add_widget(theme_label)

        for theme_name in THEMES.keys():
            btn = IOSButton(
                text=theme_name,
                bg_color=THEMES[theme_name]["top"],
                size_factor=app.size_factor
            )
            btn.bind(on_press=lambda instance, name=theme_name: self.change_theme(name))
            self.add_widget(btn)

    def change_size(self, instance, value):
        self.app.size_factor = value
        store.put("settings", size=value, theme=self.app.theme_name)
        self.app.update_all()

    def change_theme(self, theme_name):
        self.app.theme_name = theme_name
        self.app.theme = THEMES[theme_name]
        Window.clearcolor = self.app.theme["bg"]
        store.put("settings", size=self.app.size_factor, theme=theme_name)
        self.app.update_all()

    def update_theme(self):
        pass


# ======================
# 📱 MAIN APP
# ======================
class MainApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        if store.exists("settings"):
            data = store.get("settings")
            self.size_factor = data["size"]
            self.theme_name = data["theme"]
        else:
            self.size_factor = 1
            self.theme_name = "Dark"

        self.theme = THEMES[self.theme_name]
        Window.clearcolor = self.theme["bg"]

        top = GridLayout(
            cols=4,
            spacing=8,
            padding=8,
            size_hint=(1, 0.08)
        )

        self.calc_btn = IOSButton(
            text="Calc",
            bg_color=self.theme["top"],
            size_factor=0.75
        )
        self.calc_btn.bind(on_press=lambda x: self.show("calc"))

        self.conv_btn = IOSButton(
            text="Conv",
            bg_color=self.theme["top"],
            size_factor=0.75
        )
        self.conv_btn.bind(on_press=lambda x: self.show("conv"))

        self.hist_btn = IOSButton(
            text="Hist",
            bg_color=self.theme["top"],
            size_factor=0.75
        )
        self.hist_btn.bind(on_press=lambda x: self.show("hist"))

        self.set_btn = IOSButton(
            text="Sets",
            bg_color=self.theme["top"],
            size_factor=0.75
        )
        self.set_btn.bind(on_press=lambda x: self.show("set"))

        top.add_widget(self.calc_btn)
        top.add_widget(self.conv_btn)
        top.add_widget(self.hist_btn)
        top.add_widget(self.set_btn)

        self.add_widget(top)

        self.content = BoxLayout()

        self.calculator = Calculator(self)
        self.converter = Converter(self)
        self.history_screen = History(self)
        self.settings = Settings(self)

        self.content.add_widget(self.calculator)
        self.add_widget(self.content)

    def show(self, screen):
        self.content.clear_widgets()

        if screen == "calc":
            self.content.add_widget(self.calculator)
        elif screen == "conv":
            self.content.add_widget(self.converter)
        elif screen == "hist":
            self.history_screen.update_history()
            self.content.add_widget(self.history_screen)
        elif screen == "set":
            self.content.add_widget(self.settings)

    def update_all(self):
        Window.clearcolor = self.theme["bg"]

        self.calculator.update_theme()
        self.calculator.resize_buttons()
        self.converter.update_theme()
        self.history_screen.update_theme()

        buttons = [self.calc_btn, self.conv_btn, self.hist_btn, self.set_btn]

        for btn in buttons:
            btn.update_theme(self.theme["top"], self.theme["text"], 0.75, self.theme.get("button_radius", 35))


# ======================
# 🚀 APP
# ======================
class GlassCalculatorApp(App):
    icon = "icon.png"

    def build(self):
        return MainApp()


if __name__ == "__main__":
    GlassCalculatorApp().run()