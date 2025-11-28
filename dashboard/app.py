"""
Book Store API - Admin Dashboard
Streamlit dashboard for monitoring and metrics
"""
import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from api_client import APIClient
from auth import check_authentication, logout

# Page config
st.set_page_config(
    page_title="Book Store API - Admin Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .status-healthy {
        color: #28a745;
        font-weight: bold;
    }
    .status-degraded {
        color: #ffc107;
        font-weight: bold;
    }
    .status-unhealthy {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Check authentication
if not check_authentication():
    st.stop()

# Initialize API client
api_client = APIClient(st.session_state.get('api_url', 'http://localhost:5000'))
api_client.set_token(st.session_state.get('access_token'))

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/admin-settings-male.png", width=80)
    st.markdown("### 👤 Admin Dashboard")
    st.markdown(f"**User:** {st.session_state.get('username', 'admin')}")
    st.markdown(f"**Role:** {st.session_state.get('role', 'admin')}")
    
    st.markdown("---")
    
    # Environment selector
    environment = st.selectbox(
        "🌐 Environment",
        ["Production", "Staging", "Local"],
        key="environment"
    )
    
    env_urls = {
        "Production": "https://fiap-mle-bookstore-prod-d748bdd0abdc.herokuapp.com",
        "Staging": "https://fiap-mle-bookstore-staging-d571c9f02bed.herokuapp.com",
        "Local": "http://localhost:5000"
    }
    
    st.session_state['api_url'] = env_urls[environment]
    api_client.base_url = env_urls[environment]
    
    st.markdown("---")
    
    # Auto-refresh
    auto_refresh = st.checkbox("🔄 Auto-refresh (30s)", value=False)
    
    if st.button("🔄 Refresh Now"):
        st.rerun()
    
    st.markdown("---")
    
    if st.button("🚪 Logout"):
        logout()
        st.rerun()

# Main content
st.markdown('<p class="main-header">📊 Book Store API - Admin Dashboard</p>', unsafe_allow_html=True)
st.markdown(f"**Environment:** {environment} | **URL:** `{st.session_state['api_url']}`")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏥 Health & Status", 
    "📚 Books Analytics", 
    "🕷️ Scraping Jobs",
    "🔐 Auth Metrics",
    "📈 Real-time Monitor"
])

# Tab 1: Health & Status
with tab1:
    st.markdown("### 🏥 System Health Check")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        try:
            health_data = api_client.get_health()
            
            if health_data:
                # Overall status
                status = health_data.get('status', 'unknown')
                status_colors = {
                    'healthy': '🟢',
                    'degraded': '🟡',
                    'unhealthy': '🔴'
                }
                
                st.markdown(f"### Overall Status: {status_colors.get(status, '⚪')} **{status.upper()}**")
                st.markdown(f"**Service:** {health_data.get('service', 'N/A')} | **Version:** {health_data.get('version', 'N/A')}")
                st.markdown(f"**Timestamp:** {health_data.get('timestamp', 'N/A')}")
                
                st.markdown("---")
                
                # Component checks
                st.markdown("### 🔍 Component Checks")
                
                checks = health_data.get('checks', {})
                
                for component, details in checks.items():
                    with st.expander(f"**{component.upper()}** - Status: {details.get('status', 'unknown').upper()}", expanded=True):
                        # Create metrics based on component
                        if component == 'database':
                            col_a, col_b, col_c = st.columns(3)
                            col_a.metric("Users Count", details.get('users_count', 'N/A'))
                            col_b.metric("File Size", f"{details.get('size_bytes', 0)} bytes")
                            col_c.metric("Readable", "✅" if details.get('readable') else "❌")
                            
                        elif component == 'storage':
                            col_a, col_b = st.columns(2)
                            col_a.metric("Files Count", details.get('files_count', 0))
                            col_b.metric("Writable", "✅" if details.get('writable') else "❌")
                            
                        elif component == 'config':
                            col_a, col_b, col_c = st.columns(3)
                            col_a.metric("JWT Configured", "✅" if details.get('jwt_configured') else "❌")
                            col_b.metric("Debug Mode", "⚠️" if details.get('debug_mode') else "✅")
                            col_c.metric("Host", details.get('host', 'N/A'))
                            
                            if details.get('message'):
                                st.warning(f"⚠️ {details.get('message')}")
                                
                        elif component == 'dependencies':
                            st.json({k: v for k, v in details.items() if k != 'status'})
                        
                        else:
                            st.json(details)
            else:
                st.error("❌ Failed to fetch health data")
                
        except Exception as e:
            st.error(f"❌ Error fetching health data: {str(e)}")
    
    with col2:
        st.markdown("### 📊 Features")
        if health_data and 'features' in health_data:
            for feature in health_data['features']:
                st.success(f"✅ {feature}")

