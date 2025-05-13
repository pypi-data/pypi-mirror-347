
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
        b'eJzVfAlYVEe2cN3bt5umWQVExIVWo9I0m7QLgho0LuyrCq5N0wu0NN1wb7e44i4gICguuO8LoqxuuKFVSSaZybxJJpM/hskkJpm8mD2TaPbEV1UXFBTzz7z3vfe9J19f'
        b'mqo6VWevU3XO9QPw2D8J/sTgjzAJPwxgPsgF8xkDY2A3gvmsUXKYM0iOMLyXgTNKN4ClQBiwgDXKDNINzHrG6GRkNzAMMMgygPNGldOPRkVGZtzM2coCm8FhMSptJqU9'
        b'z6hMXW7Ps1mVM81Wu1GfpyzU6fN1ucZQhWJ2nlnoHmswmsxWo6A0Oax6u9lmFZR2Gx7KC0Zl15xGQcBgQqhCP6QH+kr8GYo/LoQEK36UglKmlC2VlHKl0lJZqVOpvNS5'
        b'VFHqUupa6lbqXupR6lnar9Sr1LvUp7R/qW/pgFK/0oGl/qWDSgeXDjENpYTLVw8tAxvA6oAVzquGbgCZYFXABsCAkqElARk9vhcD51yVJFnfk5sM/vTDH2+CDkc5mgFU'
        b'8mSLHH+PtkkAaYsxGlxfenYgcIzCf8AOVJ2GKlB5CjyINiemoTJUlaJCVXFzUkNkYPQMDnUsgCdVjGMQGVyh4YXYCXFJaCuqTEKVDFDEsbAZnUbn9cxjQvXqRmMu4QqD'
        b'+fL/4YrJq4t6pkyCqWcx9QylnqUUMyVsRo/vxUTk/xT1aSL1zgNlwBWAQO9R2YkzlAsAbdznT1mS9aMsO9FHoRUb782WA08AlrXrsoMv5XJi46XJHMC/5XtnZieOCUsD'
        b'9cCiwM3XJw7k7nmBmK+8lzN/9Xsr/8HcPGBxxh0TvPYwzU5rJ7nGZEe8zcf7RYvNP+Z+47HDY+JUt9Q7zK9ZS0q+Ap3AEYI7Rs2bjKVQgdl/JSwtMBBtCYsNQVtg/ezA'
        b'+CRUHRwaFxKfxACrh/PkObDsCWY7dVMdSZhNGA1MkofsZP7z7Hw48UN2uojsFOzuYDAAfuGmV5Pel6pEIuw+lIZKdQKqROWJabFxwXFzQERCRn+4YzasgDtBLqwfLHVC'
        b'h+DFmY7+GGI6PISVCp5CHfASXgLWg6JIP9qzGF5E6zQmtBGeJx0HQH4kbHT44J5E2ALXa1Lg5QiikruAfgiscxB1g+fjUEtRIaqVAhAKQmPgToqq7xQFwHDycNm4lOeM'
        b'k0R5ahZ7gWfw73DrKuFyhBaY476KlAg63LJfmfdp9t3sJaZE3Sum0PdVuljdJ9le+jyTJeez7Hjdv5lUXvE6lWey7pzxNHPGO/euIV63AGzXx+psxu3clhPNp8KnzatU'
        b'DVbOjfpm2ovJJ91n1rTfct1vBjPv//H1/k3e76lYO3EZQ1At2uuCOaVKcoQEYVmvHRjGgv6wlJPDY/Pt/oSgstHoDGboFlSNKrGmWuC6iQxsmQmvqJhONlClkvBELj0e'
        b'LNEx30km3rbCaFWaRJ8XKhSbTfYpnQrq0LQGnd1IxgnYHIDrcFfGk5EzgfjDy7qnUEk6pUt1Foex00mr5R1WrbbTRavVW4w6q6NQq31iXRXDE03hpeRBZhlB5ifC8nxX'
        b'xrKMjCFPjpH9Sp4OQj5qXJykjg0OSoZVKegAOoVVRQp80TpuIGxD9TP1bA9N5PpQcexTHqo4Sz2GBKs4S1VcQtWaLZFk9PiOVdz0uIp3T95bxWXJVAPReVQBb6BabAch'
        b'aDfaD0LyULWDDIXHwjlUiw0vDB0pAWFwO7witjclwXWi+o2F20FoCDxmHjrzLYkQijtf8S37NHv+zRpYB8/X1NfWb/i7oaVs9Kb2DXH7mZdMROFcTXcsDNj1onzshd0q'
        b'xk48LipLe04N96HL8SGoLC4xWQpcYAuLDgSjPV2C6ksDqBw6XURxmyw2nZ3Km+i9axCHJY1lrXgoa47KrlNqMOaY7TwZxBNXpWJ7yJflyQ7XQ8gEXP1QyG/2IeRhhCGb'
        b'Rg3qEjLcj2pT6EYTzIBBBRzchqrQNWqLibx35m0mjwOpNwtu8+GpDl/cOBrVwLOCfXw4x2LWszkAnUxHJ+j4WzE+aR+yhRwIv1lQ57ZrDB0vUcAdZDgDdxYD1ghQPSqD'
        b'x+n4nzlfnQ+zjAOFNwuylhweK0q3dVIsGS+Be0MBmwtQAzqgpsNfSRg49SizFtN9c3Vd+j/iqNOxFUYI9gnhnFsSYK2AWCXcS0cfmjeI+YQp40DMzdW3Y37xcvhR1YFn'
        b'UQsBYOFatBWwNjL/CV8KMcE6eFgNW8MB5c3VWVk+VsdAArEF7YEdAjo/LpwxEAi4AaC2YHiJguwYFDCijK3jQDYGibAMootEeaGLFEAKb8A9GGIjWfekC4VYGz1M/S17'
        b'mAOeN1f7Lf9qJOXRGngUNgg8XmIx3E+ROpsHK+l4MztcW8KcJjJY7RfxQrZjAG7UzsV+vM0xJpzLRFfwAjsxSpNhIwVIV4ycWACaiRBW1624kSPS3Q4PuVMIFnbACgyy'
        b'C+MU4k0hmq2jRngxl4kYVtct2RNKl0DnYC0vCJpwLgs1AXYN9gvwOtpDAU7EB+qek9wkghDqVp99RlyiSWGjK0hgJazFK+wF6DKsk1IIb0Gdsot9CUPcEvyWvr6EUp2O'
        b'mrGyERCnaDcMsA+juSaVjldZg4e8L3mVCE+omz+7i4j96KoXahNcFSzcBtcBFl1gxsKaoaK454bmnwe3McQt4faCoBQRoiYIlrvwWFdRDdqLlzgJ0KX5cBOFsGrHOL3N'
        b'3CHiFm4X/byUkq2ADWtcUMu4cA7WoE14iUpGAk8sogAvekXYhrN3MQBeYmJWvMinWljj5KKIwPp9EG3EALsY55F4QyQEorUjeRd0EYsJNQzAXZsYphi10i4XeCVUQG3F'
        b'7iy8DnDXEUaNKrV0RngYbUftgrMbamaMsB13djDjBVdKEKyHlWEuRQ50EcBqWI37WpiRcuzlqOVsUMMNggtvZzIluKeOGQp3jqE9c2fBM4IdXXJh4OEI3FXFqH18qGeU'
        b'DXlGcHdTsFhBSoFEykye6U7bNej6StzhziQWA4kzE+OHDoskXQqy4vYiLgoexxNdZkIxny5RkHHpsS5uhbCSy54HJCOYGB08Q0GUcD2qI8otRU39AFtIVGuviuI1JxJt'
        b'wrY+VhaFDgLWhH3DNHRKJPQq2gw3E/2TwlOwSTS7ViOgNomdVhlcK6AW1OaBWeeNEWlkxvrDaso/P7Q3SkAXSd9wVIr7zjAatCtZ5UGF+CE3bpg7+xWxWMHPKzCDNv4h'
        b'bcIiK/s9brwlZC1syBM1qmRiv9MMkGJLFW6PfSWANh7JjjYmsnLciEcm7LPSxg3uk7wdjKcU26jg53RU1JZc+ZSQfYwfbrwl1LlFDqSNN91jBpxhlFJsnEKW17+pxDgo'
        b'ddqiGEkgbsR6NXLsAtr4/ZDpGfNAuBQbpZAV3TiKNqpts+YcZSNxI15d5TDQRhePOKdn2Rjs/W/mZw38sIA2tpoScyGTKsUGlF83vGocbTy3IMUlEmThxlv5WXkXsmnj'
        b'AG2qejfIlmIzyPcT/Itp4ztshsYhycONt/LrApdNp64WbeNhs+CicGd08CiQuDIxy/Ko5AsXwR0uvLsbC7cPB5J+zOTZI0Qln5OO2tClYkECjxCXgBVZHZgtWmYlrEA1'
        b'2AKwo2T6L8R9O5jhcFu4iqPrb5n84iCpJNIJE1p8e1FjLm28I7w0rpONwXvdTZtf/5/9aOOkuX9YcJqJxY23bH5rBk6ijWzyH53nsqlOmHpb3ZJFgU+Py8nplh4MyQEI'
        b'mKT/4lEn7/HAhawueyJwGZXsCMDfmcilsCIFn9GqUXlcUigqx3Glb3Yc2s2NhkfQVor6twKOJwtb8BzZlmNKkxgUDx7gDDxjL0hBdnbi2xNY4PCnpohaJAlhCWhrShze'
        b'925IgRxtZJfnonbKYZ5HTbANnidhOhMH98wDeOvbBduojcyYBA+qA4egbTjALQvD0YtrrsQjfw0VM9wFN+ODQBvGHqN6JApERUTwhGkUlVVj8DqpmZi12ZYhhdPFRmm+'
        b'E3CdjuMiZXbiR0M8ANUKVKmHWzXhZMbtqMMD6Hy8HcMJF+DZJQk0dK4mx9WU0QmwOiwOngtkgNIudUeHIumhAW11N2vGEugdkbAK5Azxp+Hp7Dx0So2PYfSciyrC4jjg'
        b'bcKBL1aoy6iFLrxKheo14hlkEPYrerg7W/RdjegoLNXAVnJuOYS3kGpgCclykJPp4LQMjYZAHLSjoyB3xSjKCZ9J6KJGg0WB1bccHgZLsrCLIbhxJQGa8WR4XSo6AQws'
        b'PCeGzk34LNWREE8QgwdQQzIRjRS4F0oiYZNEtKHT0YM04wkCe1D5PGCEF+E6eoSfBjfC4wmJ8GwOhgpDVWoGuMzHfg2ecVaxlKwBsDlXMx5HhnAvvDEDmDTossjnG7Bq'
        b'gmY8QXOfBh/UcvvZqQJYirHAKxKmwybMKynghjI4ytiAFYAKuQ62B2nGY7uA++FJC8hDe5WOwWS2dQvgTnUcbBmGJYLKk+E5DrhOlnjAnWg7hcyZjvAyF+lGtQLeABa0'
        b'g6frCfDqs6gikcST8eRUJEE3GLhv6ixHMt2bUPV8ITEuLoncZDw8iAaGqoKSQlUhrAKeMMKT6CQ8HhgI633VKrgDHVf7wB2+/VGZBB0fAE+xAG7x8YSHJ6M6y/cPHjxo'
        b'no41MTFMhjUxsbPAAET+Hl0dq06GRyaHxHKAi2HgmSyNyoduNvBQfJjghq4m8A6yPR5kRqALK6himJfig26bO8RGJPZdZFTLx9P5ElJwvNrmVuwQO24waicf0YFtwurU'
        b'IrgjHC7zDoY6sAB4dildKnnBVKEIXYM1DgXugVcZpRqdF/e1CtgagneneaiiGJ2X0gBjmBuspXhMSUSHcUyAmlPReTeGbu4R854TdXd9Etzm4u6b6QKrWSCZzyzAcdwB'
        b'cdtvQaXosmCP81cUc3i168zgqXkijkeK0CXBDhtQs6KYrLWOUaJr6Bh1Ac+h5jGozZ4VzaPzmDR4gxkEW1AZBbThCKRWQK12GbFWeBIeBNhYD4eKfDyKThW7yGHjHDd8'
        b'2JBMYGLhVSeKJGxxHY7jObgOni5yJfjvZUYn+YlKerxwtYv7ZHjaFR9hJNFM3HM6CpKJ2jPwTm1C1bw7psudmYCdz0GR5KbB3rgLtgeiVjfcN5yZuhCrPA261qIj8KhQ'
        b'tArtoAvBi8zQAriPoieDm1WCYuVqUWDbMcW7YbnIqL3hGhcFujSYdEm8mHC4FTWL58Nz6Cw2llpiQ5snBIPgRcuoi4Un0A10DFZ4KIqWMnjmBg4HGrCKhQ2iETWvhAdd'
        b'3KOFbqIyUbP512/GsUI1NqzGsLuLtrcnPx/juvnzPXHsHy4svLrxJ8/+bkOkRxYMK5gx1eXApphtMYaReZOOxpTtWDDstefOjJT2dwsZOUnuccv7zp7EdRfLP/hTx5qV'
        b'o1RJHpuXlVjWrQuXVoQOZUbU+8RuK9ke+Irh1z3TpONcl6oUr3z8gWtjx7T+qvqWSNdf9t78LuHblJ+S9TtzzqadHGbeEzTvxLw3Yj9IKm24d+fnF5b4eixZbvr79f6f'
        b'7HVL+vuZy9khjbUD3z4o3+PFf/CyXalZPvvtBMtHkctqItU/tD3fPnjk76e0tn3//8qqShYP3vyOblhksGL5/ePesd+5b5nw8u6ZKzLSSnZsuX8s+mM+tUn+y71fGtyK'
        b'JmStioYvbkvP7Heu5eO1Qs4LJ13OXv2isqTj/VPl54eue/vEFOD2jtnwk/q7TeMjDicN6nf7cv0fQr54a2Nt0Mlz/n86P25ueZt/zmumzw9tPhadx39U8+P127e//3a3'
        b'/r38dS+WlHj9+4MrmpOp67/8W9iRl395d/iSTt8qhf+9vSUZ9V6d9UVlG0rKR0yObiy94/Ni2ANQbdt35dVtKrmdXBBPgu0MqghGF+H5ZOyBUDU+9brABuxp5aiOXu6Y'
        b'9EXq0LjgIFUo7kTlOKBUwjMR3GKryk6NqjFzKb36uT696/aHXP0EOGjnvDWwQR2KPVw5nhZttcvgVjZkJKq2k7A1CF5C2xKCA2NRVcI4tJEBcrzucrTf1U59hrN7QlxS'
        b'UJITjn0DZRwrR+vRUbsS94zAvrCKnNbxrKgcO85qCfDGtloVLUH74P4AO9XFdWgvOpKQEoLNoQCdXcpMXZSmkj9+CfG0h0r69P5HFxde4sWFnddZBZ14HU/vL5bhh2Ka'
        b'nJExPowrI2cVjDvjg58KiZzxYuS4DbcyCvrxpD/df8npd3e2629W5sQysgeu+G9fxpOVsxzDycg9mC+eQUbnZ9e6M76sO24j37kLvCt4dDfm2hO1HjcmT6dOxfBu3fTR'
        b'qZ4DXXcnPh193J2oCKcvwevdlydhKrzVqZMTQ0W5qGVgFjzrVOgKdxShdhVDvcRCDp5PiAuO4+AFZ4BjMbhvmPWJgNStO2ZMBDQgJTfy4Mk7eZPbwwCV/acCVJNKcr8A'
        b'T65Q9viXSsQoKHW9Uyg0L7O80KhMmj1xbLjSxtMvEaG9QHv9EWdX8ka7g7eSuSxmwU6myNFZ85U6vd7msNqVgl1nNxYYrXZBWZxn1ucpdbwRwxTyRgE3Gg29ptMJSofg'
        b'0FmUBjOVoI43G4VQ5VSLYFPqLBZlxozUqUqT2WgxCHQe4zIsbj2ehYyx9JqK3pGKo/Q261Ijj0eRzJHDatbbDEaMF2+25gq/QdvUR1gsV+Zh1EjKymSzWGzFGJJM4NBj'
        b'0o1RT58iBPPQYOS1vNFk5I1WvTGqa11l4FSHCeOeKwhdfStUj0E+CYPlkZ2dbLMas7OVgdOMKxy5TwUmIiBkPlpvGm6xGM32Fbo8y+Oju2T1aHCCzWq3WR0FBUb+8bG4'
        b'NcfI96RDIIj0PThHZ9FhCrS2QqM1irITA1hNOsx4QWcx2HqP70KmQMRlulFvLsCqgCkljOprqN7BEw4tf4RNJjqexzusfY4ml+tR9InndOjz8DAB/+UoeBrWeotNMHaj'
        b'PcNq+D+Aco7Nlm80dOHcS1/mYnuwG62UBmWuMQfPZv/fTYvVZv8nSFlq43Oxf+Hz/5dSIzgKtHreaDDbhb5oySB2o5zlsAv6PN5swmQpw0Svq7RZLcv/R2nqcgJmK7VS'
        b'4iiUXaQZrX2RRbMSv0HVNKNFJ9gp+P8NonrGDlEPt7Oee9FDf1doE+yPT9ClGUZBz5sLCcjTPDeRtdGc8xSMyc5l13UrVybeufBSFstTNKxr0Ufq2Hutp6vmv8x33oh3'
        b'UWx0UUrsZfDIdHRNn58jLtDXeOKLMPHafGMPUXUjhFlgQdcEwWj5LVA73uCfwsSueciIvpF9YsdNcFgNRmvfO2bXsniP7GOv7r0wHvNbc+Qu7b3vziLSRsdNdgF7KhMO'
        b'Ykh3X4CFPBYA9nm6vtdN7eo2WkOS+dCnYd9r7Sfw7nv/71KEx2KAXsBPjQdEWDNeum/AuGlTk5+udlobb841W4lKPelDUrr6cqhCYgNWzuSNBYbip9p6z5n/CYUWh/+L'
        b'ziRPh3ebPl3eLGMOuobNug+f8D+AGDEDamfEz/XCazbu+W1js+oKjI+8XVdcrAxMxs196qmDL6Rx0RMQc418sdFqIGa5otioz+8LWjAW6qJ6BtZ4gh5RfR8QC6zWRVHK'
        b'OdZ8q63Y+ijqNvQ8B+gMBtxQbLbnkSDdzJMo1cib9Uqz4bci/Ch8mtUVELeJcZqd91hBWW/AqK5zThQ+F/S1M/Qe3SsjQE517uDxjECSWK0zNpbWOckbPbIt5/yGiLfp'
        b'fwqiJU3K9xKzE31GacTb9HmwFF2FbSzchjYDEI1/GDrY30jLp7IS1NmWP44WxFtQuBltDtHA9bCsuxQnZBzN+6MGeCNS/cShdViAFLXDK/5zh6tcHaREBNbCs4moImy0'
        b'V3xcCNwSFp+UEBKPqhKSpWAMqpKpzbDKMYReTZTBg+p4VIoqHo3wggclsHmBE71CC185QbwQFy/DYX0YvQ9Phy1d6XXf6ITER1feKnrpbUD7KPBE1IwOoAo1qkqKj0gO'
        b'YYEctbNwC7ziJmLZjs/i+8n0cagyAR/HUXVYLKqSgAAvzm8sqkMnVjpG0kvGo7CqxzCSgiknWQ+0A114Ri2dhI6hDbTqLgN1wC29RtI8RXISA1RzQ+E1KdzrjfbTxTHz'
        b'tqf0WptkI/BA1BD8TLY0ZjC8JJZanIQNA9ShqArPFhqfhMqDJxerZGAQ2sfBY/AoOkhTQ4FYMufVWGJt4si4JLQlGA8b0J8LR61mcaaOUehAn8JzcvVH69Ep8S7zYCpq'
        b'0fjbI0iSYTcwpKIOKiq4G5UZ1PGR8Y8LCp1BTWKZ1g10fbzGuCpCSlIJIC91Bc2NZBnQWlTrlJyEhQnC0Y4RNE8wB11Am3tJtgkdoaJNXSVePl8ImNNTsqyKSHaWVsVS'
        b'FbXOmqWBrYUywCRi1JbDxslos3i9XD1slAZueg62UmJAPtwG11JtYNWGLl2YBC89VAa0B25VyeicU3PQDo2mUAKYBOCDVeMcrE6hV8mrhsODGg1qlgImHZgxxHks+VNi'
        b'wqAJVbpqNDwGSgFjpmIqNmbTDot1BgZpxSBzAWrMhxfRvtniVXaDEt7QxOs0JHlyFOSja6toeyCqm6pBx9M0hH3HgAVuE2sZpq4cAIJxd+Hw7Em3HROBwwOQKpqjowXG'
        b'mAfADDBjipjdjZ7Qj9StZk9flu06QJEPVBKaGcpDJyaQdEkVZuQweB3zUo7qWLgTnp0p5gGPoA5DQmhIEJEqbOQWhgOPuRLLRLhR5GeHxj2BFnFx6NRsjoGH4uEVLAR6'
        b'Yb8e1Yzt5hjcDnfAcwPQOiq+RdiyNz3kGTyB1sPzuKmpS6f7z+rb7FCTBNVJcvH8NId3IHFCN2+dXGCTIl9cdgu6EPiQucNhDbwIq70dpOwP3YDXUXlftrqokFrqPlRO'
        b'ub0a2/R5jW9utxQM6JhjNG6PQufR7qdYMGo0UhNGZ/xF9HaoF2m8c7sFlg030wQlXJ/5TF+GPQ+1EMNe2ZV3W4V1pUyjjNbQdCLIg+cYCo6uwVNsQlxIcig24UBipqT+'
        b'sVoCBsFSjmQUYqjnM6PjqJzkwVQh4ehAHAecnVi4Fa6bS3UhYLYHKePMS4/MDj4fNFF06za9o0uSMnSDSHIpPE1VYPbw4d0aokfHH2rIfEwQ1ZCD8FyYOj4kISQoGVUy'
        b'mIcngEeuxDg6hLIMu4CrcE+PlGwCJByDa9Fhkv0blMhh1SiVUeKUi9CR3iMfpW4HxLqj/aOpc/RBV2B1VyJ0a8/dI8jfRS+FDdnwsphgWYuu5Ik5bNiaFdeVwkan4QZR'
        b'zy6gFnhWHTgNneyd8SX5XrQBnqKT5KI2iHeJxK6sYyM8STOPAtpG72t16DqqxezJnEYZpIblWF/RlkRye59AaqUj4G5ZHGrNoWIZuhQ2YHRig+NTQmTAxRXtS2Ax/yqG'
        b'UFtEp9FWeFQd1yM3urCQZEevGbC1ktTUpGiMa0WCmHJ1RkdI1hU1TBc3uzJ/T3Xgw5T7AFiRi0E3wRpKrPFZdB5WoFPo2BMlAtxozKhyhydRDLhruQsL12MnkgEyvAO7'
        b'Le38CHRBYNApN+pRvOABqjHLxqF2l2EDSeknqieZ/Qa4hTr1RB3agGoxbjEAhICQ4SaxmMJVrLAOtGQHRxvkQLTWc2ZUgWpR6zK024n4Z6CFWxdRE5gP98PjsM20JlyC'
        b'O04DmzLQkUmwOYvWoWoBywRVxaWlwtbwjHRUhmWXFhgaEojJD+rKA2cQ+ygLnhtLKKZsTYsNJj3YahLmpKIqDiyBp2DHyn6wio+maV/fIhodxc6fnm3Rsl6Abp9Z+Qsw'
        b'65pQQx+smwA3dru7UlheCNvGkl0nDcQR9UbncsWM4k60z4d0McTdLUZNsBHHD5sdtCigerIXqoVlcWgb2oV2wLKl+FGFw5Bz42GjFLbmpNtz4IVxDBa6LAJdmwfrx4uF'
        b'XNtRPTz7cNLYEjxnJdzWpSiZ43BEdwXvod07pEzLBvFR1PmOQtszenh0YRH16PYBVN0noENp3dbulP3Q2JejXeKq27JxBNFNJDqlwERuRYccStK38bnEXqEIasx5GItE'
        b'w1oxUDg0V6JGbeP7CEQ6YlUc3VSGP4c3h/FF2LHHg2XYfzeibdiixSKhlWkadCxprIyGH0bYguMl0mEeguo0Y5diVsSAFLyn16OrU6hUYhSoBuOLmgHdai8A2Dob1asY'
        b'2qlejg2ubewY3DeTVMbVw4MCOu2YTvZVVObngqqwbm7FmoWqM1CzG2wZOyY1tkvv4lBZanrI3PTHNQr7pEMKtBfWwWpRLS4QBwIbZPAy3Ir9OliFXfPZroz2s2gTbBgP'
        b'W1jA+mJ9b0VnpgNqcTqA/Zh0GWwHoASUoO3wGi21h6czYatA6sbD0gNJzo54ycxe62eGOKHri7B7XuqIwhDxTp4uyUmoKmRul4mg8szY+CJ4fE7sbJEkWJ+KypJCQpMT'
        b'U6QAnkLNCrgJ4XikqzAE7YQbclCttHAgLa/HG2gr1SJ9Kv5ai7e7RngOb3FoD8DmXw0vYTBaRXcWHbb20LLZDNUyqRhVTB3t0q1kcN/Ah1qGSudTLUsPTSeVChdJmQLc'
        b'Z0SXmLHoOjxH13WCa+FxAV0s9JABdiHcgcqZUTjU3U+LiMyvKf/MCJvx1/4j1q+e/adqnxk+Jff1J6/mrjDl+hqGbDT+UA+HhwbJtx6+XHH3heneSUFmQ1zktea9caOS'
        b'wxrTGkKTyz5/OW7SHsu075jq/ZGFEdsKh29f9vWS9/c8uFmhvX7ww1nPnHy9qePHH69nNi1ePadddfp4wCv+y3O+VjSZPkyy7jIfDfvl84LFwvhM/YHPX7nQpv/wXNum'
        b'IGctWrH1WtHSX+6cdpvbpnpjeq5wc7PbX9Ob/LXfOALao96URf10u94yMmX/+yuqX4zfdgxGzZH5jPnlu3kjto7PaBq15Hs1//xLRW/NKEv5kfvC97Lssq3946Nuv79h'
        b'72ey7loyB43+3NuSMKkpYfamNTNnD3rnzY37+n0xq3BIYcdHY4I+jlj0+vXU2k/6/cn9XpbE9oE1+xt51jcX1/5uyyWb/7x3NWU3VAOLY19U3/n3m3/z/WLee3Nv3U/9'
        b'csh7SxXfDbv80c2/eVt3Fw64+fnQu+W/t65OnvSne7XvT45oen/TksXhKze9O3ppx21JjseWpOeHev107faA50/mLMjR+qzM+qxfS8WtxrRl39892X5k1d3fTaveMr/8'
        b'960vmPsv7Ty06cxo4fRLL1y7lPL2/ZfDZe9seNC/7Y732ZCpo7X+eYU/tYTFff/ttBf7X/S+/8Ly19JHfN8+86WXfjf+JX3mIn3+F/crGv/xakPa5zWzQqa8ELn67rgz'
        b'M39uvWf7LL38h4BD4UGv7Hjt1bPfhgRMdQp5c3Dpiu/uz3C+9kz+1h/WVu4+o9gSFVD6juuyvD9f+sfkZ65sgEc+j8xbuWzgTz9s+cs3pa/fniexTxhd8saeIXffLj7z'
        b'9UdvfnWw5nLs+7v6FfOS0WOOXZs3/eeoZZ/n8p+atvhdCLJPVi4I+sugV9PrPYWgwF0pKTt/2PzKz9V3G949pUt5dV/MX//xXeXfmzz+ejNXegr5Xbj+4Sf/tvC113/8'
        b'ZPEHlR/Ymw7tqv314v57x246H3JZtjrtq+j+Hu/WfMx9HWw712/ZDH7elLBvVn11b1/2p0MV32zqeOmXjz9YPvS+ovMvfLL9292z39jx1peSCaxpcvPrRZrKih3VHzQ0'
        b'RMPir2UN176IinxhaeWgL//c+mXJ6/yQN1+YgmQf3ovNf/bTYyl5t1vsF8a9pn1wNHDS8h9Pn0l9M7O6frp1W/20ml/+llR1oO5Dl/RPbXfXvFJa9Of7d1c2f+m8MuX2'
        b'iP7Riqi9uy88ePlLp7c9fr+v6cjQ3JTtR6bcmlVxxv4teBD0t9uv3kr76eWSJNd739xbsHvK0b+3rWHe/Gn9ntduqdzpSy8z7NjnH+fE0gXsq4i3wvHPAHiRix3qbye+'
        b'cGKQSR0UqkJbAoLwccZ5Hotj2XWL6dsQyeicQY1OTX2sbIJb/KycVj48i8oWw0N4h+8ujaB1EenwJJ24CJUtF8sicvondFVFaHW0WgNen4ej1YrgR6UaaIsPrdZYhXbR'
        b'4oj+sBFuV8ei7UN710eQ2gh0AO6nJR2p8Ahap05OCo7H284NhJ28HLazxQBtsBNnttiELqEzJQk4KgzDPlxWzIbiI289Je3ZkJQE7B+7qcIRehvwCJfkwjo5RT4PboBl'
        b'k2J67eIlA+m0aFsADu4OWtWEacGkMuksq0nNtA+mhOGz11F1j7dHzogvkMBD6ZTyMbAMH+nbFqixIHBcVEh3FBb0n8RJnAapvP/Zwo7/5EPl9l+f54kXXgrsE8eG04IR'
        b'Kyl/WCPP4hjxR0HLP8gPx7CMKykaYTn8W8GwLMv09aO4J3d3pRD+DCkXId/9aOGJ7Be51JURW8QR3Fo8D5n5gSfL/spJ2F84jv2Zk7I/cU7sD5yc/Z5zZr/jFOy3nAt7'
        b'n3Nl73Fu7DecO/s158H+g/Nkv+L6sV9yXuwXrDdZW/6p+wAlI8Prcown48d4Stwxvq54hcF4tcEPfGh5iiereCDDvwlthCrZA4KfK0uw9cJYKqS4hyUUkg/HyvAIGStj'
        b'n8F/yboKZlwprAyPc6XfB+PVfHC/P6aTtMsesA8UHKb5VwXnSnnIrWW/VniSFUipjSuej87B8h7dIlFJOjly59mjPOa/LmwVw3t2i5sutZ2ImdgHWPfMl09502zRisDu'
        b'd5Ba8ZmtOoREbwD4F0pQ+5JFT7wPRnQmhkxLoi8jeRsZzGcNzHyJgc2gr9x2etIbXFrdws/geRv/Y4B4p0v1j+8qVjEalDqr0kj6Q5NVXKdcqyWX4Fptp0KrFV87xt9d'
        b'tdoih87S1eOk1Rpseq1WVOpHD0ovOU+Rgj96uysHcla8nLwQDVtc3NElu4szoTJE7uC7jDgMHZJJF6KrKmam+bu1DCfEYOiT1bMmv/q7ZBTjKbuzaPfzycIV5+tvgiPF'
        b'8nHnC9+76fJz68bhReBQzeXshLaZ7z8/LvOd2qLhR3ZO+fyVX13b1X/8Yvf9d1K3xsu8Wo91vPHB5PN778z/8o03StxGfFEf9Mrh3d+8sCY0zTf2CjtX80VR47GO8auc'
        b'o2sOfR137Xb68wntNzbPVn5gfWDd8cy+wUHLov780sa5xz9Y52VY6c8XTouOOCj9OvDnWJ+0nD+cbp5z+TOw5DPl5tu6yuZjfvrfjbmVnLPlwIuu0RUTlw51+Wz4rttR'
        b'u97qf7bV7WzLp7dvjrrYXDXksxyPnyJvDttaWOk9tqjTUWJ8pmizsPCOV+aiEX+O3f7iN7mqL/fkvbf3owlz0k7MnnHiB+mEd7dzh06p0J7BHRmjNyQGpe1ZGFax4O1N'
        b'c38eFDCt/wL2u7xStkDrcS9mJvt+2u13AjKXLzHeHa/i7PQgvGm5Csf/+JgRCbK80dbo0fYAGuzCytjulzrhcVTZ5U7JW51D4VU7kVgquuDlEoS9OCrH7vkSPsI7ugQW'
        b'ANs4fLrcH0+3nBVR6KIAz8UmY4WF1wO7t5x+qEYCm+FJARsDtQmv/0b/LKPB9NMf1O9izbbYdAatljrdEvxgfVl2LKMkjuIBcQ1y1pP1lLMy4hyf+BBn+fiHOM/HP8SZ'
        b'4o+ME12d/Afs46iTlv3kI2dTXJlABqxhV/ky/IAeTojF1vTIBfX772ETw/s9NFOyOPFItLov9LOnvf5aBttdYYVnOrkDQ+UpibAcVjsB94GSIZNRiznFsZoVjHjcF394'
        b'bsiLY9zXx3hufm2NqdjNnnNi850j1+DzSz4PPjHih9sLbiaNu/bJpk1nTKsvvPW72vLi/Bs/7oIPijOyju9998THlz+pH7lxm8p+b//Ay3cWtheNHhPxj2Vu244FL2p7'
        b'4+AnuwNe+MzvL+YNKicaLBTPxQfSCgWJnVJS6LWVEw4YWll0OnIljd7gGbQf7ktICUEtZEiKH+wIYbFCXpPAI8OGUwMY8OxYWIFO4rMipotcT2GvS+jykgxFa7EBEM6M'
        b'Wwg3JMQlzUYVpAyV1KDCZuy/SDhiRWfQhQRUClt6/CcDLioWH91rJtJAKQnuSBRWoP2P/ycEueiinZxS09DeMep4Kb1p3gPXobrJod2GMvS/OZr5z2oP95umZbaa7V2m'
        b'RRyP3E3RVegaLAFrwBpuDT/woborOyUWo7WTI/WVnVK7o9Bi7ORIIhHvxWY9fpIauU6JYOc7pTnL7UahkyNlFp0Ss9XeKaVvCndKeZ01F0ObrYUOe6dEn8d3Smy8oVNm'
        b'MlvsRvxHga6wU7LCXNgp1Ql6s7lTkmdchofg6RVmwWwV7KSwqlNW6MixmPWdTjq93lhoFzpd6YIRYiK3002M1cyCLXJ8+JhOFyHPbLJr6W7Z6eaw6vN0ZryDao3L9J3O'
        b'Wq2Ad9RCvD/KHFaHYDQ8MmiR7KE8eUuGH0MeweRBrpB5ctnJk8QkT26feaLAPLmo5UkCgCeXKDzJxfHEJ/Nh5EFieJ6oIR9EHuStbZ4oNR9IHuSOjifvGfEk2ceTd4Z4'
        b'JXkQ2+GJbvLjyGMCeagf+gMiHedufzDzhyf9AR3xo7z7Zf1OT62263uXW/3R39T7Py9RWm12JekzGpJVcp7YFAkddBYLdnZUG4gldCqwKHi7QDLWnTKLTa+zYCmkO6x2'
        b'c4GRxi38xG4WPhZrdMoniRHKFKYbcw5wMjlLNA6s8fFkadT7H2d9FNc='
    ))))
