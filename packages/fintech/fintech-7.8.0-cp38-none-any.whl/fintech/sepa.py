
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
        b'eJy0fQlAVNfV8H1vVmAYEAERt3FnYAZwVzRGRJEdBFyCy8zAG2AUGJwFl6Axog6KuO8rGjXu+56o6b1pYtqkTfv1a5tp+6Xp16RJk+5rbNr85973ZphhU9vvF3m8e999'
        b'99zl3LPdc8/7X9Thnwx+p8GvcwpcBFSGqlAZJ3ACvx6V8VZZm1yQHeccwwS5VdGEliqdyQt4q1JQNHHrOKvKyjdxHBKUJSikUq96vCS0ZGZRuq7WLrhrrDp7pc5VbdUV'
        b'rXRV2+t0mbY6l7WiWldvqVhqqbImh4aWVtucvrKCtdJWZ3XqKt11FS6bvc6ps9QJuooai9MJuS67brndsVS33Oaq1lEQyaEVIwP6kAi/CfAbRvuxBi4e5OE8vEfmkXsU'
        b'HqVH5VF7QjyhnjCPxhPu0XoiPJGeXp4oT29PtCfGE+vp44nz9PXEe/p5+nsGeAZ6Bnl0nsGeIZ6hnmGe4Z4RnpGVCWxE1KsTmuVNaLV+VWhjQhOah07wJahR34Q4tCZh'
        b'jX4+jB8bCVlBReAQc/A7Gn570+bJ2TCXIH1EQY0a7tdoZIjmpcZ+PKY2Phe5h0GCXCenyWXSQjYV5s0mzaS1UE9anZXZc4qMSjRyppw8BLAy90Ba9BI+gF8bTdbnZhuy'
        b'jWQT2ZKvQFqyWVaAL5O97mgogg8K6XIrfa5AcjmHjy3Aa9m7M8kpcnd6dhJ7Kz+btOqz5SiK7JLhe2R7kp4XAWzE5xLJdrI2d/QYKJJLthZCPRGDZZPxSdLmjociw/H5'
        b'uWRDLS2QnS8+15JLslGZZqijP63jRAg+oEpx0qcAimzhUGg2j6+QXXgd6zBum0vOh5FrEeSmE28it+vJjWW4JSIcXr2h6j9UrsIeQc+5+0DReeTBwBi8l7Tk5ZAtMiQj'
        b'Dzh8KMICT0fA05Reo3PxxQQYic25ZAveVEibg1tTCox68iBZiWbNVDUOmQKF+1KoW5aQNhjrLfl5hQqkaMQtjRw5mYeb4HksPJevnI9fxqeTcoyGfGMyhzQxstAp6fBw'
        b'AO3TOnxZTY4NS8oyJJJNebRPYWQ7Ty6R7fhEBddhiY3xzf9uip7ByIn+U/T0JHj0nkRPksfgMXqSPSmeVM8oz+jKMRLScs0hgLQ8IC3nR1qeIS23hpeQtroj0tJG9+uE'
        b'tCYRaavHqpAGocjUES+rims5xDK/OZ4XMTnzc81d01QxEy9Ro0jIS838Rnx6/6Fi5tdT5Aj+6lJjfzG117AR6CyqCYXsUYvi5L9f+cVwhD4a+Uf+1qjKlStQTQg8uDXg'
        b'AHdjhiUCTTOP/qlj90SZmH3uhT9GmCclDuKLfs79K27CohbkRe4keDBnpQrWTkvK7IQEsjklC3ABny1NyMkn2wzJ2XjLCmNOPofqIkKe06ncGVD+JbIf73W6HA3L3E5y'
        b'm1whN8g1cotcJTfJ9Qi1JlQbEh6Gt+FmvGV0qhG3jR09ftS4Mfg2viJH+MGCEHLRFerOoYsc3ySHcvNyCrLzc8k2WLdbyGZA+E2kFRqTYEhM1huT8GV8Bl8ohrevkX1k'
        b'B9kDS2sv2UV2z0OoT2p4KX4lise3gvCHDqoKfin2O8f6yJusUibNL98Ms7laBvPL++dXxuaXXyOT5nd9V0RJ3ml+5QUOOvG2N1taOOckuHtlS8j91bmWhW+8/40r26/u'
        b'Hax4dM4y/407kY8WvHFj+/G9x5tsnFNVEU6mnzbEbs9KlVXFo5ya8Pjd9/QKVxy8n9mLDmd/mI7NMCKwXuWTOHzVOdJFO+MoNyQlwzBtMnBIibfyNZlGGPQ7rhjappWl'
        b'ScaELCMPTw7yeONiY1983kVX7Ry8U5FkJK15oxRIWcbhZnKWXCSb8EkXXbNWfHMNacnCFxHiV+N1+ACXiZsi9JyXT9DrZQ7a04ALD5fHMVMqHfZV1jpdpcijkp3WestU'
        b'r8xtE+hzp5KOV0YoF8U5lL6X9HJvSJ2l1uoEfmb1yi2OKqdXZTI53HUmkzfMZKqosVrq3PUmk55vBwf3FP0ddDIdCnqh9c2gMLQUxoNIXsnxXCi7MmJHtuLX8b0k6CyH'
        b'eLyfnAzlMvD5SZkVfBf4waZyPMUPnmGIvFLuxxDZEzGkSwoQ2glDehe4acYYvGOUMw/6AIPfthrhV6OfZ/lkx1hXLuRz+oX4FUQ85LV+jAdxq3LIdSCynGIMvoJgnbQA'
        b'c6LzTI7jK8tIC300cxrejMieQfgKqwpfH7c6DJgZ14vsciH8WgY+7o6C/LEGfRLNno2PNSBy6AVyhkHIwlfJviQg8dwCEzmNyKuV5Barp+Q5WMu7ZsPdKvLQhvKHk6ti'
        b'Uw9PggW+S0ku4MMIGZBBN00fwqoqXoZvTOZh1V6BUhvgPz63lIFeQi4ueZFfSNnSKfjvwGJNhWS3C7+m1IMcQvbBf3I2mvUtg+yDOXtNiQ8vgye34T++OpZxFrKjNzmH'
        b'X5Ph/fgopI7A//nkOAPuylUQeHAAUIPch//kFXzQ3QseVI2dj1+LGAVLgLTB/7gJrHgv/ACw/xUe7zNRASiMnMT3WXFyWE7ul8jyyF2ERqKR/UaJnd5kxU1kl4psLgSq'
        b'jFLxy0PEBq3V0MEg+wCRgNSdzkUmvLbWTZcwvmOuJded5HoD4CA5A6TxODeM7DQxShFEqPhAmkIFgyrUiBZFruYauWaQHR3yRm4Hv0xOyRFbROxylvfyyaleruIs174m'
        b'2erwhk6psTldFfba+qnzfQtRCVDUyP0cbfP2crIzVxJJGI/PIrvxdaC3mwoLyBY9viUbPZq0puKWXLwTehBGLiD8OrkXhq+Yx9nmPnQpnM1QzZSB9uGtk7U4NXLG8pGD'
        b'34ycqqj6SK7/bHrIz9SDZ3MXF7385ifa6L/mb8qfMKbwYNWKWxvTz8iTfnj46keHjQP6mPq8GTn8HfV/vT24KnnXVnPVnXHW2Q3/tbHX3+7vax52//DykfLwRz84P+v4'
        b'rPPl39yz5y33hecds+vurC781+LFB1/6+lb6T/+iOnlt5PvfLnnLCBSTzkT1ZGPSCnIuWU82G6C7+AI/hhwb7qK8GG9/Ad+aUA7yCGnOzitQoDB8lSdH8FnczOipjJys'
        b'Iy24BV81gKQGoqJyMT80fpFrMFtn5EIa44pkMwhgQC8vTMHXchSo91gZ2TmZNDMIHLkbRKtJEz4L9JrcwJs7EU+9vCM17TB9Yda6CrtgNVFyyggpFdBQlpyTc2qOR+yH'
        b'4/+llKkhJxTytHwkp+U0XBzniAwgtJzTG1pnNzlBG6i2Oh2U9TsoYercIt5BV6mjl5++0mqy/fT1blQgfaXC7eriqkAEwidHGbPkKJ7slC9fis8/gcoyLhxEZZ/Mh6ue'
        b'jg+HiHLWi/Oj0MQBBXBnbpwT4hClpxXjs5DZMpxDZnNo/+G9UCbLXa2IRI1zpiFUb9b8oo9CLPoHXShqE0A1ijRrPteNQ4wqTetHLo7Bl/DuVACHd6Fy0obv2L7882+Q'
        b'8wV4/OOvBn9u/rW5ujLP8m5lwt5P1145cO2FzULx/qa+aXGxqQbhU+FTs2G07FrfyXF9RsceSheK5xfHlR0Ylm7YGD03MvcwlQrubripFPgF40tAIlCioT+OWTdsqZ5n'
        b'+A0Ky+nqpNXk1Xbubkx+0UXVBOzR4ONJydmGRH0yyGpTc8gmhOJ08sV55Kieezqk61VRba1YaqpwWAWby+4wSTyczX9ZHEM9LVwBxXoHoJiswiZ4VRV2d53LsbJnDKNE'
        b'1xHjxzBaywI/hFeDMCyJUXpyRwAEywLVB28tTAYpdJOBbErBsMaAqT+XgG/hQ0py2oU9nZQGP7oxoY8DhGsX+jiGbM8o1NMWD++EbENEZAsZ1RuBLlY0K9TcGFUwScKr'
        b'8GGRSAcIZFll1sQkyVEpy70dyST4yGMZZs2JYXoR2y6mMlW2+m8yc96H/Gwxc/tADQIuEvnWXLPm1IL+YuaNIdFUYZ//p5nmKY8mGsXMxLkD0ESgD67F5oV90paImT9Y'
        b'qaPmiYkTG8xTZg5zSisgZxjKAv0hbZq5vD5uspipSU1ARVAyvcJc/qNZM8TMviMMCFjHtM/LzNOv9F8qZqbLmPaS9aHRXDMhsUbMDJWHIpjaojV9zZq/97KKmbNnjkB5'
        b'0M7+Q83lz9XUiZkfNiShUmCek/uap89aZhMzfxMVB+wUpRaZzf0/n7ZKzJwSx5Qf3Y8qYEAG9BEzvwjTIkD2ou9NMBt6xUpq0vpe/RBM8ooL8eaFCkeOmLkuZxCaAj3q'
        b'O8E8ZWM/qUevjBhKJcbq15TmIacMZdKAjIgFAQZVHx9ubhwzNF7M/G1NMloI0HulmcsHpWaImdqicaga+n472zz6DysGi5nXB4wGTEDVg+Xm4j8OmSBmXo5KRWZYfktW'
        b'mflzY59D+mFMrHCQM/jgGDQP9J1RaBTZU8FysafKOUZO7tVRS8docmW2m1LeMXjr3DF8g52qv2OW4/0sc6SNbBmjHA34PRaNJVca2PvW6fjqGK4SpmocGgcyT4sowpyq'
        b'TR2jwPuA749H48mpNCaE2Rrxa2Nk+AzZjNAENAEffEFswsMccmaMqh8+DkOGJhpCRCHyBr5Wgq+jcJDj0CQ0KQUfFfO3xpBD+Lq8ENZuGkrDG/Ap1jo+fLpTju+PRGg6'
        b'mo5fT2QQ8Qn8oNbJT1gJIh0IdYfxXpY93JHmVOJz5BKV4WeQnWQDy44FGemKkyO3oDcz0cxisl+UvE4Bzz3mVDSAiIgyUSZuK2UQ8fkChVOGDwKxmIVmycJZZyLIq6VO'
        b'VQmBvmShrD64meUWkZu55Dp6sYYytWxyMJZVQI6MXESuyzMApXNQTmoFy8w3xJLrfPJQhHJRbjh5lTVhZSbeTq4rgSSBwJuH8iqwh+Wn4q3kVXKdW02HNB/lk3u5TLYk'
        b'L+Mt+BC5rsD7geEVoIIG8oB18UV8ijwg12WDQKhFhajQNZ8Bzawzk+uqEECCIlQ0XxpRG740MgxFkVuwnNDsUYNZBeR2v5wwOd6BYSyKUTG+N1Aci8Mz9GGg55SD1I5K'
        b'ZkWw1g2bTs6GKanCgGDdlYK886o4K23yBWEcuUBeAZ0QzdGRO2LVbStmh0GLFyM0F80l53GbaAS7JSc7wmT4MtmJgF7OI23kmljNbXKUHA9TLcIPYaWj+frnWDYMb2/c'
        b'gvBauH8BvbACStNqcslafAy3yPE2WIRlqIzcwedFXL00sBa38IkCZQcLniP3a/7+9ddff7ZaQemk+ZeZZsPlpRJNG2+EJQbLbcxQs2Onsw7Z/vRgsNz5PXjS9Jum2m2T'
        b'C2TpkTPOV8U2hcf9aUHc1IZfyLYv4+qmmbfrXjwwfFjsrOoRo7My3uLUDb974+WJysFbZENKZz/Unlvc8MHeje+tHoMXJfXDD++1zT1y9HTphps//Oy9+a+8nXY0/LHm'
        b'x0JL3Gu/eemD7QMyv7j29lRVnOcH/Zfl/Xx9yXcmfr1/xPdy//ouvhj/9qlltnn3Ht5xvjN80ABS9l7VjQs/nPVh311l+3L++veBxsTHv1++p/DctfKYb/1r2fuX3/tR'
        b'3jerTnvuff/EwYiD9pJ3frP5wzP7/2Jag37xrbSSijdBpmU2RNCDMkiLIYIcKqC2sm2g8Ifh8zzIAmfJq6ItAN+f6lP4B4PGBVIBOUK2s9fxkdxeIKaBGpyPrzmNOdSQ'
        b'GUXuyEC9vI1vMMEVRNYTZCMgyZbcbKr7K0He3T6R72vDO12DaBUHl8134otZBcYBUQnU3km2yVAvsl2Gr+Db+KJe0aVYIe9KBggQNrSSsOGuMFFJl0kaNZTRChpODsIs'
        b'SBu8JOgG/nD/Rt5XSqUcZIo4qDFapgUpJhJEZvrXEetrk14Gcoy7oifxhXP08UsusYz/+ySXo0G2ByokxK/SBMgt+UAjjpKDhaJ5V0/WKvCuGWTrE2QWauZEATIL90SZ'
        b'5SkFZJUos3wrPhylyYDxFpkNuuWFkswyJSFsRDISxd4D4cWIrdwl+PW5Y6jIC+RvExN7HzTYBrz8e5mTmgBH5kR+bi5748r247vONh1vOntg1IZRh45nDdmgj3uUaymw'
        b'VFt3yq/GFe9PNyzb+Napso3at+KVbWl7a9rivxOL3u8V/vrfduo5hsijRuLXRETG52eK4i2+jtf55NcesClexCany+GucLlBgDU5rJVWB2hRImZp6HC8hHg1qEhMgo0L'
        b'mHm5Ewr3PPV9/VNPX1znn/q1QVM/CnJG83i7f+5TkvWJlqL8ZL0xJx9vSsnJzzXmgM4E6ifQ782hwCR2LnwiGgSLrv8GGvgqDkYDZYFovfDgA6YwapCgKv7pVHyA3MQn'
        b'GS6EqcZSgUenM1UWT1ijQ5m2fVeny50TaLO+Oedz80I251eblnEVof87/a0hd7WntW/12lT5VvTpmr1DTkV/Yt6oVUY+v//lMeFIuyVs5IiHoMdQfHKPy2g3UA4nR3jj'
        b'C2oX3RjIXobv+5SYk+QsEDufGgOESZqu7pEgroP+EowCoSIKhKi5WEABR3wgAlQ8EQH6+RGAvriJVhjJEAB9GYQCdM7IFbIDvxakuOAzRp/uEogFK/HZENIMpPfuE/Vl'
        b'WQer5JP15S4307rCAzbZ7iERVLaOSx3RPz43uUBkt7/uJ+02VI5Y1TwkRMwssEvbbpnxit1lU5Ft14Mf8s5cyHlvsutz8xfmR+XVlResn5rPWB5Vpoz+1Dz/jTvbBwNN'
        b'4B5V5lh2mj8V+O+/q1tzvGrnIlWGyhlaMuaViRkjMwYXFTIbeFFRpG1VLWAKM3HeLsUP8Pm8/ESrgUfyXA5fy5zPGJvaRvYAWyRbB+B1KYX5pLUgG1+Qoz7F8vHkWM7T'
        b'qrzhddYVLpPgtpoEi0vEk0gRTyJDuWhgEWqYVC3n6O/HFrlXTot6Q2qsFgHeWvkEqwpFa8dAP/bQirYFYM+fojryjtUgaG4gLXQrDu8lp/CmQn0+bi1kW5DDyTVFGV5H'
        b'blXIAuZVEYguaSK6yNlGmcKjrFRKKCNjhmw5oIzMjzJyhjKyNfLutjpo1cpOKKMQUUY+ZQyKq/gu3JmjyqotInacf1GBmquhd9PMmmOaMGQbkfoK7wSpFP3g2s4BW66G'
        b'r03VyD9sKE5djNJ/+I72xu6zbRn63yRGV7Zc0c8991+fF/5q7B++0bY/etjbiyZPjg+f+uMfvznz7s9jvqlPnPfg/M5fvdWU8/fnVm42NjWd/+iDH004Yc7+r62/+ZJ7'
        b'blnfSa43JDMguYwP1jB7nQrhK7k8PsHNqa5lHIZceAHvFLdz8a5MtqOLH5DTLrqo504uzCWbRpALBni3tZBDarKFx+vJnXms1ucX4PPwoDkFyJamRJ7P4YdJ5DqrVUfu'
        b'jyEt+fgCCKjkLLzDzcIHyfWeJCNlt486oqimytoBQ+NFDO0L2MnLmSATyml4nlfzUV/JlY5BflxVUFwFBKXo51VWuF32ykAy1+XiABymNk+HLhhvaaUHAvD2s9hAvGVW'
        b'0nvwcyu30BiEsYPwiemg3R5qwK92z+gmIkneodu6qFLxnzC7cPiN6YSxg0SMPd37W2h3+DsKkG6yv16ZJFk/+uvQtLxWGao3N45fIplE/rkwBEVG/1qOzGbDjZckC8Af'
        b'wsNQdMIjDl7Pq6yXVJJX+0ehYdPy6CqYckwXJ2YWVw5AE+XfoMLVFLNprpg5djLw04TDSlgaUQ1LBoiZizQqpJGfUSKdWZMbnylmvl2mR0UL/06hT28bXSVmxkx5HjVO'
        b'+QwIr7n4/ZBJYuZnec+hFTOmUUDFB7h6MfPbL6Uh13yTEtpZ/EA2RcxMGtIXpU6JorbPKboRiWJmVZIBzV/B2lneOm64mPm/xZFIN/YlZg/9YGihmDlpXDpaO9bMQWZU'
        b'Q7jUpOX9QUcrfY8u9rwD2ggx88c5GhQnPyKjguXWWoOYuSk1Ho2dOFYOTVr40wKpSdXloM0l/EMGfXfY+Ggxc35VEWpL/ZMcAOWcKewrZo5IsqJH5i95AKT872Jp6NbE'
        b'VKF3hQVyeH3EBE56/aV+fZDB9TMVZE75LEMyHB1MBebmsnEwdIbfR0rzPk14Ef25PlEGTYqN6xUuva4bg4RhHzCa9lKylHkzbAiaMTYUFoKZX1ddgmyr38pWOIcDPr/2'
        b'y5fm7MgvJqmaDR//+Mtlv9h5ev2Icf03LPhzaPx8YWPfa3vnfbB/0bb3F67dVa/9zss1P9XU/PJ3X2b/8dCbVYuNv8hY+fE3S999pc/iIz/XLD5+5edozG75c2390R7F'
        b'pZU/UJTYLPKRVx5/SJa/HvOXXocvL5mRf00V9cUPLsToawz1466OP35o2G8N3434ueP1oePQx+8qbh3O+eeDnL726m2W5ZuMMaVbJyy6eu6Oaddb/zz5iX3Q98+3Zc4/'
        b'ef7DvNd3nGza/FPL7axz999c0utw29afGg+Peez5+ax7bztemfrelPUPst5u3VjbMOPAiLQpp0Jeuzup8p0By45V/+1XN99u/fHq5+6McE9Z1pDxSWjSS7/KXvzmVzM/'
        b'2fvBgZYVX5/8JPHRhemo5Nb0ieTrxk/+pHn8saphi+38BIdeJqqir80nVxnLDuTXDWQ3sGztSLbljW8PwhdyDQlZpDWcbM8FEgya7kqrgVFZK16XnYQP4TaoIJFDcjcH'
        b'yuhWuz78CaT0yZceCHWgeZwS4nJL3VJTtb3GRgkro8ZzRWo8SS0Degy/w5jcEMnp2G5MJJMhoniNPBSoNBBM8UfW4a949yt5fw3Qc1BPgZaDejrET8lBRl1ptTgCiHcP'
        b'vIVzDPXTbVrFpQC6/YPojlZ2fES1QKTaOaDat4CuSt0vtpFNeTBBBiV6bgLeQ64qyZ2weZ20CoX011lJ54d6v6EyXghj9nYelBZekK0PKZNZ5YJcUKxHTVyZAu6V0r0S'
        b'7lXSvQru1dK92iqn3KCSF0KE0PVqyAnxgMRZFsrs8hqvKl0QHFans6BCGdAWtfTLCP9UylFEByG/w1ClWuIrymY18BUV8BWln6+oGF9RrlF1JzxThtVZl1YUuCPg3q7B'
        b'V0rg72A0aM7gOJfoCDJj2a8VTjfc6ZYeHbD5ai+cGin/unCv8Or6N2dEpyu+k/DGJmXxNl3jzEinbWHf4ldfz/7rJw1/1efv//U7J/+hnWNpPLJpVZJ3z7KH0ZH/uPnz'
        b'l4/nb/vOjYpHD99zu3vv3/a3owmaQX9+ZB79/hvvXBmOD/Q9MmaXc9RPrV/+Cz16d1BJwS/1oczjYzW5WJiEz4tryregyHmyQdwVPYvvkdbU6A4+JmQXFi1Lk3DztCT/'
        b'durWdLajenqy+G4b3oBfDyNrmdOYWDl5jcebVoW76CDlpo1ISjaKRqlEfJJPXaMWyUAzaUvCLXgb2ZZrxNvwNhUKizXgIzxoojfjmRpI1uO7M3FLISx00pqEd03U43Ny'
        b'FBEicyWQ44xQkNNzylkBAz4rR8p55ICa74t3yESD1WkdeVCP1+KWFBDXkrNFu0sUOSUjLy8kV0UQW/FJfA5KJOtz8o3U/6ylAR/lyW1yFz/oLMern5qetNMLlclUZ11u'
        b'MjEqMVCkEqvl0n5tLNtKo44xSulnVYSE1snSe+LKV3tlFTVOtmsGeqrNtdKrrrfTnX3B6lU6XQ6r1eXVuOvaLR89qSNKB/X9dNDNZHEfjrp+OvT0kugnGVQJ+SqAZGyM'
        b'DyAZnVoZJNVx0i9dC066GBvRElGv4ArOcl61SdomhHu501pT2e7KIA6ZekqNpbZcsEwNh1r+RGtcFemD53v0VACrAKCe8ypMdMQcRj8UPyhHCly08KojFXVwxeiuzkqx'
        b'zhCTb/y7rTfimeqtFutVmcTZ7LbWyC5rDRKkqasstRgB6Xx6EbqT0kf/8agjqZMV2D5NXSFzUqry2lXyuflT87ug6Gsqf/4uFP2j4mX+zePX9Bxbnqvw7YUByxNW+11Y'
        b'n+HxIkrzXS6XcJszwH7X7j32EvzErorxoUFQKdELRuZIprW0430gAKN/DKlpBsRf5IwS8Xot+r02ELO7BgEknv7ThwH2mqjbmsnkDTWZROdruNeYTMvclhrxCVs7sEAd'
        b'9nqrAxCPrTG25NoX2ljWWermZnE6K6w1Nb6V3nG1nqW4JhaDIqwLw+DyNzoy1IqmVjB0+jqql4ZjPzwv+t6WDsJtBROcedn6HGOyEoUuAdLqbug0xWHSX+cWLoB5c2Wy'
        b'3bLdEbsj4Td8d4SNr+ThTvoR+FalYKDMPcDrNhIYK2XvIcCo5VYFsHfVegTMPKSVBxavEEJZOoylVZDWsHQ4S6shrWXpCJYOgXQkS/di6VBIR7F0b5YOg3Q0S8ewtAbS'
        b'sSzdh6XDoWWhgP1xQt/16jIt7YlABYn4Vo61WQNCST+hPxMqIuDdAfRda4QwEN6WlUWynkcIg1p5wSiZT2SCThjM+tYLyg9hsIYyWFGQHsbSw1m6t/j2btVudaVst1wY'
        b'0SoTkpn4ITrR09HSeiIqQ4QEQc9qjIYaElkNSayGGEHG6EEKiDgVjFQ+HhmqC/gn5Yre/UFP9Eqv3AbCqVdOMbErxCuoUAVMPl0sWt8apw64kqwUQgdQmlifm7W2UiuR'
        b'ExWTnNRATlR+cqJm5ES1Rg3kRMbIpPwjUNRQUPPov+w6m8tmqbGtoscSqq06i9QZGzAvS10FPdfQ8ZW0eovDUqujHUvTzbTBWw72avb09AKd3aGz6EYbXe76GitUwh5U'
        b'2h21Ontlp4roP6v4fgJ92aCbnp2hp1UkpGdkFM4pKDUVzMmfPrMYHqQX5JoyCmfM1Cd3WU0pgKmxuFxQ1XJbTY2u3KqrsNc1wHq3CvS4BW1Ghd0BlKTeXifY6qq6rIX1'
        b'wOJ22WstLluFpaZmZbIuvU7Mtjl1zJIN9UF/dA0wZgKwsc7NkYaHzngaaxe98x0e8Q0vKCvAqrp9WeLI4vtSAsaopNA4ZtT48br0vKKsdN1ofYdau+yTCEmXYK+n51As'
        b'NV0MoA8odEeCCHddt/hp6vFxYrEuX+rfr0/kwGJt4v2/UVcnm3tnA6qmgB3dmAlS6A5lATU3GpLp8Y7ceaQ5lx1DGYRPyPHrpLWRGSD2pW5F/XsBr081F8wrXobc1MqL'
        b'9+P7+CyzOxaRZiqBp5BNcFdYIlZCDoXPyaL7tvn52fkcwpvJiRByi+6rsDoPv6REGs02anzRvJG7GLkpp0xfBiVayJakXOrnSPaT3Xmzs0QxnMrgZKcen0Ul6Sqyz052'
        b'i+43IaA09N8E/TQbEtPniwYTRa0CqSdGydE0s2FxhQG5KYMmp/CldLJ+bHv99IAOPYoCDU4pziKb85RoFjmlJFcz8QO28bgQP5jnXEZdpbfpSTPtwqH+tsrxHyuc79NR'
        b'ObNt+LbJddNHRc58+6+vb/tyve7U4CRz3y9eHl8cnzRze4LmlK188z8atv/x7jtp8+N/VODMnLq88dTLTd+t/OPv990+L9/13rZvFC26MrL1xbTb1T863KpalXt5ZJ+I'
        b'Py/6S3rduoGbx72Vcqg27/33fyeMn/mLmJ/VfDmw4Y/2liN/njL9+YlfFlbNE4rr9GNH3f/q2vIL97N/Ydp58MNffvWd95L/Xv4L2c+WmyZFvF++RLX3WEXUzgnbw+Y7'
        b'+p57Ydylfqb4CZGfaF/ftXDspWvv3Pz4Zm1NU/9vfnjsV1dzZmRu1Ecx1cRUFRUGw6PPdxPPImMi2ZzCoxjskatBMTvLnP14fLictBhEfwB8L8fvEkB2T3BRjR/vwE3k'
        b'Wm5yTr4hG7eSbeJ5n3h8Qw7q/Y46O2lhJu2ZeK9J2ohLlLHtVrIdt7IayF68C2rw7WFN7O2rJIasl5E7i8kp1hKyi9xSiDt25JXZyQEbds8/76II1SeEOsVuJduSyKbC'
        b'fni9f2c0F3q2VfQlmIWvqkAdvD2XyY5uJ74n2iPI5mljASXCZvNkq1kQlU4PB0jf4muMCaCTgxy5R04MZwpr0URo+NXJVPak2CQjhzi81RjBVOEGvIHsp++KK8wdrSD3'
        b'eA5fj2GjzpmjRI0TSuyV0J2pnHg7ue+iXHSsE1+hKmWrnh36YiN76AVfdUn4uoJsAO3xKBvaWeRBYeRSVmMeB+04xuHtVYtE3XUXOYG34Evj4WlyPm3kLQ4fypjIBtSF'
        b'r62mbaR+xuvwDXGrQlslSwshD9kuBbmvw03wZl42voX3ixKeNkOW+eIi0Q/09SGj6PsGvLVuCXXrliMtPiObgc+R875NMe1/bDDrKLuDaGwD7i7pulk+sX2UmjmNang1'
        b's4PJOS2v4WJ5ahHTcKLnMnXFUHb44eGH3X2lVIL+J1LeZB+IAlFaDhGF/ufpZRry6bMdZO12leCpFXi9SqwkJrh2Vmeyv2ImjU+Hy6AgheJ/RwQqFJ2a/tRq5lmqulKp'
        b'p1tlcL5PGWyH4lOQHw8v9YtIlHmBOOHjXgkOq0Uw2utqVuqTAYZMsFc8tYpKdXZTua2i2yYt8DXp8TDaABCweoT/LIYDBdO8uoW82A85qWcp6NkbQHvuoGbSboFb/MCT'
        b'A0Wo/wR+qAR/CeczO/CwxCyieiqiZ3etEYKHoifx6tmbwiwVvKPQvyC6a0WVvxUpTyOY/Wct0ffUkiX+lhifLNQ9K3KIS1VsRXcNqPU3ILWUaSoAO9Bcp5OmVVfDTnF3'
        b'24b/zM4jYzYx+eMTnaTVDKppOHW2DivVabXWstPjoN4wBaTTi/REuaR1lYCWAz2b6XbYdUWWlbXWOpdTlw496SwcJ0B3odPwYsP45NHJqfqexWf6T4E6W91LpRPN5BK+'
        b'2C+JsTn5NNK6nMPn8HW83fava3kKNkp37v7sc/O75VmWR58kFH9qflT+BaT48k+i34o+vfgT7VsrlLpt11cM3v/ymAHozdMhYyf108tFyeZSTIPESEU2uoxcZJyUXMln'
        b'p4LSMslRv3wUIB3lkXMgIOGdy0V23YRPDQg4cE0O4PPA7VeT28y/Bd/BzXhbCLmTy+QVfjGXkjm0JyuZihqnfIeCJJeml1BDKBdLTbMSJ5DKiJzSMa5jbe0mMbp3VR/E'
        b'wXZqg429wTWCBDENCj7BWYnaDZCHe2pnJRkj9PLHnk64UGJ1ibYCd43LBpqyRNvdTkk1ZjETXA5LndMSEPugfGWnimgdacxqkmbOhzJQFfyxVFkd5icocPRfZ2Oo5AET'
        b'wm/L+imayFO97BeLXMhNPRnwhrEwz12oZbhtsqiZdaWW3a+1Xbh8kGe+EN8Pn/+5OQdQ1lD8mflT85LKL4Rfm+Xf+16OfssHhpmJwzX6aQ29i042TTo6asNg5l6X+EXY'
        b'vuZrel7c/2gG+BckHUJSIMjDcqZDLMAPXNTUT3aS9Xh7oDhLDtqZrhAozoK8vldye3rS5qjT6jL5Zolx60BnKvrD+cS+VX19WNXpnQIfMCZpUVTr2bmKlUj2ozM96bgq'
        b'CJ2bA92regD81JsKIIxog1/tlvJvDGY9T4vCyb6DUpS+de/nxXxmmL8MNTH6fWae5OXls9CBUtLZQudfbnaHrcpWZ3FB+2xCd9yyzrpcouOjkkd1YQfp3vgjiBYW1nWf'
        b'tyYAStYVW5e5bQ5pZAS4q3DpBGu5zeXs0uBEFzu0wGmv9cldNmChlhqnnVUgVi0ObqXV4ezeHOWuEFuUMT0bmLNtmZvWB/JKAmXEOoevVQAr22WhrPnJNKOzo6W6wE23'
        b'pclV/DLenFtAN9tJS3hFyuyEAuPsLP/ptmLSnDc7S1asx2ezdYvLHY41tsUhaHpVRC25gQ+4KVPD98mZqEAzSsDbCF8je+YA59rDLSM38S65eh5p6sf2BYpXk6vkugZm'
        b'npyB1b8H4aNLyH43VXLWkJMWp9Y9N4vulc4hzYa5zAegBZ8tzTJQIFtmDMvOI5s5IFcn9Svw3mHkdClQlT34tqZo+Gi3AeqIwA9TWKNwG3kgNazeX2fRPONcFSp6SYlP'
        b'4kNVtq0bRsmcdfBW5cMG47uvhY/UrE3VzJz9ErZzmZbIuLVvKXi9wsJ/f8qttflX+Vbrl5/Gl99w/2Ptle//z6Caw18Kj4wRi/h1d6r3ju3/Dfn3S5YZ57jO/9b754/G'
        b'3vN8N+f8743OzWsut730qw8/Uf76+riDZxYsXvBIt+/LdH2IyNw3kJPQypZ8eubBkB1NWhUorI4nh2bh/S7qPIF34GP4RlgiPTlBqaNIRmdxPBqEr8vJ5Rq8menyKgfe'
        b'KVlQ8GF8T3RZP0KuM2NF7ShyN9dvPHORTXKkiZTFkAukhckGz618PphIA4WeP0quTlvO7BUzokGuaMnDD8nFgHAtY8lesQt78EFl+4FP0exSjrfIF4dlsqYVT4JOtBRa'
        b'hwdYILCHHBAdbc7IjPAQr8Ub200QZHe65Df4VO4wlIi2EwrfadEh7RS/txqUeJHqayTaL6aUHUhxUC0FvjYwuu6nhD0xAllAsXZusAgu1C7JNssYN1iLvozulh8ENeLZ'
        b'tGKgaN1ygeN+LjCKKWTt5K4nLeQZlBBpq1tOj9J024qT/lZM7pLOZczJ6Gji76I91A2p1mGt9Cqdtqo6q+ANAQrtdjhA3s+skAe0lVq8NT4CmClyqvZYUsgTJnnlaCo1'
        b'Et+SNyuAbymAb8n9fEvB+JZ8jaJdgfnoQI98S4yhJcp3jAUE6jTd7y/RPokMwPeu/+hA91sFbATEt9grMHo0z0K1umRdhqWOqk4W6Vn5EmBlXfIwuosFbKWkcOL41FFs'
        b'/4ruLQlUUwWtqlvw/oFP02XWWKp0y6ut0u4YdJj2ub2Er1Pdga+zu7oA47BCR+qcabr0joKzWerOUzDBzqpbaIF7JqU/54AKbmRMcBP8iBGHgA2SZokkz8mCrGKJr3Gj'
        b'o/AuvItczyXXc9BwclJLDuITGe7JUJM9C2TqZGNijgOfAUIbWIPEYlNmZ+XMSZACP4DETU4N0JAzuGmgKML3ykbbV8yQIbN5SbLQgNw03BS5GD6+640VY05+SaY1UH5v'
        b'KQkhD/WpYliNbfgEcMgWWspuzWJ272zKPZMoP21n16A2GnLykrONiUpEWvSaZdiDr7CzI3g38O/tft5+egQrT7tD4ScALQcJ3aA35ijQKvJqCG514R16GQs2Qk6Sm3oG'
        b'W0YuklYkn8rh8/H4rhiv6xQM+Zak5UvEGvKps9YB/sWVA1gsB3x3NT6UlJNPxxEGkSNH8RbUe6SMHKIDZXtvcb2cxft45YVXB3zntXCSqpEXFZtauNEbPI8iP/v+262J'
        b'd0epCyPvmhuyBtfG57wXE3GHZCe+8bfeEz8fM/ertpPlKwa8YLh8rvLcvqJRP/nZH/7X9UF+WLnnt3uPLVlzsPfOBeO+2ptQ+ofcki3fGvyDRlVMVM3xprpF3rDrqnuZ'
        b'xobtw98+dvFxxYK3Wvqc/Dxiz52k8kF/BzZO0WoRbp6ZO1bDGBxfzo3CW4a46L4avpBKXg8jp2s68G8f9ya78QbGgXEb3jXWhPf7JQFJDIiqZxwYn3Dj3bnPkavZ+Ykg'
        b'W/FIjVt4/LJDMrXva5zQgX+Tc0upkvV8pHgO4Sg572K1kmukSYwfZzKxfQqzhVynOyLMB1YZi0/V8EPwvgTmIJdrIleYm2yhGHHEwE0gR1HvFBnZQ+6pxXZfwfsU0jaB'
        b'tEVQmFklS1ucITJPzf+RXT+MMkaJfDDuntzO3ccqWTwItZ+3h0q/GnZohprw+X+GKlb1DmSyUl0Sj1eK3JqSDYdAL9ZgRh/ybF68crEmq18MEPw8sAour3aQBX4yJFAW'
        b'6KqZz+K+pfa91C0PfuTnwYMp0wCSyliIn+cEmv70cuZ0xMMvl6mPdVC7ioMevHNQvY+6Fgr2CpOJbUE4aLAxtlXhlVH7/DSa7GI3xKvyWZCp2Ycpy97wYFWWikwBslQV'
        b'e8vXLzZlvf6P9o66QzkHJaN96UxthBs1L5dHi0d5v5bzSJyOrweOZ8j1L6Xs3/wr14ZquKhQSIlRdOShXHRsxzJRnG6QeM8CNRbis5HFemdegSjQcyh0FQ/0vQlf7sT1'
        b'QqW/zn91cKwS+DK5ICtT2FCZUpCXqeBXLSjKQgRlWaigKgvbrdit3h25m6uU7Y4U1K28UAhyUpgnslLGPKGpy5DGGi6ECRrmQKVt5cu0kI5g6UiWjoB0L5aOYunI3Vpr'
        b'LzHYDshf1KsnwtOrUi30FqKpExTUGLVbC3AjhZhW5rXNyvWqpG5VfaQSvaFO6lBFfbOjoQx1sIoX+q1Xl8VA2zihvzAA7mOFgcKg9aisD3OYQmVxwhBhKPztK70xTBgO'
        b'peKFEcJIyO3HnKBQWX8hUUiCvwM8SqjJIBihzEAPgvtkIQXuBwmpwih4rmN5o4UxkDdYGCuMg7whUs3jhQmQO1SYKEyC3GFSbpowGXKHS6kpwnOQGiGlpgrPQ2qklJom'
        b'pEMqgUGYLmTAvZ7dzxBmwn0iu88UZsF9kicE7rOEbLg3eNRwnyPkwr1RKJLsMDIhXyhYH1KWLLBYXfrZXmV6LfPkOhckLlEKID4QnbnEAK0gCdI4elUOCxUBRfmtYqXf'
        b'v6iDF0+wa5gDKqi1umwVOup8aBHNoRWiGAoZVLKEOkWjSs1Knb1OlBW7kuX0vFdparDUuK3eEJOvFV7ZzDnFBY+nVLtc9WkpKcuXL0+2VpQnW90Oe70F/qQ4XRaXM4Wm'
        b'K1eA/Nx+ZxQstpqVyStqa/RKrywjr8gry5qT6ZVlzyj2ynKKXvDKcovneWVzZs3PPMt7FSJgtQ9ukAksaBekkRJh3hlKCfFqvplr5Js4gVsqcw5s5Nu448iZ6OIFvpGP'
        b'RTTkbjPfCMi8mhNkjdxSpaOskaNei/AW1yajgXoFZV8oF4ei0QS0mqtTw3MVvWtG9L1GZJJDrYrjQPZNSkHN1JGQj0xdqSMdHd2keW73c+v4QndCPhsJUcWwiHWwnB7s'
        b'WOKQpTFXspJC49jRoyYEopEAmkl2JZX4dc56a4Wt0mYVDF3qBTYX1SKAF/pc2hhkn4oooiwoKg5bubsbzSKNPk4zC9ZKCzAZPxqZQVWxVVTT2m3iOAEySnAAwTr37TM6'
        b'549jbHVsG6q9NyOHO0d6uWQvl/oZ5R6ffQ3/HsuSU1ML9CpvZEewdOPEUlNfbfGGzqU9melw2B1ehbO+xuZyLKN8TuGuh2XicCBmUGDyA0Uwx2rU46lzxoL/xy9ahMqB'
        b'ZURLtg4dTyWiVREiAjybG4Co1rOmdStR/MXvBOAD4fcBMHZEGjZ1K+utOjNMSQXw/JrkGeJfsznZQXX0Z7B5sFHqtll/9ws6/ZgnQteI2Akc7wMXKYGja3gJH+YfDRmb'
        b'EK/a4jQxp0+v2rqi3l4HKm63TfmHvykVzDPAXVsOSjIMhTQGuvoaSwXddrW4dDVWi9OlG61P1s1xWhmal7ttNS6jrQ7GzAEjKZjNFEstwhI3FKQFgmvpvGEbfB6JY8Ec'
        b'/HG1/eeROGazf+Lm7Ue/7YrYzKmnwplIaKwrKqotdVVWnYNllVvoJoNd3KOFUhZdvcPeYKP7r+UraWanyugObr0VeEYGHVTo2HRL3VJmZne67CA6MrJQ91QkQFr+viaZ'
        b'WJPMdGzdbMmLBIZSIr95HcaWesJ2sXlHo51bXdX2dv5l0DltQEulauhrdCs90J+2uz5KFaXReOlpZom1drEL2KNJpNxup1FqdZWBthc3mwqhwzR0SRyXWx2wPBuAL1rK'
        b'qU9AN1aYINGSHblHHQ0q2gJmfK/Nw68mGbOyDVTdzZ1HDRRkaxbcFs5JwPuqcgzZRiWqjVKTh8/NZS8MxLvxAVAhr5CbsxNyjDSW8LakAnyTnCg2ktO4BW/n0dhZiip8'
        b'gGwXY5numEXuO5Pzc8ie5cooFIH3yQrmJ1eq3XR54W198dXAHYmEAmNirrHYVzO5g3fkKkBIVePX8GbSxETq4mh8xZkgxl0nr8QjBd7GQXs2k1fcdBuTbEggO0twK9k9'
        b'h7SSPXPIXnyd2i0KOXIjkqzPFFvl6T2HNkqBZHg/RzbjfXgt2YSPszjjWdxCZ1ayMQKfpGaNXHxJjnpBs/EFvI3sZAGyQhurnQk0KFKmgBSrOXJxWlGprTbNxjsfwdMH'
        b'RzUxrZPrps/WzPjNPz5Ojzqz/X8WZ72tPTM0PnfHdEX2hi+UxSv63tr9scAZVB/W/XKS88J/r32/V/qh46cv/7L6g/Rp52NyNEdPZGycHJo6/9QXCY/+fv9rW+lvV2S8'
        b'98O+Z78z7b1dxvIjN37yy7bP7mh+lTParT+m2/O9xdUf3fFs+9mV98c2jd2Q9e2VX316+Dd7Dg39W8mDr76XE/p260+0d7w/qY78zryCjxap/vD895c9N9F49Wcr5uMH'
        b'e95q/fysaWDFP7VNE5+/0z/3TfPj1fzo4ucP7X1D34uZM0hLKd7J4jyRFhWSGzlyaQC+mIOviTaFhzPJySQjDP+mlCzSKkOaTNl0ThmG97GXn8fryU7ckgIFOCRP4fBV'
        b'Lb5ONpL1ok/jbdwE+JOTnwcPB3O9yT58BB8mB5iZpk89uZKbnZ+Yr8qQIaWcV/MLmBGkJLQ0lzUH3unDkeNJ+AS+j5vZBgw5Qy7jve0bMAkvBZtw8Ho9a3VydlRSsj5R'
        b'jEu1Z1K+AkWQa7KV5JZWjPewOx5f8Yfvr8MX8TFyBG8XzTNHtMOSpKj/8gJu5nR8hVwKZ74d+BjeOYbaV7INyXhTCjlhoEsLKtHp5ORWH7zTRVVrvBnvwrtz25ca4Oou'
        b'sidFXGyJ5HUFWYdvR7G9oITM58W+UnPgJg6FCTw52Y8cIvuXsDEaTM7ocguNHOIbcslNLn0K3ig6vDbhZnwvl9wld4KOcMaRQy562IjsJK/gE7n5ubn5yWSTIXcsLGop'
        b'9EIi3qrAl8mreBsbCnUaeUhaCvBFgxLJZ3ApeDu+T1rzn8Ez8t85BBkjEkVTMB/gfTxRsiW9hLTUFVS0IlGX0WjmFkoPS4oWJq3oSCrlUmdSdmSyvyT2dAmkwHesih13'
        b'/HdcQTnxVSZN7ITL1x0sSE1BJyN7bAzURQXJ7j1nWNwWFvML5AMuIG4Lz76b0bP3DJUOftiVdJAhsjfpwI0oDlIRBrgN5Vh+iUwSEqjE4JSE/M7MSNpO6CBldJApupYh'
        b'OrO20s7yioXyxCAW7uOodsrq6V7KSiqMdG6ZpaJa3J6vtdbaHSvZ1k+l2yFyZSf7ZsqT2XtHHSpYdg1wX3RZHFWgsPhK9rh5UuffPRGxw7d54hOjqPBjdQZq+0+QAro+'
        b'h64W/ZEGxooRY/uXmPOuq6VgIhGz+9PgsBOHF5v7/3ecS8y8//ztiVvR7wEdpy378dAbjYyZDiBHSIsznFzFZ8J5xJGtiFwke4H/U49u5XIeSB3QyJvtkkVO+0aNUWKx'
        b'pXSjfx4NapUyW3IdoI4DQI9WDYxMIye0tq8H/xw5z0CN31xA8qXo4VU/0g5uTIvutezCn0vnbq+vmp0Wbtu7sXfRCvs3uIlxt2yf/s+W/6le3zs6Ijb2xeHfPd5n8pAx'
        b'343ctaX8dHP9d1pbd8dvmLV/9MXorWsaawe82G+E7ftl3741Gf/p8gHvj2/MLvrslnN1/Q8P/T4x+qOf/P713ywsKd624bfRk2L3KQ9vX33pr7Pu3Pvdr/947B2Z9oOW'
        b'w3/9OD1r0uXIPzk+6vWzj8NWbJj4epFTL/GSTXgHCDh0t39QqBR9uZI0MTZUXYGP5frHQN6b7EcRc2U18/Epxs0UZH1kO5+YSa4AqwhiE0NXiRz6ciJZS/es8EF8NkWF'
        b'WOgi/Ape79JR4jFomo/Qj8QbDbnBhD5NDFOUQtZDU0SOpybHWISjg71FX8S9wwYlFS7s6w++EYav8eT8CKievhnvUvniG8nJDbKRRjgaV8seTVuNj/tZZRy5XsDhKxlz'
        b'WKPCFlI3Mh+npGwSX+rj45TDgfdQYZNcJWemM/E0GxodyDBT+uD1PLmGN3OmFDU+aQB5gu283MfbwpPY5goIoOsUSLmEH4hP4zPMwY2cJxdCO7lOyBNxqxr44UW2OyPH'
        b'rYlJhnyYMBqvPUdBjmSBzLpL5iDNuq4Oxj8tQ1NJGgNjYVMCWdh4kXkp2ckGzdc8H/ovnlf/i5dF/pOXU4YVysJOav0uEVpulVbiGVKlwf5vq4P5Vg8RP3ixbLvvA/1U'
        b'TgLU5Yxt51ZrkTcwaFNH2J30cUppmD5Oq6X6OPxSy1m8wLl4uJc1cbFQQOCDUr7g2Y/54bbH8uHJoyuhO7R1Xo2pzm6SNGanV2Ypd4oGli50d2+kyb8TLhoic3jfeXAe'
        b'Bo5f1cdnU+lQrpO10L8FTSM0NbPPKTTxjsxGjvUHLZU5ptF+ORIbuTbaD3ScW83VxbpkAtfI0rRkpUy0IcK9nH6SgfWRL3g80s9Aa21OaEZFNWM9w4HyU/MU05zpDcwd'
        b'G4Lettr6GluFzWUSB91ps9exufKGlK6sF41SbFAkC5RXwfi0Vy2adO2ObryCtaZ6hxX4l9XEys/mfT6QNDIYYJ6WpxiphHlfFeMbuKA3upx8Nmws1Ck1gsJQUDPoEq6S'
        b'jxVNMjAAUWJtCbSTBrGrjhf9k6oNbqXaZAKYDpNpIW0fk4QCjWPis+7RMIq1xIeIga1QUTSDUQ8A3QGfVCZ6pN/EDij5IGv9kNmjINGM3st9gOMY/rcBJgjccX41G4RG'
        b'binyYQE35SzvOIYkgyHcs3V4pItmKE2mGpfJVM5LvBvB7KwK97eDPnvmZnBsnwGawU95znGKgjrdDWSryVTZHWRrF5D9OJAcuHSG+BbFUt6uE9sAZIFKpSyf3jFznTgZ'
        b'tC3dIC00ybrMZFrC+zzZGbKGAuEMaBgt0alhfkuhhg0JBarxnccQAXQzBHXQzfoAFGiHU9fVADxp6OW+oeem9jjyVTCvzm5GvurfmXOFD/P5qT3POagfpuXdQbZ2sdr8'
        b'ru50aH2rvv2oSzvB7ry2qU3MZHqxy7UtPgvqZ5AgO6zLfvah2zqIkWG+ifcPdtJZWftyY4TVFwLkiD+3Q/Ng/VsEwWRa42cjTJkMoAHscZdLIADTaAOPc/5zaY6b3Q09'
        b'JXWsxqauSV1naE8xHHFdD4fRcZ3CvdF1t53ucpNpY7fdZo+777aWNSSsveNsid3qqdusxpauu90ZmgwF0BmqbfvpjNaFGE2BdHTHjovbAV5tgd2VDRzVSk8cWYV2fGCD'
        b'0d0JGpOp1g3IuJWXdjYQE9uCRoUVeCZkAP3+9Z5GhdW4u+tR6QwtCBmmBI6KrjNa9POPU78O4ySF96FIktKOJN2MS5jJ5HK4rYKtwWTa14Em8zA6Uf4G+4v9+22O97c5'
        b'vqs2M7bKpzy50RpgaTV2u4M151gXre7tb3V7uX+/2bH+Zsd21exKNtTDn9hqFYsfZDK92kWDA5DQ3pFGyAPbWoSCmXJ7W120tXS3G9rVfr+QX82vlkltljXR1svEu8rA'
        b'YfcqYYwANEjtjMa+iQIJrU81oYTWq1heba+xUifgWoutTrB2J52GmkxinSbTZd4XOZ31WMPT89+hX6/q5e+1r2T3EimVA0XOFMYmQyKFPomjK+7EQrFVmUx3uhT/2KOn'
        b'gRfaDq/qSfDq7U6T6bUu4bFH3cOLZvBcIiyuA81z7A+aj+6gg3JlMj3oEjp79NR8n51/vtIDJFsdCDDf6BISe/RMEkb3kELYArZAhW8GwIoMXN30oaMJdWFkDVrfdJUs'
        b'RY5IF2iuzC+EE2SCnDKZPtCQ1XR1UE2Qb+aPi+tFWiVsMBQFn9FKHw9h+8G2uipdvX25uKM8KlX0q3DX19tpLKDHfGqylxsFK6bZN2Ve9TK3pc5lW2UNXExeFdRUZXOB'
        b'TmxdUe9T/7o1QMBIMOAm09vt5EPNQo5qA0dEKiTyJjos+pQOboSOJVJ9zhq7i8YYoy53Xm2w4RrSlZXWCpetQYxADSS3xuJ0mUTTrFducjtqHPtobYfohXpDiA6Jfhz1'
        b'qv1KfxizhYo7sMyizpRfBw0sLVKb4/TyCr28Si9n6eUcvZynl4v0cplertILk75u08tderlHL4wJ36eXh/TyDXoh9PI2vdBNPcc79PItevk2vbxLLz/wjbE+6v+Pg2MH'
        b'pxE7XN6luwnUkUItkyvkvJwL+AG6GB3TjfeigjrXDhzJw5TH6XguVKkN08jUMrVcLdcqxb8amUahZr80R6tmPyGQK/2w7dcRqTon2UJaRXdGdRzeSA7ybnrAq5NHo1z6'
        b'6/xxB49GX3TVSjmL9apmAeBYrFcaBk4KAMfiugohLK1iAeEULCCcSgoAp2HpcJYOYQHhFCwgnEoKABfJ0r1YOowFhFOwgHAqKQBcNEvHsHQ4CwinYAHhVMw/UiHEsXRf'
        b'lqZB3+JZuh9LR0K6P0sPYGka5G0gSw9iaRrkTcfSg1m6NwsCp2BB4Gg6mgWBU7AgcDQdA+kRLD2SpWMhncDSepbuw0K+KVjIN5qOg7SBpY0s3RfSySydwtLxkE5l6VEs'
        b'3Q/So1l6DEv3h/RYlh7H0gMgPZ6lJ7C06EtJPSOpLyX1iURlOuYNicoGMz9IVDZEmMbob7o3gh6gKW0/jPrRlY6bSr5zmwGFpGh0HYpRrwzmIlJhqaN0sdwqOcC5bGxL'
        b'x+fIwcKe+VzjqC+HuHdiDd7lkfaWgn03qBIVcHLWTKmwRTwDJNgr3FQp8NccVJvd4avQ5hLtauKrvq2ajPT80hlSDeZu/PaCEtmVkiOKRVfOrIBQnbjDFniy1yCC9PVV'
        b'8s10Oax0QILqsziZKyhtHHMPaYCaLDU1OjeVsmpWUr4TdGQ46OUgjkuVPkpxqNncWc5R9ueIpCywL2rml4Y44nxs0MXMn8e51TIBWJ5JvMrZVcGuSnZVsauaXUPYNRQE'
        b'UPo3jKU07BrOrlpBBtcIdh/Jrr3YNYpde7NrNLvGsGssu/Zh1zh27cuu8ezaj137s+sAdh3IroOAectMOoGD62CWM6SRbxt6HM1AixaC0CtfrWiUt8EaPc5t55xAexrl'
        b'fdBqeV08y1XSXMcwQQVMfnijnFoVV8tdI4Dpy5t4KD/FNVJQN8pF868rgeY3KppkHFr2RTP0bom2mWPlFrr066AFoltogeM9KiSMExdAp+XS84JgXCLTy5m8vMn0WGEa'
        b'7hzufDy8YyXVFuo81e5/JdpeE72aYuD+tlrJv1EpbjaKYUllJpvgVZjcVpeDRpMRjzt4I8SQ5v4Db44ZlD/RD786qMXcQbdvxAgnZUw6CD4nCRKguKsMNda7HSDZWgEE'
        b'kwxUzCDvsniVplpnFQO9lJ4dVJis4h92kjDc9xr7Chi8VFFNd0RZNFyLy+0E8cRhpZZySw0NiVRXaYcWs3G1VdoqmJczSCQizfA/ttS62jvkjTbV2CssNcGn9mks4mq6'
        b'j+uE9rE1C9Wwv2KMYm9/U4chB3kW1qNUVgH3tU5vKDTS4XJS320mW3lVMC90TrzadN/MiDOhclpd0gOn0+qgFbIHeqXoY0ANEV7l0uX0a+gB0Q8a0ZNjL7DZ/ZDKgmVM'
        b'FoxkXhQdg2qpO+V088OLfyOZpUjDPipMr1Hcqj4dRuSZQkCLx2QcnyLUveNoFOhAoj9rXEdQfsfWKaXMT6FuafsZTYMYTcFll860Uu9CAUi3rXIlEOQAQvkMfq5Mn8zo'
        b'qbExvsY+HhEcb4tu6tfaXe0HaVnE0WcIKeTI6glunB9ucJitzmBpiNOnD7PlyO0Jar/g3gaG2OoAVoo3+n8UXWugH66+i+ha/wFoNtAlPYEe7Af9k3SdGGXW6S6XTmsw'
        b'H3YKT3KtkYI49dguJjyJFbG9Sirr1MNrVE5hQW66CAuVrCtpz6u0WSlASXCA2qFAu+ONnxc4dYnSOCUa4NbmYn99QbgS2a5kohgJK/EZ8OOFngYrwT9YYzsHO+kGP9On'
        b'z0tPgcvMZ4jFBiTks57akeRvx5Sg4/Y0noi1PPjgfcf2ZBTPnJEyY+b00mc6ee/4dU/tSfa3p5jNfgALl9yxfH75HfyEknUzWOAT0SuqZrllpVM6c66rs1ZZqD7+9IgO'
        b'rfy8p1aO9rcy0YfqPl+ngAZLnFqXUDJ3Xtkz0DOA/kVP0Mf5oY9kxN1uX0olXPHkPAi+9fV2eioKRCS3eNb+mdDlNz2BnugHHVHqP+Ty9CCk3v22JxCTgylYLaxZS5U1'
        b'AA3rq1c6qb+brig9uwDWeM0zAD/LOX7XE/CpwUPbDrTGXhUMU5eQWzwz8xn4BfT79z2BTveDFn396gSjy26EP+2MW5cw89lgQnf/0BPMGX6YA7qM5qBLyH96gNLy/mNP'
        b'AGf5AQ4WHRpBRKyjB0KkpSJG1yiaU1z0bED/1BPQHD/QKEbjmMQsnW15JtT5a09Q8ttpQkfKReVs6nVD7xOmFxbmZhfMKp05/2nppoQ9f+sJepEf+u86Qg+W/pN1mUAj'
        b'ZlmhPXVMLnT6VfGuIsMD8ZqXnVlK47sbdLPmZhh0RcXZ+ekFhaXpBh3tQ+7MF/QG5sWTSVGmWqqzu9pmFObDChKry0zPz857QbwvmTM9MFlanF5Qkp5Rml3IygIEZh5Y'
        b'bnNSv9b6GgsNYyVG/HgWwvP3noZwrn8IhwQQdVFVEhHTwhajxQmj+CzI+eeeoL7ghzq+48SJGl2yLr39RFp2QWYhTMGMglmU0lNUeqaW/KWnliz0t6RPKeP2ohoJUyhQ'
        b'3LE/5VoRo745vuoJlKmdxkvRWNgRRxGQtd0sFKiLPAsP+7In4OXBRK+d2FFHbx21ZXXBVHxeJmxbZK4E0FnAXOHi2JYh87Gq70/vxUOwdBsEfuVNcDXR8grmOqegb5rY'
        b'tU0JV9Vxjgto/uPJxaIzNLVo+WUcUeRqt611LZIl69WOX9FuLqWXDqGemU2CBjFw1CK209oeD7rD3lEY/XCbVKVV5tuABD03jn1+iTplrurXUeEMeKf7maLWNYGTnHFK'
        b'RZBdTRPdrrDL2vetOqm3fg+Zbg9Fxklz5NDSrd7jiG7tVrXvnEH//0X7KqdGii5d4NSSAcNEv04mOYNQs0BXjRELdt/v6IDGiBF5/aPATF++1ihEPaQbj7waa53JtLxD'
        b'a7owMrByBfqhXW1fMeMH23DyajsYsp73Y0470tT48MUbHmzHUkpmLJXEudl3e71KyYSlEC1YcmbAklP7FQs14tUEGa+Uku1KzuxQ2g5WqrBAI5VSsm6p241bomFJG2y8'
        b'cgzjJPRxjKB3CZw0iE8Vo83xU7h8j1qG6P6WWiYPixr9jKEyVN2F0PgPQ3B091f5tCE8NKFqmVrBPqORn4lvhTWE12v0OeTufLIlqSAvmZ0H2yZDidUKfMVIznQZn5H+'
        b'c65AgVtaAr8esQ8WygS5/4OFCuleyT5eKN6rBJWghrJqD1/JiR8qLAsRQ3OUhbLwtzwN0QG5YaxEhBAJ9xqhlxAFJcKF3mzhRnt7d8D3PBuo6fKAhsoDqQCND0QpsYm5'
        b'cZg4ujlt4qtoUAKZ4GcYcqYUeEP8nw2G21q7YKmhn48b0tGwSSGaAjdSnD4vjxSO7d76KlH76uhI3uim71qZ351K+p5d/y7gPPsZeEdvrgfet9FvMewS2r/xzTjH5J7g'
        b'eXzwnqXGKT3V2Nxtjf5Jp44SPneQ9tjn9POzjue6q5pSi80BHKe7yeia0HfnoyF1qB1qMKdl5Kk1AGpHripBZQT9/4arbn9yHyXO2vFggN/fpgC1O1I5o1wAWnL1Z05f'
        b'S2XOsXDPnKbYPb2TL5U5prgU4s4ZpJVtKuoLyLV/k/qxMVDyraUBA8rbYzCM7NDSkcHFBbtVPBovHilgoWF8p+8YmwC56DCSFqj4hfmp9O55emHeJnSGgKfV14O+7TtL'
        b'EBYAghXtxl1LZhGEXbKAEwRqyS2bnmXpgkOzYYZ3useiUAmL/DgUMKcdMGgkvHg4YE77dgWsa6nM754ZzdaLSMsb0QzUJK4b9p3DjjKw/yV6zoHS0UUaesCDCjU7+GXU'
        b'wbta5Le8I4mObqN4T9eFl3N1xEj6Ldg2meRurQQAq4xdtd9ld1lqgDjRbSnnVLihNN9eWz9Vz3llTndtlwKTgr117Eljw0oV6LUdhaV2xxyGNO340i5XMDFjBifNgmOW'
        b'X9boIfpJGhRaLZMGHTiyUvwSoVpGXVKoywkLNoAvkrv4ML493semA3g0uU42GZI5NINcVOUNJDs7cepY6a9zKxfEqWF+2Y/ssKJMRp1OqMsJ/e6gEEr5MP3CoKClfFfo'
        b'dVhbRj8prACeHCX0Bj6sYMds1TQYlifK07dSJUQLMZCvtKpY4CvxM8QqIY7eC32FeOaaohL6sXR/lg6F9ACWHsjSYZAexNI6ltZAejBLD2HpcEgPZelhLK2F9HCWHsHS'
        b'EWKLKmXCSCEB2hJpVVUia2QT2sqVRcKzKGi9XkiEJ72gJ5yQJBjgPordG4VkuO8tTJJCfdEQI+1faNRCPyNZT3t7oj0xnlhPH09cZQwLrRVSFr1btTtWGN3KCWkUCoyG'
        b'jAXYouHGYujXDIXx8GwygzNBmMjyY4UxbEVN8WooEvqcJbxckZcr1Cu8/KzpXj57ppefWQJ/S718RpZXNn1WgVc2IzfXK5s1vcgryy6Bu6xiuGRkZXplBYVwV5QHRYoL'
        b'4VIykz4oy3U0MJo0K7tIr/Xy02d5+Rm5jlxK3vhsqDur2MvnZXv5gkIvX5Tn5Yvhb8lMRyErkFEGBeZAY7KD1r0vjjrziZC+WCBG75L7o6jLe4yi7jvk9hRRv+UFbrqZ'
        b'TjavJGcp9rvIpsJk0ppPY5W2Ryhl0UGTs9lpxTwDvpaXnT87C9ZFDj3sSb+hOpWsi8A35OR12+v9fyh30nh+L6X96nPzr82PPkmISrBkWWoqa8oNloVv/OAbN7aP2j97'
        b'98tjZKi6n/J3F36kl7EvXDnJ7qwwfNaQ5Tsz2YvckyXhB/jiUnKFBRsghxbSE8CFZDPA5RA+SS6p8SF+RQi5xCJTkosl+YFfbiat+AT9ejNPPLXkdd/ZxSdvVvM+Ku0/'
        b'Oyn+TKRujKuiAzEq+GPIivbNcoeCkqcuv/kK9IqVGOEv5od8jZIqejzUfyZS/Hk/6DsBXbagQh0wzxRk8Ocz1QyFQqWPjYvrTgz00/75THVzCKBVCKCV2o9WIQyt1GtC'
        b'uvvwuMhKOqJV/wI3pe24LQofy/UFJSQnFgMmGY3JNOItixdLp3tO0XK8PgufkSGytT6MbG/Ad92UEeCHGUv8r1JsKzTOlc5t55BWssnxHMzzvASyaZ4a8FaO8F18OSx8'
        b'IlkvHiCPUdIQz5GpI8iq/37Jitj3+oQB0c7wcL6MHJJOj2fhI6z0qzFqFIlQamrlB0N/FzMOiVzh1kJ8PjiMPT1BvW5C+0FyFXqhRLUSPxznZsEwzi0lt3Oz88kFfCDX'
        b'QFr1HAor4MlpcnO1ezDFz5Y5tUlxeEcWPXVOdo1JTcXrzbloCL4pAzQ/Sy6wWDXkVCx5LamAHkFuzZ8TcFw9IdmYQJrxxriURBrZ165XA2/aXs4+NFODt/TLJS3ZeSlK'
        b'2mKk7MNryaUohpYswC7ZjveQnUl0wI1KfEWLlPgeP34paXJPg6dzV5BXksTJmEeO4s0dYFKAsxNYGPeiBLFleEOWDA3EG8LxbXx5rBjrZgveOMzZQK7JyUEr4vABGm/4'
        b'LNnLIJBDc8i9wC9J1kPBaPygNAHmssVgyJ8jxuEXj+u3h7EkJ2Uasm3qfBYwB5/B5/S+kPVk8yR8JM+oRL1nyciRshKGNGVVte1DZ/R9JeB1cgefLQ3oC4XC4808wjfx'
        b'w7BxsfiOm9pfUsPxVrKLvIKPz4bUKpQPyfUsAnH/WSNgsK8ubyA38KbleAc5Tq65lCi8H48PzB3gplSatJF7uNkJ+XPZBwruOBJyjIAFQCQZvOKE9oYpEd5F7oQi7SwW'
        b'VRmG8zC5mkRHAganJYVsK0lIACrYnFIgDUs6uSviG16Lz4ag0bjFPQReXLyCHA0jt8gNJ7m9DLcud2iWkVvIgY+iPmNkeH0dOczGLXclBkJOv5xiTM4i+/CxvAIFisJ7'
        b'ZPiSYzRbAJ+lKGgAJ13qiNaovQPWIBZ9iGzGxwc4+74kfuES4c3uWlv6uhq5cykQrSnVG+YU5xY3TYs8MjBOfeyrR32+/gQN/EZv4dSL1z/7vnrOEu7jJddGlf33B8vk'
        b'lb/bMSVTa86YOueDKZ+uPPZbW1sst+nmu69M1134KEydmDrkWEyUteT8V0fXvXmuZt2M49M+n/UWXzt0wuYpxUun7Sn7Unb2W/+PvfcAi+pM34fPmRmGgaGJiF2xM3TE'
        b'hh0BpaMUewEpitJkKGosSJGOSlNRrCBiAREBEUt8nmx6spu6WdN3s2mbdbOJyUZT/N4yMwxNTXb3d33X/9oQYeCc8563v0+978gPB/44IiTqta0/Xx+fm27XkuW2OjXq'
        b'n/8suFh59vwbXo4zXvvw+I/ypSfGPPxr3sAp+35aU733xYWjpeOWlcG5mGcm1i6W7m32ef+rfa0Jxi/srsq7W5k3Uvqnqh9/uF91/65r/XMjHRIq979fExBZl7jz2Ttz'
        b'7w8J39NmMsJyy4mYL13mbQhevmDuhve/dhn9p5cdXnC6E/hsWceAPz312dZ//HQm/S3XsV+8/W3opc9vuL8ze6rL9/enlV9tHHfT99IQi6Ro13ir0/LnZs27Fbh1WXnU'
        b'qxWbdgeY/WWo77Pqo5PX7n9l6wvrNtR3br/4zwd1zw6//Hxgov/9UW/N+ijhd3sfirGxtqNy238yVNWUzmo9rhrHDkglng7QHZAtGbozEi7uwPMcQaFjbDBZTFAavoKT'
        b'QimhSYJ1yXCBFYDVg0OUOyW9gAkUkA0nOTVPPZ6zgSJ7vJFhZmqcgq1qbEs1lQtWW6ShI/E4xyVqgWpopWBAHlAkSNLJj0bkdBOQ62auI5NKwDLGCAFZC9jbjbEeblFa'
        b'0LVwmdQA81n9GiV4egKWsuonQSVlzzRPx7ZkbE3bPZC8WTlYsnF7CitdgTegmbNZYPlADnCBTZjF8BRG4mGssYeaST0oJ2RrheRUuvdjJRENLvo7BcojoUWQbBNnh0Rx'
        b'UItcOPMUWXiFZKsg9ZY54E13EZoXhrDHtsNF2MPYr1ytGf+VGgo5ZsSxyHXqdJMtadhuDoVQbK4wNcZL5ulkFWJbxhasDyW1D5TJoWOCP39PBRzcZu+IJQGuIpyYKchX'
        b'iOSguKZlvDgJF4AINz5wUYAzZO+U7BQXDoYjjO00Gm+MgCK8grVkeOGCTyAU4D4nv0DKmdoqy9gELayH4RLsncI4PdMhkzIlFQUQ8We+BKugZDWTkEhjrk8k/XBgKCdS'
        b'ItsB3QqsA2SmkKVgFRnmYwxFznSaGeAesurlEZKxRJhqYb08LxEbydUgvLGU72UGgjJYQrq2FOoYtPmEtWR74bRkwUR/2kfeQE5OOenag8JorJNhi9KSy2p1ZLds72Iw'
        b'I4LdMS0ZaOhmDmhyRQ4VDNKrJEBcjJcEua9ksPFchoCF59JGkXacgTPsHUEBwYxHVhSG4VHZFqycywTG2WuMKBUpP0xIxQ6QA8UsVBqI2cv5gqjDc6TqRcFOQ0Y6EgHD'
        b'X0pmZKEE6/EwtLLeSLDF6+Q9l4YG+zn4EpFBUMyQrIfjO1Kp8AZXoRyyyOPsGuQH85PJl/LVLoUTtqQD/bCV89V24F57cmeQAxQ4a7Z2AzgPp0ivtBsYkCnHKiTBm8m0'
        b'OhznfjqDhLOERikZ9WLrVCYV3UjHOrpGuonqUAD7nLvrrfZk5iGZSyXjjOH4DLiVSo0s6UnkJCQPQ4fY+3lyVucHqORCgGAIl+G05hFstSa7QlGykZYl9xEUubcWMMyV'
        b'mZJEMrA1WEMmSilon5ATTVmKt7BqTd9C+H+e95UZFZgwn9JbmJ9jLCoo1atEJg6hiKjkp7U4RGJCwVEYJayJaCGxINeNxWHkbxJB8VAhtWQpgSYSYykRyCVyvThW6qWT'
        b'6/3GTMyDegjq3LbMKthgrEmu0gY6y6jlLYXO7ZQZVDtURkWm6mKW5eqojTEJMT0hVwyfoDsaFClxoqbQFHpw80LYi+Lpr8yUvknU77P2ftSQl7rxx/bdul/Dm2q4TtOu'
        b'fqFadfbz7i/71YbzlMRHGbkf6FzUtowvRZudwWtno0FC6YaA/+tCdUlbles0oVXrHsHG87OuIg59BWPFqbvq9hu5arnDur/3U22Ov39UGIvCojFY/xY7roqOclRaalJs'
        b'bL9vlereyuhYyd2O5HYbmifQFQ9Ga8Liqn8TDWqKzaPGX66rgB2Lj4iL1QREJNAwFNLrMYk00SX6N3eByTq91dxvNYx01WDRWjQ2YwOFi9MFNv6Wt6cUP2rATXSvnNQ/'
        b'FnL3F+u9l22uOohAqsnoYOa5RUGgyTc7xe3GOwSdRUFkFgVhl7hcCwDQw6KgtXv3hJDrn2/Whb05VvwVbLMbVbKP08Q+IAnpf90oi7rHfKht1BuT0uKjGfFsTAqDKLeJ'
        b'3BBJI0X6LEvH++QZHxNJI6hsvFgmDR1YDa4uC0DUoI1rYo/i+sbl1QCRR0SEpaTFRERwWtwYG7vNSYmpSVGUKtfOJj5ufUokKZzGmGkRfPulJ0zttcop5r4m9IBjFvLY'
        b'tW16IWGPR2SPiFgYGa8mNeyNFshSwIQe/4m9hlsaFPfqG5YGaqqWu01S/C3i+fWK2AfWH5EjS3FGfCO6QSUyOdJ5WhoTSLvLGdFLiaSRDi3cLCf2dCHJYjfEMIS0b5kP'
        b'aXePr1Hbx3c7bdRR8etY53b5RGgBevy13E3URVy7kzTIQqZxiPc4RDOFb0z0jtE0epBg9QRoMUjsYYDFA/b6DaMAw5SOKjiIqE/QhuX+DJEVL2G7qQsRhM/+h3lvtb7C'
        b'J+CblQWl0dz1rbMha/NgZsTQExWpFaYgwM7PAc6FcasS/UNwAKOnOg8FSnc8Aofifv9Vi1RN96Q//HX53yKcLL+MeHm9rbVdZEBk/OohsfHrv4r4PCIx9quIwg1+kYpY'
        b'OhGqbBXOV0JU0lT6FBSog/TfjC14vF9BtXMYk8o3Y71VTxJFCVYka3mYrsaw2yAXy0f0McukeBBPEom21vqJbMtk2qk10866r2k3hroyn2DqkUK4CCnTowHon35QC/i1'
        b'Qzc7d5PZOazf2fm5vq05jabbiSOHk94s+bWz0z6Izs7m4aaz8aivSsIssNaRUMynrczcLlKEerg5ghsPm8kAZfNnZG5UExZJeY3JcW+a+Bmwo6V55tzNG3yiAsiE2PTx'
        b'2ZiNGzZuiN+wReUXFRQZFCl+M3TzkE1DQpd/5mLglnxGFH5nZ7SuoVnrG9W3vfc7PEa6zmY6Q59jZG1ibCHbbt33GPFRkTxiLPRO32wyCOb9DsK3FvqSdj/v+w8SsPd5'
        b'EPe91snOvPnhq1I1tWksP3b5b2RZvrx+Y+CCWJPYjwIMhYH/lGCDIdmd6b441HxTL1115Og+tVWNpuoE53sNWo8IDjY6fW7ctr1cIyyUo2uf7odnnJY6pt+x+NjsUc6X'
        b'3sEi/45o0u849D4hZUFhcbsOFRqo6Z//sdfZP9KE7Yoy75cGiwt/3Nwl7vU6AJkrvf/zz76XasdjVPo/72h54/vtwA9MHqU29hFZ+l/pwd4iJZnJb8Y6iWpqeXG1/so+'
        b'8oVhnxM5Y/XTV/afPOx6aI/bSGHcfek3t/5Ojhi6GyRAB+U+dKAGnsExsvkitE7Fk6mMVH2vWWyvmb4IDj5qqmMJlnG/ZhOeVTM0WajGxkBHuaDATgkcGIcX+xm/iY9c'
        b'Bk69VXMeWdvv+NHyJvU7fu8+cvy6onaFXj7IEdo+jxWYD5L6/E2YjqD1+kvyBjDBpJvvP88gbyjzTQ7LG543InaEzj+p/PX+SRoKY9Vr6B2CmMMH2izwJPWbBccHOMuZ'
        b'18xxMHeaUWsmFsMBLFemYCu2mlP/CnX6YB02ChZQK8FrcAay09jwH39KZJ4fHzKIwXDBYemjfD/LvHDvViW0xoWq5Kwa2JJuosY2wU1BHXUCFGMnnmLnJdYmitiSJp/q'
        b'QT4fp7zPmXbM4YfH4SDz/RjgWV9qpRPgpDOcZ36bdGwIUaeKUE3KxnwyN8UtaXSi7FoSqVTLFk2gM06AQ2vhJC9q/zxoUmdIIBtqKWK/AIWk4W3MLzR7iiHtwWSrCREB'
        b'SQsjBUbUHeyLedQbJsNjMeSB0wJUYakJJ/m8ZoDltCmwBxq1jbmCHcwbvHoGHmC91L1zQiE3BC+lpuCVUB97aobnDrL9cMhoJxyHHE4Q2r4Sbrhh5nDc7+YiE0TSGZhJ'
        b'yj6b5kqvVi4O6+ap1QLHLFm8DCvd/OAS3go1FMLxkJyMZR1WpFESn90BEjcBTuARsvwF1wERrJOwafYYLJcGQyVRLgRnPDUx/oeHDx+O2cQcZDN2LYiI/9rNXkijydd4'
        b'ES5Bi7/uZZjvw5jJSwwcnf3CbbGA1CPUVoX7lvn4UhGpOJDJRiG0ffJE0zVQuI2VQ8Slk9RRiUX6N9LJRCUq5+BouKmZR/pA5qQQPA+dJngZzyvT1tFDYiDkmGKBrTUe'
        b'MIVMF4UBZobjMTmWhpkutBymmB0CnXADj2GT94atRrGDtxjjdXmGAgqNgk1ID2VjrQveeEo1GvNnOWG1HA56qqBl7hQ8PAQOQRNcSAsh7xhCZscR6hrYYyq4KqRwKRwu'
        b'r8RKORRgHlTaQQ7ewH0rnKE0bHjcLjhLRgxubBo7HNqhGHKhLfYpzJG62pJKlIzGZq+BgWbBbOtgs63YZLg4RSL4vG4VMSdh3HSBzRoHV9jbk+x2kgcLH9D5SPX4bhux'
        b'XRmFZTNZgQvcfYT9RBU7nRRh7CouEtIoKt0QP8ynDThsJNiYkA9L126GMlK7TLiA1/Ck6ApZWDfLjQxHeQS04gWsDp+Ep1eSKmcOCoOsGMjfgCfwquFGuG6xLRqKmPcX'
        b'DiyA/X1x8vo4+hlYDqJRMtCgIv/jmUS6wM4bYftEszCVyNzLy0dPY7Dq+5yx1NeBbBWO8glkjQ5WyFw84Rbn7s2Es6v9KXPvE/H2ks2pWcBClUkc1MARxhpMhiDL7FFO'
        b'ZuZh9oI2jZM5EUpJ9eiCV0GVCRH2K8hAlIqCBEpFT6wdyjRXS3Imttr7kK4rDuRLwNnP1zGER3ZQbW8uNHQLI/AhWmAy3QQWhzgulQjbwsy3DY5ICyNFJS7D89y577tE'
        b'E+ihUSB9AoJZa52WKNKxbYmPX2CQg2NQOKc81gspYNtzAeSSjTtkANQNwyo2C0YHS6g6vLhGFhH/2dIx5DxlAFNkyJum+jtpHD8KvCRRQi3kwwGjNOr+x/apcDY0WBXI'
        b'cezDl/URukK0TjzHGH3KsHg15hjbEIX2KtT6jIFbPmPcoEkmkNW5xxIOh0MDc8UPFAaRrbPF3EiBl82xJXVLmhgFLYKVWhqsGMO2Y7IS2+aEYtM6unFJyU53QcALHvFp'
        b'dlRm2zbfX+XI9OkgUiVbfcnCEa5SDXeNjQKyzFexFhqb4ZFQKAnDknCyNAzsRDJF90H1WKxjhwvsi8eTynTzMWYieU0V2U1WjuWBLERJPoYtcIU074oaWwwFCV4UHcnK'
        b'PqQawHbJ0KHU0StGzRbEGQLRAnMWswdn4QG47N8VvQGNfsqVEmyEuhmsbSHLyYIqipyncREz/3AIWUHsGNoL7fQwLsRLQwLkzNdKduoidkBOtsTrWDR6lj+H+B8lwqnh'
        b'qjQqXfgTbb5KGxIC52SUM7nOxEI6aBLcYGf4NiKFkUmvYio+xffnnk8DT6wRJkKmQSw22rO6Y/7wAH89wDE8JJHOgkoys4vYCTQayjLsta47wQvrTDZIzcnEq2RLBA+R'
        b'F9T5E9FAy+YDxyc68jOxisgQWOQYlAjXmI9SvkYyaBqZD7TV0/EM2ViK4Egw8+fKponQkIwXWKt9h+I1f2iBc47sEmn16UU7eF9dg70TsWhdMr9CmbTJLNzLYkLgqB+e'
        b'0VaUzF2ytKEaOkmlxkC5gRHumcYpsY6mw0myFTCFnZII9e4iYR6UBMEeQyL0ls9jTVmG+9ztnXwdVOTsMXKXkFOrCeq8oSLupXs3ZeqdEsocPdw7tDPx3fkW12eNUhVa'
        b'xqxyDmkb+NK+2QfuVM6z8S608R1au/KqjXj7RNgocVxAVrgg2oVetdltkzZ3XPKBmev2mydXdpQftXr976+++vIHfx/p/oqXo2/ZpjDV8g2bdgUeG7Bt8ex1W2vdX7m3'
        b'POyb0+NvVTz/k4ONx+0NUwfUSR7u/nRozPX37BtX/PHiQqvo2eM+VidYtaaEOxQvijTb/UNbSfuWmOMG3pUve//TdGvez45zI+cp7Ve0N7z7fEho/JTrd4sbxxUO951z'
        b'e0rqvY6kn/xC9v/tz4PfnLXww87Y5BevBX38x+bvbO8+/U5rpeOGfQM/+Ox23bk3V1oPfu+zZ7Zte/7MR3fdl36ztvL25I+rjOw6qr7NOHsvIaYqJWJQxK1Pa002XgqI'
        b'rZbHRGTNTPR6f7OX0d6Sk/9Y7vR24MHIxpM/SpoO/O319rtT0j83/cMzJ9dEty9OffjWrhNViZuSv3o95/tlL/79B+tK6bKCAz9/vLW5vD1e9tP+v/z98BvxGRcLv33F'
        b'NOFUQOTO27P+dKzk9udvZA+6dN+9wtyx7bVXx456WzpzU63VCI9vLQcWb22//MD8vZZ33hpeDZE+z9m3Fsd6PndoxsLbUc/OcR6X1zry2RFvjQv47NjQlam7Woa8UfDu'
        b'38Xrlj8+62KU9l1N0Bcv3zQPcrl4Iv6w9Zdxo57+YtL3DzY+BUbffJjuiH/6+O2orIc/+32jGGn++ZZx9mv23r0QnNL6faFrweVX5n63d/0Xv19wb/bLo4QDX50sSn/q'
        b'0huvHa55fsCu0O8Dhb/aZ8+6mfPcoLW3655Rvf7VOznvTU0off9fk+vq78W/5Zzw19qqic88dffQq3eO7I4xiH3m9IstPjs3WUz3M36jefXAtYqn4MHLV756M/De0ivz'
        b'fjZobpUPNZOoJvA4iAq4tJjFQWiDIMgGnckCIcaLLKojeD3m+QfDoUWM0Ur0gGw8wXiuBsCZGLIFwSG5ZgtyHcQjBa5B46ZulB4WcJ4Hz2zcyYJXzImgcEUbe0ZkRWiV'
        b'+OKBdOjI4Gzsx7ARy/S2xhA8y7ZGrFvPY3dqPPzIPpCF2fqbI17EAvb8ErITXWaxPTyyB89v4sE9cHksj5Y4GjOICgLu0KQK1BCSHMQSFnriQJbpNXs7JxUWOgiC0QrJ'
        b'fKyBOjw0gTOrHbNabO+E+VCBR7DAgexPUCpxhItQx96MlbFwUI88RsByRh5DSm/jYRCniNBMIzmoABOsk1/hMJ5XyYXR/kRNwJO2qXRHSzRYZu+kWkTeTSsihwsSt/kR'
        b'bERm4RkPe0fbWct8HDXcNTaDuF23E6smqaFEscUUL6tp+F2PSBtTOdR7C4HYKoebg8fw4JKjEjv77tZaLyi39JXCiacwl3O01Fqt8NeGMgTT+B4hGC4OwDwpFC+CI7yY'
        b'43BgClCSe2dHxltoOBOOC+bB0o1QQ+YLnRezyfZcZx/sQE4typ5GZlrdWCXelGC7J2Sxvk/GBkk3IUNtAPl4Ck8zkwIcSprmjyehuuvUGAa86FVY49wtHhoL1vBwLwus'
        b'5RFFJ8nJ2sQiZLKG0CAZFiGzCC7zjssmg5ytZ5Qwn99vsEc5NGss3UPwEl053aKMiOB3gkcaLZjMonyw1GZBz7CXzXiDR77QsBfMHMcsG16YRfnv/DTkPNZwi6yTTGkS'
        b'7h/Cpl4U3FxLhGbKO0fbn4GlykQJHvGGK2xOexjTuMUg7NQ75s5jB7s2YISCdPktyNKTCaDejy+2Kqz06yYUdEIOFQrwiCFr5263pL5kAsy35DJB5Hw2BMuGUXuPfnyR'
        b'GZkA1rhXZjkjnoXj4A24ZdxXOE4WHOvf8mODpWzSZ2AuWVMBUJ7mS/ahENEOcyJY2JFnJDT56xPqjcXsbaOhXmXy70TGqEb8F8Fjf/23Lsu7eQ+oTGbaorhFvUxbk6kt'
        b'VsEIYywYVZH8oYT+k8h/Yf+kJhKa4UMx5jgynDW5l94pESUPZVKKPEdhzGWinFLOMFxiM/6PlEs/WZJPNMLHkrH8WdBIH1KGiYbdj/wkV2jmFClNYqKJIDJj0UEyKY0d'
        b'MpYoJBQAl351AeZKSFkS9pN/yUXJXbk1pb4x0ZTLswN1ZrUeHcLNgDxkiIfzsGwvB/rNhUULxWztii/oSp7q8kQM+j8bV5VCr4ZztTVMydNVykEXdcRsj3vJr3b92h7f'
        b'WdCNw/BRnaQSWe5Y0GPcoNQRKjJI4Cdzg0qZQVn28Z8kfUQLeMSmUp7CyPh4BnqqxwRMKhdHaxUZ3w0LleNlRUdzQMBIm8SYjF6F8tgT24iIxQmpvomxERE26+OTojar'
        b'nDS4tdr4gzR1TGxaPA0C2JaUZpMRyckTo+Mo32FvlmL9SsQlshtjWRq/JmkzRs0zOTlIoQ2FW7KJi1Y/OTUhRR+YaePL4gDIPFTHUWxY8h4aExBpE5WmTk1K4MXqmuYb'
        b'HRGhomg1/YZOkP7R9gf9GJdokz7diZJgLyDdmEE7M3VjZKqutl3RGX2WqGkbA6xl4UU8BoIUQOFru3WRNid2Q0pSWjJDseuzRNL01LiotPjIFB7loeGt56AKahtbmpnu'
        b'QLqAvJZhnmxLJr/GpEY5qdgg9BPlQTs0NUY7LppxZ9FfiT05KDWjH53EMnKTKdRxX2V2G4DHcDiKQl8cjsZBTNGF5rFjWabJEujQmMyhdCC3mVMuQVsiWdzSy0kYAHma'
        b'tASekwA5G9ICaTl5UBSlsSPaKKTUUnltiwtWDBvlM3DClp3YFEIk0AuQCxc9oWLVAt9UcvKfhEuKOUEOI/EoEX2OekHn6O1wzsLFMIGZeRoXMWNf8tcJEcbPe8QKabb0'
        b'gC7AdiJuFhE5JpSy8O6jiS3kBxHVxm6SEXG7AM/DISxiJdRu41kQk/wiHJrWThLijPK/EdU0w89S9rsJL94wzXax8v74x2Ml94/iUBvP6D1T4sVBpq847o/b73l4yslt'
        b'8ZFJw8ZfOx383JSxytyV95TXzN/ev/2Ns190zHpw/idp3k/PfH33lb+es9m7evBRl9rXnOblvPXlG1enm/yrIzDni/eqtz9T+p2ysGOc/MpLo/fOHX482EOlZGLIdiJe'
        b'7+umzyijprKw7qtYxgQJyBsPp3X8vPmihwmWp1LKVrxKRJ8jTECBE3DzsTHDGgElETqZlLw+fKya2lYdbbWAFQNwP9TDESlcgtxdnAuxxjLRHg5gfjfdJ33tUCbxw4VI'
        b'Hxb0LgxzFXnMu9NUdiU2IISHuwuSndABZeJCe8zkGQZVO1xonD8cHaBVBuD8cB7AfsUa9uvpYUlwRJvEkISnuAx7EAtCesmwwjBvaKMiLHRuYVoLmaG3AnrHbu/AJq0Q'
        b'C0R81rjeHhvaYURz8NhyZbKLXV+yy25hBpNYKJT+Q/JdSiUTKpH08O/riupOt+jc/UDvxREp4Xd0HawF5NfT9GC16etgzRQ+tOw/xkBXBxq/Sc6ZdeSg6QZRoE1S7S/y'
        b'T5ovfWSKqpT56mQf/yDr41QNjUnUAJd2R0tPU/NTNobtc2RT9l7g6xmqh4De39EUsz4uSr0uKj6OlMKZc7VQT7EUujFqoxO7w8mbfvdkt/UHrK5XqqZfZrJ4QQddwCAF'
        b'+lXHsGompUTTP5BNv89NWQMU328dnBaGB0QwsLe05PikyGht67Ud0mehFE1UB95GzwtNCK06LS6Vw7XrKtX3UfHYWnl6hkU4/NZHw3/zo76Lf+ujHstX/ua3enn99kcX'
        b'/NZHl3tP/u2PukXY9CNQPcHDU/oJ2fSN5fQxXLyJiXawsdNMf7tucZ/dA1NZzFrf8kh/4aYLUyIZZnbXHP41kaXLqATLd4V0NyeXbquFRcRypFq+nMgL0+Mif1tPLQgL'
        b'76MKXczadI/h9eDLLS76MUKXTNAjg9UJXQM5cfYnKkPBZMd7BoJNhEOUKkBg7gEfbMRcdTS2KyU0+1SAwwZ4ibuQ9gTPxRYXF8yFfS4GgsRXwGNY686ekqZG4Bm4Zh/k'
        b'RD15VaI/3MI85g5SytYSYaHWPsiPqLeQJc6Aklk8SuIqOZ+r4foC+yBqp4B8cXaEq0qWpslqOwotzKW1azVeNhCkw8Q5REI4z732pdgcSC5eSh0IVdhOE5wqxTEbsYWH'
        b'PZyD9h1roVo9mRx0YpIA7ZPhCvemNC7EJjW2mQ/eSc4yCZ4R7bB1KE9K7STNbkGKALMU9jgLzj672SNh1IOrXkekFEr/xwMP6iNUEtYhc6FjDKsjlo3TVnICVDKfxta1'
        b'eIVVEfaH6KqIzTNYqcuWLKbVwGY4p61IBFzngvD+WDjqixe7ag97MVslZYX6To/n78vBBl2v7McTvM/KiNzZxt6pTO965dXB3CuXvcNHmW7kEktmgdRIdIbD2MEubIAm'
        b'uKY0TTHHC+ZkHB3EeSums34ca+FFCruixKa5ZqIgNSEX4FwaxR7EjiR3fyruLlKEsrBb6vglErCAp6BsBxGuizEHrgMZwzDySwVex1osI9J1BVy3NMDK9Qam5Fsg5GLx'
        b'bJuBRDa0NIezWIhX4grufi1VU6DNduny8D/MCXrGxcLgo8NbpkkmH/kqyXr8+Jl2QbcdX0/OfG3s757P9W7O9RQXTB5pMCH3jS0KL+/AV8QZBoOcX7DuTHH75dNtDrNS'
        b'PE3tVfNecG+18n7B+pex+wsrNxT8eU3twjeX/6UmdvnAV9IeVE0Y2PHCzET3S7feGht46ffSJIOJB964cvptLz/v/REzG17YuS/051d3nrRbsvN7t9RY9cPC6KEdf6mW'
        b'Hzn9o9mRke9IvheP7Pv0ruGaP99zPpf70COp4/ehK/8e+kfPTTF/zf1p9I6dLltMY9Z5nP9L58mDf3jln3//g/3nL5zNqF/5XdLdzj1tnxaPui/uXhG67VvzvaVrbgZt'
        b'Vllx82vr7g16Bn1qzT+9ABvXR3CxuMwFztFk2CFwRc+ef8CGGUZXYTFcsdcLTDZxkM6ZYggXNX4Ie7iwbDEc1oj0ogd0WvJSz0PNQpqpjx1Y4mMgyCBHxOyV2MpsosNW'
        b'whmeyeo3l+Wy0kRWeRh/sigJSvT8E1s3UCkdS3h9ZkIW5NtTCz+14SqwHPdikQT27IJWJqwnY/Yyy/VqJbZSV3GRgGcHYgt7ZzheJZtLDt6EouSpZCFgHll81mOZGRMP'
        b'4j68aSnSS3Jyicy7A3gL9rMisdJktYWMXqJFFpBVgaUe3Nly0420U5caStNCJxHd76zUayhcZfrO5gAoGwxX1OnUcw1nKDLIAD4mRVA1Fi7gcTXZDvJpdfYLZHlftuE+'
        b'knw4iZl4ERvJkwbkyXoBj4Ya8Oo0REFzwnKy2k2IBgyNAtYYh3MVpgKyhmONoE7fQt92SMDiWT6sGml4JXx2APk7eRFUCVjoQ3QQKm1PgZJFVHEKg47uuhPVmwrgbD8Z'
        b'kI8ITpapiUzMdIv1fesWEVSXoLZImqsoeSgnOoaMWUm5hVPCNA3tlwnLUDSWaK2Pun/kCXLvQ8nD7QO6xxyTtwdpQU5Y4qKJvkydUthNOWHhhaQ1JTqFpFCXX1hMPt1+'
        b'hFZyu1vkc+9aEI2M6iEsrypINbgHjtQd2bpg36A7ynWe4SEh3kGevt6hHIJThy91R5kcGZeoTTykGZB3jPUy85jpUpeFqZcwmd0dh4rBUlHTJVOzWKt49wz7/5NlPcWH'
        b'6oBSDYykwtBCKhE0X2KvTz/L5WYGQ+ZTe7pM8hvxMWUWFiYSM0riJhMeTtumEK1GKsQ0G7bc10FBjxQCURi2CPKUsrhBmNkrXtdE81NtJ3YndaOYWhxP66hMg6jFP1Nc'
        b'LSPyRT9TfC2KrsX/3vXZgiJcRg9kn62iB+k+W0cPJp+HsM9Do4dFD48ecVRJ6eLy5LFi9MjoUTkKirBZYVghRisrTCoUFZb0K3p0iWG0ax7F65IT3Xd89ASGP2XIaNYm'
        b'5QjRttEqSiNHn6tQVkhiJeSpgeSfRYVlHP/NkpRmWWFUYRwri7aLtiflTaZYYLTEPKM80zzLPKtYBUPQoiUbsWhZOYueHRArj3aOdslRUERPmbBSyXRqtzuWdNF4MmoJ'
        b'Br8WG5PyYHI36bP3DRqWNP2bHjgRUXZmnDpppjo1mv2c7OIyefJMKhHP3KqOnkkXkpOLiyv5R2RtN5X0jiwoOCTwjszHd5HPHVl4yKLFDeIdiZc3+W5EX7kuOChgRYMs'
        b'hRoO7hgwDfSOEcfgjSMfDWKJHq3+Na91pa+VpVTS1VdFvx2k61nmGxTKcRl/ZVnuZHPrXlbKSVZgqNdSjwcLNqamJs90ds7IyHBSx211pLpBCk1JdYzSpPY5RSUlOEfH'
        b'OPeooRPRIFwmO5H3qSRd5TdIGAxYSgSFOiQdFBDs6RGwjqgMDybSSnsu8GU1JD8XR26j218INSKrU0mhTi5TyHeyE9LCGsSUII6WeITW1STUN2hRgPe6BR5hnj5PWJQr'
        b'2asruzX5wfQeD3qmJKnVC5gu072MgKQNgeoNrCRXWpKkqyRSwQZalnmP/ngwrP9GPRjUZ+eplN1KodMt5UIfZbunNNK/9ijEnRXilnKRXuv/5a4P7H9FS+8YRsfERqbF'
        b'p7LuZ2P5H01i6BXJTv/rKw2Ea0z1WJOuTNdE8sFxIkmeT7OLu7TppMASREZ9eIMliAQYCncTZLai6tz4RySI3FFQftZUMqX7T4WiX4s4hGr3rcRJ+2z/+QZEihTmkE/q'
        b'sX0LAZnC77rlHDzqLQ2G/NDe1MfJHa87vumk/ILWIiyoV5aCsbZTqZDAshQELXEox0iLNdZlIBg/MgNBm1mcZdiHVdOXZ/jGbY/Rs21yBiDueqLb8CNsmaFa6l6bZMbH'
        b'wCQY9czeNzra9FgqNrZe3qpH30aX2mPvcLextVPHUT9W+nSnaXZPUCRfvTa2nj6Pv1mzSunNDjaPe0//O4iNrW/Yr3rC9RFPPOlmQIvoWen+zMYa0xe3EfHkaw33k5ZX'
        b'oL8n6YnJH+s5bZJT4pJS4lK3cfxeWzt6DlNWLXoS2/VtSbSj5zO9h56WdtRsbEePOTuVU5erdZrTZCeXmZpb+i6myyvrwm7VlNr152nsz7zo/hrGASI0TesD/oH3zyQ1'
        b'Q4Dot3uYw2Jm9+x9tsj6BnPQZN/3W6cuxIaZOl7Z3qAMFCBB55jvw+9O/yPXGAUgteQzCyoLCoiJTKUTSq0lSNPDuKBu6X4gAKgVlpSTEZmiiSHQ46VgvWMTGhND25oW'
        b'r8e51mdRnh5h3ouCQ1asowRAwaHe6yj3Syirpc5/z5ng+u0kvgnx/mFcTRrIFO24aTU3jf24b3d3l02Z+Sl4CV0mX7see4pdvwEDbISS+TpVcx65HluMHW+d9pa4xL7x'
        b'CTj6BZFJtTS5GyMTbbzDQ/qxjSfahGbEpW4n6iQbuNRHVJ5viP2sJbJgfFMj47exB/vf4ez6n7Ma2A4+IF1oHnTma4ZEh+zB3VT9tCiVxz/oAXx3e7YbKku/uxYrqZff'
        b'gHSPRnBSa6dvj3L7HhMNtWLXexml5fqY+KTEDbSkx9jXqSxi1Et6Mg/iqSA5cBn2Y7k/luJ+qSDB03gOK0Tbtet5cvppOIlNGnxNGvIAR9Rm2D6VRz0wY3D1Uje1KRRC'
        b'lqlEgy0Kx+I46mcmnltNFV8oxnby1RII16BAJphijgSLMHNbmge5a+oGU3/93K6lj8HfDDSA66Z+EmEqZJthjjfWaizdO6AzmBmDmSUYO+G0OG8UHuX29rodcIEakKn1'
        b'GJoxT5xnFJJGiWrg5moPPazVropgPtTN0aS9JJuahlC4VVvHoHBbWyzEYmcsdKDAmhw51JGa+A4OFF2CF7I+MYMyf3U6NJO+uyzT4IEu3838GYPMDI1RQrrWJsLBK3CU'
        b'wJIo05UB+gChPk5+gVhgvY002jkE8wOW+EhDoIAmxGEH1G2bIMAtmRIPxa2Ni58+RFQfJyXUjNwwocTfGOZbeNU/VXZ//Apl4o2yVbcDT+/PfH78S4rbNhWz9u1fPWbS'
        b'lUXTTf8xKHzOkCE5hwdLxsHtU5mLOraHfPjNu8rbGXcPvOCUe+mdytG1YX6v/WmKr3vIu69+9npc8p8v5976+tWX7433ei322mZLi4eJU34eP+Djr3ZPt0362r9iU929'
        b'jpFPJ0xY+OXgf3z73Mofj1w782Fq3QvK9aUT195SbXa+Z92oMuVWyMY1WGnv5MgjnWslM6DFBa45soALK+UqjmBMkZcdfPAcjdIwFMxCpK5wFGuYVXVXqkOXHdcWs1m4'
        b'xQbcywMkWqCEjPqp8O7xIjRaxA5yeMzxWdxv7h8MbVigtS7nwD6eiVxMnq3TTEQ76GTx3jTYe/x6FlibBLcGd4uCF6DVjEVfDN7AblAOxEyd5RaP4BVHLajf1rmp1BBn'
        b'vhiP0RugFK/1AAnUAARGYiGrS1wcVtt3Q3OE6mEU0FHtzLoR8vDkRh3aJN6cIxPhiNdgbgZu8aMQdHS5XSEXAwdgh7gQLsANDgV5Hm7iMbLWd8oCSAesF113jekGEmH8'
        b'b9ncdKhzXv2pTTssuc3toUzKo1kp8odMVDyUS+hPCY0OYVzHZhKJOKwf9UeDt6ZBodko9mU/TugG6xb4SI2rddRjNa5fA/HGOfzuGKxjuHb94U+VGAgagLe+XqhjVXZ6'
        b'Apm3JzgbNUeF+niE3JFRztQ7MkqfqjLsK3qWx6bSUNU7hhrW7ZTrYh/p7Oba8yNA0KWzc1XRRKMsmnJI7TzzWPMnTFrXqoxn+1IZPaKj1d05orVHZh8WPJ2w1VvzjLWZ'
        b'SUXBmRE67JCIPrz2DhrRRYdrRSMjeweS9uQ75HS/VBvvEkhTaS+masT1J1KENCKsjhH3cboQJ8Tiz/ZBWxuptomNT4qkBgIbxs+qIaDsL2QmMrEb2VtPttv+atFNQeiL'
        b'jDY1ZiuXflN1/K0JPKqznzBNck9cNBXdurqiizKPt8HGlvG606Yx0WxsyEInJ6exqn6ESh74wEKOI+ls0mNx1pXMaSq5sNt1vc/ydM90sU5qpoAmKKs7B2WfZdiGeC/0'
        b'pv4Z73VB4YELvEMcbLQ6CCfq7DeQi8UY90/YmpTMY64fUcLWvtS6fphRH1Ec/U+n9dEefpRSpsNa08zqPkvT0nD3pb/ZkF7xDgnyCOitq/UdlvyE+puWPIt3hY7AmE5Y'
        b'zbyh64KovDGMozoiIigpke4Uj4jX3pra9XZGb0v7KDKexkjTDUI3dWNTkhJIV0VH9hNYHZ/GzWQb4tJjErUznyzNaBrAYxuVlKiOI91FSyIdF8f+Snq534rxYvSNCyr9'
        b'ZmronNdviolK5ftB3+pMaPCMaS6uNpxglreH1sFBg86paS/T9unaJJtin+XEpqWwtcZWOyeK7Ven4yfSTJtQjQ6lpXenoefbyFvi48nii0zhmhS/ue+9Ra1Oiopjg6DT'
        b'6JJTkihLO+1F0rWawSYLgU/7vjtTj/zQJojodpHJyfFxUSy0kCrXbD3ph9L3vXY8NSzxXWSr9LC2sSXfVQ429Mi2sQ0OD1HRwaBHt43tAu+gftahnV5uwDSV3RNkLOji'
        b'tDx0W30PtqJHxX92UywVfSqWo4OYOpaI2cmwJ0ZPdTTDm1jLpCCmCZ3bKp+9SmSaUIC7QTqP7BLxejglqhBwb4xGmTw4lStVMnOoVGtCnDAb8imKwcHZPOrrGhR6M1wW'
        b'CsoCLQYCVEH7jLA0qlgMhjPm+kpoApZ3KaGea9P8aQFtO2XI8zgbwiipRpgGYMDf0W6pj4NfuE4bTYXWXgopR21p8h4ARVt9uVLcMBYrupRRo0XiPHu8mUbpXPEGZqc9'
        b'2bt0L+oioVky1dpWBzmhkgszXazwkg9cY2FSAXgVqrRa7kjYK85ba532FK1OE+TCZX8Gx+PoF0w1XV6KAZZhrvGEodBg3KVgzsc9eJRcOGVJnqoNgxPRS6BgwS6ohiya'
        b'hQinyc+9m7fCfjizQMTa9WuhcEFK3JIlm9amTFgNhzdvtBCwdM4IorXthXbeHRehXVRiW7IJEf3xepCMAhxYp1HBeRR2+vRbMSwYCgXz4cB6yO1Wo1w8hRXkM554igVz'
        b'RZhjno0AF5YMGBKDVWwi2dB4G2W6EQslg3wsEJ2dhqXR6TuKKJktOpVftVSDvJOclhaG+5NNzbEsTNPtPk6OZJCOai0C1ApAx0eL0KGBqAmEPXBWwd5khvnWeDEkJo0y'
        b'nI4MhbxHIiPRZ8K6RhNqoJGMKLZCnumiYe4Mf3AVHMFWf30yohK4sJhNGlKqPwMLITOp3EDtB4WW2AKFWB5C1OhCEW9tWYUlpovGjUijIjtRiI9v61WQT5cOSmvpLw7X'
        b'lQi5SqiwmoBnBkE91FkPkgpwOHAA1MHRbWlzqYkDS4N7IhoZwEXKLoInydwvxiuzyWBlYQ7pXRZWB2XrBcwLMQmBYz4MjYbUqR7LtSOBB+C8/RKfAF+Vn6MT4xHp0V3a'
        b'mpl2XzKkx2rSLOHA8OUs7s8Jz6m12A5LtGwqUI21v63sED8rUvNjkMnncTHU+DKeF8FzCTfrJOAxFpXDDF5JPnjWvjfHDWZCI+W5uTWb0ibGrbWokqrriJZlf3Zb4JJZ'
        b'FDHi/ZEpHbVeL7bF2//TULX6Uwt3D7v6fULUR1m5p5XPy78Y+7vLBRERX/ktsnlqsPuC/Xbh+6W1VikyjPmgcaON6YYPNux1a5l8IOzN6ju5ttExJT+N8Xp/4OYze2Ya'
        b'VLypsg+6+4VX2spfFsneuvfJdyc6vV5fueXL8s0pbR3r36g7n7FW/enZ+38uSMg/mv3Kje8/Oes/4YsWj/fj0ysjTAav7biw7ZszO6+1zPZ4uOPk2w/OL1z6tdWcXZ4/'
        b'iheLLyTs9n07WP5dxLKDr4Xe/lby+3VbY1+L2vr7Ca+4fb3r6fP/ei3jo42njyiTvq7xPLIoKSR4+rUbwtwRDx9cC5V/OC75hRcHPb85SZLi+/Jfjj3f+HT4mAdWOzfd'
        b'cx/2Y0X86lHbf0j+2O7tOQvmmW0/dOr9Z6sTrgctbv/LlA8/Wln8xitP7170nvThwJ+ONP8YdH9gy4mEkzdGtl7/8LNyD8/dA96IOV8R3PnV3fknLjYcV64NOlPmP+bt'
        b'Ddl/vzAk6WBe1F+H2jXczzdquP/19o+f9pnQ8svGp//29M4R6X9Wry6o/n0kxgzK+MC1/eOlL73+bvC5q78YWns0f192XGXNoQIOzcZ2jXlofajOOjQKz7DLa3bDBSgK'
        b'DlnSw/IUl8HsLpPSsYlFNEKVKzM7ZUIlB2y4TObmRf8APAb13eIpG6FoOLN5RVmr9Ew9eJLspGRTaHBgNq/xZGe9BkVaypK1A7tISwQ8zkEMTpGyqil23xBtTCGHT1hK'
        b'7qVViB6MVcqezCgDoUym8ASebe+busk+CA/i9W5pTtC4nFVwPlbCIUahxIIytxqJ5HRuxnJuVruFuezgKKLYtL5wQSbI4yVj8TKUsgjDjBRjRjEikDMni6JOwB7sZE8G'
        b'wF4DnT3ND8p05jTDRTyL6QR24r4+GDeEqXCL29Ngz3QeVdkJ+039sRQO4XVdYjxLij+FezgHSS1cGUHucKCMbjKHuatEuIZNWMrHqNbMyL4HucoOOC1bi3uxRRub2jGD'
        b'7HZ5erZNF6yBC8zwFwL16/wDfKGgR86ZVHCBq/JRUOOMJwbw7P2TUEj2CWq/JAeNBOqDiWBh5iWdE4qHmOVvGzksCu3lGi4VnlSGJy24cfXy6o2TsQGKnAMdVaQOcyQ2'
        b'eAPyVYonTl82/+9E4u3VQjZWUaGxL6vgbmGusWgiYfnqEhORZrpbSORShWhpQTPLZQ/lUpq5ThkreA47zT6nMZxyTR66hXSIZAj5Sf9Zs9x2yl9hJSoMzGjWmUTP6khz'
        b'1h9Si6NMYibheehyyfaxfdjgeiRZBz0uFb3LmJZyq3vG2pMPgX4G+a0+0sj7yCDfT22b42nX9mXbzBS+sdW3bj5BQ/uP5aF5lczox6NDhFi5LqpH+iS48w8ieikUITGJ'
        b'RJdVP86yx8wIGtWFKq6RapvlgQGP0U8GUGmvl37iEMRo2WYPnu+vB+l8AhqW9ISXK1pm2ytLFI/CRdNBuH8WQ5zCdiiDo/pHfvMUfWa78lAmN7gQGegmlxuo1LDUj8ga'
        b'tZNYCSt98Ci9kupEtl4nOAdX0skHPxqLPn6twXSsmsrEWYdxQbR88vwoqkFUwv4obGUeuoFkcz+q77/bMkO0VUEr07FeipSy9Bob88iAA4vdBKYtbRlm7kaxJKm2dYzs'
        b'Ya0C3IKbvjzhpRmOkm2ynGwruVIGA+mpkX2w0A8OK41SKC5bgxCBp/EiZmtw2yqgDY7Zq+woGsm2cVgj4h4FNrPH5M5Q6E9PlyADQW4tSRlvQtrYyC5tI9td6RBoCsUS'
        b'Ukcg1dhniuc4ylfzDsgO1cHAxfsJeAFO27LHBhMlLkfny6vAEnEeXJWxvvCWQSNLLtGkluB1V3GMH9TzMvM8Sc+x1BSWlkJOYHFOgpT7B2vICXBUydgUpYJis2iHnUkc'
        b'wqwsiCGqazQ5yvQnzsOSeQyCzQ3ObA2FEqwIJ/JrZXjgomhRUASLNKvGlvX/z8mlwghRGDJfjHW6HzaTK75fWY0TqHD/ddrGsatVU/kfz0tZCrfLH+ZuM357llzoxYes'
        b'W4Q2goYP2ZosO+GEsEOMFqLFXMlQ4aSOGZnImV9QTwBlmvGITgmIS4xp0HAjy+LJLz3Jnal5f41cjx6ZaR/Q6TqZxS1Tf+ShEVjgYKQVjbGMpUyIIdPcsQMLoMAdc9Pn'
        b'L4zd4puyKxH2jBR2TLYgc6llBGucx1BTgXSm7dcu6wMOLRzAWzw42lpwEASL+RbbVjvsChWYsr5yvYk+SGAMFFGcQAYSCGfxEB/Imz6eXcok0QIriTrZ4cxn6SVrOE8u'
        b'bjEl4pLVcrgizloDeex9gWoG6GoxPyU2vmnWLkElYUM/CG+qdLNpP14js6nGk115KgMbdRpkE7SJzgugib3FkRzTVdhCHjMUpBPh3DRxDhxyV4lMC1+7Fg+rg6iAKFGK'
        b'1nDRBk9v/bdGM5aMZgrQjR/pt9+JQi9ybjp+F7uNH1NXShIilenYZi6hLWhMEGfAebJrsHVeH0EkrupAJVVe8AJR7rA9hfduUeogbDHBNkOy8sqFMXCZ7AXZIQz7EM5A'
        b'p62SSBW15JclwhKpC6fgHA/tSls7e2wOEIWgBQo/yUq4SvRwBg4WBgXY4uyH7eSaAWSL6XAMq4jQWh33ztUUmXohqfHik4Niwv33WYVb3Ww/9nP13b179o7aO3TIs5FP'
        b'Tx9nPuC5P549e7o0a9zY7MJlb1ZHJ4YG5ru2r/7DaWujiYOiil2fCft7/paPYZB/1Oqvh/9kkGOwGeEfR88l1kdu6Xz1/s2m33ek3XVvXz/p++2X371uW/HVCy9N/l5y'
        b'eOWLL0aPN3537/vPjXyn6sCDGT+2pbi98+y5gueXjoo8vzYnf8/pyi333Jc7zVh2/8Bg//AvX3h+n+OJ57d5Dxn6y4jPVuwIf7X2m3clhWUq77+2LnV43XKp+8ChUc8s'
        b'/Os7qywKOlMmnTvkt/IFr7CpxxpGWR/IaDaurVqSU/3PQNNDSS9+oVj/ZvOwM5ZT3Iw2l5/7Wu02ed/EyRfObho7a2r4S7UHph7wmWOQXjTM9a2qIRF5mQnhaaFRLwdG'
        b'Z7ymWH+t6F7V4vf2ngo/e0vSFjh1aUKb97Wanz89l7tj3bmJ3wxtbcgvt1qZ/CBj47vLox5Gfdx0Tvw5aZN6otsLP9huTlrQnn1lU8Whsd862j57X/V6jXftlj+7GX6Q'
        b'c3Lkh1PT1+cG/lB+9sXG1Ekt7XcWFD7zZXHCvduhE763gdSvhc+OmcVa+j80TXUeu+KBQ1RLfEHquruqk227Elobgmo7Xv58V5vXg4i7Hm/cOdEh/3RM7Ch5i+OGzDll'
        b'n40PL0ndvdP+Vf/WNa1/9H959rXMb1997+Ws710vPNds5uI2/WxB3T+IzPC5R0Rtbcvs+Oj1eQMvlUbMOfxwUUnDyG2JYXj3aOw929QZm3961fN+WOmg6z77vvt56peX'
        b'6+PM7ZraP/m2tVOMef1W5uHRR8+NXFuX/36SybubJp1aMy7th/LqiE7L2dmK8Hu/5Dec+Oxi5e7T2786tP3r+OBzvqVbyq+7LX0zv3pz2oRT8vuzJwW6Qc3DEW9/u9w5'
        b'c8VHhTcVf5sQfdW/85lRI96XfDN5zu1Rk4ZvS4jdNeXQ2u2fql+23r7jD++Wzp3z5rtBV4s/SJ9Zf7Y9b+a2P54z/N7yTx/dWtxZtHbUouLRd/8WNnyQ+l5J1q3b7v94'
        b'a/FPy9YPuF448pa1wzf/8Jj6Xc3vwjNmPvz6T7NmV34bsc5wrfkHPqsD1V9P/G7q/R1+30UY1X+16dybq94bfjXqWughy+mz5284Zp/8aWLe9o+Wf+j8/T/TByQUnMk5'
        b'7paf3nnIclmT2zR/60Dfu6aBBeeb3K4dd6gue294teWyh76h8PKc0LLPHM4881b7Vr/v/1Dh0rLFL+hefc7hjlPBL8w9vHXHtzfcth4pN2g3+dT2DxlfyJ53/uDHirjx'
        b'a3+Yc+Ffl84O/uC5mZjx+pSH7XuS5JuyHubNX/ZmgOueDYHZDm/I1IN+MTzju+vPaV97+8yLDo69emDCmU/gO+XujyY+9Ln/0auRO4udFl/PDl7fefCPmXc3N1W+mxr8'
        b'Y+7OX24OjzdrPVJ75/aPVju/+Jv/sx7vf/3yZs8fLl12fHPtvfbRo0JaCj50P/X9dxtG1nyZ53/hF5OXJ686/sYr2Vtr5poVffDBmYyvVtzzrx/j/dWwHQPrXOqmPP+M'
        b'0ZK1D83ffd+r3muAajNHaGvDq3hTj9sEC+GaRrHl5CarVExfcjZe2RVMApkDmFJrHs1UvmGQjQd0Op8BdOo4NaFtMldsy+dBlT85AjVKoTeS09vcRbphZgQrYSjUEIWw'
        b'K5Nvt6BRX7EEWllFR6yglJ966isUO3QLB1mDN1hRmyab0/s0rJVE4mnQMlcOhiZemUKi4u6jSIY6FEMlNjkyxDimANcTqW6PukvcFcJEwRRvSee7QzXTpjfjqbFqJ/J2'
        b'x5QglZEKW7b6kXOYRuJggVSYguflocuwnuv71njGX2uqkK+TjIM9dngcj6UyDPHWnUP9A+zIEbRGdNk8HWsdmHnEA/bNJcPhTGRrWr19EiJj7p2AZdDAESD3BmG1DvVt'
        b'Ol6mwG/bMBvrWPMsMGuKEvMdsRmL/aWU0Hm/IV6RBE8jYjOV781NPHWXsSUAro8irYN8IhxgHXI7w0I4asigcCjQLNZvFaFh2Qz+7jbMHM0fd/QVBTgG1QpjyTI8O4iF'
        b'JXks366288XSZMaSuo9moQYZChZwSZoKB/Esm0mLUvCiv4Yl0wBvSKDCVQr1O/nQVE6fjy3+eDlYCQ22cqw3EoywXQJ1cVIetVQMF13VFJ/SiIyNAbbBRcEYS2l8XAGW'
        b'cMDGq3jIiNaQjMsl0kS4hkekpIHXpQMxGw6xyCbbkQldJpilk0TSdyewkRsVKrDNhw6mvZPK2NYueDa1cVgOkWKm3TA2oLuxKEnp5I9tKiwSKfJ/psJMsspjJ8fXObzF'
        b'bnOsmiZ6UDHhLJbDZZboiZ3DSIe0kEbTfidl4+EgLDQQBlhL4bAHmXi06v6D8JS/lvkzdDsHEB4OWTI4QxSPAp4qezZujNrJF5pMyD1wap0gmMml87wsWfctH4h7lX6O'
        b'AVvgoo/T6mlYoFaJwtAw2SIrezauO/Aw1EHRJvpnIhhSKvRqGRtXhyVw1F8LYS2BfAOy/Cqks/E6Bx0NXzqtC55xIZ4y4PCMm7GdG1NKHZapfe1URHKi/Yf7RCiBA0ns'
        b'nUvNQrFjA+nRIgNBVApwHXLIKmLBVycg37IrMXqblJvyVqxhDQ2HCivORU1BGyEfGylw495EPkqdfjI93Eay4Cu4iaoCb7GyQybjBaUtWaFbAlSSwX5kklRLoBNLTbgB'
        b'qxxz8QJtUSClEQo1ciVLDG64sU4MJAv5gtJJZUdGitQZjmCRIk4SR3SWFtYX/mSh3LQng+PkS9HQMyxJZ0CJdL1gyAeoeJkBefOWICrA1Yt4Hsvw+AJo5FtLG1YNV6ro'
        b'VKBlG+AhEbLINGklIl4d68rdpG4numxrw7aLcG05VrBrYYFYTiY/tcdJyUg0w2URTg+NZ9c2YslSf26yl4+GckHpJ8H6FG9ujb2IpXCKDlBKQJATXMEssuKdpQphOc9b'
        b'ro56Cq7jZbIZ0GlxVYDGOQGs0FF4w5u0OoUGx0ng5lIoEofjQQeOFTtzpr6lNRcaqKV1P55keemObtipE+s9dtnEwxW+fxwYENQVvzoWz3PD8FKy8dCFmeom4dV0FrFg'
        b'pGA8XwINwyalUrwwbIKrq6izopivTtIBlZDH6mxFdl086BrBFtH4edPUWKoyhkYH0tsl0JkSiJfJTUMtZHbYNJ61y08kO2oL3dzpFYOl4vqtWBg6j/XGhhmYxY2skrVE'
        b'Mzd0hkyiItOnFkChF3XipGMLGZoBIhxXrsWcXewpS6gfpmZU7yIcI+thMe4bz9motwXBaSLSY4EtWR14bBcUkzvwzBjWiZs2YBapra1fhp1EwLpJhlAuccerwI3RW6F0'
        b'OI10DaZGlgIyIwY7ke6SSKPx6kJWdpgvWQBaqPHtcFKgUOOQHcf2yjCiVWSr6fnkRzbTGZPYbigVhsB5meuwHXxiXIrEEr6bM33jiIglu/D4dijhuLZlZMe8qtkMaVfN'
        b'wytkJbWSqTAVa9mGFwil4fS4pfGRS8XlCx2xPo1veLnToUNNRtkICzLIj2XL2TsGYrkUjkOuCw/N3ANHwv01qOWUPJrMZzytMdAewXo8pWefTXCzgczd7Nz0ToILyjRT'
        b'I9KjY+RrRI8FTjxe8+CcDDUW02BVKxFLF40bBmVs2TlBg7YdvlvIDQs30gO9QTqBLL493O7fJhmgB+qOh1dRXHeoxNNwhJmlodSJrFKKFuaMhYEOKt/AicPJRs08AQbC'
        b'jNlyODV1ANs/oB4bBK1VOthRwH3cKg0HRjK8XTwRBVcZDLIWUt0rsi9Q9XBsVDinLWPVS8dDYUp2k+MWX7uEDSrK6H5FCqflWK6xuqfFdlFY22MtHuQU1mS1d7Kptnso'
        b'lpDZwNYW0UzJQHpL4NwishezkciFG1H0Mt3Cq+xgr0ikIiIvsWs5U3z5k0FO6gTSc1OlRlgiMrFsS/pcyPLoCyNXA5p/BKr4yd0YiHXaJgSpBmMea0ObFGpnkC2GTplx'
        b'dljVhUefCB0Ukl4HR5/nwBaa55aVSnKPQNZSO96YK8LZ4ZjLJ3MW1oYqsVAn+FRBkUKQLNkcyvflTKiEI2Rf9xPJs1dG4CmyDv3gIts0yKLBZtpGY79AbEmGW6wEK8iR'
        b'EiFxnwvb0qLgliUcmKZUCYI4jMzvAXiQCxz1ZIc4oQ7CZmciMKhWkSlDNmiLTVIoxJPQzCdzJl6MxxYHJye6CRy2WEfOMmw3Y+Vi4S5sVNI1IFGJqzBn1FPhrDtWjlqo'
        b'Jhs6FhjRNnViuaZdQ3C/bKYBGXfaHaZk5JSOrFHyUZIMODMQLu1g421CThZGdRPkaEcEtb2JCrpwq1YM5Fex2U/tbIeXfMgwwB48bAjXJT4z4Tyr7hR1MrY4BnErxE5x'
        b'0TysJKvnJG/uFSIo3+hCO7YaxFY/AzueCcfYEogywCa1k1+aiix+AzgIZwVjCZHzyPldzqazxWjSFi4w+5rbQkP6IBph0iF1h04ZX0MVDnhLPzAb90CruJD0wkG+0vdh'
        b'NWT6OwWSXXqbuCpx9gQyh5gRpwBOrCfHJ4/XJlJonSscHMEmQCLUwh4ddMny5QoGXOKQpBrw34G3lT/mOsen4Gm08hRm2Gd+n6XU+tW332e3YKdgCMMcsdhYtGQ4HBSN'
        b'w4rhBcopdjGLEldoUIvpZ2ty1UoyjPKXP5RIrcVhDyWKYaLNtxJzC9HioUxi/ItERlGOzcTxkvHiMPJpxAPJLxJTikhsQp6w/Ekip5/HS+QPbUWznyXkeQtxlGjxi+Ql'
        b'+SxjhoPMEI0prrFoIQ75WSIfQX7St8nEEeT7kPsSI0vyLvo7+avpEFIXikBi+5CUZfCId5OrI8i9tFyOkKwgZViR+ihIiWbfy5WKe5Lfmfhr0Uo4K7sN+T6Rvlkc8ouE'
        b'1vZnyY9yK4W4fWgf7hze83ocrY8bOL305OfIUI2ghkSqFPbjUMoUPrXWdyn1XwfyYpYS3y7S7OOgIJWMfGMB5g0mPeBLUjYJLPk61NPHO9A7lAGWsGRpjl+ySQc6QmuY'
        b'Qh1R3B1n9X8CKzJL10FldC4baJyZColMrgG2/klm+B/89LJ8ukQ0M1doAUrIlBa4Cfmh1Rwt4MgQdtWYfJZJtVdH7RaM0xg1QQs0peiM9wUORAjSGe8lwuyVcrKTFD7V'
        b'K8veWPNTbfxo6BFptELz2UjvszH5rIw2YZ9NyWczzd/N9T5rYEiOGukgRqyiB+lBjEj1IEasSwyjJ+ogRoZHj9BBjFBYEiF6dLTNr4AYGVMij56kAxgxjTWIHhs9rk9o'
        b'EQpmog8tslFle8ec4fEwAmuvmPVxqQ+ce+GK6F39N0BFZvDU9ckqyR2ZZ3CI9x3pgskLUg7RaV9Nvx0VnxzdYwbPvZz8qyBBNA/N+PWwH9rXsVRPVwr7kVLHs3MoQEfK'
        b'GQY5FOIdGBzmzeA+xveA2gj18gqJ2dI9wdwl5Sxt8JPc6qrDxNBW5MGQ/krVAWV0r7PKqFsZdBxS3tJH29B2TsofaYveppf6e4dryhV6z/8hRkZvylqDIAYdGGFE4b3M'
        b'NUB+kiV2azKYr8o/GW8q07eIizGfg5QdXbYx7p9LAw3UNJxty0tn/hbx/CL1ep/Il2Pt/uwfaRz7ufBN1tAZboJ7guzK/hUqkckhMryKpV3mJxGKFUTNOjG0HwrPVm08'
        b'CEvI6k8uoF829IzcPqTH2npClA1LQy0ccX/HGP36uhvaRv+vaqOj+AqF0qBKwn8dSmODSvbxGPmTQmlEsxpTrAAa0/+fxNHQLoLH4GhoF9Fj75jxxDga3ddlfzga/S3v'
        b'RwBb9LlU+77/V+BY9Mze4okGkYk0R4AmYfWTUqR7rC+U1F7YF93GWYN3QY8IjmFBjgm7/rN/Hgc0oa3Jr4GaiIv9H8rE/zsoE9oV1wfIAv3vSbAeui/aJ8R66HMB/w/p'
        b'4TcgPdD/eifkGASFsZB9bBEm9oYZgDLMp0ADWIYlARqqXT0ay1uYp8Q6e8yKs7ZUiGrK2ev2yVD7yM8jPv9oY+zKp9+5/ebtP91++/Z7t1+//cHta/trDozJbc4ed8xp'
        b'SkO2qqjjnRM5E3IbDjcXuOaOObTHTSrs6TSdandEZcCsMhYDsFMvZBYPjHeBU8BdR9iCDSv0EAHWbu4CBPCHM9xG2IGX4GJX1v35pboo4URHZlbZMR8uaI0ncHCH6Doc'
        b'm7glOM/LXxP1vABKuwKfZQq8jNXaUM9/J+xVlwzv8DgxZ6F+Ury8Lynk12e8D3ki6efLUY+Wfn5t2ntKh6iVw/pIeV9gKGhS3nu9SZfvPrafc65Xjrv80SG4UYY91oRS'
        b'uy5oZFueYQ8JTUlltFilRkIzZBKagkhohjoJTcEkNMNdCj0JbWdfEtqjM9f1dcT/J9LWuwN4acQeTS53AjkoaFLt/zLZ/5fJbvO/TPb/ZbI/PpPdoV/hKJ6cAPrUZb8q'
        b'sf0RW8b/ZWL7fzUdW9qn9GcZxOPYq6EFTuEpLNTPyF5gyIG8qLU9Fq6N5fEPoT5YYIWdwVooLh8/LGHMYcsoCJaCRclDGRQZwTXIwgqO9VUAR12ovTk8TJtorQf1VY6X'
        b'eJz91VBsYPndIpaKTgJeHATZadQJgFd2Q6vOX90diIuhcFH3IkPiktBgl+NGeB2uYn4azYWZgYVwswvEC/N9HHj6BubrCFbXbcXiSQoPKXawR4jc2LTIn5vGSdUvDtTI'
        b'vzQx1gFLA3kwV4jSEEugMIAljFhj7jAdY2v44mWOS5fRzF6/wABoCPOBiz6BTo6+gaQEZwkchZNwWTkZikJChVFw1CzeBC8zQ9xAczygoc3YPkWAdiXsSZsssDzAy3iu'
        b'R/E0UTV5cgqeltIEVZYwLhMioMgQKp0HpVGJSo3X3EO1t7Ik1kNwhQxYGHksRK/1q2INoc5zERuDHc64R5liRvpROkCEs5A7B89s4aHfJxYTiboF2zPUNJPklrgJKu3n'
        b'BrPo+bkDZYLCpFAqzI9w+DFoohDnOvtHmfoP5MpfGt8L39dsCi4W3r9P/+qZPfMXvWD18oEJyr0Gto0p463cVTV7F69eOdHn++fHNwyY4JZsfcDilff/dePhregXbcd8'
        b'Tk6giMpZb3u+t77CdnHQZWnI6eoT7q1G59a+J5so2v3F32/EicYK58OHfHzc3y+wqVaue32rEQwd/edPXn1zaHreNPzqpYUv3TDftSr9E8PlA4fnvPhggt08dWKR+2ex'
        b'3yfsuvk3129iV3TcU37793XBHx9f/qbze2llqT8/+/OJd0cavfiU+13ff+52HOrna+het+HSv8yzXvUrCT6tsuAO21t4ZbA++bM5VFgslcavhgZO8DsUmvWQxiZ7aDI+'
        b'J0Iud4LnjhukIbFYCc2iB56LZp5iW+wM07FZD4JabTom7kceo7IcSrFC6Y03e+ZkyhSLoJXHmTXtTtPNlcWWBgLjDlbjLR6yVx09TavzRKwUXSEHmlk8wU44iud160S+'
        b'RJNpaobXWTwSHIFWuNoVObswLK1b3OwY5DmrW6ck8wbQ5VpAXmOGNZCJndKA7XiEh9bCMbJGi7TcxWOgHc5D+QLmz/aMhzb/yX50B2iC80QnJVvFkYHssRQPEz0r8iQ4'
        b'idlYic3spXI4EGfvF+gEF7GejQkR/AdOkuIRuAk32dNyzPaCfWndUjAPkqZNoh2WDeWQw5IwyVdln4mYzlPCelPLKf+D6Y+LH6cHJrMkSKmCUe0q5HLqHBatNFS91A1N'
        b'v8wkZhKFLqFx++iemlTfWYtGT5K12JWwaNC/k9+wf47bPpITvZ9IDb1ho6+GPq5J/6X8xFiV7MGax+Yn9qW//abkROqx6J2cOI4nJ2JdMF7QpSdensOOxCfOTlSMZqmF'
        b'oydhu306lOmyE+GSsN5zjlQpjMULUszxnsBTpo6HYoUmOXEbtjJUgymhPEvoMuSN1eQdRmDNKAH229ux4yBrFk8sFMw3miRtGi1wzqvrUIM33KwdddmFdBdtw0pOX3Vu'
        b'/mAsJxtBGU8shDPL2EvWDvJXb6FhmqW0+kehAK9CNauZGjLt7SE7VpNYKOIevAwnecphtge26/IK3fGQtcQE8tL5tQ6akd6VVXjRFvbBjSG8sVWrjUMTl+oyCwW8gAUi'
        b'l02K4QI1dnVmaNIARbu55mks0uu8fUwoqfp1vVQ/TaIfHHFh/bFhEk/0y5y6M+jNoeN4hlu8/ViW6HfCJV4yIsqN/zHbwJcl+p0I3uU3KzLs30v0e8LUsGuG+qlhi8iH'
        b'xPWzNYwkDmRT3eIbiIUOZE5dwgOaeCIsgxaKb0ID+lTQJp1MhBl/KMMWtZL0mifmm4dhgS9r0S+eJiy771LiroBin1W8mZ0zBrPsPht1xuz3o304Pgbmw+k0/fw+ntwH'
        b'mdPV0mCsggJNMqYpXFAa4BltGp84y9SQFeqymKfwPT0o0eS1pVJBJbJBnQENBprQXGjHq0rRBlqx4t/q2Jwn61ipQr9jB7FzqgVylG7m2rQ7cQYWO7HkuTDDWG22XSg0'
        b'wWF3P46w2zwba7QJd7NWYTlNdc0kBxlbM2WbSVfQ+HOBJdxBTTB7yHA4nFfa2kGbKU+6oyl3pJSaNJZykIf1NPZZl3R3jUiO2SJWbU6M2xf/gkxdRWqRuuZfaWH+6kHe'
        b'VnfvfnH4x+qcr32eN7WYP78ib6HXqawXx9meWGhRuezPLQZHP6p56ZmUt1o+zipdumKq/2Crqd8uclhW4T+4Srn0wpofpLZF38yq/3FlQVWR+rMdn836LP343HUZJ4s2'
        b'2hx87qblQrNPHFd4FVyoWNL6cu6/pD+8/uI9i788vTEiBmbb1nokNCoNFpp/kgEvfrXw4y8XvHG2zqhTMvSk6bdnpy/Jt8uaummJuvid2Xan3Jd8+btF23DauVjHb86Y'
        b'xquXno37RExWXo1pTRA3Dw9PeDMjojlh/LjWnOmbqn9akx3+3OUPA84/7Iz74ztJDq/Ps1i3eWab+5gdnzh7vX34nTZbye458dL49z76cMaCzhHP7U64t9XSPm1NmuqN'
        b'0IgzP9ifC5yrLpy82fTK0I5V5+LcvtzcDm1jop76xsvxfufpMFXM3Sv3kjLc24rmLJnzxf4Bsa+MfKtuZOirvx/x/ivHzh5LUbhH2aeMytxWfXhOxNsz5c03EgNfhLvh'
        b'5/4/3r4DLqpj+//eu8uysICAgKggKIosS1Gwg4oFBZYigqgo0kGUviB2QUDpCKKAVEU6IkVBipjMpJhq8vSZhHTTq8lLMTHF/5S7C2jMS957/1/8BJh75049M3POnPM9'
        b'Z8Rwc+PW6Nvvxjv0JujcbIWBM9NWfjn19d4XX9yg/lavh/S+yTl13YYXPwlVv2CzqY+5q/b6zM3hiyqS+vdo9z2wWB9dcm/5nlaH/BenBL343bn9MTkHGlzsb854UVjX'
        b'7PQkjLI4UvzT21cdXrwzuLnygPaeWy9dDBhZdAyM9rGRrU8f2Nf8St9Jk+lujgPnnzf3yzLyn/GJxVVfi39VzGtPeqpva/izoXNDFCHe/7K+CA80aN1X33dE8zf1z7j2'
        b'jBFv93bDjLYPDdq850b/dC/9s99dPrln+aXt62/mvDz37uzonx/c2Pf915q/Vc+d89qVI++9A5etnPnjipi8eT45u6JeCPl5c+0p7+YnDz/xXVLBy2HVh7p+bW4cMbsp'
        b'NMnU+PR3A6+QnAfR3JRf9393PvT3r59Ydm2v9hffhxd9Nat4wZevWKO/F61PO7l+2p6dp46l7i9e8OKL1xZ8efv7abc/O3T7G4OYispT00aW3Jrn6Nip/qP92dLBa7/6'
        b'LC53TmvU8hv8bgFMAiN3XaeXh97OvDfzSwvjH+5pXDOsurLomTevTP3EuOm7nMO7+n765dvKwq0zLUI6BdPlo/6Rrz+Y9qnii7LR1sasZQkrhn/Wfudyu6UwTXuP6f2f'
        b'j6adMHjyiRr2amjGke5Pf/jHO8H3b/zikNlbdb5XMNhtcMp3/zM1Gu//c2pQaFPS9HMdcX2nfVcuevPYd8f7GmLnRh/RiLrxTaevc830Z973fY39YdGGg/fmqUk1h78U'
        b'fB8F2zbnf3cu9asEk12fvVB/V5pAkQGnYMWmcRA2FRt+Popw4rHwLJEDXNEe2YNBbEvDxjlmmQXSiSCxC1zVe9hviRAcB1k74BBsoKiTrHnwihyU6I4B2SiKLRK2UzVJ'
        b'pjtIH4c+45FnoMhbG17xpsJIsyY4OYY9m4FqKOJs4blIqqK5tOOgArQZjg99RZBnIA/kp0hxjt4wUMljz6Qe6CzCMJUCtGVVLiPgMyeQhTZVWLyPcPl74RXYOAY/g+fj'
        b'gznrA1OovfTVUHBpDGZmhI6bYm4O2gyp+ANaTfbLbazANdBPgWYUZZYNOsnrBfHLMXAAnfJDvF0yAZkdAFl0JPrdDSXo7C8fhzRTwsyCdpG2zTJD7/NBwyEeZ8aCVlAC'
        b'8oiNjBO4shsXn4TGngDNMMhsKm+sjZqUr4KZgdP2GGmmRJnpgVzqYyYdNESqUGagLAle5RATBwapffKmSBXKDF5xshLxKDM7kMODwNCRU8bjzFYnw0I1JcrsSiLJ4ARq'
        b'UPcHE8ZgZjzEzAhJfbhzSOAzltjJd8GLPFAMg8SmmlGJs2kNPK7CiDW4gRb7ZcTiexUc2DOGEfMFQ7gBPEYMSXI9lIDyQAM8I5ssHpP9kOBXDOppv8vN4HmJt62WFHc7'
        b'HZaDBhZ2+kMaph00IRmyCHWjKm4cqoRiSkCRMzXUb1qwXwVC4yFo8aCIoNC0Y6kw7wY7FIgi+5Q4NApCQ2d5XwpmXDaB9pUEhoZ5cJgrpTi0GRHwklAIumFnNCnFfxs4'
        b'Kwd1oFEJO1NizvqMKQF2yufKIjeqYGc85gxWRxPLd48QOKwIQUuLxyywoCjaJIX6G+gHLSrAmcwC0Wg2qKP4wtI58KJSpgfpjNJ9FMy2p+bjBZPnY99m6krcGQvOrVtP'
        b'muNgEqVEnKFx61Y6RQKtLHm9fy2s4wFnoNIUNYkizsLAMdJaa5vNMjtpKKwniDOCN0tjKLpiZOM6iZ10ASjjAWcYbLYwhRRqDPNcZdvsVFgzHmkGCuZSVMGVvWFKqBk8'
        b'Nx2jzeoQY0hJeBDUwcZxUDPQI4YVLLy8CDSRjwNWwR65h5MKacaiL/r45SdgwXEF6JiuwpqxoAGtzmJKgCPg8joKNdOAuXYiCjWLBccp8E4ftCt8YA+PF+HRIm0wn7Z4'
        b'AEP6VDizkUTQiUQKiv1ydRbDXlC7TQU3Y6fD81tolcfBBR+YPwvUqABnBGy2loIBTsGOhTxHC+uXIIZWJ5aMQQgSsBrk8MTW8fdSAYJYtPnWURzgGcQ9nqLYlrUCe5Zi'
        b'Yib502PlzCF2It5MhTUrQonyDWgnxAvGa/+88YAzHm02005XaK0F2yjqrTx5AuBMNjkAYxP64QDdEHoNl/CQMzPYs4O11wMNpH3BiI47xyBnsMZFj92xA5wmJGUY7cIj'
        b'zraCExh0VgyH9lKoyzERHIG9YetUqDMMOTunSYZ5PSwxx5CzhdEEdEYQZzaO1IggJ20bAcFgJy45XvAyaqvx2mjYJZTBEnCU1JoqT8GsdL9gjJWeYkWu8EBNiiN/kWYD'
        b'usLY+St4rGah/XaJssSVaIgQNWqCUg50JJuTIj0dvVGRhNREASDfiJsFeyfTW8WzMGMLDwmCXaAF7UUY4QbrYCfZMK3CYbGCnoIaaCen+7Ap6AZ1TkJQEh7Gb4nbDo5h'
        b'3HxgOoa51dmAXnriNuzA3D8PcQPHolEmCnGDF+MpPLJ/TZwS4gZyDQNYW9Czl2Lc2sEVt3EYNxXCzQlJZ3UbTcjkxh5G+0YVyOJRbmglaXqRcZkF69Yhgs+cq4Kl8aC0'
        b'1WgpYaoxUWBrjAJYON2Lnt88JK0whIDQrRfMn4BHG4dGA1nwNEakwcoUCjvtgPWT6EChiSzFg0Vw4oIUU8RW4C0bnD+AIeyIr9GAeVJ3/kifCtqFIEO4Hl4V0O2zAp60'
        b'I9lgtr6UdFcdVnOrQL2CvwUORhtF/u4VPmM2MRiEZgK7KMqudj8qgr+KDQRn3Pm7WHgGNNPNcAhcdIL56HRS3oaC9pmghdJRPhg0VaBafSTe7r6wWIY2Wd19goNo+Z+i'
        b'pefCE7BOhkhwBjpliuX41gFWcgeQqNdHVqoDOIqWTIEXxorLYK2A9JJl9AwFh+AZ0xSsWVgDjoHMCeC8R6BtsBqcVsLzwKAVGeBkeMxBCW5LcCBHEsW2oaOog/TM2XQJ'
        b'RbaKUZksRbaCow6EQg/AelipQNSUocRQY/z0RdhKV3Pb4mkKOazk4bsUujsfFKXgW6sjcGimbM7Bx+LvZDJK5VWg1l3ZQNDuTeqhCMKVGoQAYDVsQeygCn6nxN45oGE/'
        b'qaaxzJxsHgthV5oEXrNVIvBY0IK2SEKtCaB0IUbfgVJQypMPRt/B7MXky2TU3TrJXKkSf0dgsr102xmYAfpU4DsV8g607UUs6fnwFOyYLHoprOKRdxELYTa3i3KZhYmw'
        b'mUfeiWA33UMo8q4FHWV49YYs84O9ZgeUyDuMu6sU02PjdPQWCruDR7Wk7AzU7CKy8U9CXNPQOOgdD7tDzGkmht4hriqTEmtXHCxSgu/gMDw2g5u8kgeJL8O+aDH6zg0M'
        b'EwAeRd/B9En0QBsAWe4Ke+u94DKF4BH43Qqlg4eLoAc0jSHwcGCcQyw8tXYdHa+eTaitKgCeCn6XbK2PnR/QInK2wHwKwbMDx2CuGkXgRcBqslTUQbUl7BXJxiB4PAAP'
        b'nhCRBq6cJ0Wr4DSoH4PgsesQ5TfQGNj1Dti9J0bfuYLufawzyIZX6A5QCE9J8KWYIejiQ4RjlB1aVdVSnf97YB3BP1F1wp+h6ui/qUpsna7g8ag6sQpVp0/+CVkdVhel'
        b'zX/lRLrs30TRqYt5VJuQINfED1D+B+Tf66JFj+DqfueEFENnQL7QwcoOgsUzZo1YISrVjtXB34v+SzzdLS3niXg648fh6Ywe1j38t2C6HHWlBeCfKUDSmfsTIHWPaQaq'
        b'G0MQkt9U4ukEGE93neXvJaWT/+9wcM+jSt/HQMGDzP8IB/e6SMaxOmp/iHmb+xDmTfnugfEqcrFsAUbilffZmgaqG22WQdK+WtwMUPiImawO/1tx9BGgW6CwTL1Mo2xy'
        b'FId/lunwfxvwvzXp7xhBlCBCUMhFWKs0TjgojtZx7eM6x3VJ7GotDJgjADO1SFGEKEI9i8Exuwu5QHWU1iRpCUmLUVqLpLVJWgOldUh6EklrorQuSeuRtASl9Ul6Mklr'
        b'obQBSRuStDZKG5H0FJLWQWljkp5K0pNQehpJTydpXZQ2IWlTktZD6RkkbUbS+ihtTtIzSXoySs8iaQuSNjiuFsXysDlD8jeOAS4ONCImlgKijRMfl6CxmYTGRo+MjVWE'
        b'FOWYEsERgJ1sVGvNKi9/ZcD79/u4h0wrsW3T+BwUYaeyzElJwFEhFDTPQgcb+tuRxFDAfy2YUJhSc6ewM181zmiQt4Ej0AHe0g69TYlMJiEeEvbgKLUpE43+xod7sDGP'
        b'DA3faZ4cmZgcqYiMH1fEOKtEbM46oYTHmf1M1B9OSHgnYGsv9yhzEp5VYZ4WmRxprkgNi4sh9ksx8eMQGcSgCr0ORf+n7EyOnFh5XGTKzoQIYqSO2pwQuyeSaDpT8W4T'
        b'uw8bZk2IZ2HuGkNsnKxWSXkj3diJll/YQIq3HaQTYc/Pg3LEbcytVkuV2ULNFZHYhi0l8s8mCc+h1RophnGEjrMT5C30EpJjomPiQ2MxnoBHH6MhwFiJhzqqUIRGEyRJ'
        b'JI3bgXLR3ptHRCai7VVhnkAbToz9rPh3qzGFxSUoJtp8hSfExWFjZEJ7DxkWeku5UcHeuNhRUXhoXMrCBeGCcduOGr/1ED2UB/rB48PUjyujaknIFsKiTYSL0uHV14Ic'
        b'USZzSLhf86BApb4WEvW14LBwTH39/n32LyDGJiyix5uWPc7aEPWMGhpu8fLkLeVIABVS7ticodkh1qRoSf6xCapVJCWlx63XP0EykWFdhgEp4aFoxYegJoVQiz9amKqQ'
        b'8WT3mLA2oRERMdQ+lK93AtlhAk1KjeSXriIVrSnV1vHHCI4JVrQ0Wg1eeaGpKQlxoSkx4YRQ4yKTo8fFonkMFiQZrcjEhPgIPMJ0Pf95bJkJZ5w2T2wTzQtMvRVYeJIl'
        b'fdf76j2ZtC1F+py0L1+anXC7J0PBxBwSN354mVjop8rQD6f1RAtcAvuxT6oUJD1IQR/Il+rBLsRI9wD6CWiEJUSxyfhTneUV7BGnHaQfQPUfZg5bwnyivH1mJUd9EQcd'
        b'0PJcb8a7KD2O5IVrqJJyOIB2fCfGCQkSg7E/PXjwYLmaGo4wY34iItzzlEUMQxSfBwzgJeJoGZY5zuMYtaVyF3aDORiScgT1DoeQ1NevgHk6MDeNqhSQgAmrNTSsrVjG'
        b'AZaJZHNhJdUyH18MqiX4MRiEI5wXu3g7yEbFmONW9cyxGl+Iph0JGDlrmRoDC2YZyomZgSgK1kroC8EeBziIb/u74CAqAnOAM0AnyObLkME+2hZ36yRvJO7L3OV2WLMR'
        b'ACvEJkgwbyBdE82Bx2EvfgcuwRb8XryQi3dYLhUQX8O7YMUKOfYGhoR4W1jiOG8hx2gd4nbDDHieeFp1XA3a5PASGFBlEDFah7lYrZnk9VSQkyTHrgOVb1lG6wgXB1oi'
        b'U7F9Dmhav4TGBnHzd4MZfjibr9t4rc3aSepTQDcoJyYR2319FTJ4jIiUvrawjwiUk0ERdoVUaZnqxuCr3grsllpVgi88D08qI6vAXE+53JZLWg5qTOBVkGcIe2CP3ADk'
        b'ySWasAfke2z0YyKjdBeDDqr5N7IWEmJ4b1qSZ+MRbSY1ED2clwaujK9gLFpOob3HJiuY6wYL/LDlpHwTothKDxUVE/MZH3c1/TmaMBs0qqnBAdc5oFXKuKYZwBrQE47G'
        b'nBikwVKUs3dSYjLLcIGwEF5hLdeBPgKd3ucH+yTi5D1o9kH/FiFrPReeo1aUl/12wF6tJPwNPAdaYAc7G9YGkY/sZoQrEsm9rgC2RmqxITBTg3oUhh3whCIJ9mjhO7lm'
        b'E5jOzpbP510U+xluVMA+WuAIaAPDrJF0PaGZaCSyK+tCSzOX1JUFL6SSO7JccBGelYMu5qE5h/mgmMSdhafWwXq5dwrMHAsM42Xr4bPJTfUFP6ggHVvq1cVKQAs4405s'
        b'T9GQ9sBKZUwZ2G+q+nqDbQD9ioGlTAS8ImYUMDeGPTzMKY6iRR6dzMSddEqYvEr32bR7tz9xevfn0iW5k6t038mKTty7RGORjusIG7fhTInFbas8s3MuQ9qvxc42CHJ1'
        b'ff8LPTPG13eD78aZHh5t4saoPYeSQMM3+z9e+eCNn7/afyEo6Jb3i/s3BRnr1z+RMj/1x/yhkpdM32vY3qAzUCGdlavT1zr7qLZpop/mz5pPXofXfz57sWLaaxnvwe37'
        b'TYZclu2427jpuw1uMTut7YS6q/XO9RedK9W5WhZb2ly1zXP+R27q1wae1z7oPnv9oODNoBM2jb9NKq2sKd6d9/r1roGylGtpk0Ss51PfnwrV2rTjY1ffta/PnxkErS3j'
        b'Fp2KnKM3J+ViWeTNvkUNh748Y+jrOV8W7hwddKFEYhnZ6flK3PB3W6PV7l0InFK98eWIm0bPjG7ttnp567tfrLz03e200I4gg/KO5H0d27t/3nT9g8HZQcMXPnn+ZG1l'
        b'w8HPom9eCy3zMpSYzj17tS5z97zIu3Dya927fQ1Tdhg9VVixuhW+mpRTFPOB2857G9Src+ak1Ds1tWeVfDXn1kqPKZ+881TV1G/f0u93jdghbHsh4IcL+6M7bjt8ovny'
        b'wbPc1JyhO7VXin+oLKrq2rFt8q0ZOdc75m2b2dde9Ib1/udNj9XeO92k8/vg+y0fVJ6efPtB3ndct+Xtb5+KvZtf+Jr3Tiv3LffUD4+G7Ag89M2GA1Pf9fAMvz/pRvVH'
        b'S+/b+3xgUHxz99badc/cdKkNvPP9+wbFvf0/TPHR3lf9NbOvyMbng8qtVWfmDkf/blZ8TK3CR/r171GvHM372fRS+8Az8bfeiVnxlttzK9613fbPm6FVlR4PTn7slFK3'
        b'u+iTmLYNflOf8c92cH6j+4EkrePM1HVxvQ7dd83XNuY+/0HTzF+0PtT4Nu2wYOFBvVVO70tXkfuy7WizOimz8+IYt9UcaGHlMDOI3EGibTYX5oB8tH5ysOm7D8zjGAkY'
        b'BlV2HOwAPbCA3ABqwwLQL3P3VGdAIejmQA67HPYbkZs0R2cTmR3oAgPjXLLaOnuS688gWBYC8rGNbA/VeIpCuFlR8DRV4BSAQWfs/BOcW27vgw1ZD3PW6+EAcbQGGkGl'
        b'E/oUa1FBS4KnHcj1IRphkGPvZmNNYJ3qTDA6ky+gbewEub9aCK6CevlSz4c1/HBISBWEpWAwFebbrDB2h4W2Ika0g7OIXkg+nQ9b0QbrY+tug69/JehYumyMnaoW8IbA'
        b'DvYOMpgJOh+2MdgB68FpkmPe4QgJOB/8qCUzGAGDVCc6CNsOU79dGoi14O8NUaPqyDiGw2ov2Gu7jVW57kJ1gwZ65XgVH5Myd3ABHeJCxHGURLPwGLjoRu//TyLOog9f'
        b'fI+7VgQZiSwzDVYLk6ykVBVywTwe9sIK0K3yFLkymtDAdnBCCw21h5fcFmvavPlrydnwlJoeaHaCl1Lo1eVVX9ikgIXudlIdPZgn1/G2hZfkHDNjnRA0yvTJKMxA49gP'
        b'e5NApzss1uAzaLtycAAOG5DKdiG2pQvV5m1rs87Ta1x15vOFsBExSHQu4ZXlsEXlhozR5MAwvoQtc1dG2zm6ETsdBnlgyMfOw8vG3YtldHYKlsBiV9IQfZAOahWHUcn4'
        b'3OavgbUXCtQRnY4Q8tNYS2PqGAixhUO+OiPS4LTUwAgZrBjYrasgF/YCJ5C7mz0IqiH1BrdVgDgvpVtNRB/lWNe55CAhMIfQKSpvkR4M1dx1baH6jU6Y7010E60KqgdV'
        b'g2dYOIi6VUGmeANsgM0SOzm56q4FdbCNRWv2MqgnrvpAFaiMVYBMVOAfKjXLwYV40rywFDhMNYug1pqlmsVhNINEGVF7EI6gl6AuSuUHc0cEHxcI1urvxCoprMkUgOwp'
        b'sIoFRaAjhqrhSsBVTdy1YhlqXjisg70saIYdwfRGuQ42+cNeR9Ck8hMbYkYK3TsNR+gu5sAFqtZQg4McC0umUbebU0AJ1fzCo7CWk7Dmy2EjmbztAXqoKRsk41S/+qBT'
        b'gLp+CbaTHJpoh2ommAQcT63CFCvYwBkOsQVdaMTIxpYBckA3b1m0b8EE2yJsWDRpGV1Zg6kcYkV5XXkbqICXWYDmypiqraphqzns3QHKVQyViNGJELjC2pQUzPuaguOp'
        b'ID9tD7ykjdbgiaQxFg1DuO1hkZuXLfrEz1WsMzWZ6pIC1BQyTcQqg0vgtJRl1A9xC5byhidwYCPsVsiSpRrgUhIme/VIzmHpIqIu8V6PO6xngY0tQKEPieSnxhjCNqFe'
        b'NLhM9Qb14Ly5BBUt1diK+Bz8PWjjlhuDRvI6HHQ4gHx3WEuLQHSqzuh4C1xCk+gRwcJChQc2J7KYx8J+VhftXEq3fE1I7gFDoEHpPtERHKf2JrWgf6bCOxY1hjpQHNPh'
        b'NINC8jXaEAo8FB6gcsyvcjG4QGqcBqtMqMvPvaCLM2At1EE2mTtnnb1oblFb3NHSJPuDvRssFDAWsEkNje1iC2eqGKuzhpcRBZXAbClvSyVnGV1TgS8Yjidq7QQzmKMA'
        b'6cEql8numyjFZngkKejOIpgTDrLZ/eBoDKFYKz0wKNuz3MNWbmvtjfaUSdGCUNANzxNsBT7HYO+EpmFUTC62s5FuBJ071EAVPDorxYow1E0JPGU8RBU+i7R0EHvqBDpF'
        b'3laW9ChsBdUJSkCI53piFoT9HFNFWQ2omiEBrVHwmo2bkoj14KAAXFgAM+luWI4JV0YOHzAC+9HhJoZDHCgxcyVFJO1GXG3+AtSGh/VO+iDbWar93+t1/kf6oT9yKoDj'
        b'oP4b7c8RJlKT1eUwdETEmrBaWOPCkav230RqukTng+NfYb2IiBOTv3RQPh12BmvJWrH6nC6Or4X+mZC8ukRvImKNWCNUpj76rYP+iVFuTU7EGT38hMX/dIj+CX8r4mEs'
        b'Bux+w/E3UA/5NpCqUQDJHazT+GAiKEXrv5oLAS1urHTVeLpjI278/N+oaNKZAcvxSpo/7sdf8pUQ/W99JVwQM7yvhInVqBwlzFdeiJMbZRvzyGg7c2t8NWY3b6Gj0pPL'
        b'o34T/rorh6Q/a16Xsnn3p+N28Ler5jERE2r8S5XtRJW1sqPi4HB67f7YOntVdc4kQGeC7o0yJ59huP7frhl3U8qOagerLpWDYx5ffZ+qestV5qnxMUmpkX+A6v+7bYim'
        b'bdAKVl40/lkTBlRNsMYjoEhBQ0CuKlW3lP9pM8iMT/uzGR9W1W3nl4D9B8VHJRDPCOahYQmpKRPcEf2H9WPnMo+t/9pEihvnHuc/GvNktz+rDKgqmzZW2Wr3Nf9hXfI/'
        b'q+tpZV3JXszfWZ8Ff1bodVUHrPz/wKmR0lvHf7RYEblqEocDwRj+/9gmvDBxwojPALpo/9NFIqa1piQ8ts6XVXVO5f1L/Ic1Zim3hrDQWKwfCU5IjIx/bLWvqqpdgqvF'
        b'eemlfex4rd/DDkn+43HQUbUqPDZBEfnYZt2a2Cyc+b9q1n/rszL6j3xWsszDSgqBd8xvh66zCsyTpm8z+SLkepg46r0XGUacx04e7j/6DylL+LtgV3BeKe1gUScKHCPS'
        b'ji28/BjPk1ZK2xksPf5b7ukIE73f4KEzPjYyPjj48X4ncQWvifnR+bfsRDrTPsH75B9W9j+dgay/NgNCb/8YPcURVoEf5769Sx6qFfXeZidPdUZoxUrboseI7dEx7mbo'
        b'GCdns48wL8HBYQkJsX82gPjr0b8xgC1af8aR0domjCBuLa4TExBVwI656FS6haJKWPa4tkoBy+WoobEVoLHlVGMrIGPLHRY8jrox6A+HXHScMLZmvD+Oi+AcqMc3/rB5'
        b'Ob70xzf+zjCXqL5e0qKqr3l74vTbPEKoqiwCXIQFCp3kRTBfg6gWWDskQ1HnDNZ8/nXla5q2zWXo/fzFHfAMuRShOP3dvti7RYEc/emNHb5t3LDRNoBjdriog7OgSYdA'
        b'hl1iZsiRGAfb4TmYD4rGbr/UGOtwNdDuaUDUGLBZP0yR6J1qQzQZWmwI6A8hSiqQswLWEAtfd53xFr5gBBwjypFEPWKALjcEHfh2SWjLggvwxGHyLhK2wGGZ1Bpkxynx'
        b'vqANHCfQ4i22O2VU/MSxOLE8jmTQSHBxhT9FHheYueBuuiJZz9ZdyGioc6AINAOq6jMDZTBT7m4j2uCOyhWyoG4xrCNVYtPHXJmde2yyjRSJhxpLOdAIW40p+DlfsheH'
        b'jIJta5RoHsNgquEpTkyB+bY4XI03kRlFQZzhZp1UbGp52HeLHBa5LzTDXvY8YT4Za+pkQLZcDRbCC1seoUeJkh7XjtHjRGpkVa7J/golPuIbGJOPxiOUaOdNiG1KJCGe'
        b'xJnrQzyLV86lMWLV94IKhTfoACfGwCjwynLybifohVcV7qDVdMy2F3ZspWR9XDdA5pE4j04VP03esI+Cr4tBg7HCE5aBq+QScTd7cCvoonrgenAGVik87WE9vIioW8ya'
        b'JsMSOg95IB+2YTTBghgSwsZeBtLpPBTqM2iEQWbaOAyFzjry1R61MJgv3yYeQ73AK46kiUaGzkrYi4OVCvSS4URU2Kk0iJkTPOXHgJ79DDOTmQmarKVqhLxhGWpeqwo0'
        b'Uxmh/Hw/OEo1dTArDr12iBqDoMyZR5RxINsCnpGhBXjN6iHoywioof08aqJHAzilWfOAmgQLUm38kngZqtBOau1lJ7X18AJV21hmFshWW3pESMgfLZwsHwpgSd2kxK+A'
        b'IThIhmk6OAl6uGm8sTSiVjE3ZRJopQrzs7Ng7x8HO0HT1E4CnowcTMXxYmbPBQXENt8Te2SU4y0E5BHyt3QB/ZvVdoNroJTsPDhKeTnRYQz6Ps7mHNXgDTLU4QlnHzLm'
        b'qcGzFIk71byVO4q6McUyFwaFqLwCwe55qg2lOCqVXAHXhcFauYc/HCKQwUd3rLmgiAyRAWjCzi8LQCnIk49tPeedCfn5w7PJcltYlqyCNCCCLCajNw+Woj0BrfaSdSoD'
        b'flhjQce9F9bAQXBsOXo/thMEKgMOI3KPQjsI2oW7VYDAQ0uIkYQebNuGSNdwI8uwSxhYBC+lUSI4lwRPy7xmOuAQQcJQ7PKg1ppucb3wnBWiLTdbGy/YaYuxnqe5g2Fg'
        b'mMTNBR1GRg+Zus+FF/hIM9KNpASTIHCWz+MEr/LIE1AIaslIurjpyrEiabr7Y3Yu0OUn5UjHjsTqoyXZswdtsOeEDAtbcMSY5ihyNDjD4gMK2B29WYTVyww4YQUqUrG9'
        b'u44uqIUnRfvmM4wNYwPyl5OTy2SfJoM+26swDIntWhdFfQdsn00sRax6NENid5tOow9Ngsg25XLYJcTmiNdO+rDKjbgeWJIbGGJza58rfegfKGZ0GUa3Y3eI1h0/o0c9'
        b'LBAWEP+Pt4ODTJDOIfYgm6gVwQSgfTSJi1AKAJTD4eMms3seYrFHNZyjI+Mj9yYmr4jU4PdVIXYDsB3PfZEUne4P3XPCEurP1MYdBxAuhuUTXCzAkwLYC07qy0Gpo27Y'
        b'ItgKWvehI0fNFQ1u4x4GVPgaQmwnU5a6Ek/4VTaA6N2L4UlbuwUz3QkCxcN3g22AGzp/Hp5D0Mtpsgyi1jatELycyGk/F+1np9VAKzpZpbYwjyhiqNbHZJMQreGSSTEe'
        b'kzSEimdQn+8H6kb6DcS/6aJbE1RaavX5SOzz/7J99+WPqrPzDOz+oS5+yzjGaFEXp1Up2ijsPaWd6ar/qWD7hpV6H04vOOjSdmvV5wddoo5fCns2+/q9d4Yr36g5e+fO'
        b'ioK34buisMUZGsZ6U8qMn2+5eL7k+fkvu2fUllZk1mcn+Votzup97amI7/WCyp6vytC91BD0VeEt0znrV97Y++nT+2rMAq9lbjzq3m54vTK8+WJ+WdWvzWqjDfE/s299'
        b'kXzommSppPXkpVK7k19sfub5X2JMfmh+Ne+5UO/NW2113jP2rN0bZ6bzS1O62leFT7c0Hz2/IqM7x7rCZ1pAjXjVr5f0M1+SZCSf8bdo3jbq13jeqwUOqFubO8Mtre+5'
        b'ea8N3G0gfWLY+khfjexH57a80oQn51quT5bLbwRV1b75au/Nodu9sZ94/3hjW+CZt83NPt2Q9oPJ0w90ax1X3A+f+sMrzSb7nwWzvt/kmKWYOiXwx8O2L39ROcvoh+Ef'
        b'Cn90izu+6PbHr3PtCTlpW746EXgr/63UY9/qf7D1mRe+/N3FOSLt+uea7XU5aVu/6hl8fp+i4JeCAwWvGd9Q3Eu9+uTAawWLl/Y8UWI72eTNwPynuKsX0r63O5Q5x6aw'
        b'xi1wuXA0+rn4p+LLlk/aeS/Ir3ZdzJ7F33YrAmffWLPHv6noedNn479sLlGUpIp+c0s4Yx3wc/XLO9fe1383KYaRzhh61fBps5uv9Tq/OD98+b5zAZbgVtik3Z+svqDT'
        b'uuZ77d3ua9S2XpN1tK5Yes+yz+P469O6m/u3fn7i1xmvfzLK9OR9sabyfmn098UXo4dSbizb4nNvyVexh8pPvxH4oKzjwOhdhy9GFkdOn9nyxLIb3hv3TM4/dLm1z+7T'
        b'Bb/4F0a73lzy2VMDHw6MekeXvBxyR+y0Jmba66/Y7z329aey8NHLMfr73e8aLWp9IS3W9wez15+6XfL2Nzpvuzzzst4/H8zynM6+eTc49BdT8ZJUw2G1B3fsTQoW7T3b'
        b'LV1K1S+XROhUKQqAF+1Bi5BszMMCDaIUOAiuwVIJRoxpWCFOGTGFeuAKvAaaBaDaTJ/qJfoRM1EgsZYi3r1A7pUoYMTTuYB9gRSDUykzgb2eR9Yq1clmMIeosRaj0+Yk'
        b'7E3Z4DuGBtUDOUTzsnzDTJn7QnRME0021mLD4+Ep9PQpT4a99kEB43CPoDaIKsbyDgrQEhfDwnHsz2aqwVvk64E6YQ/ape5JnvZSEbZVEFjuhYPU01crLA94GAk6E2Qo'
        b'9aawwYj341UCe7HiFLHJR/lAgMWy2VRx3wtr0eMWvfEBBHfACniUj+oJj8JeiRWqqhc0oX3Rn12BBJijVMelC65iEG8qPMmrRo0XUGXdyCQrHnOcZK6CHMM+eJ4Uqu8B'
        b'LyjsUK3942C8eqCPdNnQIUjhiecEbXhBZnI1RlOLQ6d4wSEy5Stgx7ypsBNjIvNssJuWDs7RX0CbOgIuzeKjz/qtVroFaFpOgYaX0caYBU7CoolBLuHlBNhHQVOoRh3Q'
        b'FTA+RGaddxTpjys8jwUdmBe+Ce+tiAdYymIbOniMNNnsCChWxuVEraimUGlQs4mGUkyOVMA8d3fYLwenYBXHqCdx1oh/oSrEhKlhfMz1CCveAUwGqCa1WsKGw1iFmIR4'
        b'LsSAoNnX3MyBQdhlTxFNrWgET0+H1ySgNZFoGtXAGeyNLVOHzI4PqNqHP4cF60ncQQtd3hgDZkaAyxIP2GHvJcP68EEWlFjBajJO/r7BiBPKxuYBGnZyO03M8BiDy8LF'
        b'MB1eJdjS+aDXnceg8chWF3AOA+MKBfAkqPegeP7zhzZPxJ8mTFPFWByeStt/FZzGynZs0YIy2OnzmE1YtZtqr7NgtTVatEXjI77BU3Y+1CQF5EgkMAcM73rEjYPFbl6/'
        b'bZOows9GwgYVfhak7ycDpG4EmiSpQXY0XCO7CvbD47zxzi542iQEg5GJjYeaKwsLD/A442B0+h6VWGnHjiENNyyhRijD8AoYVnhHmSm1wQcRTeM3u0WgKhDUqMDERtws'
        b'BxcyCN5IRr+iig2ImIUcik7chmiAzFXdXLSP2YFWjzF4YiiaR2IakwHPwrbx+ETcN2V0QBnapIjrdDiyQoKEjWpbEsdvBqwHNDygLzgKLwaGP4onxFjCw/a8D0LteQKQ'
        b'MRbIb7LMlQ5RIbioh+1iEe1528NMNHdybqbzDDJzEbAJtazXBtYEjaEbwXlIQYRgGIw47QfXJsS5tgU5oI1Mmw64PAfm23ijXRsWK0AbyiBBKxl2GgHqQOAwPBdAMhRI'
        b'0fyXLXbDrhc7OdiwGdST0V4NOubiMLigzw8xieAsu2EHH+U2AdTMk/nYwDwiQnTYytUZCRzhYD8aij56pGSBa54SbII1APvQgHmxC7TBWaqHztoKshSeoCzhIaub5dT4'
        b'B8lJ9eDiOGszHVDDG5xha7N2UCk1+v8N7HpIWfrfuz0c1cS4mWBit0747Xcw9/3vr1yPMAYUligkQEX8U4e1JEpqG9Yaq5YJhE+T1Wd1WY6lamYM6dP6XUvAibjvNCdZ'
        b'sUasFafP6rDGHFFX88EF6W8tbhpWRnNY9a2PVdqIMTZmdTkcVNBYrMNhFbaJYBpRXaOWcOas5gMh/p/T/J38L8ClihgR8dZvRAGWHL6G3C99WCGMRyDYzpmojxQr7MZG'
        b'hEoWwlGNlL0RkSmhMbGKUfXglL1hoYrIcQrv/yD+AJJWfsdavN9UGu5f0V8CLJ9gMPhfuFFNZx6M98aYiu9It4PT2n9BmPFEFPzH8gyzCFZOsoENAbxhtRu4dlDuYbhz'
        b'LGa6AJXWTbB8hlHb5LxRo+pufxpoQKdLAw6L3R5ABF5u+85x9ft4GGvQssychLAs7QgvqSbbgV65B2idP64iQ9hPburQyY72okergmXGtKb8+FQM3Jw/Dd++yBFv5uYF'
        b'ToNyO3cv30Q8GCRYBnZVwDIhhuLZaA+/Ru8sKoKWyJUG1KBgg9LSvh2cIBcpcZuN5LDQVgIrEHfkT4qav9DXjXfts2y2iAF5GwiIAORHIVZwLGTH4umbac1W4645toMz'
        b'4kngLPWwNwcWa0wYF5ipNm5gljuRCxrQHx6N51MALo8vaxPv7hl3C/tHijoiBufWwJyY6Z9bChV1iGbF78ki/YbiJ68yqKk0vZj22hebZ3hXf6Ol+w7r27xab6G+vtqs'
        b'LastpoQ/t2SPZl6lyOKrf6zdtirPYM+aXKvv1A6yc+rSZ+3aXH3gNTX9l+7/VH3gxvK0qMUXtyWZ572X+H725ACH37+KnPHyre17Pzqv3bEouf4Zn4L7s485yS0ZRciC'
        b'ittJT/t79Fk0/StTqHNhxtTmqE2TX270s3xrytJ9rgE3b/oPhbUld1vWu/7CbS8ouvGWnmL9i7EOP+96auhu1jzHqVZWC/f+84lbsZp2NfqbP/l82fyG4IJpAb8wqeym'
        b'AruWJvnNadvfuGTbLlmqOXX3N14fv7nn6d3NX1m3D1U3P70v8JXLQZm7n/a6s0lz6eGPrfe93TnJ4BtF5+4bc2Ja4uyvLtuT+XH61tCmD9aAIN/rzw1IXs1tfvvDafe/'
        b'+j2zzzjORvEPjXlf27/tUNlqcz0l4Lk7Ns99Xnl92m9PdZy5XFxy8V/fx5l9pOcQHHZ85b4vz7VWe5hZ3PtodeG2ff/8rNXmllVq96uCr06+b3Tl+o7uzZ811X95x0x3'
        b'UL+8/pOyvjWHF+7X/GhazbPJwdW6312sCI6cEX26Wafo0Fuv5n5/2SGz/YfOT1bt+Eye+Vxn1O0bXPPIBtfPZ5X/uOdYwvMe5zdW3P/gJ9HQdYf5/9jzsv8bGRGffdOd'
        b'r7lwwGr5g4sZ7RGviRM+F109uySjqndblMIuP6TniZivjJ5sef/SxaFlX/kLP1Drabz65vXyH79Ov5pfuAXaxdzdkfu+4ojuxoVnS7/QfDdR+5d6+52fCJL23ql6vWlp'
        b'49a7JfUvvOt2c8VTD/ystN85GXU4c9D18641gxlTroWzMa6J399u3JPw484i+x8T717+l+27e+IsRHrVh8/EvXbH5pNP31Zc0W7bc0WQUivfb3dd4GiXdPT7xhN3dn5k'
        b'teBOds4vR9jUJN29v02SzkvBdjw+qfAErIZ1f2xpNsH+MBW2EXZJIp2BDR4XodOdCBbE3vG4hDJhu2ETvvNdu18lLHqZU070hLEjYqMQh1Iz0dTu4AzCFGwA+fHYPhk2'
        b'xigFu9mwkxz65nam4x28OcHM8XaYoIt3euQNL9hO5KkRP30G89XLHKm8eWyHBcwJ4z1Ns6tABcinEcVBnaGxmyp4uIWnHvUB1AqKYxW8/S+237R0w/oU7GUGnhKCSzAn'
        b'no/5fQAWS6wP7JVR512oY5LJHMxcAhrJoJiaSCVymI22uSQpYrDTWFgdHkI5oaOwBBYqpCzIXccbGIIKF9KbebAdXEDM3zqQSVycpaFPNdM40G6DGGj8bTQoBrkKqUYy'
        b'OE7MELERIqNH+iOCQzYpy5G0JGK4zazTAthF+39lOzaYZSNQRZR3TpARRpN1C6EmrNhAdZktb6Iq9KVcKJLMjyqs3ffABrw3Ev3GUS1QQJ3gDM0C1ZIxN2/wPMxTyQiw'
        b'biplRhuQFNeOJIyNIHeckJEAygiP7Aaz8e3ceMtC0BbAGxce52gRV5B0SMFqF/UxO0x5YVCjQ8ZiORKhj0usJDB3jPkPkBI+2QodvtcU2CU/bNqJbUAFoJUFxYbRvFW1'
        b'DjZJR8cGam4mVkQIAGL/K1Hus+SOw3cRbJPYeaEjbiAZZwOtKahuPQPBLvQJ9fYBe1D3urGAeAQOUAtfsTYXAbsdCHXortwFe+Wgdj/1OKdyN6cGcghQYSc8AQaFoIrH'
        b'KvwZUAGUAWrfjI6tLIDaXYAovJfIrkrBFZyaSmYtxkeOKlsMr4yXWtXgOdriJtAIa5DAgmjskko8RdvAOUqvc+zRGpbO4f0GBnPWsfAkGQ0kl+G6L4aqTQR7IN6bg4Xk'
        b'48mb5sF8xAEEzcfL2IeF6WtBD707KAaFIdhGFVxWV/muiwRXKTagBeTtneCBEVbCbIqQOAspoSRuhf2KMXN8Io2xaJUPH4kUzpp/gFLrJZPd2L42AF6hZ7l4CRfmBwqJ'
        b'MLcd5Bvilyo2Bg0R7aSZsRC2iZPJ4IajPWoEDetccAlRK5p07AlL05MDJ2D5IbIhSQzReCpQSZhzAbnjFSnzAkWTo2FzCuaGQB6SbMnGmg3L/siMV2nECwa9qaFuB6xC'
        b'EvsYT6KuTsJ4BQrmg57VpGrrBHsCIxsweahia5ijhrakjqmUQEpgrxMuyAeJeIii4MkIUpJAMHOfFtnFnWCZL5LwYLHDGJYFZvpL9f8/ikr/Kx8w4328WCrtVG7/NaEp'
        b'TovERsciDfqf0+WMWBMkmkzDUdKxWIOEG2Pi3wULNPqIr8fiDhapDH4Vq89IRqIPShsIpiH5icYx18RWwg847GwDh5fmsOsNMauDBDL8VMQ/0xSIkBjFPcBPRQIxJxbo'
        b'CLSItbGIw+IZ9SMjVqPu6/VZIXqKW6SJ8j5qPUuEJV4woma6v/8v7X95wchuwiC//TdMTRr/3PiXNB/bZxn/YWRzw2CMlQ9PofJfMAbG47CyJLg5iXVOIpyXoB+j6rwh'
        b'7KjWeLvUUcl4C1FHnBvrgZJ34x8u+MchXI+GyjBvVJ23lhvVGm/ENqo90XgMmywRsxsyIHT8Df/vrhvGDIfeQ9UvxvNxmCEeZXSEnA1rGcZ7fhH8H/0Wagm0BESUCgfN'
        b'gQ8LvSwzFZ3KZSuEkUiwfLxlljPDUL8njCr4r7rKSov7t1ZaOx+238BHri3zsJXWeu9UHFICNeg8LHSct8Bh0fyFjqAfdKWkJO9JSlWgfb4L8XY9sA8dLZdh78LwSWIt'
        b'TR0NbQnisnJAASyFp/w2IGatPEANQ7EGJBJ4EZ4i2tr9m+FJbC2yCFycz8yHZ2TkKWJ4ShwdUQO2gWwHxmFpQqouerpeoXDkiLO6XkfGUTuQKLj9rGGro4iYTJxcwCyA'
        b'w6CEFLHePg7TLmiHgwuZhbDRnOQGjWagyxGRwRTYuwhVehQOkaJB/wodRzS0bOhiZnESOEoeHgGN8x3RWIOi8CXMkuVJpAQXOIj4zF4GAx7PLWWWgpFIYlcA6uHVeMRT'
        b'M8xWkLuMWXZ4IX2cB2uEeCg9NVczq8E1kEk7WAtbYhUcNrZqW8Os2RlNKpy9Dh5XoL4st13LrIXdu2gJmVZ+CtyTRqkr4wrrwRmSd7MC9ilQR8Jg7zpm3eIt1F4qHbbB'
        b'AoWA8FWF65n1cHgatTRphM12CtyXK3PdGDdrWEE6MxOUz4e4L2jy2t0Z90WghWQP0tyFFS0MOAMyPBgP2LGCelwoQEdsOexF7d5/WM7IQU8SXzooU4O9qOXbV3kynhFg'
        b'gLQGnAXnN8NelrhUrfJivDxgHun9XF8O9qK2gxYzbyR5DLG0o+U7g2EvavvWbT6MDyyHuSSz3qEg2Itb3hq6gdkAs7VTsUP85SvgMDZnWuThy/harSE5QctsfQlq9Q6t'
        b'jcxG0A0yaLEVoOWQhMPX7ep+jN802EBnoFwaJhHhWSz0Z/zhuQSaeQQM+EtYfPfcsonZBM4eIZmnwNIDEjUMn2wNYAJAgxt56poGT0nwWJ9dupnZDLs4UoQ7GJwtUcfK'
        b'kaItzBZ4GRwjgxGDuOI+kI/raDbfymxFwlUZJcmCRYg9z8ej3QnrA5nAwIOkdPF6R5CPmu0ParYx2w6hZuPSbUMQn3JSDS+YfDvGLgYUU6uWWRbwpADrPnrsGXu0FrLJ'
        b'44BIWIlte8FJH2xfdBHRDq6S80ejexIvpQ7QIWNkq+BJMqhGS6L8UN9tt81h5oCcnYTOHNXN4UnUnWVO85h5oOkQKTcEnFoAT+JV15WCjSw6F5O8LutX+6GmwWFrS8YS'
        b'VM2W2pArtA0E/4T/yTCGEQeYStwvYCbDGgEcTDlMPGEgQWMInCPv8I9mrIg5mozyXER54mA9dTSQh8S1amVBM2P5LLiY9W7E+YQVWp1Fk2E5KgNnEbCMwRz0dj9sJ94k'
        b'FjiBU8qWgI4NKIM++j4f5UBc5jlyqbYHlq2jzUDDCAZRFo4xmIxyuAaTImAr7NClJdiDdFQcycCiDKADUSxuxMLkRWb+fDXq4CxqIhhA75NRI4iBTdFm0EerULdgDODF'
        b'Zfjr9aCQDBYSpHoQ9873EZ6bjpo3ix8HHXiCXvydXAqvgX54FpWCx8Cc40fBXZfWkO+P+P58MpQCC2ayng/po1EasUuzhFc2bdWVkZkQgLPOtHuHgmj3qtEmX0sbj74H'
        b'ff726mF8Bw4HkdrBcdAymbQfZxheYq+uTwcgPoKcZ6AJdiziayd9wEWd8hbwnZAraK5hUENUlvmoB7BHZzvasYbxUDXj2SgGNdQQLt1/B+0k7AmywVmc+WLSaMgUvyR4'
        b'gq8L/ToOK2S4uWQwYKmUBgMphoWWqh7ZkxaBwYUCfuZTnGmv2hZsJjVlwh7cjGORlC7KQS+hvXkOHsoRRd3C7VHO6wrYQ6bdwt2FH1TYloIzONNhCRaRid27kPgPp62A'
        b'I6BSHZxT9hfUSEgj0mCzL7wQqxxc9Zl8Z8NhGzV7LUfz0wyOzaevV6smHlTG0QgyHaDH2R3U0XHNwM5OcB2ncJbOBTTLVViwAx4HWaS3JIszX8ouUEXsdQLxaaYaVEKI'
        b'SBzqUY4YPO5NeiRaaDvWITLVaboCflDWwhxCipGhcISsRJCZzBj4wRNkpZwFFXRBX0VnaVGkOa0DtUa54kEjKKek3AobtpJJEwgYAzPQuxi/zUXnF+6LuyGo4Jsp2LkB'
        b'nCMURAckC5aSKnaKQAulQgG4dhhncaZ7AuJU0kmOOYhDaVHuTTXgwtiShz3upJr4YAGdeTSrx9D4UUqlY3GChiSCw6G7EPdTQ/rBmbO0gAg0oMRrviCZX8/5kaiCfEEY'
        b'JQ2YlUT9ADWCwml8R2To0K1Rh0eVhI44iKN04k6DY3AAZqD9gZJhBukLLmcnPE66shiWL6KTAYtd55N6+EJGQBfJEQwugWrVzMb4IiLiRywE9tHNpWOKWLl5rUGzWYua'
        b'iXsKhpZLWZJDhM6rAdC6WE5iGuIgaGJwkQMZB2DOJ4SNPJHsItUkJnJTpnCMcEklOlRCbL7fepjazflu1mKM/V9hmQ0hnv1CffrQMlKD0fVHp0hISOxL+6zow4Nb9JnZ'
        b'4rvo+AlxFrksoQ+NVqkx4g3viHCEwG6FPX04ee4kxkQM1Zh5IZ4JiQfpw5uH1BktLXTQmYdoaU+eTx+OOukx5v5LOSYxxMaWWUUf9ogljIFLtIDRDbF5w8yLPozWMWCs'
        b'PN/EFZnc8DWkD+PRCSdei6Q7l5DYLxR8jwKjcZSqWbibsbPiBQyxd96+2YixSfwXi2rf3rs5DEmG/uvIC/kKISPeeVmIO2BjI6O54wWorW7PClDu2MmmwcwnZyrxf8+t'
        b'JBUkGqC3B1H56O2xKEPmE0fy33cr6ek/H5xBc4Q3sbkJTMJ6cJJwEKGgxVGGOadGmLOX2asdSC2PySlTBTOw6SylOG/QMo7gOHiW1HnGfgpjszdYiNu/68gaPtzSVEPG'
        b'SksHt935imTZozaPKl9g1G0QtXqkwY9UQY+ieUjHqFpMfETk3mTMyP1R1KNJmuOjHmGfoOCSOETmjU19iQ2hl6cPPDXeuDHH9JEQUuAiPCNZtWI2af7dVVuZLi1nDlHZ'
        b'smecNqA58faO2avXp6bYhKq+Xj3Fa+ML8TddDK46en/51L5FqV86P9/uLGl00YzLMOI+nDS4puyfvrLLLbNipth83aEFgsx/FmxZsm1Fw+6RdDXJCsHZPCe7vC0Fzoqv'
        b'l95760BEy+SjxzK5vMT3z2Y5HPTf4KqduuCVp0wCK9anL1q99tP6/Bn3tzyhtv2pOdufMbS5Y935/rL49yzjQzX6k9RfuJJ/6uILx0rD7szeVRd26PuZvpUe1a3LkvSj'
        b'g7erpSXezX/53ezFo1YNk+fKvJ9b4p6x8Ot70oCmdHULjx+8d+Xlzv20fs32D1e7mALrGaPbvvywIO2Zty0+0JA/vWut03K/MHvFG6Hlm1y257XI/Rp3/jq5OPnpY9J8'
        b'oF7pcWeO3YHunt8UP+z2iyxuD3JYaNe8qycm2Pj1GU2Ht7x3plVRKFMvuvXED2+8dGO7Vkf+POvjXj92Bxhoi7748BXLxl3D5sYZK2I+u/Xeuo+93F/XfrKCuX2j+7x5'
        b'74KI04VPWL7yoWjxt1sW7QyIavM3rSm6USQ/fa/4t/M+hxwUP1sePlj75LnY99+03fu1y/Dca98u2HT3QcjNcz8vuNZ16tQbddY3S9845PSCVuWzZzSuPP3dUOC/Njp1'
        b'JnJVGRpdu0Zfd5jZ36NZm3SgzavqzS2GU5bvq/r8W83TnrOvK0LTPty9Ka7o/LIPizxfz9v0sqnHgyKvIIf9++tvfGGsOfRC2aa4U0N7dsfmrn9K73Ty7da9v753wiL0'
        b'2Lnrh4RV16fOKF9xsxNIhn/dcmdDaVCv6boIvyfbT3gWw47Tuve+NCs58PKW3I/NA4YC5foP6uJ6ar6K+qD323vfLi7oax2+N+Xrtf/Inuon1aEXuF3gajC+dUU0q8ao'
        b'bQ89yCJO65QadfLQuJyD+djNgjbIRFuJGwt6Y/3IdbOL/XQ5Ccgnh2c2Y3fYElgl4EAtkr5pVC+YIcGRzmC/IhycVmMEmux82GFMX/asDZPBItDhAUp01BhhBIu4rtOw'
        b'nhQciYSyMux0xx20wEEbdyEj2YMdyncFkW8PIF7jKmw9yNur8dZqy3bSzgzAEQkq2R4J3xDt7sJUFubKAY1GgX3ynQd9O2V2OPoLB3rZAANYRu5NdzgbYyM1vHTdZiuN'
        b'1M6tooZEfftgGcHeRK2wxkbjIg5elS0m9YlB/T45wfOAohBU3RRsrnMZFFPNTP8UB3gCXBtTTWXu4z1qg5OwVI7Nt9zix7sk2jBXOv3/1tDl8deF6n/zznZUUxEeGh8c'
        b'ExcaHUmubn/CO+9fsXc5wngJOeLxmP2f//xWpEfdL2gSixdNwSze/TV1lm2AnorIta4BcQJhwF8j67L6+DZMYID+MieuwTWJe24xK+SExKEDcbSN/lmSCKWaJIVde89C'
        b'XziwyViup4eJYFQQExc97hb3Lw6sFqc8cXBZQ9iAZQEe0b9iwJLOPGs83oSFGBYOw2Gfh46oSgM1xmiHUAx6Zj/ipFVTeV7iG9pxCEGWR2VxUZoq56zCP3XO+ofYQAwp'
        b'eDRWt6n34+8UsfkOqp+L4v5bvCf3SL1q3uQU/lcYwV2IW5kQrWjNLUwqdtkCuyUrMde52YrCCH2t3Nz93PCid1djFh9AbHOpyArmr4q5eeKSQIHdhsZbhX4R4hb6YpTV'
        b'i2tLPw3Z/kTXiYySs1nzs1sru3O7M2dWZDiaMgm3RG8e7ZZydI8Z3Iz2iQiB0m2MyJmb4gkGeYX1rPAxTXk0ErUneCyCiG9W4jT+4FZ5VBK+MzJ8dzBhaMi6nPfX1+UR'
        b'xoo6x99vFowdFQdjnwdj5lzjSlbSOhszjtK5CQStoyJobfSXIWahFv11gk5nvtIZT9LYVQISEdGxQbyGuSFZCRE1EuBq8H78MLAEw4a8YJEI5CGJ5nwAFjaNJbBmSwqV'
        b'kfBdcI3cBke0KRAyIANkiqZxmjP9yAXZQcFqGSz1RpuJHgvSYSkzD5wk1OIRzzFdMZhHDIm13KypDMY5VV0m9/T2trUTMeACqBH7cArQSKWOssOajMk2ewZx854bU3UY'
        b'BeaGDUpv+2mzOxOTBAwXwDKfOxK2e2SOkPnSwwCz8zaOdhwTi4fVZK4w/qCATKDWG8Zps08xCsxmtxpW+m1K/SFNwPjPFqixczpHSW0KCyHzno4hLkLraZ1ARoE52brj'
        b'OR+g4Zekv8dIZLokX8l0EZO+2YTw8FvQaiD52u52foAmS+fgk4zON3EKzPW+3an+wUccs/cEY8kY7+xS4MG5nrLVb5P2Hu3TVon+iB22ZctAvQKPwpQ+TZndnqfcbaxb'
        b'rbDZxuRuwYe73iHHBQFV61e53pz0nM1zaA2FfaPOcg7ru0i9N+LLb2J62ZLISD+9Th69Y1t+E9GQ9egkxlpiTh41v+OajzaKoNdXMkGf7yKtW7zcN/9VhvnWl7nDZGss'
        b'I8+S767Pf1XIZJUyHzDHnA/zk71OE+a7E1iQo5AJXSIG+ZwHyBbHzDY5KlA0oWLvXZW7blwV/08XrcvRDs95/p4g33b/ZMBygWT2lh/0GyVbNt8u3zl7bYPdcv2NLjXX'
        b'XCKeZEsliaV5N7s+1T/wr8Z4h9vfffdd7wfrvxNvW+P28VCxi+78pUftvr/rt3BVsuPX25Mnl77kW/JWvX3TmbwnC376YukZg6+1qp572cX7ztHn6/aou99quR/6csbB'
        b'6F9qM0C61U8fRuX8eHb2s6c/NxJNlgQMnzOc0jt13qDwy51vP7/ZMOy5OaYpTUee/yl06EbUDxZPf7bpY5PFurJNdzxOnYv26czU++Wlf6xaMlf7yyG3Rcc+nP3Lnlav'
        b'zoyaX5KfW7GvU2SwsO4L5/IvFS+BB5YruI9+7/be0Q8yDklsnzr1jWDbjoXzvhgu2u0rSpr1q2xTe7TLG0Up9xuWqP+zMqD3p1/v/9L7XquJ14Nj3h8l2NQG29d+53xW'
        b'tqC981PPoFeX/XJrq8GbibpR1+FnOqmZW2vOvJx390jDwI0r/ll6dx+MfF98fcmF1kbH1h13FKNffiAYrJg/tNT/rtn7ptuh+k+zb+aWvxlxL+39rIHtHgtNbV+DLfdm'
        b'd6i/IYx/qfDWWy6v/65ecKL2o73vSHUJV8eBbB25FBbaWomwy8MKUTRnzUrJrppmtgQzWRRrultbDE5wCSDPgrKgbWiZ4yvbwqX6XjYMI5zPgg6Y7UsNlstgpozwde44'
        b'oKE6A5s8xOAsd3jpbN5If+ZMRcqePdo6oGhSiMYk2KOVhE5SWCsANfHgEjXH6ELMaDHmcgtANeJ0eTb3IKiiRkLlOy1gvhfowD3IQi8814NBPWJssX8yCUKcTwwhtq4T'
        b'beQMpAbkI5vZrqhVe0ETeUW5zaI0ahuAjTmvIjaVsNVqGDScpSHhEKNZCFvIaASmgvPoa6ktNqAwAQWiEM7iEMwioxEOqmCfEhrCLiHgEPRpJYUDXIW18CIuOsc9GXbi'
        b'CJgS0M3BGpCtICV7rdSWu3vRYYZZnDiIi4QVsI1Y6rghDhgDhum5Bi444qMNib4nSb0HYdFmjJP18ZSKGG9YKHLiDMAJmPdfqrr/E7vhCazs2GlHjszTf+fInKujRmLN'
        b'EJZThzVidXnPX7qEmRTyHsFwxBfMemoR32BavLWAmMWexLBBty5hW4UcNtwWUsNt8p0+8SRGo7mI2eRJKkZTbVSYGJqyc1QYEZoSOqoRHZkSnBKTEhv5d1lPQbIeLlMf'
        b'/9BVndm4HoO/fWZ/PWP8mW1OuCk77LRk7MjGy6zdWJ0x8hIawOx94dw4Rg23R8X/Ye6XaJTZKIHKFwD3b30BPKJLVhb8sMcPKc8nF646iCQ2DNnGt4iIpJFMm64P+gXw'
        b'KMjUj1kvd2IVeJM4mnDsi5BPQz4P8Qz9MlJz8kbioWV6qcA/rWycexDBY/X9o9p4iiYSmvXfIbSdyZNVky+kU0Um7Y8ZMO7hGcUfb/rbM3pBd/yM4kv5ebN9yXghEf3U'
        b'hGlVZ+asUfO3BOX/8zl9xL8D/k/wyJwKvGPmnPuKIR7/o7edIrP1mmFIbFRYhFuoOOo9T3XGbFTgvn/jX5wvxX83X7uTDR6eL70/my+9ifOFP97yt+erbcJ8zWaIP9BS'
        b'R5k3mrEV8MLDEwbr1EI2w9zHzxiu/DieM/a4MEr4N+bsEUkMz9ejARo0vSmXdtkcHiUcOehEZxPiyjFHDtM1qJwWaMYdFDJ7vwleobgydbsHeVgcKWBe2YoHM8TTZHUY'
        b'vRZ+25Ll0jWEYgbN2nXFfBqiHjTCepHfxl3gAq4pCy1weDGRZJ+lJWJuaRJWWOt1rRjqCiQGZLj4oSPrhC08LXNzFzCirRwbOTtmYOmrjCIVZQjuP2/6opMOmKeb9X5l'
        b'0ow7nNtb6R+Yv7qx82iZztqBzrdstNe7/Oj1wfnfDr+UZT1tRPOYdWFh9lSzpZ6up+2u751189sR02UGy8tKPup4bt1rU1O7Wn+Y863t3ME9ptNzGl5+9YuvS27H1Agk'
        b'NUd++3HlO0mBi86XmzbXfyMVkxPUGDQektlaucEM0IqdZYMznC0cgQOUByndDY/LYU6yigsiPBCsNacHezEoPyQHJevwToc4IR/sXKIAsSNgKIgCCc/AdiQYuc2YcNem'
        b'Ds4QLmkXOAP7QTvhVOBleAnmsthZ9yyQM4t+3a8H2nmnNeTabAk8Dq/GwQxyO2ZkA8/K1vq5kcsv4WIWdKrrUa/CZxAnU48YlXX0Qo6/jkuzeWRtolX0R6fY2IrVwjts'
        b'YkRUMD4YyYJd8XcWbDy2+NPBVz3kHMdnuD6bbDhuEWOCHhU+hFp6pJlcshH+JlzZLlLEtr+9lJv1Hz5M42CODz2r3NzRmUrH0gxmqYN2IWyK9nlkj9TgfyuMHgr6VSYo'
        b'0ypTj+IiuEKWXPJwY853osQRgghhljiTDRRGqkWoRYiymAj1CHEhFyhCaQ2S1iRpdZSWkLQWSYtRWpukdUhaA6UnkbQuSWuitB5J65O0BKUnk7QBSWuhtCFJG5G0NkpP'
        b'IWljktZB6akkPY2kJ6H0dJI2IWldHJgM9co0YkaWOFAvUi2KidTLZIrYQD30Bl9oaaBNzCzCHL3Vj5hJjpZZo+peofHYdPC+7YQQMzg+lXkcfUWDb00MQYNYSLxbP7J3'
        b'qq65XBjeuxGxiCPDi08+DdUuKvzTXVRA7tGE9zP/bYSjCS0di3D0uHhCeHXQkEb4Lxy5KJQWsWHtOvOomNg/CI40gbIwTYsf2clneKfi6PaLZKBH5sbHPPGxDeAhVq7J'
        b'4ALMsbFjmfWs+mKYA9IpMKsFXAVZksQkP/RSmddfvEc7cQoo98fxhrGXD7SRhZuLtWKSyf4MeqeBazDHBeaPRZiF1w4S24cti0AnlsEGYZbnuPixIEuNaIwXLwfFMg8v'
        b'O9sAUIGdistYZvJcAawCl92oV6aL+9fJHTw4BpR7s/Ai2tJgCWygh0huKKiiwZE3wnoujJ0PmuTk7IqC2aBEzrufD4DXGEkCByv3wD6iLU+Og6Vks4W52AoR+yjBTuph'
        b'nWC1BRihmu482APOyMEFN6/1MNvOFnuxn2Qh2LIXnE/lQ40eI0LVwngsVuFOgX7ugM9s0mV4Eo3mgNw9YaGXNXqNleA4Xqc2aKcOqi7s4qinJDsRvDKdukqCddvoy3xQ'
        b'ItgKW1GjxrlUCNtLe5xxGIf6xq7g4YWl2A+VENTTz/IUG1fBC/jtmLepVnCU2oY0gJrDSpdRoE0IK2EXdTnVH0uuuk5NFzJiT0cOa65TtTwYatI3BNvnYBMxmA77sY1Y'
        b'0RFyQu/DSnbnbSzK7Pnuxjh86YbZu1hwEbRM8BHFMjbhxEXUoa2UEziESOPgeTWs8T9lp6DWEaAbnf05AcnyCTHTR8AQafmB9aADw6HtwGkcYmDMZZUb7CX9tgsFpTI7'
        b'f9gmHYsBDztAP/Us1Q+uxP6RZylwdTaN5AsHQRuZskU7YBkmmKhpROZAc6YD6wVB4Pi+GI95z9BIp2Z1dw6VDm2E83Rd0z4q/GjJ3X61ayWT6s83NyQ1nBU7Gnh7DDxp'
        b'4MGe9OmaPnLyn+uco9IXtB9I25Oa6vzjh5c3F7ad3vFayPstdX0j/ZlGV7/+psW1vf7em2vCup+M/j73Ne3b74UcOWDevvpGhpfWTx1f/ly2cOrOE6ZfBLy5Y0qK5TLD'
        b't6dccP3kd+dTqVZOmZ/+8uqkhhsNZrnTr3/9+rEXc1OOmd7+9Jusfw6ZLj3oufXtA4k7n7W8lZuh/vQn/m8VBFdctxstYZ0Wv+L9FbBz2iQr7h7a//SypT5D56uXGn68'
        b'5aWtF1xt73z4hq3puwNVZbLf8/Ztn1I6EH/eaKP2tTnaCRpDX51x2ixatjbq5JuLVm8Vf7TQr7ThZNs7FaUVGzctrnYtdZ2fPzt/xEpy+4jvPyZ5DLq5X7PKd/s5weG1'
        b'wlurP58bqbensnREmjbwVvl31ypOPQNMvw9ewfyYXqHvsUs6jdxdbAd1BpagTjaOD0Fz2E/1dPUgE61kT2s78napFSOJ5eB52Me7zl8CqnRgvo3lbG9eG4Aj4x6CnTzK'
        b'CFwDJ6ZLxoX+AMes+OgfdqCO3u0fla8aj4KjF/uwBuTSy30xPE71A1loOZVhxQ3Z4kTT4pw5TQsZaeVce9CPDn/s7ghvcLNhOiNRcPAMB3MJbizGEh4jKkif1VgJuRdQ'
        b'//GgApx3JvE9aDwFGWhjsfP3WuEyXVDJxwYBfVyaNcj3wVugIJYNCIGdhEdTwGugFOZtIt5HPbF7hToWnIB1jhR/1QU6cMhtHzsPcBw2jwvDUTKZ3J+5GyEeE2uhyC7Y'
        b'DHr5XVB/sQCc9Y8m3TIF6WAAlYF3wTgZ3QT1DwhAv8VKOjnH1DhSPd0C0Q5/hpH4on5ricnkbIcjGui9O90E4VV7RjKHg/WwMJliz07Dq2h1j/OkgCb2BGe7VZ1HLmGn'
        b'ccS3KijBcD4aC2KShiAFtAHq4SUY5oEikofsHSKxtoSbegD8P+beAy7r+9offwZ7LwEVFQfKRkBREAVE2UMZipM9RUCWiAtE9gbZyN5L9hRJzrm9SXqbNKNt2vzT2zS9'
        b'bZMmTW930vk7n+/3eRAcGfbe/+8XX1F4nu/3M894n/M553z6+AaKiZDY2QSTH/baEumhhb1izMUBd97NWIjdm7gMMSY+cMRToEwEhHO74BEPoMugH5uoBx/PkxacwBao'
        b'uYrdUuW4qwQMsf4aZ8Y9s7acc4Y8FjlobsM73JZcggdp3FUwBNUn3XkVqhYrdoA72Mz5D5NgKpnbMd99OCuVQloHxfAQxqx5grlnFMtAJiFNVjZLgja11MTQh0PuJrLP'
        b'9ygpvmhGBDt65GD7PIMZXxe23xYoKXF1E/ikIAUh745jqTncVdDcH1avgCXqKIlEBOvlhHJ/l5PX4dJ0lLhrAFY/5//8RU5Bgzsr/qbvKAmzNSRw8slK/5IkH431PgCF'
        b'r+2xFPGvWq5brpRvbFbUGKxN63lqsF+/Hrful1VPf53GxZfzX+1htZL/Dq6CvgSuPq4o/2Kl+yWFq+VD0+Jjk76kmP6b0gHx3UuL6bO3wtMzUl+gZLakNLhMaIRNxHO7'
        b'fWe1W2O3xPBYw/gYw/h0/u7OozZHV1fhxcqsXxR8yQ78YLVnA64Ydmp0VHx6cuoLX1mQ+ssv2+8frfa2VdIbf0fBv1T/XDH0cnJUfEz8l2zr+6v97uEK14enpRvyL0X+'
        b'jwwgOis6MuPLLmn4yeoAdq0OgH/pxXtfpWkuY+35fX+42replLjS17AWURnfwAvPXz40KjqCiOa5I/j56gi2cVzFPf3i1fZjpMsupdbndvzRasfb11H3C3d9V9q11H/0'
        b'3K4/We3aaK0NzVZeakCv735N75x6ezLERbga4iIoEuQJbgqzlW4IVl0CQs4lILglfJ5jlTX5tDNc4UtCa75hIXWpIyLkmff2cpR3NS6au9w4PY7dHv2Y/lKj+ZsYuMuF'
        b'k5LTn/YsPOVdkG7SU7795jecRVyN/L9/7+InYe9VclXyfeQFCsXC2YXvmgg5XKOODVC4FuZehnsSmOsT9JwK7jel2cfcnThfH3bcFshnb5Nqt9WZPo6XiYmNTvd7ful3'
        b'1u1vmPpmSbNfW33nCGrXloDPOCxgIUMXYRinJM4SrDNbnT1WPxEZAwuu3px1AMtyyrBsBmP//5zWPB2DRTua4+cu5k5rFq3eYqc18zIJMZ+GlcVKT2t2zIn7IhZoZ7mM'
        b'oOrTWCjHrKLHmyvZWaze/lWnOam3X3iTlb98k9Oi0/lucoVPBGXdEa7t/E8vsNVl605zuDK4LfiIFfr7OnuNBRbeZDGwvTZVZt8gu++Z+blcrkKHhAymXWXUhWST5eMw'
        b'91WSJZnA3FvKsCRjK6Q2i3A0/kZknoiTV6+NGF6K9Yj8rM0n3Cc84acD0XGxcbE+kV7hfuHC3+lf0k/QDwz55V5Z25Q+oWC8ReH74TZPRas9O3ItNVpCJnzhrm+yQ2IV'
        b'eTVRtuZTu8Q3fvfJfVnf5WcvsC/31samPaPj54te7jyNr3gvWD1P+zoC+C4JYN+npKcrC8lL4xU/idv1juA0w7T0+MREw8zwxPior/DpCgXPUiJyfkFunDet5Gq2QIGe'
        b'0Tj0abJh1N+V4nNeSxelhTJhvGH3J2FvRBj/witcJeYj+slcS1zjczzAxCfsSNqEblWUydt3fndGycd5KGGjQ2OCvoN+S1OJY4K+7rhllKBkr3nYuVdPoOHLVd9qg9bX'
        b'A3Tk3xbbJOs12KoK3v6FvtOP/UwU+KOr/Ns+ZswUhVZol5iiajArdj8CY/zR1wMcwe70/WZSvwjv+L0Fs9zX4aww6cP93lL3Ae9BJRbp4j0Y0/gQF8zWyBVt7BAyz7B1'
        b'LGea6+HIRs5Bi407HjtoY4G/F1cehmDK23Mj9JtLL1zQwH7uxTPQFmTGaqy0wqwnjMgI5BJFO6AZazk/TxauwD1vT3hkBSPmcgIZAyFMWmKeREV95XmXQnxaKLe5HNsc'
        b'+6Zso80XEuT+Z8HSXMUMmTU2obT5NUrsOWN6rNWs6NG/vgBLFWo90yxdHYKJ9rPKTKypJ8Edt0WxZREzg4ydOaYyefKegtSIeE9Biubfk+OB8XtyPGJ9T0EKIN9TWMV/'
        b'0dLp8ALsX78ecY3g0aMfL7FVYgNWEMmIVYQG5/63KjyoKauI+CzWh0Y4ivWs3tDqwYoSVIhgaV/EUxpbS/Jv2p0nzw7l7unfE0SJytmJmnyhaqFWoXaM7Nc/M+TfIkih'
        b'HKVyV4GdGcYIohW4UzoF1naUarmQCz9XpnZlotSi1Ll2FVe/kyXkqhGlyX2qxI1GP0qrXBS1i3tHi3tLJ2rDXUX6Xpm+F7An7snTH/0o3XK5KCOuVIWs5KoR1UK1Qo1C'
        b'zULtQv0YlaiNUZu491T4dumPwj1FGuvmcnHUbu6cVJY7yGMX5qgVqrPeCnUKNxTqFurR+xpRBlFbuPdVJe9zb9+Tj9pK7+/h+mRvqnNv6dIbitxpJHtDjZvfdjY/moEo'
        b'akfUTm6G6lHanPg3fk9NwhT0T3hsdOpP99HGrJPqLobrn2CqgP5NMwwnLbBWN7Bjw/B0w/BU5n+5khFPxL+uoRhC69zzUfRVZDqz6+LTDdNTw5PSwiOZYZv2xOmiZzrp'
        b'muRUSVervYSnrZpEpKSSDMMNY+Mzo5MkzSanXnuiGUtLw6vhqewuMQeHp48vmbX1xARXddzR40EulobHkpP2pBtmpEVzM0hJTY7K4Ia7ff3BrcSTFi9kGbFrSF5W8GRN'
        b'k9V6JmzrV2uaiIvEX5oBITGYfnr2yQ3iluqJw1upur4sndILnd+urigzxWhb127DM20utvfclkVZGnpyTqmoZBoR2WiG0Vnxaensk6tsZSMk3pzoZ0AIyYAkRjc/pqdM'
        b'8avxbJD0TUwGNRceFUVk8pwxJUXR/4bhKSnJ8UnU4Vqn1VfgF7aNT+eXqPplsAgQU7KO8taUFT3tYenlyzu9ocQea7DchysCGuDh4yctiworWKiMvThmkcHwaDLWsQuh'
        b'pU0ANbe2GXqTP2IVZGKh4k2ys2a4E0OogPJtWGvmB014z8JDRiC7R4iNQUl86Y+6DChjibFZgsB9WfuxlBPSKgIcCbTAPpzEXpvtUCkQWwrUHUW7CIjf507Y1aCYvn18'
        b'z9VJY+64nd1uhfk4IxIcMJGFauz0kRysQjcOmInYDSDuUJEGd/dxiK7hgijmsoj9FGY+JjIQcKVfYRCaocn78bSwyIddolVujhXGJr58MbaTyfKYE2XCte4JD0LSrsgK'
        b'DusLsFIAJR6QE/9+yceCtFfoywrx0eOVLE5KpeB2v2+n47e9h2Q+3JR4XlSVU24UYazlcc/6Qpi18vntC2qFP1U5eEY/8Ys//2zq9YETegds/tBxyNo0+LvHBwfeNr1i'
        b'csnff0vk6+/turi/yFS57i//Pngpv+il4nzPbb+6YBf12ky57lavu++pKY+M//vWX15ufWP0vz5p+FTLr3j8Nw/L7tZrxFS/+duUCxNthfH+bw04GVWNOhi9W6nxu+nb'
        b'WaO/+PTNOY3QlP8W7z71/f/+Xd1/Vm9uqWjYZuRk/UNDp38I/jzqFHwi00SHzzXs4Mvi4xQfBcCFAIxDPnf8swmbYHTt2Z9IAE0wwR3+4aQeBwUNCPZVevt4wjSu8LTC'
        b'ncWH7+GP/KbtxZJTSSiEee5k0kty8gT3w7W9fUw33+IPJvljSTe4x31pk00Nlkpjp0wDuOipDdDJ9XkRZnX1oMKbD74wkRMo6oigE1pucrD3LMwoYSlBAT/abxxNNzeV'
        b'I+qaFp9UxymubVVrnDGzwhJoPMqwghwMiMxhCjr4E7mJGByECVeuxPiaA1EoEPEl0Ut3HyFITUuFi1Yy24Vw35KP09+E7VhpZmlyADoe302gkc2VxoOeA1AoOabjTNYy'
        b'bws5AfZgqx7MynhA/nE+UbX14j52OCUPddyKyGmLVFNiuGqWmTC5nVX184ZK/zPExfzINKFBDJXQTzYCN/Y8uMNul+f43ZTneLVAMS2FBlfPkVis1IheZQmvDL1z6URA'
        b'ouGRnLcFV86RXRPkDhPyUGkA1dy0FHEpShpIEb+fD6Uwxoe886IIO3F4XWlEYvNkVhkRmsz4E8SlbayWqRWLgZT2KCc4qacrEBO9XHw6zOzrRHc/63AtiMnLb2In2LMI'
        b'dDkujl2Ni0lX4W7XZrHsWzmrgT8Ay9Zbr5yfc9P1qupdcwj2JYeJYv7ZZxx9bVamyTiwyXx9KyNH8Mu1mZLPHfI3cZLLfrm72FFZ4i5+qrPVAzHbVV3+tPJeo6j/hROy'
        b'1PQvO7xxkg4x1ZQFtK3Vq+v81ZxDkIsWXHUI/r/rsY4jU5VVqvh6zuXXfmMi5pzLVy4sfxL26oGXHl/BOvdegYmQE06noQJb1rEoDMAMY1OOSaHu7Fd4mFNvsTtCdz9B'
        b'B2mRiaFcbuU3ch27vhD5r6xzHnM0RGKx+bFDcYb94ONvcVKMNWZrZRHWP5lkyTkQ9beqHTaFua+IIOf8XYXCbxRB/szbc5/2I8v4cY5Rb7zD4tjWS2wabx6LKiz2MfUy'
        b'h6EgPsCQfeDvw5w4MAzFyvY4gXPxqvEvyaYxZtiwOeGTMEutX7mdCftOhLGuabhPeGJMYsSnYR+FJcV8GlYS6xXOk0a9ioL23esmYk5hyGli/zP0xVplgcuwxCkMHNiZ'
        b'zuriQytUQ9/aeCDaigdrk32dsYVTH/rBdk9pBl3RFkZ0WbAiDS/4cvkvdYCn5nxdGlzv2X7Kt77eve37QuQ4sy7G2Z3eliWMdedpcoRZQjlfRZCc21r/qJpn+GWJoxuL'
        b'4H6Gt7cdzjBa5TzdOGjN31Y4ACVx3mY4YcXe4j3dE1Adn/3zm0JO0n0Q4sI83Wv93ImxXpF+nKd74xpPd4xA8K3fmpgrhqeffNrX/SVHEnnCF3V4n1ZR0pDJ1n/eHq7x'
        b'e39F90dfaNdeWnss8fxhkBxk/Pt80cDceCxim0SDLAkH2VXhIP7KwGjmDu97yiR0j04nW1iiLdc6PJ5vTF9OjY7hDdenIlKeYe+mRqdnpCalORi6rN4iLpl9mGFyRAKZ'
        b'4F9hpz5b9cn6ZbDio3gv+CiHx709txKq9gw+cdri1Ol1cdTSKGrI2aeYkI7t3LUZYfEwxRttZKJUMMONt2kllpvEbgtQlsdyjfPxt8cCxGn+9Fr7BwGfhH0a9quw1yLi'
        b'YoaimfM+5KUQHK+aSDIK6b1rImu889/f/M4P/+2HL58Q91wiip9qzE04M9k41VTa6hUS2Og8ub/sZZXWjwW15ppZD78wkUtns0o3TTOTS1gTX6l2XWJs5Ic8YSpAJ/bc'
        b'xLuwyD1gIISe9SYUM59wwEhBIZAvsDLgilW88eWFOcz+OmLMWTkRR3Z5c0jeBeo5KK98VoRj2KTNXzfUDWXJEinrdmVN3KXk6oH6C+sY9vlYdG2VBZZpIiEYjoUdvikL'
        b'p/DRaQpclZHsTU/w0JrmeRgwKIke47zcj4HzM4X+oIh/7DFcPkxNBL0Qq4/prGX1Lxnm87n8qSiHr1L+Yu4QWeYvM8/k7/Sn40ySY6QZDP/77O7C9/k12f3Zx2qEN52u'
        b'/F2Uxsy+Mzlmn4Sdf+nNl4nt6jsLtpdaN+baigVWKHO++kbkr0xEXNF77IMcKOLzLit9N2pJvfeb8L5MNhmzuXx69QZ6xnNtGsCyK+TeUJOeJz37EHTXC6uh2wIW7/gs'
        b'opDsjATCHhFJIayTaG2vUS9Ekm1qX0WSkt5NeD54Tz4tPDM6NDzN7/nOXjYIiR6S4+wbuW/o6o14lqtXSq7MBx4lKZ3+tYjVZdVfH50ezoLIwvlgmsvJmaTYWLFzabv/'
        b'U5TOvyNZKAfmEeY89ebMDXw5Iy2duYF5zktLj0/iQ+uYxfpMPy5vxa4LiGKOemr8WT7kVSZjY00Nv8ovF835K3iLkfHTLl8lXpWGQYePRJVK9Sj2bnm+Ks3GWc6hGeoG'
        b'ozAJbWZeIoHQQ4B1525z9Us+/0MiK3yi16uaIiOQaRKmxzhybtRNzjIKbwg1uLot3wqKFgRxdjRfBHvCVx/G8Z6ZPzUVIMBmeyyJf7PrmDCNVV++aPWO73cs1I66aIg/'
        b'8Pvl32VcT2g4nv7AMEeQa+DSJvNfI+GuNmqV7y2bKCsFvtUXarjrL4pNip3aJQeH3re72nzXvPrn210KrX+/3//DgOkdvy2yyPzhz2RiP/YZHXa0tR689PHog5rvFdhk'
        b'nVPxH/vt5dax4T9VfPaXCvuYeju7jN8GusdueHnl+kuf/k7oHGaEcj8zUeA9kKOQG8O5IMUwJ82NqNThzs89VQiUc8pb1mVN6kO79OKPh1iFC9AY9rT+VsAlIe+yq4Ia'
        b'AfMHsqswCXAzh2D2Ic4bdxLyYdjM1BKLrKGdi89XPCSin+ZwiJd+HWSh9m32e8ovyPsEZwR8CMD0Bfpc4glVypLkkZKdUCWpuXRDZGaF04lYsurL3AkLz1ahJnJf16/2'
        b'nrwk6ZQToR7fXIRqSGs9aIk0uHoPCtyJvI4wW/cZoo06Wu9O4zS9i+irUQGZAo+ffQwNXOnX5BeSw7W6a+XwcwZLC8n57zhBrLgabc0fru9lx/MyieFJsUFukfJrWJtN'
        b'RUvK2gFMNrP0SeZ5UuLOT9mZrahQvVCjUFyoKTmi04rRkshs+SJFktkKJLPlV2W2Aiez5W8prJHZt2SeIbNdoqJYcHZS9NX10TTsbIo/B+OP7SKTU1Oj01KSk6Lik2K/'
        b'JHOSJKlDeHp6qkPYql0UxklDphuSDcPCglIzosPCzCVh4ZnRqVysAndA+1Rj4c89kDWMDE9iMjo1mcU3SONR08NTaR8MI8KTLj1fUaw7vXsCWT3z7O656uPLVA5bCHa4'
        b'mJYSHcnN0Jxf5WcqkMdJAUkZlyOiU7/2SeQqgfHDeBzdfzUuPjJunSbjZpQUfjn6mSNI5kOppesQl5wYRUS9Ri8+EWh9OTz10hOH6KublmbI5yZYGvqzINmr8Wn8CEi5'
        b'xyVHGTrEZCRFEnnQM1IwHfbMhqSjjwxPTKQ9joiOSZao2dUsZZ4IMljMNzsBD39mO2tp6LkruRrL5mD4ZOLC46Beab/PC+6VtBVhE/F0K2vTH77ifSYhCJME+hva2dpb'
        b'WHO/Z5CUISaMipZulbQtIn2eSp4da3wsOiY8IzE9Tcoiq209c8f3pBlyv7JIhacGtw64SCiTTSWFDAX66WvArnV4Rl0i8NbjmT1+XDKuBunAuTSbVJEl5AiEyQKYw8oI'
        b'7hstGElRzrwiNIMGgRCLBNgaQzpYyCfq1kIHzDOvmRAX2B3sFUJXGMEHHESyCbKi907yaMjY0sIYi6xMPX1PwrSOBwwFpeBk+il2qCwSwD1TxYMsfJTzNgQYXF53lu7p'
        b'i9VYY7ruFDzyogIZ9xPQz4GkCTtVgb4+Kd0TYYlO5zcJuGNsbL1gyHwBklNsXIT6k8Z89J65iYWXrOCwmRw2Y7cm78jrDscWM6yREwg1CVlhK7QpQBFfcttQTqCScpdV'
        b'rDbPs93DFwKR20QYxViZK489EavMf5jvRKAg5XUZVjIk29iSzzw2w36sw25SRdcslQXK0AzjXGko7o0gUwWBxr7rrE6zyhZVd0EGiwrxxUZWPN3CyzfQg/P4etIMKtJp'
        b'Kgxarh7L03ce5l4+lp4WpnICLDVRuYI1jhnMHY7tapC7ik6hEeqknp4yEwJIMBjksXpgSw8uKEI3zBx3M1HgNtVVD1rYOaNH3OOUbRjAVm42cbsTuJRtHD4kYCnbuGjC'
        b'UYnxAVkuXTvdWZqwDR12XE504FGjNdnagqAzXK72Qyjh131mbzDLltaXX82XloFWvmh+I7shm0uYliZLB+AYy5fGoniu6S04FWYmyXaswruShOlKeJCxh73/CBuw4KmM'
        b'6bE0LqGRz5guhnITZW4g53DEnq35FeiXJv0fxD7Ok+uF82arcZ82hnzk59aT/CBzYApz1kV27oF2dZbzP3CMW7HUPUks5f+Qu4DP+M/EBm7FYi5COedsgjuQz532a8My'
        b'943/fqE03V9wYyuf7S/PJfv7El32SrL9pZn+1lDNkv2xxoVPQV/C8kNcKKkkjjQMZnaKQ1yPc6UAjuNdbFyNUiV8fYePVHXDHv52iGbXs4/DM0QCNegmtNshvrCVT+iP'
        b'h4Y9Ug8AFu2R1AJQC+ILJ9y5DE0stCSAoDNRTK04WnjINZR70V/OMZAso6rgE+y4vQ0b5SyE0HYhkMvYP3iVmEnnA3mWhK92/jZfJgeHYNaW5lrrL2MPrQKRigBXDmGv'
        b'iRJ32cVuLMT5NLXUDJxQwQl1KMG5dCG7zgLaEsSeF7GMy5mHGppv1frH0nB4I05nMN9Gnxjv40wI/+h97IQ7q49iFxbQ41fTryimqqrJCYzFMngn+Rh/i0FjGr03lYHT'
        b'aVdUrkC5emqGWKAtCzUG4gPYgU2cFHOBBmhJu5KhxHWrjjM0liJFang6g73DxsEG4XRRTvZGMF+rvg7afFffkD6g7R4RLXZhBRXYtIOtoJwe2XiJf2h1eFthTGY3DMM0'
        b'9xTZWLlrGkpPxWl2X8Ugdh0XO+A45PD99dEnY6vPXSV5LCfQkBOpeuGYPA7zEZ3DstiljLPpNBwVRVWC9Kq3LKBRBFMx6RzBONJCTdHOnjjBb+wuWVwQQjV0wgBHsW7Q'
        b'FxhIAjwQy7EuEMpliGRG7dlFk7N7sJDr4ygWRz/RBXZmUBeHoZmnhEKYckjDWXVYCaSvRdgnNCWS5+Kmjqawe1FIQHpbkWCbuuUfzFRKgMQEN2eisszTB0tY3bU7wYpp'
        b'ew9ytnOgupY3u+dT6CDAHi+8B8vwiK8uUbQjCKc8SGh4WxCP+ckINKFV9ZQY6o+HcBL7Udomwb5jPrICjTADoaMjL8ZHRaaCIH159uGO+zL6Av56CMHnTpIfjJ1NZHib'
        b'/c4OKIdh9lOv5zXBNZjHHO5qgy04CHdhmFSH74FsQTYUXuAvTZqCFRjiLjeYdsgSZOGEDHcD0YmLQuTuWKqIjhfEG++JV09QkElLJCVzw33r5YBDSf+fs8b9CwEfhnbd'
        b'rvl4JfGVLw64vb3wqqbWHmeDl37+koKxs4bx6ZcnJzTCLvzwLeH5KvtjJYaxr54M6PFqmvN2CFZS+8l3rh86dMh2sT3wyki0Zdjy+U099yNKv5VeaHToQGrmjY/HL30o'
        b'bi41E/7XGxe3/2Di4rf3qZWkbflVuuX8ob4PDVpjF/RbQ//21tE//17tr2lfRJ+t6Ro6F/jzn/7+kmm+Wt0Hhq6fBfzK6Nc/uW6gFj7s/NrZxh8W229MDVIOP/FvVzaY'
        b'nSz9gX+CVk/tkPz7D1479pN3vLNd+9PdWvUtCt//q7ltyrsTFRnur6RZZ+p2fdT54aPR+dIsJ/9fTqan1/R/vyY1QfgtZeOALXNbUoajgz472nLnUHDSzJ13R34wrfHO'
        b'VZ/F/i1RZ/5DPkzjsrm21Y8+evNs+K8XZ5pmNv8g6exS9K/trH7yxUd/ftPv+FGLzroTXh/tCpp867+/fSEos7kses6+9Nu3fpuQF/zno2oKPlE39Zb/lDW6cO6a46uv'
        b'/rfcfY19b5veME5p/90/f/vo5y0NGZf/ubwp0C7Y/L/+kHHup4vRfzv7/mk1y19u3/Pwll69MHt36bk33qzb8p85pjML4v809jyW1By4MUG+pOT1hQcPg90ccv4ZKP/9'
        b'JN93c9Us/xx0760fuv7hwC8mR/NiLGtd03b+xaDR5J/+rx96d/TBRGT0SMRU4S/aKy1P4KhAbfjmht9b/uZKwFJ0F/xN0OII/6xyd/3w5pEPsEVt1nJk68Dd7u8kbX64'
        b'c8vcR+G2pT+43uMg96Py7ES7oU/P/O3YH8cvvPHpK3s+/37gz5pG7xsspH+RaGDZ+uGSocuvX7v+xzmzvzhrX4uxcTrwo5deSTb5/HM9Y7O/Hf6xgokld7CiZXDcbP3Z'
        b'sZYnlriJoWPnYb44ads5nONgAyxd5WADgcQB7uR503aRt/Q025+rBaOJhWbqYiCIA6Ncyp12NlY+7fdxgEaFHZLLAc7d2istQSOA5S1c2Bs04AjXgwhnEqTxWo+DtdL1'
        b'xFCJi0e58UXvxxpS4bDs4SNxHEEFTPOhcY8gDyakpUyx4RIXTKbpwrmlLkEFTj3TaXQywMM0jfcaVcFigrSqWbGQJEAyK2qmC5Oc1wgqnZXN/HxJm41juZxAZp8QBlVw'
        b'ho8IbLTGdhYex/xJGTjAuZSw6nw6fwPYTCbvjIIBqF0ta+aNeVy7mdgbvlqd9RAWsuqssCzPHWdZHIcybzMYo+HKsaIRo3LXRLtwGIe5hjOx9caaWrVWWCzgatWeuMUP'
        b'6iEWxpp5mBvRD9ITONJci9yXrrLeq6GANN0HfDigSSD/Zhmt6z1W+txKHlsUyVroEgZjbibvPZvHKawguHoO26U5LvFwl9tBu1RoY7fQEoGU0mr4mpOit8KWA2Ks2wJ1'
        b'fIINoQ3s8H4cXuu/hz+jewC5XO0RfOADAxzcugR9HNrCZltuNTIPUd8Ed8niGXoMeGWxj69ZsqwrxwFbAzspsNVK5Ct+lFthwVpka2bGkK0eLko2Dwowj0HbaLy/im3d'
        b'FDiHZPwmopu1wBY6NRmwNcMWvlLHNLZoSZFt3WUJsJ2AxvRdDEvh0KEnYa3o4BpUW4ZtXDe2BJfbWTN8/Af1c0APc8TJWO/NTe4mVsmycrlW/hYiwbV0oktTR00udMQe'
        b'OgQ8wrGGeR7kXMEZVRwX2sAdoTl2ySrui+evzoZ5RW/pvkBzGqHjZhGUxAVyHHJCQH3x1f6g2MoTRo2Fgs27odJNBu7vxSaexfJksZ+rJ7ifOMcyUyCPnSKFs3pctRkc'
        b'M87i1CKUwCIpxqNGXLunIQemJdVKJGVVtXdiDTaLscIX5jmyCYc7p/hHLH2xhBA6dQ2LQmwkA8PJmk/7uoPtp7ln/M1J3dOOiAR6+2WOBzpZb+XDRYsyNPg2VgtbakDv'
        b'49qWiep8O4Vnlblbokr4aikGmKMM5SJClJPb+CKEZZdgmHNwF5uLBPT5kJyfyADGTTlS2gT9RqtxslyQbNZhFiYrTOa+Tt1MGGdKPVMa+LsQqYiDIhg9bsOtnycJu4e0'
        b'AxYmxhZCL5gXKMaKYDJMYKL+r2cUPfbu/i9e+bz23Ds8KmrduffvGHz6Zg5vOxXuymU57iYNaalkPpSUFUTWF2qJ1FaDTRVEIqEuu5xZEmRKP4nkhOv+fC6jLCNc9+dz'
        b'mU/ltilw7fF3f/CeagX6X4WrDiPDLnz+k5yKnJAVX9bgxqImVBNpCdU45zt/J8gmrtaLGhfwqiYUceNU42rLPHXquGZZJO55Rd7Hvur8Tj3G/O6rbu/U4+td9v9aAWx5'
        b'vp/HDXM9cp1ZrvbNufs96acSZUl6yzdy9+cIPrf8soPXNUtgIn5PQXre+TgvL1JG8Pg/OcEaZxeLSOa8+LyXX1Hi5Rdyfn7m5RcVahZqFYoLtWO0JT5+mSK5PMFN2Wwl'
        b'dhor8fHLcj5+mVuya3z8gaJn+PiDUyShtetd/JyzO1zirF09sH2+41z6xPpcnHSJ33lNE+YS93NkeNIzfZIR7HjBkLtKh/kPn3+Y8CJ+dnZy8cxeTaXDMzXk8m04l6h0'
        b'HLyDmx8SO62goSfxTuVn+7gNXZOjom3tDSPCUzmnLD/h1OiU1Oi0aK7tb3YQzS2g5EjiyVI9zzpLoOafXVpC4qmW+umZa/yrXLnf1HH77Ltttvlxvr4TVq7ej+/TPvkl'
        b'EV0VJorYSVjnAeQZcrazeQyOrPGQnvRgR9lY5B+4zk0KecnZ2K9IKKPOi7NhtbFunxm2YYX0CFsHGjgr+L9DlAX0QFyaXph5/MHb/HUkdretA1W5y0guJ5wSCt45lHGc'
        b'PrWONjSDAQaai7AykHk1w7Hf14crHH36qYDa9Xa8OFgV+1iKM2c4JwTuxSkh9GADmc4C34u4zGeUw7W/CjREAv3x1B+lh5zYEslb4j9scg7ivn53y1nB+wLBXuf9/5n9'
        b'eYZIhv/arcuZ+7Z+c4Lwe/Tywq6wQ04ZhgLO5o47b2QrY7hHILAR2LCrNLk7Y6JgEu6vdVfTiEt2WXj5Yi1z0BI49JR4wLkrfrxPeniZe0muNpjDSlUvNbMMFgwahYsE'
        b'P9cFFMBdePQlwXmm50yEnIvFA0bC1leY17LBPK7APHaK+Qqg09iVvjZ1fRnrmRMzHFu43jFXQWN955iHFWv8xcar70IuPFK8CVXe3EJFOvA3HP1GNsz8jDhA4vhwTuCX'
        b'MW/jKcG0QGDofPn1sB+atu1KlWd6gjm/TWT5m7MXcN4YhmkKdQLBNcE1QjJL/E3bxVgL0wT8NJ0EAoJ9Mj78zdfjkGdkJg/5HiypLevsae7hVBzJwlIBDhGjxAvioc+K'
        b'92W2HMI+Bm+JdkrJtPKBZjshEPVDAe/bysMhaF/j7cw4ydfJvAR3eVdqHjbuXC1C6guznFs7F8vj41UzhWntpBL7zsserjqcpu2iUtD74+XK5d+/a9+goZ0wNL1X515Q'
        b'+q7jAVED+47JqUR+t+dg//fszu/UE+qZGP/5H0pOd9prHN7DrNm3fnVz13LN9y4VGSe99Osv8raXv9Hxyjbj1/802hgn/8P9f/Y26a2OTl5Ut6nue+WCbcxIzBFv7Qtd'
        b'f3D63eZ3b37fL+bTgOKdvbdmhPoRbg6Fk+WKWeLffKB8/mWLvZ9d+evFlL/+oSrwyKlw85rusB/+W03J7bfe+0lTWF63TVTia5+0rgSMd5f8Wnb6V2f3bzP//tCh5oF/'
        b'jCz2mizlJcV3+bw9dTizLvPds5k/8Wk2vHjz/Lfvff+L+z/6oipt7Hu9Aftfr0j6hfufapMW9P/+l4NvKWe99m//kai6rJhfdjX6j2NR/VE7/5Hyo1blofgv4tLbbbIs'
        b'P46Sdfh4LuDX1Qkfpuf03DSw+t7fq4+3Fr9TIefyi/MpP7qU/s/AjsKcsit+/R+r6ua+cfRbG5Z037589PX9y+/NL3+c88Y7laOm2Rt6U5bDan9170H88Qfb0r5XPBHu'
        b'9IG+xc9vp3fdsjzlnHwq5dXp81u73pkedvj9ux+srAgGPq3/ovlDE10+NGQZiiFHWpNTfiuzWbX5G/68oNx7TfZaFEwxi/WANX8Jyj2/S2s8D94wJA060YQ53jzsMLlt'
        b'dk6ZmHS1+MJhfR7xz2M7dvJRdDIwgg3MoiVqzOE9IvOOZL9wyWsyZCfeYz4HuVN81H4ZPoQBFk+KpVrrC3lKAkrbcYWLV91w4zZ/mSLZ/tevsLsUk2M4c8QGJ3Beepti'
        b'4ZnV2xQxB/hYlSSsMzOT3OwiQ/Yad2Fimy+fupaD5ecfX/yiiI9wkV384gF8zp4uzavKjMbDTU3xsmiLCKpgyoU3s2u1t5s53LAw9lgtHl+eya0lLt30fNKIh9FDVmTE'
        b'u2tyoz5ooc/MaRjw4d00MAozAnU78XlFqOHCdA7uhz7OGMNKXxKipCvM5Mika5HJwHwSwn1a3PgO4BJbOqjOlNxBKWcgkonDCj5Pbhlajj5hN2LB9p1kNsKQLm/ylcN9'
        b'KH3ScGRWYyNRUasDNvImX3cA9b/GdHRR5I1HJ2EU145+lIeZn+/RdbbjY8ORBEkVTyeDpkKp8SZQNIRaZrzhABb/i5Bd+3/RXnvCaFNZG1rAWW1DTAt8M6vttsBShbOe'
        b'lCT3IypI7CR97voa+kRM34jYTxqS2xL5f9mlN+zCG1ZHU4mztKS2nQZnWalw1+GwtCTe9lLi/tbl+tHi/s7e/GSGwZr5SMwtOd7Q8Vo1fpjFsca+0vifXl8TmTWdWa72'
        b'yBlZ/szoUJFeP/DNjCwys/auNbO+bO7SkC4bNhBb0TNMLAZNOVjKMr34NAtJLXoRZ2aJmaEVo7JqVMl8LaPK5VnBrlKj6nFB+tXYVS7k9X84NJt/R1rQhX/vGcUXLQ1d'
        b'+ZgYbijPifXhIrmZ5UWPegb6H7Tba80sncvh6SyiIy09NT4p9rlD4CvJPI5vebIEHv/9C6WFKPhlsHI3MAS9MPdENCsHPHEOcp8JPlnVajcOJO2AKsxl583hu3wfVy5y'
        b'gRa+tHx/mvb6okgwji3XQ3lYqqOmwx1mW0Q9Ps5mZ9mweCF+Z9q8MC2XHvrZ0YcWJS5KsFfn2C/933nvo/8UF72iYdUpn6KpcVaj2PKd8h+VzXkkJdwdi9n6m8F3DJ22'
        b'p+XaaZcYBV3f8hOVvvDKxG213pf1tMW/tG4T1+R/dvcVl7IDf+zKbPrt0Mnv/Kk3ZHHR7uhLn/4s8HZm+eh8yff/XD43uOxz6cey3mX/+Ic4adfO960rTGR5h+4QFkM9'
        b'DyL2ZUoc3zWkzzksmQvVsk9kn5CJ1HoTS6I5h2U0K2fPsAR04/ATEayhOMkpJ9Nb2C1VkTDru+rqJhVpD5M83lg4xXzzpZBrZSXPe9AvbV+XXvIvaY01Ql0tg+O3dWLd'
        b'70XE+m3BJmkqCn/trVS0MwGeveUJ8bO+1/XCd70sWiN8v1lBaJKs3Ps268UrJ1lPsjCdF5asxTvWStYvnxqrfpodn8L8MP+jFRKlxTQHn448TY2Mi8+UlNCRFG5dV7Tn'
        b'GaLTlXdvJF7j/CHxl1MSo5lHJzpq+3PFrGRSTxaQoY+/zt0fgmcKKhm/DLZHRjjGOd+JxaRCanbbM2KaIvQU4s/5xnd+qiniMrs7M77zSdirESEv/fDl6aoJj667JrKv'
        b'akXGxSRGmIcnxcRF+AT0SnJu++8rXPm82kSGQ8n+0IQVZlAL42uyzVxsOZ98KE4cltgNUAGN0soXOLODkwc3A2GSrALh0+HqB9XSWXgIlLngCE4xLDyBZewqRN6B4+l7'
        b'RfK0jpk3DMvDeDy0f+VVYhrh/N5KiSuNY9eDL8au9oxZV2tSrrpfn+hhfdHxgPUMub4Y4+MnOB4Lop+aVCT313xjHssRfLwuO/SrxslqKMj6+QW5+ZmI/Pj/Nb6i0tvj'
        b'ChIshZVLbuPSibhYds7DzSEwTlhws+GXYuP/NuL+mqI79QD9qKYsAWUKIhllJaHutieLtmloqIgUhDrqCkI1Jfp+kwJ/yfk/ZUQCvkrCP3ff0hJaJmkJDbcpCLmwIlMv'
        b'h/WJ05exl+VOiwTGe2Qzd+JUxu+o50CsOkEWVM3hZGzZq0HG7RwubThgBzmR+EDOAYugGmoUyIa7j3e2qRJ4yIcOGIHaY8egSxlqoES4GR8RGnmkCk0OOE3MNRkOMzgY'
        b'pCoi7s/DB4cd4RFxJDxyZzGqWHIN5mAQRixvQLcPjDnewGXsl8dxAjVDsLifkE039sVesTHCJmvMwc4kaGO3X+Akttw4DKXQR1p9Qs/9iqO/LpTuxBzXmwm2ZD8uw1y8'
        b'IxZcct+0LXyTm4O37Bmb65b+0H3GwAJqccYRFrAfpqAqCYawmpqZ9YBZ+8umWGkTimWq2BeF49qEezqgBrtccRy7yCqtD3PF5hO2CVAeiaNy0AazWJAME1iNbYE4CuNX'
        b'L2MPPLoJS9gQBNUbsevSOayHngMbcMwDlvYCqwpVDRWax+BBIOTt8aYxzGLzQXhwE4dPQpOQ84rewXvQyioBxcEANkPX1a1iZbgH09huY07wYjbuoJIjzkBhpAHkuF+G'
        b'u1HUbIMvPDSJdEve5oYV8WTvt3hh3Rl9GM1ywXkyRu/j+GE5aDxpEkxTL4U6yFfaHYRT+tiJXfTbnC8UQmsIrUcdNJjj3MEjRod36Wjj5Cn6oPX6nnNm2IRDGtpYiFUw'
        b'E5RGn1arKe3AFXpjCCfgAQ1nXIANttGHsOk8tNjAQy1sV4vwhYrY9COYE4ANW6E01E4BV2DeQBvmE2FlMxTE0usjKWR5N1obYFfUjlNnD1thLZHCPPSlhRPV1WNzkMrG'
        b'89lJh67jtMGFLdDsB10bz+EDWp8GHFCgyUwTSTVjlzOWKUDhcVzcSztZD8P2NMsRGt8c5IXQDlRaOBFFlGTBpN5mLKH1WcIOtVtiFgDhvgu7d2WUiRiIxrorcD/AhdXw'
        b'2KsCD3Fqww1n2t3+45CzFVqx0UJlH47R/kxAm/g49EWG7zSBqjgZKDW8bQW9BzOy49Sxjqixi6z/TixLCTsNyxtCoNkZmmECeiAvHFtNscFsN87jIsyJYVwR723G2XDZ'
        b'FLwP08Fnrjphy83ARBjGFlqIZWOGIrEZR5O8D1ETbQbQgrknQqjtmhBoOACNUBhBvJcrsvfFGhi3oGcmcQCGbp67qa0Rcjtin3sstmpe26dJ0PUhKd0OIr9luLOf+KrY'
        b'fZvPrmu7idQqSUeOWBOVDxNpzmNRONYkwkOa03FcgmJ57D2CNdehPcPbJR5H92ChMVkTKzcOWN6GgouKgTCvv5VVGsN+zYMyybgShpMirMrSDT+Od2FKCcpueUAj5hq4'
        b'Q8UZyMH8KHVohwH/wGCbSK3dG3HQxV1JR8tyr+xm22BioPs+WBRI29uIQ/pQREIlJxz77Ggfl+AO5ouxxg+qccIQW/2wJASHYEpGk0ivRA+6gm+xu7NIMuWH2rC1hSIc'
        b'gemrWRuhfCv1OEo0NZBF5FCYranAQj9j8B4u3LDRYRdEw13anXGSXDMKsWpe2L6RzIKOs6dwmLguH+e2XYBlX29YgX7FXVCTRjKhDwrso3HqMhaHwLLlJubhO+8Pc5uJ'
        b'5IaxPABqvL00z1/FGeqvj0ih7RzkEgOtsFAWGxzW3hO4a4M/5NKSz5zB3kRavAF/mDTBeVlojNgFnXownPG2iEVWb80gejwMlYweadQLZjCdYY+t52Wo1Q68mxQOHVeU'
        b'iSsb9p8whz6NMG8YPAJlOEur9RAbNhMdPYISmtgkPPCEgnNE4fk7cNnjyJHD2OgF3VEaSphP9NpLFDUHd3dCs2EmEXCD6Ag8vCaws/TE2kvpZrRtU9BHSKkEFolxaojj'
        b'WiLOXUgi0dFlji0JtNhLAiKkEqLUIeiGerx3/jiJxBUzvdPpFy5CB4uN6sEqnDYmzqh22mGThWU6irCwll6JO+pPbKRxzFzFPAvF2zCdxEnLe2rXoInEZJ+Lj1329kgY'
        b'97t+Q1d80R1K9SA3hia2Qg30kVjKsztC1NsofxnKoT8UalVpgwcNVaH2IDZ5QEc6PZLLyppCO7aRSuqHHHUR5h0mAdK7QR7mDuKi/m4ihUlYtMFHOlexO2nDNZm4RMyB'
        b'OuLWArynTgvVQ9Prw4cwdYL2sksTS85siSNKy8MJZ+ihJX94fg8pprEzWQZEu52XD2NVGKmvBhMYvErsUGZJW9HlYkMSrphoktTm+X2X9mO1cQIO3Dyqlk0DzIMcouMu'
        b'mLI2NI4KhykSNnMqOliLi5ingkVu0GYTRPQAnddoAMVYaQwz0AnDUJmNXfKbd9EiL2GP2xkreIStSm6mNOECEo8dpLNbjsGUe2wAbeQU3Ek7Q9vZRNqwHZaysTQTGi/I'
        b'R2P9KSg+HONuyan0Su90UjYFGSQUquixekd3vRBsgJZLUCLK1IdWIm9aRCJvaDubQANdIbPfKNnLDYuTVLE6+rT8los4ugkaGHFZEUN3uWnGns54h8g6lt31RGI2iUMX'
        b'D/GBGc4Kj28Ngw55bApQEsIEC/6tII5phKp0mBSQqN21AXOsaYEbDa7jmDwsQk+0uzE0u8KwNmmC5o30eIUatspfNkggomlWJ05stDHBR8GWHtBy8jreM4Ayr60HSAnM'
        b'KdHaPMJS+RMwGMZ4JVyYcp5hoftJ+ACXLpwmWcGE7wgJAYIfyXbQou1sFqCFD85AddgxuHMcFjWww/32OVqVjgPXtaEs0OcMDBrh9O0trmEkNIZoP4Yv05IMQ8u5a0Ks'
        b'd7OFhaC919VcMRdaoPFIJOnkO7TJXfqatNQF2COGFU2sCdbT2ERKr0QHqi74hAcR4y7bnnRIJBauDYFaS8jz0bHSwYFEGHEm1itKgHu78Y6rEHNkT8Bi1FGoc4uHqSN+'
        b'sARFR+1dj9/ahE1E+yQSe6m/QsFlEv9dOCEHHcQExbrELJO0VJXYagPLULaReLTVCJZu4uyVI0SzLFatAusdr2CXC8mTnKiTWVDgnkz033ET6m9uIKqaibqGg7H62Ejy'
        b'r5OERMkhLD+taYdE7lXY406QiAi61/AAjeE+/dTtfCDLXYMU4rFNMBVIVDgH09f2Eccv45ArltGy5ZO6az+wlaGxVCiLMdzDyBCrdZw4SdBFw8yBtnioj9DMzmR5FCRR'
        b'iKsaoCaeRjNIYCBPBBUZtPBlG6/T9FpIdw6TykwLgU5LbMMefX/VQNIR/Qm62BmNdZ60v33XHHHpPNwPo0GOHYEx4uIie7iLjM2XsT6YGim8GJfJNBDmXt6IUykkXiYx'
        b'f5fbWSUc32ztdnIL/TqdUc3wQzftby5RNk1jFUGY4bzwMlYQgjh80Azm9sJ4pvIee/lUlsXhdgprjtJ0oMOFNnmZ+p5KpYWaZUIoZAcU2GKedTjcp85LYDzl+mGVrd6w'
        b'jA8isJ2eGSP50XB7G+SYnaIdn5c5SJKwHhZM7Zxw+AIBtDpciCZwWUE6bIgU9AySXMu7bYH3tIhui45egA4vrA9wJs1aFe0MTcGmBDl6YMmBeqsgMNIBD9WJt+9DpwYO'
        b'ekCFdRbWqPlui71Mwi5Xnjik7bpSKIwbORzz0T+sSkQ2AnVqFltkaNXuK2nZ4/S23QpiN7yznRYyx4gWpldzMyn4Cmpz9DzmXYB7LkCi6QgpQZJOBBBwMRRbse3QFZJY'
        b'ddBPuqSHcP447ZTwhMUpKDVKIiXdAiP+mHcWu847QImPuS+y2N5i14TN/u4nGYQpuXAL+iJM8E4k5GhfN8QG0lbV53A2lain/iQOh2GRxV5oEBGptftgoQsR2AqLUo69'
        b'QBZJFYnu4o36tMTTYVh7CAuhPfkgLf2ADRQcIbrpwWrrMzoxdvb+EdAThvPJ51nE6iF1JSPbAzobbU1IqE+rYLH2Mb89pAtXjKA1mFqtUSXSenQZSgJOEZcsnoeO3dCn'
        b'E4UTSdRhC03z/kXihd5z0RtI/NTAqCU8UIaRBHhAbTTEsmv/Ji+kXNRzgqFEem4UmmJIRjSJE2hgOYFE9dO2UHkYlveQwl3Au7d18JEgkeXB1dtGZbxLVLkPuvcxmsxN'
        b'4khymUgyC4ejceCaAjuL177OaoPs3kLwdtpgrxbWahCOPB2Q7QFVt7cZXc+AgnD9E6EqAaTAu9kfyNtPgr+eJAm9dphhphsaqjCSRTu7iO2nnJRJWc7CinoY9mJTAinb'
        b'flnMycC6oGhYvp5EX7VEXCAkM8aBByDwsATL8UT7UxH6mEsf56duw15jIo0u4p7hoCSsvmFIMqKV4d04GkTRRYfL+sr0VjXJj3paj1LfM4T0hm4G3jwdl7VDxQ8JsnZj'
        b'7w4S3/3nj2Sp0QqXAmPfKphPSjmiBbPq6cQouakEKqpC/GwVd+F4hB/egXoye2EW7srjkGo0Fp1kd4fSx4Up0KxOhspdaMvCyVCi1nErFTMvElJN8RpuCdeOkOnUtYW4'
        b'9AGJnNLNxjK0nnV7CW5W6enAvSTDbceJXUe24II7Sa9ysk6mSSkvJrFge6y5YoR9O0luDOHdm9BsbEFCcF6eOsvDPlv3aNus7edjiNFziSHyMogXmpWgxhorLtlii48R'
        b'scOUtmZaBHczwdBZHLpAnNOznZ1wHiDUMmcLhTifkgTd6WSDF5GtrLdXh4RmgxNJ+qlDO2nYVXFQTrBBFgeCSV8WEbHWHrmEM8EbMV8G7uGDaOr3PlFbs2Dn1cMpZ9N0'
        b'T9AeT+wwJY65D9VR6dB6JAtKdmKx7HksTYAmR3p2ksV8EN8VnyJVUUrYpFXHRw3avXbf9icKHcGx7DOJhBUbAo8cP8Ass2F76HVJNT0Pc0RWlb4wcT1eJ4ZkUJM6Efi0'
        b'BXafvOGOtW6mRBFjejsw18onIRgrbAUmclzgyEF5aPb2NCMdKBBaCbDEQMgn3VRg+SVvLNcL5xOE7iXYc9Eq9gwoepMcjhAJhM4CbPKBYj5BaZ6GWuJtgeVQLycQOtFX'
        b'hKz6+Vtuu6B3I3PZ4904oUDoJcAW53j+m2q4o4Kl5gdwXMgFUrVhjmmGu1ggIGjLTrRJJ5XTWJqdVWjRH9xS2nZOEeoPudgFqIdrk3aqtiRq6KKFqmOQfTfe9XTzhYKE'
        b'I7omJG7msHdjNqmoTmjz1HA5RxK8ClojsJIwCzExttsxnwuZ3tVZlhmuMKTLkN5N6I0Ox0Jl6EwNJ66phZUjkHP6JNb50VbS98SP+cfpxx7oF5CMLQzWIgzXYkU7dt/m'
        b'7C4ivNwtZBBMmJ6hdisF/tRnfjSJ1Qekhmtpq8nEib8BBZakYquDoGo32QqTRBBnCcNU72b1jaHGnuyk/PRQX3jkTdTew/JQia4mDchmyiO7rMje5AYU2hKAWyRBMU4a'
        b'oQPGtxMgHoCmg9EHM8VYKR+tjo0el2DQDudTzbbhwkUcPuu5AQblb2RE+6aGkhSthh5F5jaARoONJDUKCWl1kYohK+X8WWqrjNaz/oxOAvHsAg2haj9Nte/wJqXTKtgW'
        b'GcYZXs1izLMhQyaHVmUUSZCu2ECZGMfPmPrbYH4IybXOQzi+m/im39YMWJLGIFQdIkxUSfPJSdXLkCHlVJVGc+iB5WPnCFDWQokptMnjSDxWeUCdE3YEk01VRsbLsvwG'
        b'LA3bHmniuhlHFKAuDOpSiU+WTdQycDAyNRX76E/NTVUabrHdqRAyIUdJGlfb4qSr+w3NmCiYMVaFWTVs9yC+unMAR608ibUHoQCZY6dYnez3acjdBK2hJAag3snjrN+5'
        b'1NNn9YgEi0iTL+gdxHupVrYkJyYzxSQeemHEQhdWMuJw+ACZA1Wm2tisxyQ5abzCvbeJSWf2Ez8UM1eUiV8MaVSYs4KWdCKoQpg7B4VJpMR7YOgYse+o920YDSWTr422'
        b'dNTLgfO+PBSTmmk/F0vmVC9UHtDbfMuMsOe0HzMjsDoGlrBrL/21gsuGulAfnWaerk+Qa/gIzl9UxVxVfCiEtou3z2HT8YxBhqtyCVD3POmYISk6dsTQWT0TR3TlNl3F'
        b'zihijdwIkssTJ85hiZeOrgsZLivQkAqtxsQzBco6smdDfQJI+FTZbiLaqYcHG7HPWt97uyNMXSejoDBE398i0kWeNNv8yVOck2bSfxv10wy1drQqD5VoFpNJJJe6SKks'
        b'x+FsBsyakKIudTQj3ujD1iT6pTJzHzSTZiMBX8VotRsmTGFsbzIh/jYHnIw6Rytd4HtKjwFOJEnde1pImO8hjTDXgBhowp2UXJuMAfabkeydwm7tUzCwgwRrBbQ4p/oQ'
        b'2G6LJcSZ58zk6wTk3kwklL/ZmcBC90Z15trywf5sLVclGLp8gURxGe8JSIskFqi6ZETDIo2GnbdIFCwYMLBKhi70+14UJGDh0USSOa0Xj8aSapjC1mgaYU06Cb88eoOg'
        b'Od6PjIIHiScO4LSeBjzaeZaooVEHe10s2YqY4qBeNC7EE+EwsD9EBsTDVFy+KOuogU2brbHGP4VkWpk2dmmREVZ7ndBUDqxcIcQz7QSDmv7GTra7SPt2YN0ZBex0T6ZF'
        b'bzHek7HVJF73hLuWJnZo385wUIWCoyI/IvohosBi6LvF0lQzTnlA6TlWE9QM5nWiiS8fEmPM3jx9mZRlElSIcYJ+HyFxvBCeSdK29fCNEOw9Y0FiqRmHTWDp6EUY3Wbk'
        b'SVKhlm0wbcIjEmxNJB1GNWkay7hy64QPNdqzH2oub3D3p74XN9N6LLnCvAuJ4MJQ2R1O6cfICvgBc9r0w/ghuB+Ipav27WnqvRwa9m1jJu6ZAGUhzGhhkR88kLOA0XNy'
        b'ujCIJAOn9xMVPLA/hctQYhlvT/RZzXlNhnZYkBhjXromTXPIJ6lGBFoA42Qd4KOr/hYmtF3D+PCICwwaQJO6wSZa/DKYjiJ27XZyFMDgRhIsQ0bQZI8520nYTcJICLYH'
        b'Q4vNGZI7hZ7QGnWGVMKDUwygdGHnmdQ9suI4R6y3wt4sLLaEyZ1BmJe0F3oSjpJa6KEZ9xN0bXUjiQMLPlhifobm3GJK/HzXYvvpOOw9sOFsKj7yI2KrJ9WRv09HAdoT'
        b'kmCcxFcb9TDuJ088sJLiT5Z7NdFLGfRk06RJWW3CPiuoyyB10uCXQNRElkuDuWoS5CsZOuCofTw2eulehocwmIEt9rDokooNtHaVOH5qK6wECQ7iXVUFXBHTKAt8N8CC'
        b'LPOOdNtDX6yuB9Qf37zJnqyuEpoSjh6i/avbQZuTTyybS1CSGPoKGaEj2rTuTRGRjHVi4oxJsJaLzrvEXlGBmXPYl+DvFx9zkdDqpBqNopk07rASTnpDaSQ0nDLTA7Iz'
        b'7mB5gko4jgRBpbZz2IXr2Oblu8Uaq/fixJa484RcRAy5khDKJ2O6HR/6ZN2gBSiN0CDt1YmPtsoYQb12ABZEhrhfPOrrRixedhjr0g5G4cIOEkhjtKulZB3KhZJ0GFE+'
        b'Y8BJGCa579FaNkbugwmc2WFCrNuI3deI4ypg3JiMoFJNeVKQQykhG1gIYxQun7hC21OOhA+qFGFW65AlibS2a9q31fcQezWRvHlkjkWh0HbgMsxuh+oMFzFL8+5IXUfZ'
        b'ZN3OikV6OIDVzuqp0KMjl7CHhO59mssEycN6a6FXkCezoCJxPhKnVImxZmjqneaH1LDK4OwWGSLxZlLfZYTgR7Jpsev2BSkGw5gdNocQdTeTGlxUZkY5DBsE02qTXQ0V'
        b'upgf6MaQjzY1Nhq6DXptcPS4KRKc8dpCC1S6A9ott7H9dYSWDbQyLWmkdvqjYSLEgOi8WRSwbzN0b7SHnAgotiLwe5ik4bZgk80kJ2riME8RJqJTb5PmyoPpM3akVKai'
        b'mQgvlU8/YQuDKgdohSuxST+U1mhBC7tiN+CYgnG2i+MVPbh/AB743CCa6mV3qWPTRpxN98JBLQI6laRFl+JIE2QruabSFrZRIzU7DqZDzyEZaxx12gUDR5SwNR1HNGIu'
        b'6EOfpsYVqN2AZd6x1FAu3DOXt/Gl7SScQcsyL2Pom+J8ICABx3aQZBgkJmoN24ErrDJdA9z3dDksIM4oIbYk/E2SqwZmlWOwcD+pZ1akzRXGNykKSRTMhZ4nqddLWzJP'
        b'reZrbjhNWrwcuhXgbhwU2OOgBYn/oluZUHPwPDIneZcApi4e2kwCZREK4vcQo/XrQ6cFcXkTMcQ4mdWtYYob9+OSHjQEHfROcSftOQADOCpDr9yBKUMdezI5uqHPBYZk'
        b'DYiRWmHFaMNGQrLlplh1A6vY0hRfhUlxyu5D9Gm1I3TtOY0LpCaxXnOX4y5sOwiN0SFEN0VYn0pqaTnrHD7Y5xgMeYnpJBfvWQrsoC88SyciglY9MQ6XoDwCxq8Qdq4m'
        b'9FZOqzXhQGI1f5c9mYQLWJjq4B1zmGRAEZZct6DFnVQRsqhyFYaLaSObotKybsK8P/3aDc0+ZKK30xZfS/HAsdOcWpzGJcdzR6DBmFQmGcDuh3Hai/DbA+UoawJyjWeI'
        b'N1bkIwit5ezw9cwQERfdhiE5xkW5RMyMjZZxyYwEcSPR5qw9TusT0A3BWqV4VxjehS2uVlAtJuXWocqeOKwRT9biw+uxHh46+wgL5HkF2xtiQXYywetl7HfhKhO2K+JD'
        b'O/lEUjrDQuwMxEWjm5BDll/dbjd15UCsj+JO1kaZo//2dbgHi8yn1Q0LATRJYhN2cQyZYtgLfR662HQtYM9ZK5pcHQ45Yu5trMAZA1KNReehPZjA1oyFXFyyjT6MeygR'
        b'34/Qg+U2tLIFicQDy+rYcQHyCQ6Mk2qpsMaqzfI0y15FCxy7EUcIsCAiC+4eJp1cAR1inNRXxJZT+m76RDAjxrIaW3DeKRiq1JwVSGQuYo47YZlhJtD24xjL6q7Dyr1q'
        b'0Scg/5y38cH0BCVc1jidvYcEPIHyI5dPQGUK1toEkknNYOiUfdwNoo/iPTCu6eBNPNypB4tKMBtyLdEUB4xIas1hC+RfxMUsJSw4Hkh8kU9GyQDJnGoyWLbTYjdsxfsq'
        b'SuIYPSw9mxB/IdQWm73VhMd16b1RqJaDGk094rdamEtQ8TSzwtmtzP1JajsHHm6COXZ212+whQy+sginwwTe2/bRWnTC2BaLJKj22UlcUUF2T1oGNO2jPSjwxBlHZYLv'
        b'S4QKWo9n62GXyi1ZmkGNGzRrK94ghquh36phxSwp7Bq0bSdzMk/roD/M6EOrxoHDKlfxjhfmG4TKY38Q1MRBG4HoWqwIOMNcptifwRxetO9LJHrHSUHkYY8lFt0K3U5K'
        b'mgDQKXr2vh9N5s5pnM22JFQGvcQutaSni5TPRGScJYZsB6ZICIz22NHcVm7Cva1YE02Qe+YKUcvoVX0iquGbWHgbikmME+64E8KOA2As4wPCSdkkqnNX+cCZeaYqT5MG'
        b'JgmW4GQYoL4Lq4gHTu+6Tl+3boyNVNTHno0Hd9H2ruBYLIzIe4RRL7MEkHpFdji7GVaw/0CCMk0pHzvSgR3/5p51hBoZqNcnUf7wKjZ5Q5eYfuyDxWjSNQO3SDJWEjvd'
        b'o82oVtqK3V4kSYdp7cuw5gauwJKjDhbbwZIFdu3yxdJEds7lyVxVUSdodfJ3k0wpVpHBoehNRPfT1wyJyRes/ZOJ4Hq0bWhsNXt1sX7nNhNs2X2cwALxhitRw7JOHM6o'
        b'YPOh7dirSlZj/nnIc8UFZxhWzCLxUkvgp45Ec7eASH6RBIWBBzQok3XQu1cdOl2socmWcEK+ftAGHNi5T04Oi066YrEy3nE9QRbxkiXhq0J7nFBPwRkrFW8b6LLFWhcH'
        b'Z1qUKWiWIa7vIVlfkB1mqMGStxZIECxAriHR+qiQUNntTGsit9oAyFfmqGIhlMT3yqXdmKtNEqEVC5Np4fqYJJjZS8ijNiYOug8SSTM/fC2W6OGUHVk11bFQJAddcYYw'
        b'IAMPjjjgLDPPMeckibBpn6uk0B/ZyhGu7oYyY8wzp7V5oAtdN6FBkyizaAc7TJa9IWcXG0Qt33NUw3rCDnJXGQDK096fRPYe4fk7JCSqoU8bm47pZbGoikBavGZYvJhp'
        b'BEMW8NANuk1koWk7gauWEBi8RAbPKHRbhHI1QxfsHJL3waLXnivYZQSNXtBntvc4TsmSUmnw3E5m7X2ctCYVN8i4pClQ65gtIexhS1wJ3kWyrSEgTC30ZtCmM0Q7RZiz'
        b'34f6aNx5eJvzTQHhy6JLOEhCcsRExFeLVfCOD2KVb6Rlb64Y8q4jsuFwiZVrEwiTFcwEjLgcTcTcdzjihAXe5mrsXmrhQQHtUR4ZF6y1MBgy9SYm3iEQCPcKWH2GLL4G'
        b'Vy5tDivMUAz1N2QEQld6ycOZS7iyhr7r3p6xVyUOMi0BDYx14iEDg97+pCSmaQQ29A2pkAW+wk29Ewt19YH8/fSSvQAr/YL4XojO7npjuSOMStxqNNEi6T0KPUHER6Um'
        b'JHboLX8BdpHg65O8xyAAlvo6YjvvXKvGwYu83y2fCUhvMwKTDRKXHPF3m4mQX6Ry6PT09iKR0kZtmgmw6BS0ct+kGh3hgmgHYEbikjuKd02Ebtx9O1zm2udHxVwk5l5d'
        b'r4h3gm8ITMTcx53Sj93Sb2SKwvniP6+GiiQfBu3/o5GTgAWZuXGtcalu8abZnwjTxklobdL1vVl72n+zi05+7NULg3Iqls7GfXkfL/9Zbft2xaoduenTJ+/cDfibzsve'
        b'uj//7BcmTjnbWqZ+Vld8rcj8wZ/b0laabL+1snTr/OI7SW9Yh50/95Pv/v1q48Zvvff2H10m3F59933x3S0/Pn2i95FHwPbmgKLRv2z669hocoOs+Morn8e3DrZMd/6t'
        b'8nrI3pM/1X+U3Zlk+kae5kMD08M/Nw3qvXf644obs2NHbxQ82HHD7UHE2xavzBYnfO/9Vx7GPKz2MnWfzZf51Wc/u3j4jRD//3DcmlOXve/EoObPzUZq43bVGn/h6zEx'
        b'Fnmh/+/7bEYuXfHrdfnTQNRb39F8e76jpmHfjMbZN70svvC8ZjLkWlNz5Vfhjq6bPy7YYrT7j7fe/vVH85Wd+OOr5t9Nf3dGu+/dnX8P2Kk4eW2wwboprG3jmeotP5r7'
        b'5M1ig8HWSIeC2PlPPhPZe5/tcXUQ21l1t055vP7trsTq92c+eSs/qebHRzx/8JeBh0M5Bw5OGQXbvNx6+KPo08lvbnj31vvbyov/+qb/g9DvXuhc0C1+a/SD7wRnf3b2'
        b's2DrqzWvbQv86A9vf2fqtQhBnkH0m9bLjRdnOn8/57XrVaegsy/39L2773riHuu7jq893Jxmvrvo3ltv/fOtTHGB9dHMXWHdL986pxXxjzcC/iHcaOm9bNrSnPxvxv/+'
        b'auXHM4U9rzthRxpWRBhoO/5Y5T+9Dt2/+HGtiUNa+m7rb/31RPnV7w1fs+23xkWTgRhrd8vSP4/IRzddd6yU/Uv5y+995/ap/ea+rck/+on30qbSkIg2o/t7DNKdIsf+'
        b'9PYW0zbXnYOv1Ia8fcNtcvL1kzYh/67kfua37guBId/a9IOJXN/E8L9uv7Pl0wj1vx58qXOscut3hg9W2H2/MPSqXMUXLcu2yr89l/fPz3+5MfjG0n6977e/+a6M37f/'
        b'puf/t5MPzX/v3/75nqzgX6zc+vD2Tw/IZQx9+KfQR0snFwucTZT40ixN0MFVBDwOLbxIqSDFP8rFuR6Homtra/NsCJBWZe6MT9/JXu4kA7lw7R00q6ls2Ospgw98rLls'
        b'qb2kWkqVU1UVL+GwKmn7UvXUDBVS0HNigUE2NTebwVdqzr/lzZ7iHrmKs1evqMoJ9J1x+pqYHdlASTqr/GcCBVCXlqlyJQPn1KEEytQVVJVwXD1TVmCiRhZqjgzp066T'
        b'6SwwdSupqjtPP2uIheqZUC7twldGDhZuw30uEyDA1R9KNJVX21TAfpGVCbZz7SX74EAalCtcoSGmkb4r5ttz2LuuOZyRg0daUMoN97JZ8Go1Oc5GeLrYCvOCP31Dm+3/'
        b'3YjT/+t/mRhwEvb/lb/4O7NDQxOTw6NCQ7kQ7DdZJK2ZSCQS7hP+n+KuPTaK44zv614++2KOh67YNWA3qX3nF3YIDqFpSMDGnM+u04DDq9vz3dpec4/17h4Yh5dqixCb'
        b'wyZGKIlIAsRAaohrbAhP0XSmoaoSNZVQRZhUVaKklDz+aCu1VUFpOt/s2aD+16oSWt3vdnfmZncee/t9u/P7fQXfCAKQ0byCU5R4p2gX6CJ6bF6v15VbkOvItXuzZs2U'
        b'hFn1vkKafydXDbIkNTAlW5QEWC/YScvifQ8uh32ywC+1JmxHBH4JfLdM77H71s5dlit6RG+uwJfu5IoEfrmVUiT4hRL6CVDcxZ2SWG6hlO2BZRd3XIJJ1nfs0/rhTiaa'
        b'cvejr56e8izqH0PF7078rrr/g+K+DUbeagw2BRuaKAADAKJScNe1e6NQzad7fNR0OrSAOjQD1DIehHBh6AU06OA83xK/Tf2IC2pV6Lpo5PEc17i/c1G6rlFclrvi5Hfr'
        b'Pvjw00qPr29opdDnKszvtY3PO33kI/d7Affmg1e+nHOzNr/vqd9eyx59986xliPe2fW3Rx4g/cf+9uDnX9f84ZfrL02Yb0urz6ZqFpkX4re66q4dvPLXGy38c/7P0PtL'
        b'qp5eeMkfPnEj9GhVrKv1pa4PKv80djzw0SgeyfrXnT/+euyLro6Jnxmvi8tO3vBf3z7fMRpdcOvlmzOfP4j/0fGXsjfLjeZLLa+srzhbkffNte7bW3qqDhQtuvn72Ar9'
        b'6Obzv9vwkm5/cp7oPDBe2ZeecVX7uLV/41e/6B3cLtU8seep/E98Mxq1fp/rN9o+94bCd2evO381J7F/QV3elluH3/lewZ/3lPckJ/1jL6be+fvVHUe1r92BX208+KFe'
        b'Mo/RpqjvcAAferoZDNimJkazdXBuNCHgN5/EkyxmJ8zRhOdNl4NNZfg0ZINZ6zPwZRHBa6kLrJzH8Fg5Ol5idQmQ/uGBD+0Sr1iAdnVbRHLq7PSC/mnIwdmlBl2AOcmj'
        b'jIwdzLbhgQrUh/dSI/WHHH7Dh9LsFrmZOru7A3hfMbCE9y5GozznKheoR3GOHpdJwI3Q//au5JRGl9TIo/Ea1GuxjPeqaJ8DHYIp92WZDB7cLzY+g0+wM1pN76NjaO/a'
        b'DNGckczPRRnlbDH12Sfw4R6r4FA9TpfUS5wXD4vUOXxtiSU0tkenzbWqtHFRNd6FL/OcA78o2CvwKSvswkV8hVbwIn41WFVNfx/MqJUtEB+jDvOwRRc/ufaJxA5Irw9Z'
        b'yR48Ji6ESfkWv/nVKur8716DByBS3SC1n5t5dAkddbC6z8HjaDCfug8DOB0q5ThpIY9ONRRZumAX0GFbBXorUIbTwJOP8+g87ZJh1qO4fw08QE5Ts4QW2+dsqg/RFpC4'
        b'vO0S+kkAjbFzexxPPDMXDQXhzGgTQFgId4mAh3zo55aE26SMDhX4jXvSs+oFNP5wJbNJOgvZk4cH8FkDvYDPafhMF7VLcjguDx/LL5Ic5RbXB10p/s730QHGSwpAURyo'
        b'PAv4qAcftioyEkDD67OmYrdaAnPt+Ay7+ePeJc1B9FYx7V4QD2Miik31KF3RWFYSf9jO1a1wbKvE56zeOgKepBuP4zPUZ6e2GN4PKq7pQEbKYICO7ckM6922LbWDxyMp'
        b'/FPWXvAKnyWW4T0V8zr9UyyjuSkJ7XajI1ZNTuP+Ztrc/SBm2ICHYwLnekigxQ6h8+wQS/FrhdThfjuwqqw0VFbOc9mzxaxH8EXrItuN97VQ5/f1IO2XYDktg15HJXZu'
        b'ZrUIL3hXskOoeLKYNtTzgZWlfjgGdAkeAmrHCYWF94qptYFV9Ao8TX22IKjoDc+fCi9UfP//5P9Pt4o598EyuRugV4N7ksfJ2PFOtsxiymjODCkT+F9gboAamTejT0Zz'
        b'ion/nks2tVRa9CpmNPiJGFMSeie9uRGbmdJiCpFiqmESKapGKCY1JUFEw9SJrXWrqRhEak0mY0RUEyaxtVHjin7p4US7QmxqQkuZRIx06ERM6lFib1NjpkI34mGNiD2q'
        b'RmxhI6KqROxQumkWWnyWaqgJwwwnIgqxa6nWmBoh2SssWmMovIn+OFvTFdNU27bK3fEYcTYkI5tqVXqSrtbqR5QEqE+RHNVIyqYaV2hBcY1ItT9YXktytLBuKDJNAoI3'
        b'mRFPRh9dbEXkkKNqu2oSRzgSUTTTIDmsYrKZpLZiop2Iz4YaiNvoUNtMWdH1pE5yUolIR1hNKFFZ6Y4QlywbCm0qWSaeRFJOtraljAgLkkRcUxu0OqkEyE/dNces9i7W'
        b'QRdY7wJIAGwG2ApgArQDJAE2AmwASAG0AqwFiAKARat3AIQBfgTQCaABrAF4lmnQAQADUe8BeI6x6QDWMcItAJyYHgfYBPBjgC0A6wFaWMlAuOuGtW0AbdP0QRhIrmnT'
        b'6p/r7jGtWNptZxsdKUqko5zkynJmPWOT356b2Z6vhSObQHsMaK2QpkQbS5yMCEgcshyOxWTZGrKMKgiUOGK3Apfqn8KeHVM28H/EOybOpbTfUzHlcWDRMQaeZJcE5/9+'
        b'6ayexaQF/w0Ftuj2'
    ))))
