
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
        b'eJzcvXdclEceMP60LcBSRURFXRWVZVlAVFRExYJSFwVRxMIu7AIrsMAWBV0URVmKFHsvWLGLLbEnMykml9zlLn0vl0su5WJi2uWqyd39ZubZXXaBWPK79/3jhQ8PT5ny'
        b'nZlvn+/MfEK5/HiivwT0Z6xFFw2VS2noXFrDHGa0rJbT0nVMB50rKKJyhRpWw22k1CKNQCNE/8XVPiaRSVxH1dE0tYjST+MorUeJp6GKpnI9aWq1VCPSeuZ5acToKiH3'
        b'3uTqo/XcQC+iNCKNKNdziWcOtZjSMznoOYvy2CjzeBjiuaBYK51XbSou10vn6PQmbUGxtEJdUKIu0nrK2PsiBOZ9Mb5g6G10ZAFtbwmL/kT2/8YIdLFShbQGtWWjuIZu'
        b'oOqoGma10ELXUVmUhamjaGotvRbXTJGaWWWBo0twIRPRXz9cEEe6JYuSSZU26gf8eUEprr4qU0Ch/9IapSqiTN+f+jOf97vpp6heEJGCojFEjJWysoWsEyr6kVAVukLl'
        b'KNAdKk5pjkT3cJcYHM1SwJ2wfQFsiFgIG2Bz1PykBUnhsAVulsFGwyi4maVmZwvhhbI5OsXRKs4oR/n+dkvxlepLVWnhA9W9zyO2hquT1A9Ur+UHFhQXljKXNgwcMGDS'
        b'm/SGBNFC7UcyxjQC5dCB9fCIFypWDhvh5nSzIhw2jYOXoxhqGLjMwQvFXqYhKFkFfKYUNIM22GYuSEXpQAtoE1E+AexQcCTG4IFSyFgbEyYzYPzjL/jlQ7/4QkP5aq1e'
        b'WsgP/TSbj9po1BpMeflmXalJp2dw84W4MwZKaB/aIHFkReVxhWZ9gU2Ul2cw6/PybF55eQWlWrXeXJGXJ2NdasIXGW3wxvde+IILGYQL9sEFf+HHCGmGFpKreRR6A/aC'
        b'RrAvNSJSqQgHjRmOToWbx4JbLBUxTgBPpUwqxVDsWHOPfm3gKxKq4jn6x5y2bBtFsOWHUSbGJKYqotV78pdnfGayY8tH08nXGf1K6LcYKqFyjGqw3Gc5n+X5SIZCw5xz'
        b'y1tV+u6iCv5lnkhIYWB/PVwV0S9iOGXGeA6PgC3ZXqBzgSECwdQA27KiM3kECItUhMGGqPDkdJpaukSctkwho81SnOUObIz3Qq0ZL0tVeIbBJnABdHLUIHCbA3tDwUkz'
        b'HsM4uAW04UGMQg0GzSthHR5DrwwGbg2oNA9FKRSgHh7FKWIDYZv7MCtgg4w1D0CJAsFheCRVIUtJF1DCLNDlywSBS3CveTD6llsKz6WS7kxOXpOrYCgvsJuBnXADuGse'
        b'juE8DK4Mhs0ZsCklPRI2poEzYOtAjgoAdSysRdh+DdUxiABytiA1mYa7IpIVBC8FlA9sYpWzS81BuJgrvmxqckQybAZXBBTH0eBQKbhMmsDky3lMTk+GLbJksM+Eiofb'
        b'WHADtWwX6i5cvAqcyEyNGYdSpMLWjOQlsENA+Q5np2QmoAS4HaBl6VicIDkdfwcb5Lj+8+xYcHmqjCE9PgK0wjqvpJnwAhqkCtgMN6cmo/YGwv0sPOEBrATP1sELVV6w'
        b'NUqRojTjJMnwKmzMSMMJJyyBm2qEydNhK2oyrjIxHt6EzRFK2JocUQO2RwpR311m4GV4NswcgkG6DY7BZ+SwNQ0NTYRMkTI9X0D1G8rCbZ5BpG8N9IzUDEWyHPV+Y3JE'
        b'SlRkUjo4D7qEVAQlgHvAgVmk6eAy2FOOYZGj76HLI2nKCx5h4DNmrTkcfz4CdglTyXfc9nlhqYghtMLNCAnnKdSgUUjN4oSwFhwfZQ5FyYfCjWjsm3Gj5oclpaGUZ+AG'
        b'ZVpG9jwFqjdOkGgAd5wcj3Hlw7sJQ7fSiIWyVs4qsAqtIqvY6mH1tHpZJVZvq4/V1+pn9bcGWPtZA639rUHWAdZg60DrIOtga4h1iHWodZhVah1uHWEdaQ21jrKOto6x'
        b'hlll1nCr3BphVVgjrVHWaOtYa4x1nHW8dYI1tnCinU1TDRxi0zRi0xRh0zRh04hR29l0kSub9rWzEnc2vUFJxhfeBBtX9cFGWCoW7CRsBG7Rm4ehlIvBNtTzzaAJnED0'
        b'p1TIFKABk1aAigXnR2QTrF6LqKMWNlvgFoSYLMWsoxMywBZCc4lwPdwuB6cikgTUyCgObKRhnT+oJ99GL4Ftchmiz2REj+A02M0ycg9wwtwfD+cVNgUPTwQa52mjuWQa'
        b'3A4v5kloF7jql4pIEH3xtHAeNDgOtueQAmcOg1sRt0nCQAwDrVwSjUDfHc5n2wa3hMhHwSuRMoZiwDU6FyHDOXMg+hTllZMKTiOCFVLCUi9wjAlbMto8EANxF9yB21Nh'
        b'E0Tig6Yqh3MjaXBuGFxPaqsB9eAggrEFWhHS0ajQVjpNt9wcjHPeBFssqQS/ImhKGIvYxW1mgFHCF3sHHgfb5CmI8jJQyxPAVniI8QkDx3hAD44dTtA4TIFyVhWAw8xY'
        b'QYgZDyO8nbI4VbkUtoahJujpaSw4QLKAUyPAHpRny4KoFAzHbnpOFbxI6vLPBVsIVcgmDsfUKwZ3GWAdCzaSlufDerATNgeCpnTEvxkLPT1+AmnbyoAFCOTLcB9swh/A'
        b'ZXoBauUGvraNcJc6FdM73MxRwkGWoYxnjIV8mg7rwhBr64THk8A5lK+GngPujCKfOHC1En1qHpERiUFsoueCM7CVoBg4nLsEMRBCrVeC5JHJqGOUAmpAMReDRmAraYdk'
        b'ZL9UOZYOAaAhBY+vh5ABO+C+8gLGju9cLx0HaThW2qnjMA1Iq6lhEfEwhHhYQjzMWrYvzatvHYdV6q5s1wuM09CLMR39v1K9mv+FqqHoC/Sf+93mhL0eSeNoXaHU+4XF'
        b'EV456+N3Xv980+bNkiEJ/ypsj7vmU68S/lpCvXnfZ93UWpnINJKIAx3o5LUThEY34IYMGWxJ5mVX0CiOhduVJiwb4EVwvYxP1y3chsM2LN/iEkyjCKHdXEZEZEQ66sbG'
        b'1DTE3hwph4EtHBKhd2eaSHdvmEhk5Zl00JaBEBS04jSesB0N80J404R5NjwXoselZWA6QyoHSgDbB/mw7PDyLBNG8DnwFuyUK5KQLBNQYQlieIUBG8HZhaRZ4LgWPEuA'
        b'4Zm+rAizfR6WUeGCDF943a4p9dCFyFuiCdm4MrWxhHGqQmvFNP/rQ3vSBn+nrsXZWI3RZGONhgIDTmjAbE/GuKhXjCEA3/dzlEwyr3MWXOemY2HcXzYfnobN6QgfhRS4'
        b'xHIRiOajQWPfynQkj2hMIfOEqnRRTzTj+kKzkMAAgRFrub9e88FXqqXPvXF06vPtL773fPtLV9q3+N/zKfwojaUSJnIPd/wLqcN4QODO1eBsakQYYn6pNBVaIAZnmOrF'
        b'cCMZcnjOF9zCA5IAD/TUj8DmmXxXMn2Pg9mkK+3WdddRYj/aEEh167psef6Kn+l62tDf2es4SwMuxg8XU0s99HHtd8JXdoZPlROliabSwAXOQIO7y8Od3U7b/7IcsFj4'
        b'7qSVPCT2yjzcwffRl+eV5xeajQVqk65cvxlnJhyDMY/BHdMBb4MWxB8JbWWkyBVKJdZdkdrAUtGsHFwWwL3Tch8DRPFjgPBwQKBtd6kfEzawIp20CzYrwVV75YicAmAd'
        b'C27DDmXfKBeDUY7GSIcsOO4J0a7YFe1oqi/uJuhO4OClw5z1EV5q5Zz1PY6b9qrPsy80P/3gI9aYgl5Ib58/8+mXqgeqL1RfFkgKVeow9b3Pwy+pNNbVnVqVpjPgC9V5'
        b'dXHhWW2nujhfUoQEe259XL24Pqk+/oRYGrV7/bghFNjknf+PwzKamH2rpmQbwbkkYNUqkeVhH1B/2M6Ci5J5aJgIfnI92U8P3BfkFahLeeSX8MgfxCD244fY0OpBxmJd'
        b'oSlPazCUGyLjS8tRSuO0SJLBwZk4taHIaBOWrML/XUiklwXIGLCIMwxyEgsm6J0uxPIgwJVYYjHegdr5SKWGDWlypMBh29cbboqCW5HMbkQ8XYkEPrgGt4FmUeZkCjRN'
        b'94DP+MMtus6wX3FGGS59sa2kqLiotEhZoFSnqVd83Kn9QnVa/QWywHelehZ+VEpT2teFv9LbHHj9RB3m5dIprjyjv5/QMLibZ/AG7yM6xNUkxvm2u/TFN259EUqICDbJ'
        b'SWeAi7DD2SFRDDUY3OCQNrIdHO6blHo5Z56SdzO9kJpTLtD9FPcHgREDBpfcTVVjDSFJzW3dLJPG9tut+UZ1/XdixL5FVNF7wnXbhss4wqFrPKqJvFVGKJQ8bwZb4Fl/'
        b'pAaD1kR4w0R8KzuRMb2RyFVkToelKCJBa0YuOIFa3iZPBufCeEGdkycuHAJOEa0AXteIeTnuSAMPwmN8ukFwBwc2gFtRxJ0yjcbYgoqWpaQp01OQRUT0goVgFxU6UjBk'
        b'ErjqigkuY+5t1hcUq3V6rSZPW1XgSizDhDT/awjpHnsbi1K5jD3tGPEhzhHHqQ+6jPinkp4jDi+OhSfkxAhOQqS9OTUdjTk4Vw6tSUJq1GpBBgc3OAfKMeIDXJgZsd1+'
        b'GfPkqL5ktlhZilvdOkss1syhpNp1r1eXRhprlhfFshdEQoq3zW9q4Tm5Ihl19FUKnJ+KrNsjNLgKj8N64rLxF/7gm5QVOYyZ9xH9n+Dh9FLe1RIUhvCMEwvYCvUwqWgV'
        b'/3JLXD8qlFKt9qJUFvk6A6Vbl3WTNVajL0n5V1PVGnWntlN7tvgLVYW64Vyn9ktE21+q9G8sKgzPPKPOfa4dXGn3D39JHNjcKT6lZk5vO6U9rz6rDhJ9yf1OMkIVt+l9'
        b'OmnA3k3jAv+S/cVb0f2vUp/tzswJCb54in31om3cWzH956x/yzrurWjhuIoTNOUxavjr259DnBe3EinpXeBEqt1DIQC3+iOjo50pB7dX9M0/HstVuGK1sZgglpRHrDFi'
        b'xIUdv0QpRKghIXdIORnqwmgGujOavuun+WQE93DmEy6494Ebt8F8uQR2aWBzElIP0YhegDe4/sgCDf05DkMMEbqHs5V5ci6Dm+3RC9skSjPWYtXwCqLrbSvGoSqjqKiS'
        b'MIIaX5VyxCGcUFNUalwczePLmSCWYC01qDTtg1FplAFz5r4uNjpP1z9xAmdsRA9zvvNQvDbWB0T7zf7tnqsHXpB1viKY5DkgiR7yenjiiPncxCRlYkGl548nJo2w/an/'
        b'lIffZm19YSAb+8F38Us44R7N/Xe9ug7lvzDE//L7wXvOZR5vGL13L+3RvPjCj3eDlurfOi3PLPP5PdRP/P7jL7/J07094M6dqzbtsMVJG6eNiPm+IGfNyJ/+yi76/ci0'
        b'NxfLvIhhoUGmeKvDXspIBdvczSVwFjaYCH+4iQzbG8YImQw2pYUrks12eRCOtK3WJQJwNx92ETvHC+4A9fByvEwJzpnsibxhLTs+EXQSvjwXrIc3QPPaie62F1ac4Tl4'
        b'jKjemaA9Wx6JeHMjtvVBK4OqP6SYvtI0Gn1cWgYOudpl3UYZXG8hdhn2TJgwBsIdoeHyFOwPSUPmrxfoYuBOP3ggdBXRaCYhzn0VGccR4eCUQhYJ25CeSlHBUm45vF7C'
        b'G3ZnQAes5dk9qorn8tiuKw8E14aOMmElW7xurtNIEKePwkZCFhIvuPpKpDvslSsVyajbGEoiRjooqBODy4luOv0jTDZhhTm/VMeLgFCeUuMYZLAFECEQSHPoyhtxnujO'
        b'E1GshDZIXai1vzu19qEWdNsTON91F0J9xc2Ow4xIgPpivTwsHTYFwaPIjhVSYniRAbVB8BlSYYHQTmPYPhQ7aCySxUq9hR5I1QgbRBZhA1XH1IgsIqOy2sfCHqYswg66'
        b'RryI0gdylIku8TRMoin8u5jSB+UgPdgixjktQlxGPKWhcd522sBZBBW5OqpGUHXEIjjMdFCzqWU7lzI1HjWeuBaLRx1jKCT1cejuvEV4mO1A5VQVojuOpA6s8WpgUUov'
        b'C1PIWjxbaZqq3I7gmE1ySRCUkgYPi7CORrlCGzwbxPi+jiY5xSSn2CXnrxdRFonhLw0SPocD3nlUZeEiqp3Rh5JSveoYBHtEA91AlQjxHYJGoGE6aD51O63/iaSjTcJC'
        b'hqRd2OBlT7uwgcFlO1P+jqQUklSWBoE9FbpzS3VWwx4WaTiNYCOyFmdTdTTqbW+N8LDI4n1YrBFpxB0MfmPxRnkvajws3kFUjbdVZPVCahyr8UT5xBYW56vxQT3gU0dr'
        b'xCW4xg8tPhovNDI++hHO9xx6/5NGgmu0+HTQQfgrp/Gu8bEw7YxhDoKXJvAyhlCNjwXlGICYdSGD0vnqpRbawpSw6Fu8xhff29+LNX4W/m6ES36Vxp/P70yDa/O1+GoC'
        b'JuL/3ihNq8WHXH01/Sw+Fm9cHv6m97H44i8Vuy3e+NnEj7EfaoUfakUgagVjeGjxw63T9Ed9yhhe5Z9Qnk/Rndj5/k/8E36PWumvCULPlGbAJmYgZfEn8Puh2oMbvHEN'
        b'Kzwtfg4YLGw7a5CaaItvHb2B1otNXvydXVwNVC54KCpF9rVeMfYhEyF1SkLGLg2JtYwdAEWItJZ51tAWegW1hank8NSiXa20ifPy9OoybV6ejLExkdE22tTDjH7oGV+q'
        b'M5oKyssqpv2TstvRQmp1SEGxtqAE2VjdZlh3woestNzwkI64T5MSygulpuoKrXSU0Q1IgYP6pQ4gg/BMrQWLasbINSCA62g7wBu7wUKMMZSIzJWPYIsGLAV+6obXgMXw'
        b'Q1+1dKW61KyVIojCRhllRPY+DDZqK81afYFWqjNpy6SjdPjzmFHGMQ/9yQt863zFkWs/l5SO3A89pGVmo0mar5U+9NXqTMVaA2ox6gh0ve9HAH9Ij3lIj3joMcq4JDIy'
        b'chl6j9XXh/4R0qJyk6OP4tCfTGIT6PQabZXNcyEGOBHbdugVqtVo4wrKK6ptXIm2Gtm5qOZyjdbmkV9t0qoNBjX6sKJcp7cJDcaKUp3Jxhm0FQYDFuM2jwWoAlKSLMDm'
        b'UVCuN2EDwmBjUUk2DqOBTUi6x2gTYFiMNrHRnM/fCcgH/EJnUueXam20zsaiTzahkU9Al9jEOmOeyVyBPnImo8lg41biK1tmLELZMRg2QaW53KSVefepej7NBQmlJKcE'
        b'FDtQ8XXKHshAMVjacTSWgz60kMXSj5eDAXbt1YcOYjzJM5aQRDoyQehpENJlg2g/YSCRn2J0j12fPrQfg/NLSH4fBktRHwbnQm8YH1JeMB2CygrCMpYhM3CwDv1excZS'
        b'OmxVJsLmiBSkwuSxk2HjOKf/XEyw004HX6ILklZM1YcW6jBF5M/vkLRiazgLawyp9DEh1RX/6ZCE28/WCCwCC2Nh4xHFGDKRDKRLhOg/khQDqcMM4o7sQKoDSR0khTjE'
        b'+TksK4yFFq6IruGqciwcKn0ekrYsliRI+h1ElIdlgkCDSxRoOFQKi5/QfyQLcUmVpbx0MZzWcBVnNVhCCywiUpuQ/76IQpKFQEBKYuL5Z87+zMVTlT5IBjKEgwmUiIDn'
        b'4mEkY5mML3Odd/idTGCYgkeYNWpNNlat0diE5gqN2qQ1TMVfxTYRRr4ydYVNrNEWqs2lJoSz+JVGV2AyzHEUaBNrqyq0BSatxoDdXoZEnFn4GDRz8Wbi2ANNnqPcoYiH'
        b'GUcTLOMQPmAs8+MxAeMawS8JHcz4oWc/hBHEdK6MK7HPc4PGKDwvl85PpS0DVjl4RgB3wtZMN+sDV4zVKVJRr2lPCk98Fno5TBsL7TCXXa0hp3KlQZcGPMh0IxLvK6gK'
        b'P4RkKJNhPEILb/SGxkKzjvZCZg4RSwgdkLCjG9gGL3zfiMNWOAQErtoTgSIpFDsdkh4WBqNPz6kcjNO4G4kv8wEGgLNg/YCq7qxajqpl8RPRk5Q1DCqCxYDV0SWUIRbf'
        b'WRAYNaw+kAAnRHidhO/QG2Ye0vbIm+AGrL8g/C9EzxjXiYYVvIiqmmnB5cbVsBZSKkrb1CBEOMoiHYbTS/A9ek+eLJyhAssZRD2oHAtHyqhYhCOaIpGmyZkEhQzSNj+k'
        b'kQ5JU6slqKMEWAYvQl2lQe/WChwRTIgyUMe10nbHNEIvrN3bRCvVBuKQZIsQCiMuaihZZYjDqDWLR8JuH2QavhCcXUZwXmswyMRPzBW70VWSR/hhBaq4zDjDiawIRRkG'
        b'o6gEM0CGQc/BDEFWRoKQOBih6iB6dbS6oEBbYTJ2S3WNtqDcoDa5+1u7K0DSeAmuGrfD4WMkLzAqyLx+KX9nbSLcbYhq+SKXOpvn4QRoEu2YTmJ5dj8Usd5BA1cP+vk2'
        b'OBSIXFycFt97/iLhk+sER2SvbAJtdxVQrHQkP+HcQcNTqWlKpSJMJqS8Ipl0L3gMbIU73JyZHvb/RszvtFQuUu9yme0i3nuByF1cKOBprY7OZcl7EkRmZwYeiBJxYB7+'
        b'ylkpjsoVkMAxgc3fHjw3R1eqTStXa7SGvudssVubcBcBCa8QFgqdpM09cq6h8PFzGyIlmW6BjXA9aE2FzSlh9jgR2M5SPuA06wdPhZqjUJLU1Bg8HQTboJXErXVHlCAD'
        b'v4Wfn72aiez6MBHcvtqT5IHPgAvwJM4WNT8sDDZFJSlgEzgVkr0gLCUdGeqRyYqUdJrS+3pMBXthHT/ztC0sLEuxMAl2LYGbZSnpaeDUAuxCyEjDMVLjwU5hKFwPb+oC'
        b'yvcLjFiBTlv3/leqV/I7tZ3qnOd2g2fbu3JObJRtOlU/Y3/Hnq7GrrpTOey9ImFXSXBczuX3m0prt1+37BwkHHvR4mEUzRIZx73J7PTZuWnz85L9Our7ewFftOXIBMTw'
        b'R3b+bXghdzFsTiUBS9xQGhyB1+F5fu7wNLwF9sgjUROtyRHhbp4HCdxgkuI0++A2NbzsMQRuVuAwr0q7K2WQmQP1SXC7Cdvts+HWMHmkIknBUEJwTA3rmejFAn6++EA+'
        b'vJ4amZIekQxaYFs+PGfvaQE1aq4gFx4HVoef+MllpXeBQYvkc15ZucZcqiVOCWyCUOvQbxFxPzC8uiWhVw/rhaKRbrmdMzpGbWkhumJm0O2nEPw8fTIGHb5f4YDKUIwx'
        b'EhModjpQtej3YJCL4+KxkLiRjnNObZqDdFwFM41o0tNJQoJHkpCbz1FAuVhEThLyURKvSsjYVTie5JqpJwHpxGbs7AyTG3lC6EU7cCO404N+4LEVZgVGgEPg0CI3+hnF'
        b'Ygrqg35a5v/8ZKydGzgnY210Yc+pWHF8qbosX6OetgblNGDeY87GANSvyDM6wa1wC3mDW1PBuaR00EqcjrgBcEf3NFsZ6JSBa2xMgBFsywyA5yhwFtb7g1oGHONZzq0Z'
        b'K4jHcncNyr8Z6d68X84nkx0bZXK2RUC5zLgSTsgrOgweUCcnZBvQwNVwaBhZMowcGUZ2LddXDAsu2ql5uXLCSegekfPoVDyDEslPjmYlyXGYUzaiXkqlkMHWtORsJ8MT'
        b'UOCw1hPeiYcniTN5sicfcvyRd2GEl3A0xUf+nlzrXiIf+QkbMlLg3Uh+bhsNYtk6j2CwpZjgChJBJwakpuIZnOT0+WHmYti4iOeB8511o9FZCrtE8EIobNdJp+oExhLc'
        b'nq6wM6b7JP4mx/JKYWSATJ2mLi0szX+gijB8qXo9/9X8X+cnq7dq7uWf036R8Ke3o6nsKXT2uLoF1nGfyi5Gb7+oNfY/Hh1TK51Xf7wucT8dOviV9pcD6bf+8Pwbz3/w'
        b'cvBrz+3xod6eHHxmGWUP1QHY73wdbJnpdD/38D0fr+HT7YZ7wAZ4uQ9OuB2sB/VwVz5xUYPz8BJoTwUtFU6+5870zoJ9JPZnCvpktc/hZZAKJaBTRHnDS2ywKod3/DaN'
        b'wM7pVsc8XyTonIIEfcBaFm72gR1kWiYU7IN1fJo55WRmhvKayMCWcrCVVLPAbzKeMLfPlofgchwT5rA59+nZrw+eCc+rMCArG5s7hP8OcvDfdZSYIcYvh8zZAGzCIhNl'
        b'9YTevE9bpS2wc75uHcq9ZJ7WBbxy1q3DPm7Sxz435O3MQNhzGbpsoh2iopb8/tuVQZuXY1RvQyhQ/8v4BZmWZ8HWybBLMAZ2JsLrCeDqKHBKRo2AOwJXJMC7pRg+S9ZA'
        b'7q8BVMJ3/arpwVUnx76Z9SVNJgm9xuyhL4ooafRAffWWOR3LOIq8Hj/4L77bfemw76h1kufnqrNDKZ3k5XWcEc9lnfzT3P6bb3rDaL9Z3yovrdWzz75CDRw5RVP77KTO'
        b'eTd+9cx7x9+aLTTpYupu6z7dQP0rad7SDVHiB/eqPjIsa0xWbWgaFnjzg9ULTxa9DoV/Orji7Q1/kn9d9yzbdXlxY+qJ2nn1mptLj98ZXxr3j6gflRLf4ht7hK/PfX3n'
        b'Hz73/Hvs9jv7Z72U5q9tn/e9NfHc0feaHkQ9p95wZM2FFwpf/2TIiOyZk4bV/MTOy4u4pT8kk5hIoPVl1LfnMb7PQ8TSM1bpGmgg2Dxs1CQyFeLURqbCu1ghKYY3eCps'
        b'gpvASUyFSni6t0oCj8NnTeE43Y6FLE9bjrEEDWjYGmeApow0nlHHaoTLQJ2YzJ7Aa5WF8iVwo1OLYaJB6xA+lO8CaDaggUdSbp/b4AuowRM40JwGNpB5dgk8BertPISg'
        b'C2jiZ/vD+8P1LLwSm0rmlIYiXtGCFDJwZ76LTnZ2KQFjLjgM2uRJ4JSGtJ2bSIPz63J5be2aBbUcFQ/ugv0u0Xs4dA9cSicgoPafXEVAuAz39hJKYC84b8Kzi1PnpsDm'
        b'NJoaE0FPomCrctSjFJ1fZrwInezCy4XSCa8Ic/AKk1NXY3DoDYfI0A/dcUyArxBd/Rg/evWQR3IOu/ZGVDGb0P6umz88sWWLtLlyfK9zsgs9ulS6aXNbhrpqc4+GC3FT'
        b'4g31zLO/yMtDJnNepVldynvCibZIKrF54yUkaqOxQIt4Xx7fIo+n7G6bh70QVAABvwhd8h3WopgJ9jbLiWrQtBbxNrBhTZ/sjaHiwG0h2AO6wGU3+1Fs/09iIh32oxbZ'
        b'hHanEVZoBEiVYTTsRg83K7HYxUqcpzah7tKjrlIWcPYSMZo4J8Hj0cWp5xItlwTCedhVJK5BjFQkAVKROKIiCYiKxGH3SN8qUm9NV6Akq05KBfAoUnWXwIs9Vd1RsME8'
        b'HaXQzwE7wTG4AwnOsKT0SKTD2C04RSZSe7LCsHstW+y+jIJOpaiYfr4ecP1a3cNThzgjNuDf/c/pr1TLnmvHVt29Cxu76rrqju/R0VmiEtEa0cszP8+tH1Q/4oLPtUH1'
        b'EZ/7nCg8kX85YGfgicKXRr9EG3yE7TlB8t2aksLT6oai82pxYRKd/2sT9drv+8+/NwxpL0RD2AI3gKOuLBM0whu8EQcOxvPTz8fgNpXDQENMZAtmb3A3uEn0A7CzVEUC'
        b'yVNBI16hgdQLxOQOafGke32xCYtQKZJx+/g1FYit7VqJo82PM1Wgdhnh7NNF8IhdL4LbwPoeLDkT7iKMLxtsQMwbMb594Eo351van3z0gtcE8iRUydFuxgfrYItDPXk6'
        b'inCN0CxEKJeH7Tp3Q3EdNcJTgv3yEsR+AunVg3thaaQzJ0+UQhtbUGq0iQvNpYSKbVwFSmsTmtSGIq3Jhe08RpVC/Golvl+FL1X4Uu1kO2Z0OdRDS/kkxJXxPApOGaNU'
        b'2lmPoQJfKgkDJpyhTGsqLteQCgwGRxc9iu/TBqMTLBO6HOhmJ0hZwpGG8ATcBq8jhuLh8LmIk9xWHk2RCsFJDnYQ0+JCJLvwP4SVqCRTRXMoN1e001WELRj3NTiFIuca'
        b'GfqRa2SK+/INu9P/QCXx6oBz0wOMCGGveFWa4TWzHGkGz8Au00p41WslaPGtkMAurHecECAGcRY0Eo4AGhKRGYWUvTQlbJErs4kJnIz+NWYoFsJtpfblkEhNaIiIBF2Z'
        b'eLURuAJueMK7SBwfeOSCTZZMcf+CiDXq57iclLQS7FTLkRELN6Q5lSCUdgGLRMB6uM9M1Km2qQD7t+zNgjvk4FQYTQ2Cp5RgC2dACs0Z3Q9+R2hjOkr8MPMfX6le/fOX'
        b'qtznLrZ3bDtVd+reqbqxzZV0+9V2/3uirj1TdmcGZ+0O2vteTN2nU4Ivvd/8IC446GLtgugYU7Rg3LFoblxFIUX9bmnAVt0Vh4tqM9yzTB4pg00RsAUcQSMHzjLjosEN'
        b'og+BukkmeRLPEvJ9CVO4DZpJ1Aw84rucOBZgk4KkCAXtlC9Yz66AHUuIKgk2ohG7jtLgVT6bWYobDO5OpkEXPLbKhEMGJ4NdY7tDZsAZRpVZPQbefewCBi91RYUWkRwm'
        b'/55MZY6EsBQ/EgqzOhwxhrxSXYFWb9TmFRrKy/IKda72jktBjloJQ3hkpEyVkyzXoMsLPbjFHbdoGTxquZKRqRkKJBXaHKMMWjKITwD952VXTysmNQKeziIdg0QC3/0a'
        b'cNCvbFwaWbAH7yYWynGfjotVwk6GEsCDNML1TtDOr/zcBHfkIVLpWrUSXqmUiCvAwYJKSSVHBU1hi4aCqzzi7Vy5ygivwC4P75Xenj5ieGlVJezARFkpoEIDuBrORGQ1'
        b'srgbwLZUJN74QRTD3RHgIgPw8qZTZuweQ7AfQmrzGcSMnkEtDE+JAKfh9lURYVhkpzmC/rPE9oWqNAWOgcuYOLxmwfqVZjxREiFDpT1x9p3giLnUE7XyEmjhGeEtsKsf'
        b'aK6oBG2r4DX4DOItJkT0z4BNMxAHecaMGpTFgfW61fyC01OgAfUVhnfXdHg9FRvkSP6miShfuIXNVIzj1wMfKrL0KnKVKAx2STyFVGgyB5qmBRM124xVVHhmEbILLiN0'
        b'nLJ4CDUlCOwkI+VRCQ/AbRmKZLhz7GhwISlZREmmMvAgk2wei3NdAXvjvRR4fVZqIdi0iG+yC38DVwkjWwbXi8At0K4gi9UC4W2PLFRzKHwWbkFkVw/288uJ54upkAyE'
        b'ASqVpDw2jg9P7FghpCaFIXKUqiRR4yciVZu8njeYpT6VeBJpEB483B4PGyykDmOFQ6qKeGflDMo8AXfE6Yk+WLmQwzOwCXuUGokPqU84y0GtuAZch026Lp0/Ryam3k77'
        b'bXr7zRR2RvCm30xfkxw78Vt6Ter3dGi2X+r3mWdb/tC2ngu6FLvktQ2hM1969a2F41o2+eZ/PO6fEc+vi93XvuLXH1uMu8eNvAVfKMjJNyyYOfJu0IXSwx/XHJ91IU84'
        b'+oq/vOXOpJnvxFzsOv/XmYqLDYdYn0mWkp2aQZ8I5/bb8Zvxb3/ddfR6+5I/5vwYceG9Exfzsk+Ubtvm/atzTdff/3DFt1eqLl3++4uLD6y6/uft6VW/+W3/g3GXrOPj'
        b'x/47teaPd94duf101QS/I+8t231Bo272jfVK//TbtX99NUF07et59bLgVc++PLIpdYit9YchA7THRv5+x9Jfj/psVuXUaabQvbvGD1kx6r+B/5pzZM63mR/k30hRM+c+'
        b'f2Fuv1EfnFxosXjum1Q1ISG284dtyRH/Kq+889nxUf/9/sDmGz9MSXxn7As1//3L5NeTzohCj64L+MNq2RJfmS9hpsE6sDkVL8lvjsCsIx8JMi94iWVEcJsJI2CmZEJ/'
        b'hMwZCppiVtIzEoCVt6svwEvpiIODOotTr1saTpRK0BI1IzUtPBLzF8QIdiIlsJRBqmpHOR9tfNd3Bll8jMdXgOj+OLgNm5kacCmRBHiWgY4Z8gwMDFY3vKaJEDx3GER0'
        b'd8EVXuutFSa6sPe9QTgkEiW+RLIz8K5aDhuSI5Jr8EJJJEUElG88Wwi2wk5+oVwHOOObGqLDFgCqQKZQIo1mQBqXAPb3I+IDifqdk+zRoTnL+fhQxVqK1B0NdtMELngB'
        b'6dLNIopT0Cj99TAyX7IEaeD18pT0QiMywrnhNDhQCFp5H8kBH7gPsVYPvljMlFEhCLMHgGtc0hzQwvfctRC8WBrLTLALWu0yE+wCG4hkBPVMhTwH7onsOamD+OTNx2qn'
        b'oqc18Pv3KeSIYMzsFozxWCxyJDIUGfmMnyf6YwJofPVk/dC7QUQT50hkA46HwdPIYhL74IekmQ+ZVvajAxgJY7A45DGy27tF5ZMA7hK8hQu50UN43gt2FZ7Ekb1nTWoq'
        b'PJbyaAEqoJabxGDHKHBMxpJFzivi8x1zbhKW2DkqeJyXZ7XJ2ApSgnNpdl8tuMqMh7vg8Vn2xdNCb9gqR9gWLkTjehiehlvR2N7MKGBdFL4gh9K3EGuQPVerU8716rTb'
        b'inXG2r8wyDnhIPjZCQeWzBtxH4eiQfSUuvxkaot0RpPWYJSairU9t06J9HRLm2yS6oxSg7bSrDNoNVJTuRR7d1FG9BZvooEX7UnLcURcvraw3KCVqvXVUqM5n3eYuBVV'
        b'oNbjiDddWUW5waTVREoX6ZAxYzZJSaidTiO1Yx+BylE2+mCqRiC4lWTQGk0GHXYu94A2jkQaSLFdFyfF28PgOxx5h4u0F49a2EeWEm01jo7jc9kfemTUSFeiPkMw9VmA'
        b'2Yg+8tmd6RNnJs/KIl+kOo1RGrZAqyvVa4vLtAZF8myjzL0ce287AgPVUtxGfRGOClRLcbwkBsdRVqRUWY46rqIC1YWD7HqVpCskufgORWOVr8YAobFCY2MsMOgqTL0a'
        b'4uZ18ellj3gpzeMxT1y7KCvKMeuXuSgJKZtZSSmCzMmTl1WDUzJPeL16MtiRMGJyfwq2w07JQLAtxw3p/Rwlp7gjPWVHe9qJ9ozVt9DvCWfW3AwqzB56b62gUKI0hHX8'
        b'zMJNZ4ADDxLlnNZ7qu13cNG91x8J+JoJw9Ud+WkPa8R2+dZPJn6lUnyepJYUfqG6ryorfKBKVnNb7kte36xLe780Mfdyw5DN0u+V78Rf83nHJF2mfvP5t56nAkoKTeqG'
        b't08JvjqrbtdQXxWuKHzt84gmZp84aNlzF/1eu6QOu+IluhQUHalRab5QCff4kemyn+TDqDOlMoYXeyfA4bjKNLkijPeU72UUyEjutH/TsXCXSA5bsaLMmWkkvvbD608/'
        b'xyTIW2VQVxAZMrRbhqyjBnEkjMgTMWg+qjIQr9iUGex8ySV8yI7BLm9wiQ4rC2PQU3hsaD4DkRtr0WUAgswY1C03aqmv3KaSEiii+RwGG+UOhO9jASeRJ+AMaCQyJTFA'
        b'FpUSQVFzQKevDmxb03coTQyP+tRTLdktfHwMgEhpxhGLsHnpwHHR42Nix04YB54BF00mw0pQBzsrzUZkHV1EatolZI10wavwsq9Y4unj4e0F2pA5s5mh8FYwHvAcvDOE'
        b'6PKLs1Pw4k5x9CiT4P4Qb17BP+abRLUjThCt/db/TYvCjtQN/8mmjfkYnH+9/eOC/i93BCTM8xO8seYfZb99/aNFoTPeEGz6e+HuLUlAn/lh0XcnD5o+nx23cNKF4ZtC'
        b'G5/5a45t8dL40N2zr48avFb+7N6XLn71vvb4f34jEr4pjGo8ut/vbx3ff9aQ/yMVeqT/hndO23GYnQpOOFXD8jKyon4N3ERUt2SweU23zwB0wgMcdhqUrXyUs+xxC93E'
        b'eYZyU17+uFiC0sGuKB3GETQOJBErAfTqiCdCZntxjgkQgp6J7kjdx2JkkqIblfFeCaN6ofIf3BbGzcQccTY44YrILYa+cdmBx7ApCjRmxMSy1ErQ7Bc5CGwio5+BbD4u'
        b'oR5VqIrYMjSZIsZkHrJBG+E2hJFpoDmSigTXQkniXeORqTrpY2ILmoQFPP4sjEaGQIiWoxJUpYtWLOXxh3wZHSmm/EJiaWR7RlhDPfiX/iGp1PaKWxzlp0oZEcfyL8/O'
        b'8aek8WtZqkKVdj3Hm+JnBEaBtizYArdnT4iGTRwlzAS1cBcNzsKtcDvJZoscRI23rGZQWZbwiBK+rE/mXqTHT2IQdX60KrjsY38SkwfbFsFjWRRSx3F5sEVAsSp6WiHY'
        b'TsxZs3Fyt7stOwmv222ISAEd8LRiIWxIRc8kQgK2ybHWDhrlnrLomWQiWFYgipzHTMJ76UnezxmeNZIiC1MVS8dQQX5+MbQqLdVQoJhYMe/XsYM8r9DELTAL7J0JLyPB'
        b'Ao9npVPpsEtI4B4zeAplCv63CDUm8zWhvbfCA6dRoTG+NDWv1hBcdMRAXtZWTKcsYbUMFa3KNM1azadUxSjoT4dCjpLWGt+L2ziZvBQUvUM/mKJDZa4vf29VVSR5Obv/'
        b'HPojgwyN7vqSnLl7ZeTlX6L70wmTNIj31NbsNptU5OUXSjNlSfwMgVq7Mlj/IV/Rd/4L6M7I62gA1V5B/QL4lxn+W+jQ+PlCSlVbtHtE0hTy8r/JOVRSoIFGIK0Ozr+Z'
        b'TV5+PWUE3V62l6Mqamvem/O8D3kZKhlK/XPMZgo107JbY1lOXu7NT6PjS2YLUPaSnCphDXl5d3wQHbF2NoNQcNmkaDlf+/KcN+jDJSc5SqWOmsWW8y/jTS9SDeqZNMJL'
        b'jyEL/fmX8lUW6p/FZSJqnmrh0ZIU/uW1/A+oZwfmsujlwCnlEfzL2GpvKtjPilNGnKNNdlxPrKA0tAjpGR/lb5/yaY2uVTeSMR5DHfT9Jv/s+Tdb30rwe1Bt+/D23yJF'
        b'Vd//JW75yyNHSENDpX/8iJqxMGb98R05ec8lj9sy42CqslW85d/TLT7DEtoGDB/+q2V/+Gzvl99U3tubHf3T56975qcOMV9LvVG96i1FuJfH3xR/2/L2Hy5lvhG9tHn5'
        b'0p8qAi8tXFo4vE5xP+aTuD/HFY3fPHr3Pd+Nmv2nZ0iHbNo1dvAr8jmTt0rH+KS0vh/45tZ33nr13p3RrwkXKn1sHgPen/zFzYjF648uvJT36eK6F9fdMnjer8+PSDJM'
        b'v8B+teIPzYUvrp6f9dqG2nOfDf8k57nVV39s2P8bxcSNb8fFRXjNvHYiJejBJ++p7/oa3hjpLXy3aswn28f9Vvvf4cfqXvw+rCrqh2d+r3+Y8v0Ck+/lw9W5B/3frTya'
        b'/aFw076wiy8ptr/3Uew3H0V+8/E05XeU7/cNE9c8CD34Xfqhv4zPOPDS5dOSf2VUJ05r/GH83ee2HfjtNwverM78zbPvls/4Xv1totwC/rn/t3dOHrDMzZuobh1wrmrW'
        b'IcMh4WdbO+9/NiBuZNGyzDPLY/vXRp3c/B/tjV0/Ljr89Yzh11f/6r915aczlzRZ/v4vX+XNtm1HQmRi3rt9Z5hRDnfCetdFpArQ1J93jrTDo+CgHEdmUQzooMGd7Hnr'
        b'/ImJDzeAW2CDPEWRqghXIiNSCC/MYeBtCrSR6bJhITKHjAoBjYitYhEFzg/lK92HdLRd8rVwB2LRyeAsYmelzIiR8DQpeWlYvjxSlgIPDJHbt7HzhbVseS7cws8Gni9b'
        b'0e1WIU4VcAo+ix0rt8A1PhJhTzBodgkpcsQTwYZScNEY/LSz135PH2DwxHqk2CE6idxd6ip3gyQ0xwT5+HlytOsORPj/UPQ/GP0G0KFIDIbQQvLFEyucbAAdRKS1kCxJ'
        b'F5PFPz4oB3ZcrB7087LbMd+Gg+9tIrudaBMQ489FaP8Pli2xhvX4nkT5b3DK+lp0Cegl678Ld5X1eB3MfLgJ7n+s1qpEWuA1LMEEeKMbpPfd0sDDZhzZAS4HCjHqFMOD'
        b'cqe3ttvbEQWuCODZafAM2R8sqizDMaUG78LzciUJIPWDm9ihYD28TvjgdCNZ3z4vwEMV8bawmGeO+/PJSvjoF2ep0jYtz+JfvjyZ7FyZ8/UolWTKVF9K98z5W5TxEPoy'
        b'eeBzQzZP9QHRkjlfjy5788pnE8WVY2IXHotc6PtGDMOe0vw5qEKgbHjlu9Aff/hhzNov9QnB32+69PEG7yXnn/28fsk3VS+WfPj9Qd+CDMGeFxMttX/9YfH+gO0x4O1j'
        b'064HfrPaf8zwvZ8ekq4dKrj3+efftCx4dWF89piGqo2+R2xvLtq/Nev5jjfWhWxe+ZHq+Nu3/vP7Gzvibj5YwDVwA4p3DvtmWNTqRQ0yEb+lRxvctbTHvqeOTU/3wevI'
        b'oGgBz/J21r6F/Xj3YrNIFMc7F8EeMQk/VEkQ/TeDs2jgXPxVsC2NpgaBg1w53ASOEF8juIXK3Ogc0COADCjiBwHhLOgELQriBgXHQGsFTuQcw6BxlA84z86eUMonuIl3'
        b'aQHNUQqlAjalyYRwj5jyDWHzwG0JHw95ZnkGaNaA5gy7suPchmkw2MKBo6AVnnBYiEH/c17wxJzCQbruMUr41x9HKIXNlRDnJYOX8jFBDL/UHXMGQx1Kq3Slb54ACe11'
        b'U3a//8Nt+Rm6x8D91MPNWR/rSvXE2b0tArTaqR5sBfvx7L1vLFuIzJ/dvWab8Y9RQneHAmnoXFbD5HIaNleg4XKF6E+E/sRFVK4H+u+5nd3OaQQt/M5WeEqf0wg1IrKg'
        b'xEsr0Yg1HhspjafGq4XJ9UbPEvLsTZ590LMPefYlz77o2Y88+5NnP1QicXuiMgM0/TaKc/2dtdHO2gI1/UltAeibGP9qglrwrld4c7cBmmDyrV8f3wZqBpFvgfbnwZoQ'
        b'VEN/+9MQzVD0FKQhi51lw2w+aTyrT1fr1UVaw8einu5T7OJzTyMlsRluiR6XQ2fEvjziUNVU69VlOuxWrZaqNRrs8DNoy8pXal38h+6Fo0woEXbS2/2TvHPQ6XckOSKl'
        b'80q1aqNWqi83YZ+q2kQSm414f2w3V6ERJ5Fq9diRqJHmV0vtKyQj7d5fdYFJt1JtwgVXlOuJM1iLa9SXVrt7ELONvFMZVaU2uPhBibd4lbqavF2pNegKdegtbqRJixqN'
        b'ytSqC4p/xsVr7wV7rZGkM00Gtd5YqMUeaY3apMZAlurKdCa+Q1Ez3RuoLyw3lJH95aSrinUFxT1d2ma9DhWOINFptHqTrrDa3lNIA3Ar6OGQYpOpwhgXFaWu0EWuKC/X'
        b'64yRGm2UfQvqh6MdnwvRYOarC0p6p4ksKNIp8Wr6CoQxq8oNmr4dRNjTivCe49daORZ21TDEC9q3i4gl+Ms93NTbq6zXmXTqUt1qLRrLXoioN5rU+oKefn/8Y/dsOyDl'
        b'ndvoQVekR/02Y16y81NvT/ZjtlAU2ncjPwgv6Huty+JXleTAeteFJVnwDlkfmwjO6UkcjF0tCUuKiIyEbVEpJtQVsWCXcE24RUYTvQRuSYGteCfaDAVe89CSQVMBpeA8'
        b'2M/C9YvgNd0HW4cJjPNQwvhbu/HSrbA/3UfXiKD7qiT7WoXIhWHqFDVzeeCA6FXRUZqlz11q79h2vU7WfLXuet3YZsUmz8bru07VjTo4ddNwssfdhuX+Bzf+HZkNOI63'
        b'QoH0/+Ye8hvuSrWL8MnwEJnoUwTizThdRDMFn1EQ2Qw3TOaDZBopcMoLNVjmVCfA2YX9gZUT5ycSGyR+FcA7OM+Ft5PGcxQLb9J6JawnlsIaeNMHNICL9o6gyW5PYH0O'
        b'6HDMf14Ohq14VjZVISKb5KYmAX7Dm/JIJDmuwx2o5KTxMRNYSrSahnthQxX5OmrOStK6hvQ0E+gUUkgjpOF1Pbj5uKA0N80+T4ewMy+PyOsgV3m9jvKQkBUIWDtfPcAd'
        b'bSMd+ZSuwcOGBndh3ffKAoZP1h0l3IRr7aVU1wW6Buz9XP19L3bCeqyFWuHYe5KE9jqmn5CSpHN2QvdEZim6tCIgyJqnXtU5VkU9HPizs1qoElZTXvCkAInz7NbLI+DZ'
        b'4oDnYaDLvJZjeizysVUVOarCrFSnMT6iqu3OqiJwVQ41ro9JtIJSHWLSCiPi1bLHg2BvrVeetqpCZyAy4BFQ7HJCMRJD0Z0Hi5meXd5duYN1D3Cybvt2nFaBC+t+Cu++'
        b'254nrkwTz0oPNcF9WbAFvQZXKXgX3ABt0TqyXTS4HgW3gDM0otq9FFVD1cyBtcSZmQMOToXNyURlH4dsLtDMjIhMAXWpulUtr7EkxHlRQs2Q5le8n5NKuFXek4uln2a0'
        b'HBfMDl0RfcGytP7+eJ8LQ1pWRuwx3bJMOlwxaPS/ti3I/fv4SkXWi5eF3sET/tP1u4l/HCPcsXZ25Tvjr69YvXha5ystv5vm138gEz1V5kkMlZXewI0bDst3tWdWghO8'
        b'HdKIjNXT2IGazEd8wJvMaHAXNC6HRwk78+yHeLpruB+0wrPVyO65SpgSCy5jXwzvEuHgIZWSBhfhQXCMZB46zeQSSIhkzRUSSXgENpPPy+GhOAdLEw4aaudoyDTeSphs'
        b'wpLUVNgahc8/4GAHG0uDW9FwN/HkgEMz5jt2WyZ7Le+PAxsZeI2PYDwMGsFl5457hAHrQFf5ZLCPD/5uHIGswuakseA6OJfkYNMB4AwL64eCfW7bez0hV9XqCwzVFSbC'
        b'VUPcuepQCQnL8CSxjWSr1F68zZ7bjbU+0U599o1Su1kr3hh0L+OYLKl1/n7xaOZqB+D/gm40q1itL9LykRAObcZB5z00JaTwPKmSpNeuehLdqO/NAznEsMh0RgQ4GOaq'
        b'voBDqzFaYPVl/Ahd2t1E1rgIo8+bH3i/KmdqpYHcc8uG/mfvoqy6WK/GcQm/uyj8m2dF1oH4/PVn/xLzr5mLK/vvGLjB8o/jV+q+3b0nuAaw+YnPbRw4+NP8H769NnPz'
        b'so++/vQf01TPV6ztzAq82TVZ5sHHX1nhLh+iAOB1jnbdAu6BnbyfsQs0yUFzBl5WCk5HhMEdoIOmfGALq50ED5IkyQj2wwi7nagdtdSB3F5wPyEs1RLYiV0PsGlJKU1x'
        b'UfhYgP0Gsmwr2bc/v4loagZoiXLoemALbKepaHhYOHm5PwnGArsmDsAaDAOb7EoMuFRCFBy43yMha10P7UcRTypeBDZUFdPu6s26ITzRHpfCO05mgFlBCTiIuUFz+dMT'
        b'pG8BQbM8B070jDfGv1GeZMeNQHr10B7k0CPz/0LlwZsXH++DLv/gRpePAUTG2oTF5UaTTmPzQFRg0mMhbxPywt5tcZA77XKOpQFO2uVIGFPfi4LstPvxTLqHHY5/Zmg0'
        b'2KbB9OaiJ/A2oFNO/yzR8sDzJJuE7pNnO0g/X60v6U24Tlq3t5XPOY9/RJnDUs16ZEEqkmf3EdvjEifkyIntZZzNLS5I1he8Bq3JbNAb46SqBQazVoXDe/htBzQRUtUc'
        b'damRf6cuRS811UhxwdqT3vTUvIdV6tT9LrJkEVf22i++Ui1/7o3n33v+recvtV/f2VHXERdTN7m5a0/XoZM7u+rHNp+q72gbvnt4+/CG4RuGC+796TWKivX1qhBky1g+'
        b'+nN3BUu4QwgS2oRB2JlDeAzPXO6C83j7Tkz6NLiSbqf93cOIy1ExFt5JTUvGWwe3s+mwKS0StEaRAE4Z2CxAhstNeODpadFHrdHkafN1BUailhJS9HMnxQRMiKuH9MB+'
        b'93x2KhTyRLULX/DJM4Y97vToCh7nkkznTEvocR+6XOqDHt9wo8dHQ/Q/pbhiRHFz+6K4TOKaQkSn57EMh6i5kJ6LU+r/PeLD2ZKzMqS8O8nEe5+IWVCo06tLpRptqbZ3'
        b'XN2TkV3b3KUMIbv9p17oRXZ9E51eaCe7NBEV6+NVHmREZEeiU62q0S5CGdPcFRqTHbwGTxBxqa5Ix1QXj6R7k13izhGY8L43cnBSIk+BLbAlKhW0ZLiRHdzOTQetogAj'
        b'3PX0dOfPOzUfQ3oZhPR6qF6RvbL+b6nvALo83wf1Pe9GfY8F6hEnkNBWyuUEkp/fX9qhqOb3QXcECQmB6M1l+YjWEN65eIi7/a4FZoMBMf/Sahcz+pegpO36CYYERRa9'
        b'+Ad8yMnF9g6CjGMfLQHufyf6wePVmhKEjNj08IuHu3lkDAdtrjKgDFwmttMqeBFetMsAKm8UQUZ4Hpl7ePomE27KwkYXshiRHHDBxnAhNR3ZSxfhsyJpPDjU40iZPhGw'
        b'oNysN7mMl7EvBFwk7gsBe2VVOmIQdT+PcbSLwoXnL9/oA8Uu+TwKxXpV+z9CsY0IxfQ/i2Ld4cZPjF7SsHCsg+n00pWxkePD++DAj0e3UskLNEG3vZaJT4JubW/Zed/9'
        b'bz1eGXAdoRs2N6LArTA33gcugFaCb/A8OMxbBDuDqhG+gQ64VeFkfwEJhP1NQJbICf5gMwe+DZrlxLhJwCpEyHlF9QTo5oc78XHYlsdvb9Vj2HvmfFpk60CX9/pAttNu'
        b'yPa4WmUDeq5BFuXlacoL8vJsXJ7ZUGrzxtc8x1yHzcu5fESnMTTjTK34go/UMWyl7H5Wm7jCUF6hNZiqbWKH65LMeNpEdiehzbPb7Ub8B8RYIRoSYdSElEgT+V75BTtb'
        b'uHj9NqLLCsYe/C324hgcx+n8ZUJ8GBIj0uvKBHiFeIf4hvj6iMlCSNgiVnSvK4ZX05HFigxOJDP3ScPAesG6klK3KRFMxwmUfWcK9xlYfrsvWz/7wgz7KJHdeB9KE6vw'
        b'HoLYI1mAV10Y9Fj/ctG3lEjOuY+a4YizxT08nqfR5SPGuR6co8n2EnAruA1uODbPMSfBVsSf7e1yzD6keIpA20yZGc9Sw4MaeKJntPGjI43rwQ63aGNwW+3G2Lwc7AH3'
        b'kD0in3I/ybF7S9Onic3Hhff2q0qUMpaEntwUe1JI6CRUCaWlu/XlVSRg84RSSCE55lc3Cwds7uq3hyrF63HvrYwX3A++XvTfxMGy6yXz8k4P6yy5kbMhbPWi4UNaKotj'
        b'Bi+OG7ZkVYr5RtyJ7NmJPy7+6+D/Dnpt4qDV1XL1fLGoJPA3Q35g4FTJ+MBJz47dNP7lmpXpk0atC+s3JSy7avo1Li/geMWFYfl5v9ddEY3IPqbSTkopec3j6+Spcu8B'
        b'xTkGQe2Iz2ev9PzSuLIibMD7iae9BnrfWPdfpPnvLjjNH/o5D57Fbk2HyzcedBCvbwo4XMhvETaEHBpLRQsbs9f5zedDbwpnB1DY8Ioe2iD9x8hA/qV0cRAVgdofvZxe'
        b's7JfBEVWgcBtoB7ugM3pikh8KGeYfWMw2JYqglvAqeqxmIUmgh2CURTYONoDdoBrfNymdS2/NVl00Aq5oTiRr+LyRBEO+fGLDqqsWD9aw2/VaZAo179VQEiF7hqu+9WX'
        b'f+SMVvT4INV/VMtNb3asZJbslX9UBk0avHj0FI1gePqNWSk3Gwdrvda8ee/ZOS+MFGSeAkH9bk6Yti3Z+pfDh3LC5r3yRsXcoynX9o4PP5YKpuxv871v+yL7/le/3hH6'
        b'xc557z9bcfTMi3//Zvy/Z4jSfKqiXi9/t/hPXkvq/zj1aOOa3792458pIQ82v5LxwrvDzrSO3prUKOP4RXwd8ECy07U7dJ79LJUz4AZxeuvjwK5esUDg/Az7Gcjh/KpM'
        b'2CYeKlfg8yb98UkIsE1AecEbDHymIJH3Lu8HxwbIYVO4IpIGd9PxgjJmMjyQ1Ts4/Jfuouq6Lt5gVLv5j0e4i6xKjkTR+WHfMeNHSxkxHYiPdTnr5MisjcOz8i6C6hdv'
        b'7kobzjnZFa7gqz6k2i6paxwMdqj3F4Or8nCl9wqw2UURGAwOcOAMtKa48Rr3fWt68RrnvjVPxWf6nr/xdPCZDL0X4jOdGRJKWhpsWjGL8JltmaIA1hkY/mliE89nYPjU'
        b'PvnMXuVLk8Yvbok4kHFuyvG4ZUPeDD+S/++Ih+nrvD8f7F1zK/ti2MZZE1L+rKye8fFQ4SDPkA9yZuZ+Mu3m6P2Z0xc0DtkefmvYkplRyZlV7/p2lX893sZuCc+siAk5'
        b'PuHz2X/XHMyu9xofcZ1J8DeOmCL42+Qpk7anPhiRvareyWeiKx8ISFNaJvB8pDY7vzQ3MdK+AryA5yPSsatDzgXH8lNq5Ms2LX/2TUV4ieTDufb4++NjefK/mFyQ9nJQ'
        b'CMUfJ3wDNua5zFlNAmcIAxszQLfg9YsCI56u+z2Vp/hVV/Nibxgt4Z47ufzSA/+NV96/J79o/HN44lIZPW3Je/vqmQ/aP/rjm1/XSlf+OF/7YGL8hEnD3nt2+tQL827U'
        b'BM1KnfXaqY5xl+5fC1/93sS1N4cEpRs3yyOaLx38+64q8NWEh0u7LP+ZUDLk6m/8ZTTxWM2tBIdT+cObBRQ4Ce+IlzFacBA2uiljv3ifG0J8Gm038YW6E986fCY1JjiO'
        b'kB0mQAkhR8P5bvLjaaab+p52HyoXmsOl/rsPmtvkupsN2UczRU5obtB4RHPJ6Q6SU3GIQR4CHW5L8/Af2UezGBFig4Df7dtCH6YwqXUwNQy5ZzUcumfb6aowE43TzKba'
        b'6WWDljI1XA3eFVzQQJkYvFM90iV9LILDrEbQQdcIFlH6oXg/7hJPQwV/8gv5hk+FEfD7b+tfs+ATRxJIGTj/DQtraEepBB34/Jfz6E5IdtTHdQlrRA20RYR3D9eIWlAO'
        b'izCeqtyLaqkn+QV1+HQP1vAG3r0etUNQpUfQCsh+5Ti/uFd+McpvQ/nnkPz8eSsJztxhztwhP5e7ncZ7lzcI+RzoHWXBu+VHLLLvnG4/USXfQmk8BmJWxU/FeyoRW9Zq'
        b'K+YYMKdb8FBgNhUqJjkPBkH4ewGPOP5owNthkHMwZCKDCuOlh1ZvLtMa8H76eBsdmxDvk63R2iTZeh2+Idopn3cKj3LdOz12F0v2LU/Blwx8wdqmjV7xlEu+bRJ8gIUx'
        b'hl8e64t4uDGOMHMxiezExzDwhzkEkC32ObIeK9jlTmL/LyZL1MX8OfegfiA4y58yHRuO1+SXjyGB89KhHOwC62e4BRo496/GVGGhjGINnUXhQ3hI9zNkj3ssD0gXGsY5'
        b'KZO20cafsRa9SaPyTOV5peX6omjWcTYji+0QspXIwhJ4iQcQmaOwkd+gELYtT0BQjgabBNXwImhzOzXFGXY1noCpoUtogwTbFxrWgk+6oTXcYQqfooKAFgRRHbSFHkBh'
        b'QYffEJwR2ptAQiKYUVVkpdZ9hm+LYHWhrrRUxthovY0u/rl24ebgZpH2TcTt8rSPFkcOzeA3294Nj8E6rDMiDRIfS4yal4HbCjYNVgip0UMF1WA/vPyIZbt0n8t2H32Q'
        b'W69lu84iXRZUdi9OM+ZVUB8h2RVgVhU+DJPxL2+NfhGNPBX8SrIq+WvtIP5lzAwi0HJODldFXC0Kp3Q7q/dQRrybX+XuaLyRHN536So4V3eq7uqe324a/s7pna0/dtR3'
        b'1A3fdzvpZJ2ZLvCe5fnJzBPKd2Z2DKoXpHkNbNokPTIkYshrEySvb5alBSQEHBkREvqqOGbMpsWSsBu1kzdphxdEs0Ve1LNdg86Yv0DKKXF03IAnMruX+MITYxnFClDH'
        b'L02pXxnoPMxssIY/zuwAMsiuEDdKwhzU4XjfjsY02BZBw4OwGSU5w8Dz6Hc/EYUh0kpwBh8Cvxk20pRwbRHYzoxABuCZp18o7F9Wrpk8kT8sIE+jK9KZeu5Ha9+XSUzz'
        b'R6iI6RDacNdJWP+/lgLjYhJYR3W1Lr/AbTkwPowUdq2FW8iZ8rWgIwN0jSdb+uJjW0Brhr2vkKpyUri2n6pvloEdQDyjwPKugyZ4yChtArWxQKdDgF2mnDK492GeomJt'
        b'VamusDqFtZ9XRLFE49WD04PJHDvZUwec4ZABsYmBneAWvDEIbugbFDzO+GgMIgQD8UEyGKAaO3hkEohRGp7jAZnmAtYjdtXyMOvtIGZ08zCsoBAws+TgoHzdGNR9brDi'
        b'zcwOwNvaJ+6xIhfAHtlfHvmx4/lzjxa69BiJqbwCjsOm1KLymHHJzsgc3+HsFHgJ7vi/2F8IQF6WLunRXxgbg9PB3lTQtQTB6NA5feB5dmyAwi32zHmGFxaEGhoxdqRE'
        b'VY2wUIZwE2b8bB2DlAmqhuWP+rEwiM0zlZ74eJ2KWAuND93hz4JQ2kKjx8aMGz8hduKkyTNmzpqdOGduUnJKalq6MmPe/MysBdkLF+UszuXFAFZNeSWBRvqAbiWiYRln'
        b'E/KTEzZBQbHaYLQJ8cYT42J50e/Rs+3jYvnBycdtJ6fSEnknJJvEkGGaDw5mp8K98GRMbHcAle8ANg5sBmf7HiaJHV80/GEzZFBecrIK2nDvZzBlXCw/EKU9MAVsWgPb'
        b'U8F+JQKhexSOsdHwJDjT9/6H5Nxi2nluMQLnyfc8pKi+DsjglGQjfljrA9Zn2Zckw51Ibu7ITveYD6+Ci5nocjXTG7QyVBh8litbqtN91hkhMOIm1LxV9pUqB4kdNV2A'
        b'BMtLKuGvTdSYD7ilaROuvy5j7IscY9bhw29bYfM80BUlojzGMaBjIrzEuyiOpSXjBYfEkQEOVzsWHMKGuT937rDOWJ5n0pVpjSZ1Gb8JBDmBxZWfrzK87hwYpm/Htou/'
        b'Eqet7JNRb+l1AjG4AupD8C5XrUSdgJvTFZHJcPMQuAl142iDYB2spea4xZe5Ox1Ze3yZi8sRDajXEwZzum1iizUC314D6q804wikJUFjUpGUbYWbOUo4CJ4JZTzhnan8'
        b'Yvj8ICpCs4ClpKr4Gf2NFAn+nD5i8rgY0BUTPX0kNYISKWmwz7yKX7B+0gDXo2/XYsDV7Okc+gh20eCaZxlZQg52rgwn6/PB0fhIKrIMHiB1HA4eSEVTkxhKpbK8WWDk'
        b'1ZcPV4ZR8/xWitDLmVfTYu1b0zWBmzlka7ql2VOoKaMhv1vchUIx5ZfQjFfsp42NFvEF/L0EWflLBWSB//qsSoQcpK2I43eA1tRkcDZCmKGnuBAaXMoaSnIMi5pB1cbP'
        b'4KgKlUGY7ckX89eF0ylLAhJ10aqYf5v68y//GIl0K8vzeDl3GpUSQunU678VGH+PvvS/MjKx/fmUFxIk9f/VnDgQuzBjzXv9fzO0hvkjaN7wsrR509DTA4Ybu8Tv1/1p'
        b'5JXyLwPf3dHu988fPvOtrNYFrvru1RfHfl/1WcwsXUddVXD50sBXh92CM+rPFx+b8QlITP+w6qd3i95Z0dE45tXvbNoRnx18+XbWiY9tk7epfcacfsd0bG/eiuFgSYH2'
        b'yzMf9Pt+0Jp/nfh+68X6jn9ekX8fHPPn9qPbuq6FZ32X+bcH265VnTccP7DjrR8KDt44GfnuwiXz3s/i8q37I3K/LKh8Lyf891H67//871aRxNL2t6iv/yM69ubMw/dO'
        b'yIS8PrcxC+zkeRC4MwNHki5jtIV+RJ9btRhYiT63Gt7oPp/2ANg3gFf39sODy1wPwQWdSYwC7kPkjZGnAp6k7EG3q032sFvQWAQb+fUH6+eleIGjYIvbEgSy/iB9Dr8G'
        b'unYguJVKVikjvnSGWUFPh5cLn2Lr7v+B49K7AgkcbR5iO5Nio8cShhPXk+Gs4WjefcnRPqwEKZESxDQ4egTNkIXAAf9fe18CHkWVLVxbVy/pdFZCEiCEJUBWUARkMYBg'
        b'JASCAoKA2iapTghJOqG6AwErLqB2N7uAoOggoKIiiCCKouC8KnXcfnXUcWnH58yov+O+zaiDo/Ofc25VdweC4rxtvv975KO6btWtu5x777nnnHsWis3nNg2I1RdiyIn5'
        b'5oi66lvVOp+X4srFsdU/41tdUF/kuEQvHlhXe7fIbW0X+SZ5lbxPv1E/XDylpIhsShDJHR42XL/LWDtM4gbykn5jubGa/HIY2/QtLUga9OOMzcb2fsbVgTrL+K+LmhB6'
        b'Mg/zGEowAmwTRoALI4to0yS1RLPBfwm2VFs2lwm5ekIeTdjBk/qteeQcFhXR+m6lyALDQi5RrQ1LO+C5Ju4UoGRGJUnVXfjUWFRDJLAoumcm40I1KKwnBZozY3s2nBTb'
        b'kwiLU+wXGMxsm7WZy9zy/NrmVuAvmPZOd8FIGTUjRm3tbW0+VcWNICoRkytHpaCvIwhUAhYRaFzuizoDPlQqCmK0zaWNSnCh+lvMLyq+k6ONQgNfwfuXY5PVndiWjaLl'
        b'op6EGDgTYU4K6GePxtu4caxxuMpYZURmMEYDHR3qazqnw1Lua2yXjEPG2nldKMIYSFk8IwInUiGCmk3CNQzSC+O8A4GMAepEBDKJ3gS1FsZWUCTIIWoihjnGoI6dIo4h'
        b'lTAfnlKQYXwPucVZnMJiicnVx4eMu2R8R0tzWfF4ouwa/Q3nLOg/+NIhCy6Da3Eh3pcVjb9kfDnRyR9iY0naZIqjgHFDwjkqB3w1at3CqK1BbW1vi9pQ2AM/za1LYVyI'
        b'4peiItQTtbehIpbqj9oAjvCBw6r2p4juVPR1CF97rcw7REvEKUqWjwByYchQhcQ8ZeuRi2XywavvR+cuemQGo0jJu6OdO7tQGibrW4fqd8foii7njTfRUAC5LWRySIAz'
        b'tkHtQEsVdSBed/A7uUCZJihAoGucF21YBLUcr/RmsibAU6EjV0PpZHonMSNQntgThoXnFk+dy75oi32xkX3hz9V4dSO9W3PiO5MAlaqjvOu4kJ9PowHAo6n6Nq2AYE1j'
        b'Mx7q+Jp9LTAGviW+5p9YdlF3m+oLohUlgvj+OGTZxMaTI5ksEFLJZTtRa2nG9UakeMjU0kLmS2uNvl+FRwBknuun77INWahv7d6AGQMNx4/PARNx80WfRJHuALjzbZvF'
        b'RfIi+3wHPLMpMj2z++yLnIrdSgGZZwcshubLjvkupT9GzYN0kuK+1jk/SRlgppMVD6TdZlQ9iaLtpSip8E1yl2dpSjo888SeSEqGkglPUrrk6qFkwbNUMlvm5qcpA0Mi'
        b'cAtomOycn64UUCpP6QupDGUQfCNDC/KVfpDOpKgMPWjQBkeTzoMx8fmD5wKXFZt1luxvloVT47J1itHKKZJ1b7F9fCeN+4f/gH/H+TFAzU/k4uHRpsYGOGENeWlNUkzo'
        b'QFtNne/JGNskLO+d0KyyEzOexLVRO3E7RZYa5qclFeGroQGfEVIN1jR0b7YVdbY11zT6vZDhmYQG9EhsQCxHl5oFq+Z0jlmLtXqsNWiZrglRmxfRPq2DU5iN4Tp5Kc4x'
        b'Lk9NrBk/7jIssUrdNCy4yE2GAc3U1C9/GuhU2e/i3ezCv8SkvW2xEUck33ExCaZ5M4bqFDxdYTFTNVERmgR1pIJiAWEctzgbnkhNciBbsWki/gKi5/HkBJ7Y2VdZnJV3'
        b'LpSPsYNprK4tdFQf54dG+aLjQtlQ6AH5lcVFqn6Kg8Rfcdx2RVFnQQA3VxZt2gVsoRoMLG2EjXMCF7dnIL/o0+ijtlPJlL2AYWDv9ZHL9TdFS62KsIqD4tDkYjCInC6z'
        b'MPGb6phHSjERcnnWHCTIBZlAX6AIybBerGES1ePYClugHYgEpA/8iqWahY2PumIz/RTCfhWjjb8vmtwgNrvrrMES/8kGLow3UP0eG2PHwmqAgkloofoDd0qa6UfEAl2a'
        b'lnFi06C0k1BNTA0xDJMpLCGdEab5vQimyVqB2spbbcUA0JolxsODBH+gpaYNWviPWLNl5lPfXAtRu4+14bQ0jVVc3p+Kph0ox4Jy88vTE/vBiu8eyMNYN4RYN4RYN4TE'
        b'biDIeStCNXaE2t+1G43oMyhoAX80XqDzp6cxrULp3Ndd+5F+Qj9Y+V2GIyY7wiO3MLQzLEI/iiyMoOYjBcLCN3dCX5AExDUcFMzJJGqWjFWENT2B0QOSihstnQWyniV5'
        b'vUBEYZR5r9fCWOdxP+9DUZWgU3+LHQOZMbBhmvXssljjhXc/RpclTrWyn+obGyV/UWxEK8wRhf2PRlQ0R1Sy8poIWapWRd6kTq2xtTEwoNVdwigDLAIxWIhxWBAKP72h'
        b'tpleY5mIzIQKRo/3nASZWFU/EWfTWlyzLdlcdzunw+utbW1t9npdUnzjzOxaGctgEuezY2NhsRgUdxyVvCkSN1eP1C2P9OutsLtsFdZZ0cYrACx/4mK04TJAxo3+YDQF'
        b'aXDFV9dcY1lmRx3BVnawa+0Hf6JG40Dkct2JGWXVh+FzPFIMZ7lPWCMsQ8VJjaeJlB9rvEKTRRHWSsT38EwBgaYCEEhS3Rln+dHgjUXgiTp9HXXN7YHGJb5oMu5hXmAg'
        b'scbA19i0fOiYP3BO//50coqolkcsBjtQM2wLVtc82KsUvLzTXddUdM6TLlmnAiSU6LpRYJtiax8/jvEar8GlEXiMjkW4XZA2w2WsW7R1SDDngS3ficfVfA53idBp65Q1'
        b'myY0yapC68OWg4F6hMBsdt/A4+848w3gCBmR+GKPJrPniz1zuY4SWFUSalFAbXlQpr3TAbXLmh1qtGsOBK5m78lBbo04FXunU3OqxzQ+cL+GWhhOyCGO4/yS5kQqJfCs'
        b'JgSeVaAXkBe+buStdUln0rg4j9sGIIlV6Iy6YU0Aw9jYrMBwR+3BVq/SWBckZQTaD2BHCcK8qo06MSMuoACRlozP+YIjMQ7tNa66Vn+Amc9FeQXPMaDQKF+nfo5vhTqF'
        b'+Waaan18io00EyrtKVlOqFDeRGwlczWXKrj5TIGxQqjJ46JQx9IJm63ZCSINkRS2Q5GzC4WKikK+ojDrRDVf6s1uqzfqR7HOfckxhhr5ZEYZIP1BOz2BhvYZwsuEhlQZ'
        b'L0m8OQGpIwmxpk5fpJcYegpbo4vmenOIDsltcwhum0fyuFOlVClTzpTT7ZkuhwRPbMx5y50TlgeMtZULjU3G2unG2uLFU0uqbVzOBKnC2KsfnF3Ik951x/BFCdZKBoV1'
        b'hNznNBYXytyZijw7r7yQKShhQKv9VRjtk4rjuaQrBf1mfadxr36DcWeXcxzEFKSg5IlhB403kRlzJ9FS0+SzaBIhruvSzYGtOaAj4ziWDpUc+vpFgYTGuPTtAnC8643V'
        b'emjoSWdB+C8wm0tgdVMpTB/qiwNjCyykBEwqz/xxzWfx2YV60WRqZfTKBXnsiltJhl+H4lFSrkWvXqxLaVH35PaWlmVmU08mjmljQTULxrHAdssnsJN8nJ1kAgW4iiRc'
        b'kEzhgq1a/Zgzt1L1E87kCmBnxCVFnCabsy8TxLxIpvtjRBMtO5k9O5EfWgWXcilGIcl8Hvxf3iOxN6fvqcXkwfL5U+6YTqBKWEMmx4aTX57VpbpYlu6JMvNwkkgOs05L'
        b'nEk1VnQ7ixi1hRjM6z0/oersE3oay9R95eU0hAoPXJ8btcKIOgQsrw4MExCQ98ZmwQALKOBTz8QBTGhuXKkJsS+MEA0gQowIoy6E4Knlb4RrpsapHQcJ2zwkauuuS6dF'
        b'7lyLx7ySVc8pBtDu9Tb7/F7vrAQYZp5QIWXoXlKA3QhyDdZhP6ECCfeTU1NY+NbrnZNQ30mzk3L8TO9QRaTiJ3pGSHveT9TCCDlssuvEjQMXkdofx3BAbCMYiJdBsd3A'
        b'+TMD2hcyjbUG1CG6ZIfoFlOdgOjFdpTCp+lbLg8UIprW9wUZ1tPvNnYQ5svTH5GMrcbd+iPdoz100GWhvc3iInGRNN/mYypeKL+TfNIiO9BqZopO3RElOuY7mMQN0CBD'
        b'i06SnLkImo5o+ozaRb66ILmiM8H0C8RDC9mOjFvrzwmH6mKjIi7veXKl/yUyooXx3eY/EQ3R/GhOmGR53XTnVEgoFukeFbeXpQY5k+0y2U8JGNAmlzqMqewSOhI1OnnA'
        b'BsJbG7xVTIVefodM7N58yGGPs3xYTrxTCUp+CYycg1g2muRRVyUwBh1MdfVzaxFEPROJUGwPmkqtMcb3l2C3VikmlBKAyvPQfxRPnRpmJv+YdOLyHMwnEnKMwuvddbXG'
        b'qbNuAg3GiTAs6VLJxGMOiRFgbrG9iMOARunGIeOBGcaqqXUd08tQlW31tOmLEyiUc/W77ANG6qHuV2luwiolUoROBYE8Mc1No72sfltIaRL6zJzW2trU3hY7krSZkyUj'
        b'tvDM3SoMQ2kSE4Dm+RhOsjGaXQoua/Opa/HWGZO+nWIvlZupzs44wwhsVf+faF0Z+6Aby7rSWDtOWipF8Gq5tVQACyIjoj8o6RsYjAnC+r3BGHwXG+sqS8qMh1AD1lhf'
        b'Voqhzxc36DtdxjbjRv1QlxOlmBQEj7dhD+dIrtGbFhSP3NIO4NN2kk69WhJGno8Ly8jKhjm6t+0U4vJ1Om4TL54+DeYOsqHRpNb4BCXu+5eG5CqDrl8vxRS6mKMpOstE'
        b'OnmyHknTV+t3Jxn3Gw/CajYOcMZB48AJ2F+25tVlCfNKiZ+0yPU2OuNxzhdJVUcGLI/nOw7YASQ60REVu+JAYlhxKi4gduWEcx3HfDvtBQ6aUJ6o2xz06UDVq9UVXRxp'
        b'xIB9B4eaO40ARIW/VQQW2hI/DQSKl29ErTtgk0m8jjSyoK6JiZzKNcF8A2RVDgd0soSMriYG/HhHaSkHSkcGG/rBBFhCR29NmIyH4Tb40mblInY7OJezRJGLhHp4s46P'
        b'Ca5klACX4NQkEVUfQhN4F3/GzviiLi9JXr01zc0MLSIpYDlVoIw/0IxoU331jR1eVOUjXicq+AOnJ9fCAm+ULCMyQUA9CwFnBDpdlsj5cirFhnMTdxw7t6GRiJPu1uy3'
        b'cwkqCwdxQBD5w0RokPDoGiUdPNBnnWLHRg1PO1YxSQceWwfOJumHRHKLvA5/UNAkPNxmx4KKfS2Ceo4lCdkhKQ7YYDT6BqcQDQmsNXklDDWVUQ3PXYCbNmMe9sZ8TisO'
        b'LUVWCuzJXKhxLqcxVJhUHbXNwrOPqHieX4lK1RiE2janprnd1z0Bwk7GUE6jCE2yKVFjqgqCOgLHdFQCHupG0ZJcGz6EJ+3kW7K0K4zrWv1LfGqQRA2BRK0I5nESiiRZ'
        b'ZmwLtWQuNpRnYUQ0nylgCVBYNyZy+Y7hDULOYsC3OGprVRWfitK6QHtzkKjmlrgg5acO6z1dW7hHMqUIHO82OQcXzChBQLXRTLjvjVZRrmx+ea+f6GeXk7OYMBCb0oAL'
        b'r5xmz8hOEcgJUmshO6MynGEkVRZ3srF2aSLsT4AfUWUCn+KzuexMABkSpNpRaAjw8sFYO7z1zaiu4CeIWWLAsQjZc/BSzv80ZTER3j8T55sk80iAHKSesHLMik7aN2hG'
        b'oTOwBHsruGrYi2w8lCHmHtbUTlQZhndMVg5vg3Qnwt2UICAiTciC3WYFT/oEgLJ28kSywSqBNaGg1M6faj3BPHhqqNjYHTwBiGZxlo0JnREKXi+bX1kX+Zv8rUv9+bGd'
        b'PL9/QaD/cfmKggAeIcpqGgLrW/xIZhhMPQOf4HbIKDUxTsWqw/mTFkQ02etHxRt0iQwFvIwgzUqYUqmmAD6Ll4VUfnluV9AmftoFMyF8SWykcInHdDRjcD/GnVlgd41c'
        b'p9QxiKnXmJZiiHfwG7Ji02RNIkRfAoheYiczi2AbqIeStguI7i2GQFYreHNqqOPxQuuPziWA/USv4kBU2hNEKQ5LSqr2wGXrZHJR6EvCcuxepIn+oP4QJ2wBRiIKLtMJ'
        b'ViehbrNqsRqWgLNbnnN8rOHUhfO7krKnGcE0Tt4C78DdECdvs3qk9gUW1MPcM6y62FgZl7cZB6Yba4ZNRp9GeT0l/VH9gLHnJI/V+I9in8bojxTiLi26g7mPt6gOfHMi'
        b'xYF0sElvkP4Iit7YwKVGHdNa65oqGpt91R+wqv4wPkZ3dDnOxwEJE+eJ0ymQGRQUnhYe4wwFekeHdlkoeZM04Ju8NpK/ySSLs6O5l9dhckNS9fEMjOyar7T6TMfv6Mbr'
        b'uL0gUIYqaThYdIwtNwYwH62qqL2mNoAH51EHqa0pjWrUjrrdre3BqM3bQkFQKGBs1O7FHD4l8Tw/KmEO9UK+O0oZp8JX8VnlJuIgnQgEmV+eZoHpZDkeojSXBaU1nKW/'
        b'iEIsNGPrWLIsNYwLDpAQIua5nH+OaRi6hAf0xHPLz9ZgUQECF9XyFfidrE4hgRcrh2+S1EuCdkVAaMMzh2KWo3CI3tCMbB63OBX4TInBehak5jIqrKHQVv1hGmGzutb2'
        b'ZoUAXVNHLufzEUAfbLsZ/90zfnahE9gXACWBJ2praQLgqhfQedGMWcSCRm0+VQWsMxsfume2+zG7+SbQ7PO1mfguaodNhoqqPeUijkpY+98l89yOI2tJgaz5XeTZRKIR'
        b'QPPe5ckx2OM33RtblHBMOqIOUmg+wmzkLZirgwD+kgV/c/7hjmijrrCpYWsMxDpsU1vg3pSldMO5tfuxIcm2BIEvmoosT4k1lOX4KTqK0YiJApW6Uwt80eGND7BYhi0u'
        b'9EhNmJH0snvAFCXUhlPSlLEKTMZKInIAjGmdSy2R1MsRKjMt0Kiz4g3rxl7F6wVki6LDLFvsNN1B9DQMXXpCI81sXVRu8T+eYpN9OY1fliXdQuAw5UM8IOQttpv0SmbR'
        b'KNU1t5reziz9DMnr66jrRvoJqAVWbJ/EAXOduKpZHmTrq3iyHO5uqyDIYI0oA+JUH14Wno5kcipk+sxiRh2Sx+VJc6N00k5eUub1dKHTnhnGuiXGav4sigGdvEh0uY0t'
        b'XbYDu/lLO3tMzIEK0BIwmjFRByodzpeU1BCLkSKG5JCjXibxoxO2hTTGmlKUEzyJccIWwbx24XlMV6Y0PSpVXDC5oguyi9EXkzmUQ5tUAR1bI/tnDRj8QpvCwiIJbXop'
        b'bVOEoMxS5pZgWakcT7pgGVZ0Zv6SgsDxZEiY4aAhaQnLVtFoorPJtpoGX9Qd8AW9bWqr0l4HFL0bv/bOOW/mrMoZ1dEkfEeeSQE5JXm9ZsRkr5epS3sxFIdFncVPzX5i'
        b'/LDuIfEJnk46pLDkk7HakxnEU8lPzROC42mzoBX5LTV+ctyIXkoQAyyOT2Xm++BEchF7FWv/0BgyEJanUzO6vK6ONQalWU4LH4QTxgyXGfqr1gQmr1kkqJeFgRvFO1Sr'
        b'Bm5SBA4UtvSVTAmb7jtFoNPFnhzq+9JT2OR3yExNgahLXl0RBhpRsa0U1qd2SsDf2jXB2rIu5GZyF1vaSjIzU/waF6WroGDWeRdMzP8au8q08jqA33cRMR4Vltaa0yAq'
        b'w2bf1h4kaEVtSntLW4CkR6S+R6d4UdtSPFo3pXIMiRE86ROhfuHpmwSrS+GT4TZLeZhMfmUzpryb4smTq+Qkgj9rWNQ5xde8xBdsrKtRR2ERZKWIg1BniZNSEkekjWdc'
        b'0E7UFeJpTJACJzVigLdoriSCL90DzwNUuYhvwnzQBryfLZNDvUr00sDSvVjaocidTsXe6WJygc6kDVzHjzDeSaSD+VWnG+h7dw7Xmaw51aetvFoyjCZKHW5VnJ3J/jxK'
        b'uyB9REmCt1b9Dqx/cbBrezS3BoRmNtfEqX/AshV3Ty6Ha/sTlOTRPOhhQknWPE12vNM8rB6476+54epBMbqJOaBMxaPZsUxF7HRCKzysFfQlvEelZ1YnvkfNDMWu2bRk'
        b'zQVbv3MRXpMWuZW0tTKU51KDmAvFVZpMMy+9+kP0e/0hjsTsD3HMPwhlvfnCt7P+Or6CZBrHxXPOOYeGLip6AW/wsxlXyOdH+XOj9kmt7WojoB2+ErVz/b6l3g72s6ww'
        b'mamru0i/tLnR7wswdNRSozY0+gPRDEzUtAdbCY15awFLNUUd+LC+1Q9krNra7leYuL8Z56tU52tujkoXX9AaiErTzquYHZXm0X31eRfPLkxhc5yOrCUqQCKzEFsguAzI'
        b'4CRsgHehr7FhIRTNWuPCDN5maI7PvAfeFaqwqT5oRVSuZTISp7+9xUtfMD1YCe/hqa8jSI9/NkxxEtNuJNXliTaTheDM2IhuOoxIJasGFvuQ+bpzmd4yyHuG0JtEcjJ9'
        b'wZadZC471EGiRZdQyUnSFNqlVK7r+qIjm950toyMzFRFiHBo4RMUiVHC3dOBcpeVpj+KHLSS4BVZ47OYNp+k2BGbBW2m4FOO8cMiiT8dNMOcx3PPrVHRkDd/eGv96HzU'
        b'zsonzwKB9hb1a5xLxadj5Fxalj9waHFBF7Ippl+FSIkslTyd0APG6Zs2SvWWJA61PS0rpdxuWR88Gm21dhOZW96XAItNHz66O/ukD9FjynGpqCBQRGulGpjklzhT3Iam'
        b'LwrpU0dF6GnUQzO7EZjwutbmVtXE4axwizl7ues+3NWf5DOxdt4NrW+0WXIn9DxENnMo1zcxsFksUbFXkEjSQsCqdmqqLsCbiF7dwZvVJAgAfrHborgooBFKGmiLiQJS'
        b'7Q4p25M5hKxQp+nX61sCSW2LRU5flyUY2/h+xoNXoFpZbNcnfSuxuroaFa3EdsRVk6YlMzO69kC/cuN6fEXmqA3tQv1ikcIpl/QemAbNqGhUfndIDKwCis3/R3n67L/N'
        b'zWjI/NUzys0DP/k+L3PxPUn3Xr3qjEEHnbmp4qeNM17/+OJZTS1V+1oGf5ryzOjP37f/aP/7jKPv/GZpNM+z9eZvP3vrc87bOtk5MLgle+HNN706oHZq0xOH5oRzLu1/'
        b'/ZHpzy+68aZXRtde1po+9tCUT17tUbv1s7RH/1p+4PwPIkePTPrklbeeuPLtfM+fz1h8wf6M0F/yFl98ODxgfv91H83f3DE6un3jvGXPfnvGmsP6N453dn838ppn5rzx'
        b'RW3KrCGHHtv9zhd/G7c26ZvRaVe8t/bpyZl/6F8/v+aV1vW9Frz3bnr9p99fu27T8MEF91RUXvJUj6Y++R+nf2pf89iqpqdec9T2vWrDm6VHDw4snqlMm1d0cPBF9zxz'
        b'4auRjx/+7bNnHtn6/Pg7V++1vzf7jqw7F2cc3ru/+Jva28o3vbtubd+a652j16k3GY/dM3nOlc9tOvT8/SsL5m3ql7NVfOGWJ4WsBf2y2nfnHHplS8b8OYVTa5zP/aX0'
        b'Y9vxc9/ef0VDub/pu35/vGJjv7tK1isL8p67cvO/ueY88mR5x6c7z37psTmfzlj7eI99x6a2PdB0F/9j7SVbbnhdmXhcuTpj65tV1y1b8ubX3/3t95881ndp2+vTflNa'
        b'8O7lz7366NMPjzvcPvc135rnJ72wNOXjT9qO3vyHa+cZRmfmgrxVgyP1ExbIKdHH7jw65a6/PP3YW18Oe/Tf3+/8asgfd7710k3vtt9fsb7u06fLls6ueP/WV6a8eekt'
        b'q0sfWfC7s78f0Pxw77dfGz+kYv8tb6iv5TWVPjdw31tvLH6tpki/+56nS8Z+UrD2N288eGTKgh8vWrQoZUbvK16Klh/Y4/oi86KG2w59U/zeZ+/++s0x+z49+G65sfOB'
        b'pdljt99ef+j5MTnPFZ/5jeM3fv2lIu2GX1256sXmUfM+Gv/Qqss2PHnViCP9XnzkHy9+ed0jMwc0DB/15zc3Nez9W8Ex9fXnHl1743vOT73v9nq96vG1392Sdvvev5Ye'
        b'G/vB4fPrbnu9ekr+c//oTL7Q8Qfb0B/O3frxNUebf33XwP6PjfvrW7bSW+/8bvtr3Du7R992vK/2zqslbffNvfut/UNrHji++4olX4qXDX+96d7cd5apBytfXN8x6cVe'
        b'b+9tOGvhoA9fnHfVukeu1Bcc//eD1QvHLAz+ff/Kxl+VVz3ZZ/qLr43c9IPx4/ej/23QjfM3NO55r+Hvf1pS+3ndXdPm97lozWfPfNdj8N62XYc/mjfrmt9tWtd47OCk'
        b'b77t9e83fPlC8IVxl75wy66HPlBufOWc9556yLd+2w99Pn9G23/vX2997sl/HB7z5OOzvvAcbf54QOHEA7+fe7AwibzaDNK3GxuM1f5B00sr9TVDp5RgdPZ0/XpRP6SH'
        b'r2K+0+8yIhiRzlhTXH2lcUtpERpDPyjoW/QD+p0UrgdYxbGBq4wDJ4dO1u83HkihPJ3GQf0GkjeuGHui+mK+zuK+lc9x6av1g8Z+PAl1ojEvhuvUHxe9o40NQfTZVFZi'
        b'XFNcXUqGhqbkEu/XVZboO/T7y/R1zAUUOy/Wxrgk41BO8Ez4sChJ3xWXdi6unF6l39VWYqwtPPmY+aoqF2es7x9EeYWx9irjRnZArd/ecGotgKnnBEcgqDYYK/oGyig6'
        b'zfr2LkfZAWNj12qWGtuc+kOSfoAi4xUYWy85QRo727g6Lo69vx/Zu59l3HexialvM65lqHq7sRNor1+yM/zMvjHqP7Gw/18uhf3Y3v2vfrHkTM2tNYoZQ/D3cOFqZDKX'
        b'P/0/l+hxeiQ3/GW6Uh1ZGZmZAj/kAoHPzRL4gSUDx/bO9tiyJ0iCwGfzI5uHLHHzDgemBqUJfH/4n5cv8Jky/HfkugQ+XRL4LDn+63HiPab690Zpa5Yb/qfgXWZqHu9q'
        b'dSPdLaTacvtn8u7eqbzL7ubdIr7Pgy978+4FcB0h8Pm8u1q9Jyb2SvSY8r+zuJtLnNJGoF3OWRTsro5Ejwos1NZ+LyDj9eP9iFJnTNMj+no758kR+xjheY0vv/cXITAI'
        b'pte5d/xYuvGZmW9NSL2+YeC8r9Z9+/blwzr4NW9K81KWyfeNvnP3lP5NZdfe/ny/3R/dduz9tC96vbfh/GfEO0fsnD3inVFvfzTnxc3HHAUDrhxy1s6NvSobpoXm1R95'
        b'XnilznNzTv2mD4fvn/7dpcOaBv1921f5+9a//Gy6/8JzOz7fM8F32wOb5452Tdvx1W3XFr1q+/4lqdcjWYOmPPHsD1++NfOxl+uudy49y7iobO09tdtmnZex97HQ+D2T'
        b'/23TBQUFtVu31Ocs2/Nqjz2PqXk/lte/+kLFj5tHfrz/zmcGn/mnoc9Lv311/paW0M23Zzz64tdX/rrkgpWv9+/z1fxdvW4pDpQ1rB0788X517XoR4sXX/T6lKk1t7ev'
        b'+2xe0/3/Z++IN9fte/CNb/Y9+Lcn1u3Z9n7V+csW5LTPLX8wo2HAa/4/7Zk/d0PTB5/99vcHZ2x9fvm4lybt+fjSoo/OGbPxw2d6fTll/d17vr1nV8qfp/74+NozLr04'
        b'b+ZzX4UrtmSMefDWma+rFZ31w7d/XPfsG9Gs753L9ndWv5734sfnJW3//eElT215/5Kxl30USD++ovf3/sHHXp176N79jTsnffRFZ8muXr+79JHHbw29OPUl/ZtHL23Y'
        b'+Pxzt+zbsOJvrz28oLJu+JXL7lq+/vPDv4/8sPKjwLi/+v5ywwv98v/46/f/8fQkuVxQbpiUZ8u88ClP0d27rh+Tu3DXdSPH/HlXqFzOru15RXZNX3v2u6nn33T5qpz/'
        b'e/ZTzuoDv87ZcvZvbGWLr2u69uFHHr9IHKG9cN8PT7zzxeYZx9KX9v/2076vHnvj5b4TC8tpk6vVN+gbcVLpu41tGHLQWF1izquZ4hnGJv0eIhVm1U/GTLStw5aurx9m'
        b'hOxcmv6YqG/SjwxlXqZ3p060Ahca1wgiJ1HcwtX6HUGUphgP6jdWFOv3lcicMHKBcQ1/+ZI5FItev6lA31FcVVqEDoYEPWysp4hmFHGe6zfLlm5s1rdSrCXeadwcc1St'
        b'7zNu6hq4fr9+vbGJhfM4W3+kqsi4Hn1OGGsKMXuxzKWMEptmBmjTris5y1g9dAq83WlsgpZO4fUH6vT9QVTnyxqh76wy1g0ROME7xM+XX15F0WiGThSL0fv1DBsnT6g2'
        b'HhY8o4z95Femua+xlWixIaU8J3dMHiqcYdw3nmDSzPWowleFlaU1xnaBc+iPC3oIALiXvsw3HgV4rZ5eAgwrEFjbNH68HmmgFvJAzO3Q7zVW0bvtRkh/gJ99xWxytd0f'
        b'CLfNCR6Z9OtqBZexeTmVmWrcspA81+F3q/X7O/mK8fo66sLZ+grNWD2jjOeE8Q36Kv58GJOjbAweNu7vYWwYBRWGgQIrmmJsARAgaYX0VMFZtslNkDMfcl7l1q9Oqi4t'
        b'anNUlbqGGKv0/RhqMlc/KunbgADaS9PlrEYdJ9JioGShicXo1KoKCMueC6Uz9V3GMeqEcYdxVL8GRmEqNOcKuL+Jr9CvNVYyVz273ROLjfBQOyfM1Dfrd/NzjXuMozSP'
        b'lFIY5tVAlYmcsNzYdBU/YeZwNv+OdgarCDPCMJ2ZXShzSfo1gnHnFIUF7Xy4BEjZGTNKK3EYp+tHxti49LGifu8cfQ9lOGemcbhKX12rP0qFVMOoyZznSnGyfqCKap6n'
        b'b6mB9urHjNUyx8/ijNsvXExjVZNqrGLO00eNt3ESRvPUrzOupVYNMR7VD8E43EPeOPYN5TmplteP6btHUUf1tcYNxuaq0sKp02FezTLuGSpknT2P2tMwnSYxTODKSn3L'
        b'VKA7k/Sb0F3io8YRgnLtJUC8rk7Q1MzX75eAU1gpGlfray4jl2gXAEjXV1VeqG8sqSw1I456jFVidWEtW5U3Xm7srqosqZzS04Zum/XbcntQ4cZBaPg21qvpAO3Cyuol'
        b'UDisFv2I/rBGhY8rNW4vrtT39tT3DSkcOhVmaopxu6hfbdzhYq6g1ukrjEeriqdUzjGugVWWy+s7jS25LHThQeN26PxqXPXrl+s74fWFPHQtZGxnDQuNKSueqkeMW20c'
        b'X8UZN+k3aQSW+X1hWgNTtA7dRGUZq6YBXDTBuFXfqYdoYo00jhkYHSU8fdpCWeakVB5mZliPsEjSO2v1jVXA5owY3qZfy3N2Y6MgV5XSULUYK66qintarE8yfS0+nEwV'
        b'G49ML6uKOTmEcbjNdHRohFtoaQCrs9Z4sArWxO5lMOGt9enRd4iTjMeN1cTdGRHJeDjuWXIplGM5wjzSMJxwMkz1ffp1xV0dUGrGAzEflEOCwwhCOMkQu5TCSimCkYLl'
        b'uhGwyTSCzZqqUn1PwQSJm67fazeuSctgbVxtHBudNKXe2ABsJVqbramqhJmVadwqGruz9bsonpF+1FihP55krBtaOrW6HTNVGg8ixYFZRywwdhkPy5X6kWICS1B/2EbY'
        b'r2zKdGgjIJckY5dgHIZZv4Y55roaunMH+WmF3aN0QRkuzAcE4wEYp+toLjSPG1dsrJsGE7WksHRq30tsXEaeCHtPyLiN4msaDxUZd1ThygWYRCpLpg6FumBQfyVzJZzN'
        b'uPkqYzcD3A36rr64TwWHoondjELg3vS1uJllFUgitGEdm9pHS/TN6Md3xgzcZ9DIo8oObToIi6sGGo1wKjJWnAXTxFjXrh+atgTnKODxaXYuB7o4L8k4zMbyNuORy6Bd'
        b'xgEsC373AXmfZsCmuNOpryGfZQH93mKCMqCALfoeOyeV8vo+ffUC2tBgtu+rwAYPreptHGQ7IG5/2OReAyV9ZbF+K2HuS5wGenQvmm7nZMk4YhwUHJfZCfxiMu6xZmcb'
        b'9cdLAbrGnTCZZhj3nq56ksli/s+zSv9yl9jxLrFtO+DCJQmCgz/xzwWMEVNKQd9sEo95POyNeWhhsnBMaU9wmXfwnYCBehzkLz+zS5luKo/ywBs32eA66GTRLchix1Xc'
        b'yX/5Ms+E1kzjAPUvAr5ge5vXG+fCLMn/Hj6xf3jD+I5vE91U0ruYlkEy/Ef/GXjOH3gCrrWcwi+Cv8ic8BxU+IoMhl8BfgX4FeE3C34l+L0oPKeRg19XeA5apkX6Yv5F'
        b'mJMP8aE5lopaJ4fqac1iixRJabF18i1yp9Bi78RzPLvibHa0ODslunc1u1qSOm10n9TsbknulOne3expSem04ylhMBVK7wG/afCbAb/p8JsHvxnwi8ayMvz207hwCvym'
        b'aOR9JpKkoQduPpIK+TLhNx1+e8CvB36z4LcAdabh165Jkf6KPdJTESPZSnIkR/FEeikpkd5KaqSPktbpUNI7nUpGJFcTFS6cg3rZkQFKZqRQ6REpU7IiM5SekelKduQC'
        b'JSdyvpIbqVR6RYqU3pESpU+kWMmLDFH6RiqU/MiZSr/IGKV/pFwZEBmvDIycrRREzlIGRUYogyPnKEMiE5TCyEilKDJOKY6MUkoiY5XSyGilLDJcGRo5QxkWqVLOiAxV'
        b'zoxMVYZHZilnRaYoIyLnKSMjE5VRkVLl7MiFyujITGVMpDrsWslFBipjI+cGe8JdmjIuMk05JzJJKY/MVsZHhil8ZLJmhzf5YUFzaM56hFJmyBPqGeobml4vKROUiTB+'
        b'Ls0VcZNeSdwnqSeUEsoMZUHO7FBOKDfUK5QH3/QLDQ6VhYaGhoUmhs4LVYSmhKaGqkKzQrNDF8F86KecGyvPEfaEHeHClULEGWIxtVm5bio5NZQWSg/1MEvvA2X3DxWE'
        b'BoUKQ0WhktCZoeGhs0IjQiNDo0Jnh0aHxoTGhsaFzgmVh8aHJoTODU2GmitD00IzoM4yZVKsThvUaaM6ZaiP1YTlDwoVwxfnh4A4UCbHcieHRPLqngz50kMZZmvyQwOh'
        b'JYOhJZOghurQBfUZynnWN51JYY+WRDUMom+ToJZkgmc2QKg3fD2Avh8C3xeHSkNnQHsrqJwLQzPrc5SKWO0itFWkkqQrXTiOne5wQdgdLgq7NXe4cqWwEnUB8EkJPSlh'
        b'T650a0mkxXM+cx9PevfM+hkxRPcKY7g1MhOeMNfkVHOD6JGCW8RbatamS4/jPQoCQwrzG5nuZk1+bXtjc7DRXyiol5JRWMK2cyrvSd56P0nMUCssYov5l8BTXnWvZS1S'
        b'KAGKa/AF61W0T3D4OupIu4VsoPHsurU+6ra0e0irh0ffGC2AE+HOhZ6UW9pUXyAAKbG5tQEtZVHpSz3CMQdD3IeknoHt+hAVRT68FS9kSYB6y62KDzAruSdAbe+o2Nba'
        b'FnVB6YqvvgYtCBz1XnZAypzSxN0XxLBxVK6ncqJJda3eGrWBgiliFEhv09JWf/Oy2CMXPPKzwqJuuA8Ea0wfjw5I1TfXNASidrijwpx04w8EA/SWdNSphiU1ajyBqrCY'
        b'ou/oxkNP1QBpJvhbqZxmGMKaWvaB6vMtQYfZmEDFA0rY6pp9NWpUphgdZ0TF2sYG0u9GNyksokLUhRF32T3TxnnAHOSgWlPnw8B8Xi9kr/WygbTDHWoSRCWv6quPerxK'
        b'Y6CmttnnraupW8i0d2FiKMx3F1J0x4UhhV3ip+HkQHKfokqg9dlK0wU6+hlCB6CdfEcWeSj0kI9DHrC+0Mkv7j2XOX2K25qeZKz4c76DcHK+G1MGIzrAZU3aWBtR60u2'
        b'2vgEvAnbAce5YVnlYDs0HrCPUI8WDXkKRUchOwcxnE/aWJImhV1NDnVF2N1p04RwUpOgToF72T+EUpx6WdidxHXawhzT3gq7wunwxgN9d/dEWMhhO6T7rBQ0OdwDahT8'
        b'ezVB3QjP8sJZ9ehhZQtqYUE9GVDPfZQ7G77ujaX5r4bnfcNplO+jcBpgHHtHPpmBZXc6IK89nAl5JdgnANor0d7kKYCrBPsHT2XKTY4NvFoWluFLZ0cZld4Lclo+WVxQ'
        b'ivm15oQ7F95RTBkHlOOcxTE4hHkq53r4OiWcnGQapGliOJXeJmejc1jgDRVOS8J3mgAYN7knx+ykyLulk7mZj2m5EVyhzN0wHq5wLtQvIHw0WybaimQzeMD7Y9TmnhZE'
        b'NMtWkc0Z93/wWON/Xij9i+TWOLM/xRlfTSjaw2hVolZRFUcWHKSkk47uNEWm0OMmWjib6FmZz+JzeUn0CB6gdHvjd6ILnsGqEWILJs3cgWjBvCqYC8YDw1xoLpjMxAUD'
        b'b0UcuLAEu9SwLksIB64YvpHoDie/TZMCn1CocTmMf1kw4CIqzGl2dYVmJ7MXhwa1sYkDSyZ3HOdfGO4VHhAeBAshp94G0/hpzQnT94JOVxhVzVxQbpLmCveCpfkGTLuU'
        b'JC4HN2YR7j14r7lp8UFJWhKQiCnm9E3CHOyd5hrHLd4yl/P7wwPDyeFeCh8eAP8Hwf++4SH1fDgNawr3xSWWCUQmPM8N8+HUcCoSZ412WuQ2nMSwnNI0B/QoGSY8/Gqw'
        b'NMKebK7TE04HkgCfeHpysGySiVRIgq9KKORTB5UA9/XQ63V8p83/CTyRw0VQZoqWEs6m94AYoL0p4XxK5ZupgZQaaKYKKFVgpvIolWemcq12UqoXpXqZqQGUGmCmBlFq'
        b'kJnqTaneZqo/pfqbqT6U6mOm+lGqn5nqG4MbpnIolYOp+hTYJEqRwNe4dYg+EQlAX8ODw8nQ41QtdYMQ2KNJdLXjleZLT5wvUAbAvh59S5u96cmhQR7AMwPnGZQqks8A'
        b'CSGPSJyeF2sSPtck0+4gwXd02n/Jui0s+xfAHf/9+GkQ7LaBFXH8hMqCgsN0nSyLHhZ4SxJ49idTeBO0As6EnJmyFWoXXS6nSmgbjP6g3EK66AKs5eFP9ZcuuMVUPl3E'
        b'gLy5oltEnj6G0ywLKsJpzBEiYC1gl8MOE6fJYS4Bp4lhG23mQKyEnUDoAy5jqtem7YPlBb67Uf+Pu64nMG6WLZN5BkYRAdGlQ06rQ3djhyRYFEh1CICG01knVpKmpToI'
        b'tcDDqej1kZ5LGuWE7iWHMWIFLqQUQErJiKYxhfrkYdf6QTyWmhROx0WHgCKEJdoApYado4D4G5egSQ7IDdAkIHNcenifCl+QZjQGmaFvudMAXsZ/71y9XU4wfJIEtB6S'
        b'7C6+t4h2M2wWueKzyJUIdNQJBtIRhRowT2JAl0ygDyGg9wDCSwyU0BtMZ2GavKpPhpnlRuNZeudan0tgQ6Nyezap82OqC4CBaAvbYd8CkhT2i3pNDKyyyGkeS5eAPIT9'
        b's6NCs6lRDCCI2BJ2JhvsIjCEnfZlLhQrkOVbpsQFuSaX+jzzoMICIdI32VgG7oXEaHuA6c8IZYZ61tvNUCeOeE1ANsIqgbbkhpPxmfU929mAZnDCiqK2dozTbPCrxGpw'
        b'omCDvp0D38IzeOOMfRtrB5ChRXMTgrOdaP0S888aC7qHfAd0GYBMEQPQ3QJGZ0FPhq0lSHs2ySbjXGFJ7oRgrfo4copP87/YuUXU0xjwttbWe5eqqP+sfi7HTFMkUpF2'
        b'MW4EWHBkx/+p0BA5/0rI3ZBNeyNrwaTC1U1oHvXC0wGNy5JEJvioRYM2hMiSyU6PmG3Hp+l2jymqTecLs5l8gRR1J3DkG2BZQN2Hz+7Dy3683E/eBOrQpUtAPUCa+Mub'
        b'G2vVg3TbUhNcqD5Alstw46tB9/3qIbIvaVTUPCoUeO+oWFMLXPvCmgDaN0ftplOiqD1g3TQ0t9YCx1+Y/J8DssK5/wIy9f+9/DOHEDgnlyOTFcV5LgjSiQcQHls2HRng'
        b'8cDJBxTsT+rmz93t03/+Tzb/x9KyW0y3S+K0EbACxfpFeM13S+Kw3ng3bhKuS8EhE3soCNTParRc2cWRA39vovzO6zVXZEtNGyzLoIrhc8kCluz42dnHXlp353XU+drQ'
        b'X6+KZ5B4ElJX0x7web3RTK830N5Gcj8UkqFtCDxN8sYT6qtd3TEkmIuOa2lV2pt95XQEgsIlSQCKUABCqLvzmGXm0/4C+VO1FPn+H0+Qu4c='
    ))))
