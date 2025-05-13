
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
        b'eJzNfAlUVFe29q1bt6qAYlARxQEtZ4pJBedZcQCZRZxihAIKKWWyBozGGbSQUUEUB0BEEZwAccABTe+dfi/dncHkvU6n6eRlfkk6Pb0Mnf6TTvLvc26BgKSTXn+v9X5c'
        b'VBX3nLvPPsP+9vedc8v3hT4/SvpdRL+WefSSKmwQNgsbFKmKVDFf2CAalWelVGWdwjwoVTKq8oRcwTL0KdGoTlXlKQ4ojBqjmKdQCKnqeME5Ta/5Os0lfMniaF1mdqot'
        b'w6jLTtNZ04262B3W9Ows3XJTltWYkq7LMaRsNWw2Brm4rE43WbrqphrTTFlGiy7NlpViNWVnWXTWbF1KujFlq86QlapLMRsNVqOOWbcEuaSM7OH/aPr1oV8t60MGvdgF'
        b'u8Iu2pV2ya6yq+0au5Pd2e5i19pd7W52d7uHfYB9oH2Q3dM+2O5lH2Ifave2D7MPt4+wj0zz4f122u1TIOQJu0ftdN7lkyesFXaNyhMUwh6fPaPie3zeLjjn65XRKT0H'
        b'U6RfN/r1ZM5IfEDjBb1LdIYTfW7KUArs2pQhwzRec7wE2wT6Yz6egAdYhIdjIuOwAEti9FCLzVgSnhAbqBYmLZPw4VqzbTrVzIUOT6pYimX+VBtLw6KwdA3dUjQ5Liwg'
        b'Aovh4SwsDo/EwnAV1S1z3oiFmMcbfmeERnAVhAFT1BeH79k9WrA9TRfdsdUT25zd4sLIaHF4Qhhc9cWCgJVReHQrXI93wsNhCWS9d3O+YZFYGh0Zk+BLBQWTyc24sJUJ'
        b'voFh4QEKuCQJVjjsNWMK5qUo+qww965Bif6RGUpzd8yBokCkORBpDhR8DkQ+7oo9YnyPzzQH6X3nwJl+XZ6YgxZ5Dl7czIZi3ShBl+R6zDpW4BeVm9nEPEezlxR5zBIn'
        b'Xzzo6ywMEJyWOyclBdSmW+WLp6dJgpPQLrksSop8eYiv0CRksKaStnlLXwwSYr92fnfSZ+KtqYmbYxQZzA+je9VeLyHJQ1iUFPymWaNIFvjle5mfj3t7lO9oMfYdxXfr'
        b'dj7zutAp2AKoAMuWJNB00JT6+mLh5DhlWCAWQtNqX5qWsoCg8MCVUQohy8N5/hbcpw+yDaFboArPYqvFVQF3dpOBKgGOW7DGNpiKvPACFFnMqrl4iUqKBCjIHMcL5obh'
        b'AYtZA8f96XqJAIXbYT83hmfwpK8FbwnaTPrjiADFeBPO2Iaydu7BXai1QKk0H8qpsE6AarzpZfNiZY074QwViXCX+XBOgJqFsbxkCzTjYcs2FTR4sN5RU3glzObN7jmP'
        b'ZeQ3tqrhFlylwkoBjkBRAPfDB0uwymJTwQ1soqKjAhThGR33fTI27LC4qbMT6HqtACfxITbxe9ZPx1oLtknYTvUFPEHmAqCde+GJ9TstUCzsxjzWRwFO2aCAWxuHFXDF'
        b'ohWTI6ngLJmDghR+C17E6mmW7Uo4vJr+OC5Q5/ChPOCVWL7E4iH4wW35niq4i3f4TSE7oB7b3CQ8v4GKrgpQO4FKWDt4bgHs05pVSaydy+yeW7m8AIrhgj8U0fSVbREU'
        b'TgJcM2r4eONRqMFDFryuGLOW/ioXoAzLsdA2jI83nqZ5b7Mp8SbNEh/xYzRBJ7gXwXDHSYstqpV4moqaaTJWYJU8h3egCest20Vs8JZtFsJpLON3mWBfigVvS9iErVR2'
        b'UoCjk0N5h0fjgTCLhwhXIF9u6hR1uEgei2I4FYBtTmIY4QueF8haKR7nHVslTKQC1TNYzQaTnIC8CHlkq/DifGyzqia6y+2UTcLL/BYPPEUT6KrGSg/5nmpdgOz3RdiP'
        b'NLKuiuFwjYoayRzeGMXNrZsYhG3YKm3FUiqpp+UPLVZe4ieOJIBT4EFso5JrAtRZ8bDs9j04M4zKVIEqeYTOQTtclyPgQiTWUpFyOSEVtghQD/vgmlzUvGMmjbkaGmbL'
        b'a+8onIcjvKnB2AjtNPOKpfBQvu1ciiu/KZVKrpCDbQqsXUhFl2iMbE68VxsxH2tYkQaLpsrrpQbvzecGfSBvDs2hgtap7Hu1GurklVSV5ad1UsCRzfT5lgAXIM/DNogK'
        b'Vpg8tHhd47WXrt8kB7aOl+vvG71Dm6uCYwlyEyc1WMCbELFNrcVb0nq8QiWt1MQ43O9YQGfhARWp1yJrvY3WsSJBniEonkgFKqVebqQO7lnkET1hpo9WBTYEUUmBAIew'
        b'Dirl+W7MhjKtRcKzqfJgV8H5SNsI3hW4TdNVNAOPwE0oVu0Au6DEc4qYWU/ZhjOj++G8DYpy8RiUQKFKh/cEKV0B+6e62ljWD4cj3rx0lBJKgh02BGcoEYfCZbysV9oG'
        b'slGG27lYpBQ2LRWyhex0uM2v4uE5WB0hCXNThWQh2Znig11NIShqjVALT3lQ0kjNpKt83vONU1nXavhc8L5dgps2PSs6D/kUlRVYAJdnQJPKEAUleH5LKNRviMLmbGGa'
        b'RUVwcZNq80EqMMJhi1WFHTySDgtghxPLZUMnVuKdLjvXsBKP8Y/TqCOVkjASSyQ8ssAZKsLlIS1PwWYL3lBg+3oZp0uTp9j8qGQAjVmpbIf60sgMhcG1bjvQIWHLLiXe'
        b'gAfcUEYWdrDUkQ8Njtyhwgs2X+Zr9ebALn+u9vDniuxPuYT38bZ6Z5w8QpV7MJ8AVsRbafRXjQBn0O7BOwYnoJJQoSIMrtAAdRsKZr6RoUClcQEBdhOU8DWcZFxtMUum'
        b'bDJiFyBfAbd4r6ith5DXPTx8mOH+Fq0Oi6BxjSfNQbuwUqfRTp0mL/nz1q2U9lw49LC0B/b1NlqXQjolnVtPjjLlqBL2dolcWqUSAs2qbRTbLTbGIHw8F1CmHDrckSjh'
        b'HJZwU1Dga+zuVYkymXtk9NpCCeAUrQAo2hAlhGG7mia/gdIxQ21q+Cw2EaJTcOId+ruU0holxGrbOCqduoUtJGZwOFTLI8VmTloljMA2Jc2aA6exbRg0WlxEWkTH5Tmr'
        b'XOBhm8Ncuo+1G3vMPesT3qYg6zl/jVHM5StR6uQoYRs0O1FKqHQQibvrF1igUJoNtTK8nSGkfsg7Owvsfsy3a91TqIRyPIyVcCiNou4UpdqpU7FWBaVQh+f5HCwM9mA8'
        b'4lmsdRAJOLWeL4gsvBTSa2HJ6/OSvD4rlHibsP5+CNbx4Y+IIfrgLm4nB/EUw/YDbjZ/NgoPYuF6f/HSJK9Pu0TQelpDrDhfXqGnLFDGyIuodnAXmpZTtims6JoRT3eb'
        b'mo135cVwtU/sTHtWReygCe7LS+ws7l/CGE9QfBfh2cSt7cSC2G48GL/m8Rq7zM1Ok9d9MJap4Cw+wGLZu0s6LGMsqXhXF0u6CqU8DgfMhhO947lrIuWOXpVEaHNKyZSn'
        b'sF2TzRjVUzwLcULVTotvMqNABJbdfnWZIZNX5N6ysIbjO4RAwlnLLrzLl1rE3kyypsEyKJUz9bEwcpgvwodaYPzM3E3P4OEIWyAHMvXwrnYusXYoTe5gCwUO6eAcxWoD'
        b'FgtR2KEJ3gVljgS1wEKEbursLkLXRhDEyLAezmzsdhla8H5X3GPeBt8Z8gBYoNYJi/Vm7pVlPVRwBtjCQ4MxQO0avoDjgmhaK7omom/cs86H5FDfj6ssWA713NgiqKAV'
        b'3KZZAYw9VHNovMgdTnfREmPUQomDMmIpdPBFSXTg/szHa/s4HOxOCKE6IpoEVUIM1miCtEPlab+L+XGMjVVkdrGxOjhpIy4gPENs6+ZjfOnlt7wQKJ9CpRAE91RbaIIe'
        b'cE6NB0k8Nli2qwjQq+QVUIL7oZaDKDRso8iSTV56IsNMUmIHtuI9vAf35LW0bzjeZYQQLhgcfHAKHrFNpKJkC17tiehylFxldkbgLaX4NLb6YQMfq7V7BpENBZyYIRPv'
        b'Yyo4LK+gmiVwk1jlmqUOTomnoJyvVCzGupzuePQkECrpXrQ945HCpSody3kzrs5wwOKhgAMjZRp6JozinrmKl0dSr3pAF/vUlXyUykhqt3nEfG4jAxufYlRWhQ0OLrty'
        b'JEesmXBjbZc/zU9GYL0Uj40agpBW3rHdS0iREPElVX/EwXyH6W3TmC+3vODuY8wq6RWKMyS47rpgTdTipXB1omDGSic84k4Mik3FM9SFOsaYt9KMy5QZ65TyEnowB1so'
        b'Ym4oiNzL6/G4Wy5PKKvxTuATKTNUpxKmwVmVzw6oHRrA+70ezyUQtZZohTL6S/1eJMqhfEal6prmZxfJ/vaEWg7ZIXhaBeVb/bg3kXAcT3IGbzc7GDyUi3xW14XPfgw/'
        b'Jd3owK8ooRnOUPfdtkxXxKk0swIox/Il2BI/m5H+AD4jnPS3klTgoda4ZFgEz2RkRY43lWGqqQf9ElZBiWZMCuE1jwzqI+kA4seErGVyPykl3OEYq4BLRCF6J3NuhiXx'
        b'XUEhcJNlNvtInpEibVuwzZ3MSDKbrbcmyhxlH+nZqr5hESyP0ghsVVKA1GEznAiXQSTbGdsof4QwQUiMoAHak21jWc9uT5zrGKmJ4fJ4O3jASDigxHtbM/ky88ZDVmzb'
        b'JsL9KDmyyvDAKjnO9xE9beqF9T0XPdiVuXidoOdskKzdD8+ge9u2qQW8LQPdkU1DbeNZST00S3KHXEhedlsSGSW5rcTW5cRruZQvpJ494CoMr4c5VNgwQnE2iTOwZACT'
        b'YUFwwqHC4BbWy8h/dMl6psL8fLpUWPVCWfuWQi1cYCpsDnVNlmFPk2xhEb0KjlqfBJ9r8ii3KNfMpTFuH8a75sxGhQQbXWl0KDb/kdyp2ABi2202BaFdoxw15TOhmNuP'
        b'hPaxDsC41GUfbjxGjCi8gaVJspsHZ9GCb7OpcD8fO6IVFVOg2RbCxoRxhWvd8UcU+HaP0Ln2mHAKU/GUilb2wVx5uNK1NJA31XBxmxxBJ0nin5Up59lYvNJtcRPR5u7u'
        b'N/a0t1YFRyJXcQ/doH08yVKRlvdRefTPQgvNmi8PbyxL6s5WY5Z0Q0R3roqN1Mzevoi7tdJnBZO3xPnuO/QtzeJRGa/r4EBS14xsGN6HPXUNXQg8VNFslK7m5kKhcRHZ'
        b'U1Ef7srisx5ubJV7aY/K7ZX4xBSHXwOwYlYytM8YCAXTFYRSLtFJAu+lGk8u4BI7kedqJrGhCs/JwuoYccDrT+iPLvTWK7fCQZoae5ZM0W/hdWIoTJNPxw6HJiciXM5B'
        b'Z+BQ5RMUqovYcRIRpRACbaocvDiLQ4XnVmghEa/OSZEtnVnjxn1KJKLQ8uQaviyv4TtKCs9qvL4EZJ0Ot/biDbYXsH6lYytgKTZyOzYjHOuXGzpE40NpMeS7h8Fx7s3K'
        b'sO1aJ/VsqJel+/mxJIW50qsbS9j1BG5dkb25poT7tDqvrdBxI8uXxLHNh1Jb1+bDoWHcSAKbye7BsU7oZzEFaGYaVnMjfkvBrrVKwXBaBuKKZ0fI2zxXp+BBtoeBTSSO'
        b'5V0MqBkjY0VHDhRrXdQWvld4hwAz3o0PjxXuPqPNlYi32amgieSQEQ/IOaKdKJK9FxntFcyEhF708SHcepo3r6QgvaLNVZO0Yaz2MmlX4jnH5HAuxnxF/8sS2jbgEQLA'
        b'EszfgvUbBPNWElV4ZIxMc+rmwB1trgovrXZsv0CJlWdX93GMjfUj+FWDZEl1F0qm4hWSCZCXyYdgpHEg26/x45uYbL8GO7w4WSTaR2zzCbXeLQI5LkBzHDHcCpUVTqyS'
        b's2sdtEWyXR7fdMcmD8HuQ+61Nh6K2DbPggld2zzXoZAL9HU7FVp3RRAD+fuUhOHeHq564E6oT3dn1lGc9xRkPaGuTkXIfnETdxsOICe5XfPTg2BcMHUBpWrbdEWsk2YG'
        b'VBIZYove6kcj3Vc/whVVMs1DFGmGwuChpKPgmqsMcvbMx+Luco8lIO9jwHUJSvdI2aO46YChFPv9TMlVOZwKJSWcd4IDpFtYevR2ie4HVuTQm6vUStix21leO6fxEJ7r'
        b'Do55lC57wlDP4alQEREqg3t6Jz7jK7Fxo9Zdiae3M6YnUK0Lel4wEG+rtNiqgNZxciDWrY2Sw6RsvpEKlBsYZ2/nsDqAxxycCJ2ldRaTaFnzqbvoOZZf9x6j0dokvCbJ'
        b'y/MEFqyS9TseS9NapImbHHt2mEeJji+bokSo0Vo0WAgt8uqogQvr5fgt8VoARQR42Mr3xjvYJv+5ZXwQAuPGQJE74yVQ4NjQg6uOqIQCvgMoQdtqKEoQ1j6txtokzNNL'
        b'3OqzoydjUeRKLFZiQ4CgxAeE/Vi/Vaa/d/ASnonAwki1IG5SDJIm0+Jo4puLgavgYARNYzuW0kV/PTuech1AEf8wWk7ed6Ed7vlHB4ZJUKYWpEXEAvFQzPIUdmTU9aMW'
        b'5PMkfpZESoUdXbEjK3Z8xY6tlHbnNGfHgZVUIOUJu1U7nXdJ/MBKxQ+ppD2q+B6ft7ODUuW7fxEFwUXX4yeUHXVadIYsfsapS8s263INGaZUk3VHUK+Kvf4Il09Y/bZm'
        b'Z1mz+WmpX9f5qs5E1nINpgxDcoYxgBtcYTRnOhqwsPt6mUo2ZG3VpWSnGvl5K7PK7VlsmV3nuIaUlGxbllWXZctMNpp1BrOjijFVZ7D0srXdmJER5NLr0pwcg9mQqTNR'
        b'M3N0q9Plo1x2xpvcbSWovxuSTSlzWDc3m3KNWQHyXczBJeGhvTwwZT3RI/aTQgNjfMbKumA0pKTrsqmSud+GeN/MO3o2Zu1yk4byp7djZafaDmtBuiibxcr6yMY9PiYw'
        b'ZOqMGbrFkbFhi3XB/RhJNfbrm8WYY+CO+bFPfjojLQ2bwWrkh+RJSavNNmNSUi9/n7Tt8F8ecb60HH3RxZuyNmcYdcts5mxdrGFHpjHLatEtNhsNfXwxG602c5ZlTneL'
        b'uuys7kUaQFeXGzIs/DIb5O0mS5/OPHFQ7iT0PaQdGL1czprtE7HFso0dzpRh4WASGJOxgh/AVngNEyjhTHnHN2lekucYQca22hQCuiIoYKG6XlgPF/byytEpLgJhmVNs'
        b'yPbIX7u4yke4p9LchZGEe4+SciN/s9BD4A1GQuUGi1ZkUgBOWxnpPoNX9B4y/2qidNLuKA2IpsJxcIyjTyIU4B3LdiUVHCfKeUOA0gVwhLukCIFyiwfrytkgdnpYtTOJ'
        b'w2rWs4T+bW4cbTfwpDvYs+tUrBFua82sz5dXs52bKuN6GXAfGMdoc1gjjZQxGSuhhJTHW9HDIY12GytqidlJeUYE+fpiKJ/GzhQFhdMWppuvZbrx61vxUi62WfgWqH88'
        b'iZ49/rzxnURfbrCjRrYNteEZkk2r8Cq/I805jB0zMgGNDU8LcGzSdBnqDyTCKXbIyNIDVJCkpjRQks0dXg6VROP4sNyicbxNRZPxogy6+2mc2rGNd/N07Bq2Q9mB+fJJ'
        b'aPMmuG7ZrmE7d5GB5MM2vCEPwB0sxquW7WwCymcy5lOIBzz0Sn6X92584CgiGr+fnWUPlAe0dDK0drUE1aOoqcUW3qdpeNLP0U4K27ss27lAbucknI9k+4esBM4vpDvw'
        b'xly9KGea1vFCV5kPnmZl1XCXF2lGYC07XWaSCg6xbHxqMlzhi61SKT958SgxI7I+I1xerkqoGBUyhSxBxW64JSSPxirT8YkvqiyUI4TEgr9Of9S6Url4gPqdk9Vvza0/'
        b'XDBkTGWJR9KciMTF8VLROrcDztKbqg+XrFLh+ZtDs36msaUtvXXn27TN33VUrhv7vuv4v8a+6636rGPf3rzz8xJWuHt9brWMafIY5L+lumrW6y3ndoVoPq3Fr4O3/Htw'
        b'7m2nWzVvLlz0xf1HC47NfaXu3Oezt30+bGLO+Lr7Az+b99mVNW2jDv7tA5/P82xXmt/S/P6V31/8vfYr/69Cvrzwdey3v+6YPvTSuv+a17pafKn6yBv3X/40tDJvqXrU'
        b'b33um//2bN7etmfDY783eyzx/Lji22/cb8U+eDr+u1eHmiI7Zk7927zhv8t6/he5KW/UTXvqzXG1zeCqnvzwUsbTdcdi9Ror36+ppsi/6h84Ey74hgWKghpOiYFYlWL1'
        b'4Vl/Mp71DwoP8NMnwcUgLAtgcsFbJ23Cwk389nlYvCciJhAORwyM4eRAGydiac5TVi7yGo1+7IkbuBbuFxikINsHxBDswBor38c5QnovH9ugbojj4Zft8sMvuYF+WDhZ'
        b'FIKgQ4U3sHYFNwa3x1H9oig8B1UB4ewMWj1NdMe7G61sM2c62l0i5NuhlHEeLONMRvDCfCW2w75svdgp+urZKhX0zvztJ78wDP3aa16aOXunMUuXJj9fFcRS7IJOFw74'
        b'iewPVs2SzEB3r6SXFE4K9uuuEBVDFGqF9L27qFaI37uIEl135WUurI4ofueiZHVZWde7XEPcN5jXZVfdFRL/56IYKboqzJouv/TqTok13qmkDN6pceTDToklsE5NYqLZ'
        b'lpWY2KlNTEzJMBqybDmJiXr1P+6uXjIzeDez523MLLbM7IkvM2NovNnjrJssHIX9Iz9ViyJ1jr1KCvV37JVviUL1sgFsOvAmtvEp6TMdeVBKsMKPpg8OtkRQkRmbsSga'
        b'S2PCVYJ7jnKWEx7k5TGQhzURcG91ZLTMLxWCdoOI16KwTIaLk5QSGruJKdaHTsZjXinKHimQdUrTlQLnCN2PRUlpkoNRKguUxCglYpRKziglziKVe6T4Hp/lR6DefUPR'
        b'l1HyR+Z6UEpzdqbO0EUCe9O93tSuD3Vb/Q8Yptm4zWYyy7wix2gmlpkpE6Cu5/h6U4CYLmZAjvitohZNmcZlZnO22Y8bM1BJav/EkfnL3JXJY99O9MuaHJ2S7+jbw/6a'
        b'YFRzeYZhs84kE96UbLPZaMnJzkolhsQZpyU925aRyhiUTIY49XXQ3f650jIT6/JjakY03KALDrTacohyOQgYHzVijr6sRgBrSP8jzEn1BHNSRdvm0mddACmefp4RPOw1'
        b'INJvZQBcWi0/MMguxUSGRykEuAyHtbO34cnVpi8//VRpmc8sfpHyaVJQmr8hrPVrQ0ZaRvIfkjY998bP3vjZEbhxZPahpuN1x1vzmsJuHKo7NLVEX1V3aEzV/hAfQf9Q'
        b'e1iTqRetPNRqoN1VS1qdHMHiqGdzbA74HA1tEgVVBzZY2UMcQz3hWkTQyihpQkA4lHTF43C4IWXRjc16sRcC/BAMchjo1MqPiT5GPXcZ9VKdFIMUMvKZPboRStXp1LWq'
        b'OjWO9SFDjCt7YY9x9mpdaWaPiJgHsBfnbuhh9n7zGHoGXeoHenSMSBGNPMQ6qoLLT/QUSiP49GGLhtR/UR+N3ISVkA/XiYWeDVA+HTENSrfBVWiAjvVTXYRkLHfD6qWT'
        b'Hee/2tXaXHfifYxzHo3Hy/gA78kbAw/G+2tzt7GiAmHYSjwzBBvlzfszeA+PWvCWR7BEtKdWELFcMcRPL/O1aswXLcE0YIpsxrCIokIFXpd5Man2Km1urppMHhTAHoGn'
        b'RugJPtnCxH16fTf4JaycjHmb+BM9eHYs1EXosa2PKF+4SWaVbXgPCvwJUhWCCKWKcCgNHYjFT8Bmt3JYwmBTyYFTfpJUtDulOXXDp/ST4DOf4PPbHxLkPO57y/EfBA8G'
        b'NKz6j8vaH1Cb7Ob/dbGZksHdshitT8rLPg6ycclOSbERTmalPOlol8BcFrtYF0p53sxwdCnlixRrtpkkY44tOcNkSSdDyTt4TQeuh5IENRsynrC3hMI1qIdvBjYpNv6g'
        b'uV986Gq/AHpbupS9hcasmkrv5J7fkuAlvCA01C/gCYs9+kTiNbtfmcw6ycc5RxbHZDWVQfqOnD4DyH5+UrLstpid82SOZD8/LU/2mrx/qTpXCP2pcw9S5wylJllS+s0x'
        b'kX5G13+QYwhc7nJRZJ0ra/hHQaZdl/Yky7L8k82DBLar+s5O07zf7FzrEPYd2jmk6y/DXYELe8z34ziR8AxeZHqf9HcjAbDoqXDGfVDFDR1fIut73SCLa+y4hYTh8gN/'
        b'dRO2hMCR2fRxqjB1EDzgV0fMhfMh8dhIfQwWgnGfgZu4NWKAQJg969G29IAP5rgyE4O4CTiUEwIX2cMlzIjvchnranVPkVzYh4eJzcUKsWa4zq0cc9PKuw8Tdrh+Ge0n'
        b'rDbZPxumtDRT0clXV00o7XCHKa75r5hOPYLnfrns9RdGWN/3ubvmvc23/c6vdA1PkA4cdPnF/WVfN4y/en/XR5+vn/TB9Hhl3T7nhYPe93t1z+88Lx9d8MWNc3mDTn1c'
        b'4pl1YXnt/L/mTxt6/gOf8sMD5/qt7Rhwo+pITNULaz9PlCpe+27K5Y3p41+e8+GWMa/PzXmQ05LxXkKH1TCi+tfC3uKNS4M07Z//Qf+bf3vr1B/X/vHcyqv3Xrz5i/ej'
        b'8t77WvP2nGDbb+fpnaw8GZSsyPGnWWwOfCzJ4G6idQyVxeZCCcv2WL9bTvi90/2USdZJzML1bLQzeIfDMUydTaYqgax6xALi8FPxrJoyIzywsoSJD6NhnzYCi/VkC27j'
        b'IdmeF9glJ3wIp6wsB2XCdTxGQm8E3qSMkatYjFfxuizyLu6Gh1gEzRvw8OQY5u4e0Q/tcIV3BVqgdBAt4tZpUY9Fm9XTyql/GS2rKxHR7lgSoe8Slx5TlJuT4vUKmQo4'
        b'/VMaTSYnzrIio0TBqckUmZrslWkJexVJTLkqZDHGZBWTW2Pp3dvxS+TF8zF5eSyGOpUE2T04y4/pKGUPHTW4m8cw0396zGOGV/TDYxhfg4bspxyKNncJlMrqeiDalewJ'
        b'PyjUKzipmO68qWvPvmZF1559B5x+4nsh3QJohsAFkJgmdn//Q/GTvv+xWa/8+uVeULZKhsIf4PBpnILzpNtzR/x/W/T8IBZ3jVRvLFZH29j3tXbNxBYHFk8gItcHjv8B'
        b'GHuCXf42RZbOYsB2eauVbaxV4FV+DI8nsB7vU2hhYRQWx2NB5DKsFQctIxp7EC7ASfqgF2IHaOAW1uBF07bFBsnCFciibz5NCkjz/2K9IcyhHdY9136krkIRFnJhSmBq'
        b'wJAgQ7RB/aspQUmfJK17wfvF534rCrGn3FyaBulVsnI4khPHoaQG7/WHJXB6j5Ut0km5cNQ/cDS2PUajOXDeyr4bFgFH9f7k2U2+R9Rzg2jjKq46sGoDVGqxdJEDX3pi'
        b'yzFotzKuOjqXqCpDqZhF2Ph4E0nCu3IIiv2GuWaz0dod5AN4kFOYj3Fy7Ku4KMxDum5oUsr7GP3KjSaFXMiDk93iTaFj8ebBKex3/7if8OQE+9woPBEBd0Zyxx977T/6'
        b'R0JPtAv/dOilUehd6rVy43MyTFZLd3zJpxEURDp2Nc1s2MxPF/rEWle8GnTT+hXGvSr7hsYkRK9etT5AFxq2LDQiPiGKFPPi6IjE0JilywJ0i0N5eWJ0QtSSZav0/1hG'
        b'9xdWPHV/NlvNtm1zFOOTXAdmpAi2WXRx9xaoZl+V86c1Q9EVF/ZYw2C5Hppc4OQO+g2HwzvYc2/70K52gYKlIfxrfnA6mYRTUZDH4/sppLgCHEX0A85RVNWa5kd+L1pi'
        b'qPrTilSvX4wZtE83eNmr28eszxw/5MMhTmm2yNpz77+4fWhLfGvN+9NsHbOWRakPThqfcHLjpN/tioWXDnqEb/nZJ6uL55cd/t47MDfw1Oseh+oG5vuv00s86+2G4wv9'
        b'u5M3XMJSMRBPrpX3VB9ELtP2jgbfUBYP0Ah2Hm9wy4x3sKg7YT4zR3RXa3iydV6PtyOgDY7whO6rFpy9RaiDw3t6Cej+A8aFZIelh2Yf7IgZp6lsh9GJ7zCyd/Pw7vuG'
        b'9rXm3R0prJJvr0h54wcSGVbBoWH+YQFweY1f9GM9PgTuSV5bYb9elu1YNX2hnMmgMIWUedlkKJTDavheKX11zg9HlWNHj3/NsXtH76dGFpOkT/fd0euZ1/jWV5Yhk4uf'
        b'ftIZkz7sRC/HSBco7fVOMOFyfGUYrFZSMikGyk29jfIsZ0iVNw2f0HC9bHXruR+Tc7J8+/81zSr6xQMneVsNDo6a9AOS58kcmwjHu9PsYB+OJ38f4M0VzxT3jEkfRM8W'
        b'+GbNOmyQH/qvjHMkXziGlfKzpOVYOKRn7u2TeNdullNv1ixu3pDu+H5vmlNq/Ohpgun9mnqVJYFKtjxawbNxdy7+fVJ6WqThl2kBg/6QtPG5N37WcmRqVV2eISBf8R9L'
        b'DkUPeOkM3D/Suu5a/oSDqis1w67UJJTXHVc01txUX6kJUQoVf/IaccegV/OzjRwdHHy8wQcXDX3SdHmGlX8B6AyUD+zB+WMolthYEtZkQXWUSpgZrd6DFVDGISqBPrUy'
        b'jDLgkW6NcXCDdRSzdHQ01vsHhROVrOuT1uHKLl4Fb27MYSiG56CjT17fg3VWhsR4nqhFR0S3K7eg1uEO+TIayiWsnhjdRfR/bMfRlWd7Wtcsajh8DelK+cuciM1TyhdZ'
        b'2mefzCO77tUrO7UM7xKzzYwq9CAA/bZHzvh0AxwzMqcnwA36t34Ajinp6XhGHdFnxB1dhJPpWI1NeE+vjI5erlcs14vRy00hSweoLMvJwTNvfZjwmibec7G3+p23OiLC'
        b'nJ6WWpOzGxvfiItr3R7Xuu/L6ft8XZ4/tP3c+J3b0we/9Eac57Tc7+v/nBlc/PJL8yyJb3VEHspTfpl1dERBxAtZ9Q9f3mu/NLDYzefER8lVe14O1Mz9dldk8Vcqf5XL'
        b'JdWSqD2lu99anrg7cuzIE6HXE77Iv/CX0bfHNsR6n9gzY+anqjnS2JTXQuLyk4+dtf5ny7ITi4b9Mn6QV9Ui/6lH19Sdil7iVl2st/o1vPpJ1eKtUytehow5Gssn8168'
        b'qG05EgTJG+wTrPrjr+4MiAmvaVvy56cOq++6XP5k+JULn/59zuspysznl991Pm3yvPXo6t27bi9Z5+Y+qn5j2fYUj7cuf/OVYeH8fXn6k1/GzMnH4rKzB0f9fOrOkVe/'
        b'kKJfi58V9btH0a98fLr2128/G732lffFjsZs5cZzcdZH0dZXf/Vxw9qc6XtXeVyb+qB0U6d9z3B02+l5++PMN+uU7RGB32Z9+vv5HdsGfPWJ0vXVWYO+GDMqbsX3udce'
        b'dHz0StqELVOK//2ZA+Nr3hu2/C+7ph2rrDEndL5QkPbqpt81ZJj8Iz543ykFZwRWzgjE4JBfrhl3/bZickDChIwPjzcoj/8ybO3663Etqz463j7mduRCw/nyiXtmq0qt'
        b'xzy3FfqEDL939/mI+yvzv/2+wsf7z27v2157Ljt3+TmX7L/MeHvgF1+9//Tyne/V/tdX3j/X7Hp+UlaE5U9l42atf8Gz8Ezwfwd7/+qlZ4NnHnwl/OTb36p+uzTsz0F/'
        b'a25Y901h9p1Tmz/Y+rbF8ubWpVF/f+6Vv2c4nVuWP/d78cD5gTNz2wgmGJiOnb2VEqgiLlBQzGIPdl/FWzLhqJodz0IViqCyT6hqx3GAweYwPPYYYXrCyzA4gc0zFvOz'
        b'Xgka8DYWES0pCVRjvbeg3iSOc8JGGRAu4Q1s8cd9ULkyEAvCI6NVghZaRayG61jFq6QSVjVHQD08YABPlbA4nFVqFvFSeNo/eSird//nznB/0I7KzLJRvy8ceZwSEzOy'
        b'DamJiRx1cggRxHGiOE2hY/sJ36tFIk+ik1J0ERUEDt+KGnaAyw51JaX4rSSJf5dU4jeSWvxa0oj/R3IS/yY5i19JLuJfJa34peQqfiG5iZ9L7uJnkof4P9IA8S/SQOnP'
        b'0iDxT5Kn+EdpsPgHyUv8VBoi/l4aKn4ieYsfS8PEj6Th4n9LI8QPpZHiB5KP+L40SnxPGi2+K+nEd6Qx4tvSWPV/SePEt6Tx4pvSBPF30kSxU5ok/lbyFd+Q9OJvJD/x'
        b'dclf/LUUIP6nFCj+hxQkviZNFl+VpoiPpKniK1Kw+LIUon5Jmia+KE0XfyXNEH8pzRR/Ic0SX5Bmi/8uzRH/TZor/lyaJz4vzRdRWiCCtFD8mbRIfE5aLD6UlogPpFCx'
        b'Q1oq3ReXsZF5/M/pxoDoAYoBCnZUJCrdFSMV4kJXxWCFi6coerO/fHmJO38d4KQYrjCP6oHnYmJiDxh3+3+ff4V5dDfms4aYMubceOLbP3DChIUiOzyCMixjPAQO4z5f'
        b'KNMI7sOUPliFHaajf4+XLFVU8903FgUWRbnAlMH5H10wdX6dpxpa+LHzvEMrcsYEHVyx9rUSVVxn9ZSXAk+dPlXwYtp/f+Pt9XMf5c7I106GDtblfRFs3JI8U4x6fWd9'
        b'+4fZXz318q9UmZmvejXX65a9+x+X/zOg4J3C3G+e9433es//f4Ji5pWf7Nx7WjMv+tXALz5ySrth3Ri3zvKSm9v2Nz9/FPBr0//o5y8/Ezc98UKo7x+v/kbvJiPD+bix'
        b'lK8a2H8dERNDvSmO0FA8XhexMXQN1/dYFoF2xo9abVtZHba/NxDvK6EuZDrX90NG4Bl5KFjSgxK4R3yMjcUg5Sh8uJdTDbUztEaER/lFaQRsgia1JDpBM1RZ+bNIHTtI'
        b'qLnDxZUqQRHBtELRQiv7soOEp6AFi4IJV3qxQSidHEH4VEqZtkwprIBWDZQ9hcfknczjKZlYpM7sfYdaGLpU8iPsusIrQfOsOdiGxYQ/k/22BWLtKhnthtskOJSOV7nO'
        b'UsBBJsFoQLBII0iBCig0wNXdWM5NBMSLPN8zT6CS8M3hzQg4TRiZHsAHF+zYDm1YpKeKfKFswPJIheARp0xYbeD7L1jovxyLlsIDuUoA6xpXrApBhzdVwjy8KEPrNbwC'
        b'Z/yhOjImAAu5VzRN+EAkNM4P7qX8fP41oPgvfNErfwhVTVkmqwNV2QPkTm4u8qMuSpHeXfkjL+J3TpKLYztnvJKzvclmXTcajO5UZhizOiV2QtSp4jsanRIpI2unlGpK'
        b'oVdSZVmdSovV3KlK3mE1Wjql5OzsjE6lKcvaqUojWKc3syFrM91tysqxWTuVKenmTmW2ObVTnWbKIM3Wqcw05HQqd5pyOlUGS4rJ1KlMNz5DVci8i8liyrJYDVkpxk41'
        b'12Qp/HzbmGO1dA7MzE6dPTNR3otONW02WTu1lnRTmjXRyLRSpxtpq3SDKcuYmmh8JqXTOTHRQqozJzGxU23LspGEeoxycmd9zGwf0sw2SMzsOW8z4/xmNnJmto1oZpTb'
        b'zDa7zewrGWb2PUgz+/qDmekcM9t6MrPzAzNjrGb2rQAzO6Ixs//wyMy+jmVmUWeeyV7Yd4LNTFab2VmCma1VM+MJZibRzOzBBXNwN2ay6XDpwsylf3sSM3mNr526Hpvq'
        b'HJCY6PjsSKxfD0/r/V9W6bKyrTpWZkyN1juxp5hSs1NoZOiDISODEoDOsYSYGKDrLjQJZqtlu8ma3qnOyE4xZFg6XXsqU/PCrmHs8SKvw3ny/4u1gMlSCzt8kgRJ7cTX'
        b'2uAIkSuK/wug3Hk3'
    ))))
