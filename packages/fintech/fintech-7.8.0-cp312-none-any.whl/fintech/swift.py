
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
        b'eJzVvAdcVMfaMH7ONsrS69KXzrKwlAUEREQFpSOCikZDXWBlWWCLvWBlAVEQywKWtYNYVrBgNzPJvaZeVkxcSCPJTe69yc0NGtNvkv/MOaBoTP7v/X3v937ft+pxzszz'
        b'zMzzzNPmzHPOJ8SkH3P8/6+Xocs+ooxYTFQQi8kycguxmCFhLjMjfvMrY/SSdElhVsZkEBJ273jLckJp9gID1XDKWBMwm0h0byJ5jEMSq9hm5QLOjxLzvIVps/P51TVl'
        b'apmEX1POV1VK+HNXqSpr5PzZUrlKUlrJry0urSqukIjMzfMrpcoJ2DJJuVQuUfLL1fJSlbRGruSrahCoQinhj/cpUSoRmlJkXuoxaeae6B8XEzuILg1EA9nAaGA2sBrY'
        b'DZwGkwbTBrMG8wZug0WDZYNVg3WDTYNtg12DfYNDg2ODU4NzA6/BpcG1wa3BvcFjH6Fx1zhr7DSmGhMNT2OpYWmsNeYae42FxkzjqCE0TI2NxkHD1lhpXDROGq7GVcPR'
        b'MDSkxk3jobEt90TsNV3nySAa3SdYt87LjGAQaz0n7lHZa6JMEus913vlEb7PqV1BrGQuIlaQiKWM7NLJy2SL/tljYlnUyq4iBCbZMlNUvhfMIFBd0fuMIovPwlSE2h9V'
        b'VsEGeAs2w8aczFyogS05AtiSNn8u6C4J5RCBKSx4yxJsE5BqzE6wH9xcoEzLgjvARtgFt2fB7SRhnsYA+gCgKyUnzcFuYg716LLHtgHNA7GGQOxiI4aYIPaZIbZxEdss'
        b'EausEdNsEVPty+0oBiHJaXwsW+sYFIPISQxiTGIFuZ4xzqBnah8zaMv/P4MyaQb9EsQhLIjWODN+UWZFmCtBVTKzmIhr3bOZRFHIHXIhXfnGGjPChvh+AaeoKLOclU5X'
        b'6uayCFNC68dKKgq565FH9BAyc1Qdn8ljPbIjksbsV5Gviy9F5NjMJ2VYvfqWdJB6k3oXZlJR5HuKcvJDgqr2C3tovdv6B3/O3FHyl4KR0DPECKEOwXQhvm9FS9UclhsU'
        b'BJvCUkNhE+jJD0rPgjtDRGmh6VkkIbc2I5nTTAufWg3WBMEleDWY1GrglSDKmY/5zfxv4/dvBNLkN/zm0vy+P9Vq5ctkLEGEF1kwU90ItQgL2QUHqJ0BDyJCtwsz4HbY'
        b'mJmbmhaSNp+IzMhzBLvzQTPYQ1SwTeAh2LVS7YRRdoP9a8XgMuo/ClwHPUQd6AcdVNOUSHBADC6gFrgLnAcHiCqgB1o1lk/Qm5ErjkQFd7gX7CVKaxepHTC9oMEetrMJ'
        b'QkTARnBABK9BDTXbLV7c+H1kEEHYFMk+DUqm1zx1vl3AIjIVlYrcR2XJhDR6ax5LuRLdO2yr6Hot4cDGxsPt59tXRfsyecfCy7vE4Q4P9iT9kGR7Ivuz4BgOR9sUoPvc'
        b'4TOZM2eb+Z98AmZvc9hr/qcSmzcXvz4XEvncfN7ZoVf2g72vvFFP1se7zDMeT4paY+6rLc/8qLUkteHdD1+xUFnbg2kvWeyXElbuzoN7eQLGI0+KJ6SIi9gnyMoBzerQ'
        b'YCQvDMIRNLBMgQ52P3JFIG7gLNiH2NwEd74AzsDtSM7jSHCeA3oFrBFGkEBhiYCeXJR4+fj19fU/OiWUK2pWS+T8ctpai5QrpOWqxBFzyhQXlhWrJKsnlRkYuRZdvq8n'
        b'HiSThI19a3Tzam1u04b3nPiD3vED8w3eM4ecZg3azDI6uWnL2mR3nYQ61V0ncbdKM8fo4KaVtOVoUowOzvtS21K1Et1MXa5W2u3YXae37XbVzx+IGMjVLx70SBpymKFJ'
        b'Gbbn6xyH7AMHLQK/xtKnwOIn4IywlxfL1JIRk8JChVpeWDjCLSwslUmK5epaVPMMpRy8nnxMq8IKV1qjy2SKfDFQFLr8UE98O4skSfuPrJybq+q5Yww26TDMtWuO+4hl'
        b'vSXLaGo9bGr//QM2wbaZuPtRieVmF8eHOMINZZYynqenZVhPGdhRUZpKPtZUxlOWkWn2lB6iMnOSTjLWM8c19Zna39fUxxN4rKmcbEopwCXQCxphe0kYsiuhRChAaqnG'
        b'drROAM/BdrAnCMUTYUSYx3yqlgsaN6Dai2pKjURTV0lf977LUMbinuKvYLU43C5obiOZx8JPhJ8p36S/po1/tNSluSBPO7Xj1O2EgG3ZurNvz12KxNqFmLvNrOeht4B8'
        b'xEPonNhpQhtwLD0UatIys9lopPMMeGDpFAHz2TXEAc7EAo5w6bUrl9UUq1ZPvqFkM4SWzbF8knB03ZfVlqXz1SmHHIRImKwdjDwkfx3cVvawvas2uj1x0MJbYfNErhSY'
        b'3hF2maREqlJgs6Kwf44sUcJEy5IzlqXJUxBOCNOPSJjykDC5/qfC1M7xJY5yRUzKIjUU25NRDCJo1GmwpmDtyVC1I6qEl2eCHcqCKFVMOItglBDwBOipocD1po5kLIPg'
        b'jZb71fCmReRRVhN2K8ENJWhIRvAkwZAQsAeci6PgZU7OZAKDiB0t/3Mlr6KDRcPfQCb0sBKclCMEJsGoIGDvrCAK/nAIj0xCXB612qHQ1vavp6azdkmVMgLsUk3Bs5ET'
        b'8BQ4B/dQ4I2ZrmQyg+CPiupLecvedFFjdsHz8EqOkgt6EAKDYNSg3uFlcJBCsFF7kKkMwmZU5Ccx+tkVqLGUgOPwONQqwS0+vBCNKQCbCdhvPpvCUBFeZCaDCB+1qqzj'
        b'MfoFNAX1sLlKmeCM4dkIfgsBLxQUUfCZad7kXAZhOmpVsMyoLJ1DKUR81HIl3D9fQfWOJnR6BTxGQUfE+ZL5mP2iz6oL8tb7UQQkguOgF/bXWKkjMMXIf8H+snGKbTz8'
        b'yAK8APJXi7VTjueoXfB0DiJPfwz2g0tLEQqiGTkoeAF2xlMoV+YFkkvwGsglVQXm39fSTNKDyxuU4LK7UozH2EDAs0APb1IIJeUCsggvgkvf2gLVnFqa5JZVC2E/7MhC'
        b'I6A1A50EHEjypuBHPIVkGYNIGl3FLufVHY+mB6iXzkFMBK0I3gTBdxHwCuhNoxBWuoeSlXjZ4nhynqozjRa6nSKwGfZHpystzBEJ8CIZlU4T8PeCMFLGIIpG0+aXG6Ve'
        b'ZbQXb/aw5q73U1AiCk4gmYXN4AwFX5kYQdbiRRYkVvKCMqdSi5wCOuBZrinUwfPRGAUFo0xwAHRRGIVqMYmUe+5oXJasQHxxHbVoSnt4kOsDT5lH4lWDe0mzpSH0TC/5'
        b'1HIzneAlanngVpK0hXvpheiD3eCE0hXuhv0rrDAVh0khPA2OUFPmgL5sZXScmSXU4w5vkTGwAeyjuowALfncF8D1OjW8hEwzPE/6h3Fpvp+ytFCCfaCXq1BhLC3paQoO'
        b'UiT5o+pOJVLOnSp4mYsbW9BoR6vU2KbMM4N7lEBTbmWJuMlkk9OmOtG2uQdsSlbOn2NlaUUSTDMyCTTFU1MIghdAozIQtFtZ1mGyBkgRQ0y1AG0CaOKCdgfLWrCdRTB9'
        b'yaSSuXRnHXZgtzJUqaDUoJaAZwrtqKnFg+1guxL2gXZVTBSHYJQjmwD3Qg0lGqAbNmcrfUEPkj02rW194MJiChFucwMDyjQBUuJ+a8zAs2QUEu/D9Jpfc6tSvrAIXhpv'
        b'O0WKRaBNYE2t4Qdzo8iVWFHjnCuMatcNVOVLkinkWgZROxq3brU2rNGTqnwzNY6sxyoqSFzOC5JnUJXKKVPJLQwidVTQLOdJP3SjKr8RJpAarJ6r/i7VTq+IoCpPzkkk'
        b'tzOIytE4YnkBs4I2XOXOSWQr1su4sGUFa/6spioHk2aSuxlEwWhau6zA/RuSqrRXp5BarI5xJ1cYxf+cRtvVubPJ/Qxi5aiZYllB7vwoqnKXfRqpw3rI/lclb9XruVSl'
        b'dkYm2Y11J+Xram3NbVoD76pzyNNYQ6KLq7Tk12FUpWlhLqnHajB/z/ICn3+oaN3m5ZEXsKQ7flrOm/dzACUrpWvTlUBbwjXHImFBJiWOSyXYaAqOc8HFpQorSyREtuQ0'
        b'cCWWNlGz4SZkDQbAZXh5BXKeWJqFU0qotmmgN0oZAg/AfiW8gKVyN+njADoELGoCgcF/JvczEaVTt6/grfqunN41Rd0hdcgFj67wkRckglKq0tn7NfIYE5mVFV1qXtQa'
        b'2qEcWvgm2c1E5M9JlRkTWplP7VzYEwFJObrsYY/vI1nUHpIoZ/9P7BY5xLMxUUC2GkfYs+Kng+YcuAPuhI1pWSLYGMbwATcIpyJWILgaStGWsZhJ1Jfh6LHIwnl+Gb1l'
        b'+DzBjDBd5I+jAtk/uOEErSWny7IywjLgjpw0tsieMIVbGKvQBmcTxf+kZa5oQ9NaBS7gnQy5iACnwQ14ijJQZeAmUxiE4ntNGAqHLCrgVribaQ1ba6g9jh3a3W8B/Wjq'
        b'8bBDScSbRCooJ44v/zRhE/lzEGlJRZl/cwynK19Rc4i1Vu4o0C/K1M8II6hwLsJ/hTicEIE+JEC7iGLmGrU3nvKhhFUZeR54+4D+7IDbM8DOsDRwJogk+Cq21ZJcagbw'
        b'hnCNOIoQ5OItCVECNKEU81JBD7wlRLtYuH22Sxba5TWHpbEIewETFXfk0Eb5nBReRxs0BbiAcNEGDTTBW7S5uQXbwD4x6GMth5fR7SFChqLQLgqrDp6BXWIxgXzHDdR0'
        b'kKgQgGuUToBb05liMQccAjfRzWFiWaGEtsfbQDPcLY4h4HHQjm0jUQa3yijm5tkvyUjHk8sORGPitSGsapmx1rH0BrIfbLEWx7BsZ2G7SUiyGLTLOOEDdmVkZsMdYbBF'
        b'SBLcxSmzkNVzUgkYtA7eBHtWimMYcA81w06iHHZPo1tuwE7QJI5BbgXtS5GDraiCV+mAZjfcLYDNaD+XxSZYnqQ52AqOwCOR1DzUL6jEMSQ8jOZAgP1EZck6tRvG6bOC'
        b'Z4R4QWBjNjjDIiymlcBOpnUk3E/xw9Efb40vEXFwBwLWEbKZ46LYsRZchc2Z6XhHyIQ3yepE0AV169RZqHHJhlnKzLS0rFyoAVpw/ckWPUgkCM4SCUIZ5uC4BJxAPuxY'
        b'UBDocRIK0NyPCR3AbidHeMwZnGQQoMnBBuhAzzTZ97/++msBUnId2xGLYchMThxBr3BfGtwnzA5NZRGsJBIg8QKn4BG5wIHiUyrUwI1KS4Uam6mDZKyPrxjupt3XcSUf'
        b'9lvRLZdIG4UgIoVC8ff3gP3jGDdJ3jQhWvMGqiUuArQrEQZt1/hzveBO0E0vRz1XqqxTm+P48RoJLtegaHIVNb0XYG+pEl5aAS+wqbgDXoNXvFen0+K0mY/C037UZklS'
        b'ft9cEenkRHNWD06Bfq4VF+xExncxCY+7voA8/hma5GvwYolSZb4CRz83SBRInHAHV+kHHHwHoMFNeLSNpAAc4cMuqKU9aL2TBParFPACjuFuIjxPt7BKihlqmyxlrg3s'
        b'U3EIEikC3BkPumicVngUbOKaWpojQz2FZJSlIg7XjytdaBTsV9dZ4Ll3kjGpgdHwKNWiBtvgZq6VhRnCmUoGxachDd4/HrgxcXRrrUDxEdOKzAO7poBuK1pue9BOsQW1'
        b'wT7sb3xI0AIuzKjZQFG8BGwBt5R11FjgEn661eQJ2l+kF/KGE9ArzekF20UWS/hrZ9IN+yrgYS7VwLQjy+Gl8OkJtHpvK66A7chah6DQCV0OADo28VkGroFma/O65WT6'
        b'TIKFwg/QAjeX0Z1p1xc/JmmRfRo8BXulwkV/ZSk/QF5on8i6JS9Dfi/J5swvRs+/BLabsSI/swey1tZY0rYLeav+tJhjW7bMKYnwTSFHTPT3mod17j4fZ6bKhr2tbn+h'
        b'GLHo2/rx1qU/n/r87V7FN/f/2vT5A7PqR8NWuSk7Ct4022v+TkTcK/H7F/ULNt2/+bJgLXNx8OcJ96d8+I22PSZRf/ylke6d596VDb352T9/3Ka8eP+dmMytQf+o9Xig'
        b'y7wakp3i9OiwMXXOSE/kF41vR+z9em5g2f7B4bAyXsNrCazyYstXqvZ/anjo8uj4W0mvxgY9MEkKfOHvO3Rc3dCngkHWO//qu52/TV++yVH/LePSiLXHq8kPPdcFfJ73'
        b'1w/5f3trwYFr8/4WOvhz6KODuq/qP7hVabSWv+K27Be2i/Ijl6pTDRvWFQVtGfL9+KUFxxs2vRj3062sypIDsk2/Ltj5Wu6UvV5xP8WlZPf+Sco/En5daF9xoTOl2avw'
        b'84xhm5czNW+9eUWm+XX9F6t+ufTIW7WC9/D7tD3h86Vv/MnJ/ajisz7F3aPfBz3cX7JT+IK08t7cigV5FUs3vbqzbHbDEf0Vk0vpPyv3nd2zwbD67qXmfx4SvbioY83Y'
        b'Pab+y3c2rzw45dfkhz9Ilc7/3hkTf0t3kfNQ/KfdQ54/N3974h8t3556a82wMzj78xt3A1/78FdyYNF+03ATgekjykq2w83VsDkkGxkxuDMEmWvQK8pA9joh4RFyg8T6'
        b'FbBbKEoLCRaIUDNsRLrfTPD4rBenAe0jLP3uq1bRz9DGH6DZZYDzAQGPsCcA293BeaEIWavGENIjBm0XdjBCwUW47xEWTGt41jEjJCgVtmSQKNAnTEEvY5Vr5iNKME+R'
        b'woy0rOAsk9mJBIfFMIXn2I/wI/gy2BklTA0J9lCjPmEjsr07mYT9VCbsAocqKVTYxXHOQLtHfU4o0qvl5Ix5sENg+czTkf/8osQX/vivvv7xkxU7+kmGSlEsVxbThzKr'
        b'n1NHPWe5wqCeszxCG3wX/1aW0dlNm2lwFqCSA0/rPugQYPT21xUfdu627Y7QubeyWgvarDBQatv6+86hBufQe85ho/7BrclaXlu2MQAXXNpzjI4u2qC2F+87igyOom7l'
        b'PUfxqKePLqKjQlesK9FWISDbtjmPocc4hLvnoSkdU3RRXdNak42untq6jsDWWUY3r0PxHfG60q7p3RHdkYNuotbkd739tWwj319XoqvTmdFF1CdVdOPrkjunGcWx2mSd'
        b'5133cKOHj66sc6kxPBpVuN11DzV6+upUndV69oBDn6XRT9CdfyRLLxlQ9VUb3fk6l46c++6RBvdIffTb7nETyGFRCNn1rnvIRIVIjCpcOnPwvczgEYlRnToy77uHGdzD'
        b'9Oy33WPGIT8SRej9e5c9gcbYwnB079SZie4PLe1Yur9wNDgM1Th2ZoxZER6+hzI7MscIMngGaZyV+oBJBqeRjwjSI50c9Qvs9j+cofc3+E3Rphi9fHVpnRuMfD/dosPW'
        b'esYQX6xXG/gJ9/jiUbruPj/GwI/Rq9/mTxtLIwmfgLFMFAP6oAVc0GYxxmC72rVyxiwI38BWa4r2/TmI8UEh56x6rPTKoaCpBgf/1hStWMcednbtUHc76gN6vDDpLO2C'
        b'DgvdfANPaAwO67AecQky8typusIhXvSAg4E37R4vesyS8AhBBCEZMmubPhgQb7CPHw1Juu1wW/qSlyEkF627U1umznnIQYBFRdBWOBiUOOSYiFZcx+lIuO8mNLgJu2e/'
        b'4yY2hqXcLrsT91KNIWzB+OALhnghDxZieZ300M90xGKybD/vsd+z2oNj66LJiqPAz5CfpymzMHgcQT1b/m4WgyRd0Rr9588Ed3P8iGPcMKaApLx3CtgFzmfYw4G0EBRn'
        b'o00E6KrKemqrZTmxz1mOLnssx7da+LiO+O2BXbnl460X679t61UhYHxTjaZhzp/0m4sZpOQXP33AS50ar6qV8LPy46LC+TUKqhApegr1qZs0FV8hUakVctyXTKpU4S5K'
        b'iuVV/OLS0hq1XMVXqopVkmqJXKXkr6iUllbyixUShFOrkChRpaTsqe6KlXy1Ul0s45dJqWUrVkglShF/hkxZwy+Wyfh5KXNn8MulElmZkupHshKtcSnqBcPInuqKOpeg'
        b'oUpr5MslCgSFz7XVcmlpTZkEzUshlVco/4C2GU9msYpfiaaGD9TLa2SymhUIE3egLkWkS+J/v4tQxMMyiaJQISmXKCTyUkn8+Lj8oBnqcjT3CqVyvG214BnM3+Kg9Sgq'
        b'yq6RS4qK+EEzJavVFb+LjJcAk/lkvJmoRiaRqlYXV8qehR5fqyfAGTVyVY1cXV0tUTwLi2pLJIrJdCjxRJ4PXFIsK0YUFNbUSuTxFDsRgry8GDFeWSwrq3kafnwy1fRc'
        b'kiWl0mokCohSzKjngZaqFZhDq57MZiE8VqlQy58LjY+Y4qkr6lNdWonAlOhOXf17sy6V1SglE9NOkZf9PzDlkpqaKknZ+JyfkpcFSB9UEjlFA79CUoJ6U/3fTYu8RvVf'
        b'IGV5jaIC2RdF1f+l1CjV1YWlCkmZVKV8Hi15WG/4c9QqZWmlQlqOyOKH0VaXXyOXrfofpWncCEjllJZiQ8EfJ00ifx5Z1OncH1A1UyIrVqoo9P83iJocMMQ/dmeTfdFj'
        b'e1dbo1Q928G4ZEiUpQppLUb5PcuN11oiLfmdGWPPpSqeEK6FyHOhoWSy35Gw8UGfiOPTY/2+aP7HfFdIkBdFShfPR1YGQc6D10urSugBngePbREivrBKMmmpJiaEWCCD'
        b'15VKieyPUFXIwf8OE8f7wRDPn+xvPG6GWl4mkT/fY44Pi3zkc3z10wMjmD/qo2L50353Dl5teKxcpUSWqhwFMbj5eYi1CrQAyOYVP3/cuePNEnlotkL0e7N/auzfzPv5'
        b'/n9cEJ6JAZ5C/t14gMaVoqGfj5g2c0b274tdYY1CWiGVY5H6rQ3JGW8roQQSKTB/tkJSXbbid3V9cs//BYGmwf9DY1JZjLzNc03eHEkJvI7U+jk24X9gYlgNKD3Ddu6p'
        b'eeWjlj9WNnlxteSJtRuPi/lB2aj6uXKqVtRScdFvMBZIFCsk8jKslqtXSEqrnoetlNQWx08OrFEHk6L652C8IJcvjefPl1fJa1bIn0TdZZP3AcVlZahihVRViYN0qQJH'
        b'qRKFtJQvLfujCD8e7ROLq7HZRHPKr3wm3fVpxPjxfU482hc8zzM8Df3UWZcV8exZV9Z46uhMpmKQpDaxIRWRXPqsqHcli2VJ2FBP7j/f4ElQhxEbwsFe0M8giKkE2Mif'
        b'mgiuULBTfDhJJSQPnyvJTtUkE9QjW3d4Dl5fn00l4eEDHqhNpk+WNhPggFCQDreDq2xhdqaIftAl5BDeXmxXL7hRYKHG22fQSFLpkOlpoaApLD0rIzQdttiCIxnZbCIC'
        b'tnCEMUFU3irUw2ugSTgOgFqt0wk7cJAJ9OBoJp3Z2gwOw+7xsx64Ywo8OXHWAw6toU5TTOF+cGDiVAfUm1EHOwx4FmgDqXYRbFkJm4WwJQucL00PZSCEKwzQBDvhQbUP'
        b'HuE6PB+BB0hbZQu3Z2SDFrgzLBW2MAkvOxbUwi2z1QEYrB+ehc0UHA2FDxivwi7YiI/3/ITsBDAAeylQR3jCPGXdU6DUUVx2FkkIwHU26ATd4CzFKBlsgJ2TIBFYcwDc'
        b'EpaGQP2K2Enw6gyK8UFgJxgQIlJQZ6L0LNgYIuAQbrCLBbfMAkfhjqU0s3bYgH3jUGlZsGkdOIThnB1Z4U7pai8E4VsHj1PrB7fO+M36OfrQJw37rWF9NTgkjmThp/pE'
        b'GdwN6qmzwUR4Zt6kxYInwfmJ5RqAhylkJtCiP22LxJFs6qCsEvaAJuqs0nXOQthuQhDhBDgNW8JVC+mzsNNV4Njj5TWPf7y6LZVUO7wct3ZicT1B68TiouVtEjDo45nj'
        b'SEZuiEFfLScKnifITAKchZvnUccIi8HheLSGYnxAio8cq8CltWqcYRkDT7jQQgF1C54IRSLcJeDQhxb9cNN6sbiWOTOVIDMIcEbIobTIeckysRjq2f4WBDmPABdkfGog'
        b'2FQOzonFCmYNlyBzCHAuAOyl+GEBj8EjCKOPvRycJMgFBLi0cCY1wqw4cAPWO4rFJBrtCFEFLySOZ4SBy3AbEoXtYjHm4VFCpqSzDLaudJ5tRxZgVU2Q2HMI+ixMj+T/'
        b'kBJ1kkKAXfBmCmLldgq8im1rk04kEURtUea2eTMJAZPmeJcoGh8NtoSBRkQlPgg1hVoG2BMeR7dv5c3LEIUGozWG3dMywFkWYb2AKYObwUma1CNrl6/ekJEWglaKxSLB'
        b'oXBwCy0FbspcbodZBs6F0zwDV8AhmqaB2a4U28DRXJpvcI+AEuz81b6U+DuBA89RvhygGz+bhRo7OeYvrAf1NIfhPmf6WO8k7AMnKBYnw2aaxSlcqnPXNHj9aY3NAb1P'
        b'FLZ8CTVrd3heBDaZPlmIA/CKOhA/BIQDLmimJ/5Ik+GWmPFjMbApDh4B1x8vWvRaNR9rHLzKfUbBo20f63fxeELWJtifIQeXxGIWdWpeCffA62o/3O8ZeAA0ZaSFZotg'
        b'U0jQxMGCG2hgIcN1GRyvhi2URIMGeMkEn/kKQHdtaBqLMDNhAHw4e5oShoViKx8tg8roln1cOZ0Yz65KcoU3QNukxUyopCyJBJxYTAsJat86SUiQY9hNHaYnQx3cL0wP'
        b'zQgNBj3TsvELB9YVTInanJp21frMjKfyDxDP8Em3WybLGuwBu8Bx2EOxh5fsMg5oFf/bVIVpCVRv6fAWUiP9StpOgB1hT2wQEVzKRmu6x4c61SxG5vQila0RHI4tCZWt'
        b'IYPHaWfTlmxHJzZMpDWsnksnNgD9UpqHjfDYOmTymyYfsoOuebBZLaQtTQe8Oc6WFiGC3hkGmzLxARPYD1oyMA8iwT5OWvlSOt9gJ7gKtWgyqSHpOfMLQjkEN4MBDy5N'
        b'GTfW8FjeRBYA8pYn6EwApjVSyltIV6lzqk3giAxqxJMSDMARuAVeo6aLjGBj8HiKCbgFTlFpJgi/q4qy9YWJyZPTYMBpF5wJQ6XBIBqP0Ekge5ZN56KYIA8ft53NY8Pj'
        b'SN+wdYK3loIt41ZlT0wKUrcT49oPe/y8grgKDir3oOAA1hdQPQlhpzVsp5KQYUN2qBqepOTuBRPTcE+Sj3NqMl9e5k7Q59K9oAc2hEyF7XAf8ghgJ1GYixwiJZJaJtgb'
        b'CQ+C/nAmTl8jasCOfHU+auEXhijRusCWtNy5oC88Dx6aPw9qqHcuRKFBiAXBVPID3J6HtUQTsiAVk04xODc1BLcg3cmYPxe2sAhwa40taDFzpvIc3ljFcj9IUtFS5i+K'
        b'UoJydZXhLk/lELWUP2YeOG+NmETR0bABHAD9UbWcZeAcQeYibZUBHW2W25cg7URNpNCesnhn7eFVtRgLM+gJge1Akwbb4F7kWjXL0aUFNIEzMQTcC86yQV/JPFUJuBhN'
        b'okXnLCqDR2k/1zEHHKN6nA520V2CNrAHSQoezyMVSWZ84URqC6eQERxjQclQ9pKZ4+YcbJzx2JzPBw20UvTlg4Fxd3AARTNPNB3cmEOP2w4arCgik+EBmkjEywuUiMGd'
        b'eQXPi0oqoA4creLS/uSAbeSkmMRKNBGS2NYIWJSs+RWCy+KYOmaEjCDTEVmz4T7aB1+FA0kseEscxaECEcmsPIrWmYhvDeKo5WRYIUEm4VSGeriLnmsL7ES87I+CehRZ'
        b'TKecQV/tCgFJt96E1xxRYwTmcyNBzkYhAdxcqcYHO/OQdGzjIpfXjNa8OQwRBvWW4HxURFbi3NQJsZsXumDes6KE7NEhc9hZB1qpOS8Hh61AL5rvWjzclrVyeJMWlQOL'
        b'QkFvDDjPAOfAfoLhRMBTDAuazPOJsaAXeY31SDFK1oNrUEu9VcStnqakXg+ZF5QaEkwZRyQVC58afWGoCbLJu7PVCXQke7OMm50FW0IXjGsGbFyYmj4/NZ8mBvTMhZqs'
        b'UFF2JrgGNuewCXAS6nHG0sV5SKJxkJZbFzT+ig0fXBWtA9cpsyqE9bCzCLYisT3DxnlIWIP3ghsICZ/Eg6NT4bVxGSuHp56EDG3gKg2we84sWsZckZua5EwOo9gQc6eq'
        b'Yi1omYFzcy5RuTmXyagoJGIU4/YG5inBHiW8VGvNQU2NZAA4raCS5aR3uGyW8q/ITrjM8jq+4M2avDk2H75/+duvvzZprC4pbc8JXHvCgXE8ya1y46C13LQuaROzJLm7'
        b'Z+3Ks5skX3ou/ubj10wyTPfMijUcVHy+Z3rzLV3/J+9fbDzE3FTQcXnqT+/+MNIxvG7R913fBGe9FfDLt//87txrMUMW2s++D6v/QrdwuIT5w1h06WLzd6YeKftq7CDv'
        b'yCcWis92v9dvdzG/zyVz344vSM1ZF3b6pVW/Wnyc177SdP/LGzUfegdkgnrV8oSkA/HHh+LzpanTpjbuPTA/4eCcLz5zbFC9aSzyV5woEHfuPvk9z4cV88O75Tb/+iza'
        b'S/PO9O7AWatnOh7ZVtkuq74xc/3e7wP5J4GH0196ww0/7h/6Non3fuuHfm66Iv+LaWe7fm5SWH8ZWy3e+5Pplf47Nzav90zpar79+Z+Wy/+9ddd5mGJ6RRL0jovPF7FO'
        b'c8/+pLn90fv1PlP+Fp1/epvyzpnV/7J9fdq290a036lfP+f9a/dHn/TskUo+OPvXOsnGBSvXfuXMab79Ym1B3zu1BZ6LNv/bcXG1zVL/q7Mf8Qyav9cdCdQc9OsMXMxf'
        b'3fR36ZEvkm+Fq7o6vPYPW/7yafzmzn1ZxzqvvPp1nYvbwhstu0quyY4YPV4P3LPR8RN/B/W91z6W9cS8tfQd29k+R+x/uJtMLFzwj9O+4sh/W+1kV/CnXq++CX+807k0'
        b'+IWK2uUN0jf89/zceubL3a/t+PKtTtlg5ZW3Pgn59aX3XRo2KVWXLPdcvpu4bMMbP11cZ7fyVtv+nz0D17I/WeisSu1YMjfu0GWXyrkX3jCT3Xtz7ZtvTdm+4U1wTBX7'
        b'VZWQb5Z/4EebHTveDT66o9XIjjwqGvzRuv9bxqq+s6zPvvJ3/3QQRK49vkm+ejdzQ22gvcju59Wn/l2b+ctXQb++7Wq34H77ByXKgJd2vq65VDco7r58qrzzFdb+2sh1'
        b'2QGfrD10IiiwNOb69qglLl/xx1q+tPtwXvLd/A+7Ag6eYbsWHq9ztL0/GPhB8Ed/n+rqGFT+Ye8F84OadXUZVRGmP7o1Xa7JucI9O1V1fZtGwfh426wLzXk2U25YHP2y'
        b'R/G3gYu/ujeuqXoj0Wy6zrol50bae1lNiz8c+PlLwdUP/+L9z5wSo/iTy3k+n3zVurJec2WzDf9gtXe299nVNmcXZRRMs77paX3z9Uchqy8RAU3R0V+oX5/2U4CxxPr8'
        b'NlVEybIFjj05H68wSu78be6+Jcffndpy6r2MH+sWFlntHQ08tNkltvqhVaGd//fDtQ/m1238/ouXb/k8+Obuhi1fpzStM5d3RXxD/nt58pxWj77mA3+tGysYbPH/aen2'
        b'X/TfCjVdL/5FoXpn4AvJw1fTv110znb5vjN9H34ur255xV/+cf/uY9XHvon7gvXdsNLz5x+mX3qxzuGzhwKrR3i7Djvgifzx1B1kCJEpBG1wVwYKrpzBJVYqPBtBZw9p'
        b'kTPTCINFAhS6HEWhM0GYLWKA42vhdip7iI821Ccfpw/5LMUJRFT2EGyLopKAYHORlxDsjB9PEqJThBJF1LtOvhwUrocEpVbj93IzSDpBqBw2Uz2jeP0CGnEiccksgE5d'
        b'QpvWF3hUptBiBujEmUJP8oS4GXSm0AvwKNU/2Jm7UpidFYIs8+l0nARqCq4wVlQ5U2lNYSawPQNeLkehZ1goQXBWMEQ5YC81dLI52JaBZoRJglthL0WUdTizAnSVUkS5'
        b'wN7yDEHB5CgBbVxuPcJetbLMT7g6RySgeMUBpxliJuyleOkPL6NAin6zC15Y//jlLrBl+SM+tTdDe4E+2I+8Eoq2apHPaq+h32pMYDHBrXwB/385yel/80WJyfjtI1Q6'
        b'K2Ti99QLa9WquKjw1ZNvqESqXzj0C2tyDuHA2ze9bfqQvZ8m2ejorJltdOBpUowuHpp0o5OzZs57PPdW1rC9h7ZMl3LPPnjYLbCbNeQW2ppsdHbbt6ZtTfu6VpbR1Vs3'
        b'o0PYajLs7GZ0cDfaO+MudeK37QONAcEnlx1eprfXFw8FxLbltM5oVWslo87uOtaudcNu/GF3Ubda/6IhLPmee4rR3edQVkdWt/899/DRsCijINQYFGIMFKJOjCHhxtAI'
        b'oygSX4VhxmCRMUT0wMXS27WTPeZOuHrp/Do9jKGRWra2aogXbHTxpCrcPHX+HQnGmXP+LHxJeKd0aOY8g/t0bYou2OAeisZdNBQ2HQ2EKgRD7iEYKdTggjoPQ91Udlmj'
        b'ikGfdINL+kcBEXr/AcYAUx88ILk940rlHd8rNUMB2cag0O5iPaObO+yHycjV13WvHvKLf2DC8nbVssfMCXdvXbbBLdIYFYfGEA25R+DMKrnBI8oYHY9qwobcIydyrWKm'
        b'alMGfSKH3MVUTdfSSSCYmi6PMYYT39XoLuiOGmOi0qi7H2Kso75uwFbvOhSQMMZGlWMcwsNXlzxmgsumhIe/rmzMDJfNCQ+0cmNcXLYiPIJRJ9a4bEN4CLuTx2xx2Y7w'
        b'COp2GLPHZQfCI7S7bMwRl53ofpxxmUfDuOCyK92nGy67Ex4BOtWYBy570nPwwmU+4SHqVo1547IPDeOLy3502R+XAwj/QGOgwBgc8lCI7rWsMRHmnG1HLJ1bdc8tdFgY'
        b'rZcMzBgo1i+7HX3H9k7k7amGmOwhYQ5OUOvINPoFdKSMCsP0pj2JEzX+2hRjCFq3nsyBWYaQ6VqWdrGBF0Rl1XWnGwKn3A2cNjDjbuDM27YGz1laJuKcd4BO0j1rkB+u'
        b'zxjkT9eyjV5+uryO1fe9IgxeEfe8xKM+/t3k4UDtLJzHV6or03ERjKeXlok7ndWx7L5nuMEz/J5nJJrqrPPLbs+6GzPHOIEzxiRQd4+h3n4CNRQzZzQo9By3h6tPGfA9'
        b'n36bHAqa2WGp5ejYw4Io/YKB+UOCWWj6BR1WRpFYP0Nf3L0M3S418ISjMVMRU2bqpfdj0gwxaXf8hmJyHjBJlyitg7bK4BLcPcvozh/0jjAgIeJ5aOUGXuh9XpSBF6XP'
        b'f5sX/1hL/Lsd7iIe+0SOEWRUGmnMmIc6icojvyZI33wSVXrkk6Pj+N0lBl6EPsTAm36fN9vAm31b/TYvC/ckMriEj7p7HkrrSBsMSLrtP+SeqiU/8g/qtj3n3OOst+11'
        b'PVpoDBKcM+kx0ZO95sNIp7wvB54PHPDux1qlviIfCsh6SnVSOhNxfmSKLvQuMgiRU1Ap5K57GKWW0wwu00Z57njgIEQoKn7kKUIzDY83Tpt5e85gQiYiITwLk+CVjUlw'
        b'ySZHvQN2pX/k4olN14a2DTrlPWeh3uGyx3mPAfW9iJQ7Dn/xeNVjcOHie2kvfMTjDzt7DHuKBsNm33E2hM0d8swd5OUOuwYPCjOHXLMGHbJwLuALBsegYYcAnbr7RUNg'
        b'wj2HaUYH+v1f/3sOQYj1rSlGb/9d6aNufJ3nXbfw3/SHs0A9DW7hejuDWxS2qd66/LvOApxLOr1jerf4nluYPvly+vn0AWV/zu3iu1FzjH5BJ9MPp3crj+bc95tq8Js6'
        b'kHzbd8hv9n2/TINf5p28Ib9cbcqwf3B3RE8pTugc8H7HP0FHjrFY3pmkMXLKAHk+aCDltvft4pf8r2R2+yM9NSciYvTFA6TefFgUN+B/m7zNGBAMiZIfsJkCHx0bmRG/'
        b'oO6YI4nGxFm65EFB/F2/qUZ/QfeCoy8io6VL7nY5kvPQgwiYhnQdAVre9Y0xxsTqWLqlBr4Yp2t6DLmH6aMM7lPexmuH1O+uixDnYS4x8ILv8yKwOPm9w5vy0bPMGctl'
        b'Ey4eD/LZhI3jsI2PLrrb0+Abe88mzmjjtM+yzVIruWfjN2rvosn6/lEEERT5kGAgGoeDpxhiU41B028HGoLSvmaScRlYCISZWAj80ZWJoX5UWiA/aGBb5nmwhjzc8mJN'
        b'6MxMmxEWPiP7L2Rk/pd9Nk77LHqej1bEEE/e5KZ88y4Mn0jQqZvFLJK0+45AF5y/afef5m/u54QQp7lTmE+dz03ka36N6dtHSPAHe1CgV0YuZq5imFUKmCM21MEglTSp'
        b'SFEoahQ/etFHhdQ0FeM5kJIyfrGcL8HtomwBa8S0sBCfrRYWjpgXFtLf2kFli8LCOnWxbLzFpLCwrKa0sJBiNJ0MS3EBp6qu/s2wO9FUlfjtvS3ExxYRFDj1jNUa9MFO'
        b'rhW8rOKaoeA0O1QRmg0u01+nCIOHOGy4e4qAnC191WeIUFahTjLegJK2OTkwyWHLivdLTn7H2OK0OmzjYEbQxkO315WZ1TEzkvxEd3bd/0xjs29J3FavV/sbmaZeiV/9'
        b'640116b+tFc94BvXdzT21NEb/c6wyE45dPaDT0O+v13juv396FsLvedXnjn36sYFgWccls1dP3Ute1ks9735vVNK/1k4/cwZO9/qDacvrxo1/fGHPZcjMqyExVui//Le'
        b'3797oLJ1lLZFS16WvZ9XK/DxWZaueXfbyRfFfq1rP031znqDn/GGd06ILjXkcObpovpYjXeJI3zZdrvdn8OzTxdvim0UfBxVrunX+r5VunFA4/9x5AJ9U/TpozssZUc2'
        b'hspKTa4ZYaJVfI/1v9JiX7bdYXg5bc6DMm+zjrcOOrjkvSI4sFSp3L30jdCrdXk/JnBrhLFXPvaZ8ZbD+/m2pwaTX3RIHs4cfe+dazfWgl/tv/7pAm9xDNx6fOsP6k9v'
        b'Je6c3uf6yS9r9oRePKSIeu+7wC9Nfmh6X7nNE/7C+Fd7zW57NwGLeoGAhA1+sBmeyc0kCTKWgDvA9SLqeyEBOUz6iyLU50SWZE58UIRPUlsm0LUO9nCDUcgPG7kVcHvW'
        b'xFdHvEA/C54Demc6jG8ALSlKcCY1O/TxOQPYLbKFrUygTwE7BC608pn+4eV/X4yOH2byk6hf/W9+dHCO1EVWU1xWWLj6cYkKy/+N5PUXFJaHEJaOYywTM+dha7vWyOYV'
        b'Wu+mtR1KXaSu+HB01+ru3M4N5/30igHv8+qB3PMr+0UvJd+xg6l3IzPf47lqI7XFHdFdZrp0A0+kdzbwYgcTsg3O2YPz8gfnLzDMW3jXeeF7TnydXbt80MYPRSW8AhK5'
        b'ADuH1hltjpqZ37I4ZkHf2rDMfMYsTPnmRgvrVqcxJi65uGvL6VKAoDuGLoljBjh0KWnW7QVUaZTCYOMShUGVKAyqRGFQJQoDl1DkZWmDcEzosqsHwhovBwYjvPFy1BSE'
        b'OV6eQSaTCJu6M6WxzegyhT1eDokc4NxeYLR11pZ3xzyv+NAaAQ6auqOo1o6Haui/D7gcH1Tr+Z1NJmm2ELkN+r8XGYS5zbCZTatSG91adc/M5zvGSqaZ63cEvn7NJMx9'
        b'8cVmjIXvx5aboPIjBmkWuX8Vcj9mkVTjA1zx/ZiES5qlkcN2XscsBkNnD/HnDNmlDlqk0k6paQYvmUO8zLFPdmHSTslhhIHM5n+fS3qu2Do8x009cVX42fMTYcX7e+W0'
        b'cT8lIEkb7KZsvsGX/9RNHeZEEOe5CUxpXa8PW7kW1bj1TZe0TDPfnMRLvjU9esSlNyjtevvCgpCXVXtP2C9/L/GvNi9G3vFh7f8s64H2h4SENQ8+/zJjh0fLoxMdnON5'
        b'AVNH/tQ2Y6FHX/8//vqXPakf3FdfWGin/STP1cJixiaHOPPdA0c2fTx98TZXS4sVCYZvj/d/ale2Z8fDT00+MLhde+uEwIT69hFsBde8qG+a5ZjDw/jgLMOE4II+BuwG'
        b'V+ZQIAFgO5GREwrPY6CclXBPKIOwhdeZ4DC8Ds5SD1BiwOVc0IzPFPGpGGgBO02svQgrO6bnenCQer8LanF6B7gEdtDvalFvaoHjgP68kgfcFJ1BfSztasn4t9K4AgZs'
        b'Dc6lnqIsADfE1LfU4MGZkz+lBi/Dxkf4IXmc+xQhPOiVzsan3FCbZinw/X3L+H/82cZzhdJ3wpb+1pI+16pK5VIVbVXpEmVV56DLv+uJr10Jtr3R0uG+pafB0nP/yiHL'
        b'oPrZRpZ5Q+bGzEFb72Ox91gh77O83mVZfsdZw2ZHfkfg6yPqOraaS1g41OdMeoeHP8KUSeQjLPwWyQhbpa6VSUZYOF0KRZDSUnTFbwKMMJUqxQi7ZJVKohxh4WTSEaZU'
        b'rhphUx/uGWEriuUVCFsqr1WrRpillYoRZo2ibIRTLpWpJOimurh2hLlaWjvCLlaWSqUjzErJSgSCujeXKqVypQqnj49watUlMmnpiElxaamkVqUcsaAGjKTT1UYs6QhT'
        b'qqyJjQmPGOEqK6XlqkIqeBuxVMtLK4ulKKArlKwsHTErLFSiAK8WhWsctVytlJQ9MTvUw6eiP/zx+bS1yJy44M/RKXPQ5ddff/0Z2QprklQwsbF4+vqAuv4npgMbypfM'
        b'ODNciJdcuDP8mD+aTnxKbMSmsHC8PG6tfnQtf/qjkHx5jYqP2yRl2QJTBQ64cXRaLJMhM0vNfSquMkfsVaiUONduhCOrKS2WIc7OU8tV0moJFaMqZBPS8CScHTFNoOPf'
        b'RIWCoANuZRq6jDFJknzAYJGsMQuCa1lv8pCVziEdxhZbEGa2903dDKZu2vR7poGDIYkvBcAgQ0i60dRm2Nxp0Fk8ZB41yIoaJmxaeW8TrtRQ/x+sUupU'
    ))))
