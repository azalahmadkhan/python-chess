# Test Scenario — Spell Chess P4

**Team 11** | Lee, Reznik, Trestka, Tuli  
**Date:** May 3, 2026  
**Scenario ID:** TS-01  
**Scenario Name:** White Casts Freeze, Black's Piece is Frozen for One Turn

---

## 1. Description of Setup

This scenario verifies the core Freeze spell flow end-to-end:
White casts Freeze targeting an area containing Black's e7 pawn, then makes
a standard move. On Black's next turn the frozen pawn cannot move, but Black
can move other non-frozen pieces. After Black completes one turn the freeze expires
and Black's pawn becomes freely movable again.

**Relevant specification rules (README.md):**
- "The freeze affects the opponent (not the caster)."
- "All opponent pieces whose square falls inside the frozen area cannot be moved on the opponent's next turn."
- "Duration: the freeze lasts for exactly 1 of the opponent's turns."
- "After casting there is a 3-turn cooldown before the same side can cast again."
- "Each cast costs 1 charge. Each side begins with 5."

**Relevant P2 EARS requirements:** 2.12, 3.12, 3.13, 3.14, 3.15

---

## 2. Step-by-Step Execution Procedure

**Pre-condition:** A new `SpellChessGame` is instantiated. It is White's turn.

| Step | Action | Code |
|------|--------|------|
| 1 | Confirm White has 5 freeze charges and 0 cooldown | `assert game.freeze_remaining[chess.WHITE] == 5` |
| 2 | White casts Freeze centred on E7 | `ok = game.cast_freeze(chess.E7)` |
| 3 | Confirm cast succeeded (True) | `assert ok is True` |
| 4 | Confirm freeze_effect_color is BLACK (the opponent) | `assert game.freeze_effect_color == chess.BLACK` |
| 5 | Confirm E7 is in the frozen squares | `assert chess.E7 in game.freeze_effect_squares` |
| 6 | Confirm White's charge count decreased by 1 | `assert game.freeze_remaining[chess.WHITE] == 4` |
| 7 | Confirm White's cooldown is now 3 | `assert game.freeze_cooldown[chess.WHITE] == 3` |
| 8 | White makes a standard move (e2→e4) | `game.board.push_san("e4"); game.after_move_pushed()` |
| 9 | Confirm it is now Black's turn | `assert game.board.turn == chess.BLACK` |
| 10 | Confirm E7 is frozen for Black | `assert game.is_frozen(chess.E7, chess.BLACK) is True` |
| 11 | Confirm E7 absent from legal moves | `origins = {m.from_square for m in game.get_legal_moves()}; assert chess.E7 not in origins` |
| 12 | Black moves a non-frozen piece (d7→d5) | `game.board.push_san("d5"); game.after_move_pushed()` |
| 13 | Confirm freeze has expired after Black's move | `assert game.freeze_effect_color is None` |
| 14 | Confirm E7 is back in legal moves (White's turn now, but flip to Black to confirm) | Set board to Black's turn; `assert chess.E7 in {m.from_square for m in game.get_legal_moves()}` |

---

## 3. Verification Checks

| Check | What is verified | Traceability |
|-------|-----------------|--------------|
| V-01 | `cast_freeze` returns `True` | Spec: cast succeeds when conditions met | README §Casting |
| V-02 | `freeze_effect_color == chess.BLACK` | Spec: "freeze affects the opponent" | README §Effect |
| V-03 | `chess.E7 in freeze_effect_squares` | Spec: "3×3 area centred on the chosen square" including center | README §Casting |
| V-04 | `freeze_remaining[WHITE] == 4` | Spec: "Each cast costs 1 charge" | README §Charges |
| V-05 | `freeze_cooldown[WHITE] == 3` | Spec: "3-turn cooldown after casting" | README §Cooldown |
| V-06 | `is_frozen(E7, BLACK) is True` | Spec: E7 is inside the area and Black is the frozen color | README §Effect |
| V-07 | `E7 not in get_legal_moves()` origins | Spec: "cannot be moved on the opponent's next turn" | README §Effect |
| V-08 | `freeze_effect_color is None` after Black's move | Spec: "exactly 1 of the opponent's turns" | README §Effect |

---

## 4. Defects Exposed by This Scenario

Running this scenario against version 0.5 of `spell_logic.py` reveals the following
failures, confirming bugs D-01 through D-06:

| Step | Check | Expected | Actual | Defect |
|------|-------|----------|--------|--------|
| 4 | `freeze_effect_color == BLACK` | `chess.BLACK` | `chess.WHITE` | D-01 |
| 5 | `E7 in freeze_effect_squares` | `True` | `False` | D-06 (center excluded) |
| 6 | `freeze_remaining[WHITE] == 4` | `4` | `5` | D-02 |
| 7 | `freeze_cooldown[WHITE] == 3` | `3` | `2` | D-03 |
| 10 | `is_frozen(E7, BLACK) is True` | `True` | `False` | D-01 + D-06 |
| 11 | `E7 not in legal move origins` | absent | present | D-01 + D-06 |

---

## 5. Traceability to Requirements

| Spec Rule | P2 EARS Req | TC(s) covering |
|-----------|-------------|----------------|
| Freeze affects opponent | 2.12 | TC-01 |
| 3×3 area includes center | 2.12 | TC-08, TC-08b |
| Charge cost 1 per cast | 2.12 | TC-02 |
| 3-turn cooldown | 3.15 | TC-04 |
| Frozen piece excluded from moves | 2.12 | TC-09, TC-11 |
| Freeze lasts 1 opponent turn | 3.14 | TC-10 |
