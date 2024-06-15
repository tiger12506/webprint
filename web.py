import os
import sys
from flask import Flask, request, render_template
import cups
import tempfile
from pprint import pformat,pprint

app = Flask(__name__)

@app.route('/ip')
def ip():
    return '<center><h1>'+request.remote_addr+'</h1></center>'

@app.route('/', methods=['GET'])
def index():
    return render_template('upload.html')

@app.route("/upload", methods=['POST'])
def upload():
    conn = cups.Connection()
    f = request.files['file'] # Refers to the element "name" attribute of the form
#    print("Submitted file: "+f.filename)
    with tempfile.NamedTemporaryFile() as fp:
        f.save(fp.name)
#        print("Saved file as: "+fp.name)
        conn.printFile(app.config['printer_name'], fp.name, 'WebPrinter', {})

    return render_template("alert.html", msg=f.filename+" sent successfully!")

@app.route('/printers', methods=['GET'])
def printers():
    result = "<!DOCTYPE html><html><body><pre>"
    con = cups.Connection()
    result += pformat(con.getPrinters())
    result += "</pre></body></html>"
    return result

@app.route('/queues', methods=['GET'])
def queues():
    result = "<pre>"
    con = cups.Connection()
    result += pformat(con.getJobs(which_jobs='all'))
    result += "\n\n" + pformat(con.getJobAttributes(44))
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

