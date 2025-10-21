import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
from data.profile_data import get_profile_data, get_gallery_data, get_posts_data
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

# Load data
profile_data = get_profile_data()
gallery_data = get_gallery_data()
posts_data = get_posts_data()

def render_profile_header():
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

def render_gallery():
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

def render_content_feed():
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
                        post['likes'] -= 1
                    else:
                        st.session_state.liked_posts.add(post['id'])
                        post['likes'] += 1
                    st.rerun()
            
            with eng_col2:
                st.markdown(f"💬 {post['comments']}")
            
            with eng_col3:
                st.markdown(f"🔄 {post['shares']}")
            
            with eng_col4:
                st.markdown(f"👁️ {post['views']}")

def render_contact_info():
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

def render_engagement_metrics():
    """Render engagement metrics dashboard"""
    st.markdown("---")
    st.header("📊 Engagement Metrics")
    
    # Create metrics from posts data
    total_likes = sum(post['likes'] for post in posts_data)
    total_comments = sum(post['comments'] for post in posts_data)
    total_shares = sum(post['shares'] for post in posts_data)
    total_views = sum(post['views'] for post in posts_data)
    
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

# Main app layout
def main():
    # Increment view count
    st.session_state.view_count += random.randint(1, 5)
    
    # App title
    st.title("👤 Personal Profile - Sonia Papi")
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Profile", "📸 Gallery", "📱 Feed", "📞 Contact", "📊 Analytics"])
    
    with tab1:
        render_profile_header()
    
    with tab2:
        render_gallery()
    
    with tab3:
        render_content_feed()
    
    with tab4:
        render_contact_info()
    
    with tab5:
        render_engagement_metrics()
    
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
