from pathlib import Path
from subprocess import run
from docx import Document
import json


def test_basic_cli():
    """Test the basic CLI"""
    run(["docx-renderer", "template.docx", "output_cli.docx"])
    assert Path("output_cli.docx").exists()
    Path("output_cli.docx").unlink()


def test_with_input():
    """Test passing an input"""
    input_data = {"myvar1": "hello 1", "myvar2": "hello 2"}
    input_path = Path("input.json")
    input_path.write_text(json.dumps(input_data))

    run([
        "docx-renderer",
        "template.docx",
        "output_cli.docx",
        "--input",
        str(input_path),
    ])

    assert Path("output_cli.docx").exists()
    document = Document("output_cli.docx")
    paragraphs = [p.text for p in document.paragraphs]
    assert "hello 1" in paragraphs
    assert "hello 2" in paragraphs

    Path("output_cli.docx").unlink()
    input_path.unlink()
