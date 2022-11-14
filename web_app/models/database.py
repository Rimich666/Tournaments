from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from ..globals import db
from ..forms import (
    Templ,
)


class Place(db.Model, Templ):
    __tablename__ = 'places'
    __table_args__ = {'info': {'alt_name': 'Места проведения'}}
    id = Column(Integer, primary_key=True)
    place = Column(String, unique=True, nullable=False)


class Tournament(db.Model, Templ):
    __tablename__ = 'tournaments'
    __table_args__ = {'info': {'alt_name': 'Турнир'}}
    id = Column(Integer, primary_key=True)
    tournament = Column(String(100), unique=True, nullable=False)
    start = Column(Date, nullable=False)
    finish = Column(Date, nullable=False)
    state = Column(Integer)
    place_id = Column(Integer, ForeignKey(Place.id))
    place = relationship(Place)
    competitions = relationship('Competition')
    referees = relationship('Referee', secondary='tour_referees')
    teams = relationship('Team', secondary='commands')


class SportType(db.Model, Templ):
    __tablename__ = 'sport_types'
    __table_args__ = {'info': {'alt_name': 'Вид спорта'}}
    id = Column(Integer, primary_key=True)
    type = Column(String(100), unique=True, nullable=False)
    specialities = relationship('Speciality')


class Speciality(db.Model, Templ):
    __tablename__ = 'speciality'
    __table_args__ = {'info': {'alt_name': 'Дисциплина'}}
    id = Column(Integer, primary_key=True)
    spec = Column(String(100), unique=True, nullable=False)
    type_id = Column(Integer, ForeignKey(SportType.id))


class Category(db.Model, Templ):
    __tablename__ = 'category'
    __table_args__ = {'info': {'alt_name': 'Категория'}}
    id = Column(Integer, primary_key=True)
    category = Column(String(100), unique=True, nullable=False)


class Competition(db.Model, Templ):
    __tablename__ = 'competitions'
    __table_args__ = {'info': {'alt_name': 'Соревнование'}}
    id = Column(Integer, primary_key=True)
    comp = Column(String(100), unique=True, nullable=False)
    begin = Column(Date, nullable=False)
    start_gate = Column(Integer, nullable=False)
    finish_gate = Column(Integer, nullable=False)
    tour_id = Column(Integer, ForeignKey(Tournament.id))
    speciality_id = Column(Integer, ForeignKey(Speciality.id))
    category_id = Column(Integer, ForeignKey(Category.id))
    speciality = relationship('Speciality')
    category = relationship('Category')
    gates = relationship('Gate')
    attempts = relationship('Attempt')


class Gate(db.Model, Templ):
    __tablename__ = 'gates'
    __table_args__ = {'info': {'alt_name': 'Промежуточные ворота'}}
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    hard_id = Column(Integer, nullable=False)
    comp_id = Column(Integer, ForeignKey(Competition.id), nullable=False)


class Attempt(db.Model, Templ):
    __tablename__ = 'attempts'
    __table_args__ = {'info': {'alt_name': 'Попытка'}}
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    comp_id = Column(Integer, ForeignKey(Competition.id))
    referees = relationship('Attempt', secondary='attempt_referees')


commands = db.Table('commands',
                    Column('comp_id', ForeignKey('tournaments.id'), primary_key=True),
                    Column('team_id', ForeignKey('teams.id'), primary_key=True),
                    info={'alt_name': 'Команды на турнире'})


class Team(db.Model, Templ):
    __tablename__ = 'teams'
    __table_args__ = {'info': {'alt_name': 'Команды'}}
    id = Column(Integer, primary_key=True)
    team = Column(String(50), nullable=False)
    sportsmen = relationship('Sportsman')


class Command(Templ):
    __tablename__ = 'commands'
    is_association = True
    add_to = 'comp_id'
    ref = 'teams'
    added = 'team_id'

    def __init__(self, comp_id, team_id):
        self.comp_id = comp_id
        self.team_id = team_id
        self.comp = Competition.query.filter_by(id=comp_id).first()
        self.team = Team.query.filter_by(id=team_id).first()

    def add(self):
        self.comp.teams.append(self.team)

    def delete(self):
        self.comp.teams.remove(self.team)

    def __repr__(self):
        return f'<Command comp_id = {self.comp_id}, team_id = {self.team_id}>'


class Person(db.Model, Templ):
    __tablename__ = 'persons'
    __table_args__ = {'info': {'alt_name': 'Люди'}}
    id = Column(Integer, primary_key=True)
    surname = Column(String(30), nullable=False)
    name = Column(String(30), nullable=False)
    patronymic = Column(String(30))
    birthday = Column(Date, nullable=False)
    gender = Column(String(4), nullable=False)
    data = relationship('PersonalData', back_populates='person', uselist=False)


