"""
Tests for the scraper module
"""
import pytest
from scraper.data_processor import DataProcessor


def test_data_processor_initialization():
    """Test DataProcessor initialization"""
    processor = DataProcessor(output_dir='data/test_output')
    assert processor.output_dir.exists()


def test_clean_data():
    """Test data cleaning"""
    processor = DataProcessor(output_dir='data/test_output')
    
    raw_data = [
        {'title': 'Book 1', 'price': 10.99, 'author': ''},
        {'title': '', 'price': None, 'author': 'Author 2'},
        {'title': 'Book 3', 'price': 15.99, 'author': 'Author 3'}
    ]
    
    cleaned = processor.clean_data(raw_data)
    assert len(cleaned) == 3


def test_generate_report():
    """Test report generation"""
    processor = DataProcessor(output_dir='data/test_output')
    
    data = [
        {'title': 'Book 1', 'price': 10.99},
        {'title': 'Book 2', 'price': 15.99}
    ]
    
    report = processor.generate_report(data)
    assert report['total_items'] == 2
    assert 'columns' in report

