import os
import fitz # PyMuPDF
import pypandoc





class TextExtractor:
    def extract_text_from_pdf(fname: str = None, pdf_stream: bytes = None) -> str:
        """Extracts text from a PDF file or byte stream."""
        if fname:
            doc = fitz.open(fname)  # open from file path
        elif pdf_stream:
            doc = fitz.open(stream=pdf_stream, filetype="pdf")  # open from memory
        else:
            raise ValueError("Either fname or pdf_stream must be provided.")

        text = ""
        for page in doc:
            text += page.get_text()

        return text.strip()


    def extract_text_from_docx(docx_path: str = None, docx_stream: bytes = None) -> str:
        """Extracts text from DOCX file or byte stream using pypandoc."""
        if docx_path:
            return pypandoc.convert_file(docx_path, 'plain')
        elif docx_stream:
            # Convert in-memory DOCX → temp file workaround (pypandoc requires a file)
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
                tmp.write(docx_stream)
                tmp_path = tmp.name
            text = pypandoc.convert_file(tmp_path, 'plain')
            os.remove(tmp_path)
            return text
        else:
            raise ValueError("Either docx_path or docx_stream must be provided.")

    def extract_text(file_path: str = None, file_stream: bytes = None) -> str:
        """Determines the file type and extracts text accordingly."""

        if file_path is None and file_stream is None:
            raise ValueError("Must provide either file_path or file_stream + file_path (with extension).")

        # Get extension (always needs file_path for extension)
        if file_path:
            ext = os.path.splitext(file_path)[-1].lower()
        else:
            raise ValueError("file_path (with extension) is required to determine file type.")

        if ext == ".pdf":
            return extract_text_from_pdf(fname=file_path if file_stream is None else None,
                                        pdf_stream=file_stream)
        elif ext == ".docx":
            return extract_text_from_docx(docx_path=file_path if file_stream is None else None,
                                        docx_stream=file_stream)
        else:
            raise ValueError("Unsupported file format. Only PDF and DOCX are supported.")



