import os
import random
import sys
import threading
import time

import art
import keyboard

width = 10
height = 10
game_field = [[] for _ in range(width * height)]
closer = False
IsActive = False
time_for_render = 0.1
snake_length = 1
x_snake = 0
y_snake = 0
direction = ""
index_previous = 0
score = 0
symbol_player = "📀"
symbol_coin = "😡"
symbol_background = "🕗"
direction_prev = ''
IsRestart = False
IsQuit = False


class Graphic:

    def printing():
        global closer
        while True:
            time.sleep(time_for_render)
            os.system("cls")
            x = 0
            y = width

            for i in range(height):
                print(Graphic.cleaning(str(game_field[x:y])) + "\n")
                x += width
                y += width
            art.tprint('Score: {}'.format(score))
            if closer:
                return 0

    def cleaning(self):

        symbols_to_remove = ["'", ",", "[", "]"]
        for symbol in symbols_to_remove:
            self = self.replace(symbol, '')
        return self.strip()

    @staticmethod
    def start():
        i = 0
        global closer
        while i < width * height:
            game_field[i] = symbol_background
            i += 1


class GameLogic:
    def convert_coordinates_to_index(x, y):
        return y * width + x

    def moving():
        global x_snake, y_snake, index_previous, direction, score, IsActive, snake_length, closer
        y_snake = 0
        x_snake = 0

        x_snake_previous = []
        y_snake_previous = []
        step = 0
        while True:

            time.sleep(time_for_render)
            time.sleep(0.2)
            if direction == "Down" and y_snake <= height:
                x_snake_previous.append(x_snake)
                y_snake_previous.append(y_snake)
                y_snake += 1
                if step > 1:
                    index_previous = GameLogic.convert_coordinates_to_index(x_snake_previous[step - snake_length],
                                                                            y_snake_previous[step - snake_length])
                if y_snake == height:
                    y_snake = 0
                index = GameLogic.convert_coordinates_to_index(x_snake, y_snake)
                if game_field[index] == symbol_coin:
                    score += 1
                    snake_length += 1
                    IsActive = False
                if game_field[index] == symbol_player:
                    closer = True
                game_field[index] = symbol_player

            if direction == "Up" and y_snake > -1:

                x_snake_previous.append(x_snake)
                y_snake_previous.append(y_snake)

                y_snake -= 1

                if y_snake == -1:
                    y_snake = height - 1
                if step > 1:
                    index_previous = GameLogic.convert_coordinates_to_index(x_snake_previous[step - 1],
                                                                            y_snake_previous[step - 1])
                index = GameLogic.convert_coordinates_to_index(x_snake, y_snake)
                if game_field[index] == symbol_coin:
                    score += 1
                    IsActive = False
                    snake_length += 1
                if game_field[index] == symbol_player:
                    closer = True
                game_field[index] = symbol_player

            if direction == "Right" and x_snake < width:

                x_snake_previous.append(x_snake)
                y_snake_previous.append(y_snake)
                x_snake += 1

                if x_snake == width:
                    x_snake = 0

                index = GameLogic.convert_coordinates_to_index(x_snake, y_snake)
                if game_field[index] == symbol_coin:
                    score += 1
                    IsActive = False
                    snake_length += 1
                if game_field[index] == symbol_player:
                    closer = True
                game_field[index] = symbol_player

            if direction == "Left" and x_snake < width:

                x_snake_previous.append(x_snake)
                y_snake_previous.append(y_snake)
                x_snake -= 1

                if x_snake == -1:
                    x_snake = width - 1

                index = GameLogic.convert_coordinates_to_index(x_snake, y_snake)
                if game_field[index] == symbol_coin:
                    score += 1
                    IsActive = False
                    snake_length += 1
                if game_field[index] == symbol_player:
                    closer = True
                game_field[index] = symbol_player
            GameLogic.coin_spawner(True)
            if direction != "":
                step += 1
                if step > 1:
                    index_previous = GameLogic.convert_coordinates_to_index(x_snake_previous[step - snake_length],
                                                                            y_snake_previous[step - snake_length])
                game_field[index_previous] = symbol_background
            if closer:
                return 0

    def coin_spawner(caused):
        global IsActive

        if caused and not IsActive:
            x_coin = random.randint(0, width - 1)
            y_coin = random.randint(0, height - 1)
            index = GameLogic.convert_coordinates_to_index(x_coin, y_coin)
            if game_field[index] == symbol_background:
                game_field[index] = symbol_coin
                IsActive = True
            else:
                IsActive = False

        if closer:
            return 0


def threader():
    graphic_thread = threading.Thread(target=Graphic.printing)
    move_logic = threading.Thread(target=GameLogic.moving)
    graphic_thread.start()
    move_logic.start()


class Binds:

    @staticmethod
    def quit():
        global closer
        closer = True

        sys.exit("Exit")

    def restart(self):
        global IsRestart, IsQuit
        if self == 'y':
            IsRestart = True
        elif self == 'n':
            IsQuit = True

    def change_direction(self):
        global direction, direction_prev

        match self:
            case "w":
                direction_prev = "Up"
                if direction != "Down":
                    direction = direction_prev
            case "a":
                direction_prev = "Left"
                if direction != "Right":
                    direction = direction_prev
            case "s":
                direction_prev = "Down"
                if direction != "Up":
                    direction = direction_prev
            case "d":
                direction_prev = "Right"
                if direction != "Left":
                    direction = direction_prev


def pressed_button():
    global direction
    keyboard.add_hotkey('esc', lambda: Binds.quit())
    keyboard.add_hotkey('w', lambda: Binds.change_direction("w"))
    keyboard.add_hotkey('a', lambda: Binds.change_direction("a"))
    keyboard.add_hotkey('s', lambda: Binds.change_direction("s"))
    keyboard.add_hotkey('d', lambda: Binds.change_direction("d"))
    keyboard.add_hotkey('y', lambda: Binds.restart('y'))
    keyboard.add_hotkey('n', lambda: Binds.restart('n'))


def main():
    Graphic.start()
    threader()
    pressed_button()


if __name__ == '__main__':
    main()
