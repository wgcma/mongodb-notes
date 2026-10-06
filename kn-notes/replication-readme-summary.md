# MongoDB Replication README Summary

**Source**: [MongoDB Replication README](https://github.com/mongodb/mongo/blob/4e90f0985468068e491ed2b3767d998e1071c2dd/src/mongo/db/repl/README.md)

---

## Document Overview

This README provides deep technical documentation of MongoDB's replication system internals, covering how replica sets maintain data consistency and availability across multiple nodes.

---

## Section-by-Section Summary

### **Introduction**
> *High-level overview of MongoDB's replica set architecture and fundamental concepts.*

MongoDB uses replica sets (one primary + multiple secondaries) for replication. The primary handles all writes and logs them to the oplog; secondaries continuously pull and apply these operations. Drivers automatically route operations to the appropriate nodes.

---

### **Steady State Replication**
> *How the primary logs operations and secondaries replicate them during normal operation.*

**On the Primary:**
- Every write operation gets applied to the database and logged to `oplog.rs` (a capped collection in the `local` database)
- The `OpObserver` subsystem handles oplog entry creation
- Operations are rewritten to be idempotent (e.g., `$inc` becomes `$set`)
- Write concern determines how many replicas must acknowledge before the operation returns

**On Secondaries:**
- The `OplogFetcher` pulls oplog entries from a chosen sync source using an exhaust cursor
- Entries are buffered in the `OplogBuffer`
- The `OplogApplier` applies operations in batches, parallelizing when safe (serializing operations on the same document)
- The `BackgroundSync` component coordinates the entire secondary replication process

---

### **Write Concern and Commit Point**
> *How MongoDB ensures data durability and tracks which operations are safe from rollback.*

- Write concern specifies how many nodes must replicate a write before acknowledging
- The **commit point** is the OpTime where all earlier operations have replicated to a majority
- Operations before the commit point cannot be rolled back
- The `ReplicationCoordinator` tracks the commit point and advances it as secondaries report progress

---

### **Write Concern Defaults**
> *How MongoDB determines default write concern when not explicitly specified.*

Three-level hierarchy:
1. **Cluster-Wide Write Concern**: Set via `setDefaultRWConcern` command
2. **Implicit Default Write Concern (IDWC)**: Calculated formula based on replica set configuration
3. **Hardcoded Fallback**: `{w: 1}` if no other defaults exist

Special handling for PSA (Primary-Secondary-Arbiter) topologies to prevent unsatisfiable majority write concerns.

---

### **Oplog Fetching**
> *Detailed mechanics of how secondaries retrieve oplog entries from their sync source.*

- Uses an **exhaust cursor** for efficient streaming without repeated getMore commands
- Fetcher runs in a separate thread (`ReplBatcher-*`)
- Handles network errors, rollback scenarios, and sync source changes
- Batches are fetched and enqueued into the `OplogBuffer`

---

### **Sync Source Selection**
> *How secondaries choose which node to replicate from.*

- The `SyncSourceResolver` finds candidates based on:
  - Oplog lag thresholds
  - Network ping times
  - Read preference settings
  - Chaining allowed configuration
- The `TopologyCoordinator` makes the final selection
- Secondaries can change sync sources if their current source becomes stale or unavailable

---

### **Oplog Entry Application**
> *How buffered oplog entries are applied to the secondary's database.*

- The `OplogApplier` processes entries in batches
- Operations are grouped and parallelized across multiple writer threads where possible
- Operations on the same document must be serialized to maintain consistency
- Each batch is applied atomically with respect to reads
- After application, the `lastApplied` OpTime is advanced

---

### **Timestamps and OpTimes**
> *Understanding the logical and physical timestamps that track replication progress.*

Key timestamps maintained:
- **lastApplied**: Most recent oplog entry applied to the database
- **lastWritten**: Most recent entry written to the oplog (on primary) or buffered (on secondary)
- **lastDurable**: Most recent entry guaranteed on disk

**OpTime** consists of:
- **Timestamp**: BSON timestamp from the oplog entry
- **Term**: Election term number (from Raft-based protocol)

---

### **Replication Coordinator**
> *The central public API for all replication-related interactions.*

- The `ReplicationCoordinator` interface provides methods for:
  - Write concern waiting
  - Election management
  - Configuration changes
  - Replication state queries
- Implementation (`ReplicationCoordinatorImpl`) coordinates between all replication subsystems
- Runs in REPL mode (vs NONE for standalone servers)

---

### **Topology Coordinator**
> *Manages replica set topology state and makes replication decisions.*

- Maintains the view of the entire replica set topology
- Makes decisions about:
  - Sync source selection
  - Election participation
  - Heartbeat responses
- Uses a single-threaded event loop to process topology changes
- Does not directly interact with the network (delegates to `ReplicationCoordinator`)

---

### **Heartbeats and Failure Detection**
> *How nodes monitor each other's health and detect failures.*

- Every node sends heartbeats to all other nodes every 2 seconds (configurable)
- The `replSetHeartbeat` command returns node status, config version, and OpTime
- Missed heartbeats trigger failure detection
- The `TopologyCoordinator` processes heartbeat responses and updates node states

---

### **Elections**
> *How the replica set chooses a new primary when needed.*

- Based on Raft consensus protocol (MongoDB uses "PV1" - Protocol Version 1)
- Elections are triggered by:
  - Primary failure detection
  - Priority-based step-down
  - Manual election calls
- Each election occurs in a numbered **term**
- A candidate needs a majority of votes to become primary
- Higher priority nodes are preferred during elections

---

### **Rollback**
> *What happens when a former primary's uncommitted writes must be undone.*

- Occurs when a node was primary but its writes didn't replicate to a majority before stepping down
- The `RollbackImpl` compares the local oplog with the sync source's oplog
- Finds the common point and undoes operations after that point
- Rolled-back operations are written to rollback files for potential recovery
- After rollback, the node resyncs from the common point forward

---

### **Initial Sync**
> *How a new or stale node performs a full copy of data from another replica set member.*

Three phases:
1. **Collection Copy**: Copy all collections and indexes from the sync source
2. **Oplog Application**: Apply operations that occurred during collection copy
3. **Final Sync**: Apply remaining operations until fully caught up

The `InitialSyncer` coordinates this process, handling errors and retries.

---

### **Read Concern**
> *Consistency guarantees for read operations on replica sets.*

Read concern levels:
- **local**: Read most recent data (default, may be rolled back)
- **majority**: Read data replicated to a majority (safe from rollback)
- **linearizable**: Read with guarantee this node is still primary
- **snapshot**: Read from a consistent point-in-time snapshot
- **available**: Read without waiting (similar to local)

The `ReadConcernArgs` class encapsulates these settings.

---

### **Speculative Majority Reads**
> *Optimization that allows reading potentially-majority-committed data without waiting.*

- Allows reads of data that will "probably" become majority-committed soon
- Reduces latency for majority reads in common cases
- If data isn't committed by the time the read occurs, falls back to waiting
- Implemented via the `SpeculativeMajorityReadInfo` class

---

### **Replication Metrics and Observability**
> *Monitoring and debugging tools for replication health.*

Key metrics and commands:
- `replSetGetStatus`: Comprehensive replica set status
- `serverStatus` (repl section): Replication statistics
- Oplog metrics: Lag, window, GB/hour rate
- Election metrics: Calls, successful elections, step-downs
- Thread pool metrics: Applied ops/second, batches/second

---

### **Configuration Management**
> *How replica set configurations are created, changed, and propagated.*

- Configuration stored in `local.system.replset` collection
- The `ReplicaSetConfig` class represents the configuration
- Config changes use a two-phase protocol:
  1. Propose new config
  2. Replicate and install on majority
- Config version number increases with each change
- Reconfigurations can add/remove nodes, change priorities, modify settings

---

### **Cluster Time and Logical Clock**
> *How MongoDB tracks causality across distributed operations.*

- **Logical Clock**: Monotonically increasing timestamp across the cluster
- **Cluster Time**: The highest logical clock value seen in the cluster
- Used for:
  - Causal consistency
  - Snapshot reads
  - Change streams
- The `LogicalClock` and `VectorClock` classes implement this functionality

---

### **Communication Between Nodes**
> *Network protocols and commands used for replica set coordination.*

Primary communication methods:
1. **hello/isMaster**: Node discovery and state information
2. **replSetHeartbeat**: Health checks and topology updates
3. **Oplog fetching**: Data replication via tailable cursors
4. **replSetUpdatePosition**: Secondaries report their replication progress

Nodes communicate using the `ReplicaSetMonitor` for connection management.

---

### **Testing and Debugging**
> *Tools and techniques for testing replication behavior.*

Key test utilities:
- **ReplSetTest**: JavaScript framework for integration tests
- **Failpoint**: Inject failures at specific code points
- **Stepdown commands**: Manually trigger failover scenarios
- **Replication logs**: Detailed logging with REPL component tag
- **Wait for state commands**: Synchronization primitives for tests

---

## Key Takeaways

1. **Architecture**: Primary writes to oplog → Secondaries pull and apply → Majority acknowledgment for durability
2. **Consistency**: Multiple read/write concern levels balance performance vs. safety
3. **Fault Tolerance**: Automatic elections and rollback handle failures gracefully
4. **Performance**: Parallel oplog application and speculative reads optimize throughput
5. **Observability**: Rich metrics and commands for monitoring replication health

---

## Related Components

- **Storage Engine**: Manages the underlying database files and oplog collection
- **OpObserver**: Hooks that fire when operations modify data (generates oplog entries)
- **Catalog**: Manages database and collection metadata
- **Sessions**: Tracks client sessions for retryable writes and transactions
- **Sharding**: Uses replication for each shard's data redundancy
