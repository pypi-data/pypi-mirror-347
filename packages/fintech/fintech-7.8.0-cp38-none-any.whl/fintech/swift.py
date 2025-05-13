
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
        b'eJzVfAdcVFe6+Ll3CmVoIiL2iZVhqKKoiIodGJolajAGhpkBRoYZnDsDasQGOhQBK6KCYkMRUUSKFZPzJdn0ZFNdYrLZZLMvm7LJbnrb/M85d1Cw5L9v3++933vOj+tw'
        b'yne+/n3nnO/yIbrrn4T8xJIfIYY89CgNZaM0Ts/p+RKUxhskDVK95ChnHauXGmTFKFcuhK7kDXK9rJjbyhlcDHwxxyG9fAlyy1a5/GhwX7I8fsFSZZ5FbzcZlJYspS3H'
        b'oExdZ8uxmJULjGabQZejzNfqcrXZhlB396U5RqF3rN6QZTQbBGWW3ayzGS1mQWmzkKFWwaB0wjQIApkmhLrrRvRBX0l+RpIfBSVhNXk4kINz8A6JQ+qQOeQOF4erw83h'
        b'7lA4PByeDi+Ht8PHMcDh6xjo8HMMcvg7BjsCHEMcQx3DHMMdI7JGMsJdi0aWomJUNGq9+4aRxWg5OsYvQRtGFSMObRy5cdQKwiZCcI5Kkqzry0mO/AwgPwMpKlLGzSVI'
        b'5ZpsciXff14pQVLkKnNBGR6vWROQfSxpjMfnpkEFlKUkLoJSqEzBVdCigsr4h1ND5GjCfCncmDtcxdmHk6FT8XXcKMQn4Q4bVMGOJNjBIfd4HrfK4JiOu0uevr1YLKYM'
        b'4QhL/j8MyfJ1Es6VSgjhPCGcu004zwjnNvJOwrPuR/hD9xAeKxLeHOFS4I4CiKQyPGBYCGKNXhbJ2FAJ/ZZhGj9ogNj4cYybyYsjAs3ISPwmQy02dmtkUcD7EB3N8HDT'
        b'F6EmZHInzaErh0i/9kWxXw5cp22Y1hkx4qECzuRGOg6NPcC1uiBlA2eeeMsalZaBWHPU9K+893pzgQ0LvuH+uUK7Sol6kD2U4hyNjxIRVIQtCgyE8rC4ECjHTUsDE/B+'
        b'zySoDg6ND0lI4pDZ220GPgM193DapZfsSZTTlMsoS3Kbl9y/x8vbQG/zUiHycqqHFyLKEBAu/2ihpnAtsgeTxsnQtZJQsEOtgR1QlrgoLsoWHxz/MJqoWTII712KK/A+'
        b'lC1zgSPQvtE+iExYj7fi82rYEYm7yAK4Ca3BxwfZ/UkPNCuhE++AE5G4nXbVo1y8eQzrwrWwB+qG4huRE+lvNUgHx+GonWra6lm4FFcbYY+MyAWFQoeJIds1TYH8EHIN'
        b'l2cUfRk5WhTnFzEDEdX8cHNrWEv8SGSMnfRHiaAlLWOXC59mfJyxOitR+2JW6O5AbZz2kwxfXU6WKfOzjATty1mqxfFaVapG22I4zZ0ZmP2xPkG7Eu3WxWktht3S8pOt'
        b'p8LnPLJDNVy5LPqY9Ks5zyQ3ei3YeflJj7ohaGnioA+qMlW8jToKfCZ/jCs0Kgi3VEn2kCAidB4Nwg6pK67GjTaiqCgRHwwlHC0vgoNQDTuI4U7j8AUXVxXXwweqVBIr'
        b'lUufB08eP/rHZFkt6w1mZZbo50KFQmOWbWaPO3Ni6XqtzUDHCR5UyqM9OA/Oh3PlAjmrvBeEStIjK9Ca7IYel/R0q92cnt6jSE/XmQxasz0/Pf2edVWclWqKVUYfFMoY'
        b'Ct+Lwv+jDy/neM6dPe1DSctEXag6To6Cg5JxZQrRDxnyhy3SIXA9eYGO76N/0vsoNXEht5WaZw5CQpSav63UEqbU/EbJgzxjL+D+Si1PttOGaXAat8IeovghS/A2FIJr'
        b'1HbqRhfD8TmwhxhZGFwSUNjjcrsfVdGzC/FVUdWIqh5FobjJ3TjV5bpMoNYcu//tTzPeeSTtiZ24FrfvbNrTVHwhbvS2y8XxddyzWVS7PLLeN3Fo/xnX2GfbVZyNsgbq'
        b'p+Dd6gQ4NyUESuMTk2VIgS/wUB+b6BTL/eTNuN6jEIWbZbJobUy6VMdRkAcnJbK1ut+WrJRJqkemN2QabVY6yEq9korvI03eSmNYH5HS6erbIn27n0ipuwXHOGhQx4ki'
        b'JfpaOolEkmAODcuT4l14K5Qwhk2dWSDYosKliM9MCkPQSKLHNWbRieDAO2kXh3hDMuxB0AQOk30wtZFrUCejXRLEZw/GN4hjwFdgt+gjtsNVN8E2hUI04/YhCM7AwVyx'
        b'qxqOwUHaxyPeMiiPTIOSQtb12LxVArRPpmvhYnAsRnDRCw7bh9DFjlpwG+uUkc4SOIQ7EbRD9WRR3o7sCMHKJlrmhxPxe8AZhqMOTqyBi/YIigfeR5SGgMRb1HZqwHjb'
        b'ULjOOgkiuGYEdFCIh8eyidG4A9cLQiSduAnq3BCcw42EODoxGC7gzWwioRwfhANjEFyCbfFs4hhctoD1uZC+Q3BiGoLL8/BOkfRi3JUOFwUPd7IidMClddwk92SRgppE'
        b'D4WVSYBE8PUIutQbmB+2z5ytgAuTaQfswHtDOAmudmErwe4lixXuEynRUAP74BDnBnuhloGTzQlVQCcjG7YlxHIc7JzHUMiEq/igABcLvSgKR9f5cmrozhT5sYNwda/g'
        b'5gmtFOSNGXFcFL4E+xnAWaPHKdbYoRORngsrcSk3Lk0pakEL7MsVFFYbnVM7GPZyI/F5XMcgwq4BUwUbdCloXyWUQxWnxq14uzjxFFGgrYKXJ2GGRAbnoY2bAedc2Wr4'
        b'xDrYTrq8OCRx8xrKxcK5JYwb6o24hLSvoXRdWg2dHLHsZawHzsXhSoVnPt4hRZIxM/BpLnaVQaSrHI7jU1Q9iOrkD8AtCFpgG2xl01bARWgmSjxJjvis2FFEvXGHK+vh'
        b'8Q0bVQCqb8XTtAjaknCrqIvXoH6tABfgojdl4jl8DZ/kJuHtsxmHpy4qFKDT2XemAHdzkbhCplKyyKbKH8hN4lFgxmPP5d1UbRzGGr8dNYibyqOA1KAX8m4WfJ7OGle5'
        b'+HMxPJra6vZ23s0h12JZ45PZQ7hY6ivc3ipawWsXssZXfYZx83ikbJ1JGiW7clljj24EF8cjnwzh2aJafaiGNR6eNopL5FG4cjUuWrGiOII1NtiUXCqPXL9c/kpR7cYD'
        b'61ijv+8YbinB89X0V4sC1rw9X4T52DhuBcEzf/2zRQGe3EOsMTdpAvcowTPf+GrRTeUPCtZYpVZxGQTPV9NACCg6PIc1vrVUTaIDim1Y8bKwgnvKgzUeHBDC5RDkM7zf'
        b'EVasdphZI/9IKGfiUcbmpT1CwPwtMSKeWeFcPqGoddbLQu2CulWscbtuIkd8aiqa8qxw0yNvOGvUrp7MrSVkZgy5JdQu705ljYULo7gNPMrPT35LqHWdWMga/5gzldtM'
        b'aA9/+D1hxahOCWtcPyOaK+FRnI/p90KtUOLNGre6xHClhCGb1zwlBKyaK4rjlZCZ3A4e5Tzh9rywIu0nO2us3zib20m4tNP8mnAz7tAA1ngqcw63l0crdrq8IdxUx09n'
        b'jYMT5nG1hHXhE24KtVEdVtb4jWUhV8ejte+PekkImP1otCj3WfFcA+FnrPzt3Fr9FVFwE9clcacJ696fD7k30xIKWONrshTuLGHdE8ZbuTcXaf3E1Tekcq2EdeGBODdg'
        b'tXUgawyfs4Rrp6yTP5l7c9BLk5nS47P4QIKgcKeG57GAbB9i55JAwHoqklIVVi9PYqwDrLiO2Goj8TXMvmq4DGJFXYWChLoN4vQqObUeX2e2At1zYD/xN8R1UyewlziU'
        b'Ym403huukjIs5sX9jquToLUNUS8WrvAZlM0a1UXPcQ0kpvuMesGyItJzLWuEsOe5ExIUq1SA5aZ1pSiWqOyXuNMSoj4Fz1hqzWuND069pyIk7vnoBgdlyf4TW5nsuzMV'
        b'urIc3Z2pjE9mARfX4JNQgyvAYU4hYbQayuKTQqGM5I/+GdIJuHWBaEsZkkff4cW9TWdEspj3tmvc0n7mlXRv41Ey14JYToYvR0KlJkwDVSkkH3OFrXgvlPDrFuFDoo+9'
        b'SDKc3SMk+CJup/k49wgVYrVJ9FRdQ/ARdSDJX0vDSMbigTuGZ0u8Y+Cc6GUv4sNKfJEQEI3IpnJrNC6XWCnTROVWSufVIranMs1eESo2Hk1z4deL+zRTxqwCJLrePbhJ'
        b'G5kDzeEU6G6kJa69gvEiEM5P1hC/X00+ZD+qwdVhBe7xuCWQQ0qbzCtC15sRlE8nREINTSXxXhKkjsNZkZnFBHg7nM5Qk30X29CSTVi8FA1USUg0PAgVLDkcsADKI/Ph'
        b'bO+mA7c+IiLWiWtSIj2ScRvdpxxBJrwFH2a7kRBlbCRR1T2RdMZhlB2tZxwJhmtDIydCdaScZhxoNVwlKzBIHQTW/ki8E85G0Sm1SL9sIBOPYh2u1iRQvJJFCXnlS6Ap'
        b'YuqE4WJc74KdoyNx3cYoisIBZMAnNPZhpCONJqaaRDIpDCrVHFKQfCSNBBM4lK7iRbbsIDlvRySQZCeK2D4+iLLgUhxDJ2E9PhVJMpSdURTRQyib5SNUHRT4fDZUkG1L'
        b'kiwNDiDpSA4fg324mk2b7Ys7I0kOeCGKmAmuQzn4ML7BDg42kEyoUk0lA2XJuEWKPFbgqhkSb9wMl1i0Xoa7cEMk7oR6kniRyQ3IBK1wTNSyndCWCBWJhAuSCfgikkA3'
        b'hw9Ngi57KiVjP26DMiExHqpxR3wSPcO4vQsNDFUFJYWqQnh3fNJA8qtGfCIwEDf5q1VEyU+o/fBe/0FwYjA+xZMo7ueDG0Jgm+n7X3/9NSJUWrBa3PAn/hBBLMWP5WxV'
        b'q9TJIXHS9CAkjeXIVnzvepUfo3w6IeS84Gm1S+YlEzd0mBsjwB7GZR3eBQdInkm6jANJVyenwvV2NulxuOQHF+kkfHku6erm1OtiRHVoIplWm0AmcZEW6ta4UQlGp9AG'
        b'FQhr7O4cbppOEoernBLO4B1MUwYQz1BFUoNCaJfhZryVJnTcQ/gi7BLTucvz4BpJzKDdk4MSgeZZ3MS5j4r76g5cN13hpcDVPDTOQZI0bmUsbGeoDII2uCbY3AulC+iC'
        b'17nh+JRe9NjXoXMR7ZEpKM1bCCq75rIel5BguGizQrsEFZE53dywh4i7puozGjcG46PQKECbTY44YhrEOE9gh0h1DT5uUrh6uiN8cjGSTOHioEXD8BscB7uJAq7x4BZA'
        b'DVnrIDcB4U5x4+Y7Q+HlQfLnPXIkmc7F++ESMf07A2WpJEuyevGecBhJvLgpxMK7xIhSQXZvTaQT2jz5wb5IMpqbjRugk2GRh48rhDVkqdW4lSDfSfLNGwNE/A4vx+WC'
        b'O5FX5BSCxG7K+wKRFY1S3KKgPaPWI4kvFw7n8S7RPitWkZUIbigYzYLGYLJx6RT96tllsP/xCbjC231NAYekcI7DlQvxFnGlU3gzbmZ0TcDNjK7RmcYtn/zIC/uIaRkP'
        b'f7Jq94yUP8d6bP/8QDyvKNzwxe6P/vb9J8Zdr45+aF78wrkX3rk8e3acvmnnqeidixsX+Ll9MHjRl4rvPfe6Vkd6vvPi2pE3vuo5fMKanXrouWYXOR4es/2XgIDn/hy7'
        b'/bPjn+FbcW8PH5qjXZ8cr599pKrhmUOnahc+n/ZOdPAXx4vHpbpM+yU1/fVHdQEr95bHLQt6oemCKe3ED39LfjaucOq0v9c87VifUP/U9dOtn+UcDf9o2Mo1jw1/8vOK'
        b'nelzZu79uUrfFPd8yh/2K86u6dmTczJudbDDt0U+fpdt/LsVj1fcfDdNvUPv9YZxRnRe4PSH36o2pZ7Az8yJyh5uffiPD2///Nfwn8Lfu7n4saYXjlRtKxz07fCAq08E'
        b'vTP26/2rRm0dNaxAkjHddUnu+WMbvxj94/7N1y7MkCo+iYp84eHvC94Z0zDiiM/37S8cefLPr2XXTVZ93jm18711Y95rjPpowMpVIyZMPHS4eO65+gtf/fWlnfBi+q7G'
        b'tFmffvL22mHfhzvcv45a/mr9Nym+Mz6P3x+6ujVO8/bfxx//xf/UOTzkl42vDnz0iZ9hykPmk2Ou8ipXGz0SJu6wnnjZiuBk4oCgmuyEFY9PxM3E8wbDPhv1zGp8eQHZ'
        b'6NeHxgcHqULJEChDKEApfSwpn/UTd7cbO+jRDzv3GRslnvwQG71iY+5wG1S74tPp6lDi6srIAnJcxYeE41rWC3WzoUYTHBhHgjqHXD0TydrroAsfsjFF3Q1Xp8coNPFJ'
        b'QUkuSC7lXfHJDNtoOu8a3kI09RA+QDfzBC6UER9aLUEDp0tIawN2MADQhvdsIoHxkiYlhCRcBdxsGe5Qud59OPGgh0r24P47Bxq+4oGGzao1C1rxIJ6da6ylydEcd86V'
        b'k3N+nAfvynlwXjz5JqFtvpw7R0+0XDl39uPLyX+V0h/eh/zW+yHfeS/xO+/uIuf4X+W8B/nNn/ch8KRyKTsT8ydPOfkEEPj0uxdn9UB3Tsg8+qLW5yTlwdSpOKtnL30M'
        b'1FzUe6Zyw6/vmUoQaZkFNxKdRyphKhL11MmJoaI41HAS9snRQnzWBe9NwHUqTvQ/NXBcpYkPJpmLFA1KI9ExAp+9J1f17E0p4xDLVelhPLr3OD7L83buyv9m7iphp2zS'
        b'b/IIYHdln3+pVHyCUtv/0oTdxKzLNyiTlk6bFK60WNmXiaH9pvb7Jd6mtBpsdquZwjIZBRsFkak15yq1Op3FbrYpBZvWZsgzmG2CsjDHqMtRaq0GMiffahBIo0HfD5xW'
        b'UNoFu9ak1BuZ5LRWo0EIVc42CRal1mRSLpmfOluZZTSY9AKDY1hLxKwjUOgYUz9Q7IRUHKWzmAsMVjKK3hXZzUadRW8geFmN5mzhN2ibfQeLdcocghq9pMqymEyWQjKT'
        b'ArDrCOmG6AeDCCE81Bus6VZDlsFqMOsM0c51lYGz7VkE92xBcPatV9018945RB4ZGckWsyEjQxk4x7Denv3AyVQElMw7680hLSaD0bZem2O6e7RTVncGayxmm8Vsz8sz'
        b'WO8eS1ozDda+dAgUkfsPztSatISCdEu+wRzN2EkmmLO0hPGC1qS39B/vRCZPxGWeQWfMI6pAKKWMut9Qnd1KObTuDjbL4USO1W6+72h6tB7NngSmXZdDhgnkN3veg7DW'
        b'mSyCoRft+Wb9/wGUMy2WXIPeiXM/fVlG7MFmMDMalNmGTALN9r+bFrPF9i+QUmCxZhP/Ys39X0qNYM9L11kNeqNNuB8tS6jdKBfabYIux2rMImQpw0Svq7SYTev+R2ly'
        b'OgGjmVkpdRRKJ2kG8/3IYrcUv0HVHINJK9jY9P8bRPXNGaJvh7O+sei2v8u3CLa7ATg1wyDorMZ8OuVBnpvK2mDMfADGNHLZtL3KtZxELrKUyfQADXMuekcd+6/1YNX8'
        b'T/PdaiBRlBhdtJJ4GTJyMVzT5WaKC9xvPPVFhPj0XEMfUfUiRFhgIrtWwWD6rak2EuAfwEQnHDri/sjeE3E1drPeYL5/xHQuS2LkfWJ1/4XJmN+CkV3QP+4upNKGE1k2'
        b'gXiqLJLE0O77Tcy3EgEQn6e9/7qpzm6DOSTZGvog7PutfQ/e94//TkW4KwfoN/mB+YA410iWvv/E+Dmzkx+sdukWqzHbaKYqda8PSXH2ZTKFJAasXGA15OkLH2jrfSH/'
        b'CwotDv9POpMcLYk293V5Cw2ZcI2Y9X18wv8AYtQMmJ1RP9cPr6Wk57eNzazNM9zxds68WBmYTJrvq6d2az7Li+6ZscxgLTSY9dQs1xcadLn3my0Y8rXRfRNrAqBPVn+f'
        b'GSvN5lXRyofNuWZLoflO1q3vuw/Q6vWkodBoy6FJutFKs1SD1ahTGvW/leFHk12sNo+6TYLT0py7Ssj6T4x27nOiyb7gfpGh/+h+lwV0R+eP7r4siBNrdVAuLfhC+TpZ'
        b'hql8boR4yC4hw8j/Ux+al+GB509F7BwNzk6Yiy/yeLsNoeloOhzH19nguKVyRParAQ0TMkypKpM4GG+RwpXIiY887jwQHwcddlr3ARfIJrVbfdeeVY7wRdVDo2RDoQOK'
        b'VR72cXTktpypUBEGbfhgQnwILg9LSNKEJEClJlmGIqBSroZmLJ7+Thi/Wk071/g7u33xYQlulXuyg+W5+DTUaxLg9Oj+R+RTh8Eedio6LSK6zym4BMoU9BQct2Cx2xWX'
        b'JkGFGk7DKahMSgjhkStc5nG5USWieQwc0E3P3+Nhh4bsx6E6LA4qJQjvxcdG+UqhFtqTRdI7Cov6jKNXM2X0TmSsOhxXy2LgMlTYJ9BxB/EB7Og3spyeHldDdXISh1T4'
        b'mgwf9PO20zOZZfq8fkvTuwkyZmwGnFwri4VtsJ9dYmihCherQ6GSAAtNSILuBCgLVsnRMDgkxcdtUMI4tVKW4hwTnwTlwappJjkaPEgaTijZIlZy7IFLLvfKzg92UdkF'
        b'QaN4NFkLV/DFyIlwAhfTK4f9SD/SjbFyDjj8maRWDuonqWmr2JWI0Q8TlVmSLWM3Cjkj8XHxkuj8GNwEe1zGwRGEwlE4tODtDF+8C7YgTcJA212CJQLZydYjEjuPO/oI'
        b'N3oqk22qWsUzVENg94xI3JYvR+m4mEtE+BxuXyAScVmdQHoM0I3Y/UwuHIFydm1CgO7H7UQjgnF5f4WQqZy1P3uCx0ZG5ksQnIRjnAbhlsCx4iFM1SR8ITISWmUIupZx'
        b'ixFuR0g8tK+BatwUGWmVoIXQyaUQomdAm3gMfBDvwgfIrDYZwtUPc8sQ7iR4lrLiozHSyWSlxfQy5RjBsV28dcIleNskMuM0lFFeHkcmd2hjthrjMhgFI7Q2IzRjw8f5'
        b'OeKtBeyD/XBD4AbhgwjNR/NxKxxho20rB9DCVddVRRkebwctQCqJyIFrcCNaAzu0s6BS5Ksr1PJ43wrYxuxx9aQ4Tag73hISRKWMz0mR9zKJaTqcE28Zzg/HLXA8VsOq'
        b'u6RSDh/BJbCZSIQ5meZHkhjvpuMqxrrha8VZFbgGn3byrtTGeOeFO+0EPTRIL7mP/WXhUmZ+E3MIaLEKg9h0M+Mx1OISxmR8ynm7BMVLYavIZDgOWxmXoTGdqf2A6Lz7'
        b'2+0wqCF2eymCiWJZghedP8Ypi7AN9vGkVZYNdf1NOYHYRz9ThvZopv7Dp+HSyMjlI5wig+vi6rAZn9x0fyMPUMhii+wi34rhQCZZvx2JF405EwUmQofEm5ZiogHTMkze'
        b'SfOQyo8BLVoL1Zr4kORQYueBGfQmRDzKHYYdUnwSt0xjHDNMxF1qDT5CFleFxEuRmwuPq6BirrPCba3b48q+UryaytQD71XHEu0wDuivHbgen2bqsRB34SZ1Aq4pCNGE'
        b'BCXTCmHvbIlho5R5ybQV0Nj/wnaYjnCL3ggOS5Ti3R7YwTzfsJz4u+51xVvdVdBNL3Y34DoRGccoKGc+xz+un89RRTL3jY9J/cTLU1zFIgwcoiJiA4N0MuJ2rxFIFO04'
        b'8n2XJgxOz7x9EV7Cr5uN2+z0UB9uhOQ6b4hTZP3uiMOhmTkjM+wcqknIujsKRfeW9OzDXSl9XFWyILqqNaJ6Vg2ODYPdzitO5/2mbLJdxaw9cArhN96vEBmOy4gJQHki'
        b'vRvQUO5OxPvl8XK47rytX5ZCCIgLTkgJkaOsMIWGh8NSXM06H9Eq+l7Bjor1mCHxjsdiJdvKGUV4K7Q573adF7vd69nEGN5y55Ifb8fdHtkS7wBoso8inTNTR+KKfpUI'
        b'c+CKsxihCVpFAo+MhetQOruPPhFHWyOypmLlBKKG23FHXz2Uw25mNnNJtLmq4GnFICJ5zRL3oQwjM74OVeqEtDn9lCzUnzgDOguur0sVuPl4s+jxukiEo2Y0yq9AYSV+'
        b'QU5vWGkhxVkpG74QmvAN2MM9PpMEDRSSB6VM6vi6BO+jvC8nsumv7bWTmP2Nm+JGKxgygjMyTE8bdWI9PS4OhKP9tXc08UR9tHx8sBiF2qfgbSTq7g9f6UKmVaP0ofgA'
        b'09spUNN76+9U3AF4Wz+9bYYW0U7rpsNZfDEc9vpJCIzTyOIvsS8lHfIBGoEoFFTGL0rFbeFLFkMpqy8P3QhnQwKJKIOcd+VLiD5AafCyOCpCph+L4oJpD3EamodToVKK'
        b'8I3HB+DKjRJ2Nf7NbJY9osDEjES7ayRiShA/Gq7epQVwRiNqwRJ83FlxQHz0cZILTiIROYHnFtHavhaoZ6JZuH4M7eAQbFlD3f+5VTPstNxiSHQh7MGl8bCLBNG9uLSA'
        b'PCqpr4/C5+AglMpwW+ZiWybumMwRSckfUY5xVg0SoR8VIWZDOYOIj/mTEMe0B4rDiZWQ5beJUpWn80H4tA/zKTFEEa9pQqFL3z/CeTlLGYg+OHAlWSxGdZdSHEgUK9sj'
        b'NSKNk3EFIxIfwheZV4OTRHINdzK1GFzTN1Oz4wox89kXubRfqpa0SUzVvGGbSsrYxbt5REatkaAVeC+XQGnbEitWc+LruCVykhVK5Cw3M8ApvI/N2OSzPHJSAUeS691c'
        b'LCKWeS6GcWrdKNxK0IVWMr4NamlobLPheufFkjsrErk4KYKQFcwtILkS3qWxz6GGOctEPBJUEJGTNL56CbR64gvesGNSRGpcr94tDlm2+G5dIhp9xB0OPoLP24nloMFq'
        b'C26WTyPmtgFtWA5izdFSklodwc1R+AKP8B68l/dHcGYE2WMw274BnQG4WeayCaGNaCN0RoqvUOBTDwmskH5xIL3ApIa3nDiP7n6rLw9xwfvSYKt9OuXzcag3KpKToDJk'
        b'mdM6oGx5XMLDuDQwbikjaBJuSoXSpJDQ5MQU4vpOQas73haDe/MZEq8PRsMeGT7nJb510DyesW2NgXjSPbhl7SwS7uEAws24cRSZQyPFwClwUhNKVKa/euGdZjGkHYBT'
        b'a4l2Dc+4S7vOhzHeFCbBqSkko7tYCJ2etOSti5sEDbidXRyS3HXzDDLZH7b+VrSYiA8xNE36GNw8RIDOfG85gVTGjcdHFolYVOOuSXcCCRwsYJGEZCvNLCkjTmTl7QzD'
        b'wN+VYBT7sDIv4xn+Bi8YyFe/ELAvfaXab77fufR3Z7z7+tXpkWeDiz98/ouPTvHHAr1OvzDHdXnSZmnM9SeO7qlaCc8tHVey6LWhXkLUwMj6taNHemR7l0ROSPmn2z+5'
        b'Zwa6dK+fcdU0+sTrq9KLHv7mvebvut/ed7gs7ecTX7iFxa0tW77r6yuvDcv0fVd1vWl0dtC0Zd8+erJuiMZSd+C5tIw3TiwrefvlHecsXk8EvdZRl/PT4NbxSY3Lujqq'
        b'N3w2cPCSpYE/Xd3z7X8E2Xd/0B2gUdXVDpnw6WZf3183/c0tofGy403rKFN7xocHNPkzR7jnT7vkcevGGwXxA97Z9Cj/yudp7y27ucdb1q2Yu6jze49X5+3b9OGLmQNS'
        b'TrxUuyrz22k3vS6+7n61SfPBwje9Fz3X3fDY0Wfc1w62S1aOe6K8QBZT0x7z5gYo/P7nLpN9yrXHUBeuM5i9L415/8dt/Hff2UsvX39//fvvyU59rviLfPjvja1fRBxa'
        b'8uGi1z659eGwiR2R2X86+t2pF2be0neEZS3yrChYZ376RUtnz60smf+qim89ZfaitILN3+mua5cVldcu/vP7sUefGDEv+fXwb4ufbtaP/+Rq7tninS+9YXhy9IigzOry'
        b'S6YXvnv2iunx5W/9+a0x/kd0hy1f/Nhx4PfaWyv/MCH0PyJ/mJc302Nf/fmgjxN+kB1pWKw4N8NrzYgh1pacyi/eOnY8Jj035qXMaHlSzpevVqY/tbaugxs0Z1NLw41/'
        b'DPlH0davrv/Jb+L5LcnLtiZHXx82ZH3goV9s7l+4bAj9kzDo5aLSoNyfVr55eJxt6LV/aPat0Vz0z9z3rDm2saZ0SkNH2gcvHmhQRU9/++WFn/0w+Nyvl/Oe3uhh82s+'
        b'0vrLrOe5L9c9s6lmxFPfNlXUdzf/5e9PP3bU+6OndnybP2XjM+9+7zv1pKJjuGdA0XutN1XjnwnFz+d/uv2JwRBw5UDok9UXPrX87a2WTfO/HLzsT1/9JVlzXpB5Br21'
        b'Rv+FdenHye/b3w/OWLztwCvvaGe+8NeABW9+feGLpUOeCyoYcfq9HX9ffuWrm4U3/vhp9LmK6A+H+b02OOH7wynmhhs7Lt1I1Zf+PEuFl3x0/kP3Xe/6nrxyea761udC'
        b'/RO/G7xk2/qvP9ZUfT/1zKvHzl9a+Hi718s3T724akH1wZdOfcS973lr1tCiucv5kfJv8uaVPnfgqzkVR2Or/NTqNu/Wt3J+VxJs9ir4y47cwX+YYPlhVvn5+T+CujTT'
        b'+P4/DCovm5LtKHMFZ2kIMUvq+kLAMYMEENwpjYPra9nLRbj+sSh1EN4lD1URC0bI7REen7TgJhuLP+Xzxqr7VKeQjVSzWKESrxErUA7CUWhWh87B+/qWoNiKxAqUG48N'
        b'1gRvhMO9NSi0AgU3wDVWH6NhvqJPecwguKFg9TH4WKaN5hK4VLNIrEGB+py7ylAO4Csi/rsfg2Pq5Ie4pOAEmhm64st8YRG+zGpUJg4doglLIoSFhZA8qJAPhRJcwhZP'
        b'gTbcoCFha7tec7v0xjtcko0vkREU8AR8gyd+Lw/vuJMZQB1sFVfdPBifV4fipqEi1+T4LB8Jl1Vi2c5BXDZOndD79g4+GSy+wLMSuhhZG8aQHOYiEQdJsfJZoPLBJTwa'
        b'FCMl+T7ZIQ/8V2to/s2HyvO/Dueed47ybNMmhbPanFhabbIJrXDlpM6PO6vDoR8px3MenC+tryH/u/M8d9/P1+5erqx+x5ULYDU5dGwA+d/rF7nMnev7EaF4ifMeBE/8'
        b'fCof7MUpOVrlI+V8uACJD+fFKoek3HDy9CNQfHifX905OSfWCUlZTRBZl/fgKTa+4uq8O1uT/PC0qkjOkw83mrTIKTYiTmSunBerkNwJ9ADOj/QPJXDpDFql5PVPuVSk'
        b'wIvvrVny4b14BoO3ehMeJvcWGUnpyXGf4qL/uvxUnNWnV4Jsrd1UcrQJbUZfjr371a5o2Iq7nHVIUB2Cd5KM+gJNBYfmS+CyH5y/5/U6qgOxFCZN1Az0FW6Uxuu5NIme'
        b'F+vce3zYITgrELLOt1ot1h9HicfiTJ+sznofg16pNSsNtD80WSXtcU1Pp/cI6ek97unp4rva5LtHevoau9bk7HFJT9dbdOnpopLeeTBi6RFONcGO1ZG58myTFUGSo2aF'
        b'F+zGR4mJKtwooSFW57uYYXBELougBVYLjB/8aZ9ECCCz/xCUMKP6cjKk+sz/41cXB07/6W8lkz/7qXvuzo+/R+5z9n/wbNIJv/fdy+Qr178S9/Psmf7TlZNeujV9oZDd'
        b'feu7XU0HN4zdpfsm6sX1Zw/HdRz868vnn3k55vUny7IeDfzn5Uc1O7+T/W3uX07eWnG9ak7Z4OdSfggev0rVNnFjzqJS/V+6S+O133c99FxuynL7jFQ/1dPmY5fenva5'
        b'zH/QmQv7b75x+vWG+LZbFVEjNlz5ulZ3WOb/SOaBmeqzbc9EDzO1PR01/bO23810GW596u/tR+KSp360QwhtLMg0NrVM6jqbuwXGLTee0w1tzOhprB2fvkkT8tq6RfsX'
        b'N+5+71R7y4h33wj53MVgvlT57mf7vbVDq7dOl1/I8DkTN3/igNIJf5LNyopfttRHpZLa6F50Ock6r5Hcf0Qch7ipCKpcoYy53QiSze9QaGRw+Z7XXSM22qiq5Y53UwQR'
        b'h0u9vXMAyZmP8GgUviiF83OXiJHhQEisgFvioFuWHBLYGxkGwE4JboVL2US9mZb7/jc6UTnLbB/8YM6RqKvJotWnpzPPmE8tw596qUncyF95nlYWEl/I+7j6uPDI+eH+'
        b'rW8/yD2cXu4nuatfCvWygZvQBp6zDu7Vf2JzPDGKO25kwH8PYzhrwG1ro4vT/b5Y3/hZaF/HQuVYiOvVuALT85GylERchqtd6LsU9V5DJCPwwRnGJ2oKyb6BDNz1+JkR'
        b'z0R4bY312f77TVmFnrbMbds/PnoNl6z+PPBC5A83V76fFNH9yTb00rYz76V1vPNBem73D4fxpsIlK04cTD/5101vLtG4jlny8cfTIvOfHHLZOiZizX9EeO86vuFK1qEZ'
        b'b77i8vTLAZ3FVSoXpqRkp9wRyv4OAjQGpLANkwtS4DYeTk9NFl/arseVyZqUELhABqWkhPBE9a6Bw1uCj86Ec0xDZ8MJ6BJJo+douJKSFo/bvHwlI/Fls5gfFUMDPZ9l'
        b'Jbh4P65iZbgleBtLvqyhGaQL6omt9P6FBYWKh51wBW7YxBuKxA1CfNJI3NH/TzDg0gXMCqEd1+FiqaBOkCFOg6B2ErT0WsbI/+Yc499VHulv2pLRbLQ5bYkSiDxdeyt9'
        b'JcGbEP0g65Db+q7skZgM5h4pLTXtkdns+SZDj5TeqZKAatSRJy0X7JEINmuPLHOdzSD0SGnFSY/EaLb1yNhL1D0yq9acTWYbzfl2W49El2PtkVis+h55ltFkM5Bf8rT5'
        b'PZL1xvwemVbQGY09khzDWjKEgHc3CkazYKM1Zj3yfHumyajrcdHqdIZ8m9DjwRacKN5p93iKOZRRsEyNCo/oUQg5xixbOot6PZ52sy5HaySRMN2wVtfjlp4ukMiYT+Kc'
        b'3G62Cwb9HYsWyR5ppS8OWSPog/5BBis9cLJS32ql52hWevdopVpspafKVnpQaQ2hD3qPYaVn89Yw+qBHFFZqD9Ygpo30QTXbGkgf9H0mK30Ny0ojqJW+T2VV0gdTXaqe'
        b'1sn0MYU+1LcdApWO222H8MOCPg6B9f3o2vv3Cnp80tOd350+9MehWf3/ZovSbLEpaZ9Bn6xytVJHQ4O/1mQifo7pAT2a6XEnQrDaBHpt3yM3WXRaE+H/YrvZZswzsMzD'
        b'Oq2XeXdlCz2uMWKOMZPmMyyXkVIbFXXNx49g7cr9P6khYh0='
    ))))
