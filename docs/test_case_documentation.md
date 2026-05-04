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