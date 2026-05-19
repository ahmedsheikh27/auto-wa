const BASE_URL = "http://localhost:8000";
export async function getAllProducts() {
  const res = await fetch(`${BASE_URL}/products`, {
    method: "GET",
    cache: "no-store",
  });

  if (!res.ok) throw new Error("Failed to fetch products");
  return res.json();
}
export async function getProductById(id: any) {
  const res = await fetch(
    `${BASE_URL}/product/${id}`,
    {
      cache: "no-store",
    }
  );

  if (!res.ok) {
    const errorText = await res.text();
    console.log(errorText);
  }

  return res.json();
}
export async function searchProducts(query: string) {
  const res = await fetch(
    `${BASE_URL}/products/search?query=${encodeURIComponent(query)}`,
    {
      method: "GET",
      cache: "no-store",
    }
  );

  if (!res.ok) throw new Error("Search failed");
  return res.json();
}

export async function getAllCollections() {
  const res = await fetch(`${BASE_URL}/collection`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch collections");
  }

  return res.json();
}

export async function getCollectionProducts(slug: any) {
  const res = await fetch(
    `${BASE_URL}/collection/${slug}`,
    {
      cache: "no-store",
    }
  );

  if (!res.ok) {
    const errorText = await res.text();
    console.log(errorText);
  }

  return res.json();
}