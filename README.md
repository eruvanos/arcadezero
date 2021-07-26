# arcadezero
A beginner friendly layer on top of Arcade to create your very first game.

> Hint for arcade devs: ArcadeZero uses a wrapper of `arcade.Sprite` to reduce 
> the available methods and provide a easier start into game development.
> The main focus is to code your first game.

## Your first game
![Screenshot](docs/coin_paradise.png)



## Basic commands


```python
from arcadezero import *


# ...
```


## ZeroSprites

A sprite is a figure, which has a position and an image.
ArcadeZero come with a few default ones.

To start with the game, it is enough to create them. they will be drawn automatically.

```python
coin = Coin()
silvercoin = SilverCoin()
playermale = PlayerMale()
playerfemale = PlayerFemale()
bee = Bee()
saw = Saw()
```

### Functions

- `sprite.move(dx=0, dy=0)` - moves the Sprite into a direction
- `sprite.move_left(dx=0)` - moves the Sprite left
- `sprite.move_right(dx=0)` - moves the Sprite right
- `sprite.move_up(dy=0)` - moves the Sprite up
- `sprite.move_down(dy=0)` - moves the Sprite down
- `sprite.rotate(angle)` - rotates the Sprite

## Example from Screenshot

Move the player with the arrow keys, you can add more Coins by pressing `SPACE`.
Do not touch the saws!

```python
from arcadezero import *
from arcadezero import sounds

score = Score("Your score is: ", 0)

player = PlayerMale(200, 200)


@player.when_key(keys.SPACE)
def new_coin_on_space(player, key):
    Coin().with_rand_pos()


@player.while_key(keys.UP, keys.DOWN)
def player_move(player, key):
    if key == keys.UP:
        player.move_up(10)

    if key == keys.DOWN:
        player.move_down(10)


@player.while_key(keys.LEFT)
def player_move(player, key):
    player.move_left(10)


@player.while_key(keys.RIGHT)
def player_move(player, key):
    player.move_right(10)


@player.when_collide_with(Coin)
def player_move(player, coin):
    coin.remove()
    score + 20
    sounds.coin1.play()

    if len(Coin.all()) == 0:
        player.remove()
        show_message(f"You won with {score} points.")


@player.when_collide_with(Saw)
def player_move(player, saw):
    player.remove()
    show_message("You lost", color=colors.COAL)


@when_start
def setup():
    set_background_color(colors.CORN)

    # Lege 2 neue Coins an
    Coin().with_rand_pos()
    Coin().with_rand_pos()

    # Und 2 Gegner
    Saw().with_rand_pos()
    Saw().with_rand_pos()


run(1200, 800)
```
