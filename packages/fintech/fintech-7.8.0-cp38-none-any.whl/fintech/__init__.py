
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
        b'eJzcvXdcW0faKDynqACiGGOMG5Y7QhLg3h3cqQLjGjckkAAZWYCKbYiwMdgITDHu3QZ3XMHduM+kOHWz6WGTTd1svMnuTXbz7ma9SfabmSMJURzbee/954Mfh3PmTJ+n'
        b'z/PM+QJ0+PHFf7H4z1qCL3qwGOiZxYyerWcNnIE3MGVsA7NYlA0Wi/Wcnt8AdBK9SC/G/6VFATaJTVoGyhgGLATmKTww+OT6WtYwYLEvA4rkeonBN91PL8VXGb33p9cA'
        b'g28psxCMBnrJYt8lvovAs8DMLsJPc4FPlsLnYV/feTkGeWqhLSfPLJ9lNNsMmTnyfF1mri7b4KvgHkhwNx9IyYX0vpWJymS8RsPhP4nrvzUGX5wgi9Hj8WyQFjMVoAwU'
        b's0W+DqYM9/gwOxc42DLAgLXMWtIDgHuQo+A0md7TQyobi/+6kwp5OkVzgUKuaQX/IK/nmUhXNDN5IAWpGr9YrWrcWj/wZ6Hsd880gi57RysbRXrHOoGTy+I8PWQe28Ps'
        b'jj10V9y+h7zGPhzfo+3wjmauGu1EdfNQhWoBqkBV0XPi5sVFohpUrUCVqJpLgRfAjPlidB6Ww3PG8bEq3qrERa+8Oukb7V+0pqxvtfe/Um2NnNJLF6f7VvtaRkhmTpaJ'
        b'vVDaa9wSULpMYp16VMHahuASsGkFKvXDNStJvcl2dSTaFM3CJtQE+sOLPG5gB1pv64tzDoDHxsIquBltTsQZYQ3cLAEBwdzEvHCmr8UHZ1BwrWyEwkKAU7iQxIdBk7Is'
        b'eUUGszxLgIsprQE6q9VgsaVn2I0mm9HMkjkQkxnpJWMCGIvMXbSRa+Wz7ObMVkl6usVuTk9v9UtPzzQZdGZ7fnq6gvNqiVwaGUsAufcjF1JJb1IxSQJfB7FihmV86dU+'
        b'lMxxDSpF1xNVURp1JKxMaZtZETrKAdVIEWqEu6eYSDdeWHGfeU0ExsXmf8j8ZxEbEgko/Pwxzs7apCAfpO/LWG5ttLjg59Nn6Nt+/ArmHfbTuaxc+9yy4c8JRX7hWcAD'
        b'+RoZ0CadDR0mJBZkSIAMrBkZKNeapi1ZDuxqnJgNW4AfPKnCPapAm+fGpKGKZRyBgogodQSqiI6MT2bA0iXSJNSM6hWMXU5W8nzyUj88nES1L2qCOyLQJngenuRBb3iL'
        b'h3sdC+19cKaBSSa8hsfnwM3ReMxkOSXAL4VFW8fq7ANJJSeQEzZ3XGbcjTt4qcNRCTym4OwhOKMa3uqTqFYkJIuAdJZ4LhuqRFvs4WRmr85FuxPRRlRLJzU+Xs3ioexm'
        b'0Ul4He2lWVbD/VZUlYI2JSRHocokeHqJhgfBsIxDJWHoNm6gH85UBEtQXWK8Kl5NAVOEIRVWB6BNnEaJjthDSV93oC3oHMkCy4eIAM8z8FD/OFoY7UK7dQJEJ8ejGkX8'
        b'kCDcAtrGwZZpGjxfZCrUM5MTR4zEbxNRbUo8vIyaRSBwADcR1fXFOUgtcCu6jLaSTPHJJM+oUBEIQOe44XAbalawdNbj0bGBfnF4ofJRFapOjFfDi+g0C0LQfg4dF8F6'
        b'+2DS1MRufqg2Wp2gsZNc8bjaypQkMjPd0M3RS8Txg9EePOy+tM11GPnwEq1VaVBtvCpKjGfvIosuwoPFNEO8HFUpUW0SXh+VQp0QgzaLQPdwDm1LRKeEJdwJT8xITFHH'
        b'K/H8V8arEqKj4pLnwloxUAER2gP3p9N6psJjsbid83A3qlbiHFEM8EOHWXQ1FR6wR5J6LqPbgYmkv0oy/NSIREwbalE1hsdUdcRCMZjOizFAVMFSOka4Hh2H5Th7ZcqY'
        b'gKQ5EXFJqFaTlDI/VY0bniCaifbDO+1oIOtNpfdTsu9kMHHlnLxT5BQ7JU6p08fp6/Rzypz+zgBnoDPI2c0Z7OzuDHH2cIY6ezrDnL2cvZ19nH2d/Zzhzv5OuXOAc6Bz'
        b'kHOwc4hzqHOYM8KpcEY6lU6VU+2MckY7Y5zDnSOcI52jnKOdY7LGugg4qOAxAWcwAQceAs5QAo5J+KNYTKCLvrQn4KUaO6Gp8xTwQBekhdAV1BJLSMs2WCNA2BXxAoJs'
        b'0fBClkatUMMKgm7BWg6ekwyhQJ6NTsFD6EwMqsKQygF2HROLLjP2MPxqaW94WQkbVXEY9uEGtAFtZFDZXHjO3gu/7DYKrlcq1KgiHtd5VgTE8BSrhIdREy2K9s6ClWSt'
        b'VHjZ+fhc2MzAW3CDlKJ2Qv7IRIyW5I1PAmDgsZVwq70HfhHeF69/VXQc6QgfNzWJgRenaukbVAfPjOsFTyijFCxg4RVmcRSspS3BsjBYlwhPETzejUrFQGxiI9ChvsLL'
        b'i+rliWgTwsQGNzYI3rYw8Ox8eFlA762wYZj0WQqADK60lkmCx+xC97fBvag8kQKbCm7qyQDxGLZn1gDal3WoAjYqEzAypkxOwAOPZQOKhgrFdqG6BFpfhDpLjQutYYej'
        b'k+iOPZiw45nwBKPEtCACj8DMTBkdQWuTwNOJDLyNh51AOrGbmbUaraf0A52cP5yihwIPrRm2sEAK77DQmQvr7D0pZ4Xn0E4F3IiqklUY3B3MM4RdCwO/DOvRRngpBJ5G'
        b'm8hLeJGZB+8Y6dKhG+jMtESC/hjZzsAmHoh7s75wCyNUewZtWoDJwQ5UFQfP4qLFzKwwvED03REA70hgFSauUaS3m5jZmERep4QK7Uokw1Ch68WkYmVUPJ4hjQj0zOFH'
        b'wO1om52AM3IOC01UEs6RgLnDJXiLAz5iFu4YuTST9YJ+AvDtZSIsETkZj0zEVmAJqJjDKMV6UIqjKMWu5VwoteHJZCJOYxwx+q+sdQpOuDny52+0r2R8ra3I/hr/59+q'
        b'jt3rEzeSMWbJ/Z9/VuW3aP2knRurq2X9Yv+dVcdWT7gSUK4Vv2EDb38dsNbfoJDYBuBKfP2mE4yD+zGL2oxqUhSoJl7gcqFDeG46bLH1x7mehUfh2Y5sMAFdoFywaoWN'
        b'ULzh0RjSCPKqklE1yECVbTn7wy082gKvptAm0WHkXEpypmB4RfUYWGpJJl9Uh9cdk+uLVL6CLag01pUrKQpWkiwzVgZw3IDVPWxkdVlUZVKq4zC/Q7f6Y7aLLrFwQzeG'
        b'inHoKNqHDtLetPEGoS9DpigiRSkYQ3e4pLQOchNNpVJTK79SZ82l8hgVm9ZKGeE3gPFlLN3deRV8K6e32lo5qyXTQgihJYiksm1V4ntCSCw93DXTwus8FZe1k8coQlxQ'
        b'YMDGiIIwn+JVqG4apgRw94BHi+IjBLBjs9inEMS7BDq+K6B7d62VtRJ2+ma47hvt0t1j7r55r+6FD+7VvXipbku3+wFZn5oYEDtfFPb31ViSptSlSpudqIrA1DGRAdJI'
        b'dBWeZgsz0S0bxb6WefBgJ+lZjU4TeGqGTcLEsl2vit1mNLVJyeuANIixhII2KZnLy1jR9UJgmTjMswakSAWphuQCJeBhgPcqkLfoCto1VkkFLkyPLaycgXf6WdutAeP6'
        b'm+vuj0OYV0Yj9LiXp+9tAwgw56XnZWTZrZk6mzHPXE2KUnLC2iNIq7UBGEMw0SKzk5KgVGs0RPDFggYHlBhBjsMaEdpblP0E/cj+1X74uDthqPPqAkF3uD0T7sRUMwFu'
        b'hHdoB+JFWF4s4+AtjK8HHw2FYwgUMgQOsUrIPwUkdpIoGNAV+RO1z+QmvP09bVPC6+Q9bf8m0kva9u0KC+YcWctbE3FCkOmn058/0H6r/Vr7l0xZtjRLq4t4eE93/6vI'
        b'Cxn6kwat/mTw19pzupysM4aTuhz2lX0jjoIXvgkbGDaw1993Dyy5Senw+z/7b54XqGBsRAlg8jOs8GycBuszrrXuhuq450Zh6bceVioYgZDwHYlVB9wQpWfqTAJyyATk'
        b'CGUZGROEiVZRb2uOMcuWbrBY8ixRk0x5OKd1ShQt4KZjvM6SbW0V564m/71QqJNuyVqIuGYJ9yATodg7vZDp22BvZCJLkwG3jcKCOqpIUmIxkOrVaCvWDioxE9BgqQFe'
        b'wWJMlSQN7ZCOB3DTMz7o6iR4xJg08B3WqsDlb+yYm5udk23K1mRqdEm6FZ+dNHyt1X15Svc11u99Kf0xvC5+9eujwmCecML8vCbFm6b0CBJb5J6s/l1NgqWbZ/Qk53av'
        b'0f+t3ejJW4V2IR28De1vGz8L+sAWHp4sROsfjVKdLEC/kayznQCa18wzmlqSRVbCvY3b1Ik6IkrE6fit1Qr5mF2zu+/W/00rpTOb/T/i/U3nFLzAv8tRoxoT7w14/Tan'
        b'aFRqjUC/u8FLHGbl256xEZ198XQsqhMGjFX0iAQ1FoBT8ARsVsaPgVfh2QiBoS9Kl2bBm7DCRowQsBqeReWkTLjGldeTsTfawcNS1AK3CWaaFrQnjNauSEjSJCdg5UoQ'
        b'IgYPQhfgDVE/1IJqvAHBa8n97ebMHJ3RbNCnG9ZkeuNKfzEj/FoGuIsoMDvBudpwodEFWIxloGf5Se6DXsv/pcx7+Wl/r2Hx6oaSKtez4ak4jOHVickYDjDKi8GQIlEK'
        b'rOfaLZkbBoik4yZtVBl8KrLaCRJ40BWDl2pMZApuWqXSpaNflTGxr6zdZ/1w6fLsMct0AyVAEEnWFxUo1avy4zGaXgZYdT7MYJX4Dk+NQtbsfwRuD2QivgPh4b8sWmyb'
        b'KBhzpqgBO26FSArydel/m7VMSCyyBYNxfvH4TtvXNN0IjNu/OSKymvFz0yXfRJ1ed9Jw0vCtNl9XoT5p+Iv2lO4vWnNWZFqjbvHdOniprlvki9IQv1M69tTWRsM53Rld'
        b'qOQv7FuygdoJGz9k4nr27vH3d2J6fA9e2JO2qG9YU+NyG/NKU+vId0b0EDPvjhCPzD+Otcbl/V4+zWHCS2R8LPveQTcSXXYPLEfCTVJYx+atmNk18XgsSeFzdNYcClZy'
        b'AayGEZnRl/4K8qOM5TFRpneMZXAbqAlEtY3sdt0+I2SjkEcKH/eCvI/aER4ib8IzKVhZjsOCJF74HmlWrL+Omf0Yiy7TwaLLPj37JuP36QRnMo2dJPj2g0fRNtxub3Qq'
        b'GkRjmeYqhYzZC/D0TzrHgVhtki18rgAumxKxdp26W4TBJQmlzQEWQqG7urQy6cbkP3zPWzfhh4HZ69SvKYNhTMjGz6x/z9nn63iWSby3EPhaTxxeEXZg6vaIofNHd1MN'
        b'/FDx8pvXP+/+r9f+O35mj/GZd8v7LM/mUs4PvfzDNxtP/qtE+3w/5uIfw3ZXp85bcFgyQ1V06711xg/eqei2b37zeFPgjRVfvr3z4ztvbXrVsS7xcmJUzLbvimO1X557'
        b'tmjQRz9wW3MHnUsVKfyodgTr0Hp0WRB526tZsBRuwKrWVFhGRWOjWG1F29FplUKBNiVFquNdNmgQuUQE7yTOt1G7JWrJQBc18KzN9dI/Q45KuFFwcw8qTfBw/4pO4jU8'
        b'HUbE63I5hXusnaObyihUgSpVWPeHN7ECXsuq4fpMQYOqggezPOocqoS7F3XU50ZH0b7kwc3BygRiWkl6DlVgFdoPNrPoADwHz9sIpEbCyslYvVZFKqLQZizJAhCGdsNb'
        b'cn55JGoStIHjqEkiqHqkpUroHOVRCK/0g9dt1AxwAlbA6sRUeMijVBCNIng4fYulh0p/pUYdr1KMhocVLJBJOSm8AI+208N+RdcT59szTEaBHYwS8HYCizW9YIylYiaE'
        b'4fGVBex/eRZff+E5fP2Z5/H1J7FIjDFbRnB5qKfOnl0218uDuCTndS/EfbmdCkjWZ/4cVKaMSEabiEl4i02MFdwmFpb4wbO0hUyxF7YRg43UjW0DOSL9O5heoFhcIXGI'
        b'K0AZWyxxSKyaogAHVw8c4gamWLoQmEN4YGNyfS3jGEB+nwXm0EVYOnZISUmHmNQxCegZUtbyo0OUv8gIikUOUT3bAGaAZXVL2WKfYl/SgsOnjLVk0LZ4fHfcIa7nGmgd'
        b'9TzNG1LsV8HhfH4ONotz+NYyDCioNcfSEjLcO1mFj0NcxuD++lZIyV0ZQ0tJaSmpV6nnHTLLVxUyIbe7jzj9h4KMOtY8mNboV8bWMRZ5BVMBcsXkDvdDpGcbGCF3HWP+'
        b'ieZjbOIsluZNqPBz5U2oYEndnpxv0Zximiu/QuTKhe/a5Tqj5+olel4v2oA1yhmgjMEz7K8X10sc/vVSvUQvbWBJisMflz2q93H4h4Jif6fE6YcFO07vi8tJHRwpVxyA'
        b'xx9QxuiluaTFtxwBej+8GgHmgZ50Hqd/p5eRFh0BDUwoecvr/YsDHGwda5mA+8vQ/rKWMH2AA5foicl1FovzBZrlDsbB5nL4XYw+kNy70qX6IIdwN9Cr/Dx9N6G8Jw9p'
        b'LdARqA8eS/774zyljgB6DdR3dwQ4/El95J05wBFI3uRXO/zJs01Y3yA8iiA8ihA8CtbyN0cQGZ2+B55T1nJbeMJlPsB3Uk/6e8ITScej7KYPxc9A33Mj2ws4utH+B+HW'
        b'wyr8SQsrfB1B7j44uDrOEmJjHIFlTCljltr8hDsXw+qlmfdQYsIauFk9/CGrkrfjiayLL1J1mthusjFKLfMtZhzMCrCFLeBJFS75slWanm7WrTSkpyvYVjYqppWxddS0'
        b'fSeZjFZbZt7K/Ck/uhmiGDdS1Dczx5CZi7WtNoWsLetDTp5necioHpCePfTNy5LbCvMN8iHWTl0VuXFf7u5qKNkqdhDWzVr5CtztMsbV7Q1tncO0MZIyzlW/QhktKnz5'
        b'CbhUI9JrX2AhA3gYqJOv0pnsBjnuWcQQq4Jy4YdhVkOB3WDONMiNNsNK+RAjeT1siHXYw240gdx6knh67e6V0136oY98pd1qk2cY5A8DDUZbjsGCR44nBF8fCHadh8yw'
        b'h8zAhz5DrEuioqKW4XQixD7sppJn59ncczUB/ylkrSKjWW9Y0+q7gHR4JtH2cBJu1drKZ+blF7byuYZCrPnilvP0hlafjEKbQWex6PCLFXlGc6vYYs03GW2tvMWQb7EQ'
        b'dbTVZx5ugNakCG71ycwz24hOYWnlcE2tPAGIVjGdHmuriPTF2iq12jOEOxF9QRKMNl2GydDKGFs5/KpVbBUyMLmtUqM13WbPxy95m9VmaeVXkSu30pqNi5NutIoK7Hk2'
        b'g8K/S3n0aS5YpNR4YFXqBsnXyZqXUxAj4ivPEHYYwIg5Irjy+FfKBLmEWhkTwvrS52CajvOzofi+N04JZYLEIfhejFNDqek0gAliCTuV4VT8xBLmGcAK4nAwG0ANrGFM'
        b'yH9xi/9l2RBcCjNYlu7SDYaX0C4sqMM9s+OSUa1GlYDlmnRuPNoLy9uZ5KUUVl1Y8TkRq7AI6wD1gPKjNzDv4op5B2ftXSCzYbGW/Bkxr9vPEQ7nYB3cJIw9llTMDZlc'
        b'Mf6P+UcvUM9imsn1Ag2YE2HOxGN+wBMOYtU7+GwG18fjulMxF+MId8GccC/GQcInRHpSn0jP4zo48oT/Y85I6inIETiO5biezz+pJ5xa5JDQtsSu9yKhdVoPOwnQZ971'
        b'zE8CBTIHSx1PRBqMxslkIelqppBLsueOpClElqlkjTmrwdbK6fT6VrE9X6+zGSzTyVtpq4SA30pdfqtUb8jS2U02DLUkSW/MtFmS3BW2Sg1r8g2ZNoPekkrSiEVMIX4M'
        b'oHnZP4mngz7dXW84pmbWoRTOeAwvBM6CBFgg0EZVJxkTxgYxQRS+7MNwTixL32AShR11WBlNdv2ShT06JbwKT8PrIrQT7o7upJKQ9onMStvrtL0KyAZrlp9b73EwdFqx'
        b'ZtNRXfLIWnp8qSBrzVRizr8C5AdhOMMFLaMwbPjjFIbw0zLGD+s/lGNhqMB8kKngKvzIfSVxnuFxR0jzvrg7siypx3Lp42AJFHXlMENAm8wqNXx+RTrBO4j4AIoO44Y5'
        b'ck9FqFQM9CxuDHetjMkFuFv4zoE7UsyZQ2n3xBi8Z5E7nMITcHNwNC20gog3GBGy8DMBeip+hTpIrROKOQetE+crrxBjUOWweMObZeQep9MnB28xEcaDUQjX4eBpeRMW'
        b'O6Ow2MnbRFksFj0/YLBIyYAiGZ4mEWHO1KsKp60Vub2qMHrgaatlXGZ1DGdEqWiVrNJZqLWSy8awjAmqJXe1JZbAWLwAjW0GyjRyocCbSYHfgCm49IkJZBvcytIpaczH'
        b'Da+0TvVALYZQFkNnAIZSTANZQv9CKcWUsTIMzaFYeejNFMXoMjMN+TZrG6PXGzLzLDpbe2NsWwOYOetI02QcGK+pLw9NMJIEv99K6rlWCZk2jL5ClRme4fl4OjSOce9M'
        b'cQLlD8f0t3evot6PHoNbntCS6nLJve9v4kNaT3ckrsZGMy6BCXDyQXRDGJaj20MSkybAfRqNOkIhBn5RLDqK9iztZPP0cf23xuGLASzGst9idrtEMHBgpJdmiQRsK2MW'
        b'czSdOrO5SIIPxkXiMEje8k7Ag8UiKjmKWru5nPpmGU2GpDyd3mB59H7wBAAEy52IOnSIs8QeBOd/29ZE520RiYa6TwRPhJsTfdFej5MKquOw2n+KC0KlvagvXcg4PFFV'
        b'PFYqBRe6NncWVOG2SlzG+LI0QoK2w72o1E6kP00/eINsSEXPiYhAm6Lj1GgTbJwXkZAc2Atr9FHx6oRkBpgDfSbz8Ap1J4MXxejoXPWCOFStSEgeZ0vC2YmhISWJOGqN'
        b'gjvFg5ehTUZRty95KxGxLxys/Ub7csZJw0ndoru74bW65kXHNyg2NpZP3d+wp7myuaxxEXc/W9ycGzZh0cUPN5lKHDt7i4c3Od4J8rFKpkusI99mdwbs3Fh9T7b/Afj+'
        b'5eAHa9YpRHQXEuI5MKOqROoyxYczocgJD8NLodQyga6hfQuoaQLVzWqzTsj55YvgSRux7w6ANagEXUTVauJlVuAytvS287AKHYTlAG6gW9EzB8Jjyih1nFoHK1kghkfZ'
        b'GNgIN1FrOdweD52JUQnJqnhcmdv2Q+yMV4fMFi0uWuHeqnhyBuqfaTFgpp2+Mk9vNxmoyYLoKGAd/s2mxgiWd5kXi/p3AtWodqU9Wz9WgykLXwlhaLNAih6Nq6wlj9zn'
        b'u3tlIRZcPUFWYo0AJfj3YKiXUeOxPemEQp4tuGluFPJm1QzGT18PKokei0qdTJQi4KU4eVApQEClUah0geDslb6kAybBy3ay2R4LL8YISNEFHsHtaGs7XEIb0Hp7FC6W'
        b'yqKGLnGJYpIGbvAgE67h9K/v8erb7TVjTZTJ6qh5SieZdCsz9Lopz+GSFkKU7PPxhdWtsnr6bEcV+e388NDWRHg2Lhnjjhtc0Y52O3XciGAr3JYWjM4S/5vybrAEHofX'
        b'XW6X8Gqcy8xZDauTUJVK2MEJSOOGw4Pp7UYkAl77t5RQCtIQS9bZQyi5CryWxTxeXc6zujxdXW4t71rdrK4IpUdM8yaUpBm0HuPvnUSyHxMlbLfOjVMSx6v5GM3VClQb'
        b'oUyKn+8hiSIA6w2+6DZsiaMm6TNDRaTuNdM1WpN9aQagCzsFnS9uq9Gux3UKnsqowrWJT2jfynU+YfAEbKTUGE/SPrQ5MZHsBsUnz4lAlQsFKjnH0/R8MEYDlqJmCToP'
        b'j/cx3nH6iayEvd7UPXfa8oB6/7ycFRWs0CXpTFmmjG+1KstftK/PHJDxSsYbGfG6rfr7GWcNX8d+/m4MmD+RmT+ybJ5z5JeKppjtTQZrj2MxI0rkqeXHymbuZwb3ebnu'
        b'pRDmnY/vvXnvo5fCXru7JwC8ezrszMkKhYSSQhHa1qcr8/UQHh1H57g8eIuSuyHo2GxCMDGf2duJaJb7wAs0lw3uKOhME/PCASGJGEHqqRXbDI8uEczCxCOVNDcTHgf+'
        b'6AIXNghdo1kM6Aa6SRTCzcKOYRQWB4JHIOdaDlWbn6VZsEKwAzYnwprprmxkl8dvLItqYB28ItDoOythc8ftdwz+ZzDawyZYEfz0NDqA7Kun51uwhk4UJUqke7uJ9Dog'
        b'ZanijBUeNpiov1ixKRrdmUAa1hgyXeSxTehqX7OA+yJBmmsTeh+3i+TabArwFKA03IovGxk3Pymhvz97U3H7coI+V2cMbCMfHWkHrIYlj6EfxPN463jULJqJrsfCy0Ng'
        b'owIMRDtCVsAT6ISJ9O/LaWH8D8Eg9rvuhcwfwkq6g7WVDN1pnL1uN9MkAfKYXgG5vx+Rrx0JaPKDCX93bUAeGvTaoh9Vo4Axo+8Axko2x8KrXu1RfcMfxQRN/z+aC2vN'
        b'3LWXQa9BE/Ul18adTG354Ng7M8Q244iyW8YvS8G/41KXlkZLv72/5lPLssp4bemm/iE3PipacCL7dST+/OCKd0s/V/617BrXfPHZysTjJanl+htLj1347+1Rpgn/iv6P'
        b'RhaY07JH/Prs13d+/JXvP8dsv71/+otJ3Qx1qd87Z5498sGmb6Pv6koPP3f++azXv+g3cP60cf2Lf+JS01U3P/5JIaPQugxeg5dcWzep8Kh3aEH4gjkCQF9H59B1ZRTa'
        b'GtluVwXLLbNQlbCjsq8H5jkeuWUZOumNhYWJNhIdMQ7dRJel6KaAYu7lhBV41fBSClR7jF68DDlX26g7VJlWuwg5qaDjknJ80XnaHtxrEXut+Up4ykU4+4zGopIBCH4D'
        b'G7ghdGQbUoQm4tVwE2mkB1rPoUvZJmEnZwcedWkPi5fQBg+jg+gK7QOW/TdPkOUp4+iQ+bEMPAd3zaM+is9QLiQ4DKLDcJfbaZC4DKK9z7n6OQ2ddnOnpOJ2zAkdhTds'
        b'ZMu0O9wahaqS4AF4mQHMOIAJS/mYXxOFfpuqI/bQCj8vNKeEIsJNKGweaY71JbYRjINB+I5ngwPF+BqE9c6ifr9KNlzyHRXWWsWutDbi8MR6MJb37OQ+z0MrbPhS0E7e'
        b'2xLuLe/9er8wKaVmVN90V0J6Olaw0wvsOpNgTKfyJG2k1Z/Eueis1kwDJnzpwoh8nmq6G5lWH1cluALa/ZX4kkG6Tzi6lGWZUBkmb8QeDi+siOiKvGlhsxClMAHeEsM9'
        b'qH52J4VT6vpvJRKBW+E0YCXSZWsi4o0ICzasntvg006tzPJSK1N1NjxrZjxjmkzeq3YCMZ5N9Vh88QjEVBymTnc+LqGJr5BioUmEhSbeIzSJqNDEE9vKo4WmziKxSBCJ'
        b'9agmKdFbtSxC2wSZGG5U2El34OYR6DhmoxFxyVFYnnFpfOo0LAHNjSA2uvnS9mEfTCKAJ8eDEd0DfdAxtM34522nOetiQrLz/viNdtndOqIK3j+/obmsuezYHiMzV5Ir'
        b'eU7y0rSvFpf3Lh94PuBK73LVVwHHs/567HjGxeCdIcezXhz6YoC4blGocrc+N+uUriL7nE6aFcdkvCEDr33UI+3WeizNEBpaKIGH3JvSF4gM4iGhcAvcKJCag0nxhNZN'
        b'Rpvd5C4C3RAo8DYDbKRzkQgrSTwJFjpgeaCBg2dGo/3CdvUBWQR1yPeHVRRopPAYuwZdmC0IHPvT07zUSrgH1nvRZxvaItTRjPYHe+ggPAq3Ulp4oDclU1lgpJsMwl0+'
        b'lBLu8XcLKk+HHt5OoVkY8NKJGther1wHBvrKyDa4DNOiEKaoTydYjfKUFDBU3Mplmqyt0iy7iaJ0K5+P87aKbTpLtsHmRYMeI1Rh4lVM7teSC3GatpR4aJADXw51kFe+'
        b'6OtNhX6tnwpWo3HRIcsqcllNZsCPkomVBltOnp42YFnjnqJfYQKWQk+nnsOXA26rFaEsdtICOtJraBtVkbpipPpiYZeESbFgolyMpZ9yuI+qGN3nkdg4sGYv0Ko+WRIN'
        b'OlmyPfalSaBjqFCWxBPKwzx9KI/btNyeBvTS2KMJ3Laou1sx4F7yK7CjK1hUuIqabavQZb9VsCYwX+aALagZgMnouAg1SdEW+2RcZhC8hU7hMpVJGlSj1MynynL8fCk8'
        b'FIfRQ+2O54RnUYUqCjankQgpLAK1+KI7vOKxsacc3UL/X8aedknzCJ7OgMfgbiU8mUQXDj9sIotHlodDVbiTDUKs1+FCPL4q4qhxBl2mo0Q7lLAxggG94RbeAm/DU8Y7'
        b'0neAleyeXGeU32hf+fNftIvvNtU1bGssa7zfWDa8qoCpu1zX7b6kec/EqAu708Lm7g4dUfblxLALH1Z9OyEstKlkXswIW4xo5NEYnjqxvbUkeMvbhxQi6oOD6rESdg2W'
        b'oWtYA6IhNGJ4hh2JdqI91EA1TwfLlFg1v+MlN02F16kVDKvCN5+hJglYvwRtUgtZAuF6bkWRnBrR9PZQ/H67hIYmVXOAH8/AZnjHKPjP7YOn+yaqIrAot8vLLwceGPjY'
        b'+Ao/XX6+AeMioQsdqc0sGaU1QXT/pygSU4x0kzHTYLYa0rMseSvTs4zeKpFXRe5WKaV4tAszJpTrPBhbii/PdyAjt9t55MzB6QN5VJGYooaVRHoVgBnWpFC7AZbR61BZ'
        b'isDWOuo6rigIzCmEqdXDg0ErYT28Q/189BNgNZbliRpcPXIMi/Xsgwy8hM6jS0Lo5sX5+A81r16FLhXIpPkFMkVaAQ9CJ3LZUxbaB5EcJWif3YouoWYf/6QVq/x9A6To'
        b'wmqCpAUiMDiYL547h5rNh+JunU8kxs7Nih5kGaWwiYXlg6wUS9PgLlgBT6NtGKUrkxbDa5EJKngKbV+tiiB8PMkdgzBX6gq5ZQBmSBf9puOh77eTwEW7cp2r9BMU3Wny'
        b'HTsbbQyE1VTkigtDJ2FVfgHcvHoiuoCuoKuYytiwmH4VNaGrdjyOuTxcD3fCOhoxO44Jpl0lW8GaLOLkVpUkAYFoC5cGD4hoFIUBnily1Yha4Lm2KlejZpmvGAyO5+Gm'
        b'AniZiuFCtEcNbIR34EUMiRPx7J0GE7EocJ62B1vg6XC0LUUdjzGqAd2G5+PiJUA2mUUHe8CtduKijQd4MNdPTWLJEsVw10Jh5F4ED16mlG0ZWi+BN/vPsRPv8SHwUupc'
        b'MdnWvhYKBovgBkr7r0+VgrjgYQBotaq/pvQV3CBPj5WApUswRMi1src03bA8TpPVGg7MSCV+D9qkV3JzhLwvKcSgLoDmTdpr1wFqr3xmLDxERA4lFifAHNy5OY/qYh4s'
        b'kRaPgaXG319uZKxjMV50l6Un103WcMODNn6yZt3W5J3f9a9MfHNAQ8SQw/Wcb0R9n26KLQteeSv1tTE+aUkzn/f5tjwzP8YOau/Gp434o+nwqH8+V/TJpMJJUGKaUD5o'
        b'aEoP/k+Xi74YOPW7y7Vla/u1fjDExBfbNxzO/Cyt8X+gqikufWDtuLV5C/VLvggd1n3uGxv2/vOdt5e+fDbvbPGcd0xLPvw/E0aee/3D8j9pXv/IdKJlonr9a+/fjv/X'
        b'tT/XvLrmk7d7HLR+XM4POPSL8f2pqYPmvTjt7asff/zKjr+99xl63TzGx3roVuTW+/bJp35kel57oV/4gOZXi3PGnQ+O/+jg8aLoxr4nv/l+y7B3UxL3Bjz/9X8HN0Rf'
        b'e6g6oexTuad7/5RqS3rGj1/Kov4hXVHx+YWXU4Y1fvXMksUnXv3kzfs5vZdtWfL52jX/2J81+KvwD7/u/yB91cb5FxSBNJINHc0pTiQnClSp0Cbo7EmsS37oAseihpE2'
        b'wnbgzenoemLKcJOaAewqZiosXSQo3NWLVwoi3hB4QiDa6GaOoCXfjsLQnxQZFafqPp8QFT8Ti44mwW30baYvpjtVKg1ZVbSvJ9ltQFVscXgSJfjz0AGxMkVFNoEwyYGH'
        b'EiW4O7dZdBXztwOUXcSERQpECx3s5SboCniejiZkMTylRBXxqvjhlGmgTSIQOInLQtvRHZphLNrbP1HZnagBGBcUag0Wbnom8bGwGl0SIvv2Y0pzR4lOwctt7qe1LMYd'
        b'3H3S/KB0GpaKsVqSjVoArybBbw2hdE4CsZhbrUxITmLgnT6AH8BgNf12AbVQjkRl/ZWoFB0TaiU0GFeCAbonvMLHYRZZQWtHVyWwXjk4rx2jrLDTro2Ax3OVqKUwqqNh'
        b'ZTaqeaycKnlavb9Hl1yNcsK0Nk44ifBBnjqYYt2fDfLFf2wwQ66+XBBOC/PsO8uof00wdS4nnjgBOD2ADaZ+O0GsjLWUuRlwI+vFG5+k414OYaSSlg7c8n6YN7ekxu2j'
        b'arjlkewyZRY8RmmOCCy3SeGObBrxT4SNAVMXtJl+YCk6Q1SeE/CcQIir4Em0G1XhmgLh2SSXLRdeZtExWK4Udoebk+FOpZpEm5ejGjFe33p2JNyALmRyHSS+ULfURzTO'
        b'TnH2wBNpz7SLtWedPbJCPTsTol/dmeDo/gz/2WC8pr5yr580Q7bRajNYrHJbjqHjETFRvu3yxtvkRqvcYiiwGy0GvdyWJycGYFwQp5LzQEgMoTyPONxlGLLyLAa5zlwo'
        b't9ozBLNKu6oydWbiUGdcmZ9nsRn0UfKFRqzl2G1y6sln1MtdwEh75a4bv7AV4i60q8lisNosRmJ/7tDbCdR7QU4UvglycgwOuSOOfaRKV/V4hF0UyTUUEuc7oZTroUNB'
        b'vXwVnjPcpy4rsFvxS6G4J//MafHT59I3cqPeKo+YZzCazIaclQaLOn6GVdG+Htdsu/0OdXIyRnM2cTrUyYlbJumOu64ouSYPT1x+Pm6L+PB1qsmYRUsJE4rXKkNHOoTX'
        b'Cq+NNdNizLd1GkgnY0wA6KiY+GloNF1feH3U3GjXrqE6bWEcFjbnxiWI0saPh40KX3S9cDzcETtwfA94mwGoDp2U9cL8ohMKBLnr17RHAeBCAsaDBKwzMCvoKTbkOumV'
        b'hH50PiJCrcH5KG3p7GXV2YVC6B7w7Az+phAo0kznECiRK1CWUGfjJ0fSOasF39V+MvQbrfqrOJ0s62vtA+3KrG+18Tp+ywPZ69XGpA9NMxf3q5Z/r3lv0pWA92zyj++9'
        b'cw8EG7MO77bpKt49LfrmtK5OD74xrMh67SvVpgw92CcNTb/bFPTaBV3EpQfaZXev1a3f0lDWSz8thssWg/3Sfv+K3+2Onq7DEutFpTpCMLXvnQCbWbUf1uaI5WdqL5MS'
        b'1RI5mrcz6NB4zOeOFD39FpUofbVFl0/ZTXgbu1kHehPnzjBKy4OYEEZMYyCKFBYXzfJyV3JBt1cKqdEVhy34Bj6xmaeREQpQFkPcTnvinllD21hMCfim3U7UJMpkhomU'
        b'BAsGjyF40EVAaRvzmRmsiE7ADH8WPBloRKfCHu2yM0ZABvDUkcSdjAtd+xhINPYZpPN35owfGTNqxJjho0fCq7DJZrOsKsCaHNF5LlEtqBldRhcDpVhfyQ3w8feDm0kI'
        b'DItHja76oLNYmLxN5f2/8gkk/FR6d1yx7/JVUkEJaBweB+qwKBezzuj7feASF2Rf31HOWpfiu9fqM3q8NCC4JEbG370xSlzF3C6N/Z5TXXtjXn3ssFPHf5ezLmHOxD4P'
        b'4vJ3ph6NebU2N33Y5BdemL4+frvq4+8m3nt3VPmST84q/7FuQVhSz1HBvwu7/NYHa7Rx/a8dD8liv3DBsMiE9rjEyBbU7JYjDQsFAfZ8N1iGJQDBpIDqtIJVobf21zZa'
        b'Hhd6J0235NnSM4gajec7zBuoIwhQB2NwllI/5SLVE4Gzqzr3JorH2/XXDAuskKMNmLEICYZ0AuaP24XqEXiIwiLqLaWbpneCZawxdABntCkaVqaMGMOBVbAqKAodQ2V0'
        b'6dcEcBigv5NKgda069kcQI+xgdfQPuRE20QAXogFUSAK7h9Pc/9uPjlx68d0HmuLTSt6C9AzcTxxcWgawMdqTb/D0jWFHvrmnr8Us416XqbVmj6drxQSjyQnYgiMVYmC'
        b'tCt2BnQXEq1rg4AcxGX652tl04ctBdSDezE8NBPWoGtzMVRsnz86Bm3igTiNgWeWoyO01A/pvcEosCZOFqR1jLO4jgrbN6qZKeFysPj+6erd61bmCgfDlMLNM+dCUg+q'
        b'EQFOO6kHM4VIh/bxZLxVueSAlzYVFyskqALj2R5VAjE6JuJn6meBNiuJlA8rlb4KjGGldD/53lgxwN2Vg1kmVUuwYbkC0AjZ0NXDpNLRzAhGm5RoyVSPzU99Y4wm+BQj'
        b'zPARJcFXhpxYUwKSQfJSdEfwFwmYAGzgvkwcpE0bEdzLNaTkZ8AG8GO+T2qJ5QPVx91o4vKgKcABpJGyGK1lV4grAjLeX8Vo2TW9/eQl1t3dm/1p4puq95lL3MnpkqD1'
        b'eWHr/rSAJk72m8VsZ9ekisD63EUz3uxLE8V8DyaG3T3LB5QU717WoqaJy/rYwHfgO4YBJas+KPphBk2E0+cxJ9ndUj5I5wcXMULrGydsYSK4kpFibUn27nU1GpqYP30R'
        b'uAbuBvnIS4rC+r8gp4lpSwYySay2P5OPGwr9SWjdNqI/mAHejJCkljgWFf1nGk18cXwyU8+mWnzlJblhg3ZMponvzg9lVOx33f3k2sm1Q+VC699a32TqufvDWK0uT5kr'
        b'ExL/NOR5UMEsChTFauPfGWUXEv89uBj8CMB031Ttguf7OoTE383+GFxjYmYFpGqfXb16mguCe8pAGIhdyqZqTecmuIpf1BWAEqYijwefZsxblTzIKFNdYqwNWFj44b/f'
        b'z5/zsvmd2KCzy1f+Tj8JBQeG/1OtemVA/7rMX7QBDH91mLVpVHCm5uR/9HUTe37Zfbb+v4GHtlm3r5AMGPDq/P85mH7n1ArnmWdFKO+PZ+RX3pmTfePovtWSjw9fqEv9'
        b'ZG7/Zz9WK0X+aNEPn/8hevaA3Bdmho74YGvUiBfHf7H/4mem0sqfYuNe9PFnH0TcrH43bnnBzkE+ls9nvTx8X8bit/Yu7vXhXGjS/unL+gP5Ww6Urb2/tce4nCH/mXlw'
        b'9KKfXlLeTDlRZ454sXTwv/4xoence7dyFpzpOfqFSOkHi/84r6/fovOr+m/5x/U/lTctnu00TL3/3ryXS4v7Tvz2X1MDio7e+zT0/+j3W4a2fPvMBlvTtcm+f3z1p79e'
        b'2Xc7bVKPj5Eq5+DO7Of7fbRyx9WpnwWJ3rvmDO7z0UvcpOcHTXqx+6QXRk768+vLx1Xucrw9e9LryhPft0RO/2XJL4MPPV+495lPX37DuProg9y03117/1j9j03/Otxj'
        b'ymc/lV8sTpn471rYN29JwaxDlkPiP209+fULu5TZy9JOLx/z0tyZ/438+NWffXISu2+tfuPH9O/U81ckbvndlHQudcXm3eFnFFJqiEaVsBaVekW01vpMYdWYh26zEewM'
        b'WYV2LI1Toopocr5UA5NqRbupRaFPyPB+MmWCOlEdqREBmZhFt1BlJmVS+pGYCWMepVV6Gb4x220RfEtb0PHxmHakxMMzmIiZQhaxA3G+TdTIMgndgPuUUYoEpeu8vmB0'
        b'IRCVcHlYmz1K+5sROlKBrngMMR4rzOx0wYXjNlxv6XQkyHVecEmqHfmUW3yKoKd3UnhiSVLqZp2U7zq8+W6ojOHZ0IAgX57xPj6J/A/H/8PwbzAzmBGzfbGgGUDjiUIY'
        b'ngtmQkm4bcfftrRfWJb9RcyJKTeXUu97Ga6RJ7sFvR/N2wXZVETDAVolLi2zVURVRy+m/r+PqcLyLznYR4g7qPHIApvwJbiTLPBdpLcsQLnX6eFwvdLR/5HSgLcogFm6'
        b'E2KJ8OYSeIDuNcJtRrrFrkzEoFJCgqqJtVfjsZhEw0sidAYdWEm3GMKfQ9eF/Tl4tZCaaYjbahDayIWvK6TEMSKeBXzqLCwga1UGzJ1p4gfzsYgQpOBBrFb1idlFcCU6'
        b'LEyETCamZ9PART2Akdm5hrMewm++yVjSr3pyAIyRzfrrUOPbl/40VlowbMyCo1ELXvhoBMtNvWD1u8YOe962ZuvP//73tpgrC+VJP854tuBeuXrX0oLX/a/e/HRI3ppX'
        b'bzQcKX3t1WE3y2xvz7kZ3GPXpybLruLasbcqdu1OCgisi/Fn9X/+6p81X+rV61/hBn+EJHP++r1y+Z65926/ue7bmlsNq7R5x35/8+EfWsYf+Pnb7fywk9HP/I2LXv4P'
        b'P5eXYxGqhhc7n/+6t8h1/Gu/ZIHW3IRHw9w2SmqgrEmCZ2EJ3CS4jaP1yElWyBbQZvpCm5PIfuBBPg/emEw9lgaiG7Nd66hD1TQbIRSRHDwJb6AKSkfGrZlAsrStXQA6'
        b'ijbCc9wMPSyhREpiiIJV0WqNGm1KUohBIDyU3ZdLXwm3CHH8W9E2BlalzECbqQCkSvAcJtUHbuHhEXQGnnPrjqH/12nEE1MQN8pSChLpTUG6Ee8nlhk6S0ZxnCURhqwQ'
        b'YSOmNMOyGed2qe9VZBjd/1/3u9aDz6TpnzrYQsvHeGMzlVSrInhlwlJ4w4XNLAgcw2WhzcYud6LJj1XGtDkQ6ZnFnJ5dzOu5xSI9v1iM/yT4T5oNFvvg/77bue28XlQj'
        b'nLtFHAB4vVgvoXErfgaZXqr32QD0vnq/GnaxP36W0Wd/+hyAnwPocyB9DsTPQfS5G30OwjVSiyiuM1jffYN0cTdPa4yntRB9D9paMH4nJb/60BpyDhc5ja6nPoy+697F'
        b'u1763vRdiOu5j74vbqGH66mfPhw/hepp1LKif2tAkkDDk3VmXbbB8pmko1WVWP7a55FTX452mR5XwmglJj5qZ9UXmnUrjcTaWijX6fXEDmgxrMxbZfAyK7avHBfCmYgp'
        b'32W2FGyGHnMkLRElTzUZdFaD3JxnI6ZWnY1mtlvJ8eDtLIhWkkVuMBP7ol6eUSh3RWVGuYzCukybcZXORirOzzNTG7GBtGg2FbY3LM63CrZm3JTO4mUepUbk1bpCmrrK'
        b'YDFmGXEqGaTNgAeN6zToMnMeYfl1zYKr1Sg6mTaLzmzNMhBDtV5n05FOmowrjTZhQvEw2w/QnJVnWUlPwZOvzjFm5nS0dNvNRlw57olRbzDbjFmFrpnCrL1dRQ/75dhs'
        b'+dYJ0dG6fGPUirw8s9EapTdEuw7ZfjjU/ToLL2aGLjO3c56ozGyjhkTz52OIWZ1n0T/aPjQOUHskL4R0uWPIillqFn20hYijLnf8w42djc5mo82oMxmLDHhNOwGk2WrT'
        b'mTM7bguQH5fh291jwfaNH4zZZjx/U1PjPa86G7qf4NxHsYaevp3jH/7oiJV4eN0TsQK3wBPCceJbcmAd3XzcvoLsNxP5IyJOFRWFNpNzY8fAXeLnwqMUDN3TSZ6O9pMD'
        b'dlPUJHKiZlZqCgOC4X4O89C9qNn45fGrjJUYU3IOv/TN397XvpwR8fkDfFWFPtDGuYIeohZE6BJ07MVePWNWx0Trl969UNew7XqZoupy2fWy4VXqjdd3NZYNOTh544Dd'
        b'60dyoDS926HXnsVqA2HCY/302b29pSlvTr3KQvOgE4nwehsbzkCNlBMTLowOoiNCnr0ZqMovkRxuvAVtcUsOoAd08lJYFUy3HuPQJZsS1caN4gGH9YO98BZjRkeUgkjR'
        b'NJtzTQMDYNVz5BAquB6VoAPCHnHThPGoKlEtAVOM5PDfRH6J4H5zbK2OVjliNAfQSVgtKWLQXngMNQi1NoShMtLz0QNQRXKSGGC5j0HX+8ODj3Vo8xbv040YQtPTKXMO'
        b'9WbO64CPjMYxEBG8qGd70I1ylxOYc6PghWwhJ+U9Lj6hkRWytbkbk9MF13WSnMtCvJ39HtX+o8OoiMzqACsEb1iG4L+PW1UwNDJC8+1Dqix0XwB3hEZTdWrSHW/1sNcj'
        b'N79wI5w+L/OJOpUtdEqa7lJVLHsf0aMt7h49DPHaAHPvo0U9XWOEwBr11kc2tt3TmIo05pbduthvyzQZMeFWWzH9VjxZJzYInfBLN6zJN1oob3hkP3Z5+jGI9KOtBGE+'
        b'HSe+ffNugk7P16ME3XV0qFPkRdB/w+Gh7c5j8Sal1Kf4NCzvPRfV8OQIXBJKCODmsGjqCzQeTF+EDsHTuJPFoBg2jBV2s+uZOagqnsrsI3kgNcfCKjaBh6eNk//1HU93'
        b'roeN6d2v6mX/u3IZv9p/fI685phoxuAVMecdS8sfjAo4369mlWqP7aZjXH1+76H/3jZv8T9HFajnvnBR7B82+pfmt8Z+Mky8Y+0XG2YUvDfq+oqiZ6ecfLnmrSlBPXqx'
        b'b/RT+NqIgxlWN8tWe1PItYO8aSTaDhupE2Lf5+ARYlWNF7wAdegIusHCSrQN0yIqBV/sgS61HQmsQg1kPwDdTKG0sZBd5TaV8Og63KFhYBO6Po+WjMzE2mqVx/0Q61Zb'
        b'iSUmYYRQ77kZqbAKVoTh1140LiRJsNI0DlmQiGqjybcfeAW8MIaBNzGFrqeN5sGrE4UzpLEuG7eYHiE9B22gpDMTNS71PhawbgA5FhDuRFuoD/goeCSXnjke5ybaweEF'
        b'8DSHyuEeuLHdsWNPSGQN5kxLYb6NElliKvcisuEy6tfhS70h6WmunUidq7R3vMeTnSfoOsu1jdIewZe9rHsDpcTz+/Wv01pXB/6fiE3ZXYpN03N05myD4EPhFnTcSN9B'
        b'iMKy0JPKT2bD6icVm7o+5ZAnn9QgIkEaPImOe4k2LsEGrs9E60fACuOwQ2IRReHR5Zf9X5kYGhsT8uX7/Jt7bv5oH5M5IOLrUYr9ZwZEvh7RtFF/4qOHm3pdgK9+OdLw'
        b'YY+Q8KAvjxxw/Kes8vfDJslDZWHDdRuXnvllWc+KZp+bB356T/za1/8MbNgXkv9mgcJHiGU4ii54SR4MPD/OrOguBMFvNZFz21NI5Co8pYpgQACq4WBlsWE22k1zLILr'
        b'h3SAdAznEd0xpJcPpTimhTtSiA0CbWIAH82gbfPhRXQV7aHHuqJ9KUMxEhFnsBRYE90mBsagejHcgXaNxwizXnB4a0ol5xMkwoMpWNChYs5odEPwcK5Dm8I88hERjtC2'
        b'RCwfnYZnhP3Ey3DrGI8ghIUgEWrGctD6OMEFb/0UeAjTiB257WkEbICbnx5VAzMp4KW7oaSj7zL5jfalNskQpii8A6J0KOwyXOx6JIJadnsw8xi+HOsCMz9uh5mPaVDB'
        b'tYpz8qw2o77VB8O/zUx4fatY4Pmd4o3aYy/vjjTwYC9PXaAeHWfEUV8Q/rNpTAdlnfxM1euJwkMwzktwEBRFD9t+JNoKgxCQNg7fx89wI3+GzpzbGXU92O4as1AyVXjE'
        b'hSMS7WasZqrjZ3ThF+TlY+QuSZRqUqydT5Giq/5aDDa7xWydINfOs9gNWuIaJBx9oFfJtbN0JquQpjPhRH0hlmOIOGW2PQH18e1EfTiN8fuEoYyV7ChfuH3lG+3yu2/e'
        b'++DeO/cu1F3f2VDWUDa+qnlPc/rhnc3lw6sayxt22DYP2L++8t72AXUDKnTDp8fsrtXGMRfGvQ1eWuavqS5TcIIicSol10UlFqjb6ITBL46inx+8iDHQiwTshE54MRzu'
        b'oBIEq1mUmBQPK1OS0aakKHgFHoW10dQxVAGrRfAs3MM9PRYG6PT6dEOGMdNK5VWKhEHtkTCWoGBRvw740L6cSzcRCwyQxAtbTpDLyfa80/srArxXtjxPXoqhp8isd4Gh'
        b'b7bD0F/v0f8zHJzdFQ6mUYsWRkOzAHfE4c0LGb1sWf//Q0dSLH5uilywQtkEoxXVG7KMZp1JrjeYDJ299J4cEaV3unMUEXvYlI9FRImha0RcAl56zt+06Q2MiPSDYndS'
        b'0REvfo3uoH0uXJSjY4LIewyek7qRMR9ux/gIL8bAchuxq2OeuXOBMgHVoJpotAOdT4Q1LrR0oeQzsFYSjNaji0+Pkt0E8+hjsDKFYmUHCS2qU1EXYzzdAfssZzzIdg5f'
        b'7nWBbPfaIdtjG3rMR1UYJ/D6qMqvn4XtwrSHGV2gGYU5ig9m+8oMjFoYzLzsyG3W2Uy7xYKpv6nQS7H+rRAYc38wTz8W1N05+RvtUhJxRmFv+J4l7aHvUUwge6Pfyfff'
        b'x7BHxKgxWCXbD69N7SQuGtLWCFziCLyFLrTxgcVwLwY9dA1upaLgSg35TFVtNFYiPcyAQl2kGIPddcnsvnJ0NKHDp3O6BLTMPLvZ5rWG1q4AbaG0K0DrVFTjdljMeyTJ'
        b'FywQFOia8OXNLoDuQsCvAV2nRv8vAx2xK5sfCXRt3stPDHDyiEgilhnN8lVjokZFdkGCnwwA++YFiSgAhv94oh0Adg1+vrfaA+BIkO30O1XzJwyARAuAFX3h6Y7Q16+I'
        b'M/DBgp6zfuw8E6z3EkTgxeeiKOypFNnEG8w2VxXVCfbGQacYg2kzKnkC2Asic/k40EsXDt/qAAUdS7pIXPOjoe0ivnzQBbSdagdtj2tH0bNjkLMkPV2fl5me3sqn2y2m'
        b'Vn9yTXdvjrT6eaJSjHrLHlLoALmQbXxLA3AZY1ul+Za8fIPFVtgqdds2qc9Dq8RlP2z19bLhEasCVWCojERpN8UlOkTBavEbztHwMgiSjxitIFM1C5Cwa96PZ7x+WSkT'
        b'4s+SQ9x/EXOP+M8H++FcMhkTFED+AqQ0urfvZLi1LXwZXU7GiizWQlkQAdcvHy9ah9+1dNpMIdgdC1yHY7TfxxWc41u7u6I+XEtHTxJ+KJ+5hhx6SCyYmSSkw2Im4piX'
        b'+KXBOmL7pbRc8kxDBwvpTXz5lPXEofOMnZz6wkuCaBg63AybhZMcmtxjc+9ZJPhK4OblqNRODl7ToNK5T+ilHDC+Z2cv5YJJnUidn5tQENHI5dgP2n/ksu0U1idw8e90'
        b'jgVppLMNVqZRcNRJpTDbD0SAiIm+QG76QK7Mpx6fP0gloC+ImREQC2QfLvpwyDPARKK1C5MmiR6EXc/+78w+iuu5qemn+p/MbVlUGrFX8+K4Uc/WqA6knJ14bMKyfm9H'
        b'Hs74WfUweZ3/V338B/xcXKjUzZFKckN+1+8fLJosGxUy7trwjaNeKl6VPG7IuojuEyPmr3nmCp8efCz/fP+M9D8YL0kGzj+qNYxLyH3N56/xk5X+PXMWWUQlA7+ascr3'
        b'L9ZV+RE9P5x5yq+Xf8u6/2Kl4OslPaXCFwr3Lk7xsg+vhKVSYiBGFSI60pC+LIgZSKJItKoRq13uk0mTu4Mzc4ljkrZvlq3Q5bjj3xPoM5YRx52lf81xCDGjK8cyqCpZ'
        b'HUU+XOo+nQxtTpSgLbCxEFXOhDtEQwDcMBTegjU+qCEHbRc+7FvIg6a8nhgDtCbdEJeDpdMoBvn6PqQB1dS+WcIBo/fem0AWjuFzAPPgnvHmm6+JrE6ccK1q6ZCaG/7c'
        b'cNl0xcv/Kggd1+fZoRP1ogHJLdMTblT2Mfg99/b9a7OeHyRKa4Sh3W+MnrIt3vn3+kOLIlJffjN/9pH77yRc2Tsq8mginLh/c+CD1q+/eWPH4K93pn54Lf/I6Rf++bdR'
        b'P0+VJAWsiX497/2cz/2WlH8y+Ujlc394reXHhL7fVr+c8vz7/U/XDt36zl4FT+VppTq1zRCMwXsH/UDMUiP19ZkODz/XyWEIJKGjru9FXx4icK4b6EymUk2+w0nmUAT8'
        b'UAs7dia6mpMqGLG3ovMYLevRESXaFElsXCRwbXxoWmcH89969qt35L3FqmtnbyYj8WJfBTz1xCMnLkvZIEZOqCe+t9x2V0M+Rk02+L3Epd/arUbGctdDs0gD33TB73bJ'
        b'vX1qyNEMC9FpdEcZqQlBl2C1l0DQBx7g4WlUKulEdtofndOJ7HiOzvlNJKfrbR9fN8k5PoaQnJgMKSY5u3v9kis4mQ8gJAfkO+IwyQn7aZxVIDl/iJn89CSn+Ob8pogN'
        b'00cn/FlTOPWzcHFv374fLZq2+IspN4buT3tmXmW/7ZE3+y+ZFh2ftub9wOa8v45q5bZEpuWP6Hts9Fcz/qk/OL/cb5TqOhvbzTpwouh/xk8ctz3x24HvzqwWf7xuHQCz'
        b'J/I/5lVJBLd+ERsQxkopTXkwTitg9/fTgrNeAuSYXa1jnHm1sCtH38yM4NcWcUGUGBgHuL4BtWOYeNpgEEaj2XsvjAT0C7KTgmIFUgZ3wjvCdhelZZWo1DhPJGbpN6JW'
        b'wrnqV5v9UcyBYhl/98TyC/u7bbj04X1lUP6WN+b73ghmHVeaxvqLrg24d+fEH5ip3/7zyCsfTJw0etyhNdbnCpfX2/6jKt9Zvnvu9Gz92yvn/9CU99Oqiaq9X4UtXBRq'
        b'mLyy//cb3s/94fqnzb8wozX9dt/8m4IRorG2oHq4MZFwS30E3Q1axhqkqK6dtPibj9yhyKg3tCHj4PbIuI58y5sgIBViKELKKHpaoKeiO7+hB/c8WEfq+bkLrNvofZQO'
        b'3dKQolOwAWPdgDkY6eKT3Tin5WED2gBPdIr4I3/0dM8FGBsrRMIh5Q6mHhBca2CLWXrP6Xl8z9kY8n4GqGOWBSxli/licpS5qALYWHLKviW/KMAhquf0ogamWLQQmMPJ'
        b'QeK5vhaT8P0a+o5820YkHBxuvusg31CJoXWQ8hccnKUa5xI1CN+xEdNvAfTGLYmLJRWMQ0KOO9dLanB+h3gSKNhuXkvLisrIt0o4y31y8j7uvwj3U0SPVydlpZ3KSnHZ'
        b'N83TaFnhyzExnUr2fVTJOqbAt0Is5MYpwEFO+I8Qjnd3fRUm1QH0Pr0weXEIgZa+GkyLDYb8WRYir817KLLbstTjLOScfAygiCwweWEhB/jQL3coJJYsAng+BrN9pcFC'
        b'zv+fSZ7F5DhvvaFVNt9sJDdUJhXKThXgq+18ybZq6fHqNNqJnCxrIbHfrcyKpwwqb5WRT25YRwgRt4GcK+qTHEAuc30KQPj8BPmQhK/r4xOhXncy138p/cCEVIDWItQS'
        b'j+rWCt/bHhNJIv6po708nEfNK1I6+SN4TtYmeOAAVqmemQvId4To7LNlLtldQ2fRMt49AnLyrvUR2qI/HVe6LS/dlGfOjuHcn5jkiFZCz29RrlPQDkbBHWqskWLyR04n'
        b'pHIWGAo3igrzn+30wRePr9Yo2lE9k8tYZES10HMO8rkeRs/XA/IBGNxtUShoYBxMT0AYG0mhgxC7BkG9J9gha2iA1wNWGI2oKMtoMinYVsbcyuQ8amRkQGRgdIRjych8'
        b'XUtGz8BnhLORTsELqIVo3nhA66aRDzLjAabQFRGDoeGiQqX6MZG/TJeRv4//KF2naEzGu2qvaMy24LYF1nzwKebIN9Zqs36fLhYSmXASbgTyd07V+ojTnxESnxkrBjIA'
        b'chIitao7UwcAY0X+v1j6PYhVef8gZ9eRs50mf365rLHs8p7fbxzw3qmdDeUNZQP23Yo7XWZnMv2n+34x7bjmvWnre5eLkvx6bRLJD/dT9XtttOz1akVScGzwYTbiRemI'
        b'IRuflUVcKRm/0TAgM4bLngAmHO9V8Px8l2CKrqG6NW1BwizaixrUqEpPJU5+HrqmTIBnLPTTbJ7vsqFbqIwaklPgbeJVoULbRBqsAaLNKgZnOc2ic7AWXRDMeTXz4V54'
        b'mp7GgSqxSLqWhVXo0sABPZ4+2rjbyjz9+LHCFw7S9cZso63jmbiug5+kFJcJDvdmLG95KnE+SXMV7uZowVjO3UCJ1y9sF0VMVOL0OXh4VagmBTaPoicEk2/LwNqUCSTm'
        b'QpiYcfCEeO08uOHRJIPIwAKhIMytQfh2CKtpFemsmUYjFnJfBG6eO6j9zEhyDGtMxqzCBNJd6j3BUeqlQg1Wsu++PZacjUZOFzvNY7VhI4ta4H547tFdIatLPt9BuV4I'
        b'+eoN6VCxq3uujlneBlT2nuHu1q+d1OVjN7s6mdJGwYgIQkVxuAc5eytRDZ7Di2PjvDpLjkk7kI4OP/Ws0c5Z3nnUjPlkjBklfKppgdecEeYUiC6h2sQRI1EdOhXv0dkC'
        b'B3AT0Y6Y/8WMZXs69d4TzRfuoMBMl3SYLwKOg+YF4i7C7QPjiUQpBHWc44Znwa2dXNQ8HyEjMel6BhN2IjMBS4SNkH2ujMVyBCjmhO8SOVhM5NkCqYPNH+FgyDeCaM9F'
        b'mtbBMcNHjBw1eszYceOnTps+Y+as2XHxCYlJyZqU1Dlpc+fNX7Bw0bOLBRZAiLYgJTBYIDCuwmir4FvFwp5FqygzR2extorJYRYjxwi836fj2EeOERYng4ydfluXE6xw'
        b'hIFTUR+WThEljhiDSuDtNs06sCc3waezk6BnkWQuWNEzLkaMl+QP7rYxQfq4S0gZOUZYCFMHSIE74H50DHdiDbqd2LYOR7kYDMyPPm6Rfo6Z8XyOGXfosUcsdnnkYOeP'
        b'ePAa+rENx2h42R3UjHb0QlfnJ/vMQZdhUxq+XE7zh7UsiEDX+JVoY7JxytyBjJWMppIXfaNdhJlOv1Idk4lZy4ta8RuhYNi/+bTCDFc8vgru7qdUx6NaVBUtDZIAn5Ek'
        b'DhLeENyAWlANPNcWsJhFFoTGKx6ARx71JWWjNS/dZlxpsNp0K4WDJOhXY7zJ+WrL555CG8CjjOo0U0GX5HpLu48pE+j0J07XmG/Vws3w0Ipo2l11VDyqVgMw1CJaB8/B'
        b'07M6uaG1NzpyLjc0L5MjXlW/p3D87GQBIFJBYKdV7aYR/Dir0GZ4LlGlQbX9lqFqHoh7s75wG7xIhYnmMT2BSnpcjNVhx8xu/sBOfBNX+aIbI0fA5rnrRsSAgUCiYeC+'
        b'tajRLpz3OAeV4JdX7LBxBLzM49dwFwOvwA15dmJxjusthPqD1Ekk0r8JCoa5L4eGgZhFvTmg1U7646qFgiSzRq8AqdItEpzI/rzO4TotYE8U3EXPwtPD9RPBRHgJVdDc'
        b'OQOlIAjrITi36ews1+F0aelYJbYtk5BQwIuR6RhUqLfr1BC4OzEenlGJAa/r1ZeBF8iph8JXfWfE4rXNxlKVNm2eO4Q7e/UU4JhEPMO0aWGGLFeYIRYTZbZ+DDnMjrFp'
        b'gLHPx2re+kf85o0PDsxMbU7gp8qSR1wceaPg8u3ufsrEO3fvNKXeG3H/Mxh6eoe+t2TAwoi18G+H9v6pdtt34et37eqZ8dN7vh+VjX5RvOO48otefM+PLm588N6i2K+r'
        b'Wl6/0vTn5tX+Q+KW3n/XdPaFdcVDjaFn5jWXDPli0zQueSIq/aJmztSN4/cvjf/7798NX+o30NH08J3AST/O7PbHL+7eGbds0Jljn8Z//JfCgI0JEb9PjZ/wWe/Xnn3j'
        b'dgF3Ptl4dKFzf/+Cvyx/uHWUMeiPd0MT3jtZWHEwv/HDq+kf3Rsw+d62P6+bsPkH6TerWz7ur1o/3fB8hUIs7GjVhizD5ImXudxQl7GGcHSKSmcauLGv68O7RLrrj4UC'
        b'IuCNcZ1AXLSqhxAMDc+hcs8Zaw2uwpOKMTjCsxHsCJe7ruCrW4dO0J3e/6+9LwGPosoWrq2rl3Q6IQkhCQHCEiAbiyCgrAoEkkACgiKLtkmqA0k6nVDdYYndbqDdzarI'
        b'gKCj4Aoom4giouNUOS4zjuO4oLaOOjrquD5HR8dBR98551Z1OiRxcP753z/f/z3yUV236tbd77lnP7w7SLYMJkNzpLbfMGW4ivmsu0J7VN9eQZbPQlVLAz95pvUnOBP/'
        b'N7Awk1vgIPK4AQSNGzNiJAGfc08HPpdLPGNkwtEjOvlcwCxlQeIHIDyhYHJZ9IyFMFTfNSswPH3EHHXNaq3HTQHy2vmc/4q3d0H9E8cl+gTBulq7hHcbO3A6ycHnGu0u'
        b'bXfRzOJCfWfvSuasepP20IhRIyRuEC9pPxvVmza9vle7/rx5nL62leP6c/0LtWtrTXNC/NdBk2gZhwgPhkOMAimFAewiSDdagpJaHLTAfwlOWksWlwG5ekGeoLCLJ61d'
        b'QygdERXR/G6NyELeQi5RrYlIu+B5UNwtQMkMdZIqOxGw8diMiHlRxNIMRp4GocBeFCuv23ilhHV0c47gCbpT5BJCrObVeJuB4mAqPl2FWWXIjhiztLa0eFQVpYcxiehf'
        b'OSYFPKsCgERgEf76Nk/M7veg5lEA44eurFcCy1SMvhcTFU/nGKrQxD/j/QfxNetMbMsW0dQaFW0G+0Li+/4giejrj4XRWo9O9PZNr8Ag0FVEkpDDxdmwm/vpt0r6A9qt'
        b'+kOdcMb42OIkI85ImC0HmG0WcdswFjFM+i4cbTikFBFHm3hxgloDEy0oEuQQgyJGccY4lSERJ5RKWARPKZYyvofc4jxOsZAZhFx5auiEJZNXNXmHFU0m/K/et3Ti4gFD'
        b'Lhm6+FK4FhXg/bDCyUsmTyJM+kNsLGNKPcERbYcnc0z2e6rV2mUxy1K1ubUlZkGOEPx4m1fC5DxJuzMmQi0xawuqbKm+mAUGEz6wmZX+GGKeii4X4Wu3mXmXaLI9Rcn0'
        b'PkARJxnYkJjzbji5HnCRM0PtIPqM0aJVDG0lF5PzK63cuAJZ2942owPa0UEMuZUmA9ByIYNDNJ2RFmoAzV7UQXjdxe/m/MOCggJofJBzo0GMoE7CK72ZFgTE3w3/p3GX'
        b'pIWIXIHSxF4wLTy3fCbl9sZzb2K5fTlBXt1E7yKnvzPQGKkyxjtOCXl5NBcweLRe/0LbIFBd74WtIXm8niaYA88Kj/dHdl/M2aJ6AmimiUN8qH1knUas2FSe+WtIJR/y'
        b'rSh0GlTYTz+qHy8aWl5SQFSjtoENMc/11263DK30dm8jjbGU22XrAJa4RaJHoph9MLSLLFvFBrnBusgGzyyKTM+sHmuDXbGaKcABrQDS0ELatsihDMD4f5BOUpxr7YuS'
        b'lIFGOllxQdppxAeUKG5gipIK3yR3eNZDSYNnrvgTSUlXMuBJSodcPZVMeJZKltHcoh7KoLAI9ATaPtsXpSn5lOqr9INUujIYvpGhBXlKf0hnULiInrTfhsSSpsOseHyB'
        b'84EW67DuTA7hPBPAtjPcKfQsp0jmvRE4NsaHaPY//AH+neLPBVx/BkdWeKQTNSc+zQk7yU07k0Jf+1uqaz2/ihNYQltuQtOGnZ6xSwqP2orUAxLfsFIZL4CMwQRV5BHG'
        b'BqqXdmUJFrO3eKvrfW54/UxCE3omNiGeo1Pdgll3GsdM0Jpd5l4kGpOv3CvELG48B2hPdGmLhjvm+Xb6si01sW78tNP0xKt10vTgdlfiFfKqFaO1CXzXNb3c3stOVE6c'
        b'MeyNTztBe54xg0n2MBOlLiwIbFBUhEZBHa0gB0GYgAFeYfc0yv5MxRIU8RfgPY9SFXhiZV9lcmZehceIyAbTxlZ5ih8e4wtPCcOGw5SRl1vcqSqPk8dffspyeWEo348H'
        b'LYul7QCqUQ34V9bDIYqHrmm0RG7ZEcjE+JbuWM9uADRwDnvI4/troql/ZRhHYbCcHCGNb8vusAwTv6ns4ApTTBy5vuYipJELMO6/QLGfYdOYZpKi2gP7ZfG3AtKA+IJP'
        b'MTUIsQMxR3y5dyMZUNPh+/dMVAWb3nHZYIn/nkaqadhSKxZY7fWqGXy32FMmvPqwQ5PST28SlNAlrKFWYdSbCCyliITIRoQWdgMswY0CtZE324iBrYMmW20vH7P4/E3V'
        b'LdDcrHhzZebS3wgzGbN6WDvOSA9ZzYYSPhUNu1KOhRzn29IS+8KK736AR7CuCPGuCPGuCIldweGGzggm47IXT2doQkfq0e1QoMBYHJPxksOfoUa12htyftmxJ2mn9YSV'
        b'32lS4gwm9JMZgZZGROhJoQkT1DxERVhU6hD0BrFB3MkBwVhKYnxni7CzpzDkQFJTsGMoPWS9S3K7AaOqD3ia3G7ztKjg/rmrRhUIeu7vcZkRYVuIc7X16rBl2wvvfqYu'
        b'TVx0w36sf2yufIXxeS015hWOQppX0ZhXycwbR5HUXN5EVnuxyaOBuAQftM81jIbfbLA54XFnkGc24f0M97SMk2aMi0twkHl9x7GJV/VPooSaTPX5rJqujlCb213T3Ox1'
        b'ux1S+wma0bE6loFw9fkdZsOkOSiwOjIPKMg4V4fILo/o7C1wzmwXNpmrqRSG5msuji6uBsBc7wvEUhAtVzy13mqmMYqW6IFmJhA2zwb8TB2A401C6NOYvbLqwQA/Lim+'
        b'rJy88IME/zvuGJattMtO0JLKi3dCoWWjCBslIoh4pqpAmAlgTVLtyNE+tKdj0YJids+qWm+rv36FJ5aM55obCEys1f8lNjIPOujzTxwwgISuANkGElyGU8kLx4TZxSHY'
        b'u6F4+bJzF9V8eJEmJcAD4QdZ6HhwYJs6QAMcijgZ8hxc6jmUISDxD9jApaxjdJBIsP6BfN+N0m4+m1sihCwhOWgJCo0yEPa4VyzZGFRI8F/A7pfy+DvBeAMwQ0bQvtwZ'
        b'lNlzuOMaJNS4gJr6QnnWkA1qloNWqM0atOHQBq29OMi5AnJaQ/agXX0wyPv3BFFfww7vxQmcTwraEWfxa0HBrynU+gb4tp6JsiVDlI1b9JRlIOJbBfaYE/YG0JH1XgWm'
        b'O2YNNLuV+toAKTLQ+QAnTADWVk3MjhlxI/kJz2Tkj4UnTg+dPY7aZp+fWeTFeAVFIFBojK9VJSxGqFWYkzdCkj/guj1cSyB3L5w6iu5HHv0d5I+Weed38Gm0y2VS83GQ'
        b'P3/ptAPY6AR5SEC8mPZigVBaWsCXFmSerhhMvTlm9kb93mwfYZdIZyP5zDAExEXo9KehoVOHIDSBIzUPL4N4Y/lRRxJiYp0x1y8hRBa2RUPoj2wOm2iTBN4hoZcvhwTU'
        b't+hypkqpUoacIadZMxw2ySW5LCQSHabd1NuP8UQfceobZ+sbi5aXF1dauOwpUqm+Qd83v4BvRbUX/WH9Xv2QYeSEBk76Jqv2CEamxG8KZO4sRZ6fP6WACaP0vX30fRX6'
        b'xkJkhWIGnku6QtDvPV8/0EkOhCCD9JlccRAR5DfFSRU+ltRU3egxkBW1XxdAympM6Jh2SEtucJz61kV+dIqrbYs3w6HdKujr9Ru027uUH+E//3wugQhOpciCqGYOJC8Q'
        b'lxKQrzxzBraIxZ8X6kSD3JXRJRjksSpOJRl+bYpLSVmLLsXYtuoRc05rbWpabbS3a4w5LptkNAycvnwCocm3E5qM4QBXkZgPkmKSnuoPnHmy4rlF5AIclbi3iAZli/cD'
        b'Gjo34u++OC5F+09mz04nlNBCYVI7oJT5vvC/rWdij36aexjmHEU9h+/mCLUDqsKaMi0+s3xbZocK41m6x9YMISfhIYZTGjNgB/V5VhdLiiFhCM7c7hkJlWed1tt4pu6r'
        b'n0RTqfBAFDpRvYwQRwD46qAIDQRS5mtIyLlLQDagehZOZEKDl8bVo3IZJkwTSaNGGFNf/kcl5wR1ytvxHxtx41zEi+uqPz8JAWLt6hYJsrrdXo/P7Z6XMIQZp1VJGbpn'
        b'ImBnAtxSzlCyIogg4fnSHdaF79zuixJq7LREKccZ9HAt9LC0294REF/4I/Uw9A6b7Dj9IMG9pI7H2ZsYPxgm4WVK/HQwgq51O63jINN4c1ptokO2iU4x1Q6gXySZbq12'
        b'q7ZZu1r0FyDM1vYHEMgbULCv9rCkbx89q3sYiEevCQO3ig1ig7TI4mGqYsjmkzxSgxUwNyNF4nuEj7ZFNsaYA5jIYKSdGGwOGk1bLK2qpsFTGyCneMZA/UT+EQINVe4G'
        b'ZBBQq41PidjWq3N9P417RNXZfox3tKz91DljGLTWhEHqBL4zRopLwpuwrvp20YkfAz02s9Y2uLSlBTiDBiOMdAH0SgKatNGhjmFavgSGxCDJJdYIMreQ5bBADtXQA+Z3'
        b'yUQBKpDL2k4F7uZZbrNnLJUQrqSdxgOcJs1c6TFHGVALq5guLAEz3Akx13mEPbYGDC3Zdrr4TCBcsxRnWQmk3JpBMC7zR4bPoCqTTt+c58VxVmsc3zu7415tx9U6Nasd'
        b'JcNyLonv0ARkzCmSktzACdn6kSp9XfnsYagUt37W7OXxPapv0Tby3PnaPdaB+s3a+u43ak7CRiXUhISJgK4YTn5ivc3um5BpKjrwnNXc3Nja0kGaaTGWT3p87xmnVgSm'
        b'0/DMBRA/Jw6cLAyZlwKrWzzqLXhrj7PoujxVZS/VGpLi/DAb3zbgR9o3jH3QhYnejPhuPG3zTIMXbebmAVA4nkN0VL9L254w1tq97dBwub6prHiY/iCq0+qbh5VodyxD'
        b'VablDn2ntrOpk/QpziRB0Tic5RyxPXJpi/GMCAyiMA9GTy2OIBnIRWSkbyMc3Vt2C+1ceBLPiRfPngXLCGnTWFJz+1ol0vynRhKbCd2/TooriTH3ViT+JNeGWxZma9eg'
        b'3x79kI6h2PXDnH6/fo9+a6cFJpsL7NKEBaa0C2fkOguJheyLRFL9kQHio0jIBqeBREIgUbEqNsSSFbviACxYThAF2RZZ6Vyw0Vi4Yk5j7mcDqq9Wlnby1xEf9V0cagHV'
        b'w2gq/C0ikNcmm2oQoMJ8ParzAQlN7HhEngU1EmdNTQoKxhvAs7I5QKAlJIWDot+Hd5SWsqF0JL6hL4zRJQSFaShKt8B3FjMPEeKqybRsEOrg+SaeN3eJjHziUlyhxMga'
        b'gxdClNqfMcFgzOEmPq0bucgEHxExKDA8p1DGnsQFa1E9dfWr3KgjSBYDMcHnPzPuFxb4M8k0gQEQBH//kC24MNDXs0Q+n1FOnmrEuIuLeWgu2jH6xI1g5RIUH/bhlOCZ'
        b'AMthqYQDhnwQHnA21KKEwbuOcUFQ2u0fQ5wRiXgauQEhKKFEnMkSFetGHOqLTB7JLkmxwZmzir7ARUQTAltOXgMTTSWUw3MHgKjrMQ97YzynjYdWJ2sE9mR5bpC5kkiq'
        b'jFnmoZwkJk73KTGpEgNpWy6q9rZ2FqPFsQImRkMOjiI0yolIOeziKpynuXGwyHelw0nOFR9E8Tz5uCzpOMa1zb4VHjVArAh/okYF83wJRRLPs51jWkQkHXK6MHybx2C/'
        b'+CkGHWPI4OkJwIMgtOj3LI9ZmlXFoyJHz9/qDRAO3dTOZvkxCb+rY/v2SaZ1I286KnUIDl4Q0OZb/t4lOoRcNKlyYEzzH+lnJ0lbnFmIsquluPVw9YwJiYBfkGoM2SwV'
        b'4/oi7rO4m822LSjCQWVVbahpgU/pmWAIQxCHR4YiYH0emG+bu86LWg4+GjOTRTgfRxYNqtQF/wTXWATvn2mnppib1jRSdzp95xgVdXmE0KpC3foEyy24BrEfWSjIIbof'
        b'9tRu1EeGd4yrDm8DdCfC3cwAAKOgkAkHzzU8qSIA0NrNEzYHOwX2hYKcPV+q+QTzoJxRsbA7eAJjmsmZ5iskVxTcblpjpzIv9DX6mlf68uKHet6AfP+AU/Ll+X4UO8pq'
        b'IQ6Yi5Yeg2NqBdEwnIG4mVwFWmWzO+PPsWS3DxV30E0zFPACDmtmwsJKNZj1mbwspPJtOR2HN/HTTtAJx5i4SpdxiWI9Wjd4PONBLbC7ei4kMc0cw/4MoQ9+QVZxQTko'
        b'EbgvDEhMjtMAR0EdlHKrgEDfdHMrq27eWB7qxXihXUgyDCBK0eM5oJrWBC6LzeSkqsMwaWe8U+hLwqbsmu15GeR/ux3dhTESkbnJRqsT+DaqFithG9i7pEMvjjecunBZ'
        b'RwT3jBCQdqS3HL6+wRQX2KTMnqn9gCh1kVVDy/x+4mJ/O457eLa+Af0j9e0laY9ot+md0VwTD6DorXEsJIXoTRP7YK7tTdwD35yOdyBabGAdpHiCnDnGTkiN2WY11zaW'
        b'1ns9lSrivB0wjw7i/3KOsScZGeXPCAgKTxuPEYsCvSMRXyYy5WBJwdVCrDmZ2HRWtCRz2wyyUqo8lY6xafOUZo/hlB59hZ2y5vuHoUobThaJveV6P+ajXRWzVtf4Udge'
        b's5Ham1KvxqyoLt7cGohZ3E0UeYVC3sasbszhURJ1AGIS5lDru6A5cSF80b6mnIQepBGKIPNtPcxB6prBh0DNYY4TRnJgepDI2UIbubbUCG42AEIImhdwviWGmWkbD+CJ'
        b'59oAM2uwAAgX1QnX4FeyOmsBkJK3DyZOGCuLb5TUywJWRcAxh2c2xSjtbA6BHJqoLeSWu4D4lNiIz4OUgY9ZKj/sQRCttrnVq9BgV9eSS/w8HKQPdu7Af3snzy+wAzUD'
        b'w0lDFLM0NcIAq8tIplQ1j6jSmMWjqgB5vPjQeUGrD7Mbb/xej6fFgHkxKxw2VNSybjdyTMLav5NMnVXeBUdoKu1jgWwycRbQXrgtOT7++EX39hxk7YDab4MVWpWwJnlz'
        b'5NXBMAuSOQsGiY5no4U6wxaIpd4f77JFbcJ7YrOcTsi1+rAhyZYEbjDGDWlLiTeU5fhnGBXDFJV2L9Xq5d1xg9G/jgcgWbqlnTOSmrAu6WX3Q1OYUB8uTIP9KjD2K3HR'
        b'YWgMC2CC6JK6CtvSYA6O2hhv2ukmMW43AFxkKmZa4oJSG+HVMHlpCY00snVS3sX/CzgDS6cZzDR5Xjg8THcRxYh8O1sKVlojzVOttxlQQBw4U7dDcntW1XbBGwUQA3u3'
        b'T+K0OU7f3ywPUvoID7s5MmhkaKqCeAnh5aoz4Vpizz8z6VOb5HK4ejiRc2llwagP6jsXomegRVqkSt+0wohnndwgOqbrGzqdDlbjl4xE40wQ1KqWgPqMM0JQeXGRpKSG'
        b'WTgXMSyHbXUy8SftcEr0YPQqBWRBuY0dTgzmLAylN4mU6rKCtJhUOmdaaSfoF0c3kKIPcAaiQJJupAvNuYNfaFdEaJDQgpjSFkUIyCxlnBKmD/RTSXNWY2Vn5a3I959K'
        b'hoQR1BqSJjuNeY1CZ5ct1Us9MaffE3C3qM1Kay2g+k782n3R9AvmlVVVxpLwHflIBViV5HYbcZ/dbqaB7cbIISbCFjdK/7GpxLqHtq/3NNJDBRiQjNV2TTd2x2k1mO2n'
        b'esyDluQ1VfvIaSR6Q0GQEG1f2cyvyelYJPYs3ofhcfggtKVRUzq8ruzQIOR5xZ2YRBLmDnce+tEOCoyr0yCol0aAWMU7VNUGYlMEAhVO+zVMsZvuQyKg8GIvDnWI6Smc'
        b'/7tkpuFASCevXhMB9FGxrBE2pwLaKe2yBgXzHJvLXcBdzBSfkIdAKt1f4j515OfPmz7nvLwvsbtMyW+V6qlzEJ4eE1bWGMshJgMe0NIaoBGLWZTWphY/s0ZFiopkfzHL'
        b'SpTMG7w7BtdoTOkToW7Zmdsfq5vhk1EWUyWZ7ItlVK2hkyuNuE5AAibRHLCGxewzPd4VnkB9bbU6EYsg+0ichFqT34T/UhJnBeFvkHAAQN95mhdEz0k9GcZcNHYVjTHd'
        b'A0kEKLuIbyJ8wALEoSWDQ0VNdA7B0r1Z2qbIIbtiDTkY6yCUBPOdRAqdX4RQ4cKZzYWSg3b1CTNfMBlmE5kSNyn2ULKvL6UdkH5QSYK3Zt02rHt5S8e2BJ1BwEGzuEZO'
        b'fQPLVpy9uGyu5U0oyRV0Xc+rE5TkoKvRindBF6sH7vsGnXDFsq0GBIEyFVfQimUqYsgOrXCxVtCX8B4VqVmd+B4VOxRr0BJMDjoAH7A34DWpwan02ChDeQ61BXNBa2Va'
        b'd2mVH6IFxYc4B/M/xBn/IJz52nN/m/fV5FJieJwSJ06cSBMXE90APfj5jFzk82L8+THr1OZWtR6AD19WIMQsPs9K9yr2s7ogmanAO0hZ1Vvv8/gZUGqqVpfW+/yxdExU'
        b'twaaCZi5awBWNcZs+LCu2Qf4rdrc6lOYWGAtrlap1uP1xqSL5zT7Y9Ks6aXzY9JCuq+cfvH8ghS2wknMLVEBEtmbWPyB1YAfJ2ED3Ms89UuXQdGsNQ7M4PZCczzGPRC1'
        b'UIVF9UArYnINY6HYfa1NbvqCKdVKeA9PPasC9PifBlVOYqqSpAJ9Hm6gStpANiPqoouQQIl4C4wQlgw+HZldodsOIZf4dTJ9wTYdbjeZk39Acyw40lNp2yVU1CW7hc4s'
        b'leu4w0jUk0vyaKR0yhUhyqERUUAkSgrPUxuyZtYYvjCy0fqCV+Qgn8kUAyXFijAtYDH4o3KcYBaJS8q4vvZTOedXq2hInDeque6cPFTvyiNnBv7WJtUBM3yq6EyMrEuG'
        b'5Q0aXpTfCaeKK2gheCKDKFcIesFYAR1MoeCMQSVS0xhqVBf0EWLWzZZEK6h+NMDY/FHndGUE9SGKeE5Jhfn+Qto3lUBJv8cZnDk0rVFIUTsmQm9jLlrl9UCp1zZ7m1UD'
        b'mrPCTQqOJFLtJ3OioyRefTPe0sfh03qLyaBC/0Zkn4dyAAMWG8USinsjybVMUKxu5btF+dbzBshXj/FGNQlcgp/oKKmdX3A1lDPIEucXpFptUpYrYyjZ6+on5mj7/Ukt'
        b'y0VO0Hdq92v38P31vamonhZHAUhvS6ysrESFLbEVJ1zfMKFkHtoH30dWe4BP3o+vyfZ1drKAi7+lTLjMOSLQAkNXWi+8WCj6NwAal/fHZ2fP//uC9KUZP39G2THok/GS'
        b'sO7YS9fm2/Zkjbxh9u38yOdv/Trw6KadixoXNzTd/MDkQR+c2N7vm36fT/70H5Mee/HrlmPPnlj51hXWb9oGrut/t/+JKRVPHOvbI33RwMFHZ82qvzrrI9fI/RfWlH4Q'
        b'Xfho2ScvDDi8eEFk4qL+X38UqrltWOq3rdvH7XoouuZ4We4Lte8cunTIpj9PfGePL/2pwJpxBxrnfvLeqiHD/V9s/a/0p4/qz2W99UXw5ifmj/e2JaesnvXQo9ve+uvf'
        b'J6xJ+vqck58/3fvGZ4Y+Pv3ZB/Vtbz2TvfhP76a9/8m3d77/9I7tyXtLly95smdjnwEfp31q3XBiXeOTJ505k64YcmTBqbvyii5QZpX9+oIb9r30p6EfPdn6xrJ7sv9Q'
        b'9X6/F6aeFNVfX7B+y7Ho4pOvvPh5zqTQ4Kf69J78pPNGNdczYrNlXvS+Tx4cUrbDY7UsvLHHM8/wH8yu7VHxaWrFua87zi37jb2kcWD5rqs8p7Z9JYR2f/bKo6P6PXT2'
        b'd1lfTiy7Yd6WGfcP3OyZXF5tufeNd7gTz80c+Px9F31atfEXnv2PbVp+pPEe/ntlyc4bXlHmykokffurFTtWf/2q/7Ogb8WkyPhjjXe/u+2djZe9/tIjTx8rfqh1wUnP'
        b'Nc9OfW5lyseftDza89219boeyni977ohhy+astiRcu6Jux6d+dBfn7nm9b8MfeTNd0P3v/r41Id225/6uGbjpKdiP5v42Z61X5xzz45Dj4zpVXRs8cvjvh3oPZ776MnJ'
        b'xaUHF7+64uSkxpJnMvaPf7X15NxCbc/ep4sf+SQ/+tSrR47PXPT9hQ37rhmyaaK36baLL7SsWrfvSNXCb3uqf1v+tvcPJ1e8tvy2Pz7/2iMb+vxu7qhFdT/f+l7P7MvX'
        b'1o6tXtbzsScqJ/9q6YM3j/7qrUPrLt1615VnHy/43cM//O4v1z58wajaUWM/3Pv0qJPfpbkf/tjzhyfH/Mn+qfvd3q/8ZtfGb9b3ePe+r0oeG//Byid7TzrY58Yp2374'
        b'Nuf21MeTLj117bBXxMtfu6pq+bRVqz9aeXfrqeJf/u1OeVXrR1f+NTTPv9P/aOkfrgiNvPnlsX84sv6//nLdw29e/PI3z914Q0nbFY8vbnvzo4sm3nVeUeWVT54a9exX'
        b'A9/8/d82tZ7/4nlHPr6yz7N/fnbh7b9/+Qtv06jXFmW89cmV16d75+598aypP/tu7W1/qPwk9MnW5ffecf/vJ2b/4u21PSv/etHEpsJDbW+M/O2CFU9/f8WvLj/rzZuf'
        b'23HPU6vTX/r6xH3q8fAbr26av+e1tz6/+tmU44t+d2zJd1feu/r73+rj//rCwe/5gvzDjz/1dkESudTRHpihosPMYGqZtmH4zGKMK5+mXSdqD+h79DXMD+Ru/SZ9HwXn'
        b'rSwpDGl3o+n1UUHbVjaZuXc/tmQVRn0ubusQ95mCPh9sYZHmrpl7GfIlh2qHT1eC1O7TrmMBT7aU2pjcVNucY59ZXIicyxTtF6L7ivGBUQhatNu03dAEsmQ0WJx4j+Jl'
        b'bVMFfLnZlDHDeXuuQ7KOpO+0rfq149q5osvLZlcU6xsLTpNLa+ur4LMrKxycqh8J4NmiRcv0/d0qEPTUbjb0B7RDvgA6teq3Wj/oH0Zxcza3ni7+vkm7vV0EznEr9Z12'
        b'7cGAjWJN6MfG6bcGWrtl3P5cP8BizWzTT2TGwbV+vJnvrx2fCIjYTzoafvRSMPbfWNj/L5eC/uzw/k+/mFwob3O1YkQ+RDyHq5Z5WZD5n/D3vtTHZXehirPI/qfZASm2'
        b'CnxGGtynC/zQOQKfk4nC7gFFg8bnZrksWVMkQeCz+DFegR/cCrlsEgnDB6XiNY+uuf3wmmahK5SWZce7VBGvGZbT75028wn+H5CLqUwnvXfRFcoc3OxE1P0HCXJge7P6'
        b'C3xfyJlldfJOKqsv1TF4MV5zRuO1sFL9ZVxWtvZ/F303l3bcHEfrMs7EeG9fdbpfW+2I9pC+UVvPvABWzdKi2mYrt0S/zpUt9tE3aDvqd+59XvQPhhU5dMP+ki3P+F4f'
        b'kXpdWdm2E099+9mr0SOvRT/1lh/ve8r56NfzUwsK128fPeOc8LmP/+7hr3p8MvbPuze/YP0okix9/u24O7KT7aGe5aXfzVl2fv7YLZmzwgvrjj8rvFjr2pFdd+OHo5pn'
        b'f3PJiMbB3237YsT+zS/8Ou2zued/8/a+KR73/VsXnOOYteuL29YWvmT59nmp98OZg2c+8et//OX1C068UHudfeVo/cJhG/fW7Jw3Pf2+E09N3jftl0fm5OfXbN9Wl716'
        b'30s9951Q+/4wyfPSm6Xfbx3z8cG7nhly1jvDf7/3aPHrfUfN+GDFbR/846qFu+SD08995+i0lWMWvL/kuZyVd9561PG6/W8HnrjwkoEF1248ec6595+8bPyRk8rNCxsP'
        b'97m48ctonwvP/k3TjNXjs1sXTDqavnTgSd87+xYtuL7xg89+/9L9Va882zbh+an7Pg4VftSjz2/++qeNq+57av7L1vm/DwcG/vDWk2sPFG/e41k9q/Y36ccPTbjrwHvZ'
        b'X+347ap9S7cePlrytf+LS79dct/EW19Z//6Eh5ubfrntvSXjL/2oIu3UutxvfUMeOzn2gYPN9QemfvR56Nk7xr98ycO/uOWp4eXPv/H1I+6lW579+reVM38ZbHzj53dG'
        b'dxwY531r75svfttnZc0Pu07lVoWyQ3dW2GaOa/n75C+uv3ozt/BP18/gp289HHbs27N7k7xz2e6NruMwZfx1rz5lq819OzU9949ZQ8b9Kvvum/6Y2+um2qvzhy2/tvGN'
        b'tzP7f9b3s5enJLvvb5z8l7ET3jty8ImlN1z+jfWlE68+v2FhwSTCGrSt2tYJxrLaoK8vZutqgfaY6wJx5JyaAK29G/Rb9Ecxk4kIaJsbCqxcD+2EqN2orx9OKEwpnKEn'
        b'zHCMcKjfIXIShmNcpN0U6Mmhx6CNC4q0A8XaPXOA9tSv5i9L1W9nkSQjffTbiypKCvVNiNhQTMkNFfr6mvOtXP95ljTtQR/51ObtZae71NYOTxY4w6X2ddo61qVd2s3a'
        b'2grIiVF3IW+RzOnre6aMFRu1X+g3MReJ1+rbZkLLZ+obZ2k3QUtn8rDD1k0KIN9IvydTO1Khbxo6K0ngBB8/KQ2wFUQOJurbxxShr+4qC6ftqJKnCC7toES9m6RHygh9'
        b'G1rCc6Or5VXCyLSpDOf6mXbbyAp8V1BWom+sFjib9gtBC+trtP3kM0cYVA7YYXG5dgDug/xkfUs51ZZiX6Ldq68rLtLvgBfaEX6+fkg7TAEq9UPz9MPkNgqdRmn3+NFv'
        b'VHMqcw30qL6lmALzaYfb4MMQX6qtmUGN1Net0K7W11cN0/av5qHIdfyM1iaagiU5F2przobqIoC1Fc7Ut0H3ER1DRev80ZZp+sNZhIcuXbQwCRDUihJHT2movk47iPEz'
        b'c7RHJXQIuZLhoQeW61vJEReMBvrfqqicrK+1cL2WSWdpRz2sIT+r0Q7A8JeXaxuwITfxpYsX0JtVqnZHkR4Zrt2i3Y+x/vbwCyqWs/BFG3LRFzqgb/qd+n5Az67kp2gb'
        b'tLsZin1Uv0d7oKKftp3AI8xRgcwlaVcL+l3atiC5MvPpW9IAAa0qKcMpnK3t1/dauLTxonZvnb6NZmqxfqi0gkU0raqkEibrd7uuEKel6OtpYbTBsnkAfa3sv1Lm+Hmc'
        b'fod7Fgu3fEg/UsbWpbZN/7mFkzBOKdzeyZq+Rd8/T1+v7cXhDaTwnFTDa48NKaL5apqr7agoKSifbeH0q7X75XlCprZhAjWot7ZDv7pCO5BCa7msDLDVJO0mAaiGY5dR'
        b'nyovzIHpbNcIFZZLQFmsEfWryvVbqGVTqmdWlBXDwmMxVPWjRS59nVjZS9tNPbpQ37MQ31+qnbCgP2nttimjA3m417TrFrAOzYYRLyjT7tNvhbL1G0XtOAzQfcw73I6B'
        b'2jVFZdr+oQXDy4vRWxy0FTa+dpV2qD9Dpw/qx3pWFM0s0x9ZCbssh9d2AzlBM908+Gx9PW75zeIIeDWX1x6ZWkUbYpJ2aEpReat+vYXjKzj9pqGGM7oV+sP6Pfr6lrqZ'
        b'uLjQmySMR1DQb9EOwrBidVek6Edhp0Vmzyp0yJyUyms79d0+2jJnQavDFUASnT2qz2Ses+pbBFk7xLzw6/fqdwyuOGuU6RpSXzOPeYdsmcuos6vhBb5nDgF96YZrxjna'
        b'UVp92QD6ohXkRdjck2O09S5tlzhVO1wbYH4Fm7WIvl6wzOzktbMojaCbdmi89iC5y2zPUq7dabjL1Pbp9wTQ+hxonBMtCE1K9Mg0/fbhhTBJsFG3AAiZRaOyoaJE2ycB'
        b'JXevVb96pYP25NS2wiSkO+nDirISLdwqcBn6LaJ+t3azflsgH/KsHqrdmaRvGl5SXtlKMksYSkA0cNGVTD57sVwGcPVWGg6/tq63vn6ctgc3+MzZw3joyO2C/pC+NsT8'
        b'w+4pWqavn96GYwHHBW7EI4J+ZLR2H6NloyHtaJG+aZa+uaK4oKQcPrzLwqX3FfUbYeBp9TVoaxZU4E6F4YiWFZcPh2q0nbNlrpiz6DuWncdIOuztHcbZtbGqAEg7baO2'
        b'WR1k5TLzJZFgAw69OAIW7/qzYPFEq6roaLFCi+7HbbR1OBv667WIE9YGtGmFvkk7DtTsZoDYs6xctn5EWhjQf079Vqa7oVH6YSynquSyRgEocDgBd1v1dSzY6FY9OphG'
        b'GPb6VUVWTirhAQrfexlVomjrR2Bjh9NB14yjh2cdHre9B0namotLGGgM57ZVlM0unG2FQ0vfJ0uCbcFyttsOX2iBR9u1a4zelsDI6nfBCqrQHjojFSfTPe/Y/wBC6j/u'
        b'EpcHE1G3Dy5ckiDY+NP/HEKqRSKZRhYQRQIvs/+CxGNuF8tjSDoYqedgKoCCw7iDEgCxt1HZGWTr2/7npJIpD7xxktWvjYSRTkEWV13Jdf7Lk3nG3WZ6C6jJ4fcEWlvc'
        b'7nb3dKaIQOMTe4o3jOD4W6I7TXrXQVEhGf6jFw9UE/A/AdcaTuEb4C96UeQiVCGLDoFfAX4F+BXhNxN+Jfi9MHJRPQe/jshFaP8W7Yf5GzAnH+bDF5lKbyEOFd68YpMU'
        b'TWmyhPgmOSQ0WUMo/rMqdq+tyR6S6N7hdTQlhSx0n+R1NiWHZLp3el1NKSErChcDqVB6T/jtAb/p8JsGv33hNx1+0TJXht/+QS6SAr8pQfKAE00KoqdwPpoK+TLgNw1+'
        b'e8KvC34z4TcfNbHh1xqUogMUa7SXIkazlORotuKK9lZSorlKarSP0iNkU9JCdiU9mhMUFS6Sjdre0YFKRrRA6RkdpmRGq5Re0dlKVnSOkh2doeREy5Te0UIlN1qs9IkW'
        b'KX2jQ5V+0VIlL3qW0j96rjIgOkkZGJ2sDIqOU/Kjo5XB0bOVIdGJytDoFKUgOkYpjE5QiqJjleLoeKUkeo4yLDpKGR4dqYyIVigjo8OVs6LlyqjoPGV0dKZydnS6MiZ6'
        b'njI2WqKMi85VzoleoJwbrYw41nDRQcr46PmBXnDXQ5kQnaVMjE5VJkXnK5OjIxQ+Oi1ohTd5ESFoC9rrcJQywq5wr3C/8Ow6SZminAfz5wg6ok5STWn3neoKp4QzwpmQ'
        b'MyucHc4J9w73hW/6h4eEh4WHh0eEzwtPD5eGZ4bLwxXheeH54QthPfRXzo+XZ4u4IrZIwRohag+zEOGsXCeVnBruEU4L9zRK7wNlDwjnhweHC8KF4eLwWeFR4dHhs8Nj'
        b'wmPD48JA6obHhyeEJ4YnhSeHp4TPD0+DmsvCs8JVUOcwZWq8TgvUaaE6ZaiP1YTlDw4XwRczwmV1Scq0eO7ksEge6JMhX1o43WhNXngQtGQItGQq1FAZnlOXrkw3vwkl'
        b'RVzBJKphMH2bBLUk03hmwQjlwtcD6fuh8H1RuCQ8EtpbSuXMDV9Ql62UxmsXoa0ilSRd4cB5DDkj+RFnpDDiDDojZWuENag+gE+K6Ukxe3KFM5hEikAzmIt70uZnKvkI'
        b'JbpXP8OTmdkIRbhGu5oTQD8YXANvKm8b9rSneub7hxbk1TON0Oq8mtZ6b6DeVyCorQh9SC6H53e3XpzcdT7ir6GWWdRiGLNyJCBWnzDtUAokAHRLPYE6FW0fbJ5VtaQa'
        b'QwbXKPZuros5TfUgUgvi0R9HE0BGuHOg8+emFtXj90NK9DYvRYtcVCBTf8sxZ0fch6TXge36EEWEH6Jx2IecqQvdrHgAvpJbBNQgj4ktzS0xB5SueOqq0TbBVudm8lRm'
        b'/tfuNiEOk2NyHZUTS6ptdlerSykYJMawdDeubPZ5V8cfOeCRjxUWc8K9P1Bt+J20QarOW73UH7PCHRVmpxufP+Cnt6T3TjWsqFbbE6heiyn6jm5c9FT1k1KDr5nK8cIE'
        b'VtewD1SPZwX6+MYE6ixQwlLr9VSrMdlbDRM8MibW1C8lnXF00cICQMQcGCqY3TM1nieNSQ6o1bUejCvodkP2GjebSCvcoRJCTHKrnrqYy63U+6trvB53bXXtMqYRDAtD'
        b'YT7EEG09JQwt6BTlDRcIIv3MX5PA4sugUhR6O0L3pCjin4bCdIHsPoU1QCYvzwmamvBdqwD+U+9FuDjfjWuTGdiAky3aDm1EtTHZbOMJeBuxAqRzwsbKxpYEeYBBQh1a'
        b'SvRVKKIL2U+IkTxS5ZKCUsTRaFOviThDlqAQSWoU1JlwL/uGUopTL404k7iQJcIx1a+II5IGb1zQd2cvHAs5YoV0nzVCUI70hBoF351BQd0Cz/pGMuvQr8s2VOGCetKh'
        b'ngOUOwu+zsXSfKvgeb9ID8r3fqQHwB0rGZhlhWyQ0xrJgJwSnBUw1mvQjuWJoAQnCE/lyY2261GNV4av7FRub8hl+oFxQAnGl0E73DnwjqLfQHoex/of4amMK+DblEhy'
        b'kmniJkZS6W1yFrqsBbpQ4YJJ+C4oALzFOHaUk5xs2plP/LhqHI0nlHkrzIMjkgO1CzguQUsG2p5ksXGA9w9Si3uZIxHs4IuhwPl/KAD5f8+P/kksa1zVn7Zr/rgYtkr4'
        b'Kmr9yIKNdHvS4C9VZAF5mLYPC8cjA36bxUuiS3ABrpuL34kOCt7jEjpslh7G+UObBWPs0mZxwVQXGJslI3GzwFsRJy8iwRk1osP2wckrgm8kusOFbwlK/j9TnHQ5gn+Z'
        b'MOkiatkFreo1QSsZ0tiCUBtbPLBdciZwPiXSOzIwMhg2QXadBZ0TwfKdE3JEUEPNAaUmBR2R3rApT8LCS0nisvFgFuHehfdBJ207KCeYBChiirGASW+PvQs6KMyULzIo'
        b'khzprfCRgfB/MPzvFxlax0d6YD2Rfri5MgDFhOc5ET6SGklF1KzeSpvbgosYNlOPoA16kwwLHn6DsDUiriwu5IqkAUKAT1y9ONg2yYQoJMFXxRSYKkAlwH0d9HgTH7L4'
        b'PoEncqQQykwJpkSy6D0ABGhtSiSPUnlGahClBhmpfErlG6m+lOprpHLMdlKqN6V6G6mBlBpopAZTarCRyqVUrpEaQKkBRqoPpfoYqf6U6m+k+sXHDVPZlMrGVF0KHA4l'
        b'iN4HuU0INhEIQF8jQyLJ0OPUYOr1gv/uoERXK15prfTCtQJlwNjXocdroze9ODTxg/FMxzUGpYrknkDCkUfgTc+LghI+D0pmxIp2b9Y9/q/s24Jh/wGw438ePg2GU9Z/'
        b'Uzt8Qh1DwWZ4cZZFF0GqNIksivHvW8mGb9FVKPpeSJMFDp62/xcELs24d3wjOdECGT1SOYU00QFwzMV3+/e5lOYUU/k00YYi1u8li1NEWr8DpDNttQjSMQeNAMuAjI7Y'
        b'DEgnR7gESCdGLHS8AwITsQMBABCOaXInuufoGmv5N/japwHeKpt2+myARRyQTp2ym53ag52SYMsgLiIAgE5jHVlDapuAF1igk6nokZKeS0HKCV1Mjsh4VsNQpADISkYA'
        b'jilUUY84Ng/msdSkSBpuSRwsAmeiBcBtxD4WUMIJCcrpAPoAiAKYx42J96nwBSlaY7wc+pY7gwFM/59dyXfIhhtFjtYwWipJVgefK6KFTo6Iq8nRcTU5EgdeQSQTEMJI'
        b'CiLA8YGXjIEfSgPfE9Ay0V9MbzCdiWlyAD8NVpgTzXXpnWNzDg0dmrJbs8hKAFMdBhmQuog1G81SJThRLg2K/nUmqs1j6RIgjnj+WtRXMQwiQlM4uSxwysAkhqxtDmQ6'
        b'kKVdhsQFuEaH+mvmyIWFcaRvsrCE5VuJCHeFU4EAzwj3qrMa4VpsCbXYELpDOzIjyfjM/Jqde4BN2GFXsXZa8Bov3Y4sD/pyDnwJz+CNPf5lvA2AoA6K27x0aVgT9x4b'
        b'jx+I1Ah0GAaYIhygeweMMINeFZuLETM1bPRN900FYkwI1KivIA35Nv+TvWrEXPV+d3NNnXuligrV6n/JcasXyfA6SOusgCcy/V+KZ5H9nwT6ddkwZTI3TCpcnXQIoLI5'
        b'ulWU0ZONgEeBQ3RQ9A8XL9udYpYVn6ZZXQbzNo0vyGKcB/RGxGJBiP7VfvVX+OxJvDyFl6eZxjP6kvGrz5B6f5u3vgZXLtqtVgeWqb8hO2m48VRjnAH1WTJZqVfUQVQo'
        b'UOUxsboG6Pll1X60po5ZDR9JMavfvFnqba6p9voLkv89Q1aw4D+A+/6/l39FXIFrsg1JsBiuc0GQThdVuCxZJFJA8UFnUQb7k7r4c3b59F//k43/8bTsFNOskjjrbNx7'
        b'dQ14zXNK4ohcvJswFfelYJOJeBQE6mclmsM8wFGMAXciZ8/tNnZkU3ULbMuAqkZ4ZmtLXgOYbOQJ2nfTV9V6WtCLsIoSOZSU1Fa3+j1udyzD7fa3thBHENlnaGwCT5Pc'
        b'7Qn1k47OHxKMUic0NSutXg86v2OxVyUALKkCIENdyWtWG08HCOTh1VQI/G/b1awW'
    ))))
