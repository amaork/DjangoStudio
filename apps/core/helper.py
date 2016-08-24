# -*- coding: utf-8 -*-
import os
import shutil
from .models import Document


def add_document(media_root, document, name=""):
    """Add a document

    :param media_root: media root
    :param document: document path
    :param name: document name
    :return: True of false
    """
    document_name = os.path.basename(document)
    documents_root = os.path.join(media_root, Document.get_upload_path())

    if not os.path.isfile(document):
        print("File:{0:s} is not exists!".format(document))
        return True

    try:

        name = name or os.path.splitext(document_name)[0]
        if not Document.objects.filter(name=name).exists():

            if not os.path.isdir(documents_root):
                os.makedirs(documents_root)

            # Copy file to documents root and create documents instance
            shutil.copy(document, os.path.join(documents_root, document_name))
            Document.objects.create(name=name, file=Document.get_upload_path() + "/" + document_name)

    except shutil.Error as e:
        print("Copy file:{0:s} to documents root:{1:s} error:{2:s}".format(document, documents_root, e))
        return False

    return True


def bulk_add_documents(media_root, path):
    """Bulk Documents

    :param media_root: media root
    :param path: documents path
    :return: Success True
    """
    if not os.path.isdir(path):
        print("Path:{0:s} is not a directory!".format(path))
        return False

    for file_name in os.listdir(path):
        add_document(media_root, os.path.join(path, file_name))

    return True
