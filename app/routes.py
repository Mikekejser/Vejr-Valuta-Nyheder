from flask import render_template, flash, redirect, request, url_for
from app import app, db
from .forms import LoginForm, OpretForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import Bruger, By
from werkzeug.urls import url_parse
import os
import requests
from bs4 import BeautifulSoup


@app.route('/', methods=['GET', 'POST'])
@app.route('/vejr', methods=['GET', 'POST'])
def vejr():
	VEJR_APPID = app.config['VEJR_APPID']
	vejr_data = []

	if request.method == 'POST':
		by = request.form.get('by')
		r = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={by}&units=metric&appid={VEJR_APPID}')
		if r.status_code == 200:
			if current_user.is_authenticated:
				if By.query.filter_by(bruger_id=current_user.id, navn=by).first() != None:
					flash(f'Du har allerede tilføjet {by}')
				else:
					by_object = By(bruger_id=current_user.id, navn=by)
					db.session.add(by_object)
					db.session.commit()
					flash(f'{by} blev tilføjet!')
			else:
				r = requests.get(url).json()
				vejr_data = {
					'by': by,
					'temperatur': round(r['main']['temp'], 1),
					'beskrivelse': r['weather'][0]['description'],
					'billede': r['weather'][0]['icon']
				}
		else:
			flash('Prøv en anden by eller se om du har stavet rigtigt.')

	if current_user.is_authenticated:
		byer = By.query.filter_by(bruger_id=current_user.id).all()
		for by in byer:
			url = f'http://api.openweathermap.org/data/2.5/weather?q={by.navn}&units=metric&appid={VEJR_APPID}'
			r = requests.get(url).json()

			vejr = {
				'by': by.navn,
				'temperatur': round(r['main']['temp'], 1),
				'beskrivelse': r['weather'][0]['description'],
				'billede': r['weather'][0]['icon']
			}

			vejr_data.append(vejr)
			
	return render_template('vejr.html', vejr_data=vejr_data)


@app.route('/valuta')
def valuta():
	VALUTA_API_KEY = app.config['VALUTA_API_KEY']
	url = f'http://data.fixer.io/api/latest?access_key={VALUTA_API_KEY}'
	r = requests.get(url).json()
	valuta = {
		'USD': round(r['rates']['USD'], 2),
		'DKK': round(r['rates']['DKK'], 2),
		'NOK': round(r['rates']['NOK'], 2),
		'ISK': round(r['rates']['ISK'], 2),
		'GBP': round(r['rates']['GBP'], 2),
		'AUD': round(r['rates']['AUD'], 2),
	}

	return render_template('valuta.html', valuta=valuta)	


@app.route('/nyheder')
def nyheder():
	nyheder = []

	mainPage = requests.get('http://tv2.dk')
	if mainPage.status_code == 200:
		mainSoup = BeautifulSoup(mainPage.content, 'html.parser')
		topStory = mainSoup.find('a', class_='o-teaser_link')
		topStoryHeadline = mainSoup.find('h2', class_='o-teaser_headline').string
		articleLink = 'http:' + topStory['href']

		tv2 = {
			'overskrift': topStoryHeadline or articleLink,
			'url': articleLink,
			'logo': url_for('static', filename='tv2.png')
		}

		nyheder.append(tv2)
	else:
		flash('Kunne ikke læse alle nyheder.')

	mainPage = requests.get('https://jyllands-posten.dk')
	if mainPage.status_code == 200:
		mainSoup = BeautifulSoup(mainPage.content, 'html.parser')
		topStory = mainSoup.find('h2', class_='artTitle')
		try:
			topStoryHeadline = topStory.span.string
		except:
			topStoryHeadline = topStory.a.string
		articleLink = topStory.a['href']

		jyllands_posten = {
			'overskrift': topStoryHeadline or articleLink,
			'url': articleLink,
			'logo': url_for('static', filename='jyllands-posten.png')
		}

		nyheder.append(jyllands_posten)
	else:
		flash('Kunne ikke læse alle nyheder.')
	
	mainPage = requests.get('https://borsen.dk')
	if mainPage.status_code == 200:
		mainSoup = BeautifulSoup(mainPage.content, 'html.parser')
		topStory = mainSoup.find('h1', class_='article-title')
		topStoryHeadline = topStory.a.string
		articleLink = topStory.a['href']
	
		børsen = {
			'overskrift': topStoryHeadline or articleLink,
			'url': articleLink,
			'logo': url_for('static', filename='børsen.png')
		}

		nyheder.append(børsen)
	else:
		flash('Kunne ikke læse alle nyheder.')

	return render_template("nyheder.html", nyheder=nyheder)



@app.route('/slet/<navn>')
@login_required
def slet(navn):
	by = By.query.filter_by(bruger_id=current_user.id, navn=navn).first_or_404()
	db.session.delete(by)
	db.session.commit()
	flash(f'By {by.navn} blev slettet.')
	return redirect(url_for('vejr'))


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('vejr'))
	form = LoginForm()
	if form.validate_on_submit():
		bruger = Bruger.query.filter_by(brugernavn=form.brugernavn.data).first()
		if bruger is None or not bruger.check_password(form.adgangskode.data):
			flash('Forkert brugernavn eller adgangskode')
			return redirect(url_for('login'))
		login_user(bruger, remember=form.husk_mig.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('vejr')
		return redirect(next_page)
	return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('vejr'))


@app.route('/opret', methods=['GET', 'POST'])
def opret():
    if current_user.is_authenticated:
        return redirect(url_for('vejr'))
    form = OpretForm()
    if form.validate_on_submit():
        bruger = Bruger(brugernavn=form.brugernavn.data, email=form.email.data)
        bruger.set_password(form.adgangskode.data)
        db.session.add(bruger)
        db.session.commit()
        flash('Ny bruger blev oprettet!')
        return redirect(url_for('login'))
    return render_template('opret.html', form=form)
