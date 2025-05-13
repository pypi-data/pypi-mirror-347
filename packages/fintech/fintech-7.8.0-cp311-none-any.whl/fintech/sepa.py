
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
        b'eJzMvQlAlMf5BzzvXtywsMt9LYrCwi63iogHgsqNIiiihl3YRVYRcBe8gsYLWQR1QdQVNa433niGxKjJTNomaZqydhO3pElNm/5ztP+WNKZN037NNzPvLnKZmPzTfh8s'
        b'w+zMvDPPO+88M7/nmeeZ9/dgyA/X9v+LnTg4CFSgFKwApYyK2QFKOWquiQfG+FFxzjAAXGDs37WuKi4HqPlncPzCYKm1QOe6lIPTBSre8PLbGJzqoB5RCwNU/IXAaYdU'
        b'8PVK54Vz5qdJVteqGqrVktpKSX2VWjJ/Q31VbY1krqamXl1RJalTVqxSrlDHODsXVWl09rIqdaWmRq2TVDbUVNRramt0EmWNSlJRrdTpcGp9rWRdrXaVZJ2mvkpCmohx'
        b'rogYcmOR+M+F9IYQU9UMmplmTjO3mdfMbxY0OzQ7Njs1Oze7NLs2uzW7N3s0C5s9m72aRc3iZu9mn2bfZr9m/+aA5sDmoObg5pDm0GZJc1jzuObxzeHNE5onNkccBHpf'
        b'fZDeXx+mD9eH6r30AXpHvYNeonfT8/Qeeme9SO+qd9J76wP1QM/VC/Uh+gn6iXqxnq931wfr/fQ+ehf9OL1Az9Ez+vH6CL1nZSR+To6bIjmgJXx432+SOgEOaIwcnopT'
        b'pMNTGLA5crN0IRj/xLx1YD13CVjHOFVJOfkVQ0dBAv4Tkc4S2IbOQiB1z692xN8c5nOCxnFJTFG9u7AENEzAUfhSTCVqRS0FufASPL0A6dHuAinanVU8Xy4AEXN46N4S'
        b'uE3KbQjEZeeifQ05WbIsOWpxQl2oLY8P3NEubj687t8gxvnimatINryWyAc8HgOPlcKLDaGkkcvwqFs0asGXoKOheVlotzSLB7zQPi58KR+elnJo9X7o3KychMQs1I22'
        b'od05aE9BFh94hHGnad0aAnD+xIApJBtemJuVx2a6o8vc+Gmow1YBbIYX1DqSSRpqY8D4Jc5ZHNiDmuc0jMP5jug42ueCrnmgmzrYgl6oQzfWwFYPNzDVGQSN5zmIAqVM'
        b'gx8umOzARa252bgKdJYLuOguAw+ju6gLZ0txNmrJRlty4KXILHQMviRHu3JQG2wpIDTB3bH5cqkAzJvj0BhCqvPF5XOj4Sl0HdOknp9bwAf8RgadWotacS65LdRZgDqj'
        b's+WyPHkMg+8BnXb15jrj8lttBdYWoBPRmbIo1JJLbgreKXdBBg66PKuoghny5BPtT74fB/sTmvHTxwOWhweqAA9oRzyIAR7OLng4u+Gh64GHsice7iI8lL3xIPbFQ9kf'
        b'D/5AzAzBeJCHYhYIwwN7PGYLMuAj9JF6qT5KH62X6eX6GH2sPk4fr0/QJ+qTKhPpgMfTR4vLiAHPoQOeGTXgOaMGNbOZYxvwY+YNDvgdIwd80BgDfj474GWBAuAKgHBL'
        b'8UbZ5pxIQBPTQziAzJ+KlarcmHHpbKLSwwkIAYirW6uWnQktYxMrFXyA/0tMS7Wy19ZPAudAtTNOLmn04z3yApIL7h9G/JVzKz51jY6pdsIZ7844xPQ44PIR1Qm/Sahw'
        b'6QI0uS3lC49ODyZy/nNfMP/2i869CPpBgwxn1KObTpj1WmMXREaiXbGZci/MVLvguaLI7Dy0VxaTJc/OY0CNh9P0NP+GdDJSelzRCV29du2aBh16AfWgG+gauoWuopvo'
        b'uoejq7O7k5sL3Av1sC0hLilhcvykRPgC7MlGRh6Ad5c6oUuKVQ3ZpJ5Ts9DWnNzs/Cx0Zm5eDtqLub4N7cJs04J2Y3oiZVExUnk0vAK74cVCXMc1dBC1o/3IgA6gfahz'
        b'MQC+cW5eqGfasAFIepUM9y8ayQDkkJkaD0EGDzt+JZcOEbzutPBGDBGu0xgPHadwRw0DzmaubYiMmTc4RFaMHCK8MYYIL19LnrGmwezM1y3AsWtzBg6/mXo0rGkNw53c'
        b'90ZvW/tW5aTxbWWtC9VuiDO3+nc/37J+0rbm8n+90M+ZCFNW+qcc8o2raAhc6IYSTE4XPjyjumoo18ZxVwjAsTqvhldWSfmPKHvvh03wEGoFPriH96I2LuBNZeBVJ9jx'
        b'yB9nr1+LLkZz4I0Y/AxaZAwQwD0cObwKdzwiXYkuwZvwWjRqi5BHZso5OLeLI9+Q+4hMUqizdFw0PLJJjnbnxvOBoJRBl9BpdOORN8m86oAfZmtmlBpewt25iZmLmiqk'
        b'vH5OpFSLBzp4HOhI70i2bNnytXdqpbZ2o7pGUsku5jE6dZ1yRj+3QaPaSAIOKb0cB19tAQNzOUDsc3BKxxRjUvv0zun6DKvIm/16LKUr5VDqkVSzKNIiinwgirkvijGL'
        b'4iyiOFLI92BKR4pR0y02i2Is5JPwQJR8X5RsFqVYRCl9rilfkCemdcCBVNDvVKNcrdZhUKHu5ym1K3T9DmVl2oaasrJ+l7Kyimq1sqahDqc8vhnyhBUKCb4frSdJ9MIB'
        b'JT6D5K4hxH9FyJ/DYZjgAfBtwUN3X72mZVXbqi0uAxw+I7a6eOmntExtm/qQ57ElZ2vejrwteVZHD6ujSO/y1QCe1oXDU7cUsL9fkHF2wEkGLrqncOdWcMYamJsJx3Bt'
        b'HMOjPCOo5A3yDP8/zjOjplXnMXjGK7+Bjq3T0AhP63L5OHqOswbAs9A0lwUA8EhlDk5npPPhUYCa4S54ly6o6Bi6Da+i63j1Y/hoG3wR4HF9Eh1k6zsHX8TrLcmbAw+i'
        b'rZhlfMc1kMYz+Oi8C0YZjCeedloAvF0+i14hx/PRuWiSsQAdmAXQYdgKD1MKNKglMTpGAJil8Ao6C9BZLbpJL1mKDkSjfYTRN+Jpsx3kwR3wWgMZHvB8ngvaJwDQlAFk'
        b'QAb3Pyd1onWhPZHQNI0DpOsBasIfeBx20Yzl8PlNz3IA3DoN9wX+oO1wB13o4YvoSgm8jevqxQyPDuIPMsIT9KJGPEvvRTiPkwrQC/gDLy+iN7lSAk3wNhegk0EA4V47'
        b'WiykF8DeSYUIpweNA+gO/sBT8HyDD6FrJ9yPv972APCkG0Am/ElGB+i9FMFzM9BJTNpOeABjZhfHyQ2ELeB2dCdqIResyAARIGJpSAPhDXgDbVmP9jkARgHiQFxqBq18'
        b'Tgm8hTv7IGZAvJTcwE+jDL1QSe8OXUE9sDtBjq7r0PW1DOCgbiZ8SQWdR0ctBHTshJBhjYf0CtAIlmOE0Mi0cNaCK4JGpp3T5kTECsroLLdz+zkxcf1MBcvIRATCbEy5'
        b'+Gvn1GqNrr6idnXdjI2h6pqKWpW6jExOManVtRXKat2MmMcFSsjVIews1ec3lf0Y13R7dq/sDu0ONXqSsDtUSwjUPN+CZ/+LOPabGPfDbyYcPb7vpvHcvknGsKb4JmnT'
        b'1KYJTZOa5E3Tm8Y3JTatcl8hn78ZLw49rvrFaMPyi0dlc37aazlTF1vBO1+Z0Z3/4acqeUVkB+czxWvntzt0Nzvhz/JfCs4F7OTnWh+ZXnq9KWxRiqD78oGrB5wOyie1'
        b'Tcr95Naj1+uvyRU//WziB/mLXKd8Lle8eubW9qm745vuNZ10+9e+d/i/WP5JWNqyrwSJdbfwfWXEMZpn8cJCRjQne3N0zDqxFO3CYEIAL3IS09CORxQH3/FGOzCiRPqs'
        b'3Hw+QPvmusCrHHTUAd2jK0civI0HbasMtgRgKI5xvuAZznh0ecojCbn4WNQ0ikrQLoyhUQu8mM2fDk8BURIXdcD2MrpqwbMO6PZzCI/yYYtaTqXUYcTyMlagc6APlyw6'
        b'7APudxnyUDcO/ULXnH+xT3NgPl5zvPHc7OZv9fUzOFqDw7rFPUWviB9HgkIH+BzfsAGAA/28AQHw9Dro0OHQ7tTppE+zevgPAK6b3Cr2PjivY54xvT23M9fAWH0CjEqD'
        b'xqCx+vkfc+pyMoV3c81+MoufzJA2wAW+gWwurixkwrHlXcsPlR0pI0RIadDuZOAZKkiVWR1ZRpUp3SyOtIgjDQyuWBj4QDjhvnCCqbJbaRbGWYRxmAghpWhwZOKPKQ0H'
        b'Zr+pFhwKUyzCFFxKJCaLafvUzql9rkF0rLJM4tDP6Pqda2rLdFh4rlLrtIRntb5P6GN2JbQtheFk7hvat1mk2FpgXxIL8JIYSFa+7wh+1HXxoJMcXHKfxn2KZZFASf6w'
        b'ZfE/DyVHiddjQUknVtoILvYC4WAg3QEoGjflz2RliFtLM4EB9GidFYooaf0EMJemGr2FQAKsk0CdojopYB1b9LdhLkAM6qpdhQrZL6f4AHYReAldWpYYx8PrFV4z94Fy'
        b'1BOpkbm+zdXV49zTP71JZq2tLcf3vbhvjf94Llop2blF/NPquOVv7S0+ID3Mz/CNPx3nkFifEKN4RXCA+Xxl8pXWq/vOZQZ1H/A83J8/sShw1/GJZ3tOxd1IyBpniT8T'
        b'd6pnXGsRs0b+uodskusiS9Vl1c8rOeZXXY/4g/0TA1rX7JZyWGTajW5rouXoTMZjYIpaUh8RcQy1FUujY7JkUdIYLMfghRsvHU5+Et4zHrBXyn/ytMAHLBK1TQqeFVXq'
        b'ilVlFVq1SlNfqy3DMHR0Ep0gWmwTRD0HCEV6nSGxZX3bemPYrkZ9o1Fn1JkSD60/sr57XNcm4yarb5ChwerlfVDaIW2P7ozWp1s9fAgnBxt1xzZ3be5eYQ6dbAmdTJPY'
        b'wkKRIc0w2zC708E43lhuXGMsPxJhFoYRLg3vE4WbFphFERZRRHfSfVFsn2vsMG7lVmhU/Q4VtQ019doN34NZiXw4xt0uHc6yOsyyAYQpvyP4sVhWS9RyYy/1G22sSpUO'
        b'jyU+Zgw2/fGVAqMkPv4YbJrBsqnLRsKmIDLXWbEsYLmfjSM3SglHgpKrmxXVHzspQBELDQ9tcE8E6CWkByAexKOjHrTw1jiqGCgJn6WQBeQKAcVYtXPGJ/LQ1blEBZcA'
        b'91bQkrMduKSLSt4QKHLHq5RsSaa6KpGThQxEZZM4FTXTki9nuQK8NgtXlSlcN+UtYEuWb0C7EwXoOu7cJJDkupYl6iUe2pnIpCDcHZPApKXwBVrBgxBvoimtqpmtWPax'
        b'ezSgGA/t8YK9iXyM8MBkMBmeSqJFfzE+GCQDkOleqAj65dwZgFbrCO+hlxO5jfiyKWAKbEL7aFlFqATMwmIqb4Oi8W5kPEtXxlRoTHRA52YCXE/ypKm0pKciHGQCMH9P'
        b'jmLci/Pr2FqhSc7A6wDeSgNgKpiK9DW07NTaSDAfX5y9QjFbX53DltXAppXwOi8DdQOQAlIWo05adnGNDGBQN+uDpYpxIdNnsjdWtQbe0vHQFlxgNpitQWdYnLtjKTqr'
        b'44BnAUgH6SlraLVuaItOJ8CI/BQmHGSgOwns/eLH+ryOgadx4TlgTjHcQyvWwKtyHR/24Ol1LpgLt1fSwrXz5+u4yATPAjAPzIOH0fMb3SN04ToHv4W4H/FvIZ2tl8Fm'
        b'jIaug0zYCUAWyELnkZGdxs9uQAfQdd40uBeAbJCNAflxCv7hadScga5z4B7M2jkgZzlO98DpM/ID0XVBeCoAufh3Cu2I7DSqzpp1I0xRfYSzmu2I2twUdJ3Jxvl5IA8j'
        b'dCMt+o86spYAx7eDFbKbHhpA21JszELX+bAZngQgH+Sji+goLewvj8BtAKCSKMoNyzcDKi/BtnrYha5z8f0cBaAAFKB7kH0eCc7RoIi0IcLPY8ksdp1Kg02p6LoDehke'
        b'xkMAzMfCHTt+fs/3w9IFUOiqFalTpk1lKUEmHbrnAtB1eBuABWAB3LKQFp4ZRtVwdf+oVbhuVmawhbF0dAhecOGh7bjVQlCIrk+nhQOfdSfKP+FfJiuqMxWFtgHfhY45'
        b'uHAmwssA8/zCgEyayofn8l0E8E48lpCwjHRlHK1A5RiI2QrUfRigaMz1C2Qr8Eua4sJEwiYAikExlhFP0aL940IAfhaOb6Qqlr3sZWsLdjvNd+E7wGsALAKLQuBJlqz8'
        b'cXiYgeQlHorZzqpytugSdDTEhQu34rl/MVi8Cm2hRd8M98USJyj5QqIIepixgOUC1ApvonMuDqthM84CJXXFtGxFfQxYhsd9UJxi9sKkCNvdnnouF7YCz/G4BbAEHimk'
        b'Rb2jkkAVLvpCnqIwfFkliy4OBiTgaRBIPIDC68vVRWyiKiYO4Kkh7vo6RfniOC2QcigJ89FtHWzl8QkjloLSINjEPohtaagbtnLgbdwVS8FS2JFU/dU333wToKLT4Xrv'
        b'OQpX/0A/tuqreBapxj12Uarw+nxTLNC898eXeLoFeO24lPaoqSOrAM4X/mzFB6tcurt7T/Zu6419eLfid1MGMk688FxuW4tD+KuGv31y/KeB8c+k1m11Kbv/abo8QFT2'
        b'182/+ONbV3719qPie+3jZv5uWt7ElW/UxA4cdb88gd+QdZe7bXPhG1fi3vn0yjud7389Y3pkydalH3+jO3Z06Ta3sz/VS6LajudY3eR/SltmbZ2hnOkFGVfn5jhZ0Kvd'
        b'dW/1Zv1+T+A6jE9+nx+wLqru9Ns3rq5om77qT1NPNfm/5XK9RBhTntXb5v1h1Ls7/mgV1mxrmvpR01Krz58Vi3ubN32Y82/GvWle8uU129dsW3jkzgXBszu6fxYf9d6H'
        b'fz/8vE/Ks1/rOL71R28XZjz/1xsXDJdTEnZ3/vzu8gfPffmrd+5NXB/i905v6tayazG3Ozzf/frlY+tePPrxkrv/W6pc9sFl4fMp3zT9M6PrTXNPzc5sn4Xt20qaQhra'
        b'o4Lemr72C+bOohXHfu+M5UGCulY8B3uwUJdPtgn2yhjgEgtvwQscdBndzqOQbTna54ZniGvRQ3SJGriblfpuwJvVOWh3NNqdJ8+WZfGBF+rlwoPwCGpGV+AeKvW5J8Fb'
        b'vkStiNpysoheUZDM8YfnUdsjIm+XJUXo4KXMfHkk2ehBe7nAExm4DjGYqiZ0Sur4FIIhC4bI8JFIJI/RUL+7DQg1VJQR6WXjiO8UA3ZzWAyYyR2KAeN3bdKzmO+hyMeg'
        b'NTIGbeeUgzM7ZppF4RZROEF5QVbfQEP9MEiIQZK/O8F9Cwa4JOYXaLTFJONNtlhkdLctFpfYY4slT+stZGNpGa+Us7HsvNe1bGzhor6SUja6rKxPWUGjD2krfBKjrdAY'
        b'bYXGaCs0RluhMdoKjdFWSGwAkK+0KZrBNkWjbFO0EBaHxbgxBzbuH2QcjIeFmwrt8Sh5d7k9nji5R2uPp858hbHHM5h5zOuD33KZAqZv/mBlRcxihjRv+7qcUTCEBPrV'
        b'kZBQOODExgOCjeX2+PiJJq09Lovt4bBxwCakpL4ybkgCCfRZA67A20c/Z4Dj6hb8fmhkt6h7YXd598KLfubQBEtowgAQeMbToH0eBvD1Vl8/Y3x7A77YO/6hX7Ap8EFY'
        b'wv2whJ4kc1iyJSy5N8EcNt3sN93IN/JJ74SY/LuTToWa/eJIijUozDT7ULbBySoKMW6wiKTdC3u8Li6+L0rqEyVZAyXGSQNcIJ701R9EQVRyeBzQwWdoGODiOEbtD0W+'
        b'hiQdnU6npEkyAsBrAc4ZkdzXIhgc2tXeXDyynywsUB33EFlhMsGvI1hCRQrWASIoEG03l2E8iSTw5OBHler3O0WDC+5Tud8pKpDdSTBEVOD+x0WFp5LoHVhRocPfjWDy'
        b'SKBaXV3BLbWJCq/OdabYSrhpZS6oqQSsTrYXg8ItRFAnUjo0TStHd1C75uOu+RwdEdq6t3WQ3aXj+zY8ViC+let6tO3oWz/323qiLc5MpfbXOqHYNYloHo/vz/K67BIJ'
        b'DbBNVsh/7abrrOvGlX59b5XLY95gBfJPQdLvPJ99d7uUobP7RIyS9GRq56BtgwL5sUQpb8w51r7pw86vAezg0dVrGyrqG7C4WaZVV6q16poK9cZvyaPz7hLAzruzeUDs'
        b'RzZ32lM7U/UZVg8vPAkntWxo2zBkErYK8QRkKDQUdjoak0wck6eJcyTZLBz/FLK0oJ+nwy0/PVukErb4Fuq3DWORNB7DeBFOeHLwo0nRyeAppGjeCCn6P88ao6Ro7his'
        b'IbDtAfXOS3bR4gLoItns2AYPFaBtrBoMC6W5q/qwnKLw2j8fy9eag++/x9ERZWN6eCTLBGseM0HbrIY2q2Xa7dNxMdxdV3b+3PvzxPj6hIYTLWfi1Ne3qA8VGrf7b4ny'
        b'6yvmUQ242NGjwL1fyqEa8HEh8EA0ujNtCJ5ZOf1RMCAbHrDZx66Cuouu2tRQRAf1TKWUO3LokBsdZAa/EVqXx6zwxBzKCHk2Rpg/ghFEvgRvmJLY/VC6JnSnd6f38M5l'
        b'Xczq5ZzP785neUMk7xPJu1VmUaJFlNjnmjh88Fd8r8E/mwz+J9LbMmzoF/y3h/7T6Hr5eua/rOsdtQU69spQREf5Kr4HET7jApIVuYXR8azMw8nmEUFIYZircC2dp2YT'
        b'H4ynKqCqP7spqn03+wDNhJp2vk5DRtyXbVR7u4/ob8/ti29lBAfiE+IuVu74fKV/iv8qvzf9WotS/H1fmdP+aoLkGbePT8ept3867vn8/xH/T1SMYGdMpaT1Hzp+1JvG'
        b'n/32Dccb7ROa/N95Pkry5/I/rfmLyrXyYTUDPl4lNructKls4TZ43hNeyM2TcQAPtrvmMPAa3JbL4v8uD9iOpQe0J7YAy5/X89Du/Cx4kQd8C3mTpfDW91DbutWo19eX'
        b'qRrUZSplvXrj8K+UU1bbOGUZT+AWbQ2U9QXKuosuLjEHTrEETjE4Yo4xru8TReBPd8aVgvMFZtl0i2z6K8x9WVqfLM0qkXanHXczZFl9Jab4jk2GTVY/jLICjRqjpps5'
        b'VH2k2uwbZeANuOHKB9wxL+pzhqlkeYSOfqdqtVKFSdrwfbZQMglXDb+hvWCYRnYp7zvtCn5U4wJWI2u3FyU/Avuo3UEYisfaS2KW4ugFdAvFQe9YKaBsxR3DsoDnNAaj'
        b'4BTeKNbhbubZ2GrMvEG2qhzJVk5jsBWfBVySPKqkAHFTj2244+HNMlDFVNYMK27i/s3cWSKguZQ0j6NrxTld775y+M3JeD1ZPbie3HSd5Ori1zL/Z9Y3SlUlcJfhL6o8'
        b'5bKf8ooQT9TCXFt5aOWhaVNXGs9v+VfMnoCdskpjtZtucsk6zzK38aL0iMXOv0ow3bnw4drFW1dLP8ywgqKfLEHWN7audCnpjJyy/S/y6k9VP7vBL+a986j0QMABheBt'
        b'V7B11ri1XblYBic7q7AXGsR099QBcOAJtAudYIonwbuPqBLwaPyUnCxZXkiWzTwS7XSg+7WpUehCDjoF96IWGb54dwEDHFEbB+7wLqWMm4LaQnC6PjZoKl7neHkMvId2'
        b'oIN0DfQthlggz4MX8WOCO+ToLjOvSCN1eVphe+SQJ3a2dtl7kKNdV6iHMPSwb6zobePnOh4QBR6UdcjaYzpj9OlWkc/B5I7k9pTOFH3GQw/vAcBzi33fN9hYaSo3+0ot'
        b'vtJ2noExxFuDJmC+zSOylU9nsnFNx3TDdGtgqElqIowuOyUzB8YYMv7gG/BQGGxwM6pMWWZhjEUYw36tOFbVVXVo5ZGV3VO7p/YUnZt5caY5JMUsnGYRTvvcie/n/gjg'
        b'QJ+JpUVxkL5gyFTgRKYCzP/EJK5fUNFQX1v55BWW7R4nOiMohmxdawvJnDCsTw6RklvZKYF0Sy2eEyYQrn/q4EcVxrqc4kCP+4zhwtjgBglddvmDwhgxFQWV/P8i6hy1'
        b'7PqMMT+EsvNDYsSboJPp4QGhQlMZtISdH5q4Eow11wlAnaJRNF3CJoY96wSEJQ84+GlVC3yi2cQ1pVhyW39EgC/PXVu2nE18I1IEwusz8RKtSJUvL2YTV60MBskKjgDM'
        b'VzSOj7CpUEPnTwJVkb92wK0lPHjOhU3sVguA63wuF0gUuXenZLGJW8Ijwfw6XFKhmF2YbdOI/jVwJmgU/lkA4hTaj6fYGoqsTwXrXW9wcUPa8aCcTUQFKaBegusUKhLE'
        b'k5exiV2NfiBufgYf19loyFnBJr7oKAMls3aSyzk/8/BgE1cvF+LZ8iMHsrvsnmJL9Bs/C2xpXARwoteFMimbuCIUA5bwFHJHrrcVq9hE+UIs9fp18nGdsjlJjWzinOBA'
        b'kJQc44BJSn1TG8ImLl42BVRXJ3HwvXv55y1kE7nyBcCkqiOtRy1YH8Em/lulBq8nBQpwQ5Wvla5hEz1kleAtVyfSdRM3xbmyiZtKfIFs/lqSGHQ5ZwGb+PZsdxAUPp7B'
        b'XSfbUpPAJn6Q/ix4VPI3DiZp0TsFMlsnZ+AVREgmJEVh63pbz+/zGwcyeKfw+FdwPCKfBRrwbj2jW4a/r/9KtX/htBoU53p6ws+fi1jwdU7/21Pn1LZHC/9XaErf6S7Y'
        b'BBpiX6p8s+P0PNm5yLTfvxkZlS78MuQfme0Dzf/g8Ws++9MMJnlgxuV1f7x4+OVXb9WJVhyM8Hv3oWziUc4njPfKbW8D05+NqKiu9tCWFf8+8OzLvzPyWqva6nbt/3lM'
        b'RU5FVmlj5Ocz9s9bmH3Vp3bG4bp3z1bdt258Lyj6E7f8SO/WtnsrXq/9yPVjYXZA1ob/PVf1z39NzZeeXPan0KpXSz70zo5acyvrtMvSn09fNScv7vP3Vv35+RkN5648'
        b'897D4+eCtFs//EtHmLKyZFk+vHfZ+TeK7MLF8w97vMPZ3PQPx83Bv9j8xbR0Rc28Q7fN5326T/5aHnPy13+Zt9/1fPd9zooFLwf/78+Q44y+DYf+/uWSP66JQzu7gl97'
        b'9/m/f9iYfufz+Pe8J1V88c8r7z7Y9dlyry/O/k/hdOZvRc9Ftx771x8KTiy4crzx34L9v94XtrxLyn1EbP8liWgn3BZpw5bDcCU6A89RG9kQtAfezpFFZsLDq9DuHLz8'
        b'wQucDegwOkxX1QYswHVG48ujGJCJ9vEaGNSC9qPDUq8fuMw9zUroZV8J7T9DFkRPMt2XK2tWlVXVVmvIIrJxdBJdGn9t00rX8YHY15BoqCcmPfqMATwHiQ2b+jzC8cfq'
        b'G24qsvhG9QmjiIrW28htd6GGQgalMaxdbVS2a0xpZu8JZuGEbs/uBee8e7zOBfRyzJF4lSO2QkJPwwKjZ3uxcUH7ElO8WRxuFoaTZLFB207MnjxFBmW7D64qwKhl7Rbw'
        b'FYXtDsZ4E+fQFNOC7nHHF5sDZT2ePeVXfc0BU83CqcOu0s+2enoZVMYi04JDS8w+E7s9zT5R3Uqzd6zZM5bNLDcmtK8webYvN3uOwylepOkIHPHwNMzetU6/zuofbBTj'
        b'lTvNpO2efXyd2T/W4h9rEBgEDx9nmP2jLP5RBgHREXsbeIYiY7xRaRZKLEKJVehj9Df6m+IPBR0Jwt2Av49OEo+8hk1IIDc9ziIcNyqBdLYvrSThUPCRYLNwor3SJ3+3'
        b'V7EGd6RFGEaf19i0jrwm3ljOXvMthI2q9VuITwygqCZ5VFH87LxEdhRmSrvvNaHPa4JV7G10MjqZwg65HnHFQ8TADHCBSDyy2ENX8d6CXQXGNLNriMU1pM81hKTk7cpr'
        b'KWgr0Bc8HBelzzOGm11DraLAYVjKsZ+3Qa3Ufjt8ery9oxjKTlqiIB2DgS6T0huBTUuxhP+dWor/gL6CildD0Ynd9e4Lssawqjo1cc0DpRgaOQGVIzXe5lRyVZwdTqXE'
        b'AY+n4u4Aw53qSvk0nTcqXUDT+aPSHWi6YFS6o5qHBTtuJUflsMNxOMwqddKD9UypM3Xec+p3SFOptGqdLr9CMORuHO1Yaw+wa1/sznUYEBKfIQ4VGqkfUaUjhYWYxhbn'
        b'EbDQgcJCwShY6DAK+gk2O9hg4Zh5309Pz8+nZh8ar8yFG8fjSBgIwyvJdtazw2llCaM7iGPvvPnLhj3x7jDOdc7qxVlH/7xMH10HDjinnICfBL3iMOvioWsfdfRmnrrh'
        b'fKD80wnffPxNxL2Hzp5Jbzls5V0yGzxNDw96dv7lVM2MPcaeTx8G7jlT8remW3/Wf6PliW7++frRa/fv/nxA88GkZ12f/XL8v15eolv72fUJB7q6ln3hG9vzzpz7z3zy'
        b'pwvQ/8v9Vn00/2RXVP22uDtMNX+Ce0631PkR4ZZK12fIyscuewK4hax80k2sNLmlZO4wC9v0qfBqCGqh101MmBIdgy6hF4YYAK9xpMspvJi/nHVPo5XOgNfQbQ5s0cGt'
        b'VGSEL6Jdc6Jj4sfJWbXpKU7c9Gl0C1epRLtgK5ZD9+bI4V54EO6Eex2Aiw8HNcNj82jd1fkTcImWJQV4OUa7o6XwPA94OHHr/WSsU8rh0lLYWgCNcrRHBs/xgMCR48/F'
        b'DRP/O7QdN90FW2OxKBuTRd3lzqItZKv5NBdtRS+hVpb8cwq4D5eKkWbnJUfJGeCCWjnoheVoy/9Zrt2yZahc61BWVqNeV1a20cPGHDG2BLp0/xSwS/d6BxAYbHCwivzx'
        b'1OIZbRUHHszvyDdNNoujLOKoPnEUngsHAMcz3lhP/1kDQ44ldyWbSkzP9Hj1FPWU9hb2hc8yB6ZZAtMMGfbLk86mnEg5nnoq1SyOs4jj+sRxVlEoaSDeXuJxzvu+QcbF'
        b'pgqzbxRGCQ98E+77JvQk9jqYfWdZfGcZeFZJhIHX6WYNDsP/nK1hUvzP3Ro6Af9zJXvbLkPmaZd+bkW1ThtDbp9Xoanf0O9YV0ss51XqfoGuXqtW1/e7NtQ83i95snaM'
        b'dKmC/gzRkK3CwajuJPbbui7ACsSsTNzgwDCzGDJX/9/CH2uip5L9MadJ4KZ7Gne4qMzYJx4vOvE0gpWDWXRuZfLPMf2OZTYbTynTz9Opqyt15DIJ677gmFqtXF2uUs7Y'
        b'KLT3jD3FjbGtiFtAd8bFvC2APqvv2T5uk19GHqaU0RKz4CFtaxvIAxnVrDsu8YWtWfHFgO/f7Aq2Wacy++h56qY9hjRddPGZH3zHDmXscH3qhoVDujrpYupYDQ+uMesB'
        b'68HI7sPh5fX/Q33IWLtw3HzNnYHXuLqJOOnZzouH30wiRuAfxOw7PmwbYZt/ciKofY/3kz/8VcpQE55adB4dxRM0np1D4W77BA3vTZVyhrA2mf8G1fka3ZDt043e9m4d'
        b'lkwnTDL/E96ucgR+QYZ6Y8aRbLNvhMU3ok8YMWQK4tPnNda8QncShjjvER3aExr0Ig+TTDZ0NlE6/jfAIB21nU5R4Lx7MhdjD/KDJ1RHPMspV6vLyvqdy8rYAw9w3LWs'
        b'bE2DsprNodMinmm1tXVqbf0GOv1qyS6ItoYEtfab7XcjXo1Kna5CXV1dViblYQZjE4Y6OT7ewZ81OO8+Q7rKjvH+TvJft3WO/XfAGcxiMhhrwuQBrodb0AD47mAc8A01'
        b'VPWFTsUfs0+KxSdFPw8vdobkvqBE/DGLkiyiJH2GFZda3yeZhj9m31SLb6o+0+odbCjpC5mCP2bvZIt3sn7uQzfvAQ7XLZK44IwMPucCd5+2kifm09FDfdCC+fCGLjdL'
        b'mi2PEVTmA+eVGJrMQNeGMYyL7f8X2/Cw3O/5GKCrGALIO7mdHp1C/OfW6aHhVHJwzPZ7kXMG89iFQYBMAf1EAucxELa7zgsxDObtcBoBtnnkpA0C3FWCiw5ncLsXBjc5'
        b'KajnqxxxntOoPAea54zzXEblOdI8V5znNirPiea54zyPUXnONE+I8zxH5bnQPC+cJxqV50rzxDjPe1SeG+4DZzwP+uxwLHVn+1CFxY6LvsMFEtpTrlj48RsljnjQ2v13'
        b'ALWHKgDXj6e1C4P7VqVC23PxuBg4vGVVBK6TuP1wVUGjet2T1hmMKQ4ZRbEXzQvFeZJReSJ7a50OnY6V3E7exbDh9KgisdDDsR2bQJ67u96j0kk1fhQFYtpKOG5lwqhW'
        b'vFVcvFxVSqVY+Kqg8ODrCOehGiVbKnsQyrAcsuGvwcJwP49MIGPNF/kVDuDxjzuwrRFHcLDfcfghKXgRc8LLGBffCDN4+gPpVKAX4OHsThc3hzGkOkenMeQ0nOI4agFz'
        b'2OxoW9zGzBsq1X34D9xDw26W/GTVaOo1ymrNRnIeTJVaorR1jQZDUWVNBTlQZuQlKXVKrXK1hHRTimSOBl+lpZdmzU7Ll9RqJUpJgry+oa5ajSuhGZW12tWS2spRFZEf'
        b'NXt9JLlYJpmdlS4lVUSmpacXFOcXleUX582eU4gz0vJzytILMuZIY8aspgg3U62sr8dVrdNUV0vK1ZKK2pq1eNJXq8g5N4SMilotnqTramtUmpoVY9ZC70DZUF+7Wlmv'
        b'qVBWV2+IkaTVsMkanYRadeD68P1I1uI+U2HkN5ocW/eQ8ZNC6SIx+6k99u6tqq1W4eH1pIttmJa93vYF99HCAnli/OTJkrTc+ZlpkgTpiFrHvCe2JUlkbR05AEhZPUYH'
        b'2hvFt2NrEcfGpvhp6rEjU7Yu+7cfXh8LN9na2PgPqGvYQjWofRmC7FzzG4ij5gLU5E22gmUx5DCbnMVIn0PP24EXVobCEzz4MnxxDt3bmOu8FwQxwC9uSuG6P6iyQMNU'
        b'nAhfRpdD6K7wfKQnWoBY1IJjBQvRHVwdrao4k9hq5+Vl5TEA7kInnNAtN9hDq9SWOdBjU+LWXnZYrpkAGuQ4UbI4mdh9R+cQn+DcBbiiu5mPVQCoQwrPgYVpDugguo2u'
        b'0Wp25FHDFxA394pPSWkduxWTt9m2mV/pPfFPLnzQEA3IERmxi4dVridn7yxE+tkOsYWZaFeuAMxDpwXo6uTZ1NiyGvYugLvgi7o15AiCvYT+59ERzesfJvB0fngtcn1z'
        b'4u4OuquzU/PGX9OzjtS/LjR90iH6yPnO7AecJTtcnQxpn1bFvv/JnU8+e6M1dsmbTd4LhQZH4Z/2flTgNe6582XCLdLPZjB+n/z72KKTdy/dS+Uad8xrjDgVPfuo50HL'
        b'JvmDN+e33r+7++tXKu63tn1S3D2lr/eurqhEucHrjuSe8V9/C97/xtpnfvsL7fsFBesGVH83NozzmffiX98/Unlow/uLlnufL/jw3wG7/vTR71+6dOIlzcs1wR95TCzc'
        b'caVw+/t+te8O5L4juOzwWcFPxuW98UX/4rfePnRW/uXhn/3zDyl/5/Sm+ogezCr6uirv1PSsE01/eWVOjP8lv+K2d0XmuX2Vu/8pWx97crXn1Uu9l85muW4O6HwWRd35'
        b'zafcN38V+rXTYtGRnVIv1jjuELwU4YL7WprXII+aX4F2xXKAN2zmOSYjA3UlaNRshFth6zBvAupKEI9aaBXK1WE5MdnPTMuTZcHdaC95XFwQAG/wauCeldRmwQfdhqei'
        b'5ZHwDDw5aJ3nIaZ6ILh3ETyYg/Zk5qE9cA++nAeP0hq80Q4u6kV7nCgVcMcyyaAbaQbaOWjCB89vfESWRHhmqRceN7iGaESOX8pMnU1rjM2RRxG2IT4I8+BVB7gXmmAP'
        b'e+97MG+8AG/ALTkFcnJmExlcLgs4uPjJGrbVZvQCasU3vze3BLVSsvioi0EvrUf3qHpqDq7sBhGhduXCoyUCwEWHGVzti/Aq1YBJ6maRi3MK0inD8tFLHAZegjtZz/ye'
        b'2miXRCp/DdOeecD2R+RkqUXIAHuJgmy3FJ2CJnpiFtvFLPtHw+t81NQIj9A+Dn1GQ6vKRUezGUzHMQYaCtBR1j+3dUMKzozJ06EuQuMtcoTVSQmlIm3pbLh/GqEyj3hy'
        b'EG8P9xXcFDwubtNbyNCiLmiS48ttSBu4p3PnZvHYHnwhxRE1o5fJ5TLc1/nyTB5wh93cjBJ0TerxY27BEUe4QZXdUMUdFrk0GDCUlWEpn517Y+wpVBJ9i2El0WecgN94'
        b'w7OmJLNvpMU30sCz+hIfds9J7weEm54xByRZApL6xElWkY99a86o7ZhhmPGHgPC+CbPNAemWgPQ+cbpVRNxoPadTX+IphxqPNHavuR8a1xca9z4pOM0ckGoJSO0Tp1p9'
        b'AgxcqyjYkGJUmYq7k0y5ZlG8RRQ/APie0oe+gca0znUHn+t4jiUHizbeUmto+IPQOFxbj7hHecO3N7x3zcsR5tDZltDZRp6R9zA88pATjlRgyg9u7NjY3tjZSG4j6IFv'
        b'xH3fiG5ed4XZN8Him0AITKXkpJgDplkCpvWJp+H7wm14xlgDgo9Ju6SHoo9EG9IN6VZv/4NlHWWmIrN3lMU7ilwZ091giZ1HY9aA0GPyLnk3zxwgtwTIcXGbXjEoFP9z'
        b'sn+z6RwnRhl4FuF4a5CEZtr+ScJppiTC5GAVB1rFoYYcE88snmART2C/OJrFUotYyn4RmMURFnHE5078MK9HAAfk4gFXEEY0mG4G/DtEe+DJag/aSLCbBGPJ0t+9CzVy'
        b'qJFhpRiizRyyO3USUG3SiHEWShQQl8CgTpMMt2cdGWYmUTn86MGPquY845QKXnZPc/4+as5KVs3JLyNw+8kqN1sn2VVuJY91fcaiI6U2ldvXE4oGYToBUBjS2hFUpFat'
        b'VMlra6o3SGNwc1xVbcX318Xyyso1FU9N49JhNC6x0xhOaMRywLeS+D0VprQDCQx/auKewSW0Z0k+JSr623H8D6WNPFytlnDX09KlHNZpy+2dFjNUTvihJAaNInElM4JY'
        b'KQcvAUpW2UV5/6kJVzG2nQuWcEtw7JahffttEsePQ7i2F9imqqemecVImhPtNMc+jWTzf6V7xRC6a78P3StH0h1vp1v+3TLUDxvJ7AxAaX1qMlcTHrsJ7DwWV0R1Bpis'
        b'odtgEttok1TTg2yfSN7/H3YQKqWcr0+MkjzTidZAJ9GMmM50avVqegRvuZpVJoy6kBzLa9OgLNTUrMB9M6dBWyuZr9ywWl1Tr5Ok4b4YLehG4g7D3YYvXDs5JiEmTvrt'
        b'ovBYB3bw84ukDPU28oO7YXc0RpromIYHeLMYeL5cpXlpeiZfNw1nm2YXkh0Qdu8jwDLN3ycuQcHMKs7NrK70m9a0xu1XCZLaSYmzJ4cs8T0S/NYrv3bazwFHlrg4Hrwj'
        b'ZUEtuoTuLByJaOGdVdyM8fDAozBcAurVsGuozIIlA5WPXWSBz9fQ7ZVA2IQ62KNjF6HL9qNjYW8dNQCvQT2wJwfLDYEZAsB5homFl8ueuO/iQPY7yHFYHvYBa0ugCJf4'
        b'fNK9Fhcg9uuc3ieKtIZLH4Qn3Q9P6im6seQV3muOr9f3hSeZw4ss4UWGjM48DCA7N/UJw3/QTgzZTBhFSN2wPZjlLv8Vg5xtLGsT6PcUfkTEoJnB7Pff9CMi7Nc8arQv'
        b'VNezms2G6nrNamW9bR1v0NkUefRo7XqtskanHHJEdvmGURWROlKoxjhFkYfL4KrwP+UKtVbxHeqmsTYSbY4Xp4R7QNCEzzggTuHuGzST1SKVQyM0jKlFGqpBgtdEQ5VI'
        b'6Czcorn4ST6jIyduvvn3DvZYvXML9rUcF2XGVqgUJW6vCft+whOrM3zzlG9VMuY5/5pQF2+K7Do/0XQ3/3/W74jZqRC8XZ/9B2Coc9dsSpdyqFyuQ9fRzkGtBdVZbFhE'
        b'tRbrIx6RfVDYO3WWTXSmYnPO5FGCM9ru+C3+sEPsO3Xq+jL7g6KIbaO/ffCPyqL8mGXjx0bCj32i8dbAicZppnpzoMwSKDNkWH0DDDpjUvuGzg2mhI7Nhs3vh0T2Seea'
        b'Q+ZZQub1+c2zy1F99DPUXYll0d1P4NMn+Cm9Tdj1yRRvZIb5LK3BnOtHuPQ7gv/cKVJPBevdh9/EU6/vOwlWJXIPgSGW4LhhIORpuTEGz9NEDaqdAkb4Ww2uXNvAYxO6'
        b'g4B6UpA9JLs3xX/H24pssOQyY2ywDM4/tVrNCk2Nsh7fpUb1JPRVo15nW7rjY+LHUGM/WXevYhXktAPtjqe4oRhJoXpNg0Zr618VjlXUS1Tqck29bsz9AjL7YQp0tavt'
        b'EoUG4y5lta6WVsBWzT6iSrVW9+TdhIYKlqL02VkY0WnWNJD6MFqOJOhNorVThdvKqlcSPPftk+hYZoiO+Q3E2TwwHR3OyUdttjO98+ULMmOy84hPV0tsIdLnLsjkFkrh'
        b'uSzJM+Va7WbNM05g9gR0c4XHamTgN8STGexc+qqhevAhlwN4De0PRM8XY5Cyn1mDbjouRs0sOEL70P65StSFrrsy5Fw+AJ/3LG9II/UZ0XZtso/OvWFRJrG2K0Z62SKk'
        b'R3tRKzxXlCkjzbRl5aJdDJ68T0nXwwPh6EwRhxxZ/YLr/Cx0kWrn3dGZ6KFU1Q1WN3+xfJEDmI/2g+cE8BQyPadZ/+ybfGpzKXo54PCbKWTiN7+wbwKGZbu+yjF+GLRT'
        b'/FO118/aXF0v+Cv/NfGn+Wf4ua4lr1Dn1ob4+Ph6zi8EXa5TVvvP/+3K3g/Kj3vlhz9rTDl03rplZd/qipo2TterzqIlr+z8xZ/FlUWbfvKvyMrriq7szlDj1s3g/JzE'
        b'wHfev3j0rZL33R5tSJ3W9ts3XD9a88qXcbzEujMMeHtLRPHe30ltmuVds9BFvLIR7WcZukwUoC41HHQY3UHHKdpDO5lYlyhyHA5eSmZC/eCSEwqv89AVnyxqSOmNzgU3'
        b'pA09TgddSWTPR70OD0fmsEre2Ayq5nUVcr19iqhLBDyPTiPj4FoGT5U8VsHPgveo/laFDnHiCJGsbp0Fks+l09obq2WDenGnukG1+BIJ2/a2VHQNtUhZ1bBdLwxvlLF6'
        b'4a0hcPeCBKoatuuF4fmK7/Lv3TJicXw8i5BjGYctNcOy6OJoti2OClfiBDGTINFGvKJ4lzDvh0T1RS8yhyy2hCzu81s8TFFpcwxe2BN+Q2YOnGkJJKow7xyGLp3pr1SY'
        b'pVnmkGxLSHafXzbR4M60BoYemfogMPZ+YGwPzxw4yRI4iVwxn70i3xxSYAkp6PMrGNGK1Dije7w5MMYSGEOKZ7LFZ72SaB66QNu0n+w/A/4davzOLtKD68OTV2pq+z5s'
        b'qX44aqke1n8tZKluBIO+hAWuDENOmHmq4Ec1fDrkFAuuuE//PkrDFXZ9HF4Wnnq5Pk7EcWL6z67S8VQt83gh+TZ9wQ9SykkpgQ1PrzA8NZzAaWMuLunF6SO3xccgVcrt'
        b'563Wqiv7BTrNihq1qt8JL4sNWi2Wq+dWDH3Jj6v9NjoAOV3Hbt9BYYbjoHESo3ejh29y9O6VrhR08DDoGGG/sYnvNAaMwCn8UcCCt5lvAx1j5g0DHYe+FXSwLw5ipRW6'
        b'fg/VQTzZtoP0Dbt6268dPMLiydv0tCfZq+gl+CmQNCXR48RI0pU1RNWhtOWVr8Q4ZEwAQixIMCZYWJA8OS6e2o4Quw4VUVtpalY8sfnBB5gimVutXCFZV6W2WabgGyb3'
        b'/LiE/aae1HxNbf0YzWjV+EZqdCmStJFioMJ2O9+BYAYPCBiCYJzzG8iJIagze9lwBIP0ti3C4kycVGhDJEyCF9wH96HrOVgoO7cyG0xAp9xRVzxsooJjXUlaTow8Khsv'
        b'fkMrGKw4M7s40nY6ORYcOVnodLAr6l4Hd1NZ1NU1CxgAiOsLqFz5K4UvaJiEE2sDYA+6mzq2NCrPzls41JyhdaETuleC4QtBZRyMZtpRKy1DtorRruXRWQT4RBMo9Bhr'
        b'oT2ZsuzcmCx5lACgVqnrGtRVSpuGJ9AL6MYwXEZuhzQdSfZe9+bI4AX0klSezQcb0VknLHSeCpNyWWzWkZhM2+YCuLOIN4OBF9az7wRKhdfzNudHsxXkEYf/Q5xnqzIb'
        b'6BZrO7qCtkZn5+FOhC/Bc6QjGSCK4KLDmhkaFVPLo75RsRcnNbVPJ34tTUeTZ+bteg2+W7EGHHDtfl8YoUicVq78pPP0wdfS30sK6z4g+8m7/3x+9R8a1nNfDDnQG/yX'
        b'Xh9hhhjsK/msWXFp2c33b332+d5m2fSHe8MNE/et47qvrHx/Z/HML9x+VXKfu6hk+aELry8M3PCxdLlZ+9uOX75TMPOC+viM9tBJReO0+Yb1lT+p+tv+d27nYZkBXf/f'
        b'u+Mnvbo5bp1kneb+tP+n3/83X7qEJkx2/NiEoRcZdYFLqzEuyoU3G/GTL2fi0bUC1jfk2GbPQcRlh1vojh1x6ZCJbk3nzatmcRu6XpY1iNvya+m+tgLu58Or6PmcrLwo'
        b'DJo5wJGcVrkVXULXKOyblgCvUdRVj84MIjqKuuZJKXFLw7TsdrjzRnpAw1p4jPralPq7zUBXiJEB9V0VVHPGocMR1GVmMbyMHzhxbi0gZ+bfGI925cnww4rlov3rNlCy'
        b'Fng/N2SvHR4vZ7fbUSfcKXX9P22Qk2Vh9O64C0ERtrllo2gotLAlUlAmt+2Rl7sRDWIy2fstZN4PmNgXMd8csMASsKBPvMAq8u1MJTl5jCnjVK4lfAr7hRbLMQfkWgJy'
        b'+8S5o/bP3x+5f+5rnPZYHXJfJOsTyWiZeeaATEtAZp84k901rzRVmEVRFhHdlE60BkcZl3dPNgcnWIITDHPtRarMoliLKJb1xgkef2xp19JDy48sJwX8jRnHsruyD+Ue'
        b'yb0viuwTRdJWZpkD0iwBaX3iNHZLOkhiDQl/EBJzPyTGHBJnCYmzhkUNOPCkXgMAB58DXpjoEQnoPrQz8AvqbByulfFgAd+nJPiMBH8EP2TX+bGVw/B9Zxs0/IrAj7Ge'
        b'31kCCk3AtveMn2GOG8NEE8j3IwU/GnAkapfjTlPAC+5p/O+DHKtYYOZov+OnBmevD9/MCSMoAK+RFBMMgoihuzdSHjHjP8fJx+3Nlfpot5NrydE52ibAuoipaivKyqgV'
        b'gJa8jpGaHvRzyzUVT7Q/6Hew700SvTnVxvW7DVNeUdg/RGD4il5lv1nP/4xHu+eI2WLIUNsFqPsA25n+ZHgVc+n0MOg9wOO4CQcACRyBu7d+sTHRxDdVdId36/pCE/sC'
        b'knoTX+diwaqb25M+wGXcp34OcPCIBA8Tp1hTZgxwk9wmDIAfFHzOt9c1wCNp1QwQBxmSrULiWWIVTxvgc8TTPwc4eEQC6l4vCjREWoUT+4QTreIUXECUiguIUh+RQJ+O'
        b'CwytIY3UkM6QKtKZRzSklRD3B6uQOOZbxRnkzSJzSRkcPqIhfcMIW09snzD2yfX4SQzrrcLEPmGiVTwHl/GbR8rg8BEN9Zm4jE+IocQqjO8TxlvF6biMzxxSBoePaKif'
        b'O4KeuYSeTEpPJqUnk9Dj6Ej67EmB2P7oeMboPreJZreJFreJAxwnN8z2TwiIa0bEYCkxCJ5gzLQK4/rwJyGdpTSYUhpMKcWhPs8+RESm8UNa8XaTDIBvCx43RVJkwx7h'
        b'PPIIs0g7OHxEQ/oUh5ZZQMospGUW0jILSRkbLeNNuu6kHse+iVNfKepzyza7ZVvcsgc4IW7hA+CHB4TkHGawphnDntAU8oSmkgc0lTyfqfp55Jf1ZSGKmhB4e4UuN5/V'
        b'EjHF3hh1cNCe1ejMqBdxkZ8v8ok3i9dwbxYVp5Sn4pbyNaBUoOKVOuA/RxW/1EklKHVWORBvj05+p2OnsJOp5HYKLzqO8K2IwyKji15YyVU5jfJsIN4gbjbPFNcRng3u'
        b'NM8N57mPyvOgeR44TzgqT9jprva0uZM7UFcED71npaPKc6S3yAhavDrd6Z0IL3qN8Dchwi6py7OSrxJ9Ry0iTJd4x8hUMXktZiVH5b3DsdQb9wVDfVx8VL47QKmvyg+H'
        b'fsRrpdTfVi4A5waoAnFKoCoIh0HE/6Q0WC/AV4bgvBA9wLFQHAtVSXCOhH4Pw9/DVOPw93G2esbjlPHEc6Q03JYyAadMsMUn4vhEWzwCxyNs8Ugcj6Q1SnFMSmNROBZF'
        b'Y9E4Fq13wjEZjsn0jjgmxzG5Kp668ZNjCWJ3OJXGqHh0XyWhX5C2mjqmnB8mM5JVk81gfVPYV/NicZi8GHCFVknkYFaIrdgw6OAwwo1guKeLFlewWl2vqZAQFzglu8NZ'
        b'wcriOIGI17hOdlugeoOktoYVmMcSaKWcfkHZWmV1g7rfqcxORT93TnFh/tepVfX1dSmxsevWrYtRV5THqBu0tXVK/C9WV6+s18WS75XrterKxzG5Sqmp3hCzfnU1OXg5'
        b'PXd+PzezeG4/NyujsJ+bPX9JPzencHE/t3heydxznH4+27Cjvd1hW0GD9vzkaKH9XIxqODqHociG3YFuHPGKZRWzitaiEzdyTEMx0hMGss6rnv84T8Vp5GzEovzolzm3'
        b'8BuZ4ambGBW3kVmLQUsjo+Kp+JQaxjT0Hh7Xyx1BpcD/MT3DcjbiKWojn5yMSFqowa2qHNg4MXcZSUMjKBvUbOH7HXInT7pffMWgS57KkVpSOX1YNpa+aaQXkW0MP3Yi'
        b'GnnBk7Q49CmzOiQlWwdN+ZZdJnY4pFA/nYUF8qSE+ClDWUSljpFkVRKVjkRXp67QVGrUKtmYih9NPVETYbRv9xeiLdt1iSw7KuvrtZryhieojlJIdopCpa5UYtA5yCIK'
        b'yboqTUUVqV3D9hNmNFs7mHlG39unZFx87a2poXZBj+8mYoIu4msmpp+J+5RM7Z9+g3++5sbExeVLHfqFI5slhizK6roqZb/zInInc7TaWm0/X1dXranXCvBT7Oc31OEp'
        b'QOvAkINuWcnKk8B44uM7EsOSgSAZoj6nxrke7HMetM39gADYVwEr34ox+qI239bQ8ZbQJEMmK62uJ28tNaXdF03oE03oLnkgn35fPt0sn2mRz8QJVGxM7V1vHiqh+gUa'
        b'ucY5h5yPOBv4uBLjBEOqIdUq9jcuNKV1c/HvnCs553N6uWZZqkWW2ltokc0yR6ZZItPM4Wnm4Nlm8WzDHMOch/iC4vZ8wxxryATjCpP6UM2RGixouljDpGdDToSYw+It'
        b'YfHkBAcD/v1hbvm0W58kMtk7yy4xfTnMlHPpsN3xoWOfjsANdWqJAo+sCizKVMdksP8Vihjtue9Hp81Oz+F70PnVMDrt5wZ8HUhticfmuGEEcewEzR5F0NNMuisHUYzL'
        b'YEdz6Tjtd1TqyqijYb+jen1dbY265omHEoy8qX+SkRrA3pTqyMoHIfH3Q+LNIYkW8kntC7afUvB1BbX8bVhdrtaSB2F7ApK6amUFMUdU1kuq1UpdvSRBGiMp1qnpXFHe'
        b'oKmul2tq8BPT4lZVCgVhdaVqZQMuSAoMr2V4dw2uZfQYWcfBt4mDwbeJO9vOA2LGMGz4j5zb/+Gfx5rzi+uIzMzO9+r1FVXKmhVqiZYmlSuJPUcta7uISyklddratRpi'
        b'l1i+gSSOqoxYNtapMSxJxw9Ri7tmtrJmFbVF0NXXYomezs41TzUT22ZhO0lllCQFeToNdOZl53myIAzaIOCnQ7w9xzD5wiUxeqqqfQyRZBKdBi9ptmrIZcRIdajP6JPu'
        b'0VZRSmVDTUWKwobexrAd+9ath/LaWvL2ZUnl0D2OBvooVCMew5hr1Dq1Fk8vazH0UpYTa9sn7HZ8p42oe34DUcBIUUtRtDwzS0a0xzmLyWYA2pOJowXFkdmyLLlgFWwH'
        b'q70c0T24E15rIK5WbvBWMGxFTctRD7q5IDJbTt7AvTc6H95EJwrlCEsuSfP4K+DNEvoC48XoOLyli8nLRvsrx60TeAEPeJAbwyymraMOeGrT0A2CyHx5VI680F5pTkUY'
        b'H4tDjvA2ehEeZ98U3N0wWxeJqV7CeonBvQzqKSxpoOYBR9HzaOtCuBt1FqPdaH9xHh8DSscCBt1AnfDSXOoDCU2pFYQePliNerjQyMAt6M7GBqKShr06eECXye7A5MDL'
        b'PLCs2hOTCy+i7bh5si+xBh3T6CKzw5VE2c3fRN4cvi+zSBPj18fVuWAuG9jy6e4FV/NRnLjxl1ePJmcFLvo3f/IM8FrbSyXni25tMz7vOzlnuecfD1/7KOJqtNeDV71u'
        b'qt6Y8f7Rvxy911U7ELjz/rXkca/s+CL41Vr/nNzfhrzW+PakZfu/qrD+SquL3yqbKORV1D3vs47HfND3mbcD7+Iu93d2teyoRf/8n21hup9GfL3njx2+x4tfyDr7heo3'
        b'y+LPDXAPf7Ph7vs3P238xGeTelXE3x+Kw/4+IfS9j36V+srPK478uqvzN5/2KUU9k5UXDqw8/9WJkzcyP849X/bLmY3iW7qObXseLX/Nu/aKefyR5zN3+Df7/+PLRM/3'
        b'5VX1HtEnz/3T8MczHx3++9/Pbn9bc//UjIHucvjP6789F/EP18pvuL//R9aR9Weknuxr3Lvg7jD65iPU6gDQnXyenLj13UMvU6MLdFc9PVqOdqGW2Eh0IhPt5gLXuVzB'
        b'kihqdFEeCm/D1liczwC0T8SLZeD1LHSGPY3raBG6Ep2dl8sAeHo1L4yBRxsns6Yabe6TcrLykBFuj8pzAAIexxGeh72skcfNUmjIofQwwBle5fky8AQywb2PiPdwJDSi'
        b'7iG7KegE7BpmwALb1rNv6rwnRb3RMdIo+s6mPD46zgce6Bp3A9qSwh5BdskJXWP3RKAJ3qG7IrAN7aMEFqGT09gW+ADdhi/x8hnYUxLJHih/PBJ3TyvamyWLgS2xcti9'
        b'MpNWI5Hw0K15hY8m4EJc1Im25NiZFbaF5BTA3bGUYUEUepmPtqEtcZTQzczKHNt7p07Cy4TLGOCi4qDDpXAH3aKB++E9eDynQM4AzlpmNrqdBo2whd6DEt0U5MiEaL/9'
        b'lDVyxNoktIPdd7o3uyAnLycnLwZed0Utshy4u4DSGQX38OGVzfAA2w8vwctTUGs+vCQTAPhCFi+DgXdgd7ZU+KOraUlgn/+Gb+x4sxNs2fA1ZWOQDVSMmUv3evbb9nqK'
        b'hMDT96BLh0tf0CSzcLJFOLlPONnqE3ywtqPWVHGqyuwTa/GJfeCTdN8nyewz2eIz2cC1Cn0Ouna49gUn9KSbhckWYXKfMNnq42+oMI5vr+qswiV8Aw6u71hvcjH7yiy+'
        b'skEvyzR2n2imOWCWJWBWn3iWNSj8QZD8fpC8W9Uz5eLq3lJzUKYlKPNBUN79oDxzUIElqMDgZB0fcXbqianHp52aZuCS8zT9Ai1+URhx+4cYBNaAIAPZvzmW25Xb7WMO'
        b'irMExZFXPMlpYMjAGN+UYwmNwyg/cJxxiimp2+HUdHNgvCUwnhjhBh3c0LHB5McepNatuu+b0OebYA2bYBQQA9w5xsj2Avvpa8lmscwilvXRj1UUZOJaJAn3RQl9ogSr'
        b'NMGQbhFPJK6Qc62ScBPPVHy29ETp8WWnlpklCbgc8bqcSANMiG+oaV2fbwz+kJdIRRoLaINfWX2Dhzk2umirwQ/ZRGLPYRvptDgLP/FvHxjfMPYX51LXRY/vfEPUE4Mf'
        b'zS64GFBxgMh9w2z7By0WqIkt32bbz6PvCHHAiNT+QgOiXRlxBuV/wL5/BUai746FRNNZKGU7wIQVnQjgxsiGoKNB2cQGSAk61dnk+tHAx2YiMgLRjsCvY+PV0TCqaDQ2'
        b'VhL8NQwu2tFbLYGVxD5mAwG+oylTVlSx9rKr1atrtRuoOU9lg5ZFgDrliu+hZnmsNhkuxQ3xZqtXaleo6wdLfqtBTM2gRQw78O0GMXbIToC2WjdUefmDjH3Zd3euI+/r'
        b'xcvyfIXrcRmfPd1CIA4GyXH5HJy4LDW6ynZw+7RbYD0eL6bkP+kWL/itO2sYsh3tCdW5uXEAg/bAI44AXXJZ0UC8CNALcKd7zggAa7e+sUO6ImJ6uxhjy9a5LrELhljy'
        b'4oVrY4gwBVe/V9PTfJWvI9vTJa8931R4mxiK1P/mpT+E+ezY4fcPrmDtjG1b9x8vNy3d4Xe+Xpk4rfwXltMzWwLbJ0vmj5uwq+DutPf+Ov5Zzr6msrPt7/3NfNSYPDM6'
        b'9KD1TsDU325/+MnnAcnXs5ZdWSR4tMB4bl7bNfHH+//8jsMbb//u100bP/5LW8rH03ed1r2zNOTXC5bNOR/0z+cmeW7+6//EJr+wL7mswXlh6Dt+b1/NzJkiv+O0gLv4'
        b'9MGD75hKGnPvdXwQ2NIf8qJ0uwAe2bos72j0l8+smvhx3Dda072XxN0Lzlb2vb25IWTtm5rxz5rdb291POJ37iPRb9FXjzjzF2//YFbfy2KpOwUmagd4fYhZLtzJlaNL'
        b'sINaY6BOL9hBzJO48LQdH3ss4lbDm/4UkywMiR7S+/AwxjvDIQk8iQy0lanoLnzh8cs+4LkMppiLWll3sZteyMTiCgwq1i4YASuivKlDWAHaV8yCKx5v81wCra4XsgbK'
        b'+5ORKbogD25bYz8w3QVe46ALaL+Sth02C52irwShLwSZiu4w8N4atJ89g/UivIWa7MCMlz8PNmFcFhVLcdlm1Fw/BJbZMdkGeA/DMnR74qMoXCgYdhVTcSoLk23vDJBJ'
        b'0RkHXYO7mLJYR3jKBZ2gxEjgUXgxmpoz84FgJQfezgqBN4XsnVwXiic9M9xvh5rcKGAnfR4RZaXRsjzUVrMUUwwvYoHGA+7jauEW2CV1+n7IyQkMOeTV5kVnk283utvW'
        b'Qtt3CovybbBI5QmCwo/N6JphDoy2BEaTNxAFGuuPbGINVayBoYYcq1+QxS8aoxCfkIPVHdXtNZ01BPgEDQCeZzyb2V1xpep81bmVF1fe90vu80u2BoUey+nKOZR3JK87'
        b'DYOeviB5z/gbkb2F1+Q9coJhsrqyDuUcyekOt0RNMwdN6624H5TWF5RmFfs9EMfcF8c8PhnWL4jVOfp2TjfNuS+S9omk1J2ve06fbzz+UIvlkr6lZZalVWZplTlEYwnR'
        b'9Pn9v9S9CUBU170/fu9sDDuyDfuOMGwDIi64IMi+DCq4L4gMKIqAMwxuuMUNxAWVRFTU0bigEsU1NNHEnJO2aZOmM3RaCX1pSPrSpH3pe7S175faX9v/+Z47M8wMgwsv'
        b'7e/94+Rw7z3nnvs9+/d7zvf7/VQDw5HVFdEdr4+YoguY0pYFBVP3Uag94EvUWkkc+Rlfr9BJK3RBCn2QQuuj4N6NvlisC0gmL/oEnnM55aJpuLilZ4bOJ13vk04IIixM'
        b'Y0elZpFOkqAnHI5bgjm6CreTSzdxX8ArOIesYuEWfB7wMFbtFk0aTrWTMZouFY17CXXo71QnWvk5M5rz0CbGeoOxycyiupHUhII1P8EhsaYTGKuTFRHslip4L5PavkrK'
        b'lz/lRVY/FUQmTKiSCmgTDDiV1daVGTb8VAP88lUqunk5cqNywK3MpOzKHbNtkRj3160i8qExANFtJzNI+2amPiJF6wE/MmguhWsUF9eel12UEQZc65k06B96aXaXoNvh'
        b'fDHpVP7JWk8O4c7iCM0EDjXAgP30CYY7omrhW54kK5c1sRbVa7rmjtKUWeZVrvRvYjXmDKXNN62PymrDG8xc7CnYJt5pVsEzf+M0PU6zuBecsbM+iCMpTAde28gd3T0W'
        b'yrd4mxjC9dUqUq0VaygrtYWfGhK1xS6K7jpGPWWjpEKuBT2q19fXVFdUN5RxY0FVXVdLx8iAfenmeu5chWtTzq53QEj5zgExd+JKIi1NOkJM5r0DLmX1ykrCklWW0Ve2'
        b'eBkb3OLxXGju/QydMzldvErNAp1HnN4jboixGxdNpsP27V2e3YF9kklaySTSBfT+yWSC9F3M9kdIrxRdKOqJuBuvi5ilj5jVkdWR9WVYrEbaL5vctalrU6/ng8Be8u8D'
        b'4UcuH5B/Q3w2fhH7B4YNX8w+oSEZvYGL2cGA0M4CMh1JAtqcRh6OmHYIZ0LvIUKCAjan2dFb2dCi5vf8M0KqgCaQbxFz1RAdtUUQFUcahRclVYIXYSmPm9tMNtshw36J'
        b'SIUpqUdx45EU92AZ1F0EY9Cp6pdN6FL1TLybenVH944u8u+R4H3nR+SfViLXuslHFsxkuguGrlCs0WaXKp5hFgD/+U/tYAYIiVRxVI8c6nZl4FKXkOtiIpfegxclFUza'
        b'hFRJiCbzYn6P4K6zNnymTjJT6zaTo8+m9XU2w819GsbWf02sgrUcyNtYc+qb2HX0L53FCP3s9Ks8JZz0cv3aUO3LWWO1G4ohKiurAWdQzqZSwO0qkuRPEVwhfAIe+8T2'
        b'kTU6qydZ5zNZ7zMZVi//9i1kOZVItW7Sf2aRWPMi8abPUK5+XmEqLQtDbqtsF2aizmeK3meKsTDz+yiKzDMKA980TKtk6mrhWU2rIRb9ymxqW0fT1LlaFm34mosvsVz1'
        b'WONTzsMM7YSC4WJbmV8PT0ekCio3WFQB3MIJnNHOesT0wxs3m+0PDO1c0pXSPa0vcBLMFhlsf2jkxcCeyLsJfaGzyIziNZsdfHY9mQ4JjaeWxjI4GU8tOebmGY1Xa9l4'
        b'cFvPM6j5EsL9gzUpp2ZoJdFat+h/ZqcTGGqezgPszOf2udWWAwhuIYmymjXo0v6T6BQa6FxNB8fM5w+O1Zb1C7cbgdD1JkJHnThhRXj2emAyWrOYcGzN83AAZjHPcw+2'
        b'QlODgA+dVOJvywu67YpcY6Bv7FUJSDl0C4zfBGuaKZ3lW6apNfYqf3hqpRyGxdgcx1qOTWPRyZJRrlBYLBn0fjtMUFMMBbc53YIQo5mvo3u5BsGh9OJynSRZLwHN2JF1'
        b'Y2o7OGN7Vs2M1obbn9WVYK3mSmK2VtMHu6EoIJ7TJjzRdKxJk8VtGT97bv0OmtDhBZtwD23CeOW2l2g2lXqV5UoP9/tg6OywOcZN1Z9oqH7HF28AOt/vel71cxSZVT99'
        b'0GrGfPgGdgjBYaJGrZPE6yXxWrf4ZzTAKuaZMoNdg9lLJYxV1QtfePSA5seAi7yuIY8w5JXgBKlSYTaKhLaawybbTRplvbrGolHo/WGogRmM7ZWOHRfzqb9U6yn9Vw4o'
        b'DnND2fq8FuWKY9ai9EE7dLLdz15I2p/ddiH/g0HlaKO1HV+wtemyxMq4gfbiLetYVtagVFcqqhtJdbibqsP07ARMMYtHaWHhuCn9ASGPA2R9AbIeYY9KFzBNHzCNCD3+'
        b'wZ2pXUKdf7zWM34wIKQzv8tLF5AAEaEdkzSRIHpxGNpaz8n/b6qaZ6OqeS+zLPFkL13XToQ7rqmrU3KV7WGq7OGH52A8vWBtN+gCpusDphtr20vnn6D1TOBqO1IXIPvf'
        b'VNsiG7UtesHa5vjCyJetbDsKcWI5ZcH9FRjiR20OcZNQ/vVwTQhJTQisaiL2ZWqiwWzTyLycTax1SV805TLaT6mbHgGtu+FdNot0NJ4/enwVz1C7AyLS+UjlkPWZ8lkn'
        b'LZkt0XCdDwg3rqmrqQTr//Xl1bWKSvOtGoPGq6kFHMrKuHxJI4wzNYLx0U3T/qiNri4aN9O8q2/SBczSB8xqy/rUP1QTcTGmq1LnP1HvDx6Rv4yK71J0r+2N1EXN0kfN'
        b'AsDIrI6p/QFhHdmaFNhQ1gVM0QdM4R5MJUnXc8OGCFkBM8GLxsxngCtNZGyz4o4Wfdnmwvvs7ReK57baonPS+16Ybf0NlUJXyobOLR3ruiZ2z9BJpuolU7VuU8dAr8Oz'
        b'6V39IvTW16ks6KX3b8NgOmdTnjENpkIzohrMUliQZLGMP2edo/qsCy376DMIL19lSTi9fwd6X7BZRZ+pgI51sq6zrquhe5tOMkMvmaF1m/FdyWnKzc+hsrq2wYJKev8e'
        b'UOlhpJI6ZutMPbqjfYfWbfx3QVnVcymzp6tTOefA3Gy9gifvW0iQAW1q8JzMOQw3bhkowULT9hx7jTFYnpA5k9tLU7qadw8Fz5adiIKvEHAs8JYRBdpmsUE6yjY6r0Vk'
        b'NUPznzdPUq5SKAcbauZpGFVQrq5dHVJft5FTcU5K5Kwl1PX1dQCf8pSXmDDAJpHZNMjYSQfEG9TltQ3VWyq57so5yxuwIzmtrm5QDfArN9VbrWfDDvO4OXW4QSgFFg1i'
        b'ePJDaJAVhgbx8OuYe2xa2zRqIJCn88vX++VrPfP7vQPbVncoNBVdOefX64Im6rxT9N4pbXzKoxtk4dk9gTqfNL1P2jPY9auUzYbmlcqsTJGVfzcQqqqpawA8sACoARdL'
        b'pR5yX1VVWdFQ3VhZBtochDmqKVc1lHG6HQOCMrWyRrkAagTcXpsZNZvG/IDYdEjkSJUpOHVhqlBETxuU4NSbW9HKIQCPyso1ENRAUAfBBgig2yk3QgD+BqkwrnwFAnDI'
        b'p2yGAOQJ5SEI2iBoh+AEBJ0QnIXgPKUTgksQgOm7sgfq55+N/T3CUtpwKilg4aSN6ySAM6CKElhaSosEYCkNgQPjm9icNxgcoXUK6A8Mbpb3B4aSwD+4ubDfY25zZr9/'
        b'FrkKi9I6BQ86ezYv7MjShGtWa/0Tej20zjN0zjP0zjOGeB7OE4aYZwVghDrTlDSG8Qpsy+13g9mCs8/1ova5XtQ+l4TNWSaL5FitW2y/ZxJYJCeDQXIy2CMnU3NkLsF0'
        b'rdv0IR7rPYcdEvJ95pF8IHxCQ5LMgXGR9Dv7DPEinYOGmJcNgG7fg0vhj+Tg4iEBPJezNEuojAqtc5jOOUzvHAbGtTKwt31OADmFk/SmHCGCdFwX7yGewHkiNMpEE9Qc'
        b'PHCydw4EK2fbgTfrXAzHTrZDEesMDsmMgYjnHAP28YZAzAP7aVMgFsDVaIET6yyFXAzBc7JiARTPRiDiQxFtBA4svGsKnpUOPKAZA5GxymwGTlaZipynEAZzlMDtfxJr'
        b'50w4ytECd9Y5FSgYEYieEQEc6siARETB1YhAZNk8Zg0lhNp4iWDY9hsfRIfQFRU+iA+B9XeWlGXEPjx143TbYON/54Hio6XtN/Uuym8WVAkUvD1iAwIhfw+jEHQLbSIQ'
        b'ikic3Yg4OzN0Qus4sRk6oXWcvRk6oXWcgxk6oXWcoxk6oXWckxk6oXWcsxk6oXWcC43zJnGSEXEc7qAPifMdEedG4/xInP+IOA5bMIDEBY6I47AFg0hc8Ig4DxoXQuJC'
        b'R8RxaIFhJC58RJyXGZKgdZw3jRtP4qJGxEloXDSJk46I86FxMSQudkScL42LI3HxI+L8aFwCiZONiPOncYkkLmlEXACNm0DikkfEBdK4iSQuZUQcZzM/idrMTwabecUU'
        b'EoYqpoK9vCKVcvvTBlzBi1zpsFPez4EPGGG3bpXIAK5olQxMpqj9VkV5LXCZqyoNRsIN1VQH1mhlRXH3jObDYGjFKZtWWqrFGpRxLQ2r4CjBzIPwSuBpyzlHeIq6CjVs'
        b'G5tytsitTmnMsLqBU9zgXjXqts5OLyrNNOSwchTbZoubvCqDlVh5yCqqZkKy41SSzT0cx3GfNJbVYJvfoKyECrHIr1xFXQEAcdR2q5HkVF5TE6KGnYuazcDFW7hOtnjZ'
        b'QraCvQ0QF//URISEVwUgtigdQHQZNjVvEavZ54kwDWZCyWh6PlZCDV/BNPHLhvE+4U5gcSe0uBNZ3NlZ3Ikt7uwt7ozeO5iRqukk1tEirZPFnbPFnYvpjk/uXC3i3Czu'
        b'xlncuVvceVjceVrceVnceVvcSSzufCzufC3u/Czu/C3uAizuAi3ugizugk13RIQsCzHdseQu1CJlmPGuiacJZ2z8Z1nnmczyBrrRJ9gmbBJoImy9oRBa9hWVSEHS0tNV'
        b'QW3oqG+JLN9SOpG3mLWRxvvTbJPgNHuGv03QUDT8FhGQrbZBVe4NxWa52pEv23Du0DDXMo8moSV+LcscVJMeZ9/EX2vqOS1W+LQqXj5op/HpdqVYrrxK8n+awk2LIybR'
        b'Z0+TVCkie4AtG+CVlT2NtH57TTkYug7bylIPAlLpgNM8IkNVrze4BBBxyvocVja/rFoxICxTVzYoAeqHc0w14Fq2qrx2XZnJCagSWlcJKFzK2xCoIKBANeByeMDF0pfu'
        b'gF0ZZ5VBcqxXK+vrVJXkE1QwtqMKjQ3lA6Ky9arV9NPrwC+rsKyS+0O9tDobXysDCwXyUsUasCigUPTlDWoVkc6VlaCZV14DSFm1VXWEYlqh1VXVFdTpCRHIuSXEFF2+'
        b'vmG4QAOeZTV1FeU1lq7uCb1EyFeuJvK9qIxO4SQb+reMq5eAMqsqLyuD6dmQVkiu16sGHAiRygYVuHKhWwsDdqRdoE0GXNKNLcO1hJ2qsgEipA6cTRJMDQOidRsJCSoz'
        b'PAIbOyuc+AyTHjfbD4vN0KpbJFZk0g3ajWVln8EWy+9Yo9YEHHKuZDsaNOmdG7UJM7XB8KO2ZCt0fmV6vzKtZ9mnksAT249t11RwJ/NtAlDTFrSLTfh0HARdVCzgKkSY'
        b'MOxCLDDshmHqzttftLcAtDP+DQ4nj536Q8JorOFFw8OgMOq4wfDQ8k+kFN4PMyY1/KGQdi7GNEbiIqLhb6jpPi4R/koN9A0GhdPPRERyqYypw6VXpl+Yfn7mRRCFxslo'
        b'cLSgLbMjklTFubRTaV3JOn+Z3l8GOIMz+4PDNKUntwCmYL9v4LngU8FdnjrfBL0vdXrN7dn3x8R3x3XF9Qp6BdrgGR2CT/3DNBNJMpNv7OXsp0Fx2vhS7cKluviluqBl'
        b'+qBlWp9ln3r6d2RqIrqEOs8EvSecl5FfvyS0bYsm4mJcj0gnmayXTNa60Z9kMujFOL6sZwvOI6DyB+zoHiN8rHuX0cuCO98CAcIEQzW9lJph1a4bdiscx2FANNQZ3DmD'
        b'ob6CMFrVVZsJ+2TG1ozJ5YXyEjMG8r34jDkI3HhL9Dwwa1pf1zDsZppiWL80apayeyyk+QBpw76wLUHzRlIGuNovDUx3ayyE+duoM3PgPCvKDDjYL1tnz8LMG5W0ICBt'
        b'2EWl1AZm3v+YOlpx746FulBL6n6ZHsJhqKvUqwyuwKgTISDJYOhoAEZ7JulUMuMyopYDIEjVk9dACKKgSDag1hJCSoafVVVXwgcNUgnJnSQYNoM0cRaqkBhDVcbEkcvq'
        b'BvrXiJAXQ3XqYzjguZiXdRSv1I6lPqOhPvtM9TlxJOjMKGMlPWNhuowEWWPwaK/84VimyVhLUqdbeN4H0JbKVZY++K1Jnj0vK1OWmZVROhaSPxgLyQl8c6dAy4wT+zza'
        b'3cw4UIM1rtGFkZWZaEJIJgWi4YxiazaWb1YZ3MiH1FauLofTlDEU6EdjKdAEy+EXYxx+RmtYszIZeNGQ6JIFC5e89HxPKPvxWAhMsZxYo+gSWle3DqR+zqW+MqS8vr4O'
        b'PAUSAUHNOeF/2bmLkPXhWKibAtT92Xhy/tS11OQ/7WWpMPAbH42FimlARRhrMcOvJxNW+epKs9FTv2azCkyvQ+ak58nJBFfz0p3sKqv8yVjom2mjDYfpqqlbbUlWSHTB'
        b'vKzsl+phhtr7eCzUpVtSxxmv1yriG+riyZ9hVi0kOutlyTK4HfvpWMjKtCQr0CYqRUh00cvSZOju2rHQlGPJ2JqwbEM5g38iAtaCey/DRMEhk8yZP2/OWGYL3VgIzLcc'
        b'j+50SaFCs8GZ2Ri6vH4shBRZtl6M9QIB0jjYNsJ1dEZxcUGePKc0a9GYVrKfj4XAOUDgv5tq6r+sCbTcRkgIySbzbE4lIbmWSjAq0xYvt14YPB5AoWBcR5cszMsunV2c'
        b'mRUXkrNgdlzInHl5Reny4tL0uBAoZkHWYmkcNT/Mhn68xpDnaLllFheRyYHLLju9KK9wMXddMj/D/LZ0Xrq8JH12aV4xTUu+QLedN1arwMFEfU05ALxxcCovP2B+MZZa'
        b'XmA5YBKMAybMbJ3l9me40VJOJ5xyFcni5SnsGwuFiy1HzCTrfsDtNCWEpA97ZcyTZxeTFs2U58DiC513DMT+bCzELgNix5uIlZRSppDbASOdRgG9te6lBRcyxgfGQk2Z'
        b'1bJrwN+hPk85WiqHz0DMRfmXr63HY6FvleUQD+Rqy7hygKeYEDjbscEKmNS7gDrOxGSYKlWdha2zi4WSq4VpaL3IPI46buQ1seYqWuTadApiuaPcxJQxZqlMpyPKceZ3'
        b'5nSV2XyqMZ2kmP9HUpjOVCz3ulkbrMXTafM4ny9wDmXi5TkpZPhEzLaUkiAVK78PbfAPIB6wHMxgHOjWMcA1KFloYD632UkT0Y1NqA2TSY3j6soG4870Fn/rRjeLrCSv'
        b'qeD84NudDNgfbgOl81wWFMynaP1ndHl2+/Zk3s3VRs/Q+uc/8nzfty2zPyJWk9OV2RNxV9pb+mCZLiJfH5FvQnGGrbi0/qSUu4Edgk5nvU9Cv6dPe9Fjz+Q+z+SeTP3E'
        b'bJ1njt4zR+uZYwH6bLubg/QEFsUGreVSzsBxZN8GJa6Rfdto91YHEyu8aTB7e4Ye5SLGelwpPUdT/bY8vbFU5l49UvNyDwdV/2/k2YAAdsBt2DyLDXvjZbYKw8UoocFi'
        b'uMJ4SPQeEbAhLSPt9dg/rs8/jtsP1XomfCrx78g4uql9U5vrMyrYaGxjVl4n87u1ZiVQsAabE3oaYyyKkHYj2/bbNZW1pCg2NtZpxEYoSZBVSZKpZX6c3n+C1nNCv8Sn'
        b'bQOlXi4Nt6VySHfuqZLggIvV6QsdGHQcDQ8hKDcdPQPOlocvIsPZi52BHVWCKe+AyHDuIuSOXQT01EUAhy4UXWfAyeLERWQ4cBHQwxMXq6MVR/OTFZHhSEY8fCLDnYa4'
        b'WJ64KIN5hs6tjICrKB61hxhVNdASDFP5FowKa8UEHRxnfGMFoCKyB7VACLwTnAOGmOcHCpYJGt9hAgWZNyTkBZWCKh8Jn9CwWW4FZDIdAEhmAv7ITIAfmfnyUCg2czBH'
        b'tUgDVIt0ijuSTnFH0jkclOE0QzyBl2xIKJIk/oEhwRMISBIXM+yQfs98AA4ppMAhhRQ4pBCAQ0QWaaDEgbTEgbTEJKRpOKgUMNsf4rFeU4eEfO/UPzAkeAJBc/aQ2ILi'
        b'WUBxBqU4g1KcYY7cwhV7BhQ7DYqdBsVOo8Ue/k6/ZyRAskQBIksUALJEUTwWc01LqBcvWi9etF5ISDUtn/sV8wSTIMEUSDAFEkwZkSAZEqRAghRIkEITBER0mCBoAHQk'
        b'AEBHAgB0JGBqc6FVQaKhIDFQkBgoSAwtiPknoLo8aXV50uoiIf3KcF8c4vG95rJDQmEQaIRC+ISGpDs6Mf7hHaS3gTOgfs8pJCt/0jQkeAJBc4EVMYVAjJwC3cgp0I2c'
        b'A7oxV0+NB/VUGainykA9VUbVU1+k5s0HD9RbENRbENRbUAohdVSoHE8WRqApEPEBn8YUOPCdfeHKOuB0++C8PzIGH3FsdK53kubjg7HywgTwxIWP4F50nM/ErBGiHnR1'
        b'goWen3FV4+A9+eZ6fnuYJXweUwk6flbr3RIhfc4f8VxEnwtGPLdTCElu4mZeFasQ7REvsVfYkXsHQAap4inE5IkjjbMnV06g9bfEWeFI2QKnAQ+rKa6wWtVggVDKMy53'
        b's7jljrVgGHnkzkQIWAWUmdjQ1cBaminiGOVoAd3bGrAvU6gNuuz2YGpWXlPdsHkgzPrAG+gpM9e3UhnNohN4VKndmInYmIfRQDrEDEggwEauJlSBnbCWRnJrqeEAN1RK'
        b'j3MNf8bTg9lwLf2N5XxTCbU4mlhhkzYTxj2IFpsYxobF0AttWUwf64f3w4e3juHDhh3CGWP9cPPoHzZxmnH0wy9mHWWU7XjKcGADZtqmC1iEUXsJ5R0P8A3GRTsZYA8z'
        b'9QEynSRRL4EV7bswLjLUG6VvFPMiysOMkEgMVFK28BDfYGI/bAFFOFqdRKaXwCryYtLC6udKC6NUFCcxtEEDhvKMDWjuBMxkeWdmMWrDdlZlqRbI2nC8NTznmDW8AW3H'
        b'n8SbC8p8q3hHagUqsHyqdG0wKe3ZUkUkb5gEXI2Z+7Dh/6yt61luztsDXtvizXd61gNMw6ph3I0oq9qMskyuqKvk4AQ4V2IUscnoRZZyvkTwBVwiOiFS5luZBlezIKAm'
        b'VdCnCJteX19ZqzD6EHM0+wSXdFTTYH65QjFCEKFNTiKO883sUqlmSGzXDp0kTS8B+4lx89lP/cK1ESU6v1K9X6nWs7TfI0jvEa5puLi5zyNR65HY7z9e7x8LRoR9/tO1'
        b'/tP7/SGS3EzU+k+kxlilOr/5er/5Ws/5/W6eZBp+7BbT5xbTNU3nNlnvZlQ+cZv8jDEI+onDY9DmyLPw/jNi3I2HcedrqwaoANfJN4AwDo+6o5vbN2vdQp5hfDqJsZ7D'
        b'gCdoYjKtZGMb9pE8ue1yRtMsYd1d7gIO6WyJokd5B11hSjQWOAaa3uATB+ppgG0wd/6gBBlzS7ytojfUNZTXkGkb1NpUM8kFcA516+tnAuyUCvLayWj9p3K/rg0d6Z25'
        b'nXLTA1ozUnaAr1KvtyEAC2nutuucRp3jGyxSYTr24/LsySSBzn+qnoSSVL0kVeuWapCAXawl4GELOTpshkeMSVjkZMdCnqH9lfN4dOfISmyEyjcJjanQT2xxVNuA2n9j'
        b'RtiTScHmxhA4UWZdG5BMfjqPiXqPic2Z/UTc2aQNmUZ+Osl0vWR6c66NR0MC1jkJeFpDIGKdE+FqRCCyYoDtwBZntMCddQ6FdCMCkss0uLIOOEYZtlfwHjl+3Q69aotZ'
        b'voNb4hJYJhO/YVdYOMOCWzbqJv8JOuWrfubcMvnHo//4ncIlfIA4U4gUdgqxwl7hoHBUOCmcyZWLwlXhphjX6bJE0MxrFhLe151wvELCBwubxYBI2Oze7FtlB3iClJe2'
        b'o6iBlry0mD732sMovLslNixj7AwWJ9ZxDjSOszixjnOkcZzFiXWcE43jLE6s45xpHGdxYh3nQuM4ixPrOFeuvFV8RQQpqRtNKasm01+lm+XccpE9zC5xI6ndDSiF40it'
        b'sRSj0J1eAUKhhz2HJ8mnjtlFABDU7EgxHl1InbrRWvVo9mz2avZuljT7VHkppHvswSKm3a7duzvGCmwuCb5GWoGviBuBTOlF3xF3x498h9CSMCK9tyKWcncTBpxgzBlt'
        b'JwbYOQNssVQ4wMvJGODlZQ3wskrI39IB3uzcAX5GjnyAn1lQMMDPyZgzwM8rIVe580gwOzd7gC8vJldzCkmSecUkKMmCiCUFSsBOIW/kzZG6DPAycgZ4mQXKhbCs8vJI'
        b'3rnzBniFeQM8efEAb07hAG8e+VuSpVxKE8xeQhLMJ8TkjVgIqInETgZ4IfB9v59wRNT3PUPENQH1fM+34fleYG/Dlz15Ihjh3Z6/XWDwfG8zzhyDST5CbqVLipl/dIFc'
        b'nUvuCvGJNTCu0f3GBtxSnIAPFeFDsXNz5WR0g8vsubiZjPeEPBLglsK4vKK5uWTE54O7bHRVwMzEr7iiu/htZbUPduFRJ7PTgvmnfzzhzPnjV4+vXnm+/Xzzu3uOsi7z'
        b'fE6wm69/HlZ0MLJQ/Ikwt0bwtSLj5x4fPTrJMilt9pd+j6V8CtSOz0bYOaKrcbkGL9Q70CVmHH6Lj95AJ1AP5xr87CL8PdxajA/ko/34TFECYIWc5m3CBxRPoA2U0/E5'
        b'1IqOkOnpELpZEI+OoCN2jKM3D+9H19FlInHa2jGEFrTSg/Y074dGJWgYmKoJjAGVPZDxlHTEaT3Gkx/ljYp1fnP0fnO0nnOsVJ+NTsm4pdpuWGVb+QWsTDZ8L1P7dwPi'
        b'+POoug1L0kaGwxonhJUHsmwweFJ+TvCdQYiDxNFhn8DccJnOrzCZ2pD/XIyd7yyMDDtuZOzn7xfsF+4X7bcjY8SBjBEBmYKEzXZkWuImIhGFjHWrcqHjhkzjLY5W48ae'
        b'jhvxiHFjP2JsiLfbG8aNzbjRx40JXM1s3ATL1dDL8SX0ZmaBERWYjJL4+IS5ufnu+MJ83FxcEg09eP6cjWhPLuriM/hwvSNuw7vQJXUqeRm1r/AffpcMqOL4BQASICM5'
        b'4ENkZT1SgO67LozGLQvFZGwKGPQ9dNPReRPuoEgFv1KKGCeGcdNM3lQjjl/HUKSCmAYFxSnAZ9B+Fh9m8Bvh+AFNrpCIGdKdEh/Vral5LWEFo44lD8lgcTWHwrLCLLBj'
        b'cFft4hK7zXx8jwJhLV7RUJBXJJ5aEIcPSVnGUc7Dl9HDIHUo1MXt2qjYXIA2wMeTVehmYiLas7KACUP3+OgdfBcdUstIqqY8fCdWDi7qDxXNN+EiyOZGJ8RH42ZZTF4R'
        b'y9ThHqSRivGd6EyKnrU5P6MAt+YVykT5pEgiCc8FadAeOoKoeW6sBPXGQlXHi/AufJ8Robd4k9ADfIuCgUWiQ+goiZbi/dAYdox4A88Bt6ylDSjAp9CNkhE04FNb50bj'
        b'I3G4ZU60iVg7BnWi4w4LSZGvqmFklsnR7RK3jYSOaCaah95Vg42WLAUfUDXi2wLGP5RFJxl8ZOYadTp01SnoKqnrQ3EJ+DDAntWTRKXRpKFb4+KK5ufiw8VG4AgTyjRT'
        b'h7rxRb4TmcJ24ysUbgzvLmwq4KLxTnxKig8UxosYjxw+afG30eu0PtAV1Sao49AtlHCGcSzgodfQNRHl49D+tcElAHSGW9HV0uEyz63AJ+n3GabYza5eiA/Q8pBJ9PhE'
        b'fBxMmLZI0RtMEb4bog4hd+nooR9h/G5tbCSNu68CtWzEtxtEjLM/D53E3XinGoShlGV4j4o8Jx07bkF0fjzpN2TZwOfxg7n0W8O1S0qBjuNeBwY/TFcnk1cnolcRWW5I'
        b'/ZD6apXhIyXR0WQxaJbJDZXF9VC0E71dia7aM+i0ixqMygLxSXzOEd/Hd1X4zQ3o0Eal0wbSKRjUkSRJ5qM9qJenBnM2D3ywDreSjl8Ujx7wE0itCxl39Cof3QjHLXTI'
        b'4CQBDP6QoRUNhdM2VjFcfdxagS6oNhBxmtSgZjyDDmQsq/7NnVS+CnSuevLWvto+ow4luu37/Z5ZH+W4v2Ov/WnLvYr9fz/wd8a7YP1u/QI2qbT8qv7ztxYGus0b7/13'
        b'heu1ZV8MLnhvnnbGH/7yn9vW75d9ddrX6Xcr06vXJd7HX2386FPh6okRn4X9/uufTLOL/fijKxWtPz0svr7oZMwP5nolndvp3/Gj070Xr9svmDU/4vhv9n9+JUX1Vprw'
        b'afXOOdNOR+Wta/w66b92Nn8obHjT89NKt7re3+U+TH6XH1pwZ/b/6dklj7l7+djapi/7Vtz65pvfzgx/7U+/9ez6quvAwulfTF3NCzhzp/k/Yn98rftq6gLRpltvfDh/'
        b'45Of8WVf3D6buuSPPVfWVO988zd9rN2OTw+pH/zylnbtH/Uf9ez/66Ki6I3803vP3FduXZ1dtemv/2V/8us1FxrWBT9oUEy+8dstmZcHKn4y+dKDmZ+0Hox03PbNsqji'
        b'3/n+959Xixun8LYmFSbPPfeWkrlfe+mJ64w6je+01E9/9yNRrbvX9+wG5Q8jtt/I3Rt+WF+Y5/K3b97y/n7QvNPid/dU75/+++S3Hf4cfacteJmu+Nc7vzi+zSX6ftsH'
        b'DqVHvy7VHJwY9jD8YtJPPsldnXlh5Wd/itg+8LOsDNetbxWK/xEZO8fxhvv2P9zZ+NcjsvXdv/J8tedpSuXtreODdjCOTzTvTE+Uhj+BzpKE3sng+BF8xsMAjMHxIz54'
        b'J8exvEZ64i4ymNFh9BBflsnjcwEG5CYPX9qETtEkMnw3w4CtgS+gM+b4GsuwhgJwrNu+A7VudHF2UOJ7Kny/wXmRr4jx3MAvWYzanlCpt3YihU3D+/ApXiObPolwQzDm'
        b'Rfhd8vVTabi1kIhmfIaP32HR6Th0h34Z3SNTVwshTo4vbSUE4GZK3A0efh2dT6UlJNRfRedRq2sjvl9PpntndGSpiHGU8NaUk09T7LtbWes5nJYcB4rUEt+ELtF3l6Gb'
        b'6ARhD+NipKgHn0qgMyfD+IQIVqx3odgpO9A7yoKEIhjjO3ib2enoFnqFIvXtIK9erK0hg/wAGU+EcMFUFt3Cd9BuChRH6GtH5wrILEdePcDwVrAydDbwCaxdtfUrVI1O'
        b'G9T4TVd0AB10FTs74B7XRjLg8f2NG5zxHjKjFAlE6Hs+cynQyjIyvZyPjceHCpNYb3yeES1mcTfavY5DYWlHVxCZanLJDMfgTnSet43NHocOc6hzZKAgwmi2ou7cIlKN'
        b'RxLIFPYq2s9n/NA9wUZ8UU0ZTnQgGfdCusP4Npm2jpA1q5AwnLN4+DV8E3dzDXFJHAmALnTaacD7uGnHu1DgjPbhPRx43bu+QahVBp1NiN+Yx4hW8sLQ6/gCZXqXyAgb'
        b'2yqTywgfQSdOIeNYzMOvipGGYgmul9ZD9qQTFgMDURRPOHSoutu4OxhfEuA7m9Fd2mSkhvfi+4a00Fm9UYuAcSFsSmaGglZ9CdrHUBjEQ4XsBPw2I8rjSaqmUViaetwS'
        b'A6+S7OWFxaTejhSiNi+W8cOdgg1yUlTokQVTtpDKMK5lJWKWcSnhFy3GzRxC44O6aBKdkIoPxhPOp4BPuuMBHr6ybhKthDR0ngyR1mIFbsuPyyOrPiOewltln0xBf0rx'
        b'Q7SLRNIY1EwqXBaWSb6RF89jYqKFhAdoQ0c4YJ8j89BeklIeh1pkhtVDyMzFB4Pxm0JhGu7l0A9PCknrE2JIgkP4ihFnyB3d4OPWRtITKbd2FB0jXyPjw7neTEZCLeiI'
        b'TIraXS02RGJJlR8Kd0DncDPaT3srOjAt0fbLjrMJX9BcKBUxhYwdur122ZN4SN8qDqQr3xEicZES5haRjx+WFcQvxrtjgIHAR/hMDrplh45k59JS4F3zNkDXIOlaimvK'
        b'uVdEjDeZCt5FF/CFf7oPJqMJqbUPJnpY52UlrnCndFSKWsnpXgzVBDI+YW1bNFFdkzk/W7DXnMftNQ8Dew9KgsDHMOdjDVLksnRHOVvnl6P3AzWqQQkINeOKWIohLnsc'
        b'nNwXnNyTc7fwkfuj0Efu+omZjyp1wYX64MKxw4sPSgLBjX0++UZUV0pfcKI2SN6juLv+UZ5+klwbVKGdV9GWAy7ulz8OTOgLTOja2N3Um9E7tzdDL0t7JNEF5ukD89qy'
        b'B30DOwMf+8b0+cZ0TdL5TtD7TmgT9UPe7LgCrlyzHk3SmfsuC448t+XUlq6ongm64En64EltToMS/xNbjm052tTe1Cbo95B0NGpWd+7QeiSQH8miI0ZbstDwW1xm+EWu'
        b'1PmV6/3KtZ7lgx6+jz0i+jwiNPN1HrF6D/ARNK6QJRVWwF1RMvJ1fgV6vwKtZ8FgQNi5/FP5mq26gGR9QHKbfb9HANRFJquRXAzoWtW1oWuVPjSp11cbmkF+lIL+yFjN'
        b'As2CrtKbi68t7tmsi0/Xx6dr49OH+Oz42QAc4p8JwCEkBG05EpJFL1gTx5WhZ+PdrVxRtJGZjxp1kUU6P7neT671lA96BAGNc1jNtJ9PKtSGw89Qa9N0kXKdX7Her1jr'
        b'WTzoEapZpvVIIj+SdXTclS0Xtpxvutikj5r8OGpGX9QMXVSaPiqtLVPvGaH1jBiMiqWXg8GR1BA4LLrLXx+WQq5dTUbFXIzRvNdgnBwYem7JqSUnl3Uuo4nCoy6mXpz5'
        b'OHxyX/hkXfhUffhUSB3SHxJFUxvyMFgMj4/ibJgjZFyW1gjzxhPr/uBQjqjxmgiNmlCtjSp/lPN+4ePMpX2ZS7XLVuoyy/WZ5bqwVfqwVUBym6tB443bcxhn8LtnNNMX'
        b'wHmVshTiJ8PelmNFeYPJ4l6kqlhTub7yRYGhzGYEGPorDf+Z5oXnTghvwgbGI4bbwPjWsIuxLpBlqSevf0H4Xe2EUIisK/YzmIcu6Y78l7abAC8FtOZHO263rD7jOfu3'
        b'FvroL6vQcPEZx/u2v/fUUv89GpSkTf5yuAKEGMCPQqKVleWK+Lrams3SlzbH5hTNBxzLDIZZZdWKlyP0b5amBPE7DRTH2bL2qlYNF8Kc6pesz6ss1V1+OUJhC9nMpDCo'
        b'lNp4gYWXyXBzbBRxuvDgBkPdUFdV9XJU8QUW7SyjlkHqhniSUQj4BBm2RgNKqZH+GMmktru+L90RRUDgsDVBDLUmqK4ymA+sB+sQ0qqVteADSfE/aVRShU5lZjPky5Fp'
        b'D2S6G9UoOMsvsHRYDdCsJhPRsTewMvKlO5wTkDRsFRJlie1qBD3jrNHMCTOja/j8G5SaQCPO4OuOT7dt4YjeCtJ3G0u3bZkR27bsiK1ZZjtr2La1GWcO9Pv84w6R3Pa5'
        b'fSPQze4nyahvM6Aa7C2sjmO28ext0DESsJhQxm7nGai2GWeieo+U97matQFPDP8ZTGIqqfcvS8MIVYhqTZ26RgEqJ2SCra6qBlP81eVgTmEzrwaDs7WQ2TWV5WDEFZJJ'
        b'3QFBx6tTgioKZ/YPy3A1GcOcvVK1ymZmqkqKlbxyZalSXUmW92pu9Mesq6ttqCOzfsW6mJCa6lXKcpI5mLk1llfXwMizmRlYbTWMmOXIa0aNdA6/mDOf22xmlWYzN86w'
        b'zkRgdnmNilA4EjkY/rPoLqbBZdZd+PLq9JnLBSoQWH/UX3H6x1POnD8e2sqKXvGd8rN/d2TGt/B+XTkgZekuwexYtA+1ojdxl0EGs5DA8F68hwxMN+PANKjhCKpWVzZs'
        b'ibAYmaqKmjJaicN6GJCKykpwjEJlpRAmIKQzTetpfppk0KG0ZNPoidZKox2M8hFoM7zQ99zIi6oqxgA5vjyEZd2BRbIOvtOjo+P2Uuaqy2S+bXCG7TBK+QZAcSE9HGIN'
        b'R6oAomB1HPpPABPf84JHqrBfIPEstZbf4XSnJXZNYUx+HLpWyp05wKPiQjj1QNdRi+PUEry/+o8OGUJVGslDvnwDd4j6vdzu40mk3x34S0HH5wH7PH9QedDJ6bpv+f8d'
        b'nz1+8Po+uSaoVCe/vGl8r8u+laKPvZmopY52Q99K+U/gyMVXjW4AKUiTNmI3wWorAXejB09gEx29jTrxEccYdN8dThoAnNiIBxyM7gjwzXEyboPlNOooRq2y5SJbfb4F'
        b'H3iRY1YyClQvNApUhlEw3TAKlCGMD8jKXoWsZr4+cgZ3+WlQjDY2XxdUoA8q0PoU9I+P0Si6Us6vu7iuLbO9uI38sziBpWNm3LPkG8MJ7LAHcuUPX2wUEXr9YBQ1MkYI'
        b'3A1kGPnCuHlO8J0B30ZBIXn0GE3ggt4poJvHAvQ2ft2VRVdy8bs0aqoanyyIldOonrBkFt3BV/CD6j9948SqUkj8HvcTp388/cwu6c+Pn98tPZS099be170/+N3K/1yZ'
        b'VyEv5/3RZ53PWp+Sjq8Shcn19xnm8Uz7oaYAroKfY51j7tbdVIVbvG1XLW38Eq7x+wXioSUh4nGxQ4yNwJM/bsIQ88xAzIRGdim0kmTtsEd3I8mj9gRLkpUfQD8YhVhX'
        b'aPk6Q09dStrdHlp29OA7a/JXmNHUEyl7xqNsjoAwOrx/LaPz/KmTrLdf/Py3PBXoV58cfHj6xxPP7Go5f/z88SNvwez3WtKExO6qPX+A1Zep+4TMQtfJ2juZJJ6djm+h'
        b'VtcKfMbW7qztrdlZqEvKM2taHp2SzHSyrTUsqDI27YK+hladFcr4+NvUxzZ2JBsL8nBHMlPpGP2DodCN1jGGZXjHaMvwd7oWP6ML/b/klOXPZdgE8tLqO0td+Cqo7bIH'
        b'5wjHNvDwTOjepI5dyc6Myzu8+UfSjErwVqwYpwRvvSvFab/TRnc0NHo2afQAg83si/Ndz8g9woLRygr9ZzcuIKr8L2vcETo3JpIsZ4cBplWoAsvVX/7sr5QbB6WyVN/b'
        b'gw+EhU6LHk0IWXFokJ1/c99/CLLEVYOFfCa0X3Ruyw7CCEHjLN2AHsIB7TU/OCkSzGLRvUnoLp1AyESxCx8Y5XQH5g9nu5EzyIwF9CirGr2Bm2MLPNA+ONqNFzFi/DYP'
        b'HY0k88vIXkZtUkbsfVJjFNrLwrle9udC6GXUIOVxwKS+gEkchJMlANKL975nfDXKovcV/Et6nxJ4fQv1sABje78FXdDLpnoY6Ke6UD/6Rg1VUbMH1V816ak2+zb7Nds1'
        b'+zfziWwQ0BzYHFQVYFIdc/7foTo2XU5VqfB5tHOhGt80aDZxak2nMjmtJmCtY3APfsVRie/he64b4Gx6Hqdg44Yu8vBb+GG4Gthg/Da+o6AaNrmk9xWjbjM1m2EVG9yD'
        b'bpvUbPC+TY7oHm6VSkWU+UOteCdfBSoyDG4DJbP96KDDRC7qygrUhe+oRaAHxDQS8eDoOHSd6sFUpOOHjvg+6MHcY9Yy6DzavUANG1NCUakKLCBwM9NEstpnL6eaaZ7o'
        b'SJkjdEt8k0E761AHPokv0ZpAF3EXfqgCXGB8jDCgZ9AB1Iu7qQrOvzvbcUpuXvU1QU1hDNXoQu34NroOukeQ3evMeHQIvbYA3abfCQxHx4cL8/YqdDAGt6un0nKiV3GL'
        b'iuR/HOrLqppwT4MS3y3JjQVFBE4dqQ112G9bhzvpR+PRafxmMr5PGOO25EQBw5IKwTvDsqhWG9oVi65RRTp8drNRl84IFzF3zkL8anJ+iR0zH3eI8L0iX1pPIegqPpoc'
        b'piKXSUwSuoQPq2GsLpw3Fx/He+cT/kjGyPCdjJpv//GPf3yVz6kirVRUO/0iuZRRz4YCXsOv4OYC03dwc24cyJiHZPnzo3ELIaAkWoqPTMAXFubmFYGkV0T6CLo/D0on'
        b'qnVe7pBCNdPQ+Xx8CvR8zZNBfyLzXUs4PiYrNtSRuXogdKTr6G0nfDt8pXolUHMdHShwJq8cdUY7E8VCvHM+PivCh0uds939xNPnEZHyIT6Lb2at3mRfJdnggB+INorR'
        b'AftiJ9SDd+OLifjhVmkwbp6WgE+J0InZUnRCiO7MnIhP+pDOssdRPYd8xCe4Gs73dzkzSWI+6pmPbi/Br4pQC96PXo1Be/BDfAQdLvWv3k667U5/9HBtmD96Ex1Ee9H9'
        b'qq14Dz9KkhRNiDgUjG9lehQtSKIzEe1pv47wYyfyGHFP7I5tv1m2gKHqgRH4JiI1U4S6hXj3HNycRwovwy1zqHKnSRsNvZErLyqiMvwN/KZjhbqS5siLzmPaGCaxXrQx'
        b'f0mZPaMGHTrUhfbKoAgn7ZkQJ3KxYMU6dAx1kxF9nk1Cr+BL0/ANdDiZNMfxlWSUduNT86Pw60sI0Tu9StErlah5NdbgXrs16IHbZnTFVQ3y2QoheouSaUbjDjJnEDJz'
        b'4/OF7l6gp42uSsmPQQfwdXv8ZsKmUimrBp2UEJkIGp+sdPhwXpyEjKzDuaR1JWJBInozgm5m4DdK0eWC+Pyiklx8WE7Gz5HYPND0jF1AFcNNPf5wblx+YUJefAzpHAek'
        b'TtXxBVSVDx2PlVpr8qXiBzaV+UCT7xrqIbTBaPbzxQ9BlbEC7WUZHjrMzsaX69SAY56A97rG5pKKO1jE9X1Zfl78PE7j1lqdc24uulZaD4N+ThjaOS9+AY/ZXOq6Gd+o'
        b'UM8nWa2pINIvVVPJm2tQwDVskdxHFxfkFhbToibMFTfi+3Nz84vkcfFyqt8LY82kzkknZ3xw3jh0Cb2L79EusD+NT1mZtjkNTu+XxxC2Uw0cA+plnAoS4knPvMvpvohx'
        b'Dw81u6FOro+cR92lJcXSInSoOC8ub/5Co16xmVKxWyLhWfA1tJO07DF8cFkIuo560cXcUPRubmgyuilg8G28yx2dRMfRMdrM6KCkhsyZd1ztxfi2K77TsEHNMnZRnip+'
        b'sRc+S6f7VQUVJeiYF8xWfDLBdTNkwj/jQbVGdyThqwXS+GXFsGFVKCdURVvKVXxmeYgYvRJRx6mgvjt9Rwk6VEqGYxs+NJ8MDWEMi05ti6Vrx4watNOx0aUc32PJZ14j'
        b'U0fmam69OY53JuLWQvJ4CllXFpGqvYQvqkHziczdnRMLyNi4O6we67iEh28syaDz8yJ0NpR04pYac/031ONCP0jG5Y140CJDuxUiqkXmOYe2BL6OXyGt1YruoHbQyRIy'
        b'giAWXcDd0+lHPdFpcUEaWSDpB6XomoBxcuN7kW56mzoP8CRT9RXSs6V0hywOn3bLQ4c47S4hWZZ2Cqsc8Os0p0B0K5PO1PiOiiNejDt4pFAP3bku0Yl6JbHoddRpUlNy'
        b'Ws13XUtKDwXYVobuFzSgW6Q7EBIFLDonkdLFczM6gR5swa/h1ng5PkIqTrSc5zV5KY2rx0dhnUcdeQn5RaQjTmLJJLBzPM0wH18JKnAtjqcRpMivo9b5dMSRPnW3DLcq'
        b'HLmomSy6Pp6lqsfbBehybHT8GidKH+mbMHCFTCg6LrRX4HfUYMCdGz+FjPKWYjk+iFpkpoqhtTIzh6sXOdplh9tctnId5TpqRi2xCXl26EyclEw79lN56FI+usExSTdd'
        b'd+A7jstBl/eOHcPDb7DxuH1rdU7BQ1YVQZbIC0urDi0oqBuY5bYiLfE3h0J9PMT2SXlPc58W/iz72tOoa7/asiz0+7kLFGEuuqfuV/d/ri0o/fPvPCR/DJ/GfvNNgr9X'
        b'wSfffPTx5OTPyM2OLTvsnfjHtrdkewb/vGvmY/vFX18dP36O64Rq1PXeB+2Zvz89ff8E3Z2T+W96h6qevPNB2L9VT5SsW3O8IGXXq+X297b/9sxHC7srHny10PlyckXN'
        b'9I9fd+yKWuZd/FnAP7xPep78aKXfb/5tdepPjpxYFtbqq1/xkyjnXQW7fGNEg18Lfnw3+nc/vC6+sN99SoxrcxovqudO3N4/X9SsyvjwwvyaPofkox+2n8yb29LVLF7y'
        b'5bUTOOBpXNTiRRUl7134QaE68JV5MZ8/6Pw46UrJawUxv+xpe+vKx39tuqzcOoiTvjly8T8PvjNjAm/Hbt212WszAlbvbv2Hx4zv/+KjHFlRVct/eIz7tE1Xzp/rPLWx'
        b'nZ92f43qN/tT1//A+44+ZdzWiVf//tn4+48++8HjY0VLP1539dNu/cdb/ivrRvz3XZ58+XTOwpb1daWfLP2vY296/eqX78v+sunun3pi//Md5Ym3/b+V6/d+XPSPH1Vd'
        b'y3v4q92Hbz/enz7j1QvX4+tOB//fbb7LMyZvKI3+lcOvJ/b9BZ/9YEPY2VdnHin5MuD+YEj1tbC+bboF4YPZX375ifJ81Jnr3r/b+N7DX3zNVr15vHKy2++ravtXbJ1y'
        b'bHr7nB3iG/q9/znwVuQP+ZOrr95+bcsvnd9e5zpt3pm1k1cHPJ6dZXcu5Hjjtc/LfIfarhTvv77Vv+mbhv/77ge/+PX0D8N/UfDl1X9T5Rz4+Ec3Pv3gN5f6XX765bLX'
        b'ZDix/ydTHH+1cue9315bO/tI1odTz17J+m+XH076bOETxd/++En7+8L6NX/2Lvv1SY/Xbrk/1Mf0f6gVZo/76Brv3tHGrK8dX3v38dcFXb/+9sDNgB/f/MvhzL94fjkz'
        b'6tz5Bz/9Ud2cmYP//ubg4LeHF38r/7Xz5L6b6oAU/UM7yQ9dP1j16JMdikmHvxr8/NsWr/oHO10On9v7maRpj+zJH1f89Y3vZ92dUvjn332W9tFrv/qle2xRzKKWmDu3'
        b'vhKpHmzwFr176tv8tKw2+YHsRS1HfvrNTcXmP965kb8vv3jzX/S3v9g4z+dv/D8tkGkuxksjDaqnG8l80IpeTwQNVQvt1MPoDU7b9g7hYh8UFMejVg+y3Day6YRHPcBF'
        b'XSET+bswheJX8U1uDnVupDrLSUvRRYNac/z0VWZKzWvRSU7X84qQMMhwQNAZx+msitE9XuN4dJHqtBLJ++7yAnwRP7Ca2WNLqC5ozI4QMqdAtMXMvoS+TNYQCW71XmDQ'
        b'YjWqXBPp6vATKlxcwDczUK8ylhIoZERreUH4nQiqoYqP4buK2JgEfLtGig+Q6ct+MZl7JuLX6Wf9ggirf0URmwArXhyZWNFhXjx+14lGzkmsKVgzw8QOCxjXBfyaKfg6'
        b'1U8lTOMNR9CPxa2r8Fl0pHiYqxYxwQUCfDbRoCOLbubj83j3htgEjgAR6uYlkwY5R2mvI8vDQdyL93Na15zO9Tj/J0nw5pEV+KwKHRJvcMa3VfguajEoQBOO6G2TErSI'
        b'KcL3ROgd1O5IVZTxTnQYX4s1ntU44jPccY17Hh9pHJfQc0x0mZC+t8B4SESEjCvFVP96HN7PRwfX4UuctvMD3OZGUhJeTUaaPB4m+gI7xrWYvwa/hXppz1i7gjSmBz5X'
        b'HEeEqlYa74jf4eE3cU8BLX856gkkjBC+423OBxUhDVU4F6vRnoJo9L3hRQ+/to7TXtawKQbzQCI9njXXx5+5jKvZd5FGjY56GTWYqfoyqeur9EiMdI8LeB9qbUKnbe34'
        b'WCjk4lcyOC3wExWEm7FSA+cz5WJOCXw3bn0Chy34lD06aqmcjA+R1BeG1ZPRWfwW7bw1RPK5FluL30mQ5nOHbELGlQjjdZOCOJ380wtxG/nePnyKdJ4CWg+OtTx8Gl1A'
        b'e+mw3E4YCvJldGLm8HLtkW5Qnd8URCq9o9qMr8muo9+V44eotYAEO60YG79QqkUuXoEvDXM1TgJrpgbsuTid4x58ei4RPDg98NMLqSo4y3jjfQJ3yJ7bWzuBT9RvgG41'
        b'6u7ayL21+fO4QtxGe8m0U5iH3gwjM9I8Nga9im5yo/eyAF0oiIuuxD1kUikA68/rvM34QY00+p+n6PyvDVTg/MFcY2EkzK2VsvWAqxWSHefWxbTrZxVLtxx3iLiN7dJQ'
        b'JiSis+lxsKwvWNZj1+uuC56uD54OCsZB7VuHGIdxS9l+SbimiTsz+zQoWist/KDho6066RJd0FJ90FKtz9LB6EKtZ2R/RPTFQn1ESs+qng09q/QRU9uK+iPjLi7rCetJ'
        b'6gnTR6a0yfslEV0ufZJJWskkEnWl7EKZLnKSPnLSEJ/xmdyfmqstXK5NhV9/5IQeRV9kqjYytXe7du78vrT52rT59Ou5H8zUSRfrgpbog5ZofZYMevh25HTkaLJPFncW'
        b'93nEaj1iDbrbjbrILJ1ftt4vW+uZ3R8Y0lGi8b4YoAtM0AcmPA5M6QtM6anQBabqA1PbHPo9vDtitB4R5NcfLDXUBl8XPFEfPLFnnj54Slsu5w9kytFt7ds0G/ok0VpJ'
        b'NKVnjrZkuU66XBe0Qh+0Quuzol8S2L6ja7w+ZoZWAr9H0T9MQAnauaW6jPn6jPnkCX1Nrp27UD93pU66UhdUrg8q1/qUD3oEtqV2rO4Sdik0TZzjiCHGeVwc9+XJoOtt'
        b'9uUhHhuYxf6BzwvOBpdqJBxieL7ZoEYtm6TzjG2Ta3L6/VO0/ik9tTr/LL1/FpyUr2Tp11fogsr0QWVan7IhPjwEh26JWgnpATrJFL1kyhAj8IrrlyZ2uPSHRXTYddgN'
        b'SmPJdajscWhKX2iKLnSyPnTy49AZfaEzdKFp+tC0Npd+v9Bz8afiT8o6ZW12/X6RHbGa1Tq/BL1fArmlGvcbj05vn64J5zTuaSOZtQ9NsV3nMV7vMb7L3awh5+n8SvR+'
        b'JVrPkkEPCaELdPyHXbNoJhzb3radlilbF5SjD8rR+oBP1Y6tHVu7JvZmaoPTdcHp+uD0Pkm6VpJOExboggr1QYVan8IXVyWXtM8En7DLWc3qK3UX6nTjJ+vHT+ae9HMj'
        b'ReBFLoMjzu04taNrY/fWR4L3nTt26ILl+mA5+YbvOvbTsDht/FLtikr9impdfLUubK0+bK02YC1pARJLWsA3+JzLKRdt1FKdzzK9D8A2UT97cHI9WZOqSe1a08vXhU/X'
        b'h0+nj/qDYzuaunK7inrZRxHvx2qD5dzX2nJJZ/UKbluiEXeF67wS9F6ADAXp4zq2dS0yWBDk9tPetqZLrPNI0nskQZZQgKhz205tO7mjcwfNxje8w0+T26XQ+Sbrfalt'
        b'xnLONmOpzm+Z3m+Z1nPZINcYnamajRebekq1Kfm9y/v9Q8mATOvK6VnxBz7rA7jWELYJSEWSpNO1HlHkx41Tnd8Mvd8MreeMQXB/Gg4tnM1S/6exbZltmYP+QR3JHQ2d'
        b'W7qSyb8GvSxDFztbHzsbbDB8HktT+6SpvVN00ky9NJN8KgDGAoRt1C2jT/sMTVafh1TrIQXwscz+wHDNqpNL27Lbsgf9wzrT9P4y8gWfqA7Xfs+IIb6Hr/sQYwwGwUnu'
        b'kBBuRUxgREfOkB1cixm/0M6AjoAhe7hzYHxDOh07HIcc4c7JGOcMdy7krc7ijuIhV7hzY8Jj9GGTtWGTh8bBvTsTENYxacgDrj2ZwFhtQG6PyyM7rSxXG7Dgg4Uf5H87'
        b'5AVx3oxfWIfPkASufRj/4E5Zh2zIF+78CLfa4TnkD9cB3HUgXAdx18FwHcKExWv8h0LhOoyRxnc76aMztNEZQ+HwJIKjIZJctwmH4sh7et+4x76Jfb6JPZ4630l630lm'
        b'lin9gYnaQBLRs+mRjy4wXx+Y35bd7+Z9wuGYQ0eKJlrnFqvn/EHGTaA2C5pMnZu0382z3emxW3if4V7PuZWUBLQ5mR1nBXPHWefgmIj6MYqFQEYtEyo3mfRuzZz7vIxZ'
        b'wne0LgMDPMK4wZbt01OTC7rRluAYOH/zZC0tHuaGsmwJtUj4/2f4nVlRwKH7Pft0R+Y9R5d0X76UpZ6d5C+gH8g2g48g0b9aP/DzT3g2tHnTqxoqlSEV5TU1FG8XLAwM'
        b'+MOkN1RDNyivsYDh5cCNFAoO3a48pLZy44hMOd326JUr56xvyKutIj1xVU1dxTppggEy2agfrFZVVqlrQEl3c506ZGN5LdWNVVQ3VitG6tBaEFFdSxNWUe/LBsd0lSrO'
        b'Wx2HuBcCYDMh1QrVSA3bEQ9S68uV5etDwGl0akge1dMlI1lVDbDE5Dugs1seUqFWNdSt57I1FS1PsXKlFAAtRlVtJvVjrA+4rK4NaZycMIFURQapxo1QmQ1ryhtM1A5r'
        b'T9vM0VA2ipVMzRs4HWWSASAnW1SR0e/famWdup5inNnMkRS9obpCXVOu5LSwVfWVFSZf2KqQaPB2GkeqgHyWwgtsrie3lQ0VCVLaCKNoYUOFNlQa28XQ7tR6pZbQrCYV'
        b'SfKHXrfZ2PqKOup1sB5Qtm3ladEAI9v0uToaDnLuhHYnehsdhKNt9C6Rvg3H21M43RvqPcK9YaKFj4aySs5LA3XREIFPqAsZcDmGL9YazvtCxHy8c/5mB/zWhkTc7heU'
        b'6xG5YRu+Cfa9b8xG7Usz8hrQdSLX94hnyOMCcSeR9Tsz0dvBW9A1t0R8TUjPYw6pc5k2ZkqycOXK/EvxldxB+8KcqfleuJVI8yXRYDQN3kDA+YodE7ZWgK/XeNBXdzvC'
        b'Caw4h521suYTuyim+m+XbvBUF0jMewedOS3dqa2syDtxwkpWelBa+GGHj8+C5Pcy1/rO61jn82OfAw92vfX5hawvIr/JfWvRTmVc4govfz6eoPnt9c8nTUxqnOC9buPt'
        b'uJXfr/pqQsgK568qb723/AP5IrVE++9hU8fvk1+WZ5dOK1l0572EmC9k4zKVUv/LHzr4lOwM9fhpNc/e4z8UN1Z+9MUr/7Hy5heVK3OrDuQ0JwqoJmbu8bC0JXFSR7od'
        b'440PBKMTpG1arXcA5457AstVbOb2Tcuphijd+ztqT+X3XHwOtVHHAK8UvbD8LnShOxgTHNBRFZyPxkdzCSY48ZlxuI2Peuo30J20ab74FaNDGCEjXpsNW4P4jRhOxr83'
        b'H+0Cm/1U/KAwiTXY7F/Ct7nNgT2oU4heCTaY7YPJvhj10K2zRZLG2PhodB6dNW2c4bP4HW4j9AZ64GLcsDRsV7qSetkvEOPzc+leT3wxvjNyqwc2ejzw1Y3oGt75BHQU'
        b'0cEpJIn5Xg+6LZNZWKLvQvefqwI7LL3bgxcnOpyttEpNz6nE/hHDSewrIkeR2PuH7V2JAKSXxACqbDH7ZVAUWZ+ls9j+jOz3YwmPLAVv3mxwMXDKwdQE0reYHfQPhuRT'
        b'CK8bEgHGxiebOpuoIXVKX3CKLniyPnhyh4BKYOy4SR2zO2ZrBCfzOvO6eKfkHXLCyWvKdH4per8UrWdKf3iUZnrXRM7s1c1T6xYO3OAGHTgDD7d0v2yhj53wLMZupD62'
        b'A3+EHq6pxl631MCeHcmyPsClPCf4bjWw2QE7sgyXkXXYtu9cyrqwJn9xnLc4vslbnPCf7i1uNWFdvhXYYF1KKmsN2KF04TIZRqpVHCtTSRcTsvJlZeTNLjHhuSQ4jLb+'
        b'V66qrlCVVdRUk1xSqc2RERSmCmAIK9Yk0BQJWRDOpslWmmU7Sq6G2k2lRlNxJqspgAZWVVIy65QKeEBWVpsrX2qVurbiGTQkZM8vXElBt9T1NXXlCmPpjRViM1OA4jSB'
        b'aMGibLCTVKmrG8Agyowo2+vxc6maPbt0ZdxYX50/5lfz5oz11fRFS8b81czMsb+aMdZXF2VNGPuryStDRuFaX+DliaPYreVVUSbOwENWKuJCYgzdP8bC+M3SOo9apdhm'
        b'+kazuctWllOU7eE+/DLmdQtBTOBmhcbkhESL0ULNAjnsVm44kQ82VpePraYySufbICGVA5hRcXMMRwc33KoVz+FsbalteskpG9gYL2J67INAFa/m421xnNe9BHwUv61y'
        b'BAVGDTqxjUEn0e0VlBGuR8dxN76TmJg4DfUKGV4eQ9iQ86iTvoYe4tPrYuUJLEO45D089BpbsKCRamd4TJbHyvN5DNqDW3joFXYKbnOmSoNzkUYcK89jmfhwHmpmp7MJ'
        b'UgGnRLknnyQG9R58uzFHyPD92BnovJASEYz3oQMkrqcBvzmVrJ08/Cob6ox66KfSUG+UaoKSx+BmdIatY9Cbilk0x2mLfFX4vqsS9ZJ8yDuX2Rj0LrpMPd+tAL+b4CVc'
        b'1jCTkRVl0xdYfBf3GlUv0XF0hPBH+IizlEeJwJcy8VUDgbiF4Sici25wWiDH8feWGijEJ8MMJKLe6QY9lg70CqUF9xQaSMHX4qjGUDTqRPcp/ej4Bko+asftUj79Zog/'
        b'vmb4JHoHH+a+mYU0VCOnBp9EZwzfJBzdCeNHD6Je2jrZRPrY7dhor0IP5wkYvj0rK0G71dAt3NBDO0dnpesKP4bhx7Fp6EAc1wbHy3A7yfGuo0tqPcvwnUjUMdyqLoDi'
        b'n1sHx+ctpKSn8ZESavgHynBE2GDwBXSsicgxBwlD+wC1o85SctOOH+CL+BgRZNrRA3ch+BfrcVqEbqNrXN+5uh51lOA2crkWdeHzTN48dJMWOjldio+DdeHBEkIeamHR'
        b'wbR0dEtQ/ZvX+vkqH5ZhLhXeAmuu88dTiMBy26e823Of5w8WjM/rLYyfHbWUv9R5tkPJJI/mz77/ix8tKO370bHvC6785vF7nT9xutA6oWTRzraUvfF7t7l8yKsSxTFr'
        b'ohwPPnRa89Xa3of3DqYczKqVBjgu2vB1xe5b63x+1qF9MkF9O2HlDy/X+brdzP527/eOV7J2k9QphSkffbhz5hLn/zM/EQt+MF29593Wjp1Nm0POefz4SM5/Fzgs9J19'
        b'NFrbIP/mRo66LjF/ysX62UWC334VNjvN9dj22i+efPX7jKRdkq+3zNaIXQsFNd6yo7Xlix/l7Lv+l7ZlPynet317xN94iq9zXNTpE56E73/LbcPTAv2421LeB9VbJlUc'
        b'CLn921nvzHFu6/xw39psj/DVjoxq6iqce1DqyTmW3YPu4y6TZ04Wv17B6SPUzaWyxcJJ3pyXNS/0llEdYSJq5969iFsUscN2leh4LuMUx7dbg16hftBQiz1VsGDBHyEI'
        b'WUTCoWLQYnS3gfqwbETXhYwA7WHxbnwcnaWRqQn4ntFDWvFWg4+0FLSXalegBzPw60SCOoFOmqQokKHGqWl0JNqPe2PznULxoQIQS8S4lYd2EVF5JydDvZOQo3IERTw1'
        b'7mJxK4O7lqD7XFSbZCpqrU/h0bN+Fu8nT7xV9GTeAbf6QxSR9m6GsNCFj+5YzHkvO4TPLoUolsE96BpLhjrpxG9kUMlrIT6O75n5HKMOx9LRGX4mOoV6qX+7cHQ5QNXo'
        b'wjIFWSy6zODTnmXcef55dBdfVpHR2cxjFkHGbQyZb244cFoexybjN8hrQmYibmXRFXDhdsuoAXIjCXWS2cOJYaag0yy6Ac5RX11A4/ApdDRC1biBEPsGjJQOBh9Eh8ZR'
        b'ShYyQhLDYzY3seg1Bh+YiHup4sN6dIuxEGkNAi0RBFEPX0okmBfYQAYJBpadYRNYFeGzt4yzNCUkj6i8F83j5L3a8VTe0wcn9rj3hPa464Mngqzn15bWHxzb1dAXnNyW'
        b'M+jhN8QEjJvQQZIl9zT2Bc/QBs/oj4zpyeqPkPakDPHZwFQi4ASmfpY6463wXsWD6u8lPEgY4jNefoOSABD8iHgYPv7KlAtTukq7l/ZGauNm6cLT9eHpHeL+4PBzW09t'
        b'Pbmtc1uHgHzSIHiKeyN0wWn64DStT9of7CCDITHjHaYp7fOSar2kn3j69HuFGu8A5HCzNmKiVgK/4UwEuuAUfXCK1iel3zew01dT1ecbp/WNGz1BZZ9vrNY31lYCUhq/'
        b'uEEv3/bF2rBUrRf8DFCMfK9Jtl4YtPUVeF8zvs8rWusV3e8f9dg/ts8/titT55+k90/SeiZ9Vwki+7yitF5RthJ86R3cVt2fPPnutB7y75HgfftH5F9/cloPIL+FplvA'
        b'pIETrgzWTJYWcZ6enMwlLqUjf6SxkIgxepjmxOlwEKdH9sX3QJJWMibv0juIKC0FYXn04DuVoo2We8CHKW+BpxOJFQLEgKCsOE8+4Fg2e/68eVny2XlZJRwiogkZYsCx'
        b'vry61uBcSXkBjpUchp0KccdOJl9YyvMQUN9XH1giSFBACTjcoVsPtMKkfv8LFEZgxn+OioiyFM6kLJzrvw5etzZZQSC6MP5BmpIefm/yowqtRz75ceiCAZqUHmHv/A8i'
        b'+739R1wO2Qn8XYYYEjQXDDnxnWMBbc124DDTuYL02f9BOItnwK+Dc8Q/8Fn/WPAhF9tcMOgVOIxaNxNQ62ZR1LpZFLVuFodaB2ep/W7xWrf4fs8MksYvE9L4gSM6CJvz'
        b'raAUJwIw4SQYcJNgvE2iqITm8HhZ8KEc+qEc+qEcdgTuIMD1eVG4Pi86bElI0e/McfgAFNAfQAH9ARTQfyrF4TPH2ANgQh8AJvQBYEKftObcIbGr88Qh5plBCOMb2iHW'
        b'+sjITzNVM/X8tIvTuLvmPAAbsY0uYgtixAxshHWGxWRkIGbS2dnsEH8j6xw4xPyvDJV8xsWreWFHuNY5SOccpHcOGuL5A27Ls4I/kJeCTUlTuRxKtc5hOucwvXPYEG+a'
        b'M0zEtkN4OdxmKg5lBbgLtwX4jKOlmhx+JZxl/HIE1fiap4WY6mT4+6cmMiW96gl2u8PgKkv4AKzCgap0CgywKtw1gKvYk39wDSArALHCPR++dlOMU7grPOi1p8LLdO2t'
        b'kJBrH3rtq/BT+CsCOh2XCCqFzaIqVhG4x8qcEiBZ2u3aWYVju1O7uN0d/nUHXSYT+XUT3pY9+aeIMxzX8hXhIyBB7HhMpVARsYdRRHaPt4JFEXP5tzu286p4JHcP8r9b'
        b'u3s1d+dOvurebt/uUCVQRHVH2/huPIDKwJeb7Zudm92bPavEipgRFNhToBQRxSQYVyVSxO4RAxTjJnYJB7mYMOAO8+lsZaWiuoHCBFVVKp9OsNhlGJkghO57WiR6mqBW'
        b'1qZWq+pSVQ0K+ndCYuKECamw85G6SaVIhdUrITExifyfnJCYLOUPCOTF84oGBLl5ObkDgvnzcuZcZQd4mVkktIdPlhXLCxdfFShB+hgQ0p3GAXu636OsJpfCqpry1aqX'
        b'+WwSfFagjId1LwECGR8W3jx5CYcv95J5TZUKrfJSTqUZlmQuSH+asaahoT5VJtu4cWOCqnpTPOwBKcG/XHyFwY9VQkXdepmiUvb/sfcecFEe+eP/NurSe2dB2gJLBykW'
        b'eu/VSq82lAUVu1gpKioKIigi6tIEK4gFMpOcmnjJLnkSiYmJyV1iyl0CiXcxpv1m5tmlKKR8L3f/7+/3P93X7PKUeaZ85vPMfGbm/XkuhU45hU4ubk7oeXzWRPztLOK/'
        b'pWQFAcw9UIqOCwqIzgiMCHpmgxMdFBhBUoi+47PK8ZsxEc/ICktRpE4uHihEvQ8cWTuzZBHt088dp1UlKSI2LDokIzAgOSj8N0blymfT6RrP8rPZz90YVFIsFAYSm9XU'
        b'OKKLC2KEBSQmVxwTayImlMAAHJf6c+XxzGjmTD3Tnbbw+NwpsWBxKwmeJm6fklB89LlIfEgk7iUh+NzMD3d95vA7cvpAITcvP6tsRSkpflKX/9tJBtNjKuhZ8gGwG4hg'
        b'SxIXD3jpjXCgFV4vurHkdQZBWLRv4WLMAQFYXJJj2NqrvccSzuubAWHxQDGjpLisFDUK2p/kVG3jJDs5hWaxgc8wMK0t+508gTi2zGflDM+YKzeZKrCO/5+gCrQr0N33'
        b'lmn68K3jHXncUj7DGLXk2CkEAmVZPR1lyFYRTUMgYBLeAHZQQ1zT5CuP0wVU/u10gXw+68MKhWmm6CJoZl/RhrxJE3U5pGLoxSr4XfMLE3NJZatXF5dgmz9uwlJuq9D3'
        b'xQsFvOf0Ac8uOIT/y5dhffKrV/jw7OyFRXjly9rZTl72vyFKWkXx7ILCf/1iqSrCFzvyfu05M6tJnl1E8u+6w/UX7vitGg9H8XyiZ5oDlc7j0BMeNE4xNy+7tLhEdmbG'
        b'2VPcLaBve15sVpcUFZcUlZbTXk3t7HFnwx4lCHc37KefFrPHnRB8De4S2OM5UHv8LrfnO00szvJycnNy8ZVeMn00E+u4XMil0lgnDnuRw3TUM2WMht1KszYNsJYuH1sh'
        b'YdbOWDxkHYHvVB4naWTT42WlPM0Z0zRBj6UTRrfX5zGwGLk6vpRvmpV6+B86V4bn3vG0NJkOJMsI87JKsUChTJU/T+XFC9lmgHriKUUUz7qsEumqQ3yrlDpKSoeXlJeH'
        b'81q2Io+XVYq6j9llpdMnKyggOSQsLnFhRnxKYnxcUkhGUFxwSBJJ5fiKPwIYnWbZoLSQaCVEl098QESsjCYtqzeZXUo6GTr9ArmJCVIy6U7HMDF/af+cTrGfcYkhqaHV'
        b'dDsVkkJ87l4fezp3skuKVk1PHKV5uqjjTc+p4kWFq3ghKYkzTPSu4iWtKyrdkFeyglRc6S8knlaIM7Ql1GAiSrNWlJMbZ9Zw9jPLrBQETFfIBB8YS760SsZZwfSaixly'
        b'VEqvmJzk9njKvVM40jNqLRLTC5PgqHikvUOhTHyfi3f6OiFjocktJSIwIJaXnbeieFUBjulXJouVpungadAdPHglEJyCh6NALd4AWstmsOBppp3cRnqj/T41iwn4T6AO'
        b'Sw1UrKAXSOK+Vxg8EUlcuRE3bjdgJez2AjdoT2t1VnAbdy08D2+prgY1sA/9v4Tdt6jCnSxYHa1Zhlf7uUUpRDlBkWAc2cJgaMFWNqjxBVfKPHBPbyO8kfQCKkPq9gye'
        b'A/XjzrnItE6fstLKAClKEoi2luGJzlLYylWjZzqT4XnaP9YZcA7s5Kqu5ZWo09OjCzII1QJe14GHJvm7m2DJ0HgLsAPsC49MWa2qmohd3tkJYlPs7GAVrHGGVY7YUxnt'
        b'TE8gj0qkXpvpkx5aJp1wOg0raI9rxN/aNht4IAdWkNn6b3XlGSq87fIMXqbjp+wERtlcBp5OvjrVE1s49udTiXLtnAj3RieEsxNBJUbfwGvgTLk1Awwqwl4OFzbAHtBZ'
        b'lH3rIlP4AEVj+PUXK+NvKgMXjVsvXy46lBofL348prqJUQ8D+q6Waizl7BGqWesraDYNPD2UzlXa56Fx5+Pv7377cdbJeK5itdU7qaxNZwa/UxEz4w6ertGKvFu7ytPh'
        b'8m1O7VzOjw9beG8OnbnezEnz/KRKy3bsC/2XOqwefT7iV2cc/Xrr9pKl+uwy37/e4ixzcx5LFcx+ulsvLUDN/e3XZ3VbrItk/nStQHS28O6Xgde3vPrDy08r7t2uubrm'
        b'wmK+5tUfhArGBtu+izlfUfGN39ZPdkZ98smW8/kJ7380v+jxw5WXfmbukfdKaBbwVcn83zxwCpx3cBLQKyjbwC0TlotpLMG+OoEuptS3Zg2sxxPZjngxqAJDLZHtCk+A'
        b'dnpj90XQD3Y5xLqClikzk6DFgJxXAxdAH1mMmu84ZTmqqQWZgVME+6xlq1EtwcUAV9Ah9fwJBwqjsLeew2D75A3Yy+id7urgrCY3yhXsnbLEk6zvvAZ2k6Ww+eCItnQi'
        b'EhzJGp+LZAfLwWMkh8Zry6c4UtroKXWlRLtRYmuTJ2nBC1scnOAxcBb7vprs9wocAdvpJaztORjeFV0ABidtX88HVWQC0nMpPISe0zdvMWrDl9HZGGYo3Mcjk6zwOjgD'
        b'OqPg/mhUAtlMIexwjV3DV/mX5gewyXDyhpVJDjmmHc5N9tMTx6TRdLkODE09sZ6dyEqi4UxpON/X8B7W8O7XH7K6Iy+OTxnxCR7Kv1M4xmZqLsDrSlE4SofyDCOzJuNa'
        b'+RFD8xYvsSG/Vm7EfNa0G0619Sft1tK3bFkh1ndDn4dmdg3LRrzn3FDtR/+H1g6tHWUz7ePIGtZ4soY1nqxhjWc+0jcWmzuL9fEHb5BkMO3JqleUKvswcn04uT6cXB/O'
        b'fGTMG2WwdN1G7AQNnCbVEUfXBg5lwH+kbYA3oYUzG0LvmwiGTQSiPImJB2XiQR99pGNQGzyia1K3pMWyxbXFktK1Ful0GYp13dCnf/YNP/T1nHOiUTZDz52+AH0mDbtV'
        b'J+17+uUR7IzLYlUZz+1K+o21G4MH6yLG1C1Iafb/e52rEE8ep5V8GNfUAhR+j3MV2i3HA7kMPJqZyU/CdEUl85awDxVVyTl8KfGW4PQbhkzPuz3BJtuk8IDEB5zgkMDk'
        b'B5ygxJBgvsJ0G95Kvpd5sX+gkFOYVVKQJywpYD9HTlSXZbgFBUcUZyQnYm6iwl61vfLEgqFOCIkaezXz1f+zfMQPRdNZMAJyc1G3evLOGlkPbhqr+Xjf/0VDSD7PF49M'
        b'fDPHKcyZ06yIdJT2pMcdJ+CtPS/uhEJPn5ygHNRTz0YjouKy0onxUSmulVLp6PE3jculIypaaH7D0Dxr5cS9k5NDH+dlCXn5K4qzsM0Nja2K0JFVZSuz86YfxuDHrRq3'
        b'BOFOsWzpdQCJbbpVlHQqpoxXJydDNlotzVtPD8ZwqdDOI1bS25Jm2GeErinKxSOJiaIoySMbzVDK6Dzw7FBCS0jWyEjBMjHUycnJkj/DGIdeVEr2zGVhaRKWlpTllJah'
        b'2CdiduKFytZkTzo/bXzj9xDJLFu9Ik8mAtIF72hQhTOLxn0rUVFOG4ddYkhoCF6IEJIRmxITGJLoyJMNiZNDFiTzZyzvPLJJDhd23qpcQWmxAH1NKh+74tX0psFfiGH9'
        b'dFYGdDSvBG82nGxl+MXo8L9xIwQu4V+yEYw785BK9bSxFRavyEUqdVpzAg+VSkhibED0i6aD6ffV/UZzQm5ZXgbeY0cXBfqLh/8iAiuVG9wuSvMKkFwgAcnMjC1ehTXF'
        b'L2w4XF868XQcGY4FjR7xJj+sIMZFN7+keCUqqtysGXYGriijrbYFRWvzVskkHzXNXLw42i6neJWwCBUXjgkVXBE5ikp5xoTR0Uy2dfEnZ5NOanH2srycUlofTD+6Torz'
        b'9nJxJcKNKofkB6fBUeoeS5pfYnzCbRMpxWnjyS8rIW2NtHay2XFmEwP9hvPlJUmH9ELeusKinEKyd7IcPWXFCtT4skrogT198fS6RSgszikilTBuYFhdUowaMtmygopW'
        b'WtmoIdBiP31hTmg5J15sMVK1q1evKMoh2zawrYe0p8l7QadvO0G0zsiSKkX0dPzy59mhkO/Iw10Anl1cSiIfVwbuCvDsAkNiZ2iH9pM2t3rx7X/DltvxNfAB46oepzt5'
        b'Itm/tLfmV+0c5jTbd3FGHhq98cHxcZIxPLuJdGvJKPzBagLxzRRZZqq8aiak18wvN4F12L4BGkEvbePojgsNpZek+8EO6TrybnVM8a2xVCb3pCXYSqm/4BLogacZ4Gie'
        b'YzLZTxoHKsB1vHBikj2kyF9qEYHHXMgi7MUbPGG11PG5Iro2WcqwjBLYp4Y7Rqa8aAaZ7J98GdjHAD0hmmjgeyOaXvB9AJ4GvfSKb6ZuErGDrAf1ZWk46SIDhd/5MMJS'
        b'dYpAQYLdONkUjabP8+UZvi46sNcX9NPmlyZ4AFzBS9AZMdnExoJy3FO2AT+21kAB1QU4CE44J9oJIuOwrYWOTQ4egruUrQ1Bu/KEfcMfbodN6ESrFtgF2pJBS24CqAzc'
        b'gmqlAnSi/6fR9+7l60EtOBuYnQ6qAkuKEhKWpZdYLwHHlhdqMOD+uSYoOT1gG52yHhclLry6WoXlBtoZLHiD6Qw7Msuwzw4huAAvRxEi9TTJgpWGoNIfHMwGu6akZxds'
        b'TYE9sA7/iRfJZ6rDPTwG6ErQNIhQpBmRB1lgAK/T56BEXiUL9cExcKksF5+7vglWj9uc+KlSuvPqsrJkWLtaVR0eSpaW/SRzFLZA4QoipjHYAG8mSFHIznExYDsQKeJn'
        b'MdTgXj3YDeoX0Qjl1kzY+SKGGxVe8yTGNL4zeaJqUbXCK2CPahgY0CNAZ2tPg6hY9Kxq9L9Tm+wR2Ae64on0oHijCJ0WidRhOWEkqNJCQl4FDycieaxiwsE1qmFwIJzI'
        b'OWh3ZcsiGo8lfMIhdOqUyMAuLqjTsYZndcE5cEZPl61WxgDHYjDH9mhcGfZDFI+E5JpwKjTbA5zHeWLBU7AOPenyHFRBFXAnKl+yYwEcymbAPYkqiaBboywWxREAW0Dd'
        b'JPNfdAQ/UuCUCve+ACyXpUs1PmVqs0HF1VymBQ7qAFFZKooyKg6ekNFGUYS/KWrQGC6N/fm4EyN1ULJvahNNkwVb8olNMUKLtioeCIeXyMJTYoGdbwK2OWCpqEHF16Li'
        b'7uICdmZGMSzBFTa4hYllfFZsctGRsNlywnfR8PLHt/btSr4eC110yprWHfbYbCUQ7GXKZwZ+lDZwQceC25aqnLjIl1fAqHzpb3s9k47+ZNUX89HLle8uqqr73vfx02cP'
        b'Bn8yB3tVG17rUpl1eZdzRue8p4JRherhXS/XnFwaze+u+/6LajtOdYpShf2Vy3pGbwQH//gn7fRjdvd8tF7Z1mr++Gyk/OdXl2S1uvU94EpEzypmR3ZpzZW01tq/vODL'
        b'NdnHs7P1fra/wFsWv+uj9w4X3otQNcyQ/+Do4mLTg92itytjJPKvaHf0/Gn54Nvtan+7Y9+tnqnx1la+Rl/51aRPr8uZZAytWVz2k33mw8vCRd8cMNfc/orDglWLHB/q'
        b'VYf98PFPS3JcL92/V2PG2b/lFYnI5LJ3066kRapzgyL6Ogq3vG13Yvt9wc2T65J73t317LVnVv7vOfzF9eyiHZ61vSVzWgdPr4+84rv7clCWttzAjypL4r5vf83B7MDf'
        b'Nlt9llTf6fXS1+rJ+62fdV5fmNVf8bPGg2OcfXGlD4IOhdhkx3S5ObtaRp+d85fKC7fOf23QtPPp/ja2oZnw0StGF82+cD9pdExJN98wKvqTBOG8v14791bzbOohrPEd'
        b'Ni6R68m7E1rEg5rFx/YqVYFGy3n8v7I+eeu9mDfe63zlYaiJzfovUxe45w7+xDafd/Zj9kq+Htn2sAF0MaMmcJBRRsQeGaJLtmDMCyqasuUeXllCzJwsLWLm9IINJtjM'
        b'yYU3yb77criP2CjzkBqbMJgzGeAU3E72oUSCW8R4GLEE7KR3orCd4BGpZdHcn9gvkUa+AOpA9To1VeUSeEWINP4+eLVUVZ6hs4adZA+PEvtlANgG9mLjrXQ7BmpPx6UA'
        b'zWOgixhb121cTO+Vtwenp9hSLfkk57AzQ8lBCTbHTjHxlmvSltrTYC8470D7sh+ER2UbWzrALnpXRy96UfU4wEoOqIqLAF0chvwKlmUYqCUFE6IOBzBxVH6dF+GNzoHN'
        b'pGBgFcdw8i6SMlfadgu3wRYawHkZVjhNMd/SxlsOOCu13+ZICYwoUY1RUZMoiEhL9WMSYgadu2DYCvrQeUfQzglCnRSOIxMMgF3p5ObCABf0una0X+Y51fQ7CFuJAR3s'
        b'EeAXuttGmQmd5QL3uBPCIrgMG7Iw1rDyOYACu5DPcAH98s5yljQCEpUauELEB72T4gTyUbCToRbMngsrQQ+9v6Ub7DN0EMihV+oEIuFIJr2F5wCo8gfVzrMdYwR8lIS5'
        b'LB5sUOXr/3+xNB2nVdaxnJmVZDmN8W06aOFjqdP4fAHtNN5GZCPRd6X0XbGt2W/EdFZDakuoKLgrRor1C300g6mZZ9WmQvFcpWRCnmet6oiF3SQ/5rVqj6zsKCuP+1be'
        b'w1be/aYSqzDKKkysYTGibVg3X+QpdgsS2weLtfHnkaVtbVRt1IiuZUvusK69WNdetGVIZ9g5ROwc8sjSBp8blWdYufbGDs8KRNcZWZx0bnSWGDlQRg5io/Be+cvqQ57D'
        b'LuG1CqO8KQ7QaffnKGs2Xtj8zR1jM22Cid90wlNDIQb6hTBp0JlPi/ywto1Y22bE2HKUrDGXmsADiOU7kFi+A4nlO5D5yHgWvtdlZJbtOd9W31Nz2uY0KD59NHXrCokm'
        b'TRZNKokmjUSTRqJJYz7SN0OXT6AQJ4iQGOjIx0vljSbFqG+GYwyVxRhCYiTANgIvZBqGMjGVzQ8nLZHmFMZLzBIoswSxQQI9PZAidpwrtpon1sYfvELepG6zWN+lNw3j'
        b'9oY9Y8SeMY94gl6dYZ6nmOfZb0X5RqFvcfxiFBL+XorEMpWyTBWbpD7Cm4NEcmJ9Afr0OgzpUAGJw26JYrdE8uRJhEmcbkXNIGbLRvq7d/MdteHZqeLZqSOy5MbSyY2W'
        b'mMVQZjFig5gRk1lNcTi76HKFyyr0L2nGA0nGg0jGg0jGg5iPTHhN0ZSJi/SW5MtLKM/QX71rVBlXvd99bf6wNl9kLdF2obRdMMnPcsTcBgP8Hplb1IZ/rGskNhaISiW6'
        b'HpSux33d4GHd4KG0O/ni1KXijJyRkHhx4iLxklwkX3r5OHoU1rJQ4aIoWHVcXPDSJ4jt/STacyjtOXjXkStqMqNs/O3o0hXRrzfsOF/sOH/E3LJB2OIhkyqJuQtl7lIb'
        b'WBdO6H5WIhWxtgf6jNi51wZTOtYjpFajxdou6DNi5VAbXBfzSN+wVmnSJInWjHC4CVt5ybIXdzj9Fv2EJwxeZLr9PtVUi2dS/sSYOpOy1JHJTCQzIP+p8A+dZxEpzWPc'
        b'UgtQmTrPIi+zBmxDwRF5stKWXiOvsFdxLyNffnzN7fPskn/LmttnmS8YLxLzVuXmlQh/bRaBmCylZhJsJMsS8hbERP+KLcSM8aItxCGWjJUW45UaUXj3hnEovX8DexOZ'
        b'4jClOs3uBWoSbALdqrpc+zKC4L4B6mCzbIDhjoYrDVNGGK60t4z4dRvG1z1YgD3obQ8HwGAZ7l+gIdjB1fhkqRPqsTmtRUFkhAC0gFsshlW63Gx4C1aQgU40PAiPomdg'
        b'j0ZmG8BuBqhNmE32x9ujkR0aJ0XhlSvgBDwpXb0CrsA9xKrTaM7eIsfCvzJVKjcsZZDBeNkWsNcdO0iKZGIgwAnM4e6ElYRdoL8UP4n4NQLXljuDm2zaiFIBtsF2rlIJ'
        b'djnSDhtAHwN226rQRiLQFunAt4/RyZJjcMqZcDs4DftI3hNALayNwh3TWDmGvLKcHktlHsoSjrAQXAQnk+A+bCa6UgLrGeAAHpsS0ADqEO2GTUnYw8karXEfJxfgAL0k'
        b'Zw8cBOewXWWZgnRrf7cTcc+hhMa1DTJAwQHQJIUFGMIDUkJBG+qo0aQB3RgpfeH4atr3yM40NWyYgscXcBjokfbrQSt5mmVmBG06godM6DU0AnCCLN0xFSgmgX2wLgX1'
        b'2Y/Auq3Yf4piHBNe1oRVpOyNow947Gd6sxgumateT55Pm9neTprlks7YiyvEMsQilT5owg23G2HxmEi12a9QWD11ubyCTIwxbO0Is55RwNjEWGq+mVnJamFM928TM5eR'
        b'y9zFMhw/chbF1zke50FWDS+JQXw1foad9LQzHygE5JZEF63K47NLcNYecFagP2iNi0lI40vKcZPaIJhGxZaQdjzhVXfOiiJhaU7xytXzlqLW942AQTqCYud8+nNHp5fZ'
        b'p3RRqd+qXzjE6hfe4EtcgimX4PELyOuElM0xdRWtJJYLakiZ0arWi+iD2Sp6brqMBRjwMafKx4belbUStirCS2yr57znYN858BpsIdWpJccgli9wxoMltXwdN6aNYs1I'
        b'TNC5NapgVyybwdZh+sGbRuRpnnrySypZBvhpKq9GF2BXvdpEZmCXP5ZDrdm0HKoE04urer3gLmzrMnKgkRSl8DJ5+GwWPA4voTsynRQYbBskffWgQ+pDaTFo8BHG4jUy'
        b'LC5s4DF5sALW/kfkoADJQUklfh1X4a0ptASU1LBlr9x/VQC6JwuAexH9uZPcG9AXcTGiP3fIfShwyP1GkcQjnPIIH7+A3myHm603uAV7uWvhVXXQD6+ycIl6e4CLpAoW'
        b'gi4VLtJJSD/4w0YGOLZiJb3erMMY3oCXVOBVBaQ+Dq/CbuC6YMdmut6ugRPOeGtFAgNcgpUJ4FwUTevYp2TCtbN3gBeiUUuOdCllLSqVJ4rFCTZvhJecI2EfOiOHhKkH'
        b'7GDCo0Vge5H87XsM4c8czO1TvblgYfG7oRrpiVr8BAXrjKrs22FqfkXNbT4bzoQNvx3zlftN42/f+5OqakOFztNTC27p8Bfplt+JEqcx5Tg6n0dt/+H4Tzt/qtyvI3xl'
        b'6Z9r6x4mb/vww79t+mD29b++rlb+xrNr/zR2X1hwNekrw5p/fPjVSz1/f/+QV8578WFbPXzL4tLLYnb/0N+ezTrKOixxKSq9aPQnnd2DLY/c7JzOfbQpqcFaL7df95Uv'
        b'L/K49xcapmgs3KpxkDt32901fr2ZuufWp7/2ivxXHsGLT4WZ/nzFpuZt35epuk0rPT6oqPp4bdD+oo7yg+rKfgV+V1aZ5bC2Mr/59lGPOTRMUVFufiZ//YsV5+X2rx6I'
        b'dcuI1zlq91O8/GsDKeYhzAGPNV7WWdXDta/p7Vp1rCFv1+j1hgzvdN00drBq0OoCx1XKKV0b3zz10K38QtHooSqd0MrvyobeaPHNWzA76o3I7PyEaLm3C0wOL/djnRi5'
        b'arq54set2/LUcgyXdQV13ch476HZlzZb5Vz27H1nf2vnu5+839Xp8sWDBV4h+zYa/D2D86V80JZH85tEn0XG6HucS475+/6QNW9u/Hx5i9v8St+T+980OP+hXPwixbm9'
        b'rVe+PKj02FayZtFcUdLmhZ3bVmrmaHetrIr+wqPG+dRf9veZPHio61jxxst5khUmdUw3v6pTQ1tV/nH/5l9O/b2Z533atfPUxz+rNi03OJf5U7mcMDE7lSm0d1U3fMPw'
        b'5I932zr+0fD6rKrXT1f6upmVfpJdJr/pi8pN52ZtKmtU73/dquRu2dtCQ+p8xrLZKls+XZse0KTarfojZ9uGt+o9OxU2XnH+nnnnY1eP+kXfmnw4/2TD93Jz1uWum73t'
        b'K8uXvvV+qfXxz5yDjw83mA/sjnL5p8728sY7cseMi0fhk7lv/7Ns8Yf9Oou6HSquHPX/9ljw0kpJgz7zx79tkfjtqPrRpMrmy/knD3S3rvnW777Zk/qCbd/t2Vtu+cHY'
        b'4TtGqUu0Y9t2nZ1VMvpz+JsVRuXH4h1BiqY591Ww/ZZDX7m7SOXZ2oSx848ObloTd9Ng3zW1W0OqHX5Oe36WaJ653lnl9k7KTf+nGVY/OGdtiX9/6Bv5l1/jfLSsEF6b'
        b'Nz/14VGLj46Mbui3zbBen1t39UvxO08+vs5yeV/fZ+Th1vaHt35WeEswt2veZ/4PxcNOy99JUB91tn0S/HPYudbzVz7MSCl1Prz8h96vJWk/eAZ+XHZP/Q3K+NTfb1Zu'
        b'+Nhn9HHVou//8WzY46/HKlINMjdXD6Xe6AvauP7x+xafbPtnfELpCrmu9V+9uvBu1d+KmV9t3Gm2ZffcTwPvCtn3IzauaguwncP8SvvSqdTitrDSlsjoV9WSX2r71H/s'
        b'6V/RjzP4x4/rWpQ/YPrFb2q+q/bk07/fqBgpVtig+lresFryXasUBaNvajZrLPrJR/x97Z1Z35UfnaP0qnnEzYB/fNcgDvqiVKe513l+wNiqL+bVbI4s3BL6dL7tD/dt'
        b'7zabVy/Vr3+6qnzJ9z95s384XvjXyp3r9ji71K3+S3yrL/W9VkjqX2r/zPyyM9n7Hx2cNOtN97bt/+fr/1z6+HV+wqdb9q0RGicPvhQ69LPg856NJmnsl9cZsJ59dqy/'
        b'Z7/rB4+7xopXumZ8ssLjmbzr9Z8/qb796T7191VaPXVbrwZurP9u7sFdrz71S+n7562U4hAx3yNUL+NI85dGpa22tpuFO2Z/cKj1u82FntVVP+cXfvbVFz+57T/wztZj'
        b'/T9q3P9zUY7r4z2uC97xOXj/21131s11tP2Hz80/KS/+mRXyzWLOXDv+cmIyK4Eny7j2eEYMeyWRmSLNwSVwCPRxYA/sheeJuVWjSM1hsjUS9aRaWGvBddhM4z8vwVtg'
        b'kBju+LDCarLlTgHuIgbGyHUJUXBfFLbqwWOwnpxXd2EXgGpwllj+HPy1xg2QsGvL+OpR2GhIm/eaYD32sfKCBRKbH9fZcuAlTRvyJH9wwgZfhp2rCORTnMKjUXdWL5qj'
        b'Wgbq6eWjR9NzJlwQoTgvYDdEGvAKbZxVgDuE0p3iYDCamIlV4SDb30PlCfYdYg8qQYfQCT1aUBLLXwt7lNDA4xKeGEJ5YjM8YKd8EqwAVbQx9jJoh4eiZOZmebBvSwbL'
        b'PhueolejHvWDp6Oi7eUZrKWoM1zBnJ0BDpD7loLD8BCqFWc0wkG3CWEvOMCyzgE1NBDoUIpulKPduIsWeB5Uscr1eXTu9kVocOFeAbwAa6LYDAV4OduXFQc71AhpJ70Y'
        b'Hho/C3bBi/ASekmqgr2odwUu5BILp7Ym6rRjdm8wuCV1cQc7GHR+TgbMp28XRKBHK8N6I1YaFIG9tOua+sIFQnvMbe2Dx1YTttKBWAWGBuhll2L4Kx3FWdAHtkURviuD'
        b'IWeCSu4mi20D9pDSlwOiYngpCl6MUwnhgnY7eTRM6GOBM/DQOtpO3ZkIzgixaydQGauE6kiOoQz3s2B1DOwlkhq3AQziFCrxYW9qGikCVXCDre3pQ5vWL24B/cR4joZi'
        b'3TIqlOESIsZc0IK7fNjAvHAjX9nOHrRzGFoGbLgN3ASVdNFfh9f0uU5R8CofVqMSUOPC66zFmj7EuO6fA/uFsdhPb1dBJgOIYIccXS7drqjBXEIZhhfi0OCwhvimkmNo'
        b'6rHBsUTQSvtCOgmuRaB44aFYR1DpPO6y0BhUcMBZeBh0kwJyR61SJHSKAD0qdrAZNAjsGQw1efZ8sGcByYM2HIRt3Iy5kYLoNaA7HImpkM9kGCZzwuBheJiInYsdqMcH'
        b'GajRHgeduIe1T4Eu3e2oj9sYRXvJDFDHvpHUQB17Dho8t9C2/Y6FoMWBdq2kGTHhXEkL7CbFE4diqBNG2PM3wDrU9wN1TLAPNdx2WtzbucaodKvlGExuei4ekZ9GlWZC'
        b'mokhPEKmZeCeiEneytDV5wjjK4NpCqtxgw7eIHW7lLaMTtBZuA320Q0sRnnC61I+PEos+e7Z+lw7VAiceWui+SwkK40scD1Rich5BuyIwnmJETAZSq4bsZw1GKoTIZUD'
        b'7aCG68S3R+0EpVexKBCeZxXZgOt0cneAq7DTAdWPE6pTpj922agO9rGzYa87eWoSH+5Bj12DZEHOEp4A55jw5CzQRwR0KezW4/JR0yAlIafCgg1MeAVcgQdJombNxqYO'
        b'PDmSvokjnRtpLqNnJQZ4RPZBB+wJQGMVWMkEpzelkQQvhq2FUdERfFgLuiMFTvIMbiQLnrOFx0i1eCPxG8TVUhLtCK5jOqKqM1vRO5Q8cb7reqIEGLAflXg9Zjk3wgFa'
        b'2itjPNC4rAReRjryGpvBAreYxjGgiZxcBWrm0FNlPngfDj1Vlgz30PM0+5AKPiwbIoGzykweOOdPCiAvXV46rYfalWh8owHcu4Le4XCoCJ7DaYWtoKIk2pnJUPZnoeo4'
        b'h94TuDHpr/ERYsdnpJ0ydLG5B6deBylfWA8Oaz2ZRYoKSfYZoQDehPv5yuC8I2pX+2LgRXShoQbHHo0upM7iutI2oYikp+TMC1KZSLNcBANE6jxhuymZLGOw0hfAeqZz'
        b'PpJXomNvwb1gG569XwsvoVoCXamazHR4ikuX2gnUWg8KifNaJvqjG9Yw4IHyUPqJZ+AZcAwNT2ClnYMuaiPwBL6mxZs+25IJa4Rwv13kOnsWQwEc1gU9LB/YTrPeouAR'
        b'sB3vsonDhq/KZG08hcZQZ7Fz4UlYRfsF3A9OgGYHpD2yUCbHfZ7CA3ZE/bsvh01CPEMYy0evLaRg0Rseq0gD0MlxlS8hUSSDASdax5PhkwgeAMeR/CbDHWT2LBK9MI/S'
        b'SnINPMEnBacMryDRAJfsSTv3hQNIhqqJ2zJWahg8xRSkxZO6A5f95IToraUEK9eVgmvoF3mINjzMBictQQMpdZ8NltgtMji+XOpGVQHpXjLzdgJeNwfVzvS8GzhlN5fF'
        b'k19AHglqwRlnbpmqEqzzRmVqwQyIBWfImfBU7Lu8Bu940QHbwGXmrJXwJMmIA8rIYTojEWu2IhWLL1KF7WxreDqOdolXAzs5477AiXtZ1DE6ywJHnOAJQitfAM9sIlBz'
        b'Z1gV44iUel5EDFLeUseI3nPkMXuAT+Q6F15aL5tzRE+ujxPIk0lHcIhNvA/CnQLQTTwcVsY5QtF03l5pd3Ep8LyiM+yfS89l9qgKuOQqcMhNsAY1G+y07zIbnAYXCuj2'
        b'dNkItKAHk0lv+VSSEbUkdkwi2ElLTCvqgu0UxvL5EfJ0cwthgQ4wgEoJC3MybIY38FlwrBhr9KNMgH04d9IuG5eAFnyuJHpLGNEqnmwlUAVO0h22+rVwUObyLlQwJQ/E'
        b'5d1GeIGkUHd9DJ2FBfqCNSg2nIOrbNAG+tJIHp1i4x2kr8PJHnKXeMkpBcvRknGtCJzkomsUIxioRfUxgQjU+9NN9eKWAC6sknWHFBnwZhArATR6EpVqButgN9Lzkbqq'
        b'THTjZdwUq8Au+q3djgrhIM6eciS46ReDRQXFoAN2suFePqwjr3wHeGkrl89gMI3iQRcD7oqAtANObVDnLYyFF5y58ArqSJD3ksYyNqgyK5J24VBVH4KXHJ2c3IuwFjiG'
        b'3mlgWz6JFO50Bi1cjMdn8ectY5rZg/NEq8EmeBC0CkE/6MaqvlJpIl8GsJbjC+sX08q3Lj6ZK0C5wj3OA+CKGUsbXBHSr66aZZuw9nSIFdhjgb4C+2ANCzdo1Dkm6Ms9'
        b'6JV6UehsD3vD+VgF3VgLr7LCwUFj+h3UNz8LXhLE0rYVb+XNTHgE9vrRrbt5Ddwu9VwIm1fHTfZcCLCbSFwfHHAtSugUWcYCPXykBlD3jcUCdctR5xAnz1oPdEs70xHq'
        b'UWvssH5ThdfYPrBNj9yuCXejeqkm6xEvw9Nq9PYucMCWFNx8LordKQbp63LYlMScA+v1n0g3UNZ5y3Z9ZYIapmvAKjq320CPoUPkBMcT7l/IAttt4Gm+wb9n3l7xVy8R'
        b'Eszu8//8J3sklKftdxsMZzTtkQl9XxUpLGSTC8PAWObTDc/mRzMfGtmIbSMlRlGUUZRYJwrzH43vGzoPGzqLXQIkhoGUYWCt/IieUd3y+3qOw3qOohSJnjul517LHjEw'
        b'aeLeN3AaNnASO8+XGPhTBv61ciMGxmKDiBZOG/c+z2OY59GbIuH5UTw/dHAoZEgJX2DWYtXmIDYQoN94clisHynKEztF9HMo7wgxP7KW88icV6syYm7TsK5lLfGRpjKi'
        b'w6uNbtFpM5fouFI6rrXMR9p6owwFTdsRI+MGi4bgpijpHrIciYkbZeLW60qZeEqMvCgjr9qgEd6s2ojaiEdGxiftG+1HDAzvG9gPG9hLDBwpA8cxNstYD7Pg9GqDRuUZ'
        b'FlYtAW3y6GIzy1FGAkvTeIyEtaEjs/jn5rTOOTWvbV5tNEpOS7REx6U2+uEsm5a15za1bjq1pW2LZJYXNctr8ukRU5v7poJhU4Eoq6ewoxA9+6Ryo3KLV5ufxMCZMnDG'
        b'BxQbFVt0j6k3qeM/uI3cluC2SLGVT6+X2Cq4P01iEEIZhIyYmDcoiA0CWwLORbRGiHJ7l0icAiRWgZRVoPRUsPRUfu8miVOQxCqYsgp+ZGgqNvRvSW0xQl/YqZv/KEPN'
        b'0Ggo6/YysGzEwqohTWw6B++q680f5uPZZlOzIYvbDsBhhGfVpiRKHea5i3nz+uXFvPAhG1RQQUwzVFIoRAVlZik29W5JblvYazNs7U3u7c8aLBwoHOFZnOO0csZPia2D'
        b'+lPF1jFDayW8WIoXi+KZj6OZbzaqgWJpWiiyGTZ1EZvE9Wb1Lb+4HCXAClgNrX3J8WVHiVcc5RWHqq8hTGySIeJQdt7ouz9hcNHAojvMNzivcu4kUzFLJeHpVHi6ZG4G'
        b'NTdjzFgtjGn0hIHDUTOGodFJ1UbVlrUtW3t1kbzbRjFlyUtty7hvPXfYem7/Mol1BGUdIeFFUrzIUTbLNpj5yNy6aet989nD5rP7lSXmQZR50Jgc2xDFi4JRRRytfKP8'
        b'iInpyeDGYCSWJpSFm8TEnTJxHxlfYKBgatab0Lfw4sIRno2Ylyfy6JpDOcxDv4Zcb3sD7zvB96Kp6AxxZo44KweFVHSuJCiPCsp7hC8vpC/3R7+GEm6ngbQ7yfeWUDHZ'
        b'4px8cW4+CqmYAklIIRVSSGKPFLn2zO6Y3etxeQ7lHjyUNJQ9lES5R0gcIimHSJxj+Vb5ltK2TZStn4Q3h+LNGbGyb1EW8/LHZ27wJyGFSlhKJeSh3xLnfMo5f0xVwQtV'
        b'FQrG5FRw7lEwaoRzj4RYmvspsXtLeD4UzwdVsSmuYlMz0qJw7c0RMXvkOuREuV0rJXZzKLs5Y0pyOEYUjKrgGJUalXCM0Y3RqL7FvDR0vWqHKpKJgosF/bk3VlDz4sTx'
        b'CeLEZHF8MjUvReKVSnmlSuzSKLs0JHwW6cxHDs64yPxG2Uz+UqZIT8yP6Q3oC7sY1h98I5qaEy3xiKE8YsT8QnFC4v2E1OGEVHHaYioth0orkCQUUgmFT0cCAm/rAT2p'
        b'ZCGxWkyFL5YELKEClowpcHCOUDDGlsfpRgESXyOzBuMW7VEsFSKLHrsOuxFTC5lAm4b25vcWD8mJTRLvhGIqcDCSPasWdZQyXmCv1+X5SKIcsEQ5GI0tZ/o4IyWEgjGG'
        b'j5n+ExzUho6uZTLMrZEaYupiNYTCBhbtp7GkacOx+U3zRVnDxs5iY+cRL+/Ly5D8NcSKwkRhjwSuDbEjNnZty3o121Y2hD0yMCONIOvcytaVuIzDGsNwrSm1Koksu2wk'
        b'PFeK54oPqLSqiBK70sSCkH5VCS+U4oUS4QoXuXV5o69+5qD8gHx/yY31Eu9wyjt8okxQDZpZiU0jRcEiRfTVr0P5RIo9I0cZiqZmqNLuxy8ajl80YmHdZijKH7bwwPVl'
        b'2W8x6DDggJ3ZRvTqDVvNFlsF9oeKraKH8pH0+Fki6fGzxNJjeU6xVXHEyvpccGsw2QDsFSrmo0/yHY97PmJ+unhBusQqg7LKQLdZ4NssyG3WFM8FSRFqgYsuLhpi3uYA'
        b'zlAyFZIi8U+l/FMlnmmUZ9qYumIC1mg4HNVimPKIFmtBmtOD1meag0YDRrhklFuVUQvz6PDo5VAu/hKHAMohQMILpHiB6Km+WNR9saibmp0MaQyR3eDW5UM5hNxxu+dD'
        b'RS1tUZbw0ile+hhbGRcaClBDsrRpMRZpi00EYpOwXos+u4t2/W43/CRuYZRb2IiJGVInYpNsVOzcAe5QwO1gEHxHi4rIlARnUcFZEu9syjsbXdUUhVdAoVqg52alFTli'
        b'7dCSISoTWyWigrYdsB2yfNnhZWeJbyLlmyi2WiFOTbufung4dbF4STq1pIBaslySuoJKXTFRiGNsjiuuXVezUWWcsdDGUJnqTGxbTFl7SnheFM9rhGfZxqV47kjfoTpl'
        b'DioNKCHdIrYqEJV0baScA9Av9LopBIV3Su5tpOKyxNl54pw8FFJx+ZLQAiq04BG+fBl9eRD6hZqfwqsK4vhEKn4xFZ8rzisU5xeikIovkoQvo8KXkfhjRGt61nWs6y25'
        b'vJGaHXaHfUfrDpuaHS1xjqGcY7C4hLaGohrwQypXYjWfspo/YufUgl6rReNTlfiTkkalZFIphei3xL2Ici9CGs8H5R8FSOPhilIhFYXyH9kYKc3/lNj9JFZzKKs5U8pN'
        b'1ipQuZk3RaGOiNgknxZ3VBS5IBeJhB8VlSsJzaNC8yS++ZRvPq7HOLFJDKpD+YvyvWv6Si+W9gfeiJPMjsa5comhXGJw0w1vDB/hOY0yuBaWva59Xhe9cGKiW6NH7Pg9'
        b'nA7OiKOgJ6ojasTFtY9zkdObekHlsgpKmsAJJU3ghCRU4HffMWTYMWQoV+IYRTlGiR2XkgaaOhyP1OESSfxSKn4pUs18e6Sa+faoYfPtid5eJbGbS9nNRU3G2ga1GGsb'
        b'1GCsHcVWoSjFqhdV+wskLqGUS+iYLtcDlQMKcBq9RvUYNrbn0lrTRGkSa08kNGOGqrh0UDC2jhnBtEX6D4djKDQ0fkLCURLSR8Y0sdYbzUcjQaP7GrxhDV6LJurnhLeG'
        b'j+jo1ocdCkM9vziJjiOl44gPRByKaFjZsPJYcVOxRMeJ0nGSHcxtWSIxc5XouFE6brJj+S2bJGbuEh0PSscDH4s8FIk7YJxGTkNy0xLK1EnWQzNpUqEM+CJLkavIkjIQ'
        b'9OpcNhQb+I4ylA3Nhjz7y8mPiZdhCxP1bvmi4K5oynFuf3b/mv5syjGAsgwcyhm2jBBbpt4pFFtmiRdlodqwtsGCJK07URJSvPSKxBCxYOEdnXsmVMRCid0iym7RiJ2D'
        b'2C6xl3NZBakf9Av1CVJB6p2Ql5a+vBS9RnCVoGBMQQELoQIWQiVczCgYU1DVRW8WFIxxta21njBQMMbQ1tR+goNREtgxNE1rVRqSJBoWlIYFXn6rb1S/4dAG7Al7qgcx'
        b'pen4hTMPYPASt/H1fvRKhO8x3XDm4YqJPHaazpAOV8pcZmAbzhj8YdDDchaBvBP2ZwIbEw1jY/kcFBBKQLvKc3D0kp8YhBGZFBQeEhOSRHDohORI09FbxpHmOP8le3BZ'
        b'6pbs/XeMK6erB2z/8p8ZWm6P62QayC4Dr7jsYNGVMc4u57BUNdDrEQUqDMtE5oip54gF6vc4jCrJWaFKwIEafWLuiMWsaU+EkBPmU0/koxOCEQsBfYc9PmE/fse0JyLR'
        b'CRvycF90whmfcB4/4TndicV0VOiEEzrhj4WGhGoME8GIntuInmC0iOlpoDbKQMHe8NFVTIaa3iiLgK2nBBg3rVezgD5lRqOq08QOceIFi0eMzUVJ/dpDQtQRVYvGq4lR'
        b'+ISEj0IjRwJCRtl+quEETv1r4ZjcxL2jHHJ8A5OhY1LrPaJhK9awHdEJHpVj6YRi5rkOcU+Pwr3BaIBCJ0iU1xsqSh/KueMpTkgWpywUL1oqjkwXh2SMGJmK3Ptn9ecM'
        b'WQ2tF/vEj5i6o4jUPFE8ap5PcIC0UygTlWNE3Cg7jKVqNMr4V8MxhYm4ydFETiBb1WqU8UeG9Poj7NAA7tOAFwjt2wl0w5uEQqUk25LGYsxZJA+rVoDDU5aecqXf3yzB'
        b'0G/tX4F+s3MVpb+VJv1WRr+5uSrktyr6rSY9rj7ptxQA3qQ0DvfWmRHuzZ4E99adBrJtMQ73NpoB7m28k5Fr0mX6P4V7d5mdRUq5U37KUy3H0d6q+XK55r8K9eZNgXoX'
        b'8Gc9UCdOEopK8nJKg/Oyi0qfOb9A9J509l/AeXvTPFU3PusBJyguMeQBO9AtsMQF62E3HHiwfztX25sGArr9Lhi39Cbv3w/clj2O8AddMXC7ZC692A+jsUvmYT62cmJI'
        b'TFxyCAFtWz0HuU4KDk7MWzOVeupS4o8z/FsudR2nUcsS8sxgpljHEdVT08xXmhIHrocSZc4kzrWscEpU0NESLj410zNcS6Jxrv+30qnzn6dTsxgvLmSXiyWrVuH5jfDs'
        b'GtBKHK9Jva7p5NHLGQ+AOnUbLy52nES8PzVFwFNFn0MtthCrta8XfYyp1acOW1Qz5VM+STS4dMy/VDNJOcmlKtqFXWDEOD4k91bNWT6T9sF0UNkYdDPpTYKyDYJH/F7E'
        b'W9PUaYPnWt1UrDWPQW8Ly/V+biMUr8GT9jykwfufsK5nfKqWwmTQdZb3fwJ0XRKPZYyFkvkZnrv6vw5kvZPP+tBC/reCrHNJqWNSL0aY/JEUa1lr/xWKtUxb/OoV3r+Z'
        b'Yj1VAc1EsZ5Jj/0CVnpanTT99b+DIv08rIrmqmStwkgUzJyagaA0ftt0DjdfIE9PqWcpbRq/C2mCNHof2s8MO/o1zLMsJb8H9FyU/1/G8/87jGdZi5sGcYz//RbS8tRG'
        b'+xtJy9M24P9ylv8gzrJcbHLZPPRnBDwHd0+P9IWH4L5oTP8A9eCgc2L4JJ7CINzDhWes/YpslnmzhBkonj5FueOvejaf2nmQqeZr6Otz1NXVpSu/otLR/1BI4m3q7jt3'
        b'37773t3hu+/fHagxFe0wtbl9pxaM3NV8Y2f88VdUcvS/qV9tGR2RtUjeY7Pne7tt/qRzL2R3pvzrpQytNRq9n3P49AqQrfCmowNok3eaxAU440vWPMHuLLywBnWwDqUR'
        b'uO5ksK65Db2MsFMAjuDFNytzJvvRZAdviqFXVOyGzSujwG5wToaOdV0nXbKgUZxDwxzKQFfIFDBu4xq+8v/AaoM7G9PSZF/sME1GyRbR3bR/rPZhaOrVFreUSjQcKQ3H'
        b'+xqewxqevQX9pUOpd1JGvAKGvO54Y5BsCgHJphCQbAqTzJ3UcupUR/TN6jbiY+HMFzCr+CB96j8HWZ0x0wYK0xBWV3r/7yWslmSznxu8/DpYtSSX9j80LVT1haKREVUD'
        b'UdFMIqpaztAVeIGiKv/Lu8BzFCalnTulSyw3tUuMOsRK0i4xS0pHVcV01Hwu6RIrTNMlViRdYoUXusSKL3R7FbYoSrvE054b7xIXoC7x5um6xL9MRp1sffh/Aos61V+J'
        b'tJ8pZYWuRG9mDG38Lyn1v6RU3n9Jqf8lpf46KdVxxt7oCvQ+oYeIsor4HeDUX1AZ/0lw6n8c96kVS3ahl6iDCuK5JMdYivvULaAdl/iiIB1cgc30XoukcFgZJ8DIi8ML'
        b'MYkwHO+jqIQHotKwhw+MNeSQxcVKYACchM0E5Am7wHY/7lpw2HE63yauYbRjlQugFZ4g7lFA11KaHoq689XErwk4pwT3j6+Ef9HRCHEyApuX45sPw5NK8IaSRpkDujEg'
        b'AO6cIBTCvTae4Y40rwPujUGjigi8xyjDVjFAR6MM7zoHfe7gUtRzIw1MW3SE+2PoLWOJy7lcBZTp84ZknJIWooB3f5GoUuLTBKlpGBcZGRMN2pPDQXd4jJMgIgZF4cwC'
        b'F7luoNoN9CcmMcxAk9qKPLCH2F43wr2OQrcSFgMeA5XMYpQIeCOzDC/KD4fX9Z+LHSMQV+fBXrcSTFUkLFIOIxNUK4Aj8LBvmRO6a658YJLsUtoZTHjyanI9jgk95CDJ'
        b'9uJ8BXDGyJDUvzcchBe5JWqqeC34xUxN5lx9Jo3y6JwNT8NLsG+dkM1gpcFdcJDpUJBOSAfipXIM9K3BDcpU2bxWn1EkqN7OETLxJNabRUcOzeUCF43dzkXHtyxu4rwU'
        b'8kPIM31W4NI2XYX2HaseO51vHngSt2GLVcwyubmKf954c+OX1nc9bzEVaiRh5z5kCLrT6nJe9auLEx5hXf/o66e36zrK3le5a9V3ff+21rW7lxkv6k7Nu8pV3f+muC01'
        b'zs/9s9TePdlVWx7HbThue613Y8igfsiXRfO7sm8u3HKfM3gr+1p8x4KGqtihtO+dOpfWqC4bjeje157xRlZ2QmCjGb+spZKdnnMmNipJV1hyvDDxydqib/6y9WneyTsK'
        b'e++qv5y88a9uD918fEtUPj2+tOJhV86p6vYfGz9XkWfJ3XyXE1TjIlofNJv6fPGigP5b7K8jYr+rzudrkHHd5hLQNokhCPaBnfRmo7OR9Ia3ncELp3AEuZorMUYQtsOd'
        b'9Mrx45tgBXGYAttLMUkQXvUhd66F1+dNovxxQRPopyl/1zeSXQtyQlgtHRjKRoXwpg0eGIIjvmQtu2p50bhsyaEYzoSuYsHjBqCfbFyxhf3L6CXrGrAKDzhBLzhFJ3oA'
        b'tcvTkyiGXFt4DW+XY4H99O6nCrgLnJBu7PWNnbq1lwN7gCibjIyNsuBOOg+4aVdGM+EJ2MNQg9fZ0Wio200XQGuKLqwW4M0InAX+85ig08SXpG+W0DTKLRK1mRtgLxPd'
        b'BvtAvTO9t6G7HFyUzT3kImWEpx/yYTspFhfYAgcdImE7K4auF5R+bVs2PA7awGFyu0oB3IVd5KA62Dc+lr8Gep6Q6d1LoFkYFQ2PgpZpQH805k8b7OKr/UFLKLBXS94U'
        b'uN4kepX58wOw6ah6A7SLl9Fgv3+NqodxbOb1Ww9tlejbUfqYWaYZQg/RgyRGwZRRsFgn+JG22Tjgzuvy/KG8YfcosXsUuSpQYhREGQWJdYJGVRjGlk3OtQoEGcfUnE/O'
        b'z5UYzaOM5ol15o1oG9X5kRMts9v8eq0uO1JugcOzAsWzAsmugUlX6pvd17cd1reV6PMpfT6+J5veWZAgTl5MJWdKbDMlRlmUUZZYJ4tEK9a2l1oY2LppzJbStvLekGFb'
        b'H7Gtz0Mze7FDyB2FeyoSh2SJWQplliI2SBkxtWpajBFwaUxRctfCfuthwXyxYD65OPSO/j0TiUOKxCyVMksVG6Q+MrakjB3FxrN79cTGAf1etYqPjGc1zG1ZU6v4sb5J'
        b'Q4YoV6LvTum739cPGtYPGgq7kypOWSJOzx4JjhMnLBQvzhljMw3ysF0EhTgzeZMNHWq/BZT260ukiEhNZaL9DpEKwVaPbsaE1QNJVpgvkxlBjBV/dPjvM338b2OdLf1V'
        b'1tl0doE/DHRmGUuQ1/Aq7NSNmnBTPy3mrBxcm550Bvu8yrD6j5oFdo6DzlxArymoZGQHzWVzGZawi41Ufh9N0EGvuV0mE17euJbwgI066XQYg72wS0YwQ6kCV0DtKlhL'
        b'Oh0eW1hk1j1z48oVPur+DJrgcxHc2OoejVR2rbuLjFIGz2nRBJ9eJ0wp8wMnCajMGbb7kT6PPurW1AnDtdbgvcf7GaASbNchCVsJbiU5oNfULb59jBRSNp8jnSXPDqAJ'
        b'ZdHojLweSyUcXiZT6/LgKNiVBHrgMSmlDF1rMo/khg9FBknpYCcmlI3zyc6bkwhXgQFYww2BjaTjjFFioFmBAMNcwK0NSdr548ywcWCYJ7hJCmKB9X6GCZNhoJG+PNbK'
        b'Xo9GXSkkWjKC0Xd82npWkroPffD8snBGLYrR32TzMmWm738GGJb/u0FR9s/rnpkpUQPYwriPLbUwkkzm2KswkCjYMTgbVdibuPTBLhs9hiPqoY46ZZk8dY2mSd9gO6wA'
        b'twjabSr5ayvoYceBgyZ0x/cmvAybuOA8OI0xXzTjSyuARPvjOnns/UCD57zZ8TM9AwafSaO8aopVZVvOmbngJA/eyv+/v6zZKMclB2RlTZfN1XWgl6sPdmLOFs3YArWw'
        b'n0i0CmgFNVwHeIwGbTHAMR7cR+7C/hxOTWC2GEuTUTtoLSIgwWXw7EYuvIL6cRi0lQA7dMktS8BuAQ3ZAse0CGeLtSgcXiDcvwBwdpMUswV38ZkMOULZCgXbilyZVznC'
        b'9agV5h74/OaChUl/CdU4mvuawqE8NWHDmz5HYxSvc+5EqCm+dmi58JBf7/GcQK0Al7zE8vB96YltWufWP8pzUC9PSOn44aM5Xw6e+jrj6t9bAmatO2CVqJTi9GDuj5sf'
        b'ur8dvfX09WsZTR94Bi1X83IQLH3zweh3j78S/XCz13PfZ19/Grfh0kdVxbdOWWy9V+t64ijjcGVm6fn7nVpOOz66qNn0UrQz+xv7S0tyrbjvb8m8J29W/sPsPV/sK9+7'
        b'pq3LptHTOefYQt2cg102s2++91Lgm2NCA+2n3zQMyp28WuHeJHnN08H4QdGax/de++ZGxt7H3yjPgdz5R4deZbQ2MBL+ujD9b5YX5zz+VlN4QXFw33fl7ws+dOfs3GGx'
        b'4JTt+Zr8rv4ftz90WTAWX7DZ7dAXV1PN5X5gNN6ueOtuSKdWQ4BODnz2JJO3QbFbPOawc6tBnvPdG3MXhg73vvSs5qPouTdyDMy2XLPf/+l5idvoAYUTz+b0Rrd1xbak'
        b'vHUl07bvlVXyVyNa324f+ue5C4qfvNz1kkrC5n2in7YPrTW38oau6nKpP6p4m4c+bnmr3uqe7vZjcvdWrDC1PFHU9cOlgObUueXnI8vNKv886yOLuEG3uD1fSRb86dNb'
        b'1zQ+YPxZYcmBV0oqy/a/PfzOW4O+132N5ziF7/1u6MHeE7fFug9a3S+3nL4SkrZj0flTV7x/KgODGou//8v6v995v5P1geVLfcG9wV9k2Hy+ifVN0P0l2y/YKt1LChbc'
        b'eW9Eo1M8eOGHv4+Gf7Tet9do+ZLl9/zfL8j+Rjl6Z7mR+I10vc2rdcUOdo1Pf3yn9+uapJPRb5yqmTV3zRvn2hV/cNb4Kdn98NtfvDL0efvKI4+WwB8+n2c3/y7/bd0n'
        b'Ee/+6faNeScUyvK+vFeeGuYsfG2z0oHc0xsfvqfqYHJJdd4b/4xUyJP/Gc46tNthbF5iSrf2T8Y7t7K/Cfrk+PqH20asNJwVvOxEnwrtuz1F/4hp/6LHvu6NraflW4Ub'
        b'djW82bn977d2b3iF/939BW/cfeqb8J0A/CyfAI9bvrsYbDjedNePv+B91a6oZc0CHd2ENwT91Vde2ew4vMvx25tDXy4b/NY1NHLuLsmr6fonbnpXH3B7aPZUoXerf+4r'
        b'Gw1efXvB4wcHX1IdOPmov+1HK6VnW7+0Ndc6tuzCP7Qj06oiRKXW0awz1bdvOyxVqvf/7KOx+rQBrQ8Gkwee+h6O7NuwpFajPmXAPOtKW8pAonVl3fmPDL/37v28uvYr'
        b'7db9i1aYVtjafHPOMuNx17s2X59qFtTsf6fez+79Ve/tuPBu8Ot+O392Bz+XNz54p79k6YqPBB/sNEnrYfysX/jX3HumH0epvLLyTCi/7BtXHcO3jmh93bvje3vN2J/y'
        b'X5rNNX8zIOnEvZN6cT994rNV/y/5Nrk/Ghkzf54tGvxoS3UBe2e1hb9ETfS+p/37tXnivqXU9QuORjfD7p3f/ezNWwuv9S+s8FI/2a5xxXxkfuE/5rdrf/HDytEtivXb'
        b'fgTZSY9ns3bE7Kg4EfHuax+uWhnlM8jtCnK4+3fl5HLV2w5r00OvaNfNdiyPlvg8ef1VtTXuA7P6PzPP9Lwb9+nR1Dm31J/ssy77UJdfTJA6GPYfMi3fijOfDXu2wEoy'
        b'Di9QB1eldKtlGjLaPjwPLxMTgsAeXHDwyHN63hsp7J9DRuMm4AhsjvJFPSaabjVOtkqFx2h8AdwB2kH11gQpkmoCSAUrosmIdzO8EC4FUmmBXrxpfz9L4AsOkttN4U2w'
        b'VwguaEx0C6VAKjt49gm2scFGeAY0EiQVaIfNghJ+pNOaCIyukUGp/MBOeXCJCRppyMhOeBKekkKpLFnoeRks1O2BZ+iz10FlgRQ9lV1ICAIsa3hQ6h/BUABbaPQUI5SG'
        b'T7HKC+Bh2i5xZSM8IoNLwW5YQeOnWHFmoIOeib+upcR1BNtk/KlJ7CkoAjdJWdijvux+7KtFxYnYHAh9qh5eI2lLh21A+gQB7JxNEFSsNHCLSfMHdoDKTYQ/NcGegs3Z'
        b'NH6qFVaRmfwgJR+aPaWSxWDIYfQUuABrSU1zUpVp9JQMPNUJmwl8KmgZeTpbexEhT0mxU7EhBDyVC7eRepoNOxS4oL5Eyp6aIE/BBniCwAY2oJpslrKjOsAemh/FWgzb'
        b'45/gjkGWYpDQ2JzGRzGAyG0dYb44lXtIyVHj2Kg8sI2Qo8IhXZ/oYVWLHQIxa2xiuSdohTdpYkMvbJ/FjRWo8K0MMdjoNBOJ9nZNEnmGPB5TgIYCGVJmHCgDdoIqUmeh'
        b'oH1F1AtEKh94DUOpRAE0QuQIKvp2IR8ep7lUMiaVQRhphinrwQ0u5lHhwQys5NNIKjMOB+5IQIW/GwkeYTHUo6rfEZXFpPFT4/Cp9aVEulxgjzvq1YArNH1qgj0Fz5iR'
        b'mvVFPcZDwihU7RghQpNKFprTyzeqFqH2eQml8yaNn2KAG760w4lY0AzOTralWcNbBD112IAUrhHohP2w2gWep8klBD4FLqO2TRrLrY0pk11dqOQaa7B1QbM3vaqkLho2'
        b'E/wUDZ+yiiP4KdQ0DhITmh0zkPCnOMqEQMUCDbDDkl7Ae1RgQOOnQkxoABWrCHR60UCXKpSXCocUFyl/apw+lapCNxKwB1QS+pQlOIO7ZZg+Bc6CHeTuNfAiPCzjT7Gt'
        b'0Zid5k8NoEaA2184vBQZtQq20P45pACqbaj1kzmCSnjZUoji6nUi2aURVBazyHM3ov76iSjaUZA8gxsPajCCCja5ktplg1PgpDAL3CS4GBksBkn1AZoNVgmvmsJLm4No'
        b'EBUDnHdBZ8jQ8iY4n44Sex5cxCAqKYRKgTY1wh5teAhWy5tET3IEzUV3ktXWLVyT8eEAvAav82APaqxEVZ2Ap+HNKGbchG2YtgufhB30U5v4bJpsg4k4PmA3geLUraDJ'
        b'NhfBDnhKCLq0x0FUUzFUgbCdbl+z8oXTAKhKwGGO/brFdA52wgYTGYLK3hHVF0ZQrfGh5Raj/dpkCCqmIzzrzJcyAGEtvKInJVDFp6CKwgCqGtBG33coHe4bB1AxNGzg'
        b'AXDQi75vwJgw7rq1MYFKxp9StaHF+TjSB200fwoN2GkEFcuHvZ5oOBvzNELDwZi2vTHwCsqLAdI9nXYch3JNWmwvuGXRwwUncFY6XOCA7U/wCINVuHXc73YhaHPlrJei'
        b'3zaAPq4sSizryv5a4BALdFksp9FO5+UiuYSgo+PLwUN+S9Akhbd0o1Fkg8O4XlKB2+0L2OorwUnirgfsVMwU0q9CpXHQlakfB26DreAgBxwgkWwBe9FQisZduW/EzQXD'
        b'rmADGKD5Sg2L1tAVLCVdocZ1naZdXSkmBnJwcDFrHHbFdIZNgg0+pPKL4U1zYWKWFHc1lXU1y5nkrXwd7IwKV6Wt6xh1hZrQIXIzPAEOYf4d6AJXaELVBJ4qJYWmUx1F'
        b'b8Prskk5eEybJlSxwJFZ4AJBVVqAXY4yOhWKRhTjyH8BTwX2o34GVgwF8BQ8PFFeDIYPuKoBK9ily0uJFteCdaiPcAn3cpRgFT9CCh4yBNtBnQsnbA5sIeVpsZlg+9BV'
        b'8EJeIMqwAmxiBaAOiogkOhjdtgNUo9FqXdyE0sU8KniCTSLwWQl6Jk+L+DPwrAg4B3toEe1fhd5o1XAv2EsXG56SAINwkNy8DJzzRO+hC3FIog44IJ1r66tRzt5UCm/R'
        b'L6r+IrjHAUkh6oothPXYogOPsTaWwnryrkuD3QpC7EeuEncZcf6YqK3D45q67M3wtAfBdOWCC/FSStcvIbougWsY0+WIYsbVKb8ODNCMKynhais8QUOu4E5AM/qKUmfT'
        b'hD6scFDDP4epd36giW7QO0tRu/ROI3wvGqsYDdvoPFU5wT4hKiJys4zth95qFWQuyNTN2GEiia6Ln2Nwob7jVZp2dQhJ/SVZGslzQMd6GiUGb6E0kh7WLdhsOx2LSy4S'
        b'1ivZOdFqtx/UFnG58CLpB9A0roW0sosp95WxuMAZcIHwuFgJIZuk/r6uwEYuelX1EnIVTeMC14tJ1aCXkChByIOXCY5rKotLAM4T+hNoWpmHMoAULuZxMeAuLwZ9bx28'
        b'kEJgXDISF3qDiQiNC54Cu0mideKWoTo7lejo5CSjccGr6TTiayHslMK4mEiPNpupC0lhmKDyE07D4YKNSzm+sN2dLoxBe/RCwiwuuC0TdaYJisuAVJzDevR8GsWlAo/S'
        b'NC4WOOqIRBkLeiHcZUZjuGA73E2juFjhPNhJzm5F8tUlBXElgytIb2ESVwlopjva/agSUAdzdQSBcU0lcW3XJrraFg6uxSAuKYUrUh9zuIJ86S7GuXgfeCkzUQrimsBw'
        b'aeqTp2/mgOOg2hqcoTlcUghXI+oyknd5BVIV16UcLibcs2hOIKA7F1uFBTRsC24rpnlbLKQ++ufzdf9zdC2cwqnW+cloLXqjut701jkyn/ejsnRjUvKcPxSqZSw28HsR'
        b'n1UrNyrP4Fn8m7FYDsMGDhIDAWUg+CUs1mYmxmLhcEYs1kyHfyMOS+eYWpPaH47Dkj5OytFoSTiX3Jossjm1pG0JXTr4RFRjlIhJcAzJXQvb1bvUJSbelIm3FJvTEtoW'
        b'JzHxoEw8fh+U6jnWkVqjWsvatq33becP284fUpbYRlG2URKDaMogGqfxv2ip/9+jpdRwunFL0JMY2FEGdlgsVBtVJxWMlIo0iR+S3LWEEsyV2M2j7ObhY0odSpgHE9YR'
        b'1hvaHtcVh4oOY11QMCYnh5EhKBhjT4MMYXNxMlAwlsD0wFwqD8yl8sBcKg/CpVpBc6kCCZcq8F/nUq1qXfX7uFRjcmycWBSMKv4x3KbIxsiWkrZyyjZgqOTlcipsYUOk'
        b'xGQRZbJIqhRwbKqtqrjIw1vDUXIWUwJ/ShAisQqlrELx4ajWqF7WZS7lEkS5RN53SRp2SRInp0tcMiiXDIlVJmWVKbtKQWLlTVl5jynI4bKXw2WvgLODglENhqn5b+E+'
        b'mZo3LW7KEJvO7g3qVRhlyKFcJwwuHFgoLa9HDoIuv675SGCtlzBb8luKe+XE1kn9roOzB2YPub3s9/J8iV8S5Zcktl4pTltwP23JcNoS8dIMamkhtXSFJG0llbby6Yh/'
        b'wG15ID+05nYpKL0TIwlbRIUtkvgvpvwXo/LHSWfjpMvNQ0lHAWpr/8VE/RcT9UdjohYyfTElyhdDonz/D3vvHRDVlfaP35mhdwSk9zoMM5ShF+lI70VRQKSJoggDomKv'
        b'IBYs6ICgg6IOiIqAioplz2ETkjXZGXMTZ92YkJ43m2wwMWWTTfI759wBQd19N5t93/f7xy+SM/fe05/nlHvP+TyfgzmigjFFVDBmiMKOIR5+JuP/XyWI+v95oX4NL9Q/'
        b'eN1uUp9JCpUS+n9NCoXZAWqNVJSkUBxMCvV3vN1v/L/B6CTCa00vInNi5PgLluOz3CrvYVatgv+WyMnjHxE5efwjIqcXepQzHnyFdexsvqb4WXnwsQf/n3pgUiYvTMqU'
        b'weJiUiYuIWXKZUiZOLr2k9QsZ5qUCT/QmuJAmnfX8V+gZHImpEv/vTubkok8T51NyRSIKZmCMSNTMCZkCv53+JhwOTNJOTNJXpmsidgERQiaz8N1MSLx17m4zFPpTKqQ'
        b'51HsKjbmTPpPugwsBa81GUaBI4R6CTZ7JKYIahJS4B4PvFvCotzAHdWVFDw3Cwmnp/z9OgK10TaTZ1mX8lUIV5HmEaNyNnaP6CmvjZW/WsxvJaec08+ZzXNU6kxsD7Hl'
        b'IbZE1GnSbdJrMmia02RcrlOq8hxvkSqbKlMrVd1Blar1qz/DmKRO/DSQn+ZzfhrETwv5aT/np0n8dJCf7nN+WsRPD/npP+enTfwMkJ/hc346xG8O8jN6zk+X+BkjP5Pn'
        b'/PSI31zkZ/qcnz7xM0N+5s/5GRA/C+Rn+ZyfIfGzQn7Wz/nNIX42yM/2OT8j4meH/Oyf8zNuUi1nlTrs0Mg3IVeO6GpuE4V0yUGaVGvSaNJGmtRHmjQkmnRC/qalbALB'
        b'cnmoEx2Zkh2jxGa+d5X9jO0nNr6aGYIhl5o2HaqrtltdXCtiwvj5eDC/QmyERK58ZyU2BQEVCewiZ1g1Ko30CJmE0hQQ+daV1WKKC7vqNWW16G62VeIMdK/Iw66suGSZ'
        b'XW3Z6toyUdmqGUnMMJvE1ruzUvhHdkmzgaizblKrsTlaQjmqHUG5NpTVltmJ6peurCQGVpWrZnB0EIsv5F2M/q9bVls2O/OVZXXLqksJbQEqc3XVmjICma3HM3jVOmw5'
        b'NrOCArvYSmKE5RbJVdokV802TcMWXErjRkYRnko9TEncw84tijsVrNhOVIaN7OrK/pmSsA7dormY2KN4hiGj0oSwurayonJVcRVmmFBSICIRYPaMZyoqEhVXEG6RMszS'
        b'UoXteZna25WWrUavLCK7aqbgxBrRTekXhVvYymrRbKO0kuqVK7HtNWl7z1g+pnLZDzlrV1Y9VCspXlnn51vCeWbQJBjGI8hp02EMr49RpHuoo8GOTQyvmQFPH3UdgyZW'
        b'uR5BU3PYVPMzJtMbVQiamvMcmlrlOcQ0Z5OKEk39Qr9ZTEQ/sP4FJqJZXfEfW9D9I6NKJB/GnnJBSrLSIBB3jmKS7lPNIx0To1nUsV9saetWxjTIf9Tr/wlDDlFOMCY6'
        b'KSlG48YSVKQljGEjk9h0IjMbb/GqF9skl5ZWMmawynxnNV7czGvqy5QDgKge9czpAejFzCCzjIUbllWiGLj/FtfXVa8srqssIc19ZVlthdJo8p9wjNSifr26elUpljAz'
        b'Kszq0f8c7T4NuZ2BdrdJFeG9wDvHuofk3/G4fXU/lXJf4V5t4b41uFVEVW7UOKN6mnmr4CJnobYQDMGD8BqGWNRZqnFhMxdcBS1ceBQMAiYCOAN3VpDV/+x6/LZsmA1H'
        b'wXnVklyK2kRt8rInqOEH+EAhivKq016S7LVIRBHgK7gDty4AQ+w6lF8IFQKuL6v6/pdffokVENM6al/iEh3dRi+KIF59wbABRsXXwb1e8IjQi02pBrHSTcAgl12PTwMC'
        b'BzfCbSK4Rw82NwgEG+EOfEZgcqpA092NRfnAI2o8cBKISbZxsHe1NnqcBDsodgorwCYepYG3WbWXwM7pJFB8LUEObEa/LMohWNUBXgT7GQTwMXDAQRsFKAI7+Xiz7AYL'
        b'9AbXoUTckS/sDrebmUhtgnsNwKf4wMu8hCQBhoTlQrGGlVY9qZcVPF8Fh5Q+YAfcT2n4sVdVgSYup5459a0StiWlwr18eFDo5ccuyaF0NrJXwL1gmDkBfDQRSp76qxXm'
        b'UTqb2FVci3rGxm4zuPrUlwX3wRFKZzN7pRPYQSg7wTVfB9jCmEnGp+pyUMiM+Jlotxh9ddPGanJqNFLXNUtRcoI73nfL4MOrZNfNCOzngJPwhkV9As5QCrrgzplmFG4E'
        b'lpeOEk1OSuKza8JAlxU8AQbhLbDHBA7CwSRjsCdJWwsOgpbEzCyqrNwgAJzQJK1mYTRpCXbXEpZ4qASGUPWLKXJKzhl47gVZYFNVz8QcN9gcD/dmYQPRpBw4QFoubrfE'
        b'hiMtQXWOsxbcCc6oqsLrsc5eoaCXS8U2GMMugB4ioeM9qnJ4wwwO6a82hzdqWRQbjrBc/JYy5qrgBjyqrVGbAe+sQapXYbmD6wxcGw5plcEhnRrYAc6QSP0sp7mgg1hh'
        b'VLkJRatTU+EOjHXh6LCW5CxkWtKQLzggwrCg1lwdHGcLywlcU0EtCX/Wp4NT6SJ4tQbcWIATBKOsuSHgMLH5sIdbQQfOLQy2TmUG+2ALaTJzRHBohs7BCXiH6FwX9tUH'
        b'4Fxvl6tgf0bvLuAIbErhJ6blxE/HUUoUbIFDFDxZpQ2k68FW0kXg7tSUp3FJxEhwMi2HohwbVeCRZbCXHAMNz8yBB7KUeqEWADGlrslCGr/iW2nU+le2iI1m1bDKz6/k'
        b'LlphFGl84lHK4PWqw1X3F3f07TuWO7rI80pm7O9+Zhk++f1n27e/b5yYcCq+favD7SrNH5y25YxnFf7wqe2T0vo/vn4v9Qb/UwDa27/c8Mlx0euvv/7gq4ClhyU2dds+'
        b'U7h8SL0TnnbJejhu7El6y8PIis+ph80ffxu86ELv2t3lh9Y25WsG+56PM9lxWPLT/T0vdXottgwam5S9bSZT/zTyUdCh9w8+CNW6rD72+ph/dOMRP+9974WJPz7e8vmj'
        b'i+BDCz+TnJR3duiaL2teX7fr6OZA8P5bbicvlnVVVYXuvqe5KPBtzQt7x/U+8z5hdELu/nO8fKFv7HtX+4a+rF30znfvGe64fTEvvOLghc8mfy9xLjt7Ku7vyyLT1n76'
        b'Xu2x12Icc/d7yLJ/Fxh03XXBm03fnpOsSHhy9VLxZwk6Xq/H+detN8r2P+RWXzHxRoyJYIXz4z/r+vlc+Opzvbrmnthc2YlBV98zi+t05DfmTx4PuPeKRWrP8sDmt7jD'
        b'c/efeWlM5tcX1NX3sU5+xT6dTzLN5+7blHQwpcCs68DCiaSfPL4KrX71otvktss+OeK0V0Lhvepd55Zc8lm7t1bzG6OinBMFTXGSygzj7uqKdQcL9pZfyRq62u49+Vb9'
        b'O+9lyn5e4v12zbj77zMfh0zy7wx+8HedO5NWH/7l0IePaJ/N5hd4r4R++ovpxI2+GpO9ix/sH6sPG/RL+cNB1fa/CxJHx1ZNPEwZXmW+9N5t11sF6f6cedcO/+Urj5Vj'
        b'hkav5jodCNkV+NprBo/O73oz0pf/Oa36DtDqH1usI3yrSE+Uu/T8+NqAV3QfcR1zDzfBPvbmLX9ffdK90WwU7kvte0vWt+tPuY0J1tY351zYnN3s94rjrTlNLyX2/36x'
        b'zo9fhOeyS+LbInSrXU83Nn3beCfizZ+WVd0Wyq7mawZ67xgOPnfS7L2NtP7yh1/0GH5/Wt1l0zcfD31S/bfN5ha/e3vForL/Ctn6y0sPv+bY/vBe+yS18OMTfRFr3w75'
        b'64kftF89EVyb+y0/2FP410XhwuY3HnD07/EktnHfltZ+f+SQa+lXc+f9pPaGptWTD4a5kQxOoW0xkPIEKWxwGJxE/VzKSioAZ5mDSYfB3gWgBVxCY1crPI7pBtLgHjal'
        b'DUZRnwc98BDBd8EDsfW8hGT1RE8UvYkVVuRHtvwbQZdg+rDdZbCZYJvBLSHxFC3AI64ng1sFI3pqS9gO8CzcSUAGXuAcPI36eLNnGp9NoYwvqW1iu/Nh7xMv0rtBK+hD'
        b'kTEmNlkAmtMIqhf0OYImz3gPd8JZpk4VoXeDC6AJ9DBIkNvgAOxKmoHUhsdgN3MO8Xm4i8HLHgfiUAx7gPv4atRSKFErZDvOK2MAnU2wF5xJSuMvTU7wwDAebTCMD869'
        b'Ds8z6UtBP0FrwdvZz8LF22A3g6E5Di6BIWwZDm7CfTOsw4lp+BbmCEmU5mH9qUPYwPYIBvwRzmdK0QVPg/7pU9jgdXCVoD/AcDWDwmv2L+UloGrvAT3oxUOlggV3OcP9'
        b'RJlWYOtyDF+aiQuBt2A/ZQE7VWqQSMUEwlENL8HbGNAYWqOEY0aC2wT7qAsPgitI7IkpSXwM5UhFabRpEniJE2xTDQFt4AiB3/FQETtEcF8CVlCSXiofDiexQb8DZROn'
        b'As7wwWkGxDbqjF7thhLgAU1liAsoO91YNryeF0hKnAlOg/0ow1S+R4oyP5QZCkfZeaugVtBdSYTCAaMoO0FiMdxdP+NgOdgDRom/PjyG5N6SJkhM8UhIYcGuGkpvGScQ'
        b't2uCxglwBJcZNA+D5CnOxwBV9dVgkIEp7oedYC8Bfu1Ngi3qFGr3W9U02TqgqYDpQK2gbY4oORUOALEAzcorWBvAns0EIaie7YgPUZ0zZxq9us6IATDe1EStHR8FCm+a'
        b'TGMx4R1wlZHNCT14lUALCbgVDCE9ww4WvAGGwSmSqXCjhbYgCfTaEtBSHwu9Xo7AM0RP3mjq3EMOSgXNcPcLMKos2EdaCx/1rOMEKwpHdAhcFNXxuoikH6EyZ/qQU1d4'
        b'nmBMD69kYGdiY3gAgwv3wEOgL1kN5X+cBfb7w2MkVW9VVHBUswPzYAsPF26IBc4tsCGNqwBeUCen3zrAKwwWG5wxJF2+FB7SmTq6W5WKBtdV4Q02ax44SeSYBE7ZEDwv'
        b'EBdiSK9doBIs6QZ7UI9omQnmnQMubrDnwJYG1KtJnzm1EPQTpgeCOIyFtygN0MEGzTEbibjQIHcTdj5nK5IL2pWcCZGwiQHb74Uj2ehlmQuaTBgI9BUWuAiP6DC44sPg'
        b'gA7xZd731CLAKKVXyokF4sQnmBoE7oR7I0FLwxo4rFvz9PUxAQmxGRzwhPvjU/hcNSorVkMPDNYzY0EX2CIQ8bTQyzyXpQGuUuob2b5+cDvRUGDRShGvljT4hixKvYzt'
        b'g8boEdIBI8At0IWqnIDByhidmMbDZhGqlAnsUzHkgV5GMJ3wcrE2ThunYQVPoqGmjx0Gd4E7Sgw76ErEqeAUUEtV91pB6aVyInwgg0wMg80BItQ+WdlQTLHgNZYBHIXD'
        b'ZEYICHHU5lKww4JB45WD/URG86HUcRYaz2A53F7CAXt8wS6i50ojuFuUygJb/JSmEODyQpLgoiLQT85ydVOj2MYsR3NvBo69A55OQ0VEpUhAvZOMEJ6b58XDfRzKEZ5V'
        b'DYAX5zOwuH40khxFn0FK65gkFmVgjTryQU4GEnILA+e9vVRdxGWBASRoCt6mwHVNBi+HPr1uOIu4mg2ov6DRhQN2stb7g1YihOWOFC+Rn8R3T01hRTtR+hWc4jC44wmX'
        b'TKyo910mpetFA/dUCTHlSDMGLXMLVcFxNISfeuJBvrSgZN3zzQO3jTR/9Bp9DOknBFxUSzWBR5nm2Av7GzHXBthf9dT2ow0cYEatO/BiiTaeXqdmGUN4oyidAy4UpZPo'
        b'1ug7sotH8MB8NU87SgPeZIODQCJgpqpzcWAbPtATzdJXn8URwuFVXMv/jWNM/pXNMdxSZ61BvGiPjPBJmsxcdprNoPlHVYapY3kUGiNtWoPFJRI/uRGXNuJOUhzD+SyF'
        b'hdVJlw4XmX3YiOhutNwinraIb41ujZ6Yeh46svSuo9wijraIa41WzDVvLRE7iusOrjqyqpWjsHVoVTmio7C268w7WdBRIBXKrT1pa88BFm3t88A68L514IiR3DqMtg4b'
        b'WUpbR6LAWvhUuXwGOMcEJg+NTGkjvszIT+EfPLz8gX/Cff+Eca7cP5v2z5b5ZLfG0MaCCbsQhV2Qwi56Ul3FfM4khZxW1UktysH1nOUpy27rHutJStMwlDgHE1qjxcYK'
        b'B5eDSehi7iNTG7FIEj1FMqJqYqOwdexc/8DW976t70CW3DaItg2apFjmfAXXQxzTmfjIxllSgmpj40nbeIo5j+zdpEbScrm9H23vJ1ZTmFmLVSe1UTLf6FGWzjLnYLlF'
        b'CG0RIjMOUZhbdVq0qikcuT2htKNvqwptYKdw5kkjexb2LKad/fEDB4WTu9S7J4F2CqadwmVO+Xf9x+3HgujoHDo6HwewV9jxJbrS8v5VtEAJ8SEsptaOnUW0tbfMOn8g'
        b'dyRyeOHIhvFyeXg27ZdD++UzsnWURHYu7CykrQW0tZC2DkRhR+Lueo8mjKbSoSl0aCYdmkOHMoGtHCTenQmdqbSVJ20VTFvNo62iZVar764ZLx5bN7aJxhiZMnr+Cnr+'
        b'ahRec0biXkziOJUJe1cpq8e8x4a2F9L2+JGewsYW/Wij8Bi+KSROa6zC0q4zuDOsNQZjDDQ79WRmIVKnfm6/B+0ecldlTOu+aaLMNJFwoCyQ2yykbRbKzBYq7F16LCYp'
        b'tslyFuOKVRUEnFXfuUluKaAtBQOG9y19ZJY+jxwEMs9lcodK2qFSZlU5yaGshBPGZq1JR5IkQvSvvmd9d3hPuNzYBz9qTVLYuRCZOnhK+ANqAzXDmrRXBO01n/ZKHi+V'
        b'O2TRDlnIX1+piYHM/uW0IJwWxNGCpPFsuV0mbZeJ409Y2kvsO4M6w3CzExAH9RJTiyNraFNX2tSdNvWUCRNkpvhPwRdKcweih+cPJ991HHMddxnzlPMzaX6mWIU2c0f1'
        b'6gyjLfkDc+9bBsgsAxRWdjIrAW0lGHCQW/kyl7jVbsbttJylEIRIV45Ej8aNJtGhybLQQll6Fp2eS6cvpNMLZUtK5YIyWlCGESNMa9WlzBJZkwaUuwB3JpePLB0lMZIY'
        b'6dwBdr9Fvw0D4pJbBtGWQbgSnsR5tiYD4TLTKPSnEPgikWQN5w0vviscCxj3HwuXC7JoQRauCO+FFUEtzHPAR45xQfgSV2QjrkgpS+ERJE0ZcRx1GeXRwYmy4MXjJffK'
        b'71XeWyUrXCr3KKE9SlAlUqYrEY0rwfPElXBVWNsyg4f5JKVtGETObXhgyrtvypMmyk0DaNMATLKTxnpk4ypzS5HbpNI2qTKzVIWpPaEscpKbeqJaYdYed4W96znrU9bd'
        b'tj22YjXUw61dxflStQHjgbIBHWYAw0m5KxzcJGbIGyMGVUyCiCPmKGzcxVVPRws0KnaufWDrc9/WZyBYbjuPtp2Hq1rEeuTAk3DHje+Zj6N/suw8OnuxDP15FMgdCmmH'
        b'QplVocIvUKzSqSUR9syTm/nIzHwmTVHFSO0m9aYynIFVMWSwKlIM4uhV+ddRK//NzINnlqdMPv/qfJOggY/YohgaHzTlpEWxWCxbjFr5jzv/KRQMQe+c0gykRvQi1Tj/'
        b'SR7j2SKaIjG+gGkvnpIYe0/t3pLtTw+7sgqBnTvegRF4+QmniOif5zT+FeXcgcvZy/615RzA5cRb2Ew5LXE5lVuFdpWls0r0KwpTgQrTy3qoUVTC7CT/ujIN4TJdmZad'
        b'PaEdJVyb5XYkQUye+xtKxmU91C2a3kctqvyVxbuKi6cxLTKXSLv6VZU19WUv4OD998q4gymjTtHUrtmvLuJ1XMQ500V0xxIU1SERkh256c2431ZMLMpa3V/d4kZn9wxB'
        b'VjU+nmFVeTXhQbYrXlpdXzfrtId/t3zluHxnqF9bvjuzy2eZPft0gn+zMGQY6f/VhQG4MBenC2PxtDBRCdG/STCXf3VZfj9LMLVD1K8an0imzqxfm+k4ztSFNSUAt+wX'
        b'nFkxxQ3+G1SDupsWITkuwpTDv66If8CzId5r20KJszuLtsxsOITJmBm8fttgoMGUrq7615Xt9dlDqbmSFfs3lah8aghdWlyFQQ9F1avLVv26YslnD6GBuFg4FWaPvmom'
        b'VOhZmvXfqGW96VKXVFWLyn5dsWlc7PvUrGLjZH5Tsf/vz4CrePYMuGlJzkA9cFIrNc/tVBHh1dPtY+zjuRHTB7ptMw98g3JpZn8QIOKymLXfIXjKD7SAHWZTS5bK9UrQ'
        b'DoZfcI6bKyaPNH7mXbOqbJVyaUOfYpY2quJYlJnVkUaZgcOvPLLtH2fwAPfeCkoJ014Rx/rfOK/t/7EGsOxfaQAqqdmVc8zZKiIs46pN146/Gr0usMt+p7d4q5BD6d1l'
        b'5/3hL4xCntfvetYLviWWVldXKRWso1RwLVFwa92v1O4/Sf7hLPXW/B+oFyPe8ALf14eoKcQbUrCKEvGm0cRSHjbCYN6oJn0l3o2NVP/MgSIbOZovUObzCDikXvYmjlL1'
        b'L/T7x30fq0L4jOptUwlyY84a2IWhFgzOIgQeYTlVJBK8kZqWqksGhTQTsURHL4NPET5D1zUqIr1aTRz4lCe4zhLAa5UEk3LST3VTJIeETua4WlGEdVwftMEmstHDsDlj'
        b'2vS9SegiFTOpZ6Zn5nvyc9lUYYQ66Bb6EsA2uA06wZakRIylAPs9E1MK4pS7eqqUe4kqOB+jpN3cUa4hWp3KIEfgLi3WEgNwiYB7UFq+DAUFBxxjhilCQQFPg/0EhQEu'
        b'gmOheBuK7Jqp8GEHOMkCF2rAReZEzFFwHjTxlESfwgoW3OoNe0jMYrgTnGOW1UGrMBXuZeGF9bL14GA2k3KXI2gha9eootv5CSqUpjob7Adb9Yjw2HBgFUMhoaLiuxBv'
        b'je23IGilWNANDvEECR6B4DaXr0ZpBrHBGdgGdpACrYeH1GCLknvKQ5UFesEoqivZiOkvAjdhCz+VLIKrFbDXgy0m5fBEvTP23F2kmgT3J+DTspKRNI/CXiJ4hpeaF6YK'
        b'94l0ZjVr7almvRc3a61ZzXp2o546N+d/p0E/N5ZpvaBB81NJs6VYKgQclV7VoJMdv4ohg4XH4fZVmCmGDUerlERM6NmdKabYbfA4ZrrAXOkHlGQWBpsZINlhXbiFl5PB'
        b'7KVMaRzsMiYaBc0sDxFmuCgBbWSDdS5sZng/z/LBJTgSLsLcGWwNlnUBaCMecWDPSigpmSbQ8QS7w5i2c8Ybk82QjVV7eFpJHITm2+v1yl2VPngJtpB9SLAbXmFon/Jj'
        b'CLbJCTTDk1OsT6rwMCF+MuCY1MPzBIJIAH7FYBeQZnmCa+janrKH+4q4qiTtNeAAHJyKXRAwFTmBR5pfxkbCzIa5l7KcGfYlNjhBuhpoSQR3eKhp9T1L/OQfR3opLzOW'
        b'0ElhMim4TwXzSdVUkwMgsvLBdR7KT4D6mYALtgFM6M6iHMBO1SDUY/YQmbBQwQYY/iZbIMEUToS/6Ry4RkqmmVisZAdBbV+DDSUbTDeCXgLIWjI/ewbHyEL3ZzhGkmEv'
        b'6SKp4KQ14aJJJrvoHrqwGw1MYA/pTi55qivAdtSZ8CkQpjaFrtEY+vFPOFZSwVZ12NqIBgsyQl2qgGeYIaoBtBJ8m50rkbd7heP0wRX4JWpLEhmgHIzr8d5hLexbPzX+'
        b'CUD3U1iDcgCEB8AWkowfPJoxNYyBHUitKnw0jFmAgwREFwAugONJmJAGnCxnqHyQ/g+QRrhcWMAQ6PNWKtlqLtuTrmAEz6bOHE5ADzhhAtozGSjfHf4KZhyCYriL4cED'
        b'O91Iip7gArwDW+aGoHisQAruh72RTA/ZBtvm8lL4XLZdI6VSjAZT43KmQbeAa+tQu4rnexCCw53gDDjK3rDWlTQPr1AoncHqogeuPCV20bSD15he3bvKThnIEFzDdEsV'
        b'HH0wvJJMJEE5+szgx4I7yPj37Ni3PEgJKASH8hLAZR/QAgfXqFAsKKXgufXLSOlDNaFU5F8IL6vhbVMKtIYCKYEuwoEK1CMPw+twF/LyoDyyVMg0aJmpRaGIGksqKj2a'
        b'86MYyuEvLRh+6gjNVVUnNSKYh3AtA+K081ino73Ch3nIKdNlGIvNSqtU0Yc1efh2oiaehr3S1633+LPIdvabCHtqJMRSS0IDJ/5IKkAvmRtYq1mlVC51jMWi9mqWTi/u'
        b'kBcwNqEDfshaI8Lx7ZivpB80QyvKVpWtXV07b33os2vEdWW1RUVPuYDJPUFez+AHnopdponezzCM9lP0bwsli1mC/7Ky72bcXTjupLyd8ccAq8OxUA6Y8jCGEvXGw3zB'
        b'4nkJhHMpMSOdnxv/dCab1iQYYmuxMPioT2cJut9Gmk5sIdiL5mguH+6ZBsdoblKnrHJUQD+83FhZzO9QES3gUNTBP0XcyktK+3OEQWHI5a6xdXfstu6Y1Lh0dF736ojP'
        b'dkY7729rXR8RVqd94WD6R/FhkkeL9K8kLhKYZKYFZV/v2f3z2H6jxi/qXZZk9MZP/Km9+uMf16wZtQ+/F32qdcX7dXrjbZv+3mZ07k+uij9Sm3Yv/b3JuZQ24ZtXVu7r'
        b'W3xG80RgGigyydWM84hdcji5+5Vd41+YG+T81PbTNuf2xCvaA5y9bQa5mQs6qjcue/fQacd5B1/zOxvE/8Pkg3cEhzx+FxGUF1nw6gFWi01xgjZvu3vL8ZWp5dEn9278'
        b'7m8nQ9ij3JMBR7pMcvWKPWJlGmqfnT14Y9277we/cYHdcazm61TNACrjyU/qH649dm6Be09Ud/mdmFbbdYVfuAh/KNMxvei/pd16z/Wc8Y9OJHbeOO+Srr/evWnpo77U'
        b'9ZVXi6KD6s/Pa17zHfugeWjtqVc/e/9zi680hJs+UUuvNPvrqk0b3Ifv0uNjb2/4OMdXPfxvDrVf/e7z17T+cvUVD80LzSHL9n08kf8HR72lmpI3jd/qlEqHZHvOLXxY'
        b'WPxfkv2PtlW2azYu6Mhl/5X1tjC65sugL7RXjhV8M/JJ7Ec6f1jAL52vJlnRnbCj7difT2y7mPTpDxpdl+fKbO6tletZdH1zqiVLbDEnC0Z7pkQGONe9Ee15+p6osE51'
        b'3+uNcoHFynU/LTSR+8VkZET1n257WHhG992XX8t6cMfrq+NvnR2/4dr/4+G2tUfLvuAHeH5690gj1/IT3QPvLDh0iP/utkbR8U+WXv6YfaHhvTtvs1T1nd7Z4PHO3+98'
        b'BW5esxO+YlaTO7b+0x+3DX2smhtRAbve2u97oWvjl+ZrLxn/6PpheMe9cy22jz41NX93894vWgWv7Fln+K3vy3sGjwlO7jux+jvjx4WZwoddxz/7+9bgOueeLzRzhV9V'
        b'/jC39kZ35znvWr2PrNq/2ffZxe9e/vnijzF+l9b/cr6++Ms/XxN9NWdTwLe+uV99Cbm3zL/eYDMfJp6zazwoeOm/xs/Hm35Qp7b456AP+1WDaKuvv+sYDM+9sOvH12Xf'
        b'pMm+3m75rufmz/74oPNvP+vltq+a+Nrzjz9R897b/X5Wof17X7JG7736ljCDdecc1PjwxMcmEZ87/Ox+/kl27hXd3OI3jUyyV66vCP+Lb+qR7yRfH/sq5T2/uAVffHMi'
        b'vSjE4cEe9rt7BXeyvjrU8+5Pqn83Dxx7eTU3iIGn3NKNwG8VQKqyBI6Q+WIUDDKoJHDOMdsyUxuztmm6oQ8C9NJrCM5xQGcm3MKQqm0HgxHa7lw4SOD0GmArvGPJzt1c'
        b'xUDbRp3BZfRh0SOaJmcsBH3ESwMcacTYNjjM0ZvHYNsWg2sMjvJWsBdGIbqx4BHYxaAQ8+EIAY+VwUFwhwDf3NhwBO6ZQr71aTGgls51mL2KvJ3pofyYtzO4M0dJ4pZu'
        b'oh2I3h1QdWqSPblqlC4K5wJbzQnhGTyZit4EMvHJNi/kZrRRkm8a5VSCYd5TkkQ0eO1ZwojyJhyGp6aBbyqGrMo5hbZ+DDyowwiegCN52oQTi53NmucTT1jCAj3RPD2U'
        b'ljfNL2pXRkpraB6nZACFV8FVzALKcIAOWBMB8kGPl4iQaepkKuk04fZYBkt2RA/eECVjpeDx90pkkiqlpcMGEnixiBFTN+ivIpywHvj8g362IbguBK2wmRFTL2yHpxiu'
        b'XszUuwo0Y7LeYrCVRF5bHTnFAspwgNqgnK/AIxSDOes1hUOEQ5QhEI1JhSfRp5qE0ezwvBQkXEyxu5fjmUKpBLHAZadchi0ZfVKeYJhLCW8p7IB9lexKeB4cU2JTswxF'
        b'cE9CAryWxKbU4RZRDdu92IBkOgdch30MfSTmjtTLSmTnw0Ogk1THE95cjbFfNehN0ASeQFrXymODG3CbK6lOanWUNuhdTUgSVUEHCzQ7wUtADLsZrXWZp4Ej4DYBjxHo'
        b'GMeBNAJL0JuonZjCUwPXDNCnyA0WOJjmQ6SfbViDvzU0BUkCzDd3axWHMgNXVAJQT7hA4HWwJytShA+5YCjgphkmjdEbOTxsBbcy4Ok78Bim4jyg/kIeSNBWweh6H7yN'
        b'viqUvImYNbEM3sbEieBcLKmfX2HpNOBXdSMLDKNW0QY6wB2yWsgFI2naKqkv4FW2gCeYIeAmvLphmsiyBB7FXJaExzJNm0jCJwW2adfrarI3gz6KY8+KRPn3KbtDgQGm'
        b'BMXoXEo1lmXsg0o7HMj4nVwGLmljoj/kreT6q4BSho5PvGiZKGDVNKFxOOghOa0Fx9O0ldA/tblsnzAHU7iHabI7NeB27adkehp1phQ7A3QBKaPFO+Yx2pgbkBegZAfM'
        b'iWDIMg+K4A4ROJPxAnJATS6JWw0O54NLYHCKyM/GGSkIv8AkL0t6hsQPdILLhMhPJRgcTWAOwToCdgcRFj9C4ZdZY5TYQJqsBTwND2FLK9T2UEXVzV2S2PZu4CLxzEAt'
        b'8CwcwpSCJmgEVLIK9s4jkosKAl3TuHgMip8PbvNDRAzm8iCUBMIWj1Q0VsMDgvUohDbqu/CiqzkDM+8BR/F5gCgAXvwAfeHkBLKLbFSag2A7kX6NVsPGVB56WUdvraCb'
        b'lV6hBBWDXbzNvDQPSKgHUYe/nqROacPbbHgNjKSTykY3lmiDEW13uJ+DTdN8wQC8Soql5g/2iMC55BkoaYKRhoNBDOHqqSzYqzQUIEYC7aj604YCq0Av1/7/Hir4r2A6'
        b'7KlnKQJfACskb/EPtZ6+m6/n/suv8WTJNgF9HHzPvLRPxsSzKA+/SaqaZe3xmLgSdYWzx7nFpxZ3F/YUStgKR1epz6lgSbCCL5TEKTx8JLGS2Inpa4W7N+0eIlGfcHSW'
        b'LO+ZN4l6cBxrIG+4kLlS8HwG/EfiLofTvGiaF0fzkmheuoy3QZa9SLZ4qaxshXzxCjq7is6uprPr6OwGOnuDJEbhypPW9a+77xoocw1UBIaNrBlQlaopPIS0R+hI7t2y'
        b'64W0RzLtkUd7LKI9lkyisX8RW1a6gi6tk9U3otvNrBj2Y4pag36eoCmfFcv8pDM/uczPIraELfHr1lTwfQdyR8ovF9H8WJofT/NTaH6mjL9JllsgKyyVVayUF66kc1fR'
        b'uTV07ho6dx2duwlF9O/WIhH7iwgrVzSKKeOXjM+XZeffS6OTC+nkEmUod+8Bl35P2j0SydUrAPPmRCKfoG5dhTsWtYewPw1zvkWxGBfV3s2jX1OqP5D5wHXefdd5ctcI'
        b'2jVikmI5R7EUbp6X9Pr0BuqG18ndImm3SJlb5Pco1QGUjkC6rj9FwfXqt6a5Iahs/QU0P1zBE1wK7AtE8fr1aLcQFHykdtbNpCrHz+UxxfFwfYKd79QoN/6p+u6GnoZJ'
        b'dY5HwKQaJQyY1KF8giYt9bwdHlPIeYIdpgqTNlTAvJGKcTX5vFTaP432z6Ixld0ipIOASLasqFxWsUpW0yCvaKCL1tJFjUjwS1iRWPDhcjuhwj9spHy4mvaPJ3Gzaf88'
        b'2n/xlGcoPiat7HdpdGg2HbqADl1Eh2JVh8ViVcuqRLI1jfKqRrp0A126WallCVvmiFn7JpAUbGnuPJobJeNm3K0YWyHBYE8kQ/tClrS8fwVzpRAGobbpMsq7u2a8fGyT'
        b'XJhLC3NlCwvkwgJJlGRtd/KEq6Bng0RFERBCB8ynA5JlAaWy9ExZVgmdXorzEsrtfJGkkZxpfoyMnznOHve/pzXVOrxx24h8ereI5ocp7wQ+/cv7q2WC5Ltz7s4fs0RP'
        b'A7q1cRisMxk/5a7P3fKxYGVghgowFN35dmvgQAv7C5VensL+9f2b0U1gt86EX+jw4uEi2i9B5lc6nocZFovoFFROyTy5nQ9uGDZICl4+jOZQB8YFQu12Ps1PlmgpHPlY'
        b'KCkshZOLZF1PygOnwPtOgSMWD4IS7gclyIOS6KAkuVMy7ZQsc0pWePphUrQ4HIOcVY9cyfzZMU1HrR4EJd1HsYJS6KAUuVMq7ZQqI38478VMboyLRpFZcU1GX5wvztrL'
        b'b0B1YOmI+fBKuVcM7RWjrA6uHs0NQzUMCBteN7xJFlAwPkeWvJhOKJjWlKOzzMWfdgx4TFnaF7FGlKDM9AJZaIE8tGDSgPL0lnlH0oKoB4L4+4L4cSO5IIUWpEjmT7jz'
        b'pY7Sil6Pfo8Rw/vuwTL34KmeWCt3C6bdgmVuwZMciid4NhhqQdKanvUPXIPuuwbJXUNo15BJSh315Lvq46wxrQcRmfcjMuUR2XRENvMcdbgoVgJr3HDMYjxPlpN7L1/m'
        b'Nk+qPsDq1RqYPxJ5ORH1aKlQ2tAb2h864n2fFyrjhSqEwddCBkMuhw2HSWPQDS2MpYWJSLR8NGKERQ6wB/wva024uktE0oDuDT0bBmqYkXUkayTrrinO6nrRaJEsPeN+'
        b'WIYsLAONJyOsYa0HXlH3vaIYIaO6zctkKRLSZRmZ9yweJCy6n7BInlCAhMv4THgHjhgOW4zU3veORCK8mzeeMZb/IDbvfmyePHYhHbsQPVSEx4zUK9eCFhQhVx6zhEZu'
        b'+BI6fImULeOFyN1CZW6hE24CLFlZwCKsSkKip1TkYw6LW4RZhZA7ybhqFM+nX4CGUXfvfl6/gHYPk7nn3TUds6QjM+nIPOJBuwfT7uHo0tEdN7cklrSC+VUERdx1lQUm'
        b'os6+Ue7kN+EWINWXBcbL3NLQ33gU8ytRnfAKkKj26CpceBJt/K9be7KIgydKZtKceU7jQ826taVldcWVVaKH6kV1a5cWi8p+C9pTeWLjzNmf2TXNVaWoXzHrc/BKXQdF'
        b'QJ9ozo+OZ7FYdnjv9Lc7/6nN168xyPOEpi81rBfJ5nA5jIV4y5x05swU5sQUsGMhBxzyIut/UfVJjBdomgYqWIDT4Ao8owJaDDLrGQMdcNkavRgegAc80FfmjQQ+2JOm'
        b'TNA2RAW9XTencNnMsndvAzgzMzONFM5mcIwsMsNjq2HHi3KDV+Ewyg2cSCJnTov04RketgO74BafIkhIyViNzWky4snew3x4IgW9Ty8x0XACHTFk40OkkTZlqg6kDV5+'
        b'LGKpDtpAF+GfwGcBgOYkuI+PvvmzSVrefhnxiR5gfzQpZrCTGgX2AynJPE4/Dr1Z78OLp+gFOY/J2k25rSCIwxsLi0GHhr457CKygfsMbKdEcwW0PCcaeB321/tQ5JSX'
        b'XtAvmpVeUmqO8nxpXDf8mV++ORNs00CfGedgC+kOlQOTeaoiGw5FCbXudOWmVL8RYfCo3urlomajgMoOl5WZt7tlP2+14dVMNO3YEfOm1oVtikT72j6bvm9YO3Zsd6c5'
        b'0mM2tRGLf5g/Yv960y9g7PHFW49dNDxi/2T9x0bh1+VvfXvsVfVfNMGnc/bdNH68wrbgU/U7UWMGvz/0xfyml1cY6XIvVk/enHszvUQ89/v9n22InazZq6cV8+On+mtM'
        b'15rsOKZX2GXkui96z/J77aygiKsPHD5oMAvdN/rJwOvDCQk5HO9StbOGJfo/+/le5Bxr/+TV/ITetj7W34q0u176eaF3ufC7crO/nBwcrF24UPPAaysd90kCCt86lPHG'
        b'iV7NQNfeck7ozrN0zpLF19l3jx4Wf1Q2UpzzlfTDMBBldcfLtnhBx0vxJjsKnJs/1Tza53DKcd2n5qPHJla8f9FzUNaemmdc1XIz/bX6bouv/zJ8UTo4vmcr3LO6z+Lt'
        b'o/fqSop3dFgVv8rKWH7dPff3fdxcrTLqL64Ltmrs6/XLWffkkPnvDIWfPsw8+/lPb21ee5EXdqzcNu1+5oHbr/P25p5aTzflni6n9wdnBHx1uvBdF96Xrw04cR/MDRZ7'
        b'7fyL7OZ+h0Hd7x7eO3LT+4GldvDN3zVs1W+a+0bZyeKDC2PC96+Lbhyw/lFclxXz+Z62919hi1b2fS5ap7inV5hyzukLrlvF/RMR7mezkk3uTUZ1vl832b470X9hc/vG'
        b'L/wUt99PC6zL7vD+ZHXLpfc2lbz9ecn7Pi1BPZty4lsFwvbGtdt/1N2fnSz54PMnb4eua270mKP2eqB2f6btcPXiyiEzUcf17dbl+/3Xxm2Ojt614FXZ4Xfmn/+62lq8'
        b'd9GGgOv7jE0rXxVrh352t/Mdw667yfp/6O//7JGqno5MFjZ6/GOtm41L885+97WbX14R58PtH81Lf82/6OSpicY1l+J6jExyJdEmP6TTj977evCA3rzdhW9Xpr211On8'
        b'zaON5xqfHJz84iWdtrf7x66r+GStOFEpu1drGPbaovXLX37XgjVv8+uLb8ALhwt6Rj6stpNe/o591r9/l19u4/nD9blhXfN+uXVkd9nrRUdP/v6Tzzdo/zFtUci53T/q'
        b'FCzVKar4JPy9745Lzo1/9gtrQZGeKDqD6/XEE/eyJnDA6AUGeFfQ9/GzBppF8CZZtpgHtuBzFXnKI3GumAAJNgndD7eQL/358Iq6cmWWUvGPwtvho2ALc3gYOF8Bu54x'
        b'SMwCezgZ4LAfWSzJA/0cZhWVUqnIWM6Cu8C1NcTqcYkNOMPYq14Hnc+dbwYvgR7QQvKwFcI7M5ayyDrWXDeVAHAVbmP4+neAM2AEH3IOdlIUPuQctG4kiwj+EUvIkpmD'
        b'EVk0g63gEMk7NQwcJqsmByvwSgCuORxmzleBbSpgGFwFW5iDBI6ZJWu7W8fwmAOsUP20jdhwO7gDtjNLiTv14AVsC1+DD5BsYIHjFrDTcjPJ3BLsWQ1OuOOzohhDzDrm'
        b'0CrQbQ5HRHAPOIZPD4IHUhtQCK0GNjgPT4ArTI0Og/2RIsYMnAN28sxZ66t9SaJV8Ey+toCrBrespth5rBA7uJs5ZeaCD7hmEC2aXq2CfeAssxhzoNRtyqK3HlzGRr3E'
        b'ohcOxZOVuVXwPLhOTh3DRuhHIZqGWGDbZqUF5gYbe+3pZblbeTNW5labM60jX2Xmwl4uElQbuMIlNV2QVgG3BWMDzOeML0+CHuVxKCvXMOtPqIFeJGtQSWx70DZXKQc9'
        b'0D1jrW1drYPQncRTh+I0EdLdAWwky0Gx9+SzwAFwhCFtUBHCXmw7vg8vcnOQPk+64hOCrZgVpCbQDo9qC1JqmRB1KFNDY7gjmbPcK4VZmD4Mblfg5Vgu3LecCExDl10K'
        b'9y9i2nz3Yi4cSuKsnnHSGj5lDQ6Ay4yN9Hl3DFF4htkBnrB9ntkBSqoYS/rupGrUUgPBHrJAPLU6DIZriJBr4V6/WcvDc7PgpSgrstzlUAtOkyVgvP5bu5wFDkYJiPDS'
        b'FwcnTb1kqBWxQwvcrYGUsSO+qAl344UuLmyfWuuaXucKzidZlnjyYUsS03HT4HnYx4Jb4LkK5nCpm6BzDm/6tLZaLrbZPQOGlCcOof64leXBe+7EQTCYRpYsTYXRM5gK'
        b'yGonizIrA4PglooD3J3ASOS4LtJbC5Id3At2kNapEche6g7OkF0ScE4PhcfeNnWz36dszVRQ2z8NbjDK2umyFrVPPriBmijSNz70SSuZDVrhtXAyFIQgZV9ACeEXKNA8'
        b'hZ+A23Txm45XvpqRPzxITin0B/1ocH2xafPKZf7orYsYNqNGeJnk7B079V6UwM9Fw94ecECd0svneINda5gq3FoQmjSdLdga/hS5AZtUwbAevEISckRD0wGcVBpsThYI'
        b'c3GOKCUOx97IghmE+uaaThN+qBWyoyscYQdS7v/kauV/f1DJb1ytfIYqmPlgcWK/yCKNfLCQJck5avjjRLkmuTaORdk4dBZMUvkcQ6fHxG2NVZqZLuSYoEfYFasq7N3O'
        b'WZ2y6rbpsRGrYdvVcNrSc8D/vmWQzDIIfe+LY8QxCmsHYpA7kHvfOkRmHaJwdMKPP8KmqPPHne950omFcs9CuUMR7VAksyqaEAbSwhhamCATVo7n/jH/1XzZgmXylEo6'
        b'pVKsJrP1lJt5KXjeUv8B52HusOCu8xh3PI6OypLzsmletixvkZy3SKwmXis3c1NwBTQ3hOZGyLi5d+NeTgSJ42vkMbl0TC4KsKZdTyEQ9q+UCaJH6mT8ClQSPp24WLak'
        b'/H5iOfJfLzdzV/ACpWEjJqOWozZ0ELZ45WXRvKyp1B1ce/i0gw/tECBzyBzxGw2jQ1LokEyxuoLrL7UeaLirIufG0txYGXfh+FxZ+gI6YaEyX55XfxBZU5LxUu+qjmmO'
        b'6SnTnLBz7tGj7YRIslwBXlAJlXEz76q9rAW0xv3lEZl0RKYyCRRQm7bzQgFtnbDdZKBUdcB42Pa+W4TMLULh5H4u8VSitEHuFEA7BYhjFe6eKF5Duz4S7vA8WhhPC1Np'
        b'YQYtzJ0S6QRSrhWx2cRrNLYBk5Sauc1IHPmZsHPp0SblUuArlC26pO0Cn94F03bh+E6nR5+285XZJY2ojmqP6tGBSZOaqoE24ji8AmTlO6m3mmWOPtv/o24ph3J270ml'
        b'nYLEmgoXrqRE6tzPp91DZe6pdznoX8Lv9Mb05C5ptEuaWHvC0pa29MNm8aUshStPUieN7W7saZS5xg6suBs5WC2OF8dPqlFuHsgngfYIoz2iaY/5tEeyzGOpDFsNF9Dp'
        b'S+WuJbRriTh+wtJxkjI1T2BNCHwH8vB6Yv5d8zEbOjKHjswXx0kC2tMUfOFAXH+hjL9oZN3oJjo8lw5fhHz821MVju6SAGnwwDqZYxL6uxvH/KL+wvWQGkkX9tr022Aj'
        b'e4WTUJKmsPOa5LCdwxSBoeM8Bd97UhXdTFLImfALeXojjp3UoPj+4tjOFHGKwtpOnCUxby/sLJTW3Lf2kll7feTkJrWQWijsuCg192iWwtsPG+9ethy2VHgEoHTQM5QQ'
        b'cidCImfePkapx7CeEFcci7JRoxx4k5Q6rjsun8w3Bi+Q57HGY8ZjZBm5ryTdS1JEJOHDKPJYjI8iLWfmLUmD78MUlRkL5A7xtEO8zAorwM6pc90DW+F9W+FAotw2nLYN'
        b'f0zZmOfhBSdXD9olQOYSMeInnq+wdencSNt6P6YsrFEWnkKJao+Owi9Cokrb+UwERYza0kEp4w33NuIDJgKX4sd+SPA9YbSj34jxqIXMMRr9KdwF/e4DecMFtN982j1e'
        b'Eq0QBEtL+qtkghj0N5LL/E5SRqT02JWyFZ4+UtGAT29DfwNeCsthPfKZJwvPkvtk0z7ZMo/sSS3Ky4f2jEBNjevHBBb2ru1fO2Lft0G64ZF/lCx6kdx/Me2/WOa1eJJD'
        b'eYVO8D1p/ryRGpofeTd7rOg+P1vGz1Z4+E6ERIzOexCSdj8kTR6SQYdkIJVwF7IYtzdJGjPgrPD0lW68qyfLzJVF4D/F/ISxRllWHj1/wYDqsN5Indwr5nuFG1+q+o0a'
        b'5RkiC8mRC3JpQa7MLXfCxlGsjf+1az8WqeFRfZKDh3tm6J+xtmbA2BIsUH3OoODfnb0Mnltb+xcmq0fYJqF3eiWtARslWOKFsP+48x+zavgbrtJlbL1nVrsdX+/Azk7s'
        b'/IychyZFmMO2pI5ZKizChLWVqyqIDXntLuxIsLGXGwcFVVfaBD/UmWmC+1B7hrFrrQ8OjYHltb9gZx925qDcH2pO2+g9VFcaxD3UmWmH9lB3ln0XMfwh9iFEIf+xk9r+'
        b'haaBX8JfcODBVPs4q4LaxyzK7wDcLNBHKDXruAMdfNwBdqwoZ65Mx35C17gpT+ws4YgtpWUD0SPGI/V3s0ZWjPvJMvNkCxbJMhbLCpfKSitly1fKSlbJAqtl/NUy3Rq5'
        b'bg2tWzPJLmLpBk1S/1MuPsuglvU0oxjOrEMG5uNDBhLwSIzcJ8RtikHDoYWD2ExhwJcZ8BXGeF6wEKIgFsIn2GlKRAFMbVuXKQzcZQbuCmM8xpsGoQCmQU+w0zQfBbBy'
        b'EqNcPGUGngrjUBTAah4KYDXvCXaaklEAS0exm8JAIDMQKIwjUADLKFwM5D4hblMSCjOzqDG4qHGkqHGkqHFMUWeGwUU1xkU1xkU1FpIARpatKCMXmYGLwtgLBTDyQQGM'
        b'fJ5gpyn6mRTwBGVMpibkPiEuScTMrnWtwoAnM+ApjOehMGYROAxynxC3CU8v5vZiDYWBh8zAgymJOS6JOS6JubAp4RmheWKheWOheWOheT8ntFQstHScC3KfEJfIzdpZ'
        b'HK8w8JIZeDFhrEkYaxIGuU0pkxosXfQK8QJHjaVrha+ec9QWcfDpC/8bLgMXxt8Y9nA3PCl65vOt2oNFmUOpSlk4vDQLKj3N+7wNOW3qxCYPc/hTSqMtzXL1afs8lf9x'
        b'+7zyFxlpPWufV5lan4rucuAlL6GXr4+/t58QXAMDdXW1a2rqRejzdwBi2NVV9Nl9BQ7pa+gYgAtaepq62uibtQnshYdgW1Y6PAiP5apS8CK8rq0N99gR0cEB0GEAWxbl'
        b'Ybg1zxMe4MEDsIVDGcEuDrwBm8IZmDtG5e+OAocwxNyb8lYDV+vxisCcfCEJjxwO3LMAbKtFES/hiHfArno8FoKtmw05XCEaEH0oH7gL9pF4bKd1U/lxYNNaJh7JcBBK'
        b'mBx3YP7KNnhayMbAduF8eJkx0tkJ261RdjxPJy8UmUUZO6NoEUEkkgHoCwdnQb8Qic6X8gWjsJlktxR94PcQPDnJUrSBMwfl14IighMLSDFNeCHgJsoMtRM/yi8I7CDb'
        b'L7ZzHJjqoUhqYCeHTRkboUhZYISxaTgLWhvhTXBRiF46/Cl/0ArOECpoeAm0E5QniomiguNwO47LwhXsBFsJD3ha3eLqDUI0IwRQAbAbbiWGNMGx4ICynOB8kjroRnIB'
        b'14k8o+uxpWyYdqYLvClETTiQClydRkRirAk7mWKqO1JwWz3JBzT5kDJywfHl8BqQAmzSH0QFgSEwWE/WKq861E4JBLaUg8McB6XusF0ZESdo9oJtYI8rGELqC6aCqwBD'
        b'X5zqiXexDnDANtAHLtXasZXKW7iMyNIUdMI7ZnrYjjOKivKErcTOI9UeXCP5oYiOlBnYySggK4ppJnvBXoNwcAHbIURT0XF8Egds2byAR5qkhw0HdIcy4g8Dp0gc2Fri'
        b'CtstREjZMVRMCjjG1GuvAbjCyBBXDrQYqi+dEuKACkOsfi0z2w22YSPWWCoW3ILbifGUvSU4ROSI49kGqs9Rauw67CHi2Iz6wL4scEeEtB1H4UNlxaQLqcA7eE9LC1vg'
        b'kZbJpMFRijPGjsl0bwHSQx+8LkI6n0/N1xSQXUpwuhIfE4+Cg22Y7hucjgajWOvnSPfjkrim8DiStaRShPQeT8X7gy7SrGNASymjBxzTJhyMhk51v53LSJG58NgS1P37'
        b'INZ+ApUQh3oRWb6Fp6BUqQ3k1IPtWEhMD9wVQqSbjsaU4wU2GGZMJVKJhnXMcHG6AnTDlvVxU/L1nBouSG86FUuyDULl7QM7UKmG2NgaJSnUgEgYXALiHFLi7XCwlgID'
        b'DUw8S3iF5Om7tloD9ZwhpNFkKtkb3CS9SSUM9k+1HCSG46ANR2ZUWokGIiwhRzBY6o+P90Y6TaFS8uBO0p/KYHsg04BQzBpwFQ6GMkpNhNdIvEVwVxS41ACHkE5TqVRN'
        b'eITRyknUZ/dPtyL1jfAKODWlFRYYYIaoO+AOD3SWwyGk0TQqDV7iklo6o+JeVjYk2ySeuv1UvxrOJLVMXF5ciFWClJlOpTeADkY258OqmczAQXAyarpTga1mTGsXg8PZ'
        b'/DpsmplBZQTDThJriciUaTxbk4twI8BlbEOxPMBtZVMPngNuwMvaSIuZVGYD3McQ3x9jwaNEKlurMnG80KncpEuY8RA0+XvAbm025lfIWoYGBAKjPOnZCFvANiNlw1GO'
        b'4Ertw50LGLlcBsOVm8BtbaTGbCobDZDNxBYP3MhDfa3FDTOxK/WpjE5UmQ/amIr2g3ONC0O1kSZzqBwLMEQGuXJ4wIaEBttrUZqDzCB3fD2JkgDPge2LgVQbaTGXyl0c'
        b'wEj0ZnwsU8IUMIxqOjU3gW3zGdvMK2jyu4UG7V5tpMA8Ki8T9Q781TinNo80bA6Hgu1gl3EAjnQujVjzwbNgK2iBnfCGNtLfAmoB6tLXSJ8SoY7RrBQMB5xKQWUanZrW'
        b'nNOJNmCrRzU8Vgxa0PVCamEqaCePY+DRyo3wBGhBSsqn8tPQZEB0d9qVPR/nhpSwCLXUbnMiXpNk1Dq7wVl4GNVWQAnglWRmNjoFxC5oxuyHh1F1PClPKE0hc0bGGnvY'
        b'VpZFEWtPbyGZfcIqTeANR3gYJc2jeMlzmOKd3AC7YBM8k4Vk70w5J+eTsKahpWss4GFUXS/KSwMcImG9Mpcj+R2ChxmzN3CSTQq3BrTC/hR4KAuVzYVygVvhLa4WMy6f'
        b'BRfATWZwROIBOxbh4YrM3m5o2iTMEl3geurTt5BB0DI148K2ANJuF8Ch2qmBAA6qM0MlaXzBeaSZLOLCQdJMysFRth2LiR0BrjNF6AVt66dmPNiSh9JfqhzjzyGZM0XQ'
        b'n1YiT73AHW6bGlLXoz6AW9UaJ9ihLMKpcLiVVAInUQZPMEOHmAu2MI0bJwK6YCdn6VTL60Iax9nkeAmfdiHUQW6oRylbSg28Q2qqmg8OTY0+0RimclY5xHbBK1wWc4rA'
        b'BTTSJMFmD9ic7BCPDy0Hl9hgqyq8+Ql5kWytjeBqEcvBtzaS40Uor7kdczxZ8Yw54W4/HWJj6DVXpey19HzmoUugBrEx9FIbiCor4jIPt62cQ+ENFa/CzsIlIf7MQ8Um'
        b'xr7aS+3blae8rJiHr4TqUaj0Zl5q1trccifm4dmN6vil1sArd7f+7fWxzMO4CEMKiSvQy39l9gZ2MfPwnjtjNemlxkvZZBHEPPwu0JhywxnpzeX/da2IeTgZx1hNeq1Z'
        b'SlWnWzIPIzYoq5n7gwkI8qGIHfg3dXNRA0W5CxTOIp8IisvOjiMeHVHKCuR+rAEFoUxoZxdlWdV+jjY2t6Q+6WjH/70STjL4W+aU74fFK9DL1idC8t/XzEtyQy64g7rl'
        b'XjwfUtVUNdg/n3mN2qmCXr1HuDzUg9ZSa9EEd1B5Hgye3ZLgfvR2OtXi0KRz42mbawQ3SL45gco62EgT38xVqur79SaMXFLtk5qXrJltDoq6H/MREUph3pFjVAU2BzXd'
        b'yGpmS6gX/Ye+aVD889NpHGTvNcMMRUrWj4eqlatKy9ZyOcRgtBa3YWYlBJ//NM3VgTvZehtRSfGqosqV+ECqpzahVZWiupLqlavn6WuhWHiT7PstlMwzi/m76z2gek17'
        b'UHsk8rLesN70Y/KFRyq71WYBNYDbJX9J5iLfpUiLqamVHt/8SVWE151eejlqX/afV2XNN+4yf7lmQ9XLzR+s6BSHDMuO/viT3ntvra48rnJ/rqmJ5za7zB06+uMPv1Zj'
        b'Ozo6xDaZ2tzjrPNu+571887wrR99oHhck2o4v+MjobDx0pXyb+dtsl5/dPNpSdGHX3LNVI76/mDg9K1jjFWE+FO7qL0OcVYxnYE7ipeyHcecMsd8fcY8ascyPmwuMXOd'
        b'O7B/xMayyfJyZUJWhfDq6qsmf24Kn5j//prP7X7ecbL5zhLXGtM1Rt8t8ayx/dZIf8LusYGe0YEJt8dm+43SJpweG6ca/XHCo4b9ydEnjfu+HtnSMrKjyLv5DyPbzo/s'
        b'eved4C+v5MTlPMjTfvPyj30/eViesTgb1iju2//mla/W9e0suxgQ3Oip9WbUo+9jHeJ/jmj89r2GS1HCLzcVNa45/JfcRdEXJbYPfOafFg6xfihyVduc7fD2199f3iju'
        b'SG85qxiIjFtZStf9PiNx2/08+4avrYUj73Tw3yg6/YH8tcbKH790t6wVXTnWGGUS8CeW5ps//hSaGPFDbMDCMglYt+rNW7tjzz8sf3v1lfIqcf5SI70j+3y/CfSPH7d8'
        b'VHvnpZdzLNtaY/L8qpJBWcM+c5v6kJElTuXqzi4H133X/9E2nTXvDL3//Un1N27dfmVOb5eB+tCB10oO/2VP/9gRd9XEj80qrqzYm56edtOhavH737Se3HNtkG4SfpdW'
        b'vWro4V8fjTX+9WPPa7ve+UE/YfGuyWuLdnePW5jq13/xxun3cn4qTC3qOv7avBV6IW/3Hv5g38KsbmPeh3V58bs+efTuYOTjrS+Fv1bw3e37Izn6Pz5KubQrZSD39e/e'
        b'fr9BuH/JWy7O9o6iXda9LXp+hy7oDSbcU2SLF/vzm9ePHdD/JfHVHwv+fKTHa6g289ak+WF/2PZnQcnRav5fj5S+WvbKjYD2yfX5r/DlOVff/KmgK7ezoe3VN97mXU8O'
        b'yvhG+uXCds/rf/3hg9wDD/aWel0HUtM18fk+goqOz1e+bL6J/+5X5r8c/eOBN640PHr0bWj4ua2unEPlx/64pvH4p73Faerv9E5aXjl96OLLf389/7U/fPrLT+8eeflB'
        b'3+PQDw49eem19kPyvsbk3ofHYgtaBB0PdffnWf1SvCpx58kNqu/6Or27wp+rx4Ag9i1zxnvzKclpqhS8Cq6pbmDBngYlbTq4Ag5GwxZPQlLuUq8SzwJDdasZwEk3GN6M'
        b'Biw0tyXxNcFldxalDY9z2OWgn6AHnEBXEEp4CF5D30hJaOLTYnmjD/l+Zi/7CthJ8fBol6hKlcItKqUsMJpTQfwWcEyT0vgJCR5wR2aCCqW9hg2PO8KbTGmPpIEr2Fgw'
        b'Fb1qEXtBbCwIdkYxqbauTUCJeqKiwFHYp1LPQvO31JTBmGwNtcIWewK4T5VigyFWbiw8TyriDneS6ZUxFMQxTxBTwbmgnYEoSMApuJdheCkD2zGlgBob3oKtMYxt2f5A'
        b'eDOJcC6wqDkBKqYsbGB0g4HrbEnmYq/radieDyOWWuAFBnHUCU9oFPnMPOODnO/hAju5jv/3tkW/avefjOAvNkSatcevNEV6OiWsn3FNNvbV1ZT8TXUpLMokitUUO8k2'
        b'MNNTGFiKsyY5+MqBLxUxV77hd43I1QTxVcVXxJdcEV98NalGGVohf3Xm2lGAQiiv/SJYKBC50WACaTLXJJDymglEbrSYQNrMNQmkvGYCkRsdJpAuc00CkWuKecCEJE/0'
        b'mJD6zDUJqbxmApEbAyaQIXNNAimvmUDkZg4TyIi5JoGU10wgcmPMBDJhrkkg5TUTiNzMZQKZMtckkPKaCURuzJhA5tPVMqO8hHeNFNZ2UtHsn0nb6TDYaYqfdJimrO8J'
        b'kRt50kaeeKnYRTHX8tjyQ8slRgerj1S3chRzTI7xDvHEeHvcvZUnn+NHz/FrilZY2XbGN6c0xbb6K0zMji06tOhgwZGCprgJQ+NWo9ZccenBArmhI23o2BSlsEAJh+rG'
        b'sh4Tt1UN7z7Yik3EayTF7WulatLaXk25rfeA90DJiMPlcrl5GG0eNkkFGeIY2G2NVFhYtUYrrB3EORK/9sWd2AjFJJA4YpbCzPKkVoeWxF9qL43tdR2I7OXRjv5yswDa'
        b'LEBG/hQ8FNbPBCeHXbG+ws5BrKpwdBVrKOxdJCYSkUQkFXav7Vk7YN+9QW7vS9v7TlLa5p7EEUcqHJwlxT0u4ugJW8EkxbH2xLYcNQOGvaL+QImGRGOCJ5BoKGwdJMs6'
        b'Nos3DwSOrL0vnC8TzlfYOZ/TOaUjzejW79GX6CtwMBTazlmyVKIp0ezRRD56+Kob/a9wdJMa4n89gahYZnYndTt02/U79VFpHXnSaGmmNLonTIyzEYsI5/ra7rCesAEf'
        b'uaOf3NaftvUXq+CAMahYcQMxA37SZNoxCId3xTAPZ4WV0zdqFCqjW/vKzpVSkVQ0ENi7sX/jiEjuGSW3iRZznorCr3t9z3q5vQ9t74PjxrIYFwnC1UOagaTkeGqTzDVs'
        b'xFHmGnPXSBwrsW+PF8crbO1PNnQ0SOrbN3VuQoUxs55RBTuHc+qn1KWq3Xo9ekj0Dk5idYUzV+onSZmk5ppjzWBXHKNw4Q+wuleI5yscHMXRk2wj61iWws1doqpwcT9X'
        b'eapyQHskS+4SSbtESjgKRxep4akASYDCiatwdZeoKNx40qW9GjgwVxr5/1H3HgBRHdv/+N1C77DA0pfO0qsoHUEElqIC9kJZUBQBWVDsXUEsS1EXRFkQdVFU7NjNTExM'
        b'3zWbuPHFxJdmejCa8pKX934zc3dXmom+5L3v/y/rhb0zd+7cuVPOnM85n9M5H2Xx8h2g9F0DZDV9oj5Rf/ip5WeX3w5KkAcl3Mi95SmfNPkV7xfnyKfOuD1hhnzCDJVv'
        b'UJ9rD1+apPILOxlzNKaf3Z93I6x/xhWzW5YKvwylXwbt4ijqWildqfIJUPmH9CX3ZEgn4D/G96RLJwyYUN5+z3FHNHd4BtzzC9RK1uhzS+dW0a2qW0WvG6IviqAcZZDW'
        b'RmmGwm8G6mnuPkfiuuL6PPv1zwYp3Mcr3cdjvxjUUH7BfVZ9bn1WvVF91X3V/RNPrT67Wu6XLPd46mfAG7fwQ33K0/ehGXkR8WSgGOBxN1CNNuo8ccwgNN/wLqt08fzn'
        b'AvJFmAzsCVxP70iOYD+YQUvOZezogqFtsuSIMhkMhgVG05/v8JdB739HNRkSQtdQs28jzGt6w0Lo6pPI4TT7GlViqA2dq/u/CJ07FKUaLXiqU9bo3Je1+FmYNPdlHbuE'
        b'+X/Jfskapd46WWSPabiASbEnPURSSb6/1WoHikQAtayyJLoiHzVzoU9qWk4qlvzSdKhIKAPtK3V9bOH60obANSwR3mz/cDd436vh+zubN4W7bg7Zx2Bva4m2sw3OZ722'
        b'rjai/eVbk8B2saBg5kv6LcWbHu7jRtsRhtVPOAZ7g3/lM4kIKVicKNAE4WEDsW4M01bHmY4ndBKcWTAsFJQz3Kq1rIfHYTOfOWhMYBFLI4UZFS0oLlo0j2zkV7jMw9Gp'
        b'52Fu7ie79EEZiGwWQtHUnQsmoQFqLV7SFCGOUHGs905smtiY1pImTrtn7yX3HhQ3xZYr1h80inXuMkpHG8MYQaGHKj1KT+JR+kc1ssaKgzJKPXTnT0JD1wyPxlEPf9kI'
        b'xRgxzct3DpMCCvyzsJE3mwKnwA5de6bhcniNVvK0TMnwg01ZyxyZFNMCbUZafUin+i0OdSrzdai35RsLvZZQfAZRI9uwlgoysrICApeH61L62UwR2nHIyAVVBoYUJ99B'
        b'lzLPz3jsbUWHcdj9oDDHpHLJR0oWxZyKthxKoqyaa6VD6Y99wKYS8svOjXejyrCL3M9od4X3YjfynIzf4/qs3kiJsL527Nv3cvJqfljGorgtLB2G58xTtL4vnE3pO7pg'
        b'us4y59oltEMht3DGx+j9v1ZqRBn9sopWwq3VpYw92pDMn298rtiSzvctQ/dj9ObMy00p09xewuT7UnvZx58WHGJi7S/35XgRVkyz+kQ5RxblmSw1qcylKN0ARsvEByLc'
        b'K26tsiam5D0+6ZnH6lmU1SnWJ0vHky2ICLepT8HNt81e8X8l7Z0uHUqPwQyNuUfuy+nb+DZuWl0+xV8tzyXnFh1MextNOImlvpTvmCBy6rf8nQ1oPlqePoeas9uPrt4t'
        b'cYPifCH66yNqs38DOff6lN4GxVdCdPHH1JY7vxD9rB/YiTGnNMIvFgZOwk2omUADMx0egb2lhg+7GCIMjTR9vndz7qnyvwWbe/JfcfN8b6fly6WXlpY3GH/wi+0XTb+J'
        b'uyLyOQvXcV5aoi/v6lREfH70lYawBzm/xMbenlqUnuufuK56xbLvvr3n5HJ63k2XpfGXgk7oDLhMCctv2/d9eUnWQptLGRc/27649tFV38wZj8wtkx34knFf/tJcs+Cw'
        b'+XGd9yYUdYQEvF4acHfyN5u7do7/MSJ23/x/qdrX1O87+bIwM27fv9ccA5wb+QM57fEru0U/XX9VJ0n39lstYTnKVwrmOt0z/im3LoR57nX9T985UvRaosXbk5JvBf/4'
        b'cE1gVIiOl/hv/ZKv70j1xq4r/PafR3uSTC7IAu4eW3YWGnCjrx88tEP8Y/Hm0mi/gMnjY5Z9986ve327Pj+0Y400cNuR3Xy/94RF7XeOzr4yIa059AXlT5V2rzmdMQ47'
        b'uKrx7e9Xexzi1H75+evfn3tgbZ1+7ODq6qx231t2Bde+Dlawd0suHjW8vUMV1/9TlNHNgSPb3i5pMlx73PvobzFf/bPvp2n/eq/8yyU/sF8+++FvsVEGP9yqmfHmvcA8'
        b's9VRsPt42CeCdx/n/vCj3mHZzFWv1hRF35t7vPL83yZd447dlPTvNXfyJpS8JfqkxuKTlTrNNvPif3Q8zPg6uG71vTa/Y498Nn299N0P4szmN/zT5HL+hx/Nehh7qfBC'
        b'+xm/03ftjpaEt358P83xzV6R5dtfxJm6Xg5p/PBm+Ll/zpx9+0PB4bjfWJNn9ie9Y8Q3p5UVO0E3aBfwsUumLgWvF+nOZ6LpGjaQVEuPILz7xxSGcGcoZjsUMyvgQbCN'
        b'aE9sS8AW7LeS6b8MbEXLZwgD9MID4DDxvdCD7fOJxiENlwb2wl49dHkncw08AU8T148ZCeC0qHrpUhNTsNPMDJ42XmKE5gcbeIAF9ovgIaLbcWMm0xoY2A2PocUFq2Am'
        b'TibOJtPgsWmwIRP04tmDCTYxJmZlkmvC4RmRX7pa2TETntWdwuQsZhA9SFTaGloLAhrhbgZF9CBhYB951ulwA9zilx5A366Lo0MZGDFBc0A67WeyAV5yQ9fyA7D7B+gF'
        b'p3Tzme68GFq9cjoqSkMelQtPYP6oMHg5nBQbNz7cD7bBE6jgurQMtEAagVNMuD8widZdbYAXTARpmbiFuQzUwHOYxel0oaDZCpzSLqtrJuFVtRhsJLUJh2JwnJB6ZvB1'
        b'USPpRjM54DTo49v+H3hSEA7up/hLqNUpT1bKFYP+Jkv2Cyz1AlkyicE2sRugnnYwpKzt6iaozKzkZi4qW4e9K5pWSD0UOEiUt5iNT6xsWimNVNj6KW398AmeeLmU07i2'
        b'Za2Yfd/CTsyVeEh1FBZeSguvAcrfxF7mpuJw96Y1pUkKO0rbSlsXtS+ShfTlKiNSxGkKzkQlZ6KYobLiiKeIC8RTWiIkE29bucut3FUcF7FAymzMbskWZyPxYe/SpqWN'
        b'tS21YvY9O0fJZClbWtNprLALUNoFiHVVNq7iRVLXI95d3jKfvhSFW7TSLVphE6O0iRGzVDa2EpYksVVHUiQxaClDJ6xsJJ5NMeIYaaK0SObaWSxL6mP0TJAu6s7qK77t'
        b'ES33iFbZu6Ltvr2T1FBh7yvWU3HtOvTa9KR6MhsFN1jJDRbrqKy4kpCmceJxKkdviUDGOKl3VK+P1VemCB5/I0XhI1D6CBSOGUrHDPEElb0LDrWFjXOtI/EufabCJajP'
        b'Q4F3zD/fd3SVJkmTZHqdGd0ZCsdgnN1T4ictOFLSVSLL6fNUeI1Veo1V2I9T2o9DxVjZDlC2FtEqB0dJjiRXktseKU6mY6ZVt45rHydjyYp7jBQO4egsksdSm1IludLk'
        b'1lkKDl/J4cs5fBXPQ1rdaSROFBeLS8QljWlDxDaVg4s4WZx8H5WeJw2TzGiPueMQcNshQOEQpHQIkjtE9IWigm15A5SpdTStxOC5ko01S1baY9Zvo+AlKHkJOIwbTxra'
        b'FiWJUnl4HknpSpGF91nTPh39rgqPaMkElZs33l6znQJVXt7kWXP7whRekUqvSLyx9pDmyCw682Rh0hndMX0Rt93Hyt3H4m22ZmM9YIAuRX3V00uK3p+0tDsDlenBP5LZ'
        b'ldnn1e+h8IhXesQ/9VRGV0YfV4ED9EWhE+YWe/Wa9BoNWgzEBgMzGKjTkp5LDg/x4TE15Nxoh59//nnUtJkMypwzQLFMfIaMlFHG0fCRZsaRm/HQaUmeGMc+QG++TkCk'
        b'nxdM0yIEZqzXzNgCK73XbBjoSEvVxnfZlQXVC+6yhQXVBXcN5hdXz6surS57PiIJQss/ODoYLYm/QPbLT+YUDha691DaaGDFWOzGNqB/7vCXieczUH2LmIP2d9pN5yqK'
        b'3nQS6nIdtHGmSlhaqvLhZp1/PVX5CLNObcWGhF1A2wEMDQgy9QTZ2FuQoPnCyWhzaQkusOCGuBmlp6aN0SEsuht2bd73asz+9fWdzZ3NPc1LTD4O9frZVXfLOwnGjBeM'
        b'27+gKmfr7D74mO4krOHvG298tSuICe40TxaRoV/JOoJhXrL1m6KOOCqUlcqtxiqsxiqtxsqNxw7a5elWAex08eJTPC+wfZ7aj4LuYy/jPjb0lnm4m1VRGq+J+VNQL3PC'
        b'PeXph7+sC2EB4P+TXWiE7mK0LsTKKs1Kf5clwnQgp658NLiD7Fq1xM6KBRfytlApWzhb8nXfrKYqA3Qyc5jP1EVEQ7uIaEQXcVF3kXLURUxs69LF1ZJchbGb0thNrvmM'
        b'7CXwWXvJq6SXDLnr9KG9ZDHuJVzcGZ5++B/0kjW4l7DUvYRB25GXsP+H/WSEbk5r/DGonxhmEY7zOf5JWhUG7I/EGgy0FyBb/Ht6zsxVbCq/ofbva2tjdF3JyaZpNGU5'
        b'VSTyN1kykTbGcI2n8NnagTmL4vvc9SjaMK5/ISsHHKfAIXgAm29T4ED6BJK9Mp62muHllWQctzSlIzFgszm4IycA7vFLTWPBxhRKdwaTYVNS+tqafB0Rft4NY0+tnhRt'
        b'CoI5j1b+I9dx/d8eG/eFTvX9sk4yqWpdcJ/ru3WuAtudt16T5/YwG91unvrtwKdH1rhK6t5Nq3qw4dstFmcX9Bxy8nnl37P77Zeb/Tb7jaM13LGnBma/v3BXXjRohoc+'
        b'rK3+ZtySd1cs5eSFNS5ZdSZBmfnuv14TnP7u7deEb3//7tW6H6dtCJS050fPWnG2ec6AMuCkNKXq8WGW80VGVOGyfzG7ZN5r983l69P7vsOBoMsvwAebYYFj4LIuaGMG'
        b'gAtqOBnWgU7Qotn66RTBy/TWr9aapo1ohtvhdWLJhbZ/2QxwClyl9OF2tAszVe8cYT/YnaZhzIXt4BKNgtsYkf3LdE8jcIxs0WA9g0qZo7uG6Qa2gitk4+Nk6UqAbLAz'
        b'xlcDZFcDej+YBo6F+6ViJBpeBxsodiQDnJjiQe4YbE/sNGmEHJ71pLl0fcBBvt6ziBd4zKtZKen5xBhP+JXCknlYdlkx5BuZTZTq2aQaLzjcvVFNUY0xLTF1ySpzJ7GJ'
        b'RNixqG2RzFvhHKp0DlWYhynNw+oSPzW3ES+ReCrMeUpzntRCae5el6iyskbXWFphWSzkU1snSQEtizWyxQxxiMqcs9eoyQgJy4mt0+84+t929JdNVpBgtgrzYCXxhRnQ'
        b'o6yIKBcyoE+ZWOzK2JZRn7U9qy5LZWy+S7BNINGXhreaKYx9lMY+cmMflZWLOLQlsiVGypZb+Uur0YH+oGpgWW7QFKhX9QVuCfbvsn6RllPLZfRM+A6eCYc02Cw8ES7T'
        b'ToSiZ5gI/9rZEIsjQ6YcA/XvRy8x0GxospcqpmYyhNRMppAxk8WkWlgtxi16Jcxe5lArszqKIBrE6wajGiX6QtYm/aGz3Uw2kyrWEbI3UUKdXt3DqLMc087DM3VJmh5K'
        b'0x+RpkfSDFCa4Yg0fZJmhNKMR6QZkDQTlGY6Is2QpJmhNPMRaUYkzQKlWY5IMyZpViiNMyLNhKRZozSbEWmmJM0WpXFHpJmRNDuUZj8izRy1KkZaHDbpz7Qg+ZxL0aRd'
        b'bDG0bbsZOxkzLVBejC8ZoFXLEeW3FDqRSIAud/UyC8qxJ+YvAYaDFRI5EyYl8hbTSTwSCi9wSDqfQdb6Icsl7iBkTapDh936g0IKaV8+EbAMtAvncFDrv7Jw/rJxSM3x'
        b'v7Ty0urSgrLSFcUiEoFyyNOWlouqsQdqoOGI66IqC6oKFvPw+Izi4eiB+C9edQWvgC5iUnIKr6S0rDhwxJUjRtLwxds5i9C9VacDKZmtJ6XCenBNLztgqppjDRyHdf6B'
        b'DGoiQy8SnrIkQbfAOtDqblS5JAclafLl6mMlPKzLhNsFU11ICKoinr6xL5DSdHp7/OEBOiIMxXaDZ3FImCzQQ9Iyl2b44agbuwSZ2ASr0RS2Mlfmsom6HGwG+5b5pWcG'
        b'BvimE6YWqzyw2ZsFcdgiCYFHJnquFoSmMylGHpTAkxS8YFBIzpfEV6M1MQPHEasDGwoZIc60TxPsg1vBLoFFYmB6pn8auqNRBRO2+vGIbXQZvMYnKyUmoW7IyGTEJlKm'
        b'sIM1PhWcp7GaBrh/mQAcT0U1QhdPBOsoM3fWdCgzJo8yP9NVrQjEjwI7DMEF5sr4LPrG6+3XCtIyfVEqNqg+agsamGC94xra4nojqpVY4LSShCLSxCECm2AfSQ6Bndj0'
        b'mwQHoFhW4BwdHKAB1BMJyXQc3KKO91QGrs1lBKH26ab9nBpBHehTB3Wi2LDbFMd0qoQ7yOYwFrbCjYKZc9WBmTRhmeBRsJvAQOGBxBZ6bH5mfsZ3+Qsp4hIRDU6D0zkU'
        b'PG5JzP4Xjiei2HIbklX/ZmJ+2TiqEqNRPHS6Eh5f9SQIkzoA01V4FgdhwqpRcm33NGJdnd/Dyi97XFxIkabMhcfBNnVUKIqtW4KjQsHNjqTe8HIU2Ov3JCJUKIeOCWUL'
        b'O+h4O7211dqoUP6GOCgU6A+ho78dsjEwAGf8RouuRAI3MdbQFv3t8BJqG9RJyMY5iAl6kORpCqWsOYXgfGnEW3E6Irza6K4JPp4bmw2DzWOjs/521vSLZTnm8Vs+vGF2'
        b'qzCk+vNJ5s2XeTbLChN7W1+dtMZj2qSyebfDLZRTDq2Mu/7g8leiDw6a3c93c89c9hbD9Odf5+yT3wrwUb1SU/LLsUKHKl3vPY0r349XvZ9laVoBl2ccuBR4jPvGteDe'
        b'M9M+K0t0Wd748sfFB3St/e8dX2JjE+JrGuw3e0/Vw7IjdRGfzK35YHXB5rcXfVLt2y5rfPt45S9nd9nP3fW9r+/Gqb6TX2vbuK3s0O2KSfUN/VMLJv199nvvW3juMCzW'
        b'C3njA5VX3qmSt/r+8eIvSW8odz9id73YqbezNvW0+1vxjIV6c2vqlwUufaBU3fzHgHC/VcShoKrXTp03fecfbbsvGSyIjbqVMuazfx2X2K1sHfdKxsKjh48cDhzz8NWl'
        b'bW9sW7D6p+ulbjPNWyzPPv5s53eP8z88Gr/s+ulVpt42vnPurGZwv0+raHD7ZcmshRFfvr8055e1m2w+Pz+rel9fuZUwrivcJfEz9zcvBfzw5pyXFne9sPijrnKr4/dK'
        b'oo/3f/PW28lneT6en7f/bYrt5VcXvu/15uXFxde/7BZc8HsY5ye979x1p+KrjSfDopv49nSYh3PgUgUtmqIBcQ7swKJpPjilNs+Em0oFxbA5wzeQzmJUxoTdYK8VEV3z'
        b'dJwJAz2N0uvDfWNgA3M1aIyiKbK6loNeTOzGzwQb4AkNNZ012MrWBxemEx6rMV7Fw1B2DLHHgI0EZS/xJcJzBeYwa4C7AlIW4AkT76VCQQvNTbUpqgolNZQEaadMIxET'
        b'tsH98CodgWADlIULiIno1JyljEQR2ENsRJ1gJ5q9gtBUWl2lmUxt4AF2VMRsGhqRTIf7QUM2nktZ4DKUlTGmzoI7acK1I7DRG6WR+ZSF5qqDsIMBxNmxGuvTXihFyeoZ'
        b'FTa4UKYLWGPBzkXkkcGBZZYkTtKTaZWypMD+SBboRPuK/aSQqXq1qATtxEpZzoSbV7LAhQIgJW+t0igcNEzMydbOrkaT0VMnhNAXW4ND6A4nbLI186uRJxNK0VK2jTwb'
        b'0w924LgDS3DwNXXogYDYSrpBZeVR5NE0U6BXCWVmwKpG5V0kDz8enoaNJMc0eJjMRrr6TDsXuIHssPTARR5q1kHR6Szj4TF4iAXXwyvOpE9FgDNhaLnqWxyknpKMUKdB'
        b'e9S9DnTjHmbBy6h89cyfv4QyTWKlgHNpj/HKnJ4NWv2yAgbFgwPbCwdPWgk1ehZoTTtOP8xOuMUdt3UmCWuVpjMF7KBM57OiamErHWK3EzZn0a9KPa9RlmBX9VgWuGIQ'
        b'TXfiAzPL0QOlpuEDGQGWcD04YMoCh8ExeJ1v+hcRXWAcncgowxguMPnHCnO1eIjJT5DQpGbq+oZmuRhYmKPRHEqTFVZ8pRV/gDKwSGUQ8EGLQDi1R3bEt8XLwhUOwUqH'
        b'YJyCT8W1xck8aDgC4ykJjHvOPnJ+nMI5XukcL+fGqxx8JLEyjsIhUOkQSIrD2VJRNl+5X4rCeaLSeaKcO1Hl5Cr1ap8tZrcYqlz8JatluX0+vXMVLjFKlxh00hhbB3sf'
        b'8enykUUr3CKVbpHopJnKkdeR2pYqzWvNbs9GJwxGnuAFSE1kwpMLji7oW64ITFQGJip445W88SjRROUaKHWSVZ+sPVrbb6gISlIGJSlck5WuySjR9PcTXdw7attqZfoK'
        b'lxClSwiu4H0Xd/xLZefUwW3jSn0Udn5KOz+xrsrK7iHlYBGisuVJU+S2vuhz3ztQukzl5C5NaZ8rm9o3oXeO3DFa5egmHdOehX+NUzoGPNRj+9g/ptBBwm43HjCl+EGy'
        b'5Uqfcf1uSp/YOz5Jt32SbiTdsqCBLYmJyo0v9e5b2l+qjEyVu6Up3NKUbmkSPZVfSB9f6Rcj0VNyfVQ+EX2FqAiJXruJyn9cv6vSnyTwVb7BfXZK3+j+RKVvHEo1UwVH'
        b'4rsquQFybsCz1HbQ1yilYyD+PVbp6P/QRA8/hJ76Icwpa7uWjDuc0NscHEoiSBmWruAIlByBnCNQ+aMe1ZKh5PDvu3qSJnZw6RjbNlaaTvctsb7KygE3ZDhuyFS5rT/6'
        b'3OcHy2xVTp7SEqVTgKy2X6d3rdwxXuXoIZ2K7o5/z1A6BqGm9MVN6YtrgS24+SHocX2i+8crfeLv+Ey47TPhRtGtEIVPptInU9OUtTcMlJHpcjeBwk2gdBPgpgzrS1P6'
        b'xf1RU4b2jVP6xvYXKH0TSFOGjsN3VXKD5NygZ6vv4O8zlY7B+Pd01KqoNfFz6Kmfg7Rm1h1O+G1OeN/0/gplRJaCk63kZMs52ZiHio/aM0vJ8VbR7SlGP4M0HMY0CRP4'
        b'j0iY1JDUk7nm96aaSqwCEVMaFcicnGdUgfzXdSMivIFrNwilTpsmUqznDGJfpcMkMbZHjVuvbQNNyPo3DLGFK04nIevd8KZTs1HV8i8NCU5fhZmpnqNOm1Cd+Iy7evNE'
        b'pfPLi4XPXDM5rtkPjCE1I9WqKOHhogqqa6qG1uz5K8WeVxha+Mw1ehvX6IS2rXxSygrm80pLeKXVvFIR2qKPDx2vbbs/Ua+qj6nneIHvDq2UI26moqpiYWl1RRWvVPif'
        b'VoT0pEfs56jIe7gi57QVcVZXpKC6tKKc92fapIR+VwbzFlcIS0tKn6MLvY+r5KXtQt64SmUFomoeXVLRn6/bAk3dimuLi2qqn6NuHw6tm4e2bnRJf1HF9Gias2ev1kdD'
        b'R52vpo9XD5oXUGenS/2To09vnrC4EHXTZ67cp0Mr50KmBFIEr6CoqKKmvPpP9zHN0HnmOn0+9D26Dhl/f7JW8zW10ijtn7lWXw2tledgXSJ+lRpF4tCaDarYE2xyKYUR'
        b'7L1UHbOOpba7p5hU/TAl6moGUa1SI1SrjBHqU2oNQ61aHTXt+ezudZ/iL0BqzaD9BUoY/0Nvgfl85i/TR6hn8T8ylJYtKEbtX4VeAhpFgwZUFRr0VWixreahblNeUT1S'
        b'wztCy6vtO0Oh/HniYpYI70b/8Q5r36tj93c2uzYwdDfYjZ1FeR1xc2IxVo/nM+hAe/XwOGbRDhqkdcWKgqnwShQ4X446m7mms6nlqBuYtNJF09m0dX5ia18yv7ia7OCw'
        b'VTQWqgqnMShHXnu8nOM7SMZj0zLeUPEOkz0Ri/7nuNd3WISbT6ntFWdNQxKcJRbFhh/+MtTqBeYzWnpQdYz/W2Oh0UYL6h5bD21giTBjebayR23pUarf3NlcaudO7DzW'
        b'Zb1Uy2123ewqWR9mQjXxdGQujqi/YJVC9SKsvqB7CzxnNUizlAoP/r4pSNXLf/g2ReqeY6/uOQtRz/H2kwplEZ2LuhehLUO2GP0MsQYhnciC8aw2Q89ShR+H2oeU4h5l'
        b'h7vQ0w9/qX2IJo78biE4KyDKPf2VbDMGOAL3g200urAF7AEbBH5ZKA0cBbvZYQxwZizsL83wP8gSYXK9V4XR2H1ofXPnRv6OkM2nNh+0ufVlflZRegHztN0i7kJujuRB'
        b'sE5Y5WEWdS72hXqDCb9u0AzL0bZUuIc/acWv0GGFxYhWJK8uk351Krb+wPRpDLaF3wA1ysGUYYF9NUc/3Od5yIRy2zD8MQ8bMmWM9o6fqW7f4ne6SN2tZuA3aoBf3KiH'
        b'v3aiGHVpIhMFmyxNbAKaUmpTn/+ZO9svmSNWlyTsJCWiJT20HA0FLEU8UXVpWRlvaUFZqfAPsMfRDMx0s3JTCP5zJGxF6EXKHDUNb+n0hSVrSs1mbWCI8DAu/+eJfa+G'
        b'osXKEy1W21qncDcmum0PbnRbyttl8Cbuua+FwZpK5nJ/7veVjcwxwrcX2km4Ua1f9C1Cxz2MN2bvCJ7WvaWA4cey6TOumxbGe7wsNDDfvffEls5tDetdG5xeyi54sySx'
        b'3+yTiW8aUwkS+2/+0crXpxkp1gmS/FLT0gRaPagpOM+aCA7DBqLVjYTnwGmMW+qhUzR0iXFLcLWa1sS2gn5wlYCB8Dy8SAOCGA2EO0NprXkXBS8MQTYthRjYrIXXiFp4'
        b'FtjqhYFGuAvuV+vEMdI4eylx5DNlGBL9LsVGw/48mwE6YB1tLwQacsAxKI30g/XZaaCXTemWMd3ALiChvSMksA1eE6AEf130UuBWRwY4DTtD+DpPV55go69B5jb6paJ5'
        b'5JU/kS81Z8hwb1MPqRVopuY6tqzGA5incnCRhKtsHVpW4q+uUmH3IvKHyoEnicDn15CvMo/egCfn73O4LZlyTrA0t3sWtvF3EkdJCqRchZWv0sqXzsa169Bt023Vb9cX'
        b'J2I3gfSm9MaMlgxpiILjgTLJcm9bhcitQjS3EVcPMZoZRdwY1WZmkLVRFV93sGStefJf8WSylNJ4/z5V4vhvCSD43WbRj2U1GtX2IE5tbClU9SV+k6zC0MKqAPy1QQe/'
        b'WM1O+q6+Zt96V5fe0t3VpTdUd/U1m5i7+prdB5lfSbPwTf48LGBCDeO/pltdhS2VNEYji3Bjz2QOo7xmYsprfNClTK3rpmGHBomv3MRTYeKpNPEcYM5gmHgNUP/5EbNU'
        b'ez0paSlzCCfzWMzJHIUpmaMwI3MUIWS2cRZPV5nz5eZ8OoMNzmCDM9hE1aUMo33GjM1WhLHZijA2oyNhfh6cJxTnCcdZwnGOcJJhMGNzOGZsHoMZm8dgxuYxhLF5MC90'
        b'LOaFjse00PGYFTqekEIPzhCFM8TgDDE4QwzJMPhBMA+2DeHBtiE82OhInmVwngicJxJnicQ5IkmGwXfBdNxcTMfNxXTc3HEjqoFjO3BjcYZYnCEWZdA3NAkfoJ52sCHU'
        b'1nKit5aOk47rjO6Opr/VpQ2wzTGL9HMcaAZosg5cY0MJPKMB1CLtKEOwkwkuu4FzQ1Y4S/XvR1jo2W03wk5Nt4XbQvUyh1pTESMlkzrLOqsSnb/SPo0uF+00DDbpqy3S'
        b'7ImVlv4oVlr6dO16DYdZ0GExxAjVjC00GlEzg6dco4N21cYjchuqn5/bazK0pkIHcg9LchezTQbDrjMi11H4yhY99MPtNT+M5pljupocBuhH6FjHICzbtKmXSZ1pnXmd'
        b'RZ1VHbfEWGg1okxjTV3Qj36LQQmrl4MkXuqYlitB6EQsB3WI8ZhRnTEqzwzXsI5TZ11nU2eLyjUXWo8o10RbLim1Ra/XZkS5OuoSzUhpNqgkA6HtiJJM1W3LHd62qJWY'
        b'QrsRrWsmNCW6Kue7puoJEv0qmF9c9fdwdPEQuSyRNzQHFubQbxGvAMlxg6U7bKBWUM0rqML6/iU1pWjWH1JQSUUVnV+Ikoqqsb6ttJpXXVVQLioowmpK0TA7trRqJC1W'
        b'VKlvpb1LgUirdEJiZjmvgDe/dGlxubrYiqrlw4oJDOQtK6gqLy2fHxU10lAO67OGPaBWSh0/ITcxkJdcUe5dzasRFZMnqKyqENaQ6roONTNk0kBTB3MYiYaWmwKvpLt1'
        b'tCQaTA3BO7E01NPSZ+j8L+gz/j5z+GsmDT7M2FAjti/WNMx/ZG+ofS9YZYU6x+CXOapuCvcg8uKFgbw0AooIK1CNyiuwSrtUVI3PLMPvp1CNCxSPspVQV0itN6XrNEKb'
        b'uqwUVxKllNSg4gqEQtTZnlKnciH6zyuorKwoLUc3HIyM/ME+RpcauY8xyaqJRt9EnoGDg+CmEhOLlVHYyAI2wR0ZJF7tlNSMLE3QOXAdbjWCh1xBb00whc1owE63kSXg'
        b'69FVxDhkNTinSy2FWw1WgzN+xEouPW0NbEab/lQ22AQOUjreDCgBV7xp5vPrKWAzpgZ1MaulauGZxWQ9KwSbrXIC4GF4WqcAHgqlWIGUWQzTA56Ae+jIvyfhWXAIk/j5'
        b'aYlJsGHopCkBU5lUGrgYydcBjeCgkDD4VhrA9X5olKTmiShRBGgh+7mA6SyK7fM+6pX5ZRetJ1M1/rg2u0GT/hN7uimwLmPyAl8cSdAf7sykg/9OrtCD63hgOzHgjINb'
        b'l4mW6FD28BIFd1Fg26IZpcq8A2yROSpYtENn95QX0l8M5rTvPZt56diJE0dif9Vx/qel2WnvIEankeHU6Y0/nr5Qa3sy1roz/ouikIIPxxRm8oW3G5tbIyvmPiqI+3vN'
        b'5r4vbzbspHauYOoa1k58Pe965Tt1i47+fPU18fQP0t+4bN0Wc3zJpQfOW1QTjTp9D499Z9kH1SWGzdL7DbqBzSciF/R0vnl4Yf8/Kw9XvK9YknlhrXAC+PifhndkZ46v'
        b'eGdRWX3fZzlx/7Y0eK1lvuiTyUE3P+Rfcfrp1MGOMq/WxXu+/+IfTm5ffmY11nutqH3OzdXH/hW5H86IXHgm+zf/70rGXdr37t6fjkzWSZnPWP7GAgvzbJ9Hy2ucB97e'
        b'9ltg4fli33370uLr+38pFn5k8ymMrDTMOTdmEp9DUwS2uIFrarNX0FtWyAjxhReInRJsrlpJTNOADEgzh5im1YA9xEpqOWgcJxhsf9ocB4/MmUFbh+3LhKeJ0dzYGRTt'
        b'zQFlYB/tg3IENsKrgiEWcxeXw+6Ucjq24wG4AWopEcEB0MaiPT7QlyNky8qbDPdHwj0C2tYY7SQMOEzQ6QkP0QZJB6EUZW5AElgWOAs34w7ki2R8cJY1GR7g09XrKYj1'
        b'C4LbkIAGjrhTukDG9M9HW15celrYcnDQaojZXgNzNTy6nJATWEyER9EuPIOCFxkU25UB9qesoou84G6ipgpAz7qOIlwBhuOIRRvc7Y8GYCDqvPVwRwim8qhHAzYAieJo'
        b'L56a6kcXsBdsttcoD5yMKV0rpgmoryFvQ1jkgsNHCnB8RsK80LFIh7IAe1lgV5662iWZBdgoLGsOGqrqCcM0h5W5pvwxmSz2zIN70aWYMBNH4tyZmgl3ApSvG5wUBJBw'
        b'oZj/fCI4pQd2QRmXFLkGNtnRRsRgI7zOoli0FfE+XaKxqAEXYzFpSjHcMDQEJxfSEUD9hbPQ46DpK9ADaG6JxH5UzHVwDezmG/4H2z3MSsUb5ilMzDJsh67jQw3BEum9'
        b'30DKDAbFdaF1CqmMe/Yecs8Uhf1Epf1EOWeiyta5ZS1OSaRT4hX2CUr7BDknQWVr17Js79qmtdJqha2/0tZfzKZtw2LaYmRs2XyFwxilwxixPp1vTdMaqZD2skY7DVSa'
        b'imOzV9AkkLIVHE8lx1PO8VTZOUk4kgUylsLOX4nD8zGsxzP6mCqufYd+m77cNbRv2tlZCtcEBTdRyU2UcxMHWDgHnY8+PiTHx9Tw8087EnfxpyTdt3Not+1wbnOW6Svs'
        b'QpR2IQOUrqYVxvaHKwY1xf2RNU/ANXfmdcxvm99a2l7aUdFWoXAOUjoH3XGOuu0cpXCOUTrH9E9WOsdLWPg5Ehj0VfTxITk+poaff9pR/RyjJd1HL3CltOi2LV9uyydW'
        b'evEK5wSlc4Kcm6ByciWmd658YnvF8yb2cW5eUg9pjdI7Xu5dcGPiixl3kmfdTp4ln52vSC5QJhco3AqVboXYEE+MfkSE9srZOUmfBfXZScZ60IyBji8ax0+wZd20ZU9w'
        b'0LvpzEBHNW/cIAMkLBc+gxUSzRuntTt6ht7tYISu2kppneJF0xkMhitWFT3f4S8zOcLL+T6DEOqUafzzWBypgXOd34WnhzeCBqWOMRpifBSmlUBHipyDxMs/ZY1E7FpO'
        b'/I6F1NPqGm802LylykJ3mPfaUKY6Fo2X17HVGOD/BjEf4cX7/xfEvOoqc1hzPgXcHmN8TocghDevmp/6eAi8/TblVc/82C+Rz3hM4owcg6dxYGS8jKFFjAnXDVnHvNye'
        b'Bm97DesAoqKyeYRC7ndQ7ikz/xTK/Yy3TDIaDHYnzfw/BLuHOKwTDKuO8T91WJ//LF2dnVUTi7651sItwyUo7M1Wn+Gb7g+O5tKObfhEdkZaDqjPZGD/63qjcfA4PFX6'
        b'zYT3dETxqJidX/FpiOpiam9zCIap/iGQ/N1xS+irnJeKtxsbH7Mr+KdXiteWLKlzriLrcK1XvykmTAinvGMNv/B14LMeB+F+2V0BukaR54bIcsfgQSLPGdSQWOB8iLZ8'
        b'2JkkE+we5k9CnEmmwKO0AL3FiK/t8dru7jmFCG5na34H332yar38rB1Sg9fHqsfAdDQGuJhXwzqDIc1T4nC9+E9iTZ+ucBYonQVyrkDl5fs7kL7e70P6T3Fufp4qZxoN'
        b'cXueNvOP8f2/FuTHbs98Js1fsA6eh9cEgmzQC/cEoE0JxvnBqWDaAuAo7IG7BH5ZVRjoJyA/aDQrbTaOYogiUPqlyhxivjEU5C/c+21+WlFWAfN77iCgv4Si7rgZKOfX'
        b'qik1/wABfNKyt3DLcp/WsuT151JazD9hJkMfg/yjHDgsjO//7kGfcvUcHfrXeXpfeK76jsfvvlLdXRNn/q4dwF9rDIAZQNF6gwG5IfOplmVjHUXbBKg9mnXrGHV6aBnW'
        b'0c6ow/WL/xWqmF8Oj9CJTSyu5hVoBK/BeuOnaxMXVxWX0Jq7EYbkoyj8qoqra6rKRVG8RF4U8QOPyle/v3xeReHC4qJRTOH+0OBAJ6sGG8IAMbi8gOgTMKKTN2lawNRp'
        b'qWjS1fo8l8AujdszWBdusDB1Hq2gOw+vLHyiwaKVekMVWFOM9KAMHoI74B4gK7353WmWqBxd+f39T/e9GkXocy42h4Ueag5A68SekJDg3pINDxfaRc2wqDLi2vWts99S'
        b'nPDwncqLhZ2WUzeVGRZ5C6wdWG1tXinSNzI+j1pkt4h7RlIQIz02Pb9s04IxkrwX54EdQj2rS19EbH/BuL2UWvGmzb0l7/N1acbC8zx4XOPnOD0Bq2xAB5+2EVhvEqtR'
        b'iIDLQRqdCJ9J+4h1JAAJ7cYYCBqGqIpyaDUTWjc65qrVTIUM2GMTMhVIaKuJCy5AInii4zSayQSXwAV4wt6FaE704cbZo/g/ovXKXARPekx6HgqQQbyFRpjDQt2vVtgP'
        b'G+mD0sjcVKse69V4afIQr5Imyzx6+QrbcKVtOOZRG7HpZ1gI6M3z+Bu5Cs80hX260j5dzklX2btKvKUerQHtAWI9lZV9S7TUo9tf6RZ62ypUbhVKKIxjFfZxSvs4OSdO'
        b'Zes8xKNFn17VCBz/+zYI+k+WNvWMVoiNEH7nOXPxnLZKu54Vz3weH5a/bH5b/lRBcQVF7yrUzEaU2oL4f2YT+cu5Uae06pGW4xUlGpaF//4Ml0jf8xlnuKdYcn5WlMkW'
        b'YYW77OKndgqaMLyUwRojf6V/e+P6ggj37fNemwTFOg+QBHCeot5/rLvythCNfDw6QWPARCR3nITNAaD+iRMpZQ/3s1dAqRGZPBbCerBbkFabq6UywDwG8KzT6LaeWjM8'
        b'F+ZT+qy6qcnYdFOPzdxZDMrB5Y697217X1m4wj5YaR+Mxpitc8saubnnECngaaOIpgJ/sqf6o/sL8ZhZrB0zE2b97pj5ywbJWPwUTJq/R09UsLR4XoEoawjoqMWcsEkP'
        b'LQ4Q0JEWB/TrmGj86P4PIUe0yfp74WiQo2YIYURXqA5P/0wDKFGLPhdXF2AHlwLa+H1xxVIkX5RUVSzWlPtXjT76GnVzR2FkkuDO/hiOXFwjqsZwJD0biKpLy2mPIKyD'
        b'GhVPpPVSQxwoMOyMCh8Ny9QOfFzXqoJldHOhZ/4PoEfDrJpwPG6Pge2ZgySaJM4ImWaIQAN3AwkdqHQdF1MpMylwSpeRSqHz5xwJReiy5XorG3IIszqbYrcyqo/QcQpn'
        b'BrF5BjiOY0K+saA2lMqlDWXwwRkeZfllMymdtYwpFGwDPaCrNCbmHFP0Okrs3WOze1KIKQg2jonOvLttx45W2+DgAdPD6dvtzFmsCb5Hm3TqXc0SelsvPW7uTl2829fo'
        b'fKhq7+Xm747H5fe/njZtbvDUlxPe+lj49+/tHm1Ktqsu+DB7+tVrr9m984nwWN/Pj7rv9xqHv7xm5fTQTya8esToZIfXa/ZJL68CNedumta8+0HuQFLugrpJmwNe6Htr'
        b'ytGZn/u/O/ahtHyzxVwvu9BrNw2PX0n3sjobMfdKa8X0YBMHxb9OLLn5TbDwI8P93mGvNJs6+ln+K/PTuu//qWPw4xjVDB2+PpGv5sE+hka8igRXYR0SsNzSCCI2Fe6C'
        b'W+MmDcecJoFmksyMT6HFK438U2hCpKtcfQJJwd7wJAxJYTxqViUD7OfAzcR4MxluyYC7dfx8CfLkz6AMopmgQ+D6mMTA3Z8Fe2lMahAghYM7E1CKC06S2dsUHILnnsQn'
        b'Y48b64mhuK1cUrMKsBMeVANpGEWDF0Ad0x/2gn1/Bt3hDaaY1lPTja2wGWUqRufJMrCBQS8DVbP+rIhmbSfOlXhI2QprT6W1J87oKbNUOTh1RLZFYr5jcfIAC50jCeTw'
        b'EB8eU0POjXaggYuRabqUs1vHrLZZMru+RIXTGKXTmEZDMVssxPy8QyEnW/u9tU21UrZ0snSKdEq3vsKWr7TlEyZfibBxJfrDyn6AYlp40/DSfHSpFqTx1qJLUk6rabup'
        b'xBRDMd4kiRwwDuP9mBpybrSDGn8Zfvq+rYPYiCAkLxhZJ/qzXvBnJwbrvRDGQEdobZMUyYKR7KRoPRjHQEd6KTYYtBQv0P1DqdaAGgSO0Et0NRZrn9IvKvDyvIHSQiOz'
        b'Zj03NPKXrdl5FHE0ITAQWbgNtK7HtDWsry5m4ysrKJ+fm1KkN2gSt9RM4t14LTem1/KtrK3srTpbddGajm3YMNOnMbFjM6szR6u8RZ0lWuOt6th1VB2rjlNiSdZ6PbTW'
        b'Gw1b6/XJWq83Yq3XH7Ge663RV6/1o6YNlpX/voY9ylqfKBRi5+by4mVDvQKwbQ1tx0ObHRVVVFUViyoryoWl5fN/h6kMrcBRBdXVVVH5WsVMPllFsUxRwcvPz62qKc7P'
        b'91e7VS8triKmysRMbURhBU81S+MVFZTjtb2qAps3a/weqwuqUC/jFRaUL3q6gDHE+mjYLmFU26Onih2/J6rghsDGUaLK4iLyhP50K48qeDxxxS+vWVxYXPXMllTa7kpX'
        b'44nj/LIFpUULhkhA5InKCxYXj1qDCtoHWNMOCyrKhGjIDpKnhnkILy6oWjTMlFD70kQ8mgsgkJeNnSGXlYroGiChcEGFkBdVUlNehLoHyqPZ5uaPWpCm9kUFZWXoHRcW'
        b'l1SoxTMtsyDdCWqwszK2AywYtZzBfeipLal1J4riDXf8f+K8qbnv05w41WUVhhaOLGUwfcAfXI/nGyTL5mTzxoSNCwgh32vQHIoGobBY86o0ZaGuT/eS0X1Kk4tLCmrK'
        b'qkWaIaIta9Q37i3ika/YXnNE5YYIvOqeiR+lEm160V/PIK4PkYOtRpGDvbNopuAti2GjKLSKaQ43UowKClwAfa4kxQnUsYyWLmGA5rEUA9ZRsB3UBfAZRAiOmAz7/LLg'
        b'TsZ8NH2CnYwksLOwZgwWqXaBBthptBQcLlgymZajfQIDfGBdkG9aJhKpj+ZWwtPVU2nLONDiazAWHABdNdijAjYhKevsEGs+mppKY8qnuzCAKpqrDzpNwVUiWadVm+D4'
        b'KMHr5uZn/JAVS9V4oZNuQDYrfw6WIbXGeDTtlz8/IF2HivXThW15mTRsUA8bYYsfbNJFYgiFRTZwAJ4F+2mGvUxClJzwN9d8/636oero6TUkTHmweUJ+Rp/1HPrkpDWE'
        b'i4973yS/bJZZHC3aw5MJBvAgcyzsoygjyggJu70kBAm5ojaSBHbnuhblZzxysqeIMWQyuA7OE77HnFQCaqWh6m/3w7sR7aOghFSwTd8/PSMwLQCtmLCBb7xkpWFNJN5R'
        b'gC3wiHZHg6TSLo2edjsficagJzdVay0G1sOLBuAg3ADOp/D1CV9ihg2UaukS4UW4hbZ0OgB2kzcOjsFzHoQwEVz0pphzGUHzHIk5pRPcCfZo2RIXwauYLXGKLUmLM5sm'
        b'ULOE5ZRrqBLHiQgskwH3MLRchdHLMVehKegmlJJgO2zCjmJagjBnd5qsUAfuI11zTOQ8NVfhRNBBGWCywoLoGgxWV8301PIU6jNHMBUmZ/GNyN2hBIgjNOSaVmMwt+YK'
        b'eILwP1qAI/O05JrR4ALtpBYJWwnJISp5FzyvdkID2+AO2hENu6HB85NJ7bLherADE2zG+6OBg/k1U8BmksKHTVVEBwy2wmNYDxwCdk8hLcUMBLsEhAwOHCzVMGyazieE'
        b'ng5gw8IhDJvjqmmGTXAZrCMGqmAd2nccfsKxORccpTk2T6ykqTJ3ZcB9WpZNuCuC9qtbjJ5JzRjaHTCYt3E/lNG8jeDUQvoGLUxwVMPECftgk1qFBS5NIr19xkLQkQPF'
        b'edQCtLeG+6lyaz3ChvmZLxkvqTUJ+f6lub4U3fa7y8Fu9EDN2Wx4CD26MQWvT0nnG5IXiGaAs5NEplU18JQxPGWGWvhCNWpfe7hxISsN7IXXa7CEbQauuagzzYK96nwi'
        b'eLYGK94Os+B+eMa/xhMXd2QaWKctDtaboZzLqpcYVJmY6lI+LDbcsAb012DINxN2joNnauBZ0RLjJWCHWVUNi7IC7bDbkRUJ95UQg1x72Ak2iZbUGJI7msFzBqjMszU4'
        b'P7m9wxJUgfi5ujqzQCPh8gT16EkPaq/Q1NFqenQxKxGen1qDt6FLwIaUJ1m2wt3aCjqDE2wv0FNM3lLpMv6ggqqr4FlUQaHxBFbUIrCfjBu4P5+nzbIMzbO6lLkuMzkA'
        b'nnCOI69xBexlGMHz1agexgaBESZVOpTJGiY4sxQeJ9VdCI+BXTmZsDEH9evdOWAHmw/2oVfdxoDnoRj20TPBRXDFO2fSJCo/FZOwUgU2aFTi0mc7TtYWbl2pLRwegAdI'
        b'7xeUFYrgeTN0ngmvToWHGb5wrwGBl5ygBPbDBjThCYIyM2pss/PwAjFFrYfxx5Pf9rQMuA3tsMGGPANRCqR1MXpAXCbAkdEZUdRYVMUWQ7ibvMw00Is62JlUNBUIAtCQ'
        b'PQBOZmSx0dBuZ4E940LJJLyn0p5CvbXSkZM/e+yY8fTM7L7Ej8pFO/AM+/zxr8cZUg/oBfTnePUfPgl8NrEUN0JDuB4co4Q1FLWcWh6TTgce3D1VFxxjw0vgCGptakUW'
        b'mj3xzg00hsLNfnreVWjup2rTAkgRxnbYxpcCB5PRy6VK8yrInrA0qFfEEtmyKErR2358qqDi7QTzD2ocXz7pUfNL3awHijGHYnxNeQzL8foPbfvlv6bX5R71vbBwcrFg'
        b'Uj38cV0/zzTgtvOkwC92Cdtv/3AizCvuvk997L8+2/fym29+vevNbKBXVLXs5snlwYe//0JnnpVuYqD1zehTL3xuUfxS5mLm5z3Ksd8eCK9yKjk684GNq1VtW/orOpt/'
        b'OqxcvOjSD+O+HnjtBm/VfrMfIl+P6v9hzp2K17+Y+OEXD/be6GM/vOP55rvutSlTmswLCsZJbizz7Ug+yHxp7va0Upu88a1nDriHf5jDMt838M2/jG6+/2hca2Xwr/Wd'
        b'B0PfnfZevEXglvkHdh6xu53UeG1gckPu/ISf2yQHDvDTa7PPTlrjdrfhh4ap73198GS859YP6mJcX/6s9WHP+ew3fTx/5elUn/Ef89npd6cdLJsT6O78wt3jA6l7XZSn'
        b'Pxz/zvmGPKO2YzEbts1p+rrteumOn75f5pYQ2/tF75KJZy6+6F5dEdhg+tJU2VyrKw4vXa7n77E9ePPVQuPH1uDXK6yQkx+88tKiUJszhhMjOL1rpDO++OBe6ZRt6Um5'
        b'l3amR04q3ZS+UnY2aPW3s/8mjxBlv3PN0Weuzrag9R8lSlUmnEXryzcGzFtZ6rRr7LnKDz+i9s6b/Jn3u9a/5QkCZA9MTDx/Xdv5IGLgCvNO+u38Y/8of602LO3dF0q+'
        b'TuQfOV5S/JLwrZD3LmR4vjN/99J+cGX9nE7h41u+vTuuBH16xmiV5yLTy8U7Imb8dDfTSbV1teyfjJdeHr/frGtrWlSDqsBhrehO4NeLp2X94vNDLTf+QSe38OtLHxTf'
        b'gs2R6f5zD3ycM/PzuFjnwnsPBnrsQ77OnfhN379fMNr4Q5Dgw0fB17N/e/Fk6Fc5H/Lq4z9oivtulUf9o31rDp66duP+tsXbXR++t85khohpHb07b98YRjwYiCncVx/9'
        b'QeOYMWda3zqv+vGNBcz5bT0xd25k1NyMVZY0Ly8+s/DwuYZZKeKfJnvcDTP/Rk+27Ae3KfsqzCbvB6sEs9redM89cugrx+s1p9++Odfav93ix5RPPlm9U+X6UHq/NOLY'
        b'Y2aW7dbP7C7GLkqY6jyt3rxswnd1j/5ulljntnOSmB9IINeJZUhE0hrorNQjJjqWaSwgTQJHiVIwHomWm4nIEg92E5FFKKTpWsRG0wUae6FscJxNeKAt4FYWkjzO+9Mm'
        b'+OdXwQtDVY5Y4Qj35+lnrCJqweRJurTpP+gD/Rr6abgRrqPv0Qb2hD8xWC9HCwVWatIG69kraLi5PWySWmsJTgEptqQH+9jEEj4CbivSRN2zBd3Ekt4CniWW8IFJohFK'
        b'S6ywZE9OzYdHidrTNA5eHxSEAjS64CgUQfF08L0zEXP8sjLhDl2KXQ1PhTNAD9gKummm35OgvUKjzUQTnIT4BayOpxN3j3ccpAcFjTOwT4KdKx0Uo90edGmDCJaCoziG'
        b'IBJMNtMkwdvSwUGBHziBqovE1gtwg+5ypgdaSiTEkB4ehs2g/klIRb2pReqAig1LSVM5rAa7NJpjcN2UIPPnptKsAPtcwDatI0QcOE/7QsCtYBNd64Z0tKg2oKVED9aB'
        b'E2i/0sXIgyeFpFy4AZ4GDRpegI0xmBbAJZ4ge6lwL7wCG/yRBIquhduAGOzP9EeySBAL7l4ArpKnnj0eHtdg9/bTaPQenoBdxgT0nwE2wlNE4LMwoMW9E0BMO4DscsKr'
        b'm1rc5oArtLR9CV4i1dJxMdSK1OCENRap0+B18jiZVXkamTrETiNTr4Kn6JfQBS9jXnO1WB1VTCjAu2EPTbBwhAMODhKrI+A1Wq6Gp7Jo/4tNKbBbLVk7gGu0ZB1l85hI'
        b'UucmwA6tbO0DJSOEaw7q+vjZ4lZl4zJoewWdRHCAMoPrWBVjQCPNp7AZNAIJDvAYlB3ApMYKUdf0LYJXH+PdW0wW2oINksKWwHMmsI8RCjasgIcY/rBLxwBeWkPeezG4'
        b'AtoE5NWg1yJCIq8+bGOCbWCfBxmBafAoVx2kBdQHpYHjPgzKoRS0pLCRuAS7SXstWFRCosBEoOEDTsIdlB7sZOpXwS2EF9rIMRkv5ptQ0Xgxh+tRK5M9QKce3KJmGK73'
        b'xy+vHnUfK3cWkrC3LCadZxo8A47RWQIz4Ta0XUA3h6fRU0vYoH2eO5lj5oL9C0mebH8spNShOcY2gu0LtsQvRcPRjbzPMRl0KVllxQGpaHpCQw89sx7lCTt08pPgetr8'
        b'pH8uuEhC1mzDslLH/EwcinMHE3bCPgN6zJ+Hm6cScKXen0kV5+tmMR1BSxI9+E7PBNdoZyHaUSgwgnYV8oWb1eFOe0TwjNlSPA+iEXwe1dMA9jDRkGsDdL8D+ysXoDcR'
        b'wPcJYIBOsJUymM8Ep8GhpXzXv4b7+L98EOGtxzANyroR/9SGMwVC4VMNZwalEVTGS5dGZdbMxoF0WuIwODGdIZ2PuTzwXyoHHmFcjuyN7s/pn3MjTx6bc6tYEq9wyFM6'
        b'5GFcYTrNtpx6K/L1aAV/qsJ5mtJ5mpw7TeurE09AnEFGM1aOcisfWY4sp8+uZ27v3P6C2wHx8gA6mzqopZwzTmVl2xijsnOVcKUe3YF9Hgq7SKVd5AClZx3YH6pyce1Y'
        b'1rasdXn78o61bWsVLsFKl+A7LtG3XaIVLrFKl1gJW+XqIbWS5spcu6d1OnY7SnRVbp5Sd2mRtEjmIVvS691Z1l3WN1nhNYbmcr7jFnvbLba/ROE2Qek2QcKWTG7Vw3AM'
        b'DvHJaDVsN5QYatGZI3ZddrLwTpduFwU3RMkNkXND1GlDM1rijJ0O3Q4KbgBNZDxghqpPnoEcHuLDY2rIudEOBNEZJc2ccnTGqJc0XMaQucpY3eMUDgFKhwBx8n0rW0m0'
        b'JFparXDwVzr43yZBhkgLT1TYpyrtU+WcVJWt+wgYzsq6JXJvXFOc1ENh5a208v4dGM7GeW9ZU1ljeUu5mHXfkady9pY7j5clnUw9mtqT3pt+xz/htn+Cwn+80n+83Dn9'
        b'hlDl6qtycFY5uLTHKB38VC5uHavbVreubV+r4rkfMeky6TTrNlPxPFTO7vd5Ht3GSl6IysW9fZXSJUil+e7u3R2jdI/Ufvfw6c5QeoxTuXlhG60IFT+g11HJTxqwMHC1'
        b'GaDwwYZy9ek2Vrl4ta9U8bzRX+6+3fH0Xx5+So9wlRu/O1DFD1by49BVLvgqdOA7cy0HKHQQswfiKFdPcjexCeqSLTFKK0JnM4uhCg4/a6wMTpeTz63MW5lyj5niTFRJ'
        b'9DrYvcZKnxiFe6zSPVZuzlOFjz2boQxPldOf9JnyWXOU6XPl6OM9D6VLLRXmHipXTykHDb0KhesYpesYsakqdNzZoD70cyNOPiVXmZQnRx/PqWJTSZXC3O0+3RphKs9Q'
        b'lY//SYOjBvLQ8QqfJKVPEqqDyj9M6Z8o9598Y9qLs/FTx6i8fI+UdpX2mSq84pVe8fQ59Ph+crcxfdYqV/cBayMb9NjoIGYOcCkONvHGU0DYmAsxp2NuGCrCBMowgZx8'
        b'bs24NUPuNU08XryyMVtlYy8WNpa0lIhZKlt78WpJjdw2UKaLu5Mt6qgWHphIO6otqjWmPQaHinV4xz28L1fpHiW3xR8yf6Tc4ij4mQrnLKVzlpybNcCiuNEDupSje3uM'
        b'jCmzkDFRn7njEHLbIUThEKZ0CBulHNRdJOx7tj4yjhLdvlqNK5MQqo2rWlbhL27i6paVclsf9JFOoX+j01yHDrM2Mxlbtqg/tL9KwR2v5I4X66jMrfYaNhlKwqWhMqte'
        b'6z7LHvs+Ub9QbKgwT1KaJ8nNk3AOkyYTSbE0sX2BwtxbSRPHoLNmTWZStsLcU2nuKTf3xGdMm0wl1bg3ByvMQ5TmIXLzEHT6jrnrbXNXNNi0F9twW+bvrWiqkAoVNn5K'
        b'Gz/cpBgaX920WppDw8kDlI6F2wCTbe2GJxqjNiNpkoLro+T6yMnn53sObmjyth50QNNl+zI83GQ5NFs8erN2bipH1wEW+k2+DLBQPjzPoI0Gh35uOlQa7r0EOcZCFrBI'
        b'ikixZL1kyU6x0XvJjoGO75paT/Wg3vXwnGbMumPEQEcaOramoWMtoFpVg/FjLZRatfQP4eRnXhyxKJtP/xu6LNIQ9NHRLCsHLYTbMAytomgYWg1FT57NYDCI9+X/4fEv'
        b'c/lDD0gdNUikqBco00RTFp91V19jzPWEO6qITT35p0VkpOiw21wDahMTNT01pG2khrSZBNTGkDZFSFBYddYlVgTQZjOp+mFg9Godg1HM0dAZnRGgNXuNjhrQHjVtCF9G'
        b'DnMUQDuvUu1ROBTPJshugRqZ1Fq1PR0l1uQYSpxRrQZZBxXhr8ZaiwrKRwXgCjGWzitdTDC3qt9Bzv8TUBnD9KPe1VdTPV8eIccg+J+mHjSaS1cJQ/Oo6uU0gjo6oMtL'
        b'qhAWh43jFRZUEQSSfuCq4sqqYlExKfv5rPVIA6rx9+GU76MB56j40fly1bCsBpTGOPAf4ZbPi1LqUyNRSpcsAivC+hx3tL/JBuvh+UC4IxPtfiePdELQGuzt5BvAk5YT'
        b'akLIFgqctB8MB6Ziez9Yl53jA3eaZT9BBlfAIwZghyuT6KozQ2ErNvJjpOKtkxjuhs2gjmiIm62NKA6VP8HEPD+janoKJcJz4MZa3xy5nknlEhbFnMqgFI9qJqCzuXZT'
        b'/YAMa2nq4K4cjONlZpAN3LQRPnNEyQ36YYdW0c3KM4GHF4KrNdj+JUgXpZxhUFQelUllgkOwi6aBnL36V9NeFo9NBecXczPOptFaalVrQi5J/nbSLP9vWf0MKn/dwp8T'
        b'3i2kk1O6EkhqvcFChpJ5a5kJLz96dborjVuCLtgrDGNTYAfopUKpUEtwvWY8Pi+GrTmDwVlYF5CeCZsxJBkEd6Spwd5U3NKCyanp5UL/dDq4D7wAd5mkC2yJpt9SADbQ'
        b'GCVog0dH9yUZYnepg8Oi4e28NdgOdgu8Ap5E5tbG5QaHwRWCovkn62mRu+SpNHAHrzqSO68BHab0nU3g8UE31oCjPtrgUGA9uGawuhieJq3ksxaH1/08R4fKN3ZxnqtG'
        b'BBIW0m340cKpC9dTCxhUwroVqsUCYVULdnbHKXwd0p41sAn0ATS3ghMLMFAAexzIeScKngDHUDtfrSK6hTbYQN50RjzXT4+Ce2E/RgrgUXiOYAUTkstgA1bPxWGoYAps'
        b'oWG5ZnAtCbX4EdiDlS2wQZdij2GAk6BHl0CZ1gw9QWB6hr82cBEB9eBpN4LD6cZXwoa58Ihaz4SVTA5wQ+lPixsYIhs03y/tfbSj5Wr534LNX06bfPpameDUG2OzugIT'
        b'XaRJF65NOEI5mQWIKbtuHGjki5TvJkzLmtke+cW73l9O7gvIuXZ2T77qk3v/Xvbyx/vXvrk25Myq/F9frkqJOVy2ZO3KvogzD2QXmJGfrnhR8t2jjfuONpYs1JlQ9vBM'
        b'bO+Yd94OzS8p8H10wkRu+XVAzc5fpx3+/r19Cx/MMb6y5K0tD15M+mZGa+zSs5cG3nQwzt723uw2y00db0w83Fr4Y6rFN8tf1F+tm7xrf5Yo/9sf0tpjP132NWsR2Hv/'
        b'cv/8oPYzK9//NOPhZ7taw28++qQuNupiff2OHv8tPx1lWas2vR4Z98Oq1J+OBUl6bKI2JU9MT7h0rO3FS6/n6bdaftV+qib8a4vc7pkJO4+av3Qg/Uby5goZe/vkL3In'
        b'X31xe5hvkWfuzxHcksXCR87/8Ivo67cq63bumRzQKGmOkByYc3xD3Vc/TVpeNfH2Tv67UtGcmsDt4Xd+e/2Xq10f//utM9v+Pe6tW0c+s3N/K9f4H1+9vkt1b01Xzu4b'
        b'q2qkyjhRYtiSubuifjqeE/29909vfBUtWnSkBbTUHn1Bmf9SpO/UV14J/y3lNdWuzosfnZfe4t3720fXb059bNyvbH21b6L7nUUncmpOVE3/9tLYjX4XUhrOLNu//V/v'
        b'78llW/frp75W8MOKe4X7zx+MszwamJr35bQzj9obzzVuetAu9Kp8+0PX93+8bgA2eJkfaHq8feuBlDUlX1y4ruN7oSwrkG9DFEoOoAN2+sFrgRpzXkxvc20crezdBNfn'
        b'ajWytQW0Qhad7aBV6/tjQI9Gte5WMjji2+Zyov4UghPuhIzVfLyGjjUKHCIqVQML2C4A6xbTGlusrgXrvMlFVeAcaPED3ZZqO2AG2D8ebiYu7EvzwVaj0rRRnajgSbhn'
        b'Da0o7rEBm2FDBKwLSsWgIjuVAc7A/fQzzS0H3QJiliEI8GXAXfMoI7iPxRyrVmrCjXA9aPObg2ZD0IsWE7aQAa7AjbFEOzYD7AHn/NID6DT7SsrAiImG7g4ndTAzHpT6'
        b'ofrgRwI7ZlAGTkwgBnssaHqi3SXWOJQ1OKYfwKRIJOvkZKKFXAIuR8MGsB9u16qoterp1ZNoveDGNHgFa4ttwFUgy1AbVpuNYc2eB8+RloEH9UC9X1bALHfivYLmbLQ+'
        b'+emi17uPDfbXwh5ae3gQ7qrGV2dmJIMD2TqUriOTbZhDK0Mb4TEzP7gVirMGz8xEG+pbQntTr58Or6GbjIc9Q/WhWBc6zp/kqXJBL0etCwUn0Yym1YfGYz0v0YZywf5k'
        b'tTZUowutBuefqEO5NLORAB6Yo1VGXmTTusiaOXyX/3s949P3WLgNBktGI7WPmtDdg635VjgMd9EdlEgUkF+qA8CV5TMorr3aBnyBwjZIaYuDuVlMopVPSTcWKDyzFPbZ'
        b'SnsSXMrWCfsSh6mcXDtmts1snd0+W5wiTlFZu4hnSnVlLIW1v9IaW1XjLL6SObIxCqdQpVMoykIoh0vQLayClFbkFn4qJ3ds3t06p30OzmAnSe5Ib0tvzWjPuG3lI7fy'
        b'ITVIUNgnKu0T5ZxE2gDdR5qssOYrrfm4iFDZFLUBujSkNao9SmZ72yFYnITt0AdRnmM79NDHTyNEf3JQ26GPYEy3tR+g7FF1HXhY8ZpDe9xPVjhPUTpPkXOnqOxdOnzb'
        b'fKXTFfaBSvtAMSaSdXDu8GvzkxYp7H2V9r7iJJWHd3dqY6Z4gmTMfSc39LS2jpLqplXiVbS6dKqspq+mZ7XCM1bhGqd0jZPoqngeEh2Vqyf6y9ZJym5aLV6t4rlLWdIJ'
        b'sry+qT1zFR4xCl6skheryaXOims4TuXs2rGwbaHMs09X5qxwHqt0Hith3cfh91jWoSqfUJlhX1iPWa9Zq4mELZmvciCqiFCVm+cR3y5fWU5nUHeQJOm+vdOwZ7B1wO2R'
        b'SfcMgcI+Q2mfIedkDNP1jFRuPoePgbOfZLEsuT9Z7pyocE5UOic2GonZ4mKVla1EH2vJn3qhq/cd15DbriEK1zClaxi6ZnqjqcrKZoAyt/BUcez3ZjdlS1NlQgUnTMkJ'
        b'k3PCVBxXcabUQ8ZWcAKUnAA5+dy3d5Z4tHq1e6GH5diSaxKlS2SuCo6/kuMv5/iruI7iRBXXTpLS+v/aexO4qLIrf7yKKnaKRYodEZR9U0ARFFBA2RdFlMUFEZBFNlkU'
        b'EFsQ2RfZd9n3RdlBBOmck8l0JskEekiaIemk05nkn+QzSdOJ/yydTOZ37iu1u+0tk1//JvktVnl5Ve++++4995zvOefWu+co9Jzd0LakT1rarQ71N2tvbukbtvK39Hf3'
        b'SLf5jshs6NvSJ2rEt963Nabn9IjRyPUp9yWPWt8N8bFN8bF18TF2NrA+sMdkQ2y+KTZfF5u/uOmJDbHFpthiXWzBvgmqD+o5OKKwuc9hymtz39ENscum2GVd7ELn3hKb'
        b'vCk2IbqKrTbFVutiK1bfr96vNYsF7RYbr4uNJYtIzISE/bqeGgLUEHrqyKI+n0rJipGmZMWIhYL9cFXiy1ki+lRIYy1/cs3ow3WjN9i60ecBmIIStfJV3vOFI7ZqdJnP'
        b'57Mw5v+NxZe2A+IeIbGFQEJ5azYHNjKvLAqxlHucA1xPRZP8RxaFBGWyZVLPU7NLFoZ4bGnoqtLLZaBXE7R/+ctACRZSP3L/tD2ML5aBPszP/nJLIreT8UveBSy55kW4'
        b'dcl1n5Lvy9bQU/LIOteVz3gUn9s0zNaKqKrvmWAnxwN2bG0mJTqLPXCdmZWRmBr/mV2QxHn/8PHzVzMRSc7/FUEX5IKy7enTxetQ9nkxF2DS99xHPGWYNPHinvb0wWWP'
        b'D58F5Z3Fu9yzoG0wzz31fBiWLQTRH8m5zh4FVcUByQOL02QC13zsaVMePlbjHjclk2wtsfOf5ASZjEdMfxdbHWSnfPe4aufR36oK9fZcyS9Y21FsaQ0P73GUUfj5136w'
        b'FbKx4xu2r36f8fLXNR1mjzr87k98xSOm3/ztz4bnj8ffCi38ec8hGfUzfWdrXJ/+Mekff/J10djhAFs7r8PzG/+W86cInYrFePG0d2L+3OlfTQ2JrVa7Ti/JfU+j7deZ'
        b'fj/LUPdTDzyUkv2k93dmhb/9RYLG1/VOVv/pz//xLz9c1Z+PuWSp8EQvJ7nuV11D37TK/d5XLaQ5UzoLCt24Z0gyhM8dlhvYJwnB0I0VOBwT8+ruQyjSlxiwiziJHR9/'
        b'GsgZhjmfBXuMJLZ2+21o+8jjIoHWr51+bo2fsJeY8mPYlCN5EIUndTWePYaif+VLTg78SXtROZsTz5cW4+5XAPfjpzmb8dc8ic3oEfs/u5VQy7j2dk/ohpblppYl+7lK'
        b'rzV7Xd2Y3ltmVrUnWnU3JKpLg7M2Xba0jGrzesxHPDe0DmxqHWAmztGtfQd6XKe0N/Yd2dx3pFVuy2z/W2bOb5o5b5gd3TQ7+rwNsinX1U22TFib2nVBW/ushl36XHrd'
        b'Btze2nf0TVKl3O+EZCxEbqgabqnurhVxeZBVLTa54PuS90d2yKt8ZFveS6j+KzUlF9rsFTUo0X8bTP99/nTkMg3Y+xENmBbzJWvAL029/YERjr8tm5eYzhbd/y5Te92z'
        b'kPpg9JP78jJiEhJvPA+z/jwf48cCu3+K5vKUrIcn53IL6Ikp6clx7CeAuFijz9Ryzwnzanhw+vozfqX4Qj0hDOI2zsjxoyVPzn1kSRObseOVPR9XtOQS94Ulxsb8gp/J'
        b'VnS1G/6Txb2ShP3TPGB/mf8gwDXwGwXvjv8o46SHyYTcv4q/FjRk6SgjE3oosMrk3+UOfaMg55DAo8ZBxPvuacX+/3jPQvKsopE0lHO4ig9w7cVS0FAgd+5YitSHMYpT'
        b'5biFoGSckCDmBFYqcqCqeOvj4ZWx2v2ZLasxBmX2OMvwdBqrbLDMF6vDcZAt//sGXn9+hT+My8LUKej5/MRp26rRknl+IVuZL1OYvfzN8pUKHBi6PQfD43F8nljz+dMb'
        b'Zh8m1HmOfMdeN/so8r2taSH5fXld1eqTmdbe/Aw4+USmtW2Zj2Ra+6xutil9LNNaWixBBPPgPqf4UpPocEPLmOazNe+goFCvoIz/YGNV/YKkOh+GhWXBxrj4PFzAEW5L'
        b'M/ejMuchcDDJEcJC52+7RKPDeyXPziddGns2X6+klFBmP383CV5JvSPPUu+wQlOSemdfz8110f4N0f5N0f4dqd2iGP4O7y8tWZqdAx9e5/axLDu+LMuOP8s9Q+UzruQS'
        b'7Xw0BQ5LLaPFUstosdQyWs5l3jtyKixLzOcWhp+TPuYdkZgNal1ksCEy2BQZ7EiJRHt2eJ9XsFHseVnV4DlZPtKCHEsr9LHiw0vYN+IXlMxcF1ltiKw2RVY7UtosO80X'
        b'Fqwh65f1D0oaChtxWNq3tWffiHiKrTQpE4GoeMaKd46f2HI5viPI57MG/leV70u/uN+OkPs2XyDpWcyIYOrMkngpYf2g97rIZ0Pksyny2ZEK5q787y4Z7Xz5H3bgwvNO'
        b'7htRHwmdMl83P/r6iXWR74bId1PkuyOlKSLY/OsLdjc//suW3CT3OrMuMtoQGW2KjHakFETWLL3RqwW7cO8nK0iCsbA9ZfrYCUsvsxbhPB3gspd/AHtI2dxM+gYUQkf2'
        b'bwigzPbjPDyAetc07DigCiXkHTzROOwIBTH4SOYIlkEd1MsB04Z394igFouhByag4cQJ6FOEeqjg6+FTWMSnImg7gnNQAzPRMI+joSIpfAhF+MjVBZ7ClA889aZa97Ei'
        b'FxZhFCZs86E/AB665OMqDsviFIzRa/kQDEI/DsVftzfBNjsswN5U6MJ7OIoz2JHvCpUwhOUwreV93QX7PII1oXIfFnjeTnLAalyFxUQXLLnmrbsnWtfriL90hP0t22Do'
        b'j9C3gQacd4HHOAyzUJtKnksdtbTgAwvOKZZ43z4Kq0Q4FItT6uQs9kA99nFPnjdf9sT2Uw5JUB2DkzLQBQtYkgbTWIddZ3ASpm6m4AA8vQ1PsCUU6nSw79p5bIaBwxr4'
        b'0AeeHAAWZL8OatROwKMzUGTmTx1YwHYneHQbx09DGx+HoB3vYiN00t/7CTCC7dB300CgCI0wh9321tiPCwlOCi40QaUx+lDgnQL3YqnZlkBYsYjxStvjhTWJ+BQ7/LAp'
        b'Qhsmc9xxCWZopqZcZaD1tMVZGnclNEGxgmkozmpjL/bRp8VAKIXOcCJGE7RY46KTm4mrsVgdZ87RF523zM5bYRuOqaqzH0FgPjSTvq1TVtiLa3TFGE7DI+rOFA9bHOKO'
        b'YtsF6LCHlV3YrXwlEGris9ywIARbDKAyylEO12BJXx2WkmFND0ri6fKJdDKrWu30sS9277lI1/3YQKywBEOZ0cR1zdgeqqRzIS/16C2c07+4G9qDoE/nPNvDAS04IkeD'
        b'mSOWase+41glB6UncfkATWMzjDvTKCeof4tQFE4zcN/mGLFDRQ7MaOmRJ/yUprJH+TUBrmC5tzG1MZ9dLcUSWmArjeZBiDvUEOcrwQrOauQfp/kdPgkFBtCJrTZKB/Eh'
        b'zdA0dAlOwlBM9D4LqE0QQqXhnf0w6JSdl6CCTcSPfThCtK1KvxwGqxrh0H4c2mEaBqAoGjstscXKFJdwGRYFMCWPjXq4EC2djg9g7mzEzWPYcftMMoxTZxpg1ZzGQRyC'
        b'k6n+R6mJLn3owMJT4dR2fTi0HIZWKL1C0lco5RzIfoe3oTozOAJjt8/fVlcNv3PloHc8dqrlHlQj/36FbOgeYsBVuHuIJKvce0+Aca4pMdt98usn7IjJx4k5l7AsGuuT'
        b'YYXGdBKfQLksDrph/S3ozvZ3T8RJMyw1xzJcyz9sewdKLsmfgSVtA5YaBofVnIRpuHYZZ6TcXLE2RzP6JN6DWQWoes0HWrFQ3xtqIqAAi2NVoBtGgs+ctY/ZZaqDo+7e'
        b'CuJdtgek9RzOkhA9CMCyMzTFrTimDWUELAXROORIc/kE7mKxAOuDoA6nDbEzCCvCyYCeFaoR+1VoQR8NhGFTcZQ9oy2U4QTM3czRgWoDut8kcdVIDjFEaZ6aHNs/exUb'
        b'8XG+vRgaiIr3aHamCLvm5eKV/bBbhwz8nshzOE5yV4yLey7CaqA/rMGwvDHUZxIkDEGJcxzOpmB5OKza6rIfXS8Ew6IeMd04VodAvb+f2oWbOE/3GyJW6DoPhSRCazSs'
        b'QnscVzc7Y6wRTHhbj/MROJhMxBsJhhkLXJKG1ivG0BuJY9n/wjiyAR4pE0O6wn3GkNTtx1Ywl+2MnReE1GwP3kuNhp7riiSYLYdOWcOQ6mV/GHVju7yIWCvYokeM9BQq'
        b'aGQz8MgXSs6TvBbvxVUfN5qiVj/oj1VVwGJi2EFiqUW4tw/aDW8QB7dIucFKLs/R1hcbrmVZ0azNwhD5ORWwTLJTT0LXceX8xVRCjz5r7NiVkkT0fsIjXqogZh2DfmjG'
        b'xgsnCRfXrLTCsi5egp5A6uMA1uKcOQlH3bG99jlYJZaHxx9lWRKQ5lM61JP5m1hkI38H5lI5yGxUzoU2wsoh9wDHPKMYmAq6la8puOQNlVpQeJWGtkYNDBE2FTm6EQO3'
        b'yqZANQxHQYOI5njUUAQNTtjmAz1ZVKUQ2Vi6sYv00jAUqEhhkSshwKCGLCw64bK2KXHDDCzb41PxTexP1cgVJiRjATSRwJZgowqRaoCGN4QrMHuKprNPDSsidicQsxXh'
        b'9HEYIKKvXDAj7fQwIkefmLc3hUThMumwFgsYvUnyUGVLk9Hnbk8wV05sSbrzwsFrh7DOPAlHbnso51EHi6CAWLkPZu0MzWOjYZbwZlFJjA24jEVKWOYFXfahxBHQm0sd'
        b'KMf75jAPvTAO9/OwT1bPmIj8BAe8IvbDU+xU8LKkAZcQRvaQ4u44AbPe8SE0lbNwNzOCJrSN9GE3PMnDyhvQelE2Dptdr3rbckr9vn8WqZuSbAKFWqrT7OKtFY4t0HEN'
        b'KqRuaEMnsTdRkNgbuiKTqJdr2C0wSfPzwvJUEdbFhcnuvoSTutDCeGs/iXOflxr2XsveJL7OdiOYJpxN5QyMFXxkhQv8kwaXoUcW20IU+CSN9cFse3QNSU0r1GbBDI/g'
        b'1lgDC+yIwq36t/ChLCzDQJy3ObR7wrg66YN2Hapeo4ydsin6ScQ17Sokja32Fvj0rK0PdJy+hY36UOVncJhUwaICEecpVsqegtHLTFyi+ekXmEn0IBUf4ZOLYYQXDIAn'
        b'CAjICElzhA7141Yhu/BRBNRdPgF3T8KyKvZ43zlPlOk5fEsdqs4ERMCoCc7d2e15mYBjjCZkPIXIMg4d53P52OzlAI9DD9xS9kSys6DVLYY0812a5T5tNSJ3CQ4IYE0N'
        b'689qqeqS6qsQQ+3FgOhQkt1Vh9NHkkmKG8KhwRaKAsT7xTiSDBPHSfrKkqDRFO968rFA+hQsx3pAk1cizLoFwRMo83D2PPmaLrYR8xMsDtL9SnkppAL6cFoGekgKyjVJ'
        b'WmaIVPex0x5WoUqHhLTTBJ7cxoXrbsS0TB3WYLPLdexzJ0gpiD2dAyXeaSQAPbeh+bYGsdV8bC6OxmuT5izHXsKJiqNYHabmiMTvtTjgTYYRcfSg4WHqwwM66j9+OMdb'
        b'lZTiCV2YPUNsuAhzuQdJ5FdxzBOriGzFpPK6DxswgywDqq4amjFWxDrxMQ4K+qibBdCVCM1X1PJuBJJJS5BCYtUC9YnUm1EyCYqkoCabCF+lc4uG10H6c5zUZmY49Npi'
        b'Fw5oB4vOkJ4YTtLE3jhs8qX5HcInF+DBZeriQzd4SEJc5gz3kEn5KjafpSZKLyXcYBoIC1N0cDad0GUGi429IhVwSs/O6/RuUhMPs+8TY4dg8zlibBrCSwvCCpf4KVhD'
        b'FoSrkxUsHoCpG4pmzrIZZMO2ep3Deg8aCvS40wSv0p1nM9gjoAyBwvdCiQMW2UXDA7p1BUyl33JVMvCHVXx0BbupzkMCj5Y7e6DA6hzN9pLQiWCwGR5bOh7D8YtkojXh'
        b'4zgyL2uoc2OkoOeRQK3ojg027iKeLfO4CD1+2ByC05HHSbXWxh2HtrOWZHUMwJMjdMMaskd6YEWFxPsB9KriqA/U2OVgvXLgnvgU9jSQLAueckshCqZMjpwI0HYVEY9N'
        b'QJOyzW4hke2Bwi5nnNtjKifwwrtGRMkCE+L7QTU90vA11ObkBSy6CI3uQNDkRnqQ0IksBFyOwk7sOnqdEKsJhkmXDJCxP0UTxT9lcw4qTVIJGTpgIhiLIrHvwhGoYM/+'
        b'PYUiKPdM0gv2Ps2smIqLr8HQFQu8GwMF6rcMsYX0Vd15XMgg5mk+jeOXsczmALRIEad1B2CpO/HXGsH6ZPxFcktq2ZOGOtpE5bnL2HAUS6E7zYmoP2IPJW7ENgNYZxch'
        b'vuroHHwFBi7jUtoFwuWeoyoKJg6HxToOFgTqc0pYrn4iyIx04ZoJdJ6lVutFxFtPU6Ai5BwJyfIF6DGFIXEsTqfSDTtomA8ukSgMno/TIPSph0lbeKRIxKzAlngo3wMz'
        b'F9MvaR2DsWSqNAltVwkf2gRJ1KuCM8Txcw5w3xVWzUjbPsZ7d8T4lJeMHVbYfP5G9lssgTqU6DKeLEzlWHKVWDIHx+NwJFeObJ4i9VtEvkLT3WTezukf2IUNqmRHhoXk'
        b'+UDtnT0mt7KhJFr7VJRSCGnvfvaCokME/M2EInSZK7OZ8lVFMJFD07qM3eeOKZKmXIA1lcs4iG1JpGmHpbEgG5tC42D1Viqd6rhykQyZh5ztAB1JxLuricT7s1e0sThj'
        b'Dw6aE0/0keSMh6ZiXb4hYUMns3UTqANll46kaCvSFXWEG81Ei8rACLLyxm6fuR2WkLNXKQjJXO2nG68E7SXkHr7glqPMnjwFJru1sJSa7rYLFlSySE4KM8igqA0PcpA3'
        b'xqkrQXgXms9QlQW4J4tjojgsO23Fnqa7C6Xp0K5Cnso96MrBmSji1Kn9SlZ+hE9tiapeSblu5Dv17SYhfURoU6lnLiRyNh0ga7NWSwyNqYZ7TpK0TuzGx94EXNWk9+ZI'
        b'IS+nso39WH/dBIf2kX87hvduQ7u5DeHfkizdrAiHHLzjHHKMLlwlOS8kYSjKJjloV4B6O6y55oAdASYkCrPqaplXCP9WcIxMxoskNQNGxIGdh8liWXSAUlxKT4X+LHLC'
        b'y8hZ1jogJrxsOUYgP3t0H3W7NgGqyWSQxpGzpCrLiFEb3K7h/FkdLBZCIz6Ko/s+IGZr5+276Zoemal5iqZ4eq8lScsDqIvNgk63HKjYh+XSF7AyCdpcqO4MzJHN2YLl'
        b'50hLVJJd0ikOUIZuP9M7wcSgE/gwLyKZ7MSWM24nDzPXbNwZBt0zLC/AInHV/UCYvpUovkr406ZC/D1ng/2n872xwcuSmOKh1l4s3B+QdJZo16FkISN5npvcmr3+vtI8'
        b'/v4wXR45d0tmkiA8pHcvPY+dQkbEAhmnatgmCfBSmpHubyXF4x+HMR8enazGFq6tw/jQlwUb4B+Du5F0AsqtuLbygPFUJVbyeXw/KOWTpwjF57m2ZMjbxUprOuFzGmt4'
        b'pGDqdmV7CXi8VN8kIlIDVpNctB9XIpo/ek1hz3l5aD4aohKtTlqpzpZYoY+o1MSsdVO85+sVCCVJbpoWhDOLOKiTR6qpF7p8Vd3PE3rXQucVvE+2CgkwdjuyFRdyvOty'
        b'bLM9YUyTmXi3YTAuGksVoTcjmqSmAdbcoCDsNDYF0TzSeZLF4pN0OADDPALX0rO7yH7r2E/T9cA+0pi4rnA3+QLTlhHU7n1eMN2zOI7w9BGp3waaZ3JvEvOhxJZUa10o'
        b'1JqSmzBD3BBJtkudKRFrEuqdyUcqzooKhKf+xOoDpCEqialm9MlfKiKfrMzZIh9KHchwWyaQmCJV0ANTRmQJj0CbU5zTDQHel41TwVafazDqiEsZVnvw8SUcj/TVgFHZ'
        b'/Oy4wIwogs86GJBniwbQqq+DhUTYccKiQoLGoQuR1FYV0bM5QpxEAvuYulB7iIY65KqrEKaEXTGXmdMlJn3YLsAie3JjCogwk0g4umYPVQKcirAMtsficIK13qM4ZUpy'
        b'M+xgBSwmxCjUHiVz6D4NqSBDK1tIiqk2k4YxAKsnzpMt2QAVltAlixOJWOsDTcew5yx5VFXkuKzKamDlZaMYC089nJCDpsvQlEFysmqhnI2jMRkZOESv+tsi6nG547lw'
        b'8iAnCYzrHHDG0ztf7WoszJuLYEEZu1nEhruHcXK/L4n2KJQgW9kpVyH3fQ4KdaEzimAAmo/5RAadzwiL1CJ7qIy0+GMtJ2zM2O9AODFzQ0DwMAgTNpqwlp2A44fJFai1'
        b'VMd2LQbkpO1KD9whIZ0/RMZiOVuLsgi6StoUFvdDRxaymBOL56E0lRT4AIydIPGd9L8Dk1Hk7nXRrE76HeGWX1YEpGW6z8eTKzUI9w9r6b1mRWbnXBDzIrDuKjzBvgNU'
        b'rOGqoSY0x2VaZ2mTvTXuhkuXRFgowhU+dF26c96GxHKYFFh86KVXF2UIQh+6GR5XuYETmjK6pBnGbmJvLIlH4RUC5ulT57HCT6zpTo7LGrRkEDVLFMXSkVEBIQQ9tQ66'
        b'xDzN8EgHh+y0/Y1cYPYWeQOl4drBNjHusqTWlk6f41ZoZoL30I3aocGRaLKiQGOYSSVU6iOVspqAC9mwYAGPoNLFioRjCDtT6cP9GwehndQaQVQtY9Z+mLaEhwfSyNTv'
        b'OoIzseeJziWB57SYrYmE04NhfDL4VkisC/VJgqa9aSxdQn0ctiLkncV+9XMwspdglRDveEYAWdld8WR7Fh1n6DoNhbeTybzXO06WQr+OClvZCsDhvF2eCjCWcpGAuEqy'
        b'CpAZQzJQe82EukX6DHtfIyx4rE+i8IBcXBgOvMRLwlKPZAKdzkse8aQYZrEzjnpYn0WKuIiuIJscH8TEwqPkU4dxTksVnu6LJF5oFeOguy2jiCWOasXh40RiG2blj5Hn'
        b'sJKBq5ekXVSxTc8O64PTCdSq1LFvF6Ftwy2yowpg7TrZOnPHYFQt2PyYgzHp3h5sipDDXu80InqHuVm2gUWi5invXWrYo34n+4gISjykgojlx4j/ymHoNYKC3uxzPlB5'
        b'noD2rhUsieNIKldILBZuh6WQqkyFGgFO0+cJMvIeR98guO10zQ/HwQgbwqV2HLeAJx6XYHKPiS8BXQObYJqEp4RsbYQNk2o0jFVce+1UADU6cAjqUzS8g+ney3pEjyee'
        b'sOROGFwaJb33WBYs6WZ/R4o9+59I/8+wgDjPXdswunk1tBzcw7zbiBBFPszvwrIgeCRjA5PnZTRhFAkD5w4REzxyPoerUGGb6EzsWcctl4zttSEYYyt0bWrWUEyoRvxZ'
        b'AlPkGeDTm8E2FjRb47ji5g6j+tCmoq9LtK+CuViS1f5jLjwY1SFUGTOBNmcsMCKkm8F7UjARjt1nSXFFEO6U+kJnbARphUfnmIHSh70RGWbSggQXbN6PgzlYbgsz+0Kx'
        b'KPUADCR5kGYYoDEPk9na6UWIA48DsMI6gnRHhyXJ8z0bo7AEHDysEZmBT4OI3ZpJexQfFMtBd1IqTBF8ddEdpoJkSQrW0oPJaa8jjqmCgTwaN+krXRzaD03ZpFFagpKI'
        b'nwioW6xFqVCsYHgEJ50TsdVPMwVWYDQbO5xh2T0DW4h893HqnAGshfKc8J5IDtcE1MuSQA14LM1WRvqdYShe0weaT+rpOpPTVUFDwkm2s2CFmOIRScEiccLqdXI+J9SJ'
        b'7m1XYpjkXE0wJ1StlrrgHn9dCebP41BScFDi1Utkqc4osyf2SeOOK+CMP1TGQMs5Ky0gB+MuVicpReNEKNxXP3754i3s8gvcbYd1B3B6d8IFrHGQYpYrYVAxOdHduBKQ'
        b'k0+jr7yiStqrF58aCE2gWT0ES2LCvS95BHqRhFe5YlOmUyw+3kt49JBmtZI8Q5koAocJxQh9DmAYbDcSIVtjDsI0zu+1IMltxf5cErgamDJnMdjUZElBjqWHa9BNK2Nx'
        b'9dR1mptqJPugVh4Wdh21JUTrylW/o2JG0tVGcPPUGsuioOtwCixIQ2G2p4Bteom+9jHOJs92QSClhSNYd1wlAwbEMklmLIYQjWWa4LDZju8X6stcpxhcisFZEcnVPA29'
        b'1/qoMtbqR+4WEou3k/quIgt+Io+I3XQwVP4sPHTE9nDi7nZC7WVF5o7DuP5Zojb51FCjicVnvJjlo06NTUbtgUF7nDxpiWTO+O0mAlXuhW7bPSSeTS7QoUGU6cgknTMc'
        b'B9Ph+sTk7VIhB/WgX8cZCq5A+X6yfF0D1AkO95y10COgqE/AInmYjsu4Q4qrCOYiHEmlzMYxDK+UzTrlAKNKh4nG97FNO4qo9HgX9sVr4EM58zx3l+ta8OAwPArIJ64a'
        b'JM03gG06uJDlh6O7yNS5T0r0SQKpgjwFzwyaxC5qpH6vUxYMHBXa4eQxYxhxU8DOLJxQvXpRG4bUVK9DgwZW+cdTQ4XQaC1rH0gTSmYGEWZJaBiYfvxwSBI+3EvYMEoy'
        b'1Hl5L655EXi1wANfd1eWabqCpJLMb4KuelhQvIqlh0g7E4tWesKUrjyfwGAx6gLB3iBNyhK1WqymEUZKvBr65eBeApQ446gN4X/Zazeg3ukCsiXyPh7MXjqqR5CyDCWJ'
        b'Zmwfizb02pCQt5FITJFH3XlZXucQPtGCllAn/3RvUp8jMIKTLBX9XZg1FDuTx9EPQ+4wJq1PotQJayYaOmTLVltibT7WMtKU34QZQbrpUfq2zgX6zMLwMelJbFYzdjHG'
        b'LidojQsnzinD5gzSS6s55/HRQZezUJScRcjYaMtzhKHoHPGVK0T15AR8AtVXYOo6Wc91ZLxVE7WmjxCwFhs7k0f4GEszjvhfdSUUKMOKWzZE3BklPvHemBKzjGki22Iz'
        b'c27DUjB97If2APLOu+FRug8+DOO04hw+cTnvBi3mpDHJ+fV2xTk/Mt4eKcbakRXXGkGysSZ7hUy1gr0032vZfJIjdehNYHJUSOzMBGkVn1gRDrcSdy4445w2mbrh2KCQ'
        b'6AnjxtjhuR/qBKTdekSshqtqIrkiK7fifXzIFCjyO+tsiCV5aWRer+KwO83+DHTL44qjbDIpnXE+9p7BZZPbUEBuX5Opl4riGWyO5X5Xm2Rr/HduQSMss9WsfngcQkMk'
        b'MRliK0Vk5A7CkI8mtuWGmEXup8E14ZgLFt7BGpzXJ81YdgG6z5KhNW8jk5Bmrw1TPgok9xNUsdqeBehKJglYVcGei1BM1sAU6ZUaO6zVk6UxDsrb4MP8BDL/Sq7kwD1X'
        b'Usk10CPAGW157Din7aVN7DJhfjpGWnU3Lh07C7XKx+UINJexwJuMmXEGaYfwIY9lF8f7B5TjTpEn5m/ulJWkgKuqYXlmzAPEAbeUU3A/HRvsz5BHzazQWeeEfOKPcjOY'
        b'UjviTzLcqwXLCrAQnptsiSMmhFuLzKm7hMs5Clhy8gzJRTG5JSOEOnXkshgRuVsM8IGSguCqFlZGJiVejHLAdn9l/klNum4S6mSgXk2L5K0BFpOUfK3244IBW/gkxV0A'
        b'K7qwyH65G9bfTS5f1ZVjrmS7dx0kavTCw902qVAXsI+kooY8n8xsaDtIs1Dii/MuimS9PyG7oPNknhb2Kb0mTSOo94J2dfl8Erh6+lQHa1apl3Ohy4gcyqJdTsEwrw2d'
        b'qoddlW7iXT8s1o+SxeFQqE+ALhgnNqoJiWCLpTiczda6aOafEPhOkYoowgFbLHstyoh0NFlA56jugyAazN0wXMizJbMMBklcGkhNlylGXMmOJIHsBqZKyBodcKSxrd2G'
        b'RgOsjyODe/468cvkTW1iq/HbWHoHygnIyeG5G07oNKyY/QP2y1ZvOmHiCzE4zpal7oeRCiYASzpmGKJijLUkAmHGt+h0p058jLw2Dug4GdPsruHDeJiQ9blMN2E71wel'
        b'HHFBD9Zw+HCSIo2oGHuygP36WxjpAvVCaNYmJF+5iW3+0CegwyFYjiNlM/IaAeN9kqZGmos6BQPs9yMgHSfSV2F9Pq7BE5dwKBRjuSM8scE+40CsTGY/cvmyparYU0Sf'
        b'YlNClXIlIY7F6RLvz+UakqA/tgtOI5YbULen7tUf0MTmfXsssMP0JBkMJB+exA+r4gScV8L2o0Y4KCK3sfgCFHni4+MwLp9DANNA1k8TgXM/j5h+WQYe6PtAiyI5CIMH'
        b'VKDX3Q7aHMhWKNYO1cCRfQdlZLDstCeWK+Jdz1PkFT+xJQOr1BmnVdJxfr+Svz30OWCD+5HjRJdZaBeS5A8Q2pfkXTZUZVv3HxMYPIZCQ+L2ST6ZZXdu2BHDNYRAsSLH'
        b'F4+jCMDXrpkSJHRiaRoRbohBwfwBMj0ariZAvxNxNFuAb8AKLZx1JK+mLh7KZKAvwRBGhPDI7QguMP8cC04Tgs0F3CSN/tRBhuzqfqgyxyJrIswjTei7DS1qxJhle9kv'
        b'ydL5Mo7xodRyo4syNpPxIHOTWUBF6odSyeEjI/YuoUQdDKlj2wmtHPZQxRmiXDssX7phAmM2sOIF/RbS0GZE1lVHOIxeI4dnEvptosj+IbXteCTtICz7mV3HPhNo9YMh'
        b'qwMncVaadEqLrxE5tQ9wxo403CgTkrYzu044kIk9botrZ40J3FpCLitH3Q7VjSDeKcOCQwF0j9Z9rnuO3+aRdVl2DUf9056nbT1LoLJCNtu9l2GBWUzgAVsuAoOKCaxm'
        b'2mcQZPdKSQLTa0CbhYDbDZ9rf8KfrSk5HYKHPGw+sZtbnvKQUfJnsSf5B8xJE7Mfjfnc8pQHdmE3izco5PE9053oAvKQZrnlKQGdaJWsjtHA6aKKRFfqHLcK1gKFe/2D'
        b'6d72MK7MVs4aArkTanzsw8oAusYZ5r14eF+R/HAunGf1SbfnK2pkmA+xn3tnsd5CElACl64R+1Va0GXBmrjGwz4XGJLc6B7cO4mVgWxdTXyeR/NW6MONUsPUTbIMJx3K'
        b'w7Y72GTB55rSJQ1z19+PWrLai8s8LCMj5pGkBwVs0fbFStxemOZhR7y7Bd+Lyy3PBSwI1uOC1fPeUcpRUjc9ybMQcF9HJElxX0+duqrUHJ0oCYZceU1St8A0PmBWQ5MX'
        b'ZCEVRE1x4Q0Sm5XmBJl/Jqi6FlvW1PiPaeqnVb/WffNtx5ofGyw6fcsi6L3V3ymf6HRKnzpoL2WsfFlebKIl/vm3bB/vNX7DueVPDflPLn33ZEWgdcoffvqtPw2tLP7Z'
        b'2ezsz5sNft7k9vOW9uQG/r/aFs14lsSGe8WGfi32gmnscMA/NQZ8o+qb/2Tb1vD22lfvRweae0RtlBpc8HB5d+xPb/z/pw91R1U0nQ158z+bTxQNJ93qwt+cXDV73F1h'
        b'f/vrZ9JmnYtnYtT6Eq++1yR784dNf/jVWkbEDw7pWK18u3cm8id15779+1+9qZuh7dmdkfsje6v8iN9unlj4jrdjxtPRtK+GaUkrnQ0bfXvi6z9bjz/m9Lgy1bw07JnH'
        b'H/R/8v9JRTWLFX7wQXXqkZ8q/yzMpMljsb2uR31E4wcFyp7e4YcOhQp/YBdvo6BRWnH+mt2I+QOPm792ztKvizhS1PVTa+tUv9fr8/dXKSWf6fyRdLjrZvlS0El9+d++'
        b'7lbzxr9Ndod88A+CI7lZy3YuHxT+Mu67bvBj/R9pO/1L5zu5l04E2n9/fOUbw/mnK07p3vtm0d2cf2gzePiPv/jm2x8UPk18f+X7KHBJcBjOVc4+m3Bt5R/+0bCrqa9R'
        b'enpcZ7rwvdtmVbUNWD22qv/uyWcdgtE/6gzc6NhIPVf882eGTxcT09yPxqvIqmqciDcaXzS/MWb/yNj03C/fbNe9+WOX2BGVZ3/OW1abMntv4ep3vtHuOm4RH+mvmfjD'
        b'dy80v9soG3dcZfO9y55NkYL5SZ15cb/7gdLIA9/rdHg3bk/enqy87nfalmt+9/s33jVN0P6+x7/kfrD0Q5e2G3+K/rr3PqfZi1n/nLvlnVvVEh1Velts5lL1aPT16Pzz'
        b'MacS/3hbX815uaD933b/+7vC74b8s9Dl0Oq303Vzb3zzooV04q7vBB6a/Of3Tn1wKv4HfzhiefSB1OTyW9/TXKzMzJfKax9y7070WlM76J95MFhxzsd/Lv+9QY3IwUOR'
        b'w6LtuWffXQ3ZTLgWtfIft3/cl+Lym8N+zr8w/Or8+E//M3f4gz83fnt+puaPb/N+uXD5l65F8z+8m72j9N1oxe9u/Ofsr/5cm2Mz9721byqnXmpysFCQxJGdx1EzQgUG'
        b'SgTmTTysCcJGboM8DAXCyvO9Q9gn/dHn3A/jA24X/mVs83o1xau2wov4BC7YIElX1kH2TKciNupkiORFLG6tSka2Ein5RQFPP08oZyF8xp5jJEgrhGrFF3Vu4sLN6yLS'
        b'JvUyPO3jAlJAA9jyjCXPRhaItTDzhtL1bFwkN/m+ClRAlYqcSAGnVG5I8yyUhTgh8nnG9hicJu/m3vOqH6sG1ZIbxDvL8AKFMkAKsZOLiHDVg9Tyi7bCknhyOCy1H1p5'
        b'ktzt5RZYnAnVctSzmUzSmuWvtudmTe3hvAy5dGNHuNCwDlDA/7TQsGyNF+5KYsNGpViEvPrsttzfUfE3jzPwt32CPoTHBTk4/jn/PvMB+8/+J9neIRcVlZwWHRsVlffy'
        b'iNu/0a34YeC5T/1XwNs5x+eJNHaEsvJaWyq7yjJr7ctvVt1sNarIL8tvzWzN7LHviR441JbXmTdyuv1O650pY3plLBnNZS+dnsuZtp2zff3E6yfe2PUVn6/6vGkfsG4f'
        b'8La2bqt9a3TnoTb5Tvkevw1t2ymtDW2ndZegDa2g9ZDQ9bPnNkPC3tQKW9cKe1vTsGcXC/O5rmrMwjKG83cUeLvEte6NGmUeZR6/35Hly/vyt3btqbUZVFq38dow9N40'
        b'9N7Y5bO5y2ddyYcFM1DgabmWKW5pGK7v89vQ8CtT2CFZt9zUOlym9A7bJ39iXc6AOzhKBzsyAvmjO7zPKhRU5Xfv8L64MJaVP7DD++Jil7689g7vcwsXaVb5cwtlofzB'
        b'Hd7nFkpyrL0vLsSq8vpsCH9RYcrT0SsT7Qi9+Oyb/2IZIrVH3nyH95cVtXHvsz/PPvz2BJ+noLojlSYl77zD+9uX73PlM8mxgLpWpfm8c7HS9GlLXmtH6jUBm42/l/J9'
        b'rnwmOaYea1cZvOi4kKvlIcfTN1iX035HXoXrfryUvM4O768v3+fKZ5LjV27I1QolSmnvSO1lwvaXFe+z4hl3JGlQcrUfP1JansWx/D/0z/uSP88+fi5PgZOIi7Lyxju8'
        b'v8eyR/997u8zrnwpJVyF4ypc50OkWeW/r7I1+X3u7zOufNltrkKShObHZVjlv9/yfa58Jjl+MQDutJdSGF/ecIf3P1FmSB1j2uOvKzyk+AxCP7eQ4cvvY0efXsiIWFtf'
        b'XBhyMxUlxRTQf1/5Plc+kxy/oDx3+oQ016GzMvLWO7z//cr3ufKZ5PjFwLjTx0VmssKdUL4plSF8ybE5leeef8OOE2VIxUhxikhqx0fOgr4K/1jVV8tsmRNCObqAK/3l'
        b'/OV20wdWrsvp7ISr8nYZMfvlJF9SlrlvcXmHRewLVtby37Y8uuS+aem2lLVpeeI7qkY9Rpuqxj2nNyQbQTWM/hfW1v8v1N4RcFVVPhxLJgt80+N+zMOCBxa6noLnEa4P'
        b'ZazxP32f9P9tReYhKi5/alC4v8Q3yvgJ25b80i2yYi1eZunCme9zhs/nq7JN4f+veFF8aXHBGV9/RVreXY/3FT1ldwtBovhIvCDzNJF+1vqDlBrfYCl31eIn8T8siNbW'
        b'5C/2yNue9rzw7q/3u1w36xxy1lZ3+dm3BgyyD19yzn0/eHvB3OjN7N9fGvzh+Niim+/MG6alF379xnCBR4X50D2/0CGFwdDBqqTGMw9037ti7N2nuv/diG8Ohv/G4MHg'
        b'n9drvn1My2w2NvXRN6ommhoHz3w3bb+j2R3HIxccs5wdni0NJWo9/bXzKf4fLf/t+zkP9obY3bKMvllncz05/Kf10cV6JRZvHXq7b8y+eexrC+/fOvnwF/o6v7z29jun'
        b'Kk61/KqobzQy2dfu67fevT61khvs8vvKlA/umJv+c6jLv3raNTX8e/dv/mg7/Ys3vz6VMK4c9q3GkZ+NBT60Nk29rlBuGjk1xddLcfpZj6KWwcJ00cXfy617lt0+8bMf'
        b'80rLrt+LMTb/kXDYCXlxnf13FS+8q2Ax9kZ6tW7G99/RvDnSb2dQ9e5bBQ/aMvfD+1o7kcky44EWe7iYEpHG59hKf3AwF2dZlheLRYowI4UjLNmpZDmuFTri/INtcBoH'
        b'WDilYLa/Vw1XBNC7FxslQTFnYAHqoRLuS/IbHYN77KdxWZ7yLoEBtOE0F85H/xYW+fsG7sdhy0BZnoxQSg5LHbnEYxlOQVi5X4aXjkX8Mzzsx1aY4TLtOEEvVlhhjbkN'
        b'rrD8gVjF58nbSkE7rulLAm2uQQGUSpYBdYXSPGEQH6bstbiLr2D3LrYz2QbLoecwF7NXGSsEQdgPndwaZGYeFnBbl+s1n4dGZQ9fSoJ0TqhAs6TZM/KBvlht4Svk7cIG'
        b'ASzzcViSlukxLGj7+1kHYZfLIQc+TxbrpWRwJZALkHQC7qX42zv4QoEmVvtL4jqrGAmO4qqSJBkbPMAyrkIpjvgGSioo40OBnQm2cc1b++/GSksWQFWMqwKe8DQfnmAj'
        b'VnI9j9OHaRZzKtDah+gvtOPDBDw2lERHbcTHWGRlg9UBUJbF5wlT+LBEE7PGpVlS0MMVK5YwLIDdMpAGL+TpQSmU3BbC3d3QLEkQNoaDOOjPukXjZzS/pqdoIYW1WUck'
        b'abFqb5/K/MhZ6A9S8JWCKZyjaeOyMizjKDQq4owKzmdCOS6m49x1qFQR8XCWPMh9QtnXoIejgzk8xgkuGIsVa5BFH7+mCO1S2HcMFiSBYu+lssd+WeKvSD+WaZfL+1Xm'
        b'wi1xxuBImD9MmvvGxttwqZy45HbBvlC9P8jGQobnfVI23+yCJFVXHa4dUUTqJN8E6nl8rOPhUKwud+5qEj5kW04DHWMDggme8vnECMXmHG9DIawdYSdtWE7mFzFUdDXx'
        b'abYQSs7BIEf1m54GRPIKLJf1wPIAKZ68qRSJQyuMSrKMFe3DRSs/G+tAGxZ8rBbrlTQECoZYzAXLir6Kw/5WLOvWxE1bLl3ufeq6uoOA7SkkCWMhynQVod7Kx9qSxRgj'
        b'imvjoiLWSuHDyGxOgMLhro+VnzQPemCG78/DVnxia3Hsb7Gc+zdX/V+SAXGMis9Yd/2vmRIsfgszJRJTE7Oer7DqCz5zhZXsC32etHpBEHtticRviQzeFBk8yNkQmW+K'
        b'zAu8toQKpQF3A9bVjAadNoTWm0LrdaH1llBU4MteW0K1gkD22mJ6l722hPbrn/3eElqtf9r7I5d/8kBz/cV7S2i7/mnvLaHJ+sffW0LL9Y+/d6RkpDV2pATyOltKRuuf'
        b'eP/+bRVd5svpfFhsKWmXBbx4kU0sr8NR7CeKmnSa2npZbKmKy6TZiypJa1CVd4QG6x9/bwmN1j/+fknDHZnTR6SZof3//vx3/7lK6kpJTGbgAYa7GjIe+jzQ43vY8UBf'
        b'2cNGAJZS7Niaz45tBOzYTsmTJ4BjfColLpDltiA5LjWjh+RsWzorOz05bluYnJiZtS2MTYyhMi09LnVbkJmVsS19JTcrLnNbeCUtLXlbkJiatS19lcx9+pMRnRofty2d'
        b'mJqenbUtiEnI2BakZcRuy1xNTM6Kow8p0enbgrzE9G3p6MyYxMRtQUJcDlWh5hUSMxNTM7OiU2PitmXSs68kJ8ZsK52URDoLjL5GFyulZ8RlZSVezY3KSUnelgtIi7nm'
        b'lUidlL/i4BiXyjKYbIsSM9OishJT4qihlPRtodepE17bovTojMy4KDrFQm5uq6WkxTofjopJiIu5FhWbGJ+YtS0bHRMTl56VuS3iBhaVlUbeS2r8tiA8MGBbMTMh8WpW'
        b'VFxGRlrGtig7NSYhOjE1LjYqLidmWz4qKjOOSBUVta2cmhaVduVqdmZMNAsLui3/4gMNJzuVpTD50LnMtOS9THL0hf8MDT8EQ66Q58wv/hf80vRxYFTh85Olmb/xf3f5'
        b'5TpbhvLujryvOCp7CAUfyF0lMYiLSbDdVo2Ken783AX+QPf5Z8P06JhrLDkPC+PHzsXFBlnIcaHKtmWjoqKTk6OiJNPMBTP7AU3xtkxyWkx0cmbGV9jqhA3JqSQAGhfl'
        b'jbHFB3IuxM/ZyXFuGXayLAYh8cZrVBB+8/k7UkK+cIfHCiWeoqhAdkeYfYQv3uF9pEzPJrdA7S05vTfl9Fr9NuTMNuXMdnhS/EPr1m6vm75u+hXzr5qvW/vRe0tOdUtB'
        b's8x6XcthQ+HgpsLBdeHBLZ7qOk+1VnuDp7vJ011/8eb69z8AIYicmg=='
    ))))
