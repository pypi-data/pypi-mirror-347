import json
import time
from functools import wraps
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    InvalidArgumentException,
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
    ElementNotInteractableException,
    StaleElementReferenceException,
    JavascriptException
)

from .heal import Heal

# Global variable for click order configuration
CLICKS_ORDER_ALLOWED_VALUES = ["se_js_ac", "se_ac_js", "js_se_ac", "js_ac_se", "ac_js_se", "ac_se_js", "se_ac", "js_ac", "ac_js", "se", "js", "ac"]


def click(element: WebElement, driver, clicks_order_code: str = "se_js_ac"):
    """
    Clicks on an element using the specified order of click methods.
    
    Clicks order code Usage:
        se -> Selenium click
        ac -> ActionChain click
        js -> JavaScript click

        Ex: se_ac_js -> Order will be Selenium click, ActionChain click, JavaScript click
    """
    if clicks_order_code not in CLICKS_ORDER_ALLOWED_VALUES:
        clicks_order_code = "se_js_ac"  # Default if invalid code provided
        
    click_order = clicks_order_code.split("_")
    for method in click_order:
        if method == 'se':  # Selenium click (WebDriverWait + click)
            try:
                print("Attempting WebDriverWait click...")
                WebDriverWait(driver, 2).until(EC.element_to_be_clickable(element)).click()
                print("Selenium click successful.")
                return
            except Exception as e:
                print("Selenium click failed: ", str(e))
                
        elif method == 'ac':  # ActionChains click
            try:
                print("Attempting ActionChains click...")
                actions = ActionChains(driver)
                actions.move_to_element(element).click().perform()
                print("ActionChain click successful.")
                return
            except Exception as e:
                print("ActionChain click failed: ", str(e))

        elif method == 'js':  # JavaScript click
            try:
                has_onclick = driver.execute_script("return arguments[0].onclick !== null;", element)
        
                if has_onclick:
                    driver.execute_script("arguments[0].click();", element)
                    print("JavaScript click successful.")
                    return
                else:
                    # Try regular JS click anyway
                    driver.execute_script("arguments[0].click();", element)
                    print("JavaScript click successful.")
                    return
            except WebDriverException as e:
                print(f"JavaScript click failed: {str(e)}.")
            except Exception as e:
                print(f"JavaScript click failed: {str(e)}.")
                
    print("All click methods failed.")


def conditions_met(driver):
    # Check if the document is fully loaded
    document_ready = driver.execute_script("return document.readyState") == "complete"

    # Inject code to track active API requests
    driver.execute_script("""
    if (typeof window.activeRequests === 'undefined') {
        window.activeRequests = 0;
        (function(open) {
            XMLHttpRequest.prototype.open = function() {
                window.activeRequests++;
                this.addEventListener('readystatechange', function() {
                    if (this.readyState === 4) {
                        window.activeRequests--;
                    }
                }, false);
                open.apply(this, arguments);
            };
        })(XMLHttpRequest.prototype.open);
    }
    """)

    # Check if any API requests are in progress
    active_requests = driver.execute_script("return window.activeRequests;")

    # Return True only if both conditions are met
    return document_ready and active_requests == 0


def is_element_interactable(driver: webdriver.Remote, element: WebElement) -> bool:
    try:
        if not element.is_displayed() or not element.is_enabled():
            if not element.is_displayed():
                opacity = element.value_of_css_property("opacity")
                if opacity == "0":
                    print("Element has opacity 0")
                    return True
            print("Element is not visible or enabled")
            return False

        return True

    except (ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException) as e:
        print(f"Exception: {str(e)} - Element is not interactable")
        return False

def retry(driver: webdriver.Chrome, operation_idx: str):
    print("Retrying()...")

    WebDriverWait(driver, 180, poll_frequency=1).until(conditions_met)

    response = Heal(operation_idx, driver).list_xpaths()

    if response.status_code == 200:
        response_dict = json.loads(response.text)
        xpaths = response_dict.get('xpaths')
        lambda_hooks(driver, "Locator Autohealed ")
        print("XPaths Autohealed: ", xpaths)
        return xpaths
    else:
        print("Error in Getting Xpaths")
        return []

def go_to_url(driver: webdriver.Chrome, url: str):
    try:
        WebDriverWait(driver, 3).until(EC.url_changes(driver.current_url))
        driver.get(url)

    except TimeoutException:
        driver.get(url)


