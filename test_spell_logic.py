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

class TestMovement:
    """Making a valid move should correctly change the position of the moved piece and shall properly capture enemy pieces at the destination"""

    def test_starting_square_of_moved_piece_empty(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.D4, chess.Piece.from_symbol('R'))

        game.make_move(chess.D4, chess.F4)
        assert game.board.piece_at(chess.D4) == None
    
    def test_moved_piece_at_destination_square(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.D4, chess.Piece.from_symbol('R'))

        game.make_move(chess.D4, chess.F4)
        assert game.board.piece_at(chess.F4) == chess.Piece.from_symbol('R')

    def test_capture_enemy_piece(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.D4, chess.Piece.from_symbol('R'))
        game.board.set_piece_at(chess.F4, chess.Piece.from_symbol('p'))

        game.make_move(chess.D4, chess.F4)
        assert game.board.piece_at(chess.F4) == chess.Piece.from_symbol('R')

    def test_capture_ally_piece_fails(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.D4, chess.Piece.from_symbol('R'))
        game.board.set_piece_at(chess.F4, chess.Piece.from_symbol('P'))

        game.make_move(chess.D4, chess.F4)
        assert game.board.piece_at(chess.D4) == chess.Piece.from_symbol('P')

class TestPawnMovement:
    """Pawns should follow standard pawn movement rules"""

    def test_white_pawn_move_forward(self):
        game = SpellChessGame()
        assert game.make_move(chess.E2, chess.E3)

    def test_black_pawn_move_forward(self):
        game = SpellChessGame()
        game.board.turn = chess.BLACK
        assert game.make_move(chess.D7, chess.D6)

    def test_pawn_move_forward_two_at_start(self):
        game = SpellChessGame()
        assert game.make_move(chess.E2, chess.E4)

    def test_pawn_move_forward_two_on_later_turn(self):
        game = SpellChessGame()
        game.make_move(chess.E2, chess.E4)
        game.make_move(chess.B7, chess.B6)
        assert game.make_move(chess.D2, chess.D4)

    def test_pawn_cant_move_forward_two_after_first_movement(self):
        game = SpellChessGame()
        game.make_move(chess.E2, chess.E3)
        game.make_move(chess.B7, chess.B6)
        assert not game.make_move(chess.E3, chess.E5)

    def test_pawn_enemy_piece_blocks(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.E3, chess.Piece.from_symbol('p'))
        assert not game.make_move(chess.E2, chess.E3)
        assert not game.make_move(chess.E2, chess.E4)

    def test_pawn_no_diagonal_movement(self):
        game = SpellChessGame()
        assert not game.make_move(chess.E2, chess.D3)
        assert not game.make_move(chess.E2, chess.F3)

    def test_pawn_no_backward_movement(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.D5, chess.Piece.from_symbol('P'))
        assert not game.make_move(chess.D5, chess.D4)
        assert not game.make_move(chess.D5, chess.C4)
        assert not game.make_move(chess.D5, chess.E4)

    def test_pawn_diagonal_capture(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.D3, chess.Piece.from_symbol('p'))
        game.board.set_piece_at(chess.E3, chess.Piece.from_symbol('p'))
        assert game.make_move(chess.C2, chess.D3)
        game.board.turn = chess.WHITE
        assert game.make_move(chess.F2, chess.E3)

class TestRookMovement:
    """Rooks should follow standard rook movement rules"""

    def test_rook_side_movement(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.D4, chess.Piece.from_symbol('R'))
        assert game.make_move(chess.D4, chess.G4)
        game.board.turn = chess.WHITE
        assert game.make_move(chess.G4, chess.G6)
        game.board.turn = chess.WHITE
        assert game.make_move(chess.G6, chess.C6)
        game.board.turn = chess.WHITE
        assert game.make_move(chess.C6, chess.C3)

    def test_rook_no_diagonal_movement(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.D4, chess.Piece.from_symbol('R'))
        assert not game.make_move(chess.D4, chess.C5)
        assert not game.make_move(chess.D4, chess.E5)
        assert not game.make_move(chess.D4, chess.C3)
        assert not game.make_move(chess.D4, chess.E3)

    def test_rook_blocked_by_piece(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.D3, chess.Piece.from_symbol('R'))
        game.board.set_piece_at(chess.F3, chess.Piece.from_symbol('p'))
        assert not game.make_move(chess.D3, chess.G3)

