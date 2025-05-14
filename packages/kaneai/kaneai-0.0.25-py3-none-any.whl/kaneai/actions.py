import logging
import re
from selenium import webdriver
from .config import operations_meta_data
from .utils import (
    execute_api,
    handle_unresolved_operations,
    heal_query,
    replace_secrets_in_dict,
    string_to_float,
    vision_query,
    execute_js,
    lambda_hooks,
    perform_assertion,
    replace_variables_in_script,
    get_downloads_file_path,
    get_variable_value,
    access_value,
    smart_network_wait,
    set_last_action_timestamp,
    get_last_action_timestamp, canvas_autoheal_wrapper, NETWORK_WAIT_FOR_ALL_ACTIONS
)

# Configure logging
logger = logging.getLogger(__name__)

from .webdriver_utils import (
    click,
    find_element,
    go_to_url,
    retry,
    switch_to_frame,
    is_action_unresolved
)

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import base64
import os


def ui_action(driver: webdriver.Chrome, operation_index: str):
    # Get operation data from the singleton
    from .config import get_metadata
    metadata = get_metadata()
    op_data = metadata.get(operation_index, {})

    if not op_data:
        raise ValueError(f"No operation found for index: {operation_index}")

    if NETWORK_WAIT_FOR_ALL_ACTIONS:
        smart_network_wait(driver=driver, start_timestamp=get_last_action_timestamp())

    # Handle sub_instruction_obj
    sub_instruction_obj = op_data.get('sub_instruction_obj', {})
    if isinstance(sub_instruction_obj, str):
        import json
        sub_instruction_obj = json.loads(sub_instruction_obj)

    # Check if operation is unresolved or needs resolution based on variables
    if 'unresolved' in op_data or is_action_unresolved(op_data.get('operation_type', ''), sub_instruction_obj):
        print("Resolving unresolved operation")
        if 'operation' in sub_instruction_obj:
            op_data['operation_intent'] = get_variable_value(sub_instruction_obj['operation'], metadata.get('variables', {}))
        if 'agent' in sub_instruction_obj:
            op_data['agent'] = sub_instruction_obj['agent']
        print("Operation Intent: ", op_data.get('operation_intent', ''))
        handle_unresolved_operations(operation_index, driver)

    max_retries = op_data.get('max_retries', 0)
    if max_retries == 0:
        max_retries = 3

    action: str = op_data.get('operation_type')
    if not action:
        raise ValueError(f"No operation type found for index: {operation_index}")

    locators = op_data.get('locator', None)
    frame_info = op_data.get('frame', None)
    user_vars_list = op_data.get('user_variables', '')
    selector = op_data.get('selector', None)
    clicks_order_code = op_data.get('clicks_order_code', "se_js_ac")
    
    # Validate clicks_order_code
    from .webdriver_utils import CLICKS_ORDER_ALLOWED_VALUES
    if clicks_order_code not in CLICKS_ORDER_ALLOWED_VALUES:
        clicks_order_code = "se_js_ac"

    logger.info(f"Executing operation: {op_data.get('operation_intent')} (type: {action})")

    # Handle secrets
    for key, value in op_data.items():
        if isinstance(value, str) and value.startswith("secrets."):
            env_var_name = value.split(".")[1]
            op_data[key] = os.getenv(env_var_name, '')

    # Process sub_instruction_obj variables
    if isinstance(sub_instruction_obj, dict):
        if 'variable' in sub_instruction_obj:
            for key, value in sub_instruction_obj['variable'].items():
                if isinstance(value, str) and value.startswith("{{secrets."):
                    continue
                new_value = get_variable_value(value, metadata.get('variables', {}))
                if new_value != value:
                    # Only replace the variable placeholder in the string if the key already exists in op_data
                    # This preserves the original value from the metadata
                    if "SCROLL" in action:
                        op_data["scroll_value"] = new_value
                    elif key in op_data and isinstance(op_data[key], str):
                        # If the key exists in op_data and is a string, replace the variable placeholder
                        # This preserves the original value and only replaces the variable
                        op_data[key] = get_variable_value(op_data[key], metadata.get('variables', {}))
                    else:
                        # Otherwise, set the key to the new value
                        op_data[key] = new_value

    if user_vars_list != '':
        import json
        user_vars_list = json.loads(user_vars_list)

    if locators is not None:
        if locators[0][0] == "[" and locators[0][-1] == "]":
            cordinates = locators[0]
        else:
            cordinates = None

    regex = None
    if 'regex_pattern' in op_data:
        regex_pattern = op_data['regex_pattern']
        regex = base64.b64decode(regex_pattern).decode("utf-8")
    html = ""

    for attempts in range(1, max_retries + 2):
        try:
            reset_implicit_wait = False

            if op_data.get('explicit_wait', 0):
                time.sleep(op_data['explicit_wait'])

            if op_data.get('implicit_wait', 0) != 0:
                driver.implicitly_wait(op_data['implicit_wait'])
                reset_implicit_wait = True
                
            shadow = ""
            if frame_info and frame_info != "":
                if selector and selector.get('frameInfo') and len(selector.get('frameInfo', [])) > 0:
                    from .webdriver_utils import switch_to_content_by_selector
                    shadow = switch_to_content_by_selector(driver, selector['frameInfo'])
                else:
                    shadow = switch_to_frame(driver=driver, operation_index=operation_index, shadow=shadow, max_retries=max_retries, frame_info=frame_info)
                if shadow == "unresolved":
                    raise Exception("Unable to resolve frameInformation")
                
            element_wheel_check = False
            if selector and selector != "":
                locators = []
                for sel in selector['locators']:
                    locators.append({"selector": sel['selector'], "isXpath": sel['isXPath']})
                    
            if locators and cordinates is None:
                element = find_element(driver=driver, locators=locators, operation_idx=operation_index, shadow=shadow)
                try:
                    element_wheel_check = True if all(event in driver.execute_script("return arguments[0].eventListenerList;", element) for event in ["wheel", "touchmove"]) else False
                except Exception as e:
                    pass
            else:
                element = None
            
            scroll_sleep_time = 1
            time.sleep(0.2)

            if action.lower() not in ["script", "api"]:
                set_last_action_timestamp(int(time.time() * 1000))

            if 'click' in action.lower():
                if op_data.get('mi_keypress_info', None) is not None:
                    try:
                        value = json.loads(op_data['mi_keypress_info'])
                    except:
                        pass
                    actions = ActionChains(driver)
                    for key_dict in value.get("true_keys", []):
                        key = list(key_dict.keys())[0].split("Key")[0].upper()
                        if key == "META":
                            key = "CONTROL"
                        actions.key_down(getattr(Keys, key))
                    actions.click(element)
                    for key_dict in value.get("true_keys", []):
                        key = list(key_dict.keys())[0].split("Key")[0].upper()
                        actions.key_up(getattr(Keys, key))
                    actions.perform()
                else:
                    if cordinates is not None:
                        x,y = canvas_autoheal_wrapper(operation_index,driver)
                        actions = ActionBuilder(driver)
                        actions.pointer_action.move_to_location(x, y)
                        actions.pointer_action.click()
                        actions.perform()
                    else:
                        click(element=element, driver=driver, clicks_order_code=clicks_order_code)

            elif action.lower() == 'api':
                method = op_data["method"]
                url = op_data["url"]
                headers = op_data["headers"]
                headers = replace_secrets_in_dict(headers)
                body = op_data["body"]
                params = op_data["params"]
                timeout = op_data["timeout"]
                verify = op_data["verify"]
                response = execute_api(driver, method, url, headers, body, params, timeout, verify)
                if user_vars_list and len(user_vars_list) > 0:
                    metadata['variables'][user_vars_list[0]["name"]] = response
                return response

            elif action.lower() == 'hover':
                if cordinates is not None:
                    x,y = canvas_autoheal_wrapper(operation_index,driver)
                    actions = ActionBuilder(driver)
                    actions.pointer_action.move_to_location(x, y)
                    actions.perform()
                else:
                    ActionChains(driver).move_to_element(element).perform()

            elif action.lower() in ['type', 'input']:
                class element_to_be_input_and_text(object):
                    def __call__(self, driver):
                        focused_element = driver.execute_script("return document.activeElement;")
                        if focused_element.tag_name in ["input", "textarea"] or focused_element.get_attribute(
                                "contenteditable") == "true":
                            return focused_element
                        else:
                            return False

                if frame_info and frame_info != "":
                    if cordinates is not None:
                        x,y = canvas_autoheal_wrapper(operation_index,driver)
                        actions = ActionBuilder(driver)
                        actions.pointer_action.move_to_location(x, y)
                        actions.pointer_action.click()
                        action.send_keys(op_data.get('value', None))
                        actions.perform()
                    else:
                        click(element=element, driver=driver)
                        driver.execute_script("arguments[0].value = '';", element)
                        if element.get_attribute("pattern") and '[0-9]{2}' in element.get_attribute("pattern"):
                            for char in op_data.get('value', ''):
                                element.send_keys(char)
                        else:
                            element.send_keys(op_data.get('value', None))
                else:
                    if cordinates is not None:
                        x,y = canvas_autoheal_wrapper(operation_index,driver)
                        actions = ActionBuilder(driver)
                        actions.pointer_action.move_to_location(x, y)
                        actions.pointer_action.click()
                        actions.key_action.send_keys(" " + op_data.get('value', None))
                        actions.perform()
                    else:
                        time.sleep(1)
                        driver.execute_script("arguments[0].value = '';", element)
                        click(element=element, driver=driver)
                        if element.get_attribute("type") in ["date", "time"]:
                            for i in range(10):
                                element.send_keys(Keys.ARROW_LEFT)
                        if element.get_attribute("pattern") and '[0-9]{2}' in element.get_attribute("pattern"):
                            for char in op_data.get('value', ''):
                                element.send_keys(char)
                        else:
                            element.send_keys(op_data.get('value', None))

            elif action.lower() == 'search':
                class element_to_be_input_and_text(object):
                    def __call__(self, driver):
                        focused_element = driver.execute_script("return document.activeElement;")
                        if focused_element.tag_name in ["input", "textarea"] or focused_element.get_attribute(
                                "contenteditable") == "true":
                            return focused_element
                        else:
                            return False

                click(element=element, driver=driver)
                if frame_info and frame_info != "":
                    driver.execute_script("arguments[0].value = '';", element)
                    element.send_keys(op_data['value'])
                else:
                    if cordinates is not None:
                        x, y = canvas_autoheal_wrapper(operation_index, driver)
                        actions = ActionBuilder(driver)
                        actions.pointer_action.move_to_location(x, y)
                        actions.pointer_action.click()
                        actions.perform()

                        to_type = op_data.get('value', None)

                        keyboard_actions = ActionBuilder(driver)
                        keyboard_actions.key_action.send_keys(to_type)
                        keyboard_actions.key_action.send_keys(Keys.RETURN)  # This simulates pressing Enter
                        keyboard_actions.perform()
                    else:
                        wait = WebDriverWait(driver, 10)
                        focused_element = wait.until(element_to_be_input_and_text())
                        input_element = wait.until(EC.element_to_be_clickable(focused_element))
                        driver.execute_script("arguments[0].value = '';", input_element)
                        input_element.send_keys(op_data['value'])
                        input_element.send_keys(Keys.RETURN)

            elif action.lower() == 'upload':
                value = op_data.get('value', None)
                print("File Name: ", value)
                file_path = get_downloads_file_path(value)
                print("File Path: ", file_path)
                element.send_keys(file_path)

            elif action.lower() == 'enter':
                element.send_keys(Keys.RETURN)

            elif action.lower() == 'clear':
                if cordinates is not None:
                    x, y = canvas_autoheal_wrapper(operation_index, driver)

                    # First action: move and click
                    click_action = ActionBuilder(driver)
                    click_action.pointer_action.move_to_location(x, y)
                    click_action.pointer_action.click()
                    click_action.perform()

                    # Second action: select all text
                    select_action = ActionBuilder(driver)
                    select_action.key_action.key_down(Keys.CONTROL)
                    select_action.key_action.send_keys("a")
                    select_action.key_action.key_up(Keys.CONTROL)
                    select_action.perform()

                    # Third action: delete the selected text
                    delete_action = ActionBuilder(driver)
                    delete_action.key_action.send_keys(Keys.DELETE)
                    delete_action.perform()
                else:
                    current_value = element.get_attribute('value')
                    if current_value:
                        n = len(current_value)
                        for i in range(n):
                            element.send_keys(Keys.BACKSPACE)
                    if element.get_attribute("contenteditable") == "true":
                        driver.execute_script("arguments[0].innerText = '';", element)

            elif action.lower() == 'scroll_element_top_bottom':
                scroll_direction = op_data['scroll_direction']
                scroll_values = {
                    'down':  ('deltaY', 1),
                    'up':    ('deltaY', -1),
                    'left':  ('deltaX', -1),
                    'right': ('deltaX', 1)
                }

                if element_wheel_check and scroll_direction in scroll_values:
                    axis, multiplier = scroll_values[scroll_direction]
                    dimension = 'scrollHeight' if axis == 'deltaY' else 'scrollWidth'
                    driver.execute_script(
                        f"let event = new WheelEvent('wheel', {{bubbles: true, cancelable: true, {axis}: {multiplier} * arguments[0].{dimension}}}); arguments[0].dispatchEvent(event);",
                        element
                    )
                elif scroll_direction in scroll_values:
                    _, multiplier = scroll_values[scroll_direction]
                    x = multiplier * element.get_property('scrollWidth') if scroll_direction in ['left', 'right'] else 0
                    y = multiplier * element.get_property('scrollHeight') if scroll_direction in ['up', 'down'] else 0
                    driver.execute_script("arguments[0].scrollBy(arguments[1], arguments[2]);", element, x, y)
                time.sleep(scroll_sleep_time)

            elif action.lower() == 'scroll_element_by_pixels' or action.lower() == 'scroll_element_pixels':
                scroll_value = int(op_data.get('scroll_value', 100))
                direction = op_data['scroll_direction']
                is_wheel = element_wheel_check

                delta_map = {
                    'up': (0, -scroll_value),
                    'down': (0, scroll_value),
                    'left': (-scroll_value, 0),
                    'right': (scroll_value, 0)
                }

                deltaX, deltaY = delta_map.get(direction, (0, 0))

                if is_wheel:
                    driver.execute_script(
                        "let event = new WheelEvent('wheel', {bubbles: true, cancelable: true, deltaX: arguments[1], deltaY: arguments[2]}); arguments[0].dispatchEvent(event);",
                        element, deltaX, deltaY
                    )
                else:
                    driver.execute_script(
                        "arguments[0].scrollBy(arguments[1], arguments[2]);",
                        element, deltaX, deltaY
                    )
                time.sleep(scroll_sleep_time)

            elif action.lower() == 'scroll_element_by_percentage' or action.lower() == 'scroll_element_percentage':
                direction = op_data['scroll_direction']
                value = int(op_data.get('scroll_value', 10)) / 100

                axis = 'Y' if direction in ['up', 'down'] else 'X'
                dim = 'Height' if axis == 'Y' else 'Width'
                sign = -1 if direction in ['up', 'left'] else 1

                total = driver.execute_script(f"return arguments[0].scroll{dim};", element)
                pixels = total * value * sign

                if element_wheel_check:
                    driver.execute_script(
                        f"arguments[0].dispatchEvent(new WheelEvent('wheel', {{bubbles: true, cancelable: true, delta{axis}: {pixels}}}));", element)
                else:
                    x = pixels if axis == 'X' else 0
                    y = pixels if axis == 'Y' else 0
                    driver.execute_script("arguments[0].scrollBy(arguments[1], arguments[2]);", element, x, y)
                time.sleep(scroll_sleep_time)

            elif action.lower() == 'scroll_element_by_times' or action.lower() == 'scroll_element_times':
                direction = op_data['scroll_direction']
                multiplier = int(op_data.get('scroll_value', 1))
                axis = 'Y' if direction in ['up', 'down'] else 'X'
                sign = -1 if direction in ['up', 'left'] else 1
                dim = 'clientHeight' if axis == 'Y' else 'clientWidth'

                if element_wheel_check:
                    script = f"""
                        let amount = {sign} * {multiplier} * arguments[0].{dim};
                        let event = new WheelEvent('wheel', {{bubbles: true, cancelable: true, delta{axis}: amount}});
                        arguments[0].dispatchEvent(event);
                    """
                    driver.execute_script(script, element)
                else:
                    script = f"""
                        let amount = {sign} * {multiplier} * arguments[0].{dim};
                        arguments[0].scrollBy({{'X': [amount, 0], 'Y': [0, amount]}}['{axis}'][0], {{'X': [amount, 0], 'Y': [0, amount]}}['{axis}'][1]);
                    """
                    driver.execute_script(script, element)
                time.sleep(scroll_sleep_time)

            elif action.lower() == 'enter':
                element.send_keys(Keys.RETURN)

            elif action.lower() == 'refresh':
                driver.refresh()

            elif action.lower() == 'open':
                url = op_data.get('url', '')
                logger.info(f"Opening URL: {url}")
                if operation_index == "0":
                    driver.get(url)
                else:
                    go_to_url(driver=driver, url=url)

            elif action.lower() == 'scroll_top_bottom':
                if op_data['scroll_direction'] == 'up':
                    driver.execute_script('window.scrollTo(0, -document.body.scrollHeight)')
                elif op_data['scroll_direction'] == 'down':
                    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                time.sleep(scroll_sleep_time)

            elif action.lower() == 'scroll_pixels':
                if op_data['scroll_direction'] == 'up':
                    driver.execute_script(f"window.scrollBy(0, -{int(op_data['scroll_value'])})")
                elif op_data['scroll_direction'] == 'down':
                    driver.execute_script(f"window.scrollBy(0, {int(op_data['scroll_value'])})")
                time.sleep(scroll_sleep_time)

            elif action.lower() == 'scroll_percentage':
                total_height = driver.execute_script("return document.body.scrollHeight")
                scroll_pixels = total_height * (int(op_data['scroll_value']) / 100)
                if op_data['scroll_direction'] == 'up':
                    driver.execute_script(f'window.scrollBy(0, -{scroll_pixels})')
                elif op_data['scroll_direction'] == 'down':
                    driver.execute_script(f'window.scrollBy(0, {scroll_pixels})')
                time.sleep(scroll_sleep_time)

            elif action.lower() == 'scroll_times':
                if op_data['scroll_direction'] == 'up':
                    driver.execute_script(
                        f"scroll_height = {int(op_data['scroll_value'])}*window.innerHeight; window.scrollBy(0, -scroll_height)")
                elif op_data['scroll_direction'] == 'down':
                    driver.execute_script(
                        f"scroll_height = {int(op_data['scroll_value'])}*window.innerHeight; window.scrollBy(0, scroll_height)")
                time.sleep(scroll_sleep_time)

            elif action.lower() == 'navigate':
                if op_data['navigation_direction'] == 'back':
                    driver.back()
                elif op_data['navigation_direction'] == 'forward':
                    driver.forward()

            elif action.lower() == 'new_tab':
                url = op_data.get('url', '')
                logger.info(f"Opening URL in new tab: {url}")
                
                if url:
                    logger.info(f"Opening URL in new tab: {url}")
                    driver.execute_script(f"window.open('{url}')")
                    driver.switch_to.window(driver.window_handles[-1])
                else:
                    driver.execute_script("window.open()")
                    driver.switch_to.window(driver.window_handles[-1])

            elif action.lower() == 'wait':
                time.sleep(int(op_data['value']))

            elif action.lower() == 'close_tab':
                driver.switch_to.window(driver.window_handles[op_data['tab_index']])
                driver.close()
                driver.switch_to.window(driver.window_handles[-1])

            elif action.lower() == 'switch_tab':
                driver.switch_to.window(driver.window_handles[op_data['tab_index']])

            elif action.lower() == "scroll_to":
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                time.sleep(scroll_sleep_time)

            elif action.lower() == "scroll":
                try:
                    value = json.loads(op_data['mi_scroll_info'])
                except:
                    pass
                for scroll_target, scroll_dict in value.items():
                    if scroll_target == "document":
                        window_scroll_script = f"window.scrollTo({value['document']['windowScrollX']}, {value['document']['windowScrollY']});"
                        driver.execute_script(window_scroll_script)
                    else:
                        element_scroll_script = f'"arguments[0].scrollLeft = {scroll_dict["scrollLeft"]}; arguments[0].scrollTop = {scroll_dict["scrollTop"]};", driver.find_element(By.XPATH, "{scroll_target}")'
                        driver.execute_script(element_scroll_script)
                time.sleep(scroll_sleep_time)

            elif action.lower() == "sendkeys":
                key = getattr(Keys, op_data['key'].split(".")[1].upper())
                element.send_keys(key)

            elif action.lower() == "select":
                def select_option(select_element, option):
                    """
                    Select an option from a dropdown with fallback mechanisms.
                    Format can be 'value::text' or just 'value'
                    """
                    select_option = option.split("::")
                    if len(select_option) == 1:
                        value = select_option[0]
                        text = select_option[0]
                    else:
                        value, text = select_option[0], select_option[1]
                    
                    select = Select(select_element)
                    try:
                        select.select_by_value(value)
                        print(f"Selected option by value: {value}")
                    except Exception as e:
                        print(f"Failed to select by value, trying by text: {e}")
                        try:
                            select.select_by_visible_text(text)
                            print(f"Selected option by text: {text}")
                        except Exception as e2:
                            print(f"Failed to select by text: {e2}")
                            # Last resort - try to find by partial text
                            options = select_element.find_elements(By.TAG_NAME, "option")
                            for option in options:
                                if text.lower() in option.text.lower():
                                    option.click()
                                    print(f"Selected option by partial text match: {option.text}")
                                    return
                            raise Exception(f"Could not select option with value '{value}' or text '{text}'")
                
                select_option(element, op_data['value'])

            elif action.lower() == "textual_query":
                utility = op_data['string_to_float']

                if element is None:
                    print("Element not found in query")
                    raise ValueError("Element not found")

                html = element.get_attribute('outerHTML').replace('"', "'").replace("\n", "")

                if html == "" or html is None:
                    print("Outer HTML not found in query")
                    raise ValueError("Outer HTML not found")

                try:
                    match = re.search(fr"{regex}", html)
                    if utility:
                        if match:
                            result = string_to_float(match.group(1))
                        else:
                            result = None
                    else:
                        result = match.group(1) if match else None
                except Exception as e:
                    print("Regex not found in query")
                    raise ValueError("Regex not found")

                if reset_implicit_wait:
                    driver.implicitly_wait(15)
                if frame_info:
                    driver.switch_to.default_content()

                if result is None:
                    raise ValueError("Regex not found")

                return result

            elif action.lower() == "script":
                user_js_code = op_data['js_snippet']
                user_js_code = replace_variables_in_script(user_js_code, metadata.get('variables', {}))
                js_script_resp = execute_js(user_js_code=user_js_code, driver=driver)
                if "error" in js_script_resp and js_script_resp["error"] != "":
                    raise Exception(js_script_resp)
                if "value" in js_script_resp and js_script_resp["value"] != "null":
                    if user_vars_list and len(user_vars_list) > 0:
                        user_vars_list[0]["variable_value"] = js_script_resp["value"]
                        metadata['variables'][user_vars_list[0]["name"]] = js_script_resp["value"]
                    return js_script_resp["value"]

            elif action.lower() == "js_dialog":
                text = op_data.get('value', '')
                alert = driver.switch_to.alert
                dialog_action = op_data.get('dialog_action', 'accept')
                
                try:
                    # Get dialog text for logging
                    dialog_text = alert.text
                    print(f"Dialog text: {dialog_text}")
                    
                    if dialog_action.lower() == "accept":
                        if text:
                            try:
                                alert.send_keys(text)
                                print(f"Entered text in dialog: {text}")
                            except Exception as e:
                                print(f"Failed to enter text in dialog: {e}")
                        alert.accept()
                        print(f"Accepted JS dialog")
                    else:
                        alert.dismiss()
                        print(f"Dismissed JS dialog")
                    
                    # Wait for dialog to be processed
                    time.sleep(1)
                except Exception as e:
                    print(f"Error handling JS dialog: {e}")
                    # Try to recover by accepting the dialog
                    try:
                        alert.accept()
                        print("Recovered by accepting dialog")
                    except:
                        print("Could not recover dialog handling")

            else:
                raise ValueError("Invalid action: {}".format(action))

            if reset_implicit_wait:
                driver.implicitly_wait(15)

            if frame_info and frame_info != "":
                frames = json.loads(frame_info)
                if any('iframe' in obj for obj in frames):
                    driver.switch_to.default_content()
            break  # Break out of retry loop if successful

        except Exception as e:
            if action.lower() == "script":
                break
            time.sleep(op_data.get('retries_delay', 0))
            if attempts == max_retries + 1 and not op_data.get('optional_flag', False):
                raise e
            elif attempts == max_retries + 1 and op_data.get('optional_flag', False):
                print(f"Failed to execute action: {action} on locator: {op_data.get('locator')}. Error: {e}")
                break
            if str(e) == "Element not found" or str(e) == "Outer HTML not found":
                print(f"Element not found. Autohealing locators...")
                locators = retry(driver=driver, operation_idx=operation_index)
            elif str(e) == "Regex not found":
                print(f"Regex not found. Autohealing regex...")
                regex = heal_query(driver=driver, operation_index=operation_index, outer_html=html)

            print(f"Retrying due to Error: {str(e)[:50]}....")

    # Mark operation as processed after successful execution
    operations_meta_data.mark_operation_as_processed(op_data)
