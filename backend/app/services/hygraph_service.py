import httpx
from app.core.config import Settings

HYGRAPH_URL = Settings.HYGRAPH_URL

HEADERS = {
    "Content-Type": "application/json",
    # "Authorization": "Bearer YOUR_TOKEN" (if needed)
}

#  GET ALL PRODUCTS
async def get_products():
    query = """
    query GetProducts {
      products() {
        id
        title
        slug
        description
      }
    }
    """

    async with httpx.AsyncClient() as client:
        res = await client.post(
            HYGRAPH_URL,
            json={"query": query},
            headers=HEADERS
        )

    return res.json()["data"]["products"]

async def search_products(query_text: str):
    query = """
    query GetProducts($q: String!) {
      products(where: { title_contains: $q }) {
        id
        title
        slug
        description
      }
    }
    """

    async with httpx.AsyncClient() as client:
        res = await client.post(
            HYGRAPH_URL,
            json={
                "query": query,
                "variables": {"q": query_text}
            },
            headers=HEADERS
        )

    return res.json()["data"]["products"]

async def get_product_by_slug(slug: str):
    query = """
    query GetProductBySlug($slug: String!) {
      product(where: { slug: $slug }) {
        id
        title
        description
      }
    }
    """

    async with httpx.AsyncClient() as client:
        res = await client.post(
            HYGRAPH_URL,
            json={
                "query": query,
                "variables": {"slug": slug}
            },
            headers=HEADERS
        )

    return res.json()["data"]["product"]