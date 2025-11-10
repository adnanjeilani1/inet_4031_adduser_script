# User Account Creation Scripts

**Course:** INET4031  
**Author:** Adnan Jeilani  
**Date:** November 2025

## Overview

This repository contains Python scripts for automated Linux user account creation from formatted input files. The scripts read user data from stdin, validate entries, and execute system commands to create accounts, set passwords, and assign group memberships.

---

## Files in This Repository

- **`create-users.py`** - Basic user creation script (runs all commands automatically)
- **`create-users2.py`** - Interactive user creation script with dry-run mode and step-by-step prompts
- **`create-users.input`** - Sample input file with user data
- **`create-users1.input`** - Additional sample input file
- **`README.md`** - This documentation file

---

## Prerequisites / Requirements

### System Requirements
- **Operating System:** Linux (tested on Ubuntu/Debian)
- **Python Version:** Python 3.x
- **Required Packages:** 
  - `python3` (installed by default on most Linux systems)
 

### System Permissions
- **Root/sudo access required** to create users, set passwords, and modify groups
- The scripts use the following system commands:
  - `/usr/sbin/adduser` - creates user accounts
  - `/usr/bin/passwd` - sets user passwords
  - `/usr/sbin/adduser` (with group) - adds users to groups

### File Permissions
Make the scripts executable:
```bash
chmod +x create-users.py
chmod +x create-users2.py
```

---

## Input File Format

Input files must follow this colon-separated format (similar to `/etc/passwd`):

```
username:password:lastname:firstname:groups
```

### Field Descriptions:
1. **username** - Login name for the user (e.g., `user04`)
2. **password** - Plain-text password (will be set for the account)
3. **lastname** - User's last name
4. **firstname** - User's first name
5. **groups** - Comma-separated list of groups, or `-` for no additional groups

### Special Rules:
- Lines starting with `#` are **comments** and will be skipped
- Lines without exactly 5 colon-separated fields are **invalid** and will be skipped
- Use `-` in the groups field if the user should not be added to any additional groups
- Multiple groups can be specified with commas (e.g., `group01,group02`)


**Explanation:**
- Lines 1-4: Valid entries that will be processed
- Line 5: Commented out (starts with `#`) - **skipped**
- Line 6: Missing password field (only 4 fields) - **skipped**

---

## create-users.py

### Description
Basic automated user creation script that processes all valid entries from an input file without user interaction.

### What It Does:
1. Reads user data line-by-line from standard input (stdin)
2. Skips commented lines (starting with `#`) and malformed entries
3. Extracts username, password, name fields, and groups
4. Creates user accounts with disabled password login initially
5. Sets the password for each account
6. Assigns users to specified groups
7. Executes all commands automatically

### Functions:

#### `main()`
- **Purpose:** Main execution function that processes input and creates users
- **Input:** Reads from `sys.stdin` (redirected from input file)
- **Process:**
  - Iterates through each line from stdin
  - Uses regex (`re.match("^#", line)`) to detect and skip comment lines
  - Splits each line by `:` delimiter into fields
  - Validates that exactly 5 fields are present
  - Extracts user information and constructs system commands
  - Executes `adduser`, `passwd`, and group assignment commands via `os.system()`
- **Output:** Creates user accounts on the system

### How to Run

#### Normal Run (Creates Users):
```bash
# Run with sudo to have permissions to create users
sudo python3 create-users.py < create-users.input

# Or if executable:
sudo ./create-users.py < create-users.input
```

#### Dry-Run Mode:
To see what commands would be executed without actually creating users, **comment out** the `os.system(cmd)` lines and **uncomment** the `#print cmd` lines in the script:

```python
# Before (normal run):
os.system(cmd)

# After (dry-run):
print(cmd)
# os.system(cmd)
```

Then run:
```bash
python3 create-users.py < create-users.input
```

### Verification Commands

After running the script, verify users were created:

```bash
# Check if users exist in /etc/passwd
grep user0 /etc/passwd

# Check group memberships
grep user0 /etc/group

# Check specific user details
id user04
```

### Removing Created Users

To delete users created by the script:

```bash
# Remove single user with home directory
sudo deluser --remove-home user04

# Remove all users from input file
for u in user04 user05 user06 user07; do
    sudo deluser --remove-home "$u"
done
```

---

## create-users2.py

### Description
Interactive user creation script with dry-run mode and step-by-step confirmation prompts.

### What It Does:
1. Reads user data from standard input upfront (allowing interactive prompts)
2. Prompts user to choose **dry-run mode** or **normal mode**
3. **Dry-run mode:** Shows what would be executed and prompts for confirmation at each step
4. **Normal mode:** Automatically creates all users without prompts
5. Uses `/dev/tty` for prompts so it works even with stdin redirection

### Functions:

