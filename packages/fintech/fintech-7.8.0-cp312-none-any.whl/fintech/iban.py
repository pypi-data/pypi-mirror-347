
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
        b'eJzVfAlYVFe27qmRKop5KiaxUFAKmVHiPOHAjAOYaFQooJBSZKgBh8R5oJhBVEBFwBFQFEUU52Tv7tvpdG43BDsinfRNuu/r7vT0MCFtOp103tp7n0JA0915X7/vfq8+'
        b'PXXW2eesPa5//WvtU/yaG/UR8d+fb4ZDHZfFreM2cesEWYKD3DqhVrRZzr3wyRJeErAzvTxLJOS0kkt8SRFnkL8uhCvSLLHlnv0CkK20I88IuB0SebZa+lW2deziRUmq'
        b'rflZplytKj9bZczRqlbsMObk56mW6fKM2swcVYEmc4tmkzbE2jolR2ew3JulzdblaQ2qbFNeplGXn2dQGfNVmTnazC0qTV6WKlOv1Ri1KqLdEGKd6T2q6RPgv4L09j04'
        b'FHPFgmJhsahYXCwplhZbFcuK5cXWxYpim2LbYrti+2KHYsdip2LnYpdi12K3YmWxe7FHsWexV7F3HWf2MivNTmaZ2cpsaxab7c3WZmezjVludjVzZpHZwexudjFLzHZm'
        b'N7PC7GGWmoVmgdnT7G12zJ4AYyvbNUHIlXhZxm2Xj5wTcm9OsMhw7mM5F3C7J+z2Wc1NfsnVbdx20Vpum0B+UC1Myhw9R7bw35l0VEyndQenliflyuA8aqWIE3PvbLTl'
        b'0nM3yOM5kx9cfBWfQddxGS5JTliJzbgiea6LGlfEpq4IlnJTl4rxQ3xYSJ8ujJVyNtyXerEqPSHFPoAzbYSLYnw+DHfJbVfGgIry2NQY1BGAzUFxibhmtQyXxKSCykpc'
        b'NQ3U48qYRFy5JiAmAVcmJSTjWmVqAJSZQ6G2lTFxqQHBMbFBAtQu5oyoxDUK3cKXTTOgCnx1ET4J2seqAb1loStjguJxOdSbgEtjJVwRqpLha/L1+PrGTMGoAbGzDMh2'
        b'OByzLYZBoTMlhlmSwizKYO6sYa5sYD7tzPbZdnSWYO2WiEdmSUhnSTBqloSj5kOwW8jP0rir3z1LihdmqY3NUv96KxhnzqF6y9bc5sBJHL1YvZtMHcd1hu2xqZ8axy6u'
        b'cpNzDhwXpnJLt8lx3cUu1nqLOfhWFSzbbOMXsZNr43Kt4fIf1O7iYSdu4VB0y/zPhDfD3b2GuVxi4Hf09YJOK879k7j0iA/1ycl/YpdvZn9uf9Re8NofUz8W/N39DeHX'
        b'3CBnCoYCF3QZlcJ0wOijhoUBAbg0NCYYl6K2lACY9aqgkNjguEQBl2cvnxcSpw4xucAz6Kat3GAjQCfxUZjPeg4dX76LFdyP0Rj0EnQI3YKCMg6Z41aayKjgHlJgtQDv'
        b'g/MKDpVmF9AHkjeuMuCbHK5FbVBQzaFy+1CTK9FUulliQJViAzoPBS0catyF7tCSiUl2UCBMparOcOg0OoOqaIkQt+EyQ6HEBtVCURXomIobTe6k+iPoLjpswNek2Iy6'
        b'QD7GoeqN6Bx9zBu1oRsGkyQtFQpqOFSG7+I7tNXo8pRcg60U18BM4yYONYSw/i9DlTMMuEucjkugoA50xbmZlFCQmY/aDKicQ8XoHpSc4tAJfA9dodWo8SVbg0KIe/A1'
        b'KGoGbZPRBVoCrSvzNWwTITNc5vBxDlXGS2hJGr6OLhvsOfwA97CH6hfIacmE3Q64y1Zsj47A9Q4ONaHb6JLJjTS6Bp9er4BJ6EJ3oOwSPIPNc2nzYlAJeojKYOa6UCcn'
        b'kHHoCjqCuuljeC/q3mPA1wXoWhFpEoeq8N31tMh/G6rFXSYRKnFmQ34UH0K3aZEPaGxR4E4Jvo1PE9uG+ZBPpS0MxftRjWGbMGM3U1cKD52mw7cOdbxhwLfEuBZWO26A'
        b'Fqf4sUm/iK/hswZ7IeraxGo6sUHJhqgtBGalSya0RWQgznHoZLiGdbcWX9gMJRJ0cAqUXIQGxPJdgr6dFeIuo+QNZGYVVeFDWjqzSwxZuMtG6mxijzSia3lsFKqS8R0o'
        b'EcCAkoXXCuo8PFnjStJycRe+Ji5Ch6DkLKz6wtW0JNgOtQJoCib7w/UrHGpB9/FeWhKOLxdAiQSVa9ngnJmMD7CKrmt3QokI740DoZNDZ8HmTtOH9szBpTDc0gB8hC27'
        b'miLcwprQmIMOw7QL3FEHe+qMj4GW+C9HldC4LkHqXChoh+HZiavYIFx0gBUNRVbooANbK6dVG6hVoJPoNL4BsydA11E7a3sjepjEGngW7cVXFDIBOr8DpJscOo/bHOky'
        b'gucuoWYFvm6F966Esm5oBz7AGqJGdeiyokiSspzV1YDK0UWTB3mqFTRcVOCbYvBPxG6ukdr2o/20uq24GV2CQik6Q6rrghW9CN2nRTpsTocSCa5GNay2Ftw1g9a21Yh7'
        b'DEYB6lRBgZlDh1EN2JQTlCy3j1QYxDI5G/b65eiMyZM0oicY16CyKNDVjQ7EonIJJ8JnBMmeLiYvUnw0nRhIET6KKtCBTFQq4cQ5ArRPhlpME6mRFE6A0Ty6hd4RQbWA'
        b'CjmqECpR/Xq1yOQId21MDwFAPY9qgZDlc/mLhfTqNCdkjncg/pDL4DJQu8zkQDRexg+84j1jpMDFuKxlb9JuxaNbu6FboOQB36/t+LppKmngOXzXHdcCil2KQm0STaQs'
        b'EVXgc5uj0dl1idx0gwQdQ8dwGTWzWLQPHTQYJYYUUFJCMKnSxxRAjQnfWGdRcgUfw0fp6XR0CR8Tc17ogDeuEMulgWzNXcaHow34hgBVTmcQXemzzhQIJTJ004FpQTfB'
        b'AEBNDLpi0YLu4m5vdF8sQvdQBZ0RW9UK4jPqCnmXkaCgjUH1fnssbekY1ZbLRMtK3OGNj4il3riOLeamzQrAVyGsJbJeT3PoVAy6xjp1Gt3Drbg2Bl2GkRlRFEFaBs1p'
        b'0XsHi3CPQkfbAk/7GPTiabCacTGHDs7ZyNqyfyuqHhkYiQbGFt3brFDhMtSqSVnjzMWprBTz8XlmIJfQIfyQeLsr+ATv7XxiTSG0KCzixfFFV3EF+WoHv3mFNCpYLylE'
        b'FfOYh6pBPegOuEjcAm6D+UjciY6ZgqDQNRvdGOlZhSiDtQsg4wRMPSpbl5gUxcXgHinuNq1i43QKTKsd0JzLgzWIK4lTq880TSLIt0czepDIlIlRpW4V54W7RLgzFB9n'
        b'DvsIPlZgsBYGL2HTdUy50zQLrm9bgootk46rYB5aWadGT11rIlF/OVGakcgVoqsydFsNY0YWUy46j84aUKnYiPcybDv1xgbaxcQdSlw7y0CaY5k9ETqCS/AxdDgbrOwE'
        b'YGmTBEDuKjSQqJJ44RJCHVCHkWcO+IKrSU3ciyF9zIJiq7KdLoMGtN8b7BLfw3fQITpUEtSAzQY7IYBaBSg6AStzE6qjy2FCDK55mZm0EVXhSd64WGyFb+BWNuSVQCPu'
        b'E8qCatbxlCVCSClW8tzJz9VU4Afo6ri2UYuZ/gY0xUbE1lal10RCclAz9JCxnHhcagol9RzbLhoBAFBxN9yyvC7RmZjOFnwErpKgZoE7RYJ56LwBeBFgzXGeGDlOpT18'
        b'4zXtWAu2zCBRYYPrvHGHWIZPJNIRd87DdZRCncriGZQebC+MYsR8fGZ0o47yOi+zxXFZD90mCx4A1QB+iU1gEr4A6qxm4nLmnI8K8Clqna5OTkDH8ANrno/NCqdLBB0L'
        b'ybdU0k4qAc+4g6wPdFiFzqxFh8FAE/F9qwgVeshIQzmuw01A4Oyyef6GexZTVf6A3A+fwyhgOG/r+MC6gCjWfQNqkuFyd2s6ggIn3EYYH96r4BmfKt8UTtkW2gs4UGuZ'
        b'gvHGfhmfwodZ349LDEkAzXTRBeIHBuKSb2HCMhph0cXDoiM1+eKbrwNNTEM3eJaIOv0o3AYFgHrLupbko2IND/3RKqDPrdD5ZHzaKsQD72PrcT8MzG3gX6DhCM/AJm2j'
        b'bYbJMAMCjQDKmJaTleCHr5Mmh6C7EhgRdJ42DFdseNWwDdaoms1+xWJ8hfqkqIKJvK728b4Egry73lNFQN2aZExJ61oJoX6Js3jm5wdMCXgbN0u8czwsTScmAjo6cbUX'
        b'vinC12YwZpIB67gRlAhwhy8j2UdxTRCd8eX4qoDQxweokuePqMuTQvJW3JI72giPobKRxTraCAslQBacmeerXxZksBeE4ErGOE/h0/gwbSy+tAzqrH0OVuSM9zTzld4i'
        b'Eb66Cj9kllzuAMgExBX3UJdFmGtcBJ1QoP17cbelUVfHm58buu+NzwLCNEnZaj6UiJsI0V2H6nii62SkEbUKyOpZXg/em0j6N8YQAeCv2yQuWoI6pnB6fEyGqyFMYovk'
        b'AQzFQUKR8YEYniJvd6UkD9/Cx2KBN94QpNEoD5bicdzlQX2IdcTmF7xktErCbfeejpolqCl8MxvAk/jyZCDT4pVWoOA8kc/H09lAlyaj7ucLcHr4eIilaB2JT0rQkTnh'
        b'dOWs2jqfMHbUNoen7EpcQ8FnyW6GPTCcJ1i3K0YQgmoTQe9tN88QrJQA1hwN5d0tBhJLif5DammE6OPru03ToHCDb0E89WCggjc3zSiatRa4/ypUYeWLGvPpKFrDaoOR'
        b'um7ljG+xjp5wQpXUF03X4ftgncVbxjhvqgncNheJuiXUcfTQPm53BX7XZWcViusYbz1rU8DIzXF0WjzePiLYKHnjRi98DZacFz7Ehr113nTcBd5jWQiJMzh0AR8MoPOW'
        b'r9o1xp9R5583cxWEwPuJkd6YxQanDBg2rIpCISzQs8zEqtDxWdTat+F9hWOgftTafxV1eaNiEb6Tw+I5XPLGbFAjBarMUK4aXdxjmgwlISkQGY/rjxA4SwPhIbfA1jcx'
        b'WoTaXfB+GnXhCzDrLOzahUpZ4SV0AGwSIi/c7cqHXnD3XVZ32fQcEnol+/ORFwTeleyxHiDGd2jwVQ/PsOhLiY4yCngoxvAiEFG6hrozvXAnDDS+Cb5YySz4qAsJ1Vbg'
        b'Lj5Uw4dwGzOtRmti+CYB2vsqM58jEfAYGcIkL7b4r/CrlJ7dYEMIYXgZAZAbpt20G9PQ+UTQIlkOK5SSiloPfIcSAbjzuPWo6QyYN2I9V0ZMAHgKPiFBpzevZzNbgivj'
        b'YDi7peg2hciLxMEUL6JGGYRrRkHkMSF0k+9+62h9r0pgGks8Gbq14xZ/CEiFUVI2/s0AEh105fuhQ5rn7mojOmfBiRF3tSLBatYeYBBEkRfqITNpK5jtzAe2MJXXGbm4'
        b'hfYnPMeKuXljyJNl3CLRQwks0mqIGensX0VNs0CfBJ/NYKHm2cQM5rAfotL1vLqbSh4thJl84yCgQT1Rjsg8Q4BOLrROWsqH64mydTS8DkFn+fgajPYCWzG38YmUF+IO'
        b'HsSD0GFvtQjfykG1bFW0AUDSaNz+NT4Yxw2erJ9XcCnoGs+iLLwOXUb7mVsONkkKUHkhXYFKfA+dgAheCmFDHVN4aheupg0L2QBPvLCUmV9ui/PCt0WgrwUf5Rs2D+0l'
        b'qYAUGZ8IAM1H6UzuSOJeShJZnHcSbB4/FNstxiwJ9wbuSFPIpOgaRA00WD+Hri1jIHYU1aErL6IYjfRw9ywvfEWErwj5tE7FlukKmQC6XmnJPpjxCdqeAlQCa2WEvGVb'
        b'v7iygqxeCYeQnQQymag2X2EU77BjyFw7EzXQkdOhu+gGyWGkogN8DgOZgcsTAjpp51qFtTRaB9dvA3xGA9Eh8Lx0zRJFkdgLERLdBnQUHUBXqSf3whehdaOp6eilCdHL'
        b'TQqLDwX+tEm7s4IVRVJ81pOl5+rWQbURhPqhFlTLxmcHRJfjlibqWkec9WZ8dh2n3wJBlRE1sXTMfnRKrigicWizJelyF9YbjRbuo31boWW3AfBeDPclTnxkdRliBRjV'
        b'hwzVWrfjFpKnwef8LWmaI4BqlDrex5UwtePjdboyGEbEAuejdLdWYkTXPBnsnIJ6Kkh2B25u49M7uKSAuasDSxQkvRO+kE/uoH24iRlxYxwyK+wETnQN3APHthZVU1vB'
        b'53BV0SisChSNCs5GY18LsBF8JoIB5uF16c8nqWL8aFyRFM6Aka4UrJBZReEDhZQKwEBeexUeaoPRGRtRosuSDJiSRC5CCfFDMipjnO48OrZmTDTArwS6yDfg897oulgM'
        b'rqiaLmXwA/VvvizEpMyX+DdvXCqWRc1jSHNmK3jBF5GGGqIbrvaeI4L5qShgOHdu95TRYFIJFv0cmkaPUa0EnZqA9qtlDNI7ISipUNiJcPlWkB6AC0YHs9g0Hkf30EUF'
        b'viYAo77LzLIFl87k0yEB+CSUiXbRRHAPyWhe9KV2s3sxqlTIhfi4gU3jRVw8iUUDJT6rFCbxaj1btnVAQVj2YSW+vkNhEKPaOD5/t5DtL8xBVbMVBit8YAZbK6dxezht'
        b'mgim+QYqAyCcgavJMiW4YwZnEEmGom7bHCirRWaW2CtFHbyZIjPNBIpRVwoqS91i4l7dIMVN7rhOLWb5wE58DlXhsoQ4XC7iRBwqxg/ItocZzIGu0Cv4BDoDoXmCVIhr'
        b'OeFGQeiqRaYJNB2Ary+Px5WhuGKaGrWLodLDnI2DyBWm/DpDuH2r0IlpScExYk687NWFAhjn+7g4k+wKWT5k44buKRnhcExq2eSs48wCus0lNHN0q0tkVmTL6SaXWMiV'
        b'SEc2uSR0k0s8apNLMmo7S7xbwm9yjbs6ssmVrRZ+MiQEgqsa9Ykmm7MGlSaP7sqqsvP1qiJNri5LZ9wRMubGMUIs2xMO3JKfZ8yn+7uBlh1hlQ60FWl0uZqMXG0QVbhc'
        b'q9/KV2Agz41RlaHJ26LKzM/S0h1iopXqM5i2WnaeNZmZ+aY8oyrPtDVDq1dp9Pwt2iyVxjBG1zZtbm6I9ZhLsws0es1WlQ6qma1KyWGbz2RXOmNES8jLHsjQZc4m3dyk'
        b'K9LmBbGnSAMXx0aPaYEu74UekU8mDIx2u5F0QavJzFHlw036l1ZE+6bfMboyo6WZMJT/ej1Gsg/PawtRJZoMRtJHMu6rk4Mjw6OiVIsSVsQsUkW8REmW9qVtM2gLNLRh'
        b'geQsUKWFpWHSGLV0Wz89PUVv0qanj2nvi7r59rMRp0uL74tqtS5vU65WtdSkz1et0OzYqs0zGlSL9FrNuLbotUaTPs8we6RGVX7eyCINgqvLNLkGepkM8jadYVxnxmzs'
        b'SrjxG7uOScuY9V/A3d6GQokeXeDTag7oIt20PVLgwQ1tzea49PS5wuT5HN0AmBBrjcrgey2+jB5wa60X0lt1GxVcbzo4A4f0oOEZGrbpuzwN6MoMiHTD0hN+v8eZo6Bo'
        b'rV5uUAgDMy15oVKAKXsGJXUQ9hyCQnRFx5faokvMu14JQQcN20QFeRzbWUSH+ZIYdDvOYE9SAFXsmXrUkEErSsJ1C8nmoiyH4XJTbhR9IhW1rCYbi/soxJKNRT9UQnG5'
        b'EHXEKApEQL8bWSxdtzqLrx4dRN2KQlF0MOP1J9EZtlGELxtcyFakGrWwnUhgPGyjNAq17sFdBuk8mlaHkOfIFMxvbd5ZUUS2KIEH9bCUVtUGfI+2OW++H9miVNFcBdmi'
        b'5BIomXHGN/3I/iSg+E3mS06jB/xG2w5cjEsV20RydJM5s9OoJJvtYx9fkIC79BI7wklOkri1LIx5uQsQElcYtlmlBbA8YBU6hM7QZ0LRLZlhmxAX0w1mkm7zFqpFjDiK'
        b'pSQRdxsd5UtQWxgtEKESH1rPbks9xXF8T8F334J6tDRCJRWl4h7aoyzUlExTkfWonM9Fgk+rVwtZA1txx0RSjOq9+FI56qJFE1/Dx8jmdDLq5vi96TZ0k663YRcrLncy'
        b'8FFVesKvIqM4NkMnwGlejAwTZ1mRbVYuA+1F3bpL7V2cwUEAIdHVrl018Uk4zOHwj4r+I8lTuPjyieCYt+TpP/J9LTV3efvRmKD1bedb571lrJq5JOTHA7GB7XPvPd3+'
        b'm88XXG36o3Ig79HGax0uNkn9H039yeCeztPa6XO+DZyd/U513p2mv4eLilztPG7Om7zjQ/PhlnN9HRsemo+kfHO7963DMzInltz/WLrW+UjwJwfLH2Sf6vCe2l702/al'
        b'h97v+Cy/cFVmbtHbIQd3DV06nfW54i9xA3fVa2av/nb2T762nWz1xdwHq26KU4467Cqs+tOc4f+M/W28e92ZFf9r8le/bZv4Se9vCv6+JirlvWv/O+Mnby767Ffbylcs'
        b'em1xZ1Vc0RGflJ+9b/rGZfeHxfcvRv/camjZ29Z/2WyVli2Zc6zjW05SvnLl8EG11TBhIstx+a5pwQExuBHXBgs5KTohDMbn8ZlhTxqutS+bFhIbFKgOwVVBuIQTT+Lc'
        b'VeKNVsuGyatNwEXO4evxyXPQ3mBUkkxoBadYKQTuVjNz2IPa7L5c8m5PYDB+mBwiAO37hZHoImofJvxQijo9ILZkL9ZsYy/WFAUH4tJQIRcC5KJnlgTfmInKhynLb0cX'
        b'NbgsMShWkE0ynNLpQrtZqGeYZGdwHb4zK54pACJTRekPvrSKc8UHRbgH4OaSWjEoDFDriel9r4OBvCejUu21fL5ynZutz9+pzVNls/fEQojjnT9oTd1AGhF2jjoXEhU1'
        b'sPq+3Ms9XSHhXNwHlN4Dzsq62TWza+ealzyxdxpw86jT1ehqt1SLnjhPaPa7GNoS2un3aNIrQ0Kxq/+Al/9jr+A+r+DWrH6vyE7DrR3Xdrzl9Nbq/ldi3/eKHZgcMCTi'
        b'vOMET2Wc5+TmyFarRx5hA16qJ0qfAR/fZt/mRfU51cuf2LsNePo2BTcEnwyttiK1L6hZ0Dz9kXPAgNJniBNMXSF4ygncVwg+nug34OpRl1aT1pzyyDUQSnunRPUpowZe'
        b'uN68pU8ZTi57TGia2DCxVfnII5zU66ysX946v897FhEcXev96vXNgvqA1pA+z5mk526e9RH1i6pzzMsH7N3qdX32U8lVlwn1m/pcpjx2CepzCWpN6XeJMC994kyG6om9'
        b'x4DS97EyqE9JCpQRvQ4RH7u41zvWO1XH1G+Dh1pdWjWdglaPPpeIasETZUCrY79yWquxTxnZ6xD55dBSAec95bHXjD6vGZ9xAlf/JxP9hkTw/ZWBuLi7fkuiuB9E2S+V'
        b'iX5oJYCjHqCDU9sMisnkDYqAIw1a8YxjUEwowqBVWprelJeWNqhIS8vM1WryTAVw5R+vIRuOeFbw3/w60hMs1RPMGr1WjpNbyZ7l13u5ZzqxQDBlmIPDJ3bKsi17FUNC'
        b'icDlicKpbNYnYvuDiQMy+ycy5y+fSjiJg0X6ykCw8aR0GndJESUCLGevCODbq+NDCsEkcFkSrkyOlXB2BaKZC1AxLZ89BZ2NT0hizF8AFt3EKdYJIVAo8ePzghgiABoy'
        b'TNxOIwZ8CXdnWt7dJB+xhXHkENovZLSfkn4OKL80W0ypvgio/ghx3yWmVF80iuqLR5F60W4xT/XHXR39PtsnA4LxVJ++fTmK6+vzt6o0FnY+loeP5dzjOHXKP6D+em2h'
        b'SadnhK9Aqwf6v5UxU8sroWO5WbKFskFDAldBjbqt2qV6fb4+kCrTQEnWyxk9aS9pLmP14zvxUjrLd4o9Mb6HL6uCxADLcjWbVDoWiWTm6/VaQ0F+XhZQVxoKGHLyTblZ'
        b'hNoylkpjEj4OeTmJXaojXX7OmSE+0qgigo2mAuDCPDOmowaUPoDcEUQqUn8vSitJMs0lHmRG7svezCxJCIwLQu0p7CVNciE5YRPujE0UkBxFiWIW7sAXUnTBt78SGiBi'
        b'5xJLO06+G9HYUttdf/dgjcB6lfur0U8uyhPLGy+vfc/Gvbn2dq36kG5GypTDJftajrccv1Z73nz+cMvh8Ap1fcth3/p9XRIu9LjNwP7tauEw2bjApzfrFIFgULgElyea'
        b'eJ82EXWJvXETvorKcobp6zkdnuhmfEgcOLWFVqiCd1ycJ7ohzluIDqil/wRXpCO+iSLKoIK9fsy80GiBuqEFHHNDy6w4F58P3Sb1Tl7c7xbd6xA94DH5sUdon0dop6xn'
        b'6lvT+z1iSuLMS6r9iHNSetWnVO/sdfAFt2GO/5zMBsNIq0GZZYEOWvFLTU8ctZ4QB73X2JZaMQQkjWXg50vAb3QTH5PbpsPhb4B+W6QCgd/3Bb5jUn/uvCJMZJpNWKc3'
        b'PjiSQ1HbWbIobfgYEPzrqBw1B4k2xE9HlRAKoAvovjWXgY/Y4sakRJajPGTEVxRFdoIdgIcCCEQA9GrRWZZW6lqNziiKCgVANu5DoRnIKT6LrlMSuhR3TzLgm/YRYk64'
        b'NAkfEbgl8G+MoWZ0GN81ROiFJKkkyOfQLfwgmEUdNSG2iqIiaSKQZwE+BExWDo0WsbKW5biUwi+6tY3H303s3bBS1Dx7VMpmN66hGZvXM1myqlLpOw1wXRC8lROiSkF0'
        b'8jjYllmsqoB7nq0B2JaYLfkaOcC3dbZsBL6l/zb4zgH4/ua7MjUUd8bmab4TvAjQkdv/eb7jO9IQ5OH/8SxEZi5tlkFrfDHvMK6BZFzyMzNNgNN5mS821JJ5WLpikSoa'
        b'6Ime4PgS8FeZxnz9jiBVgSkjV2fIAUUZO+idvF+J1kJ/NLkv6FsMNh4yqm0aMikm+puJwNXRKYFB8LVkCfmKTl4VDt/QvMDFEYtpQXR0YNALGkf1SZNryH9p/oR0ko5z'
        b'AcuagNYs4lJ2FIwbQPL5l5z1iMb8ghd9NPn8a356zOT9W9M2IyRqxMfZJy2jTg7vm4YP4DLU4/evebrnbm5ZCo2WHxS5c2EcFxaWsd07Z2cYS9lgX2eO/P7i4/l73vzB'
        b'JANHN5LeiMLnADU7yFbCWm4tupBKoWR2WDAqQ2byVvImfFLoLJA7e1ElZTvsOQgE3fcuyAhyDFnMQVBP1OBqCb4aOWEhnIZz4agTnaM5j8mB6HIkOo5PQBcjuAh0CVdR'
        b'Le1KB07FcTNVhp0J/x0yx6IF3cPngiLRYfSQ6bGdwACxB1yoGeLGRjfwKiu4FagLHaR6UnKsOWiuTOW0NWj7TDmXoouwTRMZfgRF3St+t2tFuB0KszGeuqALkJVI+uRy'
        b'6e63lF8ufmYT8NH77eedgnKzl8890+RnGyxz/b3/nTlNP5tQ8nTeTk7z083Lctxt2j/9pdeRG1ZOO9YPbewfMFZOW70QmVuafjlPubB5r99S2wfud+cfWLlg7vs/+PaV'
        b'T3/718aGhgrtzXkhM74OO7FpTt0ph9+n/zzjk6fom93zT53DV6c/ev+NM076T6s/y1m1f2tqXl1lWXfC3i8HgrvmbV8+76OFjn/5vVvQpurF/xk486lL4IXK5GN/Dfk6'
        b'6k21bJi4EidcjPZPCw72DIixhOzWyMxCYbMHOvgi9bDGXYR9APW4kTpMpn1ugYw4B4jakyF0hzEMhfuCyTPxVlw4bpbGTnAb9oEbJ8oSFPG4DTfgcvWIOldULJbhk+ju'
        b'MP9m6VG7+ORgATk7KSwSLIJYo5IWzZ+OakgCIAyfCU0mbd0tDNz5Cg3oheBSb0BAv0sWFGsJ6PF1V5pYWIBb0al4XBHP5x2WBHGcfZhoE2rG9Wr59wvgyabESPzOeJKc'
        b'BV3gQHY+P6Uc6SOeI70JHElJQlMn1zp1jbp2mjka2NATpe+HnlN6py7r91ze67J8SChy9B3wCXjsM7PPZ2aPc7/PvOrlT6XAruozmyMfOU8d8JrUNKdhTrPh4o6WHWff'
        b'eOQVCSHzx84+j539+pz9mlc/clbTGNepOrJse31E6e7myc2alimt0WeCe0QPbW7bvJX6aGY8aQbcEl5SVO/RZz+pObPVtyW7U943ZRZ92K0+sr6w2bF+ZvO2i7tadp3d'
        b'875XFEsyfDk8gXOfBGGvo+8TLxWEvY6+LOw977h4AYcWyKMVImwtgCOjdArG3wjHGRSBT3oZk/vOHMkL4S3Z9xw1vH/m+OiW8Lu1VgLBxM8hup34fUleg1TNtSmmi9QC'
        b'ysWKXkMNI9tdk3R0tws9QOfG/P5qBFrTORaf0t9fibOFI7+zEv3bfmcFxOarn45B+VXMS3xHeJVNoyPKR0bvIv1Px6Pf6aZEL7gpaZJpDoHl47Hil8ZiuHjPP3RS8zex'
        b'Xfxm8vaBoVBCtiZQLboE/DYMmemutkvATIAXXJqIy9FpVLkamxOETktRGzqEzqMGOFFzKxys0M2F6IHucMAHEhrUOZyacPLd6RDUXRsV1EFIZ0NCuvQZR/+cwb3blfHu'
        b'xbC3E7gTP7FTapdF1IWXOa9Om3r7mShhKaCNJ3f2qu2XPuvVEgqZKwB1z41AK7qJ2sdEdvgqvu1CU6q4OdSLpFSD8Tncw+Mz+Q0JhbaF/utZRhXfc+aTqjSlittRFw0K'
        b'UXcKMgPkEriFGKZtNOTGoQPDxB6BD1zYHJ/8POk6GbeQvOubuEstHGWYBNMsoGe1SWukkGc5oYAXywPebtn4oPB5knJ0xvBDN1Wv7yv9bjN7HWYOOE947Ozf5+zfnNXv'
        b'PK3XZpqexL4MSyR6Av8vjQVJNJ/+PBIk0dpIm9wFfBT4173cF1tlAoHT9wCIzwlA1Eh9uRZFkOifIoDYzP0/QYCDgADtYwxodUGuzmgYMXO2kQi2rCJXs/WaTXRjcJzJ'
        b'W2BDo5r+0tTJmJsDopNTk1JWrQ1SRccsjY5fnZoYpIJa4tOik5csDVItiqblaUmpiYuXrlJ/P+um1Crbnf0otFeizQ1d8ypnmklW4X2RE/nZ7TTyI9iShJUxz2NRfESN'
        b'2qxRww74H4tKdnCoUWqNS9A9ZN6oZ+8kH0cXdKOfBqOmMO6DW8V4fyI6g0+jk7qHR6eIDBvg/kfGQWbOs8pqBKLLh9/f8F7je2obdfmqLzibbpsZNo0J2vKlH/q/F5aq'
        b'TrjUsvOk+5yGze5++y4HrUnon92g+f1mjy3uZTWJ6cvqV+D6H1b+wv9tm1Ofch9gx69W/k0tppQEVaKrLtOC1fj2c2KF7u2hdpsTi4/yVjnKIhPWytDF3GHCSxXprwOb'
        b'Qd1bn9MZ1xS6C7ICm+3iKb8KkHJydyG+iA+gFhW+oBa/1J2SwR+xj0FriBENfE5n1Dm13jRmvUMb5ZyL+4i5vphkp1a7oN9tYa/Dwu/KtsM9zT79bmG9DmEDzu51c2vm'
        b'1s7vtfH9v7LpaGLToxobMNqsE+Xfz6z1xL2Av1fBVxa+E8z8PYQpVaGolOAfqtss5Tz3iHMWr3i51WcRqxdb/D751TWfk/73Wv4mtfCTDeNz0qPdP03e5mm20vD5JV6f'
        b'BM/kZYECLVwAdjDWD8cy+8/VGI0QC2dqwIWPVUrJgCaLpb1fyAKM0TWSEfhnCQGWAPj/h43Ikkwkz4kvq9D+fzU1zLgI7sC1NDd8iQ8n2209uLCAJwKgtutfT53A8b/z'
        b'3kV2UvbzRAXkIFxO340rdJylwzUWnvKdHMU+kyr/wQIpZzMzRMyp0nP90zZzul7pHoGB/CGM2adqWTK6bQxvSbBpfK+xYLf16psuouia9Kmr3SJF0oWtCun1rtfCUwke'
        b'li/cUZTwV5fsevnCZwVo6doVH+L9/+2zJla1VmHc4/bKBZ1f6Qwb2bOCCyLO5X03o+OXaukwScOaUGXsCK1JnTSe1BxPGyZ4HVy0dFTAmBznN59sKOFKgMRECfdKknQ3'
        b'xOvHKf+BDpfupASIYSi6YB+MbuPzbM/YHBSyCp0as6vMCFCPkQachagadWegjhfBVoau7KJBrhU+hVoY/Yl7E3eObshEdESMGx02AVh9Z7hCwGpU1tyGcg9Y5sSIdo6R'
        b'KMi+wfF5c+txFIkEbnP67Sc2R7xv70+3KSP6lBGdc/qVC3odFnzso37sE9rnE9rvE16tGFBOeqwM7lMGt2Y9UkZ+6OnX6z+n33Nur8vcJ17+zVv6vSI6w/u8ZlTLqJ6Q'
        b'PmVI6/Z+JWFZowDYalBB0DQtX0+40j8Oz1jKfdTugD6RgPKY7s0eBcvPCgGWPb5vOFYrncydVYSI1KKkpGVqwTK1MGmZ7q6fWGIoh7Gbnbb20KNnq/vT3a2GXvm0WTd4'
        b'ffmi9T3PFhbaL1n64esup9LKXKam7Buc7bB1VcGaH+xTdDy8sefcfz2Y3r3tT42ffjR1x+flz2JD6+RpCWW3M3e+5/x5Uum1VYmt6HLULvXSd0RxaWUOoo7IbS1f7QhV'
        b'dv34tcjML9bY/OXr8gSx3Rb/Lq/oJ8ccJN+c0lgFyzdd2aBZmv3O7oZ3d8/L6gpsWTtjcunxPzg/+0L2u/64DxX294ZajO+6ud4XagOSA1oX+ncsntGxKLjjQNMHZ/f9'
        b'dPHkxopZxpDf9P0154yiszoEZdwRx38aEXRxWueRK2jzHekWZ+tna6f+rWN55Ed7K25ITv7uNwner3cey8NFd0RzPg3544WOiDtWW42hf+n7JueiVe8i+3e/jp6ZUPVx'
        b'zuLY7KLZh3+9vumt2J3WFz/1OHX+t72xP/u18E+LX7kfMPWhX9Oz6+Ub307dmZgkWn9RMNzr9bvzi4b7TvYc++jTqD8X7FI+y1kgzZE9+1Rk876vTX+Yz/vme5Xv/m7y'
        b'k6fhp3svurf8LCyu6deSih9/+9Pq/pMNg+eEC37ljmdu/JXrxl/b/jLp9pG49a98kV4SMHPVE8PJ3+Upz8S7Tmpf8nPzl8l5W6Meu3Uvf9S8pt7r2tI/qk2/md1e+bc/'
        b'Cf/3pM0DDWsbTIvuxxzafL/kgs/Km0/n/lKjzA7+r6/1/aF7XD9d8u7pXfl7vLSHf9FbEXj2P4akp7YvaF/7+drftk6+emfSvJp3H3wRc/1mYPOvoms8Nz39NEyXqHz8'
        b'2d1fTZ7/SeSD9MCPE/b855+GftTbs9z/4qWor0/9+fVPkgpv/XzqNx/9vrHxDz9qvZR+5ciZJ7O79rhl/2je7T9++vUvT3295j+cO3/9as3fr2j6/I6+t+2C73+/M6/7'
        b'F+1/f3bM/bqpdNHSP/xV8U2PsvVXHgB2xCxel+AKIBACFS7mBDM5XLnbdpgQC3QG1eFbYzAHnfLiE13nUTufXEP30dEXsmtrlDxWogoBBcBXAPQbcBkQwQopuhMs5aQb'
        b'hZNRZSCL3fY6oY5pccHYHJuQJMGHXDgFuibEjWhfEcU/VKwMjyeOC+7A5bES3ICuwS1Xhbh9Ljqr9v5+77DIvuvwvd+EeSnIEEQfcc0LyWfvmA9DWFlaWm6+JistbefI'
        b'GUVWNynHfQP0dZmAs3UdElvJlQRSI8q21fuWvtlgaI5o1rTMOLmzdeWJPdf8OvU9vtdMPSuvbe8KeXvJO0445v2IhA/dCdfVNMw4KW+O63MP6VT2uc/snZvUp0zqXZXS'
        b'm7qmb9Wr7ytfJdzWqTav18FvSMS5vyYYsuacXKoX1biaF38mlXpam+2GXDgnjwFH9wFHr6dWYg9rs+2QXaLA1XrAxqHXyX9IRM4/tnGoDh2SkNMhKWfrCIIVFWRMkFPB'
        b'mgkKKtiA0OsUMGRLJTsq+Q3ZU8mBL3OkkhN7zJkKLrQoeMiVSm5U8h9SUsmd3ehBBU8meFHBm79vApV8eGkilVTsRl8qTGLteDqZSn6syJ8KU2iRemgqlQL4dqipFMg3'
        b'fxqVgngpmEoh/HOhVArjy8KpFMEqiKTCdCbMoEIUf98rVJrJt3gWlWazG+dQYS4T5lFhPt+qBVRaKOCVLBJQebGAVxPN5CW8/NlSJi8T8E1dzuQYixzL5DjL8/FMThCw'
        b'uhOZmMSLyUxcwYsrmbiKF1czMYUXU5m4hhdfZeJrvLiWiet48XUmrre0awOTN/LFaUxMtzRTw+QMi5zJ5CzL41omZ1uGYROTc5gcPqRj8mZe/RYm5lpGdSuT8/jifCYW'
        b'8GIhE/W8aGCi0VK3iclFfPE2Jm7nxR1M3Glp+RtMfpMv3sXE3QJ+uvcweaGQv32RkM23kG9pNJOXWMqXMnmZ0DLfTI7h5aexTI4Tcs6TBpz8B5zU9Ohr+ef/2Vp6h1k+'
        b'tF7Iefk1hTaEfuA5rSTOHF3tOuDu/9h9Wp/7tA/cg2vE1YLq8AH3CU22DbbNmlbHfvdpNRJAGo+Qj11COl37XKLMSwcmTGxa17CuVdI/IcQcW51ZmjQk57yCABOsHZ7I'
        b'Haoz6w2t0Z1Zj+Rzngnnyac/5eDwuYiznksODkNiEMlQ0JvrJzcbOsWP5DO+EDrK3ckNUfxdIIIJKz3qNtds7vVN6XdLNSs+ltuTClY3T25d0unaaepZ89bSd/x7p614'
        b'JF/5TDhF7v6Um8K0rBLwakAmK5tv2SO557DQRh5ECr34O0AEvBl9g5180ugbQATQYc1d/Uju+xehk3wWKaN3OTwVg/jlUKZMII8VPHGaeM6mN3hZv2p5v1NMr03MV/SV'
        b'uZJF7rG+3I99nWOn8zsUDoPCtLR/dVviX/FfDs9J8lifpU8lbHnEXRHvb5jPM+VogUDg8IyDw1Ny+L6cuVEazHUoZop0AU+DRIYfwJXsD744GfiLnz766Yc/jWj0PRR+'
        b'yLe45XjLYd+yBoHoaOdbr13y8DUGZ9pmus258K7LFL/uBIcTjhmz45Xx1tGTpk09+KMPfvjhj0/9sEqHNgc0vmN9Y5FD2es9vR+hd7jpse5lr9evTDH/6ual12Q5dTPd'
        b'nF9zmFIQYQwzdRZ1mgqMsqKwbTKTuSimqNP4jvEd0zsTp158eqGzu8AYboqQRAZEHo15a/hSmEuJYNfPen9Y/lGo+rLs88keO21+4hFYP9njXY9Z/ZxveeD7XqlqW5a9'
        b'LgXWcp7+Pb9kdGw6rqIbigp0XYhbgQ4xrlWNz+BjJFK+Rm4j+4KO+B5+iHpE5AfRr1MalIG7PFAZqsJVJLBDFajKihNb2TmJfCCULKEZN3QQd+F98bGJgYlWnDR8hVgo'
        b'0/oMkw0uyewV6KhxWpyEE8RzuF7mNEx/hfcAd6PW8VkBVBkaDzyuEh0Jh0CySsQtR9esoN6Hk9irXA/34NIxz+C2QnhMyimXiAPRNVzK+rQP3bGhIWnomleoPqbMC50U'
        b'owuiOWxj4ARq3ERynvG4DHoTnIVuClDH7hzKC3P3AAMtU4MGGLSSZHA7+N46+5Wi1NfVw/7k4Sb0ENdb7ggizcblU/1wCdypwt0SDl9GbcPkt1y4BZXHTEsOwqUh6BCt'
        b'DmYAPxDiW4vRHRryR6LuJTB25UAxQ1Ezqgos5MNsT5MYHV6ArqsnfTeH/Lcwx3/jwTCJktAXuOe4zwgV1eXpjIyKsjNKRR9wdGfyc09O4jxg6/LY1qfP1ufU9n7bgL3L'
        b'BsTWxQn7Enodfc/NfCQO+oXYFuifp0+v2G1IaC1ZJ/iFzANYn0/A4wmRfRMi+yfM6JV5DsjsqhQlikcuUx7Jpg7InB7LvPpkXvWLHsl8Buw9HttP6bOf8sg+YMDGqSqp'
        b'JKnX67Wf26x9Jt0ilsx6xpHjEDuuk3M2LnuTvxwuhBPlZ5xQEjbg6mG25tX3uoR8IANKCpf5F5rFiwM5FOgdLRdhmQCODDcnDopytXmDYvICzaCEbicMinN1BuOgOEuX'
        b'Ccf8AigWGYz6QUnGDqPWMCjOyM/PHRTp8oyDkmzAQPjSa/I2wdO6vAKTcVCUmaMfFOXrswal2bpcoxaErZqCQdFOXcGgRGPI1OkGRTna7XALqLfWGXR5BqMmL1M7KKUJ'
        b'x0z6zqC2wGgYdNyanzXrlTS2UZyl26QzDioMObpsY5qWJAIHbU15mTkaXZ42K027PXNQnpZm0BrJS9eDUlOeyaDNeu4PDASB0v/RR6Vi6J5lOZC/TWlIhsO3335L3rt2'
        b'FAhyRATbxx6H6PH7ID1xYG9bSRcpubeVikWTRF/JLD8YGHRIS+PPee/ylWf22D86q8rLN6pImTYrSS0j75xn5WdCj+FEk5sLLjCLX8skiwPXrWFw9UbDNp0xZ1Cam5+p'
        b'yTUM2oxOp+oPcHwSiaWTmC3MZX/Udr6e/MyLZM7pduCQCPzbU6FYIIbwRWG71+oz6TLo8NAqa07uyK/jOFjVvUHz356CA/qC4gZkDk+s3XqVkf3W03vF059wDtXuP+c8'
        b'aVX/B3YrDcA='
    ))))
