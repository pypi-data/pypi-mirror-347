
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
        b'eJzsvQdYW0f2KD73qiBAYMAVV7kjQKJjbFxxQ4hiG7fgggQSIFsIrIJt7LjbgAE33HHvuNu4181MNsm2bHaTzWbZ7G7aZuMk2zdbsinvzFxJSJZEnLzf+/7v/33PmMud'
        b'3s6cNufMfR899U8EvxPh1zYWHgZUhMpREWfgDPwmVMQbRcfEBtFxzjrMIDZKNqIaZFMv4I1Sg2Qjt4EzBhn5jRyHDNJCFFyuDPr8+ZApk2ZPnauorDI4zEZFVZnCXmFU'
        b'zFhpr6iyKKaZLHZjaYWiWl+6VF9uVIeEzK4w2Vx5DcYyk8VoU5Q5LKV2U5XFptBbDIpSs95mM9pC7FWKUqtRbzcqhAYMerteYVxRWqG3lBsVZSaz0aYOKe3vMaxB8DsA'
        b'fkPp0KrhUYfquDq+TlQnrpPUSeuC6mR1wXUhdaF18rqwuvC6bnURdZF1UXXd63rU9azrVde7rk9ddF3fun51/csGsOmQPT+gHm1Ezw+sjVo9YCOah1YP3Ig4tGbAmoGF'
        b'Hu+JMIkwHWVKUX6p5zzz8NsXfrvTDonZXBciZWi+WQbvf9Lzs99E9E0XXzCqEjmGw6t6DCKNpKEgdyapJ80FuI1sUZJmzZwZKikaOVVMHuPT5LKSc9BadUPwdZsmj2wj'
        b'TSptHmniUIiGx1dnk1Yl7+gJGaxKclGriddIkFgcTi5z+Gg1eeDoByn4gITso0kq0hAURZryJCicbBXlB5HzUJbOqa6Q1ONGsjW+mjQWakgTVBKC23l8I5+0OoZAhmi8'
        b'Pw8yXJfj+uXLHKR9mXyZowY/5FBvsl2Em2JIA3STDgmfx/fwHdyItydoVbG0t2T7NHyQRgShfsPEeONysrGUewo8+7mmzUzXUVhF9O3Wsayfcw25egDj53lYQ46tIc/W'
        b'jVvDF3q8O9ew4uk1pJ3p5bOGg4Q1HCsLQnIUo++m0MVXh5oRi5zD8UiMKsaGIp184uJRQuT3y2UoAq1bGKbTxfetCBYiv14roQCwmpuoM+OQeNSGzCEQPWNUH/E/otDE'
        b'v3RfqQ8Ju5V0YO4KzhwMCdvLD3D1qLQbmqhLfjt5weLfIxZdGvv3bv1Xxw3iZ7zDfdWnnVOgDuRQ0alvy+4H4NSYMDMmhmxNyFaRrbhtdkxOHtker9ao8M5FOXkcsnQL'
        b'HheHfZcg1DXqXGEJvLcRogtQFuqeYv6Zp9jvNpH6TLE830p7wSC52CwtnKWayyPShq/wIkQOq/A9RwSkxAUbCvlcUo/QUDSU7BjviILIWYPJocJZBeOh4go0FZ8gl1g0'
        b'OUguGkiLaOIyhBJQghI/dPSAaCU+jXeTFg7fJ7sRUiEVvpbioEtO6vC+ZYV5M0mzBJEt5Bq/iuvfL1EA6nMDV8LMNqX2iNMCQDfkzozBbfHZbJ+qSZsEb8D70xyRkDMH'
        b'38Sbcbt0qQPABY3NyDBZa99FtlZIOt7/40U/SQrfMDFi87sH1m9eFBcb/m50/CVz5c2k7rWyGu37Iz5YGfrevTdbqlN75+W+uWTrn7+MfuPq+qM1p/448Mm9xYYTDePi'
        b'fmN6K47Ujpnxu2N/k/c2ZLStWDw/VHXyxu67mjUb/97/b5fFjl3mr4rON8+deT1s5NoXXjA3Pl48Y/Xnac/3uvR+wctZqpoFP5v1TtC/mu+d3tS8esQvH3Ifb8/468cL'
        b'lRI73YGFKXla0hxHmvNUORSPLMBXo8gdEakbkm+nKGiyCj+My6kgV1SkXpObL0Gh+BpPDj9HdrDieJ9oeZyaNOMLypw40sDwTDeyTlTlsNkH0gler8EnQunEOQAzbE3g'
        b'kZZcjiT3RPgSfpxmp3gI8MUmfAWmeivZTppEUOUI8WgOX8OnyFUl38HHKK0UYpSh7M93eFDg+7zX2DJrVa3RAmSFESw1EBtjzfiOMKvRYjBai63G0iqrgWa1KSjEjpdx'
        b'EZyMC4GfXvAbDj/0bxT8jeCjOKvUVbNS1CEVCncEFRdbHZbi4o7Q4uJSs1FvcVQXF3/nfis5axB9l9AHbW4C7RyjhkTBSzmek7In/wXPw/bj0Fc05KC9XzUrLy6HNGsB'
        b'AWxNAFywLSGHQ8PxNWWapJicI7u99ib9J3b+tVXAw0hZBWATDFyRCH7FJlQkgb9SA18UZAivQ2WcQWyQbAoukrF3qSFok6womL3LDMHwHiJQ5TKRIcQQCuFQCANqgbDc'
        b'EAZhuYEDJLFJ2a1DOovNXD6bySdfAX4qFXl0iw49yIU2KCfjrljASaJ6EeAkMeAkEcNJYoaHRGvEhR7vXeEkkQ9OEgto//kshrcVOn1t7urqFGTSbH6JsxVAyjuvKz7R'
        b'/bjkI90uQ73+Y11T+UXjRxAu+t5CcnVH0uaZh47vjXyxQH9Ob5ac587rfijeGT9APlU9oCl0fuadM+s+7hM9q8+G6IwFqPr3Ea2hrymlbJ/w5BKpi4MtcMBNQeOkqBs+'
        b'I6rFF2rYVpORg4PjXKl1A4EGI3m8KIjsJnUsPQ/vmq8ljbnATCilkHsXPou38itgvY/Ze0N67hrAjoDQtBrJVHwJ8HEGH01uF9qjKUAdHZiEGws08UPIFo0YScghjtwj'
        b'O/B5O8XNk2eZ41TZjM2QySvJDR5vGjpAyXuAqsjfnmOQ2yErLjZZTPbiYra35HTmiyI4+iPlxFxtNwEC1K5cwp6SdIhtRnNZh5iyhB1BNUarDbhHK10ZK6WHbZyr3XAa'
        b'FUYf3dybhTaywL1ZzkYE3Cw+rZfyT20KN/SNcUJfGe+EPZ7RQxHAHs9gT8TgjV8jKvR4d8LepqdhDwWAPUc8vOPjMPMbQ0kzrNY2+N24KIFsL8wWlnbmDEYlJ5Dj0khy'
        b'eKDJaPuzyJYIpR5V//ITHYXEmNL4qDh9rv5TXURpRZm5RLw1qb9UpfuTbv4rfX78vQPh6NhC2VrRP5VitvLBRbFOoMHnyT4KOBRo8M5J9qGQOhtv7kvaAa9vJ9vVqmon'
        b'Cu+7RgxU+gIQvTayzd4H8k3H6/UMfjS4nex1AVD4BDslymvwfZG2QAUzUsXXcJOKyB1hkXm/8AK4s9xoN9mNlU6QoagPlYRwcq42yr1c7ixCVWIGAh1ii77S2Akl1gih'
        b'mSg3jDDwoDS71A0eR8MDg4ef9v6P4adnh5EYeA/RJofiLckuGAkAIFWzTcv6/4CzJUOJKRaxf/j4VMdvTXYkvpV4KlGcUn18zi2ELqtk6//6tlLE1nbuAnJfG7ygE7Mw'
        b'ADk7yT6MIo6LZB/ZIIBIGqXgXlACEFKP6xmclZF15KIAIgw8qshpgBB8f5iTiAZGIAAQNl+AKH8KIGzeACER1puufIekRm92+ICFyAMserhhg052hRs2DnaBOvw0HRh7'
        b'jBdgg/LXXJn4O2CQ8qehg3M24Q0dknyHmr7PIG1U9ptN6lUq9czsnDmkvqAQ+Fe8ozuwsNnAzao5ZCcPg6X4XJ4jForU2smRUP/gRNrxGTdIjXeY3vp8OmfLhzL3vhjz'
        b'ie5jACpzWWyvWH223kzBafx/ddX6+j3njef0H+leLYln4JajP6+PKEU/6LWVm3qg91V7YrzBYMjWy8reyQ1C6f26HcfLgCGlon3fcLLZi2EEbpFcwieAY5xjZqA0lTTZ'
        b'BZwVmtQJkLfJATuVWmVkC657GmfhO6VugBwtULx2spnKvwCQufiRm+YNKxdS9xvIXkrzpsQyqsdoHjlPbimdhEcckNMUgFbqqKYMZifNM4cANyljnGRtmBN0hDyeGEwg'
        b'Z25I9dkWgMw6CR4DWEqfK90AuycqMMB6t+ojC3rjMSaMu/EYV889s+znA6liv5Aqyjf9/M0EkS0HIpaPnK/VZ5d/CpD0w5KKsh76c5JrfXonqgwUjhr0541N+y4a+R+o'
        b'dJf1C1+Z/6OFZDaZQcxkRswvXpgveiMSiJoUSb/freqywknUcJ2RNLh4obwxThAhm2uZSJNMdmKGikbgPfGd3M4D0sz4pMTsctIYrwFm6QppBmFPupgfik8OEcSdLVlk'
        b'D2OiyAWyS+Nmo9aRA/5BoivEBuKCzW51IjWqFUD2CBAw5AAkteGd2IVmYaXaRMK6BwYPYIs6IYPKtw43ZDR3gcqeakzJ51upZkAZRpk3SlJBpAkpLhZ0evAuLy5e5tCb'
        b'hRQBx8pKAabKq6wrO2ROZs3GGLIOaZnJaDbYGE/GKC9DsQxsWQ9d6LpL6U0YEJ2iQjogiq5lvJhz/vDhMrlELomQOejykdv4Cm4MpVJP/iIq98jkvM6cEVjkoQjTS+Th'
        b'i8QGERVxDvFFkt3IID0GIs5xbiMH4o+MKZCCO6RTLYD0V37eY4qxxGSvAiEyQWs1GoTXJwLf8YQ28XnUXKO11lFuq9Y7bKUVerNRkQJJdECfy3ON9lq7UTHNarLZ23g2'
        b'6U9eggF/dgAmVVtlsVdl5sMkK2ImGaxGmw2m2GJfWa2YAxKs1WKsqDRalJkeAVu5sRyedr3F4LecRW8nD6xmtWIGLFEVlJ1bZbU8Sz5/lS01mixGxSRLub7EqMz0SsvU'
        b'Oqy1JcZao6m0wuKwlGdOnaPKpZ2Cv3MK7SoNCHzqzEkWmDBj5mygneaESUv1BrViulVvgKqMZhulqGbWrsVWU2WFmmtdbVjtmYV2q54cNWbOqLLZy/SlFezFbDTZa/UV'
        b'5swCyMGag5m3wd9ah0dxV6BkOe0dlf0Vzo5AlFpR5LBBw2aPziuSAqYkZ2qNFkutWqGtskLd1VVQm6VWz9oxOtszKqaTB2a7qVxRU2XxiSsx2TJnG83GMkjLMgLvupTW'
        b'G+OMUrrSFNONADvkVJndRkdJp9Q3t2J6rjJzqipPbzJ7pgoxykyNACd2zzRXnDJzmn6FZwIElZmFsImhk0bPBFecMjNLb1nqmnKYIxr0njUas5TCsCrfUQkVQFQuOUWV'
        b'LUvprAnTD5GarEn5NM1otJYBqoDXwnmaabNVk6tgbZyTz/aCyVIBsEbrcU57tt5RbVfRdgDnlKidbTrfvebdXzyde69BJPsMItl3EMn+BpEsDCK5cxDJnoNI9jOI5ECD'
        b'SPbobHKAQSQHHkSKzyBSfAeR4m8QKcIgUjoHkeI5iBQ/g0gJNIgUj86mBBhESuBBpPoMItV3EKn+BpEqDCK1cxCpnoNI9TOI1ECDSPXobGqAQaQGHkSazyDSfAeR5m8Q'
        b'acIg0joHkeY5iDQ/g0gLNIg0j86mBRhEmtcgOjci7CeryVimF/DjdKuDHC2rslYCYtY6KKqzsDEANjaCeOUKVFsBIQP2s9iqrcbSimrA1xaIB1xstxrtNAeklxj11hKY'
        b'KAhOMVGGwagSyN0kh40SlFpgGjLnkVMVVpg3m401QLGeQGPNpkqTXRHjJL3KzCKYbpqvBBIt5TTfNHLKbDaVA42yK0wWxWw90EWPAoVsDWjKDKYU9qysk4yriqAXgDBi'
        b'aHGvBGd5SBruWyA5cIFkvwVSFFlWhx2Sfcux9NTAFab6rTAtcIE0ViBPL9BlNufAlwB/wuLsxhV29wtgIvdrimdWmzubsBBZRiDH5R4RwzOLTBZYDbr+rB2aVAtRlPQC'
        b'lvYKJnsHAf3obXagdlZTmZ1CTZm+AvoPmSwGPXTGUgJg615xu5WcKgcg0lgMphq1YppAPzxDyV6hFK9QqlcozSuU7hUa5RXK8AqN9m490Tvo3Zsk7+4kefcnybtDSWl+'
        b'2BRFzCznrNqcjIaykzHyl+jklfwludinQGluVOYnvcB/a5Tv8hfvxYoFHkMX6YG4s2+TOTlwy1582rNkA1TpL5sXCUj3IQHpviQg3R8JSBdIQHonNk73JAHpfkhAeiAS'
        b'kO6B6tMDkID0wHRslM8gRvkOYpS/QYwSBjGqcxCjPAcxys8gRgUaxCiPzo4KMIhRgQeR4TOIDN9BZPgbRIYwiIzOQWR4DiLDzyAyAg0iw6OzGQEGkRF4EKN9BjHadxCj'
        b'/Q1itDCI0Z2DGO05iNF+BjE60CBGe3R2dIBBjA48CECQPrJCoh9hIdGvtJDoFBcSPdiURC+BIdGfxJAYUGRI9JQNEgMJDYle43F2cZrVWGmwrQQsUwl421ZlrgFOIrNw'
        b'6oxJKkat7DarsQyIoIXSPL/Ryf6jU/xHp/qPTvMfne4/epT/6Az/0aMDDCeRIvSlFvKgusxutCkKZhQUOhk4Ssxt1UaQhwVmspOYe8S6yLdH1HRjCXlAKf1TbEO5EO/k'
        b'GlyhZK9QSuYMp3LFo7CP2iXJNyrZNwrEHDMVivV2ypcqCh1Qnb7SCGRUb3fYKFsrjEZRqbc4gLwoyo0CmAI59KcGUHoUMVHibjKwYt+Y2U/9foiS/7p9MzIVU+fsKID5'
        b'VjhZXjaVZTTdOcnCe7LHO5UJOzVVn3OZ+W0yK1W0Wqk+1Uo1o8JpClU1WqkWv0Niqzab7NaBbhVehLcyj1ryPe+lzBPxHP+lVMLz/Fd8Cv8Tpsxbi2/rbdQ8pWHownjc'
        b'JkaydH5NL8P/oDKvTBncETKptLTKYbGD8NARngUrLggd+mqj+UlPQZVHteOf950CMFAJjAVVlioEsQcg2AR4B7JQjWyHmDJA1hHw+tkDiJhTKfAzVRUWo6KwymxOyAaE'
        b'ZFFpa6l6pTPYieIy52mLFEIxqkajyNNmsjmECJrmGRa23HSq9RPYe6GhrDmqwtIKM3kAS28GlsQzmJllNBvLDXQgwqtT59L5nuwUjzJdM8HYfcoPGp072yWzKQSeyCn5'
        b'deqonDIf49SptAeZYW/ZmVTgrIE1ZzZBBvZmspRVKVSKSVa7qyvOGI2FlnwqkmZL9pct2Sdbir9sKT7ZUv1lS/XJluYvW5pPtnR/2dJ9so3yl22UT7YMf9mAxSgonJ0E'
        b'EVphYSira2SRyT6REFDkGQFduhSxCoda0amIhUgBll2aUbWCsusuoVvQuHYuoyI3LjdzmsOylBn0Gq3lgJ9qKU6h8VlzFKmjBSpb5spCNcL+4p1wIyT5qTCziEkDdODW'
        b'Sj1NdIOIvxQ3qAQqltxVMf+JAgh1Ucx/ogBSXRTznyiAWBfF/CcKINdFMf+JAgh2Ucx/ogCSXRTzn0iLje6qmP9EttyJXa63/1RWsGtACQwpSV2CSoBUVrBLYAmQygp2'
        b'CS4BUlnBLgEmQCor2CXIBEhlBbsEmgCprGCXYBMglRXsEnACpLId3yXkQGqhnTwoXQqkazkQXzvjS5cbTTZj5jQg8Z3YD9Ch3mLWU9WibYm+wgq1lhshh8VIeaJOXaOT'
        b'clKEN8lRRrVibiTnoqWQRDFvJ0FWxEyy1Ar8MD3OA2ScZ7IDaTQagAPR259KfgoP+xbuxORPp1nN5JbNySZ4pWSzw50yO3AlbqmKURIV43f8igDOkTqpOZB+oDSUgy5j'
        b'vHMlJfB2owmmxe5WE2uA0bWbykxL9Z7Yv4hJgW71sSebIciOHseInmzSNKMgWBhNJTQpF1aNnovZBM4mMKPmqRqGfkPLerOjcqmxwqXHZkSQcXFK4OLyrbGBOFhqqvcg'
        b'IAfbj/+9gzLCpHWxrDrUlptPtiUwRpY0aYNQzxKxXEHO+fCxchcfu4Tz5mN3S3eH7g418Lu77+4u8LPNQYb4OkldWF33MpEh1CDfFAw8rdgoMYQZwjchQzdDRDNfJIVw'
        b'JAtHsXAQhLuzcA8WlkG4Jwv3YuFgCPdm4T4sHALhaBbuy8KhEO7Hwv1ZWE57UMYbBhgGbpIVhbFedn/qJ9gwqDnEoKrjnb0VGxSGway34cKodofs5sroyILY01VqSHOw'
        b'Qc0M6iTMCyQCygYZhhqGsbLdDAmQJqmTMR+RKJY23DBiU3BRBMRGQp9GGmKgT5HQRneDstnl3BBe161MYog1xG2SQS1RTAbYpEzskE2h9uCTC+d+nhCi8PjnilYICETw'
        b'XfLK0SaxUrsjKzWHe8LMwhPoG7PSoIKAUv6E2to8YSbO1NKmM7t1lCu7NYM+kmgWaubwhJkCUGhQBnWE6A01gJOsxSZDR3ApYAaLnb6G6wWppdgMrJ29okNW6oBNYyld'
        b'2SGjxqwmvdlpghFaZgJurrgSNmwFa7tDNHXOLMHGwzoaHqUyDxAMcf4ycx1qnePlYhVcJ60LqQsqC3FaBsnqZRvR88G1UatlzDIomFkDydYEF3q8JyKDiE2z+LMWmACv'
        b'2aP/NEJ3TbVGG3Mtc8+5iRkzlBrVPkV8IsaA0KGvVHRO1RinUxkgFqoCcnqtOedMb7H71ED/xWQBPrC7sJFSrZhEywPmKFUwI0KFo1oB+HOUwmAqN9ltvv1ydsO9Sv57'
        b'IST774H7oOMb+pD2TX3wBo8xilz2l3ZhekKuK9XZMZv/vlBqQ/E8UAm1YnYFYH7YBUaFzVFiNhrKYTzPVItgRSKIqFCTQg9VQFjov8JcBVTIqlZo7IpKBwgqJUa/teid'
        b'gy8x2pcb6UGvIsZgLNM7zHYl8ynMCLwWzm0xRjHZ+aYopZrCGPf5ooeGURmoFteWGuOCVpt7MakLY5VVESNYqywlD6y1IHYHqshpHjWGyViUH4FqBBhxYpgYY7lakZaU'
        b'GK8YlZQYsBqPPT1GMY0GFCxAqyszWWDXQB8VK4166FisxbicHnbWpKtT1UmxSt+pegbDY7ngGDGtJgKdUk1FqFpnNqBY5BgHkYUxZDNpzMMXZ5B6DWnWJpCGGdTiNDtX'
        b'SRrj81V4K9meOzMbX8rOz8vT5HGI7OyB7+Fj8ipct4hVm6cKQxmL0xGaoTM3z+yJHBMhEt/V4iZ3vbidXPOsm2wjDblAUnHD05VvWilHeAM+xWq+sTYYiVcBttXpcq/O'
        b'mSc4YZYV4zZqxudy7cpWq2JzSLMSX9Liy2KUvlBq01cy5zRWx5WpQUg8eiD1B4lf282KHNRGcgo+M8LfoEk91NkYb0uk3WtSzvXoGb5rDcXXe+PtprfnKUS2Wqhlc++G'
        b'AT/+dfC6RPnmd8/cvnFvS8udDSLZrBd/VBzVWN89Jvul1/LGbcGD//Ll7OvVVZuuDpu567XN8yo+W2V7qyRhjCb+jbaiOUGVxxf/YtxXaTF8yGJ+7EXLoHdmjjMXvjty'
        b'CelIPLhpgiX1udbf7VphPvL1/Z9fanySO3DCMaXyzv51Sjmzt43CD0kLbuz03BShbsNJC9kjKpseb6dqulmyGtxYkLLMczE51JdsFNfiU+QS81/BhxaODoXJVOa5zHbJ'
        b'cby1J64Ty1T4kF0BWVKrIaqxwGvZYLHOOHoNFoeSm1pmfEnuzyVtcaoYfGVwtopHUnyQV5GbZuYoFotPzIYKhKVi6xQ1RYovi0ijKl8w+zxImgvj1Eq8EW8mW4E/k+KL'
        b'fApZt8I+mFLSodQAnfqYwTCEtZGiKLIVb6gRwRyc6WunhvUjppAb0IiLX6O9hMXFx/EVusAIJZLNUnUZOcaqJBfHcXRIjfGxapqTNJPtwOLN1wGk2CRh/VeyXNXk4Gqa'
        b'i3J/tGEVNIvvkat4n4hsxnXkJJueXHzSCrniNU+xin3xHTFuLAwTDCVDvqP/W6djDLM2pcwHWotWSzkpc3OTOp3dwuFJXd1kPE2RcrWRLlrsdpHJd3WEWZpSnzQr3avW'
        b'SfSRRR+TkcsbZwrq2ppZJpTqrCTLXYpV4sev5wntPoU4tA4dGBjYptW3414Wz5zzl9mT0h6uRksE52AuX8l1hBZ3MhLWPu5J9PBqGmvWV5YY9OMjoZa/0xo9WnSlfe5E'
        b'7M66XExADBAMg6rKYl6pbOM6RIaq0mfq2iahayHFbubCX8+s2fDoAeWtGnj5fJDQA6GInw58m0npVuzNUgRsvre7eWWXTMe37ohzCoKLXTQ9YBf6ursQnaW3Gd1MwLdu'
        b'stzVpJunDtTkAHeTQwOyCN+y8TKhcVmxywEuUNuKzrYDshXfrW15saf0EKj9oZ0r/g28SIBeeHkgMF87vg65fe3+t/wPXNX7+B8Myd4rZs6+t7kOwTVqf0lF2afoZ00/'
        b'aXpP/oL80BM0/oS4489tSp7RuEQjOeXC42KzG5NTLE6ODbFTvoJcANqz10k/yG181geRDydtXXm/BRXTzeXp6LQWfkbWRnigM5ZBKNP76Zr6uJflOXiM4FzuzOvg5+0u'
        b'PN186leGdAQ5t6tg4S+12a1Go71DVl1ls1MGukNcarKv7AgS8qzskNbomVwaWgpsfFWlIK+K7PryDkkVbAJraajHglDMHu5alFl0vUPdcmaY+xaCcOEaiLJwJxyE1ssB'
        b'DuQAB6EMDuRs7UPXyAs93p3SZjlIm7+R+JE2JxkMNhAnKE9sMJbQbQn/S52Wcgojs+t/BoGTiUNMltErKhzlRg8RD2bIZgIRSSH4PlBpzWa0qxUFAPY+9VD8UElPaEyV'
        b'1VVWKpm6ipXqLSDu0KIgKlmNpXbzSkXJSlrApxJ9jd5k1tMmmXRA7SxtajpSE9W1weZzVumUsGidPnVA1Q6byVLOeuSuRhHLFi/2GWZkmnO0FVRN4tt3n/wxdr21HNow'
        b'uBAVLa+g2kMblVZsyxx0dkus+tKlRrtNOebZlQAC3I5RTPKiN4oF7Lx0UaBitOUxCubrsOAbPR4C1iJskzGKQvZXscBpfxcwv2s7jVFQ3ScsFRNOF3ja3wUsSzcgiLXw'
        b'VCwosNoD5xO2KGQVXlgb8QpNYYEqJSk9XbGA6jsDlhb2NQisk2arNFMUC5yHiIviFnj6cwRuvBMdUBFcCChoRZ5WxAGLAwKByayArQHb1VZqNVXbneSNwin1D2d7a5LZ'
        b'VgXwazT41R4AONHclBiZ2cVCbLHViimCCoFt0SGFdn1lJfWNswwJqExgmwEACzpQ7dxaBhO72kgP07rcBETPuAJW3LnhfOuh//Kr7EZhm7DNb7RXVBkAk5Q7KgHQoC/6'
        b'pbABYdMYYXZKjYoqoP5+6xGGRDcN043YhGGabB5dUiumAVJzISS/tXhuO6pJAVCnFzeVmmHAwp1NNqP/kjrntU1VpaznwvHK2Aq7vdo2JiFh+fLlwiUbaoMxwWAxG1dU'
        b'VSYIjGiCvro6wQSLv0JdYa80D01wVZGQlJiYkpyclDAlKSMxKTU1MTUjJTUpMW1UyujxuuJv0FtQiujraBiVz67EwEfx2YW2XGWOSp2PT5Ar8Roq3bWBkDisUFLx3Gjh'
        b'+pgTlvgU+JuExpL1SXgDfsDE/1/lSsy3UARCE3VmmzYYOaiyFl8uJGe1LmFtJqmnd6jkqBLIpVnUA3tWDPVAnUfq6R+g/ngXvhJM9qSvYhc74Rv4Lr5J2oFJoAJjEJKQ'
        b'A1m9ePnzSx1UNDOTu31Iu5re4EFdcqFm+Dk+NQ8k4kH4tJjcI9tXOKjU1BPfxHdJOwjeeXPIjmpheK6hzSD1+VCuSTunGmTeS2S3tiA3h+wRIyrzhpJTIyUO5ut6JEMT'
        b'qlbm4Af4aAgKziHnyD2eHO0T6aDMBL6+HB8l7Zq44VARh0R4H4fX4Watg14PQK7km0NJfYKaNECb8bgtBzeMgLbqOaSYLhHjLWQju3+H1I8RkfbZeH1CLIf4bC6dtPVh'
        b'MyueHcRvQn2oYsW8cK4WsauryE68rYctDG/D18geclPDGpYt5KcvtbN7qXoPxCdsYWRPWJia7CQ3c8k1smVFHNklQr1XivDFNLLHQdUWGfjBqlA1lIZ10dA5wRcmilBP'
        b'clfcDV/F10x9/ztaZDsIGadkNKte1YbgiRHi1z7+zweD2guv/11x+cGGeRWyj6Zt+NOu5kkfFWbzA9/ou2Px2CUx917W3d0zL97yknjPwId7to586eS93flXK/b8AOu1'
        b'bwyqDn3/P++m7v/02iva3LeazNKDP2v68MYZyWc3TkkuVXQsfL3mi/kXXvvwj5/b7+dVdcR8tfLlt99+3PGTJ7eKyTBR+u2XgltlX6+cNPoLlHMzbuGGrUopU9FMCB3o'
        b'VtDsh0l1KmlEZeQc3sXc8GWZwdrcoeSWt9ZC0FjEpUjI9qXkPqsK7ybH8VFPTc3zU3nE9DTD5zBtD27HO5Z7qCtw4+ROPjd9IdPE4HNke0lcvkqjydPGk2alJZRDvcgD'
        b'cbIMb2Z3BiRHkzva+Jhs6AMsHb5QVcWvJI/xMa9LQ8K/64U+AT1qQ/QGQ7HAwTEGeoSLgc6Wc3JOxvViT88fMbuJRMbVdnczwJ11OFUdYYIeogi5rNzo3SLWhfSxiD4W'
        b'00cxfejoQ08fJchL8+HfNzhUqLOzEp27iRJ3E2HuFvXudhiDb6BVeDH4vxoRmMH3Nz5lcIfcQI0AnQxTR5jABruCUn0l+0tvYTF2BDvPfkuNHaGUaQFWkVqGCT1yD7o0'
        b'xAMjU4VNhAsjz6VcfogXnx8OnH43J68fQXn9sggnpx/COP1Q4PRDGKcfyrj7kDWhhR7vTk6/DDj97UFdc/p6t4WfQris6Rn42anUNULIrQCiCvMGrCowCnrP6wopMxGv'
        b'KLdWOaohFXhovS+RqqosMVn0LrYlFjiaWEZvBXJL9QNuW1DaQbfI7FMTFaH/n2jy/2fRxHO7jaELJcS4NWPfIKJ47U+hvBDlqsAvn7bgGyxEAzYn7H+hHeeWd8YJrK6l'
        b'imp6rIyZtfhnUZdXUV7SVKk3B2CGF3RhIwsihn8r2YA9pphK6G9JVdVS2l8ao1bkOaFLz8KKqpIlsPAg+Ps/a7RQ0SgjPTHJqTyjgAByHa1uQaf9bMBOuBHlGMUcm0Nv'
        b'NrOdAYBTU2Uqde/GBR7mt11Kh05E670MzC1vgaeJ7jfKb7T4UzKclyHo/wUiWJZxubHcacbz/8Sw/wvEsJT0xOSMjMSUlNSUtJT09LQkv2IY/de1bCbxK5sphDPloKH0'
        b'sr3qcXKQr04viUAOel+VZSJp0WryyNZJkZ1nYjP9iVZr8cPg1ErcxqQZO3C4670FK37YanmokQltZOc4s1adkwecrZ86L+H1XiJbI2kMxmfJdvyYnXLPCR1nK8grcF6S'
        b'RKufR3ZA7u2kHkSsEBBIqNK3PmsIuVu4EB/CB/HJYIQvkL2h+ZFDHVSDvHgcqccNeLcthzRr8gq09H6lRDHqkyUiTeMNTGqZQS6TfbbYPLIthjSvztMmqDX4UgyHBpVL'
        b'JLipvyDLXscHyI5QchtvmzWA7JWRZlU+CF88ikoR4eNxKx2U7yXr8NXuMBGdZ9yaPv3iNfjmLHqDaRJulKyQkatCfQfIeRnrE0iJm/IKNPFKeiFqD3JSRO6TunK2SEd6'
        b'imAF90cFI53ZMnYoYgLzKLKRHA+VImspmo1m40PkviMVoleSdbpQOkcwkzvJ7WwQO5tJC7lJxdFGfAFCuWQbCAciRC4uXRgtm+7ANwUBHKTikaQdIdUEpEEa8rA/ix5A'
        b'NsSBXC4nj0A0T8Jb8BEWjXcU5ZAWEarGZ+htr/jsEvO/v/7666B0Ck7Z0eETdfJXIycIR/hRa9k9vlqRQhf/ZkoxctCjRrJlASJnRtEJanZK8dnxc+m9zAk5cwAisklT'
        b'YYwSYCJbuIQ5D8QmfItNoNQStogcL2W3yHbHOx2FZE9KzqJVIsSRizCqvuSiI5PKlt0XhjqXZ1YnsMg850ZFzjqnB18mu8QI180Jfm4UXueIo0Is2dDHFtbd6BKEZ8aQ'
        b'PYUyt+DLpN4JPaXhZPM0QSLfQM6F2nJUBWT7iLwEKgLmM9lXhJRkvwTfwBeiBQXEXT3ZFJeTitjloEopCsWPeYCW+1p23/C1jAL+xWmbw1C1vvuv++C0g4ipG8hFKgW2'
        b'U00Hj+tzVLMEQwwAL9KQUJA3M0a4a9TL5oEcxmflMPTL+L5wP89e/Kg8Tq2Jj+WQFG/n8TW8MWG6iE0kXj+LnNIyoZEn+8ldK5dRQg4oRUwTsQLvxNc9C24hrQnkRBUD'
        b'hd6WeGe56FQohQ8aBVXCLfLwubicCfic9ziLyD7Tpmg1Z5sAAtSiPMmiHePyRUkRm8vNVemta7/aFb8pbkbhqXfCU/vrxLPmZlU0zFJUbVRKG4acOPPWjf7rt9pOv1f5'
        b'oGdz+W9bC35aGmeaFxQXcmZInuOc5p3vVc9fMW1z3JU3pzWNKAz54ocHV0Tdbzr15fTfrrcvWfDzDbkT/zkz89y4N3o4ri4Zscg+wDFGfuaL13IXvbP87J/O/OnutGlb'
        b'zB+lv7z+T+vTf55w7oud3D+qNdsXRX8//EbwwszoP98pObDitzPu/vIN2+FXDC9bdw/VbLv27sAnIx/lLV6++/ez807yQz+RP/e+al/ogMl5x9+OvSR/9cO66xsS7/9z'
        b'2or86ukL1tzb+RxZYauK+0R17rdnjj9qffXXh2Lrxh36cbd+H0zd8Ksf3Uv4wx9/dGjhB/ZXvmwK+fPBgfckq4O+HnX+owurFHe/uN7zwQqyq6S2ufhXSS2vqYxVa/9Z'
        b'af2xeasyjOkERiTjC95mJLgJP6JaCrGEnY2VxyOmLiNNC/3rKPBG3MBu2SKbpYIxyYC5bnMSpqIwLGTpq2A3bNF62IHgSyXd5orMACvMDiQMMPd9vAsfjItVK5khSPBz'
        b'PD6dyjHdBL6VtyJOTbF8PAWkbTypww9VFVHsrsrn5bAFcmOliB+bsIgbhU+UMbOUGcH4BL6QmxdPrvflkVjL4evkEdkr9HYdbsZ7gSYIxh8ISVfzgP0fjxxnZLoZOTkE'
        b'I3NaifD4pIehiGAmUkmOMgsQx6gCRE54GJ94HRwOLmeZqvHeKTa6u1SUYsE8Z+N7IhRJdojwVXKUbGATkJgJm6OBHPVUwfArg8j9Li7aUkb8D6lj/ClmwqnSoVMGZ8qZ'
        b'2ZQvWMt+eLlTNdOpoKEXLwvqGRbiqV3KQEjtwUmZdQq1VBHuSouCcDizXQnh2d1pvb1UHZ2tOtU5ckGlYqSPMvoopw966aPVRB9L3GoWf5qcoGe5uTlEqLPMXbHRXdMS'
        b'dzth7iY6dTr0KvwiL53OudjAOp1AAy2VeHBe9FTd+553SV1QHWInq1xdCNPEhNaJ3fe8S+qlG9Hz0tqo1RKmeZEybYtkjbTQ4z3QWTttbBB6ms0LF9i8jzh+RILwOQTz'
        b'5z1noNks1mIW1/yOY8p1+SCJEQn3sreQxwOBH9ttw82yZSIkCucy7BzTjeOjsVMKcfNs0jwnj1wg62aSmzPIzTlh6YmJwCj0FuH1ZQuZ5T1uIhuHF5Lm2WmJZCu5Sm6k'
        b'AqslW8aRYwn4JCNF8orIiqGuujgkieUAZZCDDtp7fNCMH+F2Kb3SnTTgXWPHWQVVdgtpLVw0lJwkpwGaRqA+VWSrQNce48ei6RO16sTU5DQeSddw+IianGKfWsB38cnJ'
        b'cTmdV6gfJlfYNeqZ+KRp/7oDvO1DyPW1Xjq1IDNfnCS/+b7mw/bvqaOyJk7+0aR57ecq2p5cXGTaMdFcOe/1Ox/INC9HZqCePYe//MKBwz2vf3HoX38zj9wSHRIzv3Tn'
        b'X/vKz1x93G6ZMvXlY+s3/vxH047FbpvDDQ9+c9s/5P8NmnQmbsYHL+0x/rDPvoN7O/oGf7Ct9IXg6PB3v/qtLfG9YfP/UEmG5352I6r2y8Trr67q6Hj/i9dXZlj7ve14'
        b'7+PeLe+PmvfyT5ser7HVvv3XQb9eUFlzbGbJ+PZhP9kkiYx9X31l33LLDy8WPag7G5rXfnuf/S+P3v912L9Wqr5qXP2q6ErOik1r/hV07PUZr8z4QBllpysshfnahbdM'
        b'YB8vCEI8PsHNmTnbznwp8NUJIQUM3Tpx7QIB7+MrJfiuF6IFPLuTH4kPZ7CrP/E5fM88sqcfizwB0c4rFO6kbyDX6NWfAq3SkF2dCnURvs+uiOxNbpM92vx4YPu2Rz+f'
        b'gM+LUTh+JCrODmEkpBLvArZmL24ljVp25b14IIdPTNIKyvErwAvGedBBOWntTy/qPk12scodI8fGqYXr8u+Si51X5hf0Z91bkjBc6za17AUMHTWT7IUvifsBcTgljGB7'
        b'j+xBs7VPmVJGLRHhi0X4KqM6M1Lnp+Bj2tyAJwJSvIt1V/IcPkFNYQWjSHy1iNlFdhsoWhyVItzPX4fvkztOcouPrGYUl5LbAnyDjSeHtIKs89DgTW3wLbKVrZqGHFXi'
        b'o8ABum/4F673P+OcjvEg8azH93Va7xuGyWmDsOjn8DZ8jGzBjyiDR7YV0PtY8Q6+KmXusyHj/63vBriscoSvBDC6VdZJtxIoVWKWksxeUkxpFs/DX4GGySnKZj9iRsmE'
        b'wwYaEqwrZe5098+74sFiPpzvxVPq5mmVI3RAoGBBnbSjI0hQUNs6JDa73mrvEEG+b0uuJFb6KR2rxU2VqtykiVEler/sJUqVhrio0jr0i8CfIPDt9v8BUy+nic/nv/fR'
        b'OwhOXXaXL4lTf2t2qlWsRrvDamFplQo9PR7w0NI8k2pdsdS40gb1VFuNNmpUKah/nPosm1un79QF+VOJP63uNwtKNNqdkpV2ox91lReRlXpOoId9voM6rK0md/BR4H/3'
        b'4u24AV8ju/D1efg6bLcLM3G9BPXB6/C6LNGqJTqBmrVClsekBZZ5Fm5TIzXZv9pBbZb7kgO4lRFf3DhPRfZq1WoR6oEbRMDpPsBtVWsY7T6aAgh6yhkx/cBRdM4Awba+'
        b't26Iu6B0CNlTgh+SU4C6LuDjySg2TZIB1G+zIO61pZN1cWq8I9wt1CUMncbUODlDUj0JM9krBtoMSPkc67Zh5Xgm7QFf/RjxVN6rr2EyIvTtDNlWSIsVV4IwiJu5/mQf'
        b'uWjil2RIbJsgh3jErbwfDw7nQdh7919lRbqwXYaEF4J3yFLnV7eE3Q+f8P68ZVvS3z2Weor/V+vXrZHz7x67+l7Ty39Vv7Cj59SmEa+eP37mctCmy/Ef29veqx737s2q'
        b'8o//cPOw8vpI7dANe78O++mt6JnXK+MW/HnNuNn5v1l0MHPZy7otf+j2u08///4y8pcv+PyBwz//6QtKqUCuLpJ7QMDYUSu+R1o9rMOZTeGBZEFeacJHYJUa44dQFYDr'
        b'RuK4gezTDMBHXB8dp87jyYZwGO45ThuC97FidvtCIHHCV0B4FGq0JfPkGN5uZvf6k30FeL1/SUOBdwD43MpmuH+ahuyntIpcmuj1dRfykFxRSr8BrQSwcNTbiumWY7h0'
        b'SCcuNYtFUQJXD38pZqRHtvIvpZI+vAdCcRbO/0bzRys8PngKZx15JgNIZxNtXIe4Wm+vCHypexZyXpRNDzDppyGk7ovdxc90sbsTh70r4vwcXnaiMYpRbPoa+mY2eyK0'
        b'Z3eLowMZo9CUKWLpW6wCsLJNUJNTVGVcQX1uqdY4Vl1rqo6NZw05cabVv9LZRq8VNLhV3XpraYWpxqhWFFDN/HKTzejGi6wONgCWXa8oqzIDTfgGJEcXMdgHycny2WX1'
        b'5BI5vyQuG7bLjGxgV3LycnHb7Gx8idTHg8C/foQUZZMtQdW98SX2QQ2ya/oULeyunDw1aQBmbjYI/40JM4FZUcXgtn4FYqQlt4IAs23FRxn2wa2jgbdqwRfI1nhyfzzQ'
        b'LDOHN+jIIwd1Rlg8hhyIAygIMq9AK8LnMHEBenSSjyuYMRZgahYiB2eRh6YxLV/wtluQOOfz6+OaM8NxonzL2kzljMWFI/O5Q9wyTrpp9i3ZYOmwmNLrr32/X9TQQqvy'
        b'1Y2v57zS+OWE8Y13FbvemvKvj1/YVlS7y/ATe0dR7o0vz6iXWyIbN6Fry3ZE1L167pOp0a+GFHV/Zei2qPSMuWlB4S8Vxo9b1bK/+sJnfUdGXD77p58Oe7319lcHPmz+'
        b'S1XVf29V72tt+OzQWz1Vj3u9MGVRbb8/5LzxxcDwuWfTcr6++NrqfTk/tU2c278m5qcTpvJjipNWK7sJGGajsTeb6tWLAP5Hcfgy3qsWLsm/poiibCrlHjV4/Tx6T34j'
        b'/7xquGBpcohsmEHayY3lTIMzZzmPgvFZqv84hS8xDAXE5yq5xWpoiMeXJoHQlM/3N49zfRXqcTX9UF68WgOP0YAvQslVHhB8eyTjC9PwDfJAG4+3FdCvGeCjqzgUOpEn'
        b'+/FGNVPZTCzEj2j5hAJV2Fgqj/GxeA85y/pG6ovJOUpBlOQaPqom2+MpW9wtUVROtpcKfkjX+FR2C3yzKh23OlEuOc5arplnj0ugkHGYXNCo1EoecOJREd7cFz8QEHar'
        b'Bm9kzHlCPlDjNgmSjuV7pyQI49pF2gu0TlCFudwsRcE9eHwcCPUOwYnpaBimJwzNbFbu4CvQ9yy+j8kkpO7oOcnFSC8vcrLSQKtvs9QgchmfZX3TkLsyaBef4+NBDj7f'
        b'ld7nG9C4B+oW003sbVhDf4IFzY2M+Q7JgcN1aWIiILY2zI1YaWkBcbc5v3ZgR166lcCdbOOFvJ2329fA4+un8PvGXl18/cCrG0qnz/ZURF383Y7QgF+c/5QS4Q8Pv92f'
        b'uuqKGukbqkqLi5lDUoes2lpVbbTaVz6LMxS1ymeWO0zVwzhrRqrYeATuvsf/uB6uy1W10gOb95FTsJHxYnEIJ/1aTOfu6x7DYTY5/iup6Fv+FYeLAACctfRKAKD4WixC'
        b'X/ef2XdUeD8ZJ3yhchMVAm30E5W28HARSiGPwgbw5Di5H89OwgYvCAvF5+wUu4TS45cZ9Nilf3IwqRcPJVvm/x/6VJPP1yFd1XsToqB89m1CM96SRh1nBiNy1jFYmcY0'
        b'QVPxw8VaXLdQja8mpkFhcotbRo48xzRBsHOPTPfUBF0DWtTOk8PxeCvjYPuWwv7WxFNmK0WMZDFjcSOfQ672N43umyOxUXhVzhF/olv4vas7jrckbV7GlQa9z5/ZLA+N'
        b'zpwU/2GPMz0+3JyrS9eGhM7fffyVMxuTNh/feHyPZhc3rDv7TMaSu0kTIoteuqSUMFTVazq+F9edXHGqyZm/JIgPG5hgvjoC0Hen0E42knUM2zSlCGhu02DSEjceH/LU'
        b'pavyBrGy5JxVwLBOgb04l4rs+AQ+zrQ/+Dy/kh7uColDshbxRnJX15VjjBzELeBljMXU1IHhoF6eOGgY1QFTnCOGp3WVezOJO8S0QIfU6bLm820oegeddbV7M9CSg3mX'
        b'h+Q658+7gRlHpmqcgELjYnJU2fE5uDlBOK9VkL0Dpkp6hOBmH2jq6fxr+5vnJR9x9KILAFneINoUXCQyitlH9hD9vF4zXySBsIyFg1lYCuEQFg5l4SAIy1k4jIVlEA5n'
        b'4W4sHAzhCBaOZOEQaC0IWosydKcf6DPEw3bhDD0NvaBtuTOtt6EPvdTDoGJpfQ39IC3coIZUKfPKERv6GwZAHL2Kg6sTQ4lBBgW9gGN3yG5+t6hMtFu8W0J/DNFlPMTR'
        b'vyL3XyFWeIqFHB5P8dPvhsGHukFdIZ31PF3GMMQ37rs9DUMPdTcMO8QXRRqjjJGG4dHoWPfjaCPHQiNcIZajB7NlFPyVZDAnQc5rR3oyK8cgNk8Sg9IQC3G9DNEMwSR2'
        b'BBcDNdJPA+aY+Zj76Ou9RQzBXlLKPqEodWvpJc+spX/GL4uFCFr6XiNgRy78REr18XfN/YTTc5TShPooRwShGbr8PfFaIfJ+v9XcvweeFqNEfeZn4auQg15k0jul0sOx'
        b'Hh/Ep2dme0mZgE0ag1BhuSwCb8P1rKJhuqFoygy9FCEdL1MtQn9wdZK5FJoeNjwvtlGa+UX1pQFNL4StS5SLDqeeTuQX/OXTgfLvjYzK/rLniGNZIQta/na3ffiPpo3o'
        b'Fz/fPG7nyNRa/YzYjN6jerf9akDOuf+U7Jk2Knr1gKaefQcdWdX9j00TggYc0vysx+u/LZ7+/a1P/o3OHY0uevFDZTDjpEqBfT3s/KLdXnJQJUKy2bw9Ee9h3CE+GIS3'
        b'40Z8hamoRw6UjuQjyZkeDPMNWlnq7Qjfc9ZEenYZWc4k7+p5Y5jcLSLHfCZleLSkIou0MadxfCQiQ/BWj4tRCXkgR298dHp/8Vh8HB9iucbjy/FCL8kmXAd8I1V4N9Hz'
        b'wFYRZGroI5h0r++xwJnrIT5Lc+Xhiwgy7RHhkz26s27XkCP4NG5MAKZVU8U+NS0jW3m8ySG10+8Mx+EGfA83Loc67AK/34y3FwBtaKAO/YfJabUUjdZKYa4u4ksC6n1m'
        b'vrLTLX2gJ0pPlnIhEhnXh7mnO9WsXG2Ue+s89clIQSnaIWG2Th1iairbIe88E7NUdQSbLNUOO7sKrJPn9DRIl1g30Pd19LERudjN9V79TPAhDq93wXX66e238biWFNNh'
        b'BPS6BYlJ2CKe7bidz/t33mrq43urtmopkH8LP+CwYs+5DNilKa4ufT7Qo3lfv3P1t5mGkOLOlQvU8HR3wwM0rswum81v3a7b6ZsCU3GlKbDjdY672V5UwFCUWasqv317'
        b'Zd7t6VcEbC/P3V4P1h616P2OsyottlfZ9eaATc1wNxU9m2Z0Wf4GbO9/zofbLxPOI9+vHTLyUbGcR+Jsu4ieK8sWDReIU8ioICSvqKOeRfI7A2YiU8HdDt5GNeTBX1bS'
        b'D/hm63cbYj7U6uVlH+k+Qn9rjS7c/2L09agN0RmvI91NyZNTo5WcnSmbDk3FWwXUNzPZF/m5EN9acrEL/pUJfgzHUa9nN46bSxnW2khPLPHs3t2FPqjoShcKTt9GnnwN'
        b'//6/FaOcK9gKw6P8+MRekx19hv8wk02ScYUGaph1h44h4jXT3ddUvI3e0LJJ867wAeYdhvnf24/34+MPb+xoE/34tt71PcklD6UbShOVvLB8Lfj8ZLp85HEff8TLtX7B'
        b'2UyqycY3yDqqN4rFLTUqNZVqNvAp8+K7kk26FTOrZlOtsbjEXFW6tPODfq51Xlgb7TH93rm9vmArYea4vmLKLuSl/dgJj/k+y3++i+UP3L7XHnZBAAU91xdtRQADov+p'
        b'b5b6O7hiMDA34Z/cp6L5NvEM3SBlihQJatWT/UfjC2KED6SgWlSLj5FDzNxPjXePwRd4tJY8QKvQKjHZKti8HuiDd3jd60Q/ghqTr+JQKm6QJnYLB7aulRmJRk0H6Rrd'
        b'yQueqDPfmNQfMbPHH8/L518M/6VcMHscVvJf5KA39KkGItdFT4KTp9PuEQBoSTkFIa87no6TAyHkINmQyZAns7acQR4OoFJ9Nb7jEuypWJ+Dd5j24V4SWz3kufHyT4f/'
        b'hCqJ+4h0mduzes99IzNxbon+A+mP4z86+sobp0pCtD+KWLb1gzPD7O2GtVbc819/7hf5buKBF+v3ZJVj5ZDJs/V9hk7J/OP69JcPlMxV5+Z+3PZiuON+w9CDf73y5uzf'
        b'jf79oPa9v1l76bpScfAHc/+5eUGvpUlv/O5tTfGKLS9JWiLffm3tmt9dHHLux9XKIMYPTsAn8S0qwE9JU3oqSI1GpkGtwleXutjcwRYPEz3YbjvtIyHH7GTkwS8WLve7'
        b'6WpHs5OwYLyJXAmNdXLDbs55UJoFt4vJFSV5yLbyGLyvLzPuKBhP+WFYYXwRJG5XpVKUiM9L+5NbZJdTP71oqTY+hlzCjZ52CVfLha+ArsTX6Pig6dseVgVZ+ITS/XHx'
        b'gJpQafFyq8n5eVcvprWY2qzx3EBgWvs6bdnkXG2Ex+ZjBb2/Wq23ltsCsKS8dbf3zm+Bx0KfnX+mi697+jSeXyr22JRep8nO7xQz/zz3d4rF7DhLAntezPa8hO1z8RpJ'
        b'ocd7V7KmxGfPS/MFI6utafg2yFkbMb0XchAaVGNnArFgUFWPby6Lm6maq8KX8fF8MQqK5Aem1JjO5/WU2OhNmeKGbq+HU1XYDvzWC2+/cHXH3Za7G+/Oj9+s3D94892N'
        b'bRtHN2uaBu9f3y5BF8fIVv5zMRB0KjRl4eOpILw1K5mqBgPoMMMTDvWrEOP6WLLftTpda8Olxcxlg8FAhCcMmMOZvYfXxLOsgu5b6mH5xz48zVRQ3hi/TSzEPpWTQcAe'
        b'eJh8IOBAF1/+9elIYACgSuo6CYCAlKkvKBgEfQcw8Ev+fVUOknyP5T5Ctk4vpKu9l0Micj+DnOPypsaaUj9cwDM9yIU3//OJTquPMca8pxG4Nt0nOlNZ7N5PdE90S8s+'
        b'NXyi47cmpqc4rp9OdFytuXo6qSFJnFJdhpD9sbzmN/+d2aOTy30muxivb5BTLaLHgvfwXHCrTDD9ocanPT3murOMUNXewGC1z728++FR5bO8LX0CL6//Jp9QjUnghZ4o'
        b'7HSJc69LvsMi+71pyXevuxaZclcF5DE5Xagqxg/nkj0p2SIkCeLwBpXKFPJhhNhGr15oWnfoE50GVtkcLqxztv5jnVr/ke5TWOtPdRH6irLc0qhSyuiJ0Dlt0Od3esC2'
        b'pipVfANfn6/NJcdwG7XfXsSNmo8fP/vnhTvCi53XrHossxezXkuXubaPx2x7FXBpPbz3bIe0TF9qr7IGwO9ia2ugfU6vJljuAwiNPQIDQsCuKbsJZsidVsnUILkjrFOk'
        b'X2pc2RFWU+UorTBaWZEk72ByR2gpvajGSL8Ym+QZSO6QGUw24YYZatzcIanR2+lNxUaHHQRZepsu3b0dcuOK0go9vesVopQydt5mpTKGlfrJ+LsTmZ68FbEaqWVVUkeI'
        b'6yYZk8HD+34By2E32c3GDhn95AjN3BFK31x+7CyaXVnFakq2nqBlgqgrZUnVCuZ63yGprqiyGDtEZfoVHRJjpd5k7hCboFyHqMRUquQ7giZNnlwwJ392h3hywayp1uu0'
        b'6Xb0lA6FLildZ3q8ZZtGd5jIfZcVpaqyMtl34KPLnt5nImcT3vusVOCjf1C7mvs3v0LHJ+r7rZqeg5jB1Dh8IT57uo3c6gawxZMzXGzBQHYIB1H4is1eAynkZiiHgtLJ'
        b'TXKQDx9DzjHWl5yVT42jXNKlmOw8tSZvJqnPx5fiyfYkLiFnZnZ8TgIwxMC3udyiSMsC+eQVRoG6bwc2+BZpmQnvtaI1KM9gYpgeH08g21NScR1pSBQjbiTCLfgB3s8O'
        b'1MbinUtSeLSiH0pBKeTBaNb7bnhPWUoquY0vJgK4xyC82xQuuPfcDlO5TVw5FFqJDxfx5DI+jx8Jl5c0QA9OQlP3cFOiFHFKhPfgm7hFcIHagVtySKM2npwFnjONfgf+'
        b'GkdaSNvzbB5/mBaHZqN1KWERuqyGmHhhHqfhDfgidOXe6ETYdrEI712xnJ0AKZULtWqVmnoOQvtteSqyNZdDvfEp8URlOqsvHynQRDQ/hqvWLXxxSj/koDgrK45che5t'
        b'JTsSRYiLR3g/WV8qmIzvBL6oJY5erqIR2FNgV7vhZlHJhLWsvjdLe6N49NaqIIVubKOqULCbh+Ftr6D9I02JQYhTgeCUjy8IpnEb8GZ8NAsf05Jt7FNK4ngO30ubzCqL'
        b'1k9Aq9FfJock6mZ9VhYqdM5EzuOjKanT8vFVkN3UCB+Mw6eFqbtM/Wvi1PgKPqTMyQPxKjiJx/t5fJbV9s7sHLQbrQiRR+hicZpKmLraBaUpqXPJaXwV1jwB4VbcLhyX'
        b'4vrVY4DvH/w8yBgaarOwhR+KT4xlNU3OoK58GRPRRF3upMkOoV9V+MBMGOO659MRm7M9+Cg+xY6MyXW8mxzW5lBrZrJNMM3GeyrC8SbR+Cn4CKvyH0EZqBr1WSTV6WY9'
        b'mezsHN5hwadTUov6p/NspPt0eK/gT3ejdhWrbxs+ShrzO2GtL94thnXbTDazPo0lrc/DQjaQE+lSNrz9C/FD5vNJdgLMtAh9yhdWci0+H14tysBnyRbWpR7a7mgYWhcV'
        b'jnQL2ycsEkaJj68h9SnJ+MRICrkwzL2zQcrtLwBuA74EkDuWnKCQywPkXufIbrKRnGWj4fER3JaShjeUJ8IMgRy2N6i7AAM7E3BbnBYfJPXU1JBDUhMfHY83se26guyS'
        b'pYzCD1JpoQwYQfwSZgw1dwznBMOt+Ap1Z1o3cqwoYjneIcxc60KyJWXU2MF0a44BGIkmu1gvq/C1Iq0wW0pqPy8nG/HhCFFPfBxfZqNeHhmMItBrQUE6nTyhVONciO3c'
        b'KujEgaGpiFV3AG8uE0DuJllPdkFHyNnl1I1SC5BSyvcj10ax2Qon58kZKHg5KRXAK5PB6nbBRbX7JK0WH59ATzz4Km5iZpJzevtNSRlFHpGzqdDxsTAOsqnWdTfTfXIP'
        b'RMM55EoerFoTTFN3PnguOce6bY5chf6BXsnjI3Q1ZKLW6a+yzwbDa0/EF0tTJYjLQvjoaNwq4KjTZGMS2YSvgJSRQ89mROQRB621kzOsvvnLp6MmNH8Zp9DlHNMuEqYh'
        b'X0qaobpMciQV8MJkhI+NXM0Wqd/iqVqyNdmcCxzOYi4BkNltVsu6pdEoEZ0zhet0C3+e6dzA5GwZOT6VNGhBCpcgsZjDR42DhGl+RE7hq9TuF7cbkBqpgQ4w8+Fo/BiA'
        b'h7pezMoGoVo1VzCVI/V58YCGEDkXjaZHBfVblSpAYvOYNbDLUvF5wX+WHhoBFtgDu/BM5+3Z4TN4oIz/HsIhXfxfYzKFEZIHK/EO0iJFFnIT8Fg8PogbmfkwwMc13Kx9'
        b'6swQiI4YDSeHB+PzEkcPM0Mc+l4lpHEm2TKOOvgAPoviFuFDZDsbeuZalXY2frCGNAM4kAOIXB0Ou0cBKSPwBdvTLuAcVN00rkBiIq1yNs05Klj41lAkmgZTBf9HkFPs'
        b'6qllgKDPx8GM5JFt2aocQXBMEqMR+eT0bEmyEe9jI65b0w+lovllXIRu4Z610c4N3UquLyGtQWgwPoLwY/iPr0lZrWQLuTPep1YejRhGbsyRpChJIxvvQj25rp2Jb5D9'
        b'QGiZm/FD2PIXhMo341OS6fhhIVDoZiDxq7j+OVoGmkPwhfHaOf2BELKpOA0orQ++xdrFGwb31WqS8b48ajHWORmDcKOYes6Sk8JSrSMns0lrGIrFDxF+AP/TrAzdhuPG'
        b'GLrFYblvqTX5UFajShajfvig2EwupbGOjSFXLKRVRJ3pLyFa/iGpi2CIUTKenKClo6a4y/JQtlVciTeTawIH8VicRRoBBZE9yAT0CCgr21NranAjNeh097gab+vWXbQE'
        b'7x3E9nzqArKXqhRUZDfVKuDdK5hRuzYJX6OojBx2qBlcOW01+uObYrKVrC8W9vIDQKtXSKsE9SN3EL4P/9eSx6zeGQllpJFHQKzQUrQU5qWFbQNHd7xOq1Jp8MVa3B6T'
        b'Qzdb94kiQMgbyA6BxO3FbUAbWuWIXCP3AMNQJNMcLKCbxzn4oqczK7meQr1rguNY0cGLCb3srBnvCQM8RbfgJWAxTjMwuzYkBPVA2QVAZ82qolpBZTqAPKgmjSKKOo+i'
        b'KkDD7SOFxd6rIbeAj6M9yabe903aAhXrq6KfmFwdBLSbSiei+cO412DrKnp/9fxvVqyL/w1yREK03JBD9bAD+zE17A7cZkrv/RKy/Re4319Ykhb9/AeW7pMipO98fOT7'
        b'y6J+3b17U93hq3/OXD+sD6//XfB/y8KH7zD3eG7v9vdDe806uuP73XMf893I0L/0/6LwT03T+sfff9R2WTlvX3lycOaL5y/8d86bD+sfDg7bHTyr0nQq962/Rm1t00ze'
        b'c27N0nfafzqp77AfnpceWTsv+NqfPr728dfp+r7vFb63Qzv3R1eUJ/O+9/s+B/LPRP70xRfb32y5s2FU3rJfxF4e3TDlQ4Vj5IIpHw5ecDh1yq1JB/NLdv5xx4D8mq2f'
        b'bvi05vp0Q9Xxv43fKXllzcigKeFZ6Zljh1nvvPZu5M6Tm8e8PGXb5PyM0Urr+Rl/uPHKgQ2Heo4OGv3nDza8MvWV4SMbh+wbPO9i+R96Nv/ipUHv67dqkw78PKb1i+LJ'
        b'L+3TkP13vpr88u69K391fudXmgNXXvvAVN531JjXP3vpXsHG5xb/wBIxa9Lb9rRIR/Bfcdnbl793fsfpsSc7Pou88vvoORub373wq3Hd2leF390j/ffl4QevaG5WPRj7'
        b'5sOwR0cqzFn/PDr30obt/9lif3TwcKWi/V+NC1YXmitLznX/q2q0rZ/tztCWhn9ffuVhw1++1CQ86T/hlfSWQTmbp28O2T78a82aX0ZO6Llyr7b5aOPFX//g1rQvst7b'
        b'958Pp37x8ePKc39dunPUfw7cjnr8/r/m/j1o399nfto9/+bPPvnDlcjre7KKxzs+blg8LO+PY14fs+fxF6LYbl9WvvgTZXc7U7vfwg/xsafdCZw2DWZ8MVpSQS5OsbMd'
        b'/SCLHIzLzxqrot4ZB7m8eRMEW+AH41OpMx/wSCBeSJF4Cgd1nl0p2C/cJjvH48Zu1VJyXW4lsHW61YQFS1EPfFRUNXy04BJ3uBQ/DMVt8dkOcjbaqUCOJPdEwCm11jJ9'
        b'cHyInNTjW0/7oR0XC18wOEiOUVVxAr5ITjMTWmrPfJLHjbidHBU8vY9COXoFNN42xKUzlOXxBtwcxhwX8fWe5JK2IJbspqOr4SaRAzZW8HlyBm8CdvkBPulpKwc0Zh2z'
        b'J6nOHgaU/JSnyyNMxXbW6zVk3SJqaoIfkCaWzIxN1pMrzJw4TofbnXr4pCWervLkUYXg6XGNHMe3nJYs9+1Pm4gAx7yLDd8yabDTRORCz6csRMhNmbDM9XhfLLVJoYcg'
        b'VMChttcberlmIm60BN+KkDEv9ZEW6tiSoCEX1/hRsRalChbie8iBNS5PSMqqZ+IbzLsE38W3hBwgypEt1CqFXnPZAPW57VJmTvH3OYFvbf3aIdIbBFXPCni4VT1rkTqK'
        b'68WJuShmUkidzCPg1/nDR3E+PzTuY9mACG4YdUjn+kAZ+ivnZHxfTsGFszLUNJrmjWD5I7geEOI/lfWqDevU3EB/PE8HrFRj920d+nihVOepwQ14nOddhtvr3D9v9e3C'
        b'YtqrT4FP+idShkf4vBaqk7g1iRzTcDzbeb/PqQFtTIGe1nCMFDQc/YaJmKbljlSXazSrkaBeFK6j2QOifouEXE1DaCAamNVdOEXcVkxacQvCLWOAw0XR5HQ1I2qw5TeZ'
        b'U8Tj5Aglww9uFg6jLVQuQRkHlurk+y3DEDsuDOkno5EzrlfoctfNShAY2+Oznuf+zaMZmgx9vy0Oi1OC2YTXx6aAFILwkRq8B5UOB9aa9aJeQXUH1KNcg/ch4zKnHPSX'
        b'2VJ6UWKffoN18bI1A4SqT8+MoBOwInK5Lr53/55CJ5YXsMiMsJU6eWS/NULO1DVyeoEqql6oy/2L+Tkh58nuYTRyxfRinblE1VfI+VxEKLALSFfeXSfv1lMj5Fz4HIus'
        b'uD9IF3+7okaIHNyXXpaDVuyJ0eXWF/QRrmXF9SCzHGcM5hzKjUsm4hs1HL63iDxgfFM2bNIbKYmJUXgnMJrDEN5FHuDzrOX66UPQFGh5f5CuZPjqoQJLsWTKFGApSAv0'
        b'E3iKUryVTV8YOT6QtIbg62PoTR3wP5OcFjjcU1NgvVqlUbiRUgT4jxszBC7xwQR8jLRwifgmQiqkqiWCTDSqL1UeoIkDc3Ty/6qLhKNYwL91wfTzNvQHRDWyBTDsRnzT'
        b'NFdYpPV4HZCzFo7szQJeCg3ghjAheHQy4EoPu2wlSEmNfE5KDRs6hzdYC+kx1f3BlMfeyUWRA+QcA0klPhMeFwQc8k6YT5Cx9+YIPPVZEAn34QsoHdcjtBKtrCINQgc2'
        b'R2ThCzypS0D0ZJvcJY/YOTJbl30xbER9SifrcsdODhX0060Vn5SiA93opuH+/o5J9e4FkS2V8mWGqMqdmflkYsSW8pr3Hxyq+7s18d2woIlvvDZYvSPui1nDzl5bONk4'
        b'+O6PI2tWvcjFRJ6tz+Dei2j6Zf7ViJ+8+sXv/vSgxvqq46V3buaIzg3//ZgRQ/v+MKYi9Z3gny0jKyqKpoX+4+KJ9+Z0/+PN/D//TDPwtZ/sWfWLDUf/V3NXAtfUsfVv'
        b'bkIIEBEQV0QjKrLKomyKChYUZHHBXSsEkkCUNSEuuCIggoAL7srmjqKCaOtunaltfa8+21r7NG1ta9Vualertfb5zXITEkgQff1+32dkkpvMne3OPXPOnfM/f/drq7Ju'
        b'flcR8WjAwQtrP8qZdiPsRmNyucu0d0bz63b3euS8aXaP5/VPB8+5+ptf084lYQ/+mHo2/NKoec9srt2ZlXvzrl3+D5O+t+r3/s7tIXu//nJa/8/kN7Lzyv9YVenU+63X'
        b'7jy99nPUsorsO7HTf/t9FGTHiqbZ/FNRlvLPqU2xUtekf+5NLamfejfuhuMg1b8KVx3r7vB0ZUL9X6XNK2d0ndR1xKVFIzoPjvXL/2zkqRErfxy3+FSz/baQI5/Nj/j8'
        b'o/7e9c1Ped8HFKTyEt175OKoS/Mnw1Jzzo6DQ8E6bvcaFIB8spcM6pTgNPE7iPf2QCvUGGSknWDBZl97otx0n9rFSOlAS9oe0DQ4k/zoC9aI6cqLnUxfg2sns7lwHyyg'
        b'ENFGcAg04zU3DhusOA50LFgFzvEYh3A+OALfWEB0hDi4SorDamEYfwlSLjJmLWNd0NSpp6QUlcgWOAvWLIIbTGpoSD0LyqBa2ClYMAU3xhM/pjjCQyWC2umgmfr7F8AC'
        b'FfGMIW4x062xY0wEaCArdTg8tRArgDRuAXn42W00rJkucIIr+pEckdHEoVYXswCl3UWoGwP5oEGcSypgR4F9eqdaISiEJ7CmU+hP/WGbkBHGqTGcDoNu5fM6PcYrliha'
        b'oXAPz0CjSIYFHF610JWUMgfVUNlSClJy4AVYqlN0wP6JRKka6SBCOkeU1+DBcK3POLApErUT1vOR1DiQTC7LHLgnzIRzLiyGRdg7dyU4RcFaFb5RJFtFjAUjYHlgB9Js'
        b'qnvBIooEWwl32RrGNDgKNxKQxBuwibg79AnqTbwdWnwd4F4kNdr4O5QISN+HgzIr1Gyd6gr2wiKivnYBR4lDhgJWwTeN1bcgeHy8kfoG1g4gF8sTCftNnDcw0bmWIkUM'
        b'q13wPKikU359Nqhsia8Em0E+jrEENozXuU90aNNNgJ0JW4dVIHuqYp6A1QVQcCTalyN6dUOvHuiFj21JMAVHksOB+yOvu8Le7B2hMw4aJGaRHvZcxMe7s2JWRIBqebYt'
        b'mg2u3sDZrp02t/jeoVWGeWhCmdrYztZcqyrRGGGlBb2tI2/x5L9qGz7o3gpuRtyOVZgrjroiEx9l7J6sFencU3Wf8N4VdeokODPsJUYcRojPANlZJruKWnHihPBJ4XGJ'
        b'k2dMiEzQ8tXyXK0ARzXQ2nA/JEROTiBKI+ks1Uf/+zgaqmUo8cIjh93ZRHw7+5eGlVnYCmw72QodRXaWuugZQuJlIzR+/SxwwL/pvmdb/657PRA8FHrY8mz/I7ToEUEe'
        b'S9kiYX/KUPhbMHaTwX5Qxp85Hx5ps9+tI7VRj2zN2CvY2Jkw2nbWvctY/Sd+uaVsAFKZMUCks0Igs5SJ9Py9VjJrAusRc/y9ncixLTnG/L2dybEdORYRfl9rwu8r5vh7'
        b'u5BjR3JsTfh9rQm/r5jj7+1OjnuQY/FGgYLBrZL13MluFGLgztxOsl49mVpbDHHhjp10x93R3x5eBU82kMO9W5IwUjbFnYvtFFaEBZhw86LfrAjTroBAgkQz7fBoyPqV'
        b'84qpqSAu7oQMBRdZf8LCay/rTdwJXDkW3pj4yKebjeDhk3WssOgnSsErccMMKZgXS5opw7Nf2Zq80+jAYzJGqXNUWOhTVrI6Kx2zd2NwPQ5jTGlIcRhleXYujeRNkPat'
        b'okurAhnCyWvFcbphviPuI9l3FtHIqpj5SKaYr+XPy0TfZchlSk0G+k6UjVq+IEslU7XwAJsk4DUO2KULmG6FTCxrbjvZRh+w62UoeHG0gZ87TMGLB/uVKXhfzMDbhm3X'
        b'ZKCBV2TgNbgo+nbgkOvttAL9bK4NmRJpenaa1NtUU0IkKWmoyhQS2Lx9QuD2+YBNcP++xIi8kA8YzUcaAzpizFRJujQZU8+jj4Zhtd0HtwpYTWnsTLbCuOlkbN38DYbC'
        b'ROO5hqB74gVsxOaYh01HojDHRtxB5mGThbawEf8XzMO6+54OOz2SKGXcBRvyogumExZc4G/uSKKSpyrVaISRkEKyjEwnL4mGu2yaTByA+5UIfjvTpyvHlpKHDP1ss5O8'
        b'vrKMply3cJUYHmqP4Repk0YUvEVhYnga7LaDO6aSUtcMcWTcmGCRMCwp1GmBI6UNRipm1cj2SyXMNlGLnQ2KrskWwz0x/Uix0gDynEMpnpAkXsDLpMX2h3U9TJZqYHvo'
        b'GrsANhCn7ZNgtQ2y8Iu9SbHn+PiRzMn+OFiwqyCY0WCpD4+6A9NjEO2Jym6ExwycwFfAtVZgEyzPI+X9OQ0/UhL1tE5KElv0WcBosJ+tZhzS403yB7fYerpmwnWwiWvn'
        b'GzZgdwTcRcp9LMEbQL6ZYrskrxQljxITjZwvN1Wsm86e0ZU5JZeUeBocsoGrp8LDymbBp4y6DJVQnfKu9/tn7Fk/ceTEy8u9N4b3+63RYp1b0payOja21r+WN67OtTrA'
        b'NuCbkTeTLx9Qp1bazPC7meP+xUd//ZbUqaomHa50yixvHOJ1qnzp1j+/jYuo/NBt++24Jfs7X2xevGraE5tbF/I/G9LwZP+wUVN8cuprn+2afTb91wT1uzM7/9T3WfAS'
        b'J9dxnpcfdbZYE5wiEbpb04gdJ3xhIzYwpbDK0MZEBqYzfX4/FZmHR/GjcHimn7tx2FhYMYKYbZEeXQ1tVLgJ7qA+In3hVgE8Ck92Jw+vQWmfMcaWKrb/CsAWbKuCfQuo'
        b'NVwXHeRJrR+wFr5BofMqeJzA2yXTlDorWgI3I0Ma1C6G+6mJfUaILVCdUagBBcgurI4dRmsu74WsUCNrH1WdDA9gY98PVBM7zzMg2sA6xU3b5kGs06ThuTjazWTwJuqm'
        b'1AVrsN6wGb6hJo8v0FEs0We9hUwcKLQEVUPAyb9Ns9dDOHE0CQMzbjkzmvAJ84Qt3MKUZ5jEcNUf6Qh7kcphhmn4Ak7ewslFnACcQJy8jZNLDPNivh1RRwrpZNQndyQn'
        b'CerIwM5bwdxsJ/hd2368DOTQOlGvPpkF5k1BbaKwz5a6DCiH8VftUA53HPmZpmOANdClzDZquq5RT/u0agHRDF6NcdgqUac3ma13lr7evrTev4XqWJCItCWzdc7R1+lE'
        b'6zTQqF6NZVeQiJQis/VJ9fW5tahN0tbw2penU9bDXHWKitkWyPQt6IWfYxjoMq98ZfWmkLk6U43qRKOs14AM6nRnKVKbPBTRO+XGp/ANmoL93vG9TPxd41FCdqpwFAuW'
        b'M2CtSQxksUKs94K36JAXPJ/sXQkeWTh0mH1Kjvk3O0o+RTK/DPeUIddUmyIx95QeSO3hJfEwRHSjYwISR5kMmXOIhkubgQlJOm4F6isaJknIysC2BDW+cZQ5DpYtTc7S'
        b'5HKUTmqktZobG/wP06fI8ZDIlApCrpPLaeXGneLGm4TURMOWysXQM6EQ43/RejIoaXsGnl+ggVkjcdMxzpg3cAzHlSrvbW5WiVt4skqekpaJyW44a49E0jPZ0JZ5oFYr'
        b'UzPJVKCUMm14zdQSpWGvlMjwSTXDW6MzaPzIRQ4M0ds1uCY/dy/8uERHkYxz6DmSU8yZYmRWKsn5mF4Lj11wSMfpuRTGHcK9VsrVfx+5lhsmkyI0WO4SD48MbGyj7izy'
        b'8Hhlui2JG6HW8qYMVS9TdDvUWh06/2WJriRmCLrMEV0N7lgzjCAj7dJduenprvzcJbP8/M3TVRnCTrjLqJHT7igzSUMJuX1EXNyMGbhnpkLs4n/Z0kUZJECvXIWXKi/C'
        b'Zae3kQ0a5N9+g9rl4DJ+YkLvFh/dnWKyWVQhMmTuQtUP8TVPwmYI0tE9PzK4TdC36I7MVCtpo7IUpjnNZHPRzCDjgU8gUYqlC/HnDtI54X/hRoWoyaMzZUparpJwdqlb'
        b'GOXa3rNmy/SW+GGybLkGCVd9AWgGKyXcECEJlYHuuMgp3pOlucly/DjSNMOYtwRNFxo2NV2TMU+eZnr8vSVDWmUjtUk1ijxNrhytHDhitWRqlkpNGmWmjKHDJOEaRZo8'
        b'WYNvPXRCuCY3C69v88ycEDBMEp0pU85Xosmcno5OoLx36lY9N3N2oKkmv/wABZkqRmnQrIyXa1awqfJeblxCyEC2DP0LRt7kl5PpTMbPDVu1+6VnomH3FSrUGzc8tvo2'
        b'SZPzNKnu5qef4emSoIHmJ6BRRr8QcznRNMv0aUspSn8MaF1MoLliAtsrBk0Kff/aKSPYMJvZroUYFWaiX2YXNA5EiCQc94noA0gnRbJVJ8rdEugaa3bBbsEoYrJ7tBTS'
        b'I6TjuMWgQ3km+kPTXILXoGDzNJst6EbjYvxbFePfbjEECGnEu+hGyBYj8HoTYPY0PXCSnho5hUhq/IXEDd3k3BRHl938MGhUmH8SrRavcZ+8JAa6XeSUSRK3aXBPmgrd'
        b'pKgtQ803xQCz2VKY/muuUbqi1PM0KnXbRrWn7plTL4kq2XHNT6+ihRttAXRMhyHo0mGSePwmmeXv+3rHT/Onp/mT08xfDR1slVMhuWNsPrc3DwimFZ2C31DGtvnMS7Eo'
        b'uUqV6TNGJdWgJH2wzxgl0u7MSy2S3byswuWYl0+4AvMCqr2akVSKTENKGJL95kUTaRvS2WSmm2Fu8JAWK5fnYs0CvyMFK7Bd/S45a+EwCd5RRvqTAmut6As05uYvKj4J'
        b'Q4rpWdJ0CT5o94wUZS6+IVHarrpHkdQ4J/1ACvbCerr3EL/AQDTTzLcJQ5hRg/BbuzNSIUW9HYOESnuZCAgaXSH8JpkVaD4jJ+Z01LLtzGgdPHuYZDT6RDXhWf5B7ebX'
        b'39rkFOMtvnbHWwf65s6k18e8sMZgb6SijQ6PR5fHvERMVqagAqNfQ1WbuCPbwLTxZr5JMiwnR+zEvGIOps5oEnlwLrbrbGP0ZJQ8RjQSrKZ4utWUb2N9GA5atLULLyzJ'
        b'KyEwhAucsV4Ad7dA/GrhG6AmBdZQX+agbowX06ObUJIUeuz1BZyHciOoEWPsH1wBijH4D+6wJU6uA6Z2A+d7GwKqMZoabpxJygroj4HlvjE8X+niq47RjGYwLivfHhZ4'
        b'osyY+XE8digEDePiaNwlsB6cZWATWDOJWTjUKnUMbCIII5VrPPu2kFnYGJ0hllgeXVZNd+1AAzwIjo+ANaZCLeHioujuhRG3ZDnYJnYfDvKVj4Zc5alx3FD7Gt/yigvj'
        b'+FK7t1N/P/Nc6V12Qr7OcfMiNsai4C/VBlHx7IowUFW0v1G5cu26qOr4JaILPo/ZqWfuv/9sftnREtXYrpUB34/9+vtJn1ds3po2dFXXcx8vuOfVvPCk29D/bPSz/eDO'
        b'e3N+Fz3uKdRctr1+Yl/qzAfKvYrqe7aq3scbcrY/XpJqszty7w83PvpFflzx1zzljby5P7s8qi/ROO781LPg7tVbj68sfrL81jXVqpCD0YWuN5/ZVdl9auN0wsFBHfpH'
        b'ddXZ6Clidal76Dc7f/O+5mDzxZO3R/QMDsr/9dKVB+y651Gllnf6Lv9GNW5Ejx7uIupheCwOloIzYJencRDmeQRWooArweoWUMkEuAscE4LD9MyGLuHgJDjgCUvGR4MG'
        b'ASNMZ11gCdxDETfn4BHQRIElk2C10W5aMGgmIUElSZbUTcpwk+k1uLHNPhM4Aqg361JQMdMwyhM80o0L9ETCPIEGZ7LX152XYMRwCE4O1zEc9lERlsZBS+Fuv/SY2Gge'
        b'w07iecAGRVswiPhvCo+OveDIzhbeszXa2VrOjBcRjkIBz5Y3gER7wp+xm6E1t6vF8noR3kL8bsfLE+v3a6QyWbxRwJCWp9jYp9tgK8vqpRruLjAopCWGqb4nc03uZ211'
        b'Mb+fZdRm8ygQEjkKOykxxQJ95KiXIXNKQ03PQYUYiVDcpbZ8ggOpCJ0xm3jDZ4+MS0pf4cxniAzzBMVqtWZigC+Gu6JJxYO7py0FTbCEokSI731TZ1hnwwfHwXoGtWoa'
        b'PAuriBs/xpgl0DN5EOM+xfD4cDWp62IOFn7M9IfB0uHzui/iCjoBNsNiAukAW5guo+Rw/SAunAAofo1iQDYx8ExaykiQT4HB/QjWI8rHNUkMpsgpLqNcYY89LiT22Uni'
        b'OjacuvqXqIkbxvTReUlec0UTac5O3SnWw21OUvrs8Wk059QJ5EvR2dlJ4swBC2nO6xTr4WvrlBRbNzKZ5lTE0i/ftUvy+m7+UA7ZMp5gPaJed0+KDR7Poz2LgPkDEiZM'
        b'mMAwvAgmbwnId4FraESN+kRYNsQXcy3y4B7UbXgQ5sP9nchZHsIxCRNSQAWDsX37GJi/EG6kGNdCwWID4Mh8HlgFz4PToHwkwUgE9PEZ4rss15eDjfSFh0ksEFi0YGIC'
        b'Rvbj+Pr9+vWnmJ29cK9iiAA2zSagndAQygRdaNUfVvJAUyxBgMATi2m9jSJYZAz2CMZgD6se5Ho7LHFImCBB8wI0dxXOBIWgDlbBo2Qawc3jMwzxHmANO3/xOFtwjoIx'
        b'8BAr+AQnFMZmJHnVjwygo/mHD8EJ2Q2fm5S+3HISF8WwMQPuSZjQWz0BHxQwUlc5KWF2ZlcG3YuS/nFJS+5HhdOhjwmEBxMmgFp3hhm21EbUE9bFx9HYHseCwE51pyFo'
        b'mFhwiJGOgOecwT5laugFCzUS/ExWzZWM9SMw3qMo9ZP5yd+8W+J8e91P3VW246zzZtbmbYhM6532701Fdzb0v3/LMoedGx9WvvVEQaT9YdmDJb/8a/Gv99aP+0f9nZkZ'
        b'lxv3zsv7+s8dk67vmXLJZ8frHkEHe5yt/ejaP9w8Azb+7n/a5co7BalLnoh6fzjXqfbxnuofP/DpY/fJkazOE/fG9l2vmZLmIvZKEeVNiXHwt/N38L/V5aqmfnqaV+4v'
        b'a22dPJb6Zij3P67Y8yRMe71ma9fESeXv9xi7efh/vJ+NPXjy7tYg20GrnYrjfdIGXRWpZdPfCzky4o9Uj552N+r7uEx3ueiROCPQKt5rlkK7Nzhgy5bzmxdfnqnqumXD'
        b'prOx8tIhHw7L2v/WpfzZO4/2/KT86ImfGuIWPj/3Phw10HvH+vJ0mVNuzMT/2HSfkvtl6FV3R7KEjQAXvNquYa0WMNgQBapguSV12j+FpEWpJ1kY0e8ieIYFK9HMWZ8J'
        b'TpAoVL6g2RYpQ7E8RtCPp5iPVr982EQ8P/qDtRojikR4SLwIHvQj7vQCsNrCGCNSCotA01RYSdEPx4QzWodECIAHMOpAEmlhNXEh9UlZEQYaDeAbo4YibfBNeII67G8A'
        b'+UIC30DJeX1kU3jYguJn1yz20zvHoJu9xb8GbgPFpPjho+AWgjKJRLcTBZosY13CqOvKSLgisI3TzEA+PIVu84bXYSGNm34cHHJqUUh84XZwDGygESXhfrjTI8YA3sGH'
        b'Z2wYW1DAH201haJBL4hhtQG6A4meagrvAFujSR8nwtPSmBZsByMSMbZL+RGjkMZC+rgb1IITrZxn6vmg3A5WLqBka3PAhhRDyMYAsB9UjwMXKP73bG9w1piF0gPWZIEC'
        b'SKOxq0E1Uqlbu++E80ExDnoSCosIMydSaA51M/RDQpMJlIJivR8S2D3ZjAPLC0ISEiYZoqvktdVVsgUcmzKLNBQ7VkR84u04WCuGVdgRYAWL3q0NGCntuD/yuid0Yu+K'
        b'elsjTUHAQS7sON969onQin3Moj+RNUemRnSGtnxtpjvRirkNqykerdWUFUx1e1EOW1eqUmN1wmx849HM30DfhrUWTWutxTR3mWU8ISMDp2A9rNeTl4EyWNmKwIxjLwNH'
        b'YigZ2Qp4SoHJyHoxBGtDuMhgNTxNwY+1SP6c9LQEe8ApgjBkxAQuGYGFkud4tKA1cZRkUrBTefvRZzw1hnS8mXhrRPlwazZcvOq5THH90ZQZM2bO/M75bRu31bWfB26X'
        b'JPf7NjPk2sm4RvvQi+8XhVZu6zrgypY7y1cTVrLrsf7qe3/Ojh066uDh3av6DIj0cmDffid+9P1hn2R5f68Z88HWsD5NWxpBjurLty4uLN2bmuXQJXPW50+tCn+of9Dz'
        b'eNX4Bz0VLs8+/6Fm1snr5W/nxd9Ph0eVjbfeaXI9uMzS8tC1HnHLfSYu7ba9OnXtkpwbtaHLeSsvBUd9d869MxVzWwfDDZ5RsBYUk7C0lJRshTMN64run0J0YyWDdfEc'
        b'fIOwkiXOJxJIisZrE0c5hvnGQMl4tjfjS4weWAOKcJgeHecYYRxDufNZJPP3JFMZtDtqYAupGaE0QycdxLRmq+ZTvtpjAwfpackwJxk80AXTklUiKUo0i+NwbShHTIZp'
        b'ycAGtIagwoJI+VjuYxED34AHYowC7wbAGspMdlCm4JjJMC3ZELCW7Z8N95O6k2CTh6eP0wgMATMgJkOG+B4SoGBwLwuOlwxzkvXksd39h9Nov2NhHY4NUgZPc1OQkpLV'
        b'dKN92gcbsGFOSckwIZkr2MX2gKtgBfldAjeCE3j5ykHzzSC0whmYz+EKJ4BDnhwyTQgOTISFrBc4Lf9baMkIdRaReh5tpd5yxtulfWYyLDBamMlUC5j2YWALjarti75T'
        b'e7WVUyuYr1/IRaarGEkQYzQIhYax5C3e3aE1HGwRwxhiwjrg0ogEA44snivPUFNQVyvGMfv/ylTuwBU6h5J+WKRPZQjFmNCOJyaEYN3cX5VgTIzXnucCVIpkgcNwEY+C'
        b'u7eOhWfUenXOgkkK6tSLhZXOS9x58UpGONtC7Yw05W+bSyMrYiaBMLtVi10Fv6xYVxgq4n0l6nOxyjK77uH0Z127T276oMHrZvBkze36B1buh2/GLv9r1FPL/EFPQucv'
        b'+sbJQqMaOed+39Mu26qkt75QxHr98Hv2ldp5340PuiJq3vDliOmupyt/XZbedcCvs0ZcW3T4vfMPP5grGDPj6bhvvlwW++3SatV79j4h9zZO25lzcfitoH6j3z8658eR'
        b'G+53+SrkTPkai12Hit/71ubyvSMTp7t0c1i+Picv4JigvjE36ePro6PzHK/eqDx+6YPNZUtDjp663Snr5t3XK6VFsWe3fTjmdcdfMudMONp0d4LKZuO0CzVR1Zt3Pt+h'
        b'HrzI5aHdvMm3j5Q9rKr7d+CwlFT/uTYTP43P+akuujHcuzov7ePaQb98sYzXc7ZCNG2lO5+KmUJQD86AYqSVIiWGF8zACtAAN1IhuA8emQY2y1rx3OCHQ1Jvog129Qox'
        b'Ec4bNMOKAKTgzBnb9nGN0//OHHzpBMkdvu4eNJkQ2KooMTE9SypLTCRyBz8IZXqxLMsbyuvznEUSRshzYEW9JI69PBxHOQ5iecOwJAoV8W1tXJcz81me6t/6m4+vZRMT'
        b'DZ739Pp/MAY81Q39vYtbiu8tNTZ/mG/DzDOh4QyCGUKwBqxFi0DJ+FiYHwlKwFpLxrYn3zkiUVnm35VVr0W5oqMvO5eE2AJfR4vnjx/ahUWll4YlhzhMa5x001n+UWTe'
        b's1mFOxxmXylzzdkV27/T0F9nLV10Jz+16uPbpe5/HbVPPPiTcqDXxze7+kyuuVwX0TRw9aEMdcLUXeM8Z396V3NztZTNr6u1l35QW1QEuw2/n/OW/aCdH178eqUnm3ny'
        b'6/zULwbWAMeI5b+tuf0bX5Tt9rvwU6RXkFg6aFnHC/N4/By7OJswItuAYyw8EEhNFFADt8DjMeO9s9JgE86HV3B7eJYP6kRBRIWQg/Nc/zGwIBYtveWk/w78PnAHsiKw'
        b'ZjYIbJsUEx3nEecHmy0ZoYAVwR0ZBDbQB5wfC9f4CBmAMQMJ2F45DA6TJ57RM/t4jrNgHLvxYpCUg2hUycLrEZ9DaPRgmQu8QFibbNxZuA6Wgi3UXC2YuEBNM8BdoJTk'
        b'sI5mQeNyeJZmOA+2g/0xRGSWzGEJGsIWlvLjweqepLVieGGKbnNhXAAPDQFWZHDdlnC1M2HIjYJrZloRTUuMNJ3jAfBNXXifRnAAmUOlXtlwTfwkksMaNLPgeICGPA+G'
        b'5a/huHDHxGD1ghwNbM4R52hcl/KY7nAtH5SB00jc4IrmgKrlMSS6QrQvPIE6w6DLsp2Fu2SBxKACJVYiPOg+MUjQVJAnxvvQwK3BI+80QAAKZoAmo6DLzv/3t1jrO87q'
        b'BVLHhBBqwVwQHHonEQ03RBgHsF0n5o9srQsNoHoDkTt9tfx0eaZWgN16tRa5mux0uVaQrlTnagXYeNIKsrLRz3x1rkprQVjptYLkrKx0LV+Zmau1UCDxh95U2AsAk5Zk'
        b'a3K1/JQ0lZafpZJphQpleq4cHWRIs7X8PGW21kKqTlEqtfw0+UKUBRVvrVTroKVaYbYmOV2ZorWk6Fu11kadplTkJspVqiyVtlO2VKWWJyrVWdhRUdtJk5mSJlVmymWJ'
        b'8oUpWqvERLUctT4xUSukjn0GofRZerV/w59/wskPOPkKJ1/i5B5OPsfJtzjBLKiq+zi5i5PbOHmIk5s4+Qwn3+HkAU5u4QTvOKl+wcmPOLmDk59x8gVOPsWJFie/4uQR'
        b'Tr43unzWesH6JMKsYCU5n4oU2Jc3JW2w1i4xkfvMLUJPe3HHkmxpyjxpqpxDNEtlclm8u4hojJi0VpqezpHWEp1Sa43GX5WrxjzgWmF6Voo0Xa0VT8JuhRnySDz2qse6'
        b'UWzloK8VhWZkyTTpcox6pz0QWCJJ1nrCBTkSEP7/ABADtho='
    ))))
