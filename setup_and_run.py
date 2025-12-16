"""
Setup and Run Script for SHL Assessment Recommendation System

This script provides an easy way to set up and run the complete system.
"""

import subprocess
import sys
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


def run_command(command: str, description: str) -> bool:
    """
    Run a command and log the result.
    
    Args:
        command: Command to run
        description: Description of what the command does
        
    Returns:
        True if successful, False otherwise
    """
    logger.info(f"Starting: {description}")
    try:
        subprocess.run(command, shell=True, check=True)
        logger.info(f"✅ Completed: {description}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed: {description} - {e}")
        return False


def setup_environment():
    """Set up the Python environment and install dependencies."""
    logger.info("=" * 80)
    logger.info("SETTING UP ENVIRONMENT")
    logger.info("=" * 80)
    
    # Create virtual environment
    if not Path("venv").exists():
        logger.info("Creating virtual environment...")
        if not run_command(
            f"{sys.executable} -m venv venv",
            "Create virtual environment"
        ):
            return False
    
    # Install dependencies
    activate_cmd = "venv\\Scripts\\activate" if sys.platform == "win32" else "source venv/bin/activate"
    install_cmd = f"{activate_cmd} && pip install -r requirements.txt"
    
    if not run_command(install_cmd, "Install dependencies"):
        return False
    
    logger.info("✅ Environment setup complete!\n")
    return True


def run_data_pipeline():
    """Run the complete data pipeline."""
    logger.info("=" * 80)
    logger.info("RUNNING DATA PIPELINE")
    logger.info("=" * 80)
    
    steps = [
        ("python src/scraper/scrape_shl.py", "Scrape SHL catalog"),
        ("python src/scraper/parser.py", "Parse and clean data"),
        ("python src/embeddings/build_vector_db.py", "Build vector database")
    ]
    
    for command, description in steps:
        if not run_command(command, description):
            return False
    
    logger.info("✅ Data pipeline complete!\n")
    return True


def run_evaluation():
    """Run system evaluation."""
    logger.info("=" * 80)
    logger.info("RUNNING EVALUATION")
    logger.info("=" * 80)
    
    return run_command("python src/evaluation/evaluate.py", "Evaluate system")


def run_app():
    """Launch the Streamlit application."""
    logger.info("=" * 80)
    logger.info("LAUNCHING WEB APPLICATION")
    logger.info("=" * 80)
    logger.info("The application will open in your browser at http://localhost:8501")
    logger.info("Press Ctrl+C to stop the server\n")
    
    subprocess.run("streamlit run app.py", shell=True)


def main():
    """Main setup and run function."""
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║   SHL Assessment Recommendation System - Setup & Run Script   ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    print("\nWhat would you like to do?")
    print("1. Complete setup (environment + data pipeline)")
    print("2. Run data pipeline only")
    print("3. Run evaluation")
    print("4. Launch web application")
    print("5. Full setup and launch (recommended for first time)")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-5): ").strip()
    
    if choice == "1":
        if setup_environment() and run_data_pipeline():
            logger.info("\n🎉 Setup complete! Run option 4 to launch the app.")
    
    elif choice == "2":
        run_data_pipeline()
    
    elif choice == "3":
        run_evaluation()
    
    elif choice == "4":
        run_app()
    
    elif choice == "5":
        if setup_environment() and run_data_pipeline():
            logger.info("\n✅ Setup complete! Launching application...")
            input("\nPress Enter to launch the web application...")
            run_app()
    
    elif choice == "0":
        logger.info("Exiting...")
    
    else:
        logger.error("Invalid choice. Please run the script again.")


if __name__ == "__main__":
    main()
