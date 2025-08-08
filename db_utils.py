from sqlalchemy import create_engine, Column, Text, String, Numeric, TIMESTAMP, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone
import json
from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class BuySellCyprus2(Base):
    __tablename__ = "buysellcyprus2"
    id = Column(String(50), primary_key=True)
    link = Column(String(255))
    date = Column(TIMESTAMP, default=datetime.now(timezone.utc), nullable=False)
    title = Column(Text)
    description = Column(Text)
    price = Column(Numeric(15, 2))
    region = Column(String(100))
    city = Column(String(100))
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    photos = Column(JSON)
    key_features = Column(Text)
    agency = Column(String(255))
    registration_and_license = Column(String(200))

def insert_rows_to_db(rows):
    session = Session()
    try:
        for row in rows:
            record = BuySellCyprus2(
                id=row["id"],
                link=row["link"],
                title=row["title"],
                price=row["price"],
                region=row["region"],
                city=row["city"],
                latitude=row.get("latitude"),
                longitude=row.get("longitude"),
                description=row["description"],
                photos=json.loads(row["photos"]) if isinstance(row["photos"], str) else row["photos"],
                key_features=json.dumps(row["key_features"]) if isinstance(row["key_features"], list) else row["key_features"],
                agency=row["agency"],
                registration_and_license=row["registration_and_license"],
                date=datetime.now(timezone.utc)
            )
            try:
                session.merge(record)
            except Exception as e:
                print(f"Ошибка вставки {row['link']}: {e}")
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Ошибка коммита: {e}")
    finally:
        session.close()