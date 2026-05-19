import OrderViaWhatsapp from "@/app/components/OrderViaWhatsapp";
import { getAllProducts } from "@/app/service/api";

export default async function ProductPage({ params }: any) {

    const { id } = await params;

    const products = await getAllProducts();

    const product = products.find(
        (p: any) => p.id === Number(id)
    );

    if (!product) {
        return <div>Product not found</div>;
    }
    
    return (
        <div className="p-6">

            <h1 className="text-3xl font-bold">
                {product.title}
            </h1>

            <p className="mt-4 text-gray-500">
                {product.description}
            </p>
            <OrderViaWhatsapp  product={product}/>
        </div>
    );
}