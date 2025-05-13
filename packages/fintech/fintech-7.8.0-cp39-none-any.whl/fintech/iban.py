
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
        b'eJzNfAdc1Nm1/28qAyNNUbGPnaFJs3cRBWn2rjDAALNSp2DbtYAySBcUKQJiQUFQEUSs7J6T7NvdbP4pm0+ejyQvyaZstvyz2Ww2eS+b8s69v5mhqLvJ//8+n/f0wzDO'
        b'vffce88953u+59zf+AthxB8Z/ayiH9MyekkRdgtpwm5JiiRFekrYLdXLLslTZC0S46wUuV5RIOQJpsA9Ur0yRVEgyZfonfTSAolESFFuEZzTtU5/TnWJWrM6TpOZnWLJ'
        b'0GuyUzXmdL1m42FzenaWZp0hy6xPTtfk6JIP6NL0gS4uW9MNJnvfFH2qIUtv0qRaspLNhuwsk8acrUlO1ycf0OiyUjTJRr3OrNcw6aZAl+TJQ9Y/jX6m0I+a7SGHXqyC'
        b'VWKVWmVWuVVhVVqdrCqrs9XFqraOsrpa3azuVg+rp3W0dYzVyzrWOs463uptnWCdaJ1knZw6he9b9dqUIqFAeG3qkdGvTikQdgivTi0QJMKxKcembhnyPoi0Rfs+pZXF'
        b'JQ9VqJR+XOlnDFuQnCt1i6B1ictQ0fsjAVJBLnhblEKiv8/uNYJlNn04Ga1wFUugAO7imfiYTViEZfFaLIvatjFAKcyNkGP/hCzLAurphE/xJJZgOVb4UVcsj4zF8u3U'
        b'v2Tepkj/aCzF0ihohZ4YLI5SCHlQ4bx3F5bxmTukSmGUUDtNoUmM+cPO+YJlH32Il1UksdvZdVMkSS2N2hYJnT5Y5L8hFs9uUeGZyG0ke/hkPpExWB4XE7/NhxqK5in2'
        b'0To3RW7Y5hMQGeUvgXa5YIYzYxcE491kyQgzc7NrZfPXHFOqm+0gJEVSOggpHYSEH4SUK19yTLplyPuXHYQz/cQ+dxAZ4kH0qJ1IHYLwH4GJGWuWJAj8w/Pz2OkIQb6q'
        b'RP++cevFD41rVIKHIHi8mZ7o/5+R0eKHbXMUAv2O/FVcYsy9Da8JbUKGC31c6zpB/ofRwiqN+8/n/l7aG/wr3SIhg63DvKxOcsdJ0ARpPf1+bBylU4ofN2/53P2cu8Tn'
        b'dxs3Tfibd8Mro4UBwRJEDXAbKzzpSOhcfXyweF5kABZD21YfOpgK/8CogA2xEiELe6HT3Xk5NuF1baDFi4alYTdWmUaR4rFW8AuBmn143sL2j+2HVCajgt6UCK5wD4qm'
        b'B1rGsXlOQs9kk9GJGsoEfLQbiuEePuJN+GSdzoS97F2lEIr5UIon4B6fZhs2BpqgnFSFLcICvAWN645axrKe96AeL1KTlNmWMGk2NO2dyRewME1iymXzVwgeWVCMBdgl'
        b'jmie7WbCLiW9O0+rfA0qoSxHnL8VrgsmCxtzVsjB61CCp+AOF7YEz4aZXNmYZmHjXKibihf4kHRs3mbCbrauC8JMLINKsu5GPg8UR20yQSmTe1HAPuyE+s1beMt0uIy9'
        b'JjVb8SUByrEH6ma4i0rrCvYzHSTLxRohSkZNj+by7cPTWVhtchf4CKyeArURIVxU6Mpp2O3Kpu8U4AY8gmZsmsZXthz68b6aH8BN0hI2QW0w1nJpS7Ge1FZChyZRCYc8'
        b'4JYT1ogKeEifnzbhXXacVQKe0EFFyCsWb9Z0g5ouYrdFxvVMO+iEc1OhyzKeGhdAHVxR4x022W0B+uEJNGVjG5/MiNeMpoNSLhAu6OggeqbwQUZ4iA9NeJ8tvk7Yhw1w'
        b'FmuwVDyjRs8ok7t4pHAfrtMZ3w4Szaf9NQG7VazpqoB3aeKGsbazWG0hhXWr2CKuC0p4DE14CQrFUR1YA6ex26zgkx33hopgfMKnOgQlcAa7Ryn5sDl04o1HE8VBDakz'
        b'qIHp4oYAj8ZCE5zDfr6pzEN5ZPddbOlXBG001GBFGt8U3qfP6wjf2KhbAliDoeVVrOKDcuF2HLWISgo4QCrs3sEb8L4wmhqYZu+Que6FK8JR8TyqoGk56Vy0u1doAWfx'
        b'USBf9tRwMqluVwkf4xEClwnJL4hLOIOt7rSKbtbWLmjDoQGvQi8ftcGJLQ67nbjByJmOtu7gLfodY+kAxVW/As3QSDZiFdVghVPr1CrW1CtkkrFeo5/HfJAfnElT410m'
        b'7Z4AF+EMXJ6vFAdd3oBV6jyFaJi9JLAOesO5jW+DyjVq7GW66xIiRkGjzzab9+EpMzWwzXYLFiikQW2R3PjgMbbDNWpT8JkoIJ2HFjXtl/tZTyghkJmtr4gwZQYN7J/P'
        b'9arEk2vVDIdJ34uSoBZPY4eFRfLVUE6IVLIAK+lXKVzBawpBhpcl8b5ktKwD1sNJbyjJw3NQRhabL1EI8nQJnMRKbLdM55u4iZdtHUJEMQosJKhxhjLpeKiL0Moso5mg'
        b'ktxZWCJbSqglZAvZU2zngH1kcwXRcjgLFwQhSUjCK3DBwvw7PGBrtFIJD1nsSJk+l0fr7INJWI1FcHMBtCl0sVCGV18ZA+3hcGV3rBBmUsB5tG63+HLchIYQe99beB7P'
        b'sbcECqULwmjF5+UU+cvkzlDpY/ER+Flnir3piG6w7pFwayy2OTrDE7lsP97gnSPxLnbYZXfaZS+CZurdIYqukisNoZa5DGLIaoqwOhI6aM32vti8cUEIm4f6Bsiwb+9O'
        b'LjgJ2rFicNHX4/ge4fErag1RlBvbxwgbNE7qib6WAHba+VC73NF5CmGITfgCCmBl7Fc7kx9gVORmLrXM44xjOXmAfSllsiRROJ16PekRSkiHkdinXBxEIFkIpVzjxEHa'
        b'Y4cun/QCZf4L5JuFSdgtwztQiGWWJdTTBa8nDVFh2TDlkGZuxDIZHbHKpFgCgAK4ArdV8IDs5THfjnvMYTbNIzwNtxyakkEVOfF5KEylfvVCMDYroHwbGQjTVvykGcMO'
        b'ga2sk2w5TNz4ZKiW4WN8ulE84DvL0p8zB2eoo95t4pFZ5U4ueFpkAE/gBAGto/uQvZybRtPYrSLsqALqtuF1cVCNB63Vbp2Dh3FTS2BZJqqADQrBCgVc2jzWouWhEfpm'
        b'DTc89n4NVtu7T8ZOuSo6h+toXMomxwSrKCbbrbqXzI6vkVtfABQrTIpoiz/bdk9Yon1Iu4QG0BABzh5mOoVCDVwmm4rFJ04ho+EknwLPeJHQYT5GJrJuHBbs9lkgrsgE'
        b'zSoshRZ8IO77Dl6jv7YhN8PUz9mhbVU1ChOdUL3Fj03Ti3Q69tOzuzJeHxMersFqburx2OQUiI1aSyD136rFiw4rvLdblHtziAL4ygLhkYLMeTtXLXZMXW4b0u7o2A29'
        b'DpeeK8NHFA+s4kGU4RPC3RGG3gq11L2TdZ+EvTLsOrZQ1NJ1E/aPsA8+aHTgUPPIVUBt/KuWORz+xs5m0m8NSt8Y68AAmQxvYzdcERd+Lpepx65C29JNMMQkrsidoCvY'
        b'Mp8tvB4fEW+k7tMWjlwNFyGHu6NiV6+FzjnEQM6rsHI8kR+2JChIHrIJ8Qwq99Nph2sUQhhcUhBaNvqJyFEWsWMQOBw+tJ+Ihejc3ONCsUEBVWa8aQlm4luwf9+gP9gR'
        b'ybYqGa3K9ZX5ksNwdpPCaREdzFNxpiKCo9JoDhXUebh9iDi/Gcpo93hhOpau5L491zuXLe4qCRmCbLw/w7RQuEeogdeX8F3PjVs64pSdoIEOol085C46iQVw2TKTuvom'
        b'y4dBBrOI65MZ9E2GfDIeT+zk889XDaK2Xej22Y7DBauM6OR94j4MUEmp98nUhi/BDc4ukDJEvU82hnf1Ygi7QcS/Y6RJ3tpJ6r4lLvYOLRbuwhPendLYIuix2Vi7rTst'
        b'68QC6Bk0sx7oPMIV7X+QsHYkIC4I8820WxBXSDDWK6BpA+aLh3Nz15GRGlkQhs0H7HgvjtmhoEzirA2lCSlupg33dDKxAPOgo2+McVocH8ttBvOnQ+9wQ+OwewDv8m3Z'
        b'NhIK/QqoIO9sFUfdTxdHnad44hgpTRanCvegefoWeELRfAk0rHKJW71Y9PjblKKcGhmZ3eMdXqaV4X1iXgUcgCgfLAh1HPJKOsVBgB+KchZFDtydyS3NK8k84vA2p9mh'
        b'YRI+kBFnvwznRJcvk7HIPDIMpAUPkpV+uRuZpdj7ggkqRojG5kwyuA5R9i0Z3sJLlEFwM+rErl3PITpNUz/kCPydFh7fyYWzTT52hAyb9KyVg0bEzLk/AZ+Kqm/05uwG'
        b'z+9+geahm5AaT72CV3YLxgMU7bduEqNSzWwe9LD0tRHmBzcVo22hvoOiJOUhYoy5MIcA0m5ESbJhwD+E60C1wkzUopRb68TJuS8wcDxLSVTbMBNvIaRbfshmStDqObj7'
        b'spHLu6XInS/ZqHKCNmhfQOSnWjyQh3glko2KXDWUjZBNKJJIB7FCyHgFsetL4WLsezgLnjri5SBz4Y4q8ke4K5dTzn+SM8iYY2uf24f/ZntcmozFchU+wF5xJa1wipjg'
        b'CKOW4BmHIS2V4ZO9FOxDeF53FB89T1nCoIgsc5hLY7WCct6eCdoYnrnsWY099kQjj/RZOC2K5xlSuJ9o4qnlGbI7LVjx+h6R5j/ZtNmEPRJe0NiBbYTH7U68RQo3/O1V'
        b'E6I0T6GGmC1P36B7PZ41QSnLcJsEcu4TcHE8dNuSX7yC901GltJYKeEyAFlZjVghuLkeG+z1ltDxUBSO53gGkjwDm+zlFk8PKJ6ym0+zJwgKKdFniywX6Fy7aRV1tkRa'
        b'gR0ak4uUL44Q4C6wiCSWaHZAjdYExXKekBKU1pN+8heLC+/dC42O8g1hCp19DbFkT2aUoxeb3JjAeiF9DdRM8ebCZuAdrHFUdbBQC41k43w7xwMzHDWdMJq9Ca4dEXPl'
        b'0g3Yba/rRHhScnbdlU+/HNvwnKOuQzO3QuU8Ahqut2ue0EptTjz7x9IVcA6ehHF5yUf22ys+cElJSijCJ7Z0VMACe8nnCJRQAnuSlMB1fS2c1m2v+uw/CpXLXXnDImxw'
        b'N4nZdaMwBxqh5lCCWD1pIbkX7SUfrIB+EteGRXyUN+ZL7RWSMXtpR+cpS+R77ZdJTAcVfEMHsJ+Ce7VGVHU1ZY6O0glWwQU4exDu8XUfTYJ6apKIZacmPAnn5hP1YUa3'
        b'aTo02KsqlIH2Qz08SuODPHdBt8ldIhZVrOSVF6EB2vhca47j2cGCSzPepJZH0MOHeawn0LRXXGjcLTqnChdRfZXkVrWOisssgpgKs1j4obMp2o7dol9cIpTzghq4t1r0'
        b'mHOWbdg9im3smiDPovBwEQu58wUERDiqNIdcoTHEtqmQsUTn7FUan1eIm3USKvBCyDXo3krz8PrENTqcs1CfRZ7kxZPZ/nnY7ebEawOrpsKV2dDM102pho44KTe9u8KC'
        b'xRRuq+EEb9pI+T9tN1fKVbsW6ygcnZaLU1VNXUwtSn7w0AJVFGRb8JKoicfwMGmwWgRP50HNrFxR7eR41Y5iEQtZ0LJnlFjy6EmjaGuvFjFeQeDUDA/EkscpbMh0VIxi'
        b'lJRVXp/MJa6EwmWOghEZTBWcxZJtotpP4Glah8Wm9b5MyjIrsU8UeBOKV1CbgnviNB3t+dFE0XIrcijV6cZ7oubJoLqg7pit7gclG6EOu12lYrHrCjyFS1LCb7aSgzT3'
        b'KUeFyowP4fJiIoNcW11QMJ+aFLwElIsXaORZvM9X8mrYpsHa1THK9hugbx8XqIRLawZrV2PokJq2w2netJSiRpUa7yh5UyQ2wUVPwkVmNuPjkx11LcifD41rI/nnseQY'
        b'bWqVkheU0qVwde0RWz35EJTZq13LUuAanWYHNxm5HLvVZtEyNUSjqnfAHfGA++FmqKMMhrfXw2UszuDSVsJDH7ULm+QBpdeHyZia7ao7iZ3p6jwmro20SthynsC0lc/k'
        b'j7dmqPPYqJvCjlQ6+atYzhumqqDIXlRLwBrCkAqx2Ls00OgoqRG7q4NG2p5YSqXBZQscZTVnVlbLkIpLyMda6HBU1bxSaKsldoO4A2VatRtTw2OKAfAYbswyiaMKKUJe'
        b'Vbsx23sqKOAhBaVWm4r2QOkSNXaJygt1JXlXJ/H1RcyCR9TAxvSx3d6hdKfZXTSGVhJRoXaW8qk24wkKrMWUFrFDehV7YtQWsbrtvQ8uRBK5Y/P46aHaXtg76gK1xIov'
        b'8QYnSskL1CZbQfKUHzRJp3Iz9iI/u0274ybyRIBzk0kvHQQhodR4RHWcmqqhyFbviySA67TRQCjiVUI5QQmUbBN27FMSBl5VaeWWCTTS3UBeVQIdcDtmA5bKBBk+JbYN'
        b'ZV4iftdCO5yOxmJZboxSkO6XzLNM5OVFAyFjXTSWz8MyPy3N04yP5cIoD9nYsXiN62sBFkb40bzn4wIi5YJ8lQTaj2PtumR2p2T/QzvhF078silS4Pdb7F6L3XGxuy2Z'
        b'1TnV2XarJS+SFwivKY6MflXOb7UU/CZLfkyxZcj7ICFFtkVwTtPKf/47Og0XzZA/4exi1KTRZfEbUU1qtlGTp8swpBjMhwOHdRz2jyjxPtb3QHaWOZvfrfrab2M1BpKW'
        b'pzNk6JIy9P5c4Hq9MdM2gYmNGyYqSZd1QJOcnaLnt7NMKpdnsmTab311ycnZliyzJsuSmaQ3anRGWxd9ikZnGibroD4jI9Bl2EdLcnRGXabGQNMs0WxNFy9+2Y1wkkNK'
        b'4IsGJBmSl7Btphny9Fn+4ii2wDVR4cNWYMh6bkfsTzIpRn/IzLag1yWna7Kpk/GFE/G9GQ8PncxsXyap8h+fx8zuwG3SAjWxFpOZ7ZHpfUt8QGjwggWa1TEbI1drQl4g'
        b'JEX/wrWZ9Dk6vjBf9s5XoyfTsOjMen6lnpi41WjRJyYOW+/zsm3rFzXOTcu2F80WQ1Zahl4TYTFmazbqDmfqs8wmzWqjXjdiLUa92WLMMi1xzKjJznIYqT99uk6XYeIf'
        b'MyUfNJhGbOa5K3WVMPIm1zNuHXfsw3B7n52DYgOhevH8afySNm/HBOFxXoogJCZOrjBoBY5iBD2FXlBC73YRY6gRds0Zyzv/aoKLsDXah2hUYsb5MU7iNe+A1F1YtXyl'
        b'IAQlZvhpFDYJt8NGO+4LCxKgzuiqdRch5pYUntqbNOwmMcSV0/71u5zsF4mvhVPecXK0/YavAsvsN4nQMgFq8VqGyPo3GwevEu9SSG5GihUi4b0ShNfsd4nelJPUTjrG'
        b'w8Q27NGpc2Sce0HDdApVVdgpXtgqw9W5Ij+BMzSiAbpcbAzlNDED2+Uj4WsnscYqP5Gmd+/Ey8TulZyFBBChrHLGfq4Bp7i5jmtJBbH3Cn8fvoC102hHjkvJRxuoqXa+'
        b'GMHyoW6T407Sl3bUFLHBlqjArSlqrpxeYlbEaJuwnKLlOBGyy4kVdfO9NlDOlg+VGZP4jnROW0wHnTjln04BrIKaGnjD3my8aufvSrhBBL5epZWJbOIuXDbb27ATLkGx'
        b'RIyI2AJPNI55DlDHSk+8La78HjxZbJ/KBU9TdGu28JYxO10caQfexl6o9MNqrVQcddEbzjlap6+hpIQyGb7fnmToHLyJbqYQV48dU7m5vW1WCpWJkwRBk+h/RrNC4Bta'
        b'noF9oUFyZrkC8buOJBneNvzL7HdkJsbmvszwW14ZHCdbPSri/372bpY0RV3vs9nF19clblXE6v5Izymn1WuvRr674eyqqPBTvzQvhjgMXqT847m5P1N5zu/ddNnwyZ8+'
        b'+HJPzTNX7z2Vz8JPZnq99al0f8HVd985G/7Gu9njq/6s6br00Te+0XVq8a8eTag9rpy3uP0Xi5+umPHsaM4x15J1P5je47zvj7M+Cjs5Zsc0nXTP6Hf61zRFNm0/MHDd'
        b'w72m9vi7XX25K7b+7dpffvnWvMZm379vP5b3y7LclvzGP23+4Enls8dPPt7SdrD2O7NDfvdWb9C33/r7bLcf5FX/7J3zfqvTpa/dndShUyz9JKtx7l9zb/9rW8xnzmfe'
        b'+OD7zx56zv34zTvr2rb3rc76dYuicFxh/PEfjUpduUSqdTJ7i6lG+xS/AJ/IACmZQD2WTpYG4B2oMk/i/HCDt19glL+vNjCNkr4KfzxDSZ9Gvn/bNDM7nwyzT3R8AJyJ'
        b'x2KiCWpNwiYplmdncsHhSRspAz/jGxAoIcH5RL+bpKH78J6ZFRk3w1lGlsWnZQ6KT8vkBWC9vy8Wz5MKgfBEQYhwdgOXpMdTRORi/aMo3xeUYcQQS6Ru/nDNPIuZCDE1'
        b'tEaLIsgDKqAVe0VKMxZPybAPbxzUSgekPlpmsILWmf/6h18Ymv557LJUY/YRfZYmVXwuK5AF2xUDLhz6E9g/WDfTdga/xwWtXCKXqPiPm0QqGSdxod8u9Jd9Pop/7iJR'
        b'SZXsVTL4ytqUEm/+m/3Ljf4lZy3SyRJWBBHi+GK0ygE5m3FARgF8wMkWDgfkLH4NOCUkGC1ZCQkD6oSE5Ay9LsuSk5CgVX71HrVyIyNjRvZMjpE/xMMeDzMyksbnrWF7'
        b'm8r2dkL4ZDKtWypR8lfpX6RSImAS4W/sXxYN9RiL7R5DzmLIOXS4Yd+ezQQujHxCx/Lp0dSGJXFYHh+l0McLbjmyRYcWWdg8WEB5SUF0TJxIM/E6g0/1bimy+x3xFnon'
        b'tkMj0VPo3Wnjp9hoSZYNCYNsZ072MLhCcDxDJU+V25ilrEhGzFJOzFLGmaWcs0nZMfmWIe9tzDKdmOUzyUhmyR+0G0ItjdmZGp2dDA6nfcMp3ggKt/UrmKZRn2sxGEV+'
        b'kaM3EtvMFImQ/em/4VQg3s4QaCG+m2lGQ6Y+wmjMNvpyYTpqSXkxgWTrZcsVSeTITbyQPdk2JY4YucMXTcEo57oMXZrGIBLf5GyjUW/Kyc5KIabEmacpPduSkcKYlEiK'
        b'OAW20d4Xc6YIA9vyIEUjOq7ThASYLTlEvWxEjGuNGKQP6+HPJtJ+DYNSPMegFHGW5fTeAy5SpmZ/qnAZXhzyYOGZGN8N/tC+VXzGkH0QHxMVK2E1ijPqxUrs22oY1ZOm'
        b'MDE5b/zkw48TA3+t1UXqMlIzkj5J3P/6szeaDz17oxJ6KhcXttW01HQVtEXeLGwpDC7T1rYUTq89Geoq+Dupr/y1Qis1s/uuTcQgbijxlNqXuckZLI21BIgAOg265exe'
        b'7KGZOdTGNKiODtxACAplolNOxQqZMBF65FmSSK10GBa8DAU5IAyoxadLB0HPTQS9FAZrozm4Gd0HwUoxoLLb1YCTzUJEtGHPExrZo5/DppcZWc3V6MFenB0oxAT+6xAU'
        b'ujn65SjEHnGFqjjoHrLh8c4ch/h+4dQ2/vTDhEWbh2XOLG1uw/NwiuhW6frdcMlfti86DMpziea1whMXIQmrXLHxVSgRSdC5xdCnzqOme240OXFVvHl8uUg5L7nMVef5'
        b'TcxlnxcRcYFHUXyM2xJsMyXBXex1D5ELUqySjMOuTSIFqp4yyxSyA6tJbZJs9uDYSdvjg1PXLVbnRcPVPCVJOy1gPTbssz+h0+wzlTAwaaENAlP8eIoeGo0FQzL02/BA'
        b'zNBZuYKzqn1Ev4r94uD2DiyXCFIol4QTKyx9Dj4dWcQ6Bp8yDqDi46dSqypV5YBR+T8MoyxB/+vLEnTu/8PT85eCCAMc1v3r09yXZJ9s8P948pmcwZdl0pufTzdHLJDp'
        b'JTs52UJ4mZX8/ELtCWfExtWacAr8RoanayluJJuzjZRC5liSMgymdBKUdJj3tOF7OKWkRl3Gc/LWkNMGDlmbjh2KhT+m7rslfKuvP/1au5b9Co/fHEy/aXm+a0LW8Ibw'
        b'cF//5yQO2RMls9kvTJvZJrmec8RkmaSmMGg/nDNCgezPPxQ0HRKzc56PlezPPxYvhx3ef2u2LhFelK27U7bOggTx8RMLX/QIO0UaLPD7imBjgAdiWk8MOohS8u/KLJPr'
        b'goLETN1JM0Zg3HljkGHy+fX7BY4mUBmugxJ/YLdgu4RdBnwsAl0HnnOCEiiCIkF4DUqkYyTOCw5wMRtc3AQCHO/Eo+aYu3M0hOT8xgxOTsXToVGb6G0wewIswsLgHC5P'
        b'xPLQA3G0xxAhZKYzl/CT9R4C0cZFd3zzRuUH72QS+FKqoFcVugHu20S0ynkmnRlJaN7tBI3E6zYKG+EBtnApzttcBIJKVeLqgzGrNk4SthpCysKlpnvUNOrmudnlwW75'
        b'qzwi/u7/LekrHRm/WZaf9jsXrzfLk0arRxfvS7r8vXVJIX+cnPhhwDKV1Tg+5Ntffv5B/NPKb9X5qg6X/kel956SvC/Ld37xh8tfbp/y254da2Yuz13z6L3fVP3orMcH'
        b'pbXLVo0OrvrinR+6Hwp48/rMdcYv/jL+37/RcyDtvMsX34i68onmGw/l19Vflsb2TawJvKiY2w+vycaf3LHj2U8/0S49/ZP67vu+BcWdDd+I+94vYk+//3unN76YXzVN'
        b'p1WZGfJ7REGJPTELGQf10oCxevMMdiR9ngeeD/nQ6ylG/QB8aGbX0GugQeZHHJrSM5ajIcWdedQzgI2KdiK1XlJG+UOdWYyY1O+JOjqWGEWp1iFzLFjlqu3QwdfjOR16'
        b'KNuTCHvwsTRPshofQYFZvK3C3sUs15sXz9a6Ep8ek/rmjhLbTsJNzWDythOLw6RuRxaaWaCCQji3PBrLorWBPLWEjj2C4B4kS3PBy1qJSAhU/1SmJnIUZzEvo0DBGUqQ'
        b'yFCOC4I9MWOvUkqwRvFUzE0il7KEawb9eNt+jGOGcJjB9GhARpg9hLp8XWYlG5JZeTnoDJP92yF05tzEr6Yz2Lkcyx1ZlZhrrwr0RKuMfc3ASyvhUX2T9giWwMPjQ8v5'
        b'G6DguS+WOJIixoIopktTpY4vkEj+oS+Q2CL5n//PMFjbLMLiS3h9KqflPAAPrZb/TydCL8Vlu7aG47JSzAEytoS+BJQJkYsoNX0ZKpOn1HC+NwPr55ly5XBCrMQS/WzG'
        b'B/xRG6jEGo/oeAU8DcDiWCzdgkUx0tER0Aan4RrU0RutsNHDCXo3Yo1h9xefSExLadT8hlc/TvQfkk3sMe18va+ypVoSGXotKCDFf7ufLk6n/FZQYOKHiTvf8n739X+T'
        b'ClvCXWd+t1WrMLPHwo1qPPc8qCTCCRFU1OlmsfYXnSBi0hy4w+pF0oAJ0G+eSE2p6w/aSkXcmTfgdbFUNF3PEQZbsA+vqKMH4QULD9kQJg3rebnpGFbhxWi84jOkpsQq'
        b'Snh9tOiK0hf6u1Oa3uzwdg+7t09nXs5LLRLjOIc3t8nEEscL0482idjIvZSN8SbnMWlELz0hfOT2cj9lGhjljA2OctjeRbbFQxNWfY0TSq3C/5MTniInbB9mw1tyMgxm'
        b'k8PTxDsLcicN+zTVqEvjdxAjvM7uuTpN2AvT5mGdfcLjt8Vt3bzLXxMeGREevWVbLOXTq+OiE8Lj10b4a1aH8/aEuG2xayI2a786yX6Rg4lXCZOUk5ul3ry2G3c4SOAZ'
        b'WwJlZnXsm3d+7Lt7Z2I2RTqSHDlWaaHNBeoOQ5MT/YqCM4cFaFS6kDdewGvig/FnsQzKh44nz+JYuV8zFW/I4TI0+BvyMn8gMW2k7mvSJWPf7nI9ofGK+N7BFqP8yAeJ'
        b'zjs0bpfe/Oi99Jine15vTTpa/p7XZz/44n2vsU2VW/XGxozPVzsvHL9iVpvi+pbgPy6b87fknmf30nevLB3n2R31mlZuZo7vvHQD8x/o2STWW6UB6VghhuCS5ZBv8w98'
        b'4js0AsMFaOCV0K3YlCEG0yp/sRgqdcN8vMsbKX29tSd6XnwCC/I+SsHZWwoto7BwWIL9Yg9yoYTENCSp97I7UbCKB0lWyeSp/USHIxnHjxTn7XAd1stnmOsMfIXrsM07'
        b'w1m44hfp7xtnr1DIhHHwSI7N8GBsQJBW7OU+JQ9LWCNl7hXzoDheCU85Skw8Lk+fl/VyL7PV//g3KB31v3/S036+b2T9b2jE44WyLF0mT5FeEOhYgsTuAXP09AEFxOGh'
        b'J0r0twyd2Uz5TrKOotZwoTz+6VLEEuNzmd4wWY6s7+uSPjHJ+98agCUvxAdVnIV99RoLVcT+XxqC27eOTntJAH46kwPMh7u8Bc3aVHbbufcnu9PFu8p1uVhsylUcPmiL'
        b'yViwRvzizinshX5C9iEBeRH2viAmw1XxMrUwTCnsDJrG8WsgPkgwhO+cLTXtopbvXDTzQP359xyh+qPE9NQY3Tup/ps/Stz7+rM37lQG17YU6CTvrSmM8/j2RXhc2fWs'
        b'9dTs04qOpgkdTduqWmokN5ruKTtWnBZLgn/4yThF1J+0Sh7GXWbDdVsYh4c+z1UE5cf59QsprnEpzw1qjbb0IJ6X4xnPLI1VCAvjlMfgkYzHfJI2ljALOg5F2jErAvvN'
        b'7Hvk0AMPoJ7Cftp4R+AXoz52JvDSoyuljh0M1eDMtBF5xUIs4jc4WE0QVm4LnPfmDFvHNKiSY+OyDfZ04OvKk6M4FSC7Zl7DoWycHcoiGICNkrhIRU4wSmKc7AAzrWxA'
        b'zcAvIdvIiMQQdvDCCWk1Uxxgx6QsGQZ2b31FeZJvuJvCUk30CK3rsdmx4WkrtLK4uHVayTqtNG6d4dPj7YKJPXP47+4d2yp3xY/Z5PUvnz4J3dca8N01AT97+qlL8aOd'
        b'7e+Xe0covHo++s7qNWsu//Htdx/vrKoLNrzv9LOWL6qPtIZOr69uuPj3I1Vf+n15ZUINxOy5srDj0+jPyifsyO9ccWuW99Jfg8v7pf9ZM/CZ/mbxj2/M+GnR4s8yd/60'
        b'PqDsvR+u/OLywOT3fJty+vQ+PZZ3A29+G1IGDh/30P/Q65srl9zVBr+uCf9RzW2fLbpaz/ZPLr/pk1za3bD8E/20Lxe/vnqTW27tzLtTfuX9L4un/ygqLrc+NP87xvLP'
        b'Y4LeVgSGfHP22+Vv5e368Y6+d+bfMhU0xJhKloSG9QXcDnxnym9DvrX8Qcj0vee/XPaz6RWH3h3z60MPl4+v+665s6l+282ysb848NNDvt+c/0ZN9tHWA0dr0v5Umn3s'
        b'49ufv3u0tfXVMW6W0KYPP/zuoSO7z2x2d8JXd/62ArvLv727Um1OzE8K8niWVfPB42fG9xM+D12633q6/Jvjc8ftw+j918ozfvydj5vKf7Dy3yNqdv7aNftaZoTx45NV'
        b'KasDz+Xfzbn5OPr3Z+M2P/70Nz2P3rZ2vtq/9E/NqWu/fOv62pKOrTPfjrr9q4FX34ztPvyDfOOP+wcut35yx4sck9+nWwW4T9GLTGER4RdYsXxPNHeiwFA8OZQXi+6B'
        b'nUtV3niaO/WK3VAxgptrfRw+DfcDuJ+qYmZgCVGDsoCla5WCcr90JhaDlRPraXDN029DABZFxcTBxUyFoIYuKTbCRWgV/bhwNTREMzgNYA/5R8VjM+tzW4rte33+yStT'
        b'rds/d8P6UjkKI8P/F75wX1clJGRk61ISErif/5p530ypVCoJk0z9u1TKLlNHS1UylYuUeeFflSr++3/f3x5lnIeE/VVJRstYVWLySimhk9cYF9qLt2Syj5S1uPFXD/Zq'
        b'nGrHPIItaULCELRy/f/XusQ4zQFtbCJ2z2Ti/4fIT+e8HNZYz4nsmYsSqMAKfJDFwi6cgQonwW2CbIo/dBkyf3hHarpA/TrPeQeULHeBVV6nPshccHzipjsea9+Y+cvA'
        b'/CTtss1RE9/ziZob98dx/9bwcFJKfd2nyVu93Ef9Jjgq7fGo73/r3A3nn6jCdn9c+n7T05uH9XG30uPH7fvbQ1WSV+BTl9jHqqz0jyde+dfumGvut996FPb7VeNe+Xvm'
        b'h5/9Rbnjw09Uc3re7WvNwYCDYT/+/PXk7u/HfB7/86D3S+/+p+T1bu2a7y/UunJXUEB1LKtlxcdPwXu0FVYqU8NdKd6Yj5W8bOUMVXCJsYEu6hWUFs+KXp74WAYt48N5'
        b'h4gVOaIeoDWLhTEo43oYLZsaJz42AeVaOBkdlQ1dsb6xToJSLlVhE57gVbbgZLzit0EhSKA/OFrAWspfus3863lW4hsVI0kPlM+LJjwopzBSIRPWw6kA6HJiT3eTOFYr'
        b'XH8Ybo8coxTG4x2sXyv3JYmPzSxuuS6PxW4sJe+f55sbgH2hIhBNtMihEK9T9sFv7asnIiVggYRjpdFY4iTIAyTQCfeNPH+ZjGU7eUxjCzLk2Zc0CRrk0BoeyDUzOW0l'
        b'lmgDUsgyzpBuyUYkgvsm2TbogAKRC7Sq8CrrAo1wh/XxZxvk6ZpE0OA9hTDfgy+YxJ+Bdr94fyxGK3awtI4dFD6V4n08Db3Dkp4p/z2I9N/4opW9DNIMWQazDdLYd9IE'
        b'V0ZXKAeTySUMFtjzIx6cwjAS4yKbxajNPKPGAQnTBmQZ+qwBObs0GVDwdH5ATmmAeUCeYkimV0pBsgZkJrNxQJF02Kw3DciTsrMzBmSGLPOAIpUQlX4ZdVlpNNqQlWMx'
        b'D8iS040DsmxjyoAy1ZBBCcqALFOXMyA7YsgZUOhMyQbDgCxdf4i6kHgXg8mQZTLrspL1A0qegCTzi199jtk04JmZnbJ4YYJYnk0xpBnMA2pTuiHVnKBnicGAKyUS6TpD'
        b'lj4lQX8oecA5IcFEKVZOQsKA0pJloXxhEOrEzU4xsmzAuIi9sMehjewrVUbGcI3sO4BGlvcbWf3XyL7HZQxjL4zRG9n37IzsPwky8toXMz0jczLjYvbCvqZrZNo3sq+l'
        b'GReyF1abM7IyhJHV1o0MFo3MwYys/GZkVUFjiAM42XG4OIDzP9a+FDh5zz+r7M8VDXgkJNje22LbnyemDv+/oDRZ2WYNa9OnxGlV7ImflOxk0hC90WVkUDTQ2AyJMWD6'
        b'3IUOw2g2HTSY0weUGdnJugzTwKih6ZhxpV2dQ15Ea1wm/odTK1guxgtrcqVcpmIWF+0lYaHovwCQ3giJ'
    ))))
