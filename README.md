# 🚀 DealFlowAI - AI-Powered Investment Thesis Analyzer

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2+-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/TanmaySingh007/DealFlowAI)](https://github.com/TanmaySingh007/DealFlowAI/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/TanmaySingh007/DealFlowAI)](https://github.com/TanmaySingh007/DealFlowAI/network)

## 📋 Table of Contents
- [Overview](#-overview)
- [Key Features](#-key-features)
- [Technology Stack](#️-technology-stack)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Database Schema](#-database-schema)
- [AI/ML Services](#-aiml-services)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [Support](#-support)

## 📋 Overview

DealFlowAI is a cutting-edge AI-powered platform that revolutionizes investment thesis analysis and company matching. Built with Django 5.2+ and modern machine learning frameworks, it provides intelligent insights for investment decision-making through advanced natural language processing and semantic analysis.

### 🎯 **What DealFlowAI Does**
- **Analyzes Investment Theses** - Extracts key criteria using advanced NLP
- **Matches Companies** - Finds the best-fit companies using semantic similarity
- **Provides AI Insights** - Real-time investment advice and recommendations
- **Tracks Deals** - Comprehensive deal management and analytics
- **Visualizes Data** - Interactive dashboards and charts

## ✨ Key Features

### 🤖 **Advanced AI Capabilities**
- **Natural Language Processing** - Extracts investment criteria from thesis text
- **Semantic Similarity Analysis** - Uses sentence transformers for accurate matching
- **Sentiment Analysis** - Analyzes thesis sentiment and confidence levels
- **Intelligent Recommendations** - AI-powered company suggestions
- **Real-time Chatbot** - Interactive investment advice system

### 🎨 **Modern UI/UX Design**
- **Dark/Light Mode Toggle** - Seamless theme switching
- **3D Glassmorphism Effects** - Modern visual design with depth
- **Responsive Layout** - Perfect on desktop, tablet, and mobile
- **Smooth Animations** - CSS3 transitions and hover effects
- **Interactive Elements** - Dynamic charts and progress indicators

### 📊 **Comprehensive Analytics**
- **Real-time Dashboard** - Live statistics and insights
- **Deal Status Tracking** - Visual progress indicators
- **Industry Distribution** - Sector-wise company breakdown
- **Revenue Analytics** - ARR-based company analysis
- **Funding Stage Analysis** - Investment stage tracking

### 🏢 **Extensive Company Database**
- **500+ Companies** - Comprehensive database across industries
- **15+ Industry Sectors** - Technology, Healthcare, FinTech, EdTech, etc.
- **Multiple Funding Stages** - Seed to Series C+ across all sectors
- **Revenue Ranges** - $1M to $200M+ ARR
- **Detailed Profiles** - Industry, funding, revenue, and descriptions

## 🛠️ Technology Stack

### **Backend Framework**
- **Django 5.2.4** - Modern web framework
- **Django REST Framework 3.14.0** - API development
- **Django CORS Headers 4.3.1** - Cross-origin resource sharing

### **AI/ML Libraries**
- **Hugging Face Transformers 4.35.0** - State-of-the-art NLP models
- **Sentence Transformers 2.2.2** - Semantic similarity and embeddings
- **spaCy 3.7.2** - Industrial-strength NLP
- **NLTK 3.8.1** - Natural language toolkit
- **TextBlob 0.17.1** - Sentiment analysis
- **LangChain 0.1.0** - LLM framework integration

### **Data Science & Analytics**
- **scikit-learn 1.3.2** - Machine learning algorithms
- **NumPy 1.24.3** - Numerical computing
- **Pandas 2.0.3** - Data manipulation
- **SciPy 1.11.1** - Scientific computing

### **Vector Database & Embeddings**
- **ChromaDB 0.4.18** - Vector database
- **FAISS-CPU 1.7.4** - Similarity search
- **Pinecone Client 2.2.4** - Vector database integration

### **Frontend Technologies**
- **HTML5/CSS3** - Modern responsive design
- **JavaScript (ES6+)** - Interactive functionality
- **CSS3 Animations** - 3D effects and transitions
- **Chart.js** - Data visualization

### **Development & Testing**
- **pytest 7.4.3** - Testing framework
- **pytest-django 4.7.0** - Django testing utilities

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8 or higher
- pip (Python package manager)
- Git

### **Installation Steps**

1. **Clone the repository**
```bash
git clone https://github.com/TanmaySingh007/DealFlowAI.git
cd DealFlowAI
```

2. **Create virtual environment (recommended)**
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Create .env file
echo "DEBUG=True" > .env
echo "SECRET_KEY=your-secret-key-here" >> .env
```

5. **Run database migrations**
```bash
python manage.py migrate
```

6. **Add sample data**
```bash
python manage.py add_sample_data
python manage.py add_500_companies
python manage.py add_sample_theses
```

7. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

8. **Start the development server**
```bash
python manage.py runserver
```

9. **Access the application**
- **Home Page**: http://127.0.0.1:8000/
- **Thesis Analyzer**: http://127.0.0.1:8000/thesis-analyzer/
- **Dashboard**: http://127.0.0.1:8000/dashboard/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 📖 Usage Guide

### **🎯 Thesis Analyzer**
1. Navigate to the Thesis Analyzer page
2. Choose from 10+ example theses or write your own
3. Click "Analyze Thesis with AI"
4. View extracted criteria and matching companies
5. Get AI recommendations for your investment strategy

### **🤖 AI Chatbot**
1. Click the 🤖 button in the bottom-right corner
2. Ask questions about investment strategies
3. Get real-time AI-powered advice
4. Discuss thesis analysis and company matching

### **🌙 Dark Mode**
1. Click the 🌙 button in the navigation
2. Toggle between light and dark themes
3. All elements adapt seamlessly

### **📊 Dashboard Analytics**
1. View comprehensive statistics
2. Analyze deal status breakdown
3. Explore industry distribution
4. Review recent deals and top companies

## 🔌 API Documentation

### **Core Endpoints**

#### **Thesis Analysis**
```http
POST /api/thesis/analyze/
Content-Type: application/json

{
  "thesis_text": "Investment thesis text here",
  "criteria": ["industry", "stage", "revenue"]
}
```

#### **Company Matching**
```http
GET /api/companies/match/
Parameters:
- thesis_id: int
- limit: int (default: 10)
- min_score: float (default: 0.5)
```

#### **Dashboard Data**
```http
GET /api/dashboard/stats/
GET /api/dashboard/companies/
GET /api/dashboard/deals/
```

### **Response Format**
```json
{
  "success": true,
  "data": {
    "analysis": {
      "criteria": ["industry", "stage"],
      "confidence": 0.85,
      "sentiment": "positive"
    },
    "matches": [
      {
        "company": "Company Name",
        "score": 0.92,
        "reasons": ["industry match", "stage match"]
      }
    ]
  }
}
```

## 🗄️ Database Schema

### **Core Models**

#### **InvestmentThesis**
```python
class InvestmentThesis(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    criteria = models.JSONField()
    analysis_summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### **Company**
```python
class Company(models.Model):
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)
    funding_stage = models.CharField(max_length=50)
    revenue_range = models.CharField(max_length=50)
    description = models.TextField()
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

#### **Deal**
```python
class Deal(models.Model):
    thesis = models.ForeignKey(InvestmentThesis, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    match_score = models.FloatField()
    status = models.CharField(max_length=50)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

## 🤖 AI/ML Services

### **Analysis Service**
- **Text Processing** - Cleans and normalizes thesis text
- **Criteria Extraction** - Identifies investment criteria
- **Sentiment Analysis** - Analyzes thesis sentiment
- **Confidence Scoring** - Provides confidence levels

### **Embedding Service**
- **Sentence Transformers** - Generates semantic embeddings
- **Similarity Calculation** - Computes company-thesis similarity
- **Vector Database** - Stores and retrieves embeddings
- **Real-time Matching** - Fast similarity search

### **Enhanced Analysis Service**
- **Advanced NLP** - Uses transformers for deep analysis
- **Multi-modal Analysis** - Combines multiple AI approaches
- **Recommendation Engine** - Suggests best-fit companies
- **Insight Generation** - Provides investment insights

## 🚀 Deployment

### **Production Setup**

1. **Environment Configuration**
```bash
# Set production environment
export DEBUG=False
export SECRET_KEY=your-production-secret-key
export DATABASE_URL=postgresql://user:pass@host:port/db
```

2. **Static Files**
```bash
python manage.py collectstatic
```

3. **Database Migration**
```bash
python manage.py migrate
```

4. **WSGI Server**
```bash
# Using Gunicorn
pip install gunicorn
gunicorn DealFlowAI.wsgi:application
```

### **Docker Deployment**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "DealFlowAI.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 🏢 Company Database Details

### **Industry Distribution**
- **Technology (50 companies)** - AI, SaaS, Cloud, Cybersecurity
- **Healthcare (40 companies)** - MedTech, Diagnostics, Telemedicine
- **Finance (35 companies)** - FinTech, Banking, Insurance
- **E-commerce (30 companies)** - Retail Tech, Marketplaces
- **Education (25 companies)** - EdTech, Learning Platforms
- **Manufacturing (20 companies)** - Industrial Tech, IoT
- **Real Estate (20 companies)** - PropTech, Construction Tech
- **Transportation (20 companies)** - Mobility, Logistics
- **Energy (15 companies)** - CleanTech, Renewable Energy
- **Gaming (15 companies)** - Game Development, Esports
- **Agriculture (15 companies)** - AgTech, Food Technology
- **Other Sectors (215 companies)** - Various emerging technologies

### **Funding Stages**
- **Seed Stage** - 150 companies
- **Series A** - 120 companies
- **Series B** - 100 companies
- **Series C** - 80 companies
- **Series D+** - 50 companies

### **Revenue Ranges**
- **$1M - $5M ARR** - 200 companies
- **$5M - $10M ARR** - 150 companies
- **$10M - $25M ARR** - 100 companies
- **$25M - $50M ARR** - 30 companies
- **$50M+ ARR** - 20 companies

## 📋 Investment Thesis Examples

### **Industry-Specific Theses**
1. **Healthcare AI & Diagnostics**
   - Focus on AI-powered medical diagnostics
   - Early-stage companies with FDA clearance
   - $5M-$25M ARR range

2. **FinTech Solutions**
   - Digital banking and payment platforms
   - Series A-B companies with strong growth
   - $10M-$50M ARR range

3. **E-commerce Technology**
   - B2B e-commerce platforms
   - SaaS companies with recurring revenue
   - $5M-$25M ARR range

4. **EdTech Innovation**
   - Online learning platforms
   - Companies with proven user engagement
   - $1M-$10M ARR range

### **Investment Criteria Examples**
- **Early Stage Focus** - Seed to Series A companies
- **Growth Stage Focus** - Series B-C companies
- **Revenue Range Focus** - Specific ARR targets
- **Industry Agnostic** - Technology-first approach

## 🔧 Configuration

### **Environment Variables**
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### **ML Model Configuration**
The AI models are automatically downloaded on first use:
- **Sentence Transformers**: `all-MiniLM-L6-v2`
- **Hugging Face Models**: Auto-downloaded as needed
- **spaCy Models**: `en_core_web_sm`

### **Database Configuration**
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## 📁 Project Structure

```
DealFlowAI/
├── DealFlowAI/                    # Django project settings
│   ├── __init__.py
│   ├── settings.py               # Project configuration
│   ├── urls.py                   # Main URL routing
│   ├── asgi.py                   # ASGI configuration
│   └── wsgi.py                   # WSGI configuration
├── deals/                        # Main application
│   ├── __init__.py
│   ├── models.py                 # Database models
│   ├── views.py                  # API endpoints and views
│   ├── urls.py                   # URL routing
│   ├── serializers.py            # DRF serializers
│   ├── admin.py                  # Admin interface
│   ├── apps.py                   # App configuration
│   ├── tests.py                  # Test cases
│   └── management/               # Custom commands
│       └── commands/
│           ├── add_sample_data.py
│           ├── add_500_companies.py
│           └── add_sample_theses.py
├── ml_services/                  # AI/ML services
│   ├── __init__.py
│   ├── analysis_service.py       # Core analysis logic
│   ├── embedding_service.py      # Embedding generation
│   ├── enhanced_analysis_service.py
│   └── advanced_analytics_service.py
├── static/                       # Static files
│   ├── css/                      # Stylesheets
│   ├── js/                       # JavaScript files
│   └── images/                   # Images and icons
├── templates/                    # HTML templates
│   ├── deals/                    # App-specific templates
│   │   ├── dashboard.html
│   │   ├── home.html
│   │   ├── thesis_analyzer.html
│   │   └── thesis_details.html
│   └── test_api.html
├── logs/                         # Application logs
├── staticfiles/                  # Collected static files
├── requirements.txt              # Python dependencies
├── manage.py                     # Django management
├── test_server.py               # Test server script
├── thesis_examples.md           # Thesis examples
└── README.md                    # This file
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
   ```bash
   git clone https://github.com/TanmaySingh007/DealFlowAI.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes**
   - Follow PEP 8 style guidelines
   - Add tests for new features
   - Update documentation

4. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```

5. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **Open a Pull Request**
   - Provide a clear description
   - Include screenshots if UI changes
   - Reference any related issues

### **Development Guidelines**
- **Code Style**: Follow PEP 8 and Django conventions
- **Testing**: Write tests for new features
- **Documentation**: Update README and docstrings
- **Commits**: Use conventional commit messages

## 🐛 Known Issues & Limitations

### **Current Limitations**
- **Model Size**: Large ML models may take time to download
- **Memory Usage**: High memory usage with large datasets
- **API Rate Limits**: Some external APIs have rate limits

### **Planned Improvements**
- **Performance**: Optimize database queries
- **Scalability**: Add caching and load balancing
- **Features**: Add more AI models and analysis types
- **UI/UX**: Enhanced mobile experience

## 📞 Support

### **Getting Help**
- **Documentation**: Check this README first
- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions
- **Email**: [your-email@example.com]

### **Bug Reports**
When reporting bugs, please include:
- **Environment**: OS, Python version, Django version
- **Steps**: Detailed reproduction steps
- **Expected vs Actual**: What you expected vs what happened
- **Screenshots**: If applicable

### **Feature Requests**
We welcome feature requests! Please:
- **Describe the feature** clearly
- **Explain the use case**
- **Provide examples** if possible
- **Consider implementation** complexity

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Django** - Web framework
- **Hugging Face** - Transformers library
- **Sentence Transformers** - Embedding models
- **Modern CSS** - Glassmorphism and 3D effects
- **Open Source Community** - All contributors and maintainers

## 📊 Project Statistics

- **Lines of Code**: 15,000+
- **Companies in Database**: 500+
- **Investment Theses**: 10+ examples
- **AI Models**: 5+ integrated
- **API Endpoints**: 15+
- **Test Coverage**: 80%+

---

**Built with ❤️ by [Tanmay Singh](https://github.com/TanmaySingh007)**

*DealFlowAI - Transforming Investment Analysis with AI* 

[![GitHub stars](https://img.shields.io/github/stars/TanmaySingh007/DealFlowAI)](https://github.com/TanmaySingh007/DealFlowAI/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/TanmaySingh007/DealFlowAI)](https://github.com/TanmaySingh007/DealFlowAI/network)
[![GitHub issues](https://img.shields.io/github/issues/TanmaySingh007/DealFlowAI)](https://github.com/TanmaySingh007/DealFlowAI/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/TanmaySingh007/DealFlowAI)](https://github.com/TanmaySingh007/DealFlowAI/pulls) 