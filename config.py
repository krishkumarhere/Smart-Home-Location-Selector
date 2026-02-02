# Configuration for Smart Home Location Selector

# Supported cities
CITIES = ['Hyderabad', 'Mumbai', 'Delhi NCR', 'Chennai', 'Bengaluru', 'Pune']

# Dataset path
DATASET_PATH = 'smart_home_location_dataset.csv'

# Default preference weights (0-1 scale, should sum to 1.0)
DEFAULT_WEIGHTS = {
    'budget': 0.20,
    'safety': 0.15,
    'hospitals': 0.15,
    'schools': 0.15,
    'metro': 0.15,
    'pollution': 0.10,
    'internet': 0.05,
    'water': 0.05,
}

# Budget ranges (price per sqft)
BUDGET_RANGES = {
    'low': (0, 8000),
    'medium': (8000, 15000),
    'high': (15000, 25000),
    'luxury': (25000, float('inf')),
}

# Rental ranges (Avg_Rent)
RENTAL_RANGES = {
    'low': (0, 30000),
    'medium': (30000, 50000),
    'high': (50000, 70000),
    'luxury': (70000, float('inf')),
}

# Safety score threshold (1-10 scale)
MIN_SAFETY_SCORE = 5.0

# Maximum acceptable pollution index (lower is better)
MAX_POLLUTION_INDEX = 200

# Maximum acceptable distances (in km)
MAX_DISTANCES = {
    'hospital': 5.0,
    'school': 5.0,
    'metro': 3.0,
    'grocery': 2.0,
}

# Minimum acceptable internet speed (Mbps)
MIN_INTERNET_SPEED = 50

# Number of top recommendations to return
TOP_N_RECOMMENDATIONS = 5
