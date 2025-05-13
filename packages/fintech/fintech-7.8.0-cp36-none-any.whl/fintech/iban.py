
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
        b'eJzNfAdcnNeV7zeVgaGpoS6NOoNoQqhasoRQAdHUUEEFBhjESIiBKWpWBaShI4EkQBSBQBK9iKKKFJ+TOHHiZB1n4yS8TbMTe9dx8pxs7GSdl+Sde78ZBALH3vf299vF'
        b'vyn67r3nnnvuKf9z7h2/Lwz7k9JrPb3Ma+gtWYgTDgtxkmRJsjRHiJPqZUfkybJsiXFuslyvyBaOKs3++6V6ZbIiW5Il0TvppdkSiZCs3Ck4H9Y6fZ7iEr4hJFpzzJhs'
        b'TdNrjCkaS6pes+2UJdWYrtlsSLfok1I1Gbqko7rDen8Xl12pBrOjb7I+xZCuN2tSrOlJFoMx3ayxGDVJqfqkoxpderImyaTXWfQaRt3s75I0w877bHrNpJea8Z9MbzbB'
        b'JrFJbTKb3KawKW1ONpXN2eZiU9tcbW42d5uHzdM2zjbeNsE20TbJ5mWbbJtim2qbZptum5Eyk69ZdXZmrpAtnJ11WnlmZrawUzgzK1uQCOdmnpu1l6TD1ymLThouvEn0'
        b'msAYkHMB7hS0LtFpKvo+oJIK9GxlknNC5GyLSrAuYL39sBQLMC8mcjvmYlGMFovCY7f5KYVFm+S74B4+xwdYYQ2instPR1PHYixZTL2xOCwKi3fTkIKA7WG+EViI3X5Y'
        b'GB6J+eEK4TiUOB/wCuWzVpxUCq6C4H1EmxB5adwewXqAHs7C6kTscXbbHkYkC8Njw6DdG3N9t0bh1Z2qOCjEvLBYoj1yMu+wSCyOjoyJ9aaG3ABidHvY1lhvv7BwXwm0'
        b'yAUL5E1aPi42SWIXhoxe7g5hbP6S3Uhxt8tbkisleUtJ3hIubymXt+Sc1C7v1OHydqbXzlHyrhDl/R/rnNjKPQOVZ1b8WD9T4A83avkmCIGbZwcGLg0SH8496yx40rPA'
        b'5cmLfzfRVXx4/YxcoE9NoDJZ1zROLaS50MM7UVPlfxwvrP9kXuDCP0j7l7yZ8L6Qxrh450ylpMtJ0HQdfy3oX4JurdwqPs6d+QePax4Sb83430j+tveT04+FQcHqSw1e'
        b'8WtJ9LR53t6YHxDmh/nQvMubNqDE1z/cb2uUREhfn+zhvBYbodrKVCoGcjaZXUm2WAEtHgLcgEa4aJ1MLVjpjrlmk4K+FWAfPhcgF+vgptWLtXWexT6zyYm+FUE2VAuQ'
        b'fxR6OUF36JeYsZ91uoI59AUKx6VamSTn+2OVGYpJTFg/ZZkANZs9rBPp+Tm1hB6TjuNtNoEAtXotb4D6RDdzJmOgxMqe50Pba+L017EQcszYreTf27QCXFm1yDqFNVXB'
        b'HRgwW9moq1gOdwQogE4o4xzsV0Oe2Y0NuoWVcwWoPKu3TmWDnmEtdJixh/FWjtfwBhHESnzIZ4NrkI3lZihkPatjwwW4Cd0hIofVZrxnVjPe66BPTRR3jOMzwe1YKDaf'
        b'IF3FG5YVAhQHz+LSOU8iyTF7MEp12Iz3BaiI04mz3IN2bMUeN8ZDO9x+TYBbPis5saNYrFLzjWjFctqjCp2LOEnfdqyEAto9icrLX4COcwF8Erc9K814n+1p6Xx4LEAJ'
        b'duEN3hKGra9ij5WxdXsRNtDSsHmnuNt9W+CCGrvYLJ3YJKVdgGeYJ7J2dT1Umk+wVZbC9XTaCOzF55wgVpzETjM+YExXvgJ11PfwfnGPyqEk0uzBt5WE2UFSw55Mzveu'
        b'/dCMPSrW1BjnKUDV4bmc2FzInUfPGQv3oA6LiYeNJ3jLScjZgj0W1lIJ+Qpa0nS4ylugIXYm9riyPb13Fp+QVkHPMpGBQqjeQE1MDk3T8SFRmwIt4mILIN+IPdjN2G4w'
        b'YDvpfSKWi8PyYq3kw9ioDhMQ2/VYhc9EOfRifjy1cRnNDKFNxvskIrak5ZMOUQOTa9cCCTG1Fm/x52vjyNn2WLnKTd9M0kmO5KQi8Q6U02azabqwdzajdSVIZK571jri'
        b'rYc1tUANknFVRUEH1+6FOECumxqduJLUhrNtqkAbF8V4vB1FO8g5VwFtbs18bBcZf2aBWrWKtfTjU7wrkI20nOAUoZG255oa7zOKffiMrfj2FGgSZXFtP5arj7P1tmPd'
        b'IlJvrMFurvkhwalq7Gfy617PdqoGy+L4itOg04da2Ip7ViwkJY61K+s9vzB6zmj1nXAjsbpv54QOknabLYy1XGzAXgEu77Hy5RyBi9PUzPtiJ1nGBVJ7qN5rncbY6t1K'
        b'Jl2wHK9AH1zYAoUKQYa3JTFT1Lw5BfqnQMFxvAZF2AQ2pi/yVAlcfDXNqmGjy6ATs7HA3d4niJMhGs5QJJ2854BWxvnCu5B9/hxmYQHtqlEw4hNotpI3FxIk+ORVLI0g'
        b'zhKFxFl+1nGsdwnWwI01+yOULFgkT462LmJPe7B2AZZhLrQuh2aFLoo4ajwSCg1xRiiIEoLNCrgOjzZavRnZjeR37F07yKld41+DoRWvy4UZWISXpXLnbVBsXcwQCdaT'
        b'9+C9oR+aWPcw6BjqDQOkdQ1yGbRDodWH2/1NrHBQbx9GvU2kXupGtqAkTbhu1XKlgI5JWBYGbcT2UO8gNhH19sOq/TJ8CG3wyLqQer/m7GEnHeUJHXyV8PSIWkNW1rR7'
        b'grBV46TGtkNWf0a4ButesXfGionDFkp7UsQ+WtgUfiZFpoaMjg1RyOcOcVKENrwqSxQngAZaVOMRKIiLovU9VGJfMBndXBoiDwhgQyqwb2gBTDryHcJ07JFh1wSzdSV1'
        b'23II84fJsOhl2TRFseFtUcrEKCHzZCB0quAR3IdaztZeihNtJ2l4GSPtkJIMSjEPr8PlFFKpm8ISvKWAYrxr4lKdCwXE//BNEPesRdyzssTDMnwKxRSrmD4QYksdSx+a'
        b'xR2z0QZclzvtOWb1Y3K9eGT5i85FL03AlSIYBjxeU0Cl015rIFPNR+p5Q5r5Yhda+eBgcaeDYuABliigzgeKuBrFkXdtGKl2DlmJXLWTtyyTq+KWWAN4fJow2z5HCHS9'
        b'mIbGtolMcvXzIws1n4anHMDMmedgC+tlTDR4jbzmKSZTuKyB26RQUTjgFEQGYBNV6ko6PBxpY6QcmB3nvVzkykw0nsEtFWHZtpOcL3ygZ3zyIfMmM/G8pIR2tm4ozOSU'
        b'mvjSg+fgpaG9G7LkUA15E6bkMZgzH2ud/PdQFOFTVBPHDXbFrTnKdFcU7wsRcOb84YniyLJ1fMehlby5fUjLKA+w6DTckuGTMMzhyoQXloFtuImKW93O+k7HfgrRFTLs'
        b'DsYHIjt12LjiJQVpfllBgvFOpoKspjCNs3MWehKGazf75nABMuxgltRJ+nBP9BitS+CqY4LO0YrR4Ay35U5QPtm6jHqvUVP6MQY3/Ikc7rtGhWykpdxTLRRMeF1FDrqJ'
        b'wg7La7afIaN3jHRsdqhGQepdhz20M3BrhobrRewrni/8xstGxE1uKVwMwioFlMaTl2Q2MXMxBdchm3C4I/sgGbHldmSZZLvCiaSZtxKzjoimV+qMLRHcU1DfXMiaO1JF'
        b'yNlHCTugyGlOAt7mgpUqlPiYfNkQd9yj8b7Mly2FPuY0yubxzhOgT3QybSO2oUXc5+7DJ2gXsAv6rfOZXKH5NFuAFLKGVmz3fDMgi7RnI3RyqsGYlTjC+odvLoXMu9An'
        b'w8cBS63zmPLcgpp9xALmJY3gQsr86QPSsqR5PNrtgab5ozWyQ+S06zz0MoWpW8IZUOA9yvZE7WpxdIZeh3q5wlUZ9oaQrw3iIiaAXjiWM+wYFjSWBJ3EmwrCQ43YxrcT'
        b'ahKxYcQokaOm4YMI2jfvUcAVuCjjdr5oHj4ZaedMwYbsfJsHtEY6rYIcB2uPCTSM1LP2l5ezFC9SjvRcASXkdQpE1m5nzhwxSppkn4mUFh4uH0e5Vm/UMglUrXeJxtZd'
        b'oo3VTIRLo6Kyw8S0pLt1MnzwKjSKelmRPmRkqqmjfbzdyVkVGZC/UkQrl+dC9+gNbBU38BFUr5Ph/SgnLibirz5lzEhgxyvPD6yTuxP+6BNJ5xASGxitxm0i7Y7pOvIo'
        b'Z7aJnq0USgNGOfRhWwCPYnydVshP83iB9dClcfQerUnkI69ipYxk004J71IxLbhGmc2YwoeeOLLLnCOUE0BJnGA6ShEfaw1inKmikJ6VMHssNWxVjLfH+zaKlpALOeIu'
        b'N8DtZY5oRhnNC3TxAnCIeAfKFJZxWu6qN8CdvWPH/WFa65aI9eTqoHAHFwJc2zPzhQyKks+OshNF5jLJNpXT8oAdXMbj9mDzbpdRWATaFIkkgyghaLICCmnCR3yzCdLc'
        b'nevo3DpMxiJ6JExUil1yOeRP48Tjoih1HmMF7aJm5G/BSrmKnt7nqrFvGbnT0UotqtEr+6FLhgMHMZfLZolMORqzvGzQreuxTAHV2LxQGymmiNnQsd2eYjhhFmUYcwko'
        b'shbTIew386wyj2y0TCDPV3dIzJgaIX+BGXvZoCvBr1ACT1z2W8dTU+JZaLFXTCbvpMQxcwtP2+ACXoJrZihkaW0t5PkKUK2GcpGDZ35bzSaWyticWCKaQ/65VMyf6/DZ'
        b'PEeRpYBhnVyvBbxlHFRDkb3EsvEIy7kfwDXOWxjW4j1K8NnwYsgeL0DBUrzOeVtzZLHZRcqLOU92C3B91zY+QrsRO8yQL+eFj+fQR6xtxxrOdhDewdyhek3VIYH2vdKe'
        b'7+7GgQVmd0buJmU/A7RWijTVPJszbw9zlHJgYD+5pgNz+ZCD0O3vKOaswDoGaErhAR/ilDTFXsyh2Vkxp2ajKOrnZHxXHcWcAEqSr2ghW8w/H8OFcdTChFBJYP0qaXrc'
        b'MS6elZDjb6/yzMB7JAIKqfm8xUIW32iv8uyAckpavbBL3IbO9XDRUeVZzbL+KwlasWpUiVeTzGJaXUMuoJettQZbeCY4Dspesdd4CNTdJ4KJezh7sdTzhqMu0gHtbFE2'
        b'FR8zMWSR+QTj7jq0TBZogQ/I8zMeJu8NcZRLsArqCdtikY7LR+VCS33A9Ko6RsKKTjVhohAGfLHTXkjBwnms+tRLG8Rm8TVgr9mDDWmE1ija1VfxsijTW5Sq1zlqLHtO'
        b'k/fCS2li0xWSzz1HmcWNKUPtYZOowtWUxNY56iwz4ZZAIevpVnGYbTIBjR7RIuo8/VmlsHeKOOweGeUN7HFlq7ozzYW5ymeUqHqJ8bFtpaM+k4KNpClbQWQ+fZGPozqT'
        b'lsoUpckuovFLVTQRL0jcgT4VW/DTo3wmZ4rtA9jj7sSLVHkzmIctI1TFZlpDLFwnCMh17751jwB3sTSYEzyD/a9hT6aUw/L+46wgViVu09Ht5MN6Mhl3NeO3kmxcCF7b'
        b'q1fFs4cqRGecaLmvkP1zk+07sMxRIDqyTYB6KMdLvGU2Pj/hKA+dYHWb21Am7qE7TVztKBDhrRXEOHZF2D3Nfsx2lIiCsJM0Qkn6ygV79wTcoiYu8nSoZEAoF5rFYW34'
        b'CHupkc1WH79AgDKlvckfqtcT631c5ixrIY318xKX1RHJ1MKNiaIjDQsECkqPvLj6JR4LctSj1rOG2/NfEYdUwIXT1MLm6YanTP8bjAqxbNoI/YwHe62KnOgtpmiPNGId'
        b'q3A1m8teq/Ln2U061HNJ+a3DNjV2MQ7bJ0MxaZ4SRYXZBrcNjiIWPGXiqMF708Ql96vQplYpeaGqiZlv40LKb5jfS1+3z17e2jdHgDvYOZ6vCS/vmKK2cLX0QrK1spmi'
        b'84g9A82OkleqO9unazDAR0Ri7S61C5viUQAred91WyFu+qV9WKs+zkg1YxaQn76+f50onzs+kerjbEQr6SI593JshlaxhGQzpdmrZ0sxj3YBSk+KKynCmlOO8plsFSta'
        b'1hOg5FWv01DqKJ9pKIbcokzLXo+/B3fcHBU0aINmgbmPJ5zt45l+ane2/qfYQwJoWovtnAODOV7tzpTuGVwxCxQhG+AyH2Dci3lq7OYiM5Ix13sHiCxX4bM4amBjHobH'
        b'0V6Pmys2tHvjfbUzU5ynUKQho48LEkvgRW4L1FaxaF27iZYPuf6iyLLhcqqjgJevJUCagCV2p7AH8tRmseJYgi2kGBL79iskC8iVc8UYwDasZPXJO+etwdR0eDqUSU5Q'
        b'axnk8sIdedt2O+aDXF4MlEPPLiiIFfYcVFKgK4QbWrlYEdxIxlIQuZUeNWGJTJDhM4LWpNnX+BK2QtmqCMyP3KdWCtJDkgDyKl1cwfco3KHNGIHFAVi0WMsOo1w9ZZPw'
        b'4WtiOKnF7ojF0X5hKzfIBfl6CbGSK9ucxI6B2B+tQWBnOzxcslNPm8DPp9hZFTujktmcU5ztp1PyXHm2cFZxWnlGzk+nFPx0Sn5OsVdIlu0UnHO08l9+QrJ30Qz7C2Xn'
        b'lmaNLp0fWGpSjCbNcV2aIdlgOeU/ouOIf4SLx6U+R43pFiM/+vRxHJZqDETtuM6QpktM0/tyglv0pmP2Ccxs3AhSibr0o5okY7KeH54yqpye2XrMcSirS0oyWtMtmnTr'
        b'sUS9SaMz2bvokzU68whaJ/Rpaf4uIx6tztCZdMc0BppmtWZXqnguyw5sE4eo+I81INGQtJot87DhuD7dVxzFGNwQHjqCA0P6qBWxvyQSjP6khS1Br0tK1Ripk2nMifja'
        b'TKeGT2ZxsEmi/OrzWNgRtZ2avybKarawNTK574zxW7pk+XJNSOS2sBBN0BhEkvVj8mbWZ+g4Yz7sm49GT6ph1Vn0/MQ7IWGXyapPSBjB72jadv5FiXPVsq9Fs9OQfjhN'
        b'r9lkNRk123SnjunTLWZNiEmve4kXk95iNaWbVw/NqDGmDympLz3drEsz88dMyCcM5pcWM+IEfIrw8omsJnqz6Oez98AzO7hcFEAwLHwFP2v9IGOqEMgOYKPzwuaGawXx'
        b'IOJ5wkkL9EABSz6EfRTpc3nnSVFqgbyBKlC5f+OltGDxtNbk5y7MoKkDN0+e8u7unYLov8rgWrjj1O/uUXYsUkiBiLmS5RSgH9rP/bCP3GGxq3iawc6tsM9+8ifHHHKH'
        b'08/wFg+sG+c49tvJnOGtaDuSxWroS3Yc/N1gHhRLVfaWyXhZncGmaTIDwd/y81gmnufq4Io6U8QZbWCjeOyKRZy1/TtD7GeF8CxQoMysHUtFmHEZLm/AHjNzuvUUKSoY'
        b'znjgK/q4VqzY5jhM1EEuYacTIhaD61ALFx2HiVC+lyDrFKwX4TShXeh2nCZCwzx2TNVhPzmi8Hx1lpqLqB/7xlHT2Z1iJL2yA7Kwh6+3igiUEB47tFqMPl3hk80nWMAo'
        b'x6dniAl3Siq4IPKOY7YdglMYILiQv1nCW1IoX3joAPvnWCpyxWDgnM+By5Ty2I9zoZMFmZv74Qrf7zyD/XA/JUnoC0wWNebgCXy8NFDON558vJCoflXrIWpCDSX7dY7k'
        b'ICuexfiKBeJqCiZAo0MTSgykCXAJqkTx9BA2vWfXBcLRtexs6wIhEDbOG/vUDnUgMfQzCNA4XSR5CevO2fXBm53eVlC0vS8ycgEerLYrBJG/zeJw6Q7O/THMn2/XCKiX'
        b'kkLM3ifaQZ5yvEMhbu4ghTgbzWV9JFMzpAxlJCUodV0rzlE+i1CEXRcgx4u2YRnc5GM2HaAtt6vCyV0sebkdKu5PI7acdCjCSQIatVLM5i2zrPDArgUkjRoWTdtWikCn'
        b'CLPIoOyKAB2UHFyZYD/jxOZpkGvXhHjGAaGuHvuJHdSHTXGowmWWYS6n9Js1LCBocslBL+EEkfOcJAq0xgPy7dSgN5yRewg2rVTcpVtky5UODYLaZBoHj+CCPTONhuwh'
        b'HXoQTSq0COsMn+3+WGpmIFr5tf6oK69vlS9xvVx2t2bf2txFtu9/f9EnH0/I3RJgfvsHs258DSbe6Fvr/EQzcc5rVTbPWxvOeM5+/V6gW9Y7EZ+fNfxt2+9Pvb4y68/O'
        b'LjOerj89rmva/MbrpuQ9ge21nfMjo8+EfPr1rz97GPZvHc/OXbjX/qO/vfnN93s3Nt37w5YfV+d+pp5U/uBG6L4Pzb/44IefZmjqp5btiJgfcXTZbw/mBiRW/eyjqu+2'
        b'/37pr2992+nXs9/oLDqhOBwWf8Q/qfWHDx794KPgPQeXz21f6Lbhfu7ufT/6JOLyX9bK/mRt+PtnJe+u/UbloyXv55yu2PDXorUfJ7xxxrgm9Zs7/l7f/MZCubIq4uDA'
        b'pzM+as9eu7UHs87M+qnKdd6M9vPC411Ji35+SutkYQI9TMD4wmI/7zA/qaCEm2ugXOpHWXuXZQZXlPmei/3DfX20hPvz/LHElxCzMEUjP+Qx28KTjaZpZyJSDTF+kBdD'
        b'WE0pqLdLsRjy9/PW49h5it138vHzlxDxrGhsly6FZnxmYRWpQ9SxYRdZU4/97tEJ8e7RcT8fzA+QUsY0oMBeGbZapnE9J8N6ggVRvuFYTFsZfBTzpe7YjXcsvBx+H2o2'
        b'RogEoDgR2rGEIUuZMAlz2LGoDUu00kGpt5YVfAStM//4qm/NwueT1qSYjKf16ZoU8SqbPwNArw668HAcz/7BgqF5LwuL5wWtXCKXqPjLXSKVeNGnJ71cJOy5q0TJv0vp'
        b'U0mfKnp3pU/2Lqd+SskU3ov1dqd/yVkv6QwJqzoJ0cxeBK1yUM7mHJQRrBp0soOUQTlDFYNO8fEma3p8/KA6Pj4pTa9Lt2bEx2uV/3iJWrmJXWEyMWxs4jGW3aszMbjM'
        b'573BVscO2oULwsczpErGPX/nZ7vkb3uPDkl/mOil2MKkfyeTvAFXqH5KVou84H4E9cCCaCyOCVcI7hmylWlLeVJwAClPXOUaERkt4nuJoI6TYoczdPOUcnNGKssJFqwV'
        b'c4IgaEiS2cGIYjiyDxKGbqDJU+R2PC/LlRGelxOel3E8L+d4XnZOPgzP/1jyMp7ntw+HAXqT8ZhG54DgI8H2SGD9EnDe9Q/wvUmfaTWYRFSXoTcRxj8mwk/HlciRACzG'
        b'gcuIEZ8dNKPhmH6TyWQ0+XBiOmpJHhu2M34ZuyJ0f3kRY2JW+6LEES+vcKwpGNDfnKY7rDGI6UaS0WTSmzOM6cmETzneN6carWnJDL+KUJQnHvZkY2ykusnAlvwCGFMS'
        b'pNME+VmsGQR47fCXS41wuzfr4csm0v4D3CofhVsV0VaWEOLdSTvGunuZF+mz1RdadonXMNmDmMjwKAmBMUqbPaGHktXuXYaob3lIzWuJTKMq7DcJ/h9odWG6tJS0xI8T'
        b'vkevjxPCVn1bdySlWNeib9J/nODzTouuSReZ5JLSpFOl/CJNIsz5rfrYnPe0UgszqyNTT6p9sGgNXiNWsDDKaveMs6FHTgiuFootGmZ9zw7A1Qj/rVG+kA0l4VDkMMBp'
        b'0CtPP2LRSkfY+VguQOEw9kG1eN32hUtzF11aMnNm47lLM3m8cESKQZVDpwad7NohehJX9ubG+gyfXmZiF3NMzJOI3biHYQR/NMzDtI4f7mHYTd/N2KCI8D+6lhb58gKx'
        b'BDus66jPDGiGe6NKEc14HXLgPhRCHQWx676ygxHBUJwJ7XAXBlyERHbNpoagRCHHX9NM4erj7li1ghAY3iBIt8wg3tGDPKxSH89cgYWsJZcAxrKDIjDqh2dQZcZ+jyDI'
        b'PyUXpFgq8UoXb8idhjroNgeZsJV0TmIU4AHhNvv1xYxY9fHjeBufKIneJQFvwuNd5CV54wPMT2J+To1N9uJHK9zg/hGaCEFnTTnzcvljjZvITDONfbyYnCfUY4VEkEKx'
        b'JDTVY2wnuZo5SRl3k+IVXalNlaIacpbyf+gsD5Oz/OsXFT+4lY8sfXyhq2BuhXX/8hLCF2T2bPB/e2KflMbZMusto1P5lxhkcjEmJVnJK6YnjWbUkcxv2haiCaXwbWJe'
        b'cyNFhySL0UTpeYY1Mc1gTiVCiad4T7sXD6V036RLG0VvA5mn/zDedGxTrPyGvs/O0F0+vvSxcSP7CI3ZsYQ+iT2fDUEbeENoqI/vKIrD1qRLMxvHLEmwRXI5Z4iFCKKa'
        b'zBz4qYyXBMj+vlJoHKJozBgdEdnfV4uKIzbvv6wSwq7Bq0dFlPHRm60sFlB++pRg0ZcElSi4NiqurIoVr7cf2OOomRROXuG6VCyDeFjGC+yCSaD7pS0x6xYK/CLkGiw5'
        b'HrjQUUcRUrlbmAt3tkEBobRcCn4TWGVd4gxX3TiVH2R4iMWU3ROSk5NeEzjOgsadlDr3QTs7nF8iLFGv4cQDZi9LxLqltMAgIWgO9nICDeHjBApDKwMX/kTzb2ETxeyc'
        b'krsGLPE/zQ8atrEbGuXilfxFLmI9Z3nmpu9MfVXYRXkd718AXXAtHsvsE2J3ipVFhQgo3Xok3D7jbiv15uzVQv+qeLxh7xyK4iXQdC8vicExI9hOGxq8fiqYu6nlL5m+'
        b'C4qXuEOg66bfzo+q89Hr/u2NfQ83OE15Za9r3j+/rgvJuqR680DdNxN+oVk7IXxxwP/+e6fx7OsP53wc8nZolkf+r0Mi1/zsyi6Y/LP9Sw45LzwDU9/IvljlvuyW57ev'
        b'f6DYWDCpfKKHxyeb2zrHzy/EP0x+6vfblf4tPpGrvWvlb1rW//DbP7sa9WMh5jfTTKuOZhf9/C3rB2e7/s/+oG+YP5tmOltt/KE+9rjTd81vpv4IP/vcac4fl9Yqf6xV'
        b'WVgA2UdhvteenZ2dTvmZ1G/nFgvbdHw8nfSD0IEIDQhkl4+EBzgQbWEXQX2gHwp4RMiLoTytKwXyAqibHxsW4USSrlOGx7tY2E9pIA8K/dQRWKgI0Q6BjUlgk6uwdKGF'
        b'bdNUfHI+IsaPAsvxGVAvCYGKAJ5FToKGNSzTC4ghRhOgTXlO6gOd8MgiHsK74M2hzA3z9iiDpe6bAniKuHF5cAQWRWhZbrlkP8suPQJlh6E0QisRAYPqK2dqLzCMs5iV'
        b'UXjhCCZQRDDnCfTZ0zL2LqXkyp0nYO4SuZQlW/PpNcX+Mk0YhnFepEaDMvL0w6DNl2VVsmFZ1cQhuMNo/24Y3Lk2bTjcYZAOS/ZNH8qnWGaNWXKlMA5tMiikjLlCK+FH'
        b'Ia/B1WniEQo+gYKhI5SqzBG/yxkK+OzGDIV7aYp06Pc3ki/8/Y09I/r8eyM83g7RY34BsE/huJzH5uGHFP/dmdCYLpv9SUe5bGW09RX6PltiHtNd47UJ/ygNWIVN4hE2'
        b'3FyBt82Z6ybx6rcA+TOghd8R94ySkv1gfhQW7sTcSOn4TQRaL8EdqKQvp+GpVtjm6UQW+xieG6RZ7yk4SLsR/p3fJPhSLnHvL45s4luJaSn/miy8E6mN/G7hN44seEv7'
        b'VsLUN3xvuF9OeSNB+T0vYc0i10X1B7QKnkikLd/7wlWIhp2ANUOeghAl9zbjVx54UQkywHOpnxNUcs+AD+ZD3WJ/vLScFYOGF4JCsNrCADqRLoImdQRcPY6FL3kPKzZa'
        b'pnMqp7dFvKgVbccWsVzUBnWipUnHNGenw3rLkDF7Oox5DjNiFa+fmLxeGKtMrF6MnX1IxEZuhGzMFDIT83jRCC8IH7kPN0OGtndh+wRsgYGIlwpcshX/wMCkNuErG1gq'
        b'GVjLCP3cmZFmsJiHrEg8BiJT0bCnKSbdYX6s85JFOaxSpwkeMyce0dk7NCY2eteOfb6a0LBNoRE7Y6MoWQ6JjogPjdm4yVcTEsrb46NjozZs2qH94gxaNobx8BgfnWAv'
        b'15tSff8Uu0Xg9/phABtk7AeIi9nvF/Mit4e9yGCwVAvNLhqshMpTLlAZDnmnBKhRukDumXj+YwZ4indXvBgMjzGL/YRSTAJnYZMcbuPVRYbgDXfl5m3U/0rZlt8kvJWY'
        b'SibycUIkS8H1pclN+ibdvyZ8KyVgh1YXSUk4mZGQHxaUvMQauHzpu0HvBnr9L0k16CtCgpYV7nvru66vu1YbhNQ6z/tCnlZu4XlZdtwSZiDYGiDaiNQPuuO4+kN/PF5h'
        b'oVMrxYqXYmc+lvA4iM9WR4th8MZGsYYpdccys2gaNrgK1eyHRBE8OnsrBecpUqifgU9HaPDYFuJCWYh5WM4+0WEkS1QSV24m7mLmPuX/wVDYGO8RhjLoPipeNeuxcnGY'
        b'r0/0i+TcC54YsU0+CZ5jPcWrOQK/WWALpYB1Cq6xY/8CLAmAfNGupp2Xp7rFjW1W9moe/zXpUDXvy0wrhRLUgy9X84aHL172Stcd46nQGFGLJULsLDVDTw8ouo2MI+Gi'
        b'gaXpLBbKa5J0FIJGEuXBTJcsFgxHZXQjaA1ld1+W3InJ3P/EaCoZM5qqonn+g7VkFF+tpgaPPYbHU3iymLuUtQco/zkpkwkJCQfC5RJBPHayYSsWmDPxgsERZgVXfjfW'
        b'itcXf3GY9Q6zR9l92MWp/9KZHFbYPzkJmgTXhcskguHmO94S8242RdrnPPK+c3uojvdRQmpKpO7bKb47PiIXI/991tTVU+5X3Jy6OiTY7GJemtQd5Rzhot67duneta3z'
        b'Q/1k29Yeddt71iWUYK1SeDZh4oOVm7RKHpVD5mDnUFieRMy+BODLk/k5CZSRLNpfIPi8GF47x2LyNlEw8IpCWBGtPAe9QaKPurl6Ag/iUOZv91F48RXLLLaYfGiETvE8'
        b'RwzhmKsWozi07BczgHZo1nM3ZmdmKnTa3VjAKgs34d41O8RwuHVcxAs+FMR0qRxrNEYHcP+yQqMrj+qkz8xauNfycnitTcxXuUpcpGJ4d5WYpg3zW4Nq5ufijSaGCYb5'
        b'rzEnJG6mD3kyRmX1CE/2rRGFRpZX7QqOjRgl5H684FggDsCAVhYdvVkr2ayVRm82/OzJbLn5T0RVIX0r9qph54QQz8uHU1bM+aXyKu5/GvDUeK3pZMPtJmdp/udTgr1d'
        b'Nip++mnC93+6qeFkbNb4/7gY/4vO3hXh2+MOLv3hXw/9tf7D936AIVbPfw8+/c8339q49m7Um2mTPrz8TuFMXUjo7r+p/ql108G28HHG7bsa50ZaGt79esahsk/+WBjd'
        b'2r27/bbLtH+/3HhvXm98UWzKt511hVtbmu5ejvuo6d7FzTfe/vqOm4b668tvdFdPakue1LoP4wb3ffP08q6rUWkp6v0/eeP48bdfjz7eXbX2Y/3sv6z62utXi9/+wNO2'
        b'Cr6v+E6sxVT4vuXqe/JFqzatuLcK930vs1Z9oHFLRcSBD/ItAwd+Pe3sOwc/VK4I/051/a39roHf8nzwCLtOPml8svij1/7FadYVfY5tzdxvepecmhuw6K0pMafeeJg2'
        b'1dP3G/KyX536nvpQ0Df+uCEm9e5pWVnPmh+2X37sVNRKwvhdU9A7vrm/Hix+8yfFv/5xbeZ3n876e9nup6bIHlPUtvKCVZs7kmf8tDnnLzW7Q45dUX1UcP1X1tc/sMX/'
        b'8ujP/xx7rsh4+P2HTyv9Dn2jyO9I2VO/vf9noj723U+K/6TftGbwa4X3Qj8teTfphseZr5f3rj/z/MyC7239ybbf/kjtFbTnD7bHv3pvZ0h5z7qdFVETexb/7f3CjPg/'
        b'x723ofWt75afKT2qP/bs9wMfR9V9vsv0q4D0Y9//iXwpGTNzRt7Qu54im0SQrKSc/YlAzq5Gy21q+upXhlsUNycoweeEDHoPW9jvp+BCFJS/DNCxA/OHSv0d0C+etz5I'
        b'oaEFBCGKKBF87KcUlIek86A3kJ+RroPGDafwxuKtfpgbHhmtENTQLcWa85AjnhMUQw48gutwPYK5YuqEheGsU6cUW8gj/ydPRbXu/6nuX0xHYWLmP+Yb9xSq+Pg0oy45'
        b'Pp57ifeY7c6TSqWSYImGH6aOl6rkXhLxP5VCSpYsvv/P+08lHS9h/6kkE2Ws/jBjnZRWMHGCC61mimSGt1QyzYNe46QS0wyHtySHJ42PH+bn3P7/JS4xzRxyimwidoIu'
        b'HvT8fOFwh8iixiILPoUC0roSlupCHpQ4wYC74D5VNhMuTDbsDPpAYi6nfmv+8jW/gicusH7ixg/Tl8fMc/HKSn1/8p8DvN7Y8TB3Y3i9IacxTnf//G87vhW89MNAn3yn'
        b'za6pd1ZEb57aGPXPOenyae2fbs4M/3nVwU+N+kPR//qZ19lznbVFms2/fL/z7a/n/aLwd28nlPZbfjn51K3Ns8LufPbzFPdO7cO488UJG75TqHYpP5AZhW4P/uXghzcN'
        b'f9OuWThj+8+eLdi0aF1CtNaNx77Z8AwvsgpVdERMDC2Flb7UcF+KTfAAbnPrMW+YwzBD9zg9LTSGFbLG4VMZ1Kds5WashCsUHbkgeEwoIkF4qgX38bJZ5xbx0JuBF10j'
        b'wqN8opwEpdwId6UqqLBn1hPguXnxVgXUQJUgiWDXt5uh0cJ+ERa9Z1SlAYoDIsgFFFMAKpFRZtMibIFuJygxZvBU4xhlCXfEMbLwF6OUwuSNch93C4cWeA174Dr2YCFZ'
        b'eYBPJmSdszufaVY5XM6A5zzrSINsaGB5VQQWOAlyPwn9+yr7fRi2i7cqykLwIQ+HxBHBh2sOroTpUCWHu1ASy++JbIBK8lwFWuooqolktlHw2C6LhSubOaFxVmx3tPuy'
        b'9fEcUIKN6YIG+xQClodxhhRroXRxDOak+lLWVCDuEj6T4oNFB0fkJzP/a1zPf+Eb5VNf4LsM6QaL3XexXFZwY6iGsjKZXMKsn2VmnhzpMKzjIpvPEFCAadaQ/c8elKXp'
        b'0wfl7OxkUMHT+0E5ZQmWQXmyIYneKUNJH5SZLaZBReIpi948KE80GtMGZYZ0y6AihVwnfZh06YdptCE9w2oZlCWlmgZlRlPyoDLFkEb5y6DsmC5jUHbakDGo0JmTDIZB'
        b'War+JHUh8i4GsyHdbNGlJ+kHlTw/SeInvfoMi3lw3DFj8qoV8WK9Ndlw2GAZVJtTDSmWeD3LGwbdKM9I1RnS9cnx+pNJg87x8WbKwDLi4weV1nQrpRMv/Jq42JkmVvAy'
        b'LWdvS9gb+zWaicnNxH5TZ2LKZGJlFhODxiaWGZpYXc3Efr9qYjfSTcxGTMwITOzXaaYV7I0dFJgYvDMxmzOxnzubWKJgYqUJE4vBJgZuTRr2toq9sSqgKXDIS7LtcBny'
        b'kn/eOMxL8rbPVY6LQYOe8fH27/aw9fm0lJH//ytNutGiYW365Gitil3YSTYmkUzoiy4tjZz9LLvqMGhMz11I/CaL+YTBkjqoTDMm6dLMg67D8zPTWocAh72J+rdG/J9s'
        b'vcoe8eKZXCqXqZiORUxkEUnyfwHPS5YW'
    ))))
