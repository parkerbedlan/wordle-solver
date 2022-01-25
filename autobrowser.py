from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from math import ceil
from re import sub
import os
from time import sleep
import json
import wordle3

class_to_color = {'letter-elsewhere': 'y', 'letter-absent': 'b', 'letter-correct': 'g'}

chrome_driver_path = os.getcwd() + '\\chromedriver'
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

s=Service(ChromeDriverManager().install())
global driver
driver = webdriver.Chrome(service=s, options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(1000)
driver.get('http://foldr.moe/hello-wordl/')


keyboard_capture = driver.switch_to.active_element
game_number = 1

while True:
  rows = driver.find_elements(By.CLASS_NAME, 'Row')
  guesses = []
  guess = 'retia'
  wordle3.initialize()

  WebDriverWait(driver, 1000).until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'Row-letter'), ''))
  
  for row_index in range(6):
    print('index',row_index)
    while True:
      print('guessing', guess)
      keyboard_capture.send_keys(guess, Keys.ENTER)
      message = driver.find_element(By.TAG_NAME, 'p')
      if message and message.text == 'Not a valid word':
        guesses.pop(0)
        guess = guesses[0]
        keyboard_capture.send_keys(Keys.BACKSPACE * 5)
      elif message and message.text.startswith('You lost!'):
        # driver.find_element(By.CLASS_NAME,'Game').screenshot('screenshots/lost%s.png' % game_number)
        game_number += 1
        keyboard_capture.send_keys(Keys.ENTER)
        break
      else:
        break

    letterboxes = rows[row_index].find_elements(By.CLASS_NAME, 'Row-letter')
    if len(letterboxes[0].get_attribute('class').split()) < 2: 
      # driver.find_element(By.CLASS_NAME,'Game').screenshot('screenshots/oop%s.png' % game_number)
      game_number += 1
      keyboard_capture.send_keys(Keys.ENTER)
      break
    results = [(letterbox.text.lower(), class_to_color[letterbox.get_attribute("class").split()[1]]) for letterbox in letterboxes]
    
    won = True
    for result in results:
      if result[1] != 'g':
        won = False
        break
    if won:
      # driver.find_element(By.CLASS_NAME,'Game').screenshot('screenshots/won%s.png' % game_number)
      game_number += 1
      keyboard_capture.send_keys(Keys.ENTER)
      break

    guesses = wordle3.guess(results)
    guess = guesses[0]

sleep(4294967)
driver.quit()