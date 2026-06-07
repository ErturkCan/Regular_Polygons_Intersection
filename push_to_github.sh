#!/usr/bin/env bash
#
# push_to_github.sh
# -----------------
# One-shot helper that turns this folder into a git repository and pushes it
# to a NEW GitHub repository. Run it once. It does everything except creating
# the empty repo on GitHub.com and typing your GitHub login when asked.
#
# HOW TO RUN
#   1. Open Terminal.
#   2. Drag this folder's "push_to_github.sh" onto the Terminal window and
#      press Enter   (or:  bash /path/to/push_to_github.sh )
#
# It will ask for your GitHub username and the repo name, then walk you
# through the rest.

set -e

# Always work from the folder this script lives in.
cd "$(dirname "$0")"

echo "============================================================"
echo "  Publishing this project to GitHub"
echo "============================================================"
echo

# --- check git is installed ---
if ! command -v git >/dev/null 2>&1; then
  echo "git is not installed."
  echo "Install it first:"
  echo "  - Mac:     run   xcode-select --install"
  echo "  - Windows: install Git from https://git-scm.com/download/win"
  echo "Then run this script again."
  exit 1
fi

# --- identity (only set if missing) ---
if [ -z "$(git config --global user.name)" ]; then
  git config --global user.name "Can Ertürk"
fi
if [ -z "$(git config --global user.email)" ]; then
  git config --global user.email "canerturk333@gmail.com"
fi

# --- ask for the details ---
read -r -p "Your GitHub username: " GH_USER
read -r -p "Repository name [regular-polygon-intersections]: " GH_REPO
GH_REPO=${GH_REPO:-regular-polygon-intersections}

echo
echo "------------------------------------------------------------"
echo "  STEP 1 — create the empty repo on GitHub now"
echo "------------------------------------------------------------"
echo "  1. Go to:  https://github.com/new"
echo "  2. Repository name:  $GH_REPO"
echo "  3. Choose Public."
echo "  4. Do NOT tick 'Add a README', '.gitignore', or 'license'."
echo "  5. Click 'Create repository'."
echo
read -r -p "Press Enter once you have created the empty repository... " _

# --- init / commit (safe to re-run) ---
if [ ! -d .git ]; then
  git init -q
fi
git add .
git commit -q -m "Regular polygon intersection points: paper and verification code" || true
git branch -M main

# --- connect and push ---
REMOTE="https://github.com/$GH_USER/$GH_REPO.git"
git remote remove origin 2>/dev/null || true
git remote add origin "$REMOTE"

echo
echo "------------------------------------------------------------"
echo "  STEP 2 — pushing to $REMOTE"
echo "------------------------------------------------------------"
echo "  If a browser window opens, log in to GitHub to authorise."
echo "  If you are asked for a password in the Terminal, paste a"
echo "  Personal Access Token (not your account password)."
echo "  Make one at: https://github.com/settings/tokens"
echo "  (Tokens -> Generate new token -> tick 'repo')."
echo

git push -u origin main

echo
echo "============================================================"
echo "  Done. Your project is live at:"
echo "  https://github.com/$GH_USER/$GH_REPO"
echo "============================================================"
