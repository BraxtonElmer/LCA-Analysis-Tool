import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Grid,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Chip,
  Avatar,
  LinearProgress,
  Menu,
  MenuItem,
} from '@mui/material';
import {
  Add,
  FilterList,
  Search,
  MoreVert,
  Assignment,
  TrendingUp,
  Schedule,
  CheckCircle,
} from '@mui/icons-material';

const Projects = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterAnchor, setFilterAnchor] = useState(null);
  const [statusFilter, setStatusFilter] = useState('all');
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [newProject, setNewProject] = useState({
    name: '',
    description: '',
    functionalUnit: '',
    systemBoundary: '',
  });

  const projects = [
    {
      id: 1,
      name: 'Steel Production LCA',
      description: 'Comprehensive life cycle assessment for integrated steel production facility including raw material extraction, processing, and manufacturing phases.',
      status: 'Active',
      progress: 75,
      functionalUnit: '1 ton of steel',
      systemBoundary: 'Cradle-to-gate',
      lastUpdate: '2 hours ago',
      carbonFootprint: 1850,
      owner: 'John Smith',
      createdAt: '2024-01-15',
    },
    {
      id: 2,
      name: 'Aluminum Recycling Process',
      description: 'Environmental impact assessment of aluminum recycling operations with focus on energy efficiency and waste reduction.',
      status: 'Completed',
      progress: 100,
      functionalUnit: '1 kg of recycled aluminum',
      systemBoundary: 'Gate-to-gate',
      lastUpdate: '1 day ago',
      carbonFootprint: 890,
      owner: 'Sarah Johnson',
      createdAt: '2023-12-08',
    },
    {
      id: 3,
      name: 'Copper Mining Assessment',
      description: 'Life cycle impact assessment of copper mining operations including extraction, beneficiation, and transportation.',
      status: 'Active',
      progress: 45,
      functionalUnit: '1 ton of copper concentrate',
      systemBoundary: 'Cradle-to-gate',
      lastUpdate: '5 hours ago',
      carbonFootprint: 2100,
      owner: 'Mike Chen',
      createdAt: '2024-02-01',
    },
    {
      id: 4,
      name: 'Iron Ore Processing',
      description: 'Environmental assessment of iron ore beneficiation processes with emphasis on water usage and air emissions.',
      status: 'Planning',
      progress: 15,
      functionalUnit: '1 ton of iron ore pellets',
      systemBoundary: 'Gate-to-gate',
      lastUpdate: '1 week ago',
      carbonFootprint: 0,
      owner: 'Lisa Zhang',
      createdAt: '2024-03-10',
    },
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'Active': return '#10b981';
      case 'Completed': return '#3b82f6';
      case 'Planning': return '#f59e0b';
      default: return '#6b7280';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'Active': return <TrendingUp />;
      case 'Completed': return <CheckCircle />;
      case 'Planning': return <Schedule />;
      default: return <Assignment />;
    }
  };

  const handleCreateProject = () => {
    // Handle project creation
    console.log('Creating project:', newProject);
    setCreateDialogOpen(false);
    setNewProject({ name: '', description: '', functionalUnit: '', systemBoundary: '' });
  };

  const filteredProjects = projects.filter(project => {
    const matchesSearch = project.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         project.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || project.status.toLowerCase() === statusFilter.toLowerCase();
    return matchesSearch && matchesStatus;
  });

  return (
    <Box sx={{ mt: 2 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 700, color: '#1a202c', mb: 1 }}>
            LCA Projects
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Manage and monitor your life cycle assessment projects
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => setCreateDialogOpen(true)}
          sx={{
            bgcolor: '#3b82f6',
            borderRadius: 2,
            px: 3,
            py: 1.5,
            textTransform: 'none',
            fontWeight: 600,
          }}
        >
          New Project
        </Button>
      </Box>

      {/* Search and Filters */}
      <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
        <TextField
          placeholder="Search projects..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          InputProps={{
            startAdornment: <Search sx={{ color: '#64748b', mr: 1 }} />,
          }}
          sx={{
            flexGrow: 1,
            '& .MuiOutlinedInput-root': {
              borderRadius: 2,
            },
          }}
        />
        <Button
          variant="outlined"
          startIcon={<FilterList />}
          onClick={(e) => setFilterAnchor(e.currentTarget)}
          sx={{
            borderRadius: 2,
            textTransform: 'none',
            fontWeight: 600,
          }}
        >
          Filter
        </Button>
      </Box>

      {/* Filter Menu */}
      <Menu
        anchorEl={filterAnchor}
        open={Boolean(filterAnchor)}
        onClose={() => setFilterAnchor(null)}
      >
        <MenuItem onClick={() => { setStatusFilter('all'); setFilterAnchor(null); }}>
          All Projects
        </MenuItem>
        <MenuItem onClick={() => { setStatusFilter('active'); setFilterAnchor(null); }}>
          Active Only
        </MenuItem>
        <MenuItem onClick={() => { setStatusFilter('completed'); setFilterAnchor(null); }}>
          Completed Only
        </MenuItem>
        <MenuItem onClick={() => { setStatusFilter('planning'); setFilterAnchor(null); }}>
          Planning Only
        </MenuItem>
      </Menu>

      {/* Projects Grid */}
      <Grid container spacing={3}>
        {filteredProjects.map((project) => (
          <Grid item xs={12} md={6} lg={4} key={project.id}>
            <Card
              sx={{
                border: '1px solid #e2e8f0',
                borderRadius: 3,
                height: '100%',
                transition: 'all 0.2s ease-in-out',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: '0 8px 25px rgba(0,0,0,0.15)',
                },
              }}
            >
              <CardContent sx={{ p: 3 }}>
                {/* Header */}
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                  <Avatar
                    sx={{
                      bgcolor: getStatusColor(project.status),
                      width: 48,
                      height: 48,
                    }}
                  >
                    {getStatusIcon(project.status)}
                  </Avatar>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Chip
                      label={project.status}
                      size="small"
                      sx={{
                        bgcolor: `${getStatusColor(project.status)}20`,
                        color: getStatusColor(project.status),
                        fontWeight: 500,
                      }}
                    />
                    <IconButton size="small">
                      <MoreVert />
                    </IconButton>
                  </Box>
                </Box>

                {/* Project Info */}
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 1 }}>
                  {project.name}
                </Typography>
                <Typography
                  variant="body2"
                  color="text.secondary"
                  sx={{ mb: 2, lineHeight: 1.5, display: '-webkit-box', overflow: 'hidden', WebkitBoxOrient: 'vertical', WebkitLineClamp: 3 }}
                >
                  {project.description}
                </Typography>

                {/* Functional Unit */}
                <Box sx={{ mb: 2 }}>
                  <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 0.5 }}>
                    Functional Unit
                  </Typography>
                  <Typography variant="body2" sx={{ fontWeight: 500 }}>
                    {project.functionalUnit}
                  </Typography>
                </Box>

                {/* Progress */}
                <Box sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography variant="body2" sx={{ fontWeight: 500 }}>
                      Progress
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {project.progress}%
                    </Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={project.progress}
                    sx={{
                      height: 8,
                      borderRadius: 4,
                      backgroundColor: '#f1f5f9',
                      '& .MuiLinearProgress-bar': {
                        backgroundColor: getStatusColor(project.status),
                        borderRadius: 4,
                      },
                    }}
                  />
                </Box>

                {/* Metrics */}
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                  <Box>
                    <Typography variant="caption" color="text.secondary" sx={{ display: 'block' }}>
                      Carbon Footprint
                    </Typography>
                    <Typography variant="body2" sx={{ fontWeight: 600, color: '#ef4444' }}>
                      {project.carbonFootprint} kg CO₂
                    </Typography>
                  </Box>
                  <Box sx={{ textAlign: 'right' }}>
                    <Typography variant="caption" color="text.secondary" sx={{ display: 'block' }}>
                      Created
                    </Typography>
                    <Typography variant="body2" sx={{ fontWeight: 500 }}>
                      {new Date(project.createdAt).toLocaleDateString()}
                    </Typography>
                  </Box>
                </Box>

                {/* Footer */}
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', pt: 1, borderTop: '1px solid #e2e8f0' }}>
                  <Typography variant="caption" color="text.secondary">
                    by {project.owner}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {project.lastUpdate}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Create Project Dialog */}
      <Dialog
        open={createDialogOpen}
        onClose={() => setCreateDialogOpen(false)}
        maxWidth="sm"
        fullWidth
        PaperProps={{
          sx: { borderRadius: 3 }
        }}
      >
        <DialogTitle sx={{ pb: 1 }}>
          <Typography variant="h5" sx={{ fontWeight: 600 }}>
            Create New LCA Project
          </Typography>
        </DialogTitle>
        <DialogContent sx={{ pt: 2 }}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                label="Project Name"
                fullWidth
                value={newProject.name}
                onChange={(e) => setNewProject({ ...newProject, name: e.target.value })}
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 2 } }}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Description"
                fullWidth
                multiline
                rows={3}
                value={newProject.description}
                onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 2 } }}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="Functional Unit"
                fullWidth
                placeholder="e.g., 1 kg of product"
                value={newProject.functionalUnit}
                onChange={(e) => setNewProject({ ...newProject, functionalUnit: e.target.value })}
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 2 } }}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                label="System Boundary"
                fullWidth
                placeholder="e.g., Cradle-to-gate"
                value={newProject.systemBoundary}
                onChange={(e) => setNewProject({ ...newProject, systemBoundary: e.target.value })}
                sx={{ '& .MuiOutlinedInput-root': { borderRadius: 2 } }}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions sx={{ p: 3, pt: 2 }}>
          <Button
            onClick={() => setCreateDialogOpen(false)}
            sx={{ textTransform: 'none' }}
          >
            Cancel
          </Button>
          <Button
            variant="contained"
            onClick={handleCreateProject}
            sx={{
              bgcolor: '#3b82f6',
              textTransform: 'none',
              fontWeight: 600,
              borderRadius: 2,
            }}
          >
            Create Project
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Projects;
