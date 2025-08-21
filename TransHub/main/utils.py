from django.db.models import Count
from django.core.cache import cache
from django.shortcuts import get_object_or_404
import xlwings as xw
from .models import *
import os
from django.core.files import File

from django.conf import settings

menu = [{'title': "Про сайт", 'url_name': 'about'},
        {'title': "О перевезеннях", 'url_name': 'about_cargo'},
        {'title': "Зворотній зв'язок", 'url_name': 'contact'},
]
class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)



        context['menu'] = user_menu
        return context


file_path = 'main/акт.xlsx'
file2_path = 'main/сф.xls'

def replace_docs(replacements, act_file):

    save_date = replacements["[data]"]
    nomer = replacements["[nomer_act]"]

    app = xw.App(visible=False)
    wb = xw.Book(file_path)
    sheet = wb.sheets['Sheet1']

    try:
        for shape in sheet.shapes:
            shape_text = shape.text
            updated_text = shape_text

            for placeholder, value in replacements.items():
                updated_text = updated_text.replace(placeholder, value)

            if shape_text != updated_text:
                shape.text = updated_text
        cells_to_update = ["A22", "J22", "C23"]

        for cell in cells_to_update:
            cell_text = sheet.range(cell).value
            if cell_text:
                updated_cell_text = cell_text

            for placeholder, value in replacements.items():
                updated_cell_text = str(updated_cell_text).replace(placeholder, str(value))

            if cell_text != updated_cell_text:
                sheet.range(cell).value = updated_cell_text

        save_path = f"documents/acts/"
        os.makedirs(save_path, exist_ok=True)
        new_file_name = f"акт_{nomer}_{save_date}.xlsx"
        new_file_path = os.path.join(save_path, new_file_name)
        wb.save(new_file_path)

    finally:
        wb.close()
        app.quit()

    with open(new_file_path, 'rb') as f:
        act_file.save(new_file_name, File(f), save=True)

    print(f"Файл успешно сохранен в базе данных для объекта {act_file}")

def replace2_docs(replacements, invoice_file ):
    save_date = replacements["[data]"]
    nomer = replacements["[nomer_act]"]

    app = xw.App(visible=False)
    wb = xw.Book(file2_path)
    sheet = wb.sheets['Лист1']

    try:
        for row in range(1, 31):
            for col in range(1, 10):
                cell = sheet.range((row, col))
                cell_text = cell.value

                if cell_text and any(placeholder in str(cell_text) for placeholder in replacements):
                    updated_cell_text = str(cell_text)

                    for placeholder, value in replacements.items():
                        updated_cell_text = updated_cell_text.replace(placeholder, str(value))

                    if cell_text != updated_cell_text:
                        cell.value = updated_cell_text

        save_path = f"documents/invoices/"
        os.makedirs(save_path, exist_ok=True)
        new_file_name = f"сф_{nomer}_{save_date}.xls"
        new_file_path = os.path.join(save_path, new_file_name)
        wb.save(new_file_path)

    finally:
        wb.close()
        app.quit()

    with open(new_file_path, 'rb') as f:
        invoice_file.save(new_file_name, File(f), save=True)

    print(f"Файл успешно сохранен в базе данных для объекта {invoice_file}")

    pass