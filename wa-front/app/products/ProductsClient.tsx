"use client";

import { useState, useMemo } from "react";
import ProductCard from "../components/ProductCard";
import Link from "next/link";

export default function ProductsClient({ products }: any) {
    const [query, setQuery] = useState("");

    const filteredProducts = useMemo(() => {
        if (!query.trim()) return products;

        return products.filter((product: any) =>
            product.title
                ?.toLowerCase()
                .includes(query.toLowerCase())
        );

    }, [query, products]);

    return (
        <div>
            <input
                type="text"
                placeholder="Search products..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full p-3 border rounded-lg mb-6 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">

                {filteredProducts.length > 0 ? (

                    filteredProducts.map((product: any) => (
                        <Link href={`/products/${product.id}`} key={product.id}>
                            <ProductCard
                                product={product} />
                        </Link>

                    ))

                ) : (

                    <p className="text-gray-500">
                        No products found
                    </p>

                )}

            </div>
        </div>
    );
}