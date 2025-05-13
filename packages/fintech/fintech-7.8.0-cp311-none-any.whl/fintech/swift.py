
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
        b'eJzVfAlAU1fa6L1Z2Pd9CRBkDSFsYRdxA9lBBXEXIoRFYoAsLrhvJewoLgGpxj0qakSruNtzOq1tbZvQtKZMO2Wm7bQz07+lU9vadmb6zrkXFBT75n9vZt774/Vw7jnf'
        b'd5bvfNu557v3E2Lcjzn699sXUHKAKCeWEJXEErKc3EksYYiZGhYxya+ccZIkiLPk2L3MppzJIMTskyh/9jHUGkJus5SBys3KWRPht5Oo1Fz8VCskUc4uJCyreGY/ia0K'
        b'F2bNKeKuri1XSsTc2gquokrMnbteUVUr5c6plirEZVXcOlFZjahSHGFlVVRVLR+DLRdXVEvFcm6FUlqmqK6VyrmKWgQqk4u5o22K5XKEJo+wKvMZNydf9N8aE+ILlDQS'
        b'jWQjo5HZyGpkN5o1mjdaNFo2WjVaN9o02jbaNdo3OjQ6Njo1Oje6NLo2ujW6N3o0ejZ6NXo3chp9DhAqjspd5aSyUJmrPFS2KpbKXmWlclbZqCxVripCxVQ5qFxUbJWd'
        b'ylPlprJWeanMVAwVqfJW+agcK3wR6S02+TKIJs5Ecm7ysyQYxEbfiaWoxG9iCUls9t3sV0gEPLduLbGOuZhYSyJSM/LLxi+sI/rvjIlgNsoNhQTPPF9ige5cSSaBmWFu'
        b'0TqbwCwfQhmIbuAue7ANtsCmgtx5UAXbCniwLWvBXIEZsaYoJJ0F7/iAfh6p9Eagdc7l8qw82A5b82ArSVhBLejNYgAdaJ1aRo4bgtPYENQo2efYiIaBKEYgKrIRncwR'
        b'VS0RNa0RNW0RBe0RLR0RrZ0rnCi6IcZqeooNNzEoupHP0I3xDG3IzYxRuk1a95hulf8M3fJouv0jyZywIQiHKLPUvOYgG4Iu9GRQxIyqeM8zpn4OXbjW3pJwQGVR8UuV'
        b'10NC6MJpziwC/eVGmU1nL56RRJwmJFaoOD3eg1W1+C9BBPH7kL8yrkT/pb6CkFiiistCdb0zs9SemFEa82HMqdQVdLG/91+XZviE+jHmDpP/8AjzPEUMEcpIvIJq0Axf'
        b'QkvYEjkvNBQ2R5a6ZApgMzhdFJqdBzvCI7IE2XkkIbW3nAZawe0JS8Uam3UDXiomtVR4mYgK5uPFYP7nF8N8ksWwphdjP8+e8HCahohcahO1cSahFKBCzwB4GxGglZ8D'
        b'W2FT7rzMrPCsBQTo2BSTU+gK9haBFrCPqGSbw8OwP1rpionW4ZkjBFfR/OHVQnCaqAdXYRNVA86ugFeF4DKq8leAF4kaeApcU+LRwJPg6kJhDMpVwiawnyjzclE60Qug'
        b'joJdbIKICHclIhbAw9RIy3ysiBQxHzFOqUTrJKOZ4aUCZ+KRRSbKlW70WxFKVJ/742qmfB263yrxPvhGyovbmo50Xexa7xnAhKu4L2x1eVVS4bA8sIjhzmyOUcYsvBgd'
        b'pTmzmvHnfNHbFeTZymwRrzRXdE6sFRFnsoLZzYroUzrBjBgmufW6x3zT0u7A3emmQg9DmkdhYmf6oGHZ0G9sFNOdr/+8wzPxXZK/3evNVZ/wGA/9UPfW8BjcbY3ox8tT'
        b'CsIQFzEIVzgAb4JGlkUS7HjIwRNtksE9iM7NsAO2MsEJsJtgJZHgInwRHOexhhihPJktAnuSyDF/cbdu3fqTW0qFrLZBLOVW0Ko/Qr62ukKROmRF6fWScpFC3DAuz8DI'
        b'jSh5tJUYSSMJB2eVvDOuqaG1QT2veYtqy0duXL1/8sACg/8sg9tso9tsvcNsk5u3unyPRO/G1yj0bkKtQpVhcvFWi3cXqNJNLu4HMvdkqsWaWZp5mlm91VpXbb3OUSvv'
        b'89ItGIgemDcgvLxE7zPD4DLT6DITwTtzO6dpXA3OIUbnEL1NyLeYK2WYLXlmQ+w1IolSPGReUiJTSktKhqxLSsokYpFUWYdKniIAZuBSLiaBzA4X2qNk/EQDMFAdniie'
        b'6WySJJ1HiF9Lhu3cVdVNNa01W61HGGzSxWTtpEpoSmpNGmbZb83Zlrczb2ueycLeZOGssn40wibYDhNLtxbQ/+SYG/dZ8omzdknMOWWMyZTCRgzCwJaUUgvkY7XAmERH'
        b'My0nEXRUwnxG9BmbmaNqYdK656uFxwMbpxbM8pVYdcMWPyvYhVSbgFgjENjBTqULluXd1WAf7EIeUiQB9ygj4TZ4nhbl/RnwMi2yBGhaHBEMOqrnLueS8hmosv/jNCyJ'
        b'R7qqSWZ8J1CDy61N20RxQuice7zldNdFVdyua12nre6XrfyC9ecVr1oUQYtC5/t3P2AQQ4uss95ZxiMpaQH7wIl4cDiFny2AqqzcfDZhDS4ykKycBq085tOMgr24MS4Z'
        b'sqYZpEJSK1I0jL+h5CJxVC6KSMLV60DenjxNgEZucOEbXfiIc+1dEJ/YBpo8EOt3W3eyTc5enQnquN2pe1P1Nv4yhyeMLMOEG2KXi1dWK2RYkcmcJ2Feintp5nXHzDt+'
        b'OHwMVU9xLx5QIWJfL8ylz0/+pey73zKc6LNLZlKa9fQqJzKWQYQOx0vqXgqaaU8xQPS66XJFfBS4gvU5YyVS4RwOBf1dgCuZyCA8huNb13pvChAp8dzgsaVSDA57wHaS'
        b'YIgJeBq0w9MUwpkVbmQKg0hECDmKmK9qKFthA7clUAiqdUyCUUnAsy7wAgW+sdqTnIFWazj1Swd/bqy10gO3fwueB8fkioQoqBGh8UgJeAb2QS2FsTXJi0xjEFyEkbC7'
        b'YQuTZuCWyOUYfpErg2DUovbhrlkU9H0Rh8xkEA7DqfcTNjjMKqHGnwNu18vh5bioJHgKjR/sIOAlHrhEIbyZ6UvmMoio4dQ+5t2Qr5zoCbcHwmYKQ06wEcJOAl4GHUsp'
        b'hB/5/uRcBmGBelhf4FQdonTDCKeQod0nl8VFwTN+JDWkvrDVFLxg4RSyCNM/VWJzau39SgoenDTLgpeU0VGwswZNGFlheMnLiYKHloHkIrwCqX3BQeIVNRS8KBo0UfCl'
        b'9WjCyMai8ZxIpuCX8oPJZXgBUiU+5cpiHj2eHniUIZcLoxbUo+a3EPA8vAL3UPAzg3hkKV6BpPCq5i1/dlR6YvjDcOc8qgPQZY+WDPQQyMidANsplP+aGkaWM4gZCEX6'
        b'G8HUtRRKMbiAVolCOQK3miOcgwS8Bg/PpVBsFwrIKrxqSX21efwOOUXWINRNB7wkt7GC5zPQPOBLZGwkVFMIui0RpIRBlA4n2XhF8pODKD5KdYEt1jLEp9udMJVOIqfE'
        b'PIgC/7o6mqzD65wkyWUSr/tS4MxF4Iw1vIgWQW2J4JEzzoxbQoHXJghJpCTmIvAZX69IjKU9mvbEBGurmCiZJ1oxuJ+0hC+BO9RABQlAaw2voOW5k44b2kWSSEUeoj2k'
        b'Y2ZwlxxeWmvnvwHP4QjJj7GlKAKakDxp5Za2ULcGbsVt3iHjkWu5jWpzPmwF16zrlWghWuExZALgRTLIVkLzW4c7OCu3linQOrVgRDXp6wgOU/0tEm6WK+BVa9i/Ete0'
        b'kXwFUtm038VzldvZWoFD6QyCySanBeRSwhEB+2xQud1ScIEkmJbkDLgtkeaKdmU9qqgHLRV4VgNkBHIA1XTV0WBwwNq2Dg331AIWwQwgZ1jAbTSv9s8COzFrL5iJZKGO'
        b'gOfgMXCRpuANTxsk57GO68wIRgVSC3A7OE/VSKLDMfuBvSw2LXD9y+ARmtU6wF54QQ4vwkv2XnmYgufJWETdIxQlpHDHNDki0SV7S3AAV54hhWBnMM+eWsaBhbHkOiys'
        b'SfeLNem5DlSho38CuZFB1KHCQFMufz1VqBUnkVuxlCZJnIusT9I+su+yZHIng8gcTmote9erjkEVWoenkCosn0n314qYuXyq8N2QVLKVQVQNJ3255VFsbhFVqLKeSXZi'
        b'yUxqrfyi7D6bKkwsm03uZRCLkGywfl5gXUkVvrU+jVRjmUwKt+OmvEwrgvciMsheBrEOoftMr/+phip0WZdFarA0xt1nvu/zyUaq8GOHXFKLhSfufkU29zu6zde9C8g+'
        b'LCBxrRk5/FfW0YXpc0kdFoO4cPvi5eG1VOF8i0LyMmb2uL6oatJHQBEW3AKXoUpubWW3BnEXwbRBbHEWtFKMFOIIdlrL7GwT3REfOZLTwI5MipEWF7vCS/DqWnnVcibF'
        b'zXx+KKWwwQ5rHyQCSEOCy0CL2XIvOSUSnOWxqAHsCH6N7GWimU5tZX+7SselClemvE5qkDUfTrhvdajy6+VU4RuZb5DHmUizJEiSvw/fsIYqdFh3n9Qy0fQTJEsueX9n'
        b'P2Fnxh7zdTajZB97dBPNojbQRAX7P7hVfuYRgxnxrBsWnK/kYqa/Q4LzoKUgE2phO9KBTVl5EbAJ7SXcSlkh8ICCmjdvBXNzJwPnSm0qSkZ3yZ9EWxIzCS52OMJbUhMJ'
        b'WlqvbLLMiUwpzYHtBVlswgLuZKyX2FHrHGKP9h+X0LIgw54G95GLCdC3DJyjRW9bZTg/FO1iVJHI67IBt6GqkmnvAHZQ27UieBwxySXkTCYT8XXJ0eCGDA+AGkVICXsR'
        b'j4l8pBmlkh+kiXThri1mHCET8QO3NHc4fQZB8YwUHgDnhVGiUswmewgR3A8OKv3RjV+5TQ61Q+rAT0pyQEdkFjgXShJrpnIVbDtw2orSG2beoEkYC3oBfmgH9hIr4U14'
        b'QIndRie3BD7axVMPWdCWPotFcEGzM48JW5PEVM8ScLtQGJMBL2JMtAuFe+EtWrseQZvYbULQPx3uQrMDhwkJKuqj+vMHR5VCITgMtRjrEFEJDkA1RQ5wrqFcKFRgZw8c'
        b'IVYJ4DmqFwe4FV4Rxq/FGxagJsrBFXhB6YVuCu3B4ZxsPLZ82L4e7MQLY1fHTJw6nZIxMdJ6KmH8qjw8gm5CjGw+tSYpsMc/JxehRMI2PklYZ61fgjSiOdzBY9DatxNc'
        b'A8eE8RZgB1ITyC5XILvbRzW5OhpqhPFB8AU8xINo861eTc2pxHsGbEE71jw2oZSxfElwdD18id4NXFxhJ4z3iUcCBXqJKn+GEj8nBF2wmeTj1YBN+eAcC3FGB+iYxrQH'
        b'x0E7NWknuHuREFxZhpAQuIaQyIGGUgQKqwzYkotmzSQiwWEmvE2Cg/AQ0uX5uLcdy8FReW5WVp4Q9uKHaI+fQ4RG8MLyIngChhU4IQYn4UlwPDQUnHbj8xCVjvNdwF43'
        b'V3jcHZxiEKDZxQFoloEOyaNffvnFawVL0sWg+DD3U9tVtDSshufr+fmCTBZigVOsGSQ4g3jwGM+FNtf7aqBObitTMpHWCmPAQ2SAg5hiC7lZNLxkhyvQbn6AAa+QPMQn'
        b'F6kJM9cin/QShdWwlIGmxZfZ05LXFZwlR0gkEivYifWenxL0jAolbAHd8nqlFUlUshjgBskNB40Ub8C9yK6eRHZtLbzMJjzhHeyb+MND4Oqo8V2WihwKeNmWJCxSsWMQ'
        b'A7vzqIEsgzfCrO2sQQeD8HdhLiGXboKNNE4zPFwnV1itZSGWPMUAt0gOuLqEtspb7WtxDZuYpWTAbSQX7AQ3qeWyRJs25EcqZPAyk9gM1Qxwm/QmwBmKHkVoAkflsF9h'
        b'RtiDsyQSBiSqp1KpJpOi4TlrC1sr1PiJQGYCmQnbwFmavm0LcpEXWG9DIgIEMGAPGeI+i7Y4N7LgcWs7G0ssgbCfOZXMQq5DM83VN+G+cmTkZXZohZHtZ9qRCQGWFJo5'
        b'0C1ENbDfFlXpgplTyJnwOkKjmjxWAi7J63Fnm+FBBrhC+sKr8Cpd160APXIrej3ZDLiH5MKDSHdQnlI3y8aarupKYDqRUUtLqXIFbObBLiQ+4UQN2BUO9qNtMLVeZ/hI'
        b'FbbYW9WvIQkWuGKHfBTQhnYZnXRXu+E+eGp0ardhE54auOBX3T9FxJB/ioTLZlD+YtG0gk9mOHwU+dssi48dLD7O2EwwlnxRpbn1/Xxx8+zdM2SBO0uvHtd9ut1s3rJP'
        b'tn9i5bWZuLPjY/jlUOAhcYvz/j1f3v5g/ddvfZlobwh4cyjkyxUPf/E66TkS8fNGm6s/l51MUllaMT5dvrqj0jjvu6kzrd0aDn3zbczv2oYc2i6dK5Ys/OFvf3j9kz/4'
        b'R2Qectzi+dpg3DunWHM2rnzYMhgUa+W48kFvf1lk4r0ltTv/uMumwqrHMu/P8NT0GNGd9Vs+zmzzPZJ+1Ori/gP+L20/feTb7leXHP3lyneHf3A4HPyoFaI/PnNcz5dK'
        b'v/iwdWjg0IWR5csi9667Lpo6/y9Xrd4Pql7e+xnz00WBP+Xk/+L0jXj7Ws7mlkdvLDh99SfbW9PVH59bV8l+c8k/PD9dLs++sE72YqKp7tHB4vTM+wfvx2TceP3+x5dO'
        b'T7H67O7J4oToPzakvjTjwwWld9qOf5S38E++V87/Rrkp/7O3YsuYSQ6ftf7xxa8/sqvwPfTbdslSX1O0Y5Rz4Xnn96fHNeU3Jy762P6NH3OGfoxl8J3+tGf/n7YXJ4Of'
        b'e+t9fnf+vbm3333jlR9vt7/b7t52q7mr4Tc/dt/6TVZsjWZWQs3cvX/7xTggeqDM+/Rz3xznxXZffDDFsvijYws6ivv/uGXVD2H/teXu5v4/fm3/5/dO7Le4zbN4iJUn'
        b'PI4c2uuwJTwfKTbYEY5UeHk9OIt0ODhlTkH4IjE6w48IANeywsN4EQgGNhGEB5e1Ah5LeIhtgF3FwsdPDwm4H+6jnh5K4A2qFhzhwOv8CKQ/m1DrZuD4atDOEAhg70OK'
        b'F3t4pTnh9WB7KJLJHKQ/UN/rKzY8xLJpgdj0aE5WXlieOWHmAVpYDIs14Q+5lHELg6f5meFhqE3YhJRyBxN5C+edpzKRzOyHtx9i3VMKd1nkFAhIZLvOMtYgMbwDTvBs'
        b'n3pA899P5Djhjv62bn38cMeJfoCikImkchF9wNUwSRn1qKeHOfoIlEF4Bo0QOaTtQvIb+k8ny+Turc41uvNQzsVDzdG7BJv8gzSi4+5aR2201vk4p5PVuWi3HQbL3Lv5'
        b'gbtg0F1gcI80ukeOENGOqcNBYZ1pao/d+aZgnPHcXbC7wOTqqQ7du+KBa8Sga4RWbnAVGl2FI4QAQftO0UT3VmpEmpWalb01CMFxd8Y4zBEzguN7OKEnQRPbPa13Wmea'
        b'yctXXd8b0jnb5O13OLknWVPWPb13OhpYjDbG6B2BAPzRjAJdU7/BiZpt4gahpus1K49b0jdUT9SNN1eT1jNNPc0kTFSnaXwNnCg9J8rkM0VT3rNcvdwUFYdKvQ0cgZ4j'
        b'MPkGaBQ9q9WrdewBl35bna0pkKctOpqnydOJBxT9q3WrTRyuxrO34AEnZpATo4szcJKMnCQ9dT1pMjIWNell4ITrOeFPSiOEqNSzu0BdgMskep8YdOH23HpzH3AiBzmR'
        b'OraBE2/kxOup6zHmcES0tkwXdHpV36rxLdCt8qNQmVt3rjoXlR1e3rO8u6S3ZISw90wdDotEVa7dOeqcETvCJ+Bwbk/uCEGGzSRNszO/YZJhWYgZSJ9s8iGVjlDpcGCI'
        b'NuhIji7IEJigTjf5BWiyereMEEyfVBM3ULP4uL2OoecK0WXkCnVKAzeFvjNQ1zAN8oAbP8iNx7XTjNxpeu40lBn280f8VLzbZoTB9nLqNBuxIQJCOu1HyTlCmDmmUgla'
        b'2NDwC3Zn7HRyQ+hUY+hUg0tQZ7paqGGb3L1GCBZaayX1R+uqC9b6af0wWVnq4l4bzQKDB9+E5myvtjd5hqLpuKaaPDhUVYneIw5dRo+4AReDxzT6zuAR98jk7K623Dtd'
        b'H5ysd8bXcPiMuy53q1/xM4bPQ7zptjdX425w4aEL8zZvb4k+NFXvii/Elxqz3pQH3vxBb752jsFbaPQW4k4XkqbI9Lvl95JeqTVGFo+OrdjgEf7jyEIGJXujkjjuYarF'
        b'kM144Z3scerT6oHaAI3XDDJ8GDCZKpiNwfEJHX1IwPjfPmX9Nz1vPWApIM7ZTWXySNo9uLYUtOdkhWexoIpFsAjsE18GtyZsY23H9ortKNlnO7qNxefAxLMnwRW2j7e1'
        b'rH/7traCx/huNRqeFXfcby6mvZwrmhhoQEUvrK8Tc/OKkmKjuLUyKhMTMQF1wk2WgisTK5QyKW5LUi1X4CZWiqQ1XFFZWa1SquDKFSKFeLVYqpBz11ZVl1VxRTIxwqmT'
        b'ieWoUFw+oTmRnKuUK0USbnk1xREiWbVYHsGdKZHXckUSCbcwfe5MbkW1WFIup9oRr0PsU4ZawTCSCU1RZ1c0VFmtdI1YhqBwfIVSWl1WWy5G45JVSyvlvzK3mU9GsZ5b'
        b'hYaGAzsqaiWS2rUIEzegLENTFyc/vwkBomG5WFYiE1eIZWJpmTh5tF9u6ExlBRp7pVw+WtfAewrzWRy0HqWl+bVScWkpN3SWuEFZ+VxkvAR4mk/6m4VKJOJqRYOoSvI0'
        b'9OhaPQHOqZUqaqXK1avFsqdhUelKsWz8POR4IJMDrxRJRGgGJbV1YmkyRU6EIK0QIcLLRZLy2onwo4NZTY8lTVxWvRqxApopJtRkoGVKGabQ+iejWQiPV8mU0kmh8TFk'
        b'MpWiNpVlVQhMju6Uq5836jJJrVw8Nux0afn/gCGvrK2tEZePjnkCvxQjeVCIpdQcuJXilag1xf/fc5HWKv6JqayplVUi/SKr+f90NnLl6pIymbi8WiGfbC6FWG64GUqF'
        b'vKxKVl2BpsWNpLUut1YqWf8fndOoEqiWUlKKFQV3dGpi6WTTog5Uf2VWs8QSkVxBof/PmNR4XyT5sTkbb4se67u6Wrni6QZGOUMsL5NV12GU52luvNbi6pXPGTG2XArR'
        b'GHMtRJYLdSWRPIfDRjt9wo4T+3o+a/636S4TIyuKhC6Zi7QMgpwPb5bVrKQ7mAwe6yI0+ZIa8bilGhsQIoEE3pTLxZJfQ1UgA/8cIo62gyEmH+wzFjdHKS0XSye3mKPd'
        b'Ihs5ia2e2DGC+bU2KtdMtLsZeLXh8QqFHGmqCuTE4OrJEOtkaAGQzhNN3u/c0WqxVJAvi3je6Cf0/cy4J7f/o4zwlA8wAfm5/gCNW426nhwxa9bM/OezXUmtrLqyWopZ'
        b'6lkdUjBat5JiSCTA3Dky8erytc+V9fEt/xMMTYP/N5VJlQhZm0lVXoZ4JbyJxHoSnfAfGBgWA0rOsJ6bMK4iVPPrwiYVrRY/0XajfjE3NB8VT8qnSlkd5Rc9g1Eslq0V'
        b'S8uxWDasFZfVTIYtF9eJksc71qiBcV79JBhLpdLlydwF0hpp7VrpE6+7fPw+QFRejgrWViuqsJNeLcNeqlhWXcatLv81Dz8ZbUFFq7HaRGMqqnoq7HoiYvLoPicZ7Qsm'
        b'swwToSecI9oRzw25rZXQ0bXD0ZvDK/2t6HO4uNlsKpC2dKlEwliwlqAfeZ8Ww25wCWxfwCCIqcRUW3CMAu70MaOCdjVeK23+sHEBQZ0LceCZJGHMyhyCPjkjLalDy5Ka'
        b'RXwePtG6Azr5+bkR9INCvhnh78f2KgI7eDbKIATmPQfcgC1oh6uKzM4SgObI7LwcQTZsy8lnE9GwzYwPz8BuKlAabAuN5I+rdQKHHCRMoANnvanH7jHwdMPjI7SCrIIN'
        b'9AkaPMKhqjPggc05lhnjDsvwURkcAB30Q3vt5iWwhQ/b8rIFDMICXgO9+Iyg2SmbOn8El5ItceNZm+B+2JqTD9pgR2QmbGMSfk4sqK5JosK+QR9s2USB0TAFsB02ReYD'
        b'DdjFJgL57JQGOKAMxYDtcBd3AiB1tpmfRxI8cBOeWsIGPbANttDB5JdhL9w7DhqBtkRm5bnATpIILGXPAE2JFMlrwC5wgR8B21CDEdl5sCl8LrzFMyO84UEWOGZTr8Sx'
        b'/EALjtuNAmXlweZwHmzKNCPcXVlRCWAb1c6KeniUXrt90c8snTkaFXUIcwkt2nFhjAwcxYeSiNNAE2inDlvBCWn2Uys1A27HS7WHQZ2Omns4CGPguRls6uixKhjuog9N'
        b'1XCnJ+wCRyvMCSKKiKrhUM0JQEfhuIV1A42jK7sTnqE54xA8sjoHNILdT61uiILHoB6qOCKCNwtBf50Z1IKrBJlLgPOwbzTaqQuRtx9VxoIeqjGiJgWephpOhS+4TGCK'
        b'PNCJeALsgCqeGY18BpwDl4XCOmYFVBNkDgHOlYGX6NCbDPCCUAh1bHhoGUHOJ8DldKihjuXSVoCzQqGMaQN3EmQBAS6QYCtVYTU9E2H0s2fDRoIsJsAVeL1y7BB6D2xE'
        b'dbfgHXz8ehSt9SWgofqpRmTbjavAUUzPY4SkcDRYqznVjQhH0lqXuyGl2DeNoIicDg/CJnkx3IbaSUd3vSQd8rLMEccJJGpml0mC62MJHpM6YE5zKsGnrm00US2gGm53'
        b'xAFnVtTKQG0KGMiJEIThhQbnQX8oi7AvZkpgC+IEijytzrAPP8xiEyxWDtxLgsPwcixaFOrwrxt0wsOYdo7hNOmgtoKiA7ekiKIcuMigKQevZSvxczzQCK+lUJIgAmcm'
        b'kcNYcHys8Z65xZjGG0ErTWPQj7gb17hlw2sUlaeDbaNU7qulhDwKnJ7xrPRaMmjZhdvoAClJA9gpFIID4PToSsD9fsoQzNXwgsVzZRpch1eQUAeDa1QjsG0BuC0U1oLe'
        b'0TUD3W60CmkEWnjtWWHng35a2GFPDj3Bw27gglC4Hl6ioxKqwGFwgxJfVzu/nCxBfgSS7VAsujhAoYNJeINGFjgBzomohY0CJ8FFfKLOE2SxCEvzjfAGAwnJSTeKGwL5'
        b'9gQHHzOtlNocWWdLB2eAl8y4Y2u5fjFaShY8S+lO8GKUciKXrKpATCIDV6mu2OAKUgeCHEFYPmwFbZkkYV/JFIMD9pQBAGcYsH9ibAcimg04g2MJvHNZYM9UoFVOQZDW'
        b'U+HNUcCZMRPDQHAQiBxpcgw2D96eT6sL0D7emoSVZXuwwdkq1BqWbXyuBo/kRD6JgolDwr0esVUzRUVwMz78qZARZx4a21EmmsTJsUbuILnsGwtiYMLb8By8RYKDlfAa'
        b'recP+s/KAXcyx4gDmhC7wuZcfFiXg1/3iQEHzLL8zOjGbi3CkRcn4VbYnhmeXSAwI6xzGPDQQqCmzt/tizbxZ8Md40MtpjHtN1WNimoqMhnXxkI3WL7wAjxGgqPwfBYd'
        b'5gD2uPE3b3gSv1PJtDcvpmf6YjXcCloKxscWISPURscXOS1Q4gfyVssIa9iFXyEoJArng8NIzChHoQ8MwHb5BrhnVJ2cKab5uwPcWGMtcy4xw84E8gvcQBfFtvXgGOql'
        b'C76AFA+OKxegFg5SPPfzHAvqNZ+RnHqbhrh8go5GuAPO8BH4AR9wHRkF0EGUTPWlezgSHA0uRcHrDUxs1Iha8EKSshhXXA2ZJ0dLAtuy5s0F/VGF86EKttiCvZHzQiME'
        b'oWj6YVl5VEBJIRYPVXhxJp45FcIyLzMc1yChyVkwF7axUP8bHEGbC+ynAki6MmhfySGvUtIaUEwo8TsePqAbXH6KfLAjg6bemrpRCwS2g+ZKcCm2ziwINhPkPKTtgAq2'
        b'U5MsA2oWriJhLzhBKbzzlnnKGMqS2pshg6jKgrthhwK5HnuBag1K2pAROhcPzrNB/8r5ipXgpTgSrbvZYrEjLalXFy2lGrRMpZsDJ7mISyhLcq1idQ5tJMGL8CRJmJUw'
        b'wvL4lBzPy4e9T7Q54tkTtDpf4U9F+lgjHXbxKWtwSYoEHXTDC7ROulAFt1OTzIAn6UkKCykeCwHbhBM8E9Bd9NgziQIDVAflUwImOCZIx+6nPRM+vMpj0Qx3YQ4hjK9n'
        b'rvQkyGxsxbviqK79wC54VBgLbivNKG9EjJTZLQrDDugShbFrSNgYQJAzCHB6MYd2YE7PQ9b7UizUEbCpnrIE/aX4FAZTcAk8ykB10YhzCwhyDvIK2InKNFQxAylra+ya'
        b'oeVuQetcCHVQlWALLsZGz80c47r5guL5T3MSUkeHrWAPOAG7qGFtys0BZxEFb6PxbiQ2Ii2ylx7WAImk8Ww8sn0ucBvBcEM+RkwDhQJu8RFJzsZNRzZjM7EZ7oJ3lPhl'
        b'gbWL5XL8dtGi7Mj5ofhYHuvGhRN6XygwB/vgbg9lCoJfAPaATuv8PNgmKMaygQQDNi3MzF6QWQR1eCrg9FyoyhNE5OcWsJGNvkSAU1BnhbzLkwVjgWWHEffcQax5Fd6i'
        b'3veIQLx7eixWtC8c1ZyDR+FJNjbzBDjrWY8QKVuxtQIcesJkxfJRj0ETTXsUp+cjHpzIYztBC2Iy+1m0n94FOsFxHO90xRaHjl4tAF0kMvuwjxrXTLA7UA6v1Nmbobom'
        b'pEs7yGC3aVQoYvWZJd1sOQtZy+MfO51ze1O6NF1R8dVvOwLze2KzDr5SPTjjoH7PFRer3/ss8c2J55446xt0JmxxXdtgaI9o2ytg34kls1Rt7mtnx7tqveN1L/jcIe7c'
        b'NdcNf9h17fsXv7m1unnVm68JP5/2edy3m/5u/n531iLD5xZbOsxumAs35EaXNn9SQCzMr6w4+N3N3/4StlD3dp9i6ql2VrYqd8r5KZuXXM/gXEyBYQuvW1ay/d71/WsS'
        b'1+7dfQEfxX+9IiNpXqB5e/WRz1+5w71QeN/6/J8+s/srr+DHsM7UdT9Y+H3cmbJi9tfvZNv940P9bOjtZ1e5J0i62/X1jERm6bGPp5nNvHNy3TvVm154f/bqaZ3kUNuV'
        b'L8LPFXTON+xVat8oPfybPM+9vRdWLfmd4+mEub+dckFzXhnRtUuS0OH26vfCG594TW03Wb5y9E9vez68Q365NLqVvfJRnXnXa749F9MP8ao+PTH3QcpKdu5nF0++U3fm'
        b'67nxJ81T3+osOPrd1JUF9rpLXj/zV37eanqr5o2CzKRjPN95b6/K3r53V1l2x2t3PhLrLL6capczNNvuLZn97trugXccl/kPZI+kvKwa9nrZ3eJ2pm6OLn+E8XIL64Gl'
        b'9Hhdx4mSdae//tu9BapDsY0rAlfMe/ut200LzUPqzm2Me2sZp7035wVd76vmXmGr3qu/urfrnao8V1HgsWVfRfq85phUrH37qCLu+GuMDyMHvvosO4zPXz99+K+phYse'
        b'9P9VErJ6Q/+ed5dE/6VQxCqy/ealSuOq1+++ufjr13uufD/9cuqKsPd/Wnerr0uwWZQnWHb6upU24S/9q75bbvF5qHO1q8RrgQM4c1LS803236ZEDjfHFXAGZ17Kavv9'
        b'qryC/R/uDe9uOjLNeekWkf2K9wwf7WH8vHuKY8fvT58c7lHYbbox687vTwrWBV29/Y8iv+2Ofj99Ac8mzrv9VXjwTBFrxWxewPVVnL9PFbzWpessUcf32fG7+qVZb9R4'
        b'fn3yxLuN3unvuq94IH9o61N2OHi4uOdicdf7tYPJL/5SK7JZV+O1sPbdVdtlI+0PT1ziW307zDfIb6g7vs//01t/O89zreVWFt378dDrHxyK+Gzjx4PdDRcFl858EHHe'
        b'6+imKJmZu/QP1QmHPs87fKtTf7bx5NvfO08Lv1Bzk5321fmesLYryh9e2xJQ+VlgL/crw5/+MH3u0QanpuPF95TsvixF/8Lm7LOrycHwt163fDPhBwtlitcXH1RcvVPU'
        b'pnrd8oN7b8V96FPw+d9sNcFLP19oWvjt7DfPhh/6rHqtYN/n4O37m9YMb3z7q28N1WdK5rwf+NLf7rznbtrVNSI6bz17QL1mxVr3b/w++12If59z6lfrPzpcf1V91tc+'
        b'NT86tvabX2ZwPv38+oZFlV+2yzP0P7/6l380xXW99T770y0/SRT/lT1H8EvKtZWHv/Xu3vTG0Y9+IVI/fXHn9A94dg+xyz8VbIe60fAopC+wwhTA5nhkdcAVVmYl2PaQ'
        b'Ujq3wVWg44dF8JBZIgjLxYmgnwFOkPAkHcXVHlLFj3gSn4W3JnSMVgO8QTWAnJ6TNaPdLIPHcSBWO0MAz0LVQ+zZrakEW3PCn8RgweYo5IkeC6BbV8MbUAtbxPDOuDAx'
        b'Kkgs3JN6yxTsQLN46amALOepc8BuJjw4RUl1sRCehr38/LzwbNhOoD6uWc1nrJ0DTzykXhCCO+C+HOSYRgqyfAnCbC0jArYsf0jtrc/CVqscNLDRucEDG5AnGsWsTCSp'
        b'+DJ4fBq4OOZQNPvR/gQ8BlupXjdmgxN8impQU4QaBn0MITgCrtMvvr4EjoOd/AJw6ql3+ebBFmpe8IUG5MBeQmuCfLM66v1ZeBntFwjXFBaTXMTj/l9Hk/2bEzl2fZ55'
        b'3DoanTL2m/By4mpFUmxUw/gbKmLNx5KOWJOaES4eB6bvmW5wDjQ6B6rSTK7uqjkmFw9VusnTR5VtcnNXZZg8OCNEFcN2PvkN/aeTZXL26UxWl2vSDc5hRuewEYJ0jDB5'
        b'h6hTtCyDt8DoLehMM7l7H9iwZ8PuTXs3IXgvf83Mbn6nOSrFwD4mF47J2R33rBHS7+9+Q4gYjvNJU3DYqVVHV+mcdSJDcKIxOHF3QefMTqVaPOzO0bD2bOrcZPLmjhAM'
        b'z2gTJ0LPidAqdSuMkWkGTrqRk67npJs4Uw7n9eRpgwycKCMVgjYcGWviCUyh4aYQPmrdFB5lEkSbImJwyo80hUWYwiNGPG39vUYIlKjZ3ewRDuHlpwns8VH7mAQxara6'
        b'xuARhi6Tp+9oqbevJkidok4xzcp4jQ/498oMs+YbZ803cKar0zVhBo4ADWuxIXI6ulD3qIxn4ISjC7cg0HtGoguHULHVVd323faoVD8lW++Jr+HgaE2NLmiAMcAcYF4O'
        b'GxDfnXmz6l7A9VpDcL4xON8UKtCKdAxteZ+1KTBCk436maer1xX2NRgCk42BySPmLDwRFp7IiBXB8dfk671j0GWKTULDiDBwotGFw9qkep9YdJniklF5pIETg64n4W7x'
        b'U9Xp+imoTIiuJ8WPgX8cpUW3zwjDjetl4vC0sSNMlBvmBGpWaVbpXHX1A446+WUvQ3CKMThlhI3qRswInwBN2og5zlsQPkGa8hFLnLcifEK0rBFrnLcjfMJQW/Y470D4'
        b'8LVpI44470T4hGpdRpxx3oXwEWjLR1xx3o1uxx3nPWgYT5z3otv0xnkO4ROsUYz44LwvPQY/nOcSPhFaxYg/zk+hYQJwPpDOB+F8MBEUYgrhmcLCR/j4nhhL1KyRCExg'
        b'x95EOjqN5vwRgu0ZbOLHaZN14oGZA6KB2ZdX3Y2753gv5p7LK1MN8fkGfoGRX0BHE5oCg9Xp6vRhfqTOoi91rCxInW4Kj9YF9eUOzB4Mn65mqZcYPEKpoElttjEkQR8y'
        b'bWCmPmTWXUeD72w1E5HVP1gj1s7WVBu5UbocPXe6mm3yC9QU9jY88Ise9Is2+AmNfkIsNWHDU4K05JEQ9WwcvFmmKdeUH7dG0L5+aibuYHbvqge+UYO+UQbfGKNvDJJV'
        b'zzA0DzyH2YPxGfr4DNNYAyNMAvXxv0cYDhVcsD5jrUsfCLicfZc0hM4yhs7qtlWbadgmXqzWW1c8sMDAm23kzUYTXdRtZ4oQ6mbqRLrZfatQwXKDB384fiqi5KyBWZer'
        b'H8RnDcZn3Qs0xBcY4wu+YZKesWoXJJ+eYdrZJg5X7x+N2djDRy01eggeeMQOesTqigweyUaPZD11jZPhIK3LoLdA7y0wTYlBvI6GHptFmnLmo1ZjC3HMZkARjtlEKY7Z'
        b'LCKHR5vVrjR6ROvCjR7TH3jMGfSYc1dp8MgzeuTpqQt3EKH3jELXMMf3cFZPlj54xl2kjjKNnEw1ORwUqinUOl5wP+Ouczzt1ed1pOR4iSmUd8H8jLmOPG3VZ2WiNID/'
        b'1ZD+kAH/i2GUDlBelxqC84zBec/Kd3pPqjoVx9ymawR0zO1wTAK6QeomUs+JpHTLNL0nvoY9OHh0oXrPMHShu2HfCL1vBJpdVLJp2qy7GfqUXDT5qDw8eb98PHmU4iXN'
        b'J4f9gzuzd2cPe/qOEDysp5F637Jni0ZucOcb3fmIt1z9dS5Xffp9BpSG6HRjdDpVdM/lHZ83fPQLlxiylhqzllJlv/fgmtx9cAwnaoYagT5yzj13Q+Rcg+88o+88vcc8'
        b'k1eYHl38XINXntErT++Sh+NCl+pdQ9FlcgnWuwRrlNoVxpAUg8s0o8s0vcs0kwv9ln2QwSXU6BKqdwlF/NCZbvIPosbtzdX4Gr2jfr3XUSCdk9E7Flswf03RoDvP4M7D'
        b'0dHTe6ZrhQbvSKN35Ajh4pmoS7ua3Z89IL9YcLngrmgwNkMfm2EKDD2VfTRbKz9ScLzgQeDUwcCpA2l3AwyBc4yBcx4E5g4G5t4rNATOMwbOQzIeFKZZoI3Wlo1FHQ/4'
        b'G4JSjEEpI4SdD51oyBEWyz+XNMUkDJCXQwfS7/rfFb0cdDNXG6RJ06Q9+igkGpEUAYxPTWEJWoE+MRNdptDpd0MMoVloVZNy8HqiFK0tPxfn+RiBDEIpE6M9evQIKeXo'
        b'eJ1ogNSVXbYyRSRpawaC7pJ3GXcZN3mGiDRjRNoIm8mbMkKgRMNG0IGh2vijqZpUU+psTZqel2wInKoPnGoK4mmLj67QrEBmRJOm9TxS8OgbHzwlLkawNQbEY4FKMsUn'
        b'alia5QauEIcn++gpfjVyInWxBk4CfWegLpMn0nyDnny9Jx9HGi8zeoQ98IgeREIYaPBIMHok6D0SUGZ48lUdxt9aYNgGmRym6B2maOK0vsaARINDktEhSe+QZHJwO2C7'
        b'x1YtNjgEGh0C9Q6Bw86eqjy5DXKT3vNxXhDNei96SrGzOR1A7DDEwuet/0Tg8D/t0uGHoaWTuXCyeOLJhxwo120Phj9KjEYYi1gk6YTDh/+Vyb8sEhl/DOmwZRzxkt1M'
        b'JnPCgfJY4PG3+LnYAUKMv4JGLGGUk0uY5YxCwrKSxxxyoM6yqThfWbpMViv7yY8+3aaoIRsN2xWXc0VSrhjXR+TzWEMWJSU4HKCkZMiqpIT+TBnK25SU1CtFktEa85KS'
        b'8tqykhJqPenQcIrYSZjYz3TbgQYrxzuarY//DdtE68cuCp8+U22Myba2g1cV1pZo25QvkI1+nScSHraHN83YsA/u5pFzqr8w+jPk2/FBj/m8Tbtfz4EzXF6tjMnqKaq5'
        b'flp5eunyP9/++uclrrWHUqz8SMeUqpm8dbtnBX8T+offnL1lnD7ofvYKb1XpZmH3j7/74XcH17dP/XAe5/fa9j9+EfmlIbYbfKit2ZtYJj77qtc++7/Nf/TtW+s/c8n+'
        b'7Q+OZwubIz+z5C3dka3dkv7jkqqXb0UelvyjsvHiFuFf2G0eYY9qjt2d/l6cJ3/zg+IVRX8vNZvmO7D4ABSeH/R89e9WhevPBcdwWvt+uOZc+eX+N3WtbwwI9HNjU1xf'
        b'iwmEV7ZnGh5etn4heFEBZ94rqvpAVVas81J9du6RNlO73cqQwVciFM4b9Dlfzn7B1EH+gfuCarGNc0ZUNgcm1jO6XuHllpldUsMUN50qKLyMfXYRTI7X/bjqVn3By25X'
        b'Lu5Y/uWtM4c6m12KNnS1fuD1/ek1H+XpbWMHBNJj5276sW7s23y4LWZWQ8tPC04EK7v3vhUjzujkewUN7j17we3Rjcrb8vbf6+7V7X1wNmHZ0bVhLR8fS7Fb80buz8z7'
        b'UetW/92Cx3pIPQTdX5IGziXBllySIBPR3juzit4EH4N7wKnH31qqnUp/bQl/aQm2wZ0P8dEQOMTlWYehnSreJOcp48D+0WX3A5dY8ALYN/8hdUR+iaeQg3OZ+YLQsd20'
        b'I+xk1s0Dugiwn+dJawOLX03+fXtKvOvmzqB+W5/50ZtJJFiSWlF5SUnD4xy1jRQwqY/KPKI/LBNO2LqOsMwt3U32Tip5Z0zT2ta1av/mjaqNarlaronRiI7HdTf0Nmjn'
        b'9WxRb9EFon+yAf/LyoF5l9ddjLgccTftbto9p5czX8kcjMnVx+R+5OGljlGLeuO6LXstNdkGjwidu8EjUZ+Sb3DP188v0i8oNs5fOOi+UO++8CM3rsZpt3SvFClw5Jh6'
        b'LCKRd+Tk0jlzr6tqlmrWoxFz0hI5d05+nYITNnrBHAM3w8jNMDhlGp0y9TaZlO0zswwdIX41cWBZIuP3q4mNBdfKZGPf6TbCxDlPjrqCzgXztPF0Thg/YEbnZsy+W0zl'
        b'hikMNs5RGFSOwqByFAaVozBwDjn9tg4Ix5zOe/kgrNF8SBjCG83HJiDM0fxMMo1E2NSdBY1tSecp7NF8eMyA2d1ik6O7ukIbP1l2xB4DEmOJ3oKD9l1OHqiOvkaszaag'
        b'KpToLXxHHHJJS/wqzv/hnxUMwsrBZOmgcu+Uq+M6a/SWUwyWU4yI0Ix1TEvkCf+70m+YhFUA6gf/dWh1G2FRVWvM0d0Ig7TEu4VnkhfXf4P/PMTJGN5EWMqtaJ45fZYz'
        b'AZy9ZgmYtFvhMsRAFulf51RMKucukzgaT5wN/PbSE+nGJk9+fczT4JGkA/YO/iPJv9QDOW6ZTFy3m2nBrK773oaUb0dFFrcOrm6bZrd9hkfanekWJn9Xj31T63e1ua7Z'
        b'P7j7S92tiyeOfrNnlsrJ6WRP1u/evBlx6Na6774Pfq3da9Wfspjv5vte+b5+SuqWsKoLO75Kyo/fn7v/b27vdAyZplndf3MDx8Zm5k4Pnt29utq4NLv0bU4hHm8PHL0u'
        b'fvt6YGZk3ImP3HP2+9QFvc0zp6zCJm9whfqkZwF1em9OWMPtsAv0M6AWXvCgHtUuB7cLcwoE8CKGKhAwiLVpjvAmExwB1+AuykpxwIlS0IJDHPA5PWgDHfnwnDlh58T0'
        b'hadgF/VS7rIo2Em/dwsuwGbCjMWwAAPwGPW41WtTRs64r4VaLxbwGLATtC2mnqhmwjPwxQlfE62OoL4l2gQOUS/lptrA5oXwJX42GwfcQDXcBs/wAp5vz/6fP0GdVDIC'
        b'xizgs/ZvUltYLa1W0LaQzlG28LfEqC1EAuNFsJ235uN/JluXB7a+g7a+L64z2IYabUO3zjGxrBpzt+fqHf1PJBpY4UZWuJ4VbmL56SdeJpbt1iz8b8RsA5uN1Mf/o7TB'
        b'mrBx2Vow7i1K7hBTIpYOsfDLdkNshbJOIh5i4ahStDmqLkMpfmFqiClXyIbYK9crxPIhFo65H2JWSxVDbOqTdENsmUhaibCrpXVKxRCzrEo2xKyVlQ+ZVVRLFGJ0s1pU'
        b'N8RsqK4bYovkZdXVQ8wq8ToEgpq3qpZXS+UK/JbNkFmdcqWkumzIXFRWJq5TyIdsqA5j6KjeIVt681Qtr02Mj4oespZXVVcoSqgNw5CtUlpWJapGm4gS8bqyIcuSEjna'
        b'VNShLYKZUqqUi8uf6GPqsXvpr/64XFqN5o4lWPvIY8nH/tFzfohZ7ElSxsSq739++i/T3dhMvmxjOXMK8fIUu5lRzJ8sxr5IOuRQUjKaH7VVP3lVTPxQNVdaq+DiOnF5'
        b'Ps9CloqlFm37RBIJMrLUAk3FRVaIh2QKOY67HjKT1JaJJIh95iuliurVYmrzJ5OMsfyTfeJPFin0xjJVJiPovax8E0pGmCRJjjBYJAu5gSixIaxtt5qPsLLNSJcRYly6'
        b'xIawdHxg4T1o4a3ONliEGC1CRggGGacPT70bfDf45dBXQvXh2egyWTiYrNxU4Xp3ocEq1mgVq2fFmggHPeHQ6WEgvIyEl37soob3vwB7Qrlp'
    ))))
