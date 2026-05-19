import Link from "next/link";

export default function Appbar() {
  return (
    <nav className="flex gap-5">
      <Link href="/">Home</Link>
      <Link href="/chat">Chat</Link>
      <Link href="/products">Products</Link>
      <Link href="/collection">Collections</Link>
    </nav>
  );
}