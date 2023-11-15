import numpy as np
import agents
import random
import ui


class TicTacToeProblem():
    def __init__(self, depth_limit:int=2) -> None:
        self.depth_limit = depth_limit
        self.board = np.empty((3, 3), dtype=np.str_)
        self._ai_is_maximizer = True if random.randint(0, 1) == 1 else False
        self.agents = (agents.AiAgent(self._ai_is_maximizer), agents.PlayerAgent(not self._ai_is_maximizer))
        self.current_player = self.agents[0] if self.agents[0].is_maximizer else self.agents[1]
        self.gui = ui.TicTackToeGui()

        self.gui.draw_board(self.manage_game)

        if self.agents[0].is_maximizer:
            self.board = self.agents[0].agent_move(self, self.depth_limit)
        # endif

    # endinit

    def is_winner(self, player: agents.BaseAgent) -> bool:
        if (
               np.all(self.board[:, 0] == player.identifier)
            or np.all(self.board[:, 1] == player.identifier) 
            or np.all(self.board[:, 2] == player.identifier)
        ):
            # print(player.identifier, 'Wins!')
            return True
        # endif

        if (
               np.all(self.board[0, :] == player.identifier)
            or np.all(self.board[1, :] == player.identifier) 
            or np.all(self.board[2, :] == player.identifier)
        ):
            # print(player.identifier, 'Wins!')
            return True
        # endif

        if (
            (self.board[0,  0] == player.identifier and self.board[1, 1] == player.identifier and self.board[2, 2] == player.identifier)
            or (self.board[0, 2] == player.identifier and self.board[1, 1] == player.identifier and self.board[2, 0] == player.identifier)
        ):
            # print(player.identifier, 'Wins!')
            return True
        # endif

        return False
    # endmethod

    def is_tie(self):
        return not self.is_winner(self.agents[0]) and not self.is_winner(self.agents[1]) and np.all(self.board != '')
    # endmethod

    def game_over(self):
        return self.is_winner(self.agents[0]) or self.is_winner(self.agents[1]) or self.is_tie()
    # endmethod

    def check_for_winner(self):
        if self.is_winner(self.agents[1]):
            self.gui.winner_label.config(text='You win!', fg='green')
            self.gui.root.after(2000, self.gui.root.destroy)
            return True
        # endif

        if self.is_winner(self.agents[0]):
            self.gui.winner_label.config(text='YOU LOSE! I win!', fg='red')
            self.gui.root.after(2000, self.gui.root.destroy)
            return
        # endif

        if self.is_tie():
            self.gui.winner_label.config(text='Live to die another day...', fg='black')
            self.gui.root.after(2000, self.gui.root.destroy)
            return
        # endif
    # endmethod


    def manage_game(self, row: int, col: int):
        if not self.game_over():
            new_board = self.agents[1].agent_move(self, row, col)
            if new_board is None:
                return
            # endif
            else:
                self.board = new_board
                self.check_for_winner()

                if not self.game_over():
                    self.board = self.agents[0].agent_move(self, self.depth_limit)
                    self.check_for_winner()
                # endif
            # endelse
        # endif
        else:
            self.check_for_winner()
        # endelse
    # endmethod
# endclass