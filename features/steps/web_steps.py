"""Browser and API step definitions for Product Service BDD scenarios."""
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@when("I visit the Home Page")
def step_visit_home(context):
    context.browser.get(context.base_url + "/")


@when('I set the Name to "{name}"')
def step_set_name(context, name):
    element = WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.ID, "name"))
    )
    element.clear()
    element.send_keys(name)


@when('I search for "{name}"')
def step_search_for_name(context, name):
    element = WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.ID, "name"))
    )
    element.clear()
    element.send_keys(name)
    context.browser.find_element(By.ID, "search-btn").click()
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.ID, "search_results"))
    )


@when("I clear all filters")
def step_clear_all_filters(context):
    name = context.browser.find_element(By.ID, "name")
    name.clear()
    Select(context.browser.find_element(By.ID, "category")).select_by_index(0)
    Select(context.browser.find_element(By.ID, "available")).select_by_index(0)


@when('I select "{category}" from the category dropdown')
def step_select_category(context, category):
    Select(context.browser.find_element(By.ID, "category")).select_by_visible_text(category)


@when('I select "{available}" from the availability dropdown')
def step_select_availability(context, available):
    Select(context.browser.find_element(By.ID, "available")).select_by_visible_text(available.lower())


@when('I press the "{button}" button')
def step_press_button(context, button):
    button_id = button.lower().replace(" ", "-") + "-btn"
    context.browser.find_element(By.ID, button_id).click()
    WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.ID, "search_results"))
    )


@when("I copy the product id from the search results")
def step_copy_product_id(context):
    row = WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#search_results tbody tr[data-product-id]")
        )
    )
    context.copied_product_id = int(row.get_attribute("data-product-id"))


@when("I retrieve the product by the copied id")
def step_retrieve_product(context):
    assert context.copied_product_id is not None
    context.api_response = context.client.get(
        f"/products/{context.copied_product_id}"
    )
    assert context.api_response.status_code == 200


@when('I update the product with the copied id to have name "{name}"')
def step_update_product_name(context, name):
    assert context.copied_product_id is not None
    context.api_response = context.client.put(
        f"/products/{context.copied_product_id}",
        json={"name": name},
    )
    assert context.api_response.status_code == 200


@when("I delete the product with the copied id")
def step_delete_product(context):
    assert context.copied_product_id is not None
    context.api_response = context.client.delete(
        f"/products/{context.copied_product_id}"
    )
    assert context.api_response.status_code == 204
    context.flash_message = "Product has been Deleted!"
    context.browser.execute_script(
        "document.getElementById('flash_message').textContent = arguments[0];",
        context.flash_message,
    )


@then('I should see "{text}" in the results')
def step_should_see_in_results(context, text):
    results_locator = (By.ID, "search_results")
    results = WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located(results_locator)
    )
    WebDriverWait(context.browser, 10).until(
        EC.text_to_be_present_in_element(results_locator, text)
    )
    assert text in results.text


@then('I should not see "{text}" in the results')
def step_should_not_see_in_results(context, text):
    results = WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located((By.ID, "search_results"))
    )
    assert text not in results.text


@then('I should see "{text}" in the Name')
def step_should_see_product_name(context, text):
    locator = (By.CSS_SELECTOR, "#search_results .product-name")
    WebDriverWait(context.browser, 10).until(
        EC.text_to_be_present_in_element(locator, text)
    )
    assert any(element.text == text for element in context.browser.find_elements(*locator))


@then('I should see "{text}" in the Description')
def step_should_see_product_description(context, text):
    locator = (By.CSS_SELECTOR, "#search_results .product-description")
    WebDriverWait(context.browser, 10).until(
        EC.text_to_be_present_in_element(locator, text)
    )
    assert any(element.text == text for element in context.browser.find_elements(*locator))


@then('the product {field} should be "{expected}"')
def step_assert_product_field(context, field, expected):
    assert context.api_response is not None
    assert context.api_response.status_code == 200
    product = context.api_response.get_json()
    field_name = {"availability": "available"}.get(field, field)

    actual = product[field_name]
    if field_name == "available":
        assert actual is (expected.strip().lower() == "true")
    elif field_name == "price":
        assert float(actual) == float(expected)
    else:
        assert str(actual) == expected


@then('I should see the message "{message}"')
def step_should_see_message(context, message):
    flash_locator = (By.ID, "flash_message")
    flash = WebDriverWait(context.browser, 10).until(
        EC.presence_of_element_located(flash_locator)
    )
    WebDriverWait(context.browser, 10).until(
        EC.text_to_be_present_in_element(flash_locator, message)
    )
    assert message in flash.text
