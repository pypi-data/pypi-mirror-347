import PyPDF2
from docx import Document
from typing import BinaryIO, Optional, Callable
import io
import logging

logger = logging.getLogger(__name__)

class DocumentProcessor:
    def extract_text(self, file: BinaryIO, file_type: str) -> str:
        """
        Extract text content from a document file
        
        Args:
            file (BinaryIO): The file object
            file_type (str): The file type (pdf, doc, docx)
            
        Returns:
            str: Extracted text content
        """
        try:
            if file_type == 'pdf':
                return self._extract_from_pdf(file)
            elif file_type in ['doc', 'docx']:
                return self._extract_from_word(file)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
        except Exception as e:
            raise Exception(f"Error processing {file_type} file: {str(e)}")

    def process_document(self, file: BinaryIO, status_callback: Optional[Callable[[str], None]] = None) -> str:
        """
        Process document and extract text content with progress tracking
        
        Args:
            file (BinaryIO): The file object
            status_callback (Optional[Callable[[str], None]]): Callback function for status updates
            
        Returns:
            str: Extracted text content
        """
        try:
            file_name = file.name
            file_type = file_name.split('.')[-1].lower()
            logger.info(f"Processing file type: {file_type}")
            
            if file_type in ['pdf', 'doc', 'docx']:
                logger.debug("Extracting text from document file...")
                if status_callback:
                    status_callback("正在从文档中提取文本...")
                text_content = self.extract_text(file, file_type)
            else:
                logger.debug("Reading text file content...")
                if status_callback:
                    status_callback("正在读取文本文件内容...")
                text_content = file.read().decode('utf-8')
                
            logger.info(f"Successfully extracted text content, length: {len(text_content)}")
            return text_content
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise

    def _extract_from_pdf(self, pdf_file: BinaryIO) -> str:
        """Extract text from PDF file"""
        try:
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from all pages
            text_content = ""
            for page in pdf_reader.pages:
                text_content += page.extract_text() + "\n"
            
            return text_content
            
        except Exception as e:
            raise Exception(f"Error processing PDF file: {str(e)}")

    def _extract_from_word(self, word_file: BinaryIO) -> str:
        """Extract text from Word file (DOC/DOCX)"""
        try:
            # Create a copy of the file in memory
            file_content = word_file.read()
            file_stream = io.BytesIO(file_content)
            
            # Load the document
            doc = Document(file_stream)
            
            # Extract text from all paragraphs
            text_content = ""
            for paragraph in doc.paragraphs:
                text_content += paragraph.text + "\n"
            
            return text_content
            
        except Exception as e:
            raise Exception(f"Error processing Word file: {str(e)}") 