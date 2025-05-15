import gradio as gr
import sys
import os
import logging

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from core.config import config
from core.logging import setup_logging
from app.testcase_gen_app import TestCaseGenApp


logger = logging.getLogger(__name__)

def create_interface():
    """Create and launch the Gradio interface"""
    app = TestCaseGenApp()
    
    def process_document_wrapper(file, model_base_url, model_name, api_token, max_workers, progress=gr.Progress()):
        """Wrapper function to handle progress updates"""
        def update_status(msg):
            progress(0, desc=msg)
        
        try:
            result = app.process_document(
                file=file,
                api_token=api_token,
                model_base_url=model_base_url,
                model_name=model_name,
                max_workers=max_workers,
                status_callback=update_status,
                progress=progress
            )
            return result
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise gr.Error(str(e))
    
    # Create Gradio interface
    interface = gr.Interface(
        fn=process_document_wrapper,
        inputs=[
            gr.File(label="上传需求文档"),
            gr.Textbox(label="Model Base URL", value=config.get('model_base_url', '')),
            gr.Textbox(label="Model Name", value=config.get('model_name', '')),
            gr.Textbox(label="API Token", value=config.get('api_token', '')),
            gr.Number(label="Max Workers", value=config.get('max_workers', 10), precision=0)
        ],
        outputs=[
            gr.Textbox(label="处理状态"),
            gr.File(label="处理结果")
        ],
        title="需求文档测试用例生成工具",
        description="上传需求文档，自动生成测试用例"
    )
    
    return interface

def main():
    setup_logging(level=logging.INFO)
    interface = create_interface()
    interface.launch(share=False)

if __name__ == "__main__":
    main()