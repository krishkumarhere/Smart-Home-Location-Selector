#!/usr/bin/env python3
"""
Smart Home Location Selector - Main Entry Point
Assists users in choosing suitable residential locations in major Indian metro cities
"""

from recommendation_engine import RecommendationEngine
from user_preference import UserPreference
from config import TOP_N_RECOMMENDATIONS

def main():
    """Main application flow"""
    print("\n" + "="*60)
    print("   SMART HOME LOCATION SELECTOR")
    print("   Find Your Perfect Home in Indian Metro Cities")
    print("="*60)
    
    # Initialize engine
    engine = RecommendationEngine()
    if not engine.initialize():
        print("✗ Failed to initialize. Exiting.")
        return
    
    # Get user preferences
    preferences = UserPreference()
    preferences.get_user_input_interactive()
    
    # Display preference summary
    print(preferences.get_summary())
    
    # Generate recommendations
    input("Press Enter to find your ideal locations...")
    recommendations = engine.get_recommendations(preferences, top_n=TOP_N_RECOMMENDATIONS)
    
    if recommendations is not None and not recommendations.empty:
        # Display recommendations
        engine.display_recommendations(recommendations)
        
        # Show comparison
        engine.get_comparison(recommendations)
        
        # Ask to export
        export_choice = input("Would you like to export these recommendations? (y/n): ").strip().lower()
        if export_choice == 'y':
            engine.export_recommendations(recommendations)
    
    print("\n" + "="*60)
    print("Thank you for using Smart Home Location Selector!")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Application interrupted by user.")
    except Exception as e:
        print(f"\n✗ An error occurred: {e}")
        import traceback
        traceback.print_exc()
