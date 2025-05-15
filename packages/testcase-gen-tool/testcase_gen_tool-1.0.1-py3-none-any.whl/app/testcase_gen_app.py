from datetime import datetime
import gradio as gr
import logging
from pathlib import Path
import sys
import os
from typing import Dict, List, Tuple
import pandas as pd
import traceback


from core.config import config
from agents.requirement_agent import RequirementAgent
from agents.testcase_agent import TestCaseAgent
from utils.document_processor import DocumentProcessor


logger = logging.getLogger(__name__)

class TestCaseGenApp:
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.requirement_agent = None
        self.testcase_agent = None
        self.current_requirements = None
        self.current_test_cases = None

    def initialize_agents(self):
        """Initialize agents with current configuration"""
        self.requirement_agent = RequirementAgent()
        self.testcase_agent = TestCaseAgent()

    def process_document(
        self,
        file: gr.File,
        api_token: str,
        model_base_url: str,
        model_name: str,
        max_workers: int,
        status_callback=None,
        progress=None
    ) -> Tuple[str, str]:
        """Process the uploaded document"""
        try:
            # Update configuration
            logger.debug("Updating configuration...")
            if status_callback:
                status_callback("正在更新配置...")
            
            # Update configuration with new values
            new_config = {
                'api_token': api_token,
                'model_base_url': model_base_url,
                'model_name': model_name,
                'max_workers': max_workers
            }
            config.update_config(new_config)
            
            # Initialize agents with new configuration
            self.requirement_agent = RequirementAgent()
            self.testcase_agent = TestCaseAgent()
            
            # Process document
            if status_callback:
                status_callback("正在处理文档...")
            if progress is not None:
                progress(0.0, desc="正在处理文档...")
            
            # Extract text from document
            text_content = self.document_processor.process_document(file)
            if progress is not None:
                progress(0.1, desc="正在识别章节...")
            chapters = self.requirement_agent.identify_chapters(text_content)

            if progress is not None:
                progress(0.3, desc="正在生成章节和全文摘要...")
            chapters,overall_summary = self.requirement_agent.generate_summary(chapters)

            if progress is not None:
                progress(0.6, desc="正在提取需求...")
            requirements = self.requirement_agent.process_requirements(chapters, overall_summary)

            if progress is not None:
                progress(0.7, desc="正在生成测试用例...")
            test_cases = self.testcase_agent.generate_test_cases(requirements)

            if progress is not None:
                progress(0.9, desc="正在保存结果...")
            output_file = self._save_results(chapters, requirements, test_cases)

            if progress is not None:
                progress(1.0, desc="处理完成！")
            
            logger.info("Document processing completed successfully")
            return "处理完成！", str(output_file)
            
        except Exception as e:
            error_msg = f"处理文档时出错: {str(e)}"
            logger.error(error_msg)
            logger.error(f"\n异常堆栈:\n{traceback.format_exc()}")
            if status_callback:
                status_callback(error_msg)
            raise gr.Error(error_msg)

    def _save_results(self, chapters: List[Dict], requirements: List[Dict], test_cases: List[Dict]) -> str:
        """Save requirements and test cases to Excel file"""
        try:
            # Create output directory if it doesn't exist
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)

            # Create DataFrame for chapters with both summary and content
            chapters_df = pd.DataFrame([
                {
                    'Level': chapter['level'],
                    'Chapter': chapter['title'],
                    'Summary': chapter.get('summary', ''),
                    'Content': chapter.get('content', '')
                }
                for chapter in chapters
            ])
            

            # Create DataFrame for requirements
            requirements_df = pd.DataFrame([
                {
                    'ID': req['id'],
                    'Title': req['title'],
                    'Formal Requirement': req['formal'],
                    'Original Text': req['original'],
                    'Clarification Questions': '\n'.join(req.get('clarification_questions', [])),
                    'Method': req.get('method', ''),
                    'Reason': req.get('reason', '')
                }
                for req in requirements
            ])
            
            # Create DataFrame for test cases
            test_cases_df = pd.DataFrame([
                {
                    'ID': tc['id'],
                    'Title': tc['title'],
                    'Precondition': '\n'.join(tc['preconditions']),
                    'Test Steps': '\n'.join(tc['steps']),
                    'Expected Result': '\n'.join(tc['expected_results']),
                    'Requirement ID': tc['related_requirement']['id'],
                    'Requirement Title': tc['related_requirement']['title'],
                    'Method': tc['strategy']
                }
                for tc in test_cases
            ])
            
            # Save to Excel with multiple sheets
            output_file = output_dir / f"requirements_and_test_cases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                chapters_df.to_excel(writer, sheet_name='Chapters', index=False)
                requirements_df.to_excel(writer, sheet_name='Formal Requirements', index=False)
                test_cases_df.to_excel(writer, sheet_name='Test Cases', index=False)
                
            logger.info(f"Results saved to {output_file}")

            # convert output_file to absolute path  
            return str(output_file.absolute())
            
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
            raise 