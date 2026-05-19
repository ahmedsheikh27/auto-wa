'use client'
import React, { useState } from 'react'

const OrderViaWhatsapp = ({product}: any) => {
    const [quantity, setQuantity] = useState<any>(1)

    const sendToWhatsApp = (product: any) => {
        const phone = process.env.NEXT_PUBLIC_PHONE_NUM;

        const message =
            `I want to orde this%0A` +
            `Product: ${product.title}%0A` +
            `ID: ${product.id}%0A` +
            `Quantity: ${quantity}`;

        const url = `https://wa.me/${phone}?text=${message}`;

        window.open(url, "_blank");
        setQuantity(1)
    };
  return (
    <div>
        <div className="flex gap-3 justify-between items-center">
                <button className="cursor-pointer" onClick={() => setQuantity(quantity - 1)}>-</button>
                <h4>{quantity}</h4>
                <button className="cursor-pointer" onClick={() => setQuantity(quantity + 1)}>+</button>
            </div>
            <button onClick={() => sendToWhatsApp(product)} className="mt-4 w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition">
                Order via Whatsapp
            </button>
    </div>
  )
}

export default OrderViaWhatsapp