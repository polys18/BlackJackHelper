# API Specification

## BlackJack Helper API v1.0.0

### Base URL
```
http://localhost:8000
```

### Authentication
Currently, the API does not require authentication for endpoints. However, you must configure an OpenAI API key in the environment to use the card detection features.

---

## Endpoints

### 1. Root Endpoint

**GET /**

Returns API information and available endpoints.

#### Response
```json
{
  "name": "BlackJack Helper API",
  "version": "1.0.0",
  "status": "running",
  "endpoints": {
    "analyze_frame": "/api/analyze-frame"
  }
}
```

---

### 2. Health Check

**GET /health**

Health check endpoint to verify API is running.

#### Response
```json
{
  "status": "healthy"
}
```

---

### 3. Analyze Frame

**POST /api/analyze-frame**

Analyzes a blackjack game frame and returns detected cards with recommendations.

#### Request Body
```json
{
  "image_base64": "string (required)"
}
```

- `image_base64`: Base64-encoded JPEG or PNG image of a blackjack game frame

#### Response (Success)
```json
{
  "success": true,
  "game_state": {
    "player_cards": [
      {
        "rank": "A",
        "suit": "hearts",
        "confidence": 0.95
      },
      {
        "rank": "K",
        "suit": "spades",
        "confidence": 0.90
      }
    ],
    "dealer_cards": [
      {
        "rank": "7",
        "suit": "diamonds",
        "confidence": 0.85
      }
    ],
    "player_total": 21,
    "dealer_total": 7,
    "recommendation": "stand"
  },
  "error": null
}
```

#### Response (Error)
```json
{
  "success": false,
  "game_state": null,
  "error": "Error message describing what went wrong"
}
```

#### Field Descriptions

**Card Object:**
- `rank`: Card rank - one of: A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K
- `suit`: Card suit - one of: hearts, diamonds, clubs, spades
- `confidence`: Detection confidence score (0.0 to 1.0)

**Game State Object:**
- `player_cards`: Array of Card objects representing player's hand
- `dealer_cards`: Array of Card objects representing dealer's hand
- `player_total`: Blackjack value of player's hand (null if no cards detected)
- `dealer_total`: Blackjack value of dealer's hand (null if no cards detected)
- `recommendation`: Suggested action - one of: "hit", "stand", "double", "split" (null if insufficient information)

#### Status Codes
- `200 OK`: Request processed successfully (check `success` field)
- `422 Unprocessable Entity`: Invalid request format
- `500 Internal Server Error`: Unexpected server error

---

## Interactive Documentation

When the server is running, you can access interactive API documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Examples

### Python Example
```python
import requests
import base64

# Read image and encode to base64
with open("blackjack_game.jpg", "rb") as image_file:
    image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

# Call API
response = requests.post(
    "http://localhost:8000/api/analyze-frame",
    json={"image_base64": image_base64}
)

result = response.json()
if result["success"]:
    game_state = result["game_state"]
    print(f"Player total: {game_state['player_total']}")
    print(f"Dealer total: {game_state['dealer_total']}")
    print(f"Recommendation: {game_state['recommendation']}")
else:
    print(f"Error: {result['error']}")
```

### JavaScript Example
```javascript
const fs = require('fs');
const fetch = require('node-fetch');

// Read and encode image
const imageBuffer = fs.readFileSync('blackjack_game.jpg');
const imageBase64 = imageBuffer.toString('base64');

// Call API
fetch('http://localhost:8000/api/analyze-frame', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ image_base64: imageBase64 })
})
.then(response => response.json())
.then(result => {
    if (result.success) {
        const gameState = result.game_state;
        console.log(`Player total: ${gameState.player_total}`);
        console.log(`Dealer total: ${gameState.dealer_total}`);
        console.log(`Recommendation: ${gameState.recommendation}`);
    } else {
        console.log(`Error: ${result.error}`);
    }
});
```

### cURL Example
```bash
# First, encode your image to base64
IMAGE_BASE64=$(base64 -w 0 blackjack_game.jpg)

# Call the API
curl -X POST "http://localhost:8000/api/analyze-frame" \
  -H "Content-Type: application/json" \
  -d "{\"image_base64\": \"$IMAGE_BASE64\"}"
```

---

## Error Handling

The API uses a consistent error response format:

```json
{
  "success": false,
  "game_state": null,
  "error": "Description of the error"
}
```

Common error messages:
- `"Invalid image data: ..."`: The provided base64 string is not a valid image
- `"OpenAI API key not configured"`: Server is missing required OpenAI API key
- `"Error analyzing frame: ..."`: Error occurred during GPT-4 Vision analysis

---

## Rate Limiting

Currently, there is no built-in rate limiting. However, usage is subject to OpenAI API rate limits for GPT-4 Vision.

---

## Strategy Recommendations

The API implements basic blackjack strategy:

- **Hard 17+**: Stand
- **Hard 11 or less**: Hit
- **Hard 12-16**:
  - Stand if dealer shows 2-6
  - Hit if dealer shows 7-A
  
Note: This is a simplified basic strategy. Advanced features like pair splitting and doubling down are not yet implemented.

---

## Hand Value Calculation

The API correctly handles blackjack hand values:

- **Number cards (2-10)**: Face value
- **Face cards (J, Q, K)**: 10
- **Aces**: 11 or 1 (automatically adjusted to prevent busting)

Examples:
- A + K = 21 (Blackjack)
- A + 6 = 17 (Soft 17)
- A + K + 5 = 16 (Ace counts as 1)
- A + A + 9 = 21 (One ace as 11, one as 1)
