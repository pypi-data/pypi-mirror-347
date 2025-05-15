# *FCI Info*
### **Id: `4509`**
### **Section: `4`**
### **Name: `علي عبدالسلام عبدالرحيم حسن الشوربجي`**
<hr>

# *Tasks Being Solved:*
* `Converting e-NFA to DFA`
* `Turing Machine Simulationg for Unary Addition `
* `just handle CFG input`
<hr>

# *Running the Code*

**There are two recommended ways to run and test the code:**

1. **Run the `main.py` file** located inside each folder. This will execute the predefined test cases.
2. **Run the unit testing files**. If the output is `OK`, it indicates that all tests have passed successfully.

##### `Note:` If you got an import error while running `nfa_to_dfa_tests.py`, just move the script into the `nfa_to_dfa` folder.
<hr>

### **Another way, but not recommended: Enter Your Input**

##### *NFA Input Format:* `states#alphabet#transitions#start_state#accept_states`

##### Components
- **states**: Semicolon-separated list of states  
  - **Example**: `q0;q1;q2`

- **alphabet**: Semicolon-separated list of input symbols  
  - **Example**: `a;b`

- **transitions**: Semicolon-separated list of transitions Each transition is written as
  - **Example**: `q0,a,q1;q1,b,q2;q2,a,q0`

- **start_state**: A single starting state  
  - **Example**: `q0`

- **accept_states**: Comma-separated list of accepting states  
  - **Example**: `q2,q3`
<hr>
