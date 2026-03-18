from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

import models
from models import IdeaStatus
from database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LearnOS API", version="0.0.3", description="个人能力进化引擎 MVP")


class IdeaCreate(BaseModel):
    text: str

class IdeaResponse(BaseModel):
    id: int
    text: str
    status: IdeaStatus
    
    class Config:
        from_attributes = True

class FlowModuleResponse(BaseModel):
    id: int
    name: str
    pros: Optional[str]
    cons: Optional[str]
    market_status: Optional[str]
    core_knowledge: Optional[str]

    class Config:
        from_attributes = True

class FlowOptionResponse(BaseModel):
    id: int
    name: str
    modules: List[FlowModuleResponse]

    class Config:
        from_attributes = True



@app.post("/ideas", response_model=IdeaResponse, tags=["1. 想法靶场 (Idea Vault)"])
def create_idea(idea: IdeaCreate, db: Session = Depends(get_db)):
    """步骤 1：捕获灵感，存入避难所 (状态为 CAPTURED)"""
    new_idea = models.Idea(text=idea.text, status=IdeaStatus.CAPTURED)
    db.add(new_idea)
    db.commit()
    db.refresh(new_idea)
    return new_idea

@app.post("/ideas/{idea_id}/analyze", tags=["2. 智能顾问 (AI Engine)"])
def analyze_idea(idea_id: int, db: Session = Depends(get_db)):
    """步骤 2：用户点击【精进】，AI 顾问介入，给出可能的流程选项"""

    idea = db.query(models.Idea).filter(models.Idea.id == idea_id).first()
    if not idea:
        raise HTTPException(status_code=404, detail="没找到这个想法")
    
    idea.status = IdeaStatus.ANALYZING
    db.commit()

    return {
        "message": "AI 分析完毕，您想革新日程规划，建议从以下两个方向切入：",
        "options":[
            {"flow_id": 1, "name": "AI 极简全自动排期流 (重算法)"},
            {"flow_id": 2, "name": "Web3 社交对赌打卡流 (重机制)"}
        ]
    }

@app.get("/flows/{flow_id}/modules", response_model=List[FlowModuleResponse], tags=["3. 行业透视 (Flow & Modules)"])
def get_flow_modules(flow_id: int, db: Session = Depends(get_db)):
    """步骤 3：确立流程后，拉取该流程下的所有功能模块（用于悬停显示利弊）"""
    modules = db.query(models.FlowModule).filter(models.FlowModule.flow_id == flow_id).all()
    return modules

@app.post("/seed", tags=["0. 系统基建"])
def seed_database(db: Session = Depends(get_db)):
    """初始化数据库：注入 8大领域 和 1个标准的日程规划流程 (仅供测试使用)"""
   
    if db.query(models.Domain).first():
        return {"message": "知识库已存在，无需重复注入"}

   
    d1 = models.Domain(name="AI/ML 深度学习", description="核心突破口")
    db.add(d1)
    db.commit()

   
    f1 = models.DomainFlow(name="AI 极简全自动排期流 (重算法)", domain_id=d1.id)
    db.add(f1)
    db.commit()

   
    modules_data =[
        models.FlowModule(
            flow_id=f1.id, name="收集任务", 
            pros="门槛低，用户极易上手", cons="容易变成垃圾堆，用户记完就忘", 
            market_status="极其内卷 (Todoist, 滴答清单已霸占)", core_knowledge="数据结构与离散数学"
        ),
        models.FlowModule(
            flow_id=f1.id, name="AI 排期预测引擎", 
            pros="真正的壁垒，能极大降低用户认知负担", cons="冷启动困难，需要大量用户行为数据", 
            market_status="蓝海，目前多数为伪智能", core_knowledge="强化学习与运筹学优化算法"
        )
    ]
    db.add_all(modules_data)
    db.commit()

    return {"message": "✅ 8大领域与测试流程已成功注入大厦！"}