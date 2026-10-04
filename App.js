import React, { useState } from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, Image } from 'react-native';

const COLORS = {
  background: '#0f172a',
  surface: '#1e293b',
  primary: '#3b82f6',
  primaryHover: '#2563eb',
  text: '#f1f5f9',
  textSecondary: '#cbd5e1',
  border: '#334155',
  accent: '#ec4899',
};

export default function App() {
  const [activeTab, setActiveTab] = useState('home');

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={COLORS.background} />
      
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.headerContent}>
          <Text style={styles.logo}>⚽</Text>
          <Text style={styles.headerTitle}>Football</Text>
        </View>
      </View>

      {/* Main Content */}
      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        {activeTab === 'home' && <HomeTab />}
        {activeTab === 'stats' && <StatsTab />}
        {activeTab === 'teams' && <TeamsTab />}
      </ScrollView>

      {/* Bottom Navigation */}
      <View style={styles.bottomNav}>
        <NavButton 
          icon="🏠" 
          label="Home" 
          active={activeTab === 'home'}
          onPress={() => setActiveTab('home')}
        />
        <NavButton 
          icon="📊" 
          label="Stats" 
          active={activeTab === 'stats'}
          onPress={() => setActiveTab('stats')}
        />
        <NavButton 
          icon="👥" 
          label="Teams" 
          active={activeTab === 'teams'}
          onPress={() => setActiveTab('teams')}
        />
      </View>

      <StatusBar style="light" />
    </View>
  );
}

function NavButton({ icon, label, active, onPress }) {
  return (
    <TouchableOpacity 
      style={[styles.navButton, active && styles.navButtonActive]}
      onPress={onPress}
      activeOpacity={0.7}
    >
      <Text style={styles.navIcon}>{icon}</Text>
      <Text style={[styles.navLabel, active && styles.navLabelActive]}>{label}</Text>
    </TouchableOpacity>
  );
}

