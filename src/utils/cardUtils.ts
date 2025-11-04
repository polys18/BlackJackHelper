import { Card } from '../types';

export function calculateHandValue(cards: Card[]): number {
  let value = 0;
  let aces = 0;

  for (const card of cards) {
    if (card.rank === 'A') {
      aces += 1;
      value += 11;
    } else {
      value += card.value;
    }
  }

  // Adjust for aces if value is over 21
  while (value > 21 && aces > 0) {
    value -= 10;
    aces -= 1;
  }

  return value;
}

export function getCardDisplay(card: Card): string {
  const suitSymbols = {
    hearts: '♥',
    diamonds: '♦',
    clubs: '♣',
    spades: '♠',
  };
  
  return `${card.rank}${suitSymbols[card.suit]}`;
}

export function isBlackjack(cards: Card[]): boolean {
  return cards.length === 2 && calculateHandValue(cards) === 21;
}

export function isBust(cards: Card[]): boolean {
  return calculateHandValue(cards) > 21;
}
