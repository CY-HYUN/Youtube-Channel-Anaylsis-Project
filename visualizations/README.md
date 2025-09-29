# 📊 Visualization Examples

This folder contains all the generated visualizations from the YouTube Channel Analysis Project.

## 🎨 Generated Visualizations

When you run the analysis scripts, the following visualizations will be automatically generated:

### 1. Word Cloud Analysis
- `01_wordcloud_[category].png` - Visual word clouds showing most frequent keywords in video titles

### 2. Upload Timing Analysis
- `02_upload_timing_[category].png` - Heatmaps and charts showing optimal upload days and hours

### 3. Upload Frequency Analysis
- `03_upload_frequency_[category].png` - Charts showing correlation between upload frequency and performance

### 4. Correlation Analysis
- `04_correlation_[category].png` - Statistical correlation matrices and scatter plots

### 5. Video Duration Analysis
- `05_video_duration_[category].png` - Duration vs performance analysis charts

### 6. Channel Age Analysis
- `06_channel_age_[category].png` - Channel age vs subscriber/view correlations

### 7. Expected Views Analysis
- `07_expected_views_[category].png` - Expected vs actual performance analysis

### 8. Subscriber Ratio Analysis
- `08_subscriber_ratio_[category].png` - Subscriber efficiency and engagement metrics

## 📂 File Naming Convention

All visualization files follow the pattern:
```
[analysis_number]_[analysis_name]_[category].png
```

Categories include:
- Gaming
- Food
- Kids
- KPOP
- Science
- Variety

## 🔧 How to Generate

Run any of the analysis scripts from the `analysis/` folder:

```bash
cd analysis
python 01_wordcloud_analysis.py
# This will generate visualizations for all categories
```

## 📈 Visualization Features

- **High Resolution**: All charts saved at 300 DPI for professional quality
- **Consistent Styling**: Korean font support and professional color schemes
- **Multiple Chart Types**: Bar charts, scatter plots, heatmaps, word clouds, box plots
- **Statistical Annotations**: P-values, correlation coefficients, and trend lines
- **Category-Specific**: Tailored visualizations for each content category

## 💡 Usage Tips

- All visualizations are saved as PNG files for universal compatibility
- File sizes are optimized for both web display and print quality
- Charts include detailed legends and axis labels in Korean
- Color schemes are designed to be colorblind-friendly where possible