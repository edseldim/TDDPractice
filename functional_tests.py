from selenium import webdriver

browser = webdriver.Firefox(firefox_binary="C:\Program Files\Mozilla Firefox\\firefox.exe")
browser.get('http://localhost:8000')

assert 'Django' in browser.title