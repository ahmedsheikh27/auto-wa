from agents import function_tool
from app.services.product_service import (
    get_all_products,
    search_products,
    get_all_collections,
    search_collection_products,
)
from app.db.session import SessionLocal


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
        result = await search_products(db, query)

        if not result:
            return "No products found, try different name or category."

        products = []

        for i, p in enumerate(result, start=1):
            products.append(f"{i}. {p.title} {p.id}")

        return "\n".join(products)

    except Exception as exc:
        return {"success": False, "error": str(exc)}



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
        result = await get_all_products(db)

        if not result:
            return "No products in database."

        products = []

        for i, p in enumerate(result, start=1):
            products.append(
                f"{i}. Product Name: {p.title}\n"
                f"{i}. Product Name: {p.id}\n"
                f"Product Desc: {p.description}\n"
            )

        return "\n".join(products)

    except Exception as exc:
        return {"success": False, "error": str(exc)}



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
        result = await get_all_collections(db)

        if not result:
            return "No collection found."

        collections = []

        for i, c in enumerate(result, start=1):
            collections.append(
                f"{i}. Collection Name: {c.title}\n"
                f"Collection Desc: {c.description}\n"
            )

        return "\n".join(collections)

    except Exception as exc:
        return {"success": False, "error": str(exc)}



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
        collections = await search_collection_products(db, query)

        if not collections:
            return "No collections found."

        responses = []

        for collection in collections:

            col_title = collection.title
            col_products = collection.products

            if not col_products:
                continue

            response = f"{col_title}\n"

            for i, product in enumerate(col_products[:5], start=1):
                response += (
                    f"\n{i}. {product.title}\n"
                    f"\n{i}. {product.id}\n"
                    f"{product.description}\n"
                )

            responses.append(response)

        if not responses:
            return "No products found in collections."

        final_response = "\n\n".join(responses)

        return final_response

    except Exception as exc:
        return {"success": False, "error": str(exc)}