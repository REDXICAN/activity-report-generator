from github import Github
from datetime import datetime, timedelta
from config import Config

class GitHubCollector:
    def __init__(self):
        self.github = Github(Config.GITHUB_TOKEN)
        self.user = self.github.get_user(Config.GITHUB_USERNAME) if Config.GITHUB_USERNAME else self.github.get_user()
    
    def get_activities(self, start_date, end_date):
        """Get GitHub activities within date range"""
        activities = {
            'commits': [],
            'pull_requests': [],
            'issues': [],
            'repositories': [],
            'reviews': []
        }
        
        # Get commits
        activities['commits'] = self.get_commits(start_date, end_date)
        
        # Get pull requests
        activities['pull_requests'] = self.get_pull_requests(start_date, end_date)
        
        # Get issues
        activities['issues'] = self.get_issues(start_date, end_date)
        
        # Get repository activities
        activities['repositories'] = self.get_repository_activities(start_date, end_date)
        
        return activities
    
    def get_commits(self, start_date, end_date):
        """Get commits made by user within date range"""
        commits = []
        
        # Get all repos
        for repo in self.user.get_repos():
            try:
                # Get commits from this repo
                repo_commits = repo.get_commits(
                    author=self.user,
                    since=start_date,
                    until=end_date
                )
                
                for commit in repo_commits:
                    commit_data = {
                        'repo': repo.name,
                        'sha': commit.sha[:7],
                        'message': commit.commit.message,
                        'date': commit.commit.author.date,
                        'additions': commit.stats.additions,
                        'deletions': commit.stats.deletions,
                        'files_changed': len(commit.files),
                        'url': commit.html_url
                    }
                    commits.append(commit_data)
            except Exception as e:
                print(f"Error getting commits from {repo.name}: {e}")
                continue
        
        return sorted(commits, key=lambda x: x['date'], reverse=True)
    
    def get_pull_requests(self, start_date, end_date):
        """Get pull requests created or updated by user"""
        pull_requests = []
        
        # Search for PRs
        query = f"author:{self.user.login} created:{start_date.isoformat()}..{end_date.isoformat()}"
        prs = self.github.search_issues(query=query, type='pr')
        
        for pr in prs:
            pr_data = {
                'repo': pr.repository.name,
                'number': pr.number,
                'title': pr.title,
                'state': pr.state,
                'created_at': pr.created_at,
                'updated_at': pr.updated_at,
                'merged': pr.pull_request.merged_at is not None if pr.pull_request else False,
                'url': pr.html_url,
                'labels': [label.name for label in pr.labels]
            }
            pull_requests.append(pr_data)
        
        return pull_requests
    
    def get_issues(self, start_date, end_date):
        """Get issues created or updated by user"""
        issues = []
        
        # Search for issues
        query = f"author:{self.user.login} created:{start_date.isoformat()}..{end_date.isoformat()}"
        issues_result = self.github.search_issues(query=query, type='issue')
        
        for issue in issues_result:
            issue_data = {
                'repo': issue.repository.name,
                'number': issue.number,
                'title': issue.title,
                'state': issue.state,
                'created_at': issue.created_at,
                'updated_at': issue.updated_at,
                'url': issue.html_url,
                'labels': [label.name for label in issue.labels],
                'comments': issue.comments
            }
            issues.append(issue_data)
        
        return issues
    
    def get_repository_activities(self, start_date, end_date):
        """Get repository creation/updates"""
        repo_activities = []
        
        for repo in self.user.get_repos():
            # Check if repo was created or significantly updated in the period
            if start_date <= repo.created_at <= end_date:
                repo_activities.append({
                    'name': repo.name,
                    'action': 'created',
                    'date': repo.created_at,
                    'description': repo.description,
                    'language': repo.language,
                    'url': repo.html_url
                })
            elif start_date <= repo.updated_at <= end_date:
                repo_activities.append({
                    'name': repo.name,
                    'action': 'updated',
                    'date': repo.updated_at,
                    'description': repo.description,
                    'language': repo.language,
                    'url': repo.html_url
                })
        
        return repo_activities
    
    def get_statistics(self, activities):
        """Generate statistics from activities"""
        stats = {
            'total_commits': len(activities['commits']),
            'total_additions': sum(c['additions'] for c in activities['commits']),
            'total_deletions': sum(c['deletions'] for c in activities['commits']),
            'total_files_changed': sum(c['files_changed'] for c in activities['commits']),
            'total_prs': len(activities['pull_requests']),
            'merged_prs': len([pr for pr in activities['pull_requests'] if pr['merged']]),
            'total_issues': len(activities['issues']),
            'closed_issues': len([i for i in activities['issues'] if i['state'] == 'closed']),
            'repos_worked_on': len(set(c['repo'] for c in activities['commits'])),
            'languages': {}
        }
        
        # Count languages
        for repo in activities['repositories']:
            if repo['language']:
                stats['languages'][repo['language']] = stats['languages'].get(repo['language'], 0) + 1
        
        return stats