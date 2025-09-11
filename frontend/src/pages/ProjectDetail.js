import React from 'react';
import { Box, Typography, Card, CardContent, Grid } from '@mui/material';
import { useParams } from 'react-router-dom';

const ProjectDetail = () => {
  const { id } = useParams();

  return (
    <Box sx={{ mt: 2 }}>
      <Typography variant="h4" sx={{ fontWeight: 700, color: '#1a202c', mb: 4 }}>
        Project Details - ID: {id}
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card sx={{ border: '1px solid #e2e8f0', borderRadius: 3 }}>
            <CardContent sx={{ p: 3 }}>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                Project Information
              </Typography>
              <Typography variant="body1" color="text.secondary">
                Detailed project view will be implemented here with comprehensive LCA data, calculations, and visualizations.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default ProjectDetail;
