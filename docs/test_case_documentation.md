# Test Cases

## Description

For convenience, test cases may be logically grouped together in what are called **Test Modules**, based on areas of testing. The use of Test Modules helps make the Traceability Matrices and archiving Test Cases more manageable.

---

## Test Case Template

### Test Case ID — Test Case Title

The Test Case ID may be any convenient identifier, as decided upon by the tester. Identifiers should follow a consistent pattern within Test Cases, and similar consistency should apply across Test Modules for the same project.

#### Description
The purpose of the Test Case, usually to verify a specific requirement. This is a high-level description of the test.

#### Test Inputs
Any required data input for the Test Case.

#### Expected Results
Describe the expected results and outputs from this Test Case. This may include any possible output, including exceptions or errors.

#### Dependencies
If correct execution of this Test Case depends on other Test Cases or external systems, those dependencies should be listed here.

#### Initialization
Any required setup of the system (software or hardware) before executing the test.

#### Test Steps
An ordered list of steps describing how to execute the Test Case.

#### Owner
The person(s) or team responsible for maintaining the Test Case.

---

Additional relevant data (e.g., tables, tools, configurations) may be included as needed to support execution.

---

# Test Modules

## Module 1: Freeze Spell

### TC-01 — Freeze Targets Opponent, Not Caster

#### Description
Verify that casting the Freeze spell records the opponent as the frozen color, not the caster.

#### Test Inputs
- Center square: `chess.E5`

#### Expected Results
- `game.freeze_effect_color == chess.BLACK`

#### Dependencies
- `python-chess` library
- `SpellChessGame` from `spell_logic.py`

#### Initialization
- Create a new `SpellChessGame` instance (White to move by default)

#### Test Steps
1. Call `game.cast_freeze(chess.E5)`
2. Assert `game.freeze_effect_color == chess.BLACK`

#### Owner
Team 11

---

### TC-02 — Freeze Decrements Charge on Cast

#### Description
Verify that casting the Freeze spell decrements the caster's charge count by 1.

#### Test Inputs
- Center square: `chess.E5`

#### Expected Results
- `game.freeze_remaining[chess.WHITE] == 4` (decremented from 5)

#### Dependencies
- `python-chess` library
- `SpellChessGame` from `spell_logic.py`

#### Initialization
- Create a new `SpellChessGame` instance (White starts with 5 freeze charges)

#### Test Steps
1. Call `game.cast_freeze(chess.E5)`
2. Assert `game.freeze_remaining[chess.WHITE] == 4`

#### Owner
Team 11

---

### TC-03a — White Starts with 5 Freeze Charges

#### Description
Verify that White begins the game with 5 freeze charges as specified.

#### Test Inputs
- None

#### Expected Results
- `game.freeze_remaining[chess.WHITE] == 5`

#### Dependencies
- `python-chess` library
- `SpellChessGame` from `spell_logic.py`

#### Initialization
- Create a new `SpellChessGame` instance

#### Test Steps
1. Read `game.freeze_remaining[chess.WHITE]`
2. Assert the value equals `5`

#### Owner
Team 11

---

### TC-03b — Black Starts with 5 Freeze Charges

#### Description
Verify that Black begins the game with 5 freeze charges as specified.

#### Test Inputs
- None

#### Expected Results
- `game.freeze_remaining[chess.BLACK] == 5`

#### Dependencies
- `python-chess` library
- `SpellChessGame` from `spell_logic.py`

#### Initialization
- Create a new `SpellChessGame` instance

#### Test Steps
1. Read `game.freeze_remaining[chess.BLACK]`
2. Assert the value equals `5`

#### Owner
Team 11

---

### TC-03c — Freeze Blocked at Zero Charges

#### Description
Verify that a player cannot cast Freeze when they have 0 charges remaining.

#### Test Inputs
- `freeze_remaining[WHITE] = 0`
- Center square: `chess.E5`

#### Expected Results
- `cast_freeze(chess.E5)` returns `False`

#### Dependencies
- `python-chess` library
- `SpellChessGame` from `spell_logic.py`

#### Initialization
- Create a new `SpellChessGame` instance
- Set `game.freeze_remaining[chess.WHITE] = 0`

#### Test Steps
1. Set `game.freeze_remaining[chess.WHITE] = 0`
2. Call `result = game.cast_freeze(chess.E5)`
3. Assert `result is False`

#### Owner
Team 11

---

### TC-03d — Freeze Returns True on Successful Cast

#### Description
Verify that `cast_freeze` returns `True` when all conditions for casting are satisfied.

