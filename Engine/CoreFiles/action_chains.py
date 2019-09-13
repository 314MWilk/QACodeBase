import os

from selenium.webdriver.common.action_chains import ActionChains
import base64


def drag_and_drop(driver, drag_element, drop_element):
    """
    Performs drag and drop action in browser
    :param driver: WebShopDriver, SeraphDriver, SquadkitShopDriver
    :param drag_element: Selenium element that will be dragged
    :param drop_element: Selenium element where drag_element will be dropped
    """
    ActionChains(driver).drag_and_drop(drag_element, drop_element).perform()


def hold_button_and_click(driver, button, element):
    """
    Performs click on element with keyboard button clicked
    :param driver: WebShopDriver, SeraphDriver, SquadkitShopDriver
    :param button: Any keyboard button
    :type: button: Keys from selenium.webdriver.common.keys
    :param element: Selenium element that will be clicked
    """
    ActionChains(driver).key_down(button).click(element).key_up(button).perform()


def upload_img_to_drop_zone(driver, selector, path_to_file, file_name):
    """
    Method that performs upload for drop_zone elements
    :param driver: WebShopDriver, SeraphDriver, SquadkitShopDriver
    :param selector: CSS selector for drop_zone element
    :param path_to_file: path to folder containing file that will be uploaded into drop_zone
    :param file_name: file that will be uploaded
    """
    with open(os.path.join(path_to_file, file_name), "rb") as file:
        query = """drop_zone=var dropZone = Dropzone.forElement('%s'); base_64_file = "%s"; 
        function change_img_to_blob(b64Data, contentType, sliceSize) 
        { contentType = contentType || ''; sliceSize = sliceSize || 512; var byteCharacters = atob(b64Data); 
        var byteArrays = []; for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) 
        { var slice = byteCharacters.slice(offset, offset + sliceSize); var byteNumbers = new Array(slice.length); 
        for (var i = 0; i < slice.length; i++) { byteNumbers[i] = slice.charCodeAt(i); } 
        var byteArray = new Uint8Array(byteNumbers); byteArrays.push(byteArray); } 
        var blob = new Blob(byteArrays, {type: contentType}); return blob; } 
        var blob = change_img_to_blob(base64Image, 'image / png'); blob.name = '%s'; 
        dropZone.addFile(blob);""" % (selector, base64.b64encode(file.read()).decode(), file_name)
        driver.execute_query(query)


def hoover(element, driver):
    """
    Performs hoover over element
    :param element: Selenium element that will be hoovered over
    :param driver: WebShopDriver, SeraphDriver, SquadkitShopDriver
    """
    ActionChains(driver).move_to_element(element).perform()
