# main.py
from contextlib import asynccontextmanager
from typing import Union, Optional, List
from datetime import datetime
from decimal import Decimal
from app import settings
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware


# Database Models
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True)
    full_name: str
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    price: Decimal = Field(decimal_places=2)
    stock_quantity: int = Field(default=0)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    total_amount: Decimal = Field(decimal_places=2)
    status: str = Field(default="pending")  # pending, confirmed, shipped, delivered, cancelled
    created_at: datetime = Field(default_factory=datetime.utcnow)


# Database setup
connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

engine = create_engine(
    connection_string, 
    connect_args={"sslmode": "require"} if "localhost" not in str(settings.DATABASE_URL) else {},
    pool_recycle=300
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database tables...")
    create_db_and_tables()
    print("Database tables created successfully!")
    yield
    print("Application shutdown")


app = FastAPI(
    title="Ecommerce Backend API",
    description="A professional FastAPI ecommerce backend with PostgreSQL",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/")
def read_root():
    return {
        "message": "Ecommerce Backend API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}


# User endpoints
@app.post("/users/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get("/users/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    users = session.exec(select(User).offset(skip).limit(limit)).all()
    return users


# Category endpoints
@app.post("/categories/", response_model=Category)
def create_category(category: Category, session: Session = Depends(get_session)):
    db_category = Category.model_validate(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@app.get("/categories/", response_model=List[Category])
def read_categories(session: Session = Depends(get_session)):
    categories = session.exec(select(Category).where(Category.is_active == True)).all()
    return categories


# Product endpoints
@app.post("/products/", response_model=Product)
def create_product(product: Product, session: Session = Depends(get_session)):
    db_product = Product.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@app.get("/products/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    products = session.exec(
        select(Product).where(Product.is_active == True).offset(skip).limit(limit)
    ).all()
    return products


@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product or not product.is_active:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
