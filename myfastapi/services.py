from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from typing import List

from .database import db_session
from .models import Cart, CartItem, Order, OrderItem
from .schemas import CartItemCreate

class CartService:
    @staticmethod
    def get_cart_items() -> List[Cart]:
        with db_session() as session:
            return session.query(Cart).all()

    @staticmethod
    def get_user_cart(user_id: int) -> Cart:
        with db_session() as session:
            cart = session.query(Cart).filter(Cart.user_id == user_id).first()
            if not cart:
                raise HTTPException(status_code=404, detail="Cart not found")
            return cart

    @staticmethod
    def add_item(item: CartItemCreate, user_id: int) -> CartItem:
        with db_session() as session:
            cart = session.query(Cart).filter(Cart.user_id == user_id).first()
            if not cart:
                cart = Cart(user_id=user_id)
                session.add(cart)
                session.commit()
                session.refresh(cart)

            cart_item = CartItem(
                cart_id=cart.id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            session.add(cart_item)
            session.commit()
            session.refresh(cart_item)
            return cart_item

    @staticmethod
    def update_item(product_id: int, item: CartItemCreate, user_id: int) -> CartItem:
        with db_session() as session:
            cart_item = (session.query(CartItem)
                         .join(Cart)
                         .filter(Cart.user_id == user_id)
                         .filter(CartItem.product_id == product_id)
                         .first())
            if not cart_item:
                raise HTTPException(status_code=404, detail="Item not found")

            cart_item.quantity = item.quantity
            session.commit()
            session.refresh(cart_item)
            return cart_item

    @staticmethod
    def clear_cart(user_id: int) -> dict:
        with db_session() as session:
            cart = session.query(Cart).filter(Cart.user_id == user_id).first()
            if cart:
                session.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
                session.commit()
            return {"message": "Cart cleared"}

    @staticmethod
    def remove_item(product_id: int, user_id: int) -> dict:
        with db_session() as session:
            cart_item = (session.query(CartItem)
                         .join(Cart)
                         .filter(Cart.user_id == user_id)
                         .filter(CartItem.product_id == product_id)
                         .first())
            if not cart_item:
                raise HTTPException(status_code=404, detail="Item not found")

            session.delete(cart_item)
            session.commit()
            return {"message": "Item removed"}

class OrderService:
    @staticmethod
    def get_all_orders() -> List[Order]:
        with db_session() as session:
            return session.query(Order).all()

    @staticmethod
    def get_order(order_id: int) -> Order:
        with db_session() as session:
            order = session.query(Order).filter(Order.id == order_id).first()
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")
            return order

    @staticmethod
    def create_order(user_id: int) -> Order:
        with db_session() as session:
            cart = session.query(Cart).filter(Cart.user_id == user_id).first()
            if not cart or not cart.items:
                raise HTTPException(status_code=400, detail="Cart is empty")

            order = Order(
                user_id=user_id,
                created_at=datetime.utcnow()
            )
            session.add(order)
            session.flush()

            for item in cart.items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=OrderService._get_product_price(item.product_id)
                )
                session.add(order_item)

            session.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
            session.commit()
            session.refresh(order)
            return order

    @staticmethod
    def remove_order(order_id: int) -> dict:
        with db_session() as session:
            order = session.query(Order).filter(Order.id == order_id).first()
            if not order:
                raise HTTPException(status_code=404, detail="Order not found")

            session.delete(order)
            session.commit()
            return {"message": "Order removed"}

    @staticmethod
    def _get_product_price(product_id: int) -> float:
        # Implement your real price fetching logic here
        return 0.0
