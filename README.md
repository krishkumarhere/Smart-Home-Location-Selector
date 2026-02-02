# Smart Home Location Selector 🏠

A data-driven recommendation system to help users find the most suitable residential locations in major Indian metro cities based on their personal preferences.

## 📋 Project Overview

This system assists users in choosing residential locations by:
- Analyzing multiple criteria (safety, proximity to schools/hospitals, transportation access, budget, etc.)
- Scoring and ranking locations based on personalized preferences
- Providing detailed recommendations with clear reasoning

## 🏙️ Supported Cities

- Hyderabad
- Mumbai
- Delhi NCR
- Chennai
- Bengaluru
- Pune

## 🎯 Key Features

### User Inputs
- **City Selection**: Choose from major metro areas
- **Budget Range**: Set purchase price or rental budget
- **Preference Weights**: Customize importance of different factors
- **Must-Have Constraints**: Specify minimum safety scores, max pollution, etc.

### Evaluation Criteria

1. **Budget** - Purchase price or rental costs
2. **Safety** - Safety score (1-10)
3. **Healthcare** - Distance to hospitals
4. **Education** - Distance to schools
5. **Transportation** - Metro access distance
6. **Environment** - Pollution levels
7. **Utilities** - Internet speed, water availability
8. **Lifestyle** - Green spaces, amenities

### Output
- **Top Ranked Locations**: Personalized recommendations with match scores
- **Detailed Comparison**: Side-by-side analysis of options
- **Export Capability**: Save recommendations to CSV

## 📊 Dataset

**File**: `smart_home_location_dataset.csv`

**Contains**: ~20,000 residential area records across 6 metro cities with 15 attributes

## 🚀 Installation

1. **Clone/Navigate to project directory**
```bash
cd Smart-Home-Location-Selector
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Ensure dataset is present**
```bash
smart_home_location_dataset.csv
```

## ▶️ Usage

### Basic Usage
```bash
python main.py
```

### Interactive Workflow
1. Select preferred city
2. Choose budget range (purchase or rental)
3. Adjust preference weights
4. Set must-have constraints
5. View recommendations with detailed analysis
6. Export results if desired

## 🏗️ Project Structure

```
Smart-Home-Location-Selector/
├── main.py                          # Application entry point
├── config.py                        # Configuration & settings
├── data_loader.py                   # Dataset loading & validation
├── user_preference.py               # User preference management
├── location_scorer.py               # Scoring & ranking logic
├── recommendation_engine.py         # Main recommendation engine
├── smart_home_location_dataset.csv  # Main dataset
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 🔧 Configuration

Edit `config.py` to customize:
- Supported cities
- Default preference weights
- Budget ranges
- Safety/pollution thresholds
- Distance constraints
- Number of top recommendations

## 📈 Scoring Algorithm

The system uses a normalized weighted scoring approach:

1. **Normalization**: All metrics are scaled to 0-1 range
   - Positive metrics (safety, internet): Higher = Better
   - Negative metrics (distance, pollution): Lower = Better

2. **Weighting**: User preferences are applied as weights

3. **Ranking**: Locations are ranked by final composite score

## 🔮 Future Enhancements

- [ ] Machine learning-based recommendations
- [ ] User feedback integration
- [ ] Real-time price data updates
- [ ] Web interface (Flask/Streamlit)
- [ ] API for third-party integrations
- [ ] Additional cities and criteria
- [ ] Community ratings system
- [ ] Advanced filtering with date ranges

## 📝 Example Output

```
🏠 RECOMMENDATION #1: Indiranagar, Bengaluru
Match Score: 87.34% ⭐

💰 Pricing:
   Purchase Price: ₹7565 per sqft
   Monthly Rent: ₹43205

🔒 Safety & Environment:
   Safety Score: 8.9/10
   Pollution Index: 194

🏥 Essential Services:
   Hospital Distance: 2.13 km
   School Distance: 1.65 km
   Metro Access: 0.37 km
```

## 📄 License

[Add your license here]

## 👤 Author

Krish

---

**Note**: This system provides recommendations based on structured data. Actual property decisions should also consider market conditions, personal visits, and legal verifications.
