from pyreportjasper import PyReportJasper
import json
import os

def gen_invoice(data=None):
    if(data!= None):
        BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)))
        with open(os.path.join(BASE_DIR, 'data.json'), 'w') as file:
            json.dump(data, file, indent=4)

        conn = {
              'driver': 'json',
              'data_file': os.path.join(BASE_DIR, 'data.json'),
        }


        input_file = os.path.join(BASE_DIR, 'InvoiceHeader.jrxml')
        output_file = os.path.join(BASE_DIR, 'report.pdf')
        pyreportjasper = PyReportJasper()
        pyreportjasper.config(
              input_file,
              output_file,
              output_formats=["pdf"],
              db_connection=conn,
           )
        pyreportjasper.process_report()
        with open(os.path.join(BASE_DIR, 'report.pdf'), 'rb') as file:
            pdf_content = file.read()
            return pdf_content
    else:
        BASE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)))
        if os.path.isfile(os.path.join(BASE_DIR, 'report.pdf')):
            os.remove(os.path.join(BASE_DIR, 'report.pdf'))
        if os.path.isfile(os.path.join(BASE_DIR, 'data.json')):
            os.remove(os.path.join(BASE_DIR, 'data.json'))
        return  None

