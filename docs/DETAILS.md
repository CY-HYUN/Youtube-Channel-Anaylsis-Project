# Methodology Details

Per-analysis methodology for the YouTube Channel Analysis Project. Everything here is
grounded in the code (`analysis/`) and the original-data notebook run
(`notebooks/Youtube_Channel_Anaylsis_Project.ipynb`, outputs preserved in the file).

## Dataset

- **Scope:** 15 Korean YouTube channels — the 5 top channels in each of three categories:
  Fashion (패션), Mukbang (먹방), Travel (여행).
- **Collection:** YouTube Data API v3; up to 200 recent videos per channel. Three CSVs
  (one per category) with per-video metadata (title, views, likes, comments, duration,
  upload datetime) and per-channel metadata (subscribers, creation date, total views,
  video count). The CSVs are private and gitignored.
- **Size after preprocessing:** 2,125 videos remained in the upload-frequency analysis
  (per-channel counts below) after keeping upload gaps of 1–30 days and removing view
  outliers (1.5×IQR, per channel). Shorts were not removed in this analysis: the shared
  Shorts filter looks for a column name the data does not have and only prints a warning.

## Preprocessing Pipeline (`analysis/data_preprocessing.py`)

1. Comma-formatted numeric strings (`"1,234,567"`) coerced to integers for views, likes,
   comments, and video counts.
2. Upload dates parsed to datetime; day-of-week and hour-of-day columns derived.
3. Rows with unparseable upload dates dropped.
4. Shorts removed: videos with duration ≤ 60 seconds. In the notebook, Shorts are removed
   only in the duration analysis (> 60 s) and the expected-views analysis (≥ 70 s); the
   shared notebook filter did not fire, so the other analyses include Shorts.
5. Remaining numeric missing values filled with 0.
6. When no CSVs are present, `generate_sample_data()` produces a seeded synthetic dataset
   (6 categories × 5 channels × 100 videos = 3,000 rows, seed 42) so every script stays
   runnable as a demo. Synthetic-run outputs are **not** the project's findings.

## Analysis 1 — Word Cloud (`01_wordcloud_analysis.py`)

Extracts Hangul tokens from video titles (`clean_korean_text()`: regex keeps Korean
characters only, collapses whitespace), counts frequencies per category, and renders word
clouds for the top channels in each category. Observation from the real-data run:
category-specific vocabulary dominates — brand names in Fashion, dish names in Mukbang,
destination names in Travel — rather than generic terms like "vlog" or "review".

## Analysis 2 — Upload Timing (`02_upload_timing_analysis.py`)

Groups views by upload day-of-week and hour-of-day, per channel and per category:
bar charts for both dimensions, per-channel best-day comparison, and a 7×24
day×hour pivot heatmap of average views. The real-data figure
(`visualizations/02_timing_analysis/upload_timing.png`) shows per-channel timing profiles
that differ substantially between channels even within one category.

## Analysis 3 — Upload Frequency (`03_upload_frequency_analysis.py`)

Computes days-between-uploads per channel, buckets them into intervals (1, 2–3, 4–5, 6–7,
8–14, 15+ days), and compares average views and likes per bucket. Views are filtered with
a 1.5×IQR outlier rule per channel before averaging, so single viral videos do not
dominate the cadence comparison.

Per-channel results from the original-data run (notebook cell outputs):

| Category | Channel | Best interval (views) | Best interval (likes) | Videos analyzed |
| --- | --- | --- | --- | --- |
| Fashion | 한별Hanbyul | 1 day | 6–7 days | 161 |
| Fashion | 깡스타일리스트 | 1 day | 1 day | 87 |
| Fashion | 옆집언니 최실장 stylist unnie | 6–7 days | 6–7 days | 144 |
| Fashion | 스타일가이드 최겨울 | 2–3 days | 1 day | 79 |
| Fashion | 짱구대디 | 2–3 days | 2–3 days | 90 |
| Mukbang | 설기양SULGI | 6–7 days | 2–3 days | 153 |
| Mukbang | GONGSAM TABLE 이공삼 | 8–14 days | 4–5 days | 160 |
| Mukbang | 문복희 Eat with Boki | 4–5 days | 4–5 days | 183 |
| Mukbang | 쏘영 Ssoyoung | 2–3 days | 2–3 days | 113 |
| Mukbang | 떵개떵 | 8–14 days | 8–14 days | 127 |
| Travel | 곽튜브 | 8–14 days | 8–14 days | 176 |
| Travel | 빠니보틀 Pani Bottle | 4–5 days | 4–5 days | 151 |
| Travel | 진정부부 | 8–14 days | 4–5 days | 173 |
| Travel | Rirang OnAir | 6–7 days | 6–7 days | 152 |
| Travel | 원지의하루 | 1 day | 1 day | 176 |

