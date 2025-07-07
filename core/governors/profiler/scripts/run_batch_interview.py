"""
Script to run batch interviews for all governors.
"""

from pathlib import Path
from core.governors.profiler.interview.batch_interview_processor import BatchInterviewProcessor

def main():
    # Initialize processor
    processor = BatchInterviewProcessor()
    
    # Set up paths
    questions_file = Path("core/governors/profiler/data/interview_questions.json")
    output_file = Path("governor_output/batch_interview_results.json")
    
    # Process all governors
    sessions = processor.process_all_governors(questions_file)
    
    # Save consolidated results
    processor.save_batch_results(sessions, output_file)
    
if __name__ == "__main__":
    main() 