class PersonalData(db.Model, Templ):
    __tablename__ = 'persons_data'
    __table_args__ = {'info': {'alt_name': 'Персональные данные'}}
    id = Column(Integer, primary_key=True)
    pers_id = Column(Integer, ForeignKey(Person.id), nullable=False)
    date = Column(Date, nullable=False)
    person = relationship('Person', back_populates='data')


class Sportsman(db.Model, Templ):
    __tablename__ = 'sportsmen'
    __table_args__ = {'info': {'alt_name': 'Спортсмены'}}
    id = Column(Integer, primary_key=True)
    pers_id = Column(Integer, ForeignKey(Person.id), nullable=False)
    team_id = Column(Integer, ForeignKey(Team.id), nullable=False)
    person = relationship('Person', uselist=False)


class Card(db.Model, Templ):
    __tablename__ = 'cards'
    __table_args__ = {'info': {'alt_name': 'Карточки'}}
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    hard_id = Column(Integer, nullable=False)


tour_referee = \
    db.Table('tour_referees',
             Column('tour_id', ForeignKey('tournaments.id'), primary_key=True),
             Column('refer_id', ForeignKey('referees.id'), primary_key=True),
             info={'alt_name': 'Судьи на турнире'})

attempt_referee = \
    db.Table('attempt_referees',
             Column('attempt_id', ForeignKey('attempts.id'), primary_key=True),
             Column('refer_id', ForeignKey('referees.id'), primary_key=True),
             info={'alt_name': 'Судьи на попытке'})


class Referee(db.Model, Templ):
    __tablename__ = 'referees'
    __table_args__ = {'info': {'alt_name': 'Судьи'}}
    id = Column(Integer, primary_key=True)
    pers_id = Column(Integer, ForeignKey(Person.id), nullable=False)
    person = relationship('Person', uselist=False)


class TourReferee(Templ):
    __tablename__ = 'tour_referees'
    is_association = True
    add_to = 'tour_id'
    ref = 'referees'
    added = 'refer_id'

    def __init__(self, tour_id, refer_id):
        self.tour_id = tour_id
        self.refer_id = refer_id
        self.tour = Tournament.query.filter_by(id=tour_id).first()
        self.refer = Referee.query.filter_by(id=refer_id).first()

    def add(self):
        self.tour.referees.append(self.refer)

    def delete(self):
        self.tour.referees.remove(self.refer)

    def __repr__(self):
        return f'<Command comp_id = {self.tour_id}, team_id = {self.refer_id}>'


class AttemptReferee(Templ):
    __tablename__ = 'attempt_referees'
    is_association = True
    add_to = 'attempt_id'
    ref = 'referees'
    added = 'refer_id'

    def __init__(self, attempt_id, refer_id):
        self.attempt_id = attempt_id
        self.refer_id = refer_id
        self.attempt = Competition.query.filter_by(id=attempt_id).first()
        self.refer = Team.query.filter_by(id=refer_id).first()

    def add(self):
        self.attempt.referees.append(self.refer)

    def delete(self):
        self.attempt.referees.remove(self.refer)

    def __repr__(self):
        return f'<Command comp_id = {self.attempt_id}, team_id = {self.refer_id}>'


class StartProtocol(db.Model, Templ):
    __tablename__ = 'start_protocols'
    __table_args__ = {'info': {'alt_name': 'Строки стартового протокола'}}
    id = Column(Integer, primary_key=True)
    attempt_id = Column(Integer, ForeignKey(Attempt.id), nullable=False)
    sportsman_id = Column(Integer, ForeignKey(Sportsman.id), nullable=False)
    card_id = Column(Integer, ForeignKey(Card.id), nullable=False)
    start_number = Column(Integer, nullable=False)
    attempt = relationship(Attempt)
    sportsman = relationship(Sportsman)
    card = relationship(Card)


class ReferNote(db.Model, Templ):
    __tablename__ = 'refer_notes'
    __table_args__ = {'info': {'alt_name': 'Судейские записки'}}
    id = Column(Integer, primary_key=True)
    attempt_id = Column(Integer, ForeignKey(Attempt.id), nullable=False)
    gate_id = Column(Integer, ForeignKey(Gate.id), nullable=False)
    refer_id = Column(Integer, ForeignKey(Referee.id), nullable=False)
    attempt = relationship(Attempt)
    gate = relationship(Gate)
    refer = relationship(Referee)
