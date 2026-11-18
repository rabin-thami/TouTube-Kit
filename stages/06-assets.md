# Stage 6 — Assets

Input: `script.md` (scenes and `> VISUAL:` notes), approved.
Output: `<run>/assets.md` (format: AGENTS.md → File contracts → assets.md)
and the downloaded files in `<run>/assets/`.

## Do

1. For each scene, find at least one visual: an image, map, footage, or
   document scan.
2. Search only these sources:
   - Wikimedia Commons (commons.wikimedia.org)
   - Library of Congress (loc.gov), items whose rights statement says public
     domain (write the license cell as `Public domain`; "no known
     restrictions" alone is not enough)
   - national archives (e.g. archives.gov, nationalarchives.gov.uk)
   - museum open-access collections (e.g. Met Open Access, Rijksmuseum,
     Smithsonian Open Access, Cleveland Museum of Art)
3. Read the license on the item's own page. Allowed: `Public domain`, `CC0`,
   `CC BY <ver>`, `CC BY-SA <ver>`. Reject NC, ND, "editorial use", unclear,
   or missing licenses. Copy author and title exactly as the page states them.
   - Wikimedia Commons tip: the API returns license and author data:
     `https://commons.wikimedia.org/w/api.php?action=query&titles=File:<name>&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=1920&format=json`
     Use `thumburl` (1920 px wide) as the file url for large images.
4. Attribution text (one line, pasteable):
   `"<Title>" by <Author>, <License>, via <Source>` and add the license URL for
   CC BY / CC BY-SA. For public domain: `"<Title>" by <Author>, public domain, via <Source>`.
5. `file`: `s<scene 2 digits>-<short-slug>.<ext>`, e.g. `s03-mainz-map.jpg`.
6. Write assets.md, then download and check:

```
python3 kit.py fetch-assets <run>
python3 kit.py check-assets <run>
```

If a download fails, find another file url (or another asset) and retry.

## Done when

`check-assets` prints `ASSETS OK` and exits 0.
