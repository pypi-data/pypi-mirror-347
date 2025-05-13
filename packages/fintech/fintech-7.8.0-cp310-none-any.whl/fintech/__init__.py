
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


"""The Python Fintech package"""

__version__ = '7.8.0'

__all__ = ['register', 'LicenseManager', 'FintechLicenseError']

def register(name=None, keycode=None, users=None):
    """
    Registers the Fintech package.

    It is required to call this function once before any submodule
    can be imported. Without a valid license the functionality is
    restricted.

    :param name: The name of the licensee.
    :param keycode: The keycode of the licensed version.
    :param users: The licensed EBICS user ids (Teilnehmer-IDs).
        It must be a string or a list of user ids. Not applicable
        if a license is based on subscription.
    """
    ...


class LicenseManager:
    """
    The LicenseManager class

    The LicenseManager is used to dynamically add or remove EBICS users
    to or from the list of licensed users. Please note that the usage
    is not enabled by default. It is activated upon request only.
    Users that are licensed this way are verified remotely on each
    restricted EBICS request. The transfered data is limited to the
    information which is required to uniquely identify the user.
    """

    def __init__(self, password):
        """
        Initializes a LicenseManager instance.

        :param password: The assigned API password.
        """
        ...

    @property
    def licensee(self):
        """The name of the licensee."""
        ...

    @property
    def keycode(self):
        """The license keycode."""
        ...

    @property
    def userids(self):
        """The registered EBICS user ids (client-side)."""
        ...

    @property
    def expiration(self):
        """The expiration date of the license."""
        ...

    def change_password(self, password):
        """
        Changes the password of the LicenseManager API.

        :param password: The new password.
        """
        ...

    def add_ebics_user(self, hostid, partnerid, userid):
        """
        Adds a new EBICS user to the license.

        :param hostid: The HostID of the bank.
        :param partnerid: The PartnerID (Kunden-ID).
        :param userid: The UserID (Teilnehmer-ID).

        :returns: `True` if created, `False` if already existent.
        """
        ...

    def remove_ebics_user(self, hostid, partnerid, userid):
        """
        Removes an existing EBICS user from the license.

        :param hostid: The HostID of the bank.
        :param partnerid: The PartnerID (Kunden-ID).
        :param userid: The UserID (Teilnehmer-ID).

        :returns: The ISO formatted date of final deletion.
        """
        ...

    def count_ebics_users(self):
        """Returns the number of EBICS users that are currently registered."""
        ...

    def list_ebics_users(self):
        """Returns a list of EBICS users that are currently registered (*new in v6.4*)."""
        ...


class FintechLicenseError(Exception):
    """Exception concerning the license"""
    ...



