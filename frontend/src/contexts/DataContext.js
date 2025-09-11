import React, { createContext, useContext, useState, useEffect } from 'react';

const DataContext = createContext();

export const DataProvider = ({ children }) => {
  const [projects, setProjects] = useState([]);
  const [materials, setMaterials] = useState([]);
  const [calculations, setCalculations] = useState([]);
  const [loading, setLoading] = useState(false);

  // Sample data
  const sampleProjects = [
    {
      id: 1,
      name: 'Steel Production LCA',
      description: 'Comprehensive LCA analysis for steel production facility',
      status: 'Active',
      progress: 75,
      created_at: new Date().toISOString(),
      carbonSaved: 1250,
    },
    {
      id: 2,
      name: 'Aluminum Recycling',
      description: 'LCA assessment of aluminum recycling processes',
      status: 'Completed',
      progress: 100,
      created_at: new Date().toISOString(),
      carbonSaved: 890,
    },
  ];

  useEffect(() => {
    // Initialize with sample data
    setProjects(sampleProjects);
  }, []);

  const fetchProjects = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/projects/');
      if (response.ok) {
        const data = await response.json();
        setProjects(data.results || data);
      }
    } catch (error) {
      console.error('Error fetching projects:', error);
      // Keep sample data on error
      setProjects(sampleProjects);
    } finally {
      setLoading(false);
    }
  };

  const createProject = async (projectData) => {
    try {
      const response = await fetch('/api/projects/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify(projectData),
      });
      
      if (response.ok) {
        const newProject = await response.json();
        setProjects(prev => [...prev, newProject]);
        return newProject;
      }
    } catch (error) {
      console.error('Error creating project:', error);
      throw error;
    }
  };

  const updateProject = async (projectId, updateData) => {
    try {
      const response = await fetch(`/api/projects/${projectId}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Token ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify(updateData),
      });
      
      if (response.ok) {
        const updatedProject = await response.json();
        setProjects(prev => prev.map(p => p.id === projectId ? updatedProject : p));
        return updatedProject;
      }
    } catch (error) {
      console.error('Error updating project:', error);
      throw error;
    }
  };

  const deleteProject = async (projectId) => {
    try {
      const response = await fetch(`/api/projects/${projectId}/`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Token ${localStorage.getItem('token')}`,
        },
      });
      
      if (response.ok) {
        setProjects(prev => prev.filter(p => p.id !== projectId));
        return true;
      }
    } catch (error) {
      console.error('Error deleting project:', error);
      throw error;
    }
  };

  const value = {
    projects,
    materials,
    calculations,
    loading,
    fetchProjects,
    createProject,
    updateProject,
    deleteProject,
  };

  return (
    <DataContext.Provider value={value}>
      {children}
    </DataContext.Provider>
  );
};

export const useData = () => {
  const context = useContext(DataContext);
  if (!context) {
    throw new Error('useData must be used within a DataProvider');
  }
  return context;
};
