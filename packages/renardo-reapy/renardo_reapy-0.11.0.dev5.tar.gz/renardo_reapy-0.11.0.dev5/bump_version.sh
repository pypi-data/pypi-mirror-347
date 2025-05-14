#!/bin/bash

# Script to bump development version in pyproject.toml
# Usage: ./bump_version.sh [--dry-run] [commit_message]

set -e  # Exit on error

# Check for dry run flag
DRY_RUN=false
if [ "$1" = "--dry-run" ]; then
    DRY_RUN=true
    shift
fi

# Default commit message if not provided
COMMIT_MESSAGE=${1:-"bump dev version"}

# Get current version from pyproject.toml
CURRENT_VERSION=$(grep -E "^version = " pyproject.toml | sed -E 's/version = "(.*)"/\1/')
echo "Current version: $CURRENT_VERSION"

# Extract dev number from version
if [[ $CURRENT_VERSION =~ dev([0-9]+)$ ]]; then
    DEV_NUMBER=${BASH_REMATCH[1]}
    NEW_DEV_NUMBER=$((DEV_NUMBER + 1))
    
    # Replace with new dev number
    BASE_VERSION=${CURRENT_VERSION%dev*}
    NEW_VERSION="${BASE_VERSION}dev${NEW_DEV_NUMBER}"
    
    echo "Bumping to version: $NEW_VERSION"
    
    # Update version in pyproject.toml
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY RUN] Would update version in pyproject.toml to $NEW_VERSION"
        echo "[DRY RUN] Would run: git add pyproject.toml"
        echo "[DRY RUN] Would run: git commit -m \"$COMMIT_MESSAGE\""
        echo "[DRY RUN] Would run: git push"
        echo "[DRY RUN] Would run: git tag \"v$NEW_VERSION\" -m \"bump dev version\""
        echo "[DRY RUN] Would run: git push origin --tags"
        echo "[DRY RUN] Version bump simulation complete"
    else
        sed -i.bak -E "s/^version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml
        rm pyproject.toml.bak  # Remove backup file
        
        # Git operations
        git add pyproject.toml
        git commit -m "$COMMIT_MESSAGE"
        git push
        
        # Create and push tag
        git tag "v$NEW_VERSION" -m "bump dev version"
        git push origin --tags
        
        echo "Successfully bumped version to $NEW_VERSION and pushed changes"
    fi
else
    echo "Error: Version '$CURRENT_VERSION' doesn't match expected format with 'dev' suffix"
    exit 1
fi