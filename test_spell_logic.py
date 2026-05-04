"""
Unit tests for Spell Chess game logic.

Run with:
    pytest test_spell_logic.py -v

These tests verify the Spell Chess rules described in SPELL_CHESS_RULES.md (README.md).
Each test is identified by a TC-XX ID, documented in docs/test_case_documentation.md.

Test classes are organized by feature:
    Freeze Spell  — TestFreezeTarget, TestFreezeCharges, TestFreezeCooldown,
                    TestFreezeOncePerTurn, TestFreezeArea, TestFreezeEffect
    Jump Spell    — TestJumpRange, TestJumpCharges, TestJumpCooldown,
                    TestJumpOncePerTurn, TestJumpRestrictions
    New Game      — TestNewGameReset
    Move Rules    — TestMoveLifecycle
    Display       — TestGameStateDisplay

Traceability: each test docstring cites the relevant README section or
P2 EARS requirement number.
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

# ================================================================== #
#  Freeze Spell — Charges                                            #
# ================================================================== #

class TestFreezeCharges:

# ================================================================== #
#  Freeze Spell — Cooldown                                           #
# ================================================================== #

class TestFreezeCooldown:

# ================================================================== #
#  Freeze Spell — Once Per Turn                                      #
# ================================================================== #

class TestFreezeOncePerTurn:

# ================================================================== #
#  Freeze Spell — Area                                               #
# ================================================================== #

class TestFreezeArea:

# ================================================================== #
#  Freeze Spell — Effect                                             #
# ================================================================== #

class TestFreezeEffect:

# ================================================================== #
#  Jump Spell — Range                                                #
# ================================================================== #

class TestJumpRange:

# ================================================================== #
#  Jump Spell — Charges                                              #
# ================================================================== #

class TestJumpCharges:

# ================================================================== #
#  Jump Spell — Cooldown                                             #
# ================================================================== #

class TestJumpCooldown:

# ================================================================== #
#  Jump Spell — Once Per Turn                                        #
# ================================================================== #

class TestJumpOncePerTurn:

# ================================================================== #
#  Jump Spell — Restrictions                                         #
# ================================================================== #

class TestJumpRestrictions:

# ================================================================== #
#  New Game Reset                                                    #
# ================================================================== #

class TestNewGameReset:

# ================================================================== #
#  Move Lifecycle                                                    #
# ================================================================== #

class TestMoveLifecycle:

# ================================================================== #
#  Game State Display                                                #
# ================================================================== #

class TestGameStateDisplay: