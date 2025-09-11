import React, { useState } from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Box,
  Typography,
  Divider,
  Collapse,
  Avatar,
  Chip,
  useTheme,
  alpha,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Assignment as ProjectsIcon,
  Analytics as AnalyticsIcon,
  Inventory as MaterialsIcon,
  Precision as ProcessesIcon,
  Assessment as ReportsIcon,
  Settings as SettingsIcon,
  ExpandLess,
  ExpandMore,
  Eco,
  Science,
  TrendingUp,
  Business,
  AutoAwesome,
  Recycling,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const drawerWidth = 280;

const menuItems = [
  {
    text: 'Dashboard',
    icon: <DashboardIcon />,
    path: '/',
    color: '#3b82f6',
  },
  {
    text: 'Projects',
    icon: <ProjectsIcon />,
    path: '/projects',
    color: '#10b981',
    subItems: [
      { text: 'All Projects', path: '/projects' },
      { text: 'Active Projects', path: '/projects/active' },
      { text: 'Completed', path: '/projects/completed' },
    ],
  },
  {
    text: 'Analytics',
    icon: <AnalyticsIcon />,
    path: '/analytics',
    color: '#8b5cf6',
    subItems: [
      { text: 'Impact Analysis', path: '/analytics/impact' },
      { text: 'Benchmarking', path: '/analytics/benchmark' },
      { text: 'Trends', path: '/analytics/trends' },
    ],
  },
  {
    text: 'Materials',
    icon: <MaterialsIcon />,
    path: '/materials',
    color: '#f59e0b',
  },
  {
    text: 'Processes',
    icon: <ProcessesIcon />,
    path: '/processes',
    color: '#ef4444',
  },
  {
    text: 'Reports',
    icon: <ReportsIcon />,
    path: '/reports',
    color: '#06b6d4',
  },
  {
    text: 'Settings',
    icon: <SettingsIcon />,
    path: '/settings',
    color: '#6b7280',
  },
];

const quickActions = [
  { text: 'AI Insights', icon: <AutoAwesome />, color: '#f97316' },
  { text: 'Circularity', icon: <Recycling />, color: '#22c55e' },
  { text: 'Sustainability', icon: <Eco />, color: '#16a34a' },
];

