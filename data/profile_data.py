from datetime import datetime, timedelta
import random

def get_profile_data():
    """Returns the main profile data"""
    return {
        'name': 'Sonia Papi',
        'username': 'sonia.papi',
        'bio': '✨ Content Creator | 📸 Photography Enthusiast | 🌍 Travel Lover | 💼 Digital Marketing Pro',
        'followers': 15420,
        'following': 892,
        'location': 'London, UK',
        'joined_date': '2020-03-15',
        'verification_status': True,
        'social_links': {
            'snapchat': 'https://www.snapchat.com/@sonia.papi',
            'instagram': 'https://instagram.com/sonia.papi',
            'twitter': 'https://twitter.com/sonia_papi',
            'linkedin': 'https://linkedin.com/in/soniapapi',
            'tiktok': 'https://tiktok.com/@sonia.papi'
        },
        'contact': {
            'email': 'hello@soniapapi.com',
            'phone': '+44 20 1234 5678',
            'location': 'London, United Kingdom',
            'website': 'https://soniapapi.com'
        }
    }

def get_gallery_data():
    """Returns gallery/media data"""
    return [
        {
            'id': 1,
            'title': 'Sunset in Santorini',
            'type': 'image',
            'category': 'Travel',
            'description': 'Beautiful sunset captured during my trip to Santorini, Greece. The colors were absolutely magical!',
            'likes': 1247,
            'views': 8934,
            'upload_date': '2024-09-15'
        },
        {
            'id': 2,
            'title': 'Morning Coffee Routine',
            'type': 'video',
            'category': 'Lifestyle',
            'description': 'My daily morning coffee routine - starting the day right with a perfect cup!',
            'likes': 892,
            'views': 5621,
            'upload_date': '2024-10-01'
        },
        {
            'id': 3,
            'title': 'London Street Photography',
            'type': 'image',
            'category': 'Photography',
            'description': 'Capturing the essence of London streets during golden hour.',
            'likes': 2156,
            'views': 12453,
            'upload_date': '2024-08-22'
        },
        {
            'id': 4,
            'title': 'Fashion Haul',
            'type': 'video',
            'category': 'Fashion',
            'description': 'Latest fashion finds from my shopping trip in Milan!',
            'likes': 3421,
            'views': 18792,
            'upload_date': '2024-09-30'
        },
        {
            'id': 5,
            'title': 'Homemade Pasta',
            'type': 'image',
            'category': 'Food',
            'description': 'Made fresh pasta from scratch - sharing my grandmother\'s recipe!',
            'likes': 1876,
            'views': 9654,
            'upload_date': '2024-10-10'
        },
        {
            'id': 6,
            'title': 'Workout Motivation',
            'type': 'video',
            'category': 'Fitness',
            'description': 'Quick 15-minute morning workout routine to start your day strong!',
            'likes': 2934,
            'views': 15678,
            'upload_date': '2024-10-05'
        }
    ]

def get_posts_data():
    """Returns social media posts data"""
    posts = []
    
    # Generate posts with realistic timestamps
    base_time = datetime.now()
    
    post_templates = [
        {
            'caption': '🌅 Another beautiful morning in London! Starting the day with gratitude and positive vibes. What are you grateful for today? #MorningMotivation #Gratitude',
            'type': 'story',
            'media_type': 'image',
            'likes': 1245,
            'comments': 87,
            'shares': 23,
            'views': 8934
        },
        {
            'caption': '✨ Behind the scenes of my latest photoshoot! So much fun working with this amazing team. Can\'t wait to share the final results! #BTS #Photography #TeamWork',
            'type': 'post',
            'media_type': 'video',
            'likes': 2156,
            'comments': 143,
            'shares': 67,
            'views': 15672
        },
        {
            'caption': '🍝 Cooking up some magic in the kitchen tonight! This homemade pasta recipe has been in my family for generations. Recipe in bio! #FoodLove #Cooking #FamilyRecipes',
            'type': 'post',
            'media_type': 'image',
            'likes': 1876,
            'comments': 234,
            'shares': 45,
            'views': 12089
        },
        {
            'caption': '💪 Consistency is key! Day 30 of my fitness journey and feeling stronger than ever. Remember, progress over perfection! #FitnessJourney #Motivation #HealthyLifestyle',
            'type': 'story',
            'media_type': 'video',
            'likes': 2934,
            'comments': 189,
            'shares': 78,
            'views': 18456
        },
        {
            'caption': '🎨 Creativity has no limits! Spent the afternoon exploring street art in Shoreditch. Every corner tells a story. #StreetArt #Creativity #London #Art',
            'type': 'post',
            'media_type': 'image',
            'likes': 1654,
            'comments': 98,
            'shares': 34,
            'views': 9876
        },
        {
            'caption': '✈️ Next adventure loading... Can you guess where I\'m headed next? Drop your guesses in the comments! #TravelMode #Adventure #Wanderlust',
            'type': 'story',
            'media_type': 'image',
            'likes': 3421,
            'comments': 567,
            'shares': 123,
            'views': 25789
        }
    ]
    
    for i, template in enumerate(post_templates):
        post = template.copy()
        post['id'] = i + 1
        post['timestamp'] = base_time - timedelta(days=i*2, hours=random.randint(0, 23), minutes=random.randint(0, 59))
        posts.append(post)
    
    return posts
