"""
Main script to run the scraper
"""
import logging
import argparse
from scraper.book_scraper import BookScraper
from scraper.data_processor import DataProcessor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Main function to run the scraping process
    """
    parser = argparse.ArgumentParser(description='Book Store Scraper')
    parser.add_argument(
        '--url',
        type=str,
        default='http://books.toscrape.com',
        help='Base URL to scrape'
    )
    parser.add_argument(
        '--pages',
        type=int,
        default=2,
        help='Number of pages to scrape'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='books',
        help='Output filename (without extension)'
    )
    parser.add_argument(
        '--format',
        type=str,
        choices=['json', 'csv', 'both'],
        default='both',
        help='Output format'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize scraper
        logger.info("Starting book scraper...")
        scraper = BookScraper(base_url=args.url, delay=1.0)
        
        # Scrape data
        books = scraper.scrape(max_pages=args.pages)
        scraper.close()
        
        if not books:
            logger.warning("No books were scraped!")
            return
        
        # Process data
        logger.info("Processing scraped data...")
        processor = DataProcessor(output_dir='data/output')
        
        # Clean data
        cleaned_books = processor.clean_data(books)
        
        # Save data
        if args.format in ['json', 'both']:
            processor.save_to_json(cleaned_books, args.output)
        
        if args.format in ['csv', 'both']:
            processor.save_to_csv(cleaned_books, args.output)
        
        # Generate report
        report = processor.generate_report(cleaned_books)
        logger.info(f"Scraping Report: {report}")
        
        logger.info("✅ Scraping completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error during scraping: {e}")
        raise


if __name__ == '__main__':
    main()

