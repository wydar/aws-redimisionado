from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from aws_nubes.helpers.images import bufferExtensions, resizeImage

from config import table, images_directory, s3, my_bucket

index_bp = Blueprint('index', __name__)

@index_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@index_bp.route('/search', methods=['POST'])
def search():
    label = request.values.get("Busqueda")

    # ------------ Busqueda por etiquetas------------------
    summaries = []
    response = table.scan()
    for r in response["Items"]:
        for a in r["Etiqueta"]:
            if a == label.lower():
                for s3_file in my_bucket.objects.all():
                    if s3_file.key == r["Link"]:
                        summaries.append(s3_file)

    return render_template('all_img.html', files=summaries, label = label)

@index_bp.route('/imgs', methods=['GET', 'POST'])
def imgs():

    summaries = my_bucket.objects.all()

    return render_template('all_img.html', files=summaries)


@index_bp.route('/files', methods=['GET', 'POST'])
def files():
    summaries = my_bucket.objects.all()
    return render_template('files.html', my_bucket=my_bucket, files=summaries)


@index_bp.route('/upload', methods=['POST'])
def upload():
    file = request.files['img']
    height = int(request.values.get("height"))
    width = int(request.values.get("width"))
    label = request.values.get("label").lower()
    reiszed = resizeImage(file, height, width, label)

    if reiszed[0] == True:
        return render_template('index.html', files=reiszed[1])
    else:
        return redirect(url_for('.index'))


@index_bp.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']

    my_bucket.Object(key).delete()

    flash('File deleted succesfully')

    return redirect('/files')


@index_bp.route('/download', methods=['POST'])
def download():
    key = request.form['key']

    file_obj = my_bucket.Object(key).get()

    return Response(
        file_obj['Body'].read(),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename={}".format(key)}
    )