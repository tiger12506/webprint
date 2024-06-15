import os
import sys
from flask import Flask, request, render_template
import cups
import tempfile

app = Flask(__name__)

@app.route('/ip')
def index():
    return '<center><h1>'+request.remote_addr+'</h1></center>'

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        conn = cups.Connection()
        upload = request.files['upload']
        with tempfile.NamedTemporaryFile() as fp:
            upload.save(fp.name)
            conn.printFile(app.config['printer_name'], fp.name, 'WebPrinter', {})
        return '<p>Now printing %s. Go to the printer!</p>' % upload.filename

@app.route('/printers', methods=['GET'])
def printers():
    import pprint
    result = "<!DOCTYPE html><html><body><pre>"
    con = cups.Connection()
    result += pprint.pformat(con.getPrinters())
    result += "</pre></body></html>"
    return result

@app.route('/queues', methods=['GET'])
def queues():
    import pprint
    result = "<pre>"
    con = cups.Connection()
    result += pprint.pformat(con.getJobs(which_jobs='all'))
    result += "\n\n" + pprint.pformat(con.getJobAttributes(1))
    result += "</pre>"
    return result

if __name__ == '__main__':
    debug = False
    if (len(sys.argv) > 1):
        port = int(sys.argv[1])
    if (len(sys.argv) > 2):
        debug = bool(sys.argv[2])
    app.config['printer_name'] = cups.Connection().getDefault()
    app.run(host='0.0.0.0', port=port, debug=debug)

