# 🎬 YouTube Channel Analysis Project

A comprehensive data analysis project that analyzes YouTube channel performance across different categories using data science techniques.

## 📊 Project Overview

This project analyzes YouTube channels across various categories including:
- **Gaming**
- **Food & Cooking**
- **K-POP**
- **Kids Content**
- **Science & Technology**
- **Entertainment**

## 🔍 Main Analysis Features

### 1. **Word Cloud Analysis** (`01_wordcloud_analysis.py`)
- Generates visual word clouds for top 5 channels in each category
- Analyzes most frequently used keywords in video titles
- Identifies trending terms and content themes by category
- **Visualizations**: Category-specific word clouds with Korean text processing

### 2. **Upload Timing Analysis** (`02_upload_timing_analysis.py`)
- **Day of Week Optimization**: Identifies best upload days for maximum engagement
- **Hour-by-Hour Analysis**: Determines optimal upload times throughout the day
- **Heatmap Visualizations**: Shows upload patterns and performance correlations
- **Category-Specific Insights**: Tailored timing recommendations per content type

### 3. **Upload Frequency Analysis** (`03_upload_frequency_analysis.py`)
- **Upload Interval Calculation**: Analyzes posting frequency patterns (daily, weekly, monthly)
- **Frequency Performance Correlation**: Measures impact of upload consistency on views
- **Optimal Schedule Recommendations**: Data-driven posting frequency suggestions
- **Channel Comparison**: Benchmarks upload strategies across top performers

### 4. **Correlation Analysis** (`04_correlation_analysis.py`)
- **Statistical Correlation**: Pearson and Spearman correlation analysis
- **Views vs Engagement**: Relationship between views, likes, and comments
- **Significance Testing**: P-value calculations for statistical validity
- **Scatter Plot Visualizations**: Visual correlation matrices and trend lines

### 5. **Video Duration Analysis** (`05_video_duration_analysis.py`)
- **Length Optimization**: Analyzes optimal video durations for each category
- **Duration Categorization**: Groups videos by length ranges (short, medium, long)
- **Performance Impact**: Measures how duration affects views and engagement
- **Category-Specific Recommendations**: Tailored duration strategies per content type

### 6. **Channel Age Analysis** (`06_channel_age_analysis.py`)
- **Creation Date Impact**: Analyzes how channel age affects subscriber growth
- **Age vs Performance**: Correlation between channel maturity and view counts
- **Growth Pattern Analysis**: Identifies optimal growth trajectories
- **Benchmarking by Age**: Compares performance across different channel age groups

### 7. **Expected Views Analysis** (`07_expected_views_analysis.py`)
- **Performance Prediction**: Calculates expected vs actual view performance
- **Success Rate Metrics**: Measures how often channels meet performance expectations
- **Performance Grading**: Categorizes channels by success rate (A/B/C/D/F grades)
- **Trend Analysis**: Identifies channels consistently exceeding expectations

### 8. **Subscriber Ratio Analysis** (`08_subscriber_ratio_analysis.py`)
- **Engagement Efficiency**: Views per subscriber ratio analysis
- **Subscriber Value**: Measures subscriber quality vs quantity
- **Performance Grades**: Rates channels on subscriber engagement effectiveness
- **ROI Analysis**: Subscriber growth vs content performance correlation

## 📁 Project Structure

```
YouTube-Channel-Analysis/
├── 📊 data/                          # CSV data files for each channel category
│   ├── Gaming.csv
│   ├── Food.csv
│   ├── Kids.csv
│   ├── KPOP.csv
│   ├── Science.csv
│   └── Variety.csv
├── 📓 notebooks/                     # Original Jupyter notebook
│   └── Youtube_Channel_Analysis_Project.ipynb
├── 📈 analysis/                     # Individual analysis scripts
│   ├── data_preprocessing.py        # Common data processing functions
│   ├── 01_wordcloud_analysis.py     # Word cloud generation
│   ├── 02_upload_timing_analysis.py # Upload timing optimization
│   ├── 03_upload_frequency_analysis.py # Upload frequency analysis
│   ├── 04_correlation_analysis.py   # Statistical correlation analysis
│   ├── 05_video_duration_analysis.py # Video duration optimization
│   ├── 06_channel_age_analysis.py   # Channel age vs performance
│   ├── 07_expected_views_analysis.py # Expected vs actual performance
│   └── 08_subscriber_ratio_analysis.py # Subscriber engagement analysis
├── 🎨 visualizations/               # Generated charts and graphs
│   ├── 01_wordcloud_[category].png
│   ├── 02_upload_timing_[category].png
│   ├── 03_upload_frequency_[category].png
│   ├── 04_correlation_[category].png
│   ├── 05_video_duration_[category].png
│   ├── 06_channel_age_[category].png
│   ├── 07_expected_views_[category].png
│   └── 08_subscriber_ratio_[category].png
├── 📋 requirements.txt              # Python dependencies
└── 📄 README.md
```

