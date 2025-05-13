
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
SWIFT module of the Python Fintech package.

This module defines functions to parse SWIFT messages.
"""

__all__ = ['parse_mt940', 'SWIFTParserError']

def parse_mt940(data):
    """
    Parses a SWIFT message of type MT940 or MT942.

    It returns a list of bank account statements which are represented
    as usual dictionaries. Also all SEPA fields are extracted. All
    values are converted to unicode strings.

    A dictionary has the following structure:

    - order_reference: string (Auftragssreferenz)
    - reference: string or ``None`` (Bezugsreferenz)
    - bankcode: string (Bankleitzahl)
    - account: string (Kontonummer)
    - number: string (Auszugsnummer)
    - balance_open: dict (Anfangssaldo)
        - amount: Decimal (Betrag)
        - currency: string (Währung)
        - date: date (Buchungsdatum)
    - balance_close: dict (Endsaldo)
        - amount: Decimal (Betrag)
        - currency: string (Währung)
        - date: date (Buchungsdatum)
    - balance_booked: dict or ``None`` (Valutensaldo gebucht)
        - amount: Decimal (Betrag)
        - currency: string (Währung)
        - date: date (Buchungsdatum)
    - balance_noted: dict or ``None`` (Valutensaldo vorgemerkt)
        - amount: Decimal (Betrag)
        - currency: string (Währung)
        - date: date (Buchungsdatum)
    - sum_credits: dict or ``None`` (Summe Gutschriften / MT942 only)
        - amount: Decimal (Betrag)
        - currency: string (Währung)
        - count: int (Anzahl Buchungen)
    - sum_debits: dict or ``None`` (Summe Belastungen / MT942 only)
        - amount: Decimal (Betrag)
        - currency: string (Währung)
        - count: int (Anzahl Buchungen)
    - transactions: list of dictionaries (Auszugsposten)
        - description: string or ``None`` (Beschreibung)
        - valuta: date (Wertstellungsdatum)
        - date: date or ``None`` (Buchungsdatum)
        - amount: Decimal (Betrag)
        - reversal: bool (Rückbuchung)
        - booking_key: string (Buchungsschlüssel)
        - booking_text: string or ``None`` (Buchungstext)
        - reference: string (Kundenreferenz)
        - bank_reference: string or ``None`` (Bankreferenz)
        - gvcode: string (Geschäftsvorfallcode)
        - primanota: string or ``None`` (Primanoten-Nr.)
        - bankcode: string or ``None`` (Bankleitzahl)
        - account: string or ``None`` (Kontonummer)
        - iban: string or ``None`` (IBAN)
        - amount_original: dict or ``None`` (Originalbetrag in Fremdwährung)
            - amount: Decimal (Betrag)
            - currency: string (Währung)
        - charges: dict or ``None`` (Gebühren)
            - amount: Decimal (Betrag)
            - currency: string (Währung)
        - textkey: int or ``None`` (Textschlüssel)
        - name: list of strings (Name)
        - purpose: list of strings (Verwendungszweck)
        - sepa: dictionary of SEPA fields
        - [nn]: Unknown structured fields are added with their numeric ids.

    :param data: The SWIFT message.
    :returns: A list of dictionaries.
    """
    ...


class SWIFTParserError(Exception):
    """SWIFT parser returned an error."""
    ...



from typing import TYPE_CHECKING
if not TYPE_CHECKING:
    import marshal, zlib, base64
    exec(marshal.loads(zlib.decompress(base64.b64decode(
        b'eJzFfAlc08e28PyzAQmbrAECBAQhhD0sghsoi+wq4i4QIEA0BszirkXFBQEFlxrEJW4YXIOo4G5nelu7k2JL4La91N7b177e9mK1te3rbb+Zf0Ch9r3v3u+77z1+7TiZ'
        b'OWfmzJmzzcxJPgOj/pjD/z5eg4sDIB+oQARQUfmUJ1AxljDn2IAX/vIZsZSlFjzcIuXhVuYStj+IHW6ZhP8vw7gzGEs4/iCfNYIho5ZY+YMlz0YQggq2TaWI85OMmz8/'
        b'I22ucEVVmVYhE1aVCzWVMuGstZrKKqUwTa7UyEorhdXS0uXSClk4lzu3Uq4egS2TlcuVMrWwXKss1cirlGqhpgqDqtQy4fCYMrUao6nDuaXeo9bhg//nkaW/j4tCUEgV'
        b'MgqZhaxCdiGn0KrQutCmkFvIK7QttCu0L3QodCwcV+hU6FzoUuha6FboXsgv9Cj0LPQqFBR6HwAFggL3AqcC6wKrAn6BXQGrwKGAW+BcYFtgU+BaAAqYBY4FLgXsAvsC'
        b'jwK3Al6BZwGngFFAFXgVeBeMi/EhzF5mrfSZK3jOQKWvDyjwef65wPd5XQiSfZJ9A4Df77SWgylMX1BO2VSIGLmlo7dtHP7fmSyXRe90BRBZ5SqscT12GQN8tNoe14pD'
        b'V1fwgXYCrqIWeALuRPWoLi97NtqJGvNEqDGjYJZHcRgHBKWy0F10Db0sorSeGBhe0dioM3LQbtSQgxoowM3wgucZ0BgUWEqNosBphIItuJg6rhBTgVkDMLvYmCFWmH02'
        b'mG08zDY7zCoHzLRxmKnOMU7DDKLmjpIwJQMziBrFIMYYVlDJDJpBL7Q+Y1Dt/51B2RYGLZBxgO2a95lAWJy9LuQlQDdmhzEBa7IDh3Bt0lpHS+OpBdbAcZaOAsXFiu/m'
        b'z7A0vsllAevsVzkgqTj7jfks0A4UXDLqEg/WEyeQNOS8Nnk+51rUF35ngYKo204HHWW0AkJHqSL6o2jrrF2WZq+sxw77Hajge9QP1C/8lbyvwADQhuOOHHRMiDeqPmJ2'
        b'cDDaFTEzDO2C7XNRp0dwZg7aExqeEZaZQwGlg80UdA6dHrMjrJEll5EdYdI7QnYDxDCf8Zz5L+T5C0Jp9QLPeRaef0A5AAEA/Mg4+7U8LwbQhuLGWfC2AK+0QZyFGlBd'
        b'9uyZGaEZBSA6K98V7p8L6yEegG21xgodQ9v5WjJsFeqEhySwiwWqogFsBytVSVoX3O6Wj/ZI4BUWUKJ9AB4By7XoktaViP1meDhMEo0rF7IAfBmUoivwtJYIbj4XnUEv'
        b'26B9bADCQbgdvErTeaKMB/CI1pGcLtV5VYxlxw1eTiAA/xs5tScvqToQyAO6jjPUL+GWxQx2Z+nRNx2h4VVHqHjzPuC80jDvL7a2dRtsbU2zxun5+dad4V5MZnZOSKm1'
        b'OrKzgMfcGnaS88XWuTn+zsytjBmRvOkBbH946HVHbkyRe/DetwRvu736dg1V0xbF6uysqfy+OC3yHf7br0C9w+qCcLW182VxAX9iL9g+cxz7w1QR4wmxevCiFdrPw0wU'
        b'wduOOdqwECw2DOAKd7Cs4Z1FTwQE5GW4bwHm9S60G+5Ce1ADlvYECnagq/CGiDXACBap7DDY80JNdlBYU1Mz4Da5XFW1TqYUllvMdrh6tbxcM3WAS9vkojKpRqZywMAM'
        b'glWNix9qwKMUCjg6N8XWr9PNrn/pIzdhj19id4HJb3qv24wexxlmNy9dWbOiz02s1/S5SQyanelmFy+drDlvZ6rZxf3gzOaZOpl+un62Tm5wNaw0jjN4Ggu6o7pnGxf1'
        b'eCf1uiTvTO13Fupde52DemyDHhPJUxHRE3EG2KukCq1swKqoSKVVFhUN8IqKShUyqVJbjVt+s0QOsZFCskgVMZf0KuhiPOmNwcWPNeDpDIqinD+1d69fXsMbYrApl36e'
        b'U33CpyyH2hyztUO/tfMPj9iA7Tjy6Sc1EZl9nPHgJC+cWcr4PfUsJ+rJID6KVlBqlIIyxhhFps8Y9StgjlFFRjKTVtAXWv9zBX1GwjMF5eTS+oBq58BGtA9bk4XoShgI'
        b'W1SkJQbUG51MRPtwVDFHEgEivNE2unVNIrpJa84C2ISVJ58jX6E4y1aTKGFXu51FI1xevV9DbfHY2pLdIvzrkjbHNDvDGn/xrN0JtRnu/u/qWQ+quB9cgvdaKGBzZ89c'
        b'TvMfNSLqiRceoQJuhzXizDC0MyM7lw14WnQQdjDQEdgYIGL+dgtJvDOyfwM8i0SWK6qkGpX7iEiGWkRyaC4FXD0P5jTn6Mfr1b0u4p2pnzi4mPlY7Fp4Tex+Z09d7L6p'
        b'PbZ+Ksfn4qQiqx1gl8lK5BoVYZPK+XdEiJYhiwi5jxTiERH6CYtQPhYhz39WhPZzAsApXgSTNkF/neBExTBA8CDnxw0LNjRwaHPIL9mo1sTFWUeyAKMEoDZ0KJsG3rfG'
        b'lZrIAPxBzuJy3axfuLQpdIbN8A4Gtw+OpABDBlC7HG6mwb3t3KjJDDBxMC1BadZs5NHgsNsDHcXgTHQykgkYFQCdi5hEgxttPKgkzNnB3JtlfO5CPg1uDa/AXWpN/Fp0'
        b'kVCjBOgscykNXpXkRaUwgHCwMGSlTrDBlpa25KmrMbA/N5IBGFV4aD8ZDatWCqiZDOA4mPtguVmK5mj5RDJPpBSo0ZVYeBLtJ6TDrQB1TkPbaQwrhS+VzQCRg1PfVfBz'
        b'P7LEL+go2ruaRrkEt0eyMUotwIa/Ae6zzLJUSM1iAOvBTY8r+Iob42gXklKdoFbF8uFuMgUm6TwyTqehGb7+1FzCefu3tbqSf4/TuuFGwUK0DXVqo6bCC2S52FOhzgoN'
        b'DR/qFEgtIMzf1KDm24cm02uAO2C9M0EIhXVkzdgVoSuoNZPG8FcFUUsI/zddWMFP+yDewv+zq6zVakklm4z/EkAX4UXYRoN/XhRMFRP+ZwxVLwh8z1brQcCNaC/cTmbg'
        b'C8l+wUMAdeOmbhpFkBBClTFA0mDGug18qx4nC00nUFcxwZCgI5FWGKUVoOtor60lyAkLoyrJri0MWGuecmqTZZI2eBd1oE61bTU8wsXLQFepGLgb1lnEaFIEpWCA4kGR'
        b't9Q844pCS9SAD2thLU8VtxzV04xqA6jLDt6mERoYUVQ12W2PP69fwHIZT3MW1mUjHQ91xArLCAIOP5mx6BYN78iPpjQMMGtQtLSYvyrEY1g6UKs3jxuNjddWsnXoZcoG'
        b'taCL9OyoMQ4e46FrUXDPFHq0bRQFd62mGby4CDWqUedqt0B7spLjlPgluMeCdR3tslPb2PmhWmQkQ96l4qbDNhprBTqq4q3Uzl6CrmHRQB1UIDq8gSY8BNVWqHkq2IR2'
        b'awiSjvKRweN0l8g2Ta1BXfCYLY/0NFJiHLldp8VuNtydora3mwLvYn4y2dQUdMeB1hCbzATcvgbutacA04ZKohZYApqOhI24PSNtJVlONxUOD6PNdA+OmdA2nl31ynLY'
        b'wALM8VTSVLiV7vGArWIs2/CMF9GFahwLOaMaC7Pb0BWAlTw5MIYDcFiH2uFOWGfZ62voELqBJXAebKRVCGvdZXQa1dEs8obX89REFGDXUgfCvotUDDodS08XEgi71fg0'
        b'0ekRRHedpSTjYkUO9BaWL4yh1hB1Xfj5Gn5QKo9uXB4cR21ggOpBm2WV5vL1DLoRBidQNURJPT5SLFixR043Fk+aRNUywMzBjPS1Ooedy+nGtxZMpnYSBc1YojLPOmWZ'
        b'SOcylWpggMrBjAWbzEumhtKNzhuTqSaimjaC5QvsblgaleOmU/sZYAGWqrULUr4poBsj5qdQOqKSCddX6ayOWHSCvymNOswAawblhmW69BJLY+mymZSeaKOWVaFLU8XT'
        b'jf0TsikD0Z5Uqwp+uS6Abmwen0udJ/pR8LCCn37Ny7Ii7SzKSHQg9t563cbpi+jG7dJ86goR9NTsVWb+NkCz1SEeXlfzuEuhnkiELZWEDqNai0xs4al4KnvYjXbYYSEa'
        b'R02JQu0WwYvHe9aJulZz0TnsKokkizWA7oqB9Sos/uqFeKOvEKncT/nPLRSxaALmKF6jDjPxSpe7ruNLupbQjV4z3qD02N8OVrSt4LNXpNONQ+VvUqeY2LJUeBebX+pP'
        b'tnCv/B3KgI9Xg/GvVerCGfwxZxT2SARSiYup7OFTI4s+MYIY9n/L2bD8t2EQB/w2DJqQq/XF9UJ4C22H9Xn47LsH1WXkhKO6CGhYzwBuxayguSvp5W3DB2wWKE7Ae2k7'
        b'w32l5YxQPtkGOAJHD6vi4mzT6lhAOyI5OuGTFZGFdudlsIE1qoU70EXGWqx1zfQeCCeiGtiJPecV1jJ4A1ALATxvv9jiwrrhXnRCvBptDsbh/M4IHAjZVjAd0NlhM7CD'
        b'gfbBThbxC3tAIkjEmntFReiw+KxoPB0o5nKSim17uA6Wxvfc8bEX3J/IERbbPkxnWqQKXp3lIYmEu7AHwx/2Ain2sk1af/whbcm8LESOCnvQy57kKiAL7onIgBeCKSDU'
        b'sO3RBRUdg6Bt8A68LYmxKiID7AclShuakVAngrvE+ABL3yHg02wGCw99CDiLmKhhVRKNy+QukUTjlTYReHI4a5pPG8U58Ka7BF6eDzvw9sBjQKGBtXQHMsB6hkSCThJs'
        b'eBRUoL2r6I5y2AGPSyQr4HW8s/A4WIaultBmdAPHTxKHaibTFIGy6bBFS45DRbAJXszKJITlWnYny8O+mjkRRwlNlnD4fBzqksSp4gkFLUA2YYOWxKbobkJC1mJ0LRtj'
        b'RaBGMQV4i7Dxw85nu4hBrwlexb7+piQuFrtCgL1wuTLM0n4IbZkkibPzJAS24iBX70b7r2hU44sM+ageH99y2IDlQ2G/fBdabDpqRKeQThKHu7EKwcOgEtWl0eZZO2m2'
        b'2IVNtgPV5cILLGA7hemAybhFT2aLOjIk8NpqLZlYDxTO8LbF5Z/hwfZ4OarPziQnQCa6Q8FWdDdJm0s6bwZiKwG3wq3ZGRk55JLo2cE8OFwUkhMuCmNw4WkZFt82eCo4'
        b'GLa7iUXY6ZwSu8D9bq7olDs8wwBwl4sj1KdXKn749ddfiwtZWA6HUhlYDqV2pRaRw6LasMHeQ5wbNpMFWEkUPIu6FopcaI2oXD8Fm7XrajuVlpiro9R4uBO10GjSaHRX'
        b'5Ic67S1d1ygRGx6gkdDRyfmZaDPqHMa6g/3rgWoaSYE6AuOmqjGOxcT5ohNwFy0xhfaoNjpevVLLJSHlTUpYjrbTo6kXwDtovwB7sNXoCpuOQPzm8Gj2xWPspmLMkk7c'
        b'ZUfR/j8aNU+xUHEXtfk7TOPZ8+AebIUXUYvhGXSW7sqDJ6ViuFmt4a4mMdBtSoBeRnqajBh4aRp8uYR0kbk2U0KFPe1hM9FWRnAo6tSo0BUSz92hvOAlZKD7AtDdZWp0'
        b'WcNBLbAdUFgR0B4vuMPC3TuwLQXdQWd51nZcrGLx1MwIywEAnQ/ImS3GAd9KW0L6ISoI1WZYwoCLgeg22Raeva0NxplEZaA2jUViGj1gNz45nEGdDiocKDHtqXhYh45Y'
        b'jIceaDzH4x50mTgefyo5Gu21RGUvo2vwJtaEM+qV9HTwGuWzCV2zxFctE+FRrIBtaq5lw/ZSQnRRYxlyR/UGuB+e5tFdTCcqEt5i02dOvMFb1qF9HLBuKQgFoVHxljBl'
        b'qxC2oz3TYb0Dd+UqCrBwJAIbYe0Ey2i3ZsyHrXDz83XB7TPkiVoBQ/0tVihXz+DG/Em545MdL3xz1OGzjldeu7nhnff0S50CnJwuVRsZ/W+AQ6os++TLLOpyU+g399g7'
        b'J4KDwoHFzbMLPvvRKNns3X2uqG/9d2fbbv7tDjR8sn2zz2sg31jzJnuXSzq1YNuhpwbTxA3//nOb96WG17iZdzt/XDe5KMiv4+P9CcoTr3+VtHRaWUjb+S2/tPx0Ud23'
        b'5aPG5Oqyp8fKfQ+WdJ0vLzibtlEU8/7xayHfi1XaQ/XUfCnnnXQ7r1ejXg4pbZy1iLPjxKHDXl8Vm732zdhz63DJkdspi0/9ufhkTQTvl6yhA5+kb8n/6K/fVWZq6xZv'
        b'WR1QKPtZmdP29RuHt3C7JmhvOphmrvl6+ju+cx7PGzrG3pAzlP5K369J8ypKjydGwD+6TDn0puHDsMP73nzZcDfjw1XHl6UPrX7N/XqCzVtv3q77ZfaRSPu3Qj/qeNdG'
        b'9vkvr6UHPdT9+uVXb5852H7xc+c/fKzeGB6/63L7vpaWNxp3TXU/9lNSak5N04n8z/8a5fv0TDh8kBU7EHnLP+LOd5+lpVpZtQ9IbteeufvnhRXKvuuLrp3M/Czrx8Lj'
        b'2Zq8W0FV77esG9fYs67/rd4HGUWJGd/eOr/418Vd8XUv/aLakLhoLzds95y3ty2xuvntgObB5sPOkRUlrGnvqj87sGuTQ1bVpE+XGnNlf0BrU1sn3t4x+Clv29yV4Yq3'
        b'Rdb0FUMOvBmL6udMDs3F1g3tCcVmHJ4jdvzqNPq2bBbaliwOzwgNEYXjXlSHjpK7SyGrEBrintDyfYplM8mVvk97fpcGtyQ/ITI5GR5MZ6E2cTg2oXV4bA7czQiDJ+BR'
        b'uleSg9qzQoNnosYsCh+bz72Eahlr0UF0hx5Ygf3pFngEnsrKyAnJsQIcFsMaHoeNT4hPdUA3UId4ZmgIHhYT1YD2MPPhdeA8iYla2bD9iavFH5/Nz8oLo+ABdBwwVlHJ'
        b'YtghsvvNvck/X6hJIRz+q6l5dufiZLlz0aikSrXU8l6jItdn9NXLRQZ99fIEn/89AptYZncvXbbJXYRrLnydoMdlgtkvUC897m4YZ4jSC5pYTQua7QnQzOZNfe5hJvew'
        b'PvcIk3vEYGBIU4qO35xrnhCi89iXZ3b10AU3F/a5hptcww3qPleJyVUy6OOvj2qp0Ev1JbrlGHxcc/ow+BAHCHyOxbfE62NapzSlmD19dCtbgppmmL18jyW2JOpLW6cZ'
        b'ogzRPV7hTSkf+QXq2GZhoL5Ev1JvY6niEemql1Cf0jrFLJmo9+kVRJq9/fVlrUvNkbF6r15BmNlnvF7TusLI7nbptDMHiAxzT+YYZd2azhVmgVDv0ZLXJ4g2CaKNsR8K'
        b'EkZQI2L0nr2C0JGP4RK9R2se+aTo9Y4maG4t2X2CCJMgwsj+UBA3DPdpeJQx8NwyXcoINMEVR+rdWrPxp2NLW5YeK2opGgyJ0Lu2Zg3ZA+/xx7JbsocAFZJMmWfMfMSk'
        b'QjKoJ4DyzqQGA4KOZxkDTQHxulSz73h9xrGXzMIA/cLjDkZGr1Bi1JqEkz8QSgYtbX3COJMwzqjtE055lEEB/wlD2TgW9MfbNq/ZdojB9nRq4gzZgvFBTQ70mg/nYWYH'
        b'h16yb7c3qnuDJ5lcAptS9exP3D2Pag2u53zxgnXzWmz1BSa+2BwSccjhTx7BOl8zX0C3FvXyY7tdTPwpH/BjH9kB71C8FCw1Ns3TeiYk9jonDoYm3XO5J3/F1xQ6G2+3'
        b'W3O23v2Bi4jIhqi5qCd46oeuU/EO6zktk/u8xCYvsSGtz0vywEtijki9V3Y/4ZUqU8Q8HYuea94Dfui384mQjrr8sx6wHSPVv3P991sdoU90o9WDVgW6mEH6E8DwlTKD'
        b'ojwfgf+HS8EDnEBwmhfJFFG0g3NBrb5ZGaHwkl8GjqVwKNDqitrGHLfsRk465EF4qt3wcYs80IEXn+hi7J4dv1j/2uOXNgMHI9xZxFaohdKxD7n06/DaapkwZ25CTKSw'
        b'SkVXosO53AyNUCXTaFVKgqOQqzUEtESqXC6UlpZWaZUaoVoj1chWyJQatXB1pby0UihVyTBOtUqmxo2yMq5ULdSqtVKFsExO76NUJZepw4XJCnWVUKpQCPNTZyULy+Uy'
        b'RZmaxpWtwZteijEJjIJLvyZYekqrlKtkKtxD3qO1SnlpVZkMz6+SKyvUmNbk5zOsFVbiacmDd3mVQlG1GkMQQG0pXooskcsNw2ssk6mKVLJymUqmLJUlDo8jDE7WluP5'
        b'K9Tq4b51Igz9IhzmUXFxbpVSVlwsDJ4uW6etGINAWETIez7udNyikMk166SVCgIxzL/nAFlVSk2VUrtihUxF+nGtRKYaTZeaTPIcoESqkGKKiqqqZcpEeukYSFkuxcxQ'
        b'SxVlVSIucRR4ohWWeVJkpfIVeBswtWSBI92lWhVZ2drnM81HpypVWuUzCPK+lEiXGFdbWom71PiTdsVoKkoVVWrZCBmpyrL/BRJKqqqWy8qGaRizP/OwDGlkSpomYYWs'
        b'BI+g+Z+lTVml+QdIW1WlqsC6pFr+P0SdWruiqFQlK5Nr1L9HWz6RNWG6VqMurVTJyzGZwgiLZRBWKRVr/2U0DiuCXElLMFEQ4TCpMuUImfQD0H9B5XSZQqrW0Cj/O0SO'
        b'9lSJz0zlaJv3TIerq9QagjS8QzJ1qUpeTcD+M+tC+C+Tl4yihlhFjXRkY+djq4iHVChG7e4L2z92zLGi8A/xSCXD1hcLaqIQaxrunYNulS4vsQw0AkN0EC+gaLlsFCtH'
        b'JsPLUKBbarVM8VtwDTb6/8nih3EJxHNCXrDaWVplmUz53AIPD49t7u/Y+LETYJjf4lWsGmu708kOoFPlGjXW0HLstEj3CHC1CjML67f098efNdwtU4blqsJHUzZmjhdo'
        b'eu4rhjfnN/5iDMIY32GBl+Mpfh84Y3py7tgtL6pSySvkSrK1L+pX3nBfCS0MWAGEaSrZirLVY/TjHxCgf1jRKqXYCv6uqqfLStAtrArKf/mkRLxomSX6PWbOubjnRcFV'
        b'SlfInmv5cAwiDM7Fzc/kQquqpn3iC1DzZKrVMmUZEet1q2Wly0cw1LJqaeLoIAYjjYqOhqEWK5VLE4UFyuXKqtXK51FN2egYSlpWhhtWyzWVJAiSq0g0IVPJS4XyMhIp'
        b'JeIjo3QFMQt4vrmVv0nrC+cmDsd8icLk37Vk4dwxd/n24Ld3+TmWnKOcJUyS78BvsS5WLE+dZLkF3+1JrsbBrNb0YsVbysWAvltyzYQG2MnILSKZjpPih19Np6SRC3Mw'
        b'y9a/OHvNZAmwXEHfRV3+kmiwFF2yXFpnQqNWSO6a9qGd8LxYlIkaxLnZEnm45YQu5gA/X7ZnaJbIVkvOAejqmgpUH5GZEQZ3RWTmZIVlosasXHY5bAdRqJEjhjfnaklO'
        b'D9pNbuLFiejl50DACR5lQmMeOq4liY9TUBs8MvoSOxUeA/Qtdg06Rb8izIaHYU0WuayGt4JG3VfbJNHdcQXwMKoXo8aczDCGjwhYo+sMuAseRVtoUqeiWriZjJ+BGrJy'
        b'56ArsBHtiZiJGpnA14mFdOhuhpakRcHbs+HlZ3CwMQ9Pdy0A1ZFHiwAxezLqwgSLyJp069HJMYC70B7YTsrcHAqI4C02PIRq0QkLpwyoiTkKGu1B9bDOLSIDgwYUs5My'
        b'4B76oWIT2o8XEY4a8YDh6EZMZg6qCxVxgBdqJU8Om+F2rSVJKhl2EDAPdBlDZuSgXQTK3ZUVCfdL6TeL2cgQM7KBjuqxGwgvetD7HwwNUZJoFtyLavCYB0GZAp6mnxQm'
        b'omsu4rSsF3YL3oC7LC8le4OZkmh2EtxMvwBUojOJlvbdEQVon9VC1AFAJIiEt9EO+q1hE2oeP3p3g9zozYXtsNXyFrF7jQe9t+gOOjNqczeiJnzeIrQuQufWSODlag6g'
        b'sqNhF2ZB/BJ6ypdgVxLuAB5s+hlluRJtowViMboreSYQcXDriERcWiziWO6QD8Md7hJJNRNQWWjHVAAv+KEmekhPvoNEgoxsQM3hol0AXlmeNPxS5QIPSCQqjJEHj6gB'
        b'vIQuldAY6ybGY4zLGGMe3DwNwGvpbhYNa10XK5FQYlhPchTAcliL2i23uZ2oBp6WSNhKdBx/OgkU8PgcWlMfM91BKD56f+RXLJgpjQRacopnz7FXU2tVAKSCVHQWHrXk'
        b'HISPw6dTkMRaXWz7a7UciJj0wkOVZeSpo5FmI7pYiBeuY8AD8MJKuns8vM3LCg8LIRsLL7LsVwGHeUxsk9FWy9X/VnQa90SXZYRmsAGLRcFjyyF5EKKpbsyAHcMss0I3'
        b'Mcvmojq6ZxraCutGmLYmFPNMhM5YRH8f3AONz2Tfe8NvNE8OG4efm8Tj4eVh7k6TYObC2050+yYBbB7h7ppszNxlblo/cqsBt6WNVdVJ6ueaCg0q+vVLWoK24S1wcLfs'
        b'gBq2aYNwcxIDdr6gvqewIRitvt1ieheLXoK78FYh/UuWrUJXYQ2trq6odc1vtbrB6ZlWa2D9cD4aJZNIWOhwLP0EWBk+n+ZMOrYKd7IywnLD8eTN8FBo8PBFKPCCO1jw'
        b'tA3mINkS98Bs8nglCstgufkDGysG3A0PhdEisNWPTkWddTy22DZIKgL0m0Qp0sHtWePhledbiAzwhMUU70N74f7n8gEbAoflAx3GEkDfBxt9teLMsKywkFzUQPl4AYcK'
        b'pgweX6MNJJ0NsAGeGHlM3Y0aIj2yIK7S73Ze2cSWXJ1KZ2nDW+gsujIKMgvdhifHvLsuQ6ctIrKjaNg6wN0WP5ICmyx2J6SUDc/B7Uz6gQRdReeevUHn5ZJXaMZadB1b'
        b'ZF9a15bIxOvg1jHvtJY3WjzvZpo1Vf6T8STt6MDoR8Mp4y0WvQ7u2/CMM7AOSynalU3uxHEjVYGOgmh4kJPBiKNNJGqdDi9gSmaGYhN8LTMvjAN4WQx0FE9+gybWLgVe'
        b'EJO1wi3rR71rrvDBakrYzJKii6geL+nGqNdSaBRZnoI6UFuaODgsJB27kGcv5pvQdnqlruggi37Xlyc/f9m3POvD06iDljnYBhun8xioayEA+SB/DbyDtYwWxmNcuFNN'
        b'KbAgE2sSim7TCjxPADt5Kg7cziavmiTHdgfaR6ufE3q5HO2jnLEJBWEgDLUP5241jrcG2DZV5y0vtj2+wnP4QfRONBaHfeigFdq2FFOxBxQtWk9LsTd2aq2wM5IJr8Ht'
        b'uMcAqtJgk7aA0NruXKRG9dmoMWP2LHg5Mj9UOgftpLPGw8OC8fpDht9w84mG7AydN5OkNNDMnT0zlPRgvckqmIUaWQDeXT8ONlrBVvrR9rENHSFFeqYUh36XNw/QsQYn'
        b'MIbm3jz/33IvF90ctkUFQagbdsYQdzPbzQEbusUzLOs7JKsm7RQ2c+gcbMB+KMdaG0cWUVuFrmFjtzMDNaOX0X64cxUuGrHHuRAHL7LhZXgL1pXM0ZTAq7HY4TRwFqIb'
        b'sNGicZ0yuOXZqHeQHo+KoXVYUojQemqzsoaf6FHDEsApYoTgkffRjnMR3J8yypqjrctpcw674R26Hx4VFI3yBnvRyWF1d2EOZ5VloI6RhcJa7KfgBXjen7av+dhqXH8e'
        b'jMDNY6OReVMtseKpAFRLoPAsF38bjHShyyIWzVAOagGSuJXYuGeG5uP1zYS36XYuql0hieGgg6iNjkFwzEyLiyPcbyuJWYU5kkTSvAEJFfCayR5sCgrHFCMjwP7AAaPB'
        b'y+h0gIiiTXXSxEDcF4W70uAF7FrhUZtEbSoh89JGVMvDVNZj2amPQHvykdEOdsjg1pioWTNHhG9O2Lw5v5UobDCOcdEhvJZOWoEq4YUieI7DkQGwAWzAW33QkoQU5QbP'
        b'xcEOBmC4uaNtALvpmuHEOKjHPGyD59jIMAuTj6OhzdO0EbSzhTVJajrHfU4weQsjZnI+PfvN0GcEzA+zwubZgBk2kSiq3JuXm4Maw6ZXzxtWElQ3f2Zmwcy59IpiYPss'
        b'tDMnLDw3O48N4Blk5MJt8JrDsPqPh9emoX1sHPzcor8soIqwvI3Xzo7GwnuBjSOUGvKsDeA5dBkdwVgCC6Gbcbj7XNDgCR9a0OJQA22w5kWvfC5mc6UjMUfHOovhroPb'
        b'sLXrROd8V6NrdLZBFxUDbyos4n8DtYnUDOylrlU7cHBfHTUBXkHH6Rwgufqrnyi1Kz77bH1iujDvY6VXqsvUSZO+/6mr7uvXlO8/WHW4p/bKtVanHQ8/DHvyHvXGgoHO'
        b'+nkPT1yuVjPP7zrLXbSS6dS1xPXV1ifbrcAjsGSIMZk5/3DC0aVVX39suOAprqi4k/AfR44lqMur3F6izizzMj7p633v0rmlQ9Qr8V8U6T9tzb3KQA9Wjrt38N3rbt3v'
        b'J/zRWfL1lL9/GMAcPN9+9ejn358Wr5D0219oDR5YVnYjerDF6W9feDruObJok/s7NVN6fA/ty/nw2sMrszmbpvrl+Wz8fLHSM3/jnp+nnOpq6Fn/sDrujfXM3jcVxadt'
        b'ws39svK+nZULrN+6G67/QPTDa7MafhW2elxr4QzdeeWvF79d3PBS0OTXJ17fvLbvxsUpKy+YK7/d/E7Q9LU125Z+z6o/9LeElVafHav7D9vH7yguVv6cDuf7/d2jS/Tw'
        b'cdhfNtoknz1z3P911a+6h30Lx1/ZEmjzLmc59/z9yPg110pVU/v8V50dePdMbZ//DwmNf5qwYcreertG33Gbjq5844e2157a3NUPHY/6kTvILfb+dPNmu6+bN79zPb22'
        b'6tGy+r/EveX98t+Mb1++dV918C8+bzHe8n9r9cJvOm+9+u3lvUtnTVOsfnv99mN+b+UcCJt091Ze8sYdVwuY1rcPHP6y7U35pDkVSk7X3FcXfNv5meAdz/bggSedn+R/'
        b'cmT3gDfscv3m79v/yPV++6sFhl0pCeltkrJV76o+yY8Pom4uq/j51tO/FpTq9p5o5S082r7rkcjn7uDGX98UPPArH1gTaFjXpU8o2pr+h4lnI6pFiogv/1yZM+57xrqp'
        b'Py0uuPs0b8GXHopHa+fc1Ag/2JD+nsPcK6tWtrhf2h70fhlnav8vHp5LH1Tsu5mhsHrj7Un3f2AX/Lhe8Lps0bi5j/70vk716dxFNTsu9ue+t/wvx8cNlez5y+wTduKS'
        b'z4IuP5p67P6OVxd3zS95eD2t6osNP4hzG5et+kP4H76oq4k//6c1t4fCB3OdL6kdVaceba382yt3vonoS5CIvuHFzy183c7Tbs2V5K/iE0JKPOZXrhIfdp243nddkWDX'
        b'tp9Pb4yKSS9Kq6r5cuurk/7t5B8mVbwv+ziz4ZuvUz+Wx85++q7TpfZvOk28daW72QXVqzu4/NvudZkPN+7e+B/v/O3y4IdBEb+09lXxs05ERMwP+C496quBfXedOg8V'
        b'7fpl/odLJ+W4p/6aIP/l3qGrvTFff6f74NyVi+e+euL1YZE2fNbh7Z25a5fYXXjr6C9H2++tPHYlU7tIm/XRuS8TvpIdpt6KsDqS8qfLH6VOb5Omz1px8NHEW7y7aGOB'
        b'6aT9ygOPSrc97uoZd2npw6teYO3A6eOCv7/x97Zf3v+mhzVtdvBTn3X2ryYZqy7nfPxVx48Lhi6EpP+qOtiiPez51YSnjgmXdkuX7c88C/7St/ino1u8zVvei98Sy5sg'
        b'2zapcd75r687BEVGelWXlOX9YjVlv4uPs7fI/glxVegMPAvPkiwFytuSUEDsN47J3OE11kzU5konJJQKVotDwkXYP4EidAjYLGTgcGkbvG754tFldAodF4dnxKMjz5Il'
        b'LJkSUWjvE/q7hE2wo3AkFQLpsZGk0yHQzmA6EyMBR217R9IhsM0/RlIiGGtxuHmUzsRIDuajepKmgWO6+tGpGvhs+4S40uXoCDSK3dGZMWkRlpwIuBW2WogwujLEuTmh'
        b'mWg3gNvhWTzJdcZqdB02PCG+RsNcmYXj1ogw4A11gLOaEW4/mc7VUMGjs7MwZSMrmxMHHCKZFeG2dKoF3DetfCTISPaiYwzHWU/oHLLpyCC2MG1+Kl7weYYEewJ6wbno'
        b'LrxIf7sFdq63fMGF/nbLdHSdXg+qT8R2vBPvxAbUhaO16pFvc01mMXFzrUj4/53K8d9cqMkyhC/+1Yz+G/OFnRWahJhIFXk8prNGvuJYvrCj5AAX/sFpzdN6nQN2pphd'
        b'3XemmV34O1PNHt47M81u7jvTP+ILmlj9zt66Mn1qn3OIyTmk3yvIwOr1CmtKMbt7HVzfvH7fxiaW2dNPn9wibrL6xN2r30VgdnYno+olfc5B7zsHmSeEnFl2fJnR2Sjt'
        b'nTCxOa8pWScbdBfoWfs2fuIl7BeEG7TGQlNEygNBqlngfyynJccQ+EAQORgRYxaFmYNDzUFiPIQ5NNIcFmUOjyalOMIcEm4ODX/kYefneYg9JACevvqAVm9zWLRueS8/'
        b'xOzhQ3/08tEHtk42T09/XfyK+H5p7/Q5JsE0Xao+xCQIw7Mu7I2YhqfRi0iSCEYJ6/XAA0foKlsd8Mce/8xej8xPJ0QZA7sZ3UxjSLfsXvL1yvvjr1f1Tsg1B4cZpEaG'
        b'gdcfQBYw27jSsK43IPGRFcvPU8ce4gKBnz631yvaHJOgD+8VRJFEEmWvd4w5NlEf0SuIHkksiZvU4x/dK5CMfCbdJkH0j/QSDnsPMdyEnmaByBAzxMS1QUEA5qSrcWX3'
        b'OKNn74TJQ2zcOMQB3uP1KUNWpG4NvAP1ZUM2pM4F3ni3hnikbg+8Q/AgDqTuCLzFhpShcaTuBLyDDS5DzqTuArzDDGVDrqTuZhnHndT5FhgPUve0jOlF6gLgPUGvGfIm'
        b'dR8LDb6kLgTe4QbNkB+p+1tgxpN6gKUeSOoTQGCQOUhkDgn9Vow/61hD4YRl41omWrJJ+rzCTF5h/eJYo6w7uVtqXHYv9v64+9H3JpnicnvFeboUkrxjDpjQkjoojjBa'
        b't08daQnUpZpDo9qzu2eYQqfpWLpFJn6w2We8IdMUFN8XNKU7uS9o+r1xJp8ZOiZmnN8Ew4weYaQxyyScpmObfQNa1vX5Rpl8o/p8JSZfyaB/oIE6HqSbQfKUyvQ8DOLj'
        b'q2Pi8VqW9flEmnwi+3yiTT7RRlnHsnszeuPSzSMIQ0yAB3sO1DsC9EFc+mBw2CVeO8+Y2pF5j+oNnt5ip+P0i2KM83pFMzDFC1rszeESY7JRaliGPy418cWDcZMwF6Yb'
        b'5X1xGaa4jPsBvXF5j5iUR4zORbfc5BFimGEWCHv8orDkmPneOqWJH9bHjzHxY4xzP+AnPlOHQIML1t1+/+ghQMVkUOasOXiQmHzqMaDGz6Vwo/dcanAY31Bi4kcZQ038'
        b'aX38NBM/7Z72A34OGSm81yNyUOBzLKMlo2dC0r3AXsFMHfVpYLBh3CX3dnfjuHOeJ4vMwaJLVu1WRuoctx8rkF9XUEdQt18nUSHtdWXvhJwxepLaOpVkfYW9j7U+Ol4f'
        b'+r4ggta/Kb0eUwb5AjJpcK9HCK5+6hOOqYxMNE+Z3jM5GxMfmUOI980lxHvkUoN+E/Zlfu7hQ4zTS80v6dV97mKTu9jo0uXd4d2t7YtKNUWl3nd5z/sN7575i/oyFpsy'
        b'Fj/kCz9x9+73Ce+JSLvvboqY1eszu4c/u98zpEec3euZ0+OSQ5KeFve6Bve7TNBrDYWmoMkPXKaYXSzfdgx84BKMud+UavYL3Jc56CXU+/R5Rb4wHklv8zF5RRqdTF4x'
        b'xHz66ef2uotIkty0lmkGSZ9XhMkrwpjSldmR2a3uzLsn7Y1JNwcEn8k8nmlQn8zrC5hkCpjUnXJvfG9AWl9Atikg+35+b8BsXWp/YIghqr2UJK11+30YOFlPDbFYftmU'
        b'OTq+m+oI7k6953dP+krg9WxDINZQLoiKM0q7KSO3PzyhO/AedY/RLeoNT3nEZor89WxsQAKCDXEnp5qnzugRJfYGTDIHigzzThdiS2XwOJn3xBtMmII1HAPZ9Y2PM8dN'
        b'1LP0S01CCUlJ8+4VRBhjTIL4D8kOjtdrej3EJN9siYkf0sePIgIV0MeP//S3vHk0mw08vL+fywaOrv2O/vpYg49p/MQHjglmR7eDds12OtkDx4BBZ4+dOT88iQLB0Y8B'
        b'A6+vPyTeNHGmOXjavSBTcMZjJpWQRYRBnE2EIRCXTAL1k9oWO733g+0KnFkfOAsKIqws6WeOAyzyQvYPpJ39w46Z3IoX/54jpn0vXewlcFOBJU1NyqIop6cAFyRXzemf'
        b'zVU7wgkDF3gTmWNe60Zy0x6TuOwAWEJ+nASoGPmUipnPULHymSp2BcumXMQecKSfBemUMVWqSlWlku/ByD/5Wl4L6chBNZweJisTSpVCGQEKp7mXK+IMWBcVkXfSoqIB'
        b'blGR5bdFcN22qGilVqoY7nEoKiqXq9QahVwpU1bhBquiorKqUlxxLSoiuWXy0iKpRqOSl2g1MnVRET24JUeQ5tvEkYKQpiZfbdoO/mwbRUPQt91Vzqk8e9Sl4dng+DQ3'
        b'TBWGtm60BHQR6BiHHYIOiqg0uSj6VUotx0O8cThe1tw31ykXJTmmVnz88EmhdVNahD11OIlhc7z22w2385obmoLnBDx+02GI93NEqdhe+P2n5yv+7ZPmz9ftV2871332'
        b'3PUbyzeYJi4aH9Tr//pfuVz7Vwe3frF2+uPVwYl3w28s6/l6ZdfPvdu+X/zZav2OAv2lcTn/Fvv3Y/IFS/xLfvxTWyAjNdL0dOof+s9tL0yZ0VdvCJuwtq3hjYa3+0Me'
        b'FhxqObrdyqM5anEyvFQBeyfVBszZw5CX6Rb+WbfWRZe6Xyebq8syRB/sgEtSGxemb+1Pqb++Xfs5J65lsbn8m+KD13dsbNsW9xh4Cx5av240pToETUz1ZR7+VDCjYeDL'
        b'uiGXJcUNWUs+vXFh7dm5p970OlX24YcrnRXFE9cGvWtz8DCrKupLnmhBc1PGvNNr5+f8+/tN7IX7XSfVLf5T75EKl0/+9uc/i1/99eHFzO5jntLtS7+79K5z1YNTnIQD'
        b'bjnfpb7fEfnlsVd3LDtSmPrksdfRFXOKj0SKWE+ITi2RBqF6P9iUTQFqIkC7NegKfbCxgo0r6R9UsPyaAtqhffaDCsfh8SfkAh42ZsM6XghqRI3wnJicO5798oIv7GSh'
        b'S3bZdECfOhFdUsMLM/FZ6VBu2LPninGoiQmNqDND5GHRUOv/svjvi9bJOUeYRP/VvPBnCdOxJimqpGVY/FNGYnQrXP6CY/RQYOc6xLKyce93cGqKrl+t86vf0KLWR+ul'
        b'x2Nb1xlmt77UEWBUdft1aLtnd6zpDH8l5b4Tmtkbnf0R31MXrZO2xLba6DNN/HCju4k/sWdyrsk9t2fO3J6CeaY583vd53/kJtQ77VP2OAbggIW/gMLuwcmlKbnZdef0'
        b'pyyOTfBTR5aN/xAgha21kGu2dWhyG2KSmodAV26pTRAZ4iw1SVw3x1JLmnFvHl0bpDHYpEZj0DUag67RGHSNxiA1HJXZOWIcK0vd0xtjDdeDQjDecD0mHmMO15OpFApj'
        b'05+sLdg2ljqNPVwPje7m3JtnHueuKzfE/V71WwcM2GMtwAGvEx+3WP57xOP441afp47ZlM186hGg/xkqZACuY7+NY5NaF9u03GTj/5Sxhmnj+RSQcoguHzMBdzwpHIdY'
        b'dOsqK1x/wqBsog+vxZ7KJprufEQafhiS8SibDKrfyfeUbU9YWq8wvddpZo/tTIv/2pUsSLEFr9o6p/gyLf7LZYCBBeZf571+V3hdfsejPfdqKSMFfSafMuzVRBTlSJya'
        b'4/ek+Ged2glONLjMm8KUr/1lFlO9CbdM/GJQ1jiFuzWJn3J3Wmxbvth1X5iq9tQ71BX1kRCj1vHDP675U/FPji8n3ZN/4rKn5d8Cq5v0r6z69q/yE41Jne/7RfzHVaug'
        b'tKWa8N1tB6fNd/p49dIgr8774VP+YrrnWHZ/9sMGbqxn8CLNF1J+9bab8z9JXJQ32+367B9/AeiI8/mL74ms6GuFSLjTh/51pzz68c0K8ODlWWoGMrCoJ+T9xhpdKMrK'
        b'C0MdBCRPAzvCGNgE3WJic3ZgAW3y0I2FU2E9eZfEdi8KnsmBjXCPFbB3Yvqg07Ms33rphDvQgSx4IWTUl1Muwbv0DPAWPA/1WaN+NoonQoeQkYGaxFNoCCt4MnTsz0rB'
        b'i+TK2wg7YSttju3wELXitNhMNqCyANJNR7Wi8f+5efxfv+r4XZkcP2JQXzSnv2ta5Uq5BmtKzohpTcfFzzUkQGI7m+1c+ux8THY+h9f02gXXpJlZ3B3Zm7N7xvmdmviA'
        b'Ffoxy/ePLLunnPVsdvRTQMrv6HJoHQ/YutTkjfo2g3CAqZApB1gk0X6ArdFWK2QDLJJdhcNMeSkuSSL3AFOtUQ2wS9biYGeARfIsB5hypWaATf+kygBbJVVWYGy5slqr'
        b'GWCWVqoGmFWqsgFOuVyhkeEPK6TVA8x18uoBtlRdKpcPMCtlazAIHp4rV8uVOKBSlsoGONXaEoW8dMBKWloqq9aoB2zpCaMtGWoDdpZLIbm6amJcZNQAT10pL9cU0cHd'
        b'gJ1WWVopxcFaWZFsTemADQ7ScABYjeM1jlapVcvKnhsc+hqq+L/8EwotdiJnpCC/y6XOw8Wvv/76d2wqHCgclhJbMbb8li7/GctBTOQrXE6yJ3jFk5ccyPzJeuTHlAYc'
        b'SQhK14ed7E+e5WN/H0+orNIISZ+sLFdkrSLROYlTpQrFsNioEkkTF7NXpVGTtLsBjqKqVKrAnJ2jVWrkK2R0/KxaMSINzyPYAevJltB4qkoNLNG5OhsXQ0yKoh4xWBRr'
        b'yBbw7GqsvmVlciiXoUW2wGZcn7WXydpLl9lnHWSyDuoJnfrKBBTcG5pptnbs57r1uEt6uTE9rJh+4NjE/wB40rP9H0NAU/Y='
    ))))
