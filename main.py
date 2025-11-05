"""
BlackJack Helper API
A mobile app API to identify blackjack hands from video frames.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import base64
import os
from openai import OpenAI
import io
from PIL import Image
import json
import re

app = FastAPI(
    title="BlackJack Helper API",
    description="API for analyzing blackjack game frames and detecting cards",
    version="1.0.0"
)

# Configure CORS for mobile app access
# Note: In production, replace "*" with specific allowed origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Configure specific origins for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Card(BaseModel):
    """Represents a detected playing card."""
    rank: str = Field(..., description="Card rank (A, 2-10, J, Q, K)")
    suit: str = Field(..., description="Card suit (hearts, diamonds, clubs, spades)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Detection confidence score")


class GameState(BaseModel):
    """Represents the current blackjack game state."""
    player_cards: List[Card] = Field(default_factory=list, description="Player's cards")
    dealer_cards: List[Card] = Field(default_factory=list, description="Dealer's cards")
    player_total: Optional[int] = Field(None, description="Player's hand total")
    dealer_total: Optional[int] = Field(None, description="Dealer's hand total")
    recommendation: Optional[str] = Field(None, description="Suggested action (hit, stand, double, split)")


class AnalyzeFrameRequest(BaseModel):
    """Request model for frame analysis."""
    image_base64: str = Field(..., description="Base64 encoded image of the game frame")


class AnalyzeFrameResponse(BaseModel):
    """Response model for frame analysis."""
    success: bool = Field(..., description="Whether analysis was successful")
    game_state: Optional[GameState] = Field(None, description="Detected game state")
    error: Optional[str] = Field(None, description="Error message if analysis failed")


def calculate_hand_value(cards: List[Card]) -> int:
    """
    Calculate the total value of a blackjack hand.
    Aces are counted as 11 or 1 to maximize hand value without busting.
    """
    total = 0
    aces = 0
    
    for card in cards:
        if card.rank == 'A':
            aces += 1
            total += 11
        elif card.rank in ['J', 'Q', 'K']:
            total += 10
        else:
            total += int(card.rank)
    
    # Adjust for aces if busting
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    
    return total

def get_strategy(d, p1, p2, player_total):
    hard_totals = {
        (5, d): 'H' for d in range(2, 12)
    } | {
        (6, d): 'H' for d in range(2, 12)
    } | {
        (7, d): 'H' for d in range(2, 12)
    } | {
        (8, d): 'H' for d in range(2, 12)
    } | {
        (9, d): 'D' if d in [3, 4, 5, 6] else 'H' for d in range(2, 12)
    } | {
        (10, d): 'D' if d not in [10, 11] else 'H' for d in range(2, 12)
    } | {
        (11, d): 'D' for d in range(2, 12)
    } | {
        (12, d): 'S' if d in [4, 5, 6] else 'H' for d in range(2, 12)
    } | {
        (13, d): 'S' if d in [2, 3, 4, 5, 6] else 'H' for d in range(2, 12)
    } | {
        (14, d): 'S' if d in [2, 3, 4, 5, 6] else 'H' for d in range(2, 12)
    } | {
        (15, d): 'S' if d in [2, 3, 4, 5, 6] else 'H' for d in range(2, 12)
    } | {
        (16, d): 'S' if d in [2, 3, 4, 5, 6] else 'H' for d in range(2, 12)
    } | {
        (17, d): 'S' for d in range(2, 12)
    } | {
        (18, d): 'S' for d in range(2, 12)
    } | {
        (19, d): 'S' for d in range(2, 12)
    }

    soft_totals = {
        ('A,2', d): 'D' if d in [5, 6] else 'H' for d in range(2, 12)
    } | {
        ('A,3', d): 'D' if d in [5, 6] else 'H' for d in range(2, 12)
    } | {
        ('A,4', d): 'D' if d in [4, 5, 6] else 'H' for d in range(2, 12)
    } | {
        ('A,5', d): 'D' if d in [4, 5, 6] else 'H' for d in range(2, 12)
    } | {
        ('A,6', d): 'D' if d in [3, 4, 5, 6] else 'H' for d in range(2, 12)
    } | {
        ('A,7', d): 'D' if d in [2, 3, 4, 5, 6] else ('S' if d in [7, 8] else 'H') for d in range(2, 12)
    } | {
        ('A,8', d): 'D' if d == 6 else 'S' for d in range(2, 12)
    } | {
        ('A,9', d): 'S' for d in range(2, 12)
    }

    pairs = {
        (2, 2, d): 'SP' if d in [2, 3, 4, 5, 6, 7] else 'H' for d in range(2, 12)
    } | {
        (3, 3, d): 'SP' if d in [2, 3, 4, 5, 6, 7] else 'H' for d in range(2, 12)
    } | {
        (4, 4, d): 'SP' if d in [5, 6] else 'H' for d in range(2, 12)
    } | {
        (5, 5, d): 'D' if d in [2, 3, 4, 5, 6, 7, 8, 9] else 'H' for d in range(2, 12)
    } | {
        (6, 6, d): 'SP' if d in [2, 3, 4, 5, 6] else ('H' if d in [7, 8, 9, 10, 11] else 'SP') for d in range(2, 12)
    } | {
        (7, 7, d): 'SP' if d in [2, 3, 4, 5, 6, 7] else 'H' for d in range(2, 12)
    } | {
        (8, 8, d): 'SP' for d in range(2, 12)
    } | {
        (9, 9, d): 'SP' if d in [2, 3, 4, 5, 6, 8, 9] else 'S' for d in range(2, 12)
    } | {
        (10, 10, d): 'S' for d in range(2, 12)
    } | {
        ('A', 'A', d): 'SP' for d in range(2, 12)
    }

    if p1 == 'A':
        p1 = '11'
    if p2 == 'A':
        p2 = '11'
    if d == 'A':
        d = '11'

    if p1 == 'J' or p1 == 'Q' or p1 == 'K':
        p1 = '10'
    if p2 == 'J' or p2 == 'Q' or p2 == 'K':
        p2 = '10'
    if d == 'J' or d == 'Q' or d == 'K':
        d = '10'


    
    if p1 == '11' or p2 == '11':
        if p1 != '11':
            return soft_totals[("A," + p1, int(d))]
        elif p2 != '11':
            return soft_totals[("A," + p2, int(d))]
        else:
            return pairs[('A', 'A', int(d))]
    elif p1 == p2:
        return pairs[(int(p1), int(p2), int(d))]
    else:
        return hard_totals[(player_total, int(d))]



def get_recommendation(player_cards: int, dealer_visible_card: Optional[Card], player_total: int) -> str:
    """
    Get basic strategy recommendation for the player.
    This is a simplified version of blackjack basic strategy.
    """
    if player_cards and len(player_cards) == 2 and dealer_visible_card:
        d = dealer_visible_card.rank
        p1 = player_cards[0].rank
        p2 = player_cards[1].rank
        strategy = get_strategy(d, p1, p2, player_total)
        return strategy


async def analyze_frame_with_gpt4(image_base64: str) -> GameState:
    """
    Use GPT-4 Vision API to analyze the game frame and detect cards.
    """
    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
    
    client = OpenAI(api_key=api_key)
    
    # Construct the prompt for GPT-4 Vision
    prompt = """Analyze this blackjack game image and identify all visible cards.

