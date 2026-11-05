# Brief for Claude Code: UAE images across the site, and more useful content

Repository: `pcc40/eastbridge-website`, branch `main` (Netlify deploys every push). Read `HANDOFF.md`, `AUTOMATION.md`, `src/content/WRITING_BRIEF.md` and `src/i18n/TRANSLATION_BRIEF.md` first. Prepared 5 November 2026.

## Why

1. **Every Dubai and Abu Dhabi page is illustrated with UK houses.** The 12 area pages, the Island E worked example and most articles use P Chapman Construction photographs from Cornwall (`AREA_IMG`, `POST_IMG`, `HERO_SLIDES` in `src/pages.py`). An owner looking at "Palm Jumeirah" sees a Cornish house. That undermines trust and wastes the strongest image-search signal we have.
2. **We need more useful content, faster, without tripping Google's scaled-content rules.** The site is indexed (Google shows about 458 of ~470 pages after six days), and the first UAE impressions arrived on 3 November. Now the site needs depth and frequency.

## Owner's decision on images (record in HANDOFF.md)

Phil, as a Dubai broker with developer marketing access, has approved using the **master developers' own marketing images and renders** (Nakheel, Emaar, Meraas, Aldar, Modon, Meydan Sobha, Al Barari) on the area pages, the Island E worked example and related articles, and takes responsibility for that use. Rules:
- Every developer image carries a visible credit, using the existing banner credit slot: "Image: Nakheel", or for renders "Developer render: Nakheel (Bay Estates)".
- Never caption or place a developer image so that it suggests Eastbridge designed, built or managed what it shows. On area pages the caption reads as an illustration of the community.
- UK photographs stay, labelled as now, but only where the subject is P Chapman Construction's work or Philip's record: `/work/`, `/about/`, `/approach/`, the Owers House case study and a "Built by our founder in the UK" strip on the home page.
- No people's faces, no other agents' listing photos, no watermarks.

## 1. The image library (already in the repo)

Original files are in `assets-src/uae-images/<slug>/` (outside the published folder) on branch `uae-images` with a `manifest.json` per folder. Each entry gives `file`, `role` (hero/support), `shows`, `credit`, `source_page`, `image_url`, `w`, `h` and `is_render`. The inventory table is at the end of this brief.

Build steps:
- Add a small tool, `tools/make_uae_images.py`, that turns each original into the site's standard sizes (`<base>-640.webp`, `-1280.webp`, `-1600.webp`, never upscaled) in `src/static/assets/img/`. It should also add the entries to `src/img_manifest.json` under a new project key per folder (`uae-palm-jumeirah`, `uae-island-e`, …), with `name`, `place` and `photo`/credit set so that `credit_of()` prints the developer credit.
  - Bases: `uae-<slug>-01` etc.
  - The originals stay in `assets-src/`, which is never published; only the generated webp sizes go into `src/static/assets/img/`.
- Alt text: write each image's `alt` from its `shows` line (specific, under 125 characters, community name included). Alt text and credits go through the translation pipeline.

## 2. Where the images go

