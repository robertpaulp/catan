# Importing modules
import pygame
import time
import random
import sys
"""
sys.path.append("./BaseGame/Board/")
sys.path.append("./BaseGame/Hexagon Tiles/")
sys.path.append("./BaseGame/Robber/")
sys.path.append("./BaseGame/Dice/")"""
from BaseGame.Buttons.buttons import Button
from BaseGame.Board.board import Board
from BaseGame.CardsPrompt.cards_prompt import cards_prompt, CardsPrompt
from BaseGame.Dice.dice import Dice
from BaseGame.Hexagon_Tiles.hexagon_tile import HexagonTile
from BaseGame.Player.player import Player, players
from BaseGame.Road.road import Road, roads
from BaseGame.Road.road_events import RoadEventHandler
from BaseGame.Robber.robber import Robber
from BaseGame.Settlements.settlement import Settlement
from constants import *

class Game:
    @staticmethod
    def window_setup():
        pygame.init()

        window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Catan")
        icon = pygame.image.load("../Assets/icon.png")
        icon = pygame.transform.scale(icon, (32, 32))
        pygame.display.set_icon(icon)

        return window

    # --- Main loop ---
    @staticmethod
    def main(window):

        # Game loop variables
        dice_first_dsp = True
        running = True
        roll = [0, 0]

        # --- Background ---
        window.fill(LIGHT_CYAN_BLUE)

        # --- Hexagon grid ---
        HexagonTile.create_hexagon_grid(window, HEXAGON_X_AXIS, HEXAGON_Y_AXIS)

        # --- Robber ---
        Robber.create_robber(window)

        # --- Settlement Surfaces ---
        # Settlement.prepare_board_surfaces(window, base.HexagonTile.distinct_vertices, base.HexagonTile.hexagons)

        # --- Buttons ---
        road_button = Button.create_road_button()
        road_button.draw(window)
        settlement_button = Button.create_settlement_button()
        settlement_button.draw(window)
        special_card_button = Button.create_special_card_button()
        special_card_button.draw(window)

        print(HexagonTile.resourcesArray)
        print(HexagonTile.center_points)

        # --- Settlement Surfaces ---
        Settlement.prepare_board_surfaces(window, HexagonTile.distinct_vertices, HexagonTile.hexagons)

        # --- Roads ---

        # --- Player ---
        current_player = players[0]  # Current player

        current_player.draw_player(window)

         # --- Cards prompt ---
        cards_prompt.show_cards(window, current_player)

        END_START_ROUND = False

        while running:
            # TODO place roads only if you have enough resources
            # TODO trade mechanic

            GAME_START = False  # TODO dont pass as parameter to settlement_place!

            for player in players:
                if len(player.settlements) < 2:
                    GAME_START = True
                elif players.index(player) == 3 and END_START_ROUND is False:
                    print("intra")
                    GAME_START = True
                    END_START_ROUND = True

            if GAME_START and len(current_player.settlements) == 2:
                # Switch player
                current_player = players[(players.index(current_player) + 1) % len(players)]
                time.sleep(1)
                Board.redraw_board(window, roll, current_player)

            # --- Roads ---
            # This needs to activate only when the player is placing a road
            if len(current_player.roads) != 0:
                current_road = current_player.roads[-1]
            else:
                current_road = Road()
                current_player.roads.append(current_road)

            if current_road.is_placed is True:  # If we successfully placed a road, prepare a new one
                current_player.roads.append(Road())

            # --- Event loop ---
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if dice_btn.collidepoint(mouse_pos):
                        roll = [Dice.dice_roll(), Dice.dice_roll()]

                        # Acquire resources
                        for player in players:
                            player.acquire_cards(sum(roll))
                        Board.redraw_board(window, roll, current_player)

                        if sum(roll) == 7:
                            print("Robber")
                            Board.redraw_board(window, roll, current_player)
                        else:  # Switch to next player
                            current_player = players[(players.index(current_player) + 1) % len(players)]
                            time.sleep(3)
                            Board.redraw_board(window, roll, current_player)
                            # TODO switch to start of turn state

                    # TODO: after first click
                    for center_point in HexagonTile.center_points:
                        if center_point[0] - HEXAGON_SIDE / 3 <= mouse_pos[0] <= center_point[0] + HEXAGON_SIDE / 3:
                            if center_point[1] - HEXAGON_SIDE / 3 <= mouse_pos[1] <= \
                                    center_point[1] + HEXAGON_SIDE / 3:
                                print("Trying")
                                if Robber.check_move(mouse_pos):
                                    print("Moving")
                                    Robber.move_robber(window, center_point[0], center_point[1])
                            # base.HexagonTile.create_hexagon_grid(window, c.HEXAGON_X_AXIS, c.HEXAGON_Y_AXIS, False)
                            # TODO: Move robber
                            robber_pos = Robber.move_robber_event(window, running)

                            # --- Update board ---
                            Board.redraw_board(window, robber_pos)

                    # Prepare settlement event
                    Settlement.SettlementEventHandler.press(window)

                    # Place road event
                    RoadEventHandler.press(window, event, current_road, current_player)

                elif event.type == pygame.MOUSEBUTTONUP:
                    # Release road event
                    print("entered")

                    # If placing the road was unsuccessful, remove it from the list
                    if RoadEventHandler.place(window, event, current_road, current_player) == -1:
                        current_player.roads.pop()
                    else:
                        # If placing the road was successful, append it to the main list of roads as well
                        roads.append(current_road)

                    # Place settlement event
                    Settlement.SettlementEventHandler.place(window, roll, current_player, GAME_START)

                elif event.type == pygame.MOUSEMOTION:
                    # Dragging road event
                    Road.RoadEventHandler.drag(window, event, current_road)

                    # Hover settlement event TODO
                    # SettlementEventHandler.hover_settlement(window, roll)

            # --- Dice ---

            dice_btn = Board.roll_dice_btn(window)

            if dice_first_dsp:
                Dice.dices(window, [1, 1])
                dice_first_dsp = False

            Dice.dices(window, roll)

            pygame.display.update()

        pygame.quit()

    # TODO: remove this after testing
    if __name__ == "__main__":
        window = window_setup()
        main(window)
        exit()