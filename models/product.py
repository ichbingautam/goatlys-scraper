from typing import List, Optional, Annotated
from pydantic import BaseModel, Field

class Product(BaseModel):
  product_title: str = Field(..., title="Product Title")
  product_price: float = Field(..., title="Product Price", ge=0)
  path_to_image: str = Field(..., title="Path to Image")