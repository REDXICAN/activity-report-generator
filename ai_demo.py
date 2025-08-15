#!/usr/bin/env python3
"""
AI-Powered Activity Report Generator Demo
Demonstrates the AI analysis capabilities
"""

from datetime import datetime, timedelta
from ai_analyzer import AIAnalyzer
from oauth_manager import OAuthManager
import json

def demo_ai_analysis():
    """Demo the AI analysis capabilities"""
    print("🤖 AI-Powered Activity Report Generator Demo")
    print("=" * 60)
    
    # Initialize AI analyzer
    ai_analyzer = AIAnalyzer()
    
    # Create sample data for demonstration
    sample_data = create_sample_data()
    
    print("\n📧 EMAIL AI ANALYSIS")
    print("-" * 30)
    email_analysis = ai_analyzer.analyze_emails(sample_data['emails'])
    
    print(f"Total emails analyzed: {email_analysis['total_emails']}")
    print(f"Sentiment distribution: {email_analysis['sentiment_analysis']}")
    print(f"Urgency levels: {email_analysis['urgency_levels']}")
    print(f"Top categories: {list(email_analysis['categories'].keys())[:3]}")
    print(f"Key insights: {len(email_analysis['insights'])} insights generated")
    
    print("\n🐙 GITHUB AI ANALYSIS")
    print("-" * 30)
    github_analysis = ai_analyzer.analyze_github_activities(sample_data['github'])
    
    print(f"Productivity score: {github_analysis['productivity_score']}%")
    print(f"Code quality indicators: {github_analysis['code_quality_indicators']['commit_frequency']} commits")
    print(f"Project focus: {len(github_analysis['project_focus'])} repositories")
    print(f"Technical insights: {len(github_analysis['technical_insights'])} insights")
    print(f"Recommendations: {len(github_analysis['recommendations'])} suggestions")
    
    print("\n💬 WHATSAPP AI ANALYSIS")
    print("-" * 30)
    whatsapp_analysis = ai_analyzer.analyze_whatsapp_conversations(sample_data['whatsapp'])
    
    satisfaction = whatsapp_analysis['customer_satisfaction']
    print(f"Overall satisfaction: {satisfaction['overall_satisfaction']}")
    print(f"Satisfaction rate: {satisfaction['satisfaction_rate']:.1f}%")
    print(f"Response efficiency: {whatsapp_analysis['response_efficiency']['response_efficiency']}")
    print(f"Common issues: {len(whatsapp_analysis['common_issues'])} issue types identified")
    print(f"Improvement suggestions: {len(whatsapp_analysis['improvement_suggestions'])} recommendations")
    
    print("\n🧠 COMPREHENSIVE AI REPORT")
    print("-" * 30)
    
    # Add AI analysis to data
    sample_data['emails']['ai_analysis'] = email_analysis
    sample_data['github']['ai_analysis'] = github_analysis
    sample_data['whatsapp']['ai_analysis'] = whatsapp_analysis
    
    comprehensive_report = ai_analyzer.generate_comprehensive_report(sample_data)
    
    print("📊 EXECUTIVE SUMMARY:")
    print(f"   {comprehensive_report['executive_summary']}")
    
    print(f"\n🏆 PERFORMANCE METRICS:")
    metrics = comprehensive_report['performance_metrics']
    print(f"   Overall Score: {metrics['overall_performance_score']:.1f}%")
    print(f"   Performance Grade: {metrics['performance_grade']}")
    print(f"   Category Scores:")
    for category, score in metrics['category_scores'].items():
        print(f"     - {category.title()}: {score:.1f}%")
    
    print(f"\n🎯 KEY ACHIEVEMENTS ({len(comprehensive_report['key_achievements'])}):")
    for i, achievement in enumerate(comprehensive_report['key_achievements'][:3], 1):
        print(f"   {i}. {achievement}")
    
    print(f"\n📈 STRATEGIC RECOMMENDATIONS ({len(comprehensive_report['strategic_recommendations'])}):")
    for i, recommendation in enumerate(comprehensive_report['strategic_recommendations'][:3], 1):
        print(f"   {i}. {recommendation}")
    
    print(f"\n💡 AREAS FOR IMPROVEMENT ({len(comprehensive_report['areas_for_improvement'])}):")
    for i, improvement in enumerate(comprehensive_report['areas_for_improvement'][:3], 1):
        print(f"   {i}. {improvement}")

