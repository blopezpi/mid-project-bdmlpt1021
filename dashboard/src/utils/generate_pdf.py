import jinja2
import pdfkit


def generate_pdf(df):
    templateLoader = jinja2.FileSystemLoader(searchpath="./utils")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "pdf_report.html"
    template = templateEnv.get_template(TEMPLATE_FILE)

    outputText = template.render(df=df)
    html_file = open("pdf_report_table.html", "w")
    html_file.write(outputText)
    html_file.close()
    pdfkit.from_file("pdf_report_table.html", "pdf_report.pdf")
