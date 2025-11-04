import OpenAI from 'openai';
import { Card, CardClassificationResult } from '../types';
import RNFS from 'react-native-fs';

export class OpenAIVisionService {
  private client: OpenAI | null = null;

  constructor(apiKey?: string) {
    if (apiKey) {
      this.client = new OpenAI({
        apiKey: apiKey,
      });
    }
  }

  async analyzeBlackjackCards(imageUri: string): Promise<CardClassificationResult> {
    if (!this.client) {
      throw new Error('OpenAI client not initialized. Please set API key first.');
    }

    try {
      // Read the image file as base64
      const base64Image = await RNFS.readFile(imageUri, 'base64');
      
      // Create the vision API request
      const response = await this.client.chat.completions.create({
        model: "gpt-4o",
        messages: [
          {
            role: "user",
            content: [
              {
                type: "text",
                text: `Analyze this blackjack game image and identify all visible playing cards.
                
Please identify:
1. Player's cards (cards closest to the bottom of the image or clearly in the player's hand)
2. Dealer's cards (cards at the top or in the dealer's position)

For each card, specify the rank (A, 2-10, J, Q, K) and suit (hearts, diamonds, clubs, spades).

Respond in this exact JSON format:
{
  "playerCards": [{"rank": "A", "suit": "hearts"}, ...],
  "dealerCards": [{"rank": "K", "suit": "spades"}, ...],
  "confidence": 0.95
}`,
              },
              {
                type: "image_url",
                image_url: {
                  url: `data:image/jpeg;base64,${base64Image}`,
                },
              },
            ],
          },
        ],
        max_tokens: 1000,
      });

      const content = response.choices[0]?.message?.content || '';
      
      // Parse the JSON response
      const parsed = this.parseResponse(content);
      
      return {
        ...parsed,
        rawResponse: content,
      };
    } catch (error) {
      console.error('Error analyzing cards:', error);
      throw new Error(`Failed to analyze cards: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  private parseResponse(content: string): {
    playerCards: Card[];
    dealerCards: Card[];
    confidence: number;
  } {
    try {
      // Extract JSON from the response (it might be wrapped in markdown code blocks)
      const jsonMatch = content.match(/\{[\s\S]*\}/);
      if (!jsonMatch) {
        throw new Error('No JSON found in response');
      }
      
      const data = JSON.parse(jsonMatch[0]);
      
      const playerCards = (data.playerCards || []).map((card: any) => 
        this.createCard(card.rank, card.suit)
      );
      
      const dealerCards = (data.dealerCards || []).map((card: any) => 
        this.createCard(card.rank, card.suit)
      );
      
      return {
        playerCards,
        dealerCards,
        confidence: data.confidence || 0,
      };
    } catch (error) {
      console.error('Error parsing response:', error);
      throw new Error('Failed to parse card classification response');
    }
  }

  private createCard(rank: string, suit: string): Card {
    const cardValue = this.getCardValue(rank);
    return {
      rank: rank as any,
      suit: suit as any,
      value: cardValue,
    };
  }

  private getCardValue(rank: string): number {
    switch (rank) {
      case 'A':
        return 11; // Ace can be 1 or 11, defaulting to 11
      case 'J':
      case 'Q':
      case 'K':
        return 10;
      default:
        return parseInt(rank, 10);
    }
  }

  setApiKey(apiKey: string) {
    this.client = new OpenAI({ apiKey });
  }
}

export const visionService = new OpenAIVisionService();
