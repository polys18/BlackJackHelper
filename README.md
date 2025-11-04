# BlackJackHelper

A mobile app API to identify blackjack hands from video frames using GPT-4 Vision.

## Features

- **Card Detection**: Uses GPT-4 Vision API to detect playing cards in video frames
- **Game State Analysis**: Identifies player and dealer cards with confidence scores
- **Hand Value Calculation**: Automatically calculates blackjack hand values
- **Strategy Recommendations**: Provides basic strategy recommendations (hit/stand)
- **RESTful API**: Clean, well-documented API endpoints

## Requirements

- Python 3.8+
- OpenAI API key with GPT-4 Vision access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/polys18/BlackJackHelper.git
cd BlackJackHelper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Running the API

Start the server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

### Interactive API Docs

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Endpoints

#### POST /api/analyze-frame

Analyzes a video frame to detect cards and determine game state.

**Request Body:**
```json
{
  "image_base64": "base64-encoded-image-string"
}
```

**Response:**
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

#### GET /

Returns API information and available endpoints.

#### GET /health

Health check endpoint.

## Usage Example

```python
import requests
import base64

# Read and encode image
with open("blackjack_frame.jpg", "rb") as image_file:
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
    print(f"Recommendation: {game_state['recommendation']}")
```

## Testing

Run the test suite:
```bash
pytest test_main.py -v
```

## Architecture

The API is built with:
- **FastAPI**: Modern, fast web framework for building APIs
- **OpenAI GPT-4 Vision**: For card detection and game analysis
- **Pydantic**: Data validation using Python type annotations
- **Pillow**: Image processing and validation

## Card Detection

The API uses GPT-4 Vision with a structured prompt to:
1. Identify all visible cards in the frame
2. Determine card rank (A, 2-10, J, Q, K) and suit
3. Provide confidence scores for each detection
4. Separate player and dealer cards

## Strategy Recommendations

Basic blackjack strategy is implemented:
- **17+**: Always stand
- **11 or less**: Always hit
- **12-16**: Stand against dealer 2-6, hit against dealer 7-A

## Future Enhancements

- Support for split and double down recommendations
- Multiple player detection
- Betting recommendations
- Hand history tracking
- Real-time video stream processing

## License

MIT