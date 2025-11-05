import requests
import base64

# Read and encode image
print("Loading image...")
with open("blackjack_frame.jpeg", "rb") as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

# Call API
print("Sending request to API...")
response = requests.post(
    "http://localhost:8000/api/analyze-frame",
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
else:
    print(f"\n❌ Error: {result.get('error', 'Unknown error')}")