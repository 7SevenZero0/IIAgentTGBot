import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

load_dotenv()

db = create_async_engine(url=os.getenv('DATABASE_URL'))
async_session = async_sessionmaker(db)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class AudioRecording(Base):
    __tablename__ = 'audio_recordings'
    
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    record_path = Column(String, nullable=False)
    date_time = Column(DateTime, nullable=False)
    user_id = Column(Integer, nullable=False) 
    meeting_id = Column(Integer, ForeignKey('meetings.meeting_id'))

    meeting = relationship('Meeting', back_populates='audio_recordings')
    transcriptions = relationship('Transcription', back_populates='audio_recording')

class Transcription(Base):
    __tablename__ = 'transcriptions'
    
    transcription_id = Column(Integer, primary_key=True, autoincrement=True)
    id_record = Column(Integer, ForeignKey('audio_recordings.record_id'), nullable=False)
    transcription_text = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)

    audio_recording = relationship('AudioRecording', back_populates='transcriptions')
    tasks = relationship('Task', back_populates='transcription')

class Meeting(Base):
    __tablename__ = 'meetings'

    meeting_id = Column(Integer, primary_key=True, autoincrement=True)
    meeting_title = Column(String, nullable=False)
    meeting_date = Column(Date, nullable=False)
    meeting_desc = Column(Text, nullable=True)

    audio_recordings = relationship('AudioRecording', back_populates='meeting')
    meeting_participants = relationship('MeetingParticipant', back_populates='meeting')
    meeting_protocols = relationship('MeetingProtocol', back_populates='meeting')

class Participant(Base):
    __tablename__ = 'participants'

    participant_id = Column(Integer, primary_key=True, autoincrement=True)
    participant_name = Column(String, nullable=False)
    participant_email = Column(String, nullable=False)
    participant_phone = Column(String, nullable=True)

    meeting_participants = relationship('MeetingParticipant', back_populates='participant')
    tasks = relationship('Task', back_populates='participant')

class MeetingParticipant(Base):
    __tablename__ = 'meeting_participants'

    meeting_participant_id = Column(Integer, primary_key=True, autoincrement=True)
    id_meeting = Column(Integer, ForeignKey('meetings.meeting_id'), nullable=False)
    id_participant = Column(Integer, ForeignKey('participants.participant_id'), nullable=False)

    meeting = relationship('Meeting', back_populates='meeting_participants')
    participant = relationship('Participant', back_populates='meeting_participants')

class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    id_transcription = Column(Integer, ForeignKey('transcriptions.transcription_id'), nullable=False)
    id_participant = Column(Integer, ForeignKey('participants.participant_id'), nullable=False)
    task_desc = Column(Text, nullable=False)
    task_status = Column(String, nullable=False)
    task_deadline = Column(Date, nullable=False)

    transcription = relationship('Transcription', back_populates='tasks')
    participant = relationship('Participant', back_populates='tasks')

class MeetingProtocol(Base):
    __tablename__ = 'meeting_protocols'

    protocol_id = Column(Integer, primary_key=True, autoincrement=True)
    id_meeting = Column(Integer, ForeignKey('meetings.meeting_id'), nullable=False)
    protocol_text = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    file_path = Column(String, nullable=True)

    meeting = relationship('Meeting', back_populates='meeting_protocols')

async def async_main():
    try:
        async with db.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
        print("База данных успешно настроена")
    except Exception as e:
        print(f"Ошибка при подключении или настройке базы данных: {e}")
