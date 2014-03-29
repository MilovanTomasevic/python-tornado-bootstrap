# coding: utf-8
import logging
from mimetypes import MimeTypes
from StringIO import StringIO
import requests
import six


def replace_with_placeholder(field, img, content_type, place_holder_url=None, place_holder_filepath=None):
    try:
        field.replace(img, content_type=content_type)
    except AssertionError as e:
        logging.error(str(e))
        logging.exception(e)
        if place_holder_url:
            save_from_url(field, place_holder_url, persist=True)
        elif place_holder_filepath:
            save_from_file(field, place_holder_filepath, persist=True)
        else:
            six.reraise(e)


def save_from_file(field, filepath, persist=False, place_holder_url=None, place_holder_filepath=None):
    img = open(filepath, 'r')
    content_type = None
    mime = MimeTypes()
    content_type = mime.guess_type(filepath)[0]
    replace_with_placeholder(field, img, content_type, place_holder_url=place_holder_url, place_holder_filepath=place_holder_filepath)
    img.seek(0)
    img.close()
    if persist:
        field.instance.save()
    return img


def save_from_url(field, url, persist=False, place_holder_url=None, place_holder_filepath=None):
    r = requests.get(url)
    img = StringIO(r.content)
    content_type = r.headers['content-type']
    replace_with_placeholder(field, img, content_type, place_holder_url=place_holder_url, place_holder_filepath=place_holder_filepath)
    img.seek(0)
    if persist:
        field.instance.save()
    return img


def save_from_request(field, fileinfo, persist=False, place_holder_url=None, place_holder_filepath=None):
    content = fileinfo['body']
    content_type = fileinfo['content_type']
    img = StringIO(content)
    replace_with_placeholder(field, img, content_type, place_holder_url=place_holder_url, place_holder_filepath=place_holder_filepath)
    if persist:
        field.instance.save()
    return img
