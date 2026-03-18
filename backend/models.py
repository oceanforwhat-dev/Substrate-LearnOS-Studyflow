from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base

# ==========================================
# 状态机：精准控制一个想法的生命周期
# ==========================================
class IdeaStatus(str, enum.Enum):
    CAPTURED = "captured"     # 刚收集，在想法区沉睡
    ANALYZING = "analyzing"   # 用户点击深入，正在拆解流程
    ASSESSED = "assessed"     # 已经做完了能力质询，生成了雷达图
    STUDYING = "studying"     # 开启地狱学习计划
    SHELVED = "shelved"       # 搁置/放弃

# ==========================================
# 表 1：Domain (八大硬核领域)
# ==========================================
class Domain(Base):
    __tablename__ = "domains"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) # 如："AI/ML", "系统架构", "量化交易"
    description = Column(String)

# ==========================================
# 表 2：Idea (想法避难所)
# ==========================================
class Idea(Base):
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)                         # 用户的原始想法
    status = Column(Enum(IdeaStatus), default=IdeaStatus.CAPTURED) # 当前状态
    created_at = Column(DateTime, default=datetime.now)
    
    # 建立关系：一个想法最后会归属到一个领域，并对应一个具体的流程
    domain_id = Column(Integer, ForeignKey("domains.id"), nullable=True)
    selected_flow_id = Column(Integer, ForeignKey("domain_flows.id"), nullable=True)

# ==========================================
# 表 3：DomainFlow (行业标准流程模板)
# ==========================================
class DomainFlow(Base):
    __tablename__ = "domain_flows"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String) # 如："经典日程规划流程", "异步爬虫架构"
    
    # 关联：这个流程属于哪个领域？包含哪些功能模块？
    domain_id = Column(Integer, ForeignKey("domains.id"))
    modules = relationship("FlowModule", back_populates="flow")

# ==========================================
# 表 4：FlowModule (悬停透视镜 - 流程功能节点)
# ==========================================
class FlowModule(Base):
    __tablename__ = "flow_modules"
    
    id = Column(Integer, primary_key=True, index=True)
    flow_id = Column(Integer, ForeignKey("domain_flows.id"))
    
    name = Column(String)                 # 模块名称：如 "番茄钟" / "数据清洗"
    pros = Column(Text)                   # 行业优势
    cons = Column(Text)                   # 行业劣势
    market_status = Column(Text)          # 市场同质化情况（这就是你要在 Hover 时展示的数据！）
    core_knowledge = Column(String)       # 背后对应的基础学科（如：操作系统-中断机制）
    
    flow = relationship("DomainFlow", back_populates="modules")

# ==========================================
# 表 5：CapabilityRecord (能力质询靶场 - The Reality Check)
# ==========================================
class CapabilityRecord(Base):
    __tablename__ = "capability_records"
    
    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer, ForeignKey("ideas.id"))
    module_id = Column(Integer, ForeignKey("flow_modules.id"))
    
    # 核心字段：你的精妙设计就在这三行！
    is_familiar = Column(Boolean, nullable=True)      # 用户自己打的 勾/叉
    quiz_passed = Column(Boolean, nullable=True)      # 弹窗考试的结果：对/错/问号
    wants_innovation = Column(Boolean, default=False) # 用户是否想在这里死磕/创新？