from datetime import datetime
import random

def format_engagement_number(number):
    """Format large numbers with K, M suffixes"""
    if number >= 1000000:
        return f"{number/1000000:.1f}M"
    elif number >= 1000:
        return f"{number/1000:.1f}K"
    else:
        return str(number)

def calculate_time_ago(timestamp):
    """Calculate human-readable time difference"""
    now = datetime.now()
    diff = now - timestamp
    
    if diff.days > 0:
        if diff.days == 1:
            return "1 day ago"
        elif diff.days < 7:
            return f"{diff.days} days ago"
        elif diff.days < 30:
            weeks = diff.days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''} ago"
        elif diff.days < 365:
            months = diff.days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        else:
            years = diff.days // 365
            return f"{years} year{'s' if years > 1 else ''} ago"
    
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    
    else:
        return "Just now"

def generate_engagement_metrics(posts_data):
    """Generate engagement metrics from posts data"""
    metrics = {
        'total_likes': sum(post['likes'] for post in posts_data),
        'total_comments': sum(post['comments'] for post in posts_data),
        'total_shares': sum(post['shares'] for post in posts_data),
        'total_views': sum(post['views'] for post in posts_data),
        'avg_engagement_rate': 0
    }
    
    if metrics['total_views'] > 0:
        total_engagement = metrics['total_likes'] + metrics['total_comments'] + metrics['total_shares']
        metrics['avg_engagement_rate'] = (total_engagement / metrics['total_views']) * 100
    
    return metrics

def get_trending_hashtags():
    """Returns trending hashtags for the profile"""
    return [
        '#ContentCreator',
        '#LifestyleInfluencer',
        '#TravelDiaries',
        '#PhotographyLife',
        '#MorningMotivation',
        '#FitnessJourney',
        '#FoodieLife',
        '#DigitalMarketing',
        '#CreativeLife',
        '#WanderlustVibes'
    ]
