import { getAllProducts } from "../service/api";
import ProductsClient from "./ProductsClient";


export default async function ProductsPage() {
    const products = await getAllProducts();

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4">Products</h1>
            <ProductsClient products={products} />
        </div>
    );
}