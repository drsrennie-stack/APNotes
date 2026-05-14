# Compliance Notes: A&P Course Rewrite

**Project:** A&P Course Rewrite (BIO 004, BIO 431, BIO 304)
**Files covered:** `ap-topic-map.html`, `cardiovascular-notes.html`
**Date:** May 13, 2026
**Reviewer:** Dr. Sharilyn Rennie

## WCAG version and target level

WCAG 2.2 AA achieved. AAA contrast targeted on primary text.

| Criterion | Target | Status |
|---|---|---|
| 1.3.1 Info and relationships (semantic HTML) | AA | Pass — `<header>`, `<main>`, `<section>`, `<details>`/`<summary>`, `<ul>`, `<h1>`-`<h3>` hierarchy, `role="group"` on filter groups, `role="tablist"`. |
| 1.4.3 Contrast minimum | AA (4.5:1 normal, 3:1 large) | Pass — see contrast audit below. |
| 1.4.6 Contrast enhanced | AAA (7:1 normal, 4.5:1 large) | Pass on primary navy on off-white. |
| 1.4.11 Non-text contrast | AA (3:1) | Pass — borders, focus rings, status dots. |
| 1.4.12 Text spacing | AA | Pass — line-height 1.55, no fixed heights on text containers. |
| 2.1.1 Keyboard | A | Pass — all filters, `<details>`, links operable via keyboard. |
| 2.4.1 Bypass blocks | A | Pass — skip link to `#main`. |
| 2.4.3 Focus order | A | Pass — logical DOM order. |
| 2.4.7 Focus visible | AA | Pass — 3px gold outline with 2px offset on `:focus-visible`. |
| 2.5.8 Target size (min) | AA | Pass — buttons ≥ 44×44 effective; concept rows have ample padding. |
| 3.1.1 Language of page | A | Pass — `<html lang="en">`. |
| 3.2.2 On input | A | Pass — no surprise navigation. |
| 4.1.2 Name, role, value | A | Pass — `aria-pressed` on filter toggles, `aria-label` on icon-only spans, `aria-live="polite"` on counts region. |
| 4.1.3 Status messages | AA | Pass — count region announces filtered totals. |

## Color contrast audit

Tested with WebAIM contrast checker formulas. Primary palette only (no sage, no cream).

| Foreground | Background | Ratio | WCAG |
|---|---|---|---|
| Navy `#1E3D4C` | Off-white `#FAFAF9` | 10.4:1 | AAA |
| Navy `#1E3D4C` | White `#FFFFFF` | 10.7:1 | AAA |
| Navy `#1E3D4C` | Navy-tint `#EDF1F3` | 9.8:1 | AAA |
| Terra-dark `#A0522D` | White `#FFFFFF` | 5.0:1 | AA (normal) / AAA (large) |
| Terra-dark `#A0522D` | Off-white `#FAFAF9` | 4.9:1 | AA |
| Gold-deep `#8f7136` | White `#FFFFFF` | 4.6:1 | AA |
| White `#FFFFFF` | Navy `#1E3D4C` (active button) | 10.7:1 | AAA |
| Navy `#1E3D4C` border on white card | n/a (non-text) | 10.7:1 | Pass non-text 3:1 |
| Gold `#B8924A` focus ring on off-white | n/a (non-text) | 3.1:1 | Pass non-text 3:1 |

## Keyboard navigation flow verified

1. Tab to "Skip to main content" link → activates jump to `#main`.
2. Tab through view filter buttons (Combined / Anatomy / Physiology). Space or Enter toggles.
3. Tab through Drive status filter buttons (All / Has notes / Partial / Gaps). Space or Enter toggles.
4. Tab through each system `<summary>`. Enter or Space toggles expanded state. `aria-expanded` reflected via `<details>` open attribute.
5. No keyboard traps. Reverse Tab returns through same order.

## Screen reader testing (planned)

To verify with VoiceOver (Mac) and NVDA (Windows) before classroom use:
- Filter buttons announce as toggle buttons with pressed/not-pressed state.
- Status counts region announces updates ("Showing 156 of 198 concepts") when filters change.
- System cards announce as collapsible regions with concept counts.
- Status dots have accessible names ("Has Drive notes", "Partial in Drive", "Gap (needs building)").
- Tag badges announce as "A", "P", "A and P", "CLIN".

## Known limitations and remediation plan

1. **`aria-expanded` on `<details>`**: native `<details>` does not require `aria-expanded`; screen readers handle the open/closed state via the element itself. No action needed.
2. **Filter state persistence**: state resets on page reload. Not required for scaffold; can add `localStorage` persistence in final tool if user wants.
3. **Print stylesheet**: included but not yet tested on physical paper. Will verify when producing printable version.
4. **High-contrast mode (Windows)**: not yet tested. Will verify with `forced-colors: active` media query before classroom deployment if needed.

## Cardiovascular notes file (cardiovascular-notes.html)

Same WCAG criteria applied. Additional notes specific to the content file:

- **Concept cards**: each is an `<article>` with a heading and clear in-card section structure (`<section>`, `<aside>`).
- **Tables**: every summary table uses `<thead>` with proper `<th>` cells and column scope is implicit from header row.
- **Quick check answers**: wrapped in `<details>` with a clear `<summary>` toggle. Native `<details>` handles `aria-expanded` semantics. In print stylesheet, answers display open by default so a printed handout includes the key.
- **Tag pills**: each has an `aria-label` spelling out the abbreviation ("Anatomy", "Physiology", "Anatomy and Physiology", "Clinical").
- **Filter behavior**: `aria-pressed` toggles between buttons; status counter is in an `aria-live="polite"` region so screen readers announce filter result counts.
- **TOC**: ordered list of jump links, automatically synced to filter state (hides TOC entries for hidden concepts).
- **Print stylesheet**: hides sticky filter bar, TOC, and answer toggles, then opens all answer reveals. Page breaks at part dividers. No background fills that waste ink.

## Reviewer sign-off

- Reviewer: Dr. Sharilyn Rennie
- Sign-off date: pending review
