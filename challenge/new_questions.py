#!/usr/bin/env python3
"""
Generate new high-quality MongoDB questions based on 2026 research
"""

import json

# New questions based on research findings

NEW_ATLAS_EASY = [
    {
        "id": "atlas_easy_88",
        "question": "What are the two types of auto-scaling available in MongoDB Atlas?",
        "options": [
            "CPU and memory auto-scaling",
            "Cluster tier and storage auto-scaling",
            "Read and write auto-scaling",
            "Index and query auto-scaling"
        ],
        "correct": 1,
        "explanation": "Atlas offers cluster tier auto-scaling (scales instance type) and storage auto-scaling (increases disk size as data grows)."
    },
    {
        "id": "atlas_easy_89",
        "question": "At what CPU utilization threshold does Atlas scale up a cluster?",
        "options": [
            "50% over 30 minutes",
            "60% over 45 minutes",
            "75% over 1 hour",
            "90% over 2 hours"
        ],
        "correct": 2,
        "explanation": "Atlas scales up when CPU utilization exceeds approximately 75% over a 1-hour window."
    },
    {
        "id": "atlas_easy_90",
        "question": "At what storage utilization percentage does Atlas automatically increase disk size?",
        "options": [
            "70%",
            "80%",
            "90%",
            "95%"
        ],
        "correct": 2,
        "explanation": "Storage auto-scaling increases disk size when usage exceeds 90%."
    },
    {
        "id": "atlas_easy_91",
        "question": "Is Atlas storage auto-scaling bidirectional (can it scale down)?",
        "options": [
            "Yes, it scales both up and down",
            "No, storage does not scale down automatically",
            "Only for M10+ clusters",
            "Yes, but only during maintenance windows"
        ],
        "correct": 1,
        "explanation": "Atlas automatically increases disk when utilization exceeds 90%, but storage does not scale down automatically."
    },
    {
        "id": "atlas_easy_92",
        "question": "Is cluster tier scale-down enabled by default in Atlas?",
        "options": [
            "Yes, always enabled",
            "No, it is disabled by default",
            "Only for serverless",
            "Only for M0 clusters"
        ],
        "correct": 1,
        "explanation": "Scale-down is optional and disabled by default. Atlas scales down only after CPU consistently stays below approximately 50% for several hours."
    },
    {
        "id": "atlas_easy_93",
        "question": "What tool can you use starting in MongoDB 7.0 to evaluate shard keys?",
        "options": [
            "shardAnalyzer",
            "analyzeShardKey",
            "evalKey",
            "keyMetrics"
        ],
        "correct": 1,
        "explanation": "Starting in 7.0, you can use analyzeShardKey which calculates metrics for evaluating a shard key for an unsharded or sharded collection."
    },
    {
        "id": "atlas_easy_94",
        "question": "What is the main problem with using monotonically increasing keys as shard keys?",
        "options": [
            "They cause slow queries",
            "They create write hotspots on one shard",
            "They use too much memory",
            "They cannot be indexed"
        ],
        "correct": 1,
        "explanation": "Monotonically increasing keys cause write hotspots because all new inserts land in the last chunk on the highest-value shard, while other shards receive no new writes."
    },
    {
        "id": "atlas_easy_95",
        "question": "What characteristic should a good shard key have regarding cardinality?",
        "options": [
            "Low cardinality for simplicity",
            "Medium cardinality for balance",
            "High cardinality for better distribution",
            "Cardinality doesn't matter"
        ],
        "correct": 2,
        "explanation": "Choose a shard key with high cardinality. The cardinality determines the maximum number of chunks the balancer can create."
    }
]

NEW_ATLAS_MEDIUM = [
    {
        "id": "atlas_medium_56",
        "question": "How does Atlas detect when to scale up cluster tiers?",
        "options": [
            "Manual triggers only",
            "Detects sustained higher demand and short-term peak traffic",
            "Pre-scheduled intervals",
            "Only when disk is full"
        ],
        "correct": 1,
        "explanation": "Atlas reactive auto-scaling detects sustained higher demand and short-term peak traffic and adjusts cluster tier based on real-time resource usage."
    },
    {
        "id": "atlas_medium_57",
        "question": "What is the benefit of using a compound shard key?",
        "options": [
            "Faster queries only",
            "Combines geographic locality with distribution",
            "Reduces storage costs",
            "Eliminates need for indexes"
        ],
        "correct": 1,
        "explanation": "A compound shard key combining a low-cardinality field with a high-cardinality field gives both geographic locality and distribution."
    },
    {
        "id": "atlas_medium_58",
        "question": "What shard key strategy is best for write-heavy workloads needing uniform distribution?",
        "options": [
            "Compound shard key",
            "Hashed shard key",
            "Range-based shard key",
            "UUID shard key"
        ],
        "correct": 1,
        "explanation": "Hashed shard key is best for write-heavy workloads needing uniform distribution."
    },
    {
        "id": "atlas_medium_59",
        "question": "What limits horizontal scaling with low-cardinality shard keys?",
        "options": [
            "Memory constraints",
            "Maximum chunk count equals unique key values",
            "Network bandwidth",
            "CPU limitations"
        ],
        "correct": 1,
        "explanation": "Low-cardinality shard keys limit horizontal scaling because each unique key value resides in at most one chunk. For example, if you sharded by a field with only 5 distinct values, the cluster could have no more than 5 chunks."
    },
    {
        "id": "atlas_medium_60",
        "question": "What is the best shard key for query isolation?",
        "options": [
            "Any high-cardinality field",
            "One that appears in every high-frequency query filter with high cardinality",
            "The _id field",
            "A timestamp field"
        ],
        "correct": 1,
        "explanation": "The best shard key for query isolation is one that appears in every high-frequency query filter and has high enough cardinality to distribute data evenly."
    }
]

