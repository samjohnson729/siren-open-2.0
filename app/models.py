from sqlalchemy import Integer, String, Float, ForeignKey, Column, Identity
from sqlalchemy.orm import mapped_column, relationship
import numpy as np

from app import db


class Golfer(db.Model):
    __tablename__ = 'golfer'  # Explicitly set the table name

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255), nullable=False)

    rounds = relationship("Round", backref="golfer")  # Relationship to Round

    def __repr__(self):
        return f"<Golfer id={self.id}, name='{self.name}'>"


class Course(db.Model):
    __tablename__ = 'course'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255), nullable=False)

    layouts = relationship("Layout", backref="course")

    def __repr__(self):
        return f"<Course id={self.id}, name='{self.name}'>"


class Layout(db.Model):
    __tablename__ = 'layout'

    id = mapped_column(Integer, primary_key=True)
    course_id = mapped_column(Integer, ForeignKey('course.id'), nullable=False)  # Changed to course.id
    year = mapped_column(Integer)

    #holes = relationship("Hole", backref="layout")
    holes = relationship("Hole", secondary="layout_holes")
    rounds = relationship("Round", backref="layout")

    def __repr__(self):
        return f"<Layout id={self.id}, year={self.year}>"


class Hole(db.Model):
    __tablename__ = 'hole'
    id = mapped_column(Integer, primary_key=True)
    #layout_id = mapped_column(Integer, ForeignKey('layout.id'), nullable=False)
    number = mapped_column(Integer, nullable=False) # Hole number on the course
    par = mapped_column(Integer, nullable=False) # Hole number on the course
    distance = mapped_column(Integer) # Hole number on the course

    layouts = relationship("Layout", secondary="layout_holes", viewonly=True)
    scores = relationship("HoleScore", backref="hole")

    def __repr__(self):
        return f"<Hole id={self.id}, number={self.number}>"

    def _get_mean(self):
        return np.mean([hs.score for hs in self.scores if hs.is_completed()])
    
    def _get_variance(self):
        return np.var([hs.score for hs in self.scores if hs.is_completed()], ddof=1)


class LayoutHoles(db.Model):
    __tablename__ = 'layout_holes'
    __table_args__ = (
        db.PrimaryKeyConstraint('hole_id', 'layout_id'),
    )

    hole_id = mapped_column(Integer, ForeignKey('hole.id'), nullable=False)
    layout_id = mapped_column(Integer, ForeignKey('layout.id'), nullable=False)

    def __repr__(self):
        return f"<LayoutHole hole_id={self.hole_id}, layout_id={self.layout_id}>"


class Round(db.Model):
    __tablename__ = 'round'
    id = mapped_column(Integer, primary_key=True)
    tournament_id = mapped_column(Integer, ForeignKey('tournament.id'), nullable=False)
    golfer_id = mapped_column(Integer, ForeignKey('golfer.id'), nullable=False)
    layout_id = mapped_column(Integer, ForeignKey('layout.id'), nullable=False)

    scores = relationship("HoleScore", backref="round")

    def __repr__(self):
        return f"<Round id={self.id}, tournament={self.tournament_id}, golfer={self.golfer_id}, layout={self.layout_id}>"
    
    def is_completed(self):
        return all([s.score for s in self.scores])
    
    def get_statistic(self, statistic:str):
        if not self.is_completed():
            return
        
        match statistic:
            case 'score':
                return self._get_score()
            case 'score-to-par':
                return self._get_score_to_par()
            case 'strokes-gained':
                return self._get_strokes_gained()
            case 'z-score':
                return self._get_z_score()

    def _get_score(self):
        return sum([s.score for s in self.scores])
    
    def _get_score_to_par(self):
        return sum([s.score - s.hole.par for s in self.scores])
        
    def _get_strokes_gained(self):
        return sum([h._get_mean() for h in self.layout.holes]) - self._get_score()
    
    def _get_z_score(self):
        mu = sum([h._get_mean() for h in self.layout.holes])
        sigma = np.sqrt(sum([h._get_variance() for h in self.layout.holes]))
        return (mu - self._get_score()) / sigma


class Tournament(db.Model):
    __tablename__ = 'tournament'
    id = mapped_column(Integer, primary_key=True)
    year = mapped_column(Integer, nullable=False)

    rounds = relationship("Round", backref="tournament")


    def __repr__(self):
        return f"<Tournament id={self.id}, year='{self.year}'>"


class HoleScore(db.Model):
    __tablename__ = 'hole_score'
    __table_args__ = (
        db.PrimaryKeyConstraint('round_id', 'hole_id'),
    )
    round_id = mapped_column(Integer, ForeignKey('round.id'), primary_key=True)
    hole_id = mapped_column(Integer, ForeignKey('hole.id'), primary_key=True)
    score = mapped_column(Integer)

    def __repr__(self):
        return f"<HoleScore golfer={self.round.golfer.name}, course={self.round.layout.course.name}, score={self.score}>"
    
    def is_completed(self):
        return self.score is not None

    def get_statistic(self, statistic:str):
        
        if not self.is_completed():
            return

        match statistic:
            case 'score':
                return self._get_score()
            case 'score-to-par':
                return self._get_score_to_par()
            case 'strokes-gained':
                return self._get_strokes_gained()
            case 'z-score':
                return self._get_z_score()

    def _get_score(self):
        return self.score
    
    def _get_score_to_par(self):
        return self.score - self.hole.par
        
    def _get_strokes_gained(self):
        past_scores = [hs.get_statistic('score') for hs in self.hole.scores]
        return np.mean([x for x in past_scores if x is not None]) - self._get_score()
    
    def _get_z_score(self):
        past_scores = [hs.get_statistic('score') for hs in self.hole.scores]
        mu = np.mean([x for x in past_scores if x is not None])
        sigma = np.std([x for x in past_scores if x is not None])
        return (mu - self._get_score()) / sigma