#### Test Inputs
- Center square: `chess.E5`

#### Expected Results
- `cast_freeze(chess.E5)` returns `True`

#### Dependencies
- `python-chess` library
- `SpellChessGame` from `spell_logic.py`

#### Initialization
- Create a new `SpellChessGame` instance (White to move, 5 charges, cooldown = 0)

#### Test Steps
1. Call `result = game.cast_freeze(chess.E5)`
2. Assert `result is True`

#### Owner
Team 11

---

### TC-04 — Freeze Cooldown Set to 3 After Cast

#### Description
Verify that casting Freeze sets the caster's cooldown to 3 turns as specified.

#### Test Inputs
- Center square: `chess.E5`

#### Expected Results
- `game.freeze_cooldown[chess.WHITE] == 3`

#### Dependencies
- `python-chess` library
- `SpellChessGame` from `spell_logic.py`

#### Initialization
- Create a new `SpellChessGame` instance (White to move)

#### Test Steps
1. Call `game.cast_freeze(chess.E5)`
2. Assert `game.freeze_cooldown[chess.WHITE] == 3`

#### Owner
Team 11

---

### TC-05 — Freeze Blocked While on Cooldown

#### Description
Verify that a player cannot cast Freeze while their cooldown counter is greater than 0.

#### Test Inputs
- `freeze_cooldown[WHITE] = 2`
- Center square: `chess.E5`

#### Expected Results
- `cast_freeze(chess.E5)` returns `False`

#### Dependencies
- `python-chess` library
- `SpellChessGame` from `spell_logic.py`

#### Initialization
- Create a new `SpellChessGame` instance
- Manually set `game.freeze_cooldown[chess.WHITE] = 2`

#### Test Steps
1. Set `game.freeze_cooldown[chess.WHITE] = 2`
2. Call `result = game.cast_freeze(chess.E5)`
3. Assert `result is False`

#### Owner
Team 11

---

### TC-05b — Freeze Can Be Cast After Cooldown Reaches Zero

#### Description
Verify that a player may cast Freeze again once their cooldown has returned to 0 and they have remaining charges.

#### Test Inputs
- `freeze_cooldown[WHITE] = 0`
- `freeze_remaining[WHITE] = 3`
- Center square: `chess.D4`

#### Expected Results
- `cast_freeze(chess.D4)` returns `True`

#### Dependencies
- `python-chess` library
- `SpellChessGame` from `spell_logic.py`

#### Initialization
- Create a new `SpellChessGame` instance
- Set `game.freeze_cooldown[chess.WHITE] = 0`
- Set `game.freeze_remaining[chess.WHITE] = 3`

#### Test Steps
1. Set `game.freeze_cooldown[chess.WHITE] = 0`
2. Set `game.freeze_remaining[chess.WHITE] = 3`
3. Call `result = game.cast_freeze(chess.D4)`
4. Assert `result is True`

#### Owner
Team 11

---

### TC-06 — Freeze Cooldown Decrements at Turn Start

#### Description
Verify that the freeze cooldown decrements by 1 when `on_turn_start()` is called at the start of the caster's turn.

#### Test Inputs
- `freeze_cooldown[WHITE] = 3`
- Board turn: White to move

#### Expected Results
- `game.freeze_cooldown[chess.WHITE] == 2` after `on_turn_start()`

#### Dependencies
- `python-chess` library
- `SpellChessGame` from `spell_logic.py`

#### Initialization
- Create a new `SpellChessGame` instance
- Set `game.freeze_cooldown[chess.WHITE] = 3`
- Set `game.board.turn = chess.WHITE`

#### Test Steps
1. Set `game.freeze_cooldown[chess.WHITE] = 3`
2. Set `game.board.turn = chess.WHITE`
3. Call `game.on_turn_start()`
4. Assert `game.freeze_cooldown[chess.WHITE] == 2`

#### Owner
Team 11

---

### TC-07 — Freeze Blocked on Second Cast Same Turn

#### Description
Verify that a player may not cast Freeze more than once per turn; the second attempt must be rejected.

#### Test Inputs
- First cast center: `chess.E5`
- Second cast center: `chess.D4`

#### Expected Results
- First cast returns `True`
- Second cast returns `False`

#### Dependencies
- `python-chess` library
- `SpellChessGame` from `spell_logic.py`

#### Initialization
- Create a new `SpellChessGame` instance (White to move)

#### Test Steps
1. Call `game.cast_freeze(chess.E5)` (first cast)
2. Call `result = game.cast_freeze(chess.D4)` (second cast, same turn)
3. Assert `result is False`

