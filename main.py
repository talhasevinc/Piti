import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui


buySolValue = 0.01  #This indicates how many sol you will buy every order.
buyRepeatVal = 4    #This indicates  buy transaction number sequantially.

sellPitiValue = 230_000  # Sell piti value one order
sellRepeatVal = 1        # Sell order number

waitTimeForProcess = 18 # Transaction interval

buyButtonID = 0
sellButtonID = 0
tradeButtonID = 0

confirmCoordinateX = 1794 # Wallet click X-coordinate
confirmCoordinateY = 625 # Wallet click Y-coordinate

driver = webdriver.Chrome()
driver.get("https://pump.fun/6joW6vkAE9jAKh9XQYTCpPn7tUCKWECZr7fLf7E1L8aU")

def firstEntrance():

    entranceClicked = False
    while entranceClicked == False:
        elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//button")))
        for element in elements:
            if(element.accessible_name == "[I'm ready to pump]"):
                try:
                   element.click()
                   entranceClicked = True
                except:
                   print("Not clickable...")

    print("Trade page is opened.")


def findButtonID(elements):

    global buyButtonID
    global sellButtonID
    global tradeButtonID

    buttonCount = 0
    for element in elements:

        if(element.accessible_name == "Buy"):
            buyButtonID = buttonCount
        elif(element.accessible_name == "Sell"):
            sellButtonID = buttonCount
        elif(element.accessible_name == "place trade"):
            tradeButtonID = buttonCount
        else :
            print("Unnecessary button")

        buttonCount = buttonCount + 1

    print("Buy ID: {} - SellID: {} - TradeID: {} ".format(buyButtonID, sellButtonID, tradeButtonID))
def controlStopCondition():

    countForTry = 0

    while countForTry < 10:

        numberElement = driver.find_element(By.ID, "amount")
        try:
            value = int(numberElement.get_attribute("value"))
            if (value == 50):
               while(True):
                   print("Program Stops...")
                   time.sleep(2)

            countForTry = countForTry + 1
            time.sleep(0.3)
        except:
            print("Error during value check ...")
            countForTry = countForTry + 1
            time.sleep(0.3)

def waitConnectWallet():

    while True:
        numberElement = driver.find_element(By.ID, "amount")
        try:
            value = int(numberElement.get_attribute("value"))
            if (value == 100):
               print("Wallet Connected...")
               break
        except:
            print("Wait Wallet Connect...")
            time.sleep(2)

def buySequence(elements):

        found = False
        repeatCount = 0
        buyButtonClicked = False
        confirmed = False

        print("1-)Buy operation started...")

        while(buyButtonClicked == False):
            try:
               elements[buyButtonID].click()
               print("2-)Buy button clicked...")
               buyButtonClicked = True
            except:
                print("Buy Button not active")



        while(repeatCount < buyRepeatVal):

            found = False
            while (found == False):

                try:

                    buyVal = buySolValue + random.uniform(0.000, 0.002)
                    buyVal = round(buyVal, 4)
                    numberElements = driver.find_element(By.ID, "amount")
                    numberElements.clear()
                    time.sleep(1)
                    numberElements.send_keys(str(buyVal))
                    print("3-)Buy amount setted...")
                    found = True
                except:
                    print("***Amount Element not found...***")

            tradeFindCount = 0
            confirmed = False

            try:
                elements[tradeButtonID].click()
                print("4-)Trade Button clicked...")
            except:
                print("Trade Button error...")
                continue

            time.sleep(3)

            while(confirmed == False):
               try:

                  tradeFindCount = 0
                  confirmButtons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//button")))
                  for confirmButton in confirmButtons:

                      if(confirmButton.accessible_name == "place trade"):
                         tradeFindCount = tradeFindCount + 1
                         if(tradeFindCount == 2):
                            confirmButton.click()
                            time.sleep(3)
                            print("5-)Confirm Button clicked...")
                            confirmed = True

                            pyautogui.click(x=confirmCoordinateX, y=confirmCoordinateY)
                            time.sleep(0.1)
                            pyautogui.click(x=confirmCoordinateX, y=confirmCoordinateY)
               except:
                   confirmed = False
                   print("Confirm Error")
                   time.sleep(5)

            repeatCount = repeatCount + 1
            time.sleep(waitTimeForProcess)

def sellSequence(elements):

        found = False
        repeatCount = 0
        sellButtonClicked = False

        print("****************************************")
        print("1-)Sell Process Begin...")

        while(sellButtonClicked == False):
            try:
               elements[sellButtonID].click()
               print("2-)Sell button clicked...")
               sellButtonClicked = True
            except:
                print("Sell Button not active")


        while(repeatCount < sellRepeatVal):
            found = False

            while (found == False):
                try:
                    numberElements = driver.find_element(By.ID, "amount")
                    numberElements.clear()
                    time.sleep(1)
                    numberElements.send_keys(str(sellPitiValue))
                    print("3-)Sell amount setted...")
                    found = True
                except:
                    print("***Amount Element not found...***")

            tradeFindCount = 0
            confirmed = False

            try:
                elements[tradeButtonID].click()
                print("4-)Trade Button clicked...")
            except:
                print("Trade Button error...")
                continue

            time.sleep(3)

            while (confirmed == False):

                try:
                    tradeFindCount = 0
                    confirmButtons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//button")))

                    for confirmButton in confirmButtons:
                        if (confirmButton.accessible_name == "place trade"):
                            tradeFindCount = tradeFindCount + 1
                            if (tradeFindCount == 2):
                                confirmButton.click()
                                time.sleep(3)
                                print("5-)Confirm Button clicked...")
                                confirmed = True

                                pyautogui.click(x=confirmCoordinateX, y=confirmCoordinateY)
                                time.sleep(0.1)
                except:
                    confirmed = False
                    print("Confirm Error")
                    time.sleep(5)

            repeatCount = repeatCount + 1
            time.sleep(waitTimeForProcess)

def main():

    firstEntrance()
    time.sleep(2)
    elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//button")))
    findButtonID(elements)
    waitConnectWallet()

    while(True):
       controlStopCondition()
       buySequence(elements)
       time.sleep(2)
       sellSequence(elements)
       time.sleep(2)

    # WebDriver'ı kapat
    driver.quit()

if __name__ == '__main__':
    main()