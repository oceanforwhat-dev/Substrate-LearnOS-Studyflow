from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base


class IdeaStatus(str, enum.Enum):
    CAPTURED = "captured"     
    ANALYZING = "analyzing"   
    ASSESSED = "assessed"     
    STUDYING = "studying"     
    SHELVED = "shelved"       


class Domain(Base):
    __tablename__ = "domains"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) 
    description = Column(String)


class Idea(Base):
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)                       
    status = Column(Enum(IdeaStatus), default=IdeaStatus.CAPTURED) 
    created_at = Column(DateTime, default=datetime.now)
    
    
    domain_id = Column(Integer, ForeignKey("domains.id"), nullable=True)
    selected_flow_id = Column(Integer, ForeignKey("domain_flows.id"), nullable=True)


class DomainFlow(Base):
    __tablename__ = "domain_flows"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String) 
    

    domain_id = Column(Integer, ForeignKey("domains.id"))
    modules = relationship("FlowModule", back_populates="flow")


class FlowModule(Base):
    __tablename__ = "flow_modules"
    
    id = Column(Integer, primary_key=True, index=True)
    flow_id = Column(Integer, ForeignKey("domain_flows.id"))
    
    name = Column(String)                
    pros = Column(Text)                  
    cons = Column(Text)                  
    market_status = Column(Text)          
    core_knowledge = Column(String)      
    
    flow = relationship("DomainFlow", back_populates="modules")


class CapabilityRecord(Base):
    __tablename__ = "capability_records"
    
    id = Column(Integer, primary_key=True, index=True)
    idea_id = Column(Integer, ForeignKey("ideas.id"))
    module_id = Column(Integer, ForeignKey("flow_modules.id"))
    
   
    is_familiar = Column(Boolean, nullable=True)      
    quiz_passed = Column(Boolean, nullable=True)      
    wants_innovation = Column(Boolean, default=False) 