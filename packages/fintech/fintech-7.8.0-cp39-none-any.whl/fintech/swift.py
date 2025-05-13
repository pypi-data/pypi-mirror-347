
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
        b'eJzVfAlYVFeW8H2vFqBYRUBE1JK4UOzKoqAibsiOirtRKKoKKCmroF6ViLuiIrIpKuCKO4JAEBTFNbmnk/Rk7HTSSacTstHZ972Tzup/732AoJi/Z+ab+Wasj2dx17Of'
        b'c889j3fRA/8k5CeG/AjTyEOLVqBstILTclp+J1rB6yQnpVrJKc48VivVyYrQOiQEreR1cq2siNvB6Wx0fBHHIa08DdntVNn8pFOkLY2PXaRca9JaDTqlKUtpydEp5xda'
        b'ckxGZazeaNFpcpR5ak2uOlsXpFAsytELvWO1uiy9UScos6xGjUVvMgpKi4kMNQs6Zc+aOkEg04QghWZkP/CV5GcU+bGnKJjJoxgVc8V8saRYWiwrlhfbFNsW2xUriu2L'
        b'HYodi52KnYtdiocUuxYPLXYrdi/2KB5W7Fk8vNireESxd/HIrFEMcdvNo/agIrR59AbXTaOK0FK0aXQR4tCWUVtGp/X7HkLIRRDPVklSNP0pypGfIeRnKAVJyqiahlS2'
        b'KQZb8j0ll0ekbdlBlGGYmOaLrI+RRk/Y/RiUQklq0gLYA+WpqiX4LJTHL54fKEcT5krhzoYIFWcdQUbC7pWrhPhkqICyZCjjkCI+WuBxK+zEnRruAa669sKwgpKFI4T5'
        b'/5Aly7UHfW6PhKDPE/Q5hj7PUOa28Gn9vv8e+mMeQj9GRN97kRzNcfIifMsI4FIdEGu0WyhB2gzKwYyk6pwVYmPRBjvUNGc8acsIWD3ZWWws5qXoQsEwIrEZhjfSHVED'
        b'MihIc9N0T+l3rijmq6GFnGJkx8SJsyXIYEc6wky1XKsNUu7z2jLpDbOr/z2xeUHcN84HnTnf1oRPud88ZzvNR13IGkg6knzHEj6UBi/w9YW9wXGBsBc3LPJNSIbKgKD4'
        b'wAR8Bjcmc8jobDc9GnY9RHCbXqynMVAJsVGWpI+k3L9M0qzBSNq3eB9J7UWSnl/mhHynT0EoJMNhctYqZA0ijfjSlM0EkzL/RCiDkqQFcfEB8YvRpMQ0d3wQn4ddi3Ap'
        b'PoSyZTZQZ4t3WD3olG3z8PFQfJWsD7fhCdyA8gUot7pTqTsMl6AxFF8mfRFwCx9HuZL5Vjc6qQKOwvHQSeTrGrwLVyPNlkQrBZOX4mI4IEMoCErgDgqyQAOD9nScPWqK'
        b'DkDIJcMhaHyQyNbxsa7o8rpUKgDTjvvbIX3gAZNUUJPfX1/v/WnGRxlrspLUd7OCqnzVcepPMlw1OVmGzM8yEtTPZ6kWxqtV8xMPRaqbdRe4xqHZH2kT1CtRlSZObdJV'
        b'Sfeea60PmbW8TOWtXBL17axnUs47xe7rfMrhmB4tSnDv5otVvIWaj02EHp32hFiqZGugH+E9j9xHLsfFUls4iZstnpQInfYehKR7oRLKJEhqsonk8CXYplJxXbyvSiUx'
        b'U8b0e/Dk8ZPHtCyzaYPOqMwSrV+QUKDPskR3KZhpS9eqLTo6TnCgbPZx4Bw4F86W8+XM8t4lVJIu2Tq1warrsklPN1uN6eld9unpGoNObbTmpac/tK+KM1NRMcvog65C'
        b'DYzgTdd/24WXczwnZ0/+F54ngsWh3+hvVjoA34ZOOOYfF+CXgstT491zAuJlyAO2S4eP0MRq+H4CKR1E2omJ6ZN2nhkQCZF2nkm7hEk4v0WS1u/7owxI7wYDpV2eYqUG'
        b'zXc6roEDRAZLiFIEokCpLWteEm2FA/hqNFHDYBSM9+AjTApn4YPJZHQHPkMlEQXhFrl+XM6feYHqyNCrtp9mrHhyH67Fl/c1HGgouhTns6uzKP4Yt+PYH7Oo0DlkdRs4'
        b'VNNoG/PRKyrOQswW2uiIy/wTAmFPfFKKDNlDpx2+xMPxDXC9h1uDiQFjRpe9yPMsg0ltYUynoo/8HDgpYblZ0cdwKWNgl0yry9RbzHSQmRotFd+PybyZmst+nKbT/fs4'
        b'/bff4TQVd9gFF7PVnr2sZr4ngEMj1krx/hyzqNmdah/BEhEiRR6r+EwE56HFmxmDx+EOHKU9HJpj5HUIGhbDIdYTyUfTdgmCWtzAZyO4uBVOsZ4ZM/EtwTKZLBaGr/FG'
        b'BI2pcEw0LZ0joIR28Wg8bOdNZJI+wEr1bfhUXC/A5XCyDxzG1TwuQtAej5utwyh0lTOhmfXKkI8Nj3ciuAzNC8S+Vlw1VzDTiSa4RZdswg24hG2Hj6+NgnbrRALJkCie'
        b'mEBoD3ZhPdM88HHWwyM3M08sGVweOU1crxo3OAtCKJkD2/L4rQha4CgWwZe6LGKTJEgw8PgIgmtQkcVmQf10vIP12aCwJTw+SlDFtSpmasPxATgD7YKDgkeZ+DoPV7iw'
        b'vInW4dSKwik4ZW+mdMfX8V4en0dwFW7jOjbRDt/Kt4dL4bS3wsqTCECSj4tYFzTi3S72ikkEa7wP6nmo5uzGT2BdC3CTkz10UKQn4Zs87OI4qB7Hujzx4RAB2guceDQS'
        b'6ng4xfnDjeUMtbl5cFOwc4RWEuBt5uEOFxEHNQw1dz2ct8+3QgfZ9TSc5OESNw5O+Yucfhw6BHuzhUOBUMZDLTcqEtewHg4fzRYscNWeQzN8eCjn/HVQIZJqOxTj84KT'
        b'IyHHBtwqkXHToR6uMw3GN8bhvaTLiUNOHhI7LmbFXNFbHUxOIc35hBAt0MDDNS5oGVwQRepqfLq9Yx4uI31tCySPcTFKOMxkev0WfJMKhgxNgbN8HoLmmc4iBE1QhxuI'
        b'8IbJUQS+w2cRqYarU1jfSCjDFyn7ZchpFpPCNiIRNxm34EwWviIQ59juzKMwuMJDCxdGXMlpUXDOGAwCdLBOvMeRh0YuFJ+ZqVIyp9e+eigXxiPf7oi7Dqvm701gjUY3'
        b'N24Kjzy7I5Im8wXOoazx+rxh3DQeTSGNmRVunvasMdpjOBdD7EV3tEOs1fnbENbYnDqCm8MjZXd0kiuaMnUUa8xK8+bieOTSHW3I/dlNOYk1bhRGc0k8CumODvDZvXV7'
        b'DGu8tEHJzeeRbXd02fSXCkvHs8aucB9uEYUzOiC00HWzljXKMsZyyyic0QY/x4AGBWscPmkC9ziFM7ppibvwxRzW+PoiXy6DwhnpMPI990SzGAUH+hNHgWK6I8vyH5v0'
        b'kZQ15o4I5HIo8JGfyb3c3tzIGj+KDeYMPMog0+d8HIYeZ43uuhAuj2IUeZebH5AvwimxhnLErs7vjjSkKCzrLawRzwzn1lM0I8tsJ0ZzYazxVMZkbhOP8rojm6JNq25N'
        b'ZI3rIiO5bRT3yDLDCFXCbNZYoonidvIorjsyKSlnhrcXa3TMns7toQSJvBv+hsshB9a4yD6aK+NRDhlZcHzLSyNZ4xj3mdw+SqXIpJSi2LRg1viWZjZ3kEfLuiMDUlYv'
        b'8jSKG0XO4Wop6SKTPB3yxohoeq+M5Y7xaD2BU9uWnbaeNR5yi+dOUnqGJ81amLs7jjXe9UrmLlDShd+1U2ijRR6VxqRyTZR04WVjQ7zjRXryExdwrZR04WWKbcHhW1lj'
        b'YVYad5mSLrxJqoi2m8bUyJvH+wR7BVE8cr7YLXHgYlzwHtGInsXH0+zNTo48giJ7yRBuuhs0Mq30UC2FdrhaIEgQbvCiRsN/ClxmquKB6/BxYmqI0eaQDk7wcJDzwTvh'
        b'ukrkfvzkZ7ljEoLs1LIJ3TZtbqzxxpo/cieJT++eHLAuULUsnzU6+D3HnZUQ4Zl8N4fnhy1gjSHZd7kLEkKByXfT6vzOZzw6OI9BSDwi0pMQypL9J848DwXoFAI5ejBk'
        b'GZ9iVZLv6k0kXClNJWe2SiiJT56Bz5CYmASYHhnSCfgK7mTwX3XivU+xdTIC5nluEePiJHu7aa9wSnYG+ionAjEa817WxOBEsxkqUkl4Zgs7+cICaGUGx9+AGzL8cDu+'
        b'TEN1bjnCTXAR9rO+VbiU8/clse2eYJ8ZJHRxyJY4422RLHrClzTTcTuBOwotxC1Rw3C9mZKMwfCCWiZP5l3okcvhRugQsfFcqnzF+5wnPcY5pCyMRcxUT1PhytAQulwV'
        b'8X6CGt9ebh1LfrXiJ/D+RBY4V9KDayKuDIb90Ep8uS+HlBaZ02Pj2QJTvaApNIwZd2QVMsmpo4QREJ+EdlztT45k7NS7hpwoSoPjpWioSgJlNkT0WLxSg3eMZwcR4rsT'
        b'HDTE+e4Q3UEdrpwRitsIergOQeVCw3poY2hDh1d8aCidcQLBkTXZLp5sJSgLh4rQUMJPfAo5waU146CZdaQlQF1oBB1fi7biOi0+BGfZqRyfxLVQk5hAzlqlKSJfnPIk'
        b'44xTFI8xxKAG78MHQiMoCIfROl9dmIqFOCPW4bOJSWRGMJT7+PtzyH4F8SA+VhXPpjl6p4ZGEFWnccUpXJOFd4xhcK/Hu2B3aAQF8CgaMiTbqGCrzYSzTlCKbwWTY0yy'
        b'DElHcfg0nMZ3RKQuEre1MzSCqAU+hmYuyIHi6Qz2BUao9aesgJKUIFyBm6XIYToRjeNwRFT2cqjMDsUdDE3ki4sMc4k3pRJlcSNBYSm0+iQl0BORBG4TFy81WZPpdpfx'
        b'cZWQFG9MjE+mOY2+g6hvkMovOUgVyCvwOR05iZ7HZ319cYOHvwofhLP+bvighzucJRJIXOZeNxdC2Qq54Z/37t2bPF7qVCBhcmjImxEq6kJGLN7tj9uiUwLjpEgaw+FG'
        b'aIRilRuDfJwqWoATJkezVYJ4OME9BndwG5umwVXO0D4G73AS+zo4FZxbIvrszlQTMWFHcXnPvNucPy4XYxvYHb9EwDeSySwOUfs1ejYJA9nZ8BS0wTkBrsOefKuCdOIb'
        b'nBLK1rLOeQKUCnCFRBQdBXBZhmjYNoYw0ErPE+TMdcibiPdNqCedjnTdS9wkGpAzSFfBTSiz97FxsseVPJKs4FaSOK9YhLQsH04KxKqesygKpGTLW5y3Hh9i00ZMgyoB'
        b't/mSHrrfdk5J9rnMphmDgcS5+NJsixkuEwTxbW4E3JGJCLYlRaSoBGizyEm4RpSiErfOZD3x+DDcsYdm2G7rSI4akslcnIlnW82bguuBWpzT1nwHCv4RboJxAZO5FQvw'
        b'MXsomejkQM4vkqlcPOxZxDo2biQhX/sMOO9sJoGnxImbPG+piFMb7F5HVrvm7AxtxL1IfLiZHCEF7VsHzRsFYj+O5rN9cAc3iuj8YTEa3IlbcLngALsUIteqOKVso4jT'
        b'HnIaabHPg22sS+LKhawZ1mMxphK+HSBqFEDOBVARAKdVjCdwqwAu4lJnRf46DklJtF8F5zlcvhpXM7V0XYov2eNDcX1ozSjU2xR68UItUa75o5WrqqanvhfjsPvzw/H8'
        b'v3/96yVt5bvt9XNnle50GTfS8Wnjh/L3L7u+NvTpf0vLn3AuqdzX9Q/Bp7uHfTXCd8iobK+Ow19P2/Lhlenx7wedinh3mLPDzsj1Dj8PD6n6t+0Or91rsxdmrxJyTu76'
        b'2H3cftnmqJ1eEyonVh68suy3cqfqmJHvfZf869EPvODV04vmtC1cnlKue8nnTwUFs2KvQ8u1rzuvBkS/nPbJ2C/m7tLNs9+lSn9t77eVY96Ybr/c7ZsWrarqfR/VDG26'
        b'qvUZferpv/o0XPKOu+xRO+cvhy3BXwRmFuTeCqmKXFJf/tHlhs9mvbZE++vGj9u87V47kf/Hxb/WTzKMxp8VrX+3/puEVeuiPN5a/Gpaxmf8RcOBF4LXrXT55dXWTyWv'
        b'b6ldsdH9HyuHvWjkv3nme2nAhdfvBlz9++ufO27/fvOs7peCttq9O6Iu/5Wzlhfe+eOGD8vXH+06WG+wWo/90bDByalz3TPP1x/g6hfeC/3Lok+zV/3q9SU/+r3529/6'
        b'QHG9/bf40/WzP/7LXMe3Zn8c9ZbW8vI7Ly+ecmaGYsOO3Np7P8gCvzk3+ZVYla2Fpo1dXYlNLA1IIaaICPeRx8mh1x5fJEYXd0K1ZTTzk5X4mn9QfICfKgiKiPpVBkAJ'
        b'OSgppatxA9RZWNhfol8DpWNgZ182iOaC8EEFSxTlL8Yd/kFE7krI6nJcET2LD8SnYLuFSnEMtDknBvgqMuOgPJFDtmTzwiH4hIWKqoVsXUEMpl+yDZJLvcbztkPhPAM7'
        b'G19NpYd1suQaLXF/ZVApQUOnSoidappiocnmNZpg15zE1ECiGeu4mY6wV2X7YCbiUQ+V7NH997MXrmL2wmJWGwW1mKJnSYz1NP6ZpeBsOTnnxjnwtpwD58STbxLa5sop'
        b'OJrVsuUU7MeVk9+T0h/ehfzW+yHfeSfxO6+wkXP8PTnvQH7z4F3IelK5lOXFPMhTTj6eZH363YkzO6D7WTKH/qD1S5s8GjsVZ3bsxY8tNRv1JlDuuD06geLPDFU0nMEl'
        b'UNKTQglWER/on5IUJDLHX47m4SYbfBBXzlNxzNqMwB1bEuMDSNgSGi6lh+E4vPuhINWxN4acj1iQStP16OGEfZZjX9DK/0tBq4Rd0Ej/sZZsoFD2+zefMlVQqgdesrCb'
        b'm8I8nTJ5UWRYiNJkZl8mBQ2YOuCXeIvSrLNYzUa6lkEvWOgSmWpjrlKt0ZisRotSsKgturU6o0VQFuToNTlKtVlH5uSZdQJp1GkHLKcWlFbBqjYotXrGT7VZrxOClDMN'
        b'gkmpNhiUaXPnz1Rm6XUGrcDW0a0nzNeQVegYw4ClWO5UHKUxGdfpzGQUvVuyGvUak1ZH4DLrjdnC7+A28z4UhcocAhq91MoyGQymAjKTLmDVENR1UY9eIpDQUKszp5t1'
        b'WTqzzqjRRfXsq/Sdac0isGcLQk/fBtUDMx+eQ/iRkZFiMuoyMpS+s3QbrNmPnExZQNG8v98s0mLQ6S0b1DmGB0f38Or+4EST0WIyWteu1ZkfHEtaM3Xm/ngIFJDBB2eq'
        b'DWqCQbopT2eMYuQkE4xZakJ4QW3QmgaO7wFmrQjLHJ1Gv5aIAsGUEmqwoRqrmVKo8D40S+FsjtlqHHQ0TbpHsSdZ06rJIcME8pt17aOg1hhMgq4X7LlG7f8BkDNNplyd'
        b'tgfmAfKyhOiDRWdkOCizdZlkNcv/blyMJsu/gMo6kzmb2Bdz7v9SbATr2nSNWafVW4TBcEmjeqOcZ7UImhyzPougpQwWra7SZDQU/o/i1GME9EampdRQKHtQ0xkHQ4td'
        b'VPwOVrN0BrVgYdP/byDVP5KI6nNn/X1Rn73LMwmWBxfokQydoDHr8+iUR1luymudPvMREFPPZVH3CtdS4rnIVgbDIySsZ9P74jhwr0eL5n+Y7mYd8aJE6aKUxMqQkQvh'
        b'piY3U9xgsPHUFhHk03N1/VjVCxAhgQFuCoLO8HtTLcTBP4KIPevQEYMD+5DHTbQatTrj4B6zZ1viIwfx1QM3JmN+b43sdQP97jzKbTibZRGIpcoiQQztHmxinpkwgNg8'
        b'9eD7zu/p1hkDU8xBj4J+wN4PwT24/+8RhAdigAGTHxkPiHP1ZOvBJ8bPmpnyaLFLN5n12XojFamHbUhqT18mE0iiwMpYs26ttuCRut5/5X9BoMXh/0FjkqMm3mZQkzdP'
        b'lwk3iVoPYhP+BwCjasD0jNq5AXAtIj2/r2xG9VrdfWvXExcrfVNI86ByajXnsbjooRlLdOYCnVFL1XJDgU6TO9hsQZenjuofWJMF+kX1g8xYaTSuilIuNuYaTQXG+1G3'
        b'tv85QK3VkoYCvSWHBul6M41SdWa9RqnX/l6EH0XOtuq11GwSmBblPFByNnBiVM85J4qcCwbzDANHD7gloCc7D/TgLUGcWMZzJ0zCqh5OupgD3iwYIebZa/Jl9E5A2apV'
        b'G960LEVWF9KohGOzcXuGNzn3TkVT+Ww2MiJYjsgR1mVbbHZAkXICEnO3TZr0npQ4PoG3IQ3ehiutPrThFJyEZv/eU6sA+/sOrmNGy7zwgYUqBzZwThhUQWlwQnwg3huc'
        b'AOfdkxMDE6A8MUWGJkK53N/OUywoaMHbYKd/wv1eV3xCgssycasZn2CJ5sm5jv0y5FAmsCT5FALYFdYvI2vUs2w43oPPBEN5bz48JEm8a63l10GpvyIMypMTAnlkC508'
        b'3huFSxicBik+RZcnCyeS8zi+OQsqg+OgXIJGu0qhFnYksGFRcD2t3zB6KVMSTKAd68/xsmn4ENRafelepyePHDCMXV6kJOMmOMchFb4pw0fgJKElvd+AypFwtd9oMrQ0'
        b'OD6ZQ2Mz8GF8RBZji8+wMj+4BUVK/yAoJysGJSRDSYBKDsV4BxoBR6X4DHTgTivN9mzBOwn24rj4lbghGfaSkWiYuzREtchKa+vgCDQG93EPn5QN5F7JZJH9DXAAnwud'
        b'RK8dajblIS3uhGuMXTTPCu0PsgtO6HErNKWxS4YpNrA/dJKM3jHE6FDOKqgS17xaCMVwAA7CdhuEQlAIXIY6sTRxV8zsfgweBWd7GHxrC8uqaomEHGP8hev+/dg7NFDF'
        b'swyJZwbeEYrb8uSIS0LZ7riFUEC8u2i24N2kh25/Au+bjnJjl7OCJbgxF28nMkE2bRogFbiRU8nFsojzuMIpNDRPgrhElITrcDO+jsXcOtRAB9SHhkKrDHELUTi+ii/P'
        b'6Slru4DLE0JDzWRWKloN9fgJrahRBiO0kxltZMYSpCYzOnBbjJjfgTv4TGgovV857UFgzcXXjWJu+iT5VIaGUlKeIXBeRAZcJN7hvzbbA9FSuO41psdvzJ6HrDSTN5uM'
        b'2S74jCcrzUVzN+Ej4v3gBhda6zoFjV5vyF8/B6kkjAI8oWZ7IpThZncoF4lqSxQFH8KlGWJNVzmuhYuJQYF+lNG4Be8isoacl0gMS6eybPa6MFxJ81I202RIKuVw3XCb'
        b'nusnuOwX2Eu5uAmEcOetYrHEATi2so9s0BiJL0MnnGe6EIJrcHN/PbyweqAe1sFNsjwlpReU4IpeGm/BB/ETcHOJmLI/CE849FHZkRC2Y5SRqe+wQvPg2jsC1xL1vYwb'
        b'xQWqodzQwws4kUF4cR5KreNokm3suMH0Gg7D4V69HuIlisARIlpnetg2BB9HhtVxDAZocJgzuLbD2QmyGGhcK96Gkj2vhIayW0fYsQzleLmLdQaBTogwxnNb4saA3RMW'
        b'IJUb0+jVy/ChxPjAlCCi6749GV5cCSfQCFwsxeciZ7OrpIBCtX8iNK6BMlVgvBTZ2fC4guiyqCYR4/ATlJN4t18PKyNzmD3BJxBupfdv16F5oJTA7R7benRWmH9CYGKg'
        b'XwqRpSrYxSHnbInOJpYRDbanGAfe3xKa4WZpImxDI5KkZHwzVDP2h+HdUDdwaDy+Hnz/phfKpzFjMWvYzAetj2kNbsUluJZtSRzWPjgvmhNcEdw3VJkhQ34aGb5INq1g'
        b'oOMdelyaGIx3rkzsdyOuhRMi6pcKTX0Xx323xjOgHsrGRIgj9uGbuLif4bKf32O36onJY7e7NcPni3brJK7rZ7hwVYx4+Xc8Iw5K6SWoFq713oP6wH6rH518Bh+As5T4'
        b'jPC4BCql0BAMe5PozUEireGehGvk8cMkIiMqZHg3QSQuAM6OSkgNlCP7RB5OZG5mJnQlHMV72GVtDLRBSUrvZW28WKk0HbenQym9/cW78emeG2CkEe+0juCqSHr/jw9t'
        b'hj3BPQUARNCqRKFuwQfwjftVCrhoRnK/KoVKOCqazCsFcJnKWDh09MgYXJ/LqIAPeeCd/omJTv1lExqcWcjihNuW2SfgWyRkSUNp6jUi51qG4Zv3pa5spih002N67E8c'
        b'bpskwCE4K1pC/AS+Kl4Ski/4jj0tboUGXGNLhaURn2ZeKwrXwD444ActYnlo5mLGwnxOTo3kSfyA/MfiGqaUSwpsEYEzZJv3RsNIjS1iwuynwtcGE3vcsUkUe1w1XBSA'
        b'J4ifP0fMYo0NrUzEO1ejdGLcjovRwYF408NyjDvCegQZ7kAzM1pz4LoVt4dImPfpINGaaTQusy4hPYoVDgIRMCiPXzAft4WkLYQ9rEY9CBrx0UBfwk6/nlv2NGo69gQs'
        b'iaNsZIKyIC6A9hCDkrh4PpRLEb6zcQixWo0T2K16ja0YYHYvW5tUokxCLDqYCfuFfqJwIaCfKNiYesw3rlmgxe1h1FsvQG5wGzdrsRgiuBAHdpZ2cdQ/yKEOt6yZaQ2n'
        b'c+7gY1BKgpI98STgrIaDeM868ignDrs5ArfIcFvmQksmvhLOEW7JibBfXh7hxwTPQKae6VsTX5+DW+D6COIEaafeUZHIaigIX+XEE6TzflrcwmRsPG4Kuu/80qaLrm8q'
        b'ITnT7IqRq8hOztAyUCwKSEjKXPdR2AXV97HMJvLzxAgrvSYMHklir4GhnA8c6onkhohj8O05sK83jsPncVW/QE6Jm1RSZrZHwXY4GxqRT/xgAlq9ALcQhyd6saMToCU0'
        b'jJZ51BCXuA/pyDjWQ8R7RmjYOkKLGIRrV5A47yrsYxBHyPIIuNCKqOeEKhI0EZ97XsWxaWnT8TnSO5F0xqLxcBGfWIMPWumlF5m/e4w9lBPmVBDRgso0aHXEl8Imzo/r'
        b'FbyFgUtm4l0LHxQnItZ1CjgyRC86zbMmuIIv2kADgXoT2kTs7E629ZSFuAlfjMCXeMR7IFwWCo3L8piWy4dgMgMOuxNHuwVtIcJxyRrMDCdcUgisFn+hL736pCq4dMDe'
        b'SwNtMuEqiXUOwG3rVGof8alx9sSblwcuEVWEWKAiohJL4xIWxy0SUcIN82FPcmBQSlKqDBEb36ogIdGxoN6Ypx62k0DkgHRNb8H4EGZzFk2FHQS0Zhl9GYJ4qWsIXxwD'
        b'HWQWlbJlhcS/9kmZMlaUsgjig1gIdpNoOxEzA4FmYIx27DHGNLm7GdoLoMPRERfRCoqrXJgXPCHeMzYOIU69v/cgpv3Qw+4DX5kl2sYLJjgoQEeeM9GpUjlZrIQb75fB'
        b'zJQ8BXcy1zJ1yn3Pgs/mMlmdgq9OeTD+mKnviT7sc1g9mL769FsyIYt8/eBOoHXR9ErvuS7Nv9UeP/5m5403//H3b4+831r+9fGnnuTkRctbJ2bvtB2Dxh69oLUpjX08'
        b'OMru5eRu95y8sIkrTo0sQWP492qf9Bnv886EryTerl9dz/pyk2vsmcNbfr1+o/H6J389mDUzfHO2MU15/uRXa5Y8dTCrpvG9D7Kfqi65eu6IvuDSy289v6j1raBFyZ6O'
        b'nzoqnnn94583PtZ6JLnZ793fpBGGV1/5abddfM6ul69OOZzzQ+nSL4yHC59uHvOngz6p9p8uHrngue/e/jAiP+rPkiaP+owzjiN+2Lz329dqn3y/O6p7VN7f6n9+77fv'
        b'VdMKcq2zNanR4zctfWbR5fcd5p8rvZOXZa3zez8Kt9j9PPXVE63fut7o/PN35aOeufDyvvUhL4Y6bir7eX9gWsafnvU5oVpdN6Lz7xrzb2mXNnivDi563eV5uwL+jcg8'
        b'KJH/0Jw34SnHJ6c7PX9txs4R8XOmZtS5RHz4zJl3/nTu2XnaT3KefwdSn//b7Jv/9sE+j3jHUuNm/dNBpo7X3siSeGw+mlpe8vMY/w1P1l96K+TomNlJw815Waefmr7r'
        b'WFa+d2zpl23N3334ZYlTZkTo2yUeP34WLVv0hwKnTanHv/T+4pOwTsc9496r/bD4xpacrF/Cvmh+88/RNaGF53744g/PBS0Nt5yDhLgFDe5vH3/62vPl55bcHFeQ+23H'
        b'3ateqaUedcXjHdZ/NL4pc1PsZc591tbPL9x5J/qbX5ve2/i3XO1baJVvSfB6wXv49TNHfv3F+60P33/c78OEYxu5xRFfPNt2I67Q5qZT7rl/5JZGZC7+o3FOx5I9k083'
        b'r/j73dIFab/8ZeHU4NIPvzz32zBn958VL0QsSXf/+Y7HY92JO7b6b9jzefjb33xQvfqZvym8Nl/wm/rL/ulj3vzndcu7M54cnt7yV8vYj8p3P53S2LRy16Gvn3Lc/naZ'
        b'5rOsLbkzWtI3Wq6O+sX/9J1rirrRo698F7L0hZMeIydUjPOzTPhqcXfKH5omrIv88pkffT781tP60rOnlq5bdijw7aJPPnfYeu5owex7Fw/c/vDnC6G3F4yZ/Rc3+Zhf'
        b'9+xtr769rOGzGme3p+vvjo51f/ennYpbwhzVXz5NPPQkHOqMDZdvWvzOm7GOXb90WD7a9sT29i9O5H15cvbnb916x+GrIGNd0ozuT4dUnvl+3dA5730+blLYeG1caYvr'
        b'D+GveL3/ai3cevHFsvj3XX946d4vIz+e/ZzxV/vQDH2cZ6DKib2bBAczh/TUk0CJdQ4zgER9h+EOaVzuNLHkJCnG34/4katBKqK/CNkt54mp32drYfanOTdCLGjBlW5B'
        b'/epZ4NAMNns8dC7qV7CyH+/CFXygz3qx1qU4qjAxgINbvv0qVvBNaLFQD7rKLlssp7FQP1HZV04DDYGscEUXgqt7Clf6la04T6CBbKH4WlWj1dk/BartkwMSoAKR9Tv5'
        b'gnSoZpuvgEY4mkjMXXAgsV+wDVoL+CCogkvsXZxQKPVIJECpRKTWpCDkHCLJxjccLSxYrYU9I+4HBjFmEhfIHNimq2EHbvbvIZY8n5jiJj4U71zFlsVt+I4te8cHHxgr'
        b'vubD3vFx8bew3MsNcty5De2ECyTAyiOhZ1XvG2PTpBK8LVo19F+tvPlPPlSO//V1Hnotaa0lMiyEVfTE0KqUrWiZLSft+ShY9Q79SDmec+BcaVUO+V/B89ygn+8UTras'
        b'6seW82SVPHSsJ/nf6Ve5TMH1/4irOInzHrWe+PlUPsyJU3K0NkjKuXCeEhfOidUbSTlv8nQjq7jwLvcUnJwTq4ukrJKI7Ms78BQaV3F3XsH2JD88rUWS87TMx4e0yCk0'
        b'IkxkrpwXa5cUZHVPzo30e5Ed6Axa2+T0m1wqYuDE91Y6ufBOPFuDNzsTGqb0liZJaWa5X0nSf51/Ks7s0stBtlcV5Ry1Fmgb+mrso4uXlFTAq6EYqvDxjT3FS1AZSGM9'
        b'hLzyJNAZn/rQ23hUIGLoBvSIpaPvh6MVvJZbIdHyrLBI0uXCMuasmsg812w2mX8aLebQmXCZe4qDdFql2qjU0f6gFJW0yzY9nV46pKd3KdLTxRfByXeH9PR8q9rQ02OT'
        b'nq41adLTRYm9/2CY03xZJYGOlaLZ8mKWtTp/s70T1ATDVYu9HcUw0NyjoMFQJ5clwz4VF6uvPf81Lwwnc+1qCqZXdqbAfJe5b39b9eprBROaplxQvz3ms5X7PvonUpxM'
        b'zH9v/EJF3q45RYG3ssf+phz970JMzpHOgooPnt9U+OVjq/764zKfZ79/XXhF84+dL36fVLAlPOWDj52M0971+frP76/YsUn51Rehf87T/Gx1i/9l2ZbnJkz8OGH/ISef'
        b'0lkBoT/MTVIU3XHUr/6xsfGTU8n7F75zLqLAr/6XF07PCv86rdjL6hWmf/H87JiaUcLd9id9EgNeyt61+JVl2UXJHa9mFa/6/tUPt82u8Ez6ueG92qEpke9u+uRsddVz'
        b'kzp1i+1XBV0L62wxfrTD+Onp+Ns/VSfUFi445JA28YfXnlvQsqaxWoEn/e2Nsau///fiF8ptngqEOSFln71aofNzqcTOW9GsH5cEpCpVUgvl97wl01NwLTHvRIimIKgY'
        b'E87qJGE3Pg0X+16ZXYrPizaQvjM7ESosNKvwGC+z9yPWl5r+nvdqyYHqFo9G43YpOTUXOYtL3TbOEnBzXEqgL6536fUTQ2CfBLdCZSGRdSbyrv+NFlXOAtxHP5ilJOJq'
        b'MKm16enMTEZTzfCgJiuMG3WP52lxIjGMvIuti01/Ayf9Ue7QY8B+ltu6pVID6rsVbeI587BeaSYaxBMRv28hhvz3oMmZPft0h25O3aRY8PhZ0KNtBnXkMbM1uJRmQOhf'
        b'KSAHoEobfBJOIqfhkpHrJumfDh4iEXRk2Au6opHPTHTaEeOy+8WtWQWOlsxzu7tP3cR/WPN5wLnHfnx15ZPJ4Tc/2bWrMevAPzdfee3ZglwinPheQdqys0fePvfxtU8a'
        b'xu3cr7J8d2z4te7HO/MnTJz09XrH/WcCVrX/9cQnNaOf/szz5ZnpKhsWWyx3wTvYm6up7CxkQ9x0mx3s4OECrkUscjJD9eTE1EC4RAeR/49CDU/k6qYEn5qD29kij2eu'
        b'E/FiabNygheHdyMnV8ko2D+ZhRGL3WA/iY1u9hXm8rYCbGfRTyzULU/s99cY7FX4NhzkYV/ccjHyaiVH6rMD/16DPIH+vYbKXAs9L8fBabzXP0GGOLickkgilmjc1Cvu'
        b'o/6bo4j/rAxJf1dB9Ea9pUdBKILI0ba3AlgSsBXRDzIP7xN7ZZfEoDN2SWmxaZfMYs0z6Lqk9FaVuEy9hjxpwWCXRLCYu2SZhRad0CWlNSddEr3R0iVjb1J3ycxqYzaZ'
        b'rTfmWS1dEk2OuUtiMmu75Fl6g0VHflmrzuuSbNDndcnUgkav75Lk6NaTIWR5hV7QGwULrTLrkudZMw16TZeNWqPR5VmELge24STxVrvLUYyS9IJpSkTIxC57IUefZUln'
        b'rqzL0WrU5Kj1xL2l69ZruuzS0wXi7vKI85JbjVZBp72v2CLao8z0LSLzRPoIoA9qLM00uDTT21rzBPpgAqyiD5pGNNM/T2EeTx/UyZlpisRMo1UzlWIzTTWb6UvtZmpQ'
        b'zfQO00zfbDLT97HMNKNupi9WmZX0QUXTTOXXTJNy5sn04d9nFyh37Prswo+xj7QLbORPtr1/2aDLJT2953uPmfzJK2vg33xRGk0WJe3TaVNUtmaqXdS/qw0GYvyYVNAc'
        b'TJeCsMRsEeg1fpfcYNKoDYQbC61Gi36tjgUX5sheUj4QEHTZThPDiGgasrBwRUoVVpQ8FzcCtS33/wAvcVVt'
    ))))
