"""
Example script demonstrating how to use the BlackJack Helper API.
"""

import requests
import base64
from io import BytesIO
from PIL import Image


def create_sample_image():
    """Create a sample image for testing (in production, this would be a real blackjack frame)."""
    img = Image.new('RGB', (800, 600), color='green')
    buf = BytesIO()
    img.save(buf, format='JPEG')
    return base64.b64encode(buf.getvalue()).decode('utf-8')


def analyze_blackjack_frame(image_base64, api_url="http://localhost:8000"):
    """
    Send a frame to the API for analysis.
    
    Args:
        image_base64: Base64-encoded image string
        api_url: URL of the API server
        
    Returns:
        dict: API response with game state
    """
    response = requests.post(
        f"{api_url}/api/analyze-frame",
        json={"image_base64": image_base64}
    )
    return response.json()


def main():
    """Main example function."""
    print("BlackJack Helper API Example")
    print("=" * 50)
    
    # Create a sample image (in production, this would come from camera/video)
    print("\n1. Creating sample image...")
    image_base64 = create_sample_image()
    print(f"   Image size: {len(image_base64)} bytes (base64)")
    
    # Send to API for analysis
    print("\n2. Sending to API for analysis...")
    try:
        result = analyze_blackjack_frame(image_base64)
        
        print("\n3. Results:")
        print(f"   Success: {result['success']}")
        
        if result['success'] and result['game_state']:
            game_state = result['game_state']
            
            print(f"\n   Player's Cards:")
            for card in game_state['player_cards']:
                print(f"     - {card['rank']} of {card['suit']} (confidence: {card['confidence']:.2f})")
            
            print(f"\n   Dealer's Cards:")
            for card in game_state['dealer_cards']:
                print(f"     - {card['rank']} of {card['suit']} (confidence: {card['confidence']:.2f})")
            
            if game_state['player_total']:
                print(f"\n   Player Total: {game_state['player_total']}")
            
            if game_state['dealer_total']:
                print(f"   Dealer Total: {game_state['dealer_total']}")
            
            if game_state['recommendation']:
                print(f"\n   Recommendation: {game_state['recommendation'].upper()}")
        else:
            print(f"   Error: {result.get('error', 'Unknown error')}")
            
    except requests.exceptions.ConnectionError:
        print("\n   ERROR: Could not connect to API server.")
        print("   Make sure the server is running: python main.py")
    except Exception as e:
        print(f"\n   ERROR: {str(e)}")


if __name__ == "__main__":
    main()
