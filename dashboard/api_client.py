"""
API Client for Book Store API
Handles all API requests from the dashboard
"""
import requests
from typing import Optional, Dict, Any


class APIClient:
    """Client for interacting with Book Store API"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url.rstrip('/')
        self.token = None
        self.timeout = 10
    
    def set_token(self, token: str):
        """Set authentication token"""
        self.token = token
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with authentication"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        Make HTTP request to API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            **kwargs: Additional arguments for requests
            
        Returns:
            Response JSON or None if error
        """
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                timeout=self.timeout,
                **kwargs
            )
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Request error: {str(e)}")
            return None
    
    # Health & Status
    def get_health(self) -> Optional[Dict[str, Any]]:
        """Get API health status"""
        return self._request("GET", "/health")
    
    def get_api_info(self) -> Optional[Dict[str, Any]]:
        """Get API information"""
        return self._request("GET", "/api/v1")
    
    # Books
    def get_books(self, page: int = 1, limit: int = 100, search: str = "") -> Optional[Dict[str, Any]]:
        """Get list of books"""
        params = {"page": page, "limit": limit}
        if search:
            params["search"] = search
        return self._request("GET", "/api/v1/books", params=params)
    
    def get_book(self, book_id: int) -> Optional[Dict[str, Any]]:
        """Get specific book by ID"""
        return self._request("GET", f"/api/v1/books/{book_id}")
    
    def search_books(self, title: str = None, category: str = None) -> Optional[Dict[str, Any]]:
        """Search books by title and/or category"""
        params = {}
        if title:
            params["title"] = title
        if category:
            params["category"] = category
        return self._request("GET", "/api/v1/books/search", params=params)
    
    def get_categories(self) -> Optional[Dict[str, Any]]:
        """Get all book categories"""
        return self._request("GET", "/api/v1/categories")
    
    def get_stats(self) -> Optional[Dict[str, Any]]:
        """Get books statistics"""
        return self._request("GET", "/api/v1/stats")
    
    # Scraping
    def get_scraping_jobs(self) -> Optional[Dict[str, Any]]:
        """Get all scraping jobs"""
        return self._request("GET", "/api/v1/scraping/jobs")
    
    def get_scraping_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get specific scraping job status"""
        return self._request("GET", f"/api/v1/scraping/jobs/{job_id}")
    
    def trigger_scraping(
        self,
        url: str = "http://books.toscrape.com",
        pages: int = 2,
        format_type: str = "both",
        output: str = "books"
    ) -> Optional[Dict[str, Any]]:
        """
        Trigger a new scraping job
        
        Args:
            url: URL to scrape
            pages: Number of pages to scrape
            format_type: Output format (json, csv, both)
            output: Output filename
            
        Returns:
            Job information or None
        """
        data = {
            "url": url,
            "pages": pages,
            "format": format_type,
            "output": output
        }
        return self._request("POST", "/api/v1/scraping/trigger", json=data)
    
    # Authentication
    def login(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Login to API"""
        data = {"username": username, "password": password}
        return self._request("POST", "/api/v1/auth/login", json=data)
    
    def refresh_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Refresh access token"""
        # Temporarily use refresh token
        old_token = self.token
        self.token = refresh_token
        result = self._request("POST", "/api/v1/auth/refresh")
        self.token = old_token
        return result
    
    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """Get current user information"""
        return self._request("GET", "/api/v1/auth/me")

