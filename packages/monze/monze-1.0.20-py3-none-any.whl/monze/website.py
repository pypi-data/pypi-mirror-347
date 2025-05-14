from flask import redirect, request, Blueprint, render_template

from general import JINJAstuff, FtpAnta
from singletons import UserSettings, Sysls

def jinja_object(ding):
	sysls_o = Sysls()
	return JINJAstuff(ding, sysls_o.get_model())

# =============== endpoints =====================
ep_website = Blueprint(
	'ep_website', __name__,
	url_prefix="/website",
	template_folder='templates',
    static_folder='static',
	static_url_path='static',
)

def get_website_model():
	return dict(
		updated={'default': 0},
		door={'default': 'Victor'},
		html={'default': default_html()},
	)
def get_empty_website():
	d = get_website_model()
	for key in d:
		d[key] = d[key]['default']
	return d

menuitem = 'website'

@ep_website.get('/<path:bron>')
@ep_website.get('/')
def website(bron='local'):
	jus = UserSettings()
	if not jus.magda(['beheer']):
		return redirect('/home')

	# ophalen pickle met website
	website = None
	# get from ftp
	anta = FtpAnta(
		'cpnits.com',
		'cpnitswebsite@cpnits.com',
		'CpnitsWebsite',
		'public_html'
	)
	if anta.has_indexhtml():
		html = anta.get_indexhtml()
		if not html is None:
			website = get_empty_website()
			website['html'] = html

	try:
		message = request.args.get('message')
		if message is None:
			message = ''
	except:
		# no arg 'gelukt'
		message = ''

	website = jinja_object(website)
	return render_template(
		'website.html',
		menuitem=menuitem,
		props=jus,
		website=website,
		message=message,
		bron=bron
	)

@ep_website.post('/')
def post_website():
	jus = UserSettings()
	if not jus.magda(['beheer']):
		return redirect('/home')

	if 'html' in request.form:
		html = request.form.get('html')
	else:
		return redirect(f'/website')

	# ftp to live
	anta = FtpAnta(
		'cpnits.com',
		'cpnitswebsite@cpnits.com',
		'CpnitsWebsite',
		'public_html'
	)
	if anta.has_indexhtml():
		if anta.put_indexhtml(html):
			return redirect('/website')

	return redirect(f'/website')

''' 
@ep_website.get('/htmlexample')
def html_example():
	jus = UserSettings()
	if not jus.magda(['beheer']):
		return redirect('/home')

	sysls_o = Sysls()
	website = sysls_o.get_sysl('website', other=True)
	if website is None:
		website = get_empty_website()

	print(website)

	html = str(website['html'])
	html = html.replace('https://cpnits.com/', 'http://127.0.0.1:5000/website/htmlexample/')
	html = html.replace('static/', 'https://cpnits.com/static/')
	print(html)
	return html
'''

