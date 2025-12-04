# Freesound Search Optimization Guide for Therapeutic Sleep Audio

## Overview

This comprehensive guide outlines advanced search strategies and best practices for finding high-quality, relevant therapeutic sleep sounds using the Freesound API. Based on extensive research of the Freesound documentation and capabilities.

## 🔍 Core Search Principles

### 1. Query Syntax Best Practices

**Advanced Query Operators:**

- `+term` - Mandatory term (MUST be present)
- `-term` - Prohibited term (MUST NOT be present)  
- `"exact phrase"` - Exact phrase matching
- `term1 term2` - Both terms should be present (weighted)

**Examples:**

```
+rain +gentle -thunder -storm    # Gentle rain without storms
"white noise" +sleep +constant   # Exact phrase with modifiers
+meditation +ambient -music      # Ambient meditation without music
```

### 2. Broad Sound Taxonomy (BST) Categories

Freesound categorizes all sounds using BST. For therapeutic sleep sounds:

**Primary Categories:**

- `Soundscapes` → `Nature` (forest, ocean, rain soundscapes)
- `Sound effects` → `Natural elements` (isolated rain, wind, water)
- `Sound effects` → `Electronic / Design` (synthesized ambient, white noise)
- `Music` → `Solo instrument` (simple, calming melodies)

**Search Implementation:**

```python
# Category + Subcategory filtering
category="Soundscapes"
subcategory="Nature"
```

### 3. Advanced AudioCommons Descriptors

AudioCommons provides perceptual audio descriptors perfect for therapeutic filtering:

**Key Descriptors for Sleep Sounds:**

| Descriptor | Range | Therapeutic Target | Usage |
|------------|-------|-------------------|-------|
| `ac_brightness` | 0-100 | 0-30 (dark, warm) | Avoid bright, harsh sounds |
| `ac_warmth` | 0-100 | 60-100 (warm) | Promote relaxation |
| `ac_hardness` | 0-100 | 0-30 (soft) | Exclude percussive/hard sounds |
| `ac_roughness` | 0-100 | 0-20 (smooth) | Avoid textured/rough sounds |
| `ac_sharpness` | 0-100 | 0-20 (dull) | Exclude cutting/sharp sounds |
| `ac_single_event` | boolean | false | Prefer continuous sounds |
| `ac_tempo` | BPM | 60-80 | Slow, relaxing tempo |
| `ac_loudness` | LUFS | -30 to -10 | Moderate loudness |

**Example Filter:**

```python
descriptors_filter = "ac_brightness:[0 TO 30] AND ac_warmth:[60 TO 100] AND ac_hardness:[0 TO 30] AND ac_single_event:false"
```

## 🎯 Optimized Search Strategies

### 1. Nature Soundscapes (Premium Strategy)

**Query Structure:**

```python
{
    "query": "+nature +ambience +calm -thunder -storm -wind",
    "category": "Soundscapes",
    "subcategory": "Nature",
    "filter_tags": ["ambient", "peaceful", "calm", "nature", "-loud", "-harsh", "-sudden"],
    "descriptors_filter": "ac_brightness:[0 TO 25] AND ac_warmth:[70 TO 100] AND ac_hardness:[0 TO 20] AND ac_single_event:false",
    "duration_range": (60, 1800),  # 1-30 minutes
    "rating_min": 3.5,
    "sort": "rating_desc"
}
```

### 2. Rain Sounds (Multi-Layered Strategy)

**Light Rain:**

```python
{
    "query": "+rain +gentle +soft -thunder -storm",
    "category": "Sound effects",
    "subcategory": "Natural elements",
    "filter_tags": ["rain", "gentle", "soft", "peaceful", "-thunder", "-storm", "-wind"],
    "descriptors_filter": "ac_brightness:[0 TO 20] AND ac_roughness:[0 TO 15] AND ac_hardness:[0 TO 25]",
    "duration_range": (30, 300)
}
```

**Steady Rain:**

```python
{
    "query": "\"rain loop\" +steady +ambient -storm",
    "category": "Soundscapes",
    "subcategory": "Nature",
    "descriptors_filter": "ac_brightness:[0 TO 30] AND ac_warmth:[60 TO 100] AND ac_single_event:false"
}
```

**Rain on Surfaces:**

```python
{
    "query": "+rain +roof -thunder",
    "alternative_queries": [
        "+rain +metal -storm",
        "+rain +leaves -wind",
        "+rain +window -thunder"
    ]
}
```

### 3. Ocean & Water Sounds

**Calm Ocean:**