const Sidebar = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const [expandedItems, setExpandedItems] = useState({});

  const handleExpandClick = (itemText) => {
    setExpandedItems(prev => ({
      ...prev,
      [itemText]: !prev[itemText],
    }));
  };

  const handleNavigate = (path) => {
    navigate(path);
  };

  const isActive = (path) => {
    return location.pathname === path || location.pathname.startsWith(path + '/');
  };

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: drawerWidth,
          boxSizing: 'border-box',
          background: 'linear-gradient(180deg, #ffffff 0%, #f8fafc 100%)',
          borderRight: '1px solid #e2e8f0',
          boxShadow: '2px 0 8px rgba(0,0,0,0.05)',
        },
      }}
    >
      {/* Header */}
      <Box sx={{ p: 3, borderBottom: '1px solid #e2e8f0' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <Box
            sx={{
              width: 40,
              height: 40,
              borderRadius: '12px',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
            }}
          >
            <Science />
          </Box>
          <Box>
            <Typography variant="h6" sx={{ fontWeight: 700, color: '#1a202c' }}>
              LCA Pro
            </Typography>
            <Typography variant="body2" sx={{ color: '#64748b', fontSize: '0.75rem' }}>
              Analytics Suite
            </Typography>
          </Box>
        </Box>
        
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mt: 2 }}>
          <Avatar sx={{ width: 32, height: 32, bgcolor: '#3b82f6' }}>A</Avatar>
          <Box sx={{ flex: 1 }}>
            <Typography variant="body2" sx={{ fontWeight: 600, color: '#1a202c' }}>
              Admin User
            </Typography>
            <Typography variant="caption" sx={{ color: '#64748b' }}>
              Project Manager
            </Typography>
          </Box>
          <Chip
            label="Pro"
            size="small"
            sx={{
              height: 20,
              fontSize: '0.65rem',
              fontWeight: 600,
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
            }}
          />
        </Box>
      </Box>

      {/* Navigation Menu */}
      <Box sx={{ flexGrow: 1, overflow: 'auto', py: 2 }}>
        <List sx={{ px: 2 }}>
          {menuItems.map((item) => (
            <Box key={item.text} sx={{ mb: 0.5 }}>
              <ListItem disablePadding>
                <ListItemButton
                  onClick={() => item.subItems ? handleExpandClick(item.text) : handleNavigate(item.path)}
                  sx={{
                    borderRadius: '12px',
                    mb: 0.5,
                    minHeight: 48,
                    bgcolor: isActive(item.path) ? alpha(item.color, 0.12) : 'transparent',
                    color: isActive(item.path) ? item.color : '#64748b',
                    fontWeight: isActive(item.path) ? 600 : 400,
                    '&:hover': {
                      bgcolor: alpha(item.color, 0.08),
                      color: item.color,
                    },
                    transition: 'all 0.2s ease-in-out',
                  }}
                >
                  <ListItemIcon sx={{ 
                    color: 'inherit', 
                    minWidth: 40,
                    '& .MuiSvgIcon-root': { fontSize: '1.25rem' }
                  }}>
                    {item.icon}
                  </ListItemIcon>
                  <ListItemText 
                    primary={item.text}
                    primaryTypographyProps={{
                      fontSize: '0.875rem',
                      fontWeight: 'inherit',
                    }}
                  />
                  {item.subItems && (
                    expandedItems[item.text] ? <ExpandLess /> : <ExpandMore />
                  )}
                </ListItemButton>
              </ListItem>
              
              {item.subItems && (
                <Collapse in={expandedItems[item.text]} timeout="auto" unmountOnExit>
                  <List component="div" disablePadding sx={{ pl: 2 }}>
                    {item.subItems.map((subItem) => (
                      <ListItemButton
                        key={subItem.text}
                        onClick={() => handleNavigate(subItem.path)}
                        sx={{
                          borderRadius: '8px',
                          minHeight: 36,
                          mb: 0.25,
                          bgcolor: isActive(subItem.path) ? alpha(item.color, 0.08) : 'transparent',
                          color: isActive(subItem.path) ? item.color : '#64748b',
                          pl: 3,
                          '&:hover': {
                            bgcolor: alpha(item.color, 0.06),
                            color: item.color,
                          },
                        }}
                      >
                        <ListItemText
                          primary={subItem.text}
                          primaryTypographyProps={{
                            fontSize: '0.8125rem',
                          }}
                        />
                      </ListItemButton>
                    ))}
                  </List>
                </Collapse>
              )}
            </Box>
          ))}
        </List>

        <Divider sx={{ my: 2, mx: 2 }} />

        {/* Quick Actions */}
        <Box sx={{ px: 2 }}>
          <Typography
            variant="overline"
            sx={{
              color: '#64748b',
              fontWeight: 600,
              fontSize: '0.75rem',
              letterSpacing: 1,
              px: 1,
            }}
          >
            Quick Actions
          </Typography>
          <List sx={{ mt: 1 }}>
            {quickActions.map((action) => (
              <ListItemButton
                key={action.text}
                sx={{
                  borderRadius: '8px',
                  minHeight: 40,
                  mb: 0.25,
                  '&:hover': {
                    bgcolor: alpha(action.color, 0.08),
                    color: action.color,
                  },
                }}
              >
                <ListItemIcon sx={{ 
                  minWidth: 36,
                  color: action.color,
                  '& .MuiSvgIcon-root': { fontSize: '1.125rem' }
                }}>
                  {action.icon}
                </ListItemIcon>
                <ListItemText
                  primary={action.text}
                  primaryTypographyProps={{
                    fontSize: '0.8125rem',
                    color: '#64748b',
                  }}
                />
              </ListItemButton>
            ))}
          </List>
        </Box>
      </Box>

      {/* Bottom Section */}
      <Box sx={{ p: 2, borderTop: '1px solid #e2e8f0' }}>
        <Box
          sx={{
            p: 2,
            borderRadius: '12px',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            textAlign: 'center',
          }}
        >
          <TrendingUp sx={{ mb: 1, fontSize: '1.5rem' }} />
          <Typography variant="body2" sx={{ fontWeight: 600, mb: 0.5 }}>
            Carbon Saved
          </Typography>
          <Typography variant="h6" sx={{ fontWeight: 700 }}>
            2,847 kg CO₂
          </Typography>
          <Typography variant="caption" sx={{ opacity: 0.8 }}>
            This month
          </Typography>
        </Box>
      </Box>
    </Drawer>
  );
};

export default Sidebar;
