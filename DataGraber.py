import time
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import random
import selenium
from selenium.webdriver.common.by import By
from functools import partial
from selenium.webdriver.common.keys import Keys



def update_progressbar(p, root):
    p.step()
    root.update()


def create_graph(search_req, progressbar, root, filename):
    nfts = []
    path = filename#"/usr/lib/chromium-browser/chromedriver"
    #search_req = "solwarriors"  # SolWarriors
    # search_req = "solwizards"
    # search_req = "solarchers"
    base_url = "https://solanart.io/collections/"

    # variables
    batch_size = 100
    tries = 3

    # Getting data from Solanart
    print("Getting data...")
    op = webdriver.ChromeOptions()
    op.add_argument("--enable-javascript")
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
    op.add_argument(f'user-agent={user_agent}')

    op.add_argument("--window-size=1920,1080")
    op.add_argument("--headless")

    if search_req == "solwarriors":
        search_req = "solantasy"


    # Solanart
    if not search_req == "solarchers":
        browser = webdriver.Chrome(path, options=op)
        browser.get(base_url+search_req)
        time.sleep(5)
        for i in range(tries):
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(random.randrange(0,300)/100+1)
        html = browser.page_source


        soup = BeautifulSoup(html, 'lxml')
        availables = soup.find_all(class_="ResponsiveCardsGrid_grid_card__hNE_f nft")
        for available in availables:
            #for i in range(999):
            if available.find(class_="NFTCard_cardBottom___u34Y"):#f"MuiChip-label-{i}"):
                nfts.append([available.find(class_="NFTCard_nft_name__6gcwN").contents[0].split("#")[1], str(available.find(class_=f"NFTCard_nft_price__0oD5_").contents[0])[5:-6]])
        browser.close()

    update_progressbar(progressbar, root)

    # Magic Eden
    if search_req == "solantasy":
        search_req = "solantasy_solwarriors"
    elif search_req == "solarchers":
        search_req = "solantasy_solarchers"

    base_url = "https://www.magiceden.io/marketplace/"

    browser = webdriver.Chrome(path, options=op)
    browser.get(base_url+search_req)
    time.sleep(5)
    for i in range(tries*2):
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(random.randrange(0,300)/100)
    html = browser.page_source


    soup = BeautifulSoup(html, 'lxml')
    availables = soup.find_all(class_="tw-p-0 mb-4 grid-card grid-card__main tw-rounded-lg")
    for available in availables:
        nfts.append([available.find(class_="mb-0 tw-truncate grid-card__title").contents[0].split("#")[1], str(available.find(class_=f"my-2 card__price tw-truncate").contents[0])[6:-11]])
    browser.close()

    update_progressbar(progressbar, root)
    # Fractal
    base_url = "https://www.fractal.is/solantasy?"
    if search_req == "solwizards":
        search_req_ = "query=SolWizard&page=1&configure[filters]=forSale%3Atrue AND collection%3A5755374237908992&configure[hitsPerPage]=30"
    elif search_req == "solantasy_solwarriors":
        search_req_ = "query=SolWarrior&page=1&configure[filters]=forSale%3Atrue AND collection%3A5755374237908992&configure[hitsPerPage]=30"
    elif search_req == "solantasy_solarchers":
        search_req_ = "query=SolArcher&page=1&configure[filters]=forSale%3Atrue AND collection%3A5755374237908992&configure[hitsPerPage]=30"


    browser = webdriver.Chrome(path, options=op)
    browser.get(base_url+search_req_)
    time.sleep(5)
    for i in range(tries):
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        try:
            browser.find_element_by_xpath('//button[text()="Show more"]').click()
        except selenium.common.exceptions.NoSuchElementException as e:
            pass
        time.sleep(random.randrange(0,300)/100)
    html = browser.page_source


    soup = BeautifulSoup(html, 'lxml')
    availables = soup.find_all(class_="card-body")
    for available in availables:
        nfts.append([available.find(class_="font-bold").contents[0].split("#")[1], str(available.find(class_=f"bg-base-200 rounded-lg w-full p-2 text-center mt-3").contents[0])[:-4]])
    browser.close()

    if search_req == "solantasy_solwarriors":
        search_req = "solwarriors"
    if search_req == "solantasy_solarchers":
        search_req = "solarchers"

    update_progressbar(progressbar, root)
    # Getting rarity of each SolWIzards (SolWizard Number --> Rarity Rank)
    print("Getting rarity...")
    rarity = {}
    with open(f"{search_req[:-1]}.txt", "r") as file:
        all_ranks = file.readlines()
        for a in all_ranks:
            rarity[a.split(" ")[0]] = a.strip().split(" ")[1]



    # Adding rarity to shop listenings
    for i in range(len(nfts)):
        nft = nfts[i]
        ranks = rarity[nft[0]]
        nfts[i].append(ranks)

    nfts.sort(key=lambda nfts:int(nfts[2]))
    x,y,z = [],[],[]
    [(x.append(int(r)), y.append(float(k)), z.append(l))for (l,k,r) in nfts]



    # Getting sales
    sales = []

    #Solanart
    if search_req == "solwarriors":
        search_req = "solantasy"
    if search_req != "solarchers":
        base_url = "https://solanart.io/collections/"
        if not search_req == "solarchers":
            browser = webdriver.Chrome(path, options=op)
            browser.get(base_url+search_req)
            time.sleep(5)
            try:
                btns = browser.find_element(By.CSS_SELECTOR, '[data-testid="close-button"]')
                btns.click()
                time.sleep(2)
                btns = browser.find_element(By.CLASS_NAME, "Collection_banner__TDCo3")
                btns = btns.find_elements(By.CSS_SELECTOR, "button")[1]
                btns.click()
                time.sleep(3)
            except selenium.common.exceptions.NoSuchElementException as e:
                print(e)

            html = browser.page_source


            soup = BeautifulSoup(html, 'lxml')
            availables = soup.find_all("tr")
            for available in availables:
                if available.find(class_="ml-5 group-hover:text-solanartGreen"):
                    nbr = available.find(class_="ml-5 group-hover:text-solanartGreen").contents[0].split("#")[1]
                    price = available.find_all("td")[2].contents[0]
                    date = available.find(class_="py-1 px-3 rounded-md whitespace-nowrap text-center").contents[0]
                    if not "month" in date:
                        sales.append([int(nbr), float(price), int(rarity[nbr])])
            browser.close()

    update_progressbar(progressbar, root)
    #Magic Eden
    if search_req == "solantasy":
        search_req = "solantasy_solwarriors"
    elif search_req == "solarchers":
        search_req = "solantasy_solarchers"

    base_url = "https://magiceden.io/marketplace/"

    browser = webdriver.Chrome(path, options=op)
    browser.get(base_url+search_req)
    time.sleep(5)

    try:
        btns = browser.find_element(By.XPATH, '//span[text()="Activity"]')
        btns.click()
        time.sleep(3)
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(5)
        btns = browser.find_element(By.CSS_SELECTOR, '[class="me-dropdown-container ms-auto me-table__pagination-page-size"]')
        btns.click()
        time.sleep(1)
        btns = browser.find_element(By.XPATH, '//div[text()="100"]')
        btns.click()
        still_left = True

        while still_left:
            html = browser.page_source
            soup = BeautifulSoup(html, 'lxml')
            availables = soup.find_all("tr")
            part = soup.find_all("div", class_="me-table__pagination d-flex align-items-center mt-2")[0]
            strong = part.find("strong")
            current = int(strong.contents[0].split(" ")[0])
            max = int(strong.contents[0].split(" ")[2])
            if current == max:
                still_left = False
            for available in availables:
                if len(available.find_all("td")) == 7:
                    nbr = available.find_all("td")[1].find("a").contents[0].split("#")[1]
                    price = available.find_all("td")[5].contents[0][:-4]
                    date = available.find_all("td")[4].contents[0]

                    if not "month" in date:
                        sales.append([int(nbr), float(price), int(rarity[nbr])])
                    else:
                        still_left = False
            btns = browser.find_element(By.XPATH, f'//input[@value="1"]')
            btns.clear()
            time.sleep(0.25)

            if still_left:
                btns.send_keys(str(current+1))

            time.sleep(1)
    except selenium.common.exceptions.NoSuchElementException as e:
        print(e)

    browser.close()

    update_progressbar(progressbar, root)
    # Fractal
    base_url = "https://www.fractal.is/solantasy?"


    browser = webdriver.Chrome(path, options=op)
    browser.get(base_url)
    time.sleep(5)

    try:
        btns = browser.find_element(By.XPATH, '//div[text()="Sales"]')
        btns.click()
        time.sleep(1)
        still_left = True
        while still_left:
            time.sleep(1)
            html = browser.page_source
            soup = BeautifulSoup(html, 'lxml')
            availables = soup.find_all("tr")
            for i,available in enumerate(availables):
                if i != 0:
                    number = available.find_all("div", class_="font-bold")[0].contents[0]
                    price = available.find_all("td")[3].contents[0][:-4]
                    date = available.find("time").contents[0]
                    if not "month" in date:
                        if number.split("#")[0].lower()[:-1] == search_req.lower()[:-1]:
                            sales.append([int(number.split("#")[1]), float(price), int(rarity[number.split("#")[1]])])
                    else:
                        still_left = False
            btns = browser.find_element(By.XPATH, '//button[text()="Next"]')
            btns.click()
            time.sleep(1)

    except selenium.common.exceptions.NoSuchElementException as e:
        print(e)

    browser.close()

    update_progressbar(progressbar, root)
    print("Sales in den letzten 4 Wochen:" +str(len(sales)))


    df = pd.DataFrame(map(lambda x,y,z:[x,y,z],x,y,z))
    df.columns = ["Rarity", "Price", "Number"]

    fig, ax = plt.subplots()
    if search_req == "solantasy_solwarriors":
        search_req = "SolWarriors"
    elif search_req == "solantasy_solarchers":
        search_req = "SolArchers"
    else:
        search_req = "SolWizards"
    plt.title(search_req)
    #fig.suptitle(search_req)
    #plt.figure(num=search_req)
    plt.autoscale(enable=True, axis='both')
    plt.ylabel("Price")
    plt.xlabel("Rarity Rank")

    font_size = 10


    sales = pd.DataFrame(sales)
    sales.columns = ["Number", "Price", "Rarity"]
    coordinates = []
    shown = False

    def on_key(event):
        #global shown
        if str(event.key) == "m":
            for text in coordinates:
                text.set_visible(not text.get_visible())
                plt.draw()
            """if not shown:
                for text in coordinates:
                    text.set(visible=True)
                    plt.draw()
                shown = True
            else:
                for text in coordinates:
                    text.set(visible=False)
                    plt.draw()
                shown = False"""


    cid = fig.canvas.mpl_connect('key_press_event', on_key)

    ax.plot(df["Rarity"], df["Price"], 'o', markersize=0.5)

    ax.plot(sales["Rarity"], sales["Price"], "ro", markersize=0.5)

    for i, j, n in zip(df["Rarity"], df["Price"], df["Number"]):
        coordinates.append(
            plt.text(i, j + 0.01, '({}, {})'.format(n, j), {"fontsize": font_size, "visible": False}))
    for i, j, n in zip(sales["Rarity"], sales["Price"], sales["Number"]):
        coordinates.append(
            plt.text(i, j + 0.01, '({}, {})'.format(n, j), {"fontsize": font_size, "visible": False}))

    ax.plot()

    plt.show()

#create_graph("solwizards")
