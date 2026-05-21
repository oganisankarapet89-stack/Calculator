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
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout

from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation

from kivy.graphics import (
    Color,
    RoundedRectangle,
    Rectangle,
    Ellipse
)

from kivy.storage.jsonstore import JsonStore
from kivy.utils import platform
from kivy.metrics import dp, sp

# =========================================================
# 📱 MOBILE OPTIMIZATION
# =========================================================

IS_MOBILE = platform in ("android", "ios")

# Оптимальные размеры для любого смартфона
if IS_MOBILE:
    Window.size = (dp(360), dp(640))
    Window.fullscreen = 'auto'
else:
    Window.size = (400, 700)

Window.clearcolor = (0, 0, 0, 1)

# =========================================================
# 💾 STORAGE
# =========================================================

store = JsonStore("settings.json")

# =========================================================
# 🎨 THEMES
# =========================================================

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

# =========================================================
# 🍏 IOS BUTTON
# =========================================================

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
        self.font_size = sp(24 * size_factor)
        self.size_hint_y = None
        self.height = dp(78 * size_factor)
        self.radius_value = dp(35)

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

    def on_release(self):
        Animation(opacity=1, duration=0.08).start(self)

    def update_theme(self, color, text, size_factor, radius=35):
        self.bg_color.rgba = color
        self.color = text
        self.font_size = sp(24 * size_factor)
        self.height = dp(78 * size_factor)
        self.radius_value = dp(radius)
        self.bg.radius = [self.radius_value]

# =========================================================
# 🦕 DINO GAME (ИСПРАВЛЕН - НЕТ ЧЁРНОГО ПРЯМОУГОЛЬНИКА)
# =========================================================

