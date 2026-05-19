import Link from "next/link";

export default function CollectionCard({ collection }: any) {
  if (!collection?.id) return null;
  return (
    <Link href={`/collection/${collection.slug}`}>
      <div className="border rounded-xl p-6 shadow-sm hover:shadow-lg transition cursor-pointer">
        <h2 className="text-xl font-semibold">
          {collection.title}
        </h2>

        <p className="text-gray-500 mt-2">
          {collection.description}
        </p>
      </div>
    </Link>
  );
}