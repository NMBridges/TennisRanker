import time
import csv
import re
from selenium import webdriver

# Created by Nolan Bridges and Alex Koong
# May 30, 2021

# Creates a Chrome WebDriver from the local path of the Chrome WebDriver.
#   - It will be in a different place on every computer and does not come pre-installed.
#   - Download here (note your installed version of Chrome):
#       https://sites.google.com/a/chromium.org/chromedriver/downloads
#   - Extract the .exe from the .zip folder and place in a place you would like to keep it.
#   - Copy the path to where the chromedriver is, and paste it in the spot below.
#   - Make sure to replace any '\' with '\\' for proper syntax.
#        - e.g. "C:\\Users\\scrat\\OneDrive\\Documents\\Dev\\Dependencies\\chromedriver.exe"
PATH = ""
driver = webdriver.Chrome(PATH)

# Opens up an automated Chrome browser at the link below.
driver.get("https://www.universaltennis.com/rankings")

# Finds and clicks on the 'High School' option to ensure that
# those are the rankings that are scraped by the program.
hsButton = driver.find_element_by_xpath("//*[@id=\"myutr-app-wrapper\"]/div[3]/div/div[5]/div[2]/div/div/div[1]/div[1]/div/span[4]")
hsButton.click()
time.sleep(2)
hsButton.click()

# Instantiates a blank list of names to be added onto as
# the program scrapes universaltennis.com.
names = []

# Creates a new .csv file to write the data to.
with open('ranks.csv', 'w', newline='') as ranks:
    # Creates a CSVWriter object that allows writing to a .csv file.
    ranksWriter = csv.writer(ranks, delimiter=',')

    # Writes the proper headers to the .csv file.
    ranksWriter.writerow(["Rank", "Name", "Class"])

    time.sleep(5)

    # The number of pages to cycle through. Each page contains 100 players.
    #    Precondition: 1 < pages <= 25
    pages = 2

    # Cycles through a preset amount of pages, scraping the
    # names of the players and adding them to the 'names' list.
    for x in range(1, pages + 1):
        # Finds and clicks on the dropdown element that selects the proper range of players.
        #       i.e. Clicks on '201-300' from the dropdown so
        #            that the 201st-300th ranked players show up.
        setOfHundred = driver.find_element_by_xpath(f"//*[@id=\"myutr-app-wrapper\"]/div[3]/div/div[5]/div[2]/div/select/option[{x}]")
        setOfHundred.click()

        time.sleep(4)

        # Cycles through each name shown on the page and adds it to the 'names' list.
        for i in range(1, 101):
            playerName = driver.find_element_by_xpath(f"//*[@id=\"myutr-app-wrapper\"]/div[3]/div/div[5]/div[4]/div[{i}]/a/div/div/div[2]/div/span[1]").text
            names.append(playerName)

    # Once all the pages are scraped and the names are found, the program will
    # now go to tennisrecruiting.net to find the age/class of players.
    
    # First, it will open up the automated Chrome browser at the following link:
    driver.get("https://www.tennisrecruiting.net/player.asp")

    # Then the program will go through every name in 'names' and find
    # their tennisrecruiting.net profile.
    for index, name in enumerate(names):
        # Finds the search box element, inputs the player's name, and hits enter to search.
        textbox = driver.find_element_by_xpath("//*[@id=\"searchBox\"]/table/tbody/tr[2]/td[1]/input")
        textbox.send_keys(name)
        textbox.send_keys(webdriver.common.keys.Keys.RETURN)

        time.sleep(0.9)

        # Determines whether or not searching/querying for the player
        # immediately lands the browser on their webpage.
        onPage = False
        contents = driver.find_elements_by_xpath("//*[@id=\"CenterColumn\"]/h1")
        if len(contents) > 0:
            if(contents[0].text == "PLAYER RECORD"):
                # If the webpage has this element (which is unique to player profiles),
                # the program has determined that it is on the player's page.
                onPage = True

        # If the program is not on a player page (i.e. there are multiple people with
        #   similar names), it will select the first result from the search results.
        # The first result is generally the best matching name and/or highest
        #   ranked player, so this works most of the time. Manual corrections are needed.
        # If there are no results, it leaves the graduation year blank and adds
        #   the rank and name to the .csv file before continuing.
        if not onPage:
            links = driver.find_elements_by_xpath("//*[@id=\"CenterColumn\"]/div[2]/table/tbody/tr[2]/td[1]/b/a")
            if len(links) > 0:
                # Find highest ranked search result of player. Tie: whichever is first.
                playersWithIcons = driver.find_elements_by_tag_name('img')
                
                sixStars = []
                fiveStars = []
                fourStars = []
                threeStars = []
                
                # Goes through each player with a special icon and sorts them by their star ranking
                for plyr in playersWithIcons:
                    srcLink = plyr.get_attribute('src')
                    if srcLink == 'https://www.tennisrecruiting.net/img/6-starB.gif':
                        sixStars.append(plyr)
                    elif srcLink == 'https://www.tennisrecruiting.net/img/5-starB.gif':
                        fiveStars.append(plyr)
                    elif srcLink == 'https://www.tennisrecruiting.net/img/4-starB.gif':
                        fourStars.append(plyr)
                    elif srcLink == 'https://www.tennisrecruiting.net/img/3-starB.gif':
                        threeStars.append(plyr)
                
                if len(sixStars) > 0:
                    # Find first six star
                    firstSixStar = sixStars[0].find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('./td[1]/b/a')
                    firstSixStar.click()
                elif len(fiveStars) > 0:
                    # Find first five star
                    firstFiveStar = fiveStars[0].find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('./td[1]/b/a')
                    firstFiveStar.click()
                elif len(fourStars) > 0:
                    # Find first four star
                    firstFourStar = fourStars[0].find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('./td[1]/b/a')
                    firstFourStar.click()
                elif len(threeStars) > 0:
                    # Find first three star
                    firstThreeStar = threeStars[0].find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('./td[1]/b/a')
                    firstThreeStar.click()
                else:
                    # No sufficiently ranked player found. Manual correction needed. Will skip.
                    # Adds the player's rank and name to the .csv file.
                    print(f"{index + 1}: {name}")
                    ranksWriter.writerow([f"{index + 1}", f"{name}", ""])

                    # Skips the remaining code for the remaining iteration of the loop.
                    continue

                time.sleep(0.9)
            else:
                # Adds the player's rank and name to the .csv file.
                print(f"{index + 1}: {name}")
                ranksWriter.writerow([f"{index + 1}", f"{name}", ""])

                # Skips the remaining code for the remaining iteration of the loop.
                continue

        # From the player's page, it will find their graduation year.
        graduationYear = re.search(r'[12]\d{3}', driver.find_element_by_xpath("//*[@id=\"CenterColumn\"]/table[1]/tbody/tr/td[2]/table/tbody/tr[3]/td[2]/div[3]").text).group(0)
        
        # Adds the player's rank, name, and class to the .csv file.
        print(f"{index + 1}: {name}, class of {graduationYear}")
        ranksWriter.writerow([f"{index + 1}", f"{name}", f"{graduationYear}"])

# Once the process is complete, the automated Chrome browser will close and the .csv file will be ready to use.
driver.close()