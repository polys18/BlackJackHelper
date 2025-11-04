# BlackJack Helper - Usage Guide

## Quick Start

1. **Install the app** on your iOS or Android device (see README.md for installation instructions)
2. **Launch the app**
3. **Set your OpenAI API key** by tapping the "⚙️ Set API Key" button
4. **Start scanning cards!**

## Taking a Photo

### Best Practices for Card Recognition

To get the best results when scanning cards:

1. **Good Lighting**: Ensure the cards are well-lit with minimal shadows
2. **Clear View**: All cards should be fully visible and not overlapping
3. **Stable Shot**: Hold your phone steady when taking the photo
4. **Proper Distance**: Position your phone 12-18 inches above the table
5. **Flat Surface**: Cards should be on a flat surface, not at an angle

### Card Layout

The app expects cards to be arranged as follows:
- **Dealer's cards**: Should be at the TOP of the image
- **Player's cards**: Should be at the BOTTOM of the image (closest to you)

Example layout:
```
┌─────────────────────┐
│  Dealer's Cards     │  ← Top of image
│      K♠  A♥         │
│                     │
│                     │
│      7♣  9♦         │  ← Bottom of image
│   Player's Cards    │
└─────────────────────┘
```

## Understanding the Results

### Card Display

After analysis, you'll see:
- Each detected card with its rank and suit (e.g., A♥, K♠, 7♣)
- Total hand value for both player and dealer
- Special indicators:
  - **Green text (21)**: Blackjack! 🎉
  - **Red text (>21)**: Bust! 💥

### Strategy Recommendations

The app provides basic strategy recommendations based on:
- Your current hand value
- The dealer's up card
- Probability of busting

Common recommendations:
- **HIT**: Take another card
- **STAND**: Keep your current hand
- **Specific reasoning**: Why the recommendation is given

## Game Features

### Hand Value Calculation

The app automatically:
- Calculates the total value of your hand
- Handles Aces correctly (1 or 11)
- Identifies Blackjack (21 with 2 cards)
- Detects bust (over 21)

### Ace Handling

Aces are automatically adjusted:
- Counted as 11 when it won't bust
- Counted as 1 when 11 would bust
- Multiple Aces are handled correctly

Example:
- A♥ + 9♦ = 20 (Ace as 11)
- A♥ + 9♦ + 5♣ = 15 (Ace as 1)

## Tips for Success

1. **Clear API Key**: Make sure your OpenAI API key is valid and has sufficient credits
2. **Internet Connection**: Ensure you have a stable internet connection
3. **Card Visibility**: Make sure all cards are clearly visible in frame
4. **Retry if Needed**: If recognition fails, try taking another photo with better lighting
5. **Card Position**: Follow the layout guidelines (dealer top, player bottom)

## Troubleshooting

### "No Cards Detected"

If the app can't detect cards:
1. Improve lighting conditions
2. Ensure cards are not overlapping
3. Try moving closer or further from the cards
4. Make sure cards are right-side-up
5. Clean the camera lens

### "API Key Required"

If you see this error:
1. Tap "⚙️ Set API Key"
2. Enter your OpenAI API key
3. Tap "Set Key"
4. Try scanning again

### "Analysis Failed"

If analysis fails:
1. Check your internet connection
2. Verify your API key is correct
3. Ensure you have API credits remaining
4. Try again with a clearer photo

## API Usage and Costs

Each photo you analyze:
- Uses the OpenAI GPT-4 Vision API
- Costs approximately $0.01 per request
- Requires an active internet connection

**Cost Saving Tips:**
- Only scan when you need strategy advice
- Take clear photos to avoid retries
- Monitor your usage on [OpenAI's platform](https://platform.openai.com/usage)

## Privacy and Security

- Your API key is stored in memory only
- Card images are sent to OpenAI for analysis
- No game data is stored permanently
- Images are not saved by default

## Known Limitations

1. **Card Types**: Works best with standard playing cards
2. **Lighting**: Poor lighting reduces accuracy
3. **Overlapping**: Overlapping cards may not be detected
4. **Special Cards**: Jokers and non-standard cards may confuse the AI
5. **Multiple Hands**: Currently supports one player hand at a time

## Advanced Features

### Understanding Confidence Scores

The AI provides a confidence score (0-1) indicating how certain it is about the card detection. Higher scores mean better recognition.

### Strategy Basics

The recommendations follow basic blackjack strategy:
- **Hard hands** (no Ace or Ace as 1)
- **Dealer weak cards** (2-6)
- **Dealer strong cards** (7-Ace)

## Need Help?

If you encounter issues:
1. Check this guide for troubleshooting steps
2. Verify your setup matches the prerequisites
3. Review the README.md for installation issues
4. Check the OpenAI API status page
5. Open an issue on GitHub

## Next Steps

Once you're comfortable with the basic features:
- Experiment with different lighting conditions
- Try different card layouts
- Use the strategy recommendations to improve your game
- Share feedback for future improvements!

---

**Remember**: This app is for educational and entertainment purposes. Always gamble responsibly!
