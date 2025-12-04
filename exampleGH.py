import requests
import base64

# Read and encode image
print("Loading image...")
# with open("blackjack_frame.jpeg", "rb") as image_file:
with open("Q10-Q.jpeg", "rb") as image_file:
# with open("35-3.jpeg", "rb") as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

# Call API
print("Sending request to API...")
response = requests.post(
    "http://192.168.68.52:8000/api/analyze-frame",
    json={"image_base64": image_base64},
    timeout=60
)

result = response.json()
if result["success"]:
    game_state = result["game_state"]
    print(f"\n✅ Success!")
    print(f"Player cards: {game_state['player_cards']}")
    print(f"Player total: {game_state['player_total']}")
    print(f"Dealer cards: {game_state['dealer_cards']}")
    print(f"Dealer total: {game_state['dealer_total']}")
    print(f"Recommendation: {game_state['recommendation']}")
    
    # Print card counting information
    if game_state.get('player_running_count') is not None:
        print(f"\n📊 Card Count (Hi-Lo):")
        print(f"  Frame - Player count: {game_state['player_running_count']}")
        print(f"  Frame - Dealer count: {game_state['dealer_running_count']}")
        print(f"  Frame - Total count: {game_state['total_running_count']}")
        if game_state.get('cumulative_running_count') is not None:
            print(f"  🎯 Cumulative running count: {game_state['cumulative_running_count']}")
else:
    print(f"\n❌ Error: {result.get('error', 'Unknown error')}")