from flask import Blueprint, render_template, request, jsonify
import sys
from urllib.parse import urlparse

from singletons import UserSettings, Students, Sysls
from general import Mainroad, JINJAstuff

from studenten import (
	StudentJinja,
	Student,
	Note,
)
# =============== endpoints =====================
ep_home = Blueprint(
	'ep_home', __name__,
	url_prefix="/home",
	template_folder='templates',
    static_folder='static',
	static_url_path='static',
)

menuitem = 'home'

@ep_home.get('/')
def home():
	jus = UserSettings()

	if not jus._is():
		Mainroad.loglog('Iets mis met login')
		sys.exit(1)

	students_o = Students()
	sysls_o = Sysls()
	mijn = list()
	dijn = list()

	studenten = students_o.get_students_mongo(where={"notes.todo": 1})
	groepen = sysls_o.get_sysl('s_group')
	for s in studenten:
		for i in range(len(s['notes'])):
			Note.normalize(s['notes'][i])
			if s['notes'][i]['to_alias'] == '':
				s['notes'][i]['to_alias'] = s['notes'][i]['alias']

		if len(s['notes']) == 0:
			continue
		if s['notes'][0]['to_alias'] in [jus.alias(), 'all']:
			# door andere aan mij gericht
			mijn.append(StudentJinja(s, Student.get_model()))
		else:
			dijn.append(StudentJinja(s, Student.get_model()))

	for k, v in groepen.items():
		groepen[k] = JINJAstuff(v, {})

	bericht = Mainroad.get_message(newline='<br>')
	if bericht == '':
		bericht = None

	homebuttons = jus.get_home_buttons()

	return render_template(
		'home.html',
		menuitem='home',
		props=jus,
		mijn=mijn,
		dijn=dijn,
		groepen=groepen,
		bericht=bericht,
		logging=Mainroad.logging,
		homebuttons = homebuttons,
	)



@ep_home.post('/store-button')
def home_store_button():
	jus = UserSettings()
	if not jus._is():
		return {'error': 'Its mis met login'}
	d = request.values.to_dict()
	if d["name"].strip() == '':
		return {'error': 'Its met geen naam'}
	d["url"] = urlparse(d["url"]).path
	d["name"] = d["name"].strip()
	jus.set_home_button(d)
	return d

@ep_home.post('/remove-button')
def home_remove_button():
	jus = UserSettings()
	if not jus._is():
		return {'error': 'Its mis met login'}

	d = request.values.to_dict()
	jus.unset_home_button(d['name'])
	return d
