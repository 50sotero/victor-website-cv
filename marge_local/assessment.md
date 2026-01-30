# Assessment: Align Featured Projects Components

## Findings
-   Project cards were responsive but lacked internal vertical alignment due to varying content lengths (Impact text and Tech tags).
-   To achieve perfect symmetry as requested, fixed heights on the variable components (Impact and Tech) are necessary.
-   Titles were already substantially aligned due to `min-height`.

## Solution
-   Applied `height: 8rem` to `.project-impact`.
-   Applied `height: 9rem` to `.project-tech`.
-   Verified that these heights accommodate the maximum current content (4 lines of impact, 3 rows of tags).
-   Used `display: flex` and `align-items/content: flex-start` to ensure content starts at the top of these fixed boxes.
