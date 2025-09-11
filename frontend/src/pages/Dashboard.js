import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  IconButton,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
} from '@mui/material';
import {
  Assessment,
  Eco,
  TrendingUp,
  Warning,
  Add,
  Refresh,
  ArrowUpward,
  ArrowDownward,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, BarChart, Bar } from 'recharts';
import { useProject } from '../context/ProjectContext';
import { dashboardApi } from '../services/api';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import StatsCard from '../components/Dashboard/StatsCard';
import RecentProjectsList from '../components/Dashboard/RecentProjectsList';
import ImpactChart from '../components/Dashboard/ImpactChart';
import CircularityGauge from '../components/Dashboard/CircularityGauge';
import AIInsights from '../components/Dashboard/AIInsights';

const COLORS = ['#2E7D32', '#FF6F00', '#1976D2', '#D32F2F', '#7B1FA2', '#388E3C'];

function Dashboard() {
  const { projects, loading: projectsLoading } = useProject();
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const data = await dashboardApi.getDashboardStats();
      setDashboardData(data);
    } catch (err) {
      setError('Failed to fetch dashboard data');
      console.error('Dashboard data fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading || projectsLoading) {
    return <LoadingSpinner />;
  }

  const stats = dashboardData || {};
  const recentProjects = projects.slice(0, 5);

  return (
    <Container maxWidth="xl">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          LCA Dashboard
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Monitor your Life Cycle Assessment projects and environmental impact
        </Typography>
      </Box>

      {/* Key Statistics */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title="Total Projects"
            value={stats.total_projects || 0}
            icon={<Assessment />}
            color="primary"
            trend={stats.projects_trend}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title="Completed Assessments"
            value={stats.completed_assessments || 0}
            icon={<Eco />}
            color="success"
            trend={stats.assessments_trend}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title="CO₂ Saved (kg)"
            value={stats.co2_saved || 0}
            icon={<TrendingUp />}
            color="info"
            trend={{ value: 12.5, direction: 'up' }}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatsCard
            title="Circularity Score"
            value={`${Math.round(stats.avg_circularity_score || 0)}%`}
            icon={<Refresh />}
            color="warning"
            trend={stats.circularity_trend}
          />
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Environmental Impact Trends */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3, height: 400 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">Environmental Impact Trends</Typography>
              <IconButton onClick={fetchDashboardData} size="small">
                <Refresh />
              </IconButton>
            </Box>
            <ImpactChart data={stats.impact_trends || []} />
          </Paper>
        </Grid>

        {/* Circularity Gauge */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, height: 400 }}>
            <Typography variant="h6" gutterBottom>
              Overall Circularity
            </Typography>
            <CircularityGauge score={stats.avg_circularity_score || 0} />
            <Box sx={{ mt: 2 }}>
              <Typography variant="body2" color="text.secondary">
                Average across all projects
              </Typography>
              <Chip
                label={stats.avg_circularity_score > 70 ? 'Excellent' : 
                      stats.avg_circularity_score > 50 ? 'Good' : 'Needs Improvement'}
                color={stats.avg_circularity_score > 70 ? 'success' : 
                       stats.avg_circularity_score > 50 ? 'warning' : 'error'}
                size="small"
                sx={{ mt: 1 }}
              />
            </Box>
          </Paper>
        </Grid>

        {/* Recent Projects */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Projects
            </Typography>
            <RecentProjectsList projects={recentProjects} />
          </Paper>
        </Grid>

        {/* AI Insights */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              AI Insights & Recommendations
            </Typography>
            <AIInsights insights={stats.ai_insights || []} />
          </Paper>
        </Grid>

        {/* Impact Category Breakdown */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Impact Categories
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={stats.impact_breakdown || []}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {(stats.impact_breakdown || []).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Material Usage */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Material Usage
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={stats.material_usage || []}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="usage" fill="#2E7D32" />
                <Bar dataKey="recycled" fill="#FF6F00" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Quick Actions
            </Typography>
            <Grid container spacing={2}>
              <Grid item>
                <Card sx={{ minWidth: 200, cursor: 'pointer' }}>
                  <CardContent sx={{ textAlign: 'center' }}>
                    <Add sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                    <Typography variant="h6">New Project</Typography>
                    <Typography variant="body2" color="text.secondary">
                      Start a new LCA project
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item>
                <Card sx={{ minWidth: 200, cursor: 'pointer' }}>
                  <CardContent sx={{ textAlign: 'center' }}>
                    <Assessment sx={{ fontSize: 40, color: 'secondary.main', mb: 1 }} />
                    <Typography variant="h6">Run Analysis</Typography>
                    <Typography variant="body2" color="text.secondary">
                      Analyze existing project
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item>
                <Card sx={{ minWidth: 200, cursor: 'pointer' }}>
                  <CardContent sx={{ textAlign: 'center' }}>
                    <Eco sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
                    <Typography variant="h6">Compare Scenarios</Typography>
                    <Typography variant="body2" color="text.secondary">
                      Compare different scenarios
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
}

export default Dashboard;
