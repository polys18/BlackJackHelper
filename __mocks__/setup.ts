// Mock react-native-vision-camera
jest.mock('react-native-vision-camera', () => ({
  Camera: 'Camera',
  useCameraDevice: jest.fn(() => ({ id: 'mock-device' })),
  useCameraPermission: jest.fn(() => ({
    hasPermission: true,
    requestPermission: jest.fn(),
  })),
}));

// Mock react-native-fs
jest.mock('react-native-fs', () => ({
  readFile: jest.fn(() => Promise.resolve('base64data')),
  writeFile: jest.fn(() => Promise.resolve()),
  unlink: jest.fn(() => Promise.resolve()),
  exists: jest.fn(() => Promise.resolve(true)),
  DocumentDirectoryPath: '/mock/documents',
}));

// Mock OpenAI
jest.mock('openai', () => {
  return {
    __esModule: true,
    default: jest.fn().mockImplementation(() => ({
      chat: {
        completions: {
          create: jest.fn(() =>
            Promise.resolve({
              choices: [
                {
                  message: {
                    content: JSON.stringify({
                      playerCards: [{ rank: 'A', suit: 'hearts' }],
                      dealerCards: [{ rank: 'K', suit: 'spades' }],
                      confidence: 0.95,
                    }),
                  },
                },
              ],
            })
          ),
        },
      },
    })),
  };
});
