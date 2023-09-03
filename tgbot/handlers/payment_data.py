import stripe
import os
stripe.api_key = os.getenv('STRIPE_KEY')

stripe_customer = stripe.Customer.create(
  description="My First Test Customer (created for API docs at https://www.stripe.com/docs/api)",
)
