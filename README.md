# YouTube Channel Analysis Project

Statistical analysis of what actually drives video performance on Korean YouTube — upload timing, upload cadence, video duration, and engagement patterns — across 15 top channels in Fashion, Mukbang, and Travel.

*Python · pandas · SciPy · Matplotlib/Seaborn · YouTube Data API v3 · 15 channels, 2,125 videos.*

## Results at a Glance

- **2,125 videos / 15 channels / 3 categories** analyzed: the 5 top Korean channels in each of Fashion, Mukbang, and Travel, up to 200 recent videos per channel (Shorts and statistical outliers removed).
- **Daily uploading was optimal for only 3 of 15 channels.** The view-maximizing upload interval is channel-specific, ranging from 1 day up to 8–14 days — there is no universal "best cadence."
- **For 10 of 15 channels, one upload interval maximized both views and likes**, so cadence effects are consistent across engagement metrics.
- **Likes track views far more tightly than comments** in every one of the 18 per-channel and per-category scatter panels — likes are the more reliable engagement signal.
- **Channel age does not predict channel size:** older channels do not necessarily have more subscribers or total views.

![Correlation analysis: views vs likes and views vs comments per channel](visualizations/04_correlation/correlation_analysis.png)

*Views vs likes (blue) and views vs comments (red) for each channel and category aggregate — one of 8 checked-in result visualizations from the real-data run.*

## Quick Start

Clone the repository:

```bash
git clone https://github.com/CY-HYUN/Youtube-Channel-Anaylsis-Project.git
cd Youtube-Channel-Anaylsis-Project
```

Install dependencies:

```bash
# Python 3.9-3.11 (the pinned original environment):
pip install -r requirements.txt

# Python 3.12+ (the pins predate 3.12 — install current versions instead):
pip install pandas numpy scipy matplotlib seaborn wordcloud
```

Run:

```bash
# Smoke test — loads and preprocesses data, prints a summary
python analysis/data_preprocessing.py
# expected output:
#   Using sample data for demonstration...
#   Total records: 3000
#   Categories: ['Gaming' 'Food' 'KPOP' 'Kids' 'Science' 'Variety']
#   Columns: ['카테고리', '채널명', '제목', '조회수', ...]

# Run one full analysis end-to-end, headless (saves PNGs into visualizations/)
MPLBACKEND=Agg python analysis/02_upload_timing_analysis.py
```

Analyses 02, 03, 04, 06, 07, and 08 run end-to-end on the built-in sample data the same
way (verified). Analysis 01 additionally requires the `wordcloud` package, and analysis 05
needs a per-video duration column (`재생 시간(분)`) that only the real dataset provides —
it errors out on the sample data. Without `MPLBACKEND=Agg`, each script opens interactive
plot windows (`plt.show()`).

> **Data note:** The original dataset — three CSVs of channel and video metadata collected
> via the YouTube Data API v3 — is private and not included in this repo (`*.csv` is
> gitignored). When no data is present, the scripts fall back to a **built-in synthetic
> sample generator** (3,000 rows, fixed seed), so a fresh-clone run demonstrates the
> pipeline but does not reproduce the findings above. All reported numbers come from the
> original-data run preserved in `notebooks/Youtube_Channel_Anaylsis_Project.ipynb`
> (outputs checked in) and the result PNGs in `visualizations/`. The `load_from_youtube_api()`
> helper is a stub — re-collecting the dataset requires implementing it with your own API key.

## Repository Structure

```text
Youtube Channel Anaylsis Project/
├── analysis/                           # Modular pipeline: 8 standalone analyses + shared preprocessing
│   ├── data_preprocessing.py           # Shared module: loading, sample generator, cleaning, Korean fonts
│   ├── 01_wordcloud_analysis.py        # Title keywords per category (requires wordcloud)
│   ├── 02_upload_timing_analysis.py    # Average views by upload day-of-week / hour-of-day
│   ├── 03_upload_frequency_analysis.py # Views and likes vs days-between-uploads
│   ├── 04_correlation_analysis.py      # Pearson correlation: views-likes, views-comments
│   ├── 05_video_duration_analysis.py   # Top-10 vs bottom-10 videos by duration
│   ├── 06_channel_age_analysis.py      # Channel age vs subscribers and total views
│   ├── 07_expected_views_analysis.py   # Actual vs expected views per channel
│   └── 08_subscriber_ratio_analysis.py # Views-per-subscriber efficiency
├── notebooks/                          # Original bilingual (KR/EN) notebook run on the real dataset
├── visualizations/                     # Checked-in result PNGs from the real-data run (one folder per analysis)
├── requirements.txt                    # Pinned original environment (Python 3.9-3.11)
└── README.md
```

