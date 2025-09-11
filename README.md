# AI-Driven Life Cycle Assessment (LCA) & Circularity Tool

This is a comprehensive AI-powered Life Cycle Assessment platform designed specifically for the metallurgy and mining sector, focusing on aluminium, copper, and critical minerals.

## Database Connection

**NeonDB Connection URL:**
```
postgresql://neondb_owner:npg_nQUD6FSfA0mP@ep-odd-snow-a10f67qx-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

## Features

### 🎯 Core Capabilities
- **Intuitive Dashboard** - Visual overview of projects, environmental impacts, and circularity metrics
- **AI-Powered Analysis** - Machine learning models for parameter estimation and optimization suggestions
- **Circularity Assessment** - Comprehensive circular economy indicators and improvement strategies
- **Natural Language Queries** - Ask questions like "What if I use 50% recycled aluminium?"
- **Scenario Comparison** - Compare linear vs circular pathways side-by-side
- **Automated Reporting** - Generate ESG-compliant sustainability reports

### 🔧 Technical Features
- **Material Database** - Comprehensive database with environmental impact factors
- **Process Modeling** - Drag-and-drop workflow design for metal life cycles
- **OpenLCA Integration** - Connect to industry-standard LCA databases
- **Real-time Calculations** - Fast LCA computations with uncertainty analysis
- **Interactive Visualizations** - Sankey diagrams, circularity loops, and impact charts
- **API Integration** - REST/GraphQL endpoints for external integrations

### 🤖 AI Components
- **Parameter Prediction** - AI models predict missing process values
- **Recommendation Engine** - Suggests circular economy improvements
- **Sensitivity Analysis** - Identify most impactful parameters
- **Data Quality Assessment** - Evaluate and improve input data quality
- **Natural Language Processing** - Understand and respond to user queries

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (optional)

### Development Setup

1. **Clone and setup backend**
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Copy environment file
   cp .env.example .env
   
   # Run migrations
   python manage.py migrate
   
   # Create superuser
   python manage.py createsuperuser
   
   # Start development server
   python manage.py runserver
   ```

2. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Docker Setup (Alternative)**
   ```bash
   docker-compose up --build
   ```

## Project Structure

```
LCA-Analysis-Tool/
├── backend/
│   ├── lca_tool/           # Django project
│   ├── lca_core/           # Core LCA functionality
│   ├── materials/          # Materials database
│   ├── processes/          # Process modeling
│   ├── ai_models/          # AI/ML components
│   ├── circularity/        # Circularity analysis
│   ├── reporting/          # Report generation
│   ├── user_management/    # User profiles
│   └── data_integration/   # Data import/export
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── context/        # React context
│   └── public/
└── docs/                   # Documentation
```

## Usage

### Creating Your First Project

1. Access the Dashboard at `http://localhost:3000`
2. Login with your credentials
3. Create New Project with project details
4. Build Process Flow using drag-and-drop interface
5. Add Materials and process parameters
6. Run LCA Calculation to get environmental impacts
7. Analyze Results with AI insights

### Natural Language Queries

Ask questions naturally:
- "What if I use 50% recycled aluminium?"
- "Compare carbon footprint of different transport methods"
- "Show me the most energy-intensive processes"
- "What are the best circularity improvements?"

## Technology Stack

### Backend
- **Django 4.2** with REST Framework
- **PostgreSQL** (NeonDB) for data storage
- **Redis** for caching and task queuing
- **Celery** for background processing
- **PyTorch/scikit-learn** for AI/ML

### Frontend
- **React 18** with Material-UI
- **Redux** for state management
- **D3.js/Plotly** for visualizations
- **React Flow** for process design

### AI/ML
- **PyTorch** for deep learning
- **scikit-learn** for traditional ML
- **Transformers** for NLP
- **Pandas/NumPy** for data processing

## Key Features Implementation

### 1. LCA Calculation Engine
- Comprehensive environmental impact assessment
- Support for multiple impact categories (climate change, resource depletion, etc.)
- Uncertainty analysis and sensitivity testing
- Scenario comparison capabilities

### 2. Circularity Indicators
- Recycled content percentage tracking
- End-of-life recovery rate calculations
- Material efficiency metrics
- Overall circularity scoring

### 3. AI-Powered Recommendations
- Parameter prediction for missing data
- Process optimization suggestions
- Material substitution recommendations
- Circular economy improvement strategies

### 4. Interactive Visualizations
- Sankey diagrams for material flows
- Impact breakdown charts
- Circularity loop visualizations
- Dashboard with key performance indicators

### 5. Data Integration
- OpenLCA database connectivity
- ecoinvent data import capabilities
- Custom dataset upload (CSV, Excel, JSON)
- API endpoints for external integrations

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- **Issues**: Create GitHub issue for bugs
- **Questions**: Use GitHub discussions
- **Documentation**: Check docs/ directory

---

**Built for SIH 2025 - Creating sustainable solutions for the metallurgy and mining industry**