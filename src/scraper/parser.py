"""
Data Parser for SHL Assessment Data

This module parses and cleans scraped assessment data,
normalizing text and preparing it for embedding generation.
"""

import pandas as pd
import json
import re
from typing import List, Dict
from pathlib import Path
import logging
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AssessmentParser:
    """
    Parser for cleaning and structuring SHL assessment data.
    """
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize parser with configuration."""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        self.data_config = config['data_storage']
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text data.
        
        Args:
            text: Raw text string
            
        Returns:
            Cleaned text
        """
        if not isinstance(text, str):
            return str(text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.,!?()-]', '', text)
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def parse_assessment(self, assessment: Dict) -> Dict:
        """
        Parse and clean a single assessment entry.
        
        Args:
            assessment: Raw assessment dictionary
            
        Returns:
            Cleaned assessment dictionary
        """
        parsed = {
            'name': self.clean_text(assessment.get('name', '')),
            'category': self.clean_text(assessment.get('category', '')),
            'description': self.clean_text(assessment.get('description', '')),
            'skills_measured': ', '.join(assessment.get('skills_measured', [])),
            'job_suitability': ', '.join(assessment.get('job_suitability', [])),
            'experience_level': ', '.join(assessment.get('experience_level', [])),
            'duration': self.clean_text(assessment.get('duration', '')),
            'delivery_method': self.clean_text(assessment.get('delivery_method', ''))
        }
        
        # Create a comprehensive text representation for embedding
        parsed['full_text'] = self._create_full_text(parsed)
        
        return parsed
    
    def _create_full_text(self, assessment: Dict) -> str:
        """
        Create comprehensive text representation for embedding.
        
        This combines all assessment information into a single
        text field optimized for semantic search.
        
        Args:
            assessment: Parsed assessment dictionary
            
        Returns:
            Combined text representation
        """
        parts = [
            f"Assessment: {assessment['name']}",
            f"Category: {assessment['category']}",
            f"Description: {assessment['description']}",
            f"Skills Measured: {assessment['skills_measured']}",
            f"Suitable for: {assessment['job_suitability']}",
            f"Experience Levels: {assessment['experience_level']}"
        ]
        
        return " | ".join(parts)
    
    def parse_all(self, assessments: List[Dict]) -> pd.DataFrame:
        """
        Parse all assessments and return as DataFrame.
        
        Args:
            assessments: List of raw assessment dictionaries
            
        Returns:
            DataFrame with cleaned assessment data
        """
        logger.info(f"Parsing {len(assessments)} assessments...")
        
        parsed_assessments = [
            self.parse_assessment(assessment) 
            for assessment in assessments
        ]
        
        df = pd.DataFrame(parsed_assessments)
        logger.info(f"Parsed {len(df)} assessments successfully")
        
        return df
    
    def load_raw_data(self) -> List[Dict]:
        """
        Load raw scraped data from JSON file.
        
        Returns:
            List of raw assessment dictionaries
        """
        input_path = Path(self.data_config['raw_data_path'])
        
        if not input_path.exists():
            raise FileNotFoundError(
                f"Raw data file not found: {input_path}. "
                "Please run the scraper first."
            )
        
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"Loaded {len(data)} assessments from {input_path}")
        return data
    
    def save_processed_data(self, df: pd.DataFrame) -> None:
        """
        Save processed data to CSV file.
        
        Args:
            df: DataFrame with processed assessment data
        """
        output_path = Path(self.data_config['processed_data_path'])
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(output_path, index=False, encoding='utf-8')
        logger.info(f"Saved processed data to {output_path}")
    
    def run(self) -> pd.DataFrame:
        """
        Execute the complete parsing pipeline.
        
        Returns:
            DataFrame with processed assessments
        """
        logger.info("Starting data parsing pipeline...")
        raw_data = self.load_raw_data()
        df = self.parse_all(raw_data)
        self.save_processed_data(df)
        logger.info("Parsing completed successfully!")
        return df


if __name__ == "__main__":
    parser = AssessmentParser()
    df = parser.run()
    print("\nProcessed Data Sample:")
    print(df.head())
    print(f"\nDataFrame shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
