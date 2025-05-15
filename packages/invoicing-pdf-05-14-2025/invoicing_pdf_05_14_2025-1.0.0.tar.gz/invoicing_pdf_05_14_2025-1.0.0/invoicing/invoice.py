import os

import pandas as pd

import glob
from fpdf import FPDF
from pathlib import Path


def generate(invoices_path, pdfs_path, product_id, product_name, amount_purchased, price_per_unit, total_price):
    """
    this function converts invoice Excel files into pdf's.
    :param invoices_path:
    :param pdfs_path:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :return:
    """
    filepaths = glob.glob(f"{invoices_path}/*.xlsx")

    for filepath in filepaths:
        df = pd.read_excel(filepath, sheet_name="Sheet 1")

        pdf = FPDF(orientation="p", unit="mm", format="A4")
        pdf.add_page()

        filename = Path(filepath).stem  # stem is like a property for that file
        invoice_nr, date = filename.split("-")


        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Invoice nr.{invoice_nr}", ln=1) #ln is break b/w invoice nr and date.

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Date:{date}", ln =1)

        df = pd.read_excel(filepath, sheet_name="Sheet 1")


        columns_a = list(df.columns) # this is for columns and below code is for printing its values
        columns_a= [item.replace("_", " ").title() for item in columns_a]
        pdf.set_font(family="Times", size=10, style="B")
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt=columns_a[0], border=1)
        pdf.cell(w=70, h=8, txt=columns_a[1], border=1)
        pdf.cell(w=30, h=8, txt=columns_a[2], border=1)
        pdf.cell(w=30, h=8, txt=columns_a[3], border=1)
        pdf.cell(w=30, h=8, txt=columns_a[4], border=1, ln=1)
        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(80,80,80)
            pdf.cell(w=30, h=8, txt=str(row[product_id]),border=1)
            pdf.cell(w=70, h=8, txt=str(row[product_name]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]),border=1)
            pdf.cell(w=30, h=8, txt=str(row[total_price]),border=1, ln=1)

        total_sum = df[total_price].sum()
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=70, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt="", border=1)
        pdf.cell(w=30, h=8, txt=str(total_sum), border=1, ln=1)
         # adding total sum sentence
        pdf.set_font(family="Times", size=10, style="B")
        pdf.cell(w=30, h=8, txt=f"The total price is{total_sum}", ln=1)

        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)
        pdf.output(f"{pdfs_path}/{filename}.pdf")