NEW_ATLAS_HARD = [
    {
        "id": "atlas_hard_56",
        "question": "What CPU threshold triggers Atlas cluster tier scale-down and for how long must it persist?",
        "options": [
            "Below 30% for 1 hour",
            "Below 40% for 2 hours",
            "Below 50% for several hours",
            "Below 60% for 30 minutes"
        ],
        "correct": 2,
        "explanation": "Atlas scales down only after CPU consistently stays below approximately 50% for several hours."
    },
    {
        "id": "atlas_hard_57",
        "question": "How many distinct values can a shard key with cardinality of 5 support in terms of chunks?",
        "options": [
            "Unlimited chunks",
            "No more than 5 chunks",
            "10 chunks (2x cardinality)",
            "25 chunks (5^2)"
        ],
        "correct": 1,
        "explanation": "Each unique key value resides in at most one chunk, so a field with only 5 distinct values can have no more than 5 chunks maximum."
    },
    {
        "id": "atlas_hard_58",
        "question": "What happens to writes when using a monotonically increasing shard key?",
        "options": [
            "Evenly distributed across all shards",
            "All writes go to the last chunk on highest-value shard",
            "Randomly distributed",
            "Round-robin across shards"
        ],
        "correct": 1,
        "explanation": "Because chunks are ordered, all new inserts land in the last chunk on the highest-value shard, while other shards receive no new writes, creating a write hotspot."
    }
]

NEW_AE_EASY = [
    {
        "id": "ae_easy_99",
        "question": "What read concern level is recommended for production transactions?",
        "options": [
            "local",
            "available",
            "snapshot",
            "linearizable"
        ],
        "correct": 2,
        "explanation": "Read concern 'snapshot' returns data from a snapshot of majority committed data if the transaction commits with write concern 'majority', providing consistency across reads."
    },
    {
        "id": "ae_easy_100",
        "question": "What write concern level should production transactions use?",
        "options": [
            "w: 1",
            "w: 0",
            "w: 'majority'",
            "j: false"
        ],
        "correct": 2,
        "explanation": "MongoDB transaction write concern should always be set to w: 'majority' for production use to guarantee that committed transactions survive replica set failovers."
    },
    {
        "id": "ae_easy_101",
        "question": "How many read concern levels does MongoDB support?",
        "options": [
            "Three",
            "Four",
            "Five",
            "Six"
        ],
        "correct": 2,
        "explanation": "MongoDB supports five read concern levels: local, available, majority, linearizable, and snapshot."
    },
    {
        "id": "ae_easy_102",
        "question": "What does read concern 'majority' guarantee?",
        "options": [
            "Fastest possible reads",
            "Data has been replicated to a majority of nodes and cannot be rolled back",
            "Reads from primary only",
            "Most recent data"
        ],
        "correct": 1,
        "explanation": "Majority read concern ensures data has been replicated to a majority of nodes in the replica set and cannot be rolled back."
    },
    {
        "id": "ae_easy_103",
        "question": "What does the 'j: true' write concern option require?",
        "options": [
            "Write to primary only",
            "Write to majority of nodes",
            "Write to be written to the journal before acknowledgment",
            "Write to all nodes"
        ],
        "correct": 2,
        "explanation": "j: true requires the write to be written to the journal before acknowledgment, providing durability guarantees."
    },
    {
        "id": "ae_easy_104",
        "question": "What does read concern 'snapshot' provide in transactions?",
        "options": [
            "Latest data only",
            "Consistent snapshot of data across all reads",
            "Fastest reads",
            "Random data points"
        ],
        "correct": 1,
        "explanation": "All reads within a multi-document transaction with snapshot read concern see a consistent snapshot of data."
    },
    {
        "id": "ae_easy_105",
        "question": "What problem can occur with 'local' read concern in transactions?",
        "options": [
            "Slower performance",
            "Read skew if another transaction commits between reads",
            "Higher memory usage",
            "Cannot read any data"
        ],
        "correct": 1,
        "explanation": "Local read concern inside a transaction reads the most recent data but without snapshot isolation and can cause read skew if another transaction commits between two reads in the same transaction."
    }
]

