Feature: Product Service
  As a user of the Product Service
  I want to read, update, delete, and search products
  So that I can manage the product catalogue

  Scenario: Read a Product
    Given the following products
      | name | description  | category | available | price |
      | Hat  | A red fedora | Clothing | true      | 25.00 |
    When I visit the Home Page
    And I search for "Hat"
    Then I should see the message "Success"
    And I should see "Hat" in the Name
    And I should see "A red fedora" in the Description
    When I copy the product id from the search results
    And I retrieve the product by the copied id
    Then the product name should be "Hat"
    And the product description should be "A red fedora"
    And the product category should be "Clothing"
    And the product availability should be "true"
    And the product price should be "25.00"

  Scenario: Update a Product
    Given the following products
      | name | description  | category | available | price |
      | Hat  | A red fedora | Clothing | true      | 25.00 |
    When I visit the Home Page
    And I search for "Hat"
    And I copy the product id from the search results
    And I update the product with the copied id to have name "Updated Product"
    When I search for "Hat"
    Then I should not see "Hat" in the results
    When I search for "Updated Product"
    Then I should see "Updated Product" in the results
    And I should not see "Hat" in the results

  Scenario: Delete a Product
    Given the following products
      | name | description  | category | available | price |
      | Hat  | A red fedora | Clothing | true      | 25.00 |
    When I visit the Home Page
    And I search for "Hat"
    And I copy the product id from the search results
    And I delete the product with the copied id
    Then I should see the message "Product has been Deleted!"
    When I visit the Home Page
    And I clear all filters
    And I press the "Search" button
    Then I should not see "Hat" in the results

  Scenario: List All Products
    Given the following products
      | name    | description       | category    | available | price |
      | Hat     | A red fedora      | Clothing    | true      | 25.00 |
      | Shoes   | Running shoes     | Clothing    | true      | 50.00 |
      | Big Mac | A hamburger       | Food        | true      | 8.00  |
      | Sheets  | Bed sheets        | Housewares  | true      | 30.00 |
    When I visit the Home Page
    And I clear all filters
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the results
    And I should see "Shoes" in the results
    And I should see "Big Mac" in the results
    And I should see "Sheets" in the results

  Scenario: Search Products by Category
    Given the following products
      | name    | description       | category    | available | price |
      | Hat     | A red fedora      | Clothing    | true      | 25.00 |
      | Big Mac | A hamburger       | Food        | true      | 8.00  |
      | Shoes   | Running shoes     | Clothing    | true      | 50.00 |
    When I visit the Home Page
    And I clear all filters
    And I select "Food" from the category dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Big Mac" in the results
    And I should not see "Hat" in the results
    And I should not see "Shoes" in the results

  Scenario: Search Products by Availability
    Given the following products
      | name    | description       | category    | available | price |
      | Hat     | A red fedora      | Clothing    | true      | 25.00 |
      | Shoes   | Running shoes     | Clothing    | true      | 50.00 |
      | Big Mac | A hamburger       | Food        | false     | 8.00  |
    When I visit the Home Page
    And I clear all filters
    And I select "true" from the availability dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the results
    And I should see "Shoes" in the results
    And I should not see "Big Mac" in the results

  Scenario: Search Products by Name
    Given the following products
      | name | description  | category | available | price |
      | Hat  | A red fedora | Clothing | true      | 25.00 |
    When I visit the Home Page
    And I set the Name to "Hat"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hat" in the Name
    And I should see "A red fedora" in the Description