#### `run_cmd(cmd, dry_run)`
- **Purpose:** Execute or simulate command execution based on mode
- **Parameters:**
  - `cmd` (string) - The shell command to execute
  - `dry_run` (boolean) - If True, only prints command; if False, executes it
- **Behavior:**
  - Dry-run: Prints `"DRY-RUN: Would run: <command>"`
  - Normal: Executes command via `os.system(cmd)`

#### `prompt_yes_no(question)`
- **Purpose:** Display Y/N prompt and get user response from terminal
- **Parameters:**
  - `question` (string) - The question to ask the user
- **Returns:** 
  - `True` if user enters 'Y' or 'y'
  - `False` if user enters 'N' or 'n'
- **Special Feature:** Reads from `/dev/tty` instead of stdin, allowing interactive prompts even when stdin is redirected from a file
- **Validation:** Loops until user enters valid Y or N response

#### `main()`
- **Purpose:** Main execution function with interactive control flow
- **Process:**
  1. Reads all lines from stdin using `sys.stdin.readlines()`
  2. Prompts user: "Run in DRY-RUN mode (no actual changes) (Y/N):"
  3. For each valid user entry:
     - Displays user information
     - **In dry-run mode:** Prompts before each action (create account, set password, add to each group)
     - **In normal mode:** Automatically executes all actions without prompts
  4. Skips commented lines and malformed entries
  5. Creates users, sets passwords, and assigns groups based on mode

### How to Run

#### Dry-Run Mode (Recommended First):
```bash
# Run the script with input redirection
./create-users2.py < create-users.input

# When prompted "Run in DRY-RUN mode (no actual changes) (Y/N):", enter: Y
# Then answer Y or N for each step to see what would happen
```

**Output example:**
```
Run in DRY-RUN mode (no actual changes) (Y/N): Y

============================================================
Processing user: user04
  Full name: First04 Last04
  Groups: group01
============================================================
Create account for user04 (Y/N): Y
==> Creating account for user04...
DRY-RUN: Would run: /usr/sbin/adduser --disabled-password --gecos 'First04 Last04,,,' user04
Set password for user04 (Y/N): Y
==> Setting the password for user04...
DRY-RUN: Would run: /bin/echo -ne 'pass04\npass04' | /usr/bin/sudo /usr/bin/passwd user04
Assign user04 to group group01 (Y/N): Y
==> Assigning user04 to the group01 group...
DRY-RUN: Would run: /usr/sbin/adduser user04 group01
Finished processing user04
```

#### Normal Run (Creates Users Automatically):
```bash
# Run with sudo for permissions
sudo ./create-users2.py < create-users.input

# When prompted "Run in DRY-RUN mode (no actual changes) (Y/N):", enter: N
# Script will automatically create all users without further prompts
```

**Output example:**
```
Run in DRY-RUN mode (no actual changes) (Y/N): N

============================================================
Processing user: user04
  Full name: First04 Last04
  Groups: group01
============================================================
==> Creating account for user04...
Adding user `user04' ...
Adding new group `user04' (1001) ...
Adding new user `user04' (1001) with group `user04' ...
Creating home directory `/home/user04' ...
Copying files from `/etc/skel' ...
==> Setting the password for user04...
New password: 
Retype new password: 
passwd: password updated successfully
==> Assigning user04 to the group01 group...
Adding user `user04' to group `group01' ...
Adding user user04 to group group01
Done.
Finished processing user04
```


### Testing Before Production
```bash
# 1. First, do a dry-run to see what will happen
./create-users2.py < create-users.input
# Answer: Y (dry-run mode)
# Review each step and answer Y/N to understand the flow

# 2. Run in production
sudo ./create-users2.py < create-users.input
# Answer: N (normal mode - creates users automatically)
```

### Batch User Creation
```bash
# Use create-users.py for fully automated batch processing
sudo ./create-users.py < create-users.input
```

### Selective User Creation
```bash
# Use create-users2.py in dry-run mode to skip specific users
./create-users2.py < create-users.input
# Answer: Y (dry-run mode)
# Answer N for users you want to skip, Y for users you want to create
```

---

### How to Verify Users
```bash
# List all users matching pattern
grep user0 /etc/passwd

# Check specific user
id user04

# Check group memberships
groups user04
grep user0 /etc/group

# Try logging in
ssh user04@localhost
```

---

## Example

```bash
# 1. Create input file
nano create-users.input

# 2. Protect input file
chmod 600 create-users.input

# 3. Make scripts executable
chmod +x create-users.py create-users2.py

# 4. Test with dry-run
./create-users2.py < create-users.input
# Answer: Y (dry-run), then Y for each step to review

# 5. Create users
sudo ./create-users2.py < create-users.input
# Answer: N (normal mode)

# 6. Verify
grep user0 /etc/passwd
id user04

# 7. Test login
ssh user04@localhost