Totals: 2,125 videos. Daily uploads were view-optimal for 3 of 15 channels; 10 of 15
channels had the same optimal interval for views and likes.

## Analysis 4 — Correlation (`04_correlation_analysis.py`)

Scatterplots of likes-vs-views and comments-vs-views for each channel plus a category
aggregate (18 panels total in the real-data figure). The script version also computes
Pearson coefficients per category when run on a dataset. In the real-data figures, the
likes-views relationship is visibly near-linear for every channel, while comments stay
flat and dispersed — the basis for the "likes are the more reliable engagement signal"
finding. The original notebook run reported this visually and did not print numeric
coefficients, so no real-data r values are claimed.

## Analysis 5 — Video Duration (`05_video_duration_analysis.py`)

Compares the duration of each channel's top-10 and bottom-10 videos by views
(the script adds 99th-percentile trims; the notebook run did not use them), annotating both groups' average durations per channel,
alongside per-channel views and duration distributions. Motivating question from the
notebook: do longer videos fatigue viewers and earn fewer views? The answer in this
sample is channel-dependent — the direction even flips between channels: for 한별Hanbyul
the top-10 average 19.53 min vs bottom-10 9.83 min (winners are longer), while for
옆집언니 최실장 the top-10 average 17.68 min vs bottom-10 27.88 min (winners are shorter).
Duration alone does not separate winners from losers.

## Analysis 6 — Channel Age (`06_channel_age_analysis.py`)

Compares channel creation dates against total subscribers and total views (the script
adds 99th-percentile trimming on the views/subscriber ratio; the notebook run did not).
With 15 channels and no statistical test, this is an observation, not a tested result. Conclusion from the
original run, stated in the notebook: channel age does not guarantee higher subscriber
or view totals — several younger channels outrank older ones in the sample.

## Analysis 7 — Expected Views (`07_expected_views_analysis.py`)

Two baselines per channel, defined in the notebook:

```text
overall expected views = total channel views ÷ total video count
recent expected views  = views of the (preprocessed) recent-200 videos ÷ their count
```

Each video is compared against these baselines; per-category pie charts show the share
of videos meeting each expectation, and the script version bands results by view
quartiles. In every category, most videos fall short of the channel baseline. Part of this is
built into the baseline: views are right-skewed, so a mean pulled up by a few hits sits
above most videos. A median baseline was not computed.

## Analysis 8 — Subscriber Ratio (`08_subscriber_ratio_analysis.py`)

Compares each channel's total views against total subscribers, computes the ratio, and
benchmarks it against the category average, generating per-channel guidance tables (in
the notebook output). The real-data figure contains two Fashion panels: a first pass
that sums the subscriber count over every video row (`'sum'`), and a corrected pass that
takes one value per channel (`'max'`). The Mukbang and Travel panels still use `'sum'`, so
their ratios are not per-channel views-per-subscriber, and no cross-channel finding is
drawn from this analysis. The script version takes one value per channel but was not run
on the real data.

## Korean Language Handling

- Titles are tokenized by extracting Hangul spans with a regex (no morphological
  analyzer is used; `konlpy` is listed as an optional dependency but not wired in).
- Plots set Malgun Gothic (Windows) or AppleGothic (macOS) via `setup_matplotlib()` so
  Korean labels render; without it, matplotlib's default font shows boxes.
- DataFrame columns are Korean throughout — any new analysis code must use the same
  column names (`조회수`, `좋아요 수`, `댓글 수`, `구독자수`, `게시일`, ...).
