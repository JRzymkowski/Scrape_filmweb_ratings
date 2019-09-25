from selenium import webdriver
import csv
import time

#driver = webdriver.Chrome(executable_path=r'D:\chromedriver_win32\chromedriver.exe')
driver = webdriver.Firefox(executable_path=r'D:\gecko\geckodriver.exe')


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def wait_for_login(driver):
    try:
        driver.get("https://www.filmweb.pl/")
        user_name = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, "user__name"))
        )
        print("Logged in as: ", user_name.text)
    except:
        pass

def get_my_username(driver):
    pass

def get_friend_list(driver):
    ##assumes driver already at the friends page
    nicks = []
    time.sleep(3)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    found = False
    friends = []
    try:
        section = driver.find_element_by_class_name("section__userFriends")

        friends = section.find_elements_by_class_name("user__body")
        print(str(len(friends)) + " found friends")
        if len(friends) > 0:
            found = True

    except NoSuchElementException:
        if not found:
            print("Friends not found")
            return []

    for f in friends:
        href, fn, ln, user_link = "not_found", "not_found", "not_found", "not_found"
        try:
            href = f.find_element_by_class_name("user__name").get_attribute("href")
            fn = f.find_element_by_class_name("user__firstName").text
            ln = f.find_element_by_class_name("user__lastName").text
        except NoSuchElementException:
            pass
        try:
            user_link = f.find_element_by_class_name("user__link").text
            if user_link != "":
                nicks.append(user_link)
            else:
                nicks.append(href.split("/")[-1])
        except NoSuchElementException:
            nicks.append(href.split("/")[-1])

    if nicks[-1] == "friends#":
        return nicks[:-1]
    else:
        return nicks

def link_to_next_page(driver):
    try:
        next_page_li = driver.find_element_by_class_name("pagination__item--next")
        next_page_link = next_page_li.find_element_by_tag_name("a")
        return next_page_link
    except NoSuchElementException:
        return None

def get_ratings(driver, friend_nick = ""):
    # driver.implicitly_wait(10)
    time.sleep(2)
    films_elements = driver.find_elements_by_class_name("myVoteBox__mainBox")
    print("number of films: ", len(films_elements))

    films_data = []
    for f in films_elements:
        try:
            title = f.find_element_by_class_name("filmPreview__title").text
            year = f.find_element_by_class_name("filmPreview__year").text
            rating = f.find_element_by_class_name("userRate__rate").text

            print(title, year, rating)
        except NoSuchElementException:
            print("Title, year or rating not found")

        try:
            tags_html = f.find_element_by_class_name("filmPreview__info--genres")
            tags = list(map(lambda x: x.text, tags_html.find_elements_by_tag_name("a")))
            print(tags)
        except NoSuchElementException:
            print("tags not located")

        films_data.append({'friend': friend_nick, 'title': title, 'year': year, 'rating': rating})

    return films_data

def get_ratings_starting(driver, url, friend_nick = ""):
    driver.get(url)
    films_data = []
    films_data = get_ratings(driver, friend_nick=friend_nick)
    next_page = link_to_next_page(driver)
    if next_page != None:
        next_page.click()
        films_data += get_ratings(driver, friend_nick=friend_nick)
    else:
        print("No link to the next page found on: ", url)

    return films_data

try:
    wait_for_login(driver)
    # films_data = get_ratings_starting(driver, "https://www.filmweb.pl/user/Mikolaj_Kastor/films?page=10", friend_nick="MK")
    #
    # fieldnames = list(films_data[0].keys())
    # with open('films.csv', 'w', newline='') as output_file:
    #     dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    #     dict_writer.writeheader()
    #     dict_writer.writerows(films_data)

    driver.get("https://www.filmweb.pl/user/j_rzymkowski/friends")
    friends = get_friend_list(driver)
    print(len(friends))
    print(friends)

finally:
    driver.quit()