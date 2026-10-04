import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';

export default function App() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Football</Text>
      <Text style={styles.subtitle}>Proyecto Expo configurado para EAS</Text>
      <Text style={styles.body}>
        Este proyecto está listo para compilar con EAS Build en iOS y Android.
      </Text>
      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f7fb',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
  },
  title: {
    fontSize: 32,
    fontWeight: '700',
    marginBottom: 12,
    color: '#112233',
  },
  subtitle: {
    fontSize: 18,
    marginBottom: 8,
    color: '#3a4d5d',
  },
  body: {
    fontSize: 14,
    textAlign: 'center',
    color: '#5f6f7d',
  },
});