class DinoGame(Widget):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.size_hint = (1, 1)

        if store.exists("game_stats"):
            data = store.get("game_stats")
            self.high_score = data.get("high_score", 0)
        else:
            self.high_score = 0

        self.is_running = False
        self.score = 0
        self.dino_x = 0
        self.dino_velocity = 0
        self.obstacles = []
        self.obstacle_timer = 0

        self.dino_size = (dp(40), dp(40))
        self.ground_y = dp(60)

        self.game_event = None

        self.bind(size=self.update_sizes)
        Clock.schedule_once(self.setup_ui, 0.1)

    def update_sizes(self, *args):
        if hasattr(self, 'ground'):
            self.ground.pos = (0, self.ground_y)
        if hasattr(self, 'dino'):
            self.dino.pos = (self.dino_x, self.ground_y - self.dino_size[1])

    def setup_ui(self, dt):
        self.canvas.clear()
        self.clear_widgets()

        with self.canvas:
            Color(0.1, 0.15, 0.25, 1)
            self.sky = Rectangle(pos=(0, 0), size=self.size)

            Color(0.35, 0.25, 0.15, 1)
            self.ground = Rectangle(pos=(0, self.ground_y), size=(self.width, dp(8)))

            Color(0.2, 0.8, 0.2, 1)
            self.dino = RoundedRectangle(
                pos=(self.dino_x, self.ground_y - self.dino_size[1]),
                size=self.dino_size,
                radius=[dp(8)]
            )

            Color(1, 1, 1, 1)
            self.eye = Ellipse(
                pos=(self.dino_x + self.dino_size[0] - dp(12), self.ground_y - self.dino_size[1] + dp(8)),
                size=(dp(8), dp(8))
            )
            Color(0, 0, 0, 1)
            self.pupil = Ellipse(
                pos=(self.dino_x + self.dino_size[0] - dp(10), self.ground_y - self.dino_size[1] + dp(10)),
                size=(dp(4), dp(4))
            )

        self.score_label = Label(
            text=f"Score: 0",
            font_size=sp(26),
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(dp(180), dp(45))
        )
        self.add_widget(self.score_label)

        self.best_label = Label(
            text=f"Best: {self.high_score}",
            font_size=sp(20),
            color=(0.8, 0.8, 0.8, 1),
            size_hint=(None, None),
            size=(dp(180), dp(35))
        )
        self.add_widget(self.best_label)

        self.exit_btn = Button(
            text="EXIT",
            size_hint=(None, None),
            size=(dp(65), dp(38)),
            background_color=(0.7, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size=sp(15),
            bold=True,
            background_normal=''
        )
        self.exit_btn.bind(on_press=self.exit_game)
        self.add_widget(self.exit_btn)

        # Стартовое меню - через FloatLayout чтобы точно по центру
        self.start_container = FloatLayout(size_hint=(1, 1))

        self.start_menu = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(dp(250), dp(210)),
            spacing=dp(12)
        )

        with self.start_menu.canvas.before:
            Color(0, 0, 0, 0.92)
            self.menu_bg = RoundedRectangle(size=self.start_menu.size, radius=[dp(20)])

        title = Label(
            text="🦕 DINO GAME 🦕",
            font_size=sp(24),
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
            font_size=sp(18),
            bold=True,
            background_normal=''
        )
        self.start_btn.bind(on_press=self.start_game)
        self.start_menu.add_widget(self.start_btn)

        inst_text = "👆 Tap left/right to move" if IS_MOBILE else "← → arrows"
        inst_label = Label(
            text=inst_text,
            font_size=sp(13),
            color=(0.8, 0.8, 0.8, 1),
            size_hint=(1, 0.2)
        )
        self.start_menu.add_widget(inst_label)

        self.start_container.add_widget(self.start_menu)
        self.add_widget(self.start_container)

        self.update_positions()

    def update_positions(self, *args):
        if hasattr(self, 'score_label'):
            self.score_label.pos = (self.width - dp(150), self.height - dp(55))
            self.best_label.pos = (self.width - dp(150), self.height - dp(88))
            self.exit_btn.pos = (dp(8), self.height - dp(45))

        if hasattr(self, 'start_container') and self.start_container.parent:
            self.start_container.pos = (0, 0)
            self.start_menu.pos = (self.width // 2 - dp(125), self.height // 2 - dp(105))
            if hasattr(self, 'menu_bg'):
                self.menu_bg.pos = self.start_menu.pos
                self.menu_bg.size = self.start_menu.size

        if hasattr(self, 'game_over_container') and self.game_over_container and self.game_over_container.parent:
            self.game_over_container.pos = (0, 0)
            self.game_over_menu.pos = (self.width // 2 - dp(125), self.height // 2 - dp(115))
            if hasattr(self, 'go_bg'):
                self.go_bg.pos = self.game_over_menu.pos
                self.go_bg.size = self.game_over_menu.size

    def on_touch_down(self, touch):
        if hasattr(self, 'exit_btn') and self.exit_btn.collide_point(*touch.pos):
            return
        if hasattr(self, 'start_container') and self.start_container.parent:
            if hasattr(self, 'start_btn') and self.start_btn.collide_point(*touch.pos):
                self.start_game(None)
                return
            return
        if hasattr(self, 'game_over_container') and self.game_over_container and self.game_over_container.parent:
            for child in self.game_over_menu.children:
                if isinstance(child, Button) and child.collide_point(*touch.pos):
                    child.dispatch('on_press')
                    return
            return
        if self.is_running:
            if touch.x < self.width / 2:
                self.dino_velocity = -380
            else:
                self.dino_velocity = 380

    def start_game(self, instance):
        if hasattr(self, 'start_container') and self.start_container.parent:
            self.remove_widget(self.start_container)
        if hasattr(self, 'game_over_container') and self.game_over_container and self.game_over_container.parent:
            self.remove_widget(self.game_over_container)
            self.game_over_container = None

        for obs in self.obstacles:
            if hasattr(obs, 'rect'):
                try:
                    self.canvas.remove(obs['rect'])
                except:
                    pass
        self.obstacles.clear()

        self.is_running = True
        self.score = 0
        self.dino_x = self.width // 2 - self.dino_size[0] // 2
        self.dino_velocity = 0
        self.obstacle_timer = 0
        self.score_label.text = "Score: 0"

        if hasattr(self, 'dino'):
            self.dino.pos = (self.dino_x, self.ground_y - self.dino_size[1])
            self.eye.pos = (self.dino_x + self.dino_size[0] - dp(12), self.ground_y - self.dino_size[1] + dp(8))
            self.pupil.pos = (self.dino_x + self.dino_size[0] - dp(10), self.ground_y - self.dino_size[1] + dp(10))

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

        self.dino_x += self.dino_velocity * dt
        self.dino_velocity *= 0.98

        if self.dino_x <= 0:
            self.dino_x = 0
            self.dino_velocity = 0
        elif self.dino_x >= self.width - self.dino_size[0]:
            self.dino_x = self.width - self.dino_size[0]
            self.dino_velocity = 0

        self.dino.pos = (self.dino_x, self.ground_y - self.dino_size[1])
        self.eye.pos = (self.dino_x + self.dino_size[0] - dp(12), self.ground_y - self.dino_size[1] + dp(8))
        self.pupil.pos = (self.dino_x + self.dino_size[0] - dp(10), self.ground_y - self.dino_size[1] + dp(10))

        self.obstacle_timer += 1
        if self.obstacle_timer > 55 and len(self.obstacles) < 4:
            self.obstacle_timer = 0
            width = dp(14)
            height = dp(32)
            obs = {
                'x': random.randint(0, int(self.width - width)),
                'y': self.height,
                'width': width,
                'height': height,
                'speed': random.randint(140, 280)
            }
            with self.canvas:
                Color(0.3, 0.6, 0.1, 1)
                obs['rect'] = RoundedRectangle(
                    pos=(obs['x'], obs['y']),
                    size=(width, height),
                    radius=[dp(5)]
                )
            self.obstacles.append(obs)

        for obs in self.obstacles[:]:
            obs['y'] -= obs['speed'] * dt
            obs['rect'].pos = (obs['x'], obs['y'])

            if obs['y'] + obs['height'] < 0:
                self.obstacles.remove(obs)
                self.canvas.remove(obs['rect'])
                self.score += 10
                self.score_label.text = f"Score: {self.score}"
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.best_label.text = f"Best: {self.high_score}"
                    store.put("game_stats", high_score=self.high_score)

            if (self.dino_x < obs['x'] + obs['width'] and
                self.dino_x + self.dino_size[0] > obs['x'] and
                self.ground_y - self.dino_size[1] < obs['y'] + obs['height'] and
                self.ground_y > obs['y']):
                self.game_over()
                return

    def game_over(self):
        self.is_running = False
        if self.game_event:
            self.game_event.cancel()

        self.game_over_container = FloatLayout(size_hint=(1, 1))

        self.game_over_menu = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(dp(250), dp(230)),
            spacing=dp(12)
        )

        with self.game_over_menu.canvas.before:
            Color(0, 0, 0, 0.92)
            self.go_bg = RoundedRectangle(size=self.game_over_menu.size, radius=[dp(20)])

        go_label = Label(
            text=f"GAME OVER!\nScore: {self.score}",
            font_size=sp(24),
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
            font_size=sp(17),
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
            font_size=sp(15),
            background_normal=''
        )
        exit_btn2.bind(on_press=self.exit_game)
        self.game_over_menu.add_widget(exit_btn2)

        self.game_over_container.add_widget(self.game_over_menu)
        self.add_widget(self.game_over_container)
        self.update_positions()

    def restart_game(self, instance):
        # Полностью пересоздаём игру
        if self.parent:
            self.parent.remove_widget(self)
        new_game = DinoGame(self.app)
        self.app.content.clear_widgets()
        self.app.content.add_widget(new_game)

# =========================================================
# 💱 CONVERTER
# =========================================================

class Converter(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = "vertical"
        self.spacing = dp(10)
        self.padding = dp(10)
        self.rates_cache = {}

        # Currency selection row
        currency_row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(50), spacing=dp(10))

        self.from_currency = TextInput(
            text="USD",
            hint_text="From",
            multiline=False,
            font_size=sp(20),
            size_hint=(0.5, 1),
            padding=[dp(8), dp(8)],
            background_color=(0.1, 0.1, 0.1, 0.8),
            foreground_color=(1, 1, 1, 1)
        )

        self.to_currency = TextInput(
            text="RUB",
            hint_text="To",
            multiline=False,
            font_size=sp(20),
            size_hint=(0.5, 1),
            padding=[dp(8), dp(8)],
            background_color=(0.1, 0.1, 0.1, 0.8),
            foreground_color=(1, 1, 1, 1)
        )

        currency_row.add_widget(self.from_currency)
        currency_row.add_widget(self.to_currency)

        self.input = TextInput(
            hint_text="Enter amount",
            multiline=False,
            font_size=sp(32),
            size_hint=(1, None),
            height=dp(55),
            padding=[dp(15), dp(15)],
            background_color=(0.1, 0.1, 0.1, 0.8),
            input_filter='float',
            foreground_color=(1, 1, 1, 1)
        )

        self.result = TextInput(
            readonly=True,
            font_size=sp(22),
            background_color=(0, 0, 0, 0),
            foreground_color=(1, 1, 1, 1),
            padding=[dp(12), dp(12)],
            multiline=True,
            size_hint=(1, None),
            height=dp(110)
        )

        # Buttons row
        buttons_row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(55), spacing=dp(8))

        self.update_btn = IOSButton(
            text="Update",
            bg_color=(0.3, 0.6, 0.3, 1),
            size_factor=0.65
        )
        self.update_btn.bind(on_press=self.update_rates)

        self.convert_btn = IOSButton(
            text="Convert",
            bg_color=app.theme["op"],
            size_factor=0.65
        )
        self.convert_btn.bind(on_press=self.convert)

        self.swap_btn = IOSButton(
            text="Swap",
            bg_color=(0.4, 0.4, 0.6, 1),
            size_factor=0.65
        )
        self.swap_btn.bind(on_press=self.swap_currencies)

        buttons_row.add_widget(self.update_btn)
        buttons_row.add_widget(self.convert_btn)
        buttons_row.add_widget(self.swap_btn)

        self.status_label = Label(
            text="Click Update to get rates",
            color=(0.7, 0.7, 0.7, 1),
            size_hint=(1, None),
            height=dp(25),
            font_size=sp(11)
        )

        # Popular currencies
        popular_label = Label(
            text="Popular currencies:",
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=dp(30),
            font_size=sp(14),
            bold=True
        )

        popular_grid = GridLayout(cols=4, spacing=dp(5), size_hint=(1, None), height=dp(130))

        popular_currencies = ["USD", "EUR", "RUB", "GBP", "JPY", "CNY", "TRY", "KZT", "CAD", "AUD", "CHF", "INR", "BRL", "MXN", "SGD", "AED"]

        for currency in popular_currencies:
            btn = Button(
                text=currency,
                font_size=sp(13),
                size_hint=(1, 1),
                background_normal='',
                background_color=(0.2, 0.2, 0.3, 0.8),
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=lambda x, c=currency: self.set_to_currency(c))
            popular_grid.add_widget(btn)

        self.add_widget(currency_row)
        self.add_widget(self.input)
        self.add_widget(buttons_row)
        self.add_widget(self.result)
        self.add_widget(self.status_label)
        self.add_widget(popular_label)
        self.add_widget(popular_grid)

        Clock.schedule_once(lambda dt: self.update_rates(None), 1)

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
                self.status_label.text = "Updated!"
                self.status_label.color = (0, 1, 0, 1)

                if self.input.text:
                    self.convert(None)
            else:
                self.use_fallback_rates()

        except:
            self.status_label.text = "No internet! Using fallback"
            self.status_label.color = (1, 0.5, 0, 1)
            self.use_fallback_rates()

    def use_fallback_rates(self):
        self.rates_cache = {
            "USD": 1.0, "EUR": 0.92, "RUB": 88.5, "GBP": 0.79,
            "JPY": 148.2, "CNY": 7.19, "TRY": 32.1, "KZT": 443.5,
            "CAD": 1.36, "AUD": 1.52, "CHF": 0.91, "INR": 83.2,
            "BRL": 5.05, "MXN": 16.8, "SGD": 1.35, "AED": 3.67
        }

    def convert(self, instance):
        if not self.rates_cache:
            self.status_label.text = "Click Update first"
            return

        try:
            amount = float(self.input.text)
            from_curr = self.from_currency.text.upper().strip()
            to_curr = self.to_currency.text.upper().strip()

            if from_curr not in self.rates_cache or to_curr not in self.rates_cache:
                self.result.text = "Currency not supported"
                return

            amount_in_usd = amount / self.rates_cache[from_curr]
            converted_amount = amount_in_usd * self.rates_cache[to_curr]
            rate = self.rates_cache[to_curr] / self.rates_cache[from_curr]

            self.result.text = (
                f"{amount:,.2f} {from_curr} = {converted_amount:,.2f} {to_curr}\n\n"
                f"1 {from_curr} = {rate:.4f} {to_curr}\n"
                f"1 {to_curr} = {1 / rate:.4f} {from_curr}"
            )
            self.status_label.text = f"✅ {amount} {from_curr} → {to_curr}"
        except:
            self.result.text = "Enter valid number"

    def update_theme(self):
        self.convert_btn.update_theme(
            self.app.theme["op"],
            (1, 1, 1, 1),
            self.app.size_factor * 0.65,
            self.app.theme.get("button_radius", 35)
        )
        self.result.foreground_color = (1, 1, 1, 1)

