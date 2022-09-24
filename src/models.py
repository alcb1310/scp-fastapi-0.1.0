from sqlalchemy import Column, String, Integer, TIMESTAMP, CHAR, Boolean, ForeignKey, Float, Date
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from src.database import Base

class Company(Base):
    __tablename__ = "companies"

    uuid = Column(CHAR(36), primary_key=True, nullable=False)
    ruc = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False, unique=True)
    employees = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class User(Base):
    __tablename__ = "users"

    uuid = Column(CHAR(36), primary_key=True, nullable=False)
    company_id = Column(CHAR(36), ForeignKey("companies.uuid", ondelete="RESTRICT"), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    company = relationship("Company")


class Project(Base):
    __tablename__ = "projects"

    uuid = Column(CHAR(36), primary_key=True, nullable=False)
    company_id = Column(CHAR(36), ForeignKey("companies.uuid", ondelete="RESTRICT"), nullable=False)
    user_id = Column(CHAR(36), ForeignKey("users.uuid", ondelete="RESTRICT"), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    company = relationship("Company")
    user = relationship("User")


class Supplier(Base):
    __tablename__ = "suppliers"

    uuid = Column(CHAR(36), primary_key=True, nullable=False)
    company_id = Column(CHAR(36), ForeignKey("companies.uuid", ondelete="RESTRICT"), nullable=False)
    user_id = Column(CHAR(36), ForeignKey("users.uuid", ondelete="RESTRICT"), nullable=False)
    supplier_id = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    contact_name = Column(String(255))
    contact_phone = Column(String(255))
    contact_email = Column(String(255))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    company = relationship("Company")
    user = relationship("User")


class BudgetItems(Base):
    __tablename__ = "budget_items"

    uuid = Column(CHAR(36), primary_key=True, nullable=False)
    company_id = Column(CHAR(36), ForeignKey("companies.uuid", ondelete="RESTRICT"), nullable=False)
    user_id = Column(CHAR(36), ForeignKey("users.uuid", ondelete="RESTRICT"), nullable=False)
    code = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    accumulates = Column(Boolean, nullable=False)
    level = Column(Integer, nullable=False)
    parent_id = Column(CHAR(36), ForeignKey("budget_items.uuid", ondelete="RESTRICT"))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    company = relationship("Company")
    user = relationship("User")
    parent = relationship("BudgetItems")


class ProjectBudget(Base):
    __tablename__ = "project_budget"

    uuid = Column(CHAR(36), primary_key=True, nullable=False)
    company_id = Column(CHAR(36), ForeignKey("companies.uuid", ondelete="RESTRICT"), nullable=False)
    user_id = Column(CHAR(36), ForeignKey("users.uuid", ondelete="RESTRICT"), nullable=False)
    budget_item_id = Column(CHAR(36), ForeignKey("budget_items.uuid", ondelete="RESTRICT"), nullable=False)
    project_id = Column(CHAR(36), ForeignKey("projects.uuid", ondelete="RESTRICT"), nullable=False)
    initial_quantity = Column(Float())
    initial_cost = Column(Float())
    initial_total = Column(Float(), nullable=False)
    spent_quantity = Column(Float())
    spent_total = Column(Float(), nullable=False)
    to_spend_quantity = Column(Float())
    to_spend_cost = Column(Float())
    to_spend_total = Column(Float(), nullable=False)
    updated_budget = Column(Float(), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    company = relationship("Company")
    user = relationship("User")
    budget_item = relationship("BudgetItems")
    project = relationship("Project")


class Invoice(Base):
    __tablename__ = "invoices"

    uuid = Column(CHAR(36), primary_key=True, nullable=False)
    company_id = Column(CHAR(36), ForeignKey("companies.uuid", ondelete="RESTRICT"), nullable=False)
    user_id = Column(CHAR(36), ForeignKey("users.uuid", ondelete="RESTRICT"), nullable=False)
    project_id = Column(CHAR(36), ForeignKey("projects.uuid", ondelete="RESTRICT"), nullable=False)
    supplier_id = Column(CHAR(36), ForeignKey("suppliers.uuid", ondelete="RESTRICT"), nullable=False)
    invoice_number = Column(String(255), nullable=False)
    invoice_date = Column(Date, nullable=False)
    invoice_total = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    company = relationship("Company")
    user = relationship("User")
    project = relationship("Project")
    supplier = relationship("Supplier")


class InvoiceDetails(Base):
    __tablename__ = "invoice_details"

    uuid = Column(CHAR(36), primary_key=True, nullable=False)
    company_id = Column(CHAR(36), ForeignKey("companies.uuid", ondelete="RESTRICT"), nullable=False)
    user_id = Column(CHAR(36), ForeignKey("users.uuid", ondelete="RESTRICT"), nullable=False)
    invoice_id = Column(CHAR(36), ForeignKey("invoices.uuid", ondelete="RESTRICT"), nullable=False)
    budget_item_id = Column(CHAR(36), ForeignKey("budget_items.uuid", ondelete="RESTRICT"), nullable=False)
    quantity = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    company = relationship("Company")
    user = relationship("User")
    invoice = relationship("Invoice")
    budget_item = relationship("BudgetItems")
