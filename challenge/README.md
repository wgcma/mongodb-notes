# MongoDB Quiz Application

A comprehensive text-based quiz application for testing your MongoDB knowledge across Atlas and Application Engineering topics.

## Features

- **440 High-Quality Questions**: Curated question bank covering MongoDB Atlas and Application Engineering
- **Multiple Difficulty Levels**: Easy, Medium, and Hard questions
- **Subject Selection**: Choose between Atlas, Application Engineering, or both
- **Flexible Quiz Length**: Select 5-50 questions per quiz
- **Immediate Feedback**: Get instant feedback with explanations for each answer
- **Score Tracking**: Track your performance with percentage scores
- **Review Mode**: Review incorrect answers after completing the quiz
- **Mix & Match**: Combine different difficulty levels for customized practice

## Installation

No installation required! The quiz runs with Python 3 (which is already installed on macOS).

## Quick Start

1. Navigate to the challenge directory:
```bash
cd /Users/wing/devws/mongodb-notes/challenge
```

2. Run the quiz:
```bash
python3 quiz.py
```

3. Follow the prompts to:
   - Select difficulty level (Easy, Medium, Hard, or Mixed)
   - Choose subject area (Atlas, Application Engineering, or Both)
   - Specify number of questions (5-50)

4. Answer questions by entering 1-4 for your choice
5. Type 'quit' at any time to exit

## Question Database

The quiz includes **440 high-quality questions** covering:

### MongoDB Atlas Topics (213 questions)
- **Easy (95)**: Cloud basics, cluster management, auto-scaling, deployment options, shard keys
- **Medium (60)**: Advanced features, performance optimization, security, backup strategies, scaling strategies
- **Hard (58)**: Deep architecture, advanced configurations, internals, replication details, sharding internals

### Application Engineering Topics (227 questions)
- **Easy (104)**: CRUD operations, basic queries, MongoDB drivers, fundamental concepts, read/write concerns
- **Medium (62)**: Aggregation framework, indexes, data modeling, operators, transaction guarantees
- **Hard (61)**: Advanced pipeline operations, performance tuning, complex queries, optimization, consistency models

## Usage Examples

### Quick Practice (10 Easy Questions)
```
Difficulty: 1 (Easy)
Subject: 3 (Both Atlas & AE)
Questions: 10 (default)
```

### Atlas Certification Prep
```
Difficulty: 5 (Mix All Difficulties)
Subject: 1 (Atlas Only)
Questions: 30
```

### Application Engineering Deep Dive
```
Difficulty: 3 (Hard)
Subject: 2 (Application Engineering Only)
Questions: 20
```

### Comprehensive Review
```
Difficulty: 5 (Mix All Difficulties)
Subject: 3 (Both Atlas & AE)
Questions: 50
```

## Running Tests

The quiz includes a comprehensive test suite to ensure everything works correctly.

Run all tests:
```bash
python3 test_quiz.py
```

Expected output:
```
Ran 20 tests in 0.005s
OK
```

## Test Coverage

The test suite includes:
- **Unit Tests**: Core functionality tests (10 tests)
  - Quiz initialization
  - Question loading (success and error cases)
  - Quiz building with various criteria
  - Question answering logic
  - Input validation

- **Integration Tests**: Question database validation (10 tests)
  - File existence and valid JSON
  - Correct structure (subjects and difficulty levels)
  - Question count (≥200 questions)
  - Question format validation
  - Unique question IDs

## File Structure

```
challenge/
├── quiz.py              # Main quiz application
├── questions.json       # Question database (440 questions)
├── test_quiz.py        # Test suite
└── README.md           # This file
```

## Scoring Guide

- **90-100%**: Excellent! MongoDB Expert 🌟
- **80-89%**: Great job! Strong knowledge 👍
- **70-79%**: Good work! On the right track ✓
- **60-69%**: Not bad! Keep studying 📚
- **Below 60%**: Keep learning! Review and retry 💪

## Tips for Best Results

1. **Start Easy**: Begin with easy questions to build confidence
2. **Mix It Up**: Use mixed difficulty to identify knowledge gaps
3. **Review Mistakes**: Always review incorrect answers to learn
4. **Regular Practice**: Take quizzes regularly to retain knowledge
5. **Focus Areas**: Use subject selection to focus on specific topics

## Question Format

Each question includes:
- Clear, concise question text
- Four multiple-choice options
- One correct answer
- Detailed explanation

Example:
```
What is MongoDB Atlas?
  1. A local MongoDB installation tool
  2. A cloud-hosted MongoDB service
  3. A MongoDB GUI client
  4. A database migration tool

Correct Answer: 2
Explanation: MongoDB Atlas is a fully-managed cloud database service...
```

## Troubleshooting

### Quiz won't start
```bash
# Make sure you're in the correct directory
cd /Users/wing/devws/mongodb-notes/challenge

# Verify files exist
ls -l
```

### Questions not loading
```bash
# Check that questions.json exists and is valid JSON
python3 -c "import json; json.load(open('questions.json'))"
```

### Tests failing
```bash
# Run tests with verbose output
python3 test_quiz.py -v
```

## Keyboard Shortcuts

- **Enter**: Submit answer and continue
- **1-4**: Select answer option
- **quit**: Exit quiz at any time
- **y/n**: Yes/No prompts (review incorrect answers)

## Features in Detail

### Difficulty Levels
1. **Easy**: Fundamental concepts, definitions, basic operations
2. **Medium**: Intermediate topics, common patterns, best practices
3. **Hard**: Advanced architecture, optimization, edge cases
4. **Mix Easy & Medium**: Balanced review without hardest questions
5. **Mix All Difficulties**: Comprehensive assessment

### Subject Areas
1. **Atlas Only**: Cloud platform, deployment, management, monitoring
2. **Application Engineering Only**: Drivers, queries, aggregation, data modeling
3. **Both**: Complete MongoDB knowledge assessment

### Smart Features
- Questions are randomly selected and shuffled each time
- No duplicate questions in a single quiz
- Graceful handling of edge cases (e.g., requesting more questions than available)
- Input validation with helpful error messages
- Progress tracking throughout the quiz

## Development

### Adding Questions

To add new questions, edit `questions.json`:

```json
{
  "atlas": {
    "easy": [
      {
        "id": "unique_id",
        "question": "Your question?",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
        "correct": 0,
        "explanation": "Why this is correct"
      }
    ]
  }
}
```

Then run tests to validate:
```bash
python3 test_quiz.py
```

### Question Requirements
- Unique `id` field
- Clear `question` text
- Exactly 4 `options`
- Valid `correct` index (0-3)
- Helpful `explanation`

## Performance

- Loads 440 questions in < 0.1 seconds
- Minimal memory footprint
- Instant question randomization
- No external dependencies

## License

Educational use for MongoDB learning and certification preparation.

## Support

For issues or questions:
1. Check this README
2. Run the test suite
3. Verify file integrity

## Version

Version 2.1 - Enhanced with 29 new questions on auto-scaling, sharding, and transactions (440 total curated questions)

---

**Happy Learning! 🚀**

Master MongoDB one question at a time!
