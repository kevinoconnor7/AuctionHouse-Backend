""" Auction Model """

from penelophant.database import db
from .Model import Model
from .User import User

class Auction(Model):
  """ Auction data representation """
  id = db.Column(db.Integer, primary_key=True)
  creator_user_id = db.Column(db.Integer,
    db.ForeignKey(User.id, ondelete='RESTRICT', onupdate='CASCADE')
  )
  start_time = db.Column(db.TIMESTAMP, default=db.func.now())
  end_time = db.Column(db.TIMESTAMP)

  start_price = db.Column(db.Numeric('13,2'), default=0)
  reserve = db.Column(db.Numeric('13,2'), default=0)

  type = db.Column('type', db.String(50))

  creator = db.relationship(User)

  __mapper_args__ = {
    'polymorphic_on': type
  }

  @property
  def reserve_met(self):
    """ Return whether not not the reserve has been met """
    return False


  __api_fields__ = [
    'id',
    'creator',
    'start_time',
    'end_time',
    'reserve_met'
  ]

  def create_bid(self):
    """ Create bid logic """
    pass

  def find_winner(self):
    """ Determine winner logic """
    pass
