import inspect
import random
from collections import defaultdict
from typing import Callable, List

import arcade

# Simplified access
keys = arcade.key
colors = arcade.color
set_background_color = arcade.set_background_color

screen = arcade.get_screens()[0]
WIDTH = screen.width
HEIGHT = screen.height - 50  # Some space for top bar

# local constants
_arcade_colors = [getattr(arcade.color, color) for color in dir(arcade.color) if color.isupper()]


# simplifier
def is_even(value):
    return value % 2 == 0


def is_odd(value):
    return value % 2 == 1


def random_color():
    return random.choice(_arcade_colors)


def randint(start: int, end: int):
    return random.randint(start, end)


def rand_x():
    return random.randint(0, WIDTH)


def rand_y():
    return random.randint(0, HEIGHT)


def rand_pos():
    return rand_x(), rand_y()


# Global state
class _Global:
    all_sprites = arcade.SpriteList()
    all_zsprites: List["ZeroSprite"] = []
    all_non_sprites = []

    message = None
    message_color = colors.WHITE

    # Registered Callbacks
    on_start_callbacks = []


def when_start(func):
    _Global.on_start_callbacks.append(func)
    return func


def show_message(text: str, color=colors.WHITE):
    _Global.message = text
    _Global.message_color = color


def clear_message():
    _Global.message = None


# Sprite
class ZeroSprite:
    def __init__(self, img: str, x=0, y=0):
        self.sprite = arcade.Sprite(img, center_x=x, center_y=y)

        self._colliders = defaultdict(list)

        _Global.all_sprites.append(self.sprite)
        _Global.all_zsprites.append(self)
        self._when_key_bindings = defaultdict(list)
        self._while_key_bindings = defaultdict(list)

    @classmethod
    def all(cls):
        return [
            zsprite
            for zsprite in _Global.all_zsprites
            if type(zsprite) is cls
        ]

    def rotate(self, angle):
        self.sprite.angle += angle

    def remove(self):
        _Global.all_zsprites.remove(self)
        self.sprite.remove_from_sprite_lists()

    @property
    def center_x(self):
        return self.sprite.center_x

    @center_x.setter
    def center_x(self, value):
        self.sprite.center_x = value

    @property
    def center_y(self):
        return self.sprite.center_y

    @center_y.setter
    def center_y(self, value):
        self.sprite.center_y = value

    @property
    def position(self):
        return self.sprite.position

    @position.setter
    def position(self, position):
        self.sprite.position = position

    def with_rand_pos(self) -> "ZeroSprite":
        self.position = rand_pos()
        return self

    def move(self, dx=0, dy=0):
        cx, cy = self.sprite.position
        self.sprite.position = cx + dx, cy + dy

    def move_left(self, dx):
        self.move(dx=-dx)

    def move_right(self, dx):
        self.move(dx=dx)

    def move_up(self, dy):
        self.move(dy=dy)

    def move_down(self, dy):
        self.move(dy=-dy)

    def show(self):
        self.sprite.visible = True

    def hide(self):
        self.sprite.visible = False

    def check_collides(self, zsprite: "ZeroSprite") -> bool:
        return self.sprite.collides_with_sprite(zsprite.sprite)

    def check_collides_with_list(self, zsprites: List["ZeroSprite"]) -> List["ZeroSprite"]:
        return [
            zsprite
            for zsprite in zsprites
            if self is not zsprite and arcade.check_for_collision(self.sprite, zsprite.sprite)
        ]

    def when_collide_with(self, *types: type):
        def decor(func):
            for type in types:
                self._colliders[type].append(func)
                return func

        return decor

    def on_update(self, dt):
        # TODO maybe replace with bindings
        pass

    def when_update(self, func: Callable):
        if not inspect.signature(func).parameters:
            self.on_update = lambda dt: func()
        else:
            self.on_update = func
        return func

    def when_key(self, *keys):
        # Adds the listeners to the Global state
        def decor(func: Callable):
            for key in keys:
                self._when_key_bindings[key].append(func)
            return func

        return decor

    def while_key(self, *keys):
        # Adds the listeners to the Global state
        def decor(func: Callable):
            for key in keys:
                self._while_key_bindings[key].append(func)
            return func

        return decor


