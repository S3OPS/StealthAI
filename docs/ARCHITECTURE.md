# StealthAI Architecture

This document explains the technical architecture of StealthAI.

## System Overview

StealthAI is built on two core principles:
1. **Signal Compression** - Focus on high-value conversion signals
2. **Micro-Stacking** - Parallel task execution for efficiency

```
┌─────────────────────────────────────────────────────────────┐
│                      StealthAI Engine                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Signal     │  │    Micro     │  │   Content    │      │
│  │ Compression  │─>│   Stacking   │─>│  Generation  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                 │                   │              │
│         └─────────────────┴───────────────────┘              │
│                          │                                   │
│              ┌───────────┴───────────┐                       │
│              │                       │                       │
│    ┌─────────▼────────┐   ┌─────────▼────────┐             │
│    │     Amazon        │   │     YouTube      │             │
│    │    Affiliate      │   │   Automation     │             │
│    └──────────────────┘   └──────────────────┘             │
│              │                       │                       │
│              └───────────┬───────────┘                       │
│                          │                                   │
│                  ┌───────▼───────┐                          │
│                  │   Revenue     │                          │
│                  │   Tracking    │                          │
│                  └───────────────┘                          │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Signal Compression

**Purpose:** Filter and prioritize data to focus on high-converting signals.

**How it works:**
- Accepts signals with strength scores (0-1)
- Filters by threshold (default: 0.7 = 70% confidence)
- Compresses to top percentage (default: 30%)
- Returns only high-value signals

**Example:**
```python
compressor = SignalCompressor(
    compression_ratio=0.3,  # Keep top 30%
    threshold=0.7           # Min 70% strength
)

signals = [
    {'value': 'keyword1', 'strength': 0.9},
    {'value': 'keyword2', 'strength': 0.5},  # Filtered out
    {'value': 'keyword3', 'strength': 0.8}
]

compressed = compressor.compress_signals(signals)
# Returns: keyword1, keyword3
```

**Benefits:**
- Reduces noise in data
- Focuses AI on high-value content
- Improves conversion rates
- Reduces processing time

### 2. Micro-Stacking

**Purpose:** Execute AI tasks in parallel with intelligent dependency management.

**How it works:**
- Tasks organized by priority (LOW, MEDIUM, HIGH, CRITICAL)
- Resolves dependencies between tasks
- Executes tasks in parallel batches
- Manages timeouts and errors

**Task Flow:**
```
┌─────────┐
│ Task 1  │ (Priority: HIGH)
└────┬────┘
     │
     ├──> Dependency
     │
┌────▼────┐
│ Task 2  │ (Priority: MEDIUM, depends on Task 1)
└─────────┘

Batch 1: [Task 1, Task 3, Task 4] (parallel)
Batch 2: [Task 2, Task 5]         (parallel, after dependencies)
```

**Example:**
```python
stacker = MicroStacker(
    max_depth=5,        # Max tasks per batch
    parallel_tasks=3    # 3 parallel workers
)

task = MicroTask(
    id="generate_content",
    function=generate_content_func,
    args=(topic, keywords),
    priority=TaskPriority.HIGH,
    dependencies=[]
)

stacker.add_task(task)
results = stacker.execute_stack()
```

**Benefits:**
- Faster content generation
- Better resource utilization
- Handles complex workflows
- Fault tolerance

### 3. AI Engine

**Purpose:** Generate content using free AI tools.

**Supported AI Tools:**
- Ollama (local models)
- LM Studio
- Any OpenAI-compatible API

**Content Types:**
- Video scripts
- Product reviews
- YouTube metadata (titles, descriptions, tags)
- Optimized conversion copy

**Flow:**
```
Prompt → AI Model → Raw Content → Optimization → Final Content
```

**Features:**
- Automatic fallback to backup models
- Template generation if AI unavailable
- Context-aware content
- SEO optimization

### 4. Amazon Affiliate Integration

**Purpose:** Monetize content with Amazon affiliate links.

**Features:**
- Affiliate link generation
- Product recommendations
- Product showcases
- Comparison tables
- SEO optimization
- Conversion tracking

**Link Generation:**
```python
affiliate = AmazonAffiliate(tracking_id="yourname-20")

# Simple link
link = affiliate.generate_affiliate_link("B08N5WRWNW")
# Output: https://www.amazon.com/dp/B08N5WRWNW?tag=yourname-20

# With campaign tracking
link = affiliate.generate_affiliate_link(
    "B08N5WRWNW", 
    campaign="tech-review"
)
```

**Product Showcase:**
- Formatted product lists
- Automatic affiliate link insertion
- Proper disclosure statements
- SEO-friendly formatting

### 5. YouTube Automation

**Purpose:** Optimize and schedule YouTube content.

**Features:**
- Metadata optimization (title, description, tags)
- Upload scheduling
- Series creation
- Playlist management
- Thumbnail text generation
- End screen configuration

**Metadata Optimization:**
```
Original Title: "Tech Gadgets"
Optimized: "Best Budget Tech Gadgets You Need in 2024 | Top 5"

