# import zipfile
# path_to_zip_file='F:\searchEngine\chromedriver_win32.zip'
# directory_to_extract_to='F:\searchEngine'
# zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
# zip_ref.extractall(directory_to_extract_to)
# zip_ref.close()


from selenium import webdriver

driver = webdriver.Chrome('F:\searchEngine\chromedriver.exe')
driver.get('http://web.whatsapp.com')

# name = input('Enter the name of user or group : ')
# msg = input('Enter the message : ')
# count = int(input('Enter the count : '))
name='sangavee'
msg='hi from python'
count=2
#Scan the code before proceeding further
#input('Enter anything after scanning QR code')

# user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
# user.click()
#//*[@id="pane-side"]/div/div/div/div[1]/div/div/div[2]/div[1]/div[1]/span/span
#<span dir="auto" title="Gowtham A" class="_1wjpf">Gowtham A</span>
# msg_box = driver.find_element_by_class_name('input-container')

# for i in range(count):
#     msg_box.send_keys(msg)
#     driver.find_element_by_class_name('compose-btn-send').click()
user=driver.find_element_by_css_selector("[title^='{}']".format(name))

#user=driver.find_element_by_class_name('_1wjpf')
#user = driver.find_element_by_xpath('//*[@id="pane-side"]/div/div/div/div[15]/div/div/div[2]/div[1]/div[1]/span/span[@title = "{}"]'.format(name))
user.click()

msg_box = driver.find_element_by_class_name('_2S1VP')

for i in range(count):
    msg_box.send_keys(msg)
    button = driver.find_element_by_class_name('_2lkdt')
    button.click()
