
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
        b'eJy0vQdcHMf1OL67V+GOAwFCoHqSQOLgqKpWs5AQvQmECpJ1HOwdHAIOXRESVkfSgRDqtiSr915RtVo8E5ckju0kTuJcEjtOnPxsx3FcUpV87f+b2b3jjmbs7/cPH4ad'
        b'2d15U968Nm/e/oHx+eHgbyb82adBwjNlTBVTxvIsz21iyjiTpEbKS5pZ6yheapI1M8vk9sTFnEnOy5rZjaxJYeKaWZbh5SVMgFmneFITWDKnKE1bZ+WdtSat1ax1VJu0'
        b'Rasc1dZ6bYal3mGqrNY2GCuXGatMiYGB86otds+zvMlsqTfZtWZnfaXDYq23a431vLay1mi3Q6nDqm202pZpGy2Oai0BkRhYOVZsfxz8xcKfivShCRIX42JdnEvikrpk'
        b'LrlL4VK6AlyBLpVL7QpyaVzBrhDXAFeoK8wV7hroinANckW6olyDXUNcQ13DXMNdI1xa10jXKNdoV7QrxjXGNdYcS0dDuSa2RdrMrNE1yVfHNjMlzGpdM8Mya2PX6hbC'
        b'uMEIVOskBZWeYWXFYQ0jzZLSoS1hdMEFtUoy5jM5RppXBMXltTJtEeMcTToQNgu34dZCtK8xby5uwe2FOtyeXVqUIGfGzpHix+jReJ3EOQSexEfQ1UG52frsBNyKt+XL'
        b'GE1RIN4qKcA7m5wD4b5Dii/D7TB8P1vGSKUsOjoZ73Zq4Q66PB2fjKdv5Wfjdt1yfClbyoTiPRL0ImrG63UcBVCCDuKduanj4JFcvL1wRDHUEzxSMnUG7nAOhvv1erSP'
        b'3M7Oh7sxBXBXg69IUvDBZ8UK8HG0x2w38uQBgIW3sUxgNoeuTcEXnSPhfqpzoQrfCMa37KgV32nAN5ejtuAghhk6WjoVb1FYCnSsM5K096YZncRteTn4di7eJmEk+BGL'
        b'Dq4JhttkzpvwCdSaiy7HwkhshQdQayE0KBu1JxUk6ORM5hzFLLR+9bLpntqOpqtxB7Qnr1DGyKrRxtUsPoWOrhNvr0jOjkc38M6cBH1+QiLLqAdKAvFefB5uD4Pby/Ax'
        b'fDU+Bm3M0sfh1jzSJxXeyeEr6CG6VsmK8y6Bv3Geed9J0NEfGZn/LTq6Yl06V5wr3qV3JbgSXUmuZFeKK9U8TkRStiUAkJQDJGUpknIUSdm1nIikZl8kJY0d2Q1JLQKS'
        b'ZoUrGDXDhDRErKhtCZYytLBAIWHIgyHB9bWF9SahsFoRwIQwTPK1CUb9o5pJQmH4cCkD/7Vv8Stq/zvcwNQGQmGjI0r6t1HfG8Uw74/9grudsmDlSLY2AG5UTjrAXlMw'
        b'2mO2dam/SR2r/jNDi79K/SJ4bzAb+9bif7BfRf5peTjjZpwJZCrX4+srYbm0Jc2NjUUPl+KtSVmAA+j8vNicfLxDn5idkJPPMvXBAdPXNDlnkzduTS2xO2wrljvt+A6+'
        b'hm/iG/g2vo5v4Y5gpTpQExCkQjtQC9qWmjw+dWLKhHHoDrpWgy9JGfRocQC+bEHbnNmkni0G9CA3L6cgOz8X74B1ug1vBSRvxe3QmFh9XKJOvSIhHl1F59ClYqjjBt6H'
        b'd+Hn8E78PN6D9y5gmEHJQaF4p9OLMmQ8yeAMIrOQ7KFgErNEnFKuBSZxjQSmlKNTKqFTyq2ViFNa1ZXuSLpNqbTARui8Jea+Q2KfDFe/HmLMNb5e8WF5tfmSKYu9URN5'
        b'I/Lghgf6M+YtZVs0Z/R/0rwyWPrGFvMZfcTOrGRJ1RQm4mXV6NRwncxBCAA+FJMJo78V70AHq8nClD7FouvoMDrgIL1ABxKy4hNhbFr1sIzQCTnaziVYBzki4N70+eh2'
        b'fEJsVgLH4IdhcvQCl4DPDqSvLcT3+fgE3J6XIoNhrpSXsfgyOjnTQWgaXh8+CLdloctAPdco8UY2Ix1d07FuLlank9hIjzuT88yTgdPMNmuTqV5rFthOot3UYJzhljgt'
        b'PBkIu5yM1exANpS1kUsbGSmd1B1Qb6wz2YFFmdxSo63K7lYYDDZnvcHgVhkMlbUmY72zwWDQcZ2w4Jpgu01BEhlJSH3pBIaGwHgUwslZjpXT1EkGAG1Ee/CGeOgm3lnO'
        b'Mhzaz84emZ1RyXVBBzqDqQQdOIoQUrPUixCS/iOExLc6L0KEFThJQawOn7TnyQhjyMPnGXR2WRHlIPhFdLk6F26wqDlMx2AXOoH2OsPhztw1jbgDyCdbh9tglm7hh/gE'
        b'7Ra+UoUu4zZyC93FB+cw+Lln8A5aWyx+gI6q8skdFzo5gEH3l+AW5wC4U7tmajwp59PnMvjgM2gLhRGcg56PT5TD48fQ+sUMPvssfkSbi8+h/bV4z1y4VAQ2Mfn4fBF9'
        b'AR/Ch/FJvAeGXr8Mb2P0A/BVXYBwq2Me3jkVxhZvXqyBBKrYLNzY8zS+8iy5cRrfdJJ0X5oA5BirR/ehKryvKhkSNWqn5ej+Wg2m5XeexhshXTODlucZoM77MMz4sEYG'
        b'Cd5gowMyFgjMcUxvPERnSiGF1XJIGN5mfDgT3Q8mwPCZXJJuHE8HJAgdmoZPQqtUg6sZVT0+KYDejo6wJVDTWPQQX4eaN851hkJ5Nj4UhPcA6iU78XEmGZ2XUcjBaB9Q'
        b'pj14H9wJzkQ7GAN+HqgX4XE1QIcO4g477lgBqIfPsdDIA9HD5lPy4KVInIiGFGfIeq9iVjPPhKxhV7MtIAPapKvZXdxyKUE1unKE5cO5ucRkN1upY4XlIfUsiSeB02ot'
        b'dkelta5hxkJSJalfzjinwr8ZYzJzBSlDYNtZeC/qAGraWliAt+nw5Tp0W5Kaitpy0W5otgpfYtAD/KIKXRtcZzEN/ovMvhcqcR87HrP9oWZjUXjzm7qWY/8aN3nyk8gZ'
        b'TEeKUZvy4gT1vuwlkXd/NuHzzzQzLq1f/OvVlmUrT28pPicd/cqS5Pd368ZdeXRgUPMerSTv138+dU8z5djU1Enjs5+NGmeacSbys2kLfnq4abmy+LU/NLgW7Gj98Nar'
        b'eb+Ju/7anN+888k95+eZNX/c/p9//uvkzmO6YSVfr7u199JXbLJqzHPmd4BSkrmQr1XHJ+rwVj06WAg5dIkbZ8BnBCJ6HQS5C/E5CbglO69AxqjQ9aEchw+PXuWg0soZ'
        b'5IJJbNODFJZQL5Uz8qXcaPRwlINwbLwzehFlf3grSFe4FV3KwdfRLRkTNl6Cd6fj4wKEk+gIsB9KqEUqXaRE1/ENWTeaqZN2Kegyh26Vqb7SypsMhJBSEjqcYEqWlJWy'
        b'SvFXygbCbwgXyoawajaStWl8SCtrdwfWWw12EOmrTXYb4e42Qpe6t4SzhZDrYC9FJdVkeynqvVBfiqqFkhj8Aj7kwSL7AAGPpMxgvFvaCKh0rA/SSjmtH2ntm9d2k/G9'
        b'y8RLWgME8emNoWFM9MqH8Ez5kvySRYJQtLk2m9mZla1gysvjVk0dwmTQ0t9NHMBok/+mYBrK9f+0xwqPvrEikAmfdhBErfK8hKDVDCUc6FYkujouGRY9gEN7mAqY2QOW'
        b'nNKNnL2MLODQH8W8nhK4PnnPxJD0n/wqP1z67MBpWZ/uiq99znH953GBf7g84dSzn71f0ho3JurVH9b/+NEnfxrVsmnroL2ha1Wnf7gttGmcdaVj2cagfFXiW4f/kmJu'
        b'3/9p8OCigTLVv3UcxWb83HB0Nj4hJZ/yb8q8C9FhBxH5VTrcEp+YrY/TJYL8hVtHozsME6mVLg0ZIBKEb0SxAZXVpsplhkqbibc4rDaDyKvprJdFUkQLgRQQa4APYkkq'
        b'LbxbUWl11jtsq/rGK0IzbWFevCK1LPZCOOuHV0StjJmqBpTKykcPQNzcjrYXJoJs2Qp9S0KwoPJYZjo6KMdn8JFRfuK/F8OoLMcCjnXKcizFr97Fcz/8Io2M6YZfowX8'
        b'mjchLEQjyYKr8tUJaqeISvcLQvL+JZnJEFR65ZnBzDxa6s6ShXwmgVU1szxvbMVEAcH+NY7LG86Sq3J1x/KhQuHLcUGRbgYaXlSeJ62wCYW/XBgevkJSRF5fbR9YJBR+'
        b'kDY075GkgTw5TVkiFwoz0kYG/otZT8AP/efMbKHw4wHRSx5zO8nro25EhQuFC8bq5u2QHAPg5bNuqpOFwiXrErg6yTVSZ4UyvEYofLtJUZQlAYqoLc/bPN8gFF58NnDM'
        b'VUksWR1q8+RMofC+ZmzifWY/eZLjVqiFwh/FxMkbJOfIk6PGLH1WKBw/Nyo8nisn0Jf8p3SEUPilISDyB6yWFKrrZz4lFI4ZEZz+Cgsic3K5fnUuKxTWLx0yTclUkzqX'
        b'KIcNEAqLI4fnaNiV5Mlpv1qcLhTmGkYtfZ1pIYM8y5pkFgpfyR20ZDmzkLRzyc05M4VC+7TE4gruLnl91h6bOEeHJk8YNY17iwxd8SOz2PhqPpVLZF4jdaYWKkQdbKkz'
        b'JfIDyffIyM/SzolgdNFUQhiFmtEGoo+mMOiiKgVtnkvFjEh0asI4wKhUkGrQ9tSRZfThefhR9TiO6K/ouGwc2odOOQklrk5cNQ7EnvHMGnxtfCYWpaGDIEtdHgd4P4FB'
        b'V9D+CbWCSJKG2vHDcYC5E5lF6NJEtFHdpAlftWIcLIxJzMjwSXW59PUUohyMA/lkMvBzdHsyaptNG4a3xKhQB1w8xcwJego/mkhLI/DdMNQB7Z3CoOeDpjhDnIQ5jJ46'
        b'mKyKWVBD0SylnIJHJ0NxM5EvZoOcPW/2QHyPdiFtItpBZP50Bh1rSF9QSp8NwS+U26EDcxh0xzoHFMINgmB4HR/FN+3QhQx4Gr+QgU6baSuS56BTduhHJgiLNZmotUF4'
        b'fBvaiTrs0JUsBl0DcpGEL1KYeFtYCSZdyWb0MdnLsmi/QRgdg0lPckDoQydylqOd9OH6BnwCd0C7c5mgZ3KnN9IGxuHboCp0QLvzmPSpeTH4IS2emroOd0C785lx+EY+'
        b'egFdpFUPxW2VuAOaXcCsQtcK8F0QmmkDj+BDa3AHNLyQwS8MLcQP8AVhrNszV+AOaHgRk9lYlAhSMBnVEbithtjS5jKG5LnVw+iT+fgq3qOCVhczKdXFuM1A24w2BZar'
        b'oMklDDoyp0Q3SsCLWw58XAVNnscE4AvzoHV3Bam6Db8wRQWtBkF4K9pXii/W0EpS0UmrCho9n1kxff5I5BJadrcc71NBixcwofjIglSpMKB7Z0lV0NyFjKxxYT66Qgdj'
        b'5YAQ1Ab/FzFoM2peVIbP0RqWD25EbdDgMiYBPSxDR6fQUhm+VYXaOEL1eXx5sUpLl86bCyZNG8O9Q5Zj6tsjSpnaf3399ddREunSJJFknq8QC98aI6v/BUsLa9eUTGAs'
        b'RUWfyuw/hzr+e3dx3Y6UAi4tcvN7T49bfz9w44cfH1v/8vDvbVc1SAL1zz1/6tkUc3bWQp32wPmJY2ZnXpquUHwROS/1+7sffPz1V79/mHRO+1zRn16sLckP2XTsq+II'
        b'WdzqP43fNbDYGH/p+hvyCUn7k/8Yc/WdaT8qe2A+OOzdaz9aHPjX/Z8fCb75yee7Cj/5+oPhl5791YOrr8Y7Px76yhs5r+x/+EB39cGKrZfVf3w3e+bxwzOuDOUjX/rR'
        b'F79ubf7ZP75+AR1e+650cuVJ3PHyTz6cNDj/+mvq+eYjnxYNl6bsejzqxZgR697685QpHTNBhCWc3VCYBVJoAbF57QB9XoUuLgExFl9BJzOoUJCObkTEr9IkdMoE6B4+'
        b'6iDyoaNmGshloOvmJ+Tos2Uwm3eBdd6QYBe+iA46ouCR4WhDJSDHzmy8LTebqPfyyVwUvod2UTm3Cu3FV+zoclZBQiwxW+IdEmYA6DAnHBJYbM3osk7Wo1Ah6UkC8BE1'
        b'NKKo4aw0EKmWyhmE5TO8mpVyRMpQcuEs+Q3lpCAPDCZ5SQiVQMifnLWFe2rUSUAGcVb2JXqwtoEe0PQ9nvFIHUf87ANjCJq7JqILVO4QZI58SIhgOwtdkzE6vF4GNOF5'
        b'pg+Jg5gbGR+Jg+1T4tj0zRKtQpA4LKlqJrIonQXuXItGLBcljkETVUy4I4olnLg6rYmhGuhEdAc9HJeMduBzoqAK/OKu5Yu6CVI7Mcbplv/7z+U/rKg2f8h/XP5heY05'
        b'z/i6+eHt2N1ZxkD5F8X7SyLLDkSn6beEm0NyDx1//njz9S3sue0xQ85tGRfEPFgXlDP2qo6lWhJ+vBSdj+/EPXQT30jAF4Z5ZM4+cGCwgAN2h81Z6XCC0GmwmcwmG+g5'
        b'Aj6oyYisYzglKDNU6ozwmXGpHR7ue8oHeaecvLjRO+Xr/aacMGd0dFWBd8aTEnVx+Ym6hJx8BILm9pU5+bkJOaDcgIaIdqGtgXgDeohf6HP+/SXOvuffT+IkP1y3+ZcX'
        b'CBae82gXvqQy41ukh0QTP1CAN1Ak2JI9ofqchMopqWdHLmYyLLqLVzn7JLj1x+hVfy5/nU71J/A/z1hr/sAYO//D8o+ZG8X7byzaOq94f3PUlMiZ/y2Xv/P4DQfz9S8C'
        b'd13PB4WDWhJ3Loyms4vv5XiIy3l0zDGCtOcy6L2tnTqHDp/GrYLOgc+iY+JM9T7/kV3UDf/ZDxRmP0DJEs3DFuk795XfOPdR3rknL7aSCkPo3DP/9pv9JChbvW6Oz3Lv'
        b'VDGSvDM/HJ2TAVM/H4Bb8qP61GYlXQyF31Kb7W45lgtrvzUjmBkKY5uc8ZrxR9GiEL5suWDiTzb/TRGbIWoQi+qEHYLkFdL8EbnpjOX0wlsSex6UhA/cdLHhw/JPyl+r'
        b'IFbnD8vPGV8zJ6VyX0SVHTgYVRzZEbW+9kz4mIAtBWO0P1b/XsGUOpPPJk8Yt3WcIzU8dbPk3y+pD33EbPsy5I2fHBD1UXsxOoAu5uXrOUZqxx25LLrRiO8J2LEPPUSH'
        b'gXHh7UmFUyz5uL0gG12SMoOKpRNBJuqvThpUb1rpMPBOk4E3OgTMCBUwI5hjA4E/EMMHBxzBNtiLIVK3lDzsDqg1GXl4b9U3mDsIk7UN9WIMqWiHD8Z86aeYUuvP8yW1'
        b'uI1sfKHWQl1+ZglqL8wm/DUG35CVVeGdlRJxUmW+ODJRwBEp3ZKSueRmuYgnEmpQlgKeSCieSCmeSNZKezIokyrl3fBEJuDJ/LxxzLZnfgxX5bbPs0cLKBFnkDHX7AOo'
        b'2HRvSiljuVaylrUb4M5N9VvDtuk030tWS9dEH0t6rfEL10/Rsb1zNky05Rx76R+/vLU14+KwoJXFO/f85IPo5vnvcYOH2lrb4t8+9ZOLlnMfPbNgUsaw0N/89D1ZzJ0t'
        b'0V/L475KuvG7l3+Y/eqX7D8nRk7/1TkQYAi3bSqMpbYyBROKLnDoBFtqXkXRBx3BHfhBLh26Ffgh3SqdU+Agu30D5qIruWQltuH2QpYBlaBFibdxaBN6Dt+lpEmNzz4N'
        b'd1uSgPNEDJPms+gxuoD30ntL8OOncFs+ugQwDs2Dt9hMtB+19SWsyHu91RUl1VWmLhgZKWBkFOAiSCsawMhAVs1xnJKL4GzDvHgpI3gJyEhQzS2vdDqsZl8y1uNSAHwl'
        b'q8k23B9HSaUHfHD0owhfHCVvBDyDL+UWJlAEFdBzbZOMGYFOSPFBdCOjZ/41nhHlF7Jdyphl30WGCYK/gd3wc4SAn090P2L2slkRkpByHTNZ1J01mpHMTOZusryhfHX1'
        b'+OVC4VmZkglhkucz5eX6NodoYUioDGTCmbdS4fU8ddY6oXBGcCgTzXwoDWDKp6VLVguF6yOGgW5bNEZWVD4tKClYKDyzZAJTzew0wUKw/aCmRCgcG0n2WWPHctpy/fgG'
        b'0ZASOkkHatnCQK68nEufKVoDRkU9zaxmfieVJJfbpq8VFxcTOo1ZyVxTBRWVF3++SmznnBlTGQfzTmlQSHnx/lFPC4U/y4pkkplYibK8fMnxtIVC4bjiBFCotOEBReUV'
        b'J+c2CoU3pgxgtCDrMQ3l6nV5AULhS4PSYKJnPguFxSFBYt+XgFQC4xQVMLNc7Y5eJhTOXwGCIlM0mS0q1zOLY0STS+xgZjxzLY8LKV9db8oSCv/41CSmlrlWwWrLbb8Z'
        b'rRcKi+KLmGNM0dzAhvIaY47YzdpUnnmNeUejnFludsxcKxReXl3FvM5onSptuXlfurjxHLBsEKNnPjRLteVDrTGhQuFRlvCv3zUoksvzdoSPFwrf1TUxf2PKVaqQ8hX6'
        b'6AlC4f+rSQWMUTYGMeWhr2WKTG3l0NFMOvOvOI4p56zJEYzlT68PkthjAYc3f/BC6a78ApwcsvnV61/+dfeZTa9M0E9W3vnwxKDIDW9nZfEvVzz44pWk+E+awgtQymRF'
        b'5Z6Ma1Hr3rSa/7t3kz42aca8orS8l2s3Kj9mMpWBm2WK/cejI5k/Ks/pG368J3F/jkp+6Hsfrwt+7/P5l/75u+hfRCu0LxXgsl3oF9yCwzVD7mf//pUv/qtMfHVI8eii'
        b'N5aUv3r+7b9e3Pv5lvoRjfvemZt2+t7HW0tf/p8JP797+O3/DqtoGvgcm/TMlxd+1n5qyoXvT//H0uKw6PlLGzaOWf7Xp6q+aPxJoaPtjzk41T7oP6F/WTD4l4uabQc+'
        b'/Pxa3js//3HK4iXNv948cd3S+4bW3+47vGzfdsUbV94bkX30pS/3HflgzuuGU1fPH37UcufNsKJnI049DNmVGvz5tq//1vrm6LfffPqrcZYTn6fpJJQrgwR7Fe8VuXJ+'
        b'Djrtx5aH012LWHQcb8nVx2aB6MMySnQRX0A3uVX4fqqwE3wPnS4YOD0eaohjGamTxa1PRemCvoF8fnPSB3H2tVET4lthrF9mqLbWWgg5pRR4nkCBn1JKgAbDXzSVDEJY'
        b'Ld0ICaFSQiinlpINEo5uk8CvpMt/eqWRqOH5UDYQqLeStWm91BvkzlUmo82HYPfBTVjbSC+tJlVc8aHVb4d3NXQXVFdTUs0NLMwBHbsNbaeeDTtA5YfJ0cuZ6fi6HN8d'
        b'gzv8NAWZ+N9uhsRE3MaYMo5XUZM3BwoIx0s2BZRJTFJeyss2Mc1smQyu5eK1HK4V4rUCrpXitdIkJSzAzPEBfOAmJZQEuECiLAuk3itqtyKN520mu72gUi7CV/qykCmE'
        b'hQieNl7PG7NSZCTyFiUwEgUwEjllJArKSORrFb3tnHcXiGUF1O5UPQvfwK34bglDXGhGohcsgofFuz85xtrtcHV1Rc2wrSkaLkUt/cuPY94vy6mJG/6S6sOVTP73s88X'
        b'bPjp+d980vH5T16vyez4Qfjzyyd+dP2LI1fiXj+qSvk0/37qX38pr3g84cH7U/7+Yd7UJV/VDduR3Pr3le9tRh98eOAH30956eXP4tKvpSoK9S/9/LO9zv+wT90ZNmPw'
        b'93SB1KISgY6gFt/1Mx+f41aNQGeoNQc9QNdryZYg2l3p3RVE1/FhdJ0q1Hmj8W1hx5IZi44LO5aYqFxkaWbig9Opv5VQNb7/VDyHWvFRdJDKU47R6Gh8YgLo4tXoIrx6'
        b'iksuxDepJWg+j4+gNrQD78hNQDvQDgWjwifwuQgOu9DlSPoIaJfX9Oh8NmorhLWN2+N16IKUCQ6QOPAjdIM2bhZuHUBvw3PSyZMYuZKLwvfxTkHiv4nPQFPakkAmS8zG'
        b'27W1hdTkdFqCN+B7Ojo2uD2FgScSdTn5CSyjisaPcBuH78yp6i6XK/tNPTqpg8JgqDc1GgydG6TrQK6mG6NKNgIkM3IVysrF36ZgEZcTxfeEla50Sypr7XSjCnRNi2OV'
        b'W9lgJfvnvMkttztsJpPDrXbWdxou+lIv5DayhWSLZjxbX8TGZCPek7ZYL4kYDcl/fUjElsE+JKJbK72yGyv+kUVgJ6twNVMjyGNsgY51Kw3irhxcS+2mWnOns4AwXMpp'
        b'tca6Ct44IwhqIYuGaQrxwPLc+kZgVQIwmYGMFBC+OC8MLyBbPCQaD4z+Nj/A4Bn1PmoN7net1UKtCoMwg33UGdKtTj8hOZERjDxAIf/PTDySAgujG8vayRqJPvrZn8s/'
        b'LH+94sZr1Wa1+Xe1LBOu4X73lwOiyW0CajN4F+F8RliEl/Eu0QukZzXaYvcxtHW6YK2D34imgZ5J93vKY8Chw9SJ4Zwfm4vzjhwxpYSyHv18Pfx+pvHF4p6BAD0nPzoV'
        b'YKuBeH8ZDO5Ag0FwS4ZrtcGw3GmsFe7QdQKL0WZtMNkcq4T1FOO/qJJod4m3mNFurzTV1npWdXcrEWCY8Bg8QrswCpJ/MqKdUClj2NAQNUt/Oeq9MygLXbHnZetyEhLl'
        b'TOBgdK8GyGcuOuI3uSrxv30b68OV2TLJXsne4L0h8Be0N9jCmTm4En95rl3O6wnX9vFNDQGuSfh2AHBgqUkGfFuxiQEuHdDOAe+W8YE0r6J5BeTVNB9E80rIa2g+mOYD'
        b'IB9C8wNoPhDyoTQfRvMqyIfT/ECaV0M+guYH0XwQtCwQ8D2Sj9qkLNOQnvBEQhjcztI2q0HaGMIPpdJCMLw7jLxrCuaHw9uSshDa82B+RDvHJ4imDwmv5UfSvg2A50dR'
        b'WKMprFDIR9N8DM2HCW/vVexVmiV7pfyYdgmfSGULwbWcjJbGFWwO4GN5Ha0xHGqIozXE0xoG8hJKp5JAdqmkJPHJ2ECtz49YKvi7+93Ryd1SC4ibbinBwJ4QrqBSIU44'
        b'WSIaz8rOIERCEIICyOCJk+pxRNaYNSLxUFCRSAnEQ0GJh5ISD8VaJRAPodnS9/8NC9avWeQnu97isBhrLU3EQb/apDWKnbAAYzLWVxIP/66vTGkw2ox1WtKhKdo5FnjL'
        b'Rl/NnpVWoLXatEZtaoLD2VBrgkroDbPVVqe1mrtVRH5Mwvux5GW9dlb2bB2pIjZt9uzC0oJ5hoLS/FlziuFGWkGuYXZh+hxdYo/VzAMwtUaHA6pqtNTWaitM2kpr/QpY'
        b'3yaeHDwgzai02oByNFjreUt9VY+10B4YnQ5rndFhqTTW1q5K1KbVC8UWu5ZamqE+6I92BYwZD6yqe3PE4SEzPYW2i1x5jlF4hhfUDt5k6/VlkeMK74sZGKOSwoRxKRMn'
        b'atPyirLStKm6LrX22CcBkjbW2kBOZBhrexhAD1DojggRrnpucX/q8fBboS5P7rvXJ3BaoTbh+jvU5Wcg7274VBfQ0xvo7IgEYivUJ5ITD7kLcEsuPZpBDF5BQ0Hofrya'
        b'WhL+M3FH5OfcZI5JLi/YrzcxTuKNjW4sG0jNhUW4hYjWSbgVrgpLhEpKs8j+Z35+NtqPD+azDNqKTwTg2+jMs7RGlKVoSGGof0xtDrAfp54hBzBi50NztsWTUxGPQaFu'
        b'zZub1SlV4906dJ4pSVPgfYsWCzab4dzaNyXUG0j/+grRXnVsgHTyOYbud6ujFg4Uq76xwEqrnuTMJa6H5LBKHqiN0Nqk4iy8NU8OasJpOb6O9g8RnNaaA9BR+3LgcLOQ'
        b'C+8g7d890nJryUzW/joZyoVvxezIredSQtJ/veLNHYWMboiN2/7SsHcyfvjKrOqdZuPCF4Ienr+XVrDT3jD+h2/8adHaZxLvDUjef1ChvvPm/fSqTz96a+Cg/yn92YbE'
        b'ef/vZ7ve/dmfJ5wavaZk9V7Xsc0V7V998uOz6va/LM2o2v1pdcabz97Zt27Z2l+cd6398oOpw5p/cClPN97e9B+T1dDUceqx3vTVzo/afjDmi8KPXq5d/Ku0Hz+n0a97'
        b'oo9u1A767IPUiI4LSxasnVevPVQ8U9FQaJt7L7XqtGlx2P3YsVGJ1uM1mb95VKoLdWgZujP1cK0KRkeXD2r0bmdCHN6axDEDkUuqRIfQesEUcgTdx6e9O+toN24RdtfJ'
        b'1vqlcAfBKqL44I25iTn5+mzUjneQcZYwg9FN1I42S+vxbuSi9uYk6VSyS4bX40fePXio2kEECrytGp0TN5jwHh3R7YVqBuJNEnwXnaik2tccfAofpJtpeD9+TnTiE3bT'
        b'pPiRg+wsoufQARVMPdRAzhBtri707lnmQhe3C9vzmei6AjS8s3gjVRnRoflDBTsw3iqPBuRQzeXglRa8j6qjS/GpANRGm9SeRFolwy+w+EUYnBdoz8rwLQ0RNrdWp8G7'
        b'EnyQhQ6sTxDcWzfGokvkZRjpRU5YbDL8Isei3egyNeEXTUIt3XRJM9ruwA/xAQdRfhrVqIPoi+06eiRKGGOC1GfwTaguHnXI8GZ0YwZtCT6uHEerC8rLY6ElR1m0sxK1'
        b'03u56A7aCDcTp+NN+aSZt1l0sG4y7WGNNZq0MZ/4N5CNBk2VJBpdmoKuosdCL1rC8RZ41yPXaWZL0JbUDLQrh76OryvM5H09jDJ1a9WgcxJ0d2x6ltOzh6X5X9u+uorr'
        b'IAtbgL2LimyGR1JPUVInTDUnuEFIWQ2nZiM4YtxSi/6/IfAn7/LLESEcftUcqHcC4U30ACgQhOMAQZAnxND2FONRVbuI1p06QL91c51CqCTMv3ZaZ5y3Yip8E2/0EX76'
        b'wx/G+OoP3Zr+jRqf2aOZEoGnD31voY/2K8LwaL9PYuZ55SPCuUCW8LCuWJvJyCdY62tX6RIBioS3VvZXB5UaKiyVfTRosadBT6IJeJCt+oTeX7AyqmD1AXepF2583+LP'
        b'twMvWAhsOqZTY+wBuNELPNFXdvqu8ANF+DWspwUcLCujoINSpOyjLbz/QPQlVX2XhtjSPYugjzZUeduQ1B9p7Lu3Y2zf7ajxtiPhm+W4b4MWgpmHtqEP8HVe8MnzqGoC'
        b'kH1tb1pxSrW19ABzjy347uYbCV090icnuomls4lKYddauqxLu8lURw9Mgx5DNY1uL5JD1KJ6VQLqDPRojtNm1RYZV9WZ6h12bRr0oLsUHAvdhM7CiysmJqYmJut6l5PJ'
        b'j4zpbjefp2OF00+Ppo2KR2eGUW4mncmiC/hmsOUnHa8IXizl6BfEYSjL+NqfYos/LH+tgrgNcRV/Cn8l/MzSP2leWSnX7hi5f8O4Ycz3z7yREDD+4yKdlDLSBVWE34uc'
        b'cqaXV6YXhVFXwnS8C6/PXT7JI7N0EYPallJOLnt6Mm4rBSk2p/O8MdrgcJDOKDPycql8yy0trGKT8BF8uS+bl4IYmjynZUR3onXMikA2gphURUIvPlPwLY1dOZA0+DGr'
        b'3Rp/k61//fAyYXx9+A4RywDjYvvlOyTaBZ64uiFBickhWAOctQ4L6MIiEXfaReWXxgdw2Iz1dqPPOf+KVd0qInVMofaQKeX58AxUBf+MVSZbeR8qGvnpbtwUfVMK1m1n'
        b'hrJMZPLYH3B/rxzFOIl7Wh06inZ+k+6F7uWB+tWpeuXJLNs79jP0JO2G0qA/l+cAsuqLP6KujJ/wH5dLf6LL/Gzbr/Rz4mLUupkrwopONT91JGUzQdsgJu4T1b7iWh0n'
        b'bFqcGYJOCKqCj5qANqHrUmUZOucgxDEVuZb1JKYKIiragM+AmFqdKToffdMGpt3kMHhmhzJkip8hHvxcx7Aeea4pyoNF3d4p8ACjKPmUP9L24OJEn+hEX+IO1uSHvi2+'
        b'Tk59AO6vrKHxf60PAr/Fn7/0F3ETPeeJCEnr2d+KerNQTxZiLvR6s/TlbeWxuIGG0d3i5l1cVpulylJvdEC7LHxvrLDe1CiS65TElB7sGr0bc3jBYkK77PGOBECJ2mLT'
        b'cqfFJo4ID1eVDi1vqrA47D0akMjShhbYrXUeccoCHNJYa7fSCoSqhUE1m2z23s1LzkqhRbNnZQPvtSx3kvpAFIklfFZr87QKYGU7jITz9k0hum/qKguc0wmimmFdFZAd'
        b'cBJYAG9jYgsS5mZ5XTKLcUve3CxJsQ6dz9YurbDZ1lqWBjCzqoLr8DF00UmmG+3Dx0ARFi0vTYjaR3xqYECff64UuNRz7HJ8S7kAFu9NJ+E7IwPQI9yhhmnHO9BtfI74'
        b'pj2POoTQBS0L8Xa7xjk/i/iBl+IW/Xy6O9+Gzs/L0hN9dVt2Ht7KAnU6pVuJno/GZ+ZxDH4OP0YX0R11UQk+7yTCb5Yy3tMy0qwGb41FCxLmK5iidcua5OgUer7acmvm'
        b'VIl9GbzyRUBywrb7QeuTQ2b/NWytit+r5iRvLdmwcS+3f/1487KCDa/c+O/f1Cnunx4+O3okP+X3L7/ynHULf/5vSuXv0y8e+ihwzM6s9mUdWzsS/3nmuTd/tepfC+0D'
        b'312d9Kjxrfe+vONc37Q9Q5X/a9Wgt0YcVHysC6C7SwFjn4WOXYj06suqeg4fXFlIDSuaIXiLKo6cKCCEcCznIZkjUIcUX2WECAPocAS6I7iEj8wXjCEr8AmqTJfg9Xh/'
        b'7jS8z8cooA6RDByJTwvUuBVU/xaBHKNbM/wMN4PxLvHY7hSopU0UEMLRCSoj4E3oeQfxj8P38LE0akdhpX5WFHxlDt2CRhvXka3wQrydmBGC4XliScC3R9LuL0CXaogh'
        b'gVgR1gA23abyB2oXPfj65aJCiGYnifAcoxzVSeHDlKCNC1ReLdJ6ISfvQnr9ainwtIFSUi/t64vwS3we66T+RZC0Eqob7qH+65l/h/dK//0a0V+lW2oAOtYH1T/upfop'
        b'VMPqJHN9qRbfSuEkbXD2pWaf8rZhao/UbXbp7K6G+h5aQxyD6mwms1tut1TVm3h3ANBlp80GwnxGpVRsKbFbqz1kb5bAlzpjIzEulegsozarRS4lbZEBl5IBl5JSLiWj'
        b'XEq6VubDpQ70yaWEWFCC7EYJvq+i0vvuEOmLQO4973od83s39NOeC2/RV2DUSJmRqGiJ2tnGeqIPGcV7FTXAuHrkWGQPCphISeHkickpdPeJ7AzxROkEValX8N4Bn6LN'
        b'qDVWaRurTeLeFnSY9LnzCU+negNfb3X0AMZmgo7U26do07oKxeVid76B5XXXxwILKG+ZiTeiI508jzA83CLS3lL8WJ0FpcUiA2NTQ9EeciIxF3fkMDH4lAa/4MAHnDMI'
        b'5uMOdDc3MQHtQtvjcoC2+lST5a0+K6c0Vox3ANI0Pj1Mjc8B7TtJ5fOaumxmJ8MkJ680B37gsDPOCaTeufiOn3iO2rK9EnpCTn6JZ3OESOdtJQHA8zZnUmaONzXg+7iN'
        b'PgMseTs6j3fEZxNmGU/Yp5cNws0sfU5eYnZCnJzBbTr1crSrzJkCNXBW6M25SF+emUWHBYDHAvkGYUGvS8iRMU34bABqn1mnkwhxpm6g0/guAY3Oof35EkY6g0UXVwg3'
        b'x+J72nh4uR6YyI7cfOJFdYB7Nox1EuaBTkzF5+Nz8uH9HYkJdBxZJmysBB9cvNSyZ/pwmX0LPFXx6blhb9wP4tLU0qJnH9/JOLE1fuOo114bueijaMPGSxeZsP3Dryx8'
        b'cDDvs1NR7RPk94a/M/fzr55u/sXk16bsPnnpirHm9ol3/nDkgxWnjpwZ2Db7n7GNd6YlRP1qTvO0y4N1X1XnNKwasnx+w8jZiYGP/v73pQemfzbh9xfKc69Wzfv687JX'
        b'2hQ3/xJc+8+47JtLgV/TU0Hb8d5RudChwXgzy3AVbAqwwha6e6FaW0iYNdqILggM259dA+bdEVzS2orx8zDJnRw/YhFHvMTRLtFlTYU35mbnh6HzcSBEcYwStXEgObnQ'
        b'Abp1gbehF0IJ08YtEX5qlFTJ4C1UdVeh46VQOTfeExFtUo4QZOPULHQUGldInVDltUV4CzeqFJ+k9RbaCKPX4+0T0LFCIdaGHqYjSQKi1TUbFQbGPDsIta1Bh/zt+1Pw'
        b'YaPALNX/RwZ5FWGEIumg3Fzfyc3HE16uEfm4mjr/C39qejSFEyzvYb4sVaxJ5OhygUOVkmQ+SRb4s/WAb+dHKxVqWuBl+vO9XG8RJGe7cP5fj/Ll/D01s7/8Vul5oQ+e'
        b'+5qX544kzAJIKWUdXl7jZ1WXUtcgDv7YDF2EjeyB2QhhsBGLCXH2462VBgPdObCRc3x0h8EtqbBU9rqJ4VZ4TMDEhEMVYXeQn6pKxSMfuWkRfUtsnzBhA/6PNnx6Qzcb'
        b'OSkURUZqKVwopVIuHBCKYYdP4Kjg2O+U0wQOV3FEuOQC2fAI3zuhrHYEuaIBBVl8HbfY8woEsZxlAg2NTWSX8NQUPy4WKP63f9XFtYkvLZPy0jKZhSmT87IyBfwpeXlZ'
        b'AD+/LJAPKlPtle1V7g3Zy5ole0N4TTvHLwB5R+UKMUv4YD6EOu2oTUH8AD6UuiSFt3NlGsgPpPkImg+G/CCaj6T5kL0a0wAhegzIUcS3Jtg1wKzko/jBxA0JagzdqwG4'
        b'IfyQduoQTZ8bYJbxQ/lh4hNhUOdwfgR1ew6HZ4iLE3FLUpYNhLax/Ch+NFxH8NF8zCambBA/hh8L/yOpoxFTFiW+EcfHw1ODeT2fAKVD+EQ+Cf4P5ZP5FPg/zCWHmlL5'
        b'cfDMcBcD1+P5CXA9gp/IT4L7Wlo2mX8KykCD46dC2Six5mn8dCgdzc/gn4bSaLF0Jp8GpTFibhY/G3JjxFw6PwdyY8VcBp8JuVgKIYvPhmsdvc7hc+E6jl7n8flwHe8K'
        b'gOsCvhCu9S4lXBfxc+E6gV8oWk8kfAk/b1NAWSIvo7b7RW55Wh31pbrgJ/qQVS3cENyphKChINWRQHBVNiMR5wRZrHKV19Oniz+Nv3OWDSqoMzkslVri9mcUzJaVgkgJ'
        b'BURKhDoFc0jtKq21XpD7epLL3HLDCmOt0+QOMHja4JbMKS0ueDKt2uFomJKU1NjYmGiqrEg0OW3WBiP8S7I7jA57EsmbV4Ik3HmVwBsttasSV9bVuiWz84rckqzSDLck'
        b'O73YLckpWuSW5BYvcEtKMxdm6Di3TACr9ED1GqzIf69Ty1pCUjl7ICGra7gWdjXXzPLsMoldu5qrYZtBg7DpHRzPreYiGBIAtoVbDWi8huUlq9llctuS1SzxGIT32BoJ'
        b'CRvLB0TBc5FMODOJWcPWK+G+gly1MOS91YxBCvWCYgFXcl5JjXeB7xt6Uiq6OpuJM9zpa9b1hd5EdToOgqJgFOqgJX3YnoQBm0LduUoKE8anpkzyRSAe9ItsM5HbtfYG'
        b'U6XFbDHx+h6le4uD6ALA1zxuZRSyR8ETkBXUDZulwtmLfjCF3J5SzpvMRmAZXhQqB4XDUllNarcI4wRoKMIB5Oret4/IrD8ZaKmnO0SdvRkbYx/rZhPdbPJHRMj4iPDa'
        b'J5LE5OSCj76GH53CHdIVNtnlMNY2VBvdgfNJd+bYbFabW2ZvqLU4bIR4u2XOBlglNhLywLO/UUeSeqbP49mUq77rlRUCpcArIkRThZYjAk5TsIAF/d+QFzeCSbP6EBH+'
        b'7t2O9wDw7sYndMUbOnurGkzacpiVSmDitYnpwv/y8kSAQVSjfpqshRHqvVn/8kouQ6hPQM+42DOwEMaz99rM1HAqL1AJnQq30mg3UL9Lt9K0ssFaD3pqHw35j7chlXSX'
        b'3llXAbouDIQ4AtqGWmMl2Qo1OrS1JqPdoU3VJWpL7SaK5xVOS60jwVIPI2aDceTLywmaGvkaJzxIHvCvpZdNVHrKh6WhDrxhnr2nfFhqYO9zQ/X9T3uiMqUNRMYSKIxp'
        b'ZWW1sb7KpLXRogoj2QmwCvum8JRR22CzrrCQPdGKVaSwW2VkV7XBBGxiNgynDTo0y1i/jNrE7Q4rSICUHtT3a+2L697TJANtUjkZUydd6wJlISTIawuHMSVuqD3sq5Gg'
        b'2yZHtbWTZem1dgsQUbEa8hrZ1vZ1Zu2tj2JFU0jY7inlIjftYYOuT4tGhdVKIqtqzb6mEyedCr7LNPRIFRtNNliUK4AZGivI/nwvRhSvJElWXvcgJ5oCJ9mZx5fQ3uz4'
        b'BNDzicaauwBvrCcWBrw9C3KFpbE5+uwEOVMXqsSP5fg2PT2XPAHfQ234Gr41NzYngYS93RFfgG7hEyzeVpyAz3DM+ExZFTqBTlADwDOL6+2J+Tn4ubXI1SgPJdE6JYno'
        b'+RQhrvHtKhLzkUbV9dgcYgsS4nITij1158oYPkSJ7jsjncScDC2cbSexcXbl0B1BGdrBQlseBDnpmapWvCm55Bl0C7XjvaW4HT9XSkwOhSy+uRRfzKBxPSqy0QXSIhkj'
        b'WRmI9rNoPdqId9LX8QH8It5nzxJsEUvRsVx0RcoMgBajS1Y93bhAO0D9PmSPzeFVRPuVrWHxZdyinWd55tKPpPY34YlN2wKGtU+vn5Wm3vTqf37UHH1q698Sd5bMzHxu'
        b'4pwLLa8UR5ekFRetPLi/ohCtmsxWtU56LvPIAWtTRHLUgKYBH6dt3JU+e/abuyfH6u9mrj2fNvLAyfjiJ+/+T3hBxuO3T86LeWPc3YU7N9+ZfTU1qumdpMP3anYtyzVU'
        b'//u/Z6KDHyS737ePmzztx9Wn8c9tw+NLT06rSflpU8vZ+KtlxV9bfjWzY1qQq+Ht4OqGf7jH3Tn+jz/vmvb4Hx/8TxX+GuXGl40f8fFHM5SLt73++ae//dv2j75Q3I05'
        b'/er0H18/oBsgmPEPTV5NLEO5uE3BSBejDQksugyjfIDaBTLwOTY+AW+lgTzsWbhdwqgzJPKFeBc9w9qEDy1FbUnwAMtIjc4kFnWEhwnxbPajY3hjfE5+HtxB51aMZNFh'
        b'9ALeIRx9vbUUvZibnb8Wb47LVzByKac0xtPWVOFjeHcubQ957wE6MohFJ2zoJnUBnYPPj1Hh7XiDd+vE3xIzvobaWfLQQbQl3jwgURcXK0aWD8Y3JKvQ9jkUPNpTh64J'
        b'Rg5pI3qRmFGyJ4tBnPaj7fHiO1J0I7uARdfQffyA7tpIm9Bx1DbuKbwjW5+IWpPI6oI6tFopvk2ikTlo2KO9gKtXcjvXGmpPEhZbHN6BzuMHMrxxhp5usajC44WuZuPD'
        b'drJGWEbFc/ggPo4O0oAPqBXtQZdyJ+HrhQksw61g06YPotOyaApqy8Wt6EWf05HcKnwb3abjBAO9MSg3Pzc3PxG36nM9UTXiRqBNaLsMXY1cLWwwnSwMxW0F6LJeDp29'
        b'pkpn0cPCdd/CKfG7HC0cKFBEgz8ToLYgImSItqB1jCaQRl8lAhLx1Qyn/pjkCGIItQhpaKlGLA1lhZ2gpqGipNMjEK9zCj1E+F28MFnhVSpCNEPydRcbULPfecM+GwN1'
        b'EcmxZ08WGuGExr8CoYD1iXDC0W839O7NYgaR4Bc9iQSzBZ4mHnERJD8irwCLIWzKK3yJkgERE+yiSN+dA4lbAF1Eiy6CRM+CQ3d+Nq+7kGIkjNCPb3vYqJXwd7L/sYpI'
        b'IN1bZqysFjbQ60x1Vtsqul1jdtoEVmyn3+v4Zp7eVWPyF1N9fAcdRlsVqCeeJ/vc8Kj37ngIWOHZ8PDITkTiMdl9tfo+WL+E6Xn3n+4/3MskYSs+WxRYVK5Oj4oSw5zG'
        b'kjgeK2OVReXT6jgxRsTeoXeYUyO+BBScuXyhpS2AurXV4x3T7WiPNiiIY1i8nRwCOLGCfjLACnx3Z24XKaJU3FmhnBXY6jyyCb8AGDzZJvFs6qOjQES3AglqGh4yxRpq'
        b'Gf5Ohcx+lmD9oV/nt6doUHKI9J9vaEaGTAkf8Pml1evRrF2/jco5+4MJma+qViqDf/fMOxGy335SM//iJyNXXrtRVrjhD8dWzDIvPfbKkJdmBUyv3/ebX6U/GiD9/lM/'
        b'y/jdh69e/kP5Hy61v5ezqHHs5JIxmUP+3MjF/Xbt+RFvyMMMm0NnDTn6z3cnxASFlOmWxyW2Tx79nyV/2WFzvvfzPz69J3Nox753RvyweXfD0pF/PP3Zpk+fyDKtE7e/'
        b'uE+nEU5d38N38Ml4dBvv8okSOBpdEk4IdKBdWbnegZCCELQ0eL6kdtVQuouAjgwP684WdKiVcAbCFfKdlDsV4m0sbhsAjJBE+qFhflaOEk5R3ALGdrorXV+VB5SdkvVx'
        b'6BGtIQqfchD2hs6OFHcJ0KVxlDPWleBD8YXeGFIqdANdHMjhi2nA4WgH29B+qRAMCB0o4hghGtBldJHydAOPTwvMsRHtgZopczyIH1G3xFWh6AXitehljRF4Wyd3vI22'
        b'OfRUyhqMXqRiaTa0Hl0GMeG2z4hw+AbayhqSlOjUoCjKo57C7cPiyyZTTwYZI6/hhuO7+KZw8GQn4OPGbj5nz+AbUqUW7RFOHVxD+ybG6/NBCqXBxWXM6IJgtEdiS5/V'
        b'0xHz/jIxhagiULaV6su2JgoMS04ZkgY0fYE1kagYGrq5ITgraNgmjcgdxKr8PdHq/TlUHxEyOOHZTq+EzZDEQsPsEZ18aT3j9g1s1BW2n7JNaqXKNlEjiLINf8QqNphn'
        b'HRxcS5rZCHiA5/xynvPZT7gYyxNpTGIqcCLaMrfaUG81iMqw3S0xVtipst6zYu4OMXh3qwUTYw7nOWPNwbBxTYM8xpIuz/lZAr3bxGRfooWG+2/mbBmrWdobZpnENpP0'
        b'yhYHJaQXDLH+1Uc4JDy7mubJk2aJYB2Eayn5ZADtIVfwZKyXWdZZ7NCEymrKZmKAyhPDE1WNyQXMGh2AMEtdQ62l0uIwCMNtt1jr6Sy5A+atahAsTcKQCGYlt4zyZLdS'
        b'MNNabb345WoMDTYT8CqTgT4/l/O4P5KoWQT7OCmN0dA00DNkfs93m3Q6YARpeGLYpINCBsnMRTCerocKNcWS7umFTkLjOs1gwpx2+3ACOYcDoG0GwxJO/GwC42v2Eu71'
        b'jIWhtEEePBQbs4k0RkGwDIa9hxZ0xSqFgRyVN9BzQB7wGi94essriHG+0CM9a4Dl2WZuDR2Q1ewybxvYaQCdfB5JmEBOgL69hybIDYZah8FQwYkcm4E5agrytoHc+1ZN'
        b'8KIjN236t2mDyWAw99YGUw9t8Pr6e5fRKM8CWcZZtUJrgEBwJWIryZXgveQ7Lz6t6gWdoXGm5QZDDScaFQU09msgue/XQM4zSGo6SAS42mMU9Li09zUa9dDjBh+c6ARV'
        b'39NY9DUfUs98sDO+xXRUwbTbe5mOqm+LEjJqGiYoMePboARoJIbG3tpg6rIuvV7pZMQ9ZKLTJO1D2XukAsRGZjA82yMVEO55e+wn40b32ONBZHeHoRSba+Y8vWfjgZB6'
        b'O++xz3eOQF2PjQMSYeR5g2Gtl9/ASAT6kgl6uy/0q6HbQZ0nco5/w9gTqkgrbe6ZKvoD7Md4RHYdD4FGJXzH8bA7KwyGLb2OB73d83hoaPNUnSNS3f8RodW29Twi/iD9'
        b'RoTYXrwkSuNgKDmCfHh3HCEbBm5NgdWRDYzZRE4Lmfi+xqaXYzEGQ50TEHa7L8GS+g8RfaBfKCMO0Nl+DBCtdG/PA+QP0G+ApvkOkLY78gzxDtmQLkMmfnCPoFJSP1Cp'
        b'5+FSGQwOm9PEW1YYDPs4z0kiSuMDORi0UG8nvI99t34M9vZjcK/94JK+e0fUwEBrrVYbbeLRHnoS5u1J53PfrSsR3q5E9NQVgd3EfOeeKGh8IIPhbA+d8MFhqy8VkjI+'
        b'mw5FTHexQGi/g/SA7KpDWzuvl3BruDUSsR+SZtIjiXBl9vSJUHC3HMYMwIIGQTt21b930s7euWWN1dZaE3EVrjNa6nlTb7JyoMEg1GkwXOXE1ScKGBw56t00wNtfz3M9'
        b'y8dEHBXYnopOTXOP0k5vHJDGVasyGO72KIfSW98ENrATbPW3ANtgtRsM93sES2/1DDacgnUIIFkvCRX3XFv956UP6KD0GQyPeoROb/VLxNjUDxFDQfbQQW56qUdY9Fa/'
        b'YJn7ASuALnAjVPl9H2ghvquf3LQ5mC5mXu/6IeufrJhljC3EARo19UVheQkvJXxrENFKyUohOio5xiisHXHF0EbKCj4ilT4ZRbegLfVV2gZro7CJnZIs+HI4GxqsJAbQ'
        b'Ey450c2mwOpp8kybW7ncaax3WJpMvgvLrYCaqiwO0NVNKxs8immvphAYBQrcYHi1k4woadBQje9oiA8BvhIrpuAkILdVketqklhIUkMScl7HVkuHnMwBGT5dUhenRdsS'
        b'Eba91uogccdWkrzG38QOebPZVOmwrBBiTAPprjXaHQbBmOyWGpy2Whv5ppFtG0k63R+9OO1Weg0XKmq9FTaKqe2fqvC2rSShVGo3SchX/GzPk2Q/SUhoadsLJDlEkiMk'
        b'OUoSIgjZTpDkFElOk4Twfts5klwgySWSkHinthskIV/gsd0kyS2S3CbJHZI89syHLvT/H3fKLv4sRkheJ/seJFqqUiFlpZyU9fkFeho+sJsHpYRjtbHwN1Kt0KjUEqVE'
        b'KVVKNXLhv1qilinpHynRKOlvAJSKv9SnHB9Bt+Vkm6yd+Fai4+ggyygjOSfeh1v9vCs9Z0Xs73TxrvQEUjVLaUhXJQ0HR0O6kqBwYjg4Gr6VD6B5BQ0PJ6Ph4RRiODg1'
        b'zQfRfAANDyej4eEUYji4EJofQPMqGh5ORn0xFWI4uHCaH0jzQTQ8nIyGh1NQX00ZH0nzUTRPQsANpvkhNB9iIl6XJD+M5knIt+E0P4LmScg3Lc2PpPkwGhJORkPCkXw4'
        b'DQknoyHhSH4g5MfQ/Fiaj4B8LM3raH4QDQAnowHgSD4S8nqaT6D5KMgn0nwSzQ+GfDLNp9D8EMin0vw4mh8K+fE0P4Hmh0F+Is1PovnhPj6cI0QfTi313mTKRorem6P4'
        b'mZQDpbmDycGceZ1HWd+/1nXjy3P60+chMTZdl8eIuwj1Xak01hOqWWESXfIcFrrt5PEwocHQPM56xMlE2N8x+e9Eiftf/k4lRJnzOXdbTmi0UThbxFsrnUQL8dbsV5vV'
        b'5qnQ4hDsgcKrnu2k2Wn589LFGsp78ST0y2SbRQ8Zo7aCWi+hOmEX0PdcsF4A6emr6CfqsJnIgPjVZ7RTt1TSOOq3sgJqMtbWap1EHqtdRbiS34Fjv5e93JiomIS+EMu+'
        b'vZoljFENcg9hj1FMC7cswDbYwyId1GgLzFHCAzs0CKmUpjKaymmqoKmSpgE0DQRBlfxX0ZyapkE01ZhJGkyvQ2g6gKahNA2jaThNB9I0gqaDaBpJ0yiaDqbpEJoOpekw'
        b'mg6n6QheAqmWZyEdSUtGraxezdWMbmbSmWeWgHgsXSNbLa2J5qXN7E7WrgFBQDqIWSOtH0xLZaTUFsvLQQSIWS0lxtA1UscYEAmkzRw8P9MB63i1VDBbO2JJ+WpZs4Rl'
        b'ln+2gGkB2DWaFpY+WeHQbYRWUKlKWWC7S4SICcIS6LZg+l4SGW7W4OYMhicyQ4w9xv4kpuv71Ubi0tXpFSaYjePc6mIQDCx1oqelXNgNFSKTSgwW3i0zOE0OG4k1I5yk'
        b'cAcL8cq9p+hsRHyyPU2SNJKQo8FCJJZ8Kgz4H7gE0VDY9oYaG5w2EHpNAIIKAgq6g+AwuuWGOnsVBb2MHESUGUzCP3osMcjzGv3SFrxUWU22bGkgXKPDaQdpxGYi5n1j'
        b'LQmVVG+2QovpkFrMlkrqbg0CiEAwvLeNdY7ODrnDDbXWSmOt/5F/En64mmw026F9dMFCNfS/EJbYPdTQZchB0IXFKD4rg+s6uzsQGmlz2IkTORWl3AqYFzInbk2aZ2aE'
        b'mVDYTQ7xht1uspEK6Q2Q1qjzA/0Qp3xZI/muuE/YhDrmm4M20Nl9j4iJZVRMDKXuHV3DbCm7lfTyywn/Q6lhiuypEXMxiTnfNKjLiPQ74rNohvkZ06cLa6jE41kb2RWQ'
        b'18V22jzqRlG/rPPYp14Iw+CwisdjiccjD1TbYl4FtNiHRvbb41a0uk7ru7kDPc19MsY/ChfxOqizOjpP5dIgpP2PRPV033AjvXD9w291B0uinvYbalrfUIf499Y3+FYX'
        b'sGII0v4GWPqGuFvDvXB1PcTd+t+BTu8b9Egv6F+naYXAs3ZnhXhshLrUE3ii748Y5qnPdlHJSaiIbq4SQacBXiNCCo2K00PgqERtSWeZ2WIiAEWpAWqHBzo9g7y8wK6N'
        b'E8cpTg+XFgf97wnRFUe3UuOESFlx/caP/L4HK9Y7WOO7x0npBT/TZi1IS4JkTv+x9O2+WxHvbcU0v3P7JCCJqcL/BH/X1swunpOelD5n1rz+Bwf7ed+tSfS2ppjOvA/7'
        b'Fn3FPOcDujgxJWrTadwUwWWrttG4yi4eYtfWm6qMRPXu94j9ou82pnrbGOdBco8blk9zRR6tjS2Zv6Cs/7P1y75hT/DCHkvJutW6jIi1wjF8kHYbGqzkWBZIRU7h4H6/'
        b'Ab/TN+DJXsDB87wnbb4VgF/1DWCqP9Wqg3VqrDL5IF9D9So7ccLTFqVlF8C6ru0HaNF65u4b9Az/Qe0EWWut8oeojc0tnpPR/9n8dd+A07yABefDej7BYU2Af52sWhs7'
        b'p38QxfX1m74hpnshDusxIIQ2Nr9/4MSR/W3f4DK94EYK3pUgDtaToyji4hDCchSVFhf1H+S7fYPM8YIMpfSMysbimZp+w3i/bxj5nRSgK5Ui8jRxByLXsbMKC3OzCzLn'
        b'zVnYHwopiny/7xt2kRf2X7vC9pfxE7UZQBEyTdCaeir/2b3adk8h4YFQLcjOmEcCu+u1mfNn67VFxdn5aQWF89L0WtKD3DmLdHrqYJRBUKVarLO32tIL82HVCNVlpOVn'
        b'5y0SrktKZ/lm5xWnFZSkzZ6XXUifBQjUAtBosRP32oZaI4l3JQQL6e/k/aHvAZzvHcBRPuRbUIcEhDTSBWi0wxj2d6G/1zfMRV6YE7tOmqCzJWrTOs+/ZRdkFMLwpxdk'
        b'EppOkKjfyPO7vtuxxNuOQfMoPxfURJg8nmCNtR8rRAT0//oGZOik5mIAF3qeUgBj6rT4+Ooa/Z3fD/oGXeFP4jpJG/Ey1xIjVRfmQXZEvDsh80Vw9gLqlxdJdwypv1fD'
        b'UHItnLUlOx/wJ22G1ECel1E/Phl500DTGmIaUTSzrA99fjK1WPDCJmYqr/wiCFOdBrOeha1EndL2U9LFZ0jSJawztTUQD0Mb+QaoZ9t+MtPTZpGKfG9NrNQkEV0kGNBg'
        b'I6mPHvEObRrSVZn0eafnWSJGM97jCTZP2AXoeYrIroNV0rlN1U1x9frfdN0e8/M4smnoFhlDdnWrfDx/OBvZiHJLieGhFx88pWiWMJChET1K6JmNHpoiPNhzn8P9mkKi'
        b'8PKsuK9P7VietsjouPXuEFhrqjcYGru0pQfDAX2uQDe6px0oatCge0ZuTRfj1GQv1nQizFIPrriD/G1TctE0pRA5NP2UrlsumqVkglVKSo1SUmKTopFJ3Go/g5RctEdJ'
        b'qW1J08XypPI1PMlFi5Wy02AlGIs0/gYpm4oVUcdGvmxlIx+J6n8AN9urkPyEWHvIRpdSLeVCU/sRa0PWPfrGt4zW0T2V9h3dQx2olChl9Kv1aCPagHepVgQ1qHU5eFt8'
        b'QV4i8XjHOwagcxImrlqGruFmu99+k8fx2E72IDv3m3huE0M/Gijhpd6PBsrEazn9gKBwreAVvBKeVbo4Myt8LLAsgFfxaigLpLFsOT6I10Cpij5BIn0oy9RClI+yID6M'
        b'Yn+4O6wL7uZZQI32bIZJfVczORJJqKmBemIYWLKnbOCqSPwCCe8l+VIqwLsDvN/ohcs6K2+sJV9yG9XV6EigGXx3OOweR40Ilm6keipReuroSqLI/ut6ideZSvy03NAe'
        b'4PT/pPymfmkiW7z2vB6hfctPuNlGsX1Cc3mg9Zfzju67vpYe6/NzNPN4cHQ6jZAInbbo3ism632rD7/obRq6E+reXCpECcYHZjcuSQlMuw/UrhxRhEpJ8jdwxE394Yg7'
        b'v7mHIlf0LHI//60CptP/yR7qAMDieQHqv7VMYh8vni+Q0GtyJV0msU1zyISNLMjLaxTEA5D1OKdJCp4k+MqpdSScQEVnfIaxXVo51v9x3moSDtAL5xJozBjPcT1K4kGe'
        b'afcsSuGD7THkagxJqGMImR/gRw0NoA97DiSofEDQR3vxspIYeX6PV7gRY3ep6f9unJUOLzzfM+4EirjjdcbxncnueEO+iXjIZy6jegLWXY7yOlSH0zUi0OzVTDrT7PHj'
        b'lRT4yaveF8gxCUIvn1GTkyFEDNnFLacu4B63c/IJP4/zHfmUnZt1dFtjkBzztFrONCX01GqH1WGsBRJENobsM+CCUHVrXcMM8q0Mu7OuFwFHRt87+k1jQp8q0Gm6Cjed'
        b'vjAUUTpxpFMOoGJBPCuOvi3RKxv0EQtlJDy0RiIOOPBcufBRQKWEeIQQjw8aPCAXrUfbe2DBuAO36gFOOr6swPfR2Tzchu74seII8b99O+vHimFi6a/kkKxMQlw+iMMH'
        b'+QYgH0gYLfnaH68hjJUfcEhTRr7bKwOmG8qHAaOV0UO4ShIWyxXqijIr+HB+IJTLTQo+gh8kfutXwUeSaxI2izqGKPghND+U5gMhP4zmh9O8CvIjaF5L82rIj6T5UTQf'
        b'BPnRNB9N8xrIx9D8GJoPFlpklvBj+VhoS4hJYWZMIc3MdrYsBO6FQut1fBzcGQA9Yfl4Xg/XofQ6gU+E6zD+KTHoF4k60vm1RA30M4T2NMwV7hroinANckWaB9IgXAFl'
        b'4XsVeyP41HaWn0KgwGhIaBguEnhsIPmyID8R7k2lcCbxk2l5BD+OLqVpbjXBQI+rgpstcrOFOpmby5zl5rLnuLk5JfB/npubneWWzMoscEvSc3PdksxZRW5JdglcZRVD'
        b'Mjsrwy0pKISrojx4pLgQkpI55EZZLnUkgzeyi3QaNzcr082l59pSCT3jsqHurGI3l5ft5goK3VxRnpsrhv8lc2wT6QOzy+CBUmhMtnfBe2KgU48E8dsCQgwvqTcCurTX'
        b'COiMh3744mf3mP7SAmcmXM+ZjJ9XJc0HnHfg1sJE3J5PQo92BhylgT4Ts+kxxjx9dv7cLFgKOeQYKDovZWbgjcHoJro/0NIatkFmJxtVcXWb/jx7S/nH5a/9KTY01phl'
        b'rDXXVuiNr1d8XF5DPoaaJ2FM2fIDB6rFD5rjq+hKmQqd12c58TbUKh6nHIBflKDL6L6WHnBtxHvRKUw+YpWTj5/HNxJJ3IGD3EpeKYSvvIWuoL1dPo4cgR8P4LArOUGg'
        b'Df3ZIOY8FNl7qFL4nUy8CpvCfZHI/3vDss4NattnJOn5+xMS4Ylo72NeyDcIaSK+Zsx6v9+3/IL699iCSqU4xQSc/9crlRRrAsWPeAvLTAj10/n1SmVLAGBSAGCSkmJS'
        b'AMUk5dqAnj59K2V6CoQ7pMBJogmhg+gR2pPriUEImJOQkEgC1tJor2SCS4sa0Sa8C1/KIioN3t6gwjvxA7SLvj4XZn9j59uAZoUJ88XT3Dmz8RbcDrR4R+6CWNy6QAno'
        b'KmXQPXRVFSRdR0+Ub9PKx3/CCR/xe79pGUMDs6CWJLTeTs+TVwfSE+XoNDpPn1eXKKMHcFqGKS/XjynKYmh8d2NmuV+sWv+z5QpmUU1BiWJVGjpIYy6Go/X4cW52fi6+'
        b'jXfrcbuOZVQFHD6TPslJY2HcwYfQ1vgschAd7xmXnIzbYtCm8lxmFLolQY9YvM9JPnUbgc7GxEOv8XV0JwuWX6nPMfbYxIRY3JIUR2LzWnVK3FHE035VDscXcnFbdl4S'
        b'vot3yxn5IE4zzUyD4+DD6Igjnox2wlx0DG6hF7mJ+FG0k2yZq/DBGfHCTOBzoT3BmRtLA64XxRaQs9HtaHOWhBmONgdBZzZqnGRt4AP2ZfYV+IaUYUfHowMM3hHR5CQB'
        b'sfG1Neio7xccG9ah3fDgvFiYuja9Pr9UiJUvHNvvDFWJT0nUeAdqxy1OIhbG6kpyxeDyeGtegpwJWzA2U4IPW3C7gGbn0E18MV5oH4xWQmco/85uxOPbcwkcDm3lGHQL'
        b'PVZNWBFCm786Cbegq4l4z1zINDH56AjMA6ABY0a38FFg9NcbV+CbqLUR33DImSC8EV0fwqEDmZNoMOUZ6BA+aYdb88k3BGJzEmDagRpSWMWxnjZNX1wE7UZ78N1ABm8p'
        b'chJxZhG+Rc6ww0igaxrygYMkvKMkNhbIXUtSQanvVwRABjkfAKg7wTkS3ps5RqMC/Lppx3eWj5uN2htt6uX4NsMMGieBtXQK76YuqtEZ+AhuI180SUiEoZUxoSao5jkJ'
        b'uqJyUnTfNUgWXcPRD1HqJ9bFMzTgwlD8sAltwQ/opyXpdyXR5eGW6oHhnJ18tAn/9p3CZ0uLswvwzJBPoqytf7nE29/5Uv7G6o2/wccHfn/hqF3DRmre2DygOPP3IZ+H'
        b'HPl+2Epm7A/fGPXH4nG/fab0t9Nvv50esOhw44Lv//BCY8wPY3P/zZ9etOD6vvdy+aF/OPH7lOtfHg+r+OXH7WOdn1+qSHJ+cX7lK3fCS/6hPJ307vo45/51ra/WX+hY'
        b'cFc6NPrm6j+4X/jhh293fG/owYajwZfLLs7643sNF3Pv2uP3Ln/qUPOdX4QefOF0vn758ck5sUE3RjQMyJ38S9enZ94Iuhjx+MOwV26e/iT4/2PvO8CiutKw750Zhl5E'
        b'RMWGBWXoYMeOonSUZpc2gCgCMgyIFRSkgwUUkWLDggWUZkHdfF92kxg3fTdZ05ONKZtN3U3f5D9lZuhosrv/8z//szHCOPfec08/X33fmocvXsxzCXo3KTwj06PwsDzO'
        b'7I323DfcV7y7Sp36QfLJ0HH/VExzX7dV+vWnbg3Xn3b6/frpDkftNs3b+u2Dnzf8qDB9uVW55gNryz8+cJ2/MuFk9phPp/ncu16869TIzpzbRS82pTa//P6MJ4tNy+dP'
        b'VPyz8LvfXd34zux97rcshm8rbGp9f/28o9v+FfZe6SzLqtcvbyh5duXvjpc6/awXNjnAPKz+F6nd7MIHR55VTOSnYWkW3OKnofYknEPWODsM86CeYSVEws25ZEFBmauT'
        b'hJE0GUOTBBuCRzHSxhVTIbsLmuAQ3ujCcp4tcPiCS7u2Q3GmmalRGrapsD3dFJvhsFyw2ioNhbsJDO4ZOqA+yZ+B/yyEOxniolgFh3suxioKCh4wU68bv1NGEoMpgsNw'
        b'GZsZISfd884rsIDV7ooET0M1HuT0DrVwdT4Um2dgeyq22cIptalcMB4u2YgnXTiA07URcJixT6RDhwbpghwaVexpT3dfRg1BiSHmwx0dNwQUaHCq3TLs/Sn3g2Qi5meJ'
        b'c8n0bmOlisvVZG8qguJZZLMgFZfNFuEq1O/W4BHBBbysoaYiFby8QXQdtS2dqgRYNFKlyjDZqsYOc7I+SswNTI2w2TyDrERsz4SLULaV1D9QJocbsyxZYaugYZijM5YG'
        b'uJsQrUO+WsRLpnidN60OO4yw2AcuE2EDGvDuLnEp1OJJhp0Ug5fmUFaLYrjkEwjkrKOY8c2YR+lK22SZUaT/6PjOgebFjPyCtOMOlJFjIIBIOwsleMQFT7E74KpegIbU'
        b'k24H+nCA7gjWATJTCZbxUezEnEwodqXzbMZSPUEeJZkALbCfP56L+XCOXCXbGfmcQ7c0PcE4WIKVBqkaQBFod9IQhQVjofEOLCcvIiemXBiHDTJsGb6RiW16E7bo6MTM'
        b'4aaOTyxtE6/FcTy7kYF4lQbI4DzpK1/JcDjjwyapERxmtKak4KCAYEbdOgJOi4IN1si2GljyqXTJn0ys4mB+lmRjNTtPzEKlgUPmcsEwG48joxV1hrKVRKLwl5LpWCTB'
        b'c6RpxzlORyse14dD0ETu8nPyJUKCYDBLEgMH8HA6FdS2uehpr0CBhgoVSqHC11kiONjrYc40aGKTfy4eSCd3BjlBoSteg3OarV2PdEmHnp6+ilVofDCRkmh1dFAtlqvw'
        b'EFyRkrl52yydGuyXQzMU0vXRQyInX5W79lRKHeEiXifHTOlEI3Lutriw6bpm0jD2LF7Aqj7Pk0leEKCQCwGCPlyDvPh0ml0/28YPD8IJHSvtIJS0IXCSs/NeCZmsmR/s'
        b'djwzkjwhJ0qwFO/ivqX9C9v/eZZVZixgQntyX6F9npFoQIlVJTJxBMU9Jb+txRESE1HGNX8asSmxYrjaNhTIi3ymGXkmEiMpEbol8m7xodRHJu/2L2YeHtZLGOd2Ya4P'
        b'GGnymbQBxDJqQUuj0zqNEqQ+MI6NTtfFAstVsRvjtsT1Rl7RfzwctGBRU2jaCvqDFcJeFEL/yQw0y8Xu/dUxgKrxbA+u1v5b97jcMfqRvE2DgbHqLN89X/XYJm+NiTp0'
        b'cBP1DzrnsD2jNtEmPPD62WpAUXpRwf4a0NkHxpGa0KXIQely/qWriFN/4U6Jqq66/RYOTuoqHuTtVHPjbx8bxuKcaJTTb2KizdWOcKw6PSU+fpB3SnXvZPSn5H5n8oAt'
        b'jbzvirei9WCxyr+Fj/YRMQlyXQUcWExCYrwmCGELDfogPR6XTPNGlL/l3Q9MIrut4UEqYairBIuIotEQCRQfThcu+BvarRy83Sa6V04ZGOe454s172WbqQ4LkFpmddjx'
        b'3Fog0DyWXeJ2+U7miqfwwKKwW9gtrupyI/QoTOex0FkLDLoM29Lub3Nib4sXH5/T9V212A/eIP2vB4dQz7gKla1qY4o6ScnoXePSGNq4bXRCNI3G6LcsHRHT4qS4aBqX'
        b'ZLuEJaDQQdQg5bJgPg1wuCaqJ7F/pF0NpnhUVFiaOi4qipPPxtk6bE5JTk+JpYS0DrZJiTFp0aRwGrmlxeQdkB0wvc9qpsD5Ghc/ByTkEWFZ3QKtHg2uHhW1NDpJRWrY'
        b'FwqQ5U4J3f4T+wyxNCjR2MZLqqI65tFvtv8t6ukYA9Nv4t+5T2SrIrFj3S8KkSG3QZMKb3cXJKgUgXd3c0HCCc9pfS+9vD2y+IQ4joDG2C/39PozdvukHkeKKjYpkvVt'
        b'lzODFjAQY6yoRdzsQjajiPoWMo3/ute5mS18ZdLt5FRTyxu2T4A8454SHB50ZO1cAlc1TaX0hESUKwwm6pIC2vGwP1O4iMzfYeqGBfr/Ia7ZPlY87drsYw+mpE+riap1'
        b'sbcwSE0shQEOfk5YGweNYdxoRL8LDmC0UReh0Hg2ng9PjJEuElXUmfNl0YK/RblYfhx1P+adaHtLRXQAswN/GvVRVHL8p1FFCX7RBmxCfNx5vNNgwmQXhTSdWsPgMBbh'
        b'Ufr+1PBHiaOGWMvUEQeil1V2kRqq1VjSA5w3AVrYdBsrJ1otUXo6tvSYcBqxNR/PPJalmMw+lWb2Wfc3+8Yz4tdHz0BSiPZ9XZD+g1LAdt3GJmUUmZQ2A07Kj7pbjhlR'
        b'mTvmDR9gTk5OGnBKOgbRKXl1lOlcPWxXSLgJsGJOKJ+rMnMRr6+FczucmF1yIey34E/Ipoo+RI1sIZpQfuLVMy4SxuU6bfvUzQk+sQFkNmx693zcxoQvcWNCUoJfbFB0'
        b'ULT41cjNIzaNCF31oZve1NSzovB7B8PIt29p3ZrdzegDjo2hrqcHHiBrEyML2Xbr/gdI+7aBB6J7QjoZAfMBR+Bri+4C9QDv+w8wnPc5d/tf32RTNmp5S1BRC9LXHU1/'
        b'IyvxfsxG5pGZQ6TkoV9I4E9LycY8m23MeHtevzooVGNebz1Up4MeH9VnsHqFWAy8adv38W6wWIsB9uiBWL3pO8YPOCLvmg3mTekZ2/FbZZN+R6PvESkLCksMK/HRU9Gv'
        b'0z9d4B9tEq+qfCdAX5DZi4p7K7rkur4xB/XCYB3p2Ed344Ekj3/a0fInDdiJb5kMpif2CuX8d3rxMc4sMqfFCWESFTVb3Zs1xTGast3fj9kUv/Gzi2xm6wu2f5fWrY0j'
        b'pwuj2rs11YacLQ1ZTtR8I1soQttSOMGn/BUvqBrU7DIf9/We8XANmpkpKxBvOzlCuYzZXZ3lggHeksDB9eEDjKDpoEvBpa/2zcNXH3sEaflTBhzB1wcdQc27aPV6uBZH'
        b'a3s/RmCuReq5N2HqgdZ3L8kfwgSTHh78fL38kczlaJM/Kn90/Gid29F4ULdjDwc2jeey6jP4HkGMPgFPYUemPxZvD/MNcOWuMCyBC8ynszIdDhqnYRu2mW+lBlvq0omF'
        b'Bgs4I8GbeHmhmhpEsHpiCHPp+JDBc4Z9wXBpYNcOdezg/m3G0Eb2wk7uRZGtUFGPDB7yEPCAACWQCxfZcYjZcHcdtqjlghtWC1gvwMEJeJc9hGfwEtwyxnY9QTFRwDYB'
        b'TqqWsyvQ6rdalU6EqmMbBCwQYD/cgCpOFFEbCDnGpAPgJnYI2CRAFV6GYjWdRMapUapMiTBVTaohQBGpOnP7LN6oL1yaMpp6RQNcJkcKnEDTCzqpo0tGYf6PCXhagCOQ'
        b'Q1ozk/bxxiGsM3p1ADan40nITsPWUB9HIqKVs56AA1BluAsr4Rj3PZ7BXCyZigemuvlAtkwQSZMxe/gqxgWKrQ4GPZyrWkCVFctXYuVUv1B9vA77hHCskmMb1JB+ou3S'
        b'H4Xl1H3mjg2rBXc4i6eZBLIQK/Ak0ogv10jIFlyxHW6xBr81Wk9o9R7G/Fw/ZhkL6iW047KxcY6/7n1Y4ENGpppxgJe6+oXbYyGpTKi9AstX+vhSKagkkIk/IbSN8mTT'
        b'9VDmwPynGW7baVRE97sifOAObQoRmlyDNZ3V3W9M58tFuGWC14ZaqWkYts3CRFNKNmIK2W4GepgdjnVyLAszXWppYzA3BG7BbazDJu+EbYbxw7caYac80wCKDINhf5QJ'
        b'jQDGM254e4diHBbMccFqORxdrICW+dPw2AioMsAyNTUZ4EG4FqCHOZhjKrgbSKE5HK6twUo5FBKRrNIBcvE2lkNZ2KjE3XAes0fB7U0TRkGHFdwlkzcP2uN3YK7U3Z7U'
        b'o3QcXl0yNHCiEdsPWA8/v9JGFExSZIJF1LzNZqGCmu6eWDEfyjjLLJzBRg3TrIZmtsvL2Y1p9gp2GMfuns6K/MLTV3CbMFEUoqIcIs0nC2oK74YnRuBh2ohjhoKtCfkQ'
        b'sWEzHIJLZOGeFN1hLzbMmUoG43AUtOElGR7G6vApeHoNqXT2sDDYGwcFlNLjuv5G6LTIwrxZakptgM0WRL/RsOGqgrrX0sfZT89yGA1rgQsK8j9dRRcNsQOqN4UpRLad'
        b'YK6NNR1/ciZgma8T2RLoGmiFzuEGMjc8vospUENwH7T5a0lzByLMJbvH0W6kuUUKk0SswhvqaXz4OvEm8xVTRzGcpR6FQZ3F2xNJDRk1Dimkhcr0IpzDu4IEysTFcAgb'
        b'mVYKlXCDlOtD+rAkkC8EVz9f5xAem9EnEsBn93ai66XSzWB5iHOERMgKM88ydGMzbBvuxxzupvddoQnSwLKha5iy6BMQzNrsssIgg/rh/QKDnJyDwjnjcLfwALYdY0nI'
        b'EGiA2ylsJtw0kgpO0+hxE+VUnz6FnGos0gJqsW29v4szFkrJ/uwvJedrswQKPOG8OoRevkUGNjRYEchx6cNXdgs92YSHtNEnlMunkewFhaRHStbZEq31OpzxGQ93fcZP'
        b'hSaZgNcwxxKOESXxBHO9Qw2UeJGNssXc0ACvmWNL+la1KFippHALm4PX4EG2ya+WTgyl+5clHJGSHe8SJUA6s0BNDXHQtGOyv8KZKc9BpF72PQVnaagorLc1gL0q3MtG'
        b'bzZZ+wWhUBqGpTa+lGZIz0GE6h167D3q+VhunGEmjsBy8pojZFfBbLzO6ZIvpRJdrYUGCbQY+OgLErwsOqdAlWIIpyeKIHpYcQBR43LJ0plFCYebMJsFW2TBSTymC7rx'
        b'ghZRMF4jwSvucINdh4NwDi6Th0nFTaBM6+8l58Z1tg9PNHFkXlM4N1aQbBBdoQ728lOZnBelPCIBGsfoCbKxIpzSm6jmWP9Ys1ob4wGNYpxMMLGQDhs/VE2ZXrEglkxh'
        b'LFWwTip1DaSA/dyZqSdMhmy9eDgyks0KrFyxmO/qIzOZ588AqyRkkjfOZa8hx/CBUEfNojHBUj3BJEFqvgIOsponLMWrlKpAEqRhKsAGNat5Il53x2JnbIG6ICwnvSZf'
        b'Lxk2Zhc/4Irg8Bospo7Zq9goFWQzRLJdXJnMulkVjTfouoejcFbKGnx6PB5gZW7Di8GMSDsKyjVk1mQDPsxmGbZCJZ6i9fSk/MuuQWQS0wWuJ4yHw3qGkUksSig6FqhV'
        b'hinmdDsoVdhNYdaO7r0TBDn6eABrYR+fFpXTHaizfClcVZCNynC2hCy049CgkDNBI3DuCCa3QAXc4IILXglhLRmalc6kFjgNJ7jYQo4lPttxfwjsZ2IL1pODlwkuizxZ'
        b'j0ZkYgMVXLxwHxdcrEkLaetHwUmN3FKN5zVySx7UcjmoHZsXUMllZpRGcjkBJUnf/fLLL+tD9YTsuVb0JA+oWxYqsC8NomXC3BD2pcl70wOExJ+Ma2Wq7eRwsr9c4R16'
        b'I3mUu4XdjfyIi+vXHrG7/NeJ81WzVx51yLv408IQWc67m07sNbb/g5/dTO/zwmmv7CLb8E9s3z7g8fa7wU/rn7k/sS3IyCXhrc4sHJmWdSbvyKQp0Lgm9fyfkhbdK/C4'
        b'4vJQ1Jv70rvLV33v+1LLGihOD9j70vObnDbp/bzH1e2eLG65c3b7paefTIqRTDzZ6lbk2fCD20wxr+HekrbsjPi9pR7LnOw7rln9aeY7a0dP/65qYu2qC6+3bokbE/Jq'
        b'blznkfCNXrUhr/ptL7s55NsA2Rxn/MT6+3lD3/r4E7OIP/91iWem53Pyza96j3rLbHjnU7eGxg071XTjqbxXjd+5ofjHvIvXQ9SdTtfjYs553FqqfGfCy0OecpF++u26'
        b'V9xNj/5+2pnoMcdXfRjxkbPjJrea0p/K3o95O0xxzyJr88bSnZV1oeeuLrsrffPrjfLPrUf+5e5rrk9+M9PdPj59Yb7jB8Gfxqc+vyxt255Z9SlHnRPEBe91fpx15tbm'
        b'8PXJnzVetfrmaOflzBrTpeVlK38Xf/TpuVtfm5xZnRb5+UsXKkNSq8fv+MZ6asCNzbV7HzoHvfrJw+rnTrx47uvKNWdfvpNQMu/9ieazf28SUt4275u80Hm/2/nZd/+o'
        b'KlycsODh4pufP3/L/DLcnnnf682fzuj/44XbQ13cmq4nH7N+b+IbrV/9a8Gm7aPxl79/43ls7DSb2J3u4WNPvDd/XvtL+9Xv3bpt/yfP80G+r2wp+8g70ul04t5q/R8s'
        b'Cv4qhHvtkc+sX/42eoLnw6effHpnQuqzQze+sS766EcxZ4ID4Fii6rNfamO3ewWvvP3AO6ht2rY31U+l//mJTx0d3ULHvva78T/cn7XWN9qzbPOhlaA+/3zgs39880zK'
        b'kh1fDl/qKVkxXq2wY4EEkdA0WxOXQWMy8MJkTVjG5iUsMMUTK0dQm5mMLChKqLUL9/JIm71j09geujWAbaGheJOFCkCJLVb05BiZMYGF8ZA1U8MZ1NrnYgOLhJuzkAVp'
        b'GECbJMMDDrLoC7kDXtNt7bg/WrO1w8VYHotyZQQR/tjOnhqg3di343EWWQGdcHsqjzEKcvbBygBtkBEcWsGfvg61ckd/uE52eR1BymrcxwM7jpAD+5Sjg4siYwkWEbXf'
        b'cDXZeiJ2pjMt5mjSREcXOGBOj0Unsr1CmcR5/TwWekLE0/N4pzuTjXnEOqyQJsFpbGPhGNgg96VhIVQII7Lh6eAuSVwujPOXYZ3VKE4o06HCKkeXGTQKiVZBDpckU/E8'
        b'NjJDwE44ha2Ozths0sWms0pgFuhlWyNVUGqw1RSvqWggoLmBKZ6GI92CfljAD7bJ4Q4eS+YBERXrZnNLKml4nc6wbOkrhROketU8Oup4CjmuuDW7nFq0g1m80RDMlxKx'
        b'+4I/j//qgKqhUOxKxtuZ8SfqC+bBeAzqpRvJ6d3JQ1byM7HSMdiJqGGUw23CcDLR8I4EO+SenA6oCavWMWnJdV6XsIRXoY5xu4XB8Un05HPDHM3Rp7ZjvR8FDfYs9AyP'
        b'mql7xGE7QQ7rNr3lcJVUbouMhuxo4nVap7LAE5Pglf1bT3jQiR6Ua+JOsBnKOanQLXKk7esd8cSjnbZAeyaRc/h9J/BEFIvBMdnQPQpHF4ETo+JxS3fGQIGji8LPUUe9'
        b'l42dkCNNgcOBrGOwGq+MJdI/Jb4j52Z5op5gnCzB49Mk3Dp0lByBN9k5PWWc5pgOn8YvNSev49KMxEsjzNhhO+/tfRnOXcIM5GdwaQbyAtOpOAMt6/CQTpzJx9N95ZmV'
        b'CWzoRxHZ/RypXVfAE1GTrkOpNe6XWW7wTqf6yzg8s7tPN4eJ/UUHaW1UW0g96bCbjYAy/wBfIlBCtSAJER024yU2ncirbsj8KZ/fUbL6ujj9iKCsMPl3AnUUo/+LsLD/'
        b'RtjQA/NekJjMFPcC+dHHFOdBLcYGjNDGgpEoWVLQNwmHezPSAL/ZkOv0KjWpUVg5CmMuI59lGrJlM/5XIteUYMDCjCwZt6CFxEhqpaFl5mByBuSKGftNg5fMSNk0ZMlI'
        b'QpOR+Z8uyFsJKUHCfvM/NOGYEvCYaMriqYU6416vZnePVeJxRCx1bCj9MZyFKcVt04U4dMvE6jI9Dvu/NnraSCdLXVIYrSGjEuKVGqoLd2IW0BjyT4cBLaCvefVgSxys'
        b'kxQiS0QLGsQZS92xIgP3fbQzVkuV+BdJP6ELi+LTKSNidFISgy7tRjRMKpVIaxOd1APRlINfKZUc2y/aNjkus0+hPOTFPipq+ZZ03+T4qCjbmKSU2M0KFw36rDYYQq2K'
        b'i1cn0YiErBS1bWY0p2lUJlJmxb4kyN0rkZjMboxnufuabM84FU8B5XiDthRFyTZRqXp8EkQKOeBp68uCEsj8UyVShFfyHhqgEG0bq1alp2zhxeqa5quMilJQQJoB4zhI'
        b'/2j7g35MTLbNmOlCubW9SDdm0s5M3xidrqttV6hIvyVq2sZgZ1lUEw/IIAVQENoeXaRNpk1IS1GnMji6fkskTU9PjFUnRafxkBNValysDklBZWtP09idSBeQ1zKAk6xU'
        b'8s+49FgXBRuEAUJOaIemx2nHRTPuLOAsuTfbpWb0lSkslTeVAhb3V2aPARiELVKb6trTcG/IDfe78BJWEVHZD2t0lns45K6mYh4cxAJ9Xd4DHMCzvTIfRmGHmsLtQRkc'
        b'mqQxddoaSHHvJGpRvbnVDStsxvoMtdu6C5tCIA8uL4aKtV6+6UTkOAnNBvOCnMZgDZ7EmiVwa9x2aLRw2437mAkKzXyFA4Lg5jY/0aF2RIDAjBLb8WYM0/tDKa9vOU2b'
        b'oclI+sKETTJSTg5eXAu57HEPZxnlx7a12Jph8oTDcCFRHhMvqtLIlZe8Pe3uXTXNXWii92LK59dGWy0cMm2h13CL9V4xYw75vuBlYBgU8Krt+hnbbRLyDr1g/ocpueZO'
        b'im+fu3djYsSb+3I7YqSni0ev/XyR8b7JzqYzR2f949XSSS7u5T8uK/rlxm6950I/GH2y7YxZyQVrk/MP9Wd9YlM7VKUw5ppEpSFc6qaaML0E8qzwCJbDfs6LXIk3lDzc'
        b'H0pkRDvBc1CRTv0BqVjxCL8YETgsJ/cQOdbgZfZiZ7laRU2+zvYag5cwJHI5HpBCMzZgFZee6mb6a3N5sDlMo8JAORQxTUJK5PQOIqcXL6Dx9Jpo+mgoYZrEitl4XBdM'
        b'fxYu7xKXEhm5lOsnB4l03ESevLmoS8KHO3q8Q447QrlGtUrHu10MjkS3ao5gwrqBtSOTTE2IUNRbOM3Eqt1ctsuHOiJWFwenTO0ZIK4TTbdDk9Y/96iwEkOazcfWKBNH'
        b'7PsTR/YIs6gIQUULImJIqdhBBY5ewQW6gnoyO1r3PLv7CTCx7nmGxpF/nqZnqG1/Z2i28LblwAEOujrQWFFytESSs0UHZaDNbx0oylBaIB0wu1XKwiBl734n6+cADY1L'
        b'1oCN9oQ3V6v4gRrHtjSy/3p7+S4O7QZZPtApFBeTGKuKjE1KJKVwOl4tjFM8hV2M3ejC7nDxpj8Xs9sGQkLvVqqmPzxZnKKTLlCRwvOq4lg1U9KU9Auyv/e7/2qQ3Qes'
        b'g8vS8IAoBt2mTk1KiVZqW6/tkH4LpRigOig2ejRognRV6sR0jq+uq1T/p8Ija7V4cViU0299NPw3P+q7/Lc+umjVmt/81iVLfvujXr/10VXeHr/90alRtgPITo/x8LQB'
        b'QkV94zkbDJdk4pROtg6a6e/QI960Z0Asi5LrX/QYKMx1aVo0Q7rumsO/JqJ1JRVW+a6QMdXFrcdqYZG4HGGWLyfywozE6N/WU15h4f1UoYuum+4xvB58uSUqB5GvZEJ/'
        b'+djWnI07yESfRU4U2UU5TVvozFM+98BevKQylghYv07AEwIcWwwHmTi2Yz4RYxogB1vc3Nz0BImvgHVzsIXHJNRCpbVjkAsVD47YWIj+eB3PM/+8LCzQMchPQr7fa2Ml'
        b'zloCRcwXAPUj8KpjkC99oGAPnhPnqlYrZNwrUYidCjwOtcyzhtf0BKmNOM9tEnPpOMGFDZgH58m15nTsIAc7Vorj4TTeYfUwkISqPNIkgpgCeXiNJil2YDn3KeVhFeTj'
        b'mXgVtpuT40uCZ0UHrIRq9RBy1Wsl5OJh6RzoFARXwTVzFm/VgbVy5gFJwFOayI3yYHbFbcj60WKP+sHxRF77Nmu8mYFNPSu4fid7TA+Ppc+N7V4DJ7jE+sN7JVZpao63'
        b'sIbUfLYFz1A/6U4ErAo8ZJxhSEZQaii6DsezvA8vGi8022NsmmZO5CAnkUhA0Mx9MPVwfgueGkI9fsZmoiA1EResCVJTJEPTgEx/KpmGsvBcmmVMRFUBT8GhnUQILsFc'
        b'6IQKqAkj/6jATpo+TKTXCui01MPKGD1T8iNQMo30bclc26FEmLM0h/N2cFUh4fEndyaPwLOKHv3iTOrETNGdWOkEx3f07JehWKyQcn/gAS+86GHS41ksCmXXouFEyEbz'
        b'nk+ugk7W1j2roABb4EZX95DJcDDx0htyiepLcv21T7eHvzAvCN2s9L/4tu7laTlHzl7OffIPTyque1ubffHKE1fmrjIxCcq3mdTi7pYmmOVUVR2bLZyLeq/+zGJH1+fv'
        b'fms3p8XuWb97wWneY+JWpIVfLzvz3l9XX5PVP1Nkk7D3VUnCqYagt402e7w+YetTBzHCcc4Tt0s6h1TZ1k3+xGT7RfsXJyU+s6c8FPf94hU28YdPEz66V/nusEr1wyed'
        b'TWcs/mZMRoZS9Zr+pzun3R2VXvpZ5JKWL/a98dPy4G/eW66eGeZc07n8u32uZZNnLDczVfu0zn7T9HaOS3DH4pSTF1d8/urNT99+I2Hilvt2dm+977q2cdwv4gPX1Zee'
        b'26mwYnLzOAeV/1zM7sqi57b9u1jPLfBN0GS1bDU372uN+1iQxA1++XAuwzFsbbeAahMnqT42wU2eDXvEADq5MpABt+E80Qb2Yxm3qhelYj027mEgAnqCDHJF3Ef0uFu8'
        b'4GNSvIlHRZpo2z3LthIP8KfzRxgzYd8Pyrr8FSPwNPdmNNn4O1K7P+b4UQHaAIslkGOGHdxtUDNkg8oY20SBFG+A+wU8T7SEXF7hc+PgBhSnTifrC/O3TyOzbTTWsceS'
        b'8YKcXpGTKwVwBcqoZnB5OS/yhiW20ou0zMJZYQIeIlO/hjtATkOuH3U0QPt0jRdEk7yaOIdpTJHQkqjKIKtPhLPYZCrgcSsoZbWZEZupIltJAa3MgQVLqIO3AlrZGydg'
        b'bSR5SE+g4RnFUCyQ1XcbinkjOs0xh+wdZMsW4cqqdAFrsX4UM91mhmGnKmMrfVeV40wBS6xwH1fb9uFtrCeXyLvgSOJiMj5SCXc2tIbZ9tS9YD+WC0O49pUzgDoyWGi1'
        b'TEWEa6aaRPSvmkRRZYRaLCn5N7WXcsunhKko2j8mLH3SSKK1UOr+EpXGQNw+pGeUNHljkBZhhWVUmnQXyNPie2o0orYNiTo9Jl6X+kiJfZ4YRJl5oke0dt96kNIlgoYZ'
        b'LkgxvBds1QNZZLBv0APjyMXhISHeQYt9vUM5QqcOzuqBcWp0YrImL5IlZz4w6koc1KRx0pt75XJG94S9YihY1LjJtDPWKt5BNv8vWdjTXKnqKNUA1RnoW0jp2JtJzfRG'
        b'LJSQT48NnymxsDCRmFEqNtmMbQai1RgDHomVgdWy3rkMl6FGFGyWyRIT8ECPuGETzW+Vg9iTlk0pUbooXZVuSoMamdJQ6R4vKD3YZ2Pl1HiB/It+NqU4U8oZmu9nUpIw'
        b'9nkIpQlTzmWfrZTzKEkY+zxMuVC5SOnFPlsrhytHKEfWGFPCt3x5vKi0UY7KNaAwnBX6FaJycYVJhUGFJf2jHF2qr1ySTzG/5EQRtlWOZxhW+oxIbSLD47KjRHD0uQrj'
        b'Ckm8hDw1lPy1qLBM5P+yJKVZVhhWGMXLlN5KBSlvKcUToyXmG+ab5lvmW8UbKB2UjqxkQxarK2exu0Pi5UonpXOuAYX9lAlrjFn49bIHlnQZLGYMEQy/LT4u7QePHuJo'
        b'3xs0PGfdb/rBhci2nomqFE9VupL99nBz8/DwpCKy5zaV0pMuDRc3N3fylwjfUx/IgoJDAh/IfHyX+TyQhYcsW/5AssT7gSF9WWRwUAARJdP0BYY1R5XRB4acyiORfNSL'
        b'Jyq16te80J290DcoNOxXPjX7gSx0ScSiH7w2pqenerq6ZmZmuqgStzlT0T+N5rQ6x2oyBl1iU7a4KuNce73VhSgIbh4upGQGBZa2jG4KhgHBixcFRBIN4IfJtDqLvXzZ'
        b'u8nv5dFZdDsKoeZfVTopxMVtGvmZNp0+ZxLqG7QswDvSa1HYYp/HfNT9h5m97luclqJSeTHNo+cjASkJgaoE9qA7fdC8V1t+sBm4gj8M67fhCuMepdCB71tsry9mD1BW'
        b'769ns68Hr9XA19x/cPwVffFAXxkXH61OSmcDwYbyv5P/0F8WCVcITkNHojETRvCIMHMhXoQTWJqYt+M5Ccsvca9+muaXvHO37T7R2BSiw+tHB8kveWBAKVPTybwdOIeK'
        b'/lnGQVJ7rn4X7bOPn6xQTto1j3xSTej/ZM4Wft8jYWGwtyr0+Um6vJ/jNER7pn5MUdLCgnpkN+gGiab+s+wGQUvaySHT4o10mQtGA2YuaL17e/X7MU768gThxO1x3UyU'
        b'nH6HO4vo5jmISTJUS6hrm8pIEpgkofLse6Ozba9lZWu/xFsx+G10KT3yjtm29g6qROp5ypjpMsPhMYrkq9PWfrHPo2/WrFl6s5Pto94z8Lq2tfcN+1VPuA/yxOPuAbSI'
        b'3pUeyPqrsWBxUw/P3dYQL2mh/wd6kp52/LHe0yY1LTElLTE9i0P12jvQ85MSWtET1KF/g6ADPVfpPfToc6DWXwd6nDkoXLqcozNcPFzcPDW39F9Mlx/Vjd2qKbXr6xns'
        b'a170QA3jWBKapvWDE8H7Z4qKQUUM2D3M3+DZM/mfLbL+UR80yfsD1qkL3sFTx+faF7+BYinoXOn9eMrpf+Qa49+jBnlmCGVu/LjodDqhVFpusm5gGNSRPACCADWmknIy'
        b'o9M0Xv9u1BGsd2xD4+JoW9VJ3ejO+i1q8aIw72XBIasjKR9PcKh3JCVkCWW11HncOQnbgJ3ENyHeP4w0SYOroh03rQalMQP376DuMg0zdwMvocty69BrT3EY0MXPRiiV'
        b'r1MVp3DrtcU48NZpb0lM7h/egANlEHlSS0+7MTrZ1js8ZAATd7JtaGZi+va4tCQ2cOmDVJ5viAOsJbJgfNOjk7LYgwPvcA4Dz1kNwgcfkC7gDzrzNUOiAwHh3qYBWpTO'
        b'Ixa6YXn3eLYHfMuAuxYrqY/5n3SPRl5Saadvr3L7HxMNq2HXexmbZExcUkpyAi1pEDM5lWMM+ghPFkHMcrmZWpwO+2MZHpAKEjyNd+CCaC+FRmab9FRjNkfalAt4041l'
        b'F+ZCHjP32i2E84l4heOLcnTRuiE8c6QOq8yJfooNY1OhBDvInxYolAmmmCvBYlO4xRLyVXAeD/p3zxWL0CbhwJFZAyByBur5SYTpsI9UA6vimKHYZsTcLlMwHvEUF6jS'
        b'2QV9F+zQ2o/n43lxgRLr1MFUI04b0g1plddgURytgy5zJtXUNIRCrdo7B4Xb22MRlrhikRMF2eT4oc7UonZ0qAgN2LCUm3gL8dTmyZijAQdl0KBboJz5Iup8mC/Cwm3y'
        b'BrnlKluBJV7Os4Uj3fFCfWheRSFpq2sIFgSs8JGGQCHNq8Mb0DANarPsBLgrM8YqC9ynkHDrefVobO9mBscr4oI4Oa9NrQKatY2HTrguLoByPJG4SXFeqqojN8w/HGBX'
        b'+oQRuFksyZy55XDrPx22fVveabThyARFwZNj19rLozu/d//XwqG3nTpn3v90ie31STnjv9gYtfyJU0FHWsy/ar/XHNti5XEyZKT9M3Bs0/TThRcjppYHzg0u/fPvweza'
        b'udBhTwbvf3V90Gezt36xZ+bLseHmmVfv/s0jpfmJzcdn7U5e5rOxsnXHMyd3fpq259krnyuSs865jvKb8tWrriaHXM2ejVOYMjtuJtSvdXRxphEMWI5H5HBG4gan4RgL'
        b'Y5i3bAFeIp3DcI8pXrMTDcvQF8xCpO4B6zhC3hVy9zVtgAUchgpthEWtJ483zoMqVfew9Xq8oYlbh3w8xCLUE2eYwb50jUFYXIQ38DSr3DinOH1o6BmtLU3yWMJjLG6m'
        b'Y0v38HU4F6qJsVDDVR77cdTEdoytDiFQZ2Edw1EG/eBy7FyHLpjB3iCDUGrEw6Evu0GZDhSSTJ/IZRwTclcGDwVpgYMzu1nCR68Q4fg2rNSEiUMu1JKX0DXaSq4H2kGH'
        b'uHTIVGaTtYZ6OAC3ySrFsgDS+hjRHeoce6APGP1bdjIdgJ3nQFrWTkvRSBODStkMZMymKmN/KRGxmUQijh5AJ9KAtgX1jfMcVD0aLEbkN+DNBQ6q2rWNfaRq9+sYVx7o'
        b'RVIZeBB4rFI9LfJcf6/T0Si7PIac3Rc17oEs1GdRyAMZJUl9IKN8qVqVtGdsLY9cpYGsD/Q1JNs99FFz7XHlI+iy7blGaqLRSU05kHe+ebz5Y+TUc8J12bvn+9NMFymV'
        b'jNevG52H5mTux7ynk+n6Krjxtp5U4vSM0sGbRPXj43fSSEg69C0aMtk3wrQ31yEn9KV6fpfcm047Ll2jFTyWvqWRlHWst49SuTg9Fn+2H3LaaJVtfFJKNDU92DImVg3x'
        b'5EABNtHJPWjfenPaDlSLHnpIf6Sz6XHbuJCdruNq3cLDPQeI3yT3JCqphNjVFV3EebwNtvaMuZ02jUmAE0KWuri4TFAMILvyMAkWixxNZ1M3nmZdyZyiksvUXdf7LU/3'
        b'TBfjpGYKaEK4evJP9luGfYj3Um/qjvGODAoP9PIOcbLVqjqconPAsC8WfDwwRWtKKg/GHqSEbf1pjwPwoQ5SHP1Pp1zSHh5M99Mhwmlmdb+laYm2+1MTbUmveIcELQro'
        b'qxL2H6/8mGqiloKLd4WOqphOWM28oeuCaNZxjIc6KiooJZnuFIMEcm9L73o7o7SlfRSdRIOn6Qahm7rxaSlbSFcpoweIuE5Sc2tcQmJGXLJ25pOlqaThPvaxKcmqRNJd'
        b'tCTScYnsW9LLA1aMF9PdhqHo3kwNcXPMprjYdL4f9K81hQbPmuHmbsupZXl7aB2cNEihmvYyowJdm2RT7LeceHUaW2tstXOS2AFVR34IedqGalQ1LYE7jUnPIm9JSiKL'
        b'LzqNK2z85v73FpUqJTaRDYJOcUxNS6E87LQXSddqBpssBD7t++/MblSItkFEhYxOTU1KjGWBiFSHZ+upe4x9/2tnsYYHvotslZ7Ptvbkp8LJlp7StvbB4SEKOhj0tLa1'
        b'9/IOGmAdOnRLGpihcHiMVAZdVNci3VbfiwtpsGhRnf5q0K/+Oi6IaaGGQ201CioccWJB9MbYypQur7lyonTNmm5sG5XkMMeHB4BB8dhMVQRc7VJasSVwKYd122s9zjCQ'
        b'RUTxcKhUKOZBTyVYZ4an4QRHjeGIMeugNYz5YkOMjakrlsZt9VF1sQqq1ZSoFApCMrBYw9NA6TvCNGAI/s4OET5OfuEDUlAEhqdhEQObafIeQnSdwlTu87huLXDND25N'
        b'4TFQWG/CgqDGbsIzg70Lsxf287ouopsV9jqIDIVc8HSzwma8upN1UZreEqpTQgtc5EFZcHeumrKXQSeW2PgzqCBnv2CqVvNC9PAQNm3CPCO7kXDBqEufXYg5WEOunbKE'
        b'PDgTBieUK6DQazdUw164SP6cJr/3b95GtI+zXjEboMgrLXHFik0b0uzWwbHNGy0ELJs3GmqwETk00FK4m2yM7akm0OQqESTYKbqSq9fVYVROxouyAWqWZ4SFI6FwIRyM'
        b'oZEv3eqTh6ewgn6mgWNR5piPNeNsBbi0YsgIbIAa1hkr4CjU0MAsFVTy2CyLGDVFh3KDS246+4IiQgMYlKpWh+GBVFNzPBSm6fNuQDnU3kDngRZMRIuoAzlrsQzOG7D4'
        b'LzMssMbLUOLC0HjGroQ2HXBTX9QmPLzONYQ+F9ZjPLEN8k2XRUAtgwYasgPO+ncnOyqFS8vZnCGF+jNoEzKRDidN0lP5QZElmdtFeDiETMMiEe9uNV2G+/E4T0Q5Nxsb'
        b'+5Tk06W2QrtVRI8yIc8YKqzs8OwwOAcN1sOkAhwLHEI+QZ56LilxK+YM7weKSYInsYK8pnUuGZ29mEv6tgYrPOdCJxyKETA/xCQk0lFN4y5CpmFNNzNPgK/Cz9mlG3HJ'
        b'0M1d8E6aOpn2XC2kt2rVlnCQZsWqKfPrqvDxWhSKFT6DFN2nYMiGwj6Fh/hZQWeawAMIC6HVX0Um9O1u5iOyjttZ2A2zqllinV43Oh04OrwbnQ7k4iVKvEj/JlY9HCFV'
        b'nSTK1SjJB4Er5pW/4mbRNmZOUMbh259/YGYx/b1zL0yovbLWsNTsmYPfRDwzzOqw3DjxyrOuN8YtLD3/4r9yHRXfTLGtuy2+uC3+rR1ffzryWa9L5zfub7NXBi78+cAp'
        b's/3/cG5ccdJhr533w4s3Qk4f+cVR+mc99PzkqsUoq2Hr3qh+7ttxz5Rl/Lh/+o3n/lH/l+XHJmSdGLZ5Ru1I58575z87+0PL4ikWy4ZdvPLpuL9Mb9zT+W3Y+/s3XT71'
        b'86mDf2rNfnborXfnXI9b+q8vQu81F3zyREpTy9mP75/54e3l/9rb+EeHZRevVKX/Yv30Cq/2z699M2LNiU9TN+yd88wnE5ymzJv09493fv32M34fTX7F9MKVpXdijzZ+'
        b'entOwJyP50j+fPZp6/lzvqv543zTv1zxG1vzzRsP7xj+lPXey6+c/zbpw6pvKqx+/N777ROdVZHX9/5i/uTEd4J/9+rXpvoPZycUvr5vh7sqfNbZZ89PeXnU1tgbbenT'
        b'j3w7ReJSnerw3eLVfnZt21xOj7s965vjLTe+jvus85mmafjjnlvyyZcvQdaTCxbtOTj59MrXKj9eXK16+eEzkQm5L/9hhumP5o0//0P/2aFNpRJfhTUzBaXBOafuhiSy'
        b'456gxqTFI1lqd/pk7OyRwESOolxmpMJTUSwSzmw2pcJohQ6dlaoBinlQ4l0HuOjfFSipN5yFSpKz4zhPCr8Cd124eQjr4ZguWPLadmYgM5kBt8lyP4At3QlTOFlKHJxm'
        b'RVjtITtnsc6IhTmzOFiCy1ZmhBuOVVt1ljB/aOjKNlKP5haqhmi8xIx0Qyd0xUV6iekc0qkQClm85XCo1YZcQv08dnEFlOMxipLrC5dkFlAhyJMkE+zwMusTJ7yEV/3N'
        b'4CbnNaHwPMczuVmwVJHZw+62CUuZ6W0ZtjCYhY2LTXsZ3qCF7DtdxreNUM+aHjJ6U1fyu0xwhiMs+b0D9/KYzuIMaCE3OMEFuIu3ZILMSYSbyXCSV6MSz2K9znRn5a2j'
        b'c5ngxeIlnaEETnL7J5zaLDDzZyKeZ1WM3Qrt/gG+UKjJQ1u2SoerRA6g63LXVLzB6pAI+SyXq4wcL8FEjtDDvWZLpPNsR7IeTCYHXSOnaxGX4wWeYWaLx9jFbRQ7C4pd'
        b'A50VEryGdwX5PImtM1xSGDx23rL5fyfALkaLIFkwkOFwjzDfSDSRsNR0iYlIE9ktJHKpgWhpYcYSymmSOmXHMGIJ5pQHg36SaxLPLaQjJCPIb/rXhqWxW5BPVqKBnhnN'
        b'P5Mws6TETLRipdOUc7lk+4R+DGq98qn7sUYOZBlLO9ozvvPxO717svjRfjLG+0kWP0CtgpMGMlNmC1/ZdzdUPkZD+48BoiAOzIzHw0qEeLkuGkg6KN59rkL2Q1QfFSEk'
        b'Lplop6pH2eqYYUCjjFBVNFpluyowYBCNgyZNWPfROJyDONHbxRHp/t3JInvh3BWvtO+DRYE1cNkUq/HUMMyHE0xv2Al34Xa389yN7PFd5/kInhuwhazAYu5RguvYxsWC'
        b'baOZPBCBHQH0Unok5rmQTdUlg/xgoeOTNujNlEAZz1q4Cnst6AtkFCq0SBwrwAE51rNrgYHJGtcfUVQamftPtI8fwrSnuCwJy6/5wicqqXC0ikNnQj10QA5DuNyGuQLR'
        b'oOrIAaNYyeRhCywRiKRTi5VSlmZCjo167qY6swMPGhuSuQmlC0SyyRClq243v3R342pHhUMglsAxsrlniZgTDteZphaGebH+9NgIwvNmeoLcWmKy0U7Ng9rPkSPgOnaG'
        b'YqmM5qQIUD4GC1mB26OwlOHRxWGZFo/OcCyr38apcJZqL1aGmoSSQ0R2Zbv0iWF4UZN/IYeTuqybUFbiGrjupcnbCJisydxosdOgd0HVVKr8Yct2ogEIosN4OKimk2aV'
        b'uyXXzhZnaRJUljBAuQkzl4ZCKVaEYylWhgcGQrEoGASL2GoTzno9wqlMGC0KI1J904JGTnbmkJNNFhMFKqwvNIuTfD4skX/5UZoPy9PO3pXh4O28UehBlyzXzl060Rhd'
        b'sjVZYcImYaeoFJRinmSksE9LnEz5uj+m+Ig0VXWRMi0gMTlOS50sS6L/6IvfS89luY4/mWkSY4ONWESyix/RWeAKFjoZakVdPMTyGsSQGbPxBj3OZ2NexsKl8Vt903Yn'
        b'Q84YYaeHBVzFE1NYwywWmApkrtlHuW9KOhcRzlubMXy44ESuRY1S7vz7HHcuEGO2PdzSABRCLVzsAVIYjNei2PjF7YFOphti7gaNbrgUL7NL/nB5FLm01RT3BhLBx0qc'
        b'A6fwDnuhwlXOPLbLk+ICLuqbCmwGOaekUH0PWlO4vkfk82p2IR5zfbGFTC7b8fqCdLI4zwdzFCKbI0s24TVVEBXqdsMBibFoS8GPfvNgxZPBSqsWWQjhcVHHcZ1WI/aL'
        b's0x+XO42TvQtWJ9lbJyB7eYpGRLaiFlTlmhy3PAoHILDGca0FLJu4Ngib748WobFYYsJtutT8roSEQ9TjMcK2Mtyy+AoXrY2nkI17RXCCiwPZs9MJUWVG9s7OOJVCrx4'
        b'FW8a+EnW2MJljlxYs5VKoK5+ZAfL8iQyKewT8QjZD1sUElbJ7XhtKF2q2LCJr9V4Od8uLoRhGx2C3UR85EOQDacT7V98RapaRtrt3eYZF+6vsgq3utNR//W9+wthoe0k'
        b'iXvukHEjhuh5/96goMl+485JQ/7p84+zDvP+0Xzi0utWld+4r1rzJ+MI67gVPwuOxsOvrF7ttO67UevWHvG+kfpBZtC3JoZhnwTUf70rsn7Hj3Wq5O0bXH3UHVm+B4P+'
        b'Wf2Z3tJR+TVhUxq/WP/drjf2fb5qTO2R1+wW5KXUVvutMxqx1tBSOW3Dkj8Xz9//4b6vFQF7685avmW2w2z5pazA1WN+eeHZlYYXajYZLRtmZbfW797Fy3UedqtmO7vF'
        b'H06zXveHUS0OXw//JdChPcbhgl/jjOY/TXQwdAnPeeWvpdWmW0xXbXw23iDrk2b5a/GN7245WTS3I+af7wY8pW6Mv/nymTWNl69cCFgWGrVs49MRazdlj9FrL/2kfXJV'
        b'/cef1YTfT//wO/+T340qiji5Qdpea+N45bt7nx64fuO9qNuOrzy5fWWi/8EPt5/UG/4vyd/tkz5c7/TzMZsXml7+s1W45c5VrXcXdxS3TbsfcPWryOUlz4Qee9P7rPvD'
        b'UPMXr4cfezn8z3+s2Sb7Uhb0gdiSv3TVwdm1X5a6f3e7edfTboljK9qm/DHs4ZKOnM8+DAj5wHeqc52H/lcFVlt+vPfu9qKHmxe9/p7i6+VjF7384MQNw4cn3Mz3/aVu'
        b'6u/GPvOqMrxUfXfXaZeNDxadjjySm5VuffOV4DEbx+0bs3eey/377wTUfGT2wpTssfI/3JsSvezSc29U3f1c8drL389pPZzxweb3p73x3KETy04uvvzlDsm92NkRX9yb'
        b'+3L5yhvP1n0wb/nut9Z88reMlVkNH01xe0o/XP1+ydSMu23vvZysvPXMJ9/JS4sj3Z8fv3jYm3Mrbhydt3bR23OKf7H7Z13C3x5mBdzP/ev3+07rTUmc9Mc/eV4488TV'
        b'+/4vm/l+e1d4v/auQXxE0D/ttk2Z2vT+l0FXzV1t9NOK6qOCW8rb1kfvbq2K2f3wa6exP+x84e26sJ+T9+z40vKH1/9W8+HPb73yx79XCp8O++aJyIZ53gvKxz9V+uPN'
        b'P/3+QtaLl/fetdv81sV3f3LF56Keaqpa+cG3bn//11sHD3/rucfvX/Mu/LK1uUlsOv7q1AWNYta+HcdjL4S9ef/kS7vT5R8df2nc9YSbWwKKxn396bhnh52/9fbsZ9Sf'
        b'P/X7+W85XPvjl2eeVhn95TOrw+8te9twxh/HBvuN3VJttWDN8Fbt58j4z0+4fRvgdyfeXbH7H+UB9+bXWUXPCLr3l5/PGEz1Wxr6D4cfP7xmu2lf1o4vpn9o9NkYtze8'
        b'v14nlhV/vvvVGdeyP0/7euynu17Tb9a7cXTyB2/Kf858J+CLn4cvHJ7YWAV2r0c9P+OJdct+OrklrUZvTF3l15YfW3Vc+8OZdevqVw7fU7vy+osLTlnMzXxzykeyQ+t3'
        b'PlC9/NPo794yW3Pj+W/Vq74b/tmtZ+JTdw/dubvgyIvHo1vj59Wst5/5zfjvP2/tXD27ceOC7XNLgl9It86I/3jhnocvXo7utP3k+d/99dv3PtwpHV//9/e/+E627ueg'
        b'n750dTgV/nyH3c9Baz0mhyeEZ32/x3z+xOdNPlNsZoyUS1PgeDdeFQ1OBrTQfDtKrLImggdg3MJGvKINMtETRBUPMdkPhTyX7vbOoTolD29Bu07NM49kSuSSNTP8yfmo'
        b'Cd/AUxGCYO4mTcBr09jzG4iYcaObugrVoZpIkUgLjsNRjSeG9RcosiOMa6t4DDg1ZtCCMd2YMcmZeUJLjQkHhjNtcZgxVDm6MGxCLJ+jgSfEYmhkVXHXgyJVl+ibBXWi'
        b'YIp3pQvhoBHTSqfMtFO5kJc7pwUp6PnfwuJysHAUHpcK0/CiPHRyIk8+PJ2eqdGcoZWoJ/JIiYMPXOGQkKfXevgHUOvbaaiSrBdnBg5nz2BBoCUZC1ciajthHq1bucQu'
        b'IIp3cg2cwVYG40Yh3LAS8jiM2wXI5qN02xTLjLHAmRxGJf5SYR4e0MdWSTDk7+YBO3eXj9FdxpYAAyglbYMCIjDAbTte5xaTuRz99hiR0Tn6Le63ZqpyEOyN5I87+4rC'
        b'UKw1MJKsxDZ9no1YQo6pbJWDL5alstTQ8iB9wQKapaPxZjrWOPOc1bIhmOfPgFSwGQ7SdOrbEmlMOKvdUqiEKmzxx2vBxnDBXi4YYockA69QRFvs4NaEUynRKhcFFhm6'
        b'ULBfIyyT0AzLYqzHCtYDGzPwDq2ioQKbSRuhdJ2UNLBTOnT3bt48oqE0MkvLIk+toWUmtHHO3ENk2tHRdHRRGNk7wAWZYDlCCrehALOxwodFC6mHBRi7+GO7AolQa7LS'
        b'wEyydhM0sQzOGCjdOi1YFSRyyeI87MX9bInBfmwionALbfRVVjoW6QlDrMmMyoVjRL6q5YNz0gha/Bm36IKVOmbRUbBXBmdHbWYTVwZtmSoXX2gyIdehPEEQzOTSBVOw'
        b'hE18M/9Nxn7OAVuhKBYu+5AJqlKIwsgw2TLIIy1kctHxsdvgtpJ+L+AdAW7MmcbKnaH09dcia9P8cT2y9Cqkcx29+LQrN4DqLtDF+UEMdlGaQvSTQ8wIZReBZSpfB0V8'
        b'MpG2oEIkwn/2JG71ugn1k/EcRRzAYrJrGFPU0WNkCdC3+ojm/j2Tm2/jXbyikrNHx/vgaQ7HiK2QrwFkxCOjeVgZUQbPdDdKmVhITZOGTcQ6bu87BJ2RxvakC7YGKCRk'
        b'mlRLsEwNtyIEfrmNLLr9tEWBzqIA17Da0F0CVRPhDKtXiC82G7soHMhgkTrDNalBoiSRNKCI2xor4hMdydi4+FIE543QTnoDSqUx2GjOpkHcGnfy5q1B8zOpzHdOxPpF'
        b'fAckE7JgvrGCrAzSFxsovLIeVonYljCZzczVWDpOY0U7O1FjRMOrO3kE281dcJfMe2hMolqyFAtFOE2E2U7eGXdNscCf2+flgrGfBPYtJ9rjCajkScdNoSZ0dNICglzM'
        b'V5H17io1GO7C6opnFw7HZrKDBdAJcV2AK5YefJkclOBeomekYetUPaIzwx1x1Gy8q7H3wQnUoMrijWitMdU8kL+tEU8kcl2AtLSNKgNR5IxgHVA6P7bLALwGi3kwIR4P'
        b'5uXmjMdcXlFXUTBaKFlC9rsLC+E6I/ZavMBaRaFQ+fokClZnBqu2FRZKiVCfM4ZtQqPgzlYVlimM4ApZdUVO2E438WvkvpEWMoehaexFqw0kpBT2PTRDJxmmCBGLIC+I'
        b'9QlciTXmLNG415EaVLFsMh+ETnJGXafeGvLmkVhFxmiIuAGPybR4uK3YrmJ49xtgvwh1pP2Qw0M8HXd5EE0AC+2hYTtZIlhHLpNVsZ+vkVy8qyaVtvfLdJCQTpqpD4cl'
        b's5ebstkWAfV+NH42mJpeCsnk8J1Oek0iVUbxBZYZPsdRt1eYJEjxJpmNbZjDdpRhhnBRRc8oG38/sqOyHVEqjICLMvfdeIs3qmndcr6lB0DrNjpjj5MZC53j2NvHx0/X'
        b'7IesD43IeGKOA9xZoknKnwbnw+hZS1FMD+ExSYTo7IHH2Wa6w8ZPRcbZEAszya81s5mONBQPS6Eeq8iJQGfZRnJm5FM49RHQoEFTh5tkT2Ez8AxUQR23y0LudAkzyy6J'
        b'4ynxeYnYYKw2NcRWD9Kd48VFyVjKJ3SZWZYKSyidWVW6xEqcOJXswWzV5k2hIBPM/buV3BDgRQ/1C1K7CHsOLHsLL2Gzjj9EFBR4lkPNb4ebLFR1eWAIQwtzxaJAJ4Vv'
        b'INmmmb1/T6qeMGuuHE6N2cxLOjKJEU1rbNFYAdflAjVG40W8kk4TyRmp9wWGcNwN653urZ57eiDHhuMVA1ey6dXzbXg/1Hsbszudt5JlQoF7W6Ve0XDaLJ2NpSJT0BFl'
        b'lzpuwXrOkz06ll11HZ9B5oJmcXlLyPl0m6zVM2S42CSsSocmen02XKCb+BERyuCyNoC2aRsW84eDXPBiNOm66VJDN7ibPpnW6zpemIHH8YAWAbcv+m0AKZ4dcXlY4axt'
        b'AimPNqFdCifT4cwSzON8kXewcal2Sutg8qHUgSHlw9VYNjtWwsEFxvQMLI0hujN2iHCeHB7VfB/JxjbykiKtEBQP+w0EyYokN+5Egupwsrn7BchF8mCrSBkAKlnlxloa'
        b'0zYaEdGnhaz1WvawFeRKscAWrvHpdcsfqiEfmo0VgiDakIkYHcRBrS9hDpxVBeFVVyI5sBPJYpM0djoUYYkNWyoBCRuxxcnFZZsx3QCO0bOsGs7yU7lt0jJjCjznRSQx'
        b'hTh2O9zh8sjBedChIvs6Fu5UGXY1aAQekHlmubLmrKE+G2Nn0iB3uECkxbGSodIULgteg0KKNUzNU84OomCrMCDLF44sgMN8gTXAeXuVqwM2+5BxGOqhD50Sn+RxbDaM'
        b'ioEj2OIchB0BM8jmLujtErESO1I44XoTdK7vhmF8eR3bABiEsf84NgST9PRULn5qBVn9REiTSKAACqECC6fxWdDpwagsqNTsa25PlkJeIA0muSGdjafWaHBC8CwRQDUh'
        b'2262NGhbXDoDLvAtuhVu4xF/l0C54BcvyRLn4oEwdmEFlq7iYdzYZMkiuZs8+dopxUtwjFnoqO14Bh7jyCNkwylTDPnvoNnKH3Gdg03wdFx5GjPyM2+PAbWb9e/t2SM4'
        b'GDAQYfrHWjQSLRmkBgXWsOKIgRIKzsHvMWCgHAbkPivRSmJDGdIl1uJofRtxgsRCtGJs6SaimThJMkm0IZ9s9SjcsJnESkJ/T5IslFmIY8URMjMGZczKpj4l0UK0kY4m'
        b'P63Jd2MlNhJLVgtrkxHkDdTr5CTtr1wL8swI9jyHNTaSWEuMyA5tI9OChnDWdlvyczIpYbQ4WW4gbh/ZjxOG99VA1K6P7vYup1At6erR1HZI97EBnELZwkPr7m6hgWtE'
        b'6rKVOp3S6A8VN1am81+UxVgh63U5bXu3i3r9XUzbyc2fukvksw5GgDy5+zEui+wy+TWd30DflpYtsq7b2rsqfe6RdN2jvSzyK4NUWM4vHRBpCnZQEHlRBf13Jf1xhPUE'
        b'+ZZ9pzDpBbKStk5g2emhi328A71DGawKyx7nKCvLddAodOjSKJMSnwZW/zfAT2gP6OZOMl2m1KEYT34byGQyDTy39N/5bSC1sKBrVxCt5nJwFLqmyFEljt0jGDKY2jDj'
        b'kVofRHf/gxwOSYS5a+RE9e6E2h6YAkaa3yqjvtgoU5T2SoVSv0amNFA6xAtKR/bZUOlEPjuzz0Ya/BT62VzprvRQTmWfh2gwU+hnS+VQpZVyWI2hDgPFWjm8GwbKzG4Y'
        b'KCNK9ZWzdBgoo5VjdBgoY5XjcgWKivIrMFAmlMqVs3UIKKbxesqJykn9Yp/YKSf3wD5JUHg+MGcQQIzqe0lcTGL6D659gE+6Xf03UE9m8Sx9jweyxcEh3g+kXh5ebGvQ'
        b'bgwU6SQtg36RSX8QQVz4NUW7U3iMX3f/rF+PaaJ9E8tvde+JacL2mgdGId6BwWHeDNlkUi/YkdAlS0LitvbMqee4Jo91axccia7BIwYqVYcU0rPGCsMeZdDx6Fuoee9u'
        b'6r+sQV4+0BX3tDLaUf9ZAJHcRxOo6gVxf1QVHIJaClxI9LuDWvBCOICFnPbqOpG37hozBLJkuEYRBWuIMF+a+FTuEYmKSuYXkzMpy7tP9P14h/f8o43iPxK+2jvyz8/P'
        b'elmYvVl2zd5GIXLB8uQwvElNbHh8pw4/zstvAJrUcm2QC0sfG0jsoX9sqeiwfUSvRfkbwUgs9SlW1GCnPv3zRQ9QkgFf/XiIJNR0/F9FJBkvf1xEEiVrBIVcoDkL/0k4'
        b'Eu3CegQciXYxPfKOWY8NR9JzfQ4ERzLQqh0EH6Tftdz//b8CDqR3dhpPpIhOpjkQNMlsgJQp3WP9Ycb2gRDpMc4a2BB6AHEoEHIIOQyc3fQovA5tTX4NYkdi/P/AOv7/'
        b'AevQrrh+sCrof48DmdFz0T4mZEa/C/h/gBm/EjCD/tc34UgvKExNDyM4vAlr+wduwENYGqAhQe5y38BdzDfGs2nYAC1TEn+yHq6nonGEs/e76T1xdVi2rYn3iz9lS16/'
        b'Xix97cwXL4DsbFbsjs9nlNTNz5s6SxFmM7Fh2YzVBT/Pmv/szQzT4F1Gt7Z0LkjfZ/Ju7D6FHjN0jYQr48cO1eAkcIyEhlnM9jYvYG03eIRZWNCFkDAxlJnC5BbxOtdy'
        b'BDTqQAjgwEZuT87Hi3CVxgjmztBAACTN4tAJOXugtidBnw8eZHHd0Igd2jjX/wg8wORHCUBLOUyAvD9J5P8NHIARjyVVfTJ2cKnq14EBpB0Su+S7fqAAvPS1UAB93qTD'
        b'AZgwwGHZN/dfIR88njlWX1Np2rHG2uW1kIp3+r0EPGMq4sUbawQ8fSbgGRABT58JeAZMwNPfbdCND2NXfwLe4In93dXX/y+y+nvCqGmkJk2q+xZyztCc4/8l+v8v0d/2'
        b'f4n+/0v0f3Siv9OAslUS2fu7U779qrz/QbaM/5t5//+1bHVpv8LjEJ6tPjULL9B09R2WWso3PB+ppuhHuB9aiLBVHOAHp5ZhSagPFgZrAdF8/LCUEa6tpJBkND1XJsAh'
        b'KDaEm3BgD8smmYfX5lHbN81BH7+hZxY65EMne/vOdKhRmZrClfU6xLYGbzXNycFOaIRK5uPHW/bdcdF6o6JJiPyL9YbYuRXK1dQih8eGzvDfZqjLhsUCHyeeBoMFGqpZ'
        b'PSFyisEiODdD7UIfOCyHw/69ZGYs2D6bSNRYFkgD4GhWvT6pyl4oYqnOjhI4piOuDV++0jliJU169gsMgAthPnDZJxCP414XZ99AUpCrBK4Ze0BxSKgwFmrMkjbPYrHj'
        b'iXgU21QeaRsgj/KQUPaU03BLTT0r0DITanuVT5N5Uz3SQrBgEjbxZHqZEAXF+lAJlZyUfj4esQ3V3qsZqbBUD7gTQR/TtX1tvD40QImSR7C3L8CzxvawN82MdKV0iDgP'
        b'T2I1S2tRwi3SFy2ZWIMdmSqajXNXdHSxZ+kITus5rZ6bZ5yTUVa8kPjHCxMlqvvkilvCsfDyeWbgZpJXe8b3+M9X3VUGz72YZ+y2yuRCbmNr7E0LeUtaXU3d2IapMX81'
        b'mBVi9+ShuXe//d737F6PvfZPzRMvvnR195nIWYXvwcsmZ2qK3MaeM4mzmpnjsDBl57Jj0vvbP5gTlO5X9UqLQczclthDQ3Onzj9zdI4qocosNOf7I6s/2/XVumaXb5tv'
        b'DPNK+Vd1ReS2pqXP7jBWfVB+a2zIhn2RM71+qCz8pOnCl66X8mfOaJk0b2fzro8u2C2Kq0heVuTarrSfMkZ5Pzjq88jhSb4+XrcVFkwn2YP50Oy/DI/1glaD4+OYx9oD'
        b'S9bA6aTelH54BEsC0ikrzxSsc/MPdh4DZ3ky7FyRe+fLoBNPYStUd8tW5amq9nCOKzXnsByaemo1w6LmMKXmnI6zL1U9hM4I3QgzFmUB9vNAiEJ1KnW0w34bDWTavuU8'
        b'VxTKorAmrVdc3xUyoVjoLFy2mkqjjUkdr/WMOObRxtAEe3nsQxkWJZP52AoNtBV00RYS1cwMb0kDdmmYqqdODyUaagsjc9ZQOSvxKI+ivSKDBn8PP8hOprtAE8WAa8CT'
        b'PNSlFG9CmyPetupOcDJzGo+ayN44xNEvkAxKEjb4sQYMnSLF49AcwB8+h4WQS9RQV2zq0kSrt7LWKeCqR/d0VW1u3MKNmnRVNVT21bOM/4OZon6P0iFTWb6o1IBREBvI'
        b'5QxmzkpDYUx9+xaipWgmMZPQ69vH9daY+k/0NHycRM8uTVNvYAer/sAMwP3kc3o/lrp527a7uvmoJv2HUzqJ2vbD+kemdPanpf3qfE6KeN43n3NiEDtc8LK3iyafc4/L'
        b'r8voHAYHUjhh63m8OlaXzLl8qRs0CzGL50mNhQl4SYq50IT5PM3qGtxcq8oYtr0L5WGnJTsZvMmS3k8exqN+buQSzdOEs6PY7m83lKzhneRbIcrpnVlhAj9JamRJLBMT'
        b'm520mZi7RU6ddSAFCvAwzeMq2uwquJLNqpW/vXH18tFQpaIxCOSUhUK4AHWstIXr8Q5NxNyNpzV5mNgARzm3WAXZcS7wVEw9QY5t2GgtMcEcI1ZkKlRYey/plokJh6Ge'
        b'uc2mQy5cZ7mYWDNdm4uZgM0sw2uuExRSeSXBhidOxkAtk2PIOX9isSZFsp5shSxNUpMjiY1Yzfpj064yYXTgj/qCW5RLwp7NPEUwxnCCsES5mKz1qJh7m5L4l+6WPsKB'
        b'1FbyXZTRGdfU354lmfCrE+9u6ncl3tG9Bw4Saa1Jw9riRPbRrb6BNAz3oCb0Cg8RAbCQhz0qoF3qQUQYf7yEF4EIBSpj0nuLscA8LAjOs5b91ddUGGFrri8sjzJZMUTF'
        b'mxvkaS04GfjqC7ZRc7/fMENgXWpNOvIsTZMch1fNDQ16ZkkSUYwJHyvIsJ7kuZAHl/FcSFKhDlbq35zlgsnCeFpq0tDxQ0h7OV5S/TQrVRAWjqfnMw1mHg8l/1YW6q/r'
        b'X6lBV//SiThlCHSyxEYs2skzG7F6C7uy2m4U5EFBV2Ij3oYS1uq1/kT6ajGBzpU0u5FnNrpDBaP2g/ZQrKJ1mI71NLPx3C4OrNvmis26zEY4lUETGwOc2IwfMi5Rk9Uo'
        b'Cnp4dCZLa9wAbYn2b63TUx0kr5eO+Ls6zF81zNvqs8+y3tihmjJetDz0RdEhAwe/khxbh4KlWcv0pp9aMrbdPcNWdez606fOFZ06OfryS9WRB/Qcdxd+8FJa3NW0v8N0'
        b'/zuqm66VC2/MevnDOW/PfvnNc3c/c7gSMmXlj3us1nhmrYy4cHBp4gdKxd5xTxyNeLhsxDJPeYSnYtfZ036bXjmyteF3tj+0NF+7vvr7m0tm1rzyTMHCpTGHPdaPbMz1'
        b'jTYdHvPkkcTaS3Hhno6fKBdVmr7uFjjl3tnSJNXSiiGpxtfjYl+XlG3ZtP2L8hlO0lf/Nqlz/pt/3Woc/5nrz3++/NzEN99vfhjw11/Gzz/xevvsSTvPHLnhlXTxuaTi'
        b'mC86nmhH+fSfnxqy5m+2P7dPfCf6/vSvWneb3bcvh09Njp2u+DjmxPqn39zyzUd3lt8aPmN/yfD7xUFfXW+KmP33mDdeentsatLeedEbvvIxvv3BnVOfbX3u89FvPl/n'
        b'pj/XK+iX/TV7ftd5/75jlHzuvtcu7g66B5+Ev/WTr5Pf7fCUW68qH77j9NW69847Nj2xIX9MTPyhjN/tiPh+2qkUW8+8EXF3DI+3X4v4vem2/OhlO0vfuqL/rzfMkhJq'
        b'T099+uJVv/A3vB+uGGfc6Zai/tJv3Avua/aNfW/3D2Z3Lmd+8V3Qqjdvvel0Zc5zbxi+tuPnn2qM2kam/zn0Ylt++//h7Tvgojq2/+/eXWBhaSJNRQQLslSVoiIqioWO'
        b'SrFTlAVRkLKgoKiIINIREFHEglIEUZpIUUnmxCQmMTExJpGXHhMTY3qMKS/mP2V3ATW+JO/9f/oRmXvnTj0zc86c8z1HsON0zv32tVe64gPmH4KXm4rzC68bhUTLvvE5'
        b'Zjxp/Vuyc19F1l3S+41zlXzmefSLCWkNdxvlR95uvL7HOjxq4fXPb3auNApOHR0S88rKhwFf7A8/nXsn4k6kiX6N07jqwBk/3Mh02Hz9+qQ3OsBf9GDUZ78I217zXp79'
        b'S0VjdH1x6Ljv0q/8ImgN/3ZUupXD3ut/bLjfFvJtdYrW0Welz9UkueU4PDwWVKX3w7X9xenv5qY/1HIrlkOb5vdeL5jHv5F05I/nX//99v7i2QOnPpmxy8st+rNRY3+b'
        b'uaf4k38HvvWd9RdVh4rcHrY3r4+2+t38nf41k2d+9bC5oa/HrPvcs4WW23JeLU5850HWtbunVux5oHPP5t7oe279JrN6XMG2R7LDL/nwg73vj/36xQuu63N+zJJmnp+0'
        b'o8nti3cFv7667XxXTcWSO1/tunPlq/DP1MK6F9Zk/mHeJdL5/ZnmKSG3M8Z97lKAXl54boXZvz+98/4h7x8Tqn7VSJHPbLnh/mPOt58Vjjjx4MNFp660vr+6oWbp7Ldu'
        b'cj/WGAcd2SF55fWva06m7Wwbk7t4VsnPP0kffjzxVOO3r954GLcu9Ej3xFW+gdypG89/NXO/NIHikCBzI6rA3PfFJY/C/RjzPducsvBzUK3pINAPFUAVg/q16TBTZ7xj'
        b'6g9C/fKsVUg/1BdIRRfdUHSZYv2gfgyD+ymwfsdQMc3g64r2DIHoxcmVAL0U1EjZd6HOagU+T8CpB6MjBJ9nCj304wALEkKPcDKHLRlCTwHPs4OzKVLSwKoEaFYA9KQ+'
        b'+ASygTYzfL4wkJ6Qm4Wy1VGHKWJQISzxnEjyVQor6qgFZYXzNmg3ymOwjnyUaaLA45HXh8QEjxcko1bKY7ajPSo0HjqlS8F4qAL2sJLPrl07BIuHilADBeMt3cUknCOo'
        b'Skvx/uxKhsdTgfEuJNJxEKODKI+h8Q6iTgUab9Q22rLVmGWpHkTjLYBDBI03wYtKgVIs6tc9AYsHx0ekxI9IURj8dM9lUDyOgNM9CRIP7Qmj35tgOfOsEoq3BzdICcfD'
        b'UtTZFQxRUQ8NhgyLlzpRhcbD/F29PXvfEq9HkXjQ6ilVQE8oEk93E61/4gpUPgilQ6e3ECwd7Gc2RC7oEp6Jg3BwEE4Hp6CSDVyrkdsTwHSwG53A05NBNXo2/FYK8oO2'
        b'NKWAZ6bOrJMOWGyQBNhrSwn2sFIHnRTA2anQwtCFfUEzlGAboQJvw9A2IbOZ5Nxpvtk3ALKCCEjvEYgeOr+IgSXO6odQjN5ayCMwPYbRs4NjFEWC+pOnS3xQGxyw90si'
        b'HDjkSRlQz1wkwo8LUTZtyhInKKaQPDiJmgKpAE4heXAZZyDUZYku7iIINm1dtpSVmLxziawVh6AB1RI8Ay6gR4noWAAnGUirG3WlLYOaIag8yA5iVHtpDWQy8T0G9Q1K'
        b'8GskTLDuS7BnqDz9qQpMHjqOyuinkjA3xUKCYyuVqDwjzH8XU4LQQZ1QzEB5qNlBictDfe4olxJECF6j1UpQ3lRUSTF5miiHyeXnpqCGQVAenEa7KSqvBU7T924p0ElR'
        b'eVCwy5thRhgq76yW4j4DauwpLo9gnPKwYEOQeSRKKsMH5IrjldA8NZyhBPZTbB6cQTW03w7oyCyGznOBbiU679xM+i4MNcFZis5bFqEE50WgKgZkOBu6kELzoMNfgc6j'
        b'VwgMWIMu4e50kVlyEhBsDQPWOKCzlIgJbtTIVW8IOg91TKNv0lHZKobO25ShQOd5BtBBtIC2mQyaNyde5easEVrprY0X6oLz8gAHEyUziypn0HasWjmRAPPgcvrQqyhX'
        b'YLvxavd5FPxjiPYqwUNN0LaUnikJIXBxGC7PAB0ZissrsaG4PBd00EyOyb3TikDzHoHlOaN6ttdm7TRUAvPwLDmiLoLLs11GSRbqxkOOL+SjYxsVjs5gD7rENotIAwUq'
        b'D08M6t44QhCGCLaGroMiLOJl49dQE5uizilgeW1QroAcwimCTSXQPFtHFTLvtJzSzAQNaB3E5dWj4xSYh0ezn+6RE2wCiWTgIJVq4dVC7kLP42abQqvI1g1KaMvcoN16'
        b'kI2ucyVs9Ah0hk5GahLKxBSVgc4oTA6g14VtMmcha6qEFTkHj+Z5QpJaqIxHZ1A2NLEFvDvFQqIAGqnjPCeN+fGyUFqnaMlqBp9CxzUVoEA9J3zYkWnAE1WhLZdGokx6'
        b'LmqqMIFjZ4nQfukOOiiTUQe6pMAE4mlY704hgdaogq2UfNRnpwAFopKFKlwgurzehV0N5qgtJod7rCnpV6jAHmqiKanYo3NTh0ACoRSah4IC90In69r+dRoEE+gN5xSY'
        b'QJwzh43MPjzn9QpK6+cokE8B40OXIY9uBM6ow2AIjG8T2s9gfJC3PMWaHruwFx/Fg0i+rUsGsXwKJB/eB/LpUERa75BLlUNFnD9lCe3kKegSz/ipGsjEpz2m2OA0X6km'
        b'5Eu9FWf9KLRbtBgOO9IWaeqlkjyYHaJUsB92a8ARfh6W0HZTMouDgjiK20Pt65R8CMHtjWDGKwvgeKriGnYiylTdxKJzmI7IfO/E9HyM3oGiugTFNSg6sJMW7ZfIy3G1'
        b'gZiaSmzxhqufLoRDJhmz8HjSBXd8Bhy3hWI/zIr5C7jorWI4xG8XBdDBdoH9AXKCvs4jGzrpl4AbYSSEFtS9wwS1pBBkBtSuhnNPAjKqIIDnYfcglJHAshkdVqJSg8dw'
        b'gJhky9EpyFaAuBHxHFhGAcGO6IQCE4xOo8PhbHfsXryFvITcVCXqfANjy+DUTjhEXqHC8Ypd1VEohjwPeklrJbBUARXRPmh+DKw4HQro+uYD1R9DW6K9qBATZAE+0ihY'
        b'sd/ewdZ6AXQ9AldkWMUmKKQtDVyJKglYMdVJiVVEVVNYS6vhLDo1BKu42JRAFQNHMbOkwpg0AlWEvRpKrKLEnzYtHlWhBhVYEdVOG4JVNJucQlwWxVuNcxGqYIqBmHei'
        b'4NTmNdD9KEwR5aqjfMgLo8tv1/h0ilOcghpVQMUqhmxH5dAZLPFJTPPHZ45UYI468K5LhiEUirzlfphbOEGwio8iFVGxmJasT853ClXEjLQU9pvzI1FTCJ3qdahs6SBS'
        b'EefrZlhFFwYnRIcjoUMFVdwUTaGKJAo5o5NDUETcVlO4It6wolEDgSuiIjHrcl7K/EG0orvWIFgRlboxdyAyPCYErghnQ1WIxYp4OEQ3PO8xKFcBVjSBoxSvqAAr2scw'
        b'75LrMKulQCpGoxwGVVyJTwBDtplfgku+DpAd7o+PrXSBu2usQpEwYaEKjxgOuxkeMdBLqvt/Dz+kYCqqP+Cfhj1kf0cpEYj6wj/DHopV2EMD/NeQBrTRx2mCO/wPmEOh'
        b'WIEPFFE8oKn4UfShAcUbGtIcxDOltshUYCwQ8Yv+K9Sh6XDUofGjSoL/LeRwn4YC6PFUvUUm9+sw4OGfNErKJ9cS1cjJxwGHw9/8lUdD8YNCBgMkwJ7khse/dfnTUv/s'
        b'jTr7vUMFCyQ/nggATD5KMv5V7N/I/0vY3zFc90cEMrqM++ewP7FQX10B87NSwvwMcMrUI5UwFtv0UO3jd+g1qwScNepXiw+D1mFWvLqK/+VZj+H7VokqNCo0K0ZG8+Rn'
        b'ha7id0PF/1rs/1hhtDBKWMRH2ah0XCQWkXauTq5urj6NKa4dJYpSo7g6NZl6lHqURjYXJY7SLOJXaeC0Fk1LaFqM09o0rUPTmjitS9N6NK2F0/o0PYKmJThtQNMjaVob'
        b'pw1p2oimdXDamKZNaFoXp01pehRN6+H0aJoeQ9P6OG1G02NpegROm9P0OJo2wGkLmrak6ZE4PZ6mJ9C0Ya5atIBEYs8WrzKiv1tFTca/G1PTTSHV/4lzJXhs9PDYjKBj'
        b'Yx0lxTlMoniKxLEd0Pac5x+8QKHI+6iLf8Rsk9hNDc3BgIUqq5+UBBKQQ87yuEyzY/870fAV5DfnYYUp9YVyB4t5QwwSFfZ1FNWgsOLDb1NkyTS6RsIWEoc4ZbhB4dBI'
        b'G3YWssj1GyySZYnJMrls85Aihlg8EiPZYSX8mUnRcK3lsERAArEk8462oAF45RZbZckyC3nquvhYahsVu3kIWIQaa+HXkfhfyoZk2fDK42UpGxKiqP08bnNC3BYZ1a+m'
        b'kk0yLp0YfQ0LJWKxMJbaT1nPkypMf+OGW5UR4yuFXSKbCEfFPChH3M7Cer5UmS3SQi4j9nEpsqdNEplDa08pQZhEDrFBVFj/JSTHxsRujowjUAcFtBwPAYFxPNJRuTwy'
        b'hoJcZCxkCs7Fem8RJUvEp4LcIoE1nBoSWivezScUFp8gH25Ptj4hPp6YOFPae8RoMUDKDwjT4uMG1NdHxqe4OK8XKrYaNcW2QzVfxK+qArKmkasMZCah24cAbyB8tK5C'
        b'WS7cp76H2yHapp4hpMpyEVWWC3eKFMryDVLRR78K/gKIbdji+XNztT+zYMQ9YsaLK/z9FNZ3NGYNLXdwrvCsUAtVvBSfbNZqLWMk9Gfr9CngKjqcbgQjsz4Sr/QI3KQI'
        b'ZkXIClMVMpTc/iSSUGRUVCyzOVXUO4zcCGEmpcoUS1aeiteSast4MqhkmGUuCxBEVlxkakpCfGRK7HpKoPGy5Jgh4X/+BJ6SjFdiYsLmKDLCbB0/PZyP6lzTURDZcGMG'
        b'2wA5Yelzf7jb8foDW2lTivSqtKtA+tbbke275VzsDnGd6f4fyOep9hy94b6IsrCUsh8uEC9hKVg4kaIuVCCFyulYSG5H7CNUB4UzKTccTJWiUGWGjqBmtXB8xO/kdoqh'
        b'jWqIndcKibPoGTGSiLib/BrmLRfLq2XjUAePaskFwSxulhH00NxhnmrEmM1ayzMirm5LOMcwuFh0hC7qCRsqnKbws6w5tZmCJWIoSiWXw9CzLlYO+bqQt5WpL7DwqjkH'
        b'NdhYC7hpUKFu65BOKzWEwyYS/JBcDPH+gunoEjpLnQUvi4ZaVsAkqGVlaJEfAm68m9p4YzhKtbuRK6FP4jCKXHDbE8GyV4BOz8VNIEyq6yhDVsBUV0UbvG2whA5ttt5Y'
        b'iMkTYlmvSmwGuegAQw2f5qEROvBLbjx9LXbhN0O3RCpMZS6LOMj1DcBTUAGF9rDfaYoLz2nv4DfBwThqdrEwdJpvgCeW8xVv1TntnXwc6lhJS5+Mjs/3DTBcp3wr4LR3'
        b'8fFx4alEzYMuQfZ8FojFK9gLitYF4GxLvQYdNwq4BXoaJgmR1D4AmhJDmCudpfZ4BqhC5jzKHYmKhehYLDqYuphOPGRZDPV6rgxhA3l+vr72fNJsVGMGl1C+EbRDu68h'
        b'yvc13SDRgnZU4LMsiJNF60+HHqhIXYXLitmBdj+hKBIzxtEnxBryvKAwCKdKfEOglVKnDGUTAqW2OIHeagaTtCAH1ampQc/CSei0lFu41RBqQlA9VfeLUqKhQy8VqhKT'
        b'BRwP3QIr1BFE38yLhnqJGM9KDXEogGUam+kK28td6DTxu6MtXJ1EPzojmIh6UBF9NxKVoz554jbopq7bhNqCCNiL+plFLTpvJ08yhmpo1ybfZQomGs6nhDhlFi+HrokB'
        b'tDx0UWAcDaWU0PVQi71vQJzj8JnDQnlT6gwyd5d3wcmhgXT87X0CQ7wClNnZaHWMhjyUCR0cHIuToMa5kEuX9TYDqGHf6qYP+XqJfSgbYw7KuCjoFnNwDg7H/fzHH3+I'
        b'x1HD0rQfF0TERW4bhaWSVAK2SkLtUY8tN6hAnar1BkdRFu3oNqjxJCsO5buyFbcXdeNSyKLlYS/ks2LQBah6bNXNhAI6wttSoUbigLKgd8iys3TDpRBJMAY1wz5Wikbk'
        b'U1YeaoIstvLKUNEquvJ2ojLV0nPdRjus5Uc7bOo+P8Lu0DIbLMsxa6peXyPi473QXkU10CKiHZTFQZNELEJlSqKJRBeZKcglVE6WuLaR9iDVnLGk1bwgYnvcSq8IOzTL'
        b'hqMPnzGkD/Wf8Y/QjguUkcEmFSxeBX2YVhZMVtFKTCTrSD8UoWxioJIF7aoqXBxpYXcVHdnmFxEXu12Ni3XfeF8gL8R79anUwPjyvs0j5xnuvfPZ/YGwMclOM27vlHfn'
        b'JMoN4izmn24cb/mRekW0IWozvLXJxNb5xhSDw86vz+HUAufttk7jbGxsnpuwZFlydPvUj94ofO2X13Z9luHU0bXbfvXmFe6xBR4TD7xSqTPXZlxoxqt1M67a350WU2WV'
        b'/84b5iEi08RRpjY/uGQt3fd63LWb2fa7M4/MLBJ6u0X++6Xm9JXOzskHPF69mt5jsfj9ZP/yhvz5G17UTX/4+agbfvIr3y3//N3jx/cZvHjw14e16/b+NNfms5/mtMR+'
        b'PGGxyb2ysAGrPWVmLj+eP1mYEvbpCW2jezMa+MDt78dMWOmqdaBiywsdca+8/Xy8oM/q+Drr6JBCx7S3f8rzLT695sDxf6U7Rte4vLv1jb6fXrM+2B4b5Bk/Ojrird+K'
        b'/7j+2cWEnY32z9Qur9z7Uvtry6PM395W1sh909zsadTr3Xtc69a/E0xl8sgmCBr9h+mZl5K2Trhq0+u4/oNCh4GLNsgo48L8xcfvTN5mdWRy3aVj8RkT5h0vNv9xTO88'
        b'01vN6z8Nqm7k7oRfGeP2Ua/62yc+vqwT/PbF3s9vjvFMnZ1enp7w8e0VB4M1Nz8b372nuC6gtH1Gl+h835Kk5jM3932zKaJr99Grup6vaQS+Wfry6uK63TGrfVf+MSvA'
        b'7lmruI+urnzQXDJ91w/3yiruf+y6/+vqTRNf2LPddUGl0QvrGk/88e2b+3NfuNfvfs3J3X3nvfTDyTd/cN4fM/vT378eZf7+7J8LYsamp5XI3K8d3By/cn9+muFv33gu'
        b'DRiVv71/5Ngx7qU3vraPi8i5Evbm+6sFejozDXJDzu11HYg5+8YfcVck2yaWjbX91t1+7Mqm8Z6pp2o/OlobmPjaqOlXTv92xuffcyfOr8t5acvL+3ckRQV6ffShyfkX'
        b'9X69mCadx+5HC6DWw9bBnw+GE5jEGwW+6sHMNW63P7qMCtA5svvjMwHyeXkEJ0EXMalDLRRTL3DWULrN1ttPQ3c+/nafYPYUdJldb5ZD3y5iDeGPqphBBPVW3AmX6K2q'
        b'RYYQFTii0zLIJMbM6hH8eFS9gWoGYtXhMInk5Yg60wKJrfJO3sYZtaSQTdQCelEe/tBBOisK8v0cUF4gNQVA+xy97Gwo5FeDC8e8UQsciGfK8UxT1OWL1+pJX6UXZ2bW'
        b'gbrYtTsqgXob4tINzsmgyF6dUw/jJ+ASW9l9Z3Wk1DfQ3ttOKuXVZ+POd/JwMQx207INHFcPDe6NDxZophYlpZDFXMa1oGqX4RbrphkMhluJemn1aSgXLtFLYlRvTO6J'
        b'6S0xKphDqxfBhWhyRTxuLrskpg7tLsEZOoajoXKFrbckFLXgjV8UI8An3x48vHTqijynEgWHv70zHFI4vCMXyKPhiCjJEe1mF/X7oDeGaj0DeYWittaN2btf1kfVeJh9'
        b'/OHyKl97ct8boChhIhxQm4VfNrN6srHUC0XeDmuhTQr5vroBeIp9ec58kQjVeaMqhRPuVNQPHd7C8VCiqcigs5CHntDFVCGFDzTMhxY4BtjP1LbzH1KXxVQR1OGjI4dS'
        b'VGAwHFa554MLPuy+G+rgGJvHVpTrjQoCk9wcfPztvP0FnO4G4QzMijF8QSY+qU7K/eA4lBN2SnHTr+Mi1NiEimn5XnDJiiqFClejbF8o0ODUNXltOAutTHHTHIw65X4L'
        b'5xPNjHCTIAOOoDJGI6fCUB50pMDloGQSqJ0qtlGtLmvWRXwM9UGHI3EvnGetVNZucmXU2REMZ6grUjz/R2gYeDU4LMBUXmLG7D5qDaEZn7+lcNHXgXzcJEDHdLyoUcYK'
        b'OO88TIlN5xI1QgnTYrugPFrG3OnoOPXwinajFoUuGbocmTkLnvRO8lIILUwTPUIQZov6mNVEuXASHlFba+pXVgjVAlTsBpdpvxbikewiKugGKyixJS3rEKCGdXgyyJ6i'
        b'buHGbBLmwG7mPbl4A5tEQ8iiNlSoYgPVXalBLy+AY9DG9A6XRu+iXnhhN9RTXf8yD0poOtCJKnBbGOwET/t+qu83QGeFULAG2J4j0zShwBNHYqxNWWkxOsyjvIXuzIgl'
        b'i1vPfMafQjVPMCSDBgGbsvIgdBTzKFA/iuqahCS4z1lraGCKmVwoxz3osA0XKoUzdU43SrgQdaIGuknBBU9MSFu34CZnoU6dpEF2mkD8HaHYy98efxO0UKw7yZvOgjM6'
        b'IZbbauE27RFtlQo4jR28M+7BMabuLNqGp8g2WWoUQdU8GjJ+GhYCFN63D0HJHNxpb6IPDKTRLNW4tcuNoEk0YukopcXThaUSzC1KDVEfKwE18bPxemDmQ6giZQcZtroE'
        b'WogjZuU43QChByrDbwjlj00SyTFpCuAQHkEBXBDoQ9dM5g0+NwguEG3dijSFvq6NVhkzP1SprfOZrNLX5WOB6hjbeUrmQAuxkQp2VlhJ1eENxYgtlwJ0hvrChTonjvjC'
        b'dV2fMpm86XGBNtxO4r75INR54/VL9wlHLEQJuQlQrzYdH0o9tP6l6IKePEBKbeic3agOWH+scCmWmPtoLTvgAmog1kt+ocyhOFHkKzy9J6BjcinqnU9HSohyBJiJRozm'
        b'Ya9VsK0Ppp1ae197mwC8xejFCCMhT7Fp1qGT4ayBisYRDFSerh8xZ5CGqaHqsDBq6bdyJdG8EfqAQ3qPkkegK5Y6ZqGz6gHJzHW768gJtpjjRkcGQT8mqJuZlLXhjVpC'
        b'DMYIIR+AGkrMI6BXiA+e0jClrc7xhbbkCFrm6Y9PNzH08Wg/uuxGS5gIeUlDfKKSTRdO+zI1YzU6K9X577UQ/yPF4JNcT3Ry3H9S++3iZFoCfZ6AhNQFZgJtAhbiqS6D'
        b'AImoKk2dqtTUeTH9TRfn0hWYC6wE1gIDXp8+E+NnRO+hj9+Mxk+MBcY8ARwZ4zRRHZrj0tSpLmTYEwH5q0u/JBAlVhJR/m0zGnoT+KgXDDWmdusl2qK+4RAk7f9qJoSs'
        b'uMHSVaPpTez1Cf7zP2j2Mrkeq6G6vSf34z96wNjwlzxgtIiVHjCGV6NyfzFVqZCgN/p2FrIYBwsbckXpMMXFSenk50neMP6qi46QpzewVdnAX8eQlijuty1io4bV+R8r'
        b'i6GVDYjD1zOlx1Nq7FDVaElB7BS5HW1BPySuGP5WvWwWBnTCVRf64bFPq7xLVbnVPIvUzbFJqbIn+Gv4Oy1gwzygHa686n16A3pUDbAhvZen4O7T62LVTfE/aUQ0m+uP'
        b'uKfO9UVV3Q5BCcSt1OboBOrxwiJyXUJqyjAvVf+ofven198/nNaGeE36B3OePPfplSFVZaMHK5vv7flP6Dp53tPruqKqy5bUtTly0OuX0lkK8xbxj0Y16umVv6iq3Dr4'
        b'CT6xlA34J8tKizqbCCeuH57SgJeHTyv1GMGW9T9ZSGJWZ0rCU2p8VVXjKIVvkX9Qn2rrWBcZR3RY4QmJss1PqfR1VaUzSKUkN1OtxA3VyT7qiuYftUlX1ab1cQly2VMa'
        b'9ebwRpHs/7hRw1C3f9MXasyjvlAF3KMKJGFAbGm1p0hOeNeth4TEn6k42u+dD/2EnHif4Px6kVTAQC4HoXIyE4GgC3PVgyJQGpT+iSdTPaURFeFh/yM3tYuL2Wb4yKkf'
        b'J9scHv7X/ZiSCt8mY08saP4jw5HJNQ/zZvrEyv8n87DhP8+DKCA4duoiLA6Rx2vu3fCN1I7+sDYpTsCJFgoWad8YJLPHx/kY9/fGeeNj3NW6hIS4vzPQpMaBvzHQjdpP'
        b'4+1Y7aqRJq0gqnQibjFV+qD/V6XTMKZOF+TqqFTp/D41PAdCPAc8nQMhnQN+p1AxB9FD54AoNbXxP6dhczAuQBHRtlRPngTtDmuUyp0EMdVgqi9X48R2KzjOIyJu1uaZ'
        b'HIu0ewAOwRG5brIltGqS/LUCB2sooa5C5kKbA71BYd4alsI+gmrK8wsgHlCWLVlmH8pzYSZwykMDnZgMWdSbOZxbvsyXSKIFqNjRx59dkcElOIlFPZv1aqgZkfCjzC58'
        b'/Gx5YgDqRE1KDdU4dJqpGbEQL1MafaNCaCOrlVp9h4+hakYPdA4LZQW4Ofa7yH2UyF6ABbuzUMwwvpe2LrSV2kRr+StQ4YEom2qxpqPGaFsfKqIS9JceVEJLjFA2H5UG'
        b'02JNIQsaqUhob4fKvUWcpgaPiqFSjaK//aJtfL3t4MA8b1ysSICOma+mQ+jlBxfIbacUapKxHKk5k0d1S1AVC7bbxvsTvJd5sL8y9lqROVWT6K5FVVBgHxCHG0GkS/W1'
        b'vBFqhTo6ij46KMsXir2Js0Y/KKAjDoXm00icdNvZalAEJ1DLMIqTKCluwSDFDac3gco1nZLWtBitLcfk8xi9Ddt7yXSJH6O3KQGUrBqdRZw4uEGEycrOxWcOI6tFCdAj'
        b'D5ASJ9RSVfiZSz6052YoH3XKvW2gBBqkSlNvdHY606gfQ5mBw+Zovy+eIshLV0Rlhn44IPcLcN+ovGw8CdVMy79/hZqcWJXz6YZiwdiZUEZnLWAJ6mPhn3jP5WECR1u0'
        b'hwY1ToAclEU9F+XgQgtV2JosuEBnbieqlVFgVICnvwIYNcaAfmmNatB5PDthBHEwGK7MCPrSqNEBjTCLSb5wOjmJE2SWnKUR2itVo/1LU4MT+Ft0EvqHfbzUgvYPulFb'
        b'MsElzY8gZskUluThTolzlXvCYJgygg7r0yaAqFn+TOvWsMuOYOdKoYfirSjYCvb6pdK7sD5tU1tcm4PUxt9Bau/jL+DGQ4kY5ajNhA53FiS7CerjfP3mLB6MOgYNkCuj'
        b's6mH6lCrwnZeYL2VUxfzJtCqTW0bdWXck+IESRYz43to8aW+JmYFoQKK0PAj98i+ZAdB+YTwE3DG5Wqb8DovSyXbMeSjo1BH1BwqBMLk2MfDEAWg3Rq4s51MRz4NLkIF'
        b'3kw0UL1yL9GzTKWXkiVQgkrpXjILLjEwBttKUlEfM9I4jarH0C2rfeKwXUu5Y822pYOwUYIbQbYc0xWqLQdy4plS9RCmoRb82TJU5K9CubjQkR2N+qGH4DnGo8NKtza4'
        b'5U3MTcVpTCj5ZB8gY7HIlW0DOQr/BlKBI9k8IBv1q7aPvVBI6VpNgn8twBuHYAa3cyMUw8lxTLnvE2brb486oB6vLVEk8YnRFMdmESpQE6Ytrww7ezs8hGJUyWekW1EK'
        b'2Yr2qD0WpMlSNpPgHpKcaVPnQuE4W2t0afWQ6GR6eDIzqe7dXYqqyI5lhcqGb1qqLQvVQz4dkLX4HGnD1NC+RcQJPBygERMvKkStCjU4/qRXDm3q+PcDHNQtR6W419Us'
        b'bPOZuZZQjt/sdLPj7OCQGd2ALJIlnKHpAwGnH+F3bamJIvx4IO69O9mrIuy2hInZw95wHc7UI0SdWxLh17h+DHu4M1KT0zesJt424u55Gg/3tkH5EvKPtC2DW6u7Q5Ah'
        b'SNSO4kLxdpnERynFOcZ7KAKQC7Y8wlX/qukeI9ssS0tMniPTVDiAEHHUrGQF7NaTb4Fhl+Gwn/i/RRVQDiV23vZ4uyyBg8P8bEC5EDpQuYEvKnPSX+eKSfh0OjptpLZw'
        b'C4eqlhrhd81zmJuYXIEJscnA81Ru7+BNfT/5LF1ibwn7Qr0eO2DwUungtQQECNWkHYFyRrAjvRguoQOoAVrwviy1xwuU6oKoIsgsRITOQBbKptr952wxVS2o0cBHgfbu'
        b'ySuIqQC9aT2Ij/h65YxPxfsKmXLInkgJ1no7Oqaab8wNlKLS8TGxbz94Tk3+Hh4oU10DWTC1C6g59N75rZd2bv8qqmZyXvmMV4XiwIUOvwu8vE7lHzed9LpLvllD23W/'
        b'7BX58R6rl9TVH5+fsVhL63Jmvk14pnW3/O2pmtKL21/tuTPns1dfynNq/2RNyaSfHiZcWzdmxXPOJWt7bplAl+EqL9/VLzjMUZvmO/XDgdA1A5azvrIcCU4yW8saqfG0'
        b'1mfUYxJTPK9++Nrrxckf20X99nyC1LIqoLnn81dKb+wx+2znw8Afnn128y2Hvpuf/vaVw+cpQZM3plsf/zL5FS3D+1av177aqF3hdS31luWNW6+72nxq/q+E2OU9H07M'
        b'aJ24o3GB3UfgITux8c198tuTnzUvOHRVZ1T0zdYAdT4xyvzuvtEVv/v8uq9B3F/5cPe+tFXx3y6aduBAjl799tdfmejrc917w8aUjJ76uo6DkztWT5k9M0F2JP69Fx+m'
        b'+vt2NH++Xn/+yOgpDzW+K/yp4uC+SN/0qj3fVI055b5SsnLiuulT7kisE0LvBOt+VpjQWrBxtnOb25XPvHfsvThvo/Cmmd2St6WoILtB8wPLB6O+L33X8rTvqZ3z3594'
        b'3vvutE+v6W8ecXTSxflpxb3n0OhPH1q8W/+i+8K3zu/asNHe4ocTwjGteR9Ehn06clOVk9vX9U3ff7bolZri0Kvncx588GaOt9mFrZ962cm/PGn8a9fVkCPd+dPX9P0c'
        b'nxZr9/Enmqbv5nQ5nDa4tknn/drLXjFr77UbTv7p2zHPf/PR8s6br+lPGPv1y5/u+/L7DXO2BM/8uP3mCw4gCdnb9OMLs/u/nhpSafv5+3l+dbrTiu89m1rpJrrU99nV'
        b'vrg18vOOy8a5P7cr86Wfw766Udx0aqvbF/EZd/YeWvVHRdKDzg9+6f7t1eyWHL9fn0//1UG2vO2d8viidT0PzRu+iHQZMNl8u3tEzIf77536zeuB/sp37y39vKkJrR84'
        b'ObvbovDB2U37jn44a4nLve+D1Fb8vuxmcKLFlF3CQIt1X3Jf7rrde7aqqT+j6a6jaczkr83L7838ofghb5juenuig3SmQpEFbRsJ1Bq1LEKNIrrTX4TjY6gmwh2d95FA'
        b'vhRzHWXemtaY/8ZM5gjUIERHIFupCTswFvVKbKTJYmin6lvxGD4Uun0UCPlF0KwCHcMZ1I055R4TqkNZhJoSCPB4KZxTKWg3bqav4qb62XpjrjoTSlVa9PMRtERn46kU'
        b'Y4vPllKV4nYBgyhC5XhcPOGrjjoNYat2oxqqdUlYis6Q3ngn+TlK1Tkd1BSEc1nJrKgiErA4njVEczsRH7F5Q+DHkMciIxpDJapisTkF6AJqYCjgfKikLbecGKvED2tB'
        b'NYvqmb2doY7zR6I6CYV88auhOFgwBw/YcWbtcdhLqMLPL4YmdHFlOFMDFmjCQYl1GHQMjT+L+qAC6uhw6KIcLEJh5ivPkmlFCWA8hEXtw3LAPLkf2jtLiivCW6yvGqel'
        b'zaPjUDySaaGyNkM7dXpghw87yOfU0RneCV1gSuh56PBoXztrdMiB+aRg0aHPr6Gf6qIzqEcFcnfVU4Sf9ZpBezpxiQ+Dx09DRYq4tTvRORa6ew0Q4QmzX6gT/4YnSTRT'
        b'gNqgN4lWKpdyEgcpKvRWYPMpLj8P9jGV/u4QXg753qhkqTdc8OU5jSQec/LzFDYhoaMl1jaYs+5lEGmCj0aNnkxH2IlaUuRQuMTbPonphrWW86h3xVI2TqU7oEiCTidS'
        b'BWc52ofbfFhAvAR0U4XqHDc4ygKB8jPnGQomzIMTjLi7ZFAp8fGH8i226liW6BWg/S7QylTA3Zh4T62CY3JiCOjg66BF/AqaovOi6cG4LTSUcx86hHKZIakmieG5SQGg'
        b'NsS8NZRvRwwQidveTVDnSrDzNk/fIVBn1LaUjusiOxcKDIaaGIYNZrhgEmhYgX/tM1LCGlE3XFZYrfTOpldUfMKuoaG8BZyOtQFzHnIQFdEcM+3QBbIuPKFraARXdBlV'
        b'oIMMa302BEokqTp4Bho0WSRVDzhJ52b98s0E+05sTPBOksupLRRAkQfKpaOYjopsJNb26ATU2ygxresUuHY4jho3qNx2nFZHjRMjaWUeK9A+BWYdNY3n1I358f6Qyeb6'
        b'IDqFLhIcrNEChUEJwcHudGJK7pOGqBKT2PhoHyUOVm0+09texMuqUwGENR5DOqvCwaKGUNqe5Wgf6qfhNXlnuCwVmJtBFTO56Tdajc7NVEzmI6BVd1TORugyOogJjaJW'
        b'R6NOGmAzksUynzV+PTXYrAzCZIj7q+HLW2Lu/AJbp4WowIEAadej4w5KIC3KgywWXzNtmdK/DeRAATPp0oVyStpT7VOJ6872xAC8d2OOTsBJ8DKGs+6YhKmIcnA52o9z'
        b'RCUT5g72Uf+eZ3ks2B5HvazRRabQT4Q/Yp3ajhrRCcGSJRPZdrvbZqtt4C4nOyJFUCMvCVzm4cIKGV02uriMSxIbKMajNd3VX+CcMJpZHpVyCvNppb0PtG9zEWrA8XEM'
        b'0F2cPIkYuJGNatDITWHihte71Pj/M0bvURXtf+9Uc0CLoKXCKWqBsvUvESb/P1837uIMGQpWRFGx5KeuwIqqxu0ENgJzqionmFOCjeUFTLnNMKi8ujZvLTAWWPMGAl2B'
        b'KU8V5IpYn+x/bX40hQsSZTvJMxr/Nlqgz5Monwwrqy8wE46mynItnM9CYIb/kpL0aWkUucuT68lt0kdVzqS34Q7uVEkln+Mw2HsmrIgGNFPSomQpkbFx8gGN8JS0dZFy'
        b'2ZB7038QBQMLQG8T9flbKh36TfybkIg8BAr6F25aM7k/mHdPLfoz1Y9MFKqBrifLSP9BPoIDaA+VkUiAWD270ShbKmRSZstysa+PnQHaz7wlEVdJeCfOpaALLIN0xfl6'
        b'pijsJwOVPhxGo5MiVGAFpcx5ZhHKch/ShkCF56Vxs0Q6qBaL2lWoUiH/aEAh6sTVwUnUPFifHuqg1UFRzExfqNR/cnXuqCSV6GRGor1w1pY4c2mx9vJ38PZfmkhGhIZt'
        b'IW4vBFxEZKCReCI6P5FeUmGuqB96fQOGGOxDnXQXH+8yNpUYDQmhysMXiuwxKxRMS5rqstQLNwEzfBWkiW4T1Tko3EB9X8/DO875obFjWNXWQy5K1qyDLnRYrGeACmin'
        b'LCL0nzw20LkOKiLQJXrBbOi7UP5IUSEKl9T0bg0aN2KmJ3qXGA9oHpykMuZict1omqtOZMxayRgu9tnWhWryDryi7xd/LAuanXDDw3TnNxkBcS/8svFGZ8DLy395qLVv'
        b'ROq9fUsmTRxvOb8yaK9EK+ANS0h/1sjV99OiunXzxx4a5TYt5bPpP062UH/uGfkdbS+7n768k/7+naMPvl6zTzb5nO1Aw3ztS6LXJsUu0/7g1W9j0Pf5H0snrXH61Nry'
        b'VvZrx16qKXF+b62lbmlMmTB2bO+yig0Hl/109MRZ6xH9N9eE1FVPu1bXt7jnu+8rlm5rN1j6kvyufvddc8EPr393a0taF3RsaP3Z5ov3pgdF+u9Cz4q+bRKcPq2/wt5l'
        b'xYabqXueM+naaL1/xvWZi0b8Me3wi2dCL7xUv1G6tLU7cpPgYuR3Xat8s403vte+o7oh9gfnZyU3dzc3v1eq1TXjusOWxPVI4rpLdqClYpTx3bdeaml2vebjMWD8hZVR'
        b'0OIos88+SK3LaLJvnvbN58eaYpqvhbzl9OO/tl38/uUVzztNHnmo+peVpTedXhr9icfZq/cnOJ4euH9hpOOD0u0vuP376o6i9xb6jLvqaJRxuXz5ea+Vz35i/5XvnBHe'
        b'U74S/PCmLPXKEeOqyT/PzznrofH5L+s+KxC/Ip+y/NrRM1bPO6zMiPsutWD9B98vgaRCuVu0d8srxzed3NRT3rfeatPA2y63ZiY5/xFleOKnlBkDNZelB7yutN0tgS/f'
        b'yjmQt3/LJ9kHx3oZB4zbdO7WFx8WfFB354/R3dO+vPtR15Zr9ld0310y/VOrepMCri+1OfHjo8bea9++5pdTpfGicfHmCeEzeoU/Oli1m0VrLn7w0ug5DyYbnXQNyVtY'
        b'4VzZ0HvCvPCq36VA+ORUXnriQa2Y7wSjuu4deyNY77sdWvWRk41ynOYKx4zaMuBy8faIW9s/Mz2bGP1dcmBu0znzup+35/7+tnvspPj3Kp2/+zDVcntvjvur/zZ7b0dR'
        b'+bSNRT/M++aXTN1XZpnrh97qGoUOPrfhrTHX7UxLT5ncHve7mtkNvesJodIpKWSBoXNwEa99avn2BKvIZeJBu0h0wI1ZoLY4JEOHrTTVedAQE2WNpdzIIm90mkqTJ9Ge'
        b'QXHyhJhJM72p0K40AcQbUynarTAC1FzDZMnmsaiLSH54nSoFP2jEnAi1FO1YbsosRR+zEq2DJjjniKppLfNQFqqXTwl9jPGGAmPKAyYE4DYG2lNX53grbZ2Hd/Fs6gfd'
        b'3kpLwegbCqaiYxPi7akRYTBqnKvkWMi1OXQyR0dwQIR3rB7UOQ9OMa7/NFyAnImoUWJjy3zK4f5JRvKwBzPgR1gXWzahJmJ9jjf6JKmAU9sqgCNpKJNJFEewYF0gh0sO'
        b'UsLzUiPITnSJsk0BqGYZ5MbJFT74iEWq1lYeNY+DZvotFovReblUc3zSoI3kfnSCMnFpuIftmOtV5/jl5CL36CzMXLGA8WpLN8tRvonKNZ4vOkmrGwNnBGSSB61p0dHY'
        b'KOHCFJTP5K0jaI9IbuONxYITZH+lepYsjS10HESoCPoekSigeC4VKZw3MS6wCbfjFBVJevC+O2hIX7OJzmIwOh4LBQtlw8wgqQ2kUIEh2IsPhsuEa8YsMzoEpQq2GZWj'
        b'LEamF2diMdQmCVUx11ZYRoBKqKGs62K0Dw7ISYgIILcMRULc/tMCVCLwYZNUsMOMXAUUWbkQcV2IsJxwKBg6WMtr58AZiYN/MsmATqeYWuCaRxgKN87aQuvdAvuMiTSJ'
        b'h80MdeCRE+vwUaOs2QpowrWdS3VSukMcdIVovjmFqMb5JMimUIrHgBSB6PIwLMWoQNoTHlP7GdOJhGyHirYzgNnP4xUFXVS2PRhGKZuJtn6why4FOaoNw/LMGnRQJcFu'
        b'mEh7MU80k90KERaceLMM5212oU7mrKoBd7wHlZkOx6EoWHQ8r/W0iElQQ6JQYLYhLYCs5kABZE6ACirTeG1CmcSrIqqDRpUJLeakqukQu842sEUdqG8YjoOAOHQDKX1t'
        b'3G6LF4n5oBBBpTUBZyoTjd9gxTpeCLnEip+MoDWUExIVz+DXwYkltAuxqN6GvRzG+IwzFa1zwaR5GJ2lpcRYQGG6GhOc8XQTp2xafjwqtbSmW5LFMrQXl0I4HZRHlTf+'
        b'4QquZMoq9ZFYwu+kswr1UCl98h4b6KqG9iuti1ErXGbICMwI7RrGZWrgBdiMjq4STtUeye6rinZs8x1SM1V2Z6ILRHUE+9RQp8caWpQM9piRkgKxBOigCGeHzusJhZao'
        b'GB2hE7UY9foRsI2HVIW1QfWwR2rw/1Go+l+5JhrqekhHaTXT/dfEq3gi4oiptTH+x+vzxljAMcZCkCH+i4UgLAqZ0pAGRPwxwFKBAS+mwpeZ0DwZi0k4ZSgcTa2MTWnI'
        b'A57YEvPkH3UvhMvUJmleLNQValNrZ3UsjhGLZQNSphoLlGAgEPGsRrFQzD9uv0uFKYXgxCxJ3v5fWiArBCebYcP43t8wUal7uvkxbT6xAzN9knueAaNw4jVhfQqTD8OJ'
        b'iwQSgZm66aFee6ivnnj8Y0BDYYw7oD3UOnZAMsRSNXk0yU1wwclryY+Z5AcJNjigqTL9G9BQWOQNaA81lRvQGWakRk2iqLkOHRA2/kb/d1cPg0ZK3bj66WQ+1uGUWFfE'
        b'i3g7gdU66uxH8D/9yWsLtYVMED0EWf6PCr6L0wTcKGgUybBE+GTrLjLw1LMNp4o6raGy9OL/uqUXOQTsuUctvZYFpPrj37egwmlOU5ynuU51ccKyZmtKSvKWpFQ53qFb'
        b'MWd2cC20Qxc+Fc5Dh55YW0tXU0eCStA+fCCUwYGgJbAfDoaqEWdqPRKJZDa137D2hD5Ca1NJ6NEjU6FOh+p8dYUjnHDl0zh8HlROg7LlzLyiHe11c+KJScoGVOk0dywt'
        b'QgNdNHRS5zhnDrKgwVkP6phT/N4Nxk54qFw4OI+OuqAjlqn6+PHy8FAnPLeunDU674oK5zArkl4sAfc74QGdzumg0umR+swtRA4ch8NOGhw3g4Nj0DLDG/awsrOhNgV1'
        b'4N9mcnGrZvqjMlbMCdSmi7liLEhzk8RuqFRGmx3gC51kKOdzelbzUT4cYmrtnjVpRCfsye2K80QNqIgq+I3QKaiU494s4PDJembBBtRGn8M+lOsjx91ZyOEBblgI+Rms'
        b'lLIFO+S4P4s4J+ki4mmANeR0MhyU4+4s5sI3LoZqlMvG77Kdmhz3xou0tN8rLZoWjS4RsAzpjDeHMgO8UWUaze0yArMXpDM+XJzEB79iY3IS9eFRIaK3L4cOjvCFJkua'
        b'fd0stB86cMv9OFsbv3Eoj2ZPxPw1EF9h/sQoI98f8tEh2sRRC3C6A7c8gIPdqC9gHvPEMWoUoR7c8kAOH5KdgZjhqaLFa0DjGOjAjV/CLUfVSww16Wyig5jJJOr3pVzK'
        b'4qX222nWpajESILbvYxDXRrLoEiDdb6fmy7hiaEsuVQJSolkT4+rQ54EtzqYw1xl8ByeFjtze7IEtzmEG0+Ce7THs3GqQN2QKcFNDsXTMSN0FRaq6GBfMoAcCW7ycs5y'
        b'1nJoUAZlyIMWOwlu8AoOmhNXJKO9VPHtgvnfClSAf1tJQpllrYSjcJZ90InKF6EC3PBVnEfSKrQ7mFa7JQi1ogLc8NVYRli/GmpxdtLGLTvCoBw3xoFz2+jgg0podyJR'
        b'hTeNpuLIuQkcoVzKiOcUZqxyiV2SJTd5viX0o2w62Jsxc78HynHZtkQqKLaNhzbWpX5b6A/CIzAJs6bZk9AFH2Zi156O57gc92kKB6WyKdCHGlkFOVAfS2007HCnYL/d'
        b'DjtWTpaRTRBuoxUXD7VWmGOrkNpRRx7e0zGdEwuFAltHKLElIaqE3PzxI6FGCL0OUJZKHcW26qAi+g7lQh3+RYiykrmRcE5IYM9a1NLHLAkdpMWgc46OqhyklMVQnsoE'
        b'jk4p/pbUIxQQ37nHDCfh1zOhhlodiqRqrCFiVEnzGODvC3AGqE1ntkRHBOgCbQVUocs0C88ZjiRt6LWkRUwhulbahtMhjor3AvL+ODrOLLGKpVj4YN3VQCeSOWdUNBL1'
        b'kEp2Y7IgrZzpirppJbYaE+AkVLASsIR7gjZiyzYoZVXsX+FIR2u8YiA2oSrWTFLBbsUgWfAc3nZb2EBA03jaTDxJFT60EJxpAlEGKDp6AphxHNSY+NnS2RCiE+5E+VFP'
        b'+7kTZdE2Wq+dyzqx0pvMm8Y6jnVighX93B/z+ifYQOULaQYD1gv1edRmDJWPwhs0q9+WdoJMOj4ySlhPgjXYrO9Dx6X03QZ74kwCb/oX8ZyiBpxlC540MqD6qC+dNjMf'
        b'ypR53BUDMl1Kx2MjypnPRqzdio3rOgVhREIPNQFbiDJnsP6QxrJRxXsR5LNhQTWok3Y72hbtoZXtgfZkEotI8b4og01uK2rAq4gU4pNOh59kYyOzPYxmSdyGzpJOozK8'
        b'c7Ic7ooJroVcuiBmjWIDgv+2oGJKJ7XKXqNjUM0m6JBHFBtg/N6Sg1x0hvU5YQp7f3LKGvZyPqYAbdSoJAB0klLAGmdopiOLdpMxS+aM1UaiA6SGy4zWXdExOe0qfe/O'
        b'jYNiRRGd0ES5k11YlGdTqFy8Qm4cOqgYkv2onPnpyU3dqRpaxdrj0G4PNio7XajV4/jlgfQF2pMM56RsPCyWMlJtQ12oQlE+2p3MWS1gHU1Gu5kBc7/Ihs6ZULgY+jjD'
        b'6WQQUBcd7RF4XIppvVuMSF9rKf3QbqzC+xUFBvSOnkLKRmXEoJhmwRMyiS7I0bQFBqjZgtZ/DO/XdEkoFn0AXKa1wAXTIDYOB6GRTimrhoyDQMasKw+nTWb7hYWAG4tK'
        b'2KZRKKFkjsW8VmILbOuYhPkjthjWKfaNi+gwizCVpwmXWSU9RAq21YAsJZmjs9DP7vz3cgvYmsabCe5GGBykpWzFDSU9CY9YQ18jLImzjXadoojF3nQwgtFRd1ZJ2XgF'
        b'9SiGKx2xIpbjdVut3L88YR8cUnQ0FXqlArb91KPz031pmEwSUA9PX7UYneNJBA7UeodylqXJHtT0LmIdb/UttSyOiBPr7mT2eJCkvUJDgKWUJRHaD4NWs4dRIzQzCjkL'
        b'YqTnZ6iTxB7+rjkyQIf3Ip+vSZy5iD0MnCrSnsfrEyt37fGJnuxhvqauxU88ZoynRNi5z5rEHrqbqNvFCk2JskJbI9CJPfwqfkRaJ++BV2qEXSS/hD2s15EYe/PWeLeJ'
        b'iHPTMmYPFwQbiV8QLCEVub8dqfh8ZKoxPxef87jMjLsuYi540Z3Dh8ifq3PvONE/P8xlPNLyhWST4RI4U3QswUTBQKDyJOixxadqGjcWdqdBrgOzKGah65e5scnpxEzn'
        b'MAog7reHmS0Sbp2y7YT4YhSGiyyI1WBwMAUcY0AtdnOULE0Zu0qb+7PYVXpag7GrZlOOy9fXNgCqxxE7XWoS6O8XCAeeEBBMFQwMnYPDknmY3PfR0fo6duX8F4QRAjyr'
        b'2w6EBnNSLRY5bgRvto5nZPGi1Xo2sl7+2qtyGFn46fsnKChgrOa0LxVksWidBnvorzZyTitHySIDzfFgD4tj1DKw1E9myy8wQo89TLbUNYsXULKIuzDTlD285qixLYCn'
        b'ZGF3zUDEHpra6Ov/wlGy8Ls7YqpisjUky4w5ShZ2L27KYA+rVhitMhdSsjDTjDBlPpR+9TaJfllBFgELMrC8H7yIvpgWJtpoxZoV58lHstw+ozRW6AgYYbqHxrOHvJbI'
        b'YaeCrt+Kc2MPI5JFM7rYQ78SHVf2cN14tfECIX1o94ojscIMCIid4bdQTZ6CZy//y1Gzl/kHGs7Tb/n61nu3vhlbeevWWuP+byWGRn6uE30Mk64kTPyoNW9/NkjKLC0d'
        b'Eqs878c662qU58V88vrJ715I+/721Z+FM0bpherthVN9Te9vD7m/7biu5mjd5BdPciYLK5YsUgt5c8liofnz15+bkdGpf7xIt7fKQ698Rs6NGXs6ZuRKj7ygtua5SWue'
        b'd45OVFs+tWBT98PYt5aUBR5ZkGP45e9eAQdmtLmlGEyuOGswq/u7eTFJXx9wfWlDz6frpwWUrS/qMb/y0u1lY3cACOq2fVJw1ffHmUl1A9/o35l5Jyh3Ssnin4xnjcr3'
        b'/8hl1PTDxkfyb2a6Wvnvf6/1GV2TFb88d8U1deHqpT4nP/D8aIFt2pEkE3/vblnp6QV9edWG7xQd+OrAFxc3WTmHbOkZmBT0ybKmn96Ky74c4nT/PbO3/Wo2rbmVdMo4'
        b'6ffbobqSz/+1M6vx3rY1z5dfTLwebpFrLA052WPpXenxTecGl+4RvVM1L1v2NLzQM3HyDeeow7Mu37/yifr2FaXxF1/StA35be6Ca7OsV93e9e/3zO+/WLhweseOl75r'
        b'mxzU7nvra7R+VvsvR0vqgvs1E1+L7jj0UFfz5cir0/yCtlj/Ky9g2idp0f8OXqi2+fufK42vzM36vmXM8y9cjF3Y3xrHb95r9O6d0DP+BaurXtv23ejI5zsnXbb/vPhI'
        b'5c38rh77mxO+fvHItRWydya8/s07Jvr9lVt+TBp7QfSBTKu566W1fXMr6xZX/6vq6pK5b+8TbpY46Ge8NfnmyZKfzi+u1rjyoLNuyjN7LizUfe6TO6GRHm+NOSOKspoh'
        b'3qT5XfbvgQvinTxbVgXX3iq5WRn2WsW0SzdP3H95zBuf92WEX7lg8mXwwEONSdfevVYaKNWlF7nz8Fl1gNwS431CTQwHObUMAZxC1ZBN78FXyonhIPNaYR8v8hKgji2R'
        b'9KLaEBWS6LRQsnSqrS/xKC+BaiGPxXuqKLCHUh0SKRAuYPEXOh2EWgKih6mlL8dDY4YtFKMzPvhdH2SJogT4UO0dyVQMtXOCfQPt9VC7t7edt4iTbCGBGKp1aKWhsB86'
        b'VdGg8J51gVrfCUKYIWEmuoQ5sGJH4t/+wCpRqgDyLEdQbc6udB1bh8mYnytS43jUIQid5kMv1E2g14WZ3RGTO8yw7qNmd+gAYqZ1qD52vK2PvR+uz96G2Ner83DJGV1g'
        b'UUC0d/pSAx/clFPotMhEgGpHIea0A/Wjqim+gegEOscUavPMoIvBHg/DqUgaussBH/vVosHQXYcgTzrm/9aG589vPzX+5iXzgJZ8feTm8Nj4yBgZvWu+TA6+v2LKs4vz'
        b'Fyn8Tzz5rxbPfFJoUaMcXaEVdUtPPF8Q0x9j6r1Cl7rIJ54xiBEP839hQIx+hIb4//HUmwVxUK9PjYZ4agykRf8nZkTWittsdk8twvn1BQ6C5Nuq+03hgDA2PmbI1fJf'
        b'HJ5PVVY3pKw+YnVDfKr/JaubTO4F0yEXyJSRy0h0tQ2wRz1Dj3c1zjhMJEa9o4Z5DlZdPRIfEkPAjgIF/IyP1lJ5DBb9qcfgx2Bn2op/wy8gzQOefO1JFOm4Tj6a/4uw'
        b'1uxHYa38Y3WpMYhbbDrPiWaQwOURfnobNnPMX2k2ERZmEOGExNpVYCStvbyDvMhC9Vbjpm9Xtw5DXbHTfGcL5MSIZ5e145cRXpGvRFuXfR7xyroN0RFR1pF+kRujo5Li'
        b'1t2LEEcT3HLsLvW9VzdIebYnHEONmmTry3McJyeBbN15E+hH56hKXBsOQDbVxqNT65/ktqkOapTAlCfcaQ9I1m+Qrd8UTtk/uoym/PVltIuzZlEhto0LJ46yw4nfh0Fj'
        b'syElK4laEDuEpPlhlHtHRbmf4d+MtBQBmv8i5WZyX+kOpd35+EtLElGFOE7zoiIVAavgbb/6MTMxAofyh2J1lI/q0KlQcgVqKoEadMabCpc+ZuiQL+qDejsSvqlQxKmP'
        b'5rVsFtPruzmYq62w1RNCWQDP8SPwvpwJ2ZRc+PlCux4B5V+11y/eSELPksKSsIyZ4+sXEEDwdeJAs2m8HG/K9fQTbzstrkVIWUk/mf8OTk5khDt5NUE6iUlCjg+d6i/g'
        b'Vi2jWQv91DySFZysU4YdF0dGdYu9GkfohVtUOP+Kqda85zg5kSdCbrQE1f8eknp/q5ATqgkmdR+UE2jyS2+Gf8ITzKg8R3K0n8k9szSWpDBhKO6yZAtH89kFNn6iRtDM'
        b'psd0O96R6+FHO4oefvLpDwKe3OSZju6Tk8vAy799GxRitE9ni05iMJYO7AUVs63l5JC8I3mPugE8bU3sP0a27a8V3n7fmO7jFCg+49QPN/Su2l3Fa0VDcCKKn7bsCq33'
        b'3YRpNwhlcCfSpYen0UeXXw24gQnJhpvga3PjC/qobKd3ASaXtdyzn69te4O2Trumo+D12zL828dcznQxfdakc77gda9v8MefcHvHLqAXOdvRkWQo8KagJycRJ0YFeDU3'
        b'8j4rUykHbThFbc2rbIjtntVLZ2z1h15qE7MYr213O2AKFztt7Kdq8uO4BbHtlxaW+Qbc9tDe+1VT8LID9emvcJolnhbGZ2aIStTkXHOd96kRC8Rtid5earXbdn+upvGR'
        b'hd2MV85E5zQbTK1+8df4Px7ee7Nj296c8RPvb5itn1a49/hW8D7jts/qwzcW3LD8wsyoPKutfnyj0eWHP9j0BrTdTeGmGZgEX/580oKkk3e9vxLcCtMTCr/SWPD6rJHP'
        b'fPmvMu1NTavFL5kc+TE/2u6s4FLeM3vX2H5w+0Nfh9iW5bD4rTtfVVz7+kvvhqI1Hbcyz5WNXH5VYHt1dVfUthUftc4KKD3col4vLbvvMPqqecml151bnXfp3lr0cohH'
        b'UkfPa8lXXR8U3tdDH1m/9iC18wube+90Xc865n1p/bUO9e8v792UpG65/9cbt0M1PHqK/bYFuvXdvnEtKzGs/3fj2ZW2Lmav6/0yZsIPr+2f+Y38uom0unHDrKX7Xz7S'
        b'/vLvSaFb3/Fuebnwi723jm3Zbn9712vtNmM350w/tvzbY89MWH9hkU687wPTC51OV+QD5V+NfG1bbb/BQ3l3Znj7setL3vwgQTbn0oGmf5m6PP9j7am7AZt3S1Klsw9+'
        b'aBye01b1yeYbUn3KsgXOQ02+272Jft1anVOP4W2I6zzKXaXOQM2ETWK4RzEqdR/PJyROVkQM3Ya6iZmJvx1mw6ZCs7YAndFG3cyWpF5AQMJkvyeYCg387YnJwfxOdBH2'
        b'sYhSmVgiPiNP2bJFRxcV6+lBOwf52kn4HIWjQlQjXcDq2A+7pyvZVFEU6gnCXOp8qKLsXepEEjJOa4M/OkNMTbIFizdBN2NCcxehU7bRLj4KzlB9GW/IZ9BXs1JRh5Jh'
        b'FJmssMLsoiswr4zo9OogzGcqatOUjEZ5PCo3CacvR0IbqvNNIqea1J4YbKhH8BNS4DgdpoQ5frZwAe1lcBUGVbGASmbr0eq0hFx7dtvDPm8S/1WC2ni8k5aycH9BSzR9'
        b'vf0V47vWGqp5GRwyZlZM/WtRpy+qnU+POcUht1HpabF4KeakC/A84V3bT4rnbRZvuGXGf6lu/ye2zcP4z8Ezj25mVX/n4Jysq0YDLVEeUxfzlPr0ICUhlfQFFpRLJPwi'
        b'CYlEeE1t6iGN+VgjOQnXqU65S8KnEv6SmJPz+C01KGc2D4ryCSea/LmKs1QbECVGpmwYEEVFpkQOaMbIUsJTYlPiZH+X1xQm3yVlfkl+fKE6u0k9hn/77P7afOjZTS+6'
        b'Gv2BuLKFy+OGnt8anLG/yNDTdD2vYNdIl1TcH2FdqMpbEC1UuTngn+pS4zH3MqpbMxX/JwrAZze92i+Ac6gUy4oEkE6uNjEZG6ALQrdkyJq9JjYq7HWBnMh4IlHClxGf'
        b'R0T5343wi7wn04r+ME7AjTkrTHQuGOICRfindgYDOmRShhOXzd8hrg3J91TTLWKT8+VwQ5WhrBf/6BySj0P+9hy26A+dQwv8pe1a1MdGC09h3MghkzjJUy1YT/I/m8TH'
        b'fNMIH5tEYUCsh427iEaaeHNC6pcRY97+POJuRFz0uiivSMxzY75+3L+EPnOW/cUZkv93M7Qp+atHZ+ju02bo7vAZIh+v+Nsz1DRshqgO7tgcdIbId3SKIjcPnSI4phax'
        b'WvDkOSJGQ7lklgS5omjRP1lqwifOklYAQ2aUTtH3VXLbUOpLGG5ogA52NZsxLm6Cxs9iLvGjXd07WxyZW5uRQu5MIOW2/V603MpuYY95cfwzo0U4Z+TcqM0zFL5ujkAW'
        b'VAWhFlJPNieQoaPoJMqkHxiHaHBrNEYR/tfvqIsWx9Q2/SgbKoPsodLWy1vIqa/EB/sBgfvq2G9akgXyrTjH8x5Hxxb26fBLtUVv//b1hNEetTm2GrzB/ILyI7vF4nsv'
        b'5nlb716VvnUgblHHQs+Poaw2T+eUz09qYSnW5QMB4jPidMfiO+l3PL9/3uP6lcPFr06Iux5rq1byaf6rL2RHPJCn9h/a6HprTXfByyUfPPwi+dnI34VVWmYtHw5Ixezk'
        b'zA1Bh2ztrYmeJQodVUeHeXvUArkKZNgawTCehkdn0eEE1MbCkMKRpaiWqmlIgGziFKOQV4/D/T0aozADR93RqusvcvWF2pzStQLoqRyU4YGaKdcBeQJuxUL1nfx4VDSV'
        b'3psRF8E5Cg8uqMlfcY+F6txpsdN4qLL1ovdQIlQLWdOJ3XontDAeop3HE6+6IhNBJsokV2SL5jy2IPHSearB1oA22UgTo6LDyYlHV+mcv7NKN5PLGV0F2suUHs8GguSv'
        b'h6zcEFKL6BHQ1GPN5JO/Id+EKNtFi1j9t9dvg8GjO6zTFku2wXp547OSjCg6vAzvZJAtgvoZqGTYpqip+F9u/EhEuQphhXaFRjQfxRcJ6IUNP+gxKFocJYwSZYv3CFaJ'
        b'ZGpRalHq2VyURpS4iF+ljtOaNK1F0xo4LaFpbZoW47QOTevStCZO69G0Pk1r4fQImjagaQlOj6RpQ5rWxmkjmjamaR2cNqFpU5rWxelRND2apvVwegxNm9G0Pol6h3s1'
        b'Nso8W7xqhEwtmpON2MMVC1aNwG/I5ZQm3rvGRVngtwZRltS/1vgBDf/IzcQq8Vf7YXGMSPAzi3j2ikV2Gx7nCHOGZHt+8nZJvFdSd0zUEI8OLTneNFUbp+hPN04hbZbo'
        b'1z3/MXzWsBYOhs/6s2BVZEWweFnkNxIWK5IVsWTBIovo2LgnRN5SUROhYfFjm7dlAA02BGUzUSHBj9EVTsLsBNqHKgBdxIjdzkHALRZoTA+NpbiycXyEJDEpCD9XZgoW'
        b'b9GBFjiYGEzCbxNnJXjrWm8h1oasqdRSYCM6pgctKJfGR1Y407HeTGX6cLhgzmIf403sPIl/TKMfT0QXmUVEXwb02Pr4Mz/ptoKVcIYbOVkI1XoJzPNSgyu66DvNh49C'
        b'xzkBnOPgghkqosZO0VbUt42fAKo8aWRv1OHGzocS6DPwdfCRRTC/+pIEHg5NQWcVsZK2zaN7K0H9Fvjh11C8QxeOCeePZE6DXHSTfVGLF24R+VYTevQmCFfohDE3WA1w'
        b'CqrZxd+E6cShthhd4LdPQUdZZ6qJzTsWqGxinHAOntxg8Gg3nITTFHE4Gu+cTb5+3sRcYIg/J4MU5npsPOoNtGNR5ZUOGvD0NDBXRnvROdRPPWah3SiXRmZfBq10jBZG'
        b'e5ubUKdYSpdYqBzO0BoTtqURqIIXUXsMcYmVt4SerjnhJIZMo0zTI8LurbWmzEXW9vHQFcRxzjM5S84S6lGblO1sBP0PR6i/KjcsIQ+6rCL+qtLgJC3xo7kkeNd1Oz0u'
        b'Iq5//EZ2XsNRyB4PVZOJAy2V+yxUGMjmox6diBjqQQuaOT3iQSsUOujX7qg7zJaEZy6G44MutHJNqYnQeps5Q9xcQb31I0GmDVAjnbhli9ARTBH+VEjAE8Nv1YXjwrXQ'
        b'6kEvkSwlZCD0vXiPCD/HFc7sZgmtIUFxxIFaeHRWLdJnDwvsyUP9QD2c8xXJTPZwWyj53NRbxyNC+/2lEVxsxnP5vJwYZ5tJb+4om7UMpujv3Sq70l7z4F8fp+abZZYd'
        b'LX7+mu4rVaO0Jte9++EiaUSy1qtXN06w8FQ/fP/Bpolf7Ry9/aui5TUbjd/v9Gid7jjmg+YTixLc3h0TaZTWd2tS9tjLtYHzNz/77E+bG7xzXDQqVnz7SfbKmz9IO7qu'
        b'W07+bGBJ4IyRATnyyAlrfv7k7BnPq79X/VClMdVkqt6k+zmLDbcVy2TPOJ0Aoes455Sfj0ybnZboNWHM3XfQyY+/WfBGxWS/23ZvXOfXrmqc7NywsmHVp1PPOrzf6l/c'
        b't3aZf02t7YlRN5ZtMN9qfgN9V3O/e9X3tg9vHPrS5+6qjVc7TkVWJnaFfZev803uPasLLVfaDV+WdL0ZMC74h1crD9uHyF++1PnjG20HK8N+/Vd7lG5Q2B/tb06u/PW5'
        b'7z97ZdmxlZWvf//aq2uWL3t7Wb/dy4mV9vdLZGtf3KH2R8FKmebXlrt+FXU/X26R8bp0NAOD5YRhFrERnVPyLIRfiVBcDO31VPf1s+FXO7B3kjgeL9r+GMrKpO7E+1gB'
        b'ZmQL4LI51QaQgNA7HFA/dXQgGoMuDA9/gurQARYA5TTqoxj8gFRoorf7/4+394CrKrv2x+/l0nuToijY6VJsoKiI0osCFqxcOkqTooiiINKRIr0pvTcBQQQkWSsvb5LM'
        b'y0syqZPkTSZtJpn0vLwkk5fkv/Y+915B0Zkx7/cPn4xw7zln77P3Kt9V9lo+hqs4948lCHUJOtgRLhafYQLRFou5izoWxjjI0yEU95SZ0pXw7LCsK7xWhhK2xDnwUCXO'
        b'hmAjO4bnbM7jhlrwgMcND0MhtvM2J3JxKTq5ywQfKLtDla1Qw2FwM44ln4DyEBKZIkmS+OQOqBBm1OcSrEzImhVbDWT1HR6KoRrbsYDPyBNHPFm3ClknEhzGEdaNBAuh'
        b'jp+U8TLO5cGm52LztKPIcI8EOmEOFoUDfkOGOE3PUMhOHIQ6keENCczuxnqhmsikhx6fwF6sZT4l9trH6bUvQhX//ixh1GHWHEIdi4NsOaNqbVXCDmz3FbBzGS1bvryk'
        b'AzRpChUdVLFIOPZ2Rw8KZdVkZdLupIGehiRzHUwIQLYTJsz4BUwOQRt0spp55sewUSgnMgOVJ9m2KIQRQd4SkSH2ssytGrzLJynRJ9Ir3+EIffjAhhf10yISwlkR0Qef'
        b'RQ0M8LcIlNXsg2FDXS+JNz3rUSYLN+ETLLsomHgkuohOCl8qo3coS80A6qGJP/C8XgBvjSNXvLRp/brxEnfS6bOcLK5BXpyweTLxBu2xIsO9EliAAjV+hZM7bVP5c0wq'
        b'wnI3kaGuhN6heoONyqtdShpvejBD0fNg4rPA+9siTU0O7rV5BFddLHjk2Akh3gqd/7CyCpo8Jsy8a6pibWVjflZIk3dDkH8q/Ggr6fPY8Ge5XlOcoy+DnC+2OpCdMfrF'
        b'SseA+qd2VioJt9quWKa0z2x23LdYfqropcl+2qrqPxC9ttj4f2jK+xkoRlC0MtjEGwjIoO3zovpv0rtA1k5A7WJGYnzKa7sJfE0+IWF4eTcBdp80Myv9zWqQK1+Mcol6'
        b'zaDvKAa19k6SxlslxlklZgotZA+7HFaswZsUez/++vX/tmJkC17vOz02JjEzNf0z92uQNYf4nPi1o31PMdoG2WhCi4Y3Lu6ucTE5NSYxLvG1W/oDxajbeeV+aUamlXBb'
        b'9JsOHy8fPjY7Njrr9f0p3lMMv0UxvHDbv/TqasIxudeN/GPFyLZysspcxlJEX8Ij3ujd1S7GxEYRqbxm/J8pxrfkvMSvf7MGAooFl1Poa4b9UDHsxhU0/a90LtBQ+JNe'
        b'M/BHioG3Lrew2ZrLzeuVg8vG5krsxWQWsSKZRVQiKhDlinNUb4q4o0DMHQWiW+LV6oOzR73sYVV/ReLMZ6gGL3dJnF61PTSnr2sJsbyHdmYCa07+nMrSY4UmEryHdUpq'
        b'5ss+hhV+Bvl2vOTKV9lwTSj3r5c6+lHkW/81GaXOgyzqfeJ3okjeCWHZYnMtAb5uUZYDWA5fsSD3FVXoL8rPLfNuP58eR9wWqeVYytWW4iWfZ8LExcdmBn/60vRsGr/V'
        b'lJ3i/NR6Ok9Uu7xEfRbzOuFDqEjFKRmaw/rnvg8CjlPuhivzYHgtDlhU1YLFW9jxfxaeifvkHCvaU6P3bMU8PPO14RgWPrsU96vIingenDFXeVsk2vRE0v/BbdpbKxE/'
        b'WjmJo2x3nXHuuX0ibO8i3P+kAE565BvvtNbrdzojNnMFekteudsrwzrPr1BM6n/eYN8rVgR2GA4ia/Au1L5y4822rtx4sg/YxttqYSncgVobJaHOemUQjhFR2GEbfa2s'
        b'J4Z+F+gSnCxdWIRddN9JmGffuYphiqylqcQ/2tSJeXjoWxW/uhzvGx3IUtveH4hNiK84nhAfGO0vDZaK/2B22eySWdjpD5xUXNPiRKKJdvXvSEUvZamtnrGWfkpGQUI5'
        b'sc+ydRJtNV2lHIOXtk8+8qrb9MLIv3mD/albnpq2yviri2QeZBOK+IsUQbZPI5iDXpKqXiwTL0NQ+ySGV7qKM6wyMhOTkqyuSpMSY17j9RWLVlMoqsHh3kILgMs5InW6'
        b'Rt9u7MrpPUe0E49vE4kz2N3NgUofRX41yvrn/lLtuA/pt59KrRtE3wg86mITGGkQt6Fok4fVf4T2qK2R2kyIBkdiP4wckn4YmRRn+4dB6VtRyXEE28qcYh7tcv2mky/9'
        b'2+8UP2W8Nf+/897+eaBE9CNf038/VGEjq2uUh+MwZ+frlxgutz1FujAj8cmBPsGmL8Vmd8FBzJ3DV7GH+Yd34xPutvDBh1cFfyv3th4+xPyt2ItLQg1HaMBCO9tl/mPB'
        b'eWwFQ9xPtAZ6dZgzV1df5s5lvtwMVV6wMiDxCLensWmP0DcCRlT5Td44geN2WOqFgyF+MKIsUk1S2nTgmOBFKYFS1QD61F4Vm2FRpGwhhkmyzhvkSuOT4l/qiRkX+bZy'
        b'fjnyWfnFSJUnPvP/85RodVYiY5kNKH/8q3TbqvNboerUaWZ/ewOWKjZc1ShVTMjGaLUaF8uKWfBg3Em2SBIyydJZomT691htC3W5IfGuuhzTv6sqwON3VQXk+q66HEq+'
        b'qy5Hg1w48NcR1uJf7w25TPD8jiZ2ma0SK4WoTvRjfe5fLzGhq6WtxHO8N+MCDCp0hYpIE+bxKVQqwfw+LFuhuA1l/2bceTGEqFpnVieKUbrHAmtqxTrFhsVGcSqfPnQo'
        b'3EWIQitG+646Cx3GiWLVebBOnT07RueemGeUa9FzlWN0Y/T4czUU36kQdNWPMeCfavLZmMUY3lOK2cLvMeR3GcesuatB32vR9yJ2RZ0a/ZjFmNxTjdnKi2WoyNqk6BTr'
        b'FusXGxQbFZvFaceYx6zl92kLz6Uf9ToNmuu6e5KYbTxcqsJjeqydj26xHhut2Lh4TbFJsSndrx9jEbOe368ju5/fXacWs4Hu387HZHfq8btM6A4NHpRkd+jy99vI3o/e'
        b'QClmU8xm/oZ6MUbcFLJ+V1dG+fSPND42/f2dtDErRLin1cormNynfzOspCTylysCFkWUZlpJ05mL5UpWIlH4igfFEWTn18fQV9GZzIhLzLTKTJemZEijmQWb8UKw0S+T'
        b'FEtqumwoxSjSDIUNRBopxUpqFZ94NTZF9tjU9OsvPMbR0eqaNJ11RHN3fzmaycyrF15QodAOHw33dLQ6kpqyPdMqKyOWv0FaempMFp/uxpXxW5mzLIQFcSUyMl9xrIFX'
        b'VFFUU2HbrqioIimRvPJAg0wpv3/mxY3hS/RCDFeuk5Plr/JGYVzFSjI7jLZz+fKvanCxPedbFeNo5cc9TjGpNCMy0KxisxMzMtkn19iKRslcNbGr4ATZhGS2tTCnlyzu'
        b'a4lskvRNXBY9ThoTQ+TxijmlxND/raRpaamJKTTgco/Ua0DKCgSlACk6wcJhVdbComd5EVNfhRsb7+O9QF5yNNQ3MJg79dXOkYaHJSzWwt7LblmsDI7hlmur3043HbaV'
        b'ueCvYrFGrgp2chAdrKoE96RYSxDbV1mksl2MTTCTwmOfR89in52aaG+qKFuUjb1QyIOH51ywJ8wB+/CxBU5ir4tI4ijS26+0ZV9AlrWIlZKB8eX9uKwJ5QzQS5UeE3px'
        b'7bFRgRpsPyKUg+m56munJKIZiDJEGZkwypHazjNKZNNVH1IWRQZ+J8tIxN8M2rBN6XnQMhRLeK+ve/Zw5wpWBgm1W4+nqrHKcUv84dEx2RlXVFi7alHSJijz1E38oCRN'
        b'JePz9FWfxPJolZsuOOkf/efeK7utkgwNS7rTNA4pua81fcvXc1NdsNEeL8mff+zUlv9oXZn53w9+ZapY+vVv67n8dHB70Ylfn2krc3xcGhRxI+eXA7u+4n+5NvtbG5/a'
        b'Z75b/OF+a6Xtutv+9MvFD9+qcagw2WCivrhZe+a779/9uf5swPY//c/WVI3tb//3N5M2bTQFW0NbvX3VZjlNUaXBf7fJ/9U3d83dvnvsi+9d+upXN6t9aVfx/rio2O2z'
        b'428H//rt8AspdR//ILLqD3+QSA33Jz94z8ZYqLk9cegED/qLlKJY6SKxMy5hnwA17yaclgfvbq8TgnI8dBcLPUJedt+uswGBbieX91IKNBUCinPYlPQ8mHgIZ2HsIMwI'
        b'UaO2o2R0BULPGdvlIcX9MCwrkY+1l5dlR7mxWuOD8AhalIXvm9WgNkDIs7BRJWNuUKRhrASdAbKgF5mFo4exnHT9gdBgtte2rKDktOT49bN8aulYnRMQbLcDyxgSUIUB'
        b'JXtoAuGV92EBFMrimRV+KtAFT4WAZigWcJB76GQwgWNaLeWNYld1aIcxKOdA9ixOknVYu9FuedI4dGC1UE/0MX1ZKQu0McN0PzSyrm6qIlOYUfaFh4TOmbPnrA0UOLkr'
        b'gL2qkZKO/y2hZPwATCmz+n8BntjIKuwJZ68MoFECVUEn+cJuhHvrWZzsenqwvMigbpgkyBLbM3nLqSJops0tZydM7VgZxcoAaGXHgqByR4ADL/jIqlb4wCM1qDqBlQJA'
        b'fwjDMLQiiaLoKLRanuYxyi3YJjSFY6UTJ+jhz8snnoACIQg4BJVr2BklGoeNid3YwM8iiUzocUt+mi8nk32a5OzVQmPhnxX9uzGoqMoT0XV5Srk2bxHOktE3cFtACGLl'
        b'mK7Uv69o2K3QrsvMg9eEAiXCtasEsNZp0cu4fzZrIU/0wfKTja+c8qd1uat8kgN4v5Y8mvXiUIqglqtCab+spZdp5DeKcslCbt8QvTYIc1DrM7jH5Qp2hYfaScBEDAtJ'
        b'PqWPOuH/Tx/1+1mroS72vxVu6vTY5NRMRUNjgo8JqVlJMQztXI1N57aglTReysDYqs9SZN95JcVK01mX3CMKBCbzc3M0lCigPeZoyWJ+l1UflhGbyVBcZGR4elZsZKQ8'
        b'VGN7OTUlM5WfqLS1SkqMSpfSw1lc8Ko0MUkalRT7ShCVqehRLd9Xui01PTE+MYUBOQbBfWLTifKu21ulsuW4lpix+tOESKRigt7SpAya4Zv68DfV/5uI+/B/BgsfRd7j'
        b'TXvlPnzJZpmfd/0pYFV4CQvJJeQy6XgDH/2f+/Ev5mx7gWEzopMu8nX/l9z5Xm8ktZZWOPSP0t1Xdx6Jgcrnjt3H7JfAEAe8b7d8hbDhxTOu3LdvtkHXA+pDXpPUz72N'
        b'xeJPndT/0tGLl337yjLwXUloZHa5gmUTZUmfpYG2/vYwFC7kf7IPQgKZ+2yvHmnXUi03KHdK/Pk3AsQZzJnztfbujyIdDX8R+XbUj6TWhjbSQGlSHDs4/WHk7sqUuF9F'
        b'lsX7yw50tC6ob1qXbyPh5dXjod7q+eB6UC6Mv5p2x4cXhOrKnTf1Xqxz7rhGnntFTygUdHjLdTIs5Doc2sJXEGkkLMrjAa9X1IqIxGd2a0ex7JVPRbefEJxYJXF9lQhF'
        b'0BuR8uMVyevMFYlLSbqGZ9+AlHm0wuywrp/PRhslIV81HwaNAwJgEgdD5KEKAxznibv7sRkHA+xCdYPlgQpxTuIXjEIkvDDCiF/JyjBFQnxSvH90MA9TmM/8ZGWg4t/s'
        b'NaQ3Ql8OVLwm0CR94209pa2pr5xj9qptfTlo8QmzOPxG+/a55bGlV8+GBB7zqK4uWdhCs2R8kiwqJFtUFLJF8ol5730vaRcf0j9SOTha7sB6tZMkOT02TnBIvJREtIof'
        b'Iz02Mys9JcPdylPR3V721pFWqVGXSLG/xv+wOqJRCc5iKVdQA3ewhltfuAh1jOpPHDvlcPLUqknykLdT4xI+M+Bp8mmQZx2w3FlRjEXMYcFNdIV9HqqlxirhZySOu7Sr'
        b'ZLASvV4VFz6K/FXkLyO/FJUQNxTLoi9vRY1IE+LsT9pI/cVfLhF/L6hivbbVozNfXPtF+7iOMw32P0/6+aZ+w28bb9vwh+oknWgnSby7KP+IwZbhFBshZAHPtmKZ4vxO'
        b'qy1Lh5Wi0K0gIdCYWYhQBu0yI4xbiNADhdyG3CRZvzLlldnMOdihfo1MKoYGYsJ434rARGwW8zx7etMBweKehDJ8HBCoMN80U7TOKOEYqZUHXBC7ndzGxDUUpa7SmWIc'
        b'Zq+s4NlXGx/Lq2OwA0QyouFc7P5ZuThNSCZU592bcta+wD/LHr8y6e/ESsm8eiBFSbjsOdIwozmGvxGbjxkvZ/PXTHN1Dn8pVeV1uEHCcYPyx49X5e3MlxOEUuOspP9/'
        b'sbqnMOanYHXxqmiHkK2LyQ8lGcwtobIU/VGkdPvbUR9GJsSNxA5I34rS5sjE9m/K1n9ssFESWta1nN3GT3HxrFuYw2YhDLMW25VzEqFEaKY3eHJNgJ87TMsylYWzHmbw'
        b'RA44V49Ya72x9rktYqmpqxGCbFdeS6/iVxAom0/MGxHoA91PIlDZvGSDvquWIb0ae1GaEby6O5/JY5lGUuUGrOpncOZHrWZWyomXRTdiZGX3PxXpeioiMbGZUpYHKBVy'
        b'pZJTr5KKY4Xy5c/9v6J74R7ZArkznz+PwdgzEy85KyOTmb4CH2ZkMjOR5ScyV8Wqpp7gvliR28bMRHr4alECBcuxuaZLrwnLRe/8Gk5jhKb/EqdpBmcxYJEDvIqwDEU+'
        b'16eJWLm6SjXFO7xKdTT0wpydv5JI7HsTpkVY75HAC9J4ajiEnWB1bJRFys3/EIkz4w2529zCR0W3RCgIoz178LwoPH2RyICXAcJJc2y0C6FHhdJQo2QSQL9d4sz3/qGU'
        b'UUhff0XrVFBFp+7h49pe87/xuOCkrPL5P3rlifLP6dfm/WCX/ZaM7GcNWprv7PT4hU3dNz/03V3nfk7JZvbX7du2Dv+XZai2We340Vr97xz5iUHR+v/Zu/HD33+tYFDn'
        b'S67rWos+Toj2D2v9q7278/65z1/TKBr723zRR/M5735z9CsPszT71P+xqPb2DstHZ7ds/7u+jbrg0p7EheATdsuPsoTBKJcx7peTn3t3md7OgjpS3U/shDJyo7iIj2TK'
        b'+4DXMvWtnpEr4IIeaL0Oz6BB4QSGdrhzVUi8KII+cztb2WEKkcY+GL6tBA9FOMVl4GGsOatwAOvAOO+SK3cA7wfhZDB2pkItPoaqFf5veLTFUPCc99GnC4LrmkzkHpn7'
        b'GkezX6E+VT+tE/VdNdk5Yi5KfT+7KNXXltXlMOQZ/4b8rIG22FicY7KKIKOBVvpOuRBdq/QpEIFk2bXPpa4F/Zn6RlK31mS51H3FZGkhQ+Tnm9/VUCTICxkRGkrshHSS'
        b'NCU+3DtaTcbQ7DUM5QwdzCQxOxXLHImaPBbO4u9KxXrF+sWSYgNZyNUwzlAmodVKNEhCq5OEVuMSWp1LaLVb6ssk9C3lVSS0Z0wMy6RPib22MgWKucmEuKYQho1OTU+P'
        b'zUhLTYlhzrxXH4gluekuzcxMd49U2EGRK1xkgg/PXuY5UzgTWaD9pYdJXxlYt4qWpjCJnJ7KklHkicSZ0nRaf6soacrlV6uFFdHYF1DVqrHYVyqL1ykYthAsWJyRFhvN'
        b'39BeWOVV1cXz8xspWclRsemfOrKsICxhGs8PYlxLSIxOWKG3+BulSJNX92OmCi5V+TokpCbFEDEv04Iv5MYnS9Mvv5AModi0DCvhIImjVYjcdyrcHpuZkBpj5R6XlRJN'
        b'5EHXyAF05KoPks8+WpqUFMtcz3GpMqWqOHQuEEEWS9NnmQzSVZ+znIZeuZKKxEN3qxdPmTzP0JaP+6pMbdmzolyiXn7K8rMqn3A/kwyEQMJCrHa7ujk487+zSLoQE8bE'
        b'yrdK/iwifYFKVnc6H4mNk2YlZWbIWUTxrFV3fHuGFf+TZZy8NLkVMEVGmexV0shIoN8+BchSoBdWf27tS+jFNph7p1zXq2e4pBNwSBVBPQGSWRw+KSTfTpngktbVK2KR'
        b'GEtELOyMbadYFUETQdPmkwlMljDZyFApxn4NLz+1LJbYpgvjnnTbcQH5WDs6WGPJDlu/IAJBQ+HwNCINJzNPCqkCUGersRcHzwjx/y4otFqR2+DHTQ31i6G+8rOF0RfU'
        b'WXdwnOR4aDhTm5UbtHbyDrlu7hEtytrGHvPgsDkDEIr0BCHX0t7GwV9FdMjEw04VWyy0+Evs9IchO7wP8zimKhIb0K1kyVfxR08eUmVFP/WdTv7OpPbWCaGcy5/C2Lln'
        b'kZXTyf+9djhbW5TEtMngTiUOD522ua7bk8vrp+/KwlEH6MZuXt1QawNM8qJd/Bn6Z9QZknRyivve2pB1ISIhSf6RjjKvJRDmy/3DfjT1CjuGHRWvQV/42vsHOvpBCU44'
        b'2KqKsNxG+wq06WYxw8pJc8+LANQCHhJQIhwEg+G+8nC8iHZtTgO6Aw9526jzPGqr6zAjDx+fhEXhGL4yCC2Bords50fw2fF78a4d+z35IXtcggF8KD+AnwH5/Aw+dkbz'
        b'b6FYDIUBy86kblZmZ/BtcoTiN4+hPV5+MP5oMD8azzr5MPLUgs5jMHNr+eF4fjL+dgh/sDZUwJidI4z5C8dQ+cF4WIBZ3kkYe6ED55YdjuenS2EK+p+fjseOPTZawjSe'
        b'4COckpVvwEJbXsHBYgefxrGtMM5ado7CHXmSLsvQxRYn4QD/EyzasjwDF/p38SRcvHuIQ/ErB7GPVXDg5RvOeOMsTEM3x/s6lpryXA6xj4Mz5uMgn40aPIQ7AfLDyGf3'
        b'8gIO8buFkl+90OwKXforazjwAg4XsFiY0R1a/SqYYeXrFIUcWOZvNvYI3SuGCJmyPdmDA/LMYp5XXImlQvuJe3HXCbAWLy8ZIBQMuAt9QrEGd78AP2LpFcY/FuoLqzkb'
        b'Ys4ShsKgO5QgsyRWvA8GcYbvWgb99jSM7KDqE8foOy0YVXUQw4MoL86BF3Exmt6sNkRZpKRN8BrbcOncNRtNXoHtMMzsz9BNz8JH2vhoI1TrQRnOZopFRpckfrrYlbWV'
        b'rjlF4uCO4iJ+RQY06+B0FnNf9Emw3RAbuVzQIEYfW37ltcwrGulumKejqyqyliizokxYwge+hBNkpExl4XTGFe0rm7AE7umlZ0lERhaSPVgQmMXCwFC+GUYyrmRp8mfp'
        b'4WMNoqjpLGLJezQFPr7l/oMXVInqnvLSDVhPtPpMcQcUslanwoVGsRJPKIEm3tDE4Srkya7yEctmyaa4AcaUiYppP3h1urKNJopn4ehhWph0nKYpHpW4b8EioQ2QC8wq'
        b'rrlGUlfttKpIX1UJx9ZECrQ1uBMrtXAmkyairaFDUB0Wt+rcUoIprMElvu+5cE+Ddu/YMbZ5UUEqOCeGGsjT5APkYImt+c6wIKwJw3tYHwb3WBHTFjHOaDgLTTiebA5Y'
        b'+fxJKBYGWLzJSceRnjaZgTN69KUtzChhn9gWWs5yRYIdMapYTrIwYEdQYMgJpjJCoWyXzKK2Z4Kxwi8Qy0hOwJ0TGhlH8K4Qi8mDFlgIYI1JsVgiEruLsC6TtpZ3SRm9'
        b'Qtb6lC/JiQAHYqdgZVGCiQG0SaABGvy4hNZzWScis17d6da4UZRutiC2/3rDVhTOPnRO3Xvcy1okdBAR/eWg7BfrQzbKQv+uvMDg88Txw/T7ddF1Ox2hSVk/zkAp6dZJ'
        b'GCZlkSPKWbcti6nlc0rOoceEVhvZSVAqNKnqPZS4wQ1ZS65EUSKWQgWvunHkkLKgfeLOn/mV3i1Zl4XbMpW0+6ZPdLy58OHXj8j1lJXPH2yShA9/kyH78GqGUcbGY6JE'
        b'/41PJRmsJlVycmBy6L6Udc7669NPfeNW759CJpMi/vH9v+729jd1O/xj5RLJE4uBDpHn6XmNzyUHKndo7XPPK7cq9jX4qbabf1m4zR/fOp9lc/Xqfy38+/tpcUkhx6/H'
        b'9RpOrN/aHl+Q/oWoA3Ff+vziwoF5jb2Zvz9gfsXuR4XfGTe4fD3cKegnf/jythmnO98Psx3/XNb+xvzyLy+d/O6DS1diftp4/WhL+Perf/mjcu0TsO1M2v4jv/F/d806'
        b'B4PtktNrLifeLW+fr9Xo91bHv33Q2zYYqLV5bds6w5iMbxW+5/rTLsuSXzic/9rWK7+Zbkv781Tm3G9dWr/X8B8VTapax68ev/Kfp37gvdCvuXlYNKf5uEuyuSNb5ah0'
        b'qk/SeebozzZOqzzRWj+0ayHuh187/PZ7rt8b06mO9frT563OnN124fdfz5+F7welFv9XyvX5X//6re+vv5Bb8bXf5j8su3vmsF1n3df8BmJG33/879OXvmU+fDXXpP7v'
        b'P//Tu9/5demvjJq++RP9xd/8zjt39je/+3q1hd5v/9LWUXPBwDP/b5lf2K5j+Xubv3wcm/ze7bfNzx9ao+V2+53wJ79ofqsk9mc/Mv6z2wefjw79tw+b7S2zjc6b/1F/'
        b'CD6ovK41p5EblCT6t1NXP3j2+6v175r9pfHet8Y657/7xT033Nd/Y7rgQ8u3Y2N+kuM4tfna5o8t5m3+GfIf+67pzHz3ke07zd/3+ud7DzuK1MQHj6u5/8T5t+kpYKt2'
        b'4Avbfvv+7S/ckPw498CP8G8mM47H/939g8wPZ3U+/EJy3Z+DP4rY+WFpitt/pn4zbPb4ie/87T8zTb+/5tw///env8so/sG3vxp8+Ol15yATz796VXf8/Kehf/97w4Fv'
        b'BF54+vaO87t/9719Zdv/KQr6+u+/UPTvNo6Ct3kRGtfbrcymgH6oN/STQMdhGOOJfBJf6FdADyix25GFC0Ksuxh7YCZAHjsP4dd44YIBsTpU4Fwuj9SEHoldHuTJhEmZ'
        b'o0gDp3nVFM+LMB+gqFjxDBZ5dqT7DeFs30Os3syT+Z5n8iVeEnL5sAjz+QyPQt15wc2Evde4pylMaJcMVeEE4Rxtoh2fZxoewQKeJugMA3rL0gyZi+ks3JN5mbRiuBfp'
        b'QgbUysva3RFK2/HCdos3uPvsABZesgsOQroLGlyUd4phkCCuMHIt1EuZ+wmLvBTJk6bR3LW2Bqqdl7V9aIJK7rnyDuR3umAbIb1ym4AYRbVdGMNnfEBNW5wIsIMx41ia'
        b'rqpI9brSFly8JfQmboOGbay+7zQOLa89rHQLO+CRMKeho1tkrj7ohnbu7jPCUfnpolZkuaIGITJ4yjNFQ7cJjThwhj26fIcaWRhdYl2cOGGbxpd+4w2RrDTI/D5+lOk2'
        b'VvDl9SbBX4Tl9gQe6T4sC7Kn3WnFPqMdEqxf68O9iNBhR+/zPIZHEGecR/GwG4t5OZpTJ7FTgdMwL8X5tlCU+CgLMsqgsjuMCFAZn6YK7/k02UQOiaFbmUPiCLjDQ5I5'
        b'MOKxHBFjF9QxTHwch4QSPj2qrNaVAIpP4hOOivHubXmf8GEJLB1+CRY7wwK/+6ZPDqHiMihfBotxDmYzGeo5Q9iv6SVUPE7wRoGK42k32CyPXyOA/QBLWfEpIXxJA2Ge'
        b'JNUsnO9HYAjPXC/dceF4iIMSo0nbrdt4+uwBQ30FWiKodAUf6+CEOCjLBe6I7bFLRSPttCyzOCCWtvRiiGxr1LFFidBLMfZzapJqQ5Ws1COUnsKaHX4wai0WrfNWhvat'
        b'erKG6zjMBEPlDXgQ4reLuEakhp1K6qGQL1QSagqzw1qWFCto2XBZF/HtcXhXVoJGVjY31choswQrtbU4UdjBQI7wvWNQcjKWEbyngbFJGdqinYVtaDgj4leE2BNuoL24'
        b'Dr1KItNdygcvaPM2CLsStinqmApVTNkyP69kis9ghj/pLC2zUPKyTCAXsYoW3FPCThjyE+ppjmttYm7wIGygq2ilg5UsoABr+EyTdvoREzdza29F+jSMQL1QkKdtHW3j'
        b'lN5VmYM8HUc0cFAJRrdij0BudRvJYCjf4eToYGPNKCZeiXBZvdRG718/MfbcEfz/sGP48vC4NCZmRXj8lwyNfTbf+G5t3rNblXdEkdfAFlKMWaVrM7Ghkq4iCVldSYnX'
        b'uVaSJR/Tby90ctGUKIuX/+hK1PmT2CiaYsGdrc7rZStzL7wmr9jDqmnr8znoinWVDPmhR3lXl7W8fo8uT4DW5TW29Xkwf5Xw6LLlkHnwNQQ3vMI/nr6eueYVnvH0DSu9'
        b'+v9aRXM1WYK14sF8RD6YrWJsHhHYxJqAaclKU36miECe6C+Or4vELlsCG8m76vJA6PPzltHKAmYXqYoEnxj3ix0TiYSzVUIgQEMWCBDzUAALBCgVGxQbFkuKjeKMZGEA'
        b'5RLVAlGuSo4qC9GGiW6q8DCA8i2V5ykG74cprRIGOJEmS7JeGQXg/nCpzJ+riOC+2rcuv2Ll8atMmWt62SPsZR7qaGnKqm7LKBaBsOKNjJiL8dXxhjdxxbPgxqqj2sqn'
        b'Z2vFj1hxr6l8HoIPXJgSC2jQ1FMEv/PqbnArr9SYWFc3qyhpOvfbCi+cHpuWHpsRy5/92SLTfAFlUYsXCy+tFm6gx6+ehixzZstd+cx7/kne3s/i22WdifREL/p2LYOz'
        b'dtHv6g7uAc97th/njsHDWLV6sleljQaOh0BFFj+MMqBuwb2oDrZyByRzLWJJSNgKh2oO9mvAPeuT3HA9e8DEzh86brOAtgjrvWCE286XT2uJjJntfNLecs9uG6GrzA6D'
        b'/wzTWUoW+sqIRSXaPLnYLvIiqWKGjUuwKoz5P4MCeUHwUy9l6fpCDTatcAJITuhgnwpWcotbh8BloxZrDM57fQcRLqwVygSU6n0s0lcSmaXpZ8aeNr2cIljw320+FM6/'
        b'7o48K/qBSORUbXT/0pPdqmuEr727hF6h4v2XxN9UEulP6Jhrd3muF0qIhuFATjD2CA3iXbApiTf/gbp4j+XubCxx8A/CWubJJSToJ/OP8y5NAaowf9zX395fVhJ0Fqt0'
        b'/K/tFlL22rCTdcl97t0Nw/bXZuwRvqiykTUxeAQzhxX9AhygXNEygEyL+qtCv9ZumL22rCIBgYuR00o3CE885UQELeZk9CwbH+ehn09A7l62VtwM+fBMI/e2rDrqP7Jk'
        b'rnFVj5SvRmTKnCaHLglLOeJ0UjQtEllVr63OOW394S5FU1buLLdR4S5TX+bud4ZRuT8FH2hxUss4E7QR5uQwD/uwW/C+lGrh3QswKvOo3Los9DPtuYStnpFyj4o1yLoX'
        b't8M8cwJjKVSLiI7KVUXKu8WE2sZucEcwQdMlj4v6LzlF9yQLbvAi7MFxwvxQ6vS8FK0ljif616cpZTQS3d27XuhR7ZFh7KxdtPX7f3v/h3/7Q6xR+t0W211enn5HfUK3'
        b'HC3yR6dnzcY3bH6muufppjQVlaViy8+HdHpfqFy3Z/K/fL5h52e5setJxfxXtnutPX/oi+PW0j+fCZw2/5/3rziMKkfEuz6rb75b8Ten2JG4A74lY8c+fviX0XUHE7e7'
        b'Zv3iCzWh7xUraz/a1O71rW9vWZDcqUqT/Plz2Z/74brP/7Cqv+WXg5rRYRZbcdvMNy02/zPyflDlu+GPto5n3CJs7T5zymng8rduTn5z+DcJfR9bfsvhP763PivANbbs'
        b'wvq0X033f3vyb0lfVv79L39y5ucjS2pTfx78+ZnBy705Z9p+YB/yqxs/TN/11z9d6TP9XWhp49G7SaGb3zkfsWjnZmv+BcsdZzO8PEYf3vvNO9v+06G9ICv50Pa/h1/a'
        b'e3zjV12Nf/3DzM7fN478+HDb1Z3qkz8t+r6hxy2jt6qrnR1/sbCQZPDhpqwfPFrX8YNtf/rBO+Wj+5oMPpz83+8OdZ06rvmTsqDBsGf9Oos3x45v/+LnDvzEePRntzP7'
        b'bo3tPjS+O+1t7V/++GLmhasn4v9h8r+NSyPbq5sC/mpjwg3b7DXQaecrOfA8D4UoIk+wVIqwzVZxiJHMUksoJMsUCuw5CD+Cd/HhcgdDRpjMv6AGRdwcPGCKjSzNX15Q'
        b'gwzuik179nLz1Qx6pQF+anbMguXmqwO28y+kUGlm548PziqSV6yCuNNDOQyLXzwHwLNKo92UcdwAn3ID7Wg8jJA0MLHmvSt550rlUMF4qcfmVN66UtG4kgzMQokSdEv4'
        b'+5qS/d7Ogh53cFzW/UcMC8To89xQ34xNPst79ZxCWo1a7A3g9oSljpcdTYhb5BrrA3FCCapxEvr5QhxlPgxZcwDWGQBnYdYhXfDShGxNX2asr01iNiE31fFeqGDuTRy+'
        b'cs6Emc4wEChzxOjtlpyzIFOKnY84DGVHuNGFVUEkPElR2KmS2cbqkbaS0RiCdwSDqoTeap7dz3sHqlooYcEx5W0xgg+jOhue24YHsZ+LSME4xCl+yVF3uCe3DuW24Zm1'
        b'3Dq8Ah3c84APz5LlvNw+JHvvmWAgwqOt3ELERrwDLS8YiWQg6nnJTMSDNB5bMwtoN6AlkVtnmO9CBtqai/8iNjf6f2iQvWCVaS9PN+Bm2RCT7Z/NLLstctTmRpKmrJWl'
        b'uswgMuONh+gTCX2jxH7T54aW/F/Wroi1KmIlUDW5SSU33vS5CaXNGxmxg026sqaYyrx5kSZPjGL/zVn34imDZe8js6tUBYtms8LKYabFMkNK//96fW2Ulw1mqxiRW1M2'
        b'zMrQlneX+GzWFNlTTsvtqde9uzy9S4tNRFvpBVtK0SWTwR/hqIWs3YASt6ckzKKK01ZYT8qvtZ5YEpXnammucuvpec8BRdYqT3b9P07RFu6RV+IR7lulcqajlZeQH8On'
        b'8oq8H57RzUwsutQvLGTvbidnZtIkSzNZdkdGJju7+copCCWAnue6vFjbUPj+Mx8NUQ/mKQTrsUdnlSRWOcTEig0rUaa2rzdHUZa50Ls87sxqQW+WnIY2KBRg0jzcg6cB'
        b'a08/r2rFYs/HD3CMtfPikRci21u0WWzbIzHx972VShm5dM0mp8MOZc6sloPyb78dXNL5gbgk3upAzf486Erbcle7952ftvzsO+d6Ml3n8XMPBkukBhvKjJOjPp67VVP/'
        b'9+9dP/HF5LN1bzUV5/znN3YWty44Hsmd2Jzt8s1SifRjyfE7v9bZ+pW2X7a2+lxz+HrMP/f9OTrDZeBad88HF8otLT/YVL64xUaFi+QQnDgnuLFx6rQMLAxCJVeeETgX'
        b'j+UXry9PXFXKxTqS5gwsXID8AK1gePTSoRN1eHZCKB7wJAoaVrqtsX+zoApvQq2gw5pgHAuf+8Pxnov4hBVUrzhR8i8piGXyWzeLs9gKCR78JhL8tmit/PSJ0IxYLsWZ'
        b'rM5Z/4KkWTnqSjm7Uuwsk7OfrWQ3CVF+v9ZKSSqcSKfPrr+xEC3dtFyIvv7VWM3anMQ05mP5P6lxKeGFAZQ/Hnw54TQ9OiHxqqwCkqzE7oqaS6tISS/BZZF0nfs4EpPT'
        b'kmKZlyY2ZuMrJarsZV6sA0Qff1InF9GqMkk5mKeEHUnKFbpayuXRSwlNB7FJFGWqnngNOxJv9FWIM3bQbV/WDf8o8q2ot6J+FXkpzv6+tdRfPPkFsxbzVrOAplbzFrMw'
        b'szvme9/Z0SBqr1Vfp+JhoyzkpVftyBRY3BSnZCxeIeBnbMUieKywBwhN3hVCVVowxy/wtnRfcagMK3UFFk+DcV4E/7YEa5NvMmtzBz7CCtadUnDK+AVdkYmEABhWg4kQ'
        b'109s/aYvFTZVTk0ZnD/3vhl/ujHuVBQUVfhQXxhh5VEb+5UcuEpFUXuFn9eRfmtmTHXoTZgqT/SLFac/P2merOqESnBwuHewjVKw8H/9TyjD97wsiJT9x4xLB/Yby1nn'
        b'bmqOrrh04G8jLIX5/2s0/Slldbo+TUlXS3YCTl1LWcnKanmNPX19bSULfRMtTbHJWiaCReJtuYZixxRDsZWlkJf0IBmaXz4DfQb7lUTW21WuYp8o6480RhDUQAG0w32P'
        b'VGx10icLeRbn1+zZDXnROK7qjiX0/X11MsXa8Y6lDlmAhdABI1B75Ah0acF9KBOvI5NoFp/pQLM7TkMlTErhMQ6G67ATlAU47rEfnsGELzzzoauqsOw6zMIgjDjehO5A'
        b'GNt/ExexXw0nYIh+nu6CXujGvvgrLlux2RnzsDMFHpBVPoiT2HrTA8qhD0vhkanPlf0hJgRIMM8r95Ir3sNFmE3cj0WXfdZaStd6uweoRLjccAyB7ggLB3a0Yz/MYT9M'
        b'QXUKDGENPWbGF2bckm2xyuUiVuhgXwxOGLHWPHAfu+hnHhsivbDlmOsluBeNo6rwAGawKBUeYQ0+CMNRmLiWjD3wLJfsz8ZwqDHHrstnsQF69qzBMV+Yd4IKFtqDSoMj'
        b'MB4GBdsDaAIz2LIXxnNx+Dg0i7EPWsiGriNA1YJVCTCALdB1bYNEC+pgGh+62GM3ziTs1dyPj6E42gLyfJLhbgw9tjEIFmyivVMtvbEyEZ9hqz/WR5jBaLYnPoFJ2qYJ'
        b'D1VoOm5zgt67HOqhUHNbOE6ZYSd20V+zQVAMbadpMeqh0R5n9x7Y6rHF2AgnT9IHbTe2n7XDZhzSN8JirIbH4fTeZRn0TY2u5iZcoruG8BEBlscwQWava+w+bD4HrS6w'
        b'YIgPdaOCoDI+8wDmhWLjBii/uFsdl+CJhRE8SYKldVAUT7ePpJER3eRsgV0xm06e8diBtUQLT6AvQ0pk14At4drm53JS9t3AaYvz66ElGLrMz5JYboNGHFCnF5ommmrB'
        b'rkNYoQ7FR/GpE21lAwy70ZuO0PxmoeA07UKVw0EiibJsmDRdh2W0RvPYoXtLggtY6rNlu11WOdG9MfZcgfZQT6gksteGBZxac/MQ7W//UcjbAG3Y5KC9E8dohx7BA8lR'
        b'6IuWbraB6gRlKLe6vQN692blJOhhPRFjFw7Q2lakRZ6CxTWnoeUQtMAj6IGCDWZSbLPFRrtt+ASfwqwEJjSwbh3OSFXSsB2mT0RcO4ituWFJMEyKqBYWrektiEZwNCVg'
        b'Hz3kgQW0Yv6x0/T0+6ehcQ80QXEUMV++klsQ3ocJB7pmEgdgKPdsrpH+6dtRO33isc3g+k4DHKVXLSdiLiC+uLOLGKvUxzJwy/VtRG5VJBVGnInMh4k8n2CJFO8nwQK9'
        b'1VFC9KVq2HsA79+Ah1kBnok4uh2LrclOWLq5x/E2FF3QCIMnZhtYkTjsN9irnIpLkTiphNXZJtKjeBemNKHili80Yb6FD1RGQB4WxujBQxgICTvhEm24zRwHPX00jQ0d'
        b'nVTWuZ4gJmoPxJIw2t4mHDKDEpIqeVLs2037OA93sFCC94OhBh9ZYVswlp3GIZhSNiDSKzOFLlYzjQRT4UUXtrJQgiMwfS3bHO5toPFGiaIGsokYinMM1IkhpuIItM/d'
        b'dDGGWlrDu7Q7EyS4HqvH6/rjQ3OCAx1nTpJ5UweFOGt5HhaDAmAJ+jW2wP0MEgl9UOQWi1PJWHoaFh3XMlfduRCYXUcEN4z3QuF+gL/BuWv4mMbrI1J4cBbykRX8God8'
        b'Fxw22h62ZU0I5NOCP47A3iRauoEQmLTBJyrQFLUFOrHANOubSqw/2F1dokcPqGL0SLOes4PpLDdsO6dMT+3AuylS6LiiRXzZuOuYPfTpRwbA4AGowBlaqwVsXEdU9AzK'
        b'6MUmYdwPis4SqxZuwkXfAwc8sMkfumP0NVmLHuglepqFu5uhxeoqEXCj0gFYuC7a7eiHtZcz7WjTpqCPEFEZPCW2uU/81hp19nwKCY8ue2y9RIs9LyIyKiM6HYJusm/q'
        b'zh1laaV2pqcyz1+AjiCWyYXVOG1NnFFzcJNLNlYYa8Dccmol7mg4Zk7zeHwNCxw0bsN0CpeXdbrXoZkEZZ9n4O6cjdEwEXzjponkgg+Um0J+HL3YEj2gjwRTwe4DRLtN'
        b'aslkg/ZfhFod2uBBKx2o3YvNvtCRSZfkI3uTh/iANFI/5OkpYYEHiY/eNWowuxefmm0jUpiEpy74zPgadqesua6ckIR5UE+8WoR1erRQPfR6fbgAU8doL7sMsCxifQJR'
        b'WgE+OgQ9tOQL57aTXhqLyLYgyu1M9sDqSNJejTYweI2YocKRtqLL04XkWynRJGnNczsv78Ia60s4kHtYN4cmWAB5RMddMOVsZR0jhSkSNrPaxliLT7FAG0u84YFLONED'
        b'dF6nCZRilTU8hk4Yhqoc7FJbt4VU8ygt9Dz2eEfsgGfYpultSy9dRAKyg75rPQJTPvGhtJlTcCcjgq5tJoX4EOZzsPwqNJ1Xi8UGjzgfR67SqwIySd8UZZFMqKZrGvb7'
        b'mJ7GRmi9DGVKV82gjeibVpHoGx6cuUQzXSJjfmuqvzeWpuhgTewptfUXcHQtNDLq2kH83OVtcAueZL2jxGJVBo5M0KZweLHAalLPiI9uiIQONWwO1RTDo1ASMZXEM01Q'
        b'nQmTIhK2W9ZgnjMtcZPFDRxTg6fQE+tjDS1eMGxEmqDFnC6v1MU2tWSLS0Q2LXrEi00uNvjshKMvtB6/gXUWUOG/YQ8pgVlNWplnWK52DAYjGbdIxWnnGBpqT8FxnD9/'
        b'iqQFE74jJAYIf6TuhlajQ3ahhjgeATWRR+DOUXiqjx0+t8/SsnTsuWEEFWGBETC4Fadvr/eKJLExRDsynExrMgytZ6+LscHbFebCnW7oemE+tELTgWjSy3dom7vMDGit'
        b'i7BHAksGeP+Eqf5aUnplxlB9PlAaTqy76HrcPYmYuPY01DpCQaDxDmMcSIKRQ8R8JZegbhve8RJjnsoxeBpzGOq9E2HqQDDMQ8lhN6+jt9ZiM1E/CcVeGq9YlEzivwsf'
        b'qUIHsUGpCbHLJC1VFba5wCJUmBOXtm2F+VycuXKAqLaJ1FwlNuy/gl2eJFHyYo5nQ5FPKnFARy405K4hmnoccx0H482wiSRgJ4mJsn1475TBbiSCr8YeH4JFRNK9Vnto'
        b'Du2sWeShPdk++qQSj6yFqTCiwVmYvr6TeH4Rh7ywgpatkNTdwz0bGBxLh4o4q+2MDrHG+CCXBV00zTx4kAgNUQY5V4OwjUaZJr5qhPuJNJtBAgMFSlCZRQtfYX6DXq+V'
        b'dOcwqcxbOJBxGjod8QH2mIXohJGi6L9kgp2xWO/HT0zMn4P2SJrl2AEYI0YucYO7yDh9ERtO0FOKLyRcZSoI85PNcSqNJMwkFm7xPqOJE+ucvY+vh+7QrBqia43LwUTW'
        b'9A4KAGGHT8TJWEkAwmOvHcw6wcRVre1uaumEX5u8T+L9w/Qu0OFJO7xI406l0yrNMBl0ehMUuWKBsxTaaeAymEi74aG9IQAWcTwKH9I1YyQ+Gm9bQp7dSdruJ8p7SRA2'
        b'wJzt7oM4fJ7QWT3OxRK6rCQVNkTa+TGSWCu47YB1hkS0JYfPQ4c/NoQeIrVaHXsImk/YEt7ogXl3Gq2SkEgHLOgRZ7dDpz4O+kKlczbe1w2yjE8mWZevRuzx4IbmRZjY'
        b'6n4k0MxDhyhsBOp1HdYr04q1axq64bTlNnWJN97ZSIuYt5WovtdgHWn3Snrm6DksOA91nkBS6QDpQBJMhA7w6UVswwf7rpCwqod+UiU9hPInaI/ExxxOQvnWFNLRrTAS'
        b'ggVnsOucO5QF2gfRshVAqdeldSE+xxl+KTt/C/qibPBONOQZ3bDCRlJWNWdxJp1Ip+E4DkdiiYMTNCqR0usgWnsYiMWeRGFLJNlH48+TTVJN0rvU3IyWeToSa/dhMTxM'
        b'3UvLP+ACRQeIanqwxjnCOG63W0gU9ETik9RzJJo79ulpbnXdY2zuakNyfVobS42OBG9nIeWt0HaCnnpfh0jrWTKUhZ4kNnl6Djq2QZ9xDD5KoQFb6VXbLxAz9J6NXUPy'
        b'5z6MOsK4Fi1oGTbGQ6klTJ5Pu2B6EIaS6KJRaI4jCdEsuUSzygsjmp92hSoPWNxOCncO7942xmeiJGy1I2KYxuas7zNpW4P9pLOJMPNTOF0uEl1m43AsDlxXJ9xTYHSD'
        b'ljF/23qCuNMWToZYq09I8lRoji9U37bceiMLiqRmxy5qh5IS72Y/ULCLZH8DyRK6zYPhppv6OjCSTdv7FB+ePKhFCnMGlvQisRebL5HC7VfBvCysD4+FxRsp9FVr1HlC'
        b'M2McQAABiHlYTCQGmIoyw8J0S+y1JtroIvYZDk/BmptW7LAQQ7sJNIGSC+7JZlp0Rw1JjwZaj/KgCEJ6Q7lhuacSsjdpByMB1m7s3UTCu//cgWxdWt5yYLxbDU9S0g4Y'
        b'woxeJi1OfjqBiurTwa4aW3AiKhjvQEMYXTIDd9VwSCcWS46zfrD0cXEatOiRmXIXHmTj5EUi14kd2nb+JKKaE/W9L10/QMZT13pi03ESOOXrrJVpLeudCG5WmxpDXYqV'
        b'5VHi15H1OOdDsuse2SbTpJCfprCceLx/ZSv2bSbrdgjv5kKLtQOJwCdqNFgB9rn6xLpmbzwXR5yeTxxRkEXM0KIJ952x8rIrtgZuJX6YMjLIiCIRuIBDZ3DoPLFOz0Yi'
        b'wbY9hFpmXaEYn6SlQHcmmeAlZCqbOhmTyGw8SHJ+at9mmnZ1Atwj2KCCAydIW5YQpdYeuIyPT5iTeKvFQmWow/FYGrudKK5FtPmaR9qZDJNjtMePNtkSy7RDTUwmtB3I'
        b'hrLNWKpyDssvQfN+ZCdfpgl5NmLpSdZPkvBJm3GgLjz033Y7hGhxBMdyIpIILzaGHTi6h9lmw27Q65luew5mWcGFIHh0I9E4jgRRsx4R+bQDdh+/6YO13rZEFWOmmzB/'
        b'R+ClEySl2qDSRpWnjsB4lCTAD2dtVUTiHSIsyyJjhYXJyVQdzwjAe8dSZWeDiGTneM7QPh+YD7AjKVymJBIfEmFzGE7ytBLPG8cCHIywW1UkPkgf54bzy70i9jJ/PHYx'
        b'r4q/CFu3Qj//AnsD9zB3fpGXmGdCPTgDpVm+EnY0dgof0hLV4j1ii5ZD2rTq47c0Lc9qQMO+UD2pEammGkcihi5ao3qG2LfhXT/vICi6dMDEhkTNLPaa55By6oQHfvqe'
        b'Z0mCV0NbFFYRYCH+xYe7mceF7O6abMcsLxgyYSAvF3pjpVisBZ3pUmKaWlg6AHmnjmN9MO0ifU+sWHiUlSWHfnZOqfiEISG41h20We0uZ7YQ3eWvJ9H4yDaCnlslCqEx'
        b'C2NJrI6TDq6lXSYLJ/EmFDmyQ2PhUL2NTIVJooUzBGBqtpGIG4X7bmQmFWZeDIJnAUTsPaQoyomsJi3IZCogs6zEzeYmFLsSentKMmKCNEIHTBD02kiQeACa98buvSrB'
        b'KrVYPWzyvQyDu/FJup0lzl3A4TN+a2BQ7WZWbFD6RRKiNdCjwdwG0GRhjvm0tsO0tfkkIPvOnaFnVdCSNkQYXyKunaNZVO+it+3zWKt5ShsfREdy06tFggUuJBbzaGFG'
        b'kUTpkgtUSHAiwjbEBQtPk1Tr3IcT24hz+l3tgB2nGITqfYSJquiV8tJNs5RJP1Vn0Gv0wOKRswQoa6HMFh6o4UgiVvtC/UHsOEFWVQWZL4tqa7A8cmO0jdc6HFGH+kio'
        b'TycuWbTRzcLB6PR07KOf+7k6NN3S3SdPkxE5SrK4xhUnvXxuGsTFwGNrHZjRxYe+LLFgD47u8CPmHoQiZM6dUj2y36chfy20XSRBAA0Hfc8En00/dcaUQFEJKfM5071Y'
        b'l77DlSTF5FUJCYheGHEwgaWsBBzeQ8ZAta0RtpgyOU4Kr9jpNrHo412EGEuZO8omOI6UKszugNZMoqlimD0LxSmsDDwMHSHmHQ24DaMXyeh7QLs66u/OvS8LElIyD8/G'
        b'k0HVC1V7TNfdsiONOx3M7AisiYN57HKi/yzhopUJNMRm2GeaEeIaPoBPLuhgvg4uiOHBBcLX5dFZA0q8kHg7sfsLrhmSo2MHrA7pXcURE9W117AzhrgjP4ok86NjZ7HM'
        b'39jEkyyXJWhMp8Us0jJWOXMxMDQilqRAtetaIp0GGDfHPmezgI37YeoG2QTFp81CHKI91UitPTl+kvtoJkMsaZgWqN1Ni7KgSS8xmUJCqYu0ymICzmTBjA2MQ/l+O+KO'
        b'PmxLoT+qru6EFlJrJOGrGal2wyNbGHNKZaXj3HEy5iwtdFHQSVMGN5FEde8pMaG+BeLrfAtioUc+pOUeKFtgvx299BR2G52EgU0kVSuh9VB6IGHtB/EknwsOMeH6CPJz'
        b'kwjkrztEaKHbXI95tgKxP8fQSxOGktnhxArBFZARTRxQfXkrTYtUGnbeImEwZ0GM0E6WLvQHXRBdwuLDSSR12i4cjifdMIVtsTTD+5mkiAvoDhaPbI+OgfGkY3tw2lQf'
        b'nm0+Q8TQZIy9no5sRWxx0DQW5xKJbhjWHyL7YSEdFy+o7NfH5nXOeD8kjaRahRF2GZINVnuDsFQeLF0hvDN9EAYNQqwPum4h9duB9RHq2OmTSovear09a4NNoskxH0MD'
        b'7DC6neWuA0WHlYKJ5oeIAEuh7xYJgs6sk75QfpYk7R07eGIcS2y5QHwxk3sqmbRlClRK8BH9PUJAb056leRtm8fN09gb4UCCqQWHbWD+8AUYtdzqR0Khlm0wbcIzEm3N'
        b'JBxGDeg1FnHp1rFAemjPLrifvMYnhMZ+uo7WY94LnniSEC6+qLLpYKYpjGZ9i4j1BK1eFbSHYbnCvD1Fo9+Dxp2WzMKNCNUSw2NDLAmGcVUHGD2ragKDOLERpncRFYy7'
        b'ncRFKHNMdCP6rOFuk6FNDiTFmJOu2cAeCkmoEYEWwQTZB/jsWoiDDQ04jAsHPGHQApr1LNbS4lfAdAxxa/fB/SIYNCf+GdoKzW6Yt5Fk3SSMnMaHJ6DVJYLETrEftMVE'
        b'kFIYP8kQShd2RqRvV5Ek7MeGHdibjaWOMLk5HAtSnKDn0mFSDD30xv0EXNu8SeDAXCCW2UeQ6mi1JXa+67DxVAL27llzJh2fBROxNZDyKNxprA4PL6WQpG8kKdGFE8Fq'
        b'xANLaSFkuNcQvVRATw69NKmrtdi3A+qzSKE0Bl8iaiLbpdFeJwUKNa3ccdQtEZv8TZJhAQazsNUNnnqmYyOtXRVOnNwAS+GivXhXRx2XJDTLoqA1MKfC3CPdbtAXb+IL'
        b'DUfXrXVjGp9eCUf3kRRfwMLz9EbEBbNECYtXyAQdMaJlb46KZpwTl2BNYvWe0jnP+Cva8Pgs9l0KCU6Mu0BIdVKXJtFCKndYEycDSExB40k7UyBD4w7eu6QtxZFwqDI6'
        b'FHn+Bj7wD1rvjDVO+Gh9wjmsdFViyJVkUCGZ0g9xITD7Jr1/eZQ+6a5OfLZBeSs0GIViUfRpnwuHg7yJwys8sD5jbwzObSJ5NEabWk7moepFEg4jWhEWXMAwuV1HS9kU'
        b'vRMe4eNNNsS5Tdh9nRiuEiasyQoqN1Aj9TiUdnoNDVoeg4vHrtDu3EMCCNUaMGO4z5Ek2oPrRrf1thN3NZO4eWaPJRfhwZ5kmLkCj7O8Jfxc+xQt13LSJgN3RqJkigNY'
        b'c0gvHXqMVS9tJ6HbThc+IoHY4Cz2D/djBlQ0PonGKR3irMf08p32+3Sx2uLMemWi8RZS3xWE4UdyaLnrd4ZrnICx3dhymsi7hST3Uy1mk8OwxQlabzKtodIEC8O8Gfgx'
        b'ooeNXrSEXhccPWpLVk6x/3paovJN8NDRkhi0fj+0rqG1ac0gtdMfC49OWxChtyiF7lwH3eZukBcFpTsI/nqQOLQ8YbOOBMX9BCzQgEex6bdJcxXAdMRuUipTsUyGl6tl'
        b'HnOFQe09tMZV2Gx2kVZpzhC74tfgmLp1juf+K6bQvgfGA2+SqOkl1deDzeY4k+mPg4aEdapIi84nkCrI0fRKp018QA+5v2lvJvTsU3bG0YNbYOCAJrZl4oh+3Hkz6DPQ'
        b'vwK1a7AiIJ4elA919mouQbShhDNoWZ4oWwWlHdoTegnHNpFoGCQuaovchEveJLwaod3P00NErFFGfEnom0TXfZjRisPiXaSeiUTLvWBirYaYZMHsxXMk9nppS57QUwsN'
        b'1pwiLX4PutXhbgIUueGgA8n/kltX4f7ec8jc5F0imLqwbx1JlKdQlLidOK3fDDodiM2biSUmyKpui9Qw34XzptAYvjcgzYfU5wAM4Kgy3XIHpqyM3cjo6IY+TxhSsSBW'
        b'aoOlrWvMCczes8XqmwRy+6CYLU/pNZiUpG3bR9/U7Ieu7adwjnQlNhhs2b8FH+yFptjTRDsl2JBOumkx+yyO79x/AgqSMkk41jmKdkOfNNs4KopWPimBJSZFwcQVenoN'
        b'Ibh7tGKP3Em2Fm5xI8NwDovT3QPiPIi0S7DshgMt8KS2mKhvSJvBY9rM5piM7Fx4EkJ/dkNLIFnpD2E8zRfHTnHNOI3z+88egEZr0ppkAPt44LQ/IbhxrRhngnJNEcQd'
        b'S2pRhNfyNsFsSpYysRJx7ygJAmKlfKJoxkuLOG9H4riJCHTGDafNCO2exlrNRC8Y3oKtXjugRkIqrkOHXeGhn0hG48KNeF9fwgMF/ifcrLAoJ5VA9iL2exIJTMJDDVzY'
        b'rZZEimdYjJ1h+HRrLuQRhqrf5q2nFYYNMTy4Nsq8/bdvQB08ZV6tbpgLpXckTuljPiOCur3Q52uCzddDt5/ZQW9Xj0P7Mf82GV+PLUg9lpyDhycIbz12UE1IdTGDCV9N'
        b'Yv0RuvCeCy1sURKxwaIedpyHQoIEE6ReKp2xep0aqz6k4YBjNxMIBBZFZcNdD9LLldAhwUkzDWw9GQ4FZt5mRDYj1ir66/HJwRNQrXtInVbsKeb5EKQZZoJtF46xA931'
        b'WOWkG3sMCs8GWO/NvKSJi/qncraTnCdofiD5GFSlYa1LGJnWDIxOuSXcJAop3Q4TBu4BxMmdpvBUE2ZOX0+yxYGtJLtmsRUKL+DTbE0sOhpG3FFIpskASZ4aslw20no3'
        b'bsB2bU1JnCmWn7mUeP6iK7YE6IqPmtB9tKeqcN/AlLiuFmYvafvZ7cCZDcwJSto7DxbWwiyL4PVbrCfLryLqoAdB+Ac7aTk6YWy9QwrUBG4m3qgk6ycjC5p30jYU+eHj'
        b'/Vr8/MICtB3NMcUu7Vsq9Ab3vaHFSOMmsd19+qsGluxSIq/Dg41kVxYY7g2Bx2bQpr/HQ/sa3vHHQouLatgfDvcTyCQeJjqqDI1gjlPsz2JeL9r6eRLAE6QoCrDHEUtu'
        b'XdxIuppw0Em6tj2YXubOKZzJcSRwBr3EMLWkrku0IqKyzhBLPgSmUAiT9uymd1vKhboNeD+WgPfjK0Qwo9fMiK6Gc7H4NpSSMCf4cec0NBphXdZ7hJasCTV0KPjgEHNO'
        b'VZ0iRUxi7NJBq1C9LVhNPHBqyw36us08PlrDDHvM926h3V3CsXgYUfONpEFmCCb1Ku3GmXWwhP17LmnRGxViRyawGHD+mf1wXxkazEieL1zD5gDoktCvffA0lhTOwC0S'
        b'j1XETnW0FzWaG7Dbn8TpMC19Bd6/iUswv98YS3fDvAN2bQnC8iQW7vJj3qqYY7Q4hdtIqJRqK+NQ7Fqi/OnrVsTnc84hqURvPUYuNLf7TibYsNnSBlu3HSXMQNzhRcSw'
        b'aJyAj7WxZd9G7NUh07HwHBR44dwhGNbIJvlSSxConuRzt4go/qkqtFv4QqMW2Qi9TnrQ6enMKgV1YqFZ+Boc2LxTVRVLjnuxEzF3vI6RWTzvSCir2A0f6aXh4x3aAS7Q'
        b'5Yq1nu6HaFGmoEWZ+L6HFTfKibTSZ2ew5kgUzEG+FZH6qJiw2e2rzkRttaFQqMWJYu4iyfCly9tIILTR+mNxKi1cH5MFj50IgNTGJUD3XqJo5oyvxTJTnNpNtk1NPJSo'
        b'QleCFQwow/gBd5xhNjrmHScRNh14jbT6M1dVQtfdUGGNBfa0NuMm0JULjQZEmCWbWERZ5abq7vhwenLdfl1sIACheo3hoAKjXSlk9BGqv0Myogb6jLD5iGk2S68Io8Vr'
        b'gacXrm6FIQdY8IZuGxVo3kgYq/U0DF4ms2cUuh0uEgoi5b3bPXUnPPXffgW7tkKTP/TZOR3FKRXSKo1+G8m2bcdJZ9Jzg4xJmsMMj7gSzh52xKUTW0i6NYZG6l7MDV8b'
        b'QbRTgnm7AmmMps0elodyRYQySy7jIHZq2ygJlbIGSPTe48VvCDS1q4iE6jcL9txN5cmWNMMlHZZChOJsszh8UKhvU+d5jd+F1WfkN3Vjr1CKqYbE8DO6zYoQjXAbUWUd'
        b'd4jtw76oAHsk/C0WifeKsCFqjVDLrYBY60EAVqq7ikRiJ3YUKg+ahKFmCZsPsSNSGTigLBJ70V03oI8/LjEE6gP84EmuzL+GLQaC320GCqMCQnLxMU3Ahb5Qv8A/xz7X'
        b'YCwPhDJDusFNhFUSE/65ilVIAIHOBmuZO84Gq4SaOWQL2mG5DeSdphtCRNiV5sC/iEiKw/Ig4jfBHVdDimpGKIJbfwTuBNhBxzaZ/46kYKPwDfOeVgf407/N9DA7EZaY'
        b'reHfRJxhh+np54lU5sVzwAobsTfvXyRUfdss4cmZaaExgZM7Q0U2Ev7xRrFwuE2Um2zv73lIKBO0cYNwbZ5OirbS5XARS0Hz5k8TDrUJzSJowrVQx7fQC5/JtjA5gL/c'
        b'CbirwXa946hs+27BAxsJ/yoehy/Q/k3homz/oFtZ6IX9kFDWHG0gqbIK+RbO4rzg7mwLyWYbqAStsg2EuSM0Eb7EpbQQASFXYEC2VXo4wb/YGEMYoTzwKNyV7RVUetM9'
        b'7DCdBjSxSiG7bsk25expfoe1NztBF7TpknxTRqDMRsw3OAC6QwL81c1lC0/f9Ca6fLdKJeMZrUlnxsPc2n9PNfI0+7f4az98J3l7Zftv/vu/5t+5sVFN3z9POSrb/o5v'
        b'TZ7FnTpfdZ+Pr7pd+bHx72f/cHUhPU33rW8kLP158b23W3/88Px7X20375+K/NyTiWcPst9zeqfsce9HBVH38vrd1Hb7hCyFbr3oNKjvb3P3lMe9Z1offeWv9fm+n/+L'
        b'1GL4K95e1w9+8LsvH5mOzP6lVpb5vt/Hp+0zyKjvPlYTmlLo+vGXvqy2V/WPGyvfv3nk6c/e2n28dGi+5Pt3T4V6/qw0uVP18bXjeyrDvu06eahX94rtt7r2F2Yp+bk8'
        b'7r3lsfb0dx6NvfN347UR3/lRhf/h/xnoqXlf+152UOzptYMqX7sbd+lLVV8OOr7+fl3gMb0uldEeo33+gb/8e8/3v3bL1HN+6uLEuXcivtNudcPjGzu+FRpwVTv99I9d'
        b'HGvfdrWzm9z8t6vr3au31js0qeCutqz4mrat//GNjREP1zc4j0X0/HzL9rNbrv16r/vXj05+ZfOXzljWnf3FH1VPzfSEbmueWueR+ae/jA38xmfxe01PTHN/9adfPI5u'
        b'udygPu88dm7wO2PvR6zJ2N78vxsLg3cELbRqf+z8uQhVzb51X5/fnfkPE42//rXYf1/TN/67Ja7qV1tUnY+kv1VqbL9Nvf7r7//z61eV0Gzjvh9PSf+54KDhdHum7vYh'
        b'7y+Hjn+57+cfOZc5/yE657fixD/+5mvXUr4rrYi+M9v6xXWJ8f2nPo5pab9+dZvzv/35WGHGL0/cbH6nSfrDH52aatrc6PngTx32f6z44P9r7sqDorjycE93z8E1IF6I'
        b'iAYpy+EUUFA88UBhGEAhgqLVGYYGeh1mxpnGAPEKyXoAI7Liikc8syqrEnQRxAvznhUlsTS7qSzZLrNx3XKtWv0jG3epWk0q+36vAa24/+zWVrHVxUd3v+433e91z/ve'
        b'1O/7fudvbL7Wk/LsyFrvMq6vqP/u79pQhPvOni+qa69f2dutmJ2nqwL/8WG4ozjjmdR7O7ksw+bz2SHxDwcfrbRqzxTi1OT2nedeBHWef2/tU+tE/eV5V1Oe/fbJ/Kor'
        b'rXc3fxPat+rqnwv+8vurdX8M+b5vvuXMwz7v/rwe9sieW3XhzdWH5393R7r3IvFe7+R7rf1fiYf3Nc75pvFawoazRw+3nv5h7Pm+AlEeafKlwj1cWxRDXpdE3Ka+mbty'
        b'8XYaFzw/E/f4mTfrXg/9b4yk1imFZGTq+Km0TxMymDKCzBQOUAUgGaPb0vzcAT4BhCrVB741xV3pTwhOF8eE1fAGvGO1alx0PK146KC3cefb6wPG43d1TMgCDrX5kmuC'
        b'/J08OoJaPBv811fiLjCiI2wINQQaAnxxe+AGLWMy8oSOfIDOyBAyC+JgvPWVo4eORF71AwhHOKtjLLwOdZN531HVYaRBNPoN1WiYsAKfYuNxzxsyRGevshR5kNdAzrzg'
        b'IYxh52sVEjJCKsQXdei6jPdTGxsXGSk/+jceM4ljCKMaMJlJGfl6+qCk4Y3SHXYwhdFx5/8F1JTwgmB3WksEgYatn4QhNJplWc10zSQqzQtmDRyvMXA6liycURscHOwT'
        b'FB6kD9IF+44aybOjMkIikrcw01lNKgSw8zw5d9IWJiZ0ymLYFpI1BjW03TZdXSuYp27rQ1aFpgVxRi44KG4LE5mu7jWzJjaKjSYYrUuga3Tx14IQMPSVP3f8UPA35/4M'
        b'budlCHzi8Hf1sD1iGrUxaDA6NBHIHTxG6NY+16sZt6jS6WKmQL5wGnEjpFhDO1GjnjGiTtM4bgI+jU9Ijw8u5j2hGoaJSiyc4e3N5NKCtp0pE/b0Zv2ytzgi4tKx4jWu'
        b'av/Av27K3fH1rGVxmrmm71u7nqVtNLyjNKVu3PK3L1fsrIvc9Pns2JufPh8V5nz487WrUotqf62kHgq9fD/h7zP7On710cb+N28c9u2e9ptdDfl32jK/kjbk7fIvOhTS'
        b'2V3Wsr7gi70T9ia11v64ufrCmZqwA0+f3H+84POa63flibffjVplqDn66OaxL7+dUfNiTP6+7tNfj4w9d0vZ5/3xuwnSnB9mzx33aVOop7QzYtbyovs/i8vqDlg4kTM0'
        b't0973zviE9eD4rpxnX/6+JaRfRpxM7x//VbD9pkLG/hbMz823d39MCx2zYPggvLJi/R9t5c/0HVdWjT22uPq0QW9BTf6P7l+6ttHY1Oa1twL9ZgmqoLj6/gk2ELwImnJ'
        b'HKok1jN+6AILoaXYq8qnt69IM+fE4vNwSI44L5ZlRuCrHDrGrKS65hp8kn7/k+4AJyr4CYx0RxXeHcyFl4+nmnIyz9vqNGdYoix6RrduHM8aRuBWOuahcyujcH08oXt5'
        b'DETznEA9BioWT0INqdF411SQQTdoGJ84FnWReVx5mer51oY78+hghw/g0+CakK0h08n6fFV3f2oKbgMdQuyAAZmRicN1XHZNBf3MkjyRFIag/YPKeXwin7bGCDLvrVeH'
        b'UEsG9ppgRpfBM8F4D4cuV+fSQakQH44yZ8Zkz0jSMHr8CzYGtevgtz36wdmLdebEJHIqYdE5Y/EBEJq/wc2uxttUAf2xSB7KMyyk2IZbSLERt3EJqBm/r97WCdy0FtdH'
        b'EQ7uDYREfvxyDbqCTqrOcYKMtoLM0YJaUE8MGYITNOisDdVSaSG+grbZomMxGf6aQfdfoSGz8EtLVa/ED0CyEA3GelngDWIhTcMz4zfxHrQD1UZOpReXh6+ZzSA1gKsj'
        b'LQCt7mdi8W58bC69uRLUFO4xFbxS7JvBona0YwtV0cfLE/zwhUB80YN24i4X7lhPGEYAw4RN5kfjDn0+7qC1uGeVmTcXUlMYqAn8mg+w+LhjIBMxvhxIpu31WZnhuHko'
        b'F/HBLNwigyLIF3ViEFBNJT0LtmfU+zEnA3njs2NNOmbpEj3Z995GtDtRbc5GwiYu+eF23AH2401MAT5FHtbahWoajk68tRCiy6mcX/sOPrlRgz8kU99O+ljbtZFQGAu2'
        b'44PiqtBKHjUvQ9t4q1r/NtQ4k7R5HbgwZrGMzxR2Siqq16sZSszxQrTWkRkbY4mN0zD+ozlffBx3qTysGXfkmkmHmOPIqeTFIR17jtzAyCSOvHZkaqa+ePurUXP06reW'
        b'xUSBsBX6A+9mcVsFoWCUL9bJqCs6k0yIzITotOIWX9w2mLFo6vB/pf+PBoYxw8AuXmabdsEIZDRQxb+BLqOonZthQH0KujewcQMrteABczVyJOf4zzV0g8s0VVZGKUKU'
        b'wtlFhzuXjGWKVq502UWFt0seWeFLJBtBp0t0KJxHdiva4mpZ9Ch8sdNpVzjJISvaUkKQyD+31VEmKlrJ4aqUFc5W7lY4p7tE0ZVKdlkkGxVWl8LVSC5Fa/XYJEnhysUq'
        b'cgip3lfyQLJgq8MmKjpXZbFdsin+S1Qdp8W6jpzs73KLsiyVVgtVFXbFkOW0rUuXyEX6FCcliw6w0FICJI9TkKUKkVRU4VL49NzF6UqAy+r2iAIpAvG6MqLCWTIrRc08'
        b'IpRIZZKs6K02m+iSPUoAvTFBdhK+5yhTuEJLluLnKZdKZUF0u51uJaDSYSu3Sg6xRBCrbIqPIHhE0lSCoBgdTsFZXFrpsdHUT4rP4Aa5nUoHeGi9JF9qe091pwM9MwMs'
        b'A8gFAPc1dzZAGkAGQApAMkAOwByAJIB5ALMAFgLMBpgJsBggE2AaQCLAfAALQD6VEgMsApgOMBcgC2ApwBKAVIDlADMAEuhFgtBwBaytBFgwJJuEB8lniEj9c/UrRIqW'
        b'PTeUkidFtJXHKUGCMLA+wKufhw5sT3JZbevAQA10vFAmlmSbDFQAqegFwWq3C4L6yFKJ5BPYr1NTtbrvwp7CQcb7k+TdimEO6fdKuzgPtjzpBHiWcIP//tV5cxR1RfwX'
        b'Gu3IKw=='
    ))))
