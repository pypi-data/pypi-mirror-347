from flask import redirect, request, Blueprint, render_template

from general import Casting, IOstuff, ListDicts, JINJAstuff, Mainroad
from singletons import UserSettings, Sysls, Students, Views
from studenten import fix_student_dir

def jinja_object(ding):
	sysls_o = Sysls()
	return JINJAstuff(ding, sysls_o.get_model())

# =============== endpoints =====================
ep_beheer = Blueprint(
	'ep_beheer', __name__,
	url_prefix="/beheer",
	template_folder='templates',
    static_folder='static',
	static_url_path='static',
)

menuitem = 'manage'

@ep_beheer.get('/generate/<path:welk>')
def generate(welk: str):
	# generate all student folders (if not exist)
	# generate all html files (overwrite)
	students_o = Students()
	if welk == "all":
		all = students_o.get_students_mongo()
	else:
		all = students_o.get_students_mongo(where={'s_status': {'$in': Students.active_set()}})

	print(f'Doing it [0]    ', end='', flush=True)
	i = 0
	views = Views(slim=False)
	for student in all:
		fix_student_dir(student, views)
		i += 1
		print(f'\rDoing it [{i}]   ', end='', flush=True)
		# Timetools.sleep(0.25)
	print()

	# uploadsummative_post()
	Mainroad.loglog(f'\nGENERATED: {i}\n')
	print('------- klaar --------')
	return redirect('/home')

@ep_beheer.get('/<path:sysl>/<int:id>')
@ep_beheer.get('/<path:sysl>')
@ep_beheer.get('/')
def kiezen(sysl='s_group', id=0):
	jus = UserSettings()
	if not jus.magda(['beheer']):
		return redirect('/home')

	# beheer lijsten
	sysls_o = Sysls()
	sysls_o.init_mongo()
	lijsten = sysls_o.get_lijsten_nicename()
	if sysl != '':
		allitems = sysls_o.get_sysl_as_list(sysl)
		allitems = ListDicts.sortlistofdicts(allitems, 'ordering')
		for i in range(len(allitems)):
			allitems[i] = jinja_object(allitems[i])
	else:
		allitems = dict() # alle items van deze sysl
	fields = sysls_o.get_fields()

	# selected sysl
	thysl = sysls_o.get_sysl_item(sysl, id)
	if not thysl is None:
		thysl = jinja_object(thysl)
	else:
		thysl = jinja_object(sysls_o.get_empty())

	return render_template(
		'beheer.html',
		menuitem=menuitem,
		props=jus,
		lijsten=lijsten,
		syslname=sysl,
		fields=fields,
		allitems=allitems,
		id=id,
		thysl=thysl,
	)

@ep_beheer.post('/<path:sysl>')
@ep_beheer.post('/<path:sysl>/<int:id>')
def ep_beheer_post(sysl, id=0):
	sysl = sysl.strip()
	if sysl == '':
		return redirect(f'/beheer')

	required = ['id', 'name', 'color', 'extra', 'status', 'action', 'ordering']
	if not IOstuff.check_required_keys(request.form, required):
		return redirect(f'/beheer/{sysl}')
	required.remove('action')
	d = IOstuff.crunch_singles(request.form, required)
	d['id'] = Casting.int_(d['id'], default=0)
	d['status'] = Casting.int_(d['status'], default=0)
	d['ordering'] = Casting.int_(d['ordering'], default=0)
	# if d['id'] == 0:
	#	return redirect(f'/beheer/{sysl}')

	sysls_o = Sysls()
	current = sysls_o.get_sysl_item(sysl, d['id'])
	if not current is None:
		if d['id'] != current['id']:
			# hier gaat iets mis
			return redirect(f'/beheer/{sysl}')

	if current is None and request.form.get('action') == 'Save':
		# new
		new = sysls_o.get_empty()
		for key in d:
			new[key] = d[key]
		sysls_o.set_sysl_item(sysl, new['id'], new)

	elif request.form.get('action') == 'Delete':
		sysls_o.del_sysl_item(sysl, d['id'])

	elif request.form.get('action') == 'Save':
		# update
		if sysl == 's_group':
			if not 'notes' in current:
				d['notes'] = list()
			else:
				d['notes'] = current['notes']
		sysls_o.set_sysl_item(sysl, d['id'], d)

	else:
		return redirect(f'/system')

	return redirect(f'/beheer/{sysl}/{d["id"]}')

@ep_beheer.post('/ordering/<path:sysl>')
def post_ordering(sysl):
	required = ['ordering', 'order']
	if not IOstuff.check_required_keys(request.form, required):
		return redirect(f'/beheer/{sysl}')
	try:
		ordering = request.form.get('ordering').split(',')
	except:
		print(f"ordering mislukt {request.form.get('ordering')}")
		return redirect(f'/beheer/{sysl}')

	sysls_o = Sysls()
	alle = sysls_o.get_sysl(sysl)
	oo = 1
	for id in ordering:
		id = int(id)
		# ordering contains id's in requested order
		if not id in alle.keys():
			# print(f"ontbrekende key {id} in {alle}")
			return redirect(f'/beheer/{sysl}')
		alle[id]['ordering'] = oo
		sysls_o.store_sysl_mongo(where={'sysl': sysl, 'id': id}, what={'$set': {'ordering': oo}})
		oo += 1
	return redirect(f'/beheer/{sysl}')

