from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import LCAProject, LCACalculation


def home(request):
    """Modern professional home page"""
    projects_count = LCAProject.objects.count()
    calculations_count = LCACalculation.objects.count()
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LCA Pro - Life Cycle Assessment Suite</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <link href="https://cdn.jsdelivr.net/npm/feather-icons@4.28.0/dist/feather.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/feather-icons/dist/feather.min.js"></script>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #1a202c;
                line-height: 1.6;
            }}
            
            .navbar {{
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border-bottom: 1px solid rgba(255, 255, 255, 0.2);
                padding: 1rem 0;
                position: fixed;
                width: 100%;
                top: 0;
                z-index: 1000;
            }}
            
            .nav-container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 2rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            
            .logo {{
                display: flex;
                align-items: center;
                gap: 12px;
                font-size: 1.5rem;
                font-weight: 700;
                color: white;
                text-decoration: none;
            }}
            
            .logo-icon {{
                width: 40px;
                height: 40px;
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
            }}
            
            .nav-links {{
                display: flex;
                gap: 2rem;
                align-items: center;
            }}
            
            .nav-link {{
                color: rgba(255, 255, 255, 0.9);
                text-decoration: none;
                font-weight: 500;
                transition: all 0.3s ease;
                padding: 0.5rem 1rem;
                border-radius: 8px;
            }}
            
            .nav-link:hover {{
                background: rgba(255, 255, 255, 0.1);
                color: white;
            }}
            
            .hero {{
                margin-top: 80px;
                padding: 6rem 0;
                text-align: center;
                color: white;
            }}
            
            .hero-container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 2rem;
            }}
            
            .hero h1 {{
                font-size: 4rem;
                font-weight: 800;
                margin-bottom: 1.5rem;
                background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }}
            
            .hero-subtitle {{
                font-size: 1.5rem;
                font-weight: 400;
                margin-bottom: 3rem;
                color: rgba(255, 255, 255, 0.9);
                max-width: 800px;
                margin-left: auto;
                margin-right: auto;
            }}
            
            .cta-buttons {{
                display: flex;
                gap: 1rem;
                justify-content: center;
                margin-bottom: 4rem;
            }}
            
            .btn {{
                padding: 1rem 2rem;
                border-radius: 12px;
                text-decoration: none;
                font-weight: 600;
                font-size: 1.1rem;
                transition: all 0.3s ease;
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                border: none;
                cursor: pointer;
            }}
            
            .btn-primary {{
                background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                color: white;
                box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
            }}
            
            .btn-primary:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(16, 185, 129, 0.6);
            }}
            
            .btn-secondary {{
                background: rgba(255, 255, 255, 0.1);
                color: white;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            
            .btn-secondary:hover {{
                background: rgba(255, 255, 255, 0.2);
                transform: translateY(-2px);
            }}
            
            .stats {{
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border-radius: 20px;
                padding: 2rem;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 2rem;
                margin-bottom: 4rem;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            
            .stat-item {{
                text-align: center;
                color: white;
            }}
            
            .stat-number {{
                font-size: 3rem;
                font-weight: 800;
                color: #10b981;
                margin-bottom: 0.5rem;
            }}
            
            .stat-label {{
                font-size: 1.1rem;
                color: rgba(255, 255, 255, 0.8);
                font-weight: 500;
            }}
            
            .features {{
                background: white;
                padding: 6rem 0;
                margin-top: 4rem;
            }}
            
            .features-container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 2rem;
            }}
            
            .features h2 {{
                text-align: center;
                font-size: 2.5rem;
                font-weight: 700;
                color: #1a202c;
                margin-bottom: 3rem;
            }}
            
            .features-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 2rem;
                margin-bottom: 4rem;
            }}
            
            .feature-card {{
                background: white;
                padding: 2rem;
                border-radius: 20px;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
                border: 1px solid #e2e8f0;
                transition: all 0.3s ease;
                text-align: center;
            }}
            
            .feature-card:hover {{
                transform: translateY(-8px);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
            }}
            
            .feature-icon {{
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 1.5rem;
                color: white;
            }}
            
            .feature-title {{
                font-size: 1.3rem;
                font-weight: 600;
                color: #1a202c;
                margin-bottom: 1rem;
            }}
            
            .feature-description {{
                color: #64748b;
                line-height: 1.6;
            }}
            
            .quick-links {{
                background: #f8fafc;
                padding: 4rem 0;
            }}
            
            .quick-links-container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 2rem;
                text-align: center;
            }}
            
            .quick-links h3 {{
                font-size: 2rem;
                font-weight: 700;
                color: #1a202c;
                margin-bottom: 2rem;
            }}
            
            .links-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1.5rem;
            }}
            
            .link-card {{
                background: white;
                padding: 2rem;
                border-radius: 16px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                border: 1px solid #e2e8f0;
                text-decoration: none;
                transition: all 0.3s ease;
                display: block;
            }}
            
            .link-card:hover {{
                transform: translateY(-4px);
                box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
                text-decoration: none;
            }}
            
            .link-icon {{
                width: 48px;
                height: 48px;
                background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 1rem;
                color: white;
            }}
            
            .link-title {{
                font-size: 1.1rem;
                font-weight: 600;
                color: #1a202c;
                margin-bottom: 0.5rem;
            }}
            
            .link-description {{
                color: #64748b;
                font-size: 0.9rem;
            }}
            
            .footer {{
                background: #1a202c;
                color: white;
                padding: 3rem 0;
                text-align: center;
            }}
            
            .footer-container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 2rem;
            }}
            
            .pulse {{
                animation: pulse 2s infinite;
            }}
            
            @keyframes pulse {{
                0% {{ opacity: 1; }}
                50% {{ opacity: 0.7; }}
                100% {{ opacity: 1; }}
            }}
            
            @media (max-width: 768px) {{
                .hero h1 {{
                    font-size: 2.5rem;
                }}
                
                .hero-subtitle {{
                    font-size: 1.2rem;
                }}
                
                .cta-buttons {{
                    flex-direction: column;
                    align-items: center;
                }}
                
                .nav-links {{
                    display: none;
                }}
            }}
        </style>
    </head>
    <body>
        <!-- Navigation -->
        <nav class="navbar">
            <div class="nav-container">
                <a href="/" class="logo">
                    <div class="logo-icon">
                        <i data-feather="zap"></i>
                    </div>
                    LCA Pro
                </a>
                <div class="nav-links">
                    <a href="/admin/" class="nav-link">Dashboard</a>
                    <a href="/api/" class="nav-link">API</a>
                    <a href="#features" class="nav-link">Features</a>
                </div>
            </div>
        </nav>

        <!-- Hero Section -->
        <section class="hero">
            <div class="hero-container">
                <h1>Life Cycle Assessment Suite</h1>
                <p class="hero-subtitle">
                    Professional-grade LCA analysis for metallurgy and mining industries. 
                    Assess environmental impact, optimize processes, and drive sustainability with AI-powered insights.
                </p>
                
                <div class="cta-buttons">
                    <a href="/admin/" class="btn btn-primary">
                        <i data-feather="play-circle"></i>
                        Launch Dashboard
                    </a>
                    <a href="/api/" class="btn btn-secondary">
                        <i data-feather="code"></i>
                        Explore API
                    </a>
                </div>
                
                <div class="stats">
                    <div class="stat-item">
                        <div class="stat-number">{projects_count}</div>
                        <div class="stat-label">LCA Projects</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{calculations_count}</div>
                        <div class="stat-label">Calculations</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number pulse">2,847</div>
                        <div class="stat-label">kg CO₂ Saved</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">24/7</div>
                        <div class="stat-label">Real-time Monitoring</div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Features Section -->
        <section class="features" id="features">
            <div class="features-container">
                <h2>Powerful LCA Analysis Features</h2>
                <div class="features-grid">
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i data-feather="activity"></i>
                        </div>
                        <h3 class="feature-title">Real-time Impact Assessment</h3>
                        <p class="feature-description">
                            Monitor environmental impacts in real-time with advanced analytics and AI-powered predictions for comprehensive LCA studies.
                        </p>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i data-feather="layers"></i>
                        </div>
                        <h3 class="feature-title">Process Optimization</h3>
                        <p class="feature-description">
                            Optimize industrial processes with detailed environmental assessments and efficiency recommendations.
                        </p>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i data-feather="trending-up"></i>
                        </div>
                        <h3 class="feature-title">Advanced Analytics</h3>
                        <p class="feature-description">
                            Leverage machine learning algorithms for impact prediction, benchmarking, and sustainability insights.
                        </p>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i data-feather="shield-check"></i>
                        </div>
                        <h3 class="feature-title">ISO Compliance</h3>
                        <p class="feature-description">
                            Ensure compliance with ISO 14040/14044 standards with built-in validation and reporting tools.
                        </p>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i data-feather="database"></i>
                        </div>
                        <h3 class="feature-title">Materials Database</h3>
                        <p class="feature-description">
                            Access comprehensive materials database with environmental impact factors and sustainability metrics.
                        </p>
                    </div>
                    
                    <div class="feature-card">
                        <div class="feature-icon">
                            <i data-feather="file-text"></i>
                        </div>
                        <h3 class="feature-title">Professional Reports</h3>
                        <p class="feature-description">
                            Generate comprehensive LCA reports with visualizations, compliance documentation, and export capabilities.
                        </p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Quick Links Section -->
        <section class="quick-links">
            <div class="quick-links-container">
                <h3>Get Started</h3>
                <div class="links-grid">
                    <a href="/admin/" class="link-card">
                        <div class="link-icon">
                            <i data-feather="layout"></i>
                        </div>
                        <div class="link-title">Admin Dashboard</div>
                        <div class="link-description">Manage projects and view analytics</div>
                    </a>
                    
                    <a href="/api/" class="link-card">
                        <div class="link-icon">
                            <i data-feather="code"></i>
                        </div>
                        <div class="link-title">REST API</div>
                        <div class="link-description">Integrate with your applications</div>
                    </a>
                    
                    <a href="/api/projects/" class="link-card">
                        <div class="link-icon">
                            <i data-feather="folder"></i>
                        </div>
                        <div class="link-title">Projects API</div>
                        <div class="link-description">Manage LCA projects programmatically</div>
                    </a>
                    
                    <a href="/api/calculations/" class="link-card">
                        <div class="link-icon">
                            <i data-feather="calculator"></i>
                        </div>
                        <div class="link-title">Calculations API</div>
                        <div class="link-description">Access calculation results and data</div>
                    </a>
                </div>
            </div>
        </section>

        <!-- Footer -->
        <footer class="footer">
            <div class="footer-container">
                <p>&copy; 2025 LCA Pro - Professional Life Cycle Assessment Suite</p>
                <p>Empowering sustainable decisions in metallurgy and mining industries</p>
            </div>
        </footer>

        <script>
            // Initialize Feather icons
            feather.replace();
            
            // Smooth scrolling for anchor links
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
                anchor.addEventListener('click', function (e) {{
                    e.preventDefault();
                    document.querySelector(this.getAttribute('href')).scrollIntoView({{
                        behavior: 'smooth'
                    }});
                }});
            }});
        </script>
    </body>
    </html>
    """
    return HttpResponse(html)


@api_view(['GET'])
def api_overview(request):
    """API overview with available endpoints"""
    endpoints = {
        'projects': {
            'url': '/api/projects/',
            'methods': ['GET', 'POST'],
            'description': 'Create and retrieve LCA projects'
        },
        'project_detail': {
            'url': '/api/projects/{id}/',
            'methods': ['GET', 'PUT', 'DELETE'],
            'description': 'Retrieve, update or delete a specific project'
        },
        'calculations': {
            'url': '/api/calculations/',
            'methods': ['GET', 'POST'],
            'description': 'Create and retrieve LCA calculations'
        },
        'calculation_detail': {
            'url': '/api/calculations/{id}/',
            'methods': ['GET', 'PUT', 'DELETE'],
            'description': 'Retrieve, update or delete a specific calculation'
        }
    }
    return Response({
        'message': 'LCA Analysis Tool API',
        'endpoints': endpoints
    })
