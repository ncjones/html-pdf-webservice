#! /usr/bin/env python
"""
    html-pdf-webservice

    Copyright 2014 Nathan Jones
    Copyright 2013 Openlabs Technologies & Consulting (P) Limited
    See LICENSE for more details.
"""

import shutil
import StringIO
from subprocess import Popen, PIPE

from werkzeug.wsgi import wrap_file
from werkzeug.exceptions import MethodNotAllowed, BadRequest
from werkzeug.wrappers import Request, Response


@Request.application
def application(request):
    """
    WSGI web service for rendering HTML to PDF using wkhtmltopdf.

    Accepts a POST request with a form encoded body with a single "html" form
    field which is expected to have an HTML document as the value. The
    response body will contain a PDF rendering of the input HTML file.
    """
    if request.method != 'POST':
        return MethodNotAllowed(['POST'])
    if request.files.get('html'):
        html_file = request.files['html']
    elif request.form.get('html'):
        html_file = StringIO.StringIO(request.form.get('html').encode('utf-8'))
    else:
        return BadRequest('html is required')
    process = Popen(['wkhtmltopdf', '-q', '-', '-'], stdin=PIPE, stdout=PIPE)
    shutil.copyfileobj(html_file, process.stdin)
    process.stdin.close()
    return Response(
        wrap_file(request.environ, process.stdout),
        mimetype='application/pdf',
    )


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple(
        '127.0.0.1', 5000, application, use_debugger=True, use_reloader=True
    )