NEW_AE_MEDIUM = [
    {
        "id": "ae_medium_59",
        "question": "How many read concern levels do distributed transactions support?",
        "options": [
            "All five levels",
            "Only three: local, majority, and snapshot",
            "Only two: local and majority",
            "Only snapshot"
        ],
        "correct": 1,
        "explanation": "Distributed transactions support only three read concern levels: 'local', 'majority', and 'snapshot'."
    },
    {
        "id": "ae_medium_60",
        "question": "When is the transaction-level write concern applied?",
        "options": [
            "On each individual write",
            "Only at commit time",
            "At transaction start",
            "Never automatically"
        ],
        "correct": 1,
        "explanation": "Transactions use the transaction-level write concern to commit the write operations, and at commit time, the writes are committed using the transaction-level write concern."
    },
    {
        "id": "ae_medium_61",
        "question": "What does read concern 'linearizable' ensure?",
        "options": [
            "Fastest reads possible",
            "Node is still primary and data won't be rolled back",
            "Reads from all nodes",
            "Historical data access"
        ],
        "correct": 1,
        "explanation": "Linearizable read concern ensures that a node is still the primary member at the time of the read and that the data will not be rolled back if another node is elected as new primary."
    },
    {
        "id": "ae_medium_62",
        "question": "What is the trade-off when using w: 1 write concern?",
        "options": [
            "Faster writes but data may be lost on primary failure",
            "Slower writes but guaranteed durability",
            "No trade-off",
            "Uses more memory"
        ],
        "correct": 0,
        "explanation": "w: 1 means acknowledged by the primary only, which provides faster writes but data could be lost if the primary fails before replicating."
    }
]

NEW_AE_HARD = [
    {
        "id": "ae_hard_59",
        "question": "What combination of read and write concern provides the strongest consistency guarantee for transactions?",
        "options": [
            "local read concern with w: 1",
            "majority read concern with w: 1",
            "snapshot read concern with w: 'majority'",
            "local read concern with w: 'majority'"
        ],
        "correct": 2,
        "explanation": "Read concern 'snapshot' returns data from a snapshot of majority committed data when the transaction commits with write concern 'majority', providing the strongest consistency guarantee."
    },
    {
        "id": "ae_hard_60",
        "question": "Why can't linearizable read concern be used in multi-document transactions?",
        "options": [
            "It's too slow",
            "It requires checking primary status which conflicts with transaction isolation",
            "It uses too much memory",
            "It's deprecated"
        ],
        "correct": 1,
        "explanation": "Linearizable read concern requires verifying the node is still primary at read time, which would break transaction snapshot isolation guarantees."
    },
    {
        "id": "ae_hard_61",
        "question": "What happens to transaction writes if write concern 'majority' cannot be satisfied within wtimeout?",
        "options": [
            "Transaction auto-commits with w: 1",
            "Transaction aborts and rolls back",
            "Transaction waits indefinitely",
            "Transaction commits but logs a warning"
        ],
        "correct": 1,
        "explanation": "If the write concern cannot be satisfied within the specified wtimeout, the transaction aborts and all changes are rolled back."
    }
]

def main():
    # Load existing questions
    with open('questions.json', 'r') as f:
        data = json.load(f)
    
    # Get existing question texts for uniqueness check
    existing_questions = set()
    for category in ['atlas', 'ae']:
        for difficulty in ['easy', 'medium', 'hard']:
            for q in data[category][difficulty]:
                existing_questions.add(q['question'].lower().strip())
    
    # Track statistics
    added_count = 0
    duplicate_count = 0
    
    # Add new questions if they don't already exist
    new_questions_map = {
        ('atlas', 'easy'): NEW_ATLAS_EASY,
        ('atlas', 'medium'): NEW_ATLAS_MEDIUM,
        ('atlas', 'hard'): NEW_ATLAS_HARD,
        ('ae', 'easy'): NEW_AE_EASY,
        ('ae', 'medium'): NEW_AE_MEDIUM,
        ('ae', 'hard'): NEW_AE_HARD,
    }
    
    for (category, difficulty), new_questions in new_questions_map.items():
        for question in new_questions:
            q_text = question['question'].lower().strip()
            if q_text not in existing_questions:
                data[category][difficulty].append(question)
                existing_questions.add(q_text)
                added_count += 1
                print(f"✓ Added: {question['id']} - {question['question'][:60]}...")
            else:
                duplicate_count += 1
                print(f"✗ Duplicate: {question['id']} - {question['question'][:60]}...")
    
    # Save updated questions
    with open('questions.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    # Print summary
    print(f"\n{'='*80}")
    print(f"Summary:")
    print(f"  Added: {added_count} new questions")
    print(f"  Duplicates skipped: {duplicate_count}")
    print(f"  Total questions now: {sum(len(data[cat][diff]) for cat in ['atlas', 'ae'] for diff in ['easy', 'medium', 'hard'])}")
    print(f"{'='*80}")

if __name__ == '__main__':
    main()
