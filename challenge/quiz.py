#!/usr/bin/env python3
"""
MongoDB Quiz Application
A text-based quiz app for testing MongoDB knowledge across Atlas and Application Engineering topics.
"""

import json
import random
import sys
from typing import List, Dict, Optional
from pathlib import Path


class QuizApp:
    """Main quiz application class."""
    
    DIFFICULTY_OPTIONS = {
        '1': {'name': 'Easy', 'levels': ['easy']},
        '2': {'name': 'Medium', 'levels': ['medium']},
        '3': {'name': 'Hard', 'levels': ['hard']},
        '4': {'name': 'Mix Easy & Medium', 'levels': ['easy', 'medium']},
        '5': {'name': 'Mix All Difficulties', 'levels': ['easy', 'medium', 'hard']}
    }
    
    SUBJECT_OPTIONS = {
        '1': {'name': 'Atlas Only', 'subjects': ['atlas']},
        '2': {'name': 'Application Engineering Only', 'subjects': ['ae']},
        '3': {'name': 'Both Atlas & AE', 'subjects': ['atlas', 'ae']}
    }
    
    def __init__(self, questions_file: str = 'questions.json'):
        """Initialize the quiz app."""
        self.questions_file = Path(questions_file)
        self.questions_db = {}
        self.current_quiz = []
        self.score = 0
        self.total_questions = 0
        self.answers_history = []
        
    def load_questions(self) -> bool:
        """Load questions from JSON file."""
        try:
            with open(self.questions_file, 'r') as f:
                self.questions_db = json.load(f)
            return True
        except FileNotFoundError:
            print(f"Error: Questions file '{self.questions_file}' not found!")
            return False
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in questions file: {e}")
            return False
    
    def display_welcome(self):
        """Display welcome message and instructions."""
        print("\n" + "=" * 70)
        print(" " * 20 + "MONGODB QUIZ APP")
        print("=" * 70)
        print("\nWelcome to the MongoDB Quiz Application!")
        print("Test your knowledge of MongoDB Atlas and Application Engineering.\n")
        print("Instructions:")
        print("  • You'll be presented with multiple choice questions")
        print("  • Enter the number (1-4) corresponding to your answer")
        print("  • Type 'quit' at any time to exit the quiz")
        print("  • Your score will be displayed at the end\n")
        print("=" * 70 + "\n")
    
    def select_difficulty(self) -> Optional[List[str]]:
        """Prompt user to select difficulty level."""
        print("Select Difficulty Level:")
        print("-" * 40)
        for key, value in self.DIFFICULTY_OPTIONS.items():
            print(f"  {key}. {value['name']}")
        print()
        
        while True:
            choice = input("Enter your choice (1-5): ").strip()
            if choice in self.DIFFICULTY_OPTIONS:
                selected = self.DIFFICULTY_OPTIONS[choice]
                print(f"\nSelected: {selected['name']}\n")
                return selected['levels']
            elif choice.lower() == 'quit':
                return None
            else:
                print("Invalid choice. Please enter 1-5 or 'quit'.")
    
    def select_subject(self) -> Optional[List[str]]:
        """Prompt user to select subject area."""
        print("Select Subject Area:")
        print("-" * 40)
        for key, value in self.SUBJECT_OPTIONS.items():
            print(f"  {key}. {value['name']}")
        print()
        
        while True:
            choice = input("Enter your choice (1-3): ").strip()
            if choice in self.SUBJECT_OPTIONS:
                selected = self.SUBJECT_OPTIONS[choice]
                print(f"\nSelected: {selected['name']}\n")
                return selected['subjects']
            elif choice.lower() == 'quit':
                return None
            else:
                print("Invalid choice. Please enter 1-3 or 'quit'.")
    
    def select_num_questions(self) -> Optional[int]:
        """Prompt user to select number of questions."""
        print("How many questions would you like?")
        print("-" * 40)
        print("  Enter a number between 5 and 50")
        print("  (or press Enter for default: 10 questions)")
        print()
        
        while True:
            choice = input("Number of questions: ").strip()
            
            if choice.lower() == 'quit':
                return None
            
            if choice == '':
                print("\nSelected: 10 questions\n")
                return 10
            
            try:
                num = int(choice)
                if 5 <= num <= 50:
                    print(f"\nSelected: {num} questions\n")
                    return num
                else:
                    print("Please enter a number between 5 and 50.")
            except ValueError:
                print("Invalid input. Please enter a number or 'quit'.")
    
    def build_quiz(self, subjects: List[str], difficulties: List[str], num_questions: int):
        """Build quiz from selected criteria."""
        available_questions = []
        
        # Collect all questions matching criteria
        for subject in subjects:
            if subject in self.questions_db:
                for difficulty in difficulties:
                    if difficulty in self.questions_db[subject]:
                        questions = self.questions_db[subject][difficulty]
                        available_questions.extend(questions)
        
        if not available_questions:
            print("Error: No questions found matching your criteria!")
            return False
        
        # Randomly select questions
        if len(available_questions) <= num_questions:
            self.current_quiz = available_questions.copy()
            print(f"Note: Only {len(available_questions)} questions available. Using all.\n")
        else:
            self.current_quiz = random.sample(available_questions, num_questions)
        
        # Shuffle the quiz
        random.shuffle(self.current_quiz)
        self.total_questions = len(self.current_quiz)
        
        return True
    
    def ask_question(self, question: Dict, question_num: int) -> bool:
        """Ask a single question and get user's answer."""
        print("=" * 70)
        print(f"Question {question_num}/{self.total_questions}")
        print("=" * 70)
        print(f"\n{question['question']}\n")
        
        # Display options
        for i, option in enumerate(question['options'], 1):
            print(f"  {i}. {option}")
        print()
        
        # Get user answer
        while True:
            answer = input("Your answer (1-4): ").strip()
            
            if answer.lower() == 'quit':
                return False
            
            try:
                answer_idx = int(answer) - 1
                if 0 <= answer_idx < len(question['options']):
                    break
                else:
                    print("Please enter a number between 1 and 4.")
            except ValueError:
                print("Invalid input. Please enter 1-4 or 'quit'.")
        
        # Check answer
        is_correct = (answer_idx == question['correct'])
        
        if is_correct:
            self.score += 1
            print("\n✓ Correct! Well done!")
        else:
            correct_answer = question['options'][question['correct']]
            print(f"\n✗ Incorrect. The correct answer was: {correct_answer}")
        
        # Show explanation
        if 'explanation' in question:
            print(f"\nExplanation: {question['explanation']}")
        
        # Record answer
        self.answers_history.append({
            'question': question['question'],
            'user_answer': question['options'][answer_idx],
            'correct_answer': question['options'][question['correct']],
            'is_correct': is_correct,
            'explanation': question.get('explanation', '')
        })
        
        print()
        
        return True
    
    def run_quiz(self):
        """Run the complete quiz."""
        for i, question in enumerate(self.current_quiz, 1):
            if not self.ask_question(question, i):
                print("\n\nQuiz interrupted by user.")
                return False
        
        return True
    
    def display_results(self):
        """Display final quiz results."""
        print("\n" + "=" * 70)
        print(" " * 25 + "QUIZ RESULTS")
        print("=" * 70)
        
        percentage = (self.score / self.total_questions * 100) if self.total_questions > 0 else 0
        
        print(f"\nYou answered {self.score} out of {self.total_questions} questions correctly!")
        print(f"Score: {percentage:.1f}%\n")
        
        # Performance rating
        if percentage >= 90:
            rating = "Excellent! You're a MongoDB expert! 🌟"
        elif percentage >= 80:
            rating = "Great job! You have strong MongoDB knowledge! 👍"
        elif percentage >= 70:
            rating = "Good work! You're on the right track! ✓"
        elif percentage >= 60:
            rating = "Not bad! Keep studying to improve! 📚"
        else:
            rating = "Keep learning! Review the material and try again! 💪"
        
        print(rating)
        print("\n" + "=" * 70)
        
        # Ask if user wants to review incorrect answers
        if self.score < self.total_questions:
            print()
            review = input("Would you like to review incorrect answers? (y/n): ").strip().lower()
            if review == 'y':
                self.review_incorrect_answers()
    
    def review_incorrect_answers(self):
        """Display all incorrect answers for review."""
        print("\n" + "=" * 70)
        print(" " * 20 + "INCORRECT ANSWERS REVIEW")
        print("=" * 70 + "\n")
        
        incorrect_count = 0
        for i, answer in enumerate(self.answers_history, 1):
            if not answer['is_correct']:
                incorrect_count += 1
                print(f"Question {i}: {answer['question']}")
                print(f"  Your answer: {answer['user_answer']}")
                print(f"  Correct answer: {answer['correct_answer']}")
                if answer['explanation']:
                    print(f"  Explanation: {answer['explanation']}")
                print()
        
        if incorrect_count == 0:
            print("Perfect score! No incorrect answers to review.")
        
        print("=" * 70)
    
    def run(self):
        """Main application loop."""
        # Load questions
        if not self.load_questions():
            return 1
        
        # Display welcome
        self.display_welcome()
        
        # Select difficulty
        difficulties = self.select_difficulty()
        if difficulties is None:
            print("\nQuiz cancelled. Goodbye!")
            return 0
        
        # Select subject
        subjects = self.select_subject()
        if subjects is None:
            print("\nQuiz cancelled. Goodbye!")
            return 0
        
        # Select number of questions
        num_questions = self.select_num_questions()
        if num_questions is None:
            print("\nQuiz cancelled. Goodbye!")
            return 0
        
        # Build quiz
        if not self.build_quiz(subjects, difficulties, num_questions):
            return 1
        
        # Run quiz
        print("\n" + "=" * 70)
        print(" " * 22 + "STARTING QUIZ")
        print("=" * 70 + "\n")
        input("Press Enter when you're ready to begin...")
        print()
        
        completed = self.run_quiz()
        
        # Display results
        if completed or self.score > 0:
            self.display_results()
        
        print("\n\nThank you for using MongoDB Quiz App!")
        print("Keep learning and good luck with your MongoDB journey! 🚀\n")
        
        return 0


def main():
    """Entry point for the quiz application."""
    try:
        app = QuizApp()
        sys.exit(app.run())
    except KeyboardInterrupt:
        print("\n\nQuiz interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nAn unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
