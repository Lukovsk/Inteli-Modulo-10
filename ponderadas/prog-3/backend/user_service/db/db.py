import databases
import ormar
import sqlalchemy

# database = databases.Database("postgresql://lukovsk:3569@db:5432/postgres")
database = databases.Database("sqlite:///db.db")
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=128, unique=True, nullable=False)
    email: str = ormar.String(max_length=128, unique=True, nullable=False)
    password: str = ormar.String(max_length=16, nullable=False)
    image_url: str = ormar.String(max_length=256, nullable=True)


engine = sqlalchemy.create_engine("sqlite:///db.db")
# engine = sqlalchemy.create_engine(settings.db_url)
# metadata.drop_all(engine)
metadata.create_all(engine)
