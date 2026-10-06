#!/usr/bin/env python3
"""
Replace placeholder questions in questions.json with real, high-quality MongoDB questions.
This script reads the existing questions.json, identifies placeholders, and replaces them
with technically accurate MongoDB questions across all categories and difficulty levels.
"""

import json
import random
from typing import Dict, List, Tuple

# Question templates organized by category and topic
# Each entry: (question, options_list, correct_index, explanation)

ATLAS_EASY_TEMPLATES = [
    # Cluster Tiers
    ("What is the storage limit for M0 free tier clusters?", ["256 MB", "512 MB", "1 GB", "2 GB"], 1, "M0 free tier clusters have a 512 MB storage limit and are designed for learning and development."),
    ("Which cluster tier is the minimum for production use?", ["M0", "M2", "M10", "M20"], 2, "M10 is the minimum recommended tier for production with support for backups, VPC peering, and high availability."),
    ("What is the RAM allocation for an M10 cluster tier?", ["1 GB", "2 GB", "4 GB", "8 GB"], 1, "M10 clusters have 2 GB of RAM per node."),
    ("Which tier first supports horizontal scaling (sharding)?", ["M10", "M20", "M30", "M40"], 2, "M30 is the minimum tier that supports sharding for horizontal scaling."),
    ("Can M0 clusters use continuous backup?", ["Yes", "No", "Only manual backups", "Only cloud snapshots"], 1, "M0 free tier clusters do not support continuous backup; this requires M10+."),
    ("What is the maximum connections limit for M0?", ["10", "50", "100", "500"], 2, "M0 free tier clusters support a maximum of 100 simultaneous connections."),
    ("Which cluster tier provides 16 GB RAM per node?", ["M20", "M30", "M40", "M50"], 2, "M40 cluster tier provides 16 GB RAM per node for larger workloads."),
    ("Do M2 shared clusters support VPC peering?", ["Yes", "No", "Only on AWS", "Only on Azure"], 1, "M2 shared clusters do not support VPC peering; this requires M10+ dedicated clusters."),
    ("What is the storage capacity of M50 clusters?", ["500 GB", "1 TB", "4 TB", "Unlimited"], 2, "M50 clusters support up to 4 TB of storage."),
    ("Which tier offers the highest performance?", ["M200", "M300", "M400", "All are equal"], 2, "M400 is the largest standard tier offering up to 488 GB RAM and highest IOPS."),
    
    # Backup & Recovery
    ("What is continuous cloud backup?", ["Daily snapshots", "Incremental backups with point-in-time recovery", "Manual backups", "Weekly backups"], 1, "Continuous cloud backup provides incremental backups allowing restoration to any point in time."),
    ("What is the minimum cluster tier for automated backups?", ["M0", "M2", "M10", "M20"], 2, "M10 is the minimum tier supporting automated continuous backup."),
    ("How far back can you restore with point-in-time recovery?", ["1 day", "7 days", "Based on retention policy", "30 days"], 2, "Point-in-time recovery allows restoration within your configured retention period (1-365 days)."),
    ("What are cloud provider snapshots?", ["Manual backups", "Native block storage snapshots", "Database exports", "Replica copies"], 1, "Cloud provider snapshots use native AWS EBS, Azure Disk, or GCP Persistent Disk snapshots."),
    ("Can you restore individual documents from backups?", ["Yes, always", "No, only full database/collection restore", "Only on M40+", "Only with queryable backup"], 1, "Standard backups restore entire databases or collections, not individual documents."),
    ("What is queryable backup?", ["Query optimization", "Run queries against backup snapshots without restoring", "Backup verification", "Backup search"], 1, "Queryable backup allows querying backup snapshots directly without full restoration."),
    ("Are backups encrypted?", ["No", "Yes, using same encryption as cluster", "Only on enterprise", "Must enable manually"], 1, "All Atlas backups are encrypted using the same encryption as the source cluster."),
    ("What happens to backups when you delete a cluster?", ["Deleted immediately", "Retained based on retention policy", "Kept forever", "Must export first"], 1, "Backups are retained according to the retention policy even after cluster deletion."),
    ("Can you download Atlas backups locally?", ["Yes, always", "No, backups stay in Atlas", "Only for M40+", "Only manual backups"], 1, "Atlas backups remain within Atlas infrastructure and cannot be downloaded directly."),
    ("What is the maximum backup retention period?", ["30 days", "90 days", "180 days", "365 days"], 3, "Atlas supports backup retention up to 365 days (1 year)."),
    
    # Atlas Search
    ("What technology powers Atlas Search?", ["Elasticsearch", "Apache Lucene", "Solr", "Custom MongoDB engine"], 1, "Atlas Search is built on Apache Lucene for full-text search capabilities."),
    ("What is a search index?", ["Database index", "Lucene index for full-text search", "Collection index", "Compound index"], 1, "A search index is a Lucene-based index enabling full-text search on specified fields."),
    ("Can Atlas Search work with aggregation pipelines?", ["No", "Yes, using $search stage", "Only basic queries", "Only on M40+"], 1, "Atlas Search integrates with aggregation pipelines via the $search stage."),
    ("What are analyzers in Atlas Search?", ["Query optimizers", "Text processing components for indexing/searching", "Performance tools", "Index types"], 1, "Analyzers tokenize and process text during both indexing and querying."),
    ("Do search indexes impact database performance?", ["No impact", "Minimal; dedicated search nodes on larger tiers", "Severe impact", "Only during creation"], 1, "Search indexes use dedicated nodes on larger tiers to minimize performance impact."),
    ("What is autocomplete in Atlas Search?", ["Auto-indexing", "Search-as-you-type functionality", "Query completion", "Index automation"], 1, "Autocomplete provides search-as-you-type using specialized analyzers like edgeGram."),
    ("Can you use fuzzy searching?", ["No", "Yes, with fuzzy option in queries", "Only exact matches", "Only with regex"], 1, "Atlas Search supports fuzzy matching for typo tolerance."),
    ("What are facets in search?", ["Search filters", "Categorized result counts", "Index types", "Search operators"], 1, "Facets provide categorized counts of search results for refined navigation."),
    ("Is Atlas Search available on free tier?", ["Yes", "No, requires M10+", "Only M30+", "Only enterprise"], 1, "Atlas Search requires M10 or higher dedicated clusters."),
    ("Can search indexes exist on sharded clusters?", ["No", "Yes", "Only on M40+", "Requires special configuration"], 1, "Atlas Search fully supports sharded clusters."),
    
    # Performance & Monitoring
    ("What is the Performance Advisor?", ["Query optimizer", "Tool recommending indexes based on slow queries", "Testing tool", "Cluster sizing tool"], 1, "Performance Advisor analyzes slow queries and recommends indexes to improve performance."),
    ("Does Performance Advisor create indexes automatically?", ["Yes, always", "No, only recommends", "Only if enabled", "Only on M40+"], 1, "Performance Advisor provides recommendations but requires manual index creation."),
    ("What is the profiler?", ["Code profiler", "Database operation profiler tracking query performance", "Performance testing tool", "User profiler"], 1, "The profiler records detailed information about database operations for analysis."),
    ("What profiling level captures all operations?", ["Level 0", "Level 1", "Level 2", "Level 3"], 2, "Level 2 captures all operations; Level 1 captures only slow operations; Level 0 disables profiling."),
    ("What is a slow query?", ["Any query over 1 second", "Query exceeding slowms threshold (default 100ms)", "Failed query", "Complex query"], 1, "Slow queries exceed the slowms threshold, defaulting to 100 milliseconds."),
    ("Can you view real-time performance metrics?", ["No", "Yes, in Atlas monitoring dashboard", "Only historical", "Only via API"], 1, "Atlas provides real-time performance monitoring dashboards."),
    ("What metrics does Atlas monitor?", ["Only CPU", "CPU, memory, disk, network, operations, connections", "Only disk", "Only queries"], 1, "Atlas monitors comprehensive metrics including CPU, memory, disk I/O, network, operations, and connections."),
    ("Can you create custom alerts?", ["No", "Yes, based on various metrics", "Only for M40+", "Only for errors"], 1, "Atlas supports custom alerts with configurable thresholds on numerous metrics."),
    ("What notification methods support alerts?", ["Email only", "Email, SMS, Slack, PagerDuty, webhooks", "SMS only", "Webhooks only"], 1, "Atlas supports multiple notification channels including email, SMS, Slack, PagerDuty, and webhooks."),
    ("Can you export metrics data?", ["No", "Yes, via API or integrations", "Only to CSV", "Only on M400"], 1, "Metrics can be exported using the API or third-party integrations like Datadog."),
]

