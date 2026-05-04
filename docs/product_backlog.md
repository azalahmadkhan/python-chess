# Product Backlog — Spell Chess P4 Sprint

**Team 11** | Lee, Reznik, Trestka, Tuli  
**Sprint:** P4 Bug Verification Sprint (April 27 – May 4, 2026)  
**Product Owner:** Konrad Trestka 
**Format:** Agile Alliance User Story Template

---

## Backlog Items

### PB-01 — Freeze Spell Verification

**As a** player,  
**I want** the Freeze spell to correctly target the opponent's pieces, consume charges, apply the right cooldown, and include the center square in its 3×3 area,  
**So that** the spell behaves exactly as described in the game specification and cannot be exploited through implementation bugs.

**Acceptance Criteria:**
- `cast_freeze` sets `freeze_effect_color` to the opponent (not the caster)
- `freeze_remaining` decrements by 1 on each successful cast
- `freeze_cooldown` is set to 3 (not 2) after casting
- `on_turn_start` decrements `freeze_cooldown` each time the caster's turn begins
- `squares_in_3x3` includes the center square (9 squares for interior targets)
- A piece on a frozen square is absent from `get_legal_moves()`
- The freeze effect clears after exactly 1 of the opponent's turns

**Story Points:** 5  
**Priority:** High

---

### PB-02 — Jump Spell Verification

**As a** player,  
**I want** the Jump spell to enforce Chebyshev distance ≤ 2, prevent jumping the King, prevent landing on occupied squares, and apply a 2-turn cooldown,  
**So that** the Jump mechanic is fair and follows the specification precisely.

**Acceptance Criteria:**
- `squares_in_jump_range` uses `range(-2, 3)` (Chebyshev ≤ 2, not 3)
- `cast_jump` returns `False` when the target piece is the King
- `cast_jump` returns `False` when the destination square is occupied
- `jump_cooldown` is set to 2 (not 1) after casting

**Story Points:** 3  
**Priority:** High

---

### PB-03 — New Game and Turn Lifecycle Verification

**As a** player,  
**I want** `new_game()` to fully reset all game state (board, jump charges, freeze state) and `make_move()` to switch turns and allow en passant,  
**So that** starting a new game is always consistent and all standard chess rules are enforced.

**Acceptance Criteria:**
- `new_game()` calls `board.reset()` so the FEN matches `STARTING_FEN`
- `new_game()` resets `jump_remaining` to `{WHITE: 3, BLACK: 3}`
- `after_move_pushed()` does not double-flip `board.turn`
- `make_move()` allows en passant captures (diagonal pawn move to empty square)

**Story Points:** 3  
**Priority:** High

---

### PB-04 — Test Documentation and Process Artifacts

**As a** course evaluator,  
**I want** the team to produce thorough test case documentation, a test execution report, meeting minutes, and updated specification documents,  
**So that** the testing work is transparent, traceable, and consistent with Scrum process requirements.

**Acceptance Criteria:**
- All test cases documented in `docs/test_case_documentation.md` with ID, rule, inputs, expected/actual output, and defect flag
- Test execution report captures full pytest output with pass/fail per test
- 6 meeting minutes files with date, attendees, and discussion points
- Updated requirements document noting defects in P2 spec (BONUS)

**Story Points:** 5  
**Priority:** Medium

---

## Backlog Status

| ID | Title | Priority | Story Points | Status |
|----|-------|----------|--------------|--------|
| PB-01 | Freeze Spell Verification | High | 5 | In-Progress |
| PB-02 | Jump Spell Verification | High | 3 | In-Progress |
| PB-03 | New Game and Turn Lifecycle | High | 3 | In-Progress |
| PB-04 | Test Documentation and Process | Medium | 5 | In-Progress |
