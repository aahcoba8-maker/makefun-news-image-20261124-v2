# The World in One Day — News Image, 24 November 2026 (v2)

[![Competition](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![Rank](https://make.fun/badge/news-image-20261124/aahcoba8-maker/makefun-news-image-20261124-v2/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![Reward](https://make.fun/badge/news-image-20261124/aahcoba8-maker/makefun-news-image-20261124-v2/reward.svg)](https://make.fun/bounty/news-image-20261124)

Entry for the make.fun bounty
[Sum up 24 November's world news in one image](https://make.fun/bounty/news-image-20261124).

`main.py` is a self-contained Python program that draws a newspaper-style
poster — "THE WORLD IN ONE DAY", dated Tuesday 24 November 2026 — and writes
it to `$MAKEFUN_OUTPUT_DIR/entry.png` (falling back to the script directory).
It runs offline, is fully deterministic, and needs no input. It renders with
PIL when available; otherwise it copies `poster.png`, the same poster
rendered ahead of time, so the output is identical either way.

## What changed from v1

v1 was a thin front page: 6 stories, no drawn scenes, no region breakdown,
and it scored 40.6% in round 2 — far from the paid line (top 50). The
round-2 winners all run 30–35 dated stories with drawn scenes and lead with
concrete named stories. v2 follows that pattern:

- **32 dated stories** (all 24 Nov 2026) across **9 regions**, counted in
  code and printed on the poster: Europe 11, N. America 6, East Asia 5,
  Middle East 3, Oceania 3, Latin America 1, SE Asia 1, Africa 1,
  South Asia 1.
- **3 drawn hero scenes**: the Houthi drone strike on Riyadh's PIF Tower,
  the TAIEX +9% surge past 40,000, and the Shanghai party-chief probe
  under a red "UNDER INVESTIGATION" stamp.
- **Leads named up front** in the masthead line and date bar: Shanghai
  purge, Riyadh tower struck, TAIEX +9%.
- Every figure on the poster was checked against reporting of 24 Nov 2026
  (Reuters, Al Jazeera, BBC, Xinhua, Newsquawk, UKHSA, pm.gov.au).

## The day's headlines on the poster

- **Middle East (lead):** Houthi drone hits Riyadh's PIF Tower, 11 hurt —
  the second strike on the tower in five days.
- **Markets (lead):** TAIEX soars 9% past 40,000 as TSMC leads Asia's chip
  rebound; Nvidia +31% as Huang returns, Nasdaq +6.9%, S&P +4.7%.
- **China (lead):** Shanghai party chief Chen Jining under investigation —
  the 4th Politburo member probed since October 2025.
- **Europe:** Russian dawn strike on Zaporizhzhia kills 2, wounds 40+;
  a Russian drone spends 8 minutes in Polish airspace; NATO sends an
  AWACS to Poland; Sanofi to buy Insmed for $41bn; UK heat deaths hit
  a record 5,258.
- **Justice:** Huawei guilty on 10 of 12 counts in Brooklyn, acquitted of
  racketeering.
- **Plus 24 more stories** in the numbered index, from the Houthis 60 km
  from Aden to Australia's online-safety deal.

## Sources (reporting of 24 November 2026)

- Reuters, Al Jazeera, BBC, Xinhua, Newsquawk, UKHSA, pm.gov.au
