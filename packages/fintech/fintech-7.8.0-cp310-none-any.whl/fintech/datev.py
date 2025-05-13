
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
        b'eJzsvQdcW9fZMH7u1UCAGMZ4L3kjkMRexnsCYtnghQcSSICMEFjDA29jBxuMsY333jbeeztOzkn7Jm3Spk37JqVpm9U2w2nSpGlSv0n8PedcSQhLcpy+7/v/ff/f7zPm'
        b'cs9ez3nWeZ5z30dP/BPB71j4tY2EhwEVowpUzBk4A78OFfNG0WGxQXSEs0YYxEZJPVqEbD3m8EapQVLPreWMAUa+nuOQQVqIAtcpAx6tCJo4rmjSDEV1jcFhNipqyhX2'
        b'SqOiYKm9ssaimGyy2I1llYpafVmVvsKoCQoqqjTZXHkNxnKTxWhTlDssZXZTjcWm0FsMijKz3mYz2oLsNYoyq1FvNyqEBgx6u15hXFJWqbdUGBXlJrPRpgkq6+sxrAHw'
        b'2w9+g+nQzPBoQA1cA98gahA3SBqkDQENsobAhqCG4AZ5Q0hDaENYQ3hDl4aIhq4NkQ3dGro39Gjo2dCroXdDn4a+5f3YdMhW9NuA6tGK/nWBy/vVo5loef96xKGV/Vb2'
        b'L/R4X4wCy5WivDLPOebhtzf8dqWdEbN5LkTK4DyzDN6Xx/II4sb2kupyTuXxyDEEIsmBKfmkiWzMz5lKNpDmfCVpzppeoJai4ZPKB4vJA7ITr1dyjl6QNTyMNNuySvrk'
        b'ks1kUy7ZxKGgLB5fUuUoeUd3SJ9Jjom1WaosCRKLyS58g8OHlpITjj6QlKfFl7RZ5AreqspSk41QXIJCSaMob+gIKEynDx/T4tu4iTTWVqtqoUOboJogfJXH1/CGUIcC'
        b'csSUqSD9ihxvWLzQQa4ulC90cIjczOpBWkR4U5dK6OVgyBZtw/dxE26J1aqjaUdJCw0FjB2L+gwR43q8ndwu454Ayz6uKauk6yesHvpx61fex7l23AYA3xU8rB3H1o5n'
        b'68Wt5As93mHtKp9cO9qR7l5rN0BYu+kzA5Ac9VwQotCpVmT1QCyytpsIFnTDqiCkk5+u0wmRxqBAFI7CjWKdTr4pYZkQOSpWjGSo1iEdq5P3HTsOtSFzEESbLb3E/4hA'
        b'YxVpnw//gr8Rn7ZwEjIHQsKt5D3cpQCkODykIuHtBOvYF4Xog5VfhG0P46IK4v/BfT/rpdh3UTtyxFIoukJO4XuwbE2xU2eRLVFRpDE2U00acVtRVHYuaVFpstTZuRyy'
        b'hAWOIq0DvRYg2DXuTGEBOm8eRKe/PNg9wfwzTXCFr80h9ZpgeZ6V9sBBY3tkKgunqasKZ/CIF8HWwBdCHeEUODdVx03G2wuhhsFosGiCI4KO+XYUvlxIdk2ZBtGVaJKk'
        b'kkUPILtGLcZnSCvUGoti8ereLLoLuYcPD8D3SSuMXY3UQwoc3WjNF/CFyYW5UwtwK2mWIH4Z13feAsdwSEkkh/EDvHUM3QsxWoDjjTlTo3CbKpPtTg1pk+C1s8hxRyTt'
        b'yg0ZOQrdPYivwgBHopG9yTlTF8sEsW03pO7qMnbea/GhOE6+Xv/7rPZ1B/64WnTp6ouS8BiZNPjytB3qeS9/8dapW5NshRFbtvzsg3eXPdjUffTffx5W9NnmvL8e25Rk'
        b'NZwI+Epr/Cazz51lSVu7bPtHzI6Xu56duu/EsT1336ta97Lpj7Nfn95Y/WDGglO5O3/3XNNnXd75+L2LPXbnr1IemvT7b9948fR/HO3eb+jKK8+9gitGF9y6z22ZlbJW'
        b'oVNK7HTnk8tFo7WkOYYj10hzrjqbIpAIcktEGvD1FXaKzcjz5Hh+TLZ6YjzZkJWTJ0HB+DJPDhhwq53uXHyNXI6M0SizYyhmiRsCuCWMrBbV4GPz7P1p8dY0siMYpi59'
        b'fKYDkEIj4MEu5I4Inyf1ZKNQxWmyFz+AqW4kLQsTySbYV+kcvkxO4lNKvp2PUlopvCiD2Z9/40FB71H3keXWmjqjBcgII1AaIC7GRaPbQ6xGi8FoLbEay2qsBprVRvGd'
        b'bHQ4J+OC4Kc7/IbCD/0bAX/DuXA+iLNKXTUrRe1SoXB7QEmJ1WEpKWkPLikpMxv1FkdtScm/3W8lZw2g7xL6oM2NoZ2jEKcgUp7npBx9ijnp9/TpGEhTySlFTDZp1map'
        b'cWMs7P3NsdkcuTkfDcWXJSXx5FinLUn/iZ1/GfI1Up4A+AEDVyyCX7EJFUvgr9TAFwcYQhtQOWcQGyTrAotl7F1qCFgnKw5k7zJDILwHCeS3XGQIMgRDOBjCgE0gLDeE'
        b'QFhu4BgPEdYuncamLI9N4Uffw7YsE3l0i445wIUt0pCLrkNFAhoSbRABGhIDGhIxNCRmqEe0Ulzo8e6PRou80JBYwPMf9qOIGinipNH9Xu3FIdOlD3PEtgJIGfLQ8Ynu'
        b'1dIPddsMG/Qf6zZVnDN+COHiF+aSS1vi10/df2Rnl5fy9af1ZskZ7ozuZ+Ktqn7ySdH9NgXPGv4wY/XHPXtN67n2xd1XJejKwC4Jf9+jlLK9JZ0/jjRnxLiJZYwUheGT'
        b'oroaXtgYLXh7P3JySUcGEZKrRAH4YBkrjteQPfi+ljTlAN+glKICskWGG/kloXp7T0ieB1u3lWIw7YoeWfg8NJfG95pAjtt7QOI4bgVuys+ahO+qssRIQvZz5M5yst9O'
        b'iWAPoyhGncmYCT5CRq7xeB1pmaPkPWBT5GuTMVBtl5WUmCwme0kJ20yh8Agvhk0D8CqG7SN+XBcmrL3GlU/YRpJ2sc1oLm8XU66vPWCR0WoDBtFK18VKyV8b52qZVmkN'
        b'oY8w9/6Qw2OOa3+En/LeH16tlvFPbAM3vKU44a2cd0Ibz4ieCKCNZ9AmYhDGrxQVerz7InrID7Q5lPC+sqowmDTD+mwGwk1aCjOFdZxaME09gyc78Go0hhyRdhk8wZQ4'
        b'rD9vi6MLM1XziY4CXlSZ6j2NPkf/UBdeVil/qdxcKm6MV+v+ppv1cs9XX9jDoUNJMkfSOqWYwYm+P97qhhJ8Ig8xKCH1+KKdYo1ReBO5S66SjSX4AGkhLRp1rRNR914p'
        b'xuv7ShjAxACRXENBRpVlGOOCmKVyOx3bSnwYt2rj6vLVHOIXceNC8XZhUXmfEALoscJoN9mN1U4godgtqFTOybm6CPcyubMIVYnZkreLLfpqYwdUWMOFZiLcMMHAoQs8'
        b'ylzgEHrIBzj4aOf/GwzkFyZU8A5kd/3MzlCBG+I8AUMAClioe6aB61RiWwKU+ln8Dh9gAUDxUMc3Jjji3oo7HidOrC1H6NyvZfO+LH73ulIkIJBGsqa4A3/IioDtAchQ'
        b'4fsMMMhN3BJKAcMNFXMCOuACAIihmXhyfZUAFwwqpuBWAIxwUu+kjv4RBYCBzRsMKuSAJTyWx9YZDCTCKtP1bpcs0psdXsAg8gCGSDdE0OmudCOIvU+FCHeT/nHECAEi'
        b'KKvMlYt/JJ5Y9yRMcM7qO8OEJM+hpqtwbsRCKtkVkQ1qtWZqZvZ0siGfXNAVCgxpJvCmGg7Zyf1Aqb7IEU3nkJxDXqgFb1U8AUR9SZMpMWqS2JZHcYS69RPdxwBF5vLo'
        b'N3P/otJn6s0Mgmr1G/583nha/6HuF6WqMtW2KH22/ow+vAy90t0qmrSnxyV7nMpgMGTqZeXv5ASg+LiwtY4PgbukBGx4jJKyfp0Yv9rlwPodDGfppFGD73jAHwDfVLJz'
        b'CTlGGu2DKHyunUJOdAJAqGY25BIgcBYgMCobk+vkPr7hAYPZyQCC08kD1kgN3o2vu+gZpWbkGF6P14GgelHppCliv3yjAKlSRy1lF90ELcgsY9yhnOMfh/N1IU7IEXJ5'
        b'oiuBVrkB1Gs3AObqoGYMTqlcUu2C04gdPuC0c2te0lxnpMWEaTfS4jZwzyS9eQGo2CeAivJMf/vsJrJlQ0TOb+VafWZFsOUhwNDPSivLI/WnJZd79ohTGygENenPGM8Z'
        b'+VfUugv6uS/P+vlcUkQKiJkUvPz7F2eJftMFiJYUiSPDisITgGhRtEJu9a9ygcaIPKmTZm3VsETH8q7O5QYmx0mL4Oc6Y1/iyVYQ9ZpUWaRZLR2mBS6LH2xZxMoFkkNT'
        b'GEdE+SFyRsJYoih80jcEPA15Aa9vs1udiIuK8+H2CICHIICLutAOTEKzsFJtImGR/cMCMDgdYEDH4XCjq2YfYPBEI0o+z0oFeWUIZcAokQQ5JKikRFC8wbu8pGShQ28W'
        b'UgT8KSsDAKqosS5tlznZLRtjqdql5Saj2WBjXBWjpQx9MthkPXOh4qeKXMJA6NQU0oHQcjIk5sWc8BPKy2VySbgkUuagKxMTQg4EOyUWWOsL0+S8juwh5/xLLBr0hMTC'
        b'F4sNIiqh7OeLJduRQXoYJJQjXD0H0ouskJLiwHbpJAvg9qWPIicaS032GhD+YrVWo0F4/UhgJj6iTTyKmGG01jkqbLV6h62sUm82KhIhiY7pkTzHaK+zGxWTrSabvY1n'
        b'8/7RT2HMX+2BedXWWOw1GXkwz4qocQar0WaDWbbYl9YqpoPkabUYK6uNFmWGR8BWYayAp11vMfgsZ9HbyT2rWaMogFWqgbIzaqyWZ8nnq7Iqo8liVIyzVOhLjcqMTmkZ'
        b'Woe1rtRYZzSVVVocloqMSdPVObRT8Hd6oV2dBfKaJmOcBSbMmFEEJNIcO65Kb9Aoplj1BqjKaLZRwmlm7Vpsi2qsUHOdqw2rPaPQbtWTQ8aMghqbvVxfVslezEaTvU5f'
        b'ac7IhxysOZh5G/ytc3gUdwVKF9PeUZld4ewIRGkUxQ4bNGz26Lwi3m9KQobWaLHUaRTaGivUXVsDtVnq9Kwdo7M9o2IKuWe2myoUi2osXnGlJltGkdFsLIe08UZgSKto'
        b'vVHOKKUrTTHFCLBDjpfbbXSUdEq9cyum5CgzJqlz9SazZ6oQo8zIEuDE7pnmilNmTNYv8UyAoDKjEPYxdNLomeCKU2aM11uqXFMOc0SDnWeNxlRRGFbnOaqhAojKIcep'
        b'kqSKzpow/RCZNX5cHk0zGq3lgC3gtXBm1uQi9YQaWBvn5LO9YLJUAqzRepzTnql31NrVtB1AO6UaZ5vO907z7iuezn2nQSR4DSLBexAJvgaRIAwioWMQCZ6DSPAxiAR/'
        b'g0jw6GyCn0Ek+B9EotcgEr0HkehrEInCIBI7BpHoOYhEH4NI9DeIRI/OJvoZRKL/QSR5DSLJexBJvgaRJAwiqWMQSZ6DSPIxiCR/g0jy6GySn0Ek+R9Estcgkr0Hkexr'
        b'EMnCIJI7BpHsOYhkH4NI9jeIZI/OJvsZRHKnQXRsRNhPVpOxXC/gxylWBzlUXmOtBsSsdVBUZ2FjAGxsBOnJFai1AkIG7Gex1VqNZZW1gK8tEA+42G412mkOSC816q2l'
        b'MFEQnGiiPINRLZC7cQ4bJSh1wDdkzCTHK60wbzYba4BiPYHGmk3VJrsiykl6lRnFMN00XykkWipovsnkuNlsqgAaZVeYLIoiPdBFjwKFbA1oSgFT5npW1kHG1cXQC0AY'
        b'UbR4pwRneUga6l0gwX+BBJ8FEhXjrQ47JHuXY+lJ/itM8llhsv8CyaxArl6gy2zOgS8B/oTF2Y1L7O4XwETu10TPrDZ3NmEhxhuBHFd4RAzNKDZZYDXo+rN2aFIdRFHS'
        b'C1i6UzChcxDQj95mB2pnNZXbKdSU6yuh/5DJYtBDZyylALbuFbdbyfEKAKIsi8G0SKOYLNAPz1BCp1Bip1BSp1Byp1BKp1Bqp1Bap1B659bjOgc79ya+c3fiO/cnvnOH'
        b'4pN9sCmKqGnOWbU5GQ1lB2PkK9HJK/lKcrFP/tLcqMxHer7v1ijf5Su+EyvmfwxPSffHnf2YzAn+W+7Epz1LNkCVvrJ1IgEpXiQgxZsEpPgiASkCCUjpwMYpniQgxQcJ'
        b'SPFHAlI8UH2KHxKQ4p+OpXoNItV7EKm+BpEqDCK1YxCpnoNI9TGIVH+DSPXobKqfQaT6H0Sa1yDSvAeR5msQacIg0joGkeY5iDQfg0jzN4g0j86m+RlEmv9BpHsNIt17'
        b'EOm+BpEuDCK9YxDpnoNI9zGIdH+DSPfobLqfQaT7HwQgSC9ZIc6HsBDnU1qIc4oLcR5sSlwngSHOl8QQ51dkiPOUDeL8CQ1xncbj7OJkq7HaYFsKWKYa8LatxrwIOImM'
        b'wkkF49SMWtltVmM5EEELpXk+oxN8Ryf6jk7yHZ3sOzrFd3Sq7+g039HpfoYTRxF6lYXcqy23G22K/IL8QicDR4m5rdYI8rDATHYQc49YF/n2iJpiLCX3KKV/gm2oEOKd'
        b'XIMrlNAplJhR4FSueBT2UrvEe0cleEeBmGOmQrHeTvlSRaEDqtNXG4GM6u0OG2VrhdEoqvUWB5AXRYVRAFMgh77UAEqPIiZK3E0GVuwHM/uo3wdR8l23d0amYuqYHQUw'
        b'3wony8umspymOydZeE/weKcyYYem6hGXkdcms1KNuZWe/lipdlw4LKE2dVZqD9IusdWaTXZrf7cWL7yzPo9a3K1wKSYFfR4v4jnpd7yE56XxstcctC58hMM3bKQ5hmxU'
        b'4TYxkuFbuCmFX4n34Ev/gxq9dcrA9qBxZWU1DosdJIj20PGw7ILkoa81mj/qJujzqEr8Ue+JAAjVwF1QpalCkH0AjE2AfCAL1ci2iykXZB0Gr1/dg4jp1QJTU1NpMSoK'
        b'a8zm2EzASha1to7qWDqCHXguY6a2WCEUo7o0ikFtJptDiKBpnmFh302hqj+BxxcaGj9dXVhWaSb3YP3NwJd4BjPGG83GCgMdiPDqVLx0vCc4ZaQM10wwnp8yhUbn9nYJ'
        b'bgqBMXKKfx2KKqfgx9h1KvJBZthgdiYaOGtgzZlNkIG9mSzlNQq1YpzV7uqKMybLQks+EUmzJfjKluCVLdFXtkSvbEm+siV5ZUv2lS3ZK1uKr2wpXtlSfWVL9cqW5isb'
        b'8Bn5hUXxEKEVFobyu0YWmeAVCQFFrhFwpksbq3BoFB3aWIgUYNmlHtUoKM/ukrwFtWvHMipyYnIyJjssVcz61mitACRVRxELjR8/XZGULpDaclcWqhb2Fe+EGyHJR4UZ'
        b'xUwkoAO3VutpohtEfKW4QcVfsYSnFfOdKIDQU4r5ThRA6inFfCcKIPaUYr4TBZB7SjHfiQIIPqWY70QBJJ9SzHciLZb+tGK+E9lyxz11vX2nsoJPBxT/kBL/VFDxk8oK'
        b'PhVY/KSygk8FFz+prOBTAcZPKiv4VJDxk8oKPhVo/KSygk8FGz+prOBTAcdPKtvxT4UcSC20k3tlVUC6FgPxtTPmdLHRZDNmTAYS34H9AB3qLWY91S/aFugrrVBrhRFy'
        b'WIyUMepQODopJ0V44xzlVDXmRnIuWgpJFPN2EGRF1DhLncAU0zM9QMa5JjuQRqMBOBC9/YnkJ/Cwd+EOTP5kmtVMbticbEKnlEx2wlNuB67ELVoxSqJm/I5POcA5Uic1'
        b'B9IPlIay0eWMga6mBN5uNMG02N264izgdu2mclOV3hP7FzNR0K1D9mQzBAHS4yzRk02abBSkC6OplCblwKrRwzGbwNn4Z9Q89cPQb2hZb3ZUVxkrXcpsRgQZF0ct7PKs'
        b'0f7YWGpsdc8vG9tL9mcH5YAdJnzexpG7OXlkcyzjZskmbQDqViqWB5IGL0ZW7mJk7VxnRna7dHvw9mADv73r9q4CQ9scECgNDDKoGiQNIQ1dy0WGYIN8XSAwtmKjxBBi'
        b'CF2HDGGG8Ga+WArhLiwcwcIBEO7KwpEsLINwNxbuzsKBEO7Bwj1ZOAjCvVi4NwsHQ7gPC/dlYTntQTlv6Gfov05WHMJ62vWJn0DDgOagQFmgzKBu4J09FhsUhoGsx6HC'
        b'6LYHbefK6QgD2NNVclBzIJTTMOs5CfPiCIfSAYbBhiGsdJghFtIkDTLm4xHB0oYahq0LLA6H2C7Qs+GGKOhZF2ilq0HZ7HJPCG0IK5cYog0x62RQSwQTByqUce2yidSu'
        b'e0LhjEexQQqPf65ohYBLBJ+jTjnaJFZqc2SljjkfMfNu6lzxETPYoDKBUv4RtbX5iFksU0ubjuzWVFd2K7W6scbTLNTy4SNmGkDhQhnQHqQ3LAL0ZC0xGdoDywBJWOz0'
        b'NVQvCDAlZuDy7JXtsjIH7B9L2dJ2GbVUNenNTquM4HITMHYl1bB3K1nb7aJJ06cJZh/WdHiUyTyAMcj5y0x2JqMnXKMCG6QNQQ0B5UFOyyDZBlk9WhFYF7hcxiyDApk1'
        b'kGxlYKHHu2Di+hV1rug0c/RfltBVU53RxtzB3PNtYoYNZUaNVxGviBEge+irFR3TNMLpCAb4haqDnJ5mzvnSW+xeNdB/UeMBLdhdSEmpUYyj5QGBlCmYvaDCUasANJqq'
        b'MJgqTHabd7+c3XCvkO9eCMm+e+A+9PiBPiT/UB86g8YIRQ77S7swJTbHlersmM13XyjRoegeiIVGUVQJBAB2gFFhc5SajYYKGM8z1SJYlAiSKtSk0EMVEBb6rzDXADGy'
        b'ahRZdkW1A+SVUqPPWvTOwZca7YuN9NBXEWUwlusdZruS+QGm+V8L55YYoZjgfFOUUa1hlPus0UPbqPRXi2s7jXBBq829mNTtsMaqiBIsV6rIPWsdSN/+KnJaS41gohZl'
        b'S6AaAUac2CXKWKFRJMfHqRSp8XF+q/HYzyMUk2lAwQK0unKTBXYN9FGx1KiHjkVbjIvpweeiFE2SJj5a6T1Vz2BlLBf8HD5OCUeKpHAJqtWpuo4chhyjIZKswzfwVtKU'
        b'i88VkA1ZpFm7BB+NJRshkF+YmaMkTao8NW4kLTlTM/H5zLzc3KxcDpGt+LC8pqKI1bu3ZwjqqUtAqECn+um0UOSgHivkNNmFt3jW666UbCYbc4Cs4o2uWqvIVlfF65bK'
        b'EWmQsorvlAeicPFhCdLpzEezcpAjCiI53EZukibShls7nLQyNepo6gCDL4hRylypjdyLYR5mrJoNwwOQPGk5jxQ68wcRmcK4h+Lj5KKv7pENUGWTinZxk3KGe8wWsplD'
        b'+LY1GF8hW8eauvxJzttWQj3nba/3e/Xngavjwif9Kmdl64e/CFWNuyTSXkKp3NTUQTMO71NOyPgqXdxf9NeIV3BrF7xtYtb41PlHXhvwmqnp/keDLhecWjC937XxY9bX'
        b'Tf/6mzcPy6KWhHx+6fax+ilfXfp6/aHTIVWkMuL7nq8bqldq37u89F+fZd/UlCct/R6V6aP+OGCoUs4MunMG2XFTrIe7SNhozVBROb4vsVPFHa4fMAs35XsuJod6k3px'
        b'RH6dGq+zU9XdFHLWHIw39YcJVea6DHe74QaxrDSdWYXjtfhQFW7qT7bmd1pADnUfKA7Gh9PsVO1GDnUfE4MvJKmjMtU8kuK9vHqGlLmc4U0ZM6ETHgsVgS+ItOQOaaro'
        b'wVwNJg7AO2Imkb0aJWkERk2Kz/GJpCVcMAm+mE324CbS4rE4UhSxSITXjMD3cSu+ZaesnwWvB7CDoTo5N9rDLLytVFhfhOLIeqmGnMcn7UNpZ7daCLUfhhqjyTa5huYm'
        b'zaQlhmZV2CQheB8+xtzZBpKzYpqRaTahdTW0jXeJeo4j65eSejv1gSV3x5O9Hk07mcbe+JZYSY5B1287BPvJoH/Tl63D44UZn1IGBK2SLpdy1GVNeFKXNRlzW4MYXgqx'
        b'QVxdFxdNfsLzJkiwO6Wb1TqWPsbRx3j6mIBcXjYT0dMNmWVCqY5KxrtLsUp8+Ot8hJxmoWhN/90+LFy9+9vJ2Jlz/jLrUuZijRYgxgVyeUquPbikg4+w9nTPnYef0kiz'
        b'vrrUoB/dBWr5UvBP9WjTlfrIidmdtbm4gCigGAZ1jcW8VNnGtYsMNWU/pnNBJW7uwlffrNQTNxLKW7Pg5dEAoQdCER8d+DEth5V05in8Nt/D3bzyqVzHj+5IpdCRwBIX'
        b'Uffbhd7uLvQar7cZ3VzAj25ynatJN0Ptr8l+7iYH++UR/r3xykpcLm3+2lZ0tO2Xr/j32paXeIoO/tof3LHiP8CM+OlFJ/cD5kXHNyC3F92zOh88oxedKM80CLVJmLfu'
        b'B3lvCQ5QleUP0a82vbbpPfmL8v0fodFHbQ3i9lNlSp4h73mDmJfIE8ib7JwqIutjq+wUkRaQ+3MF3H2AnPLC37gJeI22p7m2BZTQfeXhz4RWoVWRw+vCPXAZyyCU6fFk'
        b'TT3dKzIbHsNgdm00Cq1Ba0LbfeBIr3qVQe0Bzh0qGPlLbXar0Whvl9XW2OyUaW4Xl5nsS9sDhDxL26WL9EwODS4D1r2mWpBPRXZ9RbukBuDeWhbssQ4UjYe61oL6DTUE'
        b'u+XKEPe9AaHCtQ3loc6lD94gh6WXw9IHs6WXs+UOXikv9HgXrmX46g8SH9LlOIPBBuID5YENxlK6C+F/mdNKTmFkNv3PIGAy8YfJLnpFpaPC6CHSwezYTCASKQTXByqd'
        b'2Yx2jSIfoNyrHooOqunBjKm6tsZKJVFXsTK9BcQbWhREI6uxzG5eqihdSgt4VaJfpDeZ9bRJJg1QG0ubho7URFVssNecVTolKlqnVx1QtcNmslSwHrmrUUSzhYt+hhmZ'
        b'7BxtJVWJePfdK3+UXW+tgDYMLrxEyyuo0tBGpRPbQged3VKrvqzKaLcpRzy70C/A7AjFuE7kRTGHHZPO81eMtjxCwfwc5vygt4PfWoQtMkJRyP4q5jht7/zmd22lEQqq'
        b'8oSlYsLoHE/bO79l6eYDMRaeijn5Vrv/fML2hKzCC2tDpcgqzFcnxqekKOZQNaff0sKeBgF1XJE6a6JijvPscF7MHE9fDv+Nd6ACKnILAQWtyNOC2G9xQB4wmZWwNWC7'
        b'2sqsplq7k5pROKUO3mxvjTPbagB+jQaf2gIAJ5qb0h4zu/yHLbZGMVFQGbAtOqjQrq+upn5wlkF+lQdsMwBgQQdqnVvLYGLXD+lhWhebgMYZl8CKOzecdz30X16N3Shs'
        b'E7b5jfbKGgNgkgpHNQAa9EVfBRsQNo0RZqfMqKgBYu+zHmFIdNMwXYhNGKbJ5tEljWIyIDUXQvJZi+e2o5oTAHV6uVKZGQYs3KtkM/ouqXNerVRTxnounKqMrLTba20j'
        b'YmMXL14sXIyhMRhjDRazcUlNdazAd8bqa2tjTbD4SzSV9mrz4FhXFbHxcXGJCQnxsRPj0+Lik5LiktISk+LjklMT00frSn5AT0GpoLdjYUSeg4qrueT5KluOMlu9vIcm'
        b'j7rzxeA2kAeHFEoqyVXSINy+cpK6kybCyza8HcWj+DJyhgn7hioJkqECU8hYXc5Jmxo5qIaUtA0brAXi3oJvCsR9KtkQQ5pzs9XTqGPstCjqajoTJH/4AzQfb8MXA8kO'
        b'cnsAs2oht8k9sh6a3gyioYOcJxsDkITs4eXdyAUHFU5XDV9Krmro/RvyGOp/Sx/NuSD/DsAnxOROCD7vGEvruY8fKMlVkLBzp5MttXSE5F5JxxALyIY8KLlJO70WHvk5'
        b'2WSHGJFGvDaYHCe38CEHFfVHkdVlwRplNr6HDwWhwGx+Ad5LDuE15AZLhn7uG0GuZkEFHBLhy+Qu3sXh1WT9ZHZRUz9ETgSTDbEasnERvg7tqnBbNojUGzikmCIR07ug'
        b'2KU8JfPiyNXYaA7hgxyfyaXg/V3Z7FYopEiONizmFDrzb03xiN1RtaRPli0Epuu60KpsLlkzgJ8SRHaxK6SKK3rT1JCQKWSrhmwl13PI5RiyTYR6LBXhcznLWKZxXfGB'
        b'YE0Wfh6vhd4052bRORGhbuS2OIw04L2mN1YPlNj2QM6WkQHqFZJf5AbhuHDJO6lZj/50JuaE9rN3+4nv48OH+wQ63rSocN9j99tiFVe/WfJufNf6bjNGxd0NHFxUF/XH'
        b'DRkO5QHdnt8OS2xQT131QuJL77+TtPth/M+n5Lz16lvypFPp6soJ2o9Nk7TFb1y7fWTeyDmnXv/nJ4/sd7U17dHfLyVvP6+5c+DX1Q/WTf3brD9sa5416Ztfxpz5fVjY'
        b'weiNg/orpcwpeWDkVKqKEXX1UMYMFZUHlDE+cyq5iQ9qXSqCmlFMP+FSTsQkSkjLGE7QluwmF5TBACqZuOEJfUz5DKaPycAH8TXK1u6f9qRaAoDgFj4qXPTTDHDbGJOn'
        b'JkdCsrJytSrSrORQd3JPnDB5inAZwE7ciu9pVVGZ0A/qg3mWJ+dzl5LdsZ1u/gj9d6/h8etKG6Q3GEoEHo6xzcOcbLM8U87JuO4cfXr+iOkdPPC3J1fX1c3+dtQhsOch'
        b'gsahGLlM3OjtINa59DGPPubTRwl96OhDTx+lqJOOw7dPcLBQZ0clOncTpe4mQtwt6t3tMK7eQKvw5OqHvemDq/c1LGVgu9xALf+cnFJ7iMD/uoJSfTX7S+9PMbYHOs96'
        b'y4ztwZRbAR6RWoIJPXEPtizIAxVTlUy4CxVPo6x9UCfmPhTY+zAngx9OGfzycCd7H8TY+2Bg74MYex/MWPqglcGFHu+CW/lXLQFPZ+/1bms+hXCr0jMwsZOoL4SQWwGU'
        b'FOYM+FPgDvSe9whSDkKlqLDWOGohFRhnvTdlqqkuNVn0Ll4lGtiYaEZkBRpLdQBu40/aQbdY7FUTFZP/nzzy/2d5xHOrjaALJcS4tV8/IJd02ptCeSHKVYFP5mzOD1iD'
        b'+m1O2PtCO87t7owT+FtLDdXmWBkHa/HNly6uoQykqVpv9sMBz3mKPSzIFb4tYv32mGIpob+lNTVVtL80RqPIdUKXnoUVNaULYOFB2vd9oGih8lBaSly8U0FGAQGEOVrd'
        b'nA5bWb+dcCPJEYrpNofebGY7AwBnUY2pzL0b53iY2j5VJHQi2c7LwPzw5nia4/6g0EaLPyG4dTL6/L9A7hpvXGyscJrs/D/Z6/8C2SsxJS4hLS0uMTEpMTkxJSU53qfs'
        b'Rf89XSCT+BTIFMLBMZkjmfsVZRLG6sxcnzLkSKZ8423cghu1WbmkUZXFONoYfJ+KVr4kqlX4fmDSAnJN8BI41YsccYpTZCM+1NMpToGUdcVBTWrIrpVirSY7l2yMI7ud'
        b'lfurGUSWpkB8CrfhfQ56FEWuLSIPbPkzcXNuvvMuJNrKTLIFirSQDSBcBYE0AlVC+HbhXLwf78XHAhE+S3YG5+Xgo0wExef74QO2bNKclZuvpfcnxYlRz+Wzx4uAo99F'
        b'DrBbF6HuvXibLboP3plLNkdRLh4kmPNRHBpQIZHMIjdZLhE5lxsMXP/maTLSrM4DeYvsJad4FJEowkegU1sclO8di8+DCHfV40AbJCB8fVqBmpyZJ0XxuEmyZFUi6xq5'
        b'Mg3IgtC1LJUSxnhzpQRFkmMikPW2VrAFO9CDr+zH0TddjnVJNnLQy1zIWfGAYClCRWgwPlg0G+8WlvEYSAuXg+k0wYxuJTdJQ2omiJ7NpJVcp+JoEz4LoRyyOZNKZHN7'
        b'yaaMqGIiOL4HUsY1chVes1AU2ZNVRPYIl7Semd4dJHOQykk9bovHl/OYTDmSnKhw3tCKW8j+WHwwwfzN48ePv9WKR1/mGHTJP+wzWDiz3z9HWnwdAbes0KkOFXDIQU8T'
        b'q/DWUDo/zexot2UqSPGZqhn0CuXY7OkAF5lkU2GUEqAjM8t1X7IS35hG726VWkLm4QPkOXbpDGmzk8OFZEditgiRO/g2R84hcs5qdoyiY8G7RgSzpYIZuInbpnVAjqxj'
        b'ltxThC+QbWKEG6YHzo4jDezmLgnekAQi7xUQu51C8dQosqNQFtJJ/B3TTRpKrvRjF0KHkYNkjS1bnZ8bi8+UUEjKc0rASrJbApN8iDQxUZusNeHbMdmTtOzGHKUUBeMH'
        b'PLnaXcWuCv5gSD7/khQtuRS4LPj3s4yLhwqmDvYhMeSqU90hGGAAiJGNsfm5U6OEq3eUM8gOfM7TvuMAPiWn0IlvO+hhhZlcXRijyVJF41vzOSTFLXwsbPZtDA5Msy2w'
        b'RcjtapAeeSuXBvtpjVLEbqfuiS/iPaxcX6uzWBbsMAok0SPpBbT4uN1ZqiKc6S+yyQVyJCa7OK7zAPG1INPPHp0R29JAiAr4dMy8LaPyROPk6z/tVZOyLzfzG+2Vb99e'
        b'Pfj4yclHT17dsD1Tpu7y2xySdPIdXnb8g+7/+E3tsD+W3zy65+uHSx+NLBv8ye9rJ70y6crbk3cOzdsUGvPLSvVX5vd/MzvlxEux5tmKr5pSPno89OKWyC/n/XrwnoGz'
        b'xy97nUtqCJ35Wu6ACxWlxz74uComJ+JB4ytvhPSUvHU6Y7Ni1Nh20+2Tj/IaTk8JrgsfVdnv15q/z7Dfe//lEYHf5jiujfw85Y1XNn91ic9q+RzLHi388OV9By8f3F11'
        b'5iXdgbXJF/5klo9Zv2t6/36/KB8jKX8QcGrk8H+E9h/j+M+3AxZ/diys/0bu5PcpvZdPmhpXYn/+0NzzV59/71FV4cezvx7wqy8bX/gvy6jvE/5wt+nM797L/+RX6ssD'
        b'Zm+bv/KbDfN/Pr/g538oDcson3bnROm/AiLyLVn2z5Qh7DiMA3g65TIXgZ14tENLUU1uMTVFqLLOpaQgexUx3loKsn0lqws3hwUEe5iM4M3kslNNYcO32T1s4WFkh1aw'
        b'+iCH8S1m+RE2Q2SeiI+wu7m0vQJiovEDstlp9hE4m8cnrGQTu9Or+5CsGA3F9aopURSANvNqLT7Eksgl8jy5rc0hJ8j5aCni53Gp5LaRJZUvwlfx2ZxcFY+KC8VaDl8h'
        b'LXiPcK3xyen4LmBuwcoD34pDSLqcH94Xn7RTPAx06RA5iZvygazQu8SifdiEXLUwixTNnCAf1h7kNt7KTgwl+LBwmeJ1fHKcje4sNaVcbKrxary3C9kiwpdm4Y1sEpbi'
        b'Fp1WRXbJPbQwS8n56U+5bEsZ/j+kkfGlmwmlCogOmZzpZ2ZQPmEV09DwgnamQ0cTxG5AEzP9DA3J+FCuP6RGQhw1RaH5wlkumkPOB7GS/Gr6FsHV9eik+OhoV9DpyAW9'
        b'ipE+yumjgj7orY5WE30scOtafKlzAp7lzuUgoc5yd8VGd00L3O2EuJvoUOzQjw8Ueyp2ok/6UOz4G1+ZxIMFo0fone9klzQENCB2pso1BDF1THCD2H0nu2SDtB6tkNYF'
        b'Lpcw9YuUqVwkK6WFHu++DtZpQ953socKvN7O+TwSD7kEeXTmqqxCJJj4PVogQbIlozmg0TmPB/dEDPFnLSc7bbhZtlAcJ0KiUMD868aza9Txg1F4UyFuLiLN03OnkusF'
        b'5Pp0fBOfD0mJg/3Wr4cIr8EnyQPGDNbhB/hmIWkuSl5mjSONScBoyRZygCkO4/UCybsxh7S5KuPQFHJMEs3hvcnTGFMzeYmV3b9O7nEj0chJ5ITQs0y8hxwjJ3hUhE+g'
        b'Yagn2d+dUX5cTzZGaTVxSQnJPMLnyA7pSg4fDNcJfOkuID6bYrLVnjeenywAWng6w2RvChbZHkKuI0snVreMyxbHh086uy1vxEdTp4ybGPZO7sg1F+bNTpsQ0yjSrPvN'
        b'T//4mxs1W/q+kFGcFTb4aNO3j/61dPm0tb2C4jKHb/48SDzsasauuEHHzugnPPepNrOg62/3ot8bjg/4tOvDC1233Rf/NKQg9djJ6XPe/DD0FwPmXvzFsJfXzH0xsGLI'
        b'NyuuDUzpF501enrNgNckRcXfLfipoWTAS9mv71xp+tUHs7t+2fry6x8e++c/8268FlY864+/zB+6+fH37z6wBRddfrt69TzrvyYu/3iYakNBTeQXdQ/+YDK13epzq+Vh'
        b'nz6tJW/djG1cesD+2fLJovONt+tvfSf9uI+uQWNQRjDsZAYacZd9aAD47c3kIo+PctPx8zaGbPG+0GSGbMkZPYAOxbaAExnq52G697uRLcW0ZBe+xg/H93szkzm8eUkX'
        b'p/ldZzy7Eh+iqJbcljMltpbs7coIFtCttk5qdXxyJWspD9a7RZsHPPO2vFzSAlyUGIXi50UlY1IEJfcmfAjvJU307KUH3i9B4v4cPgr8+ylWPB03kJtPXLeNr+PrAZrx'
        b'zDgSil7HV+h192RXaozzWxrsvvtZywQLyzW4ETdoqYUluSDtMLLsjs+L+8jjhTw7tHi/9gnbyYgFovyR+Bw+0ZXRH/wc3l/BSC9uJVvcFoydaO+KDIGwUPPaA/RWS5g/'
        b'IFdHXEaRYf1F88lq3MaOI1aQM4GU+kZUuqwuKe0lO4eyVHzJke3W/OOmXEZ2gK8XZgWvIxvwTuGCfrKpG3ngvKF/EL4gXON6H6/FpzrucZ2Ejwu3de5cxOw5CwJCgMWD'
        b'EednSVC2WYa38DX4WOGzYeT/1rX/LqMc4ZJ/Rr2Ou6mXLDaU4meGo+nl5JRy8fTnsZjnv5eJ+O9kYv5bmYT/L7mUf8QH8P/iZfw3fCD/NR/E/1MczH8llvP/CA/hvxSH'
        b'8l+Eh/F/Dw/nP+e78J+JI/i/Sbvyn0oj+YfSbvwnsu78x3wP/iO+J/8h34v/K9+b/wvfh/8z35f/gO/Hv8/359/jB0jfFQ8M5btDI+GUFnqY9gjdF4hgQAf5aQ8QlN62'
        b'donNrrfa20WQ78dSPIm1lr5b3IStxk3dGGGjl9Gep4Stt5OwoTWKXz/dEkno7v+CaVi5UvToz176C8ERzO5yPHHqgc1O9YzVaHdYLSytWqGnxwwe2p5nUtErqoxLbVBP'
        b'rdVoowaYghrJqRezuc8GnDolX6r1J48NzIIyjnandKnd6EPt1YlOSz0nz8OYn5nB1+K9w2HX78QteCO+TLbhKzPxFXwZn52KN0hA8FqdahItI7c1jB7OItvIbtIKC6tB'
        b'tfQY9gw+L+g5NpMTixgNx00z1WSnVqMxhIlQJN4owm3F0xjtnx/LW4Y6lQnLkzSIKSzwvv74BBQkO8lqobB0ENlRCkLhcXI0AUUnS9L6kdtMCIwkjSVUBkwk+6KdQmAp'
        b'PsjI8fA+OUDZod+bnNSdkXbrCOEzLZvIOXIXMIhtjFNGJBvHsmJ6sjoVWAZ8Ap+ghXjczPUl68h905XfXke2eshxcUFR7quwq+LD17/79Qj1z+ejK/1JvxlWkepWVuu8'
        b'hkN/n77/SG5aVEjbC9/95XFKWtDiopS3Px85Zu0bE8aFZIf8dJgmetjwW5Ez4osrX9Rd+XDre8lfJW7+sv2XH75y9KeSvNzHzw0dpTqddeqnf/yPkl82L721bHFi6qxH'
        b'n792pES++NV/BWv+OrT5zQSllGH9WGswkLhIfMH7kBaE4+cZotT1wG3CxcXhpIkqK+bzg8mGHDuVk2PIzuoYTffeuTyM8zSnncszgjaanJ0EJFH46AePgo38ygJymNTj'
        b'FibAkbMD8ZknxRMDaXHbMx4h6wUcvw1fG+H6jsvmUR2ETVaklP4ACvFjCqm3ldCtxrDuIDfWFZsjRNQsPYKLEFF8K2c/0u96SsS8BxJxFv5BM0krPD7ojJ5C9z0VPTlr'
        b'buPaxbV6e6X/O95HI+cF2vTMk34PQuq+5138TPe8A7p6V8T5OO/swFgUedj0i+ib2eyJu57dXY4OYoQiq1wRTd+iFYB8bYJmnWIl4xLqkksVzdGaOlNttIo15ESPVt96'
        b'ahu9etDg1o7rrWWVpkVGjSKfKvMXm2xGNwpkdbABsOx6RXmNGVD/D+AzunCBXvhMlscurwepez1ujMmEHVKQCXxMMt6SnZuD24oy8XmyQaUB/iKTPBdQu7Kv8MWEM+Re'
        b'mBY2VHauhmyMTQSp+0wR2UC/hQXcjDqK3j6jJTcC8E5+DtNgkWv9q0grPst0DCJzHjnP4bWBC5kQkVxEDsXA+i9Rk+NoyRCymekr43iydgW+HZPPI24aIntn4ZOm2mEH'
        b'ONtNSHSsLhiVezcIEMzbU/I+y/vlH9vnn9j3ebD5nMqsmvi6ZseG2oO61qSflmasGvivwtQuhllvHfjdni7Pj50YH/jZp/Uq6fIjhs3BqT02/+VmW/ak86U7XqjfnZYd'
        b'/h87p89rKp81OPytY/Wzhr/1wu1RW4f/MrTs/ZcXDlq3sm3mPvQi7p/9xpC/hs2p3vuXkHc/K/n22/F/vtj1/ait5/kVI2r2b0x87TeP68t7TdKtm3N/7buPilLeP/3G'
        b'Z9bCL7/nXxuclmBfqQxjXjqjwzg20wD5qWLyHIcvmMgRgac73IMylao85+fgEL4oI038CnwhlnHC03PIbXKVXFs8S+W0SQnEp3h8DJhp4bMQPchzk1l5wHXb8D4eSfP4'
        b'vmTtHFbaBEi7nn75TkU2Z2iy4C+gLnKJJ/fm5AtX+h8YnKdV4c1Vy/OF7xsEj+XJ7qlkF6sbH1QIxWPz1Q5yGOpeyUdXkgsCj36H7NVRflOpIS1sbGFxaaRRVCHBjcLN'
        b'8s+v7O+8Hr6KbHNi2ePkkFD6sgxfjImlZxlqjZIHHHgoc5QIQPIaOcfEnGTcwjHmPTZvJD4tQdKRfI9ZNQwXGwF7n9K6wZTcKwmM5PERNT7NxpSDb62kQhCbknNR0Ovx'
        b'fE+YsedZw8Bi7wPa5WSyKYdN7pHLwGXjhjGMOJC7+NogoWfDjNAuPs2r8KnAp2mGfgBxeyBrMd3DDFOr3JgarZIHUt2OjLkSyblw9qSamnCm8en7mF8tflwX4sastA7h'
        b'snvn1w/sqJMGxn9P23ghb8cF+Ivg8Zji9b5uvI7WdH/s63sIndpXOr24JyHq/+92jQbs4vynlAh/ePjt+sRlWNR831BTVlLC/JPaZbXWmlqj1b70WXyjqL0+M+9hqiDG'
        b'NjPixEYisO6R/+OKuqcuqjUJHu8j58e96CUHQWKQcx7zMHuRj/mhUqC+MIeiH/c3VCwXBTlr6f5YHhtO30V9H/eeGpoq69ObEywlN6vxIVuWCu/HJ7LUttBQEQrpx4No'
        b'2oTbhDOz5tDhwbAv8G1ymWKYYHpQU0APaPomiAeT++n/C59n8vkpHu+zzgDhlAofwCfIg4XkAPWpGYgG1uBTTA2F9wJDdUurwZfikqE4Pp9EbnALyZVidmxhD1vUSW+E'
        b'9+BdPDlQjPcyhjV9AD5MmvRZWSrKiCXSi9Ga+Ow4lenPw+s4G4XZdfjSJ7q5L1zacqQ1fv1Crizgff7kenlwr4xxqr9Enoz8y/ocXYo2KHjW9iOZF+rj1x+pP7Ijaxs3'
        b'pCv9gEaWHVVKuow8n62UMFQ1axS+FuNyoiyspm6UE3GTYFa4Ge8BBN5EtpC9HRiHYpur5LiAgXcXABkWdO7ArZPGMVTpjk8OYqhu0CCqwtib5hbrBaF+K77IUGwhvknq'
        b'tfh2GF1WljyPN+Kr1U9znZGDfAUcjbGE2kgwVNTdAxXJhoTy9PMaYkA8Ys66zL2pxO1iWqBd6vRn8/o0FL2tzrrcvSloyYH8E4gl9A8+vqhHzzWm1gyOicrGt2LVmaps'
        b'3BwrnOsqyE5J5Apy2wuawp1/bSN4jxtARtK7LwBceYNoXWCxyChmn9FD9AN6zXyxBMIyFg5kYSmEg1g4mIUDICxn4RAWlkE4lIXDWDgQwuEs3IWFg6C1AGgtwtCVfoLP'
        b'MAq2CmfoZugObcudaT0MPeltH4bRLK23oQ+khdIQcLrUcUds6GvoB3FhhjEQJ4YSAwwKeifH9qDt/HZRuWi7eLuE/hh6lfMQR/+K3H+FWOEpFnJ4PMVPvhsG7g8zIcOg'
        b'7ZJWzjB4exA8h7jqgvehQl54G+Z+G+5+izIo4RntDse431TuN7X7TeN+i3W/xbnf4t1vCe63RNeb5xgMSfv5E5wheT9f3MUYYexiSOmFDnc9guo5Fkp1hViOSGZBKbhG'
        b'yWBuAwxphnSY/W7MtjKAzbfEMMKQAXHdDb2Yq+bY9sASIGv6ycBjM/91rwOCzlKKYKUpZR9blLqPBSTPdCzg9S1c+s/b3y5IOBb44zjhG4nrJ+rkp+NGC4f05ZHNqCeH'
        b'xv58ms7yryCJEPn7xOXcNzyKi0zW9xnRTeP8Vm0LvrLK86uqmSCZ3sO7PaRTQEZNAaiwQha+SM4qCg0YjIDEzmoM1ZVmavXor65OfkkfpkN/+Stnoyc0qa8d7bdpXNDq'
        b'OLk41bTgq4Cg73aEfR5R8OH5R3xT+Krqj43lPXYmJ/xOV1rwYuknG0ce+VVw/bQX0+/eznztbwXjX+txNunOK+98ojv3+jef/3pfZcW36R++k7P3n9+PiJ6R8x8BrbG9'
        b'gk6+rwwU2M+GOHyQfn8oELcCmyhCsiLeTm6lCKrUdWJ8BATri+zYcT7ZIx3OdyF3yQMB79aTq6ZgL9/6yZyMXKsR3MfXdU/oJLB3DXBPytBekkqyY5ldQWu6SbbJBUf4'
        b'mCi1MHOQpUdfMSIHR0aOFXTDR7vPFj6UhJvx/oFMsw6YvgvZJ4JO1pOtrKpUfKeXO9c9jrTk4nP0o7k7RPgY2YLvCwemN6PwPtwUSzaqx8dm0Q9Qy0gjj9dNm2uPod05'
        b'MToTNy2GOuxMYoCaWoCWHMkH6rIxn2zWSFG6Vop34ueWC3j7mXnTDk/3/h70QJoQxMkkPZnHu0uNSz8f6N42Tzi5C2rTdgmzsGoXUwPddnnHAZylpj3QZKl12NllYx0s'
        b'q6flu8RKNUrWNfSxDrm41bWd+hn7JGXp/ktfn5rz7uWP8WOWlNDu+/XjHQdB5sfr2Y7bnb1vx32pXt68GquW4ppn6Uq50JWQEs859Nulia4uPerv0by3J7vmx7QdVNKx'
        b'Yv4anuJuuF+WK7PLQvRHt+t2I6dAVFJt8u/Kne1utjuVThTl1prq/3Z7+iV+28t1txfJ2qP2w/9ma9ISe41db/bbVIG7qV5FNKPLzthve/8zqn+fVIpH3t9MZCTjJQ1P'
        b'Ofsl3wfqVBerzAJB+grRz7gjmXm4Luf+gh7ItFjzptjGLoo73U4/75up326IKs/Xy8s/1H2IvtjXq3D3S73W9hogSUtEuiGSD0YfUHJ2qqPqMasS3x/2JLrzRnWk+SkM'
        b'L5MY3Z8UdOG1oBn0K7l1XTwxxLM7jBd6MbZnfV2s4VX5R4/h3/+CyOVz1bxFLueq/UwnZhz02BkxK3t2OzGDTUxkyU+ghitzoVIuT2ZK/68dvI2ee7w3eLHwSeYthlkv'
        b'7Ma78bUtbaJXb+rZhyjN9x0cWtAuPVQerOTZktWS1Xj901Zs0gK6ZqFA7QT7ujR6aRHZGK3W4D1d6XHFWj5xEml8mgQTVsKMpk11xpJSc01ZlfvbgK7F7Tu3rpfH3HfO'
        b'3ekztxJm7estzLSiTlqSbfCY5bXmvixP/LfbabO6lp3CmeuztyJYeNF/V9bmkO8zLLbwfXv9k3soQgU/naEb8ELtCMGqBDdoQdI+K8aHCHAjdaiObEDMYjCYrDVS57Tn'
        b'8xBahpbJyHpmbEKujiTnO7GW9KOpUXn4Nrmj5lAS3igNxQdrmalpnzHUORRlfpqpUy2cMgkxq8mdY/MEq8msTwPf7Cnq/U/kyKD17gZB+YbrhqhO5pNO6Om4HIobiU8j'
        b'fITsCQKxuj7euhrKM61ByES8mTTFk2OdJf+MuaZxn+3jbM9BFvWY9qGvxUesjYsUv/6HQ+IP+BG1wTHB6q/E/7lolSpn0k+6ju/V22Td9MHJtfaMq/9Vnvi3JaPKh7y0'
        b'aPur69Zn17wff2TsiYTQwAX3AsnE68EPXn31iy6O7+784SeB+wLfPD97xftD9w8/9ukq9U9mhO9T5oXtWDbjr69ffHDiVxe+4Ov7TJ468lf3VznwwHW//U4ZIHB7reRc'
        b'iacSdZUchcWJKmrkTFmZjm9qgiN7ed8R1R/vsNPFyO4recpmm5HNEGTxCHZGZcHryNpg0oQbo50ygLvOAfiqmFysIVfYHh4YgjcyMxHK68IS43MgkruqldbiHSgOn5H2'
        b'7YP3CnregzVLtWQz3ubp0rh0imAoUoAP9NUCvLQ8ocHYRa4p3V8a96sulZYstpqcH4RVeGxwWYmY47n+wJX2dprEyeFN/M+6cI/tx4p2/qi13lph88N18tYdnff8dnjM'
        b'fXLPhx/1deb1ZKN5ZWKPLdnpWNn5QWPm7Of+oLGYHXRJYLeL2W6XsB0uXikp9Hj3p1mTeO12aR7bv0WpszE1/ya3xg9AA8gOfJiJuGyflIGA+HzMVPUMNb4Qha+JUUAX'
        b'vj/ejK+bJk9t5W30Ys0r/aqphmwLfuvFt1+8tOV26+3627ub6zLWK3cPXH+7vq0+vTlr08Dda65K0FmTzPLF34BoU1mopAifAPmFanAwAAwzVsGN+D6H+lSK8YZx011L'
        b'8nRNubSEOYCwpQ/3WPpQs5gppzrNOssqqMSlHmaD7LPUTC/VGcG3iYXYJ3KyZd8JD9OTy+7zA8FeHfC/6mMRsy5EDVKmiqBrH/A/sfbe6gNJnrDITH7eiQ9PLKRrvJND'
        b'InKXy0jLJQfIA1PzGiKyUeX6T3rnf6LT6qOMUaVagR3TfaIzlUf/5TPdR7qq8oeGT3R8Y1xKouPKiTjHpUWXTsRvjBcn1p4UoZLHC6/L/+y42sG6PpMZTKfPklN9oscq'
        b'R3pucKtgJ0TtVuu6eUx0Rxmhql3+YWm3e02pH3vNk2vas8XHmvpu6iN63uB/dUcKe1ri3NWS/51d7VpZyjL0Wi6FdSU7EjNFSBJAbvfm8NpkfNV05e1dnI26gnT53Sef'
        b'6L75Psu9tJn6j3Ua/Ye6h7C8D3Xh+srynLKIMmDhXkXoVGvAPzPnwPalWAOv7b1cu6wsx2ninUKuPvtXiNtDS5zXr3osqyfXLasTU3fynh6z3KmAS2XReWO2S8v1ZfYa'
        b'qx/MLbbu97eZ98Fj8ZMLH9ngY+H9dkkZJhgod9grU1Pl9pAOebzKuLQ9ZFGNo6zSaGVF4jsHE9qDy+hFNkb6Ndl4z0BCu8xgsgk30FCz53bJIr2d3lpsdNhBCqW369Jd'
        b'2i43Limr1NO7X2lUMctJjaLi24NcN8iYDB5O93NYDrvJbjYqZexczkrpjpWyWb5uU85rl9HvkNAq24Ppm8vZnUWzy6xYewnWY7TmAOpzWVqzhPnlt0tqK2ssxnZRuX5J'
        b'u8RYTT+my7eLTVCyXVRqKoNAwLgJE/Kn5xW1iyfkT5tkpQ5M1mvoCQUIXUq6vpRpYLjJeYOylNlkcw2yctmP5I297LBFzuo776sygTf+eskK7pu6PmIUp+9zIT8SMVOq'
        b'LriJnLEtyyM3wgCgeHKSi8Z7JA520cPq4Xidzb4IksghfJJcD+ZQANnLh+JT+JqDTjc+pwYmmRyfQA1Bz0dl5mqycqeSDXn4vIq0xGZPzVRlxwKXC7yYy2mKtM6RTyCb'
        b'Zgh8+XFcP4S0TkXkMt5LGfPcHuMYXTfjwzGJSXFTe4kRNxzh1sVBgrvZFiDx5xMB2nvMS0SJc0czoy5yAvi3S5B9eC8ecVEIb1+FD7AjtJWmQsHnRI/vQh84FFzMkwvk'
        b'HF4tWIPt05N9UA4/h1dLEadEeEeNUjDbvoL34xvMthdvwrtyk8VIQi5zpDWZXGRTqZ4VjYp6jpKicF3py44xiJ3z5eJTMqjOiC+BgBkNtClqCjv5GUbukTNajVrbT0M9'
        b'DHPVpDGHQz3wcfHYYeSWcJ9s7kA0duTXIFzq5j7UGgWxpXQxvgD1ifEpEeJUCATTs1oHs6hYO5w0xNA7V7IEhjOsMBA3i0pX4eOsNtuEHkiVVi5FCt3ID0wVAkINI8fJ'
        b'ejrao3hvAOLUiNo3k2bhJPI23keOaQusZDP7yJJYxeE75AHZwKr7i3YMWj73cACK0yUsnjVCqA644fO2xCR8KYxcAJlMQw2at5NWNu+4ldRDBzVKmL5d2bkgMgXG89D9'
        b'k0tZfS+mZ6PtY2fyMHnRZelLBTgkV/NVtDqyE5+AVY+F1SFH+gnm+ufJPXyZmrqZq8nGLGqw8Bw/mBzQstqiNcBw27uJqa9f9uhgZ23nQHRqTExKIYcAmdLJ24HXqNhq'
        b'KEnDNC29oKaJbNYy47RQXE+24HWi0dX4LqsyclY6qlU1ByCdLuK18gxnlW147wRa4/MreDbeXcBg7mBXzZDnzbVClXkuZTuHxuDG3ni7GDeGBTDo6DZ1JZROxfVSNrrd'
        b'ZN80tpjD4/EeZ2FhMUP15PlaURo5sJB15vjSCDQkLoR6T4w8MnmV0Bm8C1+wJCbEkWPdpGx4O/F9fFcAjgu4ZbIAunfw1dxkHkD3Cke2403LhaI7QaC8n5gcR3aMg6lJ'
        b'oBF7pGxD6EhDrxitSisBmZdDUhPfC7fFCEfYp8nlsMTUuGlhUCQNet8tWlianVPHC4A4HrZYI76IkHykKNwSIThF3oOmbkAxfJjcg0kbQYHkNLnAispm4gtaYbImdFNS'
        b'63p5uKjbIHKTjfqd3jIU3jOCgyVQNYpsiPVvKNkP2z81CV8GQkBr2xOFr7NBGSeGQTfIBnx/ImnRAoSU8X1EBQ6nU9cufAZKkcvkLkBWBnQio1LAHLe69tdq8TncRo4g'
        b'xNdwY2PwHbb1puEGshfKzBgP3R5JYfG4kdU2vggEwebcXuQkrNgmmKSufKA+jHX5y/g69I9ZqQEA1t3jUbawTfAD3EIO4KtxSeQU3i5B3HiED1ky2AykkXOwUCDQHs3J'
        b'pmcpIvI8h/fhxijhau1Rk9GmkZvpJg76x0KtMAP4gZicpLWNJgcAKUxA+PDgHmyFJAvUWsArIOAcBrZmPhcrmcqqsfToieJy0nmYyJFfFVc5Yfm0JQnmvgykagkSizl8'
        b'CKjAWTby6eQovsnseifjkxqkwXfxGmYdjI8UqvHZKNKak6ualgmCsnqGYBxHNuSqAA8hNCUioI9iCcMAY/HFAuZWW4ifE7aDjOzm8Y6xkzru0L5cQt2C6njqFjSkb4ig'
        b'kcG78spJK/W+OTlLhVT4+XDmzdp7LADLgCGdbE9JC9AZMRqKz0gcsEBnBYDc4aBXeU9NBuDfFkcaAZdFcPNIk2CxJw8EFFpEmovJeoAEsgeAA58j+9mNW+Q+OUguaYNJ'
        b'PXMT7/AR59DQfIlpMtnHVqAOnyVtZF8w20hr8fMIPx+qYBXUZODWmEKyFeYkl2zOVGcLgmG8GA0rkiRQcy027J9U90ZJRV9Q7DdyWbTM6fdEDnFkXwD1Rz6MH1CoWTeJ'
        b'WVMPzl8UQw7Ln6yTR8OmSxJHDWbbrI5cw+e1U9X4Hj4H2IB6Ht8HcXQNq3kiOTu7EJ90AF1uBvq+jOs7J00ApZPVZL92OmleWELn4gQi1wLHs4GEkufIUW1W7mjYrY2e'
        b'8zAAN4nJDRk5L1CAXbgeHyP7QqiNHd6O7yF8j8ebWbeTYX9cprtbk5UHRbPUCWJqlnawD94rNudkMYgl2+sCyT4ABwM+gu8jfL9yqmBAfgZvnNWpLE9dHrf0wfvE1T26'
        b'MU4gOomcI03wUt7fhEzp5KLgx34RVvM0NeF0dzkMbyRruooWwL7YIfAcD/BB4GaY1uBMygA0wErWOoTrwK3keIxwkRlAl9M+Y4amL74uJo3kObyO9bpsQXeyjxoxrgeC'
        b'dhfhuzMNAuDegn5vIU0Azmkjq1BV6VjBfOl8Qi+tWp2Fz0XhIwOz6X7rOlYE2PgIvszq064E8rZPjtAyfBpfQ/ja9DkCGl+fRfZpPa42DzPguzNE5u4wVjb7a8kRfMgW'
        b'EoKB14f120zJ5InBws7SB6FIlCEGEDNrxk0WdpYO0e0Kw44BNgfVmMgaNmwtaZsAvFsmbPsb1CF/kzZfzbqp6CMG1NlE1jONZpVqKPc6FFaE5lr+kJY/UYlcdOG4GJ8V'
        b'031xsA7V9cHnTF++tZa3fQ2Mb/Tun8379eyaN8aGB3z+O8fDIdWtt46su9P3yNtf/3b8mp07x8/529W3Zy7puWb7vYlT+x/oMej4ivHfyf5Y85M33xEp/v71kqrZIye+'
        b'8u3IjIMPNwXeeenMqQDjf34XtGxw7+j3h7f/etaew5/8JPJXquaic9JP9Ru1D4evPHduwbv/CuvWtWr/d9Vrh7xw6lVu1/mdJd2ONf/yt7KlecPC8ye/VPifrbee+7ro'
        b'lqVb6v51g97YcrJ11KDELffzigf9l+Jq3qCt6S+vHB4wMXR8aLqpqa+m6GCPdD794w92v7zwZUvD8Il53UeMHGq9U/DXTS/Pfjl9+F8naSI/nht5u2jLzwfNVATndZ90'
        b'YfyF9NkRt0Nv60dlHNtg2repYc69XluVLV+90zKwcNuy5+IWfnlqc1TbF1eml33XNK3kyEPTYv6N/Q+X1j8gyvlZFQ23bhyTTp8ZNrUl/M3F7+eFzGh49c+9vpofuDDj'
        b'l6f7PAz6U3bFyOyKvp8veO/9u12q5rcuCL5379ijpuUZ//nW2n88PjdH8qcPMn79dV3djfWvft/94hfzLje/WjD8g9z0q+szbg2/GfHFiq0Bez4n55oUuwx7B5zIeKXl'
        b'BG4dv/7UtseqQ7aXfzlp/ge/fmfXoN+n/P43W0qyvh3xpztb/vTtzcCQlTFfaMZ8Of+9sG9/teD7D6yjm1a82BZa992jURNvTPvw7MQ/lJ/blVl4ak/e9UefDnj480cD'
        b'V7yp7Mpuwi8ja8hu3DR2Rf4TWNttftBEttnZljysx8fpfXL7OOp5sZfLrVwsODHA5r1CmpLwaSpRSJF4Iofvz+8muL6tHkbO4KawWrkV0F9z2KKQQCnqER2JD4lq8KGR'
        b'zERCCuX3BeM2VaZDTTZMEBTBXcgdET5fncp0txNh07QCDb6Fr3eyXQshh5nyOgjo4mncFBs7HxIb6baQkWM8burSnRWvHYOfF9TIa8gVipiBzuXyBthLJwVHxo1ky3LY'
        b'UICYnoOhLeLGUUtowX2wYQK+w4ziLlIBRuV0RSeHBwiGIU3kFGnGZzVWZvzBfCDxOrxHMAxpwTeGMMMQcotso+nUMmQwOcUc6LvARt5NDUPIanLhCaV6QilzNCd7Af+c'
        b'chtqHAjpbM5hxIeZNYc4AG9xZ9oHnFsnc471SuZf2Bte91PrEXqeoWYsCEyIAh8Q5iMmXYJvhEexNVuKL9Y9qTflUOwkpjVNqhNuF4SukRsu9xHmO4L3GKj7iIRcZ5Ou'
        b'ggZbmPnIgtGe5iPkag9fHxP40cau7SK9QdDrLIGHS6+DVkVounNiLoI5pVMXc+pa5/7hIzivH4iTfRzab4jzisEg9kt1+b15BRfK0qkhNM0bTsvz4VwkvPOc7GFE97qQ'
        b'DnUN9MdTyW+larkf65zHC6U6lP/X4XGGd9nCrHH99H7Dl2F0p774P5NnakLhu1qoQeJWE3JMnfFMTnneR30K9KQ6Y7igznhhBmxW9PpMKdLlHAutQ4LukDlfiPBeDCxs'
        b'DEL9Uf9ovE+4Q6aVtCzErVTuL0W9UC+LmWVOjzckAnOyBZ9GCSiB3IxglQdngPyBvpkTDPLH2OBcxM76Pqyjkbs1Ip1O3rN8usDGvjpzBfcN/9ZYSZx+2bgYlUAXgyTk'
        b'aOLkRUli6qOLyqA7RwTuYyOIZ/sTxwxLklJeFxlX4rPCB2+qqUVB7VR6C+okXblQtbVLOAw/Lkteq5O/GVMtdOLOKhopSw2CyMxhXYWcLYNDUE/0elJAgS7ng7lpQs7I'
        b'BTRyLCcu0KmksyKEnN+pgoE3KAgMCtep/kPeTcjZkkIZhrEreIjUJziLr6mjXZrVk1foVN9rzEi4DHb1UnyvkDKT08lWHeW/JYuormBDb0G4PEIu4+uJcXHAUg5B/cgO'
        b'vI0cKmQNf7qM2t5FLQtEuvF/nhUmyDOwJpvJXcpAiIADpSezu/BVNoNT8Rk52ReEVpgRvgH/cdtkgW29ijeT7WSfFFkCEL4J/xNB8KULifcUdyetHAin0UiN1CPNrNk8'
        b'CbUy/GZU0Fidip9UgZhmK43sINug7R3QwYPkKNkBghl5DgERuImvsebn4wsVGCojZ4z/p7krgWvq2Po3NwEChEUEtagQUZBVENxARJBFkU0B0YoKgQSIhi0hLrggi/uK'
        b'Ra0gCghaN1xwxe11ppt97Wuttk/T9rW12u3ZutRWaxe/WW5CAgli2+/3feTH5N6be2fOnTt35pyZ8z9/ZiC6kTrYSOyLF2DlLLiOLr26wVXa1VfrUPJ4fQtskJHUivXp'
        b'ah5oK3OAF0LpzFUFMigrfSyYPo7MQmbhMnvSIs3BSTtwkGGWwUvMImZRH9BETi4EjePBQZYp64cXpYtAA1n8Jc9k+yB8NwsFduGZojNj0+jUs+eH+9FbM/Y97NdQ3Cq/'
        b'0pomUOHIoP9yaMmvTth5MREG2K8YN/8Dj4SyD0bFWt4+fbtf0dpdzMMhU7ynOFqmHV27Wcle10xs8tkIX7OUr7h+/cewxTm7xjlNOzDk/bQ+LrdiUr17145s3jal6PPA'
        b'qTv2zH4oarS7P+zqkzS7/6Q5+Tz+xblysiZ9qaDlmgsbmfbrzpG3Dk3d3nKc1za8LfafO9vTYuMj917lO894+2TAr1d/2ran0UVS4Hmp8s7jwRO/3DZ+4L3cqF+s//vG'
        b'bUGj+vLvLwtfS3s9bb/vJ/OGzF5h5/sgacCr0XMv7Fe8fcmjaNavT3ZL1vQe8igusnRlSmSMw6Xw9yJW1r4l1Fz6ti62KmhOdo5lUpRjxpj3Fpx55WT1mrwf3Wa5pP1j'
        b'8r8v/vLw3US7kqt3/vvZOKfScp+xvdP+fXOaourpPf6jH5fd/f1rr37E8RAr4v3wWrMHaOnWG+cohR7Zok6jkbgJJPr1hzXeeCA6yaLfK0EjXfquh+VhFIcD2kJ1ygU8'
        b'ZEfUmwHReODEw+tMcIDz/ZwKt5KhcjQ67SAeVROwLYqDP6cMx9j+CD5oBZtLafbVAA3/OJYWRuyv4TEe88yXsW7g+CCigAU5IuEN8ZqgEltlOg1sNjhMBFkE6jFVBTLi'
        b'i33wNEQrDzTAivlU1zjh6sR5r/DwNFM9cV9JA7VETLgDtoGVSM5zMi0XFJnc7DND0B8esCD6CKwcwGAliYtSANeAhmB8K+58cMh3PNGTkpzRUa2ja58irM30hq1EB4EX'
        b'Cmy0OgjWUpzwvIvO73SjJYVaXQB7wGGkNNiCnZMNgilYZhMZhgZHdWSSgHqTYx2KzBJ7citjwGqAHof/JN9hw3C4h53uk5GQcD8fx+yCB4kwIaBuKbrZVZOM+MqGLgUr'
        b'CRIuLSKKONNuHDo7zowRsDywK24iRcbuQg9gOxfAQJaq9RRAzaiCNsA9Y2xMeyUg1SiEeCXAteAYeTZCR3gGK6dIM/VfpNNN48EJopgVLwVbu+hl6AmA83KtXga2mZP6'
        b'ywcXxxONyj92FNylp1Id4+DEk3rl+nhj/AdoHaMNqATL5Vr/hh6tnAmwWx/Rq3IM9CqRUsATsSRcAtJ/sFbliD590Kcf+uB9W5Sy5J8l+pEDDa6APoLb5gMEt6wGClkr'
        b'nhXryBM+teJjTwkhi+FmSHOx7dBccPF6rm/dyNzhCXcKJT90VZIcjS2sdioK1Q1WSNBXNflKRFu1eKtvJ6gY8fZVluKEeAAT12DsFawRar1DtVt4/Yn6VBKMGPbZIk4c'
        b'ZEmfrAGT9UCNKGNKRHJEQkbqi1OiUzR8laxEI8ChBzTW3A8p0akpRAMkd0iVy78eHkOJ2et8cXWdwa2TseezvZ4XEmZrhv5tHM3thUIL+ozNifeLeaeP4D7bS8AF2LDS'
        b'C7AhNGefCCzYX4RC9rHQkn0ktGJ/FlqzPwlF7EOhDfuj0JZ9ILRj7wvt2XvCXuxdcweU2/fmP9h626Ly+5n1iyLTL6VTwvS9jswYe3COTeXPBFtzuixka1ltVOGdyXoF'
        b'NXaExNZO+y1ldVv8DRaWAukQpCxj4IZdjkBqIRXqiHstpVYEtiPiiHttyL4t2cfEvXZk357sCwmxrxUh9hVxxL29yb4j2bcixL5WhNhXxBH39iX7/ci+qEYgdcdySV/Y'
        b'ydaYY2DOXBup8wtMgy2GnnD7/bX7fdF/M28jT+rBQdotSDwp61V2q+xzLAn9L6HjRb9ZEnJdAYH8CGfa4/qQDtrAW0WNBNEqG2QiuEkHE+LdXtIBxCF7KEe8G5cY/WSb'
        b'Afo7VUsGi36irLtiT0yUgtmwJAVS/IrIO3N2Gux4p2IQOkeAhbYKs1SFCszdjbHzOLAxZR/FgZVlRSU0tjcB0neKN63EXqxeFhpLjskNUx5xm2SBWUhjrWLyI2nOfA1/'
        b'XgE6li+TytX56JiwCEm+oFApVXZQ/xrl3DWM3KUNn26JjCsrbtXYWhe5q6esu3le/C/u95h1F1f0n2bdfTbpbheCXaMxBP4k6a7eA9HJgQOwdyMF+tmUDAViiaIoT+Jn'
        b'TJRgcXYeKjKbhDnvngO4ewpgI3S/z1Ejz6QARm2RRoSOikkTKyRZmHQebeoH2fYa1il8NSWuMyqFoeikbj0D9arCiPCcIOh9eAYBsSmyYeNBJkwREPeQbNhoph0ExH+B'
        b'bFj7ztNqp3tiuZR7YEHPemDajoILA87tiZWyXLkK1TDqoFA/RpqTr1jNPTZ1AQ7H/ac4fe3ovEqYoBeedClyKssU1bBZlO5mZgY4AdfNyjfCvduh9xvQ+a4IF9nD9WEk'
        b'y8dOjownwyy8FpE5ILtXMI0hm7QYthgl89VlSGhttHmCDbY4291FItgMV9qSfG+5iUhA39YZmb4fsR6MOpQq8rHafDPQ2G2MJ5g4dXcIC86A1dagsVROcm2SEXRHePrg'
        b'TMU1szJGjd3Nlg0qNCpsrE8OOJKin9dyuMkSad6Hx5LMZrN4zohZeEuWqXiaYkVFHA42DNLmNgFuMOQK1ll8nUU8ZQ32vOBEchUOxbM46AH2z1TMnpPBEG+cIrjHUZsr'
        b'aBfp5+rJWTWTDbJsBwet4eocUCc/9uF7PNV6lMcx5yS/d87ZsBGi6KmL/5iz+pXlzp7lfYSjPnnN4ZJoKu+lM6JvakZ/VPXR2fdOzQj87pMb0sE+Hnaz3n7vYcj5FyMz'
        b'L39t9/HRz1emD74jjCvIdv0qrLT3FemIoSNer3ucML4i95HoyL2g82dzZ9xPUi87MOdmcsTZplnnFT+mqN6cueCez5Lxv4XF1wwbcnr89jujns750MuKGGaDwIXFyI45'
        b'CVq6mJjgZY5qWLXIyToCvNzVixxusSAuuxHwIrankwzallmwO+MKXxbAI9MzKMixed4cA1OV2KngEjiGbFV4AZ4ixhDY7whq/Hx9DEiF97tSc/kg2AgqsK0J9oFGnTU9'
        b'pZT8GgBWelPbEGwBZ7XWIaxZQozULB/QbGDyE4N/YD9k8sM9dnR2/BW4HF7qsFKpiVrkioxU29wS7OgGXgKHF1DV1Q+2wVMqMoOB9uKJIutnziSAKosMVFI9aANH/zbV'
        b'XwetxKEiOow7psx2gi0HrdTSCFtxZML6ezpSYaRyGCcV/gdOXsUJwAnEyWs4eR0nbzDMswl3hD3JxMbglrz4Wr/88o6P2NgceVfxn4dX1SpDpzWZxMtNQ7JQNGZHWXrc'
        b'wvhQN9zCzw3IFGXoqVAmhZqhFeqJSycJiELwpxl9OXXJZLnpunJdabl/jdOYK1iQgZQkk2XO0ZXZn5app0g9Z3k52vKQLmSyPImuPM8ObUnSGfX6/LzJOdpa1uonJiWQ'
        b'6iRwxpMbeirMnyZO1lk/psrMNSgT1bJO8dEr04ulwGkyWaJzt03M5uuJgj3Y8TtM/G0no4QsS+HAFCxns1qR+MeiHJHOn92sR/7smH7KzKHH9FMyzLrZU/YpcvLzkE/p'
        b'k011yRKTT+mwzd6+Ym99kDXaJ7htdJI+dQ5RaqkYmJGk54afrqAQcUphPjYfqK2NY8ZxSGlJVqG6hON0UiFF1VTd4D/MnyLDVSKV5xB2nRJOETe8Ka6+SSxMVG25XEQ8'
        b'Izow/ovVsUFJurPpho/Ss2TEnlrKGdM2jX69Un29y4sq9ozIUsqy8wow2w1n4JG4eEYF7WgHKpU8t4A0Bcop04XYTCWW69+VHNk6uSaIa7Q2zHDykEcF60wZXNJwL188'
        b'O6IlRsZn6JiRs01ZX6RVysn1mF8L192Y4J7zc+UY3hC+a7lM9fexa3liNinCg+Ul9vbOx/Y1up1F3t5/mm9L7Em4tfwoRdXzZN0Nt1aPrn9epiuxCYYuU0xXw3omhgEQ'
        b'pFu+K08d39VwL3H68EDTfFX6YBLuMapl9HbkBURQwmAflZDw4ov4zozFxsV/RZJF+SSyrkyJhylfQmanM4v1BArsXqBuSbgMJ0no2+KvfVOMikWVIX3qLlR8UIBpFjZ9'
        b'6I12ykjvNUFH0RtZoJJToQpzjJOaSeeilkHqA19AwgtLFuLtHvI54b8Ig0xUZLZMnp1XIiekXaoOSrmu76zJPP3EwzFFtkyNOlddBqgFy8VcFaEeKh+9cdHT/FIlJVky'
        b'PANpnGLMT4yaCw2CqlDnz5PlGa9/P3FQp9NIaRJ1Tqm6RIZGDhxmWpxWqFQRoUzkMSJEHKHOyZNlqfGrhy6IUJcU4vFtnokLRoaIYwuk8vly1JgVCnQBJb5TdbpzE1eP'
        b'Miby81fQaGPZyPXEyn8+scYYy+/56iWYVGRH1T+j5o0eTKUtGU8VdpL7uVui/u3nKNHdeOK61ckkySpV53qZbn76l4tHu5tugAYnDg82dSZqZgX+XTlF6Y8jO2czylQ2'
        b'o7rLBjUK3f11k8cY/dNM3lqwQWZG7svkgMZBA1EPx20RfQDppKhv1Xblnil0jDU5YHcgDzHFPRoK6R7ScTzj0K6sAP2jZi7GY9AY0zybHZhFw2wCO2UT2G02BN5oQLzo'
        b'SdgWo/B4M9LkZTo4JL00ehrpqfEBsSd6ybkmjh676WpQKzEBJRotIrktX7Gebhc9LVnsOR025ynRS4pkGWFaFD0kZkdmusOcUNqsVPPUSlVXobpT90ypl0SV7Lnmp1PR'
        b'Igxm/XumwxBsaYg4EX+J0wMDZvf8skB6WSC5zPTT0IJWORWS28emc3ftgCBa0SX4C53Y9TzTvdgkmVJZ4B+jlKhRohjmHyNH2p3pXoucbrqvwvmY7p9wAaY7qO5KRr1S'
        b'dB5SwlDfb7prIrIhnU1qXAxTlYe0WJmsBGsW+BspWKO61e+yCheGiPECMtKfcrDWig6gOjf9UPFFGCpMr5IoxHin2yuy5SX4hURpt+oexUfjM+kGydgX6+l+QcNHjUIt'
        b'zbRMGJqMBMJf3bbIHAm62xjUqXR3EgE3oyeEv8Tpo0yfyHVzWm7Zblq0FnYdIp6AtqgmnB44utvzda82ucRwVa/b+taCubkr6fMx3VljCDdS0SZEJKLHY7pHzJJnowxj'
        b'I1HRRt7ILgBsvHZvdGXt40yWEcxazmOYTN9HRW4MBfrUhJbqGCh5A8EpDioHjlKeLMlcASMcwJox4Zm+zgV2FMDnA5ot4zB6D7ZbUQAfjixE/WwFfRjfgERMczlg5tg+'
        b'FPyzFDSV6IP6qkKJN6sbWBFJEdLgTEEHQtopi+T0ZsYS3uMCaM4ESMbeXObCkCj5YAesT/ZB52KaxyTsSwgOTU6gEZKY8WXwGFiXzCwcYZkbA1cT5NBKhTYW0uFxH/ab'
        b'HN2LLlYVzxpqLBASzmYSXanQxkLykJL1xA1gh8gLvsLFzZLDvtPNVDfQVtjWOeqNryaCTPuq3J+ffpwcnn3+PrMztDTwC697qlOfWysCJlQ0j7Kv/ahyw2Xlt0HL70d8'
        b'+kHb6U/rC3PePGP9du9p8T97uqx3TbEZOnNuU7F5/9PJ7/hdf2vLF03v30rPGRN51Tr92/c/69vv2sj+irsjz+0dt0izZ2Oo387bgXnHRLWnf8uy2fP6tLwZVx+oP2m7'
        b'/uJHSX7q89VZL3qEfHv5uzcyfzmoGj8LPA1OUZX3Vdx1e/vh48QRE1KveJx8aPvT7ym2oQ3tA/MKt3378N30P44P/vTgwjc+/PT3u/+aXta2YMJnpy55CSlQpMYVnOOi'
        b'J4M98CIHFImHLTSW+8UkeJoyE8LjkylQZASsIyASHjgH1/jANUmx4NBMDwFjrmDd4H6whvIs7gYt8zFMBGyAJzqtmpWFkbUkuH8xrKVrSXAX3NLNehKoh6/EkxBM4Phs'
        b'2GIN6mCliRBM4GgadexsgvthgyGNIVyTwVAWwxdjSKiO/rnOcWD7yPhYHsMm87x7g/NdIR6ivynGOXaHIytYMfhFLtP/CJMw6AOH0xtCABw0Pg9xOiSrVyzPmXwLl7NP'
        b'WXaAbrtUpFuo0WE4uNAfHbPX2IVbb+nK8rnk9xLoZULyNER4zDW2fuW2xcj6lYGopiEeJLoT9kNiVgl00Z2eg3VJWYwyMOgy8W24duky3WmXWRUjYEShTpjJ1zcodByN'
        b'+gNrM4pV8LRQPXVkANwgYFCr4i0NgpUdCBBHcBCssUa7013gBWb6pBAKxj4Kt/ZNIddEhjE8eI6BJxxBNSlolGgpb8bie2aos1u8yKeYgzduhhfA3iAM1rCZiOEaad6k'
        b'O7XtDaqDMLhjyRgM7/CAh0gerpMtmNciXQjDcLC1PQVcnJ7Vi5k0IwqHdlB8n+BN/fh3J9ozq1Oi8UHfkwVL6JkNRTaM0GsEw0zJVKydJaNnisNFzDsJ9KD/WBt65veO'
        b'VkxDojfD2GeKQsQz6Jn7x1kzbwk88cH4Iwtc6MHQeRaMb0h/LFL8T/7c6AGa4Er4UsqUKVOYpdMYXhQDygfAFgqvqAnvFRQQEMDMFaEKamZgOURjBelolmN67pQpDMbo'
        b'7YWnwGH0Y6w5RYU05sIjKQPiCS6kAxTSCndTlMfOibCGA4W4gGMM2NIbtqpxmKrp08FZEhW/D9zBDMp3pyCZQ2A5OB+EqjcQLs9nAsFpWEGqXQYOT8QID8YPXAAbGL+s'
        b'4aQ5zHZSUiwH3GqWNVOL5DjoQn70AseTU6aI+ege4SYGtDmZg0Z4Fqwn459nqTcavzbDGsNYeuolFHGBq3pRjpCRmqM3KDNTcc1xLK3Vf+UKmebZg8lB6JpGG4sAns9C'
        b'dYrvt7J0BCPJAu0kh4nBjowiLAU34SW9k5U0LkAkXAn2p0wBDV7MEtjChCy1ho2gOoli2OtdwBGVTVCAAN1SO6rtgxicXgPWybeuVvJU7qgCsmQP8qvjMLBjZe7O5oQn'
        b'8TNrP3jgfecLge9Z3rz546McB7VIVtw6umazUpR+M29A85fNUb7ecR/9tvvOL1/fn+wuS1UePiW9/gF/3O81BzwOe/+xekF1VOrwhbEt+7ZOTRtR83Ny+9B336jMXfJY'
        b'OODK3P4Nj/auTX/449iqk//URKZ6XZ0orbdKqCqXiSI+mxs9wXxCzIQ3LG6e9XWyrhfW/7EHrpzs8prf97/tqr7l/7L6ycCgez+etx8ZmL1zxg+P993zn/rStuwrqWNe'
        b'b97//i9m+V97Scod44L3nRxamLWDV17/3+EVTg6H2k7KXvr8neOyvbOrVF/OWxP3Uepv7bGXL+14WDQocXu+3ZmQQKfpHw6o23tgw70T9Xe/uPgvMN7Vb3H10k/eGvZN'
        b'dZPCrnxCMTugwsuxBHNnw705ll0dIpzndB3CLoETFE6wAtbC5T6wCdQSjxJ0hhCeY0E1qHKlHiB1SaABaUDxPLDJnhEM4qGLz8Dj5Ld0sBK0x7FBBqECe/lTAMABWDlV'
        b'R8wC1sKzHFXCBR7BZYIWuAUs1/Ik+7DuepBZcbSZZY4VDSlaC3aCeuxk4sNHw2gr52QSzlAXlONpiRSxAVdNHcbFG4UvgcMUjbFeCPZwjjCwNVnfm4aB1URtcIgGGzlU'
        b'ScAijCvBqBJ4KYJ44yTPBas6uciAVbCcwjlClpEMcAyJc1QnAc2ggiolU+E5Grf8ZXB6UByBYswfp8Wd2oJK/gS4w5ZW/0vgSBZFgJYP1gdzwEo3Wo012b40hzhQxYFS'
        b'bZfyoxaC3RSV0iJL1/eRAZtBvRbKsZpD9rrCl8E26osTZwYPTqWuOOiRvEK1ri0qcCzO1cUwpiOqxXqKPj4Iq106+eosteHgOestCP4G7oY7UDep9TmCy+dr3Y44pyN0'
        b'nxtNeKo8I3QgoYMhusr8LrqKoEjA6SQinj0rJAO9PQdWxaAKewKrYAl3Mqv7dAAsCKziK/P+5retBiA9h6WAC3viiI+d9AWPhZbCRwIrjgeNKAxdGNaMy9+Ja42vZXMr'
        b'1/84bDfJuaZflgqrESbDDP9lwrU8pKmoO2sqxtnGLBLVBLyzsx+s9wFn4Qod4ZhRtjFQlU4GJgeLRTryMLgNVPEVPFARAptobIwK2DLNZwHYjCnEmIXgEFxOgwgBDCQ8'
        b'ytcxiGW7y/tJhvJU2Puh9sGr4xIuWIFwUaJy/6kPrWzDyuvq2g6OOROyuuFjm5via1bDFqz7evO7088sTlH5vTXx87gHv68+GxH1RdWnswL3veNqPfyK6M7lPvyLU9fO'
        b'GHJPPGCi5c3rW5aNbpozT1Bx/xvxNstTRfvfu3W5/6pjylvxblXzW9LrmVcB78ne2M/ar+6V5wjLnirvWf/UHnN9qts/yy9u2L47983ivTsOjJ/bx6ci4sz2ed+0+l/I'
        b'2VmiWVpwIGy87bVRY2pqvewo8/p6WCHg+MPgeYFgNA+0eowg3VlaHg6Zq2MPGz2LkIeNAvtIVzMZbEGW4TbQyhGEUXIwmYj0E7ahKXBdBLJv1vgaMINJwWnSFUXC2ng0'
        b'JODAVScWGHCPDeJc/cJDbOPc5vpi6FQHd9hEGe1nG5CWcQlcotGd/ZP8KHlY5hxSth/cAs/qhb0dAVYwJO5taDANKdsUNcgFmbOUPYxSh6HGc4r8GDQ+TUccpmQIdRgf'
        b'rHjRgvwo4MGXe8MjHHMYpQ1Do89GInDohLgO2rCZqYQ1LBlyYQMqs+dPASu1xGEca1gTaKe/bvWGFztIw9DZZGiyL6DxCJoU8Ogk0ELF4jjDnEHj38IZRoitSHcW0KU7'
        b'Y8rc/HpEG4Y7Bx1tmHIB0z3Ea6FB2a7omGpIl66IKe/zsUmaMG15qK8zxHHQXS64N95O9HLoDPlaxDD6uK9/MM90S2xnSCzvElm+igK3OjGC9fpLVnAPntFFlAzCXfYM'
        b'hlKA2ZuLCGFXn6es158jABMJ8MAieCp4KuY7LBCOdeYRdDbSh6rgOVWsr38pp7KZMTbOLBq8d4EdXrxE+dQnyQJVX6QGu/uNjd44tqAyHKnBfY++er1fgF32nc/5zfd6'
        b'fXCb8VKWZ4zYljwkdeon0mpz5XfvZNXk1dUX/vHmb4fC/CPDBDERs+s3Tfx1VeuknNzaul9F/z7eWJ7rMXtiWXt0zIxtgqeXA6/Mrn8Ut0+847Pvtv6Hjf7Z5uvEbFlN'
        b'y4K7/e5VRG5c+M/h+85/ud46rPjqSuGxH36/stjjxlCg+rn43zPt+kdd2PTWN/0vf9U47bpbH4ey6uKYkW2C/UdLskZcmxBb6uh/Y/uJd69te2dp8N2zN/muN75MqZOs'
        b'ij+/40rMp44PJLPff6X41hSldc3SgPYt+9y/fvrVzrj5rw/M2jT5k61X9gT9pInJ/SE+J3/Q3I+9bMNOW9q+8npK0gbnhxMinlqzaunwd7714pPJE6VFMVw3qAhpd7wx'
        b'OF7fFoqFBZuXzrIGu9O6OkuD/XATYY5ZBtD4Y+2N9ZpYY3M4sC2k6zxM//+dFvjcCep3+LrX0FhC0KjCjAxFoUSakUH6nWG4A3Jm2RE8MZ7eeWrO4ukdsbOzo6O343h2'
        b'aAiPTAOF2vI9rJkydv4YnvK67tXja9iMDL0ZHOf/B3XAU97QvblYUtz1kPDD4d8Y4Scj0y9oZDgA1oFNUXloBFiTFA/WgE0WjO0L/IGwAtTL3cav4Ks2oROfhM4ZuCbY'
        b'FgQ4mj199IN9+CTF2vCsYIfpR5NvDJR9EF36W3pVncOsd9d7FDfFD7YZ8WP60kW3ynPrr91c6/X7kV4Zcnffazec/FN3X26MOua++mC+KiWtabLPrI9vq2+slrDljQ29'
        b'JO83rFgB+4y9U/yPXkN3Xnn1ywqfvhq24MyX5bmfue8GjlFlD9fdfMgXFnn+rLBGGgRu1WKwFe7DAzGsEyXheen1cRaMNTjOojF2r4qaPmthO2jG4XiOoftLSgLHY/xw'
        b'PKDzfNCo8CeTkpbgHLyAKwFUI9sEK+vYWkS14MB3AReReUimT1YEgtNxsQneCfbzLRhzAStERtgmGsroVCQaxNf5p8Kt5gwvhYF75rLkhzKPJT6T4XpwxIzhxWEigGqw'
        b'jpJ1noYtDnGxckxvh4rD2GtrLxZuBnuQNUaMnQ1upapYWB7YcYJVLAuOwrMhxFKxC4NtcbER4DC2b6mxZAvX8hMHLqGm6jp3UBfHBfqDjeAcDvZ3WkqsGA+wA7RgFRRU'
        b'gVbfSZyGJerNwhOgDuyivcWRJRhkDteGo1OKuFOsQBsLTpTCfcTQAevnYzsHHheB1QuK1bCtWFSs5jGwAa7uCzfxcQRVcIFadg2lqji4rhBsg+t98B0z6BHVsqj6yi0J'
        b'Zh22gGOol0cPwD8O9Tgb8aww3rMogG1M/yECUIke4lqD2MgD/+/fts4vn+UzOiAj/VEHfgJXg9DGShf0H9tuIl4Yv7NaJBhCFQjSBblq+ApZgUaA/XU1ZiXqIoVMI1DI'
        b'VSUaAbaWNILCIvQzX1Wi1JgRnniNIKuwUKHhywtKNGY5qCdEX0q8vI/5QorUJRp+dp5Swy9USjXmOXJFiQzt5EuKNPxSeZHGTKLKlss1/DzZQnQKyt5KrtLCRDXmReos'
        b'hTxbY0FRtCqNtSpPnlOSIVMqC5UamyKJUiXLkKsKsQeixkZdkJ0nkRfIpBmyhdkay4wMlQxJn5GhMacee3ph7Vn6tH/C2/dxcgcnN3HyBU4wmZvyPzj5Fie3cPI9Tr7C'
        b'CWYvVd7FiQYnn+LkO5z8gJPPcPINTjATnPIeTm7j5AFOPsfJJzj5GCcPcfIzTv5r8PistH1s1OOufSw544kwBzvnZucN09hnZHDb3Dj0xJnbFxdJsudJcmUcIlkilUkT'
        b'vYREZcSsshKFgmOVJUqlxgrVu7JEhWm6NeaKwmyJQqURJWM/wXxZNK5z5WNt7XXyttcIQ/MLpWqFLAzP9pMQBwJGYCFkOzc1x9EsaYr/A3s7A6g='
    ))))