#### Owner
Team 11

---

### TC-08 — Freeze Area Includes Center Square

#### Description
Verify that the 3×3 freeze area returned by `squares_in_3x3()` includes the center square that was passed as input.

#### Test Inputs
- Center square: `chess.E4`

#### Expected Results
- `chess.E4 in squares_in_3x3(chess.E4)`

#### Dependencies
- `squares_in_3x3` from `spell_logic.py`

#### Initialization
- None (pure function, no game state required)

#### Test Steps
1. Call `area = squares_in_3x3(chess.E4)`
2. Assert `chess.E4 in area`

#### Owner
Team 11

---

### TC-08b — Freeze Area Has 9 Squares for Interior Center

#### Description
Verify that `squares_in_3x3()` returns exactly 9 squares when the center is an interior square (not on an edge or corner).

#### Test Inputs
- Center square: `chess.E4` (interior)

#### Expected Results
- `len(squares_in_3x3(chess.E4)) == 9`

#### Dependencies
- `squares_in_3x3` from `spell_logic.py`

#### Initialization
- None

#### Test Steps
1. Call `area = squares_in_3x3(chess.E4)`
2. Assert `len(area) == 9`

#### Owner
Team 11

---

### TC-08c — Freeze Area Has Fewer Than 9 Squares at Corner

#### Description
Verify that `squares_in_3x3()` returns fewer than 9 squares when the center is a corner square, since part of the 3×3 area falls off the board.

#### Test Inputs
- Center square: `chess.A1` (corner)

#### Expected Results
- `len(squares_in_3x3(chess.A1)) < 9`

#### Dependencies
- `squares_in_3x3` from `spell_logic.py`

#### Initialization
- None

#### Test Steps
1. Call `area = squares_in_3x3(chess.A1)`
2. Assert `len(area) < 9`

#### Owner
Team 11

---

### TC-08d — Freeze Area Has Fewer Than 9 Squares at Edge

#### Description
Verify that `squares_in_3x3()` returns fewer than 9 squares when the center is on an edge of the board.

#### Test Inputs
- Center square: `chess.A4` (edge)

#### Expected Results
- `len(squares_in_3x3(chess.A4)) < 9`

#### Dependencies
- `squares_in_3x3` from `spell_logic.py`

#### Initialization
- None

#### Test Steps
1. Call `area = squares_in_3x3(chess.A4)`
2. Assert `len(area) < 9`

#### Owner
Team 11

---

### TC-08e — Freeze Area Includes All 8 Neighbours

#### Description
Verify that all 8 squares immediately surrounding the center square are included in the freeze area.

#### Test Inputs
- Center square: `chess.E4`

#### Expected Results
- All of D3, E3, F3, D4, F4, D5, E5, F5 are present in the returned area

#### Dependencies
- `squares_in_3x3` from `spell_logic.py`

#### Initialization
- None

#### Test Steps
1. Call `area = squares_in_3x3(chess.E4)`
2. Assert each of the 8 neighbour squares (D3, E3, F3, D4, F4, D5, E5, F5) is in `area`

#### Owner
Team 11

---

### TC-09 — Frozen Piece Excluded from Legal Moves

#### Description
Verify that a piece whose square falls inside the active freeze area cannot be selected as the origin of a move during the frozen side's turn.

#### Test Inputs
- `freeze_effect_color = chess.BLACK`
- `freeze_effect_squares = squares_in_3x3(chess.E7)` (covers the Black pawn on E7)
- `freeze_effect_plies_left = 1`
- Board turn: Black to move

#### Expected Results
- `chess.E7` is not present among the origin squares in `game.get_legal_moves()`

#### Dependencies
- `python-chess` library
- `SpellChessGame` from `spell_logic.py`
- `squares_in_3x3` from `spell_logic.py`

#### Initialization
- Create a new `SpellChessGame` instance
- Manually set `game.freeze_effect_color = chess.BLACK`
- Manually set `game.freeze_effect_squares = squares_in_3x3(chess.E7)`
- Manually set `game.freeze_effect_plies_left = 1`
- Set `game.board.turn = chess.BLACK`

#### Test Steps
1. Apply freeze effect state manually as described in Initialization
2. Call `legal_origins = {m.from_square for m in game.get_legal_moves()}`
3. Assert `chess.E7 not in legal_origins`

#### Owner
Team 11

---

### TC-10 — Freeze Effect Clears After Frozen Side Moves

