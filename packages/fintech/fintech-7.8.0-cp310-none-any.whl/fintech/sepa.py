
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
SEPA module of the Python Fintech package.

This module defines functions and classes to work with SEPA.
"""

__all__ = ['Account', 'Amount', 'SEPATransaction', 'SEPACreditTransfer', 'SEPADirectDebit', 'CAMTDocument', 'Mandate', 'MandateManager']

class Account:
    """Account class"""

    def __init__(self, iban, name, country=None, city=None, postcode=None, street=None):
        """
        Initializes the account instance.

        :param iban: Either the IBAN or a 2-tuple in the form of
            either (IBAN, BIC) or (ACCOUNT_NUMBER, BANK_CODE).
            The latter will be converted to the corresponding
            IBAN automatically. An IBAN is checked for validity.
        :param name: The name of the account holder.
        :param country: The country (ISO-3166 ALPHA 2) of the account
            holder (optional).
        :param city: The city of the account holder (optional).
        :param postcode: The postcode of the account holder (optional).
        :param street: The street of the account holder (optional).
        """
        ...

    @property
    def iban(self):
        """The IBAN of this account (read-only)."""
        ...

    @property
    def bic(self):
        """The BIC of this account (read-only)."""
        ...

    @property
    def name(self):
        """The name of the account holder (read-only)."""
        ...

    @property
    def country(self):
        """The country of the account holder (read-only)."""
        ...

    @property
    def city(self):
        """The city of the account holder (read-only)."""
        ...

    @property
    def postcode(self):
        """The postcode of the account holder (read-only)."""
        ...

    @property
    def street(self):
        """The street of the account holder (read-only)."""
        ...

    @property
    def address(self):
        """Tuple of unstructured address lines (read-only)."""
        ...

    def is_sepa(self):
        """
        Checks if this account seems to be valid
        within the Single Euro Payments Area.
        (added in v6.2.0)
        """
        ...

    def set_ultimate_name(self, name):
        """
        Sets the ultimate name used for SEPA transactions and by
        the :class:`MandateManager`.
        """
        ...

    @property
    def ultimate_name(self):
        """The ultimate name used for SEPA transactions."""
        ...

    def set_originator_id(self, cid=None, cuc=None):
        """
        Sets the originator id of the account holder (new in v6.1.1).

        :param cid: The SEPA creditor id. Required for direct debits
            and in some countries also for credit transfers.
        :param cuc: The CBI unique code (only required in Italy).
        """
        ...

    @property
    def cid(self):
        """The creditor id of the account holder (readonly)."""
        ...

    @property
    def cuc(self):
        """The CBI unique code (CUC) of the account holder (readonly)."""
        ...

    def set_mandate(self, mref, signed, recurrent=False):
        """
        Sets the SEPA mandate for this account.

        :param mref: The mandate reference.
        :param signed: The date of signature. Can be a date object
            or an ISO8601 formatted string.
        :param recurrent: Flag whether this is a recurrent mandate
            or not.
        :returns: A :class:`Mandate` object.
        """
        ...

    @property
    def mandate(self):
        """The assigned mandate (read-only)."""
        ...


class Amount:
    """
    The Amount class with an integrated currency converter.

    Arithmetic operations can be performed directly on this object.
    """

    default_currency = 'EUR'

    exchange_rates = {}

    implicit_conversion = False

    def __init__(self, value, currency=None):
        """
        Initializes the Amount instance.

        :param value: The amount value.
        :param currency: An ISO-4217 currency code. If not specified,
            it is set to the value of the class attribute
            :attr:`default_currency` which is initially set to EUR.
        """
        ...

    @property
    def value(self):
        """The amount value of type ``decimal.Decimal``."""
        ...

    @property
    def currency(self):
        """The ISO-4217 currency code."""
        ...

    @property
    def decimals(self):
        """The number of decimal places (at least 2). Use the built-in ``round`` to adjust the decimal places."""
        ...

    @classmethod
    def update_exchange_rates(cls):
        """
        Updates the exchange rates based on the data provided by the
        European Central Bank and stores it in the class attribute
        :attr:`exchange_rates`. Usually it is not required to call
        this method directly, since it is called automatically by the
        method :func:`convert`.

        :returns: A boolean flag whether updated exchange rates
            were available or not.
        """
        ...

    def convert(self, currency):
        """
        Converts the amount to another currency on the bases of the
        current exchange rates provided by the European Central Bank.
        The exchange rates are automatically updated once a day and
        cached in memory for further usage.

        :param currency: The ISO-4217 code of the target currency.
        :returns: An :class:`Amount` object in the requested currency.
        """
        ...


class SEPATransaction:
    """
    The SEPATransaction class

    This class cannot be instantiated directly. An instance is returned
    by the method :func:`add_transaction` of a SEPA document instance
    or by the iterator of a :class:`CAMTDocument` instance.

    If it is a batch of other transactions, the instance can be treated
    as an iterable over all underlying transactions.
    """

    @property
    def bank_reference(self):
        """The bank reference, used to uniquely identify a transaction."""
        ...

    @property
    def iban(self):
        """The IBAN of the remote account (IBAN)."""
        ...

    @property
    def bic(self):
        """The BIC of the remote account (BIC)."""
        ...

    @property
    def name(self):
        """The name of the remote account holder."""
        ...

    @property
    def country(self):
        """The country of the remote account holder."""
        ...

    @property
    def address(self):
        """A tuple subclass which holds the address of the remote account holder. The tuple values represent the unstructured address. Structured fields can be accessed by the attributes *country*, *city*, *postcode* and *street*."""
        ...

    @property
    def ultimate_name(self):
        """The ultimate name of the remote account (ABWA/ABWE)."""
        ...

    @property
    def originator_id(self):
        """The creditor or debtor id of the remote account (CRED/DEBT)."""
        ...

    @property
    def amount(self):
        """The transaction amount of type :class:`Amount`. Debits are always signed negative."""
        ...

    @property
    def purpose(self):
        """A tuple of the transaction purpose (SVWZ)."""
        ...

    @property
    def date(self):
        """The booking date or appointed due date."""
        ...

    @property
    def valuta(self):
        """The value date."""
        ...

    @property
    def msgid(self):
        """The message id of the physical PAIN file."""
        ...

    @property
    def kref(self):
        """The id of the logical PAIN file (KREF)."""
        ...

    @property
    def eref(self):
        """The end-to-end reference (EREF)."""
        ...

    @property
    def mref(self):
        """The mandate reference (MREF)."""
        ...

    @property
    def purpose_code(self):
        """The external purpose code (PURP)."""
        ...

    @property
    def cheque(self):
        """The cheque number."""
        ...

    @property
    def info(self):
        """The transaction information (BOOKINGTEXT)."""
        ...

    @property
    def classification(self):
        """The transaction classification. For German banks it is a tuple in the form of (SWIFTCODE, GVC, PRIMANOTA, TEXTKEY), for French banks a tuple in the form of (DOMAINCODE, FAMILYCODE, SUBFAMILYCODE, TRANSACTIONCODE), otherwise a plain string."""
        ...

    @property
    def return_info(self):
        """A tuple of return code and reason."""
        ...

    @property
    def status(self):
        """The transaction status. A value of INFO, PDNG or BOOK."""
        ...

    @property
    def reversal(self):
        """The reversal indicator."""
        ...

    @property
    def batch(self):
        """Flag which indicates a batch transaction."""
        ...

    @property
    def camt_reference(self):
        """The reference to a CAMT file."""
        ...

    def get_account(self):
        """Returns an :class:`Account` instance of the remote account."""
        ...


class SEPACreditTransfer:
    """SEPACreditTransfer class"""

    def __init__(self, account, type='NORM', cutoff=14, batch=True, cat_purpose=None, scheme=None, currency=None):
        """
        Initializes the SEPA credit transfer instance.

        Supported pain schemes:

        - pain.001.003.03 (DE)
        - pain.001.001.03
        - pain.001.001.09 (*since v7.6*)
        - pain.001.001.03.ch.02 (CH)
        - pain.001.001.09.ch.03 (CH, *since v7.6*)
        - CBIPaymentRequest.00.04.00 (IT)
        - CBIPaymentRequest.00.04.01 (IT)
        - CBICrossBorderPaymentRequestLogMsg.00.01.01 (IT, *since v7.6*)

        :param account: The local debtor account.
        :param type: The credit transfer priority type (*NORM*, *HIGH*,
            *URGP*, *INST* or *SDVA*). (new in v6.2.0: *INST*,
            new in v7.0.0: *URGP*, new in v7.6.0: *SDVA*)
        :param cutoff: The cut-off time of the debtor's bank.
        :param batch: Flag whether SEPA batch mode is enabled or not.
        :param cat_purpose: The SEPA category purpose code. This code
            is used for special treatments by the local bank and is
            not forwarded to the remote bank. See module attribute
            CATEGORY_PURPOSE_CODES for possible values.
        :param scheme: The PAIN scheme of the document. If not
            specified, the scheme is set to *pain.001.001.03* for
            SEPA payments and *pain.001.001.09* for payments in
            currencies other than EUR.
            In Switzerland it is set to *pain.001.001.03.ch.02*,
            in Italy to *CBIPaymentRequest.00.04.00*.
        :param currency: The ISO-4217 code of the currency to use.
            It must match with the currency of the local account.
            If not specified, it defaults to the currency of the
            country the local IBAN belongs to.
        """
        ...

    @property
    def type(self):
        """The credit transfer priority type (read-only)."""
        ...

    def add_transaction(self, account, amount, purpose, eref=None, ext_purpose=None, due_date=None, charges='SHAR'):
        """
        Adds a transaction to the SEPACreditTransfer document.
        If :attr:`scl_check` is set to ``True``, it is verified that
        the transaction can be routed to the target bank.

        :param account: The remote creditor account.
        :param amount: The transaction amount as floating point number
            or an instance of :class:`Amount`.
        :param purpose: The transaction purpose text. If the value matches
            a valid ISO creditor reference number (starting with "RF..."),
            it is added as a structured reference. For other structured
            references a tuple can be passed in the form of
            (REFERENCE_NUMBER, PURPOSE_TEXT).
        :param eref: The end-to-end reference (optional).
        :param ext_purpose: The SEPA external purpose code (optional).
            This code is forwarded to the remote bank and the account
            holder. See module attribute EXTERNAL_PURPOSE_CODES for
            possible values.
        :param due_date: The due date. If it is an integer or ``None``,
            the next possible date is calculated starting from today
            plus the given number of days (considering holidays and
            the given cut-off time). If it is a date object or an
            ISO8601 formatted string, this date is used without
            further validation.
        :param charges: Specifies which party will bear the charges
            associated with the processing of an international
            transaction. Not applicable for SEPA transactions.
            Can be a value of SHAR (SHA), DEBT (OUR) or CRED (BEN).
            *(new in v7.6)*

        :returns: A :class:`SEPATransaction` instance.
        """
        ...

    def render(self):
        """Renders the SEPACreditTransfer document and returns it as XML."""
        ...

    @property
    def scheme(self):
        """The document scheme version (read-only)."""
        ...

    @property
    def message_id(self):
        """The message id of this document (read-only)."""
        ...

    @property
    def account(self):
        """The local account (read-only)."""
        ...

    @property
    def cutoff(self):
        """The cut-off time of the local bank (read-only)."""
        ...

    @property
    def batch(self):
        """Flag if batch mode is enabled (read-only)."""
        ...

    @property
    def cat_purpose(self):
        """The category purpose (read-only)."""
        ...

    @property
    def currency(self):
        """The ISO-4217 currency code (read-only)."""
        ...

    @property
    def scl_check(self):
        """
        Flag whether remote accounts should be verified against
        the SEPA Clearing Directory or not. The initial value is
        set to ``True`` if the *kontocheck* library is available
        and the local account is originated in Germany, otherwise
        it is set to ``False``.
        """
        ...

    def new_batch(self, kref=None):
        """
        After calling this method additional transactions are added to a new
        batch (``PmtInf`` block). This could be useful if you want to divide
        transactions into different batches with unique KREF ids.

        :param kref: It is possible to set a custom KREF (``PmtInfId``) for
            the new batch (new in v7.2). Be aware that KREF ids should be
            unique over time and that all transactions must be grouped by
            particular SEPA specifications (date, sequence type, etc.) into
            separate batches. This is done automatically if you do not pass
            a custom KREF.
        """
        ...

    def send(self, ebics_client, use_ful=None):
        """
        Sends the SEPA document using the passed EBICS instance.

        :param ebics_client: The :class:`fintech.ebics.EbicsClient` instance.
        :param use_ful: Flag, whether to use the order type
            :func:`fintech.ebics.EbicsClient.FUL` for uploading the document
            or otherwise one of the suitable order types
            :func:`fintech.ebics.EbicsClient.CCT`,
            :func:`fintech.ebics.EbicsClient.CCU`,
            :func:`fintech.ebics.EbicsClient.CIP`,
            :func:`fintech.ebics.EbicsClient.AXZ`,
            :func:`fintech.ebics.EbicsClient.CDD`,
            :func:`fintech.ebics.EbicsClient.CDB`,
            :func:`fintech.ebics.EbicsClient.XE2`,
            :func:`fintech.ebics.EbicsClient.XE3` or
            :func:`fintech.ebics.EbicsClient.XE4`.
            If not specified, *use_ful* is set to ``True`` if the local
            account is originated in France, otherwise it is set to ``False``.
            With EBICS v3.0 the document is always uploaded via
            :func:`fintech.ebics.EbicsClient.BTU`.
        :returns: The EBICS order id.
        """
        ...


class SEPADirectDebit:
    """SEPADirectDebit class"""

    def __init__(self, account, type='CORE', cutoff=36, batch=True, cat_purpose=None, scheme=None, currency=None):
        """
        Initializes the SEPA direct debit instance.

        Supported pain schemes:

        - pain.008.003.02 (DE)
        - pain.008.001.02
        - pain.008.001.08 (*since v7.6*)
        - pain.008.001.02.ch.01 (CH)
        - CBISDDReqLogMsg.00.01.00 (IT)
        - CBISDDReqLogMsg.00.01.01 (IT)

        :param account: The local creditor account with an appointed
            creditor id.
        :param type: The direct debit type (*CORE* or *B2B*).
        :param cutoff: The cut-off time of the creditor's bank.
        :param batch: Flag if SEPA batch mode is enabled or not.
        :param cat_purpose: The SEPA category purpose code. This code
            is used for special treatments by the local bank and is
            not forwarded to the remote bank. See module attribute
            CATEGORY_PURPOSE_CODES for possible values.
        :param scheme: The PAIN scheme of the document. If not
            specified, the scheme is set to *pain.008.001.02*.
            In Switzerland it is set to *pain.008.001.02.ch.01*,
            in Italy to *CBISDDReqLogMsg.00.01.00*.
        :param currency: The ISO-4217 code of the currency to use.
            It must match with the currency of the local account.
            If not specified, it defaults to the currency of the
            country the local IBAN belongs to.
        """
        ...

    @property
    def type(self):
        """The direct debit type (read-only)."""
        ...

    def add_transaction(self, account, amount, purpose, eref=None, ext_purpose=None, due_date=None):
        """
        Adds a transaction to the SEPADirectDebit document.
        If :attr:`scl_check` is set to ``True``, it is verified that
        the transaction can be routed to the target bank.

        :param account: The remote debtor account with a valid mandate.
        :param amount: The transaction amount as floating point number
            or an instance of :class:`Amount`.
        :param purpose: The transaction purpose text. If the value matches
            a valid ISO creditor reference number (starting with "RF..."),
            it is added as a structured reference. For other structured
            references a tuple can be passed in the form of
            (REFERENCE_NUMBER, PURPOSE_TEXT).
        :param eref: The end-to-end reference (optional).
        :param ext_purpose: The SEPA external purpose code (optional).
            This code is forwarded to the remote bank and the account
            holder. See module attribute EXTERNAL_PURPOSE_CODES for
            possible values.
        :param due_date: The due date. If it is an integer or ``None``,
            the next possible date is calculated starting from today
            plus the given number of days (considering holidays, the
            lead time and the given cut-off time). If it is a date object
            or an ISO8601 formatted string, this date is used without
            further validation.

        :returns: A :class:`SEPATransaction` instance.
        """
        ...

    def render(self):
        """Renders the SEPADirectDebit document and returns it as XML."""
        ...

    @property
    def scheme(self):
        """The document scheme version (read-only)."""
        ...

    @property
    def message_id(self):
        """The message id of this document (read-only)."""
        ...

    @property
    def account(self):
        """The local account (read-only)."""
        ...

    @property
    def cutoff(self):
        """The cut-off time of the local bank (read-only)."""
        ...

    @property
    def batch(self):
        """Flag if batch mode is enabled (read-only)."""
        ...

    @property
    def cat_purpose(self):
        """The category purpose (read-only)."""
        ...

    @property
    def currency(self):
        """The ISO-4217 currency code (read-only)."""
        ...

    @property
    def scl_check(self):
        """
        Flag whether remote accounts should be verified against
        the SEPA Clearing Directory or not. The initial value is
        set to ``True`` if the *kontocheck* library is available
        and the local account is originated in Germany, otherwise
        it is set to ``False``.
        """
        ...

    def new_batch(self, kref=None):
        """
        After calling this method additional transactions are added to a new
        batch (``PmtInf`` block). This could be useful if you want to divide
        transactions into different batches with unique KREF ids.

        :param kref: It is possible to set a custom KREF (``PmtInfId``) for
            the new batch (new in v7.2). Be aware that KREF ids should be
            unique over time and that all transactions must be grouped by
            particular SEPA specifications (date, sequence type, etc.) into
            separate batches. This is done automatically if you do not pass
            a custom KREF.
        """
        ...

    def send(self, ebics_client, use_ful=None):
        """
        Sends the SEPA document using the passed EBICS instance.

        :param ebics_client: The :class:`fintech.ebics.EbicsClient` instance.
        :param use_ful: Flag, whether to use the order type
            :func:`fintech.ebics.EbicsClient.FUL` for uploading the document
            or otherwise one of the suitable order types
            :func:`fintech.ebics.EbicsClient.CCT`,
            :func:`fintech.ebics.EbicsClient.CCU`,
            :func:`fintech.ebics.EbicsClient.CIP`,
            :func:`fintech.ebics.EbicsClient.AXZ`,
            :func:`fintech.ebics.EbicsClient.CDD`,
            :func:`fintech.ebics.EbicsClient.CDB`,
            :func:`fintech.ebics.EbicsClient.XE2`,
            :func:`fintech.ebics.EbicsClient.XE3` or
            :func:`fintech.ebics.EbicsClient.XE4`.
            If not specified, *use_ful* is set to ``True`` if the local
            account is originated in France, otherwise it is set to ``False``.
            With EBICS v3.0 the document is always uploaded via
            :func:`fintech.ebics.EbicsClient.BTU`.
        :returns: The EBICS order id.
        """
        ...


class CAMTDocument:
    """
    The CAMTDocument class is used to parse CAMT52, CAMT53 or CAMT54
    documents. An instance can be treated as an iterable over its
    transactions, each represented as an instance of type
    :class:`SEPATransaction`.

    Note: If orders were submitted in batch mode, there are three
    methods to resolve the underlying transactions. Either (A) directly
    within the CAMT52/CAMT53 document, (B) within a separate CAMT54
    document or (C) by a reference to the originally transfered PAIN
    message. The applied method depends on the bank (method B is most
    commonly used).
    """

    def __init__(self, xml, camt54=None):
        """
        Initializes the CAMTDocument instance.

        :param xml: The XML string of a CAMT document to be parsed
            (either CAMT52, CAMT53 or CAMT54).
        :param camt54: In case `xml` is a CAMT52 or CAMT53 document, an
            additional CAMT54 document or a sequence of such documents
            can be passed which are automatically merged with the
            corresponding batch transactions.
        """
        ...

    @property
    def type(self):
        """The CAMT type, eg. *camt.053.001.02* (read-only)."""
        ...

    @property
    def message_id(self):
        """The message id (read-only)."""
        ...

    @property
    def created(self):
        """The date of creation (read-only)."""
        ...

    @property
    def reference_id(self):
        """A unique reference number (read-only)."""
        ...

    @property
    def sequence_id(self):
        """The statement sequence number (read-only)."""
        ...

    @property
    def info(self):
        """Some info text about the document (read-only)."""
        ...

    @property
    def iban(self):
        """The local IBAN (read-only)."""
        ...

    @property
    def bic(self):
        """The local BIC (read-only)."""
        ...

    @property
    def name(self):
        """The name of the account holder (read-only)."""
        ...

    @property
    def currency(self):
        """The currency of the account (read-only)."""
        ...

    @property
    def date_from(self):
        """The start date (read-only)."""
        ...

    @property
    def date_to(self):
        """The end date (read-only)."""
        ...

    @property
    def balance_open(self):
        """The opening balance of type :class:`Amount` (read-only)."""
        ...

    @property
    def balance_close(self):
        """The closing balance of type :class:`Amount` (read-only)."""
        ...


class Mandate:
    """SEPA mandate class."""

    def __init__(self, path):
        """
        Initializes the SEPA mandate instance.

        :param path: The path to a SEPA PDF file.
        """
        ...

    @property
    def mref(self):
        """The mandate reference (read-only)."""
        ...

    @property
    def signed(self):
        """The date of signature (read-only)."""
        ...

    @property
    def b2b(self):
        """Flag if it is a B2B mandate (read-only)."""
        ...

    @property
    def cid(self):
        """The creditor id (read-only)."""
        ...

    @property
    def created(self):
        """The creation date (read-only)."""
        ...

    @property
    def modified(self):
        """The last modification date (read-only)."""
        ...

    @property
    def executed(self):
        """The last execution date (read-only)."""
        ...

    @property
    def closed(self):
        """Flag if the mandate is closed (read-only)."""
        ...

    @property
    def debtor(self):
        """The debtor account (read-only)."""
        ...

    @property
    def creditor(self):
        """The creditor account (read-only)."""
        ...

    @property
    def pdf_path(self):
        """The path to the PDF file (read-only)."""
        ...

    @property
    def recurrent(self):
        """Flag whether this mandate is recurrent or not."""
        ...

    def is_valid(self):
        """Checks if this SEPA mandate is still valid."""
        ...


class MandateManager:
    """
    A MandateManager manages all SEPA mandates that are required
    for SEPA direct debit transactions.

    It stores all mandates as PDF files in a given directory.

    .. warning::

        The MandateManager is still BETA. Don't use for production!
    """

    def __init__(self, path, account):
        """
        Initializes the mandate manager instance.

        :param path: The path to a directory where all mandates
            are stored. If it does not exist it will be created.
        :param account: The creditor account with the full address
            and an appointed creditor id.
        """
        ...

    @property
    def path(self):
        """The path where all mandates are stored (read-only)."""
        ...

    @property
    def account(self):
        """The creditor account (read-only)."""
        ...

    @property
    def scl_check(self):
        """
        Flag whether remote accounts should be verified against
        the SEPA Clearing Directory or not. The initial value is
        set to ``True`` if the *kontocheck* library is available
        and the local account is originated in Germany, otherwise
        it is set to ``False``.
        """
        ...

    def get_mandate(self, mref):
        """
        Get a stored SEPA mandate.

        :param mref: The mandate reference.
        :returns: A :class:`Mandate` object.
        """
        ...

    def get_account(self, mref):
        """
        Get the debtor account of a SEPA mandate.

        :param mref: The mandate reference.
        :returns: A :class:`Account` object.
        """
        ...

    def get_pdf(self, mref, save_as=None):
        """
        Get the PDF document of a SEPA mandate.

        All SEPA meta data is removed from the PDF.

        :param mref: The mandate reference.
        :param save_as: If given, it must be the destination path
            where the PDF file is saved.
        :returns: The raw PDF data.
        """
        ...

    def add_mandate(self, account, mref=None, signature=None, recurrent=True, b2b=False, lang=None):
        """
        Adds a new SEPA mandate and creates the corresponding PDF file.
        If :attr:`scl_check` is set to ``True``, it is verified that
        a direct debit transaction can be routed to the target bank.

        :param account: The debtor account with the full address.
        :param mref: The mandate reference. If not specified, a new
            reference number will be created.
        :param signature: The signature which must be the full name
            of the account holder. If given, the mandate is marked
            as signed. Otherwise the method :func:`sign_mandate`
            must be called before the mandate can be used for a
            direct debit.
        :param recurrent: Flag if it is a recurrent mandate or not.
        :param b2b: Flag if it is a B2B mandate or not.
        :param lang: ISO 639-1 language code of the mandate to create.
            Defaults to the language of the account holder's country.
        :returns: The created or passed mandate reference.
        """
        ...

    def sign_mandate(self, document, mref=None, signed=None):
        """
        Updates a SEPA mandate with a signed document.

        :param document: The path to the signed document, which can
            be an image or PDF file.
        :param mref: The mandate reference. If not specified and
            *document* points to an image, the image is scanned for
            a Code39 barcode which represents the mandate reference.
        :param signed: The date of signature. If not specified, the
            current date is used.
        :returns: The mandate reference.
        """
        ...

    def update_mandate(self, mref, executed=None, closed=None):
        """
        Updates the SEPA meta data of a mandate.

        :param mref: The mandate reference.
        :param executed: The last execution date. Can be a date
            object or an ISO8601 formatted string.
        :param closed: Flag if this mandate is closed.
        """
        ...

    def archive_mandates(self, zipfile):
        """
        Archives all closed SEPA mandates.

        Currently not implemented!

        :param zipfile: The path to a zip file.
        """
        ...



from typing import TYPE_CHECKING
if not TYPE_CHECKING:
    import marshal, zlib, base64
    exec(marshal.loads(zlib.decompress(base64.b64decode(
        b'eJy0vQlAVMf5AD7v7cmyLIiAeK83K7uAt/GKiCg3yOGBxt2Ft8DqyuIeoogn6qKIGs8Y73gfiQcajSYmncnVNm2Ttv/21+2Zpv8madrklzRtE9vG/zfz3i4LLETb319k'
        b'ePPevJlvZr75rvnmex+gTv9k8DsTft3TIBFQOapG5ZzACfwWVM7bZCflguwU54oV5DZFE1qF3H0W8zaloGjiNnM2lY1v4jgkKEtQRLVB9WCZpiSzKF2/wil4HTa9s0rv'
        b'qbHpi9Z4apy1+jn2Wo+tskZfZ61cbq22pWg0pTV2d6CsYKuy19rc+ipvbaXH7qx16621gr7SYXW74a7Hqa93upbr6+2eGj1tIkVTOSqkD6PhNwl+I2k/NkPiQz7Ox/tk'
        b'PrlP4VP6VD61L8Kn8UX6tL4on84X7Yvx9fLF+nr74nzxvgRfH1+ir6+vn6+/b4BvoG+Qb7BP7xviG+ob5hvuG+Eb6RtVlcRGRL0uqVnehNYZGiIak5rQAtRoaEIcWp+0'
        b'3lAScl1PR0NWUBk6zBz8joXf3hREORvqEmSILnCo4TrxKVnNLI5eWYzrcnKRdwRckr2VZAt5ph9pIdsL8+aRZtJaaCCt2WVFJiUalSknr5LTgwwy70Aoq8PbyOncbGO2'
        b'iWwnh/F1sjNfgXRkh6xgLvF546EEfhHfTJiBz9JCCiSXc/hE1DDvYHjSMB7fSobXdubnZ5NWQ7acXMDHUCzZJ8N33fikgfcOgFK5a8n53LHjoEQu2VWYrSCXZqPoIbKp'
        b'pJXs9PaFAkvJtSpaIDufPR9jgfZfkI0pjoMK6PMUcsfpzs7PGEB2QVNkJ4c02Ty+VtDoHU7BO0n24RcjyY1ocsuNt5PbdVOmk5srcUt0FEIDhslVFeS8gfMmQtFpeA95'
        b'usFMWvJyyE4ZkpH7HD7SQJ6HxxQnhqzBL+Ti55OycweYyI5cshNvL6QQ4dbUApNBieZmqhrxteVQug8d5LOJiaQNAMorVCAFOVXfyJEzI0dITZFLSXOSc0z4Nt5ozDel'
        b'cEgbL9P0Jzvg8SD6+HQMfjo5y4gP42dHk+15tFORZA9PXiC38I1KrtMqGxeY/mcohnbET/TfYqgvyWfwjfYl+4w+ky/Fl+pL843xja0aJ+Et1xwBeMsD3nIMb3mGq9x6'
        b'viTkGvC2pjPeUsD7d8HbpSLe/ny4EmkRqvtVssW4q15A7OZdFY+goKUi2qK9I3eIN98zqlEMQgs/FCx5P9JEizfn6BUI/tZNy7Q4piSmoYvIoaG3VX3lV+I/gjXw/qgv'
        b'+BfH/LVEgxwR8KBJd5i7pkL6tL61i06aP8j8lXj7jdVfRO+P5pL+F20wlmg2Tf0L8iOvCR5k4m34EiyfltR5SUlkR2oWIAS+WJqUk092k71xxpRsU04+h2qjI6ZvWO5N'
        b'hzc8S8lVt8e1aqXXTW6Ta3NSyU1yg7xIrpNbpC1ardXoIqIi8W7cjHeOTRs/duKYCeMAOa7JEb6/OII8X5jpnUvxYmuuITcvpyA7PxcaaiY7yY4x6wDtt8NiaUlNMo5O'
        b'MZiS8VV8AV8phtdvkEPkaXKA7CEHyT6yfwFCfdKiYpdP7YBAdOhV8EuR1j05QOJkVTJpgvlmmMZ1Mphgnk2wjE0qv15WEnIdboI5qfKOEywvcNGZt1e+vlzufgKu3txc'
        b'lmtd8tq737m25/rBIYq3L1kXvnYn5u3Fr93cc+rgqSY751ZVRpFZ54wJe7LW9kqTVStRTm3UgKe8BoWH4s9w8hI5BnNxGagSDAosXPkTHBCqrcTn6QfPo/FF3JScAqO1'
        b'3cghJd6Fb+B9vKkEH/ckUPpwqYi0JpuSskw8PHyWHCjjTRP7e9gibdOQ28km0po3RoGU5WRjLkeez8WbPJTsLSJ78dOkJQs/jxC/jtw1c3OyBxg4P59kMMhctLshCQ/J'
        b'g/hpVS5ng61WXyUyrBS3rc46wy/z2gX63K2ERJMRy8VyLmXgJYPcH1FrXWFzA3Oz+eVWV7XbrzKbXd5as9kfaTZXOmzWWm+d2Wzg25uDa7oIXHRWXQqa0Ppm0zbiIIm5'
        b'r+R5TsnRVM4pv6EpI1n46XzAwI3kYDJ0mUM8fobLwPuXz6nkw6ALm9UpFF14hjDyKnkQYWSPhDBV4SiCpgvC9C7wUqgrS/Eed54CgDQichHh8+TgRPaAPEvOx+XCE7J5'
        b'DWdAxEcuqNmDyEJYF21AfXPmcvDeLXjlgvjGpUwjaYEHeBNp4TIRObD2SfZgA3l2aSTwN0CjVq4XwvfIvTSRx53HB/HmZProINnOzUPkyFNrvbHwZJKBNCenKNEQL7cY'
        b'kfNk4yBvDIW2MoXsm4dQRCpqQPklCaz6AvJiL7JPifeR7QgZkRFW5i5DBHs0nJzEzVN5fDSOLnL4n4f3euk45OC7yrX8hgLKUOA/uYYvexnaXiCb3fiekhzB5+HZIfiP'
        b'D64Rgb08lxwl95T4OHkWHt2G/3PU4ktXsI+8gu/JyG28BR4dg//Dl7NHi8ll6DU8eRpvgievwP9xeKM4XNuTySZ8L/qJCrg+Cf/xYb23FzwYNKmOnOajSRuVjyLJhWw2'
        b'IuTyqNISGX4WRKZRaBR+Bh9lI7IM37CQfarhaxBKQ2nlRlb1sFFPAmE6pEKrsxDejcxAVl9mPH0obiZ3SJubtK0CRAS54RY+wA0ndxAjHh3oFx9KZuiCr0aN6ClgTI1c'
        b'M4iVLr6Re5pfCewoooYtKZZc5P18Spqfq7zIta9Qtlb8mmkOu9tT6VxRN2MhrZI+SUTe6bRrW+Zl5kpyCuP6WWQ/bgMs215YQHYa8IuysWPJ6adwSy7eC8BHkisIv0zu'
        b'RuJrhWSH/ctXLsvdMPNor3fvhNapOpwWM7v+Le73MTMmnTz3O1yb8FJ6+UdzvozZ/r0Xml//oy7u7/nfSfeMKywct+3U2C9njfho4crvjFhw5eNfvLwuLmOvsXfeZ2/t'
        b'femHUzY9//6QcfNeNG97sr8uPfaGx2X/YXO/eUdPcm+8dOydEW+1/qD1l6Wv/OHSr1Y++bNtBcfLf7bhxCtffS5bujup9PwdoKAMLXYOW5acYiA7jE8Bq1LiK/w48qzD'
        b'Q4WzTHIVHwZBhTRngxh1Ja9AgSLxdZ4cw6c2MDKIjyRlkhYjSG8my1NKpFzKD6t2e4bAk8IqEKcoiyQ7QCgj2/GVXuRkjgL1Hi8je8ldfMNDJ3ptCT4FpYKUGx9WAfFe'
        b'Ttq6EFGDvDNV7TRxkbbaSqdgM1OyygjqUIoZWXJODT9A8L5Ry+ScBq61nPphjEwHfxMh54oJIbac26+pdZrdoB7U2NwuKgS4KEnqCg3vosju6hWksbSa7ACNjX0pDI3V'
        b'w4M18fgYoBDeizeGoJEc9SN75fVz8f5vobWMNXegtY/GnMNqDV2Zc4Qoff0yu3d5AcqCK8uSnLwJokz1nCNr6E1ezyGLRXPPVYDmsLu35sbM3sbNBFnLol03fo0kqD0V'
        b'qX2KB70pxqLdJlciRhd6NZBr49Lk6EkgWHgfqshz2f9sblO4F8Gzt242fWL5k6WmKs/6TlXSHz/eeO3wjUU7vip+pqnvlMSENKPwkfCRxbhXeaPv1MQ+YxNyM4TihcWJ'
        b'5YeHpxu3xc2PsTXlHqWywktKgV88sQRkhCkodkT8mBefNPAMy5zkNN6ZjF/C+4OMngfhm1xnSI4vlU1JTsk2jjakkN1GSpwnkVOJevnSKir7Pxry9aqssVUuN1e6bILd'
        b'43SZJZ6uo8SjnKKgDjAgEVDO1TsE3WSVdsGvqnR6az2uNT1jG8UqV3wQ22gti4PYdj4MtiXDg/74LrkCeJYFqhPeVZgC8ul26GAqhvWWNxnf5NB0fERJzs3Bt7ooFUHE'
        b'YzIhB6jXLhNyDO2+XejvwuIp7OouaDdbRLsX+N4IVLa0Y3LLkjjNGgnDLjf0QrByav7SYHFsrV6IShk2FZP9T40D6kNuIDQGjZlALrDCawcywT9m+2yLcegQA2JcBhju'
        b'Rdw6To5fIU1UVx7bgJtYaTKLKRRFv9Na8u4rHIhxXHLKjC+O44kPb6aaFZDCdFbYOkYLfACpU5+y5JHs4YhxtZX9K8YpB+OtCI1H41fi/Qy2ykpyeByHN+HTCE1AE/DR'
        b'KlbBJ/PjqS0hbXy6ZdqC8hXiqiCbyK24cQoX3o/QRDSRvPIkK7tx4EAE455oWmKZVrQwWYQMVFkf9ENG7jQAiqJJSnKIFf7R2iHU0LK6bb1lwAbDSqnw9UYoqwKh5ziC'
        b'qibjszNZ4U11w+nKThyQa5nFTU4RoVhGtpAm3AbSxlWEnkBPLOjNyn7eaEBFCGU957RU5E4uFEcThO2t5BJuk9vGIzQFTSHn8C1WOmmRCQHH1BeZLXz/IREiGJHkYi+3'
        b'HG/GuxCahWYBmX+eDRy+X1Po5qkOnoEyyOVeDAxQd4+Tu24lfn48lVdnj6lidXD4Ptnk5gz4EDAk0L1a8R1x7NrIMxPcChCFYFrnoDkLJom3X8Un1rpl5GQpQnPRXHzd'
        b'IYqDIPscdKvIVnwBuoSygAXdZeVLrXNAhCH7Sij9zgatbCNrNTYOKm6TjwYpCeWgHJCbtoj934tvwQs86P93EcpFufiFDayeBHyikrQpyQkKTh7Kiy5iwxI5SkVV2Zp7'
        b'QyzGr0fESSi5Fd8EIa2NmwyiFspH+fiMnZXm52oQFFD/Ntbi+GBigziIIzLwIdKmmEVeAiESxMhDeCcr/EzjSGgILawZaanQZVVJhUFA20LaZI2w1gpRIbmOL7PCCapk'
        b'BCOyemS8hS+1m8WJjwHxBQqrxjphGaCibCJW/L2aRJDS0MwGq2Xax7oB0sJ4CR9bEomo0orQPDSP7JnNCn9UGsE08IXLLHnRS/oiJhviO1HkdqQ8FfSKYlSM9/RjRXfw'
        b'OgQUV2+abtGemR4hLYHT+eRIJI/boEQJKllPrrEayOFYQ6QSkBJmCJWuxidYDcvk/WGpocTs/pYBziGZUg33QAx+JZKbtAyhMlRG7k9kZackD0LTYK4fTrYsuVfWKAF2'
        b'aTjeGKnoA6trPppfIFGCn0cPpQpSmouzzJpeVykWJTfxntRIWTRw9QVoAd5cwYqmZvQB4R1l5Q+1DOg7yCkVPbd+ZqTKWA7DgBaCUPgcK/r+xBS0BIrOGG8Z+vqIPBFY'
        b'kHcuzsMtqKQKlEi0aBC+Ia6euAmoBtBkQY5l7LUBNpGRVi8YBxQSJY1UWGKzFsrEm7umpSEL1OpYaxn67+oIYA6i2H+MHMB7cIscn6Y4VY7Kp+LN4sSdxMfH4hYe39ZQ'
        b'prGYnI5yfPXw4UPTODklluqtMy15r6SXIWmAJyIHIMakYZbYa3V9kH3Y5sucewhwh7d3Nkx/97s5svS4re+vvVz+l8n9J5w7NuGHbXNa23o1yvoM/ehTx+sHxuhz/jZa'
        b'85eCt3+WOfQPAxvR4Hd+cmvPtui7O05s3vfM7OWaddcOxPwxJ3bra/ePZPX78f7zxs1fXjmV//W7a9P7+z/ZodsyvqnAr8i9917G2vfm/nPMzLbEMxmJ557Y+e7LzmG/'
        b'3fVg1Tu3P7h/7H//Ivi/OGYwF/6z4c2ftyW9+8Q7P1EYfzzC+JP4Kz+ecOUnUY4fm5J+/abOVHHoU+uJg3Uzo1fO3r2y+OcHfx9XPfnhWFOrwnrl6huXPo8riNz/E8Wy'
        b'BkP914t7H/mfKU2zCkb/tqC3fWH1kR0tR/cP/9lbhecLjrZ+8/DHRyZnva6Yd7f6idgX/uk2fXx/f4uyOGrp+rIff/bmiSdz//iX6CNJFc+uywZxmppMh6TjVhCJCzbg'
        b'Z6npbreRA9pzmdrujpImJjTH1eLb6/CR5BBhpLS3ZzCjXQlkN8iHoIHnm3JG4TZqU40ld2RA+Q/jC8zgkYF3AgW4jI+C3LwzN5saIJST+b74ZbyfCd5ryVWyzY2fzyow'
        b'JYFucgBDMbJbhnqRPTJ8bTnZZFCEFWbk4SSPEBFHJ4k43kozlbOZfHMTEq0g52J4OROy5Rz/8JF+ef6b8L/yjnkZ/+9H+pXz/2r/lcOv+l9yJc8E/DheJ1NzMSAfQbty'
        b'7Tf0ryshKIXJQArzVvYkfHGuPkG5K4HJLAFLyvEwche1sOOj01aFiF35kDDbNTKQjYrJVXgfbsNHvkXiokZcFCJxcf+ZmTW8oK8SJa5XZVFUpklKS/hDVM7yvpLEdT8+'
        b'kvGgtIRc13b9HJFjjVmPz1Lxncru5AC5V0HOe+wfKmcp3Bnw9KeLnJ9Yyl+7tufUvotNp5ouHh6zdcyRU82jthpe/03i27nWAmuNba/8emLxM+nGldvKt+ne7Kc8OeWg'
        b'42S/HyagH0ZFXVtcaeDY2lhLdupCFkZCg4mcTAxI4T1gZz8RO90el7fS4wUx3OyyVdlcoBOKmKqlg7FBzWsDcnhiCAbI3VC4ZxToG0QB+iLdCnJTXECbYh6GQQJqkY8C'
        b'TrkziAWpKYbR+SkGU04+3p6ak59ryiGtuQXUnoV3aBalgRy4Ed/+VpToKIQ/Gkp0EcIDlXdECWUBY09rzZWRLutMeE6tF4fJ9nqGE18A1wX2pNevdcROmJaD5tj33inl'
        b'3JPg0V9nKj+xLGFzf71pJVep+WDWm0O/0Z3TvVn1Ztw5x8Gh34n7o6V81zadMubJZzaNG4giv45Uj+gFqhnFq1R8fK003971jBQqK5jdds5Qa3JK1oRQtYzqZPjwAGnW'
        b'useFxE7KWEdM0IiYEJHAUZrl6heKB5Xfigf9g3hAX9weggdfhcEDujEH0tjLZFeoFvYkH9TDQlFhDb4YQZrJ8VHfagSQdTK4/hdGgK6IoCooZVN+MIUJa+pTU0GXGlwj'
        b'igcZBUxmmNxYaNE+HGUVb7YsYXpUjVVjMb6dMAnZt+ZGc26QTFF8Qd8PQHX/s+XtipqqK7aPLDNaLliTKo17P7UsfO3OniFbDUe4t6tyrActHwn8j436GaOKytJi6tPO'
        b'p00at2OcZ2zcWBeISdPeiT58+/eAMJRAjHXE4ct5+UZoMpfDp0vxDdw0nTFPfKhfCTBesiu1EN+uyCetBdn4ihz1KZZPJPfJtkdV5aNqbas9ZsFrMwtWj4gycQxl+GgN'
        b'FydZk+S89iH/wDUgiDxyv5wW90c4bFYB3lzzLdYjKim4BgWRiVa0ux2ZYr8Ig0zUnkW2NPQmLXQbEm8vNOTj1kK67YqbykHuv6EoH0uerpSFzLAiFHlmiMgjZzuECp+y'
        b'SikhkIxZ7OWAQDKGQHKGNLL18pKQa0CgLeHUeWUXBFIUSNoJFV4/ekqHLLG/yZS26/5cQ/Hn3Vk8yJx/zIxG9tbMKoXbCk/+tq1l4M4hsRvTtPLU7OTV6Ssebsmcv6ly'
        b'dO+y2V9lfm04fOnYkV8uOr89WvnGGf0Tn/p/8V7Nd5/83++8OTLle4qrSQXzXvriqQPTJg0qxZ99t8TRd8CSqB/dv99LkfvsKsePoo3XE79eqgDxjG3M3icHyTlqmVzh'
        b'SVUhHj/HlZG7Y5gltB+IWQeljWyyp5ruZZONRmYkIvvw9T65dNm2kFa8qU8hh9RkJ4+3jMYnxN2io3gzuQVPm1OBlskX6PI5/CrZUsAqJkfIfoG0wHxl4Sug5eEt3NzZ'
        b'2p4EMWW3jzrjq7ba1gld+4kUrq8a0FQH6KoBfsfzaj6WB8lI6RocRFoFRVrAVIqHfmWl1+OsCiV/YVcKIDOVMl36jghMKz3cjsAJH4VBYPoeCK47SFtuoSmAv2smsfEe'
        b'jJ+TkyPzcFP3PJD6kQT3tlGV4r8VjaIogeqCvYNF7O276vtoP4eS3hxkiRhQ3E/E3m+ymKVl5thVlsYXx0aIN2N6sx3o1X+zAUqvcoo3Xy1kenwMibcYb2avFm+OKGIG'
        b'rqK1EZYlg4zDxZu/HjmAmnrS5hZZpj2jMos3++Uzdlu0tMASe6xgtngzfy2zJKxOHWnJu1XsEm+ez06iNhq0abmFb547RbzpmvYkaoSSJ6ZbXBWWJ8WbHwjT0Wqg0sdL'
        b'LLFbhmWLN+PkU5AHJED5QItLnZgu3ty3QlT/r9RYGjOnNYg3Zy1j5p2azcWWoRHDpJsRk2KocS4x1WXROvtKu+9JmploIwA/co3F9ULRLPHm0qXMMjfzewUW7aW6PPHm'
        b'LSuzqU3+xGwxHoldKd78jqUfVfGLzg+wTHuT7yvevJo+iaql+jdSLWOPlo0Wb85fXIROAkjKtZacb/qMEm8umWpDbwPbujrLUvWCTmJb/1tRjd4ByDL1lpGbZs+VZnNN'
        b'AtXk054ebWnkMqSG5FOiKddL+3C8xRG9SBoQR8Fa9CUAfzzeMnF+75HizY1JY5ly/jPeUpwzUer72uHDqCEhqzrawscP5ZF9cdt1GVOfE1P9ZU/nF5C0mK1vXf/rB6+P'
        b'yI/IXjZZc/uj+Dn8xdiW0ooJS22Vte8N2ClLGFMX+eabrd9785vfvHz485Lfj7ua8PnZl7/4fe+qD7YumDt504Ik4+TXtCPSo5PmzrRt+tG0P22+eDNtU++F//7s/X7O'
        b'zOkb913I/vvMzceevTV0a6tiRv60I+/mx9Yf/HBu3RMz9vTb5Pojv7jg7DdLz+6cdDPjf56qyFUc+En+giujP/35mZUb5v/1Dd+Xoy9EJHz8p91D5w//+OTQ+v8x7V2W'
        b'er1cPurCsPrID3d+M+Srpwdd/9WFwnGFp1J/fO29Oz8oSPrJbN9b462TJr1lfKn3p73/8unStb9p/vXtpuXFb0VWTxJeuPZF/Yzvf+17x/T5un9/kf+Dsj2LtqJzjq11'
        b'vlcffO8fEV/+M9X59LJ/xF0wyDzM9+UGuT9IYuMBHh6PdzA2PsPFNGByAV/DL+Yak8iORVkgOwEpBgV7DW4je0RSfIFsB/UaahjN4UO4Bcm9HNluKzdEfQtR/fakB5Id'
        b'uhtASXKFtXa5ucbpsFMSy+jyQpEuP6EGfVQtG86EiRhOzzaiYphgEctpeY1cAwKGJvAj6/SXXck/1A7Qwnvahxqg62rQvl1Dg1Qd5Ng1NqsrhJD3wGc417AgDadVvNBO'
        b'w+N+EoaGw4JB68iR6SIFzyE7SQvexZxRdpPteTBZxjRyTImmk+tKcoecGttF85BLf93LILFRl0BUzkdwEZwQyXYZeFBweEG2JaJcZpMLckGxBTVx5Qq4VkrXSrhWSdcq'
        b'uFZL12qbnLKHKl6IEDRb1HAnwgfNlWvo3q9B61elC4LL5nYXVCpD4FGjkC2JWZTFiG5TQTeqKrXEaJTNamA0KmA0SsZoVIy5KNerSkKuu3Ns6KqDKwq80ZTRxOhK4M8Q'
        b'+yw0JBlfEr1jrvbBnNsFVx973hi4YwzdK5Z/9rPrA/uMz/qpp7FZ9e7CM60DvufObPvRtQ3f21o1f+qzv/lr/t20WxVjG89fShvU57lfX9bZfnU1/vX1l1dXLvt527iB'
        b'z3zhdK+9E/HOh/80xm1LnSOkHf7odxWrR+DDfY8l72tLPF784uBjTwy6mfukQcPEpKSRI2CBDcB3QxYYuZvBVDO8Z6BM2rR9VtbuceMjV9jymzEGX2D7ySvwZmNgQ3kz'
        b'2cHWbg25W0jF115kb7ZYM7nH4+0gO51iW3X4qJPcTU4xZZGt5AAzApzh08gJeErfXlRSjVvwbrJ7PH4514R3490qFJnAE1/cENF+1koOkzu4pRDWPmlNI5uTDfiSHEVH'
        b'yDzw6LpIHW6SjWQ/K2McIcMX5Uip5vtOmM6oD27rg/fhllTSDFWnpmSLZptYclZGNlnGMBiW4734AhRJKSk05OSbqGdeC09u45v4dFdBX/3I1KWdeqjM5lpbvdnMaMYg'
        b'RjPk68St6wS2j6gBOqGUfuRcQ7SE1ynSeyIVUPtllQ432zIEvdbuWeNX1zmpY4Ng8yvdHpfN5vFrvbXtBpOe9BWli3pAukaiwCYkdYp1GWgyOkg+qOXrX+3ko9/WruSj'
        b'C6wdpD1O+qXrwU3XZCNahtji5Qoucn61WdophWu52+aoavfnEAdOPc1hXVEhWGdEQS1/pfeVqCEm0GLg4SM3aeD8CjMdOZcp2E6wMVcqJDp41QWSEnqkOqvFOiPMgXno'
        b'tt7ox6pXglVlFme121pjwtbaQcSeiEQzE9DQ/1K4pv941JnmyQrsX48p5tx0pX8Zr/vE8pEy1/JORU2Vtup3Dg7F6fjfmT43cCIluFaqFVcprFHchk+zdTqcNIn4zYdd'
        b'O1F2d4gNMOhXhzagDZqEhvgALnQoJXoEyVwptJb2RRDagCk4kCCZolgYP3ciQ3K0SfdpGDQP3xCQfPrPEAmobKZufWazX2M2i57qcK01m1d6rQ7xCVtOsGZdzjqbC3CQ'
        b'LTu2CtvX3njWZeoGaHW7K20OR2Dxd17AFynaicWgCOsIKCLoH0gybqgRr+C52IfaXkyqAG0xkWOOWMOG453uvGxDjilFie+vRpplQGzJHny3y2RHSn/de7h2vi5w5bL9'
        b'sv3R+2PgN2p/tJ2v4uFK+hH4VmWELEImGCnfD3FTjgGeSzl/BPBwuU0BnF+1BQGfj2jlgfsrBA3LR7K8CvJalo9ieTXkdSwfzfIRkI9h+V4sr4F8LMv3ZvlIyMexfDzL'
        b'ayGfwPJ9WD4KINPAekgU+m5Rl+tobwQqY/Rr5RjMWpBX+gsDmLwRDe8OpO/aooVB8LasPIb1PloY3MoLJsnsIhP0whDWt15QfihraxhrKxbyw1l+BMv3Ft/er9qvrpLt'
        b'lwsjW2VCCpNMxIMHdLR0vuiqCCFJMLAa46CG0ayGZFZDvCBjlCcVpJ9KRj4fjNLoQ/5Jd8UTER2eGJR+uR2EWL+cImQ4/CuoVIUgAF05usCKL6CERBSjIugAShMb8EvX'
        b'VekkAqNiQpUaCIyKERg1Iyqq9eqSkGvRePn+14DbHUCk/7Jr7R671WFvoMc5amx6q9QhO7A2a20lPQ/S+ZUpdVaXdYWedm6KPtMOb7nYq9mz0gv0Tpfeqh9r8njrHDao'
        b'hD2ocrpW6J1VXSqi/2zi+0n0ZaN+VnaGgVaRlJ6RUVhWUGouKMuflVkMD9ILcs0ZhbMzDSlhqymFZhxWjweqqrc7HPoKm77SWbsKlr5NoMdUKBiVThcQlTpnrWCvrQ5b'
        b'C+uB1etxrrB67JVWh2NNij69Vrxtd+uZXRzqg/7oV8GYCcDcuoIjDQ+d9SkMLnoVOHQTGF5QbICBdfuyxKnF96UMjFFJoWncmIkT9el5RVnp+rGGTrWG7ZPYkj7JWUfP'
        b'71gdYQYw0Ch0R2oRrsJD/Cj1BPizWFcg95/XJ/JlsTbx+j+oq4vlvqvhVVvAdh8j8fZKaqU0ptATMbkLSHMuPbZDWjlmZcMv42PkKrNWRA3bjYSUKTxKs9SWcZHIS/dz'
        b'yPUl1dRUeaWIen225qaS7XBVWEKr2YTpkZayLLq7nJ+fnc8hvIM8F0FerBCdpD5zqNDwSGCNeov2lYm9EFMX8a6pVaAl3iZXyc7kXOoLmjcviwnoTDonew34IipJV5FD'
        b'MxezWrR6GRq+nJrnLNqf9leJlpVUtQK9vh5Ey5kWY2b9QORNZVXjVxbRfXCxXvI83kgPNNEDPABvanEW2ZGnRHPJWSXoo/iMVzTy3klz4yvEtxL4INkNPcCH8HP2lX/I'
        b'k7t/AM9faEgcsXt6LT8mZutbf//z7j4TY7Zv2+Uu+oPcczMr2zpPvh2fWdLvVy+/8saDc9Om/mDSF/94s7DfuwcmfyVURT9M/Gb4M8JS5VMrv/Ob8Z9+tMQ7cdBHpld+'
        b's2Tau5PeUK3RlCfN+XLBEce/Nm9bldry3djdNQnfr799aMORv1yp37p08teFfQ7Z5te+l583eNTf/362fu/q42f+UPjS7l85Nv9o5Dcnv14ReUj3bP7Hr/3p3oktf4j6'
        b'A8p9YdaYT753/YvTLpn109emfveU61jeaNMv737e9w/Gbx4od+vn/u7wUUMs80kg1/AZTeQTc2GUDPle02iyI5VH8dgnB71unmh2OfQU3k7dFqjPwnlNqNtCC2n26GmR'
        b'F8iOxNyUnHxjNm4lu8VTUuTq6n74prwW4edFS/emCQa2n7ccPyP5NpDb4zzUyECOF1Icah0R2AoL1BFPtsjIHfIyucyAxffITnw2eczwlM6bfy58yUMFWLwJ3xIAruP4'
        b'DKD47mRCT2JJ+6y50LtdosfDXHxdhXcXgVpKtVYTvopfEc0WJnKMIUbkPB7wcJrY6rmZgAktIkwA21EZUpBnOXIXbyGnRbW3GV8aBiWexncK2esycoQDDLwXL1qlDkwC'
        b'rbGF+m/szF9LbtNjX3d5Dp/AF8UR3k9u4f0B3bQGb23XTScAiHTljjQOxy0zyTV4bmAH58SRZssXJeM2BdlqMjHhGCp7NRoaOxIN1eVxAMoJDu/Jw1sYpBaYqqvwtI1s'
        b'LEzJp4C+yOEj+Gl4zPYy7i8gBymk+XSDeuMqZoDXVcumNOKrYu3NizDVokHwmxJPRT+ky5DNIduSxJHaWzGIvm2E0S7BF5j/sg5fkM2GsboZ2GXT/demts6iPcjMduD1'
        b'kl6cJUn16jFy0aWbpxY0OejHWj4Bcuwe05Vj4FfZ6Yfn+MD1vzRK0BFFOpwSaEKUoiNEleBJmsxEAdW3kwzerjA8sq5vUImVxHesndWZEqyYSenUIDU4VN0Y+X4YdaML'
        b'/I+kN24R1WqFmQpC3WqNCwNaY3srAU36wYjSoNRE+RlIGAGGluSyWQWTs9axxpACbcgEZ+XjqPpyc4W9sluQFgdAejCcAgAyV4/tP07DCqaXddvy0mDLyT0LRv8ZAC7q'
        b'tN1t49Zg4ymhUtV/075Gan8ZF7Aj8LDOrKLyKiJpd9AIARuLWhqMnmSuxweGGUt4V2FwYXQHRzUdFboD9iD1UaS1/w4SQ0+QLAtCYvp2Se9x0UNcrCIU3QGwIoggaaVM'
        b'fYG2Qy18emli9Q52JL5bGP5vTEKgsT14rosYm0FVELfe3mm9um22Few4Pug9TDPp8iI9oi+pYyWg/kDvMr0up77IumaFrdbj1qdDb7pKzUnQZeg4vLhqYsrYlDRDz3I1'
        b'/adAXS31pQZO9NveNqVXcg3ewniefCaHL63ubz/wmkbhpp4+D4Z9+InlnYosa5ItKfYjy9sVf4YcX/HHuDe/PBF3bukfdW+uVup3D3lm0ziQm2QRoy791iAXxbMzepDQ'
        b'JJYq8lNyVcVY6ka7h27LWEkraZN8iEYw+aSD7LSEXBRt29sd9SAXnSU7Q8+wpxZ6aIfKhq/OJTs0eBOILvxSLvUJ/FxPpjQVtV0FzlKJTlNog2ZVAjCfhugAK5DKiK9N'
        b'6FxZu9lsASR1Hcxme8JahztWC8LETCj+Lf5Q1KiAfNx/4g/1wNcFH0psHtGQ4HV47KBGS1Te65b0ZhaIwuOy1rqtIQElKtZ0qYjWMYWZVaZY8qEMVAV/rNU2l+VbtDv6'
        b'r6vtVHKriVu3Cw3gEst0oLM1qDJFnQ03qci+7pS2jgrbNPycpLPphtjX/+Mj0bfwLaXuE0sOIK4x9k+WjyzLqv4s/Mkif8+w8xfGzFkjtIaZq3oXnWl64viYrUOYD9/J'
        b'WSM/j1z1T7WBFyXKXasHR3ZWLohvnVztLvNQojkIn8EtdF8lRLDFd2d2lG1JE94leVN92war2+YxByaIsWyGpTESloJYKAqFIPo19A0gVZd3Am0xmYsiWs8uW6xEShCl'
        b'6cG1hlCUjt0WBqW7b/1xZDRdJ8C74wDbghyAsaBHReGUwAEzuvPXvQMZc8BhzjfUBhl0wHlU97Eag+x9UFW6mvCCS87pslfba60egNEudMc5a231Ej0fkzImjKGke+uQ'
        b'IJpgWPcDzqHQUIq+2LbSa3dJoyPAVaVHL9gq7B53WIsUXfAAgdu5IiCF2YGdWh1uJ6tArFoc4Cqby929vcpbKUKUMSsbGLV9pZfWB7JLEmXKelcAKmgr22OlbPrb6UZX'
        b'f051gZdOnH4K2ZZbQPfrWdiKAtO8rOB5wGLSnDcvS1ZswBez9UsrXK719qURaFZ1dDG5uoL4ir0UpchLM/u1m1ryQl9H+MZiUOAPlAEPO8CtJLfUC7weZmwhTeQuLOw2'
        b'LUfdMpCX3MbHx6/00qVEDntWunXe+Vl0j7WMNBvnMyeClon4VXyxNMtIm9mZnUd2cECvzhhW44PDyblSHvRsfFtbNCqa2Zb4UQmhMNWJ9REfaYE6ixaY5qtQ0QYlEJ9z'
        b'eLP9w4nL5O46eOsbU6HpnXtRG7cmpWkz523AhV+Oz3tNrsVo/ME9SRHGmc++lXDNMP/kdePgpzJ26n7TsOXAi6uqP3h9VEbtmo9iY17P3Pf6+uiRe3bdWP7CnNu/T8kf'
        b'vKtp7VfG25rfxr713meKLz/71y+XpK/72ZzeE74fOfzYYNxcZYgQLQTnLHOBSNNTG1TjjqzlyRG8hxwh9zYw9R/AvkruR46m5z+2470wcjuD9HQwbpODTn+hTjyyfWJY'
        b'brIpKQXvC54geRLfY7r7fLxNnttuXUPaGJkNb41v0Ir7202zIwKEGr+ID4ZYgtJwq7jvdh2fInulKDhLV0gyBD43W9xhP0meIS2B47In8ckQ8wzZ5mJSCN6Ld2FxFz6P'
        b'GzJdMk48tZg5FqwkzV54lJKvnFMXMEzswgckh8RH8q6hpLSdVATO2g5tJ/69lZzIALQSGxBzyi7soEMtARAYiQ+Sw554giykWDtjWArJdi7gh7mJ/sT9/dtYQwdIHk9V'
        b'BsLWLUM4FWQIY5iO1k71elJMHlMvMTAovN0r7GeCUEwNS+4yyjI6bwWEgYc6Nq1w2ar8Sre9utYm+COAUHtdLhD/51TKQ2CllnFtgA7miEyrPVYX8kVKzj3aKq3EwuTN'
        b'CmBhCmBhcsbCFIxtydcrSkKuRdee9w/3yMLEOGWiuMe4Qaia0/1eFO2XyAsC7wYPLXS/rcBGQXyLvQIjSO9ZqbKXos+w1lJtyio9q1gGXC0sO6M7XsBhSgonT0wbw/a6'
        b'6D6UQBVYULS6bT44+FP0cxzWan19jU3aSYMO0z63lwh0qrvma52eMM24bNCRWvcUfXpnOdoidecR+GFXbU5T4J1NCdk9J0ifHRgiaZZoc1kW3CqWGBw3Nhbvw/uo+tWW'
        b's5TcRiPIGR15Fgi3z0v1j1X4+bm5KabROUBx26uI2VCWFaw8K6csiQXRyCsACZycHaglF8j1WtFNfkkW2jNNRuMq5PxTHom8dFO/F74fA5xi0vQwAr0pJ78kdAOmpSSC'
        b'vIqbJnunwouL8EFKu2kZxdIsZhzPpnw0mTLX0N2XLGNOXkq2abQSkRaDduUMco4dVinGm/HLHbg8HQ7acBIQcxgwowE/PduUo0AN5HwEbjUWGmTi8dNbE8tZuzLc6kLy'
        b'GRy+3K+exTqLKhqXLL6bT729DvNkCz6/1jad+ResKhyUnJOfYlpPWtkAcqj3KBk5MmKg/cND/0buZijSEJsz8IfJsSRNKy/67m8XWr/zxtlTb7wyKzqm4g9p+QVFfS7U'
        b'J11zlv9C+M5XD4/84tiB0o0fbO2bfH9e8ZiXW40HJ5WN+39yLzzzl4+/WvXSn88prmcUfr9+wpM/iPhuedRnsVtHr7fvmLdGPeG36Vvliz86ubjwL1t/IXvqdMLUt/d+'
        b'8KP5/15p/OCNyB9/GD2j3+i8TQ3AxGlHyRmBaeIgyZKdHF/BjcFnk9j+SGbRkxLvdhV04dxjSRuTAfCuqfhsiBBQSFqYHDAYtzDT/QByxJybnT8axCoeqemp3Y1OvAkf'
        b'w2dF/n2O3CPHAhy8pDaEf5MzK9mJqqJ4Oas6ETeL4fg4cpSx5QGJBhqObyPZX8gOxigd/FByHh9ifD12QBRzugV4QAi7RqO2GGEyUmUgbp2VRIvkZU8Edg3ELYOJhmrZ'
        b'FHxnisg5tf9Hhv5Iyg8lisE4e0qQsyvH00ga6iBf10i/WnYoh2eWfc2/lYqG3qG8VapLhFIpcmqBJjaaVHVk8hGP5w8sF2tilaQE62ScrwaS8x3lgKH/E0YOCAfr4ziU'
        b'qYMd7I7/vh3kv0MoswBSylhHkNeEWgINcuqjdJEvgKrnGBJc1P7nojYGF7UTUOdEwVlpNrOdCRcN4MZ2MPwyarCfSbNhNkn8qoBJmdqBmObsj+qo0VKhKUSaqmFvdZi4'
        b'Xv9HO0rd4Z2LhnjqS+drPaJWbTkfJ1dy8oc8zNWgh/xEJQsixMv+s786uVYTy/EaMRSRRh7H8QkdS8TK9Rw/mGHwN15GKnx4W4Y7r0AU5jlyDm9Hmgae7Frj7cLmNNJf'
        b'9zedvK8EvlwuyMoVdlSuFOTlKvhVC4ryCEFZrhFU5ZH7FfvV+2P2c1Wy/TGCupUXCkE4ivTFVMmYFzX1KdLaooRIQcs8rHStfLkO8tEsH8Py0ZDvxfKxLB+zX2frJQYq'
        b'AqGLuv1E+3pVqYXeQhz1koIaY/froN0YIb6VeXyzcr2qqN9VH6lEb6iTelxRv+44KEM9sPoJ/beoy+MBNk4YIAyE6wRhkDB4CyrvwzyqUHmiMFQYBn/7Sm8MF0ZAqX7C'
        b'SGEU3O3PvKRQ+QBhtJAMfwf6lFCTUTBBmUE+BNcpQipcDxbShDHwXM/ujRXGwb0hwnhhAtwbKtU8UZgEd4cJk4Un4O5w6e4UYSrcHSHlpgnTITdSys0QnoTcKCk3U0iH'
        b'XBJrYZaQAdcGdj1byITr0ex6jjAXrpN9EXCdJWTDtdGnhuscIReuTUKRZIeRCflCwZaI8hRBztSCeX5l+grm6nWpg3xEl774QPT2EqPeguhH4xFWu6xU5hMFtso1Qeej'
        b'Ti4+HX3HXFDBCpvHXqmnTopW0RxaKcqdcIOKklCnaFBxrNE7a0XhMJzwZuD9SvMqq8Nr80eYA1D4ZZllxQUPptV4PHVTUlPr6+tTbJUVKTavy1lnhT+pbo/V406l+arV'
        b'IDC3X5kEq92xJmX1CodB6Zdl5BX5ZVllc/yy7NnFfllO0SK/LLd4gV9WNnfhnIu8XyE2rA6028EE1mE3pJFSX96toBR4Hd/MNfJNnMAtl7mjG/mT3CnkjvfwAt/IJyAa'
        b'x7iZbwRkXscJskZuFXKZGjnq1ghvcSdlNPqxoOwL5RJRHJqE1nG1cniuolfNiL7XiMxyqFVxCui9WSmo2eRGvG8Op3909oKT5rndCa7zC91J9WwkRJ3CKtbB7vRgwxKH'
        b'bArzMyspNI0fO2ZSKBoJoIpkV1ERX++us1Xaq+w2wRhWEbB7qNoATDDg78ZaDuiFIsqCZuKyV3i7USWm0MdTLIKtygrcJYhGFtBN7JU1tHa7OE6AjFI7gGBd+/YxnfMH'
        b'8fZathXV3ptRI9yj/FyKn0v7mLKNjx/CvweylLS0AoPKH9O5WbqDYnXU1Vj9mvm0J5kul9PlV7jrHHaPy00ZnMJbB8vE5UHMlsDEB8p7XBtQjwfcGe/9DSf57so1Si5O'
        b'snLoOTWvAQmpIVpEgMd3CDBwDLRuRYm/Bd0BAk0EvQFMnZGGTd2aOpveAlNSCczekTJb/GuxpLjmoMfwm7/IsVHqFqyvghJOf+aTEB4RuzTHB5qLkZqja3gZH0mbraKj'
        b'IWMT4ldb3WbmEepX21bXOWtBp+0WlH9yUtRIHXpQybwEvCsqQC+GwZBGQV/nsFbSDVirR++wWd0e/VhDir7MbWOIXuG1Ozwmey2MmgvGUrBYKJ5ahWVeKEgLdKyl69Zt'
        b'x9NMHAsbEQxXHjzNxDGr/SOFj3j/03Akp6yOymYiubGtrqyx1lbb9C52q8JKtxqc4m4tlLLq61zOVXa6E1uxht7sUhndy62zAefIoEMLnZtlrV3ODO1ujxMkR0Ycah+J'
        b'EEhEIACSmYFkoePrZQtfJDOUHgUN7DC+1Fk2zBYeDSRv89Q427mYUe+2A0WVqqGv0Y31UJfb7vooVTSFhqKfYpEYbJi9wB4tIRVOJ435q68KNbl42VQInaYhLImst7lg'
        b'ka4C7mitoB4C3RhfOgiY7Fws6mxH0RWwWNiRE8mlZFNWtpHu6+UuoJYJsisLLnOjC8uScozZJiVaEasmr5JXyA4v1Qbws8n4VVAkr5Fb85JyTDQ08+7k4eUF+BZ5rthE'
        b'zvFo/FxFNT6uYPHhyU5yDPvcKfk55EC9MhZF40NaclaWQl7Be72UZOID+MrkUJNFUoFpdK6pOClHja+JtecqQFZV43vkyjgmWZM9+EyCO4ntRPaBhpAC7+bINfwsvs8i'
        b'15NjpGlOCW4l+x3kShlpJQfKqO2ikCM38cv43hy2taHF2xopWAokm0C24mc4vFGGb4vvn8QbyVl3lmgVcuODufgFOeqFD8nwFbyvTgwBv5E8N99NB4g0430AwjqOPI9f'
        b'SSy1fy67jdxvQBHz6s/jW6cXz7JqM/d9duitkuvrWrd+snFXfM1f3hV+yvV7972R9jPfHbv32LNX7+1b++n2+bJZc+Urtj2767vv3WjaOD95f+K0TJ92UpzlWs4v5u35'
        b'/JOv78176f3By178YZaXW3bcEf/JmV+PVOX7vJOrv/vTs40bS+fcO33gg0G/Ob5t6znFGcPs8tQP5n7o+MevBrx04ou/ba0yDJhUu/h3y6JPp9/58+St9b1f/2dWhcv3'
        b'g9/dfP3v75HYvy/qN+mFJ1f/e+AnA7W/d/3xC81PPnzy1b9Pr1+1wtCLmf1nzad2Kepv2KJCcvxcjonDzyfaxN3jp8k9cifZRHaQ7alZpFWGtHPwuUqZkpyLYUYRchyf'
        b'ws/hllQowiE5uV6fyuE2/DQ+zOqOysPPJefk59FHu8mFIRw+hjeTY8xc46hYRM0p+cSHz6qQUs6r8elh7K3SBfhyLgOJvreFXOrD4ecSRzNXVXy4n1qy5bRbcsg+fCyw'
        b'D7PFKzpuNOPT5GxyimE83jFaxCcFiiY3ZGsyyNNiuImD5LL4BQUFdPtQHIspsXeN2C0aA74tWXpNjp/HGws4fA2fmMUCeaUPyKPmlmxjCt6eSldYtoJcIPeQXi8nL5Kt'
        b'5CjbNLLnzc4NrrlC3JoqLrnRgF/N5GUF2UxOkBfEOKcH+HVih6lJcDuHIoWIFXQL6hJ5lTmI4J2z1+cWmriZMxG/iksHwI+IXiXPz5uXS7aMMCaFHga9MkccqgtkH7mV'
        b'm5+bm59CthtzpZAkAMA+Jd6lwFdTF4mbQnuSEGkpwM8bldDV/eTp2Rx+ZSF5/jHcJv+Tw5TxIm00d2QHzKw0k9K2DeKPRhcjGZSoO2kccxmVM3dSalzScaKTqXiXOprS'
        b'v/xGOdcwQJKCwjYTOIzFzk3+J46inPgqky32Q/KQyhZ0LkVzEtrUL0z0qZ5hgjqpeNm9Tw0LE8Oij4HMwIWEieHZJ0oeya/m/Z+FkxgyRJYnndMRBUUq2gAHolwsKKtJ'
        b'ggOVItyS+N+VQUk7C50kj05yRni5oiu7K+0qw1gpn+zA1gNc1knZP91WWUMFlK6QWStrxE37FbYVTtcatgtU5XWJnNrNPlHz7Sy/s3bVUaoNcXD0WF3VoMoESva4j1Ib'
        b'3EgRMSSwjxIQrahAZHOH2gG+RTIIf7JdLXoqNZpZdI+iN8stRtnYJVIYESWLbJvGLbY0lj+lEW++UfciWg0Yc3Lh56sT6//0JAtbqRm62C0nJ6KieMSRXUCExlZ4aYBt'
        b'cgPfmRpC8piQQXds8C2ebtowngsMt5Ru/y8AIkg3YNq9CYA0NQyKmYLIXfsY4TLvvkBlGH1jfqt4yv4fP9TF8ANnzZ62eejuk6ezc7cah7z/w1mlh7aNfyv1zycqjmyr'
        b'XTXhctmurK+u3fCr1uiO+XsdXrP52ZrYkbFbSmqvFDlip+E99qd/N/jYR2/tPlvpJCfzl5y9sSK67tzEiS/0vuD5dengo38buUQTsTTuhz9qXZ7jrzw3KSJ35cW3ev3i'
        b'w2W/3X957fMpDw//qvLQ9PfvmKJztv9Vs/fQuN01n5m9H0xcUfySQccs/LPiNWLItMgKKZR1s1lkpLcjybXc4AjIyVnyKoqeL3MsJrsZs3DgTZHhucUufJFxC0TOMnLt'
        b'IZeAObXg2zTOZCBO0gZ8hHkjkk3T6sJQ/DJ8h1F8vCtH3Cq5WI/vBljf0amU9U0eIh4hOIHPj0wOxvfAbWQ3isQ3eHJ5On6ZeTgsVcYGYynNJJtoMKVico1Vm14mD/LM'
        b'lfgaZZmFWWwHZhQw/ku4RZnekWtKHPPQXOaKNhK/4GQCazYALo7F0l7SaPCAXDs4c6oan5mqYmMd6VIms90WRbIOKZfxg8jmtawLK8mtwZFkZ2PXIzVzyXVWYj25jQ8k'
        b'G/NBMqXh73MU5GgyiK/7ZC68c2W4M/aPytNUku7AuNjYEC6mnkj5l1I6CJHAxTJORYOG6BgnE10idNQNQifxCKmqDq5wGzqyqx6ih/Bi2Xbfh4OQJPGdmFTCz8IwqU4A'
        b'dFHNKWlhqjkNMEBVc/ilRrQogfPwcC1r4hKggMCH5ljsjQf8CPsD+YiUsVXQIQqfX2uudZoltdntl1kr3KKdJYwK748xB3fARXtkDi8dItfyMIp8Q5+AaaVTuS5Gw+DW'
        b'M42E18y+R9HEu4Y1cqwvaLnMpad9csU3cidpH9Apbh1XG+mRCVwjy9OSVTLRlAjXcvpNC2YE5AsejApyyxV2N4BRWcP4zAgg89RKxVRnegGzx4agt31FncNeafeYxQF3'
        b'2521bLb8EaVr6kTbFBsUyRDlVzCm7FeLll2nqxsvYZ25zkUdgG1mVn4eHSwaR1LD/G10NFAepwQhhR2KlwauwxthJ54NG4u1Sm2hMBTUGrqMq+ITRDsVDECsWFsS7aRR'
        b'7KprXXBSdR2hVJvN0KbLbF7CS8aZuFAbmfisexSMZZAEkDAUChVFMxj1kKY74ZPKTCMAmNmxJXZeIqYd96VHHWQxei0PNJzIcP8kYILAneLXsUFo5JaLVjFonpt2kXed'
        b'QpLdEK7ZSjwRBgyl2ezwmM0VFApaPRVmG6KCcNBnjw0GFwCDnzbdRfmo62I3LdvM5iq447oMN0JbtYVpNTj/KaHLpldgQSznnTFi+8u45dRYxe7TK2a/FCeCwtENwgI4'
        b'tpVm8zJe8mrXMLmef6jhQwCjJboAFjQWatlw0Ea1AbOp2EA33a+FbtYFpr/DsNeGG4BvG3Y5o3N09mf0OOrVMKfuMKNe/Z/MtSI41zN6nmvQM8z14Vq1hVlhQS93OqSB'
        b'ld5+2qWdSHddz9QQZjavpS1dQyHm6MCTDj3sIKcOD9vDPnQ/BzHCyzfxwSFOvihrX2CMlAYihZwI3u0EHKx4qyCYzevplDPGwSIwhqx69jgs4ofgFwXwFCcZomEw7nY3'
        b'6JS4sRqbwgyGq2tbjzAYieEHw+S6Q1t9KXyn3d4Ks3kbheEehSGEyNEH3XdXx0CIbO8wOwr3ck/dZTW2BGi5tgMt79qaDIVQFapQB6mKyoMYBYF8XOcuM+8KmV9X4PRk'
        b'A++00WNGNqEdD9gwdHd2xmxe4QUk3MVLWxkadhS1AxKwAo+MBKKvhwv3NCqsxv3hkKBrWx2QYHLomMR0RYf+wVHq33mUmDDCpbYjRjcjEmk2e1xem2BfZTYfogujnfZq'
        b'QERoiA0CGyz2n8PbLwhvv7CIzKd+O8BaYFkOp9PFQDlBB/VNOqi9g3C2P/3PAU0IAprQFf3owI74VjhVLICQ2Xw+CGIIijk7r315KHQd5NJeodB5KHx08xogab9ewq/j'
        b'18kkKGVNFF6ZeFUVgNivhBGBZkHyZlTz+yiUdAYUDEo6/Yr6GqfDRp14V1jttYKtOwlTYzaLdZrNV3mJXGiYIhPDU9VG/rChV7DHgZLdS5VUlhM5TSQbegmLA5JDOG7D'
        b'ArJVm8136BCf6zjE7MGjtKZ5jNbqnG6z+V6Y1tiD7luLY615xJa4ICptEXcyn+0wF921DcqR2Xw/IK3EdmBbFeFa746Hs17e6qEley0IIt8Jkqv2dtiDR26nusd2IthC'
        b'tUKFrwdbigldw/SRaysKYxENrhN6fIaujOXIpfaAxslcOzhBJsgp2+gDYKyjK4JqcXwzf0pcI9LKYAAqCj6mlT4YyjZ07bXV+jpnvbglPCZNdI3w1tU5aayfB3xaip8b'
        b'AytlR2C6/OqVXmutx95gC11EfhXUVG33gD5rW10XUN26tRnAOLDGzea3ApKvmoUfpd/BCxkRqdBFxm3osBhSO7kAuhxSfW6H00PDiVEnXb+uo5UZ8lVVtkqPfZUYlxrI'
        b'qcPq9phFG6pfbva6HC4aL9p1jCbtzoRB/PSrgwp7JDNaitunzAzOFFfXEZowKnOaJmdpcokmz9OEBjJ1XaXJDZrQL5W4XqQJk6NeocmrNHmNJoytEprQfTfX2zT5Hk1+'
        b'SJMf0eRdmrxHk5/Q5Kc0+VVgjA2x//84J3by+1gJyTt0C4D6QqiRXCZXyHk51/4Tw8dxfHw3nogKnhvE8aPUXCLH6zWcTqmNVMvgR66Tq5X0r1aulakV9FcnUyt1Mp2a'
        b'/mgjtDLxJ0HGfLbJZbJvmpvsJK3kmVXMNRGpE3nvqrndx3r9n05eiYHoqlVyFutVzaK8sVivNNabFOWNxXUVIlhexaK+KVjUN5UU5U3L8lEsH8GivilY1DeVFOUthuV7'
        b'sXwki/qmYFHfVFKUtziWj2f5KBb1TcGivqmYj6NCSGT5vixPI7v1Y/n+LB8D+QEsP5DlaSS3QSw/mOVpJDc9yw9h+d4s0puCRXqj+TgW6U3BIr3RfDzkR7L8KJZPgHwS'
        b'yxtYvg+L66Zgcd1oPhHyRpY3sXxfyKewfCrL94N8GsuPYfn+kB/L8uNYfgDkx7P8BJYfCPmJLD+J5UV/SOrdSP0hqV8jKtczj0ZUPoT5MqLyocJMRt3S/dH01Etp+4HS'
        b'96913v4JnLsMKSSFnOtUjPpUMAePSmstJYwVNsmJzWNnmy8BNwwW1yzg3kY9McRdDlvH/RhpF6ij5wXViEJOv1ooGbaKB3cEZ6WXyvnBmjvU5nQFKrR7RKOY+GpgUyUj'
        b'Pb90tlSDpRvfuw6Z7CrJjcSqr2AmPKhO3AsLPZ1rFJsM9FXyr/S4bHRAOtRndTN3Tgocc+5YBTVZHQ69l4pXjjWU8XQ49tvh5Q4Ml6qtlORQbwZ3OUf5n0tNeWBf1Mx7'
        b'OZc2wAc9zHZ5ilsnE4DnmcVUzlIFS5UsVbFUzdIIlmpA6qR/I1lOy9IoluoEGaTR7DqGpb1YGsvS3iyNY2k8SxNY2oeliSzty9J+LO3P0gEsHcjSQSwdDNxbZtYLHKRD'
        b'2J2hjfzJYafQbPRUMki68nWKRvlJWKOnOPcWAa77oHXyWi27pzzFufYIKuDwIxrl1By4Tu4ZCRxf3sS7j3hGCepGuWi19STRu42KJhmHVq5qhn4t0zWDEOi+lIM2Q8tM'
        b'OIsocP0/VDqYICJ+l2XS80Jg7GGOnzP7ebP5gcI8wj3C/WBE50pqrNTlqd1rSjSYGvzaYmD79hWSb6JS3A4UQ4/KzHbBrzB7bR4XjQkjnlHwR4txzYOn01yzKWOi+3Iu'
        b'qk646KFcMUrJYiYWdDzYCGKfuO8LNdZ5XSDO2qAJJhKomBXdY/UrzSvc1azp5fSwn8JsE/+wo39RgdfYN8jgpcoaumfJgt9aPV43yCUuGzVvWx00sFFtlRMgZuNqr7JX'
        b'Mg9lEEVEWhF8bF3hae+QP87scFZaHR1P3NPgwzV0p9UN8LG1CtWwv2JQYv8Ac6chBzEW1qFUVgHXK9x+DQDp8rip3zUTqvwqmBc6J35demBmxJlQuW0e+sCgFD0AqA3B'
        b'r1xeT78AHxKvYD369mAJbDZ/S4W+ckStz+ow8bDUXe50+8PTNEaKRa9jRg0d5OVcQ59OI/BYMZ4l+8bnCHXv5BkLio7oe5rYuamgE+q0UuY5ULu8/QClUYx84HFKh06p'
        b'D6AAJNpetQYIbwhBfAyfVGqTc2X0BGx8ANgHIztGyaLb7CucnvaTrix06CMet2XtZvXUbmKw3Y7Bsbo2S2OVPkZsqtyeWu3fsbehgbE6NSsFDn303vYYE2tQsF1DmJhY'
        b'/0XTrMulPTU9JNj0L9P1YrhYt7dCOlnB/M1pe5KzixR4qUe4mJAkVsQ2FKlMUwevUXmEBaQJE8opRV/Sfq/KbqMNSgIC1A4F2l1hgrTfrR8tjdNoI1zaPexvIHDWaLZ1'
        b'OFqMXjX6MeapvKfBSgoO1viugUm6wc/0WQvSUyHJfAwsBRLyRU9wJAfhmNbhPDyN+2Gr6HgyvjM8GcWZs1NnZ84qfYy1CvD8tSd4UoLwFLPZD2HZkoNUwIe+k+dOin42'
        b'C1Ai+ik56q1r3NKBcH2trdpKFe/HGrUve4JybBDK0QFUD3gfhQAscWZ9Usn8BeWPN0Z/66n1CcHWRzHi7nQup5KseKwdBNy6Oic9wQQikVc8CP9YHf97T01PDjYdXRo8'
        b'kPLoTUgHKv7RUxNTO1KwFbBmrdW2EDSsq1njph5o+qL07AJY445HbFzaNvqqp8ZndBza9kYdzuqObeqTcosz5zzeSvy6p6bTg02L3ne1gsnjNMGfdsatT8p89DalLcMH'
        b'PbU5O9jmwLChFvRJ+Y/dyX/21ODcYINDRBdDEAlr6dENaamI4S+KyoqLHq/Rf/XUaE6w0VhG45iELJ1CeZxgmK6HPbWS304TOlMuKldT1xh6nTSrsDA3u2BuaebCx6Sb'
        b'9Fm3rRcFW/+sc+sdpf0U/RygEXNtAE8tkwvdQZU7XIh3IF4LsueU0kDtRv3c+RlGfVFxdn56QWFpulFP+5CbuchgZK42cyjK1Eh1dlfb7MJ8WEFidXPS87PzFonXJWWz'
        b'QrOlxekFJekZpdmFrCy0wMwA9XY39TStc1hpuCkxHMfjDCHX0xDODw7h0BCiLqpGImJa2WK0umEUH0eG/3dPaLMo2OrEzhMnanAp+vT202PZBXMKYQpmF8yllJ6i0mMt'
        b'k296gmRJEJI+pYzbi2ojTKFAccf5iGtFOp2m6Gmoze00XgqVwo4jig3Z2s0/obrI4zAYvqfGKzoSvXZiR12v9dRmFYapBFxC2P7HfKlB9yjmr6Zl+4HMEapOR6/FA6t0'
        b'vwN+5U2Qmml5BfNvY0dlzSw9qYRUdQqwsn2aHkwtFt2TqeUqKOOIIle7DS28SJZiULv+l3ZzBU06hWlmNggaacDlRGzztD2Wc6ctokj6tTapSptM2mFU8onsK0tUx1Vy'
        b'Df07K5wh73Q/U9SKJgRc9krFJsNNE92XcMqkLTfQpLuot0Gnlm4PMCZKc+RS0X3cU4ju21a3b8RB/1Uc/RIUNUqE9VNTSwYLM/0CGYNcDKIVDhixYPf9jgsBRoyiKwR8'
        b'xZipKwCNQtRDunGbc9hqzeb6UGjCGxlYuQLDsHD7VMz4wXaW/LpOhqsng5jTjjS1AXzxR3W0Wykls5VK4tzs+71+pWSyUogWKzkzWMmpvYpFBfFrOxirlJKtSs7sTrpO'
        b'VqnIUKOUUrJmqduNWaIhSdfRWOUychL6uFLp1RhOGsRHiqTm+n8heY9ahn6GxP2k2Eh+7GPGt1B1c1/+38XL6Pav8tHKaeVqjVqmVbAvYnDkTr/IVVF1WkMO2ZlcTS4W'
        b'5KVQD3L6kYDRNQp8jfjwK2FDKdJ/7tUodPdK4Lcg9m1CmSAPfptQIV0r2XcKxWuVoBLUUFbt46s48ZuE5RFiJI1yDYtYy9OIGnA3kpWIFmLgWiv0EmKhRJTQmxH4OH/v'
        b'TiifZwdNXR4CqDyUENAoQZQYm5mbhpmjG9FmvprGEJAJQdlAzvQCf0Tww8FwucIpWB30Q3FDO9syaYvm0D0Td8CTYzLHdmoDlagDdXSmcHSDd6NMYl6iJVHDNQwI087j'
        b'HVlnm//9e2J/24JGw7CtPdZX4SQBZ3ZP7fkC7T0OA8/sqcbmbmsMTjp1iQi4fbRT/BRa65xuq4YHO2jV17odnG4pfXe+GJLc2d5mR1bL6FNrsM3OTFVqk9Hz/xumuoe2'
        b'ZeK675/EVju77gc9auh3rAIuUu4IDzQsOeMzB67lMnc/uGbuUOyaXsmXy1yDPApxewzyypMq6sPHISF4QMEUKvauoOf6K9qDJYzqBOmojsUFp008vS46/bMYLoHDcIxH'
        b'gFB0HElLU/zM/Fx6lUUT5lNCZwcYWl0dKNsBb//IkCZY0W6csWRWQdgXkJE00oESDXMk6cKa2RBD+e6xRyNhT7sfT/tsdsKcNHjxqExy+ASppG+4xsKLY0GXyji2SkQK'
        b'3ohmo6bAapEVdBF+gy/RUwiUej6lpMcvqDTzNL+SeXGJjJZ3jacju168puvBz3k64yL90OvJAPRxqMEUDnqP02N1AEGiu0/uGXBB6bxzRd0MA+eXub0rwspJCvbWCYrn'
        b'P6ZrKuy4sDIFBl1nCand7YYhSzuetAsTTLbI56QZcBUFBYwewpNkQKF1Mmns1AjYsJKFYuW1MrVMJ6MOJV56qofDe8m1dr4cZMqkjWw3puT249Bs8rwqj2zu3YU3J0h/'
        b'3fu5DrwZ5pb9yI4qymXUo4T6k9AvBwoaynnpNwIFHeW0Qq+junL6vWAFcOFYoTdwXgU78aqm0ap8sb6+VSohToiH+0qbikWmEr8xrBIS6bXQV+jH/E5UQn+WH8DyGsgP'
        b'ZPlBLB8J+cEsr2d5LeSHsPxQlo+C/DCWH87yOsiPYPmRLB8tQlQlE0YJSQBLDDx/wo5sMU3oDLeLK4+B57HQA4MwGp72gt5wQrJghOtYdm0SUuC6d0SqMEWKyEXjgLR/'
        b'aVEHvY1h/e3ti/PF+xJ8fXyJVfEsAlZEedx+1f4EYWwrJ0yl7cCYyFgcLBoVLJ5+lVCYKD6DliYJk9n9BGEcI3PT/FqKigF/CD9X5OcKDQo/P3eWn8/O9POZJfC31M9n'
        b'ZPlls+YW+GWzc3P9srmzivyy7BK4yiqGJCNrjl9WUAhXRXlQpLgQkpJM+qA817WaUaS52UUGnZ+fNdfPz851lVLixmdD3VnFfj4v288XFPr5ojw/Xwx/SzJdC1mBjHIo'
        b'UAbAZHdY+YFw58ztQfq4gBhkSx4Mdi5/1GDnXT+I2jU4t7yAnWkdhNvwcboSPGR7YYonl7Tm02ii7RFEWfTOlGx2lDDPmJ0/LwuWSA49f0k/YDyDbI7GN8kmss0+t9/f'
        b'FG56zPHmewM/sfzJkmRLav3575OsWVZHlaPCaF3y2k+/c3PPGBbEv/qS8qOVFw0y8Ujm8QxVJL6Ygi8aswLHGXuRuzL8fDS5wkIZDE2KIy2FZAc0S2MAHOHJKW51eSOL'
        b'S2l01YgfZs414TZyMuTLzPgQPhY4Xfjt+9R8gE4HjjRKBxsns1D+caEY1fFzx4r2fXIX/fxv+A+5AtViJUYGiwVbviELxJDeFPoT+90wZxfDwlGpDplp2nDHj2GqGSJp'
        b'pK+Ki6tPjMnT/jFMdXMEIFcEIJeaIVcEQyj1+oiSkOt6KjV2Qi7at67fAxxQIH7Qb0/EpNxAGEHAJJMpZV5WziLcIsZ1pRNeVlSPt2ThCzJEdtVFkj1Ah++xeLJkeznZ'
        b'2P4yYF2hab50pjqHtEK53eV4f+6CJLJ9gRrwV47wS/hqZNQscpud7M5SKmko5pgiVOn4Os2D2FdUeuOnB7nx6Zz2o90LzKx0/YwIFINQ2sYMW55xZor4+cBksrWmY9z5'
        b'kBPeZCu5QYO8LypRrVlCtrHIKlUD8IXc7PxcI2k1cCiyKK6AJ+fWkkNePTyMn7AyOYueBSf78AX84ri0NLzFkouG4lsyfJ9cGc1C3Sd4EpML6Bnp1vyykFPkSSmmJNKc'
        b'OpqG3XWS5/FFgxpY1SVyysuieVwlu/CBXNKC75LT2XmpSqTsw+vIGfwSw1AWM0YznZxOxhfxmbHGLBMUwHf5iWNnsHD4+AR+tTxZQa6I8xGu1XlJLNh6UZIIG96aJQPK'
        b'sTUK3yZNJtZ1/AI5gDe603HLKnJDDgz2MCK7Z5N93nSKj8vJmdDvQtZBmdIkmMQWozG/jIbhl+HLgdjHwbCTiJyRaYEn38PPsXg84xcqA+HlyY48kzJGjXrPlZFj5B45'
        b'wuIh45PkFNmaTO7Kg0NokkL744ulIb2hDfF4B4/wLfxq5ISEcnbsH++RjyP75tGru4UNKJ80ZXkphelXUAuDfb1+FbmJt9eTGx5lf3wLRfXn8WF8O8dLvz2DjznxJTc8'
        b'mk+/JpCUYwIMACI51MKaKk5qh0eJ8D5yR4MW4tvecfTN58jVkcl0KGBoWlLJ7pKkJKCBzakFZeLnCcRPCeCN+Bo+jS9GoHkjvTT4yXB8cXUk3kFeIi+Sm25yeyVurXdp'
        b'VxKQmvqMk+EtuC3OS4mrpazs/2PvPcCiurb34TNnhqEMTQQrKnaGjh0rFpSONGtUuqJImaHYoqIoIEVpKoqKYkOUIlIU1GStm15uevGmmJ6bbpKbYjR+u8wMbbDk3vt7'
        b'vuf/3BhxmHPO3vvssvZaa6/1vphHqU6cXUjPGiRjrWAFZVIyXCXQzqb+TXsDirNkF+GT7v+ThS1fKKPh6gA1o6m8TtpLqSrHOsV7XVIaqOOI7LI5vTc8+HKg1N3yX+98'
        b'MGrzpzMPOHou8LKY5bl33uE467/NN1kz2bePh1mf105W+SR9If1Rese28fBc35++afhw80/TT5tIcstevFPuueTJyZZLkkese3nU8yd+uTh8V+7FQ3a3FlbeLmrw/PbT'
        b'GyOPtdtUTg5+V7qx+W9XFrxV9uzXuXMGx7h+evzosz/nzrae8fySwqfeHr9o/4i6l4cURDxzM3nolCU7Mr8peH+LyS+J8vNPC3PHHigesTwlakhwjFC15MXhR8a1+PYx'
        b'iN74TeLj5z28+7839tl+W1bN+n1C685xDu9XxC78pjFyZYmY8O4r9oYLJicM9uj/z/2/BzfHBn5xMC/1ysgZNRfTn/lixWuGXnUL7wS/+VaF91cbo0wWFFRD1MQn3vn0'
        b'zt0pdcsrZtg25a52+8o6PzHz6tWjGY8fDbz36fjKx4aF5t7aMeqT0eYD6rzHr/xp2zcbJw/zMP9Q3T7a67NPv+s/M/bPxKNB3/z29u+fD32q5odn7r23MnfryVTlSAat'
        b'MB9rpyg67Y2wN1SzPZqJbP+cBa0uZCVpCZwUWA7FUCfiKajBQrZHWmOmAUduxmrc0QUywBP4Le6wG9shL8PczEQVFohNamxONZML1inSUBO4ytAPoBBKMcdvKhQFEcOW'
        b'4fTsT+NwQiXY7KLhbYA23KFlbigYwMoeA1chkzF85isxhzYR6uAc1IpYhZctWAmecTPILl4AJy3SsTkZm9JI3Yr+4honL4bJkDyJSC/nIDxir2OdIAo6g4aeJaxmnBBL'
        b'4roQdkaO4nQVxXiBSuxc3E3pKMWNkumT4Ax7cDjuoIQSuIfIB9LsM4mCzEMCDcHBDH3BVYHn/ML7MrZNSllFuqcmlRqsmDcEqslSV6abpqRhiwXsgXwLIzMTrLdIJ2sQ'
        b'mzNSSNsDZHKyHVW6skZIJ8FRR+dQaMICf2LayJdK8PyI4axPJ0LBLNKGXNItcIEoIY9L5htvZYgSc8fEUB6LPDjvHRCJWeQN9rr4BkiFQdAky1gPmRxYaS/5/gzju6CE'
        b'Rnn+RPWZq/IUcf8CJ47aXY2HiADVcIMGL+BSQOjnLzNLgXzWhMXDPCDPtd9gOsUMBHmEOAKrPNmgRKmWkysa2WUgKAKxNUjEsg2Qk0qTN/E4nImFPCOy61D6sCC6JRMx'
        b'Q3ZKuTAMT8mwMT6ZI4+3rpBRHS25M80Y5RjzX8EQP1YTEVNIalq6xZn0EOkgH7E/USkL2BuYbxzMoL+dXQLxio1/ECOAlQiDsEKWIh/BFcgsrCKSPA8uK4I6dg/zUGlA'
        b'AuknDmgcFkqpP5yJFuEnFRRqPEjEP+m52jAOEXWELIwrkGcQEURh0QqJ8ThFjFq1mrPHHp8dTB4mF9LDSDtzOI2qow+ZiQ72Bpg5DTMZatZSOGFDGnEYjgUFOkGuq0aO'
        b'G5DOaDEwiISjfEQKY81ZU7RQKXA9mYjkWinmBWJjKrWOyZbW1A/yLLRaOdfJrfEc5MJe164WqyPZUApGmpA9/OJUNj8hm7ThZI+n2aNkNuT4K+WC/8YMwRAuToBiTmp7'
        b'AFrJss3ryWgbl9Gd0xavYw5HYqnDFmjn84NMwmI4r3lOTkxkKV6fs1q/2v2f52dlzgSmvif3UN9NZhgxSlaZOIBBlcrEfpIBElNRJtH4BSSWEkty3YR8T/Nkje6ZS8kV'
        b'kV6zkspFudgRssoP5Dp+oz+HSjbZdFPJO/G4VptoEqa0Mcwy6mdT0cmimk2tQUV0ZKouHFmujl4Tuz62OwiK4UN0RrWRSiXRFKpKpT9YIayiNPorc5mrJZ17rEW/2THm'
        b'b3rMDv3v+AjBQDRMmr9drziqOm9518oe2U2uyrifS/u27kzanrGXaNMueOvsNPgkXXDpHz42V8OZpliliaVadR9+nLu6hjjpi76KV3e07ZEpOzUBWOyEurf6qeXG6x8a'
        b'xsKuaNDVXyax5e53GhWflpoUF9drrVJdrYwzldztTG63o4kAHQFgtCUskPovcZWq7O83/nJdAxxYQER8nCYCYj2NOyG9HptIM1hiHr1uDSeC6apOa7rXZhjrmsHCs2gw'
        b'xmqK2KaLZPxLb154vwE31VU5tneg4q4Vd6qXCVgdUh/dpXQY8NyDINCsmsclm4y3CMyDIGFeA2GrJLTTZ33uKa3PuzuSW+/EsBNY7XGSR6SFpSyAVBjqRaftQiTUNdhD'
        b'badek5SWEMMYYmNVDEfcLnJ1JA0R0VuWjo1pbkJsJA2dspvHUmboAGtgb1nkoQYSXBN0FK8fNleDFh4REaZKi42I4Py1sXYO65ISU5OiKaetg11CfJQqkhROg8u0ALu9'
        b'8gem9ljtFBhfE3PA4QN50NrGTrFgD4ZNj4iYH5mgJi3sCdzHcryEbv9Jegy5NDD+tTWBEjVVSstKDn4d8WyUUdz3TTf9pYJRjqRppK9SwjQPOI+XqNLrilesmPLRVfHA'
        b'djPumJN0P0KSxa2OZdBlP9Hk+K6KgrBNPnTTqC47jzo6YRXr4I6TEVoAL5Ba/fykqINqlnJgWso00CZdd1Uh0/Srnvtqmhd9nXYzvKToqq1hkaP2zeCYL3053A+NROPL'
        b'DaJGFDRjiR/FSxWwHlvM3AZJ/ktEtT3cfdoF28OXTDPVo4yZQdVFi6T+l1z/TVDn4OsE58K4Y4l+F+TPOKRqIFfh4Qqn4t8Zd9FATeUU2J3+OsLlY8pgbP+5U6Q/cx9/'
        b'E/FlRGJccOk3EXtW+0Yaxd0klk5pXyPhj2eV0lT61Aw87t+lbms8qlFiu6uwsJ+osFQ1MjHxVDhYkDZ3RdvVIO3GYDafbofhwFqtnktLXoO1HbONFFb2UE5mMvvUmtnX'
        b'T8/sMxlO+YUeYgaqNTOwWtYJtr93pkAtMtdW3SzNIbN0UG+z1OqmnllKs43SrVS9z1EsstE/Rx0D6RxtGGw2HZv8lCLj6yIG94ExbPb2gzZBZiGBM5vtmY9yFTZtZI/A'
        b'cbwsyMZLoDEYr8SvmLlSwmR+/3FVn8SsWe0d7U9mxZvZaz86a3DxHwP/Uf7awdCDoUu2b3l60O5BT1u/5eH/pGnFQOHps8Zriz7WHpV2dsT3DlWg63BmTlDLUJR0HylT'
        b'G0sTE9mmfvpHio+NeJ8R6bQt55OhsOhtKCy/1qOI91Lrf4FE/SGXPhHaH5wsFtXUo7J/6NWvyTp9MWpNnGnczYQsd4lgbS7edAoigptxRR/DM7bUMh0Gp3sap73YtdGB'
        b'PYawW1gHGyt9Et3Evsd5CYvw6JDgvXCG01KH9zYu5u8+xLlMz0iS/4QGo3dMem6kssCweNNmTwM1/frnF8/6RZoygbk2U2YvUW5z79AOe+yR7NS91y1S5tjDEuRhLL3v'
        b'ibS8Ub3uifrgOfXX8B/vy7iHOyYl83vCnuMSNfUzeX/0lGPkl0QtufvWY09c2ne83P1gZqOBMKqfzOIdCdmHqN/QA3OTMc8pxtCH4cdKoGmVJ5v8mLVxgn6vTPeJ75mm'
        b'denUwg7uX83E7CgGBrsQjgU4ywUjbBOhSApNvYyi6/2WhblLT3uex9/2Ooq0vLG9juLrD+Mx0EX4Cj2OK221vb5WYMeVNEjAlJkX2jABMbsP02G6BAtkG2QPZMeYg7IH'
        b'Z9vG2eqOMhV/7SjTtPOs0k2A6YFsbxKd6DFKHj1dwzzYwU7Yhtry8zU78sMKiqFEocImbLKgZzH0mEiwhJNisgqvzMIDaTTYZRrWTmOnRN5kKIPgvNNMoeOwSM9REe7e'
        b'oICmTVCslHNO65OQtV5Nz3gE3CcsxzrInwbXGDQKNJG99yQ2psnJtWMCNuJlKKKUmmn0AH0p7sRDCmymBzpNAhT2JztsK1azYy8sNh2opj4jzBHMImC3HRSx7xdgFeYp'
        b'aEdgneBvBwc9lnG+zcrleEFNgRaxWPCNof5vzGYnScNlhrQT7eJHRDhVbpLyg0f/EVBHj89oOVUCNk+B/f2xhl3yJPO9Vfc6cHES5EODfxo1LuEiXo5gXdWtf7A+VYWX'
        b'Qr0dqd+edhJcWiLAPjho/DgeJa/P+mIHtqrG477xbjLcrhIktD/o+VklZxNvtYK8Lse6FFCGHTIvJErLkcVYNt431FAIx4NybBq+Oq0PeWizIzSPFybhVUFwF9xh37o0'
        b'urLMSMW1WCJ19xEEV8E1iPTDb/fu3cvwZCdqySsWRDidsg4Q0qi7Da/hxRV+uqowx5vRjhe4+obbYy5pQ6i9Evcu9vahilR+ANOgQhY6Y+tquSBPNFshhrJiorAedtLI'
        b'jM530vlEFS/XIE0vsZNqyFmtOaymU6kG2kyR9GpSWgTtonK4CIfMyENFZrDdzcgAt4fjUTkWhpnNV6+yGmQ0PQTa4Crp0jqv1RuM4/qnmGC7PMMI9hgHmUI9mU4n3fDq'
        b'ZuUwzJnmgofkcGCuEhpnTsDyAXAQavum0cwNshguQo4BkV6ZZoK7kRTqw+HiMiyTQy5mQ5kDZOFV3AuFYYPjt8JZ3D4Yrq4dMRhayIQqhkzYBc1xmzFL6m5PmlEwDBvm'
        b'9Q2AihQmQ9h8Gx0/WDJBFKY8NjBixtIMd4HFHKyaZ4N5AVr2WrwCrToG246T1U4ktrXYooieu54V6DLCW9hHbDh5YoTDjxtShDSayuEP25fRdyg3FuxMyYdFK9eRtX4e'
        b'd0IFXsHjEncy3U5NG0/GpCQCmvA8Hgofi1XLSJu324TBjlg6DJXYargG2i03JvXhgRE1y2M6tVLXQm9nXwMrrEuwodE1UK0k/wuwB2uMsYVYSofDlJI0argYYw7spZOA'
        b'7B5Y6ONERAYZ4v5GMmzAM25YKWMRFKlrYKcf4+zVsvHCbth3f0bePUrTeKhcwxh5+yzf2PvBNDbDyU6H09XGZGmbk+ZRCTFqC1yktoFEEKHQ2EoyF89hexrFDsDtpLCz'
        b'jt6k+/ID+DJw9fVxDuGhID2iDrzhHB7BkrBkKggWhjgvEoWNYRYb0z3SqPsLz6TRqAd6GOMTrIkM0Rid3v5BjHvYJQIvBhulY3Owt29AoJNzYDhnMu4UisAENeaH9IFT'
        b'yxawWRDXV0pN6A2L5REJH4TYke2VU/ccGrHJT3OCRLqyhWzC9SLk4BkoSKPp+mRhlkNeaJAygMPShy/WBrxool1qiPimrymQ6X8OtpMhLsb8x+zIwLbCSe/hcN17+Hio'
        b'kwlklWZaQTkRWbvZaJOuboFTeBjKiBxttDA2wosW2JiakkbUa7U06DEbJuKhGbKxIpQKL+mqFUTonRfw/LZETlTUjMdn+CmdmS0eSJpmz3UOqIRdHfkIK+yMYMd6aGRv'
        b'O59cOx8KBWFYEB5A2YfOCwYOEjiE7UO5FVc6ilju6eYSUtP+0TFkRi+FS3w/qY7vj3n+5MIUAarcsDAjkJU4D67hSb+O8zkFHAlaJmIt7nqM0xJl+kRqz5BPQYPmDHny'
        b'Nl7dma2wz09zGosnDSWuIl5jm8gCuJLMIxwM+tsIsqESOIFnrVlcTAJcgExtyAickwmmHomWUhtfOMZCKEg/l9MZrmTGPwXlx71+i00ZvP8Y2G4QN9GXNTyKmKE6wS2x'
        b'gf1k5A+KUAYVhrzhxdCwylF32mc63G611GIDHOLDQlfpUUZFYDSEsyKT5VLBmj4PzyVhnnMgPdD0wAuCfIVoM7kPf+xMKFZjHj3xhdPpgmyShMiD7TPYtSg4Cdfowpbi'
        b'HmpBk1eu2oZl7BrmbiaSlLFhZ2AbZ8OehtcZN1REGFzXNnMLka4FQTTAxEAYDiUGxkPT01zZsLda0vNoasJDrivrHGg17ugf1juBkGmI+2RwhY3NOGe8So/glc5yTxPB'
        b'2EOEU1FOrGeMVHiKzNlLamw0TIBDgogXJM7YNDH++6YLorqCqBBOLq97hb6Q2NfdumnGXv8x5aNeWld8bVX7cc+N/RrO/q15WnN9W5hb0Ym1IWmxfjl9XnvphE1IRn15'
        b'0ZKR17ZPHPZEv+phr+y9uaF4z0szfrl1+Zm3355kYVXkV3zSJFbWlnvom5Kqp3K9Nz9jfnm693vXnv10rM/RooMbc4N23Pn7Wvv8HX/ee/FV32kjx76/enKd9Yj33yzc'
        b'/8O7b+9xGFl27RVzg5G/Ycu5I+WOm53sX/zU+6ThzXXfvPT78M0++55r9/3XnEEHRnwLL6yZbKF0GDWxvuqZ9d/GFt8pOly47/03vitbJ545uTJuw8aYGSFSrxdqX5yo'
        b'sP1pRIZ5+OnXkt77vDVV9dr4L/v5et2ZP3DbILXXH+UVWww+bL7T+vS18DMfekyamXb61pLgZ3678feqOZ8WzBlw/h/uqnWLjCt+zwj+p+tvP/vea/7XqZmtH978uLjm'
        b'TP9X3vrizrAfdg60ODPVLP5W2PGnFT/4jR526oDtkMlBMZuME8urfv+n3OfrPP/ljW0HC6wMzqeMX1ofbX/jksok0WqE+k1V43sNz7zfPnfdrtIdcz81fbVm3/Lylz78'
        b'fPdnhYvih5ivuDEl/PVk2/17Iqvf+WjmJ/PPjK9dptps+/mMnz/xHbgk/cevWoMOxzb5/bDn23UfT223WJPX/K3fzQFDfgzwWlw/c0rDFxvyltW9FDTlb3eOePXNH6ze'
        b'O/zjqDGXs4cc+HLT8PFvyz5bmpSfMHqYz0GHzW98uad6cnrDF6qL4vyLavtZRleqHb8oTmzI2/CPRbL26M3SdsVjBh9IayUZ279+4o9vhs98ZeadbWveuzs8fept49Kb'
        b'w1Q5rXmDJm3fm7r9t4Nf5wSl2txSLsj5+/PXY98/+voHl6eXjJE1lvsNuXn37VSzu7df8DX8cqWr2qkkKT5fMXpX7dIL5itN/nFmy/LF37yflvjPH5rOXrtnOPiWxY3i'
        b'D5SjeYxFDpyb3zXEAvaPoTEWDk6MvGrdOmM/HhGD1SaS2XgdcpkpKAnCYp3IqkiWuA6EZs7dVT7bSNGDvYPokq1GGVO5wVdPbL9abSSgwaR0wQiaxHQoWcjCGWaaOnUW'
        b'pESG1jNJuhez+ONZZL+o0wrTg5u08TjXpvJoiEooiO0cMTSI7EE0YCimP4uMIQLtOOzSkI9g1gjGPgIVUM2uEtW8FOocHVyUuMdJ6CsTjJeSFT8VMlnVRK5UejlS7rtc'
        b'JwnuDhDkUCg6Eym4j3WmJRzGuk48MYZQz2hiiLqXk0pjY1eTplTRgA+q3AT5BCRAkVbLlQvD/GR4lChfJ1hDVkJrqCNvBR7Hc6Sm8+J4OA+tPOjGD/ZxrhpjbOQhQ1Js'
        b'T3WnGh15wWI1FBilmOFFNY3q6xHAg5VLhABskpM9qwoaWUAOlJJt+IhjlxMHzJsvWPlISYc2LWRk9likghN+2gCKIDr6wzYJfTBbSmyby16s+81mKenhxR5XZ0ZcaBgK'
        b'VwSLIOkarJHzcJY9UNPHMciJWDiUMo3Mtzkr8ZqILXgWjrNOnu4ABVpVhAxrqVYV2TmAvTq5symObTlkV+Z7zhRNNM0SA2jqEkx2DvM10WTYHMBDpuodZzLCuwJ/ibk7'
        b'C8ZxhTMstmR4LFx7QGQJNs6noSVkr6jhYSLHZzwWROaONpSpaxwTUUhPMnogPA3nN/Egm64hNiaP8yAb3IH5rPdGwCE5GXVfDRHPhNWCBW6XJkEDXOGL6wQ0hBPdmpLN'
        b'UQYeBV6FK4mUbO4UlrGAJzffkXyHxJxJfIeEAlv26tEbMFujS3iS7YopE1ZS1uUqrJnURZUQYSfRJSB/HIsRmhO+ubsmkWzToUngMTzIJ1HBMGIO59FoJl0oUz/cLSM3'
        b'1Fhh42Qe/0NMOeeH8xXhSSONswhLVEwa4SEsc/Tz9yHyKGQCHpI4RNuy1ZKAhYKfhkcP98MuzqW3CeqUpv9OGI7S9r+IP/tvBAXdsOgGtsncYTLqRezuDhsnF40YX4wl'
        b'oyqSS8R7NKuMhwFR1DpzFizUj1IZkW9E8kd2z0hKU9TJnVJKe0S5ZjjJEf/Lf6fP0jKsRErsZ06pPqRW0n6au0zYv1YixRE3FXmYkjn/TcpCkUSRutXuyUTxT5lUvCuX'
        b'iXfkBuIfcrl4W24o/i43En+TGYu/WpuI28VfZArxX3JT8WeZmfiTzFz8UWYh3pJZij8Y9RG/l1nJvjPtJ9dkzJkyor4u7rluXcWdijx2iccVsUSzifSHBwtbit3QEeLQ'
        b'kbvVceZh83824kqjTi1coG2hap+uURN14U/Mk7mX/OrQmydzziv6OA3v11VKCUtgC3zA+Ss9gZUw0OFHO3+lFMjvinpCFmbHpVLewsiEBAat2oktmDQwnrYsMqEL4ipH'
        b'64qJ4XCEkXaJsRk9CuWBMPYREQvXp/okxkVE2EUlJEWvU7po0HG1QRBp6ti4tAQaibAxKc0uI5KTKcbEU/7DnkzGnRsRn8hujGMgApqs0Vg1TyXlEIl2FOzJLj5G/fBU'
        b'hRT7YKqdDwtGIDNSHU8RaEk9NDAh0i46TZ2atJ4Xq3s1n5iICCXFyuk1foP0j7Y/6Mf4RLv0yS6ULHsO6cYM2pmpayJTda3tCBHRW6Lm3RgsLot14oEYpAAKktuli7RJ'
        b'uatVSWnJDENPb4nk1VPjo9MSIlU81ETDcM8hHdR29jQp3ol0AamWIa5sTCa/xqZGuyjZIPQSakI7NDVWOy6acWehaIndOSk1ox+TxFKCkymgsr4yuwzAAzgdJYI+TkeT'
        b'QGZlqvDyeOaAN5drElxWYAH3v1MnSTRkRim65EJslHRkQzjCiTQKEjuK2KOlGoeknRERxtTteSXFDUsHDfXuOzrlcawLIRrshblQunyOTyrU4HGoN5oR6DQEK4iOWTEP'
        b'2oZtgnOWbguglPmKbjj6UI+h2w/pqSZDR8kFBvoAeVGDme0eSol599JsGvIPUeRGrJXZ4TWsgXZoYo/nBPDcC09xm2nytk1CvNXvXwrqdFpwVNbo52eY7PS09vrojw/y'
        b'r19VrtgecWRXq3BYASeNq07uKZjk2nbw3XhZGz7jbuY953jc+7N/fcqwYbLZoLaXXl312bApn0UHW+KNw35e8+1Dy27tHG6e/rvSaeVM8+Uv/Tjzw5GRUyefHno89l9Z'
        b'UYm5xi/9aLgsc9Cr6gylgmux1dBGzB5u82AtXNTYPdTogfNLOMViO9RBjh+2rNJlA+Q+nkpPOaCd6GD7mf6yArIf9pwXj2zg8dHXh/ZVU//slDBne61rqg/uk0I9tm5i'
        b'0dprY3C/zjaillEqXhfTByzltMcVg5wdqfK6CK5pg+3nw1nWZsc0JdFCy/GILtieaPvcbGmAMqim9gLRuo9rcwwgG1pYo3C3YjKx2A5N6EG5iLlQxaPEq+Bwkk7Nxf24'
        b'o6uqOw8O8qj5/WZQokfTHZ+iCSd3gv2aA70HhpQY0/Q/tliZdkMzm7trN0S/mcJIg0UZ0yXMpSzcWWLVPZZAV5Q2mkWHsnGfWAalyO/o2F+Lya9VMg3bUff9Vci00nfi'
        b'20tDaDwp2WpWkb2mC0yCNlW2t0hEaY70oRJl6eb6m0zP5hoam6hBT+0KzZ6m5pttLBN3RDZ7zfGZG9oJbr23HSo2Kj5avSo6IZ6Uwgl1tXhTcRQ/MnqNC7vDxYv+nMtu'
        b'6w3FvVOpmr6ZymIXnXTBixRtWB3LmpmkiqFfENmvVzZrUOl7bYPL/HD/CIY4l5ackBQZo317bYfoLZRCmuoQ5Oi2oQnrVafFp3JseF2j9O8YD2zV3LlhEU5/9dHwv/yo'
        b'z8K/+ujsJcv+cq3z5v31R+f81UeXeI3764+Oj7DrRa96iIcn9BI+6hPHyWq4lhMb42TnoJn+Dl1iULsGybKgOf1qSW+hr/NVkQy4u2MOP0qU62KqyHKpkD7exa3LamHR'
        b'uRwuly8nUmF6fORf66k5YeF6mtBBuE1lDG8HX27xMQ/QvWRCJ9pYne7Vl/Npn5vAc6nd+o21OGsYKrCjBjs8gG1qaMI2BY0FqBTIxlqA2/mRSE4EtmCjm5ubgSBGY5GP'
        b'gEehEnN4AEEuXHdyDHShx4P7JXhinR8cX8eOjqRwaYhjoK9ILuyQbFg/ZQkeYdmoeB7yhzkGUp8G5Eig0mq6jVwp43nHR4OHsGMxvGhAnr8OOwdJZsyHdp4Yvd9nA7lY'
        b'n4otZLsnF/dhmWQ4USn288OSzLWQpx5HNjxJkoAHoAhasAhPs7OZsEnOamy2IJuaiNf74WmJA5ZhPWuNKV7AHDjljhSOxlVwxQbYw5q/Aiuj1eOX6AIa8vuplCKraeVo'
        b'h06NPAKnSSOhNIP31dkBnRqJ1Xa0jQm4hzexBSoCdQ25Mpc1pN6NNTEOD6zUtb4IDpHWH8AqpZS9+kg4jg0ddeIuKCN1kpc8yUMkzm3Byk5dcwDraLWbp23qs8LMXJFu'
        b'TOaAdFGCscR12BT20nAc9ixSmFE8GSkeljlJZjn48ZOqY2lE0WnESwpziSCNhFxTySxfqEpbQlufm461flT5DWVBv/QgmWjD1EdXTE+g8jGLqMKlUBFGfinFdjwJJYZY'
        b'THTtUmi3MsCyKAMz8iMAdmH+dLu+RFO0soCzluHxyg/HSdU3SQ1vfN9/xd/91oGnpeEP5e/+lvP3swt/yAvbt1Ws++VGv+ftrEbfDLnaejks69vnGm9G/hTwx95bljGu'
        b'jdc3uh8N9V3q87tT6PPP5b12NOFj79iR2z5+6uXpp07ERX/jP7J996SmtLwdtyrmG3zxzTvX1k6b8EPS1JXG/tOzF82+fMv6RmCFMsbn3YyJb16LHZYTNW/VZ6bf2j7r'
        b'snDgZpcNPhlfj/jD/Os3zhv+kZXm+MLnGd9Wbc4+u7rl2X8N+5e1vOnl72wkU/fWR760u36808YbmzILjjavjPzk+a1jDpUe2O+xwPGnOWP//GzDXYup4xft3jhKac2c'
        b'd8mrsYl5/GNWanz+1N8PtaOZyjv2sYUaXz+ZXDkaX39ttNbXfwnOOPo5O9gJ2jBoUyepITQqua+4Fs9hveb8QhIKDbNxF17nSZHFHuRJnhYqe5wUlCXBnbDLnLVoigHL'
        b'GOTJs4IMquEozZ71SOS17sQy2KHR0aEMy7ieLqaHRDB12wzqLRzpEYCPHC8SbdsI80SaIozX+BFDFV6FUrUCm+jxcp4AFyAbzzpAG29yZYAB5CVPpBAO2YIBscv2yWE7'
        b'b3IbNJCpTi7KycUcAWojyMooSGPdlAqXzeklWmausAIOkZlWj/nM4iEq+X4ZPXbghyJ4Duq0SapkCeby/Oc63DFXzY684bRgNAoPD8E2bnNk9cGDasiHHNqmfWS54yU4'
        b'voLbSXlEzW8mjxmQx84I1hFY4TGWP3U1iR4/NJtSPKJa8uB1PIJV6fwpYseeUKen0LoOCjLq/Z6gZFdcraGBXCAVwX5hE1nze2xQc0BxitiW54ntNOgx78DutpOIe3vJ'
        b'x7xPPLRMTTRhZlrE6DUtLCOo09OcE4Hdo+5Q6kSlzk3xrpFMZIQfHX8o0zHjhBdNJF3/yIhJIpLr8nub+nQNcCb1a1FWWCalaWdVWlXSxTphQYvkdfbrLJISXcJjGfn0'
        b'ZO9miWWrHrOkt6ZIWASS6n36uX83YKsbslVBPoE3FKvmhoeEeAXO9fEK5UCgOsCrG4rkyPhEbTYkzUe6YdIpXZA5M3UJop1yOfO7AmMxnCzqzGQWF3s/3rpB/3/ywquC'
        b'qTko1UwgI8HS0ERKMdvkd83lAwxET2KX3hPFv4bHaSmztDQXKTucKJt0z2ijtcRoiLWEBWPSw56kTukKUDw8gInNQQtk8cHYE3DTVPOvepykK10cBfTiYF4VMg2cF/9M'
        b'Qb2MyR/6mYJ7UWgv/n3HZ0sKqBnTl322jrHRfe4X0598HsA+D4wZFDM4xrZCQYnosuVxkpghMUOzjCigZ6lhqSRGUWpaalRqRf/EDCswNB5hPDLGPZsChsmJwTsqZjSD'
        b'vjJkJG5js4QY+xglJamjz5YqSsU4kTzZl/y1LLWK579ZkRKtSo1LTeJkMQ4xjqTMkcZOMeMoIBktNds42yzbKts6zohBeNHSjVnsrZzF4vaJk8e4xrhlGVEgUZmwTMFg'
        b'7MbfsKKLZS4jtWAYcHGxqtvjuqicPW/Q8LB1vum2C9Ffp8ark6aqU2PYv+Pc3MaNm0rV4Kkb1DFT6eJxcXNzJ3+Jgj1eKb0hCwwKCbgh8/ZZ4H1DFh6yYGG15IY4z4v8'
        b'NKZVrgoK9F9aLVNRj8ENA2Z23jDm6L/x5KNBHDGe1Y9SrTutVqY6SlfcMfqjkq5hmU9gKIeEfMSyPIho61qW6hwrMHTeotm356xJTU2e6uqakZHhoo7f4EwNAhXNjXWO'
        b'1uQWukQnrXeNiXXt1kIXYja4jXMh9SnFjvKrRYZCpoqnOIukg/yD5s72X0XshNtjaKPnzvFhLST/LozcSMVeCHUgq1NJoS5uE8hPIvxoYdUS1WIO1XiSttU01Cdwgb/X'
        b'qjmzw+Z6P2RR7kRSH+3yyrcnd3twripJrZ7DDJiuZfgnrQ5Qr2YludOSxI6SSAMv0rIsuvXH7UG9v9RtG72dp1R0KYVON1WTnrI9VC30226FeLBCxqua6bXeK3e/7fgI'
        b'b3rDMCY2LjItIZV1PxvL/0aa7MMlmaRplKIWbNUGAs6LE7DGck58YEuFjGWfRE11YdknCRJB5jXvRcn8sKL7ZJ/cMKIssKlkVjOlQ1+eHEtDWcABXLtKExfts72nMVwj'
        b'rzGDfFLb69UChEzTNj16wP3qqjbkO7Zaz7adptu76ez8J21LWGCP5AcTbc9SlAGW/CBoOUo5SluciS6xweShEhtonvMOQz1+TR+ebxy/KbaTd5MTEfEzKCqT7+PNDNVS'
        b'BdslM1oIpsKop/a80dmu27qxs5/npbz/bXTdPfAODzt7B3U8PdBKn+wyyeEhiuRL2c5+rveDb9YsWXqzk92D6uldnNjZ+4Q90hPu93niYSUDLaJ7o3tzHGucX9xLxFPB'
        b'NRRUWnqD3p6k2yd/rPu0SVbFJ6niUzdyJGF7B7opU3Ivui076PclOtDNmt5Dt04H6jh2oHueg9Kl48x1kss4F7epmlv0F9NxPOvGbtWU2vH1JPY1L7q3F+OwFZpX0wNK'
        b'wftnrJrhUvTaPezYYmpXLAG2yPRDTGiwAHptUweOxFQdjW1PqAgK26A7oddzAE//I9cYEyH15TMfKosOiI1MpRNKreVp64S8Qc+newEkoH5YUk5GpEoTTNCJHoP1jl1o'
        b'bCx917SETtRveouaOzvMa0FQyNJVlIcoKNRrFaWgCWWt1B3kc0K6XjuJCyHeP4wySgPkoh03rfmm8SDrP/fu8CqzkwpeQofT16GbTHHoNXKAjVAyX6dqTmfXTcQ48LfT'
        b'3hKfqB8tgWNyEAVVy8q7JjLRzis8pBfveKJdaEZ86qZYVQIbuNT7NJ4LxF7WElkwPqmRCRvZg71LOIfe56wGTIQPSAfGCJ35miHR4Y3wg6pe3iiVB0J0ghrv8mwXrJhe'
        b'pRYrqcfJAekejRal1k7fbuXqHxMNw2NHvYxZMyo2ISlxNS3pAR52qpUY91CjLAKZu3YUlMARLPHDQtwnFUQ5tGKVxB5KsYlpWckWQZrkQ7huw4IfoMGOBz8w5+xlqI9W'
        b'z13TAWs6YgyLihgNdRnUDoZ8oqW12EARNkKuTDDDLBHziJVcxHL746DW068TtqkWZ7VX/M8APAVHDHxFYSLsNMcsNyjU+LmH43lznS8YD2GhqWSWHWSyRtq7QbnGgWyF'
        b'5U6SWWZwLW0hudAHrkJdJ6TXjpboEmiSzcxCKNCrvXNgPJaF29vjHsx3xT1OFNeTw5Y6U4/fgb4Suw3zWVPC1XhZjbtgdyc8Uj+8xs4z3HwNx70gHUBBL53+2LBMSJtB'
        b'O/HghKjOIKXeLr4BmEve2jUEc/yDvaUhkEsjM/EyFsMpOLVxtADXZQo8CFmwJ/7YL58YqI+TYiw+XDq6oMF8h6fp7n8MTbZ1O/yb1cuFCU+/+9LB1gnmrUN2G/d79dNf'
        b'nW8GfPvPV8Z8+PYv3+/0tF+9dMCO7aL5wOk/vtn4e+DMlQO3ViqLlo+zSavxTyhdl57R8OaWf3z0aebH3wWvKXK6EzBpwk8lfd5w+eSDMaPhw4I3WgYtXHm37sDThr+N'
        b'XtOkmu5wxOi1cN9l12MPb31rf/Kkt3/u/0J8yPwbvjYrVzWJLleXCEoz5kf0eFzq6OLs7SxC3WOCHE6KbnBmOIPFwBrYCVc4qDJFgXaiYRuGgnmIlPx2yd3Mg7l4o6zh'
        b'gi4IA65jI3fwYj0e5t7IE2RCn9XEkMAp3Nk5huQQXObBqjvnT/BbDjm6EJKDscyPm7Sq04SU0Qhxa8cELMrgESL5wVDQM37eC7YbLYNyFgS8MBSOdHhzNZ7c8XhgHlyH'
        b'AywMY5oVZELeBPqO+rEL8VACD/04i4XbGMJkZ3xJKISTK+0hj3mzF0/CNp0DHmvwNPfAn4RSHk5/Bc6oSGvICsRL9I5SvBwgmZ+xlWUJuEDVZj+yMIux0J90QpTEfcma'
        b'LngVJv+WA06HjTenF2PKagt1wsmlNMzVhCLlUffcPSNRJuHBpxTlzlyUiYNogOs9/cZQZ8w7VYpEn1M5vQv2XMD9jLChNQ9rhD0qX0u15IbBKgbB1xtIVgH5xFHo9FWo'
        b'43p2eQgVuDuCHHVVhXrPDrkho0yuN2SU1FVpqC++lkev0mDWG4Ya7m/VUxI9ifMW2u1koaBLnOfWo6nGfjTjON/ZFnEWj5gev5pYkWf1WZGzY2LUXdmrtbuoHg+fTv/q'
        b'aYzG2U2l2uHUCB2KSYSeo3wnjTajA96iUZM9g0y7MzFyImJqpHfoqKm0J1M1GvxD2UYarVbH1fsg84hTdfFn9RDqRqrt4hKSIqnfwI4xx2qoMXuLo4lM7EJD152Ht7dW'
        b'dLEZ9NHkpsZu4Apxqo5Zdj2P+OwlhJPcEx9DtbmOrugg8+PvYGfPGObpqzFtbUTIfBcXlxHKXvRMHg3BwpEj6WzqxC+tK5kTaHL9t+O63vJ0z3TwYWqmgCZSqys7pt4y'
        b'7EO85nvRMxuvVYHhAXO8QpzstGYJpxDtNbqLxR/3TiWblMzjse9TwgZ9ll4vnK33KY7+pzMEaQ/fz07TgcFpZrXe0rQE4fpMOjvSK14hgbP9e5pv+kOWH9Kk03J68a7Q'
        b'USvTCauZN3RdECs4lrFnR0QEJiVSSXGfWO4NqR21M+Jd2keRCTR+mgoI3dSNUyWtJ10VE9lL0HVCGvecrY5Pj03UznyyNGNoVI99dFKiOp50Fy2JdFw8+5b0cq8N48V0'
        b'9jcoO7+mhmg6am1sdCqXB/otnNCgKZPc3O049S1/H9oGJw2MqOZ9mQOArk0iFPWWE5emYmuNrXZOYdurmcd3pal2oRqzSks8T8PSN5JaEhLI4otUceOK36xftqjVSdHx'
        b'bBB0Rl6yKonyx9NeJF2rGWyyEPi019+ZnWgZ7QKJuReZnJwQH83iDam9zdZT5zB7/Wtnroa/voMGlm7Ydvbkp9LJjm7bdvZB4SFKOhh0+7azn+MV2Ms6dOiUNzBJ6fAQ'
        b'2Qy64K3ZOlHfjVLpfkGhXWxNI7225jAOZYM7BntorEkhNY4Zk9uBh9Iz66h6NIv2klnYRfg7TrDgMC5QMwry1czAhO1zmY2JzRPm8+T8U6OxiuO4hMSywCc48hi7MvUx'
        b'ov1z8Jc4G6wSYD+2JIel0cTAWbjdQ2uawgXYRePFOmxTOIYtjJ9mmPcozNMwOFCajzANdIGfs8Mibyff8N5tVE62UDfE0qsP5E1dx95iCLGr20iDrphrbFRin6bZ81il'
        b'/bAD8h+xLk6Og3tXUX6cYHsdroVSLkx1s8b6YNAEsLVuM1IEpXDrl5i+xEQ4lLaRXmibh0V+DPjH2TeImr+8EANiD+wyGT0Qqk20Viec8sRMrCAXTljBLjgZBpUxwZA7'
        b'ZyuxpnZADcub3QG7122AfXB6TtRK2DNHFR8cvHalavRjUL5ujaWwGbKxcIYtVOBONz5wDbjPS2Eeic3JpqIgYrvENUPKwSxOhMA5v21Le2sZ5g6EXE8oiiID17lJu/AE'
        b'ltLPNL4rwgKz7QQ4H9xnAFzEg2wE+pLJcUaBOzGLx5gZS1zhalIaDQ/AnIVwVucHUC7SYPwkp6WF4b5kMwssDtN0eycXAfUMkLGBXZbhWggQLRQOMfDOGrFazDGnH16A'
        b'SsxLo9yrA2yhuQsM0yIomtYNZ4g+GNZlQLEJss0W4BUjjtq5H894+HVmSSqA8wvZrCGl+pEvyN1sNpUYqH1hjxWZ3XuwJISY1XskeD2FlNQcznJSoMXBWleQJ5Rry/Lu'
        b'sEkXaYrk5cEuBZRaj8bTNnAGTvWzkQpQHtAHTolYmDaTFpgTO18PdJKIx4nlSSz46WR4dmAW6VwWZwfFUQJmQw1Wh5iGbFvKMG+G4W7zTh4Zfx+lr7NLV24TDRyTpk1m'
        b'uuUCpVDOlgzpsSNpVlA0CU+khVN5NDJRiywR7P3XytaUG+JrDfVkdNuX2PEgyX1D8YKa+3kSsZq5epZhIwvTYW4wqCJvflzLvmOEWV3Jd5Y7Uz7HeJtnbAzUB4idtWvu'
        b'4YDgq4GDZ1t+8H7b1abHM5rdI+Z4DzwVdMywcu+nb80ZJLk4euS3AyeXr4vyGjiodEHr1/Z3ZO0SG4NYk5aN+VvabK1e+m7LrPHTxjtKfbzWB5TlzQlzsvxw1/LJuyeU'
        b'v/WGif3Skyftf48NDB9/98JnM8YtXB+9pOVK4KgV9r4elycM/vZ68YXX38yZGOv3yfWG4f0Tv8oMWNq49NDUspPPLUtT/3nI+OmQY2/O/33gP9Y2p0/wvPtB2Pp/BRWc'
        b'DfJY+9jctu2L5r0Vvrh44s5F719+88CXyo8iNzhs2P1qdPwl/zsWN1OeqPH5ecgTGX9/6558Vu61mKLFv3pmv7856XX7e0Zh+668ufWZSX872/J13GbB5a70zJvmlxes'
        b'SJz9S7+Nts1L4a7Rt1PWfJlg8f3M7+xu/fHbV33fiH8bX5n1iW24683AK2sz7w7+PrjJ8N7xTza/dDBw+bf3ci80lh3fm9Y809J++ev+slkjLv980rWw8a03A53afo88'
        b'kPHWV7NuBL3z8YsfTuo/QBn7jm3TO1Pfe+b4ttuXghe+DBN+Ghf46/NbzP9xsP8312r+/Gzb/s0nx5SsV/bj4AYVZLvY5+fivDWms4MowdGQRfKJWI0XO8M1QAM2cLcT'
        b'VsHuVB7MugkLeczjAMhNl8y2gCbm1FoJVzCvA1qBrK8CHmrpa8dcOc4+uJtsD/lwVuvtYZ6eYxOYy8sPzpFlzzlUKIPKVWzvYFHZhJU8u38vnOrfAb6Ax/Ay5UMR8RS2'
        b'TWQeJ1+yhHZw/xbsGdYl20iJZ3m6Uh3k4dFOOVDL8AT1vmVM5110miztRkc8jKc04ZssdhNzBrIAypAIejE3yAfOywS4miJPEEfMX8BiEhPJFtGiAa2AHLi+UuJKU9O5'
        b'3+0INCdyr1rb1C48HlgLbSzbP20W2afy9LjUFAuYU23uLFZLfOD4Trn0trMEU0upTUIC95YdJSLyhN/wRCx0ogxzMicJGZTTRJ6x7P7dNlDHvHGOUNSF8AXyx/MQ0JZN'
        b'UMw9m8IUKOKezfNwhMEMjEMi+Pz8fbAyGXK7ZaJJBTdolbsarOI9XItHUtg0GpZI9pcgokuYz5POSMI97A3gmjMUsDQzd4mA561YmplkKo/rLIEGa8hzDSBiRcADSfIZ'
        b'ol1fzFEaPXROs8V/JxhvrxYVspTqiHp8gcI2k5mmEnPRUjSXmJK/ctGS/DWSWklMLWmMp/yeiVTG0tuNJOJ2E5F+pmnrouZ7lkgvWktZwjv5aynKNQnxNOnM1ICmoVmJ'
        b'3N9oTr1790xpcr1IU9PptU0j9DjdHjE5vcN5pnq2a/Law/d/55zyZ/UkluvJKd9noE3A0+PRFDLtv9Dj03yIt+09uofu9MzVx8NEhDi5Ls5H+rAAqLcjepgRIbGJxIJV'
        b'P8ifx5wHGoOFmquRarslAf4PsEookOLQHlaJUyDjiIN2EQ75deSKButQ6zSIdXmL7XukjtK9wAwPYI7NvC0cK+0qnsQGutNDoxPd7Lvu9JNmcmOm0hGOc4VhLpTxsyHP'
        b'vswsmQI1cnol1YVIXZd08gPOYKUvRXMdtdJgMj2zoprzJsgkzSOly4SB0yVDBdi3FU+zzAon0oRSIgKyErSHefQkLxCOMdvqgqtUuDOIhptGmM5IMRDY4R9chxY8N56I'
        b'8N0UtJKyxh8lX4biAWY8ODtRdA+aa0J02O2CK1TCCab3jB+JVQpjoubgNWiSYDWxyaAO89krGsHVCEcomad0INuDbKOEmA6nyCUmIetH4GE/ur8EGgiLIV/eTzQlansJ'
        b'e84sHQ6HYoEM9oVSUFG6XdVo8nYWj1OH4slAhjCnwZczdWY4mOlQPV0ROUNn3gTGs67AnXOTidpbhE267BaWfiPlzWiAK3AQG0OXaZNUBklmDMFKPkI7oBxOKoKghlE7'
        b'kvocRsNObr6ejUkjpe7Gyx023NgAxhA4bzIWh0IBloZjwQrYjmXhARLBKEiCl5xNWfdvdNsr5K+fJQpuES7Xkkdwe7ev3UjByCWPjklUpWwt/9Lay0d4xX20RIiIWJsx'
        b'QiX0oGnWLUS68zOaZgVZekKlsEUSI8RIdokDheNawuYsol/+k54BUCKc2TEq//jE2GoNZbMsgfzSnXOaOvZXyAXhJ5EtGWZxzPfAyyymmZ9LGmsVYixmmRSSkEnkBsyF'
        b'XA/cle45H/fB9bgUH9XWRMgcImwZZwkNKjzO3m32SDPBdNpkQVgY4WQ0dyV/4c99+wueQ1fRM9HHdgzeKDDIODi/ERsi8Jpe4MGUSWwWmrnhYQVRrdo7WZGkLm5gtuHJ'
        b'kQq8vh6bU8yIumQtmebvxKp7iqhFvxkPpdUlVARsFZQiN5Rz8MwARUqYbir5wkVWkifsdFVA28AOq3EvtvH5cHkumWCNUG2mMFMZCtIxkhljsVYpYSlZEX5wVR1IVcQ0'
        b'b1EhscMm3397JFUvUPH/Iv3xskTowRdOx+4CGTvVKxIN9+Zk3J2hwBxZOjZbiLTxU7AGctj7Dh+ARxQqmp51hKa5EUtuxET2jHngOGw0xWZDATJtJFhCLuJ5GcOiHYQn'
        b'+yjIv8Eb4JgQPA2P8jSyWudAhb2DIzb4kznvKwbD7mWkml0cu7KRrLZd2Ojqiy3k8gRoMoCdEqIR1ybFN077SqaeSsSxk+Wa2HCfBNtwy7v3fv1m/NHyvz33zidTUvY/'
        b'mQ6HpgQaZY2OeMLJPDNr9HD5HBPpkI+O/jzPo/LD/k/vk8+eYGTcemq593ueUUWWyc+aZf0tU5GxsPUJG+OUm0/UfJUYMzb70NZ/rbx7e/mbx9z697t9ZfHUM96//uvr'
        b'qU6tU8fFRA05az3tiYHHpJMWbR5ya8jzzzzx1hthNxdmXv7JwXP+5C++bfBImrxw6LKje2YPfyPsq68rBwyqP/iTc2zTdcsxjdbVtuscmm1G+DZblx6oOb7Ht151Puqj'
        b'JWbPR0YGmr34cVlllGPw6EWz3+yXkHbdxOSLcxFr3VeffffEhUzHG6oJWbZpS3DRe3HnM98K9rr2tftP9R+eWZuxa21D85XT7Xk3J7+y70Jz2PNbjOJGvrk+4OCW74vD'
        b'J77Z9rdpP23Nfqv4bN3NvQs/yZeePBF869Dq/HsGE9tWvTZ14O8rBkW3D+vz+u6C2Px7MyZemfXK7SXPLGuNnHd3R06ArRe++ML0xZWFnyz2Ovz6rU/OP+WxYfn5r+7G'
        b'D7nnetP4m/R1lwom1d+4u7rJMG1aguHT6e99HXOtcJrHKx9E1ocukhQYT3b29prWd6/1+i146XfrKZ/LIzOMQ179V272wbfOHZQuLG4dfDx/lEnr4WIPj3NPpyj6v1F8'
        b'OnhtXem8yxvNWwZ8Eb3zneURbZGb55U/FyhWBe58X5Hez3bBdzu/bdlUefft7Ym7hng//cqA9b6fFx5Pn2X1y6S/XX2m5ucP53/6rfHY28KfT764ygXadr7t+ZzPT3d+'
        b'z/zOa3rJr86l0xqXz6v9u0f09+MdD04a+Y/Jtt9uC1guW/xe277je/YMvWgTdnGl6Y5NBxvTfv3u2mnj526N3zw24BWjQy94hcze+Xj1pLf+PD2keNNMWZthumuph8er'
        b'f2z/7hnTbT84fPbNPflPwrbjL49/ut3c+pNvG7/0+XPM+0qjtIpwtzuvvjlxutvWvEPS14d8NHVl6OXlf4++NOu5Abet1/t9nWHrEVdXHWw4Nq7997BjBzzqCj+6Y7H7'
        b'+ceNHLe+8/i8ravj/2ibH/h+6t4X3h/8vfWxaW8Y/JD2q9vBxU9Ofz7tpWvvhbw/Y8fySR9MixhWcuOJZ482vXP8OmQcnXfz5YAD625GfH7m6w3TX0rPapt3reTZX5bf'
        b'GP30H2Gt8fPfG53bctovP2PpOyvyW/2skgIODPh+7HdWwbVfFce8fMkv/9ea1OfMye+LMp579bzfvHKfr0tvueff6f9833vff77k3AyP5OlbI499PDhi1vu/vt7snnzn'
        b'quczkWMj/v5E4PN+bxQ1mN3pe9Pf7Zo0vWjM6+Zb3po04N0x1itfUjc/9+cT/1RNnul6tPDWW2vDvnz3hdVBNx+f6fVepOsTgVUm3ot+iPry55LxN1taX/F1uw5PWbuu'
        b'+GnHSze/GfPbNzevZl1JbQ9KqB3z4acJB1cNfnfRhF230+9Mjh+0rt1zWuPKBaem/vmH1d1xpRayq+Bq8ePjFbc82zdn//rO5DsvtBwPP9jy25nXn98/YvKiBeEb/znr'
        b's5em9Ss5pFzHQdxKIR/PKBw4n0pmcg9KFbKRFHJMxUvYLusC4SES3aU0HYvgAjPE1ZZ4gJh5dtjaNe5i5RYFu45VqXDUj2x7SpdFWKy5buEmXW20gtuJpVhqqY0AmQdZ'
        b'HbYqFEcwvA6oWBeoM1Vr3XsGgEhGspr8YddjjD9TNVHHosv4M6OMmKG4AC4JWrxDosRCGQM8xCu4g4ePnIdcuKDmem0alPM8JDO8LvXsC9dYt9kO3Kh2ITU7qwKhyV9J'
        b'N/ZGFneDuVJhAtbIQ8dhCYfmKxmW4KeFfcwwl68SHXBfEHdp7JyC+/38HeTCImwQV0gmL8Qj3J4u9ZtKhsOVKNISCvudLYe94mhHvMasZffx/bSgcAwQDjKdN0Im1LFX'
        b'M4dzo8i+5YwNmO8nFQzxkoiVhkFQEcaJcY7hcTihvQFbYbsfNpLdxQxyiBJAFLQzPF3zUGoK5mHzOIaFwpBs8Vx/VvvQSeb8cWcfUr2JCNmwezGWpPCUzDy4hrVqBx8s'
        b'TGZ5pnsDDQXX+ZZQL03FS2NZ2XH2Q/w0hJ14BFoN8KooXW7MfSCHfBTY6IcXgxRQbS8XjLFFjEmCU5Mt2AyMxGo8r6bokcZkYAwEEywUZ24j7SyH3XzgWrGBtc5YCbUD'
        b'aaIo6QIzaJf2xUq4ytNUd5MN9oIj1FK07g43i/VoXsAB0j2ZdCgdXZQm9g7UmYH1o60GSHG76MQ8BbMW4m6Fix82KzGPdIC5iNmTl/vPS6U6NV7ZMEkdKFnwONcLzorB'
        b'rFfkMriAjeSNaZ8z9EsDAS/CmT79pFAeHsXusYgg2n4DXPPrSkM6GHbI4PRwe9b1WA1H56hdfKDOVL6V3EJGWy6dNWM29/TUzsKzeNVN4evsnwIXvMnkVCslwsAw2QLM'
        b'l7HwMQcsWkq+w3qoodj2Alwei/t4r7Th3iA/hoKtUDEIRnMolU7f6sb63XsrHuPwjS1EOWQQjhoAx6vcOYV7R8JpdfA2Hwcl0ZWgVAIFazGbX6qfADmkQ/MMsIwYSQqy'
        b'3LaQSUZX6WZj2NUZEnWZCG1bsRazIZ+7c8qgCbMwLw3PcwhjDVA0HuXipBb3b+oC72gpVQ2yIV9fZtftcDccU9iTfkjxJ80ywUMiXLQjb3pgG3c6nYDjDJUywFkiGLuL'
        b'sDeImDatE9nFQZCnUrgoHciI5RFZFy+GQWU8XArl9MUjMNuRjI+Lj3EYh2O2gAJp1HpHzs0LO2JJtSmBEiFwmgGckeCxNRv4C52LhGyFkiwL2h8C5lkb4EEJNg2cwWZW'
        b'iDce9VMSE6iTE20d7GPXvKAyRg0541zYm0oxVwJVhlDIX6SaTNojftwpLxcUvuJgDzyzdApr6zxo6asm40LsCNzpTwEczFylRo7Ic69Jt0I9FQB4jExYsn6oDy0T97Kh'
        b'y/Ckpt5M3E/ZG4hNDNckg/tu4PMlG4tHYZ4HnO/sU8VdG7lcOwaXV3IN3hOOUhXeZT2bSO54egiPEbyANZ3cwGQxnGPtcV0Gray1/q4SwcRTXAC7ydtlzmayax5eouGh'
        b'eZjvHsKXKJmLVHhZE6GLBzIgj4VCboYab2LPN6ixUGkCtU7YTJ0TF8l9Ay1lDqbkLjZ7cid6kkI0V4h4uGawSEJEVhGcZVGONnBgPfepRntSLmmsf4x39k5TyKYnNenY'
        b'SGRDbbqsj2SlJbawHlsCteZqBk4/CdolcJQsDHPcpcmulxPp1QgVeM0Vc+3JMsGj5A5owTI2wMYu6aTB9r4ZDqJgCCXUtbzTw34IX9pttkgT7QuCKB/ALthJ9i06QyxE'
        b'aYyjwHeMPKg26YRnvloKOXMtsGQbc3LLsGIOlBPZGUh3KiJbNaJxANTI3AfAHjY7w7FsApfspEPgumgAh+m0aNag0JL5s2uqRjKyPjPBJlGKOXANGslEpDPffTnsoNsu'
        b'7dCCWeIiiTMec2BDt4EoGflqMuJ4BmqMMTeDfqT19MUSKdmTsn145x4mU6eQ7EhQ5cw2HgqTbobVPJX/dPBWrYfWBLdTD63Kn2+x57AYshSPQ1mamTHp2eGS2Y+RHYxO'
        b'xWEz4aga8ymjWa6TaC0Zidd82FQMiYdD/G18pvRPYXeQiqSjiVJQzd+3EbOgpQNDngPIH4HLRCydnJyqZFYs1MABhh/minsCnGjYqdIngMhvDsMsTJkuJ1LmbCjr3yWB'
        b'RL5T57S3E55M13mnscWBETqnQ30Qw1DuguPeDcQ9HGtJMxa6wu7pvJHNaVCtYHc6pzDpi4di+5DVClUrsIhLWWy0INVSObsOyjpots2hhYuAo8OwlUwMzZrzEsdDNZwz'
        b'cOLS+wycH6ReBNfJdSrZ90ugcL0duzQ6yY09NWoVlyoTpcYqKGVq2pik8Z2AdceYdbSfA+uew0tsDAaaQau28awCbDfrg81SOBkyjMcjN86fyCc1bscK18Cu8PcLBrOV'
        b'42qNDWTeDmcbohRbJHAWLmM+e7kJAWYK3KNVhoyIDMuD+mBr7vOHS5ADVxVTRpE9gIa+X6Lr8bySdezjRPaS18OLfZUmvgF0opDnrSGLTPgReJpNrTmU7EShFAaECpJB'
        b'Au4iMk2jKDdA1ng1GW1XokEweT3c0nKtFPYshP18vtZ44RlsVLk7ubhQQVBOtrV+yziGBJl+UKmgk5/IpDZRKRk6aANTEJabYrsBFqiJmMdc446XGoD7ZFNn+fM32o9l'
        b'0KhwZi+Epw3kQ8W+WNaPSQg3bHJkDDqBzg50MjeJI0lH7V+Qool3TsAralcHrPdWUgHULs6Ea95wch2bujak+8ux0TmQeSKgFuoNHpdgGTZzrSl8DT2CC3A2w1PdIJKt'
        b'ZNjAxW0pUWN3ql1805Rk+RPVTRShQoBS3D2AXZdYTtAo0D6ucMnCnoo3M7ws9VhjwDecciI9K8jo5fnrYrIDJPOXhzJhPQKOLPdzCZALU+eKGyXTieysTqVel/7zH/Nj'
        b'IdrB0TRIWz2Dvc06FVzlQCYaFBMyckeI1lc2Tdnnv4N3K3/AdQ06BUunlauYN5+d+SzTA32s/WPkYMTAgSnIMYUGlDGIQBmRcfRURs7gjmlsOD/LodeMyF30jzW5x1Ii'
        b'3qOwxuK9AUa2EvEnUwtLhvUh/imT0fOdUZJR4iDyJLl2m3xnRrnX6RPiHZlcRq7KxTH3xO3mEvGueM/SaCgt70/5CybTLEXK106BkCkcsqVkALnDVm4psaY4I1JbWp9U'
        b'/N3K2JL9Tr8dYDaAAjlL7Mln8p1B77WL92wNBkhouQy7hEE5W5MWGcnF382N5b8YKcSfTZ4SfzMJNWGQyRQ02VRiR36OkdC6SVv+pO0V78r/MLI2kmwaqOcsh/d+J7bB'
        b'B4xdp0zlV8lo2crJsDmR3/QfKQmZ/W7oOVTqvSGkepYm/4SEJiIHBipl5AcLLK827QZjokoQWDZ26FxvrwCvUAZcwrKnOY6JWgc+QtupohDH/FjO+v8EXmSarpsO00lN'
        b'T952CzToTSaKcpEDdN8RDf9zn+QvipPNJUYWRgyuRJRY3xNncBCSATJzet+folSUDL0nbBtqkkYRZnDXDP8evnq4iucD/YicmL5MjnugIbVHlr2J5l+11f1hSKQxRprP'
        b'xp0+m5DPihhT9tmMfDbXfG/R6bMGkqTCWAc3Yh1j0wluRNoJbqRfgaHxQONBMWN0cCODY2x1cCMUpkSIGRZj9whwI8ML5MaDSIljdWAjZnEGMSNiRuqFGaHgJl1hRuxv'
        b'WDBMHsamPS82Kj71tmsPjJFOV/8NgJEpPHN9nFK8IZsbFOJ1Qzpn3BzVcTrdq+iPU5KHR/qYwlMvxz0SPIjmoSmPDgGirY5lerpTCBBVLc/JoWAdqjoGORTiFRAU5sWg'
        b'P0Z1g90InTcvJDala365m6qBvvDD3Oquw8fQNuT2gN5K1YFmdG2z0rhLGXQcVB92Rt7Qdo7qI/pGN+ml3upwV12l9/z38DL0Eon2JMo14MG30GIIuQzQD7NHUEy/0xKH'
        b'PjJ2kGYPVUTDPxStYLBfFCavAg/gxXiTl1xFNbVGXxmcQ0nRvSNfjHOICoo0iftS+HHHwCmvC01yD0tZjZutUsI0VQMbaGa4bXMgSxf7cwGyeiELvaYNC6HWVW8qAgsO'
        b'saNcB5sGdFtlDwm8YUU6Wu12n+2MAXB8rGdL673C63RU36boGjSn7/8EXYPmRQ2XPyy6RgxrNYUPoDH9/0loDe3CeAC0hnZhPfCOKQ8NrdF1rfYGrdHbkr8P1oXe5av/'
        b'/keAtuievcUTDSITaY4ATcLqJaVI95g+6NQecBhdxlkDgUG3DQ5rQbYOh96zfx6EPaFtyaOgT8TH/Q944v8d4AntitODu0D/exj4h66L9iHhH/Qu4P+BP/wF8Af6X8+E'
        b'HIPAMAY9gPWuvpg3fbk+8AEsxgJ/DatvxwEHXMdsBZ7CXCiJL8r4xkBNcRy27dpO+cm/vLkmbtkT7zz5xpPvPvnWk+89+dqTHzx55cVf9h0pGr6rYefIo9U7lXmXl5zI'
        b'Gr2rurwh133XcMZivj3JzOOleUoDHsK6B8qJ9nF0jSaQlkXRzu7Dj1YPD5qgDxwgw93deDNzWuEVPDGmR/r98inzDOEw90xdhQo47xdtqst5xyN+PDr6IhyxVQRie4/0'
        b'fqMhsdrQz/9IPrx+soROefHzeZwqjWCV3dOjgzxy0vuAh1GAhr73UArQo2S+ZyklgSqQaBUyPVnvc0jLeNZ7j5p0Ke8jetnmeqS5y+8flRtt2G1JKLTLghIEZxt2U9IU'
        b'VE2LU2iUNEOmpBkRJc2QKWlGTDEz3GoU2ukz53b/6HF9Str9k9c7m47/T2Sud4X10mg+mnTu9WSvoHm1/0tm/18yu93/ktn/l8z+4GR2p171owSyC3RmNnuk3Pb7iIz/'
        b'y9z2/2pGtlSvAmgVyKKAR8dDqzYjW97fJUU0D3Tk6F6MDnQfFPhwfKFQb8wN0sJzeftiASMWW0yhsWjqqcwY2wQohjxjuLIqkUNhV0WO7UAA06VYT1lLAcCa8TTncKjC'
        b'bKij2d1QMlODIAZFjmnUlQMU3+qo7uy6N3guUYASPIZ7goyxfeYixjqfgufgYEcWKeZ4O/E8DszRsbOuGmuEu6Fu9mCrNKqcmOMOKPFz8Q2x7KL90oxYJywM4JFeIQpD'
        b'LPCEPWme5InZmDdfx/YavnCx86LFNKvXN8AfqsO84YJ3gIuzTwBNx92N5a4iXFSMg7yQUGEoVJgnwBF31v9peElKmTSwbiYl04CWJDifNk5gZKotUd2KxzJSVI7TouRx'
        b'KpqiytLFZUIE5BlCWXAqe/OZk8RQdmuOk3aswvjt2hfHEjtheZwhnArDRj4EJXgQ6xQqc3riSXpT2kcyYzKc4KHdB6AN9mAjtmSQd1PTlJLrEkcTdxZIbywaTBEkloLg'
        b'GWHqMz1DiN98LkFUP0Wu7A82Ct87I/QTqx2eprtKVuxftetlULyzSdy0bt2V/Kd8M9u8DQom3OqXHNo40izgx+Lvr76YFVo4IO4zhTz4ss1dsyH9vbzXhvetX/mzyZ/v'
        b'LTi5+o6d10jTmy62S+1+euO7EaPMs5om9i38su6iD8TNG9w2Nexy+TtL3ks7FnJ7td+YjKRxqz9+Nqh+tMmOyVcm2b/t/Z3n5U8H3bLZfCxp8rnHHH+ur1rw64noL85W'
        b'WB9OrPxq3e3iop+WOtus+33SJwf7TqpaVjItZu8wMwuvwb/MV1ryaL6zWB/XDRJssDQB9kl4rGAuHKaIX0FYmAg7dDzdDGvsFNSzg90luH8Dzfk0hzqGNTZak5AZipeh'
        b'lCVk0rAWDSM2S8iEnY7sQHlif9jfBW9slD03SRRJ7EA5DEoT2SSBxgka0mFKOBzrwSOYitwd2cnxAtjFbZ1ji/k59t4UPETWhy9e7hS3hrUxcJUFHxksj9TG0uoCadPg'
        b'sCaWdgpsZ8bW8JnjeTYpXaK5xJwyxzbpKKzxD8dc5g1eTTqmhhIeQ46SxsEwwuNabOSG3nmsggt+43xFrAoiK79OwJa10MDP8Stn407qRybdU6CLbtwGR9mITLRb5Ogb'
        b'wEeEtLzv2K14WYqHsdKRvbWNS78O23FCuugG59xSx5ILfYjUOezn79M1/3Kvf6cUTGiH9p5Uc4r/YAKk/wOMP5NkmgZJOX5pKqNcTg+IrdnRtzk7ijZnf8kdmnTGTcO6'
        b'2016sxaNHyZrsSNh0aD3U37D3llv9SQnej2M5WlXp8fyfNB7/RfzE1crpbdXPDA/UZ/J9peSE+mJRc/kxJGa5MTjeCjyEZITZ0FhR36iDVzYlEbPJ7AET2zWohCMd4N6'
        b'AaonR82dIVUII/C8lJIhzeGbQQucgQNqzPLvBF5pZccPkC5BuQ2WzF5Jcw9Z5iHZ2veyreD9MJHxeNWv2+L03ORoTtOFNU5YNR73jU/BXbrUQv81LG8PDpE6C7Ckryln'
        b'slo8mlURMxyq1CkSUtNh8nwhla6VcJojjR6CZpWj0mGkUptW+Fg/Vs2qxXCE5xRS74+BQJMKl2Ahx4gvx2Owh2YVLknVJBWGr2E7W9+BWBCKZeOxwkaXUwhXMZcnj10g'
        b'j50myssquSYFEK8tSaMi2xIbsCoUc0I0uX6dEv1c17Cu+DN+r2ArEQZYxqYlVqxbwVPcXlg1UphH/vV8LDHqxYEi//KNIG/G4Fq/Js73WHL6v5foF/dw6WFXqL+FpYdR'
        b'n4ffZDypIStxIhI1xScA9zhhkSasCIuhkQKa0Eg+JTRLxxH9JRqb/KAYG9UK0mNzMccijAj0Szy3z9tMID1rn6xc7fTyMFv+jurQ/oIT6bZKm21bnvJx4rl965xBX17f'
        b'UjglDVqF5WwIIjHTVYHNKXAWijT5e4kBrEiHYENOCZeQ6n8j3kBQStj8iCcb7lU17JrOInZpuO5kz3+rR9c8XI9KjbQ9Sps9fPBCRTrZZxqwTZNwB/lRfDVUkJW1Q6GS'
        b'wkXM0mTcwelxbNr3M7Qh/XEtmWXdaVLusselWdLHWlauUthQwJ5gIRiLjFlZfjbYrs24w4seNOluGZyYyVJf52M15Gny7Vb3lQg83U4K++I3n31Lqt5O1tvmCt+0sGcS'
        b'rWdbfvtdecAHKU9sv3VDXpL/3EFb/+bnPBb0HTz46Zvu66JTvvzoiR0DzL1fsKgcOCrQ2/Y3xVYht+/YWts+3na3zm3q966d+cQV34e/mXr27SGXg5tHPPPjJ3Ne2LPF'
        b'qeq8a/Sp8BFzi26bb4mPeeXld151qX+t/JXck/PXfznfpE/LiGOKkS8MHrH8wKuX533l72M3MnpcZPrJAblTFC+MHhFZeCJy0vO/5J0bNMBCPab/F337fF4Q/eNgry+F'
        b'/tsVT080iHg75pP/j7j3gIvy2P6Hn312FxZ2pYOggoCK9CIqChYsKLAUlWanSBGlCAuIigVBqSJVEQVFUCkK0kQpmpzxJjG9mMSY3hPTe2Is75RlAUtucu/vf1/9ADv7'
        b'PNPPzJwz53zPcb/+2u45FT99pa/RvuDzbQlXz/rHhI9dkpe+bu8v2y0zuV01jjVZRd5HlkbU9MRpXn3iuNZRwdHmH9xiV0s+DO9a8U7hEd/4XzZ/n/h74cW5L2xqOHtV'
        b'fMvzva8zS5K8v3KPVJS5vHT8uLfZWNH8JxymW/7+xEVpQ/7YVeHSd38PrtpYa/n71bVuS3SdLsz76KdS/90fhT/hFLnL5vf4Q+q9z7+4aPbKb36Li1p2K3buXZ+6Pz69'
        b'+4VXuY/BtLAnQiE0pTHvDT+Ps8+eEHy96fzmJ5Z/tvqG+6TWznfEyXMTcs694vqzn4di7xcbJ3aNL+t9/YP5Mc++Ez275Dc+ue3DsgkvG63OSfpQvzvujda4Hy7OWPfu'
        b'hdVGbyZ+fkPrRsDb5xaf6jH7OTgu9eWyCbOMjCa9aXB3nWHzmjzD0B9LX44x3B551zug6OVJz99sdUs/2/Tu+Xkr51vuyDw0+P2vka87bdtZ+OvEgfpdP21Mdw0RNv34'
        b'W8OtPbtLr2xO+1Jc+77FjcgbuueX3t1wL+Xe/QKD2mON1UGNb4t6x3S8Vv35pIuujZbwjkXLkxoHd362vnlP0murvg0cZ3P/ZNfEPzdtfP/9JuFMMP3dx7Tpw/tpH6x1'
        b'f3/5CoeDUueXprSuyXz3+fSypTd7NnZm6HYo0iqW3sYfd+m+Jdf87JlwzQuK1eJJ31luvnhg+vNl18bNC3/Neen2r81uXNnzrMZix3tvvbBveoZG2dMRTkHfSc78aea8'
        b'PqTq/Sf7+X7NfrX+F50Weby5PVPDY0uJbab41/11te8dPPrUhn3XJ/1otHL8q6dbWl75zbO3OGSTS5le7aX5aVe022+ceNF8pqh/zN13PjT8vSyoI87T6VDF5cCfQy81'
        b'z7/zUtGrOV2bT3UJ+zwsWgJejnwp9/vrxeUvK7aMD/7jzLdXb+768lLPvUVvB1x64q3fWl5sCuvffFX91DjtgxnfvPyebeF3Zn3mXrlbB/YOHvGbU54fdPL7T9wsPT8N'
        b'9zxok0wNjIO2wmHpTNT7IKc9BFk7gi4y8197CxVgTYD6mLdjuLCEMuEZUIb6RzkJhmZdileb50V5fTkMQot8ridFrI2Aq42BfGr26oBOG1CUmQpjBvuxuEBwZsZI6UY4'
        b'Z6mhEmgGfahZwFGg2UbMrCsVJ51YhE+ZOcykKGFmqCUljbja1ZKiAiXOzMYXnzK2WMC5TJFbDGnmAblq0LVlDa1MARe0lHgYvCfuw5WF87aQgy7QsVgOl12VmDJ0BKpI'
        b'Uw7yU/T06MMdWJTNHwKVJcEgxZVtm6/OZJ7OuDXDkDLM5xRQWFmgC+qg4zDXBe/OqBqzNMp3RiDKNiRTycJFfREJri5EXUNwskwDKsvE+aOTKjiZjzUBlIXBIRMGezgm'
        b'DH8ASqYD51HdImHaBFTIIhpCITQyNBn0QR+WvwiazBw6mSH2gAPkKfFk6RtViDIsXfZlMVBGC+TDHoYoM1OoMGWoKGsHbYE3KjeUokrUSiFlo/BkFWiAzfAANGmq8GCo'
        b'UYtAwtYswUczw9HB0WmKAAE+1w4pMWHQp0vLtkN7jB4Eheka6S4TkljnDKaYBlVwlApzPShHJczBMbhCB9Vq4zxpgIPMJiwZ9xsaBKgtNpqFgs+GAtSCiqDejGFGRuBF'
        b'ErAoSJ1u1KOCBQ+DzfAReEEEp8PQOeUAYSG+QgHnbSnqTIU5i4J2Wso0vPo6pRYBBHNG484X2DDYmZlIBB1O6Bij81aoRa1yuIAuUYjZMMAMXVyp9NxjH2W3Bp2gILMR'
        b'ALOEdXQYl4RQ7AqqQTUqGIJiNTN5r81EDF+mho4yfBm6oARGZWybxq6yxPJhSX0symMZ6+csQUV47cJF2yFsWQIqYZNaGDLk7GjphiFsmWEU3lXoehhAp6GBIct2o0YV'
        b'uKyfF9KSE8RQoMSVoUY1Ci2rjkCNtKMWaFCkwpXhRZdHsGXxkAsX6GPjGbF47eI1S8BlI6BlMl9acjS6kEChZeqojfAnBFumiXJpqyJXoewhbBlk64o5hi3Dw1HJSLHE'
        b'S4T7ZB+I2lXosq0sUimqRftRPl4GG3DHVPAyK1TKQDn5u9BFii4TQbcSYIbOOI9jdvmFcAGaFPY7KIBkCAiyAbIphbpv30DBZcXpSmzZejhIOxKFsvEukZaaBedU0LJp'
        b'6JASlzchkd6cFiwehpaNxXsNdT7fHTpZsWyVilNFJ6awORlEF33k9g6jb5sSMGnksXYOusM5ildBeZpKoAu0jMM7OXWBBQMcBZaNhJXB2elKZJkhnGRwlByR2aNQZagX'
        b'jots4wV0Ch3x+uwcQpZtF+Nporiyw9DP1Oht6IpAjk5uYf661gucoNeOAXEaFWhAiSwjDjMIsAzvH3n0oQaqA/x8Dxyl8DKGLVsP9axzreuhCTOuqMB29zCy7Cx006wr'
        b'V6CyIWgZH0LBZbOhHh9BdKsoGT+RDIsmXibkprMHd8gYnY91FtlhMtrHGnYA5UxSMc0XN1GmeR0mOzIhcCkLlctX+qisArxc6JqXQNtuKSsUiqJRDwE8akI5D2dR30Q2'
        b'zwegSCqlCJlIlC8i0qclXrp72QUYavFlyB983nQqIW3aBlFs7zq2EfIU46PZkaihgrOZeoigDPpRD7t+PBUCPUpAG6qSkvVCAG1wbhFDnGjuVqLZoAuqVYg2uLxkBWte'
        b'KxzEzSmCbtRJ8SwUz3Y6mLWgF7XbEzzbCCzbSlSohLNtQN2U/I3i0BG5g6+n8xCUDZ3VoINjAKUET4OOZVEA2gj4mR5qZVtmBapdPAw+Q4VQzgBoVRmoj97JLYLTcHAI'
        b'e7YaFfnbPww9c8cHIT1JD6F8W4VquIgwvhfPaqMwDWWjbBpbwRedxPtaF+F1NFChjY8SXWQC2Xg3qhYtxcJqPzsSandhIqQvkl7DYT/MDRzjF6zEK40+bybXAVCktixw'
        b'2PSFAM6M9dih3DsHapTX83h0m1VXr6hGg25U66BZTq8+Wxi3QO4+rd3plKaMSVLgWgMxYR20w9uuzjaUrSPM0gcGmzfB66PIDlMi5sn8sTA4BQ/ZEX6HMIsOggDze9kK'
        b'4hq0gHBIpH8CTtcQznoId06YkuZCprXcFp0bAuH5Rf0lDM8JavDyIz3ermE8CsWmiy5MGieERnRcwiipCg5OpqjWlBVKXCs0b0VtlEaECyzwo0nQqUJOT9pMc0nSXRQw'
        b'4EbBsEOwXbx5tNLJR5dRIyq3G9m2MNgzGmXXhpoZrRZilrF6FEhQF3XDCXRKiCmyBVjoj0nuqMxOF51VMgOjkXaoYSndvBzj8T7ggAacVUg7K3y60Fm/AvW2w1A7N3SF'
        b'oO2Wo364zE7bVji+Ax980LBwGGtXksoUAcVT5tM9aAhoh3nJQSXYzhdOUWS9RLRRasOhS8YMa7ce9rOAJobrRgHtdDahZh8hFKJcGRv6brzPoS57R68wFdIO89y97JK/'
        b'Fh+FdVIBVBO4HYHauS6nY7EDHYRLjwLaQdFUkft8VzoWqzw8KdBuMj4sOQK0g4twiJ1F5yPwdjwEtUM5CynaDg5BlxJCfMI0Yghqh86spGg7by9UxjihGrQPWpVYOzV0'
        b'CG9bBGo3EcopEVvgDW4fwdoNA+0svBnUTh8V0KE2dU2kOLvl6JgKalfpKKDZk9zROcxftOH9i2LtRgDtUJ4Wbd34HdDIAp+E4W1RibNbABV0Gsalon45qhQQrB1B2pnr'
        b'0DzmcrRnCFGnDsXK0ODqBjZa/3sAHYU3UYVB6F+g55QYOhOGodMRiISPQ89JHkDPiagiQZNg0+7oqIlofnOBOW+M/477G2g5ibpIiV+TKTFs/D2CbePvq93QnPkgfo6/'
        b'pyfSoTg3Ea2ZKDRIKcYSI3Lhz9uzcnEJIrX/Ejl3nf9dc/FI5Jzx45FzRg+qGP5L2Fw+UXYQ5e1fKTu4bKOvHqHueExbcAsIyCD10yHknJAg514VKK8hbfT/d4i367jS'
        b'DwkwMIn7v0K8qd3g7bQEEvEIdNvUYXQb+874vtmCdOo257TX0uHLasyB9SgvrAWcNVwRJ0K15CHDVy3lX8Xeh2Btq0WV6pUalfqxPPldqaX8bKD8q8n+xgtjhdHCA3y0'
        b'rUqjRELdyPLG5Gnl6dBo1TICj6MwMnGMWrRatHouR6J1H+BXq+O0Jk1LaVqC0zKaHkPTGjitRdPaNK2J0zo0rUvTUpzWo2l9mpbhtAFNG9L0GJw2oumxNK2F08Y0bULT'
        b'2jg9jqbH07QOTk+gaVOa1sVpM5qeSNN6OG1O0xY0rY/TljQ9iaYN8sSxAiU4zpB+JpG/JauNqNWkkGrbJHlSPDbaeGx06dhYR9vgN8ZGsxt1u5uyRQv8g4dC2394gX/A'
        b'UpKYKo18g+HoVIY2ackkzoOCvTNjmj3760qjIpBP00cVNqSVUziaLxhhA6g0aaNgAKXhHH6aFpNKgzYkZ5BQtGmjbfhGBnCwN4+J3LDRPDVmS2qMIiZpRBEjjAyJheqo'
        b'Eh5nxTNaNzgqEZBMjLd8Ys1pDFaF+daY1BhzRXpUYjw1R4pPGoGxoPZR+HEk/knbmBozuvLEmLSNydHU7By3OTkhI4ZqMdPJDpOwjdhZjYpQYe4VT02WrBfYKO1uE0Yb'
        b'chF7J6UpIJsIJ+U8DI24vbn1Qpuh1yLNFTHEJC0t5q8micyh9SIbAsyIHGH2pzS4S06Nj4tPikwgCAElthgPAUE/PNBRhSIyjmJDYlgkDvwW6715dMwWvKUqzJNZw6nt'
        b'nrXy2UJCYYnJitEmXBuSExOJfTGlvQfsBANs+JvCzMSEm2obIhPTZkzfIByx7YiVWw9VNQXgX0rUl3reUKwsKd1CBHgT4WO1lOppYb5aDrdTtF0jS0jV0yKqkhbuEgWN'
        b'+Kw0Mb4t+Bs4sFEL6fHWYo8zIMS9Y7aDK/39lMZvNCwKLXd43vAMUQNRvCwfbVVqHcPI6XFr9i/wSXRo3QnMZEMkXvURuEkRzIiPFaYqZCTpPSZYTWR0dDwz+VTWO4r0'
        b'CJGmpMcol68iHa8r1fbxaFzGKMNYFoOGrL7I9LTkxMi0+A2UWBNjUuNGRJh5DMIjFa/KLclJ0WSE2Zr+64gxo865MUqCG20+YBqgIBK4j7y665Xf7Gxa0myu2VwQPltk'
        b'80ZntoKL3yk5tfvPn0h2av2GeqB1K3ShMtRLvFClYZnBBi6gOtQARTboEBY2WCY4BcXplEsNpkpX7/loAFpx7bs41AgXdpGbEqqkRe68JeY88acIe11DZ44p/RuNeejC'
        b'W74HB/mowmPNmoTf79+/b6kjDnbhqR2Z3/1NVkrPxIex6DdIvSijSteVYmeeE88WLPOA8zY8NWmYGbRNgQq1UMFWplnw04CKAEcNW2sBNw1Vqtlh8beSKleDaDeyoVxK'
        b'nvH+Ajc4hlpxKdST3JWN5LpqqJzcJbgoTVKegLN0F1tClS0ziyhGB9BeKXsgRH0CSTo0R0pxIcSDjusmfzi/cVRrfGyxFI067HzkjkTDEYqqJRNmGrOetaJK4hHVzicC'
        b'KtljyQw+CdXo2gipL2EsueRAPgnM4YDKXJ1n8JxsJy+Ars1Q6UV9qpqhA4uGH6txsl08DKLshLXoMK3Bi8scfizgZLt56EEXEtHxBNrcxevRYRY7xDvYm7y33Huk6max'
        b'tjrsgcKxMzypGSec94bDWIzcDGcxVSx3QBeoHKkPJUI4vhX1UUMCPJ2NniOtVIbCpaACP7ncgU+ZC7UT0CAUYpms3xB1ok65ARTKpZokYILviiAuJlbHzQ3qKO1MdRKv'
        b'Py6k9GDfq5jJpa8hBFWlhvpG1GCM2kaEwjng5BtijQq8UXEQMYyUh6DzKjqmRjKBPmK9KZpYKD0lFqNLXlOg2Ybz2mqAaqFlMx52Qidr0P4FqEt7SyomEnRRYG9hRYIT'
        b'UcJFR8fpSCUEVIMFGOlM21gT5v/3COSuRl2yFJrlrGA+qp8cIWaPSg1QuWILveEVygSob3WEJR4rakZTLoIWRQrqlJFcewQm0DR52SRlGFsY1CaOuS7QIon3rQNrjNBh'
        b'D+bUuh6VTR9RHQxC32TcpQpKFNCI+sY9MO0LIScRqvzTiRMNOLgNDghRx8jIMf4OvoEh3qo8ygGFPaiLw8QihSY4C4PpTnSDkGzCS/3MQ7mXOYSyXBwq56LRRQkHBehU'
        b'fMUPv4kURES593tvYrlHsv4Cnae3fvfGb79++s1VC0+JtjD7A9EWs4w9fEH53kM6mLlcJQ+9s2dT74c16Z8Xajb27+WXf29y4vTS7zWsJ72ybFr/5Vki66Tkz+bff+uP'
        b'b96zWWpYVbuy9qTmCt7APuT5r3d1fFrzjtrM5w1vLfO29xEt/9DRMHdN85iAJU866BfPKb7T2eZimHrIqLPhhuDHvWkXDtxaWPqKd9gEicVey6vJCT5i/8Hid6Z6yA86'
        b'xPusufF7bOfLP4l1ZV/+6r/V/GxxxtbcU1vntfhEWb7w2bJXbbsn/rzQWP6F3QvGPmEXB57Z8LWxfknspx9bHX2my8dsYtOcumlV8Z9ueEl2UL9wlcbHq34eMN0esdbA'
        b'VzR4c/bh36pSXtr2c9adSfOrXlplHH/mD5NdRuuOB1oXPZWe1Ojww09LLjmvcKy5o3fxYmhuTm+31dwPv7R5dezlI3eE7/+x+PLL3R55g885R377xMdh5ycdyk71eqLd'
        b'ysDqaIKnh4Fp0M1X7jUvXJIp/uoL/y/cO55JOnV33axZySbfRT2TciD88457wmXrXFqSr4+f1FPjEZby3iGZ1zNv/u6/S/rVa04aASKvZf0vbBgEvyPVbeNiv/rCZobD'
        b'z3Om28/43m2G15jArmkn3j0zy+mT8VkVTwu3f3/1qufb45+efrtVe+MOk593h3yVaON0Zo3/xoX364/MmD7xnjxo/oKfbr58XVHj/mpw2Wd3NWq27n4lWFFTUt/83Vc9'
        b'9T8fuA/3vpm+51Jx1K/NW9WfvX2vqqEa1l+/bH3ovRe8j/csbNhue7Mr7dSfIR1x3S8ZoNfsn/VerjsleIml+3sdO/I9XvzKZPW7Xb5Xs+5LqtRsfxuXeetXN/OD+bvu'
        b'fH5FkJgm2e1TYrOA3ouJnOahKqGdoz+PF1KTQI6KoIPpPxqWkEt7aCf7Bt5QUO9aVMhzUhjAiyoTOplzq/NwEp3Hu+opOx8/dRKRRDA33IrebVmjc4bQgAZUrleZ29Vz'
        b'iHkigxpo1hVHQZET88ypFsFbohzUzx5enomqdqSTaEROgcRCdRdvC2VQnUasJncQgyDU7oyzEkWqnyMUBDKlcL6Tt70thWeqc+H4FD63BJ2id8UZ/pz8AcW+HzofN2M+'
        b'fRoOPXAUHcbHXREu5oCDGqe2np+ETpjTGzZey10e6OBjb2NLTkPc/24eDZhGMKRlXiz02Dn6+KKTD3jBXYZ7Qt6Qoot2xDIZnZ/6AFoSdU6ifY1BB2Gvwsk2CgqH/XF5'
        b'L7Kh944265M8I1W+uOjloNiEZnNDvTI7HziHz2pRnAD24dz7UR7spbfAelA4ndxsD98cwmV0BJcwDh0TpRigCjr16LT6eKL70odipcZugT61uEiQYy6lyMnXX+7gC8cg'
        b'Dw9dgNLP12TcAA8PVMc89LagRnLLfsCHTIRcKwCVQ5MD6pbznNkSEZxCZeb0jtTRBOqJ9vugRgB7OsaLX4Nq0KWxu2lzndDeebi+AAd7f1KVBbQqazN3EaFTlphiKENQ'
        b'IRAwn2KQl6S664QzqI8pUfZhfmEvFAU6+vrb+/gLOK2NQuiH/bOgDk4x1Gvp+PHsold5yTtmhhB1oQJ1KNWmNSwPQ03QvpvqBIrxSlDn1DR4GV4BHZQSNmJaP66g9/PC'
        b'zQLM4/VkYU7wMKUhW5SH/3cNO89ERzeOx/R7Zsgh2n7IoUo7pcpuKeRDHT5WjzM6asKsV+N6ooHC/aZONsWoBh+H+AG7Ukd74RyckzrK6c12i0BjDRy3gZN0+KDIzJUq'
        b'NEO0H+EpE/U4Mr3vIFRAN+qGY4oRWkXICaALeec8uAL7Zql8XRJ9pEsWUzge9AonqieiwhSiowI8eM1QMg3YBbQU1S4nHTtoRxrWJZg6A86shLNM/XnWX0a19TNQI9PW'
        b'Q741zTUe8wobY4fsaYj6uo8XrLJgcc/xEX2ZhAtQqBS/SybRC21PtGczmeAhtS9RnoswsbcJUdE45ukR5QTi+SYwA7gwTenKEWp4KNiMJ4fQLKrNQE0jrfYDoHGkOdEW'
        b'tJ/djKNG3B07pQfWHsHCcGiD46idzmcCOgMd7CnlndQ4rWihnsQL8hPTiD+wTXghdERGQ9HWDNQ9JmWYHSNYbCdU4u3vgPMEeUm0ZDI6HmuToV1hp4ln+SjmjW0EnPpO'
        b'fvruGDZx5YvQZYVdKlxEjcyfnnoMPw01zKTbtPV2VIz76wO1qIVohgJpTD4xZ4haRLpwcDztTBoaXCDFBbv7KAuAFn4u5GhS4puNpZp8UgTJjilUndMKEML+JE+8HRfQ'
        b'jcItdo2GSOFL/FMLUK9Ah7jBYUqVfjRgL7XhNkUyTQ0cgipaZhg6bzNCVwN7iZU0dYuI6nZSVbI4BQsUAQJHdFlpKuO+jRKiOy68F1qlzI8nceKJe7YnjfrsqoE6CW4o'
        b'bogPXp9Qhc7RbcnJGx0QcpPQabEbOqzPyKDMD9UrAmyIERVZ6+kwKOB0TIXLJ8Ie2nJnGJygsMHSAqpQekf22KLUf8OV8Qo2TELYJ0AV0LxdE1WyhwVzd9r5OsgdbAPw'
        b'BqMdJ0TnoD9y+2xKWStQv3S4dUyphs+vADHexcXTV8LRwJVpBNNugqrdCGUkw8GHiSNwJmZJPaBNLQCamIfh1eikzG7Ye3XoZJQTlapcDm1ov5Q8YgcL1M4g2r4+IZxD'
        b'R72ZWrwdtWvbEbuXwWk2/vhkk6B+HsrQAU86TTvRAY7ol9yiHnTliPon2oz571U5/0cqoUe5BwD8668VPtxuzRgdgRavKVATTBDImIqFpxfqd3XEEqr8UBNoUkUJ/6dE'
        b'nXzWEozDPxMEkwVWAj1leCyJwJgqhXSoKsUIf2eE/2vxeuQ3/i8RmBFFy201idEjvlPDdWhRx4ykBDUlRoU4ZRT9IlLfbjjy9mm0zwIbMUOJfE3UGN+MRp7I/qtpEbLi'
        b'hktXDa2PROln6691M1y2VfMjtDOP7szf8oEQ+299IJwjFuTUB8LoalQOEFyGbsXptbK9eUyco7ktuRtzdJ7hOuSg5WF/CH+reRtJ87b/VfPODzXv9njSDuUVq3l89Kga'
        b'/3ZlzYKbkvAN7O79sXV2qeq0oOBlitiNNafZCAT/H9cch2u2EdwcE666WQ6Pf3z1F1TVWy0wT0+KT0mPeQRS/5+2IZe1QRY+dNP4V024pGqCLRkBRRoeAnpXqbqm/G+a'
        b'kWr5VzM+oKrbMSiZuAVKik2m3g7MI6OS09NGeRn65/XTBUGcxjy2/iujKW6E15v/iOJSvf+qMlBVNm64soU+i/4zGkuV/1Vd/xqqK9Wf+5vrk85WyV8V+oyqA9bBj/BV'
        b'NOSB4z9dMprUiUA4gfQ/tgnPjZ4w6geALdr/iDpsyBZBa01LfmydL6rqNFH6jPgPa8wd2hqiIhOIgiQ8eUtM0mOrfUVV7SxSLXmX3donjFT9Pehk5D8jXNwqLVWrNiQk'
        b'K2Ie26zro5tFXv6vmvV/4Z4y7lHuKQXcg5oKYUC816mzQgXhCfUWuBM/k5KtstgP/IScJF/Qc6fRRsBY3+PTCdB6DFwMHDLIYxIQqkp+jH9JlyEjGqIw+Hc8FbdbLW67'
        b'wQMHfUJM0pCjpUd5lyQVvEk4C+LE+N9xFly2rOYRvMUjq/z/azJEAcHxk8d2cgrydbfbnVfj5JFkLtQ5kbXAZqf1MO09PNoXODbaqSWCh3iZ8PCo5OSEvxpKkvvmPxjK'
        b'w3+DTWN1jhpL0mZSMw31RFWzwy45h3xAMfWsIG+MSjXL54vxKAvxKPN0lIV0ZPldwqARnx81ykR7QIItuo4aZfMAetlvhgZsFQlwYVgXMJnYCVOl2A5/EYdHw9xZ7dKa'
        b'1/UdWDg/OBqOzivQuW1aqRokw0mBYzg0MKBltJi9n5Gh/a14BUdv7T2wGFdAr04YRJ+4syiW4w8BxMPFimUrHPygNJTn1nuqQ/2cMKpX2wRt6+SzUIUvueiHEnZZRm6v'
        b'xJztBjG0olK0nzVmvys6rEBHYlRajogFcIxqsFAVHIOOkVEnoCKZ2v1u0aWqjDlBQEKBnIQ9yvsokYMAzsWgTqYEqcWybbvdJsgejiEKjdNZPMFDqC5ZKaqmQSUR3bG4'
        b'GgPF6EowzRwER2eT7to4+Ig4DSE6qc5DydqdtMmpkZvl0AatFLohEgngOLoEjQyemWeJLhAclQ0WJjUMfGbzcGoKMBSxn9dUPBTt0DIcRyrLgKKIFSgfBlGRQwAVMNXW'
        b'oRIP3nAnFFFX3LDPI0oOZXi38iHO9fxQER135m7Abq4YHcDTc/gh6pQOUaf3MHWOpk2ByivZ36XL3AfpkoyGxkN06RjAaM+C0h43xTvCz2b+ZEZ76PQuqFaoImig3mQo'
        b'2aVPZxN64CS0KYbjJh0NwyJ3G/RQbSTqg2ZeOWN4uhaj/XTGUH0oI6N9qBVlq24fUcnuLNSpzmDYx6AGjir8VkC3EyZ3icDUANXS4JorI6BVjgrNVyrRB6hEm7WkfIEf'
        b'81fDIBfzoQOOoj50lHkzaZyD+ilaRgmVKTGAkzvhIM0q8BCQsLn1u0dGYjJElyKoupuGv4QKR8gP4nbgsbHgLKBrso2Y9nAxNEA2zgzl60dlnhRDScsCLw/5iHBINU7Q'
        b'BxVTaNYJvgF2wzAZGOAZUmYbdNFGrVmKakcEd0LHUCFUQw26kk7uSYzSUaEdrtARLxNHGwdf6JT4CzhL2CeenY6O09GdPkEu95uHDg9HVUJnZpjSZqXjldAnRXt2M5tq'
        b'TL4SfmxyejoJDAfdqAcu2T3CahxypzHL7PA45m++DA6i89R834/eLpOdBQrJekD7UD9nFSbevHQ29U0TYQj9RPMxHBlmHAWYj7ZKD4BsdVS6xY42fz60RwxrUXH20ghU'
        b'ZEaR+Hgc6mY8GNgmOxqq4BDehahu/4StnfzR29gEHlrT0CAd4xlQjue9aHgj0poK56AJGhh51sbAXvlQHB9r2AsNu9EAfZRsmkQs/Jl1/yrUjvfGvVDOKK3cC1pQ0VzY'
        b'r9oaeMNQtIcaTYStgwsER8j2Ei0FNI+RUHpPhp4JmHoFa6CHE8zicKv6lPGWJXA03o7GDBJFCnB7y1E2OoOKGM13Q4kQ05e3gz0NaHiIR8VpWU6ol2LtvVOgxG6UOTzK'
        b'TxqyiJeGsdY2r0AVdtaaY0YEXtL2QZWUFNZFQa78sVtYPybGA1E7bHha0BZUGANFqBPOo9IMESdATRxuZnsAi7p8YSKqUqAONbwe28gZwUEpqsN7JRkTH108XhVqqAnK'
        b'OM6es4dC2EfPtcgZUg6/kNmuH5Ew1moR8yqg4SQkW+VG0ZgI+6SQLezLg1l011r2XGCE3z1LG/blBLGMOCUw/yE4wk8yfSX7cqOPhNPB9Bi5OcJeSyB92PEC5RnJzzjK'
        b'imRx69R3CrIEW9SjuVC8qabw0Sp5j7JCyoDKgowHWPObGnPiYpJiMrekzovRUG60/B4jLn0V/mC3CA0oHrhGx6uJ+je193HAI3AQHR7lgQFVCFEXVOjJodxVJ2omaobm'
        b'bdBsKN4+1ysDr4flxInAYaikfkOW4iV8jGjq8T5ciRdmhYOjD/UA5bt8mUOo9yMmFLp4TQFB0bXIItApH2r8sRLVquOt28YBFY5QHplumBAigrNidC7+uTvPc4pruMMr'
        b'zeQxQZeS3vbUeXddoZ7NrXkJr/2287Pu2gYd2dhvV4gFe6cvKbSPzhQbd+aKJM5rRBlPWu3v655cauVfahmuaz6xdL53rdMzX9u/8EyKxQ+DbskltVPmn2/KvLrko8ym'
        b'VZVFq2D6wTnXdkS9XLlQ+uXGz+3z7vNHhH4ptUJHhcV4Rwv9HOEz2aXfTpYeSQ0OuHR3cLyv2e62jCcPaLa87LpLPfeJZ4NfWBRXd+yybdS3P93v9rx049zLkb19aclb'
        b'F5yJq22qCjZZlxwUerrpuJedu/a2kCk9NyKn+o0tfbPkRkrIjg8iP6uSfbQd1I6f0HErLt/y4osN+UeKS+v7C97a9vqKNvt/JS7Wr/7FSy3fSndn1YKwye9c/2L3YZlm'
        b'551X0lqrTaINRf5JZ+64nL7hs/mtxrp1JTXPBoQFKmo73nl/Q+ELiSeKmpf5tx65N3Gx60313VfVt31ftblO102S9ZbsrX35A4dmBxV1xqbrFm568ffb6cFv1xf02MwM'
        b'vGX/o8aKqcscWsS3Zvtkln1v8OGU1O8stK+Zlvf53RL8GL/ijM+6+gETaM2N02jXrWv49qtNOakHNZJXRNdZrnGf5dJjVCretOabJo/fn6o6kRu3M/nn0g/HHHrev9pj'
        b'8kvrBr7sdIxb/s476VlXX5qx/duyhvLZtm4TwsqSJ42d883z13f2NLcu8//8zv7blrUpHcjerOBJ1+L5T7jFflkb0/i09qepkO6QWp/x5Ke+2h6yXQsckp554ufxb+bN'
        b'r7cKc4lzczGcE735mV+fOpIuiawzRW+4vznjjR1w+6Odd1796stzhfXq6TsaVjl97DH9+eu3zzS+m3gFdf+Z9NTMhVbCjyd8uybDtCjrkk2vY0rNpLNL1qDBY+Ll83ZN'
        b'7v0m9OuZenlHEzXf3bN/u9/bBnfDcn94I13/Ff2sCycK1r3nKW09vlB/9brsPzwyed3Z63YVetx/vv1ikjDn16/OvLzr2vd/pk/e8eSd5678nuPycWeNzWwGNK1LVSfg'
        b'WWgSkV0aZa+EgbUWTBBtTJBICbpMwxqz0phd1IUzQujyg2ObGcDLDvVCvdTWBnWygF3jeRk6HwpnoYSqaCKwGFtKFJnreaV62iKRamFWQ/2UkarWRdA/Hq/HaqpJE2F2'
        b'cd8IxfheNbQf7dlJK9yGutHJkVrYuXAa6iAPnaHlrpqALozkitRQORyFi35U5bcT5bnT3qT4OdmoBUAfNwa/Z4X2wHGqhzPcMPshUKk+PqCYEnbdZjZa/WiPiwJ16kOu'
        b'SgNr5MdiUK6HPIUDMfkaVsBCMbDoY+tRT5TUeiXe9jFvxAcL5sGVXazAUyjfmqpYzVAfU7FqoDKqNhy/Syi1xh3qGhUTs59jUS3RUQ9oUgwHmJSgSsydnVI6O4ABvMP2'
        b'Kfyw5NFLpgdvfHIxpynj4UQAOsdCGELHQjvonE80//YcpwZneddU3C3yzG1b8qiYtagR9W6zXMqC2JVDH2qR4rktU8XGZOBldB4KWKfKN1lLI8eyqJoM9zwHnaCjNM9Y'
        b'iAeZOAjAcySaLYCWTdBBHJ5RKUMK7aPCeEbBkXgXGGDWA6chZ5kCFfr4oF45z6mn8OhEmC0+Gy4yJfcpKJkzMjo7ZhcOrY6Ecjr5+nAoSYGrRPsdUpi+VzOMx9xpO3TS'
        b'3JlBflLUGAHNW6jWUgw1AsznlOKyyewlx6I9OLcYWoY0msfcaUczoWmi1NffTg2LA32CKCwMlqGOXXTxBKABbcLsazjKHTUJC+SPLhhDj8gtCQopvRnAFXRCCVsbwsRu'
        b'XYe/PiBEFd54HingNz9G4wHgqt9GJW4VzvrTtku0FMMAT4rujIErC3h0mo3LMShfgroCoGekDUo4Xn7UbmHA1V860hHEmHilK4hFcIZFk4WmhWRJyFD3yFCScBnlR1H1'
        b'5kY4HCIdiuQIF7FsXIgKmcnDoCRLYYqXTIk1NRoRewnQgdWeTBE7GGYsVcUARCegHpowlXUws4PSEMxBBQgw11ShVC6v2sQo6+RqVCSdBDVKBCFBISfb0tosxgY+EDyw'
        b'03v5kuX0mT8c9JKq4gai05jpr0PFlnQIUmJgzyg8oy26pIQzOplTTXfmHDepryb0K2GH6BLqY2Ybl1Gt8CHgoQg6aJA/1BpAOxMP+ahUCgcmsDh/BHuYuoNOzWzo9yDG'
        b'tJjq8DpRl/PQAqcsfJQmVGbxcIxgIZVISCvUDScxR3maATQP79Cy854zyjIrWem/wSGSmL3aQ9HUALxtYx5LwEnJGm7DIsNp+kY0KtqO35iECgi/hfKpO8Y2HjWgCsRA'
        b'5LjqASjGEhvmy044YWYO6gXL0NmhMJZQvcAuEC6hQ/Z4KRdRcy0pusyjXlS6m7WvCI/lCaktDGBBV0iMkadjcq+h3d6clTjSiAdOjiN2POoaSYziTyxMIEZrEXijV9qt'
        b'qYzWUI+2jdH/ayDYA5rW/94n4k1NgrkJp/bulOH+iHLH//6altutaUCUzSKKciS/tXgrqu62F9gKzKj6W0RV3jIBv4deEpI3mUL8nkjI3+WFvJrmT1baRgIrgQ6vJTAW'
        b'qPFE9c3iEBopIxKOo0pyGf6tR3GEmrwxUZXjN40FWhKifte6P4EfJ9RSIivN8Tei++RnAk9KlFEv/kYCJTqTV+Nxm8u22zyoSyajEO44h2qeFPMch0eFCReimxppmdEx'
        b'aZHxCYqb6uFpmVGRipgRGvP/ICoBFljwvsSlSvih21d1/ElIRBTi9vff375y2ebfPHz/mk6UX1hqPST/z+UabiY6gnJQu7a9/XgbITOYP2sFB4eCrYvRIDqKDvBCvAay'
        b'08l2E5kJ/UrnOflKzYAMVQq4cdAggqIpUEXRg5OhhlifqxoRqCxvYqiRh4jG9TyDhVjmhwKV6I+oDrJJdZBtQ2tTwCWLB2rbNHuoMnQIytLtyOmwZosdseQ6Z+3t7+jj'
        b'v3wLGQ8aSgMV+qPadXjviTCUTMZM1mF6q+mEKuCYynjbFB1j9tuJ0LaB3rK4ZqESOTrgYA3NwbQslxnLvZVNdEdV6MxkNW5tOL1lgVYomkTCLA8F9GB1Ww9dgKxCTVjC'
        b'Xws1Em0xOk4vSnyheuujhgadoWMzGyrobbLpLk/F6LICQpQ+hnF956HbiTJGsbslcDIF1VLqjb9rspRXHMIfdyRqxgT1J+kvMKh9q7bnty+XmgXM1F6vkeytebOyvkFo'
        b'YTEl1bXz6srUmRmeBq5658sy4ku9auHQiYbPtU8ECsI9j/AFlZIX35mhp7fvza0vzf3tHcV3z1+Oijl5w3H8T3eP748/PetfcfsP9xS4xjz1ytpLvt7vbd1v9+o2pPaN'
        b'yUf8W6V8/u5PfNoXeuwaa/95++yPavTemvuN363OmZ/eLOsxDV3tEK7xZ+UvlZ8GXDMyTr2nJTQ68ZEgRBSsqzOuxMwn4/urS74w+dU02nKjl6elobBIUTTlaoB9uemy'
        b'68vg4geXDpUNnj92PWOzTlfz6ojPDDRO+C98e9OLEofrc1K/e0ZeNNBdarhJUFj36379byI3F1XfF6bcDEpK+f6ma1XJ6s7bnp9JvqyuORA083bL5kV3rk/79JvdtwO7'
        b'F+q+HnumqaHJ7TWbzA8Nkiw02yWF5701Q6dvrz92WPr05eag90M+PjzvWFv9vaUmG+d/PttN8E6b9u7DWPiqu/tqtsHOSFjAXw0be91rh+2Gun2Zi3ILl+VtmDeQPNU3'
        b'ZWJnTLTjW3/EuUZNyk3Wmxc4KyP4qXGFcz+3Mf7ujzVJJ5/NKek7LO/9efvap9xfLls7JyWueOWf7t+uN0kI85uleHnbdxtzKjM/NSnxmBoQItj6A7frqazKkJr7ihPP'
        b'+oR8EOv41viCMQkBbc9+arP03dkZ6WO+Dd8UqVd749LLP01476Nv038v6nfb897V4MqvZnsmhbikJc2PO5TYoCk/Ev/F/r5Jb95/cfC5X7f66+vPULz9nf7axp/XTX99'
        b'3cDuBacXdN28fLxsXcdbC6J/0tue1r/2k4Cn73zfUPL6G9E7CtvTdse/5OLw2huJ1+qe/NcX/Wtfd/hRsf+mw4GgjoQDXZ6fur24Ubj5useu52d5yLT3RWuv2nJHvchd'
        b'mmQWbOOcRlRQ0eao+tFGjajacJRdIzrEXAahAlNXvGldgfphU0poQ+UGlLlJXeMvR+eChuVHGAgzp3zjJlTuzOz3oACVK/13EAM+KNNmBe9DJVZ2mO87rJL10H44iWVH'
        b'aplcno4GHvLNzE10x0w5sfKEMo5Ws9wcakaw2VC+m8RJx2w2OufJeMkiXGYu8UrN8VboYIZgwSzoomydM7TuUhopLjEgscZbJ6dNoYJiDmoa4lBIp7HQSf3VoJb1qEoE'
        b'3ah+iHuuhD4HKRY5SlA7qlX2UarPoxwtdJTyq+HQg84S8/EUG8x5b3XQFqBjW9KoUGGdvoa43uKgAx8ExH4RBsyooGOGKjDPT32oGaLSAGJMqrmVh9ao6YxzbsVyS7Ni'
        b'CRQO2zhuh4YgWqieLpzAjK4aZti6PMIEHlgkPEwb4psEVzBHTZ3LVFKOGtd6gTkDOWYaPmwK64xOM2tYLx80wCqsjULnFPE6tnSzpO689sJxtJeyazPU0eAIAQILvP0q'
        b'b3JBqILN9GWC8xphBL/FhISjbtOmgzh53eTRHjI4o5hpxIIRD3QLk/yuoIPuIxhlzAlXyXkLOyw1khnm49BlqUoemObDW4biiukFxgk4s1QB+2Av8X9NbEyF0CzAtH4G'
        b'zrKSLzhBviIZs9X4HCGiuRC6BXAElWRSRncRZmLzpI7+qeRxAFyE5jRcv66BcBPKhpNs8I6ivkQpbhiTKiV4bq6M4aPxEcyc2mluII5xiE87uLhJOsKpnQP0Uktj6EoQ'
        b'PAoIgU4sfwALoXCjbY6FUtRP6DYlnqothmRZ53X0sQZcRG3SEYLsIlSFZdmdcIXSQTSe9r3STCuV0AplULOdPrKL3iQfMjhQC09D53lbKaqlsqo3XNiqQpJcQgOjuPLJ'
        b'wAyuUdMkqMAjdcxFzhZ0oADtQedn04ei9VBF/ByeGDaERTlwIordVlRhbmGUb0e8hk/qmuNMfaiYyRynZ8hHSA1UUosOF3DGMSLLMBGTWS5mjifmu+xQl0xDbbP4KAGW'
        b'1eh+cnCj9dBDFUMj4CauhRJjEWqBAXSRzlfiDExtlFJnYnGriHrY0vTjoXQ1Ok89L0GfGew3gUpcGGFjoGCkxsV5tZr+fCyGEdYI71EnMd0/crNlRsLr8SttagHawXQd'
        b'GKMa85HMYwceKxL2a7XQRW0e3ZjgMN6ZjsrR3u0P12yL8sXQDfUhDEpRtRHySGGBWALEVIVy19KyhEKLFAkT0DowCR8dgZeZt5af5JNso/f/UJT6v3IvM9J9jNOQ5csH'
        b'f1OokiXKqKCiRn90eCN+AhaExgkM8H8iEhGxh/mgJ57piXAj4TVpyHbJHTN1SaoBlgT0BOOEarwxFn708BPq6uO+iAWp5tXuSYhLD2KlfF9N+Z3mPTWhjMgP97EkcV8i'
        b'lPBaQplQk4prerwOtSYm9UnEWtRCWQ8Le3o07Ltoj0hA3uey+dOi+w+b51KRSik+MWtgKu/8X5kZK8Unx1HD/e7fN16xqvw7NsasE++SCo0fGSXdMJyg8jekMWkxnEDw'
        b'SWhaGiidxk2n0dJr8K+b6kqL25uykQawN6UjTVHnkLfnk3yJ5Jcn+bWb1KOhsgC8qa40y7spG2ktd3PMaCs1YhZFDXrowLB5MPzfXVAMmyTdwtW7kXnZwzGfNSIte95K'
        b'wEcxLzO88H/zVyaSCa2EVH6cCzmoYaR4PB0NMNy1CWoSxWite7zlF5kQ6meFU4UQVldZgfH/WcRoclbLuAetwDYFpBPTKNS50x5Vmbs6T58202WGK/TC+bS01IyUdAXq'
        b'RecRcSlIPJ33oC5tiUxTS2OMFA5CPhRjvrYqaBmBkIWKiavIS1IpdE9jOvmW2dpUK1lkR6BVJIaNkINKlKOPaoWoD9qkVB2swGxjG+aFThD7FBfOBTrRKar1H7/Nn2bC'
        b'v4SwN5XTR+1CuKiOOZVi6FEaaYSgk1Dj54p7M42bljKTqsGX40xnhqpV5qzFXI05znkWsqlRCZbGT0IvOh7qyhPDGFe0L57h8Vth0AVXSLLiblcLBZzBFNxYfFAX0yot'
        b'IjALsB/OuKpx3HRuuv9Wap3hhGqha7ivQj1cZZEQ9uN3+2YFM4cIJdA7bs1EVzzlM7gZ+GhqoDmhHveGDQ7NyXMG+kKoxmPSZw+HlNEQUBnsTUPVrpjOZ3IzMaNdSC9L'
        b'dsHp2axKZU6BECrdUd/m2du1BGY+OhtcMU25cW7z7OnFg7q/lbKJ6rPRXqjH4wKXSN9aIxjy/cBcMZ7oo66YCmdxsyaiQ8wKKwcR3X0bamKtVJ9EKiKwvhV0KNfhMTsf'
        b'iTvUhROzudmBuNnUSd5gGjo1NCJ4NCzpBKJGEZ76S3Amnfni3LLQHQ5jcYbj3Dl3TGCsZ5ArhqPKeU9fZs5zjGSCUTZ1lJ+ijRozJISGF3ILsyCf3eUcjFpuJKcV4oyT'
        b'6AygvgS4QufNA0sTxZAfosDzvYhbJJvM+taaxdlR2hRCNqqB+jlk+HEDzzmwod+HchZDM5Qq8HQv5hajU1BBaTMOWu3ZYJL+qUexoTy8AWc97r9da732JlEa2ZG9OK8I'
        b'GW2eKWTH0wGkGfTIGIbLUJ9zKhuIPWjQGwtKPQo8x0u4JeHoIF1DeMF1QK2yU2wgySoSoQY6mH27Amj2mXiKCqAfKhR4xpfi/5BL58AUXQFqGSAk6DXUCQNk0s8IJ41F'
        b'fdNRBR0Zn7AIE1SjwJPujZncVvwt055B/XY2AyzjHDp9qzC99omcKb0Y6KFDcNoTkXn34XxQTzyb94FtZsoGE2qJYquvHVNWHxyFbppVjoWno17riY6Q8+V8NaCf9tbQ'
        b'E4tmqlF1Uu4YJdDC5hJO6NLcbjt1cX+PI+JeRM7JUfYCtnbzoMYdHUukrc5BnalKEsA1F9F8U6FzOwnY0IUn04/zQ/sNaFdRMarePEQ3pLtsYUyWoz5DpQ0aVDijvqzZ'
        b'qAtPqT/nj5n1FkoGC3DjcocICOecQ5fGRRhEfYostuzLVqA+4raiC09sABdgFUgHyQjt3abqqTqcZNOCCCi8bxvqphOzeZauPy60C09pIBeI6mYwE7sK6NAaIqTF6uoW'
        b'bFn1zQ2iFIs3rU40iOXbatSFp3QZt2xsJFtSxQuBZVJfCJ1uqjUVziYTHUOt6KKaB7FIJNEnDi9hHkGOmmNZixJQNqaCVrwX0eGpIuNaiBppnWuhCXLx/lcixdO5gluB'
        b'2fuLtJfoJGbgm5SrqxPqsVzWOUdZbwa0s524AvexA1XDZSlPTOOD4iT0Ehft34pbNERHyt2RC4azykntwIRKB7gSWtOg3EqKJzWYC56KGljDT21dohpgtnQwKTWNY1ue'
        b'fSTNa4Wl+BN4fyuX4nkN4ULm7KDWS7r4UKm2x/sdPT9yUtl+p9hG27sY5cI5PFpHpHhCQ7lQ6LVn1FcAOVnKZqpjASs7VTkxUJjFOtqAchaKUIUUz2cYR5yfVjIL2KpV'
        b'UOW8mm3iQs7ADedZBZW0gTI4MwfL7qeleCpXcitRkRolu6k26JxyYIT4HBtgJxzag7efcTybzmYoRD2GE6AIJ1ZxqxZtpl9HJm1FeagJivBEreZWozZndo4W+vmsWQ5F'
        b'eALWcGvCUR0r4zAcHauzAFXgjjpyjlLURl8WmG3GtfejChbNR2NVOgmNMs19xkRoJMgGC84iK40WYAanJ8igHFXgcu3wPlsQSQtA+3egumWQF4QHfQo3ZVMqMwC9Ahcw'
        b'F5CLN8EK3FtnzjkOjrBN+DI0YRkOGlCFGjUYQ2ccaEHh6KQmXJYH4fZZ4bnMn2SjSYfHQobKlIcOGZ055AiHY1i+7ROhUmZQmI+Hp1rFmLBTNx5dJm5nzjP6OQKlouEt'
        b'gY0xLq9dH89oJTpNrQJXLZ/BDm0442kuYEdHSCatIcgJd6ZItWNHERoai3clfNoitjfjreMQuXVR7pNoL9th0aFQfNBBDj00NAx2sjag7CUkcBPbX/oWpbFeXAqzYtRN'
        b'+xqlPGC9UR+mSlrHTuJfeHgJqS9khJIH3cQwL56dgfvWotO4h+VDu9Ei5b5pkmYjoK1Qk++W00CJ3qhzuQPPSaCdh+wJ6PTnlK8sTfW00aTGduEiaqvHORstCx+bmMAs'
        b'8LYuZLGCnNXMDT8XLGZf+jppELM8Z2ejSvPXV/myL9/bqceR+wXnJH9TnXQX9uWpVKWxu5W7/3kHbfZlt6kWhxedsbPVn2kJkzTYl8uMlMGCQnOsFTPj2ZcVITocns9Z'
        b'zhkXDVv8FrAvV86mhoYS51Btm9VB9uzL1kADzppUpDUhTU03mH2ZmTJU+wvCN0N2si9jNZTdjC2wW6yw5Kghta2MRT9yNmsx6bIPxYJj8BL6wCJEWURovNsNbTF728ta'
        b'jbXVyt/31XlR3Oc1R8i/a/NpBaGmyqexAZODRabc567030/z2UrpQftQsYIca3gJJnPJKB+KKF+UaB4IZep2ePlkcplQ7q/03sVCfxyDgw8RWwL0YULot2fRrNYbsR5o'
        b'Ic2FnptZX1NNhkZlbkKqg+hh+0mVOzLqBF1pP8nCLA2HV1KiSG6K45OiYzJTySHzqPhK2lheJwwaZ8TRiPW2+EA8aBdAbIipRaK/XyCqGqVOhKLxNFbVcKAqzGnUSBdA'
        b'L4tbWSJfyZ0ndDbGUvZc5G48KwEB8V9OvSRSNON6ek5tOlB+LcBgucH+787d6qg5Xf+l7lUT3c81Up4QXNWN81zuefLOTF29KKHHS+tmPBUVOTmy1Sddtqb32xs/ql3O'
        b'tpv4xLn7DpK+tOXvD/527H6xzRcxvyx5Mru/RXdBZbFFgFXp5LmNz6g1XlsS/YzV9IpV3aWzP7nGF0ZrxHQaJn6i1V3h0VH0zoG5n6z/es3rZ7smmmaZek7dprPuE4sJ'
        b'Vgc/sN4me/qa/iyfOoj/UdZ3resLi5c+nLNNMPba+rWWTh9rbjPcGT2/rUx48XLLm9OTPrBK+nDmtxE6W1O0f/uB056/Y/NN6/m3+i/XLZ8RF3ntzexf3+1bn7Fz61ML'
        b'KjPGHpzn/qHHtG+NEye8P+Zkesza+ZZaZr3NNTN1ZWOaDOe6RJ/cdeyND8vLmxantjQ67536a6hikdfxAn87/TO+b/68p8b7aO7VnOqLevq1QeXWLZ0tm8+1vP/D9OIv'
        b'pvssyVxm9enTd6uvbr75mXZDv1/O1VP1Z/1Wl/80/xtTNDMn/phicuK4KQ7Nq7be652eVLteB51/ITC55faiOdHPFi9pfnrLwdSQdk0HzVuDaILJNdEPfSdnLnq7y//o'
        b'xEhtk1+/nxM3Nbm8eHpkca3bqQsNoT8vXJq+wSUyfc2tH2a+ftpPMSs77O1jg0fe3XFhR3zdp40/7axe+Urynz/A6h3xzRkbpnkXhr1p9dyLc99+7sIpcYPV1FXxzbOe'
        b'7/H1evHFpFRjlz8mp582f8t83+Hydg8rp23FuSGfff5e5MsGf+zySi84c+BZednldJuOKwn+ec+mxzq9tU4xX7/rxdMTg4IPe4nHvGEX4+Fqtare2ku2v6Vd8c2KUst0'
        b'8S231jtLf90XeCxzk8sPC0Km73lTrmGz5buGC7Cn02PRqRN+rQZ7u9sbX7839fmfvmp/duvksNcMn/6w7t7d/V87Ppl8tm/53dC7e7+0qDp7R+BbKJ1R2GCjRbUIcVCg'
        b'j45jCu+ia0HMibMEqBEOmDMdQx6Ur0JFmEkrZd4kRN7EN8SlecyLwoE44gmbRAyUO9gKOCk6ijlVC35ZAru5LsbZL+GCa/xICFgshgg1BS7Lmf9v1AblcNYuBh3CjM1Z'
        b'XzEnihbAQAy71sa8UJUb8S7kY+8j4qQZvAOPji5TunyJ27iaWdHN1FPa0W3DHWikl+2T1KDdToaaUIkTbo8oXYDX9bkVVIfDR6+xo8FtYO9UHroEoVtRNy1vhtla3MMy'
        b'z5Hmcx3OMSxWKBZ1apTgEzEnU+Nxj+rQIGYOadbV+mSb6Pejxjq4vrHEs3qLMa3PyRx1Uv0Ylg4GSNhWaNNhTm96s6aovC75Yt5JGVEJcjfajP/fmuE8/opS/R/eGN/U'
        b'VGyITAqPT4yMi6EXx57/1u/40H+RP7m/pFe97Ifn76l+hPxd1Y+Iv6P6EfN/qn7U+NsiNdFt+led/0P1I+F/V/1o8L+pfjT5X1U/Uv4X1Y9M9LNIxmx9JD/IdDWph3Ni'
        b'waMpsBQyX+DMdzjxPy7iyXU0eYNcNrPLbx2BnoDc2BkIdQTmNK8m9SFObI14+kmT/iXWR1Y0MCtJ09RtkcQS558sEH2D+/cH/yHuo3uqET90/Sm8KYxPjBtxA/03J2is'
        b'ykSHlNVPTHTcyTH7N0x0uGzj7kcY6VD12xrj0UeomDNaL4JKiSSMe8iTrebQaU6cSowASwqUkDQ+VlPlwVb0tzzYPgSTJFeQEu7Ba0izgMdfhpL7cNwGPpb/h0DYh6Bw'
        b'5B//UN3iAMorvG3Pc6K1GbjaiITl6124dBLPDLWgShHhi8Os5bAPlTNspbW3TxAxhCn2EXNuO9Sso8PiF4epCxRE6eVeLv4qwjvy+Vjrj76MWPvE+dLsstLw+lyXfc1H'
        b'Ogo6ciyqs7vEXNK7al9nNtrwVHu7GUrc5Qu0hjztqM3hx87WoGF+gqB7+iMsAKBLjvJEqH0uyh8CpTziRvymdMPGmA2bwynPRdc5Dc77t9Y5t1tizezutk8MJy6dw4lj'
        b'iGHDtRElD9G8IH4ExfOjCNtERdjG+JMh4fLm/G3C5rK13noEaRPlxRzUYER9rnmT6LR4W9echSflQYMzgpfyRyVqUAinoDGU3EwaS1HtilB2bXhAD07J7Ungn2IRpwb1'
        b'FuN4TSykHWXXKRVQMm/eSjtUHsBzvK6Ag4ZtlFicE4gM8H2ShIvw2zxtEolMSg5DdTgOtXK/gACCwJMooCSQV8BpKKF5Jm7SxGKHsVigE+HnM1aDUxAhNthkbtCYLSlC'
        b'UQqJ18N90UHlg8kJBOC0JVnNM8LPev06LoEMrcUsMZGkOG5JguwT/qOANzkFEbPzdqgHhaT/slXICS/9SyyYYuJGa7POIHKHsRkuIsF0sx6nIAy3/bWpH/PcB2JOykmn'
        b'mbJ4tbFE2Hhmpbp5RMIax7XsvRmBlh+Lua3ZnBan9UGTgjDnUz4a+PhTPH3b5Fac8e0XFGR48j7ZFxQyJqcvY8yWYCwnOggqzyUqqI59ZmrmdqrObrYmlt/6HcJP1qbR'
        b'I4jBzU9de037mv01vH7U1fcL+GnuBbRe2bUfX+O4y7mcDWfz3Y5g+t1Py5a8JuIm5HO2nG3dM/QryYKnigTcu79y67h1H0+jzVvqYl70Cv4rmvURt+9aHv0u4jnbolcw'
        b'DVrd+Jjb78mufG0mY5mnyIcCoVzxIEMd8TTA+zrDwXhxVZ1Q0Yr3oRfK+71WvJB03VN2Ie6jaKv+dw8dt7WZ+71sQums4IHFdiHv+E9ZGS8WXP2XwveVF810dn7TnPvJ'
        b'3Is/Th7g3RxvVFS97K3/1dGXjs/3eK9/7juzl2T8ZiFYBH6y8C0Xn39BdCR2zrLTGm8dbnp2+s2xiude/2LXHX/Hp38LeOeTuIhXL350u3++Z6hD0uVL0g/O/4LsBCWT'
        b'Tn6k/0Lpnc9rfOb0zi12DInKRHbNsW5RJ2ULB779Zea+YPkLU9e4DTj8fnr+ZaNfgtAfZ7eYpZeOCyp/qnJF6RPd+yycbj+b+c6THfsvn6qOv+G07Yj7rJeTJlmoxy8J'
        b'PrWsc+91Pd/9Hbtbcp45lbpJcT7eu/LlRdrxp762Xh9q+vwbNj6tfSfMKnfHrP5G1qR4xd1tv3x6bfwMlBf+ncELvwi14u4svv/kR79++dGFn3V7qwZrJs1zWzrgaNZT'
        b'tDIrderySx2zut8yTP82/fbujOjqHz9++v37dlMNjr2R9eTnNb1XX7ro8dTUrNkbUjpd3uy91f+q6/bcdVkC7d+//CPsm1dfHH8+6fV3n/v64J8Laq4k+LnWOq6ZvHHH'
        b'qbNvupsMKN6sUYz54d7E2t3HdPbwNjp0Dx2LysLlNsRsUo1T00DVcbxtsDVjiw9NTCAsHIsOJEE906GUT94KzUNW3nUEMYMO+NtjYrjAiVwEcNZsLeUoTSzQITnd5tEB'
        b'AoaTGG2Een5XCuYozUnJ/VuDFWkZGWO0oERbew4cQJ2yFHy6ojoh1M5CBymXuzHM145xzfNRMWOc4XIsfbQD7YOLYZqoyB/OEvvyXMHSscBwAwo9qLDzVbKqan5wZgVv'
        b'MA0dTWNqnw7olrNnaA8aYKwsqkeVjNGvXQCdmA1WsuoaY/WlPFTAYThMSzZB7To4s40DsRBRc0L9EfykeVBKn4XBCdRiN4SGcfcjeBgZyqfFLk70IYUWQT7K9/HDx5QU'
        b'OnhUuwpVMSkg3wQ65D7+ylGGeu11fIw/nKMPl2Dug4CmlecbXLHGR1wmNNFRGLcBGihU2M8GTx1UJ3nwBq7m/6XW/j8xlB7FIQ8fevTkrPsHJ6fWVBF1zMb4USPqck1C'
        b'Y/AQTlNEuU/CT7KIOvweGeZMRZQj1aLvqgkMSDwfytHqUG5Uht8mvCd/RyaWUc5UU2B2Xc2B1aJJz+nUcSr+U3xTtCUybeNNUXRkWuRNjbiYtPC0+LSEmH/KkQpTJ5Ay'
        b'Tcmv8aojnNRj8E+PcLObjzjCyQ2lJapzGXWEk3Vm5C9CA9MNoGDtBn4E50YapWIKiWkE1Y8LYoUqDwn83/KQsPFRbKGIe9g/Cj7UyTqfhBfPZTiFyrGISMDs5CoUE7ke'
        b'9ArR3liojhcZuPAKcri4Nn1wOPariC8ibkX4RX4doxn7QYKAG98m3OK7d4Q3FeFjjRhujiGTNZr0bP8B6ck2ppqpyEDEJs10tDXMSM6Mf3BuSeaQfzq3OkceMbdEhbMI'
        b'LluwIRs1vf7oMjdlkTgY1cGR/938Ch+aX2FA/JiPbwhY7ISZi/G06S7DE5cQGxXtHSmhTokmviX09nznb06d4r+aOq3NqRMfnLoJfzV1E0ZPHcm88h9P3aFHTB31Z9IL'
        b'OSF2AQ/NHfSiS9wUdFwcgc5C7eNnj8iteWT+BHmiWNE/nL+HREYydw+HvdBknnVmwkm4MszAj+PVEzTRWRHlbduWm/FZIi7Tc8G93bNmrzChX8Icdn2/xSPJ/keTheye'
        b'G+EdFn+beSJya/g4ib3SD0oflEBzEJwzoffuuRxxyxtG35ftYMqGLaJk+zkbkzjmXOGyCVQGOaBDdt4+YmgXcmqreAEci47v7JvDK7aSN4y/MS320OJdZIvjjt3Nl57t'
        b'XvqB+8srVhd2T0mID4v3QyZ6Ab4L3bYHJi+0Hfeenqw5eKaRe+SRAJcmg1e6UdmH0+e073Y33JaP/rWy4kWr8bca5V9NicxMrH1pzE7tK0t+Q4vdD20YEz3uysCHrvO2'
        b'PT3lPjfmabNF8XIbCWWS1kNeup2DtTfxRg41vOEsBzhuwHgKVBIyxCShw0RyIEwS5EEbuwY7tRQaqQ4IM0qBU9OJC45izLBsQ52Mi8rNdFeiZeEgGlTe9G2dxzLnoqMo'
        b'B1opO0NjD+7iF6FeSxjYxCyQe2APnGMXd1haU97dDU4Dpb/aARK62s6b2sRaaoncBNAGOegEy3sJ2pcOo2n94TK9EUTHzR5aqnhR/aUB2U0Z2Xu3RMeGk8OT3Yv9g/Ur'
        b'SdISaPE05h2Pz/a7xASSnPGp5iNWdTSpR/QAqOuhhvKpFiRP9FDLaBFr/una1qt4xNqm4TUPmKaxbdnbBx+9qCOEje1ElCtCp2Fwx0N7p4byr2LcA6HVKoWVskr1WD6a'
        b'PyCgt0T8sOuiWEm0MFqUK8kRrBbFiKPF0Wq5XLR6tOQAv1oNpzVoWpOm1XFaStMympbg9Bia1qJpDZzWpmkdmtbEaV2a1qNpKU7r07QBTctw2pCmjWh6DE6PpWljmtbC'
        b'aROaHkfT2jg9nqYn0LQOCf+Ge2UabZYrWa2Ln1rGczG6OVyjoESwWhc/JbdiGnhjmxhtjt/Qi7agzgUn3VT3j0wiZpO3HUYF8iGRwMwT2SMW5mx0oB/Me5Kd/KH9VGNo'
        b'01vMKf1DUVtAOsTkZNRQ7ayiv+sb6nbOv40lNaq1w7GkHhe5iSwXFjyKfCIxoiJZEcsWLzGPjU94RBiqURRGSPxRF4Lp5Pi0UbjSpU/CywQ6hCoxaHAO5UM79No7Cril'
        b'AnU3KIfydHK7Bc3oJKqUbkkJQvn2Q28HS8j9BAkWTZyiYM5tgzDLXCLDBwbz+aXnHDzk3AflupHovahaQTd016QlJDqvBJ2mAXpZdN7ZkE0vVv0y4ISdrz/z5G4n4PSh'
        b'GqqmCtHROdDE/IztRd0y+TRfnhOgbCxmtnOo1w2VMSVuBSpUk7MY1KhFEiVwWQoFzHfOAOpYKCcBAKBCQmIASJN5dMQhJJ3BbZbG0z2YwJqL/EiEAHRciA5Dz0I3Q9qq'
        b'uXi/rJTDOW/cMJJbe5IQ9+fiSiiCEqW+H0tjDVQawxtlsxPxAi6BXn7HrMXseT4a2I0lOWgW2mKBjaj7SWxUfN5fpO2zXu9MY6ujFnRJ5WcKmkxZ40tQ3jKV/wnYG0hj'
        b'oQvU6GWamEf1chZFHLVkEVdedbbsnD1rCHUqZ12ZoSSyvc00ZrZ0Ae/1F5SgDMNQlb+tZYvoPdlEZ5Hneyx+kN9rWcFDvruCQ5kligk6aJEJV5gmWyRe3yZgoYZemKZF'
        b'buyIALIYzsEoz1rErda6eOJYC/ZCAc361jjhMj8BjXAlm2fqztHZXey6TeXpC12CLhKePhLOM2Og/agUmkd4+6KuvrxXRIUAC9sEp1GLjETyPgQnhjx+YfI5iaqpYz41'
        b'J4MHHXLhQy97OFYyNK9k1mA14fjIxMRChRI8WVrohFAiXucyKX7iR38IFIF4w54t27uzfG4Scpbt8zlSoDc1/p6+ndj9F9u5C7RLvawLZabHzCsGrktdDb7Q/frSmS8P'
        b'+Lrc0n55pvSumf+tL12fv3rIP/HZY4lis4Bf41Gt6fRnLvyrIiTx5HvJWkeeHne8zPXCjFCdiN07zJOjnPa8NGFL8tsftm1MXdYw65UDv9TOvFV3q+3W5U2t7p//FNzu'
        b'9a7J5PcDd1Vn1d3xftdza3vW8xM2x92I2id4but8zczcHw9YnLiS2lFiOsd4W8B1/08zjnxbP3H2967qL1x96e7JGVWRfu9+Kg19a5t79NvxzikB1/2u+74+x7/uXctn'
        b'jvT/kGET/v3Czus9byxsrehP+3jdR0ld5S8+taDIeu32m6s1pFMGjBZq/lz4aa3zq7qL3/U2ijc6Zf+q/e2T9ovve/nMt/7Scsrdk/Z6n165tuLN1dJzxyu9/j/m3gMs'
        b'y/NcHP8GG2SLoKi42SKoCAKCqGwQcYCgspcIyFDEBSIbkb1lgwKyh4CM5L7bnO55mrZpkqZpm7an83SkbXp68ruf5/34BMUMe/q//uGKfvK97zPvPd9e6/1R79vf7/15'
        b'duv/3P7ju9emC//3p8rF2XVnavrN1gtdY9rDTWRCiYL/KS6U3JUZaIKgCyZ9fM2tPbWxkT+hniRhpTXy+dcm+qwmmKW/AdEHwYXAug/fhPyjQibQE3xso86boi/vtUIQ'
        b'M66isVlofQ4V8GAVvwA+jRYyA0twgctOSvj4AvP7cOIG05BP4rEaTNjyPJ/T2awj127efZwowRgjcOrpEmyCak2eHRiLjepC1qAZPL4idtuB92R2L5hW4r1V5LTPAFsV'
        b'CIVbHIn6dApdX677QmkAI35SotSzSeLTOJkqlOMo8cE53t6CiJ/U7gS2iaECR+jwGFqFqDmt7H+iAQ8OeIUKGVCV2HGR+7GWEUDdiw72UuhQOsTTfq5cotlKA57RP13o'
        b'trwuJX3mHpYIGXH1UI9Cew3CGDe8zwigeiDte4+Iry/Wm3/t5WeuQIoPQyr1HRJsjz7MvxVDP7bL+wERvRvhlSfig4R0yLtQhU/44PLygFqq0jWKGZhvzeEmyjSFf80J'
        b'B7ZYK6lIjNzd+cqu+HJ57BnR0D0Qhj1SzIXqy4JpryF+B0+U88a5zYxqqBPg4JN0KONL81bToqF9ZfX/NN2l0Kd8jK5zhidjwUPMvSiodEukhdho5fJ6fK6ZyjrwCJ5w'
        b'sf0yjp/m/XeWuKZmnBRy4Z7jQUPhMiY0CaL4VS0RH90bWgekxL/uQgPfkPdpTVoulzIFTNGFZmVNKfS6Y52Z4ssNT6qvmgPC0mG45D7NBIvPKLmLbqupscoSGtwzrMIt'
        b'dLyihFTotM1+NEiMVuPfSCSaQpWJf+ora8rsb+xv+e+Fn4+0VVT4O0rLv/vUd9g32doyIfK5Tgqy7KYNK40CKp/ZvikRXrVecVqpTK1wYaf1GdUKUa7xP1fJaHphzZ+9'
        b'jPqmT6pP/3Van9AwQT6DvFfCVt6jQCanPqvZ/2rNEWQl0JUvpCfEJX9Cu4JvLS1ImH6pXQF7KyIjM+0VipLLyn8rXIi0jXzptN+VT2t6LCkiziQh1iQhQ2iPetj2sPwU'
        b'Xq1C/wXRJ9zAm/KZjXm58bSY6ISMlLRXagrBZ/vjJ933D+WzbZLNJnSB+JcqzKteuJQSnRCb8AnX+rZ83l28NUBEeoaJ8FLUv7KA+KUFxGTFRGV+UhuMH8sXsF2+AOGl'
        b'f3l2ZSFV7+Vzvy+f23wJuDKWoRZBmTDAK1+A8oXomEgCmpeu4OfyFWzmWMWffvV+BvJ7X4LWl078S/nEW1ZA978+9ZIl6aVT/1o+9Y7lyjM7+SXNeeX0y2bnXO75ABmx'
        b'PEBGVCTKE90UZ6veEHF7gJjbAES3xEHLPq9mKWfDvmgpV/mE4JxXrFEfayb9KHjVFskcAq/Gx/A+0hnxrFn3MzhMixF6XvA+zskpGS+aFl4wLyxd1gvGf4NvfyjhnQgM'
        b'DuXzTgSx7/mWKyqLVIrFUx86m4m5lLOFhMUGmayLcz7LxF1HyDn9kur4BUsZ2YzXfnYxRHRbSTl78xKbk2/1WdRNbFxMxsur6rNZf6+2ZLb8zOxclKuxCkPPZBZ8Nyd7'
        b'HJfJf1j7zNaBlc+H2HA1wfsGzCupw7w1tv5/59d5MZyLrrZU4XVF7texv3aQueMSY38TXhYneHWURVufSF+P7v0J0BXzPFN4wGpWLVNn8FGwcMWh9p/m9kkretW71lT/'
        b'5LtOX7rrEvFzEV6l4uWTf/gqV6794SpXzqzL8MjG6TPeOekSYpFrKMybq9MXLTBjJpFZc6BOkUEEdhwWixS0xPBQC/K41QuGfXTYe1h2lb6xY+HJ3VoJno5fFafb0tdv'
        b'T3zhp9HxcZ5RvhG+EYk/eaQ49iOj7zacaAgKznF6Y33B+g8939B/08H3dY2WX4nGlFR+3CWvybxcyl3tlmJlkMLJlUT8ee5JQ6KprCbJ1nnhroTh7z1/Oysn/d2r3I7m'
        b'/64iYb+4gJcTZe5+E9oJiOTut89Dmv1eoKvuLOIvXRANiBCvtBGnm6RnJCQlmVyJSEqI/hRzr1i0GotR8j95jNvaJP7XRSr0zB8UTK4YxqkcSAh1dZGmMwk1Zxv8Ovwb'
        b'kaaxfhEasb+kT5bvK1X5Hp0z8w13SR81rYg2083/Y4hat2t/opFjQ6Kho2FzY8nJREODEetoUYmNZXjol46jyesVX2yFlq+fOHanW+s7Utv6cUXRmPa6vv17zFSEuiEL'
        b'MIAlFlxphUdXBb1VE6akHti+iRtVYrFf04JbTXz8xPHJglH4EHRz80XoORdZoIuf2CJGMKwaY4UsMkc/ZZnB+LiNSI+Zi6FBkX99ExrxrmC5heLNS8bb4M0o1PhRVjrD'
        b'9XCcgHahoQV0qXG9/zL0QJcFoaYXPFYQKSXBYxvJVmggPZ7HP81hN0NneGypBGNQIVIwFtPfhVtlfOtT/WIqCekX+MVyBDryeVmangKv0cj/l/CSImKFFRrj0vDPONtL'
        b'lvSM1TnSo/94FczS/e9P0l2XViIjK3qrVeJYVnKDO+hi2BFJmerGTNxpLIn1LZUldeMtlSW5/y0lQYR+S0mQbd9SWRI131KRS4qxS3sT5v/Xe1cuI0Zb6eNFdmRsElYe'
        b'Q0NqLJaE/nuKYGgqaKsbSIT+MIs4DU/lLEURSzVEalAugaf+iS8wc13Z3+klzzsalWoMa0TRknvM9aZcuKZQt1AvVvGzOxiFt0jiUI/WuKvCHYzbE0QxKjKXngobP3rN'
        b'PTEPeFensRWiNaO1+Niq8u8UScrVjtbhv1XjKzKM1r0nid7B39Hlb+lHr72rSt+r0/ci9kSNMv0YRhvcU1LVU9WL3smreijKurusKdQs1C7UKdQrNIzViDaKXs/f1RDG'
        b'ph+VGlVa84Z70uhd3LmqyD1/rGORZqEWm7FQv3BtoUHhOnpfO9o4eiN/f43sff52jXL0Jv6+ouxNLf6WAb2hyt2X7A1NvsctbI+0C0n01uhtfJda0XpcjTR9S1OGI/RX'
        b'RFxM2k/20gWtoPNuJiufYMyB/k43iSC+sJxbMB9jRIZJRBqz2VzOTCA0WDFQLEn2/Plo+ioqg+mCCRkmGWkRyekRUUwZTn/OFemVQdwnJU02lXyWiHS5GkVsK9kkwiQu'
        b'4UpMsmzYlLRrzw1jbW1yNSKNdXhzdHzR18k0tOc2KOd6h4+edLM2OZKSvCvDJDM9hu8gNS0lOpMvd8tKT6/MCpdG5/dC9sXK8i/y0i/s6uXlX6RF0s+Ud0HC8k/OPn9J'
        b'/Lie8/YuMfFLS9t6JYev/FSZ6kZXu/wqVtXR2P3za4u2NvHixqzoFFoR6XQmMVkJ6RnsN1fZ6UbKrEAxqwgWsgXJlHVhTS+o8FcT2CLpm9hMGi4iOppA5SVrSo6m/00i'
        b'UlNTEpJpwuXGrk+RaqSi1ZzYa/x5His8TWQFJu5FYNtSpVZPudkcq/CeL68Xe8LT13+pKhssYqE69phBHa/Hyqpew+zyUq/PBqDXvMy8layY0f8KFqretNog+BgXbGAY'
        b'q0nc9lQQKUItVOwSky5bBPNCev99kiR6hGRhfKiRdfaQQK8HbDAnyIqlhGOPLcwfFkmtRVpOku3hOJi5iw07m310eZ8xU0/LRMzB4uPHT1idlojszRShEhtVeELyJpjV'
        b'sZCwBiswejp9l7bQ0WWNxKZP8Kb6ftXYVpTJ+DqUrsHpZ47ME1jkG+gOE6zaniWW+wkF7QJTlDEHitQEXWIK78elX1ZkO4GRYyIo8cbGhJ1q7ymmv8mXOR1TsZgo3aPx'
        b'xqG/B/zO+lL1RUmu07H29F4X1y3uv/rPL7qnbsl3rNBY2PHE9Nwf1T5sPv3hSZXDh9u239KNzLr7gWf5sVltOgu9nn7b87tw/3e/9+bbY5mOA+JTft675sa8/L6s8nhb'
        b'i9H3BjebvjVwIvHB2k2nTeevHjAcDdTT/K1SxPWqxFGt/0afHVcCY7H5N+s+VPtLASTdnXn0tYRj2dq3v5b62/V5sz/96OO3xw717/5nukHsmWt1u9oCdHTjwt5vKa79'
        b'/eLtmA8drN7e+9Vd3QsZP+j40cficxvcjqfVmelnMA/3ZWMHHjtw9bZIEinec0VoLQ9dxGrLZa5DLIhe5j1UOS/Irq44c83H91mHKKiKwYdhUMclzCwo8LLwDMEcwavJ'
        b'fJpb/LkMeRweQSf3aC65M72gHbu3hXJPkQqO8hZvJTAjJJnJ8jLF2M9dXglht3xYxIYlq8qpqu+7UwIdCUIddWXIgV4sJeHAn24+imRUcyWStiekgTghSyHVTYVqi91Y'
        b'wlxQSva0kEcSy/1wV3C3ddKeG5kz9ZknFWvdJDexQtbi4TI2wZCFNwxhjp8v6ZxbxPAAWk8LjsheGLSVh7vDAyxjAe+Yo8TLeiqJYFzm58NiU2jjDSSslETrYErB09yE'
        b'78w/cbvct6UERfhQT7LGcw3fmUqKBquP6MMKEJZGQhlfng7US+H+ESjk7jEnrHJjDjuO9PfhDkd8zSCpH47HZNgK25vm/apY1i4rOMkTmaB8N4uUKxc6M3nAKJZCqTLc'
        b'ZwUihEKTdCRdWOqrCUPyPiDQfNVB0G+KXaFBKDSZhpXyWpOs0ORiOl+5Ac4rspBsmqk4QDtRlj0lMqBxFg+cfTFc7bPEkq/mozvL6Obn0SQcVHjrcQ1e7Z1VftcVG3/M'
        b'4uc1eJy98cdqEhWZL81YnL1uJbtevS25nBcv86h9gmNSKjy7ih9tg/oraCOG315FG3nZuj+P9Vnxky3PTuoyy/MLk8l9a3Zy9v4iP1/Gu/8FZ1vazU/yAx1aWmLaPhYY'
        b't5zVrjB9c3MijzyUmxP//2/8jiNAyhc/t62l83rBmHk+40MFbqfODCthduryDSo8r0ClV/zd7/qZiXkjDqyHhVtyrH2Gs6ewldAWc50/xVSdVsgaue58DhzSo5Iu8FTP'
        b'z2ODdn8VVNDoW8UgyeDJFKqWqY84yT74BlhhlcXyrWLdrqRVbdKGmzSd4dG2T4lU54ayQvHnjlR/ocbiEhg9n0nCxcBD+CD0eWLOYhSLfc29LaH/pBCuSH+W0E9xgC+z'
        b'AMEAFKs7KEFhQqq5riSdocb1R1O/Drd+/zfhX4s0/cAywjciKTYp8jfhvwxPjn3t+78JL4nzlmUv1Ogqf3zkb2bSjD0iVmYKOrERnvAqP5/MT4iX2MAsT0DG2Z1nng80'
        b'uqDGU5AVcJgYZgePCIJGaL9l5rkK/BHwKeLQUgDDJ3OGJVN6WvFnhcWVNvIXrPQrDeV+rwKXum0vgUvI1dn3GcAS2q1XtZsbHtb0gqKzMpO5NvbGcHiF+kOCxRxKIUco'
        b'PVcQaCW8ckSwmBvHJBTfdZRy2jOUsu0Fg/mPGr/TEMRM5jfeWF+gl7J+yWRuJHrjkWriZe8XTeaf4N0oE7+63fy0tpqaQrbhy65xmfn8UxZw+FUuTrt/Fd760sUQYWTW'
        b'vJeTCeYbYVHhRCYUiVAoygmF9LO6rj7qfUGD9IjJINVZxkmX20herntfSouJFfTcFwJfVlGP02IyMtOS0x1N3OTt4GUnEG6SEplIGvunqLWrs0RF/0xWrBXuhVtx2d3H'
        b'C+acLb1OHT9jdfrMC4HaLEgbcvaqJsLY1UxW710fFoJJ1bu0doUGvFLVO6GujPeg+0jCN3fPiNMD6K0kH61fh/8m/L/CvxwZH9sfwxwAwa8F40jFaPCju2aKptve+NbX'
        b'fvCFH7x+XNp90eii4XhDbmLIWMN4Y6m+T3BQg+vYvjKOBPe+pvO20bHNlWZKXD/Q0YdCIYzzIJYIOg+0QJuQuNKB92+sVC4kNtB/8ww2ZsiqyA1tejFS0xjqVRJ28boy'
        b'eO+mlyzIO1KMVQl7sP4At/VvgCaY8yHJ/2HUksavflaCQ7rXhFLt02rQu2rhB4XEZGT1fx6uwOCXi6zLy0Gw/BYZ1EiWWN/nwuhUDZ66qikUhlj/HDItG57P2icLWONm'
        b'8mfi9apcoE8iPPZMqPakIU6+CuLrN6yC+J+w1pfj/AthFZ8jge2jyVWxPePF4JaU2KV8iX8/8rsJc35G5F/dU0cSac2b/6GYznTkhdu7fx0e9tq3XicsrOso2FK6pyHX'
        b'bqNof+xuULheamIm4QqlPpac4AlHeD8aGuXxpOvxgUK2qYXgGivGVhj38fITUg5g0kvIOji4c8lLtbqL1XKJP9l+TlgW3WahmavChexihFm8JEtCrrdk+aTRrwKamkWf'
        b'ETRlSzATsOIt5fSIKzEXItL9X24xZiGcMu6kxLUhpc9pL75rJv1J5Gr24iWwZcb0aFnJ+s8EtG5yw39MRgSLYIsQIngupVwhdsdKzC+N+38F8cI7ssNyZGZlbvK3ZLbk'
        b'S5npGcyWLGBgekZCshDXx3TcVY3Bgt67IhqLWfxp8NUM0XJkY2tNi7gqHBft+VNwjMHzi3ZjNYHBBoeyqpwyhHkJd2WdCOUc1jhbSC5qxjwrC5Z3BNPw0FPEqqvv5HVX'
        b'bIPWBJn849SaK2tSFUQKjeKMJ2lC5U5nXqTywLue4ZZ/c3MSnUz7PcGCYCdewJwkiwAaTG3jCRE27Vyb8Jc3HkrTO+g769qfn/r6HjWJm4bit9qi3zylra7+RfUfXK+z'
        b'OvKtYye+ZGAwFF6dYHw343zEB73fOGvW1u353qHCantnXY/pP38p2nSv5e8f/2zicOcuhw01eou/qCwb0z/yrrtOYpX20Hc3Fvw2TyVKM7Ms/fi3j//tS5VdDT871nw4'
        b'MKNq1+lDJetSbM6X+b05+W387W8yL4b2fPFM4vEH93wu/XOy7ODJ3/55OLPhnEvDH8ye7Eg2E1p94IQF5BObJ47dKLdt3pZyK1wKVpixqkE4vILR34RiqJJ1e1XERYHN'
        b'Z6UvZ/QqcB8LhfE7sfaWhbffaWiXGxnvQKsgRVSxRqEWJM20mC+lDagelECbsZKgO406+yzZGRv2MFVhmZ0RSoR2wdADE15CnqupVG5gjRTa7sJTmD7MTKTqOM2tpMxE'
        b'ir3Zq7NaM6XPaqp7S1mWEcsp7PHPTWE1tIXmimpi44+1pbx/iFhB+M3HChLt/1WQZBusQvxowhU2Oi4Y+Eo+XYggPeLZs88kCX/6Zwoj14c/J7kW5Rr8zyoE+yVrpnPl'
        b'xkFOsVXl8eCCU/8gCwtQSIpIjjt5LEp5Gf6zLeku4f9pRsRZdiczaKlxby3zEEsKtQq1C6WFOjKHoG6sroy4KxepEnFXIeKuzIm7CifoyrdUgpZ9ljkDbymsQtzdoqNZ'
        b'CHlyzNWVET3MEyZ43QQnYVRKWlpMempKcnRCctwnJHYSyXWMyMhIcwyXq1bhnGwyJpJiEh5+Mi0zJjzcUha8fiUmjcdJcJfwC4NFvNQFbBIVkcyIeVoKi61YiprNiEij'
        b'uzCJjEi++HKOssJX+Jwotqqn8KV85pN4EzsI5spMT42J4ju0FE55VU7zLHUhOfNSZEzaZ/Z7yoFMWMazHISr8QlR8StYHt9RcsSlmFVXkCIEfC+dQ3xKUjQB9jIG+lw4'
        b'+KWItIvPue3ll5ZuImRQWJsEsBDeqwnpwgpICohPiTZxjM1MjiLwoGeWJPDwVQdaWn1URFIS3XFkTGyKjB/LE6kFIMhkkenM5x6x6jjLYeilJymPqXM0eT694lnI8dK8'
        b'Lws9lo0VaRv54ijLkzQ+5X1GJUh4CQow2W/nYLWH/zuTKA0hYXTM0lUtjUWgL0DJ6pHQR2JiIzKTMtKXUEQ+1qo3vivdRBB9r32ahCODTLaVVNIs6NNnkM9WCD5aMqK3'
        b'UvAx9ef2MHuoxJx0W2ID4hTioK3whHFF/pUm3olSv3JZLBJjkQh7s7AFc2DRTCwIPq3roZpZ4EjhhnJxpKm7HS5yUQr7sQpb6cVAQXYytbYyxSKnLbvNvfxIkOo/mYpj'
        b'GacFFzbUmKseCDPnfmmSC+4wZ9oyx7ugpAhe9wA/5kiNOq8CHVnQyEWpa1oaJvulNiLR8XDf72eeFvE0dhjFHmR9PJ65zYUIQkszK28sMlQUOVsoYRM0bxLKDpb4YC7m'
        b'SC2wSkkk1hFBa9huPvgfopSd1MTE9E3CNT60jhBqlxRuUXD9uiyz+f0NsiLla4Okm4IEL3tSra6/iPvjwwLXYBexInWRvol6JIzyilf8cTt7le3GEpJHwsN9JRrbRZkH'
        b'2arb15Bkw1Ljgzy5zdiL1l5mwcRP2seNy8JO6CtPS29fay8rcyURlpppXF4LBZnMYIhPA2HuBQG2zMzbNNXPF/pOesq9wpCLM6rQBd1ex8xUhLqM01i3S55JjgswESqG'
        b'5gwc41bRjdBoK0slPy+O2Lcbc25z6IABh3XyRPJNJMeJodMkkaemn0uwFtLIk89byNPIb0E9T+ZWZlmL8nRuSz1oE8NslgWPiLgMCyQ8ytIyD0QtZXNH4l0Y4hnzMAS1'
        b'2GVhbcYzuUlUGxWyucuxhRfTUcfK6OfTueWp3FgGtbE4DEVm6kL0dD/0718qR+CiA3NiGNAT6vDDw9QT8sBTEc6F8chTPaznyzyejtPy6FJ8ZMwqErDwUhyADqHRRCfU'
        b'QqWsHsEwrWoYnxjAvFCqoIU0hSG5qQqGsWoP9l0ScsxHoc2Oh2aUQI+lvCIB3t8t9DFoh3yYfFaUwNV2qSzBYbiLRfyEtrKkZllRAiyF+0uxrdB+iu8M88RiedisyB4H'
        b'edwsjLgKgSwtDjgoiw25biNPcz+ndINfrC/c2SC3HDjjsGA5MDcTNjZvcoVFs5ywUjLHOyJpjPggFGKxsLH717cHkTJVgYN499Rx1gPQSgytTjjFawuccFYIrxIJtQWk'
        b'F/eKOIXRgSEl2mt1gIJIoiHagnm4uPuMmRovrALTRlKYhKl0zbRMHNXAUS0owScZdA+JUi9ohiqe278N68+ufCIdJzKZOaRXmqSGD6AGKnn5LJNtdrLnHHCaP3o147Jq'
        b'2hpNJZGpVAHvZGMnL0+GBVATYUwXMp6JE+mXNS7DPa20TKlIz1hqj1M4xOnYCXeN9MuZakRKC/lQWjipiqM0MXt8aQmHzispwhR28VITntkqibH8neWr1IuRukFNEN+v'
        b'jh/2yh+4egSLlpa3CYYUdm6Cbr48LZjFJ9txYdlQGWk4Qes7KnXEhu1Cp5i70Bm7Hu48G47IsZJIW0mCQ/h4MwciQgRtdZzKoKVoqK6xcCTpfs0tCYxDwxkORFoHzOk2'
        b'j7OYp+PsMhVxhrX2XFjHGyCID2JLkB9WBhFy1GJ+ZhDcY9U/m8SkQJcKfUOwAFuJR8inEB9fmkITZwQMbMZFGEzHKS36RoK9UI9jYvOddGHMVohDW1jHKyKSPrv9fANO'
        b'MW5ygrMbKIfxQE9LRvrLvHyxxItVNj+lmo69dIccTPugPQwW4YEPK9wudmR9dZ/CrIBgd7DYD8c9iYL4WBGK6WKZvwIBYosU6nDcgZPvB/Ebwq9I4kUi7XDj/hB3gaY7'
        b'uZi7rpU+Yr/cmizWEgntOkR/OyT7YOpqpsBVfLO9mAsDjHeJ8KHbNegI5nU0sugom2GAmHO2yCIz28RNcEjdwXGclcWN5UNNloUyHyT2ChQgazeTIErAzgToPip0Bf+D'
        b'ordCOvuo+MYvL534cvJ/umoPTjn/9OYbjdvtLn9Y61w53fkH5be1TX63Y7vx3hKnXFFiepE4UzP37znGbxcd/B/dO99877Vff6ig+seHqiGnhvr/Opvd9/AjxdqZNDXx'
        b'79eVF9eEfhhs/NcfRvwVGn+2y/p6r0v32RbVI+9G602Wf922t77T6XjlVxJff2ebuVbO3w18cgL/Hqj6vd2Oxv/5jV/8Y61X4mzT+s0G8f13S7rfs/H4/VcC082nv3Jg'
        b'/ev2HRkTNpPu47bvB6tHdDZU76w8XBrSmqjb/Z3ewunhL59s064uHL6ieC/v6d5rN0v6/94KB/b92uH9d5V3KX/sFFj8X4+6DTySHb648aMPNc+d/MfR0wdrB76z9eIH'
        b'3QNH/66Y1Vv1w9Ksr4vs//u1r30l5TsXP7j8RNHvP37ceDJgJngxWCPQY/Avvk5xA9t+nf8Xnzd/8ebu0MXIf/b/5aLTtMYfPtx2cIty0kOb9NCCwddOR9Thn+ovfy/h'
        b'4Ol3rlz6e/O6tzyvtDm4H3aemik889dro++EfOT0tS+/t9Nxe6rxV1Veey3Z9m+lygYpv//eZPUf9n1w6Rs2a//jH+N/sgrZ/q33/+vt137330VB52fL+o/HBAW6vGec'
        b'MvaNr4bHTF39ksUv/fadqkx7PesLse9EnR+MXLv1dgfEun/32iOo9jP6xZ/Vsq7dLX7cN/LgS1nhV75gURg79XHE4k//8qeQofYp88riwO6/rwud+6vxw7+Zu6j+LHDc'
        b'Su/d9/z8J8/02Jpfaf+11f9cvXbxyNzXD85d/3auUldsQK/xL05f/9JQX7TBuZSHe76a/KXy4sdNyev3nXLe8OMq53vjfrfm/9Lx0x/ttFu/ScvJccZubcqtqbf+WfiP'
        b'n2qc3VQa9N2rP/6zpNWp+w//3PxNs4/ytvWaWQt+moEjomVu2V0S5prW9ZJCezZRGW4Ww0nIl8sT+yN3Z3oKlS5mYYEVvpP5yQOwZP1hekYHC6XAisLy4W9mmmDv2Rf9'
        b'QCpEZ3KFDskLO2CGhd1hBYx4y4vmEPbMy0opYPnJZ9FiWJZlKQ8Wkx7mkWabYAKniL1z8xIOkiz0APOduPln8y58JItiwznMEymxKLbz+JTHhQSF67IulPJAthXWJfrH'
        b'DI+Ei99HvF1eoM0Du1mNtq047SD0D88JxSYLfz+8pyRS2JvqJIa+uG186lSogApZcF4qdMssT22HuWGNyFkftj0rzqbgAGUwJobREHjKZ6WjgkdLtWihGydESuGSba6w'
        b'yG1q5jCR5WMBQ7RepdswKFK6JtkO4+v40MYwobS8MG8IlquwyrzQAtV8ybs3wPxSdRb72wqsXXvDDeEu2rF687NwRBjDh6r6EujAll38oHEQGl1ZkMRuZdIhOsU453dq'
        b'zz6hEl0XwUOL4LxQUIBG1ki7LQoXOBR4Q48+lloiAUkpHYjfQeYm0Nstxdo1MMJfP6QJi8zlVx65dpnHL0PKpz1CMkjVM1dhO9TvCcR+oU9x1ZHUZYLw9XMkBytAu2B4'
        b'nF+r80zehcEsknfTYY77VJLPwRNB4iWR85nICx1GfDkaUGT+TOIlhauYRF6c2MYPWJf4T/+SzAvFlnKhNwXu8LdNcT5xSeLFIZjmEq82jPP6NCSt10LjS0VeDdPYHbYc'
        b'AgySY9ggFlhMch37WouUnhTozRCcQuN6yOJVincHWEkIluYZVJrjJJZk8EDkymzS6ZYJPZdxcg2OiG3hjtgSOxUdvFRhAB/xW48gUXTaR7gZupcUyFXBJgnJItUXOKJH'
        b'EaAO4T0YWapiWLzbi3fw3nBMAR5kKgl21q5Y7OYlEvcR9oi2aypjh0TllCIPyfXbC6MyXmmDj7O1AngQ6VqCyAlZ0RWGfkaQSyept01Kwm4tFnDst77khAuqwkPWJGST'
        b'DE/zYoMCtOwgEJD1Crtzi+S8Rv5UgCWJAXQ3EtG6fQqHzkAnP3TnsKWZVhbTZdU64WFAODag0I89CcZdeS3HEqw5J9yKOtyTYMcpGonvMz80gru9iy0lR2FOpOQvMcZ5'
        b'qOMneVwN2+UBu9h2Wx6we9xIILYVMEcUZ1zritVlGBSooSr2SWDwOg7LGsaEBtJNWJmZMm2p0UM1TgJjajhmpvWv5zs9swX/G7t4L/epR0RHr/Cpf8QEq89nJd9vKNbk'
        b'ga368kLRGuJNvPizCv1v/HddFQ2JiliwpbMCNLq837YQ6Mo/SZSWl5ERK/xNQZ2l2C37+ZvSb1Q2q/CRWWMUA27RVuGlpRW4VZ41N1H6UEnDgHUE56thQbaSj3WlmmKh'
        b'LQorg7Oel63R5MG3mvSGJv/hXb0/VpOu4sxcdjyCTV9VMMzLLeVpAcxYL7eRpx1faef/16qAKwvzPBuYz8gns5bPzX0EJ+lTyav5CKx/8hmcusvOwUz6lsqSH/VZCmGU'
        b'gujZf0qiZbaxYJFIyAQSHAOqMseAmLsGmGNAUqhTqFsoLdSL1ZO5BRSKlPJENxWzVZmH94zohiJ3BSjcUgxa9lnmFgiSrOIWOJUqC/Rd6RXg9vEImX1X7gx+ua196YmV'
        b'yUIZMlP1siEsZRbrqIjkVc2YkcwjYcIbFjGT48v9D69immfOjlVnNV9anrkJTwjiVtSldQg2cWFJzMFBS08W7NCrm8VN3FOiY+wcTCIj0rgdV9hwWkxqWkx6DB/78zm5'
        b'+QHKvBjP1yBazf1Aw69eK0Nm3F4y7TNr+qdZfz+vrXf1lj+b/TNZCHEi5jG1lzdIZ93RA5f83GfOrBJHVm6misNGa3lSlIGPznKLqiezMWJRQJAplm+wWjKuKoqyScKD'
        b'e552XEs9jHVKG4K5b5z5xWHIhavK31NmrVlEB+4Zh/tmOsUJrVlif/anrGLenIW3ZgkzyjzC2DX2hlnAIyZLF+H9IGYL9fPl3PYMFh2JeS6ad6XSLz21Bnuh/DA38t6C'
        b'CizEcTHLyOJthSOhRsiBt73yD5G2RGQ4Yvs12z+n9ioL+voPGl1P8q9/oXtW9LZIZOO674bi+3pPE4Wvj3W68m/Xm18U/ye9/GhbeGhM5BrBiQ/z2VhopwC523in9GB4'
        b'nOnOfl3gjiPLjdtYZOXth9XMpmu0gUmOMnM5b3bkE+jpbektlKYjwez+Gm8FLOXW9dsGRnIzL8nIPZ8WCYhz6mZioUl8AbTB2IrC+jAIo7Li+lAFOYKJtSYNawXb5wEY'
        b'k5dixRzs5HVfYzUvyBdgbrLM0sztzKZyoynkwoLqzSvh/KTyTVjJb5GKn0q45aj7NZl9xDVROMfvhZ8WTYhEJq7OZWa/VL4kTdNl3IIZzM0UuTF9B3YawIAo2J/ZTa4Z'
        b'Cx12YSwF+kkONFJnkmD2BWziphTF6EQLZci5LXTmbIN8/vBF2iuWiuxgiltNErGVG4PE2HLQJYUJvgQ6paRz7RfD8KVEbuW9CndtfaxJvJtcWfPz3CkY5PbjM1rQbMmG'
        b'XVIKSCNQPZ2Q861ChfRO4obvGd93DjyY/CNX7Qc/PHfrdLdLTfTBknd6Nd9++A3FMAVxmKauqySsQvL21/ZHlARu2a6cOvo4raTl9fo/uNn62L2R89pv5p6k/NjJe7Kw'
        b'6H2l3/xX15bfWnf8x+aUTFO/Jzp6vxU9/OB1H7N7j69/911PK7/7D2Nbgh/cqNg5+4Xv/OlLh6Y/7DJvDIzZWV7zl4tGOVtiu39//IqNeFGU+93/sgL3a+rv/MLjiOdf'
        b'Th16I1n7N78rd/h5l+YbW69pFPhZ9mX99sP/fVdhg3Htliif8xdcvF8vj00ajhi4bvpBXo/3ZY/J9w+tfbI3zv4ndYk/3+508Zv9g/Y/vGnndeHGX7env+n8u69/ubDl'
        b'Tx96Ga21eveG5a53N79zdd9Hfx5903Iu+v2Y0cJ37x5+426I89Xbtd8vatP9xkx7yZtxXaE1r6d7NW+c+OZXfrhwuenAZpMtbXurPzx6+vIW/0mNO5Yz740FPFiU5m6S'
        b'2L6x41z3+r1nZjXsWkd/dPgr206Gfft7r//zjTe/8zQjcqBoZ4fl28M/6L7+leF4j99/89pH6qMRh977weDPbz8JPPT9g+3NG32rreqDrlZ+eCPzZ4sfS03HazP3/tnM'
        b'gGuELtgNd4MN5Vos6bCZ0MMVI/9bMCGosPAEBoSsOlJhoUWXaws4gx1QJj2ymkkiD5sEowEU4YK8ZkTGPqUk0vf7cYaHrWpgyU6osl/SdEnLNVfidhJr4yM2dktWCDE8'
        b'SIBKniYAD+EpFqwIWLVKlYes4rCxNVf3jJGUA+xxIYKwrEHlKC2JB8pM0W4qhRaV6z3kTSolO2T6sxWOwci5MIvlPSixmxQ8NnQwLmAN73rjdlLoe8O73tzZxw9Mj5b3'
        b'wIIW5JVMSEObUt0oIeo7hI8FDbs6DGdlhfHdCOOgSWIVRfoO02e2YRFLvH2m2FuKLb0FxT7Rj+tTCgehjlYNHXG74ZGvLIRIa780LAk6+OmkQCvOcdUM7/sRASVeYaEk'
        b'2sC0+HsJ8AAHjvIteEIh77Uu9OgjpXpeyViisBbz+ToUt+DoMkXSSxG7sEfQJLepCUriXZiCrlX0SIVoaLmylT+jTceUh3PiVfRInIDJDOauwi53rBSGIVWu+0VtMhwf'
        b'4UNBU+yHkSNcl7MPZdocV+VSMP9flNv1/o2623MKnMbyQASuwQ0xJvC5NDjS4aw1uA4ltJEUGvyw0qHGHytIhHKialI1sYJEhTf0URAv/a0gZo0pZe9KhGaTgp6nLfsk'
        b'NKJU0FL6k+bSZ/rTgM+ly/8kbWPD82kNy/YkqF1KgsJzSq4EMZ1jmZ6l/X99xGYKyyazls/Ila2zTOXQWKol87mULVGuzXurqFufdABLUWHObDkuklVULSaectHUW8QD'
        b'vhVJuRKq7Eu4uiVlCleshly5UvhMylUcKVduqwXULilXz0rty+NjeVjt/3EYuPDOUh0a4b1Vqktam7gL4TR8KS8JE+JR40wDo0e9ggIO7LfZwzSeSxEZLBgkPSMtITnu'
        b'pUsQCuA8C415vraf8P0rJaSoCKoE9BLJX/zEiNkC1ZWCaI/+MaHsQQuUQPOKuvkwAU+lwZizl7v+wrAPyp/5qFn/VOajPhIm+C+r0qHzhcL8WKwnPYyDOJTw9jddJOkk'
        b'/Yly2l2tSrYYgI2+wl9TvnPYLfe19wM9FZ68pxa4tsj1XKLnF9NKf9Z796/9V37x9S/1fd9ma3rB/m0lO05e3/hjjd7/vZu0uTrgUpyedNcX0l3H3vtd1qYvZJ3aldhm'
        b'tPutkh8u6JcOXNym4GuQ8tF4StIXzzxeuDjn89uYs7/eZFi3OTzPTnmb2dSbZorcPH74NnFqQbC4sZmLFvtltcuxn87n8bKkl0vbeDTseVuBx3RuxpKVcgUuOArBsPVY'
        b'xDmV24ENK/klC4m4zznmFqF2Oo6dTl5mYvfG9lNarHzcMvLxLzGQZfRdM5Nj2woK7/8KFJ5o/HrB/iY0Cl6i8iq8bVv2xucI0MpZV9DglcRoGQ3+fFWvicDy951XUllO'
        b'YMPod9c0ZF18Py+BFeVu/cMqJPaTd8hqvGYnpDKjzL+l9CPLqOl7MXo1LSo+4Yqs8I+sRO2KUkOr0FB3wd6RdI0bSBIupSbFMBNPTPSWl9Jb2caeL3lDv/4s7U1Eq1Is'
        b'BX9uwjiKdxIFR9bzOuuy2Kixy5HrVBKgEBcTThjtkKSzHLqv/fiHLBc8+LUfvD5RMVr08K6Z4pd0o+JjkyItI5Jjv5UTH/kzX6ko//vKj9+5ZqYgYF0Htp2QYf3JcCHV'
        b'rXU7F71NsBhmmEYxR1LlUp0OplE0pgho33EUmtR9YDrsBY0CHmFhBoswOQiT23Gc4fwolllhkZdgzvHyu7xEKO5f84EBZRixx5pP7aamHSHc7RKApUuWIOgVMNdBg+X6'
        b'bH7eJvvcDCuqrJ9biZsrK0w+e4Kj2wX61Pjq6Kb9rVXQ7TMtNu0dth5Ff/+Tx/zTLoq4HPfJJeue1btgibU8yY6nM/EgeW4F59IZpyB8X8KhGP27BfLPSM7TDtNHzaXU'
        b'K1bFTk3dQCzZvLL6nLaCtraKRF+soqUpVlMzEKusV2IeCjrenR/r3rIW6yabiFU26wsGqI3Y5v1iHrdEZLpL0QwXrzhjY+YfJaw+URTp4w+gyjkFm220oQCf4NO19vsh'
        b'JwqHlRxJSayEKhXS8B7gnc1rSI/Lh3Z4DNVHjkCnOlRBiXgDLsATXFgDjY6kapXDWARMYt/JNRJk7cyGnZ1gAUY8YcGDnrqPJddIGe6Dx9Y3oMsXhpxu4Dw+VMYR0rj6'
        b'YXYfq/iIvXGXbXdg4x7MwY5k0jHvYh+OYfMNZyiFXtbdZ53HZacAAyjdhjnuNxPt8B7Ow5MEJyy46LF+c8T6Y44+iiG2160DoCvE2AqqcdIJZvAhjENFMvSzmrgw5QlT'
        b'DpfM8b7tBSxbg73ROKJHMlA7VGEn/TzFunB3bDpulwj3onBQCVphCgtSYBQrsTUIB2Hk6iU6toWbpH/Xn4RKI+y8GIp10G2/Foc84akNlNHeK6Fc5wgMB0HeLh9awBQ2'
        b'HYDhmzgQCI1i7IUmvIM10EJ/348natMEnVc3SdWhBiawzdaSCNZU/AE1J5yEwihjyPG4BHejadh6P5gzizqWsvkYlieQ1tvsjbUhhjCY5YbTMEbXNOKsBA2BZqdo36VQ'
        b'C/lqO0/iuCERSRYm+cSPlPGWYDqMWqi3xCcHXHY4b9fXwzH7K6fpVy3Xd4VaYCP2a+thIVbA5Ml0FlupqbYVF+mdfhyFYVrQiAjr7WIOYmMYNNvCnC62aUb6QXlchgvm'
        b'nMD6TVB6Yb8KLsK0sR5MJ8HiBiiIo9cfp5Ja3rDHGDujt54+67wbqwkSpqE3PYKArg6bTmoYhWUnH7yOE8bnNkKTP3QaheIwnVA9PlKh7UwQRDVhpyuWqUDhUZy1oYus'
        b'gwEH2udjWt8TyAumO7hvdYgAoiQLxtZtwBI6oafYrnlLSiyg2GO7Hs5l3pfwklIL0fDghBuUE9hrwByOr73hSvf78CjkbIIWbLDS2ItDdEOj0Co9Cr1REdvMoCJeAUpN'
        b'bu+GngOZ2fFaWEvA2ImP6GzLUsPPwPzaYGhyhSYYhW7Ii8AWc6y32InTOAtPpDCiijUbcCpCMRUfwMSpkKuHsPlmUBIMYDMdxLwp7YIgBAeTfQ7SEK3G0Iy5x4Np7Kpg'
        b'qLeHBiiMJNTLlTj4YRWMWNEzY/gI+m+G3tTTDr4dudcjDlt0ru3VQcbtSgmU8wgr7uwjtCr22Oy7/dpOArb70IiP9xCQDxBwTmNRBFYlwRzt6Sg+hWJlZsKqug5tmT5u'
        b'CTi4CwtNSb1YvGFvfRsKzqsGwbThJlYhDR/qHFBIwcVwHJNgRZZBxFG8C+NqUHbLExow19gDykMgB/OjtaANHgUEnbKN0t1phH1uHmr6utY2ihvsThEKPfDFoiC6XqId'
        b'9Fa/IRQRXcmJwN79dJdP4Q7mS7HKHypx1ARb/LEkmET4cQUdAr+SddBJW2GkKf+CLTtdKMLHMHE1ywjubaI5BwmqHmURQBRm66gQSozHYg3O3LDVJzWqAe7S/YwQ6ZpU'
        b'idP0xjYjGML2s6dxgDAvH59sPgfzfj6wCA9Vt0NVOhGFXihwiMHxS1gcDPPW65khMCwAnmwgoBvAeyegysdbJ+wqTtJ8vQQMraGQSyi0SFvLtcUBvV1B29cGQC4d+mQI'
        b'9iTR8T0KgDEznFaEhsjt0EFolpv5PYJJurRF1gDphDPcZ0BJC5+xgIlMB2wJU6CB2/FucgS0X1Yn1Kzfd9wSerXDfaDPBcpwio5rDus3EDAtkL5XBWMw7AUFodB/hW4w'
        b'fyvOe7q4OGODN3RFa6thPsFtD0HWE7i7DZpMrhAg10tcYO6aaL+1F1ZfzLCg6xtnZcSwBGYJgaoI85ojQ88lExHptMTmRDrypyyWs4Qgth+6oA5rwo4ScVy0WHcm49x5'
        b'aPejRXZjBU6YEoZUHtpqm4Vl+qowsxxuCUvqjhvROiavYp6V6m2YSOZ0s0bzGjQSwex1892fvSUKRvyv3zCQnveA0nWQG0t7W6QBeunc8va7EBQ3KF+Ce/DwAlSvoWvu'
        b'M1kD1Qew0RPaM9jRIttJG7YSZ3oIOVoSzHMmQtKzVhmeHMBZw50EEGMwa4sL+lexK3ntNYX4JMyBWsLaAqzRooPqpu314hyMH6cb7dTBkpCN8QRveTjqCt106nNhu4g/'
        b'DYVkGRP8dlxyxopw4mL1ZtB3ldCizJpuo9PNlihdMfOPQHvY3ov7sNI0ER/dPKyZTQvMgxyC5k4Y32NiGh0B40R0nmjoYzXOYp4GFh2DVtuTBBLQcY0WUIz3TWGSJNgB'
        b'uJ+NncobttMhP8XuYyG7YQFb1I6Z04YLiEy2E+tuPgLjHnEn6CLH4U56CF1nIzHFNniajaVXoOGccgzWOcd6WHO2ft8ng3hOQSZRhgp6ps7JY10w1kPzRSiRXDGEFoJw'
        b'OkGCcGg9m0irXMQ26Y4U72NYnLwGK2POKG88j4ProZ5B1m7C6M5jOpB3LvM/GWTPqeE9Rm2TuYwxh8MWOCU+uikc2pWx8YSaGEZZPHE5oU0DVGTAmIgo7va1mLOHzrfB'
        b'+DoOKcMsdMd4mEKTOwzoEUNoMmJtDjWxRfmScSLBTJMWoWODrRkunLL2hObA61hjDGXem+yJFzxRo6NZwFLl49AXzrAlQpwaxkSiB6zmxNNzZ4hgMBr8mCgBCSEp+6FZ'
        b'z9XihC4Oh0Bl+BG4cxRmtbHd43YonUu7/XU9KAvyDYG+HThxe6N7OFGOfrqOgUt0KAPQHHpNjHXH7GDmpM11TXfMhWZocIki5nyH7rjTUIcOuwC7pbCog1Wn1mmvJ95X'
        b'og8V53wjThLqztsFOiYRElcHQ7U15Pnq79bHR0nw2JUwrygRanbiHXcx5igeh9now1B7LAHGXfzhKRQddnA/ems9NhLoE13sofkKRZeIC3TiqBK0Ew4UGxCujNFR3ccW'
        b'W5iHMiNC0ZYd8PQmTl12IZBtIF5XjnVOl7HTjShKTnRgFhR4pBD4t9+EuptrCagmo69hX5whNhAR7CAaUXIQ753R2Y8E7RXY7UGyEcFzj4k9reEBfepytc/y0Ca+eGQ9'
        b'jAcRED6BiWt7CeHnsd+dCOG4Bp1cPjG+NvtNTCxLg7JYk10MFrFS/xCnBZ200hxoTYC6SJ3sK37YQhNNEF7VQ1UCLaiPxII8CZRn0tmXGV2nHTYTFx0g5pkeDB3W2Ird'
        b'hgFrgohXPEw0wI4YrPWiK+7Fp2HwIJxWOeRCymI3FjnAXWRoPo91p2iIwvPxVxgXwtxLRjieSuRlDPO3HzurhiMb9hwL3LgD2zOrmBgxgnn6BNi0BbkcYYHT4ktYTnKE'
        b'8wELeGIDI1fUdzkop5EY23DsNFYdpq1Auxvd8TzNPJ5G5zTFSFDwViiww7w9EfCApi6BkdTrzhqbfGAehyOxjZ4ZIupRf3sz5FicZpnRCgeIDtbBjPn+QzhwjsS0WpyJ'
        b'ISGznPhYP7HpSSSqlnfbCmt0CWyLDp+Ddm+sO+FKvLUixpUI7MCJU+Yke3TDU0easJykknaY0yL8fgAd2tjnCeV7srBK029z3CWidrnKhCOt19UuwMgOxyO+hs5rCMwe'
        b'Q62m1UYFOrYHaroOOLF5p4r0GN7ZQieZs4NAv0dnA3H6chpzMAzzzkGNGxBtciFeSOSJJAWcvYAt2HrwMpGsWnhIzKSb5P0RuijxcavTULojmXh1MzwOwLyz2BnmCCW+'
        b'ln50cnlQ7J64IcAjkMkyJeduQW+kGd6Jghy96yZYT+yqMhSn0gh46gJxIByLrGygXkKQ1uaLhW4EX4tE1wfjzpFmUkG0u9jIkE55IhyrD2IhtKUcYPG7tlDgQmDTjZV7'
        b'QvRj9zsEREJ3OE6nhBFhbj+opbbDzl7fyM6MqPqEBhbrHfHfRcxwcQe0nKJRq9YQbC1cgpITpwlPZsOgfSf06kfjaDJN2EzbfHCesKEnNGYtEaAqGLSGYXU6zBKsj4Pi'
        b'zTB2LvX8ukPQn0QPDUJjLJGIRmkirSoniCB+wg7uO8P8LmK3M3j3tj4uiJKw2YJgYQRyMn/I6G0zIUI+g8vcZA6W8wSWWTgQg4+uqdBTeXrX6Qhzd24kQXfC2EYXq7VJ'
        b'ojxzItsTKm5v3nE9EwoiDI9f0DhBLLyL/UDePqL+dURM6DVnJjvd0F4Dj7Poamex7fQhdWKXU7CoFY492JhI7PahIuZkYu3JGJi/nkxfNUeeI3FmiIsPQOLDU5hPIPgf'
        b'jzTE/LTN2GNKcNFJ2DNwMhkrb5gQiWhhUm88LaDovOMlQ3V6o5LIRx2dR6lfCEl7/TeDbp6Jz9qq4Y8kuHZhz1ai3g/DXLI06XhLgSFvBUwnp7rowpRWBh1ObhqJFBXB'
        b'/naq23Ek0h/vQF0QPTIFd5Wxf00MFgWybqn068JUaNIideUutGbh2AUC1ZHdGhbeRKAaE7SPJV5zIRWqcyNh6TCdcukGUwU6y1obEjkr1ulDTbLJ5qOEro834owHUa57'
        b'pKNMEEueTWbxxlh1eQf2biPtox/v3oQmUysigNPKNFke9tp5xNhlbQmLZR1RCRvyMgkRmtSgag+WX7TDZt8dhAvjejrpkUQA57D/LPafI7Tp3kIg2GJPMssTOyjE6dRk'
        b'6MogRbyIFOZ1NvpEMOsPsXCcg9uYGzYe7pHQoIiPThG7LCJIrXa5iJOnjDBfAWpwOIbmfUDQ1iTadtU59Wy6wXG639Gt5oQuD6AyOgNaXLKgZBsWK4aRtFqjlAiNTvT4'
        b'GEyQ5FmPxaeJWZQyh72+rya0ee+8HUBA+hiHskOSSFisD3I5as9UtAEH6HFLMw8j2X8S7vvB6PUE/ViiQY1aBOMTVtgVeMMDq4+ZE1AMrduKubt9E09heSq2mSnx+BIr'
        b'GHXx8VIUiXeLbhBYlcSe5TlsCnTO9UuJRvZ02zVQEyFErxQHxfhYSERiV9FOXZIy5vbwlB+JtRLLGRAfEpEef4d+P3+BD3QmlvhbKZaKRWJvEY7RDps9z/AoFH9oMMdS'
        b'SzGLsiLa0ENyZSc+zvSQslQn40A6pWqSdMqxyVWDDn34ltrmUFWoO3hCK0KP+FKlNcFCJ51RLZPYd+Jdr2N+UJDoYmBGlOYJ9hhlE3PqgFYvbbdQot8V0BKJ90lgIfTF'
        b'tv3M7ELqd2WWdaY79BswKe8m9MREYKE6dKRFEM5Uw6IL5JwJxFp/ukj6njAx/yh97IaHrE9m4SldEuGad9NlPbA9u53ALncjKQOj5iE07n1RAM2ZH0MUdRgW/YkHV9Nd'
        b'k56TcAMKWLG/ypNQsZNUhTGCiLMkw1TuJCI3CFUOpCzlZ1zwgwUfAvduYhOlBFhjxqQ45ZFyVuRgdgMK7UiAmyUqMUL8oB1GtpA8/AgaD8QcuCLF+8oxWtjgeRH69uN0'
        b'msVmnDmPA2e91kKf8o3MGL+0C0RDK6FblVkPoMHYCHPpbAfo4HOJPvaGnaWxyuhI60L0EwlpZ2gJFftot73O69XOaGBrVDjXvpqkmGdLekwOHcwgEiVdtIUyKY6EmAfY'
        b'Yn4wEbWOgziyk1U7trMAlt3RBxUHSSa6T/vJSVuXyRrBVqTTHrph/kgoCZTVUGIOrcr4OAErPKH2ELafIpWqjFjrvPJaLA3fEmXmvgEfq0BtONSmEZbMm2lmYl9UWhr2'
        b'0k/VzTW03OL9p4NJjxwkUlxph2PuHjd0YqNh0nQNTGlimyfL07bHwd1ehNt9UIDMwlOsRWr8BOSuh5YLRAeg7pDnWf/QtDNn15FEVER8fGbdAaxJ221HhGLsipToQw88'
        b'tjKAxcx4HLAnbaDCXA+b1jEyTvyu0OY2oejkPpIYi5lNysw/lvgpPNnNspI76IEnoVCYTCy8G/qPEPIO+tyGwQuk8bXSlQ56O3IjzJyUeExbaBxpUz1w337dhlsWJHtO'
        b'+DNFAitjCb06beiPRZw3MYC6mHTLDEOSuAZccPr8Gsxdg3NiaD1/OxTz1mb2MQbWS/BV9Lx9htB7yMXEVesKPjZQWn8VO6IJO3IjiTCPHg/FEm99AzdSXRahPo0Os0Bd'
        b'X/HsBd8TRAQq7NYT4NTBsBH27jH02eIE49dJIygMNgywinJTJp42HXiaG2rGAjbTJE1QvZ+OhJSWdhhLJpLUSSxlPh6nMmHKjLXhdbIgxOjFlmT6x/0re6GJeBqR9woG'
        b'qF0wag5DNimsTo4jjkWH0jEX+J1ex4RNJDrdc0ZMEt8cYXWuMYsI9CAW16pgjA8tiPKOY5feaXi0lShOOTS7pvmSpN0aR8JnnisjraOQezOJRPwNriQqdBlpMfOWLz7M'
        b'1nVXg/5L54gKlwmGgPQogv+KiztoWcTPsOMWkYIZY0KDB6TkwkO/86JELDycRDSn5fzhOGIM49gSQyusyiAunEdvkFCOD6KiYTjpuD1OrNOGhW1nCRQa9LHHzZqdiDn2'
        b'rYvBmQSCGibp95P2MJeG8+cVnbSxccMerApIJZpWpoeduqSBVV8nYpkDi5dJ2Jk4BH06AaaH7LYT723H2hAV7PBIYTUCTHdlbjJLMDjuoauD7Xq3Mx3XQMFhiT9BfD+B'
        b'XzH03iIy0JF52hNKQ4nO3rGAaf0YFoNEWDF188wlYpXJUC7FUfr3Y5J/ZiKuELVtcb4RjD0hVkSTmnDADJ4ePg+Dm3d4EUmoZhdMl7CAtR63iPwPwaAObWQeF28d92X9'
        b'hfZB1aW1HgE0++wGOpGn7jDtRkS48ILi1kMZdB1T3HBzHp/qwYMgLJWrt2do/ntQv3cz03BDTqiLYVIXi/xhWMkKBkOVDKAPiQRO7CM4GHY4jfNQYp3gQBBayW0m/Vut'
        b'iIoxW12jjiXkE1EjEC2AEdIOcOFqgJUZXdgAzrm4QZ8xNGoZr6fjL4OJaMLWrkNOIugzIrrSvwMaHTBnC9G6MXgcjG2noNk2hBCr0AtaokOIKQyfZgJKJ3aEpO1SlMY7'
        b'Yd1u7MnCYmsY23YS85JtoDvxMDGGbtrxQ5JbW44RwYEZX+ZwK7EMIe7RbE4Yfddqy5l47LFfezYNF/wJ4uqIf+Tv1VeBtsRkUpDqOY8c8VcmRFhMDSDdvZKApgy6s2nf'
        b'xLHWY+9uqM0khK/3TySQIuWl3nJNMuSrmTjioEMCNngbXII56MvEZgeYdUvDejq++zhyehMsnhQdwLtrVHBRSgst8FsLM4rMPNLlAL1xBp5Qd3TDegdSvEpoVzh4kAj5'
        b'HMHFMCHCEwKG+cusMr4enXtjZBRDnth4U6Kr9yRhbnGXNWAyFHsTA/wTYs+TpDqmSUtoIp47oIZjPlAaBfWnLdYBKRl38F6iRgQ+Pgn39VzDz13HVm+/jXuw0gZHN8aH'
        b'YbmdhEmuRIbySZduwznfrBu0+9JIbWJeHbiwSWEH1OmdwIKoYI/zh/2OEVSVOWNt+oFonNlKJGmITruUtEOlC0QfHquHGHMawwh3DR1kQ9ReGMXJrWaEvA3YdY1wrhxG'
        b'TEkDKtVRJv7Ynxq8liYtjcb545fpbu4hSQgVqjCle9CaiFrrNb3bWrsIwRqJ4ixYYtEFaLW/BFO22JrpTjKNrzfWroBs0m6npJJ1+AgrXbXSoFtfKXEXs1nSXkaJItbt'
        b'EXuf9GLqUxROR+H4GkKtSdp6h+VBTawwPrtRgUC8ibh3GUnwj7PpsGv3nlQ9xcI0moJZDCcR7ll1ppLDgPEpOm3Sq6HcAPODjjHZR48GG7ywGXpscfCoOZJA472RDqh0'
        b'K7RZb2YdEpygeS2dTHM6cZ2HMTAabExw3iQ5sXcDdBk5QE4kFO8m4deZ6OHmU2YbiFJUxWOeKozGpN0mxpUHEyH7iaeMxzAiXqqccdwO+jTs6YTvY6PhBTqjGV3sjFuL'
        b'Qyqm2W5Ol9fBA3sY9r1BMNVDnK8bG41wKsMb+3RJzrlPTPRpPPGCbDX3NLrCVhqkausBvHMuA7oPKuzBwUPb4ZGLGrZk4GPt2HOG0KujfRmq12KZTxyNlQs1lsq2fnSj'
        b'JGnQyUwrmPilutqfSMShrUQc+giJWsK34uIxImD18MDLzZkVSy8htCT5m4hXFUypx2LhPmLQBKOl7jCyXlVM1ODJhTAifT10K9M0ar7O2jPEx+9BlwrcjYcCB+yzIh5Q'
        b'dOsKVB0IQ2Yr7xTB+PmDG4imzEJBwi5CtIeG0GFFWN5IODFCanVLuKrRPny6DupPHvBJ9SAW+gge4aACvXIHxk30HUjr6IJeN+hXNCZcaoHFHWuNSJy9Z44VN7CCnU7x'
        b'VRiTpu48SL+tdILOXWdwhngl1ulsd9qOrQegISaYQKcI69KIN81nheLwXqdTkJeUQaSxxlq0H3ojsvQjI+ngk+LxKdyLhJHLJEBXkvx2j05r1JEoa/52B9IKZ7AwzdEn'
        b'1pnIQBGWXLeiwx3TEBPw9Wsw4ZjusjE6PesmTAfQP7ugyZdU9DYYTvXEoTOcM07gU6dQF6g3Ja5J2q+HM054k/w2rB69hwS5hhBCjkXlSJLWckhMrsyUEB5pHadrJDzK'
        b'JXBmiDSPTy2IFDcQdE454IQhSbrBWK2W4A4D27HZfTdUSonBta9hTzhrJ5C+OHc9ztOTpIE871MOJliQnULS9Tw+dKPLH4M2VZzbr5xETGdAjB1BOLvjJuSQ5le785iW'
        b'ehDWRXP/2iAz89++DjUwyyxaXTBzgnZIaNLLrEUk5vZAr6cBNl47sevsbtpbLfY7Ye5tLMdJY2KNRWHQdopkrUkrpfgUW0MY8VQjvH9MD96zpWMtSCIcmNfC9nOQTwLB'
        b'CLGW8j1YsUGZ9tijaoVDN+JZLHVkFtx1Jq5cDu1SHDNUxebThscMCVoemypqb8Rpn5RDp6BC01WFiOYs5niQPDPASNo+HGItDGvxvo1mzHHID/UxPZCRqIbz2meydxF9'
        b'J6nc5dJxuJ+K1bZBpFQzOXTcIf4GgUfxLhjRcfQhLO5YB7NqMBV8LckcH+0gukWKHeSfx9ksNSw4GkRokc/6sBDVqSSNZQsdd/0mfKChJo1dh6VnExPOXbDDJh9N8VED'
        b'em8QKpWgSmcdoVs1PEnU8LLYjVObmP2TGHcOzK2HJ8yH99B4Iyl9ZZGHnEl6b91Lp9EBQxutkqHSdxshRTkpPumZ0LiXbqHACyed1El+f0pyQcvR7HXYqXFLkXZQdQya'
        b'9FRvEL5V0b8qYdEiOfwatG4hlTJP90AATBpCi7a9s8ZVvOON+cYXlPHhSaiKh1YYIDAqPxHCDKb4MJPZu+jmnxLxHSEWkYfd1lh068IW4tEkBJ2mZx/4s+DyMziVbU2S'
        b'GfQQtlQTmy5SD4nMPEv42AaMlZBA2r2f1Qy5CTWbsCqGZO7JywQvg1cNCawGbmLhbSgmQk6Sx51gmrkepjPfIUHJR4U43xIauDKz1P0zxIKJfiUeMjmhtR0rCAXObL9O'
        b'X7cYxUWpGmK30YHtdLuLOBQHj5U9w2mSKZKQeiT7cWoDLOJD+0R12lE+tmcA8wLnnnWCKgWoMyRaPncVG32gU0ofe2E2hpjNo1tEF+8TNtXQXVSqbcIub6KjA3T0ZVh1'
        b'AxfhqZM+Fu+Hp1bYud0PS5OYm8uL2amij9Ph5O8kilKsoYD9MesJ8CeumRCSz+wJYJkx3Xq2tLYqGwOs27bZDJt3HiVp4bGuLYy7EzjM68fjpAY2HdyCPWtIb8wPgzx3'
        b'nHGFAdUsIi/VJPzUEmnuEhHMzyrBA2NPqFcnFaHHRgs63PZAox2JCvmGJ9fio217lZSwKNAdi9Xxjvtx0omfWpN8VeiAo1qpOLlbw8cWOu2w2s3RlY5lHJoUCPG7idYX'
        b'ZIebaLP8rhmiBTOQa0LAPigmqez2lT0Eb9UnIF+dg8XMBSLfixd3EkVowcIUOrdeRgkmbUjyqI6Nh64DBNDMBl+NJetwfD/pNZVxUKQEnfEm8EgBhl0ccYpp55gTSARs'
        b'wvcqMfQFOyWSq7ugzBTzLOlohg2g8ybU67Doyq3Mpax4Q2l/3EkaucZJE+tIdlC6ygSgPL19yaTukUR/h4hEJfTqYeORdVksuiKITq4JZs9f2QH9VjB3DLrMFKFxC4FY'
        b'czD0XSSVZxC6rC6Q+EN8e79jyl6Y9d51GTt3QIM39FrYHMVxReIo9V5bSKt9gGN7iL/1MRxpDNI9YkcS9oA1Lp7aTrSt/kS45oWbJ9eHEOgUYc4+X5qjYZvzZtebIhIu'
        b'iy5iXxi2m0l41SbjozjzrJAOK9CQx1L76zNloWrV9tiK7Us14OCJM4yZSXneXJIjtvkw09IBEVYl0JpaoF+ompaHtaY+rHq82EYU6oZlSlAjtAprCCCprxSLFURid5Hi'
        b'NrrY+iChYNwjhwiZhYxEghmSyNqghVbIjGFnUmDYh9W9tRXFX6RvRs8J9W+KUqOw1JfecRDZxxCazKTy2UNo9fLyPTcOYk0cztNIfJZ2exssNaNXAkRY4oqdhPAVwkYr'
        b'SZ6mpflx6xoBVT5W2ibw8aAl3UZmi6OlNZDg2pJuJuZLwAdOWj7eNJyFKN6Q9P8BmOXz7CGa3CM3yO0nKbZZI9pMfIw3BeJJbS7rpSwm01RRLVzjzxqHRWZSIaMwimfC'
        b'BcfSr/NP7BTKB11P5b88Xi4J19gRmCryN5P401A8BS5h88abCumDRKvC0//nZvWZgA1u+vlxV98xsAlPivJV/aKhzQ/+/O71Qv2qik6nYMc0tRPd252O/qHq6OzTa1/R'
        b'eu8/PvhNVkzkpq1f/fX8L95O+cD3v3//elv17+aa0zUMz7x5v/NjTbuB4NBZl743Vf7edP3OSNc/hk4N7q46URSrH9m88MaCxa//8bNJ8Y/23DKq/6+BS6Yf/7T1fHN8'
        b'qsaFwbHzmvda09Y22X7FJ/5ixq6F4J9rt/0k7e434x12XnMYbijq+rv1B5k/mdx7wmEgOP7o+9/48K3UL2efr+ub2OLVE1IzPOK/xa938oMn29DxdceOf2pGhzx5b01t'
        b't3Hgr46s8/jla6HmO37VbnDYPvtRj4vFbvdJU6PG3k1v6P25yn+T6Z6+dZ5/7fjYuuDWX38w6vTdd970b3i3Qr875OyX67r9eqMLrhlEu2v+bLrqNVFad1r5rwxbf5L8'
        b'1OJnlr+qu2Wk8oMq37RvmE+aDox5/HHkOwVuP/P64GbV478EXvMTp6TG+jRFFzgU2nxt6CftX31z4bf33/jCNtNvWfxyZsPe71vtmV3TMuP1zXdgvv8D/z1/d1d7cH42'
        b'a/8Dwy8aehil++7uPXPpl//jrKv6x3UXLRq+9+e62G9amOkHbg1Jiyr/okKlo+NHh2arvnBg55f8FZL2/iDF5/DXDh3/6iHzn2b22cec+VOCb+T/a+7ao6K4zvi89sF7'
        b'RTCgBCEU47IsCGiK76oIIiwk8ZUYcViWAUb2xewu8hAFjJBFAZ8xSoxigtagCChawWJ7b9TjqbVpTNOcOdbY9JxWTU9O09g/jEF67x1QTsw/7ek59HD2x+ydO3d37r0z'
        b'9/t2vt/va/p+7/rqZVVDKf5zNsa9km1pON52ee6991PiY5Izir034v9aMfXLi95K77dFNyx1nuqXjQXedS/ePhO5x/P1N8mr7x7f2ndg+OSGdfLsL/ov7d+XurrnyrzS'
        b'ObmpdzeDdTV9c1fOb5x5onHPazc3rZ4jHH6/sKcloKX3z61SZ7fXaLVoBj6Hj2s4TepHE1rK6lfkHf5TmzCleOA+vHGqzvX4iuO3pY+u3NkyJK5e9YX9+qp/Xf1+0pUz'
        b'c4Yfxixsfs7z+HLMwtb9nsedGY8jLqk/3da7cEj1u89yGo7M0PuS8HfgrUpFlzC5haQhC7AFtsFawuWCfVETnqXNgbok7XyTwnQbqJoylueGjj0dN4bptmQkYLajONpP'
        b'CvAJQFf69iDJ44+W4/OsUEZFVHHa8HAizQP2ibDzSaWN8FzcxI1lAWoq7GcsWgjaQDdhY+FnwUGucv8yDzwfBJrAjjRVkDbAF3YHlasofSCHf5OE+9w4mBicy4BtY6uO'
        b'VgTNqHXcdhzYTZk4NbiAfxgm8f6g/1Wb32h7TtBKaeFxJhE1ecydQKIjT4W6QLO2DH1HF1rhvM80aVFRJtinBoMO+B75wq+CXmmsKgtsM/1AmMUnFRx9No1cyvjGmI47'
        b'6CPInfX/BZTU3zxvdZgLeZ5EX3+KHwUZGGYmHYU1Q4bVjD+tZThWS6tZNaNmAtlgVXCwzkcXqdMEq0N8uYkhTFgm88JMmtrCpDB0KskfxLE4EjcSlxnC6LRYXMbw80Zy'
        b'CzGWOWSLWTNaEqae/LpuEWqbZXTx+KiYtNG6MUwco0cvA6On6rhOUqZm4kkJ+kNlHTjAWv1wNBJcq9PSYfTYFzfMPZTynwQ6s9I9fPJPA7+Tx39ijNuEpJXOIIHXuIsM'
        b'eBJg08T5xx9JiqXQg0JBN3IwWmErTmC2ai3wglYNFRjOPo8s9ibRejOadYXSFPXP+xGzmjNzPpqhW/qbAxNfPPReRolucUFwVHpSxFZVgYP2G1iza+3Z/MYHA/bf3wq5'
        b'yv3hy6FPOh2G9mU3n6v5JH3l7db8C29P4Stfqq5faWMTIpZ8nZp+q++Bx1rQYgK7Mi/8zc4eCr/Wfm12Sb+quMV44/msyNRzFxzh91vuJR+IHB4KvTcY7rwvWb/dOXFR'
        b'5zdxPdVHM4quL/44xdhU++G1q21Hqm5Vf3bx48XxpYZDpyZnDV+53VG1oehW+aFsxwGbfdbQ7P1R/kn1vwqLnPaPpMv+9OLrPVvz0t7qaeQeLSurXRIRDZNyonb9JaQ4'
        b'9arKd137ttJbdybFynfvBOY9cLZq5h3dXd766686dscN53zOP8rdOzjMzNr0xsBXjH4q0aJaAQeRtYysVWS0grpcQr3VUH6gl0H+Rhe8oMgs9cGOsKxcI+xB9XJzjYyv'
        b'gZoAL7KgXQItyvJSFwXeVsYCSwHAQXAR/8SDRiOYjUQ3+IuEFJIB9r6OxVNNGko9DR7gGC1yWQ66sf1bqZ8PtyeqqdAUegXWPjtWQ2jK8OTkFwywZboxPwevgTTlk8Ag'
        b'H+JSDKFSJ4B9eZvheWV5VFFcDg26BXiarDWx0aAdR9kboVc/lewOhE1sTj44prCwaxeBvfCXyWNo52h1fUdRyGsHrZOURk2ZsFmfycH6BVQw3MOCft0CwkVejlzqpqzl'
        b'8TlgR9ysFJrSwN2MOhqcGFnXV2/KSk5BhxL9LhX4wEEFRbNz4aERsbR8MMDiCpkmsh/216Av18Um+VUoROd6OFhWsAZux3nyWpEN/QoNBkBLntIjB2vQ7B4kOXCbTfEU'
        b'xSXRyO99t4ScVg7oWA8+ANsNRtiMefM2GvzCBOrIacXySw1YwS4bf6gJnTdHTakBPy/l0OedExQVvZ1gMBaNENiL88mhcUQ97qdnkHPfVUoqaEAj7HBlmorAuScVfDMZ'
        b'5KK++xOSTEoHGhx+sDcI9rmAF553zkyEZ8uQVRKAnLAYTgNPgsOkobziJYSKhAp2G3A/UGjSHWTg0VmgUbEV6opxUNz0MWJ0NGiDR2C/W493N9uDssCp6Zn4Ma0RS1jv'
        b'IIqLuZmgOTHHqFdTGUs1m9bAD5VO60oFb/rBbngWS3nvCgZd+GlmN2hSUvM2JCM//8wIF15Vvn4TjZzzg6CXTH6XzYz3GeFbiXGj7KLJnlgjBxpKVxJCUwg8XYM6vAl6'
        b'0UBshd5shvKZxqCrYecbCs1xEBwB7xiWG0PBvniTMYGm/ENZX3gC9igKCqfgkfVZaGiyEtCcQ1eQXq1LpCamsMgn3Y+mJJlSXckqzKZqssVhziceFrgTy9WiC42IJeTj'
        b'5woG5KaxRjqLQh7+mQ2jyYymj//d/X+0RkwaB7PkaQrhcgTaQN8RJiZWUNONbClaZ/5EH21ka5irxTpqzDBOGKyl7ex/ziQb/eNmKJwqYjPEyaxVsEsutKzJKrfHaRVk'
        b'ziq63DJXKFoQOpyCXWZdbklWFVS6BZfMFTgcVpkV7W5ZVYTsK/RPMtuLBVkl2p0et8xaSiSZdUiFsrpItLoF9MZmdspsleiUVWaXRRRltkSoQFVQ876iS7S73Ga7RZDV'
        b'Tk+BVbTI/ksVUqPJXIoO9ndKgtstFlXyFTarrM12WErTRfQlfQpSXhLsWIxKDhBdDt4t2gTUkM0pc+kvp6XLAU6z5BJ4tAvzvOUJNkfh7J8qOT34QrFYdMsas8UiON0u'
        b'OYCcGO92IHPRXiyzr5myZT9XiVjk5gVJckhygMduKTGLdqGQFyossg/PuwTUVTwvB9odvKOgyOOykHxMss/oG3Q6HjtWo3pqjSn9PV3aiO21TRgqMdRheBPDFkJvw1CF'
        b'oQRDMYZaDDZClcXgwLABA+YVSlYMIgYPhmoMZgyYyyo5MWzGsA1DAwY3BswmluwYajBUYCjHUIqhngjbYSggH4RZdlvxViOGsifsQTyRfEYtq7UPn7WsSI3vtEVovgiW'
        b'kgRZx/Mj2yPG+XeTR95HOc2WUixIhqmteJ9QmKPXEg6grOF5s9XK88rEJSxBHzxj1UoyVenvuMQ7agj/ICWzrJ2HRt9jFRbgnHCuZRRm9nJqLfPfX0IhqxhCof43Eho4'
        b'oQ=='
    ))))
