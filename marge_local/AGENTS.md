# Project-Specific Agent Rules

## 1. Post-Implementation Verification (Critical)
**Rule:** After implementing any change (UI, Content, Logic), you MUST explicitly verify that the result matches the **User's Request**.

**Protocol:**
1.  **Read the Request:** Re-read the user's prompt carefully.
2.  **Check the Artifact:** Inspect the file/code you just changed.
3.  **Visual Check (if applicable):** If a UI change, imagine or check the walkthrough verification.
4.  **Self-Correction:** If you missed a detail (e.g., specific wording, color, alignment), fix it *before* notifying the user.

> "Did I actually do what was asked, or did I just do 'something similar'?"
