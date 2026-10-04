# ⚽ Football App

[![Expo](https://img.shields.io/badge/Expo-51.0.0-000.svg)](https://expo.dev)
[![React Native](https://img.shields.io/badge/React%20Native-0.74-61dafb.svg)](https://reactnative.dev)
[![License](https://img.shields.io/github/license/jossjb865/Football)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/jossjb865/Football?style=social)](https://github.com/jossjb865/Football)

A modern, minimalist football (soccer) statistics and analytics app built with React Native and Expo. Designed for iOS, Android, and Web with a clean, intuitive interface.

## ✨ Features

- 📊 **Real-time Statistics** - Live match data, scores, and player stats
- 🏆 **League Standings** - Current season rankings and points
- 🥅 **Top Scorers** - Leaderboard of goal-scoring leaders
- 🎯 **Assists Tracking** - Monitor assists leaders
- 📱 **Multi-platform** - iOS, Android, and Web support
- 🎨 **Minimalist Design** - Clean, modern UI with focus on readability
- ⚡ **Fast & Responsive** - Optimized performance across all platforms

## 🚀 Quick Start

### Prerequisites

- Node.js >= 18.x
- npm or yarn
- Expo CLI (optional, included via npm)

### Installation

```bash
# Clone the repository
git clone https://github.com/jossjb865/Football.git
cd Football

# Install dependencies
npm install

# Create environment file
cp .env.example .env
```

### Development

```bash
# Start Expo development server
npm start

# For iOS (macOS only)
npm run ios

# For Android
npm run android

# For Web
npm run web
```

## 📱 Platform-Specific

### iOS

```bash
expo run:ios
# or
npm run ios
```

### Android

```bash
expo run:android
# or
npm run android
```

### Web

```bash
expo start --web
# or
npm run web
```

## 🏗️ Building for Production

### Using EAS Build

```bash
# Install EAS CLI
npm install -g eas-cli

# Login to Expo/EAS
npx eas login

# Configure EAS for your project
npx eas build:configure

# Build for all platforms
npm run eas-build

# Or build for specific platform
npm run eas-build-android
npm run eas-build-ios
```

#### Build Profiles

- **development** - For testing with development client
- **preview** - For staging/preview builds
- **production** - For App Store and Google Play distribution

## 📁 Project Structure

```
Football/
├── App.js              # Main app component with tab navigation
├── index.js            # App entry point
├── app.json            # Expo configuration
├── eas.json            # EAS build configuration
├── babel.config.js     # Babel configuration
├── package.json        # Dependencies and scripts
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
├── EAS_SETUP.md        # EAS build documentation
└── README.md           # This file
```

## 🎨 Design System

Minimalist dark theme with carefully selected colors:

- **Background**: `#0f172a` (Slate 950)
- **Surface**: `#1e293b` (Slate 800)
- **Primary**: `#3b82f6` (Blue 500)
- **Accent**: `#ec4899` (Pink 500)
- **Text**: `#f1f5f9` (Slate 100)
- **Secondary Text**: `#cbd5e1` (Slate 300)

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
EXPO_PUBLIC_API_URL=https://api.example.com
EXPO_PUBLIC_APP_ENV=development
EXPO_PUBLIC_LEAGUE_ID=1
EXPO_PUBLIC_SEASON=2024
```

Access in your app:

```js
const apiUrl = process.env.EXPO_PUBLIC_API_URL;
```

## 📦 Scripts

```bash
# Development
npm start              # Start Expo dev server
npm run ios            # Run on iOS simulator
npm run android        # Run on Android emulator
npm run web            # Run on web

# Production & Building
npm run eas-build      # Build for iOS and Android
npm run eas-build-ios  # Build for iOS only
npm run eas-build-android  # Build for Android only
```

## 🧪 Testing

To run the app in Expo Go (development):

```bash
npm start

# Then scan QR code with Expo Go app
```

## 🌐 Deployment

### Ideavo Integration

This project is ready for deployment via [Ideavo.ai](https://ideavo.ai):

1. Connect your GitHub repository
2. Ideavo will auto-detect the Expo configuration
3. Configure build settings and deploy
4. Access your app via Ideavo's hosting

### App Store & Google Play

```bash
# Build production binaries
npm run eas-build -- --profile production

# Submit to stores (requires additional setup)
eas submit --platform ios
eas submit --platform android
```

## 🛠️ Troubleshooting

### Port Already in Use

```bash
expo start --clear
```

### Module Not Found

```bash
rm -rf node_modules package-lock.json
npm install
```

### Build Issues

See [EAS_SETUP.md](EAS_SETUP.md) for detailed EAS troubleshooting.

## 📚 Dependencies

- **expo** ~51.0.0 - Framework for building native apps
- **react** 18.2.0 - UI library
- **react-native** 0.74.5 - Native mobile development
- **expo-status-bar** ~1.12.1 - Status bar API

## 📝 Development Guidelines

1. Use functional components with React hooks
2. Keep components focused and reusable
3. Follow minimalist design principles
4. Test on multiple platforms (iOS, Android, Web)
5. Keep bundle size optimized

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feat/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 📞 Support

- 📧 Email: support@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/jossjb865/Football/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/jossjb865/Football/discussions)

## 🔗 Resources

- [Expo Documentation](https://docs.expo.dev)
- [React Native Docs](https://reactnative.dev)
- [EAS Build Guide](https://docs.expo.dev/build/setup/)
- [Ideavo.ai](https://ideavo.ai)

---

**Built with ❤️ using Expo and React Native**

⭐ If you find this project useful, please consider giving it a star!
