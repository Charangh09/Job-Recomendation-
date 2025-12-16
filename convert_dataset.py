"""
Convert Gen_AI Dataset.xlsx to the project's data format
"""

import pandas as pd
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def examine_dataset():
    """Examine the structure of the Gen_AI Dataset"""
    try:
        df = pd.read_excel(r'c:\Users\sirik\Downloads\Gen_AI Dataset.xlsx')
        
        logger.info(f"Dataset shape: {df.shape}")
        logger.info(f"Columns: {df.columns.tolist()}")
        logger.info("\nFirst few rows:")
        print(df.head())
        logger.info("\nColumn data types:")
        print(df.dtypes)
        logger.info("\nNull values:")
        print(df.isnull().sum())
        
        return df
    except Exception as e:
        logger.error(f"Error reading dataset: {e}")
        return None

def extract_assessment_name(url):
    """Extract assessment name from URL"""
    try:
        # Extract the assessment name from URL path
        parts = url.split('/')
        name = parts[-2] if parts[-1] == '' else parts[-1]
        # Clean up the name
        name = name.replace('-', ' ').replace('_', ' ')
        # Capitalize words
        name = ' '.join(word.capitalize() for word in name.split())
        return name
    except:
        return "Unknown Assessment"

def infer_category_from_query(query):
    """Infer assessment category from the query text"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['cognitive', 'reasoning', 'numerical', 'verbal', 'logic', 'analytical']):
        return 'Cognitive Ability'
    elif any(word in query_lower for word in ['personality', 'behavioral', 'behaviour', 'traits']):
        return 'Personality & Behavioral'
    elif any(word in query_lower for word in ['leadership', 'manage', 'executive', 'strategic']):
        return 'Leadership Assessment'
    elif any(word in query_lower for word in ['technical', 'coding', 'programming', 'software', 'java', 'python', 'developer']):
        return 'Job-Specific Skills'
    elif any(word in query_lower for word in ['sales', 'customer', 'service']):
        return 'Job-Specific Skills'
    elif any(word in query_lower for word in ['judgment', 'decision', 'situational']):
        return 'Judgment & Decision Making'
    else:
        return 'General Assessment'

def extract_skills_from_query(query):
    """Extract skills mentioned in the query"""
    skills = []
    query_lower = query.lower()
    
    skill_keywords = [
        'java', 'python', 'coding', 'programming', 'software development',
        'communication', 'leadership', 'teamwork', 'analytical', 'problem solving',
        'customer service', 'sales', 'management', 'strategic thinking',
        'numerical', 'verbal', 'reasoning', 'cognitive ability'
    ]
    
    for skill in skill_keywords:
        if skill in query_lower:
            skills.append(skill.title())
    
    return ', '.join(skills) if skills else 'Various professional skills'

def extract_roles_from_query(query):
    """Extract job roles mentioned in the query"""
    roles = []
    query_lower = query.lower()
    
    role_keywords = [
        'developer', 'engineer', 'manager', 'analyst', 'consultant',
        'representative', 'executive', 'coordinator', 'specialist',
        'administrator', 'supervisor', 'director', 'leader', 'designer',
        'programmer', 'architect', 'technician'
    ]
    
    for role in role_keywords:
        if role in query_lower:
            roles.append(role.title())
    
    return ', '.join(set(roles)) if roles else 'Various professional roles'

def convert_to_processed_format(df):
    """
    Convert the Query-Assessment_url dataset to the processed format expected by the system
    """
    processed_data = []
    
    for idx, row in df.iterrows():
        query = str(row['Query'])
        url = str(row['Assessment_url'])
        
        # Extract assessment name from URL
        assessment_name = extract_assessment_name(url)
        
        # Infer category from query
        category = infer_category_from_query(query)
        
        # Extract skills from query
        skills = extract_skills_from_query(query)
        
        # Extract roles from query
        roles = extract_roles_from_query(query)
        
        # Create record
        record = {
            'name': assessment_name,
            'category': category,
            'description': query,
            'skills_measured': skills,
            'job_suitability': roles,
            'experience_level': 'Entry, Mid, Senior',  # Default
            'duration': 'Variable',  # Default
            'delivery_method': 'Online',  # Default
            'assessment_url': url
        }
        
        # Create full_text field for embedding
        full_text_parts = [
            f"Assessment: {record['name']}",
            f"Category: {record['category']}",
            f"Query: {query}",
            f"Skills: {record['skills_measured']}",
            f"Suitable for: {record['job_suitability']}"
        ]
        
        record['full_text'] = " | ".join(full_text_parts)
        processed_data.append(record)
    
    return pd.DataFrame(processed_data)

def save_data(df):
    """Save the converted data to both CSV and JSON formats"""
    
    # Save to processed CSV
    csv_path = Path('data/processed/assessments.csv')
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)
    logger.info(f"Saved processed CSV to: {csv_path}")
    
    # Save to raw JSON
    json_path = Path('data/raw/shl_catalog.json')
    json_path.parent.mkdir(parents=True, exist_ok=True)
    
    json_data = {
        "assessments": df.to_dict('records'),
        "metadata": {
            "total_count": len(df),
            "source": "Gen_AI Dataset.xlsx"
        }
    }
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved raw JSON to: {json_path}")
    logger.info(f"Total assessments processed: {len(df)}")

def main():
    """Main conversion process"""
    logger.info("Starting dataset conversion...")
    
    # Examine the dataset
    df = examine_dataset()
    
    if df is not None:
        logger.info("\n" + "="*50)
        logger.info("Converting to processed format...")
        
        processed_df = convert_to_processed_format(df)
        
        if not processed_df.empty:
            logger.info(f"\nProcessed {len(processed_df)} records")
            logger.info("\nSample processed record:")
            if len(processed_df) > 0:
                print(processed_df.iloc[0].to_dict())
            
            # Save the data
            save_data(processed_df)
            
            logger.info("\n" + "="*50)
            logger.info("Conversion complete!")
            logger.info("Next steps:")
            logger.info("1. Verify the data in data/processed/assessments.csv")
            logger.info("2. Run: python src/embeddings/build_vector_db.py")
            logger.info("3. Test retrieval: python test_retrieval.py")
        else:
            logger.warning("No data was processed. Check column mappings.")
    else:
        logger.error("Failed to read dataset")

if __name__ == "__main__":
    main()
