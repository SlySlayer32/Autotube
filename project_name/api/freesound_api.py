import logging
from typing import Optional, List, Dict, Union

import requests

logger = logging.getLogger(__name__)


class FreesoundAPI:
    def __init__(self, api_key: str):
        """
        Initialize the Freesound API client.

        Args:
            api_key: The Freesound API key
        """
        self.api_key = api_key
        logger.info("Freesound API client initialized.")

    def search(
        self,
        query: str,
        filter_tags: list = None,
        sort: str = "score",
        page: int = 1,
        page_size: int = 15,
        filters: Optional[Dict[str, str]] = None,
        descriptors_filter: Optional[str] = None,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        license_filter: Optional[str] = None,
        duration_range: Optional[tuple] = None,
        rating_min: Optional[float] = None,
        downloads_min: Optional[int] = None,
    ) -> dict:
        """
        Search for sounds on Freesound using advanced API capabilities.

        Args:
            query: Search query string (supports +term -term "phrase" syntax)
            filter_tags: Optional list of tags to filter results
            sort: Sort order ('score', 'duration_desc', 'rating_desc', 'downloads_desc', etc.)
            page: Page number for results
            page_size: Results per page (max 150)
            filters: Dictionary of additional filters
            descriptors_filter: AudioCommons descriptors filter string
            category: Broad Sound Taxonomy category (e.g., "Soundscapes")
            subcategory: BST subcategory (e.g., "Nature")
            license_filter: License type filter ("Attribution", "Creative Commons 0", etc.)
            duration_range: Tuple of (min_seconds, max_seconds)
            rating_min: Minimum average rating (0-5)
            downloads_min: Minimum number of downloads

        Returns:
            Dictionary containing search results
        """
        logger.info(f"Advanced Freesound search: {query}")

        endpoint = "https://freesound.org/apiv2/search/text/"
        params = {
            "query": query,
            "page": page,
            "page_size": min(page_size, 150),
            "sort": sort,
            "fields": "id,name,tags,username,license,previews,duration,description,avg_rating,num_downloads,ac_analysis",
            "token": self.api_key,
        }

        # Build advanced filter string
        filter_parts = []
        
        # Broad Sound Taxonomy filters
        if category:
            filter_parts.append(f'category:"{category}"')
        if subcategory:
            filter_parts.append(f'subcategory:"{subcategory}"')
            
        # License filter
        if license_filter:
            if license_filter.lower() in ["attribution", "creative commons 0", "attribution noncommercial"]:
                filter_parts.append(f'license:"{license_filter}"')
        
        # Duration filter
        if duration_range:
            min_dur, max_dur = duration_range
            filter_parts.append(f"duration:[{min_dur} TO {max_dur}]")
            
        # Quality filters
        if rating_min:
            filter_parts.append(f"avg_rating:[{rating_min} TO *]")
        if downloads_min:
            filter_parts.append(f"num_downloads:[{downloads_min} TO *]")
            
        # Tag filters
        if filter_tags:
            for tag in filter_tags:
                if tag.startswith('-'):
                    filter_parts.append(f"-tag:{tag[1:]}")
                else:
                    filter_parts.append(f"tag:{tag}")
        
        # Additional custom filters
        if filters:
            for key, value in filters.items():
                filter_parts.append(f"{key}:{value}")
        
        # Combine all filters
        if filter_parts:
            params["filter"] = " ".join(filter_parts)
              # AudioCommons descriptors filter
        if descriptors_filter:
            params["descriptors_filter"] = descriptors_filter

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            result = response.json()
            logger.info(f"Search returned {result.get('count', 0)} total results")
            return result
        except Exception as e:
            logger.error(f"Error searching Freesound: {str(e)}")
            return {}

    def search_therapeutic_sounds(
        self,
        category_type: str = "nature",
        max_results: int = 20,
        duration_range: tuple = (30, 600),
        include_tags: List[str] = None,
        exclude_tags: List[str] = None,
    ) -> dict:
        """
        Search for therapeutic sounds using research-optimized strategies.
        
        This method implements advanced search techniques based on comprehensive
        Freesound API research and therapeutic audio requirements.
        
        Args:
            category_type: Type of therapeutic sounds ("nature", "rain", "ocean", "ambient", "white_noise", "binaural")
            max_results: Maximum number of results to return
            duration_range: Tuple of (min_seconds, max_seconds)
            include_tags: Tags that must be present
            exclude_tags: Tags to exclude
            
        Returns:
            Dictionary containing search results optimized for therapeutic use
        """        # Research-optimized therapeutic sound search strategies based on real Freesound tags
        strategies = {
            "nature": {
                "primary_tags": ["nature", "ambience", "forest", "atmosphere", "ambient"],
                "good_tags": ["peaceful", "calm", "relaxing", "quiet", "soundscape"],
                "avoid_tags": ["birds", "animals", "rustling", "wind", "loud"],
                "queries": [
                    '+nature +ambience +calm -birds -wind',
                    '+forest +atmosphere +peaceful -animals',
                    '+woodland +ambient +quiet -rustling'
                ],
                "category": "Soundscapes",
                "subcategory": "Nature",
                "descriptors": "ac_brightness:[0 TO 25] AND ac_warmth:[70 TO 100] AND ac_hardness:[0 TO 20] AND ac_single_event:false"
            },
            "rain": {
                "primary_tags": ["rain", "raining", "rainfall", "drizzle"],
                "good_tags": ["field-recording", "weather", "nature", "ambience", "ambient", "drops", "raindrops", "dripping", "roof", "window"],
                "avoid_tags": ["thunder", "storm", "thunderstorm", "lightning", "thunder-storm", "rainstorm", "wind"],
                "queries": [
                    '+rain +field-recording -thunder -storm',
                    '+rainfall +nature +ambient -wind',
                    '+rain +drops +peaceful -lightning',
                    '+drizzle +calm +ambience',
                    '+rain +roof +gentle -storm'
                ],
                "category": "Sound effects", 
                "subcategory": "Natural elements",
                "descriptors": "ac_brightness:[0 TO 20] AND ac_roughness:[0 TO 15] AND ac_hardness:[0 TO 25]"
            },
            "ocean": {
                "primary_tags": ["ocean", "sea", "waves", "water", "beach"],
                "good_tags": ["ambience", "ambient", "nature", "soundscape", "peaceful", "calm"],
                "avoid_tags": ["storm", "wind", "surf", "rough", "thunder"],
                "queries": [
                    '+ocean +waves +calm -storm',
                    '+sea +ambience +peaceful -wind',
                    '+beach +water +gentle -surf',
                    '+waves +nature +ambient'
                ],
                "category": "Soundscapes",
                "subcategory": "Nature", 
                "descriptors": "ac_warmth:[70 TO 100] AND ac_hardness:[0 TO 20] AND ac_brightness:[0 TO 30]"
            },
            "ambient": {
                "primary_tags": ["ambient", "ambience", "atmosphere", "drone"],
                "good_tags": ["meditation", "relaxation", "peaceful", "calm", "sleep"],
                "avoid_tags": ["music", "electronic", "beat", "rhythm", "melody", "synth"],
                "queries": [
                    '+ambient +meditation +calm -music',
                    '+atmosphere +relaxation +peaceful',
                    '+drone +ambient +sleep -electronic',
                    '+ambience +calm +peaceful -beat'
                ],
                "category": "Soundscapes",
                "subcategory": "Synthetic / Artificial",
                "descriptors": "ac_single_event:false AND ac_roughness:[0 TO 15] AND ac_sharpness:[0 TO 20]"
            },
            "white_noise": {
                "primary_tags": ["white-noise", "pink-noise", "noise"],
                "good_tags": ["sleep", "constant", "ambient", "steady"],
                "avoid_tags": ["music", "voice", "sudden", "harsh", "electronic"],
                "queries": [
                    '+"white-noise" +sleep +constant',
                    '+"pink-noise" +ambient +steady',
                    '+noise +constant +sleep -music',
                    '+noise +ambient +calm -harsh'
                ],
                "category": "Sound effects",
                "subcategory": "Electronic / Design",
                "descriptors": "ac_single_event:false AND ac_brightness:[40 TO 80]"
            },
            "binaural": {
                "primary_tags": ["binaural", "tone", "frequency", "sine"],
                "good_tags": ["meditation", "healing", "therapy", "pure"],
                "avoid_tags": ["music", "song", "melody", "rhythm"],
                "queries": [
                    '+binaural +meditation +tone',
                    '+frequency +pure +sine -music',
                    '+tone +healing +therapy',
                    '+binaural +calm +meditation'
                ],
                "category": "Instrument samples",
                "subcategory": "Synths / Electronic",
                "tags": ["tone", "sine", "frequency", "binaural", "pure"],
                "exclude": ["chord", "harmony", "music", "melody"],
                "descriptors": "ac_single_event:false AND tonal.key_strength:[0.7 TO 1.0]"
            }
        }
        
        strategy = strategies.get(category_type, strategies["nature"])
        
        # Use multi-query approach for better results
        all_results = []
        queries = strategy.get("queries", [strategy.get("query", "")])
        
        for query in queries:
            if not query:
                continue
                
            # Build filter tags for this query
            filter_tags = []
            if include_tags:
                filter_tags.extend(include_tags)
            if strategy.get("tags"):
                filter_tags.extend(strategy["tags"])
            if exclude_tags:
                filter_tags.extend([f"-{tag}" for tag in exclude_tags])
            if strategy.get("exclude"):
                filter_tags.extend([f"-{tag}" for tag in strategy["exclude"]])
                
            # Execute search with enhanced parameters
            search_results = self.search(
                query=query,
                filter_tags=filter_tags,
                sort="rating_desc",
                page_size=min(max_results // len(queries) + 5, 50),  # Distribute across queries
                category=strategy.get("category"),
                subcategory=strategy.get("subcategory"),
                duration_range=duration_range,
                rating_min=3.5,  # Higher quality threshold
                downloads_min=20,  # Proven popularity
                descriptors_filter=strategy.get("descriptors"),
                license_filter="Attribution"
            )
            
            if 'results' in search_results:
                all_results.extend(search_results['results'])
        
        # Deduplicate and rank results
        unique_results = {}
        for result in all_results:
            sound_id = result.get('id')
            if sound_id not in unique_results:
                unique_results[sound_id] = result
        
        # Convert back to list and limit results
        final_results = list(unique_results.values())[:max_results]
          # Return in standard format
        return {
            'count': len(final_results),
            'results': final_results
        }

    def download(self, sound_id: int) -> str:
        """
        Download a sound from Freesound by ID.

        Args:
            sound_id: Freesound sound ID

        Returns:
            Path to downloaded file or error message
        """
        logger.info(f"Downloading sound ID: {sound_id}")

        endpoint = f"https://freesound.org/apiv2/sounds/{sound_id}/"
        try:
            response = requests.get(endpoint, params={"token": self.api_key})
            response.raise_for_status()
            data = response.json()

            download_url = data.get("download")
            if not download_url:
                logger.error("Download URL not found in response.")
                return ""

            response = requests.get(
                download_url, params={"token": self.api_key}, stream=True
            )
            response.raise_for_status()

            file_name = f"{sound_id}.wav"
            with open(file_name, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)

            logger.info(f"Downloaded sound to {file_name}")
            return file_name
        except Exception as e:
            logger.error(f"Error downloading sound: {str(e)}")
            return ""

    def get_popular_tags(self, query: str = None) -> list:
        """
        Get popular tags from Freesound, optionally filtered by query.

        Args:
            query: Optional query to filter tags by relevance

        Returns:
            List of popular tags
        """
        logger.info("Fetching popular Freesound tags")

        endpoint = "https://freesound.org/apiv2/search/text/"
        params = {"query": query or "", "fields": "tags", "token": self.api_key}

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("tags", [])
        except Exception as e:
            logger.error(f"Error fetching tags: {str(e)}")
            return []

    def get_sound_analysis(self, sound_id: int) -> dict:
        """
        Get detailed analysis data for a sound.
        
        Args:
            sound_id: Freesound sound ID
            
        Returns:
            Dictionary containing analysis data
        """
        endpoint = f"https://freesound.org/apiv2/sounds/{sound_id}/analysis/"
        params = {"token": self.api_key}
        
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error getting analysis for sound {sound_id}: {str(e)}")
            return {}

    def search_by_empirical_tags(
        self,
        category_type: str = "rain",
        max_results: int = 20,
        duration_range: tuple = (30, 600),
        quality_filter: bool = True
    ) -> dict:
        """
        Search using empirical tags discovered from manual Freesound searches.
        
        This method uses real-world tag combinations found in actual Freesound content
        for each therapeutic category.
        
        Args:
            category_type: Type of sounds ("rain", "ocean", "nature", "ambient", "white_noise")
            max_results: Maximum number of results
            duration_range: Tuple of (min_seconds, max_seconds)
            quality_filter: Whether to apply quality filters
            
        Returns:
            Dictionary containing search results
        """
        # Empirical tag combinations from actual Freesound searches
        empirical_strategies = {
            "rain": {
                "primary_combinations": [
                    ["rain", "field-recording", "nature"],
                    ["rainfall", "ambience", "weather"],
                    ["rain", "drops", "peaceful"],
                    ["drizzle", "ambient", "calm"],
                    ["rain", "roof", "gentle"]
                ],
                "positive_tags": ["rain", "rainfall", "raining", "drizzle", "drops", "raindrops", 
                                 "field-recording", "nature", "ambience", "ambient", "peaceful", "calm"],
                "negative_tags": ["thunder", "storm", "thunderstorm", "lightning", "wind", "heavy"],
                "duration_sweet_spot": (60, 300)
            },
            "ocean": {
                "primary_combinations": [
                    ["ocean", "waves", "nature"],
                    ["sea", "ambience", "peaceful"],
                    ["waves", "water", "calm"],
                    ["beach", "ambient", "gentle"]
                ],
                "positive_tags": ["ocean", "sea", "waves", "water", "beach", "ambience", 
                                 "ambient", "nature", "peaceful", "calm", "gentle"],
                "negative_tags": ["storm", "wind", "surf", "rough", "heavy"],
                "duration_sweet_spot": (90, 600)
            },
            "nature": {
                "primary_combinations": [
                    ["nature", "forest", "ambience"],
                    ["forest", "atmosphere", "peaceful"],
                    ["nature", "ambient", "calm"],
                    ["soundscape", "nature", "quiet"]
                ],
                "positive_tags": ["nature", "forest", "ambience", "ambient", "atmosphere", 
                                 "peaceful", "calm", "quiet", "soundscape"],
                "negative_tags": ["birds", "animals", "wind", "rustling", "loud"],
                "duration_sweet_spot": (120, 600)
            },
            "ambient": {
                "primary_combinations": [
                    ["ambient", "meditation", "calm"],
                    ["atmosphere", "peaceful", "relaxation"],
                    ["ambience", "sleep", "gentle"],
                    ["ambient", "drone", "meditation"]
                ],
                "positive_tags": ["ambient", "ambience", "atmosphere", "meditation", "relaxation",
                                 "peaceful", "calm", "sleep", "drone"],
                "negative_tags": ["music", "electronic", "beat", "rhythm", "melody"],
                "duration_sweet_spot": (180, 1200)
            },
            "white_noise": {
                "primary_combinations": [
                    ["white-noise", "sleep", "constant"],
                    ["pink-noise", "ambient", "steady"],
                    ["noise", "constant", "calm"]
                ],
                "positive_tags": ["white-noise", "pink-noise", "noise", "sleep", "constant", 
                                 "ambient", "steady", "calm"],
                "negative_tags": ["music", "voice", "sudden", "harsh"],
                "duration_sweet_spot": (300, 3600)
            }
        }
        
        if category_type not in empirical_strategies:
            logger.warning(f"Unknown category: {category_type}")
            return {"count": 0, "results": []}
            
        strategy = empirical_strategies[category_type]
        all_results = []
        
        # Try each primary tag combination
        for tag_combo in strategy["primary_combinations"]:
            # Build tag-based filter
            tag_filters = []
            for tag in tag_combo:
                tag_filters.append(f"tag:{tag}")
            for neg_tag in strategy["negative_tags"][:3]:  # Limit negative tags
                tag_filters.append(f"-tag:{neg_tag}")
                
            # Add duration filter
            min_dur, max_dur = duration_range
            if strategy["duration_sweet_spot"]:
                sweet_min, sweet_max = strategy["duration_sweet_spot"]
                min_dur = max(min_dur, sweet_min)
                max_dur = min(max_dur, sweet_max)
                
            tag_filters.append(f"duration:[{min_dur} TO {max_dur}]")
            
            # Add quality filters if requested
            if quality_filter:
                tag_filters.extend([
                    "avg_rating:[3 TO *]",
                    "num_downloads:[5 TO *]"
                ])
                
            filter_string = " AND ".join(tag_filters)
            
            try:
                # Use basic search with tag-based filters
                result = self.search(
                    query="*",  # Match all, rely on filters
                    filters={"filter": filter_string},
                    sort="rating_desc",
                    page_size=min(15, max_results),
                )
                
                if result.get("results"):
                    all_results.extend(result["results"])
                    logger.info(f"Found {len(result['results'])} results for {tag_combo}")
                    
            except Exception as e:
                logger.error(f"Search failed for {tag_combo}: {e}")
                continue
                
        # Remove duplicates and limit results
        unique_results = {}
        for result in all_results:
            sound_id = result.get("id")
            if sound_id and sound_id not in unique_results:
                unique_results[sound_id] = result
                
        final_results = list(unique_results.values())[:max_results]
        
        logger.info(f"Empirical tag search for '{category_type}': {len(final_results)} unique results")
        
        return {
            'count': len(final_results),
            'results': final_results
        }
    
    def search_by_tags_and_filename(
        self,
        category_type: str = "rain",
        max_results: int = 20,
        duration_range: tuple = (30, 600),
        quality_filter: bool = True
    ) -> dict:
        """
        Advanced search using both empirical tags AND filename analysis.
        
        This method analyzes both the tags and filename/description to identify
        truly therapeutic sounds by understanding context clues like:
        - "gentle rain" vs "metal rain" 
        - "rain roof" vs "rain storm"
        - "peaceful ocean" vs "crashing waves"
        
        Args:
            category_type: Type of sounds ("rain", "ocean", "nature", "ambient", "white_noise")
            max_results: Maximum number of results
            duration_range: Tuple of (min_seconds, max_seconds)
            quality_filter: Whether to apply quality filters
            
        Returns:
            Dictionary containing search results with filename/context filtering
        """
        
        # Enhanced search strategies with filename context analysis
        context_strategies = {
            "rain": {
                "positive_filename_words": ["gentle", "soft", "light", "peaceful", "calm", "quiet", 
                                           "roof", "window", "drops", "drizzle", "ambient"],
                "negative_filename_words": ["metal", "storm", "thunder", "heavy", "harsh", "loud", 
                                           "industrial", "concrete", "aggressive", "intense"],
                "core_tags": ["rain", "rainfall", "raining", "drizzle"],
                "supporting_tags": ["field-recording", "nature", "ambience", "ambient", "peaceful"],
                "avoid_tags": ["thunder", "storm", "lightning", "wind", "metal"],
                "search_queries": [
                    # Query structure: main concept + positive context - negative context
                    '+rain +(gentle OR soft OR peaceful OR roof OR window) -storm -thunder -metal',
                    '+rainfall +(ambient OR calm OR quiet) -heavy -harsh -industrial',
                    '+drizzle +(nature OR field-recording) -wind -storm',
                    '+"light rain" +(peaceful OR gentle) -thunder',
                    '+rain +drops +(soft OR calm) -metal -concrete'
                ]
            },
            "ocean": {
                "positive_filename_words": ["gentle", "calm", "peaceful", "soft", "ambient", "beach",
                                           "lapping", "quiet", "serene", "meditation"],
                "negative_filename_words": ["storm", "crashing", "rough", "heavy", "wind", "surf",
                                           "aggressive", "violent", "turbulent"],
                "core_tags": ["ocean", "sea", "waves", "water"],
                "supporting_tags": ["beach", "nature", "ambience", "ambient", "peaceful"],
                "avoid_tags": ["storm", "wind", "surf", "rough", "heavy"],
                "search_queries": [
                    '+ocean +(gentle OR calm OR peaceful OR beach) -storm -wind -surf',
                    '+waves +(soft OR lapping OR quiet) -crashing -rough -heavy',
                    '+sea +(ambient OR serene OR meditation) -storm -turbulent',
                    '+"gentle waves" +(peaceful OR calm) -wind',
                    '+water +(peaceful OR ambient OR nature) -storm -rough'
                ]
            },
            "nature": {
                "positive_filename_words": ["peaceful", "calm", "quiet", "gentle", "soft", "ambient",
                                           "forest", "woodland", "serene", "meditation"],
                "negative_filename_words": ["wind", "storm", "birds", "animals", "rustling", "loud",
                                           "aggressive", "busy", "chaotic"],
                "core_tags": ["nature", "forest", "woodland"],
                "supporting_tags": ["ambience", "ambient", "atmosphere", "peaceful", "calm"],
                "avoid_tags": ["birds", "animals", "wind", "rustling", "storm"],
                "search_queries": [
                    '+nature +(peaceful OR calm OR quiet OR ambient) -birds -animals -wind',
                    '+forest +(gentle OR soft OR serene) -rustling -storm -wind',
                    '+woodland +(ambient OR atmosphere OR meditation) -animals -loud',
                    '+"peaceful forest" +ambient -birds -wind',
                    '+nature +(quiet OR calm) -storm -animals'
                ]
            },
            "ambient": {
                "positive_filename_words": ["meditation", "peaceful", "calm", "gentle", "soft", "drone",
                                           "atmosphere", "sleep", "relaxation", "quiet"],
                "negative_filename_words": ["electronic", "beat", "rhythm", "music", "melody", "synth",
                                           "digital", "processed", "artificial"],
                "core_tags": ["ambient", "ambience", "atmosphere", "drone"],
                "supporting_tags": ["meditation", "relaxation", "peaceful", "calm", "sleep"],
                "avoid_tags": ["music", "electronic", "beat", "rhythm", "melody"],
                "search_queries": [
                    '+ambient +(meditation OR peaceful OR calm) -music -electronic -beat',
                    '+atmosphere +(gentle OR soft OR sleep) -rhythm -melody -synth',
                    '+drone +(ambient OR meditation OR relaxation) -music -digital',
                    '+"peaceful ambient" +calm -electronic -music',
                    '+ambience +(quiet OR gentle OR atmosphere) -beat -rhythm'
                ]
            },
            "white_noise": {
                "positive_filename_words": ["sleep", "constant", "steady", "gentle", "soft", "calm",
                                           "smooth", "continuous", "peaceful"],
                "negative_filename_words": ["harsh", "loud", "aggressive", "sudden", "sharp", "digital",
                                           "processed", "artificial", "electronic"],
                "core_tags": ["white-noise", "pink-noise", "noise"],
                "supporting_tags": ["sleep", "constant", "steady", "ambient", "calm"],
                "avoid_tags": ["music", "voice", "sudden", "harsh", "loud"],
                "search_queries": [
                    '+"white noise" +(sleep OR constant OR gentle) -harsh -loud -sudden',
                    '+"pink noise" +(steady OR calm OR peaceful) -aggressive -sharp',
                    '+noise +(constant OR ambient OR sleep) -music -voice -harsh',
                    '+"gentle noise" +(sleep OR calm) -loud -sudden',
                    '+noise +(steady OR continuous OR peaceful) -harsh -aggressive'
                ]
            }
        }
        
        if category_type not in context_strategies:
            logger.warning(f"Unknown category: {category_type}")
            return {"count": 0, "results": []}
            
        strategy = context_strategies[category_type]
        all_results = []
          # Execute each search query
        for query in strategy["search_queries"]:
            try:
                # Build filter tags for quality filtering
                filter_tags = []
                if quality_filter:
                    # Add negative tag filters to avoid unwanted content
                    for tag in strategy["avoid_tags"][:3]:  # Limit to avoid overly restrictive filters
                        filter_tags.append(f"-{tag}")
                
                result = self.search(
                    query=query,
                    filter_tags=filter_tags,
                    duration_range=duration_range,
                    rating_min=3.0 if quality_filter else None,
                    downloads_min=5 if quality_filter else None,
                    sort="rating_desc",
                    page_size=15,
                )
                
                if result.get("results"):
                    # Filter results by filename analysis
                    filtered_results = self._filter_by_filename_context(
                        result["results"], 
                        strategy["positive_filename_words"],
                        strategy["negative_filename_words"]
                    )
                    all_results.extend(filtered_results)
                    logger.info(f"Query '{query[:50]}...' found {len(filtered_results)} context-filtered results")
                    
            except Exception as e:
                logger.error(f"Search failed for query '{query[:50]}...': {e}")
                continue
                
        # Remove duplicates and rank by relevance
        unique_results = {}
        for result in all_results:
            sound_id = result.get("id")
            if sound_id and sound_id not in unique_results:
                # Add relevance score based on filename analysis
                result["therapeutic_score"] = self._calculate_therapeutic_score(
                    result, 
                    strategy["positive_filename_words"],
                    strategy["negative_filename_words"],
                    strategy["core_tags"]
                )
                unique_results[sound_id] = result
                
        # Sort by therapeutic score (highest first)
        final_results = sorted(
            unique_results.values(), 
            key=lambda x: x.get("therapeutic_score", 0), 
            reverse=True
        )[:max_results]
        
        logger.info(f"Tag + filename search for '{category_type}': {len(final_results)} highly relevant results")
        
        return {
            'count': len(final_results),
            'results': final_results
        }
    
    def _filter_by_filename_context(self, results: List[Dict], positive_words: List[str], negative_words: List[str]) -> List[Dict]:
        """Filter results based on filename and description context analysis."""
        filtered = []
        
        for result in results:
            # Analyze filename and description
            text_to_analyze = (
                result.get("name", "").lower() + " " + 
                result.get("description", "").lower()
            )
            
            # Check for negative context words (these are disqualifying)
            has_negative = any(neg_word in text_to_analyze for neg_word in negative_words)
            if has_negative:
                logger.debug(f"Filtered out '{result.get('name')}' - contains negative context")
                continue
                
            # Check for positive context words (these boost relevance)
            has_positive = any(pos_word in text_to_analyze for pos_word in positive_words)
            
            # Include if no negative words found (positive words are a bonus, not required)
            if not has_negative:
                filtered.append(result)
                
        return filtered
    
    def _calculate_therapeutic_score(self, result: Dict, positive_words: List[str], 
                                   negative_words: List[str], core_tags: List[str]) -> float:
        """Calculate a therapeutic relevance score for a sound."""
        score = 0.0
        
        # Base score from rating and downloads
        rating = result.get("avg_rating", 0)
        downloads = result.get("num_downloads", 0)
        score += rating * 2  # Rating weight
        score += min(downloads / 100, 5)  # Download popularity (capped)
        
        # Analyze text content
        text_content = (
            result.get("name", "").lower() + " " + 
            result.get("description", "").lower()
        )
        
        # Bonus for positive context words
        positive_matches = sum(1 for word in positive_words if word in text_content)
        score += positive_matches * 2
        
        # Penalty for negative context words (should be filtered out, but just in case)
        negative_matches = sum(1 for word in negative_words if word in text_content)
        score -= negative_matches * 5
        
        # Bonus for core tags in sound tags
        sound_tags = [tag.lower() for tag in result.get("tags", [])]
        core_tag_matches = sum(1 for tag in core_tags if tag in sound_tags)
        score += core_tag_matches * 3
        
        # Duration preference (moderate lengths are often better for therapeutic use)
        duration = result.get("duration", 0)
        if 60 <= duration <= 300:  # 1-5 minutes sweet spot
            score += 3
        elif 30 <= duration <= 600:  # Acceptable range
            score += 1
        
        return max(score, 0)  # Ensure non-negative score
