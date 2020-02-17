from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import math
import os
import pywinauto

driver = webdriver.Chrome()
driver.get("https://scon.stj.jus.br/SCON/")


initial_date_id = driver.find_element_by_id('data_inicial')
final_date_id = driver.find_element_by_id('data_final')
selection_id = Select(driver.find_element_by_id('tipo_data'))

#date in format dd.mm.yyyy
initial_date_id.clear()
final_date_id.clear()

initial_date = '31.01.1999'
final_date = '02.02.1999'

initial_date_id.send_keys(initial_date.replace(".",""))
final_date_id.send_keys(final_date.replace(".",""))
selection_id.select_by_index(0)


driver.find_element_by_xpath('//*[@id="botoesPesquisa"]/input[1]').click()


#second page
time.sleep(10)
item_list = driver.find_elements_by_xpath('//*[@id="itemlistaresultados"]/span[1]')
doc_count = driver.find_elements_by_xpath('//*[@id="itemlistaresultados"]/span[2]')

for i in range(7): 
    
    if doc_count[i].text == 'Nenhum documento encontrado.':
        print("No documents found for " + str(item_list[i].text))

    else:
        item_list[i].text        
        inner_loop = int(doc_count[i].text.split(" ")[0])/10
        inner_loop = math.ceil(inner_loop)
        
        doc_count[i].click()

        driver.switch_to.window(driver.window_handles[0])
          
        for j in range(inner_loop):
            time.sleep(5) #sleep timer high otherwise captcha restriction
            print("Downloading Result html " + str(j) + "/" + str(inner_loop))
            
            file_name = 'STJ_' + initial_date + '-' + final_date + '_' + str(j) + '.html'
            with open(file_name, 'w', encoding = "utf-8") as f:
                f.write(driver.page_source)
                f.close()
            
            time.sleep(5)
            
            try:
                    
                Acórdão = driver.find_elements_by_xpath('//*[@id="acoesdocumento"]/a[1]')
                Acórdão_count = len(Acórdão)
              
                for count in range(Acórdão_count):
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="acoesdocumento"]/a[1]')))
                    
                    print("Starting Acórdão per page " + str(count) + "/" + str(Acórdão_count))
                    Acórdão[count].click() #Íntegra_do_Acórdão
                
                    driver.switch_to.window(driver.window_handles[1])
                    
                    time.sleep(5)
                    try:
                        html_format = driver.find_element_by_id('id_formato_html')
                        html_format.click()
                    
                    except:
                        pass
                    
                    for doc in range(1,3):
                        doc_list = '//*[@id="listaAcordaos"]/ol/li/ul/li[' + str(doc) + ']/a'
                        
                        try:
                            doc_list_elem = driver.find_element_by_xpath(doc_list)
                            print("Found " + doc_list_elem.text)
                            
                            sub_filename = doc_list_elem.text.split(r'/')[0] + "_" + str(count) + "_" + str(j) + '.html'
                            doc_list_elem.click()
                            
                            driver.switch_to.window(driver.window_handles[2])
                      #      pyautogui.hotkey('ctrl', 's')
                      #      time.sleep(1)
                      #      pyautogui.typewrite("file name")
                      #      time.sleep(1)
                      #      pyautogui.hotkey('enter')
    
                            
                            with open(sub_filename, 'w', encoding = "utf-8") as f:
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
            if j == 0:
                driver.find_elements_by_xpath('//*[@id="navegacao"]/a[2]')[1].click()
            else:
                driver.find_elements_by_xpath('//*[@id="navegacao"]/a[4]')[1].click()
            
        driver.switch_to.window(driver.window_handles[0])
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="voltarLista"]/a')))
        driver.find_element_by_xpath('//*[@id="voltarLista"]/a').click()
        

                

