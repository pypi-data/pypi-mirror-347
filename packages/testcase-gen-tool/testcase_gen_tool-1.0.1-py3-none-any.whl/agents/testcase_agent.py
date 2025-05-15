from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import logging
import json
from .prompts import (
    TEST_CASE_GENERATION_PROMPT,
    TEST_DESIGN_METHOD_SELECTION_PROMPT
)
from agents.base import BaseAgent
from core.config import config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestCaseAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.testcase_counter = 0
        self.api_url = config.get('model_base_url')
        self.api_key = config.get('api_token')

    def _chat_completion(self, prompt, model=None, temperature=0.1):
        if model is None:
            model = config.get('model_name')
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature
        }
        response = requests.post(self.api_url, headers=headers, json=payload, timeout=240)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def generate_test_cases(self, requirements: List[Dict]) -> List[Dict]:
        """Process requirements and generate test cases"""
        test_cases = []
        
        try:
            # Use ThreadPoolExecutor for parallel processing
            with ThreadPoolExecutor(max_workers=config.get('max_workers', 3)) as executor:
                # Submit all requirements for processing
                future_to_req = {
                    executor.submit(self._generate_test_cases_for_requirement, req): req 
                    for req in requirements
                }
                
                # Collect results as they complete
                for future in as_completed(future_to_req):
                    req = future_to_req[future]
                    try:
                        req_test_cases = future.result()
                        test_cases.extend(req_test_cases)
                        logger.debug(f"Generated {len(req_test_cases)} test cases for requirement: {req['title']}")
                    except Exception as e:
                        logger.error(f"Error generating test cases for requirement {req['title']}: {str(e)}")
            
            return test_cases
            
        except Exception as e:
            logger.error(f"Error in process_requirements: {str(e)}")
            raise
    
    def _select_test_design_method(self, requirement_info: Dict) -> str:
        """Select the most appropriate test design method for the requirement"""
        try:

            return requirement_info['method']
            
        except Exception as e:
            logger.error(f"Error selecting test design method: {str(e)}")
            return "Decision Table"  # Default method
    
    def _generate_test_cases_for_requirement(self, requirement_info: Dict) -> List[Dict]:
        """Generate test cases for a specific requirement"""
        try:
            # Select test design method
            method = self._select_test_design_method(requirement_info)
            
            # Generate test cases
            prompt = TEST_CASE_GENERATION_PROMPT.format(
                method=method,
                reqId=requirement_info['id'],
                reqTitle=requirement_info['title'],
                reqFormal=requirement_info['formal']
            )
            
            response = self._chat_completion(prompt)
            try:
                test_cases = json.loads(response)
                # Add requirement ID to each test case
                for tc in test_cases:
                    tc['requirement_id'] = requirement_info['id']
                    tc['id'] = f"TC{self.testcase_counter:04d}"
                    self.testcase_counter += 1
                return test_cases
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing test cases JSON: {str(e)}")
                return []
        except Exception as e:
            logger.error(f"Error generating test cases: {str(e)}")
            return []