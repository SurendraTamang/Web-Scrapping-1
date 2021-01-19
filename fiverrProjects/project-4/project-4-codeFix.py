# Make imports
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def translate_sentence(sentence):

    # Start a Selenium driver
    options = Options()
    options.add_argument('--headless')
    # Enable the below parameter while running on linux
    # options.add_argument('--no-sandbox')

    driver = webdriver.Chrome('./chromedriver87', chrome_options=options)

    # Reach the deepL website
    deepl_url = 'https://www.deepl.com/fr/translator'
    driver.get(deepl_url)

    # Get thie inupt_area
    input_box = driver.find_element_by_xpath("(//textarea)[1]")

    # Send the text
    input_box.clear()
    input_box.send_keys(sentence)

    # Wait for translation to appear on the web page
    time.sleep(5)

    # Grab the translated text
    contentElem = driver.find_element_by_xpath("(//textarea)[2]/following-sibling::div[1]")
    content = contentElem.get_attribute('innerHTML')

    # Quit selenium driver
    driver.quit()

    return content


if __name__ == "__main__":

    # Define text to translate
    sentence_to_translate = 'This is a translation example for my article.'
    sentence_translated = translate_sentence(sentence_to_translate)

    # Display results
    print('_'*75, '\n')
    print('Original :', sentence_to_translate)
    print('-'*75)
    print('Translation :', sentence_translated)
    print('_'*75)