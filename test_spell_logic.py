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
        
class TestCheckRules:
    def test_player_cannot_move_into_check(self):
        game = SpellChessGame()
        king = game.board.remove_piece_at(chess.E1)
        game.board.set_piece_at(chess.E5,king)
        #If King moves to E6 it goes into check
        result = game.make_move(chess.E5,chess.E6)
        assert result == False
        
    def test_player_cannot_ignore_check(self):
        game = SpellChessGame()
        king = game.board.remove_piece_at(chess.E1)
        game.board.set_piece_at(chess.E6,king)
        #King must move out of check
        result = game.make_move(chess.D2,chess.D4)
        assert result == False
        
    def test_checkmate_ends_game(self):
        game = SpellChessGame()
        game.board.remove_piece_at(chess.E2)
        game.board.remove_piece_at(chess.G7)
        game.board.remove_piece_at(chess.E1)
        #Have to manually set up fool's mate because make move doesn't wrok
        assert game.make_move(chess.D1,chess.H5) == True
        assert game.is_game_over() == True
        
    def test_player_cannot_reveal_check(self):
        game = SpellChessGame()
        b_queen = game.board.remove_piece_at(chess.D8)
        game.board.set_piece_at(chess.H4,b_queen)
        result = game.make_move(chess.F2,chess.F3)
        assert result == False
        
class TestDrawRules:
    def test_stalemate_conditions(self):
        game = SpellChessGame()
        #Remove every piece except the King
        game.board.remove_piece_at(chess.A2)
        game.board.remove_piece_at(chess.B2)
        game.board.remove_piece_at(chess.C2)
        game.board.remove_piece_at(chess.D2)
        game.board.remove_piece_at(chess.E2)
        game.board.remove_piece_at(chess.F2)
        game.board.remove_piece_at(chess.G2)
        game.board.remove_piece_at(chess.H2)
        game.board.remove_piece_at(chess.A1)
        game.board.remove_piece_at(chess.B1)
        game.board.remove_piece_at(chess.C1)
        game.board.remove_piece_at(chess.D1)
        game.board.remove_piece_at(chess.F1)
        game.board.remove_piece_at(chess.G1)
        game.board.remove_piece_at(chess.H1)
        #Set up position where King can't move
        queen = game.board.remove_piece_at(chess.D8)
        game.board.set_piece_at(chess.D6,queen)
        rook_1 = game.board.remove_piece_at(chess.A8)
        game.board.set_piece_at(chess.F6,rook_1)
        rook_2 = game.board.remove_piece_at(chess.H8)
        game.board.set_piece_at(chess.H2,rook_2)
        
        assert game.is_game_over() == True
        
    def test_no_mating_material(self):
        game = SpellChessGame()
        #Remove every piece except both Kings
        game.board.remove_piece_at(chess.A2)
        game.board.remove_piece_at(chess.B2)
        game.board.remove_piece_at(chess.C2)
        game.board.remove_piece_at(chess.D2)
        game.board.remove_piece_at(chess.E2)
        game.board.remove_piece_at(chess.F2)
        game.board.remove_piece_at(chess.G2)
        game.board.remove_piece_at(chess.H2)
        game.board.remove_piece_at(chess.A1)
        game.board.remove_piece_at(chess.B1)
        game.board.remove_piece_at(chess.C1)
        game.board.remove_piece_at(chess.D1)
        game.board.remove_piece_at(chess.F1)
        game.board.remove_piece_at(chess.G1)
        game.board.remove_piece_at(chess.H1)
        
        game.board.remove_piece_at(chess.A7)
        game.board.remove_piece_at(chess.B7)
        game.board.remove_piece_at(chess.C7)
        game.board.remove_piece_at(chess.D7)
        game.board.remove_piece_at(chess.E7)
        game.board.remove_piece_at(chess.F7)
        game.board.remove_piece_at(chess.G7)
        game.board.remove_piece_at(chess.H7)
        game.board.remove_piece_at(chess.A8)
        game.board.remove_piece_at(chess.B8)
        game.board.remove_piece_at(chess.C8)
        game.board.remove_piece_at(chess.D8)
        game.board.remove_piece_at(chess.F8)
        game.board.remove_piece_at(chess.G8)
        game.board.remove_piece_at(chess.H8)
        
        assert game.is_game_over() == True
    