def find_element(driver: webdriver.Chrome, locators: list, operation_idx: str, max_retries: int = 2,
                 current_retry: int = 0, shadow=""):
    print("Finding element...")
    
    if current_retry >= max_retries:
        print("MAX RETRIES EXCEEDED")
        driver.implicitly_wait(15)  # Reset implicit wait
        return None

    # Check if this is an upload operation
    from .config import get_metadata
    metadata = get_metadata()
    op_data = metadata.get(operation_idx, {})
    upload_file = op_data.get('operation_type') == "UPLOAD"
    
    if upload_file:
        print("Upload operation detected")
        time.sleep(2)

    driver.implicitly_wait(6)  # Set initial implicit wait to 6 seconds

    for locator in locators:
        try:
            if shadow != "":
                element = shadow.find_element(By.XPATH, locator)
            else:
                element = driver.find_element(By.XPATH, locator)
            
            # For upload operations, return element immediately
            if upload_file:
                print("Found upload element")
                driver.implicitly_wait(15)  # Reset implicit wait
                return element
            
            if is_element_interactable(driver, element):
                print(f"Element found using locator: {locator} is interactable")
                driver.implicitly_wait(15)  # Reset implicit wait
                return element  # Return the element if interactable
            else:
                print("Element is Not Interactable, Retrying...")
                continue  # Continue to the next locator if the element is not interactable

        except Exception as e:
            print(f"Unable to find element using locator: {locator}\nError: {str(e)}\nSwitching to next locator...")
            continue  # Continue to the next locator if the element is not found

    driver.implicitly_wait(15)  # Reset implicit wait
    
    locators = retry(driver=driver, operation_idx=operation_idx)
    
    if locators:
        return find_element(driver, locators, operation_idx, max_retries, current_retry + 1,
                            shadow=shadow)  # Retry with incremented attempt count

    return None  # Return None if no element was found or retry exhausted

def lambda_hooks(driver: webdriver.Chrome, argument: str):
    try:
        script = f'lambdatest_executor: {{"action": "stepcontext", "arguments": {{"data": "{argument}", "level": "info"}}}}'
        driver.execute_script(script)
        print(f"\n{argument}")
    except:
        print(f"\n{argument}")


def switch_to_content_by_selector(driver, frame_info_list):
    """
    Given a Selenium `driver` and a list of frame-info dicts like:
      {
        'type': 'shadow' or 'iframe',
        'selectors': [
          {'selector': '...', 'isXPath': True|False, 'score': int},
          ...
        ],
        'boundingBox': { ... }  # ignored here
      }
    this will walk through each frame in order, drilling into shadow-roots
    or switching into iframes as needed. Returns the final shadow-root
    WebElement (or None if the last frame was an iframe).
    """
    shadow = None

    for frame in frame_info_list:
        # pick selectors sorted by score descending
        sorted_sels = sorted(frame.get('selectors', []),
                           key=lambda s: s.get('score', 0),
                           reverse=True)

        host = None
        # try each selector until one works
        for s in sorted_sels:
           sel = s['selector']
           try:
               if s.get('isXPath', False):
                   if shadow:
                       first_child = shadow.find_element(By.CSS_SELECTOR, ":scope > *:first-child")
                       host = first_child.find_element(By.XPATH, sel)
                   else:
                       host = (shadow or driver).find_element(By.XPATH, sel)
               else:
                   host = (shadow or driver).find_element(By.CSS_SELECTOR, sel)
               break
           except (NoSuchElementException, WebDriverException):
               continue

        if host is None:
            raise NoSuchElementException(
                f"Selector Error: Could not locate frame host using any of: {[s['selector'] for s in sorted_sels]}"
            )

        if frame.get('type') == 'iframe':
            # switch into the iframe
            driver.switch_to.frame(host)
            shadow = None

        elif frame.get('type') == 'shadow':
            # enter its shadowRoot
            shadow = driver.execute_script("return arguments[0].shadowRoot", host)

        else:
            # unknown frame type; skip
            continue

    return shadow


