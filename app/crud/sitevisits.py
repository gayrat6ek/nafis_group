from pickletools import read_unicodestringnl

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast,String
from uuid import UUID
from app.models.sitevisits import SiteVisits
from app.utils.utils import timezonetash
from datetime import date


def today_visited(db:Session, ipaddress):
    current_date = date.today()

    visits = (
        db.query(SiteVisits)
        .filter(
            func.date(SiteVisits.created_at) == current_date,
            SiteVisits.ipaddress == ipaddress,
        )
        .first()
    )
    return visits


def create_ip_address(db:Session,ip_address):
    data = SiteVisits(ipaddress = ip_address)
    db.add(data)
    db.commit()


def add_today_visit(db:Session,ip_address):
    # today_visits = today_visited(db=db,ipaddress=ip_address)
    if not today_visited(db=db,ipaddress=ip_address):
        create_ip_address(db=db,ip_address=ip_address)
    return True



def stats_visits(db: Session, from_date: date, to_date: date):
    """
    Returns daily visit counts between from_date and to_date.
    """
    stats = (
        db.query(
            func.date(SiteVisits.created_at).label("day"),
            func.count(SiteVisits.id).label("visits")
        )
        .filter(func.date(SiteVisits.created_at) >= from_date)
        .filter(func.date(SiteVisits.created_at) <= to_date)
        .group_by(func.date(SiteVisits.created_at))
        .order_by(func.date(SiteVisits.created_at))
        .all()
    )

    return stats