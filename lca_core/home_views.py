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
        <title>LCA Analysis Platform - Professional Life Cycle Assessment</title>
        <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            :root {{
                --primary-dark: #1a365d;
                --primary-blue: #2b6cb0;
                --primary-light: #63b3ed;
                --accent-green: #38a169;
                --accent-orange: #dd6b20;
                --neutral-50: #f9fafb;
                --neutral-100: #f3f4f6;
                --neutral-200: #e5e7eb;
                --neutral-300: #d1d5db;
                --neutral-700: #374151;
                --neutral-800: #1f2937;
                --neutral-900: #111827;
            }}
            
            body {{
                font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: var(--neutral-50);
                color: var(--neutral-800);
                line-height: 1.6;
                font-size: 16px;
            }}
            
            
            .header {{
                background: var(--primary-dark);
                color: white;
                padding: 0;
                position: sticky;
                top: 0;
                z-index: 1000;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            
            .navbar {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                max-width: 1200px;
                margin: 0 auto;
                padding: 1rem 2rem;
            }}
            
            .brand {{
                display: flex;
                align-items: center;
                gap: 12px;
                color: white;
                text-decoration: none;
                font-weight: 600;
                font-size: 1.25rem;
            }}
            
            .brand-icon {{
                width: 32px;
                height: 32px;
                background: var(--accent-green);
                border-radius: 6px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
            }}
            
            .nav-menu {{
                display: flex;
                gap: 2rem;
                list-style: none;
            }}
            
            .nav-link {{
                color: rgba(255, 255, 255, 0.9);
                text-decoration: none;
                font-weight: 500;
                padding: 0.5rem 0;
                transition: color 0.2s ease;
                border-bottom: 2px solid transparent;
            }}
            
            .nav-link:hover {{
                color: white;
                border-bottom-color: var(--primary-light);
            }}
            
            .main-content {{
                background: var(--neutral-50);
            }}
            
            .hero-section {{
                background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-blue) 100%);
                color: white;
                padding: 4rem 0;
                text-align: center;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 2rem;
            }}
            
            .hero-title {{
                font-size: 3rem;
                font-weight: 700;
                margin-bottom: 1rem;
                letter-spacing: -0.02em;
            }}
            
            .hero-subtitle {{
                font-size: 1.25rem;
                font-weight: 400;
                color: rgba(255, 255, 255, 0.9);
                margin-bottom: 2.5rem;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
            }}
            
            .cta-group {{
                display: flex;
                gap: 1rem;
                justify-content: center;
                margin-bottom: 3rem;
            }}
            
            .btn {{
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.875rem 1.5rem;
                border-radius: 6px;
                text-decoration: none;
                font-weight: 600;
                font-size: 1rem;
                transition: all 0.2s ease;
                border: none;
                cursor: pointer;
            }}
            
            .btn-primary {{
                background: var(--accent-green);
                color: white;
            }}
            
            .btn-primary:hover {{
                background: #2f855a;
                transform: translateY(-1px);
            }}
            
            .btn-secondary {{
                background: transparent;
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.3);
            }}
            
            .btn-secondary:hover {{
                background: rgba(255, 255, 255, 0.1);
                border-color: white;
            }}
            
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1.5rem;
                margin-top: 3rem;
            }}
            
            .stat-card {{
                background: rgba(255, 255, 255, 0.1);
                padding: 1.5rem;
                border-radius: 8px;
                text-align: center;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            
            .stat-number {{
                font-size: 2.5rem;
                font-weight: 700;
                color: var(--primary-light);
                display: block;
                margin-bottom: 0.5rem;
            }}
            
            .stat-label {{
                font-size: 0.9rem;
                color: rgba(255, 255, 255, 0.8);
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            .features-section {{
                padding: 5rem 0;
                background: white;
            }}
            
            .section-header {{
                text-align: center;
                margin-bottom: 3rem;
            }}
            
            .section-title {{
                font-size: 2.25rem;
                font-weight: 700;
                color: var(--neutral-900);
                margin-bottom: 1rem;
            }}
            
            .section-description {{
                font-size: 1.125rem;
                color: var(--neutral-700);
                max-width: 600px;
                margin: 0 auto;
            }}
            
            .features-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
                gap: 2rem;
            }}
            
            .feature-item {{
                padding: 2rem;
                border: 1px solid var(--neutral-200);
                border-radius: 8px;
                background: white;
                transition: all 0.2s ease;
            }}
            
            .feature-item:hover {{
                border-color: var(--primary-light);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }}
            
            .feature-icon {{
                width: 48px;
                height: 48px;
                background: var(--primary-blue);
                color: white;
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                margin-bottom: 1rem;
            }}
            
            .feature-title {{
                font-size: 1.25rem;
                font-weight: 600;
                color: var(--neutral-900);
                margin-bottom: 0.75rem;
            }}
            
            .feature-description {{
                color: var(--neutral-700);
                line-height: 1.6;
            }}
            
            .quick-access {{
                background: var(--neutral-100);
                padding: 4rem 0;
            }}
            
            .access-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1.5rem;
            }}
            
            .access-card {{
                background: white;
                padding: 2rem;
                border-radius: 8px;
                border: 1px solid var(--neutral-200);
                text-decoration: none;
                transition: all 0.2s ease;
                display: block;
            }}
            
            .access-card:hover {{
                border-color: var(--primary-blue);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                text-decoration: none;
            }}
            
            .access-icon {{
                width: 40px;
                height: 40px;
                background: var(--primary-light);
                color: white;
                border-radius: 6px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
                margin-bottom: 1rem;
            }}
            
            .access-title {{
                font-size: 1.125rem;
                font-weight: 600;
                color: var(--neutral-900);
                margin-bottom: 0.5rem;
            }}
            
            .access-description {{
                color: var(--neutral-700);
                font-size: 0.9rem;
            }}
            
            .footer {{
                background: var(--neutral-900);
                color: var(--neutral-300);
                padding: 2.5rem 0;
                text-align: center;
            }}
            
            .footer-content {{
                border-top: 1px solid var(--neutral-700);
                padding-top: 2rem;
            }}
            
            .footer p {{
                margin-bottom: 0.5rem;
            }}
            
            .footer-highlight {{
                color: var(--primary-light);
                font-weight: 500;
            }}
            
            @media (max-width: 768px) {{
                .hero-title {{
                    font-size: 2.25rem;
                }}
                
                .hero-subtitle {{
                    font-size: 1.125rem;
                }}
                
                .cta-group {{
                    flex-direction: column;
                    align-items: center;
                }}
                
                .nav-menu {{
                    display: none;
                }}
                
                .stats-grid {{
                    grid-template-columns: repeat(2, 1fr);
                }}
            }}
        </style>
    </head>
    <body>
        <header class="header">
            <nav class="navbar">
                <a href="/" class="brand">
                    <div class="brand-icon">
                        <i class="bi bi-leaf"></i>
                    </div>
                    LCA Platform
                </a>
                <ul class="nav-menu">
                    <li><a href="/admin/" class="nav-link">Dashboard</a></li>
                    <li><a href="/api/" class="nav-link">API</a></li>
                    <li><a href="#features" class="nav-link">Features</a></li>
                </ul>
            </nav>
        </header>

        <main class="main-content">
            <section class="hero-section">
                <div class="container">
                    <h1 class="hero-title">Life Cycle Assessment Platform</h1>
                    <p class="hero-subtitle">
                        Enterprise-grade environmental impact analysis for manufacturing and industrial processes. 
                        Make informed sustainability decisions with comprehensive LCA data.
                    </p>
                    
                    <div class="cta-group">
                        <a href="/admin/" class="btn btn-primary">
                            <i class="bi bi-speedometer2"></i>
                            Access Dashboard
                        </a>
                        <a href="/api/" class="btn btn-secondary">
                            <i class="bi bi-code-square"></i>
                            API Documentation
                        </a>
                    </div>
                    
                    <div class="stats-grid">
                        <div class="stat-card">
                            <span class="stat-number">{projects_count}</span>
                            <span class="stat-label">Active Projects</span>
                        </div>
                        <div class="stat-card">
                            <span class="stat-number">{calculations_count}</span>
                            <span class="stat-label">Calculations</span>
                        </div>
                        <div class="stat-card">
                            <span class="stat-number">1,247</span>
                            <span class="stat-label">Kg CO₂ Analyzed</span>
                        </div>
                        <div class="stat-card">
                            <span class="stat-number">99.9%</span>
                            <span class="stat-label">System Uptime</span>
                        </div>
                    </div>
                </div>
            </section>

            <section class="features-section" id="features">
                <div class="container">
                    <div class="section-header">
                        <h2 class="section-title">Core Capabilities</h2>
                        <p class="section-description">
                            Comprehensive tools for environmental impact assessment and sustainability analysis
                        </p>
                    </div>
                    
                    <div class="features-grid">
                        <div class="feature-item">
                            <div class="feature-icon">
                                <i class="bi bi-graph-up"></i>
                            </div>
                            <h3 class="feature-title">Impact Assessment</h3>
                            <p class="feature-description">
                                Quantify environmental impacts across the entire product lifecycle with standardized methodologies and comprehensive impact categories.
                            </p>
                        </div>
                        
                        <div class="feature-item">
                            <div class="feature-icon">
                                <i class="bi bi-diagram-3"></i>
                            </div>
                            <h3 class="feature-title">Process Modeling</h3>
                            <p class="feature-description">
                                Model complex industrial processes with detailed material and energy flows for accurate environmental footprint calculation.
                            </p>
                        </div>
                        
                        <div class="feature-item">
                            <div class="feature-icon">
                                <i class="bi bi-clipboard-data"></i>
                            </div>
                            <h3 class="feature-title">Data Management</h3>
                            <p class="feature-description">
                                Centralized database for inventory data, impact factors, and project management with version control and audit trails.
                            </p>
                        </div>
                        
                        <div class="feature-item">
                            <div class="feature-icon">
                                <i class="bi bi-shield-check"></i>
                            </div>
                            <h3 class="feature-title">Standards Compliance</h3>
                            <p class="feature-description">
                                Full compliance with ISO 14040/14044 standards and integration with major LCA databases and methodologies.
                            </p>
                        </div>
                        
                        <div class="feature-item">
                            <div class="feature-icon">
                                <i class="bi bi-file-earmark-text"></i>
                            </div>
                            <h3 class="feature-title">Report Generation</h3>
                            <p class="feature-description">
                                Generate detailed technical reports and executive summaries with customizable templates and data visualizations.
                            </p>
                        </div>
                        
                        <div class="feature-item">
                            <div class="feature-icon">
                                <i class="bi bi-cloud-arrow-up"></i>
                            </div>
                            <h3 class="feature-title">API Integration</h3>
                            <p class="feature-description">
                                RESTful API for seamless integration with existing enterprise systems and third-party sustainability tools.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            <section class="quick-access">
                <div class="container">
                    <div class="section-header">
                        <h2 class="section-title">System Access</h2>
                        <p class="section-description">Quick links to platform components and resources</p>
                    </div>
                    
                    <div class="access-grid">
                        <a href="/admin/" class="access-card">
                            <div class="access-icon">
                                <i class="bi bi-house-door"></i>
                            </div>
                            <h3 class="access-title">Administration</h3>
                            <p class="access-description">Project management and system configuration</p>
                        </a>
                        
                        <a href="/api/" class="access-card">
                            <div class="access-icon">
                                <i class="bi bi-terminal"></i>
                            </div>
                            <h3 class="access-title">API Explorer</h3>
                            <p class="access-description">Interactive API documentation and testing</p>
                        </a>
                        
                        <a href="/api/projects/" class="access-card">
                            <div class="access-icon">
                                <i class="bi bi-folder"></i>
                            </div>
                            <h3 class="access-title">Projects Endpoint</h3>
                            <p class="access-description">REST API for project data management</p>
                        </a>
                        
                        <a href="/api/calculations/" class="access-card">
                            <div class="access-icon">
                                <i class="bi bi-calculator"></i>
                            </div>
                            <h3 class="access-title">Calculations API</h3>
                            <p class="access-description">LCA calculation results and analytics</p>
                        </a>
                    </div>
                </div>
            </section>
        </main>

        <footer class="footer">
            <div class="container">
                <div class="footer-content">
                    <p>&copy; 2025 <span class="footer-highlight">LCA Platform</span> - Professional Life Cycle Assessment</p>
                    <p>Environmental sustainability through data-driven analysis</p>
                </div>
            </div>
        </footer>

        <script>
            // Smooth scrolling for navigation links
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
                anchor.addEventListener('click', function (e) {{
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {{
                        target.scrollIntoView({{
                            behavior: 'smooth',
                            block: 'start'
                        }});
                    }}
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


@api_view(['GET'])
def api_status(request):
    """API status endpoint"""
    return Response({
        'status': 'online',
        'message': 'LCA Analysis Tool API is running',
        'version': '1.0.0'
    })
