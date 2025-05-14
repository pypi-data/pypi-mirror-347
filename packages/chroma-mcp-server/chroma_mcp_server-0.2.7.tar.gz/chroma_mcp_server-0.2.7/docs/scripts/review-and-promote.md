# Script: `review-and-promote.sh`

This script provides a convenient way to launch the interactive chat history review and promotion workflow.

## Purpose

Initiates the `chroma-client review-and-promote` command within the correct Hatch environment. This command fetches chat entries marked as 'analyzed', displays them to the user, allows searching the codebase for relevant code references, and prompts the user to promote, ignore, or skip each entry.

See the main [`chroma-client` documentation](chroma-client.md#review-and-promote) for full details on the underlying command and its options.

## Enhanced Features

The new version includes several significant enhancements:

1. **Rich Context Display**: Shows detailed context information for each chat entry, including:
   - Color-coded confidence scores
   - Tool sequences with pattern recognition
   - Diff summaries of code changes
   - Related code chunks from bidirectional links
   - Full code context viewing with the 'v' command

2. **Entry Sorting & Filtering**:
   - Sort by confidence score (highest first) to prioritize valuable interactions
   - Filter by modification type (refactor, bugfix, feature, etc.)
   - Set minimum confidence threshold
   - Calculate and display context richness score (visual indicator)

3. **Improved Promotion Workflow**:
   - Automatically use related code chunks from bidirectional links
   - Enhanced description with diff summary
   - Suggested tags based on modification type and file extensions
   - Default confidence values from source entry
   - Option to include/exclude rich context in promoted learnings

## Usage

```bash
# Run with default settings (7 day limit, 50 fetch limit)
./scripts/review_and_promote.sh

# Run with custom day limit
./scripts/review_and_promote.sh --days-limit 3

# Filter by modification type and minimum confidence
./scripts/review_and_promote.sh --modification-type refactor --min-confidence 0.7

# Custom collection names
./scripts/review_and_promote.sh --chat-collection-name my_chats_v2 --learnings-collection-name my_learnings_v2
```

## Command Options

- `--days-limit N`: How many days back to look for entries (default: 7)
- `--fetch-limit N`: Maximum number of entries to fetch (default: 50)
- `--chat-collection-name NAME`: Chat history collection name (default: chat_history_v1)
- `--learnings-collection-name NAME`: Derived learnings collection name (default: derived_learnings_v1)
- `--modification-type TYPE`: Filter by modification type (choices: all, refactor, bugfix, feature, documentation, optimization, test, config, style, unknown; default: all)
- `--min-confidence N`: Minimum confidence score threshold (0.0-1.0, default: 0.0)
- `--sort-by-confidence`: Sort entries by confidence score (default: true)
- `--no-sort-by-confidence`: Don't sort entries by confidence score

## Interactive Commands

During the review process, the following commands are available:

- `p`: Promote the current entry to derived learnings
- `i`: Ignore the entry (marks it as 'ignored')
- `s`: Skip the entry (leaves status unchanged)
- `v`: View full code context (when available)
- `q`: Quit the review process

## Context Richness Score

Each entry displays a context richness indicator (0-5 stars), computed from:

- Code context availability
- Diff summary presence
- Tool sequence information
- Related code chunks
- Confidence score
- Modification type

Entries with higher richness scores tend to provide better context for derived learnings.

## Hatch Alias

A convenient alias `review-promote` is typically defined in `pyproject.toml`:

```bash
# Run via hatch alias with defaults
hatch run review-promote

# Run via hatch alias with arguments
hatch run review-promote --modification-type feature --min-confidence 0.8
```

This script simplifies running the interactive promotion process from the command line.
