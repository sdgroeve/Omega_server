import os
import flask
import subprocess
import time          #You don't need this. Just included it so you can see the output stream.

from flask import render_template
from flask import send_file
from ..models import EditableHTML

from flask_login import (current_user, login_required, login_user,
						 logout_user)

from .forms import ParametersForm
from os import listdir
from os.path import isfile, join
					
from . import main

from shelljob import proc

omega_dir = "/home/compomics/Omega/"
omega_server_dir = "/home/compomics/Omega_server/flask-base"
omega_data_dir = "/home/compomics/public/omega_spectrum_files_/"

spec_files = []

@main.route('/', methods=['GET', 'POST'])
def index():
	global spec_files
	form = ParametersForm()
	if form.validate_on_submit():
		mypath = omega_data_dir + form.ms2folder.data
		spec_files = [mypath+"/"+f for f in listdir(mypath) if isfile(join(mypath, f))]
		prec_error = form.prec_error.data
		frag_error = form.frag_error.data
		fixed_ptms = form.fixed_ptms.data
		variable_ptms = form.variable_ptms.data
		with open("/tmp/config.file","w") as f:
			f.write("target=/home/compomics/Omega/dbs/pyrococcus_entrapment_fasta\n")
			f.write("decoy=/home/compomics/Omega/dbs/pyrococcus_entrapment_reversed_fasta\n")
			for ptm in fixed_ptms:
				f.write(ptm.replace(",opt,",",fix,")+"\n")
			for ptm in variable_ptms:
				f.write(ptm+"\n")
		return render_template('main/index2.html')
	return render_template('main/index.html',form=form)

@main.route('/omega')
def omega():
	return render_template('main/index2.html')

@main.route('/download')
def download():
	try:
		return send_file('/home/pitro11a/flask-base/test.test', as_attachment=True) 
	except Exception as e:
		return str(e)

@main.route('/about')
def about():
	editable_html_obj = EditableHTML.get_editable_html('about')
	return render_template('main/about.html',
						   editable_html_obj=editable_html_obj)
 
@main.route( '/stream' )
def stream():
	global spec_files
	g = proc.Group()
	p = g.run("sh ./me.sh %s %s %s"%(spec_files[0],omega_dir,omega_server_dir))
	def read_process():
		while g.is_pending():
			lines = g.readlines()
			time.sleep(1)
			for proc, line in lines:
				yield line

	return flask.Response( read_process(), mimetype= 'text/plain' )
	#return app.response_class(generate(), mimetype='text/plain')
 
 