class Coin(ZeroSprite):
    def __init__(self, x=0, y=0):
        super().__init__(arcade.resources.image_coin_gold, x, y)


class SilverCoin(ZeroSprite):
    def __init__(self, x=0, y=0):
        super().__init__(arcade.resources.image_coin_silver, x, y)


class PlayerMale(ZeroSprite):
    def __init__(self, x=0, y=0):
        super().__init__(arcade.resources.image_male_adventurer_idle, x, y)


class PlayerFemale(ZeroSprite):
    def __init__(self, x=0, y=0):
        super().__init__(arcade.resources.image_female_adventurer_idle, x, y)


class Bee(ZeroSprite):
    def __init__(self, x=0, y=0):
        super().__init__(arcade.resources.image_bee, x, y)


class Saw(ZeroSprite):
    def __init__(self, x=0, y=0):
        super().__init__(arcade.resources.image_saw, x, y)


class Score:
    def __init__(self, text="Your score:", value=0, font_size=30, color=arcade.color.BLACK):
        self.text = text
        self.value = value
        self.font_size = font_size
        self.color = color

        self._visible = True

        _Global.all_non_sprites.append(self)

    def show(self):
        self._visible = True

    def hide(self):
        self._visible = False

    def inc(self, value):
        self.value += value

    def dec(self, value):
        self.value -= value

    def __add__(self, other):
        self.value += other
        return self

    def __sub__(self, other):
        self.value += other
        return self

    def __mul__(self, other):
        self.value *= other
        return self

    def __div__(self, other):
        self.value /= other
        return self

    def remove(self):
        _Global.all_non_sprites.remove(self)

    def draw(self):
        if self._visible:
            arcade.draw_text(
                text=self.text + str(self.value),
                start_x=0,
                start_y=arcade.get_window().height - self.font_size * 1.5,
                width=arcade.get_window().width,
                align="center",
                font_size=self.font_size,
                font_name=('calibri', 'arial'),
                color=self.color
            )

    def __str__(self):
        return str(self.value)


class _ZeroWindow(arcade.Window):
    """Singleton window"""
    pressed_keys = set()

    def on_draw(self):
        arcade.start_render()
        _Global.all_sprites.draw()

        for non_sprite in _Global.all_non_sprites:
            non_sprite.draw()

        if _Global.message:
            arcade.draw_text(
                _Global.message,
                0,
                HEIGHT // 2,
                width=WIDTH,
                font_size=40,
                align="center",
                color=_Global.message_color,
            )

    def on_update(self, delta_time: float):
        # Call key bindings
        for symbol in self.pressed_keys:
            for zsprite in _Global.all_zsprites:
                for func in zsprite._while_key_bindings[symbol]:
                    func(zsprite, symbol)

        # Resolve collision
        for zsprite in _Global.all_zsprites:
            for hit in zsprite.check_collides_with_list(_Global.all_zsprites):
                for collider in zsprite._colliders[type(hit)]:
                    collider(zsprite, hit)

        # call update
        for zsprite in _Global.all_zsprites:
            zsprite.on_update(delta_time)

    def on_key_press(self, symbol, modifier):
        self.pressed_keys.add(symbol)

        for zsprite in _Global.all_zsprites:
            for func in zsprite._when_key_bindings[symbol]:
                func(zsprite, symbol)

    def on_key_release(self, symbol, modifier):
        self.pressed_keys.remove(symbol)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        pass


def run(width=WIDTH, height=HEIGHT, title="Arcade"):
    global WIDTH, HEIGHT
    WIDTH = width
    HEIGHT = height

    window = _ZeroWindow(width, height, title=title, resizable=True)

    for func in _Global.on_start_callbacks:
        func()

    arcade.run()
