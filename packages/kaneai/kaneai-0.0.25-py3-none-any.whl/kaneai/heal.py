import base64
import json
import time
import requests
import uuid
import os
from selenium import webdriver

try:
    from safari import inject_script
    print("Safari Utility Imported")
except ImportError:
    pass

def compare_screenshots(driver:webdriver, before_screenshot:str, after_screenshot:str):

    compare_script = f"""
        return (async function() {{
            try {{
                const beforeImage = 'data:image/png;base64,{before_screenshot}';
                const afterImage = 'data:image/png;base64,{after_screenshot}';
                const result = await new Promise((resolve) => {{
                    resemble(beforeImage).compareTo(afterImage).onComplete((data) => {{
                        resolve(data.misMatchPercentage);
                    }});
                }});
                return Math.ceil(result);
            }} catch (error) {{
                return -1; 
            }}
        }})();
        """
    result = driver.execute_script(compare_script)
    if isinstance(result, float):
        return int(result)
    elif isinstance(result, int):
        return result
    else:
        print("Unexpected comparison result:", result)
        return -1


class Heal:
    def __init__(self, operation_idx: str, driver: webdriver.Chrome):
        self.operation_idx = operation_idx
        self.driver: webdriver.Chrome = driver

        from .config import get_metadata
        metadata = get_metadata()
        self.current_action: dict = metadata.get(operation_idx, {})
        self.prev_actions: list[dict] = []
        self.tagified_image: str = ""
        self.untagged_image_base64: str = ""
        self.xpath_mapping: dict = {}
        self.tags_description: dict = {}
        self.page_source: str = ""

        self.test_id: str = os.getenv('TEST_ID', '')
        self.username: str = os.getenv('LT_USERNAME', '')
        self.accesskey: str = os.getenv('LT_ACCESS_KEY', '')
        self.commit_id: str = os.getenv('COMMIT_ID', '')
        self.org_id: int = int(os.getenv('REQUEST_ID', '0'))
        self.page_source: str = ""
        self.code_export_id: str = uuid.uuid4().hex[:16]
        self.automind_url = os.environ.get('AUTOMIND_URL', 'https://kaneai-api.lambdatest.com')
        self.operation: str = ""
        self.image_base64: str = ""
        self.dimensions: list = []
        
    def execute_async_js(self, script: str):
        """
        Execute asynchronous JavaScript code and wait for its completion.
        
        Args:
            script: The JavaScript code to execute asynchronously
            
        Returns:
            The result of the JavaScript execution
        """
        result = self.driver.execute_script(f"""
        return new Promise((resolve) => {{
            (async function() {{
                try {{
                    const result = await {script};
                    resolve(result);
                }} catch (error) {{
                    console.error('Async JS error:', error);
                    resolve(null);
                }}
            }})();
        }});
        """)
        return result

    def resolve(self) -> requests.Response:
        attempt = 1
        max_attempt = 2

        while (max_attempt >= attempt):
            attempt += 1

            if self.driver.capabilities['browserName'].lower() == "safari":
                inject_script(self.driver)

            before_screenshot = self.driver.get_screenshot_as_base64()
            # Execute tagifyWebpage and wait for it to complete
            self.execute_async_js("tagifyWebpage(false,true)")

            xpath_mapping = self.execute_async_js("fetchJsonData(\"JSONOutput\")")
            self.xpath_mapping = json.loads(xpath_mapping)

            tags_description = self.execute_async_js("fetchJsonData(\"descOutput\")")
            self.tags_description = json.loads(tags_description)

            self.tagified_image = self.driver.get_screenshot_as_base64()

            # First remove tags and wait for completion
            self.execute_async_js("removeLTTags()")
            
            # Then clear the data structures
            self.driver.execute_script("annotations = [];JSONOutput = {};nodeData = {};")

            payload = json.dumps({
                "code_export_id": self.code_export_id,
                "username": self.username,
                "org_id": self.org_id,
                "commit_id": self.commit_id,
                "current_action": self.current_action,
                "tagified_image": self.tagified_image,
                "xpath_mapping": self.xpath_mapping,
                "tags_description": self.tags_description,
                "accesskey": self.accesskey,
                "test_id": self.test_id,
                "session_id": self.driver.session_id
            })

            headers = {'Content-Type': 'application/json', 'Authorization' : f"Basic {base64.b64encode(f'{self.username}:{self.accesskey}'.encode()).decode()}" }

            print("Heal Resolve... code_export_id: ", self.code_export_id)
            response = requests.request("POST", url=f"{self.automind_url}/v1/heal/resolve", headers=headers, data=payload)

            after_screenshot = self.driver.get_screenshot_as_base64()
            mismatch_percentage = compare_screenshots(driver=self.driver, before_screenshot=before_screenshot,
                                                      after_screenshot=after_screenshot)

            if mismatch_percentage >= 2:
                print("Retrying due to visual mismatch of ", mismatch_percentage, "%...")
                time.sleep(2)
                continue
            else:
                return response

        return response

    def list_xpaths(self) -> requests.Response:

        attempt = 1
        max_attempt = 2

        while (max_attempt >= attempt):
            attempt += 1

            if self.driver.capabilities['browserName'].lower() == "safari":
                inject_script(self.driver)

            before_screenshot = self.driver.get_screenshot_as_base64()

            if self.current_action['operation_type'].__contains__("QUERY"):
                # Execute tagifyWebpage and wait for it to complete
                self.execute_async_js("tagifyWebpage(false,true)")
            else:
                # Execute tagifyWebpage and wait for it to complete
                self.execute_async_js("tagifyWebpage()")

            xpath_mapping = self.execute_async_js("fetchJsonData(\"JSONOutput\")")
            self.xpath_mapping = json.loads(xpath_mapping)

            tags_description = self.execute_async_js("fetchJsonData(\"descOutput\")")
            self.tags_description = json.loads(tags_description)

            self.page_source = self.driver.execute_script("return document.body.outerHTML")

            self.tagified_image = self.driver.get_screenshot_as_base64()

            # First remove tags and wait for completion
            self.execute_async_js("removeLTTags()")
            
            # Then clear the data structures
            self.driver.execute_script("annotations = [];JSONOutput = {};nodeData = {};")

            payload = json.dumps({
                "code_export_id": self.code_export_id,
                "current_action": self.current_action,
                "prev_actions": self.prev_actions,
                "xpath_mapping": self.xpath_mapping,
                "tagified_image": self.tagified_image,
                "commit_id": self.commit_id,
                "test_id": self.test_id,
                "username": self.username,
                "accesskey": self.accesskey,
                "tags_description": self.tags_description,
                "org_id": self.org_id,
                "page_source": self.page_source,
                "session_id": self.driver.session_id
            })

            headers = {'Content-Type': 'application/json', 'Authorization' : f"Basic {base64.b64encode(f'{self.username}:{self.accesskey}'.encode()).decode()}" }

            print("Heal List Xpaths... code_export_id: ", self.code_export_id)
            response = requests.request("POST", url=f"{self.automind_url}/v1/heal/xpaths", headers=headers, data=payload)

            after_screenshot = self.driver.get_screenshot_as_base64()
            mismatch_percentage = compare_screenshots(driver=self.driver, before_screenshot=before_screenshot,
                                                      after_screenshot=after_screenshot)

            if mismatch_percentage >= 2:
                print("Retrying due to visual mismatch of ", mismatch_percentage, "%...")
                time.sleep(2)
                continue
            else:
                return response

        return response

    def resolve_xpath(self) -> requests.Response:
        if self.driver.capabilities['browserName'].lower() == "safari":
            inject_script(self.driver)

        if self.current_action['operation_type'].__contains__("QUERY"):
            self.execute_async_js("tagifyWebpage(false,true)")
        else:
            self.execute_async_js("tagifyWebpage()")

        xpath_mapping = self.execute_async_js("fetchJsonData(\"JSONOutput\")")
        self.xpath_mapping = json.loads(xpath_mapping)

        tags_description = self.execute_async_js("fetchJsonData(\"descOutput\")")
        self.tags_description = json.loads(tags_description)

        self.page_source = self.driver.execute_script("return document.body.outerHTML")

        self.tagified_image = self.driver.get_screenshot_as_base64()

        # First remove tags and wait for completion
        self.execute_async_js("removeLTTags()")
        
        # Then clear the data structures
        self.driver.execute_script("annotations = [];JSONOutput = {};nodeData = {};")

        payload = json.dumps({
            "code_export_id": self.code_export_id,
            "current_action": self.current_action,
            "xpath_mapping": self.xpath_mapping,
            "tagified_image": self.tagified_image,
            "commit_id": self.commit_id,
            "test_id": self.test_id,
            "username": self.username,
            "accesskey": self.accesskey,
            "tags_description": self.tags_description,
            "org_id": self.org_id,
            "page_source": self.page_source,
            "session_id": self.driver.session_id,
        })

        headers = {'Content-Type': 'application/json', 'Authorization' : f"Basic {base64.b64encode(f'{self.username}:{self.accesskey}'.encode()).decode()}" }

        print("Heal Resolve Xpath... code_export_id: ", self.code_export_id)

        response = requests.request("POST", url=f"{self.automind_url}/v1/heal/resolve", headers=headers, data=payload)
        print("RESPONSE TEXT: ", response.text)

        return response

    def textual_query(self, outer_html: str) -> requests.Response:
        self.page_source = outer_html

        payload = json.dumps({
            "code_export_id": self.code_export_id,
            "username": self.username,
            "org_id": self.org_id,
            "commit_id": self.commit_id,
            "current_action": self.current_action,
            "accesskey": self.accesskey,
            "test_id": self.test_id,
            "page_source": self.page_source,
        })

        headers = {'Content-Type': 'application/json', 'Authorization' : f"Basic {base64.b64encode(f'{self.username}:{self.accesskey}'.encode()).decode()}" }

        print("Heal Textual Query... code_export_id: ", self.code_export_id)

        response = requests.request("POST", f"{self.automind_url}/v1/heal/query", headers=headers, data=payload)

        return response

    def vision_query(self) -> requests.Response:
        attempt = 1
        max_attempt = 2

        while (max_attempt >= attempt):
            attempt += 1

            if self.driver.capabilities['browserName'].lower() == "safari":
                inject_script(self.driver)

            before_screenshot = self.driver.get_screenshot_as_base64()
            self.untagged_image_base64 = before_screenshot
            self.execute_async_js("tagifyWebpage(false,true)")
            
            # Now that tagifyWebpage is complete, get the tags description
            tags_description = self.execute_async_js("fetchJsonData(\"descOutput\")")
            self.tags_description = json.loads(tags_description)
            
            self.tagified_image = self.driver.get_screenshot_as_base64()
            
            # First remove tags and wait for completion
            self.execute_async_js("removeLTTags()")
            
            # Then clear the data structures
            self.driver.execute_script("annotations = [];JSONOutput = {};nodeData = {};")

            payload = json.dumps({
                "code_export_id": self.code_export_id,
                "current_action": self.current_action,
                "tagified_image": self.tagified_image,
                "commit_id": self.commit_id,
                "test_id": self.test_id,
                "username": self.username,
                "accesskey": self.accesskey,
                "tags_description": self.tags_description,
                "org_id": self.org_id,
                "session_id": self.driver.session_id,
                "untagged_image_base64": self.untagged_image_base64
            })

            headers = {'Content-Type': 'application/json', 'Authorization' : f"Basic {base64.b64encode(f'{self.username}:{self.accesskey}'.encode()).decode()}" }

            print("Heal Vision Query... code_export_id: ", self.code_export_id)

            response = requests.request("POST", url=f"{self.automind_url}/v1/heal/vision", headers=headers, data=payload)

            after_screenshot = self.driver.get_screenshot_as_base64()
            mismatch_percentage = compare_screenshots(driver=self.driver, before_screenshot=before_screenshot,
                                                      after_screenshot=after_screenshot)

            if mismatch_percentage >= 2:
                print("Retrying due to visual mismatch of ", mismatch_percentage, "%...")
                time.sleep(2)
                continue
            else:
                return response

        return response

    def coordinate(self, operation_index) -> requests.Response:
        """
        Get coordinates for canvas interaction from the AutoMind API.
        
        Args:
            operation_index: The operation index to use for healing
            
        Returns:
            Response object from the API call
        """
        attempt = 1
        max_attempt = 3
        while (max_attempt >= attempt):
            attempt += 1
            headers = {'Content-Type': 'application/json', 'Authorization' : f"Basic {base64.b64encode(f'{self.username}:{self.accesskey}'.encode()).decode()}" }
            self.dimensions = self.driver.execute_script("return [window.innerWidth, window.innerHeight]")
            self.image_base64 = self.driver.get_screenshot_as_base64()

            from .config import get_metadata
            metadata = get_metadata()
            operation_data = metadata.get(operation_index, {})
            self.operation = operation_data.get('operation_intent', None)
            payload = json.dumps({
                "image": self.image_base64,
                "dimensions": self.dimensions,
                "operation": self.operation,
                "current_action": {
                    "action": "process",
                    "metadata": "healing process started"
                },
                "commit_id": self.commit_id,
                "test_id": self.test_id,
                "username": self.username,
                "accesskey": self.accesskey,
                "org_id": self.org_id
            })

            decode = open('stringtoimage.png', 'wb')
            decode.write(base64.b64decode(self.image_base64))
            decode.close()
            response = requests.request("POST", url=f"{self.automind_url}/v1/heal/coordinates", headers=headers, data=payload)
            if response.status_code == 200:
                return response
            else:
                continue

        return response

    def to_json(self):
        json_payload = {
            "code_export_id": self.code_export_id,
            "current_action": self.current_action,
            "prev_actions": self.prev_actions,
            "xpath_mapping": self.xpath_mapping,
            "tagified_image": self.tagified_image,
            "commit_id": self.commit_id,
            "test_id": self.test_id,
            "username": self.username,
            "accesskey": self.accesskey,
            "tags_description": self.tags_description,
            "org_id": self.org_id,
            "page_source": self.page_source
        }
        with open("payload.json", "w") as f:
            json.dump(json_payload, f)
