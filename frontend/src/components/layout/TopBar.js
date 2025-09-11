import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Badge,
  Menu,
  MenuItem,
  Avatar,
  Box,
  InputBase,
  Chip,
  Tooltip,
  Divider,
} from '@mui/material';
import {
  Search as SearchIcon,
  Notifications as NotificationsIcon,
  Settings as SettingsIcon,
  AccountCircle,
  ExitToApp,
  Brightness4,
  Brightness7,
  Language,
} from '@mui/icons-material';
import { alpha, styled } from '@mui/material/styles';

const drawerWidth = 280;

const Search = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: '24px',
  backgroundColor: alpha(theme.palette.common.white, 0.08),
  border: `1px solid ${alpha(theme.palette.common.white, 0.12)}`,
  '&:hover': {
    backgroundColor: alpha(theme.palette.common.white, 0.12),
  },
  marginLeft: 0,
  marginRight: theme.spacing(2),
  width: '100%',
  maxWidth: 400,
  [theme.breakpoints.up('sm')]: {
    marginLeft: theme.spacing(1),
    width: 'auto',
  },
}));

const SearchIconWrapper = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  color: alpha(theme.palette.common.white, 0.7),
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  width: '100%',
  '& .MuiInputBase-input': {
    padding: theme.spacing(1, 1, 1, 0),
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create('width'),
    [theme.breakpoints.up('sm')]: {
      width: '200px',
      '&:focus': {
        width: '300px',
      },
    },
  },
}));

