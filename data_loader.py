import pandas as pd
from config import DATASET_PATH

class DataLoader:
    """Handle loading and validation of location dataset"""
    
    def __init__(self, filepath=DATASET_PATH):
        self.filepath = filepath
        self.data = None
    
    def load_data(self):
        """Load dataset from CSV"""
        try:
            self.data = pd.read_csv(self.filepath)
            print(f"✓ Dataset loaded successfully: {len(self.data)} locations")
            return self.data
        except FileNotFoundError:
            print(f"✗ Error: Dataset file not found at {self.filepath}")
            return None
        except Exception as e:
            print(f"✗ Error loading dataset: {e}")
            return None
    
    def get_cities(self):
        """Get list of unique cities"""
        if self.data is None:
            return []
        return sorted(self.data['City'].unique().tolist())
    
    def get_areas(self, city):
        """Get all areas for a specific city"""
        if self.data is None:
            return []
        city_data = self.data[self.data['City'] == city]
        return sorted(city_data['Area'].unique().tolist())
    
    def get_city_data(self, city):
        """Get all locations for a specific city"""
        if self.data is None:
            return pd.DataFrame()
        return self.data[self.data['City'] == city].reset_index(drop=True)
    
    def validate_data(self):
        """Validate dataset integrity"""
        if self.data is None:
            print("✗ No data loaded")
            return False
        
        required_columns = [
            'City', 'Area', 'Avg_Price_per_sqft', 'Avg_Rent', 'Safety_Score',
            'Pollution_Index', 'Hospital_Distance_km', 'School_Distance_km',
            'Metro_Distance_km', 'Grocery_Distance_km', 'Internet_Speed_Mbps',
            'Water_Availability_Score'
        ]
        
        missing_cols = [col for col in required_columns if col not in self.data.columns]
        if missing_cols:
            print(f"✗ Missing columns: {missing_cols}")
            return False
        
        if self.data.isnull().any().any():
            print("⚠ Warning: Dataset contains null values")
        
        print("✓ Dataset validation passed")
        return True
    
    def get_stats(self, city=None):
        """Get statistical summary of dataset"""
        data = self.data if city is None else self.get_city_data(city)
        
        if data.empty:
            return None
        
        return {
            'total_locations': len(data),
            'cities': data['City'].unique().tolist() if city is None else [city],
            'price_range': (data['Avg_Price_per_sqft'].min(), data['Avg_Price_per_sqft'].max()),
            'safety_range': (data['Safety_Score'].min(), data['Safety_Score'].max()),
            'pollution_range': (data['Pollution_Index'].min(), data['Pollution_Index'].max()),
        }
