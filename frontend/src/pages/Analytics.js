import React from 'react';
import { Box, Typography, Card, CardContent, Grid } from '@mui/material';

const Analytics = () => {
  return (
    <Box sx={{ mt: 2 }}>
      <Typography variant="h4" sx={{ fontWeight: 700, color: '#1a202c', mb: 4 }}>
        Analytics Dashboard
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card sx={{ border: '1px solid #e2e8f0', borderRadius: 3 }}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                Advanced Analytics & Insights
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Coming soon: Advanced analytics including impact benchmarking, trend analysis, and AI-powered insights for your LCA projects.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Analytics;
