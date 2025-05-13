# DOCX Renderer

This package lets you run your Microsoft Word documents like a script.
You can insert placeholders in the document and use either a Python function
or an equivalent command-line tool to convert it into an output rendered document.

[Documentation](https://docx-renderer.readthedocs.io/en)

## Installation
```console
pip install docx-renderer
```

## Usage
Below is a simple example.

```python
from docx_renderer import DOCXRenderer
p = DOCXRenderer("template.docx")

someval = "world!"
def mymethod(abc):
    return f"{abc} " * 5

p.render(
    "output.docx", 
    {
        "variable": someval, "mymethod": mymethod, "myimage": "is_it_worth.png"
    }
)
```

This will replace placeholders in the template document with the provided values.

## Before

![Before](./docs/_src/_static/before.png)

## After

![After](./docs/_src/_static/after.png)

You can define some functions within the document itself by writing Python code in
the comments section. The variables and functions in this code can be used in the main document.

For example: write the following in one of the comments in the document.

<pre>
```python
def myfunc(input):
    return input * 42
```
</pre>

Now you can, for example, add the placeholder `{{{myfunc(42)}}}` in your document.

If the template document is a self-contained Python script (i.e., it does not require
variable values and function definitions to be passed from outside), you can
generate the output document directly from the command line using the following
command.

```console
docx-renderer input_template.docx output_file.docx
```

## Placeholders
You can have placeholders for text, images, or tables. Placeholders can be added
inside paragraphs or tables. All placeholders should be enclosed within a pair
of triple braces (`{{{` and `}}}`).

### Text
Any placeholder which can be evaluated into a string can act as a text placeholder.

For example: `{{{"hello " * 10/2}}}` or `{{{abs(-2)}}}`

### Image
If you have added `:image()` as a suffix to the Python statement, the renderer will
try to convert the value of the Python statement to a file location and insert an
image from that file location.

For example: `{{{"c:\\temp\\myimage.png":image()}}}`

### Table
Tables are similar to images, but instead of a string, the Python
statement should evaluate to a list of lists. Then you can add `:table()` as a
suffix, and it will be converted to a table inside the document.

For example: `{{{[["col1", "col2", "col3"],[1, 2, 3]]:table()}}}` will render to

|col1 | col2 | col3|
|-----|------|-----|
|1    |2     |3    |

## Code in comments
You can write regular Python code in the comments section of the document but enclosed between
`` ```python `` and `` ``` ``.

For example: Add the following in a comment in the document.

<pre lang="python">
```python
import numpy as np
myarr = np.array([[1, 2], [3, 4]])
```
</pre>

And in the document, add the text `{{{myarr:table()}}}`
and a paragraph with the text `The determinant of the array is {{{np.linalg.det(myarr)}}}`.
