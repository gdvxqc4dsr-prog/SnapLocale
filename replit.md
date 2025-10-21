# Sonia Papi - Personal Profile Application

## Overview

This is a personal profile web application built with Streamlit that showcases a social media-style profile for "Sonia Papi". The application displays user information, posts, gallery items, and engagement metrics similar to popular social media platforms. It uses a PostgreSQL database (via SQLAlchemy ORM) for data persistence and provides an interactive interface for viewing content, managing likes, and filtering media.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit - A Python-based web framework for rapid development of data applications
- **Rendering Pattern**: Server-side rendering with session state management for user interactions
- **State Management**: Streamlit's built-in session state stores user-specific data (liked posts, filters, view counts)
- **Layout**: Wide layout with collapsed sidebar, using Streamlit's column system for responsive design
- **Component Structure**: Modular rendering functions (e.g., `render_profile_header`) separate UI concerns

**Rationale**: Streamlit was chosen for its simplicity and rapid prototyping capabilities, allowing quick development of an interactive profile interface without requiring separate frontend/backend codebases.

### Backend Architecture
- **Language**: Python 3.x
- **ORM**: SQLAlchemy for database abstraction and object-relational mapping
- **Data Access Layer**: `DatabaseOperations` class provides static methods for all database interactions
- **Error Handling**: Try-catch blocks with user-friendly error messages displayed through Streamlit's UI components

**Design Pattern**: The application follows a simple layered architecture:
1. Presentation Layer (app.py) - Streamlit UI components
2. Business Logic Layer (database/operations.py) - Database operations and data transformation
3. Data Layer (database/schema.py) - ORM models and database schema
4. Utility Layer (utils/helpers.py) - Reusable helper functions

**Rationale**: This separation of concerns makes the codebase maintainable and allows for easy testing and modification of individual layers.

### Data Storage
- **Database**: PostgreSQL (configurable via DATABASE_URL environment variable)
- **ORM Models**: 
  - `User` - Core user profile information
  - `SocialLink` - External social media platform links
  - `Post` - User-generated posts with engagement metrics
  - `GalleryItem` - Media gallery items (images/videos)
  - `Comment` - User comments on posts
  - `Analytics` - Engagement and analytics data

**Schema Design**:
- Relational model with foreign key relationships
- One-to-many relationships between User and their content (posts, gallery items, comments)
- Cascade delete to maintain referential integrity
- Timestamp fields for temporal tracking

**Rationale**: PostgreSQL was chosen for its robustness and ACID compliance. SQLAlchemy provides database abstraction, making it easier to switch databases if needed while maintaining clean Python code.

### Authentication & Authorization
- **Current Implementation**: Simple user ID-based session tracking
- **No Authentication**: The application currently does not implement user authentication or login functionality
- **Session Management**: Uses Streamlit session state to track the current user (defaults to user_id=1)

**Note**: This is a single-user profile application without multi-user authentication. Any authentication would need to be added as a future enhancement.

### Data Seeding
- **Seed Module**: `database/seed_data.py` provides initial data population
- **Idempotent Seeding**: Checks for existing data before inserting to prevent duplicates
- **Seed Data**: Pre-populates user profile, social links, gallery items, and posts

**Rationale**: Database seeding ensures the application has demonstration data and can be quickly set up in new environments.

## External Dependencies

### Third-Party Packages
- **streamlit**: Core web application framework
- **pandas**: Data manipulation and analysis (used for tabular data handling)
- **sqlalchemy**: SQL toolkit and ORM for database operations
- **psycopg2** (implied): PostgreSQL database adapter for Python

### External Services
- **PostgreSQL Database**: Primary data store accessed via DATABASE_URL environment variable
- **Social Media Platforms**: The application displays links to external platforms:
  - Snapchat
  - Instagram
  - Twitter
  - LinkedIn
  - TikTok

**Note**: These are display-only links; no API integrations with social platforms are currently implemented.

### Environment Configuration
- **DATABASE_URL**: Required environment variable for PostgreSQL connection string
- **Error Handling**: Application provides user-friendly messages when DATABASE_URL is not configured

### Data Layer Dependencies
- Database initialization handled through `init_db()` function
- Session management via `get_session()` factory pattern
- Support for connection pooling and transaction management through SQLAlchemy

**Rationale**: Environment-based configuration allows for different database connections across development, staging, and production environments without code changes.