class TestBishopMovement:
    """Bishops should follow standard bishop movement rules"""

    def test_bishop_diagonal_movement(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.D4, chess.Piece.from_symbol('B'))
        assert game.make_move(chess.D4, chess.E3)
        game.board.turn = chess.WHITE
        assert game.make_move(chess.E3, chess.G5)
        game.board.turn = chess.WHITE
        assert game.make_move(chess.G5, chess.E7)
        game.board.turn = chess.WHITE
        assert game.make_move(chess.E7, chess.B4)

    def test_bishop_no_side_movement(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.D4, chess.Piece.from_symbol('B'))
        assert not game.make_move(chess.D4, chess.D5)
        assert not game.make_move(chess.D4, chess.E4)
        assert not game.make_move(chess.D4, chess.D3)
        assert not game.make_move(chess.D4, chess.C4)

    def test_bishop_blocked_by_piece(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.D3, chess.Piece.from_symbol('B'))
        game.board.set_piece_at(chess.F5, chess.Piece.from_symbol('p'))
        assert not game.make_move(chess.D3, chess.G6)

class TestQueenMovement:
    """Queens should follow standard queen movement rules"""

    def test_queen_side_movement(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.D4, chess.Piece.from_symbol('Q'))
        assert game.make_move(chess.D4, chess.G4)
        game.board.turn = chess.WHITE
        assert game.make_move(chess.G4, chess.G6)
        game.board.turn = chess.WHITE
        assert game.make_move(chess.G6, chess.C6)
        game.board.turn = chess.WHITE
        assert game.make_move(chess.C6, chess.C3)

    def test_queen_diagonal_movement(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.D4, chess.Piece.from_symbol('Q'))
        assert game.make_move(chess.D4, chess.E3)
        game.board.turn = chess.WHITE
        assert game.make_move(chess.E3, chess.G5)
        game.board.turn = chess.WHITE
        assert game.make_move(chess.G5, chess.E7)
        game.board.turn = chess.WHITE
        assert game.make_move(chess.E7, chess.B4)

    def test_bishop_blocked_by_piece(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.D3, chess.Piece.from_symbol('Q'))
        game.board.set_piece_at(chess.F3, chess.Piece.from_symbol('p'))
        game.board.set_piece_at(chess.F5, chess.Piece.from_symbol('p'))
        assert not game.make_move(chess.D3, chess.G3)
        assert not game.make_move(chess.D3, chess.G6)

class TestKnightMovement:
    """Knights should follow standard knight movement rules"""

    def test_knight_L_movement(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.E5, chess.Piece.from_symbol('N'))
        assert game.make_move(chess.E5, chess.D7) # forward left
        game.board.turn = chess.WHITE
        assert game.make_move(chess.D7, chess.C5) # back left
        game.board.turn = chess.WHITE
        assert game.make_move(chess.C5, chess.D3) # back right
        game.board.turn = chess.WHITE
        assert game.make_move(chess.D3, chess.F4) # right forward
        game.board.turn = chess.WHITE
        assert game.make_move(chess.F4, chess.D5) # left forward
        game.board.turn = chess.WHITE
        assert game.make_move(chess.D5, chess.B4) # left backward
        game.board.turn = chess.WHITE
        assert game.make_move(chess.B4, chess.C6) # forward right
        game.board.turn = chess.WHITE
        assert game.make_move(chess.C6, chess.E5) # right backward

    def test_knight_no_side_movement(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.D4, chess.Piece.from_symbol('N'))
        assert not game.make_move(chess.D4, chess.D5)
        assert not game.make_move(chess.D4, chess.E4)
        assert not game.make_move(chess.D4, chess.D3)
        assert not game.make_move(chess.D4, chess.C4)

    def test_knight_no_diagonal_movement(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.D4, chess.Piece.from_symbol('N'))
        assert not game.make_move(chess.D4, chess.C5)
        assert not game.make_move(chess.D4, chess.E5)
        assert not game.make_move(chess.D4, chess.C3)
        assert not game.make_move(chess.D4, chess.E3)

    def test_knight_can_jump_pieces(self):
        game = SpellChessGame()
        assert game.make_move(chess.B1, chess.C3)