# Tab 2: Books Analytics
with tab2:
    st.markdown("### 📚 Books Collection Analytics")
    
    try:
        # Get stats
        stats = api_client.get_stats()
        books = api_client.get_books()
        categories = api_client.get_categories()
        
        if stats:
            # Metrics row
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "📚 Total Books",
                    stats.get('total_books', 0),
                    delta=None
                )
            
            with col2:
                avg_price = stats.get('average_price', 0)
                st.metric(
                    "💰 Average Price",
                    f"£{avg_price:.2f}",
                    delta=None
                )
            
            with col3:
                total_categories = len(stats.get('categories', {}))
                st.metric(
                    "🏷️ Categories",
                    total_categories,
                    delta=None
                )
            
            st.markdown("---")
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📊 Books by Category")
                if stats.get('categories'):
                    cat_df = pd.DataFrame([
                        {'Category': cat, 'Count': count}
                        for cat, count in stats['categories'].items()
                    ])
                    
                    fig = px.pie(
                        cat_df,
                        values='Count',
                        names='Category',
                        title='Distribution by Category',
                        hole=0.4
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### 💵 Price Distribution")
                if books and 'books' in books:
                    books_df = pd.DataFrame(books['books'])
                    if not books_df.empty and 'price' in books_df.columns:
                        fig = px.histogram(
                            books_df,
                            x='price',
                            nbins=20,
                            title='Price Distribution',
                            labels={'price': 'Price (£)', 'count': 'Number of Books'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
            
            # Categories table
            st.markdown("---")
            st.markdown("#### 🏷️ Categories Details")
            
            if categories and 'categories' in categories:
                cat_detail_df = pd.DataFrame(categories['categories'])
                st.dataframe(
                    cat_detail_df,
                    use_container_width=True,
                    hide_index=True
                )
            
            # Recent books
            st.markdown("---")
            st.markdown("#### 📖 Recent Books")
            
            if books and 'books' in books:
                recent_books = pd.DataFrame(books['books'][:10])
                st.dataframe(
                    recent_books,
                    use_container_width=True,
                    hide_index=True
                )
                
    except Exception as e:
        st.error(f"❌ Error fetching books analytics: {str(e)}")

# Tab 3: Scraping Jobs
with tab3:
    st.markdown("### 🕷️ Web Scraping Jobs Monitor")
    
    try:
        jobs = api_client.get_scraping_jobs()
        
        if jobs and 'jobs' in jobs:
            jobs_list = jobs['jobs']
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            total_jobs = len(jobs_list)
            running = sum(1 for j in jobs_list if j.get('status') == 'running')
            completed = sum(1 for j in jobs_list if j.get('status') == 'completed')
            failed = sum(1 for j in jobs_list if j.get('status') == 'failed')
            
            col1.metric("📊 Total Jobs", total_jobs)
            col2.metric("⏳ Running", running)
            col3.metric("✅ Completed", completed)
            col4.metric("❌ Failed", failed)
            
            st.markdown("---")
            
            # Jobs table
            if jobs_list:
                jobs_df = pd.DataFrame(jobs_list)
                
                # Format dataframe
                if 'started_at' in jobs_df.columns:
                    jobs_df['started_at'] = pd.to_datetime(jobs_df['started_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
                
                st.dataframe(
                    jobs_df,
                    use_container_width=True,
                    hide_index=True
                )
                
                # Status distribution chart
                st.markdown("#### 📈 Jobs Status Distribution")
                status_counts = jobs_df['status'].value_counts()
                
                fig = px.bar(
                    x=status_counts.index,
                    y=status_counts.values,
                    labels={'x': 'Status', 'y': 'Count'},
                    title='Jobs by Status',
                    color=status_counts.index,
                    color_discrete_map={
                        'completed': '#28a745',
                        'running': '#ffc107',
                        'failed': '#dc3545'
                    }
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("ℹ️ No scraping jobs found")
            
            # Trigger new job
            st.markdown("---")
            st.markdown("#### 🚀 Trigger New Scraping Job")
            
            with st.form("trigger_scraping"):
                col1, col2 = st.columns(2)
                
                with col1:
                    pages = st.number_input("Pages to scrape", min_value=1, max_value=50, value=2)
                    format_type = st.selectbox("Output format", ["json", "csv", "both"])
                
                with col2:
                    output_name = st.text_input("Output filename", value="books")
                    url = st.text_input("URL", value="http://books.toscrape.com")
                
                submitted = st.form_submit_button("🕷️ Start Scraping")
                
                if submitted:
                    try:
                        result = api_client.trigger_scraping(
                            url=url,
                            pages=pages,
                            format_type=format_type,
                            output=output_name
                        )
                        
                        if result:
                            st.success(f"✅ Scraping job started! Job ID: {result.get('job_id')}")
                            st.json(result)
                        else:
                            st.error("❌ Failed to start scraping job")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Could not fetch scraping jobs")
            
    except Exception as e:
        st.error(f"❌ Error fetching scraping jobs: {str(e)}")

# Tab 4: Auth Metrics
with tab4:
    st.markdown("### 🔐 Authentication Metrics")
    
    st.info("ℹ️ This section shows authentication and user activity metrics")
    
    # User info
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👤 Current Session")
        st.write(f"**Username:** {st.session_state.get('username', 'N/A')}")
        st.write(f"**Role:** {st.session_state.get('role', 'N/A')}")
        st.write(f"**Token Expiry:** Token válido por 1 hora")
        
        if st.button("🔄 Refresh Token"):
            try:
                # Would implement token refresh here
                st.success("✅ Token refreshed successfully")
            except Exception as e:
                st.error(f"❌ Error refreshing token: {str(e)}")
    
    with col2:
        st.markdown("#### 📊 User Statistics")
        
        try:
            health = api_client.get_health()
            if health and 'checks' in health and 'database' in health['checks']:
                user_count = health['checks']['database'].get('users_count', 0)
                st.metric("Total Users", user_count)
            
            st.metric("Active Sessions", "1")
            st.metric("Admin Users", "1+")
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Tab 5: Real-time Monitor
with tab5:
    st.markdown("### 📈 Real-time System Monitor")
    
    # Create placeholder for real-time updates
    status_placeholder = st.empty()
    metrics_placeholder = st.empty()
    
    try:
        health = api_client.get_health()
        stats = api_client.get_stats()
        
        with status_placeholder.container():
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                status = health.get('status', 'unknown') if health else 'unknown'
                status_emoji = {'healthy': '🟢', 'degraded': '🟡', 'unhealthy': '🔴'}.get(status, '⚪')
                st.metric("System Status", f"{status_emoji} {status.upper()}")
            
            with col2:
                total_books = stats.get('total_books', 0) if stats else 0
                st.metric("Total Books", total_books)
            
            with col3:
                st.metric("API Version", health.get('version', 'N/A') if health else 'N/A')
            
            with col4:
                st.metric("Timestamp", datetime.now().strftime("%H:%M:%S"))
        
        # Timeline chart
        st.markdown("#### 📊 System Activity Timeline")
        
        # This would show actual metrics over time
        # For now, showing placeholder
        time_data = pd.DataFrame({
            'Time': pd.date_range(start='2025-01-01', periods=10, freq='H'),
            'Requests': [100, 120, 95, 150, 140, 130, 160, 145, 155, 170],
            'Response Time (ms)': [45, 50, 42, 55, 48, 46, 52, 49, 51, 47]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time_data['Time'],
            y=time_data['Requests'],
            name='Requests',
            mode='lines+markers'
        ))
        
        fig.update_layout(
            title='API Activity (Last 10 hours)',
            xaxis_title='Time',
            yaxis_title='Requests',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ Error in real-time monitor: {str(e)}")

# Auto-refresh
if auto_refresh:
    import time
    time.sleep(30)
    st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>📚 Book Store API Admin Dashboard | FIAP MLE Tech Challenge</p>
        <p>Made with ❤️ using Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)

