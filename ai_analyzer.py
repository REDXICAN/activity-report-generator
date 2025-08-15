import re
import json
from datetime import datetime
from collections import Counter
import pandas as pd
from typing import Dict, List, Any

class AIAnalyzer:
    def __init__(self):
        self.keywords = {
            'productivity': ['completed', 'finished', 'delivered', 'implemented', 'fixed', 'resolved', 'deployed'],
            'communication': ['meeting', 'call', 'discussion', 'presentation', 'review', 'feedback'],
            'development': ['code', 'bug', 'feature', 'commit', 'merge', 'deploy', 'test', 'debug'],
            'support': ['help', 'assist', 'support', 'issue', 'problem', 'question', 'solution'],
            'planning': ['plan', 'schedule', 'roadmap', 'strategy', 'goal', 'objective', 'milestone'],
            'client_work': ['client', 'customer', 'user', 'requirement', 'specification', 'delivery']
        }
        
        self.urgency_indicators = ['urgent', 'asap', 'immediate', 'critical', 'emergency', 'priority']
        self.positive_indicators = ['success', 'completed', 'approved', 'good', 'excellent', 'perfect']
        self.negative_indicators = ['failed', 'error', 'problem', 'issue', 'bug', 'delayed']
    
    def analyze_emails(self, email_data):
        """AI-powered email analysis"""
        analysis = {
            'total_emails': 0,
            'categories': {},
            'sentiment_analysis': {'positive': 0, 'negative': 0, 'neutral': 0},
            'urgency_levels': {'high': 0, 'medium': 0, 'low': 0},
            'productivity_metrics': {},
            'key_topics': [],
            'communication_patterns': {},
            'insights': []
        }
        
        all_emails = email_data.get('sent', []) + email_data.get('received', [])
        analysis['total_emails'] = len(all_emails)
        
        # Analyze each email
        topics = []
        sentiments = []
        urgencies = []
        
        for email in all_emails:
            subject = email.get('subject', '').lower()
            body = email.get('body', '').lower()
            content = f"{subject} {body}"
            
            # Category analysis
            category = self._categorize_content(content)
            analysis['categories'][category] = analysis['categories'].get(category, 0) + 1
            
            # Sentiment analysis
            sentiment = self._analyze_sentiment(content)
            analysis['sentiment_analysis'][sentiment] += 1
            sentiments.append(sentiment)
            
            # Urgency analysis
            urgency = self._analyze_urgency(content)
            analysis['urgency_levels'][urgency] += 1
            urgencies.append(urgency)
            
            # Extract topics
            topics.extend(self._extract_topics(content))
        
        # Key topics analysis
        topic_counter = Counter(topics)
        analysis['key_topics'] = topic_counter.most_common(10)
        
        # Communication patterns
        analysis['communication_patterns'] = self._analyze_communication_patterns(all_emails)
        
        # Generate insights
        analysis['insights'] = self._generate_email_insights(analysis, all_emails)
        
        return analysis
    
    def analyze_github_activities(self, github_data):
        """AI-powered GitHub activity analysis"""
        analysis = {
            'productivity_score': 0,
            'code_quality_indicators': {},
            'development_patterns': {},
            'project_focus': [],
            'collaboration_metrics': {},
            'technical_insights': [],
            'recommendations': []
        }
        
        commits = github_data.get('commits', [])
        prs = github_data.get('pull_requests', [])
        issues = github_data.get('issues', [])
        
        # Productivity analysis
        analysis['productivity_score'] = self._calculate_productivity_score(commits, prs, issues)
        
        # Code quality analysis
        analysis['code_quality_indicators'] = self._analyze_code_quality(commits)
        
        # Development patterns
        analysis['development_patterns'] = self._analyze_development_patterns(commits, prs)
        
        # Project focus analysis
        analysis['project_focus'] = self._analyze_project_focus(commits, prs, issues)
        
        # Collaboration metrics
        analysis['collaboration_metrics'] = self._analyze_collaboration(prs, issues)
        
        # Generate technical insights
        analysis['technical_insights'] = self._generate_technical_insights(github_data)
        
        # Generate recommendations
        analysis['recommendations'] = self._generate_github_recommendations(analysis)
        
        return analysis
    
    def analyze_whatsapp_conversations(self, whatsapp_data):
        """AI-powered WhatsApp conversation analysis"""
        analysis = {
            'customer_satisfaction': {},
            'response_efficiency': {},
            'common_issues': [],
            'support_quality': {},
            'conversation_insights': [],
            'improvement_suggestions': []
        }
        
        conversations = whatsapp_data.get('conversations', [])
        
        # Analyze each conversation
        issue_types = []
        response_times = []
        satisfaction_indicators = []
        
        for conv in conversations:
            # Analyze conversation content
            messages = conv.get('messages', [])
            if not messages:
                continue
            
            # Extract issue types
            conv_content = ' '.join([msg.get('message', '') for msg in messages])
            issues = self._extract_customer_issues(conv_content)
            issue_types.extend(issues)
            
            # Analyze response efficiency
            response_metrics = self._analyze_response_time(conv)
            response_times.append(response_metrics)
            
            # Customer satisfaction indicators
            satisfaction = self._analyze_customer_satisfaction(messages)
            satisfaction_indicators.append(satisfaction)
        
        # Compile analysis
        analysis['common_issues'] = Counter(issue_types).most_common(10)
        analysis['response_efficiency'] = self._compile_response_metrics(response_times)
        analysis['customer_satisfaction'] = self._compile_satisfaction_metrics(satisfaction_indicators)
        analysis['conversation_insights'] = self._generate_conversation_insights(conversations)
        analysis['improvement_suggestions'] = self._generate_support_recommendations(analysis)
        
        return analysis
    
    def generate_comprehensive_report(self, all_data):
        """Generate AI-powered comprehensive report with insights"""
        report = {
            'executive_summary': '',
            'key_achievements': [],
            'productivity_analysis': {},
            'communication_effectiveness': {},
            'technical_contributions': {},
            'customer_service_excellence': {},
            'areas_for_improvement': [],
            'strategic_recommendations': [],
            'performance_metrics': {}
        }
        
        # Generate executive summary
        report['executive_summary'] = self._generate_executive_summary(all_data)
        
        # Key achievements
        report['key_achievements'] = self._identify_key_achievements(all_data)
        
        # Productivity analysis
        report['productivity_analysis'] = self._analyze_overall_productivity(all_data)
        
        # Communication effectiveness
        report['communication_effectiveness'] = self._analyze_communication_effectiveness(all_data)
        
        # Technical contributions
        report['technical_contributions'] = self._analyze_technical_contributions(all_data)
        
        # Customer service excellence
        report['customer_service_excellence'] = self._analyze_customer_service(all_data)
        
        # Areas for improvement
        report['areas_for_improvement'] = self._identify_improvement_areas(all_data)
        
        # Strategic recommendations
        report['strategic_recommendations'] = self._generate_strategic_recommendations(all_data)
        
        # Performance metrics
        report['performance_metrics'] = self._calculate_performance_metrics(all_data)
        
        return report
    
    def _categorize_content(self, content):
        """Categorize content using AI-like keyword matching"""
        scores = {}
        for category, keywords in self.keywords.items():
            score = sum(1 for keyword in keywords if keyword in content)
            scores[category] = score
        
        if not scores or max(scores.values()) == 0:
            return 'general'
        
        return max(scores, key=scores.get)
    
    def _analyze_sentiment(self, content):
        """Simple sentiment analysis"""
        positive_count = sum(1 for word in self.positive_indicators if word in content)
        negative_count = sum(1 for word in self.negative_indicators if word in content)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _analyze_urgency(self, content):
        """Analyze urgency level"""
        urgency_count = sum(1 for word in self.urgency_indicators if word in content)
        
        if urgency_count >= 2:
            return 'high'
        elif urgency_count == 1:
            return 'medium'
        else:
            return 'low'
    
    def _extract_topics(self, content):
        """Extract key topics from content"""
        # Simple topic extraction using keywords
        topics = []
        for category, keywords in self.keywords.items():
            if any(keyword in content for keyword in keywords):
                topics.append(category)
        return topics
    
    def _analyze_communication_patterns(self, emails):
        """Analyze email communication patterns"""
        patterns = {
            'peak_hours': {},
            'response_rate': 0,
            'average_length': 0,
            'formal_vs_informal': {'formal': 0, 'informal': 0}
        }
        
        # Analyze timing patterns
        hours = []
        for email in emails:
            if email.get('datetime'):
                try:
                    if isinstance(email['datetime'], str):
                        dt = datetime.fromisoformat(email['datetime'].replace('Z', '+00:00'))
                    else:
                        dt = email['datetime']
                    hours.append(dt.hour)
                except:
                    continue
        
        if hours:
            hour_counter = Counter(hours)
            patterns['peak_hours'] = dict(hour_counter.most_common(5))
        
        return patterns
    
    def _generate_email_insights(self, analysis, emails):
        """Generate insights from email analysis"""
        insights = []
        
        # Productivity insights
        if analysis['categories'].get('productivity', 0) > len(emails) * 0.3:
            insights.append("High productivity focus in email communications")
        
        # Urgency insights
        if analysis['urgency_levels']['high'] > len(emails) * 0.2:
            insights.append("Significant number of urgent communications - consider workload optimization")
        
        # Sentiment insights
        positive_ratio = analysis['sentiment_analysis']['positive'] / max(len(emails), 1)
        if positive_ratio > 0.6:
            insights.append("Predominantly positive communication tone")
        elif positive_ratio < 0.3:
            insights.append("Consider improving communication positivity")
        
        return insights
    
    def _calculate_productivity_score(self, commits, prs, issues):
        """Calculate overall productivity score"""
        commit_score = min(len(commits) * 2, 40)  # Max 40 points
        pr_score = min(len(prs) * 5, 30)  # Max 30 points
        issue_score = min(len(issues) * 3, 30)  # Max 30 points
        
        total_score = commit_score + pr_score + issue_score
        return min(total_score, 100)
    
    def _analyze_code_quality(self, commits):
        """Analyze code quality indicators"""
        quality_indicators = {
            'commit_frequency': len(commits),
            'average_files_per_commit': 0,
            'commit_message_quality': 0,
            'code_change_distribution': {}
        }
        
        if commits:
            total_files = sum(commit.get('files_changed', 0) for commit in commits)
            quality_indicators['average_files_per_commit'] = total_files / len(commits)
            
            # Analyze commit messages
            good_messages = 0
            for commit in commits:
                message = commit.get('message', '')
                if len(message) > 10 and any(word in message.lower() for word in ['fix', 'add', 'update', 'implement']):
                    good_messages += 1
            
            quality_indicators['commit_message_quality'] = (good_messages / len(commits)) * 100
        
        return quality_indicators
    
    def _analyze_development_patterns(self, commits, prs):
        """Analyze development patterns"""
        patterns = {
            'commit_distribution': {},
            'pr_merge_rate': 0,
            'development_focus': []
        }
        
        # Analyze commit timing
        if commits:
            days = []
            for commit in commits:
                try:
                    if isinstance(commit['date'], str):
                        dt = datetime.fromisoformat(commit['date'].replace('Z', '+00:00'))
                    else:
                        dt = commit['date']
                    days.append(dt.strftime('%A'))
                except:
                    continue
            
            patterns['commit_distribution'] = dict(Counter(days))
        
        # PR merge rate
        if prs:
            merged_prs = sum(1 for pr in prs if pr.get('merged', False))
            patterns['pr_merge_rate'] = (merged_prs / len(prs)) * 100
        
        return patterns
    
    def _analyze_project_focus(self, commits, prs, issues):
        """Analyze project focus areas"""
        repositories = []
        
        # Collect repository names
        for item in commits + prs + issues:
            repo = item.get('repo')
            if repo:
                repositories.append(repo)
        
        repo_counter = Counter(repositories)
        return repo_counter.most_common(5)
    
    def _analyze_collaboration(self, prs, issues):
        """Analyze collaboration metrics"""
        metrics = {
            'pr_review_engagement': 0,
            'issue_interaction': 0,
            'collaboration_score': 0
        }
        
        # Simple collaboration scoring
        if prs:
            metrics['pr_review_engagement'] = len(prs) * 2  # Simplified metric
        
        if issues:
            metrics['issue_interaction'] = len(issues) * 1.5  # Simplified metric
        
        metrics['collaboration_score'] = metrics['pr_review_engagement'] + metrics['issue_interaction']
        
        return metrics
    
    def _generate_technical_insights(self, github_data):
        """Generate technical insights"""
        insights = []
        
        commits = github_data.get('commits', [])
        stats = github_data.get('stats', {})
        
        if stats.get('total_commits', 0) > 20:
            insights.append("High development activity with consistent commits")
        
        if stats.get('merged_prs', 0) / max(stats.get('total_prs', 1), 1) > 0.8:
            insights.append("Excellent code review and merge rate")
        
        if stats.get('total_additions', 0) > stats.get('total_deletions', 0) * 2:
            insights.append("Significant feature development and code expansion")
        
        return insights
    
    def _generate_github_recommendations(self, analysis):
        """Generate GitHub recommendations"""
        recommendations = []
        
        if analysis['productivity_score'] < 50:
            recommendations.append("Consider increasing development activity and commit frequency")
        
        if analysis['code_quality_indicators'].get('commit_message_quality', 0) < 70:
            recommendations.append("Improve commit message clarity and descriptiveness")
        
        if analysis['collaboration_metrics']['collaboration_score'] < 10:
            recommendations.append("Increase collaboration through code reviews and issue discussions")
        
        return recommendations
    
    def _extract_customer_issues(self, content):
        """Extract customer issues from conversation content"""
        issue_keywords = {
            'technical': ['error', 'bug', 'not working', 'problem', 'issue', 'fail'],
            'billing': ['payment', 'charge', 'bill', 'invoice', 'cost', 'price'],
            'service': ['slow', 'late', 'delay', 'cancel', 'refund'],
            'information': ['how to', 'help', 'question', 'explain', 'understand']
        }
        
        issues = []
        content_lower = content.lower()
        
        for issue_type, keywords in issue_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                issues.append(issue_type)
        
        return issues
    
    def _analyze_response_time(self, conversation):
        """Analyze response time for a conversation"""
        messages = conversation.get('messages', [])
        if len(messages) < 2:
            return {'average_response_time': 0, 'response_count': 0}
        
        # Simplified response time calculation
        response_times = []
        for i in range(1, len(messages)):
            try:
                curr_time = messages[i]['datetime']
                prev_time = messages[i-1]['datetime']
                
                if isinstance(curr_time, str):
                    curr_time = datetime.fromisoformat(curr_time)
                if isinstance(prev_time, str):
                    prev_time = datetime.fromisoformat(prev_time)
                
                diff = (curr_time - prev_time).total_seconds() / 60  # minutes
                response_times.append(diff)
            except:
                continue
        
        avg_response = sum(response_times) / len(response_times) if response_times else 0
        
        return {
            'average_response_time': avg_response,
            'response_count': len(response_times)
        }
    
    def _analyze_customer_satisfaction(self, messages):
        """Analyze customer satisfaction indicators"""
        satisfaction_keywords = {
            'positive': ['thank', 'great', 'perfect', 'excellent', 'good', 'satisfied'],
            'negative': ['bad', 'terrible', 'awful', 'disappointed', 'angry', 'frustrated']
        }
        
        positive_count = 0
        negative_count = 0
        
        for message in messages:
            content = message.get('message', '').lower()
            
            for keyword in satisfaction_keywords['positive']:
                if keyword in content:
                    positive_count += 1
            
            for keyword in satisfaction_keywords['negative']:
                if keyword in content:
                    negative_count += 1
        
        if positive_count > negative_count:
            return 'satisfied'
        elif negative_count > positive_count:
            return 'dissatisfied'
        else:
            return 'neutral'
    
    def _compile_response_metrics(self, response_times):
        """Compile response time metrics"""
        if not response_times:
            return {'average_response_time': 0, 'total_responses': 0}
        
        total_time = sum(rt['average_response_time'] for rt in response_times)
        total_responses = sum(rt['response_count'] for rt in response_times)
        
        return {
            'average_response_time': total_time / len(response_times),
            'total_responses': total_responses,
            'response_efficiency': 'excellent' if total_time / len(response_times) < 30 else 'good' if total_time / len(response_times) < 60 else 'needs_improvement'
        }
    
    def _compile_satisfaction_metrics(self, satisfaction_indicators):
        """Compile customer satisfaction metrics"""
        satisfaction_counter = Counter(satisfaction_indicators)
        total = len(satisfaction_indicators)
        
        if total == 0:
            return {'overall_satisfaction': 'unknown', 'satisfaction_rate': 0}
        
        satisfied_rate = satisfaction_counter.get('satisfied', 0) / total * 100
        
        return {
            'overall_satisfaction': 'high' if satisfied_rate > 70 else 'medium' if satisfied_rate > 40 else 'low',
            'satisfaction_rate': satisfied_rate,
            'distribution': dict(satisfaction_counter)
        }
    
    def _generate_conversation_insights(self, conversations):
        """Generate insights from conversations"""
        insights = []
        
        if len(conversations) > 20:
            insights.append("High customer engagement with active support requests")
        
        avg_messages = sum(conv.get('message_count', 0) for conv in conversations) / max(len(conversations), 1)
        if avg_messages > 10:
            insights.append("Complex support cases requiring detailed assistance")
        elif avg_messages < 3:
            insights.append("Efficient resolution of customer queries")
        
        return insights
    
    def _generate_support_recommendations(self, analysis):
        """Generate support improvement recommendations"""
        recommendations = []
        
        response_efficiency = analysis.get('response_efficiency', {}).get('response_efficiency', '')
        if response_efficiency == 'needs_improvement':
            recommendations.append("Improve response times to enhance customer satisfaction")
        
        satisfaction_rate = analysis.get('customer_satisfaction', {}).get('satisfaction_rate', 0)
        if satisfaction_rate < 70:
            recommendations.append("Focus on improving customer satisfaction through better service quality")
        
        common_issues = analysis.get('common_issues', [])
        if common_issues:
            top_issue = common_issues[0][0]
            recommendations.append(f"Create knowledge base for common {top_issue} issues to improve efficiency")
        
        return recommendations
    
    def _generate_executive_summary(self, all_data):
        """Generate executive summary using all data"""
        summary_parts = []
        
        # Email summary
        if 'emails' in all_data:
            email_analysis = all_data['emails'].get('ai_analysis', {})
            total_emails = email_analysis.get('total_emails', 0)
            summary_parts.append(f"Processed {total_emails} email communications")
        
        # GitHub summary
        if 'github' in all_data:
            github_analysis = all_data['github'].get('ai_analysis', {})
            productivity_score = github_analysis.get('productivity_score', 0)
            summary_parts.append(f"Achieved {productivity_score}% development productivity score")
        
        # WhatsApp summary
        if 'whatsapp' in all_data:
            whatsapp_analysis = all_data['whatsapp'].get('ai_analysis', {})
            satisfaction = whatsapp_analysis.get('customer_satisfaction', {}).get('overall_satisfaction', 'unknown')
            summary_parts.append(f"Maintained {satisfaction} customer satisfaction level")
        
        return ". ".join(summary_parts) + "."
    
    def _identify_key_achievements(self, all_data):
        """Identify key achievements across all data sources"""
        achievements = []
        
        # GitHub achievements
        if 'github' in all_data:
            stats = all_data['github'].get('stats', {})
            if stats.get('total_commits', 0) > 50:
                achievements.append(f"Delivered {stats['total_commits']} code commits")
            if stats.get('merged_prs', 0) > 10:
                achievements.append(f"Successfully merged {stats['merged_prs']} pull requests")
        
        # Email achievements
        if 'emails' in all_data:
            email_analysis = all_data['emails'].get('ai_analysis', {})
            productivity_emails = email_analysis.get('categories', {}).get('productivity', 0)
            if productivity_emails > 20:
                achievements.append(f"Handled {productivity_emails} productivity-focused communications")
        
        # Customer service achievements
        if 'whatsapp' in all_data:
            conversations = all_data['whatsapp'].get('conversations', [])
            if len(conversations) > 30:
                achievements.append(f"Provided support to {len(conversations)} customer conversations")
        
        return achievements
    
    def _analyze_overall_productivity(self, all_data):
        """Analyze overall productivity across all sources"""
        productivity = {
            'overall_score': 0,
            'breakdown': {},
            'trends': []
        }
        
        scores = []
        
        # GitHub productivity
        if 'github' in all_data:
            github_score = all_data['github'].get('ai_analysis', {}).get('productivity_score', 0)
            scores.append(github_score)
            productivity['breakdown']['development'] = github_score
        
        # Email productivity
        if 'emails' in all_data:
            email_analysis = all_data['emails'].get('ai_analysis', {})
            total_emails = email_analysis.get('total_emails', 0)
            email_score = min((total_emails / 10) * 10, 100)  # 10 emails = 10 points, max 100
            scores.append(email_score)
            productivity['breakdown']['communication'] = email_score
        
        # Customer service productivity
        if 'whatsapp' in all_data:
            conversations = all_data['whatsapp'].get('conversations', [])
            service_score = min((len(conversations) / 5) * 10, 100)  # 5 convos = 10 points, max 100
            scores.append(service_score)
            productivity['breakdown']['customer_service'] = service_score
        
        productivity['overall_score'] = sum(scores) / len(scores) if scores else 0
        
        return productivity
    
    def _analyze_communication_effectiveness(self, all_data):
        """Analyze communication effectiveness"""
        effectiveness = {
            'email_effectiveness': 0,
            'response_quality': 0,
            'overall_rating': 'good'
        }
        
        if 'emails' in all_data:
            email_analysis = all_data['emails'].get('ai_analysis', {})
            positive_sentiment = email_analysis.get('sentiment_analysis', {}).get('positive', 0)
            total_emails = email_analysis.get('total_emails', 1)
            effectiveness['email_effectiveness'] = (positive_sentiment / total_emails) * 100
        
        if 'whatsapp' in all_data:
            whatsapp_analysis = all_data['whatsapp'].get('ai_analysis', {})
            satisfaction_rate = whatsapp_analysis.get('customer_satisfaction', {}).get('satisfaction_rate', 0)
            effectiveness['response_quality'] = satisfaction_rate
        
        avg_effectiveness = (effectiveness['email_effectiveness'] + effectiveness['response_quality']) / 2
        if avg_effectiveness > 80:
            effectiveness['overall_rating'] = 'excellent'
        elif avg_effectiveness > 60:
            effectiveness['overall_rating'] = 'good'
        else:
            effectiveness['overall_rating'] = 'needs_improvement'
        
        return effectiveness
    
    def _analyze_technical_contributions(self, all_data):
        """Analyze technical contributions"""
        contributions = {
            'code_contributions': {},
            'technical_impact': 0,
            'innovation_score': 0
        }
        
        if 'github' in all_data:
            stats = all_data['github'].get('stats', {})
            github_analysis = all_data['github'].get('ai_analysis', {})
            
            contributions['code_contributions'] = {
                'commits': stats.get('total_commits', 0),
                'additions': stats.get('total_additions', 0),
                'deletions': stats.get('total_deletions', 0),
                'files_changed': stats.get('total_files_changed', 0)
            }
            
            contributions['technical_impact'] = github_analysis.get('productivity_score', 0)
            
            # Innovation score based on new repositories and features
            repos_worked = stats.get('repos_worked_on', 0)
            contributions['innovation_score'] = min(repos_worked * 20, 100)
        
        return contributions
    
    def _analyze_customer_service(self, all_data):
        """Analyze customer service performance"""
        service = {
            'service_quality': 0,
            'response_efficiency': 0,
            'customer_satisfaction': 0,
            'overall_performance': 'good'
        }
        
        if 'whatsapp' in all_data:
            whatsapp_analysis = all_data['whatsapp'].get('ai_analysis', {})
            
            satisfaction_metrics = whatsapp_analysis.get('customer_satisfaction', {})
            service['customer_satisfaction'] = satisfaction_metrics.get('satisfaction_rate', 0)
            
            response_metrics = whatsapp_analysis.get('response_efficiency', {})
            response_eff = response_metrics.get('response_efficiency', 'good')
            
            if response_eff == 'excellent':
                service['response_efficiency'] = 90
            elif response_eff == 'good':
                service['response_efficiency'] = 70
            else:
                service['response_efficiency'] = 40
            
            service['service_quality'] = (service['customer_satisfaction'] + service['response_efficiency']) / 2
            
            if service['service_quality'] > 80:
                service['overall_performance'] = 'excellent'
            elif service['service_quality'] > 60:
                service['overall_performance'] = 'good'
            else:
                service['overall_performance'] = 'needs_improvement'
        
        return service
    
    def _identify_improvement_areas(self, all_data):
        """Identify areas for improvement"""
        improvements = []
        
        # Analyze all recommendations from different sources
        if 'github' in all_data:
            github_recommendations = all_data['github'].get('ai_analysis', {}).get('recommendations', [])
            improvements.extend(github_recommendations)
        
        if 'whatsapp' in all_data:
            whatsapp_recommendations = all_data['whatsapp'].get('ai_analysis', {}).get('improvement_suggestions', [])
            improvements.extend(whatsapp_recommendations)
        
        if 'emails' in all_data:
            email_analysis = all_data['emails'].get('ai_analysis', {})
            urgency_ratio = email_analysis.get('urgency_levels', {}).get('high', 0) / max(email_analysis.get('total_emails', 1), 1)
            if urgency_ratio > 0.3:
                improvements.append("Reduce urgent communications through better planning and proactive communication")
        
        return improvements
    
    def _generate_strategic_recommendations(self, all_data):
        """Generate strategic recommendations"""
        recommendations = []
        
        # Productivity recommendations
        productivity = self._analyze_overall_productivity(all_data)
        if productivity['overall_score'] < 70:
            recommendations.append("Focus on increasing overall productivity through better time management and tool optimization")
        
        # Communication recommendations
        communication = self._analyze_communication_effectiveness(all_data)
        if communication['overall_rating'] == 'needs_improvement':
            recommendations.append("Improve communication effectiveness through clearer messaging and more positive interactions")
        
        # Technical recommendations
        if 'github' in all_data:
            github_analysis = all_data['github'].get('ai_analysis', {})
            if github_analysis.get('productivity_score', 0) < 60:
                recommendations.append("Increase development velocity through better coding practices and more frequent commits")
        
        return recommendations
    
    def _calculate_performance_metrics(self, all_data):
        """Calculate overall performance metrics"""
        metrics = {
            'overall_performance_score': 0,
            'category_scores': {},
            'performance_grade': 'B'
        }
        
        scores = []
        
        # Development performance
        if 'github' in all_data:
            dev_score = all_data['github'].get('ai_analysis', {}).get('productivity_score', 0)
            metrics['category_scores']['development'] = dev_score
            scores.append(dev_score)
        
        # Communication performance
        if 'emails' in all_data:
            email_analysis = all_data['emails'].get('ai_analysis', {})
            comm_score = (email_analysis.get('sentiment_analysis', {}).get('positive', 0) / 
                         max(email_analysis.get('total_emails', 1), 1)) * 100
            metrics['category_scores']['communication'] = comm_score
            scores.append(comm_score)
        
        # Customer service performance
        if 'whatsapp' in all_data:
            service_score = all_data['whatsapp'].get('ai_analysis', {}).get('customer_satisfaction', {}).get('satisfaction_rate', 0)
            metrics['category_scores']['customer_service'] = service_score
            scores.append(service_score)
        
        # Calculate overall score
        metrics['overall_performance_score'] = sum(scores) / len(scores) if scores else 0
        
        # Assign grade
        score = metrics['overall_performance_score']
        if score >= 90:
            metrics['performance_grade'] = 'A+'
        elif score >= 80:
            metrics['performance_grade'] = 'A'
        elif score >= 70:
            metrics['performance_grade'] = 'B'
        elif score >= 60:
            metrics['performance_grade'] = 'C'
        else:
            metrics['performance_grade'] = 'D'
        
        return metrics