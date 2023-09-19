from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import re
import time


def extract_number_from_string(text):
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    else:
        return None


class WeatherShopPage:
    def __init__(self, driver):
        self.driver = driver

    def get_temperature(self):
        temperature_element = self.driver.find_element(By.ID, "temperature")
        temperature_int = extract_number_from_string(temperature_element.text)
        return temperature_int

    def click_moisturizers(self):
        self.driver.find_element(By.CSS_SELECTOR, 'a[href="/moisturizer"] > button.btn.btn-primary').click()

    def click_sunscreens(self):
        self.driver.find_element(By.CSS_SELECTOR, 'a[href="/sunscreen"] > button.btn.btn-primary').click()


class ProductPage:
    def __init__(self, driver):
        self.driver = driver

    def select_cheapest_product(self, key_word):
        product_elements = self.driver.find_elements(By.XPATH, f"//p[contains(translate(text(),"
                                                               f"'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
                                                               f"'abcdefghijklmnopqrstuvwxyz'), '{key_word}')]")
        prices = []
        if len(product_elements) > 1:
            for product in product_elements:
                price_element = product.find_element(By.XPATH, 'following-sibling::p')
                price = extract_number_from_string(price_element.text)
                prices.append((product, price))

            prices.sort(key=lambda x: x[1])
            least_expensive_product = prices[0][0]
            add_button = least_expensive_product.find_element(By.XPATH, 'following-sibling::button')
            add_button.click()
        elif len(product_elements) == 1:
            product = product_elements[0]
            add_button = product.find_element(By.XPATH, 'following-sibling::button')
            add_button.click()
        else:
            # no products were found that have the key word
            pass

    def click_cart_button(self):
        self.driver.find_element(By.XPATH, "//button[@onclick='goToCart()']").click()


class CartPage:
    def __init__(self, driver):
        self.driver = driver

    def fill_payment_details(self, email, card_number, expiration_date, cvc_code):
        try:
            pay_with_card_button = self.driver.find_element(By.CSS_SELECTOR, 'button.stripe-button-el')
            pay_with_card_button.click()

            self.switch_to_stripe_iframe()
            # Wait for the email input field to become visible
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.ID, 'email')))

            self.fill_input_field('email', email)
            self.fill_input_field('card_number', card_number)
            self.fill_input_field('cc-exp', expiration_date)
            self.fill_input_field('cc-csc', cvc_code)

            pay_button = self.driver.find_element(By.ID, 'submitButton')
            pay_button.click()
            time.sleep(5)  # Wait for payment to process

            self.switch_to_default_content()
        except Exception as e:
            print("An error occurred while checkout, please try again:", str(e))

    def switch_to_stripe_iframe(self):
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.NAME, 'stripe_checkout_app')))

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def fill_input_field(self, field_id, value):
        input_element = self.driver.find_element(By.ID, field_id)
        self.driver.execute_script(f"arguments[0].value = '{value}';", input_element)


class ConfirmationPage:
    def __init__(self, driver):
        self.driver = driver

    def verify_payment_success(self):
        try:
            print("verifying your payment status ..")
            payment_status_message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'PAYMENT')]"))
            )

            if payment_status_message.text == "PAYMENT SUCCESS":
                print("Your payment was successful. You should receive a follow-up call from our sales team.")
            elif payment_status_message.text == "PAYMENT FAILED":
                print("Oh, oh! Your payment did not go through. Please bang your head against a wall, curse the "
                      "software gods and then try again.")
        except Exception as e:
            print("An error occurred while verifying payment status:", str(e))


def main():
    # Initialize the WebDriver (choose your preferred browser)
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--headless")

    # run the webdriver headless by default in Docker
    my_driver = webdriver.Firefox(firefox_options)
    # run the webdriver with GUI automation
    #my_driver = webdriver.Firefox()
    weather_shop_page = WeatherShopPage(my_driver)

    # Navigate to the web application
    print("Navigating to the WeatherShop...")
    my_driver.get("http://weathershopper.pythonanywhere.com/")

    temperature = weather_shop_page.get_temperature()
    print(f"Temperature = '{int(temperature)}'")

    product_page = ProductPage(my_driver)
    cart_page = CartPage(my_driver)
    payment_status_page = ConfirmationPage(my_driver)

    if int(temperature) < 19:
        print("Buy Moisturizers")
        weather_shop_page.click_moisturizers()
        product_page.select_cheapest_product('aloe')
        product_page.select_cheapest_product('almond')
    elif int(temperature) > 34:
        print("Buy Sunscreens")
        weather_shop_page.click_sunscreens()
        product_page.select_cheapest_product('spf-30')
        product_page.select_cheapest_product('spf-50')

    product_page.click_cart_button()
    print("Payment...")
    cart_page.fill_payment_details('rim.zaatour1996@gmail.com', '5555555555554444', '12/24', '000')
    payment_status_page.verify_payment_success()

    # Close the browser window
    my_driver.quit()


if __name__ == "__main__":
    main()
