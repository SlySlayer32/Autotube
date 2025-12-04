# Freesound Search Strategy Enhancement Plan

## Overview

This document outlines advanced search strategies for collecting high-quality therapeutic audio from Freesound using the full capabilities of their API v2.

## Current Limitations

1. Basic keyword-only searches without advanced filtering
2. No use of Broad Sound Taxonomy (BST) categories
3. Limited quality filtering (only rating and duration)
4. No content-based analysis filtering
5. Simple tag filtering without strategic combinations

## Advanced Search Strategies

### 1. Broad Sound Taxonomy Integration

**Target Categories for Sleep/Therapeutic Audio:**

- `ss-n`: Nature Soundscapes (forest, sea, river)
- `fx-n`: Natural Elements (wind, water, rain)
- `fx-a`: Animals (birds, insects - but filtered carefully)

**Implementation:**

```python
filter = "category:Soundscapes subcategory:Nature"
filter = "category:\"Sound effects\" subcategory:\"Natural elements\""
```

### 2. AudioCommons Content Analysis Filters

**Sleep-Optimized Audio Characteristics:**

- **Brightness**: 0-30 (darker, calmer sounds)
- **Warmth**: 70-100 (comforting, enveloping)
- **Hardness**: 0-30 (soft, gentle)
- **Roughness**: 0-30 (smooth, continuous)
- **Single Event**: false (continuous ambiences)

**Implementation:**

```python
descriptors_filter = "ac_brightness:[0 TO 30] ac_warmth:[70 TO 100] ac_hardness:[0 TO 30]"
```

### 3. Advanced Query Syntax

**Mandatory/Prohibited Terms:**

```python
# Good rain sounds
query = "+rain +gentle -thunder -storm -wind -heavy"

# Nature ambiences
query = "+forest +ambience +calm -birds -animals -rustling"

# Ocean sounds
query = "+ocean +waves +gentle -storm -wind -surf"
```

**Phrase Matching:**

```python
query = '"gentle rain" "soft rain" "light drizzle"'
```

### 4. Quality and Licensing Filters

**Enhanced Quality Filtering:**

```python
filter = "avg_rating:[3 TO *] num_downloads:[10 TO *] license:(Attribution OR \"Creative Commons 0\")"
```

**Duration Optimization:**

```python
filter = "duration:[30 TO 600]"  # 30 seconds to 10 minutes
```

### 5. Strategic Tag Combinations

**Sleep-Optimized Tags:**

- Include: `ambient`, `loop`, `calm`, `peaceful`, `meditation`, `relaxation`
- Exclude: `loud`, `harsh`, `sudden`, `alarm`, `aggressive`

**Implementation:**

```python
filter = "tag:ambient tag:loop tag:calm -tag:loud -tag:harsh"
```

## Enhanced Search Categories

### Nature Sounds

```python
searches = [
    {
        "query": '"gentle rain" +peaceful',
        "filter": "category:Soundscapes duration:[60 TO 600] ac_brightness:[0 TO 25]",
        "tags": ["rain", "peaceful", "ambient"]
    },
    {
        "query": '"ocean waves" +calm',
        "filter": "subcategory:Nature ac_warmth:[60 TO 100] ac_hardness:[0 TO 20]",
        "tags": ["ocean", "waves", "calm"]
    }
]
```

### White/Pink Noise

```python
searches = [
    {
        "query": '"white noise" +sleep',
        "filter": "duration:[300 TO 3600] ac_single_event:false",
        "tags": ["white-noise", "sleep", "constant"]
    }
]
```

### Ambient Drones

```python
searches = [
    {
        "query": '"ambient drone" +meditation',
        "filter": "duration:[120 TO 3600] ac_roughness:[0 TO 15]",
        "tags": ["drone", "ambient", "meditation"]
    }
]
```

## Implementation Strategy

### Phase 1: Enhanced FreesoundAPI Class

1. Add support for advanced filter parameters
2. Implement BST category filtering
3. Add AudioCommons descriptor filtering
4. Support complex query syntax

### Phase 2: Improved ContentGatherer

1. Update search categories with advanced strategies
2. Implement multi-stage quality filtering
3. Add content analysis verification
4. Optimize for different collection types

