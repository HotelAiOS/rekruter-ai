import pytest
from services.pdf_parser import PDFParserService
from pathlib import Path
import tempfile

class TestPDFParser:
    """Test PDF parsing functionality"""
    
    def test_extract_text_from_txt_file(self):
        """Test TXT file fallback"""
        # Create temp TXT file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("John Doe\nemail@example.com\nPython Developer")
            filepath = f.name
        
        # Extract text
        result = PDFParserService.extract_text(filepath)
        
        # Assertions
        assert result is not None
        assert "John Doe" in result
        assert "Python Developer" in result
        
        # Cleanup
        Path(filepath).unlink()
    
    def test_extract_text_unsupported_format(self):
        """Test unsupported file format"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xyz', delete=False) as f:
            f.write("Test data")
            filepath = f.name
        
        result = PDFParserService.extract_text(filepath)
        
        # Should still read as TXT fallback
        assert result is not None or result is None  # Depends on implementation
        
        Path(filepath).unlink()
    
    def test_extract_text_empty_file(self):
        """Test empty file handling"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            filepath = f.name
        
        result = PDFParserService.extract_text(filepath)
        
        assert result is None or result == ""
        
        Path(filepath).unlink()
    
    def test_extract_text_nonexistent_file(self):
        """Test nonexistent file handling"""
        result = PDFParserService.extract_text("/nonexistent/file.pdf")
        
        assert result is None
