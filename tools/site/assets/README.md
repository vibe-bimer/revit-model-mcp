# Social card template

`social-card.html` composes the Open Graph card that every page advertises as
`assets/social-card.png`. It is a build input, not a site page: it lives outside `docs/`, so it
never reaches the published tree.

## Regenerate the card

1. Open `social-card.html` in a browser with a 1200 × 630 viewport.
2. Capture the viewport as a PNG.
3. Replace `docs/assets/social-card.png` with the capture.

The published PNG is referenced by `docs/overrides/main.html` as the `og:image` and
`twitter:image` of every page, so keep its file name and its 1200 × 630 size.
