"""
Unit tests for Spell Chess game logic.

Run with:
    pytest test_spell_logic.py -v

These tests verify the Spell Chess rules described in SPELL_CHESS_RULES.md.
Each test creates a fresh SpellChessGame, sets up a position, performs an
action, and checks that the result matches the specification.
"""
# This is Rohan's Branch
import chess
from spell_logic import SpellChessGame, squares_in_3x3, squares_in_jump_range


# ------------------------------------------------------------------ #
#  Demo tests — provided to students as examples                      #
# ------------------------------------------------------------------ #

class TestFreezeTarget:
    """Casting Freeze should mark the opponent's color as frozen."""

    def test_freeze_affects_opponent_not_caster(self):
        game = SpellChessGame()
        # White casts freeze
        game.cast_freeze(chess.E5)
        # The frozen color should be Black (the opponent), not White
        assert game.freeze_effect_color == chess.BLACK
        


class TestNewGameResetsBoard:
    """Calling new_game() should bring the board back to the starting position."""

    def test_board_resets_after_moves(self):
        game = SpellChessGame()
        game.board.push_san("e4")
        game.new_game()
        assert game.board.fen() == chess.STARTING_FEN


# ------------------------------------------------------------------ #
#  YOUR TESTS GO BELOW                                                #
#  Write tests that check the rules from SPELL_CHESS_RULES.md.        #
#  If a test fails, you've found a bug — document it!                 #
# ------------------------------------------------------------------ #

class TestFreezeCasting:
    def test_first_freeze_succesful(self):
        game = SpellChessGame()
        success = game.cast_freeze(chess.E5)
        assert success == True
        
    def test_second_freeze_fails(self):
        game = SpellChessGame()
        game.cast_freeze(chess.E5)
        success = game.cast_freeze(chess.A2)
        assert success == False
        
    def test_third_freeze_fails(self):
        game = SpellChessGame()
        game.cast_freeze(chess.E5)
        game.cast_freeze(chess.B2)
        success = game.cast_freeze(chess.A2)
        assert success == False
        
def test_freeze_affects_opponent_not_caster_black():
    game = SpellChessGame()
    # Black casts freeze
    game.board.turn = chess.BLACK
    game.cast_freeze(chess.E5)
    assert game.freeze_effect_color == chess.WHITE
    
def test_freeze_must_precede_move():
    game = SpellChessGame()
    move_success = game.make_move(chess.E2,chess.E4)
    assert move_success == True #check that move went off
    freeze_success = game.cast_freeze(chess.E5)
    assert freeze_success == False

class TestFreezeArea:
    def test_board_cent(self):
        game = SpellChessGame()
        game.cast_freeze(chess.E5)
        assert game.freeze_effect_squares == set((chess.E5,chess.E4,chess.E6,chess.D4,chess.D5,chess.D6,chess.F4,chess.F5,chess.F6))
    
    def test_board_corner(self):
        game = SpellChessGame()
        game.cast_freeze(chess.A1)
        assert game.freeze_effect_squares == set((chess.A1,chess.A2,chess.B1,chess.B2))
    
    def test_board_edge(self):
        game = SpellChessGame()
        game.cast_freeze(chess.H5)
        assert game.freeze_effect_squares == set((chess.H5,chess.H4,chess.H6,chess.G4,chess.G5,chess.G6))
        
class TestNoLegalUnfrozenMoves:        
    def test_king_in_check(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.E6,chess.KING,chess.WHITE) #put the king in a position where it must move
        game.cast_freeze(chess.E5) 
        # Freeze the king's square, because of the bugged way freeze works White's freeze is needed to freeze White pieces 
        # And the center piece cannot be E6
        legal_moves = game.get_legal_moves()
        assert legal_moves == None
    def test_all_pieces_frozen(self):
        pass
    
class TestVisualDisplay:
    def test_correct_turn_at_start(self):
        pass
    
    def check_correct_turn_move_two(self):
        pass
    
    def check_correct_turn_move_three(self):
        pass
    
    def test_white_in_check(self):
        pass
    
    def test_black_in_check(self):
        pass