Original Description: "Some tech gadgets"
Optimized:
- Keyword-rich opening
- Timestamps
- Hashtags
- Call-to-action
- Affiliate disclosure
```

**Upload Strategy:**
- Best upload times by audience
- Optimal frequency (daily, every 2 days, weekly)
- Series sequencing
- Playlist organization

### 6. Revenue Tracking

**Purpose:** Monitor progress toward revenue targets.

**Metrics Tracked:**
- Total revenue
- Revenue by source (Amazon, YouTube)
- Clicks and conversions
- Conversion rates
- Daily breakdown
- Campaign performance

**Predictive Analytics:**
- Average daily revenue
- Projected target dates
- Performance trends
- Top campaigns

**Example:**
```python
tracker = RevenueTracker(
    quick_target=310,
    main_target=8700
)

tracker.add_metric(RevenueMetric(
    date='2024-01-31',
    source='amazon',
    clicks=150,
    conversions=8,
    revenue=45.50,
    campaign='tech-gadgets'
))

report = tracker.get_progress_report()
# Shows progress, predictions, top campaigns
```

## Data Flow

### Content Generation Pipeline

```
1. Input
   ├─ Topic
   ├─ Keywords
   └─ Product ASINs

2. Signal Compression
   ├─ Filter keywords by strength
   └─ Keep top 30%

3. Micro-Stacking
   ├─ Create tasks
   ├─ Set priorities
   └─ Define dependencies

4. AI Generation (parallel)
   ├─ Generate script
   ├─ Generate metadata
   └─ Generate product content

5. Optimization
   ├─ YouTube metadata optimization
   ├─ Affiliate link generation
   └─ SEO enhancement

6. Output
   ├─ Complete content package
   ├─ Upload schedule
   └─ Revenue tracking setup
```

## Performance Characteristics

### Signal Compression
- **Time Complexity:** O(n log n) - sorting signals
- **Space Complexity:** O(n) - storing signals
- **Compression Ratio:** Configurable (default: 30%)

### Micro-Stacking
- **Parallel Workers:** Configurable (default: 3)
- **Task Throughput:** ~10-15 tasks/minute
- **Dependency Resolution:** O(n²) worst case

### AI Generation
- **Response Time:** 5-30 seconds per request
- **Fallback Strategy:** 3 model attempts
- **Caching:** Not implemented (future enhancement)

## Configuration Options

### Signal Compression
```json
{
  "compression_ratio": 0.3,  // 0.1 to 1.0
  "signal_threshold": 0.7,   // 0.0 to 1.0
  "batch_size": 10           // Any positive integer
}
```

### Micro-Stacking
```json
{
  "max_stack_depth": 5,      // Tasks per batch
  "parallel_tasks": 3,       // Worker threads
  "task_timeout": 300        // Seconds
}
```

### AI Tools
```json
{
  "ollama_endpoint": "http://localhost:11434",
  "default_model": "llama2",
  "fallback_models": ["mistral", "neural-chat"]
}
```

## Scaling Considerations

### Horizontal Scaling
- Run multiple instances with different niches
- Separate instances per revenue stream
- Load balance AI requests

### Vertical Scaling
- Increase `parallel_tasks` for more CPU cores
- Use faster AI models (e.g., mistral vs llama2)
- Adjust compression ratio for speed vs quality

### Resource Usage
- **CPU:** Moderate (AI generation)
- **Memory:** Low (~100MB base + AI model)
- **Network:** Low (API calls only)
- **Storage:** Minimal (logs and configs)

## Security Architecture

### API Key Management
- Config file (local only)
- Environment variables
- Never logged or exposed

### Data Privacy
- All processing local
- No third-party data sharing
- API calls only to configured services

### Affiliate Compliance
- Automatic disclosure insertion
- FTC guideline adherence
- Amazon TOS compliance

## Extension Points

### Custom AI Providers
```python
class CustomAIProvider(AIEngine):
    def _call_ollama(self, prompt, model, max_length):
        # Custom implementation
        pass
```

### Custom Revenue Sources
```python
class CustomRevenueSource:
    def track_conversion(self, data):
        # Custom tracking
        pass
```

### Custom Content Formats
```python
def generate_custom_format(topic, keywords):
    # Custom content generation
    pass
```

## Error Handling

### AI Generation Failures
1. Try primary model
2. Try fallback models
3. Use template generation
4. Log error, continue execution

### API Failures
1. Retry with exponential backoff
2. Use cached data if available
3. Skip and continue with next task
4. Log for manual review

### Task Failures
1. Log error details
2. Mark task as failed
3. Continue with other tasks
4. Report in final summary

---

**Architecture designed for reliability, scalability, and revenue generation** 🚀