```python
{
    "query": "+ocean +waves +calm -storm -surf",
    "category": "Soundscapes", 
    "subcategory": "Nature",
    "descriptors_filter": "ac_warmth:[70 TO 100] AND ac_hardness:[0 TO 20] AND ac_brightness:[0 TO 30]",
    "filter_tags": ["waves", "ocean", "calm", "peaceful", "-storm", "-wind", "-surf"]
}
```

**Gentle Water:**

```python
{
    "query": "+water +flowing +gentle -splash",
    "category": "Sound effects",
    "subcategory": "Natural elements",
    "descriptors_filter": "ac_roughness:[0 TO 15] AND ac_single_event:false"
}
```

### 4. White & Pink Noise

**White Noise:**

```python
{
    "query": "\"white noise\" +constant +sleep",
    "category": "Sound effects",
    "subcategory": "Electronic / Design",
    "descriptors_filter": "ac_single_event:false AND ac_brightness:[40 TO 80]",
    "filter_tags": ["white-noise", "constant", "sleep", "-music", "-voice"]
}
```

**Pink Noise (Research-Optimized):**

```python
{
    "query": "\"pink noise\" +memory +sleep",
    "descriptors_filter": "ac_single_event:false AND ac_brightness:[20 TO 60]",
    "filter_tags": ["pink-noise", "memory", "sleep", "steady"]
}
```

### 5. Binaural Beat Sources

**Base Tones:**

```python
{
    "query": "+tone +sine +frequency -music",
    "category": "Instrument samples",
    "subcategory": "Synths / Electronic",
    "descriptors_filter": "ac_single_event:false AND tonal.key_strength:[0.7 TO 1.0]",
    "filter_tags": ["tone", "sine", "frequency", "-chord", "-harmony"]
}
```

## 🔧 Advanced Filtering Techniques

### 1. Duration Optimization

Different sound types need different durations:

```python
duration_strategies = {
    "ambient_soundscapes": (300, 3600),    # 5-60 minutes
    "rain_loops": (30, 600),               # 30 seconds - 10 minutes  
    "nature_ambience": (120, 1800),        # 2-30 minutes
    "white_noise": (60, 1800),             # 1-30 minutes
    "binaural_sources": (10, 300),         # 10 seconds - 5 minutes
    "thunder_effects": (2, 30)             # 2-30 seconds
}
```

### 2. License Strategy

For therapeutic applications, prioritize flexible licenses:

```python
license_priority = [
    "Creative Commons 0",      # Public domain (best)
    "Attribution",             # Free with attribution
    "Attribution NonCommercial" # Non-commercial only
]
```

### 3. Quality Filters

```python
quality_filters = {
    "rating_min": 3.5,        # High user ratings
    "downloads_min": 50,      # Proven popularity
    "samplerate": 44100,      # Standard quality
    "channels": 2,            # Stereo preferred
    "bitdepth": [16, 24]      # High quality encoding
}
```

## 🎵 Content-Based Search Strategies

### Using Similar Sounds

Find sounds similar to known good examples:

```python
# Find sounds similar to a known good rain sound
target_sound_id = 123456
similar_sounds = freesound_api.search_similar(target_sound_id)
```

### AudioCommons Descriptor Filtering

```python
# Complex descriptor combinations
advanced_descriptors = [
    # Warm, soft nature sounds
    "ac_warmth:[70 TO 100] AND ac_hardness:[0 TO 25] AND ac_brightness:[0 TO 30]",
    
    # Smooth, continuous ambient
    "ac_roughness:[0 TO 15] AND ac_single_event:false AND ac_sharpness:[0 TO 20]",
    
    # Sleep-optimized dynamics
    "ac_dynamic_range:[5 TO 20] AND ac_loudness:[-25 TO -10]"
]
```

## 🔍 Tag Strategy Optimization

### Positive Tags (Include)

```python
therapeutic_tags = [
    # Primary descriptors
    "ambient", "calm", "peaceful", "relaxing", "soothing",
    
    # Sleep-specific
    "sleep", "meditation", "therapy", "healing",
    
    # Nature categories  
    "nature", "forest", "ocean", "rain", "water",
    
    # Audio characteristics
    "loop", "seamless", "continuous", "gentle", "soft"
]
```

### Negative Tags (Exclude)

```python
avoid_tags = [
    # Disruptive elements
    "loud", "harsh", "sudden", "sharp", "aggressive",
    
    # Weather disturbances  
    "thunder", "storm", "lightning", "windy", "gusty",
    
    # Musical elements
    "beat", "rhythm", "drums", "percussion", "melody",
    
    # Human elements
    "voice", "speech", "talking", "singing", "crowd"
]
```

## 📊 Search Result Optimization

### Multi-Query Strategy

Instead of single searches, use multiple targeted queries:

