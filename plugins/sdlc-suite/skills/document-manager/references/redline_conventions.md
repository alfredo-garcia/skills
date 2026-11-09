# Redline Conventions

Detail behind SKILL.md Step 5. This is the validation gate — nothing gets written to the actual master doc files until the user has seen exactly what's changing and said so explicitly. Keeping this format consistent every time is what lets the user learn to scan it quickly instead of re-reading a wall of prose each time.

## Always lead with a summary

Before the detailed redline, give a short scannable summary — domain by domain, counts only:

```
Checkout domain: 2 screens added, 1 flow modified, 0 removed
Account domain: 1 component modified, 0 added, 0 removed

⚠ Conflict flagged: PRD says guest checkout is disabled for orders over $500;
  existing docs (Checkout domain) say no order-size limit exists today. Not
  listed as an approved deviation in the UX Flow doc — confirm before I write this in.
```

If there are no conflicts, don't include the line — don't manufacture a "no conflicts found" line either; just move straight to the detailed redline.

## Detailed redline — three tags, three formats

### `[NEW]` — brand new content

No "before" to diff against, so show the full new block as-is, clearly labeled:

```
[NEW] SCR-checkout-guest — Guest Checkout Review

- Platform: Both
- Purpose: lets a user complete a purchase without creating an account.
- Entry points: FLW-checkout-guest, step 2
- Functional composition: CMP-cart-summary (shared), CMP-guest-contact-form
- Data & business rules: requires email + shipping address; no account created;
  order is linked to email for post-purchase lookup only.
- States: Empty cart → redirect to FLW-checkout-guest is not entered. Validation
  error → inline field errors, does not advance.
- Source: 014_guest-checkout_prd.md, 014_guest-checkout_ux_flow.md
```

### `[MODIFIED]` — existing content changing

For substantial changes, show a real diff block so old and new are both visible at a glance:

```
[MODIFIED] SCR-checkout-review

  - Data & business rules: requires a logged-in account; guest orders are
-   not supported.
+   requires either a logged-in account or a completed guest checkout
+   (see SCR-checkout-guest); guest orders are supported for orders under $500.
```

For a small, single-line change, a full diff block is overkill — an inline before → after is enough:

```
[MODIFIED] CMP-cart-summary — "Used on" list:
  was: SCR-checkout-review
  now: SCR-checkout-review, SCR-checkout-guest
```

Use judgment on which format fits — the point is that the reviewer can see both states, not which exact formatting you pick.

### `[REMOVED]` — content being deleted

Quote the removed content briefly (don't reproduce a long passage verbatim if a short paraphrase says the same thing) and always state why:

```
[REMOVED] FLW-checkout-express — "One-click express checkout for returning
  customers." Removed per 014_guest-checkout_prd.md §4 (Non-Goals): feature was
  never fully shipped and is being formally retired, not replaced.
```

If nothing is being removed in a given update, don't include an empty `[REMOVED]` section — just omit it.

## Getting approval

Ask for explicit confirmation after the redline, and accept partial responses — "approve everything except the CMP-cart-summary change, make that say under $250 not under $500" is a complete, actionable reply; you don't need a single up-or-down vote on the whole thing. But treat anything you flagged (especially a conflict) that the user's reply doesn't address as still open — don't assume silence on a specific flagged item means it's approved, even if they approved everything else.

## After approval

Every `[NEW]` / `[MODIFIED]` / `[REMOVED]` tag, and any diff markup (`+`/`-` lines), is a review-time device only. None of it survives into the saved file — the final domain file reads as plain, confident, current-state prose, exactly as if it had always said that. If you find yourself unsure whether some redline artifact made it into the saved version, re-read the file before presenting it as done.