# =========================================================
# 📟 CALCULATOR
# =========================================================

class Calculator(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = "vertical"
        self.padding = dp(8)
        self.spacing = dp(8)
        self.history = []
        self.buttons = []
        self.button_rows = []
        self.waiting_for_new_number = False

        self.display = TextInput(
            readonly=True,
            multiline=False,
            halign="right",
            background_color=(0, 0, 0, 0),
            foreground_color=(1, 1, 1, 1),
            font_size=sp(44 * app.size_factor),
            size_hint=(1, 0.15),
            padding=[dp(18), dp(18)]
        )
        self.add_widget(self.display)

        self.buttons_container = GridLayout(
            cols=1,
            spacing=dp(8),
            size_hint=(1, 0.85)
        )
        self.add_widget(self.buttons_container)
        self.create_buttons()

    def create_buttons(self):
        self.buttons_container.clear_widgets()
        self.buttons = []
        self.button_rows = []

        layout = [
            ["C", "+/-", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "="]
        ]

        for row in layout:
            row_layout = GridLayout(
                cols=len(row),
                spacing=dp(8),
                size_hint=(1, None),
                height=dp(80 * self.app.size_factor)
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

            self.button_rows.append(row_layout)
            self.buttons_container.add_widget(row_layout)

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

                if expression == "67" or expression == "67.0":
                    self.start_dino_game()
                    return

                self.history.append(f"{expression} = {result}")
                self.display.text = result
                self.waiting_for_new_number = True
            except:
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
        self.game = DinoGame(self.app)
        self.app.content.clear_widgets()
        self.app.content.add_widget(self.game)

    def clear(self, dt):
        self.display.text = ""
        self.waiting_for_new_number = False

    def resize_buttons(self):
        self.display.font_size = sp(44 * self.app.size_factor)
        for btn in self.buttons:
            btn.font_size = sp(24 * self.app.size_factor)
            btn.height = dp(78 * self.app.size_factor)
        for row in self.button_rows:
            row.height = dp(80 * self.app.size_factor)

    def update_theme(self):
        self.display.foreground_color = (1, 1, 1, 1)
        for btn in self.buttons:
            if btn.text in ["+", "-", "*", "/", "="]:
                color = self.app.theme["op"]
            elif btn.text == "C":
                color = (0.6, 0.6, 0.6, 1)
            else:
                color = self.app.theme["num"]
            btn.update_theme(color, (1, 1, 1, 1), self.app.size_factor, self.app.theme.get("button_radius", 35))

# =========================================================
# 📜 HISTORY SCREEN
# =========================================================

class History(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = "vertical"
        self.padding = dp(10)
        self.spacing = dp(10)

        self.history_box = TextInput(
            readonly=True,
            font_size=sp(20),
            background_color=(0, 0, 0, 0),
            foreground_color=(1, 1, 1, 1),
            padding=[dp(12), dp(12)]
        )

        clear_btn = IOSButton(
            text="Clear History",
            bg_color=(1, 0, 0, 1),
            size_factor=0.75
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
        self.history_box.foreground_color = (1, 1, 1, 1)

# =========================================================
# ⚙ SETTINGS
# =========================================================

class Settings(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = "vertical"
        self.padding = dp(12)
        self.spacing = dp(12)

        scroll = ScrollView(size_hint=(1, 1))
        self.container = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=None,
            padding=[0, 0, 0, dp(25)]
        )
        self.container.bind(minimum_height=self.container.setter('height'))

        size_label = Label(
            text="Button Size",
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=dp(35),
            font_size=sp(20)
        )

        self.slider = Slider(
            min=0.7,
            max=1.4,
            value=app.size_factor,
            size_hint=(1, None),
            height=dp(35)
        )
        self.slider.bind(value=self.change_size)

        self.size_value = Label(
            text=f"Scale: {app.size_factor:.2f}",
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=dp(25),
            font_size=sp(14)
        )

        theme_label = Label(
            text="Themes",
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=dp(35),
            font_size=sp(20)
        )

        self.container.add_widget(size_label)
        self.container.add_widget(self.slider)
        self.container.add_widget(self.size_value)
        self.container.add_widget(theme_label)

        self.theme_buttons = []
        for theme_name in THEMES.keys():
            btn = IOSButton(
                text=theme_name,
                bg_color=THEMES[theme_name]["top"],
                size_factor=0.78
            )
            btn.height = dp(68)
            btn.font_size = sp(18)
            btn.bind(on_press=lambda instance, name=theme_name: self.change_theme(name))
            self.theme_buttons.append(btn)
            self.container.add_widget(btn)

        scroll.add_widget(self.container)
        self.add_widget(scroll)

    def change_size(self, instance, value):
        self.app.size_factor = value
        self.size_value.text = f"Scale: {value:.2f}"
        store.put("settings", size=value, theme=self.app.theme_name)
        self.app.update_all()

    def change_theme(self, theme_name):
        self.app.theme_name = theme_name
        self.app.theme = THEMES[theme_name]
        Window.clearcolor = self.app.theme["bg"]
        store.put("settings", size=self.app.size_factor, theme=theme_name)
        self.app.update_all()

    def update_theme(self):
        for btn in self.theme_buttons:
            btn.update_theme(
                THEMES[btn.text]["top"],
                (1, 1, 1, 1),
                0.78,
                self.app.theme.get("button_radius", 35)
            )

# =========================================================
# 📱 MAIN APP
# =========================================================

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
            spacing=dp(6),
            padding=dp(6),
            size_hint=(1, 0.07)
        )

        self.calc_btn = IOSButton(
            text="Calc",
            bg_color=self.theme["top"],
            size_factor=0.7
        )
        self.calc_btn.bind(on_press=lambda x: self.show("calc"))

        self.conv_btn = IOSButton(
            text="Conv",
            bg_color=self.theme["top"],
            size_factor=0.7
        )
        self.conv_btn.bind(on_press=lambda x: self.show("conv"))

        self.hist_btn = IOSButton(
            text="Hist",
            bg_color=self.theme["top"],
            size_factor=0.7
        )
        self.hist_btn.bind(on_press=lambda x: self.show("hist"))

        self.set_btn = IOSButton(
            text="Sets",
            bg_color=self.theme["top"],
            size_factor=0.7
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
        self.settings.update_theme()

        for btn in [self.calc_btn, self.conv_btn, self.hist_btn, self.set_btn]:
            btn.update_theme(
                self.theme["top"],
                (1, 1, 1, 1),
                0.7,
                self.theme.get("button_radius", 35)
            )

# =========================================================
# 🚀 APP
# =========================================================

class GlassCalculatorApp(App):
    icon = "icon.png"

    def build(self):
        return MainApp()

if __name__ == "__main__":
    GlassCalculatorApp().run()