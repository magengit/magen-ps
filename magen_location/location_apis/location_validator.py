#! /usr/bin/python3
"""
Contains class for easy access to location constrains of PI by MAC address LCTX's got
Contains interface for operating with location constrains for concrete Policy Session
Object is pointing to Client instance by mc_id and has MAC address as an hash key
When MAC address got changed - it has to be updated in the object as well = re-hash
"""

__copyright__ = "Copyright(c) 2015, Cisco Systems, Inc."
__version__ = "0.1"
__status__ = "alpha"


def boolean(function):
    def wrapper(*args):
        if len(args) > 1:
            if type(args[1] == bool):
                return function(*args)
            else:
                raise TypeError("Boolean is expected")
        else:
            raise SyntaxError("parameter must be provided")
    return wrapper


class LctxLocation(object):

    def __init__(self, map_hierarchy, coordinate, geocoordinate, boundary, zone_id, **kwargs):
        self._map_hierarchy = map_hierarchy
        self._coordinate = coordinate
        self._geocoordinate = geocoordinate
        self._boundary = boundary
        self._zone_id = zone_id

    def __str__(self):
        return "{Lctx map: %s, coord: %s, geocoord: %s zone: %s, bound: %s}" % (self._map_hierarchy, self._coordinate, self._geocoordinate, self._zone_id, self._boundary)

    @property
    def map_hierarchy(self):
        return self._map_hierarchy

    @map_hierarchy.setter
    def map_hierarchy(self, value):
        self._map_hierarchy = value

    @property
    def coordinate(self):
        return self._coordinate

    @coordinate.setter
    def coordinate(self, coord):
        self._coordinate = coord

    @property
    def geocoordinate(self):
        return self._geocoordinate

    @geocoordinate.setter
    def geocoordinate(self, geocoord):
        self._geocoordinate = geocoord

    # "INSIDE", "OUTSIDE" or ""
    @property
    def boundary(self):
        return self._boundary

    @boundary.setter
    def boundary(self, boundary_string):
        self._boundary = boundary_string

    @property
    def zone_id(self):
        return self._zone_id

    @zone_id.setter
    def zone_id(self, zone_id):
        self._zone_id = zone_id

    def get_details(self):
        return_dict = dict(
            map_hierarchy=self.map_hierarchy,
            coordinate=self.coordinate,
            geocoordinate=self.geocoordinate,
            boundary=self.boundary,
            zone_id=self.zone_id
        )
        return return_dict


# TODO: deal with other location constraints than Zones - coordinates, geocoordinates, geo-fences,...
class LocationValidator(object):

    def __init__(self, mac_address, mc_id, policy_instance_uuid, location, coordinate, geocoordinate, zone_id=None, **kwargs):
        if coordinate:
            assert isinstance(coordinate, dict), "coordinate must be a dict"
        if geocoordinate:
            assert isinstance(geocoordinate, dict), "geocoordinate must be a dict"

        self._mc_id = mc_id
        self._pi_uuid = policy_instance_uuid  # LocationValidator object will be initialized with
        # uuid from Client Collection
        self._mac_address = mac_address
        # self._zone_location = dict(location_name=location, zone_id=zone)
        # FIXME: boundary constraint is always "INSIDE" for now
        # We should pass it in as an argument to allow both checking "INSIDE" or "OUTSIDE" a location constraint
        boundary = "INSIDE"

        self._location_constraint = LctxLocation(map_hierarchy=location, coordinate=coordinate, geocoordinate=geocoordinate, zone_id=zone_id, boundary=boundary)
        self._lctx_location = LctxLocation(map_hierarchy="", coordinate={}, geocoordinate={}, zone_id=0, boundary="")
        self._location_valid = False
        self._location_distance = -1 # <0 is unknown, otherwise known

    def __str__(self):
        return "{MAC: %s, Client: %s, PI_UUID: %s, rule: %s loc: %s valid?: %s distance: %s}" % \
            (self._mac_address, self._mc_id, self._pi_uuid, str(self._location_constraint), str(self._lctx_location), str(self._location_valid), str(self._location_distance))

    @property
    def client_mc_id(self):
        return self._mc_id

    @client_mc_id.setter
    def client_mc_id(self, mc_id):
        self._mc_id = mc_id

    @property
    def policy_instance(self):
        return self._pi_uuid

    @policy_instance.setter
    def policy_instance(self, pi_uuid):
        self._pi_uuid = pi_uuid

    @property
    def mac_address(self):
        return self._mac_address

    @mac_address.setter
    def mac_address(self, mac_add):
        self._mac_address = mac_add

    @property
    def lctx_location(self):
        return self._lctx_location

    @lctx_location.setter
    def lctx_location(self, lctx_loc):
        self._lctx_location = lctx_loc

    @property
    def location_constraint(self):
        return self._location_constraint

    @property
    def location_valid(self):
        return self._location_valid

    @location_valid.setter
    def location_valid(self, isValid):
        self._location_valid = isValid

    @property
    def location_distance(self):
        return self._location_distance

    @location_distance.setter
    def location_distance(self, distance):
        self._location_distance = distance

    @location_constraint.setter
    def location_constraint(self, lctx_location):
        self._location_constraint = lctx_location

    def get_details(self):
        return_dict = dict(
            mac=self.mac_address,
            client=self.client_mc_id,
            pi_uuid=self.policy_instance,
            location=str(self.location_constraint),
            lctx_location=str(self.lctx_location),
            location_valid=self.location_valid,
            location_distance=self.location_distance
        )
        return return_dict
