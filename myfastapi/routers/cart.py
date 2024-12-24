from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..services import CartService
from ..database import get_db
from ..schemas import CartItemCreate, CartItem

router = APIRouter()

@router.get("/cart-items", response_model=list)
def read_cart_items(db: Session = Depends(get_db)):
    """Get all carts (for demonstration)."""
    return CartService.get_cart_items()

@router.get("/cart/{user_id}", response_model=dict)
def read_user_cart(user_id: int, db: Session = Depends(get_db)):
    cart = CartService.get_user_cart(user_id)
    # Return in a dict for demonstration; you could also create a custom response model
    return {
        "id": cart.id,
        "user_id": cart.user_id,
        "items": cart.items
    }

@router.post("/cart/{user_id}/items", response_model=CartItem)
def add_item_to_cart(user_id: int, item: CartItemCreate, db: Session = Depends(get_db)):
    return CartService.add_item(item, user_id)

@router.put("/cart/{user_id}/items/{product_id}", response_model=CartItem)
def update_cart_item(user_id: int, product_id: int, item: CartItemCreate, db: Session = Depends(get_db)):
    return CartService.update_item(product_id, item, user_id)

@router.delete("/cart/{user_id}/items", response_model=dict)
def clear_cart(user_id: int, db: Session = Depends(get_db)):
    return CartService.clear_cart(user_id)

@router.delete("/cart/{user_id}/items/{product_id}", response_model=dict)
def remove_item_from_cart(user_id: int, product_id: int, db: Session = Depends(get_db)):
    return CartService.remove_item(product_id, user_id)
