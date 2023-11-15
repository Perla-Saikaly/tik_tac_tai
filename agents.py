import numpy as np
# from problem import TicTacToeProblem

class BaseAgent():
    def __init__(self, is_maximizer: bool) -> None:
        self.is_maximizer: bool = is_maximizer
        self.identifier = 'X' if self.is_maximizer else 'O'
    # endinit
# endclass

class PlayerAgent(BaseAgent):
    def __init__(self, is_maximizer: bool) -> None:
        super().__init__(is_maximizer)
    # endinit

    def agent_move(self, state, row: int, col: int) -> np.ndarray:
        if (state.board[row, col] == ''):
            state.board[row, col] = self.identifier
            state.gui.labels[row, col].config(text=self.identifier, fg='blue')
            return state.board
        # endif
        return None
    # endmethod
# endclass

class AiAgent:
    def __init__(self, is_maximizer: bool) -> None:
        self.is_maximizer = is_maximizer
        self.identifier = 'X' if is_maximizer else 'O'
    # endinit

    def _get_subsequent_moves(self, board: np.ndarray) -> np.ndarray:
        remaining_moves = np.where(board == '')
        remaining_moves = np.array([remaining_moves[0], remaining_moves[1]])
        return remaining_moves.transpose()
    # endmethod

    def _min(self, state, alpha: int, beta: int, depth: int) -> int:
        min_eval = 2
        
        for move in self._get_subsequent_moves(state.board):
            state.board[tuple(move)] = state.agents[1].identifier
            min_eval = min(min_eval, self._dispatcher(state, True, alpha, beta, depth - 1))
            
            if min_eval <= alpha:
                state.board[tuple(move)] = ''
                return min_eval
            # endif

            state.board[tuple(move)] = ''
            beta = min(beta, min_eval)
        # endfor
        return min_eval
    # endmethod

    def _max(self, state, alpha: int, beta: int, depth: int) -> int:
        max_eval = -2

        for move in self._get_subsequent_moves(state.board):
            state.board[tuple(move)] = self.identifier
            max_eval = max(max_eval, self._dispatcher(state, False, alpha, beta, depth - 1))
            
            if max_eval >= beta:
                state.board[tuple(move)] = ''
                return max_eval
            # endif

            state.board[tuple(move)] = ''
            alpha = max(alpha, max_eval)
        # endfor
        return max_eval
    # endmethod

    def _dispatcher(self, state, next_is_maximizer: bool, alpha: int=-2, beta: int=2, depth: int=3) -> int:
        if (
            depth == 0 
            or state.is_winner(state.agents[1]) 
            or state.is_winner(state.agents[0]) 
            or state.is_tie()
        ):
            return self._evaluate_board(state)
        # endif

        if next_is_maximizer:
            return self._max(state, alpha, beta, depth)
        # endif
        else:
            return self._min(state, alpha, beta, depth)
        # endelse
    # endmethod

    def _evaluate_board(self, state):
        if state.is_winner(state.agents[1]):
            return -1
        # endif
        elif state.is_winner(state.agents[0]):
            return 1
        # endelif
        elif state.is_tie():
            return 0
        # endelif
        else:
            return 0  # Or some other heuristic evaluation of the board
        # endelse
    # endmethod

    def make_move(self, state, depth_limit: int=5) -> tuple:
        best_move = None
        best_eval = -2

        for move in self._get_subsequent_moves(state.board):
            state.board[tuple(move)] = self.identifier
            eval = self._dispatcher(state, False, depth=depth_limit)
            state.board[tuple(move)] = ''
            
            if eval > best_eval:
                best_eval = eval
                best_move = tuple(move)
            # endif
        # endfor
        return best_move
    # endmethod

    def agent_move(self, state, depth_limit: int = 5) -> np.ndarray:
        if not state.is_winner(self) and not state.is_tie():
            move = self.make_move(state, depth_limit)

            if move is not None:
                state.board[move] = self.identifier
                state.gui.labels[move].config(text=self.identifier, fg='red')
            # endif
        # endif
        return state.board
    # endmethod
# endclass
