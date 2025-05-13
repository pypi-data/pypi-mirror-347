#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Document identifier name converter. """

__version__ = '2.2.0.22'


def get_document_name(docid):
    """ Return the name of a general document.

    :param docid:       The document code.
    :return:            The name of a general document.
    """
    values = ["Unknown document",
              "ICAO standard Passport (MRP)",
              "ICAO standard 2 row Travel Document (TD-2)",
              "ICAO standard 3 row Travel Document (TD-1)",
              "ICAO standard visa (MRV-A) (MRV-B)",
              "French ID card",
              "Pre ICAO standard 3 row Travel Document",
              "Slovak ID card",
              "AAMVA standard driving license",
              "Belgian ID",
              "Swiss driving license",
              "ID of Cote d'Ivoire",
              "Financial Transaction Card",
              "IATA boarding pass",
              "ICAO Travel Document (TD-1, front page, named)",
              "ICAO Travel Document (TD-1, front page, typed)",
              "ISO standard driving license",
              "Mail item",
              "ICAO standard electronic document (Passport/ID)",
              "EID",
              "ESign",
              "NFC",
              "European standard driving license",
              "Portuguese ID",
              "Ecuadorian ID",
              "ID card with MRZ",
              "USA military ID",
              "Vehicle Registration Document",
              "Local border traffic permit"]
    return values[docid] if 0 <= docid < len(values) else ""


def get_doc_type_name(doc_type):
    """ Return the document type name.

    :param doc_type:    Document type identifier string.
    :return:            The name of the document type.
    """
    dt2 = doc_type[0:2]
    if    dt2 == "DL":
        if   doc_type == "DLL": ret = "driving license for learner"
        else:                   ret = "driving license"
    elif dt2 == "ID":
        if   doc_type == "IDF": ret = "ID card for foreigner"
        elif doc_type == "IDC": ret = "ID card for children"
        else:                   ret = "ID card"
    elif dt2 == "PP":
        if   doc_type == "PPD": ret = "diplomatic passport"
        elif doc_type == "PPS": ret = "service passport"
        elif doc_type == "PPE": ret = "emergency passport"
        elif doc_type == "PPC": ret = "passport for children"
        else:                   ret = "passport"
    elif dt2 == "TD": ret = "travel document"
    elif dt2 == "RP": ret = "residence permit"
    elif dt2 == "VS": ret = "visa"
    elif dt2 == "WP": ret = "work permit"
    elif dt2 == "SI": ret = "social insurance document"
    else:             ret = "document"
    return ret


def get_page_name(doc_page):
    """ Return the page name.

    :param doc_page:    Document page identifier.
    :return:            Document page name.
    """
    if    doc_page == "F": ret = "front"
    elif  doc_page == "B": ret = "back"
    else:                  ret = ""
    return ret
