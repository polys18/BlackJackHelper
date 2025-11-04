import React from 'react';
import { StyleSheet, View, Text, ScrollView } from 'react-native';
import { Card } from '../types';
import { calculateHandValue, getCardDisplay, isBlackjack, isBust } from '../utils/cardUtils';

interface CardDisplayProps {
  playerCards: Card[];
  dealerCards: Card[];
}

export const CardDisplay: React.FC<CardDisplayProps> = ({ playerCards, dealerCards }) => {
  const playerValue = calculateHandValue(playerCards);
  const dealerValue = calculateHandValue(dealerCards);
  const playerHasBlackjack = isBlackjack(playerCards);
  const playerIsBust = isBust(playerCards);

  const renderCards = (cards: Card[], title: string, value: number) => {
    if (cards.length === 0) return null;

    return (
      <View style={styles.handContainer}>
        <Text style={styles.handTitle}>{title}</Text>
        <View style={styles.cardsRow}>
          {cards.map((card, index) => (
            <View key={index} style={styles.cardContainer}>
              <Text style={styles.cardText}>{getCardDisplay(card)}</Text>
            </View>
          ))}
        </View>
        <View style={styles.valueContainer}>
          <Text style={styles.valueLabel}>Total Value:</Text>
          <Text style={[
            styles.valueText,
            value > 21 && styles.bustText,
            value === 21 && styles.blackjackText,
          ]}>
            {value}
          </Text>
        </View>
        {value === 21 && cards.length === 2 && (
          <Text style={styles.blackjackLabel}>BLACKJACK! 🎉</Text>
        )}
        {value > 21 && (
          <Text style={styles.bustLabel}>BUST! 💥</Text>
        )}
      </View>
    );
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.contentContainer}>
      {renderCards(dealerCards, "Dealer's Hand", dealerValue)}
      {renderCards(playerCards, "Your Hand", playerValue)}
      
      {playerCards.length > 0 && dealerCards.length > 0 && (
        <View style={styles.recommendationContainer}>
          <Text style={styles.recommendationTitle}>Recommendation</Text>
          <Text style={styles.recommendationText}>
            {getRecommendation(playerValue, dealerCards[0], playerHasBlackjack, playerIsBust)}
          </Text>
        </View>
      )}
    </ScrollView>
  );
};

function getRecommendation(
  playerValue: number,
  dealerUpCard: Card | undefined,
  hasBlackjack: boolean,
  playerBust: boolean
): string {
  if (playerBust) {
    return 'You have bust. Dealer wins.';
  }
  
  if (hasBlackjack) {
    return 'Blackjack! You win (unless dealer also has blackjack).';
  }

  if (!dealerUpCard) {
    return 'Waiting for dealer card...';
  }

  const dealerUpValue = dealerUpCard.value;

  // Basic strategy recommendations
  if (playerValue >= 17) {
    return 'STAND - Your hand is strong enough.';
  }

  if (playerValue <= 11) {
    return 'HIT - You cannot bust, safe to take another card.';
  }

  if (playerValue === 12) {
    if (dealerUpValue >= 4 && dealerUpValue <= 6) {
      return 'STAND - Dealer has a weak card, let them bust.';
    }
    return 'HIT - Your hand is weak.';
  }

  if (playerValue >= 13 && playerValue <= 16) {
    if (dealerUpValue >= 2 && dealerUpValue <= 6) {
      return 'STAND - Dealer has a weak card, let them bust.';
    }
    return 'HIT - Dealer has a strong card.';
  }

  return 'Consider your options carefully.';
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  contentContainer: {
    padding: 20,
  },
  handContainer: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  handTitle: {
    fontSize: 20,
    fontWeight: '700',
    marginBottom: 15,
    color: '#333',
  },
  cardsRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 15,
  },
  cardContainer: {
    width: 60,
    height: 80,
    backgroundColor: '#f8f8f8',
    borderRadius: 8,
    borderWidth: 2,
    borderColor: '#007AFF',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 10,
    marginBottom: 10,
  },
  cardText: {
    fontSize: 24,
    fontWeight: '600',
  },
  valueContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 10,
  },
  valueLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#666',
    marginRight: 10,
  },
  valueText: {
    fontSize: 24,
    fontWeight: '700',
    color: '#007AFF',
  },
  bustText: {
    color: '#FF3B30',
  },
  blackjackText: {
    color: '#34C759',
  },
  blackjackLabel: {
    fontSize: 18,
    fontWeight: '700',
    color: '#34C759',
    marginTop: 10,
    textAlign: 'center',
  },
  bustLabel: {
    fontSize: 18,
    fontWeight: '700',
    color: '#FF3B30',
    marginTop: 10,
    textAlign: 'center',
  },
  recommendationContainer: {
    backgroundColor: '#007AFF',
    borderRadius: 12,
    padding: 20,
    marginTop: 10,
  },
  recommendationTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#fff',
    marginBottom: 10,
  },
  recommendationText: {
    fontSize: 16,
    color: '#fff',
    lineHeight: 24,
  },
});