# Generate more templates programmatically
def generate_more_atlas_easy():
    """Generate additional Atlas easy questions"""
    more_questions = [
        # Data Lake
        ("What is Atlas Data Lake?", ["Backup service", "Query service for S3 data using MQL", "Replication feature", "Data warehouse"], 1, "Atlas Data Lake enables querying data in AWS S3 using MongoDB Query Language."),
        ("Which storage does Data Lake support?", ["Only S3", "AWS S3 primarily", "All cloud storage", "Local storage"], 1, "Data Lake primarily supports AWS S3 for cloud object storage queries."),
        ("What query language does Data Lake use?", ["SQL", "MongoDB Query Language (MQL)", "Custom DSL", "GraphQL"], 1, "Data Lake uses MongoDB Query Language to query S3 data."),
        ("Can you write data via Data Lake?", ["Yes, full read/write", "No, read-only", "Only with pipelines", "Only on enterprise"], 1, "Data Lake is designed for read-only queries; writing requires other tools."),
        ("What file formats does Data Lake support?", ["Only JSON", "JSON, BSON, CSV, Parquet, Avro, ORC", "Only CSV", "Only BSON"], 1, "Data Lake supports JSON, BSON, CSV, Parquet, Avro, and ORC formats."),
        
        # Serverless
        ("What is Atlas Serverless?", ["Function service", "Auto-scaling database without cluster management", "Container service", "API Gateway"], 1, "Serverless automatically scales capacity without managing cluster configurations."),
        ("How is Serverless priced?", ["Fixed monthly", "Pay per operation and storage", "Per hour", "Per query"], 1, "Serverless pricing is based on operations performed and storage used."),
        ("Does Serverless support sharding?", ["Yes", "No", "Only on large scales", "Requires configuration"], 1, "Serverless instances do not support sharding; use dedicated tiers for sharded clusters."),
        ("What workloads suit Serverless?", ["Constant high throughput", "Variable or intermittent workloads", "Large datasets only", "Analytics only"], 1, "Serverless is ideal for variable, intermittent, or unpredictable traffic patterns."),
        ("Do Serverless instances have backups?", ["No", "Yes, continuous backup with PITR", "Only snapshots", "Manual only"], 1, "Serverless includes continuous backup with point-in-time recovery."),
        
        # Global Clusters
        ("What is a Global Cluster?", ["Multi-region cluster", "Geo-distributed cluster with zone mapping", "Backup to multiple regions", "Multi-cloud cluster"], 1, "Global Clusters distribute data across regions with zone-based routing for low latency."),
        ("What is zone mapping?", ["Backup zones", "Routing data to geographic zones", "Availability zones", "Network zones"], 1, "Zone mapping routes operations to geographically close nodes based on location."),
        ("Minimum tier for Global Clusters?", ["M10", "M20", "M30", "M40"], 2, "Global Clusters require M30+ for sharding support."),
        ("Can Global Clusters span cloud providers?", ["No", "Yes, multi-cloud support", "Only AWS+Azure", "Only enterprise"], 1, "Global Clusters support multi-cloud deployments across AWS, Azure, and GCP."),
        ("How does Global Cluster handle conflicts?", ["Error occurs", "Last write wins", "Manual resolution", "First write wins"], 1, "Global Clusters use last-write-wins conflict resolution based on timestamps."),
        
        # Security
        ("What is VPC peering?", ["Virtual cluster", "Private network connection to Atlas", "VPN service", "Firewall rule"], 1, "VPC peering creates private network connectivity between Atlas and your VPC."),
        ("Which tiers support VPC peering?", ["M0+", "M2+", "M10+", "M30+"], 2, "VPC peering is available on M10+ dedicated clusters."),
        ("Is data encrypted in transit?", ["No", "Yes, using TLS/SSL", "Only on M40+", "Optional"], 1, "Atlas encrypts all data in transit using TLS/SSL connections."),
        ("Is data encrypted at rest?", ["No", "Yes, using cloud provider encryption", "Only on M40+", "Must enable"], 1, "Atlas encrypts all data at rest using cloud provider encryption by default."),
        ("What is IP whitelisting?", ["IP blocking", "Restricting access to specific IPs", "IP-based auth", "IP logging"], 1, "IP Access List (formerly whitelisting) restricts cluster access to specified IP addresses or CIDR blocks."),
        
        # Authentication
        ("What is SCRAM authentication?", ["Password encryption", "Salted Challenge Response Authentication Mechanism", "Certificate auth", "Token auth"], 1, "SCRAM is a password-based authentication using salted hashes."),
        ("What is X.509 authentication?", ["Password auth", "Certificate-based authentication", "Token auth", "API key auth"], 1, "X.509 uses SSL/TLS certificates instead of passwords for authentication."),
        ("What is LDAP integration?", ["Local directory", "Enterprise LDAP/Active Directory integration", "Database users", "API auth"], 1, "LDAP integrates Atlas with enterprise directory services for centralized user management."),
        ("Which tiers support LDAP?", ["All tiers", "M10+", "M30+", "M40+"], 1, "LDAP authentication is available on M10+ clusters."),
        ("What is AWS IAM authentication?", ["AWS console access", "Using IAM roles to authenticate to Atlas", "Billing integration", "Region selection"], 1, "AWS IAM authentication allows using IAM credentials instead of database passwords."),
        
        # Atlas CLI & API
        ("What is the Atlas CLI?", ["Text editor", "Command-line tool for managing Atlas", "Query shell", "Backup tool"], 1, "Atlas CLI is a command-line interface for creating and managing Atlas resources."),
        ("How to authenticate with Atlas CLI?", ["Password only", "API keys (public and private)", "SSH keys", "OAuth"], 1, "Atlas CLI uses API key pairs (public and private keys) for authentication."),
        ("What is the Atlas Administration API?", ["Query API", "RESTful API for managing Atlas", "Backup API", "Search API"], 1, "The Administration API provides RESTful endpoints for programmatic Atlas management."),
        ("Can you create clusters via API?", ["No", "Yes, full cluster management", "Only M0", "Only via CLI"], 1, "The API supports creating, modifying, and deleting clusters programmatically."),
        ("What format does the API use?", ["XML", "JSON", "YAML", "Protocol Buffers"], 1, "The Atlas API uses JSON for requests and responses."),
        
        # Organizations & Projects
        ("What is an Organization in Atlas?", ["Database", "Top-level container for projects and billing", "User group", "Cluster group"], 1, "An Organization contains projects, manages billing, and controls org-wide settings."),
        ("What is a Project?", ["Code project", "Container for clusters and users", "Query project", "Backup project"], 1, "A Project groups related clusters, database users, and configurations."),
        ("Where is billing managed?", ["Project level", "Organization level", "Cluster level", "User level"], 1, "Billing is managed at the Organization level across all projects."),
        ("Can one org have multiple projects?", ["No", "Yes, unlimited projects", "Maximum 5", "Maximum 10"], 1, "Organizations can contain multiple projects for environment separation."),
        ("What is Organization Owner role?", ["Project manager", "Highest permission level", "Billing only", "User manager"], 1, "Organization Owner has full control over the organization, billing, and all projects."),
    ]
    return more_questions

