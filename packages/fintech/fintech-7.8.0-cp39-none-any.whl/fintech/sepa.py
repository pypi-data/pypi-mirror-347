
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
        b'eJy0vQlAFEe6OF7dcwLDgIiK93jPADMg3keMKCAwXHJ4EOPMQA8wioBzeAVP1AERT+JtovG+EhWNZzSpymaz2Wze7r59e8xmj7zsZnPtJrvZXw53X/L/qrpnmOFS895f'
        b'pKmq7q76quqr76qvvn4fdfgng9+Z8OuaDhcBlaJKVMoJnMBvRqW8XXZMLsiOc86RgtyuaEArkMv0FG9XCooGbhNnV9n5Bo5DgrIIhVUZVA+WhBelF6TqltUKnmq7rrZC'
        b'566y6wpWu6tqa3QZjhq3vbxKV2crX2qrtJvCw4urHC7/s4K9wlFjd+kqPDXlbkdtjUtnqxF05dU2lwtK3bW6lbXOpbqVDneVjjZhCi8fE9SHePjVw28E7cdWuHiRl/Py'
        b'XplX7lV4lV6VV+0N84Z7I7wab6RX643yRnt7eWO8vb2x3j7evt5+3jhvf+8A70DvIO9g7xDvUK/OO8w73DvCO9I7yjvaO6ZCz0ZEvVbfKG9Aaw1rYur1DWg+qjc0IA6t'
        b'068zFAWlk2EcYUQqDbK88uCh5uA3BX57UzDlbLiLkCEqr1oN6YNTeCTX31AhZNW8lmtAnpFQOBefnEOaSVN+zlzSSFryDaQlq6TAqETPkC1j0uXkPt6tNMg8/Wmlgyeb'
        b'sxKz8J3VRtJEtucqkJZsk+VlWj2x9C7ZSrbR+wo0xySXc/j5hVM9Q+EG3olbYxNwUwR7KTeLtBiy5CiG7JXh2yay38B7BsJT4cZnzPiV6JRxcN9MduRDNVHDZNPIs/gI'
        b'u082qslBc/k0eCArV7yvJS/KxuKXBKhhEDwRhs/hTS56E5oh27l8fBSFZ/H4Mj440EPnEt/DN8mJCHI1ilx34SZyo45cW46b8S5yNioSoUEj5CrsJU0GzhNHn26Yuo40'
        b'52ST7TJE9k+RkXscPoyP18BtigxkOzlpMONL+ix8mGw3QtfJdtyUTyHDLUl5RoMSzUlX1Y8ibfACHb11uJVcIG0AW06+gtwnm5GiniMnw9bD/b60wueWk5MJ2cbEXKOJ'
        b'K0lEmj6y8DIX3BxMb14hl0YmZCbGk6Yc6Bq+QO6iCLKLJy+mkw3lXIfFNs6PAUcoooaiKfrfIqpX7zV4470J3kSv0WvyJnmTvWO9KRXjJPTlGsMAfXlAX46hL89QllvH'
        b'FwWlJfSt6oi+FPiBndDXIqLvxy4l0iAUXbdydXXagijECl9RyBB9cNc0d3WevFIsfMKuRtEIJR/zLM95aW61WLgjSo7gr+7z7FWaPYqn0DlUHQ7Fwyb2l/8zBs38vPdB'
        b'7lf8y2ONivWoOgxuXBp+gLusQrpkw7/GvOvUVk0Qi3+x4Iuo1ihO/3ndhOhvF8yZHY58yJNM8WU/vgmo0Eyak+bq9WRbUiYgBT5XrM/OJTsTTVnG7FwO1UTh4+S5sCdG'
        b'kKOeNHgpA58j211u54rlHhe5QS6Ta+QqeRlm+zppi1JrwrVhkRGwfhrx9pTk8fhIWcrEsRPG4Rv4shyw+akwcimCnPNk0uUTVm3Oyc7LMpBzuWayE5bydrINVkITaQGA'
        b'9InxJoMxAb+Ez+KLhfD+VbKf7CbPkl1kH9lLWucj1C85MqYvuRaCS3RggVqgfn7izYierEImzTXfCDO6VgZzzbO5lrH55dfJioLS0lxv7opUyTvNtTzPSZHA8e1rNbxr'
        b'CqRez3WabYtetbT99LXLu67sG6Z487xtwas3o9986tVru47vO97g4Fyq8kgy63Ri312ZybLKCJS9LXJyUR+Dwk1RCR+aB4PQDIOxE4bkFH4Z8GUKh69wpMVN+zVZviTB'
        b'BMPVlMihJfiyEu/gjXVkH7sHK/okvp1g1GcaeUS8U5X4EG+01boZeWjDuywJRtKSM1aBhuAmZSlHLpHWwW66lvH9EXgTac7ElxDi19rwbi5jArll4Hy83mCQOWlvgy48'
        b'XB70mV7hrF1jr9FViFzM5LLX2Wb4ZB6HQO8D7sO/2eFcDOdU+l8yyH1hNbZldhdwPLtPbnNWunwqi8XpqbFYfBEWS3m13VbjqbNYDHx7c5Cmy8FJJ9apoBdaH0VGF6Wi'
        b'6F40r+R4Tsmu/L95HmaKQ9/SHKPzT5OdkQmkJerJHA7x+AA3m1yMzCjnu0AbNrMzKNrwDHHkFfIA4sgeGXE68TiKH+GdEKd3HoOO7PGQS66xqhzoGTmH8JnR+LSnD52S'
        b'K/g2aTWTTQPhFmeA6ZyEN7M75AW8zwGE+UR5PtxRIHwdX5jOKsMnU7UE+EMEvZGOyLMl+I6HNku24JZJETPxDuCBXC+E7wwaLr6wA19HCbVTafFcRA7j7fieh2IScI69'
        b'+G4CuUdaTUrEPYXIGXwQN3li6IQMwM+RvWFj5kJ6Dcp1k5c8vSC5qBJIxV7lvIUIJaLEIrzbEMbaiCWt+OA0PhOfonBQUHbOEhu/vbLoGR7vmAXlp+A/eZHsZNBGZa7D'
        b'd5RJuAVu7If/+OxI1vEsO7lD7iifwTfgxg34D6RgvziKV9cDrbgjWwzwkaPwPxm/xF7R4HtANe7I0vBluPMK/E8kV1kjpXlj8J0osh2IETkG/1eT7aw8z0mOkBP8SrKN'
        b'Ck8ReB/ex7oHNO5ITpFsBDmP0Bg0pt96cS7OkmP4NNmrIhfJNaDgKHk+uSbeOTpCRvaayfNkv4rKFMiCrySJM/vK4hLSNjbTRdpWAEqSs9zI2gpGRUKIGR9MbwbApRLV'
        b'o6ej13L1XCNInU55PbebXy6nbIktLnY5x/t4U7KPKz/Hta9Vtmp84dOrHS53ee2yuhkLIP8FbcNDsR3EkFNJZkmKYbJAJkxZG1AhEA/Om/LIdgNQoZQU3GzGe0ibK4Jc'
        b'RPguuR0Bkop3guPW9Ld5JmG+zhlGtYzV4uTY2d+tjBhfoJdVvicf/Ju31If/a/CuA3vCRq777NVd77aOrn75+T9Vrhq/NfWsPOGXi+p+1Gfg1BfvmxqHZe8JO/1V0Tvv'
        b'jjz66i8/b72q/+1qsvm3PzOn7Vn8ojdik1L4+L9O/LSt5Mp//zL7fdMvh/Z/dvBXn/3mDz82f/HZHyY2Xro5cP3p7WPmNZuBjDJSeGGERoX3JZgMZFsiQkp8kR+H7w1w'
        b'D6Ed3oufJ7sAn8+C+EIas3LyFDDRV3hyFN/F59xU+IkiTfgW9gK3a04EAQ/ES+VifsRYfNo9DO4qcEMdae5P7gKrIttAdoOnL2YrUO/xMrKH3MHnWR3kCr7anzRXjRBp'
        b'uUTHp+ALnSiqQd6RxHaYuwh7TXmtYLdQGsuoq47OXqack3Nq+OG/VcrUkA6HtJaP5rSchovjnL2C6C7n8oXX1FpcoD5U2V1OKhk4KVHqDAvvpBjnjAmQW1pNVoDc3orp'
        b'ntyywb0/SG1WciHoJEcDyB75Snyv7CF0l7HrELr7f86ww0Th7FlTbzQSfS7nkLX+FX2kKHItXZSJdqFf1yqs1uzB8Skog5X2m9sL6VBmrqLOWn2yT4n46FP9IlAs+mmt'
        b'Ktpa/V7uYMTIkJs8R06NSyYNFXKKZaiMvKByXNV/glxAFNGwn0//xPqxtaoix/Z2hX7fhxsuH7y6cJtQeKCh/9S4vsmJwofCh9bEFNnV/tPi+qX0PZwqFC4ojCud8NOD'
        b'I1MTt8bOizYfofLDLaXAPzWxCCSHqWjEr/psvFNm4BkTH/gkbqS8H79EjgL/Z8yf17nprJWRjRMSTMl4e1ZivMEE4h1pQihOJ188FMg092g42Ku8yl6+1FLutAsOd63T'
        b'IvF5LR3q0jiGiVq4At7FBuGdrNwh+FTltZ4at3N1z2hHaaOzbwDtaC1PBdDuTA9oR9UbvD8B31kVC0iXCQoV3pFvAjG2CfqZhGH1Aet/Ah9WktOV+FYn7SOAgkxi5AAJ'
        b'2yVGjiHgo2kHnRg/7caoTgg4XERAoyoGEBAtmKe0Dlo4eqWEax/IowHXkPX3HmvOu+njUTErbcsUVYH6VGv1VcVaEQNnLxU1iVFRVs3b6hFi4amlGgTS3qotC62aedPM'
        b'YuHU+D7UFhC9L9Na32dEb7Hw1T6D0GQojCy11h9ftEws/OUKHbV8JNuXWwf9bdAaaVVMHoWAS8Y9l20tW/jkArFwXbEeFSA089Nl1lmfrSwTC69HGhHwluQ/z7cO/9K8'
        b'XixMmqCialDy+kRrzlxLslh4rTgclg+y6gdbExfUF4mF1kGjUQ6QtcEG66wDrkVi4c+fiUfFcC9pkJV/TR0hFroN/YHXogUnK6z1HxuGi4W75zItavKmJdbEosrZYuG2'
        b'yVEIEGhV/wlWTdwYk1i4p/9ANB6e7DfEumj+tHCxcIFzCAIMsDY9aa0vntRHLPzLohFU1FzgjbAOf3F5nlhYt7wfiDho1X2Ddfqh+U+Ihb+baEKLEKpSj7eWPemSiYXh'
        b'iyegKoTUkflW5wfj0sTCS+YUwASk9ymszpRYaeLmFicjK9RZtMbKfxk1GRlGMmkEv0xumMYhvAmEpLFoLG7CB5kMtm4a3j5ODncPUftJyjLSxoQUWPpbh4/jV7qoTj1u'
        b'Lm7wREFpxtw145SlgOrj0XgzvuaJpoi/wDWOq3MjNAFNwPfxK+zBNdq4cQr9aIQmoonJuFWUe3anucbJ5tKGJqFJT+JdYkPP8bPHqbJKYRDRZPw8SI10udrwhWzchsg9'
        b'/AJCU9AUfIpsEkWes7h1FG6T40NUDpuKppLn8CUGB0deWeeS44vLEZqFZmlyxDaPlWe6eHsCIDmaTVrwBlGIvTqLXHYp8UsFVPxPA9HrAHt6CtmMj7s4BxCLdJQ+lJwQ'
        b'IWzDZ8a4FHjTWBgAlFFZLtbRSu6luGTAsS8iNAfNmQFDRMdz6Cr8kksFAvA9wD+UGYZPiMN/jxxbT9rQDLKZ8sAscnwSq3wUPjSdtMkHJiGUjbIXAiC0kspe0OE2XoE3'
        b'IGRGZgveIwqnL+Dbq0mbEp+hgmsOysFb4kRgrgPkm0gblwdLPhfl1uEtomC8mxzHF0mbooo0gECK8kbBMNJmi0zkBdImowOXj/LxrRwRSBhLBWlT1eMjCNZkwXTpac08'
        b'4FGg4cOIz0Vz7biZDTi5vS4rQu6AWSlEhUbyHHvUkYQvRfDkHiigRagogtxj6IAvJJoilM5lCBZg8TiNCNtzeE9uBAd6PzRWgkrIJnyTVbGO3K+OUJAbsNjmoXnkxnBW'
        b'WkeuZ0fIBj+DgHjOB+y9ymBwL5wVoYoGcRyoxQJyQZqaDaDIvICbURqsh4VoIT6xjI3qQHx4Jm6WQ88PAKNBpcNyWfFIBSjHzTxIcY2UTzyVMab66++++y4uhpHK5CFz'
        b'rNXuIUukVTx2EqqGtdnHZHWeW7cUOZ548ze862eUCi5SLNs5LU+WGp12obLvwC/GKt/Gn1/pPfTVg0mvRqoTR765eMPmzZuX84eaEk8Oex/J76z848wjm+Le4HqdP2tR'
        b'lSTdqU4gf/ufsg13Cketnbh5vSe1pfSJ3LPhSy/+1+ErqV7Tc7lrqq/8RHvnu6szntH8+i8bZm+Nm/OLQa5Zf2wd986trw+M/FnWl/jnlwbOObXcvv/20d/f/NOenTvW'
        b'XfpB5bWLb8z5w4D3S8eNeqZ+Z98+a7++89aYkoVXwu3f6T/81QdLX/zvcb8il39+dc23E59d9NJHxT+4sPIr2dLpU47+61kQfym/BN3xwCCQXfOo/e3aU8DxORBxL/Dk'
        b'xfwk0YyQT46LhgLS+JQoK+Bt+IibGu/w3Vy8La0MVALQm3ON2dREGkNuyoj3GbybibYz+eGkmWw3Z+FLCDeR40g5me8Pq+c6k6/J7eTqcSNc+FJmnlFPjahkpwz1Irtk'
        b'oDAcyjIouhQ05F1JBUHih1YSPzzlFioKM9kjkXJZQcPJQeYF+YOP5eiP5t9KpRzkgjhaItOCXBINkrEG/jr7+es0yEAy8ZT3JJBwzjh/4+w9Afllked6sDgA8URPP4mP'
        b'UUGEvILPS8JILlxEI7CBbFDgvevJCw+RQ6gNFAXJIdz3t1J2LQirRDmkfBqTGGYee8pa/fUEoySHfBtOxVs0eWi0VfPjxfFIVGlbgVrtHUdOzkmW5Nt15I5j+fObONds'
        b'ysKWfPiJtfTVy7uO7z3XcLzh3MdpB8duGXv4eObwLYa4N822PFuVfY/8SlzhgdTE5VtLt2rfGKA8NnVf9bEB74xH//FF5HP3PjNwzFZF2qChKww98V5yXZJlp9f7RdUe'
        b'0GSAiCYut9NT7vaArGpx2ivsTtCfRJTR0AFZj3g1IAQTVvsHoYTcBQ/3jBMDAjhBX9wUwIkNPeDEBNqlE0DfTgXE0ySTIT7XZDBm5+KmpOxcszEbFCZQQ/FuvC0cuM4+'
        b'shEfHfNQFAkVVR8dRTqJqv4GQlFEmccoM1AQeYRTNpWaRKjuf/BpPUOS4vLxSPfUrwB5rIUjp+SjDEfR0DbkmgS3bsce/cS6iOHClYblXHn4+7PeGH5Le1r7RsUbsaer'
        b'9w0/FfuBdWvrZa0y+skDG8fJkHZHhGGfHjQZJi4cIg05bPojk6TJz00VSdNLgISvJJiyhtg7aDLkwjppGrtHjrgOKkwoaoSLqBGm5voCajgHBiNG+UMRY1AAMeiLTbTC'
        b'IQwx0Dc9oAYIJ2jKM3hLl3pLADEG4MuAG6vxuTDSWIm9D1WiZR2Ml4+uRHdJO7pCDIYANSotFa7RrBSrpiWqXmS2f9MrKAe2Hs23Vv9j7VixcKLAlBX1UIVV8/noxcix'
        b'qyJO7jLDnSevlX9i/dT6ZllVxUX7h9azNn15YsqH1gWv3tw1DKgH92ZFtm2P9cMRVwX+52/r1h1/WjVb5QovGndi8uwxs4cV5IMerERzK6Lr5kUA9lARJYXT4Qs5uYkx'
        b'Mh7JzRy+mof3uOnG3pMVZCO5S/YCXyQ7kvJzSUteFr4oR/0K5RNluPVRFeHIGvsqt0Xw2C2CzS2iTrSIOtHhwH6YQQZUYefgAALJfXL6qC+s2m4T4K3VDzHAUMRxDg0g'
        b'FK1oZxBCfdGDLkzNU/h2BTlMmulmH27KN+TilvysuVrKxUeRq4rSifZyWdAMK4IRaJaIQHK2CafwKiuUEhLJmAVcDkgkY0gkZ4gjWycvCkr3pAgrOyGRQkSiJXZQh4o/'
        b'gJQ1xjeuWMSXjXkgxmV+zANpyfm9bihyNKt8MlcZ3DG/Mn/w9iuRG5I18j+sKExO/eWPtNdad+861lzoKxnQlv7r2OaP//ngP6cY7ybr+yp+9LNPrHNO/Eg18PBNA9b3'
        b'm/7CzbQ/v/NK/Oqa6ec2P7nnzK9Tpnw9afq/vvuJfsHPr5VPe/KJ4v6DfrdesiCWktuALnR7TAXS1B7E4xe4kpIhjEB5ZsaKO8dyN9lPt47xbXyGEShy0UJeNNMV3Exa'
        b'8jl8EpQBNdnO481LyC1mpqkl28gNuNuYZAT8HDktl8P3VZms2lWLy0lzLgYSe2setLeZmzOEHO9JXlJ2e6sj0moq7R1wdoCIs/0BX3k5R8UkEJJ4nlfzMf+WK526APYq'
        b'KPYCylKE9CnLPe7aimBa2OVyAaweTtPDQjGZVnowCJM/6ts9JtNnyU5yrZ853xhA48SJVhj1ofgFOcXwiu4Z5EwkyVB0HxlVKP4v5KhI+O3TCY2Himh8SvEWauWQ+vLI'
        b'lWYyXzIo5hcwe8rk5MVnwr9Kk1T9368JY7u9ySvmrhmuK0PVFOgH6UzgUievOJUxrlIkpFXURAkPziiZ84VpmPjyeA0z2+iT80aMmT8xXyy8I4ynZgZdctZbK3ZNl8wh'
        b'd9LF7efk0ac4dYFdstAsMVCzTXLy2G9lw+RzxcIbVTNQPXDR5DDl05NnS3YXo3E6WkUbMqx3lhWNEgtLZFORm0KZtUp2vo/05IbKOGqMSU5ePNzd6pYI/j/WMVOQPnns'
        b'ZOVfq6ThWJxMLakwHPPKx/7LniEWasbMBEyAwrDxJfk16yRjTDhjIrrk0R+m22fWSjaSFCaq6pOVq6epYqLFwj8MZLYcdbJ2rOV4lFEs/DqCKXzRyf3/ubQhKUUs7Du5'
        b'AB2jDSmeiXQmS+M5caCA3qQNFX3JXZ6lEgsz4irQ2/R1V82UkdFSjz7zMKtPdHJeyfAw/WSxcHkvZl6KS644NsPyNCcWRs9cg/5JQRo4VL8xvkAs/Hj6OKZCJK/ey4et'
        b'kYZuUF9mXkLJtoTyP+WtR45lr09SuMYAVjtqMkp2p+aR5Oj0H175z9ebzIdi9vyiLrbmZwnbi09mZwqvLbn71hufrtn8AX9ks6tO+8YbLdZx6/6wvuLfz3799oWF9fqX'
        b'7q7yOv6JL8gGvZYQ23eQdeaDrXuOyVplx66+OmHnGlK8IO61sMTvvvp8cG367xr2ns1aMXPT0W3Xh2+5rnhx9C+nuve+funP33CLdqw8qTx2ZHVD5JnC+y8VvjHw0IxP'
        b'TZePR/Z5P3f/xey//erk8pXz/vNG1EclBSPe/nnJS6N/n/nz1PSaK0dHlSwumxKRV5BeU/lO//9Z+/mI35VfKdxfMWSW5eS6U7ajg+eebuob5cAv1uxY6Jzz7ijft6v/'
        b'unzUivxn5p/ZMeadmjcX2d77rH5fv7Frd9+yr/hg+O9nnLsXntIc/WqrMfqdz598/pvpm9Z9w63/p+Pql3sNMrYhgy+TFnymE1/HJ8hu4O2kOZupFam4hRw1J+ozScsA'
        b'csUMixU04tV914sbRrdi+AR4PZ7DR0gLkns40jQaHzBEPoTEPvzSAwEPNq9TAl1mq1lqqaqtdlCCy6j0PJFKT1HLgE7D70gmYURzOrbFE82kjRheIw8H6s1z4eKPrMNf'
        b'MfUX+SAN0HlQhoHGgzI8IkDhQcBdbbc5g4h6DzyHc44M0HNaxYtB9PwXsd3TcyOdp5YFi8gL+LJI0rPJdtKMdzDvj52kKQcmLVGJniBXlOQmPt6/k4KikP66KuBipz55'
        b'qJQXIpjJngc9iBdkm8NKZXa5IBcUm1EDV6qAtFJKKyGtktIqSKultNoup4yighfChPDNaigJ84KsWhrOJBmNT5UqCE67y5VXrgyCRS39Ml6QQZmN6KwUcF6qUEssR9mo'
        b'BpajApajZCxHxdiMcp2qKCjd3R4W5WmdVXdFHjOB4dNxKUX0rxdvG4aGkQ3rRV+UNUlvci4g0+gH5OjgbVd64eRo+Xf5+zYXeV9Pi01VvKPfkFZ+Zkjq19syX9ScK/r9'
        b'yGdc0+6Ye5++fcD9h+Px21uTPkuYOzT9TsqQG/x/3+xXHef756c507b++7eL5k/a+E3980348/SdmtGyyCOal9ImjzvxBf7Tkcj8gzeGvvni0AlpXkO46G6yocwsLjVx'
        b'nZFNE/nVqbiZmY/w+Rp8P3qF38tF2hnFu7LZSkxOmo9fzAnduT1I7rFqBY4cZk5sYr3kzpw4HjelDGaC/1P43JhKa4LJmMm2v07yyTIlE8omkcYo3Ix34pa5ZKfZCImd'
        b'KhTRlydecqrYTQWhWb0X4uZ8WP4z+pKWBAM+L0dRYTI3vraCNbsSb+LwnaHskUR8To6Uar4/uR/HzF1T8JneuDkJBDpTFrPxPIl3oRhySgY6/M71ojnuBXKhiD5zx2Uy'
        b'ZOcaORRBmnlyA18hOzorAOpHJi/t5ENlsdTYV1osfGA1rgdxXdoT7st25qgvjlL6WRMlYbVJek8kBGqfrLzaxTbhQOd1uFf71HW11GlAsPuULrfTbnf7NJ6adutKT3qM'
        b'0kkdUJ3Uk1Hc1jPQC92scyYEKAi1l/07iIJsHdAtBekEc4j0x0m/dEG46MqsR0vokqowcHnnOJ/aIu1BQlrusldXtPtMiAOonl5tW1Ym2GZEQi1OqtCtifa357/1SA1W'
        b'QYMGzqew0PFzmgKtBJpyUu87rb+VR+4E1Blm8c9Gt/VGfZ96VRZxbrutNbrLWkME7qlItEgBHX18UbsT3aP/eNSR7snyHNpbk3gXpSF3ruBPrB9a3y6rqtBU/DFHhnp/'
        b'Lv8B0AK7ZEM04g34ePuCxZf1dM2OtYmIzne5iCIdriDLYbsb23r46bumjx8dQp4S3W5kziRaS/tqCG7AFBhLEFRRDOf339gAP59ru8f3rhsE6k//GSIApy3Um85i8YVb'
        b'LKLXOKQ1Fstyj61avMPWFyxiZ22d3QnoyNYhW5bti3E86zr1vrO5XOX26mo/Nei4os9RDBQfg0dYh+j29ld0nCg/UisA9O9iemk49sPzomNypZbscuVkGbKNJnKuQInC'
        b'lwDhtZOjnSY8Qvrr2s4F8XeuFMTW1qjWaPiNbI1y8BU8pKQfgW9RComU/wc5CUcD76USQBjwcrldARKAajMCfh/WwoMUoBDCWT6C5VWQ17B8JMurIa9l+SiWD4N8NMv3'
        b'YvlwyMewfG+Wj4B8LMv3YXkN5PuyfD+WjwTIwmFNxAn9N6tLtbQnApU1BrRwDGYNyC0DhUFM7oiCdwfTd+1RwhB4W1YazXoeJQxt4QWjZJGRCTphGOtbL3h+OGtrBGsr'
        b'BvIjWX4Uy/cW325VtaorZK1yYXSLTDAxCUX0/qejpfVGVYQJesHAaoyFGuJZDQmshj6CjK3OJJCCyhkBfTAmXBf0TyoVjyWE3DEofXIHyLM+OcXErhAvr1wVNPl06Wj9'
        b'K76QEhNRnAqjAyhNrN8rXFuhlYiMiglXaiAyKkZk1IywqNapi4LSQGTEbsjf+wYQOwRM+i+rxuF22Koda+i5iiq7ziZ1ygGMzlZTTg9mdHxlap3NaVumox2cqkt3wFtO'
        b'9mrWrNQ8Xa1TZ9OlGN2eumo7VMJuVNQ6l+lqKzpVRP/Zxff19OVE3ays2QZahT519uz8krxiS15J7qz0QriRmme2zM5PSzeYuqymGJqptrndUNVKR3W1rsyuK6+tWQHr'
        b'3i7Q8yIUjPJaJ1CUutoawVFT2WUtrAc2j7t2mc3tKLdVV6826VJrxGKHS8cs6FAf9Ee3AsZMACbXGRxpeOjMT2Vw0ZT/9It/eEHPoYysu5clfi2+L2VgjIryjePGTpyo'
        b'S80pyEzVpRg61Npln8SWdPraOnqQxlbdxQD6G4XuSC1CqmuIH6UeP58W6/Lnvn99In8WaxPT36OuTob9zjZZTZ6H6nT4+vIkasBMNNHDKeb5INsiMztBQ01v+O5T5Aiz'
        b'XyyM3YEG9U9UoGSrdmFBEfJMpLWtczMrZgFppGJ60ohE0gTp/CLSSOsoyaQbw7m5WbkcwtvIC2HkZXIR72L1tRQqkSb6fxDSWRO3l89FHso6+67Fd+luc4KZOlrmzM0E'
        b'MV0U0vE10ignewz4HCpKVZH9ZDNuY/WsBwYm1y0HAcVa/d4iyVYD6iBSLxCYTbls8SixcnwLdM3N7dXXpNFzRfQUDYCbVJhJtuUo0RxySkmuzCJH2DZoFGkhF1zLqcP2'
        b'TuoIexRvSylz7CwYIXP9FG7/cVXRqJ3TamaNjU7/4Zd3d36zOe2FYQnW/p9unFg4IGH3pjSbPrfh8L9W7PrHLdvghaUv5royZqysP7Wx4T8q/vH5/r+WbPrRBzXJxf0+'
        b'zXr/uXcmVL6/8fc//+RHP5Ctnb921+Fj3rKWv/+4YmDv8f+cdjB396r0SU/d8x6dvuyPA67sfW7Oh6ox33306bact4xbRp/eb/lyx/VJWfUjz32T+85n7366KWn0t8f/'
        b'9VHCX7jSnL+++g9Xzqx/KJ2c2TR7woU3PO+b31fidzeu3NP8RsnEWy/ffbnlhm7O3//w3V9as8e8tsoQwzZPyMap+HoEjJEh12OMJ9uSeNQHe+XkFr6sxmdjmSYUR1rx'
        b'Tr/XAXU5wNfxBtHtgLyiZpYacplcesJsys6lbrXULZ3sFI8sDcDX5DX4wBRxA3iDlRySzjEo8SEOb+CN+AzexSAZjk/EBPbL/K/3IZtldb3JzWgTU7jG4sv9EkwdvB2X'
        b'aReTA/igm7oN1M2Jg0mH1xOol7N/V9ZsjMe3plKcpy4Lc/AVFd45MYHVSM5QWEXDBUMKvPWpiLk8PNuwUHT3PTDBhpv98CjIoRHkPEdul/VnSu1YvG0dbh5eKL4rI4c5'
        b'vGMN3i9WvZGcxbvou+IaU5Dba/AmngN09jLtNLnUKGqnAd3UNBi0U3Kil5udE9tYTW5T7bLFwI6sJWZRUPGJsWJ1CbhNQbY4Rb3cpFNCQ7vIC1BdDgeAPM/hXeulsyX4'
        b'XN0a3FyJL+SbcimQL3P4sBO/IKqwbWQP3kGBzKWOH3TzQ6t7plI21Yxb2cEV0oYvxAOYoqSnRNoK3DxblgGdeFa8f3ZYBH09EcaZ+QRrk8nz+Kwsrb7Gv/Om/V/b2jpK'
        b'9CAiO4C7S3pxpl+YH6tm/qoaXs1MaHJOy2u4vjw1pmk40ZOa+owoO/zwVFKnP/9WKkE7FCmvyd9Enig1h4mqwJP0MhP5dd8OMne7ovDIyr5BJVbSN7R2VmdSoGImldNd'
        b'vKEhasb7o7tXMzp15JHV3HNUzaUyULeK44IgZVpqxa9MPxhVHBCYKCsD4cLPy/ROu00w1tZUrzaYoA2ZUFv+SDBtFmGSW8oc5d2C9JQfpAcjKQAgbvXY/uMNBpN1u2t5'
        b'caDlhJ5loscHgPbcSelat43bAo2bggWq/0374VL7Szi/2YOHBWcTlVYRWbuDRggdip6ErccHhVk1eGd+YHl0B0VlAIqkRxHTvu+giJDE9wTJkgAkxoeLeI+LHKIJTISi'
        b'OwCWBQBILmZ6C7QdbOjTSdOqq2aH0ruF4f/GJiSpaw9e6CTDzqb6h0vn6LBiXXb7MnYoHpQeppZ0epEelJd0sSLQfaCH6R5nra7AtnqZvcbt0qVCjzqLzHroNnQeXlwx'
        b'0ZRiSjb0LFTTfwrU2VxfbOA84ibTYHwlAbgfvkBekSP5TA6fDyNtjmP5D5CLnoP/+49Wf2J9uyzTprfrCz+0vvlGUdmnkOfLPoh9I/b04g+0b6xS6nYOO7CxTYF+EBVW'
        b'NPF5g1wUzw6QE7NC2CvZhXdoKX/FDeSwm+7G4yO1ZBNpsXQpPJGbJtzIRASlYa54jhwEtJMyJB0k328UT4o+T3YkmkGIAYFlgxLxi7kkcjOpJ6Oailqv/OeWJB+r9WhF'
        b'ONeXWnQlpiA9I7JQ54SOtbVb0Oh+WF0Ia9vTgwWtY/0gaMyE1x7iQEXNDMjLPbYDlYztGMkfeDshSZHdLZoWPNVuByjWEvH3uCRNmsWIcDttNS5bUKyHstWdKqJ1TGXG'
        b'lqnWXHgGqoI/tkq70/oQfY/+62xRlXxw9pWAHjf2SZ7qcZGpgqjHkW2GdSGKnKjGKYXuFbkl+FnHy+c8ctdkeN/y5gefWLMBkxMLP7J+2EdtXVLxqfCxVf4zw/bfJKbH'
        b'j9IYZq7oXXCyYcpzY7eIGJ2wJOLGG0cNvOhJc6qfQ9I3IvCBIJVDTdpsTO4l54uoRJqUoQ+VfIPFXrJPKflgPWz/1WV3W/zTw/h4sGcX/eH84uGa/n606vROnr8xJpFR'
        b'XOvZ04s9kRTAbnowc00Idjd27+vVAxiPszOiDX21Ww6xNZRFPSomm/wnuyhp6d7xjA6E6KtDDZQBf51HdTvz2/dApels3wusvlqno9JRY3MDnA6hO+5aY18p0fuxprFd'
        b'WFG6Nx0Jon2GDYHfxxQaMukK7cs9Dqc0QgKkyt06wV7mcLu6NFfRtQ8QuGqX+eU0B7BcW7WrllUgVi0OcoXd6eremOUpFyGaPSsLmLljuYfWB/KNnjJundMPFbSV5bZR'
        b'Vv5wEtLZF1Sd55kG6aj15JA5j+7os4ASeca5mQFX1kLSmDM3U1ZowOeydIvLnM516+c7FoehWZVRy3Rkh4dyvnAPOR5i5Wl/G03Hm/BVepq9mTzLLSfX1fPxIXxaOtke'
        b'riBtmulrOaphIvwc6uuhzujYu5A869J65mXSLdkS0kjaBifOY44GzfhccWYibWZ7Vg7ZxgHtOmlYhfeNJKeLeUSexTc0BeQIueChu5Tz8bVeEljNHhGyukCtBfON81So'
        b'YL0Sn4wg1xzD/1rHu2rgpS0Lrxm/Ov/2HeqlmD53Pa7lMmzRcRveiIlJD+cjdn1wRVG9rU9V4o/n/Cr6RMMNznbq0h9+M/mLH+16ashtuXz5zxIdv24IO3nmv0vPfzjv'
        b'd9c/Ig531PPPznvvqQ9i/2dx6nfv3P9J5C8ql46fe+Pu00/pDv2lwhAm2h/OlYwDcu1XzsNqI2p4cjgJ72K8X4b3R0XEk5aEInKDkUq/EWcobpOTl0biLcwCULGONCUY'
        b'9eQa2ZjpP0O6gpwRd+0vzsIHzUFWiEVxmmhZn+miALIE3yC3I8x4L3muo41IbcQHWQ0puBFfxadm+cPUiKJFLTkgEvwb+Da+l2Aid6o6HlPNMooQPPs02e2KZbaQgPGC'
        b'7CD7RJeDF/G2FXZyCW63my/I6WzJi/GRnHAoJW2nEv4zrsPbmUBvNej/IiPQSOxAzCk70OOQWvL8MDBSHyCHPfEGWdBj7Qziabg0cX6QNrCfb7p3uukBpMfRa+UWIG7d'
        b'MobjAcYwluly7ZSvJwXmMbVrA4PC071afzIAxbQuSd7sktkd9wq6gIe6Qi1z2it8SpejssYu+MKAWHucTlARMsrlQbBS07nGTwvzRObVHlULeSMkTyBNhUZiZfJGBbAy'
        b'BbAyOWNlCsa+5OsURUHpIFZ2sEdWJkYVEyVAxhWC1aHuN6xo30Se4H83cAai+70HNhLiW+wVGEVaZqOKoUk321ZDtS6bdK9sCXC3Ltka3RYDTlOUP3li8li2IUY3qwSq'
        b'7IJC1m3zgQmYqsuotlXqVlbZpe026DDtc/sT/k5113xNrbuLZpx26EiNa6outaNobZW68wh8sbPWF57noXa4GqBQp0IZI2kEKo0bBlBCXZIJpYUSs+NSYvBeoKBtZtKW'
        b'jUaRk1pyqHyc5wlK3M4XxJpNxvhsfAiIc0uCWIlYQ6DyzOwSvRTRAmRycmqwhpzFd/B9JuNPqciq+prTcchqDZ81cgby0HM6QC3PjuxCyAcR35idWyRJ+PgC3sWk/Oai'
        b'MHK/DznuoZGO0rNSSXNv0soeZKb0LMpTEyiXDd6syUzMzjFlGeOViDQbNMt7Pc34Pb4/gtwPYfi0L6QxfE5+kR7IO4jxiQZjtgKtIWfCcMsgct0gE3Xoo/jmUtIMrcpM'
        b'eD+Sz+DwBTO57qGGciXZjzcnrJ8ivp9LPcQO8s/gk+Q+i7hG9k4lNxKyc+k4whhy+Goq6j1GRg5PwZccE87MkbvouZ19i08OfudOJDmckKyRFxRamrmULd43oz/6+W9b'
        b'NiBn7+jndNmvfbprlm9866GEIXXevcUbXhpTcfHrjKwffD716oLFJT8pTjpe9rL3/d9+dPVw39e1TyT+4b/+PX7MyP1LVu3VF//dXLT9LfPZb7TxI389S/W7B1VJbw/5'
        b'cMD1X6fuG7T+5Y93ru2fNGTXc+ufPZyQfqQIGDtVuXPIQfySmXE8vqwct3Jj8WV8nu2mGBeTW4yrM5Y+dnkoU19HXmZsc3B+L0kwmDiSigZMMCCH8WZ2dxzeYDWDZHU6'
        b'KzcepC0eqemx2o1hNmb2nzs0X1TCaoQQlk4O4I3M6Y40rLMxiUNBbiIWRk+jZmBX4/NmurkybzpzxlVW88NdIAfo4NYQ3EpOMG/dfDGCSiL3JG5EvZNkIH1dJLfZpkfY'
        b'wnWhuw2VMi05MNWEt4vMVPN/tEUQQVmjRDgYtze1c/vxShbVQh3g9eHSr4Yd8qG7Afz/hCvW9A5ms1JdEs9XitybEgwn9f922kMZf9jj+RLLxZpYJUmBOhkXrITLmQ6y'
        b'wW+Hdy8bdAX04/Bjtf+lbnnymwGePIwyDyCtjJUEeE+wFdEgZ15NPPxyGYa+TmqBcFIS5aS2BOrfKNSWWyxsb8NJyQ/bA/HJqKl/Js12sc3iU/mN0dRsxLRrX2SotksF'
        b'qiBJq5K95e8Xm8Be/0ebUt0hoJOS9/503uohoebl8lhO+Z2cztR3QyYyFPtWKfuef+XacA0XE86LQYLk4Vxs345PxHC6oWKaxa3EG7LxVVdOnijnL5jDofA1PNmBX8H7'
        b'OjG9cOmv69sODlsCXyoXZKUKBypVCvJSFfyqBUVpmKAsDRdUpRGtilZ1a3QrVyFrjRbULbyQD+JShDe6QsacsKkrksYeKUQIGuaYpW3hS7WQj2L5aJaPgnwvlo9h+ehW'
        b'rb2XGD4IxDDqLRTl7VWhFnoLsdS5CmqMadVCu9FCnxbmMM6e61VB3bX6SU/0hjqpoxZ1C4+FZ6jj1gBh4GZ1aR+AjRMGCYMh3VcYIgzdjEr7MUcsVBonDBdGwN/+0hsj'
        b'hVHw1ABhtDAGSgcy5ypUOkiIFxLg72CvEmpKFIzwzBAvgrRJSIL0UCFZGAv3dawsRRgHZcOE8cIEKBsu1TxRmASlI4TJwhQoHSmVThWmQekoKTddeAJyo6XcDOFJyI2R'
        b'cjOFVMjpWQuzhNmQNrB0mpAO6XiWzhDmQDrBGwbpTCEL0oleNaSzBTOkjUKBZKGRCblC3uawUpMgZwLrXJ8ydRnzEDsfIi3RhS/eEJ3ExIi1IAjSsIGVThuVAEXxrXx1'
        b'wF+pg1dQqMuZEypYZnc7ynXUqdEm2kvLRSkUCqhgCXWKZpbq1braGlFU7EqUM/A+pWWFrdpj94VZ/FD4ZOklhXkPple53XVTk5JWrlxpspeXmeweZ22dDf4kudw2tyuJ'
        b'5itWgfjcnjIKNkf1atOqZdUGpU82O6fAJ8ssyfDJstIKfbLsgoU+mblwvk9WMmdBxjnepxAbVvvbDTGOheyjUMJQz7vCKf1dyzdy9XwDJ3BLZa4h9fwx7jhyxbt5ga/n'
        b'+yIag7iRrwdkXssJsnpuBXKW1nPUGxLe4o7JaORiQdkfnotDsWgSWsvVqOG+iqYaEX2vHlnkUKviOFB7i1JQM5t22HuWrrSRjo5z0jy3+811fKE7GZ+NhKhh2MQ6WEkP'
        b'li1xyKYy17SifOP4lLGTgtFIAMUkq4IK/DpXnb3cUeGwC4ldqgUON1UigAX6XeRYy35NUURZ0FOcjjJPN4rFVHp7qlWwV9iAtwTQyAqaiqO8itbuEMcJkFFqBxCsc98+'
        b'onP+oI+jhm1gtfdmzCjXGB9n8nHJH1Gm8dF38O+BzJScnGdQ+aI7Nkv3W2zVdVU2X/g82pN0p7PW6VO46qodbudyyt4UnjpYJk4nYlYGJkRQBHOuRT2enmec9/eUT8Uy'
        b'2i8HnhErGUB0PBWL1kSJCPB4jgSVTJpgoHUrSPy/gBuBv4mAF4GxI9KwqVtdZ9dZYUrKgdVXm9LEv1aryUmP6jyG6YONUrdgfR2QbwYyX4auEbFTc7y/uWipObqGl/AR'
        b'/o18mAQ6IT61zWVhTqQ+tX1VXW0NaLjdgvKvACjlzLfAs6wMdGQYCmkMdHXVtnK6cWtz66rtNpdbl2Iw6UpcdobmZR5HtdvoqIExc8JIClYrxVKbsMQDD9IHQmvpvOUb'
        b'ehSKY6EpAoHGA0ehOGbNf+Tt3/f+1hXRKamjsplIcOyryqtsNZV2nZMVldnoNkStuMsLT9l0dc7aFQ66g1u2mhZ2qozuAdfZgXfMpoMLHZxlq1nKDPAudy1Ijow81DwS'
        b'KZDIgB8kCwPJSsfYw5a+SGgoRQoY3mGMqYdtF7t8NAy83V1V287HEnUuB9BUqRr6Gt2UD/bT7a6PUkVTaSD5qVaJxXaxXdijZaSstpYG59VVBJtgPGwqhA7T0CWRXGl3'
        b'wjJdAfzRVka9C7oxxoSImBSp5KijXUWbxxw3QYG8RxoSjJlZfSISqfprnk+tFTTsznZzfok+OzHLqETLYtTkPjlZ4aG+MaSZXMfbQKm8TK7P1dPjCI1kZ0Ievk5eKDSS'
        b'0zwaP0exiJyvxHvIHhYC3V6BNyWS8y5TbjZ5dqUyBkXh/TKTjlxjhxlTyFWyr92Cocenc6h5J95sLPRXblaAuKrGd6qyRfvDaXKGNA8nV116KSC9Au/kyGX8At7Cgmea'
        b'QMy+WIRbSGsJaSHPxuCrJdSIkU/jbZ2YnsHsH1pIv0hBUiA7vinDBzi8gVyMZaHrNWQLOeLCe8neTNHGYcYvylEvgBpfxM/xYmjfjbGJpAGfculZYCfFWo5cKsR3ih3Z'
        b'k/6hcL0JTxQvmd+nZVrNrLmatL/+68+pMWd3/X5x5g+1hSMGmNOyFE36Xb/b/MaPL59KHBNhnfL3v2Y8N+6HpZHqwb2u9V/yIHPHvsHya6XHX/+jYapw8wRqKHlrx6bt'
        b'ln99lvHnHU+e/c3UEf/V/+zqq+kX9644PGj84P3vLco6bfqzvLD/X5v67nhm8qdbt5zuf9KQVvrO+3P+Uv0f7w66tf6DHyddOln37s2/brjwynble/Xvx/7eE71+xOBf'
        b'NfxnzG9bvKM+fcrx7s3Ff19U+I+4T+bHvf7Na3+OPP3V+pTzT24+02joxfYF6pbzLFgVaVahyfiM3MjhSzDFB5mVAT+Hmwbj/YUJRrKNNCVlkhYZ0mTIlE+vER1Rr5Hz'
        b'ZCNuToLbHJqF5EkcbptPdrNwDc/gg1MSsnNzOETu4F3yYRw+2jtFPEx8lWzGh6LxbnNWbnyuCinlvHoOOcbsIq4p5JyZAcShhJnyfhx+4WnyCtukScAvkt3MnlM3qotN'
        b'GnJ4qOgv+qx+TILJEA9I1J9cYHgURa7KVuMt5BprIp0cJI2i1eSJOGaTwXvxVnGX6Hl8Jz1Bwj58GTfJ8zh8OYWcYACQBnK3hlpdshIRPmDCTUnGTFaNTicnL5NXyEX3'
        b'SDpol/HOFLN/tZGDKeZ83JIkrrh4cldBNg0fJUL6/PgCfB/fEPtLzYNNHIoQeHLYk8SsR/gqtHbfnG/kBpHziF/BpVrc4sDfcOKtIQdIt6zgV2fVuql7+oolM825ZnOu'
        b'CW/FL5GmRDMLDQFgxuMdCii5g5vESlrxkTWkOQ9fSlRCZoE8jcOvJOJnH8Pp8vucxewj0kVLKCtgtiXqXyLZltYjLfUyFa1K1Bs1lnmc0jObosVJK/qoSqXUT5Wd3Bwk'
        b'SUBdNpLnP7nFTl1+Hy9TTnyVCRZ74PJdB4tSQw8HNHsEDWqmEmb3vjcs9gwLewaCAxcUe4ZnXxh5NP8bKjb8siuxYbbI96QTPqK8SGUcYEOUlQVENkl6oKKES9ICOnMp'
        b'abuhg/jRQdjoWrjozPOKOwsyNsosQ3i7n9XWUhmA7rWsplJKZ8hs5VXijv4y+7Ja52q2NVThcYrs2sW+MvNwvt9RyQoVboM8JN02ZyVoNP4ne9xcqQnsrohY4t9c8ctX'
        b'VCqyu4LNAQ8RD7o+G6+WPJrMkRXPAFKgAqtma+wg8QQIGTko/ARXRwvr3wvPEgvfinoZraLy7Oj85Qs0f5vBOD85Re7iF8gpvMsVGQkoTnbQrZIX8HkPjYSNT5ThDeYO'
        b'0oZ/J8fPd4upd8B8kALoxozkbkDuzM4h24BQrRkSPRW3LXa89YWMd52FKhfHhOe2TNPi5Oi0yl9po2cM3tY4ed6a+IT0dxc2vuXIbBt/ZAN+JkL76muXc2d/VfHPjBFH'
        b'jq26fPnXTdO9eZ9ueHv67JyUbQeH41GTzn4ysXBJ7BDb29cKJz/4+7UVny6LO5U10PjbL+WVS8r/c17qqd/+5P+9trAWXyh4vQV/cXtlbtbgvreL/rRg0cfLM7685Rv6'
        b'3sf3Lvx4/eivJlckOae2qob9+e6st3+8RXXt/X7PNE7+gT7DoBUDIK3Gx6L6tJ/Q4I082cfc/FeTO33M4iAA22TyR9Q8WTWMwwXmtFVGjuBDQWMHjIPsIpeCmQe+Sq4y'
        b'NroGRKMW/Cy+I4ZhEkMwrR7upqdO8aFx+LrIBUQOAAN8NpgL4IPkZVaLnFwAPnE3TorYxNjhTnyf+RxUkDZyJCEQMgS39kMR+CoPXPUu3st4iCUMn7GR64GATTRcE96O'
        b'NzFGm1aMr9mNfnbKWCm+YxVDkuwkDU+ve1pkpp046R5y303dS+inUZajSQnsJnCxkHHhyVW8jbMkqfFJfHy69KGOYnxpAN6fwPZkFEi5hB+yLl7ktdvXlAafz7H3l7Zq'
        b'cvE9tutCXgHo9iUk5oLESprwEXKABa2PwntlTshd6+oE/6OyPJWkVjAmNz2YyU0U2ZuSHavQfMfz4d/yvPpbXhb9P7ycsjQan0TLWJ7oVKHl1mglPiJVGupUtzaUs/UQ'
        b'qYQXn233nmiFix7qco1s52cbkK/7IFQdIemkylMaxFR5qpJQVR5+qdFtgMC5eUjLGri+8IDAh+T80aUe8KMcD+SjTCkV0DkKq09jqam1SMq2yyezlblE20wXar8v2hLY'
        b'QxdtmNm8/8A6D8PIr+nnN8d0eK6ToTGweZ0Dl0b2gYkG3plRz7H+oKUy50zaL2d8PXeM9gMd59ZyNX3dMoGrZ3n6ZIVMND9CWk4/UsGYMZ/3YEyAtS5zuACM8irGlEYB'
        b'T6CWLaZs0wTMJBuC3o5lddWOcofbIg66y1Fbw2bOF1a8uk60Z7FBkYxXPgXj4D61aA2udXbjh6y11DntwNnsFvb8XF46tY5YcFglDBjFT4oFa/r4By7kjS4nnw0bXZkC'
        b'tZ/CUFAL6hKugu+L/AMQI9amp51MFLvqfCYwqdpQKNUWC7TptFgWUfiYrBRsVxPvdY+GMQwSPyJKUFRQKFQUzWDUg5rugE8qC40yYGFnpfwtawMts1shwhtNy/0NxzH8'
        b'PwaYIHDH+bVsEOq5pYHmuenneOfzSLI1QpqtyqNdgKG0WKrdFksZL3F1BLOzJjIAB7332GAEkJGf/oTzFG3qdDct2y2Wiu5atnfRcgAHTMFLZ7h/USzla3UiDEu4pdTM'
        b'xcppirnfipNBYekGaQEk+3KLZQnv951nyBoOZDQIMPpEJ8ACRkYNGxLaqMbv9Ss20M0Q1EA364JQoL2dmq4G4GFDL/cPPTejx5GvhHl1dTPyld9nzhWBOZ/R85yDgmJZ'
        b'2V3L9i5WW8CNng6tf9W3n7NpJ9id1zY1o1ksz3S5tsV7If0MEXFHdtnPfnRHCDEyzDfwgcFOOCdrX26MsPpjlBwNlHYAD9a/TRAslnUBNsKUzyAawG53uQSCMI0CeJwL'
        b'nMZzXu9u6CmpYzU2dE3qOrf2CMMR13E4KtlwGJ1ttN1rXXfb5SmzWLZ22212u/tuaxkgEe0dZ0vs5Z66zWps7rrbnVuToSA6QwO6BOiM1o0YTYF8bMeOMy8NmU+bV+vO'
        b'Ao5qp8ec7EI7PrDB6O7MjsWyzAPIuIOXNkUQE+JCRoU98FjIYOCcd3saFVZja9ej0rm1EGSYHjwqus5oMTAwTgM7jJMQ4NNcUjuSdDMuERaL2+mxC44VFsv+DjSZh9GJ'
        b'CQAceOz7wzwgAPOAbmHmkx4OtAZYWnVtrZOB83wXUPcOQN3+3PcHu28A7L7dD/Woh0KtYiGNLJYzXQAchIS1HWmEPBjWAhTKlNthdVNo6UY5wNWeXsSv5dfKJJhlDRR6'
        b'mZiq4ANyO5/nU8IYQdMgtTMa+zoKJrR+RYUSWp9iZVVttZ26ES+zOWoEe3fSabjFItZpsbzES0RF7LGGp0fRw79b0yvQa/+T3UukVA4UOVMEmwyJM/gljq64E4sgV2mx'
        b'3OxS/GO3HqW98Mdor67WZbHc6bI9dqv79mJZe26xLa4DzXMeCJmP7loH5cpiuddl6+zWI/N91s/LPbTkqAEB5rUuW2K3HkvC6L6lMLaAbVDh60FtRQevbnrT2YC6MMOG'
        b'rG+6SpYiZ7QbNFfmUsIJMkFOmUw/AGQtXR1UE+Qb+ePiepFWCeO3iryPaKUPhrOtZEdNpa6udqW4GT02WXTJ8NTV1dKwRA/4ZJOPGwsrptE/ZT71co+txu1YYw9eTD4V'
        b'1FTpcINObF9V51f/ujVHwEiwxi2WH7aTDzULnKoNHhHpIZE30WExJHVwPHQukepzVde6adgz+qVDnzbUtA35igp7uduxQoyvDSS32uZyW0SjrU9u8TirnftpbYfphRq6'
        b'RRfGAI761AGlP4JZScVNW2aBZ8qvk4bNFqnNcXo5QS9n6OUcvZynlwv0coleXqKXK/TCpK8b9HKLXm7TC2PCr9DLfXp5jV4IvfyQXugOoPNH9PIWvfyYXt6ml1/4x9gQ'
        b'8/+PS2QHf5NauLxNdx+oD4ZaJlfIeTkX9AN0MbZPN36PCuqcO2QM9XuM0/FcuFIboZGpZWq5Wq5Vin81Mo1CzX5piVbNfsKgVPphDuXkTB5pdtGj0NQbkkPqOJ7cHuoh'
        b'xy2dnCHl0l/Xrzs4Q/pjwlbIWYRaNYtJxyLU0sh0Ukw6Fo1WCGN5FYtRp2Ax6lRSTDoNy0eyfBiLUadgMepUUky6aJbvxfIRLEadgsWoU0kx6WJZvg/LR7IYdQoWo07F'
        b'XCsVQhzL92d5GoduAMsPZPloyA9i+cEsT+PODWH5oSxP487pWH4Yy/dmcekULC4dzceyuHQKFpeO5vtAfjTLj2H5vpDXs7yB5fuxKHQKFoWO5uMgn8jyRpbvD3kTyyex'
        b'/ADIJ7P8WJYfCPkUlh/H8oMgP57lJ7D8YMhPZPlJLC+6YVKnSuqGSd0pUamOOVKi0mHMhRKVDhdmMvqb6ouiR2+K20+4vne543aT/xBo0ENSgLwOj1FHDuZVUm6roXSx'
        b'zC75zrkdbLPH7/vBIrD5veqo+4e4q2IP3f+Rdp1C3T2oEhV0HNdKqbBNPD0k1JZ7qFIQqDmktlqnv0KHW7Sria/6N3Fmp+YWp0k1WLtx+QvJZFVIvis2XRmzAkJ14t5b'
        b'8HHhRLFJf18lt063004HJKQ+m4t5kVLgmEfJCqjJVl2t81Apq3o15Tsh55BDXg7huFTpoxSHelC4yjjK/pzRlAX2R428h3PG+dmgm5k/j3NrZQKwPIt4lbOrgl2V7Kpi'
        b'VzW7hrFrOAig9G8Ey2nYNZJdtYIMrlEsHc2uvdg1hl17s2ssu/Zh177s2o9d49i1P7sOYNeB7DqIXQez6xB2HQrMW2bRCRxch7GS4fX8sRHHURp6ehEIvfK1inr5MVij'
        b'x7ldnAtoT728H1orrxnASpW01DlSUAGTH1Uvp1bFtXL3aGD68gYenp/uHiOo6+Wi+detp+X1igYZh5Z/2gi9W6Jt5Nhzi7LRJoCAraOwPOdPqJAwQVwAnZZLzwuCcYkM'
        b'H2fx8RbLA4VllGuU68GojpVU2ai/VbvLlmh7Nfg0hcD9Hcsk10iluA0pRkqVWRyCT2Hx2N1OGspGPCDhixIDsweOyjnTKH+iO4FOajF3Um8gMbxKKZMOQk9aggQo7jdD'
        b'jXUeJ0i2dmiCSQYqZpB323xKyzJXJWt6KT19qLDYxT/sLGKk/zX25TN4qbyK7pWysL02t8cF4onTTi3ltmoaj6mmohYgZuPqqHCUMwdpkEhEmhG4bVvmbu+QL9ZSXVtu'
        b'qw4NBUCDJlfRHV4XwMfWLFTD/orBlH2DLB2GHORZWI/SswpIL3P5wgFIp9tF3b6ZbOVTwbzQOfFpU/0zI86EymV30xsGpeiDQA0PPuXSlfQ78UEBFerRw8M5sNn8A5X9'
        b'SpnsF828LDrG81J3Kunmhxf/RjPLkIZ9X5leY7g1/TqMwGPFppaMIh8i1L2PaQzoPKLra1zHpgI+sNOLmcdCzdL205yJYkgGd610CpY6IApAqh0Vq4EABxHGx3CJZXrO'
        b'7J6A7eMH9sHo0OBedHt/Wa27/egtC3b6iOd/qYewM7OnduMC7YbG9OrcLI2u+uinjp3mnlodGNrb4HheHZqVQp0+cliOnkN5DQm0a+gilNf/omk20EU9NT0s0PRvU3Vi'
        b'gFuXp0w62MHc3Wl7kpONFDGqR7iYsCRWxPYmqWxTB69RuYQFzOkiBpVJV9ReVuGw0wYlQQFqhwfaXXACtN+li5fGKT4Rkg43++uP+BXPdiHjxbBb8Y8Rcm1hT4OlDwzW'
        b'+M4RU7rBz9RZ81OT4JL+WGfjnR/1BEdCAI7pIQf0aTASe1noUf2O8MwuTE9LSkufVfwYaxXg+bgneEwBeArZ7AexbMkxy+/C38FjyKRLY1FTRP+o6pW21S7pdLquxl5p'
        b'o/r3o88dQPlJT1CmBKCM96O63+spCGCJM+v0RfPmlz7eGH3aU+sTAq2PYcS9tnYplWjFM/Yg6NbV1dIDVCASecRT+Y+FLn/tqenJgaajigPnYR69CfGbAs6/9dTEtFAK'
        b'tgzWrK3SHoSGdVWrXdTzTVeQmpUHa7z6ERuvFPecPuup8RmhQ9veaHVtZWibOr25MD3jMUIwQr8/76np1EDTotdfjWB01xrhTzvj1unTH69N6O7fe2ozLdDm4C7jPuj0'
        b'uY/dyX/01OCcQIPDRNdGEAlr6NkRaamI8TgKSgoLHo/GfdFTo9mBRmMYjWMSsnQM5rHG8sueWsltpwkdKReVq6mXDU3rZ+Xnm7Py5hSnL3hUuikN7Fc9tV4QaP2zjq2H'
        b'SvsmXQbQiDl2gKeGyYWugOrdVVB6IF7zszKKaWj5RN2cebMTdQWFWbmpefnFqYk62gdz+kJDIvPayaAoUyXV2V1tafm5sILE6jJSc7NyForpopJZwdniwtS8otTZxVn5'
        b'7FlogZkDVjpc1MO1rtpGY2CJsUEeh6x+3dMQzgsM4fAgoi6qRiJi2thitLlgFB9n4v7ZU6sLA61O7DhxogZn0qW2H17LysvIhylIy5tDKT1FpcdaJv+vJ0gWBSDpV8y4'
        b'vag2whQKFHdqH0NGhbXy756asrTTeCluCzsNKTZkbzcDBesij8Ngvump8bJQotdO7KjLt47arrpgKn6vErYNMk9q0JXHXN/i2BYh86mqG0TT4nlZuu0Bv/IGuFro8wrm'
        b'Kqegb1rY9ZgSrqrjHBeEpg+mFYpu0dSCFZBxRJGr3ZbWtUhmMqidf6HdXEovHaJMMxsEDXPgXIbYzmp7KOoOe0UR9HNzUpV2mX/DEfTcOPaVKOqSuWZgR4Uz6J3uZ4pa'
        b'0wRO8rwoFpvsapro9kStrH2fqpN6G/CI6fb8ZJw0R04t3do9juhWbmX7Thn0/1vaVzk1SnTp8qaWDBYW+uE0yfmDmgW6AkZ8sPt+xwYBI4b/DYwCM3X5oVGIekg3HnjV'
        b'9hqLZWUHaLowMrDn8gwjutquYsYPtsHk03YwXD0ZwJx2pKn244svMtRupZTMViqJc7PvEvuUkslKIVqs5MxgJaf2KhaaxKcJMVYpJVuVnNmdtB2sUhHBRimlZM1Stxuz'
        b'REOSNtRY5RzBSejjHEVT9HOZ/vhqj7Ct9C5cfkYtQ3Q/Sy2TR8SkPGZQDVV3wTb+l8E6uvurfNRgH5pwtUyt8NDpJ+fxS+R4xIrIOo2BhvI9Rm4l5OWYqKc6/bRBfJUC'
        b'X56/osvwjvSfaxUK3sQS+M2IfVhRJsgDH1ZUSGkl+8iimFYJKkENz6q9fAUnflCxNEyM41EazoLq8jSeB5RGsCeihGhIa4ReQgw8ESn0Zism1te7A8bnOEBRlwcBKg+m'
        b'AxQvKS22MMcNC0e3oy18JY1gIBMCTFrO1AJfWOAzyJBcVivYqul37oZ3NGXSFi3BWycuv1+HiWP7tf5K1P46OhI4us27QRZwoJI+vDeoi3Ye78A8MxDRr4h1H6o1YDPs'
        b'srXv8Tk759Se2vP623ucGqf1VGNjtzUGJp26RvgdQPzSH+8cSWud3l3VlF5sC+I53U1G16S+J/8P6FB7q6G8lhGolqBWO/JVqVVG0h+Br1Y9nK/uengfJd7a8ShAwMOG'
        b'xjT0u065YtzQtOTcz9y8lspc4yHN3KRYmqbkS2XO6W6FuFcGeeUxFfX+44IOPBiDZd9lNLpAWXvAhjEdIB0T+rhQaxfPz4uHCFgcGf9JPMYoQDI6gqQFyniV8wmamkEv'
        b'zL+EzhBwtbo60Lj9pwcigppgj3bjoCWzCcJeWdCZAbXkiE3PsnTBo9kwwzvdY1G4hEXtnj3tc9oBg0bDi0eC5rR/V411LZcFHDJj2XoRaXk9SkMN4rphXznvKAUHXqIC'
        b'AqWjT2vokQ4q1uzml1OX7kqR4/LOeDq69WKargsf5+6IkVFwORYgScauYHfXum3VQJjoJpRrBiQova9dVjfDwPlkLs+yLsUlBXvr+YeNC3sqz6DtKCq1u+EwhGnHlXap'
        b'ggkZszlpBpwZAUmjhzApU+ChtTJpwIEfK8WPIapl1AGFOpiIsQiu4XNkW4A/t/Nm0kaaEgGgNHKJbJqvyiHn4jpx6b7SX9ceLoRLw9yyH9kRRamMuphQBxP64UMhnPJg'
        b'+olDQUt5rtDriLaUfvZYAfw4RugNPFjBjt2qadQsb4y3f4VKiBX6QLnSrmIRssRPJauEOJoW+gsDmCOKShjI8oNYPhzyg1l+CMtHQH4oy+tYXgP5YSw/nOUjIT+C5Uey'
        b'vBbyo1h+NMtHiRBVyIQxgh5gibarKpAD2aMb0EluB1caDfdjoAcGIR7u9oLecEKCkAjpGJY2CiZI9xamSHHBaDyS9s9EaqGv0ay3vb2x3j7evt5+3riKPiwOV1hpbKuq'
        b'ta+Q0sIJU2krMCIyFo2LxibrQz+pKEyEe9NYO5OEyay8rzCOcaLpPg1FRL97hI8r8HH5BoWPnzPLx2el+/j0Ivhb7ONnZ/pks+bk+WRpZrNPNmdWgU+WVQSpzEK4zM7M'
        b'8Mny8iFVkAOPFObDpSid3ig1O1cwmjQnq8Cg9fGz5vj4NLMzm5I3Pgvqziz08TlZPj4v38cX5Pj4QvhblO7MYw/MLoUHSgCYrJB17w/HzrwgpO8giKG+5IFg7PJHCsaO'
        b'uvuia+fg4fI8D93YI+eLxqbju3Q5uElTvom05NIYp+2RTVlIUVMWO7mYk5iVOzcTVkk2PfpJP+46g2yKwtfIiYGON8KWyF00/t/tT69+Yv3YqrfrY/S2TFt1RXVZom3R'
        b'q7947dqusQc2jvs3PxhVFSo//zTZIGMHQV3kODkUgc9lmBMz/VEXepHbMnxpMHmRHSPNeFpNmvNz4Llt0DCNSXCYXzWrFzt7OS6XnKMfmIblu21gyAemnxzmP7z48P1q'
        b'3k+mA4cnxZ/J1HNxTWwwSoV+tlnRvl/ulFMa1eV3aIFosSfGBB4LtHyV0isaMTFwKFL8+WkPXx/oEp5yddB0UwBCP+mpZhgVLn0jXVyGYpCg9k96qhvDAMvCAMvUDMvC'
        b'GGap14UVBaWT22WKECyj/ez8VcNBeeIHLfZV5Jn9kQ0BpYx1ZJ/RRKPm0oi3enwuMbOkYCXenInPyhDZURdBdmWSiyy6PXk+Y137q4B8+cZ50tHubNIClHuneb6eNM1X'
        b'AwbLEb4FytcW3BQRiffOYYfMV5hUSINupmp11uqbWUsRi10/xuNaTrYEHTCfnsYejkRqFI0KJmit1sST6iLkoTNTQxqLa8n50BD5IWfNVWhhkWp13EDmuIhv91tlTiNb'
        b'snLNiaTFwKGIPJ6cBuTd7RkOtx3kIt6UkEmexcfowXSyd1xyMt5sNaPh+LoM30shRzxUOsLbba6EPHoiuSWXRbufX0Jui/3Wm4x60pgUT+MC1xrUpA2f7sM+90s2zk4z'
        b'k+asHHIS30pSImU/Xov34yMMVT1iZNg7IxPYaJcZ4T6+zU8kDQWemfTlu/jQEvFe0PH59rbmqslWPQsMX6AX4cJbMmVoCN4SiW+o8RUGAT7kGUBOkmOuFeSqHHH4IIJ1'
        b'eYMc9VDrB76IG9cHf9uyDp4q1sMkNicm5pZkkh364fn+w/z+GecQOSnTkJ0ZNR5KLPCBGUWD8U5/LHyyLQf60XuOjBydiFs9VLhYS3aT4+0jZ2z/8gD0JXORvze0FR5v'
        b'4+mHEu9HTMipFL9p8MqQFLJ3Lj5FjzitQbljyQ4WHQhvnYWvZ+SDhHBl5QoQIJpWkqtuJYocyOOD6QvEeM5t+OVxLiiGBhPn6bON+DBuAwQAWskaK9S3w6REeC+5GY6I'
        b'N41FZCa3s9IS6DjAuDQnkZ1Fer0xHh+PB1jzSoI/eIA34HNhcBU8w+hrl6Zn4HtVEeRlcs1FbizHLSudmuXkZYT6jZPhzZMcbMiWrCS3yEtkI2mmX2cxmmBoFSgGPyvD'
        b'Lyo0DOt/4pAD3luzVDOtmuLxWYh9a5OcXE3uuZZr1ynEr21uI1681eGs/wFyLQUK9t/GT0oKs/LIzOgjQ5Ka9le/s2TFP9Bzr0Y4N027dU03OUb323/86NYunadmHX77'
        b'6Ji/b5++YUjlbqfhzpl9f3McPiQf+cuUZufGy1trdfqcgmPpE38y6q3bK67OCY8x/0be1MBfGto/4tr1d6f+aXeb0r1v3pdpO5y/+QrP2H9k99lX1s3b3fBl4ekpleMv'
        b'92p+6f9j7zvAorq2ts85MwwDQxMRERt2ho4NLFhB6SjNroAUR5EyQ7ELAkqXqqKIBUVQVJCigiXZK/Wm3yQ3iWkmN72anqtJ/HeZGdqMmtzvfv///M8VgcOcc3Yva629'
        b'1vsKRxyjz/7wRGjKyd2ev0xrPp771cFXZ3//i2KC/fCdJu2r/Ywjwoo2+0Yb2Tx1MuvH/R3Oxs/urn76m79B5960p3f+lvj0jk+rXv3YLFIRUTanNih6SNSLy98eN3rc'
        b'kKoDe9eP/TlghfSThK+MHJ+Jbx4+4tNxR2oM3tp67sXlbh7j790eMbJ2+MamTmu/p58PefzavQ9ifnfKbn368rCnG0p/nfj4tZBr5f86HmmyacTXv/82/ZM1JSEzBk/+'
        b'49Dqp2QVxQc9o6+NPfLd4Zsvrs38IenOzy/cHrniNd9vHP81rGbknc6YF+5zU8KsXkJv/yaaf7M05ZaZfByl+ITaHegs3BBkZI723SjdUBZFgNiwBk++ohlQqKWikqGL'
        b'ApyehC4yIsj8Of6yAPstA2giMpIZRWgrOj0XFWWamRoroUMFnWl4VcgxlXBWqaIwlA0NDHf6goc3KhtOoIMobhA0Qg0FbJiOOi1C3ftSTEAtKqQbdZiLDM/CU6jaCYsW'
        b'csinhbsgQD3kxDCay2vmq1GReQZ0pkBHOs4UylCObKiwQQy5jGXi5mg7gnsBWWiPBvsClaAyWjVpWKijy3S42Z+/IgUdYPANV9E1uAkHUEkAoagQtvKzw1EFA6I6tRHV'
        b'+A/Fs68QrxS45OIZPMItgRuNToQS1IbyQ+BGACUQJbxbzp5pxPEQXUFHJaoMk9R0uGyOClGxuRcclJoaQ4t5Bp6L0JmZiqsRJJagq1FejEbjZhTa6+gMJYFwKdmd5yQr'
        b'eLwdXMI5WVNZDE5C1gIid/mi81gq2ckv8oynuEtQg66OJuwbRajZNwjhXc/FHx1FjUGEvrVDnAlVdrQZ5qlQMSqKdwohqPB4LwjEwtA8AVe7imeDKMsNt0QR7McrSUmv'
        b'9cA6UGxqMpQ180l0GS9mRa54nK0L9TXgJFHCWNTqSdNXQkUQKloJZ1zVq5kBJwsRoBqueKdR4+cVyLGBRrRXTYgWQjZonAneNCXcaDgthjZraKT9LYeaMX1o01DTKsqa'
        b'Nh5OsYIcQC14/BEEsJIV0BWIm8tPGDpsCoXUWBMOlRSk3NklODCEcE+lwRH8iC3UilMnosu0tDGp6DjhRdXuJagVWszCREHTY1lr7MPdiqXHcjgW4uKMRYsAER6UhQKc'
        b'gb1wlfVJ7Qw7nIS/kx+Uhq7C48xTiAlzp32CmvxsNbfIAMF5HI3C2fjhwelgbwDZg1lRUXdyALRPxI8GO6ECV7y0k3XdADfHZQODRKiiRfEPdoRGESFQ6UGPs0QXRLjD'
        b'W/AQJzuML7SNJhOkj6SOCrDse01w7avKOuIdpmScMToGZYFplGw5F5XCMR1vD0dn0H7c1ZAfKJdwgZwhurTcmPL0wsndYbqJehlLr1WMhqdX4sVQTval4S2+yDUjCbc3'
        b'0rwiwTqzCG6iguW6JfH/eepZal6gEn0KEUz7SvRexryUsM0KYt6GgKji39a8jWBCIFIoK60JbyFY4PvGvC2Ju70vFVnSQEATwViEZXJB0sublZzVSXr9Rc3MQ/pJ58y+'
        b'TIvXZKwOqdK4N4uJ9U1JxEKlB9EQZeuj07SeyhLV+g1xm+P6w64YPkJjNEmVG3h1okrKcEkToRmR3ZuZ0xV87xa7rEcTee4BBLa66/pnGGMN16lrqRfpVWu+6pvZnzKl'
        b'U4/BzQ8ye9/VHlvbU7YVTYQGK52dGg2lD27+o7vvqvneZOvU7lbrHsDp87u2IE66HLQUqp6y/SWu2iaeHWLry58ociz/UeHUM4v4Zf1lel7mGUIc59PTkuPj9eYq0uZK'
        b'+WDx0874cTsSK9DjI0ZKQn2t/xIPq3L0g/pfoi2AA/WZUMSrnSQ2E9cU3OpxSSTYJfavMRTjJjBZ12tu6y2GkbYY1IOL+GskEDA5rbPjX+kAZfGDOtxEm+Uk/VDKfTPu'
        b'lS9daLVAgiSCVYtSz4wKHAnA2clvs9zBUaMCTw0J3C4+rNe12qgQ39+ooLGI9wea009860lLEM//NdrbD9J5HQCG5F8fAqS+fiEqO9WG5PTEWMqAG6ekiOd20QnRxJtE'
        b'Z1paFqmFiXHRxMvKzptG15COVsPzUidFNXi52j9JoRveV41rHhUVrkyPi4pi/Lxxdg6bkpPSktcTzl4Hu0RFjDIaJ0780DRAwHr5D9MGzHoC4a92T2AIh8y/bWsvt7GH'
        b'A7xHRS2KTlThEg7EFqRhYVy/f/yAbhcFKyZMmCGoiFAeYLf2y6hnYqTxt09PxDKutIDvPLZbzlMtJlhCRENXKoRAK+zvJ4jUbWamO77/OZM4PiGOwqj9QA+advf7GrVt'
        b'fJ8NSLU+cR1t357DE5JALyJddpbUw6C7A9fJAmeqIuJVv102i/veRO8+m74YP4+rcwga+xlqodyxt7CFBf02LAEWhBAdC3VCZQBcVVJFDVrgsimW/VP/Qwy8bK3RYXnW'
        b'Hrr1tjwTw96udZb9xUtiqykIdPB3QmfDmf2JfBASuHE05cA6hwpkM3AjnFBcs7A0UBEZpvWXLV9GuVh+EfV8jL21Q/Sh9kBqcP4q6rOopPivogoT/KPxGEnkuQP2Utfp'
        b'YrkojbyVitrh8INkW6wGwAkm3A7GujWRm1DNUJTXw/ikUZ/D4DyDCB4RTAffZvcdmrGnHXdQhYrp2IOrqPKRjNJ4LKrUY9Fa11gcQw5BH2E84kSY4CnuxTagn/pQAw62'
        b'Qztkd+Eha6t3yH6m30idTgL1fHZDw58dsKjC0zGYDNjW4aazoXChXEgnRodQ6I4MoCNZPFpuzqMzkC2lJjunsMUB9AWxEuqn8Khti7OiuqjJQDUV33T85R+bEnzXB0YH'
        b'Rm/8oDEu/R8bEjYkJCb4rw+ODo7mvx+2yWajTdjyT90MpqR0ctyTvkY7j4/SHK/2tt7rhzvQtjpVOHR2lrWJsYV4m7XuzmLdIzygU3pt13twb5jr7Y0fLPQL6npy/w8Q'
        b'yP+JhQAv6K6xr/AqYhmJ+Lbly6jPpM14Im+IN4m/jRf1wd8J4FyIF3VygpAA1za7KHWqv/p030lQN6Av+/mG0E7TudrbDzhloU4iPYu7HpZ0kuoYvV30wQMY03Xm9z8u'
        b'6OgUs8i/gfutODhcccrrXQMV+fiNBf4B0SbxK9NuP4+3DTnvEHOxR5gcsJfS43v9W6njAMWR+cTo3zpJeuP1Nut7+rdOPTn9R9r1EU9e8bDPPBEpUhHj/PbbLzlGfxb1'
        b'zEcXYlY/1l52ooYckZpy434Vffd5K96tyPHnTLgAVVDkROxK4nk8OpaIOqDLj06L9LHQ/kiTAuVHauaFXxA1jqF8uLCEHGihNlN5kLOEk0K3gMrJeYieTp3wwBnjMtAa'
        b'wBx89XYqSW+S3k59+090ao8rMTfgHHSEpgMIP7SaJdaEKikaRwRh3yAq9/RxR9hnsG8YPR+13Td834j4EdozUtlfPyMlXjpWA8aDUzA9mzNzj6CHd/TgDp2HE4IZKmGy'
        b'KmWY2AXZcFqmhI7p0dBhTg576BmUBTolQNecQelE91oBV+ACPYTyxftpCGp2wkJHFjmN0nsSBXu3yPB46tgml9BiQMsytEcFnVwUnMJ/lXGoGMqM6JFQ4MwYaEuXQBfU'
        b'kXNZDpUPgy760lpow8IRdBqg43jEQgeHTqDrg+nG7ea2S5XGoyuonpw/cGgvFATT1CZBN2qTqcRO4fjGRQ7LdR3oHL0zDurQPlWmkElLUEHOniqt6EmVzw5ymMtZpKzZ'
        b'6lTpN52jiOGoDZ0aQY7mxFAHBwg/CYcOQB4qoYnFbIMGUp1NUKKuDrpoRU8KjeEUKqSN1a99oCVNCe1h06DA15GcCbATuzJ0yGgnKkIttMZRqBE6p0DZFDcxx6dOx60B'
        b'Wakj0olCDRdnZvY6LEZ7UPFSXw2QzdIly6B6in+YIRcBhyTQMQYVpxPl28oASqcIQICE3Dn3iMn0w9nmI6BSNRYPa1fOFU6bJP56//79MUvJaR1nV+YQa/LH+HSOct1C'
        b'24zAAG0ekO9LGddLXP0j7HEtPAQoDrOXw/5lvn5E6CoOotJWKKmXJMl0DcpHR2kyK2eEkNOH3o9F+uL2rSQ1gQLXEHUL9T7/JmPoHOo2gUtQgXLT15Ie6Rg9zhS/UG6K'
        b'stykBpAVAXUSKA03XWRpK50dirrRddxVF30SthjFD001hmuSTCkqNAoxQS2Qk2IJp9zg+nb5aMif5QKHJejgQjlqmzMVamzQIRE6kE4cGiZ4wkkDPCOyTTl3qZIcnbdE'
        b'oEsroVqClb59qNoB5cJ12I9Kw4crduG+yhqOrm8cOxxdxv2fhzrjt0OuyN0el6JkNLR6Dw4y9aOrBx1lt3fb8lMFTvryxh1rZJtXM75eVGIR0YuuF+rDtYy99mqTfoSa'
        b'tJcqKxfgsmy9YThNMN3PjyvDU+HlqMSNLy8Zy6WH0C7bPpvUoMaIszPBF5FrN6EKwsEKJ3h3tAdOz5qC+6IyCk/OZjgcMSkInYT6lbjEWUPC0Z44lJ8Ax+GK4QZ0zWIr'
        b'FDoxP4t6tNdQW8qotb1ohX2d/Q0shxCvHdQkx//JrDpnBJdF6Ey4nKfnySgLrqNjZACg/biP9rhCqZ8TXipwDw+Vit2G+1K9bTE6mxGgg3kYNaCL+tiHC+UmikR0Pp3I'
        b'5GtDIK/nsBtXdI/6wFvfaXce1OEC0kO84g3oONEfeE5ApajakF8Ix0enEzssalpp5OiLm6+Y7ICbUQOeBK7+fs6hzLlkgDeDL1YxU8jcXxLqHClwW8PNt6Kj89OJ+YyP'
        b'hb3MwcBvqdrTRK2e+gaG0Nq6LJVmQOdSX/+gYCfn4AjG2kz8GjauUHs20KUZikMHodOoFjXRURCSKlCF221FXOKbhmvwBqtevpbMDlCfPkEjasP7cIuA8kfz6UvJ3Tw4'
        b'EBYWIg9iRCsRyyDfuZfnjDc6Q+vH4VF/FvdfAaqA4tV2WFW+gk75jkE3fcdMQRfFhBYn2xLVoPqF6XY4VXu4Qciuoc3cSAqXzKEtLTWd56xUkRGiEDyqspgzx1kfkzCy'
        b'WIk4HksJJ6GZg2bUMo5SMC1BOc4BcmeqsAejXA4Xzb6vyCHi1thJcfd2oAZGb3piKBSGoZJwKIkI4tEJOMwZOPDoMKozZ9ldglZ0UpZhhrd5rBYeQjfwujIeHWGsEIV4'
        b't9iHS9yugjZDThg0Hc7zzqPQYfkgusugYulUKArkUc5KjvfkcC/keNNUU1baBfSc/8mGLVgpwIVIVElvjpiEW0FzXI2alfTEWoxymANE9mZBc+QLR1AL7wpZTvS1DLge'
        b'z7wpDDgxrmr5KB6dHAXnaEk3p+3UeKegs2LOZGOghWgIuobrQc9xG6KVePDLqQ2B8A6QU1qSzhzUORFlGcSPcqaNFYfKg7XrOR9niQfFIQFV400yW42ORvRmR+1Zosla'
        b'dClBZL4G9tPmGGuVquZcgDNwgfAurB3DBls9lKPTUOQcDPvJgeqaeQuFIXglKKYEVSuhWwFFLv5BIvxi7dDpPGqCdjhP763wQVfJtMe38Op9Ele5HvDYZqlWQA7sY8zg'
        b'nHgmlBJmcDiMjlHnmWUBgZqCzkU5eByTKW7AjUGVBkbTBtEtE1XDJWINonYAVOCKyrfqaqRglG0IZeioIRswV7fATUcXPye5s2TCLM5ohoAnWxeUKH6QvsipdmPB6ZJL'
        b'hU9Yd9Lb8yyuzRolL7SMW+UauuuJ78eFnMr42Nz3yCflY31DJU3WZvP4PfONLpRmDRr7uEMWVy1fXTa3bOaxQVd8j7reMbzyt3f8go0/T0pIiE/+pbQ2/mTFeL/Xz1o0'
        b'T5nWPfGlfMfym4e2n5rxwo9Lqr5vG3+zLP83J7v5jw+dZpkn3N/90bC4awUH17VdsO145tkti9Cnt+w3BobP8RiVN/hXuKy41uF4z8ne4WPvj97Pvvzm+7fH/dzWUhVR'
        b'eavDaeqTi+DL9z5zOHnlwGvzfY51P+U6wWDw0ft7tz33meEbJsEr3pb/5tA56l9eNm9Pb/vgqxTU/U73ktMrn/2ttrvW09X8FZt3Rj7tP6dx7PLx77jNly9T/jyq5sIL'
        b'gWFmzcJXHrVW/E/Wz4aHXZQGLnmyo3Fmh/1jLds/W3WgKH3N6bmvvLwz743HIj5fmWk780fJhg9fnn5ylf2t+8q55QFvzPDsVHh3B3wcvKPo+brnnsj/xrMuec1bbe/y'
        b'73+65VXV4c0Xw3d13jjxk0vY8nXfR3au/yUq7fMoo8QMycfjis53vJp/L2K/2Sa5weKXryHxuPdczv8xLtMp418Hnkr57NVXQp1PKt53X1Ra/kNZ6ktFz0QH7XNf/Dr3'
        b'6taovdZH331+X9pXwd2GF5+44R64YM0fxwfP7Pg2ZzAeUrYN2Tu2xd37Na9tzntpngt+e/qCj+e7728pvnNzlf+o4x+O8mqKayp6+ae7aScj184Zv3TqW2eC1zn9psg/'
        b'fO8t3uLZUWc3ZEpmjTz6VsGIDz3i3xcvuTH9yj9lW1Z/OGS1b1p5/OKJH3UqlF/dOOjuVf/pc0nRU56unjrmPdVz7ZHvfTXc0W3cqKo6n7ODc3aeP+Xm/Ny0D662jIw8'
        b'0xB9Julk5sl/fe56f4vE9qOF8gn0aD8CtWIBq6i3S8Z0yCZeGfiTCuZjchWqR6odauCYOz8fWqCe8ZldhxsLtMtQKSrBy1AFnKWes5KdKYR2BI/5in7+PFCRRF1b1mCR'
        b'7LDGGQ7LYQacFHXgLE750Ns+aN+m3qvjBMgly+NmdI06YMSbwRHt8rjal66OeF9hDjd4yYvCSmmPo1H+UuprlAHnaMHHQI1JD1cK3pguCKNgjyG9h3K9Vzs6uMix2MJN'
        b'g0bOaAWeuiaxzEfpHFShA46ExK/ACa9QeJ8/YC0448Uhl5ZZZBwVgDeyY738JAjLzTp0lZLTwDWUN4o4hhAhJsQvKAwd1UiyEm50AFYRJuMCMvcS6DZxZIXA2TTjXroo'
        b'TOHdaIeMQ3v4Ho6dMetwAZrNqe0YZZlYqVCJNNUULqmIK6A58/jxglO9nX6gQ4JuoILl1DNiKha69vXYPZNQNbULW/qJ0HFc0mz6UBze6gsCNLbokJV45SW9Pgj2ibAK'
        b'1rmItU7OmHmoyB91ueLOdqbki4aceYhoQ9Bi6lRjIvV3DHHCu2URvSMbhHvwhkBcMBEjCcJ7ykU4qZE3THaqpQ04DMVsJFZPQGXqvSPaguwca9AVOtqwYFo+SON8lra9'
        b'l/sZOraZdWsb5Bgxfx3qrGM/TBgaCe3UASUkmPA/6jJUaH1PDFApcT9BN6GR8fi0xWDdqa/PE/N3MoZacWbqEsqIh3WP8jk9bjhLJCFsOGu9cOQoj9X85vhUR9Ri5yL3'
        b'19AGmUOWKBnl7Wb2kAJUh/fXoiDCl0fqL1OGJQlwxArPBqoYn5q0VrPFoavLyRaHak1pxaNQLbHQqCUCI3SGCAQT4xntX5l8Vx+BAA6ZYInAfxkt/YZ4Y53igDmUU3EA'
        b'4WSZq1LTDC9cNmc31KxxeMJtbA17xZZwbngaCaZBnag+6NEtpKjW2hgdw816knb8KCxc1QUE+uElKBSLK1d5B+hMoLULgAZjDR+g7XLCCChstUBVcpN/x11HPuI/iGT7'
        b'53/0WPTN++F2UoPXR/jHAIPXZGLMlVL2GgvKoiS5L5BvQfIH/RaZCCQAiQDgMdg6a/wseVLghftiEYHFI5jqYl5C+G8oSLIZ+8bpkitLfEUcjywpRaEFcUDCaZioqQnx'
        b'b3zH+L5YMFG7NJmRv0TElclYkAoEh5d89eD2CjgVgf5mXxJe+EZiTRh4TNQpspBFrWGtX1MwsyDzYWL+RTQEzZE6FFH3pbgtPS4OPVFdPWcbQ/7XelQu7VVCL00JlXu1'
        b'hXLUukFRW2Qe/tNBry3yzQUPoF58UJPJeRriFvyQU1dy7spTnOI/d+rKED3FH7wl6HBbmB+fRugVoxMTKSJrL2ZjXEgFKV10Yh+gVgbuFRvL0Auj7ZLiMgckypxi7KOi'
        b'lmxO80uKj4qyi0lMXr9J7qIG1dU4QqSr4uLTE4k3wtbkdLvMaMb5GKsgNI0DWZd7F0KRRB+Mp5gD6vjSOBULOmWIinYEG8pOEat6dEZFApUw086POiTg0alSEOBanA9x'
        b'Toi2W5+uSkvezJLVVs0vNipKTqB19Ppw4PbRtAe5VCTZZXi4EHLvBbgZM0ljpm2ITtOWtsdNRGeK6rpRNF3q98ScMXACBFu3TxNpwncTlMnpKRRyT2eKuOppivXpidFK'
        b'5m6iSolbr0WAUNnZkyB6J9wEOFsK0LI1Bf8Zl7beRU47QY+7CWnQtDhNv6j7nbqlJfWnzlT3fmwyDR5OITjMutLs0wEPoZ7kOV3Uk8bBVO1duxpdojb0jbPU4S9u9syA'
        b'TuQJG3RiWr9YiWh0QxsuMdo3nURee8ABlK+2LNpJRcR22ZXqBlW2o3wHT0jdCRdDUR46vxBVrVrgl4a13BOoReoV7DQSVaCLUAsnoNYbdY/ehs5auMHVdGr4KTTz5crc'
        b'bmI5Icr/6qoNHI0D8kpyo6p2GCGk3k/CbUgokyE3dqM40xHOOaDj9N18QzEnjcIL2LyoxE3hRpziy2N/E6lIDOKp++sm/O26aY6blc8H9+pe+JYbNlb2cotBuGLDBfvA'
        b'wTPsh0x9+VpidLLt+K76kKen2hnlHU43fHeva0yy7dQ5yxbvrt59u2qhybH3VjtMXlBztni0SWr7cyHRrb96Xpj23L3RP+y4KX21yf0nqfM5s8KmCZKpP4zOHzv85OZ6'
        b'uYwJg82o0Qi1EH/f/q7mW1ekkfOh+YFBASFY+O5SRwm4zaNOzFjUvOH5KELK8JQeJ+YT86gM5OgOp1XExOpsrzExDYIyURycRC3zrRnv8F7DOVp9hyo7IwZlQKUHE8Vu'
        b'oLxM5n1fNUzjfQ/HsaZFqZvRtUHE8T5rlsb3HotB+Sx4oDQe1RJ1YNZibeBBliEVuJM2ocO9uR+FRUOZCuaOctLIsc328K1qGRbqlvQVY8WZ0kDqW2LlsbKfI7lWfk3L'
        b'gGwL1Kk+jHuo34gRiQWkU5PKLQ665JbdnCeVVgim/338U0SkEiKN9PMS0CbVlwXSpe+WPoC6UmBP9Gyt+fjPerK1uujaWrO49x8Q6qinRMSlFO8w6/AW0wdHQRNJq88Z'
        b'UZQveqQ4Ws2++qtYx74aFpekxlntC+aermL7bBxd6fCy7LPAb2FYL4B2fZtTXIxivWrd+kQFToVR/mqQqeIJ0uT6DS70CRcf8nMhfUwf7nuvVNXtM5O6LjppfRcJLrEq'
        b'jhYzWRlLPsDLvs5lWY1jr7cMLosiAqMoNl16SmJydKym9poG0ZkoAT/VYs2RHUPt3atKV6QxNHltoXRvFg8t1cKF4VFOf/XViL/8qt+Sv/rq/OUr/3Ku3t5//dUFf/XV'
        b'5T6T//qrU6Ls9IhUj/DyVD3eo37xjN2GCThxsU52Durh79DHBbWvjyx1k9MtkejzfF2kjKYQ3z1j+M84uS4jMixbFTKmuLj1mS3UOZcB67LphDPMUET/tZZaEB6howg9'
        b'lOBkjWHlYNNNEfsQsUvM9eKq1YpdgxnjtzSBncq7RcYYxU92ZqHG6JAjNKlQPeTK8O4BxzlUA6el1HDPozrUBG1ubm4GnABdXn4c1EE2OkPfk0E7dDkG4z0EXTIT0AE+'
        b'AG5CFzuRKUM5cNAx2F/g1mYIaA/vCXme9HACtaJSaHYM9uPJSVeTgPL52dvQcbmYHk/YoGZnetgFlww4EbqALtjyXlCFLrNzqZOo0grfbkmDy3jfR/tQFlTzYyALXacF'
        b'mg15cEY1Ge+B6CB08skcumyAKtipVKcjylVBp7mSVKQMGqGBd4Az0MHOpPajOtNZcBgq2QE+alL7N8BhHkpUKegKkT2ZT4LSXC6w6PFmlI9u9iptGdqHSzsK7aVNFxuK'
        b'snvKOhFLU7ioWCKlrTABzsIxTXGcoIuUZgJqpHlaYkm3ldUiZxqtRALKk4toDTeumd4rw1MxOL80VEuT3OI8tic7F9RAskNFqcxT5ALOr0GWYYQHhAjtlRjxrnB9Ka16'
        b'oieUy0wJ/IxoeJwTPxdK4AQ7s7kOnVgobIN2mRnPiaITTPi56AicTifQianEKTeAyMFhxPM3I4CeEGPRmMMSXsUOLHcXQy4WyqpQbTj+owquwSmowEJ3FbpmaQDVMQam'
        b'+EcQyoPi2XaDsfBoaY4a0d4oxaCMerGKoHOeHTkm4uXrweBmYXinW3W3fFeDz9knnnoi7I71ii1ZYXtPfR81//XHo7mIycNF43LavrPIL6ipMbwtP/TrpM9f/ttz/8rc'
        b'fSzO0KUpdsLHOatDg+ZXffPsmq2hTR+t2OM5vNFqWnVq5ODmbLP0Hw94D74SaHvhrba3v/A0axm9zUU8MfufjSduiQvXu743taLy92/OdF3/fUH1ybuJCZ/FLv5myLNT'
        b'U2BG+nSfX0ZOn9E67CvR9K9fmJM28+nP14VP+SXnvd8Onbni2ZDU/drJiqHK3Xc+fvaJCVVrJC+8+O3etQuXfXp5YfLxL9d+6zJ1tPem99/J8BoSvzDkt/ybz8ud/+DL'
        b'Jq159t6vcisWX3smDDX2tvavFKxxB14g45/KzjFYNj2stfcnr2Dxu507qOwcjmdhhWMvB2kTJ5HNNENDa2Yb7faHs8zPvAKdJOI+ugq19FakNUMcIGeRbbYol4ccIyii'
        b'pnwomzivV9Qt7t0rJPI2Hm6y2zdQ8wK1MO+MaoI0hxfZC2iJxm6ERkdyBOCHCsyxsCyFIgFlo45gmq3CGRpVMujAy0gJauChiIPGlUtYYVuGj0dFKdMELgYqediHyzEX'
        b'sqmpcwnqSiG3JBxc3M6TgVeOR9MN+touOO1F7vFciAMPBaSm7ZBFSxoyybMnknUeNPqKORrJOiGFBkyjOkcXFTnXnpDJowYOjqyCVhYOnINaVCRiN1/g8Jyo4vFaAO3z'
        b'cP0H0+mc5YFfM+BCp/DoDAe1a71ocjFKfzzJ8YI7ezqPLnBwdCQ0MPt7AXSgZlVGKq508yAeHeKg2Bwdoi/Nhavz8R2B2wD5PDrAQaHlKKqfWIxCZ7FSBVd9+utVWL3r'
        b'WKUnaPMBLtFiFZaPqfYRpVv7iCLaBrFWUv0Df4upBZVZPwWqiWi+TGhQpbGgsU9qv/Eb+Nn7wv1tg/p6NuO8gzXQLDTW0qS3dK0s6KO8UIdEXJdircJSoA2JLMJXjz9A'
        b'a3n8Ad7WA8uE9Teip9BQsGD50H6AWLfE60L8gm/J1i2MCA31CV7o5xPGkES1QFm3ZCnRiiRNrCQJ4bxl3CuYkJo6tWGkvSI+9/QF1KL4Wnm8WimjdWSNZfv/kg1euZho'
        b'jCQcNYZIF4YWIjIWpL9LJGYGNvOIjV0s/EVAT7GFhYVgRljmxNz96VulvNVIKU9dYibBUWjtG6yAWhPwOmm7WKyAtkEDHHtN1L9VDnxf1jkCA8YgwGrFahAwdk2gwIzw'
        b'F7kmkGAEEIx93nNtQQA5YwfTa6vYIdpr69ih+NqGXg+LtY0dHjuiVkb47PZJ4vnYkbGjcqUEELTKsIqPlVWZVEmrLMlX7OgSw1j3fQRiTIK14PGxEyhcliHlgZuUy8Xa'
        b'x8oJzx15r0pWJcQL+K3B+NuiylLB/rLEqVlWGVUZx4tjHWIdcXqTCXwZSXGf0T7TfZb7rOKlFPCLpGxEPWkl1LN2ULwk1jXWLVdKAEjF3EoZDQ2YcsuSTI+FlAuDIsbF'
        b'xynvTu4jfw58QE3j1vuhuy5YmJ2pUCXPVKXF0t+T3dwmT55JZOKZW1SxM8mUcXFzc8ffWNqeIhfdEgeHhAbdEvv6Lfa9JY4IXbykib8lePvgn0Yky3UhwYErmsRKYkK4'
        b'ZUB10FtGDDRYgS8N4rEmrfoz2bqTbMXKKjLPqsmPA2Tmiv2CwxiM5J9MawZe1PqmpTxOEwzzjpx/d8GGtLSUma6umZmZLirFFmeiHShJvKzzenWcocv65M2usXGu/Uro'
        b'gnUIt8kuOD+50JN+k0BRy5TrCDIjbqDAkIXzA9dhpeHuRFLohQv8aAnx7yXRW8lCF0oMyao0nKiL21T8E695JLEmXhnEwB0Pk7KahPkFLw70WbdgfvhC30dMyh2v0VV9'
        b'qnzXo9+LC5XJKtUCqs30TSMwOSFIlUBTcicpCT0p4QI2krTM+7XHXVv9lbo7RGfjyWV9UiHDTXlOR9ozlOfJp/0SmUETmaJsJvf0Z+5+1/FP1PSWYWxcfHR6YhptftqX'
        b'/5GoB53BPrqiSageMnYU1MgyvFE3c/Mj7h4noxTvPXebp2Emnx/3C4jOeNkkXhNmUrX9AWEmt6SERzYNj2z90VfkazEDfu27orho3tUfoNCOq+GFr1RuumWALO7JBwQp'
        b'PCjPJkO2Zyt0bNybtLs3GamfkzKFBw8IazDWtLA/pw5r4DR0pwzYLd5YG7Jg/EghC5oY6D2GOoyefiwWWbEtrpfpk/EZsbMpskY/wNQZpiEetkuh7BJUkFHNHPigs12/'
        b'eWRn7+0jf/BjZB4+9IkZdvYOKgU56MrwcJnu8AhJsqltZ7/Q9+EPq6cwedjJ7mH56F9e7Oz9wv/UG+4PeONRVwqSRP9C67Mqqy1jzITEwsTVTFYalgR9b5LtlL3Wf9ik'
        b'KBXJSkXaVoZFbO9ANmnCEUa2aQfdhkYHsnmTZ8hW6kCsyg5kD3SQu/ScxU53meziNlP9iO5keo5t3eij6lR7Pp5OP2ZJ66sYg7ZQV00HcAVrn0kqil2ht3noucbMvjgD'
        b'dJLphqFQ4wToLVMP1sRMLSvuQDgJAu2gPbnXcTBP/uF7lNCQGPqpgZV6DcRFp5EBpdLQvfVC5yDn1nrACoiRFqeTGa1UOxn0YtmgrWMXFhdH6pqe2ItBTmdSC+eH+ywO'
        b'CV2xjtAZhYT5rCNMNmG0lNoDfsZrp7eR2CLE2ocyT6nBXjT9plHg1OZl3efhPSZneozBUuixCDv0W1Mc9HoU0B5KYfNUxVjx+i0xDqx2mkcUSbqRFBhuBxZYNSS/G6KT'
        b'7HwiQvWYzpPswjIVadvilIm049IeUHi2IOqZS3jC+KVFJ26lL+pf4Rz0j1k14AjrkB4cEjLy1V2ixSRhp1h6apTGHCR6gZX3ebcPnozeVYumNOBYATePWqpSaYZvv3R1'
        b'94maKLInX0rQGROXmJyUQFJ6iPmdSChGA0Qq82BmUy1D7TMI1EMplIk470gB6nn7yVDEzPAn4dCMnrhCIcjOzB4VMKcIIo+lWUerTOEU6tBCoWZCLlWIjdEZKCcKMSqG'
        b'y0Ag4QrE+MNzppArQFFiXDrhIx0VhtoCegeDwSW4Gjkg2qYvcGiQgb/ATUM5ZpCL2oLlAqvF/uEoT2MYng45IhN+LnGvpfZkOAQVmcygjG6Yipz4ubvjaHiMyQyccQ86'
        b'bE9JtGEyKaamoQQf1p4E6pyH8/b2UAjFrgQjsSlcjTzrLMF1PziY94TiRbRVLOCCjypjYVAPiqk7ukDPOuosJNztLaM4zi7KSTluEEdDorzhgnlvYFNfF/8gKMA1dg2F'
        b'/MClvqJQVEDi51AJB1fR6a0TOHRTLINDqNBCYfU3Y7HqOE7kzjDPCSXuxmiehU9CfOVXSRUrW37y79zzgp3l/NjBoRMsTNDlH6TPDlEuyOwYtuXbH+6nifcciYuWzja2'
        b'iW15Ztlzr3h83/m3Fq+SgucrmhpXxH3kezXeY/DEFyQ1ht/Ia7sWFMVGu16qrzlmcrF12Cj31Du7PZbMato36+3308s93nxy01Xlr++YlzWE//2LCfd+bC383bmr690P'
        b'/Y9aV5V+dHGd2zNuRgFxclNqSAyeFOno4swco08JqG2E26C11DvDC7LGqpGYi4ljeAFBYjYLNbYVuUNOGLN3XtwY0eOdAcfQOWrRneNBDdQj4exy29kDHUpQPiqmBlEo'
        b'H2kREJIOzWqXElTmzjx7zy+DhoA+DuFD4aYocTZcpAnbG2+nLhqJNn295FE1lFH77YrE8X2QCM1QI9wwFnk7KKhPOaqBsggKmtjtpBvTEK4xtxhXdAadJiEp6DDK7QtE'
        b'OURMbbQTxsdrTOzj4LIaI/OEnAFRtqJr0IkzItOtXUTOmw6JgvhF09KpR80a29l4jictDcS1j+Hd4fzkPigVxv+WyU2LmTdPnxK1w5IY3kTM5ZXgj4h56X2JQH4LxI2E'
        b'sjWbCQJvq0f1UaPDqQFyEnhdZuTEPpB0QQ/UvTpG/Und689SvTTxtwzWUYQ+fdhZJfiKgdPpylDLEu3yCFJvf2A5Yq0K850fektMOGBviQkdrNxQl9stc2olPq63DNWs'
        b'4cpuXkckvLlmBwnntJHwTGk0UauNpgwRfJ95vPmfjHfXeMw06lIe58fGqvpyX2s2Tx2GPq3YNVAHjbebSYTCmVFaAJMoHcf7TmohRovFRZwoB/qc9udxZDTGRD/vEU3T'
        b'SGumqQX3R1KJ1MKslun3YVoRI/pi7+qg441W2cUnJkcTk4Ed5Z1VE2vq862JTupDYtefxVdfKfqoCrpIdtPitjA5OE3LS7uZOYDq8ejEzyhiiRDX0xQ9VICsDnb2lJ+e'
        b'VI0KaWNDF7m4uIyV6xEvmYcE9U6OJqOpFzu1NmVGv8nE3p77OtPTvtPDpqkeAmrvrb7cmjrTsA/1WeRDDmx81gVHBC3wCXWy02gjjIBUr8cXdUfWT0SbnMLcsx+QwhZd'
        b'Cp4extcHJEf+afU/0sIPUs+0+HDqUa0zNQ29uC5Nzg63ik9o8PzAgVqbbg/mR9TkNJRgrCm0xMxkwKrHDZkXWPmNo9zbUVHByUlkpXiAa/eWtJ7cKW0vaaPoROJOTRYI'
        b'7dCNVyZvxk0VG63HBzsxnRnMEhQZcUmakY+nZizx9LFfn5ykUuDmIinhhlPQT3Er6y0YS6a3mUHeu5pqmuqYjXHr09h6oFuxCQvxnO7mbseIc1l9SBmc1Aij6vpSvZ/M'
        b'Tbwo6kwnPl1J5xqd7YwAV692x3ammXZham1KQ1tPvNS34lwSE/Hki1YynYo9rHttUamS1ytoJ2h1uxRlMmGfJ62Im1bd2XgisGGvuzF7kTraBWMtLzolJVGxnvogEjWb'
        b'zqfeXve6585CtmZE95DIkk3bzh7/lDvZka3bzj4kIlROOoNs4Xb2C3yC9cxDh15hBNPlDo8Q3KB16JqvXer78TA9yFG0j4op1alijg6mbkCZ7tCmUSItUQ0llriIGAIU'
        b'VYtsoiWcCTdZTNSi1GkWHPPKOq5ArYxkA+uSOVS7hNz1i6hKl2bgoqL+Ty5wjrpAiVAnY7E4uhntpXAuxFt8KkNz6UDXwxlGRaNYtQTt7a+XMqUUDsO59CCSRgkPnVCk'
        b'Jn4g1CDhanSCAGeHSF8n/4ge5XQb5PbXTxngy0WfQagIl5Gpp4fQZdSs1k+xEneFIwqqe0J6BL7pgPJNxzg+Yn6azHqIdZbaa4Er5BJuppsVtKBqBVXfPWEPnKaK7xy4'
        b'xBHFF9f6UHomvrXefEsARfNx9g8hyi9LxAAqIA/r8zeNJwxDTcZM7yRK5zzIhlp886QlykOnwtHx2KWoYMEurKjsQefwVz3+vXfTFlSGGhbErEWFC5SKpUs3rlVOWI1q'
        b'Nm2w4KDUawSqtZlHexZuoOuTZNCZYiLEQTUnwDXeFSpTKHyGF+qazAqGC3JsYOGMoWAYKpiHymOwvt+7RHlwEqrINXH1ijKHfXYcal46yGbrEJbnHlwR5m4GuTGcyIh3'
        b'xYWuTo8lvXPCDzq0dgB5pBq3JyU9PRzKUkzNoSJc3eq9TATEMkC6RoPxoYG4QdmoUUq92sygFuuz+dZwfgLan04itZZDl9AHX0mDHeQHezXwQeTd8D5diofvPtPFEcvT'
        b'fUhZz20zDVDTK8FVb4pxWYKal9BRg5MNoKAjeChVGqj8UaElHuCFUBmKVetCHm6mmi6GRnSEhqpARTSuSW+mJpKOL1VP4TQUUhU1sk+SKE+GqqwmQMMQoqlaD8FKZk0Q'
        b'ASnJTqQsMDirvQT+aQAokgAnoArn1D4bd9AeyMXtS/3uUEUMB/tCUUeoSagXHKPlQrnGm3oZZQL95P7OLhpalD5AS+pSmfadMLjBjsIRdCzdEpUrTdOX4SQ9dpLQXIYP'
        b'sdRXT9pwA64/Wvqh/lZY1b6iUtPmoCuoRU1Zo0AV1N6DrkRTjx226NR7oSxHX8bXg5oD+1L2LIAzhBdSEfEUJ6gasOJ1btkHQUuvB78zz+K9kduv35h1L0vkwp+0qprt'
        b'XZdV+OMMo5I9sQGLY0X+rUmeY0zDf5Fm7DbYb3HaP29LVtWkUfzST972Gnf6u+d/mfLPmhXD/J02zv8p3OpS87xd39YnFUwLW1wiFBYeGrI4M+24rfP9cXs2rlR2vRo0'
        b'PvWEZ8YrmV2vvD7jyMS63RmHKyvOHit98+4z8jdfUyyeMK3Ve/Pfm577uMGy+IPsMI+zK2eEXbzg9O1t81fmHj2bd+P1ZySzF+xP2HDzRFx2x0+V479uCfslY5f17Bmz'
        b'k+9ce2yK2ShYFRd+XUjePnuu0Y2jFQe6ZmZI3jdq97uz6MkNTV+uv/3uHxe/nSX/dVTWlMg3bLd+ULw4zur7lkmXVClX97ssOibs/PnunGFHvnwZ/iX79MQ3/N0bb/xu'
        b'9dPM15oh/VrXN2e25m66FeIhuS9Llf02+s7ou98M/zj5mWude39ufePvGUfMZ8794cihiTVP73hz/LJZwub5X3vfUU6uCJfErPn7W08VpmZ0vr1s1ImKs2GBvq8f/EW2'
        b'fZFy2OXtI9cafrPz5uDdqLrx7icetR9Hf2r6A7y/8cCMexGmLn/w05MuWVnFyK2p0cUdr33dfYxHHjMiRYlwwJPajlySnftapKCUp9ANR6GMGqUGDYMqhtyA8lyIUepI'
        b'MrN1nV8ER3u7WyrcCLaCahEz9bTAtV1qQxB0h6rJUlAuOkZtac7ovLIPD4sp3o/q4DDhYVlrzoxeB1Id+uAvNEEeBWBIUlBTFLoShVpZZBI659vH7rUlhZXwHLrk1StY'
        b'aqWCGOOWwR4Gj9ANtQnMcxMVoAJOTF03TdPpqyMDUAVBzvVDzWIObsIxSaIwFm8KTTSUHNUlomo1ZgU6tGIt3huOB1BnQ3QVFS7tZ2o7BMeIrySUonZKIYLO26BKnfQh'
        b'o9Fpam1D5cAwKFDZMKjvE1yPl6YDFqIhqeoaVi/djW87oSYxnreXOLETj7rwxC9gMWwdqMqZGOsc1qEjfWx1HuqYeCyutJqrrZ32a4m9022bnJoE16ArcD0g0A8VuPZH'
        b'PXKDSyJ0ReK6Th3/X+kURkcQ3mpCsFhhNmG3t8jLFVUzH9eL0AHXaEyaO48FJsilQWk70D7m0XkJteLNu8g1yFkucAbokMRLsJN6y6WPHAZt/p/x0MvTQEFWENlRl7lw'
        b'NzfHmDcRaMS7YMKTWHkLQSKS8pYWJszzU0Ri3wkRB4uCJzHsxNNToo5mtxDZCDb4N/m2ptHxhJbDipcamJHYNUFtjhTMSDQ9L70vFswEFssuEbaN1WGO6xeaHfywcPYe'
        b'u5ryRt+Yt0dv/t5R6Dd0hKLriEIvI0ZPwgqm0+iZxX1vr9/s+QjV1u8DRCyu1BrIHEi4eInWG0j0yCD68XLx3agBmkZoXBJWclUPM/lR+4JapyEabbTKbnlQ4EMUl0H4'
        b'e9QAxcUpmHHO7Rs7LKDHoXNfCqEQ7ANbB0XL7AfAY2C577zpkM0ihtmVPRuq1bv/IWjqz9gHrZDLADzheBqVIvxRlvrUyB410iTwwlUNVeRm2ghocMFLsUsG/uFPgjzH'
        b'rzXwWApdTMuowDP+JMlBPAe1c/wocriXC+X05gwPdFR9zIfy0kQcPedDh6dTBeyVBRRczq3ZIMrp7fAAhoxpvQTqKUYlXvMaOY6HOg7dhEo4kk4aLRwdmw+VIizbk+gU'
        b'DudCDwxPmK+XGSkJMs1x/EYTXgRXo1MUanuXN9rvKHcIMp9uwIm38pBtbUxfGYpq8XpPkIi6R8iDDTiJtWDibktfcR7pHQYlYs57Aoc6OLTfHJUyYf6ASTzFlkMN6BjB'
        b'lyPYciZz0i3pJuERSlSeIQEc1XhCGK/iUtRCI0dIMArKQrl4AaJxOjXDWYonRqJ8dRgLHBxjwIlsea/wVSzg5gxcgTyiMy52FuNBzzuYowYm++X4YNWUanUpODWq1BE+'
        b'MwpcFrkMzoShkjGoA6oioASqI4J4ThrCQzveqo/QZo/wKOVG8JxvsFdU0k/bPJgyHGY9lvPGv7uNo4TfV4WxD8ulvgQDkpPERjkcDDPhBjA/a+ehHadmfrbGM487zu3g'
        b'Y7lYPk8Yxp3QcEATIvLPySkBYdCZH6sMVCTFNalZoMWJ+I/+NNbE9L9Goj6soICJWM6vEKgajbfaNHZgaaQRkaGCRlbwodNnwFXA2/8MyMuYtyg+1U+5Kwllj+R2TLZA'
        b'rRPhEK3ac+GmHG5Mad6qqMB/WmSy+r6RaM05cdwSK6eoHV+HTeUoF2H0ODyDKOygZVAf4EFRiM1k2o1ydDKIKpZon0xQK5bH4SrrrGpcmKv4bqop1kYqRJzIip9liK7Q'
        b'/Aan0yC05V86Rjm9t2MHJxfoADTZgZrJYEIH57HRNH4mG+YFMdBBlEnIRcViqk2aqo/MoXAbdEMbfmsr1Btyoom812DULuep2cIKzktVwVhOhEsbOEHG25lA0b/VlQm4'
        b'K5WPk20AkR9P8NwADnLSeee1nUcG9BRUDzdkGdBpzk0XSOE90WF3VvgsK1x0rLpshSw8pcjZZTHKZSh9najMF9pMoNMQGmLwnKskYfwd0EFnHZZEjqJuGbd5FZ5q3FKo'
        b'SGNt3orlGZm9g6MNnILWQDz+/YWVsFfCUjxjMBTaXP1RE4E7xTcNUA4PBxQbFGKj7wxUPnhBurbRLi4iYL9VhNWNy3W/H/5mb/beYXuH2TwV/ZjHOPNBT7/R2Fhfumfc'
        b'2JzCxU+Mrdl49tknDq1y2fDa5MdPxRS77z10dqS7y+orMYpi2a6cm1ktUZuX/3o07PVxoqK301/8ZWf6i+dVL1096lnwxhvXf/bx6bro+vkTsrT48uovl1d3mm7PmtXi'
        b'XA/1H7790SctJa8vaQ0atf6cw6InHjN61vODYctdPA/+9mbA1Ii7M38eLLNX7jpXXLoruNBpToQq6I/8PSdjHFLTT1c2Nu+JeCHCxaYtddp3n0R84fJ+6aaGA68rh7xR'
        b'kvCFYcRXa5pFio9GnIje8Sr3yZGN03NtgpoPNBl8vRpuzZu2Ncn7kw/CF087e6br7eOLLpQkNYbvq4zyeKWsKfM12wzuzfiNh/dGJZ3dLlvk/uqq2xdzP7S2Ohr6+4QW'
        b'59dmJhedv3T+w8svrXrmF4OO8pde3js5eOXGx/NuLpy1Z9rduda/+zt/tru+5OqLHbfh5HX+3en/+LvblLhPjiwpfjYs7u3nfNc//6nZtVSYdWP9V68V3rozaUn1yLeC'
        b'bz1R+NoXpe99nfOp/1cLcptu8896DQk8E/mrx8vv5sfmnTE4MiggbrvxfqvNf/zN9oOZrZ9UHN/+ZOhbOXmGQZ+6vBDhZm70g9shZwPRV+VjJ52zbb735fD0yFcjba+u'
        b'HvTJK1trM7/5xLp9f7RXaUfIobc6Di//YPPxEO5d8+LqHQcMS4K/3jDiH2OaJxVlbqjqHHJ1qWn39tCX4eUPmr+bZfhxmEHk9w6zJt9ZduW5uk+8lixNdv500y/Ci1Z/'
        b'CPFJX4d//Znx4q92bn6i4ev8jOrXXwmZ6pLhvEUy6IvPfh8TtvClVc/df+qFJ9xfuP3WjQajgtSc62GR7xS+7RgUmlq0s6ayc1jFi7vNvtzaPPSx5wN81uX+ZDn5nQ/W'
        b'xJgHv8l/P3nu46Pihm/dHL1r6qG1u6xVTtbbdpy/fPTOR13vZZyc8GPnq16PX79+oTKz+cOvN1RvvnPs1RcvHXza4p/77s18fdGTtXe2PbvuYO0vGz3/cCwwXvtk6TqZ'
        b'9UeZc4N2Jfi9fvSbucqfSwM/HvHmG9keOR6hHh/N2FJ57/DOGafjW/LDMhZeeG3V34dfWb+t8pClx62nE9baL72R8knSwe23n3nM9ZfvMoZtLj/jXfdqfsa5WkuPa05v'
        b'mqyaPSHvcpL/O3cOH9/+1ody+bX0sA/37v6+Sqp6qcpqxnPyVDgyeUL3Fv/cq9v9S00bvA+9dSnkrTl125Q/XG/7edrTAUlGz0cf//Z7o5Z1u34xetX/+mfbl38bnep6'
        b'bX+6/zen5Fsv5903eU387eJ5BxVdtY+92vDkAUXOVeG+6NX4uT91/br4mTlWIZ9eKZ/W8BHqkO2+PfF+/o6UhJY5i4aWfXW78olvhk67fe/Wl1bT3391l+LY9W8lR3y+'
        b'nngl484cn3V3Pzibavu900b4ddvH+Sff/Sx57sx5U5re9/LeLmkrDf6p3mfpMVHb+H8k7PjBbm1mFnx48fK/ht+zvv+9YkP1Fcn9gpU1/tYffXHobN09c8su78MlHvJN'
        b'FCYDcjfDaUrBsmNjHxIWxsASCTlUc10XsoNqtdugU4sCksHDVar0uQBeOYnSF4qK+zlooINUqVwKBwnXZ8lyywDtfXM3UQLsDVeTqDrZkz1z57Le/iJYgd1rRWkhXeCM'
        b'l1p95Zfq8BVJhRNUFw5A+6CCPEhwXisguzcVJ5QqmJngpAAnCBaiM6rVwCEKzlCjrswWrE9fUkHBDGMNkArPmcJN0Tx0GSopvpzHvHiVC87dWRksJ7t7GzUWHpbhWom4'
        b'qXBOEma9hObkja5CGVGlURMWMElCknWCA5Zb9zIElBISJhoQ6CDxhxZOWMN7QC00MSX7KJyg1gDX8bOwVE3KuF+Y4IGO09aahXfvVoIehzpQIxEpGH4cKkYsdHJHPMqS'
        b'4fphKbpqBBQHiDhDaBdCUtApaggZsQ724duoTkKeKA6ANrzLmKJ8LBhAlj91SEpI3USBdKbDVREnJpi1EglrvGLUtkGd9hFnZz+ctbGwDAvArP23QluyysEPSnfBwRQa'
        b'hLo/2JCzQC2iNMhCRbTa6+dPDPB3soWL+DGOM4DrggjazRmr53EsqneRY5FLITLUZE+AOiWcEVwmKLSFaD8twrJNShVBmDTC3YOuDzPgjKGUnFPUBNLaoYuoFZ3HRVw1'
        b'3dlIDi20/qbommgwHELdtAQ70Qkop2aYKBJCy+Jnl9C3x8JJVEV61NFlMmTJje0dUJOYs7QR4eLXS6n9wMkqUOYSQDb8djkU4QYwE1ZtgnMsDLYO9s1XBfMcaod2Kio0'
        b'oj0jaNNA/eax0IbrjFvuhohkgOtgwA2yFqEaN8QIS6HeCrIDCKOpn3cPp+lwtEeMGpR2dCJOjF6scokI8UMXTfADWEGSiOaiPKwD0bpfgBZUJ/N3DoSyyFR03hePUpWc'
        b'54aFixfbWKkhRM+hPPIZXIDDHNzAmgF0olo6rhzQ9YAAOf7zrBoZ2wDPwirRbEMoofdn4tFW7egyF8r6wT2GOdO08USMV/k5yI2hEgtQqIpHJXAJrwDU6lKHZ9tl3LJF'
        b'Bhwc9OZlHLo2DPYxk1OzP9RrzXpG6DANpIYLmXCYtuoMuD6FIUHuhhO4wwgS5Mz5bOE4jedyj7UK9qMWMUewIFNX0Ynkl2Ess8etkBooj0XlAh4rhwXUPRmdY3akq5Ph'
        b'HO4IrFyiziBnnjNyF9ChMNROm3oQqvSVucgd7LH22ErKLVUICqiMoxnvDnZ3xIpu+0pXFz+GvWyOSkQxeJQeZEaoE3AB7cF5j4PC1GAixZ3h4RicVyO94psnzGVyXN5T'
        b'W1mjGMAhHjrg7AiatxvKdmFWNnK8J2ZWtnlQQG+G4nbtxnMAnV2/DYvZUEBwo4tRI7MxHlqWHsBM+O6pEk7mz5h3D7MKl46CUyo/yF7iIFcGEkAIU1eRdDE6Qk1zlhZp'
        b'dC3Aa89NDq6Q4VQ6jvZeCLRbYr1CCe1wZjfWktENfvhuPOhImjKoQeeZ2dV0sZaiugG1MnPfFXQKKqh07w/7qXRvvZZagaEBKlIDXCAbneoLO4vVFZrpfDuUS4aTMtA1'
        b'3ofnjOcJuDWKfeiG4IVVjC4VQWSFNnQ8mkwnPCBJ4a3wKox3m0vhFO90CdqPmwpK5cZ42a1AF5zo/gWX8IPDLMQOGQmsN7KxCkUGZ0mQOdpL7xpE8lDoghroAEw0Jctk'
        b'YaAEa8mXKVs1nglHWHO3ogprcrazVJEBbbijBvFroQovNKTymxNTyS1JIKomAB0cXg8vJrN1tNGFaG2uUGCPCrfg2QJ1BMEjDx2lVU83G4kLbe+PLkZkOgicIaoUZqCG'
        b'SbTdtm5JJ36xcBhOhRCLSwExxXLmgig2IpIWaeZ0tF8DDr4MlRtwJgkic9i7Xb0Mhbmp8L41aZncn9i32fpog86J3eGGerfGw7AarpNVPmwH1U8M0BEyeItQKZuvB3YE'
        b'szVSjtvKm/QNdOAxIUN1bBU8jm74kV04kMfNX88Jkbzz2Ey6Qg2OmaPCXW0UBuegIBNf0fQHQ6UIHRu/mb191SeEgKLDVdQgopO9fgXWnKg9ojMKHSWW28wUYrslhlu8'
        b'WmWxewfRcaUs3dSIqE24Qcfw8/EifICeJ6DzQSIVFDvza6dwghU/Dp0IY0OwHg/Oc6QqijAsv6SSR/Bm3ySasCyOzeLcwREMMn4mGR14B2eY8Yts0yaR3WITHKdAZK5Q'
        b'GOQk9wtCBa7EZFMOewlEs+dsCd7hT06j0yTVAZ3Fz9o49FitvUVeY3CTUX6TbrwhH6IYyxq89oEQtssWGXARcEHqus2cLffFkC/I6HO70A3nVDxXCHxwuwjV78YtRrrK'
        b'KRI14Fzl6GDPqQkh64aO6XSsKMah03g4kDmWEY770UfApcwDtmZvRAfJ1JXL07DMhBf0AzwqHYIqactYoc5kPKuvQLVcs5JMExmhbpRPxUpvL29dGLyx3hyF4HXDixUd'
        b'jUWwdx2rgStu/FScF6lBpwj3SzfeFKmE2hSFztHx3IZyyJjui3aPSsYxTIwh0CEjT52FSxyeT5d51LiGCS3L0X4/GRRimQVVwh464KWcsBR1JDA5rAXVz5GRXWB/Ao/f'
        b'bMczcdwkVr46vMGUkSYQbIzxkGyjL1uhXBHkj0Ut1IUYTgWi4zI5x60J4m05yJOE07E1ezxqUQVDqyuqTMViBD1KsdgowhtE7jDa9CZhcBHanLAkWRZLFoAavKvBUTzF'
        b'SKK8TbTMP0jkA3WcIOdHGUIWLY8THN6hwos7dKVBgRGtEpu/UCaeabmW7bQNhAJQhuXjWrRf7o9lx1HC4ME2bOZehzw86QmRTrAJNDg7kAGNp+4BqRcb73uHQpvK1YE4'
        b'S8ApXzlZeq4JvoZY8CRJx+zAibc5Bys3MsvETh4vFI2BVG6e4jufYCm7wLnQfljK26CY7cUr4KLKxT9dbgQFKAvqsOQmCKhqyyhatF2mAXQi2hJWLnN7sqaZYulzxhw4'
        b'qwHC7nLT+HEH7sAbTRC/iE+g4irULEQHAlyCJKgxiBO28rOHo3J6wwevWhfxPhrID5FTB+/16o1wHLrpR81xClTp1wN0kr9cPug/A50rech9hmXBInAlSmrap2dBkcQO'
        b'pvssaDfnIKW4xQwH2Zi3pAgeBMfDiiIRkrMcKXUrl6qxkMm1Nb5rJdgSqvb7gsiat70vSG15ux8Ecwve4r5YMP5DEBPsZDN+vDCet8VXI+4KfwimBO3YBL9h+ZsgIdfj'
        b'Bcl9e97sdwG/b8GP4i3+EJ6TzDKm6MoULZlgJvMWvM3vgmQE/k1yE/Mj8E+bfwlGljgv8jf+1NQGl4Ugl9jfx2kZPCBvfHcEfpaky9CXpTgNK1weKU7R7GeJTPqj8KRJ'
        b'gAbnhBHQ2+GfE0nOvM0fAint78I9iZWU3zZMx8EOa/lefLMP67hekc1P4a4aIcF9Rhh59Bw0ZXGfWOs/atJfIlwMGmLfyZPA5eBguRj/oB7pTSb9gE+UGzkaxR220Ncn'
        b'yCeMQp3QqGuGfKLQwpWQ8ioJJyU7tLP6XwEkmaVtrnIyssm5XC7+LRXEEjWE9m9iw//Bq+clHgJvZi6lh5m4oe9beWlgS8igE/4Qi8ino3Zzxun2uCDDUDnWHglkST/z'
        b'vcDNXilBOagVCrEyemlAdL6x+rfK+MHQJaJYqfraqNe1Mb6WxZrQa1N8bab+3LzXtRrGpNZIC1FiFTukF0SJqBdEiXWJYexELUTJ8NgRWogSAmvCxY6OtfsTECVjSiSx'
        b'k7QAJabxBrFjY8fphCYhYCh9oUnsb5lT5B7Kxu0dF6NIu+s6AJek191/A5TEk0W3T5YLt8QLQ0J9bokWTF6gPEiGeQ35cYR/dHQQTxaeOflPQYqoX/L887AhmuxoNKg7'
        b'gQ1RnmLBPATgQ3maghOF+gSFhPtQuJDx/aA6wry9Q+NS+8aguynPkAo/yqPuWkwNTUHu2uhLVQu00bfMcqM+aZB+UL7WG61D0zjKf5AavU5u6cvDXdlGnvm/gLExkFDX'
        b'gDFJRkNRmhaVsAH2RPMOUO3FjocOjIYyGUEIw+pxEUU4q00erPg1dpBIRXTQ+EWfEF513+jvLz4f7/BhQLRx/Gfc93uGeb7KzdgkvuRlLuephDN5OGrVwLqh3Djo4iFn'
        b'AXTqIQ5t13iLEBlZr4RAvuzIbrnNpt88e0SoDktDdSvr3dDI150HQHboz7iD9O/zBI+DmFX/1/A4EuTiD8ZIHhWPI5aWnAAOkHCA/0kwDs00eQgYh2aaPfQJz0cG4+g7'
        b'c/WBcehbAB6AjqFzMut+/k+AYfQP/GIxCtFJJLyAxG/piUbSvqYLiXUAgEafflaDZpBNhAFh4I3EQX/g0MPQKjQl+TN4FYr4/0JV/P8DVaGZcTqQGsi/RwGM6DtpHxEw'
        b'QucE/i9cxF+AiyD/BsbyGASH0xgGOAW1g3TDFUAFlASqfef3x/n22OHQTXIOdxpVOyq2ef1TrCLYD+OMqwh3+We3N8SvfOzNx197/K3H//H4O4///fH3Hu8qO1o+Jq81'
        b'Z1xdU4686Oqbx3Mn5DXVtBa45405lD3FZIeIy+42ndZwT27AWBuqXaHM0cVZjI5qgAXc0E10nZrF4XDSbh24ApCNjovcsYqTy5x5s23TBsTwn0L5Im9zaGcorDkilEPt'
        b'K5yA9qyL4d0dMtlJ3j5b1NCbwwHKULuGSO8KOqTxE/13/GW14fX2D5OAFmnC7CW6xJE/H0Nv80hC0RcPiKXXW4pHCqRPkPPByiu8RljTEUS/wFDt2jQwJ20E/Vg9296A'
        b'qHnJgz151xv2myIyzTQJJGKbYT/BTUZEt3iZWnAzpIKbFAtuhlRwk1JhzXCXNKzXtVpw24AFt526BLcHx8L3Vi7/vwiE7wsOppaG1NHhm/H+QcJ0/xsb/9/YeLv/xsb/'
        b'Nzb+4bHxTnplpkS8E/TmTftTofIPWDL+N0Pl/6MB3iKdQqElMxmhAyu2BSwldL8aoDCzKSibwYQR4QFdWQN1zHEizBcKQpzRtfFqmC9ffyih3GXLCMwWiWIVkziGIiPU'
        b'JYtg0Q95UDm7T8T2MejsFbV9HA4yN/2swAksXBxKuUg4AedHQGH6FJLCxeneWjp0XTBf6EIsQfoSOFQJx4zg2ogV6UTc8MGJ9AThOaOLSyHf14lFfUC+lul13STp/InQ'
        b'QV/xsEbFAf0EYhJZ6wSlQYSgi0N77blQmSGudDm6SINMtgxGHVre2Igly5wjl5HwYP+gQNQU7ovO+6MW3yAXZ78gnJCrgC7JJqOi0DBuFKo1S4Ryjrpfh6ByJaXn4JO5'
        b'UFt02S6SVbwaXUA5/RIn0a4pk5UkvHU/FC1Fl8gBZBQqMkTVGXCJEqpbQG5qmOZZdT+Fs3dIUnADXaI1XxVviE6vhHwWeHHUaYFMaTZ9Mm5H0SDeyySTeXmXoQq4AW1w'
        b'ORNX+YKKRJ7c5B0nm1K/+2EbDQh2gJ2bdebMI7Y7OcUvL13mVS/jO/WKioj9XmbIzSTv61Ofj85LGjnD4NOoDwSTuj25Z9vdTsviUpYFv/xeTmXaouJafrHdGOt7T76/'
        b'PcT4zAj3H8822Xh/HPmjxfTSwrLXTs2M8vrC6HDQ8PJvvttjtdUz521lbPbz87vPl3la/OMfaZ+1vvXcBKOh+6dnzAn8PDDRKen9hqpdbx7y+zbovRrP741vFBg8bvTu'
        b'iKrugAsjHju+Wpn5nfOuG/+ceSf+D+XH8R88ue6lv3ttWDFX8bp8+k9Ff3u83XHRi9unHWj++Oawp2tbvtvon1G25v19P/tXzTklt6CHvy6oC2o0AaNWfhpPIHQOSulh'
        b'ujMcDe4dMqpAzQzHDLrs2Qnwac5HzfXN20HxfKiFFsbQcWQmKuiJ6UQXoYCT0ZhOPogpOfm7UJVGU4GzAb1iOndb0ycmQS6q7uEwhhy4zskIizHUojaWe2mipVoLiuHj'
        b'0Fl3VCSn9YqGdlTWE7AKJ1yYZ1sANFI1KZ6DIup8O8D1Ns0BLrpPZG4eLf4oi1WBzNcCdCIM52QG3aJA1B5PXRhGrYEuwqPsa0SYlCmNcqva3RKX1zVgsj9ZAC5ykIeO'
        b'w2VUtJgegofATagiFmc4aaF1hIRmOMK8gJpTIxz9g1inrIQ6LPkPniSCIyvQKZpwMC7zUUc/5x7gOjcblEv9YqSoDp0ZGMmJ6vGyRKI5SSjnaHRoIM+d7H8wijLwYVph'
        b'Co2lFEkp569UIiHnybyVmjOYnFyTLzPBTJDSuMhto/trUrqDH40eJfixJ+7RQL9PgKF+ul0dMY4+j6SUXrfTr5Q+rIL/4TBHrN7dXfPQMEdd2txfinEkhx0DYxzHBVPM'
        b'BjhiJe+JcXzUAMc5Q0iII+xDJXSPngWtUzQIB1PcUAsXs9BLJOPGoj2oCppFkGu/ke7RwzxRHolj3A4tGmjMQYNYAF457MWLHH57EzSK1bGL+cPpJtE1WJgOPLmKSsxb'
        b'N4vBw8DBOc5ToGwQnJzipglO9IaqdBLuZJs8WE2bZb/YNciUZm0MV+GSKnUrIqQmZCMuQDeH0jt83GBHOVyEOocgdWTiCGhleZxDBWPggJhEJ2pCE6HNl8k8N1dDVhiU'
        b'oG6yf7L4RH87uuXFwOWJYYD3XiiZ4q8JT4R6tJ/GlHksypBlQLEVkXRIMCE67JpO1u/VwevCUIk6VtAHdWnDBcdBM20G7yH7bR7jPAXOLSrphVkmLFDuo+RxgS+J8knb'
        b'LDixZQ37cNNQ35nDBTuei4pyMJWZ/nvRgrmPFmLWpbHDpC8mc0aG2tV0KE54ZU31C4JCJyinjkiT4byfM1SgNoKYQlwA5ahTNBlLNQFYUmhTyXBzLYR88/Ap6CitzUF/'
        b'kzR3Ee7kJVFOpdNmsCo+52HtUMEtJ0iqO+zXrOLSKUDAKVRJndrbzI1YgOCmCdoQQdlmGoIXNi1OhuXHI2hPqimLARxuT1N8drDEIoNEItpFmXDpwZycp6NjBmSha8Sr'
        b'd0WMmDr1ooNQ9b/RoCIp1ytmD67A/mRZxm5X6DRnMXtQaUkrZLMLVcqUG1GOiGMhey4on74SiC7H0oA9j4mG6ni9SVIau4uafHD3cCRUzwKLgOGDWfjwHiiYS4L1oDUQ'
        b'GlA1i9ZLn8B47s5CQSY6DedJxF6vaD03dE7hXxAqVlXj7MsbW9PDA1RDfKy++ebzmnuHc+/4PmNqMW9tYf6g8l8PLC7LFH+XN/52vc+IOy/GxbR+8daW+tLIFdMChlpN'
        b'+2Gx07KqgKH3fzsgW3Zhxa8ip8IPZ525F1pwoEj16Y5PZ32acWzOuswTRRvsDj51w3KR2UdvXMq3XCGv31gj+9bwzunqz8c8lf3KY3/L3brEN+fW6qHGxaOe+Tav+q0X'
        b'0Ot5DUsDBmcYTF4w/JOlySctIsSbXjv5iU3r1nBv1cnXiu5/ZPp24+GOZ45Mb3lhRbnhY863D7zeadC8Obxj6fvZT3aWF79m+V6j4vtM08iRz+3yOP/H6IY162+2+n47'
        b'7sY/0hJVC359RuT9j5o3O+2F3V6JosR3br/vuaB7xNO7N/+4xdIxfU26/NXKqIZfHc8GzVEVTt5k2j7s6qqziilfbLqMOses3/69t/O/uuvD5XHftP+YnOnZWeS19OuM'
        b'Z6Rtnwx//fTIsBddR7wLdY11adIZ6x2Vf4h/sJqy/fHmdJOYkO5pcln3sqa7wasr44+uuPlObPz7IxrC9nUs+GZKy+8tCTU1J8yuJFSH/jjD29zu//B2HXBVHsv++04F'
        b'Dk1AREVFFOTQERV7R+lIERsIKFXpB7ArIKAUAbFRBJXeuyBNb2Zz067JzU3XJKaYRFNMM+2m+bacQ9GYm+S+9+IvwH5ld7/Z2d2ZnfnPrCv9J9LeuqUphr8l61jT9lSM'
        b'/e24e1NiHswpeMH0C+lnvuGGpXYDJXecv31J9/t16dvrlpWoL/fek9FecuLnQ69+8fnlUMPXh194a2oHijt8+evLDgav9WpZuNvcen5JVm/FB8+sLHt2apPmXOeoVR8m'
        b'Ln9p6nzTQvXuKetjyuenGqRqLpB+tLD9a/Mh/fAXVzzzk9/dFS6TNmt9k+K2tVXN32yOT4rlouevST2+X7/4mmNHd4fi+Atz4s3u/PuB3d5vvtP4JXC22etXjrx764nF'
        b'K2Z9Zxuda+99fFfEP0I+dqo841X/xNWn7yfmv7Dj/KGOb/pqr854SWR8VP3urwaeIccfRAq++Onbj1zRz2+npxz+dsprH683ftN5evQblzbiv+eu/75o/ZTUqDPZKfvP'
        b'zbt+/dq8z177Bl9f9tqXBtElpWem/BrSEBoREajzWfBqs5QH792Os933edLkuuQ70dm3Mw+9k7fAFrVIv9D4zDL/x59K3sn1DJx6O/atfIXmy/vWrnDY9vMvP7zyVEvR'
        b'BPvX00+YxTbN/ewdyY/XF9em7pJfemHbkbd/NPzi5nz9jJ+MU6f9+O+MPUUGT/ytgh8OTT/Seffbl25d++rC9+GSSCfXSGny/V6L6m96luhDs+MAeNxesHbLmzE21Ydj'
        b'erXu6MSuv+H1wq9612+9F1S9d7FTPqpuE34Se/GHz0M1fA323pDefT57Y7vhJOfd/54wY/7H96q+lsdTHEGqfP/D8jdeKk+r4G9YfD/JAFlVWAVoVAV2sd+jRMAlTaVK'
        b'xmooWEaDnijBbXAFyhgALjCeifBpC+GkO17lyQNwFS6MIuCGoIBqGcFq6LQSucZQa3AZTjPk2rQI5pzbg3qO4CXoMgGvjSLX4KyAdmLNeixFKEUW6BgLXDuxO5mYSFAN'
        b'pO9XItfkbnj3sSTew1ixILi1JdASAZkS6I6fRqX7cNRi4rzdXWWrIsA1lBmgdP3uxotiK6QTfNooOm0rlFG9YSKcRY0EnUa8+2tRjwqd1oDOMY0sc6qxEkFGQBUwpISn'
        b'YWUkkxGrXAOVjDwRNmkMPg3Ob2XOwOewgleK8mxdA0neb4pQg8IVLKsi9EIme93GdQ/kMIhaLKphHt19UKxFIWpj8Gn7RBSh1gGlDCVTAZ1RoSjNnWYPV2LUoAKqaf9n'
        b'w0n85ghGTcKpQ6OAQtSMl7EoQUMcnByBqIk5DciexSBqtdBCn9ivj8pJDwk+DS5ghhvBqEWgi7QLB7Bc1kRhZnKUB6WoneHMVs5hLufNmwwVXsvteba3NQStUmI7oCZA'
        b'hTEbAZjZQRXBmPk7UEiK3FCINT7hUusRhQ/agliEocvW4YctZF42mnL8yVDNo7YVE1mEoWsoL4wYNxneZAbUjUBOIBOPOrUonoZ81E6xawS5tpdgE0bBa6jbkfmft6Oi'
        b'wwpbil6bB0dHAGwDqJ7WAseNUwl8LZGI2yhHTuBrqB5KeG66SASdE4yVYZrg2Fx3OQWpYQbKHQGqGa5nsI406JcSWBdmUBfiVK7CqaGzwdQ2mooaUL7CiwwjARwwZAN0'
        b'rKDK/OQNJD1rHroI2WKO4tSCFyuBo1DkPzb6lJEX0eVRlRHjyfpwTZTn7gbHaYMUpeYDXfTVFSJ0dHxMpVaxrnAi6plOb8eh07tVMDUBp8GjYxSmBp0raXf3WaJe8jme'
        b'NhpQoQSpYe5X5rs8FQODBKZGMGqzUJUSptbAFgU0rAFpVngoCEptGVSMANW8oJ/hl46bonRDf9z6KEoND8dRtuJkwYVUDwOCUxsLUuNRFV0j1PdBDv4qW9RO+YFi1OQz'
        b'KTMtQ41JCtupmvRrGULN3o1Bm0K1lPA0CSeDemggADXnA7QzplC0g6FRoDZGhSnZhdJoa7tQO2aqbo9UogVTdBqWlQdpnSvnYMbqTg5HxUkkxjuFp6GCJewbiq3gFMrz'
        b'gEYtloSV4dOOon52dHMSqlEJkWSNXJgkG2zKmOyMvZPyRAqqUkfAaZg6ObReHTgLR5XQGZ7TSEbtBDuDSuAyi29fj4pSlQC1EXQalKEuFUIN2qGCbkGoGzNWMcOoMXwa'
        b'alg4ClGDfmhnBv00rz1TJ1OQ2ihCLQbVMZhdxZ5oglBDWFeQMITahZWUP4KwklU7CZUSINooQq0ItdBKNVDtMnIHjqEaiRKjBv2ogZJ14qTtWK6FKwdQjsUIRK2LY2zX'
        b'jzLXUYzaHsvJqFGFUTsvo0t4YCpUE9po4MmCjksEnugy7rER1m+tXOAcbVk7EQ0pxWq4ikqZWH0AHWOfUwMNa8mJGmREsMj86jDIFtfLxoEyWiuuk7CkBmTNh2IBtKDM'
        b'jYxOReiEPzqFBmVK1A3WT00noGx281TQXqsRZK1mEDpJsHHpYnoa57HWUsE2RnUlMg5dwtrQtCUivOSXQB3rt5OTBhxl+8sINA7qHOl027ZjDDAOc4UVpFNkHBpWkhTv'
        b'TSfw8kWwcShnNk+hcStROgM6daE8EUXHjUDj5kGxCh0H16CE0mYp9OLdxwZ1W9Ctj+Dj/BLYxpkBfXhO0A64JkZgFhzBs8mhlQ7bIZRjP3LovzpMhWcL3E/P7aAK5TtD'
        b'LRT+BqhtBNAWF0oHIhoLRKdGyUWOx2tRNsoQJkOagpKTl+oTbnWXq6NcuStcQJeUaKXJkC5ar8syKON5cWEWe4woWCVLeCwNnBesgly8GdMtowQNrsf9oetuRMgIgg2z'
        b'qvKYcunU0cNZTmYCreRsFq9hl9hmfgIVYYrl2aA0VOGmOh7dj8eDvK0OPbZ4i+n0xjxVaIUXX10saOwTHoSGNfTtOKheaIX5EMtlnuvhNKFXqeAAgb6SjTE8FW9QJCJp'
        b'DhEhycfx3AS8X3VNFB5CZzcmE9sHZG1c/zCuz5x7GBjHcH1+mxmPDy6GLoaKU0HiLKdTUBxcdGSLWq8OnFdiYwn68jyqJOhYuGTGsJDN5nBa4boRhi3lI0jszrWUf7fA'
        b'OQV70xFlqxDAC1E7ZUE4l2j9W7g9zlzDkeD21kvoyCLCZmmqHiphh5VEXBZCtRnU0L08DE/JGtVcU2L2IqFeCdtDaakM7dm1Gx2TWUCfJREGGGxv4Wz6kUtgENXKVCA3'
        b'dBKdY7i9g9PZznVaysts0WUoIiA3BtvDhK5iUyF3UxhdgJSgvekHVLA9NIRlDZr55JxJgEwOldswpxLcnjkoLQZnw8UUuDeC2sOz/yJB7h1cxaibG4Tlh25ryLS3tVUh'
        b'90IsGdI0Y2+CzM1zHRQIKXAPXdhJKYY3Vn8K3GOovcEtY4F7ULiOSWDt69ylB2U2tirUHl6L0ykbRqOr9gy1Z2MZbqoC7Tmiy5QSntDEUdCeixwv8ErMngx10JurJ6I+'
        b'VG1IYHtjQHsFiymnmcJJIUXtqSB7qMxYidoLnEcHwR0L+pUq1B5ebY1gmID2dNF5WoEO9CSwABjWrjrohOMobg9dWkXbF0whebz74CIqZxlYCG4vFYqpIGt6ZLe7rSeW'
        b'D69JKG5v8Qz6uQ62h1kWchuUibJG0Hml++Ta//9wPIqTohaFDb+HxWP/JqsQebrCx2Px1EaweHr0n4jX5nVx2eRngUSX/5PYO6maEgsnong3tQf4+Qf03xuSBY+g8X4V'
        b'iBjyzoC+oU3sHRTBZ8Qb8iJcqy2vTd6X/JcovFc0l45H4Rk9DoVn+LDR4b+F4B0ndhACa/tdO0ga9+PvAPEe0yncEwJXSLqpQuEJCQrvaV55SinX//9Dzz2LG32PgA1j'
        b'uP8l9NwbEisBry0eg5SbMwYpp7xmtCqFYDVQHRa4C0aOsuG8g+o0m+cs4Jo4FpUuecR7Vlv5W5HxCEJuq+i09LT6af0IAfl5Wlv5t4Hytwb7HS2MEIYJTwjCLEdsTSTd'
        b'juYxrWPax3Rp0mxNgrSjyDRxuCRMEibN5Eiy8BOCrVJc1qBlGS2r4bImLWvRsjoua9OyDi1r4LIuLU+gZRku69GyPi1r4rIBLU+kZS1cNqTlSbSsjctGtDyZlnVweQot'
        b'T6VlXVw2puVptDwBl6fT8gxa1sNlE1qeScv6uGxKy7No2eCYOIJX4u0m0r9J8nG1rYbU1VJI7XBqx2SYNjqYNhMobSzC5PiJSWEC6kNqdVNzzSpP/7VKI9p7vYKHXCuJ'
        b'b9PYJxg0b8QzJzme5JlQsGfmz7Vmvx1pVgby17xxlalsdQpbk1VjnAaVPnAUUaD0tMN3k8OTaNKI+FSSATd5vNPf2AQS1ibhoTujTJLCE5LCFeFxY6oY45VI3FrH1fA4'
        b't5/xFsNxBa944u3lGmFCU78qTPaEJ4WbKFJ2xEZT/6XouDFADepQhW+H4v+To5LCxzceG54cFR9Gfddxn+NjUsOpbTOFLDAx+4hj1rgMGSbO0dTHyWKVXOmsGzPe84s4'
        b'SCl9B9lA2CnHQUVxaxOL1XLVY6EminDiw5Yc/nuDRMbQYo2coDtCx/gJKj304pOiI6PjQmMIzEAJU8YkIBCKhz5UoQiNpACTcJYJBD/Fvt4kLDwBr6gKk3jWcersZ6G8'
        b't5pwWGy8YrzP18742FjilEx57yHHQi+54KZwb2zMTcnO0Njk+fN2CscsO2Ll0kMNUb74hxI+Jj2mytclo0sIjxcRQYS20nAtPC45yh0S7dc7KKSGaxE1VgsPi/zG/D0m'
        b'wfOP/B8AlI2bTI93MXuc1yH+QuZwuNnTQ+kxR1Oz0HpHxw6PEvUqxVPzt11RLcIZSz1u3v4O0ImSdzHBq+wMxTM/BHcphHn+scpGKhnLfo9JmBMaFhbN/ESV7Y5jP8Ko'
        b'iSnhyimsSMFza2QJ+W2AxzhvWpYHh8zA0JTk+NjQ5OidlGFjw5Mix2S5eQxUJAnPzIT4uDBCYTavfz9rzbi9TkvJdOMdC6Z5KYjA/NnQJ93/+t5K3pQsf1bemyd/rStd'
        b'8cJ1LvqQWu37PzLDphXZYHtRZRRWsk6iPnJimIwVBzn0Qp4cnYUuSFcYBpJXsKpeZEglVX9mDu2BrL3QLIY0VMhxh7nDKA2OUzPuQlcWyrhcFGJtbrueozZSaIYOqINu'
        b'AbqEhfEl3JJwaIj54cGDB6YC6n8WYu4dYm03KZCjtk7Ug3I2U0eGM3DOHp12tBdw4kX8BgsYkAtSyJnXISiCTgXK1UY5e5iZwcPLVt3SgoeOrdxcdFpihQYtaUexqtqC'
        b'umSO6AS+ywk8eSdUtgvXQs7DtpOoqQo4ozGmIg3yg+dMF4tNsQZXTN0QklD5LBk5VysW2RD9b4CHRtTjhmuRE+L7Q6lCEjS2M66WWJlGnVau7rbE4hGAStSM3RxpHGQ4'
        b'E0BsuGgIrqhuq80XxKHcKLmQfXwlKrEnaUFs0ElH+/kC1GrIaR4S7BbDSRqEF1WgbOgffUASBC2c5mFBDH6xijYx/yCUjd7n4coaTvOIIBZV8SmWpIJirGaxnCMu/i7k'
        b'OR+XEf+TtbOseG6tjnQSOoGyafYMY3QVdTGF0scGMwvRJfUhHfVixRMuhKA86m8QhdWnzLFuLKqELSjHw93dRpC4DCqM0TDkTkRdM+AS6nI3gFx3mQbqgjw3Xz8uPELX'
        b'CRVExRA7fpwO44ln1oV4RMWmbCPjHYnfeLR24tlp57bRghy+5/sRh0r3jahjhI2p+ww0Gnu7ivXMNFAW1IrFqN/ZDBrlnPMeA1QBZ9BRTHYak3cTXEbdOgnhs5Iwm6Ar'
        b'vDm6tIfe8UIlqF6mlgRlnql49EW8JZyVM/eUkpD5qFszEbWE0Jda+NnoGlylHD9R00+R4IUu7ibHuUJNPgTa/JnfSuZmVK5IRF0oe4smeSuNn71QgnmJ1LgPznsoUG8i'
        b'Ko0iNcIQbwhXUR3tRwLqcyCtbZeqGtsAdXTA16IOVDBmxNHZ9XTEXfkUErBjwpa9Y9PMeNq4eW90GXlaSUs8kbs3EkeZCzEyaEBtW6kjKmoksdTdw1DGwxVssAlgL2J+'
        b'4sLQFTUSIK8wetkMH7EiDYt339RpxJ5aotB30H3arOLg1fsVdvFzFswccvhn0ZcJejGazlf52JJ5SyI2lOQH14TUZO8+PdlcMXFiVnvkD5zmRPFEs4lrXF3PhPp2F9sV'
        b'7DM4u+fBj1987t3VEhT0itf1gYlBRroX/5bskPJd3uDJ56e9iwKrtftL5KY52r2NszO0jBP8NP4994ln0DN25cvCr7QJn5D2f7MwNX3I5O1zAc+vmVl76UbizDTdXN3h'
        b'FIMzye/Whp1aeuOtHbny9Yt/eH5j2xfupotemvbGJxlh8nuHiq4nL7/l9+S67Odra+4PK17UCTGta9fc2fD1XLtcU8hV/3hKgEN0d6N1uaHP6jdf3rJg5/cRlws3Kkxz'
        b'5RFm+XdamxclP1Fz/YzawIk9M5utd76Tm/JESZJlee/Cl7zyzBKf+nH7g0sVl68qZt0buhJyJm/Wh8XP262Z/npT8le9lVbe+yMKvq694Pkg22fBRuvPF6rf+/Wz4HT5'
        b'gRmVV3I3ujddvN9l0vZ3g7o9Cxdr/8thp7H6PeNP0vR9nKUDOwfWGd1oq/rVZ2Dh94tvXS+6k31FbnrfdENQb1P8q9tmpZgp2t6/vmziMyvfMtzzZNBbF96epf5p77xV'
        b'9yqPX9dQhO9o3lXSeqm+B714/9ZLr/ztHXvj+UtfToL9wYnbTV77u6Sy5PK1N/b+kpm94/sXdH7u+dtQz9YHV7+be/XVkqe+mVG57x+Kb4IrfzQqfDl2a+X+p/zWV555'
        b'8uMncPHWj3mR4n3nvWbsK7D2/qV0y9SyOUO7f52hIxFvdpGnHnk5fvWNn7Vvvhq4c/6uL+bNWOrx7PJ3bLa8+nJoXmnFrTnPX3jpUNuiyvpLqz3DjfwmPvdlzc4vJqW2'
        b'lExeF9up1/mFydra9Oeqs2f+pPmBw1fbrvGu/5zg8eq/5avYQddAdKAV3sdO2noK8Hxq4N2hMZyZEZvwLlcKeVi9PB62iTjBe6NcASeDITy3oATVsveb8U5TawUdIa4e'
        b'UlzBcX6ZjtIsMWjmqDKPH0KnlbFdW6CPntz54f00DfLsaJAFqRYnCRGYQjULm7UBZU4k2ZDsvG0EqFCfkxwWWG6GhmTiZAm9qM0Vd2oQau2IVdXDFnK8qXEYjtu5WFtS'
        b'yKeUC8Y7cms8usCMpulwGjWqbP5kSkINFFKbP/ShTNrmdHSJIydn6ISNRHqAk2wXzEIZ0Ea/RN9+p7u3DWS7ulqTE2AZ9JD4rPVQQQ8pRdq7xjoccJzRHsgwEZHQg/n0'
        b'AJSfqhgLvyQezV0kZZZIDY7hFkjr4XABWhSB89nJofLYUBxIj/1mwXnoVJ0ZwlVNdmwIV6GZDkB0NLpm5QqteKHF+7cokkfZjquYBbd0KV7B82iAXnKoWLVPGQpsCjov'
        b'SlQdUMOZZLzdELs+BwWQzax5Xb40vK47CbKDa8iDo3Zunu425CDQS1nJbHRGvGQVlDJeyTCDXMUMKEUnXMmouGt72aAedwE3fZ0Iak1REQuXCMfQeWIUL1Rnt21QGafl'
        b'LED9Dpup/Q1y8HaXCXl7be28bKw9x7Rm4iDCy+cVxOxvnmsWKmzdZqJ01VEoOQeF4mXMjHEFTkA75Hnbunlau3piiQd1c9pRwoWo9QAL7XqMhGZlOzY7+4V8KCUGTqmd'
        b'cjwmHThCDQX57ihPCiUiTqIu0HSV03Plw/j6FYWH15FIW7zb7eYPipPo8fm0HfokLmeQ0YjdEwbQVVpdGDRNpBEm14SNWu86mQvHVgVqpEYomiupGtI5MSrj0YCTEwvR'
        b'K0R1Mlt3OG5Oz7ebeMwp7QGUWqYoF2oetmvynIEaZLHAm9UiyiFb0JUIhdCCRL9Uhb48ygL1oeYpk1XGyA3oIrVHBhrTLptDXgIxPeWuhEwPCW65nIcCl7l0PqyBVjzN'
        b'8PcUQo6zFelWN82A6Ezpoy6SMgs1f5j48MGQiy8blyIs3lSr/GrE21ET/tIBAY8fvkRPoOUaiQrUd5jEJ6XW3wRDOly7Fm0kgzkamFQPM+g5aBWiPD3UyGww/S4oHfKs'
        b'7b1VDgFqUCaAnDUHKRtj0esoNMnMLH7TvR/LuBfhNDNJXkFt21G3ldwCSpi1/DIPbXLWD3ss7/eQm0rhSYKnRgenHSZ0RoOoLNmGsMayKPx9R7FglIp6tBJH5TGC6rZD'
        b'BS6eNnIJ5+espg11HpTM2302KFA/dFlpYNlYznPSQ4J5nnjZotJTZghKV0TstUpiXC4NF8yNhXK2pHVL0XFMFldiGfKm6QDFeF3pD0JNogmbXRhVSoNRvgyq5pGqWQ3Q'
        b'JFiGsiOovS056pCqAsyZUlQFZZy2l3DlAVTMAOUn0UkDxXYvN+JWxKM+XveAER2nqJlxJMYiD3hpJ9aaOSwjl+eMsPG2ml34gctCyMXk6WQG/jKUT0Myc0vgIvWWObSA'
        b'8WEFXjnOKtYfolZSGha0E65R4/1KzDTDeL3PifDGHXHFM5IuCXYu6ARJMV8ndpLDELNO9oZPU3jJlb5U7jynOy3SSuiDl4JrycSndFNAMgm2zO07QEMtr7agk8MHykIV'
        b'cvUgzAWYQELI4vcn2DPy1eE9pcnKzcbdxtLLk08I53QihaFwFg1RAy3qg9ZwTMDRXhFMTI4dXEHHvcScfLsYytG5yGSiUVhAWSTkPcwUWLAlfOG9YD6PCdIm8YpD/Upy'
        b'RHhSLEhG1Ihr0IFdDCLTHu0pI3umioMnoAEHSBdCqxj1MCPsyVB03gov3Hl0z7GRcGpoUIAH88IEFg6gBs/emnGWJp4zlFoRQxO0Qo9c67836fwvmYZ+K8AASan6Hww/'
        b'R7hwDV5XQIAjEt6Y1yTGFgE9V/9FItal5h6SSIuYRCQCNfqXNn5Om5/Om/MWvJ5AlyTpwv+M6bO61GQi4Q15Q1ynHv6tjf+p4ac1BBKB4cNXePJPm5qeyLsSJYjFgN8/'
        b'ceyZ00OxDuRiBiF5jxgw3h8PS9H8r8ZCyKobrX2Enq5Yh1QsJfT8fetMGtdv/nj7zG9/1R+KnRDxH2MntKpczB9qZiRwgoPqYJyeLFubhEfamliSozFb+/mOqkAvj8ZR'
        b'+OOhHRJ+r3sdqu79OJX0Q3nKahIdNq7FP9RYFG6skb+pFryTHb8/ts3ukTZnUsAzRflGmNDXCGz/T7dMRkHO39QKHjlcDo5+fPO9I82brzJJiYtOTAn/DXT/X+yDZrDq'
        b'oPH3utA/0gVLQgFFMiYBPaocOaX8q93IJCM++fdGfGikbVu/eBJeKC4inkZIMAndEZ+SPC5a0Z9vn3IciT3z2Pavjee4MdFz/hLNk1x+rzEYaWzKaGOrXdf8xbbcf6+t'
        b'v6vaSiIJrv84tfJ/r9JnRj7Awv83Yh6ponb8pXHC7KpBAw8EkzAAj+3CP8YPGI0dwCbtX+JOOVkiaKvJ8Y9t84WRNicr40z8xRYjVUvDjtAYYh8Jjk8Ij3tss/8aaXYh'
        b'aZY8yw7tY8Za/x4OTPLXlkrcK+2RXu2MiVeEP7Zbr4zvFnn4v+rW/1bQy8zfCnrJcw8bK4Re0d2XvhUqiLD6TtJXJHylWsS7zts9hJzacf6y/Q05T9WraBiOorhsO7g0'
        b'VgdCnZD9mLiVc1TeNERJ+o9C1REucr/BQ5t9THhccPDjo1aSBl4nUgaJy/UfpYw0rvl3Ylf+ZtP/JwMT8ccGRuTlH716xRCnIJcX1q51D+2r14x410PKiSx4uWvDKC8+'
        b'SvlOjlE+KZN/RLYJDt4RHx/ze2Qlb9/8E2Rt+B2y/nbb4+hK+k56QLQLZrUdDfupiinFLLf8Ma0Rq63guBhTXIgpLqAUF1IqCw4L/cb8/TiKEzWTZHt0HEfxGV7UBgAn'
        b'1i5SJKIhE9Slsg9AJVyh5rLJ9mLrXh7P9pUhHraWQRwFtAbA8EaFdsrkJHXyeBVvG7CdWuI2hIkD73P0YesEyRouhQjJh/WVWYcowJ8Gx8h3x394kXgZvht8D6ITNgEC'
        b'bvtKKVyC9rXUTrZtk4O7Gzn/hwLVORmqgavuWA+03CmG5kRURC0UrtCFzisSAlCel8rqsXwzNVpBGcqBYyPuwDwHxSiNOQSruzK7WAd0oCx62lNgTY6lOJENjxW2wiBa'
        b'dSq6FGwln7hgBCIMtegifRHVo3xPpsY6RXgRZR7rseGoFl31p2DgvR6omXys3MZVxO1Cp9WlAiiAbtRGrTF2cAZa3F2hAA0Tn16RiIcLKdb0RQ90Fp0mR59yrGRC/lb1'
        b'RSQ31Hk0yMCanbroKsqzXYMuj+CC0Amop73dYrnfdBvKs/Gi2qckSDARZVqkkPTYKDsAFbijAlcSvc8D5VG6x0xguaetlolxFRmo/RH+lKn402OUP8dzJz8S5+zPcOYj'
        b'kYkp2OIRzrT1otxX5SDm1MLmSjFDaa6ZtY7hwM1RA1TrwAWaukIJcHFGV5mVuH2OHWoWKlxHnYMnaFKwNcqE3Jlk1GAIWmwsR8YND81pytTqqHFRqJeC5vsgp5BQNIle'
        b'R7VTpyqIKzJWbSELXZ6mEUPtbWjYFS4ps5Zv59G1g3YHjSl/2KBqOWRCmzJduypX+0nUzTJkdstRgxUMs6xPSjANFEZRW6wmOgPHlWgalL6AAWoImqZiErWFs7gr3T5w'
        b'mmzi6AoUzuRmRkTLxewbG7ZApvJtOAWVI6/vgjZGnqtm0vhEZYpzBmrxPkQbXmXmQKE0K6FrbM4nPEHqKds6QeEWK1sbT4LUUcF0GrVo2tuF3lBuhVu0lVt62s6SyW3c'
        b'PHnOFLLEi9A5dJl+8zq8ABRQaAwML6boGIKMEYkYY5cvQmdlcFbBfK4x+6oJJq2AWmp3h6NoCJUwv+3tkP2w6zZx3J63kj45H/VANfXs90DneHrWTFYYyKVTwnyTeDek'
        b'LaE2xo16eEUqQBXEJPLYhDRizgvSpSTH3SVKgGVwKQpVTlIkjKw0kIb6KQFQpRHBzOVDH6pTLTdsqYFOTD7ifL4YnY0dt6LFQxo9/FcuaAdllHXWQwWu4igMkmVpdE1C'
        b'w2G0D74oG/XuhgqSQkgJj4BBCb2lBmmQBdf8SaQUFRDA0ZstdPVogOAvdqO+MesDXpDKKfnjYAhVzMXDSZLiqdaVVtTLtoY6J9SLGRmz5RW8xy3kUAFm5Ho6AaykqEYK'
        b'V6xornlRKF4iF5rTBu1QA495DI7CGRcba5pR8azgIJxCwykm+LYQaraN+s5bocKxKW9WohLa8EHUOpc9BG0aFM8SKdTZbEFHOgENGo1b0VBtiDULVaFc0tA5V7mA0mWv'
        b'9RzIQ12pIo5HDRycIRCGclM2GcqT8CKCOt1MJAQSRcJPnA2laPkVm6AJncJXdZdbc9bhUEp3txg9GWdg0sZzuiHW+eaHWVSC7dPwt/t/jZfPEOvs6Fh2MdBDxKlxbhKy'
        b'bFX6J7KLN1y0OKPkNgm3IURzZngUu+ijps7pGs8QciEhMXn6Fo/GbaDiJPmfDNVBLkj7EH+QT9AM4wLwupooCBvR26hcpEzpzKc+JLffVF8aGR4XvjchaXm4ulJ6T9lK'
        b'thyJl+LhU9STLHqqtasNyUuIzo0L24BOCVE3nNJzh2JH3R0LUCM07sPsWgmNE8XOqRyU+EzE97vhMo105YH3llJixcfT8ZSNk5etK8WyuPlssAlweWhPIsMH3QINnjic'
        b'NGmGzERVLBpYOXTMwQu33AbljtqQOOONIlSG2qAFDc6I/nofCBX/wJ/7rfa9cL/+uDdX6r4dVFxs8cnVmOe+tnnnhQ/PZ+Ua2L4kVXvLKNpwbpdAs1QSKOo+IzzqrHdX'
        b'GLhh5dWZzzgZ/TvNv9Gv9jlpWOrZiM+u6P77VrmT46Cjf+Bbkfrff9kX0VneIX95qa3Lcj2fYA2bmuqK24Ll4rnSkvdvim3fLqq4uta86vt3M4puacpKk043D3UO1X7w'
        b'5Z1onaGF7V/Pur1npVpd7GXBYsUH32ycoDj1oGflvjdsVoTsGQh8+17GCxkpVQG+4cm/uG0prTps2HrX+AP/M6+8nzbNoWL99jcjjx0KSsv42vzgW6dW+V7oUi+0LPKe'
        b'sq4iqeDnGj3HU5PmXo/eceL8Lrn32eIFVdofTn+G+0ozVH70UknStt3GrpJ9W34NW7zp+r6wiaK3M7zyCz7Ijvhn0D9euNdw47O2b+e92X/ml/vZEd1T7+609A+af+yr'
        b'Fcfv9Oj8unbtsi8dpO84OKkdvKF5o/+4zEZxzfDDb5Mn5O669cNTBxp61+jv9otJf2XTM0tqUjfYNDl/snjN3pwvrd8LT7owU+fZacUDqz9Z/0GQ72BNm+8t4/eWvzf9'
        b'vflw/5VDQbEbPp/4nmeu9YawKGt36fq610y7VsY2T7uc906Iupv+HL11OpM/7w5bsGOBW+WBKz+12Ub6nH875eD75w3+pbhgfOa6T/+Hb5w4NHXRnejIuukNnkFZlhUv'
        b'Ty70Ca5aYqtV8nd9p4Enf1jz8/6z/7SetWzf7E11ga/v0Nl1J7CtoGPNN1q7XNdIoq+5Nzy7fPH3debtR2O0btwuv75YNCz9qH9BSPTfvz3ZcfUD9V9vf/qx7dsva79y'
        b'b3r3C0/tCS1p/NbbdfDNw5Oivx/Oj830kDy1b3/MjRTr7z6se+vHtPobT++aZ3X+qcQ5L5h5f9hbkVXxxCvvRWSvdrp4qfJfmm9/tQmu7H577TfG79hE7Tj3xYvwyYqL'
        b'6q2XbnypfWvlky8UXUOuR9670B8nPPrdm5NePIwWLkk0O/D8z+8FT/rBKTF1jnyRMgnffnPIpyKcHTSI6Po8hLpWUhNaKmb/qzICQVOH4vUWWKrGkuMEqBfCeRg6xKwu'
        b'LVB2UGaJ6iBdjncBmiBsqiBgKTrBTEhHty5B3R5681TAU9S/itlMMvZCV/AklhlRaX81NWV2tD50NXy3DTGSqyzkuB8qEOJ6yBcZs/R/KtNsFLrKUMbt3GTch9LxkhHe'
        b'8fJYV0sWhtKPOTAl0cNOLuG08EPmqAPyqU38QBRkKPAG2iF42EBLrbPb91D703ao3qMYMc3CkDUqjJvLKNmGMtBZxQG8x46Bix48QG1wDppTZBTgI/DnVwYuT1am5wwi'
        b'SEyCmC6drQRME02EGm1Tl0cyXDMqd6bQZopr9oFaRoeTbnB8KcqiqSxVMGHIN6MfKklyUXiQ0chBfSI8JGJOQ1MAF61RH4P15dKITELIJKZ/a/w8tAgcUZ0T8y9o4RTu'
        b'1g4aNAiBMgABurCR2qqE0AbVMlR+5CFUcxjuM3nXLGypDOs958ciolG9klG6UPFiMyyy5dHgAXh4RIt46DyEihn1+nQ8ZbaoCeoYHJthsXctUUYVcFilwK91rnZ1RX3u'
        b'Ak6aKLBERUqPigmoxUFmETSLAmIZGHbaOvqei2cKyV2YKBdg2SkHj7jGJgEMBKIB2uRBOLFdJvCBxgRqxhRDGY/aUd8M5ieTZROlUJk3sVyUOQuOhdA7a7Ho27zUVObm'
        b'aSXBFBng4eTWWGbsq4VeRyLhq9u622oQaccILovM4LhTIhpmONUSyJcoPKbCAMWzjSSRNMDCMDoFg9BFbX6b0Ll9WFzdC5fHAFpVaFZ00oseIB1CxFLbjRmmYilFgCrh'
        b'n6gIMbitx0Ys0HZvgvNj4WvQr88M0qe1VKEeZjg+lMn4HK6AyvuDWGPMUaJyg2wZLpeCciOX0dntpxEGXakkc6Qya2QrnGfs2ToFihRwygEVWFC/ErEzj05sZjZ0KVaM'
        b'L5pDv8xiFLe4RJlHFU5uQNkKr1joUQVoCEdXWKrBmp3onEyhOQaZbA6djLUKoH47mdnonCqrHwE7OitjUhyEBlSJTqEime0o3JF4yjK4Y7WptsILDU4YRTyq8I4mKJ96'
        b'SGyZBddISkECS/TZMB0NQytdMbRRdvwYZOIoLJH4ki6GU9MokdygzFI2AZ0exSYm2lE6rA3fiZnaC7VrYxbE80XqLpi5ECoYx2fEorogKKNZDlVASTgLDWzx7Egyt/KM'
        b'GhfLxMiTTlFj1LEZ5Vl74bXaEzVhMYvnZHgKo7aoGco8x9p4SSQP5Mt3YsH9uIsIP9AmQNXoGGpnK0A1XoGPE3UNy4dwiYf2sA2eeGCpLpLhiS5aeVtj3sPajSH13ZKh'
        b'qwL8Rjtqpt/rC0cn4g2BoDg9+ZmodB4aYrBndM0HZVJ6DaMrKlce6saDOlZQplxkBTXMgY24r2H9ZniMC1vkDrnh/zVI7CFb7H8fU/GmBgHkBFNHeCprv0Uk7/98dHuE'
        b'M2CARxGFQJKf2rw5tYFb85bEck3BgRq8Hq9LjgrpPwIW1PxVUyiQCO5r6FjwhryFQI/X5o0E1BquTHbIfmsKphBbt4BY1vWIxRxLxka8roAkOTRS0xYQC7mxcAq1jOOe'
        b'CEx4jQci8r9A41f6v5DUqklTAxgy4KZAF1/ZL3/Yvky+P9h2KbVGKZbbjtKD6RSim+rJe8PCk0OjYxQ3pcHJe3eEKsLHWNP/QqIDrKf8QoyCP4+Yz3/CfwlxnYqVhPz/'
        b'+QQ2jXvw+GCPKa64jsVGUPDXVBso9CbaDbcAlepYb/SQC6lCuk4OPTowOC5uTizKo9q9OtShDHel0+SIyxScRcVToFoEeWI16tjuq2M3pn1vZU0zts5YIkKn0XmUqdRZ'
        b'D0Kec/S+cS1tR5ep7qzhBK2PNLQLWlk70ydSfMA2lL3Uivh2tVq4eNq6evokEDrQNB0od7nIEy85IRPVZiuSlaeOZeYqV+6JWvbzeea7n7Gf6tqoysfYHZ2wwbKRP63G'
        b'Yb6Pi7JnC1Dh4tlYznKl57wCuEZiEYymCWGtWqjOb8vnk9OOQChT04FcVEmxlmKswPX+Bk1Qs5ASBWpQK63cDnVOw6PZvmNsle5eG5WhismXEWEo4ogaVIWijOihfT9w'
        b'ihrMv6bfuYb7/SPu5ZUGFeemvdmpPyf25TqbdsF7Qbqftm34+xT1HLFpmGPuk2s1vHw3P+9y3L/rhv/2zk9MT+ruDjge/vrBNdf4mU9KEyKMZ89e8Oy3i+5UHvh8b+Ds'
        b'XONi329KZ5ZZ5JZ9f2Tq1h9kvbOzo5uu6BUXvPHNpbAZz+yNz0owOebLuRYu/Xhj1LHrHx/IvbnJ9FSZza6Xgn2frzmyUuPTiRahR8Jb3T9qMflUFJiwMi3r7g93F69+'
        b'fcLieWWHzn7w7aRtoRHzdoR88mWTsLHZaPPSvs3vv5Lj3KXYNP+0vfHiuIk3dJo/vhmtVR/T5J9THHG1WfxlHdrWFJtpuOv5zmXn5qTs8/1ydSt69eXtrvWFlzfN3rXz'
        b'yQ0rEgdeK96qffO155qrF9wzNok9lpwf/6mt/OPPyr/7V07w5Q/nfXftJ+/L95qe3+h1QNA2ve2tpLLu83dMv//avvDr2XP27TR6dn7/YeOSsvKrOzNMV34UdOfLbrUU'
        b'+3rFrtUfXN3QFb31lZ6Sl4vDO7VrjdT1T/Sliz+pGgh7x6BkeuWGS1YvTdjvdS/1mX92rQ+xffP+5nt5+kk/KI61LzKODHhySsGa7zRyvb/JLNt/Zs3r0k0a2/eusXQI'
        b'ev3Dp+TB8h3T7u7tcDq8RX4yP/Tr76ubX8gJaDx5RfFck3ZN3tM6yRu6brQ/d/+IVmCjQithm9M9m7/LA7cFntvmvjW3dLh8uDgy1sajSn9wk7xO88b7T2h9kCd1Sr8F'
        b'AQVT55r0NU9ZvueWXnPvxqyUnOi72QNLZh/5fvnsX/RffnKd5/mFF4bX5Lb9FFD2yfTKSSFT4jb5fP3xpo43z07bY2333p3Pp/QFPjvH7eldRxKP5Nj1XXuQUfpKT7J7'
        b'sdMPqZF3ktbXP4PqI+9eyXr79b1WAa1f2b64b93JZGiRRnw2IPrKcfWzNcu+MtvnBrdX9Nhox0c9LbdPtiZTrTwGHXvUqw1yovQfcnb0WUjFqvAl6CTqtsKS0wX5qHcl'
        b'FCOWnn4xVO3CWuNk31G9ce9mKjcuR3W7sUhViBrGefcJfVC2D9PwTsAVaMIK3pDRqI6nybHoPx1QBq2PRnZGV1Gv0v3z6BTavzlzrMcJ2wfRUSJvO7kks3gS9Sjdlwa2'
        b'Rv2eglR+1Sxvdr3SWsYke8MI4rqIWkOoe64uVqBaVV7GxGsU9VABZdrsaeiMCHriYJCKZs7GWHDGugaNFHZ4Pv40mb4AHV1kxvSYM8aoKGkGcSBPlGOZew+PzmMxLp3J'
        b'sD2oDxqIVyNUoTaO+jVO92G6a9uSKIUyrNoeZ6wFYVF7jwCa/Y8wmezYCshVyCOgQH3E7xH6t1Ddcp9kNpZsJVw8uijYxC/ZiTqoHDbdDC4T501Ub8Mk6UlYHqbicpVd'
        b'qsovFo4bUcWIuMUmW9FORqZMV1hiXY2ulNT8kQF1Vix4yTmUHjQagA4rv2Piy3VhdYwlwkY1cMWZJIcfq3jMg3rKHDHQseEhb0bbPTRsxpb5StFXlEqQcEwoRmmokAjG'
        b'6NI0xjoFUGmsDmljIxRhRqYte+6GOgWWG4sWYTKewPo/NPJ47c+CY6xjORugEWv4bng7PUF0cSHWMqB0JpQxbacBBtEJme1uQ88kss9AYzJuf4KBcJct41o4MU9fhntF'
        b'nYk5VBakpiUIi3Rjzqw5k6ePBLbbak5C29G4dnaol8IgUMkk4kv9CASCxnp7CAaxCzFKQRF0ezD9FeUEoCyV/or1zyzmOjoAeajXG4pl43VYDzhLOcBerCZzMwgb1VPX'
        b'o2oG9ejagwWUs6hzXJDCnVjGJ1L4WpQ5ZVQK9z4I10aFcHR2IaNF+mrMzHnuQbvYBPbmUdpWuMSmwCVxpBU0wkXDMZHyLqIcFqAnC13QGo+/QHXeJN5jKiYVEWMMsYrb'
        b'MMbbn6pkeMZkrzQKF5nGoQI2XyrQmd3EnZft6HBlk9pCwQ5Ui7oZliJr9yTV3TGiDLo6fYaRCDXtT6YEjEOZuoxL8YBfRuWGRMH1EEDR8gnMYz8GleNaiPQCOaOICjFn'
        b'v1UCpzz0XVFtMpGIZKho3W+trEpnYRNUR/2FfadREkxBF6aPCCWm6DiRFaWc9lahA2QfZriKgQWW7uNb3YdaqDUHHRdjwlcdoCMVCR3+pCZvrO3ZohpUqcxGJhTOxMso'
        b'A+5YQ+E01LxNhZWhSBkoFcn1/g/1pv+tUDNjQ8mYqZxfXvljGlSsJk3cTvQb/D/WTQx5Y6ypTCEp3ImOgzUdIxpGhmg3eljMJ7oP0a8MflaTTk/CehAuGwinYGWKJFkn'
        b'z2FF4IEAa1kCrAGR2B5qvDbWzcg1ifKahlCCNSrBA3JVIlQTqAm1hZrUr1kiIJoa8SvG7YlZmHw9XoSvkv5o4Gcf9cylmpNSS2IOwb/8b3oaK7Uku3EkfvtP+KnU/hk3'
        b'Y/oxxBPM6DeTrk8MJqj8nclMNQwmEHyS55bmXadp2Gny9SL846ZU6XJ7U3OsB+xN2Vhf1LnkaWIiStpNfqwkPw6RdtRHXABvSpV+eTc1x7rL3dQa76ZGfKKoBw8lDxuN'
        b'if9/5xCjPkjv4OadyOgc5mjYGm2RwJo336EMNCP8f/ot0hRqCmls9PkR9g8pwBHJeImdjBpE4Wro6uNdvdZyHIuzwo3kIpaOuH0J/rDbV9TDrh5kRbfhHnb7Wu+V4s1R'
        b'4G/Hckf7eXMXOMx3hD7oSE5OSk1MUeClvwMLel2oF282BDCtpqmhra4lg0K6ORejM37m2zeQCGoBYg61oX6ZDPpRJ3PRyI+GEzQtTgE668A5QCkM0nQBRgtmOeIOaKGT'
        b'c7m55nrU6Iuaw6DSEQ+nH5Q4co6Jc5ivRSWcRMOOEtxz6JjHzZullUKMpygvdIojJmDCrPnc/EWomD6LsqFZ4Yh5AQ0tXMAtCIOr9Nkg22mOmL7LJztxTnAW2umzvlig'
        b'6HWUEvMmylrILTxiQzuxBGUshm78R8CRRdyiRNTELNUXoF8Pi9bki6B3MZbsM1EtrXuSgzGhpDnkrOZWo5YdrM+Fc6BUgb8kRGcNtwaLINnUkQWyoMVDQWzdbVZrubVQ'
        b'i4lB6piPOsIU+Ftc4JQz56yuyR7OhcsxCvwtPujaOm4d1tJPU5JOQbXQrhDSaI/F67n1cBqaGfkaIG+LQkqwObUunMtGB1qNM1wlqYDIoPu7cq54MIvodeEsAv0iHzRo'
        b'7sa5oX7IZiNWAvUkEqqARN1NdOfcOShmXji9bhEk/CcHp1GVB+fhjupYnId6yMZSL8mpbgPNnpwnXPSmN9zw1X7ULaZo1TYvzksHpTHq5G3bjbpJ6PyjmPG856Jy1nI/'
        b'DIejbik1b5Vv4DasgRZKHlOsKBBvqGQzH84nBnoYeYYh31JG+l8K13zxaHYspg8vm7RWJiCxBhV+nJ8BGmQPX4pD52SE8Efhkj/nD1UBlAstrZbKeOLENriR2xhrwQL1'
        b'F0H/IRnhocxtAVxA6CZagw70rpERordBwyZuE1zERGeeQNDuJsN9noTqNnObraGSXe7Fgz4IeYTP7LZwW+I02OWiDQQMSnp9zHkrt/WgRNk9qAEsRgkIjKxyG7ctYAEj'
        b'eSP04Zl3CncmZIItZ7sVjtHr5ugMFuNItg04tc6Os5sCQ+z5Sis0QN2SLkPvTG4mDLKRiMRTtwSdImSpg1orzsoKMV6Co6jPz4/YEXLgihlnhs6jPNajbgvSMBmLDG17'
        b'zh46p7IPaLfDcipxzLALtuasd6M29njXAuj2EzNXAXPOXI5K5db0fAlP+ItYkyMOCHlWdqjQiiTAwqNQIeT0UYUQy+d9RsxdsNUFldG7+IcQMpI4/SNY22jHjxgeoU4+'
        b'S1ATalDVw55QhNE6cO8HmN8LHEdX8Pv0iV0k7quBGb6/DaXTGqBuE17KRvoi1OP052IFK490o+4AreEw5JqwXpAHBJzBLFSkj+8v1WQpGYqXObLXlbdDUDVPenDcg31F'
        b'WyqmNGtBCpdsUC/uJfSTJxoXMt/F0zAQxVrAM+eydBZnQCpYDdeoA9lSPMtV/cMdM+X0w/EEJlRYu562sA8GoVlJIhMS1VygImQmDDNvoxIRMQ9SQsapC2fh++QLHaCK'
        b'uajlEguuFR0KIVxC2YqlnAH5RFcopbsWasPqxWX2EaQj0h24hjYj+hXQupV950kYXs7Gkjyhxxmg4iU8pSNUM6eRM2jIVtkL9jEozxvVkWEnX4O/ooIeyZLI7UfITfxB'
        b'eI/pgiFMsTnQD/XkqWOQzrKMtMJZV/bV7KGlnP7BHbQm1AnMCSwqDM4rGyTUx72GNEwgQptQdIIeE0O6xqHRD2O9uswLlRQiajCloBjKw2hjR6F4EepKUt6HPl/GRjUB'
        b'zsqGaH/I/TPBlD5GqID1dxBr0HkqIuNnMI1RnitllSa8WVE6t6IGnZHeSKGK1NM8g344qtjHBqsiAE9YJZ2l6KzvTCX9UKY2Gwji3lPHbq82QU3TVeyA6uAK7W3werxa'
        b'UPqmU9I1oHrCk2fIB1VKWfyZasUK2lH6xKa1S1UsVR5Gx0hEXBxUlFXyZoObimwroYGejIfvImYz5eewQV+vJVSyfwKegkSvXh0Ox9j87UQ9cDSJcT9K96QdCYAib9X8'
        b'Tl/qnqRilvOQwxLbDaBTqJGNXNUBoZAzcMK3d8JxRvSLqBcKld0UQhVlJayBkk+RwAlG0KuOB5VzizxAhqXJ24xy9jTaBQunvSMrFZngeG2pJ7PDEJVSgoudzEdHnraA'
        b'2qGZEoIX0E66+qJStnqYEN7k2ewywNsoNfE16u5UTW/81g7OALpgmBBhHspizowlUnKormRjlIFHQ4InNCGEGnTSTkbApRTWC5QOQ+j43KWMjvaonw4FXMObe76KAWkz'
        b'+n5QzDjnFFxIYXklWmaNjql0NRYQ9CitpmAJibJFftBK1XCegFPSNcoBX4q65Dx9YgoMCt1p3kUXG11ULeDUoF2AuagOiu9QgbMoaaVcg/rZlVgSN70+vPWFeNgkCpjz'
        b'3ampWpxRyNNCkmboyy08u9iyXY3TjfqaZFKKiTFQple6tlSPmx2iQ0SqwC7Xaexi/0wxp6YbKSJefoFT57OLUbO1OWN/KxFnH6J5WOHILp6zk3CaLsuEnEmIR1hIKLuo'
        b'Nm0CZ7LUWsolhMQodJyVnoOmMs5g3nXiY6gZtSucXby8yYCz8HiWuNUHnvKVsIsec3Hr9l+LiWN+maeCXVy6BH+mrgHZsa0dNhziqBO1nXwSZ21hIcatB5Z5BmO90n8d'
        b'vbHBTMSpzX6CeFd7pG9JYE+v2STlNDWFtK+NeGTvlJWS/55dQRvIcMJfYvQ3Upfmgpn63B1H+t/9FXQjlkvgHB4jclRbGM/FQwVksX37aiK6ZkW286yQvdzeieg8c2Ym'
        b'HClEtUnj2U2wmE27fsiibUqn4f7PvkfSNBkP+lmwL+1zxDSxX0JoYmw41f1Rx8mRKGXkxCtS6TrJ8jON5mVSokluiqPjwsL3JhEx77cSM+lgZZ75TC6nm3Q/OmblRRyH'
        b'8/AeR3xlPD280ZnfS28F7ahMtgryoZP2vtt9M9ex8IYIM9nimMOH8ZB4eUWf3VUmUmzELbsYPeXp+484/VW6n5VeHv7ux8mR976dNQSOuoKFRSKXv6U9MHFau/CMwG1D'
        b'ZoXxwm/OGz75QVrPjL+FHvpwaKdj0keyhQnvOurm3r1hkoeiIpuaBwbcZSkeL35ZtGa6+AeLqkwu3H+Ds1bKPPtj5h9NqMpaYJr8orPOIet3jV+4LbB9X88wcfKmhImv'
        b'J0xz6sgsv5IV/tZTz70evmZB/LLm7yxeOzajxe3Mt3WfvNF9q/KKxufvvTCpYljR3uOzbpvd897P7l3w9JQ9PxlYnULDE8z2z3HY96ls8V3dO4sm+R7ryP3pc8MDk29X'
        b'yIdm3pa5/33X2iXL/MJW2HQ8LQ6YmehQZet5puor76XPGEytm53LhT33Wp/4u50f/hj5ybk6WL5pIKwp0O2VsJeH7ROWedwzeXqj323Lc98va0zf3b2tyNA+wRYsZsxb'
        b'+Let2+cZtZxaX3664auMENGPNbV+FZ82rjALfV28bQWK8Ypo/If11EvuF59IiXv3UsyLFv/0z1m8dPKF6ROnfTHjJ58LP4Z91OWZ8YP1Uecbpgnbvnzr6l7vw7cTq249'
        b'eKJuTXf04VArm0T7jXXybmnc2clzC+frJ526s+fyB7WpGqAeJDF/sik69B89/aVnv8rc5he79S1ounL32U/XFm7qCDNdVakxOCu4flfi7Fdn7gmDiJa5n2/4cU/gJ8X/'
        b'un3oUMDTG94Iqut5v+mtlG073ZeaFnSc7vR68ra0b5FexDaD0sIQ/UWo+v3Imxv3Zt+ZkffW2bDXA49N6Pf/ssqz7ul7PbtyDnxe+MzSSOvmRfmvtr1W/OSDyPLAyL4b'
        b'PyT/fOhnrepYy+FfZJ87v5T9ZoZcm50s57jijYrkDfHAPzu9xZz4II9qHNcpgwidQMMojwSDQL1RQk7kwkP3CpYIyBjP7Rp36pnmbmNJvFYasfRaLiQR9ujLbqh3DsnE'
        b'hvoU0LNezAk1eIctqJH5G3WgQTUrVAAtWNfDc1MURrwYB31onzygCeW6e9u4ulq7ijjZCizGkij39dPp3SQtaFWl3GmFGlXKndp91Milvw8LggV2ljCAVwBRCo9ypqEe'
        b'aiZx80Np26HXiuapEUA3H4D1jU7aG0c/6FC5uaF0C6Wn23w9ZfYHX9SpjFIh5jQdUY5EgIYhYzWtdf1hOO1OvfNnxeAGJ/FQFYEKmCtlI+qNX4x6VblaV6G6pcyvZhCO'
        b'oVoaLglKoF11rE7CJU3fKZ/6/+sz8/jjRumfPPG9qaHYGRoXHB0bGhlOD36vkrX3j7jOHOE8RcrADr/9T/SVZAIL96BBXWA0hKbKSNssLrcBviqhh7sGNOiEgfIoWZfX'
        b'I6dgQgP8lwmNQq5BI4Gr8SKBiAaQoDG98T9zmg9Vg5ZIFHFT/MZcPklDoDpCFN4URsdGjjnL/YPkIeo/2zlIXYPqygyif+C0lvx72ujxXi1UOrs2BaWN7D104xFzhttF'
        b'WhvUoNH0kdiwGqpN0I0biQ0roUGUGY5LEKExEhNW9Idiwv7mwR4BHahxj0YFffwRI4lhjvshiBD8BTzpIxgy8p/gkfbFXnSvTdxKw4O6WIpDrKMNNLgUEmzGGzotiGi5'
        b'yYKiElEbGvbwsXBx9XMhc9tVzDkdkFismh997Ua9QEGClh5Msfg0xCX0eoRFwZfFd0MC/9ZRlH7yUqZDVmNpZ07n0Zkl6Y5CLv5VyVtzP5YL6DpihNLQWXd0DMu8JIwN'
        b'SSa6VDAJyllyNugJQm2jRnQ4Zjk+hJI9XFNBOn7jrPmmbGdU+M7dwVRsoXPP/o/PvSOcBYvSv39GMAmYHExiLoz6f42pWTUT+Ogx80Awjt21RthdE/81UUN5fPwH2T2N'
        b'u6f9eIZfieuZ6elCgtpVwUUvGxfIV8I/HvHccifuEahAArlQixVkckBnJEMVXpuo75YL1Bw5iDrcrUlynXwRJ5ki0EDD26jMmgg11laoGJ2M9BJwggk8tyucsk3TDrwt'
        b'+K+XYFFa05IXkeSgZP03c0It7h77oNvLi+DY1LwFClTpTd84MhvL7gvxbqIbYn3TYyunIOd5H6fO89NqeTYhUUjy4XAnvqJC9rxgLLz751KgrJvfFC6GkDdsgogkI+W4'
        b'dX5GN4y+mO/AKYjwfEKy7/U2v40p3+4RckIxbzaHoZGkQbiKqAYKzPUyjuQURG495BhwGw/D1yDjZO9W0eeuEHneo59I7DG3Z0nZcwluFbfxoN1r0ua0bxUqiIxb81ne'
        b'7Q/xu+b3ec7om6sKsqPdybT226iVqpXgfxdXJbHhTw+7KwgVbq7psLJt+czV2rKRZurR7xR+YDpEtwaK3t55+7OXdZz9nrV+Fk8lKS+Y+3UPbffU02kv418ziuWcvEhI'
        b'L203X/sy5qWeXZacJR9GLy0RLc/DK8e79UFc0Ka5tHe3W+/n/Qv/ft/4Bpe1Lphec/A/m/cv/OrtxEwu+8LT9Oxklh7mkTxX1BZMEUWOWMGBPIEbNFhEVwZrixXknNjg'
        b'tK6z76q4V1dqXo6c+6zHr/GyrF9rjjv6v+i8aZlg0Fb3wKfu83yd11h1funiwqccNltraGzSz81pXKgl/VvlQXVnt5bIa3cin9b5iO/NLrruNCPdZEeS6Ps3gmt2ZXwQ'
        b'8Vb/B+azy6tN+1ddK9llKXEsu2BeZtCmVf7sCyu93s94bkaq1PWVhh/jvNIPRv5UmQ5pFj98EHH8u7bZT5/9xFCiLwsYqpo4qXuy/YDos6i3n9s2ccezZtOSra/VHXnu'
        b'h9DBf0Z8O+vvH29p23drZYt/jtXG3Mpl/drrPnNylzYuigt5x7nLYfacG/ezygOFS/bcLzv0daCWxa7l95ee+8wxsvGB5XLBh792em3vg/RDMpsnz7wi7R3aFfLavmmv'
        b'V2m+v/YTu42tlXz4kpc+7nvf2D9y6/Pv33+5vTCjPmneL5OHi6517j3cv/eF+5ltL7YMVOmnOH/6mV+kTwxaZbkmtWHq9U9eSQ44+GDa87FPZU1YN/TL/WtH1j4V7WlT'
        b'oXYgxzu6u1Dn7qv5N56/tP+I3eeyfZK8BMXPhuvu//vtqU98+29ucffCn4s/+3Xr+S/P/dRYV/1hndG3z9V84vPd0W0Ks/NWam8e8Uu5mOSQKNelwtdkj91xqN5dTvwR'
        b'JZwkUmCJMtAw9RSYgc6jQSxikfTM7gxPqAZFgnjUsYPKiZar/InPyBx01NOa40QOPLTsWMScNEqhB+8CefP2k8BjJwi2TA0uCQ5Di5zlDSKC4oAieQY6lZqqpQ0FOjqo'
        b'SzMRb7uokmRO7LalMuUia+gmPkeNUI6FXKWEC02Hmfg7hE7HkkxOuViEbSG+kpn8+sVQSuXmOQGo3w4GrdyoWMlzEl+BAeTp03uOapPJctcMw/QWlTehhMFwoN/I0srN'
        b'y9OGitViTl0mgFN2CtbgWS9/4iGDX5bbEP8LSYhgFvRMoTd5lAXlqHGS1Th4SXoy87I5gbtdjeVfdNzVwwtdkIqxpN8pQBVwLpQ2qxar5e4KV6HNU0nmIEE4XFlJ702B'
        b'Iv81NB3g6I63FZrpvRDUEBztSzG3HnI8eksEBugUqv8vbeR/xft4nAw7ugXSffTsn9lH52iLaSYcKqVq84a8rjI4mS6VP0XKoGUkHw2RVjVp+DJN6mZAniTBzohTuC6V'
        b'dEUC4vwtYs7f9D0LGuyM5ZpR45O0R2RT8U1RQmhy1E1RWGhy6E31yPDk4OTo5JjwPyutCpN0SZ0TyA+dkY2ctGPwpzfyz6c/fiM3YVPguC/eysdu41LO0FOE+hYbQHfo'
        b'TsEYYY70bkRWJBHVqDGajxCORBwQ/PWIA6oGHo4+gnd4ejB+DirhlLvWSm/i3UOPFzGX60GfEGVAnTBacWyCSEEWjiODRp+G3A35JMQj9LNwjQsVEe96CLmpRULff3iO'
        b'CVUifKzDwE0tMnDj2c/yz7BfVJLeCEuI2ADSofxtWU3w8DiTlzf+6XFu1X38OFPBNhevDVfcKfFGxjoG+uhwm60R+29Y/n821I8oJuQ/4SNDLfSKtlngztOcBfeDTNkg'
        b'xjx1N2JHmEuoWsS7WLGf8b0wYjDyDw6j4r8bxt1J+g8Po+7vDaPu+GEkL2/+08PY9DvDOJsM49DBGVZe4wYR0qCFjSK6IA5BlT6PH0dyTHqMjCR/TBQh+gsj+UgsJzKK'
        b'jyae0FAGsDnpfnCscA+XoEtDezmVfyUR0wUhB39Q4xLeO7I3NmkjvfiRL9UJOfvUin3yqAh2pNy7hyNX93bMMI3/cdM2jrpeLIlDnX7QylGDPJzmoPIgXKGPP7VAQhRf'
        b'XXvzXb7c8tXs8eX2+/xs0FkrF1eothRyki0CXl0rWnvgIqdIxbdPVfZOu75EG+x1M98rTZn+vsDlrbTbJlHyTV2nbSd8GPdhRPTCo8+73q755fDzmf7zDpp9F2vk2xhj'
        b'nXzwyYu+a1/WKtCsDz1wfrHBvjz0982nCsw3vbKq/rVzT+7/YvEC3ciK6tfRLJuX50rnnjiy/Ksl0/8NZl+8Ez7tV68cuRpz++zZhPqsbCxcbAR4yy8ToFZ02Qb1OClT'
        b'ySYBjehNNnVUFaMUnw4Ay8RrK7ajlhaSKNkXWkl8i3wsxGBpg8hlB5KxVMaO6EwPKw/oNprQepMluEQlG5TDk8DjcAmVmpJo48yFNh+VQcvoaRs0wEl63FaIhlSe6OfD'
        b'kg5budAjM5ETD23oMmSyD0r3E6KOLQ8BVhPNHpmseFr91h44OoU1yUqcEBYRTLZVgYqD//AMjiOOhtrkbIlKASw8aZLBmFlNePmm6CHk1CPdFCRNJO/sVPWLVrHtT8/t'
        b'er3Hz20Kcs2HPAu2QmM+zbNzsYbTNoS8M1CmCNVBf9wji6i68rdiykP5zU4LT2uelkYIwgQneHqwJBgNERShFiYME2WqHeW3isLFYeIwSSYXJg1TOyHYKsFldVrWoGUp'
        b'LstoWZOW1XBZi5a1aVkdl3VoWZeWNXB5Ai3r0bIMl/Vp2YCWNXF5Ii0b0rIWLk+iZSNa1sblybQ8hZZ1cHkqLRvTsi7JwYa/alrY9Ey1rRPCxRFcNBc+4ShXwxfwWyfg'
        b'u+QgTR2vbTPCTPATemEzadgt05tSz9A44rf4o824TDokHZdJLLvFco2Nz7SDhVKypD+ypKqr1jwSWJLGYaIOeZTEZJtUH1lcRX9ocRXSbVL049H/mNBpXI9HEzo9Ln0S'
        b'mTksgxP5iyRqCmVVbFi7ziQiOuY3ckGN4zLC74+eIU73YhlkstEFlEkXAZLgxduGJlqxg/4FPi7Qio5b2/Lcel7qlLI5xYbuB0tnyhIS/fAN/OAulMlSz6iRkwySXFmZ'
        b'T3eniZqmG88Sq5R7kxqVsXNi4BQPzQtRCT1T8I5IRS0oR5UqV5knFxWhCmrAdMbVt1m5eUId9LKg6lY8pz9HiMrhzGa6KehJId99rhuehqaoBLVzqI9HLOaUAzQHklTQ'
        b'PCfQctjBO2iidBYSqcUDstxt7exYxH1OFi9ApahxInMi6LCKpwsxyiGxUzz1l/CcNrogXI2OzmWW8w6UF+8OrS6etjauntAEZ3hOZ5Zw825URF0EYiehVgkqVmpp5IOg'
        b'D39QqQlzERqAU+gsKghyd/W0xA8I6BEKpK+0ppTy2it391i3RJXlnMRxwhpva4oy3HtP5JjgDpvjeSgn9nxymLRh0xFltCwXdGY7b4eO4o8lu4fD+jmjsbDc0Vmi4lZL'
        b'mTNRYRLUkVBCxdNG88vrCifODqPHaK9Oonl7TNKWp3pIpriz4HTRqajaD3qhCP89k5uJ+3SC7tem69jDFwMTYp6Pm0QO9MjwJSz2VQavmrvR03ZM8CqoRZn0xYJ4Jixs'
        b'WByiWbbPkgUhQ5muTqNxtJwIUGXAEQrpAMWjrHBVXnpvV1PIUAXTOo06mLxSrUBZ+2NZ3ntVNK3uNRRwuRFOoPyH8hQ7ofNj4l2hoTm0GU0CLnG3dfOkOoodKvQSYD64'
        b'KAyCwkPRK3k/MU3quvu1OYeKB32Rva7zng89P1j4RZ/42kmdizX11YnVlxJWvRfW8IHEz0LssfyJuB+8AqZ+VcK/1PL52zdeffWrN069vn1+09Z9QUezqg+/9e/t6jb7'
        b'337PJy9g1Rd7jj2545O3j/7zrn771JYnnvj1u5UBWZXCcqMvo/91/9BrYRdXpbZsiz0Q9GLj3at306NsFt+/09iz5sbkdSuOHzY4ZPjL5rc2pM5ZEOZV6/hJx7pjc1pu'
        b'3XvjPf2Oge/ffdHLo8FPqJP7z9Iri67Znwzq2SlMDb1YcaM2KKUpYPrOPb/kpiRVpro67LG83rm14+bxrU89271t0dXu84a7f82dVNwfV/uRr9a12hm39FLf1NrTppl8'
        b'/Lp5X2zW3EnP7a6bvX7OxmEHM4fapriFebPzdhi6Gh7y+ajlQVXNjNPJJ4sP+3x08ut3wtq2Nfa/4v3c0s/mmh3yO1v61rmvrpUYPgXTNLcv54QVJcbSXPkUFhsA9U8Y'
        b'EUogS0rkkmF0hsolM6DCw90D8gMtbdkTshgBqrFladSxZFMAFagJXaQgf2ZtIEmAD6lPZA9cgmH9NbEPZzg5JlJzd6IAPCt0YQz+DvWgqofSL2D99TI99Fqxg3j/FtpA'
        b'hRdZ2Mixd6glO/QqXIBa8dZ/YNvIqiZTCLAsVrubYvAssCBWwQyZq+YSU+Y5bxbs/hTue7cM9zEPr00jy50hqhQthgIoYSi6IbxYnYM8b7LmCWPgtBkfYBbPzrN2bqIx'
        b'VT1ImIcLqMadhyIYkDGIVgZutGAkzwg0GPA0zYgVGmARMTrmeFCr1wmfZaq1j+f0nIgb4SDqYeilXDxtSa4SaA30ZusffuSAEPqMoZI+oViG2kgXLuApp1r/ZD7k05uh'
        b'mfbDIgIqSA3N81ULoMxMgC7iiuvZuVvbgvkkD09q2GhwB3TUndUeiK6woLFsuVoKAyJOR12YDM3/w9t7wGV1no3Dz2LvIaKiIiqCbHCBoiLKHsoQ3OwlewiCKIgM2Xuj'
        b'gIAMkb0EpLmuNt1p2iRtkjZp07RJM5r2zdukSdr++133OQ8Iiiaxb7/wiz7ynHPPa08s4g7HWujPPSCS52iHrLxoHYxt5w/3LhZm0cESJxpXk1IPGYEmdosxF6dwVAo/'
        b'sviQHrLEG1LyoUTAg1MwhI28JF8Bc1xTeY5EW+C8rEDVUeyEDVu4NgsHL7vxeh2rS4I3nix7dzhNTsPNhzuJGKg7x/W74TmmJtbJCFQjxXZb8Dq3WxEUspnMd29bJEIi'
        b'geY+MczBCLRwT2jFJTIB8ySU84ImwwZNVTH0YDUWGss83TSl8LxZGMzZyknw00yq+KYS/DWBoiJXxIFPSpIX8nY9lhzEdbzmfljVV5YqpCgSkYQvK5T9l6ycNpcopMi1'
        b'PFj6Pf/zlay8Ouen/rbvKAoz1aVS5ONdDaRpRmor7QPy39j0KeJftVhxXInfWsOo1nt6YtETS//mtcfXPKtS/E8Xg7AezbDUtcCA6xYglVUfVc9/vjYF0tr5chdSoiPj'
        b'n9E44OXFBfHTLzYOYG8Fp6YlP0d5cGkhbsmFEOuQp077ytK0Rk6xwZH60RH60al8n9Ij1keWTuH5auWfFzzjBn65NLMeV/g7OTwsOjUh+bnaM3Czvfes+35jabZN0tn4'
        b'fgzPtzvppSpciEsIi46Ifsa1/mZp3h1ckf7glFR9/qXQ/2QBkYsLCM8ID017VkOK3y4tYNvSAviX/uPty/E5c0+f+/dLc+9cBK7UZahFUMYP8NywLXchLDyEgOapK/jj'
        b'0go2c1jFPf38nQWiFo99EVqfOvGflibesgK6//OpFw1LT536o6Wpty9XoNnJL2rPK6dfNjvH7B6PqxEuxdUIigR5gmxhpuYVAWcXEHK2AMFVoe+yz08zn7OhnzSfyz8j'
        b'ruc5q8SLORCVfBW4as9iDhLTo8K5xs6pUayD9iN4TA7nu1BwjZXjE1KfNDM8YWpYvLQnvAKfxTRKuL4Am29/Ie0LwLoCXAwoEk7c2mAs5KP5irFgLS/+QtmVFRLwpcyn'
        b'lKe/spgbzSDgWwgl1wRymZsXud3STh/F6kREhqd6Pb2uPZv2L4y5M973jZl7jqDm6fXt0+zZEbRDCbTimFQuzLqAdSZL2gBWPR6bw+kRMC+rBPNYbfdf8/6s2v/hybAw'
        b'uufpP2hJOO9PVFg88/7ERHwcVBrJfD/ulcz7Y/CqGA3K6b6ZPL3Nc+uSsnNh96PLjln/dZ6h5KvPfe1Kz772lPBUfpoc4WMhYrnC5ZN//hyXX/oMzxB3+dVWbktXj0UW'
        b'z7570jXY3e9Uol/XwLCxiLPRbPLbwEGFGO8LJGpCuOvpw5mCNkI7XOfewSGsEUhshDC2KT7arDlDmGJN3/+99YcXI11CPYI9gmPe6Q2PioyK9Ah1C/YKFn6qe1E3Rtc3'
        b'8H1LGZvEiA/dBILhNvlf/fz1J4LoVg+oSw6Xwgo3zbe6KrGynKooU+OJ6+IHz3v8glZO+clzXFDt00PmVlnG02k156TjK/sLlpx034Zi3yCK7fkEuXVk8YMpvORA9Hml'
        b'GTlFPyU1OjZW/1JwbHTY11iEhYLVuI+sl58TZ5brFmZJzoqZM1T/ku7Bd45Hy72gLk65QN9YRR75KOilEKP33IKVI/5En0w1xdUex3yMPYIOpozoVIYZ/+L6p6cUPQ73'
        b'x6yza4zRtdNtaSo+EKOrM2weJii2NA068/L9HxxH/Rcqv3cLWn/qoy33C7F1w5iM4BWJ7rnil43lObpgR0r5uInLkl6roiRQhUmxs0oUZyUwycJJZjJW2rnMaGztyHnT'
        b'1mMeCw0tx5uulssMsAPSAPS7IZmPUEpiJbUmn+Qje9R2mC+ZdoWeUMdZdrHIhzdNVOPts7xxWyIRBkIF3MYbcJMv2zOP13VMCDdd4Z5EIIv3sTlWZLALRrk3L2OpnTt9'
        b'YyorkOgJUzEHRnEapqSs7GsdaPLRKRe4O+Vw6Oi3xSEtvjYi9z8L9+bqfkiW6ZKLwy9jdk9Z0yPuZ06P/uM58Kvw6e6zVRZkrLVauYxldTE4b14YOyQxU+uYeJH8b1Ym'
        b'Q35RFXlTflEneFOWF6/flOXl3jflF8XQN+WXpMjwxc3xtO0/by+5jCbp0MeL7MzYguVFErGyUO/Mf6tShaqSuog3889qOi2xFLixQ0agCOUimI1PeIKfa0r/Til43BEp'
        b'W6tbKwgTlTHXnFyhSqFmoVaEzDd3QPJvkeChFKZ8Q545IDmXn7zU5SfPxg9TKRNyMfRKNLYkTDVMjRtbYek7GZJ81cM0uN8qcivSDdMsE4Vt497R5N7SDltzQ4G+V6Lv'
        b'BeyJWjn60Q3TKZMN286V3ZCRdlhRKVQtVC/UKNQq1I1QDlsXtp57T5kfl37kaxVovRvKxGGGnONVhvMKsr5BqoVqbLZC7cI1hTqFa+l99TC9sI3c+yrS97m3a+XCNtH7'
        b'O7g52Ztq3Fs69IYC59pkb6hy+9vC9kc7EIUZhG3ldqgWpsVxAaM3VaVoQX8FR4Ynv8Oqia8g7g76K59gHIH+TtEPJmawnEUw32Nwqn5wMrPjJKVFE/ivGCiCpHzu+TD6'
        b'KjSV6YfRqfqpycHxKcGhTEFOecxF6ZpKLCchWTrV0izBKUuqFfGqeP1g/cjoS+Hx0mETki8/Noy5uX56cDLrv2Zn96QPlGltj21widUdOebnYK5/NCF+R6p+Wko4t4PE'
        b'5ISwNG65W1Z6gaX2uSgha1S9DOxlBI/XZ1mqzcKufqk+i7hI/I3SOKRu4HdOP35R3JE95gle5N5xi1t7Lmfw0skyVY6ud/l1rKqzMRjgri7MXN+VM3KFJdCKSMfTD8+I'
        b'Tkllv0lnJxwitQ6FryJRSBckVeL5NT2h2qdHs0XSNxFpNFxwWBiBy1PWFB9G/+sHJyYmRMfThMuNYF8jzrDrfNLBreLFpTlACxbBreXVU13M3RJgdNG3V41lHlyZUx8X'
        b'D6+lArMLWKiE3ZiDTVxfG5zG0Y38GPBQYWkY6Rj0ptRpewkLFbJjYJbzRZphkyfWmHiFHjBzkQhkdgixEYZhYLHKyUMJy9vNIK3XOAP6sIjzPJ6FSmtfM+zBUey2VoMh'
        b'gdhcoHZAtA07oDvNiO3VEsuW9/wy4jz3x+HuJR/W62uvsQxUYRPUcNnBKlCPAyYi1uckwTuFzqGdk+9cjcQRV0XsU5DpL5T2C9JYjUxoPB8jdXkqQSXbFRZxLcXKTLHc'
        b'ky81dyJBDnN2YzlfY+ThkW0pSayeSgU2mQigGFs2RD9Mc5RJeZu+/dX5YM9Key+xlXr+b7/Y8UPZT0u0c486vCD8nWGV0fH+XeYGzm8aWXVPBbd0XN/6uq2farWW5aU1'
        b'ZRG7vBP+9tPXlSss/2XgbJ+thQN/NXXzD5/zKojr2Xwm68e//OCend9uI6+gPdGBdqKP5CMzP/vHL0507Uo+mRHYkXE70VJz3lBv6C/y/6PiF7r1ja/cYjt/UjD28drP'
        b'Ff9YcOlcn2PHw5Mf7tv6luvbkdM/17JLc49//8jD31T/WObEnz/7YOerPQ9/9GnQ/puVLjfs/ugT6XHvn/+sUK2wnndx3/vSpxt+f2DflfY3/iX+d/DRmQM/MNZO5bNf'
        b'Clj2IRdlEEJi3YjQCoqgji8XPhYCJU+4GqFCQyKPg4ac3KgJD6K41k1mUC9acvl3wDyX9KgOdzZwftA4oTQ86/Qp3k/VC6Mw7e7BfKBQJrfkBsU5zOX9VANx2LGUhTks'
        b'koZvqWEXJ+d64kiwOx/bYSwrUNDGMokIOg7v5GwwG2Fag4XTl3oRJGAbQcNOWZK+x8UnsPUAHwA/mQWdJhZYvAdmmTgsC70i03PSaLZILcFK52vsYVE25GMltyUXNTMS'
        b'vz22XBQKJFuE0IZNOMiPeX1jpom5MdywXh42Dzl854DyHTBgwld8ZyowIZ+ZrGAtTG7CHAnLKmvh3H+yUHaeaQwWupwvTFZLpIIT6dxdOOEdRVbM0B1nT7GSgfzqNKBB'
        b'DBX7LbhDXYsFkcy1x5GAcgJmRgZUfcWeGjQ8ww/ffSxdgOXokqDP50RBuYW7GVe/krVHcoYRoZEcKQazKXyZxjrSC6StyrCVdfrgm3KcNeImNMa+5JXFIHX1D0Ox5Pwl'
        b'GOB8lqrubiyom6ZZnE9WoMO67/WKcWEbtD8Z5PZNItNX8+f5MSL6bZQKWxY9L8vF4Kty8fTKQkv2mRQMa07F4H1umWtXcu6nNBJf4svL/G7P8F+K+WdX8bZtUJJGc30L'
        b'lSRH8P7TE0OfuoFv45eQebaF+oCS1EL9xGRLPjibJXb/JH9fxsuf0ynHjOnJKc/yFx1aXGKyMQukW856V5jIOSsjF6m4ZGX8NkbyJ6yM/78aySNJ680SPra9xXN7ws55'
        b'7QfeIs6ePbhGtGTPHrDm+tymDxsLuUqsAQJoXwWFxWuwHheImHR8jU07OZu1XDV8DCxSQmMvcJmk38pY7fhcuLHwDHP1MXYmMOL4yGI5QR9EBu4e3mZYbbJ811i/quFa'
        b'd5OqPeTt+5pgd86KVih8rmD3VfvjPmm4lnjx9te8cGy+BtOP03kWEnnTY6ebKfT78WXx2S+8PVgEDAzATSXbFGiN/oFVhjCFEaQXDXQDFz4KMtf8MOgnIUY6O4M9gmMj'
        b'YkM+DvpTUHzEx0HFkW7SVIh6I3mL3QnG4lR2VXAbq/WfxmE0SCJcZDLEYmJ9pGW7H+INPlzprumKiuF8tFIAVnDhPf5w3XQ5HJL6vwiKuHA4ZTH+4dncYtHinnztmwLl'
        b'SlP6E8b83BX2dM/ngs+JZ8RjMwIIQ4bQvRJAj2/+RgDKWdd1j6i6GsN1YxEv8HZ5ODLAdYX7Qt62LjzEfSEnuMKe98UKIW9Yh5no6Ic3/keYsou+3aWn87hlPTbSLdSL'
        b's62vW2Zbn/xtskDwPReF7KknE9Sf5Qu5LnxeA3uAsqK6JFP3aXe5zM7+NdMfea7b+87T/SFPXxSRS4bRTycahwWc8Z0RDRkiGzJLZEP8jcO4mfm95wmd0zk8lZRtKa9d'
        b'bll5urYelxwewWvGT4TQrKJQJ4enpiXHp9jpOyy1eJeeQpB+QkgM6fhfowivzjBlvNJYpdYz60hBKJGigv/xALOTAcsCvh9Fe0POLgWoPxWTDrVpjDC5kh7cuywYllOY'
        b'V+qFPlsclORIL+3G+uiFP/gKU1jZ2ZzX4KOgj4M+DPphSFREfzjzFgR+JxCHK0cCu28YyxhtffHln7z+3ddfOC7uukhoMNaY+/vamFOjjWNNJa1ugb6Nh0d3l76g3LpO'
        b'UGOmcdlJ31iWt8PP4wMRqUXa2LeUtrId+niJuxEbIx+L/VTA2Wx1X76EfweJ9befjP7EezglD83KfIuE63EupNH5eHA6ndAKZzL5sTsk4e6PDARKpLG3nxbhfVWb1G0C'
        b'rgdyM+Q+1rqBppteIsYblFfg89MF3OW1KFjyjBRyOAy3+7YYnshH2clzlVoy1z+GVMuG58WHPmkUHGdZfySNr8ob+kT8Y49k8AM0hN9zUYL72k+nBM9Y9NOJwBPRGt9U'
        b'aljM4phYFf1Tn4ybSYhYTMf471MDB37Ob0gNVvfykfD6gzMZMilMMHCoP/JR0NnvvPzCcKXpr0fqOwq2lFhx5VYsUHLlhr2xiBMfNEK2cClNfLQqNAo4L9h6bJNkQid0'
        b'ceihxQrNLqU1eGvwiQ1EK24u+rlW99RufW7edU3AojlXAw7pzUgFYnvRokB8ULR81rDnAtRbz/AQP2MtxjyuvCmXEnwp/EJwitfTTdBMkZUyL1lOlZJ9TgN0yGoG6EUg'
        b'Zhb6MGmJ+m8Ewg5L3oTw1GAWKhfMhwjFJVwibsiKyi+O+38F//w70gOzY3Zqzo9gyozTcWkpqcw4zeNjSmp0PB9AyJTkVa3LvOK8IuyLuRFo8NUs20uox9aaHJzOHxft'
        b'+WswjgH3k4ZoRa80Bt0ndbetYL/bQ57BgGOwB8b5cuY7A01YgpOL4ArWYJ0N3OPqwDj+/RRfQEYikDQJ0z9J1f0TZ9v9+0Xiex6fCVnpzImNJgI/vroiE1NPwD0cNvGm'
        b'sXwEXqHYDHPQHT2kf0mScostNeKz8DITVZGD+tGB2cj0PMf/eUVP8Emuo7pmmNKo6AWDLGWt6ktng9/TifJ6cbi80q2u1+1D29a5D6r2QbezoWNHcHbo9rvrNN/64Rvt'
        b'rV/MFIXVdut/Gp0mLD5edyOxKd7q4z3tJ74f866e3y7tg0l/MDKc+XnPce24lItpJw5k3EwIjbUeqth0P2Go79z2QSefyLNFf/1+5r9GP29sPRT+hvH7TWPSRFtl6MLO'
        b'Rxmru7EC7mMt3uUzL4qxA2ce4/8wLcwOCuX7P1bBBBY9yf/to+WxRZ7vwVmLjVzUjQdnodwmgrYEE97oylq9d5vsXGw8qbBfBNVn4DZUwm2+7cqsvt1qRkoJ3MBRFyjK'
        b'4Oyj/lgruyKr1nUHjLAWnXxKbgvcPbsNGpl1dcm06q+8Ov81lv2mlr435aRJuByldfn2lFZ9sXKGoUida94hzwUUGAkzdVaheTTRSgMfJyYcFn29SEFqxqNnl9n26J8J'
        b'z0Wua3SeTq6fsnQ6Vs6+yNFrhaWQcz42gCBG8KYkNjg+0s8pVG4Z5rONaS5iPmv/ziWSMluYIuf8ZQ5nUaFaoXqhuFBD6l/UjNCUkna5IgUi7fJE2uU40i7PkXO5q/K+'
        b'yz4vI+1XJauQdoewMBapHh+evjIyiDnWeCce73MMTUhODk9JTIgPi46PfEYOKRFcu+DU1GS7oCXdK4gjmoyFJOgHBfklp4UHBZlKY+QvhSdzIRecl/mJwYKf6lXWDw2O'
        b'Z6Q8OYGFaSwG56YGJ9N96IcEx198Oj9Z4Xp8TCxb1fH4VC7zLM7EDoJ5RlMSw0O5HZryp7wqn3mUIRGfFhcSnvyN3ahLgMYv41GqQ3pUdGjUCobH7Sg+OC581RUk8HHl'
        b'i+cQlRAbRsC9jH0+FnUeF5x88bFIgKVLS9HnEzXM9b1ZhHB6dAq/ApIBohLC9O0i0uJDCTzomUWJPGjVgRZXHxocG0t3HBIekSDlxkt52zwQpLEAeObGD151nOUw9NST'
        b'XIrPs9N/PIvjUUTz4rxPi2yWjhViHfLkKMtzQb7mfUYpSHTx9dbfY2NrZsX9O42oDSFhWPjiVS2ORaDPQ8nqgdZHwyOC02JTUxZRZGmsVW98R4o+908WbvHE4lbIN1LI'
        b'ZFtJJC2DPn0D6WyF2KMmJXwrxZ4dXnyHlZu44JRiTQzBIkyYIIApmMRG7hsT6DVUupTE+pttEGKRgHULTDMWcrJK8DboYxY6oUBLLIJyoSPkOKYxa1ocDEERvXWCF5qM'
        b'zM2MsMhiJ4zucfUkEarfLxFHU08e55zhULtTYZ8FlHL+7YtYIVkRBcArKz6Jmkve+9Dz8tABD4BPTv6HqzIrGmj0V59E5WM26YI0VqwShqERbjP5YskBz6d5mhqbuckI'
        b'7E1wTlWWRKt5mON7nwxeO2+C1bKbsFgg1BDALUOY40b3lJPjapwkamTFXlqrz9dJ6b/AJ1Ifd0n3GNBx5n9pwRLn6W/L7UEeR7MdBZxUGJSkiHeYYYYYkpJACcuOcZW3'
        b'uBd+piovIKHPsv1aiLJH6DlB2n628HxXaRq+rwtnY3al5ZeakOwJeXGPdkPfuZi6eZi7mu2UFWCJsXKSS1Qai8KDUTr4MakAC9evPjIhlRqTuAR9fi5LLmVS/GYU4A42'
        b'ZjoZy3N58Thx9oI0ex0rzKWOUGyCWg4Q4uAh3uEz2E/vE7EE9ka4x0UtS7APZ6Up7CGnBZJNQug8qspFtslCM/SHYZ/7UkYon8Cu7sAlzFvjfaySppHD2DWBxFQID45g'
        b'HR8Vl3s6xsQBm5cyyaVp5N7efI2ATg/zZRnkEmigS7+PeXz5nocuQY8lkfPZnbY7uBxy1jLSWInPZG/fzJqGsNIHWOUpkBwUwoAC3OA7HpRA746VhQ9Eh7P2QxvfjmTB'
        b'G6e4SFUc37i88IGJFQdWenhbjat7YCUUcmUPoCaFOzA7WukoH5EAC/s4A9ZDHON2FRXI+jJjkbv58tIHGuu5CR2c1mLJOc9HpQ8WCx9Mb+MrI3SdggfuMIUTSxGyXHgs'
        b'1MMUXxmhcC1eX1n3AOe9s0giH+d7axTgJBa6Q98O80cZrXxOfRlUc7cSC0N4b0VpBJxXglx7Oni2/iSoxi4WG+NjhlPrZQXicOF+WlA39+4xaDTGUZjwJW2q0v84a/Zn'
        b'JoRbUK/MlTP4QSCPWEHnE5V7og7yFYW2XCEUKsEab4lgC86LlAW4EHfCWJGrXWAMeUkpqslpOKKMI2pQnO2GU6l0BzFi1+QMLhAHq7AT+pY/g1MptFkZARRCznrsEWMb'
        b'QW8jBzRqIXv5J6EXx/in01OTFJJVVGUFRmIJXsf2WL6WWx+pM9V0YziekqScBGVqcO9icppYoKUn3guTalwRDry5Dh6kJKUpcgOp4YQCjtDMB2GcvbG4jEPnZWUg9yjf'
        b'QWMOC8KW3mBlxHMiuYe0wsUO+ju4qe3isHbpkcXVwY31gk1wX2IYdoQ7l+T9Z5YNk6oMg8ksskHrmNhOQ5Hv+1KIPThJD+E0TEgHI5IsK1CXFeH9VOzkwEEJW7BECSdT'
        b'2Vp6YVJZQYVkfZWrIhjzp4Ux7Dmgs2dtLN3n8ePsOmVwRghV8gQq7PWTmA8PfBWVPbGKFVav84UyVo+0WYiTULKWLzZXjyUwvzhFRcCyGQgl2nhEr4HSHSk4qZYsgzew'
        b'SyDCHuFOLN+Yxryo4djOei4QnXS3oL2MeHp4+zO+4iNV100ZySx19cBiIh9w3V8h5RoMcp2mMo5ZuWOZeMsBgdBOgLWXNfmOLgs+2IRjLkQ73LNszAjPvCQCDWgVQ/3p'
        b'YI5wb9u2XkA8Tv64/sUD6LNL2rfi0E6BH/3yd0fTDeRF2gK+/4bgi0PSD0aHjSV8m7BKmNGAgVh2CZcFl49Fc4wigXX4gAGYuUY8JFOQeVqN7xvRkYitJltPcRFoGYS2'
        b'E1yTrfPqrHiCbhZ9jBZEW2lGhx45JEq5Qkxm0182xfm4x2xwUB/8ZJ3r/9a9eOiH7/7b+csdv8v487FfvhGhITqvY7Auz3LrfvVXxC84tk8kdoqjrMQHHX9gPCpve8Sr'
        b'UusPaRV68jeC+wc+nL//yf3MBw0nrt4LNwza37Tr1qVPzXTe32/6xkxVzbtKhedq/uJrfF/mQPqnopn6Ms0e96rbHx7e0f27z9f98e537HRKcn7u8YdzZqkWF0cCfmQR'
        b'IGPc/+Zu/43/PO+Z/3Ku5sd3e8+7zHfNzxblCWP/aHJKqWa/1X6x6sUtpWuT/Y65vRqi8f3dCr9Iei3/twM/DLugVVMylCopq3l/15fZkvIv3/7d+69//H7O7O0wxf+3'
        b'6xdV8R/0akeqxtt/d3/m5xvj/pB1yudH8POkej/3H/XJ6Fq84JI6/qeSM2bv7jafVhie+tHgyb/Ca+s37vtZY2rA/t7R+s9y9X8daHh+9I3cCXgz7aLvxb333hq/9OM3'
        b'487fymqE77zkdt3shbogt79uCxx9568/OmB62vN7nW993PbD3/zxtRcD/lz1sVblyy+af/Xbdybei33tnatusnvfVsjdaoZi8fvGf7H45NTc5VO/fqnLN/Tz93RsLh88'
        b'/ZvEtwzOm30Sr/rxVrV97312+fgXf2r6SYLtsYBLGeJ73/3l55e1Jvq6DF5WVUnTvfDGx/948cyx3uzvLoxf+PMvd302cW3kLtS+XdJUk9X448nPW2ZKC987+rc39vr+'
        b'v80t6T0lgY7px7oM7niORfxja2bhmd8U/0yUdHxjb1H65Yp33zQLWRNW+PIXB3+55S9qRWpfVBbuNeu16v2krxFf7Vf/efZGszm5nx7Q+bnja9a3/F/beqe/8+K/vt+v'
        b'lG9bczugaGCHoXXMJrVzDzLsUg7+M8rvn2p//8duP/t6555PbHyVMv5W/M+fbxbs/Jd9VrWxOWdhCcM2uCt127KOwosRFZquYmiHDqziwsA0oBTqeWFCDac5aWICCjlD'
        b'tgj6lKTlrGHgPJR7c09pYKEYSpOgjy9z0SOJZiaiY1D1WI0QAyIljGjY43UYuhjn7rG8UI8QcjmXPM5DLXFjFmtG3HYWRlYGm+F94FeJA9gTxtmZoOYkHwynJG2hgBX2'
        b'OMIXkMUml8VguKEIfvwCWhpnZsonwehxU5MLjNMpMHZ8lojwnaXycFCYzlWIM8AhKOcLvFXBDaGJFzF82RAcFUh2CaEPWnGW+/IKq0zB26BgBuqldqgAU27l1/aeXTJg'
        b'XYngIwu9t3Dv6WC5irQsLlZl85VxsReH+Bnb/cXuJiRGlbofwnriz5dF20jWLuSWa3AwiGv9sKxKMMyqXiXOcJd72Ru6sZu3+2EOtvFuP0O8ya1ILTlleTijKPYKdPht'
        b'4QIOZU+dZ7XoLeQE6+VF0Cn0j4c70gq/RC6nuXweI6xmKT1wWw9aODthADQnY4kpyYVY4u9Bx+BpSpzfQox1MIFjnBnveEoo3ru63B/IfIHQaMp1Jc/EXANeBlM7zkQw'
        b'OW/ehTiMc4y88mJw2YVFMXhYho/avEMjzEmFXWjX46VduuV56dtQtRbb/B6Xd9Ou8pbL0rPpUnE3O5OXdrPS+LLD0zC7wwTq4O7j4q6rEZ8VNYF3YWGZwLuPzqYR6w1S'
        b'DdnrtVhweVWBF29APSfyxsE4v8RZ07Mm/pk0EO8EpWkwR5ywDRu5S9wVTWOVkHDnbeYF0yIGkDthBO9yDtRUVVaoaUnsORitloQTKjgstIbrQlPslFGIOcKBigtOsZpN'
        b'JdJ7kcdmUQbMkTRSp8bXsqnD+WxpyUS4aeFqqsq16d7gJIE2e8jjE7a6xZDL1WPcTVgjkMMOkaahvD/hDscbS0V+MIAzx3mOCbcz+IDexjCs4wu8wP2Axeq1WlvFRE1y'
        b'DnAe5iBSHwf5R8w9sdgNBzZ5mtPc2CiBVnMY4e7jGN53pWcu04Xe9DYlOYCuRSRYu1ty6NguDsfNT0PuYwVCueKgu3GMqw8qj3PcSdhCf5ZFMlc8spi/ESUoE2EH3Azg'
        b'8MIwgcR9Zg2/aeobRsftJdLbD3ypGyy20sKSfebSON+lGF/IwWbelt6GNwKMTXBM7ZKUBipgnwgG9xCd41SbhQvxdAdmxkYMZCJF2pakIBb5G6v95ylTj6zB/8U+3cud'
        b'7MFhYSuc7J8yserbGcj3sAYqqlxIrDZf3oYVtRFu4spPywtNhZoi1aVwWXmRSKjD7NHSMFn69HjLli8kShLhip8vJB/LbpbnxuObtfCWbXn6X5krqSNhXbo/l1WWFbLS'
        b'1+rcWlSFqiJNoSpnrJfnCu2s5wrkqHIhu6pCViBHlQsNWMWVuuxYpOZ8Bd4mv2QeT3Zkdvolw3jy0ZUm/v+s/LgcP8+jgbkZ+cmW5ubcAy70qVhJ2orlW7kHcgRfmH9z'
        b'f+6yAzEWvym/6D59lIYYKhE8+k9WsMwodlYg4LOKeK+AgtQrIOT8AswrICrUKNQsFBdqRWhJfQKSItk8QbZMpiZz7gYIrshwfgDJVRnfZZ+X+QR8Rav4BPwTpUHCK10C'
        b'nHE8WGrcXfIDP93QvvjEysSjVKmdetkQplJzdWhw/Ko2zBDmjtDn+hoxe+PTnQ/PY5dnno5VZ925uLyd+lxyEWdCXVwHbxDnl8S8G7T0eN4IvbpNXN8xISzcxlY/JDiZ'
        b'M+LyG04OT0wOTwnnxv52/m3uAKUujMfrHK3me6DhV6/DIbVsL9r1mSn960y/39bQu3o3os1eaSxFF24nHXNfaohucuIZEWblxpuhQgGHsAly06wYO6mQM11uVHVhPnIs'
        b'8vaVWlexIZY3sGbiXQUSXfgW2HgPxnYy5zh02AhdBFgXuZdTmW2UlAQk/cnru2Wa5thl8O1ifqE+5quSmASafLuYL2O5AFEszIBZE+hlgnQRVvjSH6x/G2O5AY+ifkkq'
        b'bfZbTe0X+6tgj24yp39fIL1gAcd27mXRrAJPOUc+mf5l9X8I1EWvx6lZBoXryjl782r7602H/bivtxieFvxGIK+pHJQTk7HeOp3/2qnzMN9hySJG+KpIoN5ukbrBP3yH'
        b'gFf0H0BThM2eGLoAa4E19h7gQrEDYXrTcvs2Fpm5eWINs+iSvOjK2cthEkcsTnCNmNxPuLiZuvHCIElUFSpuJAbWc5fhquj1WJzgQfmnByqQimAs5C0/k0Yww0UKQT+M'
        b'PlbfHyewiDN8RkbgPG/3hLzopfR9fRjjzPvYigNbH5sdpi0fWZmNlkymkAsPFbJDsIA7qUvB0lKiNhdNe2VkpWaSwzH8OW45c1IwLrBUkTmck9nom+CTLMu4B7OYG8vw'
        b'oFRoAU0k9D2IFXDWE5zfwBlELihYwMB+uM+Lgvu0uQvYdRWaTPAhFPLWE3U93tHRjZ10MiWkMjULOPsJNsul8b07ulm/VVZSskQUKSuQ7BHCUNY2zm4aeRpuLAuuHIMB'
        b'qVn0rDZf0LR+Myl1nFKA4xtkeKVgXUR0V+xmYcoggdrNzGH7qoXyVw6rvxj5q48Obdh/rfXH+UqF6mt2p2r7BRjYKUrsTpQdduvS/p+6MZV4Q025v8t/VF78/jvrMhQf'
        b'7t5y+lRz25d//sne2xNv++z6UPaVc2+dchrvefvK7jcv/ey1F2PbQ2cvxHQPmmdlZXSXTc7bToYaOr5XNvnz7Yp/r/rtDO5IHQ1tuGkn+9m70fodjTbvJT4ce2Fuh2Hh'
        b'K5EFn5c0vJqd5RBxYPNfb162fOvM7rd+Nnu9ZKTmZrjPunuvByZ9afHmV2c2jP5uWnEm7GOrf1TU/z7D4I3dg8MKMQfDzt75ZPqNGbmUqMNhB9akG1jHH95u4PzZuq/e'
        b'nZj+2Z6fHlfbvtduzccpFysOavvkDJQ9EPr/78f3Iq9GHAr5+/d6X/++7MOMn772Uaz7vEp3ebzSq3l+lYNf1fw2v/bs/376dsidnRl9X4Q4Nv5N6dUPPSaS7I73z2+y'
        b't/vnL4+19jk6X3R538ftta1vXgv40FjXKumlhg+U/9r0q2ADrSQTt09unI65KnH+OPinAR8YrtuZKFP7hvl3e9J/d/Htv777D4N/1b1evPknumafXUsV2v9qw+93bLAL'
        b'P+nT1vnjcZPaL9P/sPBPmV1rm+qOvmmsw5fxrDeS4bRZWPBaLL2+4MsrY53YtY1XZ+GWslSjhY49pznrRBR0YDEXwbJWYaV1AmbieTX7Dg5bkvoFDdAlrUcRKzK4EsCp'
        b'w6oboIfhVRhUyfA6r88l7otd1yyZMeIkjkkz8w7BMJd7F49dCnxUa8mhVTIM8P5mTh04TTRnge9umeEmbW4J+VGcVng5Fe4/am4JDzOY8Vcs0oES7tU02yS+e6UFdC/2'
        b'9mmU6mnhx7Gc9cspxz6ZR414VOAmr27eDIY2E1qNK07jNIuXUdgogsoAaJOq+FdVTcygB8qX6vKb4VQ4pyQm4cAxXsWHZvUlXZLX8e/BEKcCJVniJFO2odeDM0246ZI+'
        b'u0d8Flq38aaYblEgp6ZhhSdRUmIZJrKCDaTPP8Q20jVJna/gTT05/rvYAB4wxPUUlNUTSXyPcVMonxBzI0RhmcUKhTL+MrfMY0FYuUydlOqS2AglpE/uUuBAwiVcm1/F'
        b'yJaV2iSt4zpX1RYe4jgWSDVKApYVSiXfcaKMr48SuSWWU+rwNtZLFTtS6+7Brf9Qltf6Lypyj2lzysujETh1rp8xgm+nzl0TmCtzapWitNOlvLQLpinXVYh+I6ZvRBJO'
        b'qZJwz/F/s15ErA8Rq0qqyKlgi0qfOqdyKXNdilhSFa+UKXJ/6nDzaHJ/Zm54PPFh2X6kepgsrwG5LmlFTPlYpnip/1+fr7Fk2WQWSzNy2pcX0ztIMEzxYOf87bQv0r8s'
        b'n65/PeskFiPFrNiyrEWr6F5MVuXkVKKwAj4XRFreX8TpX2KmgUUoL2lbkm+lbTmsFly7qG09qvG/FCvLhdj+HweI8+8sFrjh31ulpKW5viMfXMMt5SlBQ1w8OVPJ6FFX'
        b'X+99eyytmAoUF5zKQkNSUpOj4yOfugS+ss6jQJnHCwny3z9X7oo8n7uSvRHycZCkyG+YvxKjInLiAw8aApkdUOqzTt3Oe61xVJn/tuZ84qLPetPRxWJRpTjK+bwlKgrL'
        b'mwHgDM5KveLJltE9v9kqk5JDT/3B38GseEQFLLWP/uV22+H2SMF3dYu2BwkUSwxkjhSkemnt/b7O5z26xq+99UpW8oe7S3/Q2vHTohCF196+q5bXd0j/1yGf9v05NuR3'
        b'NzIUXHR+s+5nd3T/8uHRP9u863nG6tcNIUlpcTdyfvh792uflw1+Ufxaell63/xUrsfFt9bgu3IJ7lt/+4ffGctw9l+7y+ekcbHYsYOTKFxwgjfldVpeXQqKJd7RLi2K'
        b'Hgo13PcJIUrSmNjQgOUSBbbL8mkzd6AlctEebgFDWLicW87ac9Of8Dznbyc1tXOGdmiFghUJL/8RB1lG4FXTOCxbQeK9nofEXxOsX0yO4ZsZL5J5RtQzNz5GfFbOupIQ'
        b'r6REywjxtyu1TVSWe99qJanlqOxx+t3l56ayNw2eTmWfvVFWVzYzOpEZaf4r1SWlmddf9T0ZzpocGhV9SVpcSFoad0U5o1XIqCNvA4m9zBlNouMSY8OZ2Sc8bMtTSa50'
        b'c4+X1KFff5PWKoJViZbEiwvTSIHBZM6rdcnjGcFSIWvlo6E+OHrvRm0J12u4ttCZZZQHfuf1F8YrR1w6bxjL/EAzNCoiNsQ0OD4iKsQj+PKfWLq5nOBuq3yi5lpjCYeB'
        b'rh7HiADE7F/KiiMNoFpanu5yCKdRYCeJyUsqhb8sJ2NiyUYcWAyKh/4ryylALdxJZTCI90+SwDjGBOURLGX9K3kbjyt04X3PJCnVcIcBORiGrq1f29dNPZi/3EUoS+Gw'
        b'eN/zYbEtw+Glop5LxtrHZlhZ5f3ESjxdWcTy0RMc6jHDapPyIpX5tqiXI/jgGVmuX7dqVkFCxsvLz8nLWOTF/6/+NUXxHlXTYIm5XE4el+/ERdFztnJOZOMoCrc3/mDW'
        b'/bdF9G9I35P30EdVJWnyv7xIoqQo1Nn8eH07dXV1kbxQW01eqKpI36+XF8r+W8IO9t+GVzWF5vGaQv3N8tKWXDUwo8GlgIdhz1IWOMsBFwmMdshcco1O+5uICwUaIIxp'
        b'g2r7BGyxVIcCnMLZNXv3QE4oDsnaYRFUQbU8sJo41zerQCXmQzupRjVHj0KnElRDsXADPoQpfKgCTXY4DuUwGgwT2OenwjzDeThkfwAewrALPHSmpyqw+DJMQR/cM78C'
        b'dzzg/oErOI935XAY+unnwW7oJk2+JzLJejs2wfUoK8zBjni4hTewD0ex5Yo9lEAPqfkja52TDniTMr0VcxyzY2ywDOdhKvoAFlx0Xr85eL2TnbvMKessc2+4c0rPDGpw'
        b'4gDM4F1SzyvjoR+raJhJF5i0jduJFdYXsFQFe8JwWIuEonaoJoLBHND1QY7YfNwmBspCcVAWbsEkFiTACFbhLV8chOH0OOyCh9kwiw1+ULUOOy+ewXro2rsG77vArCWU'
        b'0varoFzjKAz5Qt4Od1rAJDbvg6FsHDgBTULsgWaS7WpJZmjGiijoxWboTN8kVoJaGMfb1qakS09G7VM8wCI5QvUgxzkOboTRsA2eMGcc6pSw2QnLo0nfbXHDulO6MJjh'
        b'gNMwSjc1bC8LjSeM/WnfJVAH+YqGfjimix3YSf+a8oRCaA2kw6iDBlOc2ndwu/02bS0cPUm/aM3accYEm7BfXYsEnkqY8Euh31apKhrgAr3RjyMkCU3AMEmYNuH7seks'
        b'tFjDnCbeVg3xhPLI1IOY44MNm6Dkwh55XIBpPS2YjoWFDVAQSa/fSyRFvdFKDzvDDE6etrcgIO2DaehJCSaoq8dmP+V1ZzPj92fhuN65jdDsBZ3rzuAQnU8D9srTZsYJ'
        b'pJqx8zCWykPhMXxgSddYDwO2tMt7tL4pyAukG6gwO0TgUJwBo2s3YDGdzyy2q14V4xzedN6G065p5QzwJ2FqHbT5OEA5wb0yzOHYmiuHmV/+GORsglZsNFPehffpfkbg'
        b'lvgY9IQGbzWGyigJlOhfs4DufWmZUWpYR6DYib10sqWJQQEwvyYQmg9DM4xAF+QFY+tObDAxxGl8AFNiGFbA2g04GSyTiG0w7n8q/RC2ZPvGwgC20EHMG3GG6mYcjHff'
        b'T0Pc0oMWzD0eSGNXB0LDXmiEwhDCvVyRrSdWw7AZPTOKvdCffSZbSz3wWsgu50hs1bi8S4M0hjniv+0EfvNwfTfh1U3nzR7bLhsSqFVAE96zIhAfINCcxqJgrI6FOdrT'
        b'MZyFm3LYfRCrs+B2mrtDNA7uwEIjYp8LV/aaX4OC8wq+MK27iVVhw7sa+yQJuBCEoyKszNAJPoY3YEwRSq+6QCPm6jlD+SnIwfwwNbgNvd6+/tahmobrsM/BWVFb09xS'
        b'ZoONP96KIBxq88AiX7rhRuzXhSKiKznB2LOHrnIWrmO+GKu9oApH9LHVC4sDsR/GJBoEfcVroZN2wkhT/gVrdrhQhPdgPD1jHZRtoikHCah6MwgeCjM15AkfxiKwFmeu'
        b'WGsTuWuEG3Q9w0S6JuQjVd3w9jq4j+2nT+IAoV0+Tm0+B/Oe7rAAdxW2QXUKUYQeKLANx7E4vBkI8+brmT3wrDdMbSCYG8AyH6h2d9M4m44TNF8PwcKtM5BLGLRA28q1'
        b'xgGtHb7b1nhDLp35xCnsjqXT6/WGUWOcloHGkG3QQSBWmPYqgWQG5IcRRNpDBYNIWvaMCYyn2WLrWQkN24434oOhPUmJ8LJh93FT6FEPcoe+g1CKk3RYc9iwgSDpIRTT'
        b'zkZhyBUKzhC65hvgvMvBg/bY6AZ3wtQVMZ8gtptgagpubIVm/UsEwg2igzB3WbDH3BVrLqaa0MWNQQ8JTsXwgFCnmnCuJeTMuXgiHp2m2BJDpz0rIFAqJljthztQj7Vn'
        b'jxFRXDBZG5B67jy0e9IKu7ASx40IN6oOGVhnYKm2Aswsh1jCj/rj62gdE+mYZ6ZwDcbjOXpZqwr9ksvQRLSyx8FjT+aWUBj2yrqiIz7vDCVrITeC9rZAY/QQbcrbc5BA'
        b'uFEuDsrg7gWoUaFL7tNXgZp92OQC7an0SC6yzdzGW8SX7kKOmgjz7ImKdK+Rg6l9+EDXkMWNwwNrfKidjnfi11yWRMViDtQRyhZgrRqdVRftsAfnYOw43WenBhaf2hhF'
        b'0JaHI4eBlZ6bO7uDWNP9Uxl6BL0dcfZYGUQ8rMEY+tIJJ0rN6TY6HayJzN0kuCTeeXbXxd1YZRSDvdlHVDNpgXmQQ7DcCWNW+kZhwTBG4DClzBqZP8A8ZSxyglvWfgQS'
        b'0HGZFnATK4xgAjqIaVdkYqfchm10zrPY5XTKAh5iq6LTTtpwAdHIdmLcLUdhzDnSh+5yDK6nnKIbbSJ+eBtmM7HkEjSekwvHevsIZ3OOqVe4pxK7KUgjslBJz9QfcF4b'
        b'iA3QchGKRZd0oZXgm06Q4BtunY6hVS7gbfH2BDcnvBmvglXhAXIbz+PgehIlCLgsCJ87nTSIpg+l/YLJNZuCGaWN5wSMORwywUnhsU1B0C6HTT6KQhhhscXlhDONUJkK'
        b'owKittvWYI4VHW+jXhbel4MH0BXubATNjjCgRcygeR09Xq6KrXJxejEENc1qhIuN1sb40N/cBVpOZGGtHpS6bdpLfGBKkU7mIZbIHYe+IIYswcLEs0wYaovHIZw9F0DU'
        b'gtHfe0QGSAJJ2AMtWodNfDRx6BRUBR2F68fggTq2O19jWa/te7O0oNTX4xT0bcfxaxsdg4hs9LNGX3F0JgPQcuayEOudbGDGzzJL1RFzoQUaD4YSW75OV9ypq0FnXYBd'
        b'YljQwGr/terr6YyKtaHynEewH2HuvM0Ju1jC4ZpAqDGHPA9tC23sjYV7hwn3imKg1hCvOwoxR+Y4PAg7AnVO0TCmCXkHvWAWio7YOh67uh6bCPiJLnbTlIWCOGICnTgi'
        b'C+2EBTd1CFtG6bQqsNUa5qF0HeFp63aYzcbJpIMEtI3E6sqx/kASdjoQTckJO5EBBc4JhADt2VCfvYbAaiLsMvZF6mIjEcEOIhTF+7EsQGMPErxXYpczCUYE0d36e2kN'
        b'bfTpzuG9Gc7qxBaProcxXwLDKRi/vIuwfh77HbGUTi6fmN7tvZuYQJYMpRH6OxgoYpX2IY4adNIyc+AWKYohGpmXPLGVZhkntCIVL5pW00ciQZ4IytPo7EvXZdH2WoiD'
        b'DhDjTAmEDnO8hV263iq+xCjuxuhgRzjWudIV9+DsWWgLoiXeP0jqYhcW2cINZFg+j/X+NETh+ahLjAVhbtw6HEsk6jKK+ducTivi8AYrpxMb6cTSKgisk+LpVtt8aAdL'
        b'IoQJTgvjsJxECPt9JjBlCcOXlHbYyiWT/NrodBKrj9BOoN2BrnieJh5LpjOaZAQo0AAKbDDPivCEZi6G4cQse+VN7jCPQyF4m565T7Sj4dpmyDE5SZc9LdlHVLAeZnbu'
        b'OYQD50hCq8OZcJIuy4mH9ROHnkCiaXnXzLBWk6C26Mg5aHfDep/DxFcrww9Dk/9Okjm6YNaOZisnaaQd5tQItdugQx37XKDcKgOrVT03R8axnppyhB+3shQvwPB2u6Me'
        b'uvYqBF/3oE7VbKOEjqxNUdMWxzcbyoud8PoWOsWc7QT23RobiL2X05iDZzHvHNQ6AJGlg8QEiTKRhIAPLmAr3tqfRNSKhWg202pu4TBdkvC42Uko2R7POr7BPW/MO42d'
        b'Z+2g2MPUk44tD246xmzwdj7BZJjic1ehJ8QYr4dCjlaWPjYQs6o6g5PJBDj1J3AgCIvMLKFBRFB22wMLHQi2FoikD0aeI5WkklXSWadLRzwehDX7sRBuJ+yjo++1hoKD'
        b'BDJdWGV1Sjtij613CHQF4XTCWaLJ7fvVFLfbWB3Yq73OxphI+rgy3tQ66rWDmOHCdmj1p3GrVQiyHsZBsc9JQpEHZ6HdEHq0w3AknqZsoY22nSdE6D4TvobITzUMmsOQ'
        b'Eh1nMTZEws3NMHou8fzaQ9AfSw8NQlMEEYgmcQytK8eX4H3cBirsYX4HsdsZvHFNGx8KYrHFhEBh0CztdYJJDdKkahlQ5sZzMDlPMJmBA+HYe1mehJ48rSw6wlzDjSTg'
        b'jutZamKNOkmSAT6ZLlB5bfP2rDQoCNY9fkHZhxj4HfYDebuJ8NcTFaHX7JnQdEVdBe5l0NU+wNsnDykRp5yEBbUg7MamGOK0d2UwJw3r/MKZQFuVFU/ftoScI2HmPic/'
        b'AMkPszAfTfA/FqKL+cmbsduIQKOTsGfALx6rrugTeWhlAm8UraHovF2crhK9UUWkgzYJJZ6nSNLrz/bNDojKMFD2QpJZ72C3ARHvu2cPZqjS+ZYAw91KmI5PPKgJk2qp'
        b'dDq5ySzyOdDLRmEbDod44XWo96VHJuGGHParhGPRCdaylX5dmAjNaqSp3IBbGTh6gaB12ELZxI3oU1O0ulPM5YOkO3VuJCwdYvXyNhhJ6DjrLEncrFyrDbXx+puPEbre'
        b'24gzzkS4ykg9GSeG/CCeBe9jddJ27NlK+m0/3siGZiMzon/TcjRZHvbYOIfbZGw5G0GInksIkZdGuNCsCNVWWH7RBls8thM6jGlppIQQ/ZvD/tPYf44wp2sLwWDrXpJY'
        b'pmygEKcTWZw3KeFFpCmvtdQmetlwiIj82P6ttOzKKCgjkUEGe/2JWxYRqNYcvIgT/uswXwK1OBRO87YRuDULtqbbJ55O0TlOVzxisJMwpg2qwlKh9WAGFG/FmzJnsSQG'
        b'mg6wDpIwTkJnA948yTITSC5p1fZQhdtuhte8CUTv4f3MU7EkKjb4Hjy2l6lmA7bQ7ZC88yyXUVfhCSNZ0doRRIOa1AjCx83wzokrzljjtJMg4v5aA8y18IjxJwI142ks'
        b'y+eVNhpDp7urjEBoISCWjsWboZb7IgGb97DkI5Z6BBUxWLuJZBmuel21Ad52NxEJhIcFUKZPuNlgzkWzyOCcH0sgEB4SWMhgU+JeLpHwIizsZvZ8oUDoJjgDBcQO6qWF'
        b'n69EEKyXmApZTRK8nUwy5dD5tGNigUD5GkmXbcSLyggrmg8r04kPXVXcfEYB6vf7qAVrwaQ1Iaw5gUInnVIdE9cN8YarkycUxBzUMSZaM4Xd6zKJNXXALVd1hzNEviuh'
        b'NQQrSFwhBMbbe5jFhRTvqgzzNEfo12EiXjZ0hwdjoRJ0JAcTytTAwkHICTiBdV50j/Q94WL+MfrYBXe5PqD+miS/tVjQdbVZn95GUJe7kZSBkZ2naNwKgTfNmR9ONHWI'
        b'2G8N3TPpN9FXoMCcWGuVH1Qakp4wStBwmsSXKkM6xUGotiUlKT/1gic8dCdQ7yIuUUJANapHClMeKWVFtsZXoNCGZLcHdHDDxA7aYXgLScK90LQvfN8lMVbIhatho8tF'
        b'6NuD08kmm3HmPA6cdl0DfXJX0sI9ky8QAa2CLgVmNIBGvXWYS0c7QLQol4hjz9nTNFYpnWf9Ke0YQtgZWkLlbtpqj/16xQBlvBUaxGldzWLMsyYlJodOZRCJjC5YQ6kY'
        b'h0/t9LbG/ECiaR37cdiQkOaujQmwHI8+qNxPslAF7ScneW2ahDhTZQrtoQvmj54hWbIGinfCLTm8F42VLlB3CNv9SZ8qJa1lXm4NlgRtCTV23ID35KEuCOqSCUnmjVXT'
        b'sC80ORl76Kc6W4WWe3PPyUDSHweJElfZ4Kij8xWNiDCYMFKBSVW87UJIdX0vDlq4El73ERwys85NNdLexyF3PbReIBoA9YdcTnudSQ44vZaEoSJi4zNr92FtsoUNEYnR'
        b'S2KiDd1wz0wHFtKicGAv6QGVO7WweS2j4sTuCi2vEYZO7CZJ8SYzRBl7RRA7hSkLaEklgCqEqTNQGE8cvAv6jzIO434NBi8QOtyiKx10s+NsL3NiYjG3z0SSHtUNFXvX'
        b'brhqQjLnuBdTIbAqAmax05L+WMB5fR2oD08xTdUlYWvgIE6fV8FcFZwTwq3z184cUkrrZ0aZcsKh0setMkRB7x/UP6x2Ce/pyK5Px44wwozcEKLJI8fPYLGbto4D6SwL'
        b'0JBMZ1mgpC1z+oKHD1GdSpv1BDf1MLQOe6x03bccgLEs0gUKA3W9zUId5IijTZ84yZlnRr030yTNULOHTmROkXYwGk8EqZO4yXwUTqbBpDEMQckBE8KLHmyNp39UXNoF'
        b'zcTOiLJXMji9AyM74b5lAomEt+xwNOwMnXKB58m1TMxEItHdAUIS9uYIo3P1CHlGnIm73ZLo4V0T1v8Y72idhF4Doqjl0HI42YME7FuRJHbmHWaEdQRys2NJst9wmMSE'
        b'O+vUmFHLA+9majoqQn/cOaLBpbwFICWUwL/y4nZaFrEy7LhKZGBGj7CgjbRbuOt5XhCDhUdiid60nj8SSTxhDFvDaYXVqcSA8+gNEsexLTQMhmKP78XxterwcOtpgoRG'
        b'bex2MGcnshP71objTDQBDRPw+0lpmEvG+fMyB9SxaYMVVnsnEj0r1cJOTdK9arJIjMqBhSQSdMYPQZ+Gt9Ehm23Edtux7pQ8djgT2YYWox1pm4yjdY47a2pgu9a1NDsV'
        b'KDgi8oKabGRtrXsJPHuuEiHoSDvpAiVniNBeN4Fp7XBCyznCi8nsgDhilPFQLsYR+vc9EvNmgi8RsW21vxKI3afMiCo144AxzB45D4Obt7sSUahhd0z38JDoWhMRh0EN'
        b'2sk8Llw97kGDdu2G6rg1zt4094MNdCSzjjDtQBS48IKMwaFUApWptF8xcL17hXW19sWSJdU2gKYvg4Zdm5l2e8pHSQgTmljkBUOyZjB4RlYH+pBo4PhugoQh25M4D8Xm'
        b'0bYEo1WcxaTfwIzIGLPRNWmYQj5RNQLSAhgm1QAfpnubGdOVDeDcQQfo04MmNb31dAGlMB5G6Hrn0AEB9K0jwtK/HZpsMWcLEbtRuBeIt/2hxfoU0Z1CV2gNO0UsYegk'
        b'k046seNU8g4ZcdQBrLfA7gy8aQ6jW/0wL94SumKOEFvooi3fJam11YkoDsx4YLHpKWIcLTsJn2+YbQmIwu69a04n40MvArh6Yh35u7Tl4XZMPAwT+bpFMwx7yREeLCR6'
        b'k9JeRTBTCl2ZtGliVuuxxwLq0oidNHjFEESR2tJgqhIP+Yr6djhoG42NbjpxMAd9adhiCw8ckrGBzq4Ch09uggU/wT68oSKPC2JaZYHnGpiRYWaRO7bQE6njAvXHNqy3'
        b'JZWrmLaEg/uJjM8RTAwRHkwRIMwnkeZ5T4sOvSkklOFORJQRUdUy0VmHyCRlmDiDPTHeXtER50lGHVWlJTQTux1QxFF3KAmFhpMma4E0jOtYFqMcjPf8oELrcNC5LLzl'
        b'5rnRCqsscWRj1FkstxExmZWoUD5p0LdxziPjCu2+JESdWFcHPtwk2Q71Wj5YEBrofP6IpxPheKk91qXsC8MZA6JI91knA9ILZS8QebindEqPIzGMbNfSQTaG7oIRnDAw'
        b'JtxtxDuXCeXKYdiI1J8SDTnijv2JgWtYuY4wnD+eRHdThiQcVCrApOZ+c6Jpty5rXVPbgawPwRQLlyNChkUX4NbeOJjMhqo0ZzGL1WQzrABu0m4nxaK12ItVh9WSoUtb'
        b'NmYHEd422tEIkcV6K6GbnyvToEJxOhTHVAi5JugAOkz3q2Kl3umNEoLyZuLgpSTB38ukI6/b5afgD/f3YHMgAXgzUe8HSkwjhwE9fzpz0quhXAfzfZ2Y8KNFgw1e2Azd'
        b'1jh4bCeSROO2kfUZMIDb5psJR+sOQMsaOp+WFOI8d8NhJFCPQL1Z5LNrA9xZZws5IXCTBL1eeyKKm/2NNxCtqI7CPAUYCU++RswrD8ZP7SHGMhbOKHmJXOpxG+hT3kun'
        b'UIFNuhfopGY0sTNyDd6XN8p0OJC0Ftr2wpDHFYKsbuJ+Xdi0DidT3bBPk2SdCmKks1HEEDIVHZPpIm/RINUG+1Kha7/ECgcPbYPeg4rYmoqdjGCpR5zThR4N9SSoWYOl'
        b'7pE0WC7UmspZe9LFkrhBRzMt0fdMPLzXJwbvGxCB6CNcag0ywAUnomEN0ObqYC8gBCnm+mi0EgWrhkmlCCzcTVyahQ85wvB6BSFRhKkLZ4n6ddO1TNOo+RprAoiZl8Ed'
        b'ebgRBQW22GdGnKDo6iWo3ncWmaG8UwBj5/dvILryAAqidxC+3dWFDjNC9iZCjWFSrVuDFNbtxtm10OC3zz3RmahjL/TioIReuQ5j+tq2pHbcgR4H6JfRI5RqhYXta9aR'
        b'QFu2EyuvYCU7npvpMCpONNxPv606AJ07AnBmL6uqq7HtwDa8tQ8awwMJdoqwPpk41HzGGRzadcAf8mJTiTzWmgv2QE9whnZICJ18bBTOQlkIDCeRCF1FQlwZndaIHVHX'
        b'/G22pBbOYGGynXuEPSung8VZZnS4o8pCgr5+ZSYe02U2haVkZMO0N/3zDjR7kJJ+G4YSXfB+AMcfx3H2wJmD0GBEvJM0YGd7HHcjIW5IKcyKpLnGU4QdC3IhJLLlGBD4'
        b'XU8Ti7miJ1N0M4RLuT6xBNQMneZx1oRociM9NGmL47ok8wZijWK0IwxswxZHC6gSE6NrV2FP2KtHk9Y4lxXp4kKCQZ6bv60+FmQmkJw9j3cdCAJG4bYCzu2RiyXuMyDE'
        b'Dl98sD0bckj/qzN0UlPyxfowzsE2yKz917KgFh4ws9YdmPGhbRKy9DCbEQm83dDjooNNl312nLagDdZh/wHMvcbqJOgRkyw6C7f9SeyaMJONSrDWhWEXRcL+e/RgmTWd'
        b'bUEsYcK8Grafg3ySDYaJx5RbYeUGOdpjt4IZ3r8SRaJgQUgG3LAn7lwO7WIc1VXAlpO6TroEMveMZNQ34vQhf6hUPSxP5PMB5jiTYDPAiNtuvC8gPl6HFZaq4cch/4y7'
        b'0b7UGEWcVw/I3EGUnqTzg3HHoSIRa6x9SbFm8uiYbdQVgpCbO2BYw86dMLljLTxQhMnAy7E7sXc70a4p0u/yz+ODDEUsOOZLmJFPDL2X7quKNJctdNgNm7BNWVEcsRZL'
        b'TsdEn7tgg83uqsJjOvTeIFTJQrXGWsK4GpiKUXY1scDJTcz+Sfw7B+bWwxRz4d3V20iaX2nIIXuS4m/torPogPsbzeKhymMr4UU5KUApadC0i+6gwBUnDiiRHD9L4kHr'
        b'scy12Kl8VYZ2UO0EzVoKVwjlqulfVbBgEh90GW5tgUnM09znDRO60Kq+1145Ha+7Yb7eBTm86wfVUXALBgiIyn1OMZsp3k1jZi+691kiwMPELPKwyxyLrl7YQtyaRKGT'
        b'9GwbiV1wPQAnM81JRINuQpgaYthFSqdC0k4TSt4GxlRIMu3aQ3tbyAZStKvDSfieSCJoGUzXJaAayMbCa3CTiDkJINcDaeahrWm/EbEuT7m2HBYwHDjMjFMVAcSLiYLF'
        b'HNL3UduGlQT/Aduy6OvWdZGhCrrYtW7fNrrcBbwfCffkXIJojkmSk7pFe3ByAyzg3b0xSrShfGxPBeYDzj19AKolUK9L5HwuHZvcoVNMH3vgQTjxm96rRBkrCJVq6Sqq'
        b'FDfhHTeipAPAmgxUX8EFmD2gjTf3wKwZdm7zxJJY5upyZaaqsON0NvmGRFNuKkuwP3w9Qf34ZX1C8xkr7wQCty4ta1pbtaUO1m/dbIwthsdIbCDMcCRYmNeOwgllbN6/'
        b'BbtVSHnMPwt5jjhzGAYUMlhXWpKB6og03xEQwD+QhTY9F2hQIkWh21INOhysoMmGJIZ8Xb812Lt1l6wsFp1wxJtKeN3xOCnGs+YkZhXa4ohaIk5YKLtbQ6cN1jjYHaZD'
        b'GYNmCeF8F9H6gswgfXWW7zVDZGAGcvUJ0geFJJxdu2RFwFbjA/lKHEzMXCDyvXDRkIhBKxYm0Kn1MCIwYUkCSE1EFNzZR9DMbPA1WLwWx/aQdlMVCUWy0BmlD70SGDpo'
        b'h5NMRcecE0S7xj3SiaM/tJEl4foOlBphnikdzJAOdGZDgwaBRpEBcyfLXJHdE+lHI9ceUMV6Eh5k05kclKe1O56UPuKR14k+VEGPFjYdXZvB4ip86eSa4cH5S9uh3wzm'
        b'nOCOsQw0bSEZqyUQ+i6S4jMId8wukBREjHuPXcIueOC2Iwk7t0OjG/SYWB7DMRniKA2uW0i1bcNRK+JvfQxBmnw1j9qQlD1gjgv+24isNfgEqV7I9lt/igCnCHN2e9Ac'
        b'jVvtN4erHc4WkJRZdBH71HYbi/i8pUF/T1ZZB2/jdLKMtLLOjC2fKVUVfD7FmsC5K1kk4GrC4QNlYzH3nS4tuNOdGZf2CbA6maPVhfxbD6EFyt1ZvXmhpcCLvimN2MAZ'
        b'pA5AxRmWXyURCB0FMcfom5zN3BfumOe0aCTL0SCJrBk6pH2SYRoKdruzYrjWgtRzbC2hvJlscgexyxIPeslWEEtiWoXfdu4LMRTsXDKstZhibTp00VhsZRfiCBlLjOkV'
        b'bwFJU6Tq65FixJnpRrFHBks8Oeua/x5m4KjnNzNviPNSaxzjRSSB9pw1FvK1eZoTsd3djYYzERg4YNF5R+6VQ1vpMhYtco7ZRHi7oNVY6MR1GeKy3LwD+Ry4YWG0qXj7'
        b'OYGxmE8itOR/nRgSpLxXYQtfVqj1AF9V7rhppOkLux0ELLjMiRuNS4uLvvBijThlmGjVA/dPs2sCvDc4aOdHpp/rk1U2/1u5MO+D+b+v16wWGGu6ODspaLr9j6/E4lTt'
        b'bMvdfwquxr5UHmD43pbRubezXvpXxEva//7ky6QPPPa/NSl898Wvrn4yjx7Gv6y/r1a8W3TrPT39qI8eXt/5Wf7vFd+5cSTstVdeTw/NnjXVLXrzRe93Pd4yVPljdite'
        b'v6n467++qpR2pup/nRNnT3yw07ljZ8dv3CL/Npa25nc2GWt+b3NlTdV525daep1+6vjduBfP9HUl106pO77l+Org99d9FN1016dCdufuzgP5aXplYSHbFxQUfpl276Px'
        b'20eL08xe6tv1g011u5ptj2iu9Rut7tI5rHS673uHjPc6pAVqWnvZF+0Zr4l//USIz88qPzn8vqOk7aWHcTM9Y/fb9OcP/tCl7Ls/iOg+/2LY9csRYccuhR26UGieWvPh'
        b'pOevE1Ui3zqlH+lakurW8LOI7d+3LXn1numPdH741hX7zJfdR3+19Yenf/WjwU8v59mc8dmu9ZM3Cq9e+uwf50782Xn+540ZgnWZ6+zT/zqR/97pbUemrtsEfDBzcSbg'
        b'e79JMrzm1vGKu83PDMsclJNqt/w6dWvmawUv/XbnlkP/ToyWqWk+/8rHSQfLg8NcI9qK4qwcektV/13x0t4gyZ0w5+w9H/9larvwvb/s/OPm2qrRVwdG+750+oOl01WP'
        b'IXv9P7+97qu2DV9avmj1wiue77SlvvxBg7Cp08Y5UtN3Tu21DO/55r0p623utfwzRiflD7/44juZLvUz3//fwPbf/mnop/+M9N/6i+9+WT8//5OAUA33n4x1/a/kX5/s'
        b'ee9Do7c6fm+7qzrT7ub2n97dZvZrve354fcSa9ck1Gbl+98L3rjh9e/qTG52fP0F88+HK8R6H371p5/PFf8+yjf7n2kJv2tc+CBrTH3e5ouKa1U+35van3LiXwpXyt7p'
        b'+sm1L3/ys3f8m6599ZNDL3xk/e+f2vxbaUGj13fN/P9TWn/2RM2Jh8aKfIpduzJDFg+OkJCs0YjlLniHy5jajqXGq3SBmIA++Ug/rhgJSQujJ55o5uDwKO2tD/r5YiMP'
        b'jeOUklUUVIjBl6glpyk7XyRSMCUW6GVK5HW0+fj5yqDApWfScTI9yQzzVGQFuofFLOBGwlVZ2Y7DJ1IuKevj/aQ0nFKDYihVk1dRxGG1SzICY1XWo+IGLqSysGI1c1N6'
        b'8vHH4K7ZJSjjhqexPSWyMENax3U+A4AJsHeVpONlyLEEgLsiCxbQy4X3ypE8U5QCZfL/X3PXHxxFdcf3113u8uOIB0hMSTQEMcnlwo+AhiJ1UkL0uFyCCA2isF7uNsma'
        b'vb3L7h4kGCBAZQwkJChIgGI1pUGQH1FAjCjqe7bo2E5tx0p9dlpoB6Y/tL+GMqMda9/37SUwdfyjjjPp7Nzn9nbfvt19+3a/3+/t+3y+rfQYTWrpulKV4uNp11eKTznR'
        b'WZ9i3QZnvgdv9F8n2IJ2er+g2FKAnvxikrrysR1oOuZQPJk9YP9fwM4xLstaPByVZTYO+10KnE8QBH42n/+5IABpzSu4RIl3iU6BTqLH4fV63dn52WnZTm/6hPGSMCGQ'
        b'M4WW38CVg65JBYzLFiUB5vM30Lr4nFurYJks8Hfao7YjAv9N+K4fXeLMuT+3Mlv0iN5sgS/dwBUKfJW9plAoEYrpx0exkzsisdJCKVsCUyc3KMFI6385RwXLgcWRc93H'
        b'WDo60lk0LsCJXxv9PWvsO8WYdUbebgw28hqaCDRuTSA/cecTX55aC+SQHq7AL9NQoxf34q5laEddDepCvWmc5yYxD53Q1J/MP8+bOTx9UEw7NKdnbq1Ymb3wuabfaj+7'
        b'HMt0Fky9nW+c+M5MV/Ynrsf1u2u1yi1XVp6eMel3kydvfqpxseOvu1d99pcV70394+bfqIU3vr/7Qlte/CPyiw+8S+94/+L2Z97Z88y54UH/uksnjgtXl7716HAyeqBh'
        b'9TJU++HHieivLr05dG4d3hkM1TeWNC1xfP7ZpbeX/HPu7A/Ot7++8elfarv+NL9vwZyGgj/s6bh0edeCbX//xwOLyy/Pj61q1n+aO2/G1YOnrsSvrCzyzbn4njVl+Icv'
        b'Dn949eCvxXBngVQ9NGNLT/r4isTMH3lWX3zjXL7wUeGbvKf1u65zFZXd0sEKPLfs3TcmvvzSj7P0ny/YmrnmrXsv5I9rq+r695+VvPNvN71+lawf+NvHkwYSD1aKRcU3'
        b'M2O0nPrc/eC81tUxTm4afuw+LgO9IOBnjQxbd+r5ID4bRKcz6/zUuaTlYOT6DfgVkQZDfTZPGG2+SbevRZBGEk9TkwV/99CL4RXzk3gTM4g8jTZ3gLpqKA3GA3FOSXC1'
        b'FjHqCI1TdlfjbdOdHLxu4e/j8A8WtjPqSAR3L/Lh7UV+7R6whDznLhPQ3gx8lFXpwkNoYETqi7oZtTwamue2Tc5eB9oPo+0tfNKfKuHBW8Xa+BLbPO9r4Jj6GpeHn2VM'
        b'dOq1v8TspRsfwAd8iEbMbLtQAPcUByTOi58QQcF3J9teRIemBheV1vLqnHKeGrDHBedt6DWmbRVHA7OC1FoOzCqnmwZTemcF4jy0v9KW+Buej/uCNJrtpyUCIbuABx8T'
        b'Z6KN6YxEv57ay2N4G6R27RU5c7Z0L4/OoJ4OtuvYzVGgBYZKQWtsmjSTR0di+PkUeR/tR/0+P+6hfoeG+qUYT+OMIXyYXcgW1HeXDwTuavB2CfXWBUK0ASTuG+sktGnt'
        b'FLvZDplaEA4J5B66eTQ4icsoFnBfFd5n63YN+dAr5rUCgsWlBwR4y4C6mB+BXsWH8zLwC+PwKRN14dMJfLKV9oxN6Oy4LI6bXCil0bu2326G76HX8PcZQckHNXLoSD7t'
        b'eXsFPFC+ijWDCzjktlwdt8Ftq9XR6PA025N4S0cQHS0KoJNFfqY/xpLp1QVQz/Raf7GTu3thWseaR1Jya6gT78uYTX2GIXySPkbwDg4PhtATdqMdLaKLT4DuSp0DHw5w'
        b'jg6ehupPxpnoo9OzHtb58WPT4R1jyQjZKDcpoS3UZ7Ol0NCucSHa7FvZEI1HcVeNwLmnCWibC3ezMynDz7X4FvlLQ/4yHp9Bx7nMiWI6PmjnBcGD6MzUYKCeXptgGe1z'
        b'9Daixz++XMRP5aJX7fo7aZjtu6e0BLig3bwbn+UycJ+Aj92q25JxWypqfDRiW/BtPkhvonq0cyTtUdHYP+S/JlNx4xh4JtdyFCfAJnlcjEXvYtMEJq3mShE2gQQG7gbM'
        b'eVM5iWlJUf/fCWUj0wybVcWchhIiaopuqNSgEYeVTGgKkTTVtIgUVSMU4wlFJ6JpGcTR0G4pJpEa4nGNiKpuEUcjda7olxHWmxTiUPVE0iJipNkgYtyIEmejqlkK/REL'
        b'J4i4Vk0QR9iMqCoRm5U2WoRWn66aqm5aYT2iEGci2aCpEZK50CY3hsItdOPMhKFYltrYLrfFNOKqiUdaqlV6kO6G8tsVHYSqSJZqxmVLjSm0oliCSNWLq6pJViJsmIpM'
        b'VwHlm9wQi0fn3mEn+5CjapNqkbRwJKIkLJNksROTrTj1FfUmIi4P1ZAMs1lttGTFMOIGyUrqkeawqitRWWmLELcsmwptKlkmHj0uxxsak2aEpWki7pEf9HSSOihVXXPH'
        b'7PYuMlrAYUsAxACSAG0AQBY0IJWNoQM8CPAAgAUQBljOGLQAqwCaAB4CWAmgAsQBlgHUA0QBYNdGO8BaRqIDuB+gAaAVQAN4GAB8ZWM1wAqA77CagWe3BuYeYcp4oxxC'
        b'6EjuUdfqkxVf6lqxkp+6Gmm/USLNZSRbllPzKQ/909zU71sS4UgLiJYB1RXWKdHaYhdjA5I0WQ5rmizbHZjxBSEbHHHauVmN38OSdSMe8X+lfCauO2kvSGrKtyCBnAkq'
        b'WRI4C1/9Rlo2gSkV/geBRbtQ'
    ))))
