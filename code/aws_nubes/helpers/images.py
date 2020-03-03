"""aws_nubes.helpers.images.

This module provide functions to manage the use of images
"""
from flask import flash
import boto3
from PIL import Image
from boto3.dynamodb.conditions import Key, Attr
import os
import io
from config import table, images_directory, s3, my_bucket


def bufferExtensions(ext):
    bufferExt = ''
    if ext == '.jpg' or ext == '.jpeg':
        bufferExt = 'JPEG'
    elif ext == '.png':
        bufferExt = 'PNG'
    else:
        ext == 'ERROR'
    return bufferExt

def resizeImage(file, height, width, label):
    if file.filename != '':
        name, ext = os.path.splitext(file.filename)
        if ext in set(['.jpg', '.jpeg', '.png']):
            destination = '/'.join([images_directory, file.filename])
            bufferExt = bufferExtensions(ext)

            file.save(destination)
            image = Image.open(destination)

            buffer = io.BytesIO()
            image.save(buffer, bufferExt)
            #s3_resource = boto3.resource('s3')
            buffer.seek(0)
            s3.put_object(
                Bucket = 'proyectofinalnubes',
                Key = name + ext,
                Body = buffer
            )
            
            
            new_image = image.resize((width, height))
            buffer.seek(0)
            new_image.save(buffer,bufferExt)
            buffer.seek(0)
            s3.put_object(
                Bucket='proyectofinalnubes',
                Key=name + '_resized' + ext,
                Body=buffer
            )
            os.remove(destination)
            flash('File uploaded succesfully')

            # ---------------------DYNAMODB-------------------------
            #my_bucket = s3_resource.Bucket('proyectofinalnubes')
            etiq = label.split(', ')

            table.put_item(
                Item={
                    'Link': file.filename,
                    'Etiqueta': etiq,
                }
            )
            table.put_item(
                Item={
                    'Link': name + '_resized' + ext,
                    'Etiqueta': etiq,
                }
            )
            summaries = []
            for s3_file in my_bucket.objects.all():
                if s3_file.key == name + '_resized' + ext:
                    summaries.append(s3_file)

            return (True,summaries)
        else:
            flash('Extension not supported')
            return (False,'')

    else:
        flash('Please choose a file')
        return (False,'')

