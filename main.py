import os
import random
import sys
import threading
import time

import keyboard

game_field = [[], [], [], [], [],
              [], [], [], [], [],
              [], [], [], [], [],
              [], [], [], [], [],
              [], [], [], [], []]
closer = False

time_for_render = 0.1
snake_length = 1
x_snake = 0
y_snake = 0
direction = ""
index_previous = 0
coin = 0

IsActive = False


class Graphic:

    def printing():
        global closer
        while True:
            time.sleep(time_for_render)
            os.system("cls")
            x = 0
            y = 5

            for i in range(5):
                print(Graphic.cleaning(str(game_field[x:y])) + "\n")
                x += 5
                y += 5

            if closer:
                return 0

    def cleaning(self):

        symbols_to_remove = ["'", ",", "[", "]"]
        for symbol in symbols_to_remove:
            self = self.replace(symbol, ' ')
        return self.strip()

    @staticmethod
    def start():
        i = 0
        global closer
        while i < 25:
            game_field[i] = "□"
            i += 1


class GameLogic:
    def convert_coordinates_to_index(x, y, width):
        return y * width + x

    def moving():
        global x_snake, y_snake, index_previous, direction, coin, IsActive, snake_length, closer
        y_snake = 0
        x_snake = 0

        x_snake_previous = []
        y_snake_previous = []
        step = 0
        while True:

            time.sleep(time_for_render)
            time.sleep(0.2)
            if direction == "Down" and y_snake <= 5:
                x_snake_previous.append(x_snake)
                y_snake_previous.append(y_snake)
                y_snake += 1
                if step > 1:
                    index_previous = GameLogic.convert_coordinates_to_index(x_snake_previous[step - snake_length],
                                                                            y_snake_previous[step - snake_length], 5)
                if y_snake == 5:
                    y_snake = 0
                index = GameLogic.convert_coordinates_to_index(x_snake, y_snake, 5)
                if game_field[index] == '●':
                    coin += 1
                    snake_length += 1
                    IsActive = False
                if game_field[index] == '■':
                    closer = True
                game_field[index] = "■"

            if direction == "Up" and y_snake > -1:

                x_snake_previous.append(x_snake)
                y_snake_previous.append(y_snake)

                y_snake -= 1

                if y_snake == -1:
                    y_snake = 4
                if step > 1:
                    index_previous = GameLogic.convert_coordinates_to_index(x_snake_previous[step - 1],
                                                                            y_snake_previous[step - 1], 5)
                index = GameLogic.convert_coordinates_to_index(x_snake, y_snake, 5)
                if game_field[index] == '●':
                    coin += 1
                    IsActive = False
                    snake_length += 1
                if game_field[index] == '■':
                    closer = True
                game_field[index] = "■"

            if direction == "Right" and x_snake < 5:

                x_snake_previous.append(x_snake)
                y_snake_previous.append(y_snake)
                x_snake += 1

                if x_snake == 5:
                    x_snake = 0

                index = GameLogic.convert_coordinates_to_index(x_snake, y_snake, 5)
                if game_field[index] == '●':
                    coin += 1
                    IsActive = False
                    snake_length += 1
                if game_field[index] == '■':
                    closer = True
                game_field[index] = "■"

            if direction == "Left" and x_snake < 5:

                x_snake_previous.append(x_snake)
                y_snake_previous.append(y_snake)
                x_snake -= 1

                if x_snake == -1:
                    x_snake = 4

                index = GameLogic.convert_coordinates_to_index(x_snake, y_snake, 5)
                if game_field[index] == '●':
                    coin += 1
                    IsActive = False
                    snake_length += 1
                if game_field[index] == '■':
                    closer = True
                game_field[index] = "■"
            GameLogic.coin_spawner(True)
            if direction != "":
                step += 1
                if step > 1:
                    index_previous = GameLogic.convert_coordinates_to_index(x_snake_previous[step - snake_length],
                                                                            y_snake_previous[step - snake_length], 5)
                game_field[index_previous] = "□"
            if closer:
                return 0

    def coin_spawner(caused):
        global IsActive

        if caused and not IsActive:
            x_coin = random.randint(0, 4)
            y_coin = random.randint(0, 4)
            index = GameLogic.convert_coordinates_to_index(x_coin, y_coin, 5)
            if game_field[index] == "□":

                game_field[index] = "●"
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

    def change_direction(self):
        global direction

        match self:
            case "w":
                direction = "Up"
            case "a":
                direction = "Left"
            case "s":
                direction = "Down"
            case "d":
                direction = "Right"


def pressed_button():
    global direction
    keyboard.add_hotkey('esc', lambda: Binds.quit())
    keyboard.add_hotkey('w', lambda: Binds.change_direction("w"))
    keyboard.add_hotkey('a', lambda: Binds.change_direction("a"))
    keyboard.add_hotkey('s', lambda: Binds.change_direction("s"))
    keyboard.add_hotkey('d', lambda: Binds.change_direction("d"))


def main():
    Graphic.start()
    threader()
    pressed_button()


if __name__ == '__main__':
    main()
