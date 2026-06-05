# SDK Reasoning

This file explains the SDK changes in simple English.

## Goal

We want users to connect this project to their own database without changing the agent or tool code.

For Mode 1, users must create the same database schema that our SDK defines. If the required tables or columns are missing, the SDK raises an error. If the database returns data in a different shape than our JSON output schema, the SDK raises an error.

This makes the project more reliable because the agents always receive the same JSON format.

## New SDK Structure

### app/sdk/schemas.py

This file defines the official JSON output format of the SDK.

It includes:

- UserOut
- ProductOut
- CollectionOut
- OrderItemInput
- OrderItemOut
- OrderOut
- MessageOut

We need this file because every database result must match these models before the agents or tools use it.

### app/sdk/exceptions.py

This file defines custom SDK errors.

It includes:

- SDKError
- DatabaseSchemaError
- SchemaValidationError

We need this file so the SDK can raise clear errors when the database schema or output is wrong.

### app/sdk/validators.py

This file validates database output against the schemas in schemas.py.

It includes:

- validate_output
- validate_list

We need this file so all adapters use the same validation behavior.

### app/sdk/interfaces.py

This file defines the adapter interface.

It tells every database adapter which functions it must implement, such as:

- list_products
- search_products
- list_collections
- get_user_by_phone
- create_order
- save_message

We need this file because PostgreSQL, MongoDB, or any future database should follow the same contract.

### app/sdk/adapters/postgres.py

This file implements the SDK adapter for the current PostgreSQL database.

It checks that these tables exist:

- users
- products
- collections
- orders
- order_items
- messages

It also checks that required columns exist in each table.

After reading or writing data, it converts SQLAlchemy objects into normal dictionaries and validates them with the SDK schemas.

We need this file because Mode 1 currently supports the standard PostgreSQL schema.

### app/sdk/client.py

This file exposes the clean SDK API.

It includes:

- EcommerceSDK
- ProductSDK
- CollectionSDK
- UserSDK
- MessageSDK
- OrderSDK
- create_sdk

Tools should call this SDK instead of directly using SQLAlchemy models.

We need this file because it gives the rest of the app one stable way to use ecommerce data.

## Why Tools Need To Change

The old tools called database services directly and returned custom strings or raw objects.

The new goal is that tools call the SDK first. The SDK checks the database schema, validates output, and returns clean JSON dictionaries.

This means the agent can trust the data format.

## Updated Existing Files

### app/tools/product_tool.py

The product tools now call the SDK instead of directly calling product services.

Changed functions:

- product_search_tool
- list_product_tool
- list_collections_tool
- search_collections_tool

These functions now open a database session, create the SDK, call the correct SDK method, and close the session.

We changed them because product and collection output must be validated before the agent uses it.

### app/tools/order_tool.py

The order tools now call the SDK instead of directly calling order services.

Changed functions:

- create_order_tool
- list_orders_by_phone_tool
- update_order_status_tool

These functions now receive validated order JSON from the SDK.

We changed them because order creation and order status output must follow the same JSON format every time.

### app/api/products.py

The products API now returns SDK product JSON.

Changed functions:

- list_products
- search

We changed this so API responses and agent tool responses use the same product format.

### app/api/collection.py

The collection API now returns SDK collection JSON.

Changed functions:

- list_collections
- collection_products

We changed this so collection output is validated and consistent.

### app/api/webhook.py

The webhook now uses the SDK to find or create users and save messages.

Changed function:

- whatsapp_webhook

We changed this so the main WhatsApp flow also uses the same SDK contract.

### app/api/messages.py

The test messages endpoint now accepts a phone number in the request body.

Changed function:

- send_messages

We changed this so sessions can be tested with different phone numbers.

### app/core/config.py

This file now includes Redis session settings.

Added settings:

- REDIS_URL
- SESSION_TTL_SECONDS

The AsyncOpenAI import was also updated to come from the openai package.

We need these settings because chat session memory uses Redis. We need the import change because AsyncOpenAI is provided by openai, not by agents.

### app/core/redis.py

This file now imports the shared settings object.

We changed this to keep config usage consistent.

### app/main.py

The direct Redis test call was removed from import time.

We changed this because the app should not call Redis just because the module is imported.

### requirements.txt

Added:

- redis

We need this because session_service.py imports Redis.

### .env.example

Added:

- APP_SECRET
- REDIS_URL
- SESSION_TTL_SECONDS

We need this so SDK users know which environment variables are required.

## Why This Helps Future Databases

Mode 1 only supports users who follow our exact schema.

Later, Mode 2 can add adapters for MongoDB or custom schemas. Those adapters can still return the same ProductOut, OrderOut, and UserOut models.

That means the agents and tools will not need to change when a new database is added.
