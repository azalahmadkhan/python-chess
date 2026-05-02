"""
Unit tests for Spell Chess game logic.

Run with:
    pytest test_spell_logic.py -v

These tests verify the Spell Chess rules described in SPELL_CHESS_RULES.md.
Each test creates a fresh SpellChessGame, sets up a position, performs an
action, and checks that the result matches the specification.
"""

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

class TestTurnOrder:
    """The game should start with white's turn, then switch to black, then back to white, etc. after each move"""

    def test_white_turn_starts(self):
        game = SpellChessGame()
        assert game.current_turn() == chess.WHITE

    def test_black_turn_second(self):
        game = SpellChessGame()
        game.make_move(chess.E2, chess.E3)
        assert game.current_turn() == chess.BLACK

    def test_white_turn_third(self):
        game = SpellChessGame()
        game.make_move(chess.E2, chess.E3)
        game.make_move(chess.E7, chess.E6)
        assert game.current_turn() == chess.WHITE

class TestJumpCastLimit:
    """The Jump spell should only be able to be cast once per turn"""

    def test_jump_updates_casted_flag(self):
        game = SpellChessGame()
        # White casts jump on pawn
        game.cast_jump(chess.E2, chess.D4)
        # game.jump_casted_this_turn should now be True
        assert game.jump_casted_this_turn

    def test_jump_cant_cast_twice(self):
        game = SpellChessGame()
        # White casts jump on rook
        game.cast_jump(chess.A1, chess.A3)
        # White should not be able to cast jump again
        assert not game.cast_jump(chess.E2, chess.D4)

    def test_jump_flag_resets_next_turn(self):
        game = SpellChessGame()

        # White Turn - Jump + Move
        game.cast_jump(chess.G2, chess.F4)
        game.make_move(chess.E2, chess.E4)

        # Black Turn - is able to jump
        assert not game.jump_casted_this_turn

    def test_jump_can_cast_next_turn(self):
        game = SpellChessGame()

        # White Turn - Jump + Move
        game.cast_jump(chess.G2, chess.F4)
        game.make_move(chess.E2, chess.E4)

        # Black Turn - is able to jump
        assert game.cast_jump(chess.A8, chess.B6)

class TestJumpOnOwnPieces:
    """The Jump spell should only be able to be cast on one's own pieces"""

    def test_white_jump_casts_on_white_piece(self):
        game = SpellChessGame()

        # White Turn - cast jump on white piece
        assert game.cast_jump(chess.A1, chess.B2)

    def test_white_jump_cant_cast_on_black_piece(self):
        game = SpellChessGame()

        # White Turn - cast jump on black piece
        assert not game.cast_jump(chess.C8, chess.C6)

    def test_black_jump_casts_on_black_piece(self):
        game = SpellChessGame()

        # Write Turn - move piece
        game.make_move(chess.E2, chess.E4)

        # Black Turn - cast jump on black piece
        assert game.cast_jump(chess.H8, chess.H6)

    def test_black_jump_cant_cast_on_white_piece(self):
        game = SpellChessGame()

        # Write Turn - move piece
        game.make_move(chess.E2, chess.E4)

        # Black Turn - cast jump on white piece
        assert not game.cast_jump(chess.C8, chess.C6)



