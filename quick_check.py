"""Quick system check for Gen_AI Dataset integration"""
import pandas as pd
from pathlib import Path
import chromadb
from src.embeddings.embedding_generator import EmbeddingGenerator

print("="*70)
print("QUICK SYSTEM CHECK")
print("="*70)

# Check 1: Data files
print("\n1. DATA FILES:")
csv_path = Path("data/processed/assessments.csv")
json_path = Path("data/raw/shl_catalog.json")

if csv_path.exists():
    df = pd.read_csv(csv_path)
    print(f"   ✓ CSV exists: {len(df)} assessments")
    print(f"   ✓ Columns: {', '.join(df.columns[:5])}...")
else:
    print("   ✗ CSV not found")

if json_path.exists():
    print(f"   ✓ JSON exists")
else:
    print("   ✗ JSON not found")

# Check 2: Vector database
print("\n2. VECTOR DATABASE:")
db_path = Path("data/vector_db")
if db_path.exists():
    print(f"   ✓ Database directory exists")
    try:
        client = chromadb.PersistentClient(path=str(db_path))
        collection = client.get_collection("shl_assessments")
        count = collection.count()
        print(f"   ✓ Collection 'shl_assessments': {count} documents")
    except Exception as e:
        print(f"   ✗ Error accessing collection: {e}")
else:
    print("   ✗ Database directory not found")

# Check 3: Embeddings model
print("\n3. EMBEDDINGS MODEL:")
try:
    embedder = EmbeddingGenerator()
    test_text = "Software engineer with Python skills"
    embedding = embedder.generate_embeddings([test_text])
    print(f"   ✓ Model loaded successfully")
    print(f"   ✓ Test embedding generated: dimension {len(embedding[0])}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Check 4: Sample retrieval
print("\n4. SAMPLE RETRIEVAL:")
try:
    from src.retrieval.retriever import AssessmentRetriever
    retriever = AssessmentRetriever()
    results = retriever.search("Java developer", top_k=3)
    print(f"   ✓ Search working: {len(results)} results returned")
    if results:
        print(f"   ✓ Top result: {results[0].get('name', 'N/A')}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Check 5: Sample data inspection
print("\n5. SAMPLE ASSESSMENTS:")
if csv_path.exists():
    df = pd.read_csv(csv_path)
    for i, row in df.head(3).iterrows():
        print(f"   • {row['name']} ({row['category']})")

print("\n" + "="*70)
print("OVERALL STATUS:")
if csv_path.exists() and db_path.exists() and count > 0:
    print("✓ System is operational with Gen_AI Dataset")
    print(f"✓ {count} assessments ready for recommendations")
else:
    print("⚠ Some components need attention")
print("="*70)
