from config import CITIES, BUDGET_RANGES, RENTAL_RANGES, DEFAULT_WEIGHTS

class UserPreference:
    """Capture and manage user preferences for location selection"""
    
    def __init__(self):
        self.city = None
        self.budget_type = None
        self.budget_min = None
        self.budget_max = None
        self.prefer_rent = False
        self.weights = DEFAULT_WEIGHTS.copy()
        self.must_haves = {}
    
    def get_user_input_interactive(self):
        """Interactive CLI to gather user preferences"""
        print("\n" + "="*60)
        print("SMART HOME LOCATION SELECTOR")
        print("="*60)
        
        # City selection
        print(f"\nAvailable cities: {', '.join(CITIES)}")
        while True:
            city = input("Select your preferred city: ").strip()
            if city in CITIES:
                self.city = city
                break
            print("✗ Invalid city. Please try again.")
        
        # Budget type
        print("\nBudget options:")
        print("1. By purchase price per sqft")
        print("2. By rental amount")
        choice = input("Choose (1 or 2): ").strip()
        
        if choice == '1':
            self.prefer_rent = False
            self._get_price_budget()
        else:
            self.prefer_rent = True
            self._get_rental_budget()
        
        # Preferences
        self._get_preference_weights()
        
        # Must-haves
        self._get_must_haves()
        
        return self
    
    def _get_price_budget(self):
        """Get budget for purchase price"""
        print("\nBudget ranges (price per sqft):")
        for i, (key, (min_val, max_val)) in enumerate(BUDGET_RANGES.items(), 1):
            if max_val == float('inf'):
                print(f"{i}. {key.capitalize()}: ₹{min_val}+")
            else:
                print(f"{i}. {key.capitalize()}: ₹{min_val} - ₹{max_val}")
        
        choice = input("Select budget range (1-4) or enter custom (min,max): ").strip()
        
        if choice in ['1', '2', '3', '4']:
            budget_key = list(BUDGET_RANGES.keys())[int(choice) - 1]
            self.budget_min, self.budget_max = BUDGET_RANGES[budget_key]
        else:
            try:
                min_val, max_val = map(int, choice.split(','))
                self.budget_min, self.budget_max = min_val, max_val
            except:
                print("✗ Invalid input. Using medium budget.")
                self.budget_min, self.budget_max = BUDGET_RANGES['medium']
    
    def _get_rental_budget(self):
        """Get budget for rental"""
        print("\nRental ranges (monthly rent):")
        for i, (key, (min_val, max_val)) in enumerate(RENTAL_RANGES.items(), 1):
            if max_val == float('inf'):
                print(f"{i}. {key.capitalize()}: ₹{min_val}+")
            else:
                print(f"{i}. {key.capitalize()}: ₹{min_val} - ₹{max_val}")
        
        choice = input("Select rental range (1-4) or enter custom (min,max): ").strip()
        
        if choice in ['1', '2', '3', '4']:
            budget_key = list(RENTAL_RANGES.keys())[int(choice) - 1]
            self.budget_min, self.budget_max = RENTAL_RANGES[budget_key]
        else:
            try:
                min_val, max_val = map(int, choice.split(','))
                self.budget_min, self.budget_max = min_val, max_val
            except:
                print("✗ Invalid input. Using medium rental range.")
                self.budget_min, self.budget_max = RENTAL_RANGES['medium']
    
    def _get_preference_weights(self):
        """Adjust preference weights"""
        print("\nPreference weights (1-10 scale, 10 = most important):")
        print("(Press Enter to keep default)\n")
        
        criteria = ['safety', 'hospitals', 'schools', 'metro', 'pollution', 'internet']
        total_weight = 0
        weights = {}
        
        for criterion in criteria:
            default = int(self.weights[criterion] * 100)
            user_input = input(f"  {criterion.capitalize()} (default {default}%): ").strip()
            
            if user_input:
                try:
                    weight = max(0, min(100, int(user_input)))
                    weights[criterion] = weight
                except:
                    weights[criterion] = default
            else:
                weights[criterion] = default
            
            total_weight += weights[criterion]
        
        # Normalize to sum to 1
        if total_weight > 0:
            for criterion in criteria:
                self.weights[criterion] = weights[criterion] / total_weight
    
    def _get_must_haves(self):
        """Get must-have constraints"""
        print("\nMust-have constraints (leave blank to skip):")
        
        min_safety = input("  Minimum safety score (1-10): ").strip()
        if min_safety:
            try:
                self.must_haves['min_safety'] = float(min_safety)
            except:
                pass
        
        max_pollution = input("  Maximum pollution index: ").strip()
        if max_pollution:
            try:
                self.must_haves['max_pollution'] = float(max_pollution)
            except:
                pass
        
        max_metro_dist = input("  Maximum metro distance (km): ").strip()
        if max_metro_dist:
            try:
                self.must_haves['max_metro_distance'] = float(max_metro_dist)
            except:
                pass
    
    def get_summary(self):
        """Return preference summary"""
        summary = f"""
╔═══════════════════════════════════════╗
║     YOUR LOCATION PREFERENCES         ║
╠═══════════════════════════════════════╣
║ City: {self.city}
║ Budget Range: ₹{self.budget_min} - ₹{self.budget_max}
║ Budget Type: {'Rent' if self.prefer_rent else 'Purchase Price'}
║
║ Importance Weights:
"""
        for criterion, weight in self.weights.items():
            summary += f"║   {criterion.capitalize():15} {weight*100:5.1f}%\n"
        
        summary += "║\n║ Must-Haves:\n"
        for constraint, value in self.must_haves.items():
            summary += f"║   {constraint}: {value}\n"
        
        summary += "╚═══════════════════════════════════════╝\n"
        return summary