#### Description
Verify that the active freeze effect is cleared after the frozen side completes their turn, so the freeze does not persist beyond 1 of the opponent's turns.

#### Test Inputs
- `freeze_effect_color = chess.BLACK`
- `freeze_effect_squares = {chess.E7}`
- `freeze_effect_plies_left = 1`
- Move: Black plays d5 (pushed directly via `board.push_san`)

#### Expected Results
- `game.freeze_effect_plies_left == 0`
- `game.freeze_effect_color is None`

#### Dependencies
- `python-chess` library
- `SpellChessGame` from `spell_logic.py`

#### Initialization
- Create a new `SpellChessGame` instance
- Manually set `freeze_effect_color = chess.BLACK`, `freeze_effect_squares = {chess.E7}`, `freeze_effect_plies_left = 1`
- Set `game.board.turn = chess.BLACK`

#### Test Steps
1. Apply freeze effect state manually as described in Initialization
2. Push Black's move directly via `game.board.push_san("d5")` (bypasses `make_move` to isolate this test)
3. Call `game.after_move_pushed()`
4. Assert `game.freeze_effect_plies_left == 0`
5. Assert `game.freeze_effect_color is None`

#### Owner
Team 11

---

### TC-11 — `is_frozen` Returns True for Frozen Square

#### Description
Verify that `is_frozen(sq, color)` returns `True` when the given color is actively frozen and the given square is within the frozen area.

#### Test Inputs
- `freeze_effect_color = chess.BLACK`
- `freeze_effect_squares = squares_in_3x3(chess.E5)` (includes E5)
- `freeze_effect_plies_left = 1`
- Query: `is_frozen(chess.E5, chess.BLACK)`

#### Expected Results
- `game.is_frozen(chess.E5, chess.BLACK) is True`

#### Dependencies
- `python-chess` library
- `SpellChessGame` from `spell_logic.py`
- `squares_in_3x3` from `spell_logic.py`

#### Initialization
- Create a new `SpellChessGame` instance
- Manually set `freeze_effect_color`, `freeze_effect_squares`, and `freeze_effect_plies_left`

#### Test Steps
1. Set `game.freeze_effect_color = chess.BLACK`
2. Set `game.freeze_effect_squares = squares_in_3x3(chess.E5)`
3. Set `game.freeze_effect_plies_left = 1`
4. Call `result = game.is_frozen(chess.E5, chess.BLACK)`
5. Assert `result is True`

#### Owner
Team 11

---

### TC-11b — `is_frozen` Returns False for Caster's Color

#### Description
Verify that `is_frozen(sq, color)` returns `False` for the caster's color, since the freeze only applies to the opponent.

#### Test Inputs
- `freeze_effect_color = chess.BLACK`
- `freeze_effect_squares = squares_in_3x3(chess.E5)`
- `freeze_effect_plies_left = 1`
- Query: `is_frozen(chess.E5, chess.WHITE)`

#### Expected Results
- `game.is_frozen(chess.E5, chess.WHITE) is False`

#### Dependencies
- `python-chess` library
- `SpellChessGame` from `spell_logic.py`

#### Initialization
- Create a new `SpellChessGame` instance
- Manually set freeze effect targeting `chess.BLACK`

#### Test Steps
1. Set `game.freeze_effect_color = chess.BLACK`
2. Set `game.freeze_effect_squares = squares_in_3x3(chess.E5)`
3. Set `game.freeze_effect_plies_left = 1`
4. Call `result = game.is_frozen(chess.E5, chess.WHITE)`
5. Assert `result is False`

#### Owner
Team 11

---

# Defect Summary

| Defect # | TC(s) | Location in Code | Description |
|----------|-------|------------------|-------------|
| D-01 | TC-01 | `cast_freeze` line 150 | `freeze_effect_color` set to caster (`turn`) instead of opponent (`not turn`) |
| D-02 | TC-02 | `cast_freeze` missing line | `freeze_remaining[turn]` never decremented after a successful cast |
| D-03 | TC-04 | `cast_freeze` line 154 | Freeze cooldown set to `2` instead of spec value `3` |
| D-04 | TC-06 | `on_turn_start` lines 221–222 | `freeze_cooldown` is never decremented; only `jump_cooldown` is |
| D-05 | TC-07 | `cast_freeze` missing line | `spell_casted_this_turn` never set to `True` (masked in practice by cooldown) |
| D-06 | TC-08, TC-08b, TC-09, TC-11 | `squares_in_3x3` lines 48–50 | Guard `if df==0 and dr==0: continue` excludes the center square from the area |