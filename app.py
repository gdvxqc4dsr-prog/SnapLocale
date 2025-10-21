import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
from database.operations import DatabaseOperations
from utils.helpers import format_engagement_number, calculate_time_ago

# Configure page
st.set_page_config(
    page_title="Sonia Papi - Personal Profile",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'view_count' not in st.session_state:
    st.session_state.view_count = random.randint(1500, 3000)
if 'liked_posts' not in st.session_state:
    st.session_state.liked_posts = set()
if 'gallery_filter' not in st.session_state:
    st.session_state.gallery_filter = "All"
if 'user_id' not in st.session_state:
    st.session_state.user_id = 1
if 'db_error' not in st.session_state:
    st.session_state.db_error = None

# Database operations instance
db = DatabaseOperations()

def load_data():
    """Load data from database with error handling"""
    try:
        profile_data = db.get_profile_data()
        if not profile_data:
            st.error("No profile data found in database. Please ensure the database is seeded.")
            st.stop()
        gallery_data = db.get_gallery_items(user_id=st.session_state.user_id)
        posts_data = db.get_posts(user_id=st.session_state.user_id)
        return profile_data, gallery_data, posts_data
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        st.info("Please ensure DATABASE_URL is set and the database is initialized.")
        st.stop()

def render_profile_header(profile_data, posts_data):
    """Render the profile header section"""
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Avatar placeholder (using emoji since we can't use images)
        st.markdown(
            f"<div style='text-align: center; font-size: 100px;'>👩‍💼</div>", 
            unsafe_allow_html=True
        )
        
        # Profile info
        st.markdown(f"### {profile_data['name']}")
        st.markdown(f"**@{profile_data['username']}**")
        st.markdown(f"*{profile_data['bio']}*")
        
        # Stats
        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
        with stats_col1:
            st.metric("Followers", format_engagement_number(profile_data['followers']))
        with stats_col2:
            st.metric("Following", format_engagement_number(profile_data['following']))
        with stats_col3:
            st.metric("Posts", len(posts_data))
        with stats_col4:
            st.metric("Views", format_engagement_number(st.session_state.view_count))
        
        # Social links
        st.markdown("#### Connect with me:")
        social_cols = st.columns(len(profile_data['social_links']))
        for i, (platform, link) in enumerate(profile_data['social_links'].items()):
            with social_cols[i]:
                st.markdown(f"[{platform.title()}]({link})")

def render_gallery(gallery_data):
    """Render the interactive gallery section"""
    st.markdown("---")
    st.header("📸 Gallery")
    
    # Filter options
    categories = ["All"] + list(set(item['category'] for item in gallery_data))
    selected_category = st.selectbox("Filter by category:", categories, key="gallery_filter_select")
    
    if selected_category != st.session_state.gallery_filter:
        st.session_state.gallery_filter = selected_category
        st.rerun()
    
    # Filter gallery items
    if st.session_state.gallery_filter == "All":
        filtered_items = gallery_data
    else:
        filtered_items = [item for item in gallery_data if item['category'] == st.session_state.gallery_filter]
    
    # Display gallery in grid
    cols_per_row = 3
    for i in range(0, len(filtered_items), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, item in enumerate(filtered_items[i:i+cols_per_row]):
            with cols[j]:
                # Media placeholder (using emojis)
                media_icon = "🎥" if item['type'] == 'video' else "🖼️"
                st.markdown(f"<div style='text-align: center; font-size: 60px;'>{media_icon}</div>", unsafe_allow_html=True)
                st.markdown(f"**{item['title']}**")
                st.markdown(f"*{item['category']}*")
                st.markdown(f"❤️ {item['likes']} | 👁️ {item['views']}")
                
                if st.button(f"View Details", key=f"gallery_{item['id']}"):
                    st.info(f"**{item['title']}**\n\n{item['description']}")

def render_content_feed(profile_data, posts_data):
    """Render the content feed section"""
    st.markdown("---")
    st.header("📱 Latest Posts")
    
    # Sort posts by timestamp (newest first)
    sorted_posts = sorted(posts_data, key=lambda x: x['timestamp'], reverse=True)
    
    for post in sorted_posts:
        with st.container():
            st.markdown("---")
            
            # Post header
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**@{profile_data['username']}**")
                st.markdown(f"*{calculate_time_ago(post['timestamp'])}*")
            with col2:
                st.markdown(f"**{post['type'].title()}**")
            
            # Post content
            st.markdown(post['caption'])
            
            # Post media placeholder
            if post['media_type']:
                media_icon = "🎥" if post['media_type'] == 'video' else "🖼️"
                st.markdown(f"<div style='text-align: center; font-size: 80px;'>{media_icon}</div>", unsafe_allow_html=True)
            
            # Engagement section
            eng_col1, eng_col2, eng_col3, eng_col4 = st.columns(4)
            
            with eng_col1:
                heart_icon = "❤️" if post['id'] in st.session_state.liked_posts else "🤍"
                if st.button(f"{heart_icon} {post['likes']}", key=f"like_{post['id']}"):
                    if post['id'] in st.session_state.liked_posts:
                        st.session_state.liked_posts.remove(post['id'])
                        db.update_likes('post', post['id'], increment=False)
                    else:
                        st.session_state.liked_posts.add(post['id'])
                        db.update_likes('post', post['id'], increment=True)
                    st.rerun()
            
            with eng_col2:
                if st.button(f"💬 {post['comments']}", key=f"view_comments_{post['id']}"):
                    if f"show_comments_{post['id']}" not in st.session_state:
                        st.session_state[f"show_comments_{post['id']}"] = True
                    else:
                        st.session_state[f"show_comments_{post['id']}"] = not st.session_state[f"show_comments_{post['id']}"]
                    st.rerun()
            
            with eng_col3:
                st.markdown(f"🔄 {post['shares']}")
            
            with eng_col4:
                st.markdown(f"👁️ {post['views']}")
            
            # Comments section
            if st.session_state.get(f"show_comments_{post['id']}", False):
                st.markdown("---")
                st.markdown("### 💬 Comments")
                
                # Get existing comments
                comments = db.get_comments_for_post(post['id'])
                
                if comments:
                    for comment in comments:
                        comment_col1, comment_col2 = st.columns([5, 1])
                        with comment_col1:
                            st.markdown(f"**@{comment['user_username']}** · *{calculate_time_ago(comment['timestamp'])}*")
                            st.markdown(comment['content'])
                        with comment_col2:
                            st.markdown(f"❤️ {comment['likes']}")
                        st.markdown("")
                else:
                    st.info("No comments yet. Be the first to comment!")
                
                # Add comment form
                with st.form(f"add_comment_{post['id']}", clear_on_submit=True):
                    comment_text = st.text_area("Add a comment", key=f"comment_input_{post['id']}", height=80)
                    if st.form_submit_button("Post Comment"):
                        if comment_text:
                            try:
                                db.add_comment(post['id'], st.session_state.user_id, comment_text)
                                st.success("Comment added!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error adding comment: {e}")
                        else:
                            st.error("Comment cannot be empty")

def render_contact_info(profile_data):
    """Render contact information section"""
    st.markdown("---")
    st.header("📞 Get in Touch")
    
    contact_col1, contact_col2 = st.columns(2)
    
    with contact_col1:
        st.markdown("### Contact Information")
        st.markdown(f"📧 **Email:** {profile_data['contact']['email']}")
        st.markdown(f"📱 **Phone:** {profile_data['contact']['phone']}")
        st.markdown(f"📍 **Location:** {profile_data['contact']['location']}")
        st.markdown(f"🌐 **Website:** {profile_data['contact']['website']}")
    
    with contact_col2:
        st.markdown("### Send a Message")
        with st.form("contact_form"):
            name = st.text_input("Your Name")
            email = st.text_input("Your Email")
            message = st.text_area("Message", height=100)
            
            if st.form_submit_button("Send Message"):
                if name and email and message:
                    st.success("Message sent successfully! I'll get back to you soon.")
                else:
                    st.error("Please fill in all fields.")

def render_engagement_metrics(profile_data, posts_data):
    """Render engagement metrics dashboard"""
    st.markdown("---")
    st.header("📊 Engagement Analytics Dashboard")
    
    # Track profile view
    db.track_analytics(st.session_state.user_id, 'profile_view')
    
    # Create metrics from posts data
    total_likes = sum(post['likes'] for post in posts_data)
    total_comments = sum(post['comments'] for post in posts_data)
    total_shares = sum(post['shares'] for post in posts_data)
    total_views = sum(post['views'] for post in posts_data)
    
    st.subheader("📈 Overall Performance")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.metric(
            "Total Likes", 
            format_engagement_number(total_likes),
            delta=f"+{random.randint(50, 200)} this week"
        )
    
    with metric_col2:
        st.metric(
            "Total Comments", 
            format_engagement_number(total_comments),
            delta=f"+{random.randint(20, 80)} this week"
        )
    
    with metric_col3:
        st.metric(
            "Total Shares", 
            format_engagement_number(total_shares),
            delta=f"+{random.randint(10, 40)} this week"
        )
    
    with metric_col4:
        st.metric(
            "Total Views", 
            format_engagement_number(total_views),
            delta=f"+{random.randint(500, 2000)} this week"
        )
    
    # Engagement rate
    engagement_rate = ((total_likes + total_comments + total_shares) / total_views * 100) if total_views > 0 else 0
    st.markdown(f"**Overall Engagement Rate:** {engagement_rate:.2f}%")
    
    st.markdown("---")
    
    # Analytics summary
    st.subheader("🎯 Recent Activity (Last 7 Days)")
    analytics_summary = db.get_analytics_summary(st.session_state.user_id, days=7)
    
    anal_col1, anal_col2 = st.columns(2)
    with anal_col1:
        st.metric("Total Events Tracked", analytics_summary['total_events'])
    with anal_col2:
        if analytics_summary['events_by_type']:
            most_common = max(analytics_summary['events_by_type'].items(), key=lambda x: x[1])
            st.metric("Most Common Event", f"{most_common[0]} ({most_common[1]})")
    
    # Event breakdown
    if analytics_summary['events_by_type']:
        st.markdown("### Event Breakdown")
        event_df = pd.DataFrame(list(analytics_summary['events_by_type'].items()), columns=['Event Type', 'Count'])
        st.dataframe(event_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Profile stats
    st.subheader("👥 Profile Statistics")
    prof_col1, prof_col2, prof_col3 = st.columns(3)
    with prof_col1:
        st.metric("Followers", format_engagement_number(profile_data['followers']))
    with prof_col2:
        st.metric("Following", format_engagement_number(profile_data['following']))
    with prof_col3:
        st.metric("Profile Views", format_engagement_number(st.session_state.view_count))

def render_content_management():
    """Render content upload and management section"""
    st.markdown("---")
    st.header("⚙️ Content Management")
    
    mgmt_tab1, mgmt_tab2 = st.tabs(["➕ Add Content", "🗑️ Manage Content"])
    
    with mgmt_tab1:
        st.subheader("Add New Content")
        
        content_type = st.radio("Select content type:", ["Gallery Item", "Post"], horizontal=True)
        
        if content_type == "Gallery Item":
            with st.form("add_gallery_form"):
                st.markdown("### New Gallery Item")
                title = st.text_input("Title *")
                item_type = st.selectbox("Type *", ["image", "video"])
                category = st.selectbox("Category *", ["Travel", "Lifestyle", "Photography", "Fashion", "Food", "Fitness", "Other"])
                description = st.text_area("Description", height=100)
                
                submitted = st.form_submit_button("Add Gallery Item")
                if submitted:
                    if title and item_type and category:
                        try:
                            item_id = db.add_gallery_item(
                                user_id=st.session_state.user_id,
                                title=title,
                                item_type=item_type,
                                category=category,
                                description=description
                            )
                            st.success(f"✅ Gallery item '{title}' added successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error adding gallery item: {e}")
                    else:
                        st.error("Please fill in all required fields (*)")
        
        else:
            with st.form("add_post_form"):
                st.markdown("### New Post")
                caption = st.text_area("Caption *", height=100)
                post_type = st.selectbox("Post Type *", ["post", "story"])
                media_type = st.selectbox("Media Type", ["None", "image", "video"])
                
                submitted = st.form_submit_button("Create Post")
                if submitted:
                    if caption and post_type:
                        try:
                            media_val = None if media_type == "None" else media_type
                            post_id = db.add_post(
                                user_id=st.session_state.user_id,
                                caption=caption,
                                post_type=post_type,
                                media_type=media_val
                            )
                            st.success(f"✅ Post created successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error creating post: {e}")
                    else:
                        st.error("Please fill in all required fields (*)")
    
    with mgmt_tab2:
        st.subheader("Manage Existing Content")
        
        manage_type = st.radio("Content type:", ["Gallery Items", "Posts"], horizontal=True)
        
        if manage_type == "Gallery Items":
            st.markdown("### Gallery Items")
            gallery_items = db.get_gallery_items(user_id=st.session_state.user_id)
            
            if gallery_items:
                for item in gallery_items:
                    with st.expander(f"{item['title']} ({item['category']})"):
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(f"**Type:** {item['type']}")
                            st.markdown(f"**Description:** {item['description']}")
                            st.markdown(f"**Likes:** {item['likes']} | **Views:** {item['views']}")
                            st.markdown(f"**Uploaded:** {item['upload_date']}")
                        
                        with col2:
                            if st.button("✏️ Edit", key=f"edit_gallery_{item['id']}"):
                                st.session_state[f"editing_gallery_{item['id']}"] = True
                                st.rerun()
                            if st.button("🗑️ Delete", key=f"delete_gallery_{item['id']}"):
                                if db.delete_gallery_item(item['id']):
                                    st.success("Gallery item deleted!")
                                    st.rerun()
                                else:
                                    st.error("Failed to delete gallery item")
                        
                        # Edit form
                        if st.session_state.get(f"editing_gallery_{item['id']}", False):
                            st.markdown("---")
                            st.markdown("**Edit Gallery Item**")
                            with st.form(f"edit_gallery_form_{item['id']}"):
                                edit_title = st.text_input("Title", value=item['title'])
                                edit_type = st.selectbox("Type", ["image", "video"], index=0 if item['type'] == 'image' else 1)
                                categories = ["Travel", "Lifestyle", "Photography", "Fashion", "Food", "Fitness", "Other"]
                                edit_category = st.selectbox("Category", categories, index=categories.index(item['category']) if item['category'] in categories else 0)
                                edit_desc = st.text_area("Description", value=item['description'] or '', height=100)
                                
                                col_save, col_cancel = st.columns(2)
                                with col_save:
                                    if st.form_submit_button("💾 Save Changes"):
                                        try:
                                            db.update_gallery_item(item['id'], edit_title, edit_type, edit_category, edit_desc)
                                            st.session_state[f"editing_gallery_{item['id']}"] = False
                                            st.success("Gallery item updated!")
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"Error updating: {e}")
                                with col_cancel:
                                    if st.form_submit_button("❌ Cancel"):
                                        st.session_state[f"editing_gallery_{item['id']}"] = False
                                        st.rerun()
            else:
                st.info("No gallery items found.")
        
        else:
            st.markdown("### Posts")
            posts = db.get_posts(user_id=st.session_state.user_id)
            
            if posts:
                for post in posts:
                    with st.expander(f"{post['caption'][:50]}... ({calculate_time_ago(post['timestamp'])})"):
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(f"**Full Caption:** {post['caption']}")
                            st.markdown(f"**Type:** {post['type']} | **Media:** {post['media_type'] or 'None'}")
                            st.markdown(f"**Engagement:** ❤️ {post['likes']} | 💬 {post['comments']} | 🔄 {post['shares']} | 👁️ {post['views']}")
                        
                        with col2:
                            if st.button("✏️ Edit", key=f"edit_post_{post['id']}"):
                                st.session_state[f"editing_post_{post['id']}"] = True
                                st.rerun()
                            if st.button("🗑️ Delete", key=f"delete_post_{post['id']}"):
                                if db.delete_post(post['id']):
                                    st.success("Post deleted!")
                                    st.rerun()
                                else:
                                    st.error("Failed to delete post")
                        
                        # Edit form
                        if st.session_state.get(f"editing_post_{post['id']}", False):
                            st.markdown("---")
                            st.markdown("**Edit Post**")
                            with st.form(f"edit_post_form_{post['id']}"):
                                edit_caption = st.text_area("Caption", value=post['caption'], height=100)
                                edit_post_type = st.selectbox("Post Type", ["post", "story"], index=0 if post['type'] == 'post' else 1)
                                media_options = ["None", "image", "video"]
                                current_media = post['media_type'] or "None"
                                edit_media_type = st.selectbox("Media Type", media_options, index=media_options.index(current_media) if current_media in media_options else 0)
                                
                                col_save, col_cancel = st.columns(2)
                                with col_save:
                                    if st.form_submit_button("💾 Save Changes"):
                                        try:
                                            media_val = None if edit_media_type == "None" else edit_media_type
                                            db.update_post(post['id'], edit_caption, edit_post_type, media_val)
                                            st.session_state[f"editing_post_{post['id']}"] = False
                                            st.success("Post updated!")
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"Error updating: {e}")
                                with col_cancel:
                                    if st.form_submit_button("❌ Cancel"):
                                        st.session_state[f"editing_post_{post['id']}"] = False
                                        st.rerun()
            else:
                st.info("No posts found.")

def render_search():
    """Render search functionality"""
    st.markdown("---")
    st.header("🔍 Search Content")
    
    search_query = st.text_input("Search posts and gallery items:", placeholder="Enter keywords...")
    search_type = st.radio("Search in:", ["All", "Posts Only", "Gallery Only"], horizontal=True)
    
    if search_query:
        search_type_map = {
            "All": "all",
            "Posts Only": "posts",
            "Gallery Only": "gallery"
        }
        
        results = db.search_content(search_query, search_type_map[search_type])
        
        st.markdown("---")
        st.subheader(f"Search Results for: '{search_query}'")
        
        # Display posts results
        if results['posts']:
            st.markdown(f"### 📱 Posts ({len(results['posts'])} found)")
            for post in results['posts']:
                with st.expander(f"{post['caption'][:100]}..."):
                    st.markdown(f"**Full Caption:** {post['caption']}")
                    st.markdown(f"**Type:** {post['type']}")
                    st.markdown(f"**Posted:** {calculate_time_ago(post['timestamp'])}")
        elif search_type in ["All", "Posts Only"]:
            st.info("No posts found matching your search.")
        
        # Display gallery results
        if results['gallery']:
            st.markdown(f"### 📸 Gallery ({len(results['gallery'])} found)")
            cols = st.columns(3)
            for idx, item in enumerate(results['gallery']):
                with cols[idx % 3]:
                    media_icon = "🎥" if item['type'] == 'video' else "🖼️"
                    st.markdown(f"<div style='text-align: center; font-size: 50px;'>{media_icon}</div>", unsafe_allow_html=True)
                    st.markdown(f"**{item['title']}**")
                    st.markdown(f"*{item['category']}*")
        elif search_type in ["All", "Gallery Only"]:
            st.info("No gallery items found matching your search.")
        
        if not results['posts'] and not results['gallery']:
            st.warning("No results found. Try different keywords.")
    else:
        st.info("Enter a search query above to find posts and gallery items.")

def render_category_pages():
    """Render multi-page navigation for different content categories"""
    st.markdown("---")
    st.header("📂 Browse by Category")
    
    # Get unique categories from gallery
    gallery_items = db.get_gallery_items(user_id=st.session_state.user_id)
    categories = list(set(item['category'] for item in gallery_items))
    
    if categories:
        selected_category = st.selectbox("Select a category:", ["All"] + sorted(categories))
        
        st.markdown("---")
        st.subheader(f"Category: {selected_category}")
        
        # Filter by category
        if selected_category == "All":
            filtered_items = gallery_items
        else:
            filtered_items = [item for item in gallery_items if item['category'] == selected_category]
        
        if filtered_items:
            st.markdown(f"*{len(filtered_items)} items found*")
            
            # Display in grid
            cols_per_row = 3
            for i in range(0, len(filtered_items), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, item in enumerate(filtered_items[i:i+cols_per_row]):
                    with cols[j]:
                        media_icon = "🎥" if item['type'] == 'video' else "🖼️"
                        st.markdown(f"<div style='text-align: center; font-size: 60px;'>{media_icon}</div>", unsafe_allow_html=True)
                        st.markdown(f"**{item['title']}**")
                        st.markdown(f"*{item['category']}*")
                        st.markdown(f"❤️ {item['likes']} | 👁️ {item['views']}")
                        
                        if st.button("View", key=f"cat_view_{item['id']}"):
                            st.info(f"**{item['title']}**\n\n{item['description']}")
        else:
            st.info(f"No items found in category '{selected_category}'")
    else:
        st.info("No categories available yet. Add some gallery items first!")

# Main app layout
def main():
    # Load data with error handling
    profile_data, gallery_data, posts_data = load_data()
    
    # Increment view count
    st.session_state.view_count += random.randint(1, 5)
    
    # App title
    st.title("👤 Personal Profile - Sonia Papi")
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "🏠 Profile", "📸 Gallery", "📱 Feed", "📞 Contact", 
        "📊 Analytics", "⚙️ Manage", "🔍 Search", "📂 Categories"
    ])
    
    with tab1:
        render_profile_header(profile_data, posts_data)
    
    with tab2:
        render_gallery(gallery_data)
    
    with tab3:
        render_content_feed(profile_data, posts_data)
    
    with tab4:
        render_contact_info(profile_data)
    
    with tab5:
        render_engagement_metrics(profile_data, posts_data)
    
    with tab6:
        render_content_management()
    
    with tab7:
        render_search()
    
    with tab8:
        render_category_pages()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "© 2025 Sonia Papi. Built with Streamlit."
        "</div>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
