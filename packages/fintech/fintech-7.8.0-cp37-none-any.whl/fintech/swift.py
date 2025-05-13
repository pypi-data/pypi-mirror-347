
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
        b'eJzVfAlYVFeW8H2vFpBdRERQKHGj2KUQFTdcUKDYFBfABYriASVFFb5XJUajoKiFCrKIAqLivuCGgCiKaO7N2km6092JMcROTLp7xmydtTNm6fjfe1+BoJi/Z+br+Was'
        b'j2dx17Ofc+85jz+Dfv8k+CcK/wgz8CMbpINckM5kM9nsNpDOcpIj0mzJUYYfly3lZKUgXy4Er2A5ebaslNnKcDYcW8owIFueAobkKW1+5OxSlscuWKIoMGab9ZzCmKMw'
        b'5XGK5OdMeUaDYoHOYOK0eYpCjTZfk8sF29ktydMJvWOzuRydgRMUOWaD1qQzGgSFyYiH8gKnsK7JCQKeJgTbaUdbQVfgH2/8Y0/Az8EPC7AwFtYisUgtMovcYmOxtQyx'
        b'2FnsLQ4WR4uTxdniYhlqcbUMs7hZhlvcLSMsHpaRFk+Ll2WUZXSON0XadpN3GSgFm3w2yJ/3LgUp4HmfUsCAzd6bfVIxeSiikkRtL/UY/DMU/wwjIEgpBVOA0jZRb4u/'
        b'bxsiAVK9Rg5AZnzLKDMwj8ONm5FFh3ajnfBoZFL8IlSGKpKUqCJ2aXKQHEyMlqJbWrhHyZg98dDnneBW/wIhNgHtQeUJqJwBdrEsbJkHb2mZftxz7d0/kZCAwUT4/5Ag'
        b'x9WKKlMmwaiyGFWGospSVJnN7LNQHfMUqlEiqjU+cvDV+FGYJ5n61zkZoI1qJQv0k4bgb5mB48ekiI1/ibMFDzQTcFtm4H35FLGxJ18Kyn1HYEnMdLi+uQicBXo73Lxk'
        b'/kjpd/5leNePJn7DdkwCs0uAnqzns7BhVQWT6YzHh90L+yQmS2x+c+E3Qpy3nw+bfJ/5xSM6IhL0AHMI7oBb0X54CpN9d8givxzY5Yd2hcQEoV3w7BK/uARUGRgcGxSX'
        b'wACD85CZ6FjaAPLa9OIcSshLSAtyJH0EZH6VgNueJKDNUwS0Fwn4kZMTwOTzULiaA93zHYA5GDcugpfRVgx1eYAalaOd8YtiYgNjl4IwdcpwWLsE7ob7QO4ovcwGNaF6'
        b'dMw8HE+Ziw6MVRXDEngV7wDPgrXoGjpldic0OIqq0T4V2pIA20nfIZCfhm6YCTRrUR3sUMGqjDAybj/QBuaYiVQlozp0GO3lV8kACAbB6IwfhbVjgT1wA8C2RZ7r8LNs'
        b'nMjCH6TDAJHv+8WaGX/NmA90czo/ZQUNbvl0eMRnmQ8y1+TEa97ICa7x08RoPs101ebl6LM+z4zT/DZHuThWo0xWay5wZ5jmYbkPsuM0K0DVwxptjMbI1Uh3nWw5HTo3'
        b'rVw5SrEs8tu5LyeeclpQ1fmCw8GRYEn88I9hpZI1EZPgkjbDPhlewqRSJpiD/DGLWTAcWqS2cDe6YCIKhTpCKD274C60C1Wicqyf0xh4OVClZHpYP6VSwhO+9Huw+PGj'
        b'+4wc3riBMyhyRBMWLBTpckyzeuyofcrI1pg4Mk5wIFz2dWAcGBfGlvFjeHnvEkpJj2ydRm/memwyMnizISOjxz4jQ6vnNAZzYUbGU/sqGZ5ICi8jD7LKWLK+E1n/QxdW'
        b'zrCMnD7NowhWlXD72oAYWGMT6J8IK5KwjMiAO9oiHTnftEDLWqVPOogoY2vRJ8ostQUSLMosFWUJFWV2s8Qqyjn9Rbl3wYGiLE80E1uYMG422ouFPQfWB4EgtHs0bZ2N'
        b'SlzRXqxQc+eFgBDYusjsRmDfCq/CHWgvRhTuc8cyFojadHd0K2UCkX/5C16fZabfroL1sL3q7N6zpZdjfLd3lsYeZB5GvJpDRMoh5368BNSV2/oe/ErJmEZS+Z3uGBAX'
        b'hMpi4xNlwH61H7zMokOTUL2VE4OxmBK6x17kZ47eqDFRhhK5Bv4OjBSzk7frY6aUMqdHls1l6Uw8GcQT66Nk+zGQ5YlX6sdFMj2gj4vvDuAicWIbiqYI0BIQI/KQeIik'
        b'QAZ4FUhhdQY6LhKrajRsFkwRoVLAZknGAnQqS2MeQVC+4AFvkA4GsByqmQrQWbgHHaFqj3YXw2ukTwLY3InwMkDn4I3x1FagBjU6IZimkPUMoXEANUejarpToT1qIx0s'
        b'YI2wzgvPWT7FTInbgepsBdQ+mWwFS+cgC0Bt8BK6RBfM4420T4b7tk2bAVA7PBhKIUQnUAPsEng6z6gZBdB5aMGGiayJDmJs21CbeRIBBO5LhDV4UXSCpTOHOWFUSB+G'
        b'Be6fBDvxqpmwlO4HS2FtmCCoyLziEagCoIsmI3WdqBweSaLTMNrwADpNAL2GjsNGShTfzDjaaYM7GxUIE6UTXo6ga0YUY8PQJjjY4f3Qlc2eTDg6KOvFoWa8PU/JD085'
        b'oVKArgJYIhrX/XEp9ujyZNKHyp1RFSPxgmW0S4MsJnu7MII42p8Om5kh6BK8ZvbAXV7wYpw96qB4o+1oB6pmGFgBL9N5idnopIDaipwIIEfR7iwmYAM6JPJ065wxwhBH'
        b'1ELWvAVP2jAR6IaXKAqWTfC4/Voz6gC47zK6uoEZj7pixWnHYUm0YM+byDSsUkMYb9gwhmK9ZPMmwYSu2pOeCnjJjwmYAOupKOTMhmcEJ0dMDokMnnBmZqL6zXTKBHgB'
        b'XcQ9TgyQDNkILzBRjvC4CMNW1LgJ96wlaF0LQ8eZYNiG2umsFZGwyt6xEJZLgWQsPIJOMlFjnelGyinTiHxg2SmE9TMBuoDqx1MqodIC2I4lOFwO2Bx0BHZh8caoVIpM'
        b'aU2aRySAiFzpPHQAN8AydILuJZ+8XsAkaHMmFLy4IogJH4IqqHj4on2wREAd1r5mdA41MiqMUJVSQb3ZtdWuTDgL/KrUrxfc9T4p0MZDPm7MVBZ4VE24XeDBfzSXNtpF'
        b'uDMzWDAVJL9fcFdyk6ON/pEeTBS2FYUZb2yqn905nTbaxnkx81mgKJG/uCl1dkg0bRwNRjMxLHAB/u9sqjeHz6SNb83xYeJZEPrV8z2b6h3UQbRxrWoMk8xir6uDm+qn'
        b'RNrRxp/TxjJLMJwtU+9sSh1qCKCNJmEck4rhzPT4zSYPqbMLbQwKmcCsxHDe9vjdJo8ppWm0cUGEH5OJ4azyf1FIXXk9kzbOTQ7ALgFEHRn+ppA6rsVIGz+NDWLyMPBf'
        b'Ce8J9cP/oqKN30wPZvQsyCxccldIlddKaWND8SSmEGOU6fCqkOpuw9LGOy4qBtvU5JaVUPDY8JIPbXQfEc6sx2jeV/1BuBv6/kTaWFsUwTzPgsK3+A+Fu/oIB9q4JWgq'
        b'U4Jxr5r1ipDq6bpSpBI3ndnGgpj70jeEu8nvr6aN76+YyZRhgri43RbuusXG0cbCObOYchbkZS55X7gb8nuRdOPT5zBVhJvc74VUv5LxtDF26DymlgWpb024I9z1uhpB'
        b'G+fEz2fqMelKHDFIKZ4iPes3L2QOsmA9iL8reAz5s5Y2hkljmSOYni3GD/PrY7pW0UZmTTxzBpPORfFCfurwLTG0cWp4EnMeky4q9HZ+KrtA3ChwbjLTgknnwryWX5+c'
        b'EUgbyzJTmHZMOgX/QX791AWzRVfQNEkj2NsR3XOADfAAE7VqJpV5T9g4zZ53csTqOhRdgB1YX7sXUU0ZBQ/DQ9iuXi0SJMRsRKF2JmBFtGgP8z2wqcG2m+h/bcBCxhdH'
        b'i1VKkaEfqF5hDkrAehfmTpHHploxBvw2+jXmCPbmmTF/NHrYMsW0sWrU68wJCYgqSXjd6BF3fx5thLPfYM5IMPpRd42pa4InDB5chwMgHt7IuQXkyP7JE8qAAJvsJn8q'
        b'KpmQaCbHFhxK74SdcHcSPkxVop2xCfAS7AhGO3GQ6J4pnSgV1XGTggXSwGT8LVO/aaWrGNoyubbAxeEfEnxkcfCUjANi1HUL3YCn1CFqtCcpVgbb0VZgi7axz+FlT1Kz'
        b'hb3O7lzYBo/DLthOQm4mDcDz4Umiz6tglgf44SC1bCGsCcFxikOuxBlZ8FRnEifMj4RtGIGpXpEgctpMnlCKQrIqWgps51fY4HOPflE6IzamzbEBDm519Ow1JcIW0NA9'
        b'GDbHqEiYh51pGGzSRKwzkxgSnfeG59VzeRr+VpJzpRpWhsTCC34MUJhkTt5wB43WFOiSREV4AmvB1FlZJhezAv8yMQOWBeCzE/auW1E1PpHi81SsFAxTSnBLKzxDRRO2'
        b'6GGTynqSCFZqYQfcRkVzUrStCraSo0cTQFtQtR6fRw7Q84dPOqxQqciMw8AH7s+F1a60fSkODK6pVHJyeAF2m9c4wEO0vXAMOqWKIOPrwXi/bLQNVVKz7pNfrI4jUCVS'
        b'pgCnubCsUDIVtU2m06SevqoIsn8DQLVwD4cavEVWbnVDVep4PCkEHxX2oYoABtinY5eBGr2ULIXdhFqRRRXBEraCeWhfDibdRdGpVqIj6KwqggDZiJeemQu3woMik3fB'
        b'Fhx07MYnkgQZkHozsHImPJaKDlNo0PWx6LQqAmsDPAhCp+Ul4HiBHGOwh6vLDyAsQTtRF2pOhBekwGGmxBleRHsphb1RwxAV7CD4HwGwLF0/EcsNUfGJoTzaHR9HzjUS'
        b'1M3A6kDYuAa2mJPIsofRtalCfGxsArl06DtR+gUr/ROClUGsHTzJ4SPyKXjCz4+EiPCse4AS1qITAW6w1n04OjECnmYB3OXmgr32ng36h48ePTpbLAO2fmMZcmz/xO85'
        b'QAkyAlXbByQGxUiBNIoZhcO+ZrzYVqWb6OTtGcGRNxMDdJgZifaMTYRVorbsWQxvoTYnsa+DgRdgnRJWzxCjq5oYHJBa52G8OuHNAHaFKFSwihfwLGq4mGBHH3zAu0Un'
        b'ucHuDGGt2Y4EqjcYHF7VKlKx+yd08oNXpmDvX4TaZSRcY55DrWNgRbIYvFTCfbAJx12o3ZEsepkRloQlKkRedwfb2zvZw0psXdMZtEe/Au3FQSxBjB0rE0x2RSQ0vMnA'
        b'E/Gj5NZQE55FJ21JF9lqC4NuLVCkw1Ni+Lpjsgm1mXjUToLUbiZlsVdWiig5dZhm+4XRmFOtJjlgsF5gObuJxZwueQtWoSv2to74TCGZwqB2dD1mSZHYdRiVJuPQdq0D'
        b'gf0AsxZVTVy/gkLoK19n7+SADyqS6Qxqgidi/dFNCoYZmycSCfE40pQ4MdNjpqDaUZQWoagJA+iMWok78WXgFdg5B25nRVqcXgLLhLV0I+xm0IGJ3qjdmy4YiCyoQ7AT'
        b'2VXDTB2tCMdhMsW4Mg2esac9ElcGblGFwmOjqDbAtmy4H+3FWhSBTgWCQGgZR2fkTlHC3c52a9cxIGKzFF3E8XGQUoz8SuB+mz6M4Cl4OhZeg+W602M+lwjnsFqNX/Vw'
        b'Vc3lxHtRLjty1737PTNCsaXwoasi6oMtbgtL/RYnKxaNkr1bUeWrjnnod7H+pjyan6P5Whohi25+e4bdcOcqy6ufr/e6+N6hH75vKs69c/HNz0/yp5MbX8twdtg2bb3D'
        b'T5NCa17b4vDeh632wthVQt6R7Z9MG18t2xS51dN4+ONpi+9kTat02h81etzG093HV2s9VtR6VZ+/F5imfa89Rr2q4hXP3NzyP4xJTOzivj7GzVzrGrJwH7cwYLsy471d'
        b'G4ulV4u3Pe/yTdJra8blRy/WDnG9MOLjGX+qfXC89UvXTXbxvp8k5bg8cr987n2/8oM/J19688Hf095raL3wqjza//P0V7/fOu/ip89xdz+wjPB4eVfIb3ze+Wv+K/Az'
        b'u41O5asy9xW49miuyl6odLzBtIze1nll+aJb5qFfTFCEFFTe3no96I2wHRkfef2toqT7h20Nt26fVn0afjq087uRuQlxPwWtTvuya2hxSuM3E1esGj0xrOnfXhj77t/u'
        b'/vBdzqtb/mNswhXL+c+ORlz9x9prQv08Wfqj5JdWPvI/e0TyyZURk1NPcJf+nLDAEpS4cXjwA+fSzQ7SES2mf/ikVZ35btGHSluTF/HXqHYG2h2YiA2TdDqqxOdfe3gO'
        b'22EXVGIiZ2R4Bpv6UwHBsYH+ymB0PBoPQTvJpZl0NdpWSE//clS3FnuNx7c7cbAGu/4dASZiZYIUngHBWKl24qVhM9oth3vYoEWwlk5FTbJp6kC/GFShJuZnL7DFmz8H'
        b'G/xN1Od4SNWxCf4JNkCP50lZWy7R5ENCfRxWVZJjOzoXgdfFNrscVUrAsOkS1LgBHjcRZ8zMh51qeDU6KQgryzpmTsJ8pe2T1xDPeihlz+5/fHXhKl5dmHiNQdCIF+j0'
        b'BqOQxEVznRhbRs64MQ6sLePAOLH4m8QOt7kyTgy5rrJl7OiPG/644P97P/g76yR+Z+1s5AyZbce4s66sLSuVSfFsF8Ydt8nxxxOvS747MbwDeHzt5dAfpH53Jc/GSsnw'
        b'jr140aXmgd5bk1tu/W9NAgnPask1QkAMLEVX6c1JiBK7v4DE+GCREQFysBCet4G1eXC3kqEWxTEvWx0biMMWKcD+royBjTHo3ICg1LE3hpwvBqXkMh08fZ2e49gXpLLP'
        b'DFIlOEjNVUr/XoAXtVP0+5dMGCYoNAPTGzRn8lwhp0hYMi08VGHk6Zew4AFTB/wSa1LwnMnMG8haep1gIktkaQz5Co1WazQbTArBpDFxBZzBJCiK8nTaPIWG5/CcQp4T'
        b'cCOXPWA5jaAwC2aNXpGtozzT8DpOCFbM0QtGhUavV6REJ89R5Og4fbZA1+HWYwZr8SpkjH7AUvTCUxylNRrWcTweRbI6ZoNOa8zmMFy8zpAr/Apucx5D8ZwiD4NG0kk5'
        b'Rr3eWIRnkgXMWow6F/nsJYIwDbM5PoPncjieM2i5SOu+Cr855hwMe64gWPs2KJ+Y+fQczI/MzESjgcvMVPjN5TaYc585mbCAoPl4v7m4Rc/pTBs0efonR1t59Xiw2mgw'
        b'GQ3mggKOf3Isbs3i+P54CASQwQdnafQajEGGsZAzRFJy4gmGHA0mvKDRZxsHjrcCUyDCMp/T6gqwKGBMCaEGG6o184RCzz2GZjk6kcebDYOOJjflkfSJ1zRr8/AwAf9m'
        b'LngW1Fq9UeB6wY42ZP8fADnLaMznsq0wD5CXZVgfTJyB4qDI5bLwaqb/3bgYjKZ/ApV1Rj4X2xc+/38pNoK5IEPLc9k6kzAYLilEbxQLzSZBm8frcjBaihDR6iqMBv1z'
        b'/6M4WY2AzkC1lBgKhRU1zjAYWjQD8StYzeX0GsFEp//fQKp/tBDZ5876+6I+e1doFExPLmCVDE7Q8rpCMuVZlpvwmtNlPQNi4rlMml7hWo49F95Kr3+GhFk3fSyOA/d6'
        b'tmj+p+nOc9iLYqWLVGArg0cuRl3a/Cxxg8HGE1uEkc/I5/qxqhcgTAI96hIETv9rU03YwT+DiNZ1yIjBgX3K46rNhmzOMLjHtG6LfeQgvnrgxnjMr62Ru26g311IuI1O'
        b'5JgEbKlycBBDugebWMhjBmCbpxl832RrN2cISuSDnwX9gL2fgntw/28VhCdigAGTnxkPiHN1eOvBJ8bOnZP4bLHLMPK6XJ2BiNTTNiTJ2pdFBRIrsGIBzxVkFz1T1/uv'
        b'/E8ItDj8P2lM8jTY2wxq8hZyWagLq/UgNuF/ADCiBlTPiJ0bANcS3PPrymbQFHCPrZ01Llb4JeLmQeXUzBfSuOipGcs4vogzZBO13FDEafMHmy1whZrI/oE1XqBfVD/I'
        b'jBUGw6pIxVJDvsFYZHgcdWf3PwdosrNxQ5HOlEeCdB1PolSO12kVuuxfi/Aj8blVU0DMJoZpSd4TxV4DJ0ZazzmR+FwwmGcYOLovK0BOcu5PZQVixLKbRLmEFjJkZuY6'
        b'LHePFC/U/QJkJJegqFqg11eE+YgX6oXoDAfb4M25+GA7HUxHrW7i5XuhDcCHVJdkJ138DcdUQK/aZo5GzX034PC0Ft5E+2kSYig85hHw1Al1jDe84iPzhAfhAaUDvaaX'
        b'wC1j0e6QuNgguCskLkEdFIcq1ImwziQDk1CFPAAdmE2LBtBxZEGXAvpGyIDranQEHpbAFi08Jl5uH0RH09VFaNeAi/FCyVQHeJbeNdrawnMuqeL19+Orb3jDhV6pO/ji'
        b'HXYHoAq8zsWEuCAW2KJOFu5aOsXsS6/Oo9LJlXssKsfwVaDKkBhUIQE+c1G1qxTVA3SNJg5GLoVt/YaRHMzOkMSiKBkYFyCbIZlknkjWuoHP4yV9w+YZyUCap0hMYIAS'
        b'dsngARvYbB5PxjagRtQ6YGeSi0iAl5cwYFymLAqdhKdFCEvRkbUBwRgzeBkvGByXgHYGKuXACzVK4XF0Ae01e9G72AUOZBSpn0lAu8iIEcOl8eGhmgQzueZx2ojODcK5'
        b'ySxh3DYxXQGPw85sVRjJMNSB0BHZM9FRyoLJsGbsAB4NgTcpj+BWtTjRsmqNKkwmZhDa1+aNh/W0PRfWwEa0dx7qtAEgFISig+FidcPprFFqZ1j7JEtn2IssP2aEuzGM'
        b'u55kKqpZoBSrKlRwBzqkgq2F5HL5CqqJB/DiUlROL0g0sAluxX30OhmsmJQPd6Ema84LWpxEaeiw7ScMqAR1K+XiDW8LXu6YSlUoAUy2Vg3gBXhxilhtsnUCvKlSoRYZ'
        b'YNwnL8aIwhNKepXsgq6hCpWKx1Ng44IkAC+hJlRJJxkjUTWe04rnLB61DMAOWAovUH1cNS5GpSLJk2MAo3ot32YlJVlGVI5KRSh5HKAuaNGj5lyqp0juDgLxVsDdNAMa'
        b'NgCa5YI74Ql/AV73xOtEg+hZYmL4dtRQUlo6FcQXO5wzpgOlhBLdY+RGkjOpwIJXI9LUFtWzcN/s4VSNRqG9i9RK1Bgc5E/YDC9KgfMyid7TV0S+zA/tVdPKLOnChVIG'
        b'NqF2P6V4k+6F0e8UKYa6xhKSoX2oXix9aF0FD1hphtlXRaiG6jGfiGSPWu8+mOohSwFRPUzCZrwBzTQdcUElIn2XDSXkzVxG24fGLLPSdkQaoS1q8qclqqjMF6/5lLrC'
        b'wwtEfUXtqJvaOX90MKyPCfvhgXwt2mX2I4QtgTvRub4lFuUNosqwCu63liHBU359TNuB9utR9yxqBp3lqPFpHZ8Lz4o6Do/AKxSRWNi0RqUSM4up6HDeTNRBORkZ6UyL'
        b'Kgs3Fjl8M6MQKN2oFUZlsH20OjZoA+xMDMa67td7aesFLVJ40l5PVSR9GjpLsmTjbJVBsVIwxIaFe2B7OAXZYQzcYuXmUifCTXgatVKLDK+jOrRfFJSm4P5yAnfDo2IN'
        b'1ZZAvPKiWXFB6iD/RFLW65wr4dB1W2rZxqM6WKYmxDJj696bosWEI2lAr3gprJHBdpFNXfCsu3rQTC5sjjPJnGBJJs0oDoU1DgPsDyrHkk8MEDpVSEUpeJhSTJzCPSFx'
        b'sBydfDzYXyuD5+Q6EfJ2dBLVqUPUsDlDtDo05a1xpiYyBJ4LELPDjzPDsBGW0uzwJR21IPAI6tSo0cG0J03XZNhN7bA9LMFQXHF+yh9ViDXRBnQY605fkvO6E8kHNsIt'
        b'8JxZSS3jTGSh1CdzsRBWhqBd8SQZgBth/TIGhME6eaxuqJhmu4TlNRRWqtGemMC4pCA5sFez6LBbJAXFhC762GCDL6Zi+9Kw6DSeRDOFB8NgQ192V4pavBl4bF6m2Lcf'
        b'WvxG5oop/t78/gyG0gl1wIqh/QoR+ooQNqOqiak54vwWWA5vWUUMbp9OZezaXGovJEuURC4T4JXHgilfTA2ap1eBPbRMxCFKCkhBB6Do21At6tgYgJpR2RMid8oZWwia'
        b'sz9mD8sFdA5uEy0hdq97qZXlAsbYkwJUdBYM8YD7l1rrA+EeKRaevbAC7sITgkDQKHSQsicxv5hS3xWW9pf9UNhNFfJY/hBsgkHokcXm+Ok6Foi+fIcDPE3leFT6oAIP'
        b'q1CHmHNs8sPM34vqbEgqEcCz0owUdITqtFa+9LEErxv2hPx64mCIGApfjRtsC5WQTBKpz2gyztxkXobbE+A51C1gsUIVsYuSYWtoymJURovFg4P8MAP9rVnzFGIqygKX'
        b'xRDeUcFYFBNIerABUS9NRhVxsFsK4K2NQ2FFMUtz5BccpTSYPDKnQH8+rAjQeAgeL5QOJgFeaM9EkjG3egYccmDs28KJl0aHPBdh1+AHr1EObID1Y0gPAxjPBOwWLsJT'
        b'68y0YONCAGzDrCmLRdVoP6qFZevwAzMKXoiAF2WwNWuxKQtemcyocYxQjcrlaStCKG1S0Qlb64pjcsiK9kbs+agwXtqETqyep+5VSHkG629C56kKaaPhdnUE94TXQ93T'
        b'qeXBQlyCrlCJgPu8BljDuiwxXtiPdiqsKMKOWQTFKfZUTZyXrCMB2SocFj8VtsHuJLp+JLw5SNSmWRiKY8l6pZTipUFbxqsi1pLgomJyHMZrtBgpjJkPa1XhchqsuaPD'
        b'HNwdLhK9FZuYLarwdZgQWWuisJRh2m2nhMiGDbAaA4taAF6tciR2mq0cqrMmltAVFWrGvZNwp//cBSQXb9GYSfYqHm6xsccOYTdm+KllWK5QZQpqcYSXwyclx/RK3eKg'
        b'ZYsHCpMUYHFuskMHNloLGuEpuC0Gi+pOtA/D/Tx4Hm611p/aGFfCcxHwMgvYxWibO8CAtGCVJCrsiJpC8ZyGddjBbgabp6NGcxC15eG+Aq2SX+xHspdE7ZYP2Hx5+KQg'
        b'G7gP7YCXzNNFM7IDnbdPTEAVQctE9ZgyFCvE8pi4pTFLRHzg2WRUlhAUnBifJAPYKbbYwe1+8Ko1EIEWDQ65924MEd8ngM1wl7W+A51OxzJ7QUaiAaBA1fDc6IV4EnUZ'
        b'+zAHLqqjUMsTQjYT3aQ2Jy4SlYoidtilv4jF6MQYqsEHm+y2ItRB6jlgcza6yoSvg7tp/hAeQpfx0eRZDqMJ3rB6jARriQ2s3ZwpoI5CZzkpU8lHO5kJ6BRso7owE3Z5'
        b'TEU3nvAmAFaLBWgHh2HfGRu03GOwoGMxOkTLvHSzPzkuEQT89ZF6unlJQqXbUrebXx5vvt68Med6o2bHglE28+XJUSa3F5fNf9lxjD61ZMi4F++9eqxmzyrthHnfrJ6r'
        b'T7CbF/+oJG3JyLrgla2ZH2V9HFLI/TzkF1B3uOhcbr00/uSnh4o+uOHzZbdwLnz4O9+9OGNcUvzqj94539Ww4P1KdducPz74Zf9V7i/6sxOuX1u5Jnfib1bkBiwdtgBt'
        b'aOhau+7bO+uHn89JOXdW+Qsbob9758fDX1dXbvo4aw+/6ud/W/J1SkPkS1+XTIirPv6byKU2taE3f54xLnFdpPfqhRM/Oi7zuRG8ZVPkuMJVhSOvFXd+UTMj+Je1Q3yv'
        b'5puTtEm5MQ9/66h729XryFnvfzg2/jDjcHPW6rsyzSPw/vAO/8uNG+NnP5jzapxj2U+dh/Puz7tnr28A+bPcvpr/9cd7qod5u/906cXPXI+tZq4G3ttfuPD2IXbKq5Ov'
        b'+WyfbnfR+W+TC089TLmmrfl95N13t6/6y4RjH+9Le3H5kk8z34TI+Hngj4U1+5ilixwrX6puGDF9+ntxwgFuvSlo9WjX/3h+14GOh1PveOW8dPpVZbRj4l887zWe0Xm+'
        b'POer9aVfLCkWUkxV2zcF23v/kO298V7Z699nGQ2d+uLld96+M3bEh+/Nsj/VduvLupyXjR/9ZU7I6Mufxv/9Wte8j9blfubZ84fNv5147cK0dw9vu5fo+Nfu9Qm/fffj'
        b'P4Zl5B9bOqlpS7DD+rxXfqedEfBjievRF5a9df9B0ds/F5z9IeH0ok2S9tWut/78hmvzd4fWfP/ttK5/fyl46A3XdSMK/3jq4RX98iG37Ff/tP0P17c3b1853H9U1YXh'
        b'3zjmXVjW0ulheunLN7/7tnv+L2nhLd2XepxLErV/n/f1I73J4WHN/T8tGtG5at1lVcZnaZsvv/sgevKVxoSFm7ftaY9+8F7tpbfj7tbONqR+Pq5c/VXYveljvpqocRj9'
        b'ZpPvniBD13Xtf/wycszq1Og3bGxm3jwz3HQm+vVFi2KWPUi+v+J22u3zwvTGq6jr069Gll//hPvwTx8EqZZxn19/q/vQ/Q9Nj85+OTPy0+sXLY0vTzmTHXXg+Q8nFr3F'
        b'7Y/7rvvQ66qH48YnvfdcddqrX6g9P7lh87bvzNkpdlkr//T7a9WziidMu/Rn7/TnEyKv/K6ptO0l4aOLx1O+eDjN9/BtvWRyWYTPVyMY51J2im/2Xz8fHxY+7u3Y3deP'
        b'fay84/mPu8mvff3pC9crlh/9Lrkp99G3p0+8X7v5kQ8v0//27GdKJxPxzrPQebTdWieCtZRYRKzMI2CHNNIvZjK6TGtVYB205AT4B8PtqFKJ9RmAIWksPIm64UUTNVu3'
        b'Vk/qrVTpK1OBR6JW58FrJmL0xguovjC3rxyFlqKMGU0rUdLHw71qbCHOoE5ajSJWoqADBvqeE2rCVuvQ8mXWSpl+dTJw3yxaJ+MMK+JoSUq/epQg2E1KUtDBELHY5SC8'
        b'hkOYxAR4lAmMQ3sA3qOTLZrtQ+tkoAXbfYvjFDU2hiHYW8iL2GAMzU7aOSVto3pmEYarDzPnUEmumz/tDCuGzah72YBYAR8b6ijKK2ahG+nGgGCRXnJ4nlXBrhBKzpDF'
        b'qAbHCqX93tyh7+2EwhOUnD7FAagNMwLHXIW973bNkGrhLskyf+Wwf7aY5r/4UDr+99d56jWjAtO08FBapBNIik+KQaotI7V+nGhBDvlIGZZxYFxZ8s2BsWNZZrCPWNhD'
        b'xnuwpESHjPQgBT2sHdP/I67gJM56xlrix5Z1YhSMnCUvP7kwHhIXxonuIWW88Xw3UvrDKqzFQuT1KLwb68A6UAhouRDdCf+wBG5SseOLf5fTAiIKB54lZ+1o+ZEdMwrP'
        b'd8f9nnhFKcb2MeQurFioRL6Rd6YIBjypkU7srTCSksvjfpVF/31eKRnepZdbdK8awiXSBErAV+P61yARfYxNxZZhgfXNLVQZRMI6fBQrlOCj7qQBr8wRPkeRtejRirxn'
        b'DdLZbCZdks2Kb9j1uND7b1obxEfzvJH/0Ue8Eacyw1tLfbhshcag4Eh/cKJS2mObkUFSCBkZPXYZGeIL1fi7Q0bGWrNGb+2xycjINmozMkRBfPygSJKzYyWGjhaN2bL0'
        b'TmA52oaO2Duhqyb7ITGBI/P8E4N4q+aFoCa5LHuyklmg25qTzgheeKrfhikzKzsTUbJL9Ifftg2bbv/en7dN/vyn7nlVDx4Cu7l1H786d1ctey/5rUz1lyN3zn71lSyb'
        b'bacaNv573t/eqPtpVvjwvZXj+BMfyNMq3xl+dlnKn355525Dbs/U39favzS7Lt/um+7bN3/XVet19l2N39e+PyibXrw2NnrZy85BdtVv3MudFOzwS8S45774ZNdF2S7f'
        b'k3cT3IoiT9+8nbXjs2/iPh8fsXTN27q3TkR7NTmtymnQHpa5px17JSzgfOvLkV761pcipn/e+sosm1F8+Cfja7SJU/9a/u3OQ6npawLeDPpszf3CF7gDn9VfV9bvV556'
        b'bfmHi3ebVr99srYh9suUnjt7DA9OfV8a9u69Fw3fv24J/bvNC0H/SH3LeekJ3wbbF49/tXozyP562dKqZKXURI5sm/BpCJ8B4ovQSXy0mArQnuJkatDhYXgOdtirZyqe'
        b'enV1/GwTveo5gD1Lu70/NqnEoCeYV8Jj1mE+sE2KLsHuSFqNmI5D6SMCvBCTGEQDzDG5xPgPRVXksqd7IpZsKuCu/0JbKadx7LMf1AZiidUbNdkZGdQAklJ+4E4MUjg2'
        b'OqSekFQYuti62AwwXzKraZK4JeGRxWCTA8OP6BVkrDwslu7HdmDovwY9hvfoUxuyOfFrYnXi58H9LQPhRtE8eAvuJpcZmBet8FJSPNwJK22A00jJaOxAda4f3GMFDg+c'
        b'1PS70S9Pctoa5bLj98U5RY6mrO07HhztgtvWfOF3WfXD3RX3EyZ1f7p9e/MH6Vfe/zgjv/uHw7C4KCX1xIGMk58Uv5Oith2b8uDBNFXhCyM7+bGT1v77JOfq489fz2mc'
        b'+c7vbC7Peum3Hh0fPFLa0ODAXYYa4C6WvmGaRA86NtjXtrLYv2+B+6mzXbkRXlYnBaHLZEhSEAuG6heiLgk8iuo8qcSGKF1FvNTwEPba5QmwguLlKvFerDKRo+pqdBIe'
        b'VLtHiiWzpF4W1S4Xpf0mlvdTtvCIut8fNrBXsqiqGB4XA5xzqF2KgWx/6k8f2KFdtBiXh51pAXFoC2qSAUYNUP0GTa9oe/+LY4H/qtxIf1UZdAadyaoMxFQAR1tG9I22'
        b'ksBiQD6AH9kn6ooeiZ4z9EhJpWiPzGQu1HM9UpISxc5Qp8VPUu3XIxFMfI8s6zkTJ/RIScFIj0RnMPXI6PvNPTJeY8jFs3WGQrOpR6LN43skRj67R56j05s4/EuBprBH'
        b'skFX2CPTCFqdrkeSx63HQ/DydjpBZxBMpESsR15oztLrtD02Gq2WKzQJPQ50wzAxJd3jKMY6OsE4NSJ0Uo+9kKfLMWVQz9XjaDZo8zQ67M0yuPXaniEZGQL2boXYV8nN'
        b'BrPAZT9WZhFtb54YCn4SeZDDO0/cFE/O1jxJtvIkicgTEefJVTBPDCdPrjr4CeRBEgo8+WMQPLk04Img8f7kQd4054m68iR1wZP3kHjy5hRPLid5cqfGK8iDaAZPYlV+'
        b'MnlMIY+APltAuDOkzxb8sKCfLaB9P9r2/vWAHpeMDOt3qxH80TNn4B9HURiMJgXp47ITlbY8sTHEgWv0emziqBwQLeixw0zgTQLJuvfI9UatRo/pv9hsMOkKOBo98NN6'
        b'ifeEx++xnSHGCbPIbzQekbJYSUVZc3EjZpb5f8PZKtg='
    ))))
