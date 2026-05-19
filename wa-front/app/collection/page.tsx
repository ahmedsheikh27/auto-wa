import CollectionCard from "../components/CollectionCard";
import { getAllCollections } from "../service/api";


export default async function CollectionsPage() {
    const collections = await getAllCollections();
    console.log(collections)
    return (
        <div className="p-6">
            <h1 className="text-3xl font-bold mb-6">
                Collections
            </h1>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                {collections.map((collection: any) => (
                    <CollectionCard
                        key={collection.id}
                        collection={collection}
                    />
                ))}
            </div>
        </div>
    );
}