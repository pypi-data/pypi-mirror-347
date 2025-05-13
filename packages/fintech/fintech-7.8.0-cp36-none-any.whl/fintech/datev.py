
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
        b'eJzsvQdYW0e6MDznqCBAFGMbG1e5I0CiN4MLrghRDW64gEBHIFsIrOKCu7FNBxewsbHj3nDHvW9msned3WySu9mbTUiym+wmmzjxJrnZbG6Su9n9ZuZIQjIScfbZ53++'
        b'/3k+yxxpennfedu8M+dPwOkfi/+m4z9zKn5oQSEoA4WMltGy20EhywlWCLWCGqZyrFbIiWrASrFZuYTlxFpRDbON4bw4toZhgFacD7x1cq/vN/rMSiuYvUBWUam1GjhZ'
        b'pU5mKedkuess5ZVG2Ry90cKVlsuqNKUrNWWc0senoFxvtufVcjq9kTPLdFZjqUVfaTTLNEatrNSgMZs5s4+lUlZq4jQWTsY3oNVYNDJubWm5xljGyXR6A2dW+pSOsA1p'
        b'NP4bif98ybC0+FELaplatlZQK6wV1YprvWoltd61PrW+tdJav1r/2oDawNoBtUG1A2sH1Q6uDa4dUju0NqR2WO3w2hG6kXQqJBtH1oEasHFUtXjDyBqQDzaMqgEM2DRy'
        b'06hFeNLw8MvkguxS5zkdhv8Gkg4I6bzmA7lvtkGCf3+xkAVC8GUGC4ojfjUqAlgnkK5q4A7UiOpzMvNQHWrOkaNm1fxchRhMQlfgC7OF6BHaFyRnrGSIMnh6llmVhVpQ'
        b'UxZqQicCGeCjYuEVVAc75aw1GGeBN+GNJWpVhEoEhLBrvJCBR9CWRdbhJOkIuo9O47RpI1UKVI/rEAF/1CDIjlPiwqT+TbPhKdiIGiKqcI+aVLA7VAR84DUWXq8UWceR'
        b'Ki6ih/AuztIt1cBWWLdmlRVdWyVdZWXAENQqgE3DJuGukmGNg2e8YSNsRXvQ1Ui1Ioz0GbWSGC8wfLwQ1qCr6FApY5s2Af4bbp+2YgI3Hmrgp8FNN9wGM6YOo+xGFsOM'
        b'oTBjKcyYTawNZjpnmJHGR/SB2SgeZgqrF5CCowsDZMXSx+kTAY1cWy7AgEya7QeKDa8PiOAjf18hAYGgyl9cXJz5ZaGVj7whEQEJuFLITC82nJ01Fxh8cGRwydDM696f'
        b'4Gn6YNJX7M1o9cr/BAZvnHAk7QBzxQtMf2F2ccy7MSvLB/HR9SVfBbQFMKHtS95n/jG0bNm7oAdYlQQcXd4iDKnGyLzQUNQQma5ADfBcQSjchloyslBrhFKlyMhigDHA'
        b'e0oubHSZbV/7gKfzs+26QgCZa52vYzbZfmez/NkVIOozm9JsE0mwDsYPP9SSnj9PsYAF8N5CVgDQYXQ71DoAp4wdrsxnCe50o9NgHDomtpJa0LUhmfnzcO6DqBmUg9nw'
        b'zAjrIBJ/BV3j0F48mkjYDHeDSHRuHE2YhO6gF9BePFwF7ITngCIcPaKLw7AQ3svPykPNIoAuoLPsemYEOrvJOgknLYCH1xKkD1djPK3PzAuF5yLS6TpUonNoL9wlwrO6'
        b'S0+rQVfhAbwOrokBSIXn0QOQivbBLn1qpq/QfASnNx3pXvbamCAYFbjjg/eyeiY+bnhh2zjZ7iSh+F3/42dXhwWeG1P3iylJkpo/546Xdby/+s/vbF4d7Lf0w86URxN/'
        b'+cZB/9YHr8SZi0/tHb7/l1VbF8RdPytAc0MSw7auX3AiIWPujoUvD55aFZHiOzkjZoPiv9rfzGsYmb2pdm574j+qt3739WuWUx8uvv7dE+1vNbsbW8YWrS1fc/Lhre86'
        b'Fd99NjzImmzaN1ousowiyHMAnk1T45HcQ83hqDlLkUGIRhC6LUC1U0otZEVEoTujwjEZ2pOhQHWqzGwR8IVXWQyvi7DNQtZr8LSx4Up5RriNmgSgLagb3RNUwp05FkKH'
        b'MS1L8t0EL5DJtGIi0BDJggHorgDTkZoiWgPaiQ5vwBPfgFpRkwDAbVphMgOvYvDclbM9bKjcRLBV7ku/fvrjHPg+OFVnqqzmjJhZUDakxCyEWz21x8/EGbWcqcjElVaa'
        b'tAQ7zTKCwFMlTBAjYXzwJxj/+eMP+Q7C34HsIMYkJnUTxJYLesR84R6voiKT1VhU1ONbVFRq4DRGa1VR0b/caTlj8iK/yTKizU0jnfMnnUMyVsywjJg+rWNJzJ50+Cg8'
        b'AzWrVQrYEInXfUtkBgMmEEBdERWhHYMcS5P8E9q+zeX4wRGGj5m9likU4D+hHhSK8LdYBwq9tH61QMdoBVrhdu9CCf0t0oq3Swq96W8vrQT/9uH5q06g9db64LAvDmNK'
        b'gsO+WikOS7UMpbb+PeJ5dKayn/wDL8tSga0XZIQ+dmIRBez8GpfnKY+gToApjxBTHgGlPEJKeQSbhO7oOGsjba6UR8jT8dcKhECiPYElnmLDF+xwoK/KaBeZs8nKl8PP'
        b'il8p+aR4j7ZO82lxU9kF7hMc/mXJJU25LlMzqOwsJ/zv/KErhi7ZumJLWEdM2ni118zdvrk7b2jPCM627B6zY0zH1lgBWKIP+F1ej1zMI37bWnQxHPO9ELzAKOsLF4MA'
        b'eFpQDa/MoDngfdgOa8IdrFGAWmArkEYIvOCxcLo09D6wVY0aM1EzPAgbVHIxkMAGdi08AZstRMaA19ELOkKz1Cp4EaCt6CwQJ7EhsDPQMhQnq9ABtAM25mBZQDgfZxCh'
        b'Qwy6G5xFy6IjcEtFuCJdtQCdJMtegq6zcDu8AtvkrBMiCp5FT6EdL3skRUV6o95SVERXjpQAoDCQIR8xI2SqA3h4K+25+BUj6hGaOYOuR0jEuB6v1ZzJjCU+EwGQyZvH'
        b'fFu7BNtNfuQR4FgKpJEljqVwJtBpKfRpr5R1QngHiiltKKZjbQjGUtYmwAjGUgQTUARjNwncCXfAA4JZw8iMts8N9EXNGB4tmCGj1vx0CjpVXi5lddPQMQlqEg+AzYv0'
        b'r75pYmhXJtRVflZMkO2xLjIoXJOpeVocWFquM5QIG6K56DXg7Rd/7iU9FAIO/bdkEvpILqSgM6KD6AyPFzacSN2MseIkfGQhIpocdaLT6BqmyK2oVamoUqC9Up7wDtsk'
        b'xKLmdthlCcH5GMzBmm3oQXBjMbyK0QNd8bZQ3noCHkhR5ygYwK42o3omzQI7eBCybrEB070yzqK3cBU2hCBkC5T4MFKmOsgBGkcWviohBXCP0Kip4PriAGsa4MABCv5A'
        b'/Ch1gP+IvzP43bTxbyMy5c+FAxFk1m6sQvt94c2J/eIBRoLLsENfnzpNZI7Bpa4uL3fFguRMOx48LWYbYqxRb0WdjBLGVt0E4GKtZMOsVLmAX8SX0aMQNTqPObgTNrBr'
        b'K6ZbCGeABybCemdMwGgwJsiBCA9hDV9LQwYmPTZEwPyXpxNYcDpj43KeaQCGurkv1MuegbrZFeoiHqQEuD2i1RqD1Q3sBU6wH+hAgCD8KHcgwMFA9wjgaM49CYjhEYDI'
        b'u4xO+JxkwAUFGFuVriggyrYS3MLKWEs50b8KUJ1CocxLz5iP6nJQO+zK50XKdCxdKhlgQQ+8xdNQA6UdsH0IvO+BeCzwd6AN2jNY/+XgH4A5B5f5IuLkZ8WfYrwx6MKC'
        b'wzTpGoOuudxQciH30+IqTV17F3dW80nxqyWv6CL3hGoyNF2awFLw8pCM7TUvHbi2aPKWDXN2DtpZLH7VAtZNC5zy3SG7UPgA1uT6ko4ORNtcJTZ4ppDiixle9OPJDzqt'
        b'd+Ac6kK3LET9Xu8vsOOcYoAN6+w4B2+pLUSAnlu2yYZws4GNL8GGUsr0RsDb6DJhTLABtvZyJnQZ7rQjh9Ct4NSLlWJrFRHxevmSwccmzwUy1X42POHzONMhnuX0ouKz'
        b'eI8JUi9TovhICGWFAx/bg5zx0bUdF9XLlRZRNddBi5g65vkVV6FbRBRk60u8dgiobHMvYYdak172FKPJL0vKdYM0Z7mzr7PdIdc6DoYsHVrClXSsCFl5YHr34lfim37d'
        b'dOOV+Mx46ZiS+FcSpDtiPpCObIqfvuxF6SEFiI8NeD/jHGZAhHOgrhCxC/+B+9eza4egLp6cdGIIHvPCDKSXt2D4TkX7qVSyEh0OQ+dXosYIFWrG2pV4OTsOi0jNfM3N'
        b'6NZktHWpQ6ihAk0h2uce5v2RJiyRmy0mG1kiMw4sgcwgTJgwafLvpRUki53M+f0I/Bkn0BM91uoAfbMLKXqmejmbbSLattyPyEyE12E9waeoiDd/4d/SoqJVVo2BT+Hp'
        b'oqQUI01ZpWldj8QmI5mpHNQj1uk5g9ZMRSHKEClRpJhI+2QnsR71C8cMmcik5JMhkMISVsjYPqy/RCqSigIlVNcdKUEXfFVSu1ohkbLF8ExqH3ZI/lGRxkWlYAuFRBHQ'
        b'eh1iC0VtQCtZIdZ61zA1DFYvfChZ9esRzzZier3u+0GzuBK9pRIrZZFqE6flfz4hQ3xC+vx90ALOVG0tM1dprObSco2Bk8U+IeP4XprJWaotnGyOSW+2yFmqYDz5Dwz3'
        b'vx3Ac6OuNFoqU7Lx3MpC07QmzmzGM2u0rKuSzcfaoMnIlVdwRnmKU8BcxpXhp0Vj1LotZ9RY0H2TQSnLxZCpxGUXVJqMz5PPXWUrOb2Rk6UZyzQlnDzFJS1FbTVVl3DV'
        b'nL603Gg1lqXMnq/IJJ3C3/PzLQqVNtukTEkz4sniUgowyzNEpq3UaJWyuSaNFlfFGcyEERpou0bz6koTrrna3obJkpJvMWnQES4lt9Js0WlKy+kPA6e3VGvKDSk5OAdt'
        b'Ds+7GX9XW52K2wMla0jviB4ts3UERyllhVYzbtjg1HlZtMeUmBQ1ZzRWK2XqShOuu6oS12as1tB2OFt7nGwuum+w6MtkqyuNfeJK9OaUAs7A6XDaDA7LkitJvaG2KLk9'
        b'TTaXw5iDTuosZjJKMqV9c8vmZspTZiuyNHqDcyofI09R8XhicU6zx8lT5mjWOifgoDwlH69d3EnOOcEeJ0+ZoTGutE85niMSdJ01ErOS4LAi21qBK8BRmegkMVysJLPG'
        b'Tz+OVM1IyyZpHGfSYQqBf+YvVM0pUMysxLCxTT5dC3pjOcY1Uo9t2tM11iqLgrSDSU2J0tam7bfLvLuLJ3PvMoiYPoOI6TuIGHeDiOEHEdM7iBjnQcS4GUSMp0HEOHU2'
        b'xsMgYjwPIrbPIGL7DiLW3SBi+UHE9g4i1nkQsW4GEetpELFOnY31MIhYz4OI6zOIuL6DiHM3iDh+EHG9g4hzHkScm0HEeRpEnFNn4zwMIs7zIOL7DCK+7yDi3Q0inh9E'
        b'fO8g4p0HEe9mEPGeBhHv1Nl4D4OIdxlE70LE68mk53Qanj7ONVnREV2lqQITZrWVkDojHQOmxhzWhOyBKhMmyJj6Gc1VJq60vArTayOOx7TYYuIsJAdOL+E0phI8UTg4'
        b'S0/kBE7Bs7s0q5kwlGosK6QsRCfLTXjezGbaAKF6PH816Cv0Flmoje3KUwrxdJN8JTjRWEbyzUEnDQZ9GeZRFpneKCvQYL7oVCCfwoCk5FIDq3NlvSxcUYh7gQlGKCnu'
        b'kmArj5Mm9C0Q47lAjNsCsbIZJqsFJ/ctR9PjPFcY57bCeM8F4mmBLA3Pl+mcY6kESyc0zsKttTh+YErk+BnrnNXsyMYDYgaH2XGZU8SElEK9EUODwJ+2Q5KqcRRhvZhK'
        b'uwRjXIOY/GjMFsztTHqdhWCNTlOO+48zGbUa3BljCUZbB8QtJnSyDCORyqjVr1bK5vD8wzkU4xKKdQnFuYTiXUIJLqFEl1CSSyjZtfUo16Brb6JduxPt2p9o1w5Fx7sR'
        b'U2Sh82yzarYJGvJewchdok1WcpdkF588pTlImZv0HPetEbnLXbyLKOZ5DP2ke5LOfkrmGM8tu8hpz5MNk0p32VxYQEIfFpDQlwUkuGMBCTwLSOilxgnOLCDBDQtI8MQC'
        b'EpxIfYIHFpDgmY8l9hlEYt9BJLobRCI/iMTeQSQ6DyLRzSASPQ0i0amziR4Gkeh5EEl9BpHUdxBJ7gaRxA8iqXcQSc6DSHIziCRPg0hy6mySh0EkeR5Ecp9BJPcdRLK7'
        b'QSTzg0juHUSy8yCS3Qwi2dMgkp06m+xhEMmeB4EJZB9dIcqNshDlVluIsqkLUU5iSpSLwhDlTmOI8qgyRDnrBlGelIYol/HYujjHxFVozeswlanAdNtcaViNJYmU/Nm5'
        b'aQrKrSxmE6fDTNBIeJ7b6Bj30bHuo+PcR8e7j05wH53oPjrJfXSyh+FEEYK+0ojuV+ksnFmWk5uTbxPgCDM3V3FYH+aFyV5m7hRrZ99OUXO5EnSfcPpnxIYyPt4mNdhD'
        b'MS6h2JRcm2nFqXAfo0t036iYvlFYzTEQpVhjIXKpLN+Kq9NUcJiNaixWMxFr+dHIKjRGK2YvsjKOR1PMDt2ZAeRORfSEueu1tNiPZnZTvxum5L7uvhmpial3dmRY+JbZ'
        b'RF46lTqSbptk/neM02+iE/Zaqr5nUrLlrImYzE0y3rw8hvwmOzdyiYnY3kxDyINYTfntEGIiNREba4/IXGXQW0zDHRY/5lnrHnHf2Gg3UFLrnoBlJCzLCqOtpEa0N0hn'
        b'XpROXD/qI+A5IZAksJumwq3/JstemdyvxyettLTSarRgbaLHfwZGAV4L0VRxhifEVvmEODl8P2wWRokKLGcQk6mM14IwQusxGXpC7LA9QiINudj17uP4+RW8jFNZbuRk'
        b'+ZUGQ2Q6JlJGhbqamFx6g71kL2WhulDGFyOmNUJQzXqzlY8gac5hfhnOJZZAXuTnG5oxX5FfWm5A9zE6GLCY4hxMmcEZuDItGQ3/02aH6f0dY1OZUuyTQVUAIiNyttVu'
        b'1+NkvJxk0wZ77VY2PZBK70QDxJnxerNQTcFWA23OoMcZ6C+9UVcpU8jSTBZ7V2wxKiMp+UwkyRbjLltMn2yx7rLF9skW5y5bXJ9s8e6yxffJluAuW0KfbInusiX2yZbk'
        b'LhsWO3LyC6JxhJoHDBF/ORoZ0ycSB2RZHCahduOszKqU9RpncSSP0HZrqVJGRHi7Is5bYXvBKMsMz0yZYzWupG6wnKkM06xqQmdI/Iz5srhknvPq7FmIldhdvA1v+CQ3'
        b'FaYUUg2BDNxUoSGJDhRxl+JAFU/FYvor5j6RR6F+irlP5FGqn2LuE3kU66eY+0Qe5fop5j6RR8F+irlP5FGyn2LuE0mx5P6KuU+k4I7qF97uU2nB/hHFM6ZE94sqHlJp'
        b'wX6RxUMqLdgvunhIpQX7RRgPqbRgvyjjIZUW7BdpPKTSgv2ijYdUWrBfxPGQSld8v5iDU/Mt6H7pSsy61mDma6Gy6hpOb+ZS5mA+30v9MDnUGA0aYm40r9CUm3CtZRzO'
        b'YeSInNRrf7RxTkLw0qw6YilzEDk7L8VJhPL2MmRZaJqxmpeRyRYfJsZZegtmjZwWCyEayzPJz9DhvoV7KfmzaSYDumm2iQkuKel0w0dnwVKJQ9OinERBhR63aoFtpDZu'
        b'jlk/5jREqtZRebqCMHgLp8fTYnGYjlVY+LXodfqVGmfqX0g1Q4dJ2VnM4PVJp61FZzFpDscrG5y+hCRlYqiRvTIzL9l4ltaczcW437hljcFasZIrt9u2KRMkTNI0Ect1'
        b'RPgNJ5JqBC/8Kshv5XMIvybirt2f6BuKH/fdir4hViJpb0b30DFzZjZqiYT3eO/netSk9gKDS4RSPdzpIgIPtIvAKxhXEbhN3Obb5quNaxvYNlAbr03QBjZ7aRNrRbV+'
        b'tQN1Au1A7aDtWCAuFHIi7WBt8HagHaId2swWinE4hIaH0bAXDg+n4RE0LMHhkTQ8ioa9cXg0Dcto2AeHx9DwWBr2xeFxNDyehqWkBzpWO0E7cbuk0I/2cuAzH2/tpGYf'
        b'bVIta+utUBuqldPe+vOjavNpY3QszulFn/ZSYc3e2mTqPCei5zACcVkvbbg2gpYN0E7GaaJaCT2lEUTTFFrldu/CQBw7APcpUhuF+zQAtzFQG91sP3PgXxugE2ljtLHb'
        b'JbiWIG0QVh+2y1N6JLOIn/bM/AXfR/rInP7Zo2U84eFPCrnk4JUqok09oc7aBM2eEMeOXh3iCXHIeUKcQ55Q7CHY94R4RDwhrhpPiHuF3KvHR6NdjWmWqUiv7fEuxZTD'
        b'aCE//TW8YlNkwKKfpbxHUmrFi8pYuq5HQpxP9RqDzVvDV6fH0l5RBV7Q5T2C2fPnZZdKbPjkA5wcgaaCZ04qedeKa31qvXQ+NrcgSZ2kBmz0rhZvkFC3IG/qFiTZ5L0I'
        b'aAXUkUL4N3IQwmUayD8V3x99NWemJ7Ick6enHg6lnLJPkT4Rk7HWoamQ9c7FZNtZLExZiF3IdtjLNikao6VPDeRf6AxMECx2ciRXytJIeUw6SmXUCVBmrZJhApoo0+rL'
        b'9BZz337ZuuEAg/te8Mnue+DY/fiRPsT/WB9c4T9Zlkm/SRfmRmbaU20dM7vvC2E3hNBjNqGUFZRj0o/RmZOZrSUGTluGx/NctfCuJbyOimuSaXAVOMz3X2aoxGzIpJSp'
        b'LLIKK9ZUSji3tWhsgy/hLGs4svsrC9VyOo3VYJHTo3hJnmFhw/vJspm2X7JSYj4MdWw6Opkd5Z5qsa+ZyXZsNTuASU7+VZpkobwLy0p031SN9W5PFdlcpSZTJYsIJLga'
        b'HkdspCKUK1PK4qOjImSJ0VEeq3FatJNlc0hARgOkOp3eiFcN7qNsHafBHQszcmvIDujqBGWcMjpM3neqfsRzWMofTzAtGAAwb0qv3Fhs+CLHCqyEJORj5tS5WYMas+CF'
        b'XFSnQs3qSFSPf+Xkp2fKUWNEtgI2oNbMvHR4MT07K0uVxQC0Gx6VVmKG1k7r/d14P4B5aO6C5cXSr6UGYCVnPWGrPti10hNJ9npRC6rPxCwR1j9b8fZ1UrDAQmstNHqD'
        b'QFzr3yqLM4co/AE9QaWIWex8gCod7UMdSkUYOZkCLwlBwlKxGadfp+fAaC0vMWKACW1gdlhxZqZfNbCSYy7wSDbc12fEe4aSzqE6XHVjBOlgk3yBU9/gHZMvOTOGDun9'
        b'bnUIzGtxRZp/BI185R3vLVHSHR+cvnX97s69spDb2wSS33hdjBybXZwWc/PMsSrJhmntEfeHjYlQtY3/7Zc+h//xwqglhhP7X5pxuGu+9fWQT+cv+9uvj0pCb4vXJr33'
        b'4MUT1be/gfErUE/Uwe3TpsYt7jSqUhNG/zDK8ouS4L3/M7rCLA9KuSSX8sc7sIwxFjb2Hn0UwDPDQMAEgS4aHrcQMWQVfIC2wsYcZ0hiSDBgGKoRVstK+WpODsvwxTMq'
        b'z7I74w4G02CtUALv4WoIi8tEV2fgWlzgxoBg+BB2jxH6oob1FmJrW4za1oQrQtMVLBDDg8PhHVZRPJ52A50rR3dxBQRUcAs8ZgNXELwkwOCqnUq9NmFtProdrpSjBiyt'
        b'ieEF2IlOs7G+o2kNU+E2crKTHOCi0ClD7QRAYhC0WgAfRFZZ6PGIDnQIHiPDJXIX7ehMdBO12kBMzprtECvxqO5axpPsD9CxODKsRnhwekSYkgwLNaPWcJJVZhb5wbOL'
        b'6QRJ01aRbNSMOX4mngMFbhfuF6AdG2E3nSC4i0t0apfKeuHjvMAweFuIe701hhcjff6Fw1q9MicRGKirKek82Aw2iBkxE8hIbE9yjExCj5JJWJIiZqoH2Fmx48hKtr0j'
        b'1M2UEAATWRGm6eSRRh4zgP08zEzQv6+qhC/VW0maoxStxM3Jmiek+8TfEmwBB0Y5O7T27arDn5mx/VFHUtKfDWAF7zDPZMuZHt+iXqnB7j8rdJm5HkmqQVNRotVMHYDr'
        b'MZM6ndqzp31vo+O22uw8PxTzB62i0mhYJ8eNCbSVpT/asTK+Yz5FDjnCfb9Mc/FjkL1L34/m2+cLuWn+eSckoMhVduin8SGOxuX9yhc/qRvb+W54F9lZdz8dGOboQMgM'
        b'jZlzcPt/rUE7l++nwZGOBsd5lAR+QtM2UEuKbHJBPy3Lelv2KDv8hJZ1fMvSIidRop/Wx/VC+kfEDTd9cDlRQM+3sbXAcb7tx84TPMfZJkG2/m+rpgjp4djPx33BH1Uq'
        b'1zXseQr+s+nXTX+UvkiOqE09IXznu0o5S0+RxKZgMYRQZW+0gxBmZ7JsjabH1GCHZsSzVJnSZNQ9ipDlRrStv/NmXkVkATmfOtqMP5OqA51IFc3gwbmf9eDXvwA/JhJw'
        b'ELd6TAi3gHddzpn1qV/u0+NlW5C8677YbDFxnKVHUlVpthBpuEdYqres6/Hi86zrEa/WUC3StxTL5JUVvHYpsGjKekSVGNVNpb42UJBe+dvBMYdA1tehJPo5juv781cj'
        b'6PxtEPetk2KISzHEfSnEpRTivpukNlVRh1XF90RuVMU0rdaMdQEi0Gq5ErLY8P9Sm++bjKNe+s+hLVJdhioiGlm5tYxz0s/wjJj1WL+R8YcYiKpl5ixKWQ5G6D71kFVf'
        b'QfZX9BVVlSaiVtqLlWqMWFchRbGeY+JKLYZ1spJ1pECfSjSrNXqDhjRJRXviOWlWkpHqiaUMLytblTb1iNTZpw5ctdWsN5bRHjmqkYVRYIU9x4zMsY22nBgr+va9T/5Q'
        b'i8ZUhtvQ2gkQKS8jtj8zUTXMq6xkdktMmtKVnMUsn/z8GjyPp5NlaS4cRLaE7nYu81SMtDxZRk8vLPnRMwwea+GXxWRZPv2WLbF51HnMb18+k2XEcolBRTXLJc4edR7L'
        b'kgWHdVL8lC3JMVk85+OXJM7K/6BtRMhU+TmK2OiEBNkSYq30WJpfx1jbTCtQqGbJlti2AJeFL3E+oeG58d7lT/RnPiAjFTn7BXssjgkGnsxyvDTwcjWXmvRVFhvbInhK'
        b'zlfTtZVmMFdi/OW0blV/jE4kN2EzBnqZDgW2UjaL1//pEh2bb9FUVJBTbMaxHi0BdDFgxMIdqLItLa2eXuejwdO6Ro/ZGbcWQ9y24PrWQ/5lV1o4fpnQxc9Zyiu1mJKU'
        b'WbHyT/qiWYkXIF40HJ6dUk5Wifm623r4IZFFQw0bZn6YerNTl5SyOZio2QmS21qclx0xg2BUJ5cVlRrwgPl7isyc+5LFtquKKktpz/nNkdRyi6XKPDkycs2aNfwVFEot'
        b'F6k1Gri1lRWRvGAZqamqitRj4K9VllsqDOMi7VVERkdFxcbEREfOik6Kio6Li4pLio2LjopPjE2eWlzUj9HB/Z0IQdlWYiLNZvLMmfIMrEcrlNnkPF44PIf1u/H5onLY'
        b'jO5aiTIAtyngvlgAhueBaBA9uZpq7kPDhEACtkwSTS/ObCibD6wpOHIC3I7q1HaGnofqyKUiGYp5ufPgLnRVsWBeKDkVuhAr8fgL83q4B172Ru2oBnVb6ZUJ1+FhtA1d'
        b'w5psq5lqel5AhA6wUnQWdtE7hTaswVr1NSW56oKclR0Ba3AT5OYSFoyGp4ToLmpDx6gVAT3IgUfQNaw4Z81Hu6rwIJ1GmIvqsnG5JvX8KqKxoh3qnMwM1C4EqAFu80Un'
        b'l861kn0Gog3X+MIb0Uo8RffhER/gncGiI+iqhSar0H30EF1T4SpuwWY1AwRwPwO3xMB6K9EB4cGV6JYvqotUonrS252wKwKey8C56xggmysSojYdf2HTXbhtAboWGcYA'
        b'Nh3XeJJJSIb76DQ3jyN3D71f6SUrln4NZgF6RxM8ALfBq2a/oXie2tEN3D5uW7KUnatB261E311cgl4w+6F2Pz8l2q0ZiW5koqvhaI8ADFkngBe80GU628tgFzrkqyTd'
        b'b85SRagGTUHNAjAY3REGbA7Tv91pEZkP4mwDZk1XvDrFH0ZJRcUp0yremHhl691VgRMv/WxwxNbfiGY3/WXG9g/zo1blLh/f9sHei2dSw/WXx+THD784PnXv6zFtezsS'
        b'DqsetPxycIA8eP3JX3X8vP1Xb9TlT839aEj4uCe7LVdqRj79QOhVrtkiGKH533Xbzm2I81Zt6LxjPXNzb+jXR9Z0/OlP4f970frO0wUPP3j16cKvYz6/P+/2P8HU7rBr'
        b'Sd/IxfSKGiGs0REzy0Z412FpoWYWeD3QQvaZ0lAbvKPutTrYTA7z0TFiSgiPFaFWFu7gL+24shDecLK2zEAnicGFmFtGzqOC7bCRAoe1wSHUogfRWK6F9TLaIdjiBZvC'
        b'sxUqVZY6AjUHD5czIBjdF8agPRy1pZSjjuFq1C2ICE1HBG8k8Dy7Toy2usik/v/i1TGeD8T6aLTaIl6Ko0LzRLvQnE7OxEqYYPp0/gjpbR4SpnqgQ+jtrcNmrPDjZeeF'
        b'wL5Nt4g8FpNHIXmQ6zpMS8ljGXksJ48iV1Hc/dFeX77O3kqWOZoocjTh52hxuaMdKsZrqFzvLMa/PdFZjHc3Irl3j1RLnPlsYlKPHy/82oNiTQX9JneXcD3etv3aUq7H'
        b'l4gqWEAk3lx8HxzDLPWx0WFiYAm00+EMIsv7uEjz/lieD7BJ9IFEotcF2uR5HyrP+2J53ofK875UnvfZ5Ou09dPq1b88r3E44sn4C4ueQ2qdTY408LllmHXiecICKRYH'
        b'NM4X8RGRIUJWZqq0VuFULClr+rKiyooSvVFjF07CsNwSRrkqz1SJbu/w4SQddKi8fWoiKvD/U0D+/6yAOC+vyQRQfIzDovUjiojLeuTL81H2CtxKY0t+xIvTY3P8eufb'
        b'sS1xWxwv0BoriaXGREVWo3tBdE0lkRj1FRqDB5F3ST9+rFiRcO/J6rHHhDLx/S2prFxJ+ktilLIsG3ZpaFhWWbICAx6r9+63A41EAUpKiIq2mb4IImDtjVS3pNfH1WMn'
        b'HIRxsmy+2aoxGOjKwIizulJf6liNS5xcZPvVAW2E1RUM9DjdEmc32h/V0kjxZzQ1F2fN/wsUrRncGq7M5mrz/5St/wuUrdiEqJikpKjY2LjY+NiEhPhot8oW+edZAyPy'
        b'SN9LWmS2W+kmE0UKyKJWH0iePjsGWONwZLUW7lOrslBDhMqhTZHLo+bB3Wuf0aE2wwfeceghvEdVkqiZRCMh+hOvPE1CB4j+ZEL3rfFEIpnmrVZmZGHR9Zl6n1XMGqfB'
        b'h6jRG54ZAVut0wG95dJszsnKsd1QRKpfiHbhAq1Y45tftQzd9sH6Bq4TR93JXwoPwYPwhDeA59E+32x0INZKZGd0bzp6ZM5AzaqsHDW52yhKCIaiF6JnCFCTJJ96ZqEb'
        b'qBbuH28xh2WhllAipitV8GIoA0aXiUSwew6tZwTaWeCLbnHwEWyZJ0HNimysWLEgKFYAj03PtBLvr8xY2I4nwrEXjfaivelYyYE35pEbPaNho2gtrIVNtFHYXToVd+si'
        b'vEC7poqQk/tBB6ETAnQPHYY7KaD+4iOgUIxa8LfBx4ZOAVayd5YnC16DHvmKASgABZPl1kRS2w2shh7zJbOEp3M3upWOdctm3IEbROe8vQY1wvM4IhO1pBOFa2mIZC4G'
        b'2i3+otPaKD26glXMa0S/BKoYrNGRy1kssBXeQRfQBayHEy0cdaJ9tAA8jvWZs6mj+EtQQSQ6YqK91Vn4nfWohDkFxolDgXU2qf0U7B5AJqTZpp+nRywgNw5HZszHCJCO'
        b'mvJD5fAuuYhzYbrjjmE5vEmnTGz0W4YuouNW4pUHt8NrU/JRe2yGAP/2YtAFgC6sCKC+BQp4d66vDSjzenFE4mZC4CW0RwhgbSTsmO+9GHWlWYkXVsFkjGx+dtU2D+6H'
        b'10JRe76EaLO9uuy0wWJ/dG8TVXir4f48c4YiJytyeAnBmWwV0fQFQI46RPA6rBtAbz9m4RF0N5y/x0YuRm3RwBc+YtG1MnSCXrI7hsthXxKDtVdUFdLfj54QM5D3laiA'
        b'+3PQNZspg/eQwCiF6iNzsvJCbbUtGBzu7ChxGJ6Rol3wXhJ/0OYoOgPvhytVEVjDF6PrGGatbKRhPgWgKhTtVq9QUz2QNTFJ09E1uYDOMbrtBw/bS03ExXAheL+Q4sP6'
        b'goULYVdvKXgbNdC2YF2y1DHEJQLbCAcmGL795z//+YeRdlrz8+w3xAVAv2fhe6x5CtaS6j9/sGzXlGw0PXBH2epfrD40Ougfe4bCwWfl86q8hvlH+exRjNHOO2ZFCTWz'
        b'BuTl55qFYa+2N3z81uBfv3o/8cjvX72028+wdJ7Fb7FuoHrs3J2osfuXvl0nH/5+snXfK/KvwpcEpf9wd9wP074adbLjC1VADJM8Iyuv9mzIp7cNkwSWc/VZx8//QZFY'
        b'//eJE18revx4t997H0s+GVN+5kTDp6NHzsx58+uk109cEvxl7P7jbzz2+yyiqv3N9b9i99e/Ovaz+VvHT/mPnetPHtk+dV3nsM/O3Vkwe86bId2nUy4tTNgxuXZPzMoR'
        b'r35T+1VD1D3v7HWqqtbVf7ec/+s+b+Ofho9OPatp3/a98d77viuE6+uU/sMjzguv7f9LeuM/uONDRCNN0ybvWPPrgPcmbNj6z3fOvZq4TrZs4/fi5WvQwbtfBz0KOqB6'
        b'0vLVr0fPyVx1qmCL3I/aDgrRSbgXnvJxcfmghogy1GQh1it0cU2F3Q6BWmf2miIcdgi0R0yvUEN34Pb5vmq0Y5GL4wexQ+BW7vPXbO0YMCHYR+3kYBOwQGCA++A5epMW'
        b'phitQeFh1GODQ9cB8F7MwlPh8KiFIFce6kwKVxKCH4Gxa3oxbGEVpbDLQolQM3qEuqYEqDPDxIBdxiQG5NI72yYaUBc8n5kVwYJk2C1UM7A7FzbSJEXlOswX7N4Z4iLR'
        b'BnbSjPnUjwMTlAewG3YtoL4c7hw5gkzUS2M97Ahytx94dyp101g0lbqawEeL0QEzWWuKUNQdQHKRaR6AdgngFXQ0lRpY0JUq+EjNm1cihDYDyyrU2c+1WPLAf5O9xZ3l'
        b'xZ/YGHpVcGp9KSCiwWb6YaU220uvBYbcVcfbX2iIJa4jo3DqIEZMHUiIM0kQDpNbiSWsP3Uv8WFJuHqIi2Wjt1WbvUbK20xKyIOIKCZySb6JIw8deZQ57CjuTDVez3N5'
        b'sQ9fZ6mj4hJHTWWOdvwcTfQabfRkGbkYbc6GORttPA2tVGQTtch5Qtd7zUW1XrWAbpAytT7U1OJbK3Tcay6qE9eAjeJq8QYRNa2IqWlFtEls2xzf7rw5TiofDZ6V4/x5'
        b'Oe79HF48ODpyQ+bqKDMooLGHcniKuyu9SvoweCqgxBtenLPBDJslqwRA4M/kKJLQ/TX0bv0sH1SXHwa3weYC1Dw/Kw/dyEU35vslREUBMHKIAG61CKiUJ5kpyEe1+NNc'
        b'EB+FGuKwGCVZxaCjg6NpMqzXe+Xb6mDgYSxLiMIYLI8dUVF7/qRhqBleC1tP7i4HqRNXUDY01xvuQSfQKTYVNeCVDoZO30CZUM5G9IJaGRUXE8/q0Akg3sTAF+C1hfzb'
        b'BFoE6GK468Xgd5ejwyy8qVerXhKZP8GZHoA/zc65lz0zWnrjT53vzt0afG6GbH7JRzM7FoV0vHVhQcaEwMOT38oPbt0wZ9qx0T976aXHH7//9e99Fie/mjx19QgkFQ26'
        b'cPXxWi/xhKejLvzq7CdD46pyq5dICn5+Nezo+Bd7Mpe8NcU75r1tYxMvZeabDpkOmlZ++GDkL7aJQv6javMXZVF/HN/1eNHHF5FfW3Wn94PRTRtqWt7p+dPfP0k9dMfv'
        b'87tVf2t8+b87z//p4+2Plt9JffTfoz9bX5FwNK/kYff4rMPbckPWrJv6lztD/+uHX/5x3H1l/OF3H5zM++dLrf/lW3Xk4z9Oe/l3qV9e2F72SeJmy/DsCtlgeRBPebpg'
        b'LdpOb+T3wgLHcbh7BjMfduh4H7oaPbpqo6CEfO5Ej2A3OrWOJo5JhY9sNHSjF6WimIbmwlbeV+KaYHQv/VwCjz5DQtG+UbzpeU96CmyUrX2WA6GtqIUyjdWD8tRlwuwI'
        b'LN61RsIuIfCHDwVFsAPupXR8SAk8iBrV9Cp34ShmHGqBxydoKD+ZDfdHOt1VTe6pLijyQhdTacNYwtkyOnwmPOt6F7ygMhpd5i3rDwOXqp0dHRl0zgKC4UXh8FnJvBvi'
        b'/fK1aurECB+M7fVjDFohgBfgVtRhkZMBnkTX0c6+xnw7Bz1H7x29jO5QNgpr4IHheFJ34hZ7/UbFIGCUYPk8dJheN1q5GHar4cln+SjqwjNGb6S8gW5PtfESBh1Gp3hu'
        b'MiaQv7x+TzGW9h2X15Ob62/Ci/BqDGziufBxQ4Ljpkx0BZ7h70r1TqTQGG1C3USIQy05KpEBXseJu9hK+AC2PB+h/Vevl3dxo+Evwac8SdvLkyIJx6GOitRdUUj4Ecvi'
        b'b54/STE55j9CyqX4nQIS4p0bJY50+0fMCll/Npj1wTzM2YmGb57nTV69XKHHi7c8m3tEZovGZOkR4Hw/lRGJTORyVtNKB78xOJgO5Tcr8OMiY7sAk/KbLeC/ZB68ffiO'
        b'/hu8rgSUsQi//6iPyYA/M2Wxn9SwmV4NNouIibNYTUaaViHTEMu+k4HluazispXcOjOup8rEmYkXI2+5sZmizA5zvM2M486a/ayl3sDbv0h3StZZODeWJgf7FNv+nvV+'
        b'5+8/rsG0krxWZh+WW+vhVbQHdi/EYuPVpCJ4Pg/WicBQuEWwHnaHUh6mJhqvaKUaACVQ5sHr/KtpzqP98CrlrLBxoQLrqDvQPrVSKQCDYL0AnpuOaihT/riCsuqk297F'
        b'ET9MW86/hAc3e17tKCsei9pL4AN0Eh2PGYKOg7B4URI8uIFXse7K0SleL8Oa3WUgJopZJrpDee/4PHTWwXsJ302GZzDrvYf28i8sOZM9wKG1ZaMLScPgdn4P+Nxk+Cif'
        b'llpDGEczMyIDndMvWZ4kNO/A6cH7J2Q1jfFH06XC332z7I0rxzO+m1UUuGhEUOCemM9Ojgr3vfKfu48+vLNgcODNnvcOJI5453b+7FM7Jy1vbT98aE3BgnkJK/54vMRU'
        b'q/77S49vX31R+9LHN4uXnMjymiI6nLrkN3E/U/317dLFkYIVb17K+/Czaf8judr8y5eXlXz3G82R4KG6rz/yypw7/q1rnFxMt0A3wfOb7XugybDFxbePncwTzW70gsR+'
        b'wy86BE/TW34zYQNVMOYvQlvClVksHudZJqxYjc5s5jWaRlEm1p6IceAu3KVWKVjgy7HoqCKf3mYew8DdvQpCHAZCr88gcRjcpaYkeQbaL3N6JcloeIHnRHDXZrn4RwiG'
        b'B1dDjbmILLXeN4TwNNIgFAyikvgg/E0oHtlHDcI0zols2Ipm/0QvxEr8+PAZyvSCBz9EWxNypkdYpbGUu7/0PAHYbpomO4zk/Qdix8XnQo8XnwuoD63wAwHjZnexl1gR'
        b'umHWrCa/DAZnsvX8R8tIxyfLVDpZGPkVJsO01szbsQlB4taSg6vErBumrNZXhUXQhmyU0eTeKmwm9/VpHbZojam0XL+aU8pyiOl8jd7MOagfrYMOgGbXyHSVBkzp+yFl'
        b'Lu8TcJAyCU/KJsF9aFt4Ol4WuelY2kCdcFdGViY8V5AOL6K6CCWWP9LRTq8qxUgrOZYId/vgFVAfkZGlRPWR8N5k2FWA9fLGyDwscShCycUsanTTC+4bqqHkp0g5C+3F'
        b'pK4BHYPXIjAfMjBYY9iZaSU6U2EkuhqO9ZS1YCOsWwtvoheodB8TBK+E57Dw2BTAzAPoINw5Sf/O4yrWfBUn/vK19VOaqYPHjiOHB4VuLvmESZoZ8LOXRGDRi/UxIP+l'
        b'Xcy5n70+Znfg8u6r0eaCPQUl//u0bHNkqK86zfe9Lq/hQdV56Snta6za9/Izk8/sUAhHpb2z9Wf+zQ1PYmfV/idzPNWq9koJurCqq+Xp2+Fzb1qetkUdm5JY99dF029/'
        b'bv7d+Ph3p+0+Uy9579PKs+tnvr8h2bfn6hX59j/4Xj5886/lzaP9pAlv/XHLN51ra7/6SrBmQ9wPo5A8gMqq/lhqw9MMd6QR4U+YyMBL6FE4L3UdhjtKiKhJX2JGbpBv'
        b'ZHXLNw7Q8yaEHegMqkHX0PU1CvgI7uaNK97wDAtPYKZxjxfku2dhcW3fYFpLPRbYxdnsiKGonTfP7MUV7yHvbItQwiZ0WEVz+KIrLLoPm+J4SRvuQtvUEbAlJ3wIf+G/'
        b'73QWdSyEV6gBJnaFVAa7SBWROeRIziY2DB3HIikRpgtx9GnCJuRK1BpBRhcQJdDD02WwJo0nlC3wEryO7qx3vUT9EqqjyToO3giPJLsHCqWcxdTviCDQm4x6PJ24PHR+'
        b'Ueg8KmpHYr1NnMoOQUcn8FJ6KzqPxWsHonoPYuEhVA+PwS2wnm/6GLo9BiPfTaKr2GZmBjsUHpbxb6Q5k76AF4fh3WC7RHwVc/ZddNQMbJtQVsj3DbcMz7IR6A5eJP3Y'
        b'ZX6EZDuRaSFZwq6eLeTjzVtWJPT4DabPWE7lLSVBOLbaz0FGSelsl9cBVLnS6n46yfJ5e+m3CT/++Qz9rgl2eT2AS8O4cseRZRPZAuJPxsfzlRPibSJ7C3KpKYn8TiaP'
        b'yeThqRR/mp545ZmIEds0hR8BzT4LP7L5SkltmHDZ/slF/BeL/wY+cwafONxrK0uLiuhRoR5JlamyijNZ1j3PMSXiU089cqiFh4rdlMPRaeKnfNC/3fzWL7KYyEtA/gRs'
        b'rjgSoZAlFjfADBrP2rSXH32y/gIpxijABCulzCB2RO6wRP/hVnpJAWoMNqsiYFO5SmH29xcAv5EsptZ3l9DdpgB0eI4vPGshtMmXbLPk5irEsF4JRsQIx6G7E/6/e2+R'
        b'VzZ95x7qzEWHyAGWMfCQGYzhFtF39MVuqlAr4ZUojExCdJNBV6yrVhiojIvuholczD7wDqxn0eHYRbx74mnY7oUaVRFE/ooVAi3aLYGNbAbqgI/0g4ydIjPBv7jX2j+j'
        b'p0g+0WZqXil5in+v0JXrngqvduR3zOvoPPCz7b827BsUfCV05u4sr1KfmV4zw/eOF6RPpG/aGvHzgNsTyGvsCHqGxSqdDiayaDe6HwtPRfGc4ASsWVcG77uq6FfZ5bQk'
        b'2rFuWK8VHLaw/nCbYv4SXrM/hqXNOod2DjJ9eOX8NDrElz01DXaTTVqaKlguWcZyCnSkvyMrUqx3YXGHKyLuCpRQBTsTqvHEkEsIkxA/TVbH0hD2CEmBHjF/YMzde5LW'
        b'kKjVDuQmZcew9vq32D4fOMuPdN+soAg9DA/NUKRHZMDmSLrRilWa3UCG9okGwf1whwsCDbZ9m79yvggjilwGgbGS1Qq2excKOKFWqBVtB1qx1quZLRThsISGvWlYjMM+'
        b'NOxLw144LKVhPxqW4LA/DQfQsDcOB9LwABr2wa154daCtAPJy+a0MXhFMPR6De9CqS1tiHYoufhCG0vThmmH4zR/bRxOFdNzMkLtCO1IHBegjcdxQlxitFZGLqlo82lj'
        b'2wQ6QZuwTUQ+2hAdi+PIt8DxzcfyTyGfw+kpfPa3dsyhAFyXT289z5bRJvSN+9ee2tBDA7XyQ2zhAC6IG6ANCwErBtaAGoaGwu0hmmMQ9TvkTxBJ8Jx4aSO0Cjxrg6lH'
        b'ohedJ5FWqY3EccHaEGqxSOzxLsJMSzMHy8zUXuRidnfVNHi/RjF9FaDYYWwXPb+x3T3F8uGN7Q/0vFl9+trV0gqVmT9MHlvYDIYyIPRKuDnbuK6IjyzYtJH5lgWLwFTt'
        b'+nbJCEDf0ITOYSnntstRdZddJ0woGr1Afpk3PCYJROczaU1wxVhACFdVtrVEOkcAPrb38q/koX/cqmGo/WzpN++PbHrRb0uUVHA47lQUu+TLp6OkP5sUlP7D4IlHZ/gs'
        b'2fvVnWsTfjVn4vCIRYYpuyfFVWtyw5KGJA459/bIjLPflbTPSQzZMHLS4abBw0a/sH7gX5qmeY08pHrj90Vzf97w5Ftw9khI4c6X5N68jPoC8faAu4z8i3YUAiApYC1+'
        b'3vwbloLhVhUW2xrhZWpwFk9iB2wEVIH3gfXogsPLeSZ64LS7eFtIDc6FAViSxbq2Ee3qOzMTQkTl1bF00w5HbFPwJ7/DQ+krhUO81STPkBHCVHgQ7aeauxKeQjf5TsJm'
        b'WIc6qPm6iWzbdQrgMXRHSQVzGdxTZM+FtmJxuDULK+84U7sA0/GmiTxdvjJHguoGwsZILL6qUBODpfsG8n6orcstxPPDH91eCRvX4Eos/CuMm2FrtTgHk//6HNSiFINk'
        b'tRjuW7WQp63PLV32nu8e5UyzY8SMj0jCDKXnvG0GU6Y6yLFOnnn7IW/g7BFRh6QeIfFn7ZH27mMZK3u89cYqq4XeqeXeSiAykUs9TevJYxOwC50bXPoZ2Yf2v+Eie7rp'
        b'3/Me4xUVkU73c5Q1jbUf4nZqxXGKe0TvjaB9DrQqca0qQlae81ivX5HzzPXTpVn2Ln0/yqn5vke4lc97rNenyAGlfpqd62h2pMqe3e5G+ZNadZygJmhTVKHv7xxzhqPR'
        b'YKJgyHSmyoqf1lq5a2uatf20luVobRBtjTjY/pS2bJAUF1kqLRpDPw3lOhoKKSBZ7W64blv7103zbgVnFvR90x9lCYE+gvTrAvKr2PCLJB+e4xSrvKQci8mzrDgiYcRQ'
        b'oM/962nGTPauzG/9hoi86Zo2beif1Rqp7rc5nxR/Ar7qDMnveClkW0jSG0zxTdGnO/8hZ+iFGbmw2+SgZPD6MBsxe5aUiWBNP0In1b0o3aLvKbPTrQVEyqwe4EwH/tXD'
        b'0vl9iM1lF0Olm0aI1vlvUnOeQ2iwQUsVI6IHMKaLMzYO3fjpDDohY96fVkpx849rmMEh+gFPQwRmcpVNUNR4/pXAu7SPSzI1mZoVuk+DVeCvFUPnDSWQAtoksaL8XTlr'
        b'oTa8s+jylGeZjhOcClEHBRU6Ooln3NfQfrSNGH/CFEqseZSthtvY2A1r+1MeAoqo67C+misqMVSWrux9rZ0dpkurQ5ym2jW3y+tWRdTn1Z0e0QRcrBiN+LGoD3i7XMDr'
        b'uU3HerRDmKhN9tevCjCMBf8KjEmlfbeRbF4Y5ar/YZ4KdqUKc4s3H6nwB1S/nToDC0HnhQA+nACqQfWASN5z8hxs3wzPswDdSQXrwXrUMcJK7EboMjob4iQbzsrII46j'
        b'BaHZCgbEwXqxP3yILtDWflgkwmLo2jiv6cWZ7boJgHoRfuxr8yJMPhP8zqJHwW8CK7HWoAflS+yXGrn4EtqQhF5mZEKn7fcZHUMHfNBB1Jljqsalqb/FwPlYbrPp1ehc'
        b'LFatqV4NO+F56t4n0NHuzBNML45Ysmw8oJHiRBL5/hgf3MeYhTOAnnlULjC34OpEuX+e0HzMn40OnFV26wFk2LmfR1Ydmv6Vl2SQUaA6fyluwJptu0oW5W/9sEafnPjy'
        b'/cS/fqs7VPXD/V1RRq/98jRV6Furjrw/5sL1tKcDXxIO/N/6l8IeyPN1r3V/6jMlJaUgfOrK/OCl76/tbIr4R9z687KCXyR2Fxy8dmG45aO3U/Tt/lFJJVVDJK+WfzHt'
        b'hcqxr4/eKffiDZA3YBN6SLRuJbrlbP4sm45uU+PopEzU7gtv5aj7eMaNTqSLEV2dJ6VrkWwAul+PvAgId/O+FQ0YFbb4htlkXL7OdVMjyZHSa0J0uRid4O8vOoVqwqkT'
        b'BhGEMWrAC1hrttcqBvB0RhTsEo+QJfCWh9vonoD3GxgMG+2n/CphO7WTcugwfGAzLsDb8DIxUhPzQlxK7wtwPRo6xUVrTHrb601dpNEiQtVZRoal0WE2VzIpUx3otEJp'
        b'Qdd3L2tMZWYPpJ41tbgShGb8WNqHIJx2eflln+ayS4W2tSsGfV/DS8+/OV7DK6S7USJMCoSUFIgoKRBuEnki930d68XZdCsE7TWFw73j4DUB8doaDfcmUJ2V95C6hLor'
        b'wvMUGEZ1CxTE5cNrADsKnYYH9QuPjBSao3GejLRPeG79tPjz4nLd59rP9w0vVgarNT66dM3nxZ8WZ5cGlUp072cKwLEPJV6DujDXpuh0xQtjVCO1psD6HHidbBQQ/w8G'
        b'DC8XwroMeM8+//2bs8VF9EgEhXKgM5QN/tTpwmWiaVa7StPrWkffnEyNQ32IvZCPfyYvhXIrfuj7QPlAkCco08bdA5lw+loRBrOYmhUIqL2eE9TPYcAUZfMwJf3UF6L9'
        b'+YoF8RYF3McAAbrHZC1Hd/WfbnwsMhNzdOf1zz4rVmse/zn0jyose31SHPD9J8WfFet1Yfs+K35SvFL3VPtZMdsQlRBr7T4VZb2y+sqp6PpoYWyVDgBLvvQ71eleufS5'
        b'vE9c3pJNDHhO8BzkDE+ThHevIc6bg52mtbfM8wHW/THafuC8Cz8q+8B571BnOLvv0BNi6XAP8Th+WYtsC1v0nNDWPQttkUdoUxv0/mxFPrqBjikWoPbYdAEQeZFt0BZ0'
        b'Xj/g+BiRmZyTWC5697NilQPi6ZpPi5WaT4qfYpg/LQ7UlOsyS4OqtLY1fOafXt96n8VrmFg5YfMKtE8NL6N9dhdo2GV4/hfr9vgX2S4VdQK5i/hdTUBePdRpbl0KuId3'
        b'j1inKbVUmjwQa6FprydA78GPNX0A3TjIGdAeOyMP4J14e316iTtvj1+v8r2SW9fjt7rSWlrOmWiRaNdgTI9vKbnLhSOvSY12DsT0SLR6M38JC3ENJq+Dt5CrdjmrRbOW'
        b'3hZL9pN6pNza0nINucuURPW7+yUfSM+N94iIT1N0j4/9khW91ulQ+iKaw6K3GLgeCXmXBsnc40t+2Q9702h6exOtKcZELkPo8SLnD0sq19IT6T2iqvJKI9cj0GnW9oi4'
        b'Co3e0CPU43I9ghJ9qZzt8UqbOTNnfnZBj3BmzrzZpi7S9HngZOGwS8ZEvDOTEdlu/xVTr2WmVqKT/CvbPQQfhvZZP6W8jNwzaAPz7QpfLxClWXJ3fRqgfr4S2BBvRjcD'
        b'ML7ARnSCRaeZMAXsohs6ArgD3TJbVuNkLJ49GuvLAC90kPWHl+BFK+l0FmoNCCe+kxdD07OUqqw8VJcNL0agVnhrVCQWnyMyIrHEi+Ur+1kitHeJdCbaio5RTl093YBl'
        b'qvNobx4JgCx2Ad2Ayl3nHRsXJYTHIB7qJAD3wl2wmwr0MnQP3o/F+LwcHY0Fsdwq/uzUww1oCy7BsoMBEwpgW/RCnlQ0wzPojN1l1MqGM8C3kEWX1obzx2xu4n4ewuXE'
        b'WBo4BBg5gO0l8ArdyNsE22bx7rDx5C3mVyejowzaC/dF0YkM14WBAuk3QhBYPGMcMxfQXmvKUTeujEH3UTdgwgDcNwG18kfbWtBVAexAXWqlQkncVLMUqCGTAUPgSeF0'
        b'uD+O1vkwTQamF3zPgqri1GPpg3ngwIfwIqzBtQrQzTmAiQCwA3aiR1be2+l4Rji9ZKRhporfiwqAzYIS2LyBVujFDAERublCICve0BzsDfip6hgXj6vzAhbAKMh9Ip3T'
        b'+ZNKzSOI40ELfR1QQYYwgoF3MZR5t7nuiqlgw4a/YLwpjnkxYyxf01p4a0xsHLwClqgBowTwYEYW3+VbI9Bh4oWFLnpnYcXJO5qFHUOH04pqqzJAG3hDgOctY8OAzTz7'
        b'Ri0x+aQiIaqDVwETCWBnHNpPk7zKg/jbNqjLwM4YKTuOQ0doVVItlpsXTRYBrPJ8FrDO5l9/GO7Mio1LAFNj6WS1o4ap9NzgZng4U00uYGmEe7NQC+/m7A+3C6bCs1iH'
        b'IhUuX5MMqoSDBaC4eJ5u02C+Qh/0qBjXx6KLxXSQ+/PQQ97j8L4GbuVrzLbvIDBgGGwTwlZ0CYuB7eH8vN5Gh9ExXIUY1cD7dHQd8Cg6zu+X3seofdXWr0drs3kg+lcJ'
        b'kor5QwQ/pAeB8XFhmGYUp/6HXx7fpw1pqCs2JkocAnfSQe4rQvcpui/OQztsOMtinO2GuwYyqA0dhQ/p2lkuy42NjwJxPoCJwaWGGyjWJo4C4WriyMcAsV46lg1Bt2Ej'
        b'TVlshftjE6PIMmkHTBLu+GxYTzGP26CkiKfCGtARrIRexuBIFQSiW6iGX1hbMLLfwmVZLAHjtTAZYwdsltKFNU48Xc1PlxyegaeII7o0UDB4jZkOeMd8CQjMLRBhIBiy'
        b'fSJtUL3nhx7EJsZhaFynlR1IWsWj2tnF6DruCTloqMYYUho8jx0ewiv5frNgMy4jnBUImBTcfjxspqNCx8KK1Wp4gVyFC9hKZjrqRHcpMVqnD8QF2ImoDTCpGAkXCGiH'
        b'0QV0EZ1TEzLWRPYcxANh+1TWW6Lir+kZVA2+HlpMKMGC4impgPcTxeoE3AGvRcWJ0F60HzAzADwCzyfwibtGoodYL8gguyAbiwToIQM7McWk1c1NnguatN+weM2GvcLF'
        b'8yttOGyZQyoTzNUBZiaAR6eMoqtDBy8EqTEhEcPzcAdglzORsBEepvUMCB4KotJzCDKnlpsn8AQKnchEx9Uq4n+Tt0koZHCfjkttFpE8LEDtFZEjrCuUQDkN7qNnadPQ'
        b'g7X01MK8dHhQgrVdxQLeQQ3VZUVgmoM7HOQ1XDaXx+Yd6L7Mdsb0ITxIF4QEdbCwPUTfe/GzcrMACAelEZTOrF4fzkMYHfRH99BeLE2idtgUASJkGAepb+4juHeB+pkt'
        b'OsxhhGBCFLoFu0RWHaql0zoEdaxCjXnkVIwQCIPmwDvMMnQAdfAI2RgOj6sLULNwALwIGHQAoCsKjBCEOMOT6Gzis2ejGTAhcGKOSA+PcnTq4GnUsQR1+hKmMQY+xHQZ'
        b'PZzCF69Hh+aG4znBZCVdkcErfNFCMFGdUSCK8ZHTQadtGgbiinPEGEs27K+cyw86Z94Q1OlFBp8KH5GRXkQnaZUz/Wf2qZAFE6egh/NFsQsxJyRDmgHvoGPqPIV4KToH'
        b'6CncB+gA3E97W42OxedjXtwswvNZyK5nRoSie7TNhBygno+nYT7cjgudAui6/0hKzzDEOnzowXP0AB5wnojRsFGIbsJ6KSUiQbkzUCcWNNWFmJrB++EMJa+wbuMAsqqV'
        b'qmxcRqWIEWKkPSiEF5YbjGg3RbEIdKsadWLxZOJo+ADAB7Gwk95Dhh5NRidcyrK4bKcQNk2uSIJtPAHoRPvhYURskuhqsB7oUUc2XZtFi6YRB8rsCh97bwMGClbAqyq6'
        b'oMNXYY5CTkfrlaPBaEyJX7COpYQe1vJ8k6AT7/sARsAbQrxsW/D4tyfRRlehfRijO/GayA+A9zARgjvS6UiK8kJRI0sc3uD+lWAlxp86iv84f4tVjS4HKhQqeCE0g6yz'
        b'gdMFqA3u43hy1YC2kiql+Oe+FHgdwOuY7l+gI5kMz5rIQZQ58KTzWZQVofzKPTjTYvbzYzlMu/GqQxfhKdTIHz6b5gMGJT0hHFUqCongCQY8Q3zrGvHI0ckBlaASHpxP'
        b'EWtRJLyFRbV01DIAXUjHg89R0F7KhgvRFdRaRK2YH1VNYF4XgNwyn+nG95JkFUbelIoubVhLTKnAf3I1RrCTY/RVyRxj/g4v5JRvdct+87bxjdxA8fvJv1B3Jqx6N3fG'
        b'sjdnvP0/N6arj+Yefap++1ZVdNDjfbla05N3q7Z/GP6h70s1Xyalgtde/OLlc9yqARP+uk4X84LZNG3igvps0RDBmzW7Dg/wm//5z3t25d0ZnRIyO27uuPZz1xMtb3OR'
        b'38RwBUNee3SuadGku7lPKj/8/tvMK68NnPOryy8v/XhU4lht4YEZqSMHJDaPW+X7z7iXt+a9ezOo4ZXpkxfcrHtlxs3CJw2GmlcW18/685h3Lj4NfNv7bY679fiFwo9F'
        b'ux/s2rggePY3MxMmpcpMVxI+GLMb3Zg6d1bLjJbFyUrT8Tc/Pvn43MFDwcmC5JUfHXq87rEoXD12yJj9TaW6wYM//dWRd18MjpzbVvraW3//wyHTwgS/0j++umZk3rvv'
        b'f2T6bNrZrwcPm9Z85nXr5FU+h39z5eXwj7xnFGaFff27de8MXrUtadm7Tf+rWCRLfhA2KX3phxcWJqe1LEELf3ltVHvZX8yR33z53qtxRe2bBMuVX8s+WnngPypC/7Dy'
        b'v0K/zXmofOPyvhvLtP6bVrVW1l1s9ts446E8/taVxne6D+/63ezPm3Z80bPm0AfrOb8/7PcPWDFyVMY/Tnx6f+amiK9O7kmYNvjtK4kJH5YFTbtsLHoc+Y97Ayo2yb/q'
        b'6lqn+O/hm1bGPbqW/MXPpx7tal08bZPP7ouD/mySf66tro/7W0rm8N9++/eA8RM/YfzvywfSW9ZgMzow69nzuzZ/AbRLHyIqxzLICQtZkmM3rA/PVjDwOgNYeJDJmlTN'
        b'74pcCEK7sSSFVQesItxZKZzFwAfo1iLqswDb5k+BjQFVUhO6DpsDVvt5i8EgeETgh9oqx/ryN+U/0o71jVgFz0Wk2+3CA9BdAaaoD9AuanUdhg5pez3B4JapvHfqdXSI'
        b'Jg/Bi7cTNkZGogZ4Xh1BHYdPsLBRPoA/47ZtImyjBuBMeBmdoSY9SRarRd3ojoUysNrYMLyaGNRRBNjVTBqW+C/xtuDtaA884exphm7nsooJq/hjgSfxzDywnQvcHEAP'
        b'VqMu20HtVNid7OTDAW+iPewAbRw/4Nup8AZmBb59beEbLfwBOCzQ18HGoeNtThUubhfiGN6Z+Xga2gYbi+FVeyYnr4uUgZZJdPZz84iXB9m5IFoLbMmxGzWxtNkSniyC'
        b'N9PhduoSkk6mptcA6mz8vDwK1nkD2vexqBNeJwoCPDHL5cAg3A1P86OrQ9uI1wjx80hDl5xcPaxom7v77n+yE2iPQKPljTMWAHqNM5uBkrgGC5kg6ovnQ12Gg+wfNojp'
        b'88Fxw7wCmfHkMDYzDJcgf1JGwg5jZIw/LRHI+NOcgTR3IDOI1M5W+/VaXXBfXLyPiVPVTz3wxvKleg32GJCgi1h+CKI5LD9bwFvDXHyRXXrhfh+d2vX4NzaBWpHDrsdQ'
        b'u4Tn3fQ+e3ejwLN2CTlvl8hNtp2gnlll2LZUAHhjH+E68P6cKrjXkCoipUehq2peGjuLTmyGe9FheAeHQkAIrIf3aP7JmKHeih25EdcWA2Kw9kfrv6iTkP3fqC0pmyOE'
        b'jBcviE732kD9w3JzNqXcmz3bxjmPDDXFlsHzcbgC2A5KUbMPL4Fcq9oQOx5ujcMiKtwPOHgA1dJavs31oretbCkrMVyYsZyv+tN8+kKXpJ8N2hiRG2Frr7FQSiwzoVsy'
        b'V2SOw+oUjayr8AW4fsmXKVzErKVJgMoC6rEj82FnMRHg5hNRV7QaK+PooE24w6rFaXg3NipKCJjxZALgnkxvWtkL4eN4P7VVmrGn9DKbwn8Ii3a74Xl0QyokNpZqg4gK'
        b'RyJ4ahHqjDZhKMOb+L9oHK1d6o+2Yo3oDmwjI72F/2eiRlrRHHRbjfZi7bYGw1IBFAtgF211W5KIeuQdncEZfp+z0LbN0hi4DKs+7eQjQodysdiyk1yP0yymjUdL4GWs'
        b'+l4gaDESjETHI3gN4g68DS9hEN4zOXyI6UbnOHiIajxadAPuzKfbNgzaHVPBBGF63cZv+hyA7evCZ6H99AzMWtRk4QF3Ch7MguezEdnfXgfWYTJ+lt7fkxC2Dp43MxjT'
        b'1oP1Exi610ottaNjF5VOO0NRlglqpjupB2N5/Akcstnw10Uqfnv1Z5N4IH85rthwIGUlH1lbTF+5ExpYtUG6dcoMPjIs0IcCWSbSGw5LjXxkVQV/Tc/rK8oi8jRT+Mgb'
        b'm3jvRmA0GlKWV/OR2dP5yNc1hogrmkl85IR8ftaj5m6MiBo8C+g1+Y9FZgWez9qldyt2q7IF0YGzzz99pbRs4vZ1hePevDJzqWzht+zLb1/v3tm+47e/GiFcBfbV5cuy'
        b'tyQJ/5A9sLBux1++fy2+K+bXFxZ+AiMGdtzRvll/YucqcfCENtWF8DsxYV+/U5t6UP9l19G7V3618re/Gf7b2IH/p73rAIvyWNf/FmDpiIgIllVR6VWaIIpiQYooFgQR'
        b'FnaBReoua1dERcUCKqIgCkEQsZeoUbHEGY0xiSeJJ0bdYyyxxJMYTaKJ5ZyYO+XfZRfYFXNyn3uf515XZvdv0/+Z75v53u89vTtzzr2sU37fD2nYsmbI9fBp14Qz1/d6'
        b'uNdGNndATkXvbpm+Ex+Cn+t2HziSsH9t2bXn5unwtlQhezPhTt2jpuSvfvBo2WtzUjzUOsx6snWl4tKB0U8HwXGbv3t0YPDpDxmJWVrR178+6m9XcutNhl1ac78lt75Z'
        b'U/H80IOrDuZxZu/NuLape+WIyu7KkVFzy+d8dHP1ulBRzdE6b9PPag7d/3LkY5tnKddKjF/+y+qF4HTC2UGv5g/pFnBuxs2yO48nPpF4/PqPvK4P5785+C9nO7LB6+wa'
        b'RfaNYSNXz7YxKAfvk0l91kywHa4ugkchdvbqgieno1ywKS+XCjOlcLO3WtYYFkLtznuEk0m9D9juiLV0sFbDblMWRWwl4fLe4Ayea6OxLoq9G0dxULiFsQ7jgf1ovKPA'
        b'cngISf8rsCcplNEZabCUgzFE/QrmU6crJQJYr0MY6xEPygwygwazssdAvKcd4cpD40kFw4P7OeA9uHUmuRgB68ypkYoRbMZ2KthKxR42EYEMnpoWgrJZ56miLyKLmbbx'
        b'fAdQBbeTGdx20RANXiK8uiSfxVgP4IG9Q2EJScEPboui0o0LPMkaqaIiVlDb0hYkoantQanoMteeFV7AEriZ2INagrNersHgaFvHA2D/UGJUOg+pyJtbY8GyzcihrHQD'
        b'6+FiCgkrDYGLkagx1s3DA5Z7jkOqNGxkrOEuHhq/SsFp0jJI1Vs5EhV5c4CGuava2BU9sZoipKrSkPaMTWLLIg1QGvsYPpcDamFJCEVI1cwrigRLwVk1soBs/JuAs8R6'
        b'IakvEoxW94YrddoZECMD7ICKenyoieuGEquGJz1ZVBWVWcFRUEvkcrgxNEIlusHjkjbSG5HcxqH2IgJu8aQ5YHUfcKKNaS2abNaTTrcoGCx2BWenubBwC+JSCMlpdapN'
        b'5U7tjvGxzR4Ru1K0xS6ZGYfPVXkWsCFClw362KKPHfrgYwviZcCG3GHN/uGPykuOGdeEI+TizVQzroDgvuZZtAo3OGEdFm56wF2aBm/7UPCkA3lqo9ZeWpskUQyEZxKN'
        b'2H+g3/tJpDHkv2w9Q2TXt6O6Ypy7t2VFxaa+Miy6UvNfYheMTYKVApWhqOoX3p8iJpYUioXXUIgtB9nqJ/vAZI9QaZYcGzYxLDp50rTYUXFKnlxSqORjnwFKU/ZC3KhJ'
        b'cUSoJDVB6/I/90Ihw3RtbrhacfYFPKsuncJfGVjwLcwtDG0EVkYqfxOGpCcYan1MeLSH0CNum6uqj5WBBceGZxdO1rbt86gNOVhhx04FBozVJF4CqNLepFYRtchD23LD'
        b'8jdaEu5US9W3eJD6l9FaI7ETkqQxzMIyHQNiTNVMsWZi82WM2EJsyTLFWpHjLuQYM8Vak+Ou5BgzxdqQ427kGDPF2pLj7uQYM8XakeMe5BgzxdqTYwdybLaRn87gXIl7'
        b'buVuNMTwlyxzca8eTJYFBoqwx71Vx93R32ZuGUfszALJjYhfJdMVlius0o3FQnFfygKLrhkTTle+uJ+4/zJBghWuDbHjWs4KqkGYrTBH+gPhp0X3dxH3IVbHLizfa2TM'
        b'qNebtLDXk1S0pegSJXsVOmEWEMzqJMoV4y4ubcsuqXXgMglDwFkaJ/QrL1Wel435pTFyHTvxpTyZ2ImwJL+Q+rEmMPY2vpV1YzSNlMYsMxnm9WF/kk1lAfU1ihl+xOmz'
        b'lLyZuehcjkQsVeSgc4J8VJrZeTIxGSGoYawmQay2MyuVt3BjpISZsNvEpmpnVm+jiMVI/p95naWIxXX9pyli384Q244NtkMQ/59kiNWof3U+sL9xPblAl3XlIVcoys7P'
        b'FLl3lJUgYVomSjKNePXWT1irn6+2A27ad6iRt/LVoq5HHSCHj54izBalYm509FPTp7SzRxtvzZR/rcNcaGed1K2Tj0ZVdJB5NiOo+7+FLVcXM27HXh50seV2khm3w0hb'
        b'2XKFf54ZV/WK02qnR0KpmG0w37c1mGpcYL1es0dCmSRDKkc1jMYoNJSR7uQmVLDNpsjF3qffmYDWkq6/lJhbYVXWbu6CFLfx0cbU+allT7BZH/sskiZVFLFgPThCvJ+W'
        b'DDezgltBM4n1aXA3xolhYpcOT+m5tl8cpbUNxXsTemNFgi+onho9WdOral2+GWwMYfc2P0giCynxzVNTsgdPNmOIl2IkbTenqCKGh5CEqxm5hiKiSWsLjoOVpkihaGB3'
        b'X0VeRCfP3Oac4jZQ7M8oMKAR7ioAZR1mOcI1jo0sDW4g8S2G5cagEh6BJ2i9RpB1gxRTaYrbN8HDaA3MAtvQDWx8fFCpGSVc2ar6tcnoMVOUzSpqKvJbN7JqZHe6Z0rU'
        b'B1GTaHvBfYVIM2LjBQ3zNON1Umk3WpGeBHtMUWWdASukVenrOPJVZKL5t/tnn5qP8DYL/zKwaJjT0hGPirnX48eGzFppIjCdOtL5q/PijTsUT64HfN57uVnBacMD+4M9'
        b'KsYsqr334YzUgo8TFyQ03j3GD4Y+OU/uKQf5G0eHpWW61Bz5rsudkhl3zN8Uz55XPHlR1g9xaaWf2jzo/uCjwwfGbys72uvOsJcFrxduSTjOP/0754p9wIn6Wc4mRGma'
        b'lDC8lSe3q4Fa1Zzdnyxhx8PVYL96FRzsjm9dCAe7QSWxy8WrWfBoayykj0X3GGbA9IFVfHgA7Igncfl2naGttILScA7VWlGNbiXYSrjUYqwm5FwMt/j6hZBLU0yKiD4N'
        b'Vg/hseo0qJRTxXAzPIDeC6oZhsHVBlQxBEdCiEI9sBvYqq33B9hzqNZfBJfQTZBNoGGIhpqaBc5wVFrqqoWF2OVDWD6spkgUd/g+PBYIS+RkFQOdiCKCrLshEw2WGYFt'
        b'seD0Xya/q8GRWCzS0OiKmBGE8pZj2Ep/S6lwiQ9T9ZGKYRYJHTrIcI/jAC/0yk7ioAUHp3BwGgdnGObtlrCCzkRirlUmZ/SgHLedhqq3mLmh5SKufc47DyNUi0t6oG+T'
        b'edqsuDglDVZcfEovK+47YSrNkjVkJz2Zildl6nXvNjkgssC7M6UaJ6ukJD2pJqpT7UNT/Y/ZePnJSDLSk+IMdYoONEUN+enPpIbEHz2pidSpObWKSKK2kNV34/tVwzlV'
        b'Aome9MXq9O3xAoaG1PKnCH9VUoueFDO0UkT1q5Z0NPswlyKdyQKH2og2Jo3HZgTbn+O3lVjRYlt/skeF3T1wWR3VhPj9NUs3U1ujG+i0RldRpBpYd5pSSYKpIzvLqERu'
        b'fhdCJU0CpXZRYkIlNRjZxU3ooomJRscEZI1u0qSDIZIrzQZm2ei8dqdOaIgwLi8H6whUp8ae2Vhgsyg1T1HI8hTJkTSqq27wP8wJIsFVIpamE8aYQlba1i4UW9/E2SSq'
        b'tgzW71wHgi7+F6FmOBLpU9y8/TXUFaGTikZFt+KiWa9UKG/3YgqdwlJlkrTMXMzgwmpxxPtchxlt7QdyuTQjl3QFypPSjqxLLpRqlkqKFJoMHWQsKkXFmzSyf5BaX8Ep'
        b'eTu74VUQFbsvvkNN75umS8UivVJKnsecUbjuAoM6zzmVrl0gXGqpRP7XMUY5YYYkwu3kLHRxycFKNCrOXBeXP80hJXQifFHulHbpXaLWwxfVqefflb1JqIN1Shd7k0fn'
        b'sqEF5dDL4eSk5nDydhYmevvo5mDShIOwzaiQ0OJIc0lGCd96eHT0tGm4ZB05n8X/8kVzc4jrWokMT0xuhKBNrftqZMhHf4b0Ektpr4TQt8VT9aZ0mC0q9mjSUaHkfb10'
        b'M4tpgmdU60Iarwk6i97IXLmUZiovvWOiLnEW6hmkPvADxH+vaA7+3UmOIvwvTCsSOVkSk6ZlFkoJEZW8lSat/TurM053oTfmeZYo0OCqjgD1YKmQrSI0QuWgN27UZPdJ'
        b'osJUCV5m7Jg2y12Iugt1NZqtyJkpyey4/t2Fvm1uI6mJFOnzFIUSNHNg383CKXkyOcmUjjgGDxGGKdIzJakK/OqhB8IUhXl4fpup4wG/IcKIXLF0lhR15uxs9AAlc5O3'
        b'KbmOp/07yvK7V1BAR9FINbKV827ZCuwovnerlyBSka1V/5aa7/DkJNqT8Xpgm3y/c0/ULH66DJXGCdetOk+i1HmKDGfd3U/zcWHAAN0dUOtG7yBdd6JuluvZnieTXvRr'
        b'G42/rmj89UWDOoW6fHriCNS8TWfRgrQi66BcOic0FtyHRjj2F5EHkEyKxlbVUO4UR+dYnRN2K3YQ87SjqZAeIRnHKRIdSnLRH+rmQjwHBeqhelejDrWj8WkTjY/eaAhA'
        b'UYtM0IkwCIbj+cZP52NqQCN9dNRkMlLjE0In9JKzXRw1u+5qUMgwqSLmqmd/uQk1ZLtRkycKnabCxkwZeklRXgbrzooGlrI1MvVpNlOqqOQzFTJ5+0zpE/d0iZdElOy8'
        b'5KcW0cK0lvY7J8MQ9OcQYQz+Eib6eCV1/jEf+pgPeUx3a6hgpawIyR5jZVlfPyCYU/QI/kI3tr9P9yg2ViKT5XqOlokUKMj28BwtRdKd7lGL3K57rMLx6B6fcAK6Byh9'
        b'KaNRaVQmEsLQ2K97aCJ5QzKbuONs6Ko8JMVKJIVYssDfSMDy1yvfpebNGSLEG8VIfkrHUis6gepcd6PihzDklz4lyhbiA71PpEkL8QuJQr3iHkU44zvpDxKxG5bT3X29'
        b'/f1RT9OdJwwxRhnCX3p7ZLoIlXY0GlT03URAyqiF8Jcw0V/3jewwp+JL1dOjVfDpIcIR6BeVhBN9AvTer361ySPaW3d661sFymafpO2je7DGYGwkoo0Ii0HNo3tETJWm'
        b'oQgjRqKkO3gjtWDV7c2XWddDW8Zh82W7THMmJRtYBFKXPdgTyDQ14yJBwvWYyAWVnuB98pBNATbgPC7iDk9x+9jNmAIHYT04DHZSiB6fD1YNxBi9elBDnoj0tWXcmLHe'
        b'jDAlRJI+iWL6QB3E3EEVBkwYrMGUGGA/2E9McPNmg/rIKANbNZCLQJ9BLVhGYushw+4xBTYcL1HwTccJjMITp78YtsAPXNHtmEhwPDYbBHvHRVM3SNjwcPVEuBUUM3MG'
        b'G2dkwHKCFzLLisFej8ZmzxV1/YddfmE0o8C+p+dZYkve9l6PcExj6XYEcXwEdoAW1TbfWlBt5jwzXZo6uwtffhcX+cu/lZQNzcLkhN9dHrenz9JPU37dtab8TtdG8/MF'
        b'w5yExQIHP4sNq92KC9Jk3KmhiT95n6oZOnxV8d3TAbdDLrR02yrcezPxxfaX8aVBYfsOi82lP94YuuvLic8aBRFvLpsrHL+Gz6q3n9lxf1aVdM7Gb8sfcvdV+nwRdTF0'
        b'7oPMxl9egnCTywm+aUumJH3d/clVr6ZRN0Man9xIujjd1ntuvLP06vKbAxaZlhonKr88+LfMIwt/XBTmuzR088mqwBmPM/vMN/z14wODlwWFNLZ8cTBz5DVfK+Oa8JfF'
        b'iX98bjWv6fsfLWaMHRPhHuYsoLaYB+CZBa6gJETTI7F73ATqbnhzJKxRc0fBPQEYJLJEqHJyvCvUFe6CdbB0fATYy2cMs7n9nGAFscLMASvBEdPI8Px2IJEceJLsGXmg'
        b'Ol8JVs8GG0SqfSNdm0ZzJNS+tNYKLKMuk4pBeavbJLXTpF6wmBpWnrbJVLH1tVL1hcJ6HjgIjoKdCVYRMbGRURGcRGOGO5HjssCmPbLD7C9y+Y3N1sgmFd6A1dqkKmLG'
        b'CwjdHp9jwXEknpPwb2xCaMJuUHGJAaI9+rblWHPmmam3YkRicYyWv47WpWpsSK6xK2X8Thl35mtE0uroU12SrA63pqr6aW5NaeWyY1gH8cKEbYqYFXy1F6a3sRel/99j'
        b'L+J3OPaz0JVnjqwd/kCYJB5jTb02iPxl8kSBAoOR1/IZ9E5wFsLjYF8rrGUaWAcPJseZovaYykydD8qoI4TT06fH0Wc4sIWZPAAemc/CTBwHUWfGB5O6ZHO7dKGxWIN9'
        b'PX3FfipMSqYxRTxUgQZY6puaoMawVLmTOHZIKVTFK32uUYWfHwWgPOxPTD8CvWxDXEYmzKcnP7ekKAav0UmhbuMG05MOQymKwcv2TFFNVDJlQR7n1tPfgjiQZ/qCDb3I'
        b'JJYOayHGp3gxqBiNGOO2ExZPA7UkFrdJlkxPhrHzmmK+8IWfkHXpUwOqwYo4PvhAG/MSR92BgGJ4wlEFeNkFaxmwwTKaJA83dB3gJvalaB+vSFL+KXAn2ICq4ASsoEAV'
        b'cJglLayC+4LVoBSKSFnsAI7KwRaStQNzcpjruNS8zwTDXORs1srhcjQQjoBl2oiUCT0JYoQ8+Es8hYd4DTw/7hcHG3pyop8Ntn4ReoWOiDko9KQn5QPPMYs5TODBwEWh'
        b'jQGetLeEgG2mcnNfVDwu2MOAbVJ4Gm6E+wnM44UtBZl4zeqbmWxvSrEfJkVs86Q/mqBwGUdPlvirmucS5ylqP3KS48JyQc/K4E5MFFF/G71ABT8uNjYWNU84Zs46Doq5'
        b'oIlc8gBloDkulsHozKYQuJiBxQPgcXLJEbWC+tIElFHsxMWAtE+ywQJ1fIaEsa8UCRk4/aez2ZoZXWOXWDiaIUid2W6BcfhuBi414jGiLNBE7m0wYHvilN0eqd0NGOml'
        b'D4p48mDUhuuL3HPWn4iBw21G3Xa4eKPXx0tGgjMPXJ1eMY4mLo2CJGevwTGZTo+zlt2/Urf8JRN+OSA2/+HkQTHbbT6+8vGLz2pm3/7Frfozx7+PuN104lDq1UtrbV7n'
        b'11RPn3jvucKn/NWgmPqRl5Z8FX+vWXRFuGlmxFVDQbZBt2W1P4WG/3rBral5QHnzd5+cmjx46yG/2hlXc3jRD4OXnapZv25wRILjGNdvk0bsbMy5cs9dmTDx4bmIiIBF'
        b'fQKjQ7+88Shv64Bhk3IcRNf+uaX74ZcX5tZHVDbG3apv2StbkXtm3NMem765uMSj3/OXvz5b7B2a8N6tV8OWcDzszgasu1FVOatLsGK3T/lTg5GJEbt8ooPuXthcZ3/7'
        b'xfXPQ+XTN/1+J2vmiIrJ3505GTr60+9H358Q9MPVHqKos6+Vng9qj9fxnox+0vjzc6NnsTIu2OVsU0jkupXhYJuGbYgcHoGbdMzzBXAjgQTEoNe2zhW8RzyKOEej6wLY'
        b'wgXrkYRYTVxloVepxRUJilEcht+XEwWXgG12RhTosB9ssom0gydY7kTqABEzMZLL4uHDtEkZVoJicAhJugeIGU6hB1ft8cF1qgZ+RTjKwHiWN8XANIMS2EjhK8TWBpbg'
        b'rB5aSJER+8AS7FOFOFmFS8EyFsCChqJtRDDKM5NpmgPNgE2sVRGGw5IEFMNBCQuxgaUzp1OIDSrBDpLF3nA53MPaClnCHSqMC7UVklqQ6skpGNdK+OnbC8lsJ9gCIqF6'
        b'G6pVNbilKziIa8ICLOWNgM39CbZFAir7qanMwKpCFbalP1xB8idbNFYVQXSgAqN2LRbywn3BLlK+uaAZA1GwtVARC2thjYWGgxoqcZZIF6iQKsQYaQMf1MrgcZI4WAyL'
        b'EyPhAay9aCJVjEExBSptACdgGbVYsgfH1GAlarIE98Fm6g+xZjQoVdcz3DOBtbxS210V2+r0XKdfnstTyXO57eW5fCy/saRsXCsuhQxYsTheDCixQvJcT3TWCsl3rSSV'
        b'VuwflyVzM8G0lSzQxIqFDmDSF5Z9jUhW+gneOi5aO6o3LMz1bCvMLWZqtX0utk0UxYN5h/5ixrfM/2d8ayf+dcz4ZhRDKNwS0FBTrWJ824qkjjXOHTK+jYTlBNoLqqxj'
        b'KIebG+YzgDWEw80LVhNuy/kB81yzwVKKYJXBvQR3m5uAlcLjruO5DGFwgwfnSz8c+XeOHKsClz4zH3qZMLgZ3MkYZPBJnV0gkyq+z0RNZ9Y58bLXr/MRdrMb4mg6I+Tc'
        b'JwURCaU/vv/4xd6PYEVC/cWJ7wf968w4/221X6//YvWRn0qEI/Y9NV5wu0Dpv+Xw35zOh2fZchYJr3/rM0x+P5P7yiffCyx7Hd/38kjO3VnZRWuVZ5/eL7Ctv/Fvh6+T'
        b'lsrmB01wiL8+7e7ns95zU6b8PvhoU7jBil6/Bda/Se8TO6PoyyyfF7d2O1sSVwlJLumkwrAjgErC3ebajc4aS+GOLLMpbcjbFsJqNzJieaERbYcGJxvcC8q5PcODqMeA'
        b'xYvAScrK1srINg9NVafgrjHkDnOkJJ+gzG+trG/T0TzSAJbxaBw1aBKqIbxtraxtFWADrIJrOCQLHnAT3KNB3Iak+Hqui3cOhdA1meOpUk3dBipBA/VfvCiB6PEFw0I1'
        b'SNt6gRZuf1AKy2jaO8F2cFbN3OYTTLnb0BxUCg5TTX/9TLBHg7kNzT+nud3RzEPnQ6RYL4E7Fmrzt9UPpzULV8CVgZqsbaCOx7UD68ByWvHLwOHA1hkZLnUniFW4lyET'
        b'mTM4aKLB25blzHXrb/qX8LYREjAyjru0H8eLGPd++qnb8HD4l1O39eGrXCsvbvO51wGJmyoL+kjc+BTgQ64TsB+XJo6/Ypyt20L7sE2cBr6vE4arhxni2b1QkiOnAL02'
        b'BGtd/qNVlE404zEU9OWxyysCQz4XTbdcW6fO86nhBrbjCGdbBxNNrQAJPVvkEW7mtqy4asCY2+N3cVugMydGKlnmx5M7oGnqcHHBqLIWpBhYjcq4NuvbMdYXS2/3dawb'
        b'cdEo1uqkzdSmlRu5N4Xrlx8d7J98ee+h4a7TgjO+u3Xv6U/3bmYsTLH56sLcYTeCC0f5BN9b8HLb3YSv+9i/Srh15XbtZut0A9GblOrHSVs/kO+54/Drjtp/Jrgc3jns'
        b'mP23h56X7L8rzbLj1hacdy2be9nhluyToKevvggXdFG8uTN0w6lBwPc3e0tTt+A+kQ15jp4v1gKTQ+teVqzxbS7dt14QOXr07zFOv1WUjvl560JpYtkx8S+S6bILfrcP'
        b'XfzXwAuGiZdy1/p/37Tut9VbDdf2GnOlpu/TJecqQ92H/vHH1oJz+xv72zgNSLIfGthwzX7bpeqolhPZiTsdX153bI6NbOq91v55+LkfLN02pVumnnHmFeIlgjFiP7ga'
        b'CWacBcJABpYNX0T51ivRiLCOWs3nghNaK4NIe1tPb9rkb9HGNbond3hvdpXPYlH71TqH/55+9s4BGoC4qvesw4BgkQXJydl5InFyMhmAsLc7xp7L5XIGc4RowDHkWHMF'
        b'9kIbexebYTaDQvBwNFTAszAdWMTMkl1Rv1o8JTc5WWO0sf9fUHqO7O/qNxPnFA/x1Afxo+GaNHDE6X61W0+wGpTD8oDesHR8FJpuyo0Yix68XsawSepeeJQhhAEWF271'
        b'Kr1kAoZbGbRk1Nn93my+xCHs3IOKf5f0XeElf1a11ab292sfBU3uVhk4oal6oP2rHbdCnp1viMkquLDxzbWVB45Y237/eFX33Z/fj91+3fr81WMnnF0n7Oi2/8dfTmaf'
        b'9yr+MPaLlV6ZXwBQD22DHxd82GXQ858C7y1Z7Jp7/J7380s7fzLefvZ1RMFLTsMHTl4Nd5EggUeJuEmYLbV0PN6mWBM5Jd2IMQWHubA5Gp6gc2pL3sjI8e7wEL4HT9hd'
        b'mDB4CpNOvQc2ElCFKVwaT0sPtnOxZoJVYlR8a15vcCSYgDqQdrNufmREtEu0EWPIhyuQGiTwmExVqPfAQbAcrvY0ZDhwJ6iNY2AD3A/OUOV4I6hWuI4zYDigbFIkA6uw'
        b'Q0SSLQsf2ELIA1F6SLUrgbuRpOHMhevAbniM8sfChvly9R1RGOlhEsEFBw39SARJhqAJ6X5wH1gf4c76PbCAq3gxSC3bQiQNsDgTlrC7SPAo3ItdPY5HrzVp8eVj8W4C'
        b'ms7pLsxgsNGAMevKhUcGwWIiyMQHY81wlVs+uQ6bYJkBYwLe54IjiYlUr6uADZPRLYfNQDU4A1bOLlDA9wvMChQcpjss54E1SWG0AQ7aw5ORhFADlyYfNqIqB1u4cDvc'
        b'VURjWs4Pxg1gbugZiQaYMrxNgI+NGAdHPpIHD4O9Wo6ue/3Pv15t3zbjt4w1HQw9rZgZwlZrLqAuowhlA1ZUzXihbUUhRyoRkDGnj5KXLclV8rEBt9KgUJGfLVHys6Xy'
        b'QiUfa4ZKfl4+usyTF8qUBmRtW8lPzcvLVvKkuYVKg3Q06KEvGbb3wHQw+YpCJS8tU6bk5cnESkOkIxVK0EGOKF/JQ+qX0kAkT5NKlbxMyRx0C4reRCpXgYOVhvmK1Gxp'
        b'mtKIwqflSlN5pjS9MFkik+XJlOZI3ZNLkqXyPGySqjRX5KZliqS5EnGyZE6a0jg5WS5BuU9OVhpSE87WcZQWtJfsKf79Aw4e4uAmDv6BA7w5KLuOg3s4uIUDTMsnu4OD'
        b'b3DwTxx8hYNrOLiPg0c4uIGDb3HwIw6+x8FtHDzGgRIHX+PgKg6e4OAnHDzQaj4T9aD6MlxjUCXXXgvSsZ12WqaH0io5mf3NTjav7dljpAWnzRRlSFgQukgsEcc4C4j0'
        b'h/l2kc7L8u0S+VBpgmpcVijHWrLSMDsvTZQtV5pNxCajOZJRuLZlv6jqrQ3YQikIyckTK7IloRgsQZYa+Fw+V9C2iwXYEFcJ/wXMafvk'
    ))))
