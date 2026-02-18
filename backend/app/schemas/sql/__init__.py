"""
User Schema Design Pattern (Pydantic v2)
========================================

This module demonstrates a scalable and maintainable approach to designing Pydantic schemas for your models, especially when working with FastAPI and SQLAlchemy.

General Schema Types:
---------------------
1. **Base Schema (`UserBase`)**
   - Contains all shared fields for the model.
   - Used as a parent for other schemas.
   - Enables ORM mode with `model_config = ConfigDict(from_attributes=True)` for compatibility with SQLAlchemy ORM objects.

2. **Create Schema (`UserCreate`)**
   - Inherits from Base.
   - Adds fields required for creation (e.g., `password`).
   - Used for POST endpoints (user registration, etc.).

3. **Update Schema (`UserUpdate`)**
   - Inherits from Base.
   - Makes fields optional for partial updates.
   - Used for PATCH/PUT endpoints.

4. **InDB Schema (`UserInDB`)**
   - Inherits from Base.
   - Adds internal fields stored in the database (e.g., `id`, `hashed_password`).
   - Not intended for public API responses.

5. **Read Schema (`UserRead`)**
   - Inherits from Base.
   - Adds fields returned in API responses (e.g., `id`).
   - Used for GET endpoints (public API response).

Summary Table:
--------------
| Schema      | Purpose                | Includes `id` | Includes `hashed_password` | For API Response? |
|-------------|------------------------|---------------|---------------------------|-------------------|
| UserBase    | Shared fields          | No            | No                        | No                |
| UserCreate  | Registration input     | No            | No                        | No                |
| UserUpdate  | Update input           | No            | No                        | No                |
| UserInDB    | Internal DB use        | Yes           | Yes                       | No                |
| UserRead    | API response           | Yes           | No                        | Yes               |

This pattern keeps your code DRY, clear, and secure—ensuring you never expose sensitive fields (like `hashed_password`) in API responses, and always have the right schema for each use case.
"""

from .token import Token, TokenPayload, NewPassword, UpdatePassword
from .user import User, UserBase, UserCreate, UserInDBase, UserUpdate
from .device import Device, DeviceBase, DeviceCreate, DeviceInDB, DeviceUpdate
