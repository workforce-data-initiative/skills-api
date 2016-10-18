from app import app
from factory import alchemy, LazyAttribute, Sequence
from api.v1 import Geography, Quarter, JobImportance, JobMaster
from faker import Faker

fake = Faker()


class JobMasterFactory(alchemy.SQLAlchemyModelFactory):
    class Meta(object):
        model = JobMaster
        sqlalchemy_session = app.db.session

    uuid = Sequence(lambda n: str(n))
    onet_soc_code = LazyAttribute(lambda x: fake.phone_number())
    title = LazyAttribute(lambda x: fake.job())
    original_title = LazyAttribute(lambda x: fake.job())
    description = LazyAttribute(lambda x: fake.job())
    nlp_a = LazyAttribute(lambda x: fake.job())


class GeographyFactory(alchemy.SQLAlchemyModelFactory):
    class Meta(object):
        model = Geography
        sqlalchemy_session = app.db.session

    geography_id = Sequence(lambda x: x)
    geography_type = 'CBSA'
    geography_name = LazyAttribute(lambda x: fake.phone_number())


class QuarterFactory(alchemy.SQLAlchemyModelFactory):
    class Meta(object):
        model = Quarter
        sqlalchemy_session = app.db.session

    quarter_id = Sequence(lambda x: x)
    quarter = '3'
    year = '2016'


class JobImportanceFactory(alchemy.SQLAlchemyModelFactory):
    class Meta(object):
        model = JobImportance
        sqlalchemy_session = app.db.session

    importance = 0.2