Please identify:
1. Player's cards (the cards in the player's hand)
2. Dealer's cards (the cards in the dealer's hand)

For each card, provide:
- Rank: A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K
- Suit: hearts, diamonds, clubs, or spades
- Confidence: your confidence level from 0.0 to 1.0

Return the results in the following JSON format:
{
  "player_cards": [
    {"rank": "A", "suit": "hearts", "confidence": 0.95},
    {"rank": "K", "suit": "spades", "confidence": 0.90}
  ],
  "dealer_cards": [
    {"rank": "7", "suit": "diamonds", "confidence": 0.85}
  ]
}

If you cannot clearly identify any cards, return empty arrays for player_cards and dealer_cards."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Updated to current vision model
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        
        # Parse the response
        result_text = response.choices[0].message.content
        
        # Extract JSON from the response (GPT-4 might add explanation text)
        # Try to find JSON in the response
        json_match = re.search(r'\{[\s\S]*\}', result_text)
        if json_match:
            result_json = json.loads(json_match.group())
        else:
            result_json = {"player_cards": [], "dealer_cards": []}
        
        # Parse cards
        player_cards = [Card(**card) for card in result_json.get("player_cards", [])]
        dealer_cards = [Card(**card) for card in result_json.get("dealer_cards", [])]
        
        # Calculate totals
        player_total = calculate_hand_value(player_cards) if player_cards else None
        dealer_total = calculate_hand_value(dealer_cards) if dealer_cards else None
        
        # Get recommendation
        recommendation = None
        if player_total and dealer_cards:
            recommendation = get_recommendation(player_cards, dealer_cards[0], player_total)
        
        return GameState(
            player_cards=player_cards,
            dealer_cards=dealer_cards,
            player_total=player_total,
            dealer_total=dealer_total,
            recommendation=recommendation
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing frame: {str(e)}")


@app.post("/api/analyze-frame", response_model=AnalyzeFrameResponse)
async def analyze_frame(request: AnalyzeFrameRequest):
    """
    Process a video frame and return detected cards and game state.
    
    This endpoint accepts a base64-encoded image of a blackjack game frame,
    uses GPT-4 Vision API to identify the cards, and returns the game state
    with recommendations.
    """
    try:
        # Validate base64 image
        try:
            image_data = base64.b64decode(request.image_base64)
            image = Image.open(io.BytesIO(image_data))
            # Verify it's a valid image
            image.verify()
        except Exception as e:
            return AnalyzeFrameResponse(
                success=False,
                error=f"Invalid image data: {str(e)}"
            )
        
        # Analyze the frame using GPT-4 Vision
        game_state = await analyze_frame_with_gpt4(request.image_base64)
        
        return AnalyzeFrameResponse(
            success=True,
            game_state=game_state
        )
        
    except HTTPException as e:
        # Catch HTTPException and return as structured error
        return AnalyzeFrameResponse(
            success=False,
            error=str(e.detail)
        )
    except Exception as e:
        return AnalyzeFrameResponse(
            success=False,
            error=f"Error processing frame: {str(e)}"
        )


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "BlackJack Helper API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "analyze_frame": "/api/analyze-frame"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
