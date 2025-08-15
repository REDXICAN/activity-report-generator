# Activity Report Generator - TurboAir

Automated tool for generating activity reports from multiple sources including Email, GitHub, and WhatsApp Business.

## Features

- **Email Integration**: Collects sent/received emails from Gmail
- **GitHub Integration**: Tracks commits, PRs, issues, and repository activities
- **WhatsApp Business**: Analyzes customer support conversations
- **Automated Report Generation**: Creates formatted Excel and Word documents
- **GUI Interface**: Easy-to-use graphical interface for configuration

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

### GUI Mode (Recommended)
```bash
python gui_app.py
```

### Command Line Mode
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

## Report Structure

- **Summary**: Overview of activities
- **Emails**: Sent/received email details
- **GitHub**: Development activities
- **WhatsApp**: Customer support interactions
- **Detailed Activities**: Chronological list of all activities