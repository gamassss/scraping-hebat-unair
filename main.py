import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService

# get json from key.json
with open('key.json', 'r') as f:
    config = json.load(f)

# enable this code below if you face spawn ENONT issue use linux
# options = Options()
# options.add_argument("--no-sandbox");
# options.add_argument("--headless");
# options.add_argument("--disable-dev-shm-usage");

service = ChromeService(executable_path=ChromeDriverManager().install())

# enable this code below if you face spawn ENONT issue use linux
# driver = webdriver.Chrome(service=service, options=options)

driver = webdriver.Chrome(service=service)

driver.get("https://hebat.elearning.unair.ac.id/")

# cari element login untuk membuka form login
login_button = driver.find_element(By.CSS_SELECTOR, "a.login-open")
login_button.click()

# cari field username dan password dan isi dengan nim dan password
username_field = driver.find_element(By.NAME, "username")
username_field.send_keys(config["NIM"])
password_field = driver.find_element(By.NAME, "password")
password_field.send_keys(config["pass_hebat"])

# submit form and log in
login_form = driver.find_element(By.ID, "header-form-login")
login_form.submit()

# tunggu 10 detik sampai loading selesai
wait = WebDriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, 'div.pl-0.list-group.list-group-flush')))

# cari element nama hari terdekat
nama_hari = driver.find_element(By.CSS_SELECTOR, "h5.h6.mt-3.mb-0").text

# cari element tugas
hari_terdekat = driver.find_element(
    By.CSS_SELECTOR, "div.pl-0.list-group.list-group-flush")

# child dari tugas terdekat
tugas_pada_hari_terdekat = hari_terdekat.find_elements(
    By.CSS_SELECTOR, "div.border-0")

# get jumlah tugas
jumlah_tugas = str(len(tugas_pada_hari_terdekat))

data = {
    "nama_hari": nama_hari,
    "tugas": []
}

tugas = []

for items in tugas_pada_hari_terdekat:
    # get jam
    text_jam = items.find_element(By.XPATH, "./div/small").text

    # get title tugas
    nama_tugas = str(items.find_element(
        By.XPATH, "./div/div[2]/a").get_attribute("title"))
    words = nama_tugas.split()
    new_words = words[:-2]
    new_nama_tugas = " ".join(new_words)

    # assign value
    object_tugas = {}
    object_tugas["nama_tugas"] = new_nama_tugas
    object_tugas["deadline"] = text_jam

    tugas.append(object_tugas)

data["tugas"] = tugas
json_tugas = json.dumps(data)
print(json_tugas)