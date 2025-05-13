
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
        b'eJzVfAlYVFeW/3u1gewioOJCuVPsUoiIG+7sqCguqFBAASVlAfWqRFFQFAUEBBEVcVdQEUQQRFGC5pyJ6XS2znSnY+ikY3fSMTGmO0knne4knfzvvQ8QXPLvmflmvpnU'
        b'x0t593PO7yz33vPqQ27AfxLyF0L+hFnkkcKt5dK4tXwKnyIp5NZKtNKNshTpbj5zfIpMK9/NZSgEn3iJVpEi383v4rUWWslunudSFLHckEKVxXdaq9hVYYtXKDdlppj1'
        b'WmVmqtKUrlUu3WpKzzQoF+sMJm1yujJLk5yhSdP6WFmtSNcJfW1TtKk6g1ZQppoNySZdpkFQmjJJU6OgVfaOqRUE0k3wsUoe07t0JfkbS/6s6fJTyaOIK+KLJEXSIlmR'
        b'vEhRZFFkWTSkyKrIusimyLbIrsi+yKFoaJFj0bAipyLnIpei4UUjikYWuRaNKhpdNCZ1LCPaMm9sMbeby3PLVWwfu5uL5ba77eZ4Ln9svttqwh5CaLpKGp3cxz2e/A0l'
        b'f8PoEmSMg7GcyjJab0m+71gr5bbn2pBviZFO24I58yTy1QOvYROWYkk8lsRELsNiLI9RYXnYyqXeCm7KIhneTsZbKt5MCTNDM+4VwqJwP5ZFYRnPQTPstQqTQAvsw8Zk'
        b'vncRUvLn2LeIaMoHnnDi/8OHVMdeevliKaFXQujlGb0SRi+fL3kevVOeoneuSG/eNAvOxvKRglMmeuX4xnKssHq8lJPZ/IXALFG/yW2YWDhXbsk5jA7gucREL3uvsWKh'
        b'foWcs3S/K+FCEm0uDjFxeitS6L9+hOxrRy7kC3WQ/1eSjqmb07p4/RBScTP76JAuLtGetPZ/z98Y+QnHihtiv4q95ebuJll6n/9xxBdbFnA9nNmLVCRB12bC9lLfZe7u'
        b'uM831Bv3QYPCa4V7eBRWePmEeYdH8ZzBfsjs4Xh4EGet+sj1o5ylXOVSpf2843+Wd6lP8k7xFO+sRd55DrXnRnPcCL/UWN8rO5ZzZl9SiBfNcIUsuswzAsuwhKDlFl4M'
        b'DfMKW8n5R8Q6Q/UKKIVDXJrcAk/5YaOZgsAPC7LUU1LhOpkBGrjseUFmZ1I8Bitgpxr34E1opzUnuAy78Wa6lNmTHdV4BI74k+9wmEtei01soEVYBnuwZh0elHOcD+fj'
        b'kMMW+vpKK86J4yz9XDQ2OQq5KLrb6Y7cRDq5oUibO8Wa073rFi8RNKRk0tA3P0v8JHFjaqTmtVSfKndNqOZhomNyeqo+6VFiuOaNVNXyMI1qaYTmsvYif2lY2icp4ZpX'
        b'Ja9MrWu57h8meWn5vdgRZ7zuOtk5eG45fqLzaOvBht1DUwx+0rRgLrTIuTxsuEpioqqyZTpUWRMuqaLM3h5EtEVwxFfCOUORzBK6s02jKHH7CPtOYmkI3MR9WIFlBJgz'
        b'eGiNwy4V3yNxV6mkRirwx48G7juXWanGzFytQZkqmi8fIUeXaprTY8VsU0KKxqSlFlSgWs6Nt+FteAfeknfnjVTSRipllbRHvlmjN2t7LBISjGZDQkKPdUJCsl6rMZiz'
        b'EhKemlTFGy3odzl90FEm0PHt6PgfOEgUvIRXsKd5NKWpIcvNM9TLIxrKYwgu5JzLSkJkgWwk1K5bnCzpRZ7sGTAmRqIfxhJmAqQExhIGYymDsSRf+iwT0KcXg2GsiGZg'
        b'WjeVGLSDBOneHOyBDm9otGLlUIfdBHwHSUdfbry3L1ZKzU60vB6biTBEiGFtqs8YvKB7v8SNF7xJ7elRXp9NjE78ZVKoJlKzMfVhysNEr6pQzZ8THdO4qyODa2pH7h4Z'
        b'9Gu+/EWLN1OPqHjTSNLHUok1nlgzNtwbi8Mio+WcNbRK8ARv3SuMJ7jNShmve6xFkabqMzUmJlOKbM7DhpcRiRqt+uUpY/Lpkadok3QmI21kpJZHJRkgQ4mROqUBgqTd'
        b'PfsF+c4gQSopI6onwSEqyamwiwqTeogYL54btUkGB6BrMeOWDHZtEKAm0BToJ+MkSRyejwhlFViIxzyFoERSwXMSLYcNsStYRZI8SsAzzqRcyknSOGzEmrVmF1IR4AUl'
        b'gjecNE2nQxk4vISdeIhVbZ4O5wUjtpMqCSfJJJ2IHSgyjyBVO6AhW8CdcBnbp9GZYDeHbU7QZB5OKmPHWAlkmEZaJyd1hRy2z8JTrCNeh04sFYiwjxpZTzJsEzbHsUq4'
        b'iA1wBNukQ8xT6WqIScO2KXCMjbogNAjbiOp2kzqyHGKhsB1PrWVGzRfLhgkLJwhq2msHh81wG6vMFAVZWAUHsA07oZH0I7RDLYc3VpHVUArtAyKwbTx0kCoLUnWMw854'
        b'vM2GxMM74rBtHLQINlZkOrzGB0gTWKcNcBovWg83GBnz4TyhCW/HMS5na1ytE6KxdRqtIX5aSr6zCu1GD2tfDyt/SjEe5ofAcdjJBoMbK6DQeh5RiQ5GMu7h+fAYVuUd'
        b'ZiXANSzHthw7uoIzvKcLiOu2xmuZpM5ziC220BFv84E6vMDYhAfwXJR1Cp7JNmMHieqwlZ+URroxmooUcEPAW7bWRhPtVsOP9Y1nNVBl5yRIA0143ZpWlPOe3niC1cTh'
        b'bT8BD0nsbAkbpHJ+NlThEVaTj11uAl7GSjtbO56TDuFDhsE1trzQPCgToHqanW02JekG70Oa1YqMyB9vDdeX2WZBmYyTTuBD5HCbVYzNnivYYreRQSaLw8sKaGWDReIx'
        b'PCzEYaEpMEDBSVIJpvF6rkjrkSGJAjbsIHKXixi8itWE41TwcGSqVsC9UICt2GZP+dfMB+BprGCDbg11EFYS9Hb01l3i1R5wTqVkTsy4Zhgf4CgouKV3Nt2TL17LCufl'
        b'OPNBdhEyzu/OptXSO/NY4RhnF35W9COeyyKFjrtsWWHczBF8iOtwYvvu5N0zSB1YYc28UfxCj3YLLuRO3ojw96WscJluDB+6uErGKe/krV787WpWKM1x4yOjiTNJJC3n'
        b'1oewQmv1OH6pYbuCcyBjRisWssISq/H8ijk7ObLOvNUrbmWzwp2qSfzqyectyDrzauZ0RLDCU+Mn8+uCb9J15tXkjRIp+muKO584h3LjjlBjPWs+KxRmePAp0fOIvXpR'
        b'qJn7lr3YfZY3nz6+iewP7girpWs0rNBugS+vD19BorQXhRHq94axwtYgPz5r/H0S+ZExZ+1ZxwqvZKp5UyCZXUlajp/uywqv50zjtxg+kRMyhRrNvVBWyE8M5Lcb86Rc'
        b'Imm5fpcrKyzLCuJ3zjktIbQL93a8tZkVzkiYyRca13GcA2np4BHOCu/Fz+KLw1uo4ISahMszWWGV5Vy+zMeT55a+KNxb+3dxnYdDQvjKsZ4KwiVhxNxCcUlvbF3AV6e+'
        b'TlhHaFc0iROdtljI1+R+ISOsE0Z4/iiKuG3IYv64a4OCyyJj8taprPCzhaH86dTfUrln1Axx8GGFJ4dG8Rc3xlK5Z6yeeXcNK2zJj+GbJm+TEtZl3JtdZccKH8xZyre4'
        b'rpIT1mWMCFkpLsl3w3K+PfAcQciLGTVuLbbMh1pi1wIhfZq1FVU7Gz4ELwazcmE6FlivjzLa2RJNHcrP9sGdZleqJruxMZjZwE68niNImcHwxMNYzKzufLyAhYINlGGb'
        b'gO1U/av58eOgSiVjS5A7v8wfV+dLCa05NdI/jGOFM1e9wp92O0WikjuZq9euERmQsPWXfJ30PnFzL2bW+J0ysMI669f5izukMsKAzHs6vd2zQ+oAjhO3bHSjwqXK/8Ut'
        b'yaCwms7m/FQ8MjPaPI6aA7JhIiFvaQzsDSS7qAosCYvywRISGrokyqbABZGsH4iNoz1/tTXX5vKSDDGmXZdD9igkpD09dEvkNefVHOMp1GgkEb4RuD8mDBqwkmxYsFCy'
        b'lbivw8y+BMF1J2iDdmjfCuUyjl/DQZN3nGiYTrtBnac7CU6LfUlUYpMm3Qon7LE000z3j9vd10GbFZ4nqwjmgqGIM9IIhK1js4+M0qgMkWbr3yYhDivMVJGtFtGCO8rt'
        b'Nl+us+dYxJ5q2qz2W5vB7DqngVI8aqZBORSEr4pgEW8F3UhGQIVvGFx2h6twlOimSW63GK8yIMkWQZc6YBMeYPEIl+SGlSzItJ3Ie5I9E9uDZkAJ2UOFybhhKikZK0cM'
        b'P07AaTiq9vfbzIl7CAfo9aa1UGNSw9VgFd1znOL0eJbMRQnWYW2GWp1roh1Ocmmbx4vhYMuqLWr1ONhPEAZnuI1QAS1saXgoHM6qA9MNTAZcChTozSymb9kMhyPCye6o'
        b'NJoKZcVGOWeXJQ3C07MYS4ImwB51IF6xoPMf5bQebqzbUDyQFRFJevhiOTER1mslcBTPYbMflIvu+RQWku1SIByCKiIIEjykJkOduMSzqVtIxS24QNd4jEvL7g1/5odC'
        b'MZaSLUiUnEQRw2RjeTiLTavY8ieQgUrUgUHEK5NOx7l0cxqDkzuUTfekwsCSaLgs42xmS7FDZb8aykT3fHsF3lKTMBrrGYI4fQJcZQQQxl7bgaWR4XQXg6ehTordPBzD'
        b'i3DAHEXqp0G1SogMC4uiBwz920d3H5VHlI/KW2IF9Vo4j+ehzj0fG92hwcVTBdVY5+kE1S7OWDccLkjIfsnJgci13ZKxhLjjW/ae0d6hMg7PwUFZCA+XgrxEf3wQjsFx'
        b'wdZoJmvZ4yHBk/wEZzgvdqtbRYKcNjta5zBJgh28Ci6sF7u1YNlIbBO7tcMBCSHB03aK2K2W8F4gvXhOg7epaXKDQ1LGFJlhjpBttuK5RGyRwC1eCRfgCrNoGuiGZgE7'
        b'crCdiKBWTkOxcWOgS9S/ig14k8RU2G7Lc/DCdBoh+cMLWM8GjcWzvLWdNVRIuBg8J13Lx8PhYSIUDuElaBJMVjkywtUaCbzAj7bfyjolwCFbWkEm65gpwQJe6YfNYiTk'
        b'PwrbTCSGllK+XZdANz8qzIZRDfudtgh41QSFyxQcT7BPtLKbMMtZ1KOmxdaWtlbUcCVKp/OhIXBORMIFLxKymrNteC4HSiVYy0+RJLOaZGLhu63tbMgWxAW7pTP5MOxU'
        b'MtCpsdWdxDlGEkUOGSO146crlIxNm6TU5tvjVeIvSFR3QDqen0e0eg8bLhuvOwnZdJ4hjhLo4MfiCTzLaIqztBGsqKxIbEUkUkUYf4wwns4UqF9nzaqwZrPUkfdTwG7x'
        b'aAEvEp4fJErfSpTFi/PSrGeyWAkFK6DUnujYJavszTwnI0EalMuhViVhWjsnB2vVgQnje1VPhV2sGLtdAtWBK3Bvr+YtjNH//aeffpqbIhrIyoU5Nh9oQjiVkwihkxYj'
        b'ejF5EPYyUOZCPZPBFD2hV8QkVGlFUF7DOsadLKiGoj5UdhFAUFTO7I1wV0ElNouwTMNGBku85SVKqDzOLOKS+N0iBsytI8TtTTl0DOuDJZyeyWCJeyPFjdEu3DepD5Yk'
        b'Lr3AcDkrWNSQwmHY0gtLMx6nsMTj8ALj7Zx5uEtEZc4mBsrsqSKGmqDKXUSlOxxkqJxqKWpAMdl+nOrH5UENg2UW7BPnujULuxgw2wL7gAnN4q4e9kwaI8LSMZKiEgtF'
        b'xV83hMTSIiphl5ahEvcQVrF1lGKxQsSlCo8wXJZOEjnVvTS3F5fEBFRQZNoHizU3pk7uQ2YIVFFgLp3IrO7USLwmwhIOTWa4XDmmd5tQAGdFXPpDLYMlnhYPtkLhZrgI'
        b'y0zYRWEZo9L5j/uBFy4SIxxpHvModX1VZ/RHIQ57G2/+7m8cth73T5sf+W/Or032lEgkE3eNS7zqKImfDwv85k0r2fPRzjt/HGppGdizxU17Lo8bu+uhcUrkv6//5puE'
        b'HauuvV/7ygd3T8zLWLxjlp/Dx/enPppbcCDSLuUX3b/wec3W9PqZna53j1QvdPn6U27t9i0VD0LXlL8tmFpkD5XvTv9m2DdWuPrce8Upf0p9xerV84trP904qyOoM7Ha'
        b'LvvrV+NdfGvfHjblS/2KNZsDVtU+dIvP/ov9/S+vV24ddyrcZfwar4MunpXpDU4Pvry0cG715xHto2sW/vup15Q/TktadX2564wZK6+8/cm184/mv5ub8rLW41Fc6Jw/'
        b'tTQ8fHBXNvlBfGtS/D+O3Xxk8upqbqm4c0/+23vjz6zf/JnDD/dafsd1jNIYPl/5m59uFUc7Vh7pmJI47/3zqSMh7+97t0lPx55y+Ltp/omPbRa/M+fDptBPW+6O+uzE'
        b'9D9mro090fb229nj/6obO8v4+f4TMW6BM77Ir2v4W6V5dvvHrXNtcgx/+tXO394OnPrO7XCPT0JzP19ke1j39mdbDrw1r/zDDbtjv9t92k3yovNr7+Xxqevrv1i9TWVp'
        b'osf9WIUta7DUK5q4MazwIi4biPpdCsdmbDSxFiTcKcDTnj6ZuDfMy0PlQ1phCceNUMo26BeYqLN1xRYdQWXv0R90Qjs7/oP9m0xUE9PgOnGAPrGwk7jMEjKFAvZLvH2c'
        b'WF8shZumCC/3UCyPgFvYwHOWZAFbk7HcxIz6VbyCLRFhY6E5yiPKglPIJJZxWMxOJtdMgRZ6sEPGnAe1WEJccYWUGzZTisegId5EkZoI7SkRMd7roIqE4ZuJNT6zUWX5'
        b'5EHV8x4q+fPrHx9uOYqHWyajxiBoxBsWdsZFIzZuvh1vySt4J95GYsnb8HYS8k1qRcoceTuenmla8lbsz4l8HMj/+z7ku8RO/C6xslDwtLcV7yJxlFhKSMhOPjKJjIzh'
        b'wLuQGgX5uJLR6Xc73mjDPT4htRm4sAFnas+nTcUbbfuoY0Mt4PpO1247DTxdo9cVE6FkMzsmXRMC5b4qEjV5Rkf6iLIgu8El0GQB1XF5Kl70HJV4PSUCG+FkmBeJdEkc'
        b'D8es0wbtYOjUbMOxkGM7GHrVwj192ZJq27+jkTx3RyNlJ6yybzaRQa2UA/5bSkUmKDWDb8DYtdrWLK0yasWMAD9lppF98fcZ1HXQP8JMSqPWZDYa6Fh6nWCiQyRpDBlK'
        b'TXJyptlgUgomjUm7SWswCcqcdF1yulJj1JI+WUatQAq1KYOG0whKs2DW6JUpOiYvjVGnFXyU8/RCplKj1ytjFy2dp0zVafUpAhtHu4UIN5mMQtvoBw3FzsXFVsmZhs1a'
        b'I2lFL/7MBl1yZoqWrMuoM6QJP0PbvMer2KpMJ0ujN46pmXp9Zg7pSQcwJxPStcHPH8Kb8DBFa0wwalO1Rq0hWRvcO6/SfZ45law9TRB663JVT/R8ug+RR2JidKZBm5io'
        b'dJ+vzTWnPbczFQEl8/F880mJXqsz5WrS9U+27pXV48YRmQZTpsG8aZPW+GRbUpqkNQ6kQ6ALeXbjJI1eQyhIyMzSGoIZO0kHQ6qGMF7Q6FMyB7fvXcwmcS0Ltcm6TQQK'
        b'hFLKqGc1TTYbKYe2Pl7NKqxLN5oNz2xNL1SC2ZOMaU5OJ80E8i/zpuetOlmfKWj7lr3IkPJ/YMlJmZkZ2pTeNQ/CSxzRB5PWwGhQpmmTyGim/920GDJN/wIpmzONacS+'
        b'GDP+l1IjmDclJBu1KTqT8CxaYqneKJeYTUJyulGXSshS+opWV5lp0G/9H6Wp1wjoDExLqaFQ9pKmNTyLLHZL9TNUzdfqNYKJdf+/QdTASCG4350N9EX99i4rUzA9OUAv'
        b'MrRCslGXRbs8z3JTWWt1Sc9ZMfVcJk0fuFYRz0Wm0uufg7DeSR/DcfBcz4fmf5jvRi3xokTpgpXEypCWy7ErOSNJnOBZ7aktIsQnZGgHiKpvQYQFerIpFLT6n+tqIg7+'
        b'OUzsHYe2ePZin/K4EWZDitbwbI/ZOy3xkc/w1YMnJm1+boy0zYP97hIqbaxLNQnEUqWSIIZWP6tjlpEIgNg8zbPnXdpbrTV4Rxt9nrf6QXM/te5n+/9eIDwRAwzq/Nx4'
        b'QOyrI1M/u2PY/HnRz4ddQqZRl6YzUEg9bUNieuuSGCCJAisXG7WbUnKeq+sDR/4XAC02/w8ak3QN8TbPNHlLtEnYRdT6GTbhf2BhVA2YnlE7N2hdK0jNzyubQbNJ+9ja'
        b'9cbFSvdoUvxMnJqNWSwueqpHnNaYozWkULXMzdEmZzyrt6DN0gQPDKzJAAOi+mf0iDcY1gcrVxoyDJk5hsdRd8rAfYAmJYUU5OhM6TRI1xlplKo16pKVupSfi/CDyc5V'
        b's4maTbKmFelP5AMO7hjcu88JJvuCZ3mGwa37r5DoTs6Fe/IKaZWYmfUS2coqneluNFH/tV+ceP/ypp2Mu6cmfUISbRxDRov3L1gPNa7QRvbVM53hKjdzgXgLawxWcOvy'
        b'x3CcMtFmnNU2jh1oReBtqFXbwr6+tKsgPMFurCRwAao9B29Rl2Mh2aWOc5O7QlOWysZMM4J43AMnsNQ3PMx7tiXs8w2PivAOx/KIaDk3FcsVnrBbZ6bnIpvw7BbPAZWO'
        b'cFIKx/EEtKzDW+x6xwhnx/VdoZzAs/QaRbxE4eAou2wwwd7I3tuSSqzquzHBZmjTs1uMkOE5WOqJ5VHhS/GMt4SzxE4J7MMrUM7un/AQVGABnSEMyyKioRwrfEP9YTeW'
        b'Szk3RxnW4FV383jS0AeqoWpAuxjcjyW+0Ul4Uc5N9JTPUiezzXyKNRwZ1KoWLovXW9FRPKeCLjnU5uBVxiXdVNgzaGZ6eRU1Hvfx3MREeQhU4nkx/eaAGi5njfP0wXIy'
        b'ok94FJZ4qRTcKDwmg3Ow08ga4fFJ0OwJ5XBDbBYWhftoq+HOMj8owV2MCDy3CM49IT+sx529ApyEx9hRpx3U4WV1Ilz0pzdTR7gUvAS1YkrXuWmmJwUWD9egBSrT2NVZ'
        b'RBScVGd4+8vZKXi66wLxvLUB6rEUD1rQFMDqOZwf7IOL7NzXC45N7pWv27LH0p0TwIQbhC8YROFCg9dj2eJVrBUPqKtxDzar4SoUDc1ScHwkB81kngbxYPi8dKHadhYB'
        b'O7vGy4AGLQMdlKzEvb2YgGY41Q8KIuEuttwQ3AtNanUOdGRJOT6CIyLsXMk0YwkUTVKrN+F1bJFz/HIO2rWjxFvGTqjcoFbzc42kRwwHV4x4iBGIdVAFu9RqwoIKvEo6'
        b'xXHQATdgF2MXFESGq1Od1PTm7SyXsWwNG2whVBIuuuBhNWXjOU4ficeZttZGDOci0zZQbR2tUOo5RqcBr+ERgYywaCxe4hZhG9xkjedLHDhLbh7HZSV67bTz51RS8Xbu'
        b'mgd00ju3cl8sdyJ84An5NRI4ND+PKUzati0RPt4e4dgWT88Tm2WcfZxUj7ugTLxyasKLUB/B8vlkMn6IF5zC4tmiLjVhAe55QpfwOJ7sV6Yx8WY30jA30OlpTVqhFhVJ'
        b'NsY8mfGgwXdgo8XY8aQeYbUns0oxi62eVqM1G0QtwgYsEOHQPdJPjTdt1OJtbzruz2BsOrDdnnPynUWQmWhT4RNMb2jooMTadGBNkhAR5h3tQ1TJve9wdBQUyaA+fzaT'
        b'rh4uEFjS1E5vJVwOk3FDLCSwfwgeFmHfutW3n1PZSXAKyuCCeFVfBY0b+4QQu6FfBrwtG9YuB654hntHeFM4e0TT7Gr7NKl2+SSWpQ1HsWw0lCUPvjcnnKG3tKMiZWTw'
        b'yu3MGsEV6CTW7an7dWJaitx5dr9OlPcEEwoU4pnJT+o2McWFRLnPw05RwgXxeFNUV9hPrboZ2vqaeyTLodELSsRrpVbYGSDmIniEhvVlIjSNYEZkYuis/iv7/vv6DDiL'
        b'ZVu3MO4szbfovzb3fmwUjMQIUe7k5wb3WvxG6HhsFXInsNogeAFv9N0+s5vnIns4BtVrGEeUdjP62D4JLnsSy1jhi/si6bF7BGWzPxxRhAUYmKZEEuFeJSSEeoVDA3TG'
        b'eCs46wgJnoSuZLZMT2zT9F6QE1Pcd0duj3UTxSutVjyS1XfpLhvLYyt0w9llUM2up6xdPcWEC1fo6M25sFfgJSaK1YTttVBqFxXzdFqIK+5ncJ6RtLgfWs4biBKWT2KL'
        b'WofljiIgoQvq+hBJbOY1FgbkwolwaxIExBJPfoaL3QDdorwuu+F5hrhAj8d4W7hMPHK+CcUTrIfCOZrxiw0kIiCfvaLZq8VGGzGnFg/hcc57PhxgbwfAdWiE7j5WZ8OJ'
        b'fojDCTjPFI8mI92nCcSJiV5zhig4hrAl2Bw960nIDoT2ZNzHFmUktZ14cFIgHrGgF+hcAnEGB5hfVQbCsYEgzQ0YhFEsIt6QXYzUQRs2QRsU4xk/KU315DJHQ4V5Da1r'
        b'w0o4JhAcYXnYsqVw1S92ORazDH0fb3cs9vXoTV+IpdIv9oIj2B0XSsXFELEs1IvWEpMRsXIplss4uL1tKJSHwxUm4DXj4SKUWo5+hnyxBS+KxqOegzPQFuCwgHq2ZdQJ'
        b'nYoXTfCRpdGkAq9gVxbPvFBzLO41T2U+b14uHoTiMDyAh7EaijeTRznsy0+Cy4HQLIerSctNSXBtGk9Eo1gT46QS8xagI9uCIN13uj/TJ0WCxGP0GqYESwi0jjOHYEEk'
        b'PMAhtPmw+vnDZ/VJORGvPZbyHmwXzUqVNezdoH528BLvw9pgHZ6HPZ7DofMZsUuhhuF9Cpwerg50Cswm/jWcuvmzQ5kHHQdXg9RrxgQoWKSiXZnLcJkfjgfVAdgcs5kw'
        b'KISDBuve5BmCqwMEmW0BozyxhWPe+OpoMWE338WBlHvBbcJIfjEJGaCGuA56cxM+Oomgodsay0lwsZ+AACtiscUWWgOmLg3tg8hy77jlT0qdIPCUFQkBD0qZ8nlAUTQ0'
        b'kpVuH4Vd3HaCLlH5qsmgB6ExEE4L0CrhJC4cXhoHxYw+x/FjoJGEAfkSLZePZbDP7EPJOBODBwT6MoHvcnd6f7d/ArHpZRGrBk2/ytsCDuEhS/NMOkspVE63jo7Ccu+4'
        b'XiRjyarQ8JWhK0RaoGEpFkd5+0TDXiEyRs4R69diBXussEr0n7W40yAmw8fhQRIPd4mZMi7Ew18jyz+/DS6TSjzKEf52WKkkYp5fvVuUGE4chfYB8FmfzswEnpj/OBjB'
        b'Kqh9DKALhAF0/OFZnjQFocOWZgFe54kpPxGwHurN7qRu8mis6eudtOQ51jwLGnrTdmiStIAdWfYKMlQJP23kZHmYuMpDeGqdaOlXB/fbeeyGShYLbIayqCgoek4oANe2'
        b'sYQ4QjGbZk8KXCch6TDc1ReSLsAmhkpXDbaooXZRf0iqgrMqBaty9MUCtdrd3BdwEgtbztjuuRU61epF8f0BZ5i1aHkPxWKjWg0nRvZFnEGzGYzDg8NItHlG0R9sktBN'
        b'jICWuGCTGmss+qJNI95k5fH2gfQlm5K+aHMMXCa0ODPlb59OBjsAV/oD4VpOtJ3VgXCLVNU9XhgBe01vv2Coj1WrOTzctzbcCa2shkRJ+Wp1Boki+5YXDpWkF4X6Frgw'
        b'j8WxxEWUcos0oWx1QXgp1xqq1vY7n5wtLLPmgI+cM20cRne5+o+t1lD2s4XdwCJiXIl5vDy3z3AOg3PivjZnKKlYCfV9ZhN2h6hk4rsIxK23qwOnY3GfgZmewXQ2YnKe'
        b'OjCgz7xAKfExtDhgAZSrAzZG99mX6EjR558h87eRSUiEf6HfwOBOhYpnqk43HM20ehc29pkZJJ6YLJ7p2KWhBFtMx/BmAufjhEdZNxuynz6KB2cQl96vY2RPVskY4bVI'
        b'xqWoxO3+966BnO7LS+/yAr2H/vCC2bwivnT0Iqc55k8/e23ywUl/Tkn6zdSS2tdf+mzf2XOKMtfpx75xHGc1ytIYmuiquLDqsPOlEH1h3K6v7e9ZDHXL+2Kq/dYvNF8O'
        b'/yjshyE/7pz13duf/t78YuH5W93fXXp4PPbB9gsZ6vp9+X7XXxl2cNWWaZ6Ztenf/65n3dnJN1v/tGnMjPjG8CNX3ul5N3zrZ49WrCx8q2Vs1fQ3DM1vvpw47Vj4tPM/'
        b'WN9r0cR/avvhBLfv/+2l0c43f3i/4asLwcK+D4euDD9wrsEcvhS+/ulBYPbVX3/bEjzTdpRK/+im7EHbkIJRO199cfb9kxH7bvzw8qQv3mv8zd67J38s/GJ9za+8DqlD'
        b'yk/+s1zduOi9i19Vtkg1P8m2Lbp3KuPRx+N+/W2u09nlE/6YvKc54IviooLLwxJfP7fT86WXc8rey4p6Y4cqzq3onel31jsbIm4Mu39S/u3qMy/+0/29YfddXvQuUP8p'
        b'7w8nq4vj7syZ9GiZYbbH2JyxblUNu2dY2899QfhN0bGyJQHlHqu9Ksxx+py27G3HxnndrI6JLi6asyA6ds6ebw6P/N5mqvYXL346f/c2xYzXIcjKZdW7gd81Tntr3ti/'
        b'dc5a/dE34/92sfjVb7dnGjq371j1+49/O8Hlgw/mWJ+/ffsv72y+++YfPp7nmzfj7cyvu7qjz9x8P/hh65l/7opZeln+TuN8fdrk5b4bDn9fvz3u41cvX9e99uC0tXRs'
        b'z5dFfieH54WU/CrRNSDoe+mM28oZCYLru9NDPKd9+dc3vMZFfNCwee6Owm/lM478otP1wZzF9VH/iH//2OQf/Ld8bv/Ob8ecPF/sbDW88Md5Xbz37pJ/1J/2zK//9Zul'
        b'f/zH8Lfu/LJ7Y4I8ePfbMf/24/vvDrkfI//LG4riz6OGzxQicr58acO54SuTp/9u//HTEzaNzA388LrHJP3dzOtemx3vTlq9Ne0ve+8MxxHBtVderPBe5fb71m0/ld33'
        b'bYIHr+8+fHNd3t7wC1VR7y/UqpadWVDwTsFfd64Z3nHsW9je80AYYf7dq/ktL8Q/aHp4z7blnbi/T3//xocV24X3bN8busL1g9NVQ3Vflc7p3O/T9vU38w/gZNXWhz/u'
        b'OLDnXvfpoz/+sHNt3YOZ9XdevjXT1XmNIvWjCMe/Wj2s/GrbvzeU/jAnKP73w/4sNV068cHulw/WrF9sd/b1Yz9o7hw8fefVoWeNf5vmHzDuo7DSm2e/svvt2n/eq3zl'
        b'H39P/P3Hye6zP3rw5wk/VpvKr8b/JFlxUvvVy+4qOxM9jPGDerzimb3Ih2XrEJWmPpm4leHQIQvFhjSWtjMNLkGBp4ePisQkrSSE5LghayTEnRRMN9GgKAIKiDuEW3DW'
        b'58mcIXgBDrO0oCnBuNeTTlJMJuxPC0paYKKOaGQo7hKzgmZ6RvTmBDktYvlInnA+oS9hqQnbHyctNXtAB2vhusqpNy9oQFIQ1NvjMWe4xOb2HaP1jI4iW6MCPe7nyPCd'
        b'khxik14wUTPPp2JnBHHFq3CvrzfHKXIkPjFeJnaCVLtuawQJBChBcK2XKHs/aZol1LB35EgEWGZNY1HcHdsfjOJFbGOzOkJHlKePCm6SXd4+wjIFNEnUtrCHvUQ5nZj+'
        b'Zk/2ct3seY9fr4NKOMiynbBlrhu2JcBtIg0SpWex+EnCOc+SSXXYrhr2r2Y1/ScfKtv/+jhPvRG4yTQjwI9lS3nRHKAd3GpLXtb7sWOZUfQj4yW8De8ood9seCuJhH/W'
        b'R8ywou1HSGiuFG05gmZWSaz4gR9xBDux13PGEj+WEjteySsk9D1FB36E1IG3Y3PI+LGkvxPNvpIoe7O26JuMZDaJjcSGrYDlbbGZyJ+ErpsmTY0n/1awTC62DtJLIbFi'
        b'eWBW/GjS34XUu5IRZYTaxyt3kIgZY/Qbfb2RUmC0J/yK7kvyktEz/AHJXf91Wal4o0OftNhcVVRKtIjbyX0x8cmXLKdBBdklE52bCMXsGMub7i+IJmZJyUa3feWgd1yp'
        b'qEPocDQW0dIfReDWSlL4tdIUifhKbI8Du4lgWVrGRUZjpvE7N/FugsHG2Jt0pU1RagxKLa33iVbJeiwTEuhlTkJCj1VCgvjrB+S7TUJCtlmj762xSEhIyUxOSBCx+PjB'
        b'6KRxXAVZHUvgs5Sw/fjYZWOt7fC6yXoIzXLzNrJ3oE/DC0T1fPGUQq7HUhW/WJdnfFUmjOLp2yQ9sys6ozHEaVHarOykKSkJx1v25n2QM3/eyxZLHW46LXFZXud0f+8u'
        b'RXztVMcdlRVaG8vyrwO+7WrM+eD7r3+/+PxGq9aF+9/+zO/7D78ufPvhkpz8aZ1lR6PTM+5O+PIvQvyu7Ur397SvfXf3odYprGt1/i+WTP00/MDsYQvt8r3U302c/NIf'
        b'4mI+KGw/nbf+7W+WLqur3tLwx7gH19yCqxsm5teeCy8Ptq1tT//1uNMRFWs+rkkrWHT4k7bXrBqbWt9QHNO3vm5361Hrm3zRr/M9ZvyxZlj0jGMfL18S8fm996427/F5'
        b'sO7euncCIt9qj3plckJ+mLf+dl1a04Wkb2ODL6x//zfeYwq1zTeiux4dztG4frtrlKIk0aFh9Uv+zsUWf5i7QzpvQ5zr5Q9VMpMjw0p1FNl3kthzwdwgDvcbtov2rYuH'
        b'qwNeNGcvmdel0ffMsdvbRG8AIrE039qD2FVq1vtbuUGbTMrjFSjAZuZ8THZ4SYDLodHe/Zsdu6lDsVIKLdRsE2gzhDv+NxpLBdtUPf/BjCDBqz5Tk5KQwCxgIFUNF2qR'
        b'AojVoTmdNNfTwdLBYpD9kvfaJqlTDGm5g8uz4Y3D+2BMVEdCsP3YEAz97yGPN47oVxq2jeb6MkQf+Qw0DdQZr1g0leze6XlYSUwklECFBWc3EquJOMasHanbb3tWLqSQ'
        b'ZpcW/GnM3al2u0Ic9r61IzXH1pRUv/f+mS4o3NV0YtKK2u2PLk/rerhnz6XAy2sffe6W0f19FfyUE7u6rjah/tMbDxsmef2y8IDK9PXxkTfur+vMnjLV/8uaol8s617f'
        b'9v7Jhw/cKvxH2K3xUlkwL072c92L2GvgMWyzbcHN8reGqxK86DKRAWgFHMiLiPEmgQ1tUoBXYrwl3FDsksIZLIBjrM06aMbrImH0kBTKGWGOULpKOtaVRAM0kBiHe7E+'
        b'IiwKq7f35S4vWs6cPbaE5EYM+PkROR63VkmwEq/NYEsMgl1QMej3SYqk7OdJsDqIKdGIZUGe4WQTGpE3i8MauIgv9MF67H9zIPCfxYzsZxVBZ9CZehWB7mg5W0tedIyW'
        b'Uq8dHP1wxpH9MFf2SPVaQ4+MZuv2yE3mLL22R0avpYkn1CWTJ8247JEKJmOPPGmrSSv0yGjSTo9UZzD1yNnvEPTIjRpDGumtM2SZTT3S5HRjjzTTmNKjSNXpTVryj02a'
        b'rB5pri6rR64RknW6Hmm6dgtpQoa30gk6g2CiaXo9iixzkl6X3GOhSU7WZpmEHhs2ob+YFtBjKwY6OiEzKNBvao+1kK5LNSUwn9VjazYkp2t0xI8laLck9wxJSBCIX8si'
        b'XkphNpgFbcpjRRbJHmukRsJIz0qN9JdXjNQoGukhj5FedhvpHYGR2lKjij7okbSR/tqDkd5JGak3M9IfPzHSAN5IddPoQR/0TM5IMW2kx1JGNX3Q37Iw0vsaI32T1Kik'
        b'D3alTdFrnEYf0+nDs98OUOkM6bcD/1g8wA6wuu8s+37oo8chIaH3e68B/M41dfBvGCkNmSYlrdOmRKssjdS+UNet0euJeWM4oCcOPVZECEaTQDMfehT6zGSNnvB/udlg'
        b'0m3SsrjBOKOPeU/4+h7LWWKEMIf+i0UiMgnRTxFrDk7UxPL/D7Wkj00='
    ))))