```python
def comprehensive_search(category_type):
    queries = {
        "rain": [
            "+rain +gentle -thunder -storm",
            "\"light rain\" +peaceful +ambient", 
            "+drizzle +calm +nature",
            "+rain +forest -wind",
            "+rain +roof +metal"
        ],
        "nature": [
            "+forest +ambience +peaceful",
            "+nature +calm +ambient -birds",
            "+woodland +atmosphere +quiet",
            "+trees +wind +gentle"
        ]
    }
    
    all_results = []
    for query in queries[category_type]:
        results = search_with_query(query)
        all_results.extend(results)
    
    return deduplicate_and_rank(all_results)
```

### Intelligent Result Ranking

```python
def rank_therapeutic_sounds(sounds):
    for sound in sounds:
        score = 0
        
        # Duration scoring (prefer moderate lengths)
        duration = sound.get('duration', 0)
        if 30 <= duration <= 600:
            score += 10
        elif 10 <= duration <= 30 or 600 <= duration <= 1800:
            score += 5
            
        # Rating scoring
        rating = sound.get('avg_rating', 0)
        score += rating * 2
        
        # Download popularity
        downloads = sound.get('num_downloads', 0)
        if downloads > 100:
            score += 5
        elif downloads > 50:
            score += 3
            
        # Tag analysis
        tags = sound.get('tags', [])
        good_tags = ['ambient', 'calm', 'peaceful', 'nature', 'sleep']
        bad_tags = ['loud', 'harsh', 'sudden', 'thunder', 'storm']
        
        score += len([t for t in tags if t in good_tags]) * 2
        score -= len([t for t in tags if t in bad_tags]) * 5
        
        sound['therapeutic_score'] = score
    
    return sorted(sounds, key=lambda x: x['therapeutic_score'], reverse=True)
```

## 🎯 Implementation Strategy

### 1. Layered Search Approach

```python
class OptimizedFreesoundSearch:
    def search_therapeutic_content(self, category):
        # Layer 1: Primary search with strict filters
        primary_results = self.search_with_strict_filters(category)
        
        # Layer 2: Broader search if not enough results
        if len(primary_results) < 10:
            secondary_results = self.search_with_relaxed_filters(category)
            primary_results.extend(secondary_results)
        
        # Layer 3: Similar sound expansion
        expanded_results = self.expand_with_similar_sounds(primary_results)
        
        # Layer 4: Quality filtering and ranking
        return self.filter_and_rank_results(expanded_results)
```

### 2. Caching and Efficiency

```python
# Cache successful searches
search_cache = {}

def cached_search(query_hash, search_function):
    if query_hash in search_cache:
        return search_cache[query_hash]
    
    results = search_function()
    search_cache[query_hash] = results
    return results
```

## 🧪 Testing and Validation

### Search Quality Metrics

```python
def evaluate_search_quality(results):
    metrics = {
        'total_results': len(results),
        'avg_rating': np.mean([r.get('avg_rating', 0) for r in results]),
        'suitable_duration': len([r for r in results if 30 <= r.get('duration', 0) <= 600]),
        'therapeutic_tags': len([r for r in results if any(tag in r.get('tags', []) for tag in ['calm', 'peaceful', 'ambient'])]),
        'avoid_tags': len([r for r in results if any(tag in r.get('tags', []) for tag in ['loud', 'harsh', 'sudden'])])
    }
    
    quality_score = (
        (metrics['avg_rating'] / 5.0) * 0.3 +
        (metrics['suitable_duration'] / metrics['total_results']) * 0.3 +
        (metrics['therapeutic_tags'] / metrics['total_results']) * 0.2 +
        (1 - metrics['avoid_tags'] / metrics['total_results']) * 0.2
    )
    
    return quality_score, metrics
```

## 🎵 Best Practices Summary

1. **Use Multiple Query Strategies** - Combine different search approaches
2. **Leverage BST Categories** - Proper categorization improves relevance
3. **Apply AudioCommons Filters** - Use perceptual descriptors for quality
4. **Implement Negative Filtering** - Exclude disruptive elements
5. **Duration Optimization** - Target appropriate lengths for use case
6. **Quality Scoring** - Rank results by therapeutic suitability
7. **Cache Results** - Improve performance and reduce API calls
8. **Test and Iterate** - Continuously improve search strategies

## 🔧 Code Implementation

See the updated `FreesoundAPI` class and `ContentGatherer` for implementation of these strategies. The key improvements include:

- Advanced query syntax usage
- Proper BST category filtering  
- AudioCommons descriptor optimization
- Multi-layered search approach
- Intelligent result ranking
- Comprehensive tag strategies

This guide provides the foundation for acquiring high-quality, therapeutically relevant audio content that will enhance the effectiveness of the SonicSleep Pro application.