## 🛠 Technologies Used

- **Python**: Data analysis and visualization
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Static plotting and visualization
- **Seaborn**: Statistical data visualization
- **WordCloud**: Text analysis and word cloud generation
- **Jupyter Notebook**: Interactive data analysis environment

## 📋 Requirements

```bash
pip install pandas matplotlib seaborn wordcloud numpy scipy scikit-learn jupyter notebook
```

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/Youtube-Channel-Analysis-Project.git
   cd Youtube-Channel-Analysis-Project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run individual analyses**
   ```bash
   # Run all analyses
   cd analysis
   python 01_wordcloud_analysis.py
   python 02_upload_timing_analysis.py
   python 03_upload_frequency_analysis.py
   python 04_correlation_analysis.py
   python 05_video_duration_analysis.py
   python 06_channel_age_analysis.py
   python 07_expected_views_analysis.py
   python 08_subscriber_ratio_analysis.py
   ```

   **Or run the original Jupyter notebook**
   ```bash
   jupyter notebook notebooks/Youtube_Channel_Analysis_Project.ipynb
   ```

## 📊 Key Analysis Insights

### 🕒 Upload Timing Optimization
- **Best Days**: Analysis reveals optimal upload days for each category
- **Peak Hours**: Identifies time slots with highest engagement rates
- **Heatmap Analysis**: Visual patterns showing day/hour performance correlations
- **Category Variations**: Different content types show distinct optimal schedules

### 📅 Upload Frequency Impact
- **Consistency Metrics**: How regular posting affects view performance
- **Frequency Categories**: Daily vs weekly vs monthly posting analysis
- **Performance Correlation**: Statistical relationship between frequency and success
- **Optimal Intervals**: Data-driven recommendations for posting schedules

### 📊 Statistical Correlations
- **Views vs Engagement**: Strong correlation analysis between metrics
- **Significance Testing**: P-value validation for statistical reliability
- **Performance Predictors**: Key factors that drive channel success
- **Category Differences**: Varying correlation patterns across content types

### ⏱️ Video Duration Strategy
- **Length Optimization**: Optimal video durations for maximum engagement
- **Category Patterns**: Different optimal lengths for different content types
- **Attention Span Analysis**: How duration affects viewer retention
- **Performance Impact**: Statistical significance of duration on success

### 📈 Channel Growth Analysis
- **Age vs Performance**: How channel maturity affects subscriber growth
- **Growth Trajectories**: Optimal development patterns for new channels
- **Benchmark Comparisons**: Performance standards by channel age groups
- **Success Predictors**: Early indicators of long-term channel success

### 🎯 Performance Expectations
- **Success Rate Metrics**: How often channels meet performance targets
- **Grade Classification**: A-F grading system for channel performance
- **Trend Identification**: Channels consistently exceeding expectations
- **Predictive Modeling**: Expected vs actual performance analysis

### 👥 Subscriber Efficiency
- **Engagement Quality**: Views per subscriber ratio analysis
- **Subscriber Value**: Quality vs quantity subscriber assessment
- **ROI Analysis**: Return on investment for subscriber acquisition
- **Efficiency Grades**: Rating system for subscriber engagement effectiveness

## 📈 Data Sources

The project analyzes data from various YouTube channels across multiple categories:
- Gaming channels with subscriber counts ranging from 100K to 10M+
- Food & cooking channels from different cultural backgrounds
- K-POP content including music videos and variety shows
- Educational science and technology channels
- Entertainment and variety content creators

## 🎯 Use Cases

### For Content Creators
- **Upload Schedule Optimization**: Data-driven upload timing recommendations
- **Content Strategy**: Keyword and topic suggestions based on successful patterns
- **Performance Benchmarking**: Compare against category averages and top performers

### For Marketing Professionals
- **Campaign Planning**: Understand audience engagement patterns
- **Influencer Selection**: Identify high-performing channels in target categories
- **Trend Forecasting**: Spot emerging content trends early

### For Data Analysts
- **Methodology Reference**: Learn YouTube data analysis techniques
- **Visualization Examples**: Explore effective ways to present social media data
- **Statistical Analysis**: Understand correlation and pattern identification methods

## 🔮 Future Enhancements

- **Real-time Data Integration**: API integration for live data updates
- **Sentiment Analysis**: Comment sentiment analysis for engagement quality
- **Predictive Modeling**: Machine learning models for performance prediction
- **Competitor Analysis**: Automated competitor benchmarking tools
- **Interactive Dashboard**: Web-based visualization dashboard

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or collaboration opportunities, please open an issue or contact the project maintainer.

---

**Made with ❤️ using Python and data science**