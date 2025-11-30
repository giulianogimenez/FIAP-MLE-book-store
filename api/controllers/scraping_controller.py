"""
Scraping Controller - Handle web scraping operations
"""
import logging
from threading import Thread
from scraper.book_scraper import BookScraper
from scraper.data_processor import DataProcessor

logger = logging.getLogger(__name__)


class ScrapingController:
    """
    Controller for scraping operations
    """
    
    def __init__(self):
        self.active_jobs = {}
        self.job_counter = 0
    
    def trigger_scraping(self, params):
        """
        Trigger a scraping job
        
        Args:
            params: Dictionary with scraping parameters
                - url: Base URL to scrape (optional)
                - pages: Number of pages to scrape (default: 2)
                - format: Output format - json, csv, both (default: both)
                - output: Output filename (default: books)
        
        Returns:
            Dictionary with job information
        """
        # Extract parameters
        url = params.get('url', 'http://books.toscrape.com')
        pages = params.get('pages', 2)
        output_format = params.get('format', 'both')
        output_name = params.get('output', 'books')
        
        # Validate parameters
        if not isinstance(pages, int) or pages < 1 or pages > 50:
            return {
                'error': 'Invalid pages parameter',
                'message': 'Pages must be an integer between 1 and 50'
            }, 400
        
        if output_format not in ['json', 'csv', 'both']:
            return {
                'error': 'Invalid format parameter',
                'message': 'Format must be one of: json, csv, both'
            }, 400
        
        # Create job ID
        self.job_counter += 1
        job_id = f"job_{self.job_counter}"
        
        # Store job info
        self.active_jobs[job_id] = {
            'status': 'pending',
            'url': url,
            'pages': pages,
            'format': output_format,
            'output': output_name,
            'results': None,
            'error': None
        }
        
        # Start scraping in background
        thread = Thread(
            target=self._run_scraping,
            args=(job_id, url, pages, output_format, output_name)
        )
        thread.daemon = True
        thread.start()
        
        return {
            'message': 'Scraping job started',
            'job_id': job_id,
            'parameters': {
                'url': url,
                'pages': pages,
                'format': output_format,
                'output': output_name
            }
        }, 202
    
    def _run_scraping(self, job_id, url, pages, output_format, output_name):
        """
        Run scraping job in background
        """
        try:
            logger.info(f"Starting scraping job {job_id}")
            self.active_jobs[job_id]['status'] = 'running'
            
            # Create scraper
            scraper = BookScraper(base_url=url, delay=1.0)
            
            # Scrape data with detailed information (UPC, category, ISBN, etc.)
            logger.info(f"Scraping {pages} pages with detailed information enabled")
            books = scraper.scrape(max_pages=pages, fetch_details=True)
            scraper.close()
            
            logger.info(f"Scraped {len(books)} books with complete details")
            
            if not books:
                self.active_jobs[job_id]['status'] = 'completed'
                self.active_jobs[job_id]['results'] = {
                    'books_count': 0,
                    'message': 'No books found'
                }
                return
            
            # Process data
            processor = DataProcessor(output_dir='data/output')
            cleaned_books = processor.clean_data(books)
            
            # Save data
            saved_files = []
            if output_format in ['json', 'both']:
                json_path = processor.save_to_json(cleaned_books, output_name)
                saved_files.append(json_path)
            
            if output_format in ['csv', 'both']:
                csv_path = processor.save_to_csv(cleaned_books, output_name)
                saved_files.append(csv_path)
            
            # Generate report
            report = processor.generate_report(cleaned_books)
            
            # Update job status
            self.active_jobs[job_id]['status'] = 'completed'
            self.active_jobs[job_id]['results'] = {
                'books_count': len(cleaned_books),
                'files': saved_files,
                'report': report
            }
            
            logger.info(f"Scraping job {job_id} completed successfully")
            logger.info(f"Saved {len(cleaned_books)} books to {saved_files}")
            
            # INSTANT RELOAD: Force repository to reload data immediately after scraping
            # This ensures data is available instantly without waiting for next HTTP request
            try:
                from api.routes import book_repository
                book_repository.reload()
                logger.info(f"✅ INSTANT RELOAD: BookRepository reloaded - {len(cleaned_books)} books now available in API")
            except Exception as e:
                logger.warning(f"Could not force immediate reload (will auto-reload on next request): {e}")
            
        except Exception as e:
            logger.error(f"Scraping job {job_id} failed: {e}")
            self.active_jobs[job_id]['status'] = 'failed'
            self.active_jobs[job_id]['error'] = str(e)
    
    def get_job_status(self, job_id):
        """
        Get status of a scraping job
        
        Args:
            job_id: Job identifier
        
        Returns:
            Dictionary with job status
        """
        if job_id not in self.active_jobs:
            return {
                'error': 'Job not found',
                'message': f'Job "{job_id}" does not exist'
            }, 404
        
        job = self.active_jobs[job_id]
        
        response = {
            'job_id': job_id,
            'status': job['status'],
            'parameters': {
                'url': job['url'],
                'pages': job['pages'],
                'format': job['format'],
                'output': job['output']
            }
        }
        
        if job['status'] == 'completed' and job['results']:
            response['results'] = job['results']
        
        if job['status'] == 'failed' and job['error']:
            response['error'] = job['error']
        
        return response, 200
    
    def list_jobs(self):
        """
        List all scraping jobs
        
        Returns:
            Dictionary with all jobs
        """
        jobs = []
        for job_id, job in self.active_jobs.items():
            jobs.append({
                'job_id': job_id,
                'status': job['status'],
                'url': job['url'],
                'pages': job['pages']
            })
        
        return {
            'jobs': jobs,
            'total': len(jobs)
        }, 200

