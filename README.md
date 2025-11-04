# BlackJack Helper

A mobile application that uses your phone's camera and OpenAI Vision API to classify cards dealt in a blackjack game. The app recognizes both the user's cards and the dealer's cards, calculates hand values, and provides basic strategy recommendations.

## Features

- 📷 **Camera Integration**: Uses the phone camera to capture images of blackjack cards
- 🤖 **AI-Powered Card Recognition**: Leverages OpenAI Vision API (GPT-4 Vision) to identify cards
- 🎴 **Dual Card Detection**: Recognizes both player's cards and dealer's cards
- 🎯 **Hand Value Calculation**: Automatically calculates hand values with proper Ace handling
- 💡 **Strategy Recommendations**: Provides basic blackjack strategy recommendations
- 🎨 **Intuitive UI**: Clean, modern interface with real-time feedback

## Prerequisites

- Node.js >= 20
- npm or yarn
- React Native development environment set up
  - For iOS: Xcode, CocoaPods
  - For Android: Android Studio, Android SDK
- OpenAI API key (get one from [platform.openai.com](https://platform.openai.com))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/polys18/BlackJackHelper.git
cd BlackJackHelper
```

2. Install dependencies:
```bash
npm install
```

3. For iOS, install CocoaPods dependencies:
```bash
cd ios
pod install
cd ..
```

## Running the App

### iOS
```bash
npm run ios
```

### Android
```bash
npm run android
```

## Configuration

### Setting up OpenAI API Key

1. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. When you first launch the app, tap the "⚙️ Set API Key" button in the top right
3. Enter your API key in the modal dialog
4. Tap "Set Key" to save

The API key is stored in memory and will need to be re-entered each time you restart the app.

### Permissions

The app requires the following permissions:

**iOS:**
- Camera access (for capturing card images)
- Photo Library access (for saving images)

**Android:**
- Camera permission
- Read/Write external storage

Permissions are requested at runtime when needed.

## Usage

1. **Launch the app** and set your OpenAI API key
2. **Position your phone** above the blackjack table so both your cards and the dealer's cards are visible
3. **Tap the camera button** to capture an image
4. **Wait for analysis** - the app will send the image to OpenAI Vision API
5. **View results** - see your cards, dealer's cards, hand values, and strategy recommendations
6. **Scan new game** - tap "Scan New Game" to start over

## How It Works

1. **Image Capture**: The app uses `react-native-vision-camera` to capture high-quality images
2. **AI Processing**: Images are sent to OpenAI's GPT-4 Vision model with a specialized prompt
3. **Card Classification**: The AI identifies each card's rank (A, 2-10, J, Q, K) and suit
4. **Hand Analysis**: The app calculates hand values and applies blackjack rules
5. **Strategy**: Basic strategy recommendations are provided based on the current game state

## Project Structure

```
BlackJackHelper/
├── src/
│   ├── components/
│   │   ├── CameraComponent.tsx    # Camera interface
│   │   └── CardDisplay.tsx        # Card results display
│   ├── screens/
│   │   └── MainScreen.tsx         # Main app screen
│   ├── services/
│   │   └── openai.ts              # OpenAI Vision API integration
│   ├── types/
│   │   └── index.ts               # TypeScript type definitions
│   └── utils/
│       └── cardUtils.ts           # Card calculation utilities
├── android/                       # Android native code
├── ios/                          # iOS native code
├── App.tsx                       # Root component
└── package.json
```

## Technologies Used

- **React Native 0.82**: Cross-platform mobile framework
- **TypeScript**: Type-safe development
- **react-native-vision-camera**: Camera integration
- **OpenAI SDK**: AI-powered card recognition
- **react-native-fs**: File system operations

## Development

### Linting
```bash
npm run lint
```

### Testing
```bash
npm test
```

## API Costs

This app uses the OpenAI Vision API, which incurs costs per API call. Approximate costs:
- GPT-4 Vision: ~$0.01 per image analysis

Please monitor your usage on the [OpenAI platform](https://platform.openai.com/usage).

## Limitations

- Requires clear visibility of all cards
- Works best with standard playing cards
- Needs good lighting conditions
- Internet connection required for API calls
- API key needed for functionality

## Future Enhancements

- [ ] Offline card recognition using TensorFlow Lite
- [ ] Game history tracking
- [ ] Advanced strategy suggestions
- [ ] Multiple hand support
- [ ] Card counting features
- [ ] Persistent API key storage (encrypted)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Disclaimer

This app is for educational and entertainment purposes only. Please gamble responsibly and follow local laws and regulations.
