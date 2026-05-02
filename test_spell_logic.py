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

class TestJumpSelectedPieceColor:
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

class TestJumpSelectedEmpty:
    """The Jump spell should not be able to cast on an empty square"""

    def test_jump_cant_cast_on_empty_square(self):
        game = SpellChessGame()
        assert not game.cast_jump(chess.E3, chess.F4)

class TestJumpSelectedKing:
    """The Jump spell should not be able to be cast on your king"""
    
    def test_jump_cant_cast_on_king(self):
        game = SpellChessGame()
        assert not game.cast_jump(chess.E1, chess.E3)

class TestJumpDestinationEmpty:
    """The Jump spell should only allow an empty destination"""

    def test_cant_jump_to_ally_destination(self):
        game = SpellChessGame()
        assert not game.cast_jump(chess.B1, chess.D1)

    def test_cant_jump_to_opponent_destination(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.E4, chess.Piece.from_symbol('p'))
        assert not game.cast_jump(chess.E2, chess.E4)

class TestJumpOutsideChebyshevDistance:
    """The Jump spell should only be able to cast within chebyshev distance 2"""

    def test_cant_jump_3_vertical_up(self):
        game = SpellChessGame()
        assert not game.cast_jump(chess.E2, chess.E5)

    def test_cant_jump_3_vertical_down(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.E6, chess.Piece.from_symbol('P'))
        assert not game.cast_jump(chess.E6, chess.E3)

    def test_cant_jump_3_horizontal_right(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.E3, chess.Piece.from_symbol('P'))
        assert not game.cast_jump(chess.E3, chess.H3)

    def test_cant_jump_3_horizontal_left(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.E3, chess.Piece.from_symbol('P'))
        assert not game.cast_jump(chess.E3, chess.B3)

    def test_jump_helper_respects_distance(self):
        game = SpellChessGame()
        squares = squares_in_jump_range(chess.E4)
        for square in squares:
            assert max(abs(chess.square_file(chess.E2)) - abs(chess.square_file(square)), abs(chess.square_rank(chess.E2)) - abs(chess.square_rank(square))) <= 2

class TestJumpTeleportsPiece:
    """The Jump spell should teleport the selected piece to the destination"""

    def test_piece_no_longer_in_original_place(self):
        game = SpellChessGame()
        game.cast_jump(chess.E2, chess.D4)
        assert game.board.piece_at(chess.E2) == None

    def test_piece_in_destination(self):
        game = SpellChessGame()
        piece = game.board.piece_at(chess.E2)
        game.cast_jump(chess.E2, chess.D4)
        assert game.board.piece_at(chess.D4) == piece

class TestJumpIgnoresPiecesBetween:
    """The Jump spell should teleport the selected piece, ignoring pieces between original position and destination"""

    def test_can_jump_over_piece(self):
        game = SpellChessGame()
        assert game.cast_jump(chess.D1, chess.D3)

    def test_jump_piece_between_unchanged(self):
        game = SpellChessGame()
        between_piece = game.board.piece_at(chess.D2)
        game.cast_jump(chess.D1, chess.D3)
        assert game.board.piece_at(chess.D2) == between_piece

class TestJumpCantCapture:
    """The Jump spell should be unable to capture other pieces"""

    def test_jump_capture_selected_piece_not_moved(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.E4, chess.Piece.from_symbol('p'))
        game.cast_jump(chess.E2, chess.E4)
        assert game.board.piece_at(chess.E2) == chess.Piece.from_symbol('P')

    def test_jump_capture_enemy_piece_unchanged(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.E4, chess.Piece.from_symbol('p'))
        game.cast_jump(chess.E2, chess.E4)
        assert game.board.piece_at(chess.E4) == chess.Piece.from_symbol('p')








