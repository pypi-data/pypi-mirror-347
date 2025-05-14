# some basic tests

from pathlib import Path
from docx_renderer import DOCXRenderer
from docx_renderer.exceptions import RenderError
import pytest
from docx import Document

def mymethod(abc):
    return f"{abc} " * 5


def test_initiation():
    p = DOCXRenderer("template.docx")
    assert p.template_path == "template.docx"


def test_file_not_exist():
    with pytest.raises(FileNotFoundError):
        DOCXRenderer("nonexistentfile.docx")


def test_render():
    p = DOCXRenderer("template.docx")
    with pytest.raises(RenderError):
        p.render(
            "output.docx",
            {"mymethod": mymethod},
        )


def test_render_skip_failed():
    p = DOCXRenderer("template.docx")
    p.render(
        "output.docx",
        {"mymethod": mymethod},
        skip_failed=True,
    )
    assert Path("output.docx").exists()
    document = Document("output.docx")
    assert any("mymethod" in paragraph.text for paragraph in document.paragraphs)
