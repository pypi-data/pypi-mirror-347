
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
        b'eJzNfAlYlNmV9lcbWyEguKCiFq4Uq7hrq60iCLKpuG9QFAVUy2YtKmqryFLsKIiKiLK4oYIs7uLS52Q6nU5m0sl0Twwzk23S3ZOk05l0MtNJJ538595bhYCaTp4/zzOD'
        b'DwXU3c4995z3nPfcr/wPadiXgr6X07d5Cb2kSdukDGmbLE2WJi+StskNimZlmqJFZpqWpjSoCqXdTubQ7XKDU5qqUHZMZnA2yAtlMinNKUlyzdA6f5HuFrNyRYImOzfN'
        b'mmXQ5KZrLJkGzdp8S2ZujibKmGMx6DM1eTr9bl2GIdTNbUOm0ezom2ZIN+YYzJp0a47eYszNMWssuRp9pkG/W6PLSdPoTQadxaBhs5tD3fR+g+SfTN8T6VvN9pBJLzbJ'
        b'JrPJbQqb0qayOdmcbS42V5ubTW1zt42wedg8bV62kTZvm49tlG20bYxtrM3XNs423jbB5pc+ke/b5c2JpVKh9OakA26HJhZKm6VWeZJ0aFKhJJMOTzw8aQtpifabqVUk'
        b'6AcrUk7fI+jbhwmi5MpMkrRuCVku9Pvj7QpJKeVFSVJK8DtL5krW6fQmnMPzi7ECyxLj1mEpViVqsSrGGSo3rg1xkmZGKvFJJJZY51HPBa+5Ub9aaMVqrAmiAVgdHY/V'
        b'm2hURdi66OBYrMTKmDgsj1FJe6HGdQe24EO+8M8XOkvukkbvqklxrw5bK1l30JsLo7Zir+uIddE0aWXMxmjoCMDS4DXxeCLJBcuiN9K0Q9cJiI7D6oQ4rIC6xI0B1Fga'
        b'RqKui16zMSAkOiZYBteUkgXKRs9fM1kvG2ZcHg6drPmKw0n3sKtfVion9ctJ/bIB9cu5+mWH5Xb1Fw1Xvyt9x7+g/gah/icZTAtn1kmalKxHkyZI/M2JVnYmmhA5nclP'
        b'VwSIN/9lpqvkJe0PlVJSggv2TRdvtqcpJRfpXqZ6eUpw3bIVUruU5UZvd8ePU/7WW1r+Xz7jVj+V3wnXLhkvy+JyuDXoExQpntLylNn/NtuoCpf42wu0nyVWTAqYLF/7'
        b'I9mffP8Yf13ql6yh1DAOuqGMzoLOMiAAy8OiQ7Ac2jcE0InUBIfGhKyJl0k5nlCOF1yXbouwjqYhYfAE75vdSdnL4/CMBKewEK7zFuxygiqzSUX21ReFFRKURmGjdQy1'
        b'mKALW80mZ2q5GYdVEpTDNXzCm6B9VZIZ77Dh9S54XIJKPIFFYr52KPc0QzXp1AeLsEWCpjiNlal5jns2vU92j8VZ2CrB+ahkMdlFuAznzXtIhINk4zW0UBC2W31ZUw22'
        b'QpMZu50kaQp0Y70Ex+EuNFjHssZr0AEnzFYah2ehGk9IUAEXl/G18N7BA+YRNGptNl6QoMEZLllH0fvrclebsZdkGzMHT7PJHmElF2IMNGCZGSrp1x1wFs9JcHYMXBM7'
        b'KsdqnVlNgkMpbbOZpnPKEpJ3wb0Q8z4y2xwswVMSVEMfHOcLzcVLWG72pN9SwtmQM1lQzxt8Nwdg7wiSACrXYIcEFxLwoVjmYjIcV/OD6DTidRqCVTP4Mljv4wsVdHgy'
        b'aIYWF2onxXbypgg8MdeMPXSurnAFa0lhJNM5vlDWVh32ks0SbkAh0/fJfYf4QutTLGrsYlorfhNv0jnQsV7mQ9Zswh7zPrbR4y5ssvIVeEWo+tZUfGDGu0zsk3gcGyQ4'
        b'4QktfLq1KblmTzamFW+yZc5iMzyxjmNyF5Mx3MVeF3bmPXgGL0rQiOehmC+WMZ122OtCclg34BUmxpURfMKt+ACasddCLZOtbKkafzzKh+AF90TsdadjPTieDWnC8wZx'
        b'EPfJiCqpiRSRTEdxlaYbF8FFl+OVXdiL3Uz0y4R7bcz4y9zFMHIDGUEbjcI72IWdErR4TedNyXCVie7K1HQpn6mp1YpnhTKaovAUNZFqsQVs2CVBG/alibZivPE6qZ1E'
        b'jCELINM7AbfhBG8z4Wnafu8IttoxuMDGtcJJF74zuBVhISl7qW3TCLxGesrUCxGb8BG2sybyw5lhzGLOjzcLs+hR4HU6SRrju47J3kQeUs5VSL9cXKl2YSt1+pOfwiWs'
        b'ncFbNsihQo09NNlCKMDb7NR6D/Pp5sKpVPVeZn5VtByt0wBXsUGsdBq6RqrxDulwtyd2M6G6QJjM69CLNmqiDS+fg71kz15JfLd4HW7gUWphMxaEsKVaJmEZ906owM7V'
        b'ZguJt3MmlkpQEjpaaOG8F9xXMzged4ip/EwaXLFOYJM9xuuLoGI+HofSdaTQSpWkwFZZIlQctLJojjU7oAUq9uJJ7KM+VVCukpSZMtphK/ZZWczHs+EkEesBj9ygajb1'
        b'4tO4QpV8rI+kVXABAqCTFFKhIMSD41KulAun5cLyWlbinVilhNegXEqVUmlvN61eTOSiyPGxThI2pFAESVu4zjqTow/aPLEOS+H6fGhX6eJJpRffiIA21Zpt8dJcswrq'
        b'yRJs1kDmPlAHHY6+nXjPH+tpF+yvuXAd65WSH1YpXQmnrli1bOo+hiy8O9yBqzq8z/pHQ+dAd3ikVEBrAhdk4cLljqk78AwZ9PO5b4i5a5VOqdG8b/5iOIp10XCDRMbT'
        b'hwe6ziYzYF1DFLSta69xoffiNewWMxugkOTme4S+N9QaCvpXN/lIazTOaiyDozxgwemoHXaZS/ewXTrmhptYxX5cYyuEmFR7mOPzIa50cg8c4rguxypFqliBfO0sKRMq'
        b'SJPReM8Jb2dis3UaW6UR+14b2IFdK1CbolwvTcBeBXZtgHbra0yHJ6AOG54rUcjQMUg5V+PZJDfinVLjpT1kCw1wwYUwpk9nDaHxTnhrPVun074OliqgFsuwHkrSyarO'
        b'SnAsJxwvqKB6HxRy3cJ5LB85cBKBI5+f2TVxZnUK7HM1W4NY38vwmPTisAgCkLJBkrWLY7MpnfFeNpfGe3EI1q1402FAz/cyyCjmHlTRHh7ADesstv/zawml6yzkHsJC'
        b'n5/HdT5+rjjy2VijguaZGi5WLhTAnec6m0InNUhfQqoOpQtptskaRv1HweMQ0X0EtgxagwbfEEJyCwwhVzXLoYAfOhZkU0exxhOs5naBJwlD85luoUQDrWRa8fjIeTac'
        b'mMLFypi+BOvg9JzBvkZWgoXbAuYLscx0doT7pe58Cb8gSjH4CuvY+V1/wRTtUp1SmRfhRe5yQXEHaYlmMkhxfAP+HKGh95mxJ+J559ANs/hxwBkLyc6scMV6tu0qodbn'
        b'u+dChcJD1Rs+r1sD2K7PYJOb3W6v0cGcfAEBZirw4ehEYUmteHmDw8jHWJ6fcwfrOQHvKLAb7ij5EUwlnK7DOn9sHmIc7cONY48KzkDLXAFdR7F0gcO4Dy5ydHWAgEJB'
        b'Qf4OJVNMMaST4hUOQ705E2tftIg2pfMmKLLOZTO3ukx7jnNMklyy7ee2p4Qe9/gVq6BjBkVKllVmYi3nPcb1FGMcA5cudBxxhEZFMatZBRcoDbwhdH9sgxnrdh2yQ0CV'
        b'WOq5UNzZ5mCjCmpXLeAqWohnN4m58SIWDAy6NjBIQVKNeGOebJ3KeaH3KG5y46E7N5bjA9Z7koqHWQW0ETKthypn/9xEfr7WCaMHUEnAGO/GAAwvQcEcuE1IEU9JLddp'
        b'E7RrHd3Z1p6fwDVxwt10BJSKccgLTsCrz3Vq74lXlhHk+cExshq4lSps7HIiVg1EpIlYMPxgwabAB5EJ1qnU+QBcNQ/HUazYJ2c4epfsazHUiElvUFy+6ej5BqVXA4bV'
        b'KWTtIlmnr+Gd96wm5BZ2dc2KVwbw+dZzy7pFacoVazibuQkLyVgo5g7am/0QOweFjHA8qyJsPTqZHyalFXdI1VCQNUwjcx0YLwZtVlHiXxfNI5mCjPgCjbnvNfgcmXkN'
        b'ePfaOOdFs7GaCwbnXQn6sRiaBttYx/DdzIEnKuIuNjwmtnMJOyhq1Q0aM3eyXG9fyIvWuTd/JJTOk0HjcreEnXDPOoOloP5Q7xizSP+Cb2kVeDcMW4Thn50L9+yw5vsS'
        b'QLejmlWVlwcC1PAK2Pwcs6/CwmGYMAHvK7CHkurbIibdyXKEJIZg9Fr2AkjhE6UH1EwRKHWClu1yTD9l33NruyFm71RgZ/ROfgJJBM6kG2yC28NAfNARBDsviJ0tHKRm'
        b'FzMk0fUaHJv+giUxU36yJJCHOqiNmD5E73B/yoDioXcbOUXRG9i2TTLtpgAvqUW6cpmyw1tD/MqxU5W3CPBtcC0cb1B03LiOmx42j8JSMWI0PhmUTDzPL0SOA3Uqi7uJ'
        b'j5niTkC+PfjFVdqHWHgLRzh7VIWCBGlg85SEPXwR5DpVe+bJ1ro4z88gvsIUjLdkdFwDaaBDXTdUqaSAeCkBLs0eq4LKEKgV3W+OI2JW5zCfoxMGKVgkjdCjVFKMqxAg'
        b'cDWPklOHrjx3DpKkQ9hFudIFW8bzw6NlKEtzoFvlzheM6DUFPoJeYohss7K1h2jigo3Ds5Rh7ox1Kji3DJu1cTxVT4iGIs4t4sh9GLnA8t2CddRviTczVukRimUSEbeb'
        b'qYIsFW5OM5OSWDQ4wYoZ1YF2crPxyEJeM4Gj/rxoQjLUcEIUsx4vmKGSsd72vXieUeyL2CaYwkMX6DGbGN3stqKNCMLKLYIQlWEt3OOVFkK6Y7zUgtdXCoJ1k0LhUV5r'
        b'WRMpSi03sN1eT8kdSwyfyWnLxWpW4+jK5vvRqLDB7EYy5I5j0tXDuTl8sii8D+VmKGci9E1nHPQcVCQKGSrwFt4SlRsFnTKr3EBZDF/IOBMqzB403QhsxLNst7fshZax'
        b'eBvaRUkHGuN5SYfhilDe6ag8UdWZT3kMq+rsgkbR0hAziRd15kALL+rQFqtFVec84fplUdWBhwxKWCWmYIlg0H0Wf2pyZpZFA4n+n6T4Xi+mvEkOVc8rPnpo4AWfUHeh'
        b'pcokBa/3QOEyXvCBUkJRdh7ZqRZR8cnAIl7ymUvWxdSUBp2RZk6rKefpxia247b1gnT3kPof8ZKPE2mJVXw2YKkQoYu6dfIiSRZZCyuS7MwRIjQdgULzPkZ37xBC0Z6q'
        b'9PPFdHe3k2p59QRLknjxJB+O8UFugVupgZnYxVBWdDqJxXhZLFQ0I5vXVUbjMVFWacUz9npU7Fyzp4wXhB+zmso5D/sYxW5G53m5pSCaV1s00MO1upggtkFUW/CiDy+3'
        b'EHoIRRAY2iaJestOLOEFF2ydxE+KQLlJg73cOSiz72GqOAXXdvI5M6GYGGGvOzOLYyq8RMsRg3zM5xwLtRZRqYkiNOWlmtPYIZZrCNgpKjVEbkp5qcYNhPy0ekc2LcfK'
        b'E1sy2YxnV0p8kJow5iH2erBipM2Z1QbasHEab3I3J2KvqCuW6MhRaL0WeCxKTFE+2LuHWg4lMuXWEIV5wBv2jN9GDcxcarawkz+OjzVCgnPTHNUibJzAi0WGMUIV9TFE'
        b'SHmtCFrIMFmtCDuJrTIZDjCQ5MUiKFzFi0WUJF8X9nzKl/JvXi0iB7ghqkV3E/iwEMqgzohq0RHs4tUivDlPHH9b1lpqYRWcSjIA0ntt6GQue5BXHjXQUu7QzXyxDlqn'
        b'8nIbHRWhci/eduKlt1qm9gbsoyjAJyzFci/sHUHamI7XmfjNfsFciv2ecntVqpnOj1elWogpcwBUbqYmZjQFy1ndpy2HbIbtagTR/CJ7wcpNzwtW5KX3hXs34gV3e8WK'
        b'/LWV16ywZRkXYwSJdFqNXUz3leGs6dxrsUL1nRTjRDkrQgjY5D2BA90SZabahQbMIBO4TZ4yCYu4dIvw/mpe5KJU4wqvco0J4QNkvllqi5L78XFmRXVLPfmA4D3QKopf'
        b'izx47csTTwubvAC1K9RutIY7pcb3mQ01gI037SaovqDey2a7mYzthLPUQ6iUJaye6r1M3XdJG9cJDEOyuADjCDvv8WLaODMvpW1eI/D36hboFoU0tCWKSloxPuRtwXB3'
        b'hiik0ZsneSkNS+AsF2IZPsJuUUsbQQkrq6XBmYX2ylTkarUHKUG5H/skys0KoJJLN3Ictqk9WJHyFp7Hx6xc3vCGMIVHU/CSGruZ5rq9meJaRgpTyIBOd2qgQRtpmXvM'
        b'VHvsdeu1BihQu5L1jF3P1rlCR/pIlNof7Z+ptipZ8ayd7fX0JDsedkGjDy/m4Sno4eU8b4WIdpUJtBuzMy8SFrPdnD9oXyULL46nNJ6ZR9J6fESHvSmcX2nhozl0JBWU'
        b'D5ayGl4VhZMOwdNKdtHfpaw0eFsJvRugYqO0eacTXhiDfVqlcMG6hDCsiFuT74WVCkmBjynPjrNXSlftPhCL5XFOknyXDGzQFkY7O2EdTy2hc6EnFqvDsCpIyy6s3L32'
        b'YJtiNN7JE0q8FoingxJC9smjlZJyuQyu+WBdlJ5dJTm+aBP8nonfMS2X+HUWu8ZiV1rsKkthc013tV9iKUuVhdKbqgNuh5QDl1gqfomlPKzaIqUpkiTXdK3yx/9FJ+Cm'
        b'GfQVwW49zRpdDr/u1KTnmjR7dVnGNKMlP3RIxyF/xIjL1sDduTmWXH5xGui4atUYaba9OmOWLjXLEMwnXG0wZdsXMLNxQ6ZK1eXs1uhz0wz86pXNyuczW7MdV7o6vT7X'
        b'mmPR5FizUw0mjc5k72JI0+jMQ+baZ8jKCnUb8tbiPJ1Jl60x0jKLNRsyxa0uu+5NHZgl9GUDUo36xWybGca9hpxgMYoJuDImYogExpwXdsS+9KQYw34L24JBp8/U5FIn'
        b'00sX4nsz5Q9ezOIQk1T5169jYRfc9tlCNfFWs4Xtkek9KTFkTvj8+ZoVcWujV2hmv2SSNMNLZTMb8nRcsED2W6DGQKZh1VkM/L48JWWDyWpISRki74tz2+UXGuemZd+L'
        b'JsmYk5Fl0ERaTbmatbr8bEOOxaxZYTLohsliMlisphzz4oEVNbk5A0YaTO9G6bLM/G2m5H1G87DNvHBv7iINv7gdmRDF8YMCSDslnaON7E6AcjMKaWX8TnbrrHESEcJZ'
        b'GnneDp8l/pLVm97088Q+yqerGEhslbZugHu8b3KCWhrFVnl9d/CB5AxxqWs2ekh+kuT7nq/B/V9Hj5M4CGgpq6mkPBHOmVj4ZHlnYZTWU8SUZkI9lkTCfR9H4x0DlzIv'
        b'aLN5nwKvb2bYyG4N64iVs/kCoeWI2ZMlmcfFkDPYI+5tAs1QwO4NoZjm5veGOXCat+RiOT5Wm4glTmGASmPgyS6BwDco2Hao8xRweiyLPYTNbgpBhZ7kwx31HkXkYobT'
        b'FLH3jBQXMH2vLWc3jRkHJBm7Z4RTBPIin6un7K/X7ASFfizmUDqCl0eIMZe3QQe7g8yhNfkVpNd8sXztDondQJKOi1j5j7LbHe4iDDbiuYXsDhIvQBdjPxQBllLKwUTT'
        b'vp6q3qegpP8Yu5SjBmkGX2bBrqnYa1LlebPhjC9cgg4+wHc0Xjfvc8YHnuyiipZ/7SAfMM4JLlGevotoPRerfDfe0NoD0E3KGC9SI7bn2BuhdrqA9aNYn8UWwu7N9pWy'
        b'3rRfgrnjVVpoBlyxL4R3sYsv5XrQiXEMuC8XLURmjFq5OB0d1LI2LAh1tF3ViPmqs33ZhTP0UpyT+I0zXhbPHzRsZ88fSF7/lf1mVkpogiTOrCBi+pxZSvNKFtCkVCI4'
        b'142xT5OVZhb82yY3Lj0enqBY4R75y19/K8f7nU3R6y6O2nDSr8D7OzdXNUduOr5Fuz49qeWiW3TC6amf7PUr1OfJq73WpU4YGa9/8voPf9jztb1PtxR+zePAs9UFf5zx'
        b'o3nR76o/fKfl6337H518X1W29FpCnN8f3lv7uLHw9x93bVtt7fta+skLXp8sffCZ9M0170+9pf5lf+/VD9wTdvTZtJ/EBPzZJX9G/q72/Mkrl2S++8fs6g+rftPyWeKH'
        b'bT5PTIcv/zH2978fV1i2+e3iA1mPTs+eXPy1jybuvBCT//SQ/4mCr98pNkb9KefXidkLXDt3PPQuuvze9IcwZn7e0//5l/zvTv78wAUYdeG476HQ+BsTzD058u0nUwtf'
        b'++k113mz3p916E+qb1xM/8l0rdbZwjSsd4LHQSEB0SFydmUzCc7KQ0bCccskatJR7nY6KDQmOFAbijXBWEYJzxPJV6PcRdS00MLuHPV+eC82MQTKEnl+oF4nh17yh2o8'
        b'm2Jh6faRbLzEnsYJDAmV0fzdWAzH5HOmYJ+FVToiiS4RF7M/GLNPPBizNyQQy8NW4UW5FAqPVCRD3WELJxd38VE+VsQHxxDDp8mupsyVeyyFixZ/ajz4BjTEigmApotb'
        b'Q1kMdpmJGBaxK7mScVp5vzxAywoLktaV//irXxiafjF6Sbop94AhR5MuHroKZcF2Wb8bh/5k9gfrZt7E4PeIpFXKlDIX/u0hk8vGyNxkXvTtJmPvu/P33WQucif2Knv+'
        b'ytqcZL78J/vLg/5Ssha5n4zVPaQELozWqV/JVuxXUADvd7aHw34li1/9zsnJJmtOcnK/OjlZn2XQ5VjzkpO1Tn95j1qliSVhJvYIjol5l4k9+2ViyRlf9xTbG7vKlY5K'
        b'n/iR3HKSib2KS8VeqPUfrn1pNPGa20L9bfCYUIU9YhY0xj+WWrGdXSEnYHVijEryyFMsxCtEwllGmQ1HoTs2LkEklTJJvQ2Oesix8+A8e8DAY+sHklE9XA7DB3BOrxgU'
        b'/Nh+nB3Bb7408ICUMl1pzyMVpQrKI5WURyoG8kglzyMVh5WD8shnsuF5JH9mblAiacrN1ugcqd/QJG9oQjcsYdvwF/JKk2GP1WgS2USewUS5ZbZIexwP8g0N/ImOfIAE'
        b'CVxPKxqzDZEmU64pkE+mo5a0l6eLTF4mrkgZh2/ipbmSfVNixPAdvmwJlmBGZekyNEaR5upzTSaDOS83J43yIp5nmjNzrVlpLG8SKRBPeO1J7sszpEgj2/LzhIySb51m'
        b'dojFmkeJlj3t4lqjfDGA9QhmC2m/Il9SvZAvqRKsSxnuXMAbywnEXnhMsAxOYmlc4JpguLZBPDXI3kyMi4mXMU5fpl40aswGY873ymRmNs+ZRv0vUkI/0uqidVnpWamf'
        b'pOx6+uytZ28dh1vHF5W0n2o51V3YHn29pKUkvMr9c+2ZlhL/MwVzFFKwq/pS0C+0cgv3tI78sepAcgy8CYVYhpXxVg6XcmkyUPy8iU/gtkUjcdrdA3WxoWvixyUHx0CV'
        b'wynHwy1lDra5aeVDnP9VsMcRoF8tnhV9jnIeAuXSGI55czQzeT5HJ1W/i8O0+p3tRiLgxZ29sAc6hyyvMI1kvzN4Ed047LAJvzcIdq57D4YdFp8WwMM32Q4d+1MvH9gh'
        b'PEixLmZqOBckf4EQt2M9FJF6Kt8IgOZgxc7YuVC9BzrgMjxyk1KxdgQ2LbSItK0JGj3Ueyl5kFEOGheB1+dPEBnQZexIV+/dwxpKpUnpeM4Z6njatsmHlTHveBJnPztb'
        b'KcmxVkYkW9Srtnlii3k2KUmWyw6oHCii6Xne4jYay9V79zrRdMXS1HA8u3AtASZLv6NUwQNwZzwShjdXc5iE3vDFQ4l3BFQpRgdgpWDzLSnQHkQgKpPkUC2jINwa4YLN'
        b'L+DkAElYxnBSwZFSPEQqt7mkuwzgpfKvwssvX8W7uaMPZd2vRAuGLKz7V7PXV5BKNvh/nVPqs7hYZoPlRRY5TECml1y93krAmKN/UVAHj4xcu0ITQfHcxIBzFQUIvSXX'
        b'RMwwz5qaZTRn0kSp+bynHcgjiGmadFkvzLeSXDN0kGw6dihW/mh5YFLEhsBg+rFqFfsRkbg+nH6SeIErZ6/kDRERgcEvzDhoT8RRc1/KhtkmuZ7zBAemWdMYhufnDVMg'
        b'+/qrouPAjLl5LwZF9vXXBcYhh/d3JeEy6WUk3JNIOHu+Coo3xbw0qLCAsgrKXhlTls/h9Ge+yZe4etcOKSXFT7c+S/DvoGRvaZq0nBLiFL9f7rEK/k0M9SF2QwWrHlP+'
        b'Thw+FhtEEfpMHBHwCijFGjwGpRQHfWSu4XiOz/W2D+Pyz8KdZ5HZRr5GkM3xaD5hYscc/hBngRQuhb+ewgHMGgolc5TEjeGmNFuajV3QwWcpcvGSNFLXSI+8lDhcudkx'
        b'C2V/Z0fRLJmvsTmAApmVxYD93rGsIg5ntdJaaS02BvM5kuayUsNRH6VXStzHeYulDcYnpdtU5lvUVKB7f3p1uAfMIko3Lb7/mO+JB3t8c96TbQmKdT/htWbxxq61/g1q'
        b'S0Lo06crDsyo3bTrB59/fndZW5jr9hR3rx8X3tj59XcnH5gW/hO1beJ1je/UZT9W3n10bFd//8SRn+3QZHz7ae28xnX3PpWt6PaILCp9vH1ZxHuLfvWrikDf1dOMxY2+'
        b'MfOW/8O7bx1P2PzP/SVxpjXXv1ywp/7enf4vxyS+GXpv0S/np/2gNSbw8zvf/cfvt2WrP/hvz9cT5i/c/qbWRdCZ+wcUjHhhKTxg5IsxL4rptTzOb50IBSLOD8R4uAG9'
        b'z+N8L8V59vwD/WLbzYCeKBjjYWGUDISwQbHOEl7aHI7NTjFzcjmdg9NYjI3qWKzUDmQNo8Gm9McGl6CtFh7vLmmDYhN94WQIxY29shVwDm9beDx5sMSf8biwRCxxY9Ie'
        b'lgdi1yHOILOT8LKgZb0+nJkRLdsaZeEPlB6HdrDFYlUsGcZdB4uUPGcpMmg7lVqZSABc/iYqJnISV0G8KGTwjGSWyEiOSJKDebFXOTEoD861PGRKOWNUU+jb1/5t8hmU'
        b'szznP/0KQu9BqcpXUSfFIOo0aiB9YXN/Oih9OTl+cPrClLPUBe8PkCbiz3D+dQrzI9GmgMoUIkwy7qNT8aQrq8tj0xvPC/NwP/KFz4QMUJ7ZEqc88nT5wGc/ZH/xsx/2'
        b'8P3FPw3BsvUCC1+RtafzpJtH3cGV7/9tmvNKMHZoaSgYOyVY2Ue0DqkZG30FFg8F4rlwdxAWY2W0gNh2ykCf8It8gtLWlRKUz86wBkvsMbGKxNjEECyPx8okYgty70jq'
        b'XEyY3AmXoIH+IKjzcoY7/lhsTD98XjKz4KA8kPuLlOBBVGHL03vHW+pk0XMuzQpJC94UpEvQOX1zVmjKz1K2vOP7racNvwtxkpKmj1DdXqpVWdjjaZ54YjkByFF4PARE'
        b'BgBEBX0WJnnc9jBH9YcACFplIVFwjcMFlrvCCVH9gXvQ5vBdXv4pnsTdG5om4XE7oOyEskGY4kLK6rIwwp+ExVA5UCKC1lm8SkS6vgJnhevJX+rfzhkGy4B3ezm82595'
        b'Na+dyExjBry3XSFqFi+lF+0y0ci9ko3xJc8xewuvPCr93GOwX7LUGo/mJg+pab0BtUzgivCv8Dm5TfqbfK6IfO7aEJNNyssyWswDjiWuG8h7NOzddJMug18fDHMyh6Pq'
        b'NHNfyoGHdA6ISNyYsGH91mBNRHRkRGzSxngixysSYpMjEldFBmtWRPD25ISN8Ssj12v/MmN+mT/xgP17J16ajX6mTYnbEJkiiYSnCgqhk306Loh9tK4sbl008RcneGKn'
        b'MFirhXY3aMin7xgoyyfrcnKj1KQb2/iTfthEo27x8VintE9BHsVp7SS8qiQfLt5lDPp1nsK8jvrnaU79ImXH0y7ym+7C8GL/4u76mNqWUy0lLYX+/u80Poq+VBRe3N7Q'
        b'XdatCJjyja6j7YV7/PUh+hH67olrS8ZNS8J7R/P9IyhSjZcqNCM75Y+1Su4xGXgiwO4y6fiQh+0lKdzU4VHygSHhVRVpd4bTq3gU9cHLgQMFzNl4mUVK7N7N0wHo3T8u'
        b'lqI3XIUTYSEBTpKrrxxaEkOHMOWXu4obcQ7zIHY+yuEt4S4yd+4vHoKjjx/wGNPY4dP5DvgI6xUwxEf6h/iIht6dhOehJig6ODDheWlhDB3JfXioHB0EPVrRbQe7V2fB'
        b'q5JIeE0YlJNL4VFn8qrxR5SZvqGvdih73Y5/rHGgbvfXOFUm8dCdw+t2g2MZL3Dl6LI543lJCGN8h93W5RnoDQp1Q4NKjHCtLJ3FQvRFr6N4NHRSHtl0aaI0+AJxGzLX'
        b'AIn7Kg4nONv/1dAqeykUuCRwr9+CbdjwktiqPfSy6DootK7I4FDyidFX8tuULjGas8NzpuNGsRx67NE20MJuMMuxj4dbfAgPgh3xdn7I4Ig7JNpCCd7l83cpnaW0FeS9'
        b'mpTgDTOXS8bQzHlK81ZqKdzz8dAY/POUzPQ43bvpwet/Trjy7K2u4+FnWgp1sn9eWZLg9Y/noO9497PLRdOLp2xX3Tg/7sb5jYQ2sqvnbzvdWFbMSnkTpd/+YIzT3D9o'
        b'nSxTJP7JzJLo+XB8WJo/EKGD/Czs0VGwYd/+QQn+fmhKZAV0UilBTbxKWpDgdBg6/Xgqbowa64jmscQrGKN4ghcs/NNfV7EiZMhlDoVy75kUzEvhggj4x7BP/QI9SAtV'
        b'ukANNnNasn3TLKyARhEdh0gxGWqV2EQnYXMk9V9VVHTnAZ4Mm7kNx60xDtyKZGjlTngjIr27zOQ3gFxaRb+aIV1yromlB4Ni/ksXJGkmDiAbm2XxEGR7Z0hRkSVO2ybi'
        b'7VftrzIGm5ygXqtISIjSyqK08oQoY1Xlv8vMv6JJ4/dVbTzxvc0+K0bZMtIXNHl7KZ4dHHtwtWv5xKDAFYVRX7pnjlKl4k512aeh4//hbR/Pb1QcudIb47H620vN//Tl'
        b'B3+YNeet9sp//ZGTm3fDnBlJf6r++ajxEzb+23o8s+zjO81Nyy6MVT9OadS8H+oy882EP5jeXjUjrGzUT2/5jdJPXP+7/7jz0ejvHPvt9/3Dx8R/MKFPCh+febEs/Se3'
        b'3nt3Sv+WuGN7F/9nmmvs1rdNm7pqN95IH7F769cPzO86EZ+Vrt7+/bf3Pnj2VsLe7salnxgm/2HR07dOhH77p162RSs/79Opq02Vk2p/azrn89s9tUnnPnLPWPT1/C/u'
        b'N9dX7PhJz9Uvf9CZVy/r/NkvFy/wnXbp114L7kee1eWYbe77rPPb7x7sf3Py/uWnRkblvzPVtOQjV/0XH9767GRG5ZyWmxfnfe+b0/LP/+bY6b6fzEv6zZfnTRu/f7V0'
        b'Wfi5uKDt/e96W8+996wrPrY+/ptd3yrv+eCG359xQuz0oo5/+8j0dP3onwXG7lV3fOt+fM6zqs0zj22c/fsPi/x+FjDzo7mL0+e/s/0Ho6f+KfdZgSq36PPphT/sH/fN'
        b'wGWzdu5TfnnYbfTPyo70RS77zNV58938xQs+dmmq/Ll6RMIO85xDnR8u3Rr760vTfvHv0x+PwQ8+fe/I2e/2L0jffTbj/du/un3u03k9M17/3dZvl4xUTJn9xdjvhH/X'
        b'JTuNvJhZ0d70EApwMkl2cNxCiVCudoMgvuWGJcNcCa9hG0sG4DKesbCP7KRDEZx6hfdfpHh5E0rhqigVNM/Ch1gRHANFyVhFqb7TLvnUTdDLr2CxeiX2BK0JwdKYuASV'
        b'pIZuLzgvp2zpjBt3/BCvg7EMfqkDGTDrcHMRVstJnF449zdehWo9/rab01fOozKxiPHSFw4OLsnJWbm6tORkDgwrWYiZKpfLZXNlk/4sl7NLUm+5i1IuveSf7O/y7h+U'
        b'bvRTJv/SyYX//L/375ZTgpeM/XOReStYocPvdTlB5SgfN9KTr8wvQM5aPPirF3s1TXIAMGGoPDl5EHSO+P8/UZlp8gDOsoUYlop7oh/OGIyxzCQXvBkOFRRUaubjZRb1'
        b'oQxqnCWPcYqJS6DQeOUNrdzcQN3uHf00pGKpGywfVfRx9vwnUaOCld9522f/WLVeu2TV2vWZgTGLdT133/nB+ztPGNMf16xbt2RW89enNf16dnRYUusMy9T3MjvmlMd+'
        b'0XkkyGxa+fDuf3528L+zlOFuY48Uz9ilzLhlc2qLu+T55J2Hcz9bHnj7z/N/s7/qrQ++MCt9tqXvWFv/8b2flu8en3Pvw08Xfy/uN4k/nvWT0s/+RzVpi/ZHtVrtCO5Z'
        b'UDuGNsH+r5FEYv2s4qaGHsNaOV5dCG2i5FZ1GE/HGuSUkHSzbokUmUdinwJaoAm6OFLshovYIrRBqXQzizbElJg6vBWTsiMt/KmWx+sssTHxgfHOLlmSk1Lu4pfPy3XY'
        b'qsHqoDUqSRYrwZXZeCYUWyz8EzD3aL2Hg9OuXDgjCk1hsYQz1RTaahTSauh2hppZi8WNYTeUHB48BGsWsSFO0thVysBlCp60+EMrXMderCQ0CQvcwyCL8odOgq3xViWU'
        b'GOEUf+wDH7H/UKACTmlJLVjhLClDZNChxCr+rMZrUBPDQ6xDlrVLmTQToFFJ4NiDT4R2u+EW1mOFNkTuC2WkYDIUmeS5TrERS1w4gJLGbkqsA2sOhmo8CrYwQQxlkgZv'
        b'qyRoFSeVth1PBiUGk7AV4pzw8Q64Kse72AxXhzCsiX8fgPs7vmgVr0JIY47RYkdIRpClESxdIsKnUMoYEjDS58VTKJZEuSmmsdQqzKQZQIHJ/YosQ06/kl3C9Kt46aBf'
        b'STzE0q9MM+rplThQTr/CbDH1q1LzLQZzvzI1NzerX2HMsfSr0gmg6YdJl5NBo405eVZLv0KfaepX5JrS+p3SjVnEkPoV2bq8fsUBY16/SmfWG439ikzDfupC07sZzcYc'
        b's0WXozf0O3EGpOfXxYY8i7l/ZHZu2qIFyaLIm2bMMFr61eZMY7ol2cCYSf8IYjKZOmOOIS3ZsF/f75qcbCaOl5ec3O9kzbESYXmObmKzE02s0mdayF7msBf2AJKJZdgm'
        b'9nE2EzMoE6sim9hn+Uzsw7gm9qlBE/u4l4nRUROzXRNLg03s84qmReyFPXZtYto3Mb8zLWAvjIiY2O2ziX3Mz8SQ0MScx8QIkYk9CmCaPYCV7DjcBrDyd6sGYSVv+8LF'
        b'8cBRv1dysv13e3D8Ynz60P8BSpOTa9GwNkNagtaFPQqUlqsnndAvuqwsgnyN3XRYzk3vu5H6TRbzPqMls98pK1evyzL3uw9mgKbXHQoc9CLsb4n4b6aWsdjMC3RKJ6XC'
        b'hdlY7CgZizf/D7YbAUE='
    ))))
