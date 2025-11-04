export type CardSuit = 'hearts' | 'diamonds' | 'clubs' | 'spades';
export type CardRank = 'A' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '10' | 'J' | 'Q' | 'K';

export interface Card {
  rank: CardRank;
  suit: CardSuit;
  value: number;
}

export interface GameState {
  playerCards: Card[];
  dealerCards: Card[];
  isCapturing: boolean;
  lastAnalysis: string | null;
}

export interface CardClassificationResult {
  playerCards: Card[];
  dealerCards: Card[];
  confidence: number;
  rawResponse: string;
}
