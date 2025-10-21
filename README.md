# -E-commerce

# Introduction
  
 I have created an app/website called E-Commerce.This E-Commerce app has four roles: Admin, Vendor, Customer, and Home Delivery.
 In my E-Commerce app, I have implemented Django group-based permissions.
 
 # Installation
 1 django.contrib.admin
 2 django.contrib.auth
 3 django.contrib.contenttypes
 4 django.contrib.sessions
 5 django.contrib.messages
 6 django.contrib.staticfiles
 7 Account
 8 rest_framework
 9 product
 10 category
 11 wishlist
 12 cart
 13 django_filters
 14 checkout
 15 cashcard

 # User Registration

Users can register using the following steps:
There are three roles in the registration system:Vendor Customer Delivery Boy.
1 Vendor – manages  category products and sales.
2 Customer – browses and purchases items.
3 Delivery Boy – handles product delivery to customers.

Open the registration page:
   - username
   - email
   - role
   - user_profile
   - address
   - password
After completing the registration, a confirmation message will be sent to the user’s registered email address.
In the system, only one account can be created per email. If someone tries to register again using the same email, this message will appear: ‘This email is already registered.
If the username or password is incorrect, the following message will be displayed:{"error": "Invalid credentials"}

# categories 
Only users with the role of Vendor can create categories.
If multiple vendors exist in the system (Vendor A and Vendor B), each vendor can manage only the categories they have created. A vendor cannot update or delete categories created by another vendor.
Users with the role Customer are not allowed to create or post categories. If a customer attempts to perform this action, the system returns the following response:{
    "detail": "You do not have permission to perform this action."
}
Users with the role Delivery Boy are not permitted to create or post categories. If a delivery boy attempts to do so, the system will return the following response:{
    "detail": "You do not have permission to perform this action."
}
Users with the role Customer are allowed to view all categories in the system. However, they cannot create, update, or delete any category.

# product
If a user’s role is Vendor, they can create products.
If multiple vendors exist in the system (e.g., Vendor A and Vendor B), each vendor can add products only to their own categories.
If a vendor attempts to add a product to another vendor’s category, the system will return the following response:{
  "category_name": "You cannot add a product to another vendor's category."
}
Users with the role Customer are not allowed to create products. If a customer attempts to perform this action, the system returns the following response:
{
  "detail": "You do not have permission to perform this action."
}
Users with the role Delivery Boy are not permitted to create products. If a delivery boy attempts to perform this action, the system will return the following response:
{
  "detail": "You do not have permission to perform this action."
}

# Cart
When a customer creates a cart, they have access to view the full category.
For example, if a product variant named A has a total quantity of 10, and the customer buys 4, then 6 will remain in the main stock (category).

If a user initially adds 3 items from a product variant in a category, and later updates the quantity to 0 in a PATCH request, the system will return the error message:
"Quantity 0 or negative is not allowed."

If a category’s variant has a total of 40 items, and a customer already has 6 items in their cart, but then sends a PATCH request saying they want 50 items, the system will return this message:
{ "error": "Only 34 more available in stock." }

A customer has added items with variant_id = 10 to their cart. Now the customer wants to change it to variant_id = 9. But in the cart, only item quantities can be updated — not the variant ID.
So if the customer tries to do that, the system will return this message:
{ "error": "Variant ID 9 not found in this cart." }


If a category has only 7 variants available, but a customer tries to apply (or request) 10 variants, the system will return this message:
{ "error": "Only 7 variants available in this category." }

If a customer has created a cart and later deletes it, then the items from that cart will be restored back to the main category’s stock.
The system will return this message:
{ "message": "Cart deleted and stock restored successfully." }

If a customer tries to delete a cart with ID 5, but that cart does not exist in the system, the system will return this message:
{ "error": "Cart not found." }

# Wishlist
