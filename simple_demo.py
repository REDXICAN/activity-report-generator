#!/usr/bin/env python3
"""
AI-Powered Activity Report Generator Demo
"""

from datetime import datetime, timedelta
from ai_analyzer import AIAnalyzer
import json

def demo_ai_analysis():
    """Demo the AI analysis capabilities"""
    print("AI-Powered Activity Report Generator Demo")
    print("=" * 60)
    
    # Initialize AI analyzer
    ai_analyzer = AIAnalyzer()
    
    # Create sample data
    sample_emails = {
        'sent': [
            {
                'subject': 'Project completion update',
                'body': 'Successfully completed the feature implementation. All tests passed.',
                'to': 'team@company.com',
                'datetime': datetime.now() - timedelta(days=1)
            },
            {
                'subject': 'Urgent: Client issue needs immediate attention',
                'body': 'Critical bug reported by client. Need to fix this ASAP.',
                'to': 'support@company.com',
                'datetime': datetime.now() - timedelta(days=2)
            }
        ],
        'received': [
            {
                'subject': 'Code review feedback',
                'body': 'Excellent work on the implementation. Just minor suggestions.',
                'from': 'reviewer@company.com',
                'datetime': datetime.now() - timedelta(days=1)
            }
        ]
    }
    
    sample_github = {
        'commits': [
            {
                'repo': 'activity-tracker',
                'message': 'Add new feature for automated reporting',
                'date': datetime.now() - timedelta(days=1),
                'additions': 150,
                'deletions': 25,
                'files_changed': 5
            }
        ],
        'pull_requests': [],
        'issues': [],
        'stats': {
            'total_commits': 1,
            'total_prs': 0,
            'merged_prs': 0,
            'total_additions': 150,
            'total_deletions': 25
        }
    }
    
    print("\nEMAIL AI ANALYSIS")
    print("-" * 30)
    email_analysis = ai_analyzer.analyze_emails(sample_emails)
    
    print(f"Total emails analyzed: {email_analysis['total_emails']}")
    print(f"Categories found: {list(email_analysis['categories'].keys())}")
    print(f"Sentiment analysis: {email_analysis['sentiment_analysis']}")
    print(f"Urgency levels: {email_analysis['urgency_levels']}")
    print(f"Key insights generated: {len(email_analysis['insights'])}")
    
    for insight in email_analysis['insights'][:2]:
        print(f"  - {insight}")
    
    print("\nGITHUB AI ANALYSIS")
    print("-" * 30)
    github_analysis = ai_analyzer.analyze_github_activities(sample_github)
    
    print(f"Productivity score: {github_analysis['productivity_score']}%")
    print(f"Code quality score: {github_analysis['code_quality_indicators']['commit_message_quality']:.1f}%")
    print(f"Technical insights: {len(github_analysis['technical_insights'])}")
    
    for insight in github_analysis['technical_insights'][:2]:
        print(f"  - {insight}")
    
    print("\nCOMPREHENSIVE AI REPORT")
    print("-" * 30)
    
    # Combine data for comprehensive analysis
    combined_data = {
        'emails': {'ai_analysis': email_analysis},
        'github': {'ai_analysis': github_analysis},
        'whatsapp': {'ai_analysis': {'customer_satisfaction': {'satisfaction_rate': 85}}}
    }
    
    comprehensive = ai_analyzer.generate_comprehensive_report(combined_data)
    
    print("EXECUTIVE SUMMARY:")
    print(f"  {comprehensive['executive_summary']}")
    
    print(f"\nPERFORMANCE METRICS:")
    metrics = comprehensive['performance_metrics']
    print(f"  Overall Score: {metrics['overall_performance_score']:.1f}%")
    print(f"  Performance Grade: {metrics['performance_grade']}")
    
    print(f"\nKEY ACHIEVEMENTS:")
    for achievement in comprehensive['key_achievements'][:2]:
        print(f"  - {achievement}")
    
    print(f"\nSTRATEGIC RECOMMENDATIONS:")
    for rec in comprehensive['strategic_recommendations'][:2]:
        print(f"  - {rec}")
    
    print("\n" + "=" * 60)
    print("AI Demo completed successfully!")
    print("The system can analyze your real email, GitHub, and WhatsApp data")
    print("to provide intelligent insights and comprehensive reports.")

if __name__ == "__main__":
    demo_ai_analysis()