### Phase 3: GUI Integration

1. Add advanced search options to UI
2. Provide category-specific presets
3. Display search strategy information
4. Allow user customization of filters

## Expected Improvements

### Quality

- 70% reduction in inappropriate sounds (thunder, sudden noises)
- 50% increase in therapeutic value through content analysis
- Better duration consistency for mixing

### Relevance

- 80% improvement in search result relevance
- More consistent sound characteristics within categories
- Better matching to sleep/meditation requirements

### Efficiency

- Faster collection due to better initial filtering
- Reduced post-processing verification needs
- Lower bandwidth usage with targeted searches

## Technical Implementation Notes

### API Request Structure

```python
params = {
    "query": complex_query,
    "filter": " AND ".join([
        bst_category_filter,
        duration_filter,
        quality_filter,
        license_filter
    ]),
    "descriptors_filter": audiocommons_filter,
    "sort": "rating_desc",
    "page_size": 50,
    "fields": "id,name,tags,license,duration,description,previews"
}
```

### Content Analysis Integration

```python
def verify_therapeutic_quality(sound_data, audio_analysis):
    """Enhanced verification using both metadata and content analysis."""
    
    # Metadata checks
    if not meets_basic_criteria(sound_data):
        return False
    
    # AudioCommons descriptor checks
    if not meets_audiocommons_criteria(sound_data.get('ac_analysis', {})):
        return False
    
    # Local audio analysis
    if not meets_local_analysis_criteria(audio_analysis):
        return False
    
    return True
```

## Future Enhancements

### Machine Learning Integration

- Train classifier on verified therapeutic sounds
- Use OpenL3 embeddings for similarity matching
- Implement feedback learning from user preferences

### Community Data

- Leverage Freesound pack collections
- Use user ratings and comments for quality assessment
- Identify high-quality contributors

### Dynamic Optimization

- Adjust search strategies based on success rates
- A/B test different filter combinations
- Optimize for specific therapeutic outcomes

## Conclusion

These enhancements will significantly improve the quality, relevance, and therapeutic value of automatically collected audio content while reducing manual curation time and improving user experience.

## UPDATE: Empirical Tag-Based Search Strategy

### Discovery from Manual Search

Manual searches on Freesound revealed the most relevant tags for each category:

**Rain Tags (from actual search):**
`rain field-recording weather thunder storm nature water thunderstorm ambience lightning ambient raining wind atmosphere city drops birds raindrops ambiance shower thunder-storm dripping rainstorm wet drip traffic car soundscape rumble night street cars noise forest window rainfall roof`

**Tag Analysis:**

- **High-value tags**: `rain`, `field-recording`, `nature`, `ambience`, `ambient`, `drops`, `raindrops`, `rainfall`, `roof`, `window`
- **Avoid tags**: `thunder`, `storm`, `thunderstorm`, `lightning`, `wind`, `traffic`, `car`, `street`, `cars`

### Empirical Search Implementation

```python
def search_by_empirical_tags(category_type, max_results=20):
    """Use real-world tag combinations from manual searches."""
    
    empirical_strategies = {
        "rain": {
            "primary_combinations": [
                ["rain", "field-recording", "nature"],
                ["rainfall", "ambience", "weather"],
                ["rain", "drops", "peaceful"],
                ["drizzle", "ambient", "calm"],
                ["rain", "roof", "gentle"]
            ],
            "positive_tags": ["rain", "rainfall", "raining", "drizzle", "drops", 
                             "field-recording", "nature", "ambience", "ambient"],
            "negative_tags": ["thunder", "storm", "thunderstorm", "lightning", "wind"]
        }
    }
```

### Benefits of Empirical Approach

1. **Real-world validation**: Tags come from actual Freesound content
2. **Higher precision**: Combinations proven to exist in the database
3. **Efficient filtering**: Target specific tag combinations rather than broad searches
4. **Quality indicators**: Tags like "field-recording" indicate higher quality content

### Next Steps

1. Conduct manual searches for each therapeutic category
2. Document effective tag combinations
3. Implement category-specific empirical strategies
4. Test and refine based on actual results