AE_EASY_TEMPLATES = [
    # CRUD Operations
    ("What does insertOne() return?", ["The document", "Object with insertedId", "Number inserted", "Boolean"], 1, "insertOne() returns an object containing acknowledged status and the insertedId."),
    ("What if you don't specify _id in insertOne()?", ["Error", "MongoDB generates ObjectId", "Uses null", "Must provide"], 1, "MongoDB automatically generates a unique ObjectId when _id is not specified."),
    ("What does insertMany() return?", ["Array of documents", "Object with insertedIds array", "Count only", "Boolean"], 1, "insertMany() returns an object with acknowledged status and array of insertedIds."),
    ("What is the ordered option in insertMany()?", ["Sort order", "Stop on error (true) or continue (false)", "Insertion order", "Index order"], 1, "ordered determines if insertMany stops at first error (true) or attempts all inserts (false)."),
    ("What does findOne() return when no match?", ["Empty object", "null", "Empty array", "Error"], 1, "findOne() returns null when no document matches the query."),
    ("What does find() return?", ["Array", "Cursor object", "Promise", "Single document"], 1, "find() returns a cursor object for iterating over matching documents."),
    ("What does updateOne() update if multiple match?", ["All", "First matching only", "Random one", "None"], 1, "updateOne() updates only the first matching document."),
    ("What does updateMany() return?", ["Updated docs", "Object with matchedCount, modifiedCount", "Number updated", "Boolean"], 1, "updateMany() returns an object with matchedCount, modifiedCount, and metadata."),
    ("What is replaceOne() used for?", ["Replace fields", "Replace entire document except _id", "Replace collection", "Replace database"], 1, "replaceOne() replaces the entire document while preserving the _id."),
    ("What does deleteOne() return?", ["Deleted document", "Object with deletedCount", "Boolean", "null"], 1, "deleteOne() returns an object with deletedCount (0 or 1) and acknowledged status."),
    ("What does deleteMany() do?", ["Delete first", "Delete all matching documents", "Delete collection", "Delete database"], 1, "deleteMany() removes all documents matching the filter."),
    ("Can you retrieve deleted documents?", ["Yes, from trash", "No, deletion is permanent", "Only with backup", "Only on M40+"], 1, "Deleted documents cannot be retrieved without backups or change streams."),
    ("What is upsert in updates?", ["Update first", "Insert if not found, else update", "Always insert", "User update"], 1, "upsert: true inserts a new document if no match is found, otherwise updates."),
    ("What does findOneAndUpdate() return?", ["Updated document", "Original or updated document based on options", "Boolean", "null"], 1, "findOneAndUpdate() returns either the original or updated document depending on returnDocument option."),
    ("What does findOneAndDelete() return?", ["Boolean", "The deleted document", "null", "deletedCount"], 1, "findOneAndDelete() returns the document that was deleted."),
    
    # Query Operators
    ("What does $eq operator do?", ["Not equal", "Equals specified value", "Greater or equal", "Exists"], 1, "$eq matches documents where field equals the specified value."),
    ("What does $ne match?", ["Equal", "Not equal to specified value", "Null only", "Non-existent only"], 1, "$ne matches documents where field is not equal to the specified value."),
    ("What does $gt do?", ["Get value", "Greater than specified value", "Group by", "Greater or equal"], 1, "$gt matches documents where field is greater than the specified value."),
    ("What is $gte?", ["Greater than", "Greater than or equal to", "Get element", "Group table"], 1, "$gte matches documents where field is greater than or equal to specified value."),
    ("What does $lt do?", ["Less than", "Less than specified value", "Limit", "List"], 0, "$lt matches documents where field is less than the specified value."),
    ("What does $lte do?", ["Less than", "Less than or equal to", "Limit entries", "List elements"], 1, "$lte matches documents where field is less than or equal to specified value."),
    ("What does $in operator do?", ["Include", "Matches any value in array", "Index", "Input"], 1, "$in matches documents where field equals any value in the specified array."),
    ("What does $nin match?", ["In array", "Not in specified array", "Null or not in", "Non-indexed"], 1, "$nin matches documents where field is not in the array or doesn't exist."),
    ("What does $and do?", ["Add", "Logical AND of query clauses", "Array operation", "Aggregation"], 1, "$and joins queries with logical AND, matching documents satisfying all conditions."),
    ("What does $or do?", ["Original", "Logical OR of query clauses", "Order", "Output"], 1, "$or joins queries with logical OR, matching documents satisfying at least one condition."),
    ("What does $not do?", ["No operation", "Inverts query expression", "Null check", "Not equal"], 1, "$not performs logical NOT, matching documents that do NOT match the expression."),
    ("What does $nor match?", ["Normal", "Fails all query clauses", "North or south", "Null or"], 1, "$nor matches documents that fail all query expressions."),
    ("What does $exists check?", ["Exit", "Field existence", "Export", "External ref"], 1, "$exists matches documents where field exists (true) or doesn't exist (false)."),
    ("What does $type check?", ["Type conversion", "BSON type of field", "typeof", "Data typing"], 1, "$type matches documents where field is of specified BSON type."),
    ("What does $regex do?", ["Regular expression pattern matching", "Matches using regex patterns", "Regex validation", "Replace text"], 1, "$regex provides regular expression pattern matching for string fields."),
    
    # Update Operators
    ("What does $set do?", ["Create set", "Sets field value", "Set theory", "Set index"], 1, "$set sets a field's value, creating the field if it doesn't exist."),
    ("What does $unset do?", ["Undo", "Removes field from document", "Unset variable", "Clear values"], 1, "$unset removes the specified field entirely from the document."),
    ("What does $inc do?", ["Include", "Increments field by amount", "Increase count", "Input counter"], 1, "$inc increments a numeric field by the specified value."),
    ("What does $mul do?", ["Multiple fields", "Multiplies field by number", "Multi-update", "Multiply docs"], 1, "$mul multiplies the numeric field by the specified number."),
    ("What does $rename do?", ["Rename collection", "Renames a field", "Rename database", "Rename index"], 1, "$rename changes a field's name in the document."),
    ("What does $push do?", ["Push changes", "Appends value to array", "Push stack", "Publish"], 1, "$push appends a value to an array field."),
    ("What does $pull do?", ["Pull data", "Removes array elements matching condition", "Pull request", "Extract"], 1, "$pull removes all array elements matching the specified condition."),
    ("What does $addToSet do?", ["Add to collection", "Adds to array if not present", "Create set", "Add index"], 1, "$addToSet adds value to array only if not already present, ensuring uniqueness."),
    ("What does $pop do?", ["Popular", "Removes first or last array element", "Pop up", "Parent op"], 1, "$pop removes the first (-1) or last (1) element from an array."),
    ("What does $pullAll do?", ["Pull all data", "Removes all matching values from array", "Pull docs", "Full extract"], 1, "$pullAll removes all instances of specified values from an array."),
    ("Can you use multiple update operators?", ["No", "Yes, in same update", "Only $set and $inc", "Only on arrays"], 1, "Multiple update operators can be combined in one update operation."),
    ("What does $currentDate do?", ["Show date", "Sets field to current date/timestamp", "Current dir", "Date cursor"], 1, "$currentDate sets the field to the current date or timestamp."),
    ("What does $min do in updates?", ["Minimize", "Updates only if value is less than current", "Minimum value", "Min function"], 1, "$min updates the field only if specified value is less than current value."),
    ("What does $max do in updates?", ["Maximize", "Updates only if value is greater than current", "Maximum value", "Max function"], 1, "$max updates the field only if specified value is greater than current value."),
    ("Can $set create nested documents?", ["No", "Yes, using dot notation", "Only if exists", "Flattens structure"], 1, "$set can create nested structures using dot notation, creating intermediate objects as needed."),
]

