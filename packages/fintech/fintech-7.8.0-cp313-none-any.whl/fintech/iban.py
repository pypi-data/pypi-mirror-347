
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
        b'eJzNfAlclEe279crTTf7vig2CEizyiKKOyIKsqq0cQvYQgMtyNIfjfu+sYPiAi4IrqiIKEbcTaoyySSTZCAkAUkmY5I3LzN3cickcca8zMzNO1XV3eCSmcl7c9/v9Ywf'
        b'fb6qOnWq6iz/U1WdL7hRH5Hx73fr4XGIW8zpuTBOL1gs8OD0wpWiRZbcc5/FwkkC9i3A+EajgLeilRIfbpLxzTT4lwNt44QrpT7cYrGphVaw0sKHW2nmoOTyJJb5KukP'
        b'ufLEObGpyrXFOYZCrbI4V1mWr1WmbyjLLy5SztMVlWmz85UlmuwCTZ42VC7PyNfxpro52lxdkZZX5hqKsst0xUW8sqxYmZ2vzS5QaopylNl6raZMqyTc+VB59phRAxkL'
        b'/xRk7O/BI5PLFGQKM0WZ4kxJpjTTIlOWaZkpz1RkWmVaZ9pk2mbaZdpnOmQ6ZjplOme6ZLpmumW6Z3pkemaOOcSpPdWuage1TG2htlaL1bZqudpRbaW2VDurObVIbad2'
        b'UzupJWobtYtaoXZXS9VCtUDtoR6jto8aS2Z6jaxobIbnyOwVeXlx6rEjtNpr5LuSix0b6+XLeb/gbS43QzSOyxVY5qqEqdmj18wa/jmSoYrpMudxKsvUQhl8l8qEnJOV'
        b'LXxbVbhkiYwz+MNXP1SPT+JqXJmWjBrQ+YW4AtemqXBtojo9RMpNiBfjB7gjnLbvDLbgWh29QIJVwa5p1pwhE16iA+j8PNxtab0wAbjUJKoT0OUAXBG8IAXvXyzDlQlq'
        b'4FiH64OgB/jbg+sSUnDdkoCEZFyXmpymDoCXFWHQ38KEBeqAkITEYAG6KObKUKVzdLrCQAaN9kTg68DczIVyALbVYXbo3sKE4CRcAz0n46pECVeO6i1XylFVtmDUlNiY'
        b'pmQjPGZaZ8K00NUSw0pJYSVlsH5yWC8rWFMbtW2UjXGlBBniUSslhJUSjFop4VNrIogV0pV67u1Pr5TiuZW6wFbq6gppTo/Ajcx0ckJKCkdfBloLMzI48m2V1Zt289nL'
        b'KfmWERFCJbxbZfWGdh17KbMRe3whsOO42ausniyx4i5whXJ4vWyZu/ixAzd72HFDzm+EN8Ijkm5xhcTozxQ0C7osBgPks1dFfBLxP6LXs9e9+m9tD9oK4sXpjwT/5WaX'
        b'8xk3xBlCoADvVW+D9agOWxgQgKvCEkJwFbqQEQBLXo92KoJDE0MWpAi4IlvLGehMsSrU4EzaXMVH8C5+4korWBjcxKHD/rjS4EJKWnC9JY9u4Gq9BKhqDlXgc3YGMjH5'
        b'EfgCvwSf11tAQS2HqjKCKDM73IWqeGe0E98gDBo4VOO6nDLbIMVV/BbcjOpgTnEbh07gG+ggbeSCHozjlagH1Qmh6BSHWtC5BFqCDk9B3XwYqi8lAtRDP0q8nwog8dfx'
        b'2mB8VQrvD3GoQY476fs8vAc38znuBtJgP4eqCxzZWBo9UAOPutAla9LkJIeacUcA7WSzAF3nHdF13E0kOwLMUOVaWqLE7Qk87pqGagiH4xw6iu5b0xJLfBv38GjXOgUR'
        b'uRW4zUUXaEfoBNqPq3nUvHoduHV8mEN1+Xg7LZKXoFoe38KniaWTRk34At7LWl1HO8Nxt3KiNZHhModO4v24iXYV742OKtAdtJ8uwiXSqtGPjhVVrgCJqjesgZUTyDjU'
        b'GWfHxnoB71nOo0MT8TWypAc4VD8L3zU4kaIbC/Nw9wKxQcRm+uAc1EoLJuCDUkVuOe4inVyBJUhEuymz9XgfOs/ji7PWCRmvKtSJmH6MQVfEPLqCzuMeInUzh/ajcw5U'
        b'NCcB3skLtbbGBT2Kq+INrkTkc7gSXcLduDZJRsrOcOhYMGqgbfBJVxfcPT5ARkQ4DyKsdaeivYwObMXdksllEtZJPe6MowXofCQ6CJMmsJKyFieEKQawTW4avD6Ku2FJ'
        b'q6lStwMz0ItbVASpDp8CAU5uwFeJ1KdByWDCTlCOY6w24W4nfMaStOrkUFsAPsnkrsVHFgLH2+iipXGGTsWhK7Q34L3bFji2omZLMq1dHDqNTqKztCE+lwKa1o13pBqM'
        b'ercfncJ1bNHrUTuZjDzcYS1gDU+FljDFP2FVAq12eeFuUnIRpik9kTKc6g3yAj8w824LpistaM881ll36CoFakZ3cZdxACeg8CqbrP3loQpUgw/KSNENDp3lrY3ig4V3'
        b'KNCepfgaYfgKSIG6YEKoiOfxLlSpsAgql7C+mtFxtIv5jV0pUgW6rsQ3yDRehb6W4i5akiNBOxTZ6DS+QYbcDcqMOmYwdmdwi16BjpXgGxLWVRtqLqZFAnzMgYeQdquM'
        b'yFfBob1oD+phPZ1y81WA59jNi9nUN7miiwYPKEkMi0XV0bihAAbxCqqRcCJ8SpCG29F+OrS8BaCr1eX44KqlqBZVSThxvgDtWJpj8CJc9/tb0kJUG4EbWHNLVCt08XGN'
        b'RgdVIqqTtviaJa6GVS0mJnq5GB0WGOyJy0fbnZJAmtVgQvNWo31r6dsZAeh6Eow5h8Mn8Kmc0EQ689NQ+1oeXca7zSPzi6IR3h8dwo3wvwp0KRpdkGhSQMvOrIlDp5en'
        b'cFEatJ2XoEM6OZuCZmd8ng/FR6kRVHJonz26biDQT7epFDciCPCMTSc+hA/Sr1GgWofE3BhcK7ZE1xLoJDtNw5d5fAym+bqAuec6tGe5QUWW5qoDPgzC3MA7SXN0A7UT'
        b'Vgmo08wJ3ROLkjV0THH4Cqrgs9Bhc9CI8TMEkR7QPdDMRtyCqphAl0cJ1MEEOiCW4su4li4RvoluBfL4Cr6GaohDaOFAwZrAmVOZ2ifBuBrRffDDqAPmyMwrgkgHvEJE'
        b'+OZ89ID5tjopusQvm6MnWrKPQ7td8E06zy+tn8FmOWYRTBCdZ3R3jUKJq1H7EkdugdJCEWZU6hjUNgkmCB03Rzw/3EFDqwDvMDAu+U6jpxldwbXkz0UiT4heUgpLf5Pq'
        b'TjkG2+bT480x8qUQQzC831iKd+NG44BqRauZOGAuR2H1UbVXACx/Ar4pxa+MX0+FEqOr6CiPzsjxNTpMiGqiKANAC04/aQ3j5B7GJocsl3gR54m7RbgrPsrgAJV8xCp+'
        b'ootcyBbqEN6baIiB1wXoFu5gI6KLXfvsarWn6FcQITtSpKtTuFJ0RYZuQdSuZpZ8LxHf4VHdElQlZn4Nli3OEEqK7iaKiFSd5gUToQO4Eh9Ce3PBzI5y4fikZD1E2Tp8'
        b'DXfTqZozyZn3cxnBDKVohyGQsDrlDjwax6GeUcrEVPIiU8lGEb4Lq9HNAt8VfB9f5XnUakNGexTUEtwKVaXNqAa9Aqp0HuDOc4ZygenlPrHFhHzmSI+DoJf56NBRaOUC'
        b'bjVMZBp7LBrdRLdNlts5aupGmUvUJgl4/sMTmGSnLOR8Aj4zAnHwbtRJ+YFLvTIbVYaZHcGIal2inKOYrkfgeglqLVtOJ6xQu55HjbjSjItKV9NhJkfhezDKUw6jbdi0'
        b'nmyUl8Uy1LmWDfMeQPdumC4YjBlJZWvYKt5BPT5MplWzR0kFTDvYgKk1h4Bb5cX5DI/cilzIO7vgqxYsUB8s4lnwPAhx8ySPD48zozLwETuoMYB9H1/CujHgy9SM8EEI'
        b'VhuIuqC9SnQKLDQF37OIWLyEWrl8JuBI3OhjhnGobSk10JmoVo6urH3an4Jh4V3LA6LZ4Hl0UgYdXsS3mVwdoIDXwdw3jUC/AsCkYSTMBgYwTvgMPk1W4ll7N47+sIRH'
        b'OxCLeysT0DXAQ5tYYD4B2pcAOsNmZs5UHrf4mtFi9mSq31Hjt+GWdJPIl80hIE4Ji0h8UxpusQgFVblKtSgaXwfAVYMqzVgMX0WnGPK/n7+UuoIYZne1TH9GFo1OQCi6'
        b'I1mTbqATuQlf8udxJ2pfJ2ErXxvEdAi09Byux41x6CR1UhefCykTRPhOIIAYNon+njx6AGMYAYHXEDM6sMbWMty4EXeMuG9mIZcJH098QwTm2I1OMpeyd+5K3haSjh4B'
        b'Q9sHcTNuprKmb1zP4+a1ZjgJuKbOEEHaHIXp2IPvgJBPW+OFZ62xVIKa0HbwBhRenZ2B63gw6rO2AoZCjzuEGsaTVEwzBTdOnzfivcg3U7QRifCV2RNYQG5dLMTdq3Gj'
        b'GcbC4hgmQEnYUkuQ5bKTSVueM8DTYoty0AvK5fRiRwBzV142Y17UGGOIIiW1MRYjQ7rjNmpU9KUYXbNKiZ2LLvtzenxIhhvwDiNS2JMDHXVzq8xwGV11ZfPbYmcNne1G'
        b'11j0Bz08vGITjZCeAi/obA/EJdahyXbilBIuCrVKAMFdALzhwlxjzypgcyDLiqz3WRj5BrSd6uAcT3DrZ0dC27NulrrsSHxMgg5MmkKVRw5YGITFjUVmCA+uvpNa4EpY'
        b'/6YRp2gKskZuIhi/g7P1mkmChRKLKSsBAtAhtgOS6wCGBw1m4L81iwpXvABfS6LhDHg8Y24Qe9sWQtRdhGotvFElvk+ZaeAbpBfeaoaLYaRHy1AFVezghPnPRHDKphp4'
        b'RKJXQNMAztRBstlBlyRPh/eS3EFpY8Hw6+lMvJPqyhp0Kxc3LsNdT9tHBJsqT3wVFC4QBkNxeivFZt3oli+LItcgmzKAIvlBoeNmApTYuHpoRBwBA2PQTrDXlZCEUrNH'
        b'+6wgT0DtpUJmZfWWsdQXQfA8Cu0aU8ECK54yIZP6o30ifDsX7aODGiMgYRfix+1SKfN2DblKgy/1CHZxbHbKIXkwcxESWNIDBg/ZURNd/dWefsDhHqRp5kwMAtE1ZqEd'
        b'6JXNMNimKHMu5u/PfOldl2Xgr5PNeVgBy3qDAwBjdKNj80eSsB34FTo7dmifB27Mn/OsF+pks9wFs2xtwxToFYjz53C3yt2crvkiJlEyOgI5efdWO4PReA6gnaEU84LO'
        b'ncStMP070CXqOC6auoCcwew5rgMyPsRM6IESH8fdMlcaDgFcNIIn2kvBAMxqM77+8ojlj1hP5yicGY6PSlDLNlh8hqFx51zcvQL34FeMZtSMb4EWh1J/MBcfT3N9iiMb'
        b'fftohi9JUAOu3EJHmg5WeAd3L0U7rYVs7lt9pjNAfgMfnGSFDj8dsYijMEes9GSLGM8MulLpzhG4uxRdNCe3MfZ0kDyZrkh85GlPcfnZSYtEDySoXoMa2MrcwTfW4O6I'
        b'HGsJSzdPA6w4bgin4EqN9pmYAR82U8Jso2h2INnNaHtUMUmAjs2Wp0ZPpaNUlEMS3T173UiGHQxBhXhDXxvikgyaZ3IOkwNXiXAP2plLVdgiFdUTZ7hhVDK+G92m0EaF'
        b'a43TjneLXoDrjBDCICmxiabMYiHtvq5Ygk/jLiljdhxvB5RIPAXaNwFypsbM3Gd1+BLT4Vsi4nKK6FQtAvB6W6EDcc3bAFlgtSRblIghKWnkol4AD43Z4gOxDd5pT11F'
        b'Ir5YqPCaIJOyVP0MDPsGnSDtchh1Y4jwWa/VwWTpFMESdExh2w7X7VG9whEdMm872K2i7mbRbNDFFnzgObw2SpWCLSajY6V0tTLQFdSkQBXlZcao04jvMbtHFaguUwHF'
        b'O0b2L6zn0aJp6C7eq8A1qE5OxnALHOZC8OCkqBBcU4sCX0S3ywnDC5AYZaFGquSyOIimjQZXJtfztkzc4AOYvmsM/1xDVeisQoT3lUvZ/twR4NpF0clkACZ7zFp+YMzT'
        b'eom6l+NavHsNPr2c0xeQ5KorhNrNtGgfxcvW5h0XXIXaqJ9BXeHuL/IMlyQOxryqQ2IN31o1MXTObCHPb1fExY3s0OADs1nOsUsHYrLc7+yGUWnfSCbI8lnUKClD9XI2'
        b'0dfSYMryQA3N+zqzUC3zaF2wZPsU/hYj+zp4x0LmrivCIhW5nA1Z/rskQPek07kB8z8E+PCA5EUjuvCUr2sD/BEECkxQAQQ8fMfU5OLzGKNTgqvwqdJJgnSZRbRtIlU1'
        b'YSpMosljmZezQ7IaViCFi3CV4CNCgJFd4J7J+s+yBFVvXAvuusIMoo0KwDYw0DWxGEzzATVMuV04jP1SxPODuMwMqkosw8eLKecYUDpwVLDSd5/zLcz8pokgHnauoUNN'
        b'iwguh4D/XFr4jOfGjRJ0PB/XqGQ02/e1Qw8U8g02JAje59DFgHRqh6njUYNiti2+ajTDtnB8kelvfQI+oAAAcwDQBokl4FmzwelQ473pIFaAo22xFLLVO+8SyLZaduI9'
        b'LyvwjhSDcbv6yMI5tHftJH9FKb5i3qjLNlAlWIlq8+F9FW800JaCBIM74XP0JbQHssFKGBz1effAzQBivUkxMLj8eyVQ2ghmT7bpwNBMGSKqiCZ7dmLUnYGq1dxLL0vz'
        b'gMnJ4BCV2OBJGF8EZb+Kq5MX4BoRJ0Jn0W58H9z/RkiX6F7zLQBwSbgqWcoFbxJmCsI8ylm7vXj/kiRcF4Zrg1TkuMvKTuSEW50L8Vk2I3XeXFBqSIKYE6OLRbMF6OKE'
        b'oGxySGT6kOMZenJUTlJSqelA8xCnFtDjLKGao0daIrUiytJ4mCXOkI46zJJ4cepRh1tqyVPHVuJYCT3Meu6t+TBrt0qomQ7rJY8jx6+8UlNEz12VucV6ZbmmUJejK9sQ'
        b'KpcnstPdwILiorJielIbaDrbVeqgVblGV6hZXagNpg3na/VrjYx40k6+WlNUoMwuztHS813CifLgDWtN58aa7OxiQ1GZssiwdrVWr9TojVW0OUoNL1+nLSwEKaaWaPSa'
        b'tUodsJuqzMhnR8Tk7Hi1uXaoqdJqXfZUJYidpyvXFgWzmqTzOYlxT3HXFVEJlfDJhsFp15cRkbSa7HxlMRTozQypfPoNo5mWmUSAKfjH/MrI6beRQ6gyxcCXEZnJHC1O'
        b'C4kMj45WxianJ8QqI4wNc7TmfnltiYZ2Gki+BSq1sCwGTZmWHpqvWpWhN2hXrXpKFsbDKA+bHbqURtmUi3VFeYVaZbxBX6xM12xYqy0q45Wxeq0G+tRrywz6In6qmbOy'
        b'uMisCMHwdp6mkKevyeSs0/Eg6FOHoRLu2cNQ+9R51BoUYbiFL8U7Fpt2oXDVEnrO+e5UN26ilY+UW7VqZeIGDccg/bHxYIfVFLCi1mXcMgBr12j1G1PlnFNGJwD1Vclf'
        b'BNmzs9J+extuzPR4KTdxVfC4l3w5tmN1CjWP5xWQJpw1baXgenxcZUt78ACqllfoRwpzjUdvuLMEneXXERBtOpXDNU7MFdTNXM3bqrM4znQmF8Ca7Aanirut8TkX05mc'
        b'NzrG3N8rxWKFvgCfNJ3IRaP9tGAyOoA7FSVz0GERyz6PjJvKYue5CeBlS/EttMOYnRwLBCTCXNHYzajaylNsPMRDd/zpYKzSIXx38+DrKqUsTThQMJ32UpQxhwe0Vx9n'
        b'Ot1Ddz2ZyMdw5ULcbYCn6XzPGXJQUrQZ7wRMiLsk5aYDPsjUK9mOwX33qYp1MFZyzkFiQws+lM74tYWiQ7hbj6t8SatjkOPhU1IqtceyQJjO4/iSBds4q9+QwZrsQS1j'
        b'+XWQ5e0z7VEJ0B3jaUrQwjhotAf3mIrso4z9pILYerR9urmbXZDbkiabAqXA7cAWUzeobiwV2lGn5SHb24v2m3bunPF9lZAqSRREs/tQCkD6mKnUFR9lXZ3FFeTktkaM'
        b'b3MsAT7qa0MV7rGflLOaKJeQs307mCZ6pGPAZ2ZFTlxIUCdq5FaHLdFdnPKuhFfC1P9m640ti64uwhOtDo39Vepy4UBl7Zz6HXvCk2KmrvsidNEs5bqVTUPZX0xe+n1W'
        b'R3TpllKHsP1nn2S2+H5dNWvVX4VHvrvA3Xf6eHms/uKfNl3v2LT5O+tXN7pcfih5/N7ptSfO5r+vPm/fNXM9Vz7pXP6NGUM/flzbrs0J3FLZMyvzj598+ObYPM9fr/qq'
        b'YFdn+CcLD1q+5THl80m//dsP098rr3b8+60zD1ZeD9j253WLXxuXUlJt+Sefz5c4fvI78RP/zz+t5/9+XPpJUWp8r37n54NvBl4MzVkszvCoCN+S6v8r/7c95y0rvzfm'
        b'G4forTtx76//vOXy7MzkmDe3uaQlPJrx2R9vzfFrE1SmVX1nPSaj/uzH/5nplnbq6PmLNh6zeuYv3eQacjevIF/d91+iN+ZP94zYprJ4TFbDSoqqg0ICEkKEnBRdAQRz'
        b'VBiyDLU+JpeA0OGF+qDQxOBAVSiuD4YIfgN3cJybUpy5KOcxicfoPOrUJqWFoMo0CNYQ+TuknGKhENfJQlj5FbQfnye3ZAJDQgXQwQFAsDuFkehk7GOS74AKHHSl2xT1'
        b'QWsccOU6dkelPCQQV4UJuVB0T4Kvh+DTj6luVPB5uDolOBHXccDqgneU0GbJ7MdKUnTGFx9KYo3BddQTXOEwR8Q5Q2qHb5asUCmGhAEqPYFAP+vBk5smSuV202fIeXqu'
        b'vnijtkiZy+5bhZLQOHNITp1/FiH0xAUISdsboITfb+f+ki7hnNwGXccMOroembp/auP0irmf2joMurgf0e3XNRY0iD51HNvqez6sLazLd8Bncp/P5GGh2Nlv0NNvwDOk'
        b'zzOkPaffM7KL79lwdcOrDq8u7p+c2O+ZODg+YFjEjVkg+EbGeYxvjWy3GHCf2Oc+cdBT+amr16CXd6t3a2xTfsP8T21dBj28T4Y0hxwLa7AgMszaP6s1asAxoM8xYNDV'
        b'a5gTTEgXfMcJ3NIFj8b5DkvIl2Ep5+JxJGt/VmvGgHNgn3MgVOz1j+53jR6EKiLObfIjZ/dnylsL+l3DjcURj9zHnhzXPK7ddcA9vM89nEjl6No0v31m/5gYIL7/1N65'
        b'ybdJ3ypoCmgP7feYQqbHxaMpoim2Ib9i/qCtS5Ou33YCees0timvz8l/wCm4zym4PaPfKaIi/lNHMp+f2roPunoPuAb3uZIC14heu4hHTm5N9k0ODQlN66BRu1O7pkvQ'
        b'7t7nFNEgeOga0G7f7xrUXtbnGtlrF/n9cLyAG+M/4Dmpz3MSjN/Z7yERHv7+wJO1f83Wb54D94aD3Tw/0Ru+AniSk0JOZTUkJus8JALAM2RhhBhDYoIVhiyysvSGoqys'
        b'IUVWVnahVlNkKIE3/1jFrDhyCQkCvFHN9MSvUi2ij8OkDjkQ/Nt27olOLBD4/5mDx2c2rtUF2xXDQonA6aHCoTrmM7Ht7pRBme1DmeP330g4iZ2J+oEn3vO4NJjrUEwW'
        b'gasnhumJ7qOLSQtIVEnFdWmJEs6mROSyYMos3EpP7jemJCYlpzKgLeAUy4XkOLITMpxa6vaXARA/zfD5uliCz+25bNMtSfIRmzDJGgKzhQxmU5DNAcSWRomN0FqUMQoo'
        b'F4kBWotGQWvxUyBaFCum0Pq5t6PviWnWCwi0pvcZR2FrffFapcaEkp/Gxk/jYHpv8qdht15batDpGcgr0eoBeq9lSNN0sTJUnmaCadBh4CLgrFurjdfri/WBlIEGSnJG'
        b'kDWRhYjC0PWzApohqVFIVutZiUfj73mFmjyljiH87GK9XsuXFBflAPykMJzPLzYU5hB4ylAnxfpKhvVHgGi8jgxhBN9CfqFRRoSUGUoAwxoRLR05wOwAUiOYMFf9U1gq'
        b'STXMhO9jcTPoEruViO4AVBx9M7EyOXBBMLqYQS8pkjuVlWnJiSkCDl1ClYoYK3wuQ7fT8AcxnwqM/O9/2J3d/LYduvgaJ1B9YmXVV5NuEzfxtOrgibfdkMfr72wXzGmK'
        b'a9rZnNwWcTbZykpS4x08sd9hx+f2Nf7xbyQHWrVZBVodD+Fu/iDb8e5elfCxDzDVotu2ikDQeoh2NSkGCEQHrWgsGoe6xfiKHu1+7M3R25sXEpJCF0A0AjRTj65Es1TW'
        b'A10XF6Ht+JpK+k/MXmqOLNTghxTsEi6LIeNMMYTcESYxZJ4F5+T1iYtP7/g5/S5xvXZxg+7jB9zD+tzDumQ3J7wa1e+eULmAxRVXz4aNvXbe4Okrkr4jK8HclsWQzKRs'
        b'QxZGFdKTsKonmb7e42npLJhTIgIyfzTO9Bgw+aO/gj8qkAoEvhBBBL4/1x8dlvpz5xThIsN04o0Sppn2EU6TO1CmvYQL+BDaja6hGtQaLHo5KQrVlaLL6By6J+dW4wPW'
        b'+ASqDGawsX1OpKLcBvTkOj4kgPwBX8Kn2S4bfgUdilGUlwo4fFcowBWAKZdksa2V46CFAERv2EaIOSHeASmAwCVyM3VwmfhECh+hF3LlmwTFHOpBd23ZBsPdvDRFebmU'
        b'C0gT4D0cPpqLW8ClkiKngnXMI6I2tJ34xHh0i/rSvOiMZ7YspPiSM6QircbcAx1Hd4LA2Qq47FQhqhPEJaHqp9ypzGRLem5k1wLcqURt2rewBLcqj5KZ3ar03+hW88Ct'
        b'akbvWFBf8sx+xWgnRJwUqfLifYKfSOtJg//WrD67kHbJa8uez+Of6ZyMrTg72wD+syibCWHK5OPTY5VxENn1xKfOhViQXVashzy9xLC6UMfnQ+PVG2hNoy+Pg1xfrymk'
        b'POaA/YWOkkFDJtBAb/IHLo7LCAyGP3Pnkj9xaYvC4S+IETgnYg4tiIsLDKZcRsmrKeSLX7jvQAZA56qE7TYApxzi0jeUwIQQJv9SkDNzKS5hsY20/Nfi2//9toYZQpjj'
        b'h23qPAPxhzw6t+VFt9r/UewQxyli0M18mkj+cawbtyozmzi4lXaiPLadEZLhwH3ll0jc3uZ0hTvHNscbirfRHZFl0NtVbhnavphtlVRsC98KeROqQBXgqB0FlvPxA8rG'
        b'6mVbrmQGuMeJqwofTbDiIOUl/nQD2ocvRsKXcNyex4XPR900ex2PtqOeSBhgRJKAi8BHVZTH8ix7bnv4HI4rWWU1OS2B8CCVHXURjMNxdIkLX4prKOdN6BDaS0+30l3t'
        b'uXR0JpRdb0+Rc7/3UZEtG6st8QVchq7645sC/kMo2r37zJb9KTY7J9rtyVrRqvQ4cvvbfa+/ruh67ffeQ+FHu3y+yTu7IuyR890r19NXz25KaZz8200ndLafWbze0/4f'
        b'aPu08Z1uUw999OWuxrLNpcJfFn8S3qB4s6DlI9VLNwJUv1sXeUHTogwTJMoXZ6reHev5SOb899Ik5ye//sOBFXfCJ7kfPR1v8VZaWvVXKxv//l53xN2/vDN1qOftdwLW'
        b'DL37YWxa6MD7P+ATfT7H3JZpcw6eOjX3Oymf9Pryjcrwx9Me/urW119M+vbVP/tVfZu3ZOnhE55/WV3pWf1p1kc3fLb6nFPJWIrY6ZJFklm0K5vms5DLolY9i9j1GnR2'
        b'dGTfKAkcFdgj7R6T4wJ8Cx92Jr4YMlqS1oZBlRAfmGFok2QBk98qTUQPgh6TSAiLd61ckYRrVBQnAC90CtVzzmifWBaAzjKBdkHsuK7Er0CSLOCE5YJYiExNj0nIRZX4'
        b'3iaSGoelAf9dRN6twkAe19CGilXk1yUAL8jlOpLvQrKbUvh4LB0J5OH1Sbg2SRVqUUATc46znSjKQ5fwdpXlz0twyYa4Ob9lSMSSJbPgyvUhJhzyByMO2Qw4xJWkZQ7O'
        b'R1T7VY1BFXGAOT519f7Ew793wrx+j/m9TvOHhSJ770GvgAGvKX1eU2469nvNaJj/jRQQTFN2a+SA44Q+xwmDnj4npzVPa+XPb2jbcHrTgGdkn2ckZI+PHL0GHH37HH1b'
        b'Fw84qvocVdDZQ1uHhsjq9U0R1Vtbx7dq2vzb406H3BQ9sLpl9ap6YEpS35QkIhLUCq8sb3Lvt/VpzW73bsvtsuz3j6GJoktTZFNpq33TlNZ157e0bTm9rd8zmmXk38OU'
        b'uvlA+mfv/dBTCemfvfcPPDG36/ZxoRwOlcdNE+GpAngyGKVgmInghyERxJQXoaef3El4LssLMT3+NBpVLbMQCMY9BlQ17ueiqqPSQO6iYpJIJaDnNy7ogt/IIUsLOCFy'
        b'yJKBKp/6kY/Z067mWLJGf+QjjhKaf8wj+jf+mAfQxMYW+SIWHn4iT8mlKQcFB6OPNv5fJWdPxSHRc3FImmqYQUy7azau/0dxaDPueXEasxGxzc4i3IFreHZHFO0i18ar'
        b'0Bkvdr3zFIDeo+A0cFUKrlmMK5KFDvHoAtqDzqJm+KLi0u224CMW6AYkUJd158bphHw6Ecr+SHf2UciJ2l+UE9mRnCi5rSxUlN7ivHhmk2WusMr6q5INub6ebrumhKfI'
        b'NNu7hi6kax69A9r4qmXi3DyV5DG5M4TP4OP4wNN5UVXQKPeJD3GP6V2Xq6hlHPHA+Ph8swduR3cf0yv9J/HeBWw/Ebfbhho9F9lOxHdwHa1iB7D4otGnRqiN24DUo0JS'
        b'df0xsbMVeHeQectRiuuj2I4jqipRCUfZG3FbJo9mkacto/4s2uTPko3+bKvs2bxqZJPumb2yT1yUvd6T+12m9NpNGXQcO+Do1+fo15rT7xjUaxWkV3KmREuiJxDhhVkV'
        b'yYlH5VTRpocbmCNPjlT/F4i0ViYQOPwMw/+OGP4BAPynFCGif2rYYjX332jYG+WLSwp1ZbzZetkBGZirkrzN1Wvy6OEXWLLJA2iUUS/cWpAHxKWpUzMWLQtWxiXExyUt'
        b'VqcEK4FbUlZc2tz4YGVsHC3PSlWnzIlfpPrnRktx0W/GWywfz34gGLw2K5mjV+3xPgt65bkmiPwgsjJ5YcJIuoYPqNAFOWreAP8SUeUGfA13cOiEVI4qslX0Ph0+HDfd'
        b'1BgdX0vag7lSn+uF28VgyWc9dCtK7IQ8EbFwjoAZ6JjXf8lskZfxE+MmjlfEecUFxITHyRonpa/1mSyKi4pM1k5sVGVsC8yWLQ4QBTU4v16lWy2LTH7ZKzvgtDQjSvJh'
        b'cO7uZW01sV/d/M1Z9GqzDfdDreLrd/+gEjNTrMN7Npl39o9uww/AFG/hnRRDuNii009Bl7lzjGZ2EF2jAGQyoCDzZnsUOlAgtMGt6fTIYEUZPp5EkVGAlLN0Eyr0qM2A'
        b'z6rELwx8ZAnMOj8kh2yMN+5yzDRZYxazxuFMS87JzWx+z+8HUxOc1e8yu9du9k9tDEOdVq9+l4m9dhMHHd2OTN8/vXFmr5X3/5GBzjQ9AkYbaIrlzzNQ/WTSq8BAUWgH'
        b'ql7LQnJmGShdfRiqon6M89gmzt+ITrzYgHOJAYtNkZn8+Na8hfrvNWJyO8GZbKGODtB0P7JIs5Zmqi+IyyRPJWfbJVp4AfE7VJ7ITLlQU1YGaWe2BgLu04xouNbksJ3Z'
        b'5xJruTmx/md5Ncup///ABbJUupkF4e7o1hfighm44R9ub87SUR81aOe+MVy0isDF6T6R0zl2Vw4ftCRQAVLOM+wwH7Xh8+w3GofFBooUUHvWT4IFQAr4Dmpiue4maeGX'
        b'QuoEC3/knDhdssFTxBdDSfjXD8mWaq2XHTrzIgDR8bqd8EuLyGXLwif6yiO4P0vDI1dxuxc4K6dVOC/eozr4nlb8dnf22xaROHl2qeeElS2St9YGBxRlS5YdsdC7Tz53'
        b'q81KdqT0nID7nLdBOTdUUpaaXVyPa54BFwxZ2AQCtlhjw84Kb6AdaOeo3CyNHl/guiS8Jx6aSbjJqdKt8yKpi0IP8OkccH74dkKCCYfg2zKKMcpgDhtHH2uS025cTXBI'
        b'Nr5Fq8STn9485R8B2ayhDhL3sHwy4SX0IOlpMYgM49ABz6VifKJgKviZn0wGiJ8ZtfdrRfEJaDKxDf18k1vcyhk3f+XPgBSSEE3rtx3XGtFv60fPwCL6XCO6pvW7zuq1'
        b'm/XISzXgFdbnFdbvBcn5oKvPgGtIn2tIe86Aa2Sfa+QnHr69ftP6Pab3Ok1/6OnXWtDvGdEV3uc5qUFGWYX2uYa2r+93JThnlNe0GFIQp51VrKdI6h+mPWz7eNTuNh0T'
        b'fUwVGBMd8KRPSsGTupPtY/efm+gclPpyZxRhIpUoNXWeSjBPJUydp4uNz5Pw5F6DVdWtPR/sW+GgGWMx/MQm9hHnPGH5FI8b6UFdXVGeB5ct+fZe0K92Bs9f1mDdPWPt'
        b'15pNVx50f31Pnx+b9uZ3m//06V9rn6x7wo29vzvos9R8yzQ0zW9q9c45YcV2t8NOyTbM1h2zWz3RP+JJ29CGyZ6vvJUfdPrDyIVO77wXPr5rRVDzOKdTs7pdbs0Y6x26'
        b'0C3iygnv+Nxf1uX+5/Y3lh9TK46oJ50Rd59YdD9XcPmlxA2f7XCd6TTp4fun4lvd/BIlWw++H3GwX57xfqA4f9Ka349552zsB+9P/aBf+s7p765uD507/uXdvyizPPy+'
        b'VtbnH9XvEpwW+Enenq96HDQesUEv7/kwas0bfXsnlYUM6Sw+6kvtOO+ZUzY+us8tuj/k96dW9KX0vPW3//x927SuyAuvv3OivO3IH6fMNriVTf5L78yvzv61N+3JF1zK'
        b'L99q/HaD7du/52z6sP5orFWfpqZ3/JQF80trvOYHdi/2mHDTCydulJ//g3tNf3dT65clLZmvxm9MzMw63Bd07Qv1ytMDpbs+fd333p6PH9dtXrfud4+fvDPUtJP70xcC'
        b'r8/tvb6wbPl8WWPkuTNRL1e7Vh0ffyDmSFVnqPcbau83/rb3+7TceP/IwvbSl4pys6acSs06+2FLoHfUwgnDn6TH2XxXl+k8oC+wmvTXtQNWZ/d/2fKnPyy4tyjss7Dx'
        b'yllb71a4PNq3sPCm9bsBkYFWxYM7jny4+oOYi0sdl395fcuSy+MWL/Tceu1acMfnH84KHPO/zuOCgtsH/1jfUjzs8vWw17gpv5j/lx+1N2/GqSYETRbefaL6caaq50PJ'
        b'ydOGlQtyz4XlFr03d8827Zp3/nY0LPJ3b+VuPfant9ynfybc/OuPB2J8/uPdnhX9yh/+8+GXZSt+HfPdld6iS864quDbyTaSjxZsfwPcG1H+0jFe5Nfgs5IFnGAKwLJs'
        b'1EQxGL653FsR7/yUl2Eu5jq+95j8MCIXP8CtJsfYCR78KedI0y58n/o7fKBgLK4OTkRtE3BtiJSTZgrHz0N76EbT+mh8M2hBCK5ITE6VcAp0VYj2GfAJ6wLq6iT4TkIS'
        b'CVZQAdckkgpXhCJ8Fl+EpK9KNebnXZqQ/dTjZ1+9eKFfIZdSlKbPbPLZ/tSHuVNZVlZhsSYnK0ufZnKldlKO+zsgzHkCztp5WGxh6Up8aET1uibv6s3NfGtEq6Zt0rGN'
        b'7QuPbbvq26W/6X3VcHPh1fXdoa/N/aUDTuiPSP7EjcBRTfOkY5atC/rcQrtc+9ym9E5P7XNN7V2U0ate0rfopX7Xlwj8dGgs6rWj9yCWCoblnINTQ+x+54o530qlHvIK'
        b'm2EnzsF90N5t0N7zGwuxu7zCetgmReAsH7Sy63XwGxaR74+s7BrChiXk67CUs7YHwoISMkZYUkLOCAUlrIDodQgYtqaUDaV8h20pZWcss6eUA2vmSAknWhQy7EwpF0r5'
        b'DbtSyo1VdKeEByM8KTHGWG8spbyM1DhKKVlFb0r4MDm+GU8pX1bkRwl/WqQankCpAKMcKkoFGsUPolSwkQqhVKixXRilJhrLwikVwTqIpEQUIyZRItpYbzKlphgljqHU'
        b'VFZxGiWmM2IGJWYapZpFqdkCI5NYAaXnCIxs4hg910h/G8/oeQKjqPMZnWCiExm9wNQ+idHJAtZ3CiNTjWQaI9ON5EJGLjKSixmZYSTVjFxiJF9i5FIjuYyRy43kCkau'
        b'NMn1MqMzjcVZjFxlElPD6NUmOpvROabmWkbnmqYhj9H5jA4f1jF6jZF9ASMLTbO6ltFFxuJiRpYYyVJG6o0kz8gyU98GRpcbi9cxcr2R3MDIjSbJNzF6s7F4CyO3CozL'
        b'vY3Rs4XG6rFCtt5Co6RxjJ5rKo9n9Dyhab0ZnWCkv0lk9AIh5+gz6OA36KCiT2/T//2+XUZrVFgOrxRynr4nw5rDPvIIqlxQETfo5jfgFtTnFvSRW8h+cYNg0G3sSetm'
        b'61ZNv1vQAck3Is499JFTaJdzn1N0Rfzg2HEnlzcvb5f0jw2tSGzIrk79xpLzDAZvILd7aGnXkN3Et8d15fRZTnsinGEZ9R1HHiJOPp087IbFQJJJoJWbxrfyXeI+y0lP'
        b'hPaWbqRCtLEWkGC8ru5H1uxf0+ud0e+irlA8srQlHSxuHd8+t8u5y3Bzyavxv/TrDUrvs1z4ROgPDDh/xmWRwMgGaKLTRsn6LD3+LLSyDCaFnsYaQIKnGV3BxtJndAUg'
        b'wd0wcRf3WXo/ETpYxpAyWsvuGzGQ3w9nywSWiYKHDuPOWPWGzOtXzu93SOi1SviB3ryqjB2TOJZ7a6xj4kTjDr/dkBAix7+4rf+vBC27ETD8dKCi4Yk+yE+b+ZlGVBwn'
        b'EAjsngAqtvuWPH4uNG6RhnKdihiR7nh9jIh/E94sPnTM0PCufOdspz1f/+2CxN75L/MvxFb/5XfXMpX5n61/aafd7upV4t+2vfT7LZ4ev3hbF50nfW/Gb5s3Lf8yKi9m'
        b'205fh/fShXNQKx/x6SerV1/3TXDo+ePBxzipdp7/iaDQNocdX/19Q0zV2WD3csfPlwe1WY5POvJfxUdkZe+//v6eLTF/+7Hj5cuT3+3/oNmvumdZwsLWXV51DZ+5bVmp'
        b'fNNZ6uYlfX8Z+s3iqLMrBmdHF//Pl2+m/vYY94uvfjxwym93yUPXkhxvpzNP1gs8bL3a86Qqa3opdQI+UUj/u2tpuN5zPD2WU6BrQtyOe3haoTShjKTDV0mVNEj+7PFd'
        b'0YwcSJeb8EF2cNc5EdBUNaonp2g15Ode9RacjUM6qhV5+aAaBqiq3dDRpERI7c6nBKZYcFKxUIYOxz+mx7/3s1B90AJIxg+IBEkc8K1GDY9JKi6Q5D6b+aO6sCTAbHXA'
        b'qV7ETRk3H121gJ4vhbGLq6cXiJ5tIeX0uMZ1rjgQX3amldCRqWhXUpplFjmQHMXMEx0To3MJS+h2H7q00oVsQyaBMCfdLThxiABdxg1qdmS4dwtuw9UqYIDryaaDgLNd'
        b'qHISqdFh3EX7WKFIM5UHE5HpRqiAG69S4lckXJwLu85bFZIblBaMq3D1mgI28/i+EPfgu8mUidM4VIO7cc02dB7QZFhgqRGsehjEaC86NV7l89NQ8d8CEP+ND96HYs3n'
        b'IOYzHzPi1BXpysBvZJoQ52scPcz7zoOTOA5aOw1Ye/VZex1f328dsH3eoFi+L3lHcq+995kpH4iDPxZbA8rz8OoVuwwL5ZLlgo9l7gDuvAIGxkb2jY3sHzupV+YxKLOp'
        b'V1QqPnDy/0A2YVDmMCDz7JN5NsV+IPMatHUfsPXvs/UfsA3osw0YtHKoT61M7fVc+oHVsifSArEk5glHnt/Q5/ByS87KaXva949L4Yvrd5xQMnHQ2b1Cbuyh1yn0IxmA'
        b'T3jNTkLviOeEcShsbJytCNsI4Mn85LghUaG2aEhMLpUMSegW/pC4UMeXDYlzdNnwLC6BYhFfph+SrN5QpuWHxKuLiwuHRLqisiFJLiB0+KPXFOVBa11RiaFsSJSdrx8S'
        b'FetzhqS5usIyLRBrNSVDoo26kiGJhs/W6YZE+dr1UAXYy3W8rogv0xRla4ekdJcwm95r05aU8UP2a4tzYiZnsYPsHF2ermxIwefrcsuytGRXb8jaUJSdr9EVaXOytOuz'
        b'hyyzsnhtGbmrOyQ1FBl4bc6I/+eJx1j1jz5KJfPmmaYH+W8G8sSt//jjj+TWrr1AkC8iDv3p5zf0+XPcOwlYr8mksW7ca26K2PGiH2Sma+hDdllZxu/G3OcHj9yn/5Og'
        b'yqLiMiUp0+akqmTkqnJOcTaMGL5oCguNqks0mWxCwXs5TK6+jF+nK8sfkhYWZ2sK+SGr0Xuj+i2ccXOIbRMxS5jO/pOjM/V7iD/kjGdtwyIIat8IxQIxJCoK6+0W30rn'
        b'wYCHF8k5S3ujKi8YkE3ok03oDZ75mj8O6A9eMCizeyh36XWN7JdH9YqjHnJ2DW4fch60t/8NkMMrzg=='
    ))))