def default_html():
	return '''<!DOCTYPE HTML>
<html>
	<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<title>CPNITS</title>
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<meta name="description" content="Minor Creative Programming for Non-IT Students" />
	<meta name="keywords" content="programming students hbo" />
    <link rel="icon" type="image/x-icon" href="static/codelogo.png">

  	<!-- Facebook and Twitter integration -->
	<meta property="og:title" content=""/>
	<meta property="og:image" content=""/>
	<meta property="og:url" content=""/>
	<meta property="og:site_name" content=""/>
	<meta property="og:description" content=""/>
	<meta name="twitter:title" content="" />
	<meta name="twitter:image" content="" />
	<meta name="twitter:url" content="" />
	<meta name="twitter:card" content="" />

	<!-- <link href="https://fonts.googleapis.com/css?family=Work+Sans:300,400,500,700,800" rel="stylesheet">	 -->
	<link href="https://fonts.googleapis.com/css?family=Inconsolata:400,700" rel="stylesheet">
	
	<!-- Animate.css -->
	<link rel="stylesheet" href="static/css/animate.css">
	<!-- Icomoon Icon Fonts-->
	<link rel="stylesheet" href="static/css/icomoon.css">
	<!-- Bootstrap  -->
	<link rel="stylesheet" href="static/css/bootstrap.css">
	<!-- Flexslider  -->
	<link rel="stylesheet" href="static/css/flexslider.css">

	<!-- Theme style  -->
	<link rel="stylesheet" href="static/css/style.css">

    <link rel="stylesheet" href="static/style-adjust.css">

	<!-- Modernizr JS -->
	<script src="static/js/modernizr-2.6.2.min.js"></script>
	<!-- FOR IE9 below -->
	<!--[if lt IE 9]>
	<script src="static/js/respond.min.js"></script>
	<![endif]-->

	</head>
	<body>
		
	<div class="fh5co-loader"></div>
	
	<div id="page">
	<nav class="fh5co-nav" role="navigation">
		<div class="top-menu">
			<div class="container">
				<div class="row">
					<div class="col-xs-2">
						<div id="fh5co-logo"><a href="">cpnits<span>.</span></a></div>
					</div>
					<div class="col-xs-10 text-right menu-1">
						<ul>
							<li class="active"><a href="">Home</a></li>
							<li><a href="#program">Program</a></li>
                            <li><a href="#fh5co-wireframe">15/30EC</a></li>
                            <li><a href="#enroll">Enroll</a></li>
							<!-- <li class="btn-cta"><a href="login"><span>Login</span></a></li> -->
						</ul>
					</div>
				</div>
				
			</div>
		</div>
	</nav>

	<header id="fh5co-header" class="fh5co-cover js-fullheight" role="banner">
		<div class="overlay"></div>
		<div class="container">
			<div class="row">
				<div class="col-md-8 col-md-offset-2 text-center">
					<div class="display-t js-fullheight">
						<div class="display-tc js-fullheight animate-box" data-animate-effect="fadeIn">
							<h1>Creativity is a wild mind with a disciplined mindset</h1>
							<h2>Minor: Creative programming for non-it students</h2>
							<p><a class="btn btn-primary btn-lg btn-demo" href="#program">Programm</a> <a href="#enroll" class="btn btn-primary btn-lg btn-learn">Enroll</a></p>
						</div>
					</div>
				</div>
			</div>
		</div>
	</header>

	<div id="program" class="box-features">
		<div class="container">
			<div class="services-padding">
				<div class="row">

					<div class="col-md-4 animate-box">
						<div class="feature-left">
							<span class="icon">
								<i class="icon-progress-empty"></i>
							</span>
							<div class="feature-copy">
								<h3>We start at zero</h3>
								<p>No prior knowledge or experience is needed to follow this cours. We start at zero. IT-students and E-students are not admissible.</p>
								<!-- <p><a href="#">Learn More <i class="icon-arrow-right22"></i></a></p> -->
							</div>
						</div>
					</div>

					<div class="col-md-4 animate-box">
						<div class="feature-left">
							<span class="icon">
								<i class="icon-cloud"></i>
							</span>
							<div class="feature-copy">
								<h3>100% online</h3>
								<p>This course is 100% online. You can follow this program anywhere in the world. All materials, tools, lectures, meetings are online.</p>
							</div>
						</div>
					</div>

					<div class="col-md-4 animate-box">
						<div class="feature-left">
							<span class="icon">
								<i class="icon-write"></i>
							</span>
							<div class="feature-copy">
								<h3>No final test</h3>
								<p>The minor contains a few sprints – online scavenger hunts – and ends with a final project. Results are added to a personal portfolio. Grading is based on these products.</p>
							</div>
						</div>
					</div>
				</div>

				<div class="row">
					<div class="col-md-4 animate-box">
						<div class="feature-left">
							<span class="icon">
								<i class="icon-clock"></i>
							</span>
							<div class="feature-copy">
								<h3>Full time program</h3>
								<p>This is a fulltime – 40 hours per week – program and not a correspondence course, with mandatory meetings. We expect you to be available for eduction from Tuesdays until Fridays, 9AM to 5PM. Schedule may vary. <strong>Not suitable for parttime students.</strong></p>
							</div>
						</div>

					</div>

					<div class="col-md-4 animate-box">
						<div class="feature-left">
							<span class="icon">
								<i class="icon-code"></i>
							</span>
							<div class="feature-copy">
								<h3>Languages</h3>
								<p>The main programming languages are Python and SQL, with some additional HTML, CSS and JavaScript and whatever you like to use.</p>
							</div>
						</div>

					</div>
					<div class="col-md-4 animate-box">
						<div class="feature-left">
							<span class="icon">
								<i class="icon-medal"></i>
							</span>
							<div class="feature-copy">
								<h3>Harvard Certificates</h3>
								<p>We use the world famous Harvard CS50 programs, with our own twist. This course can result in one or more Harvard Certificates.</p>
							</div>
						</div>
					</div>
				</div>

                <div class="row">
					<div class="col-md-4 animate-box">
						<div class="feature-left">
							<span class="icon">
								<i class="icon-language"></i>
							</span>
							<div class="feature-copy">
								<h3>Dutch and/or English</h3>
								<p>Both 15ec and 30ec are offered in Dutch and English. However in case of a limited group size, we can switch to English only. The portfolio can be written in Dutch, if preferred.</p>
							</div>
						</div>

					</div>

					<div class="col-md-4 animate-box">
						<div class="feature-left">
							<span class="icon">
								<i class="icon-tools"></i>
							</span>
							<div class="feature-copy">
								<h3>No special software</h3>
								<p>All you need to follow this course, is Google Chrome, webcam and microphohne on a fairly modern pc or mac (no chrome-book) with a proper internet connection.</p>
							</div>
						</div>

					</div>
					<div class="col-md-4 animate-box">
						<div class="feature-left">
							<span class="icon">
								<i class="icon-box"></i>
							</span>
							<div class="feature-copy">
								<h3>Matchbox Webserver [30ec]</h3>
								<p>We use a few items (mandatory, 30ec only), including a complete matchbox size microcomputer that can operate as webserver or a gaming device. Costs max: 40 EUR.</p>
								<!-- <p><a href="#">Pre-order the package here <i class="icon-arrow-right22"></i></a></p> -->
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

	<div id="fh5co-wireframe">
		<div class="container">
			<div class="row animate-box">
				<div class="col-md-8 col-md-offset-2 text-center fh5co-heading">
					<h2>Master the basics or dive in deeper</h2>
				</div>
			</div>
			<div class="row">
				<div class="col-md-5 animate-box">
					<div class="user-frame">
						<h3>Master the basics [15ec]</h3>
						<p>
                            With the 15ec program you learn to master the basics of Python programming. Including testing, exceptions, regular expressions, object oriented programming and SQL for databases.
                        </p>
                        <p>This program can result in a genuine Harvard Certificate.</p>
                        <p><strong>Available in Dutch and English</strong> if group size is sufficient. However all learning material is in English.</p>
						<small><a href="#enroll">Enroll now</a></small>
					</div>
				</div>
				<div class="col-md-7 animate-box">
					<p>
                        The <strong class="bg-donker">30ec program</strong> continues, where the 15 EC program left of. After the first period you choose your specialization: Data, Web dev, App dev, or Artificial Intelligence.
                    </p>
                    <p>
                        <strong>Web dev</strong> is an assignment based program, building up to developing an interactive website backed by a SQL database.
                    </p>
                    <p>
                        <strong>Data</strong> is less structured than Web dev. It introduces you into the world of API's, web scraping, SQL and Mongo, focussing also on business opportunities.
                    </p>
                    <p>
                        <strong>App dev</strong> requires an inquisitive mind and the necessary self-reliance, resulting in a working stand-alone app suitable for mobile or desktop, backed by a database driven API.
                    </p>
                    <p>
                        <strong>Artificial Intelligence</strong> is not about asking questions to ChatGPT, but offers an assignment based, mathematical approach to concepts like: search, uncertainty, machine learning, language and neural networks. <strong class="bg-licht">Not for the faint-hearted!</strong>
                    </p>
                    <blockquote><p>This second part is only available in English. You can write your portfolio in Dutch if you prefer.</p></blockquote>
                    <small><a href="#enroll">Enroll now</a></small>
				</div>
			</div>
		</div>
	</div>

    <div id="enroll" class="box-features">
		<div class="container">
			<div class="services-padding">
				<div class="row">

                    <div class="col-md-4 animate-box">
						<div class="feature-left">
							<span class="icon number">
								15
							</span>
							<div class="feature-copy">
								<h3>15ec Nederlands</h3>
								<p>
                                    15ec Nederlands als voertaal, mits de groepsomvang dit toestaat.
                                </p>
								<p>
                                    <a target="_blank" href="https://www.nhlstenden.com/minoren/creatief-programmeren-voor-niet-it-studenten-15-ec">Inschrijven in Progress <i class="icon-arrow-right22"></i></a><br>
                                    <a target="_blank" href="https://www.kiesopmaat.nl/modules/31fr/-/142679/">Inschrijven via Kies op Maat <i class="icon-arrow-right22"></i></a>
                                </p>
							</div>
						</div>
					</div>

                    <div class="col-md-4 animate-box">
						<div class="feature-left">
							<span class="icon number">
								30
							</span>
							<div class="feature-copy">
								<h3>30ec Nederlands</h3>
								<p>
                                    30ec Nederlands als voertaal gedurende de eerste periode van het semester, mits de groepsomvang dit toestaat.
                                </p>
								<p>
                                    <a target="_blank" href="https://www.nhlstenden.com/minoren/creatief-programmeren-voor-niet-it-studenten-30-ec">Inschrijven in Progress <i class="icon-arrow-right22"></i></a><br>
                                    <a target="_blank" href="https://www.kiesopmaat.nl/modules/31fr/-/142681/">Inschrijven via Kies op Maat <i class="icon-arrow-right22"></i></a>
                                </p>
							</div>
						</div>
					</div>

                    <div class="col-md-4 animate-box">
						<div class="feature-left">
							<span class="icon number">
								<i class="icon-info"></i>
							</span>
							<div class="feature-copy">
								<h3>Meer info</h3>
								<p>
                                    Er valt niet veel meer te vertellen. Rooster en moduleboek krijg je een paar weken voor aanvang, verder vind je alles in deze website. Maar, voor contact, email: cpnits@nhlstenden.com.<br>
                                </p>
							</div>
						</div>
					</div>

				</div>

				<div class="row" style="border-top: 1px solid white; padding: 1em 0em;">
                    <div class="col-md-4 animate-box">
						<div class="feature-left">
							<span class="icon number">
								15
							</span>
							<div class="feature-copy">
								<h3>15ec English</h3>
								<p>
                                    15ec English. End products may be produced in Dutch if preferred.<br>
                                </p>
                                <p>
                                    <a target="_blank" href="https://www.nhlstenden.com/en/minors/creative-programming-for-non-it-students-15-ec">Enroll in Progress <i class="icon-arrow-right22"></i></a><br>
                                    <a target="_blank" href="https://www.kiesopmaat.nl/modules/31fr/-/142682/">Enroll via Kies op Maat <i class="icon-arrow-right22"></i></a>
                                </p>
							</div>
						</div>
					</div>

                    <div class="col-md-4 animate-box">
						<div class="feature-left">
							<span class="icon number">
								30
							</span>
							<div class="feature-copy">
								<h3>30ec English</h3>
								<p>
                                    30ec English. End products may be produced in Dutch if preferred.<br>
                                </p>
                                <p>
                                    <a target="_blank" href="https://www.nhlstenden.com/en/minors/creative-programming-for-non-it-students-30-ecs">Enroll in Progress <i class="icon-arrow-right22"></i></a><br>
                                    <a target="_blank" href="https://www.kiesopmaat.nl/modules/31fr/-/142685/">Enroll via Kies op Maat <i class="icon-arrow-right22"></i></a>
                                </p>
							</div>
						</div>
					</div>

                    <div class="col-md-4 animate-box">
						<div class="feature-left">
							<span class="icon number">
								<i class="icon-info"></i>
							</span>
							<div class="feature-copy">
								<h3>More info</h3>
								<p>
                                    There's not much more to tell. You get your schedule and module book a week or two before we start, all other info is in this website. But, for contact, email: cpnits@nhlstenden.com.<br>
                                </p>
							</div>
						</div>
					</div>
				</div>

			</div>
		</div>
	</div>


	<footer id="fh5co-footer" role="contentinfo">
		<div class="container">
			<div class="row copyright">
				<div class="col-md-12 text-center">
					<p id="contact-p">
						<small class="block">&copy; 2024 All Rights Reserved: NHL Stenden.</small>
					</p>
				</div>
			</div>

		</div>
	</footer>
	</div>

	<div class="gototop js-top">
		<a href="#" class="js-gotop"><i class="icon-arrow-up22"></i></a>
	</div>
	
	<!-- jQuery -->
	<script src="static/js/jquery.min.js"></script>
	<!-- jQuery Easing -->
	<script src="static/js/jquery.easing.1.3.js"></script>
	<!-- Bootstrap -->
	<script src="static/js/bootstrap.min.js"></script>
	<!-- Waypoints -->
	<script src="static/js/jquery.waypoints.min.js"></script>
	<!-- Flexslider -->
	<script src="static/js/jquery.flexslider-min.js"></script>
	<!-- Main -->
	<script src="static/js/main.js"></script>

    <script>
        let scrollto = function(tag){
            $('html, body').animate({
                scrollTop: $(tag).offset().top + 60
            }, 1000);
        }

        $(function(){
            $('li a').on('click', function(e){
                // e.preventDefault();
                let ding = $(this).attr('href');
                scrollto(ding)
            });
            $('small a').on('click', function(e){
                // e.preventDefault();
                let ding = $(this).attr('href');
                scrollto(ding)
            })
            $('a.btn').on('click', function(e){
                // e.preventDefault();
                let ding = $(this).attr('href');
                scrollto(ding)
            })
        });
    </script>
	</body>
</html>'''