function HomeTab() {
  return (
    <View style={styles.tab}>
      {/* Featured Match */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Next Match</Text>
        <View style={styles.matchCard}>
          <View style={styles.team}>
            <Text style={styles.teamLogo}>🔵</Text>
            <Text style={styles.teamName}>City United</Text>
          </View>
          <View style={styles.vs}>
            <Text style={styles.vsText}>vs</Text>
            <Text style={styles.date}>Dec 15</Text>
          </View>
          <View style={styles.team}>
            <Text style={styles.teamLogo}>⚪</Text>
            <Text style={styles.teamName}>White FC</Text>
          </View>
        </View>
      </View>

      {/* Quick Stats */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Season Overview</Text>
        <View style={styles.statsGrid}>
          <StatItem label="Matches" value="240" />
          <StatItem label="Goals" value="1.2K" />
          <StatItem label="Teams" value="20" />
          <StatItem label="Active" value="Yes" />
        </View>
      </View>

      {/* Recent News */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Latest Updates</Text>
        <View style={styles.newsItem}>
          <View style={styles.newsBullet} />
          <Text style={styles.newsText}>New season statistics available</Text>
        </View>
        <View style={styles.newsItem}>
          <View style={styles.newsBullet} />
          <Text style={styles.newsText}>Top scorers leaderboard updated</Text>
        </View>
        <View style={styles.newsItem}>
          <View style={styles.newsBullet} />
          <Text style={styles.newsText}>Team rankings refreshed</Text>
        </View>
      </View>
    </View>
  );
}

function StatsTab() {
  return (
    <View style={styles.tab}>
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Top Scorers</Text>
        <LeaderboardItem rank="1" player="Cristiano" goals="42" />
        <LeaderboardItem rank="2" player="Lionel" goals="39" />
        <LeaderboardItem rank="3" player="Erling" goals="38" />
        <LeaderboardItem rank="4" player="Robert" goals="35" />
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Assists Leaders</Text>
        <LeaderboardItem rank="1" player="Kevin" assists="15" />
        <LeaderboardItem rank="2" player="Bruno" assists="13" />
        <LeaderboardItem rank="3" player="Vinícius" assists="12" />
      </View>
    </View>
  );
}

function TeamsTab() {
  return (
    <View style={styles.tab}>
      <View style={styles.card}>
        <Text style={styles.cardTitle}>League Standings</Text>
        <TableRow position="1" team="City United" points="76" />
        <TableRow position="2" team="Manchester X" points="71" />
        <TableRow position="3" team="Liverpool FC" points="68" />
        <TableRow position="4" team="Arsenal Pro" points="64" />
        <TableRow position="5" team="White FC" points="61" />
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Quick Actions</Text>
        <ActionButton label="View Full Table" />
        <ActionButton label="Team Details" />
        <ActionButton label="Match History" />
      </View>
    </View>
  );
}

function StatItem({ label, value }) {
  return (
    <View style={styles.statItem}>
      <Text style={styles.statValue}>{value}</Text>
      <Text style={styles.statLabel}>{label}</Text>
    </View>
  );
}

function LeaderboardItem({ rank, player, goals, assists }) {
  return (
    <View style={styles.leaderboardItem}>
      <Text style={styles.rank}>{rank}</Text>
      <Text style={styles.playerName}>{player}</Text>
      <Text style={styles.stat}>{goals || assists}</Text>
    </View>
  );
}

function TableRow({ position, team, points }) {
  return (
    <View style={styles.tableRow}>
      <Text style={styles.tablePos}>{position}</Text>
      <Text style={styles.tableTeam}>{team}</Text>
      <Text style={styles.tablePoints}>{points}</Text>
    </View>
  );
}

function ActionButton({ label }) {
  return (
    <TouchableOpacity style={styles.actionButton} activeOpacity={0.7}>
      <Text style={styles.actionButtonText}>{label}</Text>
      <Text style={styles.actionArrow}>→</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    backgroundColor: COLORS.surface,
    paddingTop: 12,
    paddingBottom: 16,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  headerContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
  },
  logo: {
    fontSize: 28,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: '700',
    color: COLORS.text,
    letterSpacing: 1,
  },
  content: {
    flex: 1,
    padding: 16,
  },
  tab: {
    gap: 16,
    paddingBottom: 80,
  },
  card: {
    backgroundColor: COLORS.surface,
    borderRadius: 12,
    padding: 16,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.text,
    marginBottom: 16,
  },
  matchCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: COLORS.background,
    borderRadius: 8,
    padding: 16,
  },
  team: {
    alignItems: 'center',
    flex: 1,
  },
  teamLogo: {
    fontSize: 32,
    marginBottom: 8,
  },
  teamName: {
    fontSize: 12,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  vs: {
    alignItems: 'center',
    marginHorizontal: 16,
  },
  vsText: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.textSecondary,
  },
  date: {
    fontSize: 11,
    color: COLORS.primary,
    marginTop: 4,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  statItem: {
    flex: 1,
    minWidth: '45%',
    backgroundColor: COLORS.background,
    borderRadius: 8,
    padding: 12,
    alignItems: 'center',
  },
  statValue: {
    fontSize: 20,
    fontWeight: '700',
    color: COLORS.primary,
  },
  statLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
    marginTop: 4,
  },
  newsItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
    gap: 12,
  },
  newsBullet: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: COLORS.primary,
  },
  newsText: {
    fontSize: 14,
    color: COLORS.textSecondary,
    flex: 1,
  },
  leaderboardItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
    gap: 12,
  },
  rank: {
    width: 30,
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.primary,
  },
  playerName: {
    flex: 1,
    fontSize: 14,
    color: COLORS.text,
  },
  stat: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.accent,
    minWidth: 40,
    textAlign: 'right',
  },
  tableRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
    gap: 12,
  },
  tablePos: {
    width: 30,
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.primary,
  },
  tableTeam: {
    flex: 1,
    fontSize: 14,
    color: COLORS.text,
  },
  tablePoints: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.accent,
    minWidth: 40,
    textAlign: 'right',
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: COLORS.background,
    borderRadius: 8,
    paddingVertical: 12,
    paddingHorizontal: 14,
    marginBottom: 8,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  actionButtonText: {
    fontSize: 14,
    color: COLORS.text,
    fontWeight: '500',
  },
  actionArrow: {
    fontSize: 14,
    color: COLORS.primary,
  },
  bottomNav: {
    flexDirection: 'row',
    backgroundColor: COLORS.surface,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
    paddingBottom: 12,
    paddingTop: 8,
    justifyContent: 'space-around',
  },
  navButton: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 8,
    flex: 1,
  },
  navButtonActive: {
    borderTopWidth: 2,
    borderTopColor: COLORS.primary,
  },
  navIcon: {
    fontSize: 24,
    marginBottom: 4,
  },
  navLabel: {
    fontSize: 11,
    color: COLORS.textSecondary,
    fontWeight: '500',
  },
  navLabelActive: {
    color: COLORS.primary,
  },
});
