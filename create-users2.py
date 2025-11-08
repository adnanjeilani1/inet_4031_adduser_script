#!/usr/bin/python3

# Script: create-users2.py
# Purpose: read passwd-style lines from file and create accounts (or simulate via dry-run)
# Author: Adnan Jeilani (updated)
# Date: November 2025

# Imports:
# - os: to run system commands when not in dry-run mode
# - re: to detect commented lines
# - sys: to read command-line arguments
import os
import re
import sys

def run_cmd(cmd, dry_run):
    """Run the command if not dry_run; otherwise print what would run."""
    if dry_run:
        print("DRY-RUN: Would run: %s" % cmd)
    else:
        os.system(cmd)

def prompt_yes_no(question):
    """Prompt user with a yes/no question. Returns True for yes, False for no.
    Reads from /dev/tty so it works even when stdin is redirected."""
    tty = open('/dev/tty', 'r')
    while True:
        print("%s (Y/N): " % question, end='', flush=True)
        resp = tty.readline().strip().lower()
        if resp == 'y':
            return True
        if resp == 'n':
            return False
        print("Please enter Y or N.")

def main():
    # Read all lines from stdin
    lines = sys.stdin.readlines()
    
    # Ask user if they want dry-run mode
    dry_run = prompt_yes_no("Run in DRY-RUN mode (no actual changes)")
    
    # Process each line
    for lineno, line in enumerate(lines, start=1):
        # Detect lines that start with '#' (commented/skipped lines)
        if re.match(r"^#", line):
            print("Skipping commented line %d: %s" % (lineno, line.rstrip()))
            continue

        # Split the line into expected fields separated by ':' as in passwd-like file
        fields = line.strip().split(':')

        # If the line does not have exactly 5 fields, skip it
        if len(fields) != 5:
            print("ERROR: Line %d does not have 5 fields, skipping: %s" % (lineno, line.rstrip()))
            continue

        # Map fields to account values
        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])
        groups = fields[4].split(',')

        # Show user details
        print("\n" + "="*60)
        print("Processing user: %s" % username)
        print("  Full name: %s %s" % (fields[3], fields[2]))
        print("  Groups: %s" % fields[4])
        print("="*60)
        
        # In dry-run mode, prompt for each step; otherwise create automatically
        if dry_run:
            if not prompt_yes_no("Create account for %s" % username):
                print("Skipping user %s" % username)
                continue

        # Create the user account
        print("==> Creating account for %s..." % username)
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)
        run_cmd(cmd, dry_run)

        # Set password (prompt only in dry-run mode)
        if dry_run:
            if not prompt_yes_no("Set password for %s" % username):
                print("Skipping password for %s" % username)
            else:
                print("==> Setting the password for %s..." % username)
                cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)
                run_cmd(cmd, dry_run)
        else:
            print("==> Setting the password for %s..." % username)
            cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)
            run_cmd(cmd, dry_run)

        # Assign the user to groups
        for group in groups:
            if group != '-':
                if dry_run:
                    if not prompt_yes_no("Assign %s to group %s" % (username, group)):
                        continue
                print("==> Assigning %s to the %s group..." % (username, group))
                cmd = "/usr/sbin/adduser %s %s" % (username, group)
                run_cmd(cmd, dry_run)
        
        print("Finished processing %s\n" % username)

if __name__ == '__main__':
    main()
