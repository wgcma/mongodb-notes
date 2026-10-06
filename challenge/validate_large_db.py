#!/usr/bin/env python3
"""Validation script for large question database"""
import json
import sys
from pathlib import Path
from collections import Counter

def validate_question_db(filepath):
    """Validate the question database."""
    print("=" * 70)
    print(" " * 15 + "QUESTION DATABASE VALIDATION")
    print("=" * 70)
    
    # Load questions
    print("\n1. Loading questions...")
    try:
        with open(filepath, 'r') as f:
            db = json.load(f)
        print(f"   ✓ Successfully loaded {filepath}")
    except Exception as e:
        print(f"   ✗ Failed to load: {e}")
        return False
    
    # Count questions
    print("\n2. Counting questions...")
    counts = {}
    total = 0
    
    for subject in ['atlas', 'ae']:
        counts[subject] = {}
        for difficulty in ['easy', 'medium', 'hard']:
            count = len(db.get(subject, {}).get(difficulty, []))
            counts[subject][difficulty] = count
            total += count
            print(f"   {subject:6s}/{difficulty:6s}: {count:5d} questions")
    
    print(f"\n   Total: {total:,} questions")
    
    # Check target counts
    print("\n3. Checking targets...")
    expected_total = 3000
    expected_easy = 1667
    expected_medium = 667
    expected_hard = 666
    
    actual_easy = counts['atlas']['easy'] + counts['ae']['easy']
    actual_medium = counts['atlas']['medium'] + counts['ae']['medium']
    actual_hard = counts['atlas']['hard'] + counts['ae']['hard']
    
    print(f"   Easy:   {actual_easy:5d} / {expected_easy} target")
    print(f"   Medium: {actual_medium:5d} / {expected_medium} target")
    print(f"   Hard:   {actual_hard:5d} / {expected_hard} target")
    print(f"   Total:  {total:5d} / {expected_total} target")
    
    # Validate format
    print("\n4. Validating question format...")
    issues = []
    all_ids = []
    
    for subject in ['atlas', 'ae']:
        for difficulty in ['easy', 'medium', 'hard']:
            questions = db.get(subject, {}).get(difficulty, [])
            for idx, q in enumerate(questions):
                # Check required fields
                required = ['id', 'question', 'options', 'correct', 'explanation']
                missing = [f for f in required if f not in q]
                if missing:
                    issues.append(f"Missing fields {missing} in {subject}/{difficulty} #{idx}")
                    continue
                
                # Check options count
                if len(q['options']) != 4:
                    issues.append(f"Wrong option count in {subject}/{difficulty} #{idx}")
                
                # Check correct index
                if q['correct'] not in [0, 1, 2, 3]:
                    issues.append(f"Invalid correct index in {subject}/{difficulty} #{idx}")
                
                # Collect ID
                all_ids.append(q['id'])
    
    if issues:
        print(f"   ✗ Found {len(issues)} formatting issues:")
        for issue in issues[:10]:  # Show first 10
            print(f"      - {issue}")
        if len(issues) > 10:
            print(f"      ... and {len(issues) - 10} more")
        return False
    else:
        print(f"   ✓ All {total:,} questions properly formatted")
    
    # Check unique IDs
    print("\n5. Checking unique IDs...")
    id_counts = Counter(all_ids)
    duplicates = {id: count for id, count in id_counts.items() if count > 1}
    
    if duplicates:
        print(f"   ✗ Found {len(duplicates)} duplicate IDs:")
        for id, count in list(duplicates.items())[:10]:
            print(f"      - {id}: appears {count} times")
        return False
    else:
        print(f"   ✓ All {len(all_ids):,} IDs are unique")
    
    # Summary
    print("\n" + "=" * 70)
    if total >= expected_total and not issues and not duplicates:
        print(" " * 20 + "✅ VALIDATION PASSED")
        print("=" * 70)
        print(f"\n✓ Database contains {total:,} high-quality questions")
        print("✓ All questions properly formatted")
        print("✓ All IDs unique")
        print("✓ Ready for use!")
        return True
    else:
        print(" " * 20 + "✗ VALIDATION FAILED")
        print("=" * 70)
        return False

if __name__ == '__main__':
    filepath = 'questions.json'
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    
    success = validate_question_db(filepath)
    sys.exit(0 if success else 1)
