"""
Database Models and Setup
"""
from sqlalchemy import create_engine, Column, String, DateTime, JSON, Float, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()


class ReferralDB(Base):
    """Referral database model"""
    __tablename__ = 'referrals'
    
    referral_id = Column(String, primary_key=True)
    patient_id = Column(String, nullable=False, index=True)
    referring_provider_id = Column(String, nullable=False)
    specialty_requested = Column(String, nullable=False)
    status = Column(String, nullable=False, index=True)
    priority = Column(String, nullable=False)
    diagnosis_codes = Column(JSON)  # List of diagnosis codes
    clinical_summary = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    specialist_provider_id = Column(String, nullable=True)
    appointment_id = Column(String, nullable=True)
    estimated_wait_time = Column(Integer, nullable=True)
    additional_data = Column(JSON)  # For flexible data storage


class PatientDB(Base):
    """Patient database model"""
    __tablename__ = 'patients'
    
    patient_id = Column(String, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(String, nullable=False)
    phone = Column(String)
    email = Column(String)
    address = Column(String)
    insurance_id = Column(String)
    insurance_provider = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    additional_data = Column(JSON)


class ProviderDB(Base):
    """Provider database model"""
    __tablename__ = 'providers'
    
    provider_id = Column(String, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    specialty = Column(String, nullable=False, index=True)
    npi = Column(String, unique=True, nullable=False)
    phone = Column(String)
    email = Column(String)
    address = Column(String)
    accepts_insurance = Column(JSON)  # List of insurance providers
    availability_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)


class DocumentDB(Base):
    """Document database model"""
    __tablename__ = 'documents'
    
    document_id = Column(String, primary_key=True)
    referral_id = Column(String, index=True)
    document_type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.now)
    extracted_data = Column(JSON)
    analysis_completed = Column(Integer, default=0)  # Boolean as int


class AppointmentDB(Base):
    """Appointment database model"""
    __tablename__ = 'appointments'
    
    appointment_id = Column(String, primary_key=True)
    referral_id = Column(String, index=True)
    patient_id = Column(String, index=True)
    provider_id = Column(String, index=True)
    scheduled_time = Column(DateTime, nullable=False)
    location = Column(String)
    status = Column(String, nullable=False)
    confirmation_sent = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    additional_data = Column(JSON)


class AuditLogDB(Base):
    """Audit log database model"""
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now, index=True)
    user_id = Column(String)
    action = Column(String, nullable=False)
    resource_type = Column(String)
    resource_id = Column(String)
    details = Column(JSON)
    ip_address = Column(String)


class DatabaseManager:
    """Database manager for handling connections and sessions"""
    
    def __init__(self, db_path: str = "data/referrals.db"):
        """Initialize database manager"""
        # Ensure data directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Create engine
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        
        # Create all tables
        Base.metadata.create_all(self.engine)
        
        # Create session maker
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def get_session(self):
        """Get a new database session"""
        return self.SessionLocal()
    
    def init_sample_data(self):
        """Initialize sample data for testing"""
        session = self.get_session()
        
        try:
            # Add sample providers
            providers = [
                ProviderDB(
                    provider_id="PROV001",
                    first_name="Sarah",
                    last_name="Johnson",
                    specialty="Cardiology",
                    npi="1234567890",
                    phone="555-0101",
                    email="sjohnson@hospital.com",
                    address="123 Medical Center Dr, City, ST 12345",
                    accepts_insurance=["Blue Cross", "Aetna", "UnitedHealth"]
                ),
                ProviderDB(
                    provider_id="PROV002",
                    first_name="Michael",
                    last_name="Chen",
                    specialty="Orthopedics",
                    npi="1234567891",
                    phone="555-0102",
                    email="mchen@hospital.com",
                    address="456 Specialty Clinic Blvd, City, ST 12345",
                    accepts_insurance=["Blue Cross", "Cigna", "Medicare"]
                ),
                ProviderDB(
                    provider_id="PROV003",
                    first_name="Emily",
                    last_name="Rodriguez",
                    specialty="Neurology",
                    npi="1234567892",
                    phone="555-0103",
                    email="erodriguez@hospital.com",
                    address="789 Brain Institute Ave, City, ST 12345",
                    accepts_insurance=["Aetna", "UnitedHealth", "Medicaid"]
                )
            ]
            
            for provider in providers:
                existing = session.query(ProviderDB).filter_by(provider_id=provider.provider_id).first()
                if not existing:
                    session.add(provider)
            
            session.commit()
            print("Sample data initialized successfully")
            
        except Exception as e:
            session.rollback()
            print(f"Error initializing sample data: {e}")
        finally:
            session.close()
