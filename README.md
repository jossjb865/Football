import React, { useMemo, useState } from 'react';
import { StatusBar } from 'expo-status-bar';
import {
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';

const tabs = [
  { key: 'overview', label: 'Overview', icon: '🏠' },
  { key: 'stats', label: 'Stats', icon: '📊' },
  { key: 'teams', label: 'Teams', icon: '👥' },
];

const seasonSummary = [
  { label: 'Matches', value: '240' },
  { label: 'Goals', value: '1.2K' },
  { label: 'Avg. Goals', value: '2.8' },
  { label: 'Active', value: 'Live' },
];

const leaderboard = [
  { name: 'Cristiano', goals: 42, team: 'Real FC' },
  { name: 'Lionel', goals: 39, team: 'Inter City' },
  { name: 'Erling', goals: 38, team: 'Northside' },
  { name: 'Robert', goals: 35, team: 'Riviera' },
];

const standings = [
  { position: 1, team: 'City United', points: 76 },
  { position: 2, team: 'Manchester X', points: 71 },
  { position: 3, team: 'Liverpool FC', points: 68 },
  { position: 4, team: 'Arsenal Pro', points: 64 },
  { position: 5, team: 'White FC', points: 61 },
];

const fixtures = [
  { home: 'City United', away: 'White FC', time: '18:00', day: 'Wed' },
  { home: 'Arsenal Pro', away: 'Liverpool FC', time: '20:30', day: 'Fri' },
  { home: 'Riviera', away: 'Inter City', time: '21:00', day: 'Sat' },
];

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');

  const tabContent = useMemo(() => {
    switch (activeTab) {
      case 'stats':
        return <StatsTab />;
      case 'teams':
        return <TeamsTab />;
      default:
        return <OverviewTab />;
    }
  }, [activeTab]);

  return (
    <View style={styles.container}>
      <StatusBar style="light" backgroundColor="#0b1020" />

      <View style={styles.header}>
        <Text style={styles.brand}>⚽ FOOTBALL</Text>
        <TouchableOpacity style={styles.filterButton} activeOpacity={0.8}>
          <Text style={styles.filterButtonText}>League</Text>
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        <View style={styles.heroCard}>
          <View style={styles.heroTopRow}>
            <Text style={styles.kicker}>Season 2024</Text>
            <Text style={styles.livePill}>LIVE</Text>
          </View>

          <Text style={styles.heroTitle}>Elite League</Text>

          <View style={styles.matchRow}>
            <TeamBadge label="City" icon="🔵" />
            <View style={styles.scoreWrap}>
              <Text style={styles.score}>2 : 1</Text>
              <Text style={styles.subtitle}>Final result</Text>
            </View>
            <TeamBadge label="White" icon="⚪" />
          </View>

          <View style={styles.metaRow}>
            <Text style={styles.metaText}>Stadium: North Arena</Text>
            <Text style={styles.metaText}>58 min</Text>
          </View>
        </View>

        <View style={styles.summaryRow}>
          {seasonSummary.map((item) => (
            <View key={item.label} style={styles.summaryCard}>
              <Text style={styles.summaryLabel}>{item.label}</Text>
              <Text style={styles.summaryValue}>{item.value}</Text>
            </View>
          ))}
        </View>

        {tabContent}
      </ScrollView>

      <View style={styles.tabBar}>
        {tabs.map((tab) => (
          <TouchableOpacity
            key={tab.key}
            style={[styles.tabButton, activeTab === tab.key && styles.tabButtonActive]}
            onPress={() => setActiveTab(tab.key)}
            activeOpacity={0.9}
          >
            <Text style={styles.tabIcon}>{tab.icon}</Text>
            <Text style={[styles.tabLabel, activeTab === tab.key && styles.tabLabelActive]}>
              {tab.label}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );
}

function OverviewTab() {
  return (
    <View style={styles.section}>
      <SectionHeader title="Upcoming Fixtures" />
      {fixtures.map((match, index) => (
        <View key={`${match.home}-${index}`} style={styles.fixtureCard}>
          <Text style={styles.fixtureDay}>{match.day}</Text>
          <View style={styles.fixtureBody}>
            <Text style={styles.fixtureTeam}>{match.home}</Text>
            <Text style={styles.fixtureVS}>vs</Text>
            <Text style={styles.fixtureTeam}>{match.away}</Text>
          </View>
          <Text style={styles.fixtureTime}>{match.time}</Text>
        </View>
      ))}

      <SectionHeader title="Top Picks" />
      <View style={styles.picksCard}>
        <Text style={styles.pickTitle}>Over 2.5 Goals</Text>
        <Text style={styles.pickMeta}>Confidence 81% • Strong trend</Text>
      </View>
    </View>
  );
}

function StatsTab() {
  return (
    <View style={styles.section}>
      <SectionHeader title="Top Scorers" />
      {leaderboard.map((player, index) => (
        <View key={player.name} style={styles.listRow}>
          <Text style={styles.rank}>{index + 1}</Text>
          <View style={styles.nameWrap}>
            <Text style={styles.listName}>{player.name}</Text>
            <Text style={styles.listSub}>{player.team}</Text>
          </View>
          <Text style={styles.goals}>{player.goals}</Text>
        </View>
      ))}
    </View>
  );
}

function TeamsTab() {
  return (
    <View style={styles.section}>
      <SectionHeader title="Standings" />
      {standings.map((row) => (
        <View key={row.team} style={styles.listRow}>
          <Text style={styles.rank}>{row.position}</Text>
          <View style={styles.nameWrap}>
            <Text style={styles.listName}>{row.team}</Text>
          </View>
          <Text style={styles.goals}>{row.points}</Text>
        </View>
      ))}
    </View>
  );
}

function SectionHeader({ title }) {
  return <Text style={styles.sectionTitle}>{title}</Text>;
}

function TeamBadge({ label, icon }) {
  return (
    <View style={styles.teamBadge}>
      <Text style={styles.teamIcon}>{icon}</Text>
      <Text style={styles.teamName}>{label}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0b1020',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingTop: 18,
    paddingBottom: 10,
    backgroundColor: '#111827',
    borderBottomWidth: 1,
    borderBottomColor: '#1f2937',
  },
  brand: {
    color: '#f8fafc',
    fontSize: 18,
    fontWeight: '800',
    letterSpacing: 1.2,
  },
  filterButton: {
    backgroundColor: '#1e293b',
    borderRadius: 999,
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderWidth: 1,
    borderColor: '#334155',
  },
  filterButtonText: {
    color: '#dbeafe',
    fontSize: 12,
    fontWeight: '600',
  },
  content: {
    flex: 1,
    paddingHorizontal: 18,
    paddingTop: 18,
  },
  heroCard: {
    backgroundColor: '#111827',
    borderRadius: 22,
    padding: 18,
    borderWidth: 1,
    borderColor: '#1f2937',
    shadowColor: '#000',
    shadowOpacity: 0.2,
    shadowRadius: 10,
    shadowOffset: { width: 0, height: 6 },
    elevation: 8,
  },
  heroTopRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  kicker: {
    color: '#9ca3af',
    fontSize: 12,
    letterSpacing: 0.8,
    textTransform: 'uppercase',
  },
  livePill: {
    backgroundColor: '#ef4444',
    color: '#fff',
    borderRadius: 999,
    paddingHorizontal: 8,
    paddingVertical: 4,
    fontSize: 10,
    fontWeight: '700',
  },
  heroTitle: {
    color: '#f8fafc',
    fontSize: 28,
    fontWeight: '800',
    marginBottom: 18,
  },
  matchRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  teamBadge: {
    alignItems: 'center',
    flex: 1,
  },
  teamIcon: {
    fontSize: 30,
    marginBottom: 8,
  },
  teamName: {
    color: '#e2e8f0',
    fontSize: 12,
    fontWeight: '600',
  },
  scoreWrap: {
    flex: 1.2,
    alignItems: 'center',
  },
  score: {
    color: '#f8fafc',
    fontSize: 30,
    fontWeight: '800',
  },
  subtitle: {
    color: '#94a3b8',
    fontSize: 12,
    marginTop: 2,
  },
  metaRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 8,
  },
  metaText: {
    color: '#cbd5e1',
    fontSize: 12,
  },
  summaryRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginTop: 18,
    marginBottom: 14,
    gap: 8,
  },
  summaryCard: {
    backgroundColor: '#111827',
    borderRadius: 16,
    paddingHorizontal: 12,
    paddingVertical: 14,
    width: '48%',
    borderWidth: 1,
    borderColor: '#1f2937',
  },
  summaryLabel: {
    color: '#94a3b8',
    fontSize: 11,
    marginBottom: 8,
    textTransform: 'uppercase',
  },
  summaryValue: {
    color: '#f8fafc',
    fontSize: 20,
    fontWeight: '700',
  },
  section: {
    marginTop: 12,
    marginBottom: 18,
  },
  sectionTitle: {
    color: '#f8fafc',
    fontSize: 16,
    fontWeight: '700',
    marginBottom: 12,
  },
  fixtureCard: {
    backgroundColor: '#111827',
    borderRadius: 14,
    padding: 14,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: '#1f2937',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  fixtureDay: {
    color: '#60a5fa',
    fontSize: 12,
    fontWeight: '700',
    width: 36,
  },
  fixtureBody: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    flex: 1,
    gap: 8,
  },
  fixtureTeam: {
    color: '#f8fafc',
    fontSize: 12,
    fontWeight: '600',
  },
  fixtureVS: {
    color: '#94a3b8',
    fontSize: 11,
  },
  fixtureTime: {
    color: '#cbd5e1',
    fontSize: 12,
    fontWeight: '700',
  },
  picksCard: {
    backgroundColor: '#111827',
    borderRadius: 14,
    padding: 16,
    borderWidth: 1,
    borderColor: '#1f2937',
  },
  pickTitle: {
    color: '#f8fafc',
    fontSize: 15,
    fontWeight: '700',
    marginBottom: 4,
  },
  pickMeta: {
    color: '#94a3b8',
    fontSize: 12,
  },
  listRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#111827',
    borderRadius: 12,
    paddingHorizontal: 14,
    paddingVertical: 12,
    marginBottom: 10,
    borderWidth: 1,
    borderColor: '#1f2937',
  },
  rank: {
    width: 28,
    color: '#60a5fa',
    fontSize: 14,
    fontWeight: '700',
  },
  nameWrap: {
    flex: 1,
  },
  listName: {
    color: '#f8fafc',
    fontSize: 14,
    fontWeight: '600',
  },
  listSub: {
    color: '#94a3b8',
    fontSize: 11,
    marginTop: 2,
  },
  goals: {
    color: '#fbbf24',
    fontSize: 14,
    fontWeight: '700',
  },
  tabBar: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    alignItems: 'center',
    backgroundColor: '#111827',
    borderTopWidth: 1,
    borderTopColor: '#1f2937',
    paddingBottom: 18,
    paddingTop: 10,
  },
  tabButton: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 8,
  },
  tabButtonActive: {
    borderTopWidth: 2,
    borderTopColor: '#60a5fa',
  },
  tabIcon: {
    fontSize: 18,
  },
  tabLabel: {
    color: '#94a3b8',
    fontSize: 11,
    marginTop: 4,
    fontWeight: '600',
  },
  tabLabelActive: {
    color: '#f8fafc',
  },
});

export { App };
