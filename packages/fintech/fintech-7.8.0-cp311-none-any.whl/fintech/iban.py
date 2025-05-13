
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
IBAN module of the Python Fintech package.

This module defines functions to check and create IBANs.
"""

__all__ = ['check_iban', 'create_iban', 'check_bic', 'get_bic', 'parse_iban', 'get_bankname']

def check_iban(iban, bic=None, country=None, sepa=False):
    """
    Checks an IBAN for validity.

    If the *kontocheck* package is available, for German IBANs the
    bank code and the checksum of the account number are checked as
    well.

    :param iban: The IBAN to be checked.
    :param bic: If given, IBAN and BIC are checked in the
        context of each other.
    :param country: If given, the IBAN is checked in the
        context of this country. Must be an ISO-3166 ALPHA 2
        code.
    :param sepa: If *sepa* evaluates to ``True``, the IBAN is
        checked to be valid in the Single Euro Payments Area.
    :returns: ``True`` on validity, ``False`` otherwise.
    """
    ...


def create_iban(bankcode, account, bic=False):
    """
    Creates an IBAN from a German bank code and account number.

    The *kontocheck* package is required to perform this function.
    Otherwise a *RuntimeError* is raised.

    :param bankcode: The German bank code.
    :param account: The account number.
    :param bic: Flag if the corresponding BIC should be returned as well.
    :returns: Either the IBAN or a 2-tuple in the form of (IBAN, BIC).
    """
    ...


def check_bic(bic, country=None, scl=False):
    """
    Checks a BIC for validity.

    :param bic: The BIC to be checked.
    :param country: If given, the BIC is checked in the
        context of this country. Must be an ISO-3166 ALPHA 2
        code.
    :param scl: If set to ``True``, the BIC is checked for occurrence
        in the SEPA Clearing Directory, published by the German Central
        Bank. If set to a value of *SCT*, *SDD*, *COR1*, or *B2B*, *SCC*,
        the BIC is also checked to be valid for this payment order type.
        The *kontocheck* package is required for this option.
        Otherwise a *RuntimeError* is raised.
    :returns: ``True`` on validity, ``False`` otherwise.
    """
    ...


def get_bic(iban):
    """
    Returns the corresponding BIC for a given German IBAN.

    The *kontocheck* package is required to perform this function.
    Otherwise a *RuntimeError* is raised.
    """
    ...


def parse_iban(iban):
    """
    Splits a given IBAN into its fragments.

    Returns a 4-tuple in the form of
    (COUNTRY, CHECKSUM, BANK_CODE, ACCOUNT_NUMBER)
    """
    ...


def get_bankname(iban_or_bic):
    """
    Returns the bank name of a given German IBAN or European BIC.
    In the latter case the bank name is read from the SEPA Clearing
    Directory published by the German Central Bank.

    The *kontocheck* package is required to perform this function.
    Otherwise a *RuntimeError* is raised.
    """
    ...



from typing import TYPE_CHECKING
if not TYPE_CHECKING:
    import marshal, zlib, base64
    exec(marshal.loads(zlib.decompress(base64.b64decode(
        b'eJzVfAlYlNfV/zsbzDDs27A7gArDLpu4i7iw44IaVxiGQUYRcIZBccUNhn1RARdwUFTEDcUFd3Nvm9olCRhaKW1S06Rt0vRpaWJSk35p/+fed2Zk0bb5nnzf9/yH4WXO'
        b'e+8977nbOb9zzh0+Yka8eIa/X5TBpZnJZlYzG5jVnGzOAWY1V8nT85lXvLK5ZzkMc4FjpNWW2TwuoxSchc8XTLWKGY3lGi7cN8vmj66/jwN3zZVjuHCYbMEyRrRBZvZN'
        b'jkXCvNhU6eaCbG2eUlqQIy3KVUoXlxTlFuRLF6ryi5SKXGmhXLFJvkEZYmGRnqvSGOtmK3NU+UqNNEebryhSFeRrpEUFUkWuUrFJKs/PlirUSnmRUkq4a0IsFB4jOuUJ'
        b'v2IyEh/DpZwp55Rzy3nl/HJBuVm5ebmwXFRuUS4utyy3Krcutym3Lbcrty93KHcsdyp3LpeUu5S7lruVu5d7NDM6d51EZ68T6sx1Vjq+zkZnoXPQWepEOicdo+PpbHUu'
        b'OkedQGetc9aJda46Mx1Xx9G56Tx0djmeMO7CXZ5cpsJ99Fju8hIxXGan5+i7cMdr9B0Os9tzt9cyxve1ZVuZbbxVzFaOKEfGTVWMnFUr+HUgA2BmWArLGJkoNU8I1EcO'
        b'PIashLDie7KBtGJGOxEI3LxnD67CFWnJS7AO16TJcE3C8sXBZqGolvFbwMcPUdlU2vrAXDPGkmFsw1bc2/FcvpXRyuEmqsR1WI97RFZL4oFLdcLyeHTJH+uCElNwwzIh'
        b'rohfDlxrcV0gPAHXxqfg2hX+8cm4NjU5bbk/rkX1+BbWhcIzl8QnLvcPjk8I4qAuPlOEKpyicQ0+oY0kMt5GTfge8B/NCDhXhS6JD0rC1fDkZFyZIJi1kilGdaK16zUK'
        b'zohBsTYOSj1cjliVw8DQWeTDDJrBDAthXi1gHi1hrq11NjnWdAZhfVfwx8wgl84gZ9wMcsfNEmc31zCDryx7/QyKXzGDXewMdqSYwxzkFphJM/P+sWYpQ29mpXFhWvVr'
        b'LJnM5EMZhpsPJELGlmEKrTMzk389I4a9+UaKgBEyz/Jt5mbmuRZxmfNMngXc7rV04T+3Z+YOO5RwfuF3c8pszilOnggK3n2jhdNtzkjDXPNXBS+LzdjC0NsDSZ/bHLbh'
        b'+A8ze4L+JClwkzBDjDYYCvy98V1cpbAn0+LvjytD44NxJTqf7g+roS4oJCE4MYXD5NuIZqHrWCcL0TqTFdSKyvExjSVMF25hUtE51IROWNAifAB1+2jUAvhUxWxAZUiH'
        b'2pBO60SKurFuqUZtDp9qmCR0GFUuw5e0EsKvGXdO1eCbpFI9A48/h6rt8APaKgD14h4NqoVNgNsZ3OWPWm2W0pJ1c+zgPhfun2LQJWjTNg+X0xJ0b8ZqzRYiQx2DHzrA'
        b'gj+Lz2hdCPv9+Aw+qMFXYZ7wESjEt1A9OjSBNluGu1C5RkvaNTDoQASqwldi2V6VoQ58RmNFWp1kUIsXOorL/diiyj2oWYN7iHzNjDu+ANvjoZ/WEYpk6KKnBlWTSieY'
        b'BSp0DOlz2JGoQVWoTiMmsusZbgA6iu6F0iYSdAff0GwF24CbmCkZqBYft6RN1DD8RzQ2DG2Ba8WoZQ3qok2C8REz3GNFnn8JxtgCnVyfz85SC7qxVEyn4gIjRpVAN6NL'
        b'Wnso8irMQlUwfRwhswY1osvum9h5OOCLKzT4GpnXRgafRp2oDtWsotwccT1qwz1aHjvexxLQ4fXoAdusFl1D3WLcTR51hXGFWW/DHWH0SYq1Is1WLuXngs+iSmY55eaK'
        b'z0/Q4FtE6KOMNe5GDbAeTtGiTegK7tDYGOb1KKpAx0pAp5Dd5eczE/cISUkH45CAjnuhE7RJPD5XBAXk8ecY1I7vwZq7u4ROODqIqnEP7ikS0EfhKnQS1eFeB1bwTrQ3'
        b'CfdYmtGGW/FB1IrPoAt0WPGpkhgoIkPRyWRGoDY1Ok4bFXngJuB4lch+mkF1gaDnyvBedsjvoiOZoFlJq8tMNmyGdqz3ZtdJNfTwNJSxg+QDK/aUTRgt8tpC1TEZ2W4G'
        b'3wThT+PrbuxKPrlxPgy6Yd0dQwdQg9UaKkbSHNLIikMboav4PjqFT8D00md1OmwmnSaFXUxqKDoO/a6nzSYvRKWkyJxdLtdhONp2oKu0y1k7nWASWdm5sFZacaOHcVM/'
        b'UIqFpOQmmA8Q8Ew4PsQW7Yf9LsbXCL8bIIcziNHlTKd+0sp54mIBfU7OLnTUCjXRFjxUt1aMb5Lhu8pgHX3OGT47WSfBslRCIelvD4PO4Cvo5HLUw05IzbZQKBLQB5nP'
        b'gZF96MEW1MqDNEVEOB10NwGV4Y5gdjZuoQq8T6zh0xFHNxSoRYyOagncQDfwSVyOqqLxaXtY2DdQtYDh4VOcNFA+h7TupMb1OPQQVRWjwzDdh1ENqhQw/FwO2svka73J'
        b'U4/lo/tQDmW9MLc14UY2IlTDlaDLGhmPrll0x9scV/FAS7YwBUwBdPaO1pa0b/TJTuIz6NwMJovJCvKkQ4Yvoe6QJDNmBuoAG5KNKxMN+gz3zjZ2Ee0VQhePS7WToGSa'
        b'Bj3Eh2AUL0Sj8wJ5RGoKqsEdG+PQ6dUpTKRGgI6g845UDtxms0NDd0EFs3ADKt+CbmtlhHc9rg8zsriMj+DD5CO6szw6El3AR/iMB67hizbBynKkvXFjNPg6h1XUx/1R'
        b'beQ8bQApqNsRxXJBN1EnYRMP3O7iuyY26D6fByv0BMunBpSBzmhBBFLUlL2UiuMfjhuN0lwySiNAR4HNRVaaRr4ZOotqaaekMRxQsEQhtMHiCUQnvOVspy7CzLfiQ/Ho'
        b'IoyLkc1idDo6nAgHbIJ5uHcZrmbX8M1kvE+jJsukHN6gMg7gRlfaLbwPNYSaRkcgh+FF9zaKpYtAM1ehzhUOTKLUXIwbcC/dXbgV2FcYzR8s7XNIx0EHtWGk7AIuxe3j'
        b'Rjoa1F0NDNFlXBONuohswWrBFit8nIpWHITuGU0mPo/ugCm7C1p3CunjGdyEXvaxhpfFCgfK4xjugP53bkRVsArica8ZvrHWoKvxtUx0FlQ83TfMLuBYBQryMoWVa3FL'
        b'AO7YMnLYYBKj+UvBrPXwwHwfAftKZs8X61GLxoJLJ08I2+zIqnBtDJHp6GrYDYfcbEwLoWbURMIsdqYQ5hdTzLJSmC3oihDd9sHtlGsBOrNRgyr5VNeplqATMKvaELrz'
        b'AUw+IGJdRufdTRPKQ424Ah9BZTmw8Y4xU/BJAaqNzmftfAfuwqdNkAJdNYdeXsFX6erA9bhi66hFRtbqvWyQrotdqod4AF0vSKhYUty0UmNN+nqMsV0Byv4SIBO6Nm7h'
        b'ZpjSsROKWwOA0Xl2sZbzzfFRb9bYnIDS9pdIpgmsXuv0tdpQKAsNBZlMjF6OWTzehy/DFBj2UOQO2Am4YSNd+7OX5ZrgDz6Vg9pWLKXrbOcCsL5GlfBylV0Atpd92Skg'
        b'vMJxnQDpw2HhUg3TDdN7yYSZKuagymJXbSBBtqg+ZvTGpp/L0TEjJw98iS+E3XmX7WZrGjryEmBdnQkK5jiuYLdAGWzMO+OEA8YXSadtSqLZTR4MylbDxYfp+G9FdaHA'
        b'z5zab3MCFJKLWb3fCVJXGfHaBH9UtWYyXS9g7vbBdBse00Uew6CGErJU4Kcb10rRKdi5Kfi+ebgXh0Vkpai10ITvbpago2LcyDK7BD+tI3Qsu8vw/om4crV/NDsEGnRS'
        b'iKtluJlu2mmwNU+ZIOFMUAr1+IpYGwRFAjAFRl4XxqiAEJGp+00CzZZ4FhBGztGw1roVjNYu1JSFelnjdhNA90kjhoQuN6GjsWvo+rZCLTNMy5sKTEzCcnGcFB+iOisN'
        b't5mH4Eu27DC2gSndZwRpjrmocvo6dtu1LgOkYNIvo0Rex2VXA58JQXcFG1E5u1eKUDsC+Cqgc69E11HNMp7Wn0jbEIH2Gnh1GZmErTAZBz8e2Ioa1E0nY+ESNxM2hO3Q'
        b'jhrycBdlgw/7bx6jnvAxZ+ByiXBxxzd5+Cq6jW5RYdKTPYENh6LviSKw4zfQGbpznOe7GvElPjMdHfNFpXQXguK/4T1mG7KPiQRV/nIXbhGglkB8gDXvB0JnaGw4FJKi'
        b'YwHohH2Y1o/sQtQ4jWqsl5J6o3KT+eHxANrUoit0y6TgGxEmXAsrUQez2Yru07nMQmfTjCJdMW2Yw3kvN99pUDFlmAWtluiitwkIp2aitgDcoo0mA9eFjwJ8PJj7qu7R'
        b'O3x0zTIldj66NJlR4yNC0Ee3s+lCcy+0NcFnsCpnwCXQA0aieK0NXQOGPSwggFXYuw41lYBfMhkKJ+ag9jGW8wZuhq0TJxUwkUgvQCeX4f3sWj6R7gpYm8z4GeIMHkDH'
        b'0Zl46p6u9HMavQQNelbqRVUZ1dcR+LgANSbi+wY4yOwyYXp0xgO1pqyj2mcJKOy9L5VPjUk50Ds86L/VxijOEi5qEJjH2IDTysL2zM0mNwA6fw36fD6AigYLrRJfS6Lm'
        b'DNiM3m4eq1gMthTVmHs7oXY6XhsU+DqMFgXLZ4hmqYQ5OQ+4mCKofbgznfYVtdq+tOgUzRE7HoFugH0Dp6yKLpr1UKMZ91ibU3BbDODgNHgfZXSbxKEHAWO2CTq/BRZf'
        b'F7tNrsLqw0fB6rtC5QzQ/AdwD2tKrjGoGp1CZ0GbdNJZBADZgC4JA0aZOQMq8ED7YNvC3jvNooIJwbhnC5fuN3wiFdVZQbf9Wft9au0orQ8MtgM0NO4GVM7Dd5yVLDI8'
        b'gDqygY8ZVXl7QlC9rbvWlwweqgvJKhwLTrgEnNwi2/64wQdziodBM/lnRa6IGNoKWsTfg/Qm7wyfkYO2AqBEdc4qdNLL5Jyhm2AhgrFhBXTARF80+Wfo5iZ0OiOebnKY'
        b'zQfKsfrobgmsy8vsQHfDQDtLab/scYPS5Mm5LUEN+Aq7v4pQUzEUGHbQ3pWAakrRfjpws2G+bxq0SJeR/428aFCsJjVyHV3LpXwmgj7RASMBhRdJSegQrKR6bTi1lLhq'
        b'8XjkCWJuBZfLuBH4AKGOCQA8gNfPGsUjUwBg9eAb7F6al4aOrshlMQZ45XvHLYlIEi8A8DmC4UoBqod9QNklywC89Fhx6eijDiuYi6o5dBynOS4aba+IlkjEe00Ga3Gy'
        b'+TTFTnZ9dEbwTH7vnChwN2+wMoEhUoxWFQYIdRKQ+mXTmEWghwJUFw1+IFHfkakzgJmA9UVPmaPTmiUsUmlKx/dxvWYUQ67CIJotiNUbbYd0URx0fK5F6vrVLPQ5HU/3'
        b't8HvBvfwEjquSKd6PBad3zXWHwEd+8Ckx2U8fAuQdBMLX9tluOWlmw5PPYbaLNF51i5fw2c4r0F4F9AhXGqEEVpBofVuVid24XIr8O3NKLsNS9GJHSV0e+OGLWPxvi++'
        b'ZbR07vg2D19bFUanL31urik64A2bohUetpfVXF3oVsB4jOiLj730IR/yrfENe+rkTlOi/WKhGfXjJ2WjDosUVkvcwNU+Y2Sxw/dASVxkZbnMw5cDkN7oEVfhMmNIInM7'
        b'IK72dZQNb4JwHFiLw6fQzZeLKch86tJJrOE5K0SnxEWs4cG3odohF3STDlnJCg9TWAN37ybrbCq7K07guiliCyL/bTD5YnBGj0pZF7sjaYG4mDA7zyzHlejIyjTWUegJ'
        b'ixmFRok+PoCvv9zHRAE+3Ah9I2yi0c0AcTHhf4FxAMjcLI2naxKdnjM/b82rVyTqWQ1a9sBGfHo1o94ETpUzaqbM5hXgm8YoTDzaj47aBLCwtht804OsVHH40mi1cEFg'
        b'b3CpLoKPgO8tooNVgu9GmgI3WbC6W/FxGCyCnHxD3hjntBvdP3QVlxs9W3RIUITq19BxjEHli0yhHnwOP0Anp9uyGvfONB9TpAfvB+zVrkDHaaMIsp7E1mTa7zGFOSSA'
        b'Bzid6jg9rkh5lY47PxO87pE6rh2QB2yIZjoOM5De4uXc1IxpnAyje1mwJYqzWGgevRJQD5lOj2xQ3uxqr9vy0oGEXSfIgnlIYcIlArCix/AtWn0tulw0CvKT2d+PT5PZ'
        b'Z0Ma6Bof0Be6zG6mw7iBPz4eo8M3jDDXA1fyhVHoNru2mnxgKY1RLOBvnDNtvRk80GRNAH3JGtqMWvjjVQdR3FfVowbpkACd4OHTMiHdDNGbcaXYmhjAB4wNrkNdIZiF'
        b'6pEMPi7GV9lt6O4KBnW/IVy3JhLdhBLSppfxAgFOp8ey++fszAyxiEtnEEB/AzqHz6joWl24HNaqlg1kI70ranafQ1tMw9eDTFG80lWoBTy5NlYNHHDDD8QadpdysJ7E'
        b'nf1YaNoMnPejKlbn3WdkBWDq94K3GwGFe/C1eCg6hHTFMAKnZCS6hy4ZNifSRZNQHh/1pKOq5czKdWb45KJcGRuh5KML2bgqORFX8xheAQzsA7AAuCOcyp+1Zm2GZxKu'
        b'TDZjuOs5oagXXDU3uO9VUpCEa0NxTSDwvyYjuTJLW54TrnJjRT22Hl0KTA2O5wP7y/jsXA4o1CPo5ELFyBQwSeLQDBPJJxwxM6ZJmxkdhybDuDqGJsR4OnGOiKbC+Fym'
        b'wmxMKkxAU2H8cakwwbh0F3+3wJAKe2XZyFTYh8MwmxbSEa84kvbVSOX5NN8rzSlQS4vleapsVVFJyKiKo4gENtscsKkgv6iAZo4DjLlmqQq4FctVefKsPGUQZbhIqd5s'
        b'eICGtBvFKkuev0mqKMhW0twz4Ur5abSbjTltuUJRoM0vkuZrN2cp1VK52lBFmS2Va0bx2qrMywuxGHVreqFcLd8sVcFjpkvTc9m0Nsl3Z5m4hLyqQZZKMZ10c4OqWJkf'
        b'xLYiAs5LiBslgSp/XI/ISwEDo9xWRLqglCtypQVQSf3KB9G+qUtGPqzIKCYM5X/+nCKS4TdwC5GmaDVFpI9k3JelBUdMiY6WxiYvjo+Vhr+CSbbylbJplIVyKlgA+RQg'
        b'VcLS0MqLlPTAQGZmulqrzMwcJe943gb52RGnS8vQF+kyVf6GPKV0gVZdIF0sL9mszC/SSGPVSvkYWdTKIq06XzPd9ERpQb5pkQbB3YXyPA29TQZ5q0ozpjOj0r8CZnz6'
        b'1y51oQEvoPNLaGRtqgrXkez7WVRNU7vOIa5MGKMX8jIzd+52S2aoEpmbjMpQFWiFB+gMswr8kgscWnloh5hxZGxdObaZeY+yfNjk8N9W2jAezKNgTlhm3qbpaoaaTytU'
        b'hmtpYGgauOfgUwDqRrdlNlQtB8jxFTZodHohW9a7jYoZjx8iPc08LgGfo4kB1+PIFhYkla/bRjOPAOVrSZsW0FKsQzUXEO5DNvmYCh0DtX0SHfVhIecR6UKafJyAjwOQ'
        b'QS0KcBOpdW8BU90rLqSJxBDwqlFzPmYzxCUz8H3xFp4hfg++1nEFukcx48xiBZuwxO3bhAy67KRmEfd+3IK6cY/GjERRLoDfgxrRvWwqgPcC3MXmMoNn4EYG1W0HSEQK'
        b'isFvbmczmXNTSI7x8KI1rGvRuH0Lm8VEd98gtqYtYa0BPqP2PWIyNnucSQasLQzVsNH0XvRgB+6h8f5zuBYfhzFaidm87DR0crVmqznpTCBuhuejVg3Lbd90dxpumx5A'
        b'5KrE53GVMVnUYRvIRuIqptOyEiV7v93KlX1MVBJ9iDeP7f8hcO1u0aeA31VBH+OPWeSXtS6DjUGK8EFSUJ8vlHFpKwUAv4ts2TR0n5YBJNlLhbNBdxezOeviWeDHA4pp'
        b'nU2X2v0QcpTEhRFJM/OqF8xmlxq6CjCwMiIMOAGjenSIyRKj/aqoto95Gi8Y+a8ET2uW3k/FYbazM3YWr8v94T5bB949TsEjcViY/s9+ZgFTeu0XdHraeczIevvwpNAK'
        b'h6Xn8j1lTT6Bf/v211+/921vhm3PvBU2H4Z4b+0a/vlf//Ir4Tdpby5Z6/jZhP1XfrLF9cLiK76//4uHLnjKj5wOqeP+6fPZqu7L++I81zUFv3srdOftO9aebV9a3+Vc'
        b'cQrSv/mL4RVBmZdsO2wdE9fdOZAb5ZSd9cXe5m8DEx7vEdUkHjB7r9tc9YZ3272u/OCyz/8e2/rTT84u2Tqjc8aPP0k9/eeseEljQtG68HfcvT/9e9vBn6y15L37Vc8f'
        b'XX/0xqHTn+g2tXsFymb89M0VefKe4z/65ovupJzqrtaDLo3TPr2v/Lxa9fCD9Ftv1yZHB2g//Nr+n+//+r0JTpLsukR7mflzav87cTV6GBjsHx/MZcxgxO9IuMFxuOE5'
        b'OSNl6Y9qAkMSggI8UJssBNcF4QqGcZHy109Cd58TcIH0sbg8KS0YVcywSaPYQ7yESw7dBLDFN/BRb3JWKCA4hAPc9+GruJQbgQ9nPaepkOot4B/3GA7pbGUP6eDmCcXB'
        b'AbgylAtO9X0B+LTNO5+T6V6AanJxVUpQAq5lGLPIBf5c6yLc+9yH6gZcV5TEtp8G6BcYsijJCR/g4V58rUQmHuL6y9RkaX6ni4acrZFKS42vb5xm5qgLtivzpTnsebQQ'
        b'YoZnD1lQo5BBiO0jPnMJizVwfVHKDC8WMI4uwwzHynNQ4lGvHXSQNE9vnN4w8/BM3fxBG/thRmzlN+js2qxqVDVsOrypnjfo4DnMmNt56yeeCz0V2j2x32fqgM9UemuY'
        b'y3eaNOg+6al78BP34M7sfveIAfeIbs2tkmslj+wfLeufmjAwNeGJe0Kfe8Kgr78+apjHeCRyXjxznzTgHgVCOE16eRmcMLFF26Id5sHnFy9ePHP1aXHVR3Sa97uGDbiG'
        b'QRU770F3aUvUoMSLEH6DXt56b32s3vdEbv2iQRvnYcYO+uTmfTL4WPDR0BOh9eakb3Ma5+gj+x38Bxz8oWvAgrb2W8yBq4vx+ow8elhAb5gxzm7NGY0Z+vR+p4ABpwDa'
        b'UWjVNzm6T0LeVE7oiMvUZ06uo2vyaU39pj7JFHibKoY/c/U8OeHYhE5Jv+uUAdcpI/riIKFEy6LO2X0e0+BNb78YtHOiU9QysUWt57SoT/h3hvS5xcCbnTRnt5bwltiW'
        b'8MO5OtL1FlWfjR+82UJHz5YNA46TnzoGPXEM6kzvdwwfcAzXLRh0GDntNq4grlXkoMT7qSToiYTUk4QPSML7bMOfObq02LXYt9gfjm/Z2u84udOxU97N6VRcdAVW9ZxB'
        b'iX+fxL/Trl8SOCAJ7Cx6Ionos43QEBP1pjA4NoZ5M8ZinhkPCThwJXlbRmY5xCfrcIgH4G/I3AClhvgE+wyZZ2SotfkZGUPijAxFnlKery2EO/96O1jCJRNexi2hJmpb'
        b'TcznyGXfRKo2wOUFecHSV/E5nMkwBv/tyzNriU5Vsal6U6l4mCvgOA6K7XVTK6ZVT3vGtylN2ptyIKU0ZVBoMyh00IlfDAsYge3ou6Vp7I+GeDJtokjmunUslweGjwSh'
        b'heI9SaAufDJxVSquTUsQMNaFvBg/MLPkLEYhqK2mpGQoCd0JPnBNIIcRr+biy7jDkrWoD6MszWaO8Lwu4TaF8XwtefGN+KyUOE9c1nmirhMDjpNZDp86TDxwmMY4O7v4'
        b'1GHijXOY+OOcIt5uvsFhemXZKIdpkDPWYaKnY0d4TOqCzVK50ccZ7c2M9lzGeCbp/8KBUiu3aFVqFjYXKtXgRG1m8b3xyO5ohJtmBL4gSMBSeKJqs3KBWl2gDqDM5FCS'
        b'/Wq/iMhLxGV9o7GdeKVTYOgU22JsD1/1COJJLcyTb5CqWH9OUaBWKzWFBfnZ4ABQh0qTW6DNyyYOAov1qWdn8OZe7QosUJEuv/Q8wMuUS8ODi7SF4FEY/As6auAY+ZMa'
        b'QeRBsu/oGAhStdMJ2MV1QsPx2FncUQdkK5IDEoNQVzp7VpbcSEtOSOEw6AKqEE9jlOkqtcNxjmYJMLH44OHxn4S3th+60fLwQAPHeqlLM6fkwoc+KdWtF8X1H9vpD90+'
        b'JDuoco1YHBWRHFRWsbe9qb3p6qEzujNl8860l02pkbW0l3m37I3gMR98ZT2/L1bGfU5ON6G2/FRxAIlYVODqFK0BDUxAPUnr+fjKUlT23Ivsu+4EdNt1dVJIImACVGM0'
        b'+W7oOj9/ukZm9m80mZnJsFMdNiRmz4izJnwkQW34Yoa14QvNGUdixqzmc9539unzndfvHDfgHNdnGzfo6vvUNfSJa2i3sNfvUWS/a/yAa3xFom5+/URq3DlWPoMS95b0'
        b'+u19tt5gfXRJX5A5YtW0+ZDQuGyHzA0LUE3QsprAKLX7aNHNWSVMpGf1Lxm0UTI/JdW2GhQwiL3JjMOZSBTpv7l8b2qWgPYWUQhz2XomTzuLzFZbwWxT1MsY8iJBwFvg'
        b'Hx5A1wC16YN465IiUe0W8OvOovsWTBZutMKt+Bx7ojS8WIv34lpxsTXxxJoYfAFczTLqbfhbFCiLxMVbSIEOfF4pKme9vUOoda0G37QJ5zNc3BqBGznOUVpWa5cnJufl'
        b'asLVXIZTwKBbuBG30gIPVBeO62aKi4vNgNtBcG1CJ4KdIEXr0MVl+DKqe6nrLYvY43o9duiCIcqGevEDU5Qtr4CNzfcGFHsrA8GEcBguquXE2cSPshBC40bVMS/Da2Ah'
        b'BDpjgE0ElsIiR2iyFGNDa9+/pTgAluLb14XWqIobHVh7rZ4kOpVU//cBqtfEjUjj//OwkSKPiqVRFo0PFI0RkIxLgUKhBZOQrxgvqDFUtGBxrDQOYJeamIz5YBoVRQXq'
        b'kiBpoTYrT6XJBUZZJbSmwYTFKaE/8rxx/OaB4ggZIZucTIqWfn0mYFlcekAQ/Jk/n/yJS1s6Bf6CeAHzwufRgri4gKBxHEf0SZ6nKXhlwIt0ko5zIRvmAq7ZxHqVFI4Z'
        b'QPL6j3CBiWNB4Xg4QF7/GSQYNXnfa5zNhONGmFOb1IXa2QyNs50G9faKL5y8zp6G4musSUW9DjTGcWYXCcj1qqwzM9fytqjZGNuaKfbMROaTuQIm08NJHMqwoaKT6OFm'
        b'Gqa7hs7SMN1NNow2Ny0cVSEdAjXihe9wHTgidMCP8mlzIrG60nBBWKaluWU2I+Nq7YjYp9VOESSxcJiZwkxBPVlswKdxJRPBZ/AdXMmEM+GoHddSJmnzbBkpU2gmLMy0'
        b'vBTgRJgQ3yMFHUVdESQfwhAukaiOcvFEVTNJDhk3WDKLmcX4ILpFuWTvtGAcmeGZXNtMy+0Wy5h0VWXT7/ia96HozQ/2Hlxy1QKF2d5fO9RxaV9MxYU7L2a13pkQI7Q+'
        b'37k/ZB++XbXpbMi3CYo1a6w4PO9fv//THaGhdR+Lqic1Pn5f5X094NZnD+74bur5qPfEn35X6n3xQFxF2i4nWWHelB/8yOsr7t1P7b/aOPfio/lci213p6ME50JHocfV'
        b'33eoC5JOaN/d9IsN3UsWL/jVi39u2t1aNE14Yd7UXb8JHvp66T8OfHxzS25TtePbO8wq7/7jZ8pLcW4d+2rrn0uS1KXhmvvPLzR7Prr+hso5P9pnF5a/86Ts43uRN9+u'
        b'uzkz8h3v9+8xUaunnVF9KRM+J8NSGD/LEG1RbDJDx7jB5pLn5IRJHD6Hzo9HPajFFoAPwJ5A9PA5STFPR53uxJKgijQSdwmFWsGkRRKM9GXUMwXrzRLwRdRFAzjkPEuh'
        b'OAlXywwMBd5cxgmV84Uq0XO6lJrQXXQ7KS0YAN6l9dxiTuzEXTQuNDkPnyaRm9A0kNQPXzfbzQ0AW3z6OVlnDmY7TJEYdH2JWSTXOnkufaA96jFPwjVJpmgRumpuE8bb'
        b'gB+gOzLRdwu9EFfNFHlhQZqI9THBrmx/+ZECtGQOC9B2AkCTjPC27Z2aZY2yhsDDgbo4isNEVpPA9Sa+fzznfbfJfX4L+90WDbgt6nNcNMzl2XkPevk/9Yp54hXT69Dv'
        b'NWvAa1b9ovpFL95nm4y40HBBS9QwDz6ToImDZ/30FoU+ot/Bb8DBb5jh2k0adPc5OePYDL3mXMmpkvYdHTvYKM3LmMszB6+nDhOfOEzUL+t3kA04yEaGCex1mvqIim3V'
        b'21rCK3frdut99fKOyZ1xp4L1wb28h5Z3LB8t749JGohJ0gcbW9RPqS5uce2z8YG3XtHp3ZHTLeqbPA3ehhrObGwjomWL3q5FcyJGv/XcrlO72vd07HniHt3nHm0MTNVH'
        b'aoh6uOwUy2fe5FvE2vPetOPAlUWrYhaakmUyxAPL+CqQ+tpg2rjgAckMj5jNP5OKVS+h6ypzDmcCAaf/jcv3GjU4IQpnrlnHMjwZx3DK22eGKRs7K4xNxh5G50Z9j9Bk'
        b'M7YxrO9Pv0fIz+Gavi84BrP9z3xf8Jt3Rpm1paxZfI3rmkM9TwrARuY5/699/dfaZd4r7LJZKvU6dqPD5OtH/8oqZ+GOVzm6qMOctYWlwbnGk+nL0XlUudyMnqV29HcA'
        b'rYkrU3D1MqxL5tovgMKD6Ay6B87NUSBkzGJbc3QTn8O3Vb/5lYBHPeb3/r7/+E8iwWO+Sjzmhz8e5TNbEp8509X2StkXd1xK/9jSfT5JPi/KLnfCjMagiLJd1eI3uo++'
        b'9+PSrnDwmD2ZxRPsfvUpRyZ4Tr48EYTbcSsxHlhvP85rBuMB67KOBtHxjVg5NT9RWEfj/dxg3CF+TvYuFx/h0GD/yEj/bI/1nvg6LX8D1fqPNCWsIeHHCDdb0mD/Blvc'
        b'nJSGe13BKo3IBcShMzLuCB1AtLVRnZtvUBZRZW78QFV5FsOq8t3C1/rao0LnY2PNHKtp7ztL+7yn9jvHDDjH9NnGDDp4PnWY9MRhkj673yFwwCGwzzJQTRIHrD4TqMnQ'
        b'vNLVJiGUzJeONgmdmIR1gY2u2UQ1FUi7WcjhEDf/1ZfvSxN9QRDUYVEA02Udw/u3moavY/7XNU3XqI26rDBPVaQxqRM2pQ46Q0ru5qjlG2iKfIxqMaonuTTyleGvUZX9'
        b'49KWp6YvXRUkjYtfEJe0bHlKkBSekpQRlzZ/QZA0No6WZ6QuT5m3YKnsu2oRilgllmb5ixjQ+dLMPLfFsxl6qH3JTnvy/fVA8l3yiuQl8az3Tzx/3ChD5y3Q0RL4TUAV'
        b'JQxqNbOwcEI6e1RKvzfH2YDKcRW6DarJ1B50CLUkXriTj06Z4X2qf8YlcDW5UP1gUw+rNEo4vOhuS91KXLLuZ60/k1nKqi8lNxZeXV3mVjaDm3o2/C2ff9jnHHjgeFZZ'
        b'Pbe1Omy3g8JvmRVv3lPu5Lyb2vDTf+xSXpQHLYxqdn3/125vCX5m+QbT9dP9rjHvcYb1zoqkj2V8NiNYiw9aBqIHi0w5QdARLUZAeSE9YLwS2GktVKCW5zQpfKsEPcRV'
        b'61ebEnVc61x8gDbGR9EhfCSJQlZ/M0QS/SIXLmoHjdkr478SMZBVbdp+QxbgjGsMIboRn6nWKDZojfUixtFlhHZ4TcKGaog5/c5zB5zn9tnO/TepmylQXe/V7xw24BzW'
        b'ZxsGd5tnNs5smH14dp+l939Lk8QRTTKiD/6jlEmK6H9DmahnEJk5WppCPbsbMPreBBbRgCtbF4oqWTXutoefy8ftr9Y2O4m24RtxDfnvCIZ8xv+OxsmVcT9cNzafMRLe'
        b'0MB/vnwzjYe8AtWQaAg5rlOohBuAfkbjjARW7+TJi4qUaqlCDhBlNFMKduTZbMpkXFhnFC9TiOffRXjYiM7/T2hLmKqdQ/Z3Nb6KykbBLVSP2/+jxAI65kh17V8KXRjw'
        b'CMKerdkzU7Uwg2FPmhxGjfghgWHoIbrGsAeZ6kvoGdSNmTPHALFJiw1QbAQMQ21YT/nrdpjTf0rStyjL8ufqVYxqotRXoCmEksm9N9hsxvmx2Yxky9afteaekiX/MrO4'
        b'IdfvPe7E94Wll31d/K+Vio7/RDn3nts7n2XxuxRvnQ056Prz+fq70xqyV3X3rtMfF+D3LzYWet6Y+zA084c5oIzv/Grae5zPb3hsmIxkZhS6oSOb8UFUs/yVCQ8C3fbi'
        b'K9TxB0e9GZ0f4fqnJaJbq2DMYbxBI6cImKmpZrvdM6gadlMUvTzTwUVd6HQwakDNrA4Hg7OSIL3J4aOw3vpV+P5z8v30BagH36ZaHvUqRil6oTaJCm2Hy9B9C3wriZVj'
        b'pBATUCMft6L9RaAMX+sIEmU4IvdiSREVrHqyp7aPoqhuP2PQ7QstXosIqbs8o99mwoDNBH34E5tJfTaTaIo9/IkkvHtGv2TOgGROn+2cZ16yp16hT7xC+72mDHhNqRcP'
        b'SnyeSoKfSMghCknEgIS453az3neb2DdpRr/bzAG3mX2OMwfdJ7VM12/qdw8fcA/vnjLgHlUvpNxDnkhCOrf1S2IGJARojjAF5kNiotczCtQEK/5rF5nN6IzIRqlTiHkY'
        b'NRDTiYHQGg3EFjAQrsQY/JvL95rQaRIFMRetp/NkvNTUhTLOQhk3daHqL7+rEmj0ME3DFgdrGv+w0mGJ7Q9/k2/x6XP7SivxVx9cVfzILNox/bnbXEenU5nJQbqcqZlv'
        b'xwZ12qX8V/1/NXwQ5J3ty5+6Yc/fPzh+W7NB/UFnYK7V0L6v9L6feDjgr1d4i2+ka3840fu3O/0mxL9f9vGtK7vCLX45y8l+1dGy9BzfiMAvj4a9czbx96hjTtLPz39x'
        b'Nu3A40/zvjr6eGaGevNfE1YXl32Uff+DnVfkd7wufuO2vzHqp74f//H8eael13DAFVmc6r3Ans8sXVbPfzjgnXmyfl5qzLMD4q8/Kiv9xN5/rvyNeXaVP7Y/3Kj09wt8'
        b'NjlwyYIVp8tOlH/9MTdooqS9aW31pI+XBvl+1n1i7d4jHwdcnPw0M/i29WfYfld07pfRWQ63Xdc8vjS4MD/trau8GT/e/iefrQqb25K/P/529XPG7fH+mPleb9l97l/b'
        b'8KMb/7XwhDTtt+lvVE5uTf3I8m8puZPf/a1HiVent+RxVa536Ifhv6yM/rzyF18v3/zBptXXPZ/+2H311EcpT/ZbX3NY93Fw0aFbW/x+N7D/7q9/g3ddk+zqkNg8Lv/E'
        b'z3xY9/zDKZ8+/QUn+Jv5F144vvv4Dy4TMzJ1OytWZi/++18cL+2IOl+TWOh7QF79LOqDZ8EffPht76SAg3/qmtW4Zc/Zky6/2bb9qXTo2GqlN3fp3K+q/pmerrKIe/RJ'
        b's+9bRx137/+NiyJ1bdt00WPfn7941rzr9x+vvqRryRn48Te/Oj/07dJZD33f3jjtL9r2P/5i94KKwuoHf70+9VTi3qxlf0qsWHo2ZlZOtfWqL9d9tpWzbOH9Uz/4kcsf'
        b'as9tWFT988SZ4W/9vjOrbbP1zifv2l3L+ebDiAfPAt/669uK1J3vfv6P0298uv5nCYlOU/2+brhbXr+5S+1z6m/Jbw9rHjdqyu55bJ/xpcPtL70Xrf7nZxl73nk27PLX'
        b'HbVeQbZvo6GvJY8UwdH+R0Hfkq01P2YJYBwOw4lh8NmVYKrqQb9OIGqxB1VFjse2uBIfEipwLause1CX+UhNjXrR/ZHa2godofpXibvgMUG4G1cm4JpgM8ZsPdfXPfE5'
        b'OW6C65zCAhODsS4hsCA5VcCI0VUubsXXN1PlOx/dQTVJxIRCDdt4XJ1Aalzh4q7l6IrM47sdYRO+7vKdD8K9Um0Ra2JCCXPJq3TUi9XuwoyMvAJ5dkbGdtMnqtXPmRsO'
        b'CFHVzmGsnIb55iIJq8rDK7ZWb23xrtyp29miadHow/Xyjqij209s71xybE/Lnu6J8KPu9b6u7V1yfdvVkOshj+Y/mv/Y/s34H8Q/CU/uC09+34UAf/mJqKOiEyJ9Yr9L'
        b'SLek3yWmb2ZqvyS1b2l63/IVA0tXPpGs7JOsJOjeviH/cH6f7URybOwNzrAFY+9YH3vYSTdPN+/FsDlHlMAZtJ9QH3zGsi94Yb900YB0Ub99/IB9fJ9lPPRg2MLMzWKY'
        b'MV501sOOjL3roJ3LoJ37sDnfFW7DRWc1bJ3CcbIYtLTts580zCOfn1na1ocOC8jHYTPGyg4Ic0oIWUJECQuWEFPCEog+e/9hK0pZU2risA2lbA1ldpSyZ5s5UMKRFgUP'
        b'O1HKmVKThiWUcmErulLCjSXcKeFhqOdJKS8DNYFSUraiNyV8DHL4Uoqh14lshUmUmEwryIb9KOVvkEZGqQBD40BKBRmoYEqFGNqFUirMUDaFUuHsAyIoEckSUZSINtSb'
        b'SqkYg9zTKDWdrTiDEjNZYhYlZhukmkOpuRwDk1gOpedxDGziWHq+kV7AGdFp9rqQYxB7EVsWb6QTWDrR2DaJpZM5rBwpLJlqINNYcrGBXMKSSw3kMpZMN5DLWXKFgVzJ'
        b'km8YyFUsudpArmHJtUa51rH0ekNxBktmGsWUs3SWkVawdLaxuZKlc4zlG8YPSS5bNmVYxZZtNDxqE0vmGUd7M0vnG4oLWLLQQG5hSbWB1LBkkVEOLUsXG4q3suQ2A1nC'
        b'ktuNUu5g6Z2G4l0suZtjWAZ7WHou11A9lsuuA65B0jiWnm8sX8DSC7nGuWfpeCOdwB0xHIlcxsFn0H7SoL2MXr2N70nDq7hjB08nGl7LZdwnngw9FtrvFjjgFggaRRRK'
        b'LxWJurh6p0GXSU9dAp+4BPa7BA+4BBOYHEQvDfx6Tv2UQRfPk1bHrPTyTrt+l8ABl8B6Qb1g0DGk26nfMVq3YNBzwsnVx1Z3Cvo9QwY8Q3QJ9YqKVF0qqCQL20GRrU5S'
        b'r2jRdMZ1Z/eJZvSLZgyIZgxzZ4kih5nvcPkrj7GYCS3JX9tq52E+KYCxNjyhxVev6eb3iaL6RVEDoqhhrp3IZZh5zYXwiIZaJl6kYDIjcW3e2Lixzzu933n5gPNynfiZ'
        b'yIYVf5net3N+t1O3tnfFowWPJ/UFLu4TLekXLRkQLRnmTiZcv8OFPHUpB5qaHk9KFnNeDlafyK1f5DYgchvmWopgHsZfSFN3qGBiQQo8XsnBWuQzzIy/jONACqSm4VzW'
        b'J/LuF3kPiLyHufaiacPMv7oQHj5Q1cRrVCk991sRO2eePYPs3eYFGRKBtkPcjIz/NPv3nwAK25d+0GgQoV5OHCITfvCl+MHoDMVxOBxb4u5875fvNYGoF0UzN61j+TxV'
        b'YO0XXM3bcCuQP1VbnyTeN9fx4F/uJdc4C+YtqFsQO6fzSJK8M6XX/03nO+J778weuvPRPvVHJ/PmJh7+7NEjj5g/3P3DOzvWDM9z/Jx3TNUba+2abqk79PjP69Ys+mLr'
        b'74IUR/Thx/629NdnX6RdLT4VuTSu496KaQsPnzq2+OLQB7+/4qPccCc7bc9FP95Pv3rctq/wm8M9v/mt3aDzskb/8h+8KCrN/uW02sKMX81hfN+K7t/4WOjdJJu5QCiL'
        b'q7XwLNpSy5W4PLOYlF9Y/vefJs8IfTrcePLNu7s5bi5T3twfJLNiwwu3Fq2j/x82DdfRYwlidG0mruLiTq71cympcAUdwD0kaHOV1EoL5k7AFYwdvsdD7eg6bqKnO9Px'
        b'FcDWVagO15G4AqrBFSpUZ85Y2/O8psxizy7cWYDuJCWkBEwUpZgzZnyucIOWHk9ApQtxT2CiAPdMZjhJDG5BOlz/nHzhekscPjA2HYhqQ5MA79fialzHm5TKLCL/r6sO'
        b'NyI9PYya6IqbxjYxc0FnGcl8fgDS4320licqFyex5zFqc1+yY9zRcT46i45n0RQZboJ+kFhJdRKuMkdd6A7DD+agS3vSKfTHnSSGVSUDNjB0FWkOaD+gApslvOVFuIx+'
        b'0SUIt6GTuIq3k60TRGSn+QMOI8U3BMy6eXQKpqzdGJgWBJ5LFTsB+MF01MbFt/AJfIw9YXsI1ZN/K4KrwckIXY8vBGwxuDxuWj4qmxon83m9F/G9+A7f40XjQ92Qcd7H'
        b'mJfJGVHlq4pYZ4T9RJ0RFcd04sCNETiUppKfQSvHp1ZeT6y8Wrf1W/kPWPmXLhzkW5Qn70vus/M+E9PPDxrgB/Xxgwb5VqUJ5AfMpZtXH995mGshWM0ZFLr2Gd+A4L38'
        b'n3pGPPGM6PeMGvCM6hO6DQqt68SV4p87Tu4X+g0I/fqEfoNC+6dC9ydC95bYfqHXgNCrT+g1aOP61GbyE5vJ/Tb+AzYkwSkC3pb2damVqX3ub/RbrhqwXNVnuerFiy/t'
        b'GEvJMMMVhL28DDq56iwMT+pzDOkXhg4IQ/uM72EBVCH+i/MmvgB0/f/wdbWIsXQEdUi/siLgz4tmULR3nBsPu3LgyhqVCUO8PGX+EJ8cJRwS0PzfED9PpSka4merFHAt'
        b'KIRinqZIPSTIKilSaob4WQUFeUM8VX7RkCAHDAT8UcvzN0BrVX6htmiIp8hVD/EK1NlDZjmqvCIlEJvlhUO87arCIYFco1Cphni5ym1QBdhbqDSqfE2RPF+hHDKjkXoF'
        b'PZKtLCzSDNltLsieNjWDPaySrdqgKhoSa3JVOUUZShJBH7LS5ity5ap8ZXaGcptiSJSRoVEWka/VDJlp87UaZfZLY6khMYfMf/WSSlnTl228kH+9rAnmGL3m17xgBdtx'
        b'OLk8YsD+f75+b7aXYJc3LUSxUuZNqXVsCO8bofG7e0O2GRmGzwZg8Y1bzuj/My/NLyiSkjJldqpMSL4zlV2ggPmED/K8PEA/2QatQmK0cN8Clo66SLNVVZQ7ZJZXoJDn'
        b'aYYsR2ZZ1PsZQ4iYDRaTKf5GOJP9P/az1eTkE0m0aXbBZZgHyGaYy+fwAefDxZIRW5WaD5sthOEYZkZcl1owIjuD4khklQlsfk5UX9DsR5MfTX7T/wf+fUGJ8B4U2g5a'
        b'OOuC+iQR/RaRAxaRffzIQca2j7Gtd+ln3AYYtz7jm4r3/wB2nozR'
    ))))
