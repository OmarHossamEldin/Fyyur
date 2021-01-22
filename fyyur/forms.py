import dateutil.parser
import babel
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SubmitField, BooleanField, TextAreaField, SelectField, DateTimeField
from wtforms.validators import DataRequired, URL, Optional

states=[('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY')
        ]
class ShowForm(Form):
    artist_id = StringField(
        'artist_id',
        validators=[DataRequired()]
    )
    venue_id = StringField(
        'venue_id',
        validators=[DataRequired()]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )
    submit = SubmitField('New Show')

class VenueForm(Form):
    name = StringField(
        'name', 
        validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=states
    )
    address = StringField(
        'address',
        validators=[DataRequired()]
    )
    phone = StringField(
        'phone',
        validators=[DataRequired(),
        ]
    )
    seeking_talent = BooleanField(
        'seeking_talent',
        validators=[DataRequired()]
    )
    website = StringField(
        'website', validators=[Optional(),
        URL()
        ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[Optional(),
        URL()
        ]
    )
    image_link = StringField(
        'image_link',
        validators=[Optional(),
        URL()
        ]
    )
    seeking_description = TextAreaField(
        'seeking_description',
        validators=[Optional()]
    )
    genres = StringField(
        'genres', validators=[DataRequired()
        ],
    ) 
    submit = SubmitField('New Venue') 

class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=states
    )
    phone = StringField(
        'phone',
        validators=[DataRequired()]
    )
    seeking_venue =BooleanField(
        'seeking_venue',
        validators=[Optional()]
    )
    website = StringField(
        'website',
        validators=[Optional(),
        URL()
        ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    image_link = StringField(
        'image_link',
        validators=[Optional(),
        URL()
        ]
    )
    seeking_description = TextAreaField(
        'seeking_description',
        validators=[Optional()]
    )
    genres = StringField(
        'genres', validators=[DataRequired()],
    )
    
    submit = SubmitField('New Artist')