| Page | Change |
|---|---|
| 12 area pages (`/areas/<slug>/`) | Hero = that area's `-01`. The image strip under the body (`others`) uses that area's support images instead of UK photos. Set `og:image` to the hero (1200-wide crop). |
| Island E worked example (`/case-studies/island-e-waterfront-villa/`) | Hero = `uae-island-e-01` (Nakheel's waterfront-plot reference design). Add a 3-image strip from `-02`…`-05` under the introduction, captioned "Developer renders, Bay Estates by Nakheel, Island E. For illustration; Eastbridge was not involved in their design." Keep the existing "hypothetical worked example" label and the generated diagram OG image. |
| `/areas/` hub | Each community listed gets a small thumbnail of its hero. |
| Articles tied to a place | `POST_IMG` hero from the matching area: Palm renovation and Nakheel NOC → Palm Jumeirah; Dubai Islands items → Dubai Islands or Island E; Abu Dhabi permit (TAMM) → Saadiyat or Hudayriyat; Jumeirah Islands and renovation-mistakes → Jumeirah Islands; Emirates Hills cost → Emirates Hills. General Dubai articles → the `general/` Dubai image if present, else Dubai Hills or Palm aerial. |
| Articles about the builder's view (`what-the-contractor-knows`, contracts, choosing a contractor) | May keep a UK image, captioned as now ("Built by P Chapman Construction, Cornwall"). |
| Home page | Hero slideshow: lead with 2–3 UAE images (Palm, Dubai Islands, Emirates Hills); keep 2 UK houses later in the rotation with their existing UK captions. Add a "Built by our founder in the UK" strip linking to `/work/`. |
| Service pages | Mix: renovation and Nakheel-related services get UAE images; leave the rest unless an obvious match exists. |

**Image SEO:**
- Add image entries (`<image:image>`) to `sitemap.xml` for the area and article heroes.
- Add `image` (URL) to the Article and Service JSON-LD where a hero exists.
- Keep descriptive file names.

**Performance:** the home hero must stay under about 200 KB at 1280 px (currently fine). Preload only the first hero; lazy-load the rest. Re-check Netlify's Core Web Vitals after deploy (First Contentful Paint was "needs improvement").

## 3. More useful content (change `AUTOMATION.md`)

Keep quality first. The aim is more depth per week, not thin pages.

1. **Three articles a week instead of two:** Tuesday, Thursday and Saturday (Dubai). Each still 1,400–2,200 words, sourced, with a builder's-side insight, per `WRITING_BRIEF.md`. Update Principle 1 and the publishing-days section.
2. **Plus one "deepen" job every Monday:** take one existing page and make it the best answer on the web. Start with the area pages, which are about 1,000 words against Tanmu's 1,750–1,990 (see the competitor brief, item 4.1):
   - "what makes this community different"
   - approval route and master developer
   - new build versus renovation
   - typical villa stock and issues
   - 4–6 sourced FAQs
   - an image strip from the new library
   - a link to the calculator
   
   Order: Palm Jumeirah, Emirates Hills, Jumeirah Islands, Dubai Islands, Dubai Hills, Arabian Ranches, then the rest. Update `updated:` dates; never `date:`.
3. **Every new article uses at least one UAE image** from the library that matches its subject, plus at least one table or a simple diagram.
4. **Next topics, ahead of the TOPICS.md order** (search demand shown in the competitor review):
   - `how-to-choose-client-side-project-manager`: DNA published its version on 2 November.
   - `older-villa-mep-renovation`: Friday's topic.
   - `villa-renovation-timeline-dubai`
   - `how-to-plan-a-villa-renovation-dubai`: a hub linking all renovation content.
   - `emaar-community-villa-renovation`
   - `jumeirah-islands-villa-renovation`
   - `defects-liability-period-uae`
   - `snagging-developer-villa-handover`
   - `dubai-islands-plot-guide`: link Island E.
   - `building-on-a-plot-from-abroad`: overseas-owner angle; Tanmu's copy site ranks #1 for "building a villa in dubai from uk".
5. **New area pages,** one a fortnight, same template and depth, each with library images (developer images to be sourced at the time with the same rules): Tilal Al Ghaf, Jumeirah Golf Estates, DAMAC Hills, The Meadows and Springs, Al Furjan, Jumeirah Park.
6. **Translation:** all new and changed text, including alt text and credits, goes through the Languages steps. Add one sentence to the translation brief: "Developer and place names in credits stay in Latin script."

## 4. Checks before pushing

- `python3 build.py && python3 tools/i18n.py apply`
- `python3 tools/seo_audit.py`: 0 errors, 0 warnings. Extend it to fail if an area page or the Island E page uses a non-UAE image.
- `python3.11 -m py_compile build.py tools/*.py src/*.py`
- `sh tools/make_rtl.sh` if `site.css` changed. Check `/ar/` on mobile.
- Look at the home page, three area pages and Island E at mobile and desktop widths before pushing.
- Confirm the Netlify deploy, then run `python3 tools/indexnow.py` with every changed URL in all five languages.
- Record the image decision and the new cadence in `HANDOFF.md`.

## 5. Image inventory

57 images, every area page covered. Full details (what each shows, credit, source URL) are in each folder's `manifest.json`.

| Folder | Images | Hero | Credit | Notes |
|---|---|---|---|---|
| `al-barari` | 5 | `al-barari-01.jpg` (2400×1599) | Image: Al Barari |  |
| `arabian-ranches` | 3 | `arabian-ranches-01.jpg` (2400×1600) | Image: Emaar | `-02` is a panorama: banner or support only. |
| `district-one` | 3 | `district-one-01.jpg` (1920×1080) | Image: Crystal Lagoons (District One, MBR City) | `-01` and `-03` are from Crystal Lagoons, who built the District One lagoon. `-02` is the Nakheel/Meydan District One West render (interior). |
| `dubai-hills-estate` | 5 | `dubai-hills-estate-01.jpg` (2400×1600) | Image: Emaar |  |
| `dubai-islands` | 4 | `dubai-islands-01.jpg` (1920×1080) | Image: Nakheel | Renders of the whole island group (Island E included). |
| `emirates-hills` | 2 | `emirates-hills-01.jpg` (1920×1080) | Image: Emaar | Clubhouse is the Montgomerie, inside Emirates Hills (confirmed on Emaar's Emirates Living page). `-02` is a Wikimedia Commons photo under CC BY 3.0: the credit must name the author and licence exactly as in the manifest. |
| `general` | 2 | `dubai-skyline-villas-01.jpg` (1920×1080) | Image: Nakheel (Palm Jumeirah) | Dubai and Abu Dhabi skylines for general articles. |
| `hudayriyat` | 5 | `hudayriyat-01.png` (1404×747) | Image: Modon (Hudayriyat Island) | Hero is 1,404 px wide; if soft at 1,600, use `-02`. |
| `island-e` | 5 | `island-e-01.webp` (1920×1080) | Image: Nakheel (Bay Estates, Island E) | Nakheel Bay Estates renders. |
| `jumeirah-bay` | 5 | `jumeirah-bay-01.jpg` (1920×1080) | Image: Meraas (Jumeirah Bay) | `-02`, `-04`, `-05` are 880 px wide: use them only in the image strip (640 size), never as a hero. |
| `jumeirah-islands` | 4 | `jumeirah-islands-01.jpg` (1920×1080) | Image: Nakheel |  |
| `palm-jebel-ali` | 5 | `palm-jebel-ali-01.jpg` (1920×1080) | Image: Nakheel | All renders. |
| `palm-jumeirah` | 4 | `palm-jumeirah-01.jpg` (1920×1080) | Image: Nakheel |  |
| `saadiyat` | 5 | `saadiyat-01.webp` (1920×1079) | Image: Aldar (Saadiyat Lagoons) | `-05` is a destination shot: support only. |

Credits other than a developer's (Crystal Lagoons, Wikimedia Commons) print exactly as given in the manifest. Never use estate agents' listing photos or stock images to fill gaps.