const TopBar = () => {
  const [anchorEl, setAnchorEl] = useState(null);
  const [notificationAnchor, setNotificationAnchor] = useState(null);
  const [searchValue, setSearchValue] = useState('');

  const isMenuOpen = Boolean(anchorEl);
  const isNotificationOpen = Boolean(notificationAnchor);

  const handleProfileMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleNotificationOpen = (event) => {
    setNotificationAnchor(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setNotificationAnchor(null);
  };

  const notifications = [
    {
      id: 1,
      title: 'New LCA calculation completed',
      message: 'Project Alpha carbon footprint analysis is ready',
      time: '5 min ago',
      type: 'success',
    },
    {
      id: 2,
      title: 'Material database updated',
      message: 'New sustainable materials added to database',
      time: '1 hour ago',
      type: 'info',
    },
    {
      id: 3,
      title: 'Report generation failed',
      message: 'Beta project report needs attention',
      time: '2 hours ago',
      type: 'warning',
    },
  ];

  const getNotificationColor = (type) => {
    switch (type) {
      case 'success': return '#10b981';
      case 'warning': return '#f59e0b';
      case 'error': return '#ef4444';
      default: return '#3b82f6';
    }
  };

  return (
    <AppBar
      position="fixed"
      sx={{
        width: `calc(100% - ${drawerWidth}px)`,
        ml: `${drawerWidth}px`,
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
        backdropFilter: 'blur(20px)',
      }}
    >
      <Toolbar sx={{ minHeight: '72px !important', px: 3 }}>
        {/* Left Section */}
        <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ 
              fontWeight: 600,
              color: 'white',
              mr: 3,
              fontSize: '1.25rem',
            }}
          >
            Life Cycle Assessment Suite
          </Typography>

          <Search>
            <SearchIconWrapper>
              <SearchIcon />
            </SearchIconWrapper>
            <StyledInputBase
              placeholder="Search projects, materials, processes..."
              inputProps={{ 'aria-label': 'search' }}
              value={searchValue}
              onChange={(e) => setSearchValue(e.target.value)}
            />
          </Search>
        </Box>

        {/* Right Section */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          {/* Status Chips */}
          <Chip
            label="3 Active Projects"
            size="small"
            sx={{
              bgcolor: alpha('#ffffff', 0.2),
              color: 'white',
              fontWeight: 500,
              border: '1px solid rgba(255,255,255,0.3)',
              mr: 1,
            }}
          />

          <Chip
            label="Real-time Data"
            size="small"
            sx={{
              bgcolor: '#10b981',
              color: 'white',
              fontWeight: 500,
              mr: 2,
              animation: 'pulse 2s infinite',
              '@keyframes pulse': {
                '0%': { opacity: 1 },
                '50%': { opacity: 0.7 },
                '100%': { opacity: 1 },
              },
            }}
          />

          {/* Theme Toggle */}
          <Tooltip title="Toggle theme">
            <IconButton
              sx={{ 
                color: 'white',
                '&:hover': { bgcolor: alpha('#ffffff', 0.1) }
              }}
            >
              <Brightness4 />
            </IconButton>
          </Tooltip>

          {/* Language */}
          <Tooltip title="Language">
            <IconButton
              sx={{ 
                color: 'white',
                '&:hover': { bgcolor: alpha('#ffffff', 0.1) }
              }}
            >
              <Language />
            </IconButton>
          </Tooltip>

          {/* Notifications */}
          <Tooltip title="Notifications">
            <IconButton
              onClick={handleNotificationOpen}
              sx={{ 
                color: 'white',
                '&:hover': { bgcolor: alpha('#ffffff', 0.1) }
              }}
            >
              <Badge badgeContent={notifications.length} color="error">
                <NotificationsIcon />
              </Badge>
            </IconButton>
          </Tooltip>

          {/* Settings */}
          <Tooltip title="Settings">
            <IconButton
              sx={{ 
                color: 'white',
                '&:hover': { bgcolor: alpha('#ffffff', 0.1) }
              }}
            >
              <SettingsIcon />
            </IconButton>
          </Tooltip>

          {/* Profile */}
          <Tooltip title="Account">
            <IconButton
              onClick={handleProfileMenuOpen}
              sx={{ 
                ml: 1,
                '&:hover': { bgcolor: alpha('#ffffff', 0.1) }
              }}
            >
              <Avatar sx={{ width: 36, height: 36, bgcolor: alpha('#ffffff', 0.2) }}>
                A
              </Avatar>
            </IconButton>
          </Tooltip>
        </Box>

        {/* Profile Menu */}
        <Menu
          anchorEl={anchorEl}
          open={isMenuOpen}
          onClose={handleMenuClose}
          onClick={handleMenuClose}
          PaperProps={{
            elevation: 8,
            sx: {
              overflow: 'visible',
              filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
              mt: 1.5,
              minWidth: 200,
              borderRadius: 2,
              '&:before': {
                content: '""',
                display: 'block',
                position: 'absolute',
                top: 0,
                right: 14,
                width: 10,
                height: 10,
                bgcolor: 'background.paper',
                transform: 'translateY(-50%) rotate(45deg)',
                zIndex: 0,
              },
            },
          }}
          transformOrigin={{ horizontal: 'right', vertical: 'top' }}
          anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
        >
          <Box sx={{ px: 2, py: 1.5, borderBottom: '1px solid #e2e8f0' }}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
              Admin User
            </Typography>
            <Typography variant="body2" color="text.secondary">
              admin@lcaapp.com
            </Typography>
          </Box>
          <MenuItem>
            <AccountCircle sx={{ mr: 2, color: '#64748b' }} />
            My Profile
          </MenuItem>
          <MenuItem>
            <SettingsIcon sx={{ mr: 2, color: '#64748b' }} />
            Account Settings
          </MenuItem>
          <Divider />
          <MenuItem sx={{ color: '#ef4444' }}>
            <ExitToApp sx={{ mr: 2 }} />
            Logout
          </MenuItem>
        </Menu>

        {/* Notification Menu */}
        <Menu
          anchorEl={notificationAnchor}
          open={isNotificationOpen}
          onClose={handleMenuClose}
          PaperProps={{
            elevation: 8,
            sx: {
              overflow: 'visible',
              filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
              mt: 1.5,
              maxWidth: 360,
              borderRadius: 2,
            },
          }}
          transformOrigin={{ horizontal: 'right', vertical: 'top' }}
          anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
        >
          <Box sx={{ px: 2, py: 1.5, borderBottom: '1px solid #e2e8f0' }}>
            <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
              Notifications
            </Typography>
          </Box>
          {notifications.map((notification) => (
            <MenuItem key={notification.id} sx={{ px: 2, py: 1.5, alignItems: 'flex-start' }}>
              <Box
                sx={{
                  width: 8,
                  height: 8,
                  borderRadius: '50%',
                  bgcolor: getNotificationColor(notification.type),
                  mr: 2,
                  mt: 1,
                  flexShrink: 0,
                }}
              />
              <Box>
                <Typography variant="body2" sx={{ fontWeight: 500, mb: 0.5 }}>
                  {notification.title}
                </Typography>
                <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 0.5 }}>
                  {notification.message}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {notification.time}
                </Typography>
              </Box>
            </MenuItem>
          ))}
        </Menu>
      </Toolbar>
    </AppBar>
  );
};

export default TopBar;
