import json
import os

from selenium import webdriver
from selenium.webdriver.common.by import By


def save_to_json_file(file_name: str, data: dict):
    try:
        with open(f"{file_name}", "r") as data_file:
            # Reading old data
            data = json.load(fp=data_file)
    except FileNotFoundError:
        with open(f"{file_name}", "w") as data_file:
            # Saving updated data
            json.dump(data, data_file, indent=4)
    else:
        # Updating old data with new data
        data.update(data)
        
        with open(f"{file_name}", "w") as data_file:
            # Saving updated data
            json.dump(data, data_file, indent=4)


def get_links(driver: webdriver, url: str, output_file: dict):
    driver.get(url)
    data = driver.find_elements(by=By.CSS_SELECTOR, value="td.cont tr.on")
    for td in data:
        # print(td.get_attribute("innerHTML"))
        name = td.find_element(by=By.TAG_NAME, value="span").text
        link = td.find_element(by=By.TAG_NAME, value="a").get_attribute("href")
        size = td.find_element(by=By.CSS_SELECTOR, value="td.size")
        if size.text == "-":
            output_file["folders"][name] = link
        else:
            output_file["files"][name] = link


def download_file(name: str, download_link: str):
    cmd = f"wget {download_link}";
    os.system(cmd)


def upload_to_telegram(path_of_file: str):
    cmd = f"telegram-upload -d \"{path_of_file}\""
    os.system(cmd)


if __name__ == '__main__':
    file_name = "data.json"
    links_dic = {
        "folders": {},
        "files"  : dict()
    }
    
    if os.path.exists(f"./{file_name}"):
        with open(f"{file_name}", "r") as data_file:
            links_dic = json.load(fp=data_file)
    
    if links_dic.values():
        pass
    else:
        url = "https://filedn.com/lCs4UeMU1vFHSAFbhydtia5/media/TV/The%20Nanny/"
        chrome_driver_path = "C:/Program Files/Google/Chrome/chromedriver.exe"
        driver = webdriver.Chrome(executable_path=chrome_driver_path)
        get_links(driver, url, links_dic)
        for link in links_dic["folders"].values():
            get_links(driver, link, output_file=links_dic)
        links_dic.pop("files")
        save_to_json_file("data", links_dic)
    
    for name, link in dict(links_dic).items():
        download_file(name, link)
        upload_to_telegram(f"./{name}")
        links_dic.pop(name)
        save_to_json_file(file_name, links_dic)
