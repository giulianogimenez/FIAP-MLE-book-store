"""
Data Processor - Process and save scraped data
"""
import json
import csv
import logging
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd

logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Process and save scraped data in various formats
    """
    
    def __init__(self, output_dir: str = "data/output"):
        """
        Initialize the data processor
        
        Args:
            output_dir: Directory to save output files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def save_to_json(self, data: List[Dict[str, Any]], filename: str) -> str:
        """
        Save data to JSON file
        
        Args:
            data: List of dictionaries to save
            filename: Output filename (without extension)
            
        Returns:
            Path to saved file
        """
        filepath = self.output_dir / f"{filename}.json"
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Data saved to {filepath}")
            return str(filepath)
        
        except Exception as e:
            logger.error(f"Error saving JSON: {e}")
            raise
    
    def save_to_csv(self, data: List[Dict[str, Any]], filename: str) -> str:
        """
        Save data to CSV file
        
        Args:
            data: List of dictionaries to save
            filename: Output filename (without extension)
            
        Returns:
            Path to saved file
        """
        filepath = self.output_dir / f"{filename}.csv"
        
        try:
            if not data:
                logger.warning("No data to save")
                return str(filepath)
            
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False, encoding='utf-8')
            
            logger.info(f"Data saved to {filepath}")
            return str(filepath)
        
        except Exception as e:
            logger.error(f"Error saving CSV: {e}")
            raise
    
    def clean_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Clean and validate scraped data
        
        Args:
            data: Raw scraped data
            
        Returns:
            Cleaned data
        """
        cleaned_data = []
        
        for item in data:
            # Remove empty values
            cleaned_item = {k: v for k, v in item.items() if v is not None and v != ''}
            
            # Add only if has essential fields
            if cleaned_item:
                cleaned_data.append(cleaned_item)
        
        logger.info(f"Cleaned {len(data)} items -> {len(cleaned_data)} valid items")
        return cleaned_data
    
    def generate_report(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a summary report of the scraped data
        
        Args:
            data: Scraped data
            
        Returns:
            Report dictionary
        """
        if not data:
            return {'error': 'No data to analyze'}
        
        df = pd.DataFrame(data)
        
        report = {
            'total_items': len(df),
            'columns': list(df.columns),
            'missing_values': df.isnull().sum().to_dict()
        }
        
        # Add numeric statistics if available
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            report['numeric_stats'] = df[numeric_cols].describe().to_dict()
        
        return report