def is_dom_loaded(driver):
    """
    Comprehensive check if the DOM is fully loaded across multiple frameworks.
    Returns True if DOM is loaded, or a tuple (False, error_message) if there's an error.
    """
    try:
        # Check document.readyState
        ready_state = driver.execute_script("return document.readyState")
        
        # Check jQuery if it exists
        jquery_ready = driver.execute_script(
            "return typeof jQuery !== 'undefined' ? jQuery.active === 0 : true"
        )

        # Check for any active AJAX requests
        ajax_ready = driver.execute_script(
            "return typeof window.Ajax === 'undefined' || window.Ajax.activeRequestCount === 0"
        )
        
        # Check Angular if it exists
        angular_ready = driver.execute_script(
            """
            if (window.angular) {
                if (angular.element(document).injector()) {
                    return angular.element(document).injector().get('$http').pendingRequests.length === 0;
                }
            }
            return true;
            """
        )
        
        # Check React if it exists (more complex, basic check)
        react_ready = driver.execute_script(
            """
            if (typeof React !== 'undefined' && React.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED) {
                // Basic check for React rendering
                const root = document.getElementById('root') || document.getElementById('app');
                return root && root.childNodes.length > 0;
            }
            return true;
            """
        )
        
        # Check for presence of common loading indicators
        return (ready_state == "complete" and jquery_ready and ajax_ready
                and angular_ready and react_ready)
    except Exception as e:
        # Return a tuple with False and the error message
        print("Error checking dom loaded: ", str(e))
        return (False, str(e))


def isShiftingRequired(element, placeholder):
    """Check if the input element requires cursor positioning at start"""
    if element.get_attribute("type") in ["date", "time"] or all(part in placeholder.lower() for part in ['dd', 'mm', 'yy']) or element.get_attribute("autocomplete") != "":
        return True
    return False


def move_to_start_of_input(element, focused_element=None):
    """Move cursor to the start of an input field"""
    placeholder = element.get_attribute("placeholder") if element.get_attribute("placeholder") else ""
    if isShiftingRequired(element, placeholder):
        for i in range(10):  # Move cursor to the beginning
            if focused_element:
                focused_element.send_keys(Keys.ARROW_LEFT)
            else:
                element.send_keys(Keys.ARROW_LEFT)


def clear_element(driver, element):
    """Clear an element with special handling for contenteditable elements"""
    current_value = element.get_attribute('value')
    if current_value:
        n = len(current_value)
        for i in range(n):
            element.send_keys(Keys.BACKSPACE)
    
    if element.get_attribute("contenteditable") == "true":
        # First select all content
        driver.execute_script("""
            const element = arguments[0];
            const range = document.createRange();
            const selection = window.getSelection();
            range.selectNodeContents(element);
            selection.removeAllRanges();
            selection.addRange(range);
        """, element)
        # Then delete the selection
        element.send_keys(Keys.DELETE)

def switch_to_frame(driver:webdriver.Chrome,operation_index:str,shadow="",max_retries=3,frame_info=""):
    for index in range(1,max_retries + 2):
        if index!=1:
            driver.switch_to.default_content()
            frame_info = retry(driver=driver,operation_idx=operation_index).get('frameInformation')
            frame_info = json.dumps(frame_info)
        try:
            if frame_info and frame_info != "":
                frames = json.loads(frame_info)
                for frame in frames:
                    key, value = list(frame.items())[0]
                    if key == "iframe":
                        if shadow == "":
                            if isinstance(value,list):
                                for index in range(0,len(value)):
                                    try:
                                        iframe = driver.find_element(By.XPATH, value[index])
                                        break
                                    except:
                                        continue
                            else:
                                iframe = driver.find_element(By.XPATH, value)
                            driver.switch_to.frame(iframe)
                        else:
                            iframe = shadow.find_element(By.XPATH, value)
                            driver.switch_to.frame(iframe)
                            shadow = ""
                    elif key == "shadow":
                        if shadow != "":
                            shadow_childrens = shadow.find_element(By.XPATH, value)
                            shadow = driver.execute_script("return arguments[0].shadowRoot.children[0]", shadow_childrens)
                        else:
                            shadow = driver.execute_script("return arguments[0].shadowRoot.children[0]", driver.find_element(By.XPATH, value))
            return shadow
        except Exception as e:
            pass
    return "unresolved"


def is_action_unresolved(action: str, sub_instruction_obj: dict) -> bool:
    """
    Determine if an action is unresolved based on specific criteria.
    
    Args:
        action: The action type string
        sub_instruction_obj: The sub-instruction object containing variable information
        
    Returns:
        bool: True if the action is unresolved, False otherwise
    """
    valid_actions = ["CLICK", "HOVER", "CLEAR", "ENTER"]
    return action in valid_actions and isinstance(sub_instruction_obj, dict) and len(sub_instruction_obj.get("variable", {})) > 0