from typing import TYPE_CHECKING
if not TYPE_CHECKING:
    import marshal, zlib, base64
    exec(marshal.loads(zlib.decompress(base64.b64decode(
        b'eJzcvXdc1EfeOP5pW1iWBREp1rWgLLCAgr136oKiUbHAwi6wUt2CYhYFEQERxN4VjA0r2FtinInpueQuySUheS710u8ueS6XJ+cl8fee+ewuSzExeb7PPz998dlPmfKe'
        b'mXef98x8zHT5p4C/afBnscLFwKQxBjaNNXBNnJE3Cka2kmtm0yQ5TJrUwBuEjYxeZpAYpPArXyu3yqzySqaSZZlFjEGWygiM0aN0HMukKVhmrcogMyrSPQ1yuCrpvRe9'
        b'qoyKDaxBlqZYqljNrmY8sjUe9/srFuQa1Sml1tyiQvUcU6HVmJWrLtZn5elzjAoN/4UMQPtCTi4E4nY2Iot1awEPfzLHryUGLtVMNmuANmyUl7E1TCVTxq31sLOVAKWd'
        b'q2RYZh27jkt1u6dQ8Los924hBY6Fv96kUIF2TSqjUevamX+SzwvyCTi9VkpilIwPdGBGeEhJDvOZmPebqS1MjxDSwsYRCLlqpprP5l1Qso8E5cauUDoL7wyloLNFklHl'
        b'USO6sDZVi3fjxgW4JvwxXIPrIufFLogNxfV4iwbX4i08M2uhFF/A9UtMt5b9D2cJg4xV56VfZXyZkZ/9dUaIMfwjrT5W/3XGy5l+WbnZ+dzFdw5sCBr3OluRI0s4mq3h'
        b'rMMgB77oias8odQwUmaSTYtv4P2heHMkxwxClwR8wYxarGpI2B/tgP91aDM+irbirQmQGNWjrTJG5csP9MJ1Zg9IpOHbuRCNmWCmeCEv7/tMyjYXrTUWqrNFBJnSrtJb'
        b'LEazNT3TZsq3mgo50glSuCiDVKzAmpXOrC18u5BtK8xql6Wnm22F6entnunpWflGfaGtOD1dw7vVRC4trFlF7j3JhRTSlxTsBxefz6Ucx0pZchVY6c/kahtO2r8dt6LW'
        b'hPAInTYU1Sa7d294NDqJ9kpwi9Q7nwDzXx4vsC9LmHHTUhD7n8VNimyGopLa38oZpn3hw2RUZP5lXfEaByp9MJV+/dewlSMCuVMSRp3Rr613sZjlyUg+dixH7jLy86eV'
        b'ii/rg2TZn/CBUGBGuFUez9i0BLxtReiUJzoVDiDV4K0F6Epq1HwRGUIitCG4JjI0Lollli2VJ9r8NaxtEOQZj/dFe0JzErSKELwZXWBmoFMC0xc9KaD96NQcW39IE4lu'
        b'xsFgbo2EBpNfGeOZzA2fDb2xf7xtICRA5+1jyAdxpPEmn47BjkWnNbzNn0B3Cx/BtxK0mvgkCRODyqWpnP/UCFoBOgR4m0C7My5OyzGeaC+Hds7DpzLRWRvBJ3x7KN6D'
        b'65Lx5gXoRHxSBK5NRGcExhdV8rgc7/GFKsjo+bKlCXHhcVpo/47FAImEUeHNvM4HbbaRcfUqwQfIdwkjCJYcFh3BV5faBpNRx/vQZYrT+DCqSEqKw/WaOCge7+DRTdSK'
        b'a6Gz+kG66XhHXsKoaA0+CSkScEMyFOU9mJ+IT5PuJBCgWysegxQL8da4uCQxgQqf50eOnavhaFf1x6fiPGNhhIpxHd6SQFrrhw+iE0oen9DGiVjWqEBXPHFDpDZeZyOp'
        b'4vAVXJucSNLi6tmjl0rjDKgJmhwEiWeFTsB14TrcEBceIYWOu8T1KcKX8B0NrW0JegIfCMMNiWh/OAxOuEYbL2F6D+TxDrwJXbdRmn4CHzUnJGvjwqD7a+PC4yMjYpOk'
        b'TDiDj6FrEuiYGnSeDhKM3/V5BJwwSBDBMp74KJeDWvA1Bt22EX6Cz+GTixJoirgkdBRdxA0pIQnaUNwA/bo1NUUrZWYKUlw+FO8Va37SpwhSQ8vmAW6iLbGJuEGXmLyQ'
        b'JAyfIJmNN+KaTmyQc2fWTVQCVLPAY/lqoVpSLa2WVcurPaoV1Z7VymqvalW1d7VPda9q3+re1X7Vfar9qwOqA6uDqvtW96vuXz2gemD1oGp19eDqIdVDq4dVB1cPrx5R'
        b'HVKtqQ6tDqsOr9ZWR1RHVkdVj6weVR1dHVM9unpM9lgHH2dqBODjLPBxhvJxlvJu4N6pbvc9SRtvB5fpzMcrdLZguF+LT+EznXkLrlviYi/AWvAJNR0J38AMSo46rUYL'
        b'wwOUBh3lm8Gj87Eptj6ko7yh7+oAR3kmaAW3np0GGNZI0WU4utk3DDfC6LSExwIdoI0srsS30RVbAHwdiqsSwzRaYBmnywBzpeg0F4Z25tFvgDJPTcd1aDeDa8Nh+IU4'
        b'Fj2ZWEZJOxTtnZUwcS1QJfngwaLj6DDeZgsUkWLnQBjlnXMjYwk8QiyLLuHKOTZf+Dg/aUVYhAboHddy6CqbFmChxQUXoMsJ6HR4HDqINwEySPO5kDEpIn1dx3vxngQg'
        b'iHN4MwaGA/UNZdG5NVqasxSd01IEZBlUjis51MAmFidSQFAVaktOoPiGjy8NZxnpGC4AX+Lox/G4Gu0JiweCRLvxkWRo+jROhZtX0Y+roTOP0lJDgGouaiHrGm6kZDXl'
        b'KYkRwLlwQwiRgNu4QnYKftKLjgG+wqELwHrjQVFazqG97Bz8xGA6Btp5OZRKNISg5egOh2pkqDoQHaX9jM4q8ElclxQOt7cBPjs7FbfijbRMdA3fWoLO4M3w0e7DoUvs'
        b'glSxtpjH8hMIF5ich7cIjLQvp8AbxC+qUHQe18WicwyTouXKAIxr6LSNYOAQ6UJgqTBiE1dwaDM7F23vTUVC8QTcCDyFkG1YRBwoF3egX3QSJiBXGIWa1ZQTog2oJSIh'
        b'jEiMeDKsHlIO+MM1tKs0Potzw3iC5J1VIlCIqlmXSsTVgOJTxgMpcZSUeEo+3Do+1e0eSCn30VQiXmc6oghkLVPghUfx7q8yXsz8PKMm53P4Ff7035Fbpu33iI1mTdlq'
        b'r2eWhHsurpi0u2rLFuWAaf/ObpxwVbUpQ/oHJfP6F6r1IQqNzEr6QjWiTBRsuD5Zg+vjRMHmHyzE4u18+EKq7ODLarzNkWpXr866Dj6FGqjqNNU7idJseBKQdW1HIsAa'
        b'IUAL+beiS1YqS1tnjiApkwFRUQNJokB1vXAjjPYS/KSVisv63sE0Sf4sQnKoltbG84NxvdZKqARf9cFbw7SxVNbJ8WUOVQM334grFliHEhYEQ3uNQgOSwSEWRGhC8Z7g'
        b'UEly72KHgtZFZaJvqcLULhToLXlUFSNKlHydnCX/VayCqGS9nWk1QjtvsFjbeYs5y0y4n9mHvOU6ioR7QkbmPs6Saeb1jFMVq+xBFaPsaEOoBYioulcSIKqUEcKBCeCq'
        b'vIfr42NE5OOyud+ojfeIekJPqLf7mZ2sZQi8GPBE0VcZy55+7W7jvbfvNj57uXFbr+dVK3dmf5DPMtMWSgIPHgeFmrCCMnQCWF14CLDGhKW4ngV2cIYrTUZ7rQPga2SO'
        b'vUOrGurZgVXoKXRE7F+u58GxWU35Lj2ZWe8jh0HxZzr0ZL4oc2XP4wFacaBrKEiWGlIMuWEqVP/uYTDIJxWunBmmwU1E8doCHNnMojvqVZ3GgnX8pTqhssMtWDqsToQ7'
        b'yNWCjmaoCovSizKzbZYsvdVUVLgF3v2TtErgbCPgZ9rgFYABtIOS48O0Ol24FpQZosRt5ZkwdEmC96MLqPl/DYaHEwZjI3lH2B/lk/gM2oKqgIWKlQOpob34jC+u5NGT'
        b'S9DWh6PiBIKKLEFGMA6F34iO3ZQKlumJE0o6J3Ly4UGu+ikfrhZc9T8qJ+6xfkVP5PDuxLGCZRa8uPbOnTMffZ7xdcbzhs8z0tDbzwX+weflp1HKiLdQiube8ykvPf18'
        b'yr0/312GX3t58Usp+LVn9nJ+Z7JCcsJzCMHozyrnPZ6mYUVeW4vOeljQuVgd2DO1aUDzdLSBP/KodTk+oWFFriJ05VxdKESSnqXPF0nEh5II5+8D3EsOGC0v535e29eS'
        b'a8q2phvN5iJzxKT8IkhtmRJBMzkZm6A351japXmrya8bMXWzMzkz4evmQS6yIrS9u4OsfL/qgayInour5gwF5R3XJIaBRqglhjbeDtpTLYgGXR6Rzxp0FYOdLZs/nkGb'
        b'p3rga6AWHTCdEZZJLBoooO1YUF5Obk5+ji5Lp0/Ur/zwlPHzxfKM0/rPwepXZH+QyDPGC9Jz/3pfbNMj9p2nW9+4M5k+Cql5sCupV099Ye7l6gSScqdbJ/yth04gafDJ'
        b'5bmuTlg5R+wGjumHbgroFN6PTzyczro5iX4nhZF/XDcMF3QLTHeu2QQLEe/ykSsS9ETViNUL27do1GN67zX8PSP2jjz7g5cZJucdaTm2aQSqUoSiO5OHo/NUgAPL0ols'
        b'vRe6zKMGvEltjSCNfmLpCiqgwWwPideCQVcfgRqSoRu2hsWhcyGiyF+cLs8GlnOOKhhoB96XSPKE6rqm64t3CaCw3VTThDFoH9jSbUBJpAJNfKIuKR4sL1HXGDZUMgAd'
        b'Urjjg9vIe9kKs3L1pkKjId24hup5FiUde+kgKRk7IvuHOLNoQMxAqg7KaHHgF2se6sICkvpwBxYoP+4BC4hxNAcsmDNh1OiOpVb6ftBJk4AqgBVImeC1kmRUy3caNCcm'
        b'EGXByfGoqfi/57gC05MCINflkyaFquRywxxGbfR+I+eA5Z1lK3LG5NQOtYlqGdqJN4Rp44Bmr4DBN1GCj7LoCj6aQV1GeeP+6b3T+x2LZ8oH7M+By20toqsnLgGQT2DW'
        b'tEYe6X+w1Cq+XCbrzZDBjBqoGywEj2RM0+8IvKUI3miffT9Bb9CfMp4yfp1RrK+5ctb4JVD8lxmF2aG+p/VpTzeiy429Qp+V+71+Vs+d/uiM8bz+rN5f9iX3J+XeS0My'
        b'JlS9w8YGxPtffDOqzzv8vX3zF/cPbG1hX2xtj36DeyX8z9LT2UqK1Eq/AW0h04EvE5mZhm6gswmiU2TufKJ1okauCF+a3zM3+VUeI+TqLbkUwYZTBJOPkINqSf6LiqaC'
        b'5X4SJErHk/AjVy5IzMEdqCey3A6m3DMUrJiMYiLJfMKNH737EMVzMboOaocKX48FxRPwoA+xdi/5/YojmO3iCOZ+H+aRHvHohnlKnY3wVXxzbDTewfvCx0gmElWrKKZ8'
        b'4iUw8KueNycjnFEPFtGnaA5PMDhjkXdG4iUfO2MmLLynSzubbnrd08BZauHh1U8Oa18eqUJRPrP+uO/KgBE1DaGjcz4UND59Xtk8JNYvw6PioEIxCD+luVpzdc29hp/f'
        b'HRF3cGTm3V7Xzs3OaKy7XTLrVm+/3odr9r6Cns/fFTr7jS2x8U9e3/+fp37Ku/tX3bmbQ94sfPPC9688c+nMrfX3vkr5YdwbK49UPz9jSP6QIb2nbroyVv/Dz8zI4CGf'
        b'vRmo8bQOofRkw1scGjKwvy4WGh+MG6nOMMMus4RrNHhzYqg2zuaQH6FLJahhEZi2J6dYqUHbig4m40s6dM4qppjBMF64nI/xHk659mSwiQ93aOO0lgFrRBuvASoiRIB3'
        b'oyrPsAhcg2uJfwE1cPgM3qrl1lsJEgN3P4wouJGyET2ZgXjbQHSW2m8pQ8eE4Qu4ATh/TVwimN6eqI3Dh5Sogtp/+Cbag/aDba4pCw/VROCt4RiGJ1AtrIhX0hajLfia'
        b'J9R0AG0mhiTUJAoCBTEjrxonUmjRlYm4CmyPORZifThMD1SHW6zEFpuege+ECTN02jjoOo5Rynm5YlQnw+0XjENpsS0z3yQKiBBKv9wEFesD5MQ9kHJ+QEqCg3IJ7Uol'
        b'ClYJ/0F4jHCVE9BjFUEuciUpb3SQq8/zPZArSb0iCZ0LC0nCm8FSloIt3MpNXYjKB+I9tJosqRtxEY+U3ElcvjyxDexsEFMmrZHZpTVMJVcmA0wavlZm55sYu7SZLZMv'
        b'Ygo9BMbKlvZjGfJ/CVPouRr0Zbuc5LNLSQmTGANLcprL7ZLiMBNTJrFLmrhmZhazPGkZV+ZRpiDl2z0qOXMZrUmAuwV2aRPfTMtoEmhaZZlnDQ/pPO1cNm9i7IpjbAPL'
        b'MqvmFA6huZQAn7LGwy6tZAFiRY2c3FWyNKec5pR3yZllV5pLapRiDiesLGUpq6LIlZbrCdBsr2FrmBLGvB2gkRi4ZtbRLmca1irN5iDd8RpPmu54DUdK7ZJKCimu1kho'
        b'CvjtnMLAN8kMgkGyEQzOWUwlC73rZZA2yexeTXKDzCBv5sgbu5f5VYOH3cufKfOqllV7gnbHGxSQS27nSa4yFbRbVcka5Hmc+a92lcETxkFV6ON6K5j/aVCSuuyqZtaf'
        b'fOMMXmUqO9cIdi9AyRIo4V5mUNkhfQDw42wO0nkXDrGzdi6Ph2+9Dd7k3vHe3+BjF+96ueUPNvQS89MvAqQhtXnbvQ2+Y8mvF6SZZFfRq7eht11l9yLlkW+FMrs3+VI8'
        b'3e5Fnq3imJI2+EAb/PIEyGW2+5C2GfqUMPCUJj5Bnhy4kzvfFxnEJ/IeWtnL4A/PjCGgigti7L0o/D5Qe2CNF6lhpcLu44TBTtq50cravSvZDazVU/wFeRSkW3Bflg/m'
        b'eKF25H0uXN1J7HEO0UeNa+K9yQESWi4pY+3sSmYbtwrEm0euQ7Vsl6enF+oLjOnpGq6di4hqZ61d7W7FpHyTxZpVVFA85QdSIkdpdG3/rFxjVh4YXR12WUfC+7y6yHyf'
        b'Df+CwHVfUZSttpYWG9XBlm6ASpyUrnYC6kmmke1ENnMWrgaArmQdQGd3gAYsMIzKxZJfYIBmMhv3oxPmgYyZiOr73np1iT7fZlQDVCHBFg0VsPcDLcZVNmNhllFtshoL'
        b'1MEm8nlEsGXE/V70Bbl1vRLotbdbSmfu+x7qApvFqs40qu97G03WXKMZWg2dAdcvRCfPfXbEfXbIfY9gy9KIiIjl8J4o7/d7hatziqzOfpoAfxplu8RUaDCuaVc8RgCe'
        b'TSw9eAW1WtqFrKLi0nYhz1gKxi/UXGQwtntkllqNerNZDx9WFpkK26VmS3G+ydoumI3FZnMo6TCPBVABLUnj2+6RVVRoJYaEuZ2HktoFggrtUto9lnYJgcXSLrfYMsU7'
        b'Cf1AXpis+sx8YztraufhU7vUIiZg89rlJku61VYMHwWrxWpuF0rIlS+w5EB2Aka7ZJWtyGrUePWoev6WC+iNyS4slTvR8RUy3g1EhnDECcqxKirTuAdyQe6QeD4ODVbJ'
        b'+sN7BU/e+DtkIcjGfwoPfH184Y0P6wt/flJf+s0f0hMJ6cMKnBR+feFJxSo4JXFYcHL6RsUR52sgC7L1AQdl+3H+UCKUy1EpOCcW3SGmUxJu0IXHyxgVemJ+Oj/ePq+T'
        b's54IP6mTLD6CCwgrzs40MVQA5YCw4ssEO2/xWiW1guJK/kwg3A7yRKTZOTs/CcjHHALijwUWH2IHURHENHHALPkgphlEDoghAQSAQISFZZRdyGGhPAHKDgGRxRNBAiIi'
        b'CYiQiAaJgZQnMQhQBk+e4BdEISlnVYwoYMypBqF4gYEIZoldRuuSOr5LxNppOdwkhj4LjmdhErNKaqeErZHogI51ZDTpkKaQi851R95pJOYZZKB5i9HazusNhnaprdig'
        b'txrNxLelkbfLCA4W6Ivb5QZjtt6WbwXUJa8MpiyrOclZYLvcuKbYmGU1GszzyLtEkln6K9jm5gsl0Q+GdGe5A1mHaSRwPhTZfFgHItBhJ+gSyPrAN4JKDhsaHUQ7cxyz'
        b'7Kg2kswAJhkTxEm7MDLXuxsfjuhmbpDaiYJMa+s23cqQCddsT6ddY2dTHQ7zruaQS7EywKWGjDRbC6J+JVMsByyDjOa+gBle8IYlYrSS9QS1gAoqwAkQf2wNX+NJ7mtJ'
        b'TI0AgJDqFQCOMlvucmF62DmCQ6k9xNAQxCZ9Sj2gnxMgBDvRGJi1C6FintxTbSkUUJ6DygC0SjaPAbDgzg6AlPGFnhQ8KSD3UHIHbziWKexl5+m70TVEnwEyIFpWjZQg'
        b'vUPTAsCh5EFlvJ2WC2ln10gBWXnQaYRCKbmH9/TJLpgXEdkDRETLsQuOMsaBrukLuqZglWRzpXks6JEss1aAzpIQ2WyA53USEmoFpAFkaWdJPjoarA7wjBi67bISvZl6'
        b'LfkcwGXgqua81ebpBMfiRWzscFQSGS4ir4Eiv9Fs1sgfmUt24K0ynfLHYqi4wDKdYG0UwQaCsZyKMjZgjsC8AlmunDBOMAQ4AdgYGPT3fWVy4o19oOLWRumzsozFVkuH'
        b'zDcYs4rMemtn92xHVSCnMwkQpEVA4TTSh75YSV54/l7Oz7fLSAcCIYtFZrka6uECaBzrnBXjiSAYCG3syymC1vZ9eBucqoWeFJdP7hW/SyzpXeDIHJWNZh2eAjUvDKXT'
        b'2ZPxBnQ8IVGn04ZopIwnPi1EcPiYMLqby9PD8WuJhYuRSQMcS+N2ykRfBtC/PFsiEl4lm8bT9zTczcEdPIAsSSgh+SpUMwKTJqFkKWnv5Qj9m2PKNyYW6Q1G88OnjMlE'
        b'LmU5EhrrIc2Wumhd+P3TFd2nS2Q6G/HKR3niI84IFmLW84zKAzej07yPHrfaCOb663EzmXWi8XViyvDpkDYFrH6HA+LKfIZZFiLDO8EMb6aBWb0ScLWYKSQEb46M1eLN'
        b'qGVBSHzSWnwTrPeIOG18EjASb4/J63C5jXjuB6Hr6FKq9rFYvEUTn5QIqYlXITkxDp3C1yFtDNotHYYP4+umqTEv8BZCrdFPrfwq44XMU8ZT+sVP70XXG9v2XtioqWrZ'
        b'NP1g87622rbKlsXC8znStrzACYtfCtz8Sbl9d1/pyFa7h0U2U2aJfp3brdpdteWu8qCJ+ey67+3t5579m0Yi+jWeQE+NxHUJNKJKGMji/cvQUXQJb6cT1ngn3oWPhEXE'
        b'dfZFkFCxFcJwK/HhoyOx4/ElvEVLQtBWOTww6Kp3X5uANuFWfNJKIx82oyfQ3rAIbayWY6RzotExLgofn0ynrNFVtC8rISI+KTwO1btm4yVM8FwJ9PJTaXjH487pi0eX'
        b'qV5ZZiPI8fSCIoMt30i9FcRqYdYz66U5hBURxiSnmtfaQd2QNqJTbteskMWYnw1XwiE63I+ShxMtZy4m96ucUJmJE9dAqJYQK1PBVPgf7O7b+FV4upGUa4pujpOk3KU4'
        b'C/SqcJGW5PfFZEgYN7PKRVoqkbTwJvRkemfawid1KkJba/S2kZBiJNqBrnWmLXRBFfcQ4irC22x0qmRfFN7bI3E5KetxdE0kLnS4+Jcngwm8HjnOyWAwUtnsrkapfFK+'
        b'viDToJ/yOOsw7wTGtpDiON4ns7jaV9wpcA9vT0DnYpNQgwt18S4ykfc4PkLm8uhEHj/K14J2zPfF5xh0Fm/qhcpX+TnmmfuZHOElW3BduOjKG4X2q+bzI8ei6k5NkjBu'
        b'87yUeYrKEkfG2sU8+RoYxzIBRpinIyzQUeXXCalu9z2NMKnKpcm5M88JlH5XcAlkjiZCnIRPjQ0jMVoLcU0+Oh6p1eCGxLiFrpGUMKjJqMBPkaBk6pP+ebyEkcd+ypEo'
        b'azx8IENHF120oAudChXjWXENnXUPxdt04SSmtWC9R+CwWBoPPRbtW5MAvAq6P2leCK5dJHLOea6aYbSWzcUncZsMX/CZb1r+QyRrMUHGlIzhZ+Z/SUOGXsiO+ChUn6jP'
        b'z87P/DojfP7XGa9kvpj5h8w4/XbD85nnQnKNn0/76M0oZmEYtzC6ckF19CffXoza2brwy+hR5eqUg8crZx9khy1SvfHW3cYXXrt7e2Pb1pF7K6IHMGsaAr4u/qMjtmhp'
        b'EtBED8FFOYnBAj93EeV7wHrr0M1uvLOvzYCOA+9E1fiU6Aq/JqCDCRGoqm9PLDLNEx2ivHoaqsRNYnRRQ7KjPq+cfvgiH4ir5lNH+KxAD7AUaQq8NSwCVATfdTxbiLeM'
        b'SaK+6eIyT+d3Et3qifajM2M5XB+USRs1buIE1/S829x8Bb6NWvGhwb+dSavInHt6sRlMd2I8US490MGlmfWcnCqQxMwBXi2UEz8yVRhHd+ePxjXGLAd37FDBOpcu0r1E'
        b'1O06lOFfm0dyTDepXBkoIycrLaoIl+jrYOTAyu/34KZeDl8LoM9+K/NwcQ60E18nocrbx+M2yWx8Yxq6EoxaNMwQvMtvJdqUnU+AlEcHCt/5fvMYz3w44r+5qyOXL/wD'
        b'Q6cdJ6XvZVtljDqq9NzY98yfLT8lvh45gsxGsiHfREX0+3lx+sJNjKmkcAJrOQ3ftuf+3GfLRFVllM+s1fkfe8e2NI6Lu//eYJn83uaQnezxiwcCa5N2RJfvrHzWb+gr'
        b'n5me2frd4GavLQNeNz12duOEF9fMfO+N3We9X910puqZ97/LF3wvtod+OzHl5oq6QQVD5m2bs+iTS6HHjEvvf4P++bL1+JtnS46PVm4a8J97I3Ze0VV9/dXTP9Sckk6K'
        b'DW2JXvfDkC9u9Npztzn4/MT4E1Fpy2LeW5absqSi4a3iB/zn/bWl/07SKGkk1aRM9FSXyRtm+gIaSnVeKc7/NKmKRR3Go8h9RoXBW0UF5Dg6gbb1QIjj0W1CiKAPWYlj'
        b'EG3Hh/xFCnOOJqqBgYORFBl3ND4/xiBdHodbrDQ+dhs+gzc6lB50KFRKtZ4DOpGqq5dkdR17CdNvNNDwAQHV6VCLmGwfatU4OAnUM212nJZM/MiYPriCx5enoAN0Skey'
        b'QgtK3Jw0pxqHjsahc6KCd2c4OhYWi8vxEdpwYSyLzuNt6ALtvOn9RjoCEp2xhktxKwk3RC34AiV6dCrV0E1CzR9LBBSqxQesRKsag64m4rpElmHH9e/DAHM5jg/+kl70'
        b'+wwgqYtveLqRu9tEFKh2Vqdqp6C+EylcFWBz+nJSb7A8OR/On1074BfZh0PZo5pbu9TxroNJPLKdDMpfCbkvdvEMG1xWuSt/A7f2oPz9MnTAXKnHVZHueJGeDmZ4+iqb'
        b'Pl/0uFMVk1bV7kVWyOgtliwjsMF0sV0ev6nTW9h2D0chUABtRCFcMkkjKN9hOOhQTjmMpUF7M8ZPexify5vLMRPQk1K0b11iN2NU7vi1EK3AaYwawcB0uKSImiMBBYcz'
        b'8Bs9Opmc2W4mZ4reCp1WCB2myxLcSido45pXJ249l3JMVWMaqOfhUJ6EGjkoTxJQngSqPEmowiSsg7o67ntaxUWUp+7qsUQnKnlHkqK7WJ6gGoPt2eyDnsSbbdMpmWbh'
        b'oyBdQ2KTIkC3cViE2vmgDKWGEHfeQrwHlcs7rxxhExhmVG9vD/wkqjTh6DucJQ2KCpjJfpWx/OlGYibGPrmxrbKt8vg+E5sqy5M9Lntuxqdpm/puGvKm6mrfTeGfqk5k'
        b'n8j8wne334nsZ4c/q1oQIW1c7B+215CXfVpfk3NeL8+OZTP/EMNc+dbvi9QfQLkhwnAdWf0FDHUAOtRljhrvx5etZNY2HQB1WnvoGLCb81yUNYTmHlAwhXZGAt6KKlCt'
        b'uCTF18ijs6gKn6UMG/jqBqILOlbGoEp0lZGj49yaOdPpHLiHAMy6G7teg64SmxNdMFAQ8NmBUW6GbZwVHZ2E66k1is9q1oXFOtkhbh2AzoNNvsmpwPw2InGPJs0G/Esn'
        b'9iHlSv4OrsSsVwzxUwosCWnxA24k/H1tv25IG+HKK1KqtJ3Pyre0y7Nt+ZS024ViSNsuterNOUarG0f6FXULWNk6ck/Crs3l5FLh4khlcDnSWYvp/0EPPOmXoNVwOp2D'
        b'K5lXk8sa0hOelGkUGK25RQZajbnU2VW/IBjMa12g2eFyiHXYboTPDGGp82Q6vojbOriM3H25Fb4l4ZiJaik6mYjOU7vjlIFnBPlRhqyvuz07n+nmAXc5o6YxXZccZctc'
        b'S4LYR1oSlNOTW7p7RE+QzhZNcPACvoOOWgCNL3uusuGroElcw234HGqzluArniWo3rtYiduIT++EBLei7eicjRh9+Fww6CGgIibqcH2YbiE1puOm4DNwV5usdS4QRedw'
        b'TXgEaptPVlyhy+imAt+R4KZfXdPK02n3/wdrWnvkhnQRRDk6hK6HMf3QqUTXOELaBTyuG9NXjAs9vM5OqF9sIt4VFg3Nbwlhmb5om2BGrXNMl3esESxkmmXU+2/12dzm'
        b'VR6lFN4fFLKXG5n6WHFFbuN8w6Ycz8dTP/q7bvVHt+oqnpm7atnF5zLntf/3R8Nvjr+0MOBEfWrNOVXl2x++M+rzcX8f9Nwh3/lrTjhdYvtxowGsI7w5HG/CTTCO6CwX'
        b'jQ6MpLpOBN7b18E7QnpRZSq9P1Wl0JaF+Bh1VuDNVnRKK6bxRhX8SnaAyNa2onODIQVZ3LSFZ/D2IcJ4FrWhRrDgSMX98Vm0k6wYQDtiOsJ2cEX2r67Y8NQXFxuBIAmL'
        b'6MJ6lHME6uWS0+Ubwn/WhgL7SM83ZRkLLcb0bHNRQXq2yd1qcivKWS9lGw+Pgga+We4i3Eq4PNOZp/jc6sEymk9pAJ2ZmJCsBUVyq3O0UX0ydS3AryjlOttDeIdjSQVI'
        b'jlgwjdpoLxvQYZ8CfAadpwuYWHwHbwijCuslz+gxHCPBh1mggR2ohspjdHGsN1BQ2+oSfHmVUl68SrlKYPwnoqZEPscA8piG3D45drAFX8ZtHl4lXgqVHGTQeXxxNSHX'
        b'VRJmmK9QVpQi+r6aC1B5AhgXYENcEQdWjlo5tAlwp802lRR1E+A/jc7gHUDhtYmh8eHoNN4J9H9kdXgIEfSJunCHA0TuWMrLMugYuuQ5E+/FT9jGQxmTH5/aObsrK7qJ'
        b'KnrIvjtfgavskJsoZukTUSuqK16Ftq7GV/E1YDrWsBmg0l/DrfiaDZqTKqCKvChRWdmBDg2nwO5JIG4CkNWJsjJPxhtv4+cPHUpXsaLDuGlmlwJLMshDm1IhZYbFCWjz'
        b'QD+qsIvRi0djotElsIHu2JiJzMRR/rTnQkHMV+Adydo4vBtdiI2TMaUK5WQOH4YBr6fuHnR5Cr7jqSXR8AmLxOa68Tx0hTK31IDluEKGbuuW2Ah2cmsWpEoZLb7ODGOG'
        b'oU05VA5cGOLB+DDFyyQZGYnLc8eJgZK35kkZJZMh4dUZ+f9Y6gMaO33Np5GQ3BReBTIjcMIMMe0r00ja62EKdUbixf5TGcrCBVMvooWEEYdULXVC1eLrw3qCsQhUtzK0'
        b'F+80XR/zJW+ZCvRRHPduUspEHT/Sz/7qin+MmDqlInZBTDET2rfvkELG92jT40PmNz7Wvtyj7y390HsL+rO3XpI0faLoXz5wlfLw6h0LDaWTL0UXfbJKGr1G0u/Vu4Ob'
        b'5/J9X+z9KYrzqhj7hx/GKa5PuLotdVhM4t7Bn7y4oc5WuSfT46Ufpm8/lrut7+UXJg3+V8iLLc/a1n7dlp3z3I7dn31WP9b4j6QnPPbMv/rt/AvfHixJ/enczg/6X7af'
        b'U5k+qXop97mP+7z33HvS0cKTz4/PG9sUFKivePOlvxX+NWD1V3/8y4kDC/V/L8g4tvv8P+7OujbN59vTwe+PmFz55U/7yvT/9e2ft/X7oXHCmPiwsZ94THnJ+9mh7Z/9'
        b'+Grmccmd3Yov7m2Obo16bOW8ofU3/nPN31osRPzT5zXJ+gv6c4OmTP/3W6XNP3rFvfGXS/9Z+lNM79gdrzU/G/Cy/4PCWbbFr32g8aZMN2EIOpxA9iyoCydMg2dIaOQe'
        b'fJHn0K4plF/3Bxt8P/AYluFK8K6J7HQWNVElsAw47y18cWCHIgha4K0EkVNv8MKtCYmhEeI3zzR8Pp8D7r4NN4jfTwYtoUuz60CLPw/jTJbi1XFluJGlUZxCfkJYMoGI'
        b'KCYyxhNgqMZPcfhaCTpIKw9BbT6EkWUv62D0+WBN00mXM76oLQzXxIXHUWEiYdBO3OI9ic9G+8CoJ/UPV49LILYClK7RAl/bogNFOyBRmOa7QvQ8nA9eSYJVw4HPOONV'
        b'tXp8kH5U4apcFXAnqoPXyRhBy6Jz6MgwUWs+1h83eaGbYfFJYM8Lg1kQ1pd8qSegd/pQRwAs4cd4C6ovSgDcDkBXhdg4VCUGnj6Jj+CdIDyNSrqSlYpOXI+viYsbr69A'
        b'1a7ZpBkxLrthIK75VT1W9lu9BH16FHRUPC4jjIIVBaQwkYTyKKmQVHA+nELhw/lyChbuOB/ehw3knPPYSroGUsH2f6CkITmcGAT0P0pPH06QKe/TUJ4HgkT5s3mjUz63'
        b'cG6C81Ga4BZpRgq52VmUBt7rQZQSXoQu4IOopgdZmoYuuotTCbPCKke7gG+RXQYIgRTIcnBdyPKEDteRNZguRdcBupXjOh06l+jwBy8E4rrC4eNLE2i4fB90LTlMq9MO'
        b'Q0dCpTDUTaAl3cb1WXwXNdDfqQqugEu3Ff2Ma00/22lVP1fdJ9vfNakheaRJDVDBPxwGI6xQu/2bb8wxWaxGs0VtzTV23ZsmQtEpbZxVbbKozcZVNpPZaFBbi9TEiQwZ'
        b'4S3Zf4SsVVQXkYi+TGN2kdmo1heWqi22TNEZ06moLH0hidgzFRQXma1GQ4R6kQmsIZtVTUMFTQa1AzUpVM6y4YO1FEDoVJLZaLGaTcSH3QXaCTQeQk3Mwwlqsv8OuSOR'
        b'g6RIR/HQwh6y5BlLSXSfmMvx0CWjQV0CfQYw9ViAzQIfxeyu9LNnxM1MpV/UJoNFHbLAaMovNOYWGM3auFkWTedyHL3tDGzUq0kbC3NIVKNeTWI+CTjOsiLUuiLouOJi'
        b'qIsECXYryZRNc4kdCmOVqScAwVjB2FiyzKZia7eGdPPfqJiuFounjq7Vy8ZH8ZXUSOes4/xFsaCLpsbGS+aPH49aNAp8o3Q82oWuDJ82ZHwfBjfiU8ogvNHSjQ58nBXM'
        b'70wHjIMSWBclcNXe2T7/2wk9wki670ih1UE6ymS6B3J1D80QQWRcs4uPahJ2s4VJVd3XVUkcS3MJ0zbFXnyJt5C58kn6G19laLPj9EK7MvvzjC8yCrK/Zi5ON0yYGZ3V'
        b'NzVo5rZc2dDY2ztGb71ROXpA7OooW1T5rP1BywMz7+Xdvb8ycFjQ02v37Q9KCKqzBgU9PXzDvYCocOFSfqDirxMWB0RFGDIMn2dI9/m8/PQ7HLNxyICD1647VmyDKl2P'
        b'zodpQ2K1HNpXDBxtP0d2XrpNXexs4bAw3ECU65l2wcbiWgRi7bfPeUnSV5v1xV2mukAK9RXYQJAfxGPtBwzelwaOrtWYHczLLRLKgeZub0iJjuXfYgDiI3uHWlgxA5U3'
        b'1XAJAMgs/V3yhqnw/6wHiUPMGhnaj6rCnEQhLl6dhW+4WWqorkMUzfbVRMaDQjAHnfI2gQFz/eFxQRNE6mB+1xLmbr6IngMXZDrbbDLi9fgK2hUdFTNqzMjR0egaarVa'
        b'zSWrbBZqGl3GF8G6acNX8CVveQHeolSoPLw80VZUg7aAMXMMX/PA5/qIFka8f3zEdiaEZXwyQvMKlopWw/ixsTNW8WqWycgIXZeic+D5m7cCJVQDGbzm2T7PNfc6f7c8'
        b'ykd4+tarBxYw8k3ZnzOeEdFyv8/X95n1YuyE4FOHkqwHi3enHIt6aXPWX+7dm1kRtz38v76Z+PSbMVUJR46Hfbz+scDEETG+qxPTTPnv+bzvfeZ5vykfDwaUJrpeBjpb'
        b'7DCYQctMjxYdCmiLOC9W04dsR+L0RxBnxCZcD2rxsYRfmr35tfV98nRzkTU9kxjezskOJ5KHCIDYfhS1Sbz02vBHQm9Hcc6ZGVeI7S+5JDgxRQdyb4ZLcFfk9n2nB+Qm'
        b'iOGBytFud+Teh6q6+CG6YDfeHIlqk0eN4ZkSVOcTgbahPRQHxkSDOSm/ASOfoVwaOpYRN3vZhZpRC94BiBmMd0cwEfg2vkGTzxkLhqZyKNkmLP8DH18Rj/42QmDkPqfJ'
        b'JnWJS5P8RTyiX35YBoat8CMPGBZeFTdPfLlufTyz0+8/HMHF9V4TxZdPTezFqENOc0xxhvLgoEhG3JzrshzXp4J+vnPh6KhAIMvNAiOdz6Kz6JKV5oro14+JCZkphaL6'
        b'b1qTJBb1rqyVLeeZlGP8B6vf7nvQSBfAzkMnwlLRKQRmAZSG6yUMn8FOQRWoyTYaPg/C52mcnMuEB/MF7JN44rAEU2bkkhAaxIG3hhGbANWGKTRrDHSyelx/GQOwqpk5'
        b'+eF/WxC4voTJJ2sb6hXD5fIlTNSJ4BurdvcbF5LTb/UyxfpWjjoBbDPQPnwJZE58RBKTFJxOwR7ITGCsk3by0BZz5KxlYltmjpnKgJ7tk7Ck3Lx3mT2Fvgz3msLYZ70q'
        b'ZaIyfCttgWLKlCFaNoNj5CuHlFsCBxUq6Mve+rfYyzxTHNqvoujtrPfX0pfWvnPYnRyz+F+KirzFgzb60JeCxo+N4piUOdLysr38QZ6+3DbSynwDTfxWVl7yduTp/vRl'
        b'bckC9tS6CuhzfZiXT4xYOxIa2RCeGVeYV54TOKy3mLL/8sXMdYBsW1j52sUzGpbQl9stQ9hEjsmds7q87O3BhSH05ePsIGYW4M8raeX2vQOjdfSlZUQi28Qx6gHq8ry3'
        b'+7wgrin9nwEBbHjfofA6Y8CdoePF2usi/sg2ycIAh/XelaEm8aVn+DNMjcdtFrDSIzFtiKOXAsoAKWdImZSMEmERL75ckvAec914jIWXQSG6RPFlU74XE5j4bwFeJlas'
        b'TBZfXlq+iilnSWjIB5lvxF+wmCynnmEt++GN7qlNC1PiGt6Y5vPy2VdKIgs33as/YHx7Tyk/d8W0QT6ywmbpC/MTLm/zOfWl4enRATHJreOLZ/1T9pe7/a5/w1zcsnFj'
        b'/B+er1HkGLPD2yel/fvFMbKilpN/+deSqf8I+Mn8WVPT1E8Ht5xI/1uM8mzxz9/g1PAJU7SZ7KLXTYNv+61QpE3vV/An2YwxuvyMT4bKdl3ctsF/wdCRpT9/tXNx4sgL'
        b'pqRD8V/2Rvk+ny24+72w5vu4Q5VTWtL6L7bGfxm8fNLin0/mXdhWFHJv885vMo7+0Pf1ko8+3dQeMWrZE75Xj3y44S9HmvwerJx5vVW3/nzojLYTh04fSy9SfTbPK/vY'
        b'3Y9ih7etePzdU/jaXm9VwNzdS77+Dv3PF5tUn7WsPDh76H/FJV/f+NIhVcTKZdOrRp8/+qz0reIBY4t7P3e96t3rlbdGvTD5QnH6mP9Mu7nmc6+BT57O+veuI38MUOwb'
        b'+7fk2LmvmtYbPi/4/ueA1AnzV7+z6nlhkOfNgMufrfb7bNwXP2ietA7e2p7zwrefXls9Je+7oGuXNE+s3zf+Y8xdPl6r0e/KX/79xdeXxq/99r537Ieb33grUSOnwUPo'
        b'KLo2IAwd6+u+SFaLDqCL1LGANgPD3DY1LAzXRILxjZrZlD64iQqpKLwHnwqL1yZoQzPRfp2EUUo5/GS/EVQpM6KTZCMWh5CakcKIPvOjK6lStmJOdFgR3gdsOQ6dFchu'
        b'YkNW9afCbRo+kRMWoYkXt7OUMN6yQbicL8KH8GnRy9KC7uCLLi8NenImddQQJw3aO446l5K1w9GRmJ5CnlrHR/7GWUKNz2+PeXhknVLuFJpU4ua6SVylv8D6cz4qTuFc'
        b'k6tyrLMnoeuB8N+X7Q8CsD8n0C1SFGQlEuvL+4OUVrDczxwn/1ngBRp9RRwg3M9KXgF5BeoIER6s7ftwCS5qpBK60qBd5jAy2yXUcnQT3f/7NVug9daTe7qkocEl8evg'
        b'4ttV4od+3YPEJxon3p+Gz3RRZzMAMXsW+BIGVSNQ/24L6Dydl8T7cYW4PZ3LG+zmOEFbI9FlCT4LFgV1faPty8d3zOHRwNcluNkHV/EDl80RZfgA4oUOnC1jQOTLHNzx'
        b'mxgJI2cWjxemZShnrekvvtw7S0Zc05FKdUZi5OLJjOmrr9dILMfgS/Tei6O3JKk2TFPOWSrdpGe+lWXdLg/4JiTizVbTOOb6goCGuInXXjuQNjJixZ/Wlf30jPf33EZ2'
        b'UIhF93bxi7stEdc/2Zzz3jfbF93+e17885OWP90vdvLfn9Gc2y4Zt2/x3IB3z6x4Jq5f4nerfab+XRJyaP+ZgPnDPb81XPMp5otmXfluVfUT1z/8MUFya9aDtuj2iuWh'
        b'xz/991t/1r7+TlJD8Linjxx9wHz7caRl8GiNjIY5FeCduNF991m3nWe3ZeMLE4NFHnMcteEjuE6Btrk7L0fjjTQWPR3fXI/qUG2MuwsMb00kE4eHhaKEIurHLMF78T73'
        b'wQTugK7P8Q3l0SkduknT9Meb0RWSRodvwUg7B1KFzvOz0Gk95TCPTwBw6iK1aC+q0mnx5kSNlPHuz6fjffOtZE0Wbg3DZ1DdaLwt2aHshDuZSD+0TUBPQJsrnQak//9z'
        b'9vDIzMNJwZR5hLsxD6GXnOW44axyDg29FBcscmQlD9kPRkUYxn/Mja7SyB5emt7/14BvddE3qfnHzu7RMT1tKUdEzBzcNNxF3BzjvTJ4DJ/ti7f1OG1N/lmUbEcskoFN'
        b'4w1cmmDg0yQGIU0KfzL4k+cwaR7wq9jJ7xQMknpx2y8SOiAYpAYZXR7jaVQa5AaPjYxBYfCs59K84FlJn73oswqeVfTZmz57w7MPfe5Fn32gROophTJ9Db03ytN6uWpj'
        b'XbX5GfrQ2nzhm5z8N/jXky3AyI54AYZA+q13D9+CDH3pNz/Hcz9Df6ihj+NpgGEgPPkbBLrUbFC7KlFk7En6Qn2O0fyhrKunlXgDO6dR0ziQTol+LYfJQtx+1PdqKC3U'
        b'F5iIB7ZUrTcYiG/QbCwoKjG6uRo7Fw6ZIBFx9jtcmaIf0eWipDki1Cn5Rr3FqC4sshL3q95KE9ssZK/yTl5FC0miNhYSn6NBnVmqdqwCjXA4ivVZVlOJ3koKLi4qpH5j'
        b'I6mxML+0s7NxoUX0P0NVerOby5Q6llfrS+nbEqPZlG2Ct6SRViM0Gso06rNyH+INdvSCo9YI2plWs77Qkm0kzmuD3qonQOabCkxWsUOhmZ0bWJhdZC6gO/CpV+easnK7'
        b'er9thSYoHCAxGYyFVlN2qaOnQN53Kuj+gFyrtdgyITJSX2yKWFlUVGiyRBiMkY6Nvu8Pd37OhsHM1GfldU8TkZVj0pHNA4oBY1YXmQ0P9xBNYqh7UhBXjjmXqpVx1FP6'
        b'SOvG7ld1d0YXmqwmfb5prRHGtRtSFlqs+sKsrtMF5J/DIe6EWvSJw4MppxD6cHpKnOtTdwf4I+w9KdXRZWbz8eYhD1sJg2uGuC0zQ2dy6aR/CVjTu4hG0muZUycJiQ2P'
        b'iMBbyb61Y9Ae6eO4Cm907BWe2VuVgGvRPlSTmKwl6zHqk1nGFx3kcQW+ge6Yzn8zUrCQddNnehWQpWghmeQa/umXGbGOlRQR/iH6eD13KSgg6qWM1VGRhmVPX2xs3nGj'
        b'UlN3pfJG5cg6bdWNPS2VwYcnVw3eW3FJwjx+rdeBmRqwHki8hZcO73GXyagB33GX3dDcCjHMphVVlVLJjM7hWyvdBfPjPlR24wPoGKr3hDZrXIpEH1SdipsE+TRcRedf'
        b'h01EG8NwwzJ0OzZGYHh8iy3El/Etao6gxtzHoC8We5GeYOluV6gCnUykBkcu2o924LoErYwpRk1kE+KELCM1VGLQeVxNdrOrWBEbM2o0z8jWsng/OpAmai7b0FVUT+Be'
        b'54lrkhKlDKiDLL6xdMWvBsW56/npJsDS9PQuMT5U0/egGxyCUPZn1wZ0Rt8IZz5RJReDm827GOZXlz+0cGKyjijmPaRSzum9rnD+9/u5h7jBh4Hx8JVaRKG1Myuda7U0'
        b'JADZOZHVwopgdF61ZbbApYFzbB8qZbpV6lzUdT/ooTNkUA1vKMp6JLA2imDJ0x0GjfnAQ2DaBvCYD8LNfT+3WTLnZFvEI1WW66yMcFyTwfLQyna6KgsnlTlVuh4m5bLy'
        b'TcDJtRZg6JpHA8LRYs9045pik5kKi4fCsccFx1ACR0cOIo26dnzn6p0cnm7qRzm8YxvTaokbh/+dW0p32hXGnbeSGXAbapOn4nqB7JvFqPAxtNU4lO5h7ot3JqMzLJkm'
        b'OMCUMWVpSeIG2bcGrsd1ceHJYPSBQh8tAI+o4+JRObplevWp7wQahf394IwBdS94Pa1WCoOLV3uNz1XXH5f4DVsZdcG+bNMXMaoLA+pLwvdZb+f3TxnntePHuFDt4/uv'
        b'7275aEmldEvfB4u/OPCP3pXxU4+Oy9u/bPST4YO+e77+T1N8/IP4P/XRKKjJtGg1aujEMTu4pSc6VYROh4n7RVfa0HkSLDIV7YgTpwHwLQ7Ves8QQ6FbE2ckhIfgyzlu'
        b'O4UN7UO/yabgIw73Ca4LZwQdi1oD8W3K7eSzbS6nDD6BDopumWIwn0ilQ6JUAFo53gDf3Zgdh3aJEZZnSqYn4IZIdErAT6E9jDCGRbch8RbKf71QU1GYNhbf6texx/VG'
        b'/JQ3zarBlUPJXoRhWSLjp3sRomu4gQaGK9BldABdAMOK7IoeC11DWbgvOsPjTbgxrdMmZ4/Ico2FWebSYitludST0MFyByrohi2i24TO13XjeI7c7qtKHm3/QsfOsh2M'
        b'9zhc9vfAeHvYVvOhYPyfqVQ5PapUM3P1hTlGMe7CqQQ5eUAXBQv0pEfVrQqNqx9VpSLN7b6mVQB2Jh49chkdQeVkm5RkfJbvqvbUB5gmnfMXLAWE5Pfp+7w8WDVEwGSD'
        b'xKB/XF01TbVt6Hfh7MKUmuPx0sGSYA/Fvg1XF7UW9V2UfGRd27TH/j2mtPnsxs0vDtgw6d2777dasr73SvdZPWyNJbDt2X6HP6575v335j+/p+T6YzU3En4U/u3be/h3'
        b'W3v/UO0/9YvjGg9Kfr1MZaBOxMbgffiQU0dpQ/WijnMRN+FqVJc8D20jC2jR6fAQFnhXPW/E53AL9XCuwqfRfpEQ0n06kwLa4EtJLRSBhkh8GHjz1EyWESJZdAntxbV0'
        b'U0Nc74cPi5uyJiSj+kiX8oh2qZko3CQdj5tRq+jcPTkfnQB+cGkwUYyoVjQQICWsYARqQ9W0i9ENQ4c+FYAvUAjGrkQnaCvnop0upQkfnEzjxTJQG6ZeGMJEUDm+5GQk'
        b'aNvY307K3lkUHdOduNODEqWIVNFIsP4P+nJrB3Yhoi7ZxZL3PpSCzftcpHsSLsd7IN23eyDdX6lVw7dLc4ssVpOh3QOIw1pI9IJ2qagfdFv31Jm8BecCBxd5CzSu6tfX'
        b'O5G4qhlsF2uf/JtuMBBriZCkm6IhWpouMf9QuhYbIlJ1LNzHzXJyh0x9YV532naxA0e7xZwp4iNkDkmwFYKdqo2b1UOwkVvgkjMnscpJtk6BSpqe4DUbrTZzoWWCOmOB'
        b'2WbMIPFG4pYMhnB1xhx9vkV8p8+Hl4ZS0HuI+lVo/V3sideZ3gq4y1vIzlKDlgZ+lbHi6dfuvn33jbsXG2/sbq5srhxf17av7ci13W2bRta1bGreOvhgRe3gqr/6VUjk'
        b'B/YFBW0IUgZtNr4YFBQ0Lcq3JrU886CJSXzFayGK1PBiGGZtPJmNScb1aIuqE+/ITqCcZ3ARcnAFyhMWzUaX8FWQzsTHWrQMH0pIjEO1yUl4c2IEaojUkuBTDdoiWe2J'
        b'zi2Y+9sJU6U3GNKNmaYsC9VzKV36dqJL1TQy/TDswdoBXaijc07RvJGKQvMUubSQy+nO8tb9RATBLVmxKy0l2rNwudgD0b7U06LNXwTr/5Qs5/ZElvOplwwos1BERRJY'
        b'50afbv6x//9RKMkWl5qsFj1bVtERRk2PbFOhPl9tMOYbu0cDPjptLv/6Lktp84ua2C602WfiQ6nzV2hz/rtAm0RchtqLRMrcsbQTZa7yFn0T+ybqCGVOxMcdxAkCuxFd'
        b'tJIV0Ho1rgmLx/W4PjIB1TvocxcoxA4anYoaZL7oivq3U2gv0e36K0Sa7CDSLrpdRLfMYsnnuhCj+byL9lrhcrcH2rvdA+39am2/cm4MW824nRvzaJt3E3U3sweqoyhI'
        b'yaPQVpAJlAZY5+aq7nAAZ9nMZpAP+aVupvrvRUjt2tsc3cfr4A8fk6NpWhubqZgY2QMivh7VGRWDX3JDxSDm7c88z98b5RAT+EbIcMA1dDO5q4Z5eygVE2oGn3KJiWR0'
        b'gSAj3hlKcRE3eqJjxMYD07SzrAiVklAqQMYbMrVkZpfzgnpEvqwiW6HVbUAtPSCffNFDkK9bZmegZPFDpYLo3aCIeBEur3VHRNW5R0DEbjX/HyFi4UMRsSOQ+pGRUB0S'
        b'SpQ5U6G6ZExETGgPXPrRkHJN5l6BIuUh3+YekPKvb/4Cf+yElCbm7b96nv2UB6Ska/furCenj7pQEp3EG1xoiVupj9YUGiOi5WS9g0WOw4etxCeOGmiQWR055q4rVjLj'
        b'UPV4gxRdWqt4BKT0IT37aziZ7sDJQV0wo2tesdxLD0fDK3B5uwc0PN7T7mG/UpkmoOtibVl6uqEoKz29XUi3mfPbvcg13TlR0+7pWkNjMpj3k0xHyKWZXJ5gHB7hdnmx'
        b'uajYaLaWtsudblUalNEuc7gu2xVu7kPiy6BWEdWyKLunpEYbKvpKfsceIW6+yG1wWck59jeUMwIneApsx38558dyXlKWI53G9/zrK8g9/Vil0odVqnxYlcpXTqdV8F58'
        b'wX0BNr6SRI4WrEBPgoHNMSGoQrJ+Ad7bbWaH0P40J450nlgWtzRt7+1YmuIYP7qf8n317DVkr0fiQc0i607MhUSXc9PddGB9dh5P81VXX3Tx0D4Flw8416J66BXWRib8'
        b'8W71hI419bhVXFc6gjTPOYESr5ChragcbbCRLTTGh6IznaKmV6GWhwVO9xg1XYK2deOGnk4+QsbMsfqA6Xz4Z8dutL/3gDdSUXdHsFKnEQMyFxZ5MkR8+WQvXruXCZTT'
        b'CNRrYbLQd/hxZPyU7yyeNfY8k09CjWoMkyVfBN7IeTC7n+ZGXkr66UGn8m4u3hCyX/fsuJglXpb8JRMGLV0db7s54cTCWbP/s+S7fg/6vjy279rSMP08uSzP79UB/+Tw'
        b'ZGWM37jrI6tinisrSRoXvD6k98SQhWumXhXSfY8XXxiUmf6u6bJsyMJjGcZx8Xkve/wtbnKYV0DuYrOkfMins0oUX1pKikMC3pl92jPI6+b6B2Be5M5kPKmXGt/Cm6OI'
        b'm5p4cD1QhdNNvR6do02NiqbnhDBRJWavBEmRGEz0QbivePZM4dGSypnR4su/rAhgAE18olR7kpm5cxm6WWZfv7G4LkkbQU51de7EhrcmyPA21FKKa2ejXZJgBm0crp7s'
        b'gZtxmxiCe9ouoQeWRD325YIZFg+x+MhYEsAExY/5JCM9o1DcX7Xgut97yixKN2xGpKkirIK1kOPqFFvDguvbVFitnPXq3o0pNu9TCQ9a7nzQPP/aqaHhxlUPuJ9j5iyx'
        b'j29eu/rPh1KqIl5cm/f362Gra/p9l/MvCQr6aFDugrhFf51TZYj74YeP/x28pN9PL9/YLnh4vNkSdv6Pbx5dOnb/z00DXpx4ds+n10wLrlY16le/lJu/Yu+SnKW1OCjr'
        b'vz2/LeN2bxye2y9EIzj2CkAngxxn40zDl5wO6WXrqK0coZ3Sc0xTAmrGF2bjRjqjOUaDmsK05IBS0oP4ODotYTzxTQ5fk+HdVKDhtkVkv71QbYSGZelCu/Ez53WPef+9'
        b'O9+6byRgtug7ebzJTEOHRBNWKaivm3i7fTg15aPk3vy0sxhyUDcJPHDTrH4vWC2sGblYF6ngq+4SUL39YUeLXR45JCxUh7aAphCCdjn1137okIDO4CPoQDf203mPoG7s'
        b'x7VH0O8+WqrnOSiFk/WYvIH1FEeCTqjO35s60Y+yntYSGvwe9fcZwHoCpw0cJ7KeLzx/ifXUhx9KPjfx+ITlA14PPZr5U/j9pPVen/bzKru9sDVk48zR8Z/pSqd/OFDa'
        b'V9H/vcUz0j6ecmv4wflTF9ROzpz0v2M96qV/EpfQW/ScyFqGp49tUjpYy/d+zmOtqoN4ryjGTLRf+uXgcvEYo6gxRwNuT58rvqyNlYpcYbjPnBagNcrTvEDYED/znSyR'
        b'rTl5mgc6ZkoyvcFbyPZUk4/1177U5oWjlMLTJ1dc/OibO2MOfbDwYtWiDL36UN4tX85+tWasl+T64Lt3Tr7rMf3r74+/+LZs0uhxAbdvTJ18IeXmT4M37d60N3VmjuH1'
        b'goXftSb/WDJRu//TwEWL/Y2T/xb5rezCW59b7t3+iQ09PiBhyngNK86jVaOzbMIMvMN5NLh8OWfkAztpkr97XyFKlQZjB1UO60SVQJeCnBwPQOmRUKZSDM9lzc+4Crr7'
        b'OyDALvIj5fzEOU7U6CA/pqL/gx4IkCRCjSGoTaTAOHQI1SU5KTBDQM3T0KVuSxXJH93aNBYos0YibuBuZ5sYQnfNXBlH73mDAPe8lSXfZzHLNyzjyoQyssm7pIaxcvSo'
        b'mtFrZXZJE2+QNLNlkkVMYR7ZWr00RjzGh34hB/xIljCFK1YDzZq309wk50I7b54BKSTN4lE+Uno6ghfUIS2T1bB2GdkC3iCrh/R26SRyQM9kmlcCeS2QN4OcRQBwSwA+'
        b'CYWP5JV3yyuHvIbCQTSvlB7C8+j5ymukYlp4ZuzkvAM/cbt7ejBOs50xeAQBY6GHn2YDewF+bDQWzzHPhL5dcF9is2Zrx5mJjgO4eY+MLflgJiKdHmWikZlzCM55GAtt'
        b'BUYzOQuB7CrcLiUbmhuM7cqFhSZyQ9VTMe8MEbU69tTsKJZuNU8XYT1GLqNISezK37gQvl1JziCxjBJXCHvzju2a5Ly4aF/lOI8Dfh8I9HwOsrrMj5zCwbnfi3fiAQok'
        b'VkY8qH4DbkHX6YnkWtSK9owJJRv/0F0b1AMF3Ia2d9mFt9Me48QlZwdmbmBTGXKOEh0GrlI8foLX0Q41T3A2hmw6bHmIPelFm5huLUrPLyrMieIdSjqJvVc5jni4Q7yC'
        b'DkgbljCRuFbcFZJoXcxwVCUpnbu021E4roCyGAqqgc1jzVJichh4OznAiDUITQw5GgcAl/gzzaydDWCIjCNvaASK1NEMwq7vc8Fr6OKzLzixPZK12ab8fA3Xzha2s7kP'
        b'axtpEmkabeNY3rl7IC+egCJ3tO9YKV3oQdqDtkb2RptJA5Npe6XM8IGSUrSz368sWWZ7XLL8Ow/kY92Ld1s52rH6bvKkYmZv2XMsU5whDQgcIb5sMN1jtqzx58myqD7q'
        b'aeLLkuEy5mAeiDB1hvLzqEWM6b69TaDnZaRIJpDd+lobm3dcqWypvLLvj1WDH7u6u3lTc2XzlrbYy5U2NstrpuLjGSd0f57R0HeTJNHzo9KgzQsHHx0QPuDl0cpXtmgS'
        b'faf5HuVCnpWPCq5aogy5Wj6+yjg4K4rPmcBEpAbFvZIAyirdhH0PuoU3hmnzlCHixnxkefOuIqrI6taow+K1+AY+0ulYutwSqqIOFEaQ7U5QNTlbNBFvDWfh+xkOn4fk'
        b'm8X4trPoaDw6Ez+erijdgmtBT13HDUHlqt++RLpXQZFh/FjxxId0gynH1FPwBbNePkdJ493EAyb8WfMbrmJqHqXCWmeFNOM0vgfp5t+Dw9lGtoIdiGpGQzvrk1FbDN0v'
        b'mRy/Q05xpb1TomOZceikdB1qxNsfzj2IdizyDCLkmkVy43TtEr0ly2QC9fd5ximEh3XuIVmucU2+Kbs0nnfEval4urdaP1S1nM74082S0BmB8UzALbiKwzfxwT4Ph4Tk'
        b'JSecUCGoIMcCEXjKHNDRYDxOZ36ToUr5bCdUv7QjmYet0AFjMoGRntDCk1AZqhx4a/COMOKIcwcV16FKsgvcIc/ev6nPsp2wmf/8sP7yyBwTI55n9RiUZH4b3omnttZP'
        b'W5QwKjpONOBAa+NM3oP5iej6pP8XfWV+55F6CmATZetSAtu7BDYa6HoKHUPbCXROlXLgGBU+z48Em/NEt8g519lsZB8/Awt8nWhMjLmPlXB9vpIDfYIp48XzmuxcAD39'
        b'ySK1c8V97Sw5PYkCLtG1D4saOSo6ZvSYsePGT58xc9bsOXNj4+ITEpN0ySnz5qcuWPjYosVL0kQZQDuZ6gwsqAemEiBbjdAuFac+2iVZuXqzpV1KtuKIHiNqAh5dmx49'
        b'RhyWTN5xrgpdbCYer/WzkhfD7erCkxNGjUlwDRK6FuQdwE9Y9Eu0pXTgiUE8MoiOyfvO2oElfdgjlkSPEUcin3ccAKAQQcC70NFsAoNzKGS4UYWP8VE5id1MvM5HVLOu'
        b'I6oBnEfaRrKby4phejrVRNCJRyRcRuXoUiqq16CzdN013rUwyWMevoJa58Plynwv1MAxIfi6UIAvLjJNWHZIsBAd7b0pT39s+Gjw5xmLQfTo2SwQMM9mSP+gZEIqhKn3'
        b'ftZwlKsX4vqcMC0YXdvicAOuA+PUI5pDzehwoRhIUPcYvh0WgY4GuK2zJKssp6CTDztm2mQpSreaCowWq76g2HVIu3MzJsdMYon5U1e2KuZhTniaaFVPfFtZ9xC3gOeK'
        b'xWSrsAZQMHCtXzRArI2Iw1u0DDPcLFmPjqjndAuR6+yW5B0hcm5OSRhjz/9tfCrREby7jXEvHd1naUYBupkwJzNcRzbCExhpX06BNuKDVLEINfmn7eIXE8Vi0vqQUoau'
        b'dsJnB+KnxqOa6FGobVQUM4SR6Vh0QBZEed76OQI+zcKnq6PQFQG+oT0sugpS4hRdOo8rlpnpxgQRTEp8hF5cEG9dEKhQsxkMk5ExyYuJF3Wa+ETNsF18E3k5A/eWMTYC'
        b'PN6Utphs9cdMZFATLp+Im71p4gMDPLjLjJokTnx8iWMFecwkYYIP50P2NVD+rfRxQBcR/NMD8vBhXJUQh86GSxmhP4sugu5yiubZsHz6hHZC7MUZvq1LB4gFJayZGq5g'
        b'f2CYqIxROgsrvkwdKM1/iQkkXZP4hHkdY3otppi3vA5fvm5Nmq17JZ6frvx5+753vmi4EuB99R8f/vHaN+oNz71WWTXwsenh+xJkgxd+F1Ty/hs7d8f/MOOD/9Tteitk'
        b'TXlw2KZnMXpR3lyruoeK82arf3whrP+LVy0Nw2IPvv1OfnTdgx+f3z585Xun0LJ3YtdgfGje8b/Vrwq+FxhxXvff74yeeCPePnzI19tvfhmw9ed5zyz98Yfh/ed+qP1p'
        b'3oP+oW+lPLHt4nfz06LeN/9rZsLtY/sN51U3pnxsPvfZldd1lTuDHzu15IlPk/o/FfP49x8NPPkXVfJfbj838f6/Bunenfangu81UtENcTN15vh+Ce5OCJCvZ8XYgfJl'
        b'wWFLF3U5eFhYT/W/6amoOQzfRG2dVm8PxRvoUkcVqov6/9r7EvCoyqvhu82ayWQlC2tYAgwhYVPZQQQCIZCwiQLimOROIMlkJrkzYQkTRUFnhrUKiqgooAiIKEhVRIT2'
        b'Xqu2WrVWUcbWtS0ftWo//bQtrfKfc957JxOSKPbr//19/ufLPLn3vve++3Lec857FkD2HkY54kQhYm1dIQECv3azMF493k7nQrL6RwZxWqj7u8EcJh1tIeCt5Sf2+SGm'
        b'1P8FjM3kBtiMPG6APqOuGDqM4A4K37RhoqzWtZpx+xG7wxZk5iWhD1CXdnK/l8N355lXclSGFP6qnDWK0I2SxOzVfqXK4yYHgq38z3/G2r2goBu7BPMlWFZTR6AuL9wB'
        b'qCN66hn18TEF0wcPKlM3ASZxLyoKbVafHjpiqMT14yX1Tu2UdlcTVnOp1Ii7s7bB35vrPWxIlaEDiX9txJVQszzCo8/IKFBV6OcvgjSkKSQpWSET/Euw5ZpyuEyIlQ1x'
        b'QsIunsSJ9WPtiCiLRrq1InMFDLFEZVhE2oVuWcXdAuTMEGGprB0xG3dgiTgY+XW1M1I1BBlmk0tB3avrunZeXQkB6WQfQQWre4wtvzvXnFfp9QPpwSSIOnJFy7AeMWZq'
        b'amjwKMo0HHyJKGFzTAp6VgYBl8AsAjXNnpgt4EHBpiD6WV1RIweXKX/E+KLsae9nFir4J3z+JD5xHYl1uUPU/Vgh78NKuvo9eemCJKIhQnY8eXs/lGgG2hmdvDwCKxqI'
        b'ErQiOQvWdC/tfgkQhg3qLe3wx3jX4hgj/kgoLgcoroP4buiiGcZ8F3Y2bE6yiJ1NXDlBGQbjLMgSxBBDIrq2Rl+eLSKOJ+VQCG/JtTR+h9iwG8omQsrMZecHjrtu4sp6'
        b'b1HBRMIEa3xLxy/uM2DJwMXXw7XAhc9FgyZeN3ECodTnsLKMWfUCRzQeUiMxc8BToVQti5mWKv6mhpgJOUVw8/pXwOi8RCs0JkIpMUsDioQpvpgJehMSWI1CvwtDT0VD'
        b'kpDabUTeJeq8H0lEgJFJ5hAMniv+2KnqqSnqY2SRUX0cxQ7UaDlDYUkL/FH1rlILN8plhp1ta1EbrKPNGeUeGg/A0YVMDrF2RmYo41E5R0nH6y5+NxfIDgkyYPUhzo1q'
        b'O4LSC6/0pU8IMH03/E/hlthaiHSB3MRsGBmea+xHsa+Ixx7LYpPbbuQi8spMijEtHqOsbQzdr5ZUFuPt54W8PBoc6E2awV/RwghW1HhhsUger6ceBsWz3OP9jtUYczQo'
        b'niDqmmKfHxZ1yt8hMptRqeQENZWepQuZSFNeaEIvLteT8baBMwpd0gCiKNWNrN95rre6xzTwKnVz59re6IS69VAeYBW3SPRI5OQQenuRaZtYa661LLLCO5NspncWj6XW'
        b'JluMEGCFFoBzqOttXWSX+6DDRAgnyY51tkVJ8XCy7ISwQ3eoKJGjxRQ5FdIkt3mXJqfDO2f8jSRnyJnwJqVNrC5yFrxLJR1vblGa3DcsAr2BWty2RelyPwr1lHtBKEPO'
        b'hzRmqEGe3BvCmeRDowtB2v6xpKkwNB5f8Cqg1dpMRYOFOM+Auq0MeXLay8mS8ay73I3xLTQFzl2Av/P8GCABEHE+oPvCmxMf64T15ab1Sj7DAw0VVZ6fxWGx0Nw9oWpF'
        b'F0fskP6juiItibQ5TFvGJSB1QkGxoHEhMVixtCMVtpitwVtR43PD558bVXAIzV0SqxCP0a5swSg7nWO6c36LsTx1Vb4DQszkxu2BFkaHSnS4bF43uDqpYnNqYtmYtN3w'
        b'xIt10PAgBJANtb0DvJIEVVPMfMclvWWUZBfa0T1xzrE3Puy0B/CMW0ynFP3wVIY50A2JslAnKF1l5DEI49AxLqye5VxgiGwKiXiHXYDHkxd4Y2GpsjgjrsyjL2mdBWYt'
        b'O88PifGDzgtFQ2DIyKKviS44ePzq86bVg1ryA7j/MlfkdiAmlWBgRQ3srbgXG4pWazh934/xDZ3xpt0AbWB79pDB+zOiPnyGQpdd6MqnCsIaO9+c22YiJqYqa2PpU0zs'
        b'u57GNKS+C7IjAoH8ZsOyMTQ8RSUbW2YKNAE2gYiETzYEFLEJMXt8wndyfKDkQvrf42CSO0hAVttOHMzxv1HJda2VVHKwphbMsMLrVbrynSJVPeDTOeRodYeH5oyLqwOp'
        b'O4Q0VCPkbERgIkUkREAiNK1rYQJuEqh+vFE/dAhOfqnXuQSY7DGTL1Bf0QBV7RWvqpn5M9B9ccYsHlaPS5J7VvIgh09FXR0WPbMjxtWcntgWln3nnTuUNUWIN0WIN0VI'
        b'bAp2NTRG0BujoBfwtg2pQZtKQZc+Ma7ES2/+EiW4lT4Q88vElqS3awnLv92gxFlPSC9FoKYREVrSxYAISiriJsyfdwu0BjFEXMdBQZ9GYshg04qwrq9k+IGkdMGG4Ukj'
        b'a12S2w1YVk3QU+92G3vFTO77rU0q/SD134wjJbuOh6Xyzdltlmtr5p2P1A2Jky7nu9rHxgqhbHxk++kjC1shjayoj6yUGJuoGqUvb6CwPdnwUVegbeyE0Yb+CBhVNoY8'
        b'btHy0oa8v25zl/ZC1jNo4ZwZCGjbO/GivseHqrHU5rNiOtpCrW53pd/vdbvtiKkj86A5s21h7DPh7/PbjIZBh5BLesT5yD07V43YL4/47X2wy+iuz3E2FUPHnOfiGOMq'
        b'AMo1vmAsBVF12VPlrWDSpqhAH/Szw2NjZ8Bkigt7mw6sL2IEmxUPOjlySvq0IuNHF4DKvtB2xbBoxR02gqZUXrwRMk0bWdgkEZHEM0EGmhKAM0lVwy7zoWof85gUs3lW'
        b'VnmbAjXLPbFk3NXcQHViqYEvsZJ50EBfYHyfPnQmC5BtEMFk2JG8sEUYTSzC1g3By1/aN1EBapBLl+LwANsGmE6bTQPr1AYaYFfE6ZJX4VJDpwjIDwBcYAhrGG0iEsx+'
        b'oOh343E4n8tdJ7SYWswhU0hYzgGtjyvFlItulYSAiz0v5fE+Tv8CMMOMoL3RHDKz9/DE1UoolwElpUB+lhYrlGwOWaA0S8iKXRuyZHMQcyzEtLTYQjZlcYgPzAf6dGHI'
        b'Bt/FcZxPCNkQYwlUhIRAhUy1r4W0NWxGSfpJNy7Q86a+iG25bDEHrAygLWu8Mgx3zBL0u+WaqiAJPdD+ADtMEOZWZcyGEXEZBQjLZBSQjScOEO099iq/L8AUA2O8jAck'
        b'kGmMr1KsmI1QJTMLdoQif8J1urFeBrGzcehQiEMieJdJB6FOWt/ptMbNJA1kJ78FSJ223YD1RhwglJgWoksoLnbxxa6si4WJqSnHjaYoQrxlSTwjvJGeZqgBIiG07VO/'
        b'0JZD4JkgkTIALwW8PveoFQlOwS6ZGZjgIwzroop6R1g5qyhIQA1KAjYbnpxiqiNVypQyzenmTIvV7pScUo6JzkkHj64NoK/VTbOALF+n7itonDG4zMTlXikVa/sb57sY'
        b'LwXIx/1jEhSqNPLUma3thVQFLjM3XDbPV58phNjIQS3UjqwqNTKFdiaV33CjoB3subTdCRFOMpJ0So+DhxpAY+KQjZnbqK+o8+jIipLXAZCy6AN6haRTKqkC8691p3ao'
        b'MJBQEXuhulm9X9A2qPd2IJduwK7AfC6BBE4lZ4sonQ4EL5CWEhCvPDNqtsjE9BWrRZ3YNaNpM4hjkR1yMtytslNOWYem0Vhz0mKOKU319av0+naMLdMeg2owjIKB3ZdP'
        b'IDP5VjKT8R7gKhIfQpKNk0tFjO+rEq8TC7BR4toiCpTN30+o69yIu/viuBStPzN7dzGZhNoNEwxAaeZ7wsqC1dQlsUU/zK4NG19lEt/JBmoDVIVVZYoxsma+OatNgfEo'
        b'nWNr+gEoYSE6nWE4JKE2z+pgSjEkDMGZ2z1NMkhDvjnnotbGI3Ve/AQaSpkHktCMomiEOALAV9Ij1BFIl2PFYKAFZA0quYROtVZ4XVx+qi/DhGkgqdcIX8rnv/NYnQDP'
        b'DAP7YTDQSfy5jttzyegPSmiwenWKAlncbq/H53bPM7oQMO3Mi4qkCJ2zELAxQW4pEyjQDfBIuL90hnPhN7d7gTFjrB1MUYpxCS1EeYriTltHcHwh4nYop9muFB25G8e2'
        b'vYv2ElxLymQcvanxvQH1l5UZ8Q3iezzdKVdCpLGSfmps5eyi1ewQU0WrzSo6RHbucaxIDrgQaKuH1PU3BBMgYU/1GUnbrm7XftQ5GEQbZwYY3CbWirXSIpOHyZIhn0/y'
        b'SLUWQN70EJ3vI4i0LrIyzhyARQYmbcRhszOORiy9vLLWUxUk+356b/1ABhLCDcXeCdQguIZ65grarWzObl/aD2MeIbdMSf4u1tEyLMwJHy8ZBC01QJAyhW+PkOKM8GKe'
        b'xdiAnh004LvgTlwHUYFLsy3I6eQXoaPXQIskIEhXdWUiwASBxBAdU6wVzNxC9t20aqQuIszvMhPpNxTiWFrJv908i2u0iYV0byetZB3gMjnG9I7ZS4BEWMmEZQmC4fSP'
        b'OScRytgU1MVoW4nhSwFrfkmfIwJQ8Q5A/hAFzEL512867zidlEy6eE2WtkHoGKY3vu0SbcXS2lWsFRnDfJa0LsxWNMwh5ogkM6cdVp9RH9COlmvrZ8wqQkm5DTNnNSYs'
        b'z6vUfZZ5V/RVN3XrfHl2TViehJPQwSLgKSIjr2PdjA4wgNJktEA60++va2poc7Jp0qdORnzF6dtVpPVUA0B97zhUMjEsXgquavAo9+OjLc6X63A7NXup1BbJ0LjDs6EL'
        b'zX2+o4ZFLEkHSn1z4uvwooVThutF0sVGrFyqSOas1WNjshO6Wj3YCgcbtc0lg4u0p0jbaEvRZHVrIWKNjXbtHvVR9XC7o6g4gwTzhX2cI4aHk1YYzwjAEB7u4WFRVgRJ'
        b'QC5iRto2wtGzabfQyn+n4zrx2lkzYS4hXRpL8rdOWCLLf6iXtLnQ/tskHdzAfkCbPEqGN6FtH3/JMHWDdlh7kue0Jy7jtSNw6za/3fwyG/Pr+oT5JbceyZirTXQYZFsk'
        b'kgiQGcA8HgRZYQuQ6OhHlC2yFbFj2SbbAfs1JxwAWRdZaDOwEhh3xhz6wM8CFF8pK25nHyTe42jFWwbiIAI7830ikNUGeyodUGC+BsX8gHQmJjwizYIyJc6Q6hUS9C+A'
        b'X+VygDhLSAKHxMBIfKKwlAu5I9ENbWEMLiEkTMFTdROkMxlxiAAfbTArawXZDOSKhOQKbywUC/KHZxM/BS8T8EJIUuu7oa1QJGZ3E6PWjSxkgpWIGbh0wy0UuxsxwRoU'
        b'T3XNSjeKEJJ6QUzwBS6N+YUZ3inpqjKCICCH4xu7yUqmqxEJNBMvN5UkOtL5rnz8lIcGpRWlT1wNFi5BGOJhDmUQZH4P9rKATBAewihiCT04mbFA8Pg7kEtsEYkYGo6g'
        b'EJLwiJzoK06WNmF/FxgMkl0SKq0oYygFzC82KrDmzGthtCmHvvDeAmCqGOOwL/p7WnmomLJWYG8aHSFRP1ABwGiah4ckMXGqT45JZehR3LSgwtvU/gwtjhOwMzRk4MjC'
        b'csa+1HFyWMgLcZQWx4Ej35GAJ5mEfMrASR1cc2HbPq7y+5Z7lCDxIgKJchbMYidkSizPVobpcKLpkNWFvuk8Ov8lQA72GEcGd1KAIASpxYCnMWbyK7JHQZZeoMkbJCS6'
        b'vpXP8l3H/s629XvEmE1WnllatfN2nFcCGUP/1i52Rw0TId0ufCZlNHf7jpa2O2qL8wuLaU7hqoVZ0a1FBEyDBGZIrSkLZxkxoMXdbMylkCjzy3lc67sEfEvvBB2HRzQe'
        b'eYqA93lgzK3uai8KP/io1wwu4fXYtzfgpeJ7MA8Zvv/c2OCZpdl06gVhjdRu9ehFdbiX0NxCCf0E5S64hrAljhCJw+5CnEvcjULL8I0x1pfjusAnEZ76BQEyhYQs2IFu'
        b'4Uk0ASDYbp7wOlgxsD6GI3vPZzXeYBw8apRN7AneQK9mcboYCjtaFIBywXl2PutqX53Pv8KXF9/g8/rkB/qcN6/OD+DJo1kZhl2WSdOPwTLlaqJPOR2RM1gLNNOuaY9D'
        b'x5LdPhTpQXvTkMEb2LG4XzHVpFSe8euzEEwJ6Xxz17bdm5i0HYSKs5equcRzPZo5uE/jji2wpxquRWIiO7rKGUIhTEGqcyFzSCLY3yUoscOcWtgXkFW7h5/LGXuAsbeb'
        b'lRpenyZKJV5oPdJhBtCnaMQd0E9LAsPFajBVlcsxaGNsVGhRwvLsmANaC/E/MKYi9pRdlATWZz3bA3K9aLEMloOtQ5K0Ml5xakJtW6T3kvCRVkR4PqS+3cBHrFyWlNol'
        b'tZfVluUkKZU+6j7tGZ07d622FpXDj8zSyH9vz2xJfVY9vrQdcmKgB+Q3Mo6cpBDtaSAlzGK/gZLgl4vREUSWdWSEpFCQUce4C6kx60x/VV1xjddTpiAm3AYhaSMLMINj'
        b'HEtGWAXsQUHmaQky0lGgb3Til4U8OphccDURp85MXDsL6p25rXGpofMZ6JQ3T/Z7dFv7aK7svCU/UIRibzhgazg6/AxgPFpfMUtFZQDP3WNWEo2Ta5SYBUXK/U3BmMld'
        b'T15myNdvzOLGGB45USAgJmEMJdABDYqT4QtjXuFKRD+MZvrZ+eY0o5M65vcheLMb/XQHZ0hKIqMLNepsXLM1ggsPABIC6ms43zDSS53EA6Diueb8ECwvWagTlZ63YCqz'
        b'MvAaIDARjN1I0lZ6fnydpAwPQj9iv8M7qyyx/Iy4Pju7r+BX4LET9fw8rtFKR03zz6URgKvyN3ll6vGKKjL3n4c9dfaeHfh3YKLLBnQOdCl1U8xUXwedrCj4bCmfRzRr'
        b'zORRFIBDy/GlY26TD6PrXwJej6dBh4AxC2w+lFVNpws6JmHh/5B0ewOo0CmQYicdTJE2CCkKrhH+ZrZJvPBlc3J8LDBl52ogTOuxFvAC6gmcu7wxBko2jIdkjMdF8my4'
        b'd5qocWzSmGoC8S4wKfX4TGyYi0m+Jh9WKNmkr3/mKAUwzW8koTklXmkW6/swL4ZTyglM41s7YxqjCR8PQLkMk4Fs8c2pCfOVPnbeTYMSysMJq3NpBcalJWY7dJOuVEzQ'
        b'XlJuwboEjQ5SmuJVu1irxu0GYIy8xyyToflJ2LeZJBASKqlHayf2i//XcDr2RaOZZPDFsHuYzCOeNvKtkk8w+5porKq8fkAUseMMERDJ7VlZ1QELFUAPrOkepjivH4kE'
        b'R9t1z+IgXwDhZCfbCfUMDdVteAnjZf2lMDfrIdJncZ4155ScdkcaMjgdFqYJdWymgpaHyrXNy3Vv3sm5fWtFe920dpuGRb+TkmmcY4Li2BLQqnGuCQo4LpLk1DBzXiOG'
        b'zWFrtZlYmDbYPNIYdUvuZ/B0xwYbCbNThmc8iXTtUld6TCqePaW4HVCM4yN4ChPkdEwCtgzAIARGRRrDB3eoW0SolVAVmcIAEoNmFtI3EM4QJkmavQoLHJ63PD9wPhkC'
        b'umtvCBo8OGabCs1xNlQs9cQcAU/Q3aD45aYqoAkcmNq9YOrceSXlZbEk/EZGXQGEJbnduvdrt5sJcLvRV4qB1cVV3b9rNLHsgcaUzyKhVYRozclYbMcEZmcsWf3g4Xza'
        b'PKhJXn2Fj0xaop0VhApbWyc3s5hyMaqJLYu3YQhUiRi3zelUkTYfy9pUx8QlcFbvTxg9XHpoGzwkMA5QraAMiQBdi08o5g10qQi0LKABa5lQOD23iIDli9kcCh/TW0AM'
        b'dpmZJAThpUDvRQDDlE1rhS1OwEylXZaQwDY3GaaRxK0VmYjUMC4wbQXPuLULOV1sqhrxeBQS/5JkGvLz502dPSnvS+wCJiC4UvFU2wnBjwkrKvUpEjMD2tDQFKRejJnk'
        b'pvqGAFNxRUlCOjmMmVbgub7OAGTgjvqZkgjVyy5dt1nZAUlGmHShOyehGA6aFg6SyEK+lf0CILPfwn6RROPDqhezTfd4l3uCNVUVCp6tMQ1MHKAqg3eFf6jOETdkg2Rd'
        b'iJAGwP55GjPE7knAGcZD1Ncb9T89A0UFGL+IXyJ80ATUpSmTQ1FPNETBwt1Y2CqbW2yypcXOOBAtSTAXkkgkNNjiALrBkcu1JIdsSqURL5QMI22FTXembGtJ9qVQ2A7h'
        b'xXJSiz1ethXLbhzVti4hRwgQ1xyujlN8mLfsyOZyuQY/5OQMOZUdcnLICTThjpBTL2NDyKHcjLx7HaZAXrIzZMG8ZLHF5nNSTCx9B35FAWxWEn5FkRDZEjKFkkN2QBds'
        b'tXhNqnXIaZvMkJtdeRRjQR3NtCjTy86hQsY57Pn553C0z4azzrz6l3lfTSwmXsl5cfz48TRcMdEN0ISfz2hMPi/GXxWzTPY3KTUAjPgSlxAz+Twr3CvZbZUrmcnP20nI'
        b'1Vvj8wQYkKqvUJbW+AKxDAxUNAX9BNzclQC76mJWfFnt9wEqrPibfDI7W9iMM1Wq8ni9Mena2f5ATJo5tXh+TFpIz2VTr53vSmGzmw7IJcpAIvUVUyC4ClDpJKyAe5mn'
        b'ZukyyJrVxo4R3F6ojkd/BkoYijApHqhFzFzJeC82X1O9m1IwYVwJn+GtZ2WQXn+vR+kkJmRJotOTcPGg+V3mzNJB6FUqs+qnG/aQdAYfU+VC4yDdySIOY1qY6SSYLTXz'
        b'BbSBRwyMVFpsCQV1yKWhfWwl13Zd0VmRk06ykSjKl4UohxpJQZGILtxjrcjRWasb2chFRQ5eNof4LCZSKMkWhHJBk85hNbehskWd02ql+WY73/WqCgWVlPNG+KtH56F4'
        b'WB6ZSgg01SupMM7nCy5FhbuwKK/fkIL8dshWXMAL9VtIx8rSAm1hXARdu6ra4PldybXqV43pgKBCxSq/gZJmcc29qJOx8iNGd6RXdQ5zOi8Nyg8MorVTBsT3OU5n66Gy'
        b'jkxC3jER2hpz0kyvAeK+yu/1Kzo0Z5kbBB8dbLXu1onWmHjlo3g9fwFJa0wG4iVkkt4f8rb68DoUZtmyc21J2UlMbgMMK/fzneKCd/I60FdUXi8ogbXwA+0xtTIZNkA+'
        b'/UxxJkOqZLXkSJnOrIF06HGFum96QL1duzmpoVHkBO0evvcC7QTKt8UxgzLCkcvKylDoSyTVXYddvQXXp3qf+mRvrre6QzuBn0mX9qfzBE6S8TjiBu/iRX25mqevvt8U'
        b'2ADo3YcvOmfN/9s1GUszd/5c3tHvT2Ml6/pjBQfXrE/LOCMlR/jVsV9/Neb0m4venVv3bslNJa+uGjLxzxM/uCn295bQvk8/bNix6vOT3zgXppx8b2P69P9wDHt9+LAD'
        b'057fdjpScyh1xPHpjqZ7735r0LB9R58/8V6f5cui7xx4+fmi3/Zd/olYueXVtNVN4Xf2rYh8c3xS99erPtr1Xp7zXMtHh31p04I7Rz1ycM5HXy1bPbf6d7nvvzh72a2f'
        b'pp2c9UV994xDhz/8Wc/+c7yrZp368MtV9uw/Bfp8/VK32/9z4E+mznxaffj9opzFv/s4vfpPfz+W9dKOO5sOFJdc90KXuh55n6R/atl4Yn3dC6etlb1u+tGZwueeGPjy'
        b'3MqZCwc9MeDqAz+f82a027Ezvxh+fPsrE/dueDT8u/kPZe1tTHr60OMFX1c+MGHrx49t6lVxW+PozcrdP7vvwJQFN768NfWjH888unbqwjt7u17iz/6ysmfSodSkMb91'
        b'xGpethXWjZ9RkVb6X4XnTOev+u3jq5dO+GzZX10frr6j977BWzyL73/pxm0/Hb7g2M8mrPx096jXTyz4tHzTqS6HTpY0HD24j/+28rq7bn9bvv68vCZj+5nSW1ctPxP4'
        b'MORb/t6WZ48tffjju+5oPOz54xL5uvvfPT6gbnjxH3qffXbL5cuPnZ7ZoD764Yf8jMKUvVunjNhVuDZc/94b1z80r1l+9dOVdy/5/IsJqx79+PZ3X7/746bDxVuqPn2p'
        b'aMX84t/f9+vpZ5bcu6Hw+OK3Rv29ynus+29PTxxY/Pi97yine9YVviwdevedxtMVg9T9B54fPPZP+ZsGvPPk8emLv726tjalvMfq12OPLb7atPK2R46WX/v3LspfGj/w'
        b'7jy9/EzjAx+/fmbsxh5DZo9YVL1z4+/vzFm9rmpkxbIuJ39S5v5oxLuz7jq/5dCes54P3Zt8LyV9diEQqnjszZfOvJLc/PXvRtfdGH38N1994av65IttXz/+n5s+2ft+'
        b'8T9+GZlz+nzW+zu/fPfBI6/VDej3o70XTt42UPrz+u037i396ifXX/HBvPS06x84/+merNfmhsrr1nxe/k35SX9t1ui3u7356dvbDy9s+fX4Z//K+3d8cujqTZ+PG33m'
        b'obPTTjx4dqfv9Iiul239r7OPTnzxuokfjm/5fOGAy3pcNubbt3+6rWzn3o82P7y07t6fV379/mu2Kw68uWfmnPyJH2c/nbG611jPG3/cXxksf+HxURW3Zjy35LV77I/e'
        b'H5z55Z09njj1/p9v3pjycOAP55T3Mp8cX1Bw32dpI58qXP3mnz7/6/Q/TFty4Ox1Rd+eeqvk253rVvyHZ/EFbuEvjnzkfMeVRE6Q1EfUO7Xb0DhnibpxyPTBWhRghXZ/'
        b'unqbqP5Y+5GVGa48MjmZLL6WFQ5Cbe4nhXFz1bu0UyFmZXmPR7v9IsfX1+cy19cLtOcoTsOUiXEpQ22z9lSCDKV6r7aWOetbo20hX7uHtSdtqIpcKHAFE1PUU6K7ZUkQ'
        b'mTPqkRptHVSClCP1A+qRqzCEh9TqZmbgSttSBFtJaIxd0p5WHwwOg4SZ2sPeVinHxpJZpYO1TS52tl2vnowfb0O6m0rtXGpjEMGzekrdZ/keEYTZ+X3VnVzwcuylQzf5'
        b'AkXkGGhLkx5ty/D2Z+hQyArtHpv6lHpI3UjeuSa7MvTaqYfVJ9uxeW/U1pBe/DU27cHAghGtcLp/MSBiP2hT+M6La+S/MLP/Xy6u3mzb/ne/GIwpr79C1n0+4omTwJtv'
        b'QH1/M3/pP+kPzh5OG8pHCyL+p/OCDVBjSyYvpMNzxkBemN2VF7IEwHj6FXQf68zJMUlXCkIOfwUvePvzQhNQp1Y8R+/HC6kCn0fX7rzQC2WQBBNdLTmQKzJuBVFAm3um'
        b'ts8OXrCyN/jfhxe6C3wWLzjou5Ouqf15h18izV5BhPpJkGPvnhAzh3dYHJRXTyoDarRY4KHGlwn8IN5RprwcP2K79X+nfSeXVrwce+sGTrclsHJPBxYkaBc4oO3V7lU3'
        b'MDOD5TNt6kNqVN1i4Zy5Yo+Qr+bkGrsp0BvmZc364YV3/Nz37tDU20pK7zrx4t8/e770hHxk56yStyc/sHv7nhdvmT5n4YmHasoVZ9OaBwKf9H3eH0vrZv3gL43FI7qm'
        b'n++/zfG33T+RZnzW79DdrurouaFfztw++oaHdyQ//OKJYT9N+emj93ywWm2c26v/nVN/szvywXtzTv5i3NKB+574XTf37yfY7nzc9vXN/7lCKdjYa8OmL7/csHfl3pcd'
        b'lZ8tM5+S0+fd2m+f/YX3j6W4r779HwN2r58xxXnol2OCVx/pO79ma7O116//eMOAC9Pv/eqpN35XmfvF9mW+Qm35T155Y8dvz658f+kfDrxad/PmVYVvHPrlnaO2P/lC'
        b'jwN1h1654uP3fr9/z8F+ew//quu0LY++dSbrdFfvvtP3ePvWFX767oTGGVe/cn7vod885xh7yvTkR2+WeXe+M+etzXkvvvrbvRkv91wyrG6OO2X/wykHdm1ZNmjr1rcf'
        b'3N1z7tQt+x99MVh44f0X1hUVbjlQM3rv7t9vfLXw7JtHrpu95Uyk7L9ce+vrt36z8TdvTzi7ePvZJi2//LOFi494Rr29/vT5W9adfGhby9M9lpyrG/PmyB+/yT/5twl3'
        b'fXjoj977Tn1RsVcqrD/1bP2YslMnziS57vZvOrr9smFbt6945O9/vfG1ne9M3N/zxQx3uNc5QUh3jfpHr2ema2u3OJ54qfcWYcaoK3O7zJ8zuUfyZb+6qluP4K8m9xK7'
        b'f2SdvHHoC9KLd1feNjpr1E9drzZszl9w7cfC9mPq5b7UD77+tuyrtz4YffSrSv+L8yasmhHKOnP2pnsmnp7xxWeuCeSRTj01oas+nTZqGwbPu0GfTnPFYdqteYS89O4/'
        b'B2OUq7dq63QUAKOkqSdEdeti9S4yRwMoxf3q9rj/SU4arT2+hFePaHt6kDs67a4BMwvUxwbPVZ80w7Z6M38DEDO3k59h9emV6smC0sJBaEtJ20LO5TaWahsU2Pi53vNM'
        b'6erBwiAe1K5W95dfbLwbSr2LGfDWHveqtzAbWMcnqZtKIaK20aVF+zYCSmXmUkaKdeq9bjLJ06hu6qVtGDJd2wQVnd5dPcirR6u0fcyw9271aGGptnmg+ph6UOAEHz9h'
        b'rIOM9QBqcUDdXIBWwcvR4tk085WCU3tqEvsYmQIYDmJvAwt57iY1al4pDFO0raxzjs66uhQ/ukoKtUfMAmdVTwlqWI2o61mZT2kP3wDY4WDtmAU2kxA/UXvmWubF76mr'
        b'5qgHtfWASMHyF9Sj/Hz13msZuviwerP241LDBNU09R5mhSqb9fcJ9fbBZMxvnnoQUrbwxWrUSaVVAPIDuGh5Ue9kHrJcz09TN8wMopy2AEUdhf+IdqQvYG6Dpmt3QU8g'
        b'ToaIWP5lpilquJZwKfUOdZt2Mgkw1dJC+0Btvfr4UvVZdb/EdVWfk9R75gFGiOBqBhR0lKx7QcegVa9SQEezl2n3q1Fp+PQeQYR11au1YzAYM7QH8rE6d/PFq/rQh8yB'
        b'Swu0yBBtbxn6L9zPX2PX7qQGuBsrtQ2Ax2mPqkDuCjfxV6o7qgm5zdceG1lKkBFGyWXmktSbhQHaw9pedat6lKHR+7UH7eqG8nJAC+8rLMHRnGXi0seK6kFowHbKRdt2'
        b'mbqvlDlyLS/T7lN3UmbOG8UpNWOpBuoayAf6cIiZ4+cJXTjtQe2ea2kelGgnqgy7a1KZeqg/rx7WTml72cfhWljbADCcTGBIlbPUk7x6siaTmqsev1a9u7TQNQNSzutj'
        b'nidkzbXoTn+0HS42nUtKAFtNUu8WBgE+v3+8epzWsLZlSTWMJyDQBYZoqcSlq2tFbU0llMxmYF1jaclgmH7RpjFUOae2XizTDqkH2Qy8O8NfSr5dJUm7jefVB9Q7V7HM'
        b'b76uhhqkbdOOzZoF3e4qgdy1raJ63LqCZuKgK9VnCkrUQwNdQ2xLZgzmuBTtQVFdUzSb8OlV2tb5pQXTS2Cpde2dy6u7k1NpEQ6YqN2lbcBFD5SMNGdJC68+u1oLU5or'
        b'1MPTC2aYOL5UvWMUVM4JzcCR6QOYO5qoxAmFNiqhM0IwadVbtPt6jWfrMOz3wEojD7dS6kJtK6/eo21Wn6CKwma5e3gp0ESXj9AeqeA5i3aHYIZVtJNRRrcKV5UOH6Fu'
        b'V59qtT5Jtidv0Z6mXsy3q49jjI03xg1AkvnHwVBtGqn7l2mnSslW8eAywcMWplPdJU6uvZ7RgfvUB7XnLjIHqt0qqGsh7vGUDIqkbRyjbiNTnPXqjxNjkiXObC6IJpth'
        b'RA6ruxGmFMIaGQRBWKV3AAyZSV2zsbRQfUTiZqkHew+xaDerB9R7qI3XT81JQvKzAVOW4mzK1O7rN1nUHpZgcbmwige1sHoqSds8pHBGWRMdaWpPIqqBkWEO7L98sblE'
        b'fVS9lYHaI+W1BPWKps8q4qEtewTtAVF7GsDPvSzClh6z0U4tbRy4II8K6pPqYwBm9q6kGt0ItGuBtnmm9qC6R9tSOthVCOOe0VPUtqrPjSSwr20EWLOrtBxWK3RKtGTw'
        b'jCFQmpkbzGkPFZi0Hf0BimK/VWt7LPpWtqncBZSeugn3qaz89DpJVLd1p/qM6QYk9QZoTzntMhao0RPCREXb71bXsd5/YpW6EeYIVGk5zk2A28FuMy1crnZUWjhG70b1'
        b'5MhroEIF2hNofbe8HN3MpGmwH+5W7xhO8Pd6h/oQ9bG2wcJJhZOaePVQ800EO2H4r8B6Dknc8g73wLp26yepa28soRz4VUmlJbMGzbJwCOnMkmDVngUSFRsRXD2ULN1i'
        b'IwuhU7W9Aoopace7aPddkmyUYQB45L8BSfVvd4mfFBN5twsfkqyClW/7s/OpgmRykKnj7oCeC7xVcOpf2EmHIaWkW0AQ7PpzqmDG3AT0D5DZJk8HnZawOKhCIlEsOzsX'
        b'EVaKiabxjJ85z8wzvrYuyG0j2wFNDW53q8E743DgFT6xffhA5IbjL+3JDYrRRoQhmUMLlEyAIPA8XCs5ma+FX3RBZAHKnEUHwF2AuwB3Ee5ZcJfgfnVkQQ0Hd3tkAerP'
        b'RXth/FqMyYf58AJDSq6FQwk5r1gvRVPqTS18vblFqLe04CGgRbZ5rfW2Fome7V57fVKLiZ6TvI765BYzPTu8zvqUFgseMAZTIfcucE+Dewbc0+HeE+4ZcIfveEQa7R3i'
        b'IilwTwmR/ZxoUgjtj/PRVIiXCfd0uHeBuxPuWXDPR2FuuFtCUrSPbIlmy2I0R06O5srOaDc5JdpdTo32kNNarHJ6i03OiHYNiTIXyUWB8WhfOTPqkrtEi+SsaLmcHZ0l'
        b'50Rny7nRaXLXaIncLTpI7h4dLPeIFsg9owPlXtFiOS86XO4dHSP3iU6Q+0Ynyv2io+T86GVy/+jl8oDoeHlg9ErZFb1CHhQdJxdER8qDo2PlwuhouSg6Qh4SHSYPjZbK'
        b'w6JD5OHRGfKI6Dz5suh0+fLoVPmK6CR5ZLRQHhWdI4+OzpXHRMsi9rVctJ88NnpVMBue0uRx0Zny+OhkeUJ0vjwxOlTmo1NCFviSFxFC1pCtGnspM+wMZ4d7hWdVS/KV'
        b'8iQYP3vIHnWQ0EqrLVZnOCWcGc6CmDnh3HDXcLdwT0jTOzwgXBQeEh4anhSeGi4OTw/PCJeG54Xnh6+G+dBbviqenzXijFgjrrVC1BZm7tBZvg7KOTWcFk4Pd9Fz7wF5'
        b'9wnnh/uHXeFB4cHh4eER4cvCl4evCI8MjwqPDo8Jjw2PC48PTwhPDF8Zvio8BUouCc8Ml0OZRfLkeJkmKNNEZZqhPFYS5t8/XAAppoVLqpPkKfHYyWGR7NsnQ7z0cIZe'
        b'm7xwP6jJAKjJZCihLDy7OkOeaqRpSYo4Q0lUQn9KmwSlJFN/5kAPdYfUfSn9QEhfEC4MD4P6FlM+c8Jzq3Pl4njpItRVpJykG+04ji2OSH7EERkUcYQckZK1Agpo0JvB'
        b'9GYwe3OjI5REh5fTmPF8slvRqhDSuVwa7pFMzyjCNfFKcpAEGmt5Q+5b18c93yU/MNCVV8NESCvyKptqvMEan0tQbkIYNAgLQuKvUxtQ7mofcdlQ/Cxq0tW1HHRMrLxq'
        b'6LK4JAB3Sz3BagWVJ6yelVUkMkMK23j47a+OOQyhIRIW4tGeRz3AR3iyo2Hp+gbFEwhASPT6l6JGL0qWKa9xzFASd45kOrBe5/AA8dx9eOEMAWq/7AEoS5YVUPg8Jjb4'
        b'G2J2yF32VFegaoO12s1OVJkmYavlhThkjpmrKZ9YUpXfXaEsJQ+V6F/TXbfC7/Ouir+ywysfyyzmgOdAsEI3ZmmFULW3YmkgZoEnysxGD75AMEBfSWSeSlheobQGUB4X'
        b'Q5SOHpz0VgmQaIPPT/l4YQArKlkCxeNZjhbEMYCSCxQwVXk9FUrM7K2AAR4WEytrlpKgOZp4Yf4lYnZ0b8yemSDPS/ogB5WKKg/6NHS7IXqlmw2kBZ5QFCEmuRVPdczp'
        b'lmsCFZVej7uqomoZEyGGiSEzC2T9OXSCMdDVzqccThAkNJi9J4F5r0FhKbSWhBZP8aB/Ch6mC6Q+KqwFKrkxOWTod3csG/i91o9wcn4cF6sknMBhTNo2dSRhVKOOP4av'
        b'EQtAOgcsrFysSYgHGCRUo5JFCtl95Ej1QozkkYiXFJIi9iZOmRRxtJhCQiSpDi0eOVrMvkwKccqQiCOJazFFOCYSFrFH0uGLE9ruyMa+MEcsEO6xVgiZI12gRME3OyQo'
        b'JfCuZySrGu3ClKIQF5STAeVcQ7FzIHV3zM03Bt73iqRRvEAkDeCOhRTVHC1WiGmJZEJMCfYK6Ou1qARTGZJgB+EpPzPkd3vEDGlslGs3iIMj4YQW2iG9ni5kgyc7PqGP'
        b'nZBtHsfaHuEh/QlIlxJJTjKU5MRIKn1LzkH7t0AWylwoCb+FBIC0ydkcU9wie502Zm0/LizHevIV6H97pCuUK2B/hEyZpHwX74G3qa7ZRg/oAm7GPHH8N48//t/zon8Q'
        b'uxpn86cmXTnfaeCqAlPDMsOzmZT40lEOiMyEOshIaBbhuWbAe7NQ3kd0CqlCd8JyrWImL0nWbwDAC22WSZq+89AyeUPQl4kThtqlL5PMxGUCX0UcvogEu1NOm4WDw1cA'
        b'aSR6wilvCkmBIHl2N0fwlwXDLqJsXciiTApZSPvGGoLS2OSBhdJ1HOerjXSL9I30h+mfW21Cs0YwdQe22CMooWaHXJNC9kg3WI51MPFSkrhc3JJFeHbic8hBCw7yCSUB'
        b'cpiiT2CS1mPfQnaY7jN8IyP9IsmRbjIf6Qv//eG/V2RgNR9Jw3IivXBZZQJyCe+7RvhIaiQVkbIaCy1rE05jWEhpISu0JhkmPNxDsDQizhyuxRlJB1QA3zizOVg2yYQi'
        b'JEEqQA6UZyk9PMkoDWxGSacWk285vDVHBkGuKaGUSA7FAWAA9U2J5FEoTw/1o1A/PZRPoXw91JNCPfVQV6OmFOpGoW56qC+F+uqh/hTqr4e6U6i7HupDoT56qAeFeuih'
        b'3hTqrYd6xXsOQ7kUysVQdQpsDIWI2oe4zQgyERBAWyMDIsnQ4tRQ6o/QbJVEVwteabZk42yBPKD3q9GAtt6abA51A6FHM3CWQa4i2TeQsO8RcNP7gpBEkrOSYb+k1Th2'
        b'2v+Vtesq+jeAH//zMKo/7LCBjXEY5dRtcKHkoZl3krurdF6QBJ79pL9brXYyMppJUozC36RkJr2YKaB8ovRXu4Oclkl2c5ZgB/gFP76zn/RnR3qqmA6wDY9VpW8dJgeZ'
        b'BW8D3wxlLoJvzKAjQDAgmyNWHb6ZI1wCfBMjJtrOAWGJ2ADhB7jGJLrboC0dYin/Aqv91KnbzLqYmw74RQDyUrtGWY1GncBGSbBMEPcQACzbWEPWkrCmkoEC5pFUtGBJ'
        b'76UQxYQmJkfMuENDV6QAoEpGsI0hFFWP2Lfk8JhrUiQdlyF2FgEx0QRANmIbCSjguDZC6j7rMC4wNVFEHYAggFMA+KL+nAq5kKA1+uSh/Lg2e3zHnZrxPzujHzTHRdVh'
        b'Dgt4tVu682YYhHS+O80x+8VzzJ44HM2IagJaGElBNDg+HJI+HJk0HF0APRMDWfQFw1kYJtPyfWDeOVDfl77Zt6RT56FOvCWHdAgw1EHXj23T9YDwRSy5qOsqKU+FxECZ'
        b'gYLzWJ4ECCXuzialCd0wIqSFfc0EOxAMdoul2YTMCFLYs0lckFtVb+Ts41dwlCKHpQ9cTcS5M5wKhHlmOLvaoruFsSaUYkXIr2yNJOMbIzXbEwHTsFULdZJyDOpyPJ6z'
        b'DZkgkOYQpIE38N4WT5NY+r2JKmy6GptY1qE6Ttwybdx5IVIq0GjodnKogCYk0JsNWmz0ZyHuujyuF2fw/oRgpfIh0pd/5H+w1Y6Ysybg9ldWu1coKHKtfG7WaRiJl3QL'
        b'rjT/XDyR8P+UD43cf6etQTPr+rtsIaHAukNw0MaAze3+rV2SyFwO+qxEhWbmdURCz5V26fOcTLvFKqTzDgt+xW0Erv+Q3pAKJd6Vw3gUq7EsckUhBlYFlNfw3et4+RVe'
        b'3mDS0Wi8JqD8mtQBmr01lcqb9FhfEVymvEVq2PDgqUAvB8ppUm+pkZV8yhTo95hYUQmU/7KKACprxyy6QaaYJWA8LPX6Kyu8AVfyv6YDXdf8G/Do//fyzxxq4JxsRqIt'
        b'xqEFFqvU9kDDKeSYHDz7tT/wYD+pg5+jw7f//M+s/7eGHeZ0UbLMFKXL7Xy1KNXa+TxRcgwVpe52fpwoTbajzQ8rkpuAwgnUzjJUn3mKI18G7kQeoNutr8j6igZYlkFF'
        b'uYNn6rpklICdpbxK627qyipPA9orVvAcEk9WqiqaAh63O5bpdgeaGoh3iIw2VE6Bt0nu1oDydVsLEwl6rePq/XKT14MWeZgFJ9gnpVS0C9vhCY91FbsLfVBb0RAylFD3'
        b'+vz/AapMzT8='
    ))))
