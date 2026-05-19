'use client'

export default function ProductCard({ product }: any) {

  return (
    <div className="border rounded-xl p-4 shadow-sm hover:shadow-lg transition bg-white">

      <h2 className="text-lg font-semibold text-gray-800">
        {product.title}
      </h2>
      <p className="text-sm text-gray-500 mt-1">
        {product.description}
      </p>
    </div>
  );
}