from database.schema import User, SocialLink, Post, GalleryItem, init_db, get_session
from datetime import datetime, timedelta
import random

def seed_database():
    """Seed the database with initial data"""
    session = get_session()
    
    try:
        # Check if data already exists
        existing_user = session.query(User).filter_by(username='sonia.papi').first()
        if existing_user:
            print("Database already seeded. Skipping...")
            return
        
        # Create main user
        user = User(
            name='Sonia Papi',
            username='sonia.papi',
            bio='✨ Content Creator | 📸 Photography Enthusiast | 🌍 Travel Lover | 💼 Digital Marketing Pro',
            followers=15420,
            following=892,
            location='London, UK',
            joined_date=datetime(2020, 3, 15),
            verification_status=True,
            email='hello@soniapapi.com',
            phone='+44 20 1234 5678',
            website='https://soniapapi.com'
        )
        session.add(user)
        session.flush()
        
        # Add social links
        social_platforms = [
            ('snapchat', 'https://www.snapchat.com/@sonia.papi'),
            ('instagram', 'https://instagram.com/sonia.papi'),
            ('twitter', 'https://twitter.com/sonia_papi'),
            ('linkedin', 'https://linkedin.com/in/soniapapi'),
            ('tiktok', 'https://tiktok.com/@sonia.papi')
        ]
        
        for platform, url in social_platforms:
            social_link = SocialLink(user_id=user.id, platform=platform, url=url)
            session.add(social_link)
        
        # Add gallery items
        gallery_items = [
            {
                'title': 'Sunset in Santorini',
                'item_type': 'image',
                'category': 'Travel',
                'description': 'Beautiful sunset captured during my trip to Santorini, Greece. The colors were absolutely magical!',
                'likes': 1247,
                'views': 8934,
                'upload_date': datetime(2024, 9, 15)
            },
            {
                'title': 'Morning Coffee Routine',
                'item_type': 'video',
                'category': 'Lifestyle',
                'description': 'My daily morning coffee routine - starting the day right with a perfect cup!',
                'likes': 892,
                'views': 5621,
                'upload_date': datetime(2024, 10, 1)
            },
            {
                'title': 'London Street Photography',
                'item_type': 'image',
                'category': 'Photography',
                'description': 'Capturing the essence of London streets during golden hour.',
                'likes': 2156,
                'views': 12453,
                'upload_date': datetime(2024, 8, 22)
            },
            {
                'title': 'Fashion Haul',
                'item_type': 'video',
                'category': 'Fashion',
                'description': 'Latest fashion finds from my shopping trip in Milan!',
                'likes': 3421,
                'views': 18792,
                'upload_date': datetime(2024, 9, 30)
            },
            {
                'title': 'Homemade Pasta',
                'item_type': 'image',
                'category': 'Food',
                'description': 'Made fresh pasta from scratch - sharing my grandmother\'s recipe!',
                'likes': 1876,
                'views': 9654,
                'upload_date': datetime(2024, 10, 10)
            },
            {
                'title': 'Workout Motivation',
                'item_type': 'video',
                'category': 'Fitness',
                'description': 'Quick 15-minute morning workout routine to start your day strong!',
                'likes': 2934,
                'views': 15678,
                'upload_date': datetime(2024, 10, 5)
            }
        ]
        
        for item_data in gallery_items:
            gallery_item = GalleryItem(user_id=user.id, **item_data)
            session.add(gallery_item)
        
        # Add posts
        base_time = datetime.now()
        posts_data = [
            {
                'caption': '🌅 Another beautiful morning in London! Starting the day with gratitude and positive vibes. What are you grateful for today? #MorningMotivation #Gratitude',
                'post_type': 'story',
                'media_type': 'image',
                'likes': 1245,
                'shares': 23,
                'views': 8934,
                'timestamp': base_time - timedelta(days=0, hours=8)
            },
            {
                'caption': '✨ Behind the scenes of my latest photoshoot! So much fun working with this amazing team. Can\'t wait to share the final results! #BTS #Photography #TeamWork',
                'post_type': 'post',
                'media_type': 'video',
                'likes': 2156,
                'shares': 67,
                'views': 15672,
                'timestamp': base_time - timedelta(days=2, hours=14)
            },
            {
                'caption': '🍝 Cooking up some magic in the kitchen tonight! This homemade pasta recipe has been in my family for generations. Recipe in bio! #FoodLove #Cooking #FamilyRecipes',
                'post_type': 'post',
                'media_type': 'image',
                'likes': 1876,
                'shares': 45,
                'views': 12089,
                'timestamp': base_time - timedelta(days=4, hours=19)
            },
            {
                'caption': '💪 Consistency is key! Day 30 of my fitness journey and feeling stronger than ever. Remember, progress over perfection! #FitnessJourney #Motivation #HealthyLifestyle',
                'post_type': 'story',
                'media_type': 'video',
                'likes': 2934,
                'shares': 78,
                'views': 18456,
                'timestamp': base_time - timedelta(days=6, hours=7)
            },
            {
                'caption': '🎨 Creativity has no limits! Spent the afternoon exploring street art in Shoreditch. Every corner tells a story. #StreetArt #Creativity #London #Art',
                'post_type': 'post',
                'media_type': 'image',
                'likes': 1654,
                'shares': 34,
                'views': 9876,
                'timestamp': base_time - timedelta(days=8, hours=15)
            },
            {
                'caption': '✈️ Next adventure loading... Can you guess where I\'m headed next? Drop your guesses in the comments! #TravelMode #Adventure #Wanderlust',
                'post_type': 'story',
                'media_type': 'image',
                'likes': 3421,
                'shares': 123,
                'views': 25789,
                'timestamp': base_time - timedelta(days=10, hours=11)
            }
        ]
        
        for post_data in posts_data:
            post = Post(user_id=user.id, **post_data)
            session.add(post)
        
        session.commit()
        print("Database seeded successfully!")
        
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    init_db()
    seed_database()