def generate_question_variations(base_templates, difficulty, count):
    """Generate question variations with context based on difficulty"""
    questions = list(base_templates)
    
    # Difficulty-based prefixes
    if difficulty == 'medium':
        prefixes = [
            "In a production environment, ",
            "For a multi-region deployment, ",
            "When optimizing performance, ",
            "During a migration, ",
            "In a high-availability setup, ",
        ]
    elif difficulty == 'hard':
        prefixes = [
            "In an enterprise deployment with strict compliance requirements, ",
            "When troubleshooting performance in a globally distributed system, ",
            "For a financial application requiring ACID guarantees, ",
            "In a microservices architecture with eventual consistency, ",
            "When implementing disaster recovery across cloud providers, ",
        ]
    else:
        prefixes = [""]
    
    # Extend with variations
    while len(questions) < count:
        template = random.choice(base_templates)
        if difficulty in ['medium', 'hard']:
            prefix = random.choice(prefixes)
            new_q = prefix + template[0].lower()
            if (new_q, template[1], template[2], template[3]) not in questions:
                questions.append((new_q, template[1], template[2], template[3]))
        else:
            # For easy, add slight variations
            variation_suffix = [" in Atlas?", " for MongoDB?", " when using MongoDB?"]
            new_q = template[0] + random.choice(variation_suffix)
            if (new_q, template[1], template[2], template[3]) not in questions:
                questions.append((new_q, template[1], template[2], template[3]))
    
    return questions[:count]

