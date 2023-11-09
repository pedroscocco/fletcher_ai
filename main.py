import selenium_wa_layer
import time

selenium_wa_layer.start_selenium()

last_message = selenium_wa_layer.wait_new_message_element()

print(selenium_wa_layer.get_message_details(last_message))

time.sleep(10)

selenium_wa_layer.stop()

