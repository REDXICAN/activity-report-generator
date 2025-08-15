# Activity Report Generator - TurboAir

🤖 **AI-Powered** automated tool for generating intelligent activity reports from multiple sources including Email, GitHub, and WhatsApp Business.

## ✨ Features

- **🧠 AI-Powered Analysis**: Intelligent data processing with insights and recommendations
- **🔐 OAuth Integration**: Automated account access with secure authentication
- **📧 Email Intelligence**: Gmail integration with sentiment analysis and categorization
- **🐙 GitHub Analytics**: Development productivity scoring and code quality analysis
- **💬 WhatsApp Insights**: Customer satisfaction analysis and support metrics
- **📊 Smart Reporting**: Generates Excel and Word reports with AI insights
- **🎯 Performance Metrics**: Overall scoring, grading, and strategic recommendations
- **🖥️ GUI Interface**: Easy-to-use graphical interface for configuration

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

### 1. Gmail API Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Gmail API
4. Create credentials (OAuth 2.0 Client ID)
5. Download credentials as `credentials.json`
6. Place in project folder

### 2. GitHub Token
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate new token with `repo` scope
3. Copy token for use in application

### 3. WhatsApp Export
1. Export WhatsApp Business chats as text files
2. Place in a folder for the tool to access

## Usage

### 🎮 GUI Mode (Recommended)
```bash
python gui_app.py
```

### 🤖 AI Demo (See capabilities)
```bash
python simple_demo.py
```

### 💻 Command Line Mode
```bash
python main.py
```

## Configuration

The tool uses a `.env` file for configuration. You can either:
- Configure through the GUI (recommended)
- Edit `.env` file directly (see `.env.example`)

## Output

Reports are generated in:
- **Excel format**: Detailed multi-sheet workbook
- **Word format**: Formatted document ready for distribution

Default output location: `O:\OneDrive\Documentos\-- TurboAir\-- Reportes de Actividad\`

## 📋 Report Structure

- **🧠 AI Executive Summary**: Intelligent overview with key insights
- **📊 Performance Dashboard**: Scores, grades, and metrics
- **📧 Email Analysis**: Sentiment analysis, categorization, urgency levels
- **🐙 GitHub Analytics**: Productivity scoring, code quality, technical insights
- **💬 WhatsApp Intelligence**: Customer satisfaction, response efficiency
- **🎯 Strategic Recommendations**: AI-generated improvement suggestions
- **📈 Detailed Activities**: Chronological list with AI categorization

## 🤖 AI Capabilities

- **Sentiment Analysis**: Automatically categorizes email tone and urgency
- **Productivity Scoring**: Calculates development productivity with actionable insights
- **Customer Satisfaction**: Analyzes support conversations for satisfaction metrics
- **Performance Grading**: Overall performance scoring with letter grades (A+ to D)
- **Strategic Insights**: AI-generated recommendations for improvement
- **Pattern Recognition**: Identifies trends and patterns across all data sources
- **Automated Categorization**: Smart classification of activities and communications

## 🚀 Quick Start

1. **Clone and setup:**
   ```bash
   git clone https://github.com/REDXICAN/activity-report-generator.git
   cd activity-report-generator
   pip install -r requirements.txt
   ```

2. **Try the AI demo:**
   ```bash
   python simple_demo.py
   ```

3. **Run the full application:**
   ```bash
   python gui_app.py
   ```