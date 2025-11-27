"""
Exemplo completo de autenticação e uso do endpoint de scraping
"""
import requests
import time
import json

BASE_URL = "http://localhost:5000/api/v1"


def example_login():
    """Exemplo de login"""
    print("=" * 60)
    print("1. LOGIN")
    print("=" * 60)
    
    # Login como admin
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Login successful!")
        print(f"   User: {data['user']['username']}")
        print(f"   Role: {data['user']['role']}")
        print(f"   Access Token: {data['access_token'][:50]}...")
        return data['access_token'], data['refresh_token']
    else:
        print("❌ Login failed!")
        print(f"   Error: {response.json()}")
        return None, None


def example_get_user_info(access_token):
    """Exemplo de obter informações do usuário"""
    print("\n" + "=" * 60)
    print("2. GET USER INFO")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(
        f"{BASE_URL}/auth/me",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ User info retrieved!")
        print(f"   Username: {data['user']['username']}")
        print(f"   Role: {data['user']['role']}")
    else:
        print("❌ Failed to get user info!")


def example_trigger_scraping(access_token):
    """Exemplo de iniciar scraping"""
    print("\n" + "=" * 60)
    print("3. TRIGGER SCRAPING")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "pages": 2,
        "format": "both",
        "output": "example_books"
    }
    
    print(f"📤 Sending request: {json.dumps(payload, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/scraping/trigger",
        json=payload,
        headers=headers
    )
    
    if response.status_code == 202:
        data = response.json()
        print("✅ Scraping job started!")
        print(f"   Job ID: {data['job_id']}")
        print(f"   Pages: {data['parameters']['pages']}")
        print(f"   Format: {data['parameters']['format']}")
        return data['job_id']
    else:
        print("❌ Failed to start scraping!")
        print(f"   Error: {response.json()}")
        return None


def example_check_job_status(access_token, job_id):
    """Exemplo de verificar status do job"""
    print("\n" + "=" * 60)
    print("4. CHECK JOB STATUS")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    print(f"⏳ Waiting for job {job_id} to complete...")
    
    max_attempts = 10
    for attempt in range(max_attempts):
        time.sleep(3)  # Wait 3 seconds between checks
        
        response = requests.get(
            f"{BASE_URL}/scraping/jobs/{job_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            status = data['status']
            
            print(f"   Attempt {attempt + 1}/{max_attempts}: Status = {status}")
            
            if status == 'completed':
                print("\n✅ Scraping completed!")
                print(f"   Books collected: {data['results']['books_count']}")
                print(f"   Files saved:")
                for file in data['results']['files']:
                    print(f"      - {file}")
                return True
            elif status == 'failed':
                print("\n❌ Scraping failed!")
                print(f"   Error: {data.get('error')}")
                return False
        else:
            print(f"❌ Failed to check status: {response.json()}")
            return False
    
    print("\n⚠️  Job still running after maximum attempts")
    return False


def example_list_jobs(access_token):
    """Exemplo de listar jobs"""
    print("\n" + "=" * 60)
    print("5. LIST ALL JOBS")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(
        f"{BASE_URL}/scraping/jobs",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data['total']} jobs:")
        for job in data['jobs']:
            print(f"   - {job['job_id']}: {job['status']} ({job['pages']} pages)")
    else:
        print("❌ Failed to list jobs!")


def example_refresh_token(refresh_token):
    """Exemplo de renovar token"""
    print("\n" + "=" * 60)
    print("6. REFRESH TOKEN")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {refresh_token}"
    }
    
    response = requests.post(
        f"{BASE_URL}/auth/refresh",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Token refreshed!")
        print(f"   New Access Token: {data['access_token'][:50]}...")
        return data['access_token']
    else:
        print("❌ Failed to refresh token!")
        return None


def example_without_auth():
    """Exemplo de tentar acessar sem autenticação"""
    print("\n" + "=" * 60)
    print("7. TRY WITHOUT AUTH (should fail)")
    print("=" * 60)
    
    response = requests.post(
        f"{BASE_URL}/scraping/trigger",
        json={"pages": 1}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")


def example_user_try_scraping():
    """Exemplo de usuário regular tentando fazer scraping"""
    print("\n" + "=" * 60)
    print("8. TRY AS REGULAR USER (should fail)")
    print("=" * 60)
    
    # Login as user
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "username": "user",
            "password": "user123"
        }
    )
    
    if login_response.status_code == 200:
        user_token = login_response.json()['access_token']
        
        # Try to trigger scraping
        headers = {
            "Authorization": f"Bearer {user_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            f"{BASE_URL}/scraping/trigger",
            json={"pages": 1},
            headers=headers
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")


if __name__ == "__main__":
    print("\n🚀 BOOK STORE API - Authentication & Scraping Examples\n")
    
    try:
        # 1. Login
        access_token, refresh_token = example_login()
        
        if not access_token:
            print("\n❌ Cannot proceed without authentication")
            exit(1)
        
        # 2. Get user info
        example_get_user_info(access_token)
        
        # 3. Trigger scraping
        job_id = example_trigger_scraping(access_token)
        
        if job_id:
            # 4. Check job status
            example_check_job_status(access_token, job_id)
        
        # 5. List all jobs
        example_list_jobs(access_token)
        
        # 6. Refresh token
        new_access_token = example_refresh_token(refresh_token)
        
        # 7. Try without auth
        example_without_auth()
        
        # 8. Try as regular user
        example_user_try_scraping()
        
        print("\n" + "=" * 60)
        print("✅ ALL EXAMPLES COMPLETED")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API")
        print("   Make sure the API is running:")
        print("   python run_api.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

