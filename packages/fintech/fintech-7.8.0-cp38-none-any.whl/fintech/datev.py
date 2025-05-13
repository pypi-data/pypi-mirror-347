
###########################################################################
#
# LICENSE AGREEMENT
#
# Copyright (c) 2014-2024 joonis new media, Thimo Kraemer
#
# 1. Recitals
#
# joonis new media, Inh. Thimo Kraemer ("Licensor"), provides you
# ("Licensee") the program "PyFinTech" and associated documentation files
# (collectively, the "Software"). The Software is protected by German
# copyright laws and international treaties.
#
# 2. Public License
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this Software, to install and use the Software, copy, publish
# and distribute copies of the Software at any time, provided that this
# License Agreement is included in all copies or substantial portions of
# the Software, subject to the terms and conditions hereinafter set forth.
#
# 3. Temporary Multi-User/Multi-CPU License
#
# Licensor hereby grants to Licensee a temporary, non-exclusive license to
# install and use this Software according to the purpose agreed on up to
# an unlimited number of computers in its possession, subject to the terms
# and conditions hereinafter set forth. As consideration for this temporary
# license to use the Software granted to Licensee herein, Licensee shall
# pay to Licensor the agreed license fee.
#
# 4. Restrictions
#
# You may not use this Software in a way other than allowed in this
# license. You may not:
#
# - modify or adapt the Software or merge it into another program,
# - reverse engineer, disassemble, decompile or make any attempt to
#   discover the source code of the Software,
# - sublicense, rent, lease or lend any portion of the Software,
# - publish or distribute the associated license keycode.
#
# 5. Warranty and Remedy
#
# To the extent permitted by law, THE SOFTWARE IS PROVIDED "AS IS",
# WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF QUALITY, TITLE, NONINFRINGEMENT,
# MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, regardless of
# whether Licensor knows or had reason to know of Licensee particular
# needs. No employee, agent, or distributor of Licensor is authorized
# to modify this warranty, nor to make any additional warranties.
#
# IN NO EVENT WILL LICENSOR BE LIABLE TO LICENSEE FOR ANY DAMAGES,
# INCLUDING ANY LOST PROFITS, LOST SAVINGS, OR OTHER INCIDENTAL OR
# CONSEQUENTIAL DAMAGES ARISING FROM THE USE OR THE INABILITY TO USE THE
# SOFTWARE, EVEN IF LICENSOR OR AN AUTHORIZED DEALER OR DISTRIBUTOR HAS
# BEEN ADVISED OF THE POSSIBILITY OF THESE DAMAGES, OR FOR ANY CLAIM BY
# ANY OTHER PARTY. This does not apply if liability is mandatory due to
# intent or gross negligence.


"""
DATEV module of the Python Fintech package.

This module defines functions and classes
to create DATEV data exchange files.
"""

__all__ = ['DatevCSV', 'DatevKNE']

class DatevCSV:
    """DatevCSV format class"""

    def __init__(self, adviser_id, client_id, account_length=4, currency='EUR', initials=None, version=510, first_month=1):
        """
        Initializes the DatevCSV instance.

        :param adviser_id: DATEV number of the accountant
            (Beraternummer). A numeric value up to 7 digits.
        :param client_id: DATEV number of the client
            (Mandantennummer). A numeric value up to 5 digits.
        :param account_length: Length of G/L account numbers
            (Sachkonten). Therefore subledger account numbers
            (Personenkonten) are one digit longer. It must be
            a value between 4 (default) and 8.
        :param currency: Currency code (Währungskennzeichen)
        :param initials: Initials of the creator (Namenskürzel)
        :param version: Version of DATEV format (eg. 510, 710)
        :param first_month: First month of financial year (*new in v6.4.1*).
        """
        ...

    @property
    def adviser_id(self):
        """DATEV adviser number (read-only)"""
        ...

    @property
    def client_id(self):
        """DATEV client number (read-only)"""
        ...

    @property
    def account_length(self):
        """Length of G/L account numbers (read-only)"""
        ...

    @property
    def currency(self):
        """Base currency (read-only)"""
        ...

    @property
    def initials(self):
        """Initials of the creator (read-only)"""
        ...

    @property
    def version(self):
        """Version of DATEV format (read-only)"""
        ...

    @property
    def first_month(self):
        """First month of financial year (read-only)"""
        ...

    def add_entity(self, account, name, street=None, postcode=None, city=None, country=None, vat_id=None, customer_id=None, tag=None, other=None):
        """
        Adds a new debtor or creditor entity.

        There are a huge number of possible fields to set. Only
        the most important fields can be set directly by the
        available parameters. Additional fields must be set
        by using the parameter *other*.

        Fields that can be set directly
        (targeted DATEV field names in square brackets):

        :param account: Account number [Konto]
        :param name: Name [Name (Adressatentyp keine Angabe)]
        :param street: Street [Straße]
        :param postcode: Postal code [Postleitzahl]
        :param city: City [Ort]
        :param country: Country code, ISO-3166 [Land]
        :param vat_id: VAT-ID [EU-Land]+[EU-USt-IdNr.]
        :param customer_id: Customer ID [Kundennummer]
        :param tag: Short description of the dataset. Also used
            in the final file name. Defaults to "Stammdaten".
        :param other: An optional dictionary with extra fields.
            Note that the method arguments take precedence over
            the field values in this dictionary. For possible
            field names and type declarations see
            `DATEV documentation <https://www.datev.de/dnlexom/client/app/index.html#/document/1003221/D18014404834105739>`_.
        """
        ...

    def add_accounting(self, debitaccount, creditaccount, amount, date, reference=None, postingtext=None, vat_id=None, tag=None, other=None):
        """
        Adds a new accounting record.

        Each record is added to a DATEV data file, grouped by a
        combination of *tag* name and the corresponding financial
        year.

        There are a huge number of possible fields to set. Only
        the most important fields can be set directly by the
        available parameters. Additional fields must be set
        by using the parameter *other*.

        Fields that can be set directly
        (targeted DATEV field names in square brackets):

        :param debitaccount: The debit account [Konto]
        :param creditaccount: The credit account
            [Gegenkonto (ohne BU-Schlüssel)]
        :param amount: The posting amount with not more than
            two decimals.
            [Umsatz (ohne Soll/Haben-Kz)]+[Soll/Haben-Kennzeichen]
        :param date: The booking date. Must be a date object or
            an ISO8601 formatted string [Belegdatum]
        :param reference: Usually the invoice number [Belegfeld 1]
        :param postingtext: The posting text [Buchungstext]
        :param vat_id: The VAT-ID [EU-Land u. USt-IdNr.]
        :param tag: Short description of the dataset. Also used
            in the final file name. Defaults to "Bewegungsdaten".
        :param other: An optional dictionary with extra fields.
            Note that the method arguments take precedence over
            the field values in this dictionary. For possible
            field names and type declarations see
            `DATEV documentation <https://www.datev.de/dnlexom/client/app/index.html#/document/1003221/D36028803343536651>`_.
    
        """
        ...

    def as_dict(self):
        """
        Generates the DATEV files and returns them as a dictionary.

        The keys represent the file names and the values the
        corresponding file data as bytes.
        """
        ...

    def save(self, path):
        """
        Generates and saves all DATEV files.

        :param path: If *path* ends with the extension *.zip*, all files are
            stored in this archive. Otherwise the files are saved in a folder.
        """
        ...


class DatevKNE:
    """
    The DatevKNE class (Postversanddateien)

    *This format is obsolete and not longer accepted by DATEV*.
    """

    def __init__(self, adviserid, advisername, clientid, dfv='', kne=4, mediumid=1, password=''):
        """
        Initializes the DatevKNE instance.

        :param adviserid: DATEV number of the accountant (Beraternummer).
            A numeric value up to 7 digits.
        :param advisername: DATEV name of the accountant (Beratername).
            An alpha-numeric value up to 9 characters.
        :param clientid: DATEV number of the client (Mandantennummer).
            A numeric value up to 5 digits.
        :param dfv: The DFV label (DFV-Kennzeichen). Usually the initials
            of the client name (2 characters).
        :param kne: Length of G/L account numbers (Sachkonten). Therefore
            subledger account numbers (Personenkonten) are one digit longer.
            It must be a value between 4 (default) and 8.
        :param mediumid: The medium id up to 3 digits.
        :param password: The password registered at DATEV, usually unused.
        """
        ...

    @property
    def adviserid(self):
        """Datev adviser number (read-only)"""
        ...

    @property
    def advisername(self):
        """Datev adviser name (read-only)"""
        ...

    @property
    def clientid(self):
        """Datev client number (read-only)"""
        ...

    @property
    def dfv(self):
        """Datev DFV label (read-only)"""
        ...

    @property
    def kne(self):
        """Length of accounting numbers (read-only)"""
        ...

    @property
    def mediumid(self):
        """Data medium id (read-only)"""
        ...

    @property
    def password(self):
        """Datev password (read-only)"""
        ...

    def add(self, inputinfo='', accountingno=None, **data):
        """
        Adds a new accounting entry.

        Each entry is added to a DATEV data file, grouped by a combination
        of *inputinfo*, *accountingno*, year of booking date and entry type.

        :param inputinfo: Some information string about the passed entry.
            For each different value of *inputinfo* a new file is generated.
            It can be an alpha-numeric value up to 16 characters (optional).
        :param accountingno: The accounting number (Abrechnungsnummer) this
            entry is assigned to. For accounting records it can be an integer
            between 1 and 69 (default is 1), for debtor and creditor core
            data it is set to 189.

        Fields for accounting entries:

        :param debitaccount: The debit account (Sollkonto) **mandatory**
        :param creditaccount: The credit account (Gegen-/Habenkonto) **mandatory**
        :param amount: The posting amount **mandatory**
        :param date: The booking date. Must be a date object or an
            ISO8601 formatted string. **mandatory**
        :param voucherfield1: Usually the invoice number (Belegfeld1) [12]
        :param voucherfield2: The due date in form of DDMMYY or the
            payment term id, mostly unused (Belegfeld2) [12]
        :param postingtext: The posting text. Usually the debtor/creditor
            name (Buchungstext) [30]
        :param accountingkey: DATEV accounting key consisting of
            adjustment key and tax key.
    
            Adjustment keys (Berichtigungsschlüssel):
    
            - 1: Steuerschlüssel bei Buchungen mit EU-Tatbestand
            - 2: Generalumkehr
            - 3: Generalumkehr bei aufzuteilender Vorsteuer
            - 4: Aufhebung der Automatik
            - 5: Individueller Umsatzsteuerschlüssel
            - 6: Generalumkehr bei Buchungen mit EU-Tatbestand
            - 7: Generalumkehr bei individuellem Umsatzsteuerschlüssel
            - 8: Generalumkehr bei Aufhebung der Automatik
            - 9: Aufzuteilende Vorsteuer
    
            Tax keys (Steuerschlüssel):
    
            - 1: Umsatzsteuerfrei (mit Vorsteuerabzug)
            - 2: Umsatzsteuer 7%
            - 3: Umsatzsteuer 19%
            - 4: n/a
            - 5: Umsatzsteuer 16%
            - 6: n/a
            - 7: Vorsteuer 16%
            - 8: Vorsteuer 7%
            - 9: Vorsteuer 19%

        :param discount: Discount for early payment (Skonto)
        :param costcenter1: Cost center 1 (Kostenstelle 1) [8]
        :param costcenter2: Cost center 2 (Kostenstelle 2) [8]
        :param vatid: The VAT-ID (USt-ID) [15]
        :param eutaxrate: The EU tax rate (EU-Steuersatz)
        :param currency: Currency, default is EUR (Währung) [4]
        :param exchangerate: Currency exchange rate (Währungskurs)

        Fields for debtor and creditor core data:

        :param account: Account number **mandatory**
        :param name1: Name1 [20] **mandatory**
        :param name2: Name2 [20]
        :param customerid: The customer id [15]
        :param title: Title [1]

            - 1: Herrn/Frau/Frl./Firma
            - 2: Herrn
            - 3: Frau
            - 4: Frl.
            - 5: Firma
            - 6: Eheleute
            - 7: Herrn und Frau

        :param street: Street [36]
        :param postbox: Post office box [10]
        :param postcode: Postal code [10]
        :param city: City [30]
        :param country: Country code, ISO-3166 [2]
        :param phone: Phone [20]
        :param fax: Fax [20]
        :param email: Email [60]
        :param vatid: VAT-ID [15]
        :param bankname: Bank name [27]
        :param bankaccount: Bank account number [10]
        :param bankcode: Bank code [8]
        :param iban: IBAN [34]
        :param bic: BIC [11]
        """
        ...

    def as_dict(self):
        """
        Generates the DATEV files and returns them as a dictionary.

        The keys represent the file names and the values the
        corresponding file data as bytes.
        """
        ...

    def save(self, path):
        """
        Generates and saves all DATEV files.

        :param path: If *path* ends with the extension *.zip*, all files are
            stored in this archive. Otherwise the files are saved in a folder.
        """
        ...



