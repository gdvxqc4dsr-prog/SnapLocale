from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    bio = Column(Text)
    followers = Column(Integer, default=0)
    following = Column(Integer, default=0)
    location = Column(String(100))
    joined_date = Column(DateTime, default=datetime.utcnow)
    verification_status = Column(Boolean, default=False)
    email = Column(String(100))
    phone = Column(String(20))
    website = Column(String(200))
    
    posts = relationship('Post', back_populates='user', cascade='all, delete-orphan')
    gallery_items = relationship('GalleryItem', back_populates='user', cascade='all, delete-orphan')
    comments = relationship('Comment', back_populates='user', cascade='all, delete-orphan')

class SocialLink(Base):
    __tablename__ = 'social_links'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    platform = Column(String(50), nullable=False)
    url = Column(String(200), nullable=False)
    
    user = relationship('User', backref='social_links')

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    caption = Column(Text, nullable=False)
    post_type = Column(String(20), nullable=False)
    media_type = Column(String(20))
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    views = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post', cascade='all, delete-orphan')

class GalleryItem(Base):
    __tablename__ = 'gallery_items'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(200), nullable=False)
    item_type = Column(String(20), nullable=False)
    category = Column(String(50), nullable=False)
    description = Column(Text)
    likes = Column(Integer, default=0)
    views = Column(Integer, default=0)
    upload_date = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', back_populates='gallery_items')

class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    likes = Column(Integer, default=0)
    
    post = relationship('Post', back_populates='comments')
    user = relationship('User', back_populates='comments')

class Analytics(Base):
    __tablename__ = 'analytics'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    event_type = Column(String(50), nullable=False)
    event_data = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', backref='analytics')

def get_engine():
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError(
            "DATABASE_URL environment variable not set. "
            "Please ensure the PostgreSQL database is configured."
        )
    return create_engine(database_url, pool_pre_ping=True)

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)
    return engine
