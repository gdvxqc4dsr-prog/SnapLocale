from database.schema import User, SocialLink, Post, GalleryItem, Comment, Analytics, get_session
from datetime import datetime
from sqlalchemy import desc, func

class DatabaseOperations:
    """Database operations for the profile application"""
    
    @staticmethod
    def get_user_by_username(username):
        """Get user by username"""
        session = get_session()
        try:
            user = session.query(User).filter_by(username=username).first()
            return user
        finally:
            session.close()
    
    @staticmethod
    def get_profile_data(username='sonia.papi'):
        """Get complete profile data for a user"""
        session = get_session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if not user:
                return None
            
            social_links = session.query(SocialLink).filter_by(user_id=user.id).all()
            
            profile = {
                'name': user.name,
                'username': user.username,
                'bio': user.bio,
                'followers': user.followers,
                'following': user.following,
                'location': user.location,
                'joined_date': user.joined_date.strftime('%Y-%m-%d') if user.joined_date else '',
                'verification_status': user.verification_status,
                'social_links': {link.platform: link.url for link in social_links},
                'contact': {
                    'email': user.email,
                    'phone': user.phone,
                    'location': user.location,
                    'website': user.website
                }
            }
            return profile
        finally:
            session.close()
    
    @staticmethod
    def get_gallery_items(user_id=None, category=None):
        """Get gallery items with optional filtering"""
        session = get_session()
        try:
            query = session.query(GalleryItem)
            if user_id:
                query = query.filter_by(user_id=user_id)
            if category:
                query = query.filter_by(category=category)
            
            items = query.order_by(desc(GalleryItem.upload_date)).all()
            
            gallery_data = []
            for item in items:
                gallery_data.append({
                    'id': item.id,
                    'title': item.title,
                    'type': item.item_type,
                    'category': item.category,
                    'description': item.description,
                    'likes': item.likes,
                    'views': item.views,
                    'upload_date': item.upload_date.strftime('%Y-%m-%d') if item.upload_date else ''
                })
            return gallery_data
        finally:
            session.close()
    
    @staticmethod
    def get_post_by_id(post_id):
        """Get a single post by ID"""
        session = get_session()
        try:
            post = session.query(Post).filter_by(id=post_id).first()
            if post:
                comment_count = session.query(Comment).filter_by(post_id=post.id).count()
                return {
                    'id': post.id,
                    'caption': post.caption,
                    'type': post.post_type,
                    'media_type': post.media_type,
                    'likes': post.likes,
                    'comments': comment_count,
                    'shares': post.shares,
                    'views': post.views,
                    'timestamp': post.timestamp
                }
            return None
        finally:
            session.close()
    
    @staticmethod
    def get_gallery_item_by_id(item_id):
        """Get a single gallery item by ID"""
        session = get_session()
        try:
            item = session.query(GalleryItem).filter_by(id=item_id).first()
            if item:
                return {
                    'id': item.id,
                    'title': item.title,
                    'type': item.item_type,
                    'category': item.category,
                    'description': item.description,
                    'likes': item.likes,
                    'views': item.views,
                    'upload_date': item.upload_date.strftime('%Y-%m-%d') if item.upload_date else ''
                }
            return None
        finally:
            session.close()
    
    @staticmethod
    def get_posts(user_id=None, limit=None):
        """Get posts with optional filtering"""
        session = get_session()
        try:
            query = session.query(Post)
            if user_id:
                query = query.filter_by(user_id=user_id)
            
            query = query.order_by(desc(Post.timestamp))
            
            if limit:
                query = query.limit(limit)
            
            posts = query.all()
            
            posts_data = []
            for post in posts:
                comment_count = session.query(Comment).filter_by(post_id=post.id).count()
                posts_data.append({
                    'id': post.id,
                    'caption': post.caption,
                    'type': post.post_type,
                    'media_type': post.media_type,
                    'likes': post.likes,
                    'comments': comment_count,
                    'shares': post.shares,
                    'views': post.views,
                    'timestamp': post.timestamp
                })
            return posts_data
        finally:
            session.close()
    
    @staticmethod
    def get_comments_for_post(post_id):
        """Get all comments for a specific post"""
        session = get_session()
        try:
            comments = session.query(Comment).filter_by(post_id=post_id).order_by(desc(Comment.timestamp)).all()
            comments_data = []
            for comment in comments:
                user = session.query(User).filter_by(id=comment.user_id).first()
                comments_data.append({
                    'id': comment.id,
                    'content': comment.content,
                    'user_name': user.name if user else 'Unknown',
                    'user_username': user.username if user else 'unknown',
                    'timestamp': comment.timestamp,
                    'likes': comment.likes
                })
            return comments_data
        finally:
            session.close()
    
    @staticmethod
    def add_gallery_item(user_id, title, item_type, category, description):
        """Add a new gallery item"""
        session = get_session()
        try:
            gallery_item = GalleryItem(
                user_id=user_id,
                title=title,
                item_type=item_type,
                category=category,
                description=description
            )
            session.add(gallery_item)
            session.commit()
            return gallery_item.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def add_post(user_id, caption, post_type, media_type=None):
        """Add a new post"""
        session = get_session()
        try:
            post = Post(
                user_id=user_id,
                caption=caption,
                post_type=post_type,
                media_type=media_type
            )
            session.add(post)
            session.commit()
            return post.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def add_comment(post_id, user_id, content):
        """Add a comment to a post"""
        session = get_session()
        try:
            comment = Comment(
                post_id=post_id,
                user_id=user_id,
                content=content
            )
            session.add(comment)
            session.commit()
            return comment.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def update_likes(entity_type, entity_id, increment=True):
        """Update like count for posts, gallery items, or comments"""
        session = get_session()
        try:
            if entity_type == 'post':
                entity = session.query(Post).filter_by(id=entity_id).first()
            elif entity_type == 'gallery':
                entity = session.query(GalleryItem).filter_by(id=entity_id).first()
            elif entity_type == 'comment':
                entity = session.query(Comment).filter_by(id=entity_id).first()
            else:
                return False
            
            if entity:
                if increment:
                    entity.likes += 1
                else:
                    entity.likes = max(0, entity.likes - 1)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def update_views(entity_type, entity_id):
        """Increment view count"""
        session = get_session()
        try:
            if entity_type == 'post':
                entity = session.query(Post).filter_by(id=entity_id).first()
            elif entity_type == 'gallery':
                entity = session.query(GalleryItem).filter_by(id=entity_id).first()
            else:
                return False
            
            if entity:
                entity.views += 1
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def update_post(post_id, caption=None, post_type=None, media_type=None):
        """Update an existing post"""
        session = get_session()
        try:
            post = session.query(Post).filter_by(id=post_id).first()
            if post:
                if caption is not None:
                    post.caption = caption
                if post_type is not None:
                    post.post_type = post_type
                if media_type is not None:
                    post.media_type = media_type
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def update_gallery_item(item_id, title=None, item_type=None, category=None, description=None):
        """Update an existing gallery item"""
        session = get_session()
        try:
            item = session.query(GalleryItem).filter_by(id=item_id).first()
            if item:
                if title is not None:
                    item.title = title
                if item_type is not None:
                    item.item_type = item_type
                if category is not None:
                    item.category = category
                if description is not None:
                    item.description = description
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def delete_post(post_id):
        """Delete a post"""
        session = get_session()
        try:
            post = session.query(Post).filter_by(id=post_id).first()
            if post:
                session.delete(post)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def delete_gallery_item(item_id):
        """Delete a gallery item"""
        session = get_session()
        try:
            item = session.query(GalleryItem).filter_by(id=item_id).first()
            if item:
                session.delete(item)
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def track_analytics(user_id, event_type, event_data=None):
        """Track analytics event"""
        session = get_session()
        try:
            analytics = Analytics(
                user_id=user_id,
                event_type=event_type,
                event_data=event_data
            )
            session.add(analytics)
            session.commit()
            return analytics.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    @staticmethod
    def get_analytics_summary(user_id, days=7):
        """Get analytics summary for the last N days"""
        session = get_session()
        try:
            from datetime import timedelta
            start_date = datetime.now() - timedelta(days=days)
            
            analytics = session.query(Analytics).filter(
                Analytics.user_id == user_id,
                Analytics.timestamp >= start_date
            ).all()
            
            summary = {
                'total_events': len(analytics),
                'events_by_type': {}
            }
            
            for event in analytics:
                if event.event_type not in summary['events_by_type']:
                    summary['events_by_type'][event.event_type] = 0
                summary['events_by_type'][event.event_type] += 1
            
            return summary
        finally:
            session.close()
    
    @staticmethod
    def search_content(query, search_type='all'):
        """Search posts and gallery items"""
        session = get_session()
        try:
            results = {
                'posts': [],
                'gallery': []
            }
            
            if search_type in ['all', 'posts']:
                posts = session.query(Post).filter(
                    Post.caption.ilike(f'%{query}%')
                ).order_by(desc(Post.timestamp)).all()
                
                for post in posts:
                    results['posts'].append({
                        'id': post.id,
                        'caption': post.caption,
                        'type': post.post_type,
                        'timestamp': post.timestamp
                    })
            
            if search_type in ['all', 'gallery']:
                items = session.query(GalleryItem).filter(
                    (GalleryItem.title.ilike(f'%{query}%')) |
                    (GalleryItem.description.ilike(f'%{query}%'))
                ).order_by(desc(GalleryItem.upload_date)).all()
                
                for item in items:
                    results['gallery'].append({
                        'id': item.id,
                        'title': item.title,
                        'category': item.category,
                        'type': item.item_type
                    })
            
            return results
        finally:
            session.close()
