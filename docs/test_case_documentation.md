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

# Test Case Example 
Use this as a reference when you make your own! 
*Delete before submission.*

## SB-001 — Test Freeze Target

#### Description
Verify that casting the Freeze spell targets the opponent's pieces and not the caster's.

#### Test Inputs
- Center square from the chessboard

#### Expected Results
- `game.freeze_effect_color` is `black`

#### Dependencies
- Chess library

#### Initialization
- A new `SpellChessGame` instance is created

#### Test Steps
1. Call `game.cast_freeze(chess.E5)`
2. Verify the return value is `True`
3. Check `game.freeze_effect_color`
4. Verify `game.is_frozen(chess.E2, chess.WHITE)` returns `False`
5. Verify `game.is_frozen(chess.E7, chess.BLACK)` returns `True` (E7 is within the 3x3 area)

---

## E.1.1.1 — Get List of Students for Valid GPC in GRADS

#### Description
Ensures that a valid GPC can access a list of their students.

#### Test Inputs
- StudentRecord database initialized with:
  - 29 CSCE students
  - 1 MATH student
- User database initialized with CSCE GPC "ggay"

#### Expected Results
- A list of 29 CSCE students is returned
- No exception is thrown

#### Dependencies
- None

#### Initialization
- All databases are loaded
- User "ggay" is already set in the system

#### Test Steps
1. Request the list of students from GRADS
2. Verify the list contains exactly 29 students
3. Verify all students have department "CSCE"

---

## E.1.1.2 — GPC Retrieves Student Record

#### Description
Ensures that a valid GPC can access the student record for a valid CSCE student.

#### Test Inputs

**Student Record:**
- ID: rbob
- First Name: Robert
- Last Name: Bob
- Department: CSCE
- Term Began: Fall 2013
- Degree Sought: PhD, Spring 2018
- Previous Degrees: BS, Spring 2008
- Advisor: Manton Matthews (CSCE)

**Committee:**
- Duncan Buell (CSCE)
- Jason Bakos (CSCE)
- Richard McGehee (MATH)

**Courses Taken:**
- nap734 — Naptime, 5 credits, Spring 2014, B
- csce513 — Computer Architecture, 3 credits, Fall 2013, A
- csce531 — Compiler Construction, 3 credits, Spring 2014, A

**Milestones:**
- Dissertation advisor selected
- Dissertation committee formed

**User:**
- CSCE GPC "ggay"

#### Expected Results
- The student record for "rbob" is returned with correct values
- No exception is thrown

#### Dependencies
- None

#### Initialization
- All databases are loaded
- User "ggay" is already set in the system

#### Test Steps
1. Request the student record for "rbob" from GRADS
2. Verify each field matches the expected values