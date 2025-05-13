
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


"""The Python Fintech package"""

__version__ = '7.8.0'

__all__ = ['register', 'LicenseManager', 'FintechLicenseError']

def register(name=None, keycode=None, users=None):
    """
    Registers the Fintech package.

    It is required to call this function once before any submodule
    can be imported. Without a valid license the functionality is
    restricted.

    :param name: The name of the licensee.
    :param keycode: The keycode of the licensed version.
    :param users: The licensed EBICS user ids (Teilnehmer-IDs).
        It must be a string or a list of user ids. Not applicable
        if a license is based on subscription.
    """
    ...


class LicenseManager:
    """
    The LicenseManager class

    The LicenseManager is used to dynamically add or remove EBICS users
    to or from the list of licensed users. Please note that the usage
    is not enabled by default. It is activated upon request only.
    Users that are licensed this way are verified remotely on each
    restricted EBICS request. The transfered data is limited to the
    information which is required to uniquely identify the user.
    """

    def __init__(self, password):
        """
        Initializes a LicenseManager instance.

        :param password: The assigned API password.
        """
        ...

    @property
    def licensee(self):
        """The name of the licensee."""
        ...

    @property
    def keycode(self):
        """The license keycode."""
        ...

    @property
    def userids(self):
        """The registered EBICS user ids (client-side)."""
        ...

    @property
    def expiration(self):
        """The expiration date of the license."""
        ...

    def change_password(self, password):
        """
        Changes the password of the LicenseManager API.

        :param password: The new password.
        """
        ...

    def add_ebics_user(self, hostid, partnerid, userid):
        """
        Adds a new EBICS user to the license.

        :param hostid: The HostID of the bank.
        :param partnerid: The PartnerID (Kunden-ID).
        :param userid: The UserID (Teilnehmer-ID).

        :returns: `True` if created, `False` if already existent.
        """
        ...

    def remove_ebics_user(self, hostid, partnerid, userid):
        """
        Removes an existing EBICS user from the license.

        :param hostid: The HostID of the bank.
        :param partnerid: The PartnerID (Kunden-ID).
        :param userid: The UserID (Teilnehmer-ID).

        :returns: The ISO formatted date of final deletion.
        """
        ...

    def count_ebics_users(self):
        """Returns the number of EBICS users that are currently registered."""
        ...

    def list_ebics_users(self):
        """Returns a list of EBICS users that are currently registered (*new in v6.4*)."""
        ...


class FintechLicenseError(Exception):
    """Exception concerning the license"""
    ...



