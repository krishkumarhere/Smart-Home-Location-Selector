from location_scorer import LocationScorer
from data_loader import DataLoader
from user_preference import UserPreference

class RecommendationEngine:
    """Main engine to generate location recommendations"""
    
    def __init__(self):
        self.data_loader = DataLoader()
        self.data = None
        self.scorer = None
    
    def initialize(self):
        """Initialize the recommendation engine"""
        print("\n🔄 Initializing recommendation engine...")
        
        # Load data
        self.data = self.data_loader.load_data()
        if self.data is None:
            print("✗ Failed to load data")
            return False
        
        # Validate data
        if not self.data_loader.validate_data():
            print("✗ Data validation failed")
            return False
        
        print("✓ Engine initialized successfully\n")
        return True
    
    def get_recommendations(self, preferences, top_n=5):
        """Get top N recommendations based on user preferences"""
        
        # Create scorer with city-specific data
        city_data = self.data_loader.get_city_data(preferences.city)
        if city_data.empty:
            print(f"✗ No locations found in {preferences.city}")
            return None
        
        self.scorer = LocationScorer(city_data)
        
        # Apply filters
        filtered = self.scorer.apply_filters(preferences)
        
        if filtered.empty:
            print("✗ No locations match your criteria. Try adjusting your preferences.")
            return None
        
        print(f"✓ Found {len(filtered)} matching locations, ranking top {top_n}...\n")
        
        # Rank locations
        recommendations = self.scorer.rank_locations(filtered, preferences, top_n=top_n)
        
        return recommendations
    
    def display_recommendations(self, recommendations):
        """Display recommendations in a formatted way"""
        if recommendations is None or recommendations.empty:
            print("No recommendations available")
            return
        
        print("\n" + "="*80)
        print("TOP RECOMMENDED LOCATIONS")
        print("="*80)
        
        for idx, (_, location) in enumerate(recommendations.iterrows(), 1):
            details = self.scorer.get_location_details(location)
            
            print(f"\n🏠 RECOMMENDATION #{idx}: {details['Area']}, {details['City']}")
            print("-" * 80)
            print(f"   Match Score: {details['Match_Score']} ⭐")
            print(f"\n   💰 Pricing:")
            print(f"      Purchase Price: {details['Price_per_sqft']} per sqft")
            print(f"      Monthly Rent: {details['Monthly_Rent']}")
            print(f"\n   🔒 Safety & Environment:")
            print(f"      Safety Score: {details['Safety_Score']}")
            print(f"      Pollution Index: {details['Pollution_Index']}")
            print(f"\n   🏥 Essential Services:")
            print(f"      Hospital Distance: {details['Hospital_Distance']}")
            print(f"      School Distance: {details['School_Distance']}")
            print(f"      Metro Access: {details['Metro_Distance']}")
            print(f"\n   📡 Utilities:")
            print(f"      Internet Speed: {details['Internet_Speed']}")
            print(f"      Water Availability: {details['Water_Score']}/10")
            print()
    
    def get_comparison(self, recommendations):
        """Get a comparative summary of recommendations"""
        if recommendations is None or recommendations.empty:
            return
        
        import pandas as pd
        
        comparison_df = recommendations[[
            'City', 'Area', 'Avg_Price_per_sqft', 'Avg_Rent', 
            'Safety_Score', 'Pollution_Index', 'Metro_Distance_km',
            'Hospital_Distance_km', 'School_Distance_km', 'Score'
        ]].reset_index(drop=True)
        
        comparison_df.columns = [
            'City', 'Area', 'Price/sqft', 'Rent', 'Safety', 
            'Pollution', 'Metro (km)', 'Hospital (km)', 'School (km)', 'Score'
        ]
        
        print("\n" + "="*120)
        print("COMPARATIVE ANALYSIS")
        print("="*120)
        print(comparison_df.to_string(index=False))
        print("="*120 + "\n")
    
    def export_recommendations(self, recommendations, filename='recommendations.csv'):
        """Export recommendations to CSV"""
        if recommendations is None or recommendations.empty:
            print("No recommendations to export")
            return
        
        export_cols = [
            'City', 'Area', 'Avg_Price_per_sqft', 'Avg_Rent',
            'Safety_Score', 'Pollution_Index', 'Hospital_Distance_km',
            'School_Distance_km', 'Metro_Distance_km', 'Internet_Speed_Mbps',
            'Water_Availability_Score', 'Score'
        ]
        
        export_data = recommendations[export_cols].copy()
        export_data['Score'] = export_data['Score'].apply(lambda x: f"{x:.2%}")
        
        export_data.to_csv(filename, index=False)
        print(f"✓ Recommendations exported to {filename}")
