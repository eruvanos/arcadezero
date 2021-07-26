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
