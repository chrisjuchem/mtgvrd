from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from app.db.models import BaseModel
from app.db.models.base import IdLookupMixin


class Draft(BaseModel, IdLookupMixin):
    __tablename__ = "drafts"

    id = Column(UUID, primary_key=True, server_default=func.uuid_generate_v4())
    name = Column(String)
    created_ts = Column(DateTime, default=func.now())
    start_ts = Column(DateTime)
    format = Column(Enum("VRD", name="format"), nullable=False, server_default="VRD")
    n_seats = Column(Integer, nullable=False)
    pick_order = Column(Enum("snake", name="pick_order"), nullable=False, server_default="snake")
    rounds = Column(Integer, nullable=False)
    picks_made = Column(Integer, nullable=False, server_default="0")
    owner_id = Column(UUID, ForeignKey("users.id"))

    owner = relationship("User")
    seats = relationship("Seat", order_by="Seat.seat_no", back_populates="draft")
    players = association_proxy("seats", "player")

    _pick_dict = relationship(
        "Pick",
        back_populates="draft",
        cascade="delete,delete-orphan",
        # lazy="dynamic",
        collection_class=attribute_mapped_collection("pick_no"),
    )
    _pick_query = relationship(
        "Pick",
        back_populates="draft",
        order_by="Pick.pick_no",
        lazy="dynamic",
        viewonly=True,
    )
    # finalized_picks = relationship(
    #     "Pick",
    #     back_populates="draft",
    #     primaryjoin="and_(Pick.draft_id == Draft.id, Pick.pick_no < Draft.picks_made)",
    #     viewonly=True,
    # )
    # preloads = relationship(
    #     "Pick",
    #     back_populates="draft",
    #     primaryjoin="and_(Pick.draft_id == Draft.id, Pick.pick_no >= Draft.picks_made)",
    #     viewonly=True,
    # )  # TODO filter by seats

    @property
    def max_picks(self):
        return self.rounds * self.n_seats

    @property
    def picks(self):
        return list(self._pick_dict.values())

    def update_pick(self, pick):
        self._pick_dict[pick.pick_no] = pick

    @property
    def finalized_picks(self):
        # return [pick for n, pick in self._pick_dict.items() if n < self.picks_made]
        return self._pick_query.filter(Pick.pick_no < Draft.picks_made)

    @property
    def preloads(self):
        # return [pick for n, pick in self._pick_dict.items() if n >= self.picks_made]
        return self._pick_query.filter(Pick.pick_no >= Draft.picks_made)

    def seat_preloads(self, seat_no=None, seat=None, seat_id=None):
        if seat_no:
            seat = self.seats[seat_no]
        if seat:
            seat_id = seat.id

        # return [
        #     pick for n, pick in self._pick_dict.items()
        #     if n >= self.picks_made and (not seat or pick.seat == seat)
        # ]

        if not seat_id:
            return []
        return self.preloads.filter(Pick.seat_id == seat_id)

    def seat_for_pick_no(self, pick):
        rnd = pick // self.n_seats
        offset = pick % self.n_seats
        if self.pick_order == "snake" and rnd % 2 == 1:
            offset = self.n_seats - offset - 1
        return self.seats[offset]

    def finalize_picks(self):
        already_picked = set(pick.card_id for pick in self.finalized_picks)
        while True:
            next_ = self._pick_dict.get(self.picks_made)
            if not next_:
                return  # no preload yet
            if next_.card_id in already_picked:
                return  # preload got sniped, could be fun to track this if you can't preload already picked cards

            self.picks_made += 1
            next_.finalized_ts = func.now()
            already_picked.add(next_.card_id)


class Seat(BaseModel, IdLookupMixin):
    __tablename__ = "seats"

    id = Column(UUID, primary_key=True, server_default=func.uuid_generate_v4())
    draft_id = Column(UUID, ForeignKey("drafts.id", ondelete="cascade"), nullable=False)
    seat_no = Column(Integer, nullable=False)
    player_id = Column(UUID, ForeignKey("users.id"))
    joined_ts = Column(DateTime, default=func.now())
    # basics

    draft = relationship("Draft", back_populates="seats")
    picks = relationship("Pick", back_populates="seat")
    player = relationship("User")
    # preloads

    __table_args__ = (UniqueConstraint(draft_id, seat_no),)


class Pick(BaseModel):
    __tablename__ = "picks"

    draft_id = Column(UUID, ForeignKey("drafts.id", ondelete="cascade"), nullable=False)
    seat_id = Column(UUID, ForeignKey("seats.id", ondelete="cascade"), nullable=False)
    pick_no = Column(Integer, nullable=False)
    round = Column(Integer, nullable=False)  # todo calc default?
    card_id = Column(UUID, ForeignKey("cards.oracle_id"), nullable=False)
    pick_ts = Column(DateTime, default=func.now())
    finalized_ts = Column(DateTime)
    maindeck = Column(Boolean)

    draft = relationship(
        "Draft"
    )  # , back_populates="picks") TODO: is this possible to split up and do we need it
    seat = relationship("Seat", back_populates="picks")
    card = relationship("Card")

    __table_args__ = (
        PrimaryKeyConstraint(draft_id, pick_no),
        Index("seat_idx", seat_id),
    )
