import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import e_mail, passw


class Pet:
   def __init__(self, name, type, age):
      self.name = name
      self.type = type
      self.age = age


@pytest.fixture(autouse=True)
def testing():
   driver = webdriver.Chrome('/projects/selenium/chromedriver.exe')
   pytest.driver = driver
   # Переходим на страницу авторизации
   pytest.driver.maximize_window()
   pytest.driver.get('http://petfriends.skillfactory.ru/login')


   yield

   pytest.driver.quit()




def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element(By.ID, "email").send_keys(e_mail)
    # Вводим пароль
    pytest.driver.find_element(By.ID, "pass").send_keys(passw)
    # Нажимаем на кнопку входа в аккаунт
    WebDriverWait(pytest.driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    #time.sleep(3)
    # Нажимаем на кнопку "Мои питомцы"
    WebDriverWait(pytest.driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a')))
    pytest.driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h2').text != ""

    # Находим количество питомцев
    pets_numb = int(pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(":")[1])
    print('Количество питомцев:', pets_numb)
    all_pets = pytest.driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')
    print(len(all_pets))
    # Проверяем, что присутствуют все питомцы
    assert pets_numb == len(all_pets)

    # Находим карточки всех питомцев
    pets = pytest.driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]')
    pets_list = [pet.text.split('\n') for pet in pets][0][1::2]

    pets_list = [Pet(pet.split(' ')[0], pet.split(' ')[1], pet.split(' ')[2]) for pet in pets_list]
    print(pets_list)


    for pet in pets_list:
        print(pet.name, pet.type, pet.age)


    pets_data = [pet.text for pet in all_pets]
    uniq_pets = set(pets_data)
    # Проверяем, что у всех питомцев разные имена
    assert len(pets_data) == len(uniq_pets)
    # Проверяем, наличие повторяющихся питомцев
    not_uniq_pets = set([pet.text for pet in all_pets if pets_data.count(pet.text) > 1])
    print(f'Повторящиеся питомцы {not_uniq_pets}')


def test_name_age_type_image_of_pets():
    # Вводим email
    pytest.driver.find_element(By.ID, "email").send_keys(e_mail)
    # Вводим пароль
    pytest.driver.find_element(By.ID, "pass").send_keys(passw)
    # Нажимаем на кнопку входа в аккаунт
    WebDriverWait(pytest.driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    #time.sleep(2)
    # Нажимаем на кнопку "Мои питомцы"
    WebDriverWait(pytest.driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a')))
    pytest.driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()
    #time.sleep(2)
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element(By.TAG_NAME, 'h2').text != ""

    # Собираем найденные парметры
    pytest.driver.implicitly_wait(2)
    images = pytest.driver.find_elements(By.XPATH,'//img[@class="card-img-top"]')
    pytest.driver.implicitly_wait(2)
    names = pytest.driver.find_elements(By.XPATH,'//h5[@class="card-title"]')
    pytest.driver.implicitly_wait(2)
    descriptions = pytest.driver.find_elements(By.XPATH, '//p[@class="card-text"]')

    count = 0

    # Перебираем список
    for i in range(len(names)):
        # Проверка  существования фотографии в карточке
        assert images[i].get_attribute('src') != ''
        if images[i].get_attribute('src'):
            count+=1
            print(images[i])
        print(count)
        # Проверяем, что у половины питомцев есть фото
        assert count >= len(images) / 2
        # Проверяем, что у всех питомцев есть имя и описание
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        # Проверяем, что страница в карточке содержит и вид, и возраст питомца.
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0












