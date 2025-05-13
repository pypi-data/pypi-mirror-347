
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
        b'eJzsfXlAk0fe8JMTSDgiCRDuIGeAhCvcXqAiN2iIWg8wQIAoBMyh4lW1taJ4gEcFrQXUKl4V64VVq53ptd1ul5S2IO127d7uu/uttnbt23ePb2aeJAQIdru77/t+f3y2'
        b'TOY+f/O7Zub3/JKy+8ey/H69DjmHKCWlp+IoPUPJ8KP0zGWsBS7UhH9KZjKD9kVZYtR8FMtaxplKJVtiMtFfNSo7m7mMO5VSsq0lNIxlTlOpZbYaJFQtx6VWyv1uE29O'
        b'VtnchZKGxmpTvUbSWCMx1mkkpc3GukadJEerM2qq6iRN6qpV6lqNnMcrq9MarHmrNTVancYgqTHpqozaRp1BotZVS6rq1QaDxsAzNkqq9Bq1USOhG6hWG9USzbqqOrWu'
        b'ViOp0dZrDHJeVYDd+ALRHx9PyYfIKafKGeXMclY5u5xTzi13KncudynnlfPLXcvdyt3LPcoF5VPKPcuF5aJyr3Lvcp9ycblvuV+5f3nAIUrlr/JReaqcVU4qNxVb5aHi'
        b'qYQqV5WLyktFqVgqgUqk4qjcVb4qbxVfJVZxVUwVQ+WnClBNUQTiBVjprAss8x+dVF1QEKUKHA2rgkb9EiorMCsojApxEFtDTWcFUzUMl+elzOIq+6X0Q39CPFQ2Wf1a'
        b'SsorrndG/uW+LPY3TOxbUfjc4ijKFIq8kdO1sBXuLCmcD1vgnhIp3JOnKpWtAXu5VORcNrwDrwZJGSZ/lBO0p4Grhrwi7wy4F+4ugrsZFC+PCfrgbrmUafLGOd4ALWBf'
        b'QV5sHh+e5FBsNgN0GU0mX5TkzC/F8TK4E3SVoNIcyh3uYhXnJ6CieJ3gjeV+oBXuik0H25pQh3bncSgeuMwEV1Q801SUYb4C9KIMr7mClrWrTfDyatfVJgblA/c1gmMs'
        b'sLsBXkfdxAOCR0Ff7EwOaAX74gpk0bivcB8OOVH+YWzwHDyYWcWwmy5/63QdRM4Mv3I0ZWgd2WgVKbR6TmilXdAa89Eau6F19UArPAWtvxCtsxdaYx+0xr5off1VAQp/'
        b'y/oyypzs1peJ1pdht77MMSvJyGKS9Z0QO/n6+kxY30B6ffuUTpQrdb+RIVlRGBS8kCKRralMik2tyHSiVsQuCFbTkZlxzpSAuh/lvmJF/YZUAx3546lsypn6NtZ91grX'
        b'zz3KqDNUPQ9FfzpXzH7sSc16KGxWp/lfSwjnNzLqMQZ5LbeD0edESeJ9dc2+Qf1lpygSPa/+K4+DHoyoh9Szrm9KXGe6UiOUSY4RCrgMrqOlbY2bHxUFd8XlyuAucKYs'
        b'Kr8I7ouVwxfB9TxZfhGD0nm4TK+aMmaN+NYhG/Ea8S1rxBmzPhReIQXftgbsf+Ma1IxfA6cJa+BarMeTaBIhZ9Yz8LxygWwhk2KyqCp3eIwLtpo8MWxu2RilZFJUKAW3'
        b'zQwFZ0EXidbG4PwoHp5IraPmwkuL6Nxn+OAoPICweRw1FxyKc3EltYMTcDu4AQ+gCZJRXHhQthC+SLafAVyDB5VF8+EeDsXcwEgEJwKmgUumSFzmLHhpI95WMQVoO+ws'
        b'nB8FzsTmqpaCI6UyLiWHZzhgWxw8RJoFx7zhMXCZS1HTKOdnpoEbRu2eZWKm4ROU5n7q24b2mzwQL95e8lHBSM7qqDTnbaIsn9TWo5dbC+TKyCk/Y/vUdoGfnX7kuzFA'
        b'+dlblUceRP72pT/NDFv6ty35/N7zYd++XLDwqjDjevqaxvs5W2PMv3qPyis7dSl+ZHP1S3mMIlGc9pcV156Hb6WdiZi6ZW21ZPZ/VLz9zbUXr6+e9ptHL+T88mrN0RsH'
        b'm84sNid/s3/w79WNp3PfSXnw3tp57tNWflHq9R/7b+tK5jmrPh5scD2xs/e0x9eL47ori79LKvm4++aNzfMyu5zfdU30OvPTv/71DwEP/pN1592o2KI4KeexBE/3G+AQ'
        b'PFAA98TAPXCbvkiWH4uQkCfsZ8Ed8Ao4+xhjCtgdA+/E5MtgD9wCW/IKizkUH1xiwmNJmY8x4gV3VmTHyKX5MXAnwXIecAurIq5xNTz7GJOguVVxfDzzC0CHCeGmXXFM'
        b'agp8nQUugBvgBmmgFlxjoIXaBffB3SyKnc4A5+B+cAlcQgjObYQZJdULUK5/0jG4YdiWbBn9N+I9rUbfuF6jQ1ST0GM5oqWaNTNG3PQaXbVGX6HXVDXqq/UYMJi4BiYC'
        b'u2+3UI82Mihvv46IA8tacj4PCO+u+TRA1u7cxhgWitunD0umtuV0JBzIu+cV3M3pNgx5xZi9YoYlEb1eFwPPBPYZ+ucMSrPMkiwHue5JQrvnnuDZpfRyetcORKYOeaWZ'
        b'vdIsyUOSRLMksS+pnzUomWZfi3HIK9bsFYuy9czu5ZzIP+FhXxO7t85W07Ak/LR7j3vvmkFJCp3nV36hA2HJN9j9qpt8c9jsQb85A6I5jwKpQPnDIErkczitPa0jZ1AY'
        b'OuAa+jVGAnqMBaTuI1x6jkacKir0Jl1FxQi/oqKqXqPWmZpQzD+5Uu7IWTFmqfRTcKKn1ZmJc6Uj5z+3UE82MBgM0RMKOV+6+7Su2sJ/yOQwRPf4nq3pX7I9ni8adva4'
        b'5yz89hGH4gisoe8MGGEd5cZQ5/gprDHozcZAEnzLOUQtw+wjYh6VDD1LydSz0R8nntJz0a+TkqV3VvJUlIKhZGPcu5KhdyEhDg7p6RQu8WMszVAxFSylEwm7Ep6JjcLO'
        b'JOymdNG71zIR88gf4S4gs/pAibpQTKa6imXXRbYVA9fhLjJolu4Qrp4iDdBkgFVmx7/q2IgMsOzIAHsMwmdlsQkZmBBrIwO148kAawIZYNOkuEbCpraIEaVGtPQvHB2l'
        b'/SzvLMOgRineI0WXq15+XwAC3trikr148dZqqbDt7Zegs/AnrDM1b5YFvrVX6v3+Ct4nPh/08j/6ccvyxvjZUaH897wjOloYLU6LfMFJhiact3WZ8K09G+vevloYf1Mk'
        b'/mhrW5Ib9cxO13PfvivlPsYMFdg2F16JIQxQaiBmgWK4lAc4xVoPzm2iMxyDF31ibBwSi0I4p8M1luUEW70JJkI04yjcUgBbCxFPKOWuBecoZ7CLuc4FvP4Ys3SZ8Ajo'
        b'wTSlIA9eLgIXKIqbxvQFhyMei3Hp/dpy0FqSFyun8tgUB77EgK+Di/AOSTRkroyR5SJ+kAO6EyhneIUJnocd8JSUM/mG4FhRF9kHI84VFVqd1oh2mwcNKHJrBEFTKyiC'
        b'ph4amVRs/MXpZ6b3+5hjssyCqDb2QdeOlcMi8eGC9oIhUbhZFN69clCU0JdlFiUj/BU0tWtV56reqb0JHY0oL384MBj98L4Q+ljKdLM/EYU/ZFEisV5oQwLcEbZBU18z'
        b'wsaSyIjTGo3egIQWvRfO4G0bAhfv6RV4V9N7GfO1esyzLsWpCuT8F9rLCMUyQn7ANv4aA9whbjj1Cj+eVcV0tEeqbXuE3iEKpmV/MMewSaygMUyQ/V5BO4GZxSL7Y0Ks'
        b'bX/Ujd8ftg7Y7Q9TDPLDk83wBT6is60I+lrj4D5lLg1n80tL4VnCOs2EPdwpVXC/9nB9JsuQjQrtMd6+XHUEbR0BEKPNc97XV+z5n2Lx8U711Dd3h7i+Xu/qemq3YHN0'
        b'aGkk/9SHkjWFlwT9ci/uh97Ujw7/3o/bZv67lE0gFxwCh5IwYKfDbQS2acAOET7GK8IFu+AFeBkR8H1wn1zWZKHTfpvhvhA22A7PJz/GLDhn5kIC3zR0p4NWBOBwV8hj'
        b'zKLlwG7Q4xFaUCJjUMw1jCy4G3RJmXbAjFfJCsmIWtRqjFqjpgEBs6cNmG1xBJ5TLPA8BwNeh7FrQ+eGQWH0537hAxEZ/WXmiKxBv+wBUfawj//h9e3rD29u39xdPegT'
        b'MyCIsYNSjj4MN8jWqRs042GTQ2DTBpqYYdfHIafKCprfbaH+PJvFYIh/KGge4IZSJ/hy1v976NsheOKRwwPwZXDbAXzCW+AqgtFRAAU9CNHN0VAcAqHXm/9GI/dxEHoj'
        b'bDyMVjkLS+P4p74QcE2Szg/vdjKoxQ3cU57LpSyCIOGd2eEl8I4N+dIAWlv+OAQlVi+Hl6zwuXqaPYRi8LwDXqOBvBUB4YFZ8KQdlCIQnb9MyhqPWlkEGkfB0eAAHA1j'
        b'wDHBAo7F3wOOoQjfHua18zoUHwkk9viSQKI+HjfIWaOuN02Ax/G4MhU7acipo+xwZRECyOAfAJB6LAw5xpEEEFk2HImFS0rB/m/BkxPESc4EQOTQgAj6wTUDVpyUwRaZ'
        b'TD4/N18FW0qUtPSWiwQ5OYMywtsuK6q5NfCIKRoXOVoLLzhGrTTYruZiwM2GZ7U/+c6VbWhEZf74u/+6XNWJ4Pb8WwhyQfX7b1FcP8GukO1Ht4YcmfK+2rlGsf01pe9s'
        b'8XbfaSJf8VfibN/sxds6xPFbkksbeKWfLxLVcWM+dz1Vyl2ewuU+n/dc+OeuPIlwOL7I+Rdvifhbb2ZtDTm2FbEogpf5vz8iQwIXFobgbj7YS8QhkwzeFtuLQ/H5ZBs0'
        b'gV0Kuz0A3wjA22BRE9kGCNLP5U7A077hln1wejOpYhES616mt4AIXrfuAl0yzeJcAwfBGxZWhHJuRAwKYUUOw1e/lxWxseQjXFMTFppG3CybhQ6SfbKE3iePFrMo8dTu'
        b'sF72kI/M7CP7HEsaMwf9Zg2IZn0WIGmbg/B2t+J0Zk/mJz7yz4OkA9Ez7orM0XMHg3IGxDkIhANDHnKpKV54Kw0JQsyCkO6wTwSRdhvKid5Q4dgZu5Ps+u1EWXC8VZjI'
        b'wg5GXA2URZhAWP7JIozlH1I/DNXTO8teaTOW+2ARpQ1Rq9nQO6OM9d+ppJmI3lnF2vPTdjMNuEetyWaCqz/o/qkYHEdw740wdqFvyBV5DGt2UK6b8NQRycLY77qvxD+3'
        b'g8eaLS1dtFWwxn/bcMLb2b7qP/8mYV7U84kfvXCO9cwbK11dEbi7hpzPd+1pWnsmvukUiyoI5qevWo74DawUcIYXQesoHBfDvQSdR4DzhJOAR6LALRpEhRIrhC7zeoyX'
        b'0HcT3sWxeXCPDOzy4VLccmZocDkp5jJHQXPf4AJ4QUVz3wbQh0DhHxAvMShIJHb8NBJeDUY9QvnuoygfhwkYL6PB+GEdi/IP7vDuCe2uPr2qZ9Xg1ESzb2Ibdzg08nRG'
        b'T8ZQaJI5NOnT0OT2AgTR4oAufid/SCw1i6W9YYPiuLYsJHJjORsBTljKIy4lDu9eOOgTOyCInUgZJoVhQhfsQDgPO/nIMVEWuoDl4VoEwp4/BHoxQZOyRjgVhIHn1mg1'
        b'9dUGfQSOZRY/+BuCa6kHljkw64QmiVdRQR9UIL9rRcVqk7rekuJRUVGj1RuM9VqdRteI5H9C45yrEEaobdQ3jzhbZAO6cn0hZZUDCMeVatuVeFwjXngR1EZtVYXaaNRr'
        b'K01GjaGi4vtQk522QGx1sBRtyMDL+AJ1X+jTgjFOS+6wjy9yvP1a5g17+bTkPGFz3SK+EbDcYr/hsdykT3hct6gnAo6b7CsKOWSRTIT1XZDNzy+Ce+PyPcErDMrZlbkC'
        b'boFHJpA0/O9rjAJnMByoEFh6jpKt5Ci5cqae60s9Q02llE4LPKgJ/5TO1pMl66/eWemid6nlIYmDP8Kdq0OsSfODTSjhO9EcTaXW2KjX6OIK9Jpq2vtAQNbxAcYD33ku'
        b'1OjXm2oNTWqToapOXa+RJKEk3N3vXAs1xvVGjSRHrzUYzzD1RSjywTtoB3zT6UlRBY06Y2NmMVpmSVRWtV5jMKA11RmbmyQqnVGj12nqGjQ6aaZdwFCrqUWuUa2rdlhO'
        b'pzbCW/p6uaQUwUQjKruwUa/7R/I5qmyVBkGcJEtXq67USDPHpGUWmPTrKzXrNdqqOp1JV5s5VyUrxJ1CvyqlUZZXXayXZ2bp0IRpMssQm1cfl7VKXS2XzNOrq1FVmnoD'
        b'Zv7qSbs6w5pGPap5vbUNvTFTadSrYZcms7TRYKxRV9URT71Ga1yvrqvPLEE5SHNo5g3od73Jrrg1ULkW9w7rHCWWjqAouWSJyYAarrfrvCRh0pTEzAKNTrdeLilo1KO6'
        b'mxpRbbr1atKOxtKeRjIP3qo3amslaxp1E+IqtYbMMk29pgalZWuQlLQK1xtliZJa0yTzNAh24MkaowGPEk/pxNySeYXSzLmyIrW23j6VjpFm5tFwYrRPs8ZJM3PU6+wT'
        b'UFCaqURYA3VSY59gjZNmZqt1q6xTjuYIB8fOGo5ZhWFYVmxqQBWgqEJ4Eit5V+FZo6cfReZlZxXjNI1GX4OwIPIqF+XllMlmN6K1sUw+2QtaXR2CNVyPZdpz1aYmowy3'
        b'g5BcpdzSpsU/Zt4dxeO5HzOIxAmDSJw4iERHg0ikB5E4OohE+0EkOhhE4mSDSLTrbOIkg0icfBBJEwaRNHEQSY4GkUQPIml0EEn2g0hyMIikyQaRZNfZpEkGkTT5IBQT'
        b'BqGYOAiFo0Eo6EEoRgehsB+EwsEgFJMNQmHXWcUkg1BMPojkCYNInjiIZEeDSKYHkTw6iGT7QSQ7GETyZINItuts8iSDSB4ziNGNiPaTXqupUdP4cZ7eBLtqGvUNCDEX'
        b'mDCq05ExIGysQfK0NdCkRwgZYT+doUmvqaprQvhah+IRLjbqNUacA6VXatT6SjRRKDhHizkUjYwmd1kmAyYo6xE/lLkInqzTo3kzGEgDGOvRNLZe26A1SqIspFeauQRN'
        b'N85XiRJ1tThfDjxZX6+tRTTKKNHqJGVqRBftCijJGuCUUnIYZV/ZKBmXLUG9QAgjChcfk2Apj5LCJxZInLxAosMCSZJsvcmIkieWI+mKyStUOKwwefICyaRAkZqmy2TO'
        b'EV+C+BMSZ9SsM9o8CBPZvEn2WQ22bPRCZGsQOa61iwjPXKLVodXA60/awUnrURQmvQhLjwkmjg0i9KM2GBG102trjBhqatR1qP8ok65ajTqjq0Rga1txox6erEVAlKer'
        b'1q6RS3Jo+mEfShwTShoTUowJJY8JpYwJpY4JpY0JpY9tPX5scGxvEsZ2J2FsfxLGdigh2QGbIolaYJlVg4XRkI4yRo4SLbySoyQr+zRZmg2VOUgvcdwa5rscxY9hxSYf'
        b'w1PSJ+POfkjmxMlbHsOn/SPZEKp0lG0MCUiZQAJSJpKAFEckIIUmASmj2DjFngSkOCABKZORgBQ7VJ8yCQlImZyOpU4YROrEQaQ6GkQqPYjU0UGk2g8i1cEgUicbRKpd'
        b'Z1MnGUTq5INImzCItImDSHM0iDR6EGmjg0izH0Sag0GkTTaINLvOpk0yiLTJB5E+YRDpEweR7mgQ6fQg0kcHkW4/iHQHg0ifbBDpdp1Nn2QQ6ZMPAiHICbJCvANhId6h'
        b'tBBvERfi7diU+DECQ7wjiSF+UpEh3l42iJ9MaIgfMx5LF3P0moZqQzPCMg0Ibxsa69cgTiJTObc0S0aoldGg19QgIqjDNM9hdKLj6CTH0QrH0cmOo1McR6c6jk5zHJ0+'
        b'yXDiMUJfpYO3mmqMGoOkpLREaWHgMDE3NGmQPEwzk6PE3C7WSr7touZpKuEtTOnHsQ21dLyFa7CGEseEkjJLLcoVu8IT1C4JE6MSJ0YhMaceC8VqI+ZLJUoTqk7doEFk'
        b'VG00GTBbS49G0qDWmRB5kdRqaDBF5NCRGkBqV0SLibu2mhT73swO6ndAlBzXPTEjUTGNzo4EMd8SC8tLprIGp1smmfYn2vmxTDiqqRphZBLdafEZnr4Ya8dKsFOKnfmU'
        b'5ZRNvwA7WAs4wjE01WuNtOaxDCvGGLTqEOvWLGrDhVYH69QMmVa1oRSrDX1bch9yKe+4Ya+oR05ssXtL7lc8ytv/ITt+ymzGk0oG5SHaqWmb3bry61pGkrdfaw6tNyRH'
        b'kjfBVr0BX7DbGQvOwJv+bMo5hbk5yfd/SXPIy6qqajTpjEhIeXALT417NgIvWsJRN2nqH3jRekM8ud/5zUEA14C4GKwcl9AyFtouWoTkUBZ883WEjbktfTnyfnMLRaga'
        b'aOapsU6nkSgb6+vjchH208kK1mNdzmhwFJ9mLipYIqGLYZ0dxtQGrcFER+A0+zC9v+dhFSMtS9ANZatkyqq6engLwVk94n/sg5nZmnpNbTUeCO21KHhG/YkWWSzTOhNE'
        b'tsDMp8aCRqwCooRmwCxi5qhCzCJgErEAi5YoM9rIRiKCWGogzdVrUQbi0+pqGiUySZbeaO2KJSZPh0uOi8TZEh1lS5yQLclRtqQJ2RSOsikmZEt2lC15QrYUR9lSJmRL'
        b'dZQtdUK2NEfZED9ToixLQBEF9MJgvlpDIhMnRKKApEiDcLNV6ysxySWjWl8UScOyVQ0rl2DZwCrh0+rd0WWUFMYUZuaYdKvIowyNvhYhw/UYgeH4bJVEkU6T9BprFqx+'
        b'dhRvgRs6yUGFmUuI6IEHrm9Q40QbiDhKsYHKZMUSn1bMcSINQk8p5jiRBqmnFHOcSIPYU4o5TqRB7inFHCfSIPiUYo4TaZB8SjHHibhY+tOKOU4kyx3/1PV2nEoKPh1Q'
        b'JoeUhKeCyiSppOBTgWWSVFLwqeAySSop+FSAmSSVFHwqyEySSgo+FWgmSSUFnwo2k6SSgk8FnElSyY5/KuSgVKUR3qpahUjXWkR8jYQJXqvRGjSZOYjEj2I/hA7Vuno1'
        b'1mMaVqrr9KjWWg3KodNgBmxUsWmhnBjhZZlqsArOhuSstBQlYcw7SpAlUVm69TTzjc8OETIu0hoRadRUIw5EbRyXPA4PTyw8isnHp+nr4TWDhU0Yk5JLTpJqjIgrsYlw'
        b'hJLICL/jUN6wjNRCzRHpR5QGs+s1hFFvwATeqNGiaTHadNJ5iKs2amu0q9T22H8JETltump7NoMWVO3OLO3ZpBwNLcVotJU4qRCtGj6EM9CczeSMmr0eGvUbtayuNzWs'
        b'0tRZleaECBIuDt/VprlqfaVjJlljdTDraEizMsmhdkxy6rCXZCyTLJ4y7UniKIuc6j/KIQdhDvkquBhnKCyGe+MImwx3F8D9i50or0q261TGGDbZzcom/wL1aYZoIpuM'
        b'GGPuVAq5fPynZCFXiP9o1jndKYgKopRTVRyVm0povYG/kmG9XKPnkEeeLn6UkqfkpzP1TiTsisJuJOxMwu4o7EHCLiQsQOEpJMwjYU8UFpIwn4RFKOxFwq4k7I3CPiTs'
        b'hnuiYCrF5CWA+5jeC7/nz0Xpm84j4wlVMS0jYiv9xo3IY+yMoD8e+mMomJZanGy+sXX7p7ugmsNU9LVA/A5QgOp3UgaMq1+gDEd5OCpn8lrQk+QJtLyImILip6DRBZHR'
        b'edp6IlQGpzMs7w3dVR4KjlKCc9jqFCpD9KJaJ5caacSI8xz8NGe2cuGDX6Kk9T48a1hC4zf6eSzvDEePJSc9vrTzAF+X0WuxD1/FJbKJ1PUBhuIH+GbPA3z1czS7Xm/N'
        b'rjdgZxXOgh8BPsAv8B644tJOIzx19RqEJvUV2uoRlyqErHRG7HVX09JURT3iNo11I85VJrSPdVXNI874Yr5WXU/feRnhkwsyFQ0Ih9QVVznbwTRuitzY2kJZL2Pav9Ml'
        b'r/4YaIXZKic0X/SbP66CZ7lO5lzGs7tOhtZM5Wx3ncxlzMUx5ywXcp1sQqz9bWHTCTRHvDy689r1GgN5v2ybdS252lGFny5nIKlH3SAZnZgMy8tkhNmwwsvy9NkyQ2qd'
        b'kYcvX0VlIwRktKI/qVyShfMjVFUlIXdiJaYmCULYqZJqba3WaJBbm7HNueNW6GS6Bdsxzfe0kTy+jbGLmSEpJL+4iXlxhdZUS8MGui1MnjBhQGRFLimrQ6QCwaVGYjBV'
        b'1muqa1H/HJai77TQMiwqKVGjIihM90dS34jIlF4uyTNKGkxIkqnUkFJqS+crNca1GnzMLImq1tSoTfVGKXkonjY6VxYgzJDMtvgkVVgvGWU7zbTTZ0qtpawAmyGxrL7B'
        b'Nrn43XmjXhJF34VZBW/p1yM521rQcrsrgwhRmOFAxeg1suzRKE2tXJKcEB8rSU2ItxWz2xEZkhwckJAALl6j1SEoQ32QNGvUqOFonWYtPipdkyJXyBOipXLe99wldqXf'
        b'JDlFCRCMU2nx3J+bFq+JpUzTUCR3zrOwtQicL4UteXBPQRzcWYovGOcWSmFrbLEM7IL7Cufnggu5xUVFeUUMeFJCwXbQ7doIz9eTWqsKXSkxRUXFr9E15ocLKNMMFFkO'
        b'T6P/HNUL98KdhYi0gZ3jKj6STcHnm10psDOZ1PsztQuFKG58fM483W+zN1DkGSs8CY6Rm822d6y5cll0Pm4gGrzKplKWcQ1gVwx5iUtqUa3iUghrCeJr7s3rNZXSY64G'
        b'1+C1cb1jziL9gy2o2tZY3Mfd0oWj3aPADT0fvLa5UHv57wc4hlcwrtoRcvmX+DWKL3gZUqyQ3bOCQl9699RbAsB4a/ep0gRx4Ad1ydvnOG8Nace3qL1OZXS4RBx9XwzY'
        b'ih2+MCDC1dBxqQNuq3Y3CCJZ3PjtnT9+mTXEufbc9BZ+68qO5ecX/lq85lLIvbdX/riX4VWirlxRusK5xuMXb6/KzDzyx43r6n979xfK4rDPsn6z+u5Pqhhf3Z+RSv1o'
        b'dc/DfvUtI/dDV+p8YfDPd8ilruSmdTbsB/tBq/U9/IIU/N7LI5xVA4+DLeTRC7xZR14KWNYd3oCvk7VnUH7wOfZ6CbzzGPMn8MhiuJ+P5h70MaVF1iesXmAH21kHj5Nr'
        b'2eB10N6AakINnZtlt9gMyjuEzQfnasm91mR4FbTGyKJyXWbImBQXHGHKwO0o0lnQk4y7sjG9xLK2eGU9wass2FpD3+mWIjbpVoxcCneB21QsfrFznpnkZulixGI1aIVd'
        b'UvyA1raUXMpzDQvcrvd8jClQSDDYjsdKs1lJ4CzpoQUSEMzB7Vz5IsVjYk2gD+6H50Crv7IEVRYtxxkRBO6LwRklBo6bWEo/Hj47BV5D7V4ILaH1m6hdGWoVHGbB7dPA'
        b'Tbqyw7XwymjDMUtQ7ZjFc6L8QD8btJrADinvn3grisnm+HeieFFHplhp1djHcWaKvs67xokKwQ/i3IZDZW3sjwWSe0LvdkNHxoFnB4WRvSGDwpjP/cIGwnMH/fIGRHnD'
        b'U2NQXg86T/qBzYPCiN4p5NUHyjNv0C93QJQ7HCI9HdQTNBiSgLK6o6xtRvwWCWe1VZc66Jc2IEobnhp9Wt5bORSSag5JHQxJn1DAVnfOoN+8AdG8+5HJuJNhw2Fx+Ddk'
        b'OCQUlxkODW9jfzLmdYkbfYd4PXY2YGcjdrAuW78ZO+Tm7bPU064ZY+56heWf3W1jclN3L+aFcCaMTP6OJvJJiRODUcX4M4XdH/oAt4ebQF3iT2ONuTvPsCLxAILEVdQC'
        b'auK/MMrleSmjWMoY4VeMch5IUsGjJ5KKxPJWclq9uqGyWj3DDiCsUVMYVgCiOsqGAmUfBdIXfb+zkC1LxVYWIwqRv2pZo66+WXqGMcKqbqz6p/pdS/ebV2FjZSZ2W9+O'
        b'nf3IEaFI8pQM97Gr4kgF3cNguod0FQ46+K/0zKNiLAP0tO75jJ3ChI8CE+gOSp/KNP3LXa2hu+pSYeVxntZJvzFzWH6knO6ib7baoLExSf+u2XOpsDJQT+tSIIrUd+EQ'
        b'6UropKzWv9ipOrpTzhUW5uxpfZLgtbRN0/Ijyy19m5Sd+/dMmGuFHQf4tP6F4mUchTX5R4FyC6x9D9c4ST9tb2SwkmMG0/JIZ/SB8L/3ic4/8ECYVaw9NNzDMOCnbLev'
        b'ZNEPfrvfoh9UFvqGKMo4Qp3X67POg7Q38LPJD8+yZ3HFUiahwuCUbw5mPa6BFyZSYbArjrA604u08EXE3ozS4TFEGJzaPOlTXacKjA4qKkYEdoSVxBC6il9f4dde+S6U'
        b'2L9D0TWjc8agT/QZZZ9oKCHLnJA1KMs2+2QPCLInvMl1RIjoJ7mY+NAwcBE7fciJYIy+dPlznssPe+lCcMB+7lTqOF/GkvJGnCxYiX6nwjUY9RqNccS5qdFgxHLSCLtK'
        b'a2wecaLzNI9w16iJsM+vQtJYYwOtBGAZ1bUjnEa0Z/VVfLvVdbeuLqaYM9iOzW4hgHOzvLd0Vnkg4Z6HAVAlQKK+i8pJ4W4BRH6Zux0guiJA5NsBousYkONnuRJAnBBr'
        b'/1bMNB3BHC+rutqApEksUlVrKjG2Qf9XWa5pSjTkZQkxTYakWSKaqiV1plqNncSNZsqgRRKuhH4zhIVpg8Yol5SgvcbDaKwBn8BpG5oa9Vjwt2arUuuQ9IqzIklXr6ky'
        b'1jdLKpsx3uOp16i19WpcJREO8SVdA5Lbq1GfEApCO9pShUUgxnXwUFGTQaurJYjTVkwSTRYlGo0gx9K7Oqwnmtg2L8qo1teiMtVW/IbzS7A214CFTcNqEx59pV5dtUpj'
        b'NEgzeOMUBRmSrDHkTbKUnE8vt2bDNWVIyMOVpd/7fMVWigbHDImS/EqWWi5P2tKtYJohwbpjNDVEtl9qf1nSlhcDcoZkNnIlS0v0xtF4GrRREu0hdcRK8pQlsqSElBTJ'
        b'UqwPtuWm4R/J91llsrw5kqWWQ9XlMUvtH9OMVj66TbAGgg5IcEH7K9u27GgjocHWIVBB4Gio0mubjBaqg9cVv00jsJVVb2hE662pJsoQtDw4FWP8emL8jky2XDKH1ogQ'
        b'kJyqNKobGvC7VN1Um26EAAdaONRAkwW0qrXE3J4aTcNaLaIkmnVoxi0AJyetFTcaNTQYEeDWGOsaq9HOqDU1oIVEbalXIQBEQKVBo6vSSBoR0SXl6C5ioCKqGwPdba3B'
        b'rkm5JAdtOuuGIqXswRArdhCoYOOAVfVoALRdQIOGzrnCYgqwsYr0hD7umVZnNDYZMuLi1q5dS1s2kldr4qp19Zp1jQ1xNOcYp25qitOixVgnrzM21IfGWauIS4iPT0pM'
        b'TIibk5AWn6BQxCvSkhQJ8cmpSekzVlR8r9rFs5hW6b+UOsVQKM2XyYtjwX5JHpaHzyChNUzJqUvIMmFML3GHF5PQrydoSaASmoOI6qJpJptyDohjUbNW1G8t1FEmbAKi'
        b'Ch7QF1jJ1nzYEgP3FOXLFuCX3Qui8EvoRbAF/yBqBvbnLAYXXeCh2aEm/Ag1JxnugJeRVI5lVyeKM38G7GS6glfgNhOmW+Vwy0Z4WY5k4DysYcE2sPYUIdE8GLzCBser'
        b'Eb18Bewkyp2G2Uvh5QKwC26Hu4tUsK3JMjjLyEphSzEqvLtA1YScksJ8eIhNIUl9Gx+ehMcWElOCEbAtjC+X5oNboItHueQzwS5wCnYh9w3S1zjYBo7Dy3moAgbFAocZ'
        b'YJsr2AKPwG5iC1AJL4KzfNgSJ4c7Uaux4Ew+kvVbGJRkHmd1LBvuW2XCSwHuRIHr8HJcNINi5jLiZqXUasnM9tc4Ua6zrqPsK2K/cfGnSJOBiGW4Y3BzB6/CQ/Aq3bLz'
        b'Mua8qZvI9KBpPSUwuMFDbm5y2A6vFsJLMXA/i/JpZiGRvgOcB+dApwnzIGiG2+BevjwPviBDvdpTlIdnhkV5wRtsD9ieqB1kK5iGN1HO0PxrDW1FntviXbcPvsj89el1'
        b'7Hf26MSL6l8yzx54Tf927y/3Ktexb1/ct6W/95j269sn8468/Mejtz7fnzrjT1HLLrz0x9zp6T1ZiwKKi1c6/Vr4K+/hs14F71TOL3nhm5dWNgVVzHku/PXffRLc/Mlb'
        b'd/5w8yFvuuJJS1aCkpffkV/6/smsF6QsTeGUqNqzf77kXrBDnSSd92rLqWfeT/89b9552aoNnj//r9Rbb0Qs2sM88NaXYcdcNt1OOz/z018/+4v/2Jg8/b1pM2OvBLWc'
        b'j5Zy6Xf8JxbDnlHtEtEtwTdKwlk1oeDqY8zewO7cIhvYjtG1xCRxUnPhvmXwFlHegC7wGjyMFUypvuP0S9Hw5uNgnGUrQ4R5vHH8HTibBLdr4R3yrr853yOmWAYv8fLy'
        b'igpi4R4pg/KGt9iJ+bCbKJCawcnEgtioXNQLtMrgHLMW3m4Oh+ekgn/FuppD3QzZ3/ZmvGwvrnnq6uoKmsMYEdr4ydFIwlL+zsJSFvIoP0k3p9t4elPPpkHf5DbusNC3'
        b'I84sjDYLE4flCW05HTPNohhaOZN6YOOgMKzbOBSZYY7M6J9vjpwxKJxBdCmz79aaw4sG/YoHRMXDU6Vt3La17R7DUgXybDYLIoZnZLdxB3wyzILM4bBoFNlsxoqWKORb'
        b'0+4+LE2w5pOEIZ+p3e0Loe9wlLxX38foxTbb0s2i8GFZUl9WX3bvEhSeYRZFD3v7DnlLO5a1sYYFosPu7e5DAqlZIO0N7dUPChKHBOlmQXp/xCeCLDuueArNFb9GWa8v'
        b'XsbOFexcxc417FzHTj92bmDn9Un4aLvFwPO+YvSfZNSIgx5i5y3cNuausU2Ev2MDIyUuWKfzhGh2vvrB+h18K7CXm0b187NYLKnLiGs1vuJp4ZhG3Gg+0xrkqhvIL5sY'
        b'k3CxHLZXaUb4mMtBvB2+ikcP2jbeKp4dCRJYSVAbZredHLHbh4iVTMRa4zM0BrFm6qKaglhvbO2UWLVVCCwMN28Mw81HDLfd6Zo9841Ya14WnzDcE2LHnKY1csYy3Grb'
        b'7UsJbUEPsalz8fMXOiRBvAHaDYgjRfyL2t7SL+ZxYiW1+kZTE0pFrK+aV9XYUKnVqa3cUjRipKIJ20BzDVibYLvfixu0icc8LB7/fw7/aRy+PdBm4IM9OsamzxrH6Y+B'
        b'ajo/HWUtQNi1pd9zcdVWHb0r6HosG8ESR3Ooukas9dATnlRHc5prGzGLqG1Q11t41qVPuYqLOHfHl3FtPcD7kW6/srFxFW4fx8glRZbVUZOwpLFyJZpoJD/SJ5Q6LEGk'
        b'pcQnWFRFeOKROIOLLx29hmtrxLbdMyQqg0ldX08gBS3MmkZtlQ0al9rd2h0jBFnQw9hpIk8Fl9rf5J0gxuDs40SZMfdD/wckk2zNWk2t5fbO/5dO/gnpJCklPjEtLT4p'
        b'SZGUnJSSkpxApBPc6lgRhTtBRJHQJ8OD5RzE637mhESNWIFCQZkwEgf7QB/cVZBXBHfF5tlEjvGSxu6ZRNh4Ftx2UZSBcyZivOxScpi9pGGKwZLGM0YTtm4SBK6C6wXy'
        b'/CLEveUVVjwzWcVEhGmFrS7gNNwC75iyiSgFboAthpKiEot5K9zAIsRut8B9sAUJHDzEn6MKUfiGchnKfQSccKFUm8E5+CK/GF6Al0zkhLIPFXnNkA/35BWVFGDLWPFs'
        b'KgG8Ls5mwd2gF+4ncltRDNhviC6Ce6MwryrPAxeiGFQmL7iWw6kAN2nR7oJmFR9eB3sXOMM9suIUuBeJIkzKM4kFespqTFI8F+3wMHwBzYbtxBp17wi2NwWuLsC2lxNA'
        b'K2cduDjLhDnp6T5iS7fyYkFHgxRbchbBEyx4MwQcJ0uVg815V+9CvOGK+puaGIrIjxuynPloccHzwWVUGTjGJqIiPAG2gef5eJbgztVoKtvh9Vwkje2BB+BVLKG1gnMo'
        b'VAj35mLxZJmv87wscIVYgM4GV1GvMcuVEJdH5QXBaybMI4EzHLgNy6m18AKSU13mEilrOngR7CFWqp1gbxwVVwK66r/9+9//nuOCgGqjFwPLr3ENYfR5fEU1Er2m/ZSJ'
        b'RK/ClugEyjQbRWrhKwV4cvZYhNrc2IXYFn1cvgrBQy7crYTd4GqUFEFGLoJG2va8FFwj08fVuS0HWznkeQka0WXQCbY3K+GhpHwWxYDnKXi+DPSZpuPUq0um8PEyoTVa'
        b'gOTLNnDQCjfO9CSNmSEkB+5nU2CHyuUZHWihjbFdhHtNWAak5cP5Uch3DFxXOo8VCWd6cd3h62sJqMFDtfCARmHIl5UUxWE4KrZIg1LYwQFXlm6ijd+3wN21MbRFHSmX'
        b'4iPZtw3cYcLLm9FcYh7Sp7iY+RZ3RaVTk1r4mfjsgjr6moUQdK5B4zgFL1v0APQVCwRmcGdcSdH8KEuV9hcZUI9Pu8I2JFgRm+HuCati5HmxSETmIsg/D/Yx4+DxKhNm'
        b'o3PBoQ0FRELSgxNMPSMNdsFOKYtYAIpHM91iK/hCLC4HjiSRKhPhRbifLjgTXLUUPEaEbHd4ytl+nFvQDsXjXLlRKz7OZxl2IN5b89ulrywoKgGzBMf++MQ76hXRlJme'
        b'2bkPJevb+TkXg4pevxlZHOZX/Oeh+3cevZue+ceFP/70QFjfZ09qfjP9i8fpf2U/iJvl/qte6r8urz57mX3v3bOudx698MmyTZWnq9byrr3z8z9OWdFF/eEv3LXVt9w3'
        b'v/7zzt1ezmtfifTd87suv5d3FyumfvwwL/TtpbOuh3wBVMnT+06H+k/5bPa8ZTURrUeP/Pxdj3nvhR9Jyghepodv/Fo276W/LVI2/2LviYWFS3p+15D00p5bvwvNGPjd'
        b'uThPw+n0ngeydfOiZ8MXC0/umr7y4nXV67u8bu/d+7Gxpf3a59M0gff2eq26+XM318jnOC3LXrjTbDj+d5f//OnRv2z86/Pf+n55K7e+9pXn1q38Zf+lD3Kk6S+dDdiY'
        b'VPn7oJmXakL776S3aK/v1wd9/pFKXvxhw4uJG0N+5r7wRsbLH514fvrqL95vuvZXUF64KTX5m18cv7qhZNl372zqPjDg/MdNeU9iKveZKp8XZL55ff/Pn+t/w1BQ0vxs'
        b'8+DVd1QJ/9Fbd+vDL6m/PHQ7c7P02cj/lLoR02Wz4BU2Ee2XJI0K90iynxlKblKU+MNL4AK4Oqlwj/bV63FESxAdvAHL9USqB6dAz6hkjzY3kcqdQxoK5LLo4CXWSx8e'
        b'C1n18EwpbVj9IOxtionGlz5iUehVcN7lGSZ4ZbbFGDE8FAJOxsgx6YhFIAmfjwR7mbJQuI3YYw0CtzcWFEZzKXAUdjGXM1L18CJtpfgaBV6BW8Eb4FxhUSxCrQUM8JoM'
        b'bKUtaB6EB5oRnbFe9+CCV+dvZEZGPkOOkYzyWVgNMeFSCOjKx/dCQFskUX2A46AdDXfCYRMawVn6wImdSFQfy4VcA96mshngOUwHyVRPgW0s0AdeCqHn4LgH7LXpLUAX'
        b'uIZ1F83g4hSp179bcTG5RgPjBonFdpwDtYY71mCMinYjPmNUG6MJRL2RxaTVG5v5lF9Y99xeBTbVPOib3salNRnTBn2iBoXS3jlDsTPNsTPvhphjZw8KZxNVRtbdQnN4'
        b'6aDf/AHR/OGpclqVQRebPugjHRRG95YNyWaZZbPuJphlcwaFc0ix7LvLzeELBv2UAyLl8LQ8rO5IMwvSh6OwbmOTWRBupw2JjMHqFhTaaBaE3RMGdlR3zx4SRpmFUff8'
        b'o3pFg/7ytjlf+PjT11puhPZX35Sawy2G41FhS0Gsqck6kDGcmtGWM+Cf9JFIcd/iNYsU9wIl3d5Hlw4FxpkD4/pYg4GKNt6w0LsjelAYdkbYu2RINt0sm95fNSjLvpto'
        b'luUMSue9FzIoLSBtFr633hz+zKDfkgHRks/TMm/Mu5vz3sI3SwanlQ2mqfDIFGZBMlbRJGfi9hLMosT7IeGnfXt829yHhT6HM9ozutlDkgSzJGFQmDAcntSnNoenthUP'
        b'+/gN+cgHguR97Osul1z6Zwx457excLfChvyizX6oc9HDQVOHguTmIHmvwRyU1Dbvno9fR2p3utlfNugj7wsf9En9PChyIKpwMKhoQFx038e/o7a7FmVHqcMxcR1O3U4f'
        b'iaOGfQO7nXo5Pe6DvvJhqQzFcjrdv70fFdtXdrfSHJTXNm84NqltzpAozCwK61aaRdJhgU+Hi1kw1aJEivhEkGCnNxLSeqO3sfMOdt7FznvY+RF23qeseqN/UGU0Hvhx'
        b'U+MVSDYd0gh2PkPOEpsOCdvTXM1jMLREh6RlPCbuD9UhneGmUzf4WWxWlfVxLP5n+yoKvt5kr+85RKmcVC4qNvkuClNFW9l3UzFsX0fhlNndjNZxgyiVnZ1lFXeMFoeT'
        b'xSW6nQmxk5/qTxQ03GlB4z1nJjnyj082xZ6QNVNlJPZuHOIUUa3ds7WFP9LGUoT7iFB4GsBe0Ar2OK9mUSx3RhrozyMf+FGkLVCCPWVwj6poPrzqC3aXwqsqt5T4eIoK'
        b'9GGBreBEETlkcAEtiUpwbSPcU5YcD3cpEJPvvJoBu2eAXsIuBsM9oMtSEwMxlQyKE80ARwxTCFsLu3RMcNkIdpLvoExDDGEn6Rc8BW6BE/BERRp8BSGvCEoMX8mnXzdf'
        b'AbcWF8jjFYmwB95IZlLczQzwMji1hqT6wL44/N0QyzdD0v3JV0NAV7WW8ddv2YYkBDGzxMI9ZQXFMF4QmLnzaPBWb3bvlhYeP0WVuic65M0jbse/Gna6z5zBWXT/jcL8'
        b'BT0fnFTs1/z6dmdq47QXK1obm86o7r5x6jNWfyXj1TmHBrqOKr7zefb33/7UP7vkwm94WVOC+P05gcf33XBKb21K52f/6uq581/+4evdL7VlXYxf8psL7/Piv4jeVdys'
        b'+HL5zJSZ773odC+/+mtOqZPyQ/VHxt9+/qel25+bu7n2uGf7Sk3cO2d7HuXPOHS1/MidT6J+v2DBI3PryE+/5nW/sPDwqUhTwpfLd/+q9t3f3Hzw4Wff3PnCeG5Pe8vZ'
        b'EwP63776muHMp01+H410CC5KwmZcWrsMHht4/Ev1juT3zB0jG7JO3KlI/m3/azE//XLP6y41b5l90xOn/emv3t11JVEHpn371+VXPbb9KaD1b4Hrnv/DfzgNfznn8mez'
        b'pJ7kNinoAUfk5NNCThQTHGdIVapwuO8xXi91QDE4txLsHyXv8HgWbfx3Rwg4Zk/eN4I9SHyLZIBj5LYmotx7wFGHNB4R+GdWu1UGkA8prALbw0Fr/eYx5x+IRUJU/zjJ'
        b'AK8ECQuE8HJxLBJf9sWBs2zKHbzBqgC34VbChbDhS8X4quqLBeSbMewgBmp7K9xCuhkFToA37L/T4BpQj7/ScAK2Ei5l/uLqmGpwZ9w3ZxpDS+kDlddF8GRBCHzZ/kI3'
        b'g/IGF9j+TB19oHIWvsEuGHMxm0H5NnuuZIHz4GD4Y3z8BfZXwY6CxVGTs3ngSjxh8xLhNngbtvrMGXP71iOIVQ666XmHL4D+5gJ4uMruei/h9HojaVZuKzydQ3M5MeCK'
        b'5YCmGd5YSqzeLoS9a2Crbp39F3Iuqapo/uiKeo7FzC7omm+1mo5m5Qpd8XXwegYWTODeEk0RNvgM2piN4eCq1PO/kV3ytLJLEz/mMuJUQX9lx/4+ER1DuKMumjt6uNiN'
        b'8gk+XN9ef0DXxsJsSG23unNlb/SQMNksTB72l3RldGa0zRkOCOkq6CxomzvsF9Q++75/UFdaZxqODu7K68wj0W2zh4XiDsWQf6zZP3ZQGDvsH9wdgjM9ZEr8PIdFfg9Z'
        b'6Pe+SHy4qL3oIQf5H3Ipr4COrPb8IVGkWRT50AnHOVviDpe0lzx0wTE8W64IsyjiIR/FPXKlvMQdrC7XTteB8JRBceqgKO2hG87sTnn5PvTAPgH2TcE+T+wTYp8I+7yw'
        b'zxv5SBM+OCTGoeL24oe+uHI/XDmvuxqzhtPNsdMHwmeYxTMGRTMf+uPMASizpceBOByEsg+J0jtnd3PIV3/WDUrSBgPSHwbjRAlJTEWJrNOuPa69iwclKYMBqQ9DcOJU'
        b'lPgwFPvCcAfwvITjUASKP5zXkfUwEoeirCEpDkVbQzE4FEuql3bM6SrqLHoow1FyPMY47IvHvgTsS8S+JOxTYF8y9qVgXyr2pWFfOvZlYF8m9k3DvunYNwP5Hs1Evjbu'
        b'w2y0e/3bOPcFXodd2107l/emDAYmfixIskR0KLsWdy7uru1V96wcikg1R6QOBqZ9LEj/ZVB4W86wyPdwYXthj7B74Qn/T0WyRywqOOK+T+DhDe0bupMRVz3kE2/2ie8T'
        b'96cP+swdEMy1473cad7rBgFs+gjHMMIxGNV64wgLAfUPY7TcrYzWOB7rIXYeIecCw2Ky/K/YZLkbgxGLOazYH3oVrosbR13kZ7D+d29FfneIRz9HNVofmVmOaOotmmW9'
        b'xmjS60hag0SNT9DsFNPk9EqyStNsQPma9BoDvg9Na7QtKneD7RjMot7Gp1DjT8TqaT0+rr6y2Ug+oWnP1Tk74OpM+GuhgjAxaIUvgn1gJ7gE94PXFoHXwCVwbj5oAS84'
        b'cygx2MLaAC7OpC9ldCKy9xw8gBhZOVUDO+XJgeTahMkPvmjAzB5oXTTTS4ZooVzOokRgJwucAUfAFsIpaj1ZZbsY5AuWsfdnqembG/Ak2O1mKepEscErxXMY4DC4CG+M'
        b'MCqItooB98MzNm3VPhaPGYck/tukNNgPbuUQLnBHAmYpLVwg7K0hyqwUsAXegYfKaX0WVmaBk6CFJG2ugYeVqAh8zhWVYoI9jADwYin5RF8I6H8WHiiQh8WhMbCyGBvA'
        b'LY32TzfvUgZ8or3zohJfa11xt+1dAQh6a4vLto6Etwt7sKF5Bmu2VMiavbXUeakg5tT7K95Zcao0R9nr2/zBmx/0fPB6vcR7IGVN4TdTsk8Vlnpfzmh7nFy54n5NKXVj'
        b'z3PV18OzfvYbv/c9P2DqlwVVxcck/J8r6l9VOdcseo6vcatxkrr94p3jL8ODU3q8e/cLT+fLqw+9+fk79SvuXFafLat01ijUCurIb0DdO87fPMt76+89rtGuL/lSP73q'
        b'Lz0aJ+XST3vO4480kcsXEfDo+Pu18LaRMGMbwK4Ii8l6bK9e1sgMTYI7iB4G9hm9G8GlGHkRE01YL6MA9j1DSHNuHnwNtMYtht2YI8iTMSm+hgm7o5wIJ8ZHy3nZqkJx'
        b'C5hwY7cVnCKMlg60zBz/8b0S8EojkiP6pM7/MMV2tlFsG51WGyrwfrOj05YYQqc/pmg6vcCDYF5EMsOlp4t7iofC0sxhaZ+GZbQXIsIbHNK1pnPNQERKP6tfORic1ZY7'
        b'HBzbu84cnIp8EdGn63vq+5IGI2a1zT1Q8siJCs986IrqGQpTmMMUQ2EZ5rCMT8OmkZr8AjvUnRGIxIv9urid3IHguD5hX9Wn4oxhcXC3k1kcNSROMIsT+qI+EWfiKCRT'
        b'D4njzOK4Pu6n4tSHTmyJd1suItmRMafrj6NGzRHZ/ZHIIS17UOHTETUWB7a5/lPXlPHVdz0DOb+yv6Y81+MHGuS/hAqeYYywm9TGujEfbLEJl/UYN3MsH2zB76fxt0Dx'
        b'x624to+2cP+NH22pRVj6sh2WxgjVoF6DffX19vh69Dkw7nuGJK9GEo190RJEBA30wSXGxJp12NgBPgeMlq/XNkXHkoosKF9PHxsasLHYatthpFpfVaddo5FLSvDZ6Fqt'
        b'QWND86QM6RDJrpbUNNYjPnIcDp/43VLnYnJOBdrha8/E5KINXZqLOPb8okJwpiwXXIAtsXLESBvccuELTk2gg22SYTycV1OAdn9+kRzuRPJMGWzBX3VFDLssCpxhU2Ab'
        b'eLUAXnMCL8LTYDt9JrgHbi2HBxqawTmiwGXVM8A2eGMxLWu3gX63GNS3dQWwh1oHdoE9JD4F9C2NKWFSCH+2LqDgEXAgSvvrFbdYhm9Q4jWv7cfmF60Cs0Qv/WzjsELU'
        b'3n3tYOVxH49yw3mn+Q9/oUldypvuNbKOX/4X6d9+PqPIm/XTC7/4P+rgxheav6757ZeMt59jznz/l7envj93edHRD9e6buR4D4Ff3AE9IzfykqFZZdzBuqd/2Fv5altq'
        b'49wlv//RnnPyd6+8e+rie8q0CNkffbK+qF7owvrEsCpysceW2+w1wtAy0Nl1YNmnql0/SRIMFnzwxtKkTd+8/ek3B2Z/8cv0vz0u7rzzl3fDPYb+vGT49q4Ph3/9228+'
        b'cg394zsZfYfm/Nq/4vbqNx59+PLjB9e+WvJpc0O7es0X+759pTBh6vNpwXdvpmZLj3/l0c6MXNbrLPUgAmMjeBXsjtkITuEFQ+xKKgO8isSmHlqu3btiPpb1LF9RdgaX'
        b'2bCVuQncsHzCNAPuCISX4ZW1ltt1sHeOCzjNBCdSYggunga3gS5UQQiSWNEiMyluMTMALdtRUrpJ/Sz+XnSsPI+k5cItfNjHhLdi4S0ig6WJmAWxYG8J/W0isCOcP4sJ'
        b'O/AhLv2tk+1LNbg8NSWuBD/83MyMBgfhWVpObtEAcnAklRfjozkyNo94Vu10eI1QllWLycdQYEuUlbgwQ331pFtCdW5MHD6pBvvkMrmUiXB/FwtsB9dhJ6E8EcWVWOxb'
        b'i+C1mENxpzF9ZCm0kv9iHrhTYAN0lzmgTcQEPcVJ9He4roLzLkRHcGWDZTKymWL5apK4fhV4BX+qNXSMLNpYQ+qdAS/AazFxU+BJ3CsOPl5jxsLnwQUp/5+VJPnUGMU7'
        b'TZrYeMuPuNnoEg4SouRBf6j1Yb6AEnkfTm1PPTyjfUZ32JAw0iyM/NwvZGCq9SGm0IskT2+f3i0aEkaYhRG9iRczzmT0VQ/FZJpjMsdkFgdgge6oexvHokA+MI3WiPd6'
        b'DwnjzcL4e34h3WG9rN5lg34ZiFZFxOAvxZxq6OR1sIfF/rhwd9mn4ngkWUQq7ot8Due15x0quO8f2JXamYpfzPSGDfnHmf3jhhFxc+507ha95D6mknuBId1TT0f2RJ6O'
        b'7YntNfaVDU7N6J/zcWDW3QXDAUFduZ253WUvFT9hUUHZDHNg1le4nZ8HZn0amPWdARuweFvgOTeO83Ycb+4MF5q2udC0jcX4h5TBRCFrE0tomueNi+JngH+3CiVY77sB'
        b'0TzxVz/wO0pEKDnMjaRO8xNZqGtHKfJNttFzEz2+3ac/jJ2XcZoLfV1UqzHoe3Hkcey8QtNsbNhjhDVXtaCYfMtEjz/nijC+5Z+UQ/8w0Z+XI8uR+L1TdWNVRQX9mti5'
        b'Sd/YpNEbm/+Rl7XktRK5VEm04g9trAGZK2J3UvQ/clyFd//4k6rRlWu0OtikimETgxjxecRmugm+cqbcvXpYZwx3M83PLLsXFNKbPpBd/ojFcF/BuD83Z3j+giesULeI'
        b'hxRyvubg2Ids5H2Uz6D8pt4TyIZFKY84TL+0lvxHXMo35J4gdliUjGJ8U1vyUExQxD1BwrBoJooJymK0FOPvIUnuCWKGRXEoSpzQkjsak45jMkmMT/A9QTQd45PZMg/F'
        b'+IfeE8jpivxRRQV/dma4zWZ8xUW971T2GC4lvSn8UdK9QMkZ4Y3QN5N+VI1HUMa4P181vHjZE5bMLZvxiMIuHkMZGgP2f1XOwIMPvaR8M/xHTneD7/kHdRo7oi+xUF1K'
        b'88JnzGoNrqaWgVjdCnw/llXCcEt8TGEX14MS2Nj/pJKZ7JbD+IbC7p91DF+3wK9ScMdCzW5BT5jebjEPKeR8zaLcg7/GQdoSkuW89w2hIS82T2Zwd2dRYGeiWyAT9oCe'
        b'aiIuKsAueIKzjA96jZjO8fHFkFJ8ISQgkR36LNjyv/od1H/gS2ROxeTmTt5ceB0bZQ2BtxZTIYwk+iBhCzwKtxdoN8tBX3wyVg9fY6xGTNGLJJWRCs7APZvszhLISQJV'
        b'TaYtNwV0wNa8WCwBJbER8W9dAE8x8+fCXu3KX+1nG/Az1A9eW0k/qxS/9d4WRmGPUV4VXyWY9lzSqWmlPjG65ad2x/9slukPHb/f1rmts6iz7eOmyvlwWzXvOW6Zot2r'
        b'em38bGcWf/FpHqvWj/rJen582BtSDqHPesmMGHicbzmjJ1YZAmA7oe2rwRVwwvpdc9gKuizUEuyEb9C629c2wudi0AJfth3i4xN82Lee5g1eAseUFt0trbkFXWA7sxE+'
        b'Dy8RYiwTYcGxyJK8HEnpB5gaeHPjpG85XZv0GsSmayrItepwhuX75tjqLSabs6ZQIjFN31rm3Bd6k69/z+nK78w/WjhILOEi8pfZntmxttdlUJg4Gl43KIxqmfOFh9ew'
        b'j3/HvI6FbZva2CitpcBemhph41ZHuPTj8u/5FivuG3FCmHbfYn1WwGD4/dBPnI2BSoHl9+svUL0z+OMsiCXgR5logzAtFqzYyzhTKSXLj8L2w9KZei4Jc1HYiYSdSNgZ'
        b'hV1I2JmEeSjMJ2EXEqbth3GIfTCOzX4YDvNRe06oPQH9ZXBlooqhYCinWFp3s6R60tbBlEkkVWRJ9cBhFVflouIp2EovS6xAqUCxbFTK22qFy2LzC9v5YimwRTRsJY1j'
        b'/VMKiQUwnsXPGue3plt/2db8437Hx5Ow0kfuEU8pxbh8BUPpi9PRr599Gyjsby2H/AF2/kA7f5AyGLkSu5gQO/9UO3+onT/Mzh9u54+w80fa+aPs/NJR//jxKqPlzLkM'
        b'ZYycqfdcJpxKLfNUxmL4XSClJvyzokurMWZLftk/mp+04mWxAEY/GOYpnJRyAhPexD6bE4EBjjKOxPko4/XiWiFCyMmIT0I8sjoHicpaxMZTY07SbToFbP8M63vtTtKx'
        b'xTE2agl/l5hrOz93+jeen08gFxM/K8+jz8//mEaflMdza4Tbp66n71Ten7OHEjOoqPhF26s/mJ9GR96L2sT4lkkt7mvgNB9m+1Em/IrGG+yBV8dYTxpraXAfkvxOw1Yn'
        b'SlnrLCiEx0hN3zVOpeag3/gQqn7Z5gjqt9ZeEnymvaB7gWHArGBi5fXLVUcxVQH7sT2kD/JdQ86f2l0aVOAeusuVVRjh8557zRXPyhW5X6qpS53nT8XHh/G23ftg4a9n'
        b'paSyZitiCtfG8wtro6uc31tW03+j8E3XN8/HShK8+1cK9nltf5dbuvy3lxjNf2gKujnjvb8GxG/OYNXyqTfniiLyOVIX+qvyVfBF0Aq3guP4U5oyFuVcxjTWwd1E8AR7'
        b'K5eBVnCRnANzI8FBRB+mFBWTM0vFBnjNdjfNci/tZBS+mtYEeogGcpnXrPFXuNBsoZkKDwI3fTl1sGcxbQbolZXwMuoDInIxUTI6H8rlI1IFsKfByyuJGlUJ+lPoz32i'
        b'9cCHyrvxRa+j4BY8ywI988Au2pbBVrhPOZqtCJynUK5D4BTYwQInFLOI2OvLBWjInolxSK7Ng7sZlDPcxQTPo0wXHsfiSl5E04E6tBbVQhglVBfYB45tLEGUeGcJ3Cvn'
        b'UukFqBIhOC7lfg8njXfJBBNDnrZtNdbGUDNF09FlU6jgsDb2QT6+6CQ6+gzy8h7xKElo97TB4Pg212FhcHfIoDC017VPPxiV3l//XtXgjPnkdlPmoN+0AdG04fAEbO9n'
        b'6vDUmN7ZvQu65dgK0XBIODH+Y/kJkuAmhkPCujlt7ENudqSWFu5GOOR6/Qgbv/YZcR2VpnSNIy5aXZPJSIzEOlJv0uKe5SDKzgpQCkJKcUy7M6ilUxiMNCzupf1Qce8I'
        b'N5o6y0/+50wAWaybcCrw0CYxHWK/SlbDP/jq3ailkyVHltB2RAJGbeJPsBwi1x+kxn3k9wfaqnGrsJ/6yQydzEARc5hjjOrEfRQYR3cwyK6DE23+yP+VOeRV2EDhaV2b'
        b'h7qm76AsGPC7wDxrIev7nn9Xf1zw12g1FQ3aSU3W4O7k4+6MmtHxxqogSY2+seHf3g/1uqf1o2hsP0SkH/h117/aCwvscCuMjUZ1/dO6UDoGppceWWoxclSGC1pfjU3a'
        b'n//ZU9/a76f6HJrq1ySSW3MrUlxXFJ4tXk0T+N6NTtiyYe5cyYrCjzIKKe25NRVMA26rqelDq3i3xWWb7zNbT3IPHgbv3W37UAy6n599VRr62WCZzwF5W5n6/gcU9bcU'
        b'TvLKT6WMx5gB49cU2hGLZj0hF+NpBbwFz08mVhG9z8gUe6Iwah8Ht4BpQrUnJQ44vKl9U/f8IZ/IYf8AfHdU0TW9E9/b7c0y+8gGBLJ/3kbOArSoSqbd4VOV5z9x+PT/'
        b'ugbBAhwdjWwsyM3ayd9SLxZL0sjFCd/DP6uiHr+DtxgjcK02JuILyoAZQIHIeRQ0ssWLt1YLkk4VxlfFH5AKy7zcb/9+VmLnlmNbk9yoJ3c5LPVWKfNxDB4wvBk+noew'
        b'AgW4AJ63AkYqfI3I8rA1DZ7EWv5omRzL8duYoA+cSpoDtkwqjXtUkEeC2vWaisr6xqpVI752IDQ2iYBStAWUmjypqFh8SbtPZY7MHIrMMkdm3Q29u3YwsqSNfdit3a1D'
        b'85EgbAIsjXDIk7rvEbwXYcF7MXIW2wveDQiafH+w4D0e0WCe9OsayipuHKKNS1MK1n8LPE24ojvxINBiJfZB5hPGH1hUVGma6dmzGesp+oDuVQYPnOPDAyj3emo97AG3'
        b'yEMxMbiEYOFcRCaanw3UBngunVwIgQfATbBtjKCBYKcsqliWBE4zKAXYyXUHp8Eu8k4MzqJlGoqx3pVXzafIg6c/JJQw3+KWKtjkwdMHMgZlwh8vBy8Lva2GW8c8ebIg'
        b'qIW5m8FJO6OtPbCTB4/AXtBNKxYxoQG3wEl8XpkHnp9npyZj5k+BrVpdYRjHcBvl+stmzuWql9FOifrg/ur9W0P2hRzMeo7BXNAhFm9sFouzOw5uOX5qt2Cek3lFzjnp'
        b'rHRfbvdiQZmrLzvpzTLwkynsM24116JrV+T+qmZFS80L5zRbzxRp2Pc8QcBb296es3ChxEW58/d+y/tbPY9J9CEfNB1+7Zm5sxqqdxx9e291qEEQearhVOkSxo5V2/ov'
        b'9bexaqLly988f63wWqHkWWr2Hp/WaZGfz5t1r/I3lREmyWdPFCxW6sAHRu6HRmrGBwE/P6CVOtGGVA/BK/Po8zRymNYMe+jzNHAbXqJvh74KDlHjJZ8d8NAmtjN8LfEx'
        b'NrmbNSvG8dafEzdKEbgbiWADr/Kr+NEWAclWY9SmYHwEeTEE3iYyCYKODnxpowRXSOADnIc74LV8sMeKVLhUPDjLDZgqpVWDd5BEebggFp6ZaWeyoxlu0xCxT+S/Ag1S'
        b'zBpVDTIbQS/olbIdSjEY4G0GPRFTsVavNWpGBHbohsQQLHOZxjJfr/GkAkPa5nzhH3xPLCHE6kBzd9KBZ3uNFzed2dSvHIrLMsdl3a1+rwqu+jwoakCaORg0bUA8zUbX'
        b'ej3xfUsf2SVW35zLLmaf9P7Zgz4z7/kHdRiPpvdyBv1ln0+VD8QVD04tGQgoGRYHDIljzeLYj8VyfODm1ulGh3uVH4sThunbmd1TB0XhvaKL/mf8+xYPSmeYRTM+EYV/'
        b'5YV6aofuuDS6Y6v1tQaHBJRrRXkWnIcRlb4aOcvscN4Tk+c/cYp1kBtGneTHsYqr2I4oGbm/wbDqWoimBSNBpoJtQYHsMfc3OAgF2qFEe40LQnbsLA5BgRNiJ+e3Jlps'
        b'ciomWG092AePA/yiNWBzMBWcCtuJQWmisIe9zuDlGDQ9wTUmyrRxEUGPAfCgGpxD1cD98DTCjwvhUW129d9YhiyU2M9MuFz1t9WdVn37Nt/ZHbPFhZ0ht/5vc+8BF9WV'
        b'/g/fO43eBxipM/Teu4rSlC7VrkgZYHQEZAC7sYsdggVEZbAOVrBi13OyielMJhtg0kw2ySbZZINlJZtk1/ecc2eGAU12s7u//+d1N4c5955+nlOe5z7P95n7lWW5mSLT'
        b'OKc+Lj9EZthi5u6aZBjeaFoeWp5b/CCTTZn4GwRFm6CrGUFobgd34GawPRhbIgO0SoieM005Vk7lc0Aj3Of7GwS/Vo/gidH6KIInTwjBhzAEP5RjQ41z7hf4KAU+Crtu'
        b'216eSjCpifuJvdOAo/MQmxI4f+7udZrbZx/UZxmkR20GIyqgtZgtrvV+/puqzIBiGGrdMbsQJ1qEAomWnf4FI6/Y0LTXEGKnvX7PWStAxYwiN91BR0R7HD1yM0AEh8V6'
        b'RoToDP7fEN2L7nEMdeGn08AB2D1pPGhBvXCmnME1cF7y2FPAkuGPs5sjEi+WdiAy2veW5jLPKdvS3RoWunYdb2NJ6mcLFhgW064/vt4WlphcO5jYenfhuOKF69zORO1Y'
        b'NTnUctxbZW+dAXfbzKnBj41OnXhNO2H/xhdUA0r3BZWhIRPyzURDSLZ6hDTymFDTeA01zbWh+OOaJyLaGbQXyT0VNv32geiSP+jkKue2pzelDAo85IWKKSpBeBNX7elz'
        b'2rPPPqTPMkSPsIz/DcIa22zjETrTiayqcLZqFFTrk9ocTGqPfy+pjR9LaroNpYrSlyKTnc1As7dx/0/I7Dl24fnrnZbM8Im5IGt8fuB0uDc8lU1xXUGXAQ3Wg13gumQv'
        b'PcCW4YuWb47TxdJDiNZeJrSm2CR4iw+czMoSJhsetc55lf+GRXGfWLxg7cPM1rpBgaBAEKOiPo/kggQZ2q3wF3d0Zp8QZWT6LVnOo7DBLTwPd6K796/SGFdLYxoj0iKN'
        b'kwoNkQn0iGzUG0JnARo6k+robMDeVR5+ht2V0u15OrM3ShmQoPJJ7HNLUton9Vkm6RGW4RjCUvPKi0vrqmtfeFYa6lEUQ09YClFbh4Kl+vS0CNPTw99JT6T0Vp4PpTAJ'
        b'Z/taMEaLxHyRGDJik0a12Yj0bJF4udqsobq+tFJcS0YidHQ0TG1SisExxVV14tpQ/UiY2rBMImNQL7E9pJrbUFyHXbmI6+uKlxGHJFihQ20qXlZaWYzdb+BHF0hKrEse'
        b'qjbWolpKyvQwuS6SFHWSOqkYDStWNamtx0EDDl7gYiZbbYidROIi1Sb4lxYIizwm4LOkvrDaVTTWRcGoNiXVywj2l5pbU1ldJVazy4uXqbnixcUSqS9LzZGgnGp2iaQU'
        b'RQwSkpKmFWYXqDlJ0/JSanfgmdpJj+HE8JhjOfrjGkprQrmXIp+WsDIpPhmoQuMIw/83PL7jc4u2lOHJ9pmtSkljD3GpkOI5p8yCKaJ+7gcOZMngFYtaLlUBDrPgCdpv'
        b'FWwjlo8z4W6okNU1oLfoSg6bxtGUATzAMg+CinpMo2nz4Cl4G7zsj62vzvqkZgWlZeXCxmxwNgDuDk7PTQ1ID0bcFbrIa2E2YMsc06SIIIYZXA+PxcIWrCC0Ihi0U1lh'
        b'+aRBL8GzYEc4NrOk80CnNwVa4Fl4niCH1MH1YHc4WiLhlAe8HJ4ynsGeAFfQHhQRwqJo9P6gDwX2BIH1pAez7OFeHaYAXAfO0pTJbBY85weOkqzgShTcirLyKBrsh+d9'
        b'Ea8D9lYxiiObY9Fmsx2b0kVy4OlCigt7aNiyEmwmY7nK0L8hm6WgKMsFrFkZ4YyxKdxTxUel0agh++B6Pwrsk4EjBOJFEA8bM4ICgzAijTE/KxBuy6Qpe3CMMxluB8el'
        b'eA9x5Iny/Om1FFWzYIKdlDQPdsKjoAWViEFIjuYHUKC1EG5j2M9ziCFFzGtjcFAa3AV3JmCexQLsZJckzycN9FtpN/MiayYilwVOkuVWTAOD4DnQjMozQOWdgy2BFGiL'
        b'KyPqIO5gB+jMIMgzHApehAc4ATS4bga2ksIWLZg024H1I0WFLMh7VzSeIuYQ8GRgUXgE6KbQ4F0GJ4ModOs4BZqI5YI/LxJr0GcFSgJoyiiUBVpXZJCS8uoz6miWD43G'
        b'beGt8mUMDbLz4UZcEppyIK8LpkA7KmoLU0mb4zzGQiCNG5OAQUJY7vCCCSkrfhwnoofGUqsFma+NK6dIzTYJ/uERUdhYowt0oBHbWwt3E1CcWfA4bMnACJ/b4a4McGIa'
        b'0e03BxvZ8a7GjAzMNnbBI+oB3pytLyXO0PTyHLgFWlGRiLyAAl5H3dwfCS/U4/2eDToQ6ZMiszVUBq6CDnSvdwB7OAAxofAiM5Gnc2ATKgPTWasEdbAV8aonCIminu50'
        b'0pQBd5lY4nk0r2HH+IMu0igBz9rSjkrFR8YEcUYMc8FbzgI94WGYbG3BAdTJfXOSGaLthofgJQ3VssB2G0S1F2i4Z2EeGRt4MaUmPDIET9hZuzCUDbQ6MJ3cDNpd/TOw'
        b'HQZd50DxJKxxqIHXySmP5nYL2BceTbJdgQdicOt74GXS+kJU42ENFW4D55dPpSjTCWxLcAQeJh3nogV1HeXFg3cHXItD3TVAixlntcqDGzOYlekLToFt4CiHMrVk24K1'
        b'SaTjt60MfezRZodmw3SeC4u5coDTiHs5FR4dgRvTChvjsCHQFriBvJTAdT6oLVjnN4MrBp0Ur5TlCPflMmuzNxruRxkRjfFA23jUELApg7wBh3lzMjLwd1GWFVhbTU+G'
        b't+BWwsHZzQ5GOVDbl/hOQERpAI+SeqaAtXBzBt7ZdsAddA68SfFsWEbuHqTZ3LoV5qXU15jAGwQWeQxRTmuAh8HFkAguRReKEylENkdDmP5cAa0RiAVLxx9vl4JGNrxN'
        b'g3ZzFinq8OIpDgtoAQaYTV9r68Es4YnwkB8uCm0JEeBmEoWu72Ar08MdoE2cgXYWdFWCR9Lm08FAsZQUZJ40LrmGXoCHctWsKp5mszo7A9zMSMNKxTNXcDg06DAFawl1'
        b'cYAcrtOYVnmAdUGwLZwo91fCQ1ICcJKXCrdOC5zOqOvDxqwAtAVRVA5nqrWBIxbCMPZU5+0tdHBMc6fhb8qtLLB3NTw04lfpQT57WZvGEKu/ejFFdnn+ArAetvAoKgCt'
        b'fueAeblkrWVFmYJzARljvp2js4ZDeYJT3HpEmgpCy9hkTAC352JjfQ7omUJxrOl5ySLyzh9uAPszCuBOvNOshwrYRsFum0CCBgwuLIB7YQfs1KGKaaqiKc9pXAncEUmG'
        b'bRxQxMB2E5T+NjZQOA1ux4KbBKRpShbeQ8EJfzQqWXBXamA6w1uHciivAm5YzAzSZY6148yb7Ep8cDg52TkxGyA4BrYuh+0G+MKLyOscIvJ2cI7AFICXp1rAjeDac6Wy'
        b'KK9CbjjYAO+QduXBtYjsc9Ehi05BKYasuiV0Zhb3CVllPjqYd3IRsYDdrJW0EyJAzfa6M3plRiEzHs1gDzxOwUu2YBepeRoaoZMa4DZnKB8ZDlewnQOvwGvwNNP4Q9Zo'
        b'P2g3wzJRAsZ0EzaDFgbZrCk6Cq/xoLRslDMtEPVzRxiHcgQHONLl1UzuFrgPXIXtbPTzFuUCusCt6ajrxEvUIdBVr5+9KDiMhTK3cxbz4LF67Kh9VqIF3I6XPrVmhsTe'
        b'mGz06SjfAWxXQhp8Ax10uNEWNuyF8EwFsw+iK8tVIplxpZzARlfYjorDU+gDOsAhfwYRGtEXlpE0VKHDyglc5qD9bZ+/5kxCY4WazMWu6Cl0Dm8BN8D1IEK8RuAaqnI7'
        b'uqMsooz8F0WlkbWwALRMzQgMTANnfOrhqXS85mwms+Geya6kPeDqRHTUt5ti03Mqdgm4BM8waA9YDzGDsW8XwSM6E/dYEZPtYni8zMwM7U8z0Za1C61oS3tCYwFTTHgT'
        b'WT6YxjLXTYrQiJx2rVoAt6M+V1NpHtWz2WSIpwcL0NUtFYO37fB2zJgWSNomdOTA7mDQSGToXy72oPvceahHk6s+jkmqPMpsafCwFdhKpFUrMPbRhhUmoFOy+U/LuDL8'
        b'ZeUfDfTefXPyVTmWr0VL8g+4cdXb1gu5px4c/zxQcc8u99qy/oPJyhWlU77c9M12i9s/j3vy8wrr2qhx7wR5N5xo+eadZ88+/Fil+vjp6ZdEdey+IvBoqdqIXvFB+k/L'
        b'P+VVbui+eP/q0VSJ4YaXazf98a5y1uEVs7veMPO77rd+QH2WNj3r8+Z4g5CanlMXatbngkW+DVdf/vLvVSkXSl6yWPDaJ88OfeGsuhUWl/2kyMr98OojRxzitl8o/Szu'
        b'2iemhw+8v/vVFUve8D+kcGqpiE175S9+LYJoSy8B8LB24CW2iC411agnt5YYVjTVfDC5tdwwPDWmQvhW2MZYj4PRll+NS7wxlBYUsjHFI2CcofPmGtrohGN9syjA/nau'
        b'v+lneZ/Jet+yPCf87NS6PrFhv3EH9Evqnd9as0H0UTIIZH8WlTTU1F0u/KjYcGlzzTSrmx8oL5oZWE5/ue3L18J9znRJNqmuuB/17BI0V0/9ZuMv89+0jNgq/ctrf/5k'
        b'dmLRrm+6xld+Ez+o2uPyt5deN/6izjXT/dmaqDePV0wZXvDl2wHuZ5845hW+edp8iWPqa9LiqM4nzyq/i7vw5utbhx/NKalU3Uh90vW91+XHKyIu/GFztc34FfM+VFq4'
        b'OQ5br14UVSiOnT3xYXzm1Y/Kb/9z2ZsLZ/30ee6p1avm+o+fKbxQFfpH6Z+cP3n9H8Y+IChp2RGbV/JvNmds/NOs2/MfTvj+i5R72fPD6m+6/Xl8yrK3LT9p4nwe37hW'
        b'ZPj5HaPChPs/utd+mL/x6rPLxQqXT0I33lo/8WbFL66vTI79w9Qksw7BqxXffW7ySdf50zYzZ/0kzah61zguTnThxqPoZ6p4qeI+3Tvpn3S2X9fB1y752jDQEjvAcbDH'
        b'IO5X9KvGcStTQDuB8shBK3mTf3YgTbEc0P59gM4Ct7gMjNeRELTNYv6FR4GT8DYnmQa3jEEbg29xAl5Et5ntFjWmtfAS2GnRYObXYMSj+KCDXT1NStI4wC7YYQK6AlLr'
        b'A9HFcRPz5cIKXmeDs47grMZSqKBaq8HMpurhaaLADC/TRBPLH2yrA9uDiQ0SurBu46Jj8yi6yYEbXAZ84micP/nmgc8AG9iMjtUsVhm4tZp0DW6eZYMWMeoZOsDPNdAJ'
        b'4CbYSPTWjGGrpxbXDFxfwmhFV9SQXODaalsNcFkQ7CLgJhb1RPwyx3ycVtltkh3F82ZZeawh34TmIRbhuuaLD9jjrQ+wzi0nQ+EFO+20amfSSj39NDborAW7SCl5c8K0'
        b'SSaCTSPKaWxw1GkCAYazSwzFanD4I13gLHTCbcvENmEakbV/LBed+pdhG1F0Wwblc8eItcFGKyLZ5oBG43DGqK0rJ1Nr2tsjGoE5gbddyTeiaEd0pm/XqMEttdEqwklA'
        b'539tbzUasoNdXFamNhsRR6EokUHd42hsgG0pFzcNmle40jmq3zmhFwXZd2c1GX/Et2/ldZi0mbSbqfheCn6/b6zSN7bXT+mbouSnNNGf2PA/cnDv85hyn//uuNfH9eUX'
        b'vOmk9ChUOUzv408fsHGW271v440//2Q0Z+DvQqgkeYoiXCUI1sW6whUN3RJl8GSVf4JKkDiSKqrbu2tSb6JKMEnvGbHykqr8k+7mqQSpY18sRGXcDVMJpox9Ua7yn9hb'
        b'O7p48qJS5T/prrVKkDz2RYXKP/4ujXI8+HfrWKzyT75bohKkvbBVoSpBygvrYKkESf/2C4nKf/JdtxcURV6Ifq0fLypKrPKf0Iuam/CrOcb2/FcHUVfU3wIdbe0exlEC'
        b'N7mXwq4zqNu93z5KaR816BvYJesO7+X1Nlwzvyu7z+qLyeiPyVXG5PblFapipquCZ/T5zmzltTa0mQ/YO7eWN6/pt/dT2vspys4v7Fqoso8h3yjjVS6T+hA5OLp2xHfE'
        b'K6Z3T+ma31t2p+palSowc8A3uJvX5dLKOWj+LxMMOrvJoxQ+SvdwjF43RUOgctZJg06DB/hTpr9S4K+Y0p3bld4fEN8b3h+Qctf9boNKkD0gcOkwbjOWT1IJwvsF83sN'
        b'7rnfLb9fpJwyT5U4Xxkzv19Q1ldSNiBw7mTLpygmKT3Gq4QTlIIJpFTNxym7qw49Dr3TVKGZ99Gg5Q781itnOU/e0GneL4xWCqN7eSrhJCVeD0zx8UqPOJVwvBLbzI8t'
        b'I0sVmn4/gbT4V1+NdDVJ8ypdFTqVWVcvyoPW4rTnOzJVFaqj+zHFZahCU7UvRuVJv89VhWb35eSqBHnPZ8tWhWbcn6ESFA4IHId8bX3tHlO2IvsnlK2tAEPTjNuf8XKG'
        b'PErJ992nb6JiwgjG8WHy+4Bb8K75HGrLUSx9PYaCU1o5Of6qnGtL0w4YEe/32LEQOXkbz5fqMokYrTGr+/6CmDSCDEC+vGBhLlVooPvyQo8S4v7PPdoJqbFCXG9GiNu1'
        b'gkUdS8O8zwLTRckCivkcg6UVRaBjDsBcuwt/NuUCz8Jm8hheqQF3QAv6NU6EeNZx3PmM+LUbXOSGczDSlgJupMKi4FFSvnu6ISWvEOHBl1rOmUwR5RpzPyPK1MedyGIS'
        b'i2cyzPu00tV09+y/YXHy+At5XKYROWAd3E/PDY/gYMURqtQonjyOsS6MAE3hERheej8lhhuLSRFTHQyonAABFlJmZlqymHKneFlRCwSJWBBq2imLZFqQ7GtFvUWRh5lp'
        b'tlwmJe1mSt33RUOasyCgaYoRk1IsMqUCHMjDzO88kykiXA2JNKE+4voSjiipmqRzcTahlrGC8CPp97MKmczvzOVRAzwH3CCppckERuhUGgCbCQNdiKUNNa7cBnSFgp0R'
        b'hO8uyoHbw0NCOBTih3fSHohfN4b7Seves3WjnKJ245kqWbNAxgg3cmEHvMCwTQtl1Io5joSZ8gItFbDdGMuDEGN6EP0JYKQNUnAGMVfteNiuFoFuFMJ9jLJAJOISX4b4'
        b'C29gUiIVCI+DC6TWlGAOdWkVHwtFTT8QBTLKSog9vLgSrsNyFbgX/49L0XAzFu3JnQhzuCjZjvla7FtDOcOmpYT7TIfH4BE9K8DKCqLgFLiEAexObMgPxBxpmC+N7qHW'
        b'8NQahrAOg7NwPYFhgFusqGVJoIeB/T7uOAGcprDXnB18arm3K4Pj0wP3LganseKXEZBTKyPgYbJ7kNmYuIJLmcZY475ITVcnMmhON//yD7xS6JwlFL39mOQBh6ZlDajp'
        b'O2dNulWIAZ/5q25cMlxvaNho1zl9h0Pkwd6mrycNXTjvNT9tx0c3f8r45U5VxtJ73wV0hvZcfeet9uG2p7G/nCjw2sOTJfwdljyccun9av823raPphbO3cHNsGXdBPQW'
        b'9UnjVQsRR7/71Nnv1/r2XT7llfNHO/8j3kvm3Az2zM2c+6nwh0VfhJwt+wfYNvvu1dD93A/XSXPbX+sxCXm/VPV0WcGTxo9WrLx++cyHS/5q53W465eH45zrJHP2v7Pv'
        b'Tfmx7Ycsl2ZIg99oOH45acZpN8uXSi7E/LzPM3zXPwP/NPtj9sN/mjizP336jsnlOW/N4w4vPfXznffXbessDzZw2XMAdoVvEW1ZNX2u84GUz0uioh8un/zSzq8ap05o'
        b'TXl6+3xCtP3myPzXz3/N89mU+xNfpv784Re3n9yc/+j8284PXnO4s3TJznj5Cjvr74o//0706sMTn772bXltz/kLb/5j5Z85/0gbunO/d82KZXb1rrIvKy48Wchr/eaD'
        b'fpcp5TtvvbfnW9dJCw3mvP5jqq/gCdahBFvBLvNf0+0M4lGL4HWi4RWQT67hflPhCaLXlx3oRxPcckN4mQX2wbUuzDX9NLgKuq2wFdEoUATMqGFuxvyleIZxCGRT4fAQ'
        b'NtABR0EPYTzQdrYuHTMNWVlwK3d8APZAlklT1glscM4LtDLl7wMt8GUMXL8dK45hpOc9k9aw3MD51YTtQBvmFdCrZSUT6eeZSdgJGomxag3sfckGYDegaf5sig3P0UC+'
        b'LJ3h9BptEJuk01+FG7hgPSscXjfW4CUGolE7C8/ouUvHX4XsZnIczcEpolhnlWHGuEDfmgnWghukGbgvnmxwZsJyDWJ1ONojdBZJifAg4tIQG9pNKqkyjWEGqhJuHWUl'
        b'hLgwsIXF2MS2IM558xjAo+lu7Opy0EQ4q0R4GmxmivECjfpWRIhRgx0ZZEg9wEHU1uDUgKDZFUH48x9qJuxiw5YyA6J3BFphE2hzJqZVY82anDgTwBZfhgU/EwnWwnPz'
        b'SKpdGVyKw6LBYcEK0teFi+EVPePdbKKjB2/ArU+wuqj9olVabUBBDKMP+LwuINjkw3R6fwLYo2W0uRTcBdYzjHYN3EEUFhHDjjHIBDr28wW8J9jFYxSV1/LH67hGmiqG'
        b'1xi2MTqJUOtEeGCBDnLcMJIAjjuCG/+WoZQePISagy0O1OYjTCOOE67RkM3gX8+2p/j2TXUtsXK6JX7A0fmBJR8rL/dbeigtPeS5CtZ5gy6DAb4D+b+95obdz/dFt7Z+'
        b'frCSH9xNq/hh3WHd4X38aPSagWFUuCv5gf38qG6Pfn58r8cgXyjnn3TsdOwXhSpFod2hKn5kP3+8kj++N0HFj9eV6qfk+/XzQ5T8kG4rFT+8O7E7CSN//Halg4i35fQL'
        b'/JQCPxXfv58fquSHdotU/IjuvO78Pn4seY8v+y3TmCIU6GWAIk+BXoaObXF+t8fVoJ6g/rA0ZVjafR9VWH4/f1bfjFn/abrobs9+/sTeML0RiFKKonpR++P6+ZOV/Ml3'
        b'UU+T8GsnRS3qVD8/RsmP6bVW8ScweVw7XbvdRsYrUcWfxEzEqHpiur36+Ym9U8gre6bLiLVjrusq1Gc3RWgfP/BfvNPN81C0U6j1Y8rJ12Y4huI7NEe1+qhs3J/EOll5'
        b'DsVRVrZa8njf0hsRDBN739JrwMa+38ZTaeOpsFHZBDzQsGNcBaffZ7zSZ7yW3yxus+gXBCuS+gVRiJnk3DG5ZvKYTfum0A8pWpSCkaptp2CAByvb/SbNJq1J71sKB/Rr'
        b'sXfYv6x5mZxz0qzTTGUf1MTRwIbKRX18D52Sah/fc8DD52RWZ1a3m9Ijst9jgtJjQu8MlUeKRj+/BHuYs3dsMnleK+ffAGMhn6BGYbHcwazGXRT8Vctq/B2xGrPsadoa'
        b'q+T8LjsQb9IYtWERY3kgq03AhafjYCpNlCmJWWFtMn6ShYOJNPYgR+72vvQ36Cr0jBgvfYPtRnzHvQhkhbEmJL7QY3AQi4M4XLqh1vpL+wvruhAbKMbOhZgnEH1dokFJ'
        b'dNuwQpLatCgnIS8hq6hgVk5KvpotE9epORgdUm2ieZGfUpDP8GR3dGgs/5WY7DlcFexFjwTY1lq2lkVwVYZ5FhgwBQUP3Si+06Cl9wA/7CGXxY9oTH7Io5w8Bi2DB/gR'
        b'6IlTVGPmCGxKOIZNiSSwKRpElACMiBKkj5Hih58EkCe2zoOWPgyOim1oY8pTQ7ZZ0LAxyyyHfmpoYjZp2IFjFjxsyjMLfUShYNiSbZZMD1E4fGhOuYg6+Z2VfU7Bgy7u'
        b'g54+gx7eg16+Cg/5bPSny11RJp8/8sPDW8GRx2n/iLzkdXJTbcxFJPdonT3ohmNOgyIPeYHceNDTTxEhz3zoaulkPeTGH2c9wHdukw2x0a8HfMe2/CEu+oUBd0Wd4Z0y'
        b'lDRoyAA/MaRsXTttcAlDRjhuTNmi1HJ+a/qQCY6boi63yeQRrQuHzHDcnLJ16nMOHbLAEcuRzFY4bk3ZunUm4TYO2eA4f+S9LY7bocxtpbjxQ/Y4LhiJj8NxB8rWpZMt'
        b'T25dMeSI404jcWccdxlJ74rjQsrWoS1JzmmNGxLhuNvIe3cUf+iBhhx3BWuDokSPvPFDT28nc0QBBTTl5Nq6SpGmdI3qdx2vdB2vcp2ocowfFDi2ZirslE4h/U6RSqdI'
        b'lVO0ShDzkMt2NG/MGDZOpM38HlM4HE5lhZg5PaFQMGIBAo9XG8Mb1vq3Xi5lWcCeDa86j+Lltb7MH2NokHirMQAZrFoMHsFxo1Bogf4zIKAIFqNj+ewxcU6sgQuV70JU'
        b'Qo0KLSI4+VwGnEIrYKjlzuXpgDUMCbAGjhuhuDGJG5K4CYqbkrgRiZuhuDmJG5O4BYpbkrgJiVuhuDWJm5K4DYrzSdyM6UW+q7al+bZBuK080jNjErLynKjn/uXbEeAG'
        b'1+ffjAVu+Bfl2P+75QTq/U6mo+h8YSGLiHgYbT0T7NAywih/3JgRZXzJm5PRdiDAEFYjM5fvGEsT5Vw2do0Zwc13wil0ea3znWttKgRGG31FakOCspaRnSIRoXvbinIC'
        b'u6t9JiyVFstkQh/se7xBXCsrrirDu7ZEXOVrbOxXgOEbGUeA2K9ldYmsWiquY7xTYg+G0mqsaIk9JIpr6hinlgRS0i/IuHYJhTW11UbFZQ0SGVa6VJtofhLdSUPGURx6'
        b'zC4rb1CzF1WhZ4vFZZL6xeiZYQ1q1dLq2rJSwzGUTaRU6yl9rXitq1BijYZHloPGlIvGhUcUmM10DiQMC/ScgVYZuVCFeg4lCo1GicsME4yIEO25p/pCtOKHaIkZp1VJ'
        b'6iTE1E+DgqwdW0mVrK64qlQ8gq2pG4w4DfbmiL9OnFOjS4rdcfokMhqsjKt1X8YzXoJQo0bMACIL62uwqXK0sExSIamTBY2phXFer6kHOxX9jVrQa20dVcJiaU1lceCL'
        b'qooVllaiKkqJ60+d60zNTL64T8xboU8WIhpUpdZ5/G/2KHJsjxCJMF4fk6dMF0qLS8RSoQ/6qe/40jdojAtKMikyUsvoppCx8AnT64qvriJEhnHCTIJvhHNNDc7UOQxl'
        b'uoXWSn5xaSV2AUrqJB5Y0RLRIJ/Wl0jFZZo1MTpXDgqrqxjnoSgnAT5FcaanmpXEjElanc6FarFmWErEdUvF4iphhNCnjPFC6UsWYYyu4dqlwwwTExNKyjQDGj52QLXr'
        b'S+N6UxMT1oorJDI0ImgtoyVPpjNAWK8Z1voq7CLzX3qQt2Akx2UrLSmhYR4Li1DfNF5AER3evBJ4UmsKqfHEkENsIRmRBDhZhBnfXH3Pb5smm1pGSkmR6no+5ZP8IXYu'
        b'v6rcw56qx5ZKYB88g1Vnf7VQVCJWUCwkhcImeFFTcEeNKTwGWmxI0W++ZEoJKrfTWLabLJ5LEed7VdMc4PZF4MALitY6niBmonq2m72g0QR0YtxYUmyylQFlOnMQ69Rl'
        b'vhefqPFReXNa7gvbm+afr1/WWrg7AXYYgb1wK7xCils20ZCylK7mYcH4VxPHM/70lriDK3A76IKnni8SNmKxFCOUGtPOKybgaBQ4TMo9hK7DfI+ZPCyvnji+lpkrN3jQ'
        b'A10z9sieL9YnNSAoiFG61ivzOja2bcyVSNZs28OWYdmryVs7N7070TxRZGow9CjrnuDdB0Zz5zpNeGWlNNv81S+dofvXq1NKmxfkt1tuBs/6XR6z09WJPX+7O//eja+D'
        b'eqnCh3/jZg/NebJi+pbxd2PZB03/Vp718Xa/U199I3rXePnm1y/Oc3n7bNu1D3fv/hP3tdBdPziFix63P1qyZMNezk8z/EOmfxcw47H6zGJ4Vyrg1Qcq7iu68v/UYfan'
        b'BYs5/uEffLvo+/nLs26wPjl8x8nPrFHma0wENSvgkZznJGSWCziO8KgXY57aVOH3vO3pLiHHEO5dwbiNPwwOEwndKPLjUq6wFeyo4sDzc2AzA0zeAs6BDVqJm0baBi+F'
        b'MAI3sDGJAXM9CY/P92fEOY5wFwNQB7eEMsC0mz1KMmtHSQPhBdDGyLY22INDpcajRVsm4DyR1Ln4gE6t1FIjswQ7FzBiSzdwiBEZHpTifgRrJ5sGZ+A2jZhtJtj1BN9r'
        b'qoE8l7mSBsKL8Mo0TxkRxaJ4JrmiBvKoLLDRAByC+8Hu/zG3RpB8rLSn7WggH3sGR/bhsnGUu1dnqcL3aJXKLRJj8Aza2DXV7X+p+SWVjbdCpLLxJ6g9U1UOqX381AGP'
        b'YIzaIyKJ+u19lIwjtwSVTSBJlqZySO/jpyPOqDNfITg6TyUKx0g+TJlrmteobLwUViobP5J4isphah9/qsaTSXsGSmnEpFzevLwlXo5K9WR8wqkcEvv4iQ+cXEmS31W4'
        b'yPekS6eLShT6r5O6ezZx/mgpfN75xTuY7X0XB304UOLgPRyocPD+vzZa07m9GGO4RoQEn2HhArp5yiag2LMfsZHkOJrOI67F8n6XUzG8VR3hhVEXTCb+Z6hDG7WIObp7'
        b'2K9BD42QlRZ5qBB1QQ8/h7nlaa9aL8D0+c9RhzStNC3Su8f9Gn4MhqufiVvWpWuZy5iWkdvOSLv+oyZVaCF1tHe932rPHNyeEUgdV6Y92svXcwP13zSIU4Ruhr/Vlvmo'
        b'LY912DqzDsxi2uTItEnvNvlftqdS2x50gfyt9hTjsfkrrR0bn5GrZvFYgCjZf92ojdpZ014Of6tlZaNnzQGL/fXukf8zCtLeNX+rLRXPtwXNlu6WqtcWXxaROjLyR521'
        b'XHYpW692jJ9NzOWIx0EjPQtXHmEXsf8FI+J1EPscNCs0jzDV2bsa/A/tXRHDWF+IGmOcUFaGfeFUiZfqzzpaHcQrTgpiL5gI5rmLy8rQZRxd4Ys13BVxdoN9JwQIK2qr'
        b'62sYtrtYWFq9uERSRVy0GyNy8tOBgvkFCP308ctQnECkoUQl1dWLcNWY5Sf8BFMtdgg/wrPqCooT5lcvxpwVIxHAPiA00GHFJdX1jO8ePEfiMm1fMDeD3c+LcZfKJOXl'
        b'iLNAewDD04xupGY8iD8f1O0KjceKMh1LVFpcRTii32JPQ6P0mDqhT3UN8TUkHWHv9MeBYX2eW3ZCn4SSWnFpZVV9VYVMw6sSPxakISPzIpNJKqrI1ASRPuoVpHEjJZTo'
        b't1qC2D7E4pFStOxcKBn0qFgdV4dLDvUNwDIXYZm4pA6Xi1KUIoZMgiOlWkaTUIGEpJeJ60jfY2LRnE3BVrREZjOWtCRiWZxuTlHZkjpNAmYcyBMd1+qTXy2VYk612lfo'
        b'57cYs+6o+uV+fjqen7RoVAnMo5EipqLuVgUGp6L9teq3imIAzjSMaLWMNFgDevbC9JhYmdT65BskzNLxzIScq0sWikvrhGQEGRrKnxYTFRKqkWdhcRVDvUEvrmaUlXLc'
        b'GNlCQ7WkVKwjmESxVFxRjtP5CueEhs17URFhmmGuFzPNk1SRhuBVkJyclTVrFm4p9m+Fm1pTvHwx8YYlrsWbb4BwMRoXHQeuV2HY6Ao1w4cBDUaPJ34yWj7CUFewlrJI'
        b'tcxVIRE1GtM+zoOKDw+Z9/zqWSRerpX26JEZeoootEomYSqtLielFpctRDND+oMTEJdexcvwb2ZtM3KgUYlkRDAlKa2sk1TgpshKK6XwJtpZpL5xI3kChWhe8uvE9Wix'
        b'6xIgCpAINV1AK2wxosiUwsCC4roSMRbGlWlyoulgnOJI6xcvElfWah6Hj3lMSiuuL19RXydGOxP2cSicXl0rI5Vq8kTECRPqyyvFJfWYFFGChPq6arw/LtIkiIwTplWV'
        b'SRokaPKlUpSgcLGsuG6FbEzLNamjXtSEf92h6Bdlk+hVu/i3q415Uf7f7lcs6fjI0IwZGRIUMDONpWZj6n1uJvWbV16LavfBfdWVWVyyor7Cd2T69JMLoz1HJnDUi9BY'
        b'z5FpqgouHpmS0cmiPEeGfyQZGlRd/XppYvQf66qOHZUY1avbsDS4BWjFaH6R/RmdwWgtape6Tz6zR+o22BEYhDhhEooImRg6M3wyUFRchf5D0yrEe07MvOezhY3OFjYm'
        b'W9iobARLgdkypicUBKYlC30K8+vQX7y/ROqS6bAWmKQphWQl4wdCH0SUmilGwzrSjfpadOSXot0iSfMrQKh31qUU5gl9ZsBjlbWIyFBdESNV6cE4jGTWPdZUqs0qW1Rf'
        b'K/Mddfz92vFJjs6Rk1B3hCWMEti++EwgQBJxwmz8RzgnLGTerycLY5KFkWQjo6FFoNAcmZo4vmDrjzOBo0BJ8B/0Yp7xyCpJFdfWVgVPqS2uR4E0KHiKBJ1mI6uCvB5Z'
        b'CzjdCP3jDCMLQD8novqUSnSooLU8QvqkLHTmlDHFaBuHTk2xuA7vvPgvOiCiRp0/JdXL4oT4cxLa/8vxKYkeoD6EjEqEcTKYVMVSIY6MSlEqqcMEg8JRxw8D/oHfMD9I'
        b'xgB8rgeGh0ZFoZEeqQPjbKAK8J9RM1BejFo3BRGt/kOCxIFGAP8RzokKGbssNEtCf4a0GCBxwkT0izk554RFj3qvIy2SZPQHgVH91SKHaFIy4zGyODE+CDpCEhOy0XCM'
        b'rJASSSnKkJaEikIU8i+cXmqE8un1bMaVuZ1y5cd51hpswS2C8TrTaRrcKNfYToMb8ATJlWqlAXBvsF9+lrOGMSJ2Bk2gMSPAl5h0E4NuuAfISfqgWDsqgKIsQ8w5Uxsk'
        b'izVojO3gCjjOrtJYegfBfTOJsWo4XAtPZWRmNxRrDX4JZkYWvEbKeiRdxUDCO6/KpmbxqXoMmxO/stQfJU3HBqtYSRKrJM5Jz2IAGynYgx2vLYswqgDXwFViVbreNZv1'
        b'Co9a1p2WZfznmaaTsxjRObgEO1D1L8BmTOODi6isVEaIOV3/g8RO0GbqCzeDHUSGJtnwpI8tM0BM5wk/6aGcN9PhZP7EpWEtU1ue2qgdjK+rNm0t6RLWnW0dT4tOrz1x'
        b'+mn1L0XV6kz/HYMxIaYH+yfKOi5Wz7zV6XjwnZOsfQvUi6Z/cIYrKRJt+3SCwcrFLU4fdEetH5R0Zp/Jv+yfkJR7rLb0ZGm3UmH4yWfdgpz9BS6q8z8/uTfP99Old+fc'
        b'U/bJvvzbtZM7jlfMHPfpDNMfUsvVyX8u37roacrlLz78Oj4mJyvqdMmnN+wW/+wz0evRD5Nsg3Z6T3M9krXOa+K76cEXv+pO6Fjif/GTb0QBUx8t/HZphKt4d3v73zPN'
        b'3/lr2dU5fpKtzuf6ynZt78sWW7zxTu373763lbsy17l+gGNS98R12oWfac+ZIVMLfvY1ZHRer4OtufAYuOg/2jPKOdhMpNNLwRFEYacNYNeIj3OwDp4nWq7Ja8BZeGyx'
        b'P9w6LQ2c4VA8KcuNV0Lk70VwfyaWv8MmuHWUDJ5jOKecQY/vnszHIukg2KORSv+aTFpqT2Dy4XYrcMrEBa5/DgSSgYB0AT0Mlt0GuB60ykBvLaaGQB+cFLs2t4JNbNAN'
        b'O8BZRiZ/A6wHPRlgK9yYmUZTrDzaD2wGZ30t/pf+obBFhp6V32ibFbWpTnqpNfRLpzUQeS6UMKDfNUSxBIPYO7bWqWzcP3H0HvD2aTXFMGce8obOgG52v32E0j5i0Nu/'
        b'K7/bprusN6pHejf8bmJf1NT+qCxlVNb9UlVUniowv8+7oJXTOr3NFLvk5rVNYFx0NycP2LrIPVS2XqRov1b8Gnv7btcl+AILpiepHCb38SdjlzNzFbF9dpFN7AEbu9ay'
        b'fpcgpUuQyiaIIFH2O/orHf1V9gHdXJV95Ecufn3+2SqXaX2CaUMstm3oYEhsr0dfSMpdm/dCUrAyJzEyslEKAod4bKtAouzooeR7yPOJBmjge/xAJT+ym6PiR/74xIBy'
        b'8nxM0agUF39FksolpE8Q8vMQGz34+YkhJRChd1aBgw7eCrbKIaCPH4DfWQX+RBAHoZldMoeCHq7JLtQrHONkR/Yr5obJduxX7Lj4t4txciT7FR/D5BD2KyFc9JsRuVsw'
        b'IvcRoRW2Jv5dtkpjqGCUt+lRlktsNPMLseAdb3UY4SvXkaZDsdg9FCMUhv4enULsu/LFsOMEDZijgR3nFlKFPB0U5v8WenyjL6t2mBrjDcj1uZPOkznp3JM4M8MYtB7p'
        b'04XFFDExgb0+4JysHoN17ORMB6cptLrp1XBd6YhZE9qyumaboFGbQfmtnAGPg60aWBpbcDqf5AMvN1A0vEHBS2Kwj9S1PmxVZAxNkK4cf3bJZQqSzpmvNUCCjXliMewg'
        b'JjZTneHLWnMleB10loI7cAspJXeVQUQDi1gnSe8s0gCmq8qtPP5JTSaGSA4BPoyhSiDfcu5Omnl4dsZKJmVRoKnbm6wQYp30NHIek1LtZ8opZpOH0h3CqUzKJ5XGqV/R'
        b'BK/B9IG3BZOSX2HM62AzIA5dMTLm4evzDCxvs0mTTF2m8pmDfBm8bJqfk5NDRVZTdDIF1q2hGZyKW8Vwb3hISAhltxQN0DEKrsPIn6TX4SthSz4XHM6hsM/pE+iVHTxD'
        b'BjapEFzRWTvBXd4UMXdKDiHZJoD9xuERoAMbPBFjJ3gQKMjo+sNm0Et8kFGZoSJwAJwhVj9WoBENLzYzo8AFy7DCPJKYFYoGmdguURFgSyDoYTPwRbvA2lk6EyXOao2R'
        b'khW4QC44NvAIvJ2fI2RT4KIV+s+WBzrrpxI6yl4Fro1YKnFWMlDMq8BlxpgID/IlkZEhny0khm0TJQ3MeF4sMLQsZUCGMnmJJsx4eoGXLfJrE3JyyBFDFYMzy0gJdXxb'
        b'u3IqB1PwqlfmSTXQLZugPCE/B8h9qTQDKm61CeyEL0vI+E8CJ2G3zCw8hLMEytEon0Yz4gs6JSe/OcqSYTC67968e7wgYxqYbHn44ys3vyymlxtdtv5b4hD4Q/L52s8u'
        b'wFfDjR4OFH3+x2d/kX44L+SGpYP62O62v98+NLzlmcn5prvW1lcCjbqDPxu8UPhP889azm+hjD79KTT1dknbL579P8Te9eKkXpZfvm/3JHPC6yk1B+awar8JTKfe/Xb3'
        b'1guLtx9WxB2L5417OVsR++T41ci741Xz/3r/TcPuVU3fhaeJHV+ZPEsSE3PK//Dqrfvy219L//rKWftOdn7437vcfzQevGU5GHK/nT9r17Tkc98fDMiC78WVfGNfFtpc'
        b'OqeHf2rya6fuLhatWrbR1d+o0yBq9g7nHfO+H/6jd/a2w423br57wvz0V4Px498P+HFS/KJ1p37u2bL65tGV8oVpvzS/vWAoYm88v+cVUUPNJae2qmV1P0Z/MPsfuypL'
        b'pT5J9XtvbV20wlN1xailvOW7NdlZ45ePv3r8nU9uRodmFlZ//t22b97ye/pF9453pgeETVhtevu9wONXbeMD/PeL80847okqO/jXKa1Jf/vZYuZg7omqcl8++Vwuci7T'
        b'+1r+K/eSDkdwCDSDg4zBTWPGKn+ibxDICw1CN/MbLNAMm+FxBkthfwY8iu7BmXSpM8UR0eAQ3DqeMRI5De/AsxkBDPZ0JLjJwE8HwDOMVoE8JFFn7bSI1tg7HRxHLjpu'
        b'BuBgBjxr9gJkC2EK1whscGUUDE6AkwWM7oE7PKFRP4gE3Uz97clw0zy4ZRSgfjhiEg6Ra9wKsJ2rU5FgweYRY6R62Es6ngD2lkpBi77V1BqWG9wZRvLXWjmNUZyYC44w'
        b'ihPRrszAnQZXYTcDNAHWgrPMFRPeoRmzrV3+cF/GKGdG5mADOwy0J6Jlf5XUAS/D0z5jPbPDFpNqdBFUkEvu6hkTMvQ9HZmvZsOjYEOyCTjFKIu87Bmnr0AxcYlGfQLc'
        b'hLeYMTxeb6TV0IDdyYyShim8QLpgYVSqsz+aBg5rQMIvw1ZSeNKM2c9pcMxkNDhqKHKxNYcbX8KupWDbC3RR0NGXAff/Bw7mR24Z+OOfxrk8uWvqOZfHJpYEWMKVOJfH'
        b'ro5MBoQe/cIQpTCEsWTvF8Y2pWIw8WUYaxxDlDsL5bbtsxWitvlNUx4ER2OU8tMvNaW0+sinKx38lfyAB3xXxnJFXntyaefSAYHjgMBFbtdmMSAQ9gsC0Z2vG138IvoF'
        b'E3v5/YKUu3yM0VtwclbnrG5aJQjrF8QoBTG9VipiLN9hgU1JcCZFsUoQ0m3dbdMniMQvzLHneYJcnqsSBHezutl9ggisvZ3a7xSqdAodXVRvYm9Sn2Ayed+R1ZalEvj1'
        b'C0KUAmyHJGDskAQxYxs4ude+X5B+d8oLn1feTe1PLlQmF/Ynz1cmz+8rqlAlV/6elM5Mv+d3zu9GPYhG46FEQ4J6ORmNV6eNfOZRZyUGaXcmI6j5P+5AMtFUMZfXKug+'
        b'gd+vPUSFDAhcUYOGIh1D7B5Tjj72w1GUwKW5obVSZe89HO1o6/vQghLFDU2hKVe3jsq2SvlKlUt4k8knNoIHHl4np3ZO/dVxJiX/yuSQbvV7Rik9sRWUIA6NglKAraAw'
        b'tMUILWhJYsjKKBA1z8jTfth6pHkK/4c2Rp5RiK68mrOG+JTAucn0eTTw31Z4IWjgY5dCrQMi+i/YevY7Ka40bT30e+13ynFZLHqMMxedtz+CQM/VgL5yNGrk2KkLTwf4'
        b'yvsfAr5WoGs3lx5z7X4eqdkgm4D2rYAHl/pj/+45qejMQgcT6CpI1fgpzwMHeFQq3GxQA7e4kntUSnYW2gtPE0tFtpSGu8BRxDvvAG2MsfalSBG8Bo8T42507dyohdxr'
        b'BAq4z38aRmB9GfTmUcRZhkLCnbCcLXuCEnyZH8Q49bPCvoRaQ/+QGJM1ThRgpkjdNo4d9I8zr3w9rYDzlwrv9EDsws87M77VyqvjDQGwfWWnZL3vnnfYB2xf2T4nvtE1'
        b'P6jVCDbMkLcP7Flbzg3f0n0gMcl7d+geUarl1UFg6lJiano809SU+0bnjgTQ6ue+J6tNGMDlFRnxeFVCswLfbR9mcjfXzS0O2uW72fMdzr3ioK3TAvvMNv7yJefxDMMb'
        b'1kHDqaUX3fcYffWnBXaC7VtFuz33eKba5a/2CQdZ9xY08ucHNQ2lV+SU9SX8aKGI35m2LsHFh11g8+rdBW8GvNvkufHV+208KiLKK6rZ2NeCSE5Y8MJcMv6IQ4umwRkv'
        b'cA7eDmcOxObganwIaExHDMHhVXA7a3UI8xZsgPJy9NoMHNW4jM9mOcGzYDc56ByMcuH2CDQZWwOC0shrE9jNgjdXgU5y2rsFesGLEenw0lKN5MQInGShyTwwkRReYwLk'
        b'GWazArBF69ZMdBkwmcyCrfAmzZyBjRjBD18UCmFP8LRAFj7p/YwXM240NkwGPTp3IOxU3DPsDcSRw9xjmi3xxSQAylemwZ3oBsWbz3J/CfQwVrdtYN0Sf2JzGxgEd4Je'
        b'XxY6wzvYYNOqaWS04J1gJ3S8goOmcGtwNpfiTWDZ0xOZ+8s6dDnbnqEhXR5lFFjPZ4HOcniaGa7N82xRi3eCJh/NcCWyBPAW2M5UvBUcILbYI9bk6KqyD/SsAM2k4vlW'
        b'c/2Dy9GFnZgD84CCFVAD7vzXoE9aOcCIf3e1me54lhU3MP5BWBpZULqI4tvtj26O3h/fHC/36LfxVtp4KxLPT+2aej6rK6vXoz9gkjJg0t3E19Lvpd+v608uUCYXfOQg'
        b'6nOLVjnEYONatE+btpm2m6MD3saecTvcb+OjtPFR2PXbhChtQgYdRHIPBVsxV+UQ15Q04OV/clHnohOL24xbOWjDxpnlBR8IQh5id/cP+Pb705rT9mY8cHTuiG6L7ohv'
        b'i1d49DsGKx2DBwQOHYZthnL+QfNRhQw6i+RuJ707vU8GdAYo6roLVG5xvcnvOyfczRtwculIbUuVFxzMHmZTLom00jnhEa7nU+eED5wTfpJhtaA/cK1TPLh/8DBOCTfS'
        b'97xYy/6XSo/MwDN+FkeZchJX8diA0JWjhxqzUkjTAuxn8fc4JCGOIXwN1SZF2GSzGCvHyGr/hMv/Mw6+xcH3OHiIgyc4GMY5OESewcCXE0hzQ93xxiK/s335L7TqdKIp'
        b'fdPOf0Mx9D5N/FLViRfLGKkTOQntdAaaVv9DqafeuOORXjv2HzP+b9OaAJs7yaQ0MeJ8yOGYWT4yxf7h2Z1Jrct7Su/lv25zN21wnJPc/5rNtfxeo9eTsHf4XGw8HD+Z'
        b'HmZ7m3k9pFCAXcOjpxwcz6O11p1R2Lozhlh3anzZYwtQx6jGjBHrzkhs3RlNrDttHActvQb4oeiJTXhj0siTePxkMk0eabKF4Gxh+mai2iePDFEHhiiWeRbdJuuxeUh+'
        b'qe0dDyR3jusXRStF0b1GSlFivyhVKUpVidJVThlqF7fO2H73WKV7bK+X0j2h332q0n2qyj1N5ZKO+uucQT+maEEm/ZCNyxrm1dNmgU8pHD42wE+GyJPhKnasmfMQhYJH'
        b'DTRqRJu70sxlmMU38x+iUPAYsU+uj3F0xGDR2wfskulYXS4FT7qbObDQeb8HHvSlsyXG8/ZwZEloepyu/STOfbtq/WTLw7Z2Ob/Y215O+UN49Nedae3zf+LAg5mpBy5F'
        b'hd5b1HHshw8Hv1nvVatu+2Hp/v6sLwuqjvuff3T6gf0nPKM9S4zFd3KErqf+7Lr23aXdK7+r/OSK4mif+9c2R7+xTRneV2r5/tsev3AeVFb0Dj8Jc1G++1bs/T0hrygr'
        b'JyV+ELfT7sbObzM8z+Z/fDLITJKYf0B50O7SMdvvfd5OMu2vMf9WuJnfahVqnd+06Lv2iebb3rnzIXdjz7u25txxVvyoyw1zpAEDX/BkbyTnbHHsff9oU/6r77lfyCpR'
        b'97EnvrePpf7SKvsPpR942D8tt9+UG/vGhKfv954QnXzb7PGZhUXWEeOLfrBXHVj11GSJaM2br55/KnVX/eHiYrfTs3reuFTs6fzI6NUj8z6u/2YVdGnIccmL+fbp9yvf'
        b'/rDo2b3tFze1fHv4n9R3P6b/EJPtyyYAin5wQzGGjDgDOmmKjkFcboiU8Ips+zR9owV0kB/RfDSB+xhHPQscp6PT6urzjrCYbyDO4Kyvx9iVaPibwf/Fuv8PdgoP5mic'
        b'TP49t2WM2Tyw0by0urisqKg2DO3g5LhMRCT6T3RcRlBmtkMcAyP7QQvrprDtS1tF21e1yeRh8uLOyPYVitz2l3o8umt7RT31vbk9yy4G3Uu+bw1TVWGZHwkcWsNai9si'
        b'243k6Yjv6rZHrGPfhGylfXZfXkFf4XRl3gyV/YyP7IRy65aqPksP7KtoJj1kTFnzmxKabRsThyOsjDyGKRz4eBsFDlMoGMLBcAE9wcihafoTCv0ZXkN7GDm02j2h0J+h'
        b'bJoythxm1XKM/IepkfApCdF6NbYcIi+H6owogZfCRGkf3mg6zDM0Egzb1bKNnFByFD4l4dBCA1JYHilmJHzMhLiwh+Tlj0MJAtoojR60dj1m2hc4RSWcqrJO7TNNZY7b'
        b'bQlOybbUK7Y2yT6azyHOahYa6//s88f/Db3g5bJg9Je1F50ymDxI4EBohGIYvlCatsQfWPSC32PggG8Tp3njqRsmCTy25KtFb7NkZ9Ejw4IK8Y40YzCZn/zSir96GLvF'
        b'cLydquRzLPpuhX+Q/mOGPRiO+mRGmiVn0eNTiiPvZEw/M9gtfu0we2pQ0ft2geIV1l8f+WZa9OP6k0f+fHHykofP3pz+D2nhu1nPqjwaLuWJu9YoLmbML+hvc8rjd6zf'
        b'GPTh3BPpmadSlg5+meCw7UNLfoRpgF/M+wLgvmBjqFdryeZYhwDLHuDgeWWgeDfskaxO2i18unCY/0N17+duWbPDECOCsYQ8QAu6O6M7/TRwchz+SL8jw4AyARdYUAE3'
        b'TyUyuMoqsCtjWiDsAZvAOpRwGr76W8GbGCxoB7hG0tTDFrgHbAe74W4suQJr67DM1IAyt2a7wC2RRAi6CpyZk5GW5ZdlQPFmgA4OyxCeq3lCOMjzMWvg9mAeRef7RVPw'
        b'aC44Sp4bLoKH/dO5FJ1RAa5RiBPZ/xK59C+BR+BeVBTXHV3Xd2RhdB0TXxZsSpEx1/oj6eCCLC3LxVv32jiNBbrhFXCVsElhqWUZ5MTbCvclMQ4f4DZ2NuKtTpNrP1ib'
        b'Dm/gFHDLDI3SxBp4hFTNFfkRRniqcaqGQTO1YcFLyeA64/PwUAM8DxBDEQBOzK3RpDAGF1ngErgeTqR94LAB8eJ+wRQ0Ll1SDy8uMV1ST1P2cDe4YMEGO6rANkYoeSTC'
        b'NwOXAA6A8/5pWRhM3wQcYMEjoJVF8KjgutlgLTgOL+OBD85AB8Eu/KUbxwwoRw8O2ICmttfX598+Cv5/eTLorXkfckZM1v77jVNilGUTDsgRgS/az9D6f+xAcW0GzPj9'
        b'Zi7oenRwmcrMZ+2UAY7xlsx1mX1WomMx73MCPuSYof9/zHH9lOP9KSfwY477MG+2JRftqCPhUxIOLRNSpvy10/SEU65qtlRcpeZgDX01t66+RipWc6QSWZ2ag0Wvak51'
        b'DXrNltXVqrkly+vEMjWnpLpaqmZLqurU3HJ0tKE/tViBDvuSramvU7NLK2vV7OraMjUPsRd1YhRZXFyjZq+Q1Ki5xbJSiUTNrhQvQ0lQ8cYSmdamXc2rqS+RSkrVBoz1'
        b'v0xtIquUlNcViWtrq2vVZjXFtTJxkURWjXWu1Wb1VaWVxZIqcVmReFmp2qioSCZGrS8qUvMYneaRI0CGl/2C3/onFI6ZA+wzTYY5mWfPnuHv3FY0XcbGm+/o8CEJf89+'
        b'jM+se4a8BAF1T2CS4M7+ybAcq/GXVgapLYuKNL81F4afHDRxYU1x6aLiCrEGIaG4TFyW7WtIWCu1QVFRsVSKTjzSdsyBqY3ReNbWyZZK6irVPGl1abFUpjbNwxrVi8Up'
        b'eCxri1ma6WcIgbmnTFhcXVYvFcfXVrAYIxxZJgqG2DRNP0Rd4wyZUyZmaw0ecaSWNH9ovogysuo3dFQaOram9xt6Kw29+wLi73lBH1VA+oCh5aCxXZ99uMo4oo8TMUhZ'
        b'Ngn+SDmQ2v4/3/ZGjg=='
    ))))
