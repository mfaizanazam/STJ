#Necessary Imports
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import math
import os
from pathlib import Path

#Initiate driver and get URL
driver = webdriver.Chrome()
driver.get("https://scon.stj.jus.br/SCON/")

#declare variables to input elements
initial_date_id = driver.find_element_by_id('data_inicial')
final_date_id = driver.find_element_by_id('data_final')
selection_id = Select(driver.find_element_by_id('tipo_data'))

initial_date_id.clear()
final_date_id.clear()

#date in format dd.mm.yyyy. Insert your date here
initial_date = '01.03.2018'
final_date = '31.06.2018'

initial_date_id.send_keys(initial_date.replace(".",""))
final_date_id.send_keys(final_date.replace(".",""))

#If selection is julgamento then insert 0 otherwise insert 1
selection_id.select_by_index(0)

#click on next
driver.find_element_by_xpath('//*[@id="botoesPesquisa"]/input[1]').click()


#second page
time.sleep(10)
item_list = driver.find_elements_by_xpath('//*[@id="itemlistaresultados"]/span[1]')
doc_count = driver.find_elements_by_xpath('//*[@id="itemlistaresultados"]/span[2]')

#this for loop is for class of documents
for i in range(7): 
    
    #ignore if no document exists for particular class
    if doc_count[i].text == 'Nenhum documento encontrado.':
        print("No documents found for " + str(item_list[i].text))

    else:        
        inner_loop = int(doc_count[i].text.split(" ")[0])/10
        inner_loop = math.ceil(inner_loop)
        
        path = os.path.join(os.getcwd(), item_list[i].text)
        doc_count[i].click()

        driver.switch_to.window(driver.window_handles[0])

        #this for loop is to iterate over all result pages 
        for j in range(inner_loop):
            time.sleep(5) #sleep timer high otherwise captcha restriction
            print("Downloading Result html " + str(j) + "/" + str(inner_loop))
            
            file_name = 'STJ_' + initial_date + '-' + final_date + '_' + str(j) + '.html'
            Path(path).mkdir(parents=True, exist_ok=True)
            
            path_class = os.path.join(path, file_name)
            
            #save results html
            with open(path_class, 'w', encoding = "utf-8") as f:
                f.write(driver.page_source)
                f.close()
            
            time.sleep(5) #timer is high because of captcha restriction
            
            #if Acórdão exist then execute another loop to iterate over all Acórdãos in one page
            try:
                Acórdão = driver.find_elements_by_xpath('//*[@id="acoesdocumento"]/a[1]')
                Acórdão_count = len(Acórdão)
              
                for count in range(Acórdão_count):
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="acoesdocumento"]/a[1]')))
                    
                    print("Starting Acórdão per page " + str(count) + "/" + str(Acórdão_count))
                    Acórdão[count].click() #Íntegra_do_Acórdão
                
                    driver.switch_to.window(driver.window_handles[1])
                    
                    time.sleep(5)
                    
                    #this is to check if html format is available. This is available on recent documents but not in 1999 docs
                    try:
                        html_format = driver.find_element_by_id('id_formato_html')
                        html_format.click()
                    
                    except:
                        pass
                    
                    #check for all documents such as Certidão de Julgamento. Sometimes it is 3, in rare cases it is 8. I have mentioned arbitrary 25, you can increase this. The loop will exit safely if documents outside range do not exist
                    for doc in range(1,25):
                        doc_list = '//*[@id="listaAcordaos"]/ol/li/ul/li[' + str(doc) + ']/a'
                        alternate_doc_list = '//*[@id="idInterfaceVisualAreaBlocoInterno"]/div/form/ol/li/ul/div/span[1]/li[' + str(doc) + ']/a' 
                       
                        try:
                            doc_list_elem = driver.find_element_by_xpath(alternate_doc_list)
                                                       
                            print("Found " + doc_list_elem.text)
                            
                            sub_filename = doc_list_elem.text.split(r'/')[0].split(' ')[0] + "_" + str(count) + "_" + str(j) + '.html'
                            
                            sub_path_dir = os.path.join(path, doc_list_elem.text.split(r'/')[0].split(' ')[0])
                            sub_path = os.path.join(path, doc_list_elem.text.split(r'/')[0].split(' ')[0], sub_filename) 

                            doc_list_elem.click()
                            
                            driver.switch_to.window(driver.window_handles[2])

    
                            Path(sub_path_dir).mkdir(parents=True, exist_ok=True)
                            
                            #save document in desired locations
                            with open(sub_path, 'w', encoding = "utf-8") as f:
                                f.write(driver.page_source)
                                f.close()
                            
                            driver.switch_to.window(driver.window_handles[1])
                            #driver.find_element_by_xpath('/html/body/div[1]/a').click()
                        
                        except:
                            print("Exiting this loop at " + str(doc))
                            break
                    
                    driver.switch_to.window(driver.window_handles[0])
            
            except:
                pass
            
            driver.switch_to.window(driver.window_handles[0])
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            if j == 0 or j == (inner_loop-1):
                driver.find_elements_by_xpath('//*[@id="navegacao"]/a[2]')[1].click()
            else:
                driver.find_elements_by_xpath('//*[@id="navegacao"]/a[4]')[1].click()
            
            
        driver.switch_to.window(driver.window_handles[0])
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="voltarLista"]/a')))
        driver.find_element_by_xpath('//*[@id="voltarLista"]/a').click()
        


