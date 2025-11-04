"""
Tests for the BlackJack Helper API
"""

import pytest
from fastapi.testclient import TestClient
from main import app, Card, calculate_hand_value, get_recommendation, GameState
import base64
import io
from PIL import Image


client = TestClient(app)


def create_dummy_image_base64():
    """Create a dummy base64-encoded image for testing."""
    img = Image.new('RGB', (100, 100), color='red')
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    return base64.b64encode(buf.getvalue()).decode('utf-8')


class TestRootEndpoints:
    """Test root and health endpoints."""
    
    def test_root(self):
        """Test root endpoint returns API information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "BlackJack Helper API"
        assert data["version"] == "1.0.0"
        assert "endpoints" in data
    
    def test_health(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestCardModel:
    """Test Card model validation."""
    
    def test_valid_card(self):
        """Test creating a valid card."""
        card = Card(rank="A", suit="hearts", confidence=0.95)
        assert card.rank == "A"
        assert card.suit == "hearts"
        assert card.confidence == 0.95
    
    def test_card_confidence_range(self):
        """Test card confidence must be between 0 and 1."""
        with pytest.raises(ValueError):
            Card(rank="K", suit="spades", confidence=1.5)
        
        with pytest.raises(ValueError):
            Card(rank="Q", suit="clubs", confidence=-0.1)


class TestHandValueCalculation:
    """Test hand value calculation logic."""
    
    def test_simple_hand(self):
        """Test simple hand without aces."""
        cards = [
            Card(rank="7", suit="hearts", confidence=0.9),
            Card(rank="K", suit="spades", confidence=0.9)
        ]
        assert calculate_hand_value(cards) == 17
    
    def test_hand_with_ace_as_11(self):
        """Test hand where ace counts as 11."""
        cards = [
            Card(rank="A", suit="hearts", confidence=0.9),
            Card(rank="9", suit="spades", confidence=0.9)
        ]
        assert calculate_hand_value(cards) == 20
    
    def test_hand_with_ace_as_1(self):
        """Test hand where ace counts as 1 to avoid bust."""
        cards = [
            Card(rank="A", suit="hearts", confidence=0.9),
            Card(rank="K", suit="spades", confidence=0.9),
            Card(rank="5", suit="diamonds", confidence=0.9)
        ]
        assert calculate_hand_value(cards) == 16
    
    def test_hand_with_multiple_aces(self):
        """Test hand with multiple aces."""
        cards = [
            Card(rank="A", suit="hearts", confidence=0.9),
            Card(rank="A", suit="spades", confidence=0.9),
            Card(rank="9", suit="diamonds", confidence=0.9)
        ]
        assert calculate_hand_value(cards) == 21
    
    def test_blackjack(self):
        """Test blackjack (ace + face card)."""
        cards = [
            Card(rank="A", suit="hearts", confidence=0.9),
            Card(rank="K", suit="spades", confidence=0.9)
        ]
        assert calculate_hand_value(cards) == 21
    
    def test_face_cards(self):
        """Test face cards are valued at 10."""
        cards = [
            Card(rank="J", suit="hearts", confidence=0.9),
            Card(rank="Q", suit="spades", confidence=0.9),
            Card(rank="K", suit="diamonds", confidence=0.9)
        ]
        assert calculate_hand_value(cards) == 30


class TestRecommendationLogic:
    """Test game recommendation logic."""
    
    def test_recommend_stand_on_17_or_higher(self):
        """Test recommendation to stand on 17 or higher."""
        dealer_card = Card(rank="7", suit="hearts", confidence=0.9)
        assert get_recommendation(17, dealer_card) == "stand"
        assert get_recommendation(20, dealer_card) == "stand"
    
    def test_recommend_hit_on_11_or_lower(self):
        """Test recommendation to hit on 11 or lower."""
        dealer_card = Card(rank="7", suit="hearts", confidence=0.9)
        assert get_recommendation(11, dealer_card) == "hit"
        assert get_recommendation(8, dealer_card) == "hit"
    
    def test_recommend_stand_against_weak_dealer(self):
        """Test recommendation to stand against weak dealer cards (2-6)."""
        weak_cards = ["2", "3", "4", "5", "6"]
        for rank in weak_cards:
            dealer_card = Card(rank=rank, suit="hearts", confidence=0.9)
            assert get_recommendation(13, dealer_card) == "stand"
    
    def test_recommend_hit_against_strong_dealer(self):
        """Test recommendation to hit against strong dealer cards (7-A)."""
        strong_cards = ["7", "8", "9", "10", "J", "Q", "K", "A"]
        for rank in strong_cards:
            dealer_card = Card(rank=rank, suit="hearts", confidence=0.9)
            assert get_recommendation(13, dealer_card) == "hit"


class TestAnalyzeFrameEndpoint:
    """Test the analyze-frame endpoint."""
    
    def test_analyze_frame_invalid_base64(self):
        """Test endpoint with invalid base64 data."""
        response = client.post(
            "/api/analyze-frame",
            json={"image_base64": "not-valid-base64!!!"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "error" in data
    
    def test_analyze_frame_valid_image_structure(self):
        """Test endpoint accepts valid base64 image structure."""
        image_base64 = create_dummy_image_base64()
        response = client.post(
            "/api/analyze-frame",
            json={"image_base64": image_base64}
        )
        assert response.status_code == 200
        # Response should have the correct structure
        data = response.json()
        assert "success" in data
        # If OpenAI API key is not configured, expect error message
        if not data["success"]:
            assert "error" in data
        
    def test_analyze_frame_missing_image(self):
        """Test endpoint with missing image data."""
        response = client.post(
            "/api/analyze-frame",
            json={}
        )
        assert response.status_code == 422  # Validation error


class TestGameStateModel:
    """Test GameState model."""
    
    def test_empty_game_state(self):
        """Test creating an empty game state."""
        state = GameState()
        assert state.player_cards == []
        assert state.dealer_cards == []
        assert state.player_total is None
        assert state.dealer_total is None
    
    def test_game_state_with_cards(self):
        """Test game state with cards."""
        player_cards = [Card(rank="A", suit="hearts", confidence=0.9)]
        dealer_cards = [Card(rank="K", suit="spades", confidence=0.9)]
        state = GameState(
            player_cards=player_cards,
            dealer_cards=dealer_cards,
            player_total=11,
            dealer_total=10,
            recommendation="hit"
        )
        assert len(state.player_cards) == 1
        assert len(state.dealer_cards) == 1
        assert state.player_total == 11
        assert state.dealer_total == 10
        assert state.recommendation == "hit"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
