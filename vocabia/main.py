# main.py
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Line, Ellipse
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.animation import Animation
import sqlite3
import json

LabelBase.register(name="DefaultTC", fn_regular="assets/fonts/NotoSansCJKtc-Regular.otf")
Window.size = (360, 640)

class RoundedButton(ButtonBehavior, RelativeLayout):
    image_source = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg = RoundedRectangle(radius=[20])
        with self.canvas:
            self.img = RoundedRectangle(radius=[20])
        self.bind(pos=self.update_graphics, size=self.update_graphics, image_source=self.update_image_source)

    def update_graphics(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.img.pos = self.pos
        self.img.size = self.size

    def update_image_source(self, *args):
        self.img.source = self.image_source
        self.update_graphics()

class LoginScreen(Screen):
    def do_login(self):
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()
        if username and password:
            try:
                with open("data/users.json", "r", encoding="utf-8") as f:
                    users = json.load(f)
                if username in users and users[username]["password"] == password:
                    App.get_running_app().current_user = username
                    self.manager.current = "home"
                else:
                    print("\u274c 帳號或密碼錯誤")
            except FileNotFoundError:
                print("\u274c 找不到 data/users.json")
        else:
            print("\u274c 請輸入帳號密碼")

class SignUpScreen(Screen):
    def do_signup(self):
        self.manager.current = "login"

class HomeScreen(Screen):
    def on_enter(self):
        try:
            username = App.get_running_app().current_user
            self.ids.username_label.text = username
        except Exception as e:
            print("\u274c HomeScreen error:", e)

    def select_avatar(self):
        chooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg'])
        popup = Popup(title='選擇頭像', content=chooser, size_hint=(0.9, 0.9))
        def on_selection(_, selection):
            if selection:
                path = selection[0]
                self.ids.avatar_image.source = path
                popup.dismiss()
        chooser.bind(on_submit=on_selection)
        popup.open()

class SortScreen(Screen):
    def goto_toeic(self): print("➡️ TOEIC")
    def goto_gre(self): print("➡️ GRE")
    def goto_toefl(self): print("➡️ TOEFL")

class TeamScreen00(Screen):
    pass

class TeamScreen01(Screen):
    pass

class TeamScreen02(Screen):
    pass

class TeamScreen03(Screen):
    def on_enter(self):
        try:
            self.ids.team_info.clear_widgets()
            username = App.get_running_app().current_user
            with open("data/users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
            with open("data/team.json", "r", encoding="utf-8") as f:
                teams = json.load(f)
            user_data = users.get(username)
            if not user_data or not user_data.get("team"):
                self.ids.team_name_label.text = "未加入任何隊伍"
                return
            team_name = user_data["team"]
            self.ids.team_name_label.text = team_name
            members = teams.get(team_name, [])
            member_scores = [(member, users.get(member, {}).get("score", 0)) for member in members]
            member_scores.sort(key=lambda x: x[1], reverse=True)
            total_score = 0
            for member, score in member_scores:
                total_score += score
                row = BoxLayout(orientation="vertical", size_hint=(1, None), height=dp(70), padding=[10, 5])
                inner = BoxLayout(orientation="horizontal", spacing=10)
                inner.add_widget(Image(source="assets/icon_user.png", size_hint=(None, None), size=(dp(40), dp(40))))
                label = Label(
                    text=f"[b]{member}[/b]\n單字分數：{score}",
                    markup=True,
                    font_name="DefaultTC",
                    font_size="16sp",
                    halign="left",
                    valign="middle",
                    color=(0, 0, 0, 1)
                )
                label.bind(size=label.setter("text_size"))
                inner.add_widget(label)
                row.add_widget(inner)
                with row.canvas.after:
                    Color(0.7, 0.7, 0.7, 1)
                    Line(points=[row.x, row.y, row.right, row.y], width=1)
                self.ids.team_info.add_widget(row)
            self.ids.team_info.add_widget(Label(
                text=f"團隊總分：{total_score} 分",
                font_name="DefaultTC",
                font_size="18sp",
                size_hint=(1, None),
                height=dp(40),
                color=(0, 0, 0, 1)
            ))
        except Exception as e:
            print("\u274c team_03 載入失敗：", e)

class LevelScreen(Screen):
    def on_enter(self):
        self.load_levels()

    def load_levels(self):
        username = App.get_running_app().current_user
        with open("data/users.json", "r", encoding="utf-8") as f:
            users = json.load(f)
        user_data = users.get(username, {})
        progress = max(1, user_data.get("score", 0) + 1)

        area = self.ids.level_area
        area.clear_widgets()

        positions = [
            (self.center_x - 25, 200),
            (self.center_x - 75, 400),
            (self.center_x + 25, 600),
        ]

        for i, (x, y) in enumerate(positions, start=1):
            btn = Button(
                text=str(i),
                pos=(x, y),
                size_hint=(None, None),
                size=(50, 50),
                font_size=16,
                font_name="DefaultTC",
                background_normal='',
                background_color=(0, 0, 0, 0),
                on_press=lambda instance, n=i: self.goto_level(n)
            )
            btn.text_size = btn.size
            btn.halign = "center"
            btn.valign = "middle"
            btn.canvas.before.clear()
            with btn.canvas.before:
                Color(1, 1, 1, 1)
                Ellipse(pos=btn.pos, size=btn.size)
            with btn.canvas.after:
                Color(0.7, 0.7, 0.7, 1)
                Line(width=1, ellipse=(btn.x, btn.y, btn.width, btn.height))
            area.add_widget(btn)

        if 1 <= progress <= len(positions):
            px, py = positions[progress - 1]
            self.player = Image(
                source="assets/player.png",
                size_hint=(None, None),
                size=(30, 30),
                pos=(px + 10, py - 30)
            )
            area.add_widget(self.player)
            Clock.schedule_once(self.jump_player, 0.5)

    def jump_player(self, *args):
        if not hasattr(self, 'player'):
            return
        original_y = self.player.y
        anim = (
            Animation(y=original_y + 20, duration=0.15, t='out_quad') +
            Animation(y=original_y, duration=0.15, t='in_quad')
        )
        anim.start(self.player)


class MyApp(App):
    current_user = ""
    def build(self):
        Builder.load_file("screens/login_screen.kv")
        Builder.load_file("screens/signup_screen.kv")
        Builder.load_file("screens/home_screen.kv")
        Builder.load_file("screens/sort_screen.kv")
        Builder.load_file("screens/team_screen_00.kv")
        Builder.load_file("screens/team_screen_01.kv")
        Builder.load_file("screens/team_screen_02.kv")
        Builder.load_file("screens/team_screen_03.kv")
        Builder.load_file("screens/level_screen.kv")
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SignUpScreen(name="signup"))
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(SortScreen(name="sort"))
        sm.add_widget(TeamScreen00(name="team_00"))
        sm.add_widget(TeamScreen01(name="team_01"))
        sm.add_widget(TeamScreen02(name="team_02"))
        sm.add_widget(TeamScreen03(name="team_03"))
        sm.add_widget(LevelScreen(name="level"))
        sm.add_widget(Screen(name="level_1"))
        sm.add_widget(Screen(name="level_2"))
        sm.add_widget(Screen(name="level_3"))
        return sm

    def go_team_screen(self):
        username = self.current_user
        try:
            with open("data/users.json", "r", encoding="utf-8") as f:
                users = json.load(f)
            team = users.get(username, {}).get("team")
            if team:
                self.root.current = "team_03"
            else:
                self.root.current = "team_00"
        except Exception as e:
            print("❌ 團隊切換錯誤：", e)

if __name__ == "__main__":
    MyApp().run()
