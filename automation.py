from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def debug_board(debug=False):
    options = Options()
    options.debugger_address = "127.0.0.1:9222"
    driver = webdriver.Chrome(options=options)
    map = [[-1] * 9 for _ in range(9)]
    exposed_cells={}
    cells = driver.find_elements(By.XPATH,"//*[contains(@id,'cell')]")
    for i in range(0,len(cells)):
        #check for exposed numbers
        if(cells[i].get_attribute("class").count('hdd_opened')):
            x=int((cells[i].get_attribute("id"))[-1])
            y=int((cells[i].get_attribute("id"))[-3])
            map[x][y]=int((cells[i].get_attribute("class"))[-1])
            exposed_cells[(x,y)]=map[x][y]
        # check for flags
        elif(cells[i].get_attribute("class").count('hdd_flag')):
            x=int((cells[i].get_attribute("id"))[-1])
            y=int((cells[i].get_attribute("id"))[-3])
            map[x][y]=-2
            exposed_cells[(x,y)]=-2
    if debug:
        for i in map:
            print(" ".join(f"{x:>2}" for x in i))
    return map,exposed_cells