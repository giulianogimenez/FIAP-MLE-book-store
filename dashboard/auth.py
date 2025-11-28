"""
Authentication module for Streamlit dashboard
"""
import streamlit as st
import requests


def check_authentication():
    """
    Check if user is authenticated and has admin role
    Shows login form if not authenticated
    """
    # Check if already authenticated
    if st.session_state.get('authenticated', False):
        # Verify role is admin
        if st.session_state.get('role') != 'admin':
            st.error("🚫 Access Denied: Admin role required")
            st.stop()
        return True
    
    # Show login form
    show_login_form()
    return False


def show_login_form():
    """Display login form"""
    st.markdown(
        """
        <div style='text-align: center; padding: 2rem;'>
            <h1>🔐 Admin Dashboard Login</h1>
            <p>Book Store API - Admin Access Only</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔑 Enter Admin Credentials")
        
        # Environment selector
        environment = st.selectbox(
            "Environment",
            ["Production", "Staging", "Local"],
            key="login_environment"
        )
        
        env_urls = {
            "Production": "https://fiap-mle-bookstore-prod-d748bdd0abdc.herokuapp.com",
            "Staging": "https://fiap-mle-bookstore-staging-d571c9f02bed.herokuapp.com",
            "Local": "http://localhost:5000"
        }
        
        api_url = env_urls[environment]
        st.info(f"🌐 API URL: {api_url}")
        
        with st.form("login_form"):
            username = st.text_input(
                "Username",
                placeholder="admin",
                help="Enter your admin username"
            )
            
            password = st.text_input(
                "Password",
                type="password",
                placeholder="••••••••",
                help="Enter your password"
            )
            
            submitted = st.form_submit_button("🔐 Login", use_container_width=True)
            
            if submitted:
                if not username or not password:
                    st.error("❌ Please enter both username and password")
                else:
                    # Authenticate
                    success, message, user_data = authenticate(api_url, username, password)
                    
                    if success:
                        # Check if user is admin
                        if user_data.get('user', {}).get('role') != 'admin':
                            st.error("🚫 Access Denied: Admin role required")
                        else:
                            # Store session data
                            st.session_state['authenticated'] = True
                            st.session_state['username'] = username
                            st.session_state['role'] = user_data['user']['role']
                            st.session_state['access_token'] = user_data['access_token']
                            st.session_state['refresh_token'] = user_data['refresh_token']
                            st.session_state['api_url'] = api_url
                            
                            st.success(f"✅ {message}")
                            st.rerun()
                    else:
                        st.error(f"❌ {message}")
        
        # Help section
        with st.expander("ℹ️ Default Credentials"):
            st.markdown("""
            **Default Admin Credentials:**
            - Username: `admin`
            - Password: `admin123`
            
            ⚠️ **Note**: Change these credentials in production!
            """)


def authenticate(api_url, username, password):
    """
    Authenticate user against the API
    
    Args:
        api_url: Base URL of the API
        username: Username
        password: Password
        
    Returns:
        tuple: (success, message, user_data)
    """
    try:
        response = requests.post(
            f"{api_url}/api/v1/auth/login",
            json={"username": username, "password": password},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return True, "Login successful", data
        elif response.status_code == 401:
            return False, "Invalid credentials", None
        else:
            return False, f"Login failed (Status: {response.status_code})", None
            
    except requests.exceptions.ConnectionError:
        return False, f"Could not connect to API at {api_url}", None
    except requests.exceptions.Timeout:
        return False, "Request timeout - API not responding", None
    except Exception as e:
        return False, f"Error: {str(e)}", None


def logout():
    """Clear session and logout user"""
    # Clear all session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    st.session_state['authenticated'] = False
    st.success("✅ Logged out successfully")

