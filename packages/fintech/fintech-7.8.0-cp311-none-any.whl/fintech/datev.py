
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
        b'eJzsvQd8k8fdOP5oeg+QvLF5jKdsS96bZYb3AGxGDMTIlmwLZNloMMwI2zJmGDDYgAkGDJgVzAg4hCTkLm3TbVGlUZ3kLW3TkfE2TkOaNm/f9H93jyRLlkxIm/bt//P5'
        b'yfLpnlvP9+6+d99xd9/7DWXz4Zh/P9uDnG5KRlVTDVQ1S8baRVWz5Zw+LuXkI2NfYFHUFZblWe0p47ApOe8C8l+xplpHaTyXs1E4X8a1T7+DhUJd5ONKYVEyXiXl1iji'
        b'f7nFfV5e1fwldFOzTKeU0831tLZRTi/YqG1sVtH5CpVWXtdIt0jr1kgb5BJ396pGhcaSViavV6jkGrpep6rTKppVGlqqktF1SqlGI9e4a5vpOrVcqpXTzAtkUq2Ulm+o'
        b'a5SqGuR0vUIp10jc66bY1DUU/XvgBnofOW1UG6uN3cZp47bx2vhtLm2ubW5t7m0ebZ5tXm3ebT5tvm2T2ia3CdqEbX5t/m0BbYFtQW3BbSFtU7opfYg+QD9Z76p30Xvp'
        b'uXofvbteoPfUu+n99JSeo/fVC/U8vbc+SO+v99AH6vl6tp6lD9ZP0U+qD0Xd4bollE21h9g38ZYwN4pNbQ61D0UhYfYhLGpr6NawSipiwrj11AbOM9R6Fmp+dnmdbWcH'
        b'o38BbgC+GUMqKZF7udIVPU0r5FAYQZL4rCzxhgBKF4ke4nJgB/prryhdCPVwf4UI7gfnQG/R4gViPhUznwtf85OJWLoQlBRcAjfcNUVl8ADc9wxVBvexKPciNhgE+6aK'
        b'2Do/lCICvOoDO/NLihKKeBSXywKnwb0NOtwn4Fozyn4f7MZxYtgO95XxKG+4l1O+EPai3LgP8+HR6aAD7k1ogR21bnAfKsMd3GKD21XwVQIr6KyvgqfBZZTopifQr1+r'
        b'g7fWeq7VsagAeJAD9oE2cAXBOg0lFYOzwaADHEwsEceFe2OI4UH87EKFRHLBTtAfVMeyabUQS6tdRs7R4DbUcqiTuaiLKdS1LggN3BACeCAE8EKd7oO6fxJCDgFCAj+E'
        b'AAEIAYJQ54fop9SHkM5HI6bdZVzns0nnsxw6n+3QwaytbHPnO42zdv6u8Z0f4KTzQ5nO3+btQnlSlC9NNys9Z82lSOC8RQxGDLo1eh7eEskETuO5Ub4IS2Y3ajyFS0VM'
        b'YPsaHoV+6W0NmzxXVzxHXaKU7ih4VWYg9/Fkavao4K/K37LvJJ+Xl7KUbigiJa2HNehC0YNBq1LeVe9afZgiwa/P+syny4cVO+r/e9ZXy94IWEKNULok3LU9DfAUxsTE'
        b'hbGxcG9ioRjuBZeqYovhfni3DB5MkBSJi8tYlMrHbQY8Afvtes/DUu29uPc8zL3Hs+s5CvddvYe1d7j/8t5xGJouTnrHs1yNm1fnjxx4EfY2VS4SL2FTbM50eJRCLXIt'
        b'QYezgF64X1XJRiOMcgXPR4B2eEsnxOED0+GdykVsCmH4OaqRmu8CnicZGn3T4RFELRIpcBYeSwSvgG7dZBSeUxsJj6C2E+PwV8TwaAEpZ0orXVm2EO7nUexN8yNZU+AQ'
        b'eE0XhWG6A3ZuRP2yL74EDaH21q2lC2PBpYRCMj1I4CUe2BHgQ95YArrBLXAL1W06BYbgtenTfBTzQoLZGiPu9wc/PfmDGae2t585cuvImqAIDlxN7ylK3yZ5YXLWye2s'
        b'lT/fHf7njZ4CzlzxXHGdVx1nuXtdzFKvnV4LLrQFNAYXeNXFfJHS97fV0T0Hpv1CeCH4u7zC+mmz3TXuHpc/jMvoPLVA8OO+6Jvnjr/pI/z9C9J5uqAVS+mqgOUxlcGC'
        b'E+VyZc7aof3pu70WZ767J3rA60eNF0q2lbrUrtOGtAxpg4xTjpUv8ewuZkPPn8xdG5Dr/bOfHBuMuPRr6sSPd/7Re8Efzu5NS77QIln1er1P649cUlvuUNTVa4Xz310v'
        b'4j2eilvoMugUl8D98fA6uA73l4mL8eQ3GQ5xYBs8t+gxnlroHHA6HuwC54rFUF9UWs6jPMANNjy1Begf4wm7sBUcjJeIiuNhe0IZmRp94DZO80rQ/xhPnhtx+ksJ8AC4'
        b'XKgTx6HhwaYmwXsccE0A20gB8LKwBPXSXngQ7kNDOhu+mM0CN8A1cFrkNcKOFanRgKb+QUfjhWtAbxv7fOk/vV7d3CpXIRJMiLsEEWb5upkjXmq5SiZX16jldc1qWav9'
        b'IxuX1YBw7y/bqNHNLMo/uLOqJ/rQiq4V+vz3pkT11RumiI1TxKOUt9d8FuMecu1kdaabBIGdM0z0tM78nuRDRZ1FJr+pndV9vD6NwS/e6Bc/SnlMms8y0dEDftdDL4cO'
        b'aobmGUR5RlGegc6bMIsbyRLRx+mbf8a9331cugHewPrhmEyDX5bRL2uUcrFP/Dad8pBOGUwd4hjo6UZ6+viXaA1+CUa/hFGKZ803t2/uAO9McX/xGZ9+n/Ev4w402ryM'
        b'QzJFXfQ+6z2wzkBnGOkMS4bfBkcMR6YPcdHf4pc87nsYIucagucZg+cNC+eZBP7dWYezevINggijIGLYM+IzPOeo8aQj8h7hM30w4lJTo9apampGPGpq6pRyqUrXgkL+'
        b'QcTwxhTADjPUk3AknmjGdf4snL4HOX/Bvb+JxWIJR6lvw3nkHaBXtK/Zt2abxyibxxKaPCbrM9uz92U/4vpsK9letqtsW5nJ1cfkKtB7/GWUR/F87UO3VTB/GkyeTrml'
        b'Ure881gcu3nbynTXYvLC66bkmOVGDLeMVc1B/1wFVc1Dv3wZu9pF5qan6lky7i63alfi4+1yrWbC+MjnjggRS8+u58hc0JMH4SW56MkVPXnKWIih3iVyH+EvIo1WTnrv'
        b'g6/QmKnj2ADEtRCSrRggFsPmduOCKVI0pnGIw28fx+Fv4RIax3GgcVwHOsbZyjXTOKdxE3MgHCc0jstwIB88i1iI0o18avaq0jOTFlKKmcNSlqYexfz0Ja+TP5h+6syR'
        b'7A4WP+eZSM69X30cGE2fzn5+0nev8y7Jdnzqn5S6ipXu+cNtHy6Fn/cnLdmuTZn2Ual0QKqUzzFxbnMk3W6/vvFA3rP3jdzjAYO1ty4dcXsrOr/vpddX/eg4n5LXCIM+'
        b'+EzEJ3PxlGlgIB5xhY3gVYYtjOdTPuACp3WBlkyl4G4KOIYSZNXEMfEcyjOB4wK3uz0OQtFeiDu+g+ZarroU7i8S8RE93sve8Bw8+RgzXwF0MCaWLrCnpAhcoyh+FjsI'
        b'HpjxOBAXfPG5OtBRAfTgHuKBuRQP9rLgvcyZJGPhGtAXL4bHVhQS3tkV3maDXexWEW/i0cezTMtk0I241tQoVAptTU2rD4M9EksAmXh1FDPxatlUQtLVGUMBxvg8g29s'
        b'J7fLs2e1SRjYVfK2MOqhMKpvtUGYbBQmD+YZhOmdLFPYtN41A9MGkgem9TajxB6m0Knox90kCEDDb1I0ytldcrikj2sQRhmFUcOW7ygHRZIUaoF1GuKPcDVyZf0IF8tx'
        b'Iy7r5GoNEvnUWHJQ+1vrhTFn1So8rzCzCWbnHeq0HKdUk/mEzCgaNosVjieEiZ1va6b4DCNzt5uYuuady6ljOxuXrdZxyYzKejYZk2wnfCfHzQkn6ThK0bhjb+WYx6TT'
        b'uIn5TitYdmNSF4ee0hdneyAOuwNhekciPFhZCDswWi9cQLjQWfAMvA5f40/iwsuKjKTP2Zp5KM+dK787+YM0NFrPHElG4/UHgR27int+tWLPaIDwu+V74jL4e+T7PD2v'
        b'BEnPlu2bPaM06b/YkZ+7DrdfiOnZnhpK/eWhx4mfHxBxyWCCA3FAX8K8kxlKzXAXe0O06+NwPGAOlWngLSQrHoQHJeIWcRw4Bu4R5id4KxfsTl9KRs4zaeA1NKyKEuA+'
        b'rXVUhRc9xmwt3AduwKMlS5MrxCyKvY6VVweeF7FtxhDuPcsAQhSxQa5VaOVNaAxNtuKbNYwMo1zzMJrHoYSBPdreTcOCOPR9LzhqODpnqMoQnWcInmMMnjMsnGMKCOlq'
        b'7d56eGufzBAQbwyIH/aNtxkMPHUEfitXJW2Sjx8CPDIErCNAjEeAE4hwL2uUzCBAMM3lsFiBGNWdOt8q+h91i6eueGdz/kPJUsNTDoF4jCPn4SvPOR0Em+Hz1nHAnySB'
        b'BxTPf3iXQ8bAnqDvMxRr3BgYPwI2ri3bd6p09srSpK0xO70KxXOTOA3B1McS95/GLBNxyBiIboS7Me++J9aWoCyFex/jiU8JtiOCscvdbhyMjQF4OJzQFrGvCo8BNF6P'
        b'jZEWeM5XxBlPNTgE48dQXuME5TV2KJ9tRvnyp0D5CExQ3HvSDL70MPnazv4E4dUS/GLeOqlS54D242f+dHu8t4LVSNlP/mUI8adiJJ/Y+bawXx2NXut80idYz7FO+lj9'
        b'QNVz/y8nfp4TrOeVM/qWXtBejnVxVVAvFksWFhYvhvqKStAJrzPyfSFsL5WwKC18xY0/H3TpElCmGrBjve1IgdtBlyPJ4E+CfbBd0ZC3l6VRoFzJs8+e/EEKkf1fOnLj'
        b'iCJIQKT/bbVfTc7nZxVKV/D/+rv3r+3pSEtel3Iv6Y0f/DzFmKS9KXv9Oz/Eo2rZocfJbyVV3UhO6vvoj4c4H9bu+TRgMGkV61TjupSU/iQuEchFvcLLVBsSyMNw1brD'
        b'i7C4jEVlRDF22YjL8MpSRh6Hx+EJK92Bt2EbM+rgeYrI9AJuBhpw+3OdjrkMmozbZeAF+CIhPEXwQrllzE2Fg4Qq1YPnefFiwszFLDWzc5ng+Nfyc1YhaoSva8FSdauX'
        b'Gf+ZRzIit5hH5DIOFTits7UvcoBrCBAbA8SY4cpjvYfFxFmG4NnG4NnDwtmmKfQoxZ5UwGLcznmIMPWl9ecOB0jQ970w0XDczAdCQ9x8Q1i+MSx/ODB/FJWb+MhX2OX+'
        b'tm/4Q9/wvkiDb4zRN2bY8rUZ1S7MqMbq2XHD2aZqLpSZnlkkxJl4ZNvXrAknXEdZiNnSJxKzb5+sMQPbVqtoz81xiFaRaITNpAxrETn/fi2iM1LGKVcUlWazNXhizM75'
        b'LSZN4bvDTx1CQ+78EfGOHyISdSw5Jelq/a5PLy8LClwdtO1PLYd4pZ7LHqTQz3r9/qWkNy6/Qb31VsrPU8JPvrIt6OR/BedX5a45vqZndeDqnqZtH4ct7vufZWuGV/j9'
        b'6MFxb+pqkLDKEyAWDlMeeH+aV4kLGvEdtuSrfAOjltoDX85jxggzQMAOMATvFcErZJBIF4TBDjR89ov5FP9ZNrwN9kfowACJg7eei8SilFWO4muDKNiN8O0pFBMY32ja'
        b'RjhyQdRDq0ZEznuMmuBnMpyazcOpkUOFTO3x74tAf7L+NYZpKcZpKYaglE6+KSKmP+ftiNSHEamGiHRjRDoeStHEOVTSOa8nyhQ4pdfj7UDRw0DRQKQhMNEYmNiZZ6Kj'
        b'rKqegMjOLX1LDAEJxoCEYd8ER7I44dghRNFm6MzHQ2dcNbBwp2mhzNqVBjR0JuPBMbHzrY2aRFwFdrkaz4giLyyEYn62pmbEvaaGWeJDfs+amrU6qZKJYRgA1zo05Bua'
        b'1RtHXM1ioEYdRaa9eoVcKdMQqY8wvoQLIBMGqfrXzaA2aiiMnq1mVUoljn+D6WjL3yNBgB5PhvpCU0AQcvyD9QUmvwB9/iiX74V6dyLHl+OVMEo5cdw5XiLsc3Dc+V6x'
        b'OO8THF+eF5q+n84h2KMjo+T0TLDNo7gMHkgsZlGuWtDhyV4lC3LgAvDns1V4HmONU1+xq7kyjowr4/Wyq3lsqouS8fv4lJOPzMV+/df+qdpF5kpWg91G+PNViE/b+KVw'
        b'nrxWoW1Wy1WJJWq5jPF+4EsQ5gM8i305eYlc3apr0LRIdZq6RqlSTqeiKAzvl56lcm2rVk7nqxUa7SU2wa8PvouG6+fHJ1NUSbNK25xbjvCJjs2TqeUaDcImlXZjC71Y'
        b'pZWrVfLGJrlKlGvzoGmQNyBXK1XJnOZTSbXwvlopoRcgbGxGeZc0q1VPk85ZYWvkCpWczlM1SGvloly7uNwSnbq1Vt4qV9Q1qnSqhtz5i8WlGCj0u7hSKy6SlasluXkq'
        b'1GDy3CrE7ioT89ZIZRK6QC2VoaLkSg1mgpXkvSrNumY1KrnV8g61NrdSq5bC0/LcBc0abb20rpF4lHKFtlXaqMytQCnI61DLa9Bvq84mu+Whdj2GDmtvaTMgKEhCV+s0'
        b'6MVKG+Dp5AljUnJL5CpVq4QuaVajsluaUWmqVil5j9z8PjldAO8rtYoGel2zyiGsVqHJrZIr5fUobo4cychrcLmx5iCRJY4ukCPcgf31Wg2uJW5Sx9R0Qakod764TKpQ'
        b'2sYyIaLcIgZPtLZxljBRbr50g20EehTlVqL5CgEpt42whIly50hVayxNjtoIP9q3Gg5Zg3FYXK5rQgWgoFLYj9Xla3CrMc2PAovm5JXjOLlcXY9mReStXFqUXyWe24z6'
        b'xtz4ZCwoVI0I13A55mYvlOpatGL8HjS91krM7zT77drdWThue7tKpDhUIsWxEinOKpHCVCJlrBIptpVIcVKJlIkqkWIDbMoElUiZuBKpDpVIdaxEqrNKpDKVSB2rRKpt'
        b'JVKdVCJ1okqk2gCbOkElUieuRJpDJdIcK5HmrBJpTCXSxiqRZluJNCeVSJuoEmk2wKZNUIm0iSuR7lCJdMdKpDurRDpTifSxSqTbViLdSSXSJ6pEug2w6RNUIt2uEmMD'
        b'EY0ntUJeL2XmxwK1Dp6ub1Y3oYm5RIenOhWpA5qN5To0jZgfWtRoQkazn0rTopbXNbag+VqFwtFcrFXLtTgFiq+VS9W1qKHQ4zwF5o3kYobc5ek0mKC0Iv4odynsb1Sj'
        b'dtNoyAvwrMfQWKWiSaGlY82kV5RbjZobp6tFkaoGnC4f9iuVigZEo7S0QkVXSRFdtMlQSfoAxywgS7y2hY2RcXE1ggJNGLE4u12EOT+KinLMkDJxhhSnGVLpOWqdFkU7'
        b'5iPxaRMXmOa0wPSJM6STDGVShi6TNkd8CeJPSJhWvkFr9aCZyOpNtU2qsSZjOmKOHJHjBpuAqNxqhQr1Bu5/8h4c1YqCMOlFs7TdY4r9I5p+pBotonZqRb0WY029tBHB'
        b'jxKpZFIEjKoWoa21x7Vq2N+AkKhIJVOsk9D5DP2wfUqxe0q1e0qze0q3e8qwe8q0e8qye8q2f3uS/aM9NMn24CTbw5NsD1ByuhM2hY5dZG5VjZnREI0xRs4izbySsygL'
        b'+zRRnHUqcxJf4fxtmO9yFm7Hik1chyfET8SdfZPEKRO/2Y5Pe5pkaKp0lsyOBGQ4kIAMRxKQ4YwEZDAkIGNsNs6wJQEZTkhAxkQkIMNmqs+YgARkTEzHMh0qkelYiUxn'
        b'lchkKpE5VolM20pkOqlE5kSVyLQBNnOCSmROXIksh0pkOVYiy1klsphKZI1VIsu2EllOKpE1USWybIDNmqASWRNXItuhEtmOlch2VolsphLZY5XItq1EtpNKZE9UiWwb'
        b'YLMnqET2xJVAE6SDrJDkRFhIciotJJnFhSQbNiXJTmBIciYxJE0oMiTZygZJEwkNSXb1MYOYr5Y3yTQb0SzThOZtTbNyHeIkcivnL8gTE2ql1ajl9YgIqjDNcxqc4jw4'
        b'1XlwmvPgdOfBGc6DM50HZzkPzp6gOkl4Ql+jgvdb6rVyDV2xoKLSzMBhYq5pkSN5mGEmx4i5TaiFfNsEFchr4X1M6cexDQ1MuJlrsDyl2D2l5i4wK1dsMjuoXZIdg1Ic'
        b'g5CYo8RCsVSL+VK6UoeKkzbJERmVanUazNYytaGbpCodIi90g5xBU0QOnakBRDZZFJi4K2Qk29cmdlK+E6LkvGzHhETFNNY6NGK+aTPLS5qyHsebG5nxp9j4sUw4pqn6'
        b'kpVbfslVnY/VjwXYKaTMS57qIuwUYxUnT9OiVGjVJVgTxmI0l1iPZtZalhGtJaNDwws9msXjtZYirLUM0heO8in/RJNf7KgLN9B7lEIOCnOn/EM6F49ykybNZX1Ry6J8'
        b'hHvlnXPbV+9b/WkDK9U/+DGFHH0+/mPUiGTPUzt4LUOD97C2J4BLXMoVXvXLYG/1BMf/TzWJ7nl1dc061BKqhhHvOQjdGIlH2iJXfuDH6BGxCv3L4HkIAZsQV4NV4jQj'
        b'c6Hho0CTHkqCN/aNcDH3pa5C3s/vo4DFTQwz1dyoktOVzUplYiGaDVXiklas2xl7HJtfc5eWVNNMNqzDwzO3RqHRMQE4zvaZGe8FWOXIyBbMi+YsFlfWNSrhfYR3SsQP'
        b'2T7mzpEr5Q0yXBHGa1b4jPlTzLJZrqUliKyBmVG5eVqxCIw0w5CZxc4xBZlZ4CRiAhY1UWI0sLVEJDGXQF6nVKAExKdQ1TfTYjpPrbWAYg4pUuGc4wJxshRnyVIckqU6'
        b'S5bqkCzNWbI0h2TpzpKlOyTLcJYswyFZprNkmQ7JspwlQ/xNRWVVMgooYToG89lyEpjiEIge6DI5mqstWmBaJ6HHtMAokMFli1pWQmNZwSLxM+resW6kS+NLc/N1qjXk'
        b'HJVc3YAmx1Y8oeHwOYvptGyGxNdbkmB1tLNwM94wUU4KzK0mogiuuLpJiiOtKOIsxooqE2VLeVI255EMCj0hm/NIBqWekM15JINiT8jmPJJBuSdkcx7JoOATsjmPZFDy'
        b'CdmcR+Js2U/K5jySdHfSE/vbeSzJ+GREmRhTkp+IKhPEkoxPRJYJYknGJ6LLBLEk4xMRZoJYkvGJKDNBLMn4RKSZIJZkfCLaTBBLMj4RcSaIJSP+iZiDYiu18H7dGkS6'
        b'1iPiqyVM8Xq5QiPPzUckfmz2Q9OhVKWUYr2mZrW0UY1KbZCjFCo5ZsjGFJ1myoknvDxdPVbJWSc5Cy1FUXjmHSPIdGyeqpVhxvFaIpqMyxRaRBrlMsSBSLXjosfNw46Z'
        b'x2by8XFqJbyjMbMJdjGFZGWpXou4EqtIRyiJmPA7TuUPc03N1ByRfkRpMPteTxj3JkzgtXIFahatVUddhLhsraJesUZqO/tXExHUqru2ZTMYwdVmDdOWTcqXM1KNXFGL'
        b'o0pRr+FFOQ3D2UzMqNnqpRHc6M1Spa5pjbzRokQnRJBwcUsRF1euXuacfcYbw1ttGMf7OH7ReBY6woaFzjT50U5Z6MBJ079IsWWgM0Mw/xxizz/T+IWgC+zVlJbDA4mE'
        b'iYb74CXYUeJC+dVyPcGriXZctKeFi45mIy5aaM9FI76Z3+XR5SFjdwm6BJifvsq7gJjcKy6W7G7oTxap5+m99IJ6jsxjl5v9/qFqLj7bLfPcRcm8rnpfQO+4Yt2uWM0n'
        b'cT4oztchzoXETUJxkx3iXEmcAMUJHeLcSJwfivN3iHMncQEoLtAhzoPEBaG4YIc4T1y/erYsZJdrtZe5TQTj/tyuTrngjnK527VMlJ5tbhuuLNShbbwt7dvl3sWqx23s'
        b'QlxLiWEXkHBwxW2sRFm0ntnMiU/++qJSXWRTHUr1kcWgVDy9KzkhPJmkone5VfuisEmoFuGoFpPImwVXp9lLO+ZTxt56n3qeLGKX67iSJxNZaJcodsR1Hj5iN7dyyZeJ'
        b'7rTNxxJMMxMpc3TeLsUlnnoBHhl4EHyABTL1s9iHt3ETgUjk+QEG5wPc+h/g7cFjydUNluRqvLVMvQonwe39AT5y+wHGZJHLiLtUtg7NzeoahWzErQ7NkCot9npLmUFY'
        b'o0QsrrZxxLVOhyYPVd3GEVd8hkMhVZq3/HjUKxBXW9OEJq5G8u4RzvzFi5g9RWq8g7TOlRr74NeT/W/HKMt+W9sz/uToLwshAVfvghqWOfjLr3cnW/YQGre7j9uy50a2'
        b'7Lk6bNlzc9iW57rVzbxlz2mcdctevYj9OT57a9cL+FPEVFvRKtcQCwnWvlOQnSl1colDFoeAHCTESZvosSbPMdtGQBM11ueZjS+Y216q0jqUgD+xc9D8qrXM7iIJnYfz'
        b'o5m4jiY7s2ldC43oUSYtUzQotBpHuMxgWHvbORRMtHMIrKtWXwND+tfBYI9mOXQp+cUgFCSWWmLNgGmcw4KpN6abiOpK6KpGREnRaJLTGl2tUi5rQPV5qlKYLUGMyI9K'
        b'oqWoCPTMwE8rmxFVV0voIi3dpEOCX63caSlSc+Vr5dr1crxqT8fK5PVSnVIrIqYxsibuC/PwyqHnmn10HVb7xloXi23UxaKJSrEMzRwLtmqsnYktcTSr6Vhm69EaeF/d'
        b'KldOWJB5W18OkVkxf4eKYXDEPFPFyhskdHpyUgKdmZw0YTE2c0MOnY8faPKAi6tXqNCoQTDSG+VSBFicSr4er1yvy5CkSZLjRI5N9bXb4z2Zs4rTRb4U7ZvHolpWlX7g'
        b'mkHp8PnVDbAT3oQdZeDqAqgvgvtLEmH7ArxrvrBUBDsSysVgLzxYurAQXCssLysrKmOBnc0UPAT6PJvhKbiLFDwrz4sKnPIum1qwynPe5gWUjmxsDElwWiw8ANtLEUMB'
        b'2u3LpeAucBu8tNGTAnfN5SZUuFG+gbNZ1KpVyoKC5xjbHir3irGj+6gAiTiuGJUPXuBSGR7g+gq+xs2NmB8gRZxS8inPKUVsil6VcHgejwEN3gDnmxng6sGr9vBBPSq3'
        b'IwHDuE+0xAY88JLaA9yEr/oqYOJsrqYPlfNifeD+g7neIMlz9n//rZLv/T3WPRl1j37DzbSZemPkUklie+obsVPDp803aM5+0fX2Y/7e9xtiOzrdPET093J9VdPfkT9b'
        b'Cb7z/mdbNy+blLfo8ysxh2vv/vHdDy8u93nvguajtx6sarr/xSef/C3h2Lsxz/l9BVX31hl2vvDRvT/v+f71P16/0zwCynI9/z7l5XXr+J+GXFj2h8OfXNjrXbtD8MZn'
        b'LrAideoUjciTHAwoyIkDHdhmiOXop09rShSnHtwCz5ODAZvgrQWgo6JUVCYZ63EWFQx3clvBdd1jbMYkELRFeKAmB/3ZojLLcX0/0MZ1FfPIubYNM1FkRwU8AHZV2nQw'
        b'i/IP53qAe6DjMd4HHLAQno8XxxaK2RQfXggBJ9hieKuaQAG6YRt4BRUx1qFKITUZvMCBHVLwAtk/rQG9ofESEdybQKH8Q3JwlZ0Ke1gk/9oIeAR0YFsB1u7jCxKoyes4'
        b'4JUmcPmxCL/jtQDQjqtaDtrALYaxxWCaEYCikuBuvgR2TX2Mty+XwP4UXKWOhDgJSnVTiArfDw/G44S0hucFdzz3mEbpFoB9CHdRQqJqRq8W893AAQR6NwfujgKHSGHg'
        b'UgDsIK+uZo1x1IibDgZDXAR3Nzgscv8HjqtjzmH8UXVyuHSShRDbH5n1MtsqWOdCheNzTV6mCHEn1+hLmwT+namdmk5NT86h57qeMwhijIKYgfCHgvhhQfx7wZHDUYWG'
        b'4CJjcNGwsMg0LR5l9RnLkn1oa9dWgyDaKIgemPTQfJQKZSkwBBcagwuHhYWmcNHFsLNhhvBkY3gyyuzNZNZas9m+KdMQnGUMzhoWZpmmxfVJBmrfDs98GJ5pCM82hmc7'
        b'y2z7znxDcIExuGBYWPAoJh1XLdIUmYh/w03hESRzRBSpscNhLi9m1zreOq/GG8/Va7GDz2SpNdjBjJ1aSz1pYzs2K7HK/LHZ3z5Bj3yAswxQzJmvv5gPflW4sFh1LLyj'
        b'/dtzv1WDAufcsqmXvPNcOHYnS1gWwjOZEJ7N1GprFFn5YJWLWCMeNWM8HpJzcXMTOZcmzfSl63SltKlWJp1p01aWoEkoHXn9Nqqnyhgq3kaRnvvSTH/N5Vp4tVhE12Xi'
        b'ZpVyo+gSa4Qja677BsDWM8C611g5QUdY1W32XWoBU4iSkNOkGMzeGguUUxkomQKdAPkNoGtgoPOpsecRnx7EAPuWTLbAKHoik/kPQmtuS7caCyf39HAG2zXlsxYwg+ZI'
        b'NXIrY/jPgmVhDZ8erFCURN2FExBwIiZkKf8hwHYxgLnWmFnNp4eLxt1qba6VluaKmJBV/WcazrPGhod9ehgjcJeOoZ7EinpfwwRPAKr12NgG5Bxlm0+zWSwT/HvOsj3V'
        b'sWxOuUL08L+5Grxozj8fgk0N4KOjzEFryym2vpv7TPIr27J6tt/6wzUeVXTZVfLXhyI2OTINz4Lz4Ko9k4E4jEuuhMkAL8NbhMuAPbznCJPhwGLA+xAxYSlAP6GpAJca'
        b'PJPU1LT62tApEkIYB2xZAZOnYjcqMASR/LTemYaAOGNA3EDlQOWg0JicZxDPMYrnGALmDPvOcbAJ4IxkMiYBMJlkkKYfI43D26MxXq+hzOfAitz+HUfAyLTT5RZHXfbO'
        b'4ojcR1zMkyFzzouv0arlcu2Ia0uzRovF0RFunUK7ccSFSbNxhL9OSrRFHnVIKG5uYrRIHK20YYTXjKYIdZ2HDb54W/AFV/8o17l9R4TYXubz1656Hz1b744RXe+r5+jd'
        b'9C713gThPRDCe49DeE+C8B4OCO/pgNQeWz3NCO80zhbhP3+P50QTlCeTaZCoj+VVmbwWT4HoW2fekkzLyeaPp1AGEVUF0TNI6UZdg9xG/YLaW6OoVWIrmfg8HdakaORa'
        b'CV2BZgaHcvBc3IRXoxVNLc1qrDWyZKuTquhaOc5KyxRqeZ1WuZGu3YgzOBQiXSdVKKX4lURyxxvaNRJcUwVeV0Dzk7lIs/YDl+lQBipap1GoGghE1mLoOIIKcU/RIvnm'
        b'2jZiVagj7A7pY7VSdQN6h8wy4eP8NF4p0WBNgmatDrdurVpat0au1Yhynl5Bx4yCHDrPjjegl5O9ISsnyobfnEOTQ2XLv/Zo2YSlMIMuh64kv/Ry80bnCdNbBmcOjdd5'
        b'UFcRxdFy243OE+bFwzmHnotcenmFWjtxOmbAo6SMh7wjgS6qrBCnJmdk0Mvx2s6EuZlZIodeklclLppHLzdvmFgZv9z24NzELx+bXLB6jHmgcUG2xzUmzI6mI9SYjWho'
        b'oOGqqVMrWrRmNgHjKbZmRMZWnlLTjPBXLnOq2UPohFNjeq0ktmtJZ0voeYx6jwzRaZVaaVMTPg6vmjahoo8MBoRYCIAW89CSKYj1XClq1vUKxBfIN6AeNw84x3Lwp7xZ'
        b'K2eGCRn8cm1jswzNJA26JoRoCBbpGjQA0aCRo9apk9PNiMdyWg5TJTxoiN5Sw1RTobEBSULno0nNMiE5LcV22GEtJ0J1bBu4TokqzJgF1sid51xltgzcXEcgZ5aSpzdq'
        b'tS2anMTE9evXM7YJJTJ5okyllG9obkpkJItEaUtLogJ1/gZJo7ZJGZFoKSIxOSkpNSUlOXFeclZSclpaUlpWalpyUnpmavbMVTX/gE5xcrmOaG0OzsnVlIqKxZJysAcO'
        b'4nPv8eBSAkVFVvIaBQIdputgN3g1IRV5kqk00JdcLCKauVuhvNVhHMQGzF6VsCC6hNJhkyzgBrwIjpWUltdvZTiYhVAfD/eXFYsXYVMci2Kx8YqlUI9/EGMDDoPrbvAo'
        b'2CcjtnwjksFueAseIDoaF2omeJ4Hj7M9UUAfUR1WwkFwCt6SwP0lRdjiByoZ27ZkU1PZy8B5LrzXAAd1szEbdbIRvAZvqOCtErivbDHsbGGqaKneAqgvR3n3lSxuQU5F'
        b'aTE8yqXgXrDDA/aDe/A0gQZeha/Bfg+JKDG1GNwHp90pt2I2PA0OgnM6fIo7IA0chLc2wReKUBksigO6WWAbPO2tw0YbwHWwE1zygPpECWxHb00Al4rhPqhnUTQ8Ca8U'
        b'8LjgKtxBrJ/KgqrgrcQ4FsVemVLIygAnppP2dRPzYxM56EX0KuXN9R4UgakabvcEN8FujRc8Cl9kXuy6gl3Agy8zllFfhLfAfRzr5SWBh+CLpfBGPDzMoQKSwc6NHMSB'
        b'9sKzOmyQhA07wDkPCSoCNSE2F7KfEwhPUH7wJa7PbErxP5zjXA3AYOxhNQ2XuIPZnvxHsrAtsx6cev47yzfs3tYXInqh2GO+9hBH/84L9z49fCEidO0fZv8w839jgh42'
        b'fM7mXc367d+4PzwhfLBc/HJYDv3ul9rB/t8lbrph/O6fhFdjuoIfh3617uE7J7Xxn9w6/p7yhZ/f5aVcfSf26ivha1768U/uro3c2zt54cdVeyfHxBefSln4O9m8lyrf'
        b'+3joABXd9+szW28VVm+tjHPd0a8u0uVd3tQV9Pjwfv6SJW3fe/TT/es+X5EUzn6d9fB/XI73JcW+NVvEJ/ZKPcvl47SoURxwBFyph6fhsccYvQJcJSUWztusVQQ7YTej'
        b'WYxP5cGDBSuJMRcFYsaPYW2qVZUKtpUx2tRQeJ8kkRbA16zcvrePhd/HzD5qZaLWjRVGx5eLi4rKShLgfhFrlgflD+9zU+BVcJQoS3PBXv+ShNhJ4HghQnjUz+AKe2Ml'
        b'R+T7z9hNdaqDxI6dxUyriQp3qUxWw3B+rQIrYz8WaKeSLHWnguke/z5en7Z/iyEo3RiU3sk3CYJ6Eo1Yu5dikiR35vfMMgjjxxSPmYc2d202CCKNgsg+rTEmZ2ihIWbm'
        b'Q8HMYcFMogyc+6DBEFVmCC43BpcPC8tN00Sd/M71h3xMojTk2WrwjTbNnNPJHw7IMfjmmiLjUOBGA9YUxiLfukPeJlGyJR0diXy6Q14IImwkI8sUKxlQD7IG1FexpdVs'
        b'gzDKJE4dzBucMzjnajUKmWkQxpn8g4b9RT0rOjkmX2GX99u+ooe+ooGIAbXBN8Xom/K2b/ZD3+yhaINvntE3b9jytRGeJjHCE2bImR3XF7GDVYbqS9jBpr3VmFVXX8XO'
        b'Ney8MIG4ZdNjuHNWjX3oMRM96iEshDnrKxGWwyBlo6w06yvdvn195b9cj4kFsMtueRT1OuWd580RuY14yvD2eDOHO+LFyC2WR760ifxiI4/yETfzxqQ6+YgH5jIRb4+3'
        b'LTP9YO2COuseDvTxtZBQ3JNHXZwJed3EmjcS6PAyP4vYY3fTT0ICH7bXToz21/sSMc/diZjnQcQ8dwcxz8NBlHPf6mEW85zG2VpB/fygy5PFPKl1RxLNWMR9CmFmPj6A'
        b'yKSmEUeF8AvJKYhLlNpeh4A5yQS6Qd2sa0GxSICSOnIozU21CpXUwrPGIXY2jjBbDK+FFXHWExcYQKtKyaEkrGL6f3Lp/5/lUtuhm4M7igmxqrC/Rj61G+tMfibIUoBT'
        b'Jn351xyFmPB1zFzCvMc8fZjDGDlH1Yw1oWoiyaicyyfrm7EgoWiSKieQhJY/4TAIki+dHweZEGI86zHw1jY3r8Hw4hAJXWbGLil5pptrV6OOp5udC1UIQZBcnJWRlGzW'
        b'QGNEQEI9Lm752EGRCYGwTro59GKNTqpUkpGBEGdds6LOOhqX25wzeaJqwDxp23cDOfy+3PYsytcK7zj7OAHe7sTDf4D8PUe+Xt5g3q/6/2Tw/wAZPDUjKSUrKyk1NS01'
        b'PTUjIz3ZqQyOP08WzPlOBHOa2ezzyTyeKp8Rr5VnqwooHbY4Bu8tB30lRWVwb0KRRVJZOF6wvgd7iXD9HHjFLQ3sySSC41wkyQzAW7HNVumaiNbgDriny8Ql74ZXfUrg'
        b'NjAgKS5DIsvExRO5vQN2uIGLz8kZafvwVm9NRVmF2QgnLn4p7ESJD0J9CbgDDy5ucUcCKSoQhb1UuQL0ghPgnBsFriApqnxOAXMXT5+oVlMM9xeVVZQgdxPsWZjEpQLn'
        b'cOC+Fm+iqoDti+BuTVwZPBCLt3tIisC1WBY1tcErgMdbD3aSNJVgHzztAe+CA4tc4X5xOby+AknebGpyKgecqakjMjLoSGPDWzY7kJD0q54BXlyEbw9JBh28DXngJpGR'
        b'QX8VOG0GqihhJTwkwpeRCOE5Dnw5ooC5lyaPMzkNX0JDrVJ+5b+AIhI9uDRjpQfq0ioqFQ5UgU54g/QeOIxa5agHbiLUjofg3cJSfJPMEfgiVkZ0gCvoqRQeWFmE5D0O'
        b'tSLItQBcTWRuWtkPT8BueAt5i6iQiKL5kLlQZRO4C7YzmhlwG3QmLwPbdZhTXbBJY75oJTA/cQW4ofzL3//+97+t5bU0UAxGTZ5rvmwni8f3/G+K0TK8+mwCpZuLZUHw'
        b'ItyGW2e/WYVTmLAE38OUWLwYIUIh3FcZK0LoUMjculSG5GBwB7deA7hL8VVeK+G2HKIhSYZ3PSvhUXAQnE4t5lAseJWCV1PhPd0M3J3bZsALHvAyeAF3FOqlRVacWezq'
        b'pI1QusNcCrQtdnumXKTDRvjiwQvgFY3XSnDXogxZGAuPVrraaz5m+fG9Z8OdOrzJaXpxmKZYXFGWiBGovCgBHsrCig9KBHt44Da8vZaMFc66DfFYWdNPLNiJ+JQHeA1h'
        b'DLgFXiL3Bf13YAW7JbDdi2qRCt5Z1i70ZXal+WvhXXjLrO1itsoh/ILtiRVlC2MZa3jWDWml8GWyZe4UuOiJqr0fnCVXVSng/uL4Zr6kKCGORfHBQXZiPegkMfDkNKzM'
        b'wnoAtjoWnGZlQb2LiEPuyfH1zoyfEW6TCdz0IuhRB1/cbMnDW8vKCgFDzFgbgMfgC/HFi+DecVU8Do8rhhb/lqvZgoRFjnDxtUUl5TDJ9/PM9p/VnPAvFimz8t9aTquS'
        b'2MZi19175/9WaTo+oxaevaIaihRcLP/NqnXLih/X/+13X3x36i9ipG8Upib9Jn3t7x+4/rX+J3Hx+VNfe7ffZW/m7V9t9K9vTBoO/SrzLJj/6tGy1ewf9b88EPI/+WWX'
        b'3Ub9fn2h+k8+b+0q2vHW5KvRV1ZHzxU+kzZHeP3Dd99da+ie8vKHQXJ1zcmzbV+dWbj1q/Vy4w/BR3N/0Z5zf1WDe/yFOx2BrSfvFXO3PPaO++TIrjMwo+HjBiRjZiX9'
        b'6Zmo3aU/W7ooIf7F9Pd+uKrqdwWvb/ivd3WqP/V9KSibm6pyifH++cFVq3/9y+m/BMd/ejXuZ3NOiKp///NFHw0dbz9zNMtj/cCUmZdj02H34erfvX8cXA299osZiS/9'
        b'LrA7Z+qHmrfvpM/q6P9xjfuV3m0ds9KPN1/1/05j7hqFOsg0tO07oo53Nv733dzXbvzl8ncuvXXsxV+qUzaf+nD7g88DEnf7b/2lH/xE98uY7edyUxew3z828L2p9923'
        b'Pv7omsiLKIng8Vlqi9oqS2hVXNWDIzMfk8ls/+x145VWJXXw1JjOCgz6Mvvzdm+utuqswDZwaGwLIDgKXiLmg9dufq6E2b6XA86QLZk+SzhKsG8aiQUXEX3oiI+TiLIL'
        b'yBY+t2fY4PwWuJMxm/8aD7wQDy+AVyWYTiRgXDzAFm9Y+xij4hY0vPpKSuP4FHtltIKVmQX2PSZ43aXKB1dKI/zKEtgUt4QFbsLD80l5yXCIxjsBz1r37PE3s2PA7hBm'
        b'PX2oluwEtGzus93ZV6bgeS2fR5KBl0Gbu92CegG8b7NtLzuVSXYDzVLnNXhsijGpux3FtPQk2MkBg4ic7GGqOAjOwFMlCbGFK+FrYzq5pc0iv29bJzexsg63GuEktm1z'
        b'prHzxgqfMbm+NcBOEzQWQTR3d9iM5m6rBxUc2RPcN38g7eoMQ1C2MSgba+4sSrrphoBYY0CsQSAyCkQD84wJsx6EGxLmPhTMHRbMJWq6vAelhqgFhuCFxuCFw8KFpmkS'
        b's5rOWsYMQ4DIGCAyCOKMgriBKqN49oNkg3jeQ8G8YcE8UsacBysNUYsMwZXG4MphYaVpehHW62UZfLNNsViJt8XgG2Wj9ouJ79+C/JsNvpEmQWhnTo+sb65BEGsUxGKD'
        b'04mmkNieGQNCQ4jEGCIh5qVx8HwWsz9xKAL9yV4S3RcZomyuK4qJt5YY1JN3OKczx5SZ05k/HJJqEKYNC9MejT2ZQumeyj7/48t7l78dmvgwNHGQYwhNM4amdbqjSvfE'
        b'DQsi0XdAgP6q3xbPeCieMVTHbLB4kGIU5xtEBUZRwZvhD0Ulw6ISAlTpm62GqGcMwdXG4OphYfV7WblDBUMFD/LfXPJ6hWF6lXF6lSFrsTFrMW6VNINvOtFjsiZNN6Xn'
        b'YqCSDcKUR+FR/UGd3iZBQFdOH9dIJz8UJA8Lkk1RqYNSQ1RmZ7kpIBhb2A6TDHJvuw3NHPYv7uRgcCONwXGMBX1T2DRjmGRAYwxL7SxAybGOti/bGCI2BEiMAZLBqIcB'
        b'mcMBme+FxQzHlhrCyoxhZcOBZY8CQnoa+hpQzofEgLcpPrHHpc/FEBg7HBhrCgrtcxng9Xs/DJIMB0lMIjGK4x33/suj2ITBqge1w2FF6IvelpDaOc8ojOyrNAhFJt+A'
        b'Hjej7zSzyjXa4Jts9E0etnxtVKwCRsX6EnbuYedl7OAjdupXsPMqZVGxPqV2dfyIw68ar2u1qlt/ipwJB1k1Vrn+hLJTuaLhttadxVIQjei/1/1Wta9X3PJY1Oss7zwf'
        b'Tp3FBgf+WO89PEzZa0q7Kb2L3k3PJTcfsvWe5JopLz3LfP8hj021jzvwtIVPtKI8B60o30HzydvKN2tFncbZHoMq/1oRzJsRwZbGcqiEYsLblxY8k0NVkdDcLB71ONSf'
        b'sNEF+c1mk8cHm+F1DdgPXql3XcuhON6IPzsJdpBVy8XgYFkl2F8F9y8uWwhfXABfXOyVkZREUaEB4BSbA7bDXk9i8GQWOLemEu6vSk+Ce9OQ8OO6djHsYMG+uqk6TH3W'
        b'g70VlnJYFC+uGFxigRNyeJkwgSzE1J1mbjqEVzci5zS4ylzgeL8iCp6D59FUHw32gLNUIBIVbhP+PL+wtUSSlJaSzqb4WxFtP8ICzyOWdIBZ/myDXcJ427sBN+SyUew5'
        b'0K7wro9ha8IRcq/85NenKmdUIBZxxjs3PvvF5n2eRx+9Nuqxqv7WgLB/WvKS3+//zqJub/1blce+Knph9rtZWUF67c3nP3nl5fUH/nfh1h0/nvLGq9t//fEhlved20fr'
        b'M7f+9AInxnvqp8sbTj6/kRfxvmbPGtUbr87vSXEtC1rFVS//ovbdTX+9FH9IsTZWsjf0D++/oT+yb8qc7VeeldQba7OmR79S3/gT9uvyG6kGNf1Fw6w8fXnpT3ds/t2R'
        b'53U1u7bcnpNx6ovjU42/vPxG7HXX73z057Mv/njH97TvnXv793//2Tt/fGehX1X/3z97+eaqxW+8m3C6IiHsQWRu0uTzV+q+evN/+EfSD3oeu52jKVM+ty5kZMN7GwOW'
        b'vwd/dm1hfPnyqo/SD6zPObgJ/GKlZqX27JzuX8Vv3vW3//X4mV/TvHdTRJMZ1qkbdoIj5CpRFyTI6Ck2OMtarIZ6ciPQ1FZwCTFBgrVWJsi1idix57MaUB4b/gfsWBPT'
        b'DA4S1k+DGKDnGRYIDgY7cEE8L3AI7CSHP+D2ZcXj1z7BySJOvQc4R0zit6rhayXlCUieO5gILnMpb/CqZjWnBhxaxdw+1oGYoJ2wowRJ7s+TmyC5YSxwFu7LI5XLQLi2'
        b'K96mdM8E2SaOy6x6xtx+nyDOfI2k5RJJ2NPCaW6sJgulnuBAYontUSUW5Q+ugTNB3BBwu5UkKQY7CkrGjh2tjSOpJq/Gy9mnlj2OxRBerAAvlJSiFjlV7uRYCGGE4TFw'
        b'iKwEg5spm/ARpLFzJpRPWDDo4DzrB+4wMF97ZmGJzcEknyVr4QBHKYaDzPUCV+BZOWYDLTzgsyvZG8GpLCbysCccwtdehky3XHzJAjem1jEt2YYY5FN2l0vBPRXsDZUF'
        b'hNsHbQXwDJbY4IEKfOEa6ITt4Ai7ORIeEE3+F/KUWGlh1k85MJQuNcydibYbO5kQwkK+ZWYhl3lRAVO7lYeVh1RdKsxUYJasoU/au3ogziBINwrS8ZWVU00hdG8OYsem'
        b'hPeWdM43BYd1zu2c+ygkrDcLB07tLTIHmgSBPWnGkISHgoRhQYIpZGpf+HGUZJRNB082CYNHOej3kTCwq2yUh3yjfMpvSk9eV7FRGDPqggNczQFdFaNu+NndmiB61AMH'
        b'eFJ+gZ1zezinPU94DkdlGAIzjYGZBmGWUZg16oUTeFN+QaM+2OeLfZOwbzL2CbBPiH1+2OePfOgtAdgfiP3lo0HYH8y8wL1PhjnmGcNRMw2BMw3CWUbhrNEQnGAKSozh'
        b'DcUPYSj1sDC7Z27P3D4euWZzg4HOMtJZhinZxinZo1NxIpokyiSJOBc9z3oOLGPu4jRMyTROyRwNx4mmoUSjEdgXiaEpG43C/mgMTVFP3mgMfoq1PInwU5zlKR4/JZCX'
        b'iHrm9ZaNinGABFc1EfuSsC8Z+1KwLxX70rAvHfsysC8T+7KwLxv7crAvF/umY98M7JuJfbOwj0JOJ390DosKCunkPfL16/Y87NmzsmflQIYhNMUYmmLwTTX6pg77plri'
        b'Kk8vO7Gsr2FA2r/aGJ1pCM0yhmIBweibPeyb/SgsCjPEEuJ05puEQd2lh0v7BOhvyZmQ/hCDUGwUiofJ1xQQ2r3p8Ka+dEYseTsg6WFA0mDgULYhYL4xYP6w73wbDtOb'
        b'4TCvkeHALH1qRngarVStHeGgofDN2ElvCzs5jpPEl8M7DrJrmIXstbKQ+BIaLxYrATN0/7zzrW23xmqxM26Z1F3vPB7nP26Lf6OI/eVvHTTxjD0PreXYu3lFU2leaFDL'
        b'tTq1isQ10VK8YG6zbvFUi830GvlGDSqnRS3X4ENDzIKIeYVHY13lNq+OOFskHr8ArmSWlTA4tRsR4F+z7c/VKWurwwcpPbbCNtCBKOJB0L41EdyAh8HNpeAmuAGuLAR6'
        b'HuIRt3E2gb3gNNFnFzyHmMsjiMmXUJvTJYhk3SEGRhLkdYjldV0LOpaK4bESL3hJIuFQQtDOQezMS+AqYZff5nGQjMkw0QtEMyym/eBtb3NeF4rrxwbnWaAbkf3DI6wa'
        b'ou8MXQaPxJtVmhmZRKl5pJ7khSfh3dmwv8WWFUZ8MLgznfDBUnBXZNZ5ujWrWVngOBgkLHoIYg4GKpkcbLAf3mhgTSkEJxjtamcyAulICYafk7cCnGRtyi5WrEiaz9Vg'
        b'iXLSttNHD81wZyf75jek/HXt59xn54tf2X5t3c6bS0Z+8D7lURvjP62/M21T0S1Qn8e+yZl72O2T3xx69y3O6tHhoYjHfr7ufpV3/3p7z3u1V6jprW+Z+oq5EfGvF7af'
        b'2/q79os/KvpD7csrf8M+mpW3MDnqTvbi2Y1Hf/5RysYPDz1/8frFP+enfbTx1U/frN/3V8Ev9kozI7mVspjkjS9mtbRf/mrRz2r2NiR+VKSbdSSU+8WynT2Z/5X02vef'
        b'WcV561ecbUeTpjX/QsRn9FuDk8HLZDsaElE6bA+gkA1pr8JT5HSvxNdn7OojeAv0PsuOSC4j+rvFKZviJWVsit00CwywSlAH3yUMjZiD1ZOYTyoSw+vwOpvykLNhHzzU'
        b'TI7W6hRldtq3HLaN8m0hOMDoONsywG4zi6iE3WNXjSdPErk+NQ/jauVhrJyLVFODB63NpGoOIZyLn3nb2iIfQn4QDxEl6i9/OzLrYWSWITLHGJmD773OYzHuoVJEzANM'
        b'U8NPrzuxbjg6Y4gzVGmYmmecmtdZaJqagMj11Ezki467qDyrHEwdcjFEzzZGz+6c3xN7qKKzgpRujEx7OzLnYWSOIXK6MXI6ZojmshjXXHxwaI+0N5rwRIHBp/kn+MNT'
        b'EwcFg3WGwBxjYM4w+ZoCp/a5GANj3w5MfhiYPBhrCMw1BuYOB+biCF6v99uBiQ8DEwf5DEszTL6jLlzavxNbEYpJ7ZP1IwCHo+eg71AM82sB81HAlE7Pf+jsz2f21Mvc'
        b'0O/bnf2Z7/Nvuf7pPHrfJdYIt0WqbbS7FdEq6+/AtIhnvhURm7px0buSK3H51psRx6kR/gU3IzaI2L/isJxs0BojTJhGaKTrsE+ptCVRT2+TBTdCDl1UT8dhXxyNmAoN'
        b'sxUAEx/5BmxAC6+Mx0laFS1xCeRFZiqodr6wrsEXFMisy/lSdV2jYp1cQlfg3QfrFRq5ldKRMkgFSHIpXd+sRCzN15AtFydky5W5FhUcmDc/vhBNXgsKkdhWXFYKLlUV'
        b'gmtQnyBBwlQh3ANuwldcWsB5uEuHd1tOhsfg3RI03RWXSWA7Em2roB6J4AuR4CaOxTZlS+Ad0BXrAo6Bs+A8IRPhcGALPAKukAUOjhL2bWKBHX7LmXXdlwvh3Xh4LQmB'
        b'uIHaALe1MtTjMGyDr8VXwGvwOJtiLaLgibxQxeHA/WwNHhULqMRTC4mViRePPC74a2np4Ou8wCFW5qptxYPy2Z6e27hz7w3Or51/9fi99w8H9vufn7d69znPO6dnffLX'
        b'STPzvrcp9sf0htIY3neajuZ6/+T1zHjDj/9r+IM3l+t6PzTpZ9XfOv2LUMG277l/eedP1Z+rP1wD6nvbNwd+f02uOOgPC2IW/aGPfvXOr3vPsQWZP33mwbrb0l0N2Usb'
        b'J9fsrt0bsOvG1X30u9/b9ce0Lwo6B7WJp768/OHq03u03aqQyDlrLlw5LLrkn537+d+OCDUbf/jg8993ekSV/nLptQ1bKv66URfl8wG3vmVywLrfBq3wDT8XK7q/Nb77'
        b'42f9f1n4zsN3RD6EnkyBLzxDuguxgZnwLjzEAi9EbGHm/FtgfzIW+rEgTu4W76gDO9lb6uAlQleaylbAW/D2erK92h8eYVNu4CIbnNtcTlQO4Sj/dpT1CjyAimhPYFP8'
        b'cvYUOFTJFN77LDiLYtsTJEXIUXIRVYKDbHjfW8RI4Rc8wfWSBHCgAt8nCk/6sCiP2WzYkxXB3PJ3SDoT5X4lEK/dYksXW9lxYGeZ+R5PcA/2YAZDJIEHUdXAZfAqRfkk'
        b'cRrguRpG1/NSCwd2gKNgcOwWwQjQBc8R2OLBvqD4RLyBQywRwZdK2YjUneaA3WBvGcnttwTcLwGH0VsOoNeX8yj+dHYAuAdOk9wr4SVwq8SK8W5C1Eg32OBMMNjFvPu1'
        b'fCF6932Ueb+5XeawA+G2tUy7dIFdK7BqwqKYgFfBKRa4sQZsYyp+ai3cFT+thICH3gwG2AngaIrI4x/VK3hQdmtVDFnm4gmh1ctKKvAjIcg3zQS52JcS+ndlds88PLMv'
        b'krFjgUW67PeCw4en2ZiWEPihRDMOz+gTMlYkSKKBlOs5l3MGZYb4XGN8rtN8gVOw0H/cu9e7k2cSBHTnHM45NL1r+tuC2IeC2AF/gyDJKEgapdwnxZuCw3ti+iIHOAMr'
        b'DME5xuCczrmm6PiLa86uOdPU34QK90smznH3Hm6PzBQYggvuqxpIMwQmGQOThsnXJAzoLjpcdKikq6ST/D0KCe3NPD3zxMyBSENIojEkEZcRY0IE3/WEa58QA9bjbfce'
        b'tl88cczvCQ3vqeqb1h9zMeFswoB2sMowLcc4LWdoniE0zxiah0oLin+wyDQl7HThicK+quPlveU95aMcFEqiiPMpdh5TdmHOHCRyOg0e5VhgIsqj70T65/N53+Vz893d'
        b'vuvFQi7DP7gx/MPnEzAR4/EFi5FWuZjhK1xZ+FJWO2T5O2YqtlGWS1k3+Tzdpaz/olvHj7slUte9Z3BEZot2+NpLGzNxiHSZPyIe88NG/4Jx1tjx4W1Zc11NDbE0MuLa'
        b'om5ukau1G5/Glgk+dkx2/ZO1KKJGINwYaTqR8N+yKI0lr/Hr0WN9KENOq9VW4G9whlKOnfHLUS7byxehE3JcKW8//dI+zoDmQe7wMytMYeED2cNznkX4672KhdAWuY+J'
        b'+2h+vmnholFOBL4C80nOp7yxTKNcHFrMooKn9QSafMXDvmKTMGOUxw7O+pRCzmPs6IsRux4U3uNq8sX3opqE6ShBUCZKEJT5GDv6IpQgLLpnmYksRpqEs1CCsDwEHnYf'
        b'E1dfjtIE0p0bTL7xw77xJmEiShOYjJIEJj/GDjH0aZsgGyfIxQlycYJckiBgamejyTdu2DeOSRCAEwTgBAG5+gKUICSiJ9bkKxn2lTBghBAwQggYyNWXjLqyvLCY8USX'
        b'T1q9p7JPM5j6QPBmqimUHhAMRTxIfVOGW76KtHwVacQq1qOFi03LVoxyxF5zUP6ndXE3WEoY5ZLwZ1lMZ0cMVj6IetPlwVRTSFiPtidukINgqBxe8sywVI5f30Be30Ay'
        b'N2Bga/CJEk4FyytllPrHXQyRtVAuCa9lp3vlI4D/aVfFCvIKHaUmcjKY9o4Y9gozeIUZvcJG2f5eaEL9WudTDuU91TH92LUJ08E+sF2DKPylIsRjaLy9OZRXKBuecW0l'
        b'W+Bk8B7s9wADWni+GPNeHngT3wK89XFKCjeiGp5wfo88uW6aZb1H3qK/+/fcIb/raUx0uJQTHn0TOAyv4It1w8FV0EeFr2whS51J8OaKEgkYTEqn4MENFBfeYa1FbbSX'
        b'UUfthPuftVnqhIPPgBtseGpOI6Nx2jcTdLvCo7CjKAEvYqVyKVfQwS728FVs487naFaiNL9Ou4yNgpw5spbFyRj01C+FG1fuE+3zCLxxifNhw7TRSVefC1rwyeqhryT5'
        b'fZJ65b1FPYt6ulk/Xv7jXWeP8a5U+3tWBu0dygmqDMwJqj4eGdRZ5lr/6EcUVfqV3y9+9r8iHmHPpsG7YWbraRLQi9gzbD3t1a0MS3tlMmi3sHYV8JR52WkyHCKLUjWr'
        b'JsWbt2XB41uZnVnwPniNRObNhe1zUu2WndjNAfAQWZtsmBQU3Iq3HDNRK9nyyZUTmiDxbFHLkdgpr8E771vtngiHhy3RYJI9exIlDLTwXfp5jwT+3VmHs3rmnS4+UXy8'
        b'tLeU2Wmkn4e5s9zDuT3rB9wMghSjIGUsaAOz1wcF+PjhOSzKFBDSU9CzpKega0snF6XSl9jqMUa4GIgRPmNraRwvwugyMN/B0CsB5jnsoA9H4GuUlIXleM6XxQrGrIRT'
        b'51u9x9oO733Nv589wlaaPWysNKdg4yJoULJ3uWF7zXKujLOLInaa7W0Y80gcH8W5OMTxSZwrinNziHMhce4ozsMhzpXEMbadx8e5kThvFOfjEOeOYHZBMPvucq32kKXq'
        b'WfUs2WQEv6c5XIDtLMvSSLgfCvfGfj1f76Z3r+fK/FGIjywdhXBR2kBs2bjLvYvdxanndHG7ePhPJqxnozD8y7H+MqGMy2VS2Ljc8X5ZUK+PgpIFd/GOsGQhXe7InWIp'
        b'C/lDmbTIF2b1TbX6aFk4cqdZnyOsvkirL8rqi7b6Yqy+WKtPZPXFWX3xFp9tHWQJvezzLJm4l43tO8snyyfJJEFWFOoTUE4+9tOvvTVocxmJ/0wZBBqh2QQyYwTHvd5F'
        b'loR62I/YsnYhvcqTJaMQf5mQGNLKGHGrQUyjNF+hlBOLoHb7jKzKPD3FLCzZ7DPCxpa56B2Unm1W6eHdRS7/8t1FDrakOJQjoXJndhcNu3DxCg2dlN/nvdl7BrMdP7Bs'
        b'HxXIomKTAsIWdeR6MoHl8zaz/sKmlg16eXO/vziZ0uF5AZwPxnZfbY4xEC37omcsZqMQIehwoSobXH1hBzhGClqimEbNQ79Jye8vWhgeQf3eAiaZKRURr/2Zq8Gq0aXV'
        b'807+IAMRsxtHop5n8XsCc47nPtPNWLlqZ/02aOH7QQt++zIiVYsCb32ge/3j2jD6pOgk7w3JZN7N47eOv678avKSoShPUcJAdFryuh1K6Z533uwCnWDkB5Fub7O65Ns/'
        b'4n+6bOEGZUtYSOf3vH9/4+LOzd/bviDkRw+O86kfnp1y5lftIjdC8cDdHB3oqMCMDIdyrWJzPLRgOzxPlEubWdWgA1wvLRPDq1jPEcOeBC56ECXNWnBTirc6o7+ucdZO'
        b'4dAWsnmmGt73HmdoC/TBPnOrRQXxGsGuRrJvOnc96GXskqaD3vhYMdO4KFHAFO70xmpmfWWfCJ5lAAX7yS6cfRwKHmuZBE9ywBlU83ayGjInG94ZS1UGriLe4gVwcRI8'
        b'ygHn4KXnyGYd30bEwHUkwvbEIriPRbnCvWwwAG6DXcvgK4wR1KORMtCxHpWiJcozeDQO7AcHKxDtb6+AByR8KruED46tXS7if43UhpHSwe7oZOuYszc8ii3mYdq3YhI1'
        b'NbKT2+XB7IAVHn+m9xn06D7qTtERPZq+6YapScapSZ2eJsHUvvCHgohhQcSA56D6YWz2cGz2kPLNuoczFw7PXEj2vOYagqcbg6cPC6ebopKxUc9ppmnxA3MHFg3M7ZcQ'
        b'E6XhUcTkp/knjCZvDo/s42Hbp53oz4bKM9qGER452DXCxeeCRzzHdmOqmkfcFKoWnZZc8OFsTYPRP5iX5p/cJomYI9hJ2azLL5/EYmVhBuCpnW91+b3XLYW66Z1HfROr'
        b'nmZjgLwa3FQTWQG0qbzFDGAe29ZUYfU2sxXAKWM3XDjY/ZOo21GSbw6bV41tB34DGOex7axkJlqADLMB0tGOp+Sb20R1r7Ei1TcArwCBp95vmXu/DC2ylGE5UvvPAeVW'
        b'gwdBTZNiQgOUTmAqxjCNWcb0xxobul7d3PSPArPLHhjphm8ATJk9MEICDD6q/U+1C79G26yVKr8BHAvscH25BY2CqnA5lnPfEwL1n7D95am4Eh7DlchFnFUnWcx5Rvn8'
        b'WoYBWenrsuINFjkkWPoBK5lSHLqu4mkyUEzbW/2M2IvtYC4KjPrVx7UXhN9dxY/eUy70+2Fg0CJZ4JJU8FbqYtb3V/F/kkbN17jOuXNdxHqMz++BNvgC7EdE/Dy0IWfO'
        b'aBncmz+RzMkYnZxkO0GP2bxMphiaJZtMBU7p2tK30BhAlhJCTSFTepKZ0w1pveajKQN5hgCsD/zHTV86QlHJtl3/rpv8b1v//uDv6PMfqMpx2H/vTJVjxsVuMRdJvI+i'
        b'3KhtymVrvaLJzrnXK07UUTnHcMEs4zOKqq5XOQQTyz7gj2FiTlDkrz7m7fNcNtu9zv1nKdH8PW+VtsyI/bJp9urAo8/vCMr6GWvvPNf6/CYR+zG2i7oS3IfHwcRIOH8G'
        b'QcMF4AhZZUvzgy/j5cU4sQSfctsBO2PZqeAa6J5QMeJTQ074K1rlNbXK5ro1rUE2qGIfRRA30Yy4LZOp2IT+LYOLjTG5b8fkPYzJexDxYL0hpsIYU4EZoB65wTdymHwd'
        b'0HaERw6xf42uYy7WdUwMzTJ7xUcTwmB86si58+0qPsZPo1gg+GwzZRH2upkrkKh6zv+lJtLZZgXzdR0d6i9YH3NWLXdbsKrGLzqfORoOXwJ7+eAKlwpVUq1UK2ibRXat'
        b'wVfgPXAWXGFTjZXUJmoTvAgO6vDGdngDHsy3E/PADjCE8LQqtlzMotJAO98bHgWXyAnvVak8JFJmRXJmr1L6LYqiyGnlkqgK9ht8qjGVnFZ+J/MPjKW+9ethL7lCYxq4'
        b's8BqpI85tmzGe7vbM87A4+7wxHqgZzTNZLH5cHbDmE50zXJGK7oRnlL89PXzHA1ekloaf+PkD6ajUWnYHf7nfPFcr7nJdT7xgrkxlV4wJR8Ny9meLNG+XyTQ95bd2yNl'
        b'cTI6wa7L55bd3hO+O/tk0BuSXydK8xd9f8flm+2TZHUxGn/BCt6VyBXpl6uVqitz1DWHfN5ISHv7ljw1773XD7zvvU67XpuSuOr1392Vz74f/JM62ez/r7o3AYjyOP/H'
        b'3724bxZYOZdLWGC5RUBFbrlBwDvKucjKKQuKV7wVxQPFY0WMi6Cuiopn8CYzSWrSJt2lb+KWxsZcTdqkDTQ2SZO2+c/MuwvLZUyb9v/9yTq77zvzzvu88z7zzDPPzPN5'
        b'Vn3Ont/d8crmFRHnX+K/+3qLyRmTqdvcNhe9ueMdflb4yb+GBnuF+YT9lvrtrOl5AiQXwqgV4sAC4xyRIZmLRYI2eIcYRuWl2vV+Zq0fXK0jk0N4EM0be0ZBwZF5Zjq8'
        b'YwRbgolwAdtj0ByQES614PCkgxx3CZlLhqwAzaZ+2jmprlK4r4ByA9e48DJorn4agGu9gaalW4n7B56PIt4A3Wlg7wzYoqvXgAoG5w2cQXsx41vQCU+AmzqvBdhrxziv'
        b'YjRCxoLcth4+GDYCVxYzZmB4BWwWcSecPeI+ORwhASlWq+uk9ZK1VnqihJwh8oyti1phQ7m446X12SRpSdQ4ueHVb3eNQKgdjg+sObRGEXZwY8tGZf3lDec39Oapg+Lo'
        b'oLiWjX2lD0tARV/FY1dflWiG2nUm7TpTJZg5PIwrbWinADSG0w7iHg76S7xifN1Y7RDVm9DvMFvlMBsvLoXJ649FtUcpef1OYpWT+LFHoCooS+2RTXtkq5yzNQLnR4KA'
        b'fkGAWhBICwJVgkB0pt2cOafMUwtCaEGIShCiwZ4HCg8V3xt9aL63kn/Z6bxTz0K1KIYWxaj5MUyOmqSDdrrH1RPRBoyI5hbVLZdNqF8Y6MS0Vk5nYTk9rnFfwOJ55bB4'
        b'brD53659HzEOoLotojlZJdyJhnSyzY6ls8wRuxwW2uwyLhHZ3Am22fGIyOaOE9m8cWKZ+yJPK7InzJtc45gIDdUwi+zkApvBcbgbYOiMcHjJDXW5JniBmB4JEGouPDHF'
        b'H70H2AYuNVAN80TMRSeBEuzDMp1aBu4ioY5E+QnpjiV/ZctiUXZwmuj4m6HalaEWoHnjvTd69hzbXDQtLKO7+VbrLblou0juvv1WqzQi57XK1/lHbgW80t1p1v5Havcb'
        b'pn/7Jwspy3jdLtELnAHNQRj0BKDejR2IkF58O5VFOZVzQVN63DN66Sa9XkoAdUYxEjlDeikmF7NRji01xeWRwLdf4Ku077HrNVALZtOC2S08jYMzVp9dNU4u8tBBDvr1'
        b'xHOqIkzJw3/YsdgqUI/HDUfcJuqwilaHd9yOVUcMKcbkMqyQ5I9ldEKfFDN6I6U1t2DUQlsWC+/4+bHkZ9NJjBFdo9h8eOgnBmiuHpsbIkbHxmdjwuyG/0Nmf65gBrws'
        b'hqWJ4rFvPbgJWlmUDF6jXCgXsA8ek/699EsOCU9avWPv8TdjEO9e3CzaHiLfvKvD9uFfShe9/mpfj2OTu0Lu5Pt2/xs391j7vmlk++dizu5Q1rywU+cV9/9S/Hnpibc0'
        b'b0QcD9kuDZShAdORWrTAWthxWscZz7GnxJAa3lPCMK8pWYrTcrCdHoeMnCZsnKdl4xdsKf6UllmEWTUO7i1rFd5KW2Z8wFzso3F2w95Wx9La01qSNAIvuZlinjJZLQij'
        b'BWGI1719FXlKb/yncghWWQXrcbbJc3D22McxGWH0YYPrAszrEz9JDWb4nXoMv+Q5Gf6/xf++iNY/4p08ozrBsDDdRumvwhBZb6iV9rz/YQcofx4FXdcByH7LtKV54vnw'
        b'cFgKhwKH4AOeIQtN6E6BHmlvcRJbhkPsJVacOP5mNOoFp0kvcN9+rrV2461tB1gWckH0lBmLjrCS5sOkGVPOL5wiyHmtX35eI8C65G+oj0+aqG8tRAKc7BLeBXaFaBFQ'
        b'WGA7bJ4OlLPQVG1S/ufp+F8L7FGgDUSp7QACPbYZlUP6wDRtH6gc1QfcFGEXOcokZVKP97mM7ozeCHVAnNo3nvaNV3kkqB0SVFYJelxuNIbLBwzKikrqa+om1FeM9Nib'
        b'Ye4XMHNPSuVqzN8b9Pi74qfw98+GZIDJbjMOpnosYjgiSwY1guBHECQJjCkxYD5igK6QrBkwX1XTUFIuqSNPETL6MHTAtARHLZBU10vqQvQPQgeMSqUyJtwABqQY4K0q'
        b'qsehaSUN9UWNJOwp3ts3YCZpLCkvwkE58akzpCT2FwsZMNGFC5CW6uEHnyUl6qX1lRL0vvCGwzps9qzDNqeJQuZmDRgVF1VX4CoHTPEvHUIuOU1ioZD7hdaVsvC2RAys'
        b'WFzTSHCKB3i15TXVkgFOWVHjAE9SVSStFLEHuFJ05QCnWFqCDgzjEhKy52XlD3ATsnOT6uqxWGxgjZnM4zbHM5KvdlA6hIijFFkVxm4YeNCkmkzKjP6H0/pxUsNpAqlR'
        b'wkzr/+mGV2NVM0yDi5ZErCvT4j+0yzJl8KZlHY9iwzO4e+/0K4cdZOtR/AtzZPWrUCa8YcqiDGFb/Cy2BTiYTKbhaXOl/tjJ/KJvSibcCpWBqZlzYVMWuBgA9welzU0J'
        b'SAtCM3M0G9RCrFGwdYlZgj+4zYzeV0AnOAFb56Lfaylw1iLTeyHJiF7jFIYhJKAc9rJ8KNAKukWM/eFkHDwbxkbz+XIqjAoDp6cwIBG3G1egC9hoQgu2snyxJDwNzjKz'
        b'/K3V4MAwxBSLMl0slrLhJYk3gRhbBfdUowsNKB48zhJR4HBFGEGPAGfBUVM8NTXBCPzTuCj/Cgu2wlOQWYp+HOlP5VMpYeZWhcUu9ssooklbgtuBqDIWBZtBE8uPAkdA'
        b'szFxNYSbgdI+PVAciAEIM8VwdwaLcgBdXHjCOxYq4W5Sp3ugOxVLRTqyagtf+ITrRpEnA3cXwFOoUiTdr7qzAiggBxfBZQKDBuW5YIc/bApCtXcEpjI7nCzBXk6xCHSS'
        b'Gi3W2VMBVBPfQljoHDS1mlGZ/MAl2IJqNKRWgO0sMQWOBRURJmCDs85o9hyAHUu4AazGUnAbHAe7SE2mKTHUesqoziC4MPRP9VZarjkB9oD9YeGgB3E1VLIC0SR8AThA'
        b'mh3uhDdhB/aKyxSzKOMQNuwqBPJ8sINU97c56dQhSlNmYFW4oj4vl2m+DNAKT+DauJRHDiuIQjeXx5MbNcDORH94eTZx/CM7+3ewPQUMnsnuqdhoVGtuFFtodsI4hakK'
        b'7FjqHhaOhD64boMb7TDYBV4mm+EyHaPS0+CepRkY6zGd+OpZgG2cmNoYUps5J5KqpRr5FoWFNn9bHMC0GOi0A7dRdWxqMXwZP+XRuOIGsm5+D56vx9XB5qwMN7B1mMkc'
        b'wSEu2O0NthHysfcpuIgqQOx/HDzAjyaPA0cbsIkGdMEu2IHrCHZGtTAv0aKWEwkuVjEOqBW2lBfVhF54ofOatfFMy4P78Bq4ERaKGNcAHMJPeARjaTA1toFrsBNi79ge'
        b'wrxsxLxXWfAQ6PRiWGpnIbp2WjBFlSOmD0XXwq1gM9NuzcYS/yX8dOxfyaIMpOwp8G4dc9EmN9gcNh1dVAYPsyLRE8AeeI28ah94vQ6zIWLB3eAyRZnNLEvjWAnBIabx'
        b'Lrp7o+tQ1zwE21nRiLyQENLF5mFExHSmxUQYtcPMKhse5NjZarvYzVQjyopSORkVFlb+wsiX6Q6zFyCGmx6O57CI4VBtx+BZ8IDhuJfB9Wh/L3gdNmEcxnTEJiVsJ3jL'
        b'nXR0NjUdXcdFj7yPNQMRwUadCJNnBrc4pafjrQwJ8Ai7hhULDmlNmgrQCTvQNejK9ayZiBvTAog8BEdzF2FY0BYs2PbgPQ4Gtmxju6WEaEXVOuoplbLCwqow4v7adC3/'
        b'HIdX0sC14HAeNcWBFY9m3DPiGZI7NuahqXAa3m7BgfdZ8E45KvsSvEHqetFpDrWH6pEYCwtNNOuLtJx9M28GropDbQRKVgIFFLPBFYbgpgardCRZEJP1GrGXsYLACS9m'
        b'HcJUQAVTsZ7cwsKZt33YFGmPFUsz01OxlwyXyyoHh8DJdRuJjSA6Et2/lUdVlVGBVKAvONlAbIDyxUgYXMjIDMhNgbuyxfMZPzTQuhE2ZQYg0UNRc2wMnYTwDnm1qeA6'
        b'GAHgxJtA5OxwO3A4F2wfCY38ERob0ftItaAKzabYRDP25aoIcBW2GlC27khwBYATYAcTjmS3W+MITGAn2KndIoQGGi7lDc7zGsBl2EY4xIa7EDavtpyLUYiQHLNhLUVi'
        b'ew95c8vgGXgnPR/u5VKF8BwLHtMi4hGw1A1Su3QtdmwM2DkyXnhn86RxsVr5roSn4XFTSshDPRB90Dh5nBEEt0G7zB81SSbclyLeAHenMRApIVxqaj4vtBhcIo9sVOtI'
        b'hVO+IZZWhc4V+dYMS6+B98AVeNyQgnfAaQo8QJ9F4F4D1l1NYYv7cK3gNOzWVcumps7jhYGLUM4Mf5vgDcv0uWh4zYZ3CUzpPXhVxHDFy+Dgqjw0KO9FQ/s61tokZ/4G'
        b'pkPfn7oxfR5uCy+wjwVPU/D6CtBJbguuIuHEwPTCjqjUkbZwA81ceBPJ5UPMbXej0egePG5OvQhOoJEKfcxAF2lNd3gDXsSdOzA1KysSXZwqDuVSTqCNWwnvJZPW5IM2'
        b'xGrHOVTxEiRI0Qdsgt0EBbcRybKz2osr4XHmaja6+ji3Ct63ZHwZr4FrfNiMwWxyKSklDXUmnGeVBtqww2SSeJhoS1vOCvgAbiFsHwtvLMX2sSKwnXKj3AjIFXmBmzeC'
        b'bf5MuBu4J35VehADz+sMbnDRY3aA/YRmKyRFEc08ag48ToE76GMLz5KKowh8UTObKgulKqgK1Ea3GRgqhW1qulicCrp903B3s43lFJgiUbgP7mTezyXYVgWPm6GRKh39'
        b'R581wYze0p6KWjBQvK5CD8aHU+nkwfhs7kZD73GZuTmbqg1kof4HL+YyvT2zyITiUwKekVWh2X0je0YCzQcX/WAzB5UCt6kaqgYNF9sYxeRkMehG6lsK4jCwYwmOJiQm'
        b'dAqduLDHKJ0swbQaebNUnMEFbCq2+nHjKlE4I0JWgi0rsdkQboEKvBiEBIP01y/9jpJtQnOjV0qun353Ts3vgvlU4cG/trRH38xb3bXO6/GMx6mtZ9Zdrg9y+IzDfng0'
        b'frAj+OP0za71orWite+84fDDGzHeN71C19t3OAbbpGW7uYna9m/84kFA7QsR31E1zZ9d9old/1Hh3xb+YnfN1T4L3m/Wf/eti5d4n9h19ke9V55c+2Pk+SVF3b/Y8Je3'
        b'VrUnbmHz4alLlid/Wf1y19dPt35v9urafz0Q10ytBQezwOeSxw2+cbf2Z1smlnWJF+aYVdYeHHp4SxBtFz7VhhPxt5WXDOb/QTZvve3Nr9/uajekzV6LFkXwV76Z817G'
        b'7syk94p9q71fq9rd+zinfeprLrt7f5PzXtLuO3Yr93f0HuV/88n6sO9ThzZ5uIbzl6esnG+dueBb99yZ7bLtbu6vdUZ9OiQQuS541XbHh6m5Mw/LXLNbPzzW/uGi3Jln'
        b'm2Q7PlyTe1fR5GD+WnpX4yLryw+LH+y6+Afla1N67Has22D8zR8vvBHjkv/xPx8fhwLTB5/cON+ym/tC5uykfou8G4GH3/lH75+GmpP+EE9fLr1zuNT1vV3qH/5840rj'
        b'jSybh4VxFw99mzjt7fsdewIbLt9znTvPc/E7+U8/FojuPwq0ynXe/NWCvjuPlG0DtvlJO5P+eYz1UcXtz+9vOv3BQ+6vPor69HbQod2ZF09KonwuG0/fsXyzxO/Lz7q2'
        b'bAgAbxV9fHHlAbls6e++qgo9O+PNtvt3PlhwyuHLAx/+c8hjZsv7878p1qj8LKfvs3A1//TJyktRjfFl/wi/VvfH15Z3fTszj74kbozb7T9leeKGHUGpX877Q1Ra0P1/'
        b'7R847/aVU+764xW/+jLly1nrW8y/LZd/5NP/j+49t093fx10oUHCz20uOfn+rRnTVnx/qvnORwvUuy8nznt10T8Nu94Kqq39RmTL4Mvugy3ikY2S4D5Xf3cp2Se5JZDs'
        b'x0RDQStQ+ONVyThwiw3aWJmg24jxKz2cBRRIOUOzGgOKm8havg7cWw6PkT2RCxfi7Y6WtWZ18DoXHgB7LVeZGxsg4XaSUwN3wIOkENghgudNwbmAFN0imzW8zUGKfDf6'
        b'vwmeZha4DoEDSK3Qc29lLTYAV8A5uI9Z4DoLbieA5iCtd6sR7GSDjhDQHMGg27rArVZkOQ0PEGjIzUS6z+1S0BVO8C+yDGAz6tospAonsVex4uCONHLTcHADbvNH2vG+'
        b'Uai3iArGpdYTjY8HycBPkN2mgXZw1RpeInmL0uEF0BzqiDexanewIjl7msEouw92rxu/rgh2pBi5BzNt8pKf4dgtp2S/6c540DEdXCOF2MFw+5gdp3i3KdwCDoLOEHjn'
        b'qQ+eN8COJXiHK14DxlMr7BetbQX/KB7cBY6BmyvAJman63mgLB9ehwAHWMNFyTIEuDyLeRfXC5aiuYsZ2KSP+8apWYKqIe/i0MrYMZtcF2eDbSHw7H/sbDwavYxTVFq6'
        b'1nzECIUOiX3sA54W/MOOcvWgXYJ6wvpdIlQucb0oyepb1GLymO8gNzhp2mZ6zLzdXM2fSvOnKvm0KKrXjxYlqflJLSyNLR+bkRewHjt6qrySH/J/PeXNKaq8/Decf+Ws'
        b'9pqndpxPO85X8edrbF0U9v22PmpbHw1fcDT9YDr2QEY1K5KUYWpBEC0I0juB/lb1SOmgWLV/HO0fpxbE04L4kfyIHp/u2b3xzIKM3mni9Fyp9k+g/RP6ctWCFFqQMjZ7'
        b'BVNlX6hakEwLksdml6n9Z9H+s3rrxt2TZJer/WfT/rP7bNSCRFqQODZ7udo/hvaP6WMxVz/5afeuUvsn0v6JfcVqQSotSJ2M8hC1IIkWJE12b7ZakEALEn5itlTtH0v7'
        b'x/Z5TFy5Ltv92c89SeUStf9M2n9mL3qwOFoQ9yNXj221H3klYyofEjvZ2T+lUDI4JommBB4taxVTlfZdgT2eaocI2iECL7svYmlEYiVfKVPKesJ6DXpX3bXokz1k98no'
        b'yPRHkXP7I+eqcuepI+fTkfPVQQvooAUq0UK5gXzVMQuNg4u87NCLOHx0afeKfodIlUMkWZePUbvOpl1nqxB3Orm1x+C7RCrn9yR3L+stvVvdL85QiTM0oqAeg25XObfd'
        b'4vkKuXjI5ykilL60Z5gWZDlZ25UU7LOGpwyf4HV7/36BvzK5Z+75NFVATG+YKiCpz7NvlVqQRQuyNALXkyZtJorZzOqOSrCs1xDlevaVPSygk5eq45fR8cvUkctUglJV'
        b'calG4KLgoL9k5Wzaa4ZaOJMWzlQLZpK7aBdF7V92vOrYm60OyaBDMh6iFzCXFszV/HgBF4WBYlWXxSPh9H7h9F4DtXA2LUREzR65ZQztFa0WzqCFM9QY0mdsjZnqkDQ6'
        b'JO1hnO7BfqTASNMkaAukqUPm0CFzhmXEJNcjGZNNC7LHP/QcdUgiHaLfV8fcIF0dkkKHpOhlj7o+7SFPHZJFh2SpcuaqBbm0IHd8FVnqkHQ6JP3hArVgHi2YpxE4DYrs'
        b'RPZDlJ27w1OcoF92gqc4GSRJAGU3pSX9ULoiQs0XtWihFvTWMkyZtQysy/80tD48qoyD6msmoASjRpXzeD1jN6XbiTHX7lkegs9OftbFjePGIdQVi9mjvQKGV+1epBgg'
        b'JLJehy3wVJOhdr2ONYHl/effmzxud4aQGm9592Es74MzsMGDquFRhRkJhaUUs4iHC5vWgwuglUeBM2gi7Eq5witLmMnhWdACdoBWirK3paZQU8AWqCRWGkvQWhXGpeJm'
        b'UKFUKNgKT5IbrGNji5kV16CwEClyThTZVJc9yxidHAxmFRaaHVxnzthe3svGiwAarnlw0RKT6CztWnozPFARFs7FLjpscI0qMYFXGaP7YV5gWLgBNn2V1VIS0MbYSh2W'
        b'GlBm1KZkc2GhGcwKZWousrVGbeAbZlZbmPGh1RqGhi+4+KQqHZ0086+PZEo2xptTAkowk51TWKl5YR5T8ssoM3SyZ7kxOnlkPosp6eViiqa0vf7GaEqb6xzFlJSE4nlu'
        b'ykw2Ovna7ETmZJI1Jik4hC0szNg7o4HxKM8Bu/yIBWQeuMgBu7kUbxUL3IZHwW7S+EuRUgq6s8OCg7kUy4sCBzfUkLva2HhSiZTKzYwq9KgwK9Huf2wrJdsf4V24H895'
        b'zQ1JHZkOtfC4CQWU7hS4iT5CeJoUr49eBo8bUOCWJQVexu5g80lxWTZogq1IGW+HzZSYEsO9UeSWq3OILXsuL7YwoOIFG4Z8uLMYXjcDctgKD+M/HsWCOyhww9WbMS62'
        b'w/OwHW+BgFfBRbwHIjmKWcLY7BIyvL0RL4do3b7Xgy2M9aYpOWchaMsTY9MCCx5g2UA5aCPstcoZnPE3pGD7iwQn6i6LPIy5LTwJLmATJLxJraHWLJvBBPe5OCsT7/wE'
        b'nYhn1lHrwLl8IrjIC2nm4yfKSTCJLTTLXr+UQQ9ddrUF9ZkUF7wH+vxJ6aXvjDiyRozG/XTxxUPpuVtjrXYsN0iJf+ljVsiumlk71u56oSP9QmHJrev1f/Qw7HnvajH0'
        b'/vOrwRmWmbzOfGv2xm+mb1yd/dbZb7wPaZR7j6e6193dGNiyayCmgK+8oeld6d6U/wu5Q0rOuWI7wxcGW57wC4oXXJsZ0SlZI936bY7pRc8Lp29kffjFhu9+bXN7YXPC'
        b'uys+f7hsx7/q/hzy556Kbz4b2PaJ2+Djl9db+t1Pn/8NVVF+JfnQ9oa1ZW7l9eZhPfKSI7/93u43f3LIcPzVil0F37fNKLyV9+Zrvz2/+N3BkwtNypZcvLozOTq0/PrO'
        b'7pgvG21A8i331s9f39zhFrdZeeb3Ue+uY7sGfH0tqMLV4YeAg5tOR73/oBSYZLmvXbzo+0owvz65s9zB6y/X6t/8Q2rbArdjH5wwDdv3Rw2n7NeahrfnGkfxoub+cepv'
        b'Z135ykHz9/S8Trt7N7/415/bv9r7XkWByxLPF75afnPN7/O+nqGO/f1vvnH6/l776ujl996f//YSz+8tNr7/6uJv97+fXXGg4Zd3RQJmS+a2WahTTL6LHHaBTYw7w15T'
        b'Mgsq3jiVbO3NEvsFgq14GnSDDY6AW5DBVoTnvUEHDsutP6UFVwpABxONZA+446P1joSXkoiDZD1i8G5mZ+oJeDcOyq3wxC4TW2VxrGwMmx3HAZcWO5DtrWgCdwdew3Gn'
        b'MBr2LhZGuoLbFnvAu+D206lEcMELDmPcJLVTf3BxIZ79w3PwKkPNTTfQA06jnoQo8sfm+EssoAD7Gfzzhtlg1I55NtgPH4SVI1qxsXNtIziO78KggJPFPfuFweAg1wlN'
        b'PS+QiWylEVTAbVl4gq4FAicrLDbeHNCNcjYz6Fdd4Bqe745MqOE9cMl6hgeposIQHAWnZkw4Z+6AJ/wJKfACPAgV+njl8Bg4TOausHcdqacGyYtDYK/NBPNq0An3MhBj'
        b'ITXzxdFohpsSEBiIV3IRqfAcB7Za15LbFHDAFsapdLRH6Zps7ky7MqbJwGYe2G1BSu1L51FcNkbnPwhaSK5nna1ury5q2T1a0AZ72EZcRF0WE3dUDJDmqL87eMzW4MYK'
        b'BhasA+wr0RlGNsBzWtsIel0NxD5gBm8Xj7EPgPtheiYCJNBaQS9jt+jBb2N4ap8MXtK6sG6DF2XE6pEO9gbjGELoZqArURtEKKjyuZxV9YChBrjY5WqtxYgSho/J3H4J'
        b'gy00uNiB4ju0hLXUH4g6FKVgHYxpiSH7YJ5Y8Q+ZP7Ly6rfyUsxVsi8bnjfU8B3JxwHv7E2n+aJH/KB+flAPS80PpfmhPaE9YT1hNH86ysaGAM9+DCId0eOl4sf0emn4'
        b'wpYMBb/LiXYP6QlR86fR/GmP+DP6+TN649T8GJofo63V7xE/uJ8f3GOt5qPKwnriexJ6Emh+5I/e1KElQc6lBX5qvj/N93/ED+nnh/S4q/nhND+8J7cnryeP5kdpi7Wb'
        b'HMg+lP2IL+rni5SoTADND1DmKvOUqEzIKPrzeryuBz4KTe0PTX3oqw7No0PzVPxFqgWL/o1S03u8VfxZvaF6bRHRix4kmuZHP+LH9vNj+9BTo4dNYEo4K+uYp3zEj+zn'
        b'R/baqPkzaf5M3eVuPR6j2jGeAU5nXtDIXSN7pqr48b3J5LyDrgFMaYEvmgWgBlV6KEOUHjRf/By5WgYYnO4cYjNEOYtsn+Lkm0iK73gwQu6rtvWkbT2HopytvVGGtfcg'
        b'SaIpazsdJ6mtfGgrH5WVD+Iv5pzaaiptNVVlNVVj60DbeittGTT7J9qpK0/JfeQ7o98Xz/LaTRVFbZYqQZAyQSWIQJNx7l3TIQ5LlIThiVA6RLHcSWqXjM/YYZwhkhog'
        b'Co6aHjSVJ6ithLSVUGUl1Iy/v4Pj0caDjQpulzkTxqeFS8DzFe4qvtfIZnaNl29XZo8H7TXtkdfMfq+ZvQvUXkm0VxLxNCrGYdUdnFpMx+8Qew5kN7I9bBSwGwaIGNt9'
        b'/4InUdg/jcyhFjk8y13uv+U9h8c9EYvMLdBXDMZQw56jdQvxL4cxuG3EPbzOFG9z8sbJVJz44J1TRjr/W90vvGeK+J4ygG3Y74ps6icbnslOULJjbsCsICcuNy6zIH9R'
        b'TlLeAEcmqR/gYiTxAVNtRl5Sfh6ZgZIm/M/speOg2hzwWxmB3QjALySEOxqrzcASA6s9M/Gg+M4tkRrSHTT80EEemx8+RKHkKU6aEhHbOnvJUYEglVWQhh+OCjhHoALO'
        b'EU9x0pQxBoAtDAOwTcMAbNMwANs0AsCmj50WgLHTAjF2WiDGTgscB67mhwsE4AIBuEAAKWDn0pKisfJVWfky8Gx2GJ7NDsOz2YU0JQ0accwDB6nJEhO2eQ4LY9Y9IzUy'
        b'NZ89SE2WOHLNgwapyRIzA/OQQeo5EyuOeSJGqv7x1IJydVfwFeUq5yCNq6fG21fj5aOZKlJ6KRbjL09lqWLZyA8vHyVXEa37cp+qqFeY6Y5QPV7yxRoPfOSMMRnyFSYa'
        b'bz9luCJj0M3KGfVLnHjwp9ho+C5y2SAH/XrCd5LnDfLQL9z87oowhQyVDxw0xGeMKDs3hS2uZtAYH5tQdk4YYkKeNmiKj83QC5PLFOHyFYPm+NiCsnNWuYQMWuIDq5GL'
        b'rfGxDWXnoUjAhA7a4mP+SL4dPrbHEUFK8BMMOuBjwcjxFHzsSNm5KjiKRPnaQSd87Dxy7IKPXUfKu+FjIWXnKE9QcOXRg+742GMk3xMfe5F2l6dpnN1IIR98khpOvH2c'
        b'LQYplCDeRxLB2U0eJl+vTKXdIh65zeh3m6F2m0W7zVI7xdBOMRqBk5wjz1Da087Bj5yn9TtPYwKAqAWRtCBykMdxQlWhpCl90CSeZe43SP0HaQo72Nx5kPqpCeMmiNXL'
        b'ImEhnhSB43a6eRGPssrnLIa31oyy/Jhqv79ahsGtrPXArVgY0uoQ95DlIcMyNkq136Vs3a9uzhk0Hl0w1FVlTJW6kQ3oxk2WZdxSw23Go41Qi7lsSsLTQl2ZTACDxSs1'
        b'RXlm4/IMSZ45yrMYl2dE8ixRntW4PGOSZ43ybMblmZA8W5THH5dnSvLsUJ79uDwz3CalQtwGpQ7tbHSEKMcQWCvMdWVKBXqgTRbUBP+eDfw0prYp/0lta8ed6WLtY5W6'
        b'N7GJ6ZHZ+mvaZNlkVWZc6jTujVmiUsZNFuR9Om8zWmzFcES3y+g6icsBp8msybyMV+q6bUxAucXWpY55lPFykccAA0eanpX03ZFRcOQ4cIcuS1hSWSSTCX1zamT1qyR1'
        b'sqLqUjyWSyXVolHXjDrwy8eo6GU1dVVF9UL0q6ZYVlMpqZcQMPfqmnphZQ3e3i0sKimR1NZLSoXFaxhkd7/RuOh1ZRT2lBkwLipdJZXhbd8DptqfZPe2EROtHJ3mlJat'
        b'GuBUVKNzVZJSaUMVOmdUiyhfXVNXShQZZic43h1eYqT3uoZD9ckpfQ+mndydvJ0GOw2JhzV+O1z0XnioTQ2IS4e5NmAf4vddJmMMxMbEQGw0zkBsPM4IbPSisdZAPGGe'
        b'/tbsD4Y4E6Dkp1ZL66XEU10bwEX30qTVsvqi6hLJ82PkD7dwtBZjX4sLU1NGatZukS/COB/xzMZ8VKBKUieaOOZ7nFDr6cDEdhE21GLckunCUulyaf0E0P2jqcAvd5gO'
        b'9PtZVKDsyWioFhZV1pYXiSciJUpYUo5uWYKqmJwcHXtN3CZMrtA3E3E1IklS/W+0yLQfaxHE19FMh0yeL6wsKpZUCn3RT3E6ut1aibSkHHXEQOE8WUNRZeUaQpaUYQrZ'
        b'hFSMJp20rW+oXlNMQLyWENS3ooUZBDoS1zInKEP3OrTNgoREXlFJeUUNbgpEEyK6ToJkwCQRFBqKKyWlWiEwupYclNZUS6q1NZEACuiYaSmt6Ji4jVPrhVUNsnphMWIV'
        b'bTMXS+pXSyTVwnChb6mkrKihsl5EpFDkpA+qkx9MszNHQmmp9oWF/dgL0wkd5nLdkbBOslwqQy2MhB2SiYSdAoQN2tfWUN0gk5T+SEyIiXx2LZlVIXYdXhuhIp8UNJqd'
        b'koVSDdHopBPshC8TeIMc2KQNA5hDwA1GjIxz9eAN4PZYszmxVvCmEanzlq0d5YvXoqzXrU+du5BqmIlOpjuYkBozwietE28Xn6df7claM9gF760ltVZm4wUbyrewQVp5'
        b'N6mKiRq/ELQtBi+BixMSq2fr1KcW9IImU9BhAG+Tes9MM6TMKMqqx74qYMWspVRDGDoJu2fAS6TShbljq031z9OvbRPcbwwOZ88ilX0nwGtgVDBVW2Gm9OMzRIbBXnAb'
        b'NoGOiaiETSP25TFU3jQFnYumkXpFgXgNijISrn4xYxevhmqYRZF9t5fgYXALtdEEFfvqjKejar0NLpjirVZiaYL/WxzZTVSNdMv0vfszTUCw1XafH1L9GyMtVZkK5Ywh'
        b'7l/qqJWfnz++rN/4nY4TZnRfS8xfv7u/5tf/4jmm7SwxzTApfH3R2/MPh/8j5nO3+12mD9/uvnTz9y9/9LjFpZB39fe3Xc/7/ooOaA3/ZXjxmU+O0Ulf1nccCnr08O0v'
        b'Ei/V3Ja/zPsgIzJM9HH0695v9cZ9/PqOz4N/czn06NdFZzcULuH+9lhrb9KjSusfKt2mHA3/6GuPb/pufdp27DOXrJbXLa9/O2cZx0pkQiym9lJwHxu/wc4XR9m/uU6l'
        b'cDcx5a+FO+FevBcMtJeNhTO8Bw4x+7I6584htbTD8/rcyKPcoJwLL3tlMKsC7SInxoZ+4MWxZnTwIJ9ZdtgCm0GnFmiYoAzDu+BYWDE4ysS3fBm2srDtG+4DZ4cN/XWN'
        b'xCydGQk7GIs1OL5+2Gh9F3YxW9bkeYhgvCBhA++NXZMohJ2MBf7mBm9sOIdXwfUxxnOws44BjupGLHOWWWkRw2vwpoystKCjDDK/WF0pNqAywTZDcMLP7mc2kBA8QGud'
        b'sjEaInGlFuWicQrlOVXhqShRlChFHdVd1WqPabTHNIJnSAKi1x/ayMS1ULr32/qrbP0JGOIctWMK7Zii4qdovIIwGKK7tvRI7PW4fluxylZMiqeqHdNoxzQVPw3PvW0V'
        b'eYo8paBjaddStXsY7R5G8BK1d3uRCZChtO4nMb7J5clqxzm04xwVfw6akZ5MbUs9lt6eji4y1l205kDMoRgFuqO3ytabifKudoynHeNV/Pgnzm6k6H94Y3fRWddTrmr3'
        b'ENo95Cdc5umNWwebOtFnfJzGK9g2hoOJ1F3DyXWc3MDJTZy8/OOu2sMRGse4a0/y7kVIPZXhsOL6Mb6zp7BYuSTu9s+d/mzbQ/DW9C7jaOq2RZzRT0GN3KbDPRzWmyeD'
        b'0xtpKx2a3jzUVnqwh4zWrlN9J8Bj/KmokVrazAr0tOnnp24hpu6lYepcx1BHNMYR2n4CWct1QIg6rfr5acKrWXo4iG4MTToldlyD/fS24hYgPfv56VmG6PlqGA9x0SYt'
        b'XU4MXXqa+r9FU5mOJqRyPz9NRbiNVCxdG/mOqOpFY8E+Zf8ZYcYFOhX5+akrHf0GHbFxXU+3/g85SqdlPz89y8fTg97csLauR4+ITRYzmGWNYWfurBKOHplI82S8uQ+i'
        b'5LCxHgKEATEe4MB6xk0mTaZNZth40GRRZjaMBzEWkfu/ggfxN57NBOaDuNJSHNS1WrJan0dQn3qu8K5JaLLHFMYmnqLSUjS1QROkIu1cmURpxRHwAoTL62oaahkrT5Gw'
        b'pKaqWFpdhMPIjqsSMavfMJCsX4DQTx/3Fh0TQF1UqLimpgKTii1RZDbHkFG/pvYnWDyGbxQtzKupwvNmxmCFIwFq8WeLimsamKC1mDMkpZO1Df6XXFMnlOAmKZWWlaF5'
        b'HpJMzAx09ENp25sEskXNtlwb53CCyR/+hya0JUXVZD77LGNGSITeFF7oW1NLgvRWTj6Z129XZqI6TkgIfeOK6yQl5dUN1ctlWssGiXY4IaEjfCCTSZdXE1YIJG2iV7E2'
        b'bLRQqv9UUjTJRxP6CWvVTd5DyEuOiBqew+M7hYgCsIlRWCoprsf3QSVK0PRaig9KJjM7EK6UkutlknrSdpFRz8EzyRjagpg0x3YVqUQW/dw8h2iV1msrYNqdnBm2gfjm'
        b'1VRWYrtHjUjo51eFDUvocdb4+U1qoSJPPKpG5tRIlXNQ81aLg1LQiFT9U6pmYH21ZowaGXlgLdTvc12POydztX53DRRmDltoSPetKV4hKakXkjc4cR/Iy46MCA7RmpOx'
        b'tZjpnYHPR8YoqJLoMZayVTXSEskww8dLKiXLy3A5kXBJSOjS56kyVPsaGyTM40irCaG41ycmZmYuWoSfbKLA1vhfbdGaKhIWW1KHh8EAYRVq52F7kB5Boc8mSPt6MHLS'
        b'6PeFz4y2DjK9JUjXUyYki1Hy4tFD4r6P60C3Dwue9PajwGF0tlK9boLOoh5ZLZMyRNWUTXjXotIViDNIe+ALSGzwokb8e2LZOLGVdVQlMmImlpaU10uX40eRlZRXwrtI'
        b'kleKxvfZSesUCxHf5NVLGpBwHa4AcbBUqG0iJKGqUI9LmifOL6ovlmDTe+kkNSF2YULbVjZUVUjKJ25/sTBsTDFyt6KGsrUN9RI0clSXInadX1MnI0RNUkd4tDCuoaxc'
        b'UtyAux66IK6hvgaPbxWTXDAtWphaXSpdJUXMXFmJLphXJSuqXysb8+STXB0xEck/vYGmT1SNVI+sqp9GVuRE9f20dokiDTnS9D/S8hOezGc4GdvIx9D9kzlR//HL6tDT'
        b'+OK2HaapqHhtw3LR5Oynf7lwuvfkDDiqYEjUZCURm1UHFU3OUqOriZismohnVYOYYvj5nlFHpH6xSR8talRlEzzXpAOaFrwKSTjtL6IPIJ0UyVadKPfNY8bYSQfsEWys'
        b'aGECOhAyR0jH8U1Hh5Jq9B+xuRCPQZGTilw9VK3R1YSOqSb0mdUQAC5myJgfly9OTRT6zsurR994vJk26WXDgF3MpUnziKTGJ4S+qJNrWRy99smboaEOqcglaLRI0P4K'
        b'EOrpdknzcoW+C2BXeR3qpIiW8MlJ0cMKG6ls+LSWKF1VsoqGOtl4op6l7k2mXhJV8vk1v2EVLW7Uctfz6TAE/SxamIW/hEtCg5c+/2WhzGWh5LLJ34YOVk2rQmqP8dT8'
        b'WXxAMNfQJfgLFRxfbnIpliKpq6sOSq4rakBJZWBQshRpd5NLLVJ8clmF65lcPuEbTC6gnnVnJJWSypEShmT/5KKJ0IZ0ttKJyZis8ZAWK5HUY80CfyMFK+KZ+l1xTWO0'
        b'EO/CQPpTGdZa0QnU5pO/VHwRBrNjriqqFOKDZ15RIq3HHRKlz1T3GAQ/XJL5QSoOwHq6OCwkIgJx2uQ0YfA8RBD+eiZHlhWhp01GQuVZhQj8HnpD+Eu4JGLygloxpxVx'
        b'z+JoHTBgtDAe/WI04SWh059Zfrhrk0tGL2c/s711cIPaK5n3M7mwxiCDSEWLj8tCr2dyiVgsLUEVpiagW0/QI0ctKRtRky4pOywhjoZU8Kpc8YwVbGYbmws8F0kgmcAt'
        b'0D4CywQOT+GTi37J1cZzi/DKWxCghduCJ+BRj3SbMh1SFDgJ90E5KX/Pz4EKoCir4Bev28VY5jPoVLAHXoWnAsEBDCGFAaTgHbif8WK7NQveJRBOcFu8DomPDS9lOJPa'
        b'1jRoY8S5HFm4T7qKavDH9r3sKH9UMg0H78ReO6A7LXNuCg4egJEDm63hg1yqMdx4eQnsIDg1Jn5ZOFRAo7BcYvu7hfmlTVTDDHzrUyn5uvVZ/TgBuKIUsuAm1oYKAMfA'
        b'Pmbhey84ZiaamUjWZaQ7r3/FkZmzKCpi13enD1zJgrFmO6o+PRieqVg6pXCzQ2z3TJ6L1Z15iQfO/6nJccc21q5Xptx2f9ekI2BDaruia/W86QFrBk98+f3G72OuBVld'
        b'i399IDi112Bd0B+2RyrNN0s8vGyuRm2N+bjLfZPL327cU7+UEnb4wPtv9H1g+OfPxc6m+xzzXb++kf1+7C/vVjXM+rr4s8uFa95a+el3p2Szzu9N/N3mJ8mdt2a8Lf/4'
        b'ykeioVn3Ss45HWx0zV94qtT0N+93q9+u//rKuj88+GRI9ulrWX+l56ZY2tnkZAl/2+m3/qOlM27BgCuPX/nrP2z+Wpl9iz3jYsr7J47UPyxRfrbXJODJtMZNH+7/0vpE'
        b'lcU12dddx//1ivmpf71v9q+O6T/wxK7p7PvbREZkPTWKlasLzQrug5e1+CH3NzDIKS3JoBlcgAcddQgi4OoS8BJZa10LN4N7/nBXdiro5oKT4CplUMn2qAYHmLXWi3An'
        b'7NQhiMBN4CW9ZWNw0oMspK4rBbsmWUYVBuP3qltGBTfgnafYvLymCG7H0QnWgpdGBSjQRieAXfAwuT3sFMLNMswUYl9wbTouCvdjZ6sWDuiBO7wIqArozoB30jNS4aU8'
        b'FsXOZfm5oS74c4Ylt6RGQYKMceA2G7aM61BBrmgXcHNcKWGAyi1YuRKHsXOS16tIGDuNE44eZCfS+PjKzRhEaS/Fqq6AHo7aIZx2CMeZ81gaH39FPfa36bHtKe2NuF7Z'
        b'F9YX3xdGR8x5FJHZH5H5sEQdkUtH5KrFebQ4T+WTL+fK5x8z0zi5KQzaZ9JOAS2JLYkaO1eFl8puKvpo7+qv8fGT41Ino9uij80cLvkJXhydrXaMpR1jVfxYHAb3BWWU'
        b'yn5aC0djay8vpV0DVbb4o42TQDv5qx0CaIeAHl6/wzSVw7THrn4q/yy1azbtmq0SZA+yOXYhmuCoHuNeL1VwUp8tSpgPdkHyVdqqBWKVQPztYycvTFbISKJx9ZdXKRPU'
        b'rsG0a7BKEIxXQgc5KAN/cznWYg1f3JJI870UeTR2wBGr+NPQp4fLfA9/vn3sIMTIKuKRROPoIxcrOWrHANoxQMUP0FZtLUbfsmDMb1zrBHsK2pskBHOg0DTBnwP9efh3'
        b'uCDRgnrVwiTRl/OqwDTRk/OqJw/9ZhaMLZkF45E1Di/qJ+IDjGG2kRXjZzLbCrxirKBGwI/nOrFYuBF/ruRn84b5jJogEg8ZNkkkHq42oBmviWoy0IZ1+N8ENdsmYtf9'
        b'iRoTH9ltgjHdmxnTOxdiR+rgUOPYwozL6+cyYzq4joZTpawBgx3u5VKwLQ3JMNYGcBxsHon6wDIAO0051CpragG1AFwBmwmCqP8LgXnT4Hl4gVzJgncoeD0ZbCP3aonG'
        b'g/HgevPgonW/9PFjMApc4RHYgVEApsO9FDhKSTLsyJBfAA+Aaxg1AEnZ4xQ4TJXALe4MFEAh3tdlJTIUFprt4LEZX/5bBVYYH8CWqi00mzKlkvES747Ae+Aia9HJgF+K'
        b'TZmSfcsxFEDOUm5OYcD61Z5MybI5+KQwA52s3OgsYEpuTcF7s4yMLawKK/cJ/ZiSs8iGrd4ZhlaFGSEhQubk5waYpD5fjrAwo8dvIfNkoQvEeTnudjk5qK0SKbAZnucx'
        b'8LYnQQ/YEhY8DbQFoz7Kgl0U3CxOIE+9sH5hXg44AXeh98oGZ1BGIDxMcPtmwI4pOrQBLrUW3CBoA+BYBaMgnQTn4Y6w4MXTdWgD62EXk7MDboHteRR2s75FuVPuUAGO'
        b'NOCeWW8PWsO4VC1oxWgPK9cwQAR7wE0KYwgUBWMEgTx4hYC/wlZwfClBCtiGqtNDC+DAu+Q2eeBCY15OEWwRcjCIop0B6FhvyQAObpsVrBci3jmAoAXAoyWMNz9u6P0O'
        b'GEtioYVhYWGGmspk2vStqXjHXXmMQWFh5WveIQyWxGLwAPTk5UC5Hd66DbdSRdqoUnVFfMqX+raEii2cOZQXxaiZKVbwZl7O4tlAIaKo6A2msANpkKcYDbQL7CmXmcMH'
        b'bmGoxdjgAgXvlRdKt31QwZHVoo79oeL10/m3kEpmdWLp+7ecfbye1PLubz04W3HG6Q2P8LmfnWpItRbxzE8lXHrvW58pM4b87ixuFbx79eKJj96adfJrh7uxJsZdlR8F'
        b'KmKmcOAbfxR//GfrmG/D0qN27hU3Zjlup9eW/K7n1Na0OTfP1KwwfmnoI3uu0OHdAV6jb03AtYzocsnNA9Wd135jv/6DlPPfL160bOXTI2Yb/trf8XDpG5Z1Hzr03/lV'
        b'WLHhihe2PUnf26dUq0PVSY2fXvnYNv5To/jshM8uGPF3rRac83u8KUoVnOBZ9rLdmSOrdjo5n5ebv9OkdOw0+H3jFNuzPn/+eu+qX+ffeVBsPlD0Qen7Ph1dZll/sp31'
        b'YJ908ZuurxlnDbW/1Bz6aal0oWwat60DVt48+guBZ7t32MUjB9Q/pM9LuxcyQC0xvfyrr3zkfidCWRe+PCM9bZTc7yArWFpx4LFyw/aXfzgJNhz+xcHZs8+9KTNvWFzj'
        b'+vcH6f948PGS/O8Pfv1kww3WB8ZbPja0edi07MMeEf8pCd98eInz5BvYGL0LnIGXsO7VBNqJprgyEm71Jwodyi/mG8E7bHAAXMplwgvsaXDwT4NnxZkZLIrrzgInrOFO'
        b'RoeUWyfrwj5R4NYMEvYp1YKA9uWXW2F0AWmhHr7AEhNGgTy7yj09w4ca7/ovTOIZp9iS65fa1YLm7LgVIx7/8Dx4mVALbvnBU8TnH5zh6dz+w4QpjJv4PQsZ8fgvhfdH'
        b'b3qEx3KZy+/nswgyAWibMwxO4GHSQLYxToW34MvoetvA8WgA67T3R7SeEYILGXAnb1h1BjvAA3L/kPxV6aODNSuh3AJs5cSD00uJdp23ABzRhwHgSggIgD0D+xcM2qrT'
        b'R8Vx7l1msYGTCG6mk02M4DzoLMRe8Mfg3rEQAJ5pDATePSEiCO+V7IbnRjz8K8Bucv9i2O0wHI2LAnfmMOG47r1AogHBA9bwEL7YHcrHoTug5tpOlPVwK4gjhKH5w4OM'
        b'iTaFgnvrRUbPrd9g6SMU6u+H+4rCoXpGFBtZQam0pJ5o0pZaH/xcN2qKUwsPB2421Qi9aGEwA32lFkbRwqhBysNaNISTlhQmOlfjsVnts4YjgpEI03bHFrcvVrofW9aS'
        b'/CRoOg4Jdm5j98aWJLmvYr7a0V/ND3jCd3vEn9rPn6qoO7v61GqNwEkjcFXYH7NEddACcY9tvyBcJZjVy1cJkvr4TKSX/K5FPSy1IJQWhD4SRPYLInut1YIZNIHcard8'
        b'JBD3C8TKIrUgmBYE99ggVd6WFkzDeRbaaGBzGei+HjaONUYLwhmnvBTaOWSiWnvjexN6E2hBrLZYe6Za4EcL/B4JgvsFGBGA4JJpEQEEkaMIj+11UAnS+pLHnyzvS6ET'
        b'5z1KXNafuExVsFydWE4nlj93MRddSyzrQQ8znRZMfySY1Y/aCT12LCHVVWGL/hZ2uHS5qHEsNBfStCMf9CSJ7anHLNotFHVKlqIOPdCzM1w1AjdE3+A0p2D7IcrJ1+Ep'
        b'Tr6JoASuB1fJy9UOPrSDz9B0JzsRxrETYfQ6xB/4VyTl5nGyvK1csU7tGka7hiF2shUMUqbWEU+8pp6dc2rOs9+N27NfK2kH2htDFgiiaUH0I0FsvwBDFmhB/UYYSsdX'
        b'g9bGYvQIxt7oEVDyjc2oR1D6D9kae0cgJp16IHOQTwlcWszGR8Z69i5UEhnrx7vbx3gu0UBpfeaT3P7H7vI5eNr0FCvi+sFmDSj9EHA8bYgPrtbPDwedNRgO7zE2KNB/'
        b'Jehs3TfUmLnCRIGBDLNI0E3bsJn+KUiPyzGAh1PQeJuWmQHO5aeAi7ApIFBkQKXAHYa14KIfA2f/MtxeMleIFMcLZMM8p5IFtoCL5lrkrwquvyES33A7QYK6zSBB2ZiE'
        b'+mezKVYuD3SgWYcpGoGnzlzIlQ2hvKTp9/fOvWMBgs2ut94HsuIt5qte7XMbNHRR2FQeEwgo4x2lcQEHFlpXnAn8Z6pZbnOux419oa/el63/dPlTdusXHWbNT4w96950'
        b'mPfn8NWR3eafRobt+uRiC7z27Tzv2+84te0z37Ch7nbS3/rpR8lvRTp9H3zwnbK0KfKHRm9kylt3n8o9NXdzZtsPi16pvut9Nvw3L3TYxewo3v3pNpHfHGtX2/jVbd97'
        b'pqQ8XrpqQ/eDpfvKg+5FpGx7N+3R6dw68aqyP32/MfdX74g539zjuiifePZZrK/8a3fE2X+8dLt151/49rUmgV+8GdYrjE9eVNf41cqs9943vJ5cPA+KLIkqYQ+7wUkp'
        b'nzQ8mmZOZ4FLErCNjIU5YLsRHr60zsPoN3zZlr2hUcL4K2wC5xeT7F1onIcPQJdBFtsZHgfnyFC8Ah5Cenwz2FOE8gNTSSFT2MOGd9GfgtQwH5yKgtfQ6Hp9tdaaZQzO'
        b'skGnxJYM9nZwi1s6vFoZgIFxd2UgVcY0lg3lSMk+QjSNSnjUHys6QdliNmUB7iNFxQ90gFOMO0MvOIrB2PemDwcQhT0v4hiiiNIdRHUDD1LdEf2pcC8GoN9osIzt6Spj'
        b'1KQzsNPXn+DyiANFbBz0c6slPMkB21egpiFajgJuDUrHWlBQFo8KA9sMZrId4IVU8lzr4UtIIRlmW2N+Cmxig44cpBjiZt0YSMJc7GUaTggOG8SzBeAkUkAIKtC+DfCe'
        b'FTwwBn0KAyoTtTIvG3T7a7GUwXagNABKdsDMWf8xfq/OfMLIPCOCtDgs82RFq5iAoqe0lro0d4pvf2j60ZiDMQovxqcCG4yilPHdcy5nns/s9VIHzKYDZpOTffG/SANp'
        b'D+vVifl0Yj459djRXeUxXe0YSTtGqviRGGHVrM0MD1xIabF1OBp9MPrAzEMzH9n69tv6Ku3VtsG0bTAO5umvcXSX+yi8lBzlC2rHaNoxuiVBM9X/bMWpio6qrqoRq9gx'
        b'EzlXXoqGEFyxIl8Zzgw+KvLR8B2Oph5MPaAFrGxJf+Lk0j79ZExbjNJL7RREOwXhOnw0AseTRm1GCj4mTG4x6j5sO3+SaO/j4i7PV3h0+ZwNOBWgrO/JV3tE0x7RvYlq'
        b'lzjaJQ7VNsW/L1fj7HoypS1FkX8sqz1LnjXIQWdJFkmGcPKUGnVuogTb4CY6PcjR0STDwu41O/uk6bzXpnOTZhi/FsNCKTMIGjOD4N9+dCRk2AMvUAwb1yZlDjcuKrqJ'
        b'0sFwrhP+aEDU/1J8VBIvUsQd437NHJLHZ5PfWSKbsZAyJixKH1fmObxZzrNItO96SZWMAYb5Stc6Iuuf0Zyu9zJw828a+495KZfxSxn2rnfH2smv2aMBZLhccyuMcWI1'
        b'aEZZ2DUtUHAUCfI1PSV9eQ9t+1I1U5wV/r22vXm9xg8TEGtazMW4Ryh9StJBAyomljXI8cFYMz+aDPH0ruTis7msUcgyERhZJhIjy0RiZJlIgizj5Cn31VjhcKYMNo0T'
        b'xqZxwtg0ThFN6WOQZaZhZJnpGFlmOkaWmU6QZWydWlANBHuJH4IK2IahArZhT3HSlDCmQAwuEMvCJWJZT0lKyujfJRjfJRTfJRTfJXQcwM0EBYxI66KeaJHJkst6bJlf'
        b'TIqhnOrlifJExRTafXqvMe0e/8g9pd89Re2eRrunqZ3Taed0jauHvFQRRXtG9U6lPeMeec7p95yj9kylPVPVrmm0a9oQh+WSjl+PIAM3MkpR5x++x6BBA8tcPEj9POmQ'
        b'Ia7zqX7N1Zwoc5dB6seTVSzSFHJPlbmr2tyVNncdZPPNkZD60WSIQ1m4jS8/Am8SlgePyeDmjGFTDo8yd2TDVnO4VcTKki4yeciVLUJ94talkg37s7O3xlq9tnyR/ZH+'
        b'H06Lr8+vWDd0vHHoD290vrGteZdh1Sn3r4vbgp/89lvz3qfp0Tlp6Xu9Fwm/+v33b/3uS2lASdj8K3a/u/KvzZePcAy8Xuz/FbfvyK//Ejfk9dWXn3+UleSpSa/98NDp'
        b'r/adaL5t+9YPubcc5m2YX1c9/x3uky/K/HP/cbPzHwVzTtW6Vb03tCzaf82Tjrzl600+LZ0zsP4lcdzH5kf9G3qvH6qkW8+2r/47VbPFeUXe/u/CFe57yzNYb0mtb39W'
        b'XX/evJf37qyXvu9K2P7W3tfnlwW/oWl9N6f3UsLmqvkz3FpW/lDVsJPufhr4+b3ZtzMCTXd+HDh12sNP9j4+dWDBqr9K0xzCO/37wy1nfRG2PKfmwNBv568uMH16MKs0'
        b'ZOkH2wburutdmXtH0ynf2Hs52/bqsT992HTuo+hpN96sXuN/4YtPDt/a1LomKOs3oV90/PrvTyr9OR+4tg86vJ3RsPGjYhGHLCZGwyPwPGyOX5fBoliRSH1JNiU6VE0m'
        b'PKAXSAHKK3SroNHgKvGd5YHD2XhNE17A69vjFzXdCkVeY6Wg0TOT/4bM/TektBejUcWSf+PE9RjBPWBUUFBZU1RaULB2+BdRtd7lDHs2ItkdTpnbDXINjR00ljZNspbQ'
        b'Xav3rJa7717ftF4uk8sUoYqirmnH1ravVc5t2yjf2OOF/up63a839M693ngl8HpgX2Jf4kObV1JeTekPzVCFZjwWOMpD5UXt044Ztxsr0tSCwB4HtSBSNTNL7ZClys1X'
        b'zZtP5y7od1igcljw2F6osDlQfahaZeU1yKEEC1mDJpQNvyXukF1TfFP8t4OGLONUlsbGrUV82kwlTlYL59DCOWqbFNomRWWWgvWVSGtjr0HqZ0l8fYyRZPqpyRBOno6c'
        b'y2fNNHYcpJ6VtMwfwl9PR86+yPLCP5+VyO2H8NfTkbNZLMrEapBdxzVGIuz/YjpE0qfMbw4ido+9ltx6Y0owVWmqdghrMhs0MDJGqtpkiX0dx9gZ1fdfTYdI+lT//ApD'
        b'0rq55Gn+/0+HSPqU+a1ry7GFZNh3b3fc7HhbCtg6xou1q+IuA+yCgn9zFfy/I8iwHC8cvY9jItXTmo1VT53wwjNg2aeU1jAWwmJZYQX//17ys/lz4wn0ReM4DvUKxyLO'
        b'miOdv5riyW6gk7YDplV7o0zYcVZJ6wpe5yXWQt4LWR/bGYR89rbZLzKUNZ8Uryj90NslOZ/r//e/KX9Q/nIPXxpa+saBs7EHdl/wlYgORu5Oe6/r2zDDrx5/2fDRkNRF'
        b'4l3z3cm86pbzbunvHFnbun5DuPPx6y/Q51p/+dI8WZjo44cxhhbmv8v/2P74e2WPe9JPvCfx4fHDzQIW15Z3mu7f5PqdoLDJ+nV54e6mKHvfnldNKipXtfafZP/u2uPd'
        b'vRvZfb3BG3cZiSzJ8M0FLXAftq5kZ8P93AS4J92QMgVX2VA5CxwmJSJXgGugeV56thhewcWwFcYa3uWADjMtgAY4kgOPwu4c0Az2w/14BQQvtxlSFjYcV3jeghhhjF8U'
        b'padm+mUaUrCZMuCyjeBVsJ9ZWdsB7s6FzUEGFCsPtsIdFOyclfiUQMdvg/um+qfxKFZ6KjhHQXkOOEpsJ+nL4D4c/28f3BNWmYkjHJmK2LAFdoOtBHh7DThcKWPy4VFw'
        b'hZQwSWWDnoWgmUHT7pGJFjqnE52SWX+ygLs5WW7OxOiTALtAO+yFV9P19hXeBi8Rg1M4hpbGpki8Na8Dg0OjIma2bHgdb88iLVYFd6WAZlSkFhW5V0JKmIBrbHAdnCsn'
        b'K0f+8BK47QofoFJXzUDT6pUN8NpKs5UNLMoB7ueAPUFgN7mZATgMD6QTEPPUQHAqEweyNAVtbHgKnob3nmIFBO4Dh0pwyweli/1S4Cby0PvxCUPKyYsLtsIDASLf51at'
        b'/k9qWnqiypfoXLG6f8/QukahShiNAhIpYumBSWDp5UjxbDdl4T+NOf+RuWu/ueuJRrW5L23uuylZwzXZmbElQ2XtfjpSzQ2guQEqboCGa74pFf/p/XBTjf5ouD6qiT4a'
        b'rlg10UfD9VSN/gwaLLbiodHk/6m0UUiZ8Tdl663HuA1wKiXVA1zsRD3Aq2+orZQMcCulsvoBLl5iGeDW1KJsjqy+boBXvKZeIhvgFtfUVA5wpNX1A7wyNN6grzrsczHA'
        b'I+7OA5yS8roBTk1d6YBBmbSyXoIOqopqBzhrpbUDvCJZiVQ6wCmXNKIiqHoTqUwHWjdgUNtQXCktGTBk8AFlA6aycmlZfYGkrq6mbsC8tqhOJimQymqwW+iAeUN1SXmR'
        b'tFpSWiBpLBkwLiiQSRD1BQUDBowb5cgoLsOCsPBZ/4TCEX4kiQm+TDyKFSf4h7jTmsUq5eCx7P/l9GcbhrFS9YqJcZyQekVoERfI+c6oDPt5l5QHDlgVFGh/a3WU7xy1'
        b'x8LaopKKouUSLUJkUamkNEtkRGyBA4YFBUWVlUglI28GWwsHTBC31NXLVkvrywcMKmtKiiplA2a52OW0SpKEOaUulq1lbobN8Zv9zmhmVU1pQ6Ukpi6ZzeBLyDagZJDD'
        b'YrHwM3MHKZxYUKbmmwwHuZVWLP4gpZcuc6eMrR8ZOfUbOcnT1EY+tJHPIMVmTVMFxPRN7Zv6iu+rvqqANPTRGFlpTOybAlQOYWqTcNokXMUN11BWKsqqRaCmHGnKUaX7'
        b'EPL+PwEZggE='
    ))))
