#!/usr/bin/env python3
"""
Test suite for MongoDB Quiz Application
"""

import unittest
import json
import sys
from pathlib import Path
from io import StringIO
from unittest.mock import patch, mock_open
from quiz import QuizApp


class TestQuizApp(unittest.TestCase):
    """Test cases for QuizApp class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_questions = {
            "atlas": {
                "easy": [
                    {
                        "id": "test_1",
                        "question": "What is MongoDB Atlas?",
                        "options": ["A", "B", "C", "D"],
                        "correct": 0,
                        "explanation": "Test explanation"
                    },
                    {
                        "id": "test_2",
                        "question": "Test question 2?",
                        "options": ["A", "B", "C", "D"],
                        "correct": 1,
                        "explanation": "Test explanation 2"
                    }
                ],
                "medium": [
                    {
                        "id": "test_3",
                        "question": "Medium question?",
                        "options": ["A", "B", "C", "D"],
                        "correct": 2,
                        "explanation": "Medium explanation"
                    }
                ],
                "hard": [
                    {
                        "id": "test_4",
                        "question": "Hard question?",
                        "options": ["A", "B", "C", "D"],
                        "correct": 3,
                        "explanation": "Hard explanation"
                    }
                ]
            },
            "ae": {
                "easy": [
                    {
                        "id": "test_5",
                        "question": "AE easy question?",
                        "options": ["A", "B", "C", "D"],
                        "correct": 0,
                        "explanation": "AE explanation"
                    }
                ],
                "medium": [
                    {
                        "id": "test_6",
                        "question": "AE medium question?",
                        "options": ["A", "B", "C", "D"],
                        "correct": 1,
                        "explanation": "AE medium explanation"
                    }
                ],
                "hard": [
                    {
                        "id": "test_7",
                        "question": "AE hard question?",
                        "options": ["A", "B", "C", "D"],
                        "correct": 2,
                        "explanation": "AE hard explanation"
                    }
                ]
            }
        }
        
        self.app = QuizApp('test_questions.json')
        self.app.questions_db = self.test_questions
    
    def test_initialization(self):
        """Test QuizApp initialization."""
        app = QuizApp()
        self.assertEqual(app.score, 0)
        self.assertEqual(app.total_questions, 0)
        self.assertEqual(len(app.current_quiz), 0)
        self.assertEqual(len(app.answers_history), 0)
    
    def test_load_questions_success(self):
        """Test successful question loading."""
        mock_data = json.dumps(self.test_questions)
        with patch('builtins.open', mock_open(read_data=mock_data)):
            result = self.app.load_questions()
            self.assertTrue(result)
            self.assertEqual(self.app.questions_db, self.test_questions)
    
    def test_load_questions_file_not_found(self):
        """Test question loading with missing file."""
        with patch('builtins.open', side_effect=FileNotFoundError):
            result = self.app.load_questions()
            self.assertFalse(result)
    
    def test_load_questions_invalid_json(self):
        """Test question loading with invalid JSON."""
        with patch('builtins.open', mock_open(read_data='invalid json {')):
            result = self.app.load_questions()
            self.assertFalse(result)
    
    def test_build_quiz_single_subject_single_difficulty(self):
        """Test building quiz with single subject and difficulty."""
        result = self.app.build_quiz(['atlas'], ['easy'], 2)
        self.assertTrue(result)
        self.assertEqual(len(self.app.current_quiz), 2)
        self.assertEqual(self.app.total_questions, 2)
    
    def test_build_quiz_multiple_subjects(self):
        """Test building quiz with multiple subjects."""
        result = self.app.build_quiz(['atlas', 'ae'], ['easy'], 3)
        self.assertTrue(result)
        self.assertEqual(len(self.app.current_quiz), 3)
    
    def test_build_quiz_multiple_difficulties(self):
        """Test building quiz with multiple difficulties."""
        result = self.app.build_quiz(['atlas'], ['easy', 'medium', 'hard'], 4)
        self.assertTrue(result)
        self.assertEqual(len(self.app.current_quiz), 4)
    
    def test_build_quiz_all_subjects_all_difficulties(self):
        """Test building quiz with all subjects and difficulties."""
        result = self.app.build_quiz(['atlas', 'ae'], ['easy', 'medium', 'hard'], 7)
        self.assertTrue(result)
        self.assertEqual(len(self.app.current_quiz), 7)
    
    def test_build_quiz_more_questions_than_available(self):
        """Test requesting more questions than available."""
        result = self.app.build_quiz(['atlas'], ['easy'], 10)
        self.assertTrue(result)
        # Should use all available easy atlas questions (2)
        self.assertEqual(len(self.app.current_quiz), 2)
    
    def test_build_quiz_no_matching_questions(self):
        """Test building quiz with no matching criteria."""
        # Create app with empty questions
        app = QuizApp()
        app.questions_db = {"atlas": {}}
        result = app.build_quiz(['atlas'], ['easy'], 5)
        self.assertFalse(result)
    
    def test_ask_question_correct_answer(self):
        """Test asking question with correct answer."""
        question = self.test_questions['atlas']['easy'][0]
        self.app.total_questions = 1
        
        with patch('builtins.input', side_effect=['1', '']):  # Answer 1, then Enter
            result = self.app.ask_question(question, 1)
            self.assertTrue(result)
            self.assertEqual(self.app.score, 1)
            self.assertEqual(len(self.app.answers_history), 1)
            self.assertTrue(self.app.answers_history[0]['is_correct'])
    
    def test_ask_question_incorrect_answer(self):
        """Test asking question with incorrect answer."""
        question = self.test_questions['atlas']['easy'][0]
        self.app.total_questions = 1
        
        with patch('builtins.input', side_effect=['2', '']):  # Answer 2, then Enter
            result = self.app.ask_question(question, 1)
            self.assertTrue(result)
            self.assertEqual(self.app.score, 0)
            self.assertFalse(self.app.answers_history[0]['is_correct'])
    
    def test_ask_question_quit(self):
        """Test quitting during a question."""
        question = self.test_questions['atlas']['easy'][0]
        self.app.total_questions = 1
        
        with patch('builtins.input', return_value='quit'):
            result = self.app.ask_question(question, 1)
            self.assertFalse(result)
    
    def test_ask_question_invalid_then_valid_input(self):
        """Test invalid input followed by valid answer."""
        question = self.test_questions['atlas']['easy'][0]
        self.app.total_questions = 1
        
        with patch('builtins.input', side_effect=['invalid', '5', '1', '']):
            result = self.app.ask_question(question, 1)
            self.assertTrue(result)
            self.assertEqual(self.app.score, 1)


class TestQuestionDatabase(unittest.TestCase):
    """Test the actual questions database."""
    
    def setUp(self):
        """Load the actual questions file."""
        self.questions_file = Path('questions.json')
        if self.questions_file.exists():
            with open(self.questions_file, 'r') as f:
                self.questions_db = json.load(f)
        else:
            self.questions_db = None
    
    def test_questions_file_exists(self):
        """Test that questions.json exists."""
        self.assertTrue(self.questions_file.exists(), "questions.json file not found")
    
    def test_questions_valid_json(self):
        """Test that questions.json is valid JSON."""
        self.assertIsNotNone(self.questions_db, "Failed to parse questions.json")
    
    def test_questions_structure(self):
        """Test that questions have correct structure."""
        if self.questions_db is None:
            self.skipTest("questions.json not available")
        
        # Check main subjects exist
        self.assertIn('atlas', self.questions_db)
        self.assertIn('ae', self.questions_db)
        
        # Check difficulty levels exist
        for subject in ['atlas', 'ae']:
            self.assertIn('easy', self.questions_db[subject])
            self.assertIn('medium', self.questions_db[subject])
            self.assertIn('hard', self.questions_db[subject])
    
    def test_question_count(self):
        """Test that we have at least 200 questions total."""
        if self.questions_db is None:
            self.skipTest("questions.json not available")
        
        total_questions = 0
        for subject in ['atlas', 'ae']:
            for difficulty in ['easy', 'medium', 'hard']:
                total_questions += len(self.questions_db[subject][difficulty])
        
        self.assertGreaterEqual(total_questions, 200, 
                                f"Expected at least 200 questions, found {total_questions}")
    
    def test_question_format(self):
        """Test that all questions have required fields."""
        if self.questions_db is None:
            self.skipTest("questions.json not available")
        
        required_fields = ['id', 'question', 'options', 'correct', 'explanation']
        
        for subject in ['atlas', 'ae']:
            for difficulty in ['easy', 'medium', 'hard']:
                questions = self.questions_db[subject][difficulty]
                for i, q in enumerate(questions):
                    # Check all required fields present
                    for field in required_fields:
                        self.assertIn(field, q, 
                                      f"Missing '{field}' in {subject}/{difficulty} question {i}")
                    
                    # Check options is a list of 4 items
                    self.assertIsInstance(q['options'], list)
                    self.assertEqual(len(q['options']), 4,
                                     f"Expected 4 options in {subject}/{difficulty} question {i}")
                    
                    # Check correct answer is valid index
                    self.assertIn(q['correct'], [0, 1, 2, 3],
                                  f"Invalid correct answer index in {subject}/{difficulty} question {i}")
                    
                    # Check question and options are non-empty strings
                    self.assertTrue(q['question'].strip(),
                                    f"Empty question in {subject}/{difficulty} question {i}")
                    for opt_idx, opt in enumerate(q['options']):
                        self.assertTrue(opt.strip(),
                                        f"Empty option {opt_idx} in {subject}/{difficulty} question {i}")
    
    def test_unique_question_ids(self):
        """Test that all question IDs are unique."""
        if self.questions_db is None:
            self.skipTest("questions.json not available")
        
        all_ids = set()
        duplicates = []
        
        for subject in ['atlas', 'ae']:
            for difficulty in ['easy', 'medium', 'hard']:
                for q in self.questions_db[subject][difficulty]:
                    if q['id'] in all_ids:
                        duplicates.append(q['id'])
                    all_ids.add(q['id'])
        
        self.assertEqual(len(duplicates), 0,
                         f"Found duplicate question IDs: {duplicates}")


def run_tests():
    """Run all tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestQuizApp))
    suite.addTests(loader.loadTestsFromTestCase(TestQuestionDatabase))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
