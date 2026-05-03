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
        king = game.board.remove_piece_at(chess.E1)
        game.board.set_piece_at(chess.E6,king) #put the king in a position where it must move
        game.cast_freeze(chess.E5) 
        # Freeze the king's square, because of the bugged way freeze works White's freeze is needed to freeze White pieces 
        # And the center piece cannot be E6
        legal_moves = game.get_legal_moves()
        assert legal_moves == []
    def test_all_pieces_frozen(self):
        game = SpellChessGame()
        # Manually set every white piece to be frozen, by adding all their squares to frozen square set
        game.freeze_effect_color = chess.WHITE
        game.freeze_effect_plies_left = 2
        game.freeze_cooldown[chess.WHITE] = 2
        
        game.freeze_effect_squares = set((chess.A1,chess.B1,chess.C1,chess.D1,chess.E1,chess.F1,chess.G1,chess.H1,
                                          chess.A2,chess.B2,chess.C2,chess.D2,chess.E2,chess.F2,chess.G2,chess.H2))
        
        # See if any legal moves are available
        legal_moves = game.get_legal_moves()
        assert legal_moves == []
    
class TestVisualDisplay:
    
    def test_in_check(self):
        game = SpellChessGame()
        # Manually Move King into Check
        king = game.board.remove_piece_at(chess.E1)
        game.board.set_piece_at(chess.E6,king)
        status_text = game.status_text()
        assert "check" in status_text
    
    def test_no_check(self):
        game = SpellChessGame()
        status_text = game.status_text()
        assert "check" not in status_text
        
    def test_current_no_check(self):
        game = SpellChessGame()
        # Manually Move White King into Check
        king = game.board.remove_piece_at(chess.E1)
        game.board.set_piece_at(chess.E6,king)
        #Manually make current player Black
        game.board.turn = chess.BLACK
        status_text = game.status_text()
        assert "check" not in status_text
    
    def test_freeze_label_shows_remaining_cooldown(self):
        #Compare displayed cooldown to actual cooldown
        game = SpellChessGame()
        game.cast_freeze(chess.E5)
        freeze_info = game.freeze_info_text()
        assert f"cooldown {game.freeze_cooldown[game.board.turn]}" in freeze_info
        
    
    def test_freeze_label_shows_remaining_cooldown_init(self):
        #Compare displayed cooldown to actual cooldown
        game = SpellChessGame()
        freeze_info = game.freeze_info_text()
        assert f"cooldown " not in freeze_info
    
    def test_freeze_label_shows_remaining_charges_init(self):
        #Comparing the display to the actual system state not to the expected state, other tests handle that
        game = SpellChessGame()
        game.cast_freeze(chess.E5)
        freeze_info = game.freeze_info_text()
        assert f"Freeze: {game.freeze_remaining[game.board.turn]}" in freeze_info
        
    
    def test_freeze_label_shows_remaining_charges(self):
        game = SpellChessGame()
        game.cast_freeze(chess.E5)
        freeze_info = game.freeze_info_text()
        assert f"Freeze: {game.freeze_remaining[game.board.turn]}" in freeze_info
        
    
    def test_shows_pieces_frozen(self):
        game = SpellChessGame()
        game.cast_freeze(chess.E5)
        #because of the incorrect way freeze functions white pieces are frozen
        freeze_info = game.freeze_info_text()
        assert game.freeze_effect_color == chess.WHITE
        assert " — pieces in area are frozen" in freeze_info 
        
    def test_shows_pieces_not_frozen(self):
        game = SpellChessGame()
        game.cast_freeze(chess.E5)
        #because of the incorrect way freeze functions black pieces are not frozen
        freeze_info = game.freeze_info_text()
        #Manually make current player Black
        game.board.turn = chess.BLACK
        assert game.freeze_effect_color == chess.WHITE
        assert "— pieces in area are frozen" not in freeze_info 
        
    def test_shows_no_freeze(self):
        game = SpellChessGame()
        freeze_info = game.freeze_info_text()
        assert game.freeze_effect_color == None
        assert "— pieces in area are frozen" not in freeze_info 