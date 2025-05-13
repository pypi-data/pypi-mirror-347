
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
        b'eJy0fQdAXMe16Ny7lbYUIYRQW3UWliLUq4UEiA4CVIxk7y7cXVhpYdEWVVSRBBJCFXXJEuq9F8uSJXvGsZ08x3bsvMTZvBfbcRLbiR07zS/WS/ln5t5ddgEh7P+/EMOd'
        b'uffOmXLmtDlz7ifI758MfqfDr3MKJAIqR1WonBM4gd+Iynmz7LhckLVxjmGC3KxoQIuVzuQFvFkpKBq4DZxZZeYbOA4JylIUZNGpHi8KLs0sTtfW2AW3zay1W7SuarO2'
        b'eIWr2l6rzbLWusyV1do6U+ViU5U5OTi4rNrq9D4rmC3WWrNTa3HXVrqs9lqn1lQraCttJqcTSl127TK7Y7F2mdVVraUgkoMrR0rtT4DfePgNoX1YCUkjauQa+UZZo7xR'
        b'0ahsVDWqG4MagxtDGkMbwxo1jeGNEY2RjVGNvRqjG3s3xjT2aYxt7NsY19ivsX/jgMaBjYMatY2DG4c0Dm0c1ji8cUTjSEs8Gw316vgmeQNarVuprI9vQKWoXteAOLQm'
        b'fo1uPowbjECVTlZY6R1WDn7T4LcXbZacDW0p0oUX2tRw3daPR7RseuoS2/iM5cg9FDJV+F4IaSZbivJnkybSUrS8n4605MwpTlKikZly8mgUPqaTufvDk2rSJOTl6HOS'
        b'yBayrYCsdyiQhmyVFeIz+Iw7Bh7AjwqL6QMKJJfjl8khDh/DGyrcg+itA/gaPpHI3izIIS06JbmbI0dRZI8Mv/Rslo53x8FTZEseuZWXNhoeyCPbi1LyoarwwbLJk9PY'
        b'7RXJZBe9m1MAN4tjcyj8K7JR5GANvN8XHhg/HO910ru0fds4FJzDz12Fr5VaWE9rZuFDIeRGOLkdN8uJt5C7deTWEtwcHoZQ/6FyFTmGW3QcA2TEj8hm0pyfS7bJkIw8'
        b'JBv6cvgw2YfXwwN05vFDZ2oevhwPY7E1j2zDl/B+vKUIWpWDW1IKk3RKNCtTVU8O4jvwQiy80Jc81JOb5BC5DE3LL1IgRT1HTkVWwe3edDUsJ/cTc5P0BUnJHArtLVNP'
        b'DK6shXt02IPJJfIoMVufQLbk006FkJ18PD5CruCbkys5v+U02jvvOyk6BiIj+r9Fx8b4Rl1jQmNio74xqTG5MaUxtXFUY5pltISkXFMQICkPSMoxJOUZknJreAlJN/oj'
        b'KW1sv05IahCR9CW3CoUiNGHzYKPt9SGRiBWmyhnmTh8VZNT3e75cLPzl9CAUgVDEmBqj/nH5TLFwl0WO4K+x1yxj6PyhVeg8sgVDcaItVi7ovhqO0Mcj/8zfGfVJ3hXO'
        b'FgQ31scemPwfnDEcTTem/ZfD+Ox1xIoz+/wlPaV//CC++CPuX7HOETrkQe5kiqKb8dEBsF6aU2bHx5OtKdmAAfh8WXxuAdmhT85Jyi3gUC3ZgK+HB001DXPPoMiyQx7i'
        b'dDmWLnE7yV1yjdwiN8gdcp3cJjfD1aHBmqCwkES8G+/ATXhbWuqYtHGjxo7Gd/E1OaDZgiByuR6582g1Z8kmvCEvP7cwpyCP7IDFuo1sBVTfQlqgNfH6hGRdUiK+is/h'
        b'SyXw+g2yn+zC2/VkL9lJ9pE9pHUeQn1Sw6LwJpkPbejgq+C3D52JVC8Vk1lk0rTyTTCRq2UwrTybVhmbVn6N7Em0R95pWuWFDjrf1oc7sxXOiZRi9vpjnmnhK+++em3n'
        b'9X2DFW9eMM1/5cWINxe8cmtn275/Rbc1WDmnqjKMzDijj9mZnSqrCkG5W8MmZL6lU7joUiJtfXiYgK0wBLA60/E6+UQOX49IE29uwOfHJSbD4GzRc0g5Ro2380l5uMFF'
        b'6VMIObo2MSk+O4lHyoWwYg/xSf3wAxftPHkhktxLTCIt+aMUSEkuVZRz5PL0YPbaoFpynDRn48sI8Qvx9dVcFl6PL+s4Dx+v08kctKd+CQ/J495TLA77SnOt1iKyn2Sn'
        b'uc40zSNzWwV636mk4zUzmIviHErvSzq5J6jWVGN2Aqsye+QmR5XTozIYHO5ag8ETYjBU2symWnedwaDj28HBNcV6B51EoMeQ0PoyKAwNhfEwgldyPKdkKSPS1eQ82Z8I'
        b'HeUQjw9wpGXoTLx5eFYl3wEl2CxSVgJ0hCKF3CL3IYWsW6TotNaDOyFFr0J3NFwPSMPNznzFCLIdZuA8YHgmbmQ3yCl8ypyXrxhQijgdIo14A3nICKWuaj65WaQgj8gJ'
        b'xCkQvk1a8R7xlb3cUNJcpMAvw0RxmZC3aNwUKrk90xJSoKjGxxEXifB9cjuHvVA5AO9MLFDgzfgs4mYjchifHOOOghulLvwoMVlpmIS4BYic1ZBrrJhsrsDnyJ7ZSJeO'
        b'0EpU8MwKsfqbHL5H9ijRtFlIj/T4KH6oC2JtJRvxWeNkHuHtAIFsgv/D8T12B9+U4eOreLQM70HkNPwnu/FhVht+Ae+04vtKlJaKyH7439/NZo2cMZITBMrJOnISkbvw'
        b'H5/tK966UUGO4/syRB7AOJKj8B83DGO3CvBeYBT01lXcgsjL8J/sK5SGqwi41v1wNC4WkePwvxqfdEfSCSOtVnKSRyH4FAg3ISNXs1LSlkPOlgIzHIngZzRuEPveBBWe'
        b'IHtUaPE8lIpS8bYUURDYQPasBJKzX5VHLlACiAwr8G3GCPG2ELyH3HSSm5kLlwIKknPcMCBZ+xiR8NEl3p+UUI5cherRcxGruXquCaRBh7ye28UvkVNkY2tHXEC8h09O'
        b'9XCVOq59KbJF8Th4is3qdFXaa+qmzadV0jtK5J4itvXMijwQOGaF+fh3NmDVTSCsW4oKyTYdviNLA0TNw7uh3SHkEsIPyEsh+NrKkdZffvEp79wLtdTuGD58+8uaDcXR'
        b'De98nin/wbFXX/3JG19zB1qCZFt+ctm0ZHlKVB/lgTF/+lqj2T9+b/OCX9ZbFy8fsXnGOfmAoW/HOt/eqOvz4a1eDfvTVx742afH7/W/NetmleXFN/5mfav1FwdOvPHJ'
        b'/Fxn9Q8qdy6svZ846cuIprkL8l87He381RLznk89swadb+1X++EnOxY+H/f43xc3nfrP8I/surEP+wPBpLQNn+o3LTEZX++rI1v10G98iR9dhtczelk+3gJyB2nKyS9U'
        b'oN6hIfg6D+izM81FxalFQCpOkmY9kLtHIJKBRKh8nh9aT066tHD3mX7kRcYIyVYQtsgWfClXgXqNSSMPZIDODXmsfjs+RtpEah3PUXrNiHVRRSe6qZN3JKSBU+gJMddW'
        b'2gWzgVJSRkMHUkTJlnNyTi39yLlg+Ingo7gILpSL5RwaP9rKOT3BtXaDE2T7arPTQZm8gxKmzi3hHRH0OtxHUmk1OT6Sei/Kn6QOhpJc3EIa80SZlSLQWrIHcEiO4shu'
        b'+TKQju90Q1wZvw0grt1zXMvTOW6QKEjdjeyF3l1bAFfGKY5h8aJ4pIvPRpc0QzhkNAYfLq5BWaz0YVgEqn8OuEadUT+uv1t89F/GYPRumQ4ELKOtTb0MMcq1EG8kLfha'
        b'6uhUAAfUqwKkjE3Wv/9musL5LMWJNeo/GH9vrLbkm96yxO/7bN21gzee3SqUHGjoOyk2JlUvfCZ8ZtSnyW70nRzbJy3mcLpQMr8ktvzgsHT95ui5EXlH2va1NdxTCnz9'
        b'7gXjSoH3x6GhP+u97u4wHe9ihHNvKT5JWfic2ZSJUw5uMbiolLwGt1kSk3P0CbpksgNvItv0ZAtCsVr58+PGSfTgqSgWWVltrlxsqHSYBavL7jBIzJrNenksQzQNpIBY'
        b'kX6IJau0Ch5Vpd1d63Ks6B6vKBtx9PLhFa1lgQ/C2QC80tPeXn0G3wekygaNBm8vSgYZcwt0KwXDagL2PRWfmYsPK8kZmJFdAZqAD8WYSMcBkrWLdBxDsB5K6rSZwzsh'
        b'2BAJwcKj0DAQKH4cZFw4L2yNhEs1tkgE5GHCZYcxf8M8NypjpQ/iFFQsL24tMuavXaIRMeyl8TKKvqn7OaM+NV0nFp6qCUVAOeZ/VG7UD4VJZ4UfPx9Nte1ilGOcclxf'
        b'JRbGRAxAEwCSZb5x4fG0BLFwTpGW2hUmjHIa62MSh4uFvQcPR9kIaWuzjXzN4FCx8H/6xUOFaILZYuQPPSMTC2cDDwcOkeouMfJzC2PFwlYTU0m0K/VG/ZoluWLh47gQ'
        b'BIw0flu0MT8mRwJ0LnEkyqfYmGKccSRdqnNpYSIqg7X1Sl/jkOZIqZulOX2BY6LlX5iNU/40rE4sXDaeaTTZ+6uM+j+F1ouFZ7LCEWB4/PnJxvyzw2aJhfPj49AYaLyj'
        b't3HhJ7bnxEJT70EIWFp1/DjjwmND0sTCI7FDqDxo7KMwVmQlZYuFkWV9oKMoYk+isf9tjQQ9PSEZLQQlK32ikR80W3rdlTQWVcOA3CswRt0J6i8W3pg/GjAB1f1cbkwr'
        b'dxvEwr+7UpER5ihoqbFi9zOjkW4Ykxxy5pANo0EAIaCVjkKjEvJEyeHWatI4Wo639Kb2ijR8Ht8QxZJ7II+dHM1PJA+pQjsaXwG5gS6blElk22glPol3Iej4mHHkHKt9'
        b'IFkfNZoj1/E2hMaiscpgVuoYjk+MVmSQ3QiNQ+PIpXQ3pej1OvxwtIychtU2Ho1X5jGA+MGz+PhoFYhgx2A40QQQZy4ygPhW3lB8E0Xg+whNRBNJ63JWdW0VfoBvyvFp'
        b'6MUkNClzFCvFzfWwPvChWQjNQDOs5LhY9wWQTzc7eXxsDUj7aCbZSA6y3peBsHncqQT97CQV1jOewzvclN2MCnvWyWXCkshEmVl4l1j1sT74gFPRDx9EKAtljS5lrUvH'
        b'N2c6ZbgVv4jQLDQrCR9kXcxcgm84VaTJDEiEspOCxGacwocA9E0YibuUkeXg1npRDN2NW8lmAr05AMIeykW55K5NnIbr+CHeT27y5OYqhPJQHrloE0dlUwS5SW4qSasN'
        b'Aabnc9NZh8JBCQYIXAGIuagAFZAXw9jjY8mhenJTEVyOUCEqxNfwTVb9UlCojpKbMnKJzlsRKlqAT4losXkBvkZuqvIi6WIvxvfwHdavKrwVXw5BKXF0hc5e0YsVVk9L'
        b'DoGmA7EoQSXkhfliA4+bDSE8eYFOWykqJWfmifLr0dm1IUpyGICUoTJgEayGUS58N4QLfx7IBppDHgns0bXL8KkQxUqq7s1Fc1eRE5IAjF9IC5HhvUBx5qF5Kgl7jgCr'
        b'2RCiIvsx4Ot8ND+JXBVvHMWPhuJmhO8mIvQsehYfBZBiD/uAuNssx/vWAlNB5eRQIqs/eWYWbubxkWDKEhbgk/G2v//73/++5WJk09gvzxi6LWaquNBW5Y9HMPqxq3TG'
        b'tNefWYmsWfsf8M734c69t4pqdkyt5UfFZnx6c4D6mcERbypn8mGq7DcUL3KK6JzxM3bt3PlB8TphnvqHt34afX//m+snKMypJzLixpT++HDFXzcE3+j9o4Vn3RdGbYj4'
        b'6WTzrsFvfLVuxI18xxebwvXXsn88a998y6Y50/7bPHbazbeVhg+EZjxvRH3l4X0Dln779o5PXmlQpBz+xcpbJT9/5/l//NeP1B8eM/wo8erRiqT0x58O075f+Cles2Hw'
        b'A314Yf8jd+6OW3+/9lfyCZUnZ77z6wrX1qxe+nJl4uiUs1Xp+adKM26+984zqsOT2komgAxLTUUK9UgQRAupCWwHuWgC3T4EX+TJFbzOwgSDkj7kEsgF+ERqtlcwQCtc'
        b'A+iAnwcFCIQzUHkLkjRjcql5Moq8KCON5ISTyceLLfUgoW7LC5mQQyddOYHvC9L/VhcV7QrJOnzSiS9nFybFkztkAzVgkh0yFEl2ygCdLwTpFF0KFfKuJAA/UUMjiRru'
        b'SgOVapmcQQ2LSAjl5HwElTX4aI7+RPFykAfiaF4WARJIBJNClJwj2ieDyEAGcVd2J3pwjt4+qSOasXGv1PFCgIEA2DlyLwvxkzkKyhTwhwq2CqQj6xR4DxCdB91IG9Tq'
        b'iPykDa5baaMH4qxKlDY+WB1G5YL4V4YZQyfPSZekDXMu48Lqdyda8rfP6IfY4osDetdGJVTcEMSE1Bx8wPrgB5/JnDPh7u/u7/iDsfyVazvb9pxvaGs4f3DUplGH27JP'
        b'9BmySRf7Zp6p0FRt3i2/HltyIF2/ZHP5Zs3rccrjk/bZjse97ULv/DXsWMtsHScqVs14+2qyk2z2GpUo2pmWecXNbqY/Tpx+p8vhrnS5Qd40OMwWswNUHBEVQulwrEW8'
        b'GvQYJnDG+E223AkPdz/bfXyzTV/c4JvtdQGzPYb2YaMFb/fNd0qyLqEgWZeUW4C34E34fkpuQV5SLmg2oB3iXXhrMFlPDi7pdvYDZc3uZz/AfOitMHD2lYWiRWEf3pkR'
        b'Qo0EePN4qoIfxOvJFYYCk+eMoRKKNlXXPDjZPg9lWWu+apU7x8Ot//nsf/5gXMim+nrDEq4y+JMZrw+5pzmjed3yevQZ2769wpDT0b8zbtYoI545sH60DGm2h+heOy8p'
        b'G6RJh/DNdP/JjeJdVO1k5oHDPnVDVDWiRoKygc+Tw9I8PXn2YzvoGYFzHyzOfZCai4G5d8T6z3zlU2e+r2/m6YtbaIURbObRtwFzPwrKgvAOuuPShX7hP+8r8PmgkhTS'
        b'hJtqu9VjZR2MhN3rsRs7Lvyupp7Nb15vDZV/s+9MNeY7ldKGwNEljDFmb8o35j+HVoiF2f3ZLkHEOrXR9vL0WGSd/1utwlkId1w/HXWx7jPjF8Y3K6otl8yfGc+Z3rSk'
        b'pP3eOP+VF3e+/dxgoADcm5Zc027jZwL/3lvaNah4jsoZXDr65ISZI2cOLp2wc9Bbrxzk0FFt5ND3LwF+UJycaAQh6WJ+gZ6cnwSA8zh8YyTexrTRZfFmYFdke0pRAWkp'
        b'nET25OBLctSnRD5umaqn2mhYrXm5yyC4zQbB5BJRI0pEjXCeCwbOQE0ePPADR5wPReQeOX3YE2QzmwR4b8VTDB2UtTr6+1CGVrTDD2X+EqCSDoGyNNLkwC/lkma6+4W3'
        b'FOkKcEsR2/IbTm4oyslWc6VMmlSFP46ME3FEzralFI1Ki1LCExkzJssBT2QMT+QMT2Rr5F0xCFqlshOeKEQ8GfcMU0pQqs5d+qZDUnTGaRieaFPH1S/m+UhknaSeqnBW'
        b'wJ2ayLIB266HrUsNlX+4tCQ1/Wc/1NxqPX98pu7LhGhL8zXd3Avv/6Ho0zF/evX4gehhbzw3eXJc2LQPPngt895HvX+gS5j38OLuT19vyP371BVbkxoaLn78i5+PP2HM'
        b'eX+76bdffstNXdJ34uYVILpQNFGSkyvJFpC0qa1MhXh8gpujSmS3yEl8Fd/Oy8EnY8RdUw4fi5nrotOQosYb8uhybCYtReRmLofUZBuPNxY62W3yCO8jd+FmE9lPLqcA'
        b'fZIXcPgR3pEj2knORFcHg2jaXIAvIQC5kZs1ZXR3ooryibc6omVolbkDVsaKWNkX8BFkFQ1gZTAXyvO8mo/hHQN8uKmguAkISdHNo6x0u+wWf1rW5XIAnKW7x46BgXhK'
        b'Kz3oh6efx3Q0yeGj1Zl5RUkBGDoIn5CTQ+QUObwAb+yah1GO6Ns3RRZFD/lYtT+ShsFv705IOkhE0uv1P4oagOJlKMKou46WiEiawmtr/8Svo+a3hbaFq8XCH84Lij7E'
        b'a0H4N+pn2ueLhWstIQlfUktIhNFWnV4qFn4aEjXwb9S+gYz1USFZYuHl3AGTbvN1oEYZ+3+xKFoyuMwZk7ALvQs6vjFqfrlk3fhrjapsFQ+TqDWGvhPnFAv11nj+NHec'
        b'QueXg7bPCqu4aWtK+b/DEjNGzeynlShx3NTqzdzXFFDaL9YuFQs3Vk4u16PPaDvTUqokI85NLjbtR7yR1ll/25gjFtZl6YesQtfo6zMe9Z0hFg7LjkgdLZtOB8R2dbhR'
        b'sm6UTl95jfKKOmPam70sYuHekQpULougPQqNdJSIhZ8tCq21cam0Ttui4j5iYdisfss/4atpk/pnDjSLhSOjxk3rw31A+552aHlfsXCIpThjFD+dAgpWPq8XC3cjszKC'
        b'38kBoKyH8yXjCB9XpdwpO8DB6yN+nSKN0oCsGFsOYAYULvynxioN3VJNzCRuAh062w9zpIm7m7pqWhb3GQdNirnWV6rzQtzoiuP8m3Q2HeXzF0gDUjh0/t/5Jlo4pHZt'
        b'JrJ+O7OYc4IWhKalvzxn19QSkhqxad6+f1z9aELsgsjo/hsXnHpTsXQzHv3WR1sr5hyc4Zo4wyErxKMmqBI/Xn782dVF9mV/e/2bLfNu/r34+RWjLHv+hC9O7f9KYnRM'
        b'f+OG3cdlrbLjN14Zm3G+ZVLlj5Ji6/jmf0+tf2PB9S9ehXW0dPqGo1tvD9l0W3Fl0s8mufa81vLbb7mFW8efUh5vnUg2l57/cJ7u47CCQUs//aA4696932+Y8+o/h+99'
        b'ccB//vXLmSt7t65/9qXfZ77RL8dcvGuBrSpn7/75b23oVbbrlwedWWv7/CP77oGrP00avawtpeTRe9fejmv9j4zm/zXjK7Vbf/jruP9KvvXtXzz/zP1i2lcLX3ZNqVv6'
        b'z2+yH4f2+dd7J6ds+bz5r2Nvvz/yT49XyC+8s+GvmU3Tf6jAff/1ea9jqvgP16IhqYseNE7TyVyUmqROwW1+3DkHt1R5uTM5Ru6K9PXSJLIxD18nj/Tx2SAHAfkFfXNF'
        b'Jn7EtjUSnaQxESpI4JCcXMCb3BxQ+FP4vC7sKXT06Uk3VNrfVE2pcIWpdrGh2m6zUrrKSHGZSIonqmVAjOF3GBMTIjgt2w+JYCJDFB8qp/skPNstgR9Zh7/sSiMLheej'
        b'uGAg42rOofWRcZBCV5hNDj/K3Q1b4RyDfUSbVnHFj2j/NNqfaDOvmlsVOpFo54KWDcoV83IAGTUfxCe9Ek0tWkyuK8mLiasDlAaF9NdpgcRM3chQOS+EMLs3D7oIL8g2'
        b'BpXLzHJBLig2ogauXAHXSulaCdcq6VoF12rpWm2WU05g4YUgIXijGkqCGkG6LA9mekuoR5UuCA6z01lYqZTgq6VfRvgnUU4iet74PHEsaomfKJvUwE9UwE+UjJ+oGD9R'
        b'rlE9aQe9s1asKGQWw5RJz5aiheQWQoPRYHOm6GpxIH0O53RRQpgzb8DW65E4NUL+76J9G0sbX8uITle8Hb8uo/LswPS/b82+Enq+9FfDVjkn38/rdealA64P2xK2fZU4'
        b'e1Dm/bQvmwbe5X/9Yh9brOevX+RP3vyPXy6cN379t/XHtuCvM3eEjpCFHQm9mjFh9Mm/4N8cCSs6eHfQm1cGjU3tpQsWF9Bu42RyA+/KC1g/5CE5xbYWyRlyYXS7F4d8'
        b'4qQ0Dl8vw4eZYh2DH01NTGbblXjDbHHHkpySM0sQOUoaVpPtw5n7lVgzuc/jLeTOOLY08fFovCMxOQl0NtKGL8PLp/hUvD+YGYOm4B2loLXvIDvykmbQC7xDhUJieNKI'
        b'9wlMco+cig/j5iJyEGjE9hTSkqjDF+QoPEjmqrGwtoX3kdP72/X4vBzkM6RU8337kWZWfZQiBzeDqjSE7E5JzhGNJlHktAy05t16Vj3epcFn4JlkXS65YypIou5czTy5'
        b'i+/hfZ0FdHWPKUc7ZVAZDLXmZQZD+x7pWpCv2d4o1Sg17CqKU0o/K8MlPE6W3hNXudojq7Q52V4VaJ1W1wqPus5Od9AFs0fpdDnMZpcn1F3bbsDoTs9QOugekoMal8Td'
        b'rxE0oZ6UjngfeaAeev/wIw+b4/zIQ6dW+sQ3Tvotpa/S1VePFommBa5Qx3nUBmljDq7lTrPN0u4uIA6XeorNVFMhmKaFQS1/oTWujPDC8t56KjCLCExhoCMFRC/BB8MH'
        b'yJEIiQZedtCdvZ7WGGTwjno3tYb3uNaNYq0qgziD3dQZ0anOADmZesJRWw9Qx+9p6eE7UTRZodV1ep/CScnD/m/+/AfjZ8a3R7wF+nqo5aO34OE/869VTdVxIhHYlUOO'
        b'tC/D07iZrUPQiC5JriBdq9RWp5/Nrd0Tay38xKzs7Z33gKe81hw2Uu1IzgdwuQTf4FErWBTn1dXXwc/XGn9E7hoIkHP6TxcCCGugTmAGgyfYYBC9lOE61GBY4jbZxDts'
        b'qcB6dNjrzA7XCnFJDQ9cV6msu9RpzOR0VpptNu/C7mwyAiQTH4NHWBeonv8/SDIZqhWIi4oI5diP6KWLr+GGWc78HF1uUrISBS/ig8hV0kge4u0BMxwi/XVu4/zYMlcO'
        b'0mVreGsE/Ia1hlt5Cw9X0o/AtygFPWXbfs6qEcA2KeMOAhYsNyuAcas2ImDTQS08MG+FEMzyISyvgnwoy4exvBryGpYPZ/kgyEewfCTLB0M+iuV7sXwI5KNZvjfLh0I+'
        b'huX7sHwYtCwYkD5W6LtRXa6hPRGoiBDXwrE2h4K40U/oz8SFcHh3AH3XHC4MhLdl5RGs5+HCoBZeSJLsIDJBKwxmfYuE54cwWEMZrCjID2P54SzfS3y7VdWqtsha5cKI'
        b'FpmQzIQL0decjpamMdwSJMQLOlZjNNSQwGpIZDX0FmRMWU0B4aWS0cXHI4O1fv+kUtEBPuCOTumRW0He9MgpDnaFcoWVKmnC6SLReJd3FqUUohQURAdPmlSvZ7LGopEo'
        b'iIrJRGqgICpGQdSMgqjWqIGCiM2Wf/wtoHBAs+i/nFqry2qyWVdSj/1qs9YkdcIK3MlUW0ld/ju+MqnO5DDVaGmHJmkzrfCWg72aMyO9UGt3aE3atCSXu85mhkrYDYvd'
        b'UaO1WzpVRP+Zxffj6ct67YycmTpaRXz6zJlFcwrLDIVzCmZklsCN9MI8w8yijExdcpfVlAEYm8nlgqqWWW02bYVZW2mvXQor3CzQkwi0GZV2B9COOnutYK2t6rIW1gOT'
        b'22WvMbmslSabbUWyNr1WLLY6tczwDPVBf7RLYcwE4FedmyMND53pSaxd9Mp7rsI7vKB3CGbHE1+W2K74vpSBMSotSho9atw4bXp+cXa6Nk3XodYu+yRC0sbb6+gRDZOt'
        b'iwH0AoXuSBDhqusW96QeL9MV6/Lmvn99IrsVaxOvv0ddAdbyzlbQ0EI3XYv4+HP4IDUa6pPpMYi8eaSJHlA4hO8UiBYw/ABff44ZFTKH7Si/jibwKNWYvNgcidwToDCZ'
        b'PEhiZsNi0kTF6xSypRjfzSFNRaWspoI52XQ3tKAgp4BDeCs5EUTu4K34rOiRo1cVHkTMlJT/SkgqcqcgdvSDKnLNZFtiHvUTzJ+d3S5Zk93kAD6pw+dRabqK7J+Nd7GK'
        b'4kbyxf15emUMNTxnE40gG2bKE74VbT22sFU65KZMDmT8i6v9KweN8RY+RY9uQINTSrLJ1nwlmkVOK8l1chU3iO4N2xfXOPXuJcDuyA7ai9v4uPXV7d8i57uUdh1RDd8x'
        b'uXbGqIjMN755sOPbjdrTgxONfb9YP64kLjFzZ3zoaWvF1v9duvPP93446Y1p8+N+XujMmras/vT6hncsf/56/92L8j0/3vFq8XPXRrasmvTzIy2qlXlXR/YJ/+tzf0uv'
        b'3TBw69jXUw7X5L/77lfCuMxf9/5v27cDl/7Z3nz0r1NmPDPh26KqeUJJrW7MqJf/cWPZpZdzfm3YfejD3/zj7R8n/73i17L/XmaYGP5uxSLVvmOVUbvH7wyZ7+h74dmx'
        b'V/oZ4sZH/E7zYM/CMVdu/PD2b2/X2Br6/+DDY59ez804874uStwIf0DaNCFkYxAMlK7AnZRAtqbwqDdulKuHD2LKyQi8AebDu82u52yF0i77RHyMVWF3TMpLzi3Q59jJ'
        b'C7iF7BAPyMThW/JarYVZtHGTuno2Oey/Z5ZBtrOtdNw2zpBH2p7z7jd5X+9NNsrIi2SjhoEwPEteTqSKY+Dmmlb+vAVfd9EZzyB7yWWYcaggkdBDN9LWZR70CDAe5v8K'
        b'3aGfha+rQNG7UsTUUdyaWyWaFig+9NOjkNk8PH0X72PqaGo9eaCvxs3eNinIIY68hG/pxH3eS846KmxSTJKRw1y0Bm+3kAambromj8D7V9M36eJQwJsv8RzZxbMBrcG3'
        b'yW4mpvprkisrXOR2qouqPngvOYXPU52xRcfORulzKvBDOrRibYn4poJsKs5jzchYCVoirSyfg2Yc48KfwTvx1iLx3MMesj4YbiYX0Cbe4VTkLD5MzgxjzViLz02hLSwA'
        b'esAs4ZoqGfWbn0S2xDBxGt8PA4W3ucgr02lmykrI6SzShG+wClJwG75Oa9DDODPXVg0+J8MHh2Us1nq3szT/15avjtI6iMJW4O2SKpvlFdRHqZknZigv+kLIOQ0fysXw'
        b'1LQVKjkBR8CvssMPT2Vw+AnlQcETqW6yF0ChKBsHiXI8PaTioPabLiXrdhWgx9q5TiVW0iuwdlZngq9iJntTj/RBAerDJyP81YdOTe+pIqwwUGmnG41vvlfja4fh1X8f'
        b'Dy/zCUeUbYEg4eVb8Q6zSUiy19pW6JIBikywV/ZUt5UbKqyV3TRogbdBj4dR8CBYdQu950o6lWa6gfu8D25i97LP9wHv0KF2hbEL4CYf8GR/wen7wg+W4C/ivJjAw7Iy'
        b'iSooQ8pu2iIEDkR3ItV3awgbCt6R6V0E3bShyteGlJ6IYt+tHdV+7RjZfTsW+dqR9HQh7rughWiSYW3oBnyND3xqGdNLALK/9U0rTanWxo4zd9mC72/AkdSvxyc6yaQz'
        b'qT7h1Fo7rEun2VzDjk+DEsPUjE4v0iPVkm5VCroM9CjT7bBri00rasy1Lqc2HXrQWQSOh25CZ+HFpeOS05JTdU8Wkuk/BepsNS/TcW524O8cCDtHEikzSyCPkHw6hy9U'
        b'kQvWWbO/4JlHyzcNzX8wvlWRbXrzd/ElnxnfrPgCcnxF3OHfRb8efeb532leX67U7hh8YP1NBXqNBM22vqWTM+eggSDstgGzPIlPdGCYGXNwo4taV/Cj6XR33ycI4T2i'
        b'xOoVhhZwjKnnkyPR0inkqXJ6DpkeQj5ILosnFveQCyPzmEzCk3v4wvNcCr5G9ndn/lJRm5P3+IzkZrQWLQ3mYqiBVSL60jOF39HuRU+o1gUwrt2aQANuYP3wMmWC3XgU'
        b'URMBauR65FEkYytJ/rixE0KUml2iWcBtc1lBKZYIutspacEscoDLYap1mvwiAFSs6FQRrWMSM4xMMhbAM1AV/DFVmR3GbnQ1+q+zqVPyWHlpyXbUn0Ox13JXFK6OrENu'
        b'6iWTQ86mdFTASNMgvL0bBSx/rXXnKz/mnVSB+yZ38h+MuYC1+pLPjZ8ZF1m+EH5vlP9Et+0X+syE4aG66l9OX9qr+FTDxBdGbQLsHT0AJXwZcmDDKJ3o2rYggdwaiu+H'
        b'dFYS8Mv4PBNaB+AHOf4iK7lP9uV0lFnJvsWSS9LTdjKdZpfBOzmMNzP0jPCi51rEeUW7lX29SNTpnUIvMIaRkwJxtgvHJ/ZEO/bSU1IrA7C3yd/1qRvAPbW5awJf64bW'
        b'bw5kNT3F22Tv+SLqe9K1ExbzbmGeLdRs6PNu6c4Fy2t5A5Wjs+XNt7bsDmuVtdbkgnZZhSdxxVrzMolyj0oe1YV948lGHUG0nLAue50mAVCytsS8xG11SCMiwFWlSyuY'
        b'K6wuZ5eGJLqyoQVOe41XsrICszTZnHZWgVi1OKgWs8P5ZDOTu1Js0cwZOcCGrUvctD6QSuIpy9U6vK0CWDkuE2XC3ROIzq6P6kL3NErjD9nJjbxCuhlOdpGdLOhAYdLs'
        b'bJ+nZglpyp+dLSvR4fM52ucrHI411ueD0Iyq8JokvM9NyehgfI6so/aR6fikz/7S/j7CN8jeOcCt9nJLyG31vHl4K2OPtcAdD5GboeQQvsFRbonwC2R/sRjP4AaPjzk1'
        b'7rnZdIdzDmnSz2Xb9M34fFk2OYMf6imcbTn5ZCsHBOqUbjneN4ycKeMR2YvvhhbLV7Hd/khDf3+7TZ2vwuJ5SXNDLCpUvFaJT5HT+Ir11y/NlDvt8M7ECYVJb/1H0Lrp'
        b'oZk/qX/dINtXMbh83eF1x1ND3gg+8uObIV/+NPWloMGN/Zp+8rMvZTh31dprS363Z/DdKa4g9a9PPPtenbxXdtEPbpf95PJLi99vfP+zgdMSL+O7b+kev7zhX0fXoh8f'
        b'7nfunZ9Vn6hdwS14Q7vvRLQuiBkPVgIv3wA02as+h9Tyk/F1cnj0RMbNJ+KmjJAEesKAkkORZuKXBB4Nwjfl5GomMH26JpUpz/ibRfDuJAV+QdzNegEfs+b5GQlCI2Rk'
        b'I9nQe3wdU7/J6Tm9QvIcuK0TTR6oEjfb28hlctsvYAlPboGswOH74vtb5GsTk53kXkeTSjjexWSJqFpy1M+yUEE2cXjnhDTRctJQgS+2WxYAVagYgjeT45JbX4/cVSjd'
        b'bKcS3pOVQ9qJfC816OYioQ+VyL2YU3agvgG1FHrbwIipj/x1R/tlfo+1M4DZkGyhDCDaywDWoW+jn8gCAhrRUxVcbgBS1g3hb/MR/lFM32qndN0pGt9N+5XTIyfdtOGU'
        b'rw2TuyRwM+fM7Giz76I11EmoxmG2eJROa1WtWfAEAWl2Oxwg2mdVyqWWUhN2qJfyzRBZU3vcJNQYIjnOhFpCJUYlb1IAo1IAo5IzRqVgjEq+RuHHqA52y6jEOFGi9MZo'
        b'vr/a8uSNItoXkeJ73/W57D/Z5s96Lr7FXoFRo2UmqrAla2eaaql2ZJLuVSwC3tUl06LbUcBHSosmjEsdxTai6CaRQFVQUJyeCN434JO0WTZTlXZZtVna5oIO0z63P+Ht'
        b'1JPA19pdXYBxmKEjtc5J2vSOYrFR6s5TuF5n7Sy40J2BmKH6AmmT2B6wvFryAuV6pEkiwHOyobREYmJcWhRoT3vIzTxyMxcNJ6c05FA6PsJCO2jJDXwxLzkpIRcIq//7'
        b'vqqzc+fES+EPQJompzPw6QGh5Jwbi0dLfqDMRjsRSv1obE1u0jPpyD2Wthuf6gVvP8AvdBTSqYSelFtQ6i+gN5cGkUe1yxg7x+vJEQyQ2TPMfp1DGWUiZZ/+myPZ+lxy'
        b'LTo/OScpQYlIsy50CWnFF9w0vhP0tQVYtv9mCvQode4cCj0eCDhI4XpdUq4CmNbZIHh29xSdjHH0OHyQ3GKwZUiOWyOncfjiEHKbxc0C3n55ZOKMDPH9AupSdZBfhR+N'
        b'd1P2NJVsS07MLaDjWDkVRpJDvUbKyGFyieyz1tx+jXPSUyY71n004O37YSQ1VF5cYmjm0jY1vhnx+Xu/bNk5o5bHvTJ0BwaUZB/eXOL8geyPdbuDv/7ba9t6fxh/Pvb5'
        b'WTH/cfHCwd8PL3vrm7r6yc8tfX/DB22Nv71/6NjvNv6mJMwetSlhjXXr7BVBYz9M3yRf8NnxBYO+3PQL2XMnYya/ufuTd+a+WPPP6ymf/ED23l/C9x5KzAgeATyb0nBZ'
        b'LL6Shx+5GU/jK7hR+PRkF3WcIPcyyfGQlbM6MGwvt8Z38QnRU2s7ORZFmqjfvj/jh35vCmGMcSY+vyIPWOPunIIEEKV4pKYHONeTjblMkVoLos+hjmpU02zKtcPJI8Z2'
        b'EwaSa1K8NLwL36fe//gEfsA2UjRx0YlleBfZUsSOjiht/BCywcq2SJLwXSXzXy1iwTeKlQV6mJIUGdlbS/az7YwYywTcPBu/GGjynzRVcuEM/X9koA+hrFAiHoyf69v5'
        b'+RglO6eo9nHzYOk3lJ1a4UVLfC9/pirVJPF0pcij5tJkHk3mBzL2oO/mVSsXa5rvY/vzfHyvHJKzHXj/L4f48/6umtlTxU/tfaEbrvumj+sOpuwCiCljHj5uE2BllzNP'
        b'IR5+uSxdjIMe5HJQSd9B6QN1/xPslQYD20lwUI2P7Th4ZBXWyiduanhUXpMwNeMwbdgTFqCvMgHJT3IqZ29J7RMnLPL/0QbQk9DNQU/09aXz9DxcqOVyPhoQCnEDx/JM'
        b'dOxxymuCB4bwVLzkg7noGP87UZx2EL1igfd64YtkrzO/UBTMORS8kh+ObwLdbiXnAjhZsPTX+a8Onk4CXy4XZOUKKypXCvJyFfyqBUV5kKAsDxZU5SGtilZ1a0QrZ5G1'
        b'RgjqFl4oApknpDHCImNOx9SHJ9QcJoQIocyjSdPCl2sgH87yESwfDvlIlo9i+YhWjTlSjCkDshR1tQlvjLSohV5CNPVKghqjWjUAN0Lo3cIcpNlzkRbq59RHeqIX1Ek9'
        b'nKgbdDQ8Qz2e4oR+G9XlvaFtnNBfGADXMcJAYdBGVN6HeTCh8lhhiDAU/vaV3hgmDIen4oQRwkgo7ce8klB5fyFBSIS/AxqVUJNeSIJnBjYiuE4WUuB6kJAqjIL7WlaW'
        b'JoyGssHCGGEslA2Rah4njIfSocIEYSKUDpNKJwmToXS4lJsiTIXcCCk3TXgGciOl3HQhHXLxDMIMYSZc69h1hpAJ1wnsOkuYBdeJjUFwnS3kwLW+UQ3XuUIeXCcJxZIR'
        b'RSYUCIUbg8qTBTmT9Gd7lOk1zLXqQoD4Q9e1eEP0rhKDioJkRwPEVTlMVKQT5bHKFT7Hnw7uNYG+Wg6ooMbsslZqqR+gSTReVopiJRRQSRHqFK0ithVae60o+3Ulm+l4'
        b'j9Kw1GRzmz1BBm8rPLLMOSWFj6dUu1x1k1JSli1blmyurEg2ux32OhP8SXG6TC5nCs1bloM83H6VJJisthXJy2tsOqVHNjO/2CPLnpPlkeVklHhkucXPemR5JfM8sjmz'
        b'5mcBZIUIWO2F67NdBWxY1FPCyjuDKXFdzTdx9XwDJ3CLZc6B9fxxrg05E1y8wNfzMYiGiG3i6wGRV3OCrJ5brHSU13PUhRDe4o7LaGBZQdkXnotF0Wg8Ws3VquG+il41'
        b'IfpePTLIoVZFG5Byg1JQM/Up6GNDV6pFR+8zaY7bnc86vvAkgZ2NgqgumMQ6WEk3RihxuCYx/67SoqQxaaPG+6OQAFpGjoVK71pnnbnSarGaBX2XMr7VRTUC4G1ePzMG'
        b'2avmiegKSofDWuF+gpYwid6eZBTMFhOwDR8KGUHtsFZW09qt4jgBIkpwALk69+1zOuePe1tr2a5Re29GDneO9HDJHi71c8oPPv83/HssS05NLdSpPBEdwdKNDpOtrtrk'
        b'CZ5Le5LpcNgdHoWzzmZ1OQTKuRTuOlgiDjNq3+KopYkddXtymzHVX/lEhWA5sIpoyVah5al8szJcRICe789XixuAtFndSAh/8+3OewH4NueTOqIMm7gVdWatESakEni4'
        b'LTlD/Gs0JgOMZ1APXMVFm4U4Qk9u1t99gks/5iLQNRoGAOO9wCIkYHT1LuJDfCKTjE2FR21yGpgPpkdtXl5nrwVFtZuG/K+vIZVs095dUwHKLgyENALaOpupku6Mmlxa'
        b'm9nkdGnTdMnaOU4zQ/EKt9XmSrLWwog5YBwFo5FiqElY5IYH6QOBtQTuqQYe+eFYCARfDGjfkR+OGdmfvL9apZN//MeuCMycOipiicTFvLyy2lRbZdY6WFGFie4G2MVt'
        b'VHjKpK1z2Jda6RZpxQpa2KkyuslaZwYeMROG0wEdmmGqXczs4k6XHQRARgpqe7TspSXvbZKBNclIx9TNlrlIVCj18dnDYUypS2oXW2s0IrfZVW1v51d6rdMK9FOqhr5G'
        b'd7n9HVuf1Eepokk0pvcko8RKu9ij69akUWG303CrWou/7cTNpkLoMA1dEsRlZgcsyqXAB00VdLv+CVYUnxhJkUiOOhpENIXuJLgmF+V5ifjsgCTQ9anKmjePWhjI9my4'
        b'LJoTn6vPSVKimig1eUSuKcWTdC/hTeQAbibXyO3Z8blJNCDujsRCfJucKEkiZ3g0Zla/EEVVInnIgnIOHxXkTC7IJXuXKaOU5AwKx/tlyWSXXoR+ZzU+429xiC9MSshL'
        b'KoFqTTNZxXkKkEbV+P5ycoSZE+Ky8DZnPFOuFfgg3oIUeAdHriVHslDgM3EbPlOKW0jrHHJtEWkhe+dQi0MRR26RFnwuSwxNdctY6kxOnViQq0AyfIDD6/D9SjfVfvuR'
        b'O6Od2Rl4o2jXycNX5CgS2osvkaOrxa39Tbh1tpMOC8A1I8VqjlzGzell1n0PVyqc78ETJ/rqe7dMLtmQHrFx1Tc/DE/ImvvPPh9FH4g8GBf77LBS896M49yrNl65atvB'
        b'1/6ynH/717af/eeOq6vmpvaNXDn79x+PjrWOGfPXS1saXtlQNezFkobpo2edzJphuP8V/jy3z4OM38++GPFp34X6z/DP2+YdDZ36xf63F95+8/bp8Fv1ayLfm/x87Jdf'
        b'PxzQ/wXLrfc+XjRxx/6E2V+djs2Z+tr7KVfLo/7nlG3ws4OyZkz4Ub9hE1Z9efRR2zd/+MkU+8o///PkxB8OeqF815Bvi4vupi9//bP+9ocFVw+s+RdXvDz95dH/q4sU'
        b'j9VdxG0yOld98fo80qxC8iSOospD5k9Q3AvfT0wiW8mWlGzSInMmoNAsmbI8jpkzXPgWacDNKfgkaYBnOCRP4fBNvA/fZfaUAnwhKDG3bm1BPtwZzOGjeNcwlxgCa3hV'
        b'Xk5BQoFqOG5BSjmvTnUz60YRvk5OQCPIzdWAp/BWHw6fqI1lRhh8itzVdtwz4dFgclHaMyH7RZ/VbfgR2ZiYrEvIxtcljELh5IZsxUIppvM4ctacl0PWq30BFMhFcp01'
        b'wF0cT6vfTG6y1+SFHL5GzoaIEVweZtmpQ2OOPhlvSaELC163DtRq5eROmdbFPKkPsKhQ+HIQvuRdbLglRVxtCeSBgmyYRC6yZuJN+WRdHnucWvS2cAYbChGYrQjvZKNE'
        b'dg/Q5xUlcWgcPswv5dLxVvwym7E6wOy2PD1u0Pifk8SPRonjtAvfGZVXgG8l5eUVJJMt+jxvMIMEvF2Br5IDs0VnkI2zySnSXJibgC/rlUieweGX8bm538FF8fscNewt'
        b'EkRDIA9gliBq7pQsQWuRJpgFZKXyEfXcjGbemfRIYgSzB2mkyJpiaRQn7gSt7C8JOl0C8bmnDEPo+/lkcuKrTIJogOTfHSxADQHnD7ttDNRFBceufVlY5BMWFAtkAs4v'
        b'8gnPvuvwZH8WC0gEP+tKIpgpsjTptIso+FFxBTgM5VI+2UsSDKiU4JSE+c4MSNoC6CBZdJAjupYbOrOzss4yionywQC27eWidsre6f7HCiqAdG6ZqbJa3EOvMdfYHSvY'
        b'do3F7RA5sZN9y+PpLL2jrhQopfp5ErpMjipQTLxPdrvhUevb8RCxwrvh4RWdqMBjdvpr9N1w/q6Pd6tFD6E9s8WgZzsXW2zTQnpJkUcr+9O4p/Hv1i6bUhwthSNdEnIH'
        b'LQfqcSRs+pIDQ98oZ1y0Ys5zzjB8xxzGI47GBr+MW/AdNw1lnEkOkN15HaQI78aKl7GW0Z34ecDh6U6JuKkfQ9bRfX0gQCsHRkyqI0etpf8+qnCegyoNr20saJmswakR'
        b'GVU/1wyunxQdueTSX8vmbqyrmj0pzLpvc6/i5fZXuQmxd6yf/Wrbr6o39ooOjzn7i5hVw99p6zN5yOh3IvZsqzjTVPd2S0tr3KZZB9IuR29fU18zYFW/Edb3yv/jzmR8'
        b'0PPBrdnFn99xrq772eGvE6I//uXXD75cWFqyY9MfoyfG7Fce2bn6yjezXnzpq9//+dgPZZpfNB/55rfp2ROvRvzF8XHkf/82ZPnmCS8b++o0osd8M74ytX1DnhzFrXwS'
        b'3p/DmOE0fCItD6+L8JMxwufKbHjLSJE17MM78Fm/4fPyBfJSH4k1AA9i/GkSbsTU/6J5MT7njf4zvVg8EHHOPTevoANhj46SSDverGduAxlh+DIz4Y9bJfG3h6SV7VDM'
        b'xpvw7UQphsUlfKlGjkLwDZ5cfAa/KG7dXyVngQE2k6aUJB6fHy7GCCIXyF7GNGbiPeSeyIAVY0Ml/nglSzqsweH9gQwSP8LrYN4Zi1TzLhag+CHelJPIuCc0P2A4eHID'
        b'byXn8RHOkKLGp55JZSD7g4x3OJFtiiiQcpGGXOMHFpNm1h0tudOL7pck4YYOXg5jzSKX3RKD9ySSe+ScvgCkUSnieDjeI3MoB3V16rynfEwlKQmMc6X5c65xIs9SiucM'
        b'uBiJO9EgGRq2uyH6K2i4lRqJQUhVBfqj2QOZVDcBM3jx2XbHhE2QxENdzph21rQOefwDHnWEHaBuU/LC1G3q8UvVbfilJrE4gXPxcC1r4GLgAYEPyHmDGj3mh1sfy4cn'
        b'pwEzYi3zhBpq7QZJHXZ6ZKYKJ1PXu1bNPREG34a1aF/M5b1nrnkYNn5lH6+5pMNzAUZA304xDa3cxL4B0MA7suo51hu0WOaYTnvlSKjnjtNeoDZuNVcb45IJXD3L0yct'
        b'MtE0CNdy+h0BxmH5wscjffyyxuqEJlRWM04zHAg9tTox5ZhewKyxAehlramzWSutLoM43E6rvZbNkieobEWdaGsSh0Q0LHkUjC171KKV1u54gnOuxlDnMAO7MhvY87N5'
        b'rxMkjaYFOKfh5Sxsw8re3iELeL7TpLMBo0gjUKsmDAK1ay7iLHyMaGmBrkeJNcXT7unFTkLj2g1h4px2+poCPZgDoB0Gw0Je+pYC8jd8ife6xsIo1iAvHkqNqaaNUVEs'
        b'g2HvogUdsUploEfnDexgkBe8xgee3fLJYvSv3As9lq2B44APAtfGr2YDUs8tRl5c4KYAdPr1JHECeRH69i6aoDQYbC6DoYKXmDaCOVoZ5msDvfedmsB554SfMvW7tMFs'
        b'MFie1AZzhzb4sCLZfxkN8S6QxbxdK7YGCARfKhILduU9sNE+L36tegI6Q+PMSwyGRbxkVhTROKCB9H5AA32mwVA2SBR4qNcs6PVr7240aqHHdX440Q6qtuNYPG0+5D6U'
        b'mPYdpqMKpt35hOmo+q4ooWBWQYoS074LSoBSYlj2pDaYO6xLn2s6HXEvmWg3SvtR9i6pALWSGQyruqQC4j1fjwPE3GFd9rgP3dhBjGLzDbxvAhKBkPo677XQt49AbZeN'
        b'AxJhEgSDYY2P38BIBPuTCXa70/rwQz/avDau3RTe9pSxp1SRVdrQNVUMBNiD8YjtejySvud4ON0VBsPmJ44Hu931eGhY80LaR8TS8xFh1TZ3PSKBIGXIj0RRKdtHojQu'
        b'xMgR5KM7jgmbHJlHU2h35QBjNtPjQ2ahu7F5wtkYg6HGDQi73Z9gyQOHiD3QI5SRTnWd7cEAsUpbux6gQIABKDPFf4C0nZGnn2/I+nUYMikeD0WllB6gUtfDFWIwuBxu'
        b's2BdajDs573HiRiND+Zh0KJ8nfA99v36EefrR1xX/WCiA5/y/TsSCgzUZrc7WBOPddGTXr6etD/3/boS4+tKTFddYeyfG/69e6Ji8YIMhrNddMIPh+3+VEju3/5iFCgW'
        b'tLffRXtAt9Shre3XC/nV/GqZ1A9ZA+2RTLyyePtEKZZHCWMGYEGDYB27Gtg7eXvvPIpl1XabmXoL15istYL5SbJysMEg1mkwXOW94dJFAYOnZ79XRvr6632ua/mYiqMi'
        b'2wthU8NISnVHaedJHJCFWqsyGF7sUg5lt54GNvj7ga2zOw2G+12CZbe6BhvNwLpEkJwfW2G7rlsC56Ub6KD0GQwPu4TObvVIxNjYAxFDRXfRQW56tUtY7FaPYFX1AFYQ'
        b'W+AmqPI1P2gR/quf3nS4UQdLb8D6pytmMXJEuECjZo4onCAT5JRv9YGmrKYrheqofBPfJq4dacWwAVEUfk4rfTyEbUJba6u0dfZl4jb2qFTRkcNdV2enEYEe86nJHm4U'
        b'rJ6V3mnzqJe4TbUu60qz/8LyqKCmKqsLdHXz8jqvYvpEUwiMAgNuMLzRTkbULIaoxn80pIfEcaVDokvp4InoeE6qz2mzu2hsseU0rwm0nEPeYjFXuqxLxXjSQI5tJqfL'
        b'INqIPXKD22Fz0LC3jm00afdp9OGpR+0zRoQwo6y4/ctM+kwtd2ylCaM8u2nSSpN9NDlAExpG2nGIJkdo8gJNjtGECjeOEzQ5RZPTNKH83EFtnY4LNLlEExrS1HGDJjdp'
        b'cosmt2lyhyZ3afLIO8a6qP8/PpIdvFQqIHmLkwKiqlVyTs7LOb8foJHRvTu5Rcp4ThsPv4NDVZqQUJlappar5Rql+DdUFqpQs19aolGznyAolX5EN/Ib+IW1TrKNtKSQ'
        b'FtnsRA6pY3l3HN4d4C0pl/46P+jgLekNlGqRs5CtahbtjYVspTHfpGhvLDyrEMTyKhb9TcGiv6mkaG+hLB/G8kEs+puCRX9TSdHeIlg+kuVDWPQ3BYv+ppKivUWzfG+W'
        b'D2PR3xQs+puK+V4qhFiW78vyNMJbHMv3Y/kIyPdn+QEsTyO6DWT5QSxPI7ppWX4wy/diEd8ULOIbzUeziG8KFvGN5ntDfgTLj2T5GMjHs7yO5fuw+G4KFt+N5mMhr2f5'
        b'JJbvC/lklk9h+TjIp7L8KJbvB/k0lh/N8v0hP4blx7L8AMiPY/nxLC/6aVKvS+qnSf0tUbmWeVqi8sHMxxKVDxGmM4Kb7gmnh23K2k+ofnyt42aW91Cn30NS6LkOj1EP'
        b'EOaOUmmqpWSwwiw52LmsbCvJ6zTCYp15Xe+o34i4Z2MO3F2S9rQC/USoduZ3nNZIia5JPC8k2CvdVK3w1RxQm93hrdDqEg184qveLaKZ6QVlGVINxif4BQZkciyS04tJ'
        b'W8HMkVCduLPnf9xXL4L09lXy+3Q5zHRAAuozOZmbKW0cc0VZCjWZbDatmwpYthWUzQScIw542cdeqc5IiQv14HBaOMrpHBGU2/VFTfziIEesl+O5mA22jVstE4C7GcRU'
        b'zlIFS5UsVbFUzdIglgaD3En/hrBcKEvDWKoRZJCGs+sIlkayNIqlvVgazdLeLI1haR+WxrK0L0vjWNqPpf1ZOoClA1k6CPi0zKAVOEgHs5Ihy6vr+eND21AGem4hSLvy'
        b'1Yp6+XFYoW3cTs4JlKZe3getltfGsVIlLXWMEFTA0YfXy6ltc7XcNQI4vLyBh+enuUYK6nq5aIV2xdPyekWDjENL/jgPNUEPF2maOPak0aXbAK1g6yio0PEilQnGigug'
        b'03LpfkEwppDl4Qwe3mB4rDAMdw53Ph7esZJqE3XUavf1Ek3BCZ7QEmD21hrJf1IpbnKK0UdlBqvgURjcZpeDBpQRj0d4wsWQ5L7DcY6plB1Np8kMmtDgN2K4lUImDASe'
        b'owRxT9zNhhrr3A4QZM0AggkCKrYr4DJ5lIYaZxUDvZieL1QYzOIfdtowzPsa+6YWvFRZTXdiWbxbk8vtBGnEYaYme5ONxkOqtdihxWxcrRZrJfOgBgFEpBm+26YaV3uH'
        b'PNEGm73SZAs8zE+jDFfT/WMntI+tWaiG/RWjD3v6GzoMOQivsB6lZxVwXeP0BEMjHS4n9QtnopRHBfNC58SjSffOjDgTKqfZJd1wOs0OWiG7oVOKPg3UfOFRLl5GPyHu'
        b'FxChFj09HAOb3Q+p6FfORL8I5rXRMZaWulPJE3548W8UMzbRfTJqAqZh5Vf26TAiPQ7sLJkm6efuuvEHjQKlR/SXje0IyOc4O6WMeUfULm4/zakXAyy47NKpV+rHKADh'
        b'tlpWADn2I5M99qOVmju1++b29jb38YjAUFvUmaDG7mo/bMvCjPY8rtD07uHG+uAGxtjqDJbGNe0x1BndQ+0X2Fv/CFsdwEpBRnsK9ynBtQb64Oq6CK71PUFX9yiA02Af'
        b'6F+ma8XQsk53hXQShPnIU3iSS48Uy6nbdjHhSayIbZhSWacOXqNyCgt300V0qGRtaXuZxWqmACXBAWqHB9odfny8wKlNkMYpQQ+XVhf7643DlcC2RxPEcFgJPQ6CVtj9'
        b'YMX7BmtM5wgoT8DP9Bnz0lMgyex5KLafdt+KRF8rpgQcx6ehRswVgQfzO7ZmZklmRkpG5oyynq+Z/+y+Ncm+1pSwmfdj35ILmNfrv4NvUrI2g0VEET2xbMtMK5zS2XRt'
        b'rbnKRFXvp7dRMqD8rPs2pvnamOBFcq93lV9zJR6tjS+dO6+8B+Mjwf5597DH+mCPZGTdbl9MJVvxdD0IvHV1dnrSCkQjt3gev8do8kH3gCf4AIeX+Y7O9AyANPO/6B7A'
        b'5ECqVQPr1FRl9kO+uuoVTupbpy1OzymEdW3r+YR6ugc9LXBQ20Ha7FWBELXxeSWZWT1fe7/sHnC6D7DoU1grJLnsSfCnnVVr4zN7BlHq6n91DzHDB3FAl3EetPEFPQMn'
        b'Tep/dw9ulg/cYNFpEsTBWnrARFocYrSN4jklxT0AKbGgX3UPMtcHMorRMyYbSydletytj7uHUdBOATpSKSpPUxcfeh0/o6goL6dwVlnm/J5QSKl/v+4edrEP9lcdYQfK'
        b'+MnaLKAIs8zQmlom/zl9CndXQd+BUM3LySqjodv12llzZ+q1xSU5BemFRWXpei3tQV7mszo9cxrKoqhSLdX5pNoyigpg1YjVZaUX5OQ/K16Xzpnhny0rSS8sTZ9ZllPE'
        b'ngUIzAiwzOqkXrN1NhONZCXGAOnpAH7S/QDO9Q3gED/yLapDIkKa2AI0OWEMe4owH3YP81kfzHEdJ03U2ZK16e2n2nIKs4pg+DMKZ1GaTpGox+34qPt2LPS1o08Z4+ei'
        b'mgiTJ1CssfdghUiU7dPuARnaqbkUl4UdkBTBmNuNPv66Rk9J3G+6B10RSOLaSRt1HtdSO1UH5kFf9+1uzJXAOQuZr10s2wVkPlx1/em1eHiW7mbAr7wBUgN9XsF88xT0'
        b'TQNLjyshVbVxnB9yPp5cIjpXU0uVT34Rhal2m1nXwlayTu2gZ3ocNCpAx9jNzNZAwxk4jKh9K34i6moDKIR+Uk2q1CyT3B4QaLCxzO+Oenyu7NdRmfR7p+tZonYzwets'
        b'WCbuAnQ9RXTXwS5r33rqpLj6fGq6PE4ZK82PQ0N3btsQ3amtEre/JPcturnkkVPDwxP86tSSWcJAPyMmeYmwoxhdNEV8sOs+R/s1RQy1K3j925gxy9sWBRu3Jzv52cy1'
        b'BsOyDm3pwnDAnivUDe1qB4oZNNiekUfTwTg10Yc17Qhj8OKKJyzQNqWUTFMqiUOzT+d6lJJZSiFapeTMKCWnNikWbsQTGmCQUkr2KDmzLWk6WJ5C/A1PSslipW43WInG'
        b'Ik2gQcoRwkmo46AfsHKwb0ExJOtJXDbHG5D8hFp76EaXOlTOR6X1IICGonNIje8YgqNzKu8+ZEdosFqmVrAvXJCN+PqQkKV4J9kSVheqyyXbEgvzk6kbOw37n1CtwNfw'
        b'PXenAIv0n5PuQbZvOQn8RsS+CygT5L7vAiqkayX7RqB4rRJUghqeVTfyFk78HmB5kBiWozyYBanlaXgOKA1hT4QLEXAdKkQKUfBEmNCLkbloT68OuJtvBTXaux8m91/N'
        b'9IwapaYG5l1h4Og+sYGvogEJZIKP28iZAO8J8n2PFy5r7ILJRj/YNqSj0ZFCM/hvcji9zhcxHNtI9Vai9tbRkUTR/dd1Mp+DlPQFuf5dwOn5+XdLjzSRzT57XpfQevyl'
        b'NkkaGMJ1C63RC62nrR/afX1NXdbnm2zqreD1ymh3BAmlS3nYkyum632rH7940jR0JtRPcZPwg9mJSzIC0+IHtSNHlKAykvwUjljVE4648+k9lLii/4kBn8sLtTR5fZqc'
        b'US4ALJ0BYD5Zi2XOMXDN/JfYNb2SL5Y5prgU4m4W5JXHVdSrj2v/HvnjJH85tYYGCahoj7owskMrRwY+LtjN4rF48awBCwPjPYXHSDzIMy3eRSl+oH04vRpBE+bsQecH'
        b'+FFdHejD3kMGIX4g2KNP8JySmQRhj0+4kQJyhbK/nTgrG154vmvcCZZwx+fM4z+TnfGGfvrwiN9c9u0KWGc5yudgGc3WiEiz61EGauAk0UZWGCCv+l6gRx8ovXwulJ72'
        b'oGLILn4Ji9HjdSWnn+nzOtTRj9V5OFenNQbJcW+rlWhlUletdtldJhuQILox5JwGF5Sq22vqptEPYjjdNU8QcBTsvWNPGxP2VKFO01G4afeFYYjSjiPtcgATCxI5afQd'
        b'yT7ZoJsIJ4PhodUyacCB5yrFD/+pZdQjhHp8uNnnEMht0haytAP/xdv6kh3kJtmiB1AZ5LIqvwifDGDEMdJf53YugBHDtLIf2RFFuYz6fFCPD/qNPyGYsln6NT9BQ9mq'
        b'EHlEU04/zKsAlhsl9AI2q2Ana9U0zlVjVGNfi0qIFnpDudKsYjGtxI/5qoRYei30FeKYZ4hK6Mfy/Vk+GPIDWH4gy4dAfhDLa1k+FPKDWX4Iy4dBfijLD2N5DeSHs/wI'
        b'lg8XW2SRCSOFeGhLhFllQeaIBrSdK4+Ae1HQep2QAHcioSeckCjo4TqKXScJyXDdS5goRfGikUTav4aogX5GsJ72aoxu7N0Y09inMdbSm0XNCiqPblW1xghpLZwwiUKB'
        b'0ZCx2Fk0klhv+uVAYRzcm8zgjBcmsPIYYTRbwVM8oRT/vL4KHq7YwxXpFB5+1gwPn5Pp4TNL4W+Zh5+Z7ZHNmFXokWXk5Xlks2YUe2Q5pXCVXQLJzOwsj6ywCK6K8+GR'
        b'kiJISjPpjfI8h5WRoFk5xTqNh58xy8Nn5DnSKDXjc6Du7BIPn5/j4QuLPHxxvocvgb+lmY5x7IGZ5fDAHGhMjm+5e2ObM5cE6ZMBYlAuuS+yufyJkc29xPwpkbjlhey8'
        b'rLAAvwQy57lRYXUusqUombQU0Jii7ZFEWQjP5Bx2LjFfn1MwOxuWQS492onPy9E0siEc3yKHcYM17MFBuZNuVJkuhP+hdqvx98Y3fxcfFW/KNtkstgq9aeErP3311s5R'
        b'7LsS1eNVIYfW62QsZEFEOXkYgs/rs71nIyPJS/g0yLz48nNkPTteuRxvVpDmhEFFZCuAprEEDvPL+WIxnuX9eWSP99vH0oePh9TTTx+XzfYeVnz61jDvpcW+I5LizwTq'
        b'I7gy2h+BAj8orGjfmnZ8TZOuPykhE58Y5nvMB/kGJUq0I75DkOLPuwGB+rtsQaVaml4KLvDLlGqGMcHSF7rFJSaG7mn/MqW6KQiwKAiwSM2wKIhhkXpNUFdYJEddfZyv'
        b'fyH7uJ4On8D78/Lpp0GkqIKAN0lJyTQOLQvgSqd3TvEyvDEbn5Mhsr0uhOzEL0S5J8PLObh1Zp43GiFFr6KkudLZ7FzSAvR3R968eLJlHr5JLqqBNMsRvoevhoTlkg3s'
        b'hPi6HCWNtxw7TGe05YyrQuyEONk5nHO68Lmw9iPim7PY422r1CgCWECp3WgbFjcZMbqfie+S4wHRZ/0Pi0cNSpqrQs+WqlaQUzrRI/A8PrssL6cgT09alpCTOg6FFPLk'
        b'zOJ4NwvF2kIu4oe4lWxPzKaHy8me0ampeKMxDw3Bt2X4ITm2gH1BMLYUNyYW0rPFLQVz/M6kxycnxZOmlIScAtIQzCG7Tg3M594ksWMHJxvzSHNOfkp8vRIp+/AaI2ll'
        b'qOimTCjKRPYm0tFO6l0Jt/FL/Dh82uqmW/q4YQJ+IVGcCX9Y5Mo0L7jZ8SyIenG82Ci8KVuGBuJNYfhu4TwxBM22OnLcqSTrl5IbcsThg4jswHci3OlsIbqBFPh9obEO'
        b'HiqLh8Fo1usL5ogx8Cc8J57Fb48+SU7JQqGSFrKbhcEhe58p9YaMJ1vxvjH5SUrUa5aMHMUHa93UoIG3usiV9mFLag/S3z5usymUaLyZx1t5hG/jRyFj8XnBTZEXn5iO'
        b'm7T4KtlDQ3+uRAX6aLcWrp4he/E5GOfry5aSW3jLssX4FLnhUqKwfjw+iNtS3FQmKTTPc5IbVnzONZd+HiA+NwkQAMghg1cS394oJcJ7yIvBMOjPs/jGZB1Zr0ykYwFj'
        b'05xCdpTGxwO5a0opnNP+cQA1fqRCeB0+H4SK8CP3EHhvDHkRPwghd8gtJ7m7BLcsc4TGW5eQOwj1GS3DG/FhM4s9hI/hQ/gIaaZfKklKziYHY/ILFSgK75XhK+SYnSF+'
        b'Xb2chmPKPjHTqH8clIrYFyMX4fuLx5IGp++TkQbykjX16yaZ0wbsyDhnzZySvJKG6RFHByrVxw5srP+TXfNR5JT0uS+NP5zcUnw6pvjKm6+/duHt7UNTV+34zSgHWvXm'
        b'2YTDqqlfvT817KdDtNd3ryhTb+xdL0sPK//N+zNO2BZNXntce31R5s4P4t99vOv69NO/fX3Eji96Hz9a/u3QX9wmD6u+mSjsyPjkb3/Zalszvuz8W8Fv1/2k5Qef9rmz'
        b'D5ed3XL6o4y1a/+4eP6MoG9Tzq74zVfv/R/23gMsqjP7H79TqEMXsaJjZ+hix66gdJRiVzqIImUGUKwIIl2RoqICIooFVKSIIEo8J9mNiUk2m2yK0dRNT4wpm2La/33f'
        b'e2doA5rs7vf5Pf9nQxwuc+99eznnvOd8Pl7nBj8aurGt1PI1B4fpY7ImhA7Nf/WF31a9VVv0y5C0Tzbs2FY75i3l6PnvuLwz66PktszgNYMjf5gUuOr85hdXvTVudI2r'
        b'jYNxttsXR1xSjlZdmVQvr7oSn3j0oOUUWYD79durnGeMb9l64PsXp7V8PsWh+EB5VUbaD/dvfbRaHHEwYcoBX+uvfTPSqraN+3ZhzdDpM+/+9NOWO9eHj1ZNjPxl8qyC'
        b'j8cPc0qEbZ55X+d1vui39dfohx/9412H1f+cuLXsl5w7JtvWXvloT3q5Im/Sexd/FynaDqzk3lGMY9vZWnfIV++GS8gQFDZEshmKVjDwgyAs20NmFONfcl/gQbERLovx'
        b'DJZsS6bDGC9h+VyshkrtTDcVbMt1w048D/lbd0GOibGhEltUeDXZWJezTJIEBozguSEr4RLsJesfNFB4H4rtgyfwOsP2gZb5PpjvA2VQpSZmoAxORa6sBnO3DGdcmwUK'
        b'MjFvYAEr4iUx1lhAOQ9+dHQ1XIZ8U2yBC6l4NRFbUkjesiHijbZ4ioFL4BUsmsUwLMyDBFqJYChLpiMds+AsZMF+PGXXh0kTCrcn0xCUcVCDDd5h3pTaQZwmmmM5grXc'
        b'VnMq0pBFJQtLyIpBCi6dJYIr1mRBoVNhGBFjrnonRvLUUxtETtaQnkxDirF52lJVqlFSCraaQh4UmOobG2KDaSp2km2gcCte3ZpEyu8r1SX7Uo2SB+E4aABH7Ryw0Gfy'
        b'HNwr4nRXi7BeH3NZ7SZiHlln8iW2HnCRSB67REtISlWMcmMiZFlAvj+04TWyotV7+ALZ/hwptPlwaJFuhUPJPLFGyeYpjNeCchPlz07zITLPAjEeHk+6kd5fiLV6KSI1'
        b'eSdZEOhqYOUjNfZ35ItXG2hNIbHIMCPbXrEOpxsqHosFC1gzGWF2GLkpbAEnnH11OJm/GMuWTUym6Mq+fpArUGb6082ZJI+l2E42TV1uNJ6RYtMC2Mf3895kLKWPQh2e'
        b'6EkYtnklD+RxFK7rkrxoQ0EFdpCG8hQPgVqs5ME6SqBiK01gKZ4i2fgRtYuSs4q44XhCmhQAl/nGOIHterTRjk3u2lVMAiW+RiZsPEbCabhKiT4ciGihgE5vCRmPeWI8'
        b'uw1L2FB3GhJEbnvZk3FR5ElkBU5/pjjcRspqOwRvQhO7S+5AjsB4agylng5iztZGB/d6QDvrOqylVKPkUT97yHVii/vEkU6k3Udjqw55DnPY1INsqLdgpaHyBZZNYyAs'
        b'FnBJgvkOM5OpNEVmbysUkwmS2kMoJ81+0CkhuKdh2I5sNIXjDKEqDjuTqSSzKyFeeDNc2etdOI85PgpdzofTg0ZDPMlYZ0mhO7GtP9rZWZjFm5951lmo9eR53vLJZnnI'
        b'dxs/TED9li7RgyVkaTkK5dqF7v88mSozFzDhPb6v8D7XUKRP+VPFUtFQimdKfluJhoqNRFJe96c+m2IzBpc9nCJ0iS1YnJ2R2FBChG+xbjcPUXpKptvtL2YgHtxLKOct'
        b'w7xeYChEKaldiKXUhqakK5iS8qDelUWEJWu8gXVVERujtkT1xlPRezKAM3+RkKhyOf1gibCMAuifzESzTNS9vVr7UTme70HJqr12T3gmT32TWZ0GAlnV2L57ZvXERm/h'
        b'+D9wYCP1I83xsA3jLFFHPfDlkwtQJ70YX5/MCVaAwpeFCM5LIQPy4PyqKYi9NoenWFVX2f4Q1abQDPSweIDcqQbH5z4qiHk6UT+nP0U4u0/dwxEpyQnR0QPkKdHkyVhO'
        b'yfMO5AU59b3v8rii5WDeyn+m0o/xStDVFMCWeSXERgtuCFuo2wdp8ah4GjwS+acawCik2xweoBAGmkIwnyjqDxFDgd80DoN/gm73MfjFRposJ/WPX9wzYyFftphqQP7o'
        b'DqEBhOetBhwNZ9kl2q67k2NWAxGzGnC7RavU4d7drAZqy3VvEDjt5K32LLdo0RNSt1IgwRSRFiBB+l8PcqCenhUquWpjQkpcJGNxjVIyAHF5WEwY9cfQmpaGYWlxXFQY'
        b'9UySu7E4FNqJAgIuc+cTsMAFv55Y7Qi6Akx4aGiQMiUqNJTnmI2S225OiE9OiKC8s7byuNhwZRhJnPpuqbF2+2X+S+4zmykavnDIzyMN8j5had1crR6Plx4auiQsTkVK'
        b'2BfjjwVQcd3+E/XpYolf7KDZZ3VUjCCu7uPPQ58N149+9w6RrfJEzomte6cqRExdmWNMFREnP3O40FeQgH3D1YcvvY57pNExUTysGSO23NPrZ9T28T12FFVEXAhr2q7T'
        b'DJpAf1ywIjWSZhdcGcXIN5MKB9i9ts107hujbhsns6sS6WwvnJT1lODwkF2XuERk/EoidB2GJvJsrj/Vl+AqlngzNFVswFZjZ6IlZP6HiGT7zEz17OxjFaYIp1FYadBb'
        b'JKRmllwfWyImXwjCi9DBm4/ol/4+jBGqDnJls4h+dCT2ctUcHRU1cF2vXvV5qKPFZ6F3wm2sbMN8mCn4i9BPQuOjvwjNi/EKI2OC6C6HZfqRSy32kJ5g+tYaPARXtEuk'
        b'24lGfKC7RBo+mic/KlwBByjubgCnjfwIi6CWaRR4KQI6tUmtUA6XsTNG+UQWYzL8VMLws9I2/MawY8fHD0GSiDq/Lqj+Aeldux5jozKUjMrh/Y7KT7pbkFMWkyfcZkcN'
        b'NCSHjdI2IO386IC8MsJ4DpyCXIWY2Rml2IqXvEfAKTZcpaYiOLsSO3gb4TGifh/zxjOj2JvSKSKSYu3sWHz2vg6jar1tYb45xiPCh4yHTe+di9oYszEmLsYrwi/ML0z0'
        b'zbDNQzcNDVz1sbOOc+GUxKsc94yHwS4Xmfpss7tFvd/uMdA0dv99ZGVkaCbdbqW9j9S59d8X3fbbMNIJpv12wrdm3WXqfvL7D3CZ8+6Sj53gZF0ebv93HRU14zhesf6c'
        b'zMU74RujjaLfjbt1UMRZmojfffUjsjZTQjgHrI7TroX20kGtV6m10GFpfTqql49F/4u2TZ9DDuZs0c8a3R9fN81jTL+98Z7JQIcqPZ07/qxoovUAru8OKfULit3mVytV'
        b'0a8n3HH3DjNii+GCJqmNSPHtx11iXV+ngypuoIa066O68Z4kT77b0fTH99uIbxsNpCb28uX8d1qxz4bVV5Qk4/lkQ5JYRe1NejX/sgujjPbrnmouMvytupw/bBxvJTV1'
        b'GU32FmrkszeXYb49Nd6YpkoXiKDFF0qT6akCZRWAth7DHS9BRn9DXj3gsSiQmUT9ICeE4b9uglpfB11OH6+L4RBmWPfTg8YDTgXHvso377/6xD1I05/Ubw++NWAPdvnK'
        b'cj1OGEeqWz+cYyeM9PDeiGkH6uN7cbY5k0p6HOJn62QPYyePw7NHZI+MHqk5fZQNePrYYzGjDl2WfTrf3o8dxiVBDjTwZ2KUN54/FYMcrOaPxZjBqnSCjkyJLdhimoSn'
        b'sZyabenhjhmcFmM7HIJMnpe6lSSQqyK3VniQvvSHevUZDx7BSu3nPLh/mwxa4DJkKXTZkQoUrIA6FT2i4bBoQRr5e4uM3Ziqb4JNKbrk6yooNaAY+DUh7ExP1x3TZXiV'
        b'HsG0zIZGDqpnYhlPF1FNxMTLqmTSm5gj8+ZgP3TMZonh4Y2QLaNtgZc3OlFQ/xJv/pXTSMadikIlYvGOXRzkeWMeOwDS0dNztKCw2/JQIzflRo7frVvW+dFTL5pQDZ6F'
        b'Qg4O78DjjD4Dz0vhpromeAIbSF3wOOSkUOz3bclCS/U6BMOGZCVegLPYHOhhh3l4kD8NK4KjBrt2T2XpklRubIHCoVOwaIqzlBNhFYfpkO2fQl2ByLsNW3ocxQrAK6vw'
        b'lN3yZSuxbIpXoB4XjEd1SX/W4b4UOoUgHQpS6UHbZC5JOZme+PGHfRVQBbVIPcOcuEUpTsOgNu7H33///f0AnfATEjOOWxAa5zhrDMf4WaHSN8ZbyIweYHsw/u9CJ69g'
        b'G8wlpQiEOqyxUeDBlR6evlQM9WUiUgCtn2688Xo8j9cZkfgiqCACfD7md3+QjijMHU9Kk+vkL7RV91NmOpTq4LoRNtrgwRTqr60/ZpgxWW4OGUO6s74OpgdjpS6R1Y6t'
        b'CjJeYjFcf04AXIcbRIm47B6zzSB6SJIhduhu1Yc8A38jaMBMPO2MN3YoRmPObEc8pgtHFiugad5ULB9KBgtplZQgWufrUG9KrdN7jbnJ+hJoCDYmonDjGizThVzMhjJb'
        b'2Ic38CAcCBoRu5tyro+AG5vGjoBWKIAsuBq9A/dJJtuQUhSOxitug3xdoYitHGzEvSwasfCv3EYpZxZqPcIvmGPnt5gFmYx9tA/LrOZIVAzF3blmL2GrLGI6tLE0I3Z7'
        b'2DhwchEXGmo4OdWXS/EnXy7Hdqym1Sg34ORG5CIGr67YsBmKoZ7eEU2GDDwzewrpk5JQaMF6PBY8CWvWkGKnDw6CjCjIicGTeE1vI3SYpQ0ay8561y6P7lZIx1maYno4'
        b'eOlYDKYOMHBeQf4nUwzrDMja0egWpBCl0BVXtNmd9j/ZN/CAJxzEffZkxSA9PERf6jzBjW+GvQl40/sJKHN9XF0Fxtw8hVEsNE9k00RvOcU47zpPxmv22o6U1efJSSGk'
        b'ZGx1OqMbQ0V+0aY5nBgOiBZvg/YUL1qebLLfXbDzIC1W4MtPACc4ge1eng4BvP9Gb+eE5R5EFUykS8CyAIcVYi4tyDSN5JadEkCSG6ur4o/xPZdvIIsH788haJIePv6s'
        b'so7L9VPx6nIPL18/ewe/YJ5ouJv/AFuisSDAHM5A5gTW+7d3SVbYSuhVqNGOSbZk00thJC94Exu92QmPt4Rsvg1W2CqGnIV4KIWi/5HJcMYg0F/hy4PRB6/U4p3CkfF+'
        b'AdJJtxZjwTo5UWevwWmPMdC5Eys8xkyBy1IOG3GvBZS76KVQXTIWbjqRlbPJ1EAfG02xiazVl5OTUogQrZL4E23yCFtf50EjnvG0CqTLloQsdfUc1kOBWwoVhYKgKNJb'
        b'4cAUaz9SLBsiZNw06en3v16uDxlKaGbVhIaNcD0QCoOwkHIL6dgOCRXBMSyAvUwpU5BdqESWaiJKI5uICA+TBSWabCTskCwHj2I6njcjJW5WYZMeJ8aLIgeiZ+9XmLOB'
        b'IcLTupjvI+JEM/UtObLOHMSLbHt1IjlUevv4bQpXH67J1ojx0tjdrH6QH6aAFmPyZrejYNdl/N5ygmiJl73pgSoU6bAzVcgmWyDbA0q8yVJ4dRPvs6DDSUeJ4JQbtLEs'
        b'HUfDfjp6lidSNxC4IOWMzCSD8fhSPlCiYCN2krGvYJo+hegnvX+FP+vU4SZCuk70Zixh3iSmWAoXNWs65X8mu0abGMrwOhaxrAzhAhy3s3Ega90VNnl0OKMYiWm8Kds/'
        b'DBZJrfGGwGVMSQqWylnpjXbjOcx38MODPmTfFXG668WDySrQwLph9QwvuEiaL58d3Eqni+D8Kuhgt+KhWUqyvubN01WTOtfMwROssYL24HWib+eqqawpj/VWLGS+KRuV'
        b'WEzKaLvem5aQDGI6v3W4MVCiYwB7MZd5E020oUsBr7lDrhNrn8F4Sd1EQvP4wV49Mh/3Dmb1CCKvnKEH6QqyOBnMMsJMMZwZCzdjrZQFUhUFQD619BP3wLb4txaY3V9f'
        b'ecrtzdfcn1tqP3rWobtl8+XueXLPYaeHn5OLbp0MchSNcctYzolsA6/J98hT5o1LPOQaUmSaWNZqN0txuiLt27eP339zwtnycxM8Awptda6XH3O6/fLYH/KHyLLX+U3Z'
        b'Ot72J8/ilV6RGz4qkf/eNDw/YO/v81XNf/d7YOmd+vlJc53Ypd4/2reckq98ZtFsy48eZid4z1678vtVy4Jur7N8J731zbfei/i+saE4Jd+10H59Xovs8o4vXzN/pvC0'
        b'o+v2e69smHD7pfvvD3l1x91diS+8W5pSD3URHyy/l3klwXb2i6JJO5/99fyFV5dYvX7vg6e3z3p24rujVq34ZmHZb7bvLfi57N6zP+0I2l7r4v3mDMOGdxIDHr0aMmHK'
        b'kUdnLv/qGu92f4ubwf7c6oQRjq9tObLwwaIfdDYsfutMzL3YyJfXnsx1n/3sg5Of/FL36wKH+6+9+0b1ZOtLZfe/trZdetVi3M/4dbiTqY/0l6Mf3C9/JW5PTV7dl8Zb'
        b'anzCdt3e8ebe3FufvHx7+Bu/GD63VPetTTHmpp/Nq5geYHjgZFqWwZKOkGG/Ln0w/IuPHHzfdT7Z1LLGvWlvVIFDzbvmH1SuPPTMGquIQ14HPhtT++1TRsaunesLPrn3'
        b'4Hv9DblpEUf3tf/kNyQ59m29SUcPh+i6Lpj7wq6Zvz69YfRXfjOX/PZWfdTM2W+nFXy9Z5XnqFMfmM+NjfzwcPXcz19Zt+VEuNupuCtL7+9dldZkNvdg0yB5sXVy0pej'
        b'7iTfu+PzT8tOgx13s79p+Yu1/3tJmSudy2a6H6v4tGh2+zNXft0w8buCyss7zpw/8XpA9raXttx/e+a3l+ufKti2apbueaep7y/xrH5rfx1uDvNbFfLZUz7rl37ltvnR'
        b'kCtHdH6uyFdM4N0I2uTuvLNDOfAOD2p3h8FYxvw9sDpOyZtNDzJHlblpjGGESGH7Y9jqQ2YEv/qUmfCH8DfhFDYKHjJY5NLdSUbizLsmNBIpoVrtZqbD6UNLIuwTpy63'
        b'YbdDyOZfTBbFKPceiyJWmDEHCwOHlWQFre25KsKxRN5jtXkkmbTUhQdOYgbvFcE78WzzZg4icC1oME8mshs7KJ+IeBRcmsF7wrrMt7N1VGAe2T8MVpPVrYZM2FEuvFtO'
        b'7lS6qdLtxN5mLFmU4IDYAa9hKXOTgOaZpPF4gRMOztNwvwyHE8zTAS+kEbksn7nSHcTcJf5doqsuN9pbipUpmMcqlwR1bnasDEA2dqK+QL14ynxoYWXfPcOHOe6Q6h8W'
        b'XHegY14yXaActuMNFRTqJxljY/RwFfWyU7vSdHOjwRZduIkZ0Mw633N2uF0PYy20LuYsPCVwcgQcZicIrngTyr3VRmJ/ttk07eLMMVsCBdF4lTX5BkhXASWVdyIigtMk'
        b'Il3ocab+ko1kh+pkD0yzwyw7f3srIgDkMb4zMsTwphhbOahnHR46D451FzCIFEk0/Bxv4CnvscSaCIAdE7ttFdAJx1kdhkZCTncH52mQK7h0QU08e3smNuNewQ8Gm1bz'
        b'bjBhQ5IpTaHbbjyi3QoHBcoeLh14yIUZuSdBCRmdZMZoPIiU+l0+RHjSI3k8eWoV1jv3dGxJwAskaY1jixJv8JRyl+EYFJEO96LUNBVEsebJ6tIlCVjqyjPYHIYOXyIs'
        b'k42nEM/xbSCLpzxxJ+Ek73HUgqfJrlvi1317G4G57OZU7MDD2EnkjO7CwHx/1vAexhuZIHnNrbssAE14gVEWYR5pi3M9pYE2WQ9hYAQZ4cxDp5GoPRWkmNSViGhO+9Xu'
        b'RFa4X2oBh7E2mVKxw9kJm7U3ONas6scMNAHOsiWHjIEbcNbbx1OE7amcOEBkC2ULWR298VSUt30XF95svCJOw0NKhdG/4wijGPlfBF794x9dJnjTXriTzNb1N/LRx9bl'
        b'Qk2y+owGxoxRD5lRUj0xD6imL0CrWZH79C61WVHgNgr+LSXXUoGk2IT/R1KiVxbkiqZhwUj5zKg7D0nBiMWEUbg2fXLHhP2mzkEmJG3qEmQopuG+/E8XqKyYpCBmv/kf'
        b'GtJLaWuMhLT44D2N9axXtbv7AvF+Oiw4axD9GMLcgKK2aVwIusU6ddn2Bv+f9Z7ak8hCE3ZFS8gIePhCDdK4E/FovORP235NjG8s6kEzOFAjKUQs1MtvgKNOetgpYgi6'
        b'jz/qVLMOvynW4hqwMDqZUgmGxcUxfNBuBL2kULG0NGFxPWBDeXipyEgePS9MHh+1tU+ivEuJTWjosi3JnvHRoaHy8LiEiM0KRwHiVe1skKKKik6Joyf+aQkp8q1hPL9h'
        b'ZCylJOxLHty9ELHx7MFoFh0vxFNGqfggSx7RT05xiuSxkaonZw+kQf2uck926E/GnyqWwqiSfKgDQJg8IkWVnLCFT1ZTNc/I0FAFhXzp10+CtI+6PehlbLw8dYYj5aRe'
        b'RJpxK23M5I1hyZrSdrliaE1RqBvDdmVeQ7zDA0mAIr32aCJ1uGqMMiElkQG+aU2RVD05NiIlLkzJu3QIFPI8VoFKbkMDxe1JE5BsGYRIWiL5Myo5wlHBOqEflw7aoMlR'
        b'6n4R+p05dMX3pokUej8ygQXLJlJUYG1p9uiAAWgWRZw2mkVDP6Zuzhu7h7eLM5s4XPMxgXw4zJvFGd9fOlTCkZ7hBUlE+rqpCTAgO3NDCg02dsKDcEIwFMr1JdQa2Z7k'
        b'jKXDR3kMmpC0Cy8HQBZcXAylaxd5JuMZOAd1WA0N+nP97K2JlFWNJ9zg+ujtcMHMGeuSmC1HMtGDK+KOjtILDfVSBEznWOzMyM1YxzTnQEqLe3Al5hhQmzzZ0PW4sZuk'
        b'WLdxKXu5JZFGM/xorrMg1H7u/NVcbP5vX0tVqeTOw8TYCc/dMM50tnR/7+fKwp+GyRdH7p0aJxps/IJDUWzR4vKp1eavpcWFJQwf317j/9epY2VZa76TtZu+VrT9lXOf'
        b'ts1+VPeLJPuXpx8+eOHDC/L964accD79suP8ff/47JVrM4x+aPPd9+m9Y9ufPvAvWV7bON3m50fvnzeiquOaQsaklY3biJyj8cwOClerKoMW86TCDVMXe/tvwya1S/0x'
        b'SGdCh/VaIsg8yVkrL3Hg3pFQhRk6TEALtsLzKmoudWBMwnh+AjUcmWORBBqc7VmxHIlYf7WHMiMOhZxUvMbx/vZ1TuN4b3Xmqu63A+vh9A5eiaqTEgky3wNbxGpv9eFy'
        b'JrSOp6cFXUSTYiLrZTvsWcEEQlfXlT3iD0biRV67wuu4nwljUiL+Z/YQUh3xpKtGSpXiGSalLthA9CYipeLJjT08sDVSqilUqc+/Hue1YUCD5tgUZdKIjTZpZA83k0oQ'
        b'VLIgEoaESh1U3uh1cK9JqCcdolXPrVuL/4ZVzy00ivxZQ7dQubYtNJ17x6J/5wFNGagrJtlZQsjWosEKUIeQ9ufEJ8mR9BtAqt4/f5Rq2T8Do+IFNM+eEOIpKn4/jWIr'
        b'Gll+3Rd5Lg7sBgve3yYUFR4boQqJiIslqfA0tmqcpGiKaxix0ZE94ehOPxezx/pDG++WqtAerswN0F7jB0jxb1VRrJgJykj6BVnetS6/Anp6v2VwXBLsE8qw0VIS4xLC'
        b'ItW1VzeI1kQpyKYG64zuDIIPrColNpnHMNcUSvum8NhSLV4cFGr/Z18N/tOvei77s68uXLXmT+fq5vbnX130Z19d5e7y51+dEirvR3R6gpen9uOJ6RnNU6jwgkxUpL3c'
        b'Vhj+tj3cOXv6mzInNO2SR39epEuUYQxKumsM/xGH0ZVUVuVXhdQpjs49ZgtzdOUhXPnpRDJMjQ37cy21KChYSxG6aK7pGsOXg59usZEDiFdSrhtNq0a8GsSzWO8fq0c9'
        b'E8wS5dH2XjOFyOPtZC87qZLR4/eTpnCdg3JjKBKOPLAzBZucnZ0xg9r1xJ4cVgZBBX+eX7obL9r5ORK5AA6LtiZ6x0Inu+EE6fZ2fl5i8n2GaAc0zdyOV1hGvlJDOz9P'
        b'+nyOiGzv1XPgOuYppHxWFVAxhB1OYSPUGOpwkuGiudCqZDdXRdqSWw3J2KoL6WRLxzLRGLyI9ezEw9xqvsqF7GqiBC4eiskr0MpEyR1rdqnwqqlyB1wmJcdakS3J4xR/'
        b'yJ6rD61YQjZmdszuBLkbeE+EHCmeULsPQP0CDgqkoYL/IFyRwkWhgJtW8uVbNZ7dktjPEIpnAy1C8Sz8WIrDw2exQuDxLUIhAvEmKwOWD9uuLneaC7QuggwFT94STETe'
        b'/eqmqIR6Pi88bsDaIiRwtpAZNMMBITc4wZeEVB1PylINVP5QIeUkBiInzIVr/DFqNpw3lRkrTZMMaIlF87Felx3jxIuwnp6xyUzwDB4QcRIjcu/CnJTV5N5WrIJmbyrM'
        b'BjLPWXpySwRcDk9B8U4iPhfgPuiAUjgRRP4oJaL3aSwmsnMpdFjoYBl0xIXrGGNZuC9kYcEc+SAiCVqYwjnMmxbrOPaCVPUd7b430oL/NtfvaWcznXfLk6Yf/yLBavx4'
        b'V1u/Ww5/T0x/2fCZZ7Pcr2QtFi1ysdaZkPVKkr6bu+8Lopk6g51uW11XTvntozT72crFxnaK+bdntVi637b6bWxRXllM7vvrTy95ddUHFdGrBr2Q8ujwhEFtt13jZzV0'
        b'/mOsb8NLkgSdiYdeaa55zc3LvSjU9fztXQcDf31xV7Xt8l3fT0mOVv2eFzms4njbB8d0j9f8bHLc+g3x96LjBz96oLf+/e+cLmT9vjCh7aXANV8Gvr54U9SHWb+M3rnL'
        b'Ock4KmRh3QfXq4/87YWvv/yb3Se3z209u+ZfCQ+u7736UcGon0R7VgemfWu6/+D6TkmMwpI3cLePxVoNkIAI6yIFm3zrBGaB2z4nhLfH4yHoVNvk52EzE5Ank14ps2Mx'
        b'b+zc1WQbZ2Qv0VsHnUxuj8HmBd5CHOwKuLoQrmE+k5ynb05iIfWQPlGHk8I+EWbi1TksSS/MIx2YT11gsCB8vRBtiu2YyVvrL0KtyM6PRsZ2k8pT59nyVk8sJMuBlwyv'
        b'YaE3FXb1MV8Me6FpPh+dW70yUSXDFhEnwnxuLnTiOTJ6TjKJPVJChnl+4jQKfJDNhSzCIsxzFt5SklFObumSWzkcnFqLh/DwRHZvHhlu5+g9mmQuJx5Phl4J5rKWXbEV'
        b'jgkhn+y0AtOFMM7l5rz6sC8QTqlSTcirUMuRNKvxuPUkdmsGFElVUAA5tDRFnPFabFZiGd+m0+PIOzrknbMc3liLJzZDFauACRwaTaY5WVlFcInoJhuwYrSEpbYVij1U'
        b'qUk0n6MctGE6FozAA+xWSBqWk1skGzhMViQopnb8VHZCAEehc2x3BUnQjmKxDhpC8WQ/sYoDOBhLVUQMZkrECu1KRChVG6hpkXJbSwVDJsX8Y8ZL4ceIxREaitWmRM0/'
        b'onzoi7ab9/QVJjn6qSFHWGihUXfRWRndU/cQqesQq9E4ojUxgBvJ1a0B1I5bPXyW+5aDpC5hmfjR/4f0QnC6Kw3x9/S7KwtZHBwQ4O632NM9kAer1CA73ZUlhsXGCwGC'
        b'LErxrmFXBJ0Qz0gf7hXUGNYTAYoBQlErJNOjWK34Bhr+/5IpXOlElTyJgNmmr2cmoX1vIjHRGbpATK6eGElSbGZmJDahrGTS6dv0RZbW+ryvEaTLh/Xy6hdxw5dKA6Ji'
        b'k7Ckh/+skfBbZSvqSVFGIap4eKoTUgGgir+mMFUG5IdeU7gqClbFf991bUbxICMHsWvLyMGaa6vIIeR6KLseFjk8ckTkyBMySn6WrRstirSOHLVPn+JRluqViiJlpUal'
        b'+qUW9CdydKFe5ORsCn+lSxTW8ZETGJyTHiMNm7SPi7SJVFBSNPpeqaxUHC0mbw0i/8xKLWL5vyxIahalBqWG0dJI20g7kp4LhdaiKWYbZBtnW2RbRuszQCqasgHzWdVl'
        b'Pqzm0bqRTpHO+/Qp/qWUWyNjoYZT7lrQSbCYUSUwILPoKOUjlx5iY98HBM6v7g89ciQyqGusKsFVlRzJfrs4O7u4uFJR1nWbKtKVTgxHZ+fJ5B8RkqcoJHelfv4Bvnel'
        b'Hp5LPe5KgwOWLiP6vtjNnXwa0CxD/P18VpMVjGr7d3WY6njXgGe2iCWXOtFEAVb9kWwn02ylyiQ6m5T0Q0Xnp9TTL5DHNPyDac0iy1XPtJTbWYKBbisWPlq0MTk50dXJ'
        b'aevWrY6q2G0OVKhX0mBQhwgh1M4xImGLU2SUU68SOhLR39nFkeSnEHelT64pqpZyKYsIvmvg4794oU8IkfUfTaSFXrzIk5WQ/F4WlkaXswBq51Ulk0QdnaeST7KyJfHR'
        b'xNP45Gh84V2jQE+/pT7uIYsWBi32eMKkJpO1N6lHlR/N6PXiYmWCSrWIKSE90/BJiPFVxbCUJtOUxF0pkZKl07RMe7XHo+H9V+rRYK2Np5D1SIUOt77J9vpiVj9p9f56'
        b'Fvt64FL1f2/yI7s/0Dx39SKjosNS4pJZn7EB8B+JPugTTaMthoP3gWvDanMZk3/wMNZDJhFa8PCG2KT6wyIW3iGLG+X93g80wOMOUSkVIluDmQOEd9zVpzSkyWTw9x++'
        b'RH+W8iClPRcdR/W7Tx4rcJBUbC65Uo3VLg6kc8/0iBcYKFeFHr99L9OyhwdoNnI6nD+lgGVBfj0iDAzVLUyd8VmEAacmz+TRy6INNdEDhv1GD0hY6Ij0vQw9LQZMTz5G'
        b'N3Z7VDczJs+Bw58n0YV7ALNloJqpVp7ImAqYDKNy7fugg7zX5JLbkFV74MfohHrsE7PkNraqWHo4lTrDcbrtEyTJz1G5zWKPxz8szFz6sL38cfn0P7vlNp5Bf+iNyQO8'
        b'8aQrAU2id6H7sxALVi7eHMSHTwvsR2r8/f7epHss/1rvYZOojE1Qxian8Xi5NrZ056asUnTvttVuNLSlOzp9hu6vttRCbEs3RluFY9f56XRHF0dnV+ER7cl0HbU6s0eF'
        b'VLu+ns6+5pPur2I8nINQNS1QDXz7TFIxtIZ+m4edSbj2jL9nk0w78IIQP99vmboQFlw1vKp9IRQonIHmtF3LYTr9j9xjJHjUaM+MpeykPyosmQ4olZogrBseBT1r7ieI'
        b'nxpcSTpbw5SCY0A3/gbWOvLAqCha15S4bpxjWpNavDDIfal/wOoQSorjH+geQllRAlkpNYfyPBNav43EL0J8+zDmIgHaRN1vat1NMBVrP8PuMh+zIwk+hS7rrm2vNcW2'
        b'Xy8A1kOJ/DxV8TxqvZYYW7526kdi47UjDPBYFUSKVdPEbgyLl7sHB/RjBo+XB26NTd4epYxjHZc8QOH5BbGfuUQmjGdyWFwae7H/Fc62/zErgGzwHdKFvUFHvtAlGhwO'
        b'/kSqnxol804N3QC1e7zbA0Gl31WLpdTniIA0jyA1qdTDt1e62vtEoBbsypdROoZHxSXEx9CUBjClU3nEoI8IZerH7LBDoB2uY4k3HsAiCSfGGqL12ljjeSZfWUDekm5+'
        b'DHgTq03wkD3vx8Dc7q5CkZeKYX3CMQsG9+kymA/8y1+0kSrHUICt5KcJcvEGXJRyxrhPjPlwBm6yiC3I3r7Iu3sw1opewS5u0t7gmL46XmJuGmSa4D4i7RUrxLzNu22b'
        b'N2/+ZaZfOCSe77GStxjXOeJVajFm9uKxo+fDhTgWKTMNqlO74Z92lUITpJJobBxAEVBtHPyCbWwwDwucqPPt+SABV9WBhoUdJcLnkUEiOAs3l7CiWMp2qwSYziMBDKkT'
        b'j49n5xYH5Hqckf3nEk4eav+WvwuXQlk83aCFOmCy8JtCPMqH4Hg4evliLqm1UwDm+Cz3kASQBqQ/bXAmbQIHnVIZHg3BytiKVeUiFbXKPLBeM6HQ2xAWmLmd3VH80/jV'
        b'svgbxWtv+Y4rTn92/PP6t+Slsw8WrRszqXnpDOOvBgfPHTp0X/kQ8Ti4dSp9adv2gHe+eUt2a+uDQ7cdsxreKBt9Osjr5Tenes4K+PjvsYnvN2Z1Pnzxznfj3V6Obt9s'
        b'YfZ7/NRfx5u/98WeGTYJD71LN535rs36KcnxLROWfDbkq2//uubn4+217ySfuS0LPzBxQ6cizulfnqYKY2YtNIVyOG3n6MD7LpwWb7F3TsV83uN4uxGPJkwRkO2pC4Ye'
        b'ZxIxLEAy2RIPMsvtJut53V0pzqyldlu4CRnMk3iW5USNA0j1zi5ndTwEbczuGQxV2MAbk7EU61NFC3fO5g3YBePxSNcolHKmeAxaV0ji5NbMz0N/DhT1QnXEfXCOulXM'
        b'w318Epkuyu6WWs4kCIqopZaL4l1g6wLm9QbvY8B93nYMus8mjPdQL8Orq3rhK2LjaLl0g/sU1gQLIHNID+f2Q3gJjsPRJcx4jWdWYx3Jhs64ZvKArwjyMG8J1E3jnWBO'
        b'7rYgE92HNkABnAsXTVZu7RHPb/hv2ds0iHCu/SlOOy1EhoLTKUXqkDLbrJT9o9y+JmKxaHg/ao6AgubX17FzYI1nAK+QPwHg5jugttYy6rHa2h8Ec9MJoRLtAHhTheSK'
        b'h3LTlp2GmdjxCaTmvjBs1AgW6LEw4K6UMo/elVISUrWe2dOdlndWpb6rd/UE5mplqahXGLupeg/y4DRh7LyaaSQomsY8UHa2abTpEwSrq/1lzmlTNxdGRqp6Miyrt1st'
        b'9kKNoNZXa42Wu1Ix0jVUgxkSquVw314QezSoVtRVsq9naW8WQZ4ql2rwXcJsMm29ZEHUfyIlShB/NXyyj9OjeOIp/l0ttK9hKnl0XEIYNSrIGcepQOnYn2dNWHwPQrXe'
        b'bLH9laKHcqGNzjU5ahsvOSdrWFC38G6e/fhtkmdiI6nY19UUXZR0fB3kNowTnVaNiXVjA5Y4OjqOVfQjkPL+EcwHOYyOpm4MyJqUefJHXlDuuq81Pc07XVyOwhAQfLd6'
        b'MjtqTcMmwH2JOz3dcQ/xC/Zd5B5gL1frLzz5Zb/+XszpuH/y04RE3gl7gBS2aVMJ+2EaHSA5+p9GY6QtPJBCp0FaE0a11tTUFNbadD85aRX3AL+FPn31PO1+yk+o+6nJ'
        b'rfim0JAA0wErjBs6L4i6HMUYnkND/RLi6UoxgAP3tuSu3BlZLG2jsDjqNE0XCM3QjVYmbCFNFRnWj6d1XApvYouJTY2KV498MjUjqZ+PTURCvCqWNBdNiTRcLPuWtHK/'
        b'BeOT6W6YUHSvpkCJHL4pKiKZXw+0q0KB/jOnO0+W86StfH1oGewFBE6hvsxSQOcmWRS1phOdomRzjc12nn61X32Q34lc5YGC/qWmRqe+6Gkkl7g4MvnClLwWxj+sfW1R'
        b'qRIiYlknaLTBRGUCZTinrUiaVuhsMhH4Ya+9MbuRDMr9iF4YlpgYFxvBPBCpYs7mU3ffeu1zZ7HAsN5FY0o3abkN+VTYy+lWLbfxDw5Q0M6gW7bcZpG7Xz/z0LZbsMB0'
        b'he0ThDBo3LkWapb6XixDA7mJapRSfa1K6WgeWAYuwGk4Q/24MUOtfJpANWYz6YepUvc9eBcwbkay0ZdGMzmmzC6HJjyuEqgnMAMqiD5KcdmX8J5eJZOhgXeLUsViERH7'
        b'l8sEzoqdPgIUy/BkrOHg8ApsD2Je8XAAzmJTT0VWCucwQ63IdlqkUDrQ7UQQP4r5Ah8CZcsIsuEdyL0dbFd42FMokyprx374HgTigsvu5kR4L5jCdG8dODVbUGiXYAHv'
        b'ztQJB1KCaanSI2KtzAbOrk9eXYQyy200YBMKXc7V2RIbTPAq3xSXsHQGU5ZH4CnmXzUM0lMoyyEewhvY6c1geBy8/KnKzCejg8WYZThhGJw37NJRF+BePEFunLKALDgd'
        b'BCcjl0Puot1wDDKgjvzUkN/7N28jOlLtovANSi/IW6SMXb580wblhHVQvnmjGYcH5o6EEzG+rDH88fIGGV5NNBIHkv4RY4fICeohI4WKzZDnAq39lgtzh0HuAjgUDlk9'
        b'CpSFp7CUXlMHsFBTzJanunBQv9x8aAo0Mie0tZgLR6gTmhQ7gpgTGpzAjhSKwbRuDBRpLAeKFQLcTmJKShAWJRqbkm6rxOIgod27GRaoPYF2jhqVo4A2l5O/L+yFc/o0'
        b'J84Ec6zw4ujBjNiDDN4irNeGiqQB/aFvBfH1hYNrhB7FFsg2Xop7bVOWklSWQDpe9RZ4hbCRDArqAlcI9cvYuCEpe9Mv6GAq0VGRnrAggzwPSwKINp4nws4kktQFyGbB'
        b'KK54HVu8u3MU0XQ8ujTaFUJykD2FTxGyZFBqOQFrB8NZOGM1WMJBuS/FFcnHdMaOMguaQrXAGYmxmijpBdg8h/RRBu7DLObRxZzyoDicw+wAo4BU3M9QaOKWibsZcnw8'
        b'FV4Ojn14QrKoUxg1p/AFM+45aUirVaRYwCG4CmdSVpI0dxPFulYN67Dc47HJ5zvhZcjqP/kAL0vomBnMhpYqWaW2EJXjWThGyVxqZjHfHmY8WwWFkKOmsMEj2NaLxubi'
        b'Csp0GPtMoYlEdYaoWeGL7H2X34h/dYHZ29Y7bnxfsevIuuJxe23cvUZlTPLQmTvJfVxRx9/3fmGpeM140mnPCzuk1/1vjZPb2j4tOT3na32bCe88mGVRGHOzathLd55z'
        b'C1g+YtORU0Vl0765bpbiX1+u+5nlsoCz9TN/8oq58Mo388eeq510We/+hOLX8gKrdspjjm+evr795sNjU5a+cHHS1TFKk+k/3C2pcSw7/ZLuv2KvX5ZGXHv4XNQLmTO+'
        b'xMIPDR597N3ycsjUxoyzn3w94q7pxqjILT97N+52OTf7+u4RcwfP8X/4y94Yq7n7P3aM/U08Wtqx23pX9oGr7W3f6b6j0+z+3cR/Jde95f1uzdeXX5od9fC+5Ej9ur0d'
        b'30+UH3l6zoPcL4avG3zK/+WzS6o+uOJ/+y8fVmebDrkUfn/udyUnsxV319e/+czn0pQZft8aX/pw5n2jX7Y+PevHqndDCu7/8FzEnYyrmamum9L2PBWTuf+38bXPv6bo'
        b'/KLx+OK9V6t3j9k2q9zLMWtVlfHVpvCO9daFZZeXeb5wCQZPPP3RC99mScaV3Xn0geiy5AfPN3JfSpqw6e1s45XB99Je2mnSuqbs7ZuBz/x1j9WiKz+8957CitlopkV7'
        b'ew/C+u7WphWSOKzCs8wCRIe9LbNjQZN1D9CFTZt4I06VDFoEl8gJWCNauATrmQlqF9n8Osg08CHrdHdoBGibw0xHmIlHdgq2IziO1wRHzInjePqSogVwEfK39qIlGQ+V'
        b'kkCowmpWuOT1kMPwE7BlWHf4BDguMIzIsQH28qYyuDi/BweKbzwrxcyRmGmHdS49QqJSE/Aa75vZDCeMmV+nDhSRLZp37IzHdv4unSx5dpgbaOHvCfVSTjdOPBYuYylr'
        b'GGcnKPQWOERc9UROWAWHWaFiIJNsk/l4xKe7fY4a53SwgcWyz4IbZFXpZp6TQJXGQsfsc1CCe3lDX/5sKQ2LJ9lmdI+LpwwgdKcygMIIct8ezks9AzipvQjaqbsxT5ix'
        b'H04uYda9RbN68KdMdmKOshtcIdfOEfdCnsY+6kz20RKGtLtp0SzvSEcfT8h16k1R7AzXdMnqM5VlsgGOwE3I98Qb/gzFyp9IFiZukrlR0MFjXNSMG2XnANlGmqgzrJ/h'
        b'KtDLhJANmSxk+/Gqr4OClGCuWE5KX6XQf+JYZtP/ji9fuBq2Mac/2+Iebp6hyEjMwtXFRiIa3G4m1pXoiyzM+CBzGrhOGSnUV/rMA1RXCEY3kwwVDyW/6T8rFtpO+Sks'
        b'Rfo6JjQoTcwsl2ITkQVLnYah64q3j9Vic+sVY63FYNmf6Ux5pKcr6ZM3evcA8iNaosi1BJAXUUvm+P4smencNzbdbZlPUFHtrj8UsJCZ+Hg/Ei5aV+MEJBkQY36jQvoo'
        b'tI/6EBAVTzRX1ePseMxoICgqVE0NU8lX+foMoI2Yk3+j+mgj9n5MQjHGnN3e3Tkae8HG5a8k+7wdlPUKF8UTcNF48FhvxhOmIMJMqZ+9dlq6gCAmFWDbjolULMBrKWqK'
        b'NyyTMIGAgj6vpfeSHcmK6phKPryoc3ratPEbdGbgYTjKNByPQZ407SgH8v4oCv1ItAleobo5hYgN6lM+uCihB302eHMFHw8cKKbxNstmyELjvrKx4/EptwYsZjCR9Nhg'
        b'pwgrOegk0vvFFHN+k9rvhiWSZFMWd5JmxaNW1sF1SJcZKOFUEkVcO08F2Dqo4CHJcv3H2ilsyYIPpXhBmiaiMO2Qy0oXT66PetNdww+r4YwOp2slNqKO9SzZQaQe7dCI'
        b'xYFYKKWLFAcHiVqWzpJdgKdgn4DxlizmUd4oaBtb6RrwKlTwJ3+D4DoLFikYyV5bhekeQvgJ6XA8zKJPtsSz/EaRt9qFuBUdTomnWdjKoSF8mp1QAIdkjA2RLOeXSD1t'
        b'N5uxNKVwHdvVR5CG0M40tv0OPLleNd5YGwiFrngOS4Mp/RCFkdP3F2HzsBmsD57ZfZAbSabQtSmhfnpe1rySe9RjLOfGcRuPmISGT0pV8l+6RdHobU5uHh9qezrIlOvB'
        b'VqyZeHRPZ2zFVmSqcSe5naJILlKUJR7GVat5izcSIfJTSlpJA1kXRip9YuOj1MzF0jj6R1/0XPKxXldDX8zQOxPhhMswL+YIzR9aGqilXiy2ozKOKGD6LGwj2lTuLMxK'
        b'XbAkOslTuTse9lpzO13M4ApWwBlWsREkedIBoQ8DQ+OeCzfma2s2bghnz3E2zypCR0r1bTjmeY2VCvMuBMDN07FJg/9nAcdYRy1dA/t5jZGbtJRXGCuIYkdniR6W7CK3'
        b'kowl3A47iaVo9kwsYXm9p2SEljbN40N9fhoTwynE7PnFiXiSH0WzoJGNohNjGPbpnkVwlimI3JiVVD/U386yHgdN/thE3tDjcG+0ZKJoLlRjo0LET/JMuGCt8oNLUOEq'
        b'5cQykRw7Mfff6kPlMd4/9bhIwzytPCHSCn5MPi526z4GVYCVdrJUvGoq5miIDKnHTBfIZ8YABZlmOVBMak9VEzK3oNzdm411EwnptyYjMlOI/qdH5noJue07nS0OulCo'
        b'knHB5I3l3HK8CdfZHCcT+4Y9Xh4hs7G1wys+ZPB7iddAGVzhURIridB6EpucvLDVZyeeE3E6kCki69o+SWyR9Yti1XJSk0tnQqKCvVWWwZY3W6u+fe7OgkVyM4tRk/fl'
        b'mBbkZJwKd3t6peXUecU526VfBp3JHmVVmnL8lMu5wjPBN0Kjlq9onf/Uc5C1ecVh2ZDfdF8/HLXccd1PFa/MHbP3mYp5H/98c94P36fd8zzx9Oefxv/cOPb+K3WuX4sr'
        b'Vkd+6LrizBZ88IFJ3POfPGz+cXrbrLiIaUFxJX99o3HIuPB390WeeBixynHmkV/e8J4avN31+0Eym+87qgsO3PTPW7/zwkfHfjHXcX8m6P3Pnks81Wi4YtrKttA7f/nH'
        b'q9czZkQHf+b424jXfRzqPrS9NOKlVw9eeOP6Or2/PzvLC3+sFd2Z8Y84LunYKodA2d22/S1Zm765l3dfL9B62vnKz/yOD2+b3l4dYO2XYX1KFDh6xedvTA5961zs8Iy2'
        b'8w9eHPaMz9YDnZZ5ndVDHf9R99TVwM1vWq2Nmv10gtPaN76ybbnyzrS7AX9pW73pVtb8xbMzWr51tPrVzeGT1zduvqRy+PHkxj3Z8UM2xxaVKz/uPDm07OxzqUcOLSl/'
        b'yXpbxJIzK1YOm91yasyPHzz7XGWck/GVsS2uESN2Pfy54ftx4PYw/Yu55j61K34c8TfJSM8Lc8x9cs80ZmYtzbu6K7YwsXLVt2UnXwk//8UtyIzeljlRovI4mv1UnNPQ'
        b'UNMhOxov3GoP6VwxZOqXJw99PjhsVLn7DdWM1pO7LD93fi0C7tR//LThV9yukZ+Yh9bvFH9+7uXz1l//MDf3X0Ffm3x5ev0zbz+7//5qi++GJp+bttt/UVrHU14bovx/'
        b'+HXwg8aYH42C/rnWe9eXDwy/svxN/6Ontwd/afNhzv2EgjeaR7zssmJp60afL9Y8tB/76su/S87vembytO9utPwYcs9n5CtGlZ/HDj8yc09Da+gzF6/d+Pv4wa1vHEmL'
        b'PS769LePr/z4T6f08rL6m/qfB32WPHKe4sX39kUs2PD+pDdeiYtIWHt0tFHt0apn5uRnzQv5KmGp7Z7WzoqNBr9+mfyiak/CZx/NfX7UG3VxmZ1Ldjy/e5R7wdofUuoK'
        b'62e992Vxp8OOt+ve+9Fpku3MzEGdFh22nUs3vrP1cOTbn/6i+NfW079Neuqmbsewjsr2MMmzI+699YX3mWO3Rtp+uT8m/abi1707amcXeiaNq/z1gyxxytbZZ6892NU5'
        b'569ro5pnVVqm+Y29W6EMuPdw7a3aN973VHT4lry/f3OGX9MzJQHbjk98puzN2ePvzC0J+GK1X96I38aVNFZNcj9aWKK8Ol8Bd0pvPPd926uys7c6bvw27WOvB9bO99y/'
        b'XSf6/vmvdr/eHHDwq2++mFv/w5V5T60p2hG76O0t73VKZt36OYRbf/q20vCIT77DK7qqQb9l176w+7OUbStezD+ruvfc8BJl7JYN6x9FbXhvye85Ox/eS6k6OcjD7+vY'
        b'8B/y5jy88aXxkOnvvL47NuTaVxOPL/ztL7P2PHQ8NePXxH/MfLbCacb3YT9tbb+2etapT7jt9w6+1+b396DPtkZ/Grrno5cv7m6Wf/bSU5Y/vP/xTsmYyk8/aJgpmb4n'
        b'5qX3Qy7lrMjd/PD3c2XnIxdeevHCZ//6XbTs9aW1w1wUm5lm5bkeblIKk+4EJkTVvKIhMSlezUOpHQ3RMZndE8wjFSrXMrUrSrQMToX3pcYcA7zemIJZcMkbC4OivTX3'
        b'TZ0lMXh8Kbs/Cgr2UA00Kq2nijoWcpkDif1qy77+I95E8RMU1FFOvIp5eYfRYGstBJRbLHnzwjk4CpcErELqvSWgFRL9tpAHnTtKdOFqFeaa4/6uqCZj7JQsMIObTFse'
        b'F4bpKkeSv4PST0E3+ybmsUOKdVkk4aZinS6R1FxZk6UQYa9eYBWWBJC8QsS2ZFM5mkz3N+Ol5t4+tmT7v0lU9vWiGXK4zFRoTyyLJ33hRCTstN20fAfFE6DQgPdwKYKM'
        b'oVAFLd0h3cRpcEao/nk4uh3OusgwxwGvYIG3hOz2zWJ/aJnOTAHT6I6NOWbJ/F1sIhuRMeQQ+QAqxzP12J1sgvkCgmx0DMOQXQHX+byvpsAhLIQDfOoOniRzQ/FKaON4'
        b'LL7rlnhGZeuJBxIxb08KEd4P+ulxZtAgSY6S8RaY9kio9eaB/2q2cJwO3hBLoA2q2F3ZVgU2eWOjvwzO2+hyBtjqayOGM/P8eM+gq8Z4XUXBHw1Ir+hwhnhgJVynJxCX'
        b'RSz7IJLhOVIyKOEcDBTYwCpvDB2SQUuggEfWvEF283zeusLBGcjgrSsueJIRvG4m8vgF2pd2jgrDFGi0saVE8xZDJZiONzGfdc3yhZgHVQYyR2+8qsB80gAm4rVT9Zn9'
        b'ZQpc04MLU1R+Il5WOActCcy0tJBIv83YRGpNG91ugj+thQ5nbiUhs2wf1LKHJhAJsdpboPCE/M0CJPAIWspac2hm3WuUjFkqR7wGGZ5w2cjGgai0JrqS+XgVs1kjxTjC'
        b'cZmXg08SXPSIxRNkiKoUIm5YkHTpdgkbcuOhdPgKI/olhzdp+Ei+HT/qr0MG7vdWUJB4Aatah8y/UskcvALH+O5NHwrFZOK0QzkDZOwCY4TLvqxxzCEvSuVpqxATLQH3'
        b'SaBUBIXO0MZCa3cSQenyfB1KP6vDiWQcdKyBCt7o0inz7gqe5mRrtsvFeCkW29gEWoj7VGpwRjiyhOEzEh3kLN+hRF7j8Zq7LFHJmySDd29m7w5KwGqZDWmEJB9SJkM8'
        b'tjRZDNdDB7Ob6+SwLwoyKLqkr4OIM5gshqNkqbvIl+kmtuCFNY4yR4Ut6TNSZP1YcawOlPMmsCK3BXZkoO0d5eToyQMim0KhJJzClDIRd++GaSTfJL8ASKeC3FkRVk1V'
        b'8CU+gPtMZAoyVElDWCfrkClwVIQtbnCDvRm5FMsF4xnn4c+MZxvwMl+keqJMFpMJQKsJ1QESzBVBTSzu5+f9NSJFF3vzpnldTuaFVVgixrN4wZHlG0cBulWenphpq1D6'
        b'ULAHYyeJPlkKD/E21fNYNC4wmC0HJC0OLiWs5MEj4eZGolwoqTcd1mCpGG6KRnhANSuSHCppNXhnvBA7gYz5Jl5jaRpNEjMxvxAP8XI+1Mew19ZDExlqjiYhPS3A8nB+'
        b'jTgyDU/QUaT0cSJq5IJhUCyG87ZYwxBGzaNSUqFURYFS+ZlKxiEttCXmSvCIHR5je8UKImw3q/CAwhAukUV+OuTSdbyRPDfMTGqLHXieNYolNmIRSYbdg0Yp6asVIswb'
        b'isVsyDqQ9ZjaU6HDmqdlpudB/EaYSTLIpoc2qdg0cbKUk5qLNvhjKY9bdX6BnN6ygRZdTgSVHB5MTWTzIzIBDxMRH3NtxNyskRKsJHexKpBPspyMiZsLpKTUNl5bbcWc'
        b'HpSIZy024lGDD8JhPEFdZKMm+FO7Sy4bIaZiSaQe0eFpXUyhFvbZCTD8FEkc6uMlptCMPO82tJrDdRXbrWQW3qS7+eVxKNRJJ4+I40vQMEbML+w+y6CEjtvjZNzGbuAn'
        b'fyaWJwhrI2tIQzJBaqCWjAcPfb7a9XDame67Ph6ciBOvEDngBVM+Cr7ONoysNC0q0tkGmLuV/GIK0CAskUBV4ij2esiqTTw0ORTARQZPbkJmG2211R7jId/J10EBN+EM'
        b'b5KFJrJ2sJm2nyx9x2QpxgZkzTmMpyRjRAtHmbAELTF/mgoLHLA1mBTHUjSO6N/XhekLR+S0LoPGEnEliTxD9/fzkgkj1/JztASOuiyY3RO8XQxlQeLkSfT2PrJPFDAA'
        b'MSfM87VXePqSNZuZ/IPFOtzMObpwKgWKWbMNIY9SZmbSt609jNFkBFUm0+h1hyQrBn3cAzy9F3J6MF4i07dC34n0cS4vxZSQMSFjzzokea5na645maNQk6LPHgjEiuWU'
        b'mboYq3pSUw8hU4S26hzfJDIchEnmPherxHABssP4KXgMs+EovS0m21KpBA6LyLrVCNlsnMApZzyr8htlrVCvJNMkBpjjx1DTNsFZ2KvGxA3Eoh71YJi4O0ezAs4UOajL'
        b'vwtrWVbmeFUCp8djBk+Y12hPUhIGtAA8PxJOC9jzEbCP9fI6vBEgY/vgKjwuwVYRnNsexYZG/DQ7YyMZ5qnFIH1OvHzwJH6k3yCyaD5Z271EnAtkSbCZTEQ3PMBmyiJH'
        b'LFi6k1be0MuXjhLyriVRw8l630a2arqJ+opGDcEamYLjRMMpqUgR2X3ZInxk+yyVH15xMrQJ17dlC7XZJgnk4aF1PFRzLWYRGaDJ3tFRzA0JkWA52cwsI1iaRqnYIPPy'
        b'nQHFEk6sEI3CoiSe8PqKN3aoyLqOuQZE9OjAfHWFhmKR1BXLdvBdtheuYrnMgdSJjM12IjSOEg+CZrKtMNmpEbKIqNHCs9v4OdjSId0ihsMxmMVen0S6rciETFEnW2zw'
        b'UNDVp0PsISXyLm1kO+ed2OTgh60+Gyj3wy4Rlq1YyhKWzFiyDWoEYOMeoMZ6VjzDuSRG5eiVoiDznohs4sEqMZTOwSNM3oKSPZtoA0MrO1TzNLWhi5oxtklm4XkyCmhX'
        b'edqSkmn8ubFyl8RXtCQUT7A2w0osUng7+sqxjSzQaaI56+az8upMxSvUzZssUKfJ3A8XTR5NRDy2iVbIoWPbGmaV64ZtcmOTwvy/g2yr+5j7PJ4FH3yrq2TGfXbKo0/t'
        b'YdpPefZwtvoMUJiHJzYUWTDUDordYcnDB4op/gf/jD7D/dAnz1mKLMXDRUNFVmIr0Ui94aKxYjOBmdxIZCIaLx4vGk6u5DoUethEbCmmv8eLF0jNRKNEQ6UmDNaYpU3P'
        b'kkRmouGSkeTTinw3SjxcbMFKYWU0lORAsUfsJdrSNSPvDGXv8xDHhmIrsSFZm4dL1bgkPEO6nHxOJCmMFE3U1RdtH6bl8IVvq/54VB/f7F2HQRWkqUdSmyBV7fo5DErn'
        b'PrLqfhzUf4lI1ixknuiVXJCfn59CSj6YK7jCqBdciXI9x0KuAxd7uPu6BzKAEhYSzeOVLNOAjNASKikvIl9by/8LGBHSRNM1TRRPRyM9L4smv/WlUqmASC35d37rS8zM'
        b'6BDlRJZzeJiRoYzqnhON2sMZpIxnC+o4PKvFsL5rGpm7c9boYt5i9x6B8obCb5XhwDAjkkh94dqg27UhuZZFGrFrY3JtInxv2u1agBw5YaCBE7GMHNwNTkTSDU7EqlAv'
        b'cqIGTmRE5EgNnAiFIOEiR0fK/wCcyJhC3chJGjAR42idyLGR47TCiFDgku4wIvsUNndNGZYOI492iwqPTX7k1AdDpNvdfwNAZCYfdO6iEN+VLvYPcL8rWeSyiIymZN4g'
        b'T2EtBNAQZSod11vpxzbRk8N7zORDKV3+ECaI8NLMP477oc6ORW5OFnA/urA+JKxGyt0MSijA3dc/yJ3BfozvBbkR6OYWEJXUM2zcWUD7eKKHJ2sQMdQlejS0v3Q1oBg9'
        b'C68w6JEG7aW+iZr2bjHtaQ2QeX93JisPsIXsP4qV0YfvtC/zrA4P4edkbMEg/HQ48SLMoBB+WDWJP5o9SCSlazIG70XEvNoAyh/V5h47bJCFjorKojHt31EecY+wO9G2'
        b'73uHGUZ/wn2TMWzm2tEx3Kxc6d+u1StEvP+Kr4tgXZLCcaKuUOsS0bXK+qHiPKj26WABVf3t9vRHTnfM7UN7zdI/ibhhoUdxmAba7OjPwx7IG/1m/WSwG6co7AZd0f+r'
        b'sBtjdJ8UdiOS1YTiClAf/v8k5oZ6Yj0Gc0M9mR77xMwnxtzoOT/7w9zob9YOAIKhdS5rf/4PYF70jtbiAwvC4mlMAA266ieESPOaNvDUPjgZPfpZwMagmxKPd0E2Jtv+'
        b'o30eB0qhLskfgaWIjf4fIsX/fxAp1DNOCyAD/e9JcCF6TtonxIXQOoH/hwrxB1Eh6H99A3B0/IIYKEEgnlonYBKo8QjmBgqIBFiMhT4Cj26XdQ06MVuGZ6ARimMdJwfr'
        b'qBaTZCa881fKDP7Juxuj1zz1xq1Xb71567Vb9279/dbbt9qLKg6NybqSOa7yfKYiv+2Nk/smZJ0vv5I7OWvxnTGMP3zv68bL/ZcodHi/WkyPpbgBeBYuaHxjD0Twvsvn'
        b'x63SQAeUwJEu+IAAyeRBWCQcDcpihBPUcQndDlghfydvwK1JhFI+On42tlOrCea484aaFrxG3u4JAADZcAmvSPU5mdrB899xb9WEzk98nCi0hA+h19Umk/y/ESM/9Ink'
        b'q89GDSxfPWmgfAwLlFcWi7okPS1h8otImfgw+T45aWLkx/azY2qJi9cd2JE3Qq/b/JKp59gCKuPp9ZLyZFTOi5YJUp4ek/L0iZSnx6Q8fSbl6e3W7ybl7dIm5Q0c7d5d'
        b's/3/Rah7T8AwQXQS4r+3kM2GBuL+L/r9f9Hv8v9Fv/8v+v3x0e/2/QpYcWTt785/9oeC4QdYMv4vg+H/ayHcEq0SpAXPgEaksEPGGw27oYeZQIUVjxw2m96/gc2GvPNE'
        b'IJHp9nlgrr8a/MvDCwsZ89hKCr6lz5ztoRjyDaAdDsN1xsw9ynlBr6hsrIA8ISobbwxjnttu0IT71PHgrjSg1nNLCrXr4zFst9accGvB/oIOPMzwv8SUPaTKADvgiHMK'
        b'pYWNJ1nm8w47yhn0ZczxsOfDQDDHl8jKzHcoZJL+QrgYwtjml2LlNm8NnhcvPdPIWXs84Et9wTguQKYnxTosHO3LAk5IBYqSGKsrTSx42UqHFStpALCXrw+cD/KAix6+'
        b'jg6eviQRJ7GHNzTKXCA/IJAbBSdM4uZhIY+HVoRXPARiDkgfw0FrMB5OoYcvk+FiQq/EaSxroouSBq+yiHIpHseLXCjk60EZnotPcSSvGc+E0kD1w0I/BfEvCWnBCXcd'
        b'bm20HpxxEmg8qqFSLlOaGIvxHLZwEnPRXDw2hgVZrMRsMgKasHWrSgKFlP6jU2S3EsuYH34B6e91O0gtFoTGTTFM4mIdrv1VrHqZ3PHMjA4+eMUYnM3cX0r94mlP+Xqv'
        b'2tADU+0XJFkUjxvzz9PJw9+s+ftIh0Hjdzh7bnK7bXTCfbyb6oddX/3uVO7ipb/kzX9I65V/fWTVenS8YWnTyPRXT0d/8v2ujE2WK/d6pr/2434LvXNrPxwxcaJFgJ/p'
        b'2JwHzx6ZuiEj8S/ZM9umpOy/X/2S88+Nt5VfVbxz2DrNePOpBRsvhpz6xvTFsqOqB7duvv/x7K/GfnW4zLvT2en37dN/yz3+vKw1c/yutIiUV349LP2w5oRtwC8h3vsD'
        b'/r7wxU9FX3wqybjilXgyQmHG+1zkc5YMgGwx3OzmE7QHMpgfRRQe3NFFbscHhEKnAR6GYrzMmLiXRdsJMaFYPUS0cByW8EpPu9ifBWx2RWvCyW14BjuMeL+WorX6vRQb'
        b'Ww8arQk10MA/cRVrsFkzXhi9MGSQb4+7wH7BGwiu08hLhisWTmHwRJPhtBCUCkUyaOvh3iaWQANewoaxzPcWO1fGd/neYqZKXQ7B9faSEFiaCplOfEW8oWESdQEiuZng'
        b'dYkPZM7mOTaaB8/mOY4hQ6A5xhZo5D0Pqv3xiLeLF10HLpOpfZLDVmvgPYewLgzreLM1WUZq1VwilwUfO1OsgyN2Xr78CmEnWraMGzRJgsd3ruajKc9iBl7Sd+kGaecc'
        b'YMR8QVz1/L37C9fcATd0nSBvW1+FS/YfjJX0epwymcgiJiX6jJhXX1eXYbFZCsS+howQmEZTmojp/e2je6tO2kMdDZ4k1LFL5dTp/wxWr39eXC0Rje5PpHfekHfXOx9X'
        b'pf9CUOP6xwY1alPX/nBEIwX57hvROM6PoW7izVg4PnBII1QrbPowYPIhjWSadKZQ5nqySHRidVdMI5nYh+AIF754rkTGjcV6Ce7bsJAdMa33gSo4pIHFpKGNZFttZ5v0'
        b'tmC44T6Evi9ELXrjcbYNyEezsERugUlo3FbjMTzEC9bHYfsUqBfxsYlCYGKpPwvIwoObHLFEgq2BLC7RG8t4UJN6bFCqkkQumE7+OMBB7lCo4bFBa8ctsEuJYnGJLCZx'
        b'NlTy2bQFWdOIRLIbtij8hIjEw3Cc39duQMN2Go0YDaVCQKIXnuTDu8onrgz0ggo+IpGPR7R34Nm6bkDmMNlWERNnaNxg7EoWzCaGXDgfCIVdgYFQu5aPDYTDc1lLeK49'
        b'QIMDQ4tdQ+M/HDKLj4xrHj+OBgfqR8tCxXVuO/gvP53vSYMDneujQ211Jrr8+eDA6D8cWNau1xVYRnFHyOrbirUCQYo9WUGTPH0xzx4PCe5HWEyks1ze808BVyUuHolE'
        b'jvEmW1qTSkYabjHmmAbNnciqVS8xoqGBHmErQuOi4s34ut4LtqKhgQuWKULnrHWbw6Uwv7nj/pDRFRuoiQyETEeJP5RiDusmV7iMJ2X6q/koQBoDCI1whKV6O5UFASY+'
        b'dAqNW7E9mVSWBw9qxMxJkbrUpZd3512HJf+HUXsS/a7GZUM6D7JWyKBSj4/co1F7gyXszkYonyFTSibCaSFkj8y8GjYJI7dAppc/C9tTh+yRodfMz5zqqVAh42IsWdQe'
        b'tEETT7BQIfOT2dgG44GuoD1sHsEi+sKhgcYLOHmNJFtgq486ZG/0xFjZzzOkqgqyZMa8MT8lyFs12N3ywYO0eztUk8bMsVCiXcfoU/vSpUELJpzsEGeYmZ+ac4wbdGfd'
        b'RPvGT843XltmEhT7gtPJ6FVfe9scPmyXX7Z5yKX1jype2XVe+twz5fPe+enF8gfzfk35ePeo1H/u/H1xddTSecVpQ58PiA2+7TPznUynQh8T5++bTeuTi9LaXj33wi/r'
        b'9n49+5vzzi43qt5qX/C67fnMwwuWhGbYnxhxx30YbCo7N3NJnJXVrUWl2YNO6dcGr5jS0rghtz5+TuDoIeV697j4oe9MTd816PDcH5cOsipfc2+t57Zd7S9+4HLnXtVv'
        b'50d8OaP9LBwbd+iXzB+V96f+a2HYuCwfy3C75MjhlpmdFlcNp5/8ev6Bv63Re9j6DxPTsEuvvfXI0xnn5CkLnx9Ze+c5vTX591I+3H7/400znlpSdGXy20Geo2YMsa1e'
        b'Hzf5u9YhI996rtKmdfXprA3fu7VsfKH027yat94c9KFJftErnTYfOznPLn9TJ7otyuznp170XL3qhtdnnTnDzq/8pOzg53e+qHxqWPBC9/U/mX1vHmc6paZZ8naT1/fj'
        b'2oe8PPlpG9XouM5DWV4J8PPQ1Kde+yR4+1Mvrt+7Zf7Hn8z8xrA+4MzBorS//WWk03OL1895Xe87g4sLTZXzt+jN/0dd2i93Lj5InJH/+QHnrZbft83t9Gq7q+/6ueJV'
        b'8A7MvPnqd9/Wl/9cO2zPy4e2b1wxeMNw8/baRpvPKz5/ZWzEnfYvps2tb3YK+2vooNAD3/pMendX8LYvx3UsyRq17baRXcaSutozFxYE/zLtgt9fzv44u3ZtZ4CpP774'
        b'1ItjXYdV5b/07e+dSZ/AWOP14+euvJb77s1n5lw2v+7WPvbOWbdpH2TN+H3/S8/7p6bfuBMTOWy+tdvvN37aU5gRcjawwcjvVkJCdeAn7/8+K0sx453xn/5/vH0HXFRH'
        b'1/fdu7u0pQmI2BERWZamCCg2xEZHEbALSJNIERYQxUZRBKQjgooIKk1ABJQqJmfSjOld09QUUzS9mvZNuUtR45Pkeb5XfsLO3rlTz8ycM+f8z6l45oWK23r1YQtz5lw8'
        b'PO/V80u9ku5Mv5yQNHfH6bC88k/f9ttUUlC5Y/kzKb44zy9VyfO8XSIjzxdc/uLzisqVfeo/njNa5Nb35x9341pnf2lV8czFUUvOvXJtVMqvJ5xWjjot+3rPvt81+nT7'
        b'nvjqqXGt+V97ti6dnJn1yaXGt3rmJl5d0ly0yV7e5nTaL1Bytzo9bvzZNyOnTXv9lxtfyb+5ca3scZnzKfHX20O219Sk9efO/snlot73R3d8+XHt6ue3/3En7avnLe85'
        b'L/ld3LtwvHHorXtuqdHLvD79oXtUqMtpZ6PQtDWFSY7c7uzPTKL+lHwS8tOLK+f1vJyPTlWldV4uuDX3YGmR2TNzP3jiD+8VLwbeqt0y7w+96De/uPJErzyeGhpDLWqK'
        b'Hg5/m+A8nANXd6WWo9tgP/QR6FukzzDwmy7KpVz+vBDqWmwI+jYVOin6zWwZfR6I5e0ML7zrq55vgIsU/TZlK4PfnEDnlowErXmjHopbU0IxLcIIzqNmilurhH34PBFw'
        b'a6gSnaYCAuqCDjisHBaKi8QaZLi15Ukk5DQqN3cRYGtyT9sELKgc8SDoFoZdE3NzIUsNOnaaUaEmHss8PRRZUzGHCi4UuVbvyUSGOsglXmyIMA+nMdckgNQSJlCZYKO7'
        b'0svaEnKThwHUJoxn4tBpUQgBGayBhhHwtGJ0hPZCe2rsIHSNADvGSAV4GuZDTjNRphYO2aO8VNRGIWoUoBYCR5kkVo8OrSDvQ33kED5tljodYwd0ChpV8DRNp+HwNAvo'
        b'YSJUH2Zcarw8rT1j6LUExafNi2CS5BnXTcPgaQnQTxBqPJxZH8JsrDvRmZ1D+LQVqJhA1MhdTI8FHbRIk5WkaSpomp4fA6ehtlHMgvtiKlTKbL2gATOGQ9gyM6b904VT'
        b'qFbpS9xlHVWhy45jCY10TBrhMgQu83YeBi6Dc5DJOnYGTnAKKLVXWScRES9EwWyi01FWkszXhsQC1ZYTv3unRKh1O5xjur8OVEEUiih/CHgSB5kUezJGAJfMn2evAq4N'
        b'odZQlZcE6qDLjzZgF1TtUNqqQGtmOyhsLXQrW4CHUfEsilojTDjKkS/fw3BrkyQSOA/509gNQbnXFi+5Cpu2K0ZAp5XAAB1+bwc0QLBcAjANDaQwbBo6hsoYVCQznlem'
        b'OFCkAUM04K6VskfVUICKKTRt7SwGThMDuz+ISIPuYZE9K+GS4FOqiXlzgjy8LI9h4mwwZRgHBlDLZ4E4YT+qCBgGTxuFJ474SnLZSV+WjIGjg/g0tD+YQNR46Nu7ly2y'
        b'KiiGC7hPcBo1DmHUoMuMPT4VDodleLKPo75hGDUjOMWwTXI4qsCTIQDUQswYRG22MBrmqBs14brnz0zwVUHUghlEDR1yhUYCUYMDSgbXYxi16VOpmnirxhwvqx0CRo0i'
        b'1HbgKmmYU5SOTihRuwPDqDGA2mTUyvAmqFmqgqft8OZkngScVm/CECVNplEMjOJrK4IOG4oogSML6IupuCE9ZCvwJiGDKTYNLuBJp6OfhXepdiyOdWgxiBqFp6GjkfTN'
        b'BCxw7Ed5MxKGeYs/Nl+XQgfgotdE6ZghZtYfMYAlOu8RNswRPmrA+zi5iNLAuyyDvLXiTVYAzlj5clpLCW7mNMqjlzlwCQ2EPwBOm2kmwNPwcjzNnOEXQR/BQ6kAakPo'
        b'NOs1EiuoRidYY9qkuCyCTxtNHBd6C/g0zLM2MI193dIYqEPFKqdfIrtEVMPePA7HoIWg0PAufyEFdTCIGmZXGfpnE2qCbsiAMySLCqVmsou9W4xOIczXTsOHIIWqCUC1'
        b'Oiij77qOUycgNXv1IZgaHEL9DGY2EGpPoTN4xZBr0Qu4zSaoLRhlSBT2DCS6ehJcwhw1yl0/zA1GYwKFDEbq68JZVKG6ShPNwPIzPRaC8AFxRqYqFNMk9MzltAgysHmh'
        b'P1vDRaaYV8flHp1KqQ/Lq2YeY9jO2q4xbRAZh4/Jo5x2lFhvEbRT2wk9lA/lSnIgelhpQqM/yhSwcRPnSqA4fDul0MdgII4dW5W00QwbN3sW2/lL5uNFOISNg/aVBB6H'
        b'aXGnP52nCRtRFtRYUXAcg8alQRPb+o6jkpD7cHFQEy5A49CZWDpkO1Ej6vKaCWUUIEfBcfjFHtq5GYZprGoGZFvnxqBsHmsZTuwoXNCh1/zQBZeHg9m0ZlMwm7otHhAC'
        b'ZcMzXno/nE0As5mjQnZ296GBXWykdqESMlgcp48yxEkOHL3vg368O+0n9Ool10S5cg/hhB+LT5giDclyvOX0sx2mAZ3dTvNBXbycDqg6Os4vCppPiSgcr6gDuFFD224d'
        b'XvYEvAYDUMJKyFBglmnwThZ1h5NrWXRshaEQ+7cVMyh5cGETGzFyFzo6QoCRa0CmElfqh8npuDUqVODzQH+HeFcEXpv0mE4AzNkUeDtBM2bHiJMiVMmn4bO0lXFqreis'
        b'l5Jc1ebgpqWhctpJETdqtHj3grFJM+kiWAGN/wnUB6dmEFyfhh3mG1j4Dv2xe1WIOGhDlcMgcWt9WadrIUOiQsbiEcrgtFx5XFOLPmOMytCAv9LKmoIBGfgaz1gJWwJt'
        b'UCJnr+Itdgv0UPivH2pLmkY3PVmwYqiNqE7vPsweXvvtdB0aJcJZVSP3LhgGO8TkdZQuJ+lKKB2G2luESZcCpClqbzJ0M3YE70NQIYOM9RS6x3B70fqMys5i3qGYAPeW'
        b'Yb5jCLu3Ee2j7xqj1lAZaocuCt9j2D0/fAKRylE2PhEujMDuQY2HAN/bg2rpJjNqPO6vnEMD6IKA3ysxpBOwBJXuFeB7a1D+MPyeCWKsZyqcxiei0oji9xh6D++LhbRU'
        b'1LwLtbqayQi9EfweZGLmgjBQ0zej4kH83jDs3kJ0VOJiakhPoxWrAmQ2trBPi3SJIPd2T2HT1r/MgUL2bGcMA+1Bk8BdnESHo5V2Vvg47BiG2otDHXQRJI5GpQS2F63B'
        b'LicIbG+6GxunTszyHBgJ28PMKkPueaADgl5gx+xB7B5qt+G0eB7KMN8+wFC9BZhcDgiuLxh2D09cGcPvQeNy2oGxKAOyIE9n27CILMugRfB/MRF1LoYqaPKy9WH4vVVJ'
        b'jB9ogHINcknmvmoYSs9yplz3/x6VR8FXVJnAPwqSx37GqoB5+uK/guRpDELyDPCPEQ0Bo4/TBI73H6B4Yg0BNiehMDkTjftBeQYUhmdEc+gScJ/ERGQskvDL/iswnslI'
        b'MJ7x/RqD/y0S76C6gAF5pBJjH3dvBB7vLxqFayfIg8QOFRhPTH49FIeXeIJk/LsQPMP/S/RdNa77JgEokphd/xZ9pyHWVxPQdhYqtJ0BTpm4UjfvqBg67GQp67bed1kt'
        b'4izhsjQWLkPnCMNZXeGvMuMBoN06SZl6mWaZYSRPfpfpCp+NhL9a7G+0OFIcLs7nw60GFUkkHI52tk62brY+jZOtTQB7FOAmjVALVwtXz+JIfPB8fp06TmvRtIymNXBa'
        b'm6Z1aFoTp3VpWo+mtXBan6ZH0bQMpw1o2pCmtXHaiKZH07QOThvT9Bia1sVpE5oeS9N6OD2OpsfTtD5OT6DpiTQ9Cqcn0fRkmjbAaVOankLThjhtRtNTadooWxopEmB7'
        b'o+lnEm9cY50xNZQUUyWbRrYMj40eHptRdGwsw+U4x5hwnppFKq5rL17kE7BE0JbdvMjfZyRJrJSG52AIv0Ebm6R4EhNCyfI4zrRmfx1oBAXyadaIwlRKOaWt6aJh5n+C'
        b'NRsFEgg2c/hpUkQiDfAQn0Li2yaNNN8bHuzB2jQiNGyLaWLEtsQIZUTcsCKG2RcSk9QRJfyVAc9I1eCIhG88sdvyiDSlgV2VptsjEiNMlcmbY6OpJVJ03DB8BjWNwo9D'
        b'8f+kLYkRIyuPjUjaEh9OTdZxm+NjUiKoEjOZbD4xO4iJ1YhoFqZLo6m1kuUiuWBoGzPShouYOglWgGwi7IR5UI24tamlm1yVLdRUGUGs0ZIiHjVJZA4tF8sJqCN0mMWf'
        b'YGsXnxgdFR0XGkPQBQKSGQ8BQU7c11GlMjSK4koiWNQOnIv13jQ8YhvebZWm8azh1GzPUnjmRigsNl450norLD42lhgUU9q7z0TQV85fF6fGxlxXCwuNTXKcFSYWthqp'
        b'sO1QHRPx2imgxNSzVbG0ZHT7EOENhI/UFTTS4oNqmdxuyU61XWKqkZZQjbR4j0TQSEfKJTfvif4GbmzE4vlr47C/shfEPWKmgmt8vAVbNxo2hZY7NFd4Vqg9KF6KDzci'
        b'tYxgJPRX6/QReCY6nC4ElhIWild6CG5SCLPZY4UNFjKc3P4imE1oeHg0s/AU6h1BboQwE5IjhCWrTMZraXDLeDiOY4QdLItRQ1ZcaHJSfGxoUnQYJdDYiMSoYRFo/gIR'
        b'kohX4rb4uHAywmwdPzqizOC5piMQ2UiLgYm+SiL5bHvuo45XflLIm5LkV+QX8+RvtqcrHU246N0aZyYvpZb11DgO1aegZsyOF6MucuOXhNl+OVyEPDkqh3ZIV0IpdJCX'
        b'4Azq1KJcZgBTP1ajfh84K+Xggju3h9tjHkp1sWfDiAWApb4WF6L9s7EuR/OOnmgFHTxH3Bhxc7m58WhfzM9//vlncbgEC0o3bLVdQ7QPitcza4FZCzGPXmri4WBvj8oc'
        b'7HlOOke0Ah1Wl/PJBGmRAL3QqkS5uihnO9MMYPlQ08pShOrRaW4mKlNTzEKXWAvPGm+XWVmGm4g43kfkPAEGcBmEdViOetAAKwP3KpuVo0V+iTgzF6mZHxoQXDDbQraM'
        b'3IkdhXIbIrr1iqAR1aTicghEAfVAgWJEWzyswqEzwRcL6woPL1uioghCFRoTbOTJzGQM9eL3O1TPNNAJM0c+zhadlotZhssLiEc1dMhvoQ0qdrB35Dnt3fxWlDsxmd6N'
        b'FMIAdJPn0L6OZVDjtPfwMYvQBfo+rnYReewOOeyxiNPey8cuh+5kwrOuQz0pLAqIe4A7zmaz0h3lqKNzQ04Dl+ipjyHBN6lefgzUk2GqhW4qDK60QRepKGgIBeSqp0GU'
        b'7EHaXALnid5lyDLFErfzONTTQCrE46GXDZ8wH6omoEuQOxq1o3YvI8j1kmlhkTjP038VFxGp72yGein5vCWXYpLQN1ZzDYnRnuXCJa8nVRQ+ZnRfBUJ0nHw7T0wPxwMt'
        b'UY47sUo9iAq9AlHbICFTwxgszBtM08JS8xmpFPUsnQaNcm7pdiNUNQta8MBTNcw52IeOog69bahqQyIJttktsnBDecxApBs6UbdMIzHaOAUTgURkhcW9ZmYTCXkwgDq0'
        b'E6AbXaLvNYvMV0E6szlJ342qldt8UZ4tubQVa4tCVqAz9D3IxSuuXpmAR6PKTpu8t09kDsWzMWGRx7qboVCJLiagKtRDSoV+kTFcRI3MTLQDDjmSOv3nqWq0mEfpAwv3'
        b'DVBNCMAJHR1OAOaoLNmZzGi8eDASDGQYrEQHfWw8/QIpLdDswtDiwejACzxGhmXnBuijxqTUl3jN8EAy5F1HWeAKmyD2FodKuHDUrcHBgYnRU/Z78coCzNPtf+pmbOnV'
        b'uNdcjQ7cNn6mYOJPJ5zOlM216Xo10WO9wUm3jeebspY4nYxbJrLwPzx77ZotkZmjjsZZLeRkv05bY2o8j1MENesXPt7u9aL3eytsj30z589fXjoe//TFlKTA17KWfNdb'
        b'MqVgTtq3r7xx/MvVP7kdW/ViQaKOi920JVNyOi/nTTMwP/XulRl2b41aYrtk03uvV/wover5S8Kdba8nn3oryOY7zwLxqoTul8SbPr6Z1rTtt4Bbz7/witPOPz4du3LJ'
        b'So+bVwKiP/UwH/v1mYuXzTwK1KvNZ6RNfsuovbhGmbJiYeypmpeeMfjt6RVqTdZXa63cPjUpLagZ/aHTMct2j1F13c4bw1dddGqZ/+nRUaEZU84umrd14/rltgtsvRwl'
        b'cR9WKVy+aPuqPznZ17I+N1o29W7nGqOo5q9u6N1t/qFqfPTtp6RnN0yQH4nZU3kkdGNu2GeP7/6hTLHRwWPHq4pP9mY3VCiMe2c99cpLN2dW2zsb2GX+qvW9TVOu7dXc'
        b'7qMhC65F3Jgjeansm9Pde98+sP3JojW83s+G/QUa1zdmPHfbqUT3+ctqzklPJm98V7/mFydXPPhRbxybmuy4Z3XqWyGJp3d9lrf+1sVuccFnraUllq9qdPaZzVJUN059'
        b'5619MRPnXbAVvbTc6/Ub79eFRj9+Lch/5s8iw93npzjd/Oj0Ty88Pf7yjpQVnvdWjk/47gXHW5k35981ztqq6fv1wnkdjy+e+m3wiU80J42bf3HeCxn1mvPOyid+7/v1'
        b'y+9fvZwalJ79o8cTr+2KeLM8Up5nUfPnnqCbyjkHLnXcFG9y/spt7tHoT6V3MyOvoQl3Oy4dDdw4Melgo/bAlh/5rzpS1zvM9vOSjrtq+oRV0RNb/Jxc2273V25+Xbdx'
        b'yq/ZkpOdrtceG9t+7sAdzW/f/4N/Q2JQd+wL+SLmu4pCE33gqC+PV1eDyEs9nLnwKhhDYv6mo0o4R7YXvOmgXJ6TQT9eZyhLuKdCOeuhVuHhvRG1quPXD4rm4x25nF64'
        b'xQTgY5S5ahVt9hQctZYvZioM6PUBvPCIQlMO5ZxaCG+GjjBHe9Cvs5VELrLzs+HtUC6ntoe3csGbGDmmt6KGDfg9oiX1toUcP09rD9MxqAAO2rlbW1GspzoXjA/olq3A'
        b'tDD2OpOI5h6dmTvCby20o0vMPx0qjCBXYCjfRg1lJ3Nqm/ipqNJZuDL3JBepPeiIn42HNbnRlUEn0WaXmtI7NjHqHq0w2/aA09w1YnZPdwF1orMy4jzvfvClREMCOfS2'
        b'bKoEVQ757VrtSe4AcT9YPJnJ6MAswXeXyAztY7eAePCL6NCP9YZihQe0wAkoshRxkigROrBMqLp1FiLhE4ij3Tkoc8i71zh0XJIwS858xUJmCOqAGsWg20hUglqoistS'
        b'jk+tPDtPHzk65mVD1Gm+QgHm6LB0rhbqpdfpiehElBLle1gmkwnx0vW1QZ1ePDdpmQTO6DOTgcmoewPRbxfORHmawnOdpTzq0dakVJaK2z+Aq/INNbex9hlWkekMCToD'
        b'RdvZbeZxM2ulNaob5oyM3GbWoFOC22B0wg7y/GyhDi55+lh7+Ig43S3i2dDqSF+3RX0zld4eEVrkkpzd4eo4itW3AAvMjQ5sGktv/A95oTz1SVM5NU1eG2VCKSPHDHJZ'
        b'qvT2hX1utvjM2yrahS6hKmaykI15FOJhM8plUIEJmOCZfrMgAE5Sj5GQ7TaoiYODi4Q22xDlDe4r0W+KrTkpOipCvWgAXaazE5I6XmbrNRoO0tvqJhFUQxYcZorKDHTM'
        b'ThkHeX/hSNMTKlnrjqfAfqpG7IZ6lZ5wD8qlai2/+VqCC0zJPCiiCsYldszRJVySEK0SiaTmrYYrPyaCgtF76TMHmTrpUWEyuqgg7eoggeNbprKt4Ig75oo6wmSDTmLx'
        b'xpHP5q/YHjpVFjLSJZjYpKiXF+kKmwjmGCp0qbvRktlCVIFe1EB1Fk6b/cnEoraYIX+jBtAqRnmQvZEOpL8J7KfoAkFBBifxjB3lISfWifngO4Y7TSyEFk8b7iJbZSEE'
        b'+WK22FtRLv7pUMglaB/TgF8Q4S97oYc2xALXmEUewyU8FYylUuN0w8VL0altSUR6SIFGGeRtT0GdOgmDHJoM744EzW2HCtx9bPAbq5Zq6ELuVEohHigdzigVWphnlos4'
        b'dchEBbv5WSjLgV2kH9K1UyoSGcGrwyE4GcHPhDZ3um4WQMV6zHBVo3ZiUQH5fjSIn5QbjZoko/CcMHUYprCTc2SkeFYIzlMFTfx8b02mTquGvr147DxQpj0pBJOqOqfr'
        b'K3Z9DNM30Yts1x+rxOQJl3WIc50ukf5E6KaADXOo3iEzmD/oRLFOixZoZbGE6GB84ZidluUwHQxUoXo20z2YRJqUeqhwyM/ykam0rkVwAJUTn5+eSczlpw80MwVXsxqm'
        b'dT/cDtSz0AMvUrpF2LmjfDE3FdVJnVEfHGIK00oO5Sp95ebaCcw2ykvE6U8Ur8RyWyMj0R5ULVOi6vmDLpQxB3mMKeA61Tco5ZraJJ6FlBPDftFOKFA5OS6EKmOFp804'
        b'VOZlY+WLdxe9KHGoFWqiDsUt4Lw+a5/QOIJ0ybGTQ4OvlJNvklJnQscoicSifkKsQzQClbg+yskTIvFzwkzqXGhV88X78hlKBFboIPQRfEeg7aDpD2bCL9L9dyXxyi7D'
        b'DxdvdFdR9SjUK4YWdBrKBCMLb3MFPX5s1LCQdW4G6uOhOArvfES9lQb74BLKmwiXHvQB6YQy5Dr//V34/0jr8zBvA53413/Q6ezlIrRE+jyBg6iJJoi0CSyEpzfqBDJC'
        b'9SRqVF+ixmvQT7o4l65okshCZCky4PXpdxr4O3L7ro+fjMPfGIuM8RMD/FdXRPRCk3BpavRGfsQ3IvKjS98kYBRWEtHs7Bw9/DrqfscHUqZT6SU6i76RYBPt/2omxKy4'
        b'odIHR9ODmGcTweY/qG32cT0WwxU3D+/Hf3R6kPW3nB604DeY04OR1Qx6PJihuhWn18rWphFRtqZW5J7M1t7RQeXc5WEOEP5jAyNZAwMf3cA2VQPvjSctES5ZTaPDR9T5'
        b'N0fjukZwGLt5f0SNHYM1TqG4ZQrWjTSlLxL0/T+ql3Xyuk7w4K1ycPSjKr84WLnFItPkuOiE5IiHQPT/RQu0g1X3jY9uQM9gA6xI75VJuPv0znLwuvLfNyLxJvfIue4f'
        b'rNt2VTxxJxQXGU+dHJiGbo5PThrhneif1S94AJn/6Povj6S1Yd5y/k1nXR9dGQxWNm6oMjePxf+qLrdH1/XUYF0KUldc6JC3J5V/DOYg4J9VvoVVHvHoyp8drNwy4CG+'
        b'kFQN+DfLWYv6FwgmaP9HNODqyGmlTgLYsv4XvcVbCK0zKf4RNb44WONYwZ3Ev6gvS7V1bA6NIYqU4PhtEXGPqPSVwUpnk0pJbna/HzNcMXi/95F/1SbdwTaFxcQrIx7R'
        b'qNdHNopk/9eN+m98YG653wemiLtfiyH2jXadeFGkJHLb8nMHiDdLjUjjqBvPc5xGrqhrbqZcRPlfOWTPcUADI6QhIgmhdnTsL7xY6qkMZIgN4H9kpvZyUTuN7jv0YyLi'
        b'goP/vg9LUuFbhN+wJxX+J35jH3d2hCfLh1b+fzUNEt+A6HN9JVIl+bpfr9crVFt2NvKGtzonsRTJrxwdorIHx7ma+2fj/NgDzNXm+PiYfzLQpMbr/2CgG7Qfxdqx2gdH'
        b'mtRG1LlEcmbq3CG3nyo3UUylK8rWGVTn8geleA7EeA54OgdiOgf8HrEwB1HD54CImdr4v8OIOZjsS/GM2sv0iMZAW8RBgRXVGDhvp3q0rWOkXJa5PnG+oL3J0p4FCYSc'
        b'dahaqZuoKeLGR/CoVmSLzsBFqmSR20i4O7upswZtuyQ9jvqYQOdQHxYVyc2KFwXrE4cXh7xQDpbQe719iR8M/xX+NkE8t8lVHWqkqI4CitEl1AKFXp4Ud1tg5+kjXJ1J'
        b'uTlQbhUmhbNEHUcbdAJlByi3UQN21DmVqENQvTGNtakGJdOYaw/oR0eG2fyiI9BLUY0zrceSix9yV0XibTRLbETQYrGOFhw8BaqEOKWFcIpigk1ROwtSmAXlkIulWCLC'
        b'EtCPXhQWm8UR6MjiAKoxi0dnoYDKitA/28ZDwmmq81CAjqIDtGgezkI/c6LgYieRiKAal9hLH0nXoXoCoLLVlGMpU3MOD2ccUCNt7PhgKBTiUeFd6CgF/EDjUqb5abJE'
        b'FSjPxpcInah3Dqe2kR+NLqgn00AdJXAK+rxQgQdx4ueN8ui4MxcE6LJUMV+K8lHbuhEUKVNR5JIhihxJj6JBZ2UqWtRitLgak9cD9Jg1nB5JRzUfoEdbX0p2wWZS9zc5'
        b'SnYxM9xtGdlpefmwMBxi1OrFQCuXUD9VXC1FhzRYsCUxaplKzX0n2rFIkwfHQPqIWRKj07oR7mPoe3vVoEJJ43aIsax+YKtoF5RYU3y2DJ1FdUpvO3tzEYdl2YkyOMRU'
        b'ZJlLlhKIwR7UzVAGqBKy2fBXzvNRxf8RwyVooRCLROYAB7VO2aqK3CRRVyO4mLlwihLSAjgGZ2gQ8Qyr4THEp0MW1YmzGLvHV+mTI3oKR3QHUyRGcil9OUiEuui7Bah0'
        b'+MtwkYW2nW64QhVCSQLNU2gA8qMoP5nBz6KWDEPFUEyMDNVvnokyaFeTdGYrbOVbZw/BbZzgAgWpz+QRiWuiiEYltnh12MptPH1EnBnsl85Bh6cyN9JZ+g5e3h4+jqoY'
        b'TATiUjibjlQK7ENlguW0iFMzC9Xgx0ArnGRu7ou90QVc+JY9D8Z+ofbXdiiHquu3w0lMsnl20OSJ54NeN5OdBHLpnYvFaulWVI4OU587TjNHEQ2IYID+2PaHxZXxhXR1'
        b'VMSxuKzroWONsJ+IoSoC7yckwjvThNahorV0R0FVyuEgAjigpCYAcHC8aGjTmovOD+1bdNPyhiqmGM7eNmpw45GsEpFtB/VDO6MXEpQokwUBklj6UJTDKTX26AJqHsd8'
        b'm3ASe9RD7PnTYugjf8jZodoAOLXoiWT9l22gkylzkgn7hiRRxnYN6GczlW+OcjHhijjRbA7PTAMqgG5UyTbWbFSpoaDR3yUkFlEo3gDVEthrnTvgOKYt92VyG2sKAS3n'
        b'd81cxeawDDqgQWFpg7f4nuExawTTd3QYMmkhtjMRyRY1dTBSk1gP5ZrQ7d8alaCLgxvWQtsRWxbdr6BfJufZmBRAsRTyUHuKVE3CiVADh+oNFiQzO/WcTUp0Xg1nOkxi'
        b'pNVAEToNjXSRo1NW6Dgqxc+s8aG22Bql69NTLGaszOo53pLj9ENiQmYJHhY+mMhb3uPIpxDtwxMl7MvJe6Vx74vZRiWetZB9mWGik/ojh/mEFSExWRMc2JcnpmkG+YlN'
        b'8ds455S5I30xUFaG/CeEsYvbqLtbtEu0TTucC8I7aAIfrpJsGbsiRGUWpdzHh9/TnBcVEReRui1xQYSm4CFAwiVvYBNZ5q9MQZ14YxoYdp+uQMXMV6q1hw3k4g9HRrhh'
        b'IO4zOqDUwAtKHPQ3OyFMNTugcbR0aQoHFSuJ749GTCmLSAWly6GTqO/xQjwLB1Gpja0HBaR4rlxhE+T+kHMHOngtEYeqUJN2CJSupZHNfaANmvFuLbdBuUMqJG4CZC0O'
        b'xPuXIRyPrl8hESlv4a6pv/xnRMDc+NdWGC0YuGg498W5vuvqv3KKfc1Iq6y+6dAvInf3pKaQ7sde0Wl6NSnn5Uuja7U3uU6qcJljIDa8tT0p5MYY+xk/jDFVe3F+ymKv'
        b'7Lc/+Knqq3lfzg8ySwvf3zNpyZvvx0trRiOTslEu737aEXrM4anuxucXq1drV8oXmTxXotbFz/5yShgyjPZ4+q5cw7UCDH688YbjtMyF66+9qtth9s5be1bNVLNq/OSk'
        b'w2Lf1R/Z//Td3qPTY+6U34V82w/iUxbVl85eeTWP77X1DzrZMDfHOHBZ5JKc1zeM0XWNWL6+oSyt7S3/gqSsiWMzI7586vCMJU+/fORad9Mb50NNF367fYqkajwX+Uab'
        b'77Kf4ZNfugsaFl2z68lOzf1665d3O84XB4zvv2na0f/1ou12n1emesx00fTJL7Bb3Rn+47fhKau8/V5c79HxwtZrl1u3eKSM3m3Kv2LkYPJnZuqynlfz326btvH5J7Zv'
        b'2WK+cZPsRtn+gnMv3V71fvNzV45XvDbwhG7TD67PfG50bPoP8m/VGnUClJvTe31HbTKf55Oa8+70Z8WJ6qdtS+9p7ih93aJRUea8uHtpavnXVjfnfD5g8ab8J/WbTks/'
        b'kbfX9Is3bhVVTnfZvOpd+Mre7rviOc9Hz+fe3bIpfslXSZ3LWt/p/rPOyvtWatqRgmdfXz/5wstdS1tvPRnY/8n1J+KRz+b6ZS6ig3NrWzzbl3x3NLOrwe7VtWP6im48'
        b'O24P+nnjb7nl98ZuPv3MTz9/+/aKj1/ZteXqt41PrL73dkSq7dWEw2nRL53rM73av//Lu+dbX190MffOH4Hls00u9d3rub6/85N11dMGfhb9IQ549dK6Zyau9Uhx+axl'
        b'd9TRz9b9WdaZ9upX1ncH5od+IdrmN7fwg2l3Zhr39r/g/P6Hs+Y3L/tpv3Pi2xoO3yx+3+PLqT3Zzn3noz9NC2+yOntr1HunHGdPP5S22nFJ4Td3r45L+UW+u3nPlK2v'
        b'fhBVcTlnekhNT+EPC8c12S56M3he8Q+3Qx4v7pBNOJGe9vWYD0rmo0PL5XMEIPbs+fSMb8CH+DI4jXfvfgdUSTUO/qg6QEbgZZqWmK/G3OIodBq1Qr0YjqPjUEh1HqHo'
        b'UqjMSo7a/THLSBFE4/kg6FRQzVPSbulgoEN3KbSOi2C6zm64DM2qYIf8nACiip0ITYL6GDNe7URXTvTkmH05RHTl+PRiTrKS0MEwVWQ/MT7RGpmiNh9lURWKJT6lhvik'
        b'CsiifBIUezKdUwmUQjPtUoK3nVyN08H58FbQYiFdw3yEndyJSofBSkfjtgzX1qKzmlT/FTga+olGVuGqUtUGLWGaqSo4HqXS1XKSJVA3SrTJZFoSYbNsJjrJLKFRaS7h'
        b'+ADRAsPVtKjxULdkKFZndir0p6UyJWeVGcqRWdqGWw6F1eShD8sKpWygcoxQtnIQAYyPdIICJj71GGYpH3p2KL3l6vPxxOA90UvKaWnzcDJMl85ByByoJSjKXMzCqDlC'
        b'FjTz5Daino5ioCe0eFlbmkHFML8C6CScYZrIrjWoSxVZU8pJ8YgXUtyyETrO5rffEJ2gYTlFnNTYiUKeUR0qZgr8eh08aXlEA0omSQJnEueI4LydM9V0x0SKSbQ412E4'
        b'60gp68/xMVCuRLke6BKUeGDGlOfUE3grOLaAagu3r50ms7RS9xzmPOYC6mT+Gk6jAnSaRigsdE9gumCt1Tz0Qi0UMcXbRTxCBTJo3EZDFErtLOCoCJ0LM2QhO/tSaHzD'
        b'5XBQpew8xbpyHrOd1TJPH4UaJrbL0AO9IijejtJpg2PnuhHuX9PWy1aLsEYm0LEcLkicd3tSsw+ZGjQIaDU8HhkSAQtrhPlkzG33SZg+/DKW20qGYKvjSLi1oYiO3sBc'
        b'3y0w9mYgz3PQNgzlCbXoIB2ciWMIdpvZpnDStWnENEWxjq5xdIL4hBrhCYL6gVgkQv2odRSb8AJUvZguiJVwYigqJQ8DvuF01rZBAzrMYkOKA6FqimgRymbuOFA27lcB'
        b'QTFTaxIpnon0pSKUH4RpidodoYNwRiZgE3Mx003wiW7BtNRoc1QxGOK3G3MXDUnACAw6Mb94WSZordXggLExb+YKvWxWGqbuodEIa+YPAzXCQIjwFConywREYxZqoqhG'
        b'tA/V0kkJQEVQK6AazbEYPzwoITqDGumuNhWVbsKTDkcsGQBxYRqz9Dg7GbofxB9ixqWBxg/EpCI4BCi1puEDMReN6jxI9MB0OMzo8KApFBDDXH1oxsSI+67uxU8JxHsb'
        b'GSs1KHIVQhpiucGLoSJrlrMRKYZjqFxlwcWpmRgSC66kbXT+UuCcA8qz9jV0wNs45sZEnAwvaNSKupHgebElFNpIDmsR5szQQeq/sZVHp3CjWVBhe8xsZxF5zj2Y3C7U'
        b'iFaggt208C2znRV+1tCNRzGXShzqWLwd4FHXKDhJX03Ci3+fzAoVLHERE4PmWXitHWHbcRl0QS4bsiFTH1Q9Rj18OTON2odJ7xDmIYlRW2XQfXZtnqly4//P6LD71bL/'
        b'vcvE61oEphNMzeUpY/4cYdP/8x3jXs6IwRolFOZIfuuKLKg63FpkJZpE1eMEREjAjryIKbQZqJBX0+YtRcYiS95ApCsy4alSXIhpyP5q8+MoUI0o2EmecfjTOJE+T6IZ'
        b'MvCjvmiCeBxVkGvhfKaiCfiHlKRPS6NQTJ7cSe6U369mJr0Ntp1HFVPKBbZDvWfihuS6ZlJqeERSaHSM8rp6cFLq5lBlxLDL0n8R7ACLMG8Slfkbg3rz1/EnMRFayIXh'
        b'37he3cf9yXw3atHfycS7JWSKdypH2gv9TflGOoNIOJwTqtSzxtttucp2u2bBehahHcuU2UKE9ouoi8oqi/B6KxLitx/0mxqv0hGMg1MSzLCUoTZ6HUDCznYJbTCHNtIM'
        b'P1YkN3muBJU5wn5BiPXTWS1UtgzlsspQsS27U8jGm3D9YGXo2O6RtWGmhF50BKBM6FeQY6bF0t3H1sNn5bbYuWREaIAO4tFAxIWM1jCH41DJ7P67eFTmNWikTWy6nfHG'
        b'EwuVqCeZ+EmCtklw2Qvl21iiMi1oDNhGSpvhuNJd6IOLuRqH0lEDrR5vBt3rhgcKobmnTF5pOezydgMc1dCzmM2QlgdQ6WZhcCB98wODA9W7k+3ovtoCJ+jUDisqEB2c'
        b'TAJB27HOES4ocq8G1IqmRh+Kf1Ok7MbU+7bbjohVfXGGi4yqjrzV98WFS74TpqeAoj/4wLgz3vv13dzAyMRrS3jN+YgJc/fnVVosu34m5+KpnCKfRR5VJWaOH7g+ob5i'
        b'qZHR8crk9CUdabffVb40/6cX4ywiE9YFhVeH1yq0r/x8p9Ai99bzfZe1fS5J1xugWYEbND3UY751b9cL7+xzm1003Z/L0ZO1F53SmVm/3Oh8/ZOpDddqLS9Ne8N7Z5r5'
        b'hXUDBj/K83xmRskbDT/6bT5v7frU9NWjunMfr7n5/Vnzr3xjs07c3DdlVUaQprvH0sdre556rmDjxWd/rs+z8jTRndR16Juej2fFduWGBQU2L1n2zOgxshuB2W+9fnTU'
        b'uobkI7FzF57/znCqXcDEJunGZz/9qNE2ZO948YGfz3z4Rvnrnzze0tI57rHXfhS1f1J04JuYd83HVu15bZLVNwHrC8I+eGFvbXme0+oFd9U2vBvcOG1WqKbfEn/3DHPv'
        b'5zQ9rH5f0Xr1XtoHRht/iv2wfsG8r2bv/yD65O9zqlYZPv7T/kM+F1+tNVYePZ+wUd1fO0tzuU3IQG+D7bVjbnX5hmYB+12WvAC+6n/G/GZSeTVl8tkd56dkX074uRed'
        b'75j16oo7HxYUNMo/npTUuH3ax9E1fhGnxRtLxk/f0FFYPio6ePml91754rjmau2NlydvSraatV27K9+wfPXjW+rXztrZ8Pshn5eUL/w5Z8UZ3zeeOdIbfXlFzI3rt3rf'
        b'Xfeqt/f8mC+WPf2Mjo332iN3vSsrUr82/iEOgl/vk37vZJE453mDH778aEbSl7rzrl5cWeCY0/j8wKe5vW9NT/l896vznQKfX/VU6y/fa0w6+qVdY9Ovs/cuq7tlMXps'
        b'9XGzd9qvrUSfTHv93dVPx9p+qI6unSgISPsmJGdh1zt7nvKOeazX4srj2W/q9bSE/Xyz1CGgyzHuyXbHL0UXoiZ++/xA9sQM27kvLv4+Y0Xiy58XZbYtNt/hm9G1V/Si'
        b'xOBAppfcnhq4oWooi3nACFIxFjPG9xtBzp9JOZAZsqXUqhIzXejIaMHoMiuGPrNHPX4qQRLLZSeJ9qA/ypCywpugbY4Seu195SNt/VauoMyLCxyAY4LEh3nWbGodjVqS'
        b'mQefZhsz6jPOGnOHD5qEohYdxsI0orpogd92iVRx3JjdxvxDP2XbRi+VEL/VNqia41NEiyDfmJrUS5PRMcLdY35fm3L3thrUx0oiZEwhrEkq2dHRedJr1Mnc1aDDEsyB'
        b'5kImZdomhYplS+dbKZhbMNwzmSGPd8oqL8aYHQm1IW6vE+QiXEAWJ90uwhLu4bnMrVAP6okl/rfgWDAzcUQX9Jjzk31wBpUroS2BCkqFvsToVGs70escgyo64CvHEd9d'
        b'1FYU4e+YFWQmx+I1n/WDdszlqkUFc/xq0dxYtJ9+Pw3lQx3hqR0lzKBz1STGiVVA+y42tYPGsnBhjngpFg2YXHt8NeqmLt3wyKymXr0yIjA/TNrqjyWFUw9IEKskPOpf'
        b'iHl2KqvWw3k0oBJBNqF8Zh4PZyV08vx4s/siW2NZqoxaNi62pvVHhFkQvhjPcj9UqRjjqRImfQSjUkEWSEB51B+Rwy7G7GfC4eVK4t+f2J8u9RVDowgKZwpXF64JqI/I'
        b'+vlEgYFKU8SAZYFK71gmfdft1JGJ1W19ElmOJFznKCPxY3MEF1w+AbuJvCiHFixnkgHT0OHDUS4LuW6PDm5DHRGQPujETvBgtwmdp0vPDTVE3QeNwGdvJ2p5EBzBmbP2'
        b'DKDzgUo3A0ypI0TYS1AmOOSzma4SYKHJBkvlRIJNUdAR2oMaUS6TUwNNxFRKXWfIyLMZXTAU/KaJIFtJnQ9OgzYqG+o5wQXIW+H4MExJCVRSaUZ/ZRrK82JLNx/1SPxE'
        b'aN8Y5n/KdgEaEIJ0howWrGFPQD4TKQ+EorYRfhyxEG5JABnO7mzZZ2Kp6PyQbJAwxotKYyLOJEJihg7hgaSEdQZvK8Sg1zoVXabUqTGb34z2Qy01R4bTcBYzN+S5GlQJ'
        b'/I3A3Ew2kWDx76Tgb2fqYjtcfjXKJCSKp5z409Ly5qEIiyj76YawFQ5PwSURdgZyhiuM7deNhiNqhlANdUkUXtmJKtXZvora5w7fWkfaDcOJ2XT9xGC+sX0EI6nO6a6D'
        b'/WvFMyyx6EfqhhyUqef1YNV4bPKs0EEpdCoDaFlplLBwLVjSsxUik4mhOUA8BVci4CCqURGqUuFo7KCZ4mgMg+QG/x8Fp/+VP5nh/mJ0VOYw3X9PhIolYowGtSLG/3l9'
        b'Ep4dCy/jSMB2IuhgcceEeoshIo4BFW40qIA1QTwpEYtCOGUkHketh02o03qe2Ajz5D/1CYPL1CZpXkOsK9amVsxqWOQilsi0TClzdW8gkvCsRg2xBv+gXS4VmAThiJmI'
        b'vPm/tCwWhCOrEcP43j+wPTnzaLNi2nxi32Xy0CDso4MJJD8sicmAwQR/T8LqUicw1CcM9QQTi39dVxeMbK9rD7d6vS4bZoGaOI7knkPe20R+uZBfJG7cdc1Bk77r6oKl'
        b'3XXt4SZw13VGGJ9RWydqh0MHhI3/6P+764Uh66NuXL0zmY/NOKWhK+ElvLXIYjN1JSP6n/7mtcXaYipurkdtY+4XbkXcWNQggaO+EVAO5x9utzWb45jfFG4wjLD6oA0X'
        b'/0gbrhH2Q+SEs+Hut+Fa7pvshz+boW7IcLCfNdNphqMD3o7bkpISUxKSlXifbqNeKS/iA+IC6tDTWIcatLV0NXVkUAgH4RAqQYdXrUDF6EiQlLiT65HJUFsKNXkI8IQ2'
        b'QpQzuBDomQG9y5khxD7UEeSA65/JwanAmZEcU+SekCY48MSYBJ8GWQ7oPPTS3IsdVzmocdwsDjVOmIVPq1qaexnmdeod8Gg5ctCFmh0TUCUrpQxKUaUDnmInzhg6neKh'
        b'ipYSa7HBAY+pMxaG0UXnOKhn0QIuYQ7oqAMe6NkcZjF6ZqODWsw5QKbxCujAH+ZwfujcHMh3ZD7jDy7F7FQHbroLiYXT7SKC/TS/xMqdDKgbB8XokBu6CD201ghc/Bmi'
        b'w13MTfFajMr9WRubUf48Je7TEjwU/BLcp1ZaCFT7ailJ3AsO9aH0pZGoP1kff20bOUeJ+7OMMO29yyJdaRmToQFVK3GPlnOQrbEcT00tzRwAOepK3B93LjHJfQ/qo82A'
        b'S5hHQaQ7Hpyb2GOslH67bhbBpuFWe3JQ7uC5YTwLapCpxBPagdvsxSlmeKEjqI02zsyVeJTFjfYmxdV6B7BZi8WyQRUi/qh8OFQj9/GGTlr4aKjCJ2AHbrcvt9LQd6oB'
        b'/XaPoRh14Eb7cZjZ6/OTubDBPoeOa6MO3OoV3ARUusLQn2a2CoZmoiRfyaECn5UoayPLnI7qNshwq/25AHfi3LKaZvbhoEDGExvYxO2rsFhTwSitbQqckuFGB+B53x1g'
        b'rUGLWAcVUCbDTQ7kVqMDgXBwBh06i0XLZLi9QZwOqgzaC6W0f5vQcdQlw01ezcmhdjW0wHFWcicPB2W4yWs4n9Q1bqiZNS4nxhHy8Ie1HFRor90CBcy3/wAcwaSWh1u9'
        b'jgtEA+uIYQgtfi7qM4U83O71HKpyWY+J/jIjtB603waV4ubYcph5OmyLjvkyGjkBrVCGSsUkHsb0VDv5dkZSvTDAMeOiWJQ7BZPDRTabddAIFagU16DgJsJ5hZ89+77J'
        b'H5WswkMwjWjvs6apowxW71l/VI5Kcb/s8YZQbU/wXrReywg8/czKIo2EvTpvSIchMXHVKtxICw72p1rgDaxTbk2DeWG6L1lDTQnyFHaoUEGiUIk572hDVCVGva4yaoK0'
        b'Hhqm4icWcALnQoViyEjkDNE5nAF35yDNggcqnzKKefZjSUFCHlII9IRQ6zCJQSB+mT7EzHEZajCahp9uhIxkwlwvgNJttB0NqJa1RWyAC8gjBRyEFnqBNgFKSDvmYT6V'
        b'5eA5I0PSinLURA0QCV+voKWcd1HYCTlEpIgy1Mty9ONpaRY6rA41idxjCYbQQwppms6cbzTidY4Z9TNKMhYK9amsBJS+gBYQi1p16euZUETagFtoJgyG31TaT/tkVCeM'
        b'kinPJa1ho4BOhtD3MRN6CSrx+1Wwj43mVKGbhug8bcCymeisgk6FGGrmEbeUx2gv5QHUkixhywxSf9hCNmfqmznWfshYwSooIncGZCJL0UkhjwHrwwodOtQGy83p92wy'
        b'yEcx57aC9cEIKmgp6qJU8gCOmOF+EGcf0I/nE+pxFh8nOuOzEJYEcBnrRw3mmCcMBBw3ooU4GE8mhVgRh9B0LDcLJIGqoZj6JtkBJdDHZoM0lI0nt1kYEUzvbNKq0THU'
        b'r4B2dIoMSiZqT1SRRtV22hgndMCWzTvUsrGneejAOIlZIe3joJsOi4cqxzw2LGGQTtcCyl6UzKxqCLCQ0ketqtNEsGTD24AuWinYsCnUp3CoBTUIve6NZEZrxXASBAJz'
        b'wxTgtkFYB0eghlmz7hPRyRNDOhm3RG6LniEcxjm2cayAy17C9NPn8ziLUFaCGTpJ2RMs0dRMEqZQtXLFHPRKhGHr9qSDa6PAR6VqbIWVx6E6L4Hej8TSe/cQlANVCmjz'
        b'p6s2M5GNySIN2hRt1DJXKB/SEzHxnxLWfQd0JzMPwc3TFXDWgS42MWfkjB+aQz+lsyiUDWSlzkFn6LxCLSUi2hU1fLDTWalAGahTYTfBdzALnhWyMdhAERutwvlQRzpw'
        b'0o1tUKpVPyWO1oLa4LI9eV60SZhWVgsdiUsTaR89JVDDNgxTEd6yNen7Tugw7WO8zk7yej+cU62GzWwMHFABbeMUvDn34iwOeIOmZIwyVJS+04OSH9RtFQZZjNJJDyAD'
        b'Ktm20YWPlsnsPEhH3TjPKOhR7bObhVKMUQ9tySI4aIFzeMSoyMtNGK0oKKFbw94xq/Ga3E8NBvDjxaputk+Ti2hH9dYae9FghyQkGsreoEHCzqVvX3ubspVFia5yLWog'
        b'l+UvjmzlqX2d99o1WkJYo4naj9Xz1JTOukC6h305xVjT9C5nSkzpvD+MSWJfjpIbarXw7uT1CY9Pnca+9LKVSAQ7Yu3Vs2PZl8tkuqmFPOaL7UNidmso2Jfpkeou7/K4'
        b'vaYhMe4TArgYwkBrG+sHXRa7cty2EOu31tN810ZpregWU9NAbdNFo9jLh3yMgmwxA4KrmdDqHcG+zF4mTf2NZ3XX6niwL18QizetY53U/lXPn6PWznGexuFfYqYb170h'
        b'fLUEC4ABy+iDlRqSCVMF68Lts41Z7ufGqvtPFbOWqiXHcrePVpJ/VxbSCuz2qK3rEtGn1tc2GXO3Hei/7xbSk3gbOqVOdjMunnOBE/HWKJ0ZNR/De0m5Anc5lajxz6VC'
        b'GRxgxseUlDJQNo8nF/Pg9xMburSRVqvJGbuN4lgXjJZMZp31WW3kuVbMhkV91s6RJo+DzsUIjUQJRo8sQtJgZKQsAf1xXRodFx6RqgqMpM39VWAkPa2hwEgEmgqtYXiD'
        b'9SV2v9Sa0MfbD85gLv7wfcGmRoSagnPoqGwRqoAKZuK5YC2HRCEiTG07vw2dhGfH1ze6My5GrEzCNU2+OWup/1Vfo5X6LWlpkTvrbl95+bsnp1vlmn1+8oZ4l++GsYth'
        b's8HUZt8iV7cJpnWLP29dF9Zh/5leyCul3Z9s3dCdGL2hIzzivadv1CrjA6tcAm+/e8DFdMvsZ03zJmz4aOW+bDNPy1MZVo+ZLJ744devuBradL6yaIzh7OzvuvfldWdd'
        b'rXhy9IanHL1vusSFjHNOkDl0519DYxevdEo0u+BR876O2eGGZ8c2iqcnOkU0fTTx3V/qXpv93abxEUkfmV8bNXb6c21Pv6epdfjKky6z4dKCp3b+0HfFM8mkx//uhZyO'
        b'4980+lSg3WmyKqML8YmTn+1+ouxGQMO9zuuOO1JKJ8w9Hvax4e31r9cU+8/6zaGo4IbjpNNVeXWmVZOeNcq8+2x+4p0Dz/l6rn2/0qBvw+dFcuWUoLnxsVknPp55+K72'
        b'EZ/9Vze8m3j6xxxFlLPdlZqoes3a7o1het+t/WxRfPqEdafX6ESpm6/ld78CvxwI/PixWwXuXwdesTn+Se2hmFWHYyfde/PwuNU9B5bXngma90XuG1/6hZ6987HNt5P/'
        b'+EbiUzRWtrNxkt285HD/ztQgWWFszrdVLieevHeqcOkxn+0uY/XLS/i0qRGf1z7RMb4q4ukZ8b+tkc5p/e7nXuOnDRf98qbOh2Evzsr4YM1Mn9bpS+d9/LT7MTVn+yMv'
        b'Xg+28D5W/uRLkvfKX0txzNCJ8/ih4p32qPkB8h/X/PzOj9Inz01ff6+z4HbGV/bTpq3/uOCNwmmVr9wyrlv1+rmIWxZdkreMdrlMfxO9PfDjtli7Pw+/OXrTjY9vz3N+'
        b'6sMdV1+e/oXOJscrST2VZVNvtf7ulRV7d6HVq3eyH9t47rS3/INj6T+cnXnypt4vBU92/aE12ukPfq3D++dnhcmZfZgDypOTIJVLKF1LOekuETqNOu2ZNiBj0VSUx7w6'
        b'7IAiibsIk3x/MLP4yRcbeaECE3QU7/pexJe2DB0Tk6tqZsUSi/o0SdA01IVlR11oEWuJZkCrgrl8aIiVK1ABNHtKOUsok4SLoN+ORfCYh9p2efnh4/WkjYeHtYeEk6Xw'
        b'mEnq2EpfdPDHa8zaklmrzVlK7dUme7Ayu9S34zLtcEM8UJMkWYRy4qE4SXCQVrdZYRuGReN8KcdDhyjIGPaze+V9xpSXEKzUUMcWCbFScwbmxIY6wulVeKLCtRT8IeW0'
        b'1Xh0CZ1A9exaPQcdhAwvag8j4jwtJWNEmElNV2cRMfJsINvLzzuBBlEVLbITPOOsw2xyvyp00UpUNugAKTJSPv7/1tDlr68P1f/hLe11LWVYaFxwdGxoVAS9rB0ge/Tf'
        b'sXfZy/lIBMcMD//R4pmzBi1quaIrtqDOuImVCrGPMaZuHXSpY3DiMoJYujDHEAbEMkZshP+aUTcPxC23PrWs4anFjBb9S2xtLGmMUtVFrwTn1xfZihI/HLwgFF8XR8dG'
        b'Dbub/ZvD89GgaQopq4+YppDLz79x+0p+njEZdgPLmK0LcI4IJ6fWjziOpJzxJomGdsoIz65aqrNxATfo2VWNuj9m0Cs+UmvQo6vkLz26MtT4sCs8be5hIbon+j784pA4'
        b'sMB18pH834R8Zt0P+eQfqEvqy2I1LuA5ifledcLqHZqzkUuWc8Q1SydUwnE0QBjJ1ZYCUtDS3WOVO1mkHlLOOU3NErqio/3c3XglUeOYLNzxRYi7dU7o85GWJZ+GbHi8'
        b'rSi9uCZrxv7GyvM55zOnVKQ7TOTiX1d753CVnGervkRX6kX9yZAwnlimOj+PHwOHw5lCK98KThBF9pSND3NttBBOq/AXD7kUvi4L2xIRtjWYcip0Gdn//WW0l7NkvvB3'
        b'Tg4mboyDiUOEIYusYSWriFoUPYyk+RGU+8kg5X6MP43WEmLU/k3K3cfd1R1OuzRCbJ0V5BCvYjY2KMsdDgnAjAeMqQgcyAcVqEEu5rJOB5HLQxMZqoJ8PYaQuwzZcNTL'
        b'moSuOSTZhdo5tXG81lY7ds9VjHrXKlCJL48yFnD8KBE3G9Uz4E0Ui/xqr/am1qqxK0gMTvLCppkiL2+8lnrRUYIw0/Djle5h9IWgCBlnxHEa9ilf7ZbEbOWU5LYpI8bW'
        b'ZfcqnW0JYhJ0hnsfKDO9QJ04BeVM7S3UpcsDbLgYMqjrR0tIfNEttWqc9rU175tYckrCPP94OXhVYPIP28VPyzmxVDStpoPWluIsFBEUHaQmcuKUBMgrtXjlLHzIEwyl'
        b'LLmI5ntymjpZgfr2FofHvhtjxPI9d2/ezxofSgn6V7frG6Ue/urbZ5M//JjnLM5wFpzJXKWSXK1d2Gi2KlAnRWfbx1MCMHNrIyoLdFCS89Gp6whV0TZaevqIN0s4w/Pi'
        b'j1oO072dwqpD1pS+pnfF+tZrV/D6URfxM3M1ab0/cY+n9L9G6IWTj3mafnV6YqmTxmt4oK04q++j6Fdxdlkf2edhItrIbdSMoK17b/6svFcwi3CKu8Xtf8GPfnc1cUPe'
        b'KxLu4gfch9yBfepULFSmEQWmB8H67MfS5SEHCacBebynXmr06YwbvLIRl7rqwN2l/k/Eve6qfSFq5hXvlHfcrsb5v17YsPPGk8u5+WV6bUFWxU1Obg3qhQHypVXzTX98'
        b'XN1878t6Nx9/ZtvnmmntBkcO/fDbb7/d+fnKvCee1i/Z8f0oDTOL5S/v/2Nj0zL3OGjxilvSPseqZPz3TwWsmlEx8Y9dORb77Q68sGW66fSERR/r9e03fyxgt3O960DH'
        b'7pdcQ12NdiUZLvn1gvkz5Z8bqxnKgvprpWNKx9r3Su5sufbc6tGbr0ybmFT3Z9U3KKX6hc+X57529vkd77k2B+QoAnNPzO/RTXn73G1dmBMX8sHS9hnm06/l9Tj1qF38'
        b'8pNlbxza/e0GHcvHFry1w/YaFtb+NF3Af/zHed9NXZC+W2bz5P6vxes3zbL/rL9g60q1BLPffmoK8tvXPvGz75tnq78xdkzpz/2/J9ukWm2vW1hv+Mv4jtvOHbfn+X2q'
        b'9UKTYl2jYl1k9cyrvy9d9taErPHty98LfbO+ruPWb19lH/Jc+vbN96oVP39lavZh9+nyIP/5z9R3vv+M+vcpcOf2iveCc/4s/FpzwdVdtw6UvBd8wPCTXYo3Umd9oHdq'
        b'U1nbwBXbbWG2Zz4xgA8XvlBZXbDrI7k+8zaGt+FILzkxBlSLgZOcWhRvFe4mBHeDrBTqGbIAsnUI0E8Divh46NVOEjCLl2frLCd2Gj7WHCeZIYLm8DGMGa1GTaiW8mEe'
        b'MycRRKc6freG37NTmxoYx0C5uTIpJWUGtOnoQoGeHmrXTsCnJjohhipUYMG29QIZFKF0qYozpWwp3ksEn5qzd6I8H2jmDOAC5iGzRMvhoBO1ukCNjy3ALCLlAXfO5dT8'
        b'eSN/Zs2yhrC/wWkq/pBxhycDKaPrjeqxVOlpgwrGmtHqNGU8lKJDq2hbliXBAH5Njh8TXEM9ccY5VRtdpA9HYbazXgB1pEEZPoKaeQe4bMAGsSXQmRR70MNbgprwASWD'
        b'8zyqMoE+xvBeQg3Q6uWBd1gSGIwO8kY+Yg0qYGOwD7MYdarDLUzBqeGjLQKdpWMQjfL0KQTWW64GNeM5tbm8kXj6f6mn/jeGvyP4zqGzjh6YFf/kwJyuK6VhZShvqYt5'
        b'SX0hUj0xITCl3CHhE0kAGMJjalOXYczpGMlJuE01ylUS/pTwlcTWmsdPqbU1MxYQyiccaOLtQY5Sel2yLTRpy3VJeGhS6HXNqIik4KTopJiIf8pjihM/I2V+Tn59Onhm'
        b'k3qM/vGZ/eWk4Wc2WTdwFgrTyIqV42N76MxW54x9JEZoIC2MF7g0yXCmj/AsVFcsihQPIvv5R3qZiLyf7ZM8wPZJfOWsUbgR2dDm5UdsZOidoIcU88IFeGF2iVFG2pTo'
        b'kKDFIiXZFqy9nvB69ouQT0M+D/EOvROhFXkjRsSNbxVvWx41zC+I+C919Nd1yLyMpC+rf0JfWxK/GJxxCZufz0caeQznuvj7p5G8HPiPp7FFf/g0mpMRy0KXoX0MlLBB'
        b'GzmV0xZLA7ZC8/9sKh9w2iJ+YCrFvtG/frFASsMAVH9jz2YoJnJzuHuoBvXdMvm6+OArHqkn/uYsKf+7WdqaeOf+WfrsUbP02chZIi+v+cez1DRilojkoB4bkmKl8H3I'
        b'DKFqaQgWM1oePkfE8iabzJIoWxIp+TcLjszQg3EatHxZlIFSlOO/GjWrWG7Kb6MD6DJlSJ/wmsTvkmyRa2+7ubfbrtaGfrk5Xiww295BG8evYxe51qs4woKntum9Y1Xn'
        b'uJO541gOXdCwClqIwtkT0ylRJ9Sa0vx7fdQYqxvkuPKDSBeOeeKoRX0LV9mgcoW7h5hzgna1tbwICwfp0bMWPsUrd+Is5oq0ic/P1QV7oyWvVCYseE6t6G23crHUx1NR'
        b'/Gq6peUJhXPhgWmmafUVnT9teTpwxfEXvil/LdBkbWXl12VTrBQHHAyczAci0YeJ39tuXelWcj7r7WO+lhsnPPaOwU+/HHjzV61bX79y7M+n0II7p8LOfHPW79dZm2bE'
        b'LpSPnnTG5CW5Brs1O4sO7R4LxxQ2lkRboQZHeRtUFk6PX0MotmAcDjl50WGooCyOhuAbFnpnWFI9B4kOLOI0NTXQIcxrxEE6LXkuSrcavP6ydWZwzSO+jClA+1CmfAuc'
        b'pZwIyhERH91my0zpyR2OSrQxU+AfOewSa81CZjtbibogX+GO99HRUI5Jy5kYe6ejE7TUifpQoboeMwnBs0puxyJQ9wPLES+ch51RQ4tUm2yl28Ijg8mxR9fogn+yRuPI'
        b'zYyugIcyoWe0gSjx7rB1G0RqkdwHK3qgmXzil+SdIFW7aBHr//HqrTcYvnopCqUczk5n+6u7BxZz3em13mSUJUHt1qgOlULPiF1RU/irNL4v3leZuEy7TD2SD+fzRfS6'
        b'hh/ylROpES4Ol2RpZIrWSSKk4dJwtSwuXD1cI59fp4bTmjStRdPqOC2jaW2a1sBpHZrWpWlNnNajaX2a1sLpUTRtQNMynDakaSOa1sbp0TRtTNM6OD2Gpk1oWhenx9L0'
        b'OJrWw+nxND2BpvVJTDLcq4nhk7I01o2KkEZyEaMyuQLRulH4Cbma0sSb1+RwU/zUIHwKvQoyu67uExpHzPru2YyIMkNCU5nGskcs7tbIKDSYQyT784j9cvDSitggUkdE'
        b'1JCNDi053zQHd07JX+6cYnq+Se5l/sfgRiNaOBTc6K9CCZFFwaIZkU8kaFEoK2LFkmWmkdExD4mLNEhNhIw1Hti9J/nSmCpB6IQdXdwk1omfDQ04YrfSHVrQQWtbYq4C'
        b'h5eL1J2dUDOLotHnAcWybQmr8GNV3gCN1FkpOtsCSKRgFh2WCzPV0IZTy6glz5RAB5S313YoLmxcPL2oMY+PUKASN+KvYyjqKxYlmLVBOj5WjipWQrunDwsOrRBxhtPF'
        b'6JgryqU3M+Ogzd1rC9TO9OQ5ETrHoS5/VERNhDYnoxwvglRWxTSG5ghao3QyOr3QwstW8DYvi+fx5nYY1TKFfLl3FN1WCTY2z9tHFAIDnC6qFruhUm2q8o+H1jQvaHHH'
        b'DcKvOys4vaniNWGxzMZn9hIvqItmchHpDHTxacR5DFPlX0YViV7QjHI9fKxwDp5eU+A+Hl3P4uYM4GPtLOpbr4rXzVwZjYd85pPKxw3lbYWG4VG11byZT5oTcBIKvVD/'
        b'7MGI1GJop73V8kf1KI9Dx4eHSW+GDNoiOyiGEk3oHxYqnbp0Wgwn6ZXVKyIS2ojT/3VxiPfP7ntZGKQdqGjjKs4JVRArrimY7b9AD+Irm+jdFPeVR0hM8tKx5OqMKPUD'
        b'dXwVqJEgdu5337RuLDvAp9Art5BpfEjMTKOFLHwSKpkHnV6obe7weOdLoIwBCc84kDjEg96knLH0S4Oso8OT2PGfgcXWXAUc2GkrH/IohRo1KJv7GOr3VTzMLZMFFmvx'
        b'mSaNFLvQYvTDoJmQCZUe7PgZ5pgQToo37omPtlFz5JXENNlNNHZ3SV8cstde6lF5fsLt3y9e/+BZ9aQ777fkjamR+p/MLF256fOlY9d9ZHjnzAdrc1dOdn3H+vVLksaz'
        b'YW+XvrXJsWndzo2Z+0/tef/e+7rrvu9Fp4xbMt6P18t5Si345embnNdkZv5+N71Za76604wbHe23V70ZfnJRSvP62LSNL1d+GpAU3Glc9et3AW/W3NGu/Wr5wkMLCveM'
        b'/dQ8zrQvbPzM6a+OTVlzChkGfZXy0dfyiOSvnqiZeGzFdLVJRtWrEhz2hJr1bVmududd17kXZH13AlrmPf3l56O/+Gje3ZLETwIqwhyjLhhfOFga1ZW063acf+vPik3u'
        b'n/QWr3N3/K18Vv+0Oxe3frlh7Kf6lT5x72hETCl7y9ujwLdpZ5jnZs/A97YZexg/ZV1ifa/Wes2fSz0WWn5mNu33Wmuzjy9f2eDsL2usLlv6doTnvbp3P04MfvHPzUHj'
        b'ZNtf3vsb92PYkR/4U/JxjMHphio4jicJnWQHJGM3zqAaBowvRzlJke5e3la27LEshkenp4IQSv4YFGviNVwL2ZgXZdf5JJLtbqsVFBQRgapQpmxkXA+FNonsgdpQDwPv'
        b't6Jze2TooAWh24dFHqiR0YZsRW0wgHLgMtGx0K2Ncr2XdjFPE0XQI8VC1TF8zg/ubzIlj47C/tFU96dEFeiUl+Y2P0H3BwXjGdK9SAbVNIrH4K5nDAcxV3tC4oL240bS'
        b'K7Kyxwj49wIU+5HdTxwjCoLTm9gAZVtq4kfN6Jwf3f7EqFoERVAYQJ+6OqJCEpmBbYDQp04jbqA+XQrzCTLE2wN+dy2BSQ1ug5yBsxhq9KCI4nXCg6ES8uau9xvcBzmD'
        b'NDFm0ntRF61i4TzYL0ql3kyFrVC2Evd7kiudoQg8YOWKiSR8gbARyqbx6CSWXQro2wZQg9rhjOmQAwPivkCicjhyBG8Ag45SyZ6FWvw4PU1xUnQMo57GBXAWr/d6monu'
        b'H2oa/Ni9qJP5uOiCbLQf8rZusRvmkc4AnRFjfjZ7HqsjC7IdMZl1UlgW3UNkmIRQlxUUUB5bb6c3iZTO9mnN7ZzuYvEyuLgziWiX0KlZqJRJaA/bZnb6uCarj0K50MWq'
        b'yoQSTKsk4otwbgajRk43SuyywYWSkWQDPiLyMB0V+g1tRpzBbDH0O1pTit7rQUzu4AjkDmcqDXTFUAfVmnLpX98Laf5bWMKgJ/+2f8Ke7+W0tChzrk3Vrxoidq1G8DE0'
        b'ejP9IY4DtKhCl1yRqYm0JUYUKaNFffyrvmU/2rw+Vez+k/xaop36Ar94vwN/AWHz6UixXuNv3zjy7FWrEcO07R+LDSUThmNqHmjs3/XS/y73SBfaL+B2MS/9gzUMOug3'
        b'o27xBb50yFX8v/HIL3h3Vg9WRkfFPdJH/suqBrHqVT7yyXuhScmJ/87TtSR488zNj6j0tcFKLZfFhEaZRkeaRiex6JxuM90Gx+Df+E/3f/T4vzlY8wTqxToxIjw6KT7x'
        b'H0chEBymX350yINrg7VNEmpjgQf+tctyzeDY+PDoyOhHTum7g7VOp/7oQ5VJpuy1sH9bfZSq+ojUiLDkR0dd+GCwevPB6tlr/67u/8fce8BVdZ8NwOfey94CAgoiLvZQ'
        b'cACCioM9lKGgKHuKoAwHLhAZsvcG2ciQPZSZPE/bt/maNp1pkjYd6chq0r5p05Gk7ff8z7kgKGb1fb/3iz8N3HvOfz57LsMynyT2eTO/tTyz+RJYpa9AKYIvYYivOX90'
        b'TCSByufM/7vl+TfzuMQ///XK4i/f9xKEfs607yxPu2UVTP8n9fgVl+1BnzPx+8sT71ipHrMzX9KNV08unZtnYk/HoYiW41C4Ao60fBFp+Ryv5Yt4LZ+7JVorbY0N9awV'
        b'W+E5MS9foci5tF/yJ8Frdt7l4etKfAzfnjg9nvV9fgJlqTFCawS+PXBySvqzBoJVRoKl63jGEP/yuRpZvoj9pUMGQhH7XyWVJpOG2yP6UVqemYiXVCyxzXe11MoUeB0m'
        b'te6Ne0519bCltF2+ic2XFyRuc/KZm5f41vIun8SxxMbFpPt++ZLrbBl/VJLmMH5pRp3FVa0svZ7BWoGQdpAHj3CcSXNKDiTPYY3F8olgxdNhLKwIBQfzcsok/Y6E/u95'
        b'yp4NkKJb/ey8jQzvXjlwboq5V0KbEmP/EF4cxztYXua4rY8kvZaj0tvFcS/oW329xniPv10lly/yvqSGf+17Vv78e06LSV8lvCWvvuvVPpknTywv6q9f49aLV3llmJDn'
        b'BI9OCXcOjdD8hbdO2gG7dXNlvKd+3kwsRMZX6GUK4CADrZirLoJeUahQ//gRKUQdwkuk7PjYiWAcShISzu6YluH9Or+YPHs+zj3KO8I7IvHXD2Li4+LjvKM8I3wjRB/p'
        b'nddL1AsIlnN5e6es3cVYjhtpUfhp0/1nosvWjjRLDZaCjlAr66tcm0RFXk2cue6Zq1uaec0remrmD7/G3VSvDClbY/61qTHvHRPKznPL3rEvosnMxuvzDEE9wiLo0gSO'
        b'TxR4tYk3zSiN1NQko8sRSQnRn2OtFXFr8RI530BX3mj2iX8mpyDi7FWUjS6/pjydmPCj73wgSQujb17W/tP74d+LNP29Z4RK7Dv0k6WmpNL7mL+Zd/iBtFGd8mizH975'
        b'KETJ+1B/4gbH+kQ9R72mhkKnRD2dEetornCnZfiZbx9HoxfLv9kKzd/1l/xDW/6HEtu6cVnuRzJ6Zw1mzBQEpXXxMDy0eKJshrpxajAlcYMelNZtzcWWfRZY6s3KwDwx'
        b'7OL8UWndRazX4eNHZGHmianUXFaw4Nw5FPcEe3ShSGr0dYZ8oVQLdm97YoIV4Thvg7W8IXTfhJKzgvmZdTrowEW4fxuK+Vm1sTnJgtDQAwZlOLkknMdF8VZWIFxY0xw+'
        b'gB4v+tJSjpMxEOEM6dRjGtCzxC++yHelkJAWxt8rjzBHvyrCaAkV+vi/fCwzKz4hs0L/Wxr+eWxtzfWt4nLy9OKnXwOn8jXXVEiXF2SmtVZ1hxVlHHhH2il2SBJSx1KZ'
        b'GTn1NVbVQWFJiXhDYUmef0NOEI3fkBOk1jcUlsTINxSWJEGeOvDbEc7iP+92uILy/JEWdp6dkjf9pkBQZBr6nxdXUFNWEfMehtStrPTRso9ECUrFrLwTzGIeDq9i2ZrS'
        b'/6fdedr3J1etV81Fi0uYR0w+XzVfM18rVvbL+/yEt0iWUI5WuavAfH6xXIwC72VTYGNHq5aI+EBwZRpXJlotWp0fV3H5O1kSWzWi1/GfKvGr0YvWLBFHb+ff0eTf0o5e'
        b'f1eRvlem7zn2RLU8/dGL1imRi97BV4mQlXb2UM1Xy9fIX5evla8XqxK9IXoj/56KMC79UahWpLXql0iijXk/pyzvjGMdatTy1dls+dr56/N18nXpfY1og+hN/Puq0vf5'
        b't6vlow3pfRN+TvamOv+WDr2hyHsT2Rtq/P62sP3RDsTRW6O38TtUj9bitRHTN9SkkE//i4iLSf31brqYVTTcxWj1E4zw0//TjCKI5q/kBMz9F5FuFJHKzCuXMhIIwlcN'
        b'FEviOv98NH0Vlc4UuIR0o/TUiOS0iCimvaY95SX0SCfOkpIqnWp5loi0Zf2HWFKyUYRRXMLlmGTpsCmp154axtra6EpEKuvx5ej4rBuSqVZPbXCZox0+FuhibXQ0Jdkk'
        b'3SgjLYbfwcXUlOgMfrlbVjtepYYyP+Z9XZmNsLqUyHIZEXbty6VEJAWS5+YhSLnyr08/fTH8ET3lfF1iyheWtvK1/K/LJ8l0MLrOlce/prLF7py/qmhrIw/e2hSdQisi'
        b'5cwo5mpCWjr75Ao70UipmSZmDUFBuiCpXi2s6Rlt+0oCWyR9E5tBw0VERxN4PGdNydH01yji4sWUhGSacKU16nOkFHZ1z2Z5qPpmsKCNXSyjuAhLXKBvqUan+7IBGyux'
        b'xJsvpunv7u27VIQLFjFfGbuhAVsymNIDdTE2K2t8wl2VJ0PQi1I36WXMV7yJ3VjNS8uxZ1glCRKW3WU4WRMRzJ0mWQPGhLoRLSQ5DwnZpzh37CrmwijvCV0PM1yAFfbg'
        b'GHbbhrhzEmtO3Um8HYqwnO9pdA5KIWtlWylT3lt+3N9xH2smtc9MFip0cVyornEfB/dZiFmbDQfMToMyF15mEyVJguekScfvb4vneMe7POf7xMXojwV8v6qSrbqWWOoj'
        b'FCc9kSKPWQGQI2QuZGGVHlR7pV2SZRGOHBTCzN6Ei6aPRWnfoK97R/2PlbGgJpW8272q3XOb/XdouP1ac9+Ps2SSLBsKZTQ/qLeuftHyYu5vHQ3y7H4VHTHyu1+WvbK3'
        b'8+ie/peOe12JrO4/fc//RHfMW/6vtrY6fqtx0mMuUSPIJLC/MaAut+CFe7keZz623jj22xlXZXXZwx9wOapT9m+Nlf3occ2NjyvPgpnGX8++WlGuGLFB0Vn9p7r6V+s/'
        b'FJd8EiB+vT8t9VOFLWU/TfywOU/nLTeDz+rvBTk8vtV95b3Ynrd/5/bSK6qXv7354OZfHfzBQLuZtlBmvQFKnFiI94KN1H+v4MK7b4KwXh6rMPspDx7vv+vHekGAfExS'
        b'J6mr7Ti5ypUOC5pC7FWPm7nFkmcRF6BGBENn4A4vucpAp5sXyY3zq72LnrAgSIntUGy6omC9w2koE8Fo8kV+YLdIepcPmjCT47h4RW0xtEO3Iu+lgX7sUMEi4vy+dN9Y'
        b'BcOW5nIkNk9ITmCnEBMWa7jdwgYLmVwgBw/EJJFWWarAohDrrcaanix7NP11eZ+mn6qwoaLNcJdEZjoqmS14H1pE0ALdMfyK5XAKB5aL+8OgmC3ETh9KeVcj1MFspIK+'
        b'1NXGV7cs9rKS43RhSsYdZxIFf+IwFjxxLMlpibEZFlXhjhbf0NwZ78BdVgvPi1WaY2FlBcCWuA7qJFCmBS3pQi2FChxiPjOG7RaEogzh1QIkPm44nM6QHYth7Dq9Xsrq'
        b'A9zzw1J3GE9hAeilNl5WfBFEVsDBDUbloQy6sYg/FcIN2l7RckzE5UOswUO5nlDHsgbmbwTprC4syKoKYm2QkIXVvQ5yEqGY5RvRRPykLKmI06GxFqEF558NDfsy8dZr'
        b'OcoCv6o+4MCERzk+tlyNjxJX4dtgs/hyQ147EFxambqrOfJzmlIv89sVCsPnOAYlwrNruLP0lWkzjl9Nf8ji3l6ZpPjcJX9Zk7DsF5mDnZSl5uBnplp2cdkts/Fn+fYK'
        b'Hv2fdKH+Ife5LpmDS4v8MsbyJZa7yl69U5CSmHQk+ZIW69j/zyzWd0kOy1hLDmP/rTJap8ZcSElfbtpLAmV8SkZSNJN/Lsek8tqhUURcBBPP1hxrOZDuSFJMRCrrBHt0'
        b'WSaTWr15+ShBkP+Y7SWDmWLWHCwtJp3JdeHhgakZMeHhS44b8/MpyekpfHKkuVFSQmRqBA3OvISXIxKSIiKTYp4rVqUv92Feuld6LSU1IS4hmYl2TCh3i0klyLtmaZTC'
        b'juNKQtraowl+yeUFukYkpdEKv65F/6Z/pdCWdt+Q1ZJFX8QpvGDVI/qR+AUzEU/aHaxsnqWNxJZaePpYgtX/41b9sEzjpzA2LSopjD/4/8i4f+Rrka3FVeZ9N3o7FrtE'
        b'y+o7TrIfvP2ssNKChb0v7l4+J6xd09KvZ6jmDA+h43Ni9HkbZL7oS8fox32xqV/GlzdSQ98RVsReymFdL0iXyiI473mbe1pCf6AQzMk+8PNmYT0wAPeUHXbDYELaxWku'
        b'jRXIzzO89n64teZ74S9HmuqYR3hHJMUmRf4h/J3w5Ng/hBfGeUbwkLRowdWaKths2GomSWeEwzgBR1Yxd56znz37LG+/dE1odtPgIlZeM/4K8qNw+BgIPVoCSGcYYTC6'
        b'XutZDo4tsUu+gc/n0sveia9s5o5knPhLwewXOCrWiEFfw1vh87XAeHJVHPoxejsZxgyeB8Zb8MHngDHvhdA7rOZhH2Im5hUuqIX8/VLPhTpUJ4uglwBoSHBdDOK8vdRz'
        b'YQczkCWC8Y2QnXD6NQ0RX+TgwINHT7sukuI8o3wjfJWaI0QfbRDcF7zzokfEfdNcMWzW+lnnxec4niK+9tWeUlHSkMnUe97VPuvI+IJVHP5ad/fCSl/T81dDBI8ZWdem'
        b'K+ygWWA90RVZoiyyy5RF8rkx7Mzn3PMMe3EjBhSxJB2ttGk9325yITUmVrBRPBNTtIZpIzUmPSM1Oc3RyGW5hbt01+FGKZGJxNk/xySxtkgj65vBDNSWrgSPRVKoDzp+'
        b'yurkKT7ePXHrMxHvWbsVEyOOZbAytFDnDvWkpVvbrDJeMEX9iZruryyPJdgdlBDw6yaZNFaoNmTirffD/xD+XvhLkfGx/busYpg3JviFYBwpHw3uvmsma7rtW99/+bVv'
        b'vPbicUnXeQL08frsxJCx+vGGombP4ID6Q2N7il9UabbiqjzW1bzwOzM53r3hbHBjSXPFGixhcbFw31bQerO0WQ3KVUGvUIntN31v8Q5cL6yHaaY2Q2P4U5pzsp6gdN9J'
        b'wxyhia9U6Xbayw99ECdxyMvbl0tYMtUonxaTOncfu4WA2RaoguKnyLWX4ZOA2UW7Vfj6fM1jZZULlgskBRgegx2/KgZfFOIKFfhWRZkbn8KdFcOvjv87uZoyr+1XEQuP'
        b'PZEydGmIwK+F4kPaK1H8c5a5NnY/E7XyeRKDVDL/ZHJNvE5/NlYoJXYpyeR/H81dhDm/BJqv7R8lsfZgwj6ZNGYnWmc/+X546Avff5HQrbY9b0vRLr5Eiw3I/Pvh9bv2'
        b'ZmLemkQIjD18PhaW+cSKlrwyG7FFJhPLd/IWoS3Q7em1MmUjFRogG0ohe0nYXNuDrfy1Oc9tjkWprgUI0lv5XHgVPQdA2XqivxaAtqp9EYBK1yWd9A35tIjLMWERab5r'
        b'W/dZNKyUG8nx2qvcl7Ttx5FOGbmWTrkEvMzZES2tP/+lQNdl2TETkx7BQgIjhLCpCymXib2xivFL4/5Pwb3wjvSAHJkLgHfJWDL97kJGWjrTewU8TEtnOiILVWR2ijX1'
        b'PMF2sSrMjemINPhaToNllGNrTY24IhwX7flzMI3B0rM2fiXfDCZUmOJjaHuKo1rAo7WTyBhLNcQmIdilHPPcLDzFOKDLidw5YmV9OMWXkUlzthTqz8gc+A0n0yBKl2Tw'
        b'5vON1/n8Io08r3BvDf+NXCBvOuEN7sfgkaKFn3gzdnMifw4bz9onRMkmiNOISXKPZg/4vNyuBoc0ZL7/+uvn9VVcXP70mYbRIaNTQeLUV443DmLnh/+qluRu2FV1Lbv8'
        b'HVfvlxU2nfjGid9Nzf5oe3SJh6Fmup7JQm1IaOFJBYfo1vDXfpNl17yj4XT/3E67gfPvDg5U/uSTH14/o2I3/fe9vj/1ue42s9DZrepz9p8/fjHk2J/+aDh69RYX9G1j'
        b'5yP6ZgpC1kYvLMpYxCutyGs5D6O8EdfXPOAJ97bbKiStHFLhjcfaLjDLs+6h808bvYuhR2DeA4HJFhG3pUZgEbRswVnBelsF2UoW5tJkCn/o5hT3i+G+zWGeAhpBWQqz'
        b'/m69/Kz9FyYv8iMcgG45LIIa9SdmbxGMQkUoX9lEZAp9FjaWak8M15ZXZZ7DNeW+rOH0DXlpJjBPQd2/OgXVUJGW19DkY/41+WwDFZG2KFNnDfpFE622l/K0c4P4SwgC'
        b'khXPPiG2+vRrytcitlU6K4ntcxZLB+m3lKH8huJyiLwQF6EgZjnOSRHJcYGuUfJSPGbb0FzCY19GgFlSKzMeKvEeceaFF+er52vkS/LXSR2vmrGaUsIsX6BIhFmBCLM8'
        b'T5gVeMIsf0thBWG+JbMGYXaJjmax9MkxV1ZHQjHTmODdFJyxUSmpqTFpF1OSo5kB7/n5rEQuHSPS01Mdw5dVn/BVZjHBbmcptZYtGxCZu/2ZwSKe6143iopIZoQ4NYWF'
        b'pCyFEqdHpNL5G0VGJJ9/PjdY5ZN9Spha0yP7XB7xeXyFHQRzGaddjInid2gpnPKaXOJJBkdyxoXImNQv7V9eBixhGU9SMa7EJ0TFr2JX/I6SIy6sbbtMEcyoS+cQn5IU'
        b'TcC8gvk9FR1/ISL1/FMhEcuXlmYkpJJYG/kt2UuF12PS41OijRxjM5KjCDzomSW5OXzNgZZWHxWRlBTDzM2xKVJeupwzLgBBBgvUZ/EMEWuOsxKGnnuSy/GHjkZP55k8'
        b'idFemvd5sdrSsSJtI58dZWW2yhe8zygDCR4BfkZ77RysdvG/ZxB1ISSMjlm6qqWxCPQFKFnb0Hw0JjYiIyk9bQlFlsda88ZN0oz4X1ncyTOLWyWdSCGTbeUi6Qb005eQ'
        b'rZaFFnUpoVsttJj48tnSMIN52mm2RO5Fu7EqhWM9veCeYK6qwDkcV758ScSJsGs7FnDYjNVK0jKAUK5/jRnISDW2wBEoFR1hVdqZdB+FdU701gn/w4LQY2ptZYoFNuYe'
        b'PiT/9AdexLH0k8f9WaQAVJsr2kPR7QzmAVLzY0XInsQ3uAtaxpPIhigY8jynAO02yUI18pOqnJ7CG/KsRLlckg7Ht03dfpavcc8iE8r8pcEJQrqppZmVpyznbCGHjTi5'
        b'jg+A8IfJ7RZYyfrUlxxZx+qotG/kh95tIsep2A/JckbhKj/TdBSKsTTsleEU4gvF3KFw79djo4UPayLFnMwNK1ZRU8V4lxcntG55JIN12EmMJzxDmVNOUeFrbwkj71Tg'
        b'NNxPyXJElVM9r3EZjCPqw70zWGTl6RPgztuEPWjhxRaXApnQuBxjQV+5W3p6W3tYmctxWGSmcmkrVmTsYfc0nkkC49OWnGIzEn6gL1AqcprBA1iU4yAbHytCp0qIq5mC'
        b'0OKiGlqurPAZizZCPTRBP8EAgxe/fVDjJeTRO8qdE9lgiRIPNuY7IA+LltPo/aAROoxOC5n980I463ISvRfksTx6kq14sDqjesPrSSY7zp6AGRjCaWE195RPrkhm59SV'
        b'oYcls6e7Cpnw96APKiyWEtlh3ILlsm8+w1cTibfA9jVS2YOghM9ml429wpkpCx2EJh2V+PPmqy9sT4WB4NP80q7ePGzxpPiC4x4WpQt5p4RE+yxCjM4nkbi3rkoDcSHn'
        b'NI8Qx7EoxosvvbANivjqC9dhgD9EE3lNL6HyAvSYR4p2meMoP53Bfny8XHpBJVMovtB2Wihb2wXttquKL3Bq0HGWL77QCZNCc4hibFJ8EvvLqUMPZm+TBGMX5vJJ+yHQ'
        b'Zur1pAADs1+zyOL4RP7bc5twckVKP6fmFspS+uPl+W/1sQ2qnmj6OHaAr8/g48ffRAh2YCOLEfK3gipsk+MkMaL9yVjDQ4DbTZwKIJWnPOg4Cc9QBj1yVqyVfA808ZUU'
        b'DhqQ9pLUKyFMsrQ4uYvjj2/7ERPabpWfDCcWQ78KKxDREWemJJQvG4rG3DS11AwcVUnDRziqDoU4nU4XkCjxgKHMDNbQENvxvrL0IekTaTiRoQYPmQmjR4ItOHycL3rg'
        b'pIdFwoNQByPCw1fSLymmqqrJcaYSGbzj5Cd0simFhUgcz8CJtEsqnkGXoEQ9NUPCaRlI9p3FUr718l5m8E+7lKHEj6KOk07nFXGU5lWhp4UVyHIHz8nJpkCNsJf7XjAk'
        b'fWEDVCwtU5bTipG4YLec0NVjBOcdlke9km4IfdLlGcKQjDF0hgq15u5rSZae6sYW/lBScYJWeEziCNMpPJRomso8GYlorxynEY9TcmIc0o4VCouUwqCpMk6l00pUFFVT'
        b'cVQiy6neEhOwtAmQsgmrUulCjx9n98nBrCw+FkHFPmznT2kX5O4J8MGKAKLfNQFQQmRSnMh6bE5BJebxU6zHKlhYMQWHvdIpjGjvjKDcMIb2NJxSJ4VBjD0ibRlz1vEz'
        b'g8VPq+ICETwiil42Pt5+QYx1+EvVaUtGHIs9vLHQA7Nuy3JwJ0gxDcc2C66YfsxC1kNbwomsYNqRaB1WYRZ/cirYpobj7kQuvKwIwXxhGltluHXQLKH7nIRunlhPm+lz'
        b'u9N/K+E0wm8cvXVEoOBuF8y5QNN8EX0Y+W/7TE5op8H9/aD0B9NDZjIClelzwjIY4PjaB7XXuGv4yFb44i6M0N8BYsVbsDCTy8QJNYFvDEHTaRaPpwJ1V7mrZ3cLEXR5'
        b'8DgaWYMqGNBJ4BL2WiXMcz+XTTtP/CXnN+9d8N+frO2i8fDDhjf/8cfS27OGP/t72T9MdNolpZyc4jYHyw0JJ8dORpm4O9875f7BC7HqvwpvPKJh9L0XTigUKFx70854'
        b'a33jqY/PnTp1qsawNnBTYojSa23VOgnDb4TvejP6pV+UzNnP/eW16f9e991v1HAf2Zzb8mraue/tvtcfsOn9G8aPDra/px36q0faocH//MFh9e8Y5tv9I+Z0VUdPygPF'
        b'P+XmJbZH7bA3L5+tzXTJ/5vhf0W9Zuz/QwX9/WMmUb7FGjo7mvf2abqm34p1L/9eo+hP3y8vWTDp2ZfubfKNhp+kvpzzyhh3peW9wL+lO2pppVj3i8wNZwo/LVD/zg3j'
        b'835xMb+wNH1FwfTc4Yr3J97P+qVlR+rmNwx+PvpR04652Ne/H+r9y13vZv+1PKbbINtlYtJ77lcdUXG54wPf0/nekMPsh3/IG1e/+t/WRxf/K9lcM1Hx4V3/wybtlQ/z'
        b'6j6snPlp7OCnH4QE/rWo7szgJ3GpR8M13/70nYwXLD540/xXJ1xqp98paKvwXXc4+9PAv5epb/rlwuAfP9ms5/36yV11P/rp2dyBUsWSR8MGoS9Ffe/qx9ZD2/7ifXI6'
        b'tM2iaU4u6MNUt7nSn+/udHzVUFv1Z2lh1zp902X+3VvaaHXkpxWl1tNB/t/ffugv+37/0SG38IIPQr/3tw9K3kmL7v3s4J6Uc1cWvlX6kz7PDwzfuP04LW9jsuzFn/+h'
        b'v3r6apPdb37aUPgd56SP1P716Zyd8S9+5/yLxXcj3n/r9+3/j73Zz6de3P/9hHzDyfF35v6rP67iZw9MLne+l41+P+F+9ruzn/1dZvFarPPs5NvyB84euP+NtOFPrN2P'
        b'X/no3D8/KDzw/cdOow1hryX96kfT2jc/Ux6t/Szxjq+ZtVAwoh1zt1msDILYhU1ynKaHBNpgVkfo3TyM5UekUkMkNDCxoeMQb7mx3YRdXkv+bj96Ig7b5bh1mC+BYgNf'
        b'fgKSUx7A46cCGg/AFDPvkJwkJNSUktg6vFwZCEaU+IhGI1gQoiKVWJmRJyF4HjDhthSB54t1vIEoDeYMl2IERQrBrMRKsrSk7fqdQoAgNGA+J60Um+UuBAgWQs7NZ8MD'
        b'9xnwBqK2cKGLbGNM6HJNueCTQlW5C5DD27XgDvHDJgtfHyyR42R2i7BUD/psLggvLogwS4h5NLKVGo+wCGaFLKMFGIDqlcGWIhd8DKPQDuW8MS0tCMek9W8Pk+zPqt9G'
        b'wh0hTrPxOLZ5WZCYVeyFd2BSjpO7Jt4ejsO8P+siPgoS6gAvVQFuxbusErCaq2BLq9YxWQ4QFV1Ig6FgXf4atp/zfRLgqUjywkM+xLMH8/jtpMMgQQKJ4zbyRNO7iOh1'
        b'iIJwyIpvOX7Y2HA5MUnJFO6H7+IPWA2nsBOLLEn8o/ew0McSs7GZGL2NBGvO0/2yeY0xB7K8nkRKbxEccDrYJdQdbjOH+SWB63EIq3b1AMv503f32r5S1nUmmG2C0gAe'
        b'ajdFGq6QaCW+0GEMkwK43dXA6pUSrXIgE2hxIYLfpz/OJa6UaFsTCDpnMJ+/tj0wIrdKooU+Pb480wN6gK12p73LskBrAeNMoF0PDXxrYzWoUlpDooX70CEVacO0+QWu'
        b'd7JiYwjuRjZHiSNmSVLCcJ7f9a0DcJ8VIbbxs8IFaBUzgDQ/fyidxXLT/nuVl0QcJuBcwklVHBHZwh2RpS1rUSmriC3XpK09ErDCS3ovJE+eI7WjUUw4UWnPB0jF0eP3'
        b'pcUWYSEI7tkIjev1XWUIv2akiWfQCSOKfDXHPYQ1nLwLScvtYgUZPx4unHezul/EGq2wl1ijPZ2SoYB4nTAorSPDF7DlWGMSrW0SLFVI4WdnsRmQJTxiDVW7fbCQhHWa'
        b'HetloNkQH/EDHcBa7OMf8rMkzk83I+Z0oSNoj8xBpSX/be1NGHm2qOhVa2lZUT28z7uQYRLvSvjSk4UC2GD1QWUoEWP7OZwTiu+wSjTZvB37nmUwFtDJ+4oNSAEt4dey'
        b'Dh9i5XIQNB8AbYBzfAx0BZTxh6W3/QqOq1+W0kEfW0XsE8ND6N0m4HWxL5TRfViZmTLwkcXWODGMJUOOmfp/ngP2xKj7v9j9eqWHOyI6epWH+z0mTn01O/deFb7/tBzf'
        b'nGSpLLUQIsyKT+uJNMVqy0HECmIxX3paLA0epp+eaqqiJJERrfyjJlHgR2KzKIkE07QCX8JahreoK/H1d1iBaw1+DWoiNbEm33RlqcHKRr4ajxofwKzGl73W4P3xa3g4'
        b'VxyH1BqvKJjUl23dqQbMzL5s5U7dtNpC/58VGZcX5nkyMD8jP5n58ty8dX8L/VSoLK0S+ZWs+1nc360/z5m64gjMJG8oLPkyn2RQRskIQjdHaskTG9dxjhOypQSjvqLU'
        b'qC/izfrMqC/OX5evmS/J14rVkpr0ZQrkcribsplyzMsawN2Q5U36MrdkV8TvBojXMOkHXZQGSa+26PO27QipbXbZCft8O/nSE6sTqtKlZuYVQ1hKrc1REclrmiAjmTfB'
        b'iO8pxMyFz/cdfB2zOnNUrDmr+dLyzI34pCneArq0DsGeLSyJOSdo6cmCDXltk7bRkZToGDsHo8iIVN4GK2w4NeZiakxaDD/2V3Mu8wco9UA8XUZpLdcBDb92GLHUML1k'
        b'lmeW8C+y3H4VO+3abYI2+2aw/L/LxKsavZ60ID/xJGDrGd9yqZki1NFvw9hxlQ/1wgXrLYJVNFNGak1klkIs8AtYZR3NxF5FKAnAct5sdcYJ5yz4UqJtvFcast14Dbgs'
        b'WIn7u9iGtWL0tt7pJ7R5kX1ZZ7nJy0vrOO0f8AHCUAl1YRbwgAnLBTiAFVgWwIyaPt48Uz31TLDtSo1elpMEqWIPNp7ll3MMJu2EptVQbUb/9MGYkP+vafspp6FmzPpK'
        b'xgQba7gJivhrDYcC+a9DMk9zP7+xU8yFZyX+PdjoqPC1a8ch/tu6i4kiFXfe1HsmONlBaJC9F4ppMroC25OYw9mSrDaf4crxpRALYNlIDb0wLWzCytMHq5iFliREjxPS'
        b'nfAdLE64e1p6SitXT2OZqic+0uaN5JIb7lKTrS4UrYq/WzNUIB0rzUS8tWXbJZxfVcifL+J/BXrxDtZ48MY5HwWok9oxM9WXqg0kQClvLQ4hQWxcOjWU2T5rMDZdtoCy'
        b'5seKNzEPsvmj+rO5hHuwU8jZS0/2klo+DiUKB6m++SQ3YW8rzx3KytTzllu/3GaUN36byQqdsB9aefAmkWvO+IC7BvNnpP3BYXwvL/VlprkSFDZv5z/efAxb+fTEWJji'
        b'rkIVVPA9vxU1tvLmkARsv8klqF/i97xVH6qYjEvQU0SK1V4RNlrD8EU53iCZHAVTgqUTpzZKjZ3M1Amlmfz3rGAsyYVPpH8chWbogD6cSNhkO8ylkQbC/dPoE+dy5zTt'
        b'XSp5O3726a/f/PSjGK3Uu43me464eByT1z4e/WC32Yex/n/ortaf+sH6bAtT0/nbuZtf9Gt3PVeqv2/sF24/tPCYzb37luvPww5u/OE7SnKfFWr+1eab2/fDFqfB7lqj'
        b'91/8y3CMccQLR+ptT9r9cfv2OrN/+n32vY/DJqoaZna/5d73x7MyeYHl32uPjNt6S3znb38SHZD8Zt3fhmX+dtDQy7zX3DvosrZqU2DAxzZvfLJf60J64H/dsbrW8ucz'
        b'5pd/PDKf7Xt24Ped3Scz3Ox+8u8HyQnf+7DrTKNZ1cdvFdzsfHOy9s35l7S+MVB2pmHccdFOfrOXdc1MUH/3N1//7kcvL/zE6lRV2P3YTJFN7tWQpIido5XvDg3+ouYP'
        b'NSpv+dVZPe6ofdXP9W99nW8XvdFovbet6pb5T1r6yn+/LfqD76a3/6tu8IeHmy/vVhj7beH7Lp35KWLJ0Whvr5mXUyYU0tfrJ7+WUZ6idSb53de/t8lHPb3ldlLQDwZM'
        b'c3+2vim094aXfua/Ajt8vbP/WRAwUfvvH+R+8vh1bv61F8x+dOlmofWfh957+bbM7X/rcmfrjLt3mUkND81JgU801TTSYoe8lHlJ/AR04aJUWfXADqav8rpq0yFelBcn'
        b'mDxlccBJbGcmh504yA/t5bdBWi0jFO+zghnirV4afN3Sy/Bo3bIqu2Mn3Ne8KBgSRvbh42UTA8yR0tpC/3bxOoYJDOK4NEQUsqKeKarqJ+0fA7lHtZbaScq4i0I9YDwE'
        b'mgSt9IEDtjLrfhlkh6xoJ6mtKLTYGfHVXNGWJ+UozJmFCPVIvTGf76JDa+jEhaU+OmpX+GWfgI4wC1qJhyUtuIB2pbhJDOVOkUJUDt5Zx9fo34HD0jL9UE3aDDvDI5F7'
        b'VynugtJeCI1Yc8JCUOLKMUuorwwPvHcwzYUPzVXfKwmFYU9e/99/CKd51QvLfIhwEpOwkOP0oUnmrCW07IcaIcGzHCtYo3rWx293jCwnZyCWgeEjvI6aBnf1VqqJvI54'
        b'8DSWXnURLDhVJ6BRqiSu1BAjsZFQPv82r7TfOAvNT+uIx21IRdwNRbxmHgq56cIgJ7Bwjc4TRIU6+KVe26oj6Gdh+JCpaEw/g1LV/1A21/pfVMie0spUVoYO8GpZP6Pr'
        b'X00tu81Zq/BKkpK0q6SCVCHS43sB0ScS+kbMftLgFa2l/7MOQqx7ECtoqsSrVEvKmwavQqnwvYVYXpKatD+lDN9PSIkPcmL/Zuo/nSSwYj9SvUpO0Gi2Lms5TLVYoUhp'
        b'/E+fr5nMisnMl2fktSlTpmWoLPV6+GraFOlTO1fqU5+396VQLSW2EGXxU7oUk0V5OfQwx8dTy5L2JFT+F/P6lIRpVLEqy9qTzBdqTy5rRaouaU9Pyv8vB57y8ar/w1HW'
        b'wjtLtXWE99aog2ltdESIdeGX8pwYHj4om6lY9KhHgJ/93p27mEpzISKdRWqkpbPcy+cuQSjq8yRu5elKhcL3XzmzQ0HI7NhyPOnpcID1Ms8VLc2xWfCua2Ktuzx0r3Qo'
        b'b5MEX9koePWLoQBYOgRRw5UF/b0hS/BFP9ytlih+ymHNvNUwI0lQEzvIpGUxaHvjjlXhqCprNPPHsGaNI69wBbs0vF7gtIc0FbcceXd3/VuvwS+0t3XPXM/0a5H7h2KD'
        b'8qevTzQct2x/489/j9ypej36elNo4my9nn3ZfxuUW6ab/Fw9cq5Pd/I7xadKIqdsvvnDn0yuE8du3vzJ+PmkbwYNLqTM+XwQc/p96z/d35zssu0fDn80kxVMkKVH8YGF'
        b'O7bizJPIU8jCSeHbEs6ecbK2wFUV028E8GzuLN4JeqbcAtZGySiEQR7PgkReFvS62vqnWWHNCUPenp6gi6x/clGMJjOMM6O4vfmqhJD/iDmsoN1qGTx6raLevl+Het/m'
        b'Ni4ljwg9gZcoOKPTmZueojKrZ11NY1eTnBU09qsV3yYCyr+vtJqK8gTUnD679rUJ6L2tKwno52+NVZ/NTLjI7Cv/I7UqpbGjn/Q9GziaGhWfcFlaz0haLHdVBaU1KOQR'
        b'wVyRdI23byRcuJgUwyw0MdFbnktNpZt5uqoPffxFDVW4NemRjK9QuaYfWmFMcDGtHZ6EPVDEnEiRugoJycYJrj9+SYY/vOnPXmPp2MEvvPbiRNiF8lH3jrtmst/WjIqP'
        b'TYq0jEiOjY/0llbn7G1RuJT0OzMZXvZNtTEn7M5KfYLcl6BKsMjnw+OQFU4rbSwmFGxPwXIha6zqxM4l5M5cGViebp3OMouwHuvMcZyh9SgWs46RgjXGw+eSlfk10sHZ'
        b'C14wIA8j12DxC7uwaUQI97oEUGk8itp/PRR1YAi6XB502YT61Ayrk2UsViPhGvVBLZbNvFb0UwPDq0NfB6+yuHdX5W5+0TpZ0QhZX99AV18zsa/wV+ML6uo9qeoRwf7R'
        b'5akM+4mFn/NWal644gkEvxvhKDb8bwvTX5Jcp6rTj2rK0hw2BWUZsZHRyqJ5GhoqYgMNHWUlkc5GRoU5kfFNTZF1sqbIaHMGc4Cd8r25MouZw1khkVnMmZrIXsaF4Iy/'
        b'iHnfeS2Wkypa6ZyCTTs1IA+ncXb9vr1MDR2Wc8QC1gdHgTSwFryzWZV0tlxog0GoOnoUOpShEgpF+rgA07igCg2OOAGlMBYBk9gXqMqSIHNw2NkJFmDEHRbc6KkyLLwG'
        b'09AHg9Y3oNMbhpxu4Dz2yuMIUYV+mNkD3dCJPXGXbHdgwy7MwvZk5n7GPhzDphvOUAQ9pCGP6rpdcvLTgaJtmHXkZqIdluA8TCc4Yd55t42bIza6OnrJhthet/aDzhAD'
        b'FpE26QSPsRfGoTwZ+rGChplyhymHC+ZYZhuGxarYE40jWiTNtLGGE6xFHtaGH8HG43aJUBKFD+WIYk1hXgqMYgW2BuBDGLlyAbtg4SbMYl0gVGzAjvNnsBa69q3HIXeY'
        b'3QnFtPcKKF13FIYDIMfEixYwhY32MHwTB05Ag4hoXCPewWpSMxuxLB4ekMbZccVQogzVMIH3bS1JGZ+Kt1dywknIjzKALLcLcDeahq3zgTkZ0t6jXFM2u2JpAi5gkyfW'
        b'hOjBw6su+AjG6KZGnOWg/oRZEDOCQQ3kKhkH4rgetmMH/TbtQ2SvOZjOowbqLHHa/sAO5+3aWjh2kj5ovm5yxgIbsF9DC/MJMCYD0+jTCjWlrbhIb/TjKAzTikY4rLOL'
        b'2Y8NodBkC3OaeF8t0gdK49IPYJY/1hlCUdheBVyERwZa8CgJFvUhL45eH7xI+nP9LgPsiN568rSzDVYRKDyCnrQIgrpabAxU2RCambz/Ok4YnN0Ejb7QseEMDtMR1eED'
        b'BdrMBIFUI3YcwmIFyD+GMzvpJmthwIF2OUjrm4acYLqEMquDBBGFV2FMVx8L6XxmsU3tlgTn8J7bdlsczigiwN94HKegxd8FSgnsVWAOx9ffOET323sMsgyhGeutVHbj'
        b'EN3QKLRKjkFPVMQ2MyiPl4Eio9s20G2fkRmvjjUEjB34gA62+GL4KZhfHwyNh6ARRqELciKw2RzrLIzxEc7AtARGFLFaH6ciZC9iC0wEhVw5iE03A5JgAJvoHOZNaRME'
        b'Ifgw2Ws/DdFqAE2YfTyYxq4Mhrp9UA/5kYR62WIHH6yEESt6ZgwfQP/NMze1NIJvR+52i8Pmddd2MzfyHDHXNgLAebizhwXvum323n7NmICtDBpwcBcB+QAB5yMsiMDK'
        b'JJijPR3DWbgnj90HsPI63M/wcknAhyaYb0oqwuKNfda3Ie+cYgA80jNkhd6wd529TAouhuOYGMuv6kQcw7swrgTFt9yhHrMN3KA0hOTn3Gh1uA8P/AKCbKM0jTdgn4ub'
        b'kram9U5ZfbsgQqEWbywIoNutx3490iYGISsCe/bSNc7CHcyVYKUvVOCoETafjPLFwmDsh3GZdQR7hbrQQRthhCk3zJadLRTgIExcuboBSgxpxocEUg+usl42mesUCBvG'
        b'Y7EaH9+w1YYqOsW7dDsjRLgmFeLUPPH+BhjCttMncYDwLhenN5+FeR8vWIRexe1QmcZSYCHPIQbHL+C9YJi33shsyqF+MK1PEDeAJf5Q6eW5LvQKTtJ8PQQKrWcgm/Bn'
        b'kTaWbYsDWiYB29f7QTYd+WQIdifR4T3wgzEzfCQL9ZHboR2GEzJeFfOtu1swjyDSGcoYRNK6H1vARIYDNofK0LhteDc5AtouKRNa1u05bgk9GuFerJ1PMcHxHbrxOn2C'
        b'pAUWfgFjMOwBeWcIW3O34rz7gQPOWO8JndEaSphLENtNMDUNd7dBo9FlAuE68QGYu8bttfbAqvPpFqyWH/SQTFQIM4Q5lYRyTZFnziYT7eiwxKZEOu5ZFideSLDaD53E'
        b'PqpDjxFZXLTQPZV+9hy0+dAKu7AcJ0wJNyoObrW9isXaivB4JcQSftQe30DrmLyCOVaKt2EimaeY1WrXoIFIZY+L997MLVEw4nv9ho7knBsU6UJ2LG1skRUiJrqUs/cA'
        b'wW+9/AUogd4wqFKlK+4zUoUqe2xwh7Z0eiQb2U7uYysw30yWuhhznImCdK+Xh2l7nNEzJmAYgxlbXNC+gp3J66/JxCdhFtQQvuZhtTodVBdtrwfnYPw43WbHOiwM2RRP'
        b'sJaDo4egi458LtSEONNQyFUDgt72C85YHk78q84M+q4QQhRb01V0uNgSibtHUEl8M3T3+T1YYZqID24eVsukBeZAFkFyB4zvMoKCK6bRETBOFGdaRRurcAZzVLDAFVpt'
        b'AwkkoP0areEelpnCJAHNAJRlYoe8/nY651nscg2xgQVsVnI1pz3nEYlsI77ddBTG3eL86S7H4U5aCN1oA3HE+zCbiUWXof6sfAzWOse6WfM8vcwrnRhOXgaRhXJ6ptbJ'
        b'TTcY66DpPBSKL+tBMwE4HSIBOLSeTqRVLpIyvyPF0xXvJatiRcwp+U3n8OFGqGPAZUMo3eG6jlh2c8YPCbRvQ5cDI7XJvIAxh8MWOCU6ZhgObfLY4K8kglEWwFtKWFMP'
        b'5ekwxhG53b4es3bREdcbXMcheZiBrhg3U2g8AgNaxAwaN9DjpWrYLH/BIJHAplGdsLHe1gwXgqzdoenEdaw2gGJPw33EB6aV6GgWsEj+OPSFix0ZvkSILoaywi4tyTiM'
        b's2dPEcVgJHiQSAHJICl7oUnrkIW/Jg6HQEX4UbhzDGY0sM3t9hk6mbZ917WgOMA7BPp24MTtTUfCiXT004UMXKBjGYCmM9dEWOtqB48Dd15XO4LZ0AT1B6KIMd+hi+7Q'
        b'W8fSe7FLAovrsDJIV2Mjcb5CbSg/6x0RSMg7b3fCMYnQuCoYqqwhx1vbRhsfJMHgIUK/gkSoNsY7R0SYJXscZqIPQ41rAowf8IVZKDjscOTYrY3YQPBPhLGb5svnLhAT'
        b'6MBROWgjRLinQwgzRodVhs22MA/FGwhPm3fA7E2cunSA4LaeWF0p1jpdwg4XoilZ0SeuQp5bCuFA202ovbmewGoy+hr2xemR3nMP24lQFO7HklPr9iKBfDl2uZFoREDd'
        b'bbSP1tBCP3Ue2nfVTYPY4tGNMB7Asg1g4tpuwvp57D+CxXRsucT07u8zZCJZKhTHGpkwUMQK7YM8NeigZWZBawLURq7LvOyDzTTLBGFWHVQm0Gr6SCLIEUNpBh188Ybr'
        b'tL0m4qADxDjTgqHdGluxS89PNYA4RW+iDrbHYI0H3W8PzoZCSzgtcegADBEeFzjAXWSIPo+1QTRE/rn4y4wLYfaFDTh+kQjMGOZudz2thCP6u1xPbML7WzMqmejc78AK'
        b'IfrTFpZlCAt8JLqApSRDONtbwPROGLmsbOIgn0oibL3rSaw8TFuBNhe64HmaeTyVDmmKEaHgrZBnhzm7IogJLBLlHbl43VnF0AvmcTgS79MzQ0Q/6m5vhiyLk3Tbj2Ts'
        b'iRLWwmPzvQdx4CxJaDX4OIYEzFLiYv3EoieR6FrObSus1iSYLTh8Fto8sdb/EPHW8phD0BBkTkJHF8w60mylJI60wZw64XYLtGtgnzuU7rqKlWo+m+MuELHLlifsaL2u'
        b'FAYjOxyPeus5qxKADUKNmtUmGTqzFiVNB5zYbKwgccU7W+gYs3YQ0Hev0ycWX0pjPgzFnLNQ7QJElw4QGyTSRCICzoRhM7buv0TkqoY05UZaTSuO0C2JjludhKIdycSm'
        b'm2DQD3NOY0eoIxR6W/rQseXAvSOJ+n5uJ5gQU3j2FvREmuGdKMjSum6EdcStKs7gVCpBTu0JHAjHAqudUCcmMLvvjfkuBFyLRNYfxp0llaScSPe9DXp0xBPhWLUf8+F+'
        b'ij0d/QNbyDtAMNOFFbtCtGP3OvhFQlc4PkoJJaLctl9daYfdPu0NdmZE1CdU8J7WUV8T4oWLO6A5iEatVCXAWrgAhf4nCUNmQqHNGHq0o6HcEkeTac4m2mnLOUKF7jMx'
        b'64n6VMJDaxhWpvMsxLo4uLcZxs5ePKd7EPqT6KGH0BBL9KFBkkgLywogiJ+wgzJnmDchhvsY797WxgUuCZssSHjugvGM1wgsM0j+m2BgmZ3MQ+U8QeVVHIjBB9cUSPDJ'
        b'0bpOh5htvIlk3AmDnZpYpUHC5Cn/THcov715x/UMyIvQOx6m4k88vJP9gZw9RPtriZDQa85McLqhoQqDV+lyZ/D+yYPKxC+nYFE9HLuxIZH4ba8sZmVgTWAMzF9Ppq+a'
        b'Is+SMDPEyw9A8sMszCcQ+I9H6mFu6mbsNiXI6CDkGQhMxoobRkQempnAG08LKDjneEFPmd6oINJRS8dR5BNCol7/zYCbp+KvblXxRZJZO7F7K1Hu3tADV9XodIuA4W45'
        b'PEq+eEATptTTCU+yU0mmKA/2tVPcjiORvngHagPokSm4K4/9qjFYcMKC+V7vQP5FaFQnReUutF7FsTAC1hEbFQtPok8NCRquidcOkOrUsYmQdJioTZG+qQydZc1OkjfL'
        b'dbWhOtlo8zFW4XgTPnYjwlVC2skEMeSZZBYfj5WXdmDPNlJv+/HuTWg0tSL690ieJsvBHju3GLurW0KhamcsoXo2oUROBmFDoxJU7sLS83bY5L2DEGJca11aJJHAOew/'
        b'jf1nCXe6thAcNu8juWXaDvLx0cVk6Eyn+y8gdVl3pzaRzLqDROfH92+jlZfHQwlJDbL4IIj4ZQGBa9WB8zgZtAFzZaAah2No3haCt0Zu2xXni6fTdI7TFY9uNSecaYGK'
        b'6HRoPnAVCrfhPdlQLEqEBid6dgwmSO6sw3sniVEUkWjSrO2tBvc9jW/7EYwO4lBmSBJJi3UBB47tY8rZgAN0u6Sah8I0QVWZD4xeT9COJSrUoE4gPmGFnSduuGGVqzkB'
        b'xZDuVsy28U4MouOrkDOT47NibieFed2095DlRDYcvTF1iw/RgeEUby/MteSze1hqj5IGn1xzMRF6vEg8brIQc6JDHDYYQSEfTGLkHe61FZqt5DjRQfpYF0qEIthjx1je'
        b'WTeJSCJO5Mlhk1o0P8FWLEzHImMrSxFfk6MVy8QZbhKOM4bO66zCE5YQPjQeUqGzHr6ltPmMItTu91eP0CKGVGFNUNBBp1PDJHVjvOvh6gN5iQd0zIjKTGP3hkziSu3Q'
        b'6qHhcoYIdzk0R2IZiSmEuHh/L7O1kMpdcdU64wj06zDp7iZ0x0RgvjK0p0YQtlTB4gHIOnUCa3zp/uh7wsHcY/RjF/RyRFrzgzRJdGuyoWtqsT29nQAuexPpAaPmITRu'
        b'GedHc+bGEDUdJs5bRfdLuk3CDcizJq5aEQjlxqQijBEUnCaxpcKYqNtDqHQgBSk3PcwHFrwIyruIPxQRMI0ZkLKUQwpZgYPZDchnNe1miDiMECNog5EtJAc/gAb7GPvL'
        b'EiyTj1HHevfz0LcXH6VabMbH53DgtMd66JO/kRHjkxpGxLMCuhSZuQDqDTaw9qMkXHWw0CDoCT1NYxXTedaGaCcSrj6mJZTvoa32OG9UOqWCrVHhvMbVKMEcW9JfsuhU'
        b'HiLRz0VbKJbgSIi5ny3mBhMta9+PI8aELL12FsByKfqgfD+JQWW0n6xU3QzWbaicpRh2wfzRMyRFVkGhObTK42AClrtDzUFsCyJVqph0lnn59VgUviXK7Ig+DipATTjU'
        b'pBJyzJupZWBfVGoq9tCfypuqtNx7e08Gk+74kChwhR2OHXG7sS42GiZNVWFKDe+7EzLd2YcPbTwIn/sgD5lB5546Ke4TkL0RmsMI96H2oPtp3zOpp07rkhxUQAz8sa49'
        b'Vqfa2BFxGLssIZrQDYNWOrCYEY8D+0gFKDeBWXMtbNRlBJx4Xf7O24Sck3tITrzHDFFmvrHES2HaBprSCabyYfoM5CcT++6C/qOEtg+9bsPDMFL2WulWH3o68oaXOQlx'
        b'l/tn4kiR6oayfbr6tyxI4pzwZQoEVsTCLHbspH8Wcd5IB2pj0izT9UjUGjiAj86pYrYqzomg9dztM954J6NXzArJd+o/bZIh8jl0wOiQ+mUc1JHbeAXbo1mASyQR5NHj'
        b'Z7DQU1vHhRSWRahLpdPMU9aWPR3m7U/0ptxuI0FOLQxvwJ5del5bnGD8OukB+cF6flZRLvLEyx6dOMnbZsb8NtMkjVC1lw5kTok2MJZMhKWDWMl8PE5lwJQZDEORkwVh'
        b'Rg82J9MvZZd3QyPxMqJL5QxSO2HUHIZ2ppCI3+qIY9Fn6JDzfE7qMhkTiTh3nxKRoDdHOJ1tQOgz6kasrVXGAHstiNyOY6fWSXiwlWhpKTQdSvUm6bo1bruEpM6cQ4yo'
        b'jkL2zSQS7PUPkYzQuYEVmlnwxt5MzSNK0H/hLNHfYsEAkBZFKFB+fgctjDgZtt8iUvDYgDChhfRb6PU5xyVi/uEkojnN5w7HET8Yx+YYWmNlOvHfHNb5l0hfS1Q0DCcd'
        b'34cTuhqwsO00gUK9Nna7WLMzMcc+3Rh8nICPePm+n3SGuVScPyfrpIEN+ruw0u8i0bRiLezQJM2r6joJUVmweImknImD0LfOz/Sg3Xbium1YE6KA7W4pdOxNpiYZhmYJ'
        b'OsfdNNdhm9btDEdVyDss9iWg72fFNqHnFlGC9oyT7lB0hujsHQt4pB1DeDlHiDF189QF4pDJUCrBUfp9kCS8xxGXido2O98Ixu4QKyJLjThgBrOHz8HDzTs8iCpUsSum'
        b'a1ggwtZA1OHhOtrGPC7eOu5Ng3btgcoL6938aO4ZfTqP2SPwyIVIcH6Y7NaD6cQ27/FSFt36NGniLQFYtKzWnqL5S6Bu92am2Yb4K4tgUhMLfGFYzgoenpHTgT4kKjix'
        b'hyBh2OEkzkOhdYIDwWgFby7p32pFhIwZ6BrWWUIu0TUC0jwYIbUAF674WZnRhQ3g3AEX6DOABnWDjXT8xTARTdjaedCJg74NRFr6d0CDA2ZtIXI3BoPBeD8ImmxDiPLk'
        b'e0BzdAgxheGTTDTpwPaQVBNZSbwT1tpg91W8Zw1j2wIxJ3kndCUeJsbQRXvuJYG12ZVoDjz2xkLLEGIdTeaEznettpyKx+5960+n4oIvgVstMY/c3doKcD8xGUaIgLXS'
        b'DCO+8oQHixf9SGGvIIgphq5M2jSxq43YYwM1GcRQ6nwTCZ5IZamzVE2GXCUjR3zokID1njoXYA76MrDJAWZcUrGOzq4MR04awmIgZ493VRVwUUKrzPNZD49lmU2k0wF6'
        b'4nTcofaY/kYHUrcKaUv4cD8R8jkCimHCgmmChPlLpHYOatGhN0RGMcyJjTcluloiDnWJu6QCk2ewJ9HPNyH2HAmoY2q0hEZiuANKOOYFRVFQd9JCF0i7uIMliSoROBgI'
        b'ZVqHws9ex1ZPn027sGInjm6KD8VSOzETWIkK5ZL6fB/nvK/eYIX0IzWIebXjgqHMDqjV8se8qGC3c4d9XAnDi52xJs0+Gh9vJYo0RFdaRDqhXBiRh0HlEAOexDCqXU0H'
        b'WR+1G0ZxcqsZYW49dl4jhCuFEVOWOrROnvhj/8Xg9SzBKxrnj1+iuylBEg/KFWFKc7810bTWa1q31U0IuxqI4DDTeKslFoRB674LhJi94RmuEpaUTqRqaBVwk2Y7JRHr'
        b'4gOsOKSeCl3acokmwPxG47T6HqzdJfIM9GDaUxQ+isJxVcKuSTqAdsv9alhucHqTDEF5I/HwYhLfBzPpyGt2ByoGwdBebAwmAG8k6j2jzNRxGDAIojMnnRpKdTA3wJWJ'
        b'P1o0WC8h58OwzdBtiw+PmdOv+Z6b6KiKtsJ9682EqDVO0LSezqgpjZhPbwyMBhsQuDeK/XfrQ+cGB8iKhHs2JPo6E1ncHGSmTwSjMh5zFGE0JvU28a8cmAjZS8xlPIZR'
        b'8yL59ON20Keyj866DBv0wui0HmtiR9x6HFIwzXRxuqQLLftg2PsGQVc3McAubNiAU+me2KdJEk8Z8dLZeGIKmUpHUukySV7Eyq326dC1X2YXPjy4HR4cUMLmdBzUiD2r'
        b'Bz3rNC5B1Xos9oqjgbKh2lLe1oculgQOOppHMkY+Fw/t80/Eoa1EIPoIl5rDt+KiKxGxOmjxcHHmCEEKCTtJ+qZTqoQp5VjM30NMmkC16AiMbFQUEUWYDgsl8tdN1/KI'
        b'Rs1dt/4U8fIS6FSAu/GQ54B9VsQHCm5dhkr7UGRm8g4Oxs/t1ye6MgN5CSaEb7160G5FyN5AqDFCanVzuOKGPTirC3WB9l4X3YiRPoAH+FCGXrkD40baDqRwdEKPC/TL'
        b'GhBKNcPijvUbSKQtMcfyG1jOjubeFRiTXDTeT59WOEGHySl8TBwTa9dtd9qOrfZQHxNMsFOAtanEn+avnsHh3U5BkJOUTuSx2prbCz0RV7UjI+nUk+JxFkoiYeQSCdEV'
        b'JMaV0GmNOrL6F9sdCNIfY36qo1esM1GDAiy8bkWHO6YiIujrV2ECMl1kQ3Ta1ZvwyI9+7YRGb9LP78PwRXccOsVzxwmcdTpzAOpMiXOS7uvmjBOeJMYNK0fvInmuPoSw'
        b'Y1E+koS2rK3YZZIhIlRKjPNjeMRKYjJEmsdZC6LG9QSZUw44oUfybjBWKSUcgYHt2HTEBiokrICGKnvCWSOBlMW563Hu7iQS5HgGORhhXmYKydjz2OtCdz8G9xVxbq98'
        b'EvGdARG2B+DMjpuQRTpfjbGrunIA1kbzbrWHzMh/+zpUwwyzZnXCY3/aIKFID7MUkbDbDT3uOthwzd/ktA1trQb7nTD7NpbipAGRgYJQuB9EAteklVx8iq0ejLgrEd4P'
        b'0oMltnSqeUkE//Pq2HYWckkmGCHuUroLy/XlaY/dilY4dCOeNXCLvAp3nYkxl0KbBMf0FLHppJ6rHgHLoKmsxiZ8dDAIytUOKRDhnMEsNxJoBhhZ24NDLNW5Bst2qsUc'
        b'h9wzXqb26YlKOK9xKtOEaDxJ5gcuHIeyi1hlG0D6NBNExx3ibxBs3DOBkXWOXoS/7bowowRTwdeSzPHBDqJa09gEuedw5qoS5h0LIJzI5dPMi2jyfLstLKrDEFtUlCSx'
        b'ulh0OjHhbJgdNnqpiY7p0HsPSRWFynW6hGtVMJ2o4mFhg1OGzOxJnDsL5jbCNPPc9RpsIq2vOPKgM0nwrbvpLNphaJNVMlR4byOMKCXlJy0DGnaz9GgPnHRSJhl+lgSD'
        b'5mOZutihckuWdlDpCo1aijcI2SrptwpYtEgOvwatW0inzNG094NJPWjW2OescgXveGKuQZg89gZCZTzLmCUgKvUPYaZS7M1gxi6691kivSPEJnKwyxoLboVtIT5NUtBJ'
        b'erbFF6r8Y+DOKZzKtCbhDLoJWaqIWRcoh0RmnCZ0vA+MoZBM2rWXdrd4E6oNsTKGBO/JSwQvD6/oEVgN3MT823CPCDkJH3eCae56vJvxSzFfU6TpCR4cYkapslPEiYl+'
        b'JR408lffjuWEA6e2X6evmzfERSnqYdcG++10wYs4FAeD8u7hNMsUSUnd4r04pQ+L2LsvUZk2lYtt6cC8v9mnnaBSBmr1iJDPXcEGL+iQ0I89MBND3ObBLaKLZYRO1XQd'
        b'FUqG2OlJdHSATr8YK2/gIsw6aeO9vTBrhR3bfbAoiXm5PJiVKvo4nU+uMVGUeyoy2B+zkSB/4poRIfnjXX4pBHJdWra0tsqdOli7bbMZNhkfI6GBsOMIwcO8djxOqmDj'
        b'/i3YrUrKY24o5BzBx4dgQPEqEZcqkoBqiDB3srpbM3LQYuAOdcrEe7t3qkO7yy5osCN5IVcvcD0+2LZbTg4LThzBe8p458hxUoxnrUnIynfAUfWLOGmj4mULHXZY5eJ4'
        b'iA5lHBplCO+7iNLnZYYbabCcq8dECh5DthFB+0MRiWa3L+8igKvyh1xlHi4ehxHxXjxvTAShGfNT6NR6GCGY3EniR1VsPHTaE0Qz83sVFuri+F7SbSrioEAOOuKN4IEM'
        b'DB9wxCmmomPWCaJfE95XiJ8v2MmRbN3JGkPlWNLBDOtAx02oW0fAUbCVeZJlb8jtjQukkaud1LCWRAe5K0wKytHak0wqH8n0d4hGVECPFjYc1b3KgioC6OQaYebc5R3Q'
        b'bwVzrtBpJgsNW0jCagqGvvOk9DyETqswkoGIZe91TNkNM54ml7BjB9R7Qo/FzmM4Lkv8pM5jC+m1LTi2i7hbH0OShgDNo3YkYw9Y42LQdiJtdf7hamE3AzeGEOAUYNYe'
        b'b5qjfpvzZqi3O3STIyGz4Dz2Yb+7mVgonvYAyy+tqFoDD8zNT1zi7UoOyvBYKKuWwuEdNYKu+ltmEt6yhI8i1byw5iqzLNlzdEfdt/hXvIKhxQuzlFkFddFOFnHbtZP/'
        b'IojeLsGiPSfwngwnOkKv6PrxI52CspNeJNfNLlnHzjvRytg3u0hI8uJc/Gh+W/qcFM0JvsrSDqzSJhbc7eNNbzhwhCGNMMfvxYlgOt+LUcplkxou7FxqxzwBHTvovWpP'
        b'M3rPj8MOHD/Pm9Vc4rZhUfBxH8GsVrELZ4U9lppBoRdOKi+Z4faEmIn4bwzpDoa8vHU9aSALDgvUcFGYYurWSSwyCVm2wxE3ajcTufLdg/gMs1FvMQuvNPqpanjSS7uO'
        b'cWYS/uNgXwn7WC9HJdxyUlZfqNLzt0T+w0PfkA9XGQm25FgEmSs/Gp+OlrDL5dtc2otEqLZs232z6pSfvot2btyVN98Nj0oy+kvkC3/5xfV87Uo9za3Z6b/V3t613UlD'
        b'scu0KP3Kn6t7ndo/e7V507D3y0eiEyb/9vM/v+lgN/6v1//xwcsN6Y5Jkm/lfvzxa9fzG/wHrc7+cX2ijFPp5u++fuT7ry5YBP0l9y2lX3cdjn79R+/Mjiw0n91Q8Ma3'
        b'1Lf1Wuur/O6fzf+00Nr1sz/9WCtjw/6/mjzaZJpW03m8NTC5we4vLzmq/2mDk/p/bzhQ5l5n8HufwLaPrN/a+9Zk9QmHb5954Prdsz9+eKz0466X/fuObarxPNEKjqUy'
        b'De9FLhp6vLpn8Hz6osjs1SD7Hn+T/YE/jP/tXbnm4y95Sia5xu97W/3rxGOPfkll9Yn3XJxclN+dsdph/LHKuycn3jz2/d//4Y3a844DM1rRw2ds/c1+Ej3ub7HN9ltO'
        b'AWPbz4w1Dbvsd3TPeK3nwqO88fderhjv8nij6824cduX9yj/eOLl78i99MENK8cfHBv7zraXTv+x5syHf5Y7NdUV+q36cX3n9I//PvTgQ7f5BO+fF6lc3zB/2TvNRzNi'
        b'37dqvvPxG0FOA4c/tK862PX9d7srrlS5bv7EofuXe98s+MVk+5/3eX37lYPHf/7io55Tu6/Xl0VxIZUhJpFnvDXM2/HfnX/O0PuGxutb7qt++vYFj6x//KzoH59Gj2z/'
        b'eGzw/IHsiOLyzT+4ru5edCV/Ic1q87dMv3V11myu4uTlzK5Txq81RMQZaH1maP6n2kzZxZc9vEeH/jaQ8HK512+qMxYtPyqO2/Vft+CXTf94ZUiuu/V9q8y4huEXnHTq'
        b'41zeVvzkQ5OXf3L6szylv5UbfXxRS7nRz+P0XocduccsL/0/lft+dzJig0XwNze+Opr93U81pkZKNv0hUv3TmQOP9r3S+dPbF0eGfvHPhT1DP7v07em/PLy2fn7X34dv'
        b'N/rnTuunnfun0o3St7WdX/F0emXztZ7Jt4/de/udircDr5+rvXrO+aMbr1x7JdjXZVPfO/mL//2rU8aftpgp8Vlo7izerOgQyzZjRKUUc/X5VKa0TCxThkrxsw0CVW/x'
        b'rWU23TJ/TmeZIuzH4e2Yz+dNMeW6VPawcqqqoiox+yL11AwV4s/TEs4gU0bBSl9oU9OIHRHLj1zBqSuXVOU4vUMSbBez1gwwwtccScYCyEm7rHIpA6fVoZBo7BhOqiuo'
        b'KuGI+mVZzkxNhtjp/YN8qxxDrHde+eiJm0sPQsnSBD4ycsyQ4i2kxc36wZDy8mAK2CtmsRU2nr7pLHwUqlKwPA1KFC7RGtOI5d2DQds1hsRJOWIQpTCQbsyT7C0keY5n'
        b'JJ5as04KXySl8PazbWvs/m9jS//P/zEz4Mnt/1/+ETqTh4UlpUREh4XxwdY99A9nIRaLRbtFRnw+maZYQSIjUpDIiemPRE1WU1NTUcNQQ15DTlNJW0tGrO2ht3XvbW63'
        b'WOTIwq5lZOhdo9uc5Ubjo+z3sL0iBSEgO2q38NOpA8Lv8nohG100JGoSTQ3r29x2V+FTL7GZ2FxsQf9ayO3if+L/qMiy7LWNK/6mWi+HLEtSv8O28yRw2/b//qr/z0BM'
        b'JBwGH0LNjojVkk1TY9f604srOz2x5J00bxvSHcqwjLX0ItQvI81qWJ5T2yDZpCCX0PbnPeI0AxHHvXzs3T0lbr4SF41jAyZu151+s1NN7265u/iu4laDHNmRzS/eSbax'
        b'TLF8Ue3d2eSI5G+42Ms4f7ft9FxY5nrzExVd6pm9JcGnw+78JmNu1MIrzut40Jn8gCN1+/MM326c+kvNKwtKrwVs0Y19taKi8PWg/7e4a4uJ6gjDZ/fslQUUQWOVqL0Z'
        b'FuQuCAIWKqDLsizaUlqlniy7Bzh1b+7FWyUhtlIBKUUslhoFlHqplXqBtoqlyUyqSRP74gsdTao+NCZtTB+aeGnS9P/ngJq+tWliNvl2z56Z2bmdne/fPd835qJr/h96'
        b'XV2JNP9+bO69dy6dPxZaWvf7z5nOrXU9q/taD/+ZbNpw7Y2Be2Jh7cuWsp7lgwVjyZMVXYGy6EAXK7l+c+fnrT89GLxy/bvrfcPJp7KbH3Y0pe1PHP/+zC/kwI0lf2S3'
        b'lZotq6fmu2KNGcenrsQXP5iqaCt5f+qqJj7htunq3t5buhMFtHB9w9Aee8PtBT7P3VuGwpibd+Lv3z16P+f0ndSHsVObbsxKmvxLa/3t7W39ddbFqpZ3ADpyLyrunU6u'
        b'fTUKFnJe20JH6clVRVwpBd+YbcV2Zzo9h4mcyanpWiGBXhYhwpmIqmLc3RC9n1ZHhDtb4e83naUwIHPEReRgPZdAb4KQYMIOoeiYzZHqMAoGndaUYuVKKkOA9m600q5M'
        b'YJ+vCRB0XCD71EWgnRx+IY1+mILy3X0aITNoztDC6nQhj58uh+WpZ8YtS1dDL0EacpaMkz7Vau1jcnIr3kXPczvCKXohnnaKNaSTvsf1JVW0vXBG8k379Roy6KWTvFvo'
        b'hC+gFuyw0W7rWjJo0wlzaJ8IIcflBi6wXkQvlNirltXk5WoEuqfRSPdrDXiTNf9oBz1WZ8/JhbzokEXGs1Af/bxYBCFiu2o69QkEIGcwic0BKbaRNhvWblTMJudaVfna'
        b'uUL6Ae3CjeR6gASvm0sGNGTiLTrMBcnNtMODKj0HLK46/BGrW0O+kBN4s17KyU9Lp90oWPfR4a0a8g3pj/Jm5dMvoTshBqlGLwsHNF0nLGzVLbaQ3TH0omoOdkp+1451'
        b'grZjl1usWjKkgQB+XzmvVv1CR/ip0zE27ewQRKHv6zlzyMugn1no+Vl0nOxJCJMO+nWQjm0BmhEnCMkv6oxlieqHdNTTSS4kSsOyBJhzn2o3LqRHnYXquPdDT448ZfGW'
        b'Rb/VkEMF5CgnE3C1j5Kv7ORMCgwtmnbREXqcGxk6baQ7sybdahDWVBh30UOQASvdkET7LPQs/rlCx9AGu1egx/ksw5EsgEAXIu9ZHq5E1wv6XRo60kj7uAmhRIYr8dbp'
        b'dLS+3jLNqxZEdXEyaV854w92EUrrhD7vRDNBCG92BM1LtaQr26nae43QTjKaVpW+zJGeoRFi54pe4ClHyCH1CjxRGrDDoNgzIDNcQM/Nhdon5oqQYIweUSfyELT3YNra'
        b'ZamoycRBoR9pJZjGoxvmc9YYpUPzRE8axmJ2AUL4A2TvzI45Kc/+q/1/WiDmPQOW8WSr4yCuRPEmLlc38UcS9yIzTcsnUbWFHmToAzZn2hkMUor+f68Am3lkqaIoThVS'
        b'meiV/aFaWNWYPhINemWm8yrhCNN5FDdgICj7mRiOhJi+cUdEDjNdYyDgZaLijzB9ExAleAq5/M0y0yv+YDTCRHdLiImBkIcZmhRvRIYDnyvIxJ1KkOldYbeiMLFF3g5J'
        b'oPgYJYw71br8bpkZgtFGr+JmsRWqENHh2gyZY4MhORJRmnZI231eZqoOuDdXKlBJc2NuvuxH/ycWp4QDUkTxyVCQL8h0lbXllSwu6AqFZQlOofKaJfgCnsIV6hYYkkdp'
        b'ViLM6HK75WAkzOJ4w6RIAHifv5mJbzqqmSXcojRFJDkUCoRYXNTvbnEpftkjydvdzCxJYRm6SpJYvD8gBRqbomE333qImWcOoDlRPxpAPSFhan+nhCqQplUhrEFwIqxH'
        b'cCCUIqxFyEfIQ6hBKELIQShBKEAoQ1iJsAJhNYINIRMhG2EVQjUC2pOFXkd4FSEXoRjBjlCJUI5QiFCLsBwhix+iTG4dvqpDeOWx6A8nkvkxoXq44SlCxc89MjXBTJHd'
        b'LRlstiRNv57m148WTB8vCbrcm9H9C4WoeE721FhNXL7HjJLk8nolSZ2yXOD3K75vULcKDf2I79TPMN9/7BzNTMUw7lGvvAqPwmjRpNMCPfjvl05dErf0+xsIjuET'
    ))))
