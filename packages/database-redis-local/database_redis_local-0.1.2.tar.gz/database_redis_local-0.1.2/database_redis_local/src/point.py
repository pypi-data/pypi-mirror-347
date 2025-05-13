# TODO copied from database-mysql, do we need it twice? We prefer to have one copy

# from to_sql_interface import ToSQLInterface
from database_infrastructure_local.to_sql_interface import ToSQLInterface

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


# TODO: rename to OurPoint
# TODO We should consier to change is to OurPoint everywere
# Classes which uses Point Class: Location, Organization, ContactGroup
class Point(ToSQLInterface):
    def __init__(self, longitude: float, latitude: float) -> None:
        self.longitude = longitude
        self.latitude = latitude

    # TODO: POINT(%s, %s) with params
    def to_sql(self) -> str:
        return f"POINT ({self.longitude}, {self.latitude})"

    @staticmethod
    def create_select_stmt(column_name: str) -> str:
        return f"ST_X({column_name}), ST_Y({column_name})"

    def __eq__(self, other_point: 'Point') -> bool:
        return (isinstance(other_point, Point) and
                self.longitude == other_point.longitude and
                self.latitude == other_point.latitude)

    def __repr__(self) -> str:
        return f"OurPoint(longitude={self.longitude}, latitude={self.latitude})"


ToSQLInterface.register(Point)
