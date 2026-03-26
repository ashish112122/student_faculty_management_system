# Git Commit Checklist

## Before You Commit - IMPORTANT!

### ✅ Step 1: Check for Credentials

Run these commands to search for credentials:

```bash
# Search for passwords
git diff | grep -i "password"

# Search for Oracle credentials
git diff | grep -i "oracle"

# Search for email passwords
git diff | grep -i "smtp"
```

If you see any actual passwords (not placeholders), DO NOT COMMIT!

### ✅ Step 2: Verify .gitignore is Working

```bash
# Check what will be committed
git status

# These files should NOT appear:
# - backend/config.py
# - backend/.env
# - backend/setup_simple.py
# - *.bat files with credentials
```

### ✅ Step 3: Safe Files to Commit

These are safe:
- ✅ `frontend/` folder (all HTML, CSS, JS)
- ✅ `backend/app.py` (now uses config.py)
- ✅ `backend/requirements.txt`
- ✅ `backend/database/schema.sql`
- ✅ `backend/database/demo_data.sql`
- ✅ `backend/config.template.py`
- ✅ `backend/.env.example`
- ✅ `backend/setup_simple.template.py`
- ✅ `README.md`
- ✅ `.gitignore`

### ✅ Step 4: Files to NEVER Commit

These contain credentials:
- ❌ `backend/config.py`
- ❌ `backend/.env`
- ❌ `backend/setup_simple.py`
- ❌ `backend/test_connection.py`
- ❌ `*.bat` files
- ❌ `*.whl` files

### ✅ Step 5: Commit Commands

```bash
# Add safe files
git add frontend/
git add backend/app.py
git add backend/requirements.txt
git add backend/database/
git add backend/config.template.py
git add backend/.env.example
git add backend/setup_simple.template.py
git add README.md
git add .gitignore
git add FIXES_APPLIED.md
git add SETUP_FOR_GIT.md
git add GIT_COMMIT_CHECKLIST.md

# Check what's staged
git status

# Commit
git commit -m "Add student portal with login, marks, attendance, and feedback"

# Push to your branch
git push origin VANSHIKA
```

## If You Accidentally Committed Credentials

### Remove from last commit (not pushed yet):
```bash
git reset HEAD~1
# Fix the files
git add <safe-files-only>
git commit -m "Your message"
```

### Remove from Git history (already pushed):
```bash
# Remove file from Git but keep locally
git rm --cached backend/config.py
git commit -m "Remove config.py from Git"
git push origin VANSHIKA
```

## Team Member Setup

When your teammates clone the repo, they need to:

1. Copy template files:
```bash
cp backend/config.template.py backend/config.py
cp backend/.env.example backend/.env
cp backend/setup_simple.template.py backend/setup_simple.py
```

2. Update with their own credentials in:
   - `backend/config.py`
   - `backend/setup_simple.py`

3. These files will be ignored by Git (in .gitignore)

## Quick Check Before Push

```bash
# See what you're about to push
git diff origin/VANSHIKA

# Make sure no passwords are visible
git diff origin/VANSHIKA | grep -i "password"
git diff origin/VANSHIKA | grep -i "Vanshi"
```

If you see your actual password, STOP and fix it!

## Summary

✅ Template files are safe to commit
❌ Actual config files with credentials should NEVER be committed
✅ .gitignore is configured to protect you
✅ Always double-check before pushing