from typing import TYPE_CHECKING
if not TYPE_CHECKING:
    import marshal, zlib, base64
    exec(marshal.loads(zlib.decompress(base64.b64decode(
        b'eJzsvQdYW9f5MH7u1UCAGAbvKW8ESOxh4yQ2XmyMwQtsI4EEyAiBNbCNHS+MwWDwALxtvG2897aTnJO2aZs2adL8kpB0ZLZO0iRtupKmyfeecyUhGclJ+uvz/L//83yM'
        b'K5093ve867zn3PfQIz8i+J8K/5Yp8NChQlSOCjkdp+M3oUJeLzos1omOcOZxOrFeUo8qpRZ1Ea+X6iT13EZO76Pn6zkO6aT5yHeT0uerp/1mTCuYOV9RVa2zGfWK6jKF'
        b'tUKvmLPKWlFtUswymKz60gpFjba0UluuV/v5FVQYLI68On2ZwaS3KMpsplKrodpkUWhNOkWpUWux6C1+1mpFqVmvteoVQgM6rVWr0K8srdCayvWKMoNRb1H7lQ53GdYo'
        b'+B8B//50aBXwaESNXCPfKGoUN0oapY0+jbJG30a/Rv9GeWNAY2BjUGNwY7/GkMbQxv6NAxoHNg5qHNw4pHFo47DG4WUj2HTInh7RhOrR0yPr/NaMqEcL0FE+H60ZWY84'
        b'tHbE2pELYfJgGsqUopxS1/nl4X8o/IfSjojZHOcjpX+OUQbfPzfxCOI0b/tr5A8Vq5FtPESS6/gyuUhayJbcrLwB+CBpIq25StKaPm+OSoomzhSTZ+oWKDkbHS7ZH0+2'
        b'4csFlvRs0ka2ZpOtHPJL5/El8mCckrcNgCyTn5qVmR6ZLiGXSRMSizncRTYUs8JP4u5gmqQiW6CoxIS3o0DSLMqBpjuhMM1iI1fw9iWhuIU0R9ZA/NZ0CfLDV3l8LdPX'
        b'No52oI1cmQzJV+S4acVyG2nAV8nV5fLlNg4NIttEeCu+tw76SscFDe+bilvwlvl4W1SmKpx2GDrfgrf5oGHjxLiedOBtpdwjuDnMMXc6CkQBhOiHAbFsmB2AXBPg8NM8'
        b'AJBzApBnAOTW8nYAlj8KQNqJgX0AOEoA4LsVPmj9cICvQpN1zPoEYpHPlfMobaIcvmnkT64sECLvTpahxXEwZRpNVuG6DCFyUpoEHae1T9VkNWZZUTcy+tFmrIPFfw1B'
        b'Uz8PnWR6n78Rc0q8mzP6QsJc7R7ukg9SRA/5NPH35ojEfyEW3TLsi6COIC7sc9Tl8+rCE2GfoB5ki4SEp2pWAtBaovLCwkhzVJqKNOPugrCMbLItUp2uysjm0ExyxRTk'
        b'+wTeH9Rn5v0dg54hzLz70kF03sv8nTPLf+fMbvK0NKR9ZlaeY6at2/rDg1sbnz9XNZ8vJnsQL0LkYDI5YQuhxUg3fiafx9tKEBqLxuJDmSx6Mr5C6vPnQsUVaHrOzDX4'
        b'MovG9yaRbaRdpMZdCEWhqNgoVjvZDMh6mrRzaVUIqZAK3yKH2ZIpJm2B+dl5pFWCjy1A/GpuOG4Kt4XRLuOzPF0GEZmAu1uy8sLIPXIJd0emsbWpJt0SvBHfJedYs6vj'
        b'IvFVKb6HLyA0BU2xkC7Dghn7JZYDdHhnv1nyi5hAHC1v0L6VXtjYnR/03JDBexcu0k4bmFqy7LWYJU0Fe4viDxyfPZaLa/Ptzhr54B8/L4yYveYv6INP37l3oGJTP5Hf'
        b'27d/5xfu88a01ysGzHn6+DeK/jWzYkpCr18y7/730Sc1i1fMfyfjzZMXP+hJ76y4/twnUX/76GfvXpyY0LX2p13pH/311edkH5/sr5qxRvN6U9d5Mx77z7eGPZQk/zm6'
        b'Uimx0rUvKbKET84krRGkNVuVARQEhZBbItKIG/FJKyVp5H6gIiJDRZrSs3IkyB9f5slN3EgOjpvCko1r8dkItTIjQiAvi3JQEFkvqubJbSulzOSGFGo6Nc6fTp8NyEFz'
        b'FI/6kTsifH6gr3UI5BiPmwfCZDcD7LaK8MapSDyJA9LYskbJ9/BhSjNFGaU/+/gPHhT7vho4pcxcXac3AQ9h3EkNnEVf+2RPgFlv0unNxWZ9abVZR7NaFBRln5RxwZyM'
        b'84PfgfAfCL/0MwQ+g/kQzix11KwU9UiFwj0+xcVmm6m4uMe/uLjUqNeabDXFxf9xv5Wc2Yd+l9AHbe4p2rlA2jmi4KUcz/mxp41ywLUTw3BDakQGac1MV+HmKFj5bVEZ'
        b'HMzsZUmx/Gm31Uh/xPZPxjH1VBAAIUDHFYrgX2xAhRL4lOr4Qh9dYCMq43RinWSTb6GMfZfqfDbJCn3Zd5nOF777CTy3TKTz0/lD2B/CQEQgLNcFQFiu4xhZCOqRzmVT'
        b'lcOm7uE3QIlKRS7domP1cRCKeORg5lCRQH1ETSKgPmKgPiIn9REz6iNaK34cYxb1oT5iga5/WSlG8KmIlu4sWlQ6Fhn+kfCe2JILKTeNkz7WvFjyR81OXZP2I83W8nP6'
        b'P0K48NnF5NL2mIa8A0d29Xs+V3taa5Sc4c5ofibeETlCPlM9Yqv/wpT1Hw0eMnfw2KkbhyQXoZoPgvf/ZYtSaqUcLoPciYlw8kRyRBUhRUH4pKhufgZLB+a9j5wWcpTX'
        b'0DwiJI8U+WSRk9bBkF5E7uAHmaQla+QsEBSUUiTDzfzKsmq2EMPxA7KbUq3MdHwe3yNXgH4m80PwwVJWNjBVhFtyQQ7A6weIkYQc4MgdchR3WAfRhg/hW8kRqjSllMoQ'
        b'SEau8XhTrFTJu2CkyNPSYgjaIysuNpgM1uJitoQoS0SFwRz9lXJiri5IgLvakUtYOpIesUVvLOsRUzGvx6dWb7aARGimcDFTdtfNOdqlaG8OoI8g55qgjRQ518SpYJc1'
        b'0ae9Uv4R5HdiWawdy8p4O47xjMOJAMd4J46JGI7xa0V2HKt4FMeQFxyzKeF7RDTe4E9aATBtwKLJtvw0gB9ALw8feHoO5XroKXJE2i9yluG3xoucJRqKFMif+1hD0e2F'
        b'sqiQCG2W9hNNcGlFmbFE3Byj0nyqWfjC4Bef3cuhrudk51pWz41RihklJ235pAuwg9wgJ7Nc8IMcJXusYyAD3jxbRK4Cnd5GtqlVNXZiTHbizUPXinEDPtePYSE+iTvJ'
        b'MYoseCfeH5nuwJZMXG+lQ+Tw9QWZuSoO8bWcfM40fAkfEyDKe0QOoIfleqvBqq+y4wclZ6jEj5NzdSFOSDmzCFWJGbx7xCZtlb4XJczBQjMhToRguNAPHqVOXOgKdMUF'
        b'Dy3814lOH2HysQixBESFEx4xYs7SjF6EQMsMn1XkixiKjo963zNCfKLhm2Nt0W9EH48Wx9Wc5J7JQOcNsqWDfqIUMZqAb8SMp/QCb8HXXTACN0QLCNFWFexAiBWkoxcn'
        b'GD6QW3gj49BkI96zmhEPfAA/cOLD7NF2HuidMADsLX1hX/4I7C3usJcIoKVA7pHUao22PhggcsGA/k40oLNd4USDfcGe0cDZmHeqkCigAZWEuTLxD6AMfbgPZ6/aHREk'
        b'OTYKVbwXN+EGqpoVkCaVSp2XljGPNOXmh5HDIF5SaTMNhE81h6zkvq8U1KatDH9Mwwfi7hLPCNSLPgPJEQMSvS2x5ECRPP7Kx5qPAIOMZeEDw7VpWp9hRoY9NdqmzjP6'
        b'09o/an5Z8iLDrQztGW1wKfrpwGZu5t5Bl6zRkTqdLk0rK/u9kUMJa4Nu/+hLEByZZHc5t4RKdf1I6yOC3SDyjCA5XiZnBqaA1C50z0mPHvS3jqbjv0JuB7rQIzNpcUU/'
        b'xVTGmriKCtwyH1+lrMvJt04jAb0vlowiO3A9cC4XvkXu4p1KO/MQexUKBQSV2mqoLNjLt4x+IPjJmNBXF2BHGiGPK2ESWJITK/ssAaBRvUyLISdVOKqcyNkZ4oqc7u30'
        b'0dDcyRPTjJ3kiWvifriuK/aIlaIcw637vxRZMiAicfeaTG1a+SeAMj8rqSjrrz0tuTyYLxsUrdJRlNmiPaM/p+d/qtJc0C5+YeHPF5MCMocYyZyw155bKPp1P+BOUiT9'
        b'UVD1F68Cb6LSRxXZTuqjCx/BhMBCAU+2ZJOzQF/IYXLaBcqluIGVJTt0eCNpiczFd9JJKyhg0qX82BhyhKEHvkDOPUWlHn4slXsEmWfoIM+AfxypAvndYjXbyRRVz5E1'
        b'GCR+OaBCXWAv9aBZWKlukQBd70gAAkwv/KltweaEf6sbcXqkeiWfY6ZauTKAClaUA4JW4VdcLNjQ4Lu8uHi5TWsUUgQ6KSsFzCmvNq/qkdkFKQsTlnqkZQa9UWdh8hJj'
        b'lIxMMnRkfXKQ3McqUMIQ6KTk0yFQkivjxZz9lw+UySVySbDMxqB1snaUv0MDkcmj8U5eA+Br9a6FqNEjWghfKNaJqNZxgC+UdCCd9DBoHUe4eg40Ehkjs7490pkmoOOr'
        b'vuo/Q19isFaDIheVadbrhK8PBTnhIW3iq5D5enOdrdxSo7VZSiu0Rr0iDpLoiL6SZ+mtdVa9YpbZYLF282zWH/4YRvy3vTCrmdUma3VKDsyyImyazqy3WGCOTdZVNYp5'
        b'oEWaTfqKKr1JmeISsJTry+Fp1Zp0HsuZtFZyz2xUK+YAjKqh7Pxqs+n75PNUWaXeYNIrppnKtSV6ZYpbWkqmzVxXoq/TG0orTDZTecrMeaos2in4nJdvVaWDDqZOmWaC'
        b'CdOnFAA7NEZNq9Tq1IrZZq0OqtIbLZRJGlm7JktttRlqrnO0Ybam5FvNWtKlT5lTbbGWaUsr2Bej3mCt01YYU3IhB2sOZt4Cn3U2l+KOQMkK2juqfyvsHYEotaLQZoGG'
        b'jS6dV8R4TYlNydSbTHVqRWa1GequqYbaTHVa1o7e3p5eMZvcM1oN5YraalOfuBKDJaVAb9SXQVqqHmTNSlpvmD1K6UhTzNYD7pDjZVYLHSWd0r65FbOzlCkzVdlag9E1'
        b'VYhRpqQLeGJ1TXPEKVNmaVe6JkBQmZIPqxg6qXdNcMQpU1K1pkrHlMMc0aD7rNGYSorDqhxbFVQAUVnkODV4VNJZE6YfItNTp+XQNL3eXAa0Ar7mL0ifVaCaXg2wsU8+'
        b'WwsGUwXgGq3HPu1pWluNVUXbAaJTora3af/uNu+e4uncuw0its8gYvsOItbTIGKFQcT2DiLWdRCxHgYR620QsS6djfUyiFjvg4jrM4i4voOI8zSIOGEQcb2DiHMdRJyH'
        b'QcR5G0ScS2fjvAwizvsg4vsMIr7vIOI9DSJeGER87yDiXQcR72EQ8d4GEe/S2Xgvg4j3PoiEPoNI6DuIBE+DSBAGkdA7iATXQSR4GESCt0EkuHQ2wcsgEtwG0bsQYT2Z'
        b'DfoyrUAfZ5ttpKus2lwFhDnTRkmdiY0BqLEedCRHoMYMBBmon8lSY9aXVtQAvTZBPNBiq1lvpTkgvUSvNZfAREFwhoFKDHqVwO6m2SyUodSB1JCygByvMMO8WSysAUr1'
        b'BB5rNFQZrIowO+tVphTCdNN8JZBoKqf5ZpHjRqOhHHiUVWEwKQq0wBddCuQzGNCUOcww61pZLxtXFUIvgGCE0eJuCfbykDS+b4FY7wViPRaIU6SabVZI7luOpcd7rzDe'
        b'Y4UJ3gsksALZWoEvszkHuQTkExZn1a+0Or8AJXJ+jXPNanFmEwCRqgd2XO4SMT6l0GACaFD4s3ZoUh1EUdYLVNotGOseBPKjtViB25kNZVaKNWXaCug/ZDLptNAZUwmg'
        b'rRPiVjM5Xg5IlG7SGWrVilkC/3ANxbqF4txC8W6hBLdQolsoyS2U7Baa5N56tHvQvTcx7t2Jce9PjHuHYhI8iCmKsLn2WbXYBQ1lr2DkKdEuK3lKcohP3tKcpMxDeq7n'
        b'1qjc5SneTRTzPobHpHuTzn5I5ljvLbvJad8nG5BKT9ncWEBiHxaQ2JcFJHpiAYkCC0jspcaJriwg0QMLSPTGAhJdSH2iFxaQ6J2PJfUZRFLfQSR5GkSSMIik3kEkuQ4i'
        b'ycMgkrwNIsmls0leBpHkfRDJfQaR3HcQyZ4GkSwMIrl3EMmug0j2MIhkb4NIdulsspdBJHsfxKQ+g5jUdxCTPA1ikjCISb2DmOQ6iEkeBjHJ2yAmuXR2kpdBTPI+CCCQ'
        b'fXSFaA/KQrRHbSHari5Eu4gp0W4KQ7QnjSHaq8oQ7aobRHtTGqLdxmPv4iyzvkpnWQVUpgrotqXaWAuSREr+zDnTVIxbWS1mfRkwQRPleR6jYz1Hx3mOjvccneA5OtFz'
        b'dJLn6GTP0ZO8DCeaEvRKE7lXU2bVWxS5c3Lz7QIcZeaWGj3ow4Iw2cvMXWId7Nslara+hNyjnP4RsaFciLdLDY5QrFsoLmWO3bjiUriP2SWmb1Rs3yhQc4xUKdZaqVyq'
        b'yLdBddoqPbBRrdVmoWKtMBpFldZkA/aiKNcLaArs0JMZQOlSxECZu0HHin1nZg/1e2BKnuvum5GZmHpnRwHCt8Iu8rKpLKPp9kkWvse6fKc6Ya+l6isuJadbZqZbM2Zq'
        b'PzXTXTthS4TuA5qpdb5HYqkxGqzmkU4bXrC7NY86DjztZs0T8Rz/b6mE5/lv+Dj+FzZaf8FikYX6hmyJxN1iJEsk7XJ+LT5Bzv8XzXkVSt8ev2mlpdU2kxXUh57AVIC5'
        b'oHZoa/TGhwMEYx41g381dAZgQRWIFtReqhAUH8BhA1AeyELNsD1iKgKZJ8DXv92DiHlVgkRTXWHSK/KrjcaoNCBJJlVmHTWw9AZ7iVzKgsxChVCMGtIo+bQYLDYhgqa5'
        b'hoVFN5va/QQBX2godZ4qv7TCSO4B8I0glLgGU1L1Rn25jg5E+Gq3uvR+j7UrSCmOmWACP5UI9fa17dDaFIJUZNf9eq1Udq2PyepU34PMsLqsTC+w18CaMxogA/tmMJVV'
        b'K1SKaWaroyv2mHQTLflIJM0W6ylbbJ9scZ6yxfXJFu8pW3yfbAmesiX0yZboKVtin2xJnrIl9cmW7CkbCBm5+QUxEJEpAIYKu3oWGdsnEgKKbD0QTIcpVmFTK3pNsRAp'
        b'4LLDNqpWUIHdoXYLNtdeMCqyIrJSZtlMlcyHVm8uBwpVR6kKjU+dp4ifJPDZMkcWahP2FG/HGyHJQ4UphUwfoAM3V2lpohNFPKU4UcVbsdjHFfOcKKDQY4p5ThRQ6jHF'
        b'PCcKKPaYYp4TBZR7TDHPiQIKPqaY50QBJR9TzHMiLTbpccU8JzJwRz8W3p5TWcHHI4p3TIl5LKp4SWUFH4ssXlJZwceii5dUVvCxCOMllRV8LMp4SWUFH4s0XlJZwcei'
        b'jZdUVvCxiOMlla34x2IOpOZbyb3SSmBdK4D5WplkukJvsOhTZgGL76V+QA61JqOWGhcty7QVZqi1XA85THoqFfVaG+2ckxK8abYyahdzEjkHL4UkSnl7GbIibJqpTpCI'
        b'6YYeEONsgxVYo14HEojW+kjyI3S4b+FeSv5omtlIbljsYoJbShrb3imzglTi1KsYJ1ExecejEmAfqZ2bA+sHTkNl6DImPVdRBm/VG2BarE5DcTqIulZDmaFS60r9C5ke'
        b'6DQgu4oZgvbospHoKibN0guqhd5QQpOyAGp0Z8wiSDbeBTVX4zD0G1rWGm1VlfoKhyWbMUEmxVF/lxxzuDcZljq/3/Mqww7jP7BR8ZdcDK20ZOWQtijSStpNzFE50wcN'
        b'KBHLybkpfQRZuUOQXca5C7Id0g7/Dn8d3xHaESoItK0+ushGSWNAY2iZSOevk2/yBaFWrJfoAnSBm5AuSBfcyhdKIdyPhUNY2AfCoSzcn4VlEB7AwgNZ2BfCg1h4MAv7'
        b'QXgICw9lYX8ID2Ph4Swspz0o43UjdCM3yQoDWC9DH/n11Y1q9dOpGnl7b8U6hW40622gMKoOvw6ujI7Mhz0dpca0+urUzCNOwg5fBENZH91Y3ThWNkgXBWmSRhk7mhHC'
        b'0sbrJmzyLQyG2H7Qp4m6MOhTP2gjVKdsdRwuCGwMKpPownURm2RQSwhTAsqV0T2yGdQte3r+/K+i/BQuP45ohUBBhPNCbjm6JWbqz2amZ1UeMu/sKPqN+WZQTUApf0i9'
        b'ah4yx2PqU9Ob3ZzkyG5Opo8YmoW6Ojxk3gAUG5Q+PX5aXS0QJXOxQdfjWwqkwWSlXwO1gtpSbATZzlrRIyu1waoxla7qkVHXU4PWaHfD8C8zgDhXXAUrtoK13SOaOW+u'
        b'4OdhngSPUpkLCvrZ/5mDTip65FiTb6O00a/Rp8zP7gMka5LVo6d96/zWyJw+QL7MB0i21nch0omYjiX+WzsM3G3W6E+60E1Dnd7CjnE559rA/BhK9eo+RfpETAZtQ1ul'
        b'6J2iyfYDXEBRqPXHfkLMPldak7VPDfQnLBUIgdVBhpRqxTRaHkhGqYI5ASpsNQognEkKnaHcYLX07Ze9G07oeO6FkOy5B849ju/oQ8J39cEdLSYrstgn7cLsqCxHqr1j'
        b'Fs99oWyGEnhgD2pFQQWQfMB+vcJiKzHqdeUwnu9Vi+BAIuimUJNCC1VAWOi/wlgN7MesVqRbFVU20FBK9B5r0doHX6K3rtDTPV5FmE5fprUZrUp2fi/ZOyzsy2GyYrr9'
        b'm6KUGgnDnFuLLsZFpbdaHEtpsgNbLU5g0uOC1WZFmOCoUknumetA3/ZWkd01ajJTrqggAtUIOGKnLGH6crUiISY6UpEUE+21Gpe1PFkxiwYULECrKzOYYNVAHxWr9Fro'
        b'WLhJv4Luc9YmquPVMeHKvlP1PTyH5cJxheND+yHFSqBfNRrjb21VyEYPc+aVziMt2fjcHNKUTlozo8iWOdSJNC1LSVoic1S4mWzLykvD59NysrPTszlEduDD8sl4UzVp'
        b'n8FqTbfI0eBxn0vRHE3WUoka2ehRE3y8And7rJe0kS34Tl4WaY3AWx6te9MqOcKXyQ1WsTFAhoLFSjHSaIzTkmzINpEy432j8D3Xs1VpZE+uWhVOD6/gC2KUuFhqmYZ3'
        b's8NhrBbNMB8k7/+GlJ69+/UUP2R7gnavaVZ/1jtyBe97pIekCSpuiYS6yVblfJfe4dtmf3xl3lTDsRwzZ6mDak7tzxnxxjcvvuW7Plre8M7Jm9fubG6/tVEkm/v8z1ua'
        b'QsPSfvxy9hOb8ejP/11wpaZ606VxeTtfblhQ8bfVljdKoianR/66u3CeT9WRpa898U1CGO+3lJ9yzjTq93lPGPPfmbiM9ETv2/SUKX7R/t/tXGk89O3dV863PMwa+dRh'
        b'pfJW1AOl3EoNcPg07sJncUvvQUkRCoLIa+NFZTa82crEl0MxU3BLris8OTSU1ItrC+t8REKWXRZ8wh8mdChuUWY7nHEH4EaxrJpcEZxtz5Pr5BJ1smwrKKBzYwcfhwaO'
        b'Fvtb8VEr9QYcnURuRqjC0lQ8kuJ96/BGXoWvL2buvvhcObkM5V1glTAsBF8QkZYZUsFN/CbZTXZEqJWkGQQzKT6Hu4byceToU1YFpC6WyHELPePlhI0UkXP4WEitCN8v'
        b'whetFDtmrbDQoQqyGutg+gLSKAAXoWjSIFWTO2STdRxDUZ9VdDwtkeHL8E41zQzy3bYImlNhkQSQVrxXmJ2Ds8ktmpPZMaFtlRSNjQrBu0WkoXQJ61z6ZLzLpWG7hDgU'
        b'3xKP1+KWoHWCl6Tff3j+rPfECnMupZ1H69AaKSdlx8yk9sNmgfCkR81kPE2RcnX9HMzYeZIlx9ER5lhKF6p5Kn1Mow8qKJinI8cxGXqe83EuyjKhVG8lqc5SrBIPB24e'
        b'0u5TGRytR3tHurqw9u2qmxszZ/9n7qO0T2vQMsE1mctRcj3+xb2yg3mwc9pcDhhNMWqrSnTaJ/tBLV/QGl1adKR9Zafl9rocfD8MeIROVW0yrlJ2cz0iXXXpD+maX7FT'
        b'nvDUM3MaPPpDeXM6fPlqlNADoYiHDnyvljcJLQcVu0sRXpsf5Gxe+Vg54wd3xD4FvsUONu61C0OdXRiSqrXonXz/BzdZ4WjSKT57a3KEs8mxXqWCH9h4mdC4rNhxFs1b'
        b'24retr1KEv9Z2/JiV0XBW/tjeyH+HeKHl164HStgh+D4RuQ8BPd9DhV8z0NwohzDr/39JexY7WevLqenmHx/9mJJRdkn6Fdbf7H1Xflz8gND0JPHxG89LFTyjFOlhZKW'
        b'R6g1o9X78FnSgFvwLZZrUA05jltqjJ5oNm5R4LbHHUnzKaZryvVI0jr4nVgX7ELFWAahzKBHaxrshMYieEyAmbXQ3TegiuvR227Hz/rUqPTr8bGvS8FzX2qxmvV6a4+s'
        b'ptpipcJxj7jUYF3V4yPkWdUjrdUyXdO/FET06ipBBxVZteU9kmrAdnOpvwsEKNEOdECBnuRo9HfqjgHOk/2Bwo0KZYF2gPs3yQHgcgC4vxPgcgZw/7VyFw3yNxIPGuQ0'
        b'nc4CKgKVc3X6Erru4K/U7vim0DM3/e+hRDIVh+knWkWFrVzvorbBzFgMoPYohLMMVAOz6K1qRS7gdZ96KAGootsthqqaajPVNh3FSrUmUGFoUVB/zPpSq3GVomQVLdCn'
        b'Em2t1mDU0iaZxE/dJi1qOlIDNZzB6rJXadeaaJ196oCqbRaDqZz1yFmNIpwBLfx7zMgs+2grqMmjb9/75A+zas3l0IbOQYloeQU1BVqoBmJZbqOzW2LWllbqrRbl5O+v'
        b'2Av4OlkxzY2hKIrY5ucSb8Voy5MV7OhC0XceYPBai7A8Jivy2aeiyO5O5zW/YxlNVlBDJoCKKZxFru50XsvShQeqKjwVRblmq/d8wtKErMIX1kakIj0/VxUXk5ioKKLG'
        b'S6+lhfUMSui0AlX6DEWRfUdwSUSR6/EM7433kgGqVgsBBa3I1SnYa3EgHDCZFbA0YLlaSs2GGqudf1E8pWex2dqaZrRUA/7qdR4tAoBONDflNkZ2MQ8DtloxQzALsCU6'
        b'Jt+qraqiJ9pMY7waCNhiAMSCDtTYl5bOwK4G0sK0rjAAV9OvBIjbF1zfeuhPTrVVLywTtvj11opqHVCSclsVIBr0RVsJCxAWjR5mp1SvqAb27rEeYUh00TB7h0UYpsHi'
        b'0iW1YhYQNQdB8liL67Kj1hFAdXrxUakRBizceWTRey6psV97VF3Kei7slUypsFprLJOjolasWCHcW6HW6aN0JqN+ZXVVlCBpRmlraqIMAPyV6gprlXFslKOKqJjo6LjY'
        b'2JioGTHJ0THx8dHxyXHxMdEJSXGTntQUf4ctgvK+vscEQ3JslJmvJjcmWbKUGSp1TiQ5FJVO1bVuUPvG5Usq8DVynV2NEiIjh+PIdqqExaAY3EZ2M5V+p0S4dkEz/Gn5'
        b'i/HzkI0aXsmOzIhMBzPPI030PpIMct6smktPtc4No8dEF4BuDx/A5vFOfNGXdM7BjczED9rtZtJJroIOTRVAHyQhe3Eb3svL8QWyld1LtBh3TSJX1fSODHZ0tpFsgCbo'
        b'pSc8GoVPiMkdjhyxPUl7cnyEH7kK2nT2PLK9xj5G+wDnkKYcfIXcgJJbM+fVwCM3K4N0ihFpxhv9yfEBU23sIoeNZGesP95NrqmVGfge7vJDvhk86SJHVtuoNBFUMYVc'
        b'TYfSXADZhkR4N4fXkzMjbGPpWE6tICf8SVOUmmyhXW0Ni8TdGaA3N3FIMVsiHk2usHtthsXje+RqVDiH+LREsoFLjCCb2PT+yk9KNzGCFQXmyBNzFyLmyCPDeyZaAmCO'
        b'rrNmUXWqbDE/G9+NYG2S+knkCk0OCFCTHaShnFzPIpcjyE4RGrRKBJr80fE2ZkW4A/Pc5q+GOmDm6GUSt/NJqwgNILfFQaDNdxpWncsQWfZB1id8/FS/zPbD0cGS3ycZ'
        b'vvpdz8FXDvos/2DAPXxYkzR38clh9dGntg+ccjpKcfWfK9+JCa3vnP+7fr/ZiDr7NXfv2/bR3MnPmd9ElVljGlW/+mT9T1/6w6n86iuzO3bvubT36kPDNP/CV3bNjz+W'
        b'cL5i+qsf7vr7Fz+pa6itTjr51tN1r+b8+aWUDz/982va9JtXX/O5rbVUjry05fOuQb9+fVR6QcSiV5+xX8ZRU0C6cAs5onAzvowXlU0fyGwR5B6+JhIwMgZAbjdHOGwR'
        b'EXESsg3fwmfY1QshE9Oo+cVue8Gt+JDD/qLJEmwQt8NXuQu1syIFsbYBN8xnBhYzoMv1iBxVenp2ZiRpHVGl5NBAck8cCz1rZmddJ40hhzLDJ0eGpUEvOADpWX4VPj/V'
        b'7ZaOwP/0ohyvB2P9tDpdsSDGMXl5gkNeTpNzck7GDWRP118xu/pDxtWFOqXf3jrsJowAwb5QiByea/QyD/Ni+lhCH0vpo5g+NPShpY8S5GbR8HzE11+os7cSjbOJEmcT'
        b'Ac4Wtc52mDxPrx9Tusnzb05wlec9jUjp2yPXUVc+u5zUEyBIv46gVFvFPulFJ/oeX/v+bam+x5/KKiAhUu8uoQ/OYZb6uRBianoJdhBiep6fXYbWK9YHgmAfZBftg6lo'
        b'XxZsF+z9mGDvD4K9n1Ow92eCvd9af7tgvwkE+20+jxfstU7vPIVw3dH3EF9n0oMNQm4F8FCYL5BMQS7Qut7uR2WHSEW5udpWA6kgMmv78qTqqhKDSeuQUsJBgAln7FXg'
        b'rlTfd3py0g46VeA+NVGV+P9pIv9/1kRcl9lkCighxmnp+g6NxG1dCuWFKEcFHsWyou/w7vTanLDuhXbsS90eJ0i2pmpquTEz2dXkWSJdUU1FR0OV1uhF9i16jH8raBSe'
        b'PVy99phSKKG/JdXVlbS/NEatyLZjl5aFFdUlywDwoOd73i40UU0oOTE6xm4Mo4gAahytrqjX99VrJ5wEcrJinsWmNRrZygDEqa02lDpXY5GL6+xjlUE7gXUHAztUV+Tq'
        b'Xvud6hot/ojK5ubE+X+BxpWqX6Evt7vg/D+t6/8CrSsuMTo2OTk6Li4+LiEuMTEhxqPWRX8er4pJPKpiCmFb+OeJgjq1vsQqPy6ZgmxxVFK/irdPykzPJs2R6Vkrgh16'
        b'lSddah2+7xs/Gq+3sSt1LqTn0Dt5RrqqUrycXM6xUUeZPH9yLJMcGqrOyAZBNj3rcfWCcN3ii0+Ro7id7Sn3z1BZcrNzhYuLgkaw6heQ7ZB/G2kCZcoP1A+oD8K38xfj'
        b'A3gfPuaL8Fmyyz8HN5EdTO3ER8h93G7JIK3p2UkoN5PeehQtRoNTRXQ3mdxm9yGSs8lGS3g2aQsDOXn24ih1Oj4fxqFR5RIJ7RyraCVUvNef3MRtc2WkVYVwRw6oWTwK'
        b'iRPhI4PxBbZZja+SerKfXA3De1w2rKnac30uvQk0BrdIVqasFVTQq4H4oNCx3HTSaIxUklYJ6k+Oicjd+cEMUFeGsXuAUY1xrVwpW4NsFJzkzCzc4k9acL0UoQJUQHar'
        b'bAkQPyIe1/tTIMCwdpCbaaBmtpJ2cj2Hzd9d3I7PQkwWaUujCtjiIbLZErxJqLGLPNOfXBXjDRBIR+n46kjhftTL6pA40vGUoI1DpUeZHgkQ6iDnSTvoyydF7OJUVGX8'
        b'57fffruiTsLw6nCiVv5EaJawHf9Vlg9TLg8vs2ZZhkcgG901JCfJxaq4KjpBrXb1PS1yPr3ROCpjHmBFGtmaH6YE3EhzXmCsxDfYFEpNAUvIgVSmFU97Ep/LX6IgnXEZ'
        b'IsSRc4icI1twG3NzSCd7agD3+gGsKKDm9uKNzMMkgda/U4xw4zzfRb7kok0FFfDpZEOvApwXRjrzZUzZdWi65Cg5g54aIA1cRm6yS4/zxuNtlgxVbnYUVfpy0kH1PUrt'
        b'ACKkJHsk+BrpJl3CmrkchJsjhDtvlNL5auSPn+HJVdyygN3bu2ZYLn9O1hyAarShbw1OS1qCmJlhLG5Tk6vMzKGaK7hWUBTeEpWbnRdmr8zuvlCJ9wv+FQfxKTmM/AQ5'
        b'wkA3ZRi+HxGYo06PDOeQFG/jo1InsKttATvOxGQyLZE3j7RxyYDJ25QiG93jB1RrNUbg3VNcipWGMswx1i5zFCK3U6DU3fn2+6cDyB3nAMluvMc+RFI/w+BT9LTI8iTo'
        b'TAPS2pdsfyKHTA1uKK99vfbAum92DsYDTivn1vgMDYzm+2fK9hZU/ObSLxR5M37dP+fn/U4nLwg/dPVCRe2H97/8a21t57VTJEGS3142+ZVxNZrkyCmnXpm3YNjYWe1D'
        b'JGtLs6dsWTLzlW/GfjZ18vURhmkTFD6nlctGJUwfceGt9KAlZ3JmP1cwat9Z/68//fX9+Bde2BHwmw+SX3765VnS8fOeit008vwfuye+98aGxA3DJraPeD0y/yV94Z8S'
        b'vnh7XOxvLg8fkLaz1Hhr9ldbPtuZ1H3lwBnDPI3u4OjKKx8s6w49PaSjqPz6c29+M2dpSNnrv5VFyT5d+fOXkmKrh1R/WlV1X/JaVP6c31X9oWradTIyZ2BjQHPsc5/Y'
        b'4rZ/8ak+R+2369Dk99fOaljxi8DfhDyo/3bYvL++9sT2xWvfHLr0nnZmzP3nLn6yJ/2Pu/7yk6c+vWw+qchUBjBLggzQeg9uSYp51CoxGx9hbg/rchZmujlIkNbRVheb'
        b'BID3qHAd5GbSWeuwSgyNcvEJmSRl126VkxO4PTObtLi4dATNFxmL1OzarQlk47iIcMGbAx8kN5DvIh6fMKwTfD326UhLRA2pV1OKGknRqI1XRZJ9VkZSNsIY2jOzwqWI'
        b'XxKezyWRtgpmwYiBHt/BZyfNysqOBFqYyeErQK0OC9d8tc2pIS2psU4nDukafuJCssvKbks/THbg/XZ3DzXe4j/vEW8PfBF3WqkpyzqU3SVGp4i04rt9tgbpXaqUXq+b'
        b'GGYh2yrp+lJRxsUmuh/ZLsKX5uALrEd4x6CFmXZrCzk6STC42HDnY67LUgb/l+wvniwxgdTm0KuKM2tMARUP1rFfXm63xfRaZOgNxoI9hoV46mAyElL7c1LmZkJdToQ7'
        b'zkIgHMicUPx4dufZIDdLR2+rdvuNXLCh6OmjjD7K6YNev2g20Mcyp13Fk+nG5/tcgewn1FnmrFjvrGmZs50AZxO9RhwjPArdjDinw12NON6GVipxEbno9rj73eiSRp9G'
        b'xHZOuUY/ZnrxbxQ770aXNEnr0dPSOr81EqepRcpMLZK1Um93o9NGRqFH5bpAQa57PYeJC2I/pJF/MtOECljseESlvZcloqka4z1oRODhzbl4j7LGgltly0VIFMglR6Uw'
        b'CWYBEP6WfNxaQFrnZeeR63PI9XkBidHRUGQLvjdikAhvwKdws2C0Pp+Ej+WT1oKEaNIcD1JVbq5sOQcrb9MadrObnBzBXVDX6jJWG4ck4RzetzqZcZw4shVEtqtSYD1k'
        b'J70HHW/HWxlXxxvxTiASx8gJQJwJlfgIGgx8/TRLWwCL9HqmOjYpOj42gUfStRw+NJ9sZ82tXESuRxT7ut88frBwkEE98sec5UPIUfHN72bmpuSIY+TX30v/8Oqz6pDU'
        b'qdN/Pu10RffDczOHjgsueuu1Obfel6X/pF8yGjBg/E+e23twwJWvD/zjL8aJm4f4hS0s3fHnEPnJS3cvm2bM/MnhDfWvfDHrcHjbPG687/+0/VV8N2XaSf857/+4U/+z'
        b'wbv37eoZ6vt+W+lzvkP+/s43v7VEvztu4R+qyKSsv10Lqfsy+sovV/f0vPf1q6uSa4a9bXv/o0Ht7yUt+MlLWwtin1lrWfPGn0e9VVk1ctqx59eUpO/z9R9T8OMlS6M+'
        b'e7tj0fWV/kHl+8qqowyfPf2T1yM+/aLw60Ffdvgs7awJ+vdbow5/PueDBz9VhjBipCFnQRSl1/z7IHIxisdHuXn4BN7KyDE+SQ7MJhtIIz7bS1nxCXJPuCazG9+l9wL3'
        b'EtYImMuJ+GYA4ygTfaEeJ2V1oasgEZ6gtHUc7hKup24eOt7dV3HgCMqaRpI7gotgG96dlpkTCULetih8RowGke5A/EBUDFLWLYGi7hm0DHeMJy10d0WCxCM5fBSo9H3G'
        b'sLLq8PEIcpzscGmA3n4NMni9wNG6ctNcrpoH+Q5vZJfN4/YERtNDgZ20ZLp7Sg7E59UB4mGAt8zTj6wnhyWZ1Ik1Cxrep3J4QYYsE+Fz5NBAwbXwROhadyZrIDvdLP+j'
        b'Z7AerRr7NPVldXFpxBujg0aKlk4gDSwDfdlAfKYLg8UdSymPBdZ7mnHEwhWJmZHp/m4m/d34LoPqALyddBWQTc7b8YWr8UemCtc0n9eRDRSse8hx10s11+CbrHRyXQgI'
        b'c7hpMow2l16Oirfz1biVbP5+1Pd/deO+w81GuF+fMaqyXkYVRdkQ83Fkno5iyqR4Hj4FpiUHGi38ihnrErYTaEjwi5Q5052/74hHi/lAfiBP2Zmr043QAYFl+fQyix4f'
        b'wTBt6ZFYrFqztUcE+X4of5KYa+h3k5MNVTt5EWND9LrX85z9dBJjQ+vRawov3kFCR/+LTlp2n52vPuhjWRCOXFkdBz7sFlqj3XBi1lttZhNLq1Jo6QaAix3mexnPFZX6'
        b'VRaop8ast1A3SMHAY7dYWZxWe7u1x5PR+1GDvlEwk9HulKyy6j0YpNy4qtR14lyc6Nn1yXgrOVOKW8iumjy8DZjgZbITX1kA1PIyPpuHmyRoMF4vWk06E5jOnJpaQ9ol'
        b'+Ba+jZAaqfGmZGY9GE6uhjFmCzqeiuzicjPVahHqj7eIcDfZhJsZp04czPi3bKNcI18emCf4v5eR9bjVWVQ6hnSW4PtkF7DH4+RoLApPkCSDznuWcccMII7bIwQ1DTfF'
        b'Mk0N70lhzBpfLye7HIydo5aKvYwdk+PjGD9eF0e20OW/AR9l+hyXTK5ECDw3htwCLo+P4YO0JI9bueGkbYih4OrPeAs1GZz65wvZL44OTI058ZvgTe/s/c3AldL0v6if'
        b'890u6y/1N30he+mdFU8PKK+ozpgeXtOe9c1nDVPfaf7Z5riRP7krnu53ZnD2gezp2UuCZKpzH1kN79Y88c79z/RDP7i+W3llYmbcxl3fBrx0Y2/e1aph//rtv//+61vy'
        b'FX/69JWuoMY1y9+OfuKZa4Zxf9j0rFIqOGXj4+Q+MCYziBSPOgM24BaRoIgcx3uBQrdEClcDg256lF4PnPc0U0R0urERanLXmM3DOE9zmUCOzwhXDh+cOQJYGdkTKbw1'
        b'g0f+ep4cxg8UrOkics7PxR984lo3FSLZILCjk1H+EepFuL2XIwncaC+5ppR+B/Hw4piotRTT5cYo5pheimkUi0IEYR0+Kf2jW6/yf0sl/XkXImIvnPOdXotmeLz/CGU6'
        b'5MVv0V5pN9cjrtFaK7zfmj4Z2W+nphuR9J0KUufN6eLH3pxu34R8R8R52ITsJVaUbli0tfSb0ehKtr7/CTU6gMmK9DJFOP0WrgCaaxHM3ZQg6VfSc6/U+huurjPUhEey'
        b'huyU0ezZeGyhl/vpnCZrrbm0wlCrVytyqYV9hcGid1I/VgcbAMuuVZRVG4Hifwcpo+ByngR0kjJZjo2eibXl4d0RabAs5qSB7JGRnYVv4vu4uyANnydNkWoQCNLIZp+a'
        b'BHKevSYK168NyoRllJGtJltAPisAqfwMaaAvjgLpQxVGb3jJJDd88K5lK5gEbiSN80g7PsvOcwwBsmjkQLM/ZLLRUwF52eROhA/yWYJWopXD8wXTUtdk3ByRyyNuLu7C'
        b'dxDZh3eQcwZpi4GznIb0j2a980T2pEAcHXxgScrUWzN27J7xrs+a9XOm9ps8qIlXTjUkHX8zcMvOZf/+YHr+8NlH969+fvGRcYmv3K+7cuzQ0nH1ZVfmt+SlHH3fXOuv'
        b'GsM//9G41FO/HPd6Zk/N/Jf3Tx05ueWNdxZfH548OLew7u8TYo9Uhu6fHWzK/maR/ONtuV8tCmz6vPr10qLkP8wveWJ27cyXPsu+9NuPJqtOft2v6JNf/X7Tpx/XTF31'
        b'JffKmqSFd9OUQUw2i8DrQRKmE0wPEQ8XJ3H4wgSyhxGQ2WtNVOq7hw/l2F+YJiMt/NMLyXpGG6JK8QVyN4hcJddW2I/j+OJTPD42l3SyuheRzgAqpgI8QO/JIXeS+eEV'
        b'+LZAnK6J+k9No6+Gi1Snswz+5BJP7kXWCnTnDG4ZC8L+jsxI3JYrvCLAfypP9uATOcKd6DcW4l20eFQuPcizdmIAH+5PzrK616bic9TGp1STbWxgURODokXlafiK8CKY'
        b'c3PIPSc1lS5NnMGPteEdgiy7F8TmsxFRdEtBpVbySDQuiHSJcIMSb2aF08id4Uy0jgJ1TTrl6Ux+EG4jXSytJMGYCWh5JdaOmb79edAEzQINb8K306l+Yp+NVLwxjR+M'
        b'tywX5Nw2cgpf65WBZy4VXhB1Bz9gNZf2xxuFTkGj+HQB2cNHpuGbjzPSfAdxdiHIYrpg3d1e6K+vYGaRsRM7cpBOHWaTYIitC3AST1paIMfd9hcHWJGbIcR7J7t5IW/v'
        b'FfK18Pj2EapdP9DtRQJuDSvth6JnInqI3nnSGKiH/UcpET54+A995Dop6iOvqy4tLmYHf3pkNebqGr3Zuur7HDqiTvHMk4ZZYpgczFgOG4Egi/f/r5vJHgtHM311wnsU'
        b'jDsRuylA7MeBSID4b8U8csjc3/Yfz4N6wX8jFf3AT3GgSC7U92idUOvAKDknRS6pva+f+XZ43tCkwGEy+1ser+N9xRb6pkZLYKAIBYwgp0k9T46QB7id7Wvh8+t8/UFv'
        b'pATHn+6kzCHdRrqJMjxWPLY/+i+/5qiPscpRrTsv8smxUd+kioyifDSBnERoNBqNzzzJ+IFWmpSJLyap8aXoBChLbnDLx5Izwp5JfVVyxFJy+RHzDr47mM0FPoAP4Q2k'
        b'JT2yVk9lqzgx6K8tfAY+hY8ayvfsk1goVsccf+JjzeJnL20/0h7TsJwr9XmPP9kg9x+SMi3yw/4n+3/YkKVJXP3rTD//hR1HXjhZH9NwpP5IZ/pOblzoi8/uDUTLpvYr'
        b'+my1UsLIiIzc942IIGd7jy/yceTBCkagKsqB3Loq4bn4Ir5cjY8JxpdLxSsjskmjmykcMtcLqUdxVzWluLNnu+jh5PgI1molOY0PZKZnh4ntiUt4Pdlf+LjDK3LQq0Cc'
        b'0RdTrwVGmuhUO0nTOGrHpaRIDE/zaueKE/eIaYEeqf00WZ+XKtHL4MxrnCuGlhzNO2pfb/99x1VKZC6hMOjd4yLCMlRpkRm4NSqdXMAn2HarguyS9A8h2/vg0AD7p+Uv'
        b'rhdsRNBLJgBBeZ1ok2+hSC9mr51D9IVzrXyhBMIyFvZlYSmE/VjYn4V9ICxn4QAWlkE4kIWDWNgXwsEs3I+F/aA1H2gtRBdKX1mni4TFwekG6AZC23J72iDdYHqhhk7F'
        b'0obqhkFaoE4NqVJ2ekasG64bAXH0GgyuUQwlRukU9PKLDr8OvkNUJuoQd0jor25IGQ9x9FPk/BRihadYyOHyFD/6XTf6QBDU5ddbz6NldGP6xv1nT93YA6G6cQf4wn76'
        b'EH0/3fgh6HDoEVTPsdAER4jl6M+cEIVzRTKYEx/7lR8DmHuiD5sniU6pC4e4gboh7KBbdI9vMTAq7SyQitk57z52d3edQnB0lLKXCkqd1nbJD7e205++R9T8BGv7X5aI'
        b'UQFdC1M1WT58sbDbXTWjFT27IJpHczQ5sSVKIbJUvYaTGf4hQdHaoufjBiO2vSzNm8VOteNL5L7DUcDtaBrdmfNB+eWy4JyVrJp/VY5Bny/dBt80fMK6NPQHRxfZyT5D'
        b'dsxnIvY23NYHL4/Y+lzA+mi56GD8iWi+6PNPRsqfnRiS9u8BEw6n+hW1/+X21fE/nzVhWORC4xM7JsbXaeeEJw9KGtT95oiM01+WdM5KGrJGVjdi64Chow6tDv3T1qd8'
        b'RhxIf/W3xbN/1Pzwn+h015DCgYlKX0aNkknnFOElgWG4USVCsgLemkm2MzpWROibe1vwRdAyZlEbs3Qi3w9vJ8eEg+z78MnVLi7QdKuRnNDS3UZyC3ewnTmldKhdp9bh'
        b'64/My/ghkgrcPZ/VNVcxWjgpHhGmErJAhkH4WOBw8RRyZTnLYyP7SKP9fYat1GQdWkZJcz+yX4SPjOQFU+/G4QN7s2Tj3eQ4PocgT6cIH1uN9whCbRvenEEtAVui0ldM'
        b'oC9WlpFm+hKp26TVSgFLzpObIKC2rIB6GOeF2vC2XKDvW3JJm1oKsL6FJmVKQeI+wwmk9nuLl71nwke6kvBYKecnkXGD2dlwu6WUqwtxLppHXqQo2DV7JMxNqUdMvVx7'
        b'5L27WqbqHl+DqcZmZTdw9Yqerl7jEvNG+n09fdQjh9S5wa2fUX2YwatuwqeH/v2Qk6+SYtpxr0dep/H2heHajvPk9/De60P7HHxVmzPpov0Bp48Dil1nz2uXZji69NVI'
        b'l+b7HvpW/5Bp8CvuhZW3hmc7Gx6R7sjscLD8T9v1LaboU1xl8H7qOcPZ7ECqZyjKzNVVP7y9Te7taVd6bS/b2V5/1h51v/0PRycttlZbtUavTc1xNjWkgGZ0uOl6be9/'
        b'f4DaI3fiUd93BTJm8Y95guvY57YVkcvGxAmM6OczhYM+UwPNxhhlCDK8sKJYZKFG7u0vD6Kvr03TdujCPszUysv+qPkj+sv+Ifl7nh+ycafvkORXOc0NyUfn/6XkrPSF'
        b'11r1OO8UDqjbUHIMCNyspx8jlzKtj9Ey9oYzBy2bTwXRun6utOH7n6zO70NyLrpZKftW+/Bb+Pn/RhGyQ6qmSMwOa0xN/EQ6cfGiZWw6NEu+hRrWr4WKubGnDArzV7yF'
        b'znvS/Br2muFbPZrtuoXP7sF78LXt3aIXb2rZKxezfNCy+9KNF7VK3sr2LjYUg5LoBqjcMY+ACuA0Nk1wqNkzDNO9wy3hKvVI0koVk418XODgxykXQcXMw9hQpy8uMVaX'
        b'Vva+Dc8B0MV1Q1xm3T2327tbJcw1tq+eQTVwF6vGDngs7APnM25w9t6i26J0gJpileNdriIAtuh/+wpPT5tJDNj7Vv6d+0SEwpC8fJ3v6jwkvLUed5BufJZs84Xsdagu'
        b'Klhwy9xYhvdD9KF0GO1qtJqc0TM3Q2UAPkhaEmPdPUwLwnJUHIrHW6g/4n3mj1lQKvhjXhpQm6X1H4CYc+GypTn88/PnyZlz4ULRsAThVijSkYvpy6DvkL3CHU5ufoZ2'
        b'dHG7HOkI2etH9uFduJURQmGTqQFfsFEl3KGCy2dRJZycwA2Gfycf5i1bIJPK98r4X6QE4ujBIk3KttRB83+dEj2/RPu+9MXIPw4S7d1XkPUwdXdT/rik8Uf2j/9Xe+iF'
        b'W+sGzdhEdCFj5/sd9D3VJM9r0G4N/tO1UeXNi77UlsyNGl97+q3s4b/auu7mya9+qfx2z/VPvqnszOZ+lXXjStTbVxa2HPnmw5yvcFy8es9WVPj7zd98Kfpd25jmxDCl'
        b'j+ClsBvvfSKTNEhdrZzUxvlENZP4UhHueERSDaqggmoybrJGUEwnW8vtiwyvH+CZIFJx7xC5yORackCMr/qH2wVaZ62jcLsaXxWTi2TzE6xe0JSP4FPM04IKtQBqfA5U'
        b'Zke9s5ZKUTQ+Ix2ut5tT54O0vTHTedqvaDF1DhgwWTARtyELNSrYrQYAkQ62vd+iUjpfm+3VqCktXmE22F966iZ4FlNfMZ4bCYLnULsPmZyrC3ZZfayg+yuateZyixex'
        b'kjd3uC/2dngs7rPYT7q9DbNPczmlYpf16La5a39TLzsI53xTr5jtN0lgmYudy1zClrl4reRxr2yW9FnmUsG4NcYnLECF6f2Jo9CoabBCKPu3u8uTu+RyRJ5qvgpfWIOP'
        b'iZFPP34kOU4uGspeWCK20Nsk/c+FpR2gdqrt+I3n3n7u0vbb7bfrby+MbFDuGd1wu767flJr+tbRezbEBaBzw2VFJ4qAKTO82ovX43bQTaj7OgYUacEn5lBPDw4NqxDj'
        b'JjHZ4IDE443Y0mJ2OoLBO9gV3sZA5mLhNuUsq2Cylrp417HXLDMTkTtB7xYLsY/kZNDuhIehD7T3hniDNmvaO7ApXWuUALilzLRAQe7zA0D+Pc0BkhwBuszjDQDwIJ/C'
        b'dheHROQuR65XZuOGcsOlPUtE7GLOj75J/liTqX3hw7B30wUxS/OxxlAWvutjzUNNZdknuo81fHN0Ypztyolo26XaSydihs/eEsPe1Y2sefJ/dHX0iqPfy+vE7eXa1KDn'
        b'Atv+rrA1ywTHGurLOcBlknvLCFXt8o5Bu52Q3AOP6j6QbB/sCknPjTykJgzvME0WFrDEvoQlPwCeHm8g6ruEHfCkNox1uAs3ADxJZ1waOcGLkMSHwxvxrQWGQ6e/5Cz0'
        b'3EzjnX98rEl3AjRN+5FGrf2j5hMA6ieahLHB2oqyrNKQUhDOXkToNOfz1Z9XwHKlL9bFDZLKijl2p2cuaYz5+79atyew2H7NqAs03cToOgrNusEuU+xWwGF3cF+FPdIy'
        b'bam12uyFOovN+72tXHqAf0UfeLf0d4W3184ogwR33V7vXeq42xPQq1RX6lf1BNRW20or9GZWJMY9GNvjX0qvcdHT16PGuAZie2Q6g0W4f4U6AdMXxFvpnbx6mxVUSXp/'
        b'LF2WPXL9ytIKLb3dFKKUMrbxZabWRHMKfXi4/ZdugRWyGqmbUkyPn+OeFYPO5Vh6EcthNViN+h4ZfbsGzdzjT785jnuzaHaRE6sp1nyUlvGhJw9LqleyM+k9kpqKapO+'
        b'R1SmXdkj0VdpDcYesQHK9YhKDKVKvsdn2vTpufNyCnrE03PnzjRfoU1fRY9YMSgQKWSp0GOhJ0rs9wNLmZ8y1ygrk/0AwbcPRxTZq3ZfTqWC4GtcuIb7J48Gv5OsLfr7'
        b'NLNALnlyZZWF3AjCO/FJwCOenOTCySlylsmSxbiBdFmstZBOrvvXkQ0c8iH7+MAhZL+NwoQcxY3kfgR1kzwflpatTs/Oo3dtnI8k26Iy8tIiObIhIwqEWBCzHGeHSHuR'
        b'fPoKss3uAr2G3CPteYjK3Gkgh60mXSxhAt5PtsXFR4snkwuIm4hwe9kCJqc/Re6Mj+PxCRhoHIojJ8kh5jkVsZpsgOw8uVaLuDAQFvENckNg9tvxnklOv9A1+RzyL+TJ'
        b'hYGkQ/B+6CBtuBOKSvFxfABxSoQ7Q5YzwiMuSiYtmdNxO/Qrgb7f/DJH2kG67maTqSwORwWgJE7pr0k9F7NYOBeGdy4gu6Eybu1wxIUjvGtBuHC4bdcK3JSpVqnpKbts'
        b'FWnO4tAgfFy8lGyYOhtfZhUOVSjQVIRWvrRCM9w6fiBifl/kDNmID0ONIhjSM4iLRKBtdq4WBP2uoWMi6JUj6UygpKeiUBBuFZWsm88qnLBgEIpEKGzXWM0U2eBcJIx3'
        b'F2kaBfX5kEN0uCqE9/bHRxgmhOCOOpBNI/FN3EzdSsSRHL6jx52ssufmPInWQO/GPakxl0rMggd7Jb6hi4vHl1ANbkOcGuF9mkxWVSU+EUydfrNVHG7yRb4xPHT7HHnA'
        b'qupZlYFAxFR8PlSzrCy9v1DVtKQ8WpOYPIBRcFEI768dwaoazpPbIKPj9YNBJ2DeApv5seRQDasqaiQ7RRmclqOJbOD6IYYLZfjcyLj4RDSFbGIT1okP4E1sg7J8sjWT'
        b'XsrSQtqYL3MIbkKBeJPoyafwWVbfguxJqAahwQtLNbGT06RCfUH4MtkIFfKjEtkgd+Nt5Ipw60vXPLxbqDHHcVd9A3kQwaGhuEOMm8mDYAbFSeQmuQg1SMkmvJ6Nbg++'
        b'SfYx/JwTQM7bq2Bg9MX3UGCNKHm2L+tR3aoQBDQvLU+mmbJGlCj0iDwzEDfGxUZLhxexEe7Cp8kBNlt11ArekqmEVQVIywPSXuFIhylaOGC2L6c2LiEaYYopXCyUK4B1'
        b'zvY7z5LTeHdEZiE5RR32OCQ18EPIfbJLOAywG2TjjrikaETu4gbEJUP/y0kDKzmAdE23I2EzvjgsCOSvKaLgANzIVivZM30hlOMzoxE3GdpfKmKFdIrATGE9KvEZIDZX'
        b'xEgeLBpgC2FD9suTUWNMzW9KNHLfxDkCfpAjusK4pHgURPaxqvbiYwnCq+uP4x3J0ANyP4EeLswEDCnlhxU8xdbjEnypFEqJq2ipFOiAXgAIacQH8ZHMTHwOhkROI76a'
        b'mxqIzws0qX7JGijD4zOLETcFEBHfFTNIkWN4jw/obwS07mwA2FaYplDeN9N+QVLsyjr0V4QWHgrVJB6XpNiX2+bU5fhqdLyEbLchDrTYLtwKJItOQi3A6BRpycogO2ro'
        b'NoiIPODw/gn2+4De4WajrQgly8dpwq8NKxUmIWDKE7QykRRvQ9x0hA9LyE2WkEcu6TKBqkhryE3EL+WiluGrrJpD04agaFhrQ6s1i1vr4oRqppLTT2WCpky6YD2JxRzu'
        b'iucYuGaHktukXbIcKA11nCWH/ZjL2tJB5Dw7ozA3jSq9TYtU9JhoSxTQ+myopQ0KhvgMA4p7WnCJOJYY5TxVygHF2w667h4ed07AV3uviLauZsbRZH+RxnhreYJghRm8'
        b'yIe0S8fizQgoVyRQ93PM2kKeCZZkZsnJNve9OWA0YjQen5HYyIYxDK7+89NJS14o2UJPwwAFC+GWAC3rELD4cDTQ4ALSKs4n+xFH9iJyyYa3MtfgRTm5mTDcLPcD0hwa'
        b'nysxALXYzJbPKHIIlsR+f3ILH4fqHsDfyCeF7fS9pG1hBGnRk46obNKWpsoAuILOFyNGEwokscOmsBFPKh2K4mGMg0Zphn8UON6+lLvFFrLfZwC5BlU+A3+wlE+yShfl'
        b'4Y1Q54hq9yp5NGGeJI6csHeK7Fg3PzNPJc0jW4TTt/enAGERKD0+Miw/Ow9v6U8PNfOrueH5pEWYivPkbk7mPJgKsmkIFDuByLU0csE2RhjL1hLHGXTHROB9Q9Ao3CIm'
        b'N0j3bIZDBQOV9IDpXXwXqrsHf6vwdXakupLU40a6utXpOVA0XbV8fKwYDcP7xEZyTc76XIWPLCf7RbH4FJS9D3/kGtnICq8pxFtcy+IbRbE8FN4PK7ghgQ0Ln8JNpJG0'
        b'0OMz90BVRQYgTtcY4gXPxaepr6Sj12T3EBQUKlqGO8h9G5P2u4skuF1ETgUyowB6io14GG6dEiFc3QVoRRV3fGdKGIeG4+ti0gzzIcw0gGZfFdkvIfXZELgLf7ihklka'
        b'tHWkjbTwQyC+ElWGhQncebMv3pGpUqXjc2EZ1M0tdOraZSLSgbu1DNVN8liyXz4BEANfg79gskFYPLfwMXLc5fDJeBM734mv4cNs/OH4DrlsCQjgyS2gKLD4YG12jWQI'
        b'dnS+HwLY1PDDNFkd4Qvsp8y244OALS2iFNIO+iCqHgeCEUPa7eRmDchtafQ0+tbMXBXtJdm/CimGicklciObmSrfN4zjXhahqS/yU02/Wdk8krcLOq3k4kp8Voyv5jBz'
        b'Kd60yND1Rjhn+RcIu7MKFyx55aem0GnB0t9/dOhHy0PeCg3d2njw0mcpG8YN5rW/8/1XWeD47cb+i3Zte89/4Nyu7T8KzXqGDyJjPx/+df6nW2cNj7z7oPuCcsFu35Tn'
        b'z5z917z/ud90f3RAh+/cKsPxrDf+HNLcnT698/Tayt9ffWna0HE/OyM9tG6B7+VPP7r80beJ2qHv5r+7PXP+zy8qj2U/+8HgvTkn+730/PNX/6f91sak7OWvhV+YtGXG'
        b'hwrbxKIZH44uOhg/48a0fTklO/60fURObfMnr+g2flJ7Zbau+shfntwheWHtRJ8ZgamJKVPGmW+9/E6/HccaJv9kRtv0nORJSvOZOX+49sLejQcGTPKZ9Nn7G1+Y+cL4'
        b'iS1jdo9ecK78DwNaX/vxqPe0zZkxe18J2/918fQf704ne259M/0nHbtWvXlmxzfpey++/L6hfGjS5Ff/9uM7ufWLlv7UFDx32tvWhH423z/jsrcvPHtm+4kpx3r+1u/i'
        b'B0Pm1be+c/bNJ4Kurg683Sn954Xx+y6mX6++N+V/7gc8OFRhTP171/zzG7d9udn6YN/BKsXVf7QUrck3VpWcDv2zapJlmOXW2PYt/7zwwv0tn/87Perh8KdeSGwfldEw'
        b'u8Fv2/hv09e+3u+pAat2ZbZ2tZx766c3Zn2d+u7uLz+c+fVHz1Sd/nPljqQv994Meea9f8z/wmf3F3mfhOZc/9XHf7jY70pnavGTto+2LB2X/afJr07ufOZrUXjQv6sk'
        b'pcpQK/W5tMCaZPcB3yRtHhwqqOPAUHKGeftXkZbUiBwVN58cRDzex2VzeJOVrjfDokCQifD5Qj5SisQzOHwfn3+C2djwGVjRJ3FLUI3cTK7h1qDaAHreyleK+uMuUTUs'
        b'oRvC/W1HcfNQf9wdmeYw7/Yjd/D1cBHQv20VzO48qgjftTuJdZB9ztNaIA9tZCbb+daluCVKcFTFOyzAyI7xuAVyCv4VtfiZYGYbZhY+uqKQLJvXpS0TTlQ34OtmWFgc'
        b'blmL+FpuGr41VDjbdxcI6dYINdlPnnH1P1u1SNgDuk32zqEMF9eTvc6DgfeDmYF5WRWupx4d8/GNLIdHxxhymw14cTbe84iVHDeKYRoOAwNWM/8KkGX3Sl19MOweGPpg'
        b'ET5C7mYzRw0QU7eNd/XCEDwwQIUT4WNliG1rkS58j7pYkG0R6WQjvZIR5A/q2izMBYqYJME38C3SzJpNBIlrp6tVFDLJyx1G0WLEpkW7NMnlpKCpVDiZQc6TI4ILdfcI'
        b'fMHu9QHCF2mJcbh9XA72dFP+D3Y47RFpdYIZZyU8nGacdUgdwg3kxFwIc9Cjx66D4d/+y4dwfX5p3EeyEcHcOHpEmxsMZei/nJPxQzkFF8jKUP9jmjeY5Q/m+kOI/0Q2'
        b'sC6g10YD/XG125upCe6HnnjjhVK99nyQNNAZaieiuOa0E61Hbwx1c0t264X3fXRmDBReEoUaJU5jIMesFz/wOnLaiAI9ar2YKFgvri8UMeuJL6+J1I8TIcFCSLNWVOKj'
        b'uF0CatBthEaikUvxbUECugzovQW3U5kGJMohaAgstpvCvt56vJNsjxOTi3gjiO4odlIxa0Se6Et1D830Uk0knp2A2B6eMp9FzhlRrckauUQkyK8rljJjypxfPalNOasr'
        b'tjPbreSANY4cjImHnuJOVDoeujJAWPGnquLwLd94KdWnkJ4cwMdYPbJFzB9gzoEwTZa/YbZQeaMsmE7E1Kk2Tda3S/KEbrw5kEUq+tdqIjtTZwo5e6YHIICjInaBJvKz'
        b'6kohZ9NaOY0M3jpXk/UP0GFYzuyF/lQ6iF4zUGN8a85aIeflDBYpOzJKI49asFiI3L+WdWlwplITObJ/pWAnqiPPjAFpkrTOCyumcreklgNJZJdBGN5hsg9fjYse5hct'
        b'Rtw4hHfy+BRrlZjGoBkIrez216TGF/OCmI8blkwD4UGxjskOZDu+KcDrLAa9fL8foeZtfAP+MAijQgM3I+rIfmkB3ke/wx+5Ss4IhTqBEt0n7ZRENiCkQirQDYV32Yyd'
        b'wPZeNcZUTaQ5eqCwPRoeD91uh1KdIEaRTgnIUJsRvg6krEOQbHaFyTHUdpsSvRFoxFTQ9Zk817xonGNXFbDnGYdz81DSweYnD18kF/JVQGx30SPDHNnBhYCaf4UJnmW1'
        b'kRE+5E4xouduyDFQ1mlTNWQ3OYLPoomrEVqFVoGIt4/lXrKcHikme/EutuecP4Zt7jLQkLlsSKgzQxMpUcgFg/NbPw0rRV1v0vXDXX7ZcPtcGGeJh7W0equ0akcKvdtl'
        b'c3nte/cONH5hjn4nwGfqr18erd4e8fXccacuL56uH337xX61q5/nwvqdakrm3g3e+nrOpeBf/PLr3316r9b8S9uPf389Q3R6/AeTJ4wd+rP774ZVxP/e91fLycqKwln+'
        b'fz139N15oX+6nvPZr9JHvvyLztWvbexSvrq5+s2HbTP+Nu7MM9teWb7gjalvXCppHbPgx6miI8eG/m1E5+LB33Z/pV760l9jLh9YM/VPX86/N+1HT1V+7f/q+0XWNz/4'
        b'P81dCVxTV9Z/eQkhQICAIIhbVFTCvrqiggWr7AIqKhoCCRAMi1kUVwQXBAU36i6KWvcFRK0iaufedtoZW7/W6Uxrxi62U7vYvZ0utlO/u7yEBBKKnZnf9xm5yXvvvnvP'
        b'u+/de8959/zPX1L9MPNTp2Gv7N87/tkP3psz4p7qrYrlDT9t2DFw0PNP/ePRX76evrqxIue776dA9mnRHJdbhZsLbs1uS1GMyrv1bFHdydkfpr7lNVp7e92GCz6ej2qy'
        b'Tv6rvr1mrnem96QXl01yD02JqL43+eqkmi+TVlxt99gz/ty9JQlv3xkRcrL9Ee/TmLVFe1fKfPUEdrUTKRiNZq8NsG2UnQVlNZp6yRuUdfB4f+JMmhaiyAjEHomXWLAz'
        b'ZiKd0TtnLKBqxvSxZiWjCI0V+GAsvASv0tk2CLZyHpxwL59SACFFAbTjaTYV26Y4tHAluIqx7/F8cG4mWENql8FqlO10EsG11yFtYjULqsOG+8eSOCwecDueONNhDThq'
        b'RxsL8aBIomqw2ROLkgu2BOFXEud44FC2B6nj6STU56hjCvVKAQdAUxRYP52EEYCd4MScLsYjWO8EN2Agf45gYOpUqlTshltLCZcRZTJCI3P7AHwhI/ngTNxQ2ortY0Er'
        b'8VflVBt4CG7wmIhURTwtwP05RZaqS6aky30UrIcNVOnbh0aDOgs9AtlHZ6gmMQHuIuX4gh3ISO1Sb8ImdLmYojGoiZSDVMyOcUjbmB4cGoojI5xITUKywpN8uMMN7iRX'
        b'lANrSqydXsGxUuL3OkgQq1hMroiPbvoFkqkRnK1MdmAELA80Dwad5KgG7MjkPAKqSsxw/72wlvgeCJeg6WlTOrgEWm17H3C+B8vAOVJaGNyl4rTVOCnxMMDKag5YT9zF'
        b'4MWFYAvR17opa6AeXjUrbKcyqKvCM74mB9tlMV0OtrHgAr1Pm+CBlTTOEGjxRh2GhBlyB60mR4Y+LaAJsKMe0beKrfUtrZgnYE0RBbyItuWFPv3Rxxd98LYbiS7gRXJ4'
        b'cn/k86FwEPsP4WAcNkfMOvO8GMFjER8vqYpZEcF/LXfr0mywABZObb1I3eXjdgklX9hQn5qsFtq6VYLaBasr6Gsr+Uoj/7V78IZPNxQXcdzVYqoz6sxLvHyxg69RZHL3'
        b'NP3CK1HUSZLAt7BbFnHXIKv4ZAGYrAoaxfKM+Mz4VHn23IzELCNfp9IbBRjwb3ThDmQlZmcRxZBcHtU5//1gEtrVKAlmTQguvsTjiTFaDm4CN1c3oZdI4mgKISEkPi5C'
        b'68/XAk98zLSf7X7c9Plc8IUw0I3n9qvQwTeBopa2JqWaB3rnMgILlWTz54EzoLXHUrWJtoXETrPimRU0uRMeVnfTt5I1/+I3OCr9kYqMoRXuhQKlo1JkZp11UjoTQIyY'
        b'Y511JdtuZBuzzrqTbQnZFhFWWmfCSivmWGf7kW0vsu1MWGmdCSutmGOd9SHbvmRb3CQoZLBUygH72SYhhryUuCr9BjCH3DA4hNseaNr2QX+72EaeciQHEXckgZRcat1r'
        b'JYVOhLuWMMqiY06EH1ZAwDSieRLcGsphDbxaahqIa12RYTBcOYJwx3ooBxHPjlEcd2xyWuKjnVaI6mwTpyk6RIljpQGYCwRTPCnKlPjZV3ennrTaCMzGwG6O1Qn9Ks/X'
        b'lWsw6TTGo+MIvpREE0cQVlXoaRBrAk7vFlhZi32VZI5GJ46eDDP6cD/JGrKIBhXF3D7KwiVG/qIytK9UpVQbStE+UQWSfGm5VqntYq+1SRtrHbLKFCPcCZlUztzSsIs5'
        b'ZFVfiGOLZIL7X/eZOBY38u8mjv1t3tgeHLE2Mfm/kzfW4maY5cBRxnuRAh22J0OZVKGpKFaE2BJlvLSgGFVZQGJ5905j2zuLrQ3G2idokd9ksUXPIQ17nDBttlSjyMdM'
        b'6einZSRpWWi3GM2Uic2mFNaik7YNiLRoChvCc4KgvvAbHLr2+HJtB22wx6HbR75cm4V2cej+G3y5pv5Om51uSdVK7oZF/dYNMw0SXKxrbkuqVRWpdaiF0eCExjDyOAVL'
        b'DdxtM5ThmNO/i5bWnb5N+WigpPB57G9QkacxSGYwBuxng3TvGzG9EdMqspDeaEUeuz5OLJkJ6eq5O89ryBZeBkbjrUwf5MIY4nCZO/ojzb+rTBx/tEe5sJ4wt1gWfLBC'
        b'DI+GgWOk5FWsa2YzL5xhMvLEdxasoHyycK0/spzs0d1SE8NK2OXO4ArY6AJanMB2UmxjonBhBItfn+Sl7FgRQIMwzxmabbNQsMZzRlCWpff1GrjFCTwDjlJo4NllTpqd'
        b'+AVNXp44PMaXUvLC4wbwrK3i4EazPWclow4Ze1fAZRdwBJyAHaTgT1OdNSEMUuElecGTIkYyxPMGHAL7kclho+QAzmJJsrpPxxeDDnDaBW6ctVCd/lkBX7cZFTL7QFLI'
        b'K9c8QJw4cab6cWRT/LDv3mOnN+UVib1b3bKF0XGyN16Y/+qGvbqDmjblG1fb/9RwZrfmStMP312JnfvURz5/b31vw/wRnzknlxUMfTB5eb/XldH1xyr7vfvJU1991nzf'
        b'e/Xz+1Zs8K48+zj7o+Ofjgz1bpI3bdpVurrki5yHTr+uPVj7bm3dnSTtLzyH4+Oqpo6UORM7cixYg6wQCzuSGpFLgwa6wxpimGmXwo6eL7mHgO0iuA0cJUYzPDIdrLcs'
        b'pCCMxq4bCncL4HlPPjHfxkwRWpmj2BaFe+AJbI/6gsvEDnIA22C7BTsuCzfCE1HIZrpKQ+MdDIV7sCWJjWUtMtKwvQwu5pODA+TLqOGHrT54HD6LLT94ahB5mS2IDrYy'
        b'6nHlLuOxTd9vDMkg9C3psj6x6QmOjyDWpwdsIxhH8AzsCKGKawhsTxDAyzryggJtpxD/9xAhkwrWOYIDA0D9f0yjN4MfMVTDwmSrYqYSGlyesIsSl9Ljkoil5i0T6yxS'
        b'OuwQ5N7EyfM4+QNOAE4gTl7AyYsM89t0MqK+FOJqdU0yNFLq8B23sOjWMHetIr/1lPzJQIJmlckupG0WkoICJrvqsmDKxbt6YcrtO2ZynYm41EJ/sitUjkmoR0O6SUC0'
        b'gd/NT8vpSnbrnW+udyit999j6OVug0CONCS7dS401zmQ1mmhRf3e+pAiZLc+hbm+gC5VSdEdmPrkLMBmSl6TcmJXAqVZAj/8xsJCf/nddZrNHnt1FlnViVrZrPVY1Clj'
        b'KaqZvP4wO9OmFfAtRMFu6bj3Em/aaSghq1A41gPLGavOJOKvuFBsdlJ36NVJ3USu5ODZZ3IlFWaT7Cu3Esn8JNRKllRKPYrE1Epm6HFgsDTQEgONtgmsGmWyJIYh2iwV'
        b'A/Nt9N3iM1c0QZpVXortBmpg4+BrHJBZkV9u0HOMRTqkodprG/wPs4OocJMo1YWEO0bPaeDWF8W1N4kniZqtiAstZ0P5xf9mmLmOFL0ZcxFjLEwYaYCJUMW+MWPZrlRR'
        b'79FJpQHx+VpVQXEZ5nLhLDsSYM6moF3PgU6nLiojjwJlTOlB26WTqi2vSo2MnCI7tCwm4yWC3OQx4802DK4pQhaMX4mYCH9xDjPjb4E9s4s8lWpyPmaPwm03bnzf2acK'
        b'rS8IX7VapfvPcUcFYK4kwvIkkwYGlmLDGl3OssDA380mJQ0gzFEhlIDpSYruhTmqT+c/KY+T1A7/lD0ep9C+iWEF8eiVzSnAzOYUIZPOj4i0z8ZkCRPhbqNBRS9HXUYE'
        b'JVzsCampc+fiK7MVXxb/q1AsKyXRaVVaPEUFE6o2sz1sIVBk7wL1SjFl/XaE9pYwU0+xKRZVhCyJqVD1UeH2OcYsQTWmd0UW3QTtRT2yTKemQpUX2qbsUpagJ4O0Bz6B'
        b'hOhVVOLffWQrwv/irQrRkddk6oJivZpQUum6CNN69lm7ZYZIIzD1s8qABldzAegJVku5JkIjVCnqcYmzQrIV+nwVfvVom0ArRIoeFxpNVGMoXaQqtt3+IdKobtlIbQpD'
        b'4XKDXoVmDhymWTq7XKsjQtkpI3qCNN5QWKzKN+Cuh06IN+jL8fy2yM4JMROkM8qU6iVq9DBrNOgESuum63blds4eY0vkJ2+gsbaKUVuIVfpkYo2zVd6Ttct40pBdTf8b'
        b'LW9zZzZ9kvE7wm5yP/GTaHn5hVp0NQG4bc0yKfKXG4pk9h8/y9OlY0fafwCtMkaMt5cTPWZlYT0ZM+nBmO7FjLFXzJjeikEPhfn6eiljnGU2u5c23qowG9dld0LjQH9o'
        b'hON+EX0A6aRobDUN5QFZdI61O2F3YQoxdTuaCukW0nECktGmqgz9ocdciuegcb2wv5vRiNbFRHYrJrLXYghw0YpWMIBwCSbg+SbG7mlmoCM9NXEWGanxDmkA6uTcI45u'
        b'u/1mMGgxvSKmr+d+BUstdLvEWZnSgDnwaLEWdVIkS7R9USwwll2FmXdzQpmK0i0yaHU9hepN3bOnXhJVsu+an1lFi7d63d83HYagQSdI0/CXdH5k+IK+nxZJT4skp9m/'
        b'GyaYKadCctvYbO7tOSAYVHQK/kIZe+azP4pNV2m1ZWHTtAoDSjShYdPUSLuzP2qR7PbHKlyO/fEJV2B/gOqtZjQqJRYjJQyN/faHJiIb0tmUtsWw13hIi1Wp9FizwN9I'
        b'wRrTq36XX145QYpXjZH+VIi1VrQDtbn9m4pPwhBgepZCI8UbvZ5RoNbjDonSXtU9inzGOekPUnAw1tNDoiLGjEFPmn2ZMOQYCYS/en0iCxXoaqehQaW3TAS0jO4Q/pLO'
        b'H2M/IzfMmZhTe3miTXDqCdKp6BfVhOdHju01v7lrk1Osl/N6bW8TSJs7k94f+4M1BmcjFW1qfBq6PfZHxHx1ASpwxlOoahs9sge8umdkd476Kd+bZcTZOKJyXnDzvJXU'
        b'3RTuKYk1g+Fg51M8Dgvnya2ZbS0TMNOXe+A1M3GLcxVFDU6RgX0EoHcOtHMIvWDYSFfCgn2YzRE5eMkqN8MtnfrTwmfBwXi4w4FhQktgCxMal2Yg1D7Pwiv5HPT5LLxA'
        b'EG0E/AzWgwukNO+ElbwM729wVMwVhxcOp1ExI4eD+iCUGVMHphNuujNJqTS+EQPbwCZwGrZlMpXRTkXg7DQCEtqemMa+IGQqJbzF/f6es3VMCbdGtaUgzLRCZRnKCPvd'
        b'XQDns6fTZQrLiEawAewRy+a5qC+kPhDo3keF3PqbfH1jahJ/pmTd6UevVuUmX1jqfa/jltM957ov9nlEhr+smw03uzi2tDs1x3m+fPeFgh+bdczY1L/M+qdhgDzyw+rA'
        b'UakPnvvjm8928EOiXlc6nB719Q8PzrTqbwRE/2urd9prn70yo3HjD66Fhv/x+LzhQVX00OJL/asfpGmbLx3WzUtb+RFzZOSlgeNf+/OqO//49aVvrqS+ccqj6pPMBQlF'
        b'N6Nz5jq+O+eX/oP4Y99qWTD6leaPLxz75t0XAhKqVJvi8/Nrr72maxq77IV+xvCfH4738Xtg+Hi5/4j7S0atvHP+cVHAkIzJj9l3mKe3BX8lE1Ef0UMrQENQ6LAlloiQ'
        b'bLCTOmYeXgZuEgwmaA43IUJq/QhQpqQY7g2CdUND02eAMwJGqGGHR8+kvpDXwdnxLsnZ4Hr35TJRCDisD0VZYpOKzWtI3VeQ0EZn1yoSPA3rKfymGj1NDd1jJ2WG4uhJ'
        b'OHTSHNBMV+HalGCfzpKrD+4Ez5n4+kBjqR53o4Xh4HRyyowMcIPHsJm8wCBwuSeYQ/wfiiiOPdzI6hWOvGC1elXFpIsI656A58bzJ3GU8G/sNOjMrVyxxPXQD333x4RF'
        b'YvMKjUKpTLMK5tH13hq7Z1ssVzk9keAygUUhXRE+zVdSYnPNavdwyzUrKyntozhITCbsdMTUCswxmfrCVlSIhFyMTrYaJrHwPRnyRtJhcqvegREVj+KhES9YFTyFogvg'
        b'KSdQrTPMjAmHDQJGsAqchOd5q2QJFORBxrhaUKN0QZsysGkOM2c+3EhB2Vvh9UlZMeGgHV7Hp/LgNQZehGfgHlKZh+cq3o/54/AAN/AD93gOvHh8GDgShZEYPPSQ72JU'
        b'iiy6/xQ4Ex+FoRvhuRi8AU4FkUIe5Dgy4pxX+GjMFX/jM5jCKapXezDSipewA0XK29IM6p4/KATtFL/PxztfnpZGc6bkuzK+lSkOTEZeSp18Ps25KE3M+ObW4iDFmllP'
        b'p9Kcn2tcGK+V6AmV5KVA3niac/QcZ8YroT9Z/q8erqM7xXFCRpwxwhGL9PKEGHpd/YLdsjIy5PBSBrqyBNRPJeVkOpHAk+qo8HCwPjYcX/JRBlbrYDsBrKSvVGRloDvK'
        b'5oM14Bg6MABepREBDqYspHAPAvaAZ8EpDPgY1Z+CLi7CRlCLykQNDq4XYcAHPBFPwAsr4E0pXhkC7S7DmGHwagG9e2cngR1RGBTTqo1kIsHhmRSGc9EFnIM7eBhQqg1h'
        b'QkaAa6T26XkVFKMBmmBzF0jDZ7mBUnzmwkNZGVK4VcfHFXkLif83DUgAnoPnVlmGv1vAYJhGv0wKosDNvDPHiZHkzhYweXmaD8bMoS2qGoJ2xjby8M4/rxhOW7QErotG'
        b'TYp+lc6AaxmFL9xHSih29GYC/AUO6BkeZBwtYThU9dPLszLAIXCzn4xhJqxygS2onc6SYx5g52ydaxRYCw+gNmPBaTw2b3RXhzzD5+nQtMykij8o3cbx8P7Nqe7bobXj'
        b'/H9Zv3/t9prm/ieavUSp7OcdF7bmate9/bM0Le5VpxMe5Z9LZiYEzZ14sPPbdzqXNaXs3K5WzH7/jVvPdH7ytqHQuW3Um7teHHU/Vbs+zX/TmcX5bn9s39A2M3BX/l8T'
        b'N+a6xrzBbyuc9dIfdiy7kViwakuhx6Mh0tsNi6Tft5R0+IacL35q4avZ0+f5D97+xc6EluRzRyfd+XWKMVT2c17G6wfembjhobv/tUf9jvzT53Tjw/dfe9hYteNx66ez'
        b'Bn1wRzH0+h3Fa6fn7DheE5GZUtlYv/GxeHd13NpPJ9fINuwOKVr4tuSlhddPaTz3X9n74aSsW7mfbJ/7tQrI0k4aZqdWfzvpqkA+4pVkue6bi0mVP1/PGfO4KXgsbAi+'
        b'4np124/3fXxm6+871Mq8CEQDXggGN7i5a5qN2atr5nJ1IFjPAtAJNgURzxF0SAQPwTZ4jQXb4D4hmUdF4GZ/pPRIslN4jGAYD8145+BeMjV75cPTXTH9JPAKYfx7Lor6'
        b'wt8cPItiOwY/1QUgPQqqaTy4U0iyY8k2YBdSjT7RwWksOEBKyV8M9mJHEngGnDYjL2AHmqWxAKXggpsZe1EEt5OgoJ7gDHGZmQk6mO4eM/AqrM0RDAwVkcIzQV2MBTpk'
        b'DmwTrmaHw52LiJbgBffHUkeY89mWvjDYD2aVqx73dyekfKzF6sewADMF8LUIGkS8DrbCk8lWeFI3Pprp1/Kn5sHLFLnZga7loCULpDt/FcF27lHQgN6dYGtMsiXc1A3s'
        b'lq3iJ8ADFVSXOA8ugcPYIQacBnu7nGKIRwzq+9eoCrVnWBJ1uYFtriasBVxbRiEN++BueMMi/mKqgaAtjqiprrS2/1TqkQN2WjrlYJcczTQ9dt4tDMMipFv5rDkgpedm'
        b'InEr8oBH7Pij/EasP8KzQtSS5T3VkgoBRwXMImVEwoqIa7uEQ6BiRISEYCJY9O1swa4o4f7I54FwIPuhaJAzT8gKOLSEhHORZ38UOrE/sOhP5MwRiBFloScrme2L6MZP'
        b'hjWSQd01kjVMs3X4wO7VaHW4e/7XSMq0hu4Kim2GLsc0AwbKgI1gW3DQ9OD5PAuSrh4EXW5aMhfllYw3s23xNbA9ELNt1cAjJDBEjPuqIEeM5x5SyVTGwlYCZdSBDrg/'
        b'KB1lq8acWwzcC8+NVHvebXLQnUKHI4L+NakBR2aVJBS96SZZffg9QVPT9HtrXCRbD625Pcv5aFzStWFeQX7+aa03ZGnDX7/++u2/e2RNnaE5+lLSvAc7v1wUUbL81Nkj'
        b'G5r99xR68PINkpanXvpkXrL2QLLSI3rU1trG4UuuhIZhxq29KzDj1oRj0Y3Se/VlRXdKb/zl9sWR4N13vrtc8ea+un8Ount3w5RNedf/uuzR7kejNW1PV0edOg95Pz10'
        b'HP/HmNKl/TnCLbAOVoNOjnFLMDYQ1vDAuRULacffHoI6J2bMMtNtgbOgnV0FDzPk5Mlwexym5KoeZyLVYgcNRL2ZQMpuan3xoAfXgVprTi1QO5eM6OzgckzWNR1utebr'
        b'0oAbNKrsKaVDcjDSHDdYc26VAoq8A1ti4WFcxeLVHOsWG4js5EZa/aUiLSHdQiPcM5YhacE1UEspsFrhYUxeGwzPeJq4t9gR8DJDK2+FnXLCcbViNaXeosRb48E52m71'
        b'JXg4aiwJNXFvsT5acJQIlgl3CZLNz5uTVxzsZEGLnwONHtAwDHRi5i1wEGwxsW+xvmPAeY6SfbjGkvfGCWxFE9L8WD3lbm4Dx4LConzM1FtsMNjg+h/h3SJMUWQYC+w5'
        b'jFUxIcN7p97C40EX9ZZ2KdM7IKvSqtqhAlNY3DXdPh/YINsyVYWGBmtkBgVpseQrTebZHZi1jGEs0Vl9cDK8ypCg2npVqY7Cq7pRann8W4ZtH+7JdZQMw6NyPkM4tIQS'
        b'wnkltOS0etxf9ns5tMR4KnksQGVJl3pO5DixQN1qUK8zv1NwYFz9xGANiyfq4TJemnrD62/xdX5I6Y2dcCix8SoFKL+55P0RtZ//uFH3XqzzYPe4+I8zf4lMPOr1nvO2'
        b'DQ3RY9JfPdNWc/nuTw+mPBj9S6xhmY+vg2HJ5Mbv3Rdse+V2+JtVUbm3OvyaB+hD3jbs2Bwe4vTrEdXhiRO/PD47PvLmX10W/K3+s4duZ6cVNz17Xu+0pWDq0K/WjVj4'
        b'1faCtGUvDvDp/KijTqJY8u2KL+uUB0X/c3dR7CttV37K8V018m5stHPyC1PfD4tMOz9tp9R7p9vmjrMZ24e8mPX9yNLJF0cWyG8vOlcJJ35f+a4yZ1i/8sKLM+es79yX'
        b'f8z7jUWfjdt+j/0w5OMFf/rL9m+rdLdHXnu/sXXayC/+/PE7A5aXHolaMurIZcmlz70ch+4VDNS82D7YL+bjPTXPyaflFoYfaZPxiUqK+vgpeAVuQooIbxysX4I6t6uI'
        b'jKwqKdjHeUF7wTbLNzuL44myUp4OOqze0YADSNWlMa7xWxqVoudrloH/nafxiRM05vBNvdFmQuCjIrlcU65QyuVkzMEvsxg/lmV50bwhj1k0ugh5nqzIT+rlF+g1xWs0'
        b'y5uAR6FYEd/NZVQVs4Tlad80d0O+kZXLLd7T+P0/aAOe9i1zL8aS4mGIxpf9OM6SzwvPVQNBZxrYBLagMb8uPQXUgS2O3lLGbQB/MLyWqP56bAtfhzmLonPB4MTyuhnO'
        b'IM7L4fGXVwuyBaNrauC2zqn9cvVf5o6aeP+nco/yks9mzZpZ10/lpz5UJ//01gj32E+OFs5J+aSq4cekIMWx2+cqWx6luI2sD4nPLd2374Jk1rz7xtCwW0nifiKxQ4No'
        b'rTAkeNDf3srbNPj7ce9tdBsyer9HxR+8x977OfQnr3fiv3t6SsDkKlF2gDH7T0iBwMJ7lrmjWXQjnofT8ftmzNnrAi6w8EQ03EymUpUn7EhOD0H2GsqBJur8yYwH7OSD'
        b'llIJhZa3wDX+9PqxTo7NQMd0uJ5x8+QPEUAaTigCrvWXg8bkGamBqY6MUMCKYHUODdNzORVeg5uyQWeYkOFlMfCIsJi+dL0Jm2FzELYEkhwYXjKGsNfDGiI0Hx6YCXeD'
        b'JhwprRHViTHSLjIWboXtYBMRejHshLWwRa6zyOE8gwWt4/KpbvQc3FGZTEZJilM/F8a4wXp+Whi4SKs/OhuewRkcwNWZdBUArkWTPC7cY4kcHIWnieI5nVOuxP1YeFE1'
        b'gIb5aYG7wEkZPIpMmvrgCi6HM1K9wEUk4RZiVEmqwBp0/IIYbFy62FC1FLYvFi828BgfuIUPNoPTMmqbnYFbFg4LTibBDfC1MOju7GWR4rTZUe+PMkSB47lgkwJsA1vC'
        b'ktFI1Ihf9eK74cgM9BeAtagdrlvFMB78f9+7unc2p98YcGyMP11QCMIy6iqiEX5I+H1sn4n5k7urQP5UeSBDzlAjX6MqMwqwD67RQW+o0KiMAo1apzcKsElkFJRXoMN8'
        b'nV5rdCD86UZBfnm5xshXl+mNDoVo5ENfWrxkj0k7Kgx6I7+gWGvkl2uVRmGhWqNXoY1SRYWRv1xdYXRQ6ArUaiO/WFWJsqDindU6E+bTKKww5GvUBUZHCofVGV10xepC'
        b'vVyl1ZZrja4VCq1OJVfryrFXodHVUFZQrFCXqZRyVWWB0Uku16mQ9HK5UUi98CxizbP0bn+Hf3+Fk4c4uY+T93DyACdv4+RjnGCuT+1nOPkQJ3j1R/sFTu7i5B5OPsHJ'
        b'5zh5ByeYfk37DU6+xMk/cPI1Tt7Fyd9xYsTJtzj5J04+tbp9zuYx9ccEizGVHHskKsSutgXFoUaJXM795macR37ctrRCUbBIUaTiQMUKpUqZJhMRRRGTsSo0Go6MlaiS'
        b'RmfU4lq9DrNXG4Wa8gKFRmcUZ2Kvv1JVIm5t7Q+mduvmN28UxZaWKw0aFQaeUxtb4IgGse6P2FgvgoL/X/YhUJ0='
    ))))
