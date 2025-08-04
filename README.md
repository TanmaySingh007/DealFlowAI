# 🚀 DealFlowAI - AI-Powered Investment Thesis Analyzer

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Overview

DealFlowAI is a comprehensive AI-powered platform for analyzing investment theses and matching them with relevant companies. Built with Django and modern machine learning frameworks, it provides intelligent insights for investment decision-making.

## ✨ Features

### 🤖 **AI-Powered Analysis**
- **Advanced Thesis Analysis** - AI extracts key criteria from investment theses
- **Smart Company Matching** - Intelligent similarity scoring and fit analysis
- **Interactive AI Chatbot** - Real-time investment advice and insights
- **Comprehensive Database** - 100+ companies across diverse industries

### 🎨 **Modern UI/UX**
- **Dark Mode Support** - Toggle between light and dark themes
- **3D Visual Effects** - Glassmorphism design with 3D animations
- **Responsive Design** - Works perfectly on all devices
- **Interactive Elements** - Hover effects and smooth animations

### 📊 **Comprehensive Dashboard**
- **Real-time Analytics** - Thesis-based statistics and insights
- **Data Visualization** - Charts, tables, and progress indicators
- **Company Database** - Detailed information on 100+ companies
- **Deal Tracking** - Status management and fit scoring

### 🏢 **Diverse Company Database**
- **15+ Industries** - Technology, Healthcare, FinTech, EdTech, Manufacturing, etc.
- **Multiple Funding Stages** - Seed, Series A, B, C across all sectors
- **Revenue Ranges** - $1M to $200M+ across different company sizes
- **Detailed Profiles** - Industry, funding stage, revenue, and descriptions

## 🛠️ Technology Stack

### **Backend**
- **Django 4.2+** - Web framework
- **Django REST Framework** - API development
- **SQLite** - Database (easily configurable for PostgreSQL/MySQL)

### **AI/ML**
- **Hugging Face Transformers** - Advanced NLP models
- **Sentence Transformers** - Semantic similarity and embeddings
- **spaCy & NLTK** - Natural language processing
- **TextBlob** - Sentiment analysis

### **Frontend**
- **HTML5/CSS3** - Modern responsive design
- **JavaScript (ES6+)** - Interactive functionality
- **CSS3 Animations** - 3D effects and smooth transitions
- **Glassmorphism Design** - Modern UI patterns

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+
- pip (Python package manager)

### **Installation**

1. **Clone the repository**
```bash
git clone https://github.com/TanmaySingh007/DealFlowAI.git
cd DealFlowAI
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run migrations**
```bash
python manage.py migrate
```

4. **Add sample data**
```bash
python manage.py add_sample_data
```

5. **Start the development server**
```bash
python manage.py runserver 127.0.0.1:8000
```

6. **Access the application**
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

## 🏢 Company Database

The platform includes 100+ companies across diverse sectors:

### **Technology (10 companies)**
- AI-powered workflow automation
- Cloud synchronization solutions
- Data visualization platforms
- Cybersecurity systems
- Mobile-first SaaS applications

### **Healthcare (10 companies)**
- Medical device technology
- AI-powered diagnostics
- Telemedicine platforms
- Mental health technology
- Genomic data analysis

### **Finance (10 companies)**
- Digital banking solutions
- Cryptocurrency trading platforms
- AI-powered insurance
- Wealth management tools
- Fraud detection systems

### **Additional Sectors (70+ companies)**
- E-commerce & Retail Technology
- Education Technology (EdTech)
- Manufacturing & Industrial Tech
- Real Estate Technology (PropTech)
- Transportation & Mobility
- Energy & Sustainability
- Gaming & Entertainment
- Agriculture & Food Technology
- And many more...

## 📋 Investment Thesis Examples

The platform includes comprehensive examples covering:

### **Industry-Specific Theses**
- Healthcare AI & Diagnostics
- FinTech Solutions
- E-commerce Technology
- EdTech Innovation
- Manufacturing AI
- PropTech Solutions
- Transportation Technology
- Energy Innovation
- Gaming & Entertainment
- AgTech & Food Technology

### **Investment Criteria Examples**
- Early Stage Focus (Seed to Series A)
- Growth Stage Focus (Series B-C)
- Revenue Range Focus ($1M-$10M ARR)
- Industry Agnostic Strategies

## 🔧 Configuration

### **Environment Variables**
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

### **ML Model Configuration**
The AI models are automatically downloaded on first use:
- **Sentence Transformers**: `all-MiniLM-L6-v2`
- **Hugging Face Models**: Auto-downloaded as needed

## 📁 Project Structure

```
DealFlowAI/
├── DealFlowAI/          # Django project settings
├── deals/              # Main application
│   ├── models.py       # Database models
│   ├── views.py        # API endpoints and views
│   ├── urls.py         # URL routing
│   └── templates/      # HTML templates
├── ml_services/        # AI/ML services
│   ├── analysis_service.py
│   ├── embedding_service.py
│   └── enhanced_analysis_service.py
├── static/             # Static files
├── templates/          # Base templates
├── requirements.txt    # Python dependencies
├── manage.py          # Django management
└── README.md          # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Django** - Web framework
- **Hugging Face** - Transformers library
- **Sentence Transformers** - Embedding models
- **Modern CSS** - Glassmorphism and 3D effects

## 📞 Support

For support, email [your-email@example.com] or create an issue in the repository.

---

**Built with ❤️ by Tanmay Singh**

*DealFlowAI - Transforming Investment Analysis with AI* 