Two layers do the same analysis in different forms:

- **`notebooks/`** — the original analysis, executed against the real CSVs; its cell outputs
  (per-channel results, tables, figures) are preserved in the notebook and exported to
  `visualizations/`.
- **`analysis/`** — the same eight analyses refactored into standalone, importable scripts
  sharing one preprocessing module, runnable on any dataset with the expected schema
  (falls back to the sample generator otherwise).

DataFrame columns are Korean, matching the source data: `카테고리` (category), `채널명`
(channel), `제목` (title), `조회수` (views), `좋아요 수` (likes), `댓글 수` (comments),
`구독자수` (subscribers), `게시일` (upload date).

## The 8 Analyses

| # | Analysis | Question | Result figure |
| --- | --- | --- | --- |
| 1 | Word cloud | Which title keywords do top channels in each category use? | [PNG](visualizations/01_wordcloud/wordcloud_analysis.png) |
| 2 | Upload timing | Which upload day/hour gets the highest average views? | [PNG](visualizations/02_timing_analysis/upload_timing.png) |
| 3 | Upload frequency | Which interval between uploads maximizes views and likes? | [PNG](visualizations/03_upload_frequency/upload_frequency.png) |
| 4 | Correlation | How tightly do likes and comments track views? | [PNG](visualizations/04_correlation/correlation_analysis.png) |
| 5 | Video duration | Do longer videos get fewer views? | [PNG](visualizations/05_duration/video_duration.png) |
| 6 | Channel age | Do older channels have more subscribers/views? | [PNG](visualizations/06_channel_age/channel_age.png) |
| 7 | Expected views | Which videos beat their channel's expected view count? | [PNG](visualizations/07_expected_views/expected_views.png) |
| 8 | Subscriber ratio | Which channels get the most views per subscriber? | [PNG](visualizations/08_subscriber_ratio/subscriber_ratio.png) |

## Key Findings

**Upload cadence is channel-specific, not universal.** Per-channel optimum intervals
(after IQR outlier removal on views) ranged from 1 day to 8–14 days. Only 3 of 15
channels performed best with daily uploads; several top travel and mukbang channels
peaked at 8–14 day intervals. The full per-channel table is in
[docs/DETAILS.md](docs/DETAILS.md).

**Likes are the more consistent engagement metric.** In all 18 scatter panels (15
channels + 3 category aggregates), likes rise almost linearly with views, while comments
stay flat and noisy. If you can only monitor one engagement signal against views, use likes.

**Channel age is a weak predictor of scale.** Comparing creation dates against total
subscribers and views shows older channels do not systematically dominate — recent,
consistent channels can match or beat channels years older.

**Expectation shortfalls are normal.** Comparing each video against its channel baseline
(total views ÷ total videos, and a recent-200-videos baseline), a substantial share of
videos in every category miss their expected view count — under-performance relative to
channel average is routine, not exceptional.

**Subscriber count alone misleads.** Total-views-to-subscriber ratios vary widely between
channels in the same category, so subscriber count without an efficiency ratio is a poor
proxy for actual audience engagement.

## Methodology Summary

- **Collection:** YouTube Data API v3; the 5 top channels per category; up to 200 recent
  videos per channel; video metadata (views, likes, comments, duration, upload datetime)
  plus channel metadata (subscribers, creation date, total views).
- **Preprocessing:** comma-formatted numbers coerced to integers, upload datetimes parsed
  with day-of-week / hour extraction, Shorts (≤ 60s) removed, rows with unparseable dates
  dropped.
- **Outlier handling:** 1.5×IQR filter on views for the cadence analysis; 99th-percentile
  trims in the duration, channel-age, and expected-views analyses.
- **Statistics:** groupby aggregations, day×hour pivot heatmaps, Pearson correlation
  (views–likes, views–comments), quartile-based expected-view bands.
- **Visualization:** matplotlib + seaborn with Korean font handling (Malgun Gothic);
  bilingual Korean/English labels.

Full per-analysis methodology and the per-channel results table:
[docs/DETAILS.md](docs/DETAILS.md).

## Limitations

- The sample is 15 top channels in 3 categories — findings describe these channels, not
  all of YouTube.
- The real-data correlation results are preserved as scatterplots; numeric Pearson
  coefficients are computed by `analysis/04_correlation_analysis.py` only when a dataset
  is supplied (the original notebook run did not print them).
- `load_from_youtube_api()` is a stub; data re-collection is not turnkey.

## Tech Stack

Python · pandas · NumPy · SciPy · Matplotlib · Seaborn · WordCloud · Jupyter ·
google-api-python-client (YouTube Data API v3)

## License

MIT — see [LICENSE](LICENSE).
