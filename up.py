#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, request, flash, redirect, url_for, render_template, jsonify
from flask import send_file
from werkzeug import secure_filename
import os
from PIL import Image
from StringIO import StringIO
import shutil
import json


from scripts import izi


app = Flask(__name__)
app.secret_key = 'd66HR8dç"f_-àgjYYic*dh'

app.debug = True

DOSSIER_UPS = 'ups/'
TEXT_FOLDERS = 'texts/'
DATA_FOLDERS = 'data/'

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy

data_complexity = []


@app.route("/complexity", methods=['GET', 'POST'])
def complexity():
    # return json.dumps( result )
    return json.dumps(izi.getComplexityData(TEXT_FOLDERS +  [t for t in os.listdir(TEXT_FOLDERS)][0] ))

@app.route("/topics", methods=['GET', 'POST'])
def topics():
    # return json.dumps( result )
    return json.dumps(izi.getTopicDistributionData(TEXT_FOLDERS +  [t for t in os.listdir(TEXT_FOLDERS)][0] ))

@app.route("/significantWords", methods=['GET', 'POST'])
def significantWords():
    # return json.dumps( result )
    return json.dumps(izi.getMostSignificantWordsData(TEXT_FOLDERS +  [t for t in os.listdir(TEXT_FOLDERS)][0] ))

@app.route("/topicsGraph", methods=['GET', 'POST'])
def topicsGraph():
    # return json.dumps( result )
    return json.dumps(izi.defSignificantWordsGraph(TEXT_FOLDERS +  [t for t in os.listdir(TEXT_FOLDERS)][0] ))

def processFile( path ):
    return izi.displayResults( path )


def extension_ok(nomfic):
    """ Renvoie True si le fichier possède une extension d'image valide. """
    return '.' in nomfic and nomfic.rsplit('.', 1)[1] in ('txt', 'mxliff')

def is_image(nomfic):
    """ Renvoie True si le fichier possède une extension d'image valide. """
    return '.' in nomfic and nomfic.rsplit('.', 1)[1] in ('jpg', 'png')


@app.route('/', methods=['GET', 'POST'])
@app.route('/up/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # if request.form['pw'] == 'up': # on vérifie que le mot de passe est bon
        f = request.files['fic']
        if f: # on vérifie qu'un fichier a bien été envoyé
            if extension_ok(f.filename): # on vérifie que son extension est valide
                nom = secure_filename(f.filename)
                # remove previous files
                images = [img for img in os.listdir(DOSSIER_UPS)]
                for i in images:
                    os.remove(DOSSIER_UPS + i)
                txts = [t for t in os.listdir(TEXT_FOLDERS)]
                for i in txts:
                    os.remove(TEXT_FOLDERS + i)
                f.save(TEXT_FOLDERS + nom)
                # processFile( TEXT_FOLDERS + nom )
                flash(u'File sent. Here is the <a href="{lien}"> link </a>.'.format(lien=url_for('d3')), 'succes')
            else:
                flash(u'Ce fichier ne porte pas une extension autorisée !', 'error')
        else:
            flash(u'Vous avez oublié le fichier !', 'error')
        # else:
        #     flash(u'Mot de passe incorrect', 'error')
    return render_template('up_up.html')

@app.route('/up/view/', methods=['GET', 'POST'])
def liste_upped():
    images = [img for img in os.listdir(DOSSIER_UPS) if is_image(img)] # la liste des images dans le dossier
    if request.method == 'POST':
        if request.form['submit']:
            print "maybe here ?"
        if request.form['submit'] == 'Delete All Files':
            print "YOLO it works"
    return render_template('up_liste.html', images=images)


@app.route('/d3/')
def d3():
    d = [d for d in os.listdir(DATA_FOLDERS) ]
    return render_template('d3.html')


@app.route('/up/view/<nom>')
def upped(nom):
    nom = secure_filename(nom)
    if os.path.isfile(DOSSIER_UPS + nom): # si le fichier existe
        return send_file(DOSSIER_UPS + nom, as_attachment=True) # on l'envoie
    else:
        flash(u'Fichier {nom} inexistant.'.format(nom=nom), 'error')
        return redirect(url_for('liste_upped')) # sinon on redirige vers la liste des images, avec un message d'erreur

if __name__ == '__main__':
    app.run(host = '0.0.0.0')