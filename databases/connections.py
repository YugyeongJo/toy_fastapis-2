from typing import Any, List, Optional

from beanie import init_beanie, PydanticObjectId
from models.users import User
from models.events import Event
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
# 변경 후 코드
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    
    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(),
                          document_models=[User, Event])

    class Config:
        env_file = ".env"

from utils.paginations import Paginations
import json
class Database:
    # model 즉 collection
    def __init__(self, model) -> None:
        self.model = model
        pass       

    # 전체 리스트
    async def get_all(self) :
        documents = await self.model.find_all().to_list()   # find({})
        pass
        return documents
    
    # 상세 보기
    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)  # find_one()
        if doc:
            return doc
        return False    
    
    # 저장
    async def save(self, document) -> None:
        await document.create()
        return None   
     
    # column 값으로 여러 Documents 가져오기
    async def getsbyconditions(self, conditions:dict) -> [Any]:
        documents = await self.model.find(conditions).to_list()  # find({})
        if documents:
            return documents
        return False    
    
    async def getsbyconditionswithpagination(self
                                             , conditions:dict, page_number) -> [Any]:
        # find({})
        total = await self.model.find(conditions).count()
        pagination = Paginations(total_records=total, current_page=page_number)
        documents = await self.model.find(conditions).skip(pagination.start_record_number).limit(pagination.records_per_page).to_list()
        if documents:
            return documents, pagination
        return False    
    
    async def delete(self, id: PydanticObjectId):
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True

    # update with params json
    async def update_withjson(self, id: PydanticObjectId, body: json):
        doc_id = id

        # des_body = {k: v for k, v in des_body.items() if v is not None}
        # {**body}는 Python의 딕셔너리 언패킹(unpacking) 기능을 사용한 부분입니다. 
        # 이 코드에서 body는 json 형식으로 전달된 데이터를 나타내는 변수입니다. 
        # body 변수에는 업데이트할 필드와 값을 포함하는 딕셔너리가 전달됩니다.
        # {**body}는 이 딕셔너리를 언패킹하여 새로운 딕셔너리를 생성하는 역할을 합니다. 
        # 이렇게 생성된 딕셔너리는 MongoDB의 업데이트 쿼리에 사용됩니다. 
        # MongoDB의 $set 연산자를 사용하여 업데이트할 필드와 값을 지정하는데, {**body}를 사용하면 body 딕셔너리의 모든 키-값 쌍이 $set 연산자에 포함되어 업데이트되는 쿼리가 생성됩니다.
        # 즉, {**body}는 body 딕셔너리의 키-값 쌍을 언패킹하여 새로운 딕셔너리를 생성하는 역할을 합니다.
        update_query = {"$set": {**body}}

        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc

if __name__ == '__main__':
    settings = Settings()
    async def init_db():
        await settings.initialize_database()

    collection_user = Database(User)
    conditions = "{ name: { $regex: '이' } }"
    list = collection_user.getsbyconditions(conditions)
    pass