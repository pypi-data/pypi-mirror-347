
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
        b'eJzEvQlck0f+Pz5PLu4z4b6CgBAI4fTCCwSVGwW8sAqBBIgiaEJUEK1aK0FEg3iAqEDVCooVpVZbtcdM73a7ILoC63Zt193tdndbbe2xfrvtf2aeJAbBVru7v39ekMzz'
        b'mXnmmeMzn3l/PvOZef4EzD5cw+/XK/DXAaAAeaAE5DEKZhvI4yi5K6zAqI+Cc4phQ2orBZcDlPxThpi1QGO1lIMpAgXPmGYrg68tlKZ7GFDFtyqRCO6vsM6ZPS9BvKpC'
        b'oS1TiiuKxZWlSvG8qsrSinLxHFV5pbKoVLxaXrRSXqKUWVvnlqo0xrQKZbGqXKkRF2vLiypVFeUasbxcIS4qk2s0mFpZIV5XoV4pXqeqLBWTR8isi4LNih+C/21Ijb/H'
        b'X7Wglqnl1HJrebX8WkGtRa1lrVWtda1NrW2tXa19rUOtY61TrXOtsFZU61LrWutW617rUetZ61XrXetT61vrVyuu9a8dVxtQG1gbVDu+NvgA0LnpvHUeOn9doM5P56zz'
        b'1FnqLHRinZ2Op3PQWeuEOludlc5F56UDOq7OUeerC9KN14l0fJ29zkfnrnPV2ejG6QQ6jo7RBeiCdU7FIbgvLDeGcEBdoLGdN0qsAAfUhBivcVhiDDNgU8gmSQ4IGIO6'
        b'DqznLgHrGKttEk5mkXmfRuN/IWkUHmWDKiCxzyyzxOEtEziAB0r9OKBAGlrqBLQBmIjOJqajelSXlT4f6VBDlgQ1pCwoeWpeuAAEz+ah1+DhlRKu1hunhHtQW01aijQl'
        b'HNWhnRl8MBe12KMd3EzUmaN1JVk1Z6nSUmDTamkKH/B4DGyDnWiL1pfce3oe2huG7+tNx7dmpKAGSQoPOKMmLnzFI17C0frgRDPhi7AlLRrWoUMxOEUa2pWFM3Lw505F'
        b'TU60CFFwH7yCUzwXFJOSksHG26MXuFHwdBrOxItwNNoLt2pIJH4Q2skA30rrFA7sQedCtYGkfefCyzbonAM6r0Ev4gfWoQur0YtrYL2DHQDeATyLp9FlCaN1w0kD0PGV'
        b'qD49zCUV7eQCLnqVga3w0BwcS3iwFO70SIOnQ3Bz7EhDO2FdFikPbIjIDJcIANounjvbokbmYMhr3Fqoh/vUqBeXKj2LD/g1DDoWuADHeuBYD9yMYanh0oxwGQPgCdhu'
        b'68K1RntRrSFeDPdKw5KloagunVSpNN0G6TnohdWiIsas42OMHQ/x177oWtz5mC95mB8FmG8tMa8CzLU2mGvtMIc6YI51wlwtxBzrgnnVDXOsB+ZxL8zzPpiX/TCn+2P+'
        b'DcDcT/g6WBeik+hCdWE6qS5cJ9NF6CJ1UbpoXYwutjiG8jWWDnU2Jr7mUL5mzPiaY8bBzCaOga8fopr4uuRhvvYexddZLF9/7CYAPwg9cTMV2B5fogWUuCAP5+1ri0MF'
        b'6Q1rglmiU5glOGQfhGkFtnVlRSxxmoYHdAzupPgCW35wGugCZdaY/IdV7rx7ziD+jrCKWVrdEfVBbhdTRkSo+1PNTI8FEEdOGS+7GS1a/zKgZOXMrx32OjAhd+Zdd/9x'
        b'MTc6EQwDrQxHzIZHYDceYvUR80NC0I6IZMwwsCs3JDUD7ZbKnGFvSnhqBgPKHaymT0GN2kR8SxBqQNs0leq1a0RZWg26gHrQi+gcegmdRedRr4OlrbW9lZ0N3A11cGd0'
        b'ZGz0xKgJMfAC7OEB+OpSK3QannDXppJh1xgRkpaempmSkYZ24+G9E+3A46IO514fESINlaHL8IwkPAyegZ2wOxvncA4dQI1oH9Kj/agJ7V0EgFuknXM83D2C0UgHEKb+'
        b'WkEYjUMEL2Y1BrMXv5hLWQFPHHU8EytwrUZ0NA5zzTqds4lrYIWHqCZWKH6YFXijWIGXqSZ9qdr+QxhXk4xD6yzWtL4/7bD/s1H1jQy3Mu549Avbd/zu03nzkf6tnZJX'
        b'POckahVnP12Y80Hfe4fe2vVW+fOe26+nz/u3d/NX339oW3wrnQtkV+yWJB+V8O+RERgcAU/gPtwBX4abcVNiecCbwsCzq/LueZJ23r4YbgmT4Rauk65ArzBAAHdxwuEl'
        b'uOUeEYzwMmwUhYWHJIePRxc5OPIgJ7yQc88dRy2DrRZh4aghPYqLLvCBII/BvfcKOn/PBUd6ytBWVJ8MT+M2gztQ10ZmTo2FhDfMCZGoHXH8gy8NaQjx5s2b77tMK1ZX'
        b'VCvLxcXsvCvTKFfLZwxztSpFNfnikNTz8Nf3m8GdORwgcj0wqXFSc2zTdF3SoNCFvWiLa4lrnTYgDLkhlPULZQPCSBLpdiCuMa5Z1SkaEMpuCKP7hdE3hJP7hZMHhHF9'
        b'tnFfk45RW+AviWDYqly+SqnBU75ymCdXl2iGLfLz1dry/Pxhm/z8ojKlvFy7GlMelF9ABmqBGFdB7USIzviLljeJxMbir/ubwbezOQzj84m9W/3KzTZ3OHxGNGTjXD/l'
        b'E57DtoxBS4chS+H3d7FodTRe3f+a8ESTIAActZFxizhjcVAxYWGugYV5lIkFxTwTE/P/d0xsPYqJnTK1Ihz2njtdg3ZFpPPxlNpFpoMX4REt4Qd4vAyeS4O1XjiKkQBU'
        b'iznlZTr1lsLN8Arqhft98dzC8AE8D4+jMzQ3Xgk8iOrhHlsSMxugfcHoqJY8F76sgr02AjmeyRknAC+h3mxKXxuP9oTBljJCnw9QK6q1pfSpwbAnDOrQcZkAMEsBOjFx'
        b'IX2AGF3CUqkJdZTPJ50GMlBDMI1AjTFwN2oSzEGHAZACKTqDJzQr9tmn4MGEqZxKiGPQs/hvvDelZ4jhyQ0cdGo5Jh/Hf7BlkpawQjQ6uwFeEpTPwPQD+G9JHIs4GlBn'
        b'NrokwIOjDV9dwH/weCBtK7TTDiOBS1x4HpcKFwAdVsE6WqzKmegEwhFXJuOIK/gPD1q2ebtROx9ectDSUrXjv9noWVqsZHQR7kRHObAhlwBOG0d0hBYLi9Jz6HQONx+L'
        b'iGAQnAHbaUap6BRutiYLdBSdBCASROJibaMFht0bQlETriM6gEcK3A3y4VbUSRGCMBPWol4N6l3LAA7qZGDvwsAgeIYVa0xnI19zBYdmtdds1EfZw0jb2T7BGV55i8O+'
        b'eD2q+pkXKk/ys99ZuDVoyub5gW9uXnwxISJlW/zs2Ftvoad//PHbBX/Y/M3m7pXihOQ9oqBjkuM7bcO/eJt/RRh56u71rINNm4QlIX5vtT639RvmfrQ+epbrlrciFn5/'
        b'ddaBbNcfPl6WkMMpQ4eE9n/6aOHiQ4f+ncecWOaZ0qP4d2PB9ZYp6JWtvWVrHMInJqy7mrrQwn3bb7svt/92wbxDh1748adLcX2fTlnD690AGp6OOD7+FpalRObBS1J4'
        b'KUwmQTukAAvD7kTUwIlBLUVUlEbAPZswFII74RGkS0nP5AMbeJaDDk8qpnLYEU95p1G9FONDjFAFy1EdPM8J4MJX7/nj2BB4XkJnWjzPbYOXMP7D8d2pfCCM5aI9S9Gr'
        b'NI/V6fOIKDeJcXQQPQ/Pwu1rJJYPidVHfmlIr4jFRF4ZJNawjbK8qEKhzCfyttr8gkrcAVbi3p2HJa7LoJu73nLQx79T1JP7uuhBwNvvLp/j5q+be0cAnJwPWDRaNFnp'
        b'EoYcPAZFLgfmNs5tTmxK1zODrp7N8kbVoLtHm1WLVXtgJ3fAXapPuMMFbl7N8j0qfLNvUNuylmVH8hut9Dx9Ebk7pTGlWdGeOCAKaWRwSt/wW45eNxyD+h2D2os75QOO'
        b'kbqEQUf6yI6EAfcpHQnNazqdOlec9Dvo1J7Q7z5lwDEOpxCKyPzQNKXP1vtfX3GBR5yGACzoZZUILGEQD3+zE4DFMKMZti6vyNdgRa5UqVET3le7jdGOFia5bxD8YiJD'
        b'zJsvxWwC+C4LTwBeTzoB7BUEgmM2EY8zARAUwx8xAfz3UMwoRW00irFiAe2CNUIQm09QTEHNqaIlLEy9GJACjknGM7i5rEN87cEcSl1S7Ah0IQmYqQukjYkObFJ1uTX4'
        b'rBorx44FZd5LfQGVYZPRZZuYSF4C6sA91gQKw1GXqnXj9xwNsRbMjDrb+n704S11HU0vN62ZEMB1PxZZHBMVKdIcrYtWXoqMFEUt5Lx1rr3w3YIJe78obKn6hyLUmXNS'
        b'/nbuwHu8mNPuZZnWadbPiLj64mT5vsJOzo4bW2/CbAQu7Atf+swW/+YtMXZg7gmXXpczEs49wgewBXU5wFdhC4VFBkw02eoe0QPxfNUL94XJUqShEhnGyKgOSOAu4C7m'
        b'Lff0l/AfPSj5gAVBhhHpVFSqLFqZX6RWKlSVFep8jIBGk+joLDCMzkoOcBTqY+rXN/vvqGnRtMe0ru8cd3DjoJv3oLPLAUmjpClMlzjk4NqsadvUsqmz5JrfRBKH70nQ'
        b'z9JbNAc0FzavaQ7ud/THw1YY2D5/QBjcGdsvjOizjVCTTjAOD26RSjFsUVShLa9UVz3B6CAGjzEqsdR8jGjwGPF8gjGiJmaAUfieMmahYWxQRfIBumdGjIv/VNEbNS74'
        b'o8ZFEjsummOFIDC9CmPFgmn/lxNoGAI/BDkCcekBOgRi51eBXBZhnIO70CtEJUZb4NYoEFVdTVOLFvGA5eTbHKztSe9N2QDYebx3hnMMflowfD4aY42LcD9N+/RaDuBZ'
        b'bsFNUyB1d54OtKQP4B5H2B2D2UbqFgNiJsFnadL8PFvgXvZ7DphXkF7pyAFa0n9+sGlSDC6tN9THglgZlxbMCr0Cd8XgPOFRuH8CmAC3zqY5RDiKQIi7nwUu2FMngoWA'
        b'YhXYAw/DF2L4dMDsmAgmesAOmvqZDT5gcvJX5HneAU9VAq0DJi6UzYjh4rYrnAQmBSM2YZGvGMTH37DAreNtURrLJizaII4h+KNhzWQwWbWcJhw3LggkJ9cTNbhw1mou'
        b'YCFRFzweCntJE52Hz0wBU+AedJomrw2UgHlJO4g4KmyLyDIU97w3nnB7cUuiS9PjQBzWV7tp6vpYKVgsbePj4s46PVPNpsbY6fIMormgk2jfLDAL1WK4RZp4jRSe1OAW'
        b'xirX8USQmFfDJm+Be9ExoinMhxeSQBLWZLtp78EWeAHt1OAm1cDDs8FsP0dayRlBmUQiVNjPAXPQeWvaIyt94jS4hdCr5XPB3GJ4kr1/D2oNIGMtBj2fDJIXwYNsR79W'
        b'rEak6vnrU0CKFulp4jCOPaIV3IM2p2Kk1xlGexWdtyUAnBR6KzyTBtKs57D0KzNQN+rFhZ4EL6WDdHgojTZIhaMA2IryLYC4QPo3sZBlQ7irYgPqxfVwSMkAGRgZNtG0'
        b'fiIbIIq9ysPiPP2bhdVs2mxveBT1EhWhCZ3KBJkcW5q2SzsepMdf5uN8CzXp41jRD9snrUe9uN4WcG8WyIL7Dbzx49wwkBvZLcAZjwu1FbBdjkFrDzyLegl/XIDd88A8'
        b'VKtmrSceHiAy8jk+7vJpr0pUhqFzCaP0PcQIG5A3H/fM9lCadu56K+C4Pp6H00rjFK6GobPDQmhD2q5rfTbI9kAXadJz4fbAe3IAAyILbP9auIpNinZo0W4b3JzJsDYH'
        b'5IRL2AaqhV1Ib4Nbkw8P54LcpFyaQ3CAF4hNOmWB6zEtOjKUzSG8Eh63YYi+gJoXgAVKZ5r0Qo0vmOY+zMEPqwmJdGfHKawNgc02uC3LMheChdmsWNlrMw4kidrJ4B8X'
        b'EjfPkKk3rLPhEukyfxFYBC9E0KRe1m5AmnRRgBvduyUzy9Awp9agBhvSih2oZTFYHOXCzs1xMvBUvJcFLkChrlpiGDcXsCZxGdaTYBvSLQFLZpTR1OlesaA0dhkRCtkf'
        b'F05hp/drU6KBQpxFSpb958ynWKJgRiQo4B0X4HFeuGtyKZBw2BZ7yWc6rMdtPh/tygN56JXVLEfUMWgHrMftu3HpUrAU7kPby77/6aefJo3jA8vKU+R5ZX/a6MRm/de0'
        b'iaBscSIPVy97ztSlQNX8f6V8TTx+/qRzX2r738vkJDgKbp38W8uW+WvywTqLSW9ufMMnvcbK+cq/65wqkrcmVvsW7JxUeHn9n99My4u1jYr69pO/H7v04xeV35y4P67+'
        b'uaTba5s/BK+J6lZ4L2602fp+9vnXvt5Qef/rMIu1txde/8nlyy9i3tjy+8JAvWi6bR2a96ll9qchb7+5Jl3X1Ox8Iirgo8LM9NaytxW946dWnLMZf6n0XNofum/2ll0N'
        b'G39lxdWVd97y/t1bdmU7lg66fj3oZDPo8l1PhO/mtxK9696Z7JS1ZrzrGtnyW9mXobb+9zu9bj53b9X5KYGBid92fvHmlxOXhZVIvvjr9Ol/qfOVPtdnve+lW5OW/a0i'
        b'T3M7V/j0/z1//VbwF6/s+83ewH+hG93KiMRn9m3NOLhhQofPlOGP7pVHrPvr9w7TrcvaPn/v+3ve10U5z3JOJVz5pOLkLLtvj2wCCzbKCz6pwwoRsVnHz5+GVZpMYt3d'
        b'LWWwwnMqGuk46AVUN4mCJdRQWmjASfA59BrFSrBhxj1qWX8NHYRNaaihPCcMNWSEpxLjuzO6yEW1SniKtU7txhKuEas8O9NSiC0JXa4RTOZ4oCbre344evZMuF+Dlapt'
        b'6EpyZngIMe6j3VzghPRc2LPS+1coRSa8MmxvgCraonwC6KsfuqbgaxGHBV/JXCP4itpBINctoate3czoJx2Y2TjzmjBw0M3LDIVhZONhT5DX/DtcEnL3ajaExAHthlBI'
        b'WKchFBnTYwhNnnoxmw0lJL1eyIZSM95Vs6GchX2L89jgU/l98iIavEWfwich+hQaok+hIfoUGqJPoSH6FBoiT7lLQ/QpNMQ+hQbZp5Ag0flE+DkWbNjDu9kU9g9szzaG'
        b'Q8M7C43hmIk9amN42szXGWM4iZnLvGu6SmeymL55psxymUUMebzhchlTwJAi0EtLUoTsO1Zs2NOnudAYDhjfrjaGpRE9nLuGcNy018d9RcK6lDu2wMVVN/sOx9bO56Zf'
        b'SKewM6ezsNP9d37RjXMxPq7EWm9z1B7tLXefdq8b/tH9/tE9sQP+ky/i0PR+9+ktfFJr33aPztgOv373SHxtB8Qxd+yBz7j2WS2peqtBoW9zVb9Q0pnT49y16KowdtBL'
        b'jHVZ0QRcDpH79/f4QOTzFWDsfIbcvO9w8e99DZV1gQk2idEARVslzuCi6Qz+NpopuZgRH42+qU3SDHyThbWHOZhYwCny/hcxT3IZxulJtdM9gnHgOZtw7i8icLKQA8wQ'
        b'OPe/hsAfw75uwSJwNBPD3PhCHoG5Z3OKDQi80scaiFZPJPqmbXrhOnZOc0NH1sdgKN0cyWMVzgrUpqq7KuBocnDsN3VvE/N8R9MUYp7v3n512Yfptod3Hv7wVMeKbPfe'
        b'Fnf3He5hLXEtOc057sc2389xz24+7n5y87nztvHXl+amT7BdfV065Glr+4btIRV4c6u97LXNEoZad1APehYeYsUlxgt6VrVEOlsJb0yhZbScswLLk+1eTaVaW1SpxRpW'
        b'vlpZrFQry4uU1T8TRwXZbMBa1WfxMDsSW3nTNF3SkIOzPra+yiDTBh3xENdn6y2bY9s57U7Nk/sdA35WVRQM8zT4KY/PpJMJk/5MSbeaM2wCj2Gcn0RVJDc+BqOOVBX/'
        b'e4xa+jCjckcxqiCTolgZ1hZetlFz4ckszBLdWEeYAI9TZp2ciyEVeDeZG1+gLo5JBHNUmtNHgCYBR81hNrNMGWVkyp3xVcXp/xK9fX3estk3MYOmH169yTrnJZvSq/P2'
        b'nt3jEfLRZkcHuli0Zqlt6Lt/lnDous0mZ7TXzK7BSQ0Xw14616L9SAdfDpOlwCZ46oF5g9o2uOiQhPtw95IKmpjT/SHF/wFrPjKGMuYEA2POM2dMsp6DJ9b22GvCkK7E'
        b'Ht6plIuck5mYR4eE4Z2KAWFMn23MSEYseiJGnEEY8ZHlqjNnw6xfxYaPY83j65j//6x5AlZmzrWyJ2vX7rdiatInpq5kMfVeDwy0seC5xakpeznakiU2h3JoNndK1pe9'
        b'KEsFqje7nmc0yzHly+33qX2uiVjoujB/MsLu4m1957HInGCr3DnbOl774eJrCX8TvV02XrB93MeZfxE9HyoTbJcVi+s9pG9/aBUb4K7b8tLZY50JkW+kv8D5VPa2b/BH'
        b'tkA74Cx0hRJ2LRIdgeeF8FQ6aoK7MqS4KGkMPIf2LKY4cxnauhqDVLQrwhduz8pADZkpsJsH3LJ5E9E2zRNY5ezKlesr8xVaZb5CXqmsHnlJ2TXPwK5P8YDQbchL2pl7'
        b'ZknXkgGvSXpLzLTN6/uxpEw6k9WVNSCd/jpzVZowKJZ0JnTY6VMG3cTtUXs2Drr73BK66dIwOHD3blF1Mq1l/W6heh4GFEK3EXY4HnnosFWZUq7Az696EkM1WZh8qPS7'
        b'gZkZbinvydYqWTOc0YeLfARGjiojTM1j/ZswW3N0AmqottBZFgsoa3NHrFTyrEYwLg7zzJiYu4lnYO2HqI+WslajWJvPsvZBRQxIinufNI36T4EilotV1nzwvYMLMSSV'
        b'Na0sAarzFh8BDZl35swZan1/Ipav4Qb5et52gu2SD9ff9pi6pP5e6mL5p4e7JTtPtYj/4S5e9kHuBzffm49y+bfXrQG/KUSxp7ZPmbo9Pn5Lh+7S9kY8DMKeVU24Nn1B'
        b'wddpk+Wfbz53aMLOw96RX79Rc/kFbsuN93aV+e60izm6//j2IGp9fsbFO91tO1a4iIAuz5hCl4ks0JaVgAOfYxb4wmP3qL2mOSeA+DhRB6aJWbBt0VKqQ9lCPWxOy5yG'
        b'6qT4zgasfFuinRy4TSpjVaxjsBG9imN0EVjo8zIY2IDVstfQ4TjqADBXg06i+gzYTYwBR/ATtzFzJwdJbB5Xs3qYGYm5xahomQaWbYnSbFyNuKLD6hnDsFqNh5XXAWmj'
        b'tEmmSxwUuh6Y3Di5KU6X9ImDy003n+bi9sIBN0kjT8/oowa9gzqZlgwCvWmy5jV7pg96+XXg4XZU2u8l0yfddvP8xNGnWdGeMuAoI6GittKW0tYVXVN6ck/N7PeNG3Cc'
        b'+rUV391el4z1A5G3Lsts/FmR8YcH3RxSfEGRtrKi+NETDFtzKzoMC8wW3tSZZCCOqG4LSTkFf/0fHocVeBwG3QX460mR+QFBMDhhEz0SmZuM03Sm4ZuQOXGxAsX8/xeg'
        b'x3XUcPRjh+MbQR+AvQwI2eRUYFXj488OR1svMYgHYPWtdQXTvh83jyVuWGkJcHvGC4oL0t935bDEM4U2ACP3yMPCAts7G8NZ4uGNQhAIwPo/2RdMO5gpM1iglD4AA82Q'
        b'vryCGreCuSxxC48AK7A6Jqsg+6ngZJb4sYUFsAVg8cSwAumNuQY3rKf9QsA8TFy4sqBQOF3JEhfGzQA1+Dd3UkH2kpzlLDEhazpYjx80mF2Q/ZtlziwxoyIOVGLiTM8C'
        b'9d+XLWSJv7f0AJF4VHyuKpjmO3cjSzytlYLFuEhbFxbM+us8Q8ofxjkCMeYiUU1BGVdawhIzq+LBZgAsp2wsiJZNiWCJSxPpJJ28N6Ug/R2OwbGsm6hAAMyrXFhgeznC'
        b'4EPmo/UCWPCXfiYseOpe2FKWOM95EsCie/3vAwqihWsNxrR5y+eBdowGJq4rWHF6qZQl8scrwbv495v4guJvp5WzRH/PEvAhbqVBccF4uaMvS0yMcQNSfLskrKAmzNHQ'
        b'SvsqHQjCKP1mYoHt5xuzWeLNjA3gHu7Nu84FE3+rrDL0kVcMwCprcii/IHsGlquU+KU4AODZrLSfWzDLVWULVLFTxvE0xL4YZKFuaErLRPG22w+nj/+ypOr85mtFPfL3'
        b'7Kr5ae0LC/v59e9OeV38ki7x9p7BgZS8oIRxS3b+tfenP8bs+ur0069b5LQ8/93rM9oanj6oSv8XM3dV6kBZ8z9ej/3s/Ix4i8+OjiudAE7u17hbXmhcO+3FS+9+tXeC'
        b'79v1nu/96x+HXvSfay3Mzk48cjol3C7k9fSTVb/5w0G7FdmLBxe3ZfappBK97sU/1L773af2f/J478LH+9b//kenhaLswLv8hpa3fuffwfs7snn97G2Jy6dBSSertQcX'
        b'HXj1hOxEyJScd773cbc6FeU7ftWX+ri4j/Lvx/3z827tbeujHi8f+f6PT8VNWXvp9S9c416Yn/GD1830H750q/T8d115wzfbRDYXqpob53/zyufn5v9r8kcTTtR8eT9/'
        b'xpWl832OfL9ylaQt65u2vC9Xpg0t/83fQ/xuTrtl/e8LTbf//GWV64KXnrn9T7fGF7YGVN6XcKkSAC8sgq+yWAoeXzkSS3FgHZ1QUAO6ArfDV5amSUOSUUManm/gKU7V'
        b'PPgMq+SeQtvcwtAutAe+HBHKAJ6WQXXoOOyWOP/KOeVxph1n47Rj/JjNPk5EABfKy1fml1aUqYhYrx5NovPQYoO9bzUfiNz0lU1TdEl3BAArxhv7HQIH3QLbczFY63MM'
        b'JQYxl2Zuow11TdDLm/0blcTxoT2h34U4LnQ6dc7vculx7vK8yOkPieunHgqOTvr5zU6NC5rnNy5pj+oXBfY7BhKySK9utMIBJ6Fe3uiKs/JsVtNlWnJHdqNFc1Q7p2VS'
        b'+/zOcR2L+r2kPU49hWfd+j2n9DtOGXGXbtagk7Ne0ZzbPr9lSb/r+E6nftfQTnm/S0S/UwQbWdgc3VjS7tS4rN9pHKY4k0cH44CDk37WjnVDHmS2TGhXd87qWDfgEdEo'
        b'+MRIGfAI1QvuWuJa63Obo5rlA47iQUfXFo/2qFZvXF8cNr8cwnUyJmPD0c3qAcdx5mHShG74juhWn37H8ezdo8PGO9YMOPrfFYx+vHmqqOZCnGqs55nfPUZJYjwJBrg7'
        b'2TwBbllnIYtE2hOuOgcNilxarNr9W21xv+mJm4pQZIwdcA66ZSvanVWX1ZxwzdaXhDPqMnZm3RoXqstoDuy39RsUeo0AF5bDvCqlXP3zeOKB3brAnJvViwimGM2/LxiB'
        b'BdZav1vCx1rrHfCEqitF+eazOc/w+/UOYLSgKMmuDZCHgYMVUFhQn0QOtadY5ZE9GjwFZxsw7sHI41MK14wioBSeGcWCUvhmFEslD+sR3GKOQrDN0gg88qx0YD2TZ50D'
        b'rIpx+1kkKBRqpUZTJDArrqURfKwFRk3buOkCIyHiZM6hygl1PC+2pHgIF6jO2oSHLCgeEpjhIQsz5CPYZGHAQw9RH+0YPtpfgJ9JV+uSHWKIrdEfoAsSf9SKGlhnuq9C'
        b'ejmaXTj0x/xvW9+POux/uGN/R1Nvcs92f+orrH5h+47o6Eq1KEZ7znXJ8cjiqKL5781/Y/GHb76r5+Ryi45HvVF5I7pw0mvbo+pdcion7Jwz+Bv+Wv+prhtedjyZOvnW'
        b'cx8eLrvyafzB09vlE4TX7NIP/2NC+t2y1RO6431vvplpL3boWLqzTfjun7Zd2iPBugkXLFzu99KdKRJrutiT4G5nLvOrSzlVWAvvYGeFE/AgumTuvDZ7EQPPwjYZvTUH'
        b'dXmHySSwwdvoWseJgc8H0hlDazuR7lZg80WXFsFn8VwD62VUIcphwsNk4eiYkLVZHeNEoovz7xGP+/iny2A93I12p4XD3XC3BbCB5ye5clAtOpNHMy5MnwXrs/BchhrC'
        b'1qZJ4EkecLDiVs6ZRWPXr8OqEYnGN/RIYRcPCCw5HvDZadSo4DMT4dgIrDXJUtjdHM7o+GJ0gIu2zIXb2Znu2MIsnEQmSc0IZ4BNPAfVc9AFdMT3P9aeNm82154s8vPL'
        b'levy86sdDFwvMxDonEU0e6I7rbcAXj56iyGhx6DI60BmY2b7xGui0CGhV0vloJdv2+SWye2Ln1ve49yTey7vYnZfYPyAV4I+yZg29kRcR9zRaddEkUNCPyORXN50825e'
        b'1F7U7xbdE3PRYsAtXs8bFAfreXvtBn388Y/1oL8E/9gP+gXhH9tBNy+9jZmosxnmFpVp1KGkHrwiVWXVsOXqCk0lWZ8YFmgq1Upl5bCttvyBOfjRZg7SNgX0Y2bqKCHS'
        b'8OF2+YEkn4q/fsSyUGvBMPHM14B8P4E0pJL3kEAKum0mjVSzGOOY9qZjugasAKM/WE6VSJjMLmbYMt/gSyVhhnkaZVkx8QYBYrZrLaeVyVcVKuQzqh2NdTBS7BiD+N8M'
        b'OpPOZJzMoK36q0qyDZcEP52fTzpAwqhXk/Z5UAr1GtKIowpgj1N8bSiA6IznSc9fX4AStgBW+ca+f+xCOJgVIvfM8pPL/+NWsMhn2e6xi+Bo1hGxZ6adnDa6CCYDawFg'
        b'd52wSw14Cvvv69yj5pjRCw3cTJXbP49yNOMwof0Vh9b3Y6n7ZIfJOEuXplbV8N6b7d2xQ8KwdqIj6Bm4B22F26hQNAlEn0wJx2wUEpljspeqNGYLOdUuxpYbQaZCighy'
        b'AqxLLYG7d3NSW2pL6oBbcJ9jsJmo4NP+GGv8Uzut2Q6MjaSfxn6aM/PAeP+N3PLJEBBltEaBP+iwkXLxTE0+WIJZYrEiX6XMzx+2zs9nN4fisG1+/hqtvIyNoXIIizZ1'
        b'xWqlurKKyju1inwRZlSvNJZ62I7sMZFj4KIsK8vPl/DwmGAJ5ltOHqz+xZsEHbE8Vxthz3ckPpvUchu4Yw3imSRmMHrid1wHO++744CbX7/flAHXON1cLP37vWMGhLG6'
        b'pCFMFU8dcJumSx5y8en3nTTgMlk355adyz0O1y7kay6wd6Uh2iF0uyJqQxdRpyY9RZIaLpPC/QJgvYJMrr1wxwj+szH8fh2Lu3qf0wOMqGAIJlwEerj43wH/Oxp+7civ'
        b'ilPMMVyP+O/mnDKAOooxgwjCxNDNuDvQEQM33jYrEy7kkZ3BBD8qBN0WpwwLLxRn8hWWmGplRrWgVGtMtTGjWlKqLabamVGtKNUeUx3MqNaU6oipTmZUG0p1xlShGdWW'
        b'UkWY6mJGtcO1scaCwXWbZZ79g9ZRYLzb7WbEwLTGthhXu5shYAean8c2oHRQeOIcDfb4PMcRbezQ7WV8lmI8zoe4jHMV3mYt5kTz8cHl8jUrlzOl+mGq2IwqHJk3/rfA'
        b'/5bFhMLr9jeWQRGMYTXHsJOT9JO9zqHYSjHO7Kkimn8Azj/QLH+XKi6WyyEYzxfRWfJ+sLW5Em+gspuuR8SQRT8VVoCGeWQAjjXeMosszJjUHhiE5Db8tc9y5IZsLK2t'
        b'sLzm4qIzpi2opOmAToAZzp5KcYsRmoKl1Qg9AIctzeS1xSZLgxR/iGq+RvfJv3ArjKgU+aSUqypV8jJVNdljXqoUyw1NoMIYSV5eRDapP3xL3Gq5Wr5KTJojTjxbhe9S'
        b'01tTZiVkiivUYrk4OrxSu7pMiTOhEcUV6lXiiuJRGZGPkr0/hNwsFc9KSZSQLEISEhOzFmTm5mcuyJg1OxtHJGSm5SdmJc2WyMbMJhc/pkxeWYmzWqcqKxMXKsVFFeVr'
        b'sXBUKsjeeVKMogo1FmarK8oVqvKSMXOhNZBrKytWyStVRfKysiqZOKGcJas0YrqCi/PD9RGvxW2mwPBmdHEMzUP4JI6Wi4SMJwEYmxer0Qql+pE3GyAce7/hArdRTlZ4'
        b'TNTEieKE9HnJCeJoyUO5jlkn9knikIrV5FABedkYDWh8KK6O4Yk4NHaJHycfI+hi8zJe/fr8WPzE5saGf0VeI6YQk+ZugjC2mdrxOBwKz6B2sqolhUfGy8jG+bRFSJdG'
        b'9/j7wed48DJqQkepqXi+djfwZoB75KTNyW2e64B2EqDGyIZIurw1D+lSkpyxihmB6nA4K4fNZkEyPJ2cmZGRksEAuAM9Z4VegrvLaYaLpgrI+oBj5EQPu4mVKqANw8T0'
        b'OTHEWzEsjezfSp+fzCqXWLWEL6h4aI8EdoGcBAt0IBH10Ez64tl188jiDTmuEw029ZOb2BX2yOJPy4sDpwNtOCY6FcIe86yRLj0V7cTFjHBLyk5GO9IFYC46LkBnYSfq'
        b'oQ60uejiBs0a4me9G6yfDneElKnekc9kNFZ4Fjk0Lnbjnunl2yIdn7V45l9RM5cc3BfyrXXjS8M2t90bS7tDCoOsS1r3tadMutfvuzWtOHLwzS1vNvy76kjbHwte3WER'
        b'+Tp467Mtvs/E32382JWjP9JVU31s56Ljihtu4Jucv2Pt+vr8v//ziO0LB/KrX/086F7OHssprs2Xzzb+xkU7R4Z2LGxwaI2S9Z6MLPv+pcySoyuOnK9d47P+g8bXzqmu'
        b'55yv+/Fb38lVwRs+PvyN5tXFl9de3xI69fvfXqn9tuWLrAvWLe5+2ud4Qws7UoefHk4rzsy8Il/4zvNXmcZ/8vmNPbeFQ97q7GL7P9u72A+J7m2/9+39tsLxzz5/reNm'
        b'n7v0Qsk3b6yR2n3p9gf/qp8E59Qp2Zd7Jc504w7qTYu3wS0rydCGw91FoWhHBAe4wFqeJToeyqY4DI9sRPWwA3WO8HfloBeq4mgKTVRomiwVPWuRIU2BDWh3Oj18wRO+'
        b'yCsP8aa2igXoqDvrXROC9rLeXYuT6fa/BRmwPQ3tSs5Au+AutBvp0Rn2dhe0jYsuJq6m3rbuPNhp2FyUucDM/wbukt6LIGU8jy7ZYibBOYQhcqoDm19EWngofLmEDA/i'
        b'HjsXnrWAu33gRWqlEBTBo2krYUtWODkHgrCRzXwO2uXFblrkJaIGWG+oS5oM8NFBBr2yCZ2nsXA/2pFG1AF8Wx46DbiolYG7gmEdG9swAb5GbqbjMcEJ3/wKh/GHDbQu'
        b'6JiHwGR9kdjAF4zml1UT7pG9Ql7ooJIYWBok9MwOtklpTrA2CoTBXj56Fu1FB9jMTqngfppbOkP2COCStDFQD8/DI2xRjsCjsBUnkGUIpKgZR7/EwNYMeJTe7Y92byLl'
        b'zCBuxtK1qIuczVHCjXOEbdS7JLVCgm+lQLcI6mQCYJ/InQNfsqM3V6PXosnNUtzOmeEStDeZB+xhJzdJYSVx+G8uYZCNISbLj7n9B+sfKowK8vOxbsoKWJmRQpWrHIZV'
        b'rpZbAfeA9tgBtxA9b8jN66ZnYPvyAc/YPlHskNCVrGY0q/fMuO0Z2Bc0a8AzsU+UOCT0bNG0T2qt6Vxz1S/yJomZOuA5rU80bdDVU88dEhLr/4LO2Pb0a8KoW25ezQmN'
        b'6w483fj0NbeQQb/AG36R/X6RPaIe+Vm3i4EX17wcPOA3q4V3KzCkxaqZ11w06OZ1oLqxuqlGzxt0877hFtzvFtzJ6yy65hZNHxU34Dm1TzQVl23Q06dN0iJpDWtMHHTx'
        b'OJDfmN+ee80ltFN7I2Lu1Yi5g55+beEt4Z28Ac9wfaLR7OTth3+sjFcGk9T4UD3vmmPAoLeYRhp+xIEkckgcPCjyGhL5tfMGREHk13JAJCG/ggFR8NdWfH9nkuyOLfAP'
        b'0vP22Zmppk6saqojX8Q9bEz97pet+Q/3OOndAjOTlpmVvw1QU8RD3e1HtFvivfbTZvDdBqzdzvwO4C/iQjDzSW1bRwUxoNdmxq+zbZWyti1+PgGdj7akGIpvtKQsfmDM'
        b'ac5tyzuYR5v4flCuCawSGIGBnRFHhKiVckV4RXlZlUSGH8dVVBT9J6Y4Xn6hquixS7t0RGmXHFzCljaQlBbj4p8t7H9SSj61Njx2MZfjFOqjJJ4WL+znEe5/XkpiRlOX'
        b'4/Bjl1A+oiGXHVzGllRmjqV/bWEjf6awKzijaXT9iMmUcLBUlbPGFDqOH7syCjIE7U2VaVl2wyfiqk+EWeP/HFj/X9SH2jU56heBQRo9dlVKRlcl5qoP61l7P+JxdIX/'
        b'dXVWPkl1VoyuTtRVnyi2OuG/rKz8pwODlYm04I9d5lVk8J4FxsEbmUvVdFxA8yURsYFRxWX0PLpHFvT/pRW6VMK5/9wopS6RKOQaseohyahRKlfRE/MKlayePupGcoqe'
        b'wTiRoyovwW0wW6uuEM+TV61SlldqxAm4zqN1yBDcMLh58I1rJ8qiZZGSn9cyx1qMzZUwdEuIJAk2h2WGLxZidMeLZ+BJdMJX9U3MPxgN2bXwW9thYkRnDeixn62NVkQV'
        b'7eBeemdBb4GLEoky5E+hFw96PD/Od8kEV69nPCYPAM+vrN31VyU8qjiUwa1FRggJD4RmhhshJNoNL98jVnqsp56cZ9APyMYUoiOY6wdZhVS/sMosQ/XpqSL1g1PfZOPv'
        b'kfKnoFfgC2kU3hfBZs5yJkKkeKTd3oKYzMlZIA5GfjQQKJwkC2dkQbHUhrjkT2+c3icMGQyU3AiM7Q+M7cm9sOTsktd571i+YfluZV9g7EBgrj5pbwYBexsbN/Y5Bv4q'
        b'i/6bgC7jjSzNanNb/jKbJ/Rm2MSOQwLXHsMfn3hJMnis/C/88UvwWKkdxZo5ykrWwqctq1StklcaZm2txmDQosdWVqrl5Rq52fGThVWjMiJ5xFELaVxBBk6Ds8I/8hKl'
        b'uuAXzC6jV44MztM/2lJbSoF3ZEHmgbk+QEscSyahnbAbHUVdJnvK41hTyuBZ1RbXUI5mJpGF3V+SvQIdTV3zd01cWtchTD5TrADPyMaL25zeyJJ/uFZeEPKpbMtXW8at'
        b'fnl8+yuZf1l/MT2IW2IDViTbbot6T8Jhd6p0obPwvA18Hp03aPRm6nxh4D1yBKIGPoM1ToN66QMvjdQwDeplcvDPbLwy8x/TKCvzjb1EwVm1h5FVR0WN2NVSQ4ZQnzBg'
        b'yGt8e+WAl1SfNOTm2RzbVNUevWfTTd+QPsmcAd+5fe5zqeJy3THAfAcAO3jqHjGCHuH6Txzef6Z01cYhRbYBrMFDyv0/Oo3jcafGYhbZ2o8szGPPktsJgCRnkpGZ/YZP'
        b'5FWfSLNZ/XHHjwzLQwl5CDl5Y8RuBtPEsAI8cBw6AKjjNFnXMDpP/9f3MnySzoyxBGCSDBVqVYmqXF6Ja6NSPAq2lCvXGWbAKFnUGIbWR1uXFawJlzaUcRsUfpBMnK1c'
        b'o1WpDe2owKGiSrFCWaiq1Ixp0SZyCZdAU7HKiOdVGKbIyzQVNAM2a7YripVqzaPt3doitkSJs1IwAFKt0ZL8MPoMIWBHrDaWCj8rpVJO4M/Pi7fR254sM7VEe/ZEz6MD'
        b'aZlop+Hoy8zw+cmy1AzYlEf2UNRFZCNd+vxkbrYEdqWIlxeq1ZtUy63ArBKHVfAoPKqlJ7ecDICXUb0a9ZgZg3EehgwAPIf2LcBz/j5mDTpvuQidRr3sqSV70POeqHeW'
        b'oy05/6GTrrqv187CMdPhCVSnsdcuTCbuRgu80DNIJ12IdGg3qodduclS8pSdKeloB4NF6zHJerg/ED2fywFoH7xgO88NdmulpGAveo+wUK+2h12o0ZjrvEXhCy3AvKcF'
        b'8BjS56ne2CbgaohVQ2/t1/p+HBHM/UebgjDIEa05EIkGJTtPefh3j38783npwvTrpzoq3YTCxOC+3PaWssW5UQmfFb7qnHlxaOj36YfTF8SfT54YOek++EYj//y3n74l'
        b'SpNv/5v0L3Oi9/GHpl2WFQtece8UlFuf+/3iqS39NwX3lkybmv5qk8e7f9p8N9Rj8lJQHig+8d4/JVasOa+nEL6Mpxlqr0vhA5tyT3cOap057V4QmbbgVtRtg87DnaGo'
        b'IYxaD41TgB/s5aEzcDfqoJtblqFTMx7sdsTzl54TXiOlZj24H55RpZnM9zxg64gap3FdFqH2e2LSjrvhlak2sB1dHD3HoG3oDPWZcEbd+QSQmeDYWXgItsJG+CL1IVsM'
        b'2+CFMNhlbX5eFGvQ3YI62Zo2w81wt8GySa2aGyZC/XJ4ij2Kqhm2y1irJjVpRkTi3Hcl/NKWts0PzV0P5Ag5aGrE7DAiis5dhw1zV4Et8YGeSYBdzZ6am76hfWELB3wX'
        b'9bkvMpnr9IlkC1xOT+AF6VnpNa+ZdEZLfL2oX5Iy4Jva5546KHTFOXj5tU1pmXLDK6LfK6KHd81rAk2XOeCb1eeeNSIzSWfANS8ZjY5/PabfNDsabH3kZ5+VuSMtO0ea'
        b'pPqjJ0rqRztiprw5aqYc0RZ1jNlGnSxbhvEm/rTeT+pNsl8wHjxvE/XrrGzFRrMVltWPPVl2EJXyJDCqlFHUJPFAuv+c9vsfKr8SWlTt41vYjo0s6tQxZX/igsSH11XH'
        b'KLSEO8xbpVYWDws0qpJypWLYCs9aWrUaa49FPLOi2hrrU42/9lkZ/QDoZG9pcjNhdHb0VDGOzr7Ylk79PDz1m1b7N/KtRkzsOMw3m+R5m/iGqf8h6oipv+Vnp3720HoW'
        b'zdNZ1FyhfrQPAGkCdg413mva1vzo5VzaYOxd9Bbc2IQmJ8YHmThRXk70drkhrnAFRgNjwgDiaYBn5pysyRMjo6iPAVn/VxCrC1bpH/l4Uz/FieeUyUvE60qVBg8GXGFS'
        b'5wcpjJV61OPLKyrHeIxaiStSrokTJzysJhUYqvMLOMK02dWEI6wz6ZSNLmfD10biCKQzTFoLkjEp2wAJmGhnuJsPm2AT6k1DvakgCB2zRwfDrbTTcTZJeAbvTZOFIz06'
        b'G5qK5yPzXEy5J6cuCEkNpwePYu0KHfexRZ25kF1l/ktKMtADx0KmoMD6vDoFaCdioghdfJSuFp6akZOcgraZaWv1OVbotRx4RTsN34rnsUZ0CtXTdHS1MYWAjzBX1EUQ'
        b'ifnyd7I0NV2WEh4qAKheYrvGXqglZ5FEu8ALuNjdGMQ8SEzqQ54fguc6rIhJJeGpfFCNTljBBmuFhEvxkTtO20YeDHwyuIA3g4GnnBPoQfPwOV/UEcbemkH8xFs4vtYb'
        b'1OgKdVbbhK6gl8NSM2ThpAXFPmEMEAZzUes89Lzq0vxTPA2xkP8+wqP1/RiMcmIeRjhz2le4Sk+6nK0vOesU2WIlj8YwZ2Ww1842eOifnIUfWC36YOtt64ntK4q3fV6m'
        b'iT3fHfKXc5VqrfpM8dbh3zIi+Ze3t3Z99unWkwVbTzl+dvv9T9+u/NcKAapvtm9f8bZ0+c3QyJsfbf/Ud3vmxHa7Hy5+s059rOe3GB397fbOv27uet33ozdsD/0NRMjD'
        b'mUXOGADRA+WOeqArGJ2szcCogFPIRKH90XQdOWyW2GYk6oG9+Sbgk4FaWGf8Zkg2A2MmKpYbERTGT87oIF3vLIYX8tJSMkIxUuUAS1jPQc3T4ZaZHMM6eNVsG3PMo0AX'
        b'WdgTip5hUYkebY/H2cKLsNf4OoUNaDtFXF6odiFZmqa7xgRl4WGccbBnMs1YaQnb6NayLHoKbsYyjhR3UgQX7bNHFykmS4YvWtN1WnjQ3Qj9yDot3LNcYvsfra0SsT96'
        b'YdWGzPoGmVItNIcCBiIFRMOABUSFdsQeNnnP5Jue4/uC5w14zu8TzSdHVUzbM6096UR6R/qNwElXAyfR6LQBz/Q+UbrZwutNs4VXfFfLVGoRuCqU0oi5A57JfaJksuRa'
        b'3F50TRg65BPaOXHAJ1o/h6WVXhNGDPoEtC1tWdq6TD9nUOjButG2pl8VhtAs4gc8E/pECWSZ01s86Bt4w1fW7ysb8I0c9A+9a8GTOH8NeP5CusRpDdy9D9Q01vSNsDg4'
        b'sGjqz+TrL+Trr+DXLGs+WM0eubBpwF33CBQYq7FPGBHXDxhxpdkxTBhZ3Ax7UsR1RCADL9hM+fWIS0J89g1lemwo8+5IQ74/mUzxVEOnVtNcbG65l/CId3EXJxM/b47E'
        b'Vf00uXcz+doC2D0fioqi/Hy6EKwmJxTQ1edhbqGq6JFL0MMWxiUtYk+ltqBhuxEmF4p6zfDyPXqXsbJO/5u9mU4PDT4zZtgOqFcz25gehAGaiDPDNnCXx7Fz/MoS2Lu0'
        b'xHTwO4q6Ars0fX4xfZ6xL8e8xx3y9Onink28x2Xsp9yKmTQYN+M7bqxd0NeAfPEx8Q4Ph+6WMUDkPeQYPCiaeo/PEU3XJd0VAKHXkOP4QVEcpgin6RIxxZAmgaRJZGgi'
        b'N78hx9BBURImuc1hdHMNqSJGpnIXDznGDIpmY5L7XEaXjEmuvkOOUYOiRExync3o5jzIaw7JKxnn9Y2lpV3QVyJatXZec9g1u/HfcKzswogPdvAdErorAj5BQ46RfdGJ'
        b'bFY+OKsMtjWEHQH4hm85LnZiww04dFdqrNZcUq0UhtbLQJpPSDmYxGYQ0KHpij1r2Td+yhu51+xSv+P42gXeA/iLZJfG3CHXd2cYSz2JlHpK3VzWLZzMw37w6BxNeiar'
        b'OU9C+xhgXc3B07Jm1BsEAB1wxCnceaRTuIKTx1Nw8/gqkCdQ8PIs8L+lgp9npRDkWSssiDv1ItDDJ47GBqdxhjocO3ZbmlybIzBGt9E5FnMVVmZOxsTl2s7g4G1rcjK2'
        b'p1Q7TLU3ozpQqgOmOppRydPslU6GXYIW1BvYQedUbKlweuCKbXqeM0ltKq1jt7PJgZvoDuR+p2K+QjjGnUL8bNG2B9ci8gKcYo7CZZtlnguuF0MdxF0VbttAnpvCHX+7'
        b'E9fvPA9DOk8c66nwwhQvhTf+9iYO3Xk+OgG+0xfH+eoADvnhkJ9CjGPE9NofX/srxuHrcYZ8AjAlQBGIKYEGShCmBBnC43F4vCEcjMPBhnAIDofQHCU4JKGhUBwKpaEw'
        b'HArTWeGQFIekOkscCsehcEUk3X9JNozKtlnlyap4WBOKGhYkrKK+3ydHwHAiQdkI1v2bfdMW1jDIy0NK1HKiWrB6QVGVybf4IQ/ekc7kapzBKmWlqkhMdmnI2UWVIla9'
        b'wQSiseA8WXtnWZW4opzVQcbSESScYUH+WnmZVjlslW8sxTB39oLszPvTSisrV8dFRKxbt06mLCqUKbXqitVy/BOhqZRXaiLIdfF6rJc9CIUr5KqyKtn6VWXk5L/E9HnD'
        b'3OQFc4a5KUnZw9zUeUuGuWnZi4a5C+YuntPFGeazD7Y0PneELdvkShvIEFs2nus4Gtux5zt2mavG9M40BbNyEpbAjjWcFdzRqY2sqrGv5BtpCk4NpxqrR+ZvYavj1zDG'
        b'642MglvDrAXqwBpGwVPw6fOYFRZg1EfBNZVCQKSM8aoaC5JqPjnOiORWjvNWWLBhspz94Ek1IN+k5uPy24BRH2P5cUrTpuEqS6sSidUn+WOp4g874ht48YEf/sM3PErB'
        b'pb3FqtdyNg9K+RkzONutcdTVPScrPDY6apI5qyuwVp5STLRdsWa1skhVrFIqpGPqxKpKokFjjGV0uadPNlpT2GGFlXS1qlD7CK06jkTHFSiUxXIMJEysXoDVdFVRKcld'
        b'xbYTHjCG5+BBMLpufyMcdd9FVU7X/x/UJjhIEzzMyIaZyL8REfy3n/DnPlcWGZkpsRh2fPixZOVaXra6VD5svZDUZLZaXaEe5mtWl6kq1Rzci8N87Wo8lNVchpwLx+JZ'
        b'spFSTTYzPoxLCBuIzSyC1OfOge1nk8vdxwSU7AWsh6UIT/mDfgE3/GL7/WL1yQTdr2+a3p5wVRjUufhG+PT+8OnXwmdSND7t4vp+E6p392qe3Wqt5w8KXZuDGqcNijya'
        b'c9oTurids8+kdaVd5A5Ip13M7pfGD4Qk9Acm9PvM6hfNapx9Cydb0Jipnz3kG9SubC3H0N1m0F9ywrfDd8A/Ss/bZ//rN0OyQJe22aMwrrEljBD3mxFuXEsPLjVbgzNn'
        b'bMpeVauV4gLMNkUYe5bJktjfggKZ+vivLbHBvYb7BCX+fkSJlx9kN4/e96L+hmMPrBFF4xiLlvkzRfs5WbmCNzrOxmQu5VLWHLaUa/Lp9pxhS+X61RXlyvJH7k19uIL/'
        b'R5jTk62gom1Fy4obvlH9vlEDvjE3fKf14z8fdrPq/SLqFahdVahUk+4x9It4dZm8iHgUySvFZUq5plIcLZGJF2iUVDwUalVlleGqctyPavxUBdbl8OiWK1ZocUKSYGQu'
        b'I5vONA3RA+IsTS/8A6YX/lkbTmBgRiyq/hf8kj75YixxvmA1UXFYUa5cX1QqLy9RitWUVCgna8YVrPsRTiUXr1ZXrFUR16LCKkIclRlxTlqtxMghEXeWGjfBLHn5SroO'
        b'qqmswAoYFbzljyVkDQLWWKR8WqQC0gtaKlRZEU5kvWn9E/cC2Qs1hiMIeXmpsrK04gGKkYo1KjxbGbIhtxF/MvMdVY+qoyGjOPL607gCA8Aaw6PkZw2uhRUV5I1q4mJz'
        b'y66WdoXioW4Yc/pZp1Rj4bIWoyN5IXGMe4SN9xfcvOwztXT3xP5IpAsLT06REutZ2iLirIJ2JeOgPdqXtSAkVZoSLgCrnC3Ra/Agepnu90EvoGO+sB71oPPzYTtsC0kN'
        b'J+/S2x2WCc+j57LD0fMcEDuXX1KO9lDtSL4W1WlkGalo3zqBM3CAB7hieEiGah3oHp/CRcSWK4EHHlhFQzLDQ9PCs435pvGxPmIJL02HLVq6K/ukBNVrQuZsNLzYlA93'
        b'M6gHbofPaul5Tfvd0MUc1CaADWjvAtSA9i0gttEsBr0IdbBjjpa+1OoQ3Ldcg69fwQXjAy5sZuBm2JRK31uKat1FmulTk1nDaRp8gQeccKlhdzncx959xA69pAkZj87S'
        b'89v5G8lrALtRd66qK6iZq7HEg+3YLK+N8z5I5UU5/uMjRXRTy0axDRxnvelZNxeHdzJ+3FIylBZfWnHp0y6NU8SWl3f4nZ2pqv4Dz3+NJuXqguvXr+f/e9K2Kf6idz75'
        b'cfFsS5sVqXPckw9cP/bcC1t9KiKOvPRpl/u3oS+HWu7XzHSwjV0Ym1Es/lN5TWtJUvBtLkr+IPuDz4bPR2aoj/cKc071HLv+03r3idzbkw4fSP/jxY/+7nYnPOB02JL7'
        b'sXcDpv3xp/HqhbqP31x17+6kdyOCv7jYUZ8qa3K/eeVjULbP68pf3i3WhF3fL8vqcnzewq67cMepPes+K+X/4fbh1J8mfyL9SLMs9Or2H4+1poyfePPVP9mfWD7+0tTK'
        b'Ftf+JTO3/PsHJu76jMBGb4kTu6Z7dEIm7ucj8ChmLVRvAXjhDDy9AJ6kp5agM2gzPBkWjnaguohk1MAFtnO4IWIB3Au3G94/JEJtsN4HvRiBEzGAF8HA3poJNG4yfHVj'
        b'GKxDW1KJYZjnz8DD5KUY7Kscj0L9U2kpoehARmiGBRDwOJYV6DgtkTU6W5EGt5CjvXCR8I1uDHwO6uGle8SlJ1c9/oFNGXWg0yNX01EdbGU34TzzlDQsrlwmCQ0xcKMD'
        b'OsetQs+hWvZdAM3LYSseS9tSHrxltx42sHGn4XGrsEJrw428TAb2oMPl1PkRHkeb0Tli+E2RymBdxIo5ZIziLMRiHnoJt9OVe+T1uHM3oLY0KTpgGrVZsCGCHbOh6DIf'
        b'bYU7E6n1exY8y01j3ylAxhgDbBQcXKPWOePpOZqwNikwLSucAZy18FglkxAMdWz1WuBueDwtEB0fca4ZHpVnqOm9Gh1ITFuCi5+WliFDddI02JBFixkKd/HhmaRw9lCY'
        b'7ej5p8kWrYWZ8LRUAHhJDLwC96IXJY7/dcMa+TKKwJGWbRdWxuaPnFaqvQ34YcxYauxOZvcS3cl1BE5uB2wabfq8J1xznDjo6nOgorGivehEaUfpgGvEDdfYftfYAdeJ'
        b'eu6go+sB20bbPp/onsRrjpOHXD2aA5pKMd3N88D6xvXtNgNuUsN+pPF9wTMHPOP7RPGD3oE3vMP7vcM7FT2TulZdzBvwTr7hndHvnTHgnaW3GgwIPjGlY8rRqXruNUfx'
        b'oLvXDffQfvdQDKA9fPWCQU9vvcWgt7gtvSW90/V33pH6JAzK29P6/SIxJvca1x7badExfcArCtPdvA9UNVa1uw+4hXYqrrpFD/oHNQuIt93s5pDGLONBN5Ovi6R37IBP'
        b'1B17IPJp594QR/eLo68Kowcl0frEa6LxZJvRnCFxYPuCE3kdeUef+p04Wp886ObXvu6qm2zQ2789pDkLZ90iuGMB/GPuWAJ3X735BiIbdSn4NbZ09tCbhzcHTcOd9PN9'
        b'+ZPRlk5OA9vgwDBO5ACcJ3kBgJq8MRPjUKI4jfCfNa2GUmc5vun1pHx67C8wHfxLjAuC/5oPbTHGdb8bC9clssDEsFmeVUMITMU4gWANE7o3wDuC9TQGBXg0jDAsMz+E'
        b'Dx9Cg2Ojv9GgJHc00pQTNDMCfBmxUAUBaWSNvYrAyNElkxeVsp5vq5SrKtRV1CWgWKtm8ZSGvrz+l4HZw/aFkXqQ2T6PSrm6BCvzxpQ/u6heblpVZxnSuKhuBMAEtio1'
        b'5ta6X+G2R1e5d+bZkeNNQ/TpxVL/STPZvdR7stjzXuM3ldQ8NbfUcGAr8xJYj7mlfXJ/YXOFcjp18VfPS9dYojo7Ow5g0C48I03AGIu8wtHNCXWkPZhVKBAky/doP9pF'
        b'lvCNyCiXeM8twvMBWY1/4I6HZ4BqX8e4aWi/6pPYXXzNn3CWJQ6faxunk3ehPnv4RZWNi4t4y/cvgwCvMumhzb6bj+ecm63rSHV7s3Dtm/7VKTc7Z89KOZf0/v993Fv0'
        b'WpNDu9720MC336W1v56rPjBvKvhNVPiWe4PXvV5Pev6T29s9+hbdWfRVsayo+UOUOfsPn9lENUXmRKUd1oU+dfLTz9M/942ZYlMyr0Kz6PQ7t3d3P5365rh/lCyDV697'
        b'fdFW6nKKe9z33ye3TB049fv7cy2+zQ6+lvBav0XMzc1tf9/6+c21Afff9xK9lHp30ez1zs9q6z9adfHmK3/7sa3o5ldygXdkdO6G9RL5vR84ZZZxS44USezZ+a4dtUeF'
        b'wVrYafa2RAxFzrBgpxa9ArvT4F5zfOmwkFvmhbbQSR2dh8/FpZlP6U/BIyNm9fnj6NYH+MzkIlSfCpvJ2djswdjj1lL4Eg13wdo006yM9rmOnJgxaKc5xMBTaIfpAO2p'
        b'8FnYZulOSwm7YENkGHvaaQXaTZaubeA5DjqF9j1NF8zjs9Fr5idoX0bt8DX44lqKu6YsGR9mBmta0S7YYzuNIhsf1IL2Ywz03FwjtjFHNvASar1H1uIixPAc0UuqrImP'
        b'etYIgMPByGgHkx9hCY9VTKbPc8lAjWHoZdhDF+n5QLCC4xs/iT2+tYWAMRt0GdaN9loE7BudYEtOZhhsdpJmYCXE8A5aB9jEVW8cJ7F6MvxhBcxOqzNsLTEoitX2hunJ'
        b'cE3BRagBXCicgHdg24yWGQNeYeTgfK/myraNLRuvCqWDXn76tEF37xvuYf3uYXi+d/U9UNZY1lSu5w65eZsiOovOlHaVnlpx1X3yoLdfW1pLWmtGZ8JV7/CegAshZ0Mu'
        b'Zp8LJ/ggpSWlNa0z8Ebo1H785z31YtFV74RBkfsNkaxfJLsmisQZtlm3UMOcG9np0j77qlBi2MrSObvfLYq6Ii7uW5p/Y2lpP/6TlA74qvrcVWTKn90ZeCa8K7w/cHK/'
        b'92T9bFIN7VXyLii/dm2/m9R4a1G/pGjAV9HnrmBvCunI6veOwendfdrsW+zbK09Ud1T3TB9wT9Dzh9x8mpXtiwfcZH2OMvPTyFlLJjViPsahoexJ5CNODc0kkOGhPgnh'
        b'GEAC2QyQ4cQw3nef0MVR/QfwqJPQ9oJHm8xqxtz7txao3RXMg8UFnEowOpVpYUBArIIKzpOlxziCm3mfE6S6zwuSRRdLeLRNh23zyyvyDeYszTBXXqihprnRZrhhx3yT'
        b'Yxu7/lPtZjQYPxSRSlo3DhDb3C0DdyXdCJzQj/+EEzCfHwtoV5xY0bHiaES/V1SfKOqWl/+xxE7eGesu66NZ/V4xfSJ2J+aI1R3T6w6I2r2PcwCwKyp1XOMCpnptDfOI'
        b'Jh+DStZ71PPH7g61N86JP5o+dk4PVnzKJZWm9R0FU8NpZRScse9ppatDj4jhHbZ4sKqEU1mOTrUR0+mGUX5mtasJ6K1SaXA3FJVSiFTNjRMHV1sEU9tc8DATLOGzPS5U'
        b'rVpdpipSVeazg0Gjqiing2TYKrdqNbuwwPIAu4ltmE/x5LAlu3SII0e6XItNe9mG7fNXq5UYainz6S3VLkYGGUGeT9iD1B0LROLho2xfeA3LP6yvbGrc1Ck649Plc9Vt'
        b'IuaTG14xV71iBgMlJzI6MnoCL4SfDR8IjG+Z/edxYcMRky6KXvO55PMu/7f2H9jf4TLhi8lJlwFLmDuA8VnC3PL2J8IRCxs3b73t6NUCk6ksHX/twzheQayxzM93saFD'
        b'x2AZ0qGH+dS8zcustmTrHRJczQuW4l7gBEvUZNeDhMNKM9O2RPGDcy5wC6npQafGRRiW8BTHYOf+fgsYiojuib0Qdzbu9NOv896xQ3Z9bpl9jpmjK2fa3UYGIanakwij'
        b'Yo5BYJDjFu9bEGEhDtKw5R8tFSzyyRGEuOD2poLT63yOyT5P3v+SdCK1I7WHd8HurF1fwIx+txl9jjPYco+5QXEOMIhQZlTxQA2jYIxjfiMzdh1qmJUcUx2GmWldHDU5'
        b'04Bla0MnLGGMnWCoiiA/v4wcNWJnqgm5LMRJvg5gK2KahGf3xAy4T8KTJ3vQRzueMCV9jpL/bY08DWIc9wpn2nR10S/VRTmyLviyeOy6xA64T35QlwXsQe8/U5cjwCSB'
        b'sRSr45gkcOwj+GxMSbcyBGBNRe3BPIIP8V1jUMldOY+aXBk2lj2ogTIs70H7PLTJ8YHUwm2lXDOircglebiGvO19pJTy8W/La8nrnHBmatfUfp+JX2FhM4sZ9A864dPh'
        b'0xN0QXZW1u8fj8WRSyJz65ca1LTIRgpFmIOtgK3xRAwWAf1MF5eP7GJyuZpj8EDEXezl1z6hZXqfW0ifY8j/ljWTDOuUZLDN+EXOLBk5ysglSaJWMgYnwv9ZOZ8ylfM+'
        b'Z8YvD6GSke1LLteRgqpMBR1T6hL/RDKl/PKEYtrpMkIyjTU9kOWkEdMDS9jAMbwBgnCpm9eo82XHbslyQwH/k7Yku0iopYtbQ+bEMZZ7jXmYxHBY1//H3JsAVHVd+8Pn'
        b'3InxAso8XybhMlxAwAFHEJDxooBjNIBcQBRB7yCOiRqNIA44gyNoVHCIOBNn926btE1TEFOQpo2+19chTfuIMUnra/u+vfY5d4KLcUjf93c495x99tlnnT2utddvrSU0'
        b'TsOUGTEbn1LWfHzqv54sMcUqldkSQ6/fgtksnvt2C1MzJ+CQ0Qe7p5x4UXBqfsv8bve4Tqe4wbVjaD7wvjd03Zg0Hee1Rr3qeb0IVnaOepOVnSa8A+RTgChDLc12rmlO'
        b'7f6+qfcHaTnbl2g5bkxHqVe+RGtpdAvMGQK4fhcGzmqLI9xQ82F8zdt9f90DjEC99vtqnqPEpOZpAkTYpkFoSc17+jaKwbFXs67bParTKeo5dQ/72BYFD4nWkDl/yMUM'
        b'oFwvXOsUoyLsc1BWazMIt14KrkBKVSbjRmypJSzy5KQ9lugqzdqDXm+HSgCDFbP17TNveaeL/P9g7HBWc+rN39eCHO0mLUgT9kBnevv5y4UJl2LeXAGvNXjsntvIdi/R'
        b'yBvp0IrmhtaLN6hdYaFWrStVVSwnFTPcUDGGtP0wr+QwAxkXH1mPT3SXT3S7uF3T7TOOCEbe/kcTmxJbxV3eUZ0uUY98ZLB2tLp2+SgaUh96BzSHcLJYt/foTpfR//cV'
        b'LXhuRQtecg57Joh+6Zq2JxxzZXW1mqtqZ0NVGxOPwiB6bl1ru33GG+vatctb0emi0Nd1CMnz/0RdS55b15KXXi9CXraqrah7efNZCq5PwUDfZnGgGyT43xvrREzqRGSo'
        b'k7AXqROtYZPJ8retYY1f9+J559H+Sd1miGitWdqf4/PSPMLn5ykT8KJfn4R0PFI1ZC2mrNRec35KYqzxPnHNwurKUjAHXlJcUaUqNd244QGghvq3LSzkyiVNMMzQBPqk'
        b'89DNwcxmyG6+ottnckPqZ6QnB58KbwlvLe32Bu+bvwuNalWdX9S2qCOkO3QyBJBKbRz70CewOYHbQe72GQNXY0mmJW1LyFAhkpPPxH6GdZ34nFATYID6fP7abojObMaS'
        b'6mXEobhuGnym3KxP0usOmGC9+Noga6P26KqmVY2LW+PPT2ib0O0+ttNp7GsRf078wxC/tFpjRjy9vgED6qBF+cUwoPJMSNQacgxBlAGF/r0iAMV95pv31+eQX7zAnHx6'
        b'fRt6oo+h7g+VcP3tYHWr9vzatrXd7hM6nSb8kKKZWvc9ZFZUac3IpNf3BLzxFyXTqzEeZv/db3c6jfi/o82GLlTFnPNck6ULUn5kJjb6gEvSprndQ2wUGPpFM8PbVZAJ'
        b'FPbX1HbG3qESGPesYSJWCVUijuldZUL42iG2Ty3utgvqJIZpWvgikyTtZWLln+D8WSBF7lZUlcuWVtdw2N/YGM5yQLd0aTV4438miFH0sbFkKvXS98o+62W64iptxapS'
        b'rn9yrqj6rEhJ5RVaTZ+wdMXSAUuZ0R0VN6Eaq59SYFb9fMqHUP3TuOrvdfZqnL5rHEXOZ3R7ZXa6ZD50A+/DJa1TW5Z0+cV3uyU0CHmOnJdxp7T7dntMGoozb6OctSuQ'
        b'Hz3AuFL9jCdNU1mthcArHvDNDuYIGnJdVlZaoq1YzgXuJXxQZbFGW8gBNvpEhTp1pToP6mAWHIxmmoZh3Wdt0CjZUYQEh6il6B2qalAXwIEuYPPhUAQH8C+qXgiHxXCg'
        b'DiLBEZ4a9pvVy+EAorb6LThsgMNGOIAIoQafJeqtcGiAA5hSqhvhcAAOhymdcGiBw3E4nIX6+XfH5Rxk+8nrJAH6v4o3/voYxJ5qlrP9lIikTv22jGdMbcYj/+BOe59e'
        b'X/9aZa9vADl4+9dm9zpPr03p9U4lZ4Ghnfb+/yF1aUptCWop7/RWfOD8QDrhW4GzdCTYM07sh7OvwhlX34dOYZwxpWsqW5vKW29G9LrEgvVmHDXehJTx/QLWbRr7VCz0'
        b'yAOTTlvGwb1X6vGdIETq94QhByjWEw7u/SJy+RVpSQf3PkJByQNpIFhTRsPNID4HueyfTHK4fSUQSeNpmJ1+OPvG3kbq+9SNleayTySsdNITiUAa/sRaII34xlokjXhi'
        b'z0rlxrSn1qw07KlEKI1/YsuSS/2Z4htSVfGQOeIbiUQ65hsn48FKOvHpcFaa+FTCHybCIRQO8u8kYml8P0MORrtOtEUyUYO34m1g18ky1h4C1BSiw7fCLYeEhF30vWJz'
        b'u07qLE1YKyqDMJDWfGge4UZGJTorHhCaR0JSrUxSrUwC9hhTrU0C9hhTbUwC9hhTbU0C9hhT7UwC9hhT7U0C9hhTpSYBe4ypDjTVjaS6m6RywXg8SKqnSaoTTfUiqd4m'
        b'qVzAHR+S6muSygXc8SOp/iapzjRVRlIDTFK54DmBJDXIJNWVpgaT1BCTVDeaOoKkhpqkutPUMJIqN0n1oKnhJDXCJNWTpkaS1CiTVC+aqiCp0Sap3jQ1hqTGmqT60NSR'
        b'JDXOJNWXpsaT1ASTVM5SdRS1VB0NlqqqMeQYoBoLVqorE202ysf1OYI7nAKjL7/H7ewAKKDekZ1JJj5q0IBsYAVBTTJKiqtgHVxQypv0aSsoEE9vOEEDzeiN/cB2gkO8'
        b'lZpj83hEoLmtBGxsmjgeLIJVt5jz6KOqLtHBNpahZLPSqtX6Aiu0nJaZe1QPsJuSlFOQwpdQNIQlotlFRhlv+FEsW0B14qQ4Dhdp6hgxknul/lt5i1ituhQqxKy8Yg01'
        b'wAXiqDnGclJScWWlTAeCVeVK4DPMPC6aPWzG7wEDA4ilrycTzm+vCNgptRWwVDAV1Vnr2KHYKq2BcbIMTjAwWUIVs0ZYaJBV6ZXI7EpsdiUxu7Iyu7I2u7Ixu9JbujOm'
        b'eFeSbmeWy97sSmp25WC4EpIrR7N7TmZXw8yuhptdOZtduZhduZpduZlduZtdeZhdeZpdeZldeZtd+Zhd+Zpd+Zld+RuuCCtbKDNcseQqwCxnoP5qjWDRVGbQH31dpzDz'
        b'S/m9BtFa8RrRoozBeVVifb/QSFQkD9XbiKoCh8gt0edWD1OBHJo5OM9Bdo3oIHtYuFakzTHQKVxj2HfROGhzDeVZkTeamUlrp5s+s0asD6TGMlvLRdCTbNYIFxnq1Pin'
        b'zhA6TSPIBGCMkAuIrFSfIGU/S+CmtkET4fOnOqphTetjC/sEhYXPQgY+vbAY7M+MJmzUZlcu77PPI3xbxRLeCFfCoX65QIjCwgpVn7hQV6pVg599zr1HnyMXsdrgkUx9'
        b'DGq4DQ4QvVpdDQfq9/0XDMXRmDnkI2ImB+8mJS7VqYkcX0peQZlxK4q40hb3SQqXaMrpqxeDLzhxYSn3Qz3DSfWPFdLos1aFJQsBmkwDghZrdRoiEahLAQpUXAmBLarK'
        b'qgnFtEIryipKqLsAIgRwy4DhdvESrfGD+lwKK6tLiivN3dxCBNiFAKjWEProNEyKob9cZNg+n8IBVU7kZzLF8nnF5HyJps+WEKnWasAJAhVn+qxIu0Cb9Dkk6VuGawkr'
        b'TakWbshtOaMDGPx9ksU1hASNiU9hC/Ibx7LDhMbN2EZWnYbZdR9Apj7c7ucgyB1hDepXbXNSU02nYmKX/0Rq8/Fmt1dhp0vhZ+6+gG1qLul2D28QAdJTtMfaEL+Fhmjp'
        b'DY2A+C3BhhgvMrMYL/owLsdtzIK96H/9g2gEYlmgaXRiPtEvkFpP84nmPyFyeD5Qn5X/gSAwexz0efSEBYfBb4DhOjIGfuU8bY/8guhrgkO4XPrcQfJT41vGn5y4M6sh'
        b'pTEE9sEnNU1qjXvgHd3rH9hc0LSqSdTr6XvUv8m/1eVTT0VveNT5yNORH4g6/Sc0ij6jFi0u1DFmZGdUQeesN7qi3uj2m9fpMe8zF+/GlObgVvGnLop+RyZ45FdOjEdg'
        b'c/CpyJbIdskD99GdTqM73UcbozK/hnNHNWKHNr32GNg39CbKw4VmvpuNERnGF1BzjKrFRheFkZz3Zm017wESzF9VhNepKFtJOBgTzuI1zMgpKqaFeYUvcRUypoFWRphH'
        b'rQFDhyXVWqOPShpB8RW9adJ9rdZXIdIDiDS61DQPVjOYRojv+OoOP9XnXoVEbwv1aBqwZgCNfGTGV6/H58WqGZJIPyDS6M9LbiFWzQ9IJ+2UN16FzgBzOn+dJOMifWp0'
        b'C3ivOdRPBxDHm0jxsUSe+xFUnOIKolhmkH6WksdAcqEhCyxEJ1HI8o1pZRWl8EJelCClkwxGAyoDK6GRhfOVGh5JTiu09FcfdSaconbDuagt4a9Rsx+/Ss2GQc1+YqjZ'
        b'+MGu5ocYU0nJs5KiySH1NQY/oRa/ymwbYU70eDPnv+DMvXSBuRvggcRPyUtNiU5JTS54PeJ/9CrEK4Sm7jrmHZjHfUQe7YwmDClv5ad3MzLA/EwhS6Gu6jlju8qa4pUa'
        b'3sWtrKq0vBg2dF/r0378Kp820nyYhuuHqd7ezuTreCZVFpY/c9bc14gkRmj8yauQmmA+PYfSZbq6ejEI95wLYCLzL11aDW64iAyh45wGv1aVfvgqdI4BOr/S6/CeORYY'
        b'3Bu9Oj0bOXo+ehV6xgE9fqzZirGETHvF5aUm423pwpUaMP2UTUvKUJJpsvI1KG1j1T99FUonWmhhI4WV1eXmBMrCsvJS017LL7j6Z69CZ5I5nZxBbZUqSlsdRX6MbKMs'
        b'LPX1CCQV+fNXITDFnEBfi363ZWE5r04dP0A+fhXqpppz3sYodQGcZTIRMavAew8/33De1qfNyJv2epPOL16F1kzzwTycrltUPOe9Fr3WKOl8FZJyzBs3fOAqBDsAYPAF'
        b'52HJublZGcqpBamzX3Xh5Guv61VInQakPjLU3n8PJNV8E0MhSyNT+NRSQnwVFcA0hk1iS1HiyUI0KyOtAGK9R8qmzpwSKZuWl5GTpMwtSIqUwQdnpc6RR1JrqzTo8Av5'
        b'MocqLSU3h8wsXHFpSTkZ2XO48/wZyaaXBXlJyvykKQUZuTQveQPduK6p0ICd/NLKYog4w3mWf52p/v6r1PdM85GluO/LGWs+CzRZ17mNIm5YFdPpqlhDynidaeCTVyF2'
        b'jvnQGjWwc3CbXwpZktF7W4YyLZc0c4pyKiz20Ldfq0//8lXIngdkBxrIdi+gzCq3PUf6lAo6c/UrTgv8nP+rV6GrcMAyz8csoM4QOapKjeoW0y2L1+ml3a9C6QLzWcGX'
        b'q0H9qgQ+MmSgULLAhBiwLmtYA9DeAn2a45ZxLCtYQFQMAQ4cwtpuBauxH+oZ6iJOsIa1jHshqRZsQ/Ub6muYQtOctoNzqr0tp1v+5kLx8+8vkg5OIzkdBqfqlQHsc4f9'
        b's3F5nKcNULwZJB1OWjOqAC1Lcwq5tfoetP//wGcOCF5N99nBQ7j6n+QgF5pEuKa7wFB/BnMGu/JSrX4bf5X3wA5ncrOUPKaB7em/rWPA8mvtrrWw2zmmacx97wmtLuc9'
        b'2zzbU66lX0jvDJtw3zvzrsuHnvc8G1IeBke0prQHX5NfkHcU3Jn3wbzu4ExDVElSRGzCNd8Lvo2io9Im6QMPRa+Lx/6cnTk9LnFdLnHtKT3xaV3xaQ9cpg4IQmnWp+EP'
        b'7dPQhfYzK1mKPC/grMsGDy0A2gweWnqDo2pYAGikJbBaeQ6aLY8ZenirnSwjc/V6LVOkbbkp6o2PkNtLUvpEoCmwYJFqzesQCi19BHdHDW3F20E6u/c4B4PzArA3juzy'
        b'juymEO3P3L0bk3evaHB8zt5x5vM+0e1lQv/ybUJVWfrvE9NuZdnktrK0inyfBa0EvVEDnycb4vN6vEd2eY/sdBnZ6+5Bv00pD7KEEqOKD4rr6nMYoLyiQ4WOLOOg+gfD'
        b'j6c+qbnuSsKrrqx4bludCpkkvNpKzGmtRFRpJQKdFQ3C0GdvprCS8PoqEdU9OQzQTNmZKqYkvEbL2qjQ4pRJDuYKK7W3gO/rahmcBQkoXn1INJd5cDH1VRgkA7EZXaAN'
        b'Al+xFMllI3X6zk0h9flKxTJ+I6hv/LynYoFfAVurNLreHw9O9Sc+3z2/SR7eN/0k8E2fxHnnp0n9ApFr9FOxxD2GpDlwPvR7XTLBgX42W5tDsvFJQIJvAZcEHvvl/QLW'
        b'dexTsdAtsTbtK2v9CybDC5KN7v8JFROAikmUCvpgr0sIuPoPpZ7+eZAZ0OWaxIHMBj/Gp4yClDGmKXGQkkBTfIJprAFwvu8ztjbb+LIweFk4fRn/FNDokszFI6AV3C8Q'
        b'uk5nn4rFfnlQx/aMd9BDJzJljiEZvRNrs4yFZUNhSi5IAQ+GiwIwXDQFw1n4GL4BgVC/hFrlUy6QASv1eSIRSmVf2wqlnhyeDKL0TcZ75tktly61xxvQTXkm3hqhzFaA'
        b'nxy8Q8iELxSj9hDcMSgcLfz5GkL3AsTWiC3byMwVCphSwJUZZsK5YpoiNEmR0BSRSYqVSkyeta4VlLEqyUbruTYqK3JtC37oywQqa5JiR+/ZkDN7QJrNla60I9OQfZ/z'
        b'gH6dXaExDyUm0M+AE7kZkDXjNQTkyjBfAma30DDnlQNXYpjaV/KbJCK6mdNnU6jS8YhTG7D+KK6s0K7sCxyoIgZqCk1RRhq9XWK4gEJP9YVY68vQWyjKTJxd+1go1eD5'
        b'eh1MoP7cBMprQQPkVCfK/4wIM8asfXX1zD+ew9tapM8QFRb4WzA6fG3F5hjBK5KwGUioeS0SeA5/7KuSUDs0CQYuREFJeFEjBr3gJlD7w5qQaJkyWC+G7D+Uv9giNBiY'
        b'Ah+RwpnJdLvHdDrF/FAGALyESWkcwgSALmqDmFaeUsopbANCATClt1Po8VZ0eSu63aM7naJ/GE5yiIriuMkGaEJfgb4JTf39GAxm/sVYNnnTmMLkWCPAyLLfCMsNT6M+'
        b'hJEnLMtrFmQu+oQjNemyIHtRr0J2WiMAzgS+R56wH/zEIsfBaUZDWRbmSOq4Kcp042IJ+CFfYHQ3HzqgjkPNs6uqSzk/2px3IBpNRO/wkTJHRFqazfITKOXP1OPgbDwc'
        b'qGkE9DLCyS1dWlql0rsFsjN5BZd1SOs+YbFKNYhbpR2B3NgNfRCiOdE+GNAc0fr2A/dJn3kFdQbnd3sVdLoU9Dr79TgHdTkHNWtPrWxZed85ptd7RI93RJd3BGf2c997'
        b'fK833F3bQs7jqS1FQbfXjE6XGb1OLj1OQV1OQT1O4V1O4a3jPnUa/ZwhCABB4xAcaG9j6o9j0GALhMHmaekjKSN/CD5TyhiH2u6VnU6ywaQYnIwCgsl86kphdrAlgnKm'
        b'RDDfg/MBZdGWxkJf3inY6iUiz601McEuEbA0pcZgbi7U6JaoR0BLmnij6GO1ZkbZYm21trjS8ofSW0fhQyEQPUx+XhdSur3HXkhpXdaYdDS9Kf2o8qCyPaXLe2y3e2Kn'
        b'U+Lf73uPpavzFl+FtVLuMFAQMdqW0K5p7JUGnp1j4dMFfAOocwRUpB/AvUP7Gnj3UdBQlnictUA5gCIJ//5EIpLKCQvp4tPlE9ftHF+b8tDdv0s2rtt9fG26yekTESuN'
        b'BcuCGDBm8PlGYiUdA8YHAV+Ty3EcTwiODl3xprfsvFEHsIXmLCG+hOsiFSyTgs9ZZSummPGFerzq1/8B21Fepnwh+Sugf4WHxHOFEGJGJVFZqaxVNipblZ3KXiUlZw4q'
        b'R5WTatghh7miWkGtmPB9wwm3JyY8oLjWGqI71Q6v9SyzgjhNlIO0opGZ9BykNU1x3cio3M66m9kgWPH4f3czGwQrHv/vbmaDYMXj/93NbBCsePy/u5kNghWP/3c3s0Gw'
        b'4vH/xlRHjv4yoSqYUO5E8ygqyKgtddLvIbzHbmfnOpF8w/nITsPI97M0rtNwegZRnZxtuHhaQurFV2KIgiutdSC140Trx7nWpda11q3WvdajzFUVttEGbBJmMe1W5L/b'
        b'WbkheE8MvIvUplAVYRKXy9WQ1/pspGleGhnKmM9tZThZ0mP77KFf6pHufey0PjZXLu4TTE3uE2Sk9glS88lvQZ9gSnqfMHmqsk+YkpXVJ5yaPK1PmJFPztLzyGFKelqf'
        b'UJlLzqZlkyx5ueSQnwo35maprYDVFk7NmCZ36BMkT+0TpGSp82B6F2SQstPz+gTZGX0CZW6fYFp2nyCP/OanqmfSDFPmkgwzCDEZg0xbKaCdc5DBBRbez1C3yAwRMUTU'
        b'KbLQzCmyyMbM5bFpSGGWeUv4loh3ijwg1dQpsnKQBEWnTYPrXJFSBxs0rvPxHRDGtLguV4G35UCQWX1oWXQEX4ieTsO6KjKoT9DsyIyc6elkQGaCS1XUJmIm4g2O6DK6'
        b'jY9UXI/QiDQJpMwVf9x58GcjIWb87pY9LbU3Nu5kbfM8Zk15mLM1JDumK3KmxJ492flTUb7nx3ebWKYh0Fp2d45cSB2V4ma0Dh+yQ22R6LAiXe+mdBi+LkTncvEF6sZd'
        b'OYJMCvW5eAtQsQdfBH/sBwUrcK0tDa5ejI5WoHq0A+/IikI70A4rxs5NgDvQDbzZFbURacjSBgbUywBUq4tpX9NDWmGIaWDGooE/fRkX98bILucRdD3O7faa1ukyzRTO'
        b'qndXw62NVkbcrRrCB1ly2UlNJfnwmN9HzEWYkcHFD4QiL/ZlWf+XjYm5VxLCnLCLEZaYcmsO+s4CQRj3WulDYW8WbRZvlmy2In3XlvRdEZkIxLVWZHLgpgMJDW3nVOZA'
        b'+zOZHOvsDP3ZhvZna5P+bGPSc63fsuH784BU0+At5v3ZEEXG0J/9lTroe27OuD5LH4SQ9N2oKAUESIbowsPxhjDSr9JnTKtBG9NRq5DB25fa4YaR1TpwBJiFmucYnySd'
        b'PDdqJu/SORNvI4vRjqxZYWgjvobrZlmTESNi0AfovJ1U50g9SzeFS5hDTkSmkxVVflqTxdCgxT7Z6JQGncdnjb6lvTQ0O5ptzdTGBUJT2zs65zM0pkgWql0I4QkMgZEV'
        b'uDXOzMm0FTMn32ol3mrDxQA5gdejd7KWo2sZOVmReJucZeyUAnwy3JrGAElRossR6eCNGu+Oi4mRx6KNRVlMILoiRLeV6D0aeETuuSBCCU6Ft+XMMPFiHaaICsO10eEQ'
        b'Abp6zDi5NRlx7zrRb5KV4bNZuD4jO1rCoB05EneBQ4aW9m8ddGcbfEsSAdUcJWHGp0jQdcEoH7yeBgzBG/F6fIHe9J46Y5oVY71MYDsMNelGw7ccy/XOH/T26WF4RyR6'
        b'H2/GddPCDHRaQeSS3bazFqK9OhgzSm/bfEJA2Fh0gwnDm4Op2WIqvo5PaPBJVLscXxQxLGpi8A6YXHRJQMttvHU+qettkQq8HWK+LB3lTPIVhJGmro+MzJmRjrfn6mN1'
        b'63sFy+D3hPaEJ2lFH9AaxrvQ9UlZ9CY6HBUhx1uyyWc7TxXiw/g6ukgDUKPN+GpURCY6pyefYeyyBGgfvj1MFwllrCtH6/MhxAuZcdsKDN+Oj6ELMNkSAhgm18lqaTpu'
        b'o+7K0daZc/FRfBLvBluRVUxOMmrWyaCkhhkk/RK+ULMc7dHiy6iuBl/UShiptwA1oY5sGvwbXyV9eLuG3CC9O3JmWGYU6ThkPqdvQg0xecZqJp+CduMOWyZmOY3dje7g'
        b'm/hKBNQQqbP6aLwjPyyMzNC10Uq+urguitbNCERtNoxVkQ4sdaai+ll2+Cq+rMHXlqFtNWr7FHR1Gb7KMO5xQkJM+0odmAWhw/ZJZOzirTlop2+UglS6mBmO9gpJ6+/K'
        b'oWOmdKGI2ZNHhv3kosg/rwrjhpgTetcHn7PTLCNCFd7BoC34A1xXseKt44wGtOJZBSf2FkyoRjFOV5wFsf5KVLPuamv+DZnui9/+y8kta8m2BwGyBzOL/7T8yxlWP4p+'
        b'lPtt8oWMLxpsHTOOrK35798c1hT+4+Bs0RePJleU7/zngR63PT77mm/g70LFU/t+NHvcsVs+fyk9cbP3H27j54yaEBL3XcPxRX+1DfySHTb38YGW30tifhx46OGE8P71'
        b'P01bn3wkb7bk2/UH8hL//o9hjWG/qLJeeXznVJvTvx87NzwgI/L3biFo/uH2xNHXGv/42d88h31w/86x2F/87sN15V/XV7wpmu6a8OObF+/uX19x/Itr397b0dYa+vfo'
        b'igfZFxLufj7t3vr/7P514p9O/2ymw5nzkcf8Zp5YMldVld9f7ZYz32rc1eM3UOavW9ce2vLbvjNV9du/bJp44Vxg9R+vah8EXL9wJbiLaXo29ovuw3/8519EHdPdP/vx'
        b'5DnNRy6v9f/s7C3r7+Y5W/9u009PXA+K/sWlY1UbRn/z6W8Xp6qWZg8TTw2WPD4/Nf8v63ek17j1f6LUuX93IdHzwaf7No1tPvFX9l/i3Ye2fvLLvO+syg+NliacDrw/'
        b'Yd3IYy2/Gp8Sf79cEdjucc6rPDv26My/7WqO2HRkePxM6z/MEi96cm/rxkvl6bkfb/ns7Yr3qrasCvrllcS1oV/+3eovvlttmc/lQdQt+7joSuAQ0hPizRkE0vdvUt/z'
        b'FTXJ0JXI1LE9WhmVDl7bzwvwCc+3abxx1FKhNgQyL/I3OkJH19A7lAuZWIVPERZi85oaB6mtGl/R4KtaqYRxWSbMR6fxEeo1Hu9He2yz8HlvLmIMm4Q78BXOkfr7+KI3'
        b'rs8mcgzeg44LGSG+zaKDpGu+TxkU1I7Wh5LBvhl1RBJWS45rKYXvC/BxfCWFsjhW+MQqVO+4HF9diq/oyKvt3B1kgoWL8VHq6d0Kn8a3Izi/+mhrFHWtP28451j/XBHa'
        b'Rvi1yHC5gsx3W8i6UMcwHjLRm1nFfU4+NiuzrBIVORJGsJIdP7qYviwLbZeTIb2FzEBb8SZ0QMiIxrLownL8Dhdy/gje65iF300jsxt57k022lXyFGYuhRc6rlluv0yH'
        b'rzmiLWiro7U0B1+2xe2Oy8kwx1drlhHCc0QS9MFoCfWWP4NwYW0RUXhbdiyZStfNlMxh8dkcfICrz8Y4MinWD0tJR+cIi7CWTSvDd2h8HbyHWUZaYyO6mEtq7Wx6DiKL'
        b'sSIzR8h4oSuimqJhXK1eJeSg+vmoLZfMTjvIEpVNOL/JAryPFNvAMZe7Q8j0Vw83t+aQKQY1kFWWTDNu2SIp/iCV0oh3oiukZchcSDqYmCn2kxQJAifg3VzPOY4bUCOq'
        b'XwX9ipsmxYxdrgDvRTcTaNgCdLtgIryB9Lxc4BnIaxaQtaaO1Jw/PiHCl2LxZVoUPkM4iW18Vq6TOqBWLb4gTImezlFyFh0ir6uPhgpjGXR6oSRD4M7GcA79b6NtLKqf'
        b'uIC+Qpmdi7bhHSSXFz4kWpacwMUt2jMSX0D1ucblyyF/rkSYg4+VcNENNqEG8rce7Rqeq4giDE+WkHTDLQJ8KjSbC+Gw3x0dJgVkRuJDYzII+8JYjxEswFfe5iI0fBCH'
        b'N9K7InyE3EW1udx7MkivDA8T4/Vjl9D2Q7XowjCSURmJ6qLpguGB1keTevfH18RiW1xP2w+3Ll9KMhFC2hYYIkIMR+8LSZufcXw6ig4svzAYFVRccVqtF1hQHdoRbb5r'
        b'EEGWrm1Btugoro14CiHeSEUfyTA8a/JkG95KniY/tdlyCZPNWKGLeJ3fU9gZd0Pv4f10rdtBZB/ycek55Cu3R2eRT9iOjsdwGqup6IIV2jHcn7ZqXmI1aTBS34jmX7iG'
        b'PCFh3MgMcMcq7N/uT0NvmjfQnwZV6bgOkCA4XQ6VZy4LuCimlb5gIxbaOvqBexyVaPgwpY/c/cAJ5AP3MLp3mNbtNbXTZepjd38a8jS6yz+6xz+uyz+ufeq17AvZd4ff'
        b'DeiMT7lb2u2f/eKhUB+7+/b6h7YmdPnH3PdTtquuLbmw5G5G1yjlfb+SzryShqngW3h+0/weX0WXr6K15vyatjUdyR3TO6Mn3XXv9s1oSHvk6XvUt8m3xzO8yzO8dVS3'
        b'58gGyUN3X/qmyXdHden9x/T6h4BLqtbQ9pHd/qMa7HlHxLvXNIh6nd0blzeXN73d5az4jVfw/fxZ9+cUdoYUdXsVd7oUP3L27HEO7nIObp7xwDmCfGzWxSxaema3V1an'
        b'S9Yjn0DwW9e8utsnrsHmobNPs/spnxaf1gWtyzoDYjs8uwKSSaF9IRGtBefntM1pX/kgKqlfyI6YAq7ZvVPANbsrOZJ1xr+ZCJWK9pprqy+upm9Iubu8KySn20vZ6aJ8'
        b'7OzXPO7BqOyuoGz+28Z1hSi7vXI7XXIfOQc0z+tyjiWFhEVC/Ijja3pCR3eFju4JndAVOqE7dFJDyqcuwY9CIxpSHpBf/xBq0hgY1urdFZhAzh0N5pHcHb2hIm+Gyfl3'
        b'PjiPZgkKPZXYknhqYsvEnqDRXUGju4PGQmZZryyUZuaL4E0fR4RyxpjB0VyJJvFqeZUhNdWEt9s/DBzRrOsJndQVOul+aPHdqR9m38vuSXmjK+WNznlF3SnF3YELGkR7'
        b'HU1E62G8JyK9SbEIdv7V4ERIHQe7M3YlxVqDdbBEU7KwdEnpi4bNMBllMJyK+D+Gsfa9g+wayOng2ex/ySj7bjER1HPZ7xg4fkWPLyG1a4ARfk8Sz1y2myR8DYwjGDfT'
        b'ShhKt2j+JYbAuWaY0VfX7R59jlbT8pufmaNVwwC0aHCawX2KjA/XIAtTlxaroqqrKlfKXzuucJ9dIW+sUVihejmS/2mOBo6678v5z30WackEpEJj/B7TD3gdfPu956jQ'
        b'LdMM25Um9kh+BdTwA8w+DJZgr0sbp5oFM3udtrqs7OXoE4rMukE0tQfQaaNIQTLwOWA0VgGaqRXxD0Kw2vWle6wESDUCgsMpILiijEcALwH4N2nz0irwmKJ6fSo5KHif'
        b'faHJTPdyBNsAwQ56dTNnDQKw5XKIK2ewPvsh6FQHvHTHtAfijLDv0KFDdZuTaPp2g9K8iOFwRLxXKiHdsgStpiEO4VqWblkyJluWrMnmJPMWy29ZDkg1bFmWf/8WvERp'
        b'2Qfmm0AdSyNjgwckfSxsgzrgtWNhb5QLHoNzRIuRldNMIzKb44Y1Ms3Cal2lCpTrZK6tKKsAK9/yYkAbWyxLyztfkk2pLC0GkwxZCnUtAh2KD9lMjbdgmawg45UzNKiw'
        b'HPJZU0oDOBYVFah1pWT5reBGevji6iptNVkAShaHyyorFqiLSeFgtKIPDm2xMDC80A6a28hjengmF1SRM4ZZaWJjYrE0zkzGQGBacaWGUDg4nCH1dmTaKQyDxtAphMqK'
        b'8VYNYg0IcKvK2w/+bMzhlt0B9ayzKG5pGcNkvzHuU8F/fdYnZznRamcUumAqcVB5A11Dm6jMUeVNBpmTfpDxcANRWXmpdlWw2SjTlFQW0iok4w1qRDNRAbmodADPg7aj'
        b'Usb4yMA/RaeLqVKDR5eZs1FUn1Kkh4mrwa3qi73RScSrNP6+jnk6X8ayw19WpdEgkTHNdhFCyx6iy+jI52OTiqnSguVVcODDWfSDxSUdpLKwqIKbAG14eSI6MFDMBNVD'
        b'XXZ4ZiQ6XcBtikNCbjZsyCcvQGdQnd1YtA4frYh5OkpMY7Ud+Xg3p3X7IP3m7ljSYVw0+2Nwr3zrGc+AsyPSRryrbFZ43Nm9o1Z+xObk6V3rL4mZs8tsVlz/WC58CpoA'
        b'QelqvIlGM7Qo75oKuwWVT2XkCetl6KoxPjS3FZcapY8O7T6dZpo6AR+rgiDOA/oo7Z/4quJF9HGky2peqMtq+C4bxnXZr9QyxsO3eUZPyIT7IRM+8wvvjMjs9svq9Mh6'
        b'OCK8NeH44oaUvblm+jnalaXPEwt4/ZzRlakavVjnJrR56Ts3xNVbRjq358uE1ANEvlxAlSz4djW6mJWF6ubA5qPIkUWn8KFyuh+O389DrVkRaONkJdyKY9GltzIqit6+'
        b'JKa62WO/2XDwZ+MPr9/d8o58W+ymC5uOu330RdFfizJKlMWCJx6LPRZ55Df+IUYc96u5S0+yTI/M5v7pP3G18z3wb1PnrobvX+VmuV5oK/lxrdQrsn46V2Y9LOJbF+Gw'
        b'kf3WTEBIq6rL6LBV//YhW8T87WoM7THEex31LUDe++0bpAVsXqYFAH5seckuYjjdPg14zJQJ/g2L9gvo9MnaYbf3r0INaF2W3C05+LP4w+vrWna30OngbNnGznv2hzyZ'
        b'JW+JVqb4fT6cLCGwqSYPhW1I/cbY6soX2VQ7PF0uMGkAAR2sJqDKgdpqiqakbe7Oj8zJAYyHtwVApb6xLawpxsY2UY4P/boAk5Xkm7dfciV5TlP/27mzQZwjM6ihRcqC'
        b'CveOW2INjPj/2Sg9+CELfMKunXFCxvaYwHPiOD3odMDiz4FOB+5ScGhT2j42XPv0p5H28XnJVf45ZQebLuupAS/ZGDcF/781xsaBjTE4CDUZdYH3RQKKCpn5ZDzl2ADy'
        b'kuh58er1Ro+YyW4RJ3sXeUg/9f74bpMD81mhOOCtUWTRhbrUBOhQGyy6kbBpLprMoiuFqOUprOdotxXh4yzsWA8elug4eocfmuhqBLf3v0+C10dQJVeUhLHGN/CFBQK0'
        b'Ex1CFy30CorZHrR3RcHatFfIuF7xNBt6hR6w3eMzqstnVLfPGBOn/i/eWZ7zylDTzpL1Sp3FFM7io28x8Cq419UinAVQbQ7US7Ee1yapdaaoNwO6rdaz1qvWqtabSIxM'
        b'rU+tb61fmY8B6iL9waAug0b/YKjLeKUOanWSA27LkuP1PBYDgBj4AL7IQTFAGVEVG22nxlfwFUdQu+OLWtfpEsYJvSfA1xeN00EfC1n7BiABliycmU56Si46OxAQYI4G'
        b'wO+usENX8FnUJJfogCZ8NDxMg6/OouqqBgZtTY3mmJDzynx8SYevoIsSyEXklCnD6B10KyUOwABXwEkrvgK6WLSbwhpcVqBrGq0XBn+BuJZB7+ahq/QRT7R/uZ0mG90Q'
        b'QcEMasTX0VEOCbF7Bt6gqVm0TABQDAZtQUeWUqTAj52sGHuGcYopWz15rFUAQ+tLjo+sBnTECnQaSjrOoH3oBNrJMVRb8NFi8iUrcLv+U1xxmy6OXASXv03REgMqBrdr'
        b'1fhyUnR+egRoTjm0RANqtFlbHUrRLkl4L+qIww1xMSIG16EjLKkGvG7YBF0MuTkZbQZlpwnUR+9ge/q0WXjvcvxOXGa+FTMDN0rwlSy0n6vtS2hzILoaClTFMrH4MtpF'
        b'09F7ePN89wQMUPFoJhqdQmcq//a///u//1KKoPfIYkb8pCZ6wXxGB9h1fEKBWrIMb8O16ZEga2yLzpwRhusIGflhcrxjVnpGDvD8OaRboKt55OPwRnyGkVRJ56NNeJdu'
        b'CpTUgtvxTQAKcrmX473cA9CZyNRUF53L15UxxnsB7UZn0A17fBEfLdWBXRRqVoTgjrek5JGdUrQuxlqM183ARyR4e4E0bbiX9fg8dAPdwkfw+dTyFTZl7sts8U1JjTXa'
        b'YpNrj9rxO/i9GHxrtdwf145T4AMStH+KHF2aGI+bPFAjOlWpKwBaOwLQQTEZK+ulTKy1ELXPQBfn4r0SVIc3l1qjveFoI76Fd6DtBd4Vb6FWvM4b3VoU6E0m4K1oE7pa'
        b'thpvFMaGERq2+eMLKc45+CRqVENPo93tjtibjRcw1u3Kt33vOMxldOPo2FDgdbg+B52dhmszyNdH47ppgEMDzAx57x0ON4POpStzckCsQ+/ja3YlaD06Sgv9SUk608Aw'
        b'MTGlJROqhLaMDpQZ6DJZLs7DhzTZMDJ7cjLzzcVoFzqLr+MWNhZtwCfGxeH6NHQd7y6CoYoPzAjFx+cSyte5FqANpai2HDfjDquF6KbTSmYhhQShsz5CS4SmR2WKh7sC'
        b'zhO1yck/ANecsUHNc/G1afhigZzlUEfrqtElChfdEY23Z0SS+SIqIE3CuFuLYlA9PsNVxh5tYVZUZk5+OpUuMwCUFjGTQksNA2B7emRmtiKDVM6+MNJJtsjtK/C7+CYd'
        b'hPg0Xh/2Isgj1GaDt2aROaOWkAejHtWjw/idYeh9gLmxjABtZ6cI8GYd+A3Ghxbg7RHppPa25nCDITozIyovjHzwpomR6TMGodHSiTS+FCaDaXlRMwXMygLHlfjOYtrD'
        b'YtAltJWDgmVM53GDvCifnp1Lv1cx3Xo5vjo9PTNHGRmlpJhEGHmRpHvf0KPQKGALb80bhk7MFtF+8LsqIWU6YkYEiG8X2xCmjmL/yCTYGpbFqe0XhwjJEt8uQLXoXbRZ'
        b'B7CwmhC0LT9XnoO25WZEZsyYZYaE5GCQDOmEp9E60r678NZ5MnQGdaD30gPQHXQT7U0PiEPnycR1Ea8fjppS0EaKd0PtYgWZQi852ljji7JkR3xJu0zHMi4aYS4p6BSd'
        b'9wpX4xv5eG9cppDBH+DrLD7LkG64IYzCDdF2fH5iljyK7m4oCWFhel4mCu3R24DOl1mTjnwuXgcrdwkZ+lvz0bYCvG1GDhmlJ1hGHM6iA/govkwXgeoxw/AHgXbLHViG'
        b'xftgctnM0GnRZjrqwPXZY+3JjTEM3h6Er1NA3mwypi9nZSsz0FY9LsJurgC/j68n07Vgrqs9B94RMlX4FofdmRZH3zVpOD4/Dl3JMiBh0CZ7CjYchraR6ZCi18RkPKE9'
        b'Ij8WHZuNG2iV2KAjU6Br5KjI2+Sw/Ng7CV1jinQAowiKXUA6tpzuoURmAIwDSsGkAsTMCLROXIZOJ+oowOVdXFtlmLlJS19mSas3CtBedBhd5rCG+yagKxFhUfgkfoeO'
        b'DjFjXy50JCPgFLfM1YeQ4kmHEAPO5apIxKKj6S50lfVbBaNrWlSUkuJIJPMFrmnL6J1luCUX11O8TYynaBSL2oRk1YQ7uln4KIxqIZMZDR98HDfic9yLrtrPxPX0Fr6m'
        b'FU1kSe864U/nC3QM72di8NUIfgCTHgojWMwEoN1imzfLdQC9GOH/FhnqdblKvBXVRZtXTzTay9WzEq23wg34mjWtZHSbjC0APsmjqnQSxmasAJ3Am9B5brScLSc1egkw'
        b'iJesGHwnRoDPsVH4KNpTMff9ZwKNM1k6t3yYsWlmTu6vJzv95orvhxnptTYe4yb/benfwjflZdqdO301OX3GL2+p56X+5eTP7iW5tHxz4trjTrvTz4LQji97L/iOu9Ey'
        b'tvLQyuqyz7ce7fn7pWf7J+93/jvWjf1JWHda398Sgzt/9+7Hnv9SXZeNDl56/udzjqxfPXvkd58Eq1I+7LkTFrHJZeWMTfvGbnJDH4+ySSiI9f5004in//IMuKf53S9+'
        b'fnP6E1+PZPf4vKj4mX/97+L3grVlqbNw2vu7t3TWn773K+uPLyzy+tN/rtmwJk365QLJk2v3fp+z6cBG/MaW7b/Pi4+fPd+jVSezv/1e0a/yRyxeMezOxnHLU+T1B/75'
        b'c/m2r1HjX7eMU5duva522ftl/fDClZmae9Icna4ic/Ej7HD2u5G/FE+dHvroD4l1f10SNevXn3zzqLD4zYW//Z/GT4eXbbH/9dh/JRd/uCnjL82itxZe/NWtSZ2zI+I3'
        b'tX0R841j4cFtm0b8Lfe/fvJsX+i4D+98PV/xk+8iPv+vvCRd+X1vTfBf1VWBVSOTvrO5ffAPH/5s3u8nXO1eLctZE/LhdwKrm39WbvlN54afz7x3UD1nf/VHGpu3/vGH'
        b'Obfyjo6/N3X249s+sy4t++/3fdbOy/ofn7/+YU/Ng4ST1x8+ujFy87lT9pl3bcIvnPed/Yvxfyl+T/pJlO+iPe3SB1dOdV5pevLfh9cfftD7yaLZHg8FoZqG3TH7Rr4r'
        b'dZjU8OcyP62kPuOTBaPW931T/Ksfz7y37Ebrk/T3T06sv5ez6us5NWvcNuzYnvDhwtlupWeXR/7hNy5rr87v/0Xdx45ffLFioVRZvnh77n8qJu3dqZ3U+6OHh3865tcZ'
        b'nkFBv8n4S/hV7zvTI9OQbe/ZZbNQ3a+FVn/QKS79fVyq487qL2I+P/65za+d/8vqZ9+21P057puPh42dttpt5x/n/+3NOp/AJ0l1PgFPMupuMt49JcW/vX+3+eGwlEcV'
        b'Pd392//8x5o7U4ettnF4P3TMQbvSTbMQ+sZl3rzCetv3q+/ibyp/coe9sl3z7bfr/3Wy2PWSwnXOlv+NQz/7bVvCdO+Zy34iLX4c1z72fuiyf83ZOWfTl3U/OrL4iwmb'
        b'XLfN+UvVv1LvRed+Yjv9n5nhn/+LzT3pcLWoTx5CgWJBeE80qgdY3ZkkM2RdEDpBsXvV5NaG1bg9S4+FRE14CwUPoh2rp+vwdeOM6YyOU6TUXHQDbzCgMGHnGJ3jYZgZ'
        b'PhyM8gzhLpv16PRInZixRlcEy9EVdIrCFvGBxfgUmceryfptOo9HKDgJ+D3cIdJP5IRLbOZmcjIJHOTud6TMI3I3WZGarExBoni96CllHPajJt+IeTJKopiRLBL44VP4'
        b'NAXGqVATao4IV8jxlkjUoCIz/BwByBKjaG2MmVMVIUpSwBoXSWZStF0QlZ5KSV7igm6h60lZBn5YxDjOFFbi5tCnsGf3ZmgN3lAOmEDgpnKNLLiE8c8S4SNjyihlmpVE'
        b'tMcHV9DXM+QFZwVxeK81D1+MRHsjyGJ8lUOHUmhoCdpBQXB4t/1bGrTNepkUX9QAPtzRWmpLmPgbeK8ZZBNfkaDbqyM4oOFWdEQZod+7z8CnuO374RlC1IwvTqNaKClq'
        b'H5OlVxcQxva9XNrcw/BmIVljG/A6+vF2cTloxxREuLct0VEwn2dZMY65woXqau5FzaRxaiNyI9HxAiJR1dP7dvi2AF8jU3sj1+SX8YUJPNODW8lCxLM9YzI5COktH7yB'
        b'W97s59LFDR+2ob2tZgVLEcO6KNSKLpthhi8EcBVXh1pwG6oPxsd5wCWgLR1GPwVxDdWRNf2i5c0YfBwfMocPfiCgtbLcYQ4MGg6xehRtN0etosYCiqIcg94bQ0GUGXi7'
        b'Fm0YDKIU470cvvUdBEYFZ9DGCIU8k9O5iBlHvE5Yjfe50W6JzijCCSOPt1aO5GrBrkqAD4ag92m3SWDj+CUZXcX7uTX5Gj7CPXmOdPxdegZGjjdQ/mUavkHrRoRbkoF/'
        b'SXzLlH8RTX0K8YzxbcJFXrDAwljjAzwHk4oucvjbO8MJj1BvAlhNnsEybvhd0XAy2tY/BTsQCTrhN7CivdCZ5+5Ho3eUdDcN7yMteBDfqs7KziDzUB4bTrLV0q4RnrEo'
        b'KzKMTCRZb5SDvdgZwcp5I+Rh/z5A5v/tgWq8TLXMg0OrDQCF9jkOiEbEuSIwbMYNuEu3AR3E3OZwQQAjCz66pmkNB/5st+oY3u0/HpCUfvtX71rd6x7UvKbLPe4zv7BO'
        b'efZH2l+u/unqLvncbr83Oj3eeBSW3ekS0hscdiq7JbsnOKErOKF9QfuyzuCxDTm9IZGn5rXMaw9sj+0MSWhQ9roHtzrcdx8F6YUthQ9CRnUoOrPndyXO7w0Z2a66H5LY'
        b'8Vbn9Bn3J82gr0r/aGKXfE6339xOj7mPnD2bpjanHcy97xzBY02Xd4WkdnuldbqkPfSVNbsBNLPbV9Hjm9Dlm9Be0u2b2GDb6+zWGN7lHNzrL+c/TdjtH9+e1+U/piEd'
        b'zNLH7F7bvOy+exh937TO/Pld8vndfm92erzZ6+4LGNnWET3hE7rIP/cJd8M+VNxTdE4veJDM0afsnD6rZ3pRF/knL+r2K+70KH7s7NtY3ipuVTWveeAcD28YvXuN/g39'
        b'AtY3lf1aKPBPY/sZgWcaYEOjR3W5RDQom6c+9E5or3rgnUqLfrPbr7DTo/CxO2mMB+5jeuUxjQ69gcFNVo/kEeQsILonIKErIKE7YHRPwISugAndAZMaHHq9Ao5GNUUd'
        b'jG6weugV0lze7aUgZ85uDTW7xzcH3XcOoRWnrzOS/la384jW4foazev2yu90yX/s7M4b7DeP3PUWpSat229qpwd4XWta3RrfkfLAP+m+exK9ldXtl93pkf18DKv7/om7'
        b'JjaXn6puqX4wYnQv36v8g4++3fR2a8351W2r74o+lN6TNr79wF/5WWBkZ9QbnW+W9rxZ0UX+RVV0By7q9Fn0yMPvqEOTQ2foGw885lFHRi2JrQs7hA+Cxj/0j2hNP53T'
        b'wd4N/jDiXgQpZGf6Q1f/ZuvWoAeuiof+ka2zARmcDsF8F7ZaP3CO7fUPPbq2ae3Bt0lGz6Dm9FbVA08OIv1Gt9e8Tpd5j/VhTJtrTq1pWdNecD8hs2N+r3dAc1rTpNap'
        b'7W9+LWQ9UtkGEfk6knF80/gu51CuY3Z7Teh0mfAIXJGRSg+irsjAecPOlMfeflz43La4Vm1PdHJXdHJ3xBSASXv0yBO75IkdY7rlKaRknzS2IQWAwx77J+yc0Jx631kO'
        b'YVRSen2Dmhc0vbEz7ZF3ICA3eryju7yjG1Iee4T2ugQ/ETp7Dn/s7t0vJr/gAyu434qc9VszpGP4HPDpt4ErW8ZTdtTugF2/HVzZ6+9J4cqBPHM090BuvyNcOTFB4T2B'
        b'o+8Hju4fBiUOZ3wC+53hjgvjG3HfJ73d4a5VZ3T6fZ+ZH836KPNv/a6Qy43xCux3h1wejLf/0egD0f2ekO7FePn1e8OZD5z5wpkfnPnDmYwJjOoPgKcCGXnUefs2+56w'
        b'5Pthyf1BcDcY3hxCzhrE/ZHkmR7PyC7PyB7PmC7PmHaXbs9RFBn+0JdctK+469Htm9mQ1uvktt92p21jQnPYA6eI3siRDSLONUZzSpeTvNfJZb/9Tnt9CkR2cfdpsDdR'
        b'evhzSo8DgJ+jXiJC4RBBwcelKwyQPBMvDS+DPP6BlglYhQfhly2ZDHxj8OIz1IoQDlqadIYHNU8PYNl8Cmo2P74MtBn8wlyUJAmYewK7JKlQzlK3FsoXAPKwteC0QfJv'
        b'AfIAWO6hwAJYLqlMW6qWlRRXVtLwdgDg5cP9kZqqgCoqrjSLescFHlCpuEg2xbKq0ppBhXLg0LCiomlLtBlVZaSVFlRWlyyWK/gIhXr4nU5TWqarBAzcymqdrKa4ikLP'
        b'VBXLK1SDIWpmRFRU0Yxl1NMf7+GmVMO5veGi68jArbusQqUZDGAblJC4tFhdvEQGDgoTZRkUBkd6uaYCogCS9wAkrlhWotNoq5dwxRo+LUNVVCQH789DIgdJ/ejrA04r'
        b'qmTLRytGkqpIJtVYA5WpXVisNVBrBCdaLJH/NhqakCKFOQggKQACFZpVkd6BULm6WreURiexWCL5dG1Fia6yWM2BHDVLS0sMfhc1sjBwsxZJqoC8ljrWXbmUXJZqSxRy'
        b'2ghDgByhQrWl+nbh252Cw6sIzTpSkaR86HUr9a2vqqbui5ZCUEtLZZo1wOA2/R71tq2S7uiVLYsCq2/ckaxXNqLzuJVTNsrIYdWCeIOR74xEauZrtPFFLSN0SmDQb8ZJ'
        b'eC2MzFoIap7ry2LwHi+/dOeQZWvx+Ty0CZ2bgvbgfaj1jeQMLTqDW1C79QRlpC8+hFvwoRR0w38VOu0UQ8SpK5yaxD4j8RNWxpJpbdGH8+wYHcgkMiJ13ST/d68gAld+'
        b'GBjigWk52PBbMYGLRPgMkaz30efnrxTlnRc4gVFx9tYJc5iK4b5qVnMYvvhEBgeoG1vPOqti//BuyZYTMSdjzpVtaF/smde42ONnHlv+se7ZnJhP3TL2tONvLjCfLi06'
        b'3bagpGj2L6yLR8cuH+m2WHtRtazk9BtSjbOjW82T/5z5uTj+UvrWOnCNMaws13bxVbtO3WchG5b2XAi40bLhQmPdzgCxR/hXh2JcD3/sunVOYOO377XP+mpkTHDcjzX3'
        b'UsI9x3Sz+Tq/kXbD5XZUbgvOXMFtzBh2ZVR+ArwvPZFuviQT2ewstycTis4tZ5NWoH1PwdcBOk2k9MsgZq3BN78fX6AXs66j05wcdwTfWasBzVVUmH7TfpiTEjcIUftI'
        b'vI/bXmnDR9L1mzdEgD/Db9+k4x1UGsXH1RPBFHQmugzWoNQUFJ+Kp3Jc0WrUius5O1C8Dh1Yy6aV4PforXT3FRHkpetwi2F3Yzi+QqmqIX1ij10W3oE7jLtK/JZSJBGi'
        b'qc3iHiLnrzOK5SCSo52o3iCW26ONT8FJJemBxxdBvi1xVDQfLJfjO6O/FxJnlLZswGEHHdMDoGmGdCphQVgBkLDeDLEsYfXy9l2Ete5xD7/vHv47v9B+hpVPZnuT04CX'
        b'/UrIypVgT+afC/ZknrnsY29/whmS0ggfeXCN3lwvocs/odt/dKOIsO9NU5pFBzNaBQeUhCFtLuz2Suh0SegNCj02vjWeM+iiXsLuE8ZnWZdT2K94z45mmMnw5zE0gzGT'
        b'YuEgjJ6hIo6boiSnhLCsx0ujJNk+K7JAFpIV0rLTPMo8sAZXPJwjHqHBEY/4h3TE8/hvIgvMQ35pFR93yzz8r07DMROldDona09qcsaUfJOQvkOtwKULKko0hSWVFaSU'
        b'RAqq1zsFL4OAPCULFTSHIhWOU2i2oSIFm5TK12IitQqINJgFQCA+TSkls1qtggSytllce/jIx0PSoEibkV1EY0TollZWF6v0X6+vEIuFQsgqQ8wHWBZ5ox+NrkLLxR82'
        b'EGV5RfxeqqZMKSiKfNVHZ7zyoxnTXvXRpNlzX/mtKSmv/mjyqz46O3Xkqz8aVyQbgm98gYfjhzDMyCijbBTPxZWqImXhfPcPN7PuMDc/ofhuy2zXUEYlaepiGtPS2Idf'
        b'xn5kFjDq3KywPE4RYzZaqN0LF9mMG07khcsril+tppILZlggIZFzJ67h5hiODm64Vai+h7ccjGRzVVIe7IGbFWOffUbAyIoiWxSFnGMXwgoeLtDYCWZNBq9gDGoiXMcG'
        b'qoWfg7dMw5diYmLE9mR6ziDsiCaF8qiozRq9E6FUAMxjJ96E9rFZaH0+hYHg8/gcOhyhzBSQe3WoFm1gx+DmYAoU8MBb0IYIJWwZq/xRLTt+1GS5iKr1cSPetpoCHvBF'
        b'MT6tZoRe7ATUgK9x/ozOoU1u5G67Fl9jqsIJr7KXDRChTbRQK/xBsWakWsCwqDWqmkHXfEo4PMqxmlQNvuqoFqOj+CR55iQbjo+vpR+Ga5fgwxTGRdje09FM9DQenjYR'
        b'3/EhD8EbL/HwtDJ0WG8MsD/WTU/jmBxKohIdoLfmTM7W01em5ehDN1Pop6F31qKtPCHXSP1SQtAtdEUHngSC58zhiT+xEIivmCsXco+dxw34uP51fvgsVyXvRnN3dyW6'
        b'61+Ib0dwb8TX0Ab66WvwPnzAbrmNRoRPohuM0IaNxrfRTfrp0szZdlK1I4MP4vWMMJKdhHbIOLX+MfxOMmju7RxY1I62MUJ7dtJI/A4F8IQTAaEhC/j6fGogA9ggwugz'
        b'+BjatYZ0oK14I7qJ9qBDBeRiD76J38O7iCCxB92MSR4uBiav3X52vDP95MiwsfmkZgW4iWEWMRmTcS3nY+sC3uOPd4MRztZ8hsgy5H8dm4Svu1csbmEEGnAY+Gz3dDCq'
        b'aNmdQCWFYiInvBeTGftgpPZiQvuvyHnp4pgY7QXdRVfX5RdVF4qm//LQkk/uTtuzBwk2npVXyr/UzL7YG/spO//uevn1A8OSe0b+KkZZFJmZ9fij//jJ6f1W+Zffjd1m'
        b'8/5Rm9Z3/ev/niqddn2f5x9XJUWWxXwac/7dd5NjhB/fSc129vjaZd14ZUy0341f53cQ4US0/ve2JZrYj0vvjVlzBElHeb9XuCfyn+OL/lm+/tmPf3r/l3baW37TlIJ8'
        b'hy/DKwQnL6p+uqs02v+zz5+o/vSHzX+eFZw1KfCzvSSbsOf8lsK36xLn7WC+dRl/MDbV6UbUZM8WL9nY/dKyN52DyiVMhm7W0XtiuQunS7qF3nXPMjodsZsb7SrA789Z'
        b'xt29HA+iGVXL2jnzrnHwTXSCkxq24OZFESYGR/aRLmiH0AqvE1M1zlpUi69yEg2+lgqK5h3oOqca3I1r0U3qXEychtsYEdrI4ndI9tv0tfHpb+hd3AjJwNvAubhBzY70'
        b'tfnoHbwBhBV8Hd/gvLpwuubboziyruI2n4hMvA3dmZQFEoA1rheg9XgvWsfpijegttkaO3yFZdh89B6uZ3CrFm2hEstcNdqF6pcmkME0nnTIzWT4zie34LFZ6BQ+Afck'
        b'ZKDtfwM67k5fVMfpIz8gffcC3CRlEoqJ4MLgXeH2VJ05C93OHeA65gy6glqFKfjcJE686piADmooKGoe7kAnycBCjfgid+9wqaMGbUW1ML5PoXWk1+PL/nM5FdqNYryP'
        b'PCdmWHY0OsXgQ+gDdJJShBqV0WTCsCdMLj6DTqD3SUGkrU9yqtdjy301y5eR16XiVtTI4K3ocBK9o/RAt8gdeNdNe7SPNPEMdIQKbKJKfBlfLRooSFIxchjqIKLFC+xo'
        b'gmgBK43RVkxDWOtVw8ztf0gSla/AJRjIV1UjDPJVTJd/TPvw9oBO/3iQr7waJvX6R7Rqu/zjGqY+dvZqXMP7Nll+339Cb0h4e2pvsLw9gchZvomfJ074IKhDdafig4ob'
        b'in4h4+r1H+4+vUEjTo1pGdNacP6Ntjc6QjojJ3cHJTVa9/oHHV3dtPrg2kYRKZ8X66w7grv9J3V6TOp1DWguuO8qf+jioT+FmDUrd67sDI7vco83PiLq9k/o9EiAqOCe'
        b'TZ7NZfc9I4e8WXrfM2LwTVfP/XN2zukMTOxyTdTH0RmY6dEQTzWPuO8a1usdyruXTun2ju10iX39myH3XUMH3fwvN//euNHXxl0ad1f0oQ22eRg3qV8sCEgi4i1E3+hn'
        b'BMOSWRNRVML5ALE3FYXUEuFgSwQJo3exyUmjENPZQo+5pxdE/2cd8+3bRBCVv6wgqrfCASZHfQ5s3t0H+HDuExXmZij77AqnzMjLS1VOyUjN50LLGHw799ktLa6o4r11'
        b'qA+DPsHW6JGC0zcANJj6OVEfggP1a4LNfUBTl9Cwq09lb/rJcq//BxTXMHd/j6panQvKCDPXv8fBo8osLpZMvwPj7dec3y7siLtb0uWcWQuaMHef5oR2cceMj0J63bwH'
        b'nX5lJfJ2qM36xl4ojfjOdqK0hH3CwPGryQIaFUX+tZD1jqjNegyxTuS9LhMhIMpkLiCKV+BDp6hel2SS5JXC1mYaw87EQ1SYUTQoDB9IJRWem8qaxoCBsCyuyVzYFD4A'
        b'C0Rz8R5LA7Dw0VYgKozHpNr0b60dpfFfyRjPgC6P6Jaxx8eRn9qMb0SsNAacavvAIbHfmklip7DfCWtYqe93jPH4FT0+UQsZB9emoAdSv28F3lLyaYyDfz+cPUmEGwUP'
        b'pIFPBeOkySzcCfqKnnKeuWGSzsZHR5s7CGY0ZFH3miqqwK14sxmDr3fg//VG8MftAmZZRo/cc4XgjZvzxH1IxPvi5s7BI7cN+Qvn4Jkb/HJz6cZzJ9Uw1XCVMz13Ubka'
        b'zt1U7uTcg557qrxU3iqfQ3ZzRaXiWkkZq/LdaLDEAQ/evK9pVmVHjvbgdZr8H67/f9bvjBWX14b8VYXySiWhyt/EE7WVgCkV8364Aw0et62NZZP/ULqgTMCX68z/OsFv'
        b'hTF9OE8D/NqQ/7ZlIlXQ2WAzGsLALzlQUWtTK60dXutSZq0KMaHGhvrmllAHvMPKJNR/t20ts4Kda0c92Mj7hsOwmUIjfVN/7mWl6mcjzeS0wRm4uKBmmZ4piNCXWKGp'
        b'TtRoVfR3ZEzMyJGJIDsmrtCoEmGSUsTExJL/RCqNkwv7RMrcvJw+UXrG1PQ+0Yy8qdPa2D5BSio52sArC3OV2XPaRGrg/vvEdK+mz4YL+l5BTsVllcXlmpd5bSy8VqSm'
        b'4dnlcAgXwvyaocznQnC8ZFlj5eIBZanjaYH5KTOTniUv1GqXJkZH19TUKDQVK6JAilaDu5moEt7VhaKkekm0qjR6AIUKImvHjFSQ98kFxvLbBNSJuLqcepnps8nOnZKU'
        b'XUiE62cjgOgpyRmUQvI7rXglTIB5oFXSaEmhiph4ciSLDBTWxqpncCFPIGZ6n31+hnJqdmphclLBlPQXLCpWLuToMnzys9EDHpyirtZokqnUb15GdnV5jqaclhQLJQmM'
        b'JRECx0NZjgPq45nX0B/1zNVi5cntzEqB7qaeZKHssWoIFD2wkLG0kDj1ZLg39Mtjn0W8xJf2WalKy4p1lVpa/bQt/18xWGUYC34ngDGPtEXrObOJarSLWk6swrcq8sv7'
        b'GWpW/JcZNgc5o+JL4l99ydjeFiT4aIcwK+6zLlRX67Sk13PxdMynE4X+ppmF8So54+H7kkajEA36uW+YIDYxHa2Rv4LpaJsVx1IdtMBXHdYzV2b2pbb6Cuaikw1hX8pS'
        b'a1Jwl04dpZfZGmxH7X8w21GAKmywsqBtyOD861SsKjXROZTQKuQ03zDpP0fHkK9burRaDduXS2l4ZcqLahIHZ4ySDRiYsrCUVPnzs8HA/t4cY2Vh4ZoKUKMvH60YFf4C'
        b'RXJzhSxsSvr3Z+bnBMgcKfu+9ww9X8nCMgpe6onY5zzxolMPFDGQ6KHUOfyWNLd3y7k+UpUu0FarDZFhh3oS1mfusYHdZqm6olpdoV3JxVoKC4dVP5wQBOt+uOUd/nDg'
        b'BiAPrM3hoM4Jh0U1XK4wIj1GKUYqYhL5LJaLMYJCYmhWvlRj8iiazBU91IdxTuj4T7PgSI6rn1AN9SU3ZPVQxWWiue8sOsgsO3vjfV8NSZPRgxtHGDdeB7piA2dnBlyQ'
        b'BdgP/CH3dKBGBA0b1WxQTFJpsRY6FPmolQO95QEqZggHXKAdIeXUFKt5CJNJZGFaO7L80lL4Vl1lqaxYS/i4BTqtZbKmJBWkTs3Nm1M4bUbetNz81EII5Z5PqTTAh6gz'
        b'MAsYJL6SuEmIq59pSRlKvRNIfbvpJXler2MZbWPU9VD9IVeCURUTPmBOCR8Sr0RbaCk3TjW0Egc8Ozac+zp9looqy97BOE92hAPm1EOAUKqSpc7IG0JnVSXLr6nQripV'
        b'V9KG0z6HeG5CHGIskQGToS2uXEkfHHqGCx+6z/Iu+LgGMXrmg57PN4nBSx+nPh7ii7Qc/MokGJvZs2b+HYectWhJg/R5pHp4Nk2j774DyrXcJlQoMR0pGclJStmC0srq'
        b'qnIo6Xv0XjaDODAnJWeueR1fhzgOWegEXoe34wYhI8DH2TBb9AHl0NLQKYes6bNNHDygdwI4yBXcHp+Hb2r4yCK5+B0Gn8ONKTTkQik6hI6A1I624mv4Wjo6hS+hOhEj'
        b'xRsF4E4btek4X/G5aJPeGGlCHHq/gGGG42NCtLWoSjcGMhzD29HefHQU3bEYmcM0Kgf5nG34mq0Nvox285op1IgPotOgvFloa0f4JlDdRC6ntFvnRtpJ8U58Wu3IUH0P'
        b'bkH1FCMWgi/Em8RhMboOwLWqlbwR81KpNC8M180Ki1LOCAvDW/DWaLDEaivgA7xESUid7HdmpzincYTsRTerNfo4IOjdFQzekWpNdY/9JC91FZG0NvvHo3MZGgsGbxRO'
        b'Ng0Okq7IzMF15HOj83Bt9vR04Rx0IA/VgZMD/AE6sTKEQXdEdrhxSlJFf3+PQPMxKeNH9xyXNOTYohinTeWL+uLrXFN2HrNa9peMz0Tuy3r2JZ/4TYf3vRMdYUea98ef'
        b'eGq1y0H4MDju89W4ZOITO/HWVPano69FB6XGbnLZKfvtV+sDG+LtD62y2RacuXCV3wefWdecFN76YsPjz5u/ydjx7m9+yTxM3Zywr+HwFlXgzs+7jv0+eO4/Ljhs/qlz'
        b'xp96r4+2uyb7pn1seY7072lZu2ZNrHim8Bv382vBH3+ye/q2N0ae/fI3H//2OHtr4rfXxnZ8PCLrXIQu4323ut1jF4tda3/tf/xo9JXZd+RSiidTrsQ7I3zXKKI47NV7'
        b'gphsEXXy9uZYdJYLuQSRoyIBRIaacZMV45AnjEUtLKeh2Yvb0AkKCXMndw1KFt8V1L4pCHqqAcx2faKJ//5t+MZTuiGFr4/jTQyzq9kkvBnv5GIetOWijUajOlxvy9nV'
        b'oXZcTzUNq8l4uIX24PWmBoc8NCwRb+f8zx/D21CriVYFncikPvmFKXGkGNjODS/C1wc499d79k9ZLCL9fG86R0/z8rf9GUMQBkMEBjIIOYOqKaSi6sgHZuFGap7IacHE'
        b'LKcha8RXJ5PXXEN1I0idXCa3c1gyFdjRNhi+ZmYW3p5N6mABOhrDxqJmdEdu/1pbsLBtZwoGN/FnbVHWMnUdL+AUKk9VEcwwt063sNbgLqcxHe53gz+SdE6b0Ts25W7Z'
        b'RwufCtlhs8F4xcvvqHeTd4Ok19O/eVSnp7xBDGoRC4ZEzu5GQwb3wObKLveRv/EL6x0z/o70hvTe8n4hG55LUW7TKMptGvvI3buTlOEeDXYzDBtOAXFfkWxTabZ0mi2d'
        b'fewt6w2LahQdkvZGxjaKHnjIHzt7NKb1+ER1+US1lj7wiX8EGhif/fN2zmsObI7tdA1pdTnv2ebZ5TqyY/SdcdfHmXrA7xcy46eyna4jTcRYqYkZwHNlyKHRchAG0wyk'
        b'/4INkgPC73iGR+TPCgfX4t+8rINx6kOzWRLDtNuNezUH42Wc32xxIQgEQzn5tfQdele/28h3qAEJybn6VbyA1DHQ4TdsP+anJ+X1iVJSkwv6RFPyUlPkVpaMM9Tf6kNn'
        b'9lmVLCxWl5dqzKR7R/1X15LDXushvUeB7yirWgci3YOc70i9RDnVDitz/Df4iAI5v9WSnJ+kUhHm0xTMrudzLGzyGjjkwdsFZbJE4N8TiwyOE4ssQKAieX7T4AoY0PSD'
        b'jQ/I200JKiH87AIiN1TrtEYpQgsVr+VlrBeSXnm5g+sXLyDAFi8xPmtKDpcuK9bIyiqri2EPiUggFSSlSrdkQallZh9eV2XYLwHWUY+1TKKlWYJNcVSYSXWmZOhlOm3p'
        b'Ck5kgVrh3CEv4SwBhoD2kzwVKuC3jVWhLqW2HYQy7htkYYRQNf00yk8H5qUpFIpA+RCSAIcio2YqxdCbNFq1rkSrI6UbS1bI0vQgTJP7FsszPEN7pm5pZam+C/AIVyJ6'
        b'wMcS6WgJqUqLZYTlpaalgno0tVA5Iyc5NS9SphccC1JnF8iHrO9SapcClV1apYrSVkeRH5P6CateytnpPKeEFZZkcZJaqv7/2HsPuKiO9eH/7C59qdL7grRl6U0QEOm9'
        b'NxVUkK4IwlLE3kURBBUBUQEVARVp0mzozE3UmCjLxoCJScxNbkxikmsk1RvjOzNnwcWSm/zu/dzf+3//V5N1d845c+bMPNOe8zzfB/v3iO/Ffzc7/Gd6q45r+Pd20tN4'
        b'apFUvzK37PzcdDRqvnLTzUG14h8T4R328gb71a4sf3DTnV6csRS7tdBVgX5x8C8isCK5wf2iKCMLyQUSkJSUiPw8PFL8jo/P6qLnd8eZ4VzQHgv71eABYlp0MwvzV6Kq'
        b'Sk99jTNObjGt28zKKcnIm5J81DXTsTWkRVp+Hj8HVRfOCVVcDklFtfzagtHZiGuEuOKPSRc1f9nyjLQiejx49R40NtLVxc6eCDdqHPI8uAxWooAPouclKhrcN9Gg+Mp8'
        b'MosLSV8jvZ34F71+I05PYnM5saKNL59Tmp2D9tLYXakM3SU3F3W+1EJ6+0uf/Oqxhc/PT8shjTC9DV9VmI86MrFRR1UramzUEWixf3VlPh/lbDgRaEOeumpVbk4asdPG'
        b'GhHSn8Tdr17dd3zpMSNVNCiiu+P5nWOBPrlWHDzLcywi42O4uDHwbM+x8PGPeE0/tBTzJ3PhWv4BL7dpo1fv6aH+hQjZv2dM/0+0AYb0+xgwFB8hCqy5gk3jHJt4ZFFJ'
        b'NqrmvmijatfBoDgp8v2Lg+lom6DCLn9KBYB22jvQlt4fbg4g5pZRaCNxHFuNEotRuMkO7IFb0c4f30sWnCjELEQRCLGBDw7KceKKMbZCE+61JKqDzXxaezBDdVAFjxaH'
        b'o7OcQVcGrBDFrMThUONEJK9Qa8uEIKuQ+NdoCsAer+nYkl3+KmjT2AWbaDPWnXCblcjQE2sKLDZ4eYCh4nh8qHO+9p+82fOoxdEWNOAtG5W9kseVoubaqcHuFD5twrsf'
        b'7REvE8tTrIWA2+A5L7QJbC4uw5XbBy6DLaEEg2kdEonVEXReknAf3C5nqg065J4rAebDzfAwOnBsFtgOTsSB5vSI3Giwy2cDOAS2gNPo73H0744Vq0E1OOmzbAnY7VOY'
        b'Ex29fEmhaTJoWJGtTMEqTz1wGHblkObL0wS72XBglTyTYsKLDCeMGtkHO0mFoCzLwfHXlkwO7YF3aYNd80HNMrB9Rqm2o23uAfwd28emKMGdHAqciVbRAoOriGBEwO0h'
        b'xEQXm+fqgC228Bw4VbwMHTGShvun9TLcBBH2clVxcRysXqWgBPfFiar+ucoG9sOmOKyrwW00xcSbQkOCzaBdhtxJEZZrwE62QvF8dJt02C1DeJuvI5Lia+IspqF9XCnY'
        b'DY5TsB/sVAgEA3OL/VAm0qtATagoijUxDK4EZ6KI4KBcQwmeD0nTfkl+CNg9C8n3brg/BonibgYcKVDQhPsD0+DB4jCUUSS8oPVSRkHP9/4JM/ID29nggJopPAl65qmD'
        b'NtCqoc5CnStcBbSCpuLieRRGqXQYTOFE4SFfsQdjwhZ4AN3pnAdqnS1IEnfTlspg3zLUN2LkY2zgYHEoysIhO0lMPxYWzA2xtnlFLNeYqVIplChYa4t3GSkKHimeBWrW'
        b'zStegPvAAbAf7JnCrUUH/cm8cc5L4MDzzGNC1MBFuE+PWITrg0F4/rnmbRfYi6PwNsA9xCaOeI6aUCyxKMXPYxQPoe5y2R7UcpkRcTkff31dkn8H7SK/GWirjLsZAe2U'
        b'zx3JajzxZePYQTll6er7b1ca3r8uHReksTPuFMc6fvthVnkFr8Bvnd+GfZVJOyUu7E0e+/btW7fev/CL4kZl74s31n97UmJX1ntbytk1JdveDexN0I6I8+h9V+uNA9cv'
        b'Sngf7bzBdy4r11l/IOXbb+bLfhGvNHl11e45NvLfPjx/3Mzx6HXmNan+Wfz30+vf3x+6bVmdylflS6WKGT1amSb/aKq/bxNVO/bO2l2fKh9feWfbFn+evHXUvaz3zsxR'
        b'4p+TO3LnjsWFM3NcPe9ek5aKiD3+tWxXW/MX6mpPfZa4rv28v73vw18sD1cNtkv7PP2saU1ns8HoqkL24QvMJR8/PG9UZFuvrlncuN3D9qtTZaaanTHqtVZ/13pj76af'
        b'4n59umPhGr8ip7eyjkmdufzWblnH0Kr3TQN1Fi+/lDmY/9UPfneOLXkQqZSXIntHY5mO40c3GebvWh95ECXcrPSdwKD2eEzi+cr3uKWDq36Kf1h7KmfAeG5s2vcLMt+Q'
        b'Upq1NiTbq+fBg1kP1D/67fzOQemlFzS6JqWUGo7MXeFUsPrK4QJeluGS0urxSzsWKpbmCajLA/ofVZ6N23HPr0Mq7/H6O7fl9EGy+12Tyq3M2Dn8FWZhTybq7D/3aH7r'
        b'gW3qSP3XAXVcDWJmbWQNemewsUAv7MN8rKMeRK9mk1EMKmDnupcCfLaCLqIgtPcCLSIFoXIwwxv1Jxo9FQ7a/UPROHFW3CqdCc/6xtIatwPgQvwUKgzr4mA7qAONUmG0'
        b'YrBbYRkOP2rzcjDYUnCWFDxMXg9W6MD2F+LNovs3kCwWJS9+WfMIesFhDOa+SLJYALfD7il/WUl4GJwVmaD3htPaUzwPV9D27cS4HTSpYKoZbKGNs2vgaXQY9eFgcEbC'
        b'Yz4llcs0huf9iAm2A5p8zk0h2Cx9GLawE/TSUUj3w0vrX7AkbzTCOs8lqOqwIywYzoM14kpPWAkHxRSfErAvLpjmtaFR1DqUpyKaIaYwUfAiPEAX8RyoBTtDYZUV6JCg'
        b'JNBsW+0DzutIk4tTc0HrSwrTsqQlgbCOqD3tot15RO8cBS7Qqmf9JXT5OtaDztCwYLDLBFx6wXOZRdmBISnbpe7E7J0jrUfUy2gyikTLD8UcfT+W52IdWgKGQSUoF4Wm'
        b'tQX9tD+yuci8HzXSJQ1QYRtuzWWCnQWUlCeTIwlauZr/Gwaz5FFEf16P7jB+hX7tVUgnbAeM4zFkWuPQn2btZu9q2t/Vn90c0O7XFd4RjqlIAfdfraPlmLTJt8iPc+wF'
        b'HHuCbOI4VytMGFmIxbysVrxvYjFu4iQwcRo3cRWYuA7pC00CR5WNJlS167xqvNqdRx18Ry39BKp+943Na0In1I2b08fULds3XFEbs/W/b2xWE/pIijKx744QzPapDsXE'
        b'ItsGW6EOb0wnqFtqUKlH6YqzwC6oWvoRZypqZk/pPR2TRxTDzAWri9nD7O9YDDM/EmLTn4TY9GfQpBy3GrdmqTFVs7u6xiKlsTfRFfsQXbEP4xPd2aIQl8c9GmTui5mx'
        b'P78igVyRSK5IZNzXNEDHRXSoKd6V+HWaBqLr/Ml1AeS6AAam87gfcqehUkKD6FGt6CkNePyoleeoyTyB6jxUaC29uvU160c17boTaQDSmHP4fY51t9oYx3nIZHxu6Njc'
        b'UEFUEiEixQuNE0b1EnBwU3RNu6RA07qbd0Vt3DtG4B0z5hBDbiaCZX2iadCytnv9dcWxOQkTYmUJExqEj2qFT+jNxpCfbulB+V550QP4kAfwJQ/gy7ivx2kKawgb17Mb'
        b'07PrjhtM7kkedw4Ycw545dmP5HD1u9e4j6tyBarcdtN3Ve0mDM1qgu4bGlUHfaauM6pr3V4kUPe7kng9czRh8ejStAn/qNGYRaPJ6ZMshkYmo5qJasPQrJp5gI0rajqr'
        b'UUv3d1U97hpZIOkN7gge0hiz8rpraNzsRLei0NCu2udAEEEt4Tiu7fICVacJC0ccC9V0QlTjYQJUGhNetd+B8Pua2tWyYrr9Wa9F/DzXIhemv+xw8Ee6NXZBe5nM8+d6'
        b'dLWkeJzRxVYMRgzB8MQwHpPPP/MaAG9TW6WcqX62NzXzPYDU1AY2G33UShFbRtoKWbpcppzKlJq2apT8d1o1Pkl5aV8dk5GXnlHI/2cKbqJNE+3gsf4mlc9ZEB72T7bp'
        b'BtSL23RuRLEXXrN6O4U+52VEi4DmHHhummlekWjxEkEDTeidCuqL4ADZY3v4wE1ia154lnq+7L0MO2AP7X06hNYEzfTiGe1vGtECGi2eQ8FmsmyWyXDEh4ps0ILCpgR9'
        b'hGDHNDNYabJEck4o2Et7m25BmbTim6AstiszDChQzYKVZO+bZAYvoy0dbXewAPYQ04NkuJ1oG7q8CXV8vgEzJXfr2lQ6ggLcYwE6SUgDHE3hBAMepcBI0jpae7HbHTbB'
        b'/SxYDdtJGALYBY4S107LjaCTLVvIoqKMGLADbebXwtN0PIPGDBaPaxkuSa1eIFHGgJvnyBFNQAbYxQjFy6UISTt5SkqDKY/yOkU/z7kScBRtZ4diYSUqHpqowV7Y70iO'
        b'qaFtxYiIPA7OeNLg8dnpdOkqV4PD9DZfBR7C9gZz4SX6mYZgH3fKZ5VSZhKX1bRYUkOrwKn4KVdXClyCJ7GvK6xyJKW3z5LCahIJKhscZKExDu5cSOsxzuYbTqkxQE88'
        b'tnmAB2WJvUW4v1YsqIS79OGBeLSMqo0PZ1AykQy0xe5NJrV+cNVeSo9BpbztkaLohSSfJPZmzKbQpnbBiGIKc8GyGDoxuphEB7C4kpdiWe7uSCfuNVOgULmDDi9Ksbqu'
        b'nkYn/khpUlYUtZpvluKxzCiP3nPBHejvlmmUOw1ylwmgUe5L4UWR8IDN8LhIB2EJW7EawtbLjFToYnN4AB0pUGBRcGAjS43hDjtSyP3cJIhBhd0isxQrXxPtqZBlaFNb'
        b'sYZuAbQ/PkJMPjZ704ea0AK+gtY6oOUk8Qse8COyky0PdsI+dJk0pZbDMmN4csEgl0HHGNkM2x35EXifkMpjshkcHOJd5AYeBc6xS+CAEpOyAQMoP1ewO5AWuSrQI+Ps'
        b'wS7EPtZn0N68IJ20dJgp6Id98nBAGvU0SQbcj46CrWCwGI/NKxLy2RTaIe9F1U5FK7nQmqMhuDOZbWHJgz1haDcBqmRCmIvcQC+963VBe/c+2xA4GMYAu/IpSbCVAQ8y'
        b'QGdOvX4sk++Hxuk1vRqXFv5jhV682uXSHy/1Na7/7FKP2ftmA7u3ZDdqqLAH4vyyW7ZYBFTvOXcv6C/hldFZUXKWNe0q1uoq3t5+g3LG/nF+u9styo23bKy4r3R02B39'
        b'eXDhYVhS38jbbw8/+MetUkP+3936Hjx+sN3UxdylbW7MFx8fWm82pApqPB8uHHZrtbq6wfLayqo7vmXGkpaqx8b+8tYOi5u1ur2e5uH2bOrIwxbZhhrQbwluupa93W1z'
        b'0apfrYzdorvt1lj/sU/rhpXsHxzeUtcmMCje3fIV03OvyjGg0hIpqP1G1+oTDQXP05uP1q7JbrPT/5vlsGnXxfPXrE9JBdYUq31R/tCoyuZ04keH5xoPfNPKKsq/MKAz'
        b'5/il3Y2lvNsJX9pszHTYk336SwmV03lXO5fnXrU+rd2+TvPcLebpzs/nh2kvK5lMaNPLaXrwjZMj+17Iw6v7QM+czw5t7Nym1/vXwcrgppWG5QmtNW8FOvk/zWf+Nttp'
        b'bvQzPf/vE088KljxpvOw0WBGUvZ7jWUrlPtPCgY3tffX+n94TfKdVTw99W2nu75WuHbSYE942vx/dNcv/nqD/qRL8/n2H80TYiosOiRDDnmaXjrNcNdJeXBu3xsnQg4L'
        b'XDfa3ZIublIqlOj/sD3tXs2xwU3mBoP7Fdy+lXj7mLtBntmejZqPeu+k5sWX8hsdNfZG/ur4eLdWkDC6uaO9qoBXecOTc+vSPY2G0m1Dez/4fq3T6WtfuI5+evt+as5f'
        b'3Tf//P5a5w+CPzp4+A2VW6tPeyXA+Htefm+wdsVTGjH2KrGCjPV29g99q4t71RdLh+66e+XXH+58Oee7TQUHDD4ZmP3XH2oyHh5YMHDQ7It1OkbWewttS9NXuXzUPXCy'
        b'd9t3AXO9E4Q94LIVa120p1Rn29Cd5qdOg9olx7Q9vXjVv3xnZPXUwIPRP0/2zIZbA+2fdnq/HRvlD35zi71VVPHDvh+P1O1xvHhr5Teqa+7cWlF72+Q9Vr2xXNXygQdn'
        b'pT74ysq+7KJ+l3bbG7c2/2x5XdJ95Otvtf4y6fGu29d+79z8TXaZpPnX8p7/cAuzWX35ZGPjqOyjLcOl+msf3T097PK3w8OtI19e/nbcJm/xEedPjyy+fKxEf61n2Ir3'
        b'Vqx+584O38SvVT87Hz6Yed1j6bb36lqKVRc8/Eq9bwO4KGffVbCi+uo5qZIP1o/99FHAR1cbfzP7TLp8VYSDym8nvY6v+bj90ArD5U/fP5D1bXZJ2d/cPu1/aHxmcv5a'
        b'5QKN9Br3hg9+yLy+cedehRtWStp9z053dXhJP+BMlqV0nh4cjr+0f0L1cKLm52vM1T/+zviB4cSkxZsX7un0vntn7UXnw5/8xDB8O85eSfeN8082rW3hb1E7179FqYVZ'
        b'ZBnI3/jpcF2y92f3GuccWfvl3Svnn8g8OvSmlr9ujIKWct1iBa2fYxJYNxauck650nZGal/fiQ4p+TN1CxVMmryWKGh1u8cqrJN/xD3F2PqjxJ0rG8/8GjlUGfCwxLOx'
        b'yaf4xse+VxTi1kupF5V+cLuFuaok1aB7cB2jW2H3TwerSlXe/MesRSNb3svfZ1lyNu0rnUcf/PxDTdcHCp2Pk+73676b/zHDWuHzcfkyW8azzHteP5stjPtY6YdvF/O2'
        b'3t5X+Fvnxt5lH3w094B63sKn1JMYzo9N1Nrop293Hrg5u/9X0Fmj/ax2MOaSvcGzuSt/3dFo+LPZiieFSeVlT6V+eNa09FzU38KKY2/+9OzI4Je//hT47JniJa8l+3Y8'
        b'tfj5GtPuxJ1PxpfeOhq0xMsw/S47x3LpEXakFu+Z11Dlsfqnzz4b+K30QN6HtWZj1XOcVDfu/+svK37Wc/c8MbLE/MOYZ/qFoV/ZNrsPHT3hGPQV/4svry/+8vuRsIqI'
        b'Mf00bi6BeoFToAfWvhiJlEl5LKUjkYITImI8OAIbpad1LBTsKSQqlnQ4TNRLEv7a0yoIR3DqudlWI9hPTsiH7QmhsBJsA5Wh03oKJTtWFjjDI+oUTbR6qyD89sveYhoV'
        b'7Je/JYMg3gPB1mWvMiEr1ad1KcHF5E4Kskx8FsZoW9sEqYOKsAhJSiNMQgFejiXKlNSSVTwRYR52atOQeXARXqJR6i2wVYOPsj8G908tVBmUAhxhzQe1oOJ7c3zOCNis'
        b'zrdBd7cudAMVEVxZtGbtI+Z7cBeLcoKnpWJ1wVZyM2mwCdaHijRnG+FWSmop0xK0ORCdG2heggoahrXKF4OZixlz5KOJ0sQMnC5F7WEbDPcwNIpRCfcyTYNQAfGxAFil'
        b'JcJxMyh4YA7hcZtI0mqk89awlw3LrWEP3BPKoiJhjTQ8x4wE/XOIrSE8Ci+BveiEWdn0KbAPTcAKoJyJwwXAPTQ9oQfN18OiqCW2USRqCagCw4RxoLE2ic7fOphBGZbK'
        b'yDETTUElydwRHgFNfMtgWLWKwCL2RkjjuCvHlUE3qwgcW0qrg3bCg5ahBAtHuWpQkvASkwV7LGgRqwoygH12DqGwN5INOiykKFk4yASt/kvJw0XDmjV8uHkVRvfLopaR'
        b'pORgFRNWyMOjtK6xZgU4iwoHTsB+a1ku7CZVoAAuslTBsQ2k9KiVh4JFesA1LBpzIaFExE8fNi7Fbciz4cpZWGItWxZonqXFgpvCwSBdL00OHLZNKBzgwgpU85dKZBSZ'
        b'SeCcHN2Sp4PgJg1tfgSDXhy1p88ihTKCOzYgyUQbhR6SN9wtSaloqGiwQIM06Cb1FgMvbQyNsAK7bEVRXWAVWuTogi0S4CQcgHtpFWY/I4tvA09JBoMueXQeRSlKsbzQ'
        b'2m8ruQ0LNoAudoh1WAHoDEJyyeeijnuRQWnHSQSGmBMtYAmoKNEHg3wuLuFlCgzLws2kv6BdwAmTUC5oh7WikEeSqN8dYHmAqo2k4pcsSefZgE545AV0PqheT1SkCd5Z'
        b'/GBLLhO1NqhggQMMUBkuQ+45dz6sh8NFqF4rJCkGWgheDMyjBbUW7PUJ1QYnXlAqr4UDdF2fQzI6hdSfH0SI+nAE9hCFI7wM9juFFkS9oCzNlyA1tRo9yDk22Bpsgeqh'
        b'IAwVSw4eYoILhelEBDhJ8BQOAhBuzaCcwGZZeyaoz00gN5VdJMm24VqilkKlxQHxZHKYOebgDJEPsAvsXsZD0tULq21tgumwO0qgkrUMbpGgy3wgADSxLWwKIhgLzdGy'
        b'tY0Bm8AxkfBIo80em4t6Ba6KkEgk+PUM2M8yJp1CEx4HB6eUu9KBElYMcN4O7iDHZEAdm29DHnKJBAvuYoDjqCoaSMUnp5SGaq6h3zRJUewQJmxzYJP61bA35IMDsDWM'
        b'C3tJuAjUWeSZoBm0JZFcgxh8frCJhCW3MAwjnxRsWTKgC/aSGlq/BtaVYKv3MCwpQzi2WjkaxPEN5y9JRLudQmxXq6bJBJcZuiXoCNkQG6OKEb0FQEPoYdoqVy2HiEHi'
        b'nGR6s4F2KwfwdiMQnCQtGVsaFGoDLqXODOnhLnr0CBl4nJ+gH4xLacug5OYz0UDU6UUCRKjPXsLHcS7oLgt3hYPdpMBqaACGdaB+LpkxkJhtnc+HVVw5cNYK9SU0mveG'
        b'wX5Yg3qGsoQlrFaiBeqCOwdlRI5iUNJJSjKBAXe7G9B4lk54dCX9BmCdCw7DAlsBDcYBu1DNdOFXkiWwT8JSn5JQYSwBQ6CV1GP+OriXT2KS2cE6BjhKwb1csIdcaA9b'
        b'l6M9DtxlwaTm4ThZR9FxOAz66Wz7XTeiQluElFoy8d0vSYP9TDdYU0S6+lJqFjavR1I6GIljwe0iUqPEZKXD43AbPZD2g8YiHhxKEQ0odCQreBLW0YOF4ho+mbPQIEtG'
        b'ybmggUVpgdMS9mB3Jl0jQ+CICj3QoxrZsx6JcyMS53Wr6JF2AO34ymGfSzo9pqFaQ52sHwkEHESTCH74JCROp/E0jA6lwm5mAsMabIogTccF54v5qLll4a5S9I8VuES2'
        b'gapwP6YL1YFzJAP5KLiDjo+FppXtJEIW6OSRBgmGp+Sn3ii0MsgbhSXryCjM3FDILkbzPwWPzWYZMbxBS7gokg48PpsP9+A+n8RUY8yWA3WkV89F8opFCFSAy2j9UkBO'
        b'UYAdLFM51O9xT3KHF0unA4cx8DKohw4c5rWCXgvUG2cQJqot3B2OWUdW3OBwNJaLQt+4ekiBY2hxQEbabHSrg+jkbDD0/FWKH8sTrTX2fO+AK7YC9G4ka6CXwneBC2Dz'
        b'dHgQSSoenpWxnQM30W+iGmXAUTY51bqAHolrTFVQLwXHVxWSp/BQg93oxmjh8XzAVYxlhUuC9u9pvFgTn6+0OoIr6mr+THBqHjxCA5p2g80cJDAo24IIFkBb8Sp4Cd0Z'
        b't1KqZRo/wh1u5U4NJM4sWV0eiW0CDnqBzdOhTcB2MGQlVn4S2yQP1tBrrp2rYdVU+cmNUAXtUoEDLHAiC1bRS5dNktyXwp7BikAS+SwPbift7GsezyaTI9xdxIKDDNAu'
        b'v4gMTwuXpbDh7qllUXCBDMWMhrtBFS3s5+DxKDTyh6Dm3Qd3suA51BvBYXiBCLtTKriIn14uJBz2gcZ4koMa2MZCff9s9vdYybwqQBacXcjmUhRDh4LbPRl0q2wL9OdH'
        b'wB5btJ4g47cO2Kq8nIUGqrOiAQ5V424T2GdlY8PEMzj6D01zKXHfY312hg+4xCbif3Qlk8swmJ1HqmEhGPLkoxEf7pKdeh5wGlSh7gurJeaqRJBuoMK1ZVvj55GD9ZSU'
        b'AVPVU5086Ar3SBI3NcLaEj3qSKQM7rMHYa05GTWU4anFfFtL2B3EJcNOjTS4yAxC816raJBMMId91hFYL2MGDlKS6xmwFu4Dm+jmOW8P68TC03SA7aTv0wFqqovpcWkv'
        b'WoCW82UdbEKKuaj7o0mJyQQHnKFoim3TxS+t4R7dfBzUWckCD2wKcJjlFiVaTK/ORN2gghhWoSkIVi8i3h0XEkjjw14FuC/UJlwKPcl+ZhnDAw7pkOqw8FGj3T7g+SLm'
        b'MoZ9BDxBr6m2o1VvFUaTES5Z7lwRmWyY4mr/74J9cH2/wvZOPASNVCFR4K/RfsWrDfoQeUe5ik2/o1xnR2LGHyi7p2M2ah4i1AkdVQvFrCvdBt1xbVuBtu2onbdQ26da'
        b'akJDp25FzYpxDSuBhlV7vFDDsZo1oaXXxG5gj2vZCLRsRm29hFrzqyUntHTHtIKbJdrYLexxjpOA49QdL+S4o7Qr/ldk8XGDZpM2XgtvVMsa/aJfpo1phrRnjNkED0mM'
        b'uwYLXINHuSHVEvcNOdXydw3NmksaN6IvapxmtTbDFkOhmn014xNVjbs6uvV+TaENoSJXkzShnkO3vUDPWajjUu07wZldE3xfR7fJssFyQkt7XMtSoGUp1LKaZDF1Nap9'
        b'H0lRRibN3i1S1cGfGRhXB0zM5rZ5tHgcn1cdNoFuFCZQs6sOuzcb3RvHHjm+QTjbRfzIhL7ZuL61QN+6PbUruyMb3aBJrkGu2aXNvcVdqGWLf8s0yDSrNyrhr6iOmv3a'
        b'QlpCxkzcul3GTPyGEoVa/hN6hvXSY1o+zd5twS3B7endyQIbb6GJjyjdT5Se2b1OYOMrNPG7r60/pj2/OaFZB/2Dg5fMF9jOn6QUtXWupF5bfnX5hJFJfeKYvgftXdOd'
        b'KeB6PKaY+gZXjDDFeoJj0ibbItueIOA4jnHmDUmNcYKumKHa8GUYoMowMB7Td22Oa1vYsrDbTGDqSq4cSh3JHs6e4Bi1SbRIiB0cM/UdShgzDb9SIuREoCy8DB4poxya'
        b'FjYsbDcT6NuN6UV2pw6u6FmBbm1y1eRKCbQSukSiFqkPHNNb2i4xbuEqsHBFX4eiRxYNL7rOuC1xQ+J63Hj4YkH4YmHQEqHn0kldxUCGziMDSlunSaFBobnk2MZu9ccU'
        b'wzyUMVWeBBzAaNzUU2DqObRcaBos5IQ8ZjHN/Rj3DU1xWJtxwzkCwzlDckJD30lJlrbOIxmcmVSD1ISefpNfgx+SJr0WvXEjB4GRg1DPcWL6hatAz26SktY36I4eXNiz'
        b'cIJjNsbJaHfq8ujwGOfNE/DmoZ9X7K+5XnW97nc77EbYeNhSQdjS0ZS00dS00bB0oW/GfXxJ9tQl8wW8+ejnlehriVcTr8fdTr6RPB6+TBC+bDQtczQ9czQ8S+ifTe4S'
        b'0m7fNadjTrfToEePx7ijn8DR70rslWWjjsFCXgh+bKkWqeYiLJDj5u4Cc3chx2PCxLJZboyTORodPx69WBC9eDw6Yyw6Q2ibKYjOuK7WzRiU7ZEdMhniX2EOce/Y+Y1G'
        b'ZwhsMycVpF0MJiXlUaXo4EpBsiuqlBfu4iowdxVy3FAb6xuQLoNb0KOd0SXZIdme3rWyY6XQwmNSVhJlJI8zkm2QxRmhekStPcZJRGcqdCggYcjqyRpKH8kdzh2fFymY'
        b'FzkaFT0aEzc6L17okiC0SETSZrSEcZ9nS9eY+xjP/RGLsrQb44Z3ew8G9gQO+Y2EDYeNe4QJPMKETuFj3OzR6Jjx6ARBdMJoYtJ4YpogMW08MUuQmPVudPaEt881jasa'
        b'IrFCApUk9E6elJbQN5hkSaGSKlM6Bod0m1UfU0gq2o26LDosJvSNnkuvfkB3Zm/+FckxvZjrAUjm9P2QzJkcU2rXGOP4dLsMevV4IYHi6UyuYLjZakxSbgaa1QHflzAo'
        b'Q9N6Jg4wVEjA8F7tqWO6thMuroPLe5YL9BzrIzoC71vb10dMmFm0LW9Z3q3SsrI+EMdUwgKe2rayZSWuu8CGQNwIuK8ad5l1mAk59vi3fIt8e0xXYkfimLX/kIKQE0Ak'
        b'Jqjdocu1wxV9GWKMSA1LDRWOrB5eLXQNIo+L2sTAZEw/pN2vXQb9M6Q27hYicAsZdQ55TMnoG6BGGI9aJIhaNGFk2qbdot2eKTBywk1hPGQ0whvm4YhiaATq1hCYzBkz'
        b'8RkKGDMJu5KJZMHdGMuCcZtMi8yEiWmbX4sfPeaMugSMcgPGuHHXnW673XAb4y4ZXbBEaLIUXWJELjEd59gJOHZIMFDfWtSz6ArjmsRViStx4/7xAv944fwEoXPipJJM'
        b'NBqSZlH6HDIINfvR1i70iKQyojOsg+tDrkUO9RanDqduiXG7+QK7+UKet5Djg241F0uqvkGTf4P/1IkOXW4dbuM8fwHP/7oDLtp46GJB6OJmOSFnySRLDtWUDmVsdky3'
        b'XXVUz3pML7DbaNCix2LIYcR92F3oEDihZzCu54iacExvGapn9jD7ivc1v6t+12eNB6cIglOEfqlC12XoLDwbNUU2RD6mUO3TfU/UdhOmvGNL24vHTGJQ3ZoPm18xxoPy'
        b'NdurtsK5MWMmuaMJieMJSYKEpNHkJePJWYLkrPHkFYLkFcKEXFJ7kywJe4NHcvi5AhoCpobAmLaklqRxU2eBqbOQ4zLBMaYnXUc0xqMRDLUjY0R2WBaNEWMmWe2FOMrX'
        b'uK23wNYb/URzRvbV7OuFOJLceGSqIDJ1dFnGaFrGaGSmMCDrPr5k+dQlvgJbX/QTdSjpG9KjUTHjUUmCqKTxqHRBVPpoRvZoZvZoVI4waDm5UXh7QVdpR2l34eDanrXj'
        b'cwIFcwKvs67PGp0TJrQNx+IS0BKAGsS9w50eTYUmXhMWNs1obswZjU8cj08RxKeMx2ePxWcLHXME8dnX49AQENwTPJR+xfGKz1DOHaeg0fhsgWMOGsTcjNEgRloP1UtI'
        b'Q4ioXl64i7uA5y408ZiqR31Sj4b0ysEZrRfG9DJpgUd1kn41HUmI+w338dB0QWi6MCBDODcTtyxq1TG9cNSmUj1S3QWDRT1FQz4jkcORQvRcduG44wY1BE1wbB5TbCPj'
        b'bvtBlx4XXIywlrAJC26XRIfEhJV1V2hH6ISd/aBEj0R3Qp88KpC1DZJVa/dxK3+Blf+VdKFV6JjVYtIvEwRRaGhLFkYtRsMr1xJ1Za4lGXXzhBaeqI+YmqEuYmo1ZhKA'
        b'yqTQozCUJbQLmFRnOxnjErg80qDMzNsSWxLbE4WmzpPaCmjwK2UEM8x1fqSCGdq6j1XQaPXIm0kZzn6UKUGp6IwrcwTKnGYVtOoIagmaUFOvC6wJROsr9NxCNSv8O7gm'
        b'uGFlY75QzUb0qz69OVlgYC9Uc5hKyGxeJzBwFKo54YSQmhC8+JFokKiPa0puSB7XtxHo25DVkV6TfIP8uBZXoMVtN263RyvBbrVB7R7tUa25jyk5bYMrzkNl5ItoVrrL'
        b'MUJrRm4Lt92vK6wjbNzKU2DlObRsqGDUyltg7HMlTWAcPGaccD17zDh1dFEqqlNTMywBoqpvj0WD5pQNlb/A2X/MeuF1tdt6N/TGgxcKghcKLRZNWPDGLGK6JQble+Tp'
        b'8QT9RFN2wtWE6/5wMRrvTc0mpaWxAMmiqpRWUNeYZKuazvqeUlVR/c6CUtGvj31X2WhCU6duTc2a/etGlWf/8thXgrLLYvzyOIVJOS1nEKfwMRPd1TI2X/F0VyvY0RZQ'
        b'sq+CdL1+D4CNiFJmrPkLv8UIr9cv+PWk0GVuFAF4/VRsx2DM+o76kxSvIiZhwWLy3JeKKKe4iIgIrgT6KEzFhDz5FwishU8oAjCL9Q3yD/ePJcxVAhqjEayN09xUXPLC'
        b'rbgW1Au3/ad2UURj+XoyqimuzVcgHilsCbaRgapxG/WdBFNBGXVJ4xjGhL7zhBFaP/C+k5U0weH7SJrnhNHsF9P8SZrhdFomSrOeMLKmz7OcPu/FtBCUZkbuMRel2U6n'
        b'Ob+QlkRfi9JsUNp8Bk7Us57QcJjQsP4uh+GspVge9CiPQSlqTDIZCvoYTarxCH97bIChpYmjvEjBgqS7uoYdscOqV/nfsxiKYYz7ASET3v4/stwVghiTkjjlkQT+/t0a'
        b'BqWmd1fZfELN73tJploAo9zvsQzJpyOjJ6B9ydW0G86C6DhB/ELBosWjIUtG/Zfe1dHvcByePZx21eTq6lG3qAl9R3SpojPqrgEM9ETBkT+xApkKOpMU+ZQmh/DXn2Ik'
        b'fFgKJj9Q+JPmqJIwuWcWw1YCUqVZIrLwhMSURwaT8lgkBXeD3bwZJmhs0b+T6RinqvpPcKqsdBnRd1mx73LoOztdnnxXQN8VRelKYt9FaNXDstPYVLXXYFNZr8Smqs9A'
        b'lupPY1M1XsKmam6j0rXOaP+7salndE5LiZXAYBqaqpApma77O7hUvRm41G1cw/eVCGU4pzAjrcgvY1lO0RPbl1ipYkf/BVCqKw3Ic+Ay35fwjYzxf5/l4+BTyMNjjDX+'
        b'sGX9cWKpK014cvhTmFPRRa5/HmU6dTsClLLHKNNCV0z4ZBHoaKEbJo/KxfiHR8b5E4SpyQv40Fg/v5iMgpkYO7tCd/zAf+RU+2nO51RBnmi9Ltdp+OfMMnNlZ+SB26Hw'
        b'N3GC6FTlFGIjyMJn+NDr7mFfGIif+n+b+5n9IveTSb1owCoZQVs8nkyB5+nIHyTqByiHhyzdLIhRXdY8OMgGW5IIyR/HIzgMWqNzVJStGXz8oiAzppAwQfcbVTBUT9hl'
        b'rrCzU1ObZZ/gkFqnlHn/bYp6N1TysuU1LoNoOlVhTam4wwoODr8VnFz9Mj+UBntqvdC7ZnJDsZIdc0PTXcWN9yd0OVOgfGXO/4Qm+tqbzpIWQ4mmuv4PUKKFoaz/a1Gh'
        b'WVzmJ0ZSfxQVmk7qB7MQsfv7v5MTOtX9/gkndKr7/tMzXP8wJ3TmiPA6TujrBpbfAXe+cpB49fl/gtP5IuiE9slPzcPu9JhX8hr6xvRlr4rO9BLbc0Y7i3ieeHKiGZ1o'
        b'grJ8PSjjn4E0p0ryZ1CaOZn/pWj+v0PRnOpxr4BI4j9/hGU5s9P+QZblKzvwf0mW/xaSpWREXDFGjsVZwJpXExPhPlgZRnuNBz1/cQ9G4M4ABTZsDYAjOe//OEzxMfvx'
        b'8LfvNb7lfKRlG0NqrvZctzV3NzvFmmeZJ5nzzUPN15o/XF5SbjXbVy7NPNBDNdk5VkOXJWXxuc0n23pi6xMcfRaE76ker5U//CVVulTh/LNwriR5vx8FW7J5NtZgD9wx'
        b'zS1006QD2dbAHSunwIVGMSJ0oQhbuF+Lhvk16eSILDZDwR4xk06weRVtW7MZ9HuTl7NwL6ik8NtZO3vaKq0DHNIWd/wtCxJBBxPluHL/A20AXj+8ktP38ipGHNIXQC+d'
        b'vl/lRqloVOc3FwmUnbuzhoquJFyPn3DxvuJy3RUj+uIZRO1dLXFAYULToG7tvrUvwO60Zv/nQHevfSItaXHK3UrX/xHlrjCZ9cJK/Y/S7bZxGRGFS+iABq8k271U8Cms'
        b'nQ8quBjWzvg1E+5LKDup33c4TJMWKyB7xgJTcuYCEy0vZUULTKaIU6eAOXWZbLLAlJ6xwJQhC0xpsQWmjNhSUnqDjGiB+ULqDEbd+lctMH+fUSe+uf5/AlA3k68uWrWJ'
        b'qG0r0TyH8Vn/Zdb9l1nH+S+z7r/Mun/OrLN67douF80b9IZrqiH+BMLud4aM/yTC7j8MXptFK8RywfnM0OeQdXgY7FKEB5bToHX8LgoeAjs9aMvw2CC4K9I6QQSzCoGV'
        b'2IknNBHDyGVKwGZwCXsE44CfsuD8shwCY/cBR+Dh5zB22LcAo52niWpdYHuxyET1vAthucF94AQDVmH7xbawYmcKe0RvwiAykQXvTCj6cyQ6kwL7YZMs3A+b4cV842Ib'
        b'CvO8BsDW57goWB5kRbuow/JwtE4PtgqeDzolqaXmMt65oKHYGhekEVTkhr6wfsfoKytYFU6cXqjFNjFsaVgJjswnLvHgDNw2H1aIMoyPSgTnllsnJGKCV0h4GOiICwKd'
        b'QeE21sHhKB9bJuhlO4CKmFjKABxWzJUOod15u+VgN4k57DqHgUMOgxaws5gYFB9M036eeQroiEpEmWMo1SqHQkyiIlw4CSoFVEiDWrSxOFpsiy7LgyPesVNnwnJwAVwi'
        b'bRZHXyXKT5JKypQGrXaraM/hHZ6wgl2oiKqSpQJa/Bie4BBop+MQVynBetgHB0v5mNI/ArfoMniGcJj4PLsoSODo1pz5hhlWTDMjKiezfhOD/wwd2ek/eWSfZxWhwOtd'
        b'3zifNyrX8k3LsdbPlJOvHpM5otqpHLL7w7zqgeSC8uR9jH3KWrON7u354dfLZWk3nwlU1KL8DNxqt9x8K+CM6xkT7vU7Q4oP+Ka3hZffdVp+Z5VpdeOag5eL3znmke3W'
        b'lr0UPPxWs7hrU75d7OPc2C9/K5FNOX9mbZqb/YGwXZIftZbNOXbF6eC2hRPFG3Ztjlt5a81be12EIzf1go+trwveKTfhfvCjSzd/yxuJ/PKXuxPFjp8mhZ04C2++/eH3'
        b'Xzz9/uuyt341Mt1gn2Hp6e4k523u/vat4ijLxw+fPrr/YGnl3jUHfu0cOv/rB2lyFiYjUfFP3ceVcyOiPwncljfKVabtbg9bZDwHO4FGJ9pJwofeJsEuL+Np8DuGOsEu'
        b'PuE6wR16xPjVNgl0EKyTajYTx/zthdtoD5xO2JKCN20iTzswqEGDl0r8aBv/dnVwXrT/SqfEoe9om0c7DqEtWyeonhYvSQpeMmLnMWGjHOijLXI3e4bQlrcUbMR7u1Wg'
        b'nTYE3gqabMTCHK+HHcT9Rz6fdkrcAneBrS87JS6BjbRXIjyuS5tYH4U1mvRD4B6+KyzXj0EpwgussHh4iQYnDcBuf1hBHAkk5sFzcC8DnAbbC8ju0wWczgx1CEF9v92e'
        b'AbsoOGgjcrJbD4cWPVe/gxOwnAG3Rs4mhbcK8+GFhNMtAnoXoOKrmrNgI2zMpttrAHaBat5z0D8cgqftXGELQS4t4IOjhLhEcEvgyMKXiEugx4Gr+G96A45f4XNmoI7E'
        b'oCiGL262XsU4KqQZ9d/5uf9ZxhFm7hjWbazZ+K6mBdkL+wp1/EbV/O6rGhDWEG1fdyVjzDGUHPYR6viOqvk+kqd0jTGoqFoaI3/wEU+hzrxRtXkTqjp17vvcm+dg29tu'
        b'k0GrHqtxBx+Bg8/YbB9i1Tx1nqbBuKa5QNP8XU0uSY8ejUsaj0sRoP/MU4Q6qaNqqSSvGvdRVUvRbr25qK2spazbf8zc7Z6B5SjP/7r0bfkb8gJenNAgflQrfkLfpCnp'
        b'UFJ7XNfCjoVDpmPWXuS0gOua2LpEwIsXGiSMaiXc1zUe17US6FqN6c7p1hjT9R5yqZa5rzv7kGdzQbXMZ5p69Uvb0wWavlcCryeMxiePLlk24Rc5Gr1wNCltksXQysCU'
        b'H5UM8cC8in+Em/PPbUqIKMxE5PwJUfDHegN3dPqzTdRPgXMZjGDGjxT+/JfUBv8bMJxMLvPJ4n8Kw3nVTvrfRMLhRBCWpQYYUnwFCudFDk6+xCtIOLOsydpIVgbsfA7C'
        b'Ad3UMl9PFpsyhmdY6QvgtmDQQ8/LlXLwLB9cXDMFkkTj9pxSsm6wRuNnN9wfIYsRN4RvA88HkEk5lc+k3nbA/P6UMEaeI42wQYe7szHCxgButcORzDHCxje6GMuRXyLc'
        b'BPejFraFjRKU7ZxwgiAxWA0GsB9iTQGeAqoosMugmH6PWgVPwyYe1xIO6oWjMRYTbODRXBoC0yMJm2mGjZKjJM2wGbChySlwJCs2RE+MX9MF2+iy1RuFYn6NATwawqJo'
        b'fs1GUEsDbLaAdngGrSLB2WVohYmBMwVrivH8oSGHI/RUEqQMOAl2iWFlZrmRirjgtZcKKp3HpOxSFHPnGdNYmKIEY+o6qxLXjk/d7Hg6MZcfROW6zWagXib3pjKTTvzU'
        b'Up66yLWnqKiUMB9ZZTpRTU+DSt6wFA3NKR43yuZRBGtkDdoZYAc8/wJXhqbKgHZwjF7pNYBtvpgdA5uzFVgUZscwykim6cukqHKGDs40t0pakhKRXiRBHRzkR4BO4n+J'
        b'fS9h3xpypEAmHnNeYAM8qsTExFpXOFJEQC/+qMLK2et8p0EvSiKE0WlwRBX22cMqAnuhSS+ZDBoOcygDnsUatGi0hK6josGODLoxay3AMDuJNwV7waQXBxMSwQleBjtQ'
        b'3dOoF7SCr2GIWC+5KjlfSj5l8ltRK89N/fHSgn9U3ItTu/VOWGbmg2Hhh3dLsqx52TmnLSzeWOS9rttSbvfYli02xyrV8wtqF/af/shiXpSU5vll8X5WlhZ3etSio5Rr'
        b'jNGfY5zd90f+euOIyf53fsm72NH5i+mN0tu/3Cr9+MFH47z8uWcdD2v/GAAEt5d/2vPFzYJ1KsdvV6RGnldce+Ka/ceVl5htmxK5380KObPr6ha7ssTNpW7flay3tYg+'
        b'cvJpyJbaL0dCc52/bZhYHSJfcr7qsXy0Lme5848/XvrFKdE/fstXb21/a7/1t/7Z0l9c/8qoyn5FlP6PBw9XPuk99vdDp26cveteH2Pq/IOav0JIutv+tIWJGfHjBzPi'
        b'az3b+Ty/B4xF+9crh5rM+6CsY2lore3jwq92TrqFzIbqVV79Zgmw1PMT5Xe6cxO25WpuylZYXhcSEvv+Bunu/JiHcS53Us0HjYvm+NlK7ems571RtqtzTv+brXqSe+oY'
        b'bx66eO9r3f6/1K65/M0nJXElNXmtlyTPMY+eeS/a7ZMJaeelb0SXOV/71SV7+4rm9x6i/7wPm1a98bXUXl23ATOXv6RED374zvzIid5xOdWPrcvzu0P7Pnzr5tcL1137'
        b'+/fmK2u7/jqgp1664DRldWLZ3OPL3j7/8aEfqPRvfhR+ej9ihcvoRtXiNTuSU3NbL7gOfKa3Uq/IsEjx/E3+uTddgm5+eC/E2eWnN09/+2TA4ReJyuhzgVX3TtjcvPLx'
        b'/p98vp9XpXPu49v2Lk1v8v6y5dsmac5ki97BYAWDLYuUWE5vUz9+tVrJtymwWe7mk1+Sfm2Yd9r0Gwtb7bU/R1cp5I0fL9mZMLy8U9quVe1e810DL91cXsVfirbVfWr/'
        b'6e3eHxq6TkUyR5ac+jXng+xtUsr9763I3pvlenDsJ730jZuPr+uqCuzpqT3U+GzryVPR731ubdj294T6tNMH1wnO3Gpyv1jx5rtOA+d3HpP+prlv7IcvK1cey+05fmhH'
        b'7rcZ5YpGT+TmJxV+eKZpXZVPk0JVwPAHVklGYOHG2AiD3sj6ye6+I0fCvvpBJyXvRppebf6CpC0/PN7f2VH72PrKZzcGjZ4o7lmj57deM+XvfKv4n5R+U/1pJ9X3zv15'
        b'zJLgAS/LjK+THqflNaWfNS/TviVlrxS7M4k684bTWKjxR16R2dZtzRrnpBcFautFCQ7H5H1UpbMw/XZ232z1LHdp97G2aoWfrGIa9z/Q9bjlenvOI/W3J79ZuOpo/iPb'
        b'+gcf9KndmFQ4k4W+/WR4e1Lh8rPIo8+0H9lWP9A9l/TZL88cHns90Op/z+DDxqXzi3+cVF7Fil/qI/mp82+8durrZ/XSZ6yXsj52ecP95KfrWZ8e2fHFoPLTWwk9I5Ud'
        b'K6D7u7/cOO/5xfLaj1mn57k2PKXOnWtYbP7JU5WJ0t4fz63d07nxrf6qjyvfebal98EPP711K2D907u9x089zorS3DuxkfH10V9rjx/45embgri9z26Fcvkf77vU6PyR'
        b'3UGHOTt+XtJzuOcJ6yuvutL4L8LCzKs3ZD8zt11rrBfZtj1Vffe3b29eKvjik1/eWCpz21tg/fcyQXDq2pqL3k3Gn+8x/2XENSD67R/LzN+yG/t2WU3h5xlc940TDY6/'
        b'3f5a21ivte+UQ4PbKeNnUueP/7Th/bJtH62vOnH5pOJT1s+tEh6xjtxVZNsCN4MeIzbcB/a+tHOhty054CLteNgLhmE9LwKcn+apEJiKBU3xMIbV4c95rlFLp1gq/uAw'
        b'2ZqBs7ANng2FGKQC9sDDYjAVLtxLtmbFqfliDJQwtEcSMVBy4XGywdGY6yJioMSjvQ3NQOGCLnpfN5AAO/n04mRemhgAxQF0EJ9nGQM0p9jYRM/DABRuiE1BMIYmTOFP'
        b'3ME2KdAHOlbTPq5181eI8CeOYJBB8CclgCaNyHFgrwhzEgIPMmjOCTyynlQSmg3B+VDQsXCKdUJAJ+AIoIEYoCncnR2HJvZp2AkhncATkeQZVkTxpzgoWXCTOOdEbSMp'
        b'V0YQrMaME9AM+vHeEFNOMsAQDTNIMWODfeDCNOgEY07gwTn0e88dYA/Y/ALnRBl0G65lFcGDZuS1qdx8eJiGnEhilQ+hnCz3pbes7TGgBvbNZJzA/ctwGENz0vywEdTk'
        b'8WdSTvI9YIURPEUfP03p4GeT5YJDVuKUE82NpPTRZcZs0O09TSohmJIBeJTmlFxiFvPXLZjGlOTDC/RTnUsFfS+DSmCzDQs08GbRgIudq4zxphjUgGaRXRrcCg8spTfa'
        b'mwPT2BHW8lxwXB0vO44z4FlYLyIO+MFaVFUVsJIQC3bDY2LUgrIUUoAitG7o31g8A4QyRUHxhJU0GOFMZBTfBhNQYsDl5xCU80Z092uCPaCJXQYbMAcFr6fhLi5GoTAo'
        b'AwkJ0IP+bieiYwiPJIZyw4kXubkY7mRnKRGdeaChGBNCeOAEOCbOO1ES9R14CO5z4UdwQT0Y4qKlE3GJN1WiX2gP+4BOtIY7KTeNPElJppvtkCE8HjqDd5KIcj8bCPqJ'
        b'zCyHFyhCPIHbrPCSGCNPVvqR51Yw8Q6dCTuJAi3qK6Y0OYMsGfYM2IkJGAQX0MKvg262bksdHtgPakXUE4I8YYBBcle+vTI7GDZMY08w8sSdlsMIuDeSh5rBJljHRxx3'
        b'0o7kEF8anwl3EtzJQniUIeKd6OmSArvAPu4U7YS/WFJEO1kOBuj6G4nfiGknsB4cFuGswfnZlnQTH3WFxzDvpDsUPyoNPEGLc1qbMw+22oSK8U6SwAnYBqrsSXm54ADY'
        b'z59JPIE9kaC5qIzc1iEAVGJH/kJnxjSrwAV0k2eB+yQkYR9oAXXPoSeDhjT+oBM2aBDqSaUT9jon2JNQ56nBbSXWbYN2veehCKNjifIrKww08tmq0+tuNJz0E/FLhtv0'
        b'aYXePrR9eY49MTKg9Uf9oN+JL0ZiiJsHToFesJvAM2ANHCyYQT6BfQ550+CTYj36rJ3GsFML1r2IPqGxJ3aglTaxqEAlqJoCn8CjoJZBg09AzUoizGhD1AR2hkrBYRH/'
        b'nGGbNZ8uZMP6YBH3BC3huyQI+QR1vxa6EbtgK6zlr4GDBH9Cs0/ALnCAbgdQbkXgJ3mw3wKDDzD8RM6MHkX6vf34q9FIJKKfEPIJ2JtKngpsh0dgDR/sIzgG1JGwJrof'
        b'PZQW7JbgucB6kv08MKLHhlVzxHccoNeLtMnqINgSaou2mnQQSIZ9JDhJBihD0M9mT+WI+4Ec2IeEJwCcQfvUzXRbn1KBe9gE5bBOUgJvS41RRtuJ+JSYqfDEWStgn7nS'
        b'8nUEQYO22FvRbIlm7BP0TCkrgq6wKH13CVAT60RX2U4kvTtExJXlaxgi4IrCBjJpLLBFW8O+mbAVOVAFLqNZ4xBpKis5HqgAzbCFUBcwbsUInqEL0MYCZ8V4K6iV2sHx'
        b'aeCKJzxBHmGOGewPtQ4B22LwbIhxK3AQdBKBVV29jL55sHmmGCElAC1HcL+TBSdjQ9PRbDoNSaEBKdqwjyakHAPnTaYQKaAJHgx/BSJlHs34WikDD/Kn6wkzKbbIBrCK'
        b'wEV4kX6YI/AUvASHN2CpDeXKwt3cYNH0rw02SwTOmkNq0xo2x8E+yxR8DhECaXiY6Q12hNNIl2KwCZUHD8WgHJ59TkNxCCTPGwK28MS02lilfVkDNqaKhq9Et2KsUEaS'
        b'v40olbFCeTMcIllbwXYmH90yEgnTXh4ajpXLYLs7ax0F6knBpJWdeaAJLdqqwtDqDOsaYANzLaxOJ3OgghzYxsehWXbh9SN+LAaloo4GiQrWelCz4ns7igQrGAh7NSLm'
        b'BTzMIthq66tKz+7lSAhrZxBWVOCAAuxmoTmu3oGeRs7BKme+OGypHXXaDiQH+4mAWFjDBnQ4Dxwncx6mfFnBc3Sv3ZMO+8mla1Wf86QO+9FBBnrBMTfeqwqJGTBgv0Em'
        b'qC8lpfQF++ChGRgbFXgOXoDHWeA4aJWnn2RAJ4WnD5peJMEQDExSAT1in4SH3dkW1sqzLTEZDWNg4CY035G17W7UpY+yc1DXncbBEBjM8SkmyyHQLs9G/Wwn7AhhUDQM'
        b'xtaRdEP7CLtpEgzcMxtUTJNg4IElZHnlm+nEBuc1pkgwoBXQ5B/dPNA/gwWjvBwchNUssDtEnZ6kdyxHw1uflY0rqKJpMGj6Xw93ERYMKv2wKnupB36JgVkw0rGkLgIX'
        b'w4a5eS/QYEQkGDnYKZq9wH64g9BgwClHBqHBlMF9NG9lLxhCi6YK0EDWfIQKI0LC1IfSw/xZuNcCjV1Lp7AwBAmjDhpIP1mPLRFpIgwaNIcYIiTMCbCZHq6r4Xa8KZhm'
        b'wuyFTY7TSJjLIq5kEjiuxBfnwcA6eAocgGf8SMWlg4tRIrRiMLikLcaEiaQjU0jOjqCJMCXs6XC/22AjaQ0pcNA11AJswUwYDIRxBCP0YNuUH4mGywVT5Bea+yIBL3I1'
        b'/sOgF0Kke+HPSx6fGi9q58X4LgZy9PuZOI9/je+iO6bl/hLKpVrykRTFMfo3sll4Ai2eUMv6z7BZXp34x7Asao2K/z4si+gmIg/w5ui2uJa4drPjyeiJcRqqg3YGcUIm'
        b'74hOKwn1XEWYh+aAtsiWSKGe058jozynbSg2KDaXtG1s2Thu7iUw97oiJzQPFWqF4RL9F3Py/3vMiSIuKRZ3DaGWBZYJhQYFsccXwTvEvOTjupI7ksetPQXWnkKLeThV'
        b'tkMWYwsCOwK7A05HourhWk5KSpqaTbKmPeFZbG2dyWiGEwahOBEQSu6/CkLJa8n7MyCUSUkWajWZf5kXEtIQ0lyIX/eOm3sLzL2vFF4ru1o2HrhQELiwPkSot0jUm3Fm'
        b'Ci0KuO6CWoJQUZI6ksat5wus549b+wus/YUmAfhYaEtoN3OQ3cMet/MV2PmO24UI7ELG7WIFdrGjcUuEdkuFJilT50kLTVwnpSVxlaL++EiZ0jf8I7wRfcOmpIakpqUN'
        b'S8f053T7dks/piTRI0ePLBxeKKqp+zxrzMDo8jrlhSTN3PpYfrfkmGnskP3InOE5VxyuuV91v+Z11UvoHjtmunI0ccF4YrIgMXl08dLxxdmCxdnji3MFi3PfTVw5Md/7'
        b'mtRVqSsF14quFl0PFwYuEs5PQhWPiyw5D4Nm/gsm+S+Y5H8KJlnImIu5JHOnsCSlDIwl2cD6vw1L8v9tGkkxi6aRxDynkdyy0+V72HxuolvEsPm30kheszYtlxZDkYR7'
        b'/Asokh8xigSrdwmKhIVRJI+wB4naf4IjwsdKo1chROgamMQ18CL14BNMYYl4BT7E6hX4EKtX4ENeTMuk06wn9P2nUSFBM/Kzfl0apoLYYSpININLqCAJNBWEpWAkooKg'
        b'b4/lCM2jfd7V2a9hgpiKMUHw9+8ippkgrpgJMvfPI0HwDWIY9/2DJ9y9fmJ5KWDLJ/yJbxODboO//+TDzGViGgj+pGkgHLzHhkfjCAykIBvusgoJtykIDoe7rRiUBRiR'
        b'XGnoM8MAR1H07+QTzAFRf5ECskhimqKBeRiqhJQhKyJoKM5IVZvxS+75rxxWJusMa4rLkW5KXISwgxB2GJIvVyhXLFcun1WulimfLiHG05BkUhlS6ZLbqHSpM9LTVA9p'
        b'kiqDUmXFUmVIqhxKZYulypJUeZSqIJYqR1IVUaqSWCqbpCqjVBWxVHmSOgulqoqlKpBUNZSqLpaqSFI1UKqmWKoSSdVCqdpiqcokVQel6oqlqpBUPZSqL5Y6i6QaoFRD'
        b'sVRVkspBqUZiqWrlkpmMdONtMovUybfZ6JtGOYVqnIXqW6pcppyN6lsJ1bcKqW8TdFyzjCmbxTV7X97XOzzOT2TM9ckA8wX3KuzfIH4GjSeZts4vyscx4Pn0Oc4OVvS/'
        b'jiRiOv7mNCOzKZsxvg3HW8xxSOQHQ7yfRd426GhRRiEJ6J5fklGIfs10/BEP7m7FyUhNy+YUZqwqzOBn5IllIeaZhB3hZuTwOtP/mZZrM35E5GOPj+BM9HTELK40ozCD'
        b'wy9etjKH+DDk5Ik5lROnCnQ4Ff1flF2YMfPmKzOKsvPTiZ8tKnN+bkkGsbErxnNEbhl2zpgRvZ7jn0P8HCy8uSL3vtyZ3h/YSULkP0Q3hK2oHaZq3Ipj4cOdOi2Vw8/A'
        b'fixFGb/XSLgNLXy52BM9VcxXSOSlk1+Yk5WTl5qLXaJFgChUBdjd+4UH5fNTs4gzfAbGCuRilzn66TnpGavQpMjn5NMFJw4/FqJjPljCVubzZ/p9pOWvXIndGInsveBc'
        b'FMFlvs9avTL3fam01JVFzk5prBeGO2JvuA591MrTPox1FOkc0mhAYhIfRnpQUkIdR7mckalIzCxZTGrXtD/iegliZskSM7OUEDOoZG2QEJlZvpA6w4MRj7j/FJExo8u9'
        b'3hnldf5JqB5o16QF4WEi3xrcCVJJvs9bGLUl8T9DHfjVTmsWGbTgva53/w66gTTCXOyBn5aKxocUVKQU2keIzmw6E3EhTc17tXtfenoO7VEmuu8MIcXiXFCcIero/GLU'
        b'A6cHmle7rM/wuyvNzkFX4H6aWlyUvzK1KCeNiPXKjMIskf/R7zi/F6L+uyo/Lx3XMN37Z/Tc3zeDlaZeNIM1iOBjFbTeO3v7BD/xfnmDe6qIe4M7UMF9r3czn8pZL9O6'
        b't4me8i3Rx6wCsA304XefPD+4hwvQyXAXFwyACi48CHoBfQlolYwiodHjiPGpUjxsBKdBDzgtSVEbqA2gBRwnppLf+DIJXMguM1i3coMfRc7mwh6wH/bDXaAPTQ3ulLss'
        b'aMr9+dmzZ5patH+KncszdhpaPhCPluxUuJ8OP3nA0Y5JSbox1I2iYK00l1mM33nAreAMiw93K6Ls2n1L6UhBYRE2spYWDMoBHpDiFcHD5Lag0S2PjVOZ4Qy4034ObIVb'
        b'UCYkxIVvPp1FKTwE60gecviDQRnPlTSGu5fT5r2H1AvYODlGB7+tOI+D9VTMRlnw0MGN8BxoE2VCFyLYsiACPSpvjWxwqA221kmA9TJ6obCXdtTZA0+tgn082MkUHZZx'
        b'ZuYlMbgsYrHpgt+eeIAzoRFwjzWscbRzZlLy65krYJNSMbFraosGHTKznh+WouQ3MHPBrjByOTjChOWgVeP5cQYlv5G5MhCcKbZAx32SseEz7WgUhM+JDnpuIQ03L2NQ'
        b'fkrSmoZ2ZBUIdsIu0Eq//IgGm2St4QB5+6EKqligyVKpOBCd5K8KmsStrC1M4UliLRWFcg4LDbVmFniCI3rwEtitDnthb6ga2B3KloO9oCIkJpbKyFSeA8/BLURq1kSK'
        b'5CAhWldxeTxVnIQSLTbCwzNuQOeOPb5sQ+It4K4guCcWu1mFxsNu3pTgEgPvyGDJWaZy+B2RpCQc9jcFHVzKvxScgkfV4JESsBfVOd6XGcB9vrBPaVUhDmyExAQOMcxA'
        b'dRptDVw5F7SwZQpLUjxR20swLEE73EOb6l4Glz1gn3xBIdgByWVnGCY5a4tFQZB6wAX+qghw1gRUSlAseUaKlwmRRnvlEH4B7JUPBpfwNZsYJrP5SJTwvVScC/lwAOVX'
        b'jjbtTHCRoQF3SxKh8QDVsIPcC9aCAdG9YKMGbeQ7CE+lgiMLX2xzN7ir2IXCFh09RF7odofl4dYhkfFB0yeLKtTADmyCfRRsymWDdlNwhHQycBbuAYemLpYGF6evp6jZ'
        b'ayXgAbANHiQhJY2kPWItQCMqJ2kdNB7JMlCb75fK+XHHXSbfHM2gQb9pvJP4Tp5wvvJHxfdc8+6dy9twSELR+q+RnBa5Fg2Gj56lop5ldMH89ii/Oo0BC5/w9pBzGupz'
        b'Ei8ZK243v85a5XtRoevqX9KvnS1JXllhWaO3LDLz8i+Zn3/ww5PQv/H4C5IrP/ju3SupN7IuaNwOurVn732w64Ot4OMLT0vaDn2aqJz3ntIj808HtIQ/q8Ra5Z1NPbFs'
        b'zDn6RCBHU/q4xSf9j9eFfPGp0nqO6rFr4QuNHWrDP6BmV/lJn3zwUbLiVyZXVybz2Tuu+5+r8+eY+f0tyeivu2/aNd2etfYymLAscig8tsXSJDHP6b3TyyPfOHDa/cO/'
        b'Sb+jV1IsPKn3ztmHXPMkt0oD/f62SevC92ST32u8+sTM+XGWojDv0PDsyLLe8Ece+e9v0v4xQT0wpL6/6o1vl33tf2Fi8Ucrv3P6qrf4zUOXd9SObprbddf/q6MMH5bb'
        b'2sc7nD9Y81ZCWEfPvC86a2/Patui/pGJwzuzBpLe26Pxyw2BptXTL06Nrsn9yH3bNwapF/Lrxo/FfLBH6WsHn1b+kycTF0O3fdNSrJjMvfb56vTKnSuCVq8qNfXfuf5b'
        b'86/lTON77wR/xnsmEXJ4+y8/PztpXfbBuTxrMNl3b+2Zv/vX3/0lpPCNPZtCbKl/FEzoLl+ePM/e81GZy6X+A19/2Sm/wfmN0s1Cm7qbZj5bwjPHBU9l33zvSBFTeiS5'
        b'nvn2Z2ukjm+O3bjc+EbWtsovktYoUkX3bgZ8scHmSUVs8+0VvMcbMgLmP9vo++zmKSvJmrSt3Zd6Pov5QDtihcHyRqooR9N/7e4n1RtPDmzfs/Havsi0h5btfUfbP9P/'
        b'buTjpoi4TRPN38ULuy4cDjtt9bFq2eA3Q3sSOJXed8/USmTt3XfzLzUGP8z7gpeyJPCIyvLRh97PjrbMzbwVpV/q+Ftb9DXF70YSpJdtnbvk0IZnrXNXmV9vZz1c7X4R'
        b'ZuXr5T3b9NYTP42/vr12ltWhRdzuh4HZK1svFD4uUf8/xH0HXJRXuv43M/SOoCC9wzCFMtJ7772JiKBSgh0RbNgbCiLYGERhsDEIyiAqYMVzkhUTk8wHmhmMScwm2WQ3'
        b'2UTTTN//OecbEJPs/97s7r3X5Dd85ZT3O+97+vM+50/j36Gfzp9KHP5q8stmZXfDor9VLoW3B2rtDfy+D43e4aKIOMRal5MtEcVs00l94+pGLryaotg0+kqAxY9NW9aK'
        b'3hyk/rw2xaPuHdF5uNv2es1E3Hc/tG2hbAdNvh7Q40Ywu8qdNaCFJ0xho5ZAyoK3IGplj4JT5CSQJXAHFIN60IcbQdQ0wn1sShdcZ4tQ993rC44RII4DG+zjJSRrovh1'
        b'rCpwJAS0bSApO8HdjgwwFYp1+Spgqg9DRmO0YAao98AAxFv58eqURjHbARzXJNEsYZs2agX2eqQlhmG3u81sd9ACJF9jN15WLWxB8TCkMVkI9qYRXCao84jno+ft7oRz'
        b'R5MqQuOH84HgJAPQPV8WVO7CIGynH1V4fCnJTQB7Y/GGNAZviQUalMYCtiNo3cBEPW0GtielCRL4GGWhCy6xCQ7yelIN41bZgtrxdgbdayucTByjewmUx4bp0WGdyvOy'
        b'HFye7noJGzQJWiDLDOyo8oAdqdO35XXgXrK77QAOL2S25RcTnA/ZlQfnwDVGdQdQF8FLAOfdYAOHRamVs+Bu0MElO/Y5YFcEhpakCOA+2DC5a4+SsIDH1SpBvynj1dkI'
        b'mrdMng6Wo4Pa4diqrx3J6MEEDqOSTkxJWgI6BXh3PVWVgBM8oh4Ejy8iuAVWIDxcBfcnYI0kGczkpgrgpSQ2ZROrBs4EghNk3z8BnJmdC89jROoBbVUA/Rg2Sv+iNpPZ'
        b'RdgDr6PcUgV81PUm6YCtk5nZeanBM7pI+1gfkcag6UV8QV8UhhdAGUG9OIJG2ApuwpOgPk2YmMJPSGFRBi9x/BNRceH36+CQGhgEPcxAQ4Ww0PfhaJqsIoXtAZssCRqn'
        b'AQOrWlE/RGlos/WKOaSoNKvzq9CwD3U811AHvZRVuwqeIQpcj6yzjTlKrQAOq0CFQDaXwYIcMUEdOTkeLGUKIFcODhCBzLRmk2O1EmEn3I1Bh+rwGAteBVtVEElYbwIb'
        b'dIVo9HYD3MSRz7FAR+QkJOOEUOs5eNAmhMAHp8CDcFsOg/o4iwplW9UUdg/ssEMfeAyeJEiz9QtCCPJvNoYxM8C/yMXEtJBO9THOa18y2G+igbJuY4FGPX8iVvpmcAp/'
        b'0gHeangDizXAAl3B8DRjkz2u4PTkIYGwPQoNUcB2yKDLoBRcT1dh2WtBawoGk15ls8A2cJaIk4JG7XuqJlGW9qDRDjZ7MPXoIAYMYr0+P15uBrjA0V4G62ckMomfXV2I'
        b'JR5E9q6C5WqBY2ywd14RKa+N8bB+mhuykfsLcH54bikxsSQwjMsRD+/AFQyG5MDLLHBhATjKyNEDroGzcBsSdGBqCKhBGZRwYjbD5q/5KEhyBNgP6tfWwEv6lc9Hk5hP'
        b'ywM2+griUwQoQlaMlsFiFY4MzWx6YWcVD1znomq/lsuiNDex54AWLmkonT0M0auW5NWM0WuWsr3BDhMizCqtleiDEzAMywaeSuNhBLs6NROeUzOGF4JV7Uc3VxdJAfas'
        b'VcUH59ghVirQqCaQgJ0myNZVqSAr1aQMUjnh4MRa5oxNCWwHw1WJsAHToA6yrAKNvOAJpuW4gkajx5lzsnRAMwV3bTYlfQYa9V6HPb8CSHGQ1s+DfUCKjBfH9tfjq47X'
        b'3AwuUejxVvQCw6NqfLyZs93YpqilK3b0iSN48BlLypGQSI4EcBbUoQpK2gePeLifQznCs+p+TmCIwUFtBefBUFUqV+XHkMSijKw5QXAwA+wKZgz0MJoZyVRHZ26EzRTS'
        b'+G4Um0CHd1quqMIFVQauq1McsIu1QQSaGFzc/tng3BJNXqIgSeCeiloWw3LOwlTUTJMGrFO7SiUfIxt24t/rkZoYpE5xF6iDttqUrwVMbayHA79nHYvQdx1I80Uj6iBw'
        b'QSMVTYdPMMZxGgyGEO91eFltEqePjGk/UWB41BJd/G7SNcUYXuWsNwDn4TC8wkDkukAHOM1D7Rnpg1D/pgWvsUEzsrg6RlsX1eE2Fa4LXIuf7CQYXNdB0Mm1/N9FUf3z'
        b'7Rtcx19Ylfi9XRxCmTZz+kLUiwxwx9UZiNWSSNRQ2ogXS3zum3CVFlYdLq0ucvuQoaqRqHGL+Oaox5OPgocWjTiOW8Q2RU3Mmi12FK85tKKJo7R1aFI7rKe0tuvIa83r'
        b'KGwtlIrGrT1kLNraW2HtT1v7D5mMW4cMLaKtI1BAHXxQzbzWeQzKCQUkz0zMFCYC2kQgN/FR+gZilIXCN4H2TRjljvtmy72zm6Lvmwof2wUp7QKUdlFPNdVmz2hSf6JD'
        b'Obh2WXZanrVuTmiKEpsqHVyak9DFrEdmNuIqSdQDMzelrSNGcChs59C2c2RZ920DlFy+OPp44iMbZ8liJKmNh5jzyN5NaiItG7f3EWtMmFs/MaQcPFAFtHSWOweOWwTJ'
        b'TYOUs606LFotmjRUoC2F4xzacU6T2n0jO6UzTxrRmd81v3O+wtmXdvbFTx2UTu5Sr84EhVMg7RSocAqjncLGnOaN+I7a3w5QROXQUTmKqHl01Dwc2H7CTiAt61vRvUIh'
        b'jMBQLbtIQrdn7YiREQprL9raa8x6nix3KKI/f6h2tIwOy6Z9chQ+82ifeUyROkoiWvM7FrQuYPaCFdYi2lrElD6KORQ74jWccCt1OFURnEIHpyiCM+ngTEVwDh2cowie'
        b'RwczqVg5SLxaEzpSW1MVVh60lYfCKpC2ClRYhdJWoQqrKNoqasxq1UjN6MLb6+9svr1ZETePjpuniCul40oVcUvpuKWKuFV03CqUlvYLEnnS1p7TJcKZPbZ3lbI6Z3fZ'
        b'dNoo7EW0vUhh70/b41cGShtb9Ef3bWvHphilpV1HYGtgR0hrSFM03t7WbtXGoLEx8yCpUx+3m9vH7+Yr3INo96ARtTs6t3XGzBIJf8HccZt8uXm+0t6ly+K0hVh9wtJG'
        b'XN2xuXXzuKVQZjxu6f3IQSj3eGncoUJuVfFEnXLgP9GgZs5uSTqY1CmSVHdt6NxwKow29T6ahKzBxumJEWXvipUy4eAh05BV9mszm9oKzzjaM07hmUx7Jo+WjDtkoTCG'
        b'RJ2yzO4lCmEYLQxTCGNpYaxCmEQLk0azx+0ycTqPLe0l9q0BHSHHQ5qi8C53TXMNQ+6gMHOnzdwVZh60mYdclDBmljAhEMmiMLhqMLk/ecTxjutt11GX2x7jgkyx2n1z'
        b'd6WlDS4fhaWAthRgbgY/pZWdwko4ZiWUOdBWcx5YCXEt2HJsy4QwaCjqVuxw7K2k4SQGozUWvECensVgIhTp+XR6viJ9AZ2+QF5cMi4sRRUljakQVtwnMyh3Ia6HLh9a'
        b'OnZGS2fJ2N0WfTbdNuNO/m9ZBvx/vkIWNmYWOSFE1W8wrz8PowZGRHf8bvuN+t4OGxdm4Y/g/ZOP8Biz8pB501Y+D6w88EdsOrZpgh8w5HjLZdgFw0oUgYl0YOJY4PzR'
        b'xW+W3S17s+JuxZsr7q6QL1g0zl+MpE9RSR+IpOd5YOldldbYvHQmTGarOMIVZjzajCdNvG/m98jGVe6WMm6TKjdPnTCzl7hIne6beSjtXbusO61P2bZqTFi7SjVkprJS'
        b'md596xClg5vEXKzxtq2zmDNh465qTVCD2LGudZ3C1pu29ZYF3rcNfceBN2r65uzXZsuz8xTZ88ey58v5heMOC+RWC5Q+/mI1AvEUdYV2ho6Zez/VpuxckMymFtPIMowZ'
        b'UEMbJp4/rvbfhzf8F90I7iae82b8dzuPBC0UFVM8/biVepYWyWKxbJ9R6AcjIWz/ABKiCq8+dmh4UH26gZx/iXez/L/i3XzxAyZJN8+jjKeRbnpNbpGSPUa+XWm50M4d'
        b'b38IPX1Ek/TEv+Xg/NclPs3+oxLLsMRn2ZMSW2KJVTtzdhUlL8j2L4vVzXqoVbSY2cL9Y9INYOn6p8rTnlDqER65MjuSICaG/LdlxCSrXNZD/aKprcyiij8o6BUsqNpU'
        b'MbpE2FWvqKisLv0dpsn/RIkiafWKJre2/rCww1hYgylh3XGpVq1BxUq2zaZ2zP5TAr+ELVP7D1vm9RfrkjBrJab5XlG2kjCA2i1ctLJ6zQus4f++pGVY0k7qj0p660VJ'
        b'LbNf5Lv+z4gl/cNiASzWuSmxLJ6LFZkQ9Z+pNavP/2GpXnmhsFb3Uf8OM7I9649mP4qzd2BNFopb9u9wpE+y5/5HLB9VVR1CCFqE6Tn/mLCv4f4Q92VbKXF2R9GxomkG'
        b'Rlg/mcbwP9WkaDFyrln5x6R848VGeraKS/Y/JNtLk43zooXLMNKhaOWq0hV/TED6xcbZHwuIU2E25pdNxwH9mqb4P9a5GEzJv3jZyqrSP/YB9/EHvEG98AE4mX/rA/73'
        b'Dgsq//VhQVNlNwVu4KRWdF1ap06WH1ZZ1auO/Xn37XqWiZpo1VkOFXSf/eGqa1wWWW+Jh6cMCYUjWYCE28FZ1SIkbDH8neN+HDFhm+mvRpzLSleoVitwGHzUz7JYFmVu'
        b'1bKxeaPcyOEPHu7zz7NQ4DqMWVXxwT5LY1n/wsk+/0dqK/u12qjfqE0tNbsifyFHjRwcGDPve6K3g80ifUrHxVbCNktTQad/q5Ma1u/MAhatXLlMpRQdlVJWE6X8QW38'
        b'fxJ/OF0dlf++OjB8DBvtVxuoSfgYUoiaCj6mVcdSkeAzADKqzlAFHmMjVU3R3W/iaL+giOlAMqQU9maOSlW/evrPVYUR7KIXVGWbSqAMGnDnSgxYgBdj9VSAhVVgmMB2'
        b'7OzVKS3KbbV+ePGyjc4bGZCPANSDwSqD1aECbRz8JEuY7kPAHQE8DO7Q4qHQeomVFhRhwYU3bUET2SkxCGfoRTGVb0MSukjF7L6Z6ZmCXDa1IFwTdIKOmdV40ZmN9z6T'
        b'yKJzHawHjXgzjNkJU6fcF6uDHnhKm+AptiStqlqVCltgO96XwBgMcHgTIaWDl2BfetKvvOllYCc4slhF6RcKDxnjXZykkAC84aQmYIHzuYvJF1qClkwe110vbpJVLxqe'
        b'I6mCS3AbOMZLFKCkbuLlaLw+b1jOKYV7gDSbADm4waCHh9d8BQlqlLYme1EIaATt8BJD5HbGeVVSAr8WdCeglNVYoAM2gqsM2KQX1OfiLU2uQIPSDmCzVoAz4fAqSdMA'
        b'Fc0tzLOzHFyZpNmBR8BFgsuwAVuR7q5owXpBKllC1ihkzwQDsJvgO2ZyXZNgY8ICcAwfjJIM60mpM0ypvBB1uB8eB1tfMF/dSfNdg81X5wXzfdF4J89t+M8a7m/OkdP9'
        b'jeEKUol1jlQj6zRfpU6FF/P/nLiFIkUshL0vVRHnfA44Co/DUyzQWGHEYGxgHRioIj7xHHAY7NNhgf2o/NvIy5Qca7zFAHY6TlOrFlIOIeY7viy4ijjlc5Z6WrBqwbYy'
        b'8hxI4ZnAKuzqz9ZiQYmhtf0WBpDWM4dKmqT7APvBaY/Fa4iyDExAM8PjTYhO4F7QwQJt1mA3kcEsHJwi7DWEukYb1LPAScyURHBhS+GOymkENkbwLOawmQlPCAlcrxpv'
        b'4mSB5hlZuK4DsT1lD86Ak1x1EtnOHA5PixwK6pnIR2KIWFDqZYLJZBgiGXgEl9pVcBm2kcg2LiGEwgZeBWcSppHYZNQwgLUza2AdT8WLA6/BQcKNA9tAH6kzeaBlCQ/l'
        b'K+S6pwhdkUSCxBQW5QB2qQc4hpHc3crBrUlCGngV7sSkNLAL3ohjSCnr4J4IFaHBXENk3lpsM9CUX82wFeWwJlkRYAe89BtmhDLzDFINAjPgaUKdkQwPgHPgOqr2uPEB'
        b'+0iNcclTX+oHmglfuY4vKvP63/JCGG2YlnQq2KYJm0JhO4Mgk64PJ0gw3ASZZbOK4RXYwYD1Gjng8rRWyHMFw+oB+tMZiONZsEuEGzpVKwcOZb7Y0CFJDxHTgDfA7nLS'
        b'XDGNVSTchtor+0imiFrBEZckhp7ZBn2emAVOLQfHmYgX4Rl8MpKKvNkKSlmo/dxRQyqLkSVL1WysBBKm5SiAMpKmBzyDwqE2hzQ48fAQxkT2RDLN2FnYBIdBdxYyZRbF'
        b'8sdMpPUMG6qdEO7mpQhQFVNbCLfDRtR4FuqSBD2NTJGJxQswL1MI7NcCR9m1SUBSjbfxqkAzEPOm6CjQqO3adEoKuANuJ6YGLoHtyVMkMbAuCfPEGEIJkJHiXLvWEjd2'
        b'qpYONgb/prHbCg9y2eQbAtetBvXwYo0axYJSCuKNua4gcwbb14QUWA+vL62C/RoYSYCeOOZXYyLXTCdLeAg9S4jiU3z9FaTb2y/UoUzDnTQpo+JlEWpLGXrSecao2Dzb'
        b'1NEYhJ8emcw8HElBHWS6Ogc1WHqzXN2Yh5op+mg486UmZjcdmuvLPDy2SZsyWoVjF+st8/V7cYDBmWwQMao3CbWfeK5RiIZHm1i1rHWsKjaLKqGOslpYLKpBTw01mOc5'
        b'ZMiNZsdkvMR+yBZ6PmTVVOFhlR0z13ioHVxeuqJ03arVoRuCf70Su6Z0dVERmnrglYKqUCG5J/Dl58+mYpdqI3ViXX2CB2vy6GJ6bpE8K3skA+SPOsF8dPc9GZptN5rB'
        b'qg5HF/lgD9yFwYfwADwkECagancL7kG9ZGJGuiA3/rk+p5QJBtg6LMJio1dctJHQ+BYJ4BXUfHMFcB8DJAGDYaSmWOWoIc0eBTcqVg1lc6pqUNk5/sh+kFew1CTCtH3i'
        b'nUfjc14/n3LsT8qly86YGhtrn0lMzzBudpjXu8/aMrA5dNlIUuv6r5yNTns8DHtc8HXYhjJR29jnCeJLN8V7Pvv83rNNHweVv3nPKWzGAW1n19NZy5s++ORzB/uDaxKP'
        b'Hxzp6uo7WOPecGXJziH7soT6ibHQNY/f3u5aYLRCfXjM+HBAzNBSV9b7asYrkvzBok7HoTx/G4NF60xn12veuSn/VsNZY0NCiR609yqJ3xlYFTzz+FP3D7QKwn1Oq0+c'
        b'3WG+apaN/2t2xlVlwjVnzeozPOtZK4WZeYp//O3nrZ9Kv3g43hGxznnxrZgN50pG2Zr9IoNXIxr06j37zD995ciCQ6NasnMR0Ts+Y4fHxqyJnzXLmX/bbHvVLw9XjH9+'
        b've6Js1PguYnxH9Wc30nZM/d0Vrow58rjVROefZ59rfb5B/s6f/q0rPYWe2Su7YH+ld+3Np5rjzUx/j6E1q1Ye/jMD4UjLrt8Pvn2terFre0K0Rd3v25tfzl3XMO7ZviI'
        b'v490688HeMVFEvbsN/Xf9zP6U0rJZ7P+ZvfXv18bPd6wV1xg4sW/WrDbx3v/m3vNXzuXvOGHnz7Lboxsf+/4txst9840q9ys+bQhTxB9ZMG7BR2rHlz9xut79dc91v3k'
        b'/96cDziL54muNMwWHatcmXwg5u/90u/3e33v/LpHxS+bFt8ZOPZULs54qyHuTw0BP/+l3a6hq8y9qeKIwfi6ss9OnzwRbPjGq9FZ9hfW1am9FzunyG6xx+uLXjsdf/Wr'
        b'xPcKflbuPWJ1Oa+jfX7U9b+r3Xlcu6sqKrWhIXDbsE/V2DurWhoOtymiHLtiY1MLhd6fJefVbtpS9uQXrS07XnLc5OD6yofmIcqi5Tk3Hp6r3pTz5p37m9TnfXHvkvJB'
        b'2r7+jwa+t9ne+uyrgxWjNbmnfy6/It9eqDhhUtF7kV85j3s47tpISf2CR4YRN4tWrtVMT7I5F8D+ZiTu+2Mbj17teRZ39P43x+tLvwi7YzEUZn6B13Xv2Q818cnfB9Xa'
        b'LZ756aYtl7744tGjbyWzTl28HiR9RbrvPGdJTOfcyIrBgV++is/N/ca7Z9OODT7sdz5/NvH+kq57BREza16//ulPKz6d+Ll8ZVzML++82jD65EDdX9Zd87mwcKjgNf4T'
        b'Q/3+gOblBQ4fx0bnfvitYLQq5xlI7hpKM7T7qujroCPrI6J/+fvjlr2j/zjtevjgBy+tfcW+6K7tj6L9Pv9gfzbTpyXuTW4Ag+a4bgcO4JEIkKKhhu88cJAFroPd/gRD'
        b'omUEOnUxG5W2G5oegAN2aChsDLo44Djct4pEr3Q003XH5HQYQQYPw0YtS3YuPKLiPWuDh9EIfTfq7gamGOjAIRuGkujKUicGK0aAYuA42MuynCdisB4nYOdcAufDWD6C'
        b'EUepSOA2JtmD4MQyBklGcGSo8UED+qtLGBaci0WwZ/qIbgAeQyO6ck/m7QFt0EW+KHltZbIHV4PSR+Fc4swZ8MrQQjbcAep/xUQ3BSVzBwwxGjgPDgqeI8nMvVEDd9qe'
        b'vPLKgVdUFHLOZQyObBG8xkBqGsBBE11C9cPOZqE5UkcovKFF4F7+qeAY3IOBgVP8iiblDH/VtVnw+hQPYj5oIVSI4Bq4vogpqWYwBNowtSDDK7gMw9NOCWEzWYSJhDK4'
        b'Yxp5YApowPyBQJIHB4hMul7gMqHF5IcnYmahXraoDBwhpRwBW8KTJllK4V4TQlTqD1pJwjVwEPZMciGiEfHgJBuiH2wjCafCbWqERlHLeZJFMUXFo1eNhqRHUSzMMop0'
        b'pBawGA3J+3XhEYYB9RDYDdt0p6gb0cRpO6ZvDHdiyuOWNrhaBfclJMDBJDY+EOe0ZiXbHUiBirTrMLyqpzvJkgePgbOYKS98C4Ni7UUjk2aMqqokaLWSWEonjw2u2qcx'
        b'+NM02KcLuleh91puWOpjLNiXC3YSnBbodvWdwmM5g0ZH0KRHvnRGlo1uYgpPA01hrq4Cl1lo5HQRNJLqY4PGSbvwNEVbmCTUiYMyPHYzB5fV/OCFuQSKh30bmvmwS0V3'
        b'NUWiZ4qG8/DQEhU0KSvVHTTA6y/Q3U1R3cH9eqRk3CxRbgNT3HCgBRwj/HCzwQ7G9IfA2SgVsRWoA/tUEFpfioHzXRMkMTx9CVCMB7XPqWWBJJN8TQrcWjaNrg9VxxOE'
        b'sg/cXAQOMki4dnVt3Wp9bVQr7eEFc1bEBrib4WTci8aqmLfRDV5CMzrYy6bUY1hwPxrA7yOFuHAOOKZLuE85cDAkiIX0uQecJXRX8Jy2aUxM1RS3K7w6k8FloqH4OYa5'
        b'EFzXYKgLfeFBosmNMRt1n1OHxa4gXGgdoE4FRK0Bx5GBMTxooBfsQJU4AkgZJrZd8JIr7F0xjRFtig4NHLNl2GYvesGLuirasqXrbcBFNlETH81hB6cTly0BsufcZbwl'
        b'5Ev5qElqJ8xllq4McRmQgB7GPPuQ8Q9hxyZkhOh7I/Q0k9j2aAKmYjw9CY8FYDI1hkkN3lyCZqPoKaPdfeAAvKwiP9YHp1QY87xaRruyQNAC6/mpqBWHB/gsUBdO6aL6'
        b'DC+AdsDwd8KTdhYkRAMX1sWrbSpHAS6w4akaSyL2Znh0OZ5zUqit7mSB+vJ0NB3Zx4C/r2WAXl4an3DhNiRp6sNblC68yYaDoBEw6FrMdAeO6LrDRg52CdNNmwM7bBmU'
        b'4o5KVCNRmW1C8/DpSGR4GtST5De5ofblBeA9vMAh2HvYO38z1/7/HpD33wFb2FO/pUT7DXiPGfjrPB/Ob+D+t0f+ZEW2EE0nviPj/K+j41kU30eiqXTmY3TaqQUSttLR'
        b'Vep9MlApEElilXzvzpjHqitJjNLdiwFSSTQfOzpLlpwMleUNLri4QMnzlvkOxfaH0bwoBS+W5sUqeEk0L0nBS6d56WO8Wnl2gXz+InnpUnr+Ujp7mSJ7JZ29UpG9hs5e'
        b'o8heS2evVWTX0tm1kmilK0+6pm999/oxV3+lf8hQjUxdqqHkixT8YJofPJQ7Ujq8gOYnK/h5ND9PwS+g+QUKfjHNL/6SogQFbHnJUkXJGrpkjbx64xOK2sKKZj9F3RDz'
        b'p5QVw36G/6Qzd+nMXS5zl8vcFTB3BWwJW+LTqa0UzJHlDpX1F9GCGIUgnhbEKwQptCBFIcikBZljgs3y3EL5ghJ5+XJ6wXI6d4Uit5LOrVTk1tC5NYrc9XTuekXuZjp3'
        b'M0rNt1OHpNZdNEmkFEULophExwSLR+Pk2fPupimSF9DJCxTJi+nkxapI7l4yl24PhXsE7R6BNOXpxxCmRNCeEShEQKe+0p2PnvNFfWm9aagI3fiY0uqcoSxT4RpKu4Y+'
        b'cA1Xunn0GXQbyNYMru9f/8At4ok6JQh+qkF5+Sv5Qun67hQl17PPuttawQ2iuUFIzL7C7kKFIIwWhCl5wj7/bn9VCgq3INotaMwtYmj1b588Uef4uHxFcfiuzzQoN0Fn'
        b'9am1X2py+H5PNCiR3xM9yjvga0sDLwdG6Cc2lF/oUPmoBh2aSvumKXyzaN8shW8u7Zur8C2gfQuQRv0i2PKiMnn5CnnlWrp8LV20TlG0kS7aiDRVzIrAmsJ/UHphtJ1I'
        b'6RuCFLVS4RtP+8YrfNNIotm0b7bCN4/2zVP4zqd950+GDcanEJXeTqODsxXBc+nguYrgAjq4QBFcTAdjWwqJwbYkX1Ylr9lIL9tIl9QqSrbQJVueMWaksiYJW+7oT9sF'
        b'PEalZ9ttq+CG0txQBTeS5kaOcTNGyu8svb1UojHhyJWW9S09t3RCFDBEIGkjNaNltzePi3Ll+YW0qFASKVnXmfzYVYh52iRqSr8ghrhJ4ZdM+yWP+ZXI0zPlWYvp9BKc'
        b'oYi2m4M0xGhHIYimBdFjgsxR9qjvXZ1JM/PqK8JmFkELIp4/IhRemPdM9Ujo3beke0nfyu6VY8LkkRkjcbct0Ru/Tl0ceEr/Y4KUEe+RstuBqliTvG7BNC8YPZrTqYWD'
        b'53fn9y3oXqAK4yHq29C9oW9L9xb0wL9T77FPMIb0DRb1Fyl8EmifhDGfktE8hjyviE4pUqSU0Cno4yShtJ03NkWbbhuJhtLTmzEV1AAxwjMVJo4WxCkEybQgWaIz4ShQ'
        b'OrlI1nemKJz8aSf/IQtFQAIdkDAekHTfKVnp4cNQaMXe94iVxL0Y0uyW1bCVIiCJDkgaD0h54JT6hEN5xuGjrIVz+ub3zkfN3QvhZ2KStanUHzglo/DCwPc9fWSLhmb3'
        b'Lx/3jFZJy8iv4IbQ3BD0FX4huNINbu7fPOZXODpDnjyfTiicUqSjs9zFd9zRb2ga4FKeXjgWXPjEiPLwkntF0MJIhTCeFsaPmowLUyRx77sLpOU9/CHjMffAyXq9+r5b'
        b'4FMOxRMyb8bdA5E1SSs7NyhcA2jXgPuuQSOao6zbOorwTDo88354NvrKSFYCa9T4tsVonjwn9+48uVuoVFPG6taRxQ1F9CdOoLTW9gQPeY3xgpWiwMGg/qCBEGk0ulSI'
        b'YmhRjEKUOCZKVIZEyNgy336d913dpX6namWVqN0ezhoxwwlfK5KnZ4yFZKAWa4jVr6PwjKQ9I+97Ro+ayTMy71ooEgrohIL7CYVKL/8h436LodVjXhEjeaMZt+cpYvLo'
        b'mLz7MfkTYdE0WYoajy4eDyuWsuU81NQEP3YT4s+W+xXg0n1OdKYq3K85LG4RViTPu0/YLURto7tXH6+bh28U7iG0e8iYe96I2R3L25aKiEw6IlMRkUdH5JFwCvdA2j1Q'
        b'4R5Gu4dJNCcc3bvLlQHhI65y/0RUTTfRTj7vu/nJ/eNpt7TRSPQjUX/s6SdRP62vdOGd1n1axEHd6feEOmlHvHqxB2tUO9MC/XnoFKuL/qiONXuovWZdSemahRXLqh5q'
        b'Fq1Zt2hhVem/A9dUHXA2fZTAbJ8mqlPUHxgdcPAiYCCK+MNW6llUPIvFssNHndn9gX3Vr/AyaJsGj+rR9eVwOWRhdi7sTY5ewJwJoToQAl4zZzzZr7yknaRySmRQAIng'
        b'KI9FWYBTaqCeyiLLzAVL4B40tjuAxqQJArAPOzGCS/ASTsw2SA0ehgO+XDazITKEpvgo5JoXMisDfYRUIMIXDL2YGRiGl6ZyK1lPjjGFJ8AhNx6ePe1Gs/zzbvEpwoSU'
        b'jFXYAyUjnmxGpPBZVPFMLacssK+aOI3sACpn7LWwd7qj90zQTCgcwDZ4DexLgvsFaF6fTZLygqfAcZ+MeJWcgU4a2HnoALP3KgNt8BA+MoIPd4UJiZNmHiOA27Qt1fng'
        b'mJYhOORMtlRAqwEaar9YSGgOcXGqkILheZI4F26LrfpVWjmqY2nx1+0vQJ/Cosq2aIGToL6QWGzFp9kD6lVRHIpi9Stv5L2zdDzd9JZrytVLKWGK6qV5g4Ev77d3cHD3'
        b'3m2ormliqxZTcmq7Yvta+Z6SZGs/iYM4sfnGJ+HffvL2k/yfFv9UFJxQNXD40VCPyTN5Q9XnX6y9mbYi9Mi7Cl/tpijv+SVO3yucNSeW7zFqWQUumf5sch+uapyd8HPl'
        b'd2t8DPht90Ui7inZQGTdic6Hex4W/2y4qtWoy3FFxaDRXf3qxk3Ba/U++Md77D/zfR4lrToXPvSnV2fcuri9eemca7vT9ut9OlqY8cHRjtNZKT+FGCz17v27JevWsG/s'
        b'/V+2vTcsfm+4aVD4kXxreu3DlPgAx/N57/aZrTYDx49HLYvafiLrw4Fo36YB8x/e/mFjaEMPp8JquY+Bn8nLRwKe6ufrawUvawwR7GoXxpsHvdrua7c/6q0MC8Ge3Ban'
        b'Ot2D/msuDNS/+u7pZ9nOb2UdGdE8cV769KqG32fefquyzrtcvv1ZXlZv7q6cDo4gb4vJz857P7sY/VbGVxbnH0QunVHm9+mnP6eu2vyk9+cT5RNHRMqDp/p+MfvT0lcb'
        b'ykfL5hwqf/zJpydd3r2U96zs+m6/T1/fuHwl3bP+xOb21Fuid7oPfz7UfnjY5Y11uj9+d3a1nst3P65obzvpceqXewvXvpe46DOd9pWrC4/rDsY3/i2oMPojTctt75Ys'
        b'nWH7lrP3K2vThvKTH3yVYbW+fbDox0NvOWU8SK4pACf9f6bv//ld/yNZlVl7rXcOFzzOevTZ0jczvp0Zur1A3Gvo8fUbuqZLynYPbJLMevMp+7xtaWTDKykrvjl5Yfaj'
        b'tg9H5n0fdO7Gxo93cmU6hy6/cu4Nq4rFb7h1vFXc2paapEyNk5h5vh9jX2Oy5Pij5bI3fZ3yHya/+klvePEb1lu/0vv4zyu+vPedwUj14Gj9uZkh1Ebrqpe+ObpL7auK'
        b'bxzmeL+TtzhzcEIhj/z62/Q7C6/YuJzZ+PIvXIVU9OONz47KTBI/y8hMevuk47WSH3Xb+ZohObNmVv75wYn6d+a/9lnlwdcr1D7J7HWs3KjkeTX+pcIq+1lI6nrN98J9'
        b'zUMez3r7YPR7Sa++/IwVu+f7hyDoYEFlz/Uf/iQRLJhwNGjY98menfs1C8JX7NXMCpn34OlrZcV/dZr1Xi0/9FORFfux2b1Puj//x+d//XDm90fXs4Z/8Zh1V+/bti+4'
        b'nsS1LQscjvmVY5tn4nPHx+duj7BD5fcYNN8dO1HCHtDHLONhR0vMDcGsNnbCw7p4hVbdmFmjZYHrJuqMU9t+eHHOcxc/uNeK8fLLAJdnk0WS5aip68ALqeDyejeVXzQ8'
        b'PZM5j/Y63AkO/uo82izfKUdQcAvsIXP0LaBt5tQqViI8A4cnl7HWwGNf4+5o6Sa4OymNuwWvjtWwItQ3MktmErCvrAqJdb2UWTZzzF/LkOfvQG38mUnnY7wBju4bgDgf'
        b'Hx8Bj6iBSz6Tp8D0ANkiXXcec4AP+jhdE3aoHdxhAc4za6rnYxbZw0HsV17JZVHqa1nweMBsJvdOcCS5issC7Ssw6IUCw0GZzGLUTtidXqU65Ag7meqsZcPhWtBjALuZ'
        b'RK9FgsEqrrZoHfYTJb6PqATJh4LWzfN0hRE8pEF2HiuoVoeJcPElKKlKZZnCbapFKtCuosgH1wMziYPsBXj8BSdZcMWAWdU5HaGDj13aBy7jFp0cu7NdC/aQ1ShwCSlJ'
        b'itfllqeQApi2LAev8ZgV4A5wKnENuKZa2lMt65kDGXNmSj16f3E6XX0yaw28pHJrPA2ukjS04GHQ+HzhSTOJnQPP2usjKXBJZsKeRR6JuioXVrzOlu7LrBntWQ52VeHz'
        b'zmGLOXZA5YBuFuqoTnszr/dugMfxWvr+ld541ZsDLrFAK7wBWolZxYIz8ICuMGU1DgG614AbIShvY1POEtCkxnzaUbAPHsVLsky5aemzLcDWkpA1zLpTAzJr6a8PnbIs'
        b'RckOQOnXuEsEh1AtuvAiTQI4kDfJlPACSwLsUGPqVF0s3Pd8jZisEJ9ECV2NR4kS9+pToGkZ3A4bVGvFkyvFFeAWo9Fb4Bro0k1MEYFmZlmYBZpXgwPkpTbo58M2sCNp'
        b'0jMbnxyGjy3CYyZUN09W/Q7JhBrYDntnwUuqdVzU95+G9UngvLEXrtNpLLgVHIE7SPo8TSgjp1k1VD8/zOoIuMHQD8yCu54fwQb3UtWwgbA0wDNLyUEkDnxQN40TgBxR'
        b'cAgOo3pnXqrmgBowMcnEOSAb+/gyAxwtf7YW2LUI1MEjpHLDMwZooFaf9sJwDF5BZcGibM3V4DlwAzQzh4YNo//aGbtFNoDPvNFJZgcvAE3w8gySVgYYxr73mDgH7J0O'
        b'OoM3wXXPeRomsAmKv+biUjmY6vyrRje6WNXoTnMmvlVMTCe7HAlBhlRI771kWAUOaFIG8zhesIfztQsZv6LGuAMP/Qrgtl/l7g7r1NE4dS9sZmppExpZnsPppRXBE3Av'
        b'NjSSHIdjPxNeJg2xQQE8NhuIGX4NFbkGrBP9jy5fav1PL1/+ikOWmZnYsX/Pd4zMTMgaZSuauXxP1iifrItlUTYOHYUnCptiiLPmGQuxutLeDTP+n7IRa2AH0LDWMIWl'
        b'B23pIfMdswxAs+rWaKW1w3PfWFnumHWQ0tGpNfpD7NQZN+r8psddD0XiAhr977Fg3KFIblX0WOTPEPUrRAm0KGFMVDGa++Y8NDWe+9J4SoVYQ27rQZt7TvC8ZM6D3H7u'
        b'oLBfOOJ8h3ubOxpLR2aN87LleQU0r0CsIV5Hm7spuUJmOU3BDae54WPc3JHYO4m3E0drxqNzUZiaVgOlUIRp98eEUUNrxgTlSCjBXYEicT6dOF9eXEYnlqFgG2hz9wke'
        b'Xn6wHLa8ZTNsowhIpgOwJykvazInB9cuQadA4eBNO3grHPxoB78xh8whn1shwyGKoBQ6KEURlEkHZYo1J7i+srUjauPcmDFu/ugsefpcOiFfJQvPsy+gO+D54s4YL3VE'
        b'/Y72be07BrcNVDk9tnPuMug0YDjOkRK4QmapI5jmBo9xM0c0sH/tqO94eKYqURSecKJ70naeYvUJWyepusx00LbfdswtXOnkjs+lkK4dd/ITxyjdPVCcta2GSAuDof2h'
        b'ClE8LYpXiFJpUapClEGLMhSiXFqUO6mGx8gSkAEg9dviJZQxW7/h2Md2Lji75yIqmQdM/swjhZ0/bef/qxeBtF2gwi6MtgvDL/Q69boMOw2Zw0DG7JKG1DE7/S2DYQOF'
        b'fxLtn/REW93fRhyLV3Cs5jwzWMWazf+Gwr9PSjiUs3tXameqwimAdgoQa0+4cKXOfYJugcI9mHYPHnNPvc0ZSYAG4y5pYt3HlrYKS58xS58JV5405tTGMdcY2dKRiP6V'
        b'rfFPNSg3vjSBYd1W8KNofpSCH0fz4xT8ZJqfPMZfJMduuIV0eqEifRGdvmjcdbE4/n1Lx8fCObI8vKI3b2T2HZvbNoqIHDoiRxExj46YJ46V+LWmKQUiWWz3gjFBwdD6'
        b'W5uHNyvCcumwXEVYAR1WgEL4tqZOOLpLA2XracekkVj0I46e4PKl+T022Cd+wgkVqucTDts5ROkfPMpTCryeqqObxz5B5K845okWJfAVx5xImbC2k8xuWyCtHLP2/NDJ'
        b'rdtCacdFEd2jWBNePrLSAUsl3w/FQfePgyKYi68otnM0qzUGfb4D730nkXxO9BOK5ZzHuhstz8h9LUkZnvSUg++VaTnMBcpPgxJ44/yYmj3uEC+3isdntzh1rG9dr7AV'
        b'0bYiWeID2zD0zJWvcPGjXfzGXMKHfMRxSluXjk2tmxS2XuO2XkoPkUT9tJ7SJ1yift/O+3FA+C3bYVtFQAodkDK69s1NdzepiPr9F+EAPkpH966QzhCFow/t6DNkilcH'
        b'accopbuwz73bXZY3WNhfqPCJo9H/7vGSKKUwULq4b1n3MloYPZR7XxgtZU94eMu8e9c+8g6Vh2WNe2fL+dlPdChPb4VH+JhHOH4r6lk3ZH+u9pFvpDyqYNx3vtxzvlLg'
        b'oRCE0oLQoUpaEDGSfafodtGYIFvJn/M4KPxW6HCoIiiNDkp7KyijO0kaLXNWesyRbhoxkGfmjoXnKuMS7my8vVGelUfHzZWpDxr0G6CGxzP6iToVnMlChc4VPrGnPGJY'
        b'qG/zCJIH5YwLc+VuuY9tHI/rflmFdMJ/yqFseN8TWvWd+frztFkTM/zQL7OuZcQA+pPVf4Pq/1c7FKPfrGv9N/qPdyZ9j/Eq1lrsGGCJfY8tse+x5R9xEfgGZ3QeO6aZ'
        b'r96Cr7fin2345wf083BmEWZdXbyGWTwrwhSrFSvKiVv06u34pw17KjlyUFBNldPsQ73pnqkPdad5fq4W4tB1ON6P+Gcv/jFgYYzflNPZQ02VX9dDvelOVA/1X3BJIj4s'
        b'xHWCFBN35v/eBibexv0dyvhJrbWqIa29QEbth5W1CYn6HWaM19M3emJFOXPlevZ/1jdtde7kiC27S/ujhk2Hq29nDS2960Nn5tFzC+QZ8+kFi+iSCnrJcvniFXL/lXLB'
        b'qvv6lc/YRSz9gGcU/sUk76tZT8iTp9GcSdL2OEzansCqi0bmbuEwYSRQmnqhRxaiukT0xMx2wshdaeqHnpgF1MWhJ1ZOE0YeStNg9MQqtC4ZPbF0nDASKk3D0RPLSFZd'
        b'EnqkSjsapx3LpK16hNM2FZEnJpYTRi5KU0/0xMS7Lup5mAgcJoqJZm43YcRTmoaiR+bhrDrcEcy2nzDiMynNFtUlPJfSA0vpNV3KVCxlOouIae08YeTJPLJGj1K+1mLp'
        b'O36twdK3eqZRwNF3ekbh3yfkl2GbJYcMboMDaLb2It8O2OuChuWzoVStVG3hC5jWKXJb7DN3RJP4MGE6ckrlNKNdpjnlz6T2P+fPpEf92p+pPLU6BV0bQkmeyHOOt6+X'
        b'jwgMAtmaNatrKqur0ExCBi9h/ws0g7kMBwy19HQMtPV1wQFQBxrgQXgkKx02w5ZcdXwM3LBpuq4u3OlGFpHheQ1wleBe63ke8EAo6OShiW09hzKBJzjwanE0QfSXwB5L'
        b'jPX1AkfhHsprLbxRjWcU1aAHdJHwPNDuBw9wwPbVKGIfimgML5CYoAk0zBSh7/AuAH2UNzhZWk1mD93zQRuTKTiOpvGTUXGeMeAqiVoE2sA2EarxItBQSYngjiCyKM42'
        b'FqIssbAcFmVaBo86ozigEZ6vxnVyrshBpEFRc9AU+AT6PT2LCMqCN7GUJENzuBvHnYFyq0cx4e4QkluuPxgQIVvwQQW2m/Kxg50M6WkXqPdXfWKbF47IpkxNULx5nhsM'
        b'FodwRah38PWLo3y1lzG+OT2gHh5RFecAlKhisFCMVC2SEexeFCFCjagfmkHdoPyS4VUm4oUIcFkloiboRIWxEU3XhlG8BeAwE1GSZCJCFuoPtgrRzzbQxPAXB6kz8mk6'
        b'onzgMXASxdFEU2GCI7oFbqBp6AC6DNDgUQHwvJCUvz1oMFMJeQE0E407qDSHIuwkcechAZvAANJdILi1kQp0g3vJ/gBoAbtTeIzKUINsAjs1iN4wnJHJtB6powXjqyNB'
        b'Tw0VCY/OYDYWrsLroJ9ki2I7YgWAZnccs8mhGre3YKeoGsPBo3LYVFQ+6GeyOwd74RWscpxlZzBlqgU6sAag1JW4ucDLoDkZdedUNKYCpKLBYdhAdLcxFxxhShTW27J5'
        b'HpqLKBNSoqbGpEA3oZl4P/b9i4EHEqgYX3CdwPv19Sp5jLWAdnAKRZvB6C9oIbEweKECSKuQ2mMDwFEq1ryM1CNwuXKl6suQSZ/QZxLgqMo0EBwgOcbAfWB7FVJ+HDJy'
        b'Ki4C7iA7QmAXPEowhfWoTEErqsYX4UVwHdkA6MIfehIcYyrTBRd4sQqZQDy4vB799OgR05nFyWbUUWXJRAyeVOU5MEwK1mMGquTYCBJ8fKkEz02kUoA98IK3SuYNmdiA'
        b'FqlqIFLSkKr2wgPWmBqQSnRBFT/RfQOzO7MHNtROliz63F2w32Oy1cB1CuyHBxkPpMNgAAXGNNxJC2ZSSagpusG4pLSDY+AWkXoHvIhrfj0Uq6GoS2yICbkVYo5BpNNk'
        b'eAqepJJNQRcj8xGwzVclMzw9E30ziU206qzJ5Hl9EVL7AAvzCdYhy0+Bu9cwznjn4c1Exo7g6SASNZjRLDxUS1QbErUODiDNplaWUKmoFovJph4cgoOzJ78We82g+nly'
        b'UjdGSDCcaw7YCy7AAaTaNNgAuqg0IK5lnEU6zOAelT3xNO0pE/sFRDeefPKhWrA1GQ4glaaDFgf00wdkpJXTjAaHmCiRuI45uxPFwIYtRNCwYnAUO6RlpIObVAbcX8sU'
        b'TjPYFcpY0TZsCFjGE3AYHMENQgrjKtZuAdt0kT4zE8EtKhOeAieZsjmBpG4l+iBRkQWVZjG2cNGJmIJxAOjXZeOF/utwK5UFG1IZ092Pcm2a1Aj6E65qm1WmEAV2kugR'
        b'oD5XF+kzGwzB81S2Buwl7RBnFaibMiR4YHOwKi5RaJkFkXk9asQu6rJwGctgC5UTBy8xTfMhcNyAhAc7ViNFgj3gOhb4Cqgj8bxBI7iui9SZC/fC7VRuBGwl8Vb6YFgg'
        b'E3Eb6XRAN1HJTF1SuFlzwU1dDnYZuw46qLyaaIZPvde8mueBI6Gxlx/o08BZHYFSpk1oX7deFylxrjXYR831hLeI4ZSilnXrZMGcx9mdJJWalGsF6GM0MrgMXAb16Crf'
        b'2InKh02wg1TZsrIoUI8UNW/JDGpeAmpZcT6zHMA1UI+0UCAspArCYSNJIjE2FR5Sx06H3bAN/d6CbUztbQAHk+EhDnaj6jehPOZlbDBISSnArnn2szQoe08u01wfdWbB'
        b'QyhRXh4YpLC0h8lzL7g1KgsVuzMYgE3odxsyTZxsVTbcBw+hr/WEF0spT3A8kvmQTigBN4lfEj9Tn+LDfRZE5pwI0JuFpHMBstWUSxm4ytUh7XoyOAAlPNJuZMDdpGxQ'
        b'dcSdeeBSoqeETXGMmqC0lve84wWnUJUjNnu01oTpStQycWVmyhYbXSToJTv1hRxHoma2HRopLDTEse1hO6mW5ZXYlxW/NSsnVWYR0xQYZxO7hAfAJdim0h2QrOFpwu2T'
        b'rSrsD2d67BvgxGZGALiNCA/7s0hzshd0kBC6NsjySJeA6tRW0kIuUiViEUIKIZSNqhOTSw2qGbi6q+xjlRbTfFzz1ZscFUThz1sAj6K3VmA7l8VU+kFUjjuT4F4+3BuP'
        b'D8AFB1GX3sdG9fgc7PiYjCebVodzdYhHF0uPTd0zxlfF/KdmRoyb10l1fUqyFo3v0ouXDS6eyzx8JVub+s7XAU9Yl6mZ2DIPNxfNoEbLknH02qpAO+ZhQr46tdUcTZXC'
        b'i/X+rh3GPKzxNqT8lwUgIynW21/OYR72RGlS/pWoNtkV8x2WJjEPgxYaUaOlsRS1qjh5+9zlzMOFM3QpO2MPijIq5r8Zmco8PGcwkyqpTscZBWsk6TIPP3JVp+45M7mn'
        b'ivxUaWYio8/Hw+hiPeVL6RRx1P3CfBZ1T1iAcw823hJCcdnZseRFo7k6pbQwJklouC1nQt8J1qB+KrHAofUsdd2oj4+14n93w0gG5ms1qMMC8pa/MVBEfSwi/74KIyYP'
        b'riRi3z0kw8rVptTK6FpSb7z04DYeqjbrUJvZQq2rAocYl1ls68XRcSoz0I+cbmubwRCjN44ZVac7H+dntS42jfnK+RkzKdMKUh61/LmqMv45ay5lWlzCQnqz0Clajr4y'
        b'NbXC+vXt7Co+bggafHYdvltlGWP6p2sFB8+/frRk/Zx5y3hvsBcmzGWrxY9utz7qr520aFX8YbWvc+Y39Kxu6gbSBR3+e4+5zzJ7xVlx/PitOl7eue/Mvkw5EJthH5Ht'
        b'c+uvH93ou7X5nVPvlf8jXZ67qae46aEi3jHqjeKj9xzi/pJhVy92/DjD4TVpk670YP2TUYvai40aE9H184H38Hbf9Vo9Hy60mlDM/9itsf+ZVbvrgQ/Uv4y5Hn3T+26D'
        b'yYcJ1yNv7lOMKir31XJWHlz5/pzvfd+1f++V2V/y33V88/3g9Syzu8/6Yy98MHZz8+mnrNCX474zb+nfxhvat/Q7tY7Qe2FjuZY+c60vab627dhP1uLvbhS8X7tk9WZ5'
        b'qLzy065vJdYlLo5NC/9y78PvPnhzxvKW1hMNQ6+vX7ps38Au7hu7V7ad/UfUQfDxpljnFcs0FIoHHmerdv99dqzVwpf3b17AbW1O7gg95ev7NOZRkPnnr3/U61leUzDR'
        b'+5po71+u/o1f6eI6Ubxi7MDp0tzk087DoT/qf3N/f+77ifPeTzr36Rvv3R/NukGV1tM6tQZJvnv3FzaeX9/+tOrgkeF4+o2kmy31GxosLyxKMmy49/bBe0mVH1/KvLH7'
        b'8O7zMdzkr/ZZpp3wGjBvP8i+8u299oqXDcTjKdWv538L6iteyVd/kH2F/5Hk6/fKIy57O66Mbaa7h04ciQv68dWcwIDOfYfPbC+4sOgISN+Ut+fWprzZD9Yc/tHjzNt0'
        b'ftyBQvMcWdO9xgdvVF3mvXz50C7rd6Uh74jmdQ50rT317MRLb/19/GPtd/TPZaXWnF7W09v1bMuPW84Chyu9rjn511d+8oVH119fKa8IWfZwXqPFWy1LHqf97XH7/YN9'
        b'f3rr9O7XX4oLsbaBu88P/OPyeIVsJu+t0+9e4+rndSz58+2P5p/aE1ureNS6tqaxas3+xe8N3Tv7icSr1PXewbJDNnGhf8u8s/u1twwb93lUt3yRxa3M+uL7rBDTrg3y'
        b'9+d994HS+sn6U1eOBb/eUVA4cP7qWajz9lGpxOeVIl7++3kmGypi36a1rm76xXDC+emOj7itiUf/dGuivaU3+WPen50/eJbS8qzsp+ELIGz8p4twS7zJhcD2pB5bozjl'
        b'W8/cB39WO95v7H/QgmvI7McOVDDUESnJaeqUei1sgDIWPL0ijuyC62tGwHo7U4aKWC2ehfrK86CFceppcEZTNtiImn8H/SR8IrsubOOwYZ8BQ0TcgobnB+CAuTNKfBBN'
        b'KDg6LK/Qdcxu6jkdOMTzBbthI+hNVKfUSljguj9sYwTqgTtnYVp61MYcSOAnqFG6NWzY5r+B2QsFR9OnPJi00rG7NHt9GrzCpCvJgT08zDoAGz2QQGrVLLh3Pjg0eb78'
        b'UQFPCPerU2xdcAkMsHLRdH8rA0nohmfiYb09uPjcg4kF+tFwlXHTANtdizBxAabnF7inqlN6Gmx4g8OQ/WuB6yuT4NG1xFMCZWrGAidDHQnfszOQuKJPYVFs1pYaVgQH'
        b'9BJRNgehDhOHTgDnKUrDHx7zYc/eXEGKNRUMbmTo/OdjMMMUo3+hA9fp/97n4V9YZMQzqt/3knjRWULlKFG1eOGKoorlC8tLN0y7JruMH6kx3DRrUljUzEhWXcwTtpG5'
        b'gdLIUpz1hIOvHATSKuZqTtiICbl6TN6q4yvyllyRt/jqiQZlbIXeazLXjkIUQnXtE85CgciNFhNIm7kmgVTXTCByo8ME0mWuSSDVNROI3OgxgfSZaxzoqeqaCURuDJhA'
        b'hsw1SUl1zQQiN0ZMIGPmmgRSXTOByM0MJpAJc00Cqa6ZQOTGlAk0k7kmgVTXTCByM4sJZMZck0CqayYQuTEngZ7OZq49RSMmSms7adWLf760NcLnez51UDFUdwV1Bt03'
        b'8VDOsmxZ0rxEYnJoZRNHOWNmC6+ZJ14sdcbbM0288Rk+dVFKK1t8bvDelLqYJl/lTPOWguaCQ4V1se8bmzblikuaC8eNHesiH1l4NGng1WJbcY1kYes6qYZ0dbc2besl'
        b'85ItHnLoL1PMDmmKUFpYNUVNWDtIfNrni1lKc0vC2OortZfGdLvKIrp5tKPvA3O/JxzKxv1Dnr/YUGnnIFZXOrqKtSbsXTqrpKJT62T2nbVv2c8RRygdnCULO13EUe/b'
        b'CpU8obRSZtxd1e3fqfWYJ5RoKW0dJC8d2yLzH1o3JorDe6z4uPCM04YoKApi5yxZdEpbmtFpcFr7iRnl4IOKzonbbSzxF2spze3w+ePHDZWOPGmUNFMSgrK3degUSdad'
        b'CpF5044+47a+YjX8NhrlGSuLlvnIHQNwIFelldPXGhTK261teXeVzL9n01AV7RFJ20SJOcwn+Jza8Ja9NxLflY+yXydz7Nw85hoy5DjmGj1iIo6R2B+LR9/vIHpsa9+x'
        b'tnWtpLptM8rL3Folkp1Dl2anplT9lAEqGAcnsabSmYvSTBFHK10EMlbnUnGc0sFRHKV0cFG6uUvUlS7uXRWdFTLdoaxxlwgJR+noIjU+6ad04ipd3SVqSjeedFG3Fg7H'
        b'lUZ0lks4Ey7u0ur+qqE5A+vHPMJHsked5ekZd11vF8pz88di8pXuHjL7bq4kSskT4X3wIbWhnBHRkOHojHFeMuObVHVyo9JNoOR7yaK7kyUx+CKyO1ES81SfQm//Wdrj'
        b'MfmoGjkLHvGEo+qji0dX39UZ98i6qzPiJVPHp6cPRVw2GNWhPRgMQT7Ny0dKdnTDbL8y5yGtfo/7jpFKnqfMROYgDexfMxQ3sEnOi1Y4Rcudop+4Uo6uX2pSzt5fhlH8'
        b'gC+1KYvQJ5qUpeeTDWgOZ/c9euWZzcKrfdRrxubJbkbMXp3OQ07F8vI/tE1HmLyKX2xdVx/DCPNpzeq1SQg5Pvy4KoXFYhl/SaGfP7Lv9g6K/sLJjjhjsrxPuI00f3Wy'
        b'oxY5dJbhN6LKdKZOdNT4T57o+OJ+w2/P9LNK/X1ut2IsMZvhdqtTK2P/b7C7cX4jnXoqmeps1yGH//m/qV/M/2x2IXO+IGjJBn14vpznpiL6cotPyIrHo4kE0AmuqFN+'
        b'GzXc4CmwtWL9BzVqVX4ojqHhhrZX52Biv11ebXu3dcZfPeRV38zi9O4ea9BzvufZb3r2QfqRlIYTerf1bI4eF1BpBlqCxjgumwxWikEzoTVCc/3rQR5o7KMRzDbTTCUo'
        b'KX/3MBXW1IQ7iTadwpqGFXHZ0+wRd+GTvbzu4pdKFy8tqlhRUrpug20RPvu0CFPMPndzmBaA9P341D3c97+UjurJzKbKgz6qg9cPJzyycJG7TtL6m5k3aU1jrVN/yKr4'
        b'vWqDF7iZ2sFUjJO4YvxXgszUec5h9015Oqothn+komxGMRkup/oQ0JjET8VIRTVKwwJcBK1sHTRYbmEWh+GREh48mMqm2MaszESk8jRiDxGJHGwPdomaxcsWsPIoLoss'
        b'zTrFJiYlp6YKhBrUFl+tNHYVkKWQ8EfSdSkUIP6cWTG/19iGIVwsOd4xujFLf1Ulh2Lnsqi/95HVgB0V5MTA9JmJxckBxj7UMnyIeusWtWVstie2Ub0J855wT6oKj2nz'
        b'9nhm5VR/s5ZDcdQ5gOVcUE1ya6vFLHaUll1kMf8kO5rxctEIbP2AfSoc04vpftBBwnWmaeINQP9a12I9zY1VTDi+4i8fqI8MYFo/g1mHqjAJUNnedz74iE3Fn6ZcKPOA'
        b'Z8RJZ+emnVk5+jX6qzzY2ShxAeuw8/4qrN3ZTlyCgay37nbDPtwm/ZwPXY+Q9YcqXKTO9XvHDe/y7yaoU4dmaLLY3s7+JN/KCd44Nb8RGQrFZX9BHq26UTau1ltJUe6U'
        b'e3EQebTnTzfqWY9Rg1FIFXpmEOmkbVX1NEXRutSfqV2DkDxLe2BZT6tRYzzqA2r3LweZPaGGlDmwPoFw6ojUKHAV9GiBenYiuAykFcE/3qOqnqF0Xx2gqrNT0t4ONzpR'
        b'+PbTHxydXLRtI3IMV4VLW2zOtW+I+Fnz+NCBpr/FW+m5ux0LsbM/st8/59wPjo9sJyZSfL2UNR/uKH/35vqvyi5uGSv6vmjdxMa7K532lZ9hRehmBReKE7iSb8Qn343O'
        b'28V9VbI/fDgq3vODv2j/YnOMo7dkuLGWJXi9t+Eh3+m1Ievzm/Y3pXXX/FKUvdL0/OpDjo+LDcw9brKzE9ks976YrXdf67213eDzPW83Rup45p89/s4nb3WWLt6dEfcP'
        b'7i6bj3v+Ovqh6cKyALdjO2zk1FevBHxqce3eqhP5jnO/an8twSrgw3UVAX/+fIPpF3+riNGB6ltyPv5Zp7Vf1mAd+P311OSMTV/m7I+6sO/trEWarx9edKD62P2ziXTO'
        b'ruz691YXrb6jvbol8HLDtZ8lOw///b2bgYvfStBcGj5x8fZoFd+tOrHqc+vU3mP5Px7v6Hn8819WLKk/W2Lw0cKwbzMeJbDCPjv7Rd6tyo5/mG3anPruD3/9i2TWe+sN'
        b'wq69c/uvb1jfO/r4RtqGRy/Pdi749uWAoXddPmcZPtpd//a2+sCXP239Il13xkeVmh/Ypw42bBI7Hr9x+/ia4sbB8cu/1L7keOzdtzvKLw30CNdpxn6x4sgF9/0Fu1ae'
        b'PbA8+tCOl7NGN9qv+HDmnb7HpqHwxLrHFQuqclh979nsWLrO6O5XW/72w88rjnd+DrhGjC/AEQ48msTF/kYalEZ5IGxluxunMxPatkVkMsjQdOWiqWYTeyWU1JKGuQie'
        b'C6+BlzDSOoWPOjEvFuiF7XYEFWwNT2AGGNwrwP2Yogke1tQCnezNpWj2bocCWMCTBVVramr0DUCjIQfcMIQX9SrVqVmwnQNOgD5mbQC0gRtzQsA+3vR5OpTBwyoykW54'
        b'DtangF5MILCTBU/CQ3FwVxQRzgwOLOYlqqbEGpkUbGeb+sBDJFknsNUfHgZ7k6bPmOFNeIxMgH2hFNShybYqT7h1jrYuGxzyBEcZipkW0MtBMbkCDFTWKE7XYzuGg+3M'
        b'0sF12A4lDPcJYT5x8GKL4KHJ04K2oi+7gFOuS0gGB5egrkwX9LPhCT/YTqK7gV21SQkpTGFDMajTKmSXwibVcXSwOTo8iTn4CPeBcC+4wjZbnc4U1CDcySWEdslcpMOg'
        b'SChjm6LueA/X7P8A7VuFxf0nmF7VLPt5T7dh2jXpaW+xmQ6uLJ2lpj8bzV9nzq6LURqayA1t8fkaG5o3SJzGzVyb1PDdxuaNEr9xM16T2oSZncT00JYmtfeNZ4udJOr3'
        b'jV2kDkpT85aE5gTxoo6K1oq2pVIvWbbCJ5b2iW1KGDeNa2IpTUybMpsWNvmI48ZMHCdMbSXsw2moD8fHjhxa16T2aLaVOEOiJqnu1BufLWjSmJhlL7Hvcu10lbrJYscd'
        b'gsZnBaPZ4iwzMUcc0aouXty0DN2azBI7HwyWREgWS+07S6VRMlZ3jCRVVjrmFKS0sG+KUlpYS3RoC/cmTaX57A7NVk2JpnTWuLlnk7rSxFzsdTBgwspVyurT7NaUcWTL'
        b'aM/Ikdhxt6Rxq+SmGKWFLZo2mlniOd082tZD5kTb+raqPbay74ySap5Kpq08m2ImLNB0sKuss0yaJXMed/EftwhAkUzMlJZodizOFvs1RePDa9a0BUg50tJuXdpyTlM0'
        b'Hs3EN8eLsyXRrQX3TblKOyfJmk7dpoim0qaypoSpwY7S0rY5+jFKKUciEgczp6uMW3qMWfrIvFG6ZnbMRNXOnkzOONKKbsOhWeN24eiZpZ3E+1ig0sm5K7YzVjpHNnPc'
        b'yW/InnYKEscoHVyZiZqLKxE8WyYad/HDczQnSZbUuDNHKpIEy3zGHP3xdG1ygvZEG01mkIE4u0hQMUuSUTpO3K6UzhSZy5DTuFPY798ndybLzMedAtGdkXGLZrPmYe1n'
        b'+SxqhuvTeSzKyHTKjl40r1+ZnqGp3NAOPRPnNGHWaKWJWV3Ss3KcitzY5YcqfWTIt6k4vwQR5+7/I+/Lw6I6sr5vL0Cz7/vWbEKzbyIgoAgisqqA4E6ziiIgNIILCi4I'
        b'iNKISjeINKjQgAuICu5J1cQkk5kMLSSib5JJTGaSyUxmNJuZZJavqm5304AmOq/zvH98+tA0devWrVvLqbP8zjkBakvDNGhuUOchu4Qv2PiQncMX8B9q5ucKNggKBIUv'
        b'581L4JSqOVZoDvIyEa2m9pKJlly0wjlVcjGz6PQdEq2cXoZjTERtZjNVZAWloJJD0YIKCRurhkQqKo+lDBPLfmVhYmdFEFd2QCUUtdxSBxu5liuBND4ZO1YQex2iokZg'
        b'hAX3gr0ZBStMY9WILrAiTb/912EdNfVdLV0tfS1bdT/dNEfdl5MnuftxggaVFMP+KsuSni7WzJHHopKShuni6ZsiY9P/JJQMs4w4HdrGFSQdWo60YMI4eEwnWEU+UC+9'
        b'gvGvI88BwRJBPFNFTriOZ3n6o9IUUsGP1dT3+SvQRNu+zBzjk/T/dI5nicuz55iVVGBiaMcg09drYaScvs8O4wmca8yy8PVP9S/pYVAxb7Hz7GQvNH1l06evbNb0yePD'
        b'PylC06drLhSIUt/TcZw9d1dfdO5ukbmb9pwM1bnbgufO4tXMXR6eO5Z87hg0xDKP/V+YvVnqBLVZs6eVRELDMtJ3y2VOcBkIsdyJZM5ReyKUecbYM3exqcrHxTvKf1j5'
        b'VggpXG5A5M3M/exMz/oMC9r+eqqIwlqJzGEBf0HHSic6HDQ8Dw+uSIHtQdicQcH9FDilBVpJ/QOIp0UEc+F3HpmFX4VmUARsEo7YtMYUL3jCI3Ypi1KvBMdXMRnwmGvB'
        b'8r/+kSo7iWpse2dl+6/9O7pa5soVFevOJeh0eC6c+xvRphUW6VHl4IvVtUYrRYW6UVrjm+ZI4/KWDhaGRnll60Y18xrczbJrRP0Wc4Rtq3us7npu87w69L5v2pCfb87W'
        b'rObsqApNp7HPHO/apUhWfTBapZF64EPv75NWCtdxxqu7Xjvxxr4+/0P6KedaQjqGarcafrr6aoRwj+U+y+Bx6kKvg/nFn3gcmjc/D+pAt4eXW6wXaAWdTMRvtjG97DYR'
        b'ZnGbFeiaYtw5LomYcRckEwa3Ihr0E0ADYtyTcdD0GjPYiBjozbSDJDgJrutPmbhKwAVs4gL7aP9LE8QdD4IBwlnD+lJwk4FTSDsy5a6CvuDOWo9dvnQaT7mZCl6Fx2kO'
        b'tnOOhkcssSix5zFALXqDC/AERW7cBpp1VeP3MXRBExhKSOBpvMiRiPej3JJD724dTCJLcvI24PN2x7S/yN7uoeSmHEyaLVpDm0NbwuqiHxjYinI6N4s3S13H7fzHDQLq'
        b'Ij8zMBNuFbmMG3AlhjIDp7rISWNTVNHI+DNzWxEfcwrNbCFD6DdpYNKq3ayN+KdIccZ9G0+Zjad0+biNz4SB79calLHJYw6la9iUUJ/QmDSpY9AUXx8v4kgCxfoTOm6T'
        b'xvZC/9Z5zfNaw5rDJOwxY0+J4J6xZ1004SpUCI5G6R/wu7F/NgAIGQs5d0DTnbcw3Zk2BGtUyM7TspcmOxiYNm3Pa8p/f4O9CI7rtlK51GpGDrWamcNYzWJS6dQgC/3o'
        b'oB+NPOY55oBc91lHEV0sQX5jfWweJ4e1n6MgNKvZTCpXLYe9n8pRO6c+ICdzq9VJqQYq5aiUapBSTVSqpVLKIaXaqFRHpVSTlOqiUj2VUi1Sqo9KDVRKtUmpISo1UinV'
        b'IaXGqNREpVSXlJqiUjOVUj1Sao5KLVRK9UmpJSq1Uik1QKOBtb7W+zmrDUkNuwJE7nINFWNyhnGEsdoQ1cK6bE1E0G1QTaPttogM2z/USOQXYYePH720VIWvlMXLIrlb'
        b'6EtckiTGe9p1HoOcY9POEU0FES9BH8c5KukBlJNF+AFN5Ymi/ipPlB/3Tesh/re0qEBQwC8s2JFbRnI1TXurgqIyAXZo8daadV9oCb+Uv4WLV30oF+fPwd+4gmIun25i'
        b'WXQMN6+gMNd71p2zVvj0U80uqdyDwikowCgcIlRtWSySv72oZSvl8VHAeVjn6c2gljA05sFB2FruR2GMMehbA1rgAe2SrSnouqJyKmebbkkqrEvEVnlPRLOzuRwdWAf6'
        b'6WDlNxNilNHdGVEJYAD2wU5yrEYJCj1w5Oym+ERErT34UMzcaQV7ae3fIS7s94hLpNN6e+iAIwzK2JUF29VBOwnkHgva/eL945gUowregRcpOAJb3elw9+IogLXuCQyK'
        b'CYS7shh+G8EIHWteYgBOxXvHJapXkhzw2sVMKIbDbgTYtxBcB/vgIZxzHB0uODLkoQScJx52shaBxrl0r27lgevx8CSsBedjUd9wI/pOrAw0XmdpUF4jHCDe7FjXgd/K'
        b'0AuMMHcagm4a3HwCSrTjlya6o8tMdHwdALfBISZ65FF1uoN7123DmQYWg16cbIBONMAAV+iYP4d2LFCJ5MvIgzdAO3rgPhrrfnuTqzylAzjps57hAzps6Qk44ghbp7I2'
        b'MEpKQHflchonO4LOYSHte8/JIZkX6LQLZ1cS3XbaHqLb5nLTShLcIrdSBH6qXQiHU0AtXmMOlEPcZsKreC0lKmyu77byBKvidVjBToCQg17xytwK8sQK68EIzq1glUtu'
        b'/PVCwilRlFNh4S4NY4rMYDpsqJxK98AIjALX+Sx6APeWOXostcLZHlQzPYC94AZZUmVbwFlFqgdNcIjCmR5CYCMBJOd7gX5FMoYIWD87F0PQKvIMdVgviM+EUrROiCyG'
        b'ZkoPSljrwMGygifevWplJ9Eh8Hrj8Nm0G0nQ1+SKseuWtjNnt8StEQotLN2fzD23ynN/mIDD0Xybn1lW8aslx3yy/hg1mrTlzYmilMjatZ//cPKnx0vbn37GUot1djS+'
        b'taW6baAheqVTQ9CDH5N0LEp9zK6L3rpaOfIwRyNV5vde9o8T425vWFXBsXV3VlnlvlcXn5clinzns7raeHGAT6LLst5q4/rNc/7y5o5Op6DSG93Nb3xVUZJ9qF1QstOs'
        b'4vGNJT53Lv79hHd4ZGul4IHm9ZolrRW/Obb6g67IP4xLox5cbwi5cHvju08C+td33anLDj12KtLm7Ur7175McPj07m/HUrf8ObPtnfDQ5optX/WFnD2w+3d/ptzfWP1N'
        b'SMCH+6+r678z9LbtXy4xg4YGyw4kdth9m8Tftqh52GOkt7Qn/c/t43kHg9O3dj26FNIyGW68J/Fqqd9bpfx/J/lu1BeE3R+4+/mBtz9++vd7Jz0/OfOjemf9E7F0Vb34'
        b'OPr4tGzNwX+8nv/oifgfML904vM1v+v76qcPQub/6lqDtunTqqD8Rxf/9J14NGIY/MFWBP5R/Po8J5/WH/+k5qK/YPtn4tPWi3hWNGrpJjxgP8W0wTZ9cCFYHla5ajls'
        b'i09w9+bDGrqCdiETngE9QEgYyRAG9tRBLD/WAqOVDS/YwUPMqow4EqjByxxe1YbnQDdJna6w3JmCg2xOxVI66MMZOAhGZsSSwda9VWCIDiZTA2qIBruYW4ETAnjFwYMU'
        b'IpFYslgMDtAosVr3neCQDyJkFstoGqldxoRt1vACAUjpwZbdNEAKHrbZxoj0qaSjSNyx9ACHykGLj5J44qztp9ihq+Ap8khDPiLOh5Ix7WQVMkBT+ko0UhJaLw5ETiRL'
        b'WQIOBtzJyIV7gTDbiwZ6HQ6G11Bfzy5JRjuD0E+9jaxg7E5Fxx+5VmVGchsoiaevJ4MymscCXb7gJN23atgZj9pXEE/ERYtRlZ0sMJJHh6TWcFhCng/rwT4gJSRUezl+'
        b'aXmElRZ4rABVwLeW0kRU24UJJcvdCCe+Dt02QAf9LQbVnvKgvzpL6NAzt3kB4BA4CU8lTyWaofQ1WYJ8H/LyMeUp5NmeZlCMKY86h2kJjnnTEYNbQKstngwF4YkDHWqU'
        b'ETzLgjVrd9A68v2gxYHEVskEJwgB0kZrBh1Lo1BMI+H686LBoZyNyfJUMpReFCvGAXR9iw9jcB2ehfUeSV6qOV0UBAq2wRpEpBaWaxjCxnQ66spth13gkDW4BJuU565e'
        b'Pis0DdaT3vhXIDJ7KFlJwzSQ8GAUzAI3QU0FeSMuvITW4iGf2KX4A1UBtwIpykiPBXoM4GWe3iuCsGEjoCpUbVpKZQM526fMpkwEnGUsWnmxKYXWPUmiJ4x5k9b2wmi5'
        b'Bte2c554Ho6EIQ0ct/bFxXRJhDhC6jxh7fOBndsYL2LcbsGYxYIH1m5Sk3Frb6w4tifZ0GPG7ZaMWSyZtHWQzBGvJemv7T2lqYNufevH7cPQ3zoYzuba69blJp0/7jgP'
        b'ZzGftOFi/JQkrT2ZZHSf/ifOcZ5zcWPfxsHt48qM9Q8cvKWCi5V9laNa4z5R4w7ROJ37MwtxLu9KcaWUM27vhx//sb0T/jVpadtpIbaQuI1begjVSYpuriRGZu7+ias3'
        b'TikfI14vXTm4uG/dmM18nK4+SJyEf4XIbLy+0WC7WYnYJ3Ue61E8H+l2mVvIqKPMLfy+W5TMLeq1qLcMx93iRboPHHmD20YLZPNiJxyXijQmPfwGeTKPMJHGhIXbpNvc'
        b'wSx0n0jjpO6kZ8iog8yTXOBNuvsOWsrc549Gytwj0FX9Sd95InanjljnPQuvX+6ayp+hMhtv/DsYCZzf6GrIe2yAM88nNCfcN/GXmeBoyz6ygLgJk/hJTzTT+MKECe9j'
        b'BxcycNb2ncHiYEncuLWPkPPA2BqPUKzM3PMTnu+krYskT2brJa0cVevbM2azYNLGWbISPQn/XiWz8UFj5I6fiMGBPD/0Sm7zRxfJ3Bbcd1ssc1v8WvZbfuNuifQYVb6m'
        b'KZsXN+EYj8coYHCpzCPil8bIfzBE5h4+ype5LyRj5B+CxkhPrPeehc+LdE7179UyG1/8OwMNFxomeafJMCU1J903CZSZBA5mjBbL5iZNmCTjsAy8Ph4aKnQRZ3jHQ3Vc'
        b'T0UU16GDF1z5j4IXyDX4U9v553ZziUKPj2X1dSlYVv+WejmBnaSSFavzqD7twP8sLTpJusv4mVTOym4rUpf+FnVbJTeyI8kvLhfXpnJjv7oU6DzGQ40NZQX5Rc9PNT6r'
        b'j2O4j08Y0/qoyDKOm+ILyktfXSZb9oYs/6wX7ts47ttUEme3mEJ+Prcgj1sg4BaUIeF1kf8i5Xi+mpTOv6deYnrfn949G5KZtjQ3p0BQXPpK8seT5OF/ZL9Elx7gLk2l'
        b'I7aTd4nOFf9KcxJrbthSnFOQV/ASS+0D3Lmp9NOuJCc3v0zApVvKfpW93K/oZW5lbna54CV6+fvpvXRW9pJu6ZV3UYOOQPLiHXw0fce6K3aFQIW6oO1Bt/rK8mNrbMjJ'
        b'zUIL+4W7+Yfp3bQnhIU08cpzjGtuUGy7F+7dF9Nn2WHa3n1l/ctT9E+hdH7h/v15ev9cVLV2eKIVKrvpfVR9/PRcyRj7y6xjydG0FJOqVyonqxhEWUmpKCsZKmpJajdD'
        b'rqycUfoyaFr152B9/+t5nPfzmD9mzFJr4n9k21RszEWjWYqGFO0Ylc1TirZ6KTqeBVy0HIqKBbM1o7O0o8/M6/2r/fpsktf7w8//Jc/rTbJ6a1gq8no36PIYRKR1s8bp'
        b'WJCsnbVourSNimufkUT6Bg7nZK9YN8oOT4Fm8/JzBdNyfGelMygbEvhvzMT9JbNKv9DT/qaCzf12Tfp/lF/6RazwVB3jv2KFn5WQd/ZCRnP6TgafVUai7T72aa9eooRR'
        b'FMx1YlkI/O8GvLbQhZWvTeV8xf7EO1w+u1VgH+gj06uY3Fx4hJ7fOP2ft9KXgl8c+zL5TBtRcoEXzbSrh3Tu6c3C6OPJ08z1ZKp1GS9orn+hR3+vasAvwNNu+bIGfB6T'
        b'Tu96HAzAGrDPIJ7oo9j6DNCbB3qJKjcxyBsOBMd7JOELAdgJshm2FgRDK1YZDht07OYDjK+vaenaxzvsd2DowGmzt77MTMqO4zMvWW622GSRImJu+NxXLaDkKkW93qOZ'
        b'1bBKsfqfJZ3gCZ8aBuzivsNw1jCQMbelx3ySzfk2I53BNvT4To9h6P8x11maIzMPGDMImLbTnjXoL/SsvyoGGT3ru1V4kDX/V7nbp+8tNiHBdOprSo6ReOUuFz8mzqKi'
        b'URjYX0ZzL4jsTjdolXHLBAWFhdxt/MKCnF+wTc3Gy6gnpcYQwwBn2U6Kw8jcokVxt2XEG8YVRA97s8pK0ZVyrxYa4OCCiLJJwEp/Zq7IN7ehsvqRZ8avLD3E1f6FGb95'
        b'pNZQ9vFEzeKevUOig82MG/+8kmKok6DT8Zu5Oh0JA12XFjPn6qz6QOSeDssF/nlPHp24yJc+ysp86xFMbQYnv2JuzXdxQtTAdJ/F6gx3HofWcB6B18BtD6wxg33ghg+t'
        b'OdYDV1lLtshzMW6EV8GRKaPWxvUcYtSKoDG2F0C305RtKIrPwbYh2K1F6yfFVaDZQ0VpC+uCiMUrFZwgbUeBvi3xWHW6BB6eMj3ZMElKMXjO34vWAsIGZ5K5HbSlkdvW'
        b'wFp4bgU47wHrk5eCc2xKvZDpaKMIpj4Er/PjUbGnOrXRkG3DAJd0YAdP7fkKAAySUUErcArKNpCZnmKGFCVkn1XQa//xDkTbLGxaq45WTVoTMOzOozslOb2buzdPWmM0'
        b'Yuvuo7ulzhe9+r3Q3x+bWLQmNifeM/GVpPau6VojZDwwxpAFiwljdww8VRert3OEkRgiG9cc15Ig8ZOZON83dpcZu0tT7xn70U1Ogx8846x8JvpABYlRaqOuyuMpXusn'
        b'lePyadlLH5d4SuR5jo2fFWxRJaoihkyU/hGPMgvJ36U4rnPpHjU86Aoh7iFHISg9VKclh4fqNLf+kKPgix9yFGwsIVLkrXi6/3vNLgaKPiPy4TsYsqGw52/GY2WmCHrI'
        b'1DX4Wp3SMxUHiAUi9wldl6fMVQzdOV9T+BNHMZzzmBQ82cZURAwMxhEDQ0nAQDO7BwY8usQstC5mKs4gDiFovJBBAg3Ki/xxUSApkYcQDMQhBINICEF55MFwHHlwAQk8'
        b'KC8JxSVhpET+MBz60GwRgzxNXjQXF80jJfLbcAxFixDVhubjkvC62O84WrqBT8woSweZhU9XyOn56Ffd0qdsA12bxxT6oKMRks0v8QAdcFiuyvcIUqO0wBGc11QKT0+j'
        b'mEby399EoO113PIZeBV19GOBfqhzTAU6g4AfdOuM6ozz1P5znArdCmLhNPdz5PgUC4Lx4EzDeHCmenFOS4mXwYeUNno+O0db5fmaz6yrhmQKHZVaWtPey+KcrqJPOZak'
        b'VSPSrv5+TeUd2so7KMVdGMEj/7E4ZzCgTtfURP9zrOoYJJYjDQ7RrdOrM6gzrDOus8jTyTFUaVVnej/kPxz0o5nHOmc0IPfkzLEm2CA1AjfRrtNB7enjPtaZ1JnWmdWZ'
        b'o3YNcoxV2tWd1a68TdzfcyYq7arJW9QnrZmhljRzTFVa0lMZT7Op8UTjw8wxVxlR/e166Gi3eagn36foFz8/t/STQHTLtBM7kju9Bj7m0e8yLh+d8KrnPoa28AVcfinW'
        b'kW4tL0DEZ1pDeUgiI/Vz0KVsAdYpFAi4glJ+URk/G6tnymYgYJYKEB9RXCp/lPIp/DKlEI0YkCIun5tfsC23SN5scen2Gc14e3Mr+KVFBUX5oaGzITZYPp/xgkr+ZdHi'
        b'1EhvbnRxkauAW16WS96gpLQ4p5x012E6EIlJ69PbmDMcepX+s0Xo47ia0qGXqQgbSrBIGkpXXrVX6cr7yeqZ00kGdgYcScG4bVEMwH+ESFKOPxbO0SJQnbRnSuF4pZAJ'
        b'zvHmLiXK4Zxi1CMktXNzKwvKBLikAs9DllwXmvsMZlLeIbnmh+7TLH1QRQHuJLqSV46a4+fkoEX1nD4V5aAfLr+kpLigCD1QVS/8C5ysOjWTk9VNKg/HKwBcI+kcDnvK'
        b'81vFKm2y8Cg8nECSUVFbVsQmJClyYIA78KA2PAuOppVjF1JwDI5UqLawJGiqDXSf3Jq8DR7UrAK18LQciAQOl8AWD5xUOMkrlk2puTKgCGcQISCedHgrm0Scojhalcmg'
        b'kaB1HEAduJjiBXvgJXjWH/QyKZY3pR/GdAa3wf5y7EYMqssiSM5jD3hB6UON8WPLVnitZFLzeGqgGVyF1+nQd2fC+R5oQ5RRLMsyJCH2Er7+SSLTbQ2LxBnT8SudT5Fc'
        b'XaAb7i2P9wZXQJvyxWBdwnKc+MMTHkmkU2ssL9aA1aALHCKAp9KEgLKtaji0JwWbKJwZBbQV7A+5oFZmhEPTfeXX/usIJCSEYCGhrNUXTvIaByzf+dDh3JwYySYzZr9Y'
        b'mDqcP8Tvf/fRr0z+/Fn1n7589FrXIev2CyZ/fC/BYJsXS6/q5g+FHtuYXz56s3dvM1YWnK91OKCW18LDWOnsE9yeCyYr/9K1Sk1gDm6a+O4X331LeH8v/AMQZc0tKWv4'
        b'uxCcPN/CenBkToy0/YHsA8+GgkebRFseVX7mvPWdsyXVzpvFY1UHwp2/FF/6raVFg3Bc23XFjk+++Kzx4Jvpuizhmxqflvuztj8WMX9sOtsyN54xXqt117Fg8Ks4Uemq'
        b'flEWb63vT/zAMbvKt9L93QIs/E0CTgT4+Uczq954a8x47es2by97t85hvabh54UM6t/xMf8cusAzoZNSn/dYLQfHZTF0PfxADRwkiII94do4bxAvNHg6pAXdQIO269al'
        b'xicgWV8iX3AEnJYxh8gRqSumkDbwPE66fgFeNyNSj/lKeDM+QVDp7q2CtIHt4BxBdETDU3tUwdPwImxkgKF18uTUoHMX3BtPwxF56lT8Ik0TJuhiq9OgjP2wBUcDQlxT'
        b'Elo14LSLpzviL8Fl1vK5YC/d6U5wZZ6Hjz1ohg1YOFIHUqanF2ylMRQ1UEhykChwPsEOHAzzgbXBNIDolMVmJJChoWI7wL3wEgOxaPvBFfLChVUmHt6BoE3pL8kMsAFt'
        b'JMdQFmzDeWUwCkXdE7sv41zzXogTBVfZsWhvD5CeIamODw75gH3gMD0u6sZMXTCgRYID7NoATuBEL/GgKRn3LQY2o+4ZglYWaGKCA6T3aRpI1jyUTMhGJJpFTDn0UliJ'
        b'qFPfeqPrRnD/EnQvDjKFc+cciU2ER8ARn3gvkuYHx9KEJ8GJJWBIAzTZZpOpCoVXQJcKxBD0L2KAdtiQQguow7B6OfYV50YpM+aQdDlm4CZxjPWDV5ajV0IdAvVlQPFM'
        b'xDmjtu6Ariye1n8gZuCQGNwZDmPE3Gw+/eCejiFZzqDFzphVSOy0x8LmB1bOYy4x41ZLxkyWTJrbte45uocULRi3WjhmsnDS3LK1ormidU/zHolg3NxTyFagSsLEYVK2'
        b'NH/cOkjIUdTa3bxbkjNhjlh9s9b45ngJe8LE5YGlrWijlDVh6TnInLSw6uSIOWMO/oPpI2uG1sgcFk5YRD5lUVZeY5aeH1tad5qLzTvtxHZSzoSlH+lH8GigTNGZT1Sb'
        b'suN25ovz2ws6i8XF43Y+9+1CZXah43Zho8tldgtELNLox+iFsMNf9j1zHkG/LBi3WzhmsXDS1gEDXCYdeAQvwXUlyBTHOZLy+64LZK4L7rnyX1vyZsLrCfej18ii14yt'
        b'zRyP5o87ZgnZx/WfWtK9/fGplvxLGdmRNvYxRiwY5Btjx7prpBZjrXHXTi3GVe4mqKUCLsDM0AsgDOhoK0pMwQvMsLW2in9gWQaSwB1w6BWHl8UViNTdKKl2wH+GK5Ab'
        b'2NR+1kA08w0UdqIw7WkQgwAlLzWbeVJhlF4R5oDYp/t+BhHxvF4v0FY1U5ey1Wf4UkyPBcOibVd1bLnS//8f6xXqW+koc8bgPNPQdOGL2yxiaLr8vkzV0FRyVfw9Rc1/'
        b'wmJYonVGcpHBWhxpT0FeVWirKexH5DUAnnuetWnOjOksyy7cQEKz/IzRacXq/6XR6QUfGqWtYnuKWv3qbE/TvAiJfryO8V/xInwB6xM7qTwMfbcH59xnHsjYh6I+wT3O'
        b'E/Sn0u4UsE4b9uNoCFjBCwZAvXYI6CkuGBE9ZJSFoFbSr1TT2u9rsTcNNrf4TWNvMXM7pzZJ4m1xp4V3SrOn/2hNgC51LkVzdcsWHouk4yxKR+voZ9kCzBKU2IAmMDyX'
        b'BjNfBo2wXQFm3os4hJnhipzBHcL5rIMHEIM+tURBv4kKB7AL3PgZs80U7Qcvun4U9jMevWifZKBFa2ErSbvvEn7PJZyAPePG7eLHLOJxPLTZZjWNnzerPccn7WW6l6g9'
        b'ZWN7mr76ZW1s2GuBxyQhgp12RMXH6k3Z10KL6djj1XBgfTySz2qmLGy4rGBx3nkmeXKpVQpxOp5uYftr5tLsJD7za4vNFpu2aFukiBQ2tvsRmo8Xs+QRoH7BCjA1JhCP'
        b'icXzxoRMkj2lNLgtXM3gGHp8b8Iy9H/MoRxcnmFyU3v+hLzUoxdpT9nfvo9c/bL2Nxx3CpFVrIifRmaUnsIbKdoMJ3cyU69j1GmgU0VNSWjUXhmhyecxf+yZpYRYkivg'
        b'8hX8gapC7vnqmy2luXm0qmQWqvEZGpbSXEF5aVFZKDeSG0pc8EIz5YOdyS3O2pSb/QyUxS/Y+NSSiD/Z8uUxRHaLX2qLBPy0ZeleK9OJH9pMLzRQHai5qRhIyrFYAw6B'
        b'frf4GTqUKT0BaHLGqoIV2hrwMB+cKqg4J2GXYUaoKVHa/uvQjpqtf0KS/LWWsy1eiHKey9s7dkWn49zkZ8Mivzc2WawMWJTxxi6Xc74yk7tJJ9yD1EfXGjuNrZ+z/+Hq'
        b'u1Z3PYMSxqv/+ui1LB+z4w/+qKOz+AOXD0qsxQbb3vNVDyhBJ07+gHHHv6J46kRCXFcGO2mZGHZaE6/hC7vBCdqN4TAcrJrmX3KIaQ2PVFm50Jlgt2zQlruWwP4FKqI4'
        b'uAWuEyFeHx4CQ7QUDyRrkSDvF2pPt7w3BOyLl6uSnMBVJBNqr2bCC3OMSI5j2AZ6Qa2clCNp9vIsUu4Y/jJuyypxcbSxl658Qe2wmrEfVa4RYrBRTrEFmGI7S6Klzhi0'
        b'PG4eiKOVTBexiHC06LVUmcvScau4MZO4B1YOEud2L6HGpLFV6/zm+RLnXs8uTzon5D1jfxLSLnzcKmLMJALJeUJV6DOHJvjErvbztkDOFNWX05k0bAz8mfdKVQglmNTn'
        b'Ykpj8fglwc6lgueyM1kUzbPKgyJQckTYKw9n8eOVZ1IYwWwUYHGewg/1v09wIulnviDBeSb8507DWZpR6D823u5tRWI68nCABIH/hdqG9/0nfHP8+P2cvI8TWNT7Pmp7'
        b'H5zmMQlPA+rAZbg3HrbCYzg8i4q7jRXsYO/YsogoYxbBYdA15dgJDjHheVALanLA3mfDhJTAEWvmc9aVfKDJfnGg98vj1DUMytr+vpW7zMpdGjhu5Yt2ARL90V4ZM3CZ'
        b'dnw+b6HT0RunmPVfenyOCgfz3eI1L+tvH4h7w6Sd/zXK+NtyN/DLkqZZSJSK80JKcZQSCwl9lHKQCEnlqf8X7CPoOP0k61n2EcV6x2amHHnyvhda7ZFKk1iugI/Rxnwa'
        b'k7ileBs6m3FWQ0W7r2qr0PfIhzUUm1GIMcwT2062lJcJsO2E3rplgoIiGqiN1QzPNH7QqodpKFVsC0ONP8vwotyluK+l/Ap6uNA7v7SdRCup3B/vsyZDVzk7oGQG3EKe'
        b'yw4sh4eId/NCOADOeMQxYRc8SzFiKXgc7cRjJHKlh/UbdMhLNsUWM971EvyQSiwQbxYSr2aDv8Zm6hiYLqZSaTM8SWBTBk95JDNzNCjGCnRYwk5+weltqxhlv0LXljl1'
        b'bEmO1AK+Bic/DCw4JK24+IgV9oNRslpTyB96TN2Pcutaq9OfGP7zTOJmk4fO+3WHh4cDfL5Th/nrf7yXuWO1Xf++36VUOfWIFsfDi+tP5kbP3b497Yfv/jrxVZpZ26dH'
        b'bG1W+W8Hb4yEvs+Zl2RQVPhr3gbtjsXv1sCTxitFq/byTtu7Xvb/JrotKT77wILfXTK9/9Fhn6R2ITAPtT+bMedY8CaDuyGef/tp5K7Z3LkJ0lDm2LHHYeujD9TerfxY'
        b'r+PrJ4yDK3xY2V/wOETPawyPglseQAL3TYU0uQA7YDvhIVbMgc0zmJPyoCp4ETSRy+pmuzF3sihthuurIFnu5QhG4VEPOLpKrjlngA5wFVwlGvWwPV4e7kQz7smgNOcz'
        b'l88FnfC8Np3tvT1qHdaag+tbCWs3TW1uA67QTpa3kHxTg7ifvbB6er6B/foEB2UGbmp5+MCGcj2luj949f9G8cxVDf6nIQ9FssPsGRQTlRNiLaOJ9ZPSNf8Bc2OKIwCy'
        b'J0xdpEZyBXR7iDD6KYsym/NYHWcHXyNeI7UcjBy3DWrWErKFORg7paK0NrdqrWyulLAlyyUrJJxxcx6J/ybKad4pZD8wtsJK6nyJQFVJLTE5qSdXIlsLtYUCofZTU/S0'
        b'MVOXH58aKIpp3e/rGoZRHBZwN4oyYUGOWpShBjRRi7KT6341VQ6dNeq/yGJpUipqX/owysc81nOGtlhV6bsGH0QOT15S6Vu6nCJgWqKYJkeSptJXisZG2arjIDWF/KL8'
        b'bA0VomWkIFqN+IzSoc+og6yD7INqB9XRWYWBIzhSlQ4Bj+jXGaDTy7DOCJ1dxkgoxIlCTfKMyBmmgc4wbeUZxiFnmIbKGcZROa00dnPkZ9iM0mk2/t3sZ5xhkTk52NOq'
        b'KLdiOjgTG7hpYzpt+88uLi3NLSspLsopKMr/mYAi6GQJ5QsEpaGZSsk6k5wO+Kws5mZmppaW52Zmesp9vLbllhJ4GsGEzGqM/1wMCDebX4TPrNJiDGlTOE0I+KVoDXCz'
        b'+EWbn39wToMAzGBVnwkAeO5x+nNHMB4IjFAoK8nNJm/oSY/yMw/UKV/BovItWbmlLwxnUC5KuhtT/nwVGwuyN0472ckbFfG35D6zB8W0e5FiHDYWF+agDaXCJ8xwPtrC'
        b'L908A7ejnLQyLu2i6M1Nxr4XFQVldA8Qs7OxOIcbmldelI2WB6qjkIgyn9mQovfZ/MJCNMdZuXnFcrZDGeiHXgTl2A8Kg274z2xHdQ09dySVOOxQ7kwvxClfEcVzn+cz'
        b'Im8ryz9rdiuqvoy/cD+mKohHS0nmBgWEePmRv8sRhUObMCdXMVWKttDSp1fJs11YonPz+OWFgjLFFlG29cwZdy3jkj8xOGpW56YxcvKViV+lBEle6NsLsKHT+DvjWfyd'
        b'axId6K5TAE+VgYug0b+USTGKKTBiAdrIpWBQF60dDk5s28qgGLAO26XPwiM8BnEgsIUn1nqsh0eS4BEcz+cIIwqc0SvHcgUYAFJ37W1blxP+EF5hLXfz9nKDdT7uSxMR'
        b't9ifWgIvCVbSyBRwzF0zGFwpIIGPwGXH7Sp4mm2wMT2WFt2m0DTZ6zmgi+1JGEaxoy6Fjj8335VdWW8KIqhyV0ysczBuodEj3geelCNhaNi3J88rTo0K91CHbeC2Ge0g'
        b'cQGMwNMe8Kg6euBeimFIgVNwxJE0Hm9Hgrob+KoP7OHnM+lQgY3G8nA6KzO4DgmGdGGsO0lqQPnmfWoq3BpDc6wlaAw1wUV4mkkixcNWCxL5mNyQZ8Ch0FHr6xukzvpy'
        b'pxFVjo9PKGZGkHhMKbHECLAUdb7RA/PY6F3oF4mFrUHwSKxnXIL3Ui93dQoe4uls5ZuWYzEQXoMNmTP5dNjIQ8we6EuleXRwE57BaA3EqF3TBKfXecTwOERbzffEWS8V'
        b'8IITGvA2A7TnyHMDm9rAM/G+6+kQRusZPiWgg4Q9SodX8QTL4xeBG+C6HQN0AxGTjsjUDg+CQ/EqET10DFiwCQybLttFR02qNYYDymBC4E6hJwNcR6xvI7m9EnGKHoqg'
        b'HrARdCgiCsELc+lle9kddMkjCs21oTRxQCETbZLrFl71MqHjCUXitLez4wmBPneeNnnxvALYrQiChZjhyxEMMICY7HPkYnEgaFW6DJiBFor4DHgvooHBR1x5cqcAcAQ9'
        b'BqM8iFcAbNch+yMbNKXEp8JhEgqLxMHSBTfoOFhtaByuxm/yVqB9/OARSxoc1gSaYE28IoyLdjEzCxyFYtAUQAIgGfttIQEW6TAurpqKKFjw0jrS4RAOOBIvj+ECRzly'
        b'RwSzHNK2PbjhrPRxACdhG0W8HEDrDtJ2DLgYrdTeZuQoYivBQXiKbJVytx0KNUoSbCWaFFBjtJjeRnfsclJAMxo6YRp+vw6qCIyCThKqam2hfMfkfaf360wPOo7U2iy0'
        b'VMHoKtiSzKaYOhS2QZ3madFpmS+4wtoyvdJyOKQDh5AkcUIfNMARARreTayl88Apssv9wUnQimuhAWshNUmtMni5HCuAelhIaroKjpH1sA6cAydQXTBMlSuqVgi2apbq'
        b'6qlTbiw23BvrSqcQlUSCM3C4HF4u26qzFV6LAof1S8tZlLENax7cV0IHZ7vtblu2tVyLtKIPr2iiPl4u19mKlpj86QvWqweDq2rzLUgI4U3w1DZlfdDlpahlnMuK3GlB'
        b'4l9BMRxUV9aBx9OVnbMDF9hzwClwnjQVZpY/1ZJ0FRqTUngZ9W4xK5QHWugk7e3LQKOyUgWis+phTMpAnQkvgPNgH0ETbkWyWqM2vCpAXdHRBPtDdUvVKN3dTCTA3RGQ'
        b'B2XxYENKImxOgYfh8ZRFcAgcRpI5aGOgHX8kk45qJs2ZnwI7DJYtw3/so/igb4U8KXqsgbJx2AHala0zwXUy+fFz3cvgVX1UzER9qoY9DPeIXeXY6cwxGCdwRYQv3icx'
        b'ITkNnxAr5DoGT0wCG5cmbEmGDYgUgL1pmmWIdp+Xx2oF9XBfPDzMAqfnUYxQCh4Dx1eT1cQFPeAIHI5F5CDeC9aDYXgxIYlNGYKTLHACCav9hCDr5FpT6OTi+EYItwi2'
        b'hdFU+l64O5WKCx0+i83KCaDoxKzUDwvkX9wW8tiEQC4EV43gXkQAsTSwndoOboTQaa2vVHJQ9y+BAXQ67KB24JBD5AYfcBmeBtdAM430rAT9HHpQR0EdaAc4DCrOLlxA'
        b'FfDjiQhXsCZhDbvMEqegZx7sWPlh8sRCg99/VXXl1keRTRc/Mv3iT3yduxZzdxs4yUQWgXcNohqNNjyNbB2xM1z0UHrTy+Gu+aesx3m7Qv41998avWe/Mt12lWcX8rD9'
        b'n7/927yAGx3v/u5dH0ezkOYF/4rnl+kOXWxYtb7lq+DVgm19F5eDL7xtY9K/uuwfVxKVf6P5UYbp098PGPt35z/9ycT3eqNlUFnYFZuHPwUNGMpM12/K/s5r7PE3P8To'
        b'/W33P7V/WCo9yBvwDT/8U4Tm0oWV8Xcbj3p0umUMv7fZ4fAjXbeA6zknK6Q1V/R/f+2Qx28+eOefj1L8yyRnB5r/9ukXcT/oHF0X8IaM43eQ6/nR4h8Kvqx49/dpn8fW'
        b'iz7X5hh/curh5t+8++iOwOfjCu1Df9bOnbP5qf8dVvrostcLPuk5cf6geRL41Q/OVGnMaInej7HR9aUZNWHC8oiFpQNnPtg9vzeY94H25zsbNkSZtGzOOCAKqzxl1nU3'
        b'bfe6w5+98+WVz0KcsyIFXGgdqz6vWad/8ck3BgY3XF30pxOFKdyhj/Y6FbfGfOR1+Ga61d8lgaVnA79uLszuyLa97rBywU39/9m4rvCyelDbxcN/zDu9fbJf9GBia8C5'
        b'47+/Nrj+9pzba+x2RotNJ5q+WOpyDo5/lFLpWNx+zmPerzvdl7XrWRX2WP++M3VHUPdPUvM3f/3FfK8U2ZPwBsvvbE7vvltZ73r9whdfPLA2vK57vWks0rM/YnldWteZ'
        b'/LjW4LeX/rst1yuoorC29vE/vL/tTIt+b+nfu1b7qv2q3D/Dp+8f0e+nJxbEbYU9Jf/I/eSxq3/xlxUfc/J/KjiRGBD3JOC79FLb3euD77H35WjZ3vui+d9j9yZBTY55'
        b'0rcLLjMHNuppeh2mHlka/faeq5HFnT9VaNnM2ePtxDzk5d90Jea9/QNqo3MtXde+f/C4eV3Mgra1k6bbvhP4xvUsrRwQ/8O0+/2s3/5jwvjT9dmbPjf4M6db8PuQN79V'
        b'r+8LinH7Y7XurzzaWejA/bPXo/eSbtXaOq3Ymb6/3ulfy87oGt6wzln4V6HDhzXjtzXN4nan6v/7LyuD3tazFX71tO++0ZPw3No3hu5VZUas/R+H/HN339xT6Me+OvEj'
        b'j44HBpvB4FoPJRSn0JvAHIyWsoBkObxB7H/wIBwGZ+NBCxAreZpV+sSmAK+thsPxCuxFMmzyIjUM4UEWaISd8BoBgcIuxDde1VYNMsdMlhsCh2E70baZwEvwcnzCFCLX'
        b'1xz2LgDXachQNSIFLSo40v4AotGjcaSgD54kxsStoGGjHObq44DVdWvgTTqccguUgiM4J0g/4uuUOFdnPVpfd2JHCY1ynVLW6cLTtL6OIw8oV2wH7pCQy6E+mLekIy6X'
        b'smmXxYOIcnkkJcLD6hTbgBvIAH3z+TTwtsEgCSvxUuFepRZvDqBBu6GwB/VrCjGcAVuJ/q8VXqERv7XguiVOchIQLU9zwnQCl8Ax0jA/DhyI90DDWpuJ+qtOqW9nOhfB'
        b'o6RhQyCZr5L2BYyASxTJ+1JcTobJtlBPAXGGdVysMfXeRIZpTRRqVAFRhuIYimCUs0AXuYqOSChEzQ5j1tdHAx1G3Yw00Anraf/LFngbnKLtSexwDvHbvB5Opt8NDCIx'
        b'6JAnZkyReNMAb9gneiLuxIcFj4PuXXRMvlpExU/FT7kOaK9mWuyGF8LB8W/xCcDIyopHx36tkgOsXEUPUj3s9lZy4ouiCSMOWyLJICWvQBKNgt/WzCDc9gXYQOtfa+GV'
        b'4BncNjgNakxtQC95obIC7ylmuzEEM9tQnEruZSaCW0peG5zfrgze2QbE5N6FoDFRzmo7edCsNhwO+JbwLjd8TWle25R6Jqt9PZYop9NAG8liE0fiLu7eg67rw2pWsa8h'
        b'PdxNQOyHk834GEYnezHxanQ33k1QTpvL0UsqeLKILMSSbYVXdOEgwx/sZXjCbjVNeHwNDRs/vBAejCdzgiYEXOUihr2NiXilnnx6290CYnBRHoYc1JuAGp+l4Lwbg7KO'
        b'YYMOeAXQKXP80mE1CXI+F20YMKhFacAuJgecnf8t1oXGbdfUA0eVR3pjORlCXXCHKY8RWO/JMCR5IoydWHiJjBC6xGGBG3QF78QIRDKQ5ICeC0VsxIlfN6ZR8xfggBWp'
        b'k+yJWBU0IcyM9ZT5XPYCNHaXaZhAJ5rTW6QOvKPpk+QVi8gS2m7xOB2SC+xUy3QqJUiFOXA/xiEgCtBAT4Y2OMxcDm9h0kUvJrjPBzFGhzyTwPE1qB4a8iSmTVU5TURF'
        b'XkicVMD3PTfDQwr4PiKLV+gFfmV+ERzW3yY3NGjCPibstQHndwGa/nn7oO11yMeL5+bFANWRlGY+E1xKgiKew6uJX/hf/iCG3RnqlOpZ/+QAC35OznMBFirXiA3CXI02'
        b'GO9eS4LERxyNkOTLna1J4MR5F+f3zR9Nub7utbR74Slv5YoWTFinEeR47Fvzfjf/7fky3spxu/Qxi3RVrLwCVmFsM2bs1pcyaDmwfpR/z2sBDWAftwoZMwmZNDYXhj2w'
        b'dJA493p3eQ86T1jOG/WfpPOgtm/v3CPeM27ve99+vsx+/rh9uIj9wMFZkip16Eo/bSNSf+Do0pUtdZZu7XM9XTi4XDYnaNxx3n3HcJlj+GjeuONiEVu0XKyBDRc49xDj'
        b'pJbShtFr2WUpDTxtP2HhJy+bumiEL562nrDweqpPWQU/NqBs7LBlRRIoZUgdJCHj1l7C6I+NzcXzJYJxa897xp7khZaMW8WOmcQ+MHeabsMxNiUR7yOaIyTOE8aus2w4'
        b'k2Z2rYXNhS1FQtbHNtxJO9d7doukURdj+2IH4u57LpR5Lhz3XHTPLu61nEkH90lrOxzGMEwcdt/aQ2btMWnv2FklrmrfM8l16tXt0j2tP8l1nrRz+pjrjJPf3uf6ybh+'
        b'OGLkLvGu+/Y+MnufyWlXnFx7w7rC7jvNkznNm37F2Q3nD7rvHCJzDpl0nEODZubKHOdO8rwu2vTZ3OdFyXhRTww1Hcwem1EObvjWSfs5nTvFOye5ruQvJ/feBV0LFH85'
        b'e9x3DpQ5B0468vBUT/J87/MiZLwI1IS92ROenYWRkP04gnJwmeqEUBctD5wr4L6x1z1jr0nfwBGdIZ37vnHjvnFvJ445rxYmPnBylbIv6vTp3HcLk7mFjTuFjxlwJwOD'
        b'RxKGEu4Hxo4Hxo7FrR5bs+5e3Pox1w3omsRIZuD8wMEFLfDiruJxhyCh3qR/yIjPsM9rEWMrUu9FpY25rBTqiUplBo4fK4YnQOYUMOniP+nmeVGzT3PMf9G4WxQau0nP'
        b'gPuekTLPyHuey19Lf3Pt62vxO6M7FBl49cbnLFAUodf26PK45xg0aDrp4PTEVNvMSMh8YkGZ2E4GBI2EDYW9pvVeQPzbq8bmpAsXCXc2Jz8ws2rJE7Imza2OVonK75l7'
        b'S9WxUc4cL4BQcWh7mDB60tx6wilwMFXmFCozDyUbMuYtExkvcdwuacwi6WNrR+KPwpQajll73Lf2k1n7jVsHzLwPrQ8R+wNzN6mJDD1EIKNNjyQLVMsu/NVRKMD+IjJz'
        b'N8kK9IGKLKw79cX6UrZ086j/aOm4xSKh2qSBcatWs5YoUOIvNb5o2mc6aNRnNVg2miPUmjCIwld1m3VFuZJI8cYJA1f8t36zvoQ9YeCCv+s164kE9Cr1ldn7Thj4odL7'
        b'Bg4yA0QacH0zi9b85vzW4uZiSc64mQceF9o4WtVcJUmZMOc9ZrJNHfEe1hZrS6ImLNxwNnETuksTBjjCg1D76R4m2tEyy3k/fbuNSdk4fU0x0T00tcH7SJoyYe83aePw'
        b'hEVx/R+z0MUfCRIVWC+KSA9n3bc0zNCi7oerZWhoTGq5ZPizJv0Y6JM2aJrSBk2lubB0I7ZqKg2FpQW/aOR84XMA88OZ9L/pJwBtGO14FvhMheY3YOPoIlTz39XU0+Vr'
        b'GQzGIsZTCn9+Rz5fxjMG22V71edRI9qRTBaP9ZCjAMFMxaPIZlNT/5Qa/zr0cdxAYRwlEB4NuWlUW24aZRLjKDaNUsSDnVVnmmdMDKNsJlWvNHNWqWlOg+6g72oqJlD2'
        b'bjW5YXRGqSoo/5MU5jMMo2klcqea6XZRYiHkyy1cStTP862NihrTvaAFcmOdShOecptdNr/omYacLGyT5ZKE0tjo8nwL7H9inMTm3mc+1V3RPXcu8XQmdiRFP2irIN0l'
        b'bOJFXS+iLXHPNgxyo4pzcgNCuFn8UmLJol+4NLekNLcsl7T9cmgmMoByO+7MiKbPMsCi5p8d5k1u3lMYN7E98ZfsXy9r7eJQM61d9knl2EsD8dUnQS/ijJO94WEk4Xos'
        b'n4I3w0u+syBNR3ia8CLcD4UEC+U4L5+2LcntMdjSAuvAZXAsOWWalWkH7NVEklD1DqIfh72ISb/mgQ0BsegBvRgMdQscJFpGiwUkozHHN7Ao4f2MlbSnz/KIGzifcdEQ'
        b'ndF4w2/KF+MtDgfhsAeQYrG+DjalYNNQYgLh/9On3FUWWabO0JkSjSkrTRcJ6AcjiAd4CRjIh8M8HBAxkUoEbZvo0E5qqT9Swp1z2JRvZm6GgV0ireicFC+k8Vmby9dQ'
        b'othRBpVZvamy4qPN9OWY7oXk6t+CNzEmmJSBpGCHtZ7FJopoOuFNUD83oAo2o3nwp/zRUErLozCZH1kFO1Rd52GdV1wibFkeS0TYpcR0CK7F+CwnacDjl8fGecbJk5iO'
        b'wCbdODd12up1wRjnBplh9ZqNTXOEPTQ8DbaDozwGre1vC91BMvvBGnB7Rna/bHidTsQhgc1wRCUZChQjwb6ZuRPtU/x8UB0ARc+1urkp7rMH5ymAnqJZBY/CajJcN93o'
        b'/BrcwB0J9axyuXZ54SZ6ME8vSqdMnLYwqIXVOzIs2PalddhxE1/hqdE2pDpwHPV7AIxiyXY7tR3ehPtJBIG83SFgwC6Ylk/9QV85zuNsC48Wexg70+rmhXPJ3OivBjj+'
        b'wUnYThFdcyhoIFak2LkuWBLHSmgg8len2EEMcFEHniQDwlkvmML4O4EhhZloBN4hN5sh2fgYraQISyBpTUA3PA9vFLwbJFQr4yDS7+X59eGWxOIJX4Par4J//6DJ+X8E'
        b'Nz7s4aRxAr4xcNX7IPhr/eC0RxsdPouzORq3eGBo5aM/mmp419k32/29pnG4PKLErfBMov/2P3bc//RJ03vJ3e/vnVzw+l9EcdY7dvWbj5yqL+2/15Fc9/fvj/dfendi'
        b'Efvqom9KFhzrDDgoNU7rf+duyN1+A6f8/sDQg1/XZGyL7o8zDO9p+PZ0efFHXXH+j//67YWhh31xIQHvfWSwtLruVys/vfD2o49+q73I+Q/RG+a0HA0/v6dve8cH796w'
        b'2TPWeS3jYX9VxVnWkbfmfKnu5DhSr//FQv8/fb1sx2uVExfmvXn8/Gt/8Bu0vZD3+Xc7D+Q4WyYLt/29cGFAhMb9bstOfm3PrU0H9LT+h+FbsiD0VnLaRKt0tMa7J9xO'
        b'60/7NuRKh05lfP6osyPjiLtORaDtt9cMrOePtJ9gVuX2L/s85Zvi71eo/3tPBFcUZp+RvStisEiPkfzXspSzH44sizH4+vjVtbrfJP/rN2+mDP7zp+uX766p6k3r844u'
        b'aHFf3Pvhue52L7bB94ZpN+/LxMuPmUgrs/78eNEG3YDt/0i9a/C3deEBP217P4epuWGkzPSbgH/WBtRtaBo+EGiavOXDW6fLHe5+8Nt/bv/UuurMxUIrx3HxicqgoY+y'
        b'osM6xzh/X/m0Y8MX/zb8Z2mDneHFOXUSV8G8i29tXjE+/+DRzY3Lvv7w7yf28O9/diSmczfri3faXzdbzzMjysYSuC+bqO+KYZMc8Ki1kFbn1INL8MZUjAFNk3DYxARd'
        b'sH4j0VLEgRpYoz0z1Qe4FcvmpIFhGvPYjajDCUWAtXlRJMQakPJpPfDlHeA43rawOwqtVKzig7VaRDkSD7vAFax6hTdArwIredaE6Ij9NMAR4qihlTQ9hQhx0yiHI3Tj'
        b'DRvhAUSBYuHh/AVop8cy0GVN8l6bEMU5G09s/PFe7jgbRTvlw2KCUdBO3ypVs6SzUxfBIXmC6iImPSQNsBY2TCWS1tReA2uYoAU0z6EVw6Noz571QP0hiktNW7YnEwjh'
        b'mXDScHocOEFy+zEDYBed2m8huE2D6U/CIS25TvM6lCp0aLRSE/YBEa34vg6ukq77AGkCrZE9Ay6oUfpBrLXwpC7RPm/1ZnmAG3AgicbkI6qNzicPdcoatLNBR2YBreZs'
        b'gp1huIHEhGQ1MBpCqdsw2WBkA60HOw0uxREdFyJxB5WEmajTtJeQjjjDHjSt26BYrlGbpk9bmEfqgI5oeGe6Oo0yn+sDz7EXwHPwBNEtZsBuOrfH1VWonWeo08ApeJbO'
        b'+dIHR6IVCi1KMz8KjR64BA6Dszz7/3t11fPlFzwSqlzSbCWWIruhKkJsh/VMvz2Vi0SP9QaT1mMVZjIoCysldnbjhLkP0btEvbZR5pI0bpU8ZpL8wNx20tahc7V4dfva'
        b'5pgHpvYSdSlrwtTzga27NGjc1l8Yg6MI5qGbjX0mbZ0wkrZ9nTBm0thSFN0ZJ45rT7hn7EZaXThuFTlmEonBuG6S6AlTnnSFHIwr8WsPlZrLrH2FURiT6/6JudUDay5x'
        b'NV0+brdizGLFpJV9p7vYXZIxbuUtjHqMVqRdp4fYQ5I9buUujJp0du2N7YptThQuFgV9bOuIHm9uIxIc3YXVYCul5YPlfVUyl/BxhwiR+iTXWaQ26eCCvpnbSthHqx5w'
        b'nSSLpWmDK/vWy5zDxrnhisv4A7+9nUPnJvEmqcugutRu3C5YxPrE2v6Bm/9gwIC+WFfEFuU/sHacdHTpde9yl6ac9hFFfWxlq9K5B+bW5PXjx60SxkwSVDQGs3Rgv4hj'
        b'tvOQRo9GT9hFNmsL2cLcSWNzEedoxGxdmYPrfQc/mYPfuEMAqpfRrPfA2GzSxKo1uTlZEivNmTAJeGDiIHGWsidMvB7bURY2Qu0n1pS1ffscNJgm5qRepGSr1GHCxHMS'
        b'XY2ctLAUxYi1JGkyC3f0l7mFKOBoxaQNV8SYtLGVqImXStVlNt7oL3Qzzq+eLVkudZBuHYwcXSRcOmGyAJcnNidKXCZM3BQPiMZZxdH3pOYkSaBUS+YUMBgjc5o/YRKG'
        b'Su+buMhMXNAwmHjgOnHNcSLBhIkzrZ7YykCLRGbK+5EkzgD6pnGBrF8HqsVFyDHTZrSK4ZQ6pRLu8dXoFJ65T3HLs5UMU4qGG1jR8HO7Ugu9R9kCVPUfWNOQyWAw3LGi'
        b'wf17/PFSrrUskueYvLQ9fn2u+gzFAh4xIlztQB/HNVUUC6w6jTqmPJsjrVygsHohT0epSlB/paqEyGf5CSlUCVMpHZVuP8Rb6BW7xdH3KMJ90vc9I8GBNzeKhs+SrjwH'
        b'Fky86LC+AVVdmpIcHOTrh+X7LXwBBn+WCUoLivKf2wU6zugUFHZmEHb6+ks7BXOSCDYnNhgenC7o8EDPz7gFG8ObMQR3Bu+4gjtyVFoAHFGExzUCw+RyLKiDF5fDbpXU'
        b'jCT47i0GgdntQDLv4BTozchbmfoxoKqg8UKvWhmOSNMVFHPgiJ8R8NVh565JKuTc3PuJadibx7W1WGqNKa+dCdlRu+SzFs7erliLiYyKo+/u3PzXM5pmet/Efvrld4+v'
        b'shfMbcr7S+6X742ZVn91YueaDyQfJ5lW5Zm7/Hvl7z9cWbMvYlk/M9f0NzE3v7I6ufJS+r4hN8+36wNYre947MsOf3195UcFY/naXg0bfh3975/+mHyqag5ncctiU+/F'
        b'S77+kPX+I6e/2g/y1Aj/VWIFhHJL9fpSwumCTjAkTymnAcRa8PQM956qnE10fjYJuJwwndXFYCqMOFibRdiuzfAy4pYVRmk9cFiVf2uHZ2jDfodFBmodMXe1KXKD95ad'
        b'rzij2GzOQq+cbEglb2E7g4pNv0y4i0GK9tRZlPMfeOqYO0tSx83dsUHIWlQuM3aedPUQRous7pk4PzC1fWDuIHGTRk2Y+z5w8h20GHcKFXEmXX3uu4bIXEPGXefjmjJ0'
        b'Shhbjhm7TLrgOy2akyadPLBp4XTEfaf56IAZdwpHh+JqmQGXpHeWRL9nwFPx8tRXcbhRktD/8PAo0599MtBHwq/wkfDzg7ldR+6bgw+F4mzlofAy58F3+I0YDzV2FJRg'
        b'Dej/aUYBHPW8b7ZTTWn2xoJt8oCk8jwt00KgPoPUR9FKyMLtRGtZsKWkMBfrXXNzHJ57LMgHYGaATVT8Itl+ZxNWdhIdRbIO1kbT+JYZ+iMwFCcHbmPxN8ucU4BI4dWC'
        b'iphv2WU4bk3t+BkcQYSOTZTjlx3wr4Zy//N5+wcbfojL4HfzGjsS0gp1dHyvzblrtE30wSZ1kUW+NvWXu5rHI/7EY9OCmBDcgnUK+ExqHO1vCNqIFFzuDC6oit9M42zQ'
        b'xTOihbQG0BivoEgb4WUVf0NfOEoC2qzRQ682jKnNEGz0gnVLaYUrvLZiaeJWORWLBwMaYDAKDvx8zoaHBnx6jhULu0yZRUFpdJlRgdARP5qOPF6Yy6BMzJTWYdcJY3c6'
        b'xtxrrkq68YEZb9zMY8zAY3Z+hzees31n5Xf4rbpKfofn9Uyso5LfoTgHbUrrl41TTnpXep6B1YFJSakxSaV/x901+IW45VPR33BwFhI5gfiZE/8+YssifCahLORdeJb/'
        b't9KrJTUjlPlsxtgFD/mMcMl62OqWrohurqlr8LUZjm7u1FUxoevzlGmrm83AUc19H5OvTyIUQc2X4qDm8QwS1VwenhzHEDcPqVvyPUdfN/AJd0bE8Ee6JmKnCV2775m6'
        b'uva4SfvH+NvXduRx6MI3TA4dQR1dQN++NqH7UTah6/GUaaFrgy95Psbfvg7El9L7Aq45PbB36jMZivqWxdAL+Xhh9GTYwqesXQxdm6cU/vxGDRU/ZuOvX+9i4Zuy+1hD'
        b'KddMrm0cC1wyoRv7lJlMKuPPb+hPVG0p4zEp/3otucepz7gvdchtzG3+69ETukufMs103b+l0AeuG4fqoq9fR+CaKRO6Dt8ytXQ98RXHJ/gb7ZeNFc8rQxOUwdHhFfwF'
        b'XgL1CRjC5eaqtg1WV5Z/jRZYCGiE10AHOBpeDNt9DUAtHIE3TOcFgepseFE9FNaBZnCUA+phB9xrrwuE8ACQgHOgJToadGuDo6CBYQ1vgxF4WxeIQxGncwRc4oMrsC9V'
        b'FwPb98GL4aa6YeA2GIwFt5egek2wYTsYQRT0nPcucDoBXAjbBW/BXg04CPrR/+tzwVlwGvbkb/V3gWI/WA27isApuB/2wUuwfVc4OAR6YD0YMl+yNSzZDBxygtVRVZsC'
        b'4GF4C4wUhMHazUus7PlWMaHxaqv8d3ong9OrbLxAC7wSBq7BXjAMhEWgHzajZq7GgqshW9xhk/8G2KgLe3LgoDFidCXgKOxG/2/AE5lRsG1ZwCZwOBueVwenwFVYWwyG'
        b'YDM8lQLPg8GKLfAMuF0FbsDWVNBsCbs3r4EnwJl5pvBCLLjhCxrR2zeDI4bR4GIK2OcajzpwFbYFg4tVcGA5EDNgD2iDe+ExcBL9btoIpLANdFfYsbTBMXAZdvp7Ip7z'
        b'6sZgrTB4BRzMtgHVS7aA/Tmo2dZEcJOXHVNsHwOPFMDbsD0OHl9lAc5XRsJRxGl2wMFwdSBazkvDoE9wHBzQmpMKhy1gF+xGf40kgoPgZAYajOOg1ROOBEe4hDubGMNL'
        b'K1HByZ2uazygGPYbGCOZQgiupJah0mY9LUd4B93RD4fARdSdQQq2BuTOh+K1oN0f3DSCnXpZieBIviACVq+ArXbg0IYgDrwDRm2MwWghuGMNavPR7edKYD0U+dnA7hzH'
        b'lavDfWALWgejoKeMjxbdCdiWqmO5dkfR/J3wss06W9CWBLot18CL2J0ESjnoZS6jFdUGuxfCRg44uBhe90XTeAIMhKC3PIf6NwL2ZaAZaPJagJZDQyW4ZG4NG9D43IAS'
        b'vd0seBPWL3EuBu3ljWjZW62De0HHikhwBK16HXATDpvuWogmt3cxqLYDJ6HISycQXkDTMwROsRaDnmy+Ew8IN7LBIe4eH3A2uHzHRn3EvteDbihFA9tYkpkObplmgLaF'
        b'oA0MgTNgHx+edIetHnPgKLwORlhgUBMes4ZX+Wol6BS/nLaqYgFsr0opBANIBmgBt9zQS6DlAc8Xxc9HTZyyAe2wZlkGavtoBmidB0TgYBbaeTXMkER4FAx6oTqXoBT0'
        b'V62pMjbI2JMVuCQfnjTcHmgIz6M3PYTW8T60JfbORXuqfol9gvP2OWilNQExPOeHVvgAWpmjsI4PjxaCm+idFsMboF4Dno2AR3eCzvL4yAJ43hUedEPi451d87z3gNr1'
        b'milg1MIOR7KGvYbB7GJ4JxNeYkJhpRl/MdwPhrVA4+5YIII1NkvAkVWgGh7I0UdClDQ5Jc0/22iOJeyLXKJlYuTtq2YdkIb2T0cCrEtBsyuC/RagDpGUaj7sCULTeAPs'
        b'hQdY8GgSaIZDXHgyCTZkwH4wzDZEK6/BHHSj18BU6cAGfzyyiJM5By5XVFqCw3boeefRgpJW5oCDaDkc3GHIQdthOA8eg9d2+ZuAFjSM+9H0DCLCdYWTrxcHOy0RVyVZ'
        b'vRIOoF13AI7YrwO3EuPBHdCr6QyOliGC0ANqQ3Lh8BZYnwFueVthw8LaZDBijZbcADy8AhyNjzNcWwGvoOf1oLVwag2oQRvoDs5X7g8HjF1TnE2TQQ0a8yur4NlCNHrS'
        b'ZHCJB0fVgCjLGXQBoWn5OBPL4rBPgFZkOGjCKxJ1+5oHuFweAk+uZaNmJXB/ER9Itmqjbdk6d5kn6DHIjAd9EYh6X0XjdRO2WqOVdBvxfkfBJXBxKahdg3brAUd4KzYi'
        b'IhyK4sDpHAMteACt2LNoTY2A/U6gjbsNLeFWZgS4uZ0K8l4KWzYLPNDEDYMejF0H19HOOYq2XHvWmnVFiHZ0e8L2TWjAb2Annga0VvvBaXACHlu7GNHEOx7m6YJ164Ek'
        b'EfXwDBTCy25obzQvcPSvhI0mmuCa6opF++PEMkvUjysVcJ+X5h5wuYiQy2N624EY0cmeyISgHQ7ZYDBp5y4z1vol4JA5qMlDL3YHNdCD6NK+oAi0fkUaW8Bh0LsBtOii'
        b'Ge7j6oKWYCiOBRIBqlID8Zt0wlPoSOoF1fpMuC8cUZCzphpgJBhet5iD1sIlcN0f3japgKeLTLezNxbCanAc7ddaeEwfDdQZ9Ho98CYYXoYms9sQNqyy3YhW2z44tBCc'
        b'QUN+c60rOpYurKq0Qau3a0s4FGaiw6uVB/oq0IZo9EZT0R3pj0hcPVqX6NhcG7h5Lmx22wSlVYv0dqAO7gPVaC13g2E/rlsOHwwjcjOiYwJb0LJu1IL7dGBdDDjln4qW'
        b'BOjajvpQD5vcwBW0ZgZA0w7YrWHtjMb5BjwTs8oH3IYntWLc0TvXYjg3Orbbo8HwkvwVaC6Hwd6yVWhGxeg47AQ3dsBD24BonUYuPBGet8SbHOlN8QJ02tSWI7IgRHVO'
        b'hC0xz4CtoH0zaGBuswAn0fpGg4jWNzi1ehPq6B3YyXIpjouB9UW6sDk3XcN2PTxvBVrx4vJBW7o7xjA3ufw9vK674UU0B4jUFhH+4ia86AGvMhbbZQKJBhSv0GKAIexJ'
        b'dgRtGhEQCsAlCpFbZ1NY7YeGWGSzE17QANfBmdwlbqAtCgwYo8OgzRJVP6IHT2pssdmElk2bPtqMIn8evJ3mHYvoZmf88p3wmA1ojLObh46CES00OrfhIY1loC8Tbxg+'
        b'o2QtZok6ilDfbqxLR0QD0+BziBQgDqQ4CLQbL/RYYQQvrgLNmdFg72Jw3QBKluxZg4ZGMm+nMWhMSVgF+lzg5T22UZmIdPSjGRnYgsZlALSv2c6AJ2ICwLVU3516UbAG'
        b'tANRRDY6mfeime62METjXQvPsMAdQ3g0zdzACh19DSZAuC6Bn4p2762A5aGFaB+3ZIAWb7AvwcTHBEoLwbmFaP/VbQLH5sC9UQxYrbYMXM9ZBI7HFIDhiCRwA9QtCola'
        b'vNsKitEGQLTxLHreQWoLOgW64ZA6kKCdUG+GdswlNFpN8KQ/uAUaLdFGPekCblTBq1sj0MIVobPuCDwRthV2RyKiUp2zvBLULilGm0BSBU5UmaJ1dSVnO+zLt4AiRAW7'
        b'EKX4f+V9CVRV59X2uRNwmWVGUAZlHmRQBhkEEWRGBgEFvTJcJhGQQVFRQWQWZBCQeQaZZBARECTZu236xybRmLaGmDZN+3XK/6UYTczU9tvnYJKv/dt+7Vr/Wv3X+tH1'
        b'3nPvPec9593v3s9+9nvP3qfaDWtjNjkh6Xw9Du4nYkRaPWToTNfQRVsDXs6F+1XJL+7bDLciSQ/vwNyZnWT2Kzjmg1dIbGXk9Xqct7KELBeupBiasbqIDRp7ODjop8ss'
        b'hu50aEncdPZUCHbSWebItFqhMZ2uZpQoQSkf6gpI8Fd0z9HwOsiFjpPnzIuFPlvsxkGdMKVIchYjGVrYJ8XmAJrfYbwbD13H6BJvesJNMuRKV7iMrKWvYMtB6qLiaNop'
        b'1g1hyQldvJVDCDOLZdv9DsvjtJ69X/gWOxgraOJzqUJN1F9XBI3hWxZhhQu8E1hHLMLDxQru2MH0KQUzV9lcYrDX/aKxcS+NBXq9aYZX2HzWXJLSPAtDscbEvGt5jlhq'
        b'nwBddPpqmM4556G4NQhWcCoRe2i3mwQirRcNoNgqmmZ8QehCcNgCi5ZOe3D8CNG0ZlyUsmmg5MnGyE/fRgK30os2eE2N9LZy7xHoDcSWCC9ysPVSL2g7aMmuPsLd3XS2'
        b'OuIkvbCsQgbeBX2qOOoPdfaF2KgcYpB6ghCvRJYspPucvASmTXbvC9bxUCIlm4BmZZstQpJbl7yaK84ZmMoJ/PCSEYmy2IQUf2iTHvn5OupzMh5Lj8A1byBw8iRXSPhE'
        b'PAGXJNiJ3W4nCbOaYYQcyiBR/WmaKd4Bm2ioMckiV90BE2FYehj743dDdbB1CEmuFKp8MvTC9oezTKb6yAUYTrTAS0lQrH7OEFvJZTXE4XwuaU9LOI4fw0obO2jlk6r1'
        b'BGOFNynYKmH7ZOoRCkrqCb+rdHVIxHPHsMkNK6An24VEf8MByj1Jbwaxwf6QRoqTa1giDB7Dhex4mvJeNxV5E0dnDV1HC0L2OUWsUt8XakYOcdUEOg9Sr41KpFz3TkB1'
        b'RDRZyVI89JrCsEYyzmTRCTtomF1HyRaG4qSaBD+NMGkLUwokzGpsTYUqA5g9knNUew+MZdJOk9CWQgDRJsigqyqOJJWfc4SrHrBiRi53ES9f1MB7TCZ2WBF9HoHGgndZ'
        b'vawmRWxl9bIki1PLFVLLQhyX4o0zckR9StXPkQhLTLcQzZ3Tt1PDJlXikzERZ/2h/qKBybkCKE/QOSBRjCA3PsD+g9JdBP8tBCV0mAdLnYpUlWCikKZ2CXui9yiQy5yH'
        b'VZVjOIRtGeRyR0RYXIDNUVJYOZdFX3UkHiE+c5OjEEAU4i6spJP+30rUwbJcAxwyJ73op4sej8rChiJDAohOlvOm0QVUHt19QkeBjmgg8GghedSEHCK+N3Y+8nxMWqGx'
        b'YigSbR3AIWPC7pF4z0JlEm8NsNZbDwtZOZ5qMK+ST1ZSkku0oj421FG8HacTQ4n8t0TSLvNwWRbHlKRYGW7FLoBdgoocaFchWV6G7kKclZCqTu9QtAokhGpLV/XLOONJ'
        b'zLJLD/q3kJVOsTd16JkLSZzNdsQ767U14FqWoYEvmevEFlzcT+hVSzHKHEHFUhab+IiNJ01weBtFuGN4+Ty0m9uwtb9k6XylOOy4X+pYaBSfQoZeQgZRWkC20C4PjfZY'
        b'd9wRO4JNyBxuqW/KSyQQXMaxwzh2hCxn0Ii0sNOZqMsdR7q2hZwsGMinQLySwmVtOw0CzdY9bF6l2zaK++rToJaIgwhvHCSXWUnK2uR5HG8f1MUyIVzDKSmdt4sUrp3Z'
        b'dtoj53Ce1gGa4hljS7byKTQk50OnZyFUb8MqUTzWZECbO+07C3NEPVuxKppcRQ2xk06NYGXoCTS9GMbWa8CbZw9lEmFsjfT0dWbjs3FXGPLOtYyHO6RVV0Ng5ly6Rgph'
        b'UJsKae6cDQ6EF+3HJj9LUoqb2sZYsiM44yDWqWKJhQx3cxy0nyEPHyCCpSSGt4PUXcdsI9W8SYILbKY5jfbqRqo5IfbGIZ1wZ3uQFR9uHGd4Xgy2FWlwN1uGn9ENspG5'
        b'qMHw9tCHbrjMdbTVjiv3XcOjUc8zvEAGO5KgnLu3rwgmj2ONNc8furjKed1sOdgCPwHDeGw5SyJqwlqyinYvRbqGqQvyBnFiaHGLUElQJ8fUYEuK0E8yamYpuyleDvAL'
        b'gfIMTy0LQpo7OKR7lrxJH3QHqHrHEXjXQ2ciXiW6QuaLPU7smgvF3g2FtgU+MKbF0rzzMCRNwAoF6MtNIJtpglVPKI4Jx+ZQmkX6niyxzJc2B2GEIXitOKhGHK5jB01W'
        b'l8Ph7aRzJVsoIJixPET9XmXC6JxlUkLUKbZuA80yxTjpRVBuyz5/NgrqTSlWmCVdOEz0pcEU2+woSJqERld6KcuXhMC9INL1QXITNaRVs/oUN5USj610tSiCCkdicEuE'
        b'EtPkD3ph2og48Q1oc5G6nBLgVVmpCl73Pw6jTriQa2WAi0dx/HCAJozKFhVIQ3IlhKENMChmlw7gur4ulpBsxwmMSggfh+MPU19XSKQthzQyyGgX6RLqd9Fohz02y8co'
        b'YnfSMS74ahdgqQPFMsUkmEkkJF11gCsCnD5kGeaAZbEEan1uOG1KVjPiaAVsquwo1LsRI7pK4ynO1S4Qkmuqz6MxDMLKvjiik01QbQndsjiRjvX+0LwHew9SWHWF4pcV'
        b'WU2sOWaUZOGjhxNy0HwMmnPJSlYslAtwNCk3F4fpX+N5JbrcKqfoWAojJwmKGxxx1md/0aaUZLhtrgTzytjjT1Z1yRkndwSQYY8SQWAXd6pUKIifg5LN0CkhEICWPf6H'
        b'Q+NyYw5rEyWqJD++qO2C13J3OJJqzp4SEDgMwYSNFqwWpOG4M4UD9Zbq2K7Nwjj5uwq7i2Sit3cRX6xil6MsQlPIn8KdHdCRTzpVAXfioCKLXPggjO0j450MugiTEor6'
        b'umlKJwN3cyswywLyMT1xqRRRDcFVZ229C1bsz6KhbCSBDSlwF/vtqFnFFUMtaJHmWefrEOUa98SFo0pYooTLPOg+ejEOmwwKbpADk8IV579emyEEvelp6KVyCie0ZDaf'
        b'xr5kso2SRILlmQNxWB2ooeVNkcsqtOaSKMsVNESHJcERhDr1jptJbVpgSheH7XWCjNzh1jmKBipidcJskrxlyaMthEdzizSzYQZ0knZociKBLMvTAGazCJD6yaGspOF8'
        b'AcxbwBTUuFuxWavYmUVvrp7aCe3k0QjZ61k1HYAZS7hpl01Uv3s3zibHkZDLQ6K1Wa6JBNFDMTzie8tk0yX6ZDsz+8nBdQv1cYR7kCUOqEfDDWNC1Dro8MoNJpbdnUrc'
        b's9SLBdYZKDmfiW3Enl30vIgrDOiqsItbwThyVs1HHsZOHCEYvrKxFJCXRAZQf9yErowcGvZdICxY1Cc76KJIF0ZCjjIZWLE3k0Cn8+jeVHILt7BTShfZmM/elUlHEC3H'
        b'rqRkmMo84Ixz2qpwb9th0oXrGjjkbcsKxRJHtaW4mE5qwxL9MQoelnNx5ajIXRXb9OyxMSyHQO2KOvarUQDWdI6YVDGsniS2M7cHRjeFme9x3E7OtxebD8lh3/5sknuH'
        b'uVnBVot0rQP71TZhr/rFgt1KUL6XH0oqP0b6VwXDFwgH+gqi/aEmjoD2khUsaEjJKpfJLObPx5wgR5kFdQKcofcTRPMWE04R3HZ6FMXi0CEbAqV2HLeAu3uPwqSBSQBh'
        b'QhM7xzQP9wjZ2tgqLJtoGCu4euFAMHU6uAsaT2juD6NzL+mRPO76wII3YXCFRGS8J58tM1DwE1JWkmqdLHRFYs238W0Mnb4WWncasCHuoQgFHtxWw8pQmJKxgck4GS3y'
        b'LgSBc7tIE6Zco3EFqm3TXUlHG7h1kzFjG0IxdqWubZM1lBGokZKWwzSFBnjvdJiNBc3XOC57esOoPrSp6G8m6V+BuWSy1oE97gyM6hKujJlAmysWGxHWzcJELPYchA6H'
        b'QwQ7FQHQmXyInMJUNMtO+rHvUK6ZSJDmji07cKgQq2xhdlsUlmbZwWDGXnIMgzTkEeKtnX4EOLAYjNXWh8h1dFiSOV+2MYpJwyFnzcO5eC+UtK2FnEfZTg056MnIgmlC'
        b'r246w3SoLNnBak4YRe4NpDBXYPAsDZrc1WYc3gHNBeRQWkMzSJ0obGm1VsqCMnnD3Tjpmo7XA7VOwDKMFmCHKyx55xKtHaX4dTp6K6xGMS54WUkOVwV0leUhmrAoYhdH'
        b'BlxhOFXLH1p89Ta7UtRVTUPCSTdC8WXSiSmarjukCCsnKfycUCehtyUmsYaTkmZOoFrLj/dOPakIt+NwOCMsND3lKNHUWWW6hHZyuOPyOBsENUnQGm2lDRRhXMLaDMUE'
        b'nIiCq+pex46cw+7AkC322GCHM1vS4rHOkc/SVkKhMgqje3A5uLCIRl+TqEqeqw/vbRWaQIt6BJYnxe4/ujfEj2z8igc257kk46IxIdJNmtIaCg1lJAQPEwqH9DmIYVH7'
        b'GgnyetJOmMHbxhZkuNdx4AzZWx1Mm1P4U7NJlpzjWE6sJp20JhlXDpykualFogf1YphXc7MlTOs+E+iiflHFjMyrjSDnnjVWSqDb+QQRlVWcLdgrYLMwYkz+QrMpup0X'
        b'8LXxBjZ4qeTCoIZMhhmhbhcNZ4YwscWeFxgVwIZPSbiQhLeUyLJu0+j7rN2UsV7/8BYhqXg7ee8rxOAnzpK8m3dGiQ/CTSdsjyXtbmcT7hXYmBzG9Q+SwCmuhjotLIv0'
        b'Y7mPOnU2KTGAIQec9LVEIjSBW0hGNcbQY2tABtrsDh2aJJyOPPI6I1KYidUnPW/nR+zUgwFdVyhOhKodxHw9CA4NDlroEVA0pmGpGGakuRfJcZXC3CEntgyalIXxGtn8'
        b'A44wqugMbKGrNh0JCWlRDftTNfGmnPlZb/eT2tDlDFPBRaRWQ+T5BrFNF+fzA3FUjXjOVXKid9PIG5yV98mlWeymThqNXfJh0E1oj5N7tsMNT3nszMcJ1ZQjOjC8SfUk'
        b'NGnilaBU6qgErlnLOoTQjBLNILEsCA1DcrycIzLwpjFXhGQBOo8Z46ofgRcFegHeHgxZRjWZJZFvgq5GmFdIwYpd5J1JR2t8YHqzmEdQcCfeXxJPwDdEk7JA/ZZt0owh'
        b'N14LA3JwOQ3KXXHUhjxA5YVT0OgSz9YpgH4Gbh110yNIWYLydDMytREdtlTWFPGcZQomy7DzmFh3F97VhtYol6Cc/eRDb8ANnBTSIZfglqGGK0UcAzDsDWMifbKmTlg1'
        b'0dQlNltrifVFWM8Kp+o0zApyTN3o0wZ36DeLwUVyltiyabv7dux2gevSWNKcSmzJJc+0UhiHUzvdD0JpZj4h4zVbxgmGEwo1EhNJ7plpeBdqE2H6JPHnBrY6FslrZjcB'
        b'a9l2VwoKF7Eid3dQigcBQSVWn7NhH4aoyCPdG1NkuTFNZVtyXuF5WAijtwPQHkwReg9M5fjjzRjOL87hXfc4T2g1J59Jwe9+D5wLJPo2pZBsTzzu+iGyjVXZRCJrxcaW'
        b'UFzAF7DVnbE9kLUj8hTAGtIK3rUiKL5O2jnvinM6xHRjsUk+3QfGt2OHzw5oEJB/61Vi9/BQTadgcflcqr8/8YHSwIOuhlh+NpvY9QqOeNP8z0KPGJedZDPJ6YzzsC8S'
        b'l0zOQzGFfc2mfioKkdiSzP24Nsku9V88B9dgiV3SGoDFCBoimckwu1RENHcIhv21sO1MhNnhHTS4Zhxzx5KLWIe39ck3VsZDz0FiW7dtZNKyHXRg2l+e7H6Cdqx1ILmW'
        b'Z5INrKhg7xEoY5+OSa6lzh7r9WRpjENiG7xZlEYEsDyxEC57kFOug14BzuqIsSNax0+H1GXCXKS6BRf2HIR6ZS85Qs0lLN5PZGacxbRdeJMh992MV+2UpQegLC7I3CU/'
        b'Qx5XVGPOmhHAEyf3PHEAruZgk0MkxdMsC73lmlZE2lFlBtObdgeRDfdpw5I8zMeeybTEGyaEWnewA8qO4lKhPJb7RpJVlFFMcoMwp4HiFSMSdutW7FKUF6RoY83hjPQj'
        b'EkdsD1Lm+WrRcZPQIAONm7TJ3prgToZigNUOnN/Krn2S2y6G5c1wh/39bkR/C4V8VxL3eBB3795JsuiDm1tssqAheBvZRB2FPXkF0LaT5qA8AG+7KxB7v0usoNP3rDb2'
        b'K14Q0Qga/aBdXVxE5tZI7xpg1Srr2BnoNiKcLlVzCYPbOtCp6uyhaBh3Gi8FYpm+RBZHoqAxDbphnNSoLuIQu2KKIwXsehfN/F0C32nyEqU4aIuVFyRG5KaJA0XTvl2h'
        b'NJxLMTh/1paIGQyRuTSRp65UOJRYcJgMsgdYb0KUdNCJRrd6Hq5txUYpse7bJ0lfJk/rkFqNn8eKi1BFQE7M41IstG6D+oInLFEayjP+1gq82FWpqzHkhAnBMvYYRqhs'
        b'x3qygJjt5+jrTt3UJLEODuq6bKfpXcWbqTAh63+MzjFPBGmI74TzerCKI84ZCjSgMuzNB/YX4JLD7tAohBYdgvLl09gWBP0C2hyGJSn5mhsXCBmvkjFdo8lokN+KA4GE'
        b'pOMk+yvYWISrcNddA6uc4K4N9m8PwZpM9peuAHaZKvkAyabMlBClSlGIY9LNpPdzZwzJyBftw7JJ4QbVHejaGu20sGWbgQV2mPoSXyDb8CFtWNFIw9uK2O5mhENKFDSW'
        b'xUOpDy56wbi4kMClichPM0HzAEMqvyQDXfr+0KpAEcKQnQr0edtDmyNRhTKdKE28sW2njAxWhvtglQJe8jlAAfFdW+JXFa44o5KDt3coBjlAvyM2ee/2IqHcgnYhWf0g'
        b'IX352WOGqmxy6iIBwSKUGJKuT/KIlV08ZU/q1hQBZQqcTixKCLxXj5sSHHRiRTZJbZiFgdt2xDyaUtJgwIX0mV2Bb8JqbbzlRGFNQypUykB/miHcEMKU526cZ0NzLA4n'
        b'9JoLPk3e/J6jDLHqAbhijqXWJJgpLeg/D62bSCkrjdlfk0VFMk6pUdTzNXdlbCHiIHOaJUCl6ruyKNojNn+JEKIBhtWxbZ92IXtXRSRJrh2Wjp4ygTEbWPaDAQsRtBkR'
        b'ueqIhdHjFO5MwoCNhOgPOW2n3dk7YSnQ7CT2m8D1QBi2svPFWyLyJ60BRhTSduGsPXm3UdZA2iLV9jkSvR63xdWD2wnYWiOOKUvOR20+RIpTmS3B4l3BdJbr2zwMvM4z'
        b'RC8rj+NoeqEFf+PJYhMEAf15ZkRxNooosgUUI3GcW4Myz1TOc4DZwG8q+YZgs4VgoxjhJVjeFWTN08AShufCYEssVmysaN2jCKUjCOsoyohneHYM2UtbFLcQFQXl7IPx'
        b'qoThsMTwfOggqHPmqttu3om9QQGiA1kbi2Ni7KGrYxe7TO2Cg8L4ckcYngN9bonFG4UN6+GaAtYEi04bMzxXBq8qQxd3vVHJsMrVbew5sbGYpiugjthzE19uPoA1FqIQ'
        b'W4YXxhCe92Az19lmLFHEmhAZHDzMLak1QO8x7twhDkrs8tsV743lNwV3C95GEvJ1GE4PChRhrTLDs2KwUpS0MfJ+C1luCQ4ux2yswJH8yy14ftwTRLk83A+PCJiv7bkH'
        b'oVqH5YcyFgLu49+kCZhrOgrcxw6qvhv1IudTBcw7qlz1/OB3fdSYUAt+KHXFZe2mu8n/gp/3MZv++vussqjXst7z0ogP3G4SGL2jJTno45UXm18cbfz8uo+yzFaN7Ysm'
        b'ez/UedPEbvrqlSlv2z8J/phcrhHg1lKjLEz9WccvOt7/8Z/aGrxHA0N+77Ad367fpNts42D6SwejJgeTRw7bbjmYPZs9qJUc3pLckdkqPfSF1QUVHWPDH5ncWr0p95v9'
        b'r/9GZHQva1esvMarX9zujezw/c/bMds+vVBxxOgNn9DTi782Nmr/+nmQ0lsPhv649V5Up/Jrb0VfqPrJpe5GxbBnQfZFBuM9/dEPFCNq/vPY99/4XdhS2pdd4x9su7q+'
        b'+/PPtxVdl/1iYjMo9T4ueDz2wPO1kp9Hl2qsOk3ob2Fsnlp9IMypLnWSCex3++VPI7wO9U5EBgmGfqfq8pbZK7rm7/1WrrDxvVduXBM9+jI81iRHPf5D1+nN/9F7X/Z7'
        b'944pfW1+7YuP7G63jxScllq/8aTgo8/e8XF/3eLNVxIa89zvP7ue0nbn88qwcQtLr7gJ2c2vL3X8JOKNI3lvPH2wWHpu8a1P236lG/wwJ/YXBZ7F90/uCjFZmPPIf/r+'
        b'cxUI/LzO8tdvu7767IdvKx/5IuBIzXjazGplp2b+6Z1vbM474uZS/aaOaYjLreGZN2t/NOl/3vl2U6fV4zfUCmDmft5c/8dLo6G/D3V68o76hY9FryW9dtJlPGVU78ut'
        b'jr+fXN7T9PQVi086I3f5rKz/7tz3zD78w+CbRoMfPXtU+/Sdi23zZ37+9PXwPcsy7dEW33v/s/STu879WFXpQ/3bj+xfFBv8etNR4ar8BbkR2yp1zx8GdL5I6O3/ypPv'
        b'2xZa/IMz6l/ZVx9+NWzs/fsu3/ctSn109KOMKz+we1j4aF+C5N2yd89+fWvt8S2+/senTuDTjN84GMCMv3pOZ9FvP498oBHySPGNt/XfeASToTVz++7P7R1//vqrx++U'
        b'5JX+5NT3vsr+bUzalmzRsigj/Q89F4ZcnB+X/7Hoh0dF0U+XLUYvOfVEZa30PrkQsfjsUu6LgP/42bPXOxQOfq3qsXfmDx8673rjo4HK06U/e39Q+9XTH95NjP+zwLzk'
        b'0IOpPgt5rkRfLPnqWbJ/nqYXBz51FE9sJLR2FLr8RV6D2oWNm4iPanMl22TOwPg3D7h8mWqbLfdtsi25gQUu+8HKg6+QqyRWIjZQo5JboEgu/I6A8UjTPyuUI1pWySWE'
        b'Hgjf/O1Op3H+NEXncUoyjI6XAG4qYh+XECoHU4V5hIh9pxRPFuAdttDuFRU5JXmcVjklYiyUhTjhl//cmvbUgX7lvL+xF9RS31itevok9R0ilIHFxFQuNzea6EOJwsu9'
        b'sDeWzfAY4e/wzORulg7HK755UCt3ki4vj1xi1V/057plozu8LQP3QuOem7Kiq/UltrZRGG/vKbYA8f9RGE8Z7lhE/PWNtXL/DzX/9vzYf+/tzREMl5zr9Q/+/u7dz3//'
        b'b+OOeTmJJDM7IVkiOfvtFndL/EcULP75z3/+uphZj+YxSprrQlmx9rsqavUONaevG1UXteX1OvQm9O3qOHsjvP3izPbp3AWjmYKF8JnCW7av7vuhGvq/7RD8RGfzdYfr'
        b'CW27OsS9gQ91bKe1H+q4PHAPfagd+iAi6sHB6IcRMW9rxzzRMuxVa8p6oLp9XcDoxPLW5Rk1jXrvBs3KvesyjLZHpcJjTcMH2wIfagZWytMnOpY/1XZ+qO1cqfiBkeNP'
        b'jfY9NNr3QG4rt+320MiNtj+VEYjdXsirire82C4rtvtMTV+s85m7iLaUheKdLxTlxDovNFTF+usM25gyunqVSi+Efjz2E7Z9EcE3EJuvM9TUS5+zL+v7eIy86gt+Nl/s'
        b'+oL5rv2Ea58J6Mt17sv1ZBFtPxZrv+BfENC5mO/aZxst7auzcYCQfb++V47R3/pATucDsQp3WCpfrPsZw7b/fVf2/XoU9a3zgm8sdnvOUMN9v86+fRHIOywSs0Wj/sbL'
        b'842X9bPy3BCOyIq3v2C+a59yba/+M+715VDYzXUvFe6ACBG763ftOtdez3zGvb48gPsiY+MMXjLsrt+1n3Htyx25j/0UY3hiw08Ytn2Ry98j1nnGUPPZXj5P7PqpDE+8'
        b'7YWMklhn3ZDrT8KnKWHY9jOufdkTu7m+T8TtclBGbP2C+ev2E659uTu7ue6lZCYrXI/imVIbwdvYNqc2+uUntP00XYbmhb/uL2dBH8X+xU5/1T4tkNknlOM/DZILktvC'
        b'fyCn+yxWlVEzqvR+T9OsnvfE0m3B+6Gl50L+Q8t976ga9Ro9VN3eG/62qhnpuZb5LzWN/qd9jP+5ffT/0T5PaZ8tT1Xosj5f98nn8cQBvHfVDAYVH9j4PTLc/0jN/4Gi'
        b'/0Z6c6+3TrA88yN59eAtLyuo7cq9+48ervz/UcNl4hz7m4UR/hmczX3M5p98C7FW38D6F8XMi0gej6fK5tv9zYZNzFb9V+q/sTP5Kl/GW415VU3Be4sgfcJJUZgXxGNz'
        b'XX4irf9foXxv1fK7qR+9e6w4QUb45JLpwj6lk1X34wrtnlTZp3yZ6L/e69z45WjhLs/LO3732Ctx8Kv1P3b9aexuRI+gMbkhRHnxVw3GPXx5i/7rllFDlzOiRmSG3hm8'
        b'8skO+5ak8MrTT027T8zMm75pef6+yLX7tbcy3tePuxh/3Hux8P1fjPXdV/K5+qjxVN9couSrifxXQn652/fGts/yf/Tx7Dw0JDRblYt/U77rzcAl3yPOsb+/duKX53wj'
        b'U/XbJ17vzDP0PbC78+NP/re2zfsp95+IfPefXszKjX3+3NTs/p/nF2SqtNamp3l6W1x+2y+rvXV+pvSI+ee/3faK517FnGKffS5gnxiVcymyM6HS8s2GD/itC3uVCnbm'
        b'1GqEPPlA6/QP6/cov/bwR6mpHz+puXddMabpPfUdGe8GvPuRf5F78PfHPdQiv3jry66rdj949Lpcyh5RVMaxx9ssDLh6vme02JxmrAoL4+qByDK5KQowy8cb0HKUy8jN'
        b'gtXkoDBfGLTBGXY3NuNlEy4LoE8KFRwnFYXADFG+qxvlkNk1YlkGS+CusppgK7ZBD5did4ii1xtYgkvsszVCZBkZIV/OCKqfszF2JrTqYs0OGSbehRfJ4EDky7I4FU4R'
        b'VlhnztY0ucJjYBJHxLZ8aE/D2o2Uvi68i31EmCO3bVSKDuXBtDMUcyTU7Sz2sbk63MH0Zfg5ZawWhBr7cwnKCngPGoICouO5qtdczesO7OdGE4xj2MY+m3gCu+nIkACs'
        b'tQgQMmrYJIClQBjmRrMby6OCAq1DdznyGGtzWWzky2A5jmwUDG4+iBNBDiZiRzo0aKOUl4qRwM0GF14WiO5PD3LwiXYMCAjZ+FYZbwrsz+PoRmWbSQ2YwxrLbVjBVs4R'
        b'MMJwHvuTfx534d55bLVhrMWBwBAi50J7HkyEijlxOGMDTlnZ4D15rGUrqZ/gwQJOQ/NGqfSedGsrtqp4MBa7sGcNIdkIGb3zQjY9ABs3Uh1XYUkSxF4VDZwT+RROKljw'
        b'sR6GoYRTF2UtnMn7b3tQBNEmH8CH6f1Y95x9XAlJbxXbFXBWBW/n4RJ0UEB0JwfnTlK8osQw+tuEshTOtHGdqWyCFS4f1IrtkS31la8A7Xz2Hue9nJiN8bIFXbLCtpfP'
        b'62FrhHvg0HNzVhIwohMEk+Y0w2zlZ64KflgA1O4ItWEf/HOVv99XtgiqmY1KQ/PMYQWcxjn28U4NjKY/DsNdvQ0tuu6YDpVCNhODrdHDiIp4OAgVBhvVglbCsZP9ygYr'
        b'4fLuHZbfpHNuLhBCeTRdCjvjJ6HNmARfzRahD+azi0f9YlM+mUSXLXcKJRyCSqtAG+sQG1seY4jFipoCeVUs36jVPQOXYTXIiq5ojvTFljohS6IhqDsKsBtu4tJG3nz/'
        b'mTgrf2tLtjgAyd3kqALW8/EmDvpzcSeWeECdVaCIwfLjvCAa1C6csNjz74iD/u1+7v+St2QrjPydgOVf85tsVirrN9Oz0vNfhib3GTY0+VMx80yfEak/VtL4qdLWh0pb'
        b'OwsfKZkX+z0WylcElwQ/2GQ06PKO0Po9odJ7wk3vCVV+LnR4KHT4udCKtr/5r/Vzoe37QpP3hZbrfBmR5jpfINZ9X9HoU3lGZPC+0IiOfSETvlvkS0T6f3z5dONlPSWf'
        b'xyhqFId9/vwMbanqfcLw2E511gX0+tWvFLToA5HmY1WNahF9JNL8Ms+SVVAFGR9dBnWVfCwEaMr3sWbQnMduWwjYbWsFn90CdOVRu0HMLNcEmdKs3A4SyJoovyAnU7om'
        b'zEzPy18TJqcnUZudI81aE+Tl566JEs/kS/PWhInZ2ZlrgvSs/DVRCpEQeslNyEqVronSs3IK8tcESWm5a4Ls3OQ1mZT0zHwpvTmRkLMmOJuesyZKyEtKT18TpEkLaRfq'
        b'Xj49Lz0rLz8hK0m6JpNTkJiZnrSm6LuRGh+ScJwOVszJlebnp6eckRSeyFyTC85OOu6XThcpTnR0kmaxdUbXlNLzsiX56Sek1NGJnDWh34F9fmtKOQm5eVIJfcUWNVnb'
        b'dCI72dV544GVkuT01PT8NdmEpCRpTn7emhI3MEl+NnGqrNQ1QWxI8JpCXlp6Sr5EmpubnbumVJCVlJaQniVNlkgLk9bEEkmelEQlkawpZ2VLshNTCvKSuGcqr4m/eUPD'
        b'KchiC41+R3m56Tn2T/4ZGn6ntVzDLvPmRXMKS39E9lR4vEwRS+z+VvuMa/9lsrdFxtuGedVGwdtF8KVcCk2xNCnNdk1VInm5/ZJ0frn55XvDnISk42x5WLamAfudNDnU'
        b'Qo7LAl+TlUgSMjMlko0hcHnia0Qd12Qys5MSMvNyV9h4wJB0cCO3nMuB31hIcKe5KsiUeuay5SN57LgDqSEd5/Ge8oU84boio6BULPuJsGA3T2M9p4DHiDf9VE7voZze'
        b'9cB35MweWHu+aormD60DH8upviuv9UDb8ZH8zgfCne8yqvU6P2Y2c+f6L8L9d/Q='
    ))))