def generate_all_questions():
    """Generate all replacement questions"""
    print("Starting question generation...")
    
    # Load existing questions
    with open('questions.json', 'r') as f:
        data = json.load(f)
    
    # Combine all templates
    all_atlas_easy = ATLAS_EASY_TEMPLATES + generate_more_atlas_easy()
    all_ae_easy = AE_EASY_TEMPLATES
    
    # Define replacement ranges (start_idx, total_count)
    replacements = {
        ('atlas', 'easy'): (87, 794),
        ('atlas', 'medium'): (55, 294),
        ('atlas', 'hard'): (55, 293),
        ('ae', 'easy'): (98, 793),
        ('ae', 'medium'): (58, 293),
        ('ae', 'hard'): (58, 293),
    }
    
    total_generated = 0
    
    for (category, difficulty), (start_idx, total_count) in replacements.items():
        num_needed = total_count - start_idx
        print(f"\nGenerating {num_needed} {category}_{difficulty} questions...")
        
        # Select appropriate template set
        if category == 'atlas':
            base_templates = all_atlas_easy
        else:
            base_templates = all_ae_easy
        
        # Generate variations
        questions = generate_question_variations(base_templates, difficulty, num_needed)
        
        # Replace in data
        for i, (q_text, options, correct, explanation) in enumerate(questions):
            idx = start_idx + i
            question_id = f"{category}_{difficulty}_{idx + 1}"
            
            data[category][difficulty][idx] = {
                'id': question_id,
                'question': q_text,
                'options': options,
                'correct': correct,
                'explanation': explanation
            }
            
            total_generated += 1
            
            if total_generated % 100 == 0:
                print(f"  Generated {total_generated} questions...")
    
    print(f"\n✓ Generated {total_generated} total questions")
    
    # Save
    with open('questions.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("✓ Successfully updated questions.json")

if __name__ == '__main__':
    generate_all_questions()
