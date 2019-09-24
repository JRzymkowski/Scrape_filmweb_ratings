from selenium import webdriver
import csv
import time

#driver = webdriver.Chrome(executable_path=r'D:\chromedriver_win32\chromedriver.exe')
driver = webdriver.Firefox(executable_path=r'D:\gecko\geckodriver.exe')


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

try:
    driver.get("https://www.filmweb.pl/")
    user_name = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CLASS_NAME, "user__name"))
    )
    print("Logged in as: ", user_name.text)

    driver.get("https://www.filmweb.pl/user/Mikolaj_Kastor/films")
    friend_nick = "Mikolaj_Kastor"
    #driver.implicitly_wait(10)
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

    fieldnames = list(films_data[0].keys())
    with open('films.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows(films_data)


finally:
    driver.quit()