
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
        b'eJzsfQdcW9f56L1XAwFi44GnvBEgsYfBC0+EmAZsBztGAgmQEQJrYBuP2AaMMWDsgAe2470n3jtOzknbpE2btEnblDT9x0nbxHHSNm3TpGmbvu+cKwnJCOL09fd+7/1+'
        b'zzJXOnt83/nW+c65HzIu/wTwNwv+LNPgoWOKmQqmmNWxOq6RKeb0gsNCneAIa56oE+pFDUyV2KJcyunFOlEDu5nVe+m5BpZldOICxrtR7vX1ep+56YXzFsmqa3Q2o15W'
        b'Uy6zVupleWuslTUm2XyDyaovq5TVasuqtBV6pY9PYaXB4sir05cbTHqLrNxmKrMaakwWmdakk5UZtRaL3uJjrZGVmfVaq17GN6DTWrUy/eqySq2pQi8rNxj1FqVP2Sj7'
        b'kMbC32j48yXD0sGjmWlmm7lmQbOwWdQsbvZqljR7N/s0+zZLm/2a/ZsDmgObg5qDm0OaQ5uHNA9tHtY8vDmseUTzyOZR5aPpVEjWj97KNDDrx9SL141uYAqYdWMaGJbZ'
        b'MHrDmCUwaTD8crkgp8wxpxz8jYC/ENIBIZ3XAkbum2OUwO9fWDkG4maNlGqy3kydytimQCTegzbhLtyKW3Kz8vFW3J4rx+0kqCrKU4iZKfOE+EEGOi5nbWRguA0fww8s'
        b'qmy8Hbdl4zaW8VFxM4JQD76Ce+ScbQjkWZsjSkGX1KoolYgRCll0CN3A22wjISUGdY9Tq2I1USoFboHyIsYfbxPk4Gv4OpQlk4evw6cZteJtUbXQiTaowgdd5fCuXHQN'
        b'n1lkm0jyHMObVkGWK1K0ddVKG766UrrSxjJoy7phuEOA2vAWfA+6Oxmyoo34NupGragjWq2IIH3GHSTkxYzEL+D2iULUgM5llLEuGDnSMXsaAj4eeMx3A1/5SDvo2K2A'
        b'ues5AB1LQcdR0LEbODvoKl1BRxof2g90Y3nQnRwiZiq1gGYyjfRf4xczNDLRKGCskwLgl0a6PmUIH3knQMIsKZ4AcRqjqkBvz5kmYjauh5pnaYw9gpXMGcboA9HysOHC'
        b'vwYzs3bI35/yZ+5GbKIYM0ZvSPiRsJudtVATAPnjfm2uEK7lo6ttfwl49RnlWC7vffab4WvqJjG9jE0BCXVS1AHgao3ODw/H26IzFHgbOlMYnpmNO6KUKkUmuu2TzTKm'
        b'AO/p+MBUt+n2dYx4Fj/d7iuFIZNd7uucTm7Q6ax4ciWI+02nNMdMWrWRiUatK1QFC7PQZcUijuEEDH4B7UZXbaEkaT9qx1eG4f0FUM0EZgK6jK7bAiFhTlpKwcJY3AbR'
        b'lcy80DAbqR4BTlXhTVLcCXVHM9H+aKctiCDqroDqkZW4E8arYBRpqJkuD3QPNy4syA5dlY/bRQy3lh21Gl+hSxEdsg4jSB+pBjxtycoPR2eiMory8Dn8AFaiEp8Roc2p'
        b'eDPtIb6Ld+Lr6PBadBVGOY2ZloCOG1JPp4gsRyD1xW7zsz8e549mBTY97DbcfG/eor+GjmJbXhkX8/7kxNNJQ7Ze0P74w6HvNTYEJjSX+nq/9sHkv//mULrfyK/Koy/t'
        b'3F2lPvWD/Mn73rn6s1/5V+mX5I78ZGThwYebpWlD3oivOqLv2h2X/NqQn1hevRv8tipuneLn88+F/2rL9LrO/3mo2f29kujwGf+KXz/0woe5P5itWKT+6cL3I7/88aa3'
        b'fzzJ+Nvpt//gt25B6vHJp+Qi6xjoZx66jI+ocTu6hZoicXu2IpMQjWB8S4Cb1WXWMMhSgO6lRmbNyFTgraqsHBHjiy5zsHZPy6xkpaIb5fi0FG+JVMozI+00JQBvFNTE'
        b'JFoJUc4sLPdFZ9BddCgqwwYUYFs0xwThOwJ0YfJ4KyGU+B7nB3O+DV+z4A7cJmCEU1no1D5CkXq5cLmZoI7cl379Bw+ChV8PnVZurqnXm4BdUEakBCair5vR62fWm3R6'
        b'c4lZX1Zj1pGsFhlB3RkSNpiVsD7wGQp//vAh38HwHciFsmaxo2a5oFfMF+71Kikx20wlJb2+JSVlRr3WZKstKfmP+y1nzV7kt4g8SHMzSef8SeewjBOzHCumT9s4EvMA'
        b'H0A3IzNxu1qlQNuiYdVvj87Mk7PMJHRZVKISOtck+Se0f1sq4aEnHB+4vY4tFsCf0MAUi+BbrOOKvXT+zUw5qxPqRI3exRL6W6zzapQUe9PfEp03/PbhGWy5QOej84Ww'
        b'L4SBhEBYqvODsFTHUsIQ0CteSCcqh07co29gTZYJ7F0ho/RykIoYxsG1oRKe7gi2CoDuCIHuCCjdEVK6I9ggtNOdxifpjqAf3RHyZLxMIWTgW7ZxUUXU/vU6xvDr2aGc'
        b'JRdSimQTHmteL/1Y87xuq/YTTVvFef3HEC5+aRnu2RHblH/gyO6gV3K1p7VG0Vn2rOaHwp1Ro6XzlKPbfJekbfxkeNjC4ZvDUt5i9q2s/UHg+qHPycVWwk5rAPOvRTpZ'
        b'XySwzlYxE4BOCupxM75Mlwg6gRpxN59JBj8hn4CRRgm8UIMfXYGT0NESNW7Nwu0quZjhUI8EbeNW4wdG63BIHVNUQ2iWuhTdVaELQHNTuDBYSZeshMTGyMNQay4QiSiV'
        b'kBHhAyy+g88+R2tFh8ZkRyoyqJSA96LjEnyNQ43PkXXngocCTwuKomWvpKTEYDJYS0rowpGSuS8OZMlHzArZ+gAe3kpHLn7BiHqFFr2xvFdI5Lherzq92QIin5nAxuzN'
        b'I769XYLsZj/yCHCuBNLIUudKOBXoshL6tVfGuSC8E7uUduwq5+y4xVGeJgDc4ihuCShucRsEnqQ7ZgDcsskJ4g2p8KWS23bgw7ijAF9WZPBQy89bSFjcTHxEHDQDHzfU'
        b'LvQSUTz/0y3pYw1Bs1fLo4MjtVnaTzWBZZXlxlLhtliF5g+aJa9+9uXw11/q9mcOvSSp/6JFLrQOg2LaUrYPH/D+CooPhRHW8aR7k6vwVdyCmvAFwIIOpaLWTnVHbBCi'
        b'Joi+TbEGH8S7swlqAGLg47PtuBFVYKXct9kXXVPnKliGq2Nr8Nb0MegYDz7OIyYAyavQWw1WfbUdGQjFYkp9WClbH+wEizMLX5WQArdXaNJW6/vDnzMHOeFPQU+Yf5kT'
        b'9If8XUHvoY3/Gm2pfCr4R5Ip3b0Mb/EdjS66IoEHDECHlIbL/9PBWuKg0N5fZnjGgE813LY4W8w7McdjhPG1J6vmsMwFg2T5I5CxKOOdhdpQlxqk8BtOTKBogE6EWGWQ'
        b'PmpszTSANqCCBzTA9zNpJfXoDD5CsQDtxQedJAJdwJft/G3g5Q9At/QHesUTQLe4A13EQ5TAtldUpzXaPIBe4AL6ECf8gxki8Tngvy/QM/ydzXle/XE8/ImMy5YLn5IC'
        b'uEm1rL1KdwwQ5dhi6LoBqXUvUbwK8VaFQpmfkVkEq2d+bgEvSWaAUKlkGSu+7y3G59BuWwQUygft7AXfwXFm6LggK95jmPLxIaElH8r8aMLex5pPAG+M5RFDI7QZWiNg'
        b'zPm8TzS12q27zupPaz/W/KT09fLoh3nPh2sztWe1gWXMa8MyGxte6R7WY42J0ul0GVpJ+ftZAmb98sAd094AcZCwovnoVo4v6aqrqIY3s+iCxkgpT8QkkdoN3yajPatX'
        b'P0Mpz0TUleGGb2i3yAXluvALVODLkuDtdsLDiNApdI5HuWZ8h7IlvHM8uuzgS5QnteOdqDEszIEewgHlPB4vxbZaIt71MSWjj12WC2Tr/eyYwudxJUQ8v+lDxicxHyhS'
        b'H0eiGEkoZbUTI3cFu2KkeztuCpc7MaLarZMYsVvZQRUsN0FH6BEVBTmGo69mCKhME/BQrNZOejmj4lNAlR+WVpaHak/rT7/JXQkbFqPQEVxp0Z7Vn9dzryk1F7XLXl3y'
        b'o2W4EOdhI84LD/nJmy8vEbw9hHKf7K8Dq37LAvchRAPvQCdRO6ABvlHpSnkA53nB4gHehDbbQVyQ6BA7TiRSiQS3TpiEW6NUuF0hXoL3M+Ll3IR5S/mKn68DVYvIMkSQ'
        b'QQ24gwozoN097xnqg5EnkMctVrOdNBFdm7EGsqFAnIA8+ffRC5LFQer8vgUDWBfgE0XS5gR+uxs5eqJ6OZdjJlq23I+ITITdgZbgU1LCm7/gt7SkZKVNa+RTeNooKQO0'
        b'qagxr+mV2EUkCxWDesXlBr1RZ6GSEOWJlDBSXKR9cpDZQRUifghkUgrIEEhhCSdk7R/OXyIVSUWBEhtZ8RL8Imrx5VUKVryKkUg5DX4x0bNKQaQrN5WCKxbqBESFOMAV'
        b'i7oYnfgwqBBH2AYW1AsJ5a7eveJ5JiDaa74OnasvNVhrQCeLVpv1Ov7no0C69h6RJr4OXqQ319sqLLVam6WsUmvUy+IhiQzma2mW3lpv1cvmmw0WK0QS/eLR92GwX3TD'
        b'BKlrTNaatByYYFl4us6st1hgek3WNbWyIlAIzSZ9ZbXeJE9zCVgq9BXwtGpNOo/lTForvmc2KmV5AJ4aKLuoxmx6mnyeKqvSG0x6WbqpQluql6e5paWpbeb6Un293lBW'
        b'abKZKtLmFSmySKfgu6jAqlCBQqVMSzfBhOnTCoH3GaPTq7Q6pWyBWauDqvRGC+GIRtquyVJXY4aa6x1tmK1pBVazFh/Sp+XVWKzl2rJK+sOoN1jrtZXGtFzIQZuDmbfA'
        b'd73NpbgjULqK9I6o0jJ7RyBKKSu2WaBho0vnZbEDpsSlqfUmU71Spq4xQ921NVCbqV5L29Hb29PLFuB7RquhQlZXY+oXV2qwpBXqjfpySJutB5myitQbbo+SO9JkC/SA'
        b'O/h4udVCRkmmtH9u2YIsedo8RbbWYHRN5WPkaSoeT6yuaY44edp87WrXBAjK0wpgAUMn9a4Jjjh52mytqcox5TBHJOg+aySmiuCwIsdWDRVAVBY+TmwXVWTW+OmHSNXs'
        b'9BySpteby4FMwM+Cxar5hYo5NQAb++TTtWAwVQKukXrs056htdVaFaQdoDelSnub9t9u8+4pnsy92yDi+g0irv8g4jwNIo4fRFzfIOJcBxHnYRBxAw0izqWzcQMMIm7g'
        b'QcT3G0R8/0HEexpEPD+I+L5BxLsOIt7DIOIHGkS8S2fjBxhE/MCDSOg3iIT+g0jwNIgEfhAJfYNIcB1EgodBJAw0iASXziYMMIiEgQeR2G8Qif0HkehpEIn8IBL7BpHo'
        b'OohED4NIHGgQiS6dTRxgEIlug+hbiLCezAZ9uZanjwvMNnyovMZcDYRZbSOkzkTHANRYDyqRI1BrBoIM1M9kqTXryyprgV6bIB5osdWst5IckF6q15pLYaIgONdAhAW9'
        b'gmd36TYLYSj1IDCkLcbHK80wbxYLbYBQPZ7HGg3VBqss3M565WnFMN0kXykkmipIvvn4uNFoqAAeZZUZTLJCLfBFlwIFFAYkJY/aWF0r62PjimLoBRCMcFLcLcFeHpIm'
        b'9S8QN3CBOI8F4mWzzTYrJPcvR9MTBq4wwWOFiQMXSKQFsrU8X6ZzDnIJyCc0zqpfbXX+AErk/BnvmtXizMYDYrYe2HGFS8SktGKDCaBB4E/bIUn1EEVYL1Bpt2CcexDI'
        b'j9ZiBW5nNpRbCdaUayuh/5DJpNNCZ0ylgLZOiFvN+HgFIJHKpDPUKWXzef7hGopzC8W7hRLcQoluoSS3ULJbKMUtNNW99Rj3oHtvYt27E+ven1j3DsUmehBTZOEL7bNq'
        b'sQsa8j7ByFOiXVbylOQQnwZKc5IyD+m5nlsjcpeneDdRbOAxDJI+kHT2XTLHDdyym5z2NNmAVHrK5sYCkvqxgKT+LCDJEwtI4llAUh81TnJlAUkeWEDSQCwgyYXUJw3A'
        b'ApIG5mPJ/QaR3H8QyZ4GkcwPIrlvEMmug0j2MIjkgQaR7NLZ5AEGkTzwIFL6DSKl/yBSPA0ihR9ESt8gUlwHkeJhECkDDSLFpbMpAwwiZeBBTO03iKn9BzHV0yCm8oOY'
        b'2jeIqa6DmOphEFMHGsRUl85OHWAQUwceBBDIfrpCjAdlIcajthBjVxdiXMSUGDeFIcaTxhAzoMoQ46obxAykNMS4jcfexflmfbXOsgaoTDXQbUuNsQ4kibSCeXnpCsqt'
        b'rBazvhyYoInwPI/RcZ6j4z1HJ3iOTvQcneQ5OtlzdIrn6KkDDCeGEPQqE75XW27VW2S5ebkFdgGOMHNLrR70YV6Y7GPmLrEO9u0StUBfiu8RTv+E2FDBx9ulBkcozi0U'
        b'n5ZnN664FO5ndontHxXXPwrUHCNRirVWIpfKCmxQnbZaD2xUa7VZiFjLj0ZWrTXZgL3IKvQ8mgI79GQGkLsUMRDmbtDRYt+a2UP9HpiS57r7Z6Qmpr7ZkYHwLbOLvHQq'
        b'y0m6fZL533Euv4lO2Gep+ppNy5FLzMQwaibWNjPZm+P3P4gp1UwM5r0iS63RYDWPdJr32CdNecR2v95hjaSmPAHHSjiOE8baSI1WfBn1WHB7JG6JQmeEwxYzkiRugzby'
        b'v2TFK5d79/qkl5XV2ExW0Bp6/WcDqHltQ1urNz4awtvwiOX76xFzAfjVIFEQC6mM13cAdQ1AcCALMbz2Conk42bDuwfxRdW8PFNTadLLCmqMxugMIEgmhbqemFf6gn0k'
        b'Lm2xuljGFyNmNEI8LQaLjY8gaa5hfsktIFY/XrznG5pdpCgoqzTiewB6I4gkrsG02XqjvkJHxsP/tNtc+n7H2dWjNMeEUHGfyIN6+8p26GwyXiaya359Niq7zkcldaLt'
        b'QWZYW1aqFdhroM0ZDZCB/jKYymtkClm62eroij1GZSIln4gk2eI8ZYvrly3eU7b4ftkSPGVL6Jct0VO2xH7ZkjxlS+qXLdlTtuR+2VI8ZQMRI7egMBYi1DxgiKirp5Fx'
        b'/SIhIMvWA7l0GGJlNqWszxALkTxKOyyjShkR1x1KN29x7QOjLCsyK22+zVRF/V715gqgT/WEppD42UWyhKk8ly13ZCEWYU/xdrzhkzxUmFZMtQEycHO1liQ6UcRTihNV'
        b'BioWN1gxz4k8Cg1SzHMij1KDFPOcyKPYIMU8J/IoN0gxz4k8Cg5SzHMij5KDFPOcSIpNHayY50QK7phB4e05lRYcHFEGxpTYQVFlgFRacFBkGSCVFhwUXQZIpQUHRZgB'
        b'UmnBQVFmgFRacFCkGSCVFhwUbQZIpQUHRZwBUumKHxRzILXAiu+VVQHrWgXM10rl0lV6g0WfNh84fR/1A3KoNRm1xLRoWaGtNEOtFXrIYdITmajP1mjnnITgpdvKiVXM'
        b'SeQcvBSSCOXtY8iy8HRTPS8Pk+08IMbZBiuwRr0OBBGt9YnkJ+hw/8J9lPzJNLMR37DYxQS3lAy6uVNuBanEqVVRTqKgYo9HFcA+Ujs3B9YPnIZI0OVUdq4mDN6qN8C0'
        b'WJ1mYhUIulZDuaFK60r9i6kW6DQfu4oZvO7oso3oKibN1/OKhd5QSpKyAGpkX8zCSzYDy2uupmHoN7SsNdqqq/SVDjs2ZYKESZrJWYBvFXTNxAd7MDE3HB73PIq5YTYZ'
        b'RC3Dl1CnJSsHb48GWTcdnSMOyWovZkipUIp3oufdxF2pQ9xdwbqLu13iLt8uXx3XFdIVwou97V66qGZRs19zSLlA56uTNnqD6CvUi3R+Ov9GRhegC2znisUQDqLhYBr2'
        b'gnAIDYfSsATCQ2h4KA17Q3gYDQ+nYR8Ih9HwCBr2hfBIGh5Fw1LSg3JON1o3plFS7Ed7GfLEx1s3tt1Hp2jm7L0V6mS6cbS3/vyouny62HIyMi/6dJQa3+6tU1LHOBE9'
        b'WREIZb10E3QTadkAXTSkiZol9NxFME2bpJvc6F0cCLFB0KcpunDoUxC0EaKTtzsOEfg3B5SLdBG6yEYJ1BJsVxVieiVzifv1nIJFX0f7yFz+OaJlPIHhjwC55ZCLzMSr'
        b'1ky8nh9RL2ziePdIwusXTn1BLn1EPG4eUU9j4nPTV8qc4ChlTiQPcnjiEfGEeERcNB4RpJB79fpodXVAuswlBl2vdxkQEJOV/PTX8jpOiREkQGtlr6TMBmvLVLamV0J8'
        b'Tg1ao91Lw7fcAEJfSTWs60radq9gXtHCHNpDcwqEyyR27POx/1EnnhnMEweWvJvFzT7NXuU+dv8gyVZJA7Peu168TkL9g7ypf5Bkg/cSRiegrmrCL8gZCLdJI/9UfPcM'
        b'9XoLPZjlnGoD9XEo0yv7FekXkQq6iLZa1jc1qfYjWUBviGXIfubLPkdak7VfDeRf+GwgE1YHkZIrZemkPBCUMhn1B5TZamVAVpNlOkOFwWrp3y97N5xQ8dwLPtlzD5z7'
        b'H9/Sh8Rv64M7OqTKsug36cKC6CxHqr1jFs99IUyIkH9gHkpZYSUwBEB+vcxiKzXqdRUwnqeqhXcu4TVXqEmmhSogzPdfZqwB5mRWylRWWbUN9JdSvcdatPbBl+qtq/Rk'
        b'/1cWrtOXa21Gq5yeyEsZGBb2ZZAqm2P/JSsjBsRw57aji+FRPlAtjiWU6sBWixOY5ABgjVkWzjuxVOF75nrQxgeqyO4xlUpVLyKmQDU8jtgJS7i+QilLjI2JkiXHxgxY'
        b'jcsaTpXNJwEZDZDqyg0mWDXQR9kavRY6FmHSryJ7oHVJygRlbIS8/1R9iw+xlD+fcD0qiAFOltJTqs/63lwlYyMkAR1HV9Be3JqNzufhrSrcro7GLXmySXhrbkFGlhy3'
        b'RuUo0DbckZWfgS5k5GRnq7JZBvjdYWnNXLSV1htQImWA44bHrCyLSkmt5+vF7egFtOvJemmteDtuyQIeilqeqDYBncKNa6QMN53W+6namwlkmBhNrUk6QjmLsU2CSJNX'
        b'kOspqgylIiITtw9BzWp0UcgkLRNb0O7p9BgYrePPEV6EGQfuiK6L2h7yLGMjx1HRZXRA5alreCvU2hpFutcmX5SxdFpf39Btsy+6smqZYbhgndBST0SOv747+vV3vTfG'
        b'SJsenrx57c6WTs0ntzYLJAv/9LfxHwh9no+1FnQcqZWsm7kr6tcjx0WpuiZaHw4p/tdvRt14pzUn2Nd2dtHP05eeXmzreM5v28bNe5iAc+96rS4MeLfwq5benqS2yQ87'
        b'Rmb/4vc3J47Z/9G/L1ofl6Z2/iDgcIT8dkmnXEpdGifg3fgWau07/DghQcAETBKUB8+1TiDDbI9DJ1BrLj6Kn3eFJMuMwA3CetSG26zk2CdqK0E9vjCh8mybIqJgOvWr'
        b'hRkVSmLxC/SkST46ha6RmpyQy0ynFQ0dJ/RdW8P7Xl7XoZuRivDIsAwFx4jRPk6B99VTd3F0WI96oDjACp0sJEeJCKyC0UUBgPIc3mElNjyTHl+LVMolcXhbFAPlz3Px'
        b'3lLq+7sCXU1FreQAF4wBbceXefiImeA6AbqPNqIrViLcFeQh4m7ukNDQNnSWYJgdvoBHuEms9E+nVaJj461kPK1REUqSaRjegdvJERrIJ7OI/DJm0XEvwrdnkmzEtonv'
        b'BxDEUECzaI8AN+H74VbC9NEDzg/yzNA7GrbLhSPQLSFqXYVP8PKmz394vqzvbAp1NiVHZJnnmHViVswGshL7kxwjk9CjZBKOpIjZ+iAHF3aeWclxdIQ6mpI1aiYHv8yz'
        b'yCOdPGYzjgMxc5jBvVUlfKm+StKdpWglHo7WPCLdJw6XzEame4yrS2v/rjp9mln7H3UlJf1Zx6zgD86wOXK217ekT2BweNBybjPXK5lm1FaX6rQzgqCev5A6XdpzpH1t'
        b'J+H22hzsPhxYg05RYzKukUNjAl1N2dN2zKfEKUJ47pc5Ax6hRGJTwY+vx/Lt84U8NP+t7Tby7QaUuIsNgzQ+zNm4fFDR4jt1wz587xIH1x6kAyOcHQibrbXonYz+P2vQ'
        b'weAHaXC0s8EJAwoB333KJSV2kWCQlmV9LQ8oNnz3QUtLXKSIQVqf0Afpb5E0PPTB7VQBPeDGNTPOA27f6UyBo7p+ZwrC0xtF9HDspA8s/IGlyvJPmZ+2XVL9uO0D6cvS'
        b'A2HMjGPCd3eWyDl6sBg11awHkouaFPyukytZ9h7FE/hr+AXcRNlBUYYHupwTOdiZM68Ssn5cjx49B58p9YEulIpmGMC7nxvAsX8JPCbDzFqIXz3QwY3Mr93OmvWrX+7T'
        b'62Vfj7zvvthiNev11l5JbY3FSuTgXmGZwbqm14vPs6ZXXKel6qRvGUjjNdW8mimwait6RTWA6eYyXzskSK/8HdCYTwDr61QP/Zzn9P35SxHK/e0A990qBYBLAeC+FOBS'
        b'CnDfDVK7ktgISuJ7Ig9KYrpOZwEtgIiyOn0pWWvwv8zu9ybTUy/9p9ATqRZDVRCtrNJWoXfRzGBGLAbQbGT8KQaiZFn0VqUsF/C5Xz1k0VeT/RZDdW2NmSiUjmJlWhNo'
        b'KaQoaDhmfZnVuEZWuoYU6FeJtk5rMGpJk1SoJ16TFiUZqYFYzmBV2au0K0akzn51QNU2i8FUQXvkrEYWQYEV8RQzMt8+2kpi1Ojf9375w61acwW0oXPQH1JeRmyBFqJk'
        b'WFbayOyWmrVlVXqrRZ769Lo7j6epsnQ3BiJbSnc/nx2oGGk5VUZPLiz91vMLA9bCL4tUWQH9li21e9MNmN+xfFJlxJIJoKI65VJXb7oBy5IFB9ooPGVLc83WgfPxSxKy'
        b'8j9oG1EyVUGuIj42KUm2lFgvByzNr2PQM9MLFaq5sqX2LcFnI5e6ns4YuPG+5U80Zz4gIxW5+gQPWBwIBkxmJSwNWK6WMrOh1mrnWgRPyflqurbSjZYawF+9zqPSD+hE'
        b'chMuY6S36VBgK2Vzec2fLtHxBVZtdTU5yGYaP6ANgC4GQCzoQK19aekM9D4fLUzrKgNwM/1qgLh9wfWvh/zLqbHq+WVCF7/eWlmjA0pSYQO1n/RFWwULEBaNHmanTC+r'
        b'AbbusR5+SGTRUJOGhR+mweLSJaVsPhA1B0HyWIvrsiMGEEB1cltRmREGzF9UZNF7Lqmx31VUU0Z7zm+WTKu0WmstqdHRq1at4m+gUOr00TqTUb+6pjqalyujtbW10QYA'
        b'/mplpbXaOCHaUUV0bExMfFxcbPTc2JSY2ISEmISU+ITYmMTk+KkzNCWDmBsI9+t/SjA4h972M8eKL1iy5JkKZQ45kReJzkSRc5x38KUCUaVpGn+Jys0ZcWh/eTz8jGVi'
        b'1fgsb6gYxV+kEDP/WvV6qS9jmwqRqxajHrVDx8rHW8mNIpmKheQc68JwcjB0MW6eAgo8/AIuj55Hl7zxLrQfHbfRexC2o5sR+CoosETJ82JEuJtDhyul6Cy+YiPK8mL8'
        b'oABfVc57hlx0QQ7MQv3kzhKOGYtOCPGdPNRuI5oOPhGCbuCroC1nF+Edte7jy8Nbc6BYm7qoFh65WZl4l5BZMAtvQ5t98XG0CZ2zkb0I1F2d6Ksswz3yTHQPHfJhvDM5'
        b'fAifQ/fpRUrQ14v4Dr6qgjpYJhUfFKA9LKi5DbiLdjUJ3Rzti7fm4XvRStwCTUehM5mgHG9lGdkCkRC04O30Lhp8LbEGX40OQ3sjWIbLYJNQI75KJ3j5RN4qElMeYBs7'
        b'aQhDb38CPbh7gsUP78LX+ZbxAbxZsoxbgPehXfxdIJsz1Ra/+AK8y89PSW6oycKXI/HzAmbYGgE6j/bW0I2SOBhnp68SdeigGphCFZkdATME3xYG4G7UZIir2cJa9kPO'
        b'lycsUvxE7YNmBQrf/OS138b//eOc137ScOvPPsuPjNMkBS+bvF86+9Ds4D8d/sXGv36QP+en08WRimmB720Oi5geWpb47NsnrE2/W7R/rv/So78KO3bIFH3qN79tDO/8'
        b'+Nzenu6rjwzpvsU/27Io4dimRddOGixz7j4qe2H2uzcfv/WZ8r7h3FcfCSz/+OcnK1U3r/74jTjNqqUzyoY9nPlHCQ5QFUUWBzyWi6lpBHfHok1ifNvVysLbWNCWFCvZ'
        b'eKpBm/ANB17izTmRbjaHyHgR7kB7+QPQunSrr3q2l93O0mdlwRdwIzU3oP0ctZO4SrXz8nm5NgKf5nt0dJY+MgffVyhUqmx1FG6Xs8xQfE8Yh1vQTnr7QjJ+ER9QR80P'
        b'C8+AbrCMBJ3j1nhDRlep1P8/vfNmwDOxPlqdroSX46jYPNkhNmeQY7ESdih9un6E9D4PCVsf4hR7++qwWyv8eOn5GcaxoVdMHuSaDvMy8niWPJaTRwl5aMhD6y6Mez7d'
        b'68vX2VdJibMJrbMJP2eLGmc7VJAvo5K9qyD/q8mugrynEcm9e6U64spnF5R6/Xjx1xEUa6vpN7m9RN/rbd/BLdP3+hJhBURE4t/F98E5zDIfOyUmFpZAByXOJNK8j5s8'
        b'7w8SfYBdpg8kMn15oF2i96ESvS9I9D5UovelEr3PBl8Xib7Da3CJXut0z5PxNxY9hdw6jxxo4HPLgHnCPIFICgKB1vUuPiI0RMkqzDW2WkgFWVnbnxnVVJcaTFqHeBIB'
        b'kksE5as8WyXKvdODk3TQqfP2q4nowP9fBfl/WQVxXV6pBFB8jNOk9S2qiNt65MvzUY4KPMpjS7/Fr3PA5vj1zrdjX+L2OF6kNdUQU42ZCq0mz6LoqhoiMxqqtcYBhN6l'
        b'g3i2girh2bd1wB4TysT3t7Smpor0l8QoZdl27NLSsKymdAUAHhR8z1uBJqICpSTFxNptXwQRQH8j1S3t83odsBNOwpgqK7LYtEYjXRmAOHU1hjLnalzq4jQ7qBZoJ6zu'
        b'YKCH6Za6OtZ+q55Gij+hq7m5b/5foGrN1q/SV9idb/6/uvV/gboVnxQTl5ISEx+fEJ8Yn5SUGOtR3SL/BtbBRB51MBm/5dsloJpU5ffma4z11gWMLYmIkNvRVlCSVNl4'
        b'W5TKqVG5KlIOLeo5vAPdQPe9E9ClmTbiSrUwFO8qzXtCj5IWolZbCtVrUNdItTIzG6RXvmK0adFAdaNW3OqNTqE9oBSRPSO8F93C5yy52SD+jkQ36Y1FpI3FeAeU6cBb'
        b'QanyAc0DqoXw7YJl6ADah455M+gc3u2bUwDKEdE+ZuD7+IElE7erstGBulw1uesoRsgMny3AbVDrOaqarlSjrZaIbLw9fB3qIbK6UoUuhLPM2AqRCHXOoBVVVqFWX3wT'
        b'bV8owe2KHNCxOCYYtNfz8QJ0BB/NpbvRz0SkwmT07UarovTolApdX0hu141FraLVuFtEtaulWvQi361cVZScXA4amj8dHxPgu3hvAoVVzyx6ga/sbW+NsXOBD2MjsiXa'
        b'm4aO+orj1zNMIVMISuJRHoSHs4t8yQTBZO7ENzOyMlETbgQFpBNfJxpoKzoHbWXh7RlE9VoWJlmAGtBl/obSFnwX/q4yVbiHYVSMCjTL5/m2GmfFxDPoXgBVxvEefJIv'
        b'cCYWXcCdAnQabac3oKIL6J7xq3//+98NpRS7ZumzNFF/HPEMv+P+IFJMpFGNNUpjNA0vYChw0XV8IZhMUrtde8+IWkSuI47OLAK0qA3MwG0F4XJAjwzn5cNydIPOotjk'
        b'9+yz0BXi2DexDt8sWAAIsSs+U8Cw+DyDz48ArTkN0nzQDb2vHVILHTiD24aoiyRuE8VPEmjYzwsZ1Fzk/UxgPr3l1gp4dL1P/c0Px7sKJHY1NwEWDK/pzhwi9sebZDay'
        b'xzAC3ZVaUKM+U5GbHU2wKMeu6srxXhG6hjoXU20/Mx63RpI7bizoenSmXMz4ogccvlqNdtNrd68zudwr4phyUa025N3hK1JEdr+MVnTIiq/arRy83wTgGG6Jzs3OD8/M'
        b'Rt1rya058kWubhkvoFNSWLK7/OlsocPoiFGqi1SqoiJYRow6OFiP+CAF6jJ0FnerqX6Iu2dwZjalHu+QC2habuxa87NupU7hPfReWiW+OIcvZJlNygBeHKbmFdzhl0PH'
        b'iHaiOy6DBH3/pGG04aLAMgO0paC0G8/umJ6DZwU2VdT9su7Ac988PxwNOR2xSr6w1muEf8z4hVHjdAuP2HBSw9yg/IIUxYLDHyw7s/ond47+qvvL37/17q+KfnbQPzk0'
        b'K3vfo4zOlzY97PnTgczF7xnbh2eXh37Vnvj5xLohqn90rGMevV13XNS9cdThk6fXvy213TJMmW49kzpaVLC+8qLyT3cLvvyZbMKCJOueD2d9mT4yrKvwX68G1l87eupg'
        b'W5lXr9B0IOtvy65mTd9jsL35uqXzVesb5oUyVc7lh+yjihfVvzn5Q/PFk0Wbdto2nX9t+7kTOYfL80ydPxdX/GPOGtXe9+on3JPd+nD0zP957Z7+3ppr178YWvggK339'
        b'zRduin7uvzblmVHJ4T8UXv3lZ7OUd/dMvR3x8d5/hA35TWJanfor/29qCn+6+Obk299cSby3Gm8rrW8o+VV855vTf/d45h96zCfeiJT7USsC7gnGO93sEfWTeYtE0zJq'
        b'kcAPcNMqNdDGbqcrRD+TRMk4upH2jAltcTp+8AYJvHcFsUmgK/gCfwfvnVB0Rc172RC3DS1uZAIWCYyoZya9kGsC2p4bGaGU422z0MUohvF+hkMn0CG8haaaASOO43tF'
        b'kUpC96MIPm3nFD5oq5UQHHyiWKLOihAziiLuWTYZPz+eepIkj8Lb0LmV6GZWdhSQRDWLrpSgF+n9buikDz6Dj8OibHX6a4jXcVNmLKe+GCOYNXavDnS8nDp2uHl1LF9M'
        b'c+HO2Hq7o0gMvthva7CulM5zwYQCC1laCsK3qNlHpw7COwSop340f8vl3cWoWR1FrCzx+KjD0JJZO8gFWfLA/5LZxZMBxp+YGvo0cWqEKSQSwnP0w0ntJpg+Qwy5t443'
        b'w9AQR1xIxkBqKCumjiTEqSQYwuR2YgnnT91MfDgSrh/mZuDoa9VutpHyphMdeejJo5w8KsiD3LNoNjjNKZ4sNl5Pc4mxD1+n3lmxzlmTwdmOn7OJPttNFTyK3Ww3pyNc'
        b'bTcDDa1MZJe4yHa4+83momavZobulLLNPtTi4tssdN5sLtoqbmDWi+vF60TUwiKmFhbRBrGnOyBJ5WP7iXP+9oviZwpARNCs82U00pfmljGFNLa4krDhr0L8ZmmifFXJ'
        b'DCX+voD9py2oXbJSwICMdVbgz6bgPRv4twJ0Aws8U4DaC0H6uI7bi7Lz8fU8fL3ILykmhmFGDxMAn2hU2d8JgA75F+D2wsQYvC0BJCl8Ct2RrGTxYXSuksqElfgwcGVS'
        b'GVQ0v55lRBEsUJ+DM6hQgRtwWzW5xnxDBrnIPBSdoN3LxAdQMz6GT+AeDIIVM5kZjprQbpoWhw7j/WplTEJcIt49hmPEG1h0MJ1nplWiwEj+tnB8DN113hiO2msMxcdb'
        b'RJbPIM/5ygPzcu/nCGKlNzrVfzg1q7Vw3I6Iy3+WZZ2XZhkXRT47KfCF1HfeUoxZ06j7MGg1M/nk9vWjDjwuevXPH60rmfFuS+lmKVdskN0TNL382Zhrj/LffLNlwpRv'
        b'ql/OC8VHN66uK/5yg+/dKfP/fFOWsUv+VteMrMSc64ve2DHCJ8xrYkrT35f+KGf6vO/H1Xxm0oSfCvvHl9Ff9C7Jfba+7bmRqyouvnBbmfWvoGnjar5Sf2/l8M8rk/d8'
        b'NPrfl1/cs0IQnHI8sn2Z396gIzErfrau/qPxHZ9sOPEwaPme4AWrfvT5b795pePnvnn7f2+cqfrl2z+NultRmfzcR0Pzr/97mDyYJ0YHJuMb+A7eSC/q92I4dJQtwueU'
        b'/KWJByWoA52j5BSdR5spSUWd6DZ/M2IDfh5d4gnqKNZJUkEQaubdCM+AvHs+RurqL+dGVuvK+Xr2yiLc7eRjxxK+hJtjeev2LrQD31PnRIGI1xGNzgIqXUYt/uhFQQk6'
        b'gfdQ0j+rOg+3qulF72jfDOEYFh3FV9Io6Rfl43vOy647k5z3WF9aRluPQ3tMrvfEozPz6VXxC9BeyuqSItFOtasX5LPoOssMRReEIwPwJt6TrxVtMqsdPo74ICgnLdTL'
        b'MXiFAJ3PQ9usxPtu4YZhDnP/AnTBA2/F54far97GXfOIr6rTo1TMPLMsYIxg+cx5dERSvc6FsTIgLhHGCsBoodeh4s26YTx7UU+KsHOXbLyfFl2Lukm9eBt/rT0+P4m/'
        b'2f6oH8+0d4Patt9xmSr87rJfoxln5tnoftQylwhyeHuuCtjpLREk7+BqJkQ/He3937ox3+Fiw9+PT9mUro9NRRMmRH0YqSejkLAojoNvnmVJgULzHyFlXPweAgnxfo8S'
        b'Z7rjI+aEnD83lPMBtubqYMM3z7Mrrz5G0evF26QtvSKLVWu29gog33flTSJzDfld7WRBJicfoizICI8LrP12TMqCNjI/lw3gCcR39L/gkCWgd2IKv/5dP2MCf77K6ji/'
        b'YTfKGu22ErPeajObaFq1TEts/i6ml6eyl8uq9GssUE+tWW8hDo68TcdupLI4DfV2A48nO/eTNnwjbxkj3SldY9V7sEE5OarYdcJcfOLpveqoNZ5sueHdQCBbqlbBEnoe'
        b'XVkM1PEyOpePtoqALW0UrB2Jj9B3gWQAzcCdIvqCjn1KRolu2PgX2zTETKW8FrUuVuDd6hWzlUoBE4paBEA8t1golz4RArw79GcARo0xY0UxQ19hg69kogvOkuLx5GUj'
        b'eFcpug+L8mgcE5EoSvHHW3ltbr86qU8pQ7fQQS56HWrnd4x3pYACjfejg3Y27GDCrdm034uAIFyhitvc6QxR3FKTqD43bUFcAZ+dQ+3sc/NG4XM+hu4rQawFiBkztOjj'
        b'7Nft7xlJjr87a/S243veF+76eN+2fR9MnvT2w4jyf0b8pGdtQZLuxIp576mXf/NHvx/MmNi748z7mz5ar53yUePrmT+cP29ZYZapVtX1vVdv9byse+mj1LKSFaOLp/8i'
        b'dfW1w0eaO79/rCw/d7r5bcuRO9H/fm9I8f77RWsvvLFn34yfxGR9vHzmhNYpk2wz5WLep28Pur3Kvj16G598wvEPxIkdPLe7lD3ScQkwI16O2vBpbgK+hjZSDjMUNyoi'
        b'ldkc6CN7YNSnWTXAcg9/O/Q2dHXYGDHwMP5tFxzjq+fw4dCplA2KUSPa7uJfDnzm0HIXtSEOn+Fp7/U0fN3tjSXVJYQR4d3L5eJvoRsDeCNqLSVkxfW9Q4QnlUahIJTK'
        b'6KHwTQgf2WgNBlLnQj3sRXO+o6PiSnj89gkCdXAAV0V7E3K2V1irtVZ6vhw9ibHfR022IMkrEsTOC9KFA16Qbj919lDAeth+7KNZhHxYtHXkl9HoSr2e/twZ6XiqTFUu'
        b'iyC/ImRAci28oZvQJf1qctaV2H0jlPWG2ogo2pCdQJo9m40t5Do/ndNYrTWXVRrq9EpZLrGtrzJY9E4iSOugA6DZtbLyGiMQ/EEoGgGR81yfk6JJcuiV73GwEDojM2Bt'
        b'5GWAzJEZMT07C50pzEAX8NYoJcggGXiLVy2+BGQliiB993h0SQ1rKTNbiVtALEMHxhbC4miNzgfJQxGOzggZNb7hhXbLSnhasxdfRNdwJzpHD2oIjCy6AURzM2qo4t+X'
        b'dMIfHYwEwOMt41czq0FQ6ebfurRrPd4Umcsx7Cp0cyGD92XhTsN7PnkCy1VIfRyxb3p7mj8XK537g5yhSzYcfUdQK/af9T0R4x2+MUJ0dNYHBcadGVurf/3T/LTkSc9M'
        b'vPP561+1743vemX+naKAurffbJ249uQX5aVvf1OYeTvbVzGee2XFlNl3f3L8r/KWh+cPx2765Ezz38YPTSlc6z+qbYpi+tqQ7trppp1/2CB8eMVwU7zm4Teqpfi85It/'
        b'5u79lwRVWyb+wqJbnPDPg8LHF7aHND9KXG982POKT9qyxMeJP3xr2DnN1D1DF8oD6PssChOW09kGhE9mqzh0ET1vpuQkdkoSkTapBHh+OL1wvpVbj++WUekwItQfX8XX'
        b'VvF2F9ykZLzRKQ4dQ/txNyVUoWtBtCTlW0BqnygR53Cj8LVFvP/zAXR9OXmLW5RSRZLxeXyB8cU9HL6H7up4YfwC3h+njkLbc+lrAfToAeM7i8N70eFCKlyOyZlMKojO'
        b'VRCVAN8Vb+Ai8vEDnoKdwpuXE24hV+IOOrIAyfoYQcVyUAioYNqALy5yUliLityyju4H0bJDwtC1yGiysaBQyjkmALWg7fiQADWJtFRPQYfWo31Uxo4G5U2AXxBP44at'
        b'RafokGPHF6l5NM1XAKJ6h3LoSGE+bdO3IJVoKPxsoM4c8Wxu+BLEv24Etcfr+mRhEIRV6Cq6rFlJEycCL23heyRiElGPGJ3moiLQmcGsNN9Cpl1Is5AsW3d3F/Lx5u0s'
        b'EnooB2gyiKi83SQYYuv9nKSTlM5xe1GA2Z0+D9JJjs/bR7Ot8Pj3EzS7YajbiwPcGnacd54LjxzzPPKTbOIAHbH/k4v4Lw7+Qp44XU9c5HU1ZSUl9GxPr6TWXFOrN1vX'
        b'PM25IuIFTz1oqCmGCsOU4dAR8LMR+l+3kw0KRzN5d8eHjN11RiIUcsQ0xrChEzm7TvGtT85fIAVgM+xQpZQN5UbljUj2H0lNFrhJgY9ZVLAi4sos/v4Cxm80h4+ApHmT'
        b'7jPlVeDTvui0ldAJX9UC1JGNt+eRjY9RccIJ6MUJ/6VXDfV71Uz/PUOvHErAcSd0ZXeBH1GJxzHjYF2do2/UwxtBPFQrUU9MIrMhixHiG+zK5HQ6RFktarCbZabk973G'
        b'rQedoyyjFp8GaqOKIgJRvBBUzVauBO3KBEZ10rCg6muBhSDfNs7yWLPspZ4dRzpjm1ayZV4fciebpL5haelRvw89Gfr7pixNktrHd0nXkVdPNsQ2HWk4sks1af7z7MSQ'
        b'11/qFjMrZgYVVwBOU2oRDyT3SCQxSkcxRfH8YcIwvJ0ShPm18TC+y+Nd6AW6bMOHaaIU31rvsFWPw6d4c/US3EMJ+gx8+RmH0swrzPjUuBrc6UOJF7ohXEn2VPnEZ7kw'
        b'fF8ftnawUyZSUIdA/NCXEP8CSkSGuhKRicTkSoiGEJ7mVc61IewVkgK9Yv6Il6fXG60hUaud2E3KjuMc9W+0fx66ynO8GrOnMCYyPFOREZWJ9s9C7dH8rqgM7xaF2tAZ'
        b'N/QZYv+2/Nn1hotIcssD4CSnEzR6Fwv0QvqGN4a8262dKxZBWELD3jQshrAPDfvSsBeEpTTsR8MSCPvTcAANe0M4kIaDaNgHWvOC1oJ1IeTtcLooWA+sbohuKLQttacN'
        b'0w0nN1roFDRthG4kpPnrlJAqpgdbhLpRutEQR+6hYJuFUGKsTkZun+jy6eK6BOWCLmGXiHx0YeUcxJFvgfObj+WfQj6Hy1P45G/duAMBUJdPXz1PltGN7x/3nz11Ew6E'
        b'6CYe4IqD9MH6IN2kMOZwyBGmgaWhyY4QzRFK3QT5Iz8SmBMv+50bQ6gDoRedJ5FOrouAuKG6MPtNG94lwE6080GCpcet3czj7nI/74Yopu/uEzuN4qJBjeJP8Wo0H94o'
        b'Hq6G9RYFa2OWJurXo6fxu9DHfduY4aKXxEyeRhkzexEfuS53PfvVZH+OidGu/XjkM4wtmvQbRJQDuBXtXuiyj+92lhfoRKsXU1AhCczAHbQiZfIEZu46LfREw12LWMl8'
        b'5OgkPWZneKNML7SQzn/JqUa3Xf4qw29jjFT4PzmzNcIbh18fI51VJp935yXh3IzyKuO+u889+iJzREDlmwnTdk6S1h8JXJGSHH/zndap19780feCvd473mPLG5pRv/qL'
        b'od/r3pATF3b1t59cuqr5wcKZpw+GPfO7b+TevAzUsIS8WTdXNQ5dAE4jYCSFnBUdNFBymBmMX0St6FJWKTpJbMDiKVwQbjTysuQ5fASfemITEDULcct6SWUWv6HYMGSJ'
        b'u+LrmJNJoIVvCxNVorvoOL+11obb0/mz2pHhCj4n5Bs2SliHrk9DRzVUlcY38Gncwr/EB7WjUxuoQRlocRDeT5wrdqAH9Ny4F+oKc+Y6jzpwRzY6z0CuXQJ0DF/V86fX'
        b'r6CjwGlao6G1y0XRKvLaYgnexqHGtWiXlao4J42LUOsqFbqH7kWpKKMlFXbkAgtoycXblWJmqlqMdqNNaDdPYp9aAOw7mD3GlXTHiVkfkYQdTg9o282ZbH2wc8E88d5C'
        b'3vzYK6KORL1C4ofaK+3beDLV9HobTLU2K70dy7PyLjJvIL/XkcdzjEMuXO/Wz+h+LOAtN/HQQ/++9ShqJX8UVVRCOj3IGdR0zr44XFtxHr8e1Xe/Z7+TqEqoVU3W6bd1'
        b'pYLvil+J68wN0qW5ji59Pcal+f5nr5VP27JPiRNKgzS7wNnsaJUju8P98Tu1Wuk4+kzQpqTaMNgB5Exno0OJDiArN9dUf7fWyt1b064epLVsZ2uhtDXiGPsfzKe4xFpj'
        b'1RoHaSjP2VBYIcnqcJ/12Nr/3knmfvyIY/q/qI8yh+RaskkLfRNojLN1Up71dM2hXlExlvGarHmV6xlDgfU1kYVYoOt9u8i7YTO0Xbrw36u10vKPNR8zf94fVrD3lbDN'
        b'YSlLGU3esLfEXtMy5ayV2HeU6dMIMQNClg6kciBaBhT11iCyJ9XBKN2irxhz0K1FRNisD3KlA//pMeeCfsTmkpv9sH8jj/4N//7PaTt2aGmrhEzg8DfE0E/jO8PiJ9IJ'
        b'Cfn+NVKaHZPIsM8lGUSzfyyykPvhbnzJ0Pf4Tlmk2aFb8tJetBdd23FG8PpNLX3joZFlVvSKDz2cKeco40FncbvNDizPkPLBpwnj6cY3+PdV70b7hxK7TIRCWY/OEEv/'
        b'Zi4emOygb0gNKKFuv4Z6fUmpsaasqu+tdA64LqsPc5lu99xuL0wVUX9VTyrFdsbN2NAOjyX9QHzWDcQDt+lckw4oEynF8QJVAcBZ8JRwbnzy9ZmeNnoonHfO+ZL91Cue'
        b'CIQln2kMDH3hu39eMTonJNs55nqmXupNPRZy1i5B5zhyR0zOWmYtbsQ7qKsn6lhf73bzkA96nryMMzxHQW4uahH75+CtvFukH+i4skNCEEizPpnKMdTN79djcrj3jW1+'
        b'DHHzW9KY9w/+VKMfaq903ETk5utnRxJX9z50BJ1YgLt98D60cx0le1T5FsUTdyiHdo1vGqmCnZmD9xhCKjiBhUBu4/1Fk36s8OdiQ4Xvr7k0s8d/wd+CX/2e7DbLNa31'
        b'9i569+KSnyaeN+w4cPi+XPF4cvff4/6S/HDbDyo2Tkqfm9KWlP9K5uyc5oK5W2qPxMzdav5hQEjL8kfZLcEPlmSV3NyfcjRs5s2T9Y/f+dFx3Zclll+IGsuv7Fx/RNEa'
        b'+/Hjmhs/G5I65+Hmn/5m3K0ja79hfnh2wj/nR8u9+A3yo6hnobudsQTdiBFU4H1l1JioKUPniGQasOiJE3NV0630pbh7K/E5D+srMtOdFp7HG+kG0nR0Nsc3wi7CZuOj'
        b'qMVR61h0VYgv5YishCKvQ9cmUmcH3LYwn0Ibnc9E7Y6FK2Zi0FnxKH90kkreJhBS7dv0bDg+w+/T4ytDqclgJXV7tZsMYvFmfpsd7Y7pex/tgLZFcckqs8H+rlE36bKE'
        b'UGmOHQPS5Qi7L5eUrQ90WW20oPubkLXmCssApJsz73Bf3B3wWNZvcZ90ew9lv+ZyyoT2dei24Wp/Ky49h+Z8K66QbvqIYFkL6bIW0WUt3CAaiNmK+i1rcQ5drJl4z3hE'
        b'biUcC2J+7Fjcwd/9RXdMVyThk5H56BzqUSxSEA8LryBuTGWi4W/BRwSWWMjQGR5PTE470Dsv//rlnh23O2833F4S1SR6Vr53XNPthjMNU9tVbeP2broqYs6nStZsGwss'
        b'mGg5kWung76hwl34ProQjgApqKMFy4ysFKKt6GS8Y+oHNx6LS+ipBArgQFcAG/2pd4PbHNOsDu2kz62NvsOYmnv60WwhH/9EXgrgnfAw9ANwd/BAAKaNe4YvMRk3iwDC'
        b'YmoqIFD2ekooV3y7ii/K6QNnIdq3pECx6DncrkC7WUaA77LZuCfAcPNRq8BCTMxC5pePNWrtq78P/0BF5ahXLB9rHmsM5RG7H2seaarKP9U91nDbYpLibVdOxNh66npO'
        b'xLbEkhdgs4w1X/ql0UXGfCo/D7cXVhObnAtAQ10BapbwjizEc3KIy7z2lXk6yHo+yjoIoJ+HR00/QHcOdwW05w490kEBzyBP4Je0yL6oRf+9Re0ANyGdoRGg1R+0AMTx'
        b'rvgMASPyYtFmfAu1GfJMPxJYyJUB1T/XP9aoKMD/4ENAnqH9RKPUfqz5FID+qSZQW1meVRZcRt5F7cWcZrz+btgEK5huUp7HW/ytMup8TFyPM9Cup3+5ba9/if1GTxd4'
        b'u8nR9QTe9cNdJtatgGdg94rLtWXWGvMAVFpo3jUQlLvgsaoflFtDXaE8YGfkAbz7bJ83LYF8r1+fFl2lX9PrV1djK6vUm2mRWPdgXK9vGblORU/eUhrrGojrlegMFv4e'
        b'FOKUS17LbiXX3uptVu1qelUr2SDqlepXl1VqyUWiECWX0H0oMxGPzKnk4eGCXbIj9QytkbgQxfb6OO47MehcTocX0xxWg9Wo75WQ11yQzL2+5Jfj1DWNphcp0ZrizAdI'
        b'GS9yELC0ZjU9Gt4rqq2sMel7BeXa1b0ifbXWYOwVGqBcr6DUUCbner3S58zJLcop7BXOyV04z3yeNH2BcTFZEAASqBKhxkKGZL+CV0z9htlmSbnkKQVet0UksFfpvojK'
        b'eIFXvnI9+xXHpOiStWuvhZYz9GhH2QizBd8IALTh8Em2EG+LmIGv8XdSnBbiVou1DlLxdV8Wd3OMF97H+QcttZEOc/hmQSRxVLwQnpGtVGXnk5su7mvQhSjcEZ2ZnxGV'
        b'GQ3SK4hWjmM7uHOpdA4+iVr5PaW9yXgf7hTjC+QN8/VMtnwWdQrAN2LxznjiVsziC/FTGNQpT+Tdhk+gpqHx3DTUyTDxTDxqnM6fRbqKdlVCfo5h4/CZcAZ1BeHT9C00'
        b'ihV+zttBWHRrFuNbzOGLhqW0mdQAvBtKiaGVvQlyBu3yx9spkVF5o028w2mikBHhy3g/bmFxZ0YlncKECZFMIcOkvBiiKd230u5YDV24hE9DbSzDBuAXIhgQMK/hczYi'
        b'ouHT6IpCrVQoyRm3bAXeVo6uZbHMMHRcOMvHROv8euo4ZhbDrH5nvWbaV5ZEHixoYwa6BlUKGDYaNUURH4u7fhQsG0rRvki8NVqpoiLkwigmALULSitAzCe1nTYMZUDT'
        b'DPxRlGZdSqCEoaOtHRUOdXnBYC/iVgU5lddtozt4GpCCQBQlb+lhhFGs/wp0Zzg+QCs6kzaDWQdFC+M05jmWIr5bo9BhdCg+AfWAbjUTbVIywIHD6LzhfRmokzg5ZYPy'
        b'Q+5ZeSGWQ3vl+Aqt7F8KNQM0afhvRmkyV+oMfGXJqBm1ksoA1lX4VDSD9hfYeI+Sa6gtgr/xQiUClXcLuoLucxNQA75Gq4teKSKrJy97nkZ6OmQIXx2+n4ra4xOSoGu4'
        b'LRCmbNccdJLuYhnwLtykzqT+sdupLzHeiY4y/qhRMCMPN9EqO6ZNZWoZJuNxhcYcSY5cUWRsjLFCjYBb6F4RDHZPHdpNa1y0dAVfX44Tw/D9KGYE6hKibSPthffl4INQ'
        b'GnAMnS6E0e3dMIK/eeZg1Dx7aQpCdBo3Mv61ghS0tYb25VfSYGYi0IfuAM2o36yL4Ic3HJ8qi48jGOuHT0cRh94juIFOPWpToP12nOUAZ6+sRE0s7hqyiK6bqrjS+ERQ'
        b'pNmStDgoFYBepNVlxOOjkWriL8cyYkNZBRe2Hh+gK1M0Ljw+mRRQocYU6DU6X0nRPHionx3vtqFLjNTCSKcJAsd409rWocO4GUrBTAWgLamAFsn4JB1sHW4uUvNTJEdn'
        b'hagN3WOkgYIh+DY+SAf7RrKE3unrU6mJmh49jh+sPz6DNsYnA3Fn0U011Nc9Ae/l8awtFB+DfpDTfGrAjbJAdIMbaUQdvKvRpZXDoBghHjcC0qAbE/L55bRPUqVWk60C'
        b'Dl9Hu2rYWejeUD6lsXwmlICO46uodRrgoBxmiLb0IjoyXk1oWBvZQRCH4I1+nDdumEa7/T7QrL9Ct1NHaBYVFqUydDlV4CP56GpMgghqu406ZzPoEN6qo9QIvyAmlypn'
        b'ZZJdDQF+kfUhdxHFz6CVKeYuYNoA4PpoTeb9/GfsJODs8jxSGZCAWej6HAYdjkeXaDPoqBkfVeNtWSCqFKCby9lo3IEP0ZpGeQ9niNVkhlGzzhi/1iEnN6FutYr4uwiF'
        b'LNCmE+hQGL7K0+GdqCEPd4rGo2sMo2SUSfiQjbDTOLTNQA8IAJXetDAD9FzFIt4JDG/NjgLawzALgr1GgrbdzCP18Tn4pvM8J8tIJuCzeC+Hdvmi9r7Ll7+IoCdaV//e'
        b'VxN1yW8yv1B88SXI2ykmOMQA8YrCN6U2wH9GrDaon9hjykEXAHNahMwkdFZkW4kv8ivgFD68HrfmkxMpQMiC0Ymp7LOQs4lOV1xhtLoQtwNSqPAZ3M3gHrwHbaKuFul1'
        b'091OJ5OGDuMHLDMpV2RIRTfpFElWlOH9vnjLCmjoRfiPNw2nlx+x6Kg2EmYkG2/PUGTyGl9sOO4WMpMLRXHo2Dw65PGTRzCAx4HRgZpphpmVPKLgfeiQEu/3wndRG7kw'
        b'GP4b8H06aHwLb8H7+tWLb0ZzzOQiUTzqRMdptyZEeanzga+ylQHk2Ot9fLmSp4MNupACYMftwNLXsvjI2FEmfIO26o3PhqqL6EygYzPxCQZfC8H8RU5ZaH/eE+e/WWYs'
        b'6sAXUKsQ34gQ2ZdXShje7zcGJDdYxugeakynXA7tyl1FFrlSlQMFVYo44WTczoxE+4RG3JxIezUXN1bj/QJ8SQXZ78N/QNnnaeGU4ky3shyQ+VNQeL+wug5f4s8h7zat'
        b'wK0MPk5WsIExpMopm5gUbSJ+ik4ev4lhAkIEK2AGz9K7xHwSF6NOAbqJzhFrwNh1qfSQLt6zQEoJGUUp3qNhKNoIvO26EG+Dye+kY62MXoH3iyzkhDO6C/9jYRJJpWtw'
        b'dwBu5epBbKliqtCtMLq8U/MT1QqFCp0Pz4xShSWJmJBZAtwVmMtD5PZwWEX7pYtSCGsjN5EeRtv4VfMC2pXkcuQDbURXGf7MRyS/PM/IMix+fkCeJnjBmsMXwmbyN6Fn'
        b'+TCwdpYUjNJErV81h6GZp+Aro3GrAB9Cx0DJY2qmAQITbpWJmvJATssgh7/b1LmKTEIJZOimbqQQ9+TmU2vktOmT2DdLvEGtm2V6L2XsdCVDR5uvkaNzwhR8mMho9fjC'
        b'ZIPhlwqh5R8gx57a/v6zP3vNFJIeKH7/k4PfWxn8bkhIW/MLPX9M2zRxOKf9H+9/lPtP2mEMfWZ3x4e+Qxce2vG9kKwHXACe8KdR/yz4Q9v8UVF3XzxzUb54j3faK2fP'
        b'/aPoF/e33h/n1+W9sNpwPOudz4O3nVHN2XV6Q9X7V99IHzHxh2fFB59b7H35D59c/uTfSdoRHxR8sEO9aOXlH12SH8t+6XfDu3NOBr3xyitXf9F5a3Ny9sqfR1yc2jL3'
        b'9zLblKVzfz9u6QsJc2+k78sp3fnZjtE5dds+3fxp3ZUFupojf56xU/Tqhilec/1nJ6VNm2i+9ebDoJ3HmlJ/MHf7nJyUqXLz2byPrr3avfnAkKleU//4282vznt10pTW'
        b'8XvGLT5f8dGQ9p9/f+yH2m3q2O6fhe//Z8mc7+9R4b23vpnzg67da351duc3qu5Lb/7WUDEiOfWtL75/J7fhmeWvmQIXpv/amhhk8/4clf/64ktnd5yYdqz3i6BLvwsr'
        b'amh/eO5X0wOurvW/vUv81cVJ+y6prtfcm/aL+34vHqw0zv7boUUXNnf8fYv1xX0vVMuuftm6dF2Bsbr0dMjniqmWkZZbEzpbvrr46v2WP/1LFf1o1MxXkzrHZjYtaPLp'
        b'mPRv1YZfBs0csma3uv1Q6/l3X7sx/5+zP9jz99/P++cnD6pPf161M/nv3TeDH3z45aK/eO35S/6nITnXf/r4o0tBV3bNLplh+6Rl+cTsz1LfSt314J+CiIB/VVdlyUOs'
        b'xADuPQQd8+QGgO+hLi9mUpioMgi30HO9OT6rI4lVnCtcifax2UJ8kfdRuI86xCAGgdIgZoRz2dmlEHMMH6Z+CGVF+ag1oFZqxtdQe0Cdn7cY3UJbmFB0SFCzbjG1F6fi'
        b'A2N80ZmoDN5qGwFsPAjfEaAL6EYUtbY+lx7h5geKbqSjy8AYdvPm5jt49wTUGm33BZXgNog5xqFWdJU/yozbUYuFGn55a54EX/XK5nQSEfXzLcKNeBMsJ3JW4mBKHZu+'
        b'Eu2lw4rOq3I93gyLuoVT4Ib5vCca2jTBfvJOqGbxLT26Ahz5Ln9Q4RzeCCyBOGbwXhm4CbVzQRvqaXcXLpjg4pURhzY5jN/o8nh6nm4uOjLL4R3BO1AUTHa4UKAGLzqr'
        b'HDog68uTjc7HjHT4T6zAHfTafLzPG8DQSs7ztROVJQuGcC/EOQmRU0XoxnB0njpkFI9Ax4nl083qGVnP2z1z0T7+cNlldK/Y5QDEOB+GnsQLLqfJKWtASyLeGnZXjVkr'
        b'qbOGP7rl6Zr57+zK2SvQ6niLDPEmdVpknmOUxPdWyAZThzof6pMb7PhwwWy/D8SN8ApkJ5Kzz+xwKEH+pKyEG8HKWH9aIpD1pzkDae5ANpTUztX79ZlaoC9u7r3EhvZd'
        b'D5NxfKk+8/xFeJwl5h6CfU5zz0bmnRFuzr5uvfC8C04tefwblZhmkdOSx1IjxMB74RVP7rrJmCeNEFN4I8SqFAGTEEYOS2uyPvcezfDmPbKcFqOrQYgcpRoDCtF5ePag'
        b'Q5QHJVhTiNLPhOEb6DATlqigO3WoOQpUDqg+rlrPxEkTeX+u4d7M1grg8hpNVtKMEIbuvv18jIR5yX8KiZRqS4J5SXT3xPXs3Ol/FTEx2pGT59nvVpmcOCM+QWgB9QZE'
        b'GqYsCB2hctNsEOP3xSeIURO+Qg4dMXpYHUdpNftlwDENsPhkmqi3qlbydXPBgcyfatNBedYYj82I5HthEAUyeWHzSKR05IJsuxNAsR8jFSaDKqvJigrM43P+c7Yf85I8'
        b'hkRK76xJ53NGVPgwy7QgmQdqjHE+z/I57/r4MLKqCBIpDUjn+MgNs8XM66NGki5lfZBTz/Aa9XHUgs9RsbAIXRAOAfVXVMeiO+G4i5fsdiYsi4+JEeKdIFBOZNDzS4tp'
        b's0HJE5jzE7cScM2+mB/EQ6oeb0Rn6TZpPepAe5n6VPQCr5gcwzvi8H4f4vsKQDwLX+vRPl4bvo4vxuL9MFvoZhRqgqd4EoXu5GE+uBNQRkGcfxnFKl5qNiwXMfeIyXyW'
        b'RvpeQI59ED34+AzcCdo8fIiOtYWZCV25jm54UZSY6TUXkapG4+bpzGhOxV9Esgu9OKZvN9SITvK7obgZddFOZ6CNqgKyG0THwuKdbDDeN5aXOy8VTCMHV1aPwPeY1fg4'
        b'vsuP5Sa+NpIIlcwaQIkXmTWjUCt/ouUY3ooO0L3itaPxHWbtEPyAbstSwDwuETIfkzsGYEzpAXN4C/GsqFvUseAVEMo7ew2dajFrSYAxTB6KqnemkZtRtlTUfTbxJ2+p'
        b'RjUH/qaWmes3+gPuNoreceD7Zr9dTb+NW/DOZ0Feh+dOFX0g3DonZvmUl2cnpP3lubt/6ZXfenNqw54I3yNDCz9ubKsMP3b44cvDjoa88VXlkvkhfz1f/rtz4mL1C++N'
        b'z/jjm8qutT+fO2Xxyabt+lOClk8yC2uGnei80fNiz8tb1ugvHmjaMrs5sXdloVn711Of3F397Fv4HfOdLb2fB3z+9chvnvmwZOvPan5atEfQePF/tXclcE1d6f5mIQQI'
        b'EBFFUTQgVnYRERCtFQUKIpuIGyoGCBBlMyGijrsgLuygorjgWldccMH9zTntdKxtp9NV06m1TttnZ6Z2e51ap9Z3vnNuQgIkxZm+5fd7j+jJvbn3nu2e5fvO+f7fP+Ho'
        b'iPLgxQvvNyWhzOqlLcpX7gw/7J906rTt0NEf7E3a8K22/MnZi08Hfh4x8afgiwWxEecK+t1yzZVdmLtsW/PC9LvlMRENWq/Qbdfq3nIbnPDlzF1Nrx9rDvtjn6S/LivJ'
        b'fc17vt2nf7/5ZZ8VaXe+O7m7fsd9VPjiu2Oef3vdun8M/Uvo+lxJqO8AamSRhk6mWrKxwOvxXqN131m0ns7Xc0O86T5+UqCfIKaEzPLnhWjbMryVCQl16LzcTIjA+3EL'
        b'OoN34AP0aRsySW9jU2qgCFd4U0PLDHyMQdwvLbKBqTQxURYJ61nVuBrg41Ei1EZkp/W8/xbS8lrQ8Slknm2k4KBNRG5YJfRCF6ZROQvfyEBHmaC1g7S9bjaXRNDyy2Im'
        b'59v9syAr/rDG0CawG4Na++EWunUehc/gJrAkQZfRer/AIN6UBLXhzVQwyERbVkAauAE3MlA8mfkFXP9Z4kEL8Xo62eOz6HgET/rjFkIh8bB85DJchE7gU6iNZmG5GmZz'
        b'dErmMNVoWXo0glZGtsCF1hPaZWeUUIzyyXEdzaZkFDpERQW0N9QAlwRZAW3OYRV6BrWtprEsxmcMMoxBgvEvZBas69AFDGJJXMAY96AgWI8mucRHRbgxAq+lG//j0X68'
        b'n6cQqhjUxTJ1PG5D15jk0pZXQu+qSbDhxEIB6sDX0R5cibfTzOpQK95r3M1H56ax3XxyfR2VpOyiV/JmAxaMBibHSgbPjaZJJRDZ84JRGMUVQ0g7BFl0cDATyvaKYO3c'
        b'VCgzlcgEuJmUucKJNdlGtCu3U6Iaixt5+1d8cgQr1jVUh+uZk54ADnd4Mic9IbjCsFXcq10vMRjVUclqgblkpZEJxEIDMN+VylWu5NOffAaQD5w7UZC+K73Dhf8PH4Pf'
        b'GZnQXqAQwg6pTCil2KnlTp3yCyRswQTNCkDK1CKNTPHcwx5EpiazPbIuSZIYRCyiKvqVRP9pQDjxdevKNgoGtpolEFCjW2qNC4a4eqnBPNNwBJtI1LCRAaHAkopaXNBd'
        b'ebpjSzf09LLMlKhpUYmZ02enxKTpRVpVqV4MOHq9A38hLWZ6GhUGafFYBf3rnhk0wG0WAHUFZZCK5H16hX6ycRI7OTpJXKVyW4MPBgl9vRKzj72IvXZ2Juxy1fCR2zgJ'
        b'XEUDoqkHmiG4FYi9PNCxzkHehpNPF81BLclmG8oGahPqbMyMdVXc5ExZSZ0N3zlC45Go2jbHm8jAgHNwzhXn2OZIjRysdjn2FJ0i4zlYHem5Ez0HDlZnei6n51LK0WpP'
        b'OVplPAdrX3ruSs/tKUerPeVolfEcrG70fAA9lzWJcznIVc7AXcImCeBPFjrmuA/kWp0AqcGfDzKcu5H/24U1gpzhPK7aljogcqh0rpTn2lEmV8qvSq7ZUbZUMUW2SOfI'
        b'oTZyPKsFlUz2l1U6EsnfK2cYZVLtkzOY2k8+xzOpJiTFPN5mBkWebqD4JJcYjarCB3gzgAZJWZQDjVzdlYnR7MRvOiCied4jclScpS0uAIZmAHKD01vGKQlOd1Ulpczv'
        b'M0V1d/FFbErY2oV61ddWb8eTeQEXDn9Id3+lzDsnsOLk5C7RixYVkd8KVTlqXSH5TVpCylNWrMnRdFK7duNUNXf+ZHCybUe0KHt+U9fB6Pzpl1hVy33Fn3zTa1ZVqPJ/'
        b'mlX1l0lVuxGo9ght/ydJVU1egjEf4KbbSi7IZUt5KFIoC0rylYE9ZWWsIjufJJlNnWFb53i1TvHaA53rM9TIL1K8kvbH/AZHx85QFCizgGScHJq6YvYN6uLkmPGW9ZgL'
        b'86zTuvUJMamKHjLPZ4T0gV8gmLVEJtuz7wNLBLO9JJPtMdJOgtl/gUzW0M9ZtbMzhTqHf2Gjf+mFGQYH3lk0f6bQqPLUWlLDZKgiIxptTgEKHf/adEXgtPmZOVud2QJK'
        b'qKecy1/F1hHkruEcdXU6LAW9ZEpfSmTMU0Z21alGcd6MsbViokyO1y2gkdovcOV+8pgBqukK/XQJT9i6HZ8o7JGv1RgjJT0xRlqG2ki8e0tk+ODIWBrvR06O3J9Wj6Lr'
        b'G39xLeYYYcqaIXifZR7YVegg0yxMc4s60EYHMuk34MM04mvzbbnoVA9Y5JBNVidwOhjt0amsFBIvPk1E+25xx/unmca3Btfaoa2ZfjS2WLmU+zqeLhsF7NWVsGwuJKpG'
        b'Q8+csImJeJMd3sPUuS7ZvOBAFLuLaAONeIncngst9IEFmoD9bk7Mwhutcxf2FK9PXEAQ3uMQxOxnTCK9jI474I2eI9X7j68Wa0H0HN7vQeDrVxyFUbKY1N/8PN9n/aQH'
        b'SgfFmfIlN+X9gsVBIvdW14X3q8fs0z1sD9xWFVkWdqmuX6PH9m8DP0p2fv+tH2+GBXR88r50HG748Hblpdq70aEDq/f73n257LF8/JW8pRU37r3xPN68+th3ad8XDnDZ'
        b'bv/ayNdeuRX2wpiyE99zT39biy8q959rmPvUZnNE1n888bWnihls2zWAtlOODk7tokDiQ88xqpLKWascEiS+3QlPWtFuqpfhw/mguSXjc33MGpkNNxQ3i/Ep8SymiVZP'
        b'II900s8a9NAQ0kROoH3udKXdA51G+/wX4cNMzWGg7/7BVEsdhPZLqKK8kFeVUSvamM4W/dtQvSuv9CWgNUzv24NbPGkx8WFbb6bQm6nztugG0egPZjAd9RT4UwP100z5'
        b'rMKHcCM6JywF58JD41zYGkUgvjgSt+MLWrpMQX6YSuXZQAmXiMpt0W60G2/81SR5IzgRuouJwraam0S5YgWSTt5YxiFLnX4azwzUrETqsMAiewmCyxBcgeAqBNcguA7B'
        b'Da4X1qvS3kTiaFYmXzJcakGzNdHk1nB3zByodc9577lbjfKSFehZOskDAzR2pmRCJws/WaWTfSZMoyzTRHiykqlZhkw9HtIlB1QYeHZyU7tMg5hkJdUMY6pDWar/Mo2t'
        b'OJOIRlZSnG9McRBL0USAenYeVXEmkX+spKY0pubTKSMpu0JGn40o11i/BonESvo5xvTdYX3CRGx5lhSNcFGD2GIlxTyzFEn9GkUd0zYsZEhjutRhtHlNyhbxGQGbceit'
        b'1OgV7PPpLhP4XRDyuqo9dZQry5UZLchtLFqQ877Avrdx6TUVkQpIF3vLRERvfhYiIlPioW5RAhGREQzsF6DwM8Ukk3MKciY3mdKoUNGVZQPYKXqv3hkTilSkFReCksB0'
        b'a3BYxgOLlVnFulKe30dLxFFLdQN/wKWhgirJUedSppVSXtw2LxRf39QVI6m2PN4dWw+SLvzFG5mBlNY0t1FhJvqKwsdAP2JZczGtVyaVd+uYCp+oLI0qO78ImE94NY46'
        b'Zesxo53tQKtV5xXRpsD4RbqRXGkVatNSqYlGk2eBxMSgqYyiLzlsrFFhgZRG+QbAaoiBFxfuMBLjZlvSsWirVNPngWsJ6i5ibO+5mnLNCwSlVqu0vx7Tkg8wC1FOJF+F'
        b'n18haNGkOMv8/P5p7iWFD+VZCmR0Rc8StRWepV49/6ysRwoLbE2WWI+CepcNMwSGVe4jHyP30ShfRcaoEMvcRaYoDv416lSsOOoimlFKVB6dmDh7NpSsJ9es8FeiXFZI'
        b'HbuqNDAxBVBiM6Pya5KhEOsZskrIZL4UwnrLSENP6TFbTOwxpXEiyY8OtszIZYp5MSwMmXQT8ivpkUVaNctUcW7PBFc5C0nLoPUBD1DvtsqlcNxLbh/4izKLREvXxNTZ'
        b'+aVqSuCk7aQX695nLcYZqBgFDMkqHRlcjRGQFqxW8FVERqhC0uNi0gOnK0uzVLDO2DPdVKCCNBfmgbNAV7hIld9z/QcqRne5jaam1OUu15WqyMwBno0VM4o1WpopC3GE'
        b'RiqidLn5qiwddD3yQJSutBjmt0UWHhgTqYgvylEvUZPGXFBAHmAkaNouJbfwdFhPWX72CgrvKRq1SbYKny1bET3F92z1MpZWZGfV/0LN9/jjdNaSYUGwS76fuSWaFj9X'
        b'Q0rjA3VrzJMya7kuz9dy8zN9XBE+3HIDNLtx1FhLd5JmVjSyO78kuzimazRhlqIJsxYNaRTG8lmJI8L0NotFG2sWWQ/lsjih8Zg8MsLxR1QeIDIpGVsNQ7lPGptjLU7Y'
        b'nZA/YDgnUyE7IzKOTwI5VRWR/6SZK2AOirBCkm4EC5pHE9IlmhCr0VBcoRkJnw9l3ouG+WaMxceMOET2aEw6HanhB4UP6eR8Eyev3XI16DRARggs7/xRgMJEtotJn6bw'
        b'mYkP5mtIJyV5CbWcFRMIZGdkxp/5TBmi0i7SabTdM2VN3LMkXlJRsveSn1FEizJb2++dDEPBmpGKJPhSZIQEz+v9YyHssRD6mOW3YUCB8iKkgfieKMvW2gGFiJJH4Ivc'
        b'2P0+y6NYnEqjKRoZq1HqSFAQNDJWTaQ7y6MWvd3yWAXxWB6fIAHLA5S1lMmoFJNPhDAy9lsemmjeiMyW03M2LFUekWJVqlKQLOCbCFhhVuW7rOKlkQrYMCbyUy5IreQH'
        b'UueWXyo8BAhd9pSyQAEnVp/IVpdChyShVXGPAZPhTnZAIw4AOT1w9KiwMNLSLOcJEMEkQ/BltUXmKklpY8mgYu0miikmbwi+FBlhlm/khzkDz6iVFm1AO0cqJpEjJgln'
        b'hIRbvd/Ytekj5nt3VuvbgKHmn2Tvx/JgDdhpIqJNikoir8fyiJilziYRxk8mSffQI81Q0N29ofOMSeHR4IxrgNqWWyCbOK+QMd3jJrwzyxS9BtC1o7gJbZXgM/QxNxlA'
        b'Tm872UxcIBu0KJAZwqJy3J6REB8Q0J9B69DeeDd698ehgMI97e6gWLDivYEi5ltI4FkIVBFoz1gA2hXPYSjDk5MiOmHKnANulQBM2cOFxrN49ArBI+GCoTbBykE5nn4c'
        b'5SWcgg6iQ/7kdqDXSwYbQHRiihwdSwS2yfjpQKKzZRq3NNQuLwmtoeCezBRgFOSWnlb/VvzhLHnZHY5CuPGhxUDz093XEEQTR7chtEsCzfgEq9EOme+kIPXQr3dz2nsk'
        b'jp+9nlbUJE4RpcrLjz9+Y/XchLNl/cZPSro3I/hycW792qg97Zte7yhxjWy5Z+ct+MNzQ/APK2xL3glNfy9z+zdnUoYcyXq7389vPjo3vay133M7Ty54I+Dn3+1K3zYi'
        b'Zt+PV06UrOuf96Ym+t3wuIc1fR/7Bz7Nn/DWnJPCN3Z/uuvqwpI5f1jxmfSA6mRLxNt/mff+1p9ffa3jjXcP93065tPLG28+eXuBbpBm7zcZ0alxVX9asGXVbqXP5d+t'
        b'7tso/4PbhQHD5xdk32q99vvnh7xVeenG1LJ9yjsb2l4McWnr+8n6VU9emLx4y+Mv3b55L86+FftKmR+udcPRwU5Qhwc+CX6A0VF0lm4nzUZXowHUgc/g4waGuvyCUgB/'
        b'jcStaf54U3I8OiHmJJHSAqFXYBm1HswJmNfdyyZaI5cm5NEtogEheJthj8jCBtF+8htsEnm40t2zvH4xnd6MaKx4s73RmRG+gBrZ/tQetBFXmXDZzZ0D5EmMy67/UApu'
        b'wfvw5tiEqcvx9ngBJ5wm8IvE27rDMWS/krdtsFmj+1Kw72y2L7WaS5ZSSjqxwEngTZ0bwTEYBdrze1JCalLoTr77C1wEy2XG3RdlTk6SmWeNztVpML022Yiye6aM+4pN'
        b'Iun0rWksycIed6OavUx3o8xy2TMWgzpKAjsirlJsdJT0S3Q+uf/36HzglXQnyBvOhvukPmTcnvi+LbheeydoOgMS4HW4/kVUi65qdYAZrhZzpHsIVpJx9VonHgXfwNV4'
        b'gwM5RzUFM7mZaC2qpHDqGHRkXtoYtFNOnxTgKxw+h/fNpcm5260UPFr+CjgUHvfDcncGK5mBb6SNDpVwqHUmRY8ETmEg4C34eOToUDGHt6O9FHCCdqArzFmxvS0nW+Av'
        b'AQzH2+lqBgF5ZNuHU5QMl3AlCwKqhhQxUIHLNDmnUEjEgDVZGO7H7vwiS8YNUBwRcikLCiZO82B39iGtdEDBIxHASuIifdmdf0904FxDX7UFAwWf1XPZnTJPe841IEsM'
        b'Pybkj2M/+ulIlrhb1OLisXsqw6gXo31BaSn4UmJKCpnfojm0VokbGHq98kX30cElNkAfKMAHObwWNaazYtco0Za0FPDKAMi5w+QSPpJCaxZfiOoj7G9EqTCISuJKGqGc'
        b'DHZnRwcH4/OzxAyigjYsZxjZE6hBlkYPcJUn54m2pNLfA4PRPgAIocuoNoQLwevxdfo6QvBRAYWcoNqZgVwgriqhM/FC3DEYwCWo6blOfAk6r1FTgO9svBefSEtBzfi6'
        b'AppEez8J2oe2TmSuUq5EcvgqOtvFpf2UxECG/oCa3ucq5eTiMmpjEjNPwSq1abYdJx/fIABo0g/2kQzG2zfVNS0lJRuwRhxezynRwedoDGkl/Tgfn9vgRXDFkmGZDEke'
        b'lELml5R0fB21+nJc5EoHvA9VubLaPBON2rWOy3DH6GAxqenjHL4Who6pB7fJxdoIUv6IlPrCep599/03a7/7qjnC+ycb+6So+JiEteXl5W81yvYtnjT5TFuA9/ax6GG1'
        b'/H7EMO7dwWs3zx43y7V++K2vPvz+6o7w5KbUSQOLH31/ISUhpOCLhrAVZVuPrjv32o+freh3y+0z2Z5pn6tVTf0cD11rDopr/+bewKET3Gvyzxe0/nji/R/yDznnuwXo'
        b'WqQa1RzpibTCvq3ZA+e91bKzvq6mbk/dz9uWtk15c5LtpMqn+RcPTrM9sPn9VV9J33GuWvSkwudJ//dGr/zb7LYfnfc7vnT9QZRuXfydP8vXn33x328fya216/ty82vt'
        b'mUs1ed6+8ts/PvRq9nx5/I6MME+ngIzcOa+El0/+86LUgYtuLnnyxbcNq18NuVnf4TGz8V7Oi2Ft7dItZ9srvu6YsuwfExL1q+fPuTAsY2xj9VtjbGpvvKtdkjsvzteV'
        b'4kz64nZHk/l5SKAlEw7ckEUtS15IQlUrcZ0/nfTJVSm+IkT1g3AHFRTS8dHZ/lPwNnwqcaqAE3sK0O7ofgwWesOpBNeiOoNTQeZREB2zZcb8+3FHPgBUUAfebsJgMHoE'
        b'da39Al6HznR1o4C3BIy35RQxNnZAEEYTsUMgSG5JluGL8UabGHwR7+MZVeLRcd4PKUOOxIePxm2FDMBSp30eoCMmVj/ouBsY/qxYQp/2Wy0A+vFOaEsQvuSFO5ZTaSRq'
        b'OD7QzZSHdMRNACtxH0HrBh8Y60PkqwXompEAeNAiivWIRQcWgGsLvHVkJ6TECa0XTSKi7SaWvcrJeDdgSsj40OJvCipRiHmmyHNDIA4ZqjACSpxWiqJx+ywaQQje5dzF'
        b'nOeIB4WTaPozfpzreAO6BGZBq8ihASuyB21GDNdrl4rK59iaM0UUoyO4ghozoSseuLmbTREuRzUAE5oooxggVIPPocOmtQxmUWROumQwjcLl6RbdwVmXvhYbpK+i7tJX'
        b'CUhbPJmYUC5k1v1yHioLgA45kb5A9pITaayTY1HO/2e2/cBZIRGKeaCHnLfyBzsjnjWMykHWicl6Llo3ijIQvQZ3Fb3WcHvMPRl2TZTEA9w5/89URv/++5nKbBlT2XB0'
        b'hfTUTqYyU54yXDHNSFXWPIzOyf0Xom0mtGPpmQK0Dp3Ap5luXkk+L/nbgnOY9dxSbimuKGYXriQPA9YxMqK2CYB2zA2dVMvuvcRpT5OrqYnLgXYMBcuj8z5wkq/af4/b'
        b'2NAgSlksmDjFp1W71qdO6Or7tw2hGVEJ6o9dx9U/uLsw7+7Gy6jxwcTaQ96fv/zDVp9TkcsXTna8Fhey1yZi49+vcR+HD75x/uW21HWxY4+59V8lP/3KslVZrybN/vaS'
        b'6riw77H90VcrBeUZfyyq1n9U9if3EV7vttxQfjSw/MNPMxqiz332b7HhP+0YW3h+b+yigqbg28raYceK74u+veUsvBpeN+1bX2dq65iFGtFOI+vYQHRIgNpQ/XQ6QXhN'
        b'I5MK4x27MJhCZSjvGNodwob2GnwU/AXzxGKSpAJ8VTg4aTEbO/cIyXUjsdgce6GBVmxnMsOaHQ9A9Z28ZU6LhTxtGd7KHN6OeyHeyDqGasngSVnHUokqConnElG80sg7'
        b'JlmF1s8S+qFmX5rxyXNyzZwBp+MO52BRnheuYgzHDXJ0yJTXce8Q4TDUkESHZNtovNOEdgxvet6Zso5p0VpaYSOUM42kY5LxeCM6JXTzxPWsTKfRdlvGO4YP4/ogA/MY'
        b'PoIb2ZR7Oo6I/Eb2Mcmk35AJeQC+gHewy63oKm4xw4yOAy7etS+yfLeiI+iagYFMgo4sQluFAQ6CX4WAjFJm0cHcr/tgvpoL9LLOQQZj4q/OQTZUbHBYvKbL5889sJEZ'
        b'skASN0fcMOydkH4l+bp0xdvpOM4UdNcLG1KgGdTbqEtVhVqGmuvCOdbnX1rd6MW7ukgCTxG/7CGViIVkYhX29+k9xRi8xQECRZnLOLaMWYFPB1BiMSJ6vEQXjWw4R3ch'
        b'kaZ2iX0FSWrbpB0i7SAyJR1Y9XVMzSUGL/9gyf1hlV8+2qi9N97ew3li1INpP52t8zrEhccdVA6rfiNt9CLNshOthUuu/1j7o90LyfPu2sRG7d5de+DJ5Jne7aNf//5j'
        b'2Qdn2zbkSeYllH3kPWxqwrqn+TsevPnmP46m171e/P2k7ee9/nF58vE+7qov/OehPze/ZTv+k41uVz9tTpu/+Hc2X10q8opu/uinu7/xujMCaf/u7qwNKJrQPzYzPsy5'
        b'GrmcqXu0peqd4/XD4yoOiQ4U+TcdfPGbppXxLc6FN29v/26n/92va56/Gz5wxu9fbhlY+G6651e5Nt+7j6vxvjhxmcPymd+e+/Snj3dpb7Z1DDuRuulKyOWyDfM/fFC1'
        b'++aRwOjCca/8tvK530oyvimojHVcfvjel27Rr+QGv57gK6ILYDpUUYK3EElMEEFGtBZcg3b7MnTxlQjcZFi4Q7sXm5qx77Sn7qBnuOLqzoW4xajF3Ku4qLT7Stqg/5q2'
        b'9swBGWlEhr7WY0CRv9LMzIJiZU5mJh1pgAiBcxcKhYJQgYKMLBKBi1DqrnB193N9wXXEeBh3npeKnByeW80t0bxj7F4ivTAz02RYcf9fUHqB5l1j74ScwnDOPPk+mGhK'
        b'jga9zQ/vGIi2oFqb4WSY35Q8FW1Ctbac00CRBzqsUj9c8FCkBRTvrcupHpvGEonC1ebpDw/lE+OETgWbJ2aNdZl5elJ2WVN85X88uigNH96xc2Di/egdse7597c//vb3'
        b'ouTIo3f6pT3OHHb97SnNR9v95x+Z0Dh5U1aCfOaHnx8OiN46o+PCrVtnXbBYODlqGGqNcnCoHBN2O6vyeaeI/etftcsTzy15xfGH6wkTKsrkT/7ovPkPQ6VpPne+epkI'
        b'DDDH2Q9TwbSbDPsHQFnsgM4KB0XgI+gGrmHN/CW8cUlCciA+gzcNWZmcDPNzH3wVoPrn8TnazKOJ+HUIaoB0jjpcSxWSaloHLqIhuA1tpWvj/iTSHQnxiX6JthwZ4qbk'
        b'SnELaqVOl+3Eg/CWkRJOkIbq/YmShw+lloJPEEk0vuY/xYYTJCSO4HBzTBqdVqdkEqUH+PTAVX8VESR8hblEX6ubMoPN2jVov5vW5Lp9PJFTStBpT1TFw+JnoasJ8bh9'
        b'MmjsTA10wptFSUTeYTSmHaX4DLrsbnSViPbi63gNrQ583J3oeCBqxvF4Y1lfoSMigg8+hg7Q+MvsQJEld5Twd9ijdmEiEUnP5XvR5fnf4HV25IazMrSxbLEOty+WLdYJ'
        b'uKwgN1wrQlVoO9rC9hpeihyVQB1SQGE48mp2Cvs74v2Ts0q94fLBICVU+sgEMqiQshI5dgtU+qDJ6CVvMVpPMt1h5ifa43++X3XtZna/MMj0MOZ0YlcosaqjlDlfotol'
        b'6KMy0YSuwo43EwfoYDNULypQFenFYEittynVlRSo9OICtbZULwYFUC8uLiGXRdpSjd6GLjjrxVnFxQV6kbqoVG+TS0Y78qUBuwugRCnRlepF2fkavahYk6OXEFWoVEVO'
        b'CpUlehHRsvQ2Sm22Wq0X5auWkltI9PZqrQGlq5eU6LIK1Nl6WwZn1uodtPnq3NJMlUZTrNE7Eq1Oq8pUa4vBNFTvqCvKzleqi1Q5maql2Xq7zEytiuQ+M1MvYaaUnQMo'
        b'K6iH5ms4/hsEwEKn+QiCP0FwH4I7EHwKwccQPIDgEwjuQvAXCN6D4DYEn0HwBQR6CIAQVfMQgr9CcA+CLyH4EIIPIHgfgq8g+AaCz81en71xNH0UbTKa0muPpblgL52d'
        b'H6SXZ2byx/ws89idPyfKbvYiZZ6KB4Urc1Q5Sb5SKvoB/yxRbXn+WSoc6u1JjWtKtaAM6yUFxdnKAq1eNg1MNwtVMVDbmu8M9dYF9KCXji8sztEVqCYAaIGuKIiFYqG0'
        b'axMLd6ULHP8JAgmO7w=='
    ))))
