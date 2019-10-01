import get_films
import csv
from selenium import webdriver

# path to webdriver executable
path_to_webdriver = r'D:\gecko\geckodriver.exe'
# nick of your friend on filmweb.pl
friends_nick = 'narmacil'

driver = webdriver.Firefox(executable_path=path_to_webdriver)

try:
    get_films.wait_for_login(driver)
    my_username = get_films.get_my_username(driver)
    print("Detected username: ", my_username)
    films_data = get_films.get_ratings_by(driver, friends_nick)

    fieldnames = list(films_data[0].keys())
    with open('films.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows(films_data)


finally:
    driver.quit()