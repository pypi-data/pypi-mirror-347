from typing import List, Dict, Optional, Tuple
import re
import requests
import logging
import json
from .prompts import (
    EXTRACT_FORMALIZE_REQUIREMENT_PROMPT,
    CHAPTER_EXTRACTION_PROMPT,
    SUMMARY_PROMPT,
    CHAPTER_MERGING_PROMPT
)
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Tuple
from agents.base import BaseAgent
from core.config import config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RequirementAgent(BaseAgent):
    def __init__(self, chunk_size: int = 2000, overlap: int = 200, timeout: int = 240):
        super().__init__()
        self.requirement_counter = 0
        self.api_url = config.get('model_base_url')
        self.api_key = config.get('api_token')
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.timeout = timeout
            
        # Validate required configuration
        if not all([self.api_url, self.api_key, config.get('model_name')]):
            raise ValueError("Missing required configuration: API_URL, API_KEY, or MODEL_NAME")

    def _chat_completion(self, prompt: str, model: str = None, temperature: float = 0.1) -> str:
        """
        Make API call to chat completion endpoint with error handling
        """
        if model is None:
            model = config.get('model_name')
        if not prompt:
            raise ValueError("Prompt cannot be empty")
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature
        }
        
        # Calculate input token count
        input_tokens = sum(len(msg["content"].split()) for msg in payload["messages"])
        logger.debug(f"[Token Count] Input tokens: {input_tokens}")
        
        try:
            import time
            start_time = time.time()
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=(30, self.timeout))
            end_time = time.time()
            duration = end_time - start_time
            logger.debug(f" | Request duration: {duration:.2f}s")
            
            response.raise_for_status()
            result = response.json()
            
            # Get output token count
            output_tokens = len(result["choices"][0]["message"]["content"].split())
            logger.debug(f" | Output tokens: {output_tokens}")
            logger.debug(f" | Total tokens: {input_tokens + output_tokens}")
            
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            end_time = time.time()
            duration = end_time - start_time
            logger.error(f" | Request failed after {duration:.2f}s")
            logger.error(f"API request failed: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status code: {e.response.status_code}")
                logger.error(f"Response content: {e.response.text}")
            raise e
        except (KeyError, IndexError) as e:
            logger.error(f"Failed to parse API response: {str(e)}")
            raise ValueError("Invalid API response format")

    def process_requirements(self, chapters: List[Dict], overall_summary: Optional[str] = None) -> List[Dict]:
        """
        Process the text content and generate formal requirements directly
        
        Args:
            chapters (List[Dict]): chapters to process
            overall_summary (Optional[str]): Overall document summary
            
        Returns:
            List[Dict]: List of processed requirements
            
        Raises:
            ValueError: When error in chapters data structure
            json.JSONDecodeError: When API returns invalid JSON
        """
        if chapters is None or len(chapters) == 0:
            return []
            
        formal_requirements = []
        requirement_id_counter = 1  # Initialize a counter for requirement IDs

        # use threadpool to process each chapter, save result to formal_requirements in the order of chapters
        with ThreadPoolExecutor(max_workers=min(config.get('max_workers', 3), len(chapters))) as executor:
            futures = [executor.submit(self._process_chapter_requirements, chapter, overall_summary) for chapter in chapters]
            for future in as_completed(futures):
                chapter_requirements = future.result()
                # Assign IDs to each requirement
                for requirement in chapter_requirements:
                    requirement['id'] = f"REQ-{requirement_id_counter:03}"  # Format ID as a three-digit number
                    requirement_id_counter += 1
                formal_requirements.extend(chapter_requirements)
        
        return formal_requirements

    def _process_chapter_requirements(self, chapter: Dict, overall_summary: Optional[str] = None) -> List[Dict]:
        """Process the requirements for the given chapter"""

        # Validate chapter structure
        if 'title' not in chapter:
            logger.error(f"Chapter missing 'title' key. Chapter data: {chapter}")
            return []
        if 'content' not in chapter:
            logger.error(f"Chapter missing 'content' key. Chapter data: {chapter}")
            return []
        if overall_summary is None:
            logger.warning("Overall summary is None, which may affect requirement processing.")

        try:
            # Sanitize the content to remove invalid control characters
            sanitized_content = re.sub(r'[\x00-\x1F\x7F]', '', chapter['content'])
            
            # call chat completion to process the requirements for the given chapter
            prompt = EXTRACT_FORMALIZE_REQUIREMENT_PROMPT.format(
                title=chapter['title'], 
                content=sanitized_content, 
                overall_summary=overall_summary or ""
            )
            response = self._chat_completion(prompt)

            # Handle response that might be wrapped in markdown code blocks
            if response.startswith('```json') and response.endswith('```'):
                # Remove start and end code block markers
                response = response[7:-3]
                # Remove leading and trailing whitespace and \n
                response = response.strip('\n').strip()
            
            # sanitize the response to remove invalid control characters
            sanitized_response = re.sub(r'[\x00-\x1F\x7F]', '', response)

            # parse the response to get the formal requirements
            formal_requirements = json.loads(sanitized_response)
            return formal_requirements
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            logger.error(f"Problematic JSON string: {response}")
            return []
        except Exception as e:
            logger.error(f"Error processing chapter requirements: {str(e)}")
            logger.error(f"Chapter data: {chapter}")
            return []

    def identify_chapters(self, text_content: str) -> List[Dict]:
        """Identify chapters in the text content using multi-threading"""
        if not text_content:
            logger.debug("No text_content provided to identify_chapters.")
            return []
            
        chapters = []
        seen = set()
        
        try:
            # Create chunks with their indices
            chunks_with_indices = []
            for i in range(0, len(text_content), self.chunk_size - self.overlap):
                chunk = text_content[i:i+self.chunk_size]
                chunk_index = i // (self.chunk_size - self.overlap)
                chunks_with_indices.append((chunk_index, chunk))
            
            def process_chunk(chunk_data: Tuple[int, str]) -> Tuple[int, List[Dict]]:
                chunk_index, chunk = chunk_data
                logger.debug(f"Processing chunk {chunk_index + 1}: size={len(chunk)}")
                prompt = CHAPTER_EXTRACTION_PROMPT.format(chunk=chunk)
                logger.debug(f"Chapter extraction prompt (first 200 chars): {prompt[:200]}")
                
                response = self._chat_completion(prompt)
                logger.debug(f"Chapter extraction response (first 200 chars): {response[:200]}")
                match = re.search(r'\[.*\]', response, re.DOTALL)
                
                if match:
                    try:
                        chunk_chapters = json.loads(match.group(0))
                        logger.debug(f"Parsed chapters from chunk: {chunk_chapters}")
                        return chunk_index, chunk_chapters
                    except json.JSONDecodeError as e:
                        logger.warning(f"Failed to parse chapter JSON: {str(e)}")
                        return chunk_index, []
                return chunk_index, []
            
            # Use ThreadPoolExecutor to process chunks in parallel
            with ThreadPoolExecutor(max_workers=min(config.get('max_workers', 3), len(chunks_with_indices))) as executor:
                # Submit all tasks
                future_to_chunk = {
                    executor.submit(process_chunk, chunk_data): chunk_data 
                    for chunk_data in chunks_with_indices
                }
                
                # Collect results in order
                ordered_results = [None] * len(chunks_with_indices)
                for future in as_completed(future_to_chunk):
                    chunk_index, chunk_chapters = future.result()
                    ordered_results[chunk_index] = chunk_chapters
                    logger.info(f"Processed chunk {chunk_index + 1} / {len(chunks_with_indices)}, chapters count: {len(chunk_chapters)}")
            
            # Process results in order
            for chunk_chapters in ordered_results:
                if chunk_chapters:
                    for chap in chunk_chapters:
                        key = (chap.get('title'), chap.get('level'))
                        if key not in seen:
                            chapters.append(chap)
                            seen.add(key)
            
            logger.info(f"Identified chapters count: {len(chapters)}")

            # Merge small chapters
            if chapters:
                logger.debug(f"Original chapters count: {len(chapters)}")
                try:
                    # Convert chapters to JSON string for the prompt
                    chapters_json = json.dumps(chapters, ensure_ascii=False)
                    prompt = CHAPTER_MERGING_PROMPT.format(chapters=chapters_json)
                    
                    # Get merged chapters from model
                    response = self._chat_completion(prompt)
                    match = re.search(r'\[.*\]', response, re.DOTALL)
                    
                    if match:
                        try:
                            merged_chapters = json.loads(match.group(0))
                            logger.debug(f"Merged chapters count: {len(merged_chapters)}")
                            chapters = merged_chapters
                        except json.JSONDecodeError as e:
                            logger.warning(f"Failed to parse merged chapters JSON: {str(e)}")
                except Exception as e:
                    logger.error(f"Error merging chapters: {str(e)}")
            
            logger.info(f"merged chapters count: {len(chapters)}")

            # Add content to each chapter
            logger.debug("Adding content to chapters...")
            for chapter in chapters:
                chapter_title = chapter['title']
                # Find the next chapter title to determine content boundaries
                next_chapter_index = chapters.index(chapter) + 1
                if next_chapter_index < len(chapters):
                    next_chapter_title = chapters[next_chapter_index]['title']
                    # Extract content between current chapter title and next chapter title
                    pattern = f"{re.escape(chapter_title)}(.*?){re.escape(next_chapter_title)}"
                    match = re.search(pattern, text_content, re.DOTALL)
                    if match:
                        chapter['content'] = match.group(1).strip()
                    else:
                        chapter['content'] = ""
                else:
                    # For the last chapter, extract content until the end
                    pattern = f"{re.escape(chapter_title)}(.*?)$"
                    match = re.search(pattern, text_content, re.DOTALL)
                    if match:
                        chapter['content'] = match.group(1).strip()
                    else:
                        chapter['content'] = ""
                
                logger.info(f"Added content for chapter: {chapter_title}, length: {len(chapter['content'])}")
            
            return chapters
            
        except Exception as e:
            logger.error(f"Error identifying chapters: {str(e)}")
            return []

    def generate_summary(self, chapters: List[Dict]) -> Tuple[List[Dict], str]:
        """Generate a summary for the given chapters and return a string of all summaries"""
        if chapters is None or len(chapters) == 0:
            return [], ''
            
        # use threadpool to generate summary for each chapter and save summary to summary key in chapter
        with ThreadPoolExecutor(max_workers=min(config.get('max_workers', 3), len(chapters))) as executor:
            futures = [executor.submit(self._generate_chapter_summary, chapter) for chapter in chapters]
            for future in as_completed(futures):
                pass

        # join all summaries into one string
        return chapters, "\n\n".join([f"chapter: {chapter['title']}\n{chapter['summary']}" for chapter in chapters])
    
    def _generate_chapter_summary(self, chapter: Dict):
        """Generate a summary for the given chapter"""

        logger.info(f"Generating summary for chapter: {chapter['title']}")
        if not chapter:
            return None, ""
            
        prompt = SUMMARY_PROMPT.format(content=chapter['content'])
        response = self._chat_completion(prompt)

        # save summary to chapter['summary']
        chapter['summary'] = response.strip()
        logger.info(f"Summary generated for chapter: {chapter['title']}")