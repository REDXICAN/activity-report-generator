import os
import sys
from datetime import datetime, timedelta
from email_collector import EmailCollector
from github_collector import GitHubCollector
from whatsapp_collector import WhatsAppCollector
from report_generator import ReportGenerator
from config import Config

class ActivityReportGenerator:
    def __init__(self):
        self.email_collector = None
        self.github_collector = None
        self.whatsapp_collector = None
        self.report_generator = ReportGenerator()
    
    def initialize_collectors(self, email_enabled=True, github_enabled=True, whatsapp_enabled=True):
        """Initialize data collectors based on user preferences"""
        if email_enabled:
            try:
                self.email_collector = EmailCollector()
            except Exception as e:
                print(f"Error initializing email collector: {e}")
        
        if github_enabled and Config.GITHUB_TOKEN:
            try:
                self.github_collector = GitHubCollector()
            except Exception as e:
                print(f"Error initializing GitHub collector: {e}")
        
        if whatsapp_enabled and Config.WHATSAPP_DATA_PATH:
            try:
                self.whatsapp_collector = WhatsAppCollector(Config.WHATSAPP_DATA_PATH)
            except Exception as e:
                print(f"Error initializing WhatsApp collector: {e}")
    
    def collect_data(self, start_date, end_date):
        """Collect data from all sources"""
        data = {}
        
        # Collect email data
        if self.email_collector:
            print("Collecting email data...")
            try:
                sent_emails = self.email_collector.get_sent_emails(start_date, end_date)
                received_emails = self.email_collector.get_received_emails(start_date, end_date)
                categorized = self.email_collector.categorize_emails(sent_emails + received_emails)
                
                data['emails'] = {
                    'sent': sent_emails,
                    'received': received_emails,
                    'categorized': categorized
                }
                print(f"Found {len(sent_emails)} sent emails and {len(received_emails)} received emails")
            except Exception as e:
                print(f"Error collecting email data: {e}")
        
        # Collect GitHub data
        if self.github_collector:
            print("Collecting GitHub data...")
            try:
                github_activities = self.github_collector.get_activities(start_date, end_date)
                github_stats = self.github_collector.get_statistics(github_activities)
                
                data['github'] = github_activities
                data['github']['stats'] = github_stats
                print(f"Found {github_stats['total_commits']} commits and {github_stats['total_prs']} pull requests")
            except Exception as e:
                print(f"Error collecting GitHub data: {e}")
        
        # Collect WhatsApp data
        if self.whatsapp_collector:
            print("Collecting WhatsApp data...")
            try:
                whatsapp_stats = self.whatsapp_collector.get_statistics(start_date, end_date)
                data['whatsapp'] = whatsapp_stats
                print(f"Found {whatsapp_stats['unique_customers']} unique customers")
            except Exception as e:
                print(f"Error collecting WhatsApp data: {e}")
        
        return data
    
    def generate_report(self, start_date, end_date, output_format='both'):
        """Generate activity report"""
        print(f"\nGenerating report for period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        # Collect data
        data = self.collect_data(start_date, end_date)
        
        if not data:
            print("No data collected. Please check your configurations.")
            return None, None
        
        # Generate Excel report
        print("\nGenerating Excel report...")
        excel_path = self.report_generator.generate_excel_report(data, start_date, end_date)
        print(f"Excel report saved to: {excel_path}")
        
        word_path = None
        if output_format in ['word', 'both']:
            # Generate Word report
            print("\nGenerating Word report...")
            word_path = self.report_generator.generate_word_report(excel_path, start_date, end_date)
            print(f"Word report saved to: {word_path}")
        
        return excel_path, word_path

def main():
    """Command line interface"""
    generator = ActivityReportGenerator()
    
    # Get date range
    print("Activity Report Generator")
    print("-" * 50)
    
    # Default to last 15 days
    end_date = datetime.now()
    if end_date.day <= 15:
        start_date = end_date.replace(day=1)
    else:
        start_date = end_date.replace(day=16)
    
    print(f"Default period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    custom = input("Use custom date range? (y/n): ").lower()
    
    if custom == 'y':
        start_str = input("Start date (YYYY-MM-DD): ")
        end_str = input("End date (YYYY-MM-DD): ")
        start_date = datetime.strptime(start_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_str, '%Y-%m-%d')
    
    # Select data sources
    print("\nSelect data sources:")
    email_enabled = input("Include emails? (y/n): ").lower() == 'y'
    github_enabled = input("Include GitHub? (y/n): ").lower() == 'y'
    whatsapp_enabled = input("Include WhatsApp? (y/n): ").lower() == 'y'
    
    # Initialize collectors
    generator.initialize_collectors(email_enabled, github_enabled, whatsapp_enabled)
    
    # Generate report
    excel_path, word_path = generator.generate_report(start_date, end_date, output_format='both')
    
    if excel_path:
        print("\n✅ Report generation completed!")
        print(f"Excel: {excel_path}")
        if word_path:
            print(f"Word: {word_path}")

if __name__ == "__main__":
    main()