# Static experiment gate review

Scope: prompt-v1.md, prompt-v2.md, screen.html, components.html, ui.css only; reference translation, not a working travel app. Catalog version4, all75 active rules and original checks retained. The comparison board is a separate review tool, not a product view.

The implementation reviewer first read the original assets/source.png AFTER completing the blind implementation and tokenization. It did not influence the first generated markup. Original295×640 image-px and captured390px output were directly viewed. Original viewport/DPR/font remain unknown. Browser evidence uses headless Google Chrome via Playwright,390×772 and320×772, screen and components; native pointer and keyboard interactions, forced colors and reduced motion checked.

## Positive reference comparison

| ID | Source / prompt | Implementation and observation | Judgment |
|---|---|---|---|
| Q1 | E4 checkbox outside item | x24 checkbox and x55 card in390 output; every check is outside photo perimeter | retained |
| Q2 | E4 photo fills card height, equal short/long variants | three96px square photos and96px cards at390;320 long text grows row while photo stays96px | adapted-and-verified |
| Q3 | E3 groups distinct from same-day rows |40px preceding group gap versus18px same-group gap; no group card | retained |
| Q4 | E1/E2/E5 hierarchy |18px centered title,64×32 pills,342×56 disabled completion. Same three full rows remain visible | retained |

Initial P1 observation (before the correction recorded below): reading text is visibly larger than original; the smaller source metadata is not evidence for original CSS size.14px minimum adaptation is explicit. Native checkbox outline is darker/sharper; Lucide grip shape differs; the Day3 box perimeter seen in original is absent because prompt requests only18px photo fragment. The Day3 omission was subsequently corrected under prompt-v2, as recorded in Corrections and final verification. Other local translation differences remain for user review, not as a claim of pixel identity. Original bottom horizontal line is deliberately omitted under RUI-14. None removes a supplied full place or changes core date grouping.

## Browser results

Both pages at both widths have zero broken images and document scrollWidth equal to viewport. All measured reading nodes are>=14px; no text-node horizontal overflow. Full provided Korean and Latin strings remain in rendered flow.390 cards all96px;320 long card111px, containing every line.320 page naturally reaches787px, preserving text instead of clipping. This is expected narrow comparison adaptation, not unnecessary internal scrolling.

Pointer clicks check the first checkbox; Space unchecks it. Tab then Shift+Tab restores focus. Focus outline is2px solid#111 and persists with forced colors; native checkbox size remains22px. Back and complete have disabled attributes. Day labels are noninteractive spans with explicit selected-state accessibility labels. Drag handles are decorations. No saving/loading/error/date navigation claims are made.

## Initial confirmed corrections

- V1 / ORC-F13,G21: checkbox and disabled buttons show browser default cursor. P2; use pointer for checkbox,not-allowed for disabled.
- V2 / ORC-F14,G24: place rows use div collections. P2; use ul/li with scoped zero margins/padding and list-style none, preserving geometry.

Initial review status changes-needed. Remaining literal359px media query and negative border overlap are explicitly documented exceptions in ui.css, not missing token references. Generic catalog4px grid, header row sizing, visible icon labels and completion radius conflict with the analyst-selected reconstruction geometry in the fixed prompt. Limited rule-specific exceptions preserve the authorized reproduction scope; the user did not explicitly choose these numeric values.

## Corrections and final verification

V1 and V2 are fixed-and-verified: scoped pointer/not-allowed cursors and semantic ul/li lists now apply in both assembled and independent specimens. All measured pre-existing photo/card/row/heading/footer/button boxes are identical before and after at both widths. The initial FAIL result and sources/captures are preserved under evidence/gate-initial; failure-events.jsonl retains the initial run.

V3 / PROJECT-FRAGMENT: original Day3 visible top/right card boundary was lost in prompt-v1, so the blind implementation followed incomplete language faithfully. Prompt-v2 corrects this translation omission. The shared .fragment-card uses the existing96px minimum as a comparison choice, clipped by the existing18px slot. New390/320 captures show the top/right perimeter, no artificial bottom line and no hidden text. The source photo and all existing geometry remain unchanged. Status fixed-and-verified.

Final review aligned only for this static specimen and its stated adaptations. No functioning travel app, backend, full scrolling experience, save, date-change or drag behavior is certified. The whole-source comparison has local font/native-control/icon differences and requires the user's qualitative response before broader translation-skill conclusions. The gate CLI checks completeness/integrity of these human observations, not image aesthetics.
