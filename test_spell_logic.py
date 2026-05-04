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
    """Each side starts with 5 freeze charges; each successful cast costs 1."""

    def test_freeze_initial_charges_white(self):
        """TC-03a | Spec: 'Each side begins the game with 5 freeze charges.' (White)"""
        game = SpellChessGame()
        assert game.freeze_remaining[chess.WHITE] == 5

    def test_freeze_initial_charges_black(self):
        """TC-03b | Spec: 'Each side begins the game with 5 freeze charges.' (Black)"""
        game = SpellChessGame()
        assert game.freeze_remaining[chess.BLACK] == 5

    def test_freeze_decrements_charge_on_cast(self):
        """
        TC-02 | Spec: 'Each cast costs 1 charge.'
        Expected: freeze_remaining[WHITE] drops from 5 to 4 after one cast.
        DEFECT: freeze_remaining is never decremented inside cast_freeze.
        """
        game = SpellChessGame()
        game.cast_freeze(chess.E5)
        assert game.freeze_remaining[chess.WHITE] == 4

    def test_freeze_blocked_at_zero_charges(self):
        """TC-03c | Spec: 'When a player has 0 charges remaining, they cannot cast Freeze.'"""
        game = SpellChessGame()
        game.freeze_remaining[chess.WHITE] = 0
        result = game.cast_freeze(chess.E5)
        assert result is False

    def test_freeze_returns_true_on_success(self):
        """TC-03d | cast_freeze must return True when all conditions are satisfied."""
        game = SpellChessGame()
        result = game.cast_freeze(chess.E5)
        assert result is True

# ================================================================== #
#  Freeze Spell — Cooldown                                           #
# ================================================================== #

class TestFreezeCooldown:
    """After casting Freeze the caster enters a 3-turn cooldown."""

    def test_freeze_cooldown_set_to_three_after_cast(self):
        """
        TC-04 | Spec table: 'Freeze cooldown after casting: 3 turns.'
        Expected: freeze_cooldown[WHITE] == 3 immediately after cast.
        DEFECT: cast_freeze sets cooldown to 2 instead of 3.
        """
        game = SpellChessGame()
        game.cast_freeze(chess.E5)
        assert game.freeze_cooldown[chess.WHITE] == 3

    def test_freeze_blocked_while_on_cooldown(self):
        """TC-05 | Spec: 'The caster cannot cast Freeze again until the cooldown reaches 0.'"""
        game = SpellChessGame()
        game.freeze_cooldown[chess.WHITE] = 2
        result = game.cast_freeze(chess.E5)
        assert result is False

    def test_freeze_cooldown_decrements_on_caster_turn_start(self):
        """
        TC-06 | Spec: 'The cooldown decrements by 1 at the start of each of the caster's turns.'
        Action: manually call on_turn_start() with White to move.
        Expected: freeze_cooldown[WHITE] drops by 1.
        DEFECT: on_turn_start() only decrements jump_cooldown, never freeze_cooldown.
        """
        game = SpellChessGame()
        game.freeze_cooldown[chess.WHITE] = 3
        game.board.turn = chess.WHITE
        game.on_turn_start()
        assert game.freeze_cooldown[chess.WHITE] == 2

    def test_freeze_can_cast_after_cooldown_zero(self):
        """TC-05b | Freeze may be cast again once cooldown is 0 (and charges remain)."""
        game = SpellChessGame()
        game.freeze_cooldown[chess.WHITE] = 0
        game.freeze_remaining[chess.WHITE] = 3
        result = game.cast_freeze(chess.D4)
        assert result is True

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