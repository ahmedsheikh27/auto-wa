from agents import function_tool
from app.db.session import SessionLocal
from app.sdk import create_sdk


@function_tool(
    name_override="product_search_tool",
    description_override="Search for products based on user query",
)
async def product_search_tool(query: str):
    """
    Search for products based on user query
    """

    print(f"product_search_tool called: {query}")

    db = SessionLocal()

    try:
        result = create_sdk(db).products.search(query)

        if not result:
            return "No products found, try different name or category."

        products = []

        for i, product in enumerate(result, start=1):
            products.append(
                f"{i}. {product['title']} "
                f"(ID: {product['id']})\n"
                f"{product.get('description') or ''}"
            )

        return "\n".join(products)

    except Exception as exc:
        return {"success": False, "error": str(exc)}
    finally:
        db.close()



@function_tool(
    name_override="list_product_tool",
    description_override="List all products",
)
async def list_product_tool():
    """
    Get all products from database
    """

    print("list_product_tool called")

    db = SessionLocal()

    try:
        result = create_sdk(db).products.list()

        if not result:
            return "No products in database."

        products = []

        for i, product in enumerate(result, start=1):
            products.append(
                f"{i}. Product Name: {product['title']}\n"
                f"Product ID: {product['id']}\n"
                f"Product Desc: {product.get('description') or ''}\n"
            )

        return "\n".join(products)

    except Exception as exc:
        return {"success": False, "error": str(exc)}
    finally:
        db.close()



@function_tool(
    name_override="list_collections_tool",
    description_override="List all collections",
)
async def list_collections_tool():
    """
    Search all collections from database
    """

    print("list_collections_tool called")

    db = SessionLocal()

    try:
        result = create_sdk(db).collections.list()

        if not result:
            return "No collection found."

        collections = []

        for i, collection in enumerate(result, start=1):
            collections.append(
                f"{i}. Collection Name: {collection['title']}\n"
                f"Collection ID: {collection['id']}\n"
                f"Collection Slug: {collection.get('slug') or ''}\n"
                f"Collection Desc: {collection.get('description') or ''}\n"
            )

        return "\n".join(collections)

    except Exception as exc:
        return {"success": False, "error": str(exc)}
    finally:
        db.close()



@function_tool(
    name_override="search_collections_tool",
    description_override="Search collections and list products",
)
async def search_collections_tool(query: str):
    """
    Search collections and list products
    """

    print(f"search_collections_tool called: {query}")

    db = SessionLocal()

    try:
        collections = create_sdk(db).collections.search(query)

        if not collections:
            return "No collections found."

        responses = []

        for collection in collections:

            col_title = collection["title"]
            col_products = collection["products"]

            if not col_products:
                continue

            response = f"{col_title}\n"

            for i, product in enumerate(col_products[:5], start=1):
                response += (
                    f"\n{i}. {product['title']}\n"
                    f"ID: {product['id']}\n"
                    f"{product.get('description') or ''}\n"
                )

            responses.append(response)

        if not responses:
            return "No products found in collections."

        final_response = "\n\n".join(responses)

        return final_response

    except Exception as exc:
        return {"success": False, "error": str(exc)}
    finally:
        db.close()
