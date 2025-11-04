import React, { useState, useCallback } from 'react';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  Alert,
  TextInput,
  Modal,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { CameraComponent } from '../components/CameraComponent';
import { CardDisplay } from '../components/CardDisplay';
import { visionService } from '../services/openai';
import { GameState } from '../types';

export const MainScreen: React.FC = () => {
  const [gameState, setGameState] = useState<GameState>({
    playerCards: [],
    dealerCards: [],
    isCapturing: false,
    lastAnalysis: null,
  });
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [showApiKeyModal, setShowApiKeyModal] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [hasApiKey, setHasApiKey] = useState(false);

  const handlePhotoTaken = useCallback(async (photoPath: string) => {
    if (!hasApiKey) {
      Alert.alert(
        'API Key Required',
        'Please set your OpenAI API key first.',
        [{ text: 'OK', onPress: () => setShowApiKeyModal(true) }]
      );
      return;
    }

    setIsAnalyzing(true);
    try {
      const result = await visionService.analyzeBlackjackCards(`file://${photoPath}`);
      
      setGameState({
        playerCards: result.playerCards,
        dealerCards: result.dealerCards,
        isCapturing: false,
        lastAnalysis: result.rawResponse,
      });

      if (result.playerCards.length === 0 && result.dealerCards.length === 0) {
        Alert.alert(
          'No Cards Detected',
          'Could not detect any cards in the image. Please try again with a clearer photo.'
        );
      }
    } catch (error) {
      console.error('Error analyzing photo:', error);
      Alert.alert(
        'Analysis Failed',
        error instanceof Error ? error.message : 'Failed to analyze the cards. Please try again.'
      );
    } finally {
      setIsAnalyzing(false);
    }
  }, [hasApiKey]);

  const handleSetApiKey = useCallback(() => {
    if (apiKey.trim()) {
      visionService.setApiKey(apiKey.trim());
      setHasApiKey(true);
      setShowApiKeyModal(false);
      Alert.alert('Success', 'API key has been set successfully!');
    } else {
      Alert.alert('Error', 'Please enter a valid API key.');
    }
  }, [apiKey]);

  const handleReset = useCallback(() => {
    setGameState({
      playerCards: [],
      dealerCards: [],
      isCapturing: false,
      lastAnalysis: null,
    });
  }, []);

  const hasCards = gameState.playerCards.length > 0 || gameState.dealerCards.length > 0;

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>BlackJack Helper</Text>
        <TouchableOpacity
          style={styles.apiKeyButton}
          onPress={() => setShowApiKeyModal(true)}>
          <Text style={styles.apiKeyButtonText}>
            {hasApiKey ? '🔑 API Key Set' : '⚙️ Set API Key'}
          </Text>
        </TouchableOpacity>
      </View>

      {!hasCards ? (
        <CameraComponent onPhotoTaken={handlePhotoTaken} isAnalyzing={isAnalyzing} />
      ) : (
        <View style={styles.resultsContainer}>
          <CardDisplay
            playerCards={gameState.playerCards}
            dealerCards={gameState.dealerCards}
          />
          <View style={styles.buttonContainer}>
            <TouchableOpacity style={styles.resetButton} onPress={handleReset}>
              <Text style={styles.resetButtonText}>Scan New Game</Text>
            </TouchableOpacity>
          </View>
        </View>
      )}

      <Modal
        visible={showApiKeyModal}
        animationType="slide"
        transparent={true}
        onRequestClose={() => setShowApiKeyModal(false)}>
        <KeyboardAvoidingView
          behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
          style={styles.modalContainer}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>OpenAI API Key</Text>
            <Text style={styles.modalDescription}>
              Enter your OpenAI API key to enable card classification.
              You can get one from platform.openai.com
            </Text>
            <TextInput
              style={styles.input}
              placeholder="sk-..."
              value={apiKey}
              onChangeText={setApiKey}
              secureTextEntry
              autoCapitalize="none"
              autoCorrect={false}
            />
            <View style={styles.modalButtons}>
              <TouchableOpacity
                style={[styles.modalButton, styles.cancelButton]}
                onPress={() => setShowApiKeyModal(false)}>
                <Text style={styles.cancelButtonText}>Cancel</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.modalButton, styles.confirmButton]}
                onPress={handleSetApiKey}>
                <Text style={styles.confirmButtonText}>Set Key</Text>
              </TouchableOpacity>
            </View>
          </View>
        </KeyboardAvoidingView>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  header: {
    backgroundColor: '#1a1a1a',
    paddingTop: 50,
    paddingBottom: 15,
    paddingHorizontal: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: '700',
    color: '#fff',
  },
  apiKeyButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 8,
  },
  apiKeyButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  resultsContainer: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  buttonContainer: {
    padding: 20,
    backgroundColor: '#fff',
    borderTopWidth: 1,
    borderTopColor: '#ddd',
  },
  resetButton: {
    backgroundColor: '#007AFF',
    paddingVertical: 15,
    borderRadius: 10,
    alignItems: 'center',
  },
  resetButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
  modalContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  modalContent: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    width: '85%',
    maxWidth: 400,
  },
  modalTitle: {
    fontSize: 22,
    fontWeight: '700',
    marginBottom: 10,
    color: '#333',
  },
  modalDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 20,
    lineHeight: 20,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    marginBottom: 20,
  },
  modalButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  modalButton: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
    marginHorizontal: 5,
  },
  cancelButton: {
    backgroundColor: '#f0f0f0',
  },
  cancelButtonText: {
    color: '#333',
    fontSize: 16,
    fontWeight: '600',
  },
  confirmButton: {
    backgroundColor: '#007AFF',
  },
  confirmButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});
