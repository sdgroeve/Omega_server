from flask import url_for
from flask_wtf import Form
from wtforms import ValidationError
from wtforms.fields import (BooleanField, PasswordField, StringField, SelectMultipleField,
							SubmitField)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, EqualTo, InputRequired, Length

from .. import db
from ..models import User, FragMethod

class ParametersForm(Form):
	frag_method = QuerySelectField(
		'Fragmentation method',
		validators=[InputRequired()],
		get_label='name',
		#query_factory=["option 1","option 2"])
		query_factory=lambda: db.session.query(FragMethod))
		
	unimod_ptms = []
	with open("unimodptms.txt") as f:
		for row in f:
			l = row.rstrip().split("=")[1].split(",")
			tmp = "%s %s (%s)" % (l[0],l[3],l[1])
			unimod_ptms.append((row.rstrip(),tmp))	

	ms2folder = StringField("MS2 spectrum file folder name",validators=[InputRequired()])
	prec_error = StringField("Precursor error tol. (ppm)",validators=[InputRequired()])
	frag_error = StringField("Fragmentation error tol. (Da)",validators=[InputRequired()])
	fixed_ptms = SelectMultipleField("Fixed PTMs",choices=unimod_ptms)
	variable_ptms = SelectMultipleField("Variable PTMs",choices=unimod_ptms)
	open_search = BooleanField("Enable extended PTM search")
	submit = SubmitField('Run')
 
