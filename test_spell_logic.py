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

    def test_turn_change_to_black(self):
        game = SpellChessGame()
        game.make_move(chess.E2, chess.E3)
        assert game.current_turn() == chess.BLACK

    def test_turn_change_to_white(self):
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

    def test_white_casts_jump_on_white_piece(self):
        game = SpellChessGame()

        # White Turn - cast jump on white piece
        assert game.cast_jump(chess.A1, chess.B2)

    def test_white_cant_cast_jump_on_black_piece(self):
        game = SpellChessGame()

        # White Turn - cast jump on black piece
        assert not game.cast_jump(chess.C8, chess.C6)

    def test_black_casts_jump_on_black_piece(self):
        game = SpellChessGame()

        # Write Turn - move piece
        game.make_move(chess.E2, chess.E4)

        # Black Turn - cast jump on black piece
        assert game.cast_jump(chess.H8, chess.H6)

    def test_black_cant_cast_jump_on_white_piece(self):
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

    def test_cant_jump_to_ally_piece(self):
        game = SpellChessGame()
        assert not game.cast_jump(chess.B1, chess.D1)

    def test_cant_jump_to_opponent_piece(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.E4, chess.Piece.from_symbol('p'))
        assert not game.cast_jump(chess.E2, chess.E4)

class TestJumpChebyshevDistance:
    """The Jump spell should only be able to cast within chebyshev distance 2"""

    def test_cant_jump_3_forward(self):
        game = SpellChessGame()
        assert not game.cast_jump(chess.E2, chess.E5)

    def test_cant_jump_3_backward(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.E6, chess.Piece.from_symbol('P'))
        assert not game.cast_jump(chess.E6, chess.E3)

    def test_cant_jump_3_right(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.E3, chess.Piece.from_symbol('P'))
        assert not game.cast_jump(chess.E3, chess.H3)

    def test_cant_jump_3_left(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.E3, chess.Piece.from_symbol('P'))
        assert not game.cast_jump(chess.E3, chess.B3)

    def test_jump_helper_all_less_than_3(self):
        game = SpellChessGame()
        squares = squares_in_jump_range(chess.E4)
        for square in squares:
            assert max(abs(chess.square_file(chess.E2)) - abs(chess.square_file(square)), abs(chess.square_rank(chess.E2)) - abs(chess.square_rank(square))) <= 2

    def test_jump_helper_24_squares(self):
        game = SpellChessGame()
        squares = squares_in_jump_range(chess.E4)
        assert len(squares) == 24

class TestJumpTeleportsPiece:
    """The Jump spell should teleport the selected piece to the destination"""

    def test_jump_piece_no_longer_in_original_square(self):
        game = SpellChessGame()
        game.cast_jump(chess.E2, chess.D4)
        assert game.board.piece_at(chess.E2) == None

    def test_jump_piece_in_destination_square(self):
        game = SpellChessGame()
        game.cast_jump(chess.E2, chess.D4)
        assert game.board.piece_at(chess.D4) == chess.Piece.from_symbol('P')

class TestJumpIgnoresPiecesBetween:
    """The Jump spell should teleport the selected piece, ignoring pieces between original position and destination"""

    def test_can_jump_over_piece(self):
        game = SpellChessGame()
        assert game.cast_jump(chess.D1, chess.D3)

    def test_jump_piece_between_unchanged(self):
        game = SpellChessGame()
        game.cast_jump(chess.D1, chess.D3)
        assert game.board.piece_at(chess.D2) == chess.Piece.from_symbol('P')

class TestJumpCantCapture:
    """The Jump spell should be unable to capture other pieces"""

    def test_jump_capture_attempted_selected_piece_not_moved(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.E4, chess.Piece.from_symbol('p'))
        game.cast_jump(chess.E2, chess.E4)
        assert game.board.piece_at(chess.E2) == chess.Piece.from_symbol('P')

    def test_jump_capture_attempted_enemy_piece_unchanged(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.E4, chess.Piece.from_symbol('p'))
        game.cast_jump(chess.E2, chess.E4)
        assert game.board.piece_at(chess.E4) == chess.Piece.from_symbol('p')

class TestFreezeCharges:
    """Each side begins the game with 5 freeze charges. After casting a freeze spell, remaining charges reduces by 1. Cannot cast a freeze spell if remaining charges is zero. """

    def test_white_freeze_charges(self):
        game = SpellChessGame()
        assert game.freeze_remaining[chess.WHITE]== 5
        
    def test_black_freeze_charges(self):
        game = SpellChessGame()
        assert game.freeze_remaining[chess.BLACK]== 5
    
    def test_freeze_charge_reduce(self):
        game = SpellChessGame()
        initial_charges = game.freeze_remaining[chess.WHITE] 
        game.cast_freeze(chess.H8)
        assert game.freeze_remaining[chess.WHITE] == initial_charges - 1  
        
    def test_cannot_freeze_zero_charges(self):
        game = SpellChessGame()
        game.freeze_remaining[chess.WHITE]=0
        success = game.cast_freeze(chess.H8)
        assert success is False, "Cannot cast Freeze spell, when th echarges remaining is zero"
         
