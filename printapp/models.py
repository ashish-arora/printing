from mongoengine import *
from mongoengine.django.auth import User as BaseUser
import time

ADMIN = 1
SUPERUSER = 2
PRINTER = 3
CLIENT = 4

OPEN = 1
RESPONSE_RECEIVED = 2
CLOSED = 3
CANCELLED = 4
RESPONDED = 2

USER_MAP = {"Worker":PRINTER , "Employer": CLIENT}

VALID_REQUEST_STATUS = [OPEN, RESPONSE_RECEIVED, CLOSED, CANCELLED]

VALID_CITIES = [(1, "New Delhi"), (2, "Banglore"), (3, "Gurgaon")]

PRESENT = 1
ABSENT = 0

VALID_TYPES = [ADMIN, SUPERUSER, PRINTER, CLIENT]

USER_TYPES = (ADMIN, SUPERUSER, PRINTER, CLIENT)

VALID_COUNTRY = ['+91']

PRODUCT_DATA = {6: {"size":["Standard", "Slim Card"], "paper":["Standard Card", "Extra Stiff Card", "White Textured",
                                            "Cream Textured", "Non Tearable Card", "Recycled Card", "Metallic Card"],
                    "lamination":["None", "Matt", "Gloss"], "corner":["Straight", "Round"],
                    "type": ["Standard", "Semi Transparent", "Premium Plastic"], "side":["Single Sided", "Double Sided"], "color": ["Single Color", "Four Color"]},
                1: {"size":["A4"], "color": ["Single Color", "Four Color"], "paper": ["Premium White", "Bond", "Textured", "Recycled"],
                    "binding":["Loose Sheets", "Pad Binding"]},
                2: {"size":["105x242mm", "A4", "C5"]}, "color": ["Single Color", "Four Color"], "flap position": ["Short Edge", "Long Edge"],
                "paper":["Premium White", "White Textured", "Recycled", "Extra Thick"],
                3: {"size":["A6", "A4"], "color": ["Black & White", "Single Color", "Four Color"], "side":["Single Sided", "Double Sided"]},
                11: {"size":[(3,2), (4,3), (6,3), (8,3), (8,5), (10,8)]},
                33: {"size": [(89,203)]},
                12: {"size":[(5.5,9,3), (6.5,9,2), (8.5,14.5,3), (9,9,3), (13.5,10,4), (14.5,9,3), (4,14,4)]},
                14: {"size":[(6,9)]},
                15: {"size":[(6,9)]},
                16: {"size":[(5,5,10)]},
                17: {"size":[(11,17)]},
                18: {"size":["A5"]},
                19: {"size":["A5"]},
                20: {"size":["A5"]},
                21: {"size":["A4"], "paper":["Executive", "Textured", "Metallic"]},
                22: {"refill color":["Blue", "Black"]},
                23: {"size":[(195,89)]},
                24: {"size":[(12,16), (14,14)]},
                25: {"size":[(4,6), (5,7), (8,12)]},
                26: {"size":[(12,12), (16,20), (18,18), (20,30)]},
                27: {"size":[(12,12), (16,20), (18,18), (20,30)]},
                28: {"size":["A6"], "paper":["Standard", "Metallic"], "packing":["Plain White", "Transparent Plastic", "Printed White", "Printed Metallic"]},
                29: {"size":[(1.5,1.5), (2,2), (3,3), (3,5)]}
                }

VALID_PRODUCT_TYPES = [(1, "Letterheads"),
    (2, "Envelopes"),
    (3, "Notepads"),
    (4, "Folders"),
    (5, "Paper Files"),
    (6, "Visiting Cards"),
    (7, "Flyers"),
    (8, "Posters"),
    (9, "Brochures"),
    (10, "Booklets"),
    (11, "Banners"),
    (12, "Gift Bags"),
    (13, "Gift Boxes"),
    (14, "Name Calendar"),
    (15, "Desk Calendar"),
    (16, "Tent Card Calendar"),
    (17, "Hanging Calendar"),
    (18, "Wire-o-Diary"),
    (19, "Rubberband style Diary"),
    (20, "HardCover Perfect bound diary"),
    (21, "Certificates"),
    (22, "Printed Pens"),
    (23, "Printed Mugs"),
    (24, "Photo Frame"),
    (25, "Photo Print"),
    (26, "Posters"),
    (27, "Canvas Frames"),
    (28, "Invitation & Greeting Cards"),
    (29, "Stickers"),
    (30, "Magzines"),
    (31, "Books"),
    (32, "Notebooks"),
    (33, 'Gift Vouchers'),
    (34, "Other")]

VALID_ATTENDANCE_TYPES = [PRESENT, ABSENT]
VALID_RESPONSE_STATUS = [OPEN, RESPONDED]

class User(BaseUser):
    msisdn = StringField(max_length=15, unique_with='type')
    devices = DictField(required=False)
    country = StringField(max_length=20, default='India', required=False)
    city = IntField(required=False, choices=VALID_CITIES, default=1)
    address = StringField(required=False)
    pincode = IntField(required=False)
    rating = FloatField(max_value=5.0, min_value=0.0)
    orders_completed = IntField(default=0)
    token = StringField(max_length=20, required=False)
    type= IntField(required=True, choices=USER_TYPES)
    product_category = StringField(max_length=40, required=False, choices=dict(VALID_PRODUCT_TYPES).keys())
    business_name = StringField(max_length=40, required=False)
    description= StringField(required=False)
    images=ListField()
    md = DictField(default={})
    ts = IntField(default=int(time.time()))

    meta = {
        'app_label':'mongo',
        'indexes':['msisdn', 'type']

    }

class UserRequest(Document):
    user = ReferenceField(User)
    status = IntField(required=True, choices=VALID_REQUEST_STATUS)
    type = StringField(default='Printing', required=False)
    description = DictField(required=True)
    hired_user = ReferenceField(User)
    ts = IntField(default=int(time.time()))

class UserResponse(Document):
    user = ReferenceField(User)
    request= ReferenceField(UserRequest)
    status = IntField(required=True, choices=VALID_RESPONSE_STATUS)
    response_data = StringField()
    quote = StringField()
    delivery_hours = FloatField()
    ts = IntField(default=int(time.time()))




