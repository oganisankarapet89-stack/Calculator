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
# 📱 MOBILE SETTINGS
# =========================================================

IS_MOBILE = platform in ("android", "ios")

if IS_MOBILE:
    Window.fullscreen = 'auto'
else:
    Window.size = (400, 700)

Window.clearcolor = (0, 0, 0, 1)

# =========================================================
# 💾 STORAGE
# =========================================================

store = JsonStore("settings.json")

# =========================================================
# 🌍 LANGUAGES
# =========================================================

TEXTS = {
    'en': {
        'calc': 'Calc',
        'conv': 'Conv',
        'hist': 'Hist',
        'sets': 'Sets',
        'language': 'Language',
        'button_size': 'Button Size',
        'themes': 'Themes',
        'clear_history': 'Clear History',
        'no_history': 'No history yet.\nMake some calculations!',
        'currency_converter': 'CURRENCY CONVERTER',
        'from': 'From:',
        'to': 'To:',
        'swap': 'SWAP',
        'update': 'UPDATE',
        'convert': 'CONVERT',
        'amount': 'Amount:',
        'popular': 'Popular currencies:',
        'update_rates': 'Click UPDATE to get real rates',
        'updated': 'Rates updated!',
        'no_internet': 'No internet! Using fallback rates',
        'not_supported': 'Currency not supported',
        'enter_number': 'Enter valid number',
        'dino_game': 'DINO GAME',
        'start_game': 'START GAME',
        'tap_move': '👆 Tap left/right to move',
        'game_over': 'GAME OVER!',
        'score': 'Score',
        'best': 'Best',
        'play_again': 'PLAY AGAIN',
        'exit': 'EXIT',
        'secret_code': '🎉 SECRET CODE: 1337 🎉'
    },
    'ru': {
        'calc': 'Кальк',
        'conv': 'Конв',
        'hist': 'Истор',
        'sets': 'Настр',
        'language': 'Язык',
        'button_size': 'Размер кнопок',
        'themes': 'Темы',
        'clear_history': 'Очистить историю',
        'no_history': 'Истории пока нет.\nСделайте вычисления!',
        'currency_converter': 'КОНВЕРТЕР ВАЛЮТ',
        'from': 'Из:',
        'to': 'В:',
        'swap': 'МЕНЯТЬ',
        'update': 'ОБНОВИТЬ',
        'convert': 'КОНВЕРТ',
        'amount': 'Сумма:',
        'popular': 'Популярные валюты:',
        'update_rates': 'Нажмите ОБНОВИТЬ для курсов',
        'updated': 'Курсы обновлены!',
        'no_internet': 'Нет интернета! Использую запасные курсы',
        'not_supported': 'Валюта не поддерживается',
        'enter_number': 'Введите число',
        'dino_game': 'ИГРА ДИНОЗАВР',
        'start_game': 'НАЧАТЬ ИГРУ',
        'tap_move': '👆 Нажми слева/справа для движения',
        'game_over': 'ИГРА ОКОНЧЕНА!',
        'score': 'Очки',
        'best': 'Рекорд',
        'play_again': 'СЫГРАТЬ СНОВА',
        'exit': 'ВЫХОД',
        'secret_code': '🎉 СЕКРЕТНЫЙ КОД: 1337 🎉'
    }
}

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
# 🦕 DINO GAME
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

        self.current_speed = 160
        self.is_running = False
        self.score = 0
        self.dino_x = 0
        self.dino_velocity = 0
        self.obstacles = []
        self.obstacle_timer = 0
        self.dino_size = (dp(40), dp(40))
        self.ground_y = dp(80)
        self.game_event = None

        Clock.schedule_once(self.setup_ui, 0.1)
        self.bind(size=self.update_positions)

    def t(self, key):
        return TEXTS[self.app.language].get(key, key)

    def setup_ui(self, dt):
        self.canvas.clear()
        self.clear_widgets()

        with self.canvas:
            Color(0.1, 0.15, 0.25, 1)
            self.sky = Rectangle(pos=(0, 0), size=self.size)
            Color(0.35, 0.25, 0.15, 1)
            self.ground = Rectangle(pos=(0, self.ground_y), size=(self.width, dp(8)))
            Color(0.2, 0.8, 0.2, 1)
            self.dino = RoundedRectangle(pos=(self.dino_x, self.ground_y - self.dino_size[1]), size=self.dino_size,
                                         radius=[dp(8)])
            Color(1, 1, 1, 1)
            self.eye = Ellipse(
                pos=(self.dino_x + self.dino_size[0] - dp(12), self.ground_y - self.dino_size[1] + dp(8)),
                size=(dp(8), dp(8)))
            Color(0, 0, 0, 1)
            self.pupil = Ellipse(
                pos=(self.dino_x + self.dino_size[0] - dp(10), self.ground_y - self.dino_size[1] + dp(10)),
                size=(dp(4), dp(4)))

        self.score_label = Label(text=f"{self.t('score')}: 0", font_size=sp(26), color=(1, 1, 1, 1),
                                 size_hint=(None, None), size=(dp(180), dp(45)))
        self.best_label = Label(text=f"{self.t('best')}: {self.high_score}", font_size=sp(20), color=(0.8, 0.8, 0.8, 1),
                                size_hint=(None, None), size=(dp(180), dp(35)))
        self.exit_btn = Button(text=self.t('exit'), size_hint=(None, None), size=(dp(70), dp(40)),
                               background_color=(0.7, 0.2, 0.2, 1), color=(1, 1, 1, 1), font_size=sp(15), bold=True,
                               background_normal='')
        self.exit_btn.bind(on_press=self.exit_game)
        self.add_widget(self.score_label)
        self.add_widget(self.best_label)
        self.add_widget(self.exit_btn)

        # Стартовое меню
        self.start_menu = BoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(280), dp(250)),
                                    spacing=dp(12))
        with self.start_menu.canvas.before:
            Color(0, 0, 0, 0.92)
            self.menu_bg = RoundedRectangle(size=self.start_menu.size, radius=[dp(20)])

        self.start_menu.add_widget(
            Label(text=f"🦕 {self.t('dino_game')} 🦕", font_size=sp(24), color=(0.2, 0.8, 0.2, 1), size_hint=(1, 0.4),
                  bold=True))

        self.start_btn = Button(text=self.t('start_game'), size_hint=(1, 0.35), background_color=(0.2, 0.6, 0.2, 1),
                                color=(1, 1, 1, 1), font_size=sp(18), bold=True, background_normal='')
        self.start_btn.bind(on_press=self.start_game)
        self.start_menu.add_widget(self.start_btn)

        inst_text = self.t('tap_move')
        self.start_menu.add_widget(
            Label(text=inst_text, font_size=sp(13), color=(0.8, 0.8, 0.8, 1), size_hint=(1, 0.2)))

        self.add_widget(self.start_menu)
        self.update_positions()

    def update_positions(self, *args):
        if hasattr(self, 'score_label'):
            self.score_label.pos = (self.width - dp(150), self.height - dp(60))
            self.best_label.pos = (self.width - dp(150), self.height - dp(95))
            self.exit_btn.pos = (dp(10), self.height - dp(50))
        if hasattr(self, 'start_menu') and self.start_menu.parent:
            self.start_menu.pos = (self.width // 2 - dp(140), self.height // 2 - dp(125))
            if hasattr(self, 'menu_bg'):
                self.menu_bg.pos = self.start_menu.pos
                self.menu_bg.size = self.start_menu.size
        if hasattr(self, 'game_over_menu') and self.game_over_menu and self.game_over_menu.parent:
            self.game_over_menu.pos = (self.width // 2 - dp(140), self.height // 2 - dp(120))
            if hasattr(self, 'go_bg'):
                self.go_bg.pos = self.game_over_menu.pos
                self.go_bg.size = self.game_over_menu.size

    def on_touch_down(self, touch):
        if hasattr(self, 'exit_btn') and self.exit_btn.collide_point(*touch.pos):
            return
        if hasattr(self, 'start_menu') and self.start_menu.parent:
            if hasattr(self, 'start_btn') and self.start_btn.collide_point(*touch.pos):
                self.start_game(None)
                return
            return
        if hasattr(self, 'game_over_menu') and self.game_over_menu and self.game_over_menu.parent:
            for child in self.game_over_menu.children:
                if isinstance(child, Button) and child.collide_point(*touch.pos):
                    child.dispatch('on_press')
                    return
            return
        if self.is_running:
            if touch.x < self.width / 2:
                self.dino_velocity = -400
            else:
                self.dino_velocity = 400

    def start_game(self, instance):
        if hasattr(self, 'start_menu') and self.start_menu.parent:
            self.remove_widget(self.start_menu)
        if hasattr(self, 'game_over_menu') and self.game_over_menu and self.game_over_menu.parent:
            self.remove_widget(self.game_over_menu)
            self.game_over_menu = None
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
        self.score_label.text = f"{self.t('score')}: 0"
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
            width = dp(15)
            height = dp(35)
            obs = {
                'x': random.randint(0, int(self.width - width)),
                'y': self.height,
                'width': width,
                'height': height,
                'speed': self.current_speed
            }
            with self.canvas:
                Color(0.3, 0.6, 0.1, 1)
                obs['rect'] = RoundedRectangle(pos=(obs['x'], obs['y']), size=(width, height), radius=[dp(5)])
            self.obstacles.append(obs)
        for obs in self.obstacles[:]:
            obs['y'] -= obs['speed'] * dt
            obs['rect'].pos = (obs['x'], obs['y'])
            if obs['y'] + obs['height'] < 0:
                self.obstacles.remove(obs)
                self.canvas.remove(obs['rect'])
                self.score += 10
                self.score_label.text = f"{self.t('score')}: {self.score}"
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.best_label.text = f"{self.t('best')}: {self.high_score}"
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
        self.game_over_menu = BoxLayout(orientation='vertical', size_hint=(None, None), size=(dp(260), dp(240)),
                                        spacing=dp(12))
        with self.game_over_menu.canvas.before:
            Color(0, 0, 0, 0.92)
            self.go_bg = RoundedRectangle(size=self.game_over_menu.size, radius=[dp(20)])
        self.game_over_menu.add_widget(
            Label(text=f"{self.t('game_over')}\n{self.t('score')}: {self.score}", font_size=sp(24),
                  color=(1, 0.3, 0.3, 1), size_hint=(1, 0.45), bold=True))
        again_btn = Button(text=self.t('play_again'), size_hint=(1, 0.3), background_color=(0.2, 0.6, 0.2, 1),
                           color=(1, 1, 1, 1), font_size=sp(18), bold=True, background_normal='')
        again_btn.bind(on_press=self.restart_game)
        self.game_over_menu.add_widget(again_btn)
        exit_btn2 = Button(text=self.t('exit'), size_hint=(1, 0.3), background_color=(0.7, 0.2, 0.2, 1),
                           color=(1, 1, 1, 1), font_size=sp(16), background_normal='')
        exit_btn2.bind(on_press=self.exit_game)
        self.game_over_menu.add_widget(exit_btn2)
        self.add_widget(self.game_over_menu)
        self.update_positions()

    def restart_game(self, instance):
        if self.parent:
            self.parent.remove_widget(self)
        new_game = DinoGame(self.app)
        self.app.content.clear_widgets()
        self.app.content.add_widget(new_game)


# =========================================================
# 💱 CONVERTER (ИСПРАВЛЕН - ScrollView)
# =========================================================

class Converter(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = "vertical"
        self.padding = dp(10)
        self.spacing = dp(10)
        self.rates_cache = {}

        # Создаём ScrollView и ОДИН контейнер внутри
        self.scroll = ScrollView(size_hint=(1, 1))
        self.container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=dp(15),
            padding=[dp(10), dp(10), dp(10), dp(20)]
        )
        self.container.bind(minimum_height=self.container.setter('height'))
        self.scroll.add_widget(self.container)  # Только ОДИН виджет в ScrollView
        self.add_widget(self.scroll)

        self.update_ui()

    def t(self, key):
        return TEXTS[self.app.language].get(key, key)

    def update_ui(self):
        self.container.clear_widgets()

        self.container.add_widget(
            Label(text=self.t('currency_converter'), font_size=sp(26), color=(1, 1, 1, 1), size_hint=(1, None),
                  height=dp(50), bold=True))

        # From
        row1 = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(60), spacing=dp(15))
        row1.add_widget(Label(text=self.t('from'), font_size=sp(20), color=(1, 1, 1, 1), size_hint=(0.2, 1)))
        self.from_currency = TextInput(text="USD", multiline=False, font_size=sp(24), size_hint=(0.8, 1),
                                       padding=[dp(15), dp(10)], background_color=(0.15, 0.15, 0.2, 1),
                                       foreground_color=(1, 1, 1, 1))
        row1.add_widget(self.from_currency)
        self.container.add_widget(row1)

        # To
        row2 = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(60), spacing=dp(15))
        row2.add_widget(Label(text=self.t('to'), font_size=sp(20), color=(1, 1, 1, 1), size_hint=(0.2, 1)))
        self.to_currency = TextInput(text="RUB", multiline=False, font_size=sp(24), size_hint=(0.8, 1),
                                     padding=[dp(15), dp(10)], background_color=(0.15, 0.15, 0.2, 1),
                                     foreground_color=(1, 1, 1, 1))
        row2.add_widget(self.to_currency)
        self.container.add_widget(row2)

        # Buttons
        row3 = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(55), spacing=dp(15))
        self.swap_btn = Button(text=self.t('swap'), size_hint=(0.33, 1), background_color=(0.3, 0.3, 0.5, 1),
                               color=(1, 1, 1, 1), font_size=sp(18), bold=True, background_normal='')
        self.swap_btn.bind(on_press=self.swap_currencies)
        self.update_btn = Button(text=self.t('update'), size_hint=(0.34, 1), background_color=(0.2, 0.6, 0.2, 1),
                                 color=(1, 1, 1, 1), font_size=sp(18), bold=True, background_normal='')
        self.update_btn.bind(on_press=self.update_rates)
        self.convert_btn = Button(text=self.t('convert'), size_hint=(0.33, 1), background_color=(0.8, 0.5, 0.2, 1),
                                  color=(1, 1, 1, 1), font_size=sp(18), bold=True, background_normal='')
        self.convert_btn.bind(on_press=self.convert)
        row3.add_widget(self.swap_btn)
        row3.add_widget(self.update_btn)
        row3.add_widget(self.convert_btn)
        self.container.add_widget(row3)

        # Amount
        row4 = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(60), spacing=dp(15))
        row4.add_widget(Label(text=self.t('amount'), font_size=sp(20), color=(1, 1, 1, 1), size_hint=(0.3, 1)))
        self.input = TextInput(text="1", multiline=False, font_size=sp(24), size_hint=(0.7, 1),
                               padding=[dp(15), dp(10)], background_color=(0.15, 0.15, 0.2, 1),
                               foreground_color=(1, 1, 1, 1), input_filter='float')
        row4.add_widget(self.input)
        self.container.add_widget(row4)

        # Result
        self.result = TextInput(readonly=True, font_size=sp(24), background_color=(0.1, 0.1, 0.15, 1),
                                foreground_color=(0.3, 0.9, 0.3, 1), padding=[dp(15), dp(20)], multiline=True,
                                size_hint=(1, None), height=dp(120), halign="center")
        self.container.add_widget(self.result)

        # Popular currencies
        popular_label = Label(text=self.t('popular'), color=(1, 1, 1, 1), size_hint=(1, None), height=dp(35),
                              font_size=sp(16), bold=True)
        self.container.add_widget(popular_label)

        popular_grid = GridLayout(cols=4, spacing=dp(8), size_hint=(1, None), height=dp(160))
        popular_currencies = ["USD", "EUR", "RUB", "GBP", "JPY", "CNY", "TRY", "KZT", "CAD", "AUD", "CHF", "INR", "BRL",
                              "MXN", "SGD", "AED"]

        for currency in popular_currencies:
            btn = Button(text=currency, font_size=sp(16), size_hint=(1, 1), background_normal='',
                         background_color=(0.25, 0.25, 0.35, 1), color=(1, 1, 1, 1))
            btn.bind(on_press=lambda x, c=currency: self.set_to_currency(c))
            popular_grid.add_widget(btn)

        self.container.add_widget(popular_grid)

        # Status
        self.status_label = Label(text=self.t('update_rates'), color=(0.7, 0.7, 0.7, 1), size_hint=(1, None),
                                  height=dp(30), font_size=sp(12))
        self.container.add_widget(self.status_label)

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
            self.status_label.text = "🔄 " + self.t('update_rates')
            self.status_label.color = (1, 1, 0, 1)
            response = requests.get("https://open.er-api.com/v6/latest/USD", timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.rates_cache = data["rates"]
                self.rates_cache["USD"] = 1.0
                self.status_label.text = "✅ " + self.t('updated')
                self.status_label.color = (0, 1, 0, 1)
                if self.input.text:
                    self.convert(None)
            else:
                self.use_fallback_rates()
        except:
            self.status_label.text = "⚠️ " + self.t('no_internet')
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
            self.status_label.text = "⚠️ " + self.t('update_rates')
            return
        try:
            amount = float(self.input.text)
            from_curr = self.from_currency.text.upper().strip()
            to_curr = self.to_currency.text.upper().strip()
            if from_curr not in self.rates_cache or to_curr not in self.rates_cache:
                self.result.text = "❌ " + self.t('not_supported')
                return
            amount_in_usd = amount / self.rates_cache[from_curr]
            converted_amount = amount_in_usd * self.rates_cache[to_curr]
            rate = self.rates_cache[to_curr] / self.rates_cache[from_curr]
            self.result.text = f"{amount:,.2f} {from_curr} = {converted_amount:,.2f} {to_curr}\n\n1 {from_curr} = {rate:.4f} {to_curr}\n1 {to_curr} = {1 / rate:.4f} {from_curr}"
            self.status_label.text = f"✅ {amount} {from_curr} → {converted_amount:.2f} {to_curr}"
        except:
            self.result.text = "❌ " + self.t('enter_number')

    def update_theme(self):
        self.convert_btn.background_color = self.app.theme["op"]
        self.result.foreground_color = (1, 1, 1, 1)
        self.update_ui()


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

        self.display = TextInput(readonly=True, multiline=False, halign="right", background_color=(0, 0, 0, 0),
                                 foreground_color=(1, 1, 1, 1), font_size=sp(44 * app.size_factor), size_hint=(1, 0.15),
                                 padding=[dp(18), dp(18)])
        self.add_widget(self.display)

        self.buttons_container = GridLayout(cols=1, spacing=dp(8), size_hint=(1, 0.85))
        self.add_widget(self.buttons_container)
        self.create_buttons()

    def create_buttons(self):
        self.buttons_container.clear_widgets()
        self.buttons = []
        self.button_rows = []

        layout = [["C", "+/-", "%", "/"], ["7", "8", "9", "*"], ["4", "5", "6", "-"], ["1", "2", "3", "+"],
                  ["0", ".", "="]]

        for row in layout:
            row_layout = GridLayout(cols=len(row), spacing=dp(8), size_hint=(1, None),
                                    height=dp(80 * self.app.size_factor))
            for text in row:
                if text in ["+", "-", "*", "/", "="]:
                    color = self.app.theme["op"]
                elif text == "C":
                    color = (0.6, 0.6, 0.6, 1)
                else:
                    color = self.app.theme["num"]
                btn = IOSButton(text=text, bg_color=color, size_factor=self.app.size_factor)
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

        self.history_box = TextInput(readonly=True, font_size=sp(20), background_color=(0, 0, 0, 0),
                                     foreground_color=(1, 1, 1, 1), padding=[dp(12), dp(12)])
        clear_btn = IOSButton(text=self.t('clear_history'), bg_color=(1, 0, 0, 1), size_factor=0.75)
        clear_btn.bind(on_press=self.clear_history)
        self.add_widget(clear_btn)
        self.add_widget(self.history_box)

    def t(self, key):
        return TEXTS[self.app.language].get(key, key)

    def update_history(self):
        history = self.app.calculator.history
        self.history_box.text = "\n".join(history[::-1]) if history else self.t('no_history')

    def clear_history(self, instance):
        self.app.calculator.history.clear()
        self.update_history()

    def update_theme(self):
        self.history_box.foreground_color = (1, 1, 1, 1)
        for child in self.children:
            if isinstance(child, IOSButton):
                child.update_theme((1, 0, 0, 1), (1, 1, 1, 1), 0.75, self.app.theme.get("button_radius", 35))


# =========================================================
# ⚙ SETTINGS (ИСПРАВЛЕН - ScrollView)
# =========================================================

class Settings(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.orientation = "vertical"
        self.padding = dp(12)
        self.spacing = dp(12)

        # ScrollView с ОДНИМ контейнером
        self.scroll = ScrollView(size_hint=(1, 1))
        self.container = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=None, padding=[0, 0, 0, dp(25)])
        self.container.bind(minimum_height=self.container.setter('height'))
        self.scroll.add_widget(self.container)  # Только ОДИН виджет
        self.add_widget(self.scroll)

        self.update_ui()

    def t(self, key):
        return TEXTS[self.app.language].get(key, key)

    def update_ui(self):
        self.container.clear_widgets()

        # Language selection
        self.container.add_widget(
            Label(text=self.t('language'), color=(1, 1, 1, 1), size_hint=(1, None), height=dp(35), font_size=sp(20)))

        lang_box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(50), spacing=dp(10))
        en_btn = Button(text="English", size_hint=(0.5, 1), background_color=(0.3, 0.5, 0.7, 1), color=(1, 1, 1, 1),
                        font_size=sp(18), background_normal='')
        en_btn.bind(on_press=lambda x: self.change_language('en'))
        ru_btn = Button(text="Русский", size_hint=(0.5, 1), background_color=(0.3, 0.5, 0.7, 1), color=(1, 1, 1, 1),
                        font_size=sp(18), background_normal='')
        ru_btn.bind(on_press=lambda x: self.change_language('ru'))
        lang_box.add_widget(en_btn)
        lang_box.add_widget(ru_btn)
        self.container.add_widget(lang_box)

        # Button size
        self.container.add_widget(
            Label(text=self.t('button_size'), color=(1, 1, 1, 1), size_hint=(1, None), height=dp(35), font_size=sp(20)))
        self.slider = Slider(min=0.7, max=1.4, value=self.app.size_factor, size_hint=(1, None), height=dp(35))
        self.slider.bind(value=self.change_size)
        self.container.add_widget(self.slider)
        self.size_value = Label(text=f"Scale: {self.app.size_factor:.2f}", color=(1, 1, 1, 1), size_hint=(1, None),
                                height=dp(25), font_size=sp(14))
        self.container.add_widget(self.size_value)

        # Themes
        self.container.add_widget(
            Label(text=self.t('themes'), color=(1, 1, 1, 1), size_hint=(1, None), height=dp(35), font_size=sp(20)))

        self.theme_buttons = []
        for theme_name in THEMES.keys():
            btn = IOSButton(text=theme_name, bg_color=THEMES[theme_name]["top"], size_factor=0.78)
            btn.height = dp(68)
            btn.font_size = sp(18)
            btn.bind(on_press=lambda instance, name=theme_name: self.change_theme(name))
            self.theme_buttons.append(btn)
            self.container.add_widget(btn)

    def change_language(self, lang):
        self.app.language = lang
        store.put("language", lang=lang)
        self.app.update_all()

    def change_size(self, instance, value):
        self.app.size_factor = value
        self.size_value.text = f"Scale: {value:.2f}"
        store.put("settings", size=value, theme=self.app.theme_name, language=self.app.language)
        self.app.update_all()

    def change_theme(self, theme_name):
        self.app.theme_name = theme_name
        self.app.theme = THEMES[theme_name]
        Window.clearcolor = self.app.theme["bg"]
        store.put("settings", size=self.app.size_factor, theme=theme_name, language=self.app.language)
        self.app.update_all()

    def update_theme(self):
        for btn in self.theme_buttons:
            btn.update_theme(THEMES[btn.text]["top"], (1, 1, 1, 1), 0.78, self.app.theme.get("button_radius", 35))


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
            self.language = data.get("language", "en")
        else:
            self.size_factor = 1
            self.theme_name = "Dark"
            self.language = "en"

        self.theme = THEMES[self.theme_name]
        Window.clearcolor = self.theme["bg"]

        # Верхняя панель
        top = GridLayout(cols=4, spacing=dp(6), padding=[dp(6), dp(6), dp(6), dp(6)], size_hint=(1, None),
                         height=dp(50))

        self.calc_btn = IOSButton(text=self.t('calc'), bg_color=self.theme["top"], size_factor=0.7)
        self.calc_btn.bind(on_press=lambda x: self.show("calc"))
        self.conv_btn = IOSButton(text=self.t('conv'), bg_color=self.theme["top"], size_factor=0.7)
        self.conv_btn.bind(on_press=lambda x: self.show("conv"))
        self.hist_btn = IOSButton(text=self.t('hist'), bg_color=self.theme["top"], size_factor=0.7)
        self.hist_btn.bind(on_press=lambda x: self.show("hist"))
        self.set_btn = IOSButton(text=self.t('sets'), bg_color=self.theme["top"], size_factor=0.7)
        self.set_btn.bind(on_press=lambda x: self.show("set"))

        top.add_widget(self.calc_btn)
        top.add_widget(self.conv_btn)
        top.add_widget(self.hist_btn)
        top.add_widget(self.set_btn)
        self.add_widget(top)

        # Контент
        self.content = BoxLayout(size_hint=(1, 1))
        self.calculator = Calculator(self)
        self.converter = Converter(self)
        self.history_screen = History(self)
        self.settings = Settings(self)
        self.content.add_widget(self.calculator)
        self.add_widget(self.content)

    def t(self, key):
        return TEXTS[self.language].get(key, key)

    def show(self, screen):
        self.content.clear_widgets()
        if screen == "calc":
            self.content.add_widget(self.calculator)
        elif screen == "conv":
            self.converter.update_ui()
            self.content.add_widget(self.converter)
        elif screen == "hist":
            self.history_screen.update_history()
            self.content.add_widget(self.history_screen)
        elif screen == "set":
            self.settings.update_ui()
            self.content.add_widget(self.settings)

    def update_all(self):
        Window.clearcolor = self.theme["bg"]

        self.calc_btn.text = self.t('calc')
        self.conv_btn.text = self.t('conv')
        self.hist_btn.text = self.t('hist')
        self.set_btn.text = self.t('sets')

        self.calculator.update_theme()
        self.calculator.resize_buttons()
        self.converter.update_theme()
        self.history_screen.update_theme()
        self.settings.update_theme()
        self.settings.update_ui()

        for btn in [self.calc_btn, self.conv_btn, self.hist_btn, self.set_btn]:
            btn.update_theme(self.theme["top"], (1, 1, 1, 1), 0.7, self.theme.get("button_radius", 35))


# =========================================================
# 🚀 APP
# =========================================================

class KarCul(App):
    icon = 'icon.png'
    def build(self):
        return MainApp()


if __name__ == "__main__":
    KarCul().run()