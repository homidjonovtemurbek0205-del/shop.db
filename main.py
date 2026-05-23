from sqlalchemy import create_engine, Integer, String, select, ForeignKey, Numeric, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship, selectinload
from decimal import Decimal

engine = create_engine("sqlite:///online_shop.db")

class Base(DeclarativeBase):
    pass

product_category = Table(
    "product_category",
    Base.metadata,
    Column("product_id", ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
)

class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    nomi: Mapped[str] = mapped_column(unique=True)
    narxi: Mapped[Decimal] = mapped_column(Numeric(precision=19, scale=2))
    miqdori: Mapped[int] = mapped_column(Integer)

    categories: Mapped[list['Category']] = relationship(
        secondary=product_category, 
        back_populates="products"
    )

class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    nomi: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(String)

    products: Mapped[list['Product']] = relationship(
        secondary=product_category, 
        back_populates="categories"
    )

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

with Session(engine) as session:
    p1 = Product(nomi='iPhone 15 Pro', narxi=Decimal('1200.00'), miqdori=10)
    p2 = Product(nomi='Samsung Galaxy S24', narxi=Decimal('1000.00'), miqdori=15)
    p3 = Product(nomi='MacBook Pro 14', narxi=Decimal('2000.00'), miqdori=7)
    p4 = Product(nomi='Smart Televizor LG', narxi=Decimal('650.00'), miqdori=12)
    p5 = Product(nomi='Robot Changyutgich', narxi=Decimal('400.00'), miqdori=20)

    c1 = Category(nomi="Elektronika", description="Barcha turdagi elektron jihozlar")
    c2 = Category(nomi="Smartfonlar", description="Mobil aloqa qurilmalari")
    c3 = Category(nomi="Kompyuterlar", description="Noutbuk va orgtexnika")
    c4 = Category(nomi="Maishiy Texnika", description="Uy ro'zg'or uchun texnikalar")

    p1.categories.extend([c1, c2])
    p2.categories.extend([c1, c2])
    p3.categories.extend([c1, c3])
    p4.categories.extend([c1, c4])
    p5.categories.extend([c1, c4])

    session.add_all([p1, p2, p3, p4, p5, c1, c2, c3, c4])
    session.commit()


with Session(engine) as session:
    stmt = select(Product).options(selectinload(Product.categories))
    products = session.scalars(stmt).all()
    for prod in products:
        cats = ", ".join([cat.nomi for cat in prod.categories])
        print(f"Mahsulot: {prod.nomi} | Narxi: ${prod.narxi} | Miqdori: {prod.miqdori} ta")
        print(f"  Kategoriyalari: {cats}\n")

with Session(engine) as session:
    stmt = select(Category).options(selectinload(Category.products))
    categories = session.scalars(stmt).all()
    for cat in categories:
        prods = ", ".join([prod.nomi for prod in cat.products])
        print(f"Kategoriya: {cat.nomi} ({cat.description})")
        print(f"  Mahsulotlar: {prods}\n")

with Session(engine) as session:
    stmt = select(Category).where(Category.nomi == "Smartfonlar").options(selectinload(Category.products))
    category = session.scalars(stmt).first()
    if category:
        print(f"Kategoriya: {category.nomi}")
        for prod in category.products:
            print(f"  - {prod.nomi} | ${prod.narxi}")
print()

with Session(engine) as session:
    stmt = select(Product).where(Product.nomi == "iPhone 15 Pro").options(selectinload(Product.categories))
    product = session.scalars(stmt).first()
    if product:
        print(f"Mahsulot: {product.nomi}")
        for cat in product.categories:
            print(f"  - {cat.nomi}: {cat.description}")