class TestJumpCharges:
    """Each side begins the game with 3 jump charges. After casting a jump spell, remaining charges reduces by 1. Cannot cast a jump spell if remaining charges is zero. """

    def test_white_jump_charges(self):
        game = SpellChessGame()
        assert game.jump_remaining[chess.WHITE]== 3

    def test_black_jump_charges(self):
        game = SpellChessGame()
        assert game.jump_remaining[chess.BLACK]== 3

    def test_jump_charge_reduce(self):
        game = SpellChessGame()
        initial_charges = game.jump_remaining[chess.WHITE] 
        game.cast_jump(chess.G2, chess.G4)
        assert game.jump_remaining[chess.WHITE] == initial_charges - 1
        
    def test_cannot_jump_zero_charges(self):
        game = SpellChessGame()
        game.jump_remaining[chess.WHITE]=0
        success = game.cast_jump(chess.G2, chess.G4)
        assert success is False, "Cannot cast Jump spell, when th echarges remaining is zero"

class TestNewGameResetsBoard:
    """Calling new_game() should bring the board back to the starting position."""

    def test_board_resets_after_moves(self):
        game = SpellChessGame()
        game.board.push_san("e4")
        game.new_game()
        assert game.board.fen() == chess.STARTING_FEN
        
class TestNewGameResetsFreezeCharges:
    """Calling new_game() should reset freeze charges to 5 for both sides."""

    def test_white_freeze_charges_new_game(self):
        game = SpellChessGame()
        game.board.push_san("e4")
        game.freeze_remaining[chess.WHITE]= 3
        game.new_game()
        assert game.freeze_remaining[chess.WHITE]== 5
        
    def test_black_freeze_charges_new_game(self):
        game = SpellChessGame()
        game.board.push_san("e4")
        game.freeze_remaining[chess.BLACK]= 3
        game.new_game()
        assert game.freeze_remaining[chess.BLACK]== 5
        
class TestNewGameResetsFreezeCooldown:
    """Calling new_game() should reset freeze cooldown to 0 for both sides."""

    def test_white_freeze_cooldown_new_game(self):
        game = SpellChessGame()
        game.board.push_san("e4")
        game.freeze_cooldown[chess.WHITE]= 3
        game.new_game()
        assert game.freeze_cooldown[chess.WHITE]== 0
        
    def test_black_freeze_cooldown_new_game(self):
        game = SpellChessGame()
        game.board.push_san("e4")
        game.freeze_cooldown[chess.BLACK]= 3
        game.new_game()
        assert game.freeze_cooldown[chess.BLACK]== 0
        
class TestNewGameResetsFreezeEffect:
    """Calling new_game() should remove any remaining freeze effects."""

    def test_white_freeze_cooldown_new_game(self):
        game = SpellChessGame()
        game.board.push_san("e4")
        game.freeze_effect_color == chess.WHITE
        game.new_game()
        assert game.freeze_effect_color == None
    
        
class TestNewGameResetsJumpCharges:
    """Calling new_game() should reset jump charges to 3 for both sides. """       
    
    def test_white_jump_charges(self):
        game = SpellChessGame()
        game.board.push_san("e4")
        game.jump_remaining[chess.WHITE]= 1
        game.new_game()
        assert game.jump_remaining[chess.WHITE]== 3
        
    def test_black_jump_charges(self):
        game = SpellChessGame()
        game.board.push_san("e4")
        game.jump_remaining[chess.BLACK]= 1
        game.new_game()
        assert game.jump_remaining[chess.BLACK]== 3
        
class TestNewGameResetsJumpCooldown:
    """Calling new_game() should reset jump cooldown to 0 for both sides. """       
    
    def test_white_jump_charges(self):
        game = SpellChessGame()
        game.board.push_san("e4")
        game.jump_cooldown[chess.WHITE]= 1
        game.new_game()
        assert game.jump_cooldown[chess.WHITE]== 0
        
    def test_black_jump_charges(self):
        game = SpellChessGame()
        game.board.push_san("e4")
        game.jump_cooldown[chess.BLACK]= 1
        game.new_game()
        assert game.jump_cooldown[chess.BLACK]== 0








