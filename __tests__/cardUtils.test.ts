import { calculateHandValue, getCardDisplay, isBlackjack, isBust } from '../src/utils/cardUtils';
import { Card } from '../src/types';

describe('cardUtils', () => {
  describe('calculateHandValue', () => {
    it('should calculate simple hand values', () => {
      const cards: Card[] = [
        { rank: '7', suit: 'hearts', value: 7 },
        { rank: '8', suit: 'clubs', value: 8 },
      ];
      expect(calculateHandValue(cards)).toBe(15);
    });

    it('should handle face cards correctly', () => {
      const cards: Card[] = [
        { rank: 'K', suit: 'hearts', value: 10 },
        { rank: 'Q', suit: 'clubs', value: 10 },
      ];
      expect(calculateHandValue(cards)).toBe(20);
    });

    it('should handle Ace as 11 when it does not bust', () => {
      const cards: Card[] = [
        { rank: 'A', suit: 'hearts', value: 11 },
        { rank: '9', suit: 'clubs', value: 9 },
      ];
      expect(calculateHandValue(cards)).toBe(20);
    });

    it('should handle Ace as 1 when it would bust at 11', () => {
      const cards: Card[] = [
        { rank: 'A', suit: 'hearts', value: 11 },
        { rank: '9', suit: 'clubs', value: 9 },
        { rank: '5', suit: 'spades', value: 5 },
      ];
      expect(calculateHandValue(cards)).toBe(15);
    });

    it('should handle multiple Aces correctly', () => {
      const cards: Card[] = [
        { rank: 'A', suit: 'hearts', value: 11 },
        { rank: 'A', suit: 'clubs', value: 11 },
      ];
      expect(calculateHandValue(cards)).toBe(12);
    });
  });

  describe('getCardDisplay', () => {
    it('should display card with suit symbol', () => {
      const card: Card = { rank: 'A', suit: 'hearts', value: 11 };
      expect(getCardDisplay(card)).toBe('A♥');
    });

    it('should display number cards correctly', () => {
      const card: Card = { rank: '10', suit: 'spades', value: 10 };
      expect(getCardDisplay(card)).toBe('10♠');
    });
  });

  describe('isBlackjack', () => {
    it('should return true for Ace and 10-value card', () => {
      const cards: Card[] = [
        { rank: 'A', suit: 'hearts', value: 11 },
        { rank: 'K', suit: 'clubs', value: 10 },
      ];
      expect(isBlackjack(cards)).toBe(true);
    });

    it('should return false for 21 with more than 2 cards', () => {
      const cards: Card[] = [
        { rank: '7', suit: 'hearts', value: 7 },
        { rank: '7', suit: 'clubs', value: 7 },
        { rank: '7', suit: 'spades', value: 7 },
      ];
      expect(isBlackjack(cards)).toBe(false);
    });

    it('should return false for non-21 hand', () => {
      const cards: Card[] = [
        { rank: '10', suit: 'hearts', value: 10 },
        { rank: '9', suit: 'clubs', value: 9 },
      ];
      expect(isBlackjack(cards)).toBe(false);
    });
  });

  describe('isBust', () => {
    it('should return true when hand value exceeds 21', () => {
      const cards: Card[] = [
        { rank: 'K', suit: 'hearts', value: 10 },
        { rank: 'Q', suit: 'clubs', value: 10 },
        { rank: '5', suit: 'spades', value: 5 },
      ];
      expect(isBust(cards)).toBe(true);
    });

    it('should return false when hand value is 21', () => {
      const cards: Card[] = [
        { rank: 'K', suit: 'hearts', value: 10 },
        { rank: 'Q', suit: 'clubs', value: 10 },
        { rank: 'A', suit: 'spades', value: 11 },
      ];
      expect(isBust(cards)).toBe(false);
    });

    it('should return false when hand value is under 21', () => {
      const cards: Card[] = [
        { rank: '9', suit: 'hearts', value: 9 },
        { rank: '7', suit: 'clubs', value: 7 },
      ];
      expect(isBust(cards)).toBe(false);
    });
  });
});
