
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
        b'eJzsvQdclEfeOP5spfelCz50FtildxuoSEcFjKIGFnaBVZpbUDF2IotYQFTAEiGxYEeNii2amVzam+RYMSdyyb3mLne5XNXExLu8d5f/zDy7yy4sJt7dW/6fz4/EZ+f5'
        b'Tnm+M/Odb5v2K8roj6P7/XoFenRRUqqEqqJKWFJWM1XClnFWWFET/qTs0ywmpLCSctiUjHdaF9NIKa2WshGEL+Xq02xhoXcLmSEPi1rLs2oW8r9bbz0nrWjuIrq2Xqqu'
        b'kdH1lbSqWkbPX6uqrq+jM+R1KllFNd0gqVgpqZKJra2LquVKfVqprFJeJ1PSleq6CpW8vk5JS+qkdEWNRKmUKa1V9XSFQiZRyWjmA1KJSkLL1lRUS+qqZHSlvEamFFtX'
        b'TDGqkQ/6Z4Mb4QP0aKFaWC3sFk4Lt4XXwm+xaLFssWqxbrFpsW2xa7FvcWhxbHFqcW5xaRG0uLa4tbi3eLR4tni1eLdM6aI03hp3jbPGUmOhsdNwNQ4aa42LxlZjpXHV'
        b'UBqOxlEj0PA09hpPjZvGRuOh4WvYGpbGSzNF41Tpg5rccr0Pm2r11jfnel8rik295KN/R2FffZhFbfDZ4FtIBZiBrqbWcJZQq1momdn5FcZd54X+ueCKcklvr6WE1vk1'
        b'lijsnMWhPApwqCziw9RkSh2MgvBKKjgC22BrQe4CqIE7C4RwZ1YxbFs1X8SnQuZy4W14GXQIWWpvlBjcgD2Wyqy83ES4C+7IgztYlHUWGwzAN4KFbLU7SmEHDsP+nCz4'
        b'OuyOyOJRXC4LHFkPm0luOFAbmJMVkSWCrSgzj7KH2+Exb05+GNiEcuP+qYLbwDXQBrdHwC2LGxBWO1AZ1uASG7y+Llztj8u46uyPElysKrIFmtWr1PDSKttVahblDndz'
        b'wA5wEGxGqAZiVF97EV4BbWB3ZI4oDGMLd4fCmxhgQXkHcsFWFthawTJqNm99s+1Bj31eLajpUG9yUV9SqA8tUH9boZ62QT1th3rXAfWzE6ICF9Tbrqin3VFPe6Je9tZM'
        b'qfQmvYyGRKuFoZfZpJdZRr3MNupP1ga2rpfHQQ29XDm+l90n9LIP08uf2/Pn7Kc8KIoui/jjSkeKALVRnDWvsknX13zaMJ0BvlNn5f8qi0awstwnTdEM8KMc7pQDHEeK'
        b'mlVWI671pE5SNdYIfEnp2fCOzW+DKOqzkK/YV6KnW69l1WC+8dMl3awBC4qO8qxbcmtGnncnRcDVfl857HVghT6iNtaMJkxJnkKNUmoxiogsBkdRx7ZFLggNhdsjM0Vw'
        b'OzhZFJqdB3dHiBFpHASbsvNYVJ2D1fR14KpJD9noq6zAPWSj6yGeSe9QuH8qbQw9wP239cCEcWYxoQds8xW4CdVumFD3w1ulhQs9YI9oEZticyh4GJ6PUuMM+fBCTCGb'
        b'gtfBZvTJAHgVtKudEDzuJUHhQnAM3GKj9qPmzluidsYF9bsXwE4OFQ43UZFUZCM8rUa9QxXapsJOFuUfQYkokRweIx/1BjudC/MWw90L4E4exV7HmgJfhq+qA1BUoB2F'
        b'x1N4DhoJrbkLQsFJ1osRmcV4lIvhSR7YYp9LPodGSGc5uMSnsoOoadQ0eMlKvqUxnKX8EMUd75t28P3phze39nVe6lwZH8DxUK3aN2uJra3lAvdtI4dtbaNzbW0v217e'
        b'Eb9j6Um7GuGOw8vibRNmXfOd0Ws1JX7H4U9O99Cn2gILu1d4XOr2jJplrbS2yS129X6X3+/Jnx878lnlI2ru4EoPiXjTadXLp6S/l2ZXbDm9P61458d1PxMkdDcNypPn'
        b'D3d/Fmy1OZdd3tgs96irbvld+ZfSuYqtoUM/PbP4D7J3hm7fbPYR/wcrrs1C4h5aVPaH4Ay3bYKPIvJzY52iXT6408Oirr6Z2nH4tpD3ZCpu3pPwFjiXA3eGw515omx4'
        b'oBTzLWc4yIEtHrD/Ceam7JkN4dkiqMnKzedRG+F2G3CBDQ+DQdDxBHMt8Cq4BA6Hi4XZ4TrOBg7AHQ5wE6c+L/KJL/5IJw9etAEnIzLViBm9Di8iymdTTvA6B5zlssg3'
        b'mlbNRf2zHfHi1+FuuINDcZNZ4AI4D7uEdqPsUKECd/o/+VDaoQdNbxr7+85tWqWivklWh0QlEcJiJEBljTNG7RSyOqlMUaqQVdQrpE2mr2xc1jfo8ZdN1OOXWJSbV3dw'
        b'5zJNxidTgnorfzZF1GHZzmqPH3HxaJ8+Qvu3Z3RH78l64Dq1l9ervOcaPkIH97ue9znpM6AcnDMsTNPSaeOTPKADeue+Zm0E7uf1rx4KSbznmqSLu0/HaOmYgdhBzjA9'
        b'zTi/6p5rBErTN7uf91r2aw7GZXD7q5kyRuigE/Z99v2Nw3QCk+Bzr4ChwPhr3MHiGzbawNnDXnOGBHMe+VA+4ke+lMC9K6kjqTtj2CVgyDbgazzoFXjUC+1H+UyLjFqU'
        b'lirUdaWlozalpRU1MkmdugFB/slussf82aSfFJgvKPC4HNcVM3H6ZPT46ybq6ToWiyX4lkKPz+zd21ZusnnE5rEED2yc25I/4zo0541YOjywdPnLYx7Fc9S/fafErOoA'
        b'P4w6ZRPPMWFsBnWxDPNZXhclw8oiUhWlrBIO+seVUyU89MuXsksspJYaqpIl5TRblTAhbrNliRUJ8VDIGnFkloZdyZHy0ZsN0ZC46M0CvdmuxVzVapS/kFQpn7RtBccI'
        b'E66exVZiTFiM1taFS6RImZjLI+W01aCcrucSLs8x4vJcI37O2cDVcflxUAOXrxrP5TkTuDyXkbOn1/OoZdVuRFDu8Sik5FG/+SlbuRzFZBTeP/j+tMN9ncltLBfVxUz2'
        b'ex7BdFvyK07BJTYLP9xyMqXNp/DMNkl8Ual1hWtmZEDjLaFt/I6F9NLusl/H+/fQvstkIYUdjvNDEt0SY96sKZP2c9M/UlGfT3Wqcj8k5BOe4wcuTQs3aDbhfMoBHAdb'
        b'wAVOUw64RRgK2JLcOJaCQ9lGgIPLORZwd/UTTxSdCgfm5sC2XLgTnoOvZwn5lCXYzl5jFfDEAzOsw7LlWFwQTe4KOEtR/CS2p8yelAx78uA+0FaQFQE64CtZXIoHD7Hg'
        b'dW94hJTcuAFuChdlZsG+dMxKLeHrbNAMzsJWIW9y0ufpORSh+FHL0lJ5nVxVWtrkwBCHWA8gPKiM4UGPVGwqIur89JPTB9214Wlax9B27l7b7hUjAo+unI6c+4IgrSCo'
        b'd8WwIHogTSuIb2eN+PofWdmzst+/P7q7HqW1GfGZin6sH7i46/L0cj8WBD3iUAIPhYthuPNHuUpZTeUoF1sZoxaNMoUSGSQKV5zAzVAFPh69ZXj8MqPWD4/a8egvxSnj'
        b'0OO/NlHfKtkslt9zDNmvMd3t5QdSR20iORVscwOl3DBQmGFSySaDhG2iCnGsTBQd4wGDhgN7A0c3SMZBJx8khs8bDRJ1GAovWQC22CASa0NU2BYJdxdmEpLLWkBbzV+I'
        b'FaOZsI/vBN+A1+WLXviAo5yB8rwjffHg+3Fo+PR1RqMBtDfa7fG+KLjmy9tIn7AtrrG1Pe3p97fgjF6xW+7yJX/oLj/csPxN20Mi6uxu6/jPTgu5T4ilcjoBHkT0DV4H'
        b'V/AH9fQNjjo+CcLxOxBGF+ElJLB3w91ipIXC8w1osGC57LWBC14GR8F+pqQLyKTZS8idIfVGcABRO9wCX32CGXMBvPZiTkHuNBGLYjey0uCBPCHbiLBxL+mpGsmIKplK'
        b'rpLVIsJ2NlCGAUZoO0FH23MwEXarjqzrWad1CfvEK2goOGWwSBucNuyVPiRIH3H37mrqaOra0LGhVzrsHj7kGG5EsTwFNpZGuXWSWtl4OuUROjWQaQQmUzPIVOgp9btN'
        b'1DezOSyWx/NS6h6+P/WqjYjzv8zSJ5hOk1JrbhEYGE+tcF80IVgjclXAffLtdZ1sQq2BswUMszelVhNafTs/uHeGW+76w0gZvrhnc6wd9Y/Uwa1Wv11/SMhhOOrALHiC'
        b'4cY6SgUaa/YauC/pCdbdYSu4CI6PEWspOGtCq2rwOuHa05PSxuh06wzClUEvvCzkjGe3HEKVY2SpNEOWShOyjNaRZf4PkGUA4sFd1h3W3XF3HWljHkooUiHCH+Q1SmrU'
        b'E+hyPP+MMyVMAzrVlBELzUOEOfU5CFOBB7951kkIkmNgndiupCq5/w3ss3o8QfImECQvnxjL4FIDuIldJkVQIxKJF2RmF0MNOBpWUBiKjYniTGTKiVmUCt6y4nt5qcMx'
        b'rRyCe+B1YyqGV7wMbNeIilN95RsT32IppShTreDUwfdjiGF3rfNCpzzeheMhUHZFxcxKs/7VitAbrRc6tS/7Ldq1uW9/37a+zqC2VhYHUXrst5b7BoA69uOoogvRUfQH'
        b'ZawvpfBez088UlqFP7O6erCjDxE7h/qvvzmtzEhG9hZ2x4Gd4JI1MYXmpqp1RMwYQuGSJ9ipUeLYYBgJ4PIShm2vbniCxWnldFQn/TBYNEVkyrF74UFSQibcv5KMAxdk'
        b'sum1k5V5RDkBZ8FgFNZOkGoCr6XptZMtG39QOTGo46N8dQO2lprsdLTJvJJR8gIzSh4v5lAe/r2B/dx77qJPsIkxc9hr1pBg1s+n0O1zEOvujTuR2pd61138ia9wKGzG'
        b'HYE2bO6wb8aQR8YjHuXj94hPObniUXTf0U/r6Ncb+LFjiNFYsmDGEmYN4waREdIWlI7N662I6Xg8meJcS43x+KcvPCePZ4aSsYPGVAvhEAcNcaDp+Dp2yHD+bQ6ZCcNo'
        b'Il/n5Mt5Z45zCY1/eOIOZtR+L/sd7kB0fqxThNj1mcrmoeIz2GkxKz63e8XFxRd+u/Wu2NZHfuGUrW30rOWXd1zOHfnju+XvCE5Lmh8s+49lsAjOhzUc6dP+S1HUp++X'
        b'cFa/EMWp8qJ2qJ2WvpWlUz4wecIjOioOBrf0ygdstWCIsBveLmhcY6RTYEZ9AnYzuveA+2q4H56FbRFZcKeIT/FfZAeAvgISKQ0E5+DFBkY31+vl4JAPookfYWBimqBp'
        b'Iz0bma9KlQKxffsxPovfTbTsag7lPbXbrS+gV3piZd/KYf8YrWdMO38kIORESl/K/YBYbUDszwLiO3La53QHjXhMOWLTY3PfQ6j1EPYHDntEtqchs5uxthFxByY85lMe'
        b'Qb2Lht0jhhwjJkqISQmayAcjep6D6Xkc3mo9QSOz+NsqRNDOz0PQmOUiovryH4iohXbYCMH6EzLurUtLmVkJFLYtLV2lltQwMYw8s6xAY6mqXrF21FJnGygVgYRTVMpl'
        b'NVIlMQWIokWEGhmJBP0fYjpGPgDc+U06S7kQx8fj3mmmHrq4azBH0WSOuHuih5uXZt6Iq7sm4xsu3y74iSPHLuKJNcdO+K013y70qSPPTkSaXI2bGfYHcCKW2GTnwV2R'
        b'2SzK0pZd5lAyQTLhv68X4hHNGucKYJdwpRwpV8o7xC7hsakXqAFKyl9hR034k1roZ4b0vyUWay2RHYGM/7l1SK6v/U4wR1YuV9UrZHWROQqZlAl+6Uh65Es8oL9zXiRT'
        b'NKmrlA0StbKiWlIjo2NRFMbwO9tcmapJJaMzFHKl6iRbMRcBv3wbEfE3PUhFz6mvU9Wn5qMOo0PTpAqZUom6q061toEurlPJFHWy6lpZnTDV6EVZJatCT5WkTmo2X51E'
        b'BW8qasT0fNTd9SjvonpF3Y9JZ66wlTJ5nYxOq6uSlMuEqSZxqTlqRVO5rEkmr6iuU9dVpc4tFuVipNBvcaFKlCXNV4hT0+pQg8lSi5B6VBOZtlIiFdPzFBIpKkpWo8RK'
        b'Uw35bp2ysV6BSm7Sf0OhSi1UKSTwiCx1fr1SVSmpqCaBGplc1SSprkktQCnI51DLK9Fvk9oou/6lfDXGDvumaB0iCCSmS9RK9OEaI+Tp6EljYlJzZHV1TWI6p16Bym6o'
        b'R6XVNUnId2S678noefBmjUpeRTfW102AlcuVqUWyGlklikuXIaNnJS43VAcS6uPoeTJEO/BopUqJa4mbdGJqel6uMHWuKE8irzGOZSDC1CyGTlTGcXqYMDVDssY4Ar0K'
        b'UwsRQ0BIyowj9DBharqkbqW+yVEb4VfTVsOQlZiGRfnqWlQAAuXCo9gZuBK3GtP8CJiVnpaP42QyRSViOyhY+EJWRpFodj3qG13jk7Egr6tGtIbL0TV7pkTdoBLh7yD+'
        b'VS7WfVMXNml3c3Dc9iaViJlQiZiJlYgxV4kYphIxY5WIMa5EjJlKxExWiRgjZGMmqUTM5JWInVCJ2ImViDVXiVimErFjlYg1rkSsmUrETlaJWCNkYyepROzklYibUIm4'
        b'iZWIM1eJOKYScWOViDOuRJyZSsRNVok4I2TjJqlE3OSViJ9QifiJlYg3V4l4phLxY5WIN65EvJlKxE9WiXgjZOMnqUS8SSXGBiIaTwq5rFLC8Md5CjU8UlmvqEWMOUeN'
        b'WV0dqQPixjJkFutfGhSIISPuV6dsUMgqqhsQv65DcMSLVQqZCqdA8eUyiaIcNRR6nSPHyodMxIi7NLUSC5QmpICkvgCPVitQuymV5AOY6zEytkZeK1fRoTrRK0wtQc2N'
        b'05WjyLoqnC4DHq2pkVchGaWi5XV0kQTJRaMMhaQPcMx8Mp1kXNiYGBeVICwQwwjF2U0idPlRVNDEDDGTZ4gxmyGWTleoVSh6Yj4SHzd5gXFmC4yfPEM8yZAnYeQyaXOk'
        b'lyD9hMBUsjUqQwBxIkMw1jip0pCM6Yh0GRLHVUaAoNQSeR3qDdz/5Ds4qgmBsOhFXNrkNcb0FbEfiVKFpJ1CXqnCVFMpqUb4o0R1UglCpq4cka2hx1UKeLQKEVFWnVTe'
        b'KKYzGPlh/BZj8hZr8hZn8hZv8pZg8pZo8pZk8pZs+vUo01dTbKJN0Yk2xSfaFKHoeDNqCh26UNeqSp2iIRxTjMxF6nQlc1F69WmyOAMrMxNfYP5rWO8yBzdRxSavwzPi'
        b'J9POnidxzORfNtHTfkwyxCrNJTMRAQkTREDCRBGQYE4EJDAiIGGMGycYi4AEMyIgYTIRkGDE6hMmEQEJk8uxxAmVSJxYiURzlUhkKpE4VolE40okmqlE4mSVSDRCNnGS'
        b'SiROXomkCZVImliJJHOVSGIqkTRWiSTjSiSZqUTSZJVIMkI2aZJKJE1eieQJlUieWIlkc5VIZiqRPFaJZONKJJupRPJklUg2QjZ5kkokT14JxCAn2ApRZoyFKLPWQpTO'
        b'XIgyUlOiTAyGKHMWQ9SkJkOUsW0QNZnREGVSHx2KGQpZrVS5FnGZWsS3lfU1jUiTSC2cOz9NRKSVSqmQVSIhWIdlnllwjHlwrHlwnHlwvHlwgnlwonlwknlw8iTVicIM'
        b'fWUdvNlQqZIp6YL5BYU6BQ4Lc2WDDNnDjDI5JsyNoHrxbQSaJyuHN7GkH6c2VDFwndagf4sxeYtNna9zrhhlnuB2iZ4IipkIQmZODTaKJSqsl9KFalScpFaGxKhEpVZi'
        b'tZapDV0rqVMj8UJXyRgyReLQnBtAaJRFjoW7XEqy/WBiM+WbEUrmy56YkLiYxlqHRso3rVN5SVNW4nhdIzPhGKMwtgnHPFWjrNT8k5aKDOzfm4cfmZRuikyRhR/Z2IfI'
        b'UzbUyFWKHOwJYzGuQexD07kF84hbkPGhrcdxqXq3oBC7BT01mY/4lFvkiGvoYwuuh70m8ytrys37ETfKaTbraTmLchC0ytpnt634uooV6+bVmsE4B/EKE9gJXgY34ADc'
        b'ocSL41ojwEkuZZnA3gCbwab/QSchXiFknVZRUa9GlayrGrVPR5TEGDOSBlnNl66MixC7kL/zmoNoqxYpLNglTDPmFBoZcsTPUBK8LnWUixUrRREKfnMTAYprGT2pvrpO'
        b'RhfW19REZiJGVyfKacJum7HXMdaZ+kJOCc1kw+45zJSVcqWaAeA443dmKM/D3kTGbGA+lF4sKqyoroE3EUnVIFXH+DU1XVYjq5LiijBBnS9nLByjM7tS9S1BzAisZ8p0'
        b'HENvC9KMrqWzKMd8XzpbklgA2IpEidGYVRFrQ1cC+VyNHCUgIXldZT0totMUKj0qOkhWHc45DoiTxZhLFjMhWay5ZLETksWZSxY3IVm8uWTxE5IlmEuWMCFZorlkiROS'
        b'JZlLhlSXgsKiaATIYToGq9AyAoyZAEQvdJ4MsWG9g5dWi+kxBy8CMrSs97iKaWwG6I15xpM71o10bnhuaoa6biXZNiFTVCG+14R5FYanF9NxyYz0rtQnwZ5mc3Ad3TBR'
        b'ZgpMLSFWBq64olaCIw0kYi7GQCqTZYt5VjbzkQwJPSOb+UiGpJ6RzXwkQ2LPyGY+kiG5Z2QzH8mQ4DOymY9kSPIZ2cxH4mzJz8pmPpJ0d9Qz+9t8LMn4bEKZnFKin0kq'
        b'k8SSjM8klkliScZnkssksSTjMwlmkliS8ZkkM0ksyfhMopkklmR8JtlMEksyPpNwJoklI/6ZlINiC1XwZsVKJLpWI+GrIvruaplcKUvNQCJ+jPshdiipq5Fgl6VyhaRa'
        b'gUqtkqEUdTKsa435MHWSEzO8NHUl9rYZmJxelqIozHnHBDIdmlbXxOjZeJoQMeM8uQqJRpkUaSAS1bjocXx4YuYxTj4+TlEDryh1aoJJTCaZNKpUIa3EYK0RSSIi+o5Z'
        b'00JXU500R6IfSRqsmVcSnbwWC3iVTI6aRWVwP2chBVolr5SvlBhz/xJiXRrc0sZqBmOTGk1PGqtJGTLGYJHJy3FULuo1PN+mZDSbyRU1Y5czwht9WVKjrl0pq9b7x4kQ'
        b'JFocXm2Tr1hsXjPGK22bjBTHmzg+Sa8dBxhpx4kjrrSpduzhNO1pzJhunOg9phrjqXywD+9vU+bmw12RRDeGO3IsKHgW7Hct59pmwgMm6rGtXj3ms5F6LDBVj4lCzEf/'
        b'bPA/KRs9XfA/rDKf4Z22YLJaof+ktIansdO4kMXzVvo1MSVcvDdTatlMSa3OWJ/WLWwr4ROoDYLaGkEtCNQOQe2NoJYE6oCgjkZQKwJ1QlBnI6g1gbogqMAIakOgrgjq'
        b'ZgS1xfhWsqXuzZYldib1dPmBf1ZnPE5bG9XcT8PW1Z0r9TSqu71p66F/1ugfq1LfihaGkGnpXqet9KVL/TXMYj+8rc8RfcFC6m30BQdpAIrnaSzJxj9nEj+l2arEEcGc'
        b'UN18UN2cDFi4nPHVmy66rYP2GodKnnRqs6WhROe1fKsqYeCo5Ry84WZ24aLvIq1poz89mGb4IbPh1STFSZ5iPiZwbG19iRfFKF7EIbziltg1QtsvMRJf4n74Ei/0HEuu'
        b'qNInV+BVlIoynAS39Jd4b92XmFKFFqPWEmkjYrGKUrl01KoCMbo6FQ7aS5ixVFqDNFVV9ahlhRrxgLqKtaOWeG27XFKjW/ViUylHymlpLeI/1fkVlkZDAX+KrNDaQOnX'
        b'WhrvwiX7+Vios7kaC9R4zG4+fqU1WTyGyLTV2rB4zIosHrM0WjxmZbRMzHKDlW7x2Dio8RL2bzpR45i0LP7LYqoib5IpyV5lQ3/IyXqQCpl4QpYJgBRkX0lq6bFmTNHt'
        b'UkY8FHvRdNugde0pqVNNKAH/haYj1qfSM16hmE7D+RGTrKDJ+lla3UAjUZFIS+VVcpVyIl46NAw9aB4LJto8Boa5oh/AIf6HcDAlnRQ6l/xiFOZF5upjdYgpzeOCBSsW'
        b'aUggiumiaiTk0AiR0Up1eY1MWoXq86NKYRbiMNY4KomWoCLQO4M/XVOPBK5CTGep6Fo1ssnKZWZLkegqXy5TrZbhuXI6VCqrlKhrVEKyST1p8r7QDZkUerYuRFdgZ2uo'
        b'YYrWyEkrnKwU/XBL0VOr0tCZeE98vYIOZRb8rIQ3FU2ymkkL0q1WSyHmJFa9UDEMjei4T6isSkzHR0dF0InRUZMWYzTeU+gM/EKTF1xcpbwOjRqEI71WJkGIhdXJVuP5'
        b'4sYEcZw4Okw4sal+YGm0LbP96qGfE0VTURK7hrLceeyZlBovxoevvQB6YVseODMfarLgzpxI2IpCBYWZuULYFpEvAtvh7twFmeBsZn5eXlYeCx4LpGAH6LWtB9v8SbmU'
        b'kx3lQWl82PPLbFVRAbpy970Ez5gtF+6CrblIBwCtpgVTSeAKbF5rS3HBEVKuo8CKcqQ8XuKVleXOdmdR6hBcbkcm23hXbqZYFJaNigfnuFTCMnBNxVfCG+A82VVMSrmf'
        b'ZIH0iTIJiy6z/d2qBkqN3X1rc+Alc8hBDSq1LQIjuEO4yAg3cE0RtsIGXPRslJddiGEre1EhF6HF+t3R9iDKdm7tiZOdRQ0+4jvTr0v9Pt3EWvTWLzm0vTZnT+agtd2p'
        b'Y6Hf/fXbjY/Db6bdfGRZsmVJXxj7y69Xbfn6ad6fNcNOD6ctO/ttxsI/b05P/kmc8N7R7uBjpxfmfjV078zMX6/qCeN+JviHKvy9/BbXk+czv93mnq451HhwTvHZF52e'
        b'es+5/4ffhJdnKX+X2fXxxd+fXPPZPLtTf3p4ZOrDX0Qkx+8U2pKdtOAYvFoP2iKNNrbBY/C6QxCnEpwrJIvE61PhAGgriIUHjTudRXnBrdwmeBDcekLjgs5thGdhD9xk'
        b'g9pemKdfiu4KWriW8ATcSRL5w5e9HKahwky6mUW5+XFtQAvY/gQ7H5WzN4SLQjNFbIoPDsTCPWyRC+gim/SEAaATZR7rVLBzBeUMznFgmw+fLFUvF4Hj4WIh3B5Bodxn'
        b'8sGr7NggqHmCV8LOhO3wMmjDu4ENvciHGtBPOTdywK16uPVJKKahvbNBB/qKXhvFKBaBGzpCoKgo+DJfDI8qybYneArcBptxhVCJp+CuMDFODnfC3eE4La3k2XkuJ/ui'
        b'Z8DmCJyOuH7Rx0V8eKYIId/FgS/bwl2kpW3AVluUBrwyf5wq7AUGuaAte4HQ+p/YBYuVhPE7YMleOie9LDbdDKilmGXKjRaUH94AaDcSIGrn3nOkH7i4dSi7Uzo3DruE'
        b'9PvddQn/xCtwKChz2CtrSJA14h+O0jowaZI7Nwy7BPc73cU7WlCaecNemUOCzBE/4QnfPt9hv2iU1B4lbVfh/VY4qaG4xGGvpCFB0oh/2Kvi/vL7folav8Rhv+QJGQxl'
        b'Zwx7zRsSzHsYEo+RDBwJjMS/fiN+ATjPSEBQO/djk50zdsy66Hr8aMCPVfiBz0BQKPED61wKFfWspdPY216m+zNaQT1Jq36Js0xDj+9Rsz4tsGCxKljfUPj5vNuLe/lR'
        b'SC9P5ZjsEmDpWfoUwtJfolZQE/8KKatKIStfyBq1KR3To5CZh9uCmHm0bqfotBpJbblUMsOoInqQE0tPTlR30X0f0V0fZvHzdzohpytYrxCFIuEpFdXX1awVnmSNcqT1'
        b'Ff8K3talBsVrItqKbaZNr8dYgJKQvXMY4yOlB0oZfKcy+DIFmkH3n8KzisHTodRUOfvxyLqbNm/0XZ9oBl3hM9W7fxlxXQNbleq1qR+PspdJ+7544EUGYc90iVJmUM7+'
        b'ZQSr9QjqFbUfj6APSqLoxAkIYgGTKnj/IorNDIqWpToV8MdjSONeNzTh8gPLdZhOqkL+ezC1LTXSMn88tgG4w8doVHzXR6yj0R/QUyfB2rDHqAw99rF1W5z026z/vRuc'
        b'fsTGVU6+/KMpp3hKvHv14t/fxPum8SY+Zi8q3tw0/08fuuYOFhexVkVxqmyouL/yP2v9XMgm2g0csICHGRm/DF7Ri3mdjAf9BSRRwXRH0Ja2osCshAcnyybd7GxRihlK'
        b'aWmTo5GAIRAitbE2gnfKZVtRHt7dcUdm9MwYdg87WTgguB+dpo1OGxala93ThxzTJ+xqNifmmE3NWLQx1PAapoYJHw5mje0O+ibL6vl2BxG20cH3o/psIjhC61ELHVtj'
        b'tgDxlSqFTKYatWyoV6qwSTfKrZCr1o5aMGnWjvIbJcSLYlOBDMv6Wsa7wlFJqkZ59WhgKypsjDraXt/ROzCVcc2fVoYoz063T9VS46Bha6wxJWocNRyNlcai0p5QpA2i'
        b'SHsDRdoSirQxokhbI9qz2WCro8hxUOMzkL75lGfGa5ImlSqRWYxtO6msHDMo9H+FbtEsLSPLE36E44SY9cQml9DV6iqZkasCtatSjkx9mtlShb0OSplKTBegITqhHMwp'
        b'a/Gkqry2oV6BPSz6bBWSOmS246zI5FfIKlQ1a+nytTjDhEIkjRJ5jQR/kli5eMm1UoxrKsfuccQodEXqPAW4zAlloKLVSnldFcHIUAwdRro87Ee0SIauttXYFTgR9wnp'
        b'Q1USRRX6hlTPhHF+Gjv8ldjqVq5S49YtV0gqVspUSmHKj3dmMdSeQqeZSHN6KVnisHyybPjLKTTZ9rT0Bzc/TVoKM7hS6ELySy/VLcWdNL1+EKbQeLoCdRVxsiw1Xoo7'
        b'aV48bFPo2ehJLy1QqCZPxwxslJQJkG9E0FmFBaLY6IQEeimeopg0N8MNUuhFaUWirDn0Ut28//LwpcZbuyb/+BgTwa4k5oXGBRlvKJg0O2I7qDGr0dBAw1VZoZA3qHSi'
        b'G9MpPuWEjK20GmU9ol+Z1KwXDJETTo0FZw05cZF0tpiew7jCyBD1L1RJamvxVuM6/0mdYmQwIMJCCDTohpZUTs58lKBmXS1HAlq2BvW4bsBNLAf/5derZMwwIYNfpqqu'
        b'lyJOUqWuRYSGcJGsRAMQDRoZap0KGV2P9B6z5TBVwoOG+PiUTDXlSiOUxHQGYmp6hmS2FONhhz2CiNTxiZYVNajCzGGWSpn5nGW68yzrKwjmzIzotGqVqkGZEhm5evVq'
        b'5qQusVQWKa2rka2pr41kzIJISUNDpBx1/hpxtaq2JiBSX0RkdFRUbExMdOSc6KSo6Li4qLik2LjoqPjE2OQZZaXP7X9zzldjvWA6OAZvK3OF2SJxPt6nDF+Bh8LByQiK'
        b'CizkVRfMJCfaRbqAwViqZAlFRVPR8CjYwrjCWDwK/Wa+Nq/M1j23mFLjc6zUdvBSjl7JWAA1+Di2bNFCfGDBwlC84/8FqME/SPcoBy1gDzhvBffB4+C8GuuPa8Al0Acv'
        b'wV3EkWFB8WAPvJHAtoW7wYAaqxplYAt8HV4Sw505GNk2VDw+741NTQXHhOAEF16Hmxar8ala8MZMb4QK3JFXDNsbxiqIKzcfavJRxh05xQ1wB7ioyCnIzYb7uBTcjo+5'
        b'OQpeAefU+DyPuiVwu41YmC0BW8FNcMSasspmwyPwBmgn0SjlZrADXspCJbEoDuiCB2JYYBMYaCTTi/AW7J5lAzWRYtiKPhwBTmbDHVDDouh56Vwed24mOUUQXKqphpci'
        b'w1gUO3M6vMRKCCwnrfuTjXw85ZjEDSyzdeBHU8zRm6/YJyntYKcctdll5rOWy9jzUJt1kGM1PUoXoOh9dnZi2AEv58IL4XAPh3Jfi/DcxAFnwEUv0sxwv0RoI0b5XV5A'
        b'rZeFm4VDucJrXAeWSh7odJ9SXkOpdrdfrh3Ksd8S5UgN9exn/7rwk98tWda0Nyu3oUV8b1b5joPJmx47LrsroQf780bfyN84/Aa0sB2Q/FS293ubVZ4ffuIwxPls0ZMG'
        b'afCff3IxtrPkgs+qJbefKA60FgSs6/pWRf0W/OSstvmP0//+x/X+S6+9mZfYEJZdfC208ONXl/16zovFGuti/7DivKufbdt06tO966e/0+8/tGpo1eAvH9DzY3s/P/R2'
        b'8tUZu75Zs2zjcdH3H5yvTxvcvHE9689Pw+f6CIR8chpLrXsAaIssg9eNnIzYwegYQXxosRx4LWfM2wbaneBug7ctPJYHd8PmOcRZmQwGYCvxL66F+01djPmgjajXq0C3'
        b'Xgc3VsDB5Sakg8POF5gDBreUgs3h+aIsETiVlZcTAXcKWZQbvMmNiQGnyLEAYHNccE5EaCY4RCNMUOeC0+y1RXC/0PFfOTfQrHsOP0zOqDMcJmAtkUpLGV2vycWge48B'
        b'id7/W53en2tNedG9vF7VifV964c949v5Iy6e3ZFal7Ahl5gRcXR7RvdMrSCc8c8ldr407BLYq7ofkqINSRlcoA2ZcddlBnGnzb5TpQ3KG/bKHxLkj/gL2/ntqzscRoRx'
        b'KLBB6xg8MiO9nT/knqJ1TB0JDEPAtVrsawtFocYO+xFhtD4dHYhC6g67By6eI6HifsUAqx+fQ5isFQSNiGIH0gbS+0vQ+wytIGzEzfOum7B7WTtnxFHQZd9hf99RqHUU'
        b'9gf0K4YdY+47JmsdkweDP3ZMMzJdnBjT5RilX+B7HD9O4Ec/fpzEj1P4gVVvxRn8ODuJsWPUGbjdy8b+6LFTShRXsQlkrhuE2ApKR7Hf/xd271lhx95T4t57/NxOPjyP'
        b'foKfSF21SWNzhFajtlK8FFqnK47aMRaA/pUvqSW/+Bg12aiVbqVKhWzUButrSEvG61iZRjDUv8LaSBg56oXRLmwWWZgzi7rIAbDIBMKTyCxyTK+VxgmZSPgYX3Joc6Uj'
        b'MYysTQwjG2IYWRsZRjZGJpD1BhudYTQOamIY7bZ4tmEkMSxFoZkzHH+E+j8XbypjUtNIB0GdiDR7pFdJjI+9xrpXBF2lqFc3oFhkckgmyvT62nJ5nUSv5YUhBTCMqCeM'
        b'doIdS4ZV9BhBgzdkQknYO/L/LLn/P1tyxkM0BXcUAzG4aX/AojMZ00x+BqQvwKxau/QH1sBP+jmGZzDf0bEJHYyxDOrqsRNPQXT/OvMa/ep6rHrLayU1k9gOS5+xCwBZ'
        b'ZOb3AUyKMeZuDL7l9fUrMb4YIqbzdNQlIe90ffkK1PF0vXkzBBEIsiSTEqKidX5UTAjIDMbFLR3bITApEgbmmkIXK9WSmhoyMhDhNNbLKwyjcanRBoNnGtM65mzaDWRD'
        b'81LjTQg/aO7i7ONMXpOl7v8HLNZ02WpZlW6h4v+zWv8PWK2xCVExSUlRsbFxsfGxCQnx0WatVvz3bFOWP8GUpZmlJLumI3s07gGHmlVmW8cvo9Qx2NTZwwOtOVl5cPtL'
        b'L0RkGQxTc/boRnDLKi5exFhIe5E6f9DUEnWDrWzb5bBVjY9sWhe7MkecnYeU/YmFOpiWC9pgmxU4kQiOqtOwjr/XuUJZkFegO9pvN7IPjqFPvADbUY7dUIOMUmtkwqFC'
        b'0fu1wmXgEDgAXrOiwGm43yYfnlqrxjaJC+iFF5XZcGdWXkEOem5MXBDFpTzSOXCHB9xOklRkw3PKsDy4KxRbNcEZ4ixwNpRFTa3i8eAVIUni5lVvA6+CXQszbCzhTlE+'
        b'slHZlHMsB/SB82CTGq9LSATt8ApqiLHFLcheBJcX4hPno1HVNoFrvDWJ4LianMJ+AXTAlwlaqWvzCrIihPgAewF8jQNvwD0rSTf9SsGmuJn2qPfKco9ZF1LEwwC2RINb'
        b'Nqhr14ILRVTRdClp5Lg4uNuGtFEr6OMik/ZqJjLUd8JOeBnb723gNHrLhbsysf26zNNyHmiF+4lVXQ6aneAlFIiGu7KoLNgCDjNn9oPbcF8sxnQHaI1GFdjrpBbg72+C'
        b'uyzx8fwUPsY/kopMhtdr/vL999+v8eVSlpZbeYioIty9aWb5TqunBWWb+ZCL72agFqVTaqyGg31VoA230U6d6yMzYhG+iSMy2wLcLkZkkQl3FIYKEWVkInJk7t0Qgiuk'
        b'Ifl1dsuXphKnAjgM++aDTeB8IUI0m0Ox4BkKnoFd4A2ySGjjetBpo+uqhWMkY8m0Emkim3B9I4FzcA+XAi3FVksU8LYaGyxx8Do8i30ExH8AX1XmLAiF+wotTT0GM135'
        b'9vBcE/EpZIHjYC/cvFGZLSrIi8SklK/zGAhhNw+8Hi1g7hS56L80nDmCLBt0CPmUDbjNRnQzAHaQmyRsFxdwX+Bq7KgGicvPFwfaHaLUeG0C1KxxgZd0XiJmKRaiMtga'
        b'WZC3IDRbbUEKNFn1hAbmCVvYbgsOqLHJ7A464b5wcVZEGIvig92op3vYkeBAHbnGBLXKTmTlE1uarWCBa+B8EuguF3LU5Py+3bAHNI/lTYQHUNbj4Bq5hIGHiG6vIasd'
        b'2J4EBsBO0kez4G2Jrq5h4NxYXbvY8jl9/2ArG5Fp9rFj6bGF0wtglOPlwwUheQeOC4MEwRn/SH/nH7YZbdmtb7UvsgyrkqQ2vgVm/vbI53+413cSzjn61hfrVv/5lSNf'
        b'96x3yrizlVvpeuFIwO9/tqg479GHfil3XRpLLnQ+OLzF99HSekv53Vv3qzznWHx/9enh9MDWhp95PHUBG/Ma/G52O/6SW5C3yTagdF7hji3qd/74808020Lyohve3emQ'
        b'p+kRDEq+f3hn9U8eqM4VDP3KPTvpq4ymFfQvvZK9S3Ojuvo/uRSy0GXl/juqRS99/qRw65Ui6Z432n+Tlhwqd91dVHW85IP3Y6vm1v01sUvV33TEw/av6xfMath10HVf'
        b'5JP3tr+9lb36haZ3Tt9bNBzzQVWj75/9r14aDSmIufnnzKcflX65a4H//l/9Yc/05LMBPtLwGsH60R0BdxeI6j96/Vyj1vU+58j73zkVv/Vfsj8Pf/jwxeUXwnYuuv3z'
        b'36feuv/47Nt7h0/Xnb/A+8eSl3Le+vTq8PW7f8/Zdyq+6ZTi6KsvZL3n/dnPpxYuVqh7ooV25HTSWHBrGVldZge7THw/heBV4vxZ4AwvgU5wJMd4uZWp92c5nyygAlvi'
        b'4WXi/FkCroxbX3YU3CAHRdrBdnA9RywKA+3gkH7hn8MiTk1iBHHrLA93Dg/TLQ8Dg/C81RI2OAZfT2QOpr4M8LotMZYXEZgOd4FdmWwRPAn7n2CWVeIMEZphfIq9nAW3'
        b'VSU2gHbGV/TKYlTWFXACnM7Ni0A8NYcFLoLW9eRoyjzYD7qQfNGvCOO/5F7GDgGvR5KDiBdIkUghi8eYhWPg+Isma8emg+tP8HKkOUgKdBmtSUMDsy/IaN4Y3oJvEPdX'
        b'AuJaV5V4jIpA5wwsV0mLO8F2DhhIhh1kkRw4pwrEzi0ypNaAfuLcmuMpdP13+7Ymd3phLwzRKDZtMuf5ssfelTH7vsndxO0yFkE8YNPZjAdsgw3lFdg7tz8OH2A/7Jnc'
        b'zmecXdOG3UOHXYT9c+5HzNRGzLzjp42YfddlNvF2pd3J1QbNH/ZaMCRYMOIvZrxdTLbpw+7CYZew/qL7olla0aw70VrRnLsuc0i29DvLtUELh70KhwSFI9OysEcsSeuY'
        b'PBKK3V/rtY5BRg6zkHDskUNvL2kdAx+4+HRLe2ffcwl94B3aLxj2FrfPeeDuzax8uxYwKL0h1Abpbs1AOXW5sCcvbU/KSGJKe8aQd+xdQdxDXVAriHvgQ/e6HVx63ydS'
        b'6xM5wBn2iWu3HnFx6w7TugSedOkvuS+arhVNH6wYFqXfidGKMoaF8971uyvMId/MfbdJG7Rk2KtkSFDySVLqtXl3Mt5d9GbB8LSi4aRiXK04rWM8duHFp+LvRWsFMQ/9'
        b'gk549nm224+4uHeldKT0cu/T0Vo6+q5L9EhQ7IBEG5TYnj/i7nXXXTzkKx7gXrW6YDU4Y8gtu52D0Qq87xWmRf+7hI34+t/3FWt9xf1KrW9s+7wH7l7dib3JWm/RsLt4'
        b'IOiue+InviFDobnDvnlDHnkP3b27q3qrUHJU8Eh4ZLdFr8Vdj9ART59ei35en/1dT/GIUISgvAP2D0MjBorulGt9s9rnjUTEts+5LwjUCgJ7C7UC4Yije7eV1tFf52MM'
        b'/tgx2sit6MK4FQfxA7veFdfx4wZ+4P1OiluU3q34Iz2K4wkff2q8f9HgYvwIPSal9RKDmxEfLrzKmsWSEzejnPU1eT6vm7Gfn0QN2qRxOBX68wbwn+FOqCbK1CXYRWks'
        b'NFYaLrkViq2xJTeP2GlYuruheGyq1bB7ZD2fuP94Ru4/vpGjj7eBr3P/jYNOvlJnoq1hz9gaA24csownKsONurVGTBURaPZGLp4Ro6Mq/UKSlguYG6TAGfDqEiXYabmK'
        b'Q3Hs4ZZkVhLU2JLLzZaA9tWFYGcR3FmctyAcKXCX58PLxXYJUVEU5ePOAZsXwKtET4fHkF59DgyCI4VwZ1F8FNweh7R9y1Us2Av77Ij+xYE3USwpDN5QFiNFiRfGQmy+'
        b'D75BNN8o2BeBVKV2fCcUuRHqqAPRfCWwJdQaCZLX4DHE0IIpDzbSFDG7VoG+6TniqDi4Iywmnk3xN7DAK+BiLqOk7otZZrhKaV0opbtJ6Q14UB715T6OMgQRzaL8kzsL'
        b'c/KRAnR4lXPiTPZcTUE41/mFz/jLL3k7vZcZcTF933oqp+b6rCn+v9yV63c2u3Kh03sXv678xcEvLvx9wfr0D3y2/OU7iX0ZvehC8M3Pbif9/sPIX4h+dTJ2j3v746I3'
        b'7Xrab4qn/TbibbVb81sHR5LCX4s8c0/mK1zStXSnW+in9Be/iel6LHE4N83r7O4Mb9H7PmEPvl/2dujvW37xp9/Y3a0e+E/l5cpfiY+f6vim/+nnD878URL/0fV7RS99'
        b'te1T17qCq5+7DN/86dGnM8/88vaZpO8fr5r+JaTnKwaOvJMhWx4w8Hb6sMfqIu/ShKOi5g+q/rRoxaMN+S+lNO7qrSr8058Cr98OeBoTvK/i75YFh3z/cPS12PqgP6/v'
        b'YbuWrL99e+Wf0h4vW3h53Y3w0NH6pOXSqJc1QmciHKfCFltk0GwCV2FbpAXFBq+yiuFruWRlejYHdBuEPDxfjOR8AjPFJVsIdmApD16ZYhD07BBkr+0k8tsbCeidxoIe'
        b'S3l4s9wg6OEAcw0NvAGOgRtgMMt0ST7WmBYxB66v8F0MB9k5+RHIdtkdCU5xKXvwBqd01jRGtO9NRp2PrZ88HsX1lfmxwKsr4TGi3wQ2gi6jC2yKwTnKNoJjAa7DCyQ+'
        b'GDTD7nDwsvHFW+TSrZJIRgE7vEQuBbdyTHcBuIGzXG+wBxwhaeaBM5U54xb3O68AB8F5DjhjIX6Cb0i0RQpRj5G+l7JhvMYHWuB+MuE3D42GZosgvKVjbMk+5eDLeRGc'
        b'hacJ1rPhZTQo2+gco60eWONrQPHEttgWsozM5B0BR8em8mDPWub0/DPgEsTXNW7XXxImBTfwPWF7kHJHGnSbp5A5eJwnMlx6Ur+AdLoVopE3sGECd82Hpwrw3TygnV0P'
        b'+2qFzv+NupOzXneaeLPVqEUpc6uV8Vo9BkJUpUOMqvRosR3lPrWrpqOms66dg3WSql5Jz4r+sHsu8SPe9JGUnpT2OSNT/I7k9OS0zx3x8u2Y/dDb90hSTxIGTz2S1ZNF'
        b'wO2zR1w8uuPue0dovSPuukSMeE/t9cOJHrFpL+cRgdcjDvp9KPDoyuvIe8RD4Ud8ynVKd1pH9n1BiFYQ8sgCwyx1sK6CjoJHVhhibUgVrBUEP7JBsMe2lKtHN+eIbY/t'
        b'UFDCsEfisCDpkR1ObE+5ej5ywCFHHHLCIWcccsEhAQ654pAbCpFPuOM3D/yW35H/yBMX7oULt+6VYiVxujZi+lDQDK3HjGHBzEfeOPEUlFiHsQ9+90XJ7wqSe2b38sj9'
        b'Z2uG6aThKcmPpuJImkQmokjOCds+2/7Fw3TC8JTER3440h9FPgrAoUCMAG6XIPwWjOB7srrTHoXgt1D9mxC/henfwvFbBCle2D3nSF5P3iMRBolxHSNxKAqHonEoBodi'
        b'cSgOh+JxKAGHEnEoCYeScSgFh1JxaBoOTcehGSj0eCYKtfMfpbMoT+923kNH1y7bDtue5f0Jwz4x9xxjdYDuwiOLexb3VvVL+lbcD07UBicO+yTdc0z+lW9Qe8aIwLMr'
        b'tyO3z6V30WveHwtEjzjU1OCH7j5d6zrW9cYj/fq+e5TWPWrAYzB52H3ukONcI03MntHEzhCqZmbslKM8pUqiUI1yEEU/n9plr1e7xmlcv6JM17UyY+UsS3cZ3N/xNQ52'
        b'LFYEvgwu4nkXt77CF1PnbJI5/5sLnr/79QQnLnMGgEq/H1c3GVaj81ErZCq1oo7E1dISPNdq5PL+UfOU9ErZWiUqp0EhU+LtFYwvXTc5oDRMkOoc6+bmF8fPndYwMxIY'
        b'nfK1KpkZ37+JsmhpRllUCzEzPxuIN5DB/WA3aAUX4B5w8QVkql8ApxcADY/yQFJ/2zTOOudsoqjBk6vVsBMpx2IKXIM3xIthK/GtpoJzoUiNdIAXLVeBthdEcH+OWMyh'
        b'BKCVA04up4kCur+aHVNGECmz/VklmyK+bPAy3AsOEw0UtFlQXHCMBfbAq8iyv5IwyiplrjndVzlrzBHGfgkLyaNLmVVOt+BrM3Raqj/cq1cs4V4u42LrhRfgljEX27ms'
        b'JNgMjpI40GsBbyGNtbgKHEf52GAnawrYt4h8cTm4sBF25ojBMbgZVYOTxloH9uXIf9L8G67yAor/+dAX+9qnW7OjHTOqgjfe+JPVzW2LS5o4S3kdEomS2zOlLO0Pb6X/'
        b'4Q+KLBdNiZSXFzt7TefNerHq5Z96s9g7Ppq9/uapP5efXDkioq5wHaOGqm+dXJIR/ObiF6227+t/7cPl3/3045u984/e3dpffOrEsY8aP/zPxv8qP7HV6cOmV+zaP4w8'
        b'nigN37b8lcefcj+d81JH68rbiksO73z6KX9uctvh7F/8iir3XfP26q+25i8dmfXzmazdzWH2Xv8p5JPNdPA8eBnsNF4KBC4nGpbjLwQHn+Dar1aWGt8LAjszAprAcaLt'
        b'ucGtoCVcnMdG7dXPqnfOgbdBG+Mpen0GOIk0NKxvZInYlI0MqYmZsBcc9GcuQ9OAs6AHffoFuMfsOn94ArYRFeJFcCBzvL4lzqmHr+QJLX+0QmBpUAgMaoBEWYqHrRFr'
        b'00GIGvCQYtSAhQ6EtyOhHCQ8kd+Xfz8wSRuY9LPAlI7c9tnd7iNT/Y409jQOBScMcgYLh6emtWeOTI3oX6OdmohCwWEnavpqBmIHLYaDZ7XP7Q7dU/DIggpKfWSLSrsf'
        b'GKcNjLsfmKINTPlZ4DRdeV4+3ZKeYKRMeHgd4ffwh6ZGDrgMVHzskTLiMbXXQusRet8jWusRPRB6zyMVg3g99vc9IrUekQP8jz0SH1lwabf2TKQchMT2SpmPa4PTB0PQ'
        b'Q/d9BypoOpL9Hj7ttv/UNoevTMWBrs0+N97mMNfhOS9BOYoynmSNchskqmqTi7IMNi3eqLOPp7soC59yga9fxncN8g2XZRkM5X/5siwkEz7jsMysrBkTC5hDKyWNOFRT'
        b'YywgfvxRDbiyKXRWJR2GQ2E0EqtKZg4Xs37ZGnzkDZ7SDBM3yRvCIsiHdDJIYX5GVIlPC5ca5mEliopqeaNMTBfgaePVcqXMIGdIGaQCJLmErqyvQUL9B4TGxNunLfPJ'
        b'BWDgKDIGXg7PRBxkfiayP7LzcsHJokxkgGgi4LHlYmQUZMJtFg18sItM7MAb8JXVOYjjZOeJYSuy0IqgBl/PnYl4DGyRh+JjH3PgFQuwH96eTbiz5VQ/2AlOE680BzYX'
        b'1bDAFviakFwfvSocnA1HuCHzZfMaao0A7GZ8Gc1ieCm8gE2xFlKwGx5A/52GZ+XnX0FM+wsUH/7V4p0LLliDKMdbOXdXCDr8/ece/hvbYuMsVaObysbe82xv+vVB3rKf'
        b'7P5tQdPI29bRK2I+X/P0T59++h+iN7bWrni0+zczKmWbZa/XT/VvCVP9lscp2Xm+JODUno2rK+o/Lbn+x/uuHx/s3PKn5q+v//4LwcZvlsUMXNiXPdLff/Nd7aZ8sN1m'
        b'xJ5K2NEd8QVf/dMvvCrXvPm+x2cHrOkXZ55pbbD/+9Cdd1b89GLzqbv1ts1Hfv7B72vf3ZlRtuuzE+Jt10TFn7/q+TmwnP7tX7fdLzz5xfqvq/3e3WqV6wcDjpycvdgl'
        b'47e/e+t+w5xr66jkXyXvy/6L0IFwatgKtrqTHkL6lQ8vEQm/xlhi/RXlIlsSWauyGdiGJLentrHXO4DtxPqTgc0Qzy2/vtpupW4+wQqcYIPXnEEzkQ4r61bDNg9cAOpP'
        b'NsXPZ0+Br04neRfBN9xRma0R4FChOItE28ABNrxZCTYzl1Ztc4OXcyLALrDPsYC5V85mFht2W8FdzLTBNrB/YTXYhguJLMC73Teww+CJJYxd+jq4gYQyki9CMdxNKuaA'
        b'0IriVKWFktyLwaGQfHDS5E4rJK/eIGazJTwE2sIjEUFlicRCNso6AAfgEQ5SQI6DnaRm65YmV4M+YqpH5vMo/jS2uy84SoqeC1un5WDyFoPNEZi8rQRs0LdSyNQKz8Tv'
        b'BW3gIHZ36Jolne0BW1yIQOPCvWuMzOlgeAhfuw13AOYu2xWgswJcge0Mcui7oJ8dAY+CfUKbf9YctqFMphIYAcjFw7/JzsDJ8SsRfXwWI/qyHSmBW1diR2LXjI4ZvYH3'
        b'XEI+8fIb8tfvPndxJXHTO6b3Cu65BPfHnE85mTIgvReeapLMYwq2Rw/at/N0zvDOafddQrUuof1u91yiHnj59Qb2c/qXDXulIFM5OBzf9nW8tse6m9stHfHwxnl7i/rj'
        b'PvaIQpZRSNxDgXtXVkfWvpyH3j5HEnsS8R6+/sB73pEjSF5a9lj2Cg7ZjyvlgY9fr/+JkL6QExF9Ef2qgaJh/5TBOfd80u4sHJnieySzJ7O36FD+Uw7lm84a8kl7jD/z'
        b'nz5pKPidEp9O9FaS81xX3k9ceXN9rRhhacUIyyeTSMzxrY89yQarihGiFix8L55J03+vN6iw63odkqAeeGnsc1+Aup8fTB23ieYImRObRjlzixfmk8upFHKMu2W+7k/I'
        b'Y37Y6J/LuPOA8UZKaX1FaSnZrj9q2aCob5ApVGt/zIEAeBskWQhMXPXEeiQ6A6mzUPA/MnWGfcXjZ83GGh/fzNdkOAsLI6isZZEz2h5z2XaOX1lS9q59nJPKO6naJcse'
        b'+Pr1Jw+lv/iEw7IvYz2cmzGyYOG3nAC74K95GPCIi4KPs1mUl/8DR9GIIOEJj+2VpMl+zKc8/R44RowI4hHEM1GThSC+wQ8co0cEMxHEN42lyce30tEPHMNHBJEI5BGt'
        b'yRyDJGNIKoG4T33gGMZA3FM18xDEO+CBo5gpyBsVlPONJctuNusrPkK8p7BPeSH2TZf3Yh/40CddrgW8GfueFCNfxHq4oHhk8bKnHJFdOgtjX4Swx+GvXmThGgdcKHwz'
        b'6D2LO1MfePv2qLrDLnBQKYXaRUu0EhkuoIqFlOBSvHCbU8Cyi/mKwk9cDorg4vDTcna8XQbrawo/v6ljedr5fJWAUQq4Z+f7lO1mF/41h7Kf+hiHmIPtMCstAddtlFmI'
        b'Cysl0fb2HMrOhw37auDrZD3HHHANyflD4JwN6Fdh8WSDl6PMx8tQpsRwA4rA1f/bV1Jb5DP7Zo7Aqx6FSI7hxfd+lB9sW65btnEZyT8xGIiKxxfsceEV1irneLLewy8z'
        b'hJm0EBXlIuHDTFrAdridNJr1NLt18Bhsy4rARlEsl7IEbezsrEz53keXWUo88LdafcjcaB3d1sHinNl2d/kO4Y4lH3R/NWv5mUH12crmL/mnKt4p6gJ7wc0DVll2IW7x'
        b'EZnHowQXGmOOR6liMjd/bBHbULkc8bjaMic7/xQhj8jE9Dy4iTk8ZkM0OT6GHbtM50VOC5gGj6AKGTmKkViLgheYGybPgstq3cKBdBlZOsAW1YOXGWPxOtgLL4LtYD/j'
        b'Kjb4iWVs4mF2D+OAAxF4ZRwTtZwtg+fA7Un3gds2KGRIyZaV4gWiTSZvRMItohgJN8uJEngwMkkz56GLW1dSR1L3nCPZPdkHc4fJaeZIZKV2pHav7rcadokZe18z7BKq'
        b'mfPAwXXE3bt7Xvei9vXtXBSnyTE2qUa5+IOjfOaMix+4EtsFSwQTTP3YRpdhb3Rksbye915JE+J01P1+/Qt8JKSN0ZGQkXhHNxkhVvhwSBlXym6mpJwzXMOxijwC5SEo'
        b'3wjKJ1ALBLU0gloQqBWCWhtBLQmUORySa3LgI1d3OOQY1BrhY4HwcWi2LLGRRmlYlSypI8LNVgd3woc7SqMJ3AXB7XFYw9dYaawruVIBgjhIYxCEi9K64oMTdYc04oMZ'
        b'OZUc9OSifzz9P6kzObLRWhfmjAvr4/W/XH36cb/j4eRd6nbIQU5J3XH+TpbUA8ejX0/jb6B3L30+FPY2Ck8xCvtIfdFzqhGENgr7GYX9jcIBRuFAo3CQUTjYKBxiFA4d'
        b'C4+vr1R4iH2MJQ07xMZHUcqcZU7ScKK7hlAT/vTcU39MpS59xI9NT74i0J3RyJw8YF1pIRUhKnAlB2lakJ7nScUI4rbW2apZGDtqVYrkuyQDmbomU/cGfwLWYbBn2Wjq'
        b'Hh8DyUWF4zvh+YYJe4t/24R983hxwaHGiwtrZsL+lRRman5+UoXtQtd1zDpOynoH5cGiQjdFbMxfv8GFAQ6tWs/6C5taPFTRsK7AV0WpoxAQbIdX8ZF0RstgTTxsiDu3'
        b'4ZW+oYVVlo5g02JSEnT0p/D1sPMt1ewFs9jUF3osCUeTbzhozVPi9Q6nqzsOvp+A5MqFzqBXWKVX+N0eKT2pS16ITV8zyzND4MnvznWfHTLbuiLBhTM72r39J3v/CO7M'
        b'D6Sk0VUHOUs+CToTtV4YETU9b8dh2qVHEnM4V2grPLOQjnYbXOG42/Xld/hfXGCt/UOD77qUd389JWpDEKeKT3XLvIqDPxFaEQkEdoDDZaCtINAXKw0cyrKIrfLMJGIC'
        b'mZizkdl1HrzuSyag+SFsJxYSMXjWuBjsgwMTzl0rA91cy0UOZAK6shoMmq4f2wE1CbrWCvLkVYNzkcRrCm7H+jBnpIWHipgWRSncp2TDV7jTwFGwnywzW+IF32BuW8ZL'
        b'5vAOXg6FhO1xJ3iQA/q8E8h5a6iYm/D8WLI8cAb3H7jhBPdxwGuFyA4mSxguzC8FbZEbX0KWaBbcwULW63Z8hXiP8xPss4fXKmtA22pUBtGRUElgtxPoL0CCuLUA7hLz'
        b'qeQcPtifVizk/4DijMfHhDPQnA1jyfQQtLUUI0WXOVFTA9u5e23wMivBwSUoaP3YmqIDeqcNT41qtx1xmdrrd9cloN92QHE3NHmw5t2KuzMWkLVVqcNe04YE00aCovGB'
        b'ZP4j/uH9s/sX9orxMWkjfkHkdDLdjy+NPzHiF9jLa+fuszMStIw5Nsojy/1HuXi32Kjt2KKguvpRK3ldg1pFzvs25+FkDDTdzNezKx7JNpr2WurEYiVhKy3pea20Hr6Q'
        b'OmkT988dUqY7RItXims62bFERrjrzyVKYxufolRyoIQ5lWjK2HnVE84hEis01LgL15/zQCq7UuOeeA5s57BNTvqKvOsTyeDra4TvxGPJxP/KgU/WpQZCeQ5M5yFMFfjU'
        b'HAY/nyx9GfrNU/8yeobTxzCJl9bKJz06ywx22Ri7sdO93LDdS1cq6mv/dbSqTdGSrHkOtPJM0RIQtPBGvX9TW/FLVfUqSc1zYDTfZHgsPbBUd05bES5Hv/9vUvT+Vw/p'
        b'mqhJ8BhNwj6RPf9lZo41wualYEZpiCi0WPE7ChlldFnE7aQASn728/dZSqw5WIT/UW80slyORmWz3yt/OzsjeFv+lBWLYtM/jilmvVfG/8iNOuo93dWi6TxfyHqCTwGD'
        b'F+CrruMF0Mb14+VPMbgwmcXGHJ7lZMxvx47twiIOyxmpM+UxpWt9x/reBXfdQ0a8p+DVsHFHpvfgZcj9aVp30ZCj6J8/umvi1wvZRpNaFc7/xKTW/6J3ovqHvRM6IjkY'
        b'zCXW4ayEmoS/pp1nk5UgT1Lfxbn/pmBRrMvvyWfVvceQyBdP4w7u+dZAJKqYTPZ7EZW5PYK3Bcc/zp1fnPRklHovGxOJMtxCPlMlZD/BM0RwD+yfOp5ETAlkNrwE9sNd'
        b'/syStNYVrtjrHyYSY1/By6AHbGHHwquySW1+h1Kyx1LeJCstr6mvWNnkadSfplGEqsJ0VNXgTIVG4OXnA8XakNT7IWnakLQ7AXdWD4cUtHO77DrsumV3HQMnkNUoj+wg'
        b'/AGrPh1b9ZMjstjYxK9FBOb53Cb+eB6E9eCvsYeTsW66mJsGqErO/wSJTZwg1J2c/Tffb1lH639uQc0v2/g3bibFeMW2zYKt4DRK2ySBZ6kmcMpP7y0b8ADYHbAuooZa'
        b'B16H58l5OgWwy3bMqomE55n9fUWh+SIWFQda+faFsI9shPuJD48qWos6ZFaZbcKMaops6mp2yWe/xX83wops6qqyf8ocAjR9OvqA7iRrsBu0m2zv0tGnyUHWfbDHGh6w'
        b'cGNcmGTVyRV4bYmRM44qJe44Fbwi59prOWSJiK3l5oPvT0OjRvuyX2MIZ7Zott3s6AoHb5fZIYV2cEUGPypT8kGjpCzU7bTk3S3b6a2C4O7r5Zu9tgl+U6Pkbzv1uf+f'
        b'nCsHp9nkvtHqJK0LUbrZuBUuDtocmBt06u/FDYmC5PTcTTd2iJZyarxTP5nS2Fw762BSdG2J3TFPz4EbgW3ebb9PKjv+y7v7QMmbRW9yv+JE7V1z4V0lWM/Zm1eZX3mR'
        b'dXFd46WoopiGKxT1zuaQDbKvhBZkIHpVCE2n2KLgCR6nauo85mjsi+GwhVhVuWXj9hvthzuIcACHwuoMAz8TnjE79sH+JeA82e4D98+Am2zCdAaYoUy4ZeFUcIkLz8Pt'
        b'3k/IFPJeX3CZLBfG9tdlMIhpApzJBjv1JfOpKHCKPwU2g7OMB/K60tawpScItJNFrjPhacbCuqmCB8ecj6B/PfE/KsFRIdespYQp3HCqMdI2VivkKlmTo9FQJxDCagYY'
        b'VvN1ozPl49c+54H31BEPmgivzrW9sXs29qvOrz+5frDwXmTaHem7FWDlJ76hQ8LUYd9pQx7TDEKu31nrHTHsLrrAGZhzyUrrnjw4+677zAfevt2qg8n9vLveok/8xUOR'
        b'+cP+BUNTCkY8ptz3iNB6RNzzEOM5OLseO+a9v/CeR/QIs960139YENQvOO990ntg8bBwhlYw454g6LErQtOI4fEZhseVKKqUZqUpX8/09BdEYq43oSmWGTG7b9XO/8Tc'
        b'Vic/gHrNRszJr+Cak2tkjQhL79MhHh3M/diVXML7uCZrRHiE93GNeB/PiMtxN/B0vG8cdHLeN/HUMr3zf6ewIBK0Arxhdyo1FVyBzOH6ZC/x/HjY3AivhqMWU1NqsKuC'
        b'2eG7Lwy0wMvwVYY7Uk1R4IqcwwEcctVmzMd+B9+P0bv2j0Y1xqyOOVO57dH17tSeNs/wnoXot5Ijq4w9PvCBzOrSYOXDXAsq9rr1yEf7kcKGBxnoBafBddAWiXdZAzRY'
        b'8OLtLBblXc0FR8FrQJMf8wyy32RE9mT7vklfEwgh+yiG7B/Nd6E8fe57hGo9QvvdBlwH+cMeM9t5D9ynjHj7POJQHj6fBQSf4g25i4ccxUZkZzG2ulWBN1grXFkTtDml'
        b'BcWY7gaJWzie9gg+cj3t/Q0fP+TCYgU/j6C1RGWakJxBzhE3IteI5CwQ0WEXohUhPIv/BsL7EbNOvHyGwHALza1/EXQi/H1gewnlk7VQvuqlWJYSX/W68cKy/6+574CL'
        b'8kj/f7dQll4WWKlLZ+m9qUjvvdgVF1hgBQHZBUvsFcUCIgpiWSxxsYIVu5kxiemsa0JJcvEuuVxyyd1hi0ku5T8z7wILgtG7+30+f2Le3XfemWdnnnnemeeZmef7tL0b'
        b'gcTo9NquXY1b2k3v/r1o1gd3KM03rSM/sTDek37p421GqyysGj5i576hnaN485N3wtu6mhYFF+oo536N7AApleVg8M1fVw1110tszGpRwxuztATpkq0OlRiZqXXbSDKR'
        b'pVCVLM01pbiTGqYiyem3sJc5y03vW3j1W9vJNNqSG+L6eU6yPHm8kheAxMvZ7YRzj4Vvj5GvmkzpvIRMja2zzoiIDa+LTcdSNn51K4dWiLCozcGi9oh6RXlzGytvw2NL'
        b'OaW+bE2GOC3VIKfxfyBrzy1ZP6/gDckankTFSH/aleM1HTbDDvB6QCKL0tBigHUBsEWcuPouWxKO8rTe3N32bjiSumNI6vw2djRd2dDI0GnhhU+aPGt6zE8H9PJO6en5'
        b'zrfMMbNixfiySsI5fCp9DifOwQ2NXbijwH54TIp9jMFmcB37GYeA/VOQUj6hzGkMyZzKbzZfFU1IJXQ8tV4c9YTInadK7sqH5a7Pwk4WcIrVEdfpfDK1O1jhGaV0i+5x'
        b'iFFYxPQYxajJmvYYWRvQLBYWSiurx51CtdWEjBYx7Ms4ceWWqEtZGZaywVeUMvKTezVdqeO6/iyBIe3ASVw5iVMndu8c0B9ZuysTLRvQr62sKSwVVZMa+I2+9R/QLcQI'
        b'uKIKqajaT/3Gf0C7SCyhoWuxb+iARq1QisN8iWqkwqUk3BQ+RzKgJ1paWCrEwZBw0jGSEx+H9xvQGYKeFRepwde9TnJIxdJyEeI1PtxSjTWA6jJ8wVvgY8KPpQ9o4+DD'
        b'mOSALv42hBFHkgl+Nvk9/+oCBj4CgyGHCiqXEpi8AY2q0soK0QCrWLh0QEO0SCguFzAH2GJUcoBVIC5EN1pRMTEZeem5A+yYjOy46mo8sOBlp1EWGuY53vB+XEENuY7u'
        b'pcimFj7PiicNqk6nWPv/wFZ7bs3I6rlXuZC21W7UrmD8GB3GonyFcyIN4ihy/rISnIDbJfCSYbUGVarNhK8z3EEXoA8jJEqzdSIl0lr0FF7UZVBacB/TANZ5E/MKNtnD'
        b'ax7Y6ey0W2Kad1KasUsWrEsHpz3hTp/krETPZB9kcCF1fwheBDbN0YuBm+mjndolWrApC2yHDRTWg9I4sTVkDLgMD2sEYLdShivsRup6EzhbTQqAxrjVAUy8SwQPBVAB'
        b'ZuAMOWih6wtPo/xMiuEGOuF5vBHTBpvJQQsTzeJKuG/Y145B6c5mwjPg/ByiiYmAHOxAJTUphsDtNaSYgeNeZKxbBRsdaCdCuBHuC2JTGrCLAZvABjvCxJkMDyo39TtN'
        b'ymiBQzVnvsrgPb6YQrQYFGJeRxoF9mil0QA+B1YHpXh7eWMMnjQvuDW12oZBWYCj7Mg0J0ItuMSeimT7a1BVC+barwqkfXUZ3qRmLIrhCdbCzRRB9TxLQ6+eZoBNHhjN'
        b'VTczibZoDMF2VkEcaCH0+iwsKM/EThbFX7Bin585RTN1f00YoqdFMbzgaXiIAq1wXwLpYO0kxCC4g0RjDwD72Z4MpDyuhY00vow4glqxAE1RvgtMckyQaY/ZZrJ6VUAg'
        b'6MSVhLfgCQrsCywnlXYBu83xYf40ZLJz/OZxmaAlHF4ihH6dk0LtnuvJQixbyA02oAnB7bB7HiaFutpnWQkF2mr8SJ2QCGzWpJ0WOL7klOQmpqMxaCekLjmzKW3rMoyu'
        b'lNocnqLi/oGkooDAYFQnT0O4A3XlsknEXzkTnAaNKRjuth605sEdtGOoAdjAioCbGITeyWlhVBU7gYGG6OofPKxo/ms7wo2IHhO3cQvYQ4G9sAV20Gi6R8B6cImmma6S'
        b'LGcKyZYl2M0GW2dMUTHcBFxEFJBsoeds1IFmYAstEDfgBoouDrckpNM9aFDFCg0E20mFPi00oZy4jWhqW7DiA+FiFdM14OEAfyyqnvCULRKvJLiRyKopXKdDyyo4BLYF'
        b'MZGsnmPA3RFwA21tXF2kHxCEtHWGPzhZhcrBbnfa0eYGOLPAIwWxGBxjpjIoTTFzku8MUvcCuHZqQAguEwqOwXpUd3AjlbxPPO0SeIpJhC8JbgVnKUpvCssIHBQPvblb'
        b'NVFBxLXwXNiCBKMEHKQXUU7mwZtwf2kK/R4KsNuunhHLjBdMewuZ4VhmdZqoC1L1ypxokZ0MbmoFhCC9nhEOjoN1SGRBmzcNl3OEkYHqQCCHTi5KQfJRyLSCDXATKVfl'
        b'C9egckimJsO98AKqBeicSYRkFrgBTqak4G1YZmVsDCNSFEVYkecNjqESqNpTwC54DckhKthGS+KOZLsUPIZtqwKb8OaspimTMw2eI9VeYvIa9YTrzURCPf1EQI7qTbsZ'
        b'rQPO+wZqUIxoUTJe72qGJwgT8kADPIyssWSyW9zFYcGbDNAGtgMZofYXKoHatqAXYzm5v5W7nJZDuB+er8Tk0EgQswLsQ9ZdFpCR1mTaTE9Bw4kmxZy/Sg8J2UZwldDZ'
        b'UMGjfNmztRAzrTvnCughHl5Av3QpJQmfOYYHwSU2mwEOsSeTYTVbCOqInxc4CJu8Ke85+uTcPzwO2+yJt3d2Irg0GW7J8JpOn+SHdWmeaOShqAQTLSvYDW7UENfteniO'
        b'Nww7hbexWyrBVSZohhtAy0jEObiUSbGr8IHYBXq8mKm0IbMiQQKbNLHL0TpPylNKB7MTo+F5T8qo0w1IPzwFd6IJhk05gxMaNeAklNNTWJwHrM8K8gWHneFWNsU2YcwD'
        b'R1EfEuF7HbX9Skoufg0ZOEIbaKJgJ0rbRtzZmOCWiTqCWu4Muv7OGRriQDRu4reoxIQJ23TJlv5xcBP1MRfsqCHG9ia4Vx/9tE8a3JHolYx61xBxcXuSH5tyydXwh4fA'
        b'GtLqx5qWVGDiJg0kKnPvVPmqxr9LyUAO27TwJn80uEWBW3HZ5GQkuJIFD46iCtoWYapMyiVPIwBNAUTUcsBBVkoWmlYZ8BTY5Yte6WjQSNghTIHXc9KyMOYZ2Ai2Ml9j'
        b'WEM5mj/IUlknGsHkKXk0O445g0tYOm76kPboohbuJSh1I3ByDMoO1DPB62x4Ce4FrfSwclSrFrbpU5QZ2Is0dXC9BjSTATcRXDHHb7l3UjoqmuRlBbb6sykrsI9dXgM7'
        b'6TfkVDHsgm0sinKDp8ENCtywRsME7ookcMxRvTDogqf8mah0G3sRuJhJFlUWW5igIQnDUogpMWp3A5kUw1GburDTSTpof22o2oamrIWVDjWGuJMXeZI1Gn6lHWXnr0MG'
        b'clv3qR40KDqSLLxaAo/A3cg8swYX2XArGudoL8hzbrAJtqHXY9YKgMaGa8IVRGQTHZbBeqyM7OWUUWWGEvod2A9vmKTA5qVeXknglFsyft1MI1nEYaCekNMMhpthmx5S'
        b'0dCghganC9OYNGrZhaXh2IU/GOxW9+KHXaCLZtrpVeCiRF8fDVJwBxMcRzLgk0dE6y5bh+LqfcZGouU5LcmeXnoyKCuB9RhE7oRlJVUJ613pONNXDOYiXS0RA9VtS8nw'
        b'IvXjW4Ez8CobdjrDZrKW3p/mzPjF6wgSy8iKz0PPCy9TZJiAt5YLyJKVfulyajmUgcPi8DuTWRK843KyLal5zyyJSZTR2yWbImf6OtnzNEwL9RZerzzi4hL/5covLs/8'
        b'a+6xhcvmLOPff7Tr8squFV2/GK1Ieu3L9Bi/z1ub3VtOHPzt96uv1V5q++KnaQ6PVghXXyj31lHsWbsr+uSlX4zPtp4pFW1L2P3s/KUzJdNbly5b9eEPOnFmqyZr2F/1'
        b'3/1G+Xuw2zH8OwvOxsA76WcyvthjX2RR8nOKxqdGZe9PX1ezX+5zPOG1hTN2XjfJCn637Gx45s6YHOr3gu/PPnvif235jjd+SjP5YdeWo2/bbOBs8t2y4dx63zeN3BP7'
        b'vuOnBkxft2FlYt+/+LmTovU5WtYbJm3yrd+w3gBYx4Tu/tnpb5OA0MkzVLtmUxWbc8aqZre9dcrKI+aTwMP7f6taZ78/Fgi0/hwYE9r0s/WH/hskHRxUQMNprtTI22/D'
        b'e4ndf+F7+m04mdhdrH3j3Vt5W70YUz20pn6z/LP1h9d9Oz3K5vtJP+74p/TCgXn6GeddfhE4vPWo6vK/BQUfJ7+fen/Vm59EOSsvXbzCflh/2v3ejJ8/t+IGzTHe3cWs'
        b'vsWZpbHxZgbrWsSPH4UuvbNKUlg3w39yVYHjglt+oYyrWw8GLG/eN+fB5JI5Mcd6/+K+66er+9/vbWsHP0VP+7WmScMtRdbd/L786Rt6X3JajWY8/cedwsI+ln+bq8Nn'
        b'Qocv3nxtSeWDr7M3/Fvvz2vTegwfRngZbU1Y/9Pf305yzsie/mj3O19O6m8SAMmmwXVORh/NulWkfbbud9NczbOTfrWqjs7ZcPn3IDO55Z/8NjwTlP14+5tpf8+I75g2'
        b'ufpH4HuzwEz/es4Xwa6+54uaby9KuVVhGv3x2iU/XVu4e7soZWnbaoZh4FNhF0tgSlxMmeAi3DbmRBe4WKh2ogs2TCZnyqaAa7DFA28jMcE+uA+0M9LgGhY5U7YiuBTp'
        b'cMhc0aRAN2hgxzKQhrBTm3ggpbiFg3rDKr1qNDhuN6zVn+rB0aS44BCrMsCOZMiAB8W6C+eADs/EoY0MY3iVhYaR7hyyJ1ED5FYjB6a1Q8mRaXi4kjyMcQE7QL2Pyg1I'
        b'Gx5ZPJMJ6h3n0RukO2rCyPYHvXKrnQav85hFk+GeJ+RF3GCyAr28qD211ZqMKDbYRXY5vMFxZIyRQ9hoht/uqTqGDbYkkB8sQSbELRV4Sy1sokHajsKjhBHpC5DxUw/O'
        b'pqbBrrmqw3WgzpK0c0mZrfrROjRjHVVtA03VIpgnsbOFGH4zdfRxOPooHNzjSIcG2wVPoSaVwW2jTsPRJ+HAVocneMKf5YdU2HqMH7M9zSsDzfVbU8GOYS54hGmAS/Ai'
        b'vEQO18FzoE46ZpHbAuxSrXPXwf1mpPJwrybYj20SeAZuHgXqMj2ecG0WrItCZNTO3rHMmGADbC/5rz2yRiOTsIRFRcv1R5Z80C1ZhLrJVvkim1G2DioQswCFTfA9m6hu'
        b'dEm/PatB5zOuRYvmId1W3TZ9JddFzu0VhCkEYd3uCkGcghvXwOg35X5m6djjFH+X+9Gkdyb15OS+Z61wylNaTu/hTu8ztZGZK01d8bZQSmMK3i9ClGRx8gAlz2f4riNA'
        b'XtspVvhEKj2ilLzokVzBna4d07qjlbxpamnEG6xc6RFzO1vJSxz7YCGicdtfyYsf+6BY6TG1u3o0efKgVOkx7baJkhc79kGJ0iPiNgOVePCyv7FI6RF7u0DJSxq3Vn5K'
        b'Xty4v8FU8mJe+oFY6RF522EcUuSB/UTtGI+USOkxpRtVN2rCEmNbPiETh0k99bIyM38YTvEcZC5y83bvTsf7FsH9Aq8OSWdAt2Z37RWD25K7zJ7QlN7QLEVoVk92njJ0'
        b'utJnRo9gZotmS22rQZ+FTUtx46peC3eFhbu86OzCjoX3LELJxmWE0nZaD5IFK7tDEfsi5NM74zvmdxfdqrhScc8rtU/g06nZYdvC3m/whxn6bRxkwXI3hWMARuyLV0mn'
        b'jHlcq13rAd7f9FDwPOTxnVkdyfc8I7oD7nnG3Xa8XavkpffxbA/ptOrIpil5Afd487u13nC8XXw3XxE/Txk9XxE6/x6vqKegqI9n086SxcunKZwmK/lTFLwphKpqo8r8'
        b'smWXZXeG0i/1LuJYVt+LHtnINGW17Qa9/BAFP6RbU8mfpsAvA00+QuEUruRPVmCH/bE00pR+yXejSI0nfDTS1BjVo2SlXwL9Uo1XBr2IGc83JEHpNyz0Y8ilKP0Shx6M'
        b'KpN8V0Ppl96TmaXkZT9fLF3pl3J3hpKX18ezGhSYCcwfU2b2Fk8oMzMeRuCZtDdlV4osWMEV7FF3i9Gll8WxhfBq+DR4yHwOnGYLcaQcNWSeGFoax46UWWYMhiUG/3sV'
        b'5xmyNN6i6UbJdQNGH9Ed3ogppmg8ArIFg9dvqTot1RYMY9S67X971u+5LRg+NXbd1pVet+UkMMle4AOeVM9U24+i92WwNrBkbg5ogme5qPa2lC2UwxPEAJiRkAqaymLQ'
        b't0nUJHgUbKEzu4DmAF2ixftT/nAzuEioO1B4/YXy7QkrLq+eYUSRczY6TnSib+Xi1MspKkeFRCHtk1A1e8Xk6WlldBWmTloaEMjGO9sLvalC9GPrianjgCbrpoBATWwj'
        b'FTlRIrhnOqHxXiSOOU8Z+YaIPVMTjWnC/9Iywq0PlTkK9Ro8XOkqHDQ3Jom+OstSdXRW0zkdVujh841ulJ+0fFM+j87pqEknDtoIUzeF5dI5fw9DlhFFad/OW+Bpn1NA'
        b'56RqdEkiVVRefqhCSic2LCAxrowWhNV4vpNWTq+ZBFoKiA2dh1S6zaVsSqOWAa6uiCTm2IoyeMYN7g/wxcvUThTYhWxjelGoJcGR+Frcrih0CE+qVln6V2FXBTgJjxrQ'
        b'W/7wdbCZ8CgUXCmHbVaeOohJl9A/cLyC0F8Nb1XCNqxWYfZdxktrB+fS9uh60OoAmzymINH1orywukV+10tEgqDxKbNSz4TkWRRZKYNdgWHIem3G/3nnaCDbcROG+T1p'
        b'QEjpmYM9oGkBvIW3kCkbpKNtI6WcDVjDB55qwHGVAyLc7EIvSd2sjQVHgnK8sI3KgI0ME9gKLxBB0PQH3R5ABs6hwWAptRTstqNb3wUvzAIn9eE6dLOMWoaUbDl5MAmu'
        b'd0NcOQ+u4/Ng1GvgMthJRhPSKff96RZV1ZR7xs9k0iBWQf0FhSmLyKvESPtSfCl/N1uCd2Ju6cy+2PxBOojkbvxX6mp2FHuDjpfD4fjtLt6ff/NuwqBZRUF2bXfUkckh'
        b'U9Y8tF+adPyD9+u+neT/Vl9c22eSr7+busTlHwlPknbtqZ50ht1sUd8fppg75eTs9I89DE8EmXs+1r7PMgjL3s+rWij7hNrWV3vpzd27DgetPRl8zX523RXunacbl7of'
        b'/NR91oOlr+n6Wnp0fGyQW2NnUNAbkKH8ul+xzOj035LKZg1UROVscZxi/+X63ZeOST9xe8dHUBv92dO+jlTujqiPG0sWfHxQ+N2N5vlPFNMUuhkfLQ3Zf85vwYWQg/7X'
        b'TJ3zqlYfufY7tPna9JuHDlV/aVyWX2JbdSdmZXLmP8UXi7+I2f/6k96P9z+sa3r7/YNv5/T8tDbrA/a7AYs194PQeTvMTn/7oeCDfzUvZ9zvOpE//bsTyzdebY2SJ01+'
        b'GDP1IeeHfUU+D59te9c2yyLhN8GyrTf/9uPOBfJKgwNvHkgJq/WIqfno7Nrqcz/YbPKo/PjXZlv5b79pPO1d+YtUW8B7gndQF5PoeS86/RkPD2uCPfAmvEgcQmeL4S1y'
        b'1C/dy90bHMFK90UmksSDcCNRya3glYghuwmeKFP5moK9QE4DVL4Gr9NONV5wV4nKRwjsJKbInOg52IBIw4t5OCBf6mvgAoMyiWKBM6ANrKdPg9VDGTyNEftRHczDIJpl'
        b'NFcxHWCzJTk+wwc7o2Abb4xpqWZXMoNo+Iq9ObAR18PDHpkTFAueYSDJX0sbcFHwGlhHH3FdCXeTU67rmAFlYA0xSla/5obJYxhJIFuejjeFGJT5TLaVDjxJTt7ZRiCe'
        b'IvtPhSOJr6+zUTucWeCUA429CM8ijh5U2WyXTFU2GzwFWwkjIsoTR/snAXnOkE3mBw+SapS+BraPYC+BzTNVlhHcAy4TX6iZYP/cUe5LcC3cPmy0nUE8J0tviVbIgEr0'
        b'9PbGm34efqiesIMFmzLQc0xFBDsqRjyqmirVnKrYU1C/1pNeRfbcLg7JtiNlrr4GxWYywEGmNuFmEGz2HTq+Vwh3q9yHC+E5cgaxCnYkDp8VHHtOEDTnq44KpsPzpN9Y'
        b'qeVDdrczvEBMb2R4T8qkzzNuBbdg57ANqm6Awr1gu8oIRf28gzQ9ygWcHzYe4br5w75bJ2eQiq+Eu0JUeOuwJRDN4gRufS/Y+1K+WmqYEgNs7Jqw3GBEF8L3xH7UZtHo'
        b'37MtKK5Fg7QpTMbYFdFnZfPAiIsPOPcaOSmMnGRZcuZZrQ6tPq4l+WehUrd7uQKkwvVyfRRcn06Gkuvf6d8Z0MMNQY9p6Em5o4LrdY8b3Ol0jxvR7dTP5cu4x63arXrt'
        b'/RT2fp1+Sm5QL3eygju5O0rJjRim6q7guvdyfRVc305jJTegM7ozBsOFvPhH+5GVy+7luSt47kquRy/XT8H167RXcgM7sztzerhh5DnW/JsyaBJy9NBTni1HD/3G1jin'
        b'0+myd5d3r3+Swj/prpvSP+ced1bPjFn/ab6QTud73Knd/mocCFbYB3ej+of3ciMV3MjbqKUx+LG1vBo1qpcbquCGdpsouVPoMnbtdp0OI/yKVnKn0R0x6ndCO13ucaO7'
        b'48kjC7rJyMijdXclarOD3K+H6/UHz4b7eTDE2s/kMWUtMH0WSnEtG4Nb3JSmjk/CrI2dB8MpY7Mh8bhv5IoEhr67b+TSZ2rRa+qsMHWWm94z9Xygss005Oxet8kKt8lD'
        b'lqew1fAez0cec48XjCxL9i3dK7qPWQxBHA78Zx/HeEIxzOIxsISx2V7dRt2WmPtG/D71X7Gw3Lu0camMfVy/XV9p4d3AVkGlyux7uE7Dx1h7uM59Tm7H09rTOh0UTkG9'
        b'TlMUTlO6Zyid4lRn+AtwCEYLqwbd5w/ovASCCzmdMwrA5Si2O8a8a/8cMjx+QobHLAsGwwSfyXklnxG8bClgEM1dwPgWKTi/E2+mb/GBfoHFGJQW4qRYrYsPmjjjCw41'
        b'X43RrAe0h/zEhr7hUyvEH4qGZ8FuCeSULjkuSU6zkfNGA3r5mVHZUWn5ubMy43IGWBKRdICNoSoHdFUPcuJyc4jRRTjw361/PQfMYoGZOuK57Yn5WcMkyCw/aBrquzx0'
        b'oLjW/UaufVz/JxpMbmBd7ENNytqp38injxuIUqyD61JHgFcCMPBKEAFeUWGqeGJMFW91lBV3nOJJUsxs+o3caCQWM7+6uKfaLH3vpzpM/UzGU21d/WlPLdn6Ps/0NPX9'
        b'Bil0+cGIpR/LeGhA2dq3c9tLe6x9+m0d+53d+p1c+10EcifZbPTR4Sgvks0f+eLkKmfLwoc+7F1kUpne0J2tvcypZXa/A76z7rd3kuXKdPqd3eWBstSHdkbWJoMO3Ekm'
        b'fVybVskgC317wLVqzRnUQN8wXLB9e0C7BGX1HtTCKdqUmV27KaYwyMH3OpQZyi3jtiQP6uJ7PdTYVokssGXhoD6+N6DMrHts/AYN8Y3RSGFjfG9CmTm0x+A6Dprie+7I'
        b'czN8b44Ktxbiyg9a4HveyP0kfG9Jmdm2s2SxLcsHrfC99ci9Db63Hclvh++RdWLZGiNjt4QP2uN7h5Hnjuj+oRNiOW4KPvWJMj1yxYnOrtYGqO9zGZS1XcsKeZLCLrjX'
        b'brLCbrLSbqrSKqKfZ9WSKjdXWPv2WgcprIOU1iFKXuhDDZaVQV3KM51ohr77IwpfnyUyffWtH1LoQrt3YFULKQpIl6G110TQqUJJM8plzQYyeGiUca6r+nzsgEE2jNVA'
        b'NhgYWkMFPWGI/tciYAqGo++KmKPvT7FOatEEOVSRNTnsyakzLGYXsTdwhtYLZrOZlEhDBc6hNQqcQ6NIG6Vy1FK1SKoOStVVS9UmqXooVV8tlUNSDVCqoVqqDkk1QqnG'
        b'aqm6JNUEpZqqperRLS6yGWpVEXc/k6RpkisB5VhoST33V2RGwCFsnn/yPJjEC+mYvyyd5WrfjzJ2MIps65hkZYc+l6eLo7oWc4p4anw3RM85dQakPyZt0J5tNNK/pyyH'
        b'aJHDuSwcH7ZYo8hqw3D4h9nGyyw4xQK7ARqHKiU97uc9o8AXMUjw0CN+YblQIuG7ZVZKpLWiaomwoggP62JRhWBUmVE37rkYA5IO5IjjuFYWSCrLRVI6+iqOYFleic9a'
        b'4giaoiopHcSV4FiOCSxajZe6BFoDHGFRrViCz2AO6Kq+kqOU2nRQPZTMKiquHWCVVaC0RaIicc0ilKZdhWq+pLK6qFBbjfvDETTWUOrn54eC6hKnNcx+NmK8BmKeJjnl'
        b'rK+Ko4HEdctw2NyVHLLApq22wMZRW0rTXsVRLbCNSVU/T//nh6xxwD6TKsRSMXHWU6FAD/WGuEIiFVYUil4e6nOYdeEqqNCRyLSYsuogKg406xZNH39FGRaJqgXjxxyM'
        b'4qvOAtMA0fyaKuw5HcIvEpeIpeMgkI6uBe614XrgcLwvqAV6PFEdKvjC8qpSodd4VQnjF5ainywkQW8nDOqqkpvxeUI/5bulIXFFVRJV/AccCfojjiCBpeODxsZP55cL'
        b'C0TlfDf0VT3kqsB7TDBTIhSScWsxuuqEt27+aqwYp/KqiqCXJpyfSnCiMJUEn9Th0Lg0W9DbnyMsLMXBbEmdSKxj9HJPAARbU1AuKlK93aOpZKJrZQUdFhdRIjiw6J7m'
        b'lGpMGJ/HSdLhYMVCFZsLRNIlIlEFP5DvVkTHMxWQ4SV0woYODQw02+k7vrhI1WEBf9RhQ6OJKiis6o5fLSoRSxCH0SiGBjsiTp78GlW31VTg4Kx/AG37vPeWIb2qLpca'
        b'U0aBMRRVtUDvgjiGqsFODKspjSGXUVVUjkziL6oK+wG3pmYNeYyCC3AdDgS4MVLPCDQlE5pO5WZUAz6dHrlgymSLRKpmKkpMh+cyX0wUH+DMUw8ueAiss6/Sg0clHEL2'
        b'Mkefuj7Xj6IyF6RGZrOpmggKo+BmhY5HFnbGJqotHmWpe7h2gzpd0A6OgbOELsbkbplljfEC9C5qTaFIuMtqS3h9HLqxsCUnMckjR53cGriTA5rBWthNyJWbaFN9pQ54'
        b'M0cv2NyGriY8Dq/CreNV1M8f1o0s1o2p5yVdcMQf7iJ0qyp0KCO+O16i19vMz6R7CtyCFyrGI2sudhtajxpF8yo4qQvrHMEu8Xb/BA0J9jS482v1xo9SDJj2epoPHr2+'
        b'YNvmR7bnW4v+0h1Q8dnVL6m3YpYmKRI3Z65L064Hv1/c+SObI/jqiOl19oqTn3Fc3Zrz+zZ4DLqfLVkcwZz7l7zmDz1T/uW96674XJJyfeCb957siQ9478P3n3x5vG9t'
        b'QUvBydaPtx64FblLfNS3wbpphXPr/njJvdoz5w+Uvf/r7djiTe8+WX3p8XYpLzE2sDHpWlr4ynt3rzK8K63WTg7qmCXQISuDEfAy3Du0eDi0chgA5DPZVtMhDX6LcrTA'
        b'42PQkGaH4AMbBvAwOY2RW0GjIakLnwZlV54EW9jwbIE5oTNPgjcg1BchGZSJI2zBi5AlQnrRrl5Q4qEKJ6gJTqH/DjIDfK3JM43oSWR1FC+NymvJ6ii8BNpU0L+wW1e1'
        b'2KdBsbPhGbzaZ+dGKgfOGAL56FVc9MMieBmv4vrCFrLy5u2rqbboiJ4XriaLjmDLdOJBPI0LL2KtngcO4nXi8/CShCxLIzU/lej4XppUGtigBQ44gT3/Y0uXwAsZD2kU'
        b'o2GVLGj43YdLJ1GOLu2FcsGRCqVDEEZE6jc1b5DuXd24WmnqKre/Z+pBMJQSlJaJPdzEPicfjKFkTzL1Wrgp6Ih+UfdMvUi2JKVlcg83GZmW7Tly3pF5SvsAjKtE01zV'
        b'uEpp6iI3vmfqTjLHKy0TergJqkA2bSkoJ4fOuaxxWVOEDFF1poMDKi2je7jRD6ztSJZXIm4vOG7bbqu09/vjrI7ODeyPjfjPxz7pwksR5/DlPL5cwJeL+HIJXy7/sXff'
        b'cNSTMR5+E/SQAGmKEhwL9vcfsSfpJAYjm4EDn2S/Umw5PFy1a/pRXbpT/jMIqGG8omHNciKgm5EmDOHc5KEmqMEV0XrtkHI4DqLSfw0BpZevpnm+fD1n4noeGK6n7Zh6'
        b'Eu1qpJb/Ha7SkC768rWbg2s3gl9kR9duSPV7jon/DdAXOx/pqS9fs/moZo+HcYxm7ZtF19CKrqGapvu/YR47HymvL187IeZbD2OIb24jSq9wLKyX5L+u4jBA1ZDa+fL1'
        b'LBrdv5Z4UVJNX/0fdS0nf0iHffmalTxfM9Svw7qwWs0ETLIcTC8MDzskphey1OqCEc6JRyIJZslRcy3WJCY4jrLBIQEtcThL/TqDYr1hR2Ot/5mjcamA+VTDZBwjPKqo'
        b'CMdXqhAtUZcP9I69VKSlOGQy0ZnxCoiwqAgZCMjMEKosThIwCYfD8OSXVFfWVNGLIEJ+YeWiAnGFEEd0eo4kElT3YZA4d0++uzq8HbonCHooU0FlZRmuKl6oITYRXQ3p'
        b'sqpXWDcY/qFwfk7lImx90us5OCyICltOWFBZQ8ePwhIgKpqIN/gvvrKaL8IsKRIXFyNrCY1UtB03ulEqfpOYUohtJaqgJ+OYUPgPmYWFwgpiFb5oScAvWM0Q5rtVVpF4'
        b'WeUTm8TqfKXNvecGCL5bVEG1qLC0oqaiRKJaHyChT8at6IgcSCTikgoiCt6EJ2qEVVHU+GL1VomRqYzM4nGpDpnAfqSTg8OGLWH8S34CT7wCxy8SFUjx76AchchIFeOb'
        b'womMdyKVYlJeIpIS3oWGvYTMxGM3bLLiN/ZVEYsk4S8tc6iuYqmKAM13kjK8kuCWU1lejlcPKgV8d/dFeHkGNWeZu/uE6zykxaMo0kkjJBMQeyu8fBLRvFTxKqRpUD7V'
        b'YkClhDRYBdT3UuXxy0mXVn9dvflpw+sc5PWtLFgoKpTySQ+O/w7kZIQG+/qpVlvxYir9dnq/XDVGudWHj1lvqq0UF4qGBT5aVC4qKcb5BPw5fv7zXoakv6oba0R0c8QV'
        b'pKL4rY+NTUubNQu3bLwYc/ivSrhsEYlQJ6rGE58nfxHi8/CqilqF/F9cIVX3YJyM0f2FU0avsdFvi8/QmzJutWj1Lxo1Er/7mAb6+QDfCX9+FJDB0Iqj2muCUtEbWSER'
        b'05WqLB73V4VFC5FkEH7gAiRMn3Ap/j7+2Dj+WuUoIhKy2CouLJWKS3BTJIWl5fA6GsnLBc+/sxPS9OIjucmRimrQ4DpMAEmwmK9iERqhFqE3Li7PK1coLRDhBeyiCSgh'
        b'caHjXJXXLCoTlY7Pfy9+wJhs5NeENcXLa6QiNHPgGJH86ZXVElKpCWgEhvOjaopLRQU1+NVDBaJqpJV4fiuboEBQOD+pokhcK0bCXF6OCuQtkgilyyVjWj5B6eDxqvzq'
        b'DAoZj4xYrVqLXq1aoePRezW+hBFGjrD+Dzg/bmIuLcl4pXlMvV9ZEtWbX1yNWuOGeTtcJ2HB8poSwcTip16cH+I8sQCOyugXNlFOJGYVPsKJRWo0meCJyAS/iAwSiuH2'
        b'vYBGqHq2CZsWNorYOO2acEJTAa2gEU71jegDSCdFY+vQUO6WQ8+xE07YIzgu4fwYdMOn75CO45aCbkUV6H8k5nw8B4VOOOSqIcCMJuM/hoz/C8kQsBh6ypgeleuVFMt3'
        b'y8uRok883wRNWGwYXIYuGpdHRmqcwHdDL7lKxFG3T8yGmmqkIhei2SJG9c2Tr6bbxeVl891mwKOl1eglRXUJnLgqarg2I8SGk1WVGiIlKaupljxfqRepexOpl0SVfHnN'
        b'b1hFixq1afRyOgxB6gnnp+MP/hx/33kvX8yfLuZPik3cG0MQQCoVUnWPjfEXyQHBB0JF8AfK+Hy+iUexRFF1dYVPfLWwBl3KvX3ixUi7m3jUItknHqswnYnHJ/wDEw9Q'
        b'L/plNCrFlSIlDI39Ew9NpG5IZysavxoTMQ9psSKRFGsW+BMpWMEv1O8KKpeG8/EhBaQ/FWOtFSUgnk/cqbgQBl6iSwnL+fjmhSUKxVL8QqLrC9U9Gm0K56S/EMKeWE/3'
        b'CvALDkaSNnGdMNATqhD+eKFEFgtRa+PRoPKiTAQqCvUQ/uDPCZ44o2qYUw1xL5LoIRCrcH40+kZrwnP8Q16Yf/jVJkVGbwq/kN9D0FiqknT/TDxYY0AspKJFR6Wj7pl4'
        b'RCwQFyKCSTHop8d5I/8gULVqYzZuLou4O/m6MM1vzmXSR7XgWXirBB/x3gZ2qYGMYISRm/AKKfeVEx1cxbe4y/5Tg/k0hkrFSriORj5hs8FusJcBDolhM71Zm2FOeWJX'
        b'pFXtq55xFtFgJLPjHaa6qAJfe0tgI0F28AJb4K6UVHgNbBoNJgVbwE5C63XXFcQ1qnNRKHOP1JwiICq60/09UN5kHNwKuxCAU8lpWYmoJRsxuDEFu0B9NrU0kFOyIINg'
        b'L7gaYRzjxCgGwTH+zJFH1WBUUDfNbFifFgJbyVanOooxJpNI72ipAxnD7aBVTwCbwUayoyI+sepnpoTJoKhjNrHNmdfSYaTR/qmH8sNcpwZyj8oOH2s3NPvK9ZsZsbwt'
        b'oOsvsedyek7XS+tsFbN+cfxbk4/AWzDzW+m9Dz/8/vsV5vlGN45ddPB9uq/5jlVuxuHerUfmeyR6+33nQfnbcefmpXya8X3ArmW733gYlByduV8vp/exIW/WziNf3/HO'
        b'u/vd4KqPOh5Lvvyl6Maeo9vgO8KffeQt4VOXv3Njr+HCf/x1181Ym4tOca0bP9PPM/zh3f5l9z0efv+PD4sLFko+K0ifUz1zY+LW5s8fpd3acuPXU7NTCm0rfmb+s3r2'
        b'Bm2Ls8Fv24UbCTfPub8xYY/86wPnttZPP2DtF35xhn5QX/xHpd/8vm3FU63cU7FTDMIE2nQgTzk4CDuJv3xTIdwy7C6/H+wh+5dOoBXeVPnLs1PAnhIGOGcPd5NnoAOc'
        b'D/GAWzJ4/CRwik1pljMdwM1lNGpyN5CBY+rbr3kilb98Cdj+BON6A3kgaAT1S8B6t6Q/2J3MhpdJ/JogcA1cGAc5eR84QEMng0OraG/9GqEEi4GXG86YVQF3YrePBhbo'
        b'nGn9hCC3rIdt8ExKahISkrYqZjbD3d9PYPi/DNCI8Vb4I+7vY/w59YbXvIc84JNUIUkzbSm+5z07X/liHFbGqkWqMHXst3Ltc3Vr0cOAoE6y2nbPTtZ9i8B+V4+OnE7T'
        b'zqLu4K7y2wG3o3uCE3qD0xTBaXcLlcHZSq+cHtfcFnbL9Fa9Pis7mWbrlF4rT4WVZ2Nsn5mtzElh5kLourfgx4fCW8PbhjN8hXcmpyktI3u4kTj+21x5WI95UAOrz9S8'
        b'pajX1luB/pl6E9zmXisPhZWH0sKzU+OeRdBntu49HulK24weXsYgk2Xm1+8b1u3U4xt32/Sebxx2bCDet6YKntegJsvYq4/r1RDby3VScJ1kOcQfwkuB/wV1spXcoB+f'
        b'aFHWzo8oBqJj6yGPUdr69vB8/z3IQgn/fqJN8ezRM2OvfktXOUtp6dnD9cTPjL1+JsC8wN88RkBBjl0sEhEBJ2YaC/prx4SzYLgG+n6HyYnlse7oaseasu6YaqDv9K6r'
        b'Ib3rOrKrgN2hXsmNd4wQjGy7vlAIFrLU4C6zrBgMv2cUurzK0Xoc0Gr8iB0ELZ+titihUUfVaaoQo/+3UTtKBMzqb6kxUfnsnpvenOnp7d1attSHQUPYhxW/Rvtqgo1a'
        b'4HVJTVaQL0ZmyoGn0FvNWAkvx434+sJbcJOrLmLXDAq01syAx82Io6pbGTidg4uBm47YJfMaBS/ArRLyU/+Yt6ImnzWogQEfS0JdVWh5G8BhKMeuueYFFNhLicwktG9p'
        b'ux84jF15V4GdFGimCuexCZG3VmoVtzFIUBE9bbHKY/dhlrF5AyMSH57yzKoNoX02m6uMyvXpxPLaxZPpnFNi9XOrKF98dsnzY3YpnfNOjf7cTSySWP7pnHQ6p7aPbmYJ'
        b'ww0f80n1T3eic363UifiIUUS9Q5FGtCJORxNqYBFV6nbLYl2swVNTlCWk5mZmbwY9VAsBdYudSMNm6EvDfD19Z2MeoQBj1JwrXstcbOFm0ojcjLBHmsKo8O8jh6sAgdJ'
        b'b+hqBww5/7Ix39cQ798loJmUmwc7OQG+U+GJIfdfsBvuIcoDPGypl0PhQKDlsN3er5rm9w24BuwNIF7XZcX+YAs4Rad36oOtsIl48sKGHC8gExOIQHAmEp4a8ts1AKeH'
        b'HXe7YT3t11vHgmtyMvksuAUcQfnPm2mCdrgebCOAZzoRQK4WsQBpAUeJB+/qhbRzLeb0vJmc+J+ZfPySph41ZtJMda7UNj/HohP3uk6jmerEA/tyMmFzLYZdhespoRGg'
        b'laeqmWahXzIzsRSvKKitUsHf7Q6nEEdlgsQSigpfqQvbbeEt+skVsCtJoh/gu1KHjZh9koI3/CLEv2zfySIOvBc/X38g95106Gt0YPGuCukxXWevY57RK9gJv60JuNzo'
        b'8P7pG7nNjh82L3+w7se63yaZ/L7mwFuaX7UnJx6baXPrmf+/5/xokNEQzRRUuJv8kqB5c9HeQ88Gt+60ozqMOjnNfX/+0807izzOr7lodObpZP3dDYovluskyhfMY3QH'
        b'/J45faWnxrkPZ8Zs/SH1142akvxlNzVm/jman1mzMUXyyYWdjTuuvvPgu8mNb38hrHzcHXjtuy/ei4Di7rnWxnc2hbndLQ8vfs/3Ym9eRHJ9Yd5A+rHHMaLc7Dfj0ucd'
        b'yeZ/emPKp29rdK7cfkCWZfPvxDBhH+u7DMFT8away69v+Bdm/mP9jUcHnn3zbHdLxTH77d/E/v7W67azV//TI/TmwcO8d/nf7l7Ode06+Y3Zl1/c+dOA6dPcymkxMkGI'
        b'WMfLO06j3mvazoFbZV+8W3u/9fHy4vCtH/4+LWfZ9greV7/snr9g+9fpJbGKlEsJ30e01x+d7rna/dPFyzfPK/5U11Z2cAVD/yfpZ5GzBVyijkTAE6CddoEYo4uAHdqj'
        b'1RGws5h4n4aA6+CMB9Fx0LMkcEYbXmOCRl3YSXQMrxngCtJ5U0XgEoNi2zPAAYk/UZwmg8N5w2EaYjVIlIZUQLsFgy3xUD7s93sYblE5/pbBrXTwiPWwvjQlFXRFPO+X'
        b'y4/T4ITDjeRwWYAQKWD45BkXY8zRfrlQBhvoHzmDHnaNBJ+B63OxZy64BbYQ7Y0Lb6HWjz5fB9sdsXMuPG5N2i5IhntV3sPEdxjug6dWIf3vlCnxvHVbDW4+d2zOmQUP'
        b'TAanwJos4hdqhZrXSXRL0AV2Yf0SgzHVgzqiwmXOB2tTVE63czNoNCUDsJ4V7QLbaVCjNX7wuMpzFxwF9SOgRuJVpBV+8CQ8MUQCHIGbCNiSwUpWLEF8IlBwu8Fx2DH6'
        b'DB3sYKGXVI4GntPgAKnonKTFqmN68BjYofLKhbvhOfLUPwGuGQmrkWlM3HLhBtBIn+PrRIPezecO8kWxQn3BmWzQRcM4nUpcgrgF5DpjDyOSo4jgWoRA+6V1Djwo8fnq'
        b'B71wbPLlRiPKhiS/SFxIhwnuYKpwl+yoSVYNGjgEoW4f36mX76vg+9JYL738sIZEHINj6f6pOKiHDV9m1jZbbt86vyH+gU8IjutxcnVDXIubbLrC0kPB9XzAtaOdOWXV'
        b'x5e0L+njWfXxbGXmrYaodC/PC6l+nUj/C7zHm9rNvceLu83FoPa5x2e1z+pkKHn+vbxQBS+021hJwGQOGbYa0oXkQiXPt9Ok07SHF4QfGLQaqMJ9ZCl5Pp3MTlYPLxC7'
        b'QSX2WvsprP1Gk+qO7o7p4UWS54fSWtOUPPdenq+Ch11zebRrLi90bAUjuy3u8ZJvx4+bXno7sTc2TxGb1xs7XxE7vye/RBlb+io5beh2z2+f34laENLLm6pALEGtjET8'
        b'ajeVzTxio8CRTWwIB1X/cANiyYlFA1m1nNHDc58oERHp4+EwLINBVr7mjykrN4tnwRTPtrG2pVRp4fpDiJWZYNCQsg8fjGdQdg6HSltLZa8pbQMadPtNeQ+cXI4ntCdM'
        b'yGdCeYLOIc3qdQ5WOGPHYF54Ly9SwcOOwRj3aUQWhkRi0JjjharHcbZ4ZjJSPbnHQ1OOczCSK5fGtEEuxbNp0Hs+csaLDz6SyBl//CJ8xRqJgfYszu4V/VkzsI3wmBoT'
        b'CG04Ci+J2KKhQkFnq7ytcEA0zWEE9JFgBv+DcO3VP4zVv58PaKCVTiPLssAmj0SkH2UmoikMTVSgI7eoIBGchnWe3gJNKhFu0qqakkPgUgsqwDnYBE6SQ86scm24gQHW'
        b'wSu+BGUH7l5o5qEF9i8geCdwSyCt6VxD/x2Ht7Q8MpgUIxtZ6b7wknhB/AKG5Gv02NyxaWNWlw7wNbqRUlDGNTZuPJx+xtvgtzXffD+3xysn3uxEg/dfTKrMph2e9q3Q'
        b'yqxgof9XS5/96fMb701dvmbRwsGdX0cUi9aKpC0audvDP16VeqJ7jyIiebO79BuNRSmXV87LuhGW13Ogav6SX/cX/OtgmWbwuezFn7q594ZZ9tyoetPs+03UnPjUPZL1'
        b'V/+FlLHrC0TbqlLYRpVGZ7ZUGfz6Zs/bN387nHDi6I61g70fPNom+HLTJWOtr3m//r2gRdKxod68QdfxyZ2/KdP/lNPR++uAIrnH4HXfzaxiPXvnbT0fbDne0H49gqHd'
        b'GnJnu4/AkA7MdCYJbCO8RkZZCJrlTjPQHLx2Og3F0Q07yLCvcruEe32RwsFcWetIyoaA4yLydAuGt0hH885ZprU/vE7mWTRl77ZF5drBBvTcO4lkQgoIE16HV8E2Os8Z'
        b'1BE34HkTsB9eWKJaM+GA40w0J7YBOZlMQZMEXkkBN8SeGOphSyrSCnQjmbAFdsFuorMUwENhWGHwyfBCtVgFb05lulvAzfQxdBFsRTMgH9xQD6LFKqkCh+mD7jfQhFuH'
        b'2pAEtyNFSXM+3DeV6cifT2oHzyB23PTwgceQJrMVKV/eAiaaxg+xwEbU1GaawHHYHZeClQmfdA1KcwrcG8K0AFsW0A83J3ulDAttymIOlwna08Fa+uEhcKsM1Xu7in3R'
        b'7gVMXtbQwwPFS0agKdlh8Fwm0rRKY+guuwQa4OseKmhKTSCvhbuZnr7R/zUg4tBaAD0kaRF0r+EhSSKspQNq/UTRE3OyPcU13xvSGLI3ojFC5nTf1FUefTahI+FsWkda'
        b't9N9z2m3o99OfiP5rvR+bO5nlvY9DiFKy1CMMoFGZ71WvTYDNKmbWuwNbwxvmtJr6qYwdZOb3zf17be0lznJWfK5Ssvwhpg+F4/jZe1lry9q1WlhtxShURqXleXKAz/m'
        b'+Q6yKNfAB1yLvUmNSc0pD6xsDoW0hhyKaI2QO9238unjWR7SbtWWcfcbjKHSb2Mvczju2u563LPdUy7tzFU6hHfH3reJup3dZ217KLE1UZa7P/0Zi7KNZvTYRD3EP/OF'
        b'TRT6+rMEH9m842USp6Pxpo5GnClHPQpy9ZM/HPlpftMxj0dhGozDbTu2Gpbaa3wGg4fDHb9K4C4SPEnAJgsUdFQOEqlDe3iyYpLv6QKTsegGOgxKHeLgJU76n2CQuIxS'
        b'0SIJjVHwaKhZAuP/4eqlGhcx39aM/aO5eRZzc9i71x5Po/MYBMvgIZutb/RIjzIwa2e1x7Qs6yp8I+cd09tJ/ZOsZR5XTK/kdHPeiXnCYhhkYWCMiEjGM5arvstjDZLA'
        b'Rl8fZjOGQA6CMchBKAE5sHLsN/KmgRCsgutSRkAOgjDIQQgBOTC16jdy6eP6oRTTgLqYkZQInBLJIEmqYr64mL86WsJQyiNtVPdBimmQxmiVdJk+JN8GLKz2xbZP6rUP'
        b'UdiHdHMU9tG99okK+0SlfbLSOmXA1qE9rNcxTOEY1u2icIzqdUxQOCYoHZOUtskPWQybFMZjisFLZTxkYVrPNGsY+l5PKHx9rIVTBknKswpWmL7No1oG+v1Wx/v6ts+Y'
        b'XH2Px8j2sXuIv9E++9ju0IAblkhoazU1FdmrGpS+JRM2mc0VMNLFet96MSSxqDP+WfKdqPGj9PWRRm+VrN147Mlqse7pjwdurtuyxCdi/TOOReVArPMPBft8H/T/aHS9'
        b'aPM/vBdlG2w4UHnzixWTf/HSvTyoM+vHuEz56h//sfFBZOvuz2evWZV5PYJ5fdqBE98cnVsWNKPM8NSiU5v+JEo4Irvg+vmNgVbT22YffeR8a/31n6Zf6bGpjtrXG/rF'
        b'4QNlB3izP9qpPSf942MNPwce9ksrTQ7Yl5NcNlBkHK+VJ9A6uPZpy3ecjtSCZ7LOGZNd79leWHWI871k5aD+xdYZy077F4mk7d1/Pf3J3IPfZ212+Nrw6S99TomlSSEX'
        b'Dk/OvvBhgXWAsKDkk68jXlu7OOzuSpfkuZmHXNMMhWall4q+/ime4+W2IHtDgMsHXh2P0na5rK/MvvNW47njSW9EDBQ7pva1zhdV3Vyge/inkk8PlId83tUWUfmLcuVa'
        b'Q+PihC9vL3z3X60CFgnLhOanEythPTLfIk0YoRTcAXaA88TSlNYaj/Y0QxbnaTpGpBweJtMcJyRZ1+v5rQt622I6W+A09uXTfuHl/+JV/w8GByd6Soskf8+NEmPGiwHt'
        b'/PzySmFRfv7y4W9krpuK5PQ3NNcFUvpmg2wtjkW/oUmDf/2SFvutK1olMn+ZsD2obbk8a9/qLqfO6m77rprurK6l573fiL1rAhPv+ad+xrNs8W8Rtga1cWTJyGbqtEBm'
        b'X8+UdIVFek92bk/edEX2jHsWMz4z58tMmip6jJxwTL6ZjEEdyoTbENVoVhf9LNCY4/QDhS7P3Fw5Xs8odPkhlzGFY9kw/QmFPn5YxXDiWLaYP6HQx2A6g9IxesasZnM8'
        b'nlEj16fkil5WHaNB8nBQyqF4LnJdhUVAnd5TTW0O75l5NYtjjbKj61NyHVyoRYhlEzIj10fkSog9JA9/HIziMThJjH4Tu6N6PV7xSn6C0iSxRy+Rni+3RvFitak72qax'
        b'VqqtDJsBZn7+f7h18X8jL3gPecHoTbHxJhZjJp5YhmQE68iSaIq2z/wYDCO8MUJfsF+a0au4pWGd4IRmOHVVN0qDJc6depktwdHLjD45LtqWpAMyeeu/mHJ/ttEbHK2q'
        b'0MYZbjp/vXHgvaumv/34rzdjliYdizN6/+uUxLuFcVsDJ5376m6OLPHNnPvnzJPmxnlYev0m9ct/tmvq2XPN23/P/+TvJSeXv/vb51Xfl175MdN179STZwIEX92N0DKY'
        b'd6njLiv4StHnor2brhS4anAD9Tw1q9yy3nBcsMHPpaVgU5j5TIeC7fo65V3QdrPycJnzD5dv/1Cx0+HgF8fqvN9p1kEmBWZjKlwHTmGNPCOfgTfVsQuzLjjHhPI4eJrk'
        b'0PMH51My4Hp42gup8VsyMrDqbgyvs0C7nh4Zt0TIoLsC6sFOuJOEztkOdmpRBiagexrLduUKghsPusD+nJSkNPc0LUqTnQfXMLVhpzF5FAZaYQOs99GkgGwBIweHBDoC'
        b'6KXP6bA5yCNZg0JWySVGCgVblsGtxM5wzQMXETXwOpAjdX5bGkYb1xUwYQPoDCO2hDVcA3dKktKcwaHhDDpJTNDpnUUvXW7SnJVCZj0axdwAbs0Gu1npTFhHBum5znEp'
        b'SXBnOX3QgYH0/064jzRWDDsw4CHS58G5RYkqW0vPlAkvgD3gGOHYNHAsCiCDwLMWnKhS5dAB55ngggm4RpZfyxCRCyjLOdClpQfqliyugecX6y2uYVAWcCcLbFsCd6mi'
        b'BheBCymYBFgDbnkkpeFAMbpgHxMeBudW0hFKO+FOd8x8nxQ0GaC2wp0BFvhei7JyYoP1oKFa4PbSE8L/l/OD2pvvRmaKyKG/F8wVo9xTtUf5Dc9Gl9/RKPDYktIw7dPn'
        b'9urbKvRt9y9V6rutie9j62xOXZvaY2x/NPQ+2/NTtj769znb7gu26xdsr8/Zjs80ZxtpoMF15PqUXAeX8ik97poMteUluwFWuahigI19mQY0pDVV5aIBdrlYIh1g4xWj'
        b'AXZlFXrMkkirBzQKlklFkgF2QWVl+QBLXCEd0ChG4xb6qMZHH3EQ9aoa6QCrsLR6gFVZXTSgWSwul4rQzSJh1QBrubhqQEMoKRSLB1iloqUoCyKvI5YMIbAMaFbVFJSL'
        b'Cwe0aBQbyYCupFRcLM0XVVdXVg/oVwmrJaJ8saQSe2cM6NdUFJYKxRWionzR0sIBTn6+RIRqn58/oEl7M4zMBhKslSx40R+fP9IR5ILDhEoycB/8/jvepTZmMIpYeBwe'
        b'fR0k11cZlfH09YaWZpQF9YaFbpQD62ftYuyQVFjqPWCUn6/6rpoNfrZU3fOrhIVlwhKRCulHWCQqShdoE5tqQCs/X1hejiY/UndsdQ3oIH5WSyVLxNLSAc3yykJhuWRA'
        b'Lxv7RiwSxWFeVkcyVd1PCwKtskxZVFlUUy6KqI5n0q6PJLDsIIvBYDxETWMPGlC6+mu0HrHLjRjcwfn2FMe4V9tKoW3Vknxf27XHM+INF+im8Ezu0zbq1zHvsQhQ6gT2'
        b'sAP7KaMG3seUJfmp/wej2a0i'
    ))))