class TestKingMovement:
    """Kings should follow standard queen movement rules"""

    def test_king_one_space_movement(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.E3, chess.Piece.from_symbol('K'))
        assert game.make_move(chess.E3, chess.D3)
        game.board.turn = chess.WHITE
        assert game.make_move(chess.D3, chess.D4)
        game.board.turn = chess.WHITE
        assert game.make_move(chess.D4, chess.E4)
        game.board.turn = chess.WHITE
        assert game.make_move(chess.E4, chess.E3)
        game.board.turn = chess.WHITE
        assert game.make_move(chess.E3, chess.D4)
        game.board.turn = chess.WHITE
        assert game.make_move(chess.D4, chess.E5)
        game.board.turn = chess.WHITE
        assert game.make_move(chess.E5, chess.F4)
        game.board.turn = chess.WHITE
        assert game.make_move(chess.F4, chess.E3)

    def test_king_no_two_space_movement(self):
        game = SpellChessGame()
        game.board.set_piece_at(chess.E5, chess.Piece.from_symbol('K'))
        game.board.set_piece_at(chess.D3, chess.Piece.from_symbol('K'))
        assert not game.make_move(chess.E5, chess.C5)
        assert not game.make_move(chess.E5, chess.C3)
        assert not game.make_move(chess.E5, chess.E3)
        assert not game.make_move(chess.E5, chess.G3)
        assert not game.make_move(chess.E5, chess.G5)
        assert not game.make_move(chess.D3, chess.B5)
        assert not game.make_move(chess.D3, chess.D5)
        assert not game.make_move(chess.D3, chess.F5)

class TestCastling:
    """Kings and rooks should be able to castle following standard chess castling rules"""

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
        game.board.turn = chess.BLACK
        assert game.cast_jump(chess.H8, chess.H6)

    def test_black_cant_cast_jump_on_white_piece(self):
        game = SpellChessGame()
        game.board.turn = chess.BLACK
        assert not game.cast_jump(chess.C1, chess.C3)

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

class TestJumpDestinationOccupied:
    """The Jump spell should not work if the destination square is occupied"""

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

class TestFreezeCooldown:
    """After Freeze spell, the caster enters a 3 turn cooldown. Cooldown reduced by 1 at the start of each of the caster's turn. Cannot freeze until cooldown reaches 0 again."""
    def test_freeze_cooldown(self):
        game = SpellChessGame()
        game.cast_freeze(chess.H8)
        game.make_move(chess.E2, chess.E3)
        assert game.freeze_cooldown[chess.WHITE]== 3
        
    def test_freeze_cooldown_reduction(self):
        game = SpellChessGame()
        game.cast_freeze(chess.H8)
        initial = game.freeze_cooldown[chess.WHITE]
        game.board.turn = chess.WHITE
        game.on_turn_start()
        assert game.freeze_cooldown[chess.WHITE]== initial - 1
        
    def test_freeze_cooldown_nonzero(self):
        game = SpellChessGame()
        game.freeze_cooldown[chess.WHITE]= 2
        success = game.cast_freeze(chess.H8)
        assert success is False
        
    def test_freeze_cooldown_zero(self):
        game = SpellChessGame()
        game.freeze_cooldown[chess.WHITE]= 0
        success = game.cast_freeze(chess.H8)
        assert success is True
        
        
class TestJumpCooldown:
    """After Jump spell, the caster enters a 2 turn cooldown. Cooldown reduced by 1 at the start of each of the caster's turn. Cannot jump until cooldown reaches 0 again."""
    def test_jump_cooldown(self):
        game = SpellChessGame()
        game.cast_jump(chess.G2, chess.G4)
        game.make_move(chess.E2, chess.E3)
        assert game.jump_cooldown[chess.WHITE]== 2
        
    def test_jump_cooldown_reduction(self):
        game = SpellChessGame()
        game.cast_jump(chess.G2, chess.G4)
        initial = game.jump_cooldown[chess.WHITE]
        game.board.turn = chess.WHITE
        game.on_turn_start()
        assert game.jump_cooldown[chess.WHITE]== initial - 1
        
    def test_jump_cooldown_nonzero(self):
        game = SpellChessGame()
        game.jump_cooldown[chess.WHITE]=2
        success = game.cast_jump(chess.G2, chess.G4)
        assert success is False
        
    def test_jump_cooldown_zero(self):
        game = SpellChessGame()
        game.jump_cooldown[chess.WHITE]= 0
        success = game.cast_jump(chess.G2, chess.G4)
        assert success is True








