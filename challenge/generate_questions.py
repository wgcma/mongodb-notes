#!/usr/bin/env python3
import json
import random

# Read existing questions
with open('/Users/wing/devws/mongodb-notes/challenge/questions.json', 'r') as f:
    existing_data = json.load(f)

# Current counts
current_counts = {
    'atlas': {
        'easy': len(existing_data['atlas']['easy']),
        'medium': len(existing_data['atlas']['medium']),
        'hard': len(existing_data['atlas']['hard'])
    },
    'ae': {
        'easy': len(existing_data['ae']['easy']),
        'medium': len(existing_data['ae']['medium']),
        'hard': len(existing_data['ae']['hard'])
    }
}

targets = {
    'atlas': {'easy': 794, 'medium': 294, 'hard': 293},
    'ae': {'easy': 793, 'medium': 293, 'hard': 293}
}

print("Current counts:")
for cat in ['atlas', 'ae']:
    for diff in ['easy', 'medium', 'hard']:
        current = current_counts[cat][diff]
        target = targets[cat][diff]
        needed = target - current
        print(f"{cat}/{diff}: {current} → need {needed} more (target: {target})")

# This is a placeholder - actual generation would go here
print("\nGeneration script ready. Run with proper question templates.")
