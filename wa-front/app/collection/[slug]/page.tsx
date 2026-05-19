import ProductCard from "@/app/components/ProductCard";
import { getCollectionProducts } from "@/app/service/api";
import Link from "next/link";

export default async function CollectionProductsPage({ params }: any) {
  const { slug } = await params;
  const data = await getCollectionProducts(slug);

  const collection = data.collection;
  const products = data.products;

  return (
    <div className="p-6">
      <h2 className="text-lg font-semibold text-gray-800">
        {collection?.title}
      </h2>
      <p className="text-sm text-gray-500 mt-1">
        {collection?.description}
      </p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {products.map((product: any) => (
          <Link href={`/products/${product.id}`} key={product.id} >
            <ProductCard
              product={product} />
          </Link>
        ))}
      </div>
    </div>
  );
}