from robocorp.tasks import task
from robocorp import browser
import time

from RPA.Browser.Selenium import Selenium
from RPA.Tables import Tables
from RPA.Desktop import Desktop
from RPA.PDF import PDF
from RPA.Archive import Archive


csv = Tables();
rpa_browser = Selenium();
desktop = Desktop();
pdf = PDF();
lib = Archive();


logs = ["log1","log2","log3"]
typed_texts = [] #Textos que el usuario ha escrito por teclado

@task
def run_bot():

    previous_element_was_mouseclick = {"category":"",
                                       "coordX":"",
                                       "coordY":""}
    for log in logs:
        csv_file=csv.read_table_from_csv(f"ScreenActionsLogger_logs/{log}.csv",header=True)
        execute_csv_actions(csv_file,previous_element_was_mouseclick); 
    
    
def execute_csv_actions(csv_file,previous_element_was_mouseclick):
    for row in csv_file:
        rpa_action(row,previous_element_was_mouseclick)
    

    
def rpa_action(csv_row,previous_element_was_mouseclick):        
    if( csv_row["category"]=="MouseClick"):
        #Si el nuevo click tiene las mismas coordenadas que el anterior, supondremos que es un doble Click
        if(csv_row["category"]== previous_element_was_mouseclick["category"] and int(float(csv_row['coordX'])) == previous_element_was_mouseclick["coordX"] and int(float(csv_row['coordY'])) == previous_element_was_mouseclick["coordY"]):
            corX = int(float(csv_row['coordX']));
            corY= int(float(csv_row['coordY']))
            desktop.click(f"point:{corX},{corY}","double_click");
            previous_element_was_mouseclick["coordX"] = int(float(csv_row['coordX'])); #Actualiza coordenada X almacenado en el actual mouseClick
            previous_element_was_mouseclick["coordY"] = int(float(csv_row['coordY'])); #Actualiza coordenada X almacenado en el actual mouseClick
            time.sleep(1)
        else: ## Si es un click pero tiene otras coordenadas, no se trata de un doble click
            corX = int(float(csv_row['coordX']));
            corY= int(float(csv_row['coordY']))
            desktop.click(f"point:{corX},{corY}","click")
            previous_element_was_mouseclick["category"] = str(csv_row['category'])
            previous_element_was_mouseclick["coordX"] = int(float(csv_row['coordX'])); #Actualiza coordenada X almacenado en el actual mouseClick
            previous_element_was_mouseclick["coordY"] = int(float(csv_row['coordY'])); #Actualiza coordenada X almacenado en el actual mouseClick
            time.sleep(1)
    if(csv_row["category"]=="Keyboard"):
        text = str(csv_row["typed_word"])
        typed_texts.append(text)
        desktop.type_text(text)   
        time.sleep(1)
        
@task
def create_pdf_file():
    ''' Pasar las capturas obtenidas en un solo archivo pdf'''
    add_type_texts_to_pdf()
    # embed_screenshots_to_pdf()
    
def add_type_texts_to_pdf():
    pdf = PDF()    
    pdf.html_to_pdf("<br/>".join(typed_texts), "output/prueba_multilogs.pdf");
    
# def embed_screenshots_to_pdf():
#         pdf.add_files_to_pdf(
#         files=["output/screenshots/log1/google_form.png",
#                "output/screenshots/gmx_pagina de inicio.png",
#                "output/screenshots/google_form_with_checkbox.png",
#                "output/screenshots/google_form.png"],
#         target_document="output/prueba_multilogs.pdf",
#         append=True
#     )
   
@task    
def create_output_zip():
    '''Crear un fichero zip con todo el output'''
    lib.archive_folder_with_zip('./output/', './output.zip', recursive=True)