def demo_oauth_manager():
    """Demo OAuth capabilities"""
    print("\n🔐 OAUTH MANAGER DEMO")
    print("-" * 30)
    
    oauth_manager = OAuthManager()
    
    # Get OAuth URLs
    urls = oauth_manager.get_oauth_urls()
    print("Available OAuth configurations:")
    for service, url in urls.items():
        status = "✅ Available" if url else "❌ Not configured"
        print(f"  {service.capitalize()}: {status}")
    
    # Test connections
    connections = oauth_manager.test_connections()
    print("\nConnection Status:")
    for service, result in connections.items():
        status_icon = "✅" if result['status'] == 'success' else "❌" if result['status'] == 'error' else "⚠️"
        print(f"  {status_icon} {service.capitalize()}: {result['message']}")

def create_sample_data():
    """Create sample data for demonstration"""
    return {
        'emails': {
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
                },
                {
                    'subject': 'Meeting follow-up and action items',
                    'body': 'Great discussion today. Here are the action items we discussed.',
                    'to': 'stakeholders@company.com',
                    'datetime': datetime.now() - timedelta(days=3)
                }
            ],
            'received': [
                {
                    'subject': 'Code review feedback',
                    'body': 'Excellent work on the implementation. Just minor suggestions.',
                    'from': 'reviewer@company.com',
                    'datetime': datetime.now() - timedelta(days=1)
                },
                {
                    'subject': 'Thank you for the quick support',
                    'body': 'Thank you for resolving the issue so quickly. Great service!',
                    'from': 'client@customer.com',
                    'datetime': datetime.now() - timedelta(days=2)
                }
            ]
        },
        'github': {
            'commits': [
                {
                    'repo': 'activity-tracker',
                    'message': 'Add new feature for automated reporting',
                    'date': datetime.now() - timedelta(days=1),
                    'additions': 150,
                    'deletions': 25,
                    'files_changed': 5
                },
                {
                    'repo': 'activity-tracker',
                    'message': 'Fix bug in data collection module',
                    'date': datetime.now() - timedelta(days=2),
                    'additions': 45,
                    'deletions': 12,
                    'files_changed': 2
                },
                {
                    'repo': 'client-portal',
                    'message': 'Implement user authentication',
                    'date': datetime.now() - timedelta(days=3),
                    'additions': 200,
                    'deletions': 0,
                    'files_changed': 8
                }
            ],
            'pull_requests': [
                {
                    'repo': 'activity-tracker',
                    'title': 'Add automated reporting feature',
                    'state': 'merged',
                    'merged': True,
                    'created_at': datetime.now() - timedelta(days=2)
                }
            ],
            'issues': [
                {
                    'repo': 'activity-tracker',
                    'title': 'Improve data collection performance',
                    'state': 'closed',
                    'created_at': datetime.now() - timedelta(days=4)
                }
            ],
            'stats': {
                'total_commits': 3,
                'total_prs': 1,
                'merged_prs': 1,
                'total_additions': 395,
                'total_deletions': 37,
                'total_files_changed': 15,
                'repos_worked_on': 2
            }
        },
        'whatsapp': {
            'conversations': [
                {
                    'customer': '+1234567890',
                    'start_time': datetime.now() - timedelta(days=1),
                    'end_time': datetime.now() - timedelta(days=1, hours=-2),
                    'message_count': 8,
                    'topics': ['technical_support'],
                    'messages': [
                        {'message': 'Hi, I need help with installation', 'datetime': datetime.now() - timedelta(days=1)},
                        {'message': 'Thank you for the help, it works perfectly now!', 'datetime': datetime.now() - timedelta(days=1, hours=-1)}
                    ]
                },
                {
                    'customer': '+0987654321',
                    'start_time': datetime.now() - timedelta(days=2),
                    'end_time': datetime.now() - timedelta(days=2, hours=-1),
                    'message_count': 5,
                    'topics': ['billing'],
                    'messages': [
                        {'message': 'Question about my invoice', 'datetime': datetime.now() - timedelta(days=2)},
                        {'message': 'Great, that clarifies everything. Thanks!', 'datetime': datetime.now() - timedelta(days=2, hours=-1)}
                    ]
                }
            ],
            'unique_customers': 2,
            'total_messages': 13
        }
    }

if __name__ == "__main__":
    demo_ai_analysis()
    demo_oauth_manager()
    
    print("\n" + "=" * 60)
    print("🎉 Demo completed! The AI system is ready to analyze your real data.")
    print("💡 Run 'python gui_app.py' to use the full application with GUI.")
    print("🔗 GitHub: https://github.com/REDXICAN/activity-report-generator")