class TestEnPassant:
    def test_en_passant_legal(self):
        game = SpellChessGame()
        # Move white pawn into correct position
        w_pawn = game.board.remove_piece_at(chess.H1)
        game.board.set_piece_at(chess.H5,w_pawn)
        game.board.turn = chess.BLACK
        assert game.make_move(chess.G7,chess.G5) == True #Set up en-passant
        game.board.turn = chess.WHITE
        assert game.make_move(chess.H5,chess.G6) == True #See if en-passant is successful
        
    
    def test_one_turn_limit(self):
        game = SpellChessGame()
        # Move white pawn into correct position
        w_pawn = game.board.remove_piece_at(chess.H1)
        game.board.set_piece_at(chess.H5,w_pawn)
        game.board.turn = chess.BLACK
        assert game.make_move(chess.G7,chess.G5) == True #Set up en-passant
        game.board.turn = chess.WHITE
        assert game.make_move(chess.E2,chess.E4) == True
        game.board.turn = chess.BLACK
        assert game.make_move(chess.E7,chess.E5) == True
        game.board.turn = chess.WHITE
        assert game.make_move(chess.H5,chess.G6) == False #See if en-passant is successful after the window has passed
        
    
class TestPromotion:
    def test_promotion_default(self):
        game = SpellChessGame()
        game.board.remove_piece_at(chess.H8)
        game.board.remove_piece_at(chess.H7)
        pawn = game.board.remove_piece_at(chess.H2)
        game.board.set_piece_at(chess.H7,pawn)
        assert game.make_move(chess.H7,chess.H8) == True #Does promotion go through
    def test_promoting_to_queen(self):
        game = SpellChessGame()
        game.board.remove_piece_at(chess.H8)
        game.board.remove_piece_at(chess.H7)
        pawn = game.board.remove_piece_at(chess.H2)
        game.board.set_piece_at(chess.H7,pawn)
        game.make_move(chess.H7,chess.H8,chess.QUEEN)
        piece = game.board.remove_piece_at(chess.H8)
        assert piece.piece_type == chess.QUEEN #Did pawn promote to queen?
    def test_promoting_to_bishop(self):
        game = SpellChessGame()
        game.board.remove_piece_at(chess.H8)
        game.board.remove_piece_at(chess.H7)
        pawn = game.board.remove_piece_at(chess.H2)
        game.board.set_piece_at(chess.H7,pawn)
        game.make_move(chess.H7,chess.H8,chess.BISHOP)
        piece = game.board.remove_piece_at(chess.H8)
        assert piece.piece_type == chess.BISHOP #Did pawn promote to bishop?
    def test_promoting_to_knight(self):
        game = SpellChessGame()
        game.board.remove_piece_at(chess.H8)
        game.board.remove_piece_at(chess.H7)
        pawn = game.board.remove_piece_at(chess.H2)
        game.board.set_piece_at(chess.H7,pawn)
        game.make_move(chess.H7,chess.H8,chess.KNIGHT)
        piece = game.board.remove_piece_at(chess.H8)
        assert piece.piece_type == chess.KNIGHT #Did pawn promote to knight?
    def test_promoting_to_rook(self):
        game = SpellChessGame()
        game.board.remove_piece_at(chess.H8)
        game.board.remove_piece_at(chess.H7)
        pawn = game.board.remove_piece_at(chess.H2)
        game.board.set_piece_at(chess.H7,pawn)
        game.make_move(chess.H7,chess.H8,chess.ROOK)
        piece = game.board.remove_piece_at(chess.H8)
        assert piece.piece_type == chess.ROOK #Did pawn promote to queen?