from typing import TYPE_CHECKING
if not TYPE_CHECKING:
    import marshal, zlib, base64
    exec(marshal.loads(zlib.decompress(base64.b64decode(
        b'eJzcfXdcm8fd+D1DAxDDmGW85I0QEnhvG88wBcZ7IoGEkQ0CNGyDhY0NRkwb7xEvPMETvFc87pI0zm5Gk9AmTdy0zXDyJm36NnUzfnf3SEIs20n7/vNDHx49uufG97n7'
        b'7vve3Z9Auz9v/B+L/y0b8UUPFgE9s4jRs4dZA2fgDUwpW88sEi0Hi8R6Ts+XAZ1EL9KL8be0yM8qsUpLQSnDgPnAFMsDg1dhEQMWeTOgKEIvMXin++il+Cqj97706mfw'
        b'3sjMBwuBXrLIe7G3yVv4jgExOGU28MpSeD3q5T0n2yBPLbRm55nkM40mqyEzW56vy1ypW27wVnCfSzCgn0vJhcDfwqgzGY/34fC/xPltGYMvDpDF6PEblUmLmQpQCorZ'
        b'okA7U4phtrOlgAHrmHXsbI97DAnAkCxXcJpMz44ilY7G/91JxTztrNlAIde0gL+Tx3NyCEgHtSIQ2z0Id6lWJpqeAf4qlP1mciPoFEpa2QQCJesADi6Lc0PK/HpIXQ20'
        b'hZTX2Ibi+wAGlcxWoV2obg6qiJqHKlB19Ky4OegqvB4XiWpRjQJVohoOTJ8rRufRWXjZmJe3VGRR4qJf7rn7pfYLbU7WQ22EIWpbpC5O91D7akZQZrb2t1k57IWNPcYs'
        b'Bht3SmzhLyhYqxyXWDSzpw+uVIkqTetRTbJNFYmqolnQF17k0fmesMLaD2eC21Ad2g2r4Ra0JRHngrVwiwT4wQ1oayDXB97Wm71wLgXXwkYozARdhQtJfBQwIcucV2Qw'
        b'ybMEPJnU4qezWAxma3qGzZhjNZpY0gdi0iM9ZIwfY5a5ijZyLXyWzZTZIklPN9tM6ektPunpmTkGncmWn56u4DxaIpdGxuxH7n3IhVQSTiruRSr+LIAVMywjplf2B5bF'
        b'w8OAn8gv20D8PBLemJcYpdao1uVHwsoUz06OGi5CjegWqskhIK0a/NLoVHaPD8i/y/w7rHbMfUBxKivDylqlID+2G5vRp/tvVzlx6uPJ9OmZeSuZ7JQGEZBrF3/WI0Eo'
        b'sm4kB96fQ+60OcV5KiGxaqQE7PAKAzinjB0uBzY1TkQXUB3rAxuiMEAVE6ADbZkdkyYgRYRaFYEqoiPjkxmwZLE0CVUGKxgbGVZdATzvo1FFJqq8I1AVPA8beBAOn1uV'
        b'xcN9cDe8Y+tNai5BNYvJqEbjNybfEnhoMvBJYdE25RRbH5zDOGKte9RXwFLXwJNBL0O3FZwtiGDHzbyJiSqFEt5ISBYB8Ww2JC7XRjq/fww6kUg7Mz5excLaFOAD97Co'
        b'IWM+hXEsOo6aUXUKqkpIhtv91agyCZ7mQSAs5VDJHLQLV98TZ5Omw9OJ8VHxqpW+ZEhwE36oitNg4LfbQvDz4iXwAnkumoT2AJ5n4CF4AV2gLUzrhs4qaaFkWAafi0e1'
        b'injcANrOwRvoNtyJO4vgB3oW1s5MHDYcP9fDW4loc0q8CPj348ZPgA04C+2q66g8hGSJR5W2ZCGHHzrHDYX7caWsrT/ph8vwNtrkE4cHKh9Vo5rE+CK4VcWCILSfQyfQ'
        b'EXTcNhhnGzMcHfRBm6NhJTysStDYSNZ4dBlVpiThXgIjF4vj0aXp+OVJF05Ez8aj6igN2hwfpRbnB+MevMiii6jSQvtmCiqLV6LNSWSALs6LUqgSRKB7Hw5tF9kpSPNg'
        b'TVZiigrn2YFq8EBUxkclRKvjksUgCojQXhk6SltBBxamEjCU+JGaWW0CPugIi672g3ttkeTFLqrgvkSaIR6/e2pEIuYSm3GFW2anon2hKjGYxotRCQNraaOR6ARswLnx'
        b'C83qlRYRl4Q2a5JS5qbifFHjRDPQHbYNL2Q9ufYxKg4cDGa2nIN3iBxih8QhdXg5vB0+DpnD1+Hn8HcEOLo5Ah3dHUGOYEeII9QR5ujhCHf0dPRy9Hb0cfR1yB39HP0d'
        b'AxwDHYMcgx1DHBEOhSPSoXREOVQOtSPaEeMY6hjmGO4Y4RjpGJU12snQQQWPGTqDGTqgDJ2hTByz8dke906GntWeofs7+U1bhr5RQ9lLIca1Uspf1vbplL8EwqOU3BJW'
        b'SZEDc3RCkhqVQgUrCLkFajl4Dh1cQLEdXkQH16JqjKr9EznArmdi4RV4wRZKRvEKiFbCxqg4EbwoBTwsY1ApdBTQEYYn0T54XalA1RglUQXGXjE8xSoD4VVbMH7cy7qE'
        b'DFiUmsntCfh4Bj4nRQ22MFLpMfQcwoNfmaRmotFpwHsx8LgOnqcthsJmtAEzojhUyynQRsDHMfDi4hT6DFPYXlSpVCvQ3uUsYOEVZhGm92fps8FidCgRnkJN6CqmazEQ'
        b'57ARaN90+oKjZ8KSRFSFMNNhEsMAP4CBZ0fGCi+4Pxkeo2hYkM7gKjczSeg6bBSelfr6YxQdiUtWpkQxQDyKDYXbhXLwmAhtUiZIkjBNpuA3j2X94Ea4Uyi3Fx6OJHVi'
        b'5qmMUOGCa9ih4UraK6vRnYWYG0Sg/agMv4KJmQQ3DxNGYZ8/LMEvngAviwgke5iZI9BOgZlsWY6aKLEoCDlLMcu8De+w0AF3DaC14oQ96CyqTo4qiMfYb2cmwz1DBDh3'
        b'TZPC06gqCh7DyMXCi8wcdBPtcY57QnRi1AB4UEMojwficNY7tZAWG7EEnkDVcfAsugFrcbliZiasROdpY4PgOQxLijoV7iVwVjHPZKONlDei47ARnUbVo9C5KFKlUh2P'
        b'u0cjAqHZ/DBYqaRVZ62xJCqJ/EjAIwy8Ig1iFu4MkmeyHqhPsL2tooTVJAfjVpTYCqwOFXOYrlhKVxylJXYdN9vj/pcpSpzGeDPtEWOZhBNe/nPel9qXMz7TViz/DH/z'
        b'b9XE/TF2n1fccMaYJfd9fmGUz4INE3ZtqqmR9Y79V1bduCt+5Vrx6zLw9ud+6z/5QCGxDiCdcRI+qxIkHapNUaDaeCrp4GFYCkIG8Rza6EO1JdQEz8HnYDU6ndxOF8Ii'
        b'MR5esw4iDB42TqAkHJWMeWQl3C9qzdcXbuXRVngswNoX58yMW0UypmCUhZvJY28s6uGz6DSm8i3ohLUPRWy4A26H1RMsNGOSGssN0iDH9UP1sdYeOEsfVI+uKVVxRAii'
        b'vf2BFF1isby7tlh4typUK6bwCIKCSAkBmEHT5keKUtDtJKf61k6hoqlUnWrhc3WWlVRRIyoWWCdlhI8f482Yu7vyKvgWTm+xtnAWc6aZcERzAEllW6vE90RjMAe7aqaF'
        b'1wOXolb6GEWNUEE4rOxHKAdtFg+aBfgozBsmotqu9fZxAjqyWeyv0NqzO0NGvjNk/LZ+FmMhou/ZFaIvtUvuvnmv7oX379W9eKlua7eX/LI+zmFu+YHYuaKwK81Y7SYv'
        b'MmTG1ER4YHhUBGadiQzmEqfZwjhOwLFrWEFrdKtdqKavp9pVqhC6mu18nGxWY06rQr0eSAMYcwhoVai5vIwVnQ8NVp/D3KNCilSQaggGghLwyK/rcSEYCA+jAwFKFRFp'
        b'DDqFLgHezMA76MDUNkPDOP9nuwC0C7KU0Qiv0MP9Mq1v5GfKS8/LyLJZMnVWY56phhSl3Ie1ReCrJh0TSjWinZWC6eZAglKl0RBVGWsnHFDCiyK0by50/MdweLmAMNR5'
        b'gEB0sEn90bN91JjJCk1j0RqISjn4nA+80zViEs6FtRxiVHJZ/K9AzrL2yMmAzjilqG0mF6/u64aB8moH74bhl3DrDgRCYPDujEA+rvgrY0kiGPnO309nHg78TPtQ+5L+'
        b'M+0i+P5vwl4PePUuTIWpn999KfUV/D/ot/eWoDdfXfBKKnqT31Grj2Oq3hv6acGUbE6exHzxSQ4DZo7zjx3TomAEBnkmGl2zwLNxGmwMVQK1MPLdUB0Hm3quUTAC4+Hb'
        b'M7d2lCNKz9TlCKQjE0gnhGUCMIOTMkXhlmxjljXdYDbnmdUTcvJwTsskNS3g4nu8zrzc0iJeuZp8exBYByOVNRNzwtzHTWqE7+3yILWHgV2T2ihCamctI7HKjyqSlFiV'
        b'pOY62oblRSUWIhpU4xWmgFcQlheStLEAVk32QlfRRXjQyJ80MBYFLj//m7srl2cvz1muydToknQrPmkwfKbttv+U7jNtTpZ31sdJHDCcF5/9Y5Dwak/ZfT4eXeTJf4ID'
        b'xGa5O6tvZ11i7ubuC5Jzh0dffP2YviCKNTwFq7Pbd8Y1dIYFPeENHjbgT1nXNNjB9fQfiga2A+bzmjnGh/mPOAsBdsDPVxJ1RE2J0/HbahQfHZCP6r5H/7VWivtcApa/'
        b'L17/yh0FT/0tmIXugCdgtRnexEJfE6XSCBKgG7zEwc1qVG4lzh4T2jmXynW1KiIiAZ2SqdRwcwrujS3KeHg2QtATFqRLsxTjrAQA9agegrZBcvRCda2ZwtFOHmvEDWgn'
        b'zQivTPKhFSsSkjSoHN5JTsA2nKChDBwg6o12wXOe2OGBB742U2a2zmgy6NMNazI9yamvmBE+5n6uIgosj3CuVnJpdGIbY+7vxgmS+6AHTnwq6xoniLqjgJdXKLFQHZeF'
        b'NscR8ZmYjFEDswcxGFQkSoHNsKbNyLlQgqi7LpZIjc9fxZY7IAYPOtMZpJoc0i2frvWS6mcCuWH9a4U5M95dsmz5qKHMIh5QuYIVvwq4V6mKx9R8Gd3GKSJ0hIGXLegA'
        b'9UWN7vl3/x3+TMQ3+cdDfwq7O+RtwYekHYwRcUyNFOTr1v8zOEtI/EuPQDBQdhy3r+1VGd4bGL9uOiKymAhcL32RqNPrGgwNhofafF2FqsHwhfaU7gutKSsyrVG36G4d'
        b'vFTXLfJFaZDPKR17aluj4ZzujC5E8gX7lqy/dtymD5i40PDgv70TE/wteGFv2oKv3+8V1tTIvNzUMvydYcFi5t1h4uH5J7Cluqz3/W8MmGVTf8NzqAKeSES1i+c5vS1S'
        b'WMfmoea5nTOaJ7IfPltnyabYJhewbQjRTr3pR9BUZSzPyIQ7xjywFQMFdtzKsDtvnxGyUYQkhU94IOQfHsOkiB61hgvD1hlWWQEWSIAPxvYzOr/mCb5mpp2vmf31igHp'
        b'Fq8OGCjTCL67i/AQ3Ie2c0CD9oFoEI2uT6UY0xiJBwWELfCK1Sa9Lo4X0KhSz2JkjtVyQJtTuXYKMBMu39mlhUk31p2xiCxV+Meul3+jenWoH4wJmP7bvZcPPB/0zqfs'
        b'O2NFoXEbGrLnBU05UjJCfnIjfBD0v8nNMy69oFz1XfrvI7Z2L4oa8+DKxT1jX5lxcO2Rj7yqunHs4IsxMQuPt/glhIyc2P/cX9Y1/JyW3zjrtDqxeWHu/JsrPv1g54d3'
        b'3jr1ht2eeDlxUsz2PaOZDVvz0Fs9P5k8eez9Aep9GQofyl4DrGvgruEdzT1q6kEHOmol7AfdlKEDliiFAlUlRariXZ7xOLQ5crEI3oE3061Eds9GV7Cme1EDz1qdOVYp'
        b'fFEJNwLuXkSNPNSc3L296xzegjuIOj8DXrQSrTtnOK9UowpsLN5KJM4LuJlVoQ1oH7Une8ENRNARgxLWSahN2d6g7JZAYYHPpqLtSnQUJBAfTxI25n1gM4sOoA2w3krd'
        b'mJt6o62D4G5s7EdFKtRoC9aUAQiT88vQ5UzBWrwMj6LDuLVLaC+RFcSArXSbplfww2oKMTwJD8YlYvul58hWCwaeWW8lfFQOm3opUQncrlHF4w5kgUzKSdXSNpbgY6xN'
        b'cb4tI8coSI8ogZ7HsVgVC8DUK2aCGB5f+Z95lv+J5/gfeZ7/QSwSY0qXEdoe7K4rtNNmergJmeS87kHI9x9jfBKGvAaTiTIimXiYksT4hS/GoiYWlqAt8BJtMFPsQXWB'
        b'+F/qoroIjtgYdqYHKBZXSOziClDKFkvsEktSkZ+dOwzs4nqmWDofmAJ5YGUKRzG05YXAFBKDtW67lJSzi0kNE4CeISXNP9lF+fOMoFhkFx1m68F0sHTPErbYq9ib1G/3'
        b'KmXNWtoSj+8a7OLDXD2t4zBP84YV+1RwOJ+Pnc3ijMDufYzZzDCgoMY0nZaSYfhkFV52cSmDIfaukJK7UoaWlNKS0nYlX7TLzA8rZEIJF6w4/VGBto41DaS1+pSydXiA'
        b'KpgKsAqQOwyPSM/WM0LuOsb0A83HWMVZLM2bWuHjzJtawZK63TnfojnFNNeqCpEzF75rk+uMnjss0fN6URk2Z6eDUgb3s69efFhi9z0s1Uv00nqWpNh9cdlTei+7bwgo'
        b'9nVIHD5YL+T03ric1M6RcsV+uA/8Shm9dCVp8X27n94Hj4qfqb87ncfp/6uXkRbtfvVMCHnK632L/exsHWuOxfAyFF7W3EfvZ8clQjHzzmJxPn+T3M7Y2ZUcfjZK70/u'
        b'nelSfYBduOvvUX6RvptQ3p2HtOZv99cHjibfvjhPhd2PXv313e1+dl9SH3lm8rP7kyf52+y+5LdVGOMA/BYB+C2C8Fuw5u/sAeTt9MG4T1nz88IvXOYjfCd1p/9B+EXS'
        b'8Vt204fg30AfuontAezdKPwBuPWwCl/Swgpve4ALBjtXx5nDrYzdv5TZyJikVh/hzulZ76GZ80iSg619k2roIzZK3kZSsk5pSU13IsCWY8Ja6l3M2JkVYCtbwJMqnLpp'
        b'izQ93aTLNaSnK9gWVh3TwljbW/XeE3KMFmtmXm7+pO9JIhHCRb0ysw2ZK7Eh12rrtWZ7xMnzzI+YqM8JVI+887Lk1sJ8g3yQpQOYIhf1y11ghpDpbTsR5qyFr8AglzJO'
        b'kJe3AoaZZCSVoKsewyLNhC3+4ILYTKT6I3+dfJUux2aQY5giBlkUVBA/CrMYCmwGU6ZBbrQacuWDjOTxkEGWIY+60QRy607i6bW7R05X6Ude8lybxSrPMMgf+RuM1myD'
        b'Gb8z7gp8/VxwJT1ihjxi+j/yGmRZrFarl+J0ouI+6hYlX55ndfXSOPyvkLWIjCa9YU2L9zwC8AxiNOIk3Kqlhc/Myy9s4VcaCrE5jVvO0xtavDIKrQad2azDD1bkGU0t'
        b'YrMlP8dobeHNhnyzmVi1LV5zcAO0JkVgi1dmnslKrBBzC4drauEJGrSIafdYWkQEFkuL1GLLEO5E9AFJMFp1GTmGFsbYwuFHLWKLkIFZ2SI1WtKttnz8kLdarOYWfhW5'
        b'crmW5bg4AaNFVGDLsxoUvp2qqr/kgrVNjRtDpS5kfI2gUjlFLqLZ8gyRiDJGzBGdlscfKZaPgr4rY8JYb/o7hKbj/GwIE8iE05QAcRC+F+PUEOq/xXKVJRJVhlPxL5bI'
        b'UT9W0JQDWT/q5Q1jgn7GLf7MskG4FJa1LJ1V0qOro7ECH5eMNgdiFSgqQQL80rmx8Oz6NjMERA6KXdTwAF+w3GLt4DCgsuh1LLe4Yt7OWcILZFas4JJ/I5Zz+zki3eys'
        b'nZuAqcaciiUhswrgbywzeoDDLOaTXA9Qj6UPlkg8lgE8kRoWvZ1fzuD6eFx3KpZeHJEoWAruw7RHZINIT+oT6XlcB0d+4W8sFUk9BdmClDGf0PP5DXoio0V2CW1L7Hwu'
        b'Elqn9bATAP3NO3/zE0CBzM7SeQyRBpNvMhlGOpYp5JLsviNpCpF5ChlhzmKwtnA6vb5FbMvX66wG8zTyVNoiIciXq8tvkeoNWTpbjhXjLEnSGzOt5iRXhS1Sw5p8Q6bV'
        b'oDenkrREUlj8BDTz8K+SKAx9uqvePpiLWQZTLOMxthAsCxAwAWOBmNpUBLsCGPIJZOiEdhqqB85pfnQc7YSV0WQSMplOGQIlvCpCu+bC8g42CWmeqFW0uQ4zvoDM+Wb5'
        b'uAwgO+OaHWpvN7mVLD2+VJChZiqxsF8B8gMwmuGC5hEYNXxxCkNEaCnjgw0gKqQwUmDRx1RwFT7kvpLE9/AYENK8NwZHliV1O0W97CxBos4sfILZpFOpT/U7AgRvJxoD'
        b'KDqFG+bIPdWc5mCcZ3FjGLRSZiXAYOE7OwakmDOFUPDEGLtnkjucwmNsy7FzNC2kgmg0mA6IxlUhJljv1LpC7KTmScWcndaL81ZViDG2clir4U0yco/T6S87b84nMgdT'
        b'Ea3HzjvryMd6ZwzWO3mrKIstfMBgnZIBRUG4s0REKtNQMJy2TmTyFr5JKBimE0yjdobUQY1ORoORjpgYLZJVOjP1hnLLMWJj3mpeudocSxAuXkDNVgdoGrlQTM6klGDA'
        b'zFz61LyyFYll6ZRL5uOGcy1T3CiM0ZVlAyibxOyQJawwnDJPGSvDqB2OEbgPUxSjy8w05FstrdJeb8jMM+usbZ29rQ1gCa0jTZP3wEROg45ogpEk+Pxars+1SEi3YVoW'
        b'qsxwv56XG6AxjGsKjhOEQB/MisN7FIV3/Q4upUJLqltJ7r1/lUjSusGROBsbyTgdCoCTDxDiSBoXo8uJvrAsSaNRRSjEwEfNomNwJ9rYwVnq5fy2xOGLASzC2t8idodE'
        b'cHxgHiDNEgnEV8os4mg6Db9zcggvTJok2JE85R2AB4tEVHcUtXRzhiPONOYYkvJ0eoO568nqqQAIvj4RDTkRZ4nd9M4/9STIU07ESDQ0jqgfughLW0NpUB0H/OApDt7x'
        b'D5hcZIvBOYLTSHCAEPIX5844EtakogqXs+IyJpwlERK0A26S0kKoDt3BpvnxlULJiAhUFR2nQlWwcU5EQjI289XxqoRkBpj8vSZiDn2Aes+Dp6DG2ap5cahGkZCchLMS'
        b'B0RKUnwy03suGAF3iQfOMBk/3LEXWIi2Pcu36Evt/YwGQ4Nuwd098Fpd84ITZYpNjeVT9tfvba5sLm1cwL20XNy8MmzcglfCqnJK7LvCxUOb7F4WybSJ/5RYhr/N7vLb'
        b'tanmnmx/D/C3osD/uWdUiKgrIWQJ3IqqE2loF48aYXUfBh6B29MEV+HV/oPbeSsUGjm/jJNS54pu4DB0EdWoSBRcgeB/gdengXAbD8vD4DbqjViCmpYq1ao4FQsmwzNi'
        b'eIyNQfvRJerkgQ2wApZzzySqE5Kj4mGt2yEkAoOeES0aAGtcMyBPL1J9M80GLMbTc/P0thwD9WIQSwWsx5/l1E/B8k5PZFHfDuiqblPaPb9kMeRk4SvhDq3OSlHXBMua'
        b'88h9vgsqM3H26hmXh7QEfw6GdOnveCJcHYjKPe2X4CIqT1nOYIr1dhOX6NcTlwh4GFZu4vITiCtrNmxqR1sRGJNOcQGo2s8WjXMszFd3pK32hAX3F1Haem6YEH+5AZ5D'
        b'ZZ6EtdLYBWnloFOPn2h2zhE4J5qxicpktTdJpRNydLkZet2ktYzTvLPNw5foKPicxQ1yfpugQbQtEZ6NS4ab3diLadw9I0jnA8dzwwItmKYC0VkAz6DybrAE3UCNNkJD'
        b'oaHonNMZWoOqo5zxJfA6OpvGDY1IbfNGIuAxgUz5p6AzsWSw3fyTq8ADWczjIeboEPN0WLl12NRtvX8c/3QrdZ78czxpF9bDo4lKrGyWxSaqhWn+2XFKEi82F/MAlQJt'
        b'Toqf6x5QEYCHDd7oNtwP91MPdvQgEbg1I5REf0f19NMBihWz0SnchWTSyFWjEF6LKuicPtwarYkiIba5673CVqK9tAy81U2aSMMz4u1RybMiUOV8gX3Ocjc+l7CeZgk6'
        b'PwI2GH3fT+YsubjgFP240+bPb3ejMUv3s9SBCl2SLicrJ+OhNsr8hfa1jJczXs+I123Tv5Rx1vBZ7IN3Y8Dc8czc4aVzHMM/vd8cs6Np7uChw0rkqfuPl87YzwwMvV/3'
        b'Gz145/f36u6/ee9WWfOWoXs2XMSMdGqPiUO/c4U3NXZHpzrzd8PSfiS66QI8R7lpkSiRctPV6LoHQxW4KdybLMxNXoWb4XYXv1TNascxJVG0JsxVLyGHc7oxpVeqs0Ff'
        b'dIELS4Fb6MQ9LLHB89h8dE1JqhXawWIQuI5DNT5oj5XYBv04uMmVIyU+AO4RAZ/RLKqF2wYKzRwyoYPuuX86dGtdc//94alfzrv9yKR+er4ZW/LEpKLMO9zFvNcDKUsN'
        b'bGwasYHU3RzIFI3syCoNawyZTkbZqpG1rVlgACJB1WvViJ80EeWcr/JzF6C83YIvmwhv7+/i7SXgx665u20JzpWWBMv/A4bCwW1jUbNoBroeCy8Pgo0K0B+VrUE7g1YE'
        b'oEM5BNbnlT347wJBbJP/v4b8jb0y9C8BeQyduJyQsJdpkgB5jNeOkX8wP/INAjSZ6eecz9Q+4/NT2JWRFmD88PVAxnIKPxvz7yvBNePpFNLqnCE/HZuRgJgx4tUfg2ML'
        b'FvYfVNnwQPzM397KL5/+4PCYF+L+XhheMKA4LpvL/I31YLCy/uCwjwLGL13xO8dy9FrCg6+LRrHfLsytvda74cPDL9Tm9p/lU3vlZcPc+7t+3/Lv0IMD3q6tUuTWPziq'
        b'e+XtPSabl823cdu0BU0NFZL4Af3+5IjednB8c4+HKc/Xn9RHHn1BXX5TOWNn8Gdr/vGtf7dvVW/o7AoZxe216LnRHdZLLIGnArk+6KKW4rY0KqidYgOvDceajRjV0ziw'
        b'kBXjnKoNruZAe2o8KLISNyEeoEOZApnhAZyxmg4mrMDJeCAFTj5KL146GDmoKgR3TO1GVSF0ZTILqCpEgs0oYaeh8qV02Hlvj4EXgZ4jedyAA14SYgMaYPkqJyuhuAKr'
        b'SCPBsBTtQBs4dGmNa4JoW3csYaox0jQ7VTui1i3XWmkM7On8AUpTQBx9b340A8/BU2I6hbU2p7szJNId6eiL9nNcP3h9He3ZMehqbEdplQj3YWE1mbcGURY1WoeqkzC+'
        b'94BXxwDcIcciHqcr/TqDSOxmGj4e9E45RoSLY1jd6h7rTdwpmBgD8B3PBvqL8TUIW6dFvR/LP5wKINXmWsTOtFYu8dTWMlYIbeQ+z800rPhS0EYh3Nqna4Xw8VBiDku9'
        b'sN7pzoT0dGyUpxfYdDmCB56qn7TJFl+yiEdnsWQaMD9MF97P6xd1fiPT4uWsBFdAX4ZI1gzyMkTIS1mWCZFhPqciyHAcE9DlrjgdC8ah8wx8Tgz3wuvwcAczVer8thBN'
        b'0GWmGrDp6XRYEe1HhPUeVs+VebUxRrM9jNFUnRV3nAl3miaT96idoJB7ap4Ywm6lmarMNDjQy6lT8RVSrFOJsE7FU51KRPUofh1uq/W+qzBqolN1VJtFgtqsh7WijiZp'
        b'MDwXAJtG2ibjHCtwFixlI+KS1fHJs5xmoioN3kDNWEeaHUH8fXOlaHO0x3oWJhGAYd39vUags0bV+b+ILItIU/dEX2qX3q0j5uNL58uaS5tLj+81MrMlKyVrJb+Z+pdF'
        b'5eHl/c/7XQkvj/qL34msExkXA3cFnch6cfCLfuK6BSHKPQNi9CuzTukqlp/TSbPimIzXZeDVPwSnbRmONR3CPnJ6oo3tuCoqU2Oumg+bKQeckIfOYw7ohZqJPShwwK1o'
        b'F9UmVtrgddoRibASlaMSYaVMoIGDZ+AF2EDt0VGwso+wtiUe8586GuF/nF0jhQ7KneZ207W3R7HmL7Dss+sFcxfVo6NOezcaHRX44hi0iYKHuxLWKilfhDvhBYE3Tpnm'
        b'UmR+GZ14hq9mYfRLJ+ZjW3t0PejvLSMz6jLMooKYop4dMFbtLimQqriFy8yxtEizbDmUtlv4fJy3RWzVmZcbrB6s6QlKF+ZpxeR+HbmQCHBziZs12fHlUDt95k+9umZO'
        b'j4NawWo0TvZkXkUuq0l/+FDukWuwZufpaXPmNa4Oe4ykMBe6QVyLLwdcDjDCcOhKKVRmgzdaeY3UYy0YxpTxmHLOysXw5DOolloji4dxgF9IlDmtrH7ZWtDBR+52VU0H'
        b'7ddFZUnc65aYp1631IExtOFAbsbQQ0Mt335zYY0Fo/MlnwIbuoK1iquo2boKXfZZBWv982WomaxPOwEPhotQU2pvGwlcgrvgoUlkfVqSBtUqNXOplR2PvypTVM6VrKkF'
        b'ZKlKRZQaNqeRNWHwErzhje5MVz5x+S1HZ+X/S9GanbJDapbUzpmlhA1JzlE0ZKLNOOccDv9uQjdsdD3s3pUDCBMQXhLrxs/NU8LGCAaEw628WYo2GDOHmXgLmZ7hpTlf'
        b'al/+6xfaRXeb6uq3N5Y2vtRYOrS6gKm7XNftJUnz3vF70nr+T9jsPSHDSj8dH/ZyWPXDcWEhTSVzYoZZY0TDj8XwNHzurQ8Cd+3r43SYoV3ompmsrKqKgg50C48iPMMO'
        b'954jqFbY7lqPOYi+wK1bBZsobyr2hqepGwNVqdCJ1YLy5Q83cCtgA9pOdVKfAngZZyGrr2rhBrI+jR/LwGZY5mRPqG6NItFz0cIweLWwT+oT14/46PLzDZggCatoz4Bm'
        b'yij7CaCTS0WRmImk5xgzDSaLIT3LnJebnmX0tKI8KnK1SplH1yHXmHeud5MtWUL/fDvOcvsxcT9kto6De4sTU1RYJmCV1wedF0Yd1qZQtwP+FiReewvJ2U+wMlroaT08'
        b'GJALG7zpgolBa7VKosEOH8XysAGI0EEGD9weeIiuoMTG+oYFmIqaV69ClwrQKVQjk+YXyAp4EDKeW44OoL22IWSoS+BtdNSCLqFmBm3z8l3l6+0nRRdWE5ItEIGBgXwx'
        b'3ASbhGjS/fCwJRELRtLqInibw8PXxGKpVLLYNpE8P4iOLMX4sR3b91vQPozbkQlR8BTasToqggj8JNeiitlS56JjBsBj8KLPNNgw10bW2aANqBnuIBXQwrYZTyy+K8cb'
        b'beoNK4VFphdGwApYnV8wCPOQLavRFXQV8x4rBuYqWSdow+8zm8c4eXEEJUF0ORyjKIF3N9wanEgcCFh0J0mAP9rKpeEBsBGOb0C30BlSKTqS1qbS1ahZ5i0GA+N5bL/c'
        b'gOepNk8jInuhnf7wIgvgWVgNxoPxsBrVUTVpPTqNqW17iioe7YLn4+IlYCSqlE1k0cEiuJt64WOnpfmoyFq6xPnCO/eFhzy4ILxM+d1StEECb6ESPIgEX+WDJ80Wg2wJ'
        b'GAgG4ooPUMFQu0YKAkCTltdqk9LmyYXoy+OMBMjAZ2o/uTZqRNAzWKWnyaYemEpBfqo30OYMVVmEvHfDxThvk5mXa2UPp48DtmE4sQhtySDaiZL4rSqpp8qDT8Oa9a1A'
        b'5sESaXHWdOMq/iveMoMQTM7k5NRmDYoJsr+heetEsk9Qw8dDAnJkwd0ztKeeLwl7/2DDOwlb9yUkRSfObszasG7jc/LbJdG6jAfDx/3t4Ym5hg+uv/3hze8nbBwdcz8s'
        b'KnBc1Ib6a93Pncn6ZsLHL/3pg7vTRw1+4c3Q8rqrsvfLuGWnBkVtD03ed2TGxelvh42OONiQ8fqCk0P8lAVfr8lEf5+w5tkHP8r2XUhOuLpsheiNH02nntv94MAH5e+t'
        b'cNzQfLDDr9dH0DI4t+7el2+n3x/3XTZ/fJj8i3+vu5qh+nCR9dJXWfJdGZP/WTBvxe+ufHW4ps8G+ba5xusp/+M9b8zN67zsy/hRz4yyTPrnkZqxV3rv3fo/3tX1Tep/'
        b'9PJWzxvT+8K2+dU/pk/wObn3XG3W3H69U3Z8f3vBb++Pff+dDc9wL51f+eN3c3944Y3Xv/rgUMrAhu53/v6q/B/F273/+tIXzFsvTJ76RuGbQ7cp/IUozAvwNqxLJLsu'
        b'VEcRHsIBH3RhQBDH8qiMWrDwOipDJZjpkEWbe0esYqYkz6Drxli0F11Xuuxmcwjm7ujAZCoVJqBD0xKTItXCQ58ceGABi46l+VK9GJ1Dt2bSheSUVx2eIwJSVM0Wo1JU'
        b'LnjSqlC1nzKFgEPUFQmG6DY8j3axmB8cQA10naFvANrn4moHB7piPm+h08Jb7ZkE9yhRRXxUPJUxIhCFrvtP4LLQeXRYcPjdRBvgjkRiSBAde1+cQqXBalFoEh8bCZ+l'
        b'AghdGwvrhFDYKAZuh1uEWFisom+j0m01M5rCh6olgFcpIxh41jdbkHtN49BtZUIyNvv5fjnFDDwQjRzUsTFv+khnjagSnofPEkaUiHE8FF7h4+ABuJsq9rARbUMVglQF'
        b'8HSCIFSxOn6Rvt1YdD5PMCxQuahN4GwNfPaJuq7kl7oUgjsVg1R0prWKzglEcPLUERnAerMB3vifDWTI1ZsLwGlh7olvGY31iaAx8IG4jB9O92NJVAeJ/5Gx5lKXxG5k'
        b'PYTp0wDuEZZGKrnRTry+FNa1eKWe9NrCOLd47Vy22tBtEVhmlcKdQzQKTliXvhPtHO+0oiTopmBFwTsSYbeG8+iMEXO0M7BeA88mCUsMfOBlFh1flEvlLzrKostKFTqL'
        b'qjSqSDEe7MN4sI/A0kyunY4Y4tITyXx8h00JgHtbAqbNxgSsIzgrxD0bInqq2RCOqqr8JwPxMHvLPf7SDMuNFqvBbJFbsw3t99tRe7fJG2+VGy1ys6HAZjQb9HJrnpz4'
        b'nXFBnEo2UyGLKOV5JB4ww5CVZzbIdaZCucWWIbht2lSVqTOReD9jbn6e2WrQq+XzjdhcslnlNNDQqJc78ZNC5aobP7AWYhDa1GQ2WKxmI3F7t4N2HI2okBM7cpyc7ClE'
        b'7kjcIanSWT1+w06KrDQUkthAoZTzR7uCevkq3GcYpk4rsFnwQ6G4O/+MqfHTZtMncqPeIo+YYzDmmAzZuQazKn66RdG2Hmdvu8IidXLyjqblJCZSJyfxogQcV11quSYP'
        b'd1x+Pm6LhBh2qMmYRUsJHYrHKkNHAMJjhcfGkmk25ls7vEgHD48faG/S+GhsZJXbIliSOxudQBejXTOWafPjsJ46Oy5BlDZ2LGxUeKPrhWPhztj+Y4NJMEGDrAemoc0d'
        b'iCHA1cK8tsQAnOTAuMmBdfhnBfyK6cAOthphLh131lBhPiBMonaMCOsY3yGACdzzk//R3k2kuY4rukTOtcOEhRv7Z/XiLAX4rn/Vz71rmn1LY4OmfeXTd2u3C1O9Bx/W'
        b'c+MGjtvxZf9N0siGc0MX3z2Rf6f57JCJr/z07kt+kfrKyJl/qYn7oUz09uJX7VfzFNWrldK9A6+EffHac8HR13oGLtdM/GTL6/77b4f/EP7Bve5lff7lfbweDV92cHHv'
        b'Hy/9qGCpMMyaE4iZ2y64N0Lwcu1jVZMXUguutxldUKLNsGouUcF5G4Nl4m106ZfPlInSV5t1+VQi9WmVSOtBOIlFxXKHuLqZIEaMpY2UKVKYnTzMI6TKie0eKaRG50p1'
        b'IZjxqb1JjYxQgEohEiUbiiGjyy6dUqgEfPmYCTFiAc2Gp+YrCX1kwK2ERDxX1TrX1LZKqBmBiuiEKABmwgZ/owqe6DrIaJJAKeC/t8q68xgIicY2A9+j7YP7DY8ZMWzU'
        b'0JHD4VXYZLWasTXZtKrAZqGG1CV0AVtBzegyuugvlXn7efn6wC3Y8KrBFs8xdNULndWgC9SESJ2QEPUzF8GAAO2KvvN5wa4I7B4X/h6QM0Cr9bZqFznxvfu/fstYyKTi'
        b'11MmBf+mX2BJjIy/e3OEuJq5vTH2Wy7q2utzDscOOXXijez1CbPG9/w8Ln9X6rGYVzavnPjCC9M2xO+Iajn34Tfj7707onzxH88q/75+XlhS6IjAN8Iuv/X+Gm1c32sn'
        b'grLeuYdRm+ppDfA5kcsHgRqXClooeg7eEB7XrCbzQkR7WAlPuD0YmXDr42aAnrS+UJpuzrOmZ2BrnfR5mCe+RxB8D8SYLqUR10VRT4XpzupcszvuyN3H+TFYIUcrnmMN'
        b'FAzqgOcfPmY9IoksJhbqEYwBpUqXMHgSpqOqaFiZMmwUB1bB6gB1aB5FhcJ1XFw4S5ecJv0xaxGwkSVPsBRdGIy2Y/RUg+IkdT94i+aNTJKoMwDd2Cxqmd6521nGQl77'
        b'PRtAYjFyRnQzCLgkVJ0unVrIynHN2pyxfZ07poXMTOz/B0Dx0Xtb3hQh8R2vAKzsxgKQr006FhkCaBjiel90eDaqRTvmjozJXouqeCBOY+AZX1hGy0i8ey74GmRjaaad'
        b'MGJmnlDRfP9mpgRLj2/Gy4bks5o06jSB1XB/9GxIakK1cCc8IQKclpmE7Zha2wjy/IJ8aqsfcO6oNXHYtkEVUQnE10nsHBoMgrYoibEAK5XeCrYHnet+bb4YYLNMDmbm'
        b'JNUUV/c5B+h64G6awVLpyBOjGW1SojlTNTo/9fVRi/qfk9gIqcMKdAhdQxex/EkGM+DtZDCWQv5w2rjUAcxn5HUCF7MG4XVg9GRQBkBE7Ngz40qMA6Jp4hezJifZ2O8B'
        b'iNGav+4dLOScYYpitCwIuDv21ZSJY1bPp4nXZr/HXOJA3N3RUf2HRbyQRhMDsmcyO1gQe3dkzortQbOEdaJXhwUzMRgH705KCtGPHGClifVDreAb/B07/kzWvnV97TSx'
        b'+7w5BX9nU0UgQOdzaGC40Hpach0TwYGYu8NrTHmT7BKaWD5gIbiG24ud+Gq3JkXaWpr4yuABTBILxtyd9OqEfYOcmzmmxPQB08lrTjqTUDDhbBFNzJuWxBwmbzRSViyZ'
        b'H51ME0ukoUPVzAIeY+DEePkEofWdfX+7MpqNlQCtzv8j5UAh8VD3F4IesAEcRst4MNyZ03+ZPXIB9w0DUrXzqqY5uy5D82GvC2w+hxMX7lrh9NKEJvr2CQExmH9qZXuG'
        b'9BASrdoCUIIHLn+od9S9sL9xxgqQJ7IcxSlf/fnR3FmvbH47NuDhQUffZ2u7h+Tnr4n+N3heN7nkT+uYsfKAPyQwirSBD54rydJk/fkDn79tPfqa5NuR+7tNXFZWNvPt'
        b'D+eea/y8j+PWQYnyZsNfPw6+/M7g3BZNy4+rbmgOH76TNenCiQNnR8rOaL/+/pXVz/TL+z7Sf+y2qnPme5s+nnphZ05prT0lztHtHzU52vMZI+ve2/ZubNLm8zsD/z40'
        b'K1jVMGtrcfz7X84YOy7sN+oL3d88fmr6hh9nVqZ/OqP08/W3VoV/sC0jKv5+8Uf8b3OTfvOPJd/dql8gmnlh1ns7nw+sfO/3qyM+/UNO/J7oI+jMwE99Fp1Os+8f83DV'
        b'lH9kHf7oQfmr+gOrRt14+FH5mZT8mKZXDT9/dKX3nbQJwR+iZTFvnf2u4tlr72Yf4mt/H9F8t/ecBQ/UX38yqc/H/fp8MtTv2+mDx5u9f/O3t4a89Vrj8DWP6r1f8F83'
        b'448vnWw++mjIsavvXZo4zLp11Q//Cp295MHE3PdPbjsUr/nozXnXdAdm7fm4EP31u9vfLHxTXVu1efKPqyoTR9+Y/Y/q5iPrd37+zteyS0e6Kab89W/Rn+78XdGMrW9M'
        b'/okZ02vLYna+QipEoh4PWuj0I8AbaKdzlS6sgnuoZyaVwanX0SYlqogmm3fVM6moug/1mySjCxOUCapEVSQ8iJo0IiATs+g51JBAn8LjcL8fkVjjfIlv1uVyv5QqyLM7'
        b'6NYIzD9S4rE1uwFd4Mlmaf3RDnSDFkabxo1QqhUJOEfScBpm4Y9KuLyVYYJL5iLaU+x26miXCm4dlmwJgi4Jmw01Sya3iZ/iQDe4g2w5ycGm8ejML5xxVAT88lCKp9Y4'
        b'pS45SoVwhqcQDpExPBviF+DNM55bU5HvPvg7DH8CmYFYJvbCCqkfXSYVxPBcIBOCv71/Yln2JyknpqWkdL2ADJfjyXxEeNfiXNBURXQBQ4vEaYO2iKhh6SHH//MFYVgb'
        b'JvseCSslat3ivwpfAjuI/28iuxb/Y3G+4QPQ0SdK/lh0joo0EYAOiJXCW7B5IHWoB8NKBZ0Yc7uQNfAsajQ7fSzR8JIInYEbYbngpD+MKz/YOh0IL2ehmjTM2dEmrg+6'
        b'APdR5jhmIgv4OWSlu1b2cnqaUx4reCC1QgkJ1ESTY4XEojESIAuKY8n+qEszIoBxF5AwlkP4ybcH1vWumegHY2QzvxpsfPvSn0dLC4aMmndMPe+DxTO18rhVJmb+x2V7'
        b'/FIuTJ68PvDF//Uu8zoUoVS/3/Tnbcpz1z/ZFXrrU9+8wtHWOXWF/ypbXWcat/1C1fwjDwL3J3994Y1vT4R+G7j9/idM4IkpJQ//8IfbW/efGZRaWFK29nv5qYnrXlBa'
        b'It8PfbTlud/6PTw7Yt/89YtHn7x46MC2j/l//FnyNRu99I+TFBJKbYnpxT6R2VPpdrsdNtuVwWvUj+sNq1UePs4l6BqDu/hSkBCvXuulcGtnl4XpBRK1nkTmHg/yed6Z'
        b'gqe1CV3v66nFJUzGrCEwkoMNI+A2yhvWy+A5koOM335f5/j5wXPcdHQ7lvpiYR06gPbB6miVBu0oVqGqJIUY+Pfi0sNmUL8qB09MgNUpVOVZpopKcO+61RNu5eFRY6jL'
        b'qAz5rzOFp2YZLuqlLCPSk2V0I0FZLDN4poySO0tWSrIhdHmQmDIJ8xac22nVV5PX6P5/DfdmN2mTpn9o50ctH9U1YQubuMLbqwTKRuWJahJw4D+Ky0KOQZ3OfZM/i4xp'
        b'jWrSM4s4PbuI13OLRHp+kRj/S/C/dDlY5IW/vXdwO3i9qFbYtIwEIPB6sV5Cl+D4GGR6qd6rDOi99T617CJf/FtGf/vS3374tx/97U9/++PfAfR3N/o7ANdIPaq4zkB9'
        b'9zLpom7u1hh3a0H6YNpaIH4mJR99SC3ZvIzs7heqD6PPunfyrIc+nD4Lcv7uqe+FWwh2/uqt74N/heh5amr3bfFLErh7ss6kW24wfyJp740lHsO2eeQ0mKRNpieVMFqI'
        b'a5D6Z/WFJl2ukXhpC+U6vZ74D82G3LxVBg93ZNvKcSGcicwKON2dgq/R7cakJdTy1ByDzmKQm/KsxEWrs9LMNgvZo72N59FCssgNJuKX1MszCuXO5aZqpzNZl2k1rtJZ'
        b'ScX5eSbqWzaQFk05hW0dknMtgo8aN6Uze7hVqfN5ta6Qpq4ymI1ZRpxKXtJqwC+N6zToMrO78Bg7e8HZqpp2ptWsM1myDMTBrddZdQTIHGOu0Sp0KH7Nti9oysoz59Lt'
        b'A+Wrs42Z2e095DaTEVeOITHqDSarMavQ2VNY6Lep6FHvbKs13zIuOlqXb1SvyMszGS1qvSHaubP5o8Gux1l4MDN0mSs75lFnLjdqyNYE+RhjVueZ9V07jmIB9V7ywuo0'
        b'13K4YpY6U5/sOuLogjj+0aaOTmuT0WrU5RiLDHhsOyCmyWLVmTLbTyuQP6fj3AW54DvHP4zLTbgfp6TGux91dJQ/xT6aYiHoCF2ENai8s3Vss9DmduttbGIaB4Hq0XF4'
        b'2FMtiYiLQsdnqtVoS3QCA0bB3eK1IUUKhsb3pGXDK2Q/4xSVGm0kcaCoNoUBgXA/hzaEFhsLKnQiC/Gx9FuiIgveIh58jq9RIZ9r45zLNNTzInQJOvZij9CY1THR+iV3'
        b'L9TVb79eqqi+XHq9dGi1atP13Y2lgw5O3NRvz4bhHKh9c2N6t0Of+WEzgnDzoiV5noKZCm94UO6U3/AkPEFVBViPO+GoU0AL0hlegocECR0Kb1AJndB7vs+UXvidFW5d'
        b'Ihg6eGkaKhHCdZrgxR5KVIr1/81xI3jAoZuMKUYrWA4V8DyZhKYdwQCpbTGsY+GGWVPoBHRWL1ifiJpQdaJKQndaTgwYRbWTMfxiJals2EgOSLB2sKmIQftmYmuEzjLf'
        b'CEXn0WlAX7AiOUkMsDbIYKuoAZ5/Ymydp6KfbsQ4mp5OpXaIp9ReD7xkdAEGUdOLQtsir9pVTpDajULUtJnsKPikhRWNrJCtNTya7Mm4voN2XRrUdRRiV9B0vSSM6LR2'
        b'sMK1+6iCxDW7Zr0aGQGYtsvDzGZ82YzBErYqad+ka+3Yox5dTqbhRjh9XuZTAbVcAEqa7jRuzPu6gGirC6JHQR4Taq55OfVTNVbmaowwXqPe0mVjO9yNRZHGXCpeJ/N3'
        b'mTlGzNBVFszXFb8ICJ90w5p8o5nKjC7h2O2GYwCBo7UEEUrtO75t8y5GTzcdjAWt+7A6RB6M/unnCDrd9K3jHIFY2PRNjBlqSVrIbFTLk1MLANyyegJ1Ma5GlyLhaQxo'
        b'cTzaBYrJKlm6p3k/eFaNquNJ/MR2dALVDMe2GaxmEzDz2m1saAjhLItxrj3lB3tX3+9WEiPjBg3pZSx5Mbsfl7Qibpl9SfmHisHRXz3MHtk44tatsW/q5gxeNuZf2+es'
        b'uPLpmBONGdclvhFrf8g8rroyTjw+tzrj/P2xKxftnfTZtu5//hcICO3Bx+QqvClTXLV8npN3imCdpr3ts2Co4E/ZNGQK8b3G2xcLYYroJgsrk2Ct8PQiPEr3LYMlfVs3'
        b'LlOjo9SJEzZ2kNJ5yATcD6t4DQOb1iid/HIIuuWMjazhsCGmoX6aAJngHNozF9W42J4m1cX4MlA5rRdV9MxLJGc+NPAgCm3hRzHwVlqiwKPro+eSvbvhviiyd7Cwd7e0'
        b'h8BPy+NhWSIGE23GTLS0daPEq2gXzfBMzzRUDY8Vx8GzcS5OHghPc6h86PI2u609Jd81mDLNhflWynfphtytfLcP2UQhkDpVvGmwZkd+5yztuWTl6bZXdG6K28p8j+LL'
        b'Pta1j0OJ+/PZL2G/TnD+TzWs5Z1qWNOydablBiFcw6UTufhBO30Lq01Pq2qZDKufVsMir9xxDS2vcZ1mcjo40KUCOdWf8b5UAcqAu40rB2XzlhycrfC9xcE1/QJLY4JE'
        b'f3zl59T8dyeKlmxQysfNHTmr28jLhxvWVLylHDg6d8+Bkcp5r9YFfz34jR1/Tk29NrVuyO+/v3l2yR77PebB5h9flp7PmXnr3ICP3k798v7RU3X7irJ9nrdW/iD+18Xq'
        b'Pb9d/9M/m0MSulkUXpQavAvJBoZOZaUClRGFBSsXVNsJiMc6S3UKWaYLT46Fp6IiGOCHajnD4oGC02M32utND0JopYXVuAghh3WjaPXROrSVODRQFQP4pfBSNIP5we71'
        b'VqJFRsBbqCqRbhqbmAJro+OisP54Hu0TdMgYdFg8FtbCSkrP+ZgLljuVozFYC8L6ETohFRhMZQo8TToXHXxG0KyoXoWtE+pTOVCIKskLopPojqBEEQUKXcEaHVGvgtKz'
        b'PJQnmZhyEXhl8C8nZv9MioTpLoxpH3ZNPtHe1NkZwRT1aUc87Qo73SC7uyRh8x437R7Hl+Od0O6Hj6HdJzSv4FrE2XkWq1Hf4oUpw2oiCkKLWFAUOqyoakvfvGvZhJu+'
        b'eRqP9eSVVE76/mQq084DQP6m6PXEeiI06aF1CNanW+Z3SdjCywhkHYfv46e72EOGzrSyI3G7+YHz3YWSqcJPXDgi0WbCtqsqfnonQUoeAU+uksRSJ8XaBDgpOoPXbLDa'
        b'zCbLOLl2jtlm0JI4JWEjCH2UXDtTl2MR0nQ5OFFfiJUgoouZrL+KP3Ea4/iVkQxdNzEh8+Mvtcvuvnnv/Xvv3LtQd31XfWl96diQrOrmvc3pp3Y1lw+tbiyv39Jv/4bK'
        b'fps2iKTP7u3RY2MPWY8qlSws7F5MYMXskoz9n4OkVN/R3nIFR4V05AroYiDJfh78o2CZQLn74IZAN3eIZtAmnP0irAgW1tDfRns1iUnxmL6TUVWSGm6OptGrClgjmhwM'
        b'z0JH3C8nUj+dXp9uyDBmWqjWS2k0oC2NxhIKLerdjkDalnPaO2JBgpLNic0nyaWhrfD1PO2B98iW585LCfgUvlzohIDffAwBPx6+/3MSfaYzEk2jXjRMpSYBLUlwnget'
        b'evjP/v+jVlIsfnaKXPB8WQVHGbVJsowmXY5cb8gxdIwofHo67ZZiZCmdHnz3Zhs6fW27QKm/iE5VICnXd86HKzGdEq0zd7HcJefdRIqOo0oD2j9G0MW3whtk9gKT6obu'
        b'TmrFlHoxmQryFbAUXlQmoFpUG50Iaym5auPcBDsZbpYEMnDjL6fWboJf9gkEm0IJtp2ep+5Q1ClST7cjTPMZNx2ew5d7ndDhvcfQ4RObfcJZOYwDeJyV83S7jjvjlh9l'
        b'dEKBFB0pqZhsuRmY6jAGeri1W53FmTazGcuNnEIPe/7XIid7MpS3PIMTkv9e96U2WLmELL2jaDn0iWhZ64GWRvC+2qcqZglGS3rQiANtUrgRE91Et90SBO0bS/VLr3x4'
        b'2iVBMEJuo3i5KNhKNgSYCxvgdmIEYrvVQ4igalZFQ9Anw+sSOdrq3+68pE4RMTPPZrJ6jKqlM0ScL+0METsU1bgiLvO6lBaCC4QiZRO+vNkJUl7o+oSgJ4Pwf4SUxDgz'
        b'dYmUrUHaT42Q8ohIovAZTfJVo9QjIjvh3k+HoL1yEzmKoNOsfyDnRXWFnlfsj0dQFXg/yadhZDFGUGJcLEQlsNmDc9rHONEzfCY1LoqxsXcJ1sMjHkoOvMjPoVwTPQtP'
        b'5MJdUcI5gG21HIydY6BDDC8u7fUU2BlA+vVJyJkubH/WDjPal3Qyyeau8fEivrzfCT6eegw+PqlVRWj75eKS9HR9XmZ6egufbjPntPiSa7prlqfFx71Sx6g37yWFDpAL'
        b'iUsw1wOnL7lFmm/OyzeYrYUtUpczloZ1tEicDs8Wbw+nI/GAUFOKqmNUFlDaoy8seFh+xbYlHh5McozVCtJxMwmWsrwPz3h8WCkT5Iu7j2F/EnNdfPOBPjiXTMYE+JF/'
        b'P6mNxHDAGz3gTlfIB9xZoNSgy8nYpMYGOYtt7A2i9ahxWofpIMIAYgmakCDStjPSgnuzpbtz3Ytz7OhWz4/kM9aQrSiJzzWTLGoxm4iS56HUabC52nYszZfc/dDOp3sL'
        b'Xz5m3Uv6ecZGdtnGFHUGHW9d04+a8Kv1z6feR9ekS4K3BG5BNXIaX6suWNYuAPuxwddVTLv4a3QquAM/9HFxERIC5FzSANqejtq6V+5/sjKeNNbRbyzTKDgagMOM8AER'
        b'4GOlP5DnhI0bxtJgVt1MCQ1mvTuwl+yDMIfxeZBDNMOvpk0QfR52ffnPM3oqrq9MTT/Vt2HljQUbI/ZpXhwzYmFt1IGUs+OPj1va++3IIxk/Rj1KXu/7l56+xbfmNmX/'
        b'9RmpZGXQG73/zqKJshFBY64N3TTiN8WrkscMWh/RfXzE3DWTr/Dpgcfzz/fNSP+98ZKk/9xjWsOYhJWven0VP1HpG5q9wCwq6f+X6au8v7Csyo8I/WDGKZ8evjfW/4yN'
        b'j+z1Z/1puMQiWDbtGXRecGt7uLR3ZArR74Uc4KWFYhKUdDl8mhB/NIcJBAPHvMuQY3SOji4WEreIQ0GU7F1yvLMdyUOFpbYpaPdkVJ2sUpOTb4ePdm0Ph7YkSrDy2liI'
        b'KmfAnaJBAJYN9kL18A5qpHXNNmAweqWJSNTTO3OkQgMtayVAFjZfQoKnB+lHCBvADtf8mwzc9+MwW7ty2XirLp+zOHBCkF/soNqbvtxQ2TTF/X8WhIzpuXDweL2oX/KN'
        b'aQk3K3safNa+/dK1mc8PEKU1wpDuN0dO2h7v+NvhQwsiUu+/mf/M0cwPE67sGxF5LBGO37/F//OWz758fefAz3alfnAt/+jpF/736xE/TpEk+a2Jfi3vvewHPovL/zjx'
        b'aOXa37964/uEXg9r7qc8/17f05sHb7u4RcEL7q5d8Dxq7E+2gKr1POlnLKwUDhY/AbdlOM8fdwdEFcx2hUSN0whhjDfglnSlKiFLRqKicCeKgA+6QcIYbzp3dUGNdnhD'
        b'iaoiVaMz1AxdzTe2D9rcMYb+1+7O67mXgdmia+MopzE6rZKtgKfxhWSDbCkbwMgJK8X35tuuasi55iRswUPX+rVgNTLmu27+RRr4shNRuFvedeAQWfo7YpVNGamBNW69'
        b'YSlsYEBPeICHp9Hp1A7MqO2ORR2YkXvHov/oOMPOJ7C8XYxo3jBvQJTqgFFJI4v7RugoI/o+2hlVH5It+mDBK+qvBEY0Fkxsw4jupc+dnDrfNlQ0a0Tv2oLsYT0Xjuu7'
        b'eHWC7ca4E3Onz/j3wu96/hz+6ujwokKlbtb/HSPas2ii8CplRi7ikbCOIqqnXC/QPBcSuOIhIB2sXZI+f6Qwz0ifvDRFpH2JE1ZNbNB5CYmnWcnA9zm6viJn6JL+wjKI'
        b'Gejaeg/21p0RGNxNdNr48Z+CGXr81wt//afqlWZfRBbsnFx2YX+3sksfvKRsiql7fa73zUDWfqVptK/oWr97d07+npny8H+Pvvz++AkjxxxaY1lbuOyw9d9R5bvK98ye'
        b'tlw/cPrbuXO/a8r7YdX4qH1/CZu/IMQwMbfvt2Xvrfzu+sfNPzEjU3rv/exnBSPsX3IQnkTHEuOd56jzodKlrEEBy9volr96qyNKn3pDK30ObEuf68kh8YQmqZJDaVRG'
        b'KdYM3RXd+RUQ3HMTIqnnx04IcVPXWxhRQkQ7A9MESoxPpoQIHfAmpkQtD+vnoKoOyyLJP92IdQ4m0QqRsOu8nTkMCAHWs8Usvef0PL7nrAx5Ph3UMUtlS9hivpjsTS+q'
        b'AFaWnJpgNhX52UWHOb2onikWzQemXmRH+MIVwklE9Ak5o0i0EJgwyZru2skpOGpaAyndZOfMVTiXqF44kUhMT3YIx+2IiyUVjF1Cdq/XS2pxfrt4AijYZlpHy4pw2Ye4'
        b'7IvkHAUMvQhDKaK75ZOy0g5lpbjs66aptKxw9o+6Q8leXZWsYwqkFWIhN04BdnJeQ4SwW7/zXB+NHei9emBOYxfCH7w1mFUbDPkzzWQt6ZxHIps1SzXGTOwljKyIDDZ5'
        b'YCbr2OkpLAqJOYsgoZfBZMs1mMlpDmRVXouY7MeuN7TI5pqM5Iaqr0LZKQKute4B2lot3R+frveaSy5DSU3Mil+4KL9FRo5PsQwTlif7c06rmuwgL3Me7CAcJUIOBfF2'
        b'HiQS4nEnc35L6WEhUuGYRbQXHuuXiJEUXYQH4lWjIsnGCXTjCHkfHjXDTai8Q8CFe1d0wgTswCLVM7MBOQ2KjgBbyjqX29KeNI91vQXZJtnSha3pS98t3ZqXnpNnWh7D'
        b'uU4e5YgVQ4PDRiAHPEcBPRoYryIOl0ph80qii4HBcJOoEJW2O6qXsA13gNoICqyeWcmYZcQa0XN2cvASo+cPA3KcDwZdFALqGTsTCojMIylUoomdL0JDRNhBa+j6ts9Z'
        b'4Y1ERVnGnBwF28KYWpjsrt6OvBR5OfqWo8nbeTuHjqfnt1CLqwgeRhvoTptb0KUlieSgb/yKKfiV41ViMLiPqBDu6vuEVdJMp6uk/4NTBxnPJjwWqbYu8htlzgcfY0V7'
        b'qV2bxSQuERKvip7HGAG0D6dpjc/1WCwkvjWAbGYDpA1KbVTi0unAmPcW4Oh5H/evrCD7CZKdtS6XNpZe3vvbTf1+d2pXfXl9aX1Nc9zpUhuT6TvN+09TT2h+N3VDeLko'
        b'yadHlUh+pHdU71dHyl6rUSQFxgYeYSNelA67Ih20aaEs4krJ2E2Gfpkx3PJwMGFID5v3GKzKhtFeroSXlCphQTU6AxvIomp4VCOEf2xBN9ABZUKute3Be2NzqAI7G14i'
        b'+2pFoXqxhswMb4licIbTLDoHm/oKy3wOwef08HQCMTNRJdZg8de5dWx/L/MvX5ndLTdPP3a0cGJFut643Ghtv42xc+MtKSVtQtLhjPktdyWOp2muwtUcLRjLuXY9LfH4'
        b'wMesuCam9Ty4lW6sXpsCm0fQPZ7JSULkDFtnH40xon3wpHhdIqzqmpkQBVpgIUTw1Qu0x2paRDpLptGINeQXgUs6D2jbUZJsw5ocY1ZhAoGeRolwNjkZzSvwdAaGawc6'
        b'Qreqw+DA0zy2OTax6IYZPts1LIR/k8NaqFAMIkccEYiKnfBRg5vVmN8GVHOf7oLrcTunedlMTihTWpkb0VZoLKu4u98iuIVsh17tCSnZre7Aqshf1GfLXZCZ3+mqv7wy'
        b'Ro0QjuSa59FjNPTiALwFz8CrCxOHDY93m3r+/bjxaAs88N/oL/Pvnqq3MISCpF3crreINWpAtwoKUTmB0aV7+qFz3FC4S9UhOs99yBw5c1vPYHZP9ClgjrASYcCVsljL'
        b'AMWccAaVncWsny2Q2tn8YXaGnAflPAOqZWDM0GHDR4wcNXrM2ClTp02fMfOZuPiExKRkTUrqrLTZc+bOm79g4SJBMBA1VdAhGKwuGFdhKlbwLWJh3qRFlJmtM1taxGRf'
        b'kOGjBM3Aq/3LDx8lDE8GeXl67jIn+PPILj+0C2Rw52K4r1visFGtFrl/KDcObQVdj5LMiS164QQkQl3m37vaxvzpw05xZfgoYSRyPHCFBrU9C+/AU+sSCAytw3CMi4Gb'
        b'F3W9ASY9rJtxH9aN4fn1m14Cz5fziI4S9gtuXKZzLflGO+cme81Cl2FTGr5cngAPpPnCzSyIQNf4XNSAjhodptc4C2Hx2181fKldgCWRjsnE8uZFrfiDb14PAUP+xacN'
        b'e0vBCtOWuyeg/UpVvBodQptRdbQEeA1nYT07is566lagrUosJi4IyzlbF3PCzcldnbZttOSlW425BotVlyvsxUEPB/Lk8qvND9yFykBXTnuaqaBTLr71CQdum4bCI0S2'
        b'bYZ1gVT3wJCr1PGoBvfmYLNoPayLn9khBq+tQ5NzxuB5uDPxWPv8NwJh6eLtDmPdTUM3kYKXjOPhYbg3MUpDtu3jgTic9R4Jr1Gt498zQoB98kJiUy8psk0CNupoqoiD'
        b'TcOHweZhMaA/kCwr1jDw2d4TKWLDOwp0FD+7Mgxe5vFDdADL990MvAKbha0FcUIDbBJ2R5iNdgM1PGaiTammh4GH4Vlkv4MJLwY4V0D6rlQAbd8TJLH/gAh/YKO7nO1F'
        b'57LJ9oRgPCxBzWA87u6dNPu6aCkYKBlA90wYvFTkXDC5QgR2FHUnzgLZF4ZpGIVoLehmin9iPDwTJQb8rNBeDLyAylW0QPyaKSAmj2FAvnbYmIULhVoOWieB58WPyL4B'
        b'afYFI4TE5IViUDe1D+mepMbVzwBj8bDdjIWwgpNv35iRei/h+VhZ8rC3946a98bSgC19XvD/JnpCxcdDX3ow1f/d6m3Xx0g/KH0w5NL6FS+rlZ9MZKOjo5///nLwNcnK'
        b'Gt/IZNXw3S8Ol6qvLfd5u7a55M3QXO0bmf8TnlB3re70B4uqf36U9FbUgsYMJvHF4E2rRuT6+mx+b6Yo+C/55kH3n5m/Nl9V8c29L2ZP/ubj0Blrqu98v25T066Nf7We'
        b'/pMiKLJ++rRBn5etjFk+9t8vMsv2vRV33m/s5AfvTPznIONb8gl3xQm/ayj8q9fbhz+4mv6He/3G3zt6cv24LVafL/NufNX38O2pr+z4SiEWFL4GdBmdd/MvKawFS1kD'
        b'3A23/r/2vgQ8iiprtLZe0+mshARCCEsgO5uAsssSCIGwCgpKk6Q6ENLphOoOS+i4gNrdrAqIsijgyiIqoiwK6l/lqMw4OuM4qO02vzoyKI6OjjqDjr5zzq3qdEjC6Lx5'
        b'/5vvfS/9papu1d2Xc8859yyE8KkPqM9o4YLJ2iHtrtYYoXqQCTNqR7SHtLsD6hbD2J3u9PmEtpNghagdk0iKmQkppzWSFLN6/+XsKPo+7fFRcRcpfhwej7of2uaefjIX'
        b'sbr7YBxjiRPGjVrCjx6nPfUzrMX/G/ik8Q2wYbldAKIuH9J/AAGnYRcDp1USz7ilsEWJDj4THVoKEt+TF4jWTObT6R1zaql8aBSgW0yJ2KvrlSq3i5wmtjBT/xVz/oLy'
        b'EcfF2lbBshrbhYcbLsFORXhYVa0eKphUKGgn80k8HSHjsf6D+ktcb15S7wBic3VjEg7Qw00WxDB69OzB9QBs82CVoZaJf62kpBZziCahv8wwEGXo4jCEJKgpICmFARP8'
        b'S7A9m9K5VIjVGeIEhD08iTTrp+YhURaNdGtE5gcZYolKZUjaA+8D4l4BcmYIl1TehhaOOu/EuUeubFMZpRuADDuTN0Xdke3iNo5sCVXpYNNBImCHqJPITdmVnnqgWJjI'
        b'Unu+dxl2JEZMjQ0NbkXBg8uIRGS0OSL53Sv8gHVgFr6aJnfE5nOjJJUfXcsur5H9i5WPMb4ou9s61oXq/Qmfz0YnryO2LptFQ3RWtOrcEInP+lES0fQikeA2WJo3laFn'
        b'8Dna3mmMhkEbmFNhXXfX7pG0J7TgijY4ZrRbcXwRxyRUmANUOJ04d+ibGsZ7D3Y07FuyiB1NfD1BqYQxFmQJYogBEb17ow/TZhHHknKYB2/JtzZ+h9iwWcrMLYG5/ELu'
        b'iGtHr6jzFBeMJnyxxrto5Pyefa/Lnb8ArgV5+FycP/ra0aMI9T6HlWUsruc5Ig2RcomYfe4KpWpxxLRIqW9siJiQvwQ3T/1yGJsXaJVGRCglYmlACTTFGzFBX0ICq1Ho'
        b'pTD5RDSACaldRuQ9omF5SZQMAw7kjZSBD4lvLIBv12kH1M1kTVJ9FG3vqOFpDM8tqSOznxbu8jwzgOmt2slWOEmrc8+tNByAyAupHCL2jBpR/KgjpPTG6x5+L+crDggy'
        b'IP4BzoXaQ4IyCq/0ZXwASAUX/I/nrktuJgoHchM7w8Dw3NJJFNsTjb2RxfZ2CfDKRvoWuvibjsdK5RHefkHIzqbRgO6jCfsXWgf+ihoPrA3J7XHXwSi4l7k9l1h6EUeD'
        b'4vajrit28mMtfevQ/QgnkrdXdoiVypNV6uRu8wtyJ49dWpRHZKa6nnUxz/VQ7zXlomJNx4rm6F275VgfYBI3T3RL5MMRunaeaau4xLzEMs8K70yymd5Z3JYlNtlihABB'
        b'tAA8QzVz6zy73BP9QUI4TnbcbJsXJ/fSw/GyE8IO3V+kRH4kE+RESBPf6l2SnAzvnNE3kpwip8KbhFaxOslp8C6R1Mu5eUly76AIJAgqkNvmJcs5FMqSu0MoRe4DacxQ'
        b'g2y5B4RTyRFIJ9Ls6xuJmwCj4vb6xwL11mreGZzGWQZ0bWHfk2NiTpaMZ8JugaTkm2n0z/0Ifxf4YUAVoCTRft3h3/ToMMesJRetTXKG7muoqHL/IkqSCU2ZMVUrvjhi'
        b'uzQh1RXpDKTXYaYy/gEpMAqKyCOQ9Vcsak9tLmJr8FTUeF3w+XRMFTrFViEao03ZglF2Msf09eqdxlrUvertFyImF24EtCbaVdzDFfObFoq0KTG2bEzaZniixTpoeHC5'
        b'y4aq4H5esaCbPoFvv6Tft7SyDQkUZTB7osNO8J5nTGU6y5iEZzjMR3BAlIVaQblMRp6DMAJ9/8LqWcb50mRTQMQ7QHweT2ngjYWlSuOMuDKP/rL1gbKWX+D7Rfj8C0Jx'
        b'PxgysjqMK1XhcfD4VRdMq/Kbc3y40zI/63agLxW/b3kN7KK46xrKXWRXH4FMhG/oiIXtAkADG7GbTPa/JRqSYLoSGfpF6iIk800ZraZhbJryVlZIxdieyzImIfWcn50k'
        b'COQZHBaNocAqKknYLpOvEbAGRBi8siHtiA2I2KPTvYNTBiUF0v9R1AlIrHrraYM5/nsqqSRjTS2YYYXHo6TyHaJOafDpXKsqpVxcJcihXVhDtUJV+xBMpZCE6EaIJvYS'
        b'mIIbBKojb9QR3Z4H2LQRYLpHTF5fXUUDVDc9Wl0z88mguxyNWNysHj9JplrJQBtooq6EyzF39HxTcmxbWPYdd3B/1hQh2hQh2hQhtinY3dAYwWB2duZpD41pSA1adfLn'
        b'6ZMDPR8pXfifKB2udIWYX7VuSfJFLWH5txmUKC8K/ZyEoKYhEVqSb8AEJRtREea0vBlag/ggrmS/oE8lUV/ZKM11gR/DkANJScCG4Wkka12cywU4VY3fXedyGbtFGffP'
        b'jV8q3SD136NnT4RvIdbV1LnVkm3JvOORWhA76Yov1T42Vt786LiW6OMKWyGNq6iPq2TElZkWvVSuZPIGutqZDR51xHX4omWsoTd8RoWNAY+a1/xpA95dtwTMeG56vzgF'
        b'O1kmaN030aL+iXtYgxE/mxXT3hZqdbkq6+s9LpddatlBU1sXxyIQtj671WgYVAdyIEjBl3zQc9WI7PKIzu6CfSbq010sL4Gu+YaLoosrATDXeP2RBETMZXeVp4JJq6La'
        b'vr+eHTAbewMmU3pif9Oh9kXsYbPiRjdNTik6rRy88KME/61XDItW0m4jaEplRxsh07SRhQ0SkUQ8E3wwsCapasBlXtQjZD6fIjb3iipPo69mmTsSj/uaCyhMLNX3FVYy'
        b'Gxro9Y3s2ZMoU4BsvQguw67kgW3CaGJfbF0uXr5q20QlBz4kSzHwQPjRLLTeOLBOraABdkWUDHkFLjUcnjog5Q/YwALWMNpIJJj/QLvvxZNzPoO7Vmg2NZsDpoCwjAOq'
        b'HteKKQM9Qwm+mex5EY/3EfoXgBlmBO1LHQEzew9P3BIJJTigpCzIz9JshZLNAQuUZglYsWsDls4cxFwGMS3NtoBNORrgffuAGn08YIPv4gjOKwVsiLP41IDgU2Wq/RJI'
        b'W2PwFtiROC7RC6ZeiG/l2SIOWBtASdZ4ZBjuiMVf75JrqvwkGEH7A+wwfphblREbRsSF5CM8k5E/Jp54PrT32KvqvT6mgRjhZTw0gUwjfJUiYTZClcxs6BGSfJbrcHMt'
        b'gtidJYP5Qx4W7GThl3lLsPPJtMrNJEJkJ/8K0kUbsN4IMieBeDGtxTyhpCSPL8lLu1gmmVpz3GiN8oNRP8IukdJGApphCIiL0O5PXUO7DkFoAkdKNl568/r0o4bEeDb7'
        b'yfy/GEdnWBdV1IWZrKJVEni7hJbT7BLQ36LTkSglSqnmVHOyJdVulZyS00Q65hnaepMPPcdumKptKFg6ubB8YcDEZYyRSjzazbPzGN/kulHqwRhNLY38jk4dNgxS5Jm5'
        b'gbJ5dqO2I4/ZN8svm1OWqj4RzZLn4q4XtIMZ6pNtTo1wjpFgVHIUOtQAFqMDtsW6jY+6ilq3jqso3duBURZ9PIe0AFo6Q/Nb1Z2+gc6YitjVewRtnXqTqd1jJvzzzeZi'
        b'COBE8heJ0u1A7gJhKQHpyjNravNMTBmyWtRJXTPaVIM4Ftkhx8PdKjvlhJvRJhtrS1LEMb6xrm6lXtn2seXoSSajX2Dn5WOITL6FyGTMBriKxHiQZIPsVH7kjF0V9ywi'
        b'FWCbxHVF9CebuGep31yIu3ujeBStPTN7dzGRhJoRo1qApJnPgv+mTrEt+nl2dJjJGuUKvoPt0wZoCqvK+Oiw8k1prQqMRukYU9OPRAkH0Us1nKdQm6e0M58YAoagzOWa'
        b'GFN4+kWtjUbquPhRNJQyDwShA0XVCGkEYK/0DlFHIFWOFYOBFpAJqAzEgYyp8OKomFUmw4JpIKnXCFvK4i950E4QZ3IL7mMlXpyTOHHttednIT+sXh0iQBaXy+P2ulyz'
        b'Yrow9aIiKULHDARsjJ9bxEQMdMtLEu4tHWFc+M3lmhNTYpspSjF+YgtLOmwdAfBrLlEOQ+2wyvaLNxFcS8pwHL2R0U1hFF7GRHcG3WNeh8N6OUQabgyrVbSbraJDTLQB'
        b'2BcbEf5ru7KafXloWl07pm1QD/ljgGCWekLS7tTu1jZ2DAVx4zWg4FZxibhEmmdyM3kzZPJJbmmJBfA2PUTn/QghrfOsjC0HUJFBSRux1+yMnRFJnla5xF3lJ7uCelf9'
        b'C9wjxdwB0CCwVhUdFLGpc9vyfh7viOCF9VKco8Utm85PhkKLDSikjODb4qM4KTwxMyurnUZcCvhENRlxxjUl+zmdAiN8dC60SgKKdOVlTGKYwJAYoFOJNYKZu4Z9N630'
        b'6hLF/B4z0X4LIY6lhf7by7O4RqtYKOZwv4W6A2wm2ZjnEXsp0AkrmFQtgTJcBxHnlYQ3Nvp1edsWivinwLd6KcqsEoCUdwAGiHhg2iW6Tqcn4y5emldGsVVLFNMb3Hql'
        b'tmBpbarVgoxhPtdF12cMGuYQyYni5OFobnmatnby1GIUoluXmjRl6tKYRTpWfcjSS31WvaXjNdolZo0SXkJHiICriDQEUqSr0XoDLI1D86dT6utrGxtanWGa9JmTEl12'
        b'+pYVgtHU9c8A3HeJQiYTw+Il/8oGt7ILH21R3ly7W6rZQ6U2S1FGmJVv6nmJ+hWzBO2oBU6MLsSL1s14+NBkrBuAg8PhVqGuU++O6Wj1YAskXKptLC0s1o6SPO5WdY+2'
        b'qbgIUOg7ltq1HdqNpjbHTlHuCJ6Ow0bOEb8jk1YXz6i/AJ7jQe8phSGk/7iQGQnbEEfPJp3IJTKDTubEq6dOgVmERGkkrr5lqhJN/nNduk2C5t8qReXJmP0vOvjEidJV'
        b'vdumomPcJ7UH1fthZWuH0b3hdu1wmwlmNibYgpgJJrecypirTXQeZJsnkkCQGYA9ngVZYSOQ6PRHlC2yFVFk2SbbAQU2x5wBWedZaEuwUl84Iw597KcCkq+Ul7SxQBLt'
        b'9fs5lAmqgd6U+V0i0NUGf6o34MF8DUr+Ae1MfHjEnAUlFOVJjQoI+hdAsjI4wJ4lpIEDos+LTxSWMiB3pLqhLYzDJQSE8XiAboJ0JiMOUeCKwa1cIlQjwSIhwcIbK8WM'
        b'TOISnKXExRqCF8KUWt6xU8GI3UVMWheykAlEImaQp1uHoYidiAXWoLira1a4UKSQ1A8igtf301hfmOEdkqFbA1AIfv8wm3ByoPFsiYxo4yl5ou5wMHrGQ+PRgtLHLgYL'
        b'FyPygNZpFsGQ3IsdLCADhIcwClxC593K2B940O0bSCwRiZgZ6X4hIOFhONFXnCxtwK6eYzBH9kio3qL4KQVMLTYgsOTMa2CgKYcSeG8BELUe47Av+ntaeKi+skZgb5am'
        b'B5iRAStAk4hpFh6RRMQJXjkilaNfdNOcCk9j2xO0KErATtCQeSMLyww5RSbiICjTcJRmRAEj357AJxmhPIpn8yQ+UdS6h6vqvcvcip+4EL5YaQpmIRSyJHZnC7O0gCg6'
        b'ZHKh2zy3znnxke8/xovB7RPAB8Fo0edeGjHVK7JbQWaer9HjJxS6roXDcqnjfWfr+h2QDD1K8tmADBW7YOcFAVXNzT84RbuQiZpadnRRf4l2tjlki/IJS2g+4WKFGTGk'
        b'WQQEg0RiSPmpEGcYMZ7FvWy8rQFR5pfxihXFLPAtvRP0cxBE4ZGXCCifG8bb6qr2oIiDl/rM4A6iUpYyBy9z/wmyMQ++n24hpphx22SSebp43egFtbuJ0KxCufwYFTC4'
        b'BrAd6QGSjN2DiJa4F4WX4RtjqC/DFYFPIjxN8gM4CghpsPWs5kkKAcDWXp6QOVgrsDJkZOp5E403GAePGGUTe4I30KdpBshiR4qCy0Vz7ELaVd5ab/1yb3Z0W8/umePr'
        b'ecG8KseHJ45mJR87zElTj0ExpYxIGE7H3AymAs2yqW2R50i8y4tCO2jeGjJ4DbuVLAjzzG5wos6nT+PNQiLf1KV198YmbQObolylai72RI/mDW7QuFUL7KmGa5aYWI6u'
        b'yobwB1OQel3AHJAI4Of7JXaEswQ2A2TQ3svPjAJ+Y1M3Ky5enyTK1XihtUiHGECZot14wDgtMawWq8FKVYoxaGPMU2hRzNJsn++5EOL/oQXrhZ4SkbvJ+qwNCNeLFsth'
        b'MdjaJUavjlacmrCwNZ77kxCRFtx3MqS+3TgvsEppnRK7A2XqJJk7UV2j7UFuY4m6lWFh2uGp2no095TVWVKfVh+ubtcCOf6RQ90oPpJARKeBhzAXAQYWgl8uxkAQQdbx'
        b'D5I9QQYdY8wlRqxT6qtqS2o87nIFsd9WOEgrCYDJHGNTMlrKl+oXZJ4WIKMYBfpGp3xpyJuDqQVXE3HozMSts6BSmssaPQO7kILugrPlerdu3B/tn12w5PiKUawNh4tO'
        b'vs01PoxHqytiqaj04Xl7xEqib3KNErGgbHl9oz9ictWRbxvyQhyxuDCGW44VA4hIGEOpaYfwxKnwZcuschCSkEyIgplvSjI6qX0+HwI3OxcjmMXkIJHBhep2TYkhXHQA'
        b'jBBEz+W8laS3eiMPQIrnmiYHYGkBzSEqw1ZjGrNSPhcoSgRh15NQlZ4bXysplX6LLGCvwzurrOdnxF3qZPf+SItKrN9ncfhW54+eSyL4VlXf6JGpyyuqyMFANnbV2R3b'
        b'8W//6Nl5NqBuoFOpoyKmulroZmUxHS5Nm0VEasTkVhSAQx586ZjZ6MXo+hefx+1u0CFgxAJbD2W1uMMFHZGw9O8lQ/uLd8KGmkh8OoF8nOBYoDhrU3x0FDBFx6oghRxj'
        b'nih9ZJqbMDN5o/+VPjAWkjEWes/gTmmixrBpYqrxRZtsUurwmTguFxN2jV6sSLwphjWMFW5KiFaUxfhn+BXDHOUY1vCqjljDaOTHDRAtxdTCJEmMmZ30seOuyY8pD6en'
        b'zosVGC+WWOrQNbpqMUF2SVmBdVlidI5SG63axdo0LhcAXuQwppmiJ6ZWwrFh8JJjKqlHayPCi/9zOR1jpxFMM9hf2D1MiBHPE/kW6SaYabU0TlWeekAIseMMIQ/J5V5R'
        b'1Q6jFAANrOBuscNmv3iVszhI+SNU7GDroJ6hoQrgpRkvN/4UFia2/M8GvWqVnHZnkgPZmBam/zQuHW0TTdM2LqtXHyLn4iYufoloH9zUZoOw6HfSNI1yRFCwWgJSNMoV'
        b'QRHGeZKcGGSeccSgOWitNhOf0gYbRRIjXsm3DZ7g2GDTYAbN8BynNdmaHJFKpo8vaQMAo5gHGoTwczrOANsD4AoCIxKNwYM71C0kLJFQJ5nCJlnwm1lI3ywMZtqFuOkr'
        b'scCB2ctyfBfiIaD7FoegwV5jtqvQnmdDxSJ3xOFz+10NSr3cWAWYvwNTu+ZMmDmrdFp5JA6/kXVYAFZxLpfuftvlYsLYLnTEYuBvUXX3S40llp3bMuHTSCIVgEA8Fts+'
        b'EdkR11VnvV9ImgU1ya6r8JI9TDTDgjAh3DK1mUGVi5FKbFm0Df2iAEJoSqaqtPpc3qpCyASLsk53xYwfLj20NR4QGJtniaAsCAH1ik8otg3UpwgUK2z6a5iQNz03i4DR'
        b'i505lCamt4AG7DEzWQfCQXllWwiwSdm0RtjUBbBQaY8lILDNTIaJJHFrRJ7zJg7gfOv7c4wZew2ni0WRzjqKfH+FNbbn5MyaMP3K7K+wC5gI4ArFXW0nVD4iLK/Up0jE'
        b'DChCQ6OfejFikhvrGnxMuRWJLjodjJiW47m9zuBjwI76mZII1Yt/unqzsgmSDDIZAsukvmxGwRtC65OJNZXLN8XRuLCKRWyT3J5lbn9NVYWCnp6ZviUOTJXBlMI/1CCJ'
        b'2rZBoBwg5AAwfJ7GCjF4El6GcRD1lUb9Ts9ANQFWL+KXEO83Af1oSuVQjBNNUbBwVxa2yuZmm2xptjP+QnMczIE4Evf8shnFMRwZXHN8wKY8b8QLxMMIW2GDvUu2Ncd7'
        b'syhsh/BROQ6+GmVbseylDa3rEnAEAD1N52o55R3MW3Z05jK4hvcgJ2fAeRuvjJDjA85lPD4FnKwceM4KOOCKeVt0qAJ5ys6ABfOUxWYb1MLJakEp4TuKWbMy8TuKfciW'
        b'gCkQH7ADkmBbgte4JQ45aYMZ8rMrDRgLamumhZlcfg4VLM7hGMw+hyN+Npj21ivfzvp6dAnxRC6II0eOpIGLiC6AKPxsRlHy2RF+bMQyrr5RqQGAxJfmCRGT173ctYLd'
        b'VubFMwF5O4myemq8bh8DVHUVyqIary+SgoGKRn89AThXJcCv2ogVX1bXewH1VeobvTI7OrgZZ6tU5fZ4ItLV0+t9EWnKhJLZEekaei6fcPXsvAQ2w+kgXKIMJFJHMfn8'
        b'KwF1jsMKuBa7axYthqxZbewYweWB6rj1Z6B7oQiT4oZaRMyVjMti8zbWuSgFE7mV8Bneulf46fU/dWIdxwQpSUD6SpOue8npzjIdJHiZSJoUVp1WlnRGHqlnoZEQIZMY'
        b'esxRJlt0uNwcP6LSFuzyibToYopplx9DO9kKrvX6osOgTDqvRhJosiyEOdQu8otEYuEua0XezRrd3kYGambwsjnApzGhQUm2IJTzm3QWqrkVRS3qrFQrzTbbhS5jKxRU'
        b'Ts4eVF99RTYKgGWTvQRfY51ih1G+UPBTFLeLirN79yvIaYNsRUW4EESRvpSzGdrCOAa6plS1wdlDMVNDV2pQO+QTotz1kCPj8nWnLsaqD7qiPR2pc6gFc0HKz/Hl07op'
        b'BzL7j5zOvEPVG5nEuCMitDTipFleA2R8Vb2nXtGhOcvcIO7o1Kplt4410cQr70Vr+RwkrTEZPCy0rER6fHhYoMNiPVvCe7fQ2ZcBipWtfId44DpeB/nKcV4vJoaF8DNN'
        b'NLUwE26CfHqbosyERItVSnem5pKO70L1Hm2vL65hqajeqT7FCdoOvodV24nCa1G0gKS6xPLychTnEsn1eWWmeor0+a7Q9nE9tFPaAfxKurJrLQI3/VosaqFn0JIh0HMl'
        b'NQP8t/K+9YDdrTv//dTZf5+bsij17tPy9t7nh0vC2uOv35Jj3Zc+4Pap9/IDfnPPN/5TG3fMq52/pG7nE6N7nz15Z/e/df9i9Gf/GPXM775pOP7yyeXvX2/5W1OvtT0e'
        b'9D0/puz541lJKfN69XlyypSam9I/cQ44dFVlydnwNadKz7/W8/D8uaGR83p880lz5e7ixO8a77x8z7HwmqdKM1+r+uCxBX03/mnkB/u8KS/611z+SO2M839c0bef78ut'
        b'n6e89KT2Svr7XwZ2Pj97uKcpPmHllGOntr3/17+PWBP3zRVnvnip65bTuc9NePmotu390xnzP/ow+ePz393/8Uvb74zfX7L02hc61Xbr+WnyZ5b1J9fWvnDG0WXU9X2P'
        b'zL3wQHbBTHlK6S9n3n7g9Y9yP3mh8Z3FD2W8O+3j7q+NOyMqv5y5bvPx8Pwzb/zuiy6jmvu82K3r6BccW5RMd/9Nplnhh88f7Vu63W0xXbMl6fRp/uzUqqSyzxLLhr1t'
        b'H1b6K1tRba/Je250X9j2tdC8989vnBrU/djg79O/Gll6+6zNEx/vtck9enKF6eA7H3AnX5nU6zcPz/k29Nm0Dc+6Dz2zcemR2of4H+Rrd9z+hjzDLIdS7nyzbPvKb970'
        b'/TngXTYqNPx47YMfbvtgw8K3X3/6peOFxxrnnnGvfnncK8sTPj3fcKrThzfXaFpz6ttZa/senjNmvj1h2MkHTk069tfTq9/+S+7T733Y/Pibz407ttf24qeVG0a9GLlj'
        b'5J/33fzlFQ9tf+zpIZ0Ljs///eXf9fI8lXnqzOjCkkfnv7nszKjaotOph4a/2XhmRr66b/9LhU+fzwm/+OaRpybN++GqJQdW99040lO3++qrTCvWHjgy7ZrvOinfLv2D'
        b'590zy95auvu/f/PW0+u7vTpj0Lzqu7f+sVPGqpurhlYs7vTM8+Wjf7Ho6M7Lvn7/sbULtj5ww+Cn8l498eOrf7nlxMxBVYOGntv/0qAz3ye7TnzqfveFIR/ZPnN92PWN'
        b'X+3Z8Ld1SR8+/HXRM8PPLn+h66hHu20Zs+3H77rcm/hc3IILtxS/Ia5668ZpS8evWPnJ8gcbLxT+17f3m1c0fnLDX5tn+Xb4TpW8e33zgJ2/H/rukXWf/+XWE+9d/fu/'
        b'vbLl9qKm65+b3/TeJ3NGPnBlQfkNL1wY9PLXvd777bcbG8f+7sojn97Q7eU/vXzNvb/9/ZeeukFvvX/+httSPDP2/27guDu+v3n3u+Xnm89vXXrwvsd/OzLj2T/c3Kn8'
        b'r3NG1uU/1vTOgF/PXfbSD9f/YtXA93a+sv2hF1emvP7NyYeVp4LvvLlx9r633v/ippcTnpr36vFrv7/h4Moffq0N/+trj/7A5+Ucfu6zY3lxZIph+US7MA/Nd5aq6/tN'
        b'KtTCHJes3iqqT3jVXaSdvUjbkUMWYcuL8nnO2s2iPSmo29SdArmpGqtunaeG1S0XO9Ymp9rXqvtIhbtSWz23tXxk9RwmH6mu1e6hKFVN2r3atjx2vmqbVJiP/MwE9VnR'
        b'pT2jHfcPgijT1dX9oBKk5qhnhc8bS7Ubry4sVjcyQ1fsCDowzC6pmxf70T7p4OmDYgovnVpWqG3Iizm53qzdbSS7oczOaQ8t9SN0vqLf5a3EC7RN5vbkC47096PVrMml'
        b'Pl8xuRja1Bh7PK6uvr7lhJzKWK7tsKlH1S3qbeQjUdtbOwyr10m9sV1u7j2DyepnrbamjuC09oR6nMFp7T71JOBgP2tXuOQlb+i/MbP/Vy55Pdi+/Z9+MbhSnvoKWfcm'
        b'iSgOV2Em9f2f8ftY6ua0OVH2WWT/yTbAhy0Cn5oMzykCnztd4Luk4UF4z4LewzPTnab0MZIg8On8EI/A92mEWFaJDsp7J+I1m66Z3fGabKIr5JZuw6dEEa+ppoufHVbj'
        b'Df73zMRQmoO+O+kKefapdyDW/qMEMbC+6T0EPgtiplsAT6e8sqiMPvPx2uUyvOaXK/8VPUm7+f9P+g4uLSg59tZCTleh4e5d0bFBCObFT+qjrmNGB6cNt0+BrWGThXNm'
        b'iN0KfDXnfniV9/WFqXmP8FTR5tPet/sn3lpauu3ki9/9+c3wZ+c3Hsk71/SnQR9FZl3Ze1/hgtee6HtFcNhzr574OumDoX/au+k1yyeheOmL7y6/LyPe1pw0ueT76YvH'
        b'5ryxuXy788jL/u2mB1/MHDjo5T6/W7Rg+xcHF56ZsmK3MvTQptd+meydPnbF2QNj3LuPbJ17hX3Kni9335z/uum730i1J5L7THr+tX988/bMk69V3Wpbfpn2+cAN+yt3'
        b'zJqQUngqOPrA+P/aMj0np/LOtOqklQde73TgpD/rh1HVr5+Z98PWIZ8+ev/pvgM/6PfbZ54sfDtt0MQXl+0++48br9ljfnTCji/n3Vu7s8BXvGjD8JmvzrulbtOquR8c'
        b'eOT2rWrJp5ndrql9rNvVtY/D/fBnV9d+Fe521eB1d278csjAT35IfL1815NXnwgfXHLdlY/c/fTE4Lbmpxae+fCmrJnX1c+asWlxn99tGfrB4axZV30+fcLnrz3w/Q1d'
        b'U4Yd2zXzV0pJ1a9GDjv8zkOP/JH/evuv/za9+4wXzhx9c9PpVZ/5Hv9yxYJ+O7766JknZx0tPBv5y9jdt//m7EdvLh/+l1ueub+ueYKv28zg51VZ1x3882v/+OOIwJzV'
        b'Hx99/9f5W+QF73luTn352AvvTtpx1+lfDf/9qsCz/11+vvvs3R/u73fvJr+Zt1mKf5yYNTDv8BdJ2esyv8zdExp4dPqVnQa//tsxKUVP/PbKziP/OuC5xLfTK9Z3O1+5'
        b'Oq/6TW2UsyHUK/NDyber8qZBuz4U7jw+NvTp010HT9fOnv/ltO8HT/v7RwVLC5Rvf+T+++ybb/5hT94o5usurO2J1yfVem1d6mWF+qyaKQ4YOp2wkMsWajsxBmID6rpF'
        b'iA1gjCT1pAgb7eYezED3TUWw0xteLbWQtpkjt5baHoEc3SWVaA8WqI8UmmF7vYlfqe1cqD2lBckh1oyyiQVlRfloOEnbRE7r1pdp6yxcj1km7ZR6LFk9NJ82c/WZherG'
        b'i218MwvfUxu1R/uqh1mLjqpPqjeWQTxtfZ56kxMjF5i5hKFirbplHJlgVDeZtUe0df0maRtE9R71Tk6axKtHzJmEDIxSD6mPlWkbcwVO8PLQwlOjtP3aZvqm7tMO+Qom'
        b'Q0WfdZdNM3HmMYJTPbaKmQ6/X92h7iRkzjkkt4jnzCuEAZ2zyMqP4Cspwy950IHafkA/rOqzghpUT5jJSbJ6s/bMCkATgUIXAvwi8+h87UbqNfWZvhb1oLYWP6hHeG1j'
        b'/mztoTnMBtg29cQgtDf1aHGLySl1g7aOEmZzaJF+knoIEjbz6l3q/pKrtFtYG05cq27X1k0r5iHPtfxw9cmJ6h3a4zQUqb6roLgQoHD5k7RtZSOSIGtAzxAhy7nMNF47'
        b'CngVTokC9d6KOEBZy4rsudpa9VF0R9pFPaXuvlZSd8xQb/cjaybHr24je17QI2jGq0x7XC43cZ0XSwPVNepWVpn96gH1JhiKyVibu/gGvgT6cLMfjUtBJwwv0EL90G/0'
        b'Pj4vf662T1tPX3LV8GxtHeCBIifcwC/X7huj7nUye0kPu9VwGQFIGKU8s7pF4eLUmwTtAfXx7jRRByraY+q6adOKSrVDNTiUU01c8nBRPTgmjblKDWtr+5Yx77DTtB35'
        b'5ZgN57xeHD9EYWNyu3qHukNbp25Y0M/M8bPQhtLO66k1NwzSDuoW14Q6jpy+qnvVx5lhznXaIW0vJNtPti7UBxo4qZJXnxkznJpU7NGOlxXlqY9oT0yGGplnCWk3CFTh'
        b'4T0b2GQuLS0StEPqfdCguwRtX666icaiuxouhOFEXDpRPVqsW25MVteI2o3aenUHtcqn7dZuLSstLC3SHh+l24RzamvFcu2JIpqCsnZY3YURTCnj0a61urswl7IPaKfi'
        b'WZumAsL8LHR6Xilkr20R1ae0R9UnqNsXwtOhglL1UG6eukc90G8yTNgE7T5RvVFd25v12mOz1FBZwaRSEXJ5gJO68OreETNpNfZPgfm/Dtf/JjFPW8dJM3j1ae2ulX4y'
        b'bvTQivwCW9lkE8eXcdpdo1ZRc9TgEvUxmN84udBWJaylQVxcQNB2JaYxy+CH1Qd7wopD95fQp49xUiKv7rg2wJbOSajXyTKglAarG8yDeM6ibRbMl6tHKe+yodpuZn1S'
        b'26JtirFA2aAdYYU/FK/uJNuPudrBWPOP2rEa6o3eK2eWkQ3jQrP6kG4QzqnuEcdpJ7UDDEY9kaIeamVqs7lGNwuqbptB0E7W1vkMe5zQP/tb2+TUjqsn/KivPktdlz1T'
        b'ewKBSxGslXwYKViwmwGYTKG+WV9WpB6QuKnqQYt200TtARrTIu0RdU8c0qMNmLCsFCLuBaiUqu0StQevHuIn/yv3L0iOQ1fDIe1E0eTyRjrjRDf306bAROQGzzeX9kxi'
        b'sP/hvhoDfMWTphbz2rFV0JZ7Be3YUit12MhU7VkABOVEFZrV4zkwg48IaO9Z3UhrozpuToG2cQr0drV6sjCvCEY7JUvUtnBeRgbXaPeXwYItWLgMOiRcWji5HxRk5go5'
        b'k7Y9CchgPIrWdqkntRv1nWzDtDyg+tQNAL234V6VliOJ2vY8tp1BzDVo5XjaNNpqLNpd2hGo0eOwptQH1Q00QKPUOyphgkClluG8BOA9xcJlaEc6dZGuKW+kfNR9AAce'
        b'g3pph7Vwf/XRadPQMU2SBrviXvU2dQtBhInqkZHUxbChZWv3clIRrx7KqqAO1vbAat6DNe4Xs/1hdbv2Lh4mQSWPaavZ1rJNu007gEbiTqrr86daOLMkWBdOoZp2gTW+'
        b'n2zfYpOLzOp29W7o/gdwKh2Z8JNkowzLwEP/Ayit/7hL9PyYqL4DcOHiBMHKX/yzC4kmic470oFqAiye/QsSj7GdLI5+CsJoQTuTIBTs+hPkAJi/lfJOJS3hlp+DcqY4'
        b'pD0iCSw/eC+YxRU3cG1/2Waecb6ZoAOKfvjc/sYGl6vFxJ1xdKDysS3FB0aRfNuxyU6K2UrUIR63MY4JGvieh2slJ/NL4BeeE5qDcmjhvnAX4C7AXYR7GtwluF8VmlPD'
        b'wd0emoO6dOHuGH8JxuSDfHCOITnXzKHUnEesk8IJdaZmvs7cLNRZmvGg0CLbPNY6W7NEz3aPvS6u2UTPcR5HXXyzmZ4dHmddQrMFjyH9iZB7J7gnwT0F7slwz4J7Ctzh'
        b'Ox6ohnsEuFAC3BMCZEknHBdAg+V8OBHipcI9Ge6d4O6Eexrcc1CwG+6WgBTuKVvCnWUxnC7HhzNkZ7irnBDOlBPD3eSkZquc3GyTU8JdAqLMhTJQeDzcS04N58mdwsVy'
        b'Wnia3Dk8VU4PT5czwhPlLuFSuWs4X84MF8rdwgVyVjhX7h4ukbPDA+Ue4WFyz/AouVd4tNw7fLmcE75M7hMeLPcNj5Rzw2PkvPAQOT88Qi4ID5ULw8PlovAVcnF4kNwv'
        b'PEDuHy6TB4T7yQPDk+VB4VnyZeFJ8uDwBHlI+Ep5aLhIvjw8Q74iPFMeFi4P2ddw4d7y8PBYf2d4SpJHhKfII8Pj5FHh2fLocH+ZD48PWOBLdkgIWAO2auyl1KAz2DnY'
        b'PTi1WpLHyFfC+NkD9rCDhFtaDLQ6gwnB1GAaxEwPZgS7BLsGsyBNj2DfYHGwX7B/8MrghGBJcFJwcrAsOCs4O3gVzIce8thoftaQM2QN5a0RwrYgc8LO8nVQzonBpGBy'
        b'sJOeezfIu2cwJ9gnmBfMDxYGBwYHBS8LDg4OCQ4NXh4Egjg4PDgiODI4Kjg6OCY4NjgeSi4NTglOgzKL5XHRMk1QponKNEN5rCTMv0+wAFJMDJZWx8njo7HjgyIZxI+H'
        b'eMnBFL022cHeUJO+UJNxUEJ5cHp1ijzBSNMcF3IG4qiEPpQ2DkqJp/5Mhx7KhNS9KH0upC8IFgUHQH1LKJ8ZwZnVGXJJtHQR6ipSTtL1dhzHZkcoJ+QI5YccAUeodI2A'
        b'Yhz0ppDeFLI31zsCcXTEOZFZ2qdDQybfjzCjY+k13BqZylGIa+SVLn60p8Et4Q1JcF1Z60KnHF9uXnYNEyutyK5srPH4a7x5gtKIsIhO8JAi6dAalKvaS+w4FFILm3TF'
        b'WI6OkpXnDZWWPAnA3iK3v1pBRQqre0UVCdaQ8jYekNdXRxyGcBEJFfFo16MO4CQ82dHsdF2D4vb5ICR66hehdi/Knym/5pjRJO4cSYBgvc7hYeI5lMs5xxki1fWyG6At'
        b'mVdAcfSI2FDfELFD7rK7ugIVHazVLnbyypQJW8wvRCF0xFxN+UTiqupdFcoicnmJfjtdtcvrvZ6V0Vd2eOVlmUUc8OzzV+gGLK0QqvZULPJFLPBEmdnowevz++grCdFT'
        b'CcsqlJYAyuhiiNLRg5PeKj4Sf/DWUz4eGMCKSpZAcbuXoXVxDKB0AwVMVR53hRIxeypggAdExMqaRSR6jqZemEOKiB19KLNnJvDzgj7IfqWiyo2+EV0uiF7pYgNpgScU'
        b'V4hILsVdHXG65BpfRaXH7aqqqFrMxIphYsjMFhmiWheE3Lw27ulwgiB2xew+CczrDYpUodUktHGK4gDj8chdIC1SYQ2Q0ku7BAyB+vYlCP+pFSScnB9GZdF03MDBJm2r'
        b'OqLQmdmo40n4GrIApHPAwsrAmgR4gEFCNapdZMnkaYaUMcRQNgmCSQEpZG/klNUhR7MpIITiagVlEjybvbkU4pQFIUcc12wKcUxwLGQPJcMXJ7Td0Rn7whyyQLjbGiFg'
        b'DnWCEgXv/QFB2QzvskJp1WgfZhsKe0E5KVDOIxQ7HVJnYm7eFfC+eyiJ4n0cSgK4YyF9tfRmK8S0hFIhpgR7BfT1GlSKeT4gwQ7CU37mRu42lAI2Qyob5dsVYhn2ZOyQ'
        b'g54yYIMnOz6RVx4Iz+JY+0M85XE9pE0IxccZGnNiKJG+xqej3VugGGUuEIffAgLA2/jOHFPlImOdNmaNPypYR/0Jed4D42APdYHSBeyXgCkVFVnSWT/A96NU485GTwSE'
        b'VvPF8b95XvJ/n339szjcOKs/w9leTuDZyXBXwVDOMgtWkgJKhl+iyBwFMbkg5ibIDNhuOi+JTsEJmG8mphPt5FTIKbRaLEn6/kOL5XVBXyxOGOo8fbGkxi4W+Cri4IUk'
        b'2KP6t1o+OHgFkEaiJ5z4poDk+xM5kjeH8JcGgy6iPF7AoqwOWEgrxxqA0tjkgeXSZQTnlUNdQ71CfWARZFSb0MgRTN/pzfYQyrLZIde4gD3UFRblGZh4CXFcBm7MIjw7'
        b'8TngoGUH+QTiAEVM0CcwSfixbwH7CG7pVq831DsUH+oq86Fe8N8H/ruHcqv5UBKWE+qOiysVUEx43yXEhxJDiYia1VhocZtwEsNiSgpYoTXxMOHhHoClEXKmc83OUDIg'
        b'BPjG2ZmDZRNPiEIcpCokh1krKAd4JhVTM8pFNZu85+GtOZQP+SYEEkLpFAeAAtQ4IZRNoWw91JtCvfVQDoVy9FAWhbL0UBejrhTqSqGueqgXhXrpoT4U6qOHMimUqYd6'
        b'UqinHupGoW56qAeFeuih7tG+w1AGhTIwVJ0AG0QRovgBbiOCTgQE0NZQ31A8tDgxkHib4DsQkOhqwSvNl844XyAP6P9qNJ2tt6YzhzqD0KcpOM8gV5HMHUjY+wjA6X1B'
        b'QML3AclQcm8xi530f2Tt5hX/B8CP/3kY1Qd2Wt/aFhiFEomCVbcJbRadBK2SJVJQxt93khW/otnRVFSyNBv+jtGatONvkgNVmNGelUNIE+0AvZx8h78vpGSHmMgni1Y8'
        b'h/1BMjlEpPdbwTdDzYvgGzPvCBAMiOeQVYdv5hAXA9/EkIk2dUBbQjZA+wGuMenvVptRu7jKv8FmP3XpVrOh7M+6VMQOadMoq9Eo9JockmCRIAYiAFhOZg1ZQ4KdgA2Y'
        b'oJGJaM+S3ksBiglNjA+ZcYeGrkgAQBWPYBtDKNYesm/qz2OucaFkXITYWQTERBMA2ZBtKCCCI9oKtK+NFWgHIAjgFAC+qD8nQi4knI0+eyg/Trf+c6lOTfmfnc/3mQ0e'
        b'Ds1kVHmSLHY+U0RVn2IRZ5i99Qyzxw7GMkQ3ATUMJSAqHB0MSR+MXBqMToCgib5C+oLhNAyTUfnxMOscqAVM3+ybelPXoY68JZ20DTDUTscva9XxgPKFLBmoASvBftMQ'
        b'EH33GIg4jyVKgFbi7mxSPkHnjQhnYV8zwf4Dg91sabIjS4KU+ZIlzs+tfMfIG11PUop0TL90HxHozmAiEOepwc7VFt1fjDWmDCtC/duw5fH4zkjN9kTANGzVQi2rpQmv'
        b'0dxtyA6hlJWQEt7BF1s0ZbQOgLwOafE7057aTtRCbdTfIVIq0FzocnKhgJYk0MUNWm6sL0SsdZlBbJcYPEDBX6m8gfTlH/ifbcAj4qzxueorq13LFRTMVj43R/VpJN2y'
        b'Ic28PJ5I+H/Je0bGf9KWoGEDx8csoUS4OmhzQJH1PgD6zWgzR8Atwi7aydcIIK82h5huwbfJFqfO5k3m89IZV6IJcyeHE6JvpU/5Bb57AS8v4uUlJjeNZmt8ymlSEmjy'
        b'1FQqv6THugr/YuVXpIoND+4K9GagvEyKLzWy0psyBYo9IlZUAq2/uMKHCtsRi26JKWLxGQ+LPPWVFR5fXvy/p8vy5v4H8On//+VfOdjAOdmE5FkE57kgSBcfajhN6XT4'
        b'gAcNbQ89rLqVjbY/R7tv//WfWf+Phs0OMdkiiVMG49qrXoLXbIck9s/EpxHjcF0KVjMRloJA7SxHpZonOPJj4Irl+rlc+oqsq2iAZelXlBDP1HjJMAE7RXme1t2EFVXu'
        b'BrRUrOAZLZ6pVFU0+twuVyTV5fI1NhC3EFlrqLQCb+NcLQHlfGsrEzH6riPq6uVGjxuN7DE/sRIAlkQBUKb2TnZW6m97ortdZ1T+8H8B2z0t+A=='
    ))))
