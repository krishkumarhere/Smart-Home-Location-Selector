import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

class LocationScorer:
    """Score and rank locations based on user preferences"""
    
    def __init__(self, data):
        self.data = data.copy()
        self.scaler = MinMaxScaler()
        self.normalized_data = None
        self._normalize_metrics()
    
    def _normalize_metrics(self):
        """Normalize all metrics to 0-1 scale"""
        self.normalized_data = self.data.copy()
        
        # Metrics to normalize (1 = better)
        positive_metrics = [
            'Safety_Score',
            'Internet_Speed_Mbps',
            'Water_Availability_Score',
            'Lifestyle_Score',
            'Green_Space_Score',
            'Power_Backup'
        ]
        
        # Metrics to normalize (0 = better, invert)
        negative_metrics = [
            'Pollution_Index',
            'Hospital_Distance_km',
            'School_Distance_km',
            'Metro_Distance_km',
            'Grocery_Distance_km',
            'Avg_Price_per_sqft',
            'Avg_Rent'
        ]
        
        # Normalize positive metrics
        for col in positive_metrics:
            if col in self.data.columns:
                col_data = self.data[[col]].values
                normalized = self.scaler.fit_transform(col_data)
                self.normalized_data[f'{col}_norm'] = normalized
        
        # Normalize negative metrics (invert: 1 - normalized)
        for col in negative_metrics:
            if col in self.data.columns:
                col_data = self.data[[col]].values
                normalized = self.scaler.fit_transform(col_data)
                self.normalized_data[f'{col}_norm'] = 1 - normalized
    
    def apply_filters(self, preferences):
        """Filter locations based on user preferences"""
        filtered_data = self.normalized_data.copy()
        
        # Filter by budget
        if preferences.prefer_rent:
            filtered_data = filtered_data[
                (filtered_data['Avg_Rent'] >= preferences.budget_min) &
                (filtered_data['Avg_Rent'] <= preferences.budget_max)
            ]
        else:
            filtered_data = filtered_data[
                (filtered_data['Avg_Price_per_sqft'] >= preferences.budget_min) &
                (filtered_data['Avg_Price_per_sqft'] <= preferences.budget_max)
            ]
        
        # Apply must-haves
        for constraint, value in preferences.must_haves.items():
            if constraint == 'min_safety':
                filtered_data = filtered_data[
                    filtered_data['Safety_Score'] >= value
                ]
            elif constraint == 'max_pollution':
                filtered_data = filtered_data[
                    filtered_data['Pollution_Index'] <= value
                ]
            elif constraint == 'max_metro_distance':
                filtered_data = filtered_data[
                    filtered_data['Metro_Distance_km'] <= value
                ]
        
        return filtered_data
    
    def calculate_score(self, location_row, preferences):
        """Calculate composite score for a location"""
        score = 0
        
        # Map weights to columns
        weight_mapping = {
            'safety': 'Safety_Score_norm',
            'hospitals': 'Hospital_Distance_km_norm',
            'schools': 'School_Distance_km_norm',
            'metro': 'Metro_Distance_km_norm',
            'pollution': 'Pollution_Index_norm',
            'internet': 'Internet_Speed_Mbps_norm',
            'water': 'Water_Availability_Score_norm',
            'budget': 'Avg_Price_per_sqft_norm' if not preferences.prefer_rent else 'Avg_Rent_norm',
        }
        
        for criterion, weight in preferences.weights.items():
            col = weight_mapping.get(criterion)
            if col and col in location_row.index:
                value = location_row.get(col, 0)
                if pd.notna(value):
                    score += value * weight
        
        return score
    
    def rank_locations(self, filtered_data, preferences, top_n=5):
        """Rank filtered locations based on preferences"""
        if filtered_data.empty:
            return pd.DataFrame()
        
        # Calculate scores
        filtered_data['Score'] = filtered_data.apply(
            lambda row: self.calculate_score(row, preferences),
            axis=1
        )
        
        # Sort by score (descending)
        ranked = filtered_data.sort_values('Score', ascending=False)
        
        return ranked.head(top_n)
    
    def get_location_details(self, location_row):
        """Get detailed metrics for a location"""
        return {
            'City': location_row['City'],
            'Area': location_row['Area'],
            'Price_per_sqft': f"₹{location_row['Avg_Price_per_sqft']:.0f}",
            'Monthly_Rent': f"₹{location_row['Avg_Rent']:.0f}",
            'Safety_Score': f"{location_row['Safety_Score']:.1f}/10",
            'Pollution_Index': f"{location_row['Pollution_Index']:.0f}",
            'Hospital_Distance': f"{location_row['Hospital_Distance_km']:.2f} km",
            'School_Distance': f"{location_row['School_Distance_km']:.2f} km",
            'Metro_Distance': f"{location_row['Metro_Distance_km']:.2f} km",
            'Internet_Speed': f"{location_row['Internet_Speed_Mbps']:.0f} Mbps",
            'Water_Score': f"{location_row['Water_Availability_Score']:.1f}/10",
            'Match_Score': f"{location_row['Score']:.2%}",
        }
