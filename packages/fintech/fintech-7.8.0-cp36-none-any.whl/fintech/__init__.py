
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
        b'eJzcvXlAk0f+B/xcOQjhEBE5FKOiEiCAoqh435xB8UI8SCAJBDBADgQNiqICcoj3fR9FRQXv2zrTw1q7Pbe1bNu13W5rrT22u9vddbvbd2aeJCSAV999f3+8Ig/J88zM'
        b'M8f3+/ke852ZP1FO/7zR73j0a6pAFw2VQWncM2gNl8doWS2npSuZSjpDkENlCDUCjXA1pRZpRBox+isu8zSLzOJKqpKmqbmUYSxHad3yJcZSmsqQ0NTSfho3rSTTXSNB'
        b'Vyn57EGunlrJKnouNY/SuGncMiTzJemUgUlH32ZSbqvl0se9JLNytbLpZebcQoNsqt5g1mbnyorU2fnqHK3kGxGq5DdifMF1b6Mjs2lbO1j0K7H9NUWgSxWlozW0hlkt'
        b'LqerqUqqnFkqtNKV1EzKylRSNLWcXo7fi7675cpZZba9Q/ArhqPf7rggjnTKTEreR9lG/RU/nlWAX3/fIIj8A436brxK+kPueOprPu+P4zrVhxQTjevDVFFVrI511Il+'
        b'ap1ynOtkL9C1TpzSokCfxxT0m6mAW2HjLFgdMQdWw9qoGfGz4sNgPayTwxpYB1ZOZqnJs4XwdGi0fv3DVawpHGUz+Hh9q3ro5qkq0D1S3f4qYmOYOl79SHU3yzc7V1fA'
        b'nFkVMOJ9etV40ZzSv8gZc1+UwydI4I5KlcLWcFxsikURBtdFMVQfcJaDp5fBGnNvlGqkpwjUgvVwfRKs6wHXp4B6sF5EefqwwXnw1DFKzrYxoXIj7hr+4oYuj71H64yF'
        b'S7UGmY4f8bFtnmqTSWs0Z2ZZ9AVmvYHBLRfifgiQ0p60UWrPisrjdBZDdpsoM9NoMWRmtrlnZmYXaNUGS1Fmppx1ehO+yGmjB/7sji+4kEBcsCcu+IE3I6QZWkiulkHo'
        b'DqwHe+GWpIhIpSIM1IC9mtT2TmWpiBgBPAY2wE0FuB4f6m7TjwZtd6eKXqb/nT5NtZAihHKLskz8WPTAm1KtzPos4NxkG6HcH0eefj0/z83CNgkomWpZ3eg+fBbBEjZ3'
        b'Cos/qZIfuAXwN+8MFE3/ifWnUMpkVkRTlihcv11otNe7g6YIVCP0aWZ0Gj/8oZGKUFgdFZaQQlML5ovhldRkK9wkpy0y3Fp2hTtqUFI/cE0hCYXrwGnQxFGB4DoHdsIb'
        b'8KYFj+KQ5Aw8ilGowfivCFyZR7mnMnAjWAUOWYJRCn2kyjHO7YOsAKeDYS3cLWct/riGzaAObkpSyBNTBJRwJgMP9/eDW8B+8g5YMQBsTiJdmpCgYMBLcBflDrYzsCkO'
        b'VJN3lI2ZAmtT4brElEhYA7Zak8EJjvIBlSysAKf80TsCUKJhE3slJUQkKAhNCihPuI5Vg+vKeXpLT/Q0DV6JwI8FFAf3gyMcDfaBKrid9AQ4IoXbeFpOSYD1i8EJeQIq'
        b'H25iwRVwAJ5EHRaE4TEE7kwaEoNSJMEG2ApOpaLSvPqyowIWoxS4CqN8pDhBQgpsiBmOn3rCU+zgTHBKzlj64ZYehEdAg3s8Gqci1Dt1LNifhFpM+cLdLDwKToEzlgEo'
        b'mWcZbHGHDVGKRKUFJ0uA52FNajJOOWy+EDaB0wnTNKjVvXCR+5YugrURStiQEBEphJfBGdR3Zxl4Fq7qThJkw5u+4bAhGQ1QhHwpOKZIFFDdg1m4CTamW0Jw61fBRlCb'
        b'lKpICEdDUDMTrEmISIyKjE8RUhGUAO4AG+EFUlKsP6jB1QlHzyJpWAW2UO7wIAMvjoM7CJ+MgNczk0gK3ANLPKeHJiFoaIB1iCSnK4TUJE4IK0Yv4ruiPjUFJUXNmhEa'
        b'nwwblMmps8HhKThZRJxgCqiOc6Ae44zE2wmkV9EIRtkqrkpQJawSVYmr3KokVe5V0iqPKs8qryrvqm5VPlXdq3yrelT5VfWs8q8KqAqsCqrqVdW7KriqT5Wsqm9Vv6r+'
        b'VSFVA6oGVg2qCq2SV4VVhVdFVCmqIquiqqKrBlcNqYqpGlo1rCpWN9wG1VQ1h6CaRlBNEaimCVQjsO5KfHjZMMUVqiuUpMvT8vpjNEF8cxUjSmc4mQB3WfqghOGzELRg'
        b'/lMq5ApQDdaD1XCLiPJRseCUATQRyoaNPcDeBLAP1iLKZClmBT0eHoLVNqpfWxoOjkXEW+FBRPlgNQ0rYXN/ix8e90ZwaGj4LJ1cAasRqQrBcSZ8uBt5lBIwFo9NRGQB'
        b'uEFTXAINrsNVEv5tO9MnJsGa5MgxoAY9cqPBEXgYriTkDy5lwf0Id+IRWJwBG1mKi6fB2QSwytID8yfcRw+Ha8Ij5QzFgAt0BrwKd5Myabh9RJI7ynQcsa+QEhYwoWA1'
        b'WMOXeS0eNCbBdRAhjNQbvbE/DU7CQ+AYyQn2g2Z4MDCcEB2Nim2gk0NhLWlEGVjrkQQvpREqi6ApYSzTc1owgSNQNQWsDwc34JVEWJeUiho/nvEEF7UkX0kxaIK1KiUq'
        b'MVSBspUygyeAnRZf0sApcBtomYr4PxQ1wkCPzS4hD3KCeoJKuAq1PRHXYjs9dUg2j20nBAiKj8HLhC/kmIXF4CYDqsBF1AQyDFcG58ADCMJrU5C6wljpcYjbW8gjd9AA'
        b'zoJrvuAEXIefgbP0rFSKtCAK7AF7kqLASsz5sI6jhIGMBBwKJvngqaIYhLioFfHgJMpXTk/tA86TRwvhKnANbmAQnEbimq6jp8HNQ0lVo8r7ISDBpYVHJqBuUQoosNqt'
        b'Zy43BB4ZwXfb6eKSGQlJ4VhWJGJacxMyYMviBdmMjei5TsoOUnWqaIeyw1Qj9aacRRzEEA5iCQcxy9knKTtMJw5ilfrYi2qBaQy6IQ7/ssedWx6UTMqMb/r9K//q9fJL'
        b'CR/9CO99UblAHCoBaw9ebMrVw7WLPzzW/P3Wbauv/fHXIABGe9319Qz7YrFcZMaiZXpEOi++ECDJy2hYn8DLML8BHGvRmjETwsPZ8HRnGTcdbmeDYSNnluM0RxHiHies'
        b'GpGCAK/GnhKuBBdFSDXawMEN8Dg8YcYCB14ahIYWJU5FpIk+rRfBfUWUBDaiIYY34XlSM7gHrPWxJUqORHoHfisLt4ObbN8JSjNmjjGgFR4KV8QjuYYk1WkBJYbnGLBa'
        b'lWMeQKgcIL2E1MmO/4pEvvYDwlb0FaTCk/CsTXnqoB6Ru0Q5auMWq035jEM7Wi6m+R9PWkIbu9nTyrk2VmMyt7EmY7YRJzRiAJQzThoXY/TBn7vbSyaZVzgKrnRRuwhz'
        b'nxKWY66ADemjhBQXgRgfXIWnulatI3lqY3TM/06xRrS26OotzoSV3iFbD36LlOIHqttZj1Tx2Xk6DXemMmBE/7D3qbj3uaMRbyPlGOM92IKg61pSRCgCwSQaMfuJRQam'
        b'DF6E5wgtZcJ9CMu2hHShMgX3hWv5vmS6HgiLWV/Qrv+uoMTetNGXatd/2cKsvCf0PW3s4eh2nKUaF4NNPqqCeuzZseMng+vgbDhRpFiwBWGukQY3Q0SOjqdtvzPtlbHi'
        b'DtXJaSVfFdvb3Fzr72kozCzM0llM2WqzvtBQhzMT4GAsA9G1B6zVIowk/cIVpCaGK5RKrM8i5YGlwsFZAdw5AZx5Rh1WP6MObvYKaBudXo/RD2wH12UIFfn3JoAbPQRI'
        b'A6xkkeS7Ets1yQ3BJEdjokP2HPecZLfamezoLslO0J7ADqh9HO8jgFrFOd73QpCK3+fdFZmLNvyDMiWiG/v6TL5WduLLh6pHqgeqh9lSnUodqr79VdgZlaZJi359HqpO'
        b'qXN1zdomdW6WNKdagyR8xtq4teK1o4+KZaO2r4zxoICPR3bTBTlNoK6HF7xmAifjlcgSIYOZDJCS0w02sqAFboTn0UARCuU6IlAH6hdkZqsLePKX8uTvxyAE8kZItDTQ'
        b'lKvXmTO1RmOhMXJ0QSFKaRobSTLYwYlTG3NMbcL8JfivE5N0sgsZIwZWY6CDXbDg2+rELo98nNkF66UWZErsQyo2rE4OR8ocsYaRgXTWazpqcU0qUiTk4ALcBGpFaSMp'
        b'sG6cG7wIdoFt+syEnzkTFh79rRn5Obk5BTnKbKU6WZ33eZP2geq4+gEyySW6+1O1dylK2yo8PfkvdtJ+rh5zd+oVZ9jo4S00BrXDBm8HP6VHnC1lnG+zU2d879IZWLU1'
        b'w82gGnfGEXjFuUMYKghc4ZBOcg5Wdc1OnZw1L8BIhI87ETannKX/6N2faROu2J/HvJ+EujTtTnVOvJrbWCeXxXbfrvleJdbdL6CpnL8Ld3+TIecISCPuRziEJa8yQqHk'
        b'Abrv6G7gHAsa4OGZZuw2kXjHgFpkGiLhiozs0ERFJGhIRc1eH54AToby0jo9U6wbDGvM+PV+4CUkGog0tyUKW2FLFgi3cMicrvLipfYGWGFT+uWJycqUiXBTIrKPiJZA'
        b'hfQX9EZJW50JwWnIPSyG7Fy13qDVZGpLs52ZpY+Q5n+MvdqHvo1FqZyGnrYPeG/HgOPUe50G/Eup84D3R/dSkYpxMZzYxPGIv+uSUtCQI4YvmyukBixFSsa5+Y5hso93'
        b'Tyc4I3bcc8OnznnUOduv66iLlQW40eahbmLN1KbegvF3lu8yfbxgUU5seEJPjiJWRZAOabmKBMSU5ylk4x4cAVpocD4PNhEfTr+ov3ptnja0DzP9Pv1f/yGWX3nfS7gB'
        b'0Ri338OjSJ25020mf3Pwou5UCKVyl1Cq0S1xaZS+9MQ82lSKnszP9U9Sa9RN2iZtc+4DVZG6+mST9iHi64cqgy4sra74hPpOVrw6T7d63WDm1X5hE/O2VzzU5O3I98/f'
        b'/urKuJVDK8XbleoS6r01us+la6w94oYlT1GMH3nU108kLHhYMaT5Z+n55DUzZH//XDqs7pZ0t4L6cnLfbe/9goCXKCI1WcjuuN4jiQwNdkaIQSNTCC75d40cz8QTLldt'
        b'yiU0JeNpapAYAbD9h6iEiCqk5BPSTIKdICbAFWK6fj/NJyNkhzMfdSK7T1xwBmsw6blLkXmDdMPBiBu5HsgM7cM+xelKd3C6Ms+PLbjJ0k5UJlWSasD9YDfcjD1F+4qR'
        b'CUVFrQCHCV1EmFCHU1RoTKKqIGq4nieWCTNYQrAfUaqIZmkoZcSQ3NWljc7Uz8i7xprWoi+fL92ouDvYE0R7T353x/k9r8ib3hCMSIxsZOJ29ohvmNztE9nILUG1M7Nr'
        b'c2vnPnqwQjlFwg58dOkLi/q1C9V1PzVaPomcPOrVVUE+qz7e4d+cNqB2p5vgxMdf/Xxa0DPu/MMzs67C/xbl+n228NP/hF9/fPcfF+dU3e8eUzNiYIifDrbNv79v3Ot/'
        b'6Uv/w0PuTpy/YCM8HAFql6XYbSYXi2k02GLG3p15YF1PU4RcDtclhykSiIM4CNxEQiBsvgDcBAdBhRkjCzgagrrvrBKcNPNCQl5EecAKdigLVhLtIQlZxmc66MpwK9xM'
        b'9GV4KcKMpbMF7ASnwyORnV0TAfdkIJMdNDAKaT8eTrfncF2YZdgk24LyYbMsyGDGcm2BHim9iYq54CKsTkhG1q87aGXgHtgEDxGHNli7HL0GbA6MTIgIk0fC9Ug7pSh/'
        b'GbcInIgiciNHylc2VQ3245fx8E7MugsDwHlisoE1InC93TyAtZHgBFM2ADaYic9iniBcqSiBWxJQ5zGUVMyK4eZhLqr8U0w1YZElq0DP434Iz6NxDDLUfAjy+9IcuvLG'
        b'mwR9kiBeldJGmROf9nDl0y5UgXYzAue77MSib7jYb7ipyeCaN7w4Ojw0BZk8NclC1NoWBlT07pMttLEWNgg97awVyWIl3koHUOXCapFVWE1VMuUiq8ikLPO0snmUVVhJ'
        b'l4vnUgZfjjLT+RLjCJrCP/Mog186UnytYpzTKsRljKY0NM7bSBs5q6AoQ0+VC0oPWgV5iNMnUwu3LmDK3col+C1Wt0rGqCPv49CnU1ZhHlKhy4WlOvSJI6l9y92rWZTS'
        b'3croWKukgaap4s2oHpNJLimqpbTajdROWBpSLakW48+VNMkpJjnFTjl/N5eySo0/VUv5HPb6TqeKdXOpRsYQQkp1r2RQ3SOq6WoqX4g/odoINEwlzadupA2/kHS0Wahj'
        b'SNo51e62tHOqGVy2I+V7JKWQpLJWC2yp0CeXVM0aNk+k4TSC1cg6nEzhFpR7aIR5IqtHnhhP9uEpwHIPqwfK26Jxs3r4UeUeVaIqd6SzsRoJyie2sjhfuSfqAc9KWiPO'
        b'x2/8zOqpcUcj42no57jPofu/aKT4jfiOH37KaTzKPa1MI2OciupLk/oyxhCNpxXl6IkwWsegdF4GmZW2MvksejZa44U/2+6LNd5W/lM/p/wqTTc+vyMNfpuX1UvjMxz/'
        b'9UBpGqye5Oql6W71tHrg8vAzg6fVCz8p2m71wN/N/Bh7o1Z4o1b4olYwxsdWb9w6TSDqU8Z4h/+G8nyJPiF61ASR+1/w3/B91Mpump7oO6XxX8MEUNZupP7e6O0B1R74'
        b'DXkSq7e9Dla2kTXKzLTVq5JeRRvEZnf+k83f3Es567GoAJnTBsXgx0yEzCEAGZsQJNYxcVAi1looKaetdB61gSnmsCplUyLbxJmZBvVibWamnGljIqPbaHMHs/mxZHSB'
        b'3mTOLlxcNPaflM1uFlJLe2XnarPzkUXVbnS1J3zMygqNj+mIb2hSQqFOZi4r0soGmFwqKbBzv8xeST88TWvFEpoxcdWowpW0S4XtLpIQIiZLnoKHRuxW+KW9vkYseh97'
        b'qWUl6gKLVoZqFDrAJCfy9rG/SVts0RqytTK9WbtYNkCPHw8aYBr0uBu5gT86bnHk2t0ppT33YzfZYovJLMvSyh57afXmXK0RtRh1BLp+g4HyMT3oMd3vsdsA0/zIyMiF'
        b'6C5WLR53i5DlFJrtPRSHflELh+I2DONb2/5Z2ibQGzTa0jbJHNyMKdi8Q7dQXUxtXHZhUVkbl68tQ7Yuqk+hRtvmllVm1qqNRjV6kFeoN7QJjaaiAr25jTNqi4xGrMK3'
        b'uc1CLyYlyX3a3LILDWZsRBjbWFRSG4eJo01IOs3UJsB1NLWJTZYs/pOAPMA39GZ1VoG2jda3sehRm9DEJ6Dz28R6U6bZUoQecmaT2djGleAru9iUg7LjarQJii2FZq3c'
        b'o0sd9EUuSEbFOwSi2E6gb1G2yAaKwcKPo7FY9KSFLBaGvFj0samxnrQfIyHfscAkwpLxQ98CkVLrR3sLfYk4FaPP2APqSXszOL+U5PdksFD1ZHAudIfxJOX5071QWX5Y'
        b'5DJkIhGJw5uzkFIOakbHp8AGZUSiiPLMZEcmwmaHK13szBwP0QWJMKb0MyuVRxGh9B4SYWw5Z2VNvYo9zUiNxb96JPZ2s+UCq8DKWNnRiI2MaUgw0vlC9BeJjwAqj0GQ'
        b'yQaQaA0kmjgkDjgsQEw6K5dDl3Ol6VYOlT4diWAWixckEvdWE9GL8uMSBRoOlcLib+gvx8d9FBfwIsd4XMMVNWuw2BZYReRtQv75XAqJG1IDUhIzmv/O2b5zo6liTyQY'
        b'GWLiCZSIq6fhUSRDmYAv0xyf8D25wDgKDzBr0prbWLVG0ya0FGnUZq0RzwvIxW0iTHuL1UVtYo1Wp7YUmBHJ4lsafbbZONVeYJtYW1qkzTZrNUbs/DJOwZmFz6AyJ48m'
        b'DkrQZNrLDUbAZhpIiIxD5ICJzJsnBExqhLyktD/jjb57I4Ig7pIZ4BBs5ee+OV0CqInCk3Up2OFPU+HgogBujXVzsUTwizENkRd1mgal8ESozt1u5lhpuwfQ2TIS28lK'
        b'gy7VeJDpGiTz86gib0RkKJNxKCILD3SHxpK0knZHJg+RVSQMCOEzW+2OP9fgUBYOVQK/WoKqItWJHW5JNyuDyaejNYXRFjv+iUfzEa4AZ8VKA1XWVLoIvZa1UjblSVnO'
        b'oCJYXLFKOp8yxuJPVlSNctbgSyonRHQdjz+hO8x0pAKSO/7VWKlB9K9D3zGtE7XLfy5VOtGKy40rZ62kVJR2XbUQ0SiL3s8ZpPgzuk++WTljERY+iHtQOVaOlFE0F0c4'
        b'RSL1kzMLdAxSQT+jkWJJU0s9UUcJsGAmEU3op1ywXMBHNCHOQB3XQNs85Ii8sG7cJipRG4lPks1BJIxA1Ji/xBiHSWsST4TtbshkfCE0u5DQvNZolIufGxTbyVWaSeCw'
        b'CL14sWmCg1gRiTIMJlEpxj+GQd/9GUKsjBQRsT8i1UB6abQ6O1tbZDa1i3qNNrvQqDa7ulzbX4CE1nz8atwOu5eR3MCkIHf/rfDOtolwtyGu5Ytc4Giem6NCI2j7pBLL'
        b'o30wQt7AgKWBT26DXavIwMVp8WfJb5I9GY7qiGwvG0bb3AYUK+tvIZ6ZlXA9OJGUrFQq3MDuULmQco9k4GF4OtvFn+lm+2vCgKelMpDSl8FsFvGuDMTvYp2AZ7ZKOoMl'
        b'90lkmQ0N3BArshqOPOWqKI7KEPDY2tbNFk03VV+gTS5Ua7TGrudvYymK984JSLyFUCd08Db3YlMOnac4REoS3gB3wd1BjoiRc6WwATaylCc4znrDq7DGMhiliRgENuF5'
        b'IRLM5ggumY6sfd75AFdhL14ast9DRXAzOJtHguGmFoINfK7QULguKl4B14Fjs0ITU5DZHhkDmhIUiSk0ZfByGwNrPC2h/KisBRdmKuaANdp4WCdPTElGObBTITUZx08N'
        b'BVuFIb3hEf1+8x3KhBXr7n8Y/63qjawmbZP6dlayukAXsVWuTlQfV3vn5OoKsh6pwj6kftox4VHgWs8PCy70C5LtO3LVb+0EaUQm+OTWO7c+ubv51fduvXfX/+7LOzyp'
        b'e2U+E67FywVm7Bv1XAibYG0SiWPigkGNFw0OwktTiBsibQSoBHVwX3gnN4QenuFdNEfBZTd4FtaVwM0KHP5VbPPAB1o4sLYnPEy8JnCX75DwSAXqmQOgiaGE4DATDTaC'
        b'zcR/0x2cAzeTIhNTIhJAPfHzgF2BuLcF1IBpgoxEuNruLH5+aemRbdQiCZ25uFBjKdASJwW2TKgV6CeHuCMYXt+S0kv7dKLRSJfcjmkdk7ZAh64YDtr9FoIncyhj1OPP'
        b'efZaGXMxSWIWxb4IqgL97PVzcmQ8syZd885YO+84i2YaMaXEwUOC5+chAeWkCzp4yFNJorIK/ZLaY64w+4CD+YSDBsOTJDpQ5aZ+Gv8Q3kmBTYR9esLtFjy7kZw+qxP3'
        b'GOFmOwO1c88Ay5NnZDUdZoXbaF3H+Vjx6AL14iyNeuwyPAS4FMscdBkAzsLtJlxZeBOcIBUucgmEgxuTwMn4FNDg8EHCLShP+3QbO8THBDal+cCTFGiGa7uBihVZBHLA'
        b'6olTbAEfdbA2gnfRpSV4prGDQQ3c4miNgHKaeSVQyKs6DB5QBxSy1dhZxKFhZMkwcmQY2eVcV9MVuGj3rqBwJGbH0/PA1SQ8jxLJz5POjA/HUU+zEQMrwGGFHDYkJ8x2'
        b'jJqAAvu1EnijZAlxLL8ZQ7zNsuipv8zS6YIoCw6HyIebc1xK5INCYbVtkhvsnYWBbfEKN/9BaNyxnzwFtoLDiJ7qUF+nzAiFNXN5ACzMmeF49WwEtbBVBE+ngg36DOsf'
        b'OVM+HrctWSfM36juZD1QvaGL9JGrMSBiEIwwPlRttL6VdSfrd1kJ6o2a21kntQ/Gf/H7aGr2KHp2TOWsqpgv5S3Rm1u0ph5HoodUyKavPVI5ZTcdEvRG4+u+9AefYqh8'
        b'HYHkxwz1+zn+tx8sl4uItzVtFHypPXTH5oYOm807ogO8zXzAZX+4D0NhRxyE2weAtXAD2ErczOBmfD8XtEPF+c+1gZ0erCfvA8fDZgXYHLx4QoV3I3vAM6w/vAZW8qFC'
        b'p8AJWIdNO36eL04WHonku89yFtaFgFYyMSOEjcvsKVIT6BkCyn04gwyAxskk7CfEZ6ltvhysAwfsARD8hPnECS8Ou554GjyzyIjMa2zoENwNtOPuCkrMEKuXQ3asD7Zd'
        b'kXGydFhnzNOWarNtiNeuPbmWzHO5gFfL2rXXZ0372GaHPBwZCCwvRpc1tF1EVJCf/zgDswXrwnAPWBdscoDaC2IEnrXZOBK2CqbAy+PB+QHgmBwxwNF+cItvXgZoLsDV'
        b'GxIWwP3NZ7venfp80E/MhcGm6IM0mSM0SbfTLSLEcQGGst/nK2PEFLmtZX/y2uxFh/5IrYjoNuVjax2lP/fuFM50CD2b8eO9HnWjPMF46eTFPwz8d0LtZEiPEC65Tx1u'
        b'6XfOHPJnQ2X/k/oRMS+nKge/d3fXu7kRPwrWrKpb9a22/8A1MeLl0+HS8488395b1Xvo2E++6jHMbcuEQ7LAXXteGxI7/fj0VXLJx8Yv3y1dumaJ+tKkf5Q/euf9L0YW'
        b'fZI9Kd909s+7w+dkTBe9tWpcgWHXULExjv46Zmjh9fenj0kdnh4v/rw0+e1xD+Mi/PJq5VKiY6TAPfEdI5RksAlPuhgnECpF96p8sQqiBvUdJkPOwI1EDZk0HB7jWe8s'
        b'1UkLgVfAYXMYSlVqyeA5yj6IoBqNFxpAHpnBQbAqViNcOAtcIBMk4FgIPELUFobK8CVKSzk8ZMZerFlgM9yLhxycBFudh11ABQ3jQG03uIXMxMM1YJPOBhw1nggNEa0g'
        b'VkMv6wFXsvAcYrgzRAuDL6mQVl6bpA+wKWJYC7sewtdjjw+8HB5fsIK0mxtOg1N5YBuZ1PIOT+4QtQcvL/Vk2b5IZ+PR5nwKPNtJBsHm7kQIVQ80YwERGx4Ka5NpBE2e'
        b'9AgKYcmWuKfpNb/NWhE6UMLdicEJRITaIcLsUM0YHG7DIe7zRp84xsdLiK7ejDe9tPdTAcOmrBHNq01ou9cOC89tyiLlrRB/1jtQwoAuxS7K24ZgZ+Xt6fVCIEq8n5JM'
        b'243MTGQjZxZb1AW8P5woh+QlbR54MYnaZMrWIsjL5Fvk9oLd3eZmKwQVQKqfgy5ZdvNQzPh7ENMFrlsEzz0J1BgkX85SceC6EOwAq+A2F4tRbPtLgiHtFqMWWYE2PxHW'
        b'YARId2E07Go3F7twtZNdOF1tRh1mQJ2lzOZsJWJCcSi3o9HFodgStZZEwLnZdCKuWox0IgHSiTiiEwmITsRhf0jnMHmsE3UO4RDwqi1YbxmZBFtGuqi3RLcNnGvBKjZo'
        b'cS9CwjI0PiUSqSs2W02Rhnh6ZiisN2Jf2myx60IKOgmBencvN3BDrD9ZeZozpaNyhp+40Pu23K8i2pt7d+8bzILqSbLoXlT3W0EB/SrVyX12Tfmg56ua0C/SPhroO3Xu'
        b'zIGevcYseNDkbqoSHP925MX0D/7s98Xvxy7buvxs/uvBcbGbL35TSu0553v8yEWkqeB2BMMKuK2DvaYdg7ByIThoxjOqK+Bu2EJQTVpmM8WSh/FKR6MQHCf6PdwRkwRq'
        b'+HUZPloWabXr4TpiyY2Ap/P5pRR8ePmuHuAIUzqmiIBN/zR4pl0BAkfhamcYjiwgJfQGWxFeYoMTXAm1Q10/uJnAINgO94O14fERFgR/drATTrJrIi/GBc6xmDpEZJnY'
        b'dHO1BVdQ/SRS7HuXIsjxpZcGdaLLSEdOnhGFbWx2galNrLMUEM5t44pQ2jahWW3M0ZqdoOYZWhPCqBL8eQm+4BAeY5kDaizosq+DQvKnXs5g87R6yhml0gY3xiJ8KSag'
        b'S9BgsdacW6ghLzAa7V30NKynjSZHtczosqcdQpBehIMevMamtAOI2LHcCK816plCjZIJwUtmATEcJINJRIq3xUsVodf5Uy6+ZgfHj6A6LrrRiRyLYujnXxSDYaSzBRSo'
        b'JHaqTJBrQpR6zr3YAi8gLeAibDWXwPPuJaDeq0gKW3G4+3GEAUcFsKUEVhAAmAaudkd5auJhU7IS1ocrZxMTNwH9qUlV2BdBgpOwOiIStKbh1UXgHLgigTfhSbj5qYs0'
        b'WTKv/Rui0qgnQRrh551gF9gcDpqSyfj0AzV4iFDiWSysFSzll6OtjBiC+ZlvEdijhFvCwbFQmgoEGzijt1Kv+Q7hFvYK/31Y2beqO18/RGZXru6B5qEqDBlbd7PuMmd2'
        b'Bqy0eu+6XClfE3R78JpjOwJC/nir8a1Fmo9uNb7KpN26/c4t37uNwJu4nnZe7DbhzUVyAVFsZoaEI5OFrDcRyvJAMxODRM8JXh9qSgVnwuMJfvXIIjCAVJdmog+WIDML'
        b'Lw6rXZQSBdcp+EReYCWbBxrhLhL5EgmOoNGrJUt56lhkGHAjadBqBYcIBCXB/X3hhSDnwHmmDO7s8cz1Ce7qoiItYjPM8h2BZKqUwIg3iXhZGobAILNAn601mLSZOmPh'
        b'4kyd3tmccSrI/lYCAk8NiCl1sOIydHmlA0LccAmKScWDeygsLSlVAWqw9mkb4fpUYuqjv7yQ6mim2DoFoT/frxqw13tB4WJ4EJ4igTZTxfBoOO7VmFjG30IJ4F4aUXk9'
        b'ekps0vNhZHVK65ISeK5YKi4qlhZzlN8o1srkwF1TCWCAi/AKbDYh5bfVzaPEQ+Iphmdkg5ZgdiwWIJOUK4dH+/JLHCd4JSFBxo+hGLQwC8BhpM7vMFrwzBvYWwYuIBVl'
        b'E+LemuSwxAjEsZuXRIRi0ZxsD+efKY5UDIHHyMpUpOAeBmfdJ4Hd8DjvB2m1dO+YPQds6FyCPfvWAgnS6JuXWrA1kVgCLoHaomKwfgm8AC8iPDGD9eAmuIEKbIEXLagt'
        b'MzmwMhjesGATxRdejCO13YYMck8ECsjeqU0WUV5wA5sGW+Fe3jO8ZioOyO1QqgSuWwJbpRIhFZLAgXUTwB6iTluwKjp2CNwKziJqDBk1ihoFjoEqfo1By8hYuClVkYCe'
        b'no5PEFFSuBHcHMPAvXDXbOLsBi/Bq/PcFXgRVtJcvsmwHq6VO4ANnCcgthCuFIFrJeCQBaMMIpiVC2YKsYsCbguhQsBVPtzwoURMeY//gqVUKunBwTn8zU9RNaXRbyGD'
        b'TiV9XTSRv5lYjMRA6V1UhKogrdCHsuDg3HBYNxWrDuFIL1CUobrMsNeoY3UKQYW4HFSZ5QwprdtsVJqUFqDSpKYps/lXHF2M3htyicErl6+KrZT+1++/psk01CLrBymN'
        b'15Uw2nfN25b/7oxV3AzLytHcp4fMqWt62dvvQvi6BfK09wdUwun98wb+JE6+O1rMer18dta9hAzLTyPH7lv//d+lP0QfWB0yMKWH77r8b9f8zXd34TnDsR/+NmTYDWl6'
        b'aN3J/l+WswHHp55+NfDbH9/IXv+fjxZNGbixm8g0o9nX8t2BgdO+t37w+Fruvb3amzuTbwe/Pn/rvz1MZ5cNu5dfrHnv8U8H36wa/d7E16z79atef+X7Sd+trr159++9'
        b'48ZMGnBnOJt07VFh+qF793r/23ru03e57/+bPavszia2/s7bL196tXfw9KN3ttWUKObO3s+MPHd5TPcPzu1OH/dF9h8SXjWl1Nb4/Hya+eibBWvleRGxAXUvrR44dod7'
        b'0vKwWy993di6dqb8p3Nvvv3VgbdWvPlm78Jl6/p8dOdBxs2YL2v6Bl98/3R8zbJXzq6wmM1HU+7LvYiaCQ8NKk5Cg4NX8a3DTiN3RMbwDMvMh5uImokAeD2oROhDU0wJ'
        b'Yp39E8DRAIK+iP1qknloB0cG8yoeGuw64rCCO0ETXJeUHBbJw487rIgrYODhgXPJY+nMDLIAGdMDXoFWy7BgZTk8CHbwtWpxZ8NTcY2wBiKi3MG2XHiDgRejwH5+ImLz'
        b'aNDggvvx8GJZYCYRGoolpnBYnRCRgAQ5XCegvOaDXaNZXYqRD8k8mxqahPV/VLJcoUTab89kTgUPjkfqwzo+3LJmBuoRPjaUBttG87GhoHkKeeqGOOcUqResFQnhHopT'
        b'4EVmG6YSUYiYswEeDE9MSaanhlBcXxrsAZeERC2PA8cG2iNOazAmJSEu6AkucLFL4kvgQdKurKngqk2UToDH0YuxLN0Jr/GL+y6Lwc5OUzhhoHERvAouPVNRFb2ofd+j'
        b'S9lH5GVau7wcjaUlR+JCkY3PeEvQL+ND46uE9Ub3AolSzpHAFxz+gqeNxSRQBslYxpNMI3vTPoyUMVrtYhqZ7e0S9Hkq7hTBhQu50kGm3vZ3lqlYcywEuwpcZGo0ONJZ'
        b'rAqoRWYx2FLYR86SVW6+4IKGn2RzgxtsNs9UsJpE6Mwpz4K1SnAyGSFxA6jF0fPu4DwDj0yR8itsG+CxgvAlcC8iujAhGtv9TIxEks3a1D88eeBnVwHxhEanteqUY7U6'
        b'7bJenanqofNzTC4Inji5wBKjnfs8BA2hROb0L02bozeZtUaTzJyr7bhxSqTEJW2CWaY3yYzaYoveqNXIzIUy7NFFGdFdvJcGXqYnK8RBcVlaXaFRK1MbymQmSxbvLXEp'
        b'KlttwEFv+sVFhUazVhMpm6tHVo3FLCPRdnqNzEZ7pFb2stEDcxmqgktJRq3JbNRjh3KH2saRuAIZNvDiZHhzGPwJB9/hIm3FoxZ2kSVfW4ZD4fhcti8dMmpkJajPUJ26'
        b'LMBiQg/57I70UyYmTJpJnsj0GpMsdJZWX2DQ5i7WGhUJk01y13JsvW2PDVTLcBsNOTgwUC3DIZO4OvayImXKQtRxRUXoXTiirlNJeh3JxXcoGqssNa4QGis0NqZso77I'
        b'3KkhLg4XR8i1wzpxV1pwcGHPxctmRtmn+NLmxiMFVL1gZnyiIG3kSHBMLoGXy0aCLeP7jexBwUbYJA2AW+FqF6p3rC5MdKV6ykb3tIPumSovnfdvmUbD6CDr1IIIZdfW'
        b'nCOKga8J5Zi6e5ZN9xxuKk5JEFa/49InjAmb9S8nf/qtSvFVfLZY90D1jWqx7pEqIZva8M34IfXyXSfjT1R2C/nsjZ2vf3hrp+fh8IK47XH+47PeqouUtsadV+0ZJt2o'
        b'Kpf3vTv+3YLfHQxtqVG9G7FWF/3m2gPvRPa6fSerQKfSPFAJd2Cbjaa+uxs8389fzhBJMw+ugZeRxr87XBGKHeNCsJNRwJcoIuNCwEZwJRw2YGWZs9DgKtwGa8AZsPXF'
        b'p5IEmUuM6iIiNILbhcYKKpAjcUIShMh81KQvXpUpN9qgyCk+yEa0TndwiXZrC9PMC3hraD4DERTLMfWimpn82gVFBfWty4wRNlCGSsH5cDuF40WaHZZo2iVIEtgXrpzi'
        b'I49KRIbwVNDkpfcG1V3P9Q/hKZ16oWW5umfP74uUlono83BmXEz00CGxg4fNg1tjwEXQYjYbS4otJmLSnINnkEnSimz0s15iqcTTzcMdGTzVoI5BhhW86AZPxifxM8S+'
        b'SXjlpji6x59S7rG+vE6+U5ZANVJUdLTgUbmMG8avPdIX377PmTLRJ/Nr43q8fsBn/HhfwTvL/njj4K5bp+NX7XeXLK7asSUeLNO/uTz2vR3dvxlx33rUZ52vLqD17ycu'
        b'lYZG12z8c8wvsUXD6j//YNk/T7yz+edx3aVHew+pObHIe9i720ceassMaPS9914wol4iJM0Tk2YKXez+iXCVjXZv+MFacDnJ7jQgLgMD3Pc099iz1rGJM42F5swsZCvj'
        b'7vZ3JuRQjhCvLwlD8aGXRjwXCduKs09zEKKc4krKXSwzJinaCRhvhDCgEwF/6rLuDZMDvKTr35mA+8L6zjRMCBiuiwI1qUNiWaoE1HpHgnozGfkKEUOoOFoY6aMQFFK8'
        b'HblKBi/BrWVwE6LGSCoSHhpPEitmivAKOO/okuYBM4eW8LQzOYfjQw78BgiWCzU87ZAn6kluWA5ER5dME+RJ1PxNbXQiT3/aOTN/EKTzN6fHeWMoHxGtuzLz10FLKGIl'
        b'TwUnwLaZyOzdPHtYNFw3AmzgKGEaDZoRkF0i2VaygdRQXFawpOj3aQl8Wa39WmjvoSIRRd1fsj32PwtJqB2smwh2zQS4LFgvoFgVDXaCl8b6gkre2VADG0Flu69tdjwy'
        b'JmB1RCJ2HWLDgkQ9wPXhWD8HNeHjwBGJHG4Hq8lc7/L+QqqldBzeN0/6sf/tmYMpsvA0aslAsXgepepTmJxkzFYML5r+u1jPUXE0rzg2w6NgKzgJD8CzSKikUHhWYyNp'
        b'gGZmHGXGrUoY1t+9kOFbNWf5OKo5QExT0yuM98xFJfxCVP+xFNKM/aMTlnqsGmdbW7iaiaA3L3iFo2QVpvTlA2bzw6z9kDaXFIgo75WF6bJoI7n51tRp9L0SBRrjlfnb'
        b'Z00QkpvNHr50S6AG0URFeXpsdx3vHfawUC3cV6iiFSXbyx6lkJuxo2fTTQwV3zLg08l9B4/h336baqTTLTOElKoi5574Whm/6VnKPGpyXhGNqrT0nntYJLkZOLIf7S/f'
        b'w1FF6EXGcwHkZlxxMBWSXI0oosKaPvJVvpnqoSn0K72mCFD2/O3SgwXk5uspPekIhvJuUc4buXpGf/7ty4a9Q+9nqaKWnJPjX0828jeLp7xKVaN3t4Sw3WTzZ/E3/x5X'
        b'Tv2TokKjg0LpqZN68zf7c59Ql2gqtMWa6nWSXcrf3BTmQfnjlH67Z27xFfE3B+YVU/t1LNIw7mfNir8Uot/7OytjakId9N3X0tlptwwfRHv3Xv/diI8/dd97dHzfP0RM'
        b'D30n7b8Vk9ZbqTQvgVvkA3nV5Ixbkcf3G5WR65YdM375yty/jOzl/8Oc+NAzOV/9+c9v7brX+s/RNXPmXD413uON93KGvtPoYdjueVb90hv7X55btm96zKPYwMCpecOO'
        b'/zBuzKv9mr7t59cybGHPtG1p23xOTg5aDOZPvHAyQ9Bz1tty9w/ya3rFb5g7/+ijf+mWDHtLXjQx1W3KicK/180de6D7O16n1qzUq95NulQU/W+vjxZBReh3PVr/9m2K'
        b'76Kcqec/63njYah2xq2Sa2/pVjV7qpZd/6Wi97/OLPAu+TrhULP4X7sDT01+o/a1h0OM+cx5vyWasG/P//FB89hXr71VNDx0x93Pfr5671rKw20JY5QHu938wucfLT3N'
        b'+6bU/7u0QmJ6dOg1xusv4vXFFYNK100avenjvctec//XR9O++Ope0LWCh+n//SLo4cKfzv7Xo7hE+Wb2pMyFwzcsWuF7ZNq5nC/eSRi9Yfv1lwbcPFRYO+LVE/s/e+f1'
        b'M28f+vmbgk9uZ/5k+mnHkj3BZf9Zuundm3frrsUJ9iwOiPj9/JEb3vvWbPJZNHQFvT+/QfturlxMhA4dssDuFSAugSS4ShFiNGMzc0ywKhxWR+H9lg4kLKWnI6v/GJFG'
        b'cLe8IDxRkaQIU04BDQJKKmTgdXgaXubXsjbACiSGz4HL7T5uIq4QfvHzaOdmzUBAkpoAmjm8xxXYAU71C1pBHBmT4CaECK2gPjxSnhhu28HOC1awheDocN7Vsac33Nbu'
        b'R0Fv2yyi3IkjJW4w8UmMA+dLXXbaYOFOuMYWOSQd+aLT1d4vHlHw3Iqk2C5FiQhe4CyC/aR4vY2nt4SjnXcawn+D0V9/9ONDD0QSsRctJE8kWONkfWg/IriFZPG5mLgn'
        b'PFEO7KpYGvhkMW6fbMPh9W0im23YJiAGn5P8/h+sS2KNK/FnEse/yiH2K9DFp5PY/zGs4x4jA6WFvNRP7P50xTUcb9tVBZDmdw20hpCddcDeHmXpiWS+CUf2ET8u79vA'
        b'fo0ocE4Am8ct4Wfc94csxPNpyaJB/NQEDg71hmvYYA8rAUBOatMb5oyJq7QW8ai4PMoWfRirGLko1+Znjlsg5JWGOddUAYNoSq/VvcmYDqAn7JcTe9vioL4rGLsrBQwX'
        b'Fwcox0+r3azrMWVW6AFO4vfG2Y8+X73dN/XM62+zwz9c8lOvf76VntBvatobRxrTwo5p+yZ9fHtOSfmfuheOjf1xU+r+dz5paEkctadRcGX7vclBf6hapHpX2P3T2vtH'
        b'g798//LlG2febln713+tZH7oMWfZLyDMJPne5z9f/y5XtEQe9lbtzZPzj57ds+eT93fc+Vz0ys3IB9m75SISPLgQrBuGNzrtsMupAtwkG52CdZ4EFvyHwu2EJ73gIVgr'
        b'4n2IcBu4wkcgXgVnR/SFTc4jhIMMk/F03l6uUDGf3xHs/Cykt5M04Apo4NMhDPAJY0GTEaziMWDD8hKcxjZ4YB04iveYBKfYyeWB/KYPZ5DGBGqjFEoFXJect1gupLx6'
        b'sZllYDUJkQI3wIlh8Po8UJtqU3QcOywFIZgCh4IK7Vah3/+c/Z8bHOzc6hqHhH+64Sik0GlS4qFk8PI8xo/hV7NjMDBWorRKZ5bmeY6wWzszd///uC1PYHVcuV86+DLX'
        b'xjozOnGXH4ArsYkK9sDTNi2fobxiWR2on+4yxSyw/TVJ6fZgHw2dwWqYDE7DZgg0XIYQ/YrQrziHynBDfyWb2c2cRlDPb1qFp/E5jVAjIotE3LVSjVjjtprSSDTu9UyG'
        b'B/ouJd89yHdP9N2TfPci373Qd2/yvRv57o1KJN5NVKaPpvtqcUY3x9tox9t8NT3I23zQMzH+0fjV4w2t8L5tPTX+5Fn3Lp4FaALJM1/b9yBNL/SGHrZvvTXB6JufhiOR'
        b'833aPJN5dE9RG9Q5WuPnoo5eUuzJc00jI7EYLomelUNvwi474jfVlBnUi/XYe1omU2s02K9n1C4uLNE6uQldC0eZUCLsibe5IXkfoMO9SHJEyqYXaNUmrcxQaMauU7WZ'
        b'JLaY8CbYLh5BE04i0xqwv1AjyyqT2ZY9RtqcvOpss75EbcYFFxUaiM9Xi99oKChzdRTONvG+Y/QqtdHJ3UmcwkvUZeRuidao1+nRXdxIsxY1GpWpVWfnPsGTa+sF21sj'
        b'SWeajWqDSafFjmeN2qzGlSzQL9ab+Q5FzXRtoEFXaFxMNo6TLcnVZ+d29FxbDHpUOKqJXqM1mPW6MltPIaHvUtDj3rlmc5EpLipKXaSPzCssNOhNkRptlG3D6ccD7Y91'
        b'aDCz1Nn5ndNEZufolXjdfBGimCWFRk3XfiG8ZBvRPcevn7Iv1ipniK+za88QS+iXe7yms/PYoDfr1QX6pVo0lp0I0WAyqw3ZHd37+J/NgW2vKe/DRl/0OQbUbxOmJzge'
        b'dXZYPyOiRagkS0WiwK7hT1xplaAYyNmXigyZT2bT4Q1kQDe7aCOrRKHxEZGRcD3ePTUWbBMuAytj5TTZ+jnYywel2ou3nE1V4IUM9ak05QN2swgmj43Xj276hjMpUbol'
        b'r7yGF2Pd/vohukb4faOKt60/iJwTqk5UM2cDzm4ftX1XwNn0nQFxO0ZtP5M+avvKgg+zCuR3ryf3jvjLI7n0lnR3AFXQ3/un72TISsDxAWEzgtvldnfY6iq6QYOen8vb'
        b'0b+bk1jmRTK4Cnawk0fAfURyi5BwP+iO2it36BFScK0HqOLEQ+P5WdAd0ahXKsDmcNgQP5SjWHiVNoCNsbxY3wZ2g7PxGlsv0GQrJ7ByDqgm87pwtwUeKTXA2iSFiOyB'
        b'mwTP9CK6iRBu6QaaQS0pdMgwlhItpZFVsHMS2fFmPGhEP7iB1SnJQkoAVw2BzTS8DNf1flYQmosyn6lH1JmZSeS1n7O8XkG5ScniAqyQL+3pSraR9nxK5wBhY7WrsO56'
        b'0QDDJ2uPBF6H39pJj670dQ7Qe9L7u17BhHVYvNretqskCd+1zzIhJUnv6IT22coCdGlgbAuZOr3OvtTpccATJ6/QS1hNYfbzVkicaTNYnlKfDfb6PPZ1mr6yz4JFPvNV'
        b'ufZXYSjVa0xPedVmx6si8KvsalwXc2XZBXoE0goTwmr5s6tga617pra0SG8kMuAptdjmqEV/XIv2PFjMdOzy9pfbobunA7ptO21WCZyg+wX22rRvwdIJNPENhXD5TFjP'
        b'pcAteDkABdaXFfAbTDcjG2IXOEETf8Lhcqp8bAYJu6KnwCuwNiECbs3CGnsMhyCglklcJNAHxW0VmOaiJDs/3KF4802Pimhp5ecjFOsjX85qnt7jjZjDLy0YEnvgiy9T'
        b't/439IDv65XygZMP/yVh1MEzlxZ8+82dvGPylSu2BC3Z5sauj/jdol4nhH94PHNSof5PJySCus/8sgZul0tsi0ozemGo6BvZlRUDV0URvAlcBpuw37TQLcG2v9VVBtSM'
        b'Aud4GDuNLFMczYZ3tXZ295v4OJNz4FK2zfkBm8FRilPSoAVcgZUErcAe8BK45HCuyOFF3r8yENST58hubSnm0cwb7OcBDaNZMdjHI+xp2OifBBuiQBO3CJymuFgaXPOE'
        b'VeShXzo4Eq6Il4BmckYAv48yWN+HlJwPj8NrZB+9G+Cy8156J1P5BR2XwA493AfXkg234+0g7QNOsHBtNDjpsn/Xc2Kq1pBtLCsyE0zt5YqpwVISeSEhUY1kA9ROyGbL'
        b'7QKsz7UJn23703Zgxbt97mTsEyUVjp8HT4dWWwX+DzSjSblqQ46WD3ew6zJ2Lu+gJyF153lVJIN2yfNoRvYdOTrOCyPlBbvkRoEz8DgR2lHgUgftJQIe0/u01bEkPmTX'
        b'+D953An3IQsQdoT80msuy41IlrTmxH+wcwI1d+CZzPO5082fzXijKffW583eGcN//erOxCRBVHXvAPc5vaa3nPr0+qRzff/qlhj85tfbW9VXlmcIuqf0ipW7EV/nDLi9'
        b'P1EAwEtmm2KhBxt4ntkFa7xAbSqi7X6KSHA8IpSmPGE9q+2l4FWbTfByMk/VubNc6boP3MZHWF0H1UHY5YD0vkshNMVF0eAsPAOvEfeHt7eZ3xg0qF9SKqiPatfzouF+'
        b'4cg8cJrnzf3wlBLWgiZ4vV2HuQKbeNg4H4WPAGhXfcBOhH1gZflw3i1bB1emOik44Kgn1nHWa/gW7oY3x8Kr8ICznoNhYVbCi7OlVzYhtkw7ZXSMN8Y/URKylYYvvTS4'
        b'A1N0yPy/UHvwxsRHuuDOT1248xkVkbNtwtxCk1mvaXNDvGA2YEHfJuQFftdLgAgHc/YlAQ4O5kjEUtdLf+wRSxPpDrY4/jdBo8F2DeY6J12BtwMdsvqJrMtXnmfcePQ5'
        b'YbIdALLUhvzO7OvgeFtb+ZzT+a8oc2iSxYCsSEXC5C7CeJxCguw5sc2Ms7mEAMm7qq9Ra7YYDaY4mWqW0aJV4UgefjcBTYRMNVVdYOLvqQvQTU0ZUl6wBmUwPwOB3Doh'
        b'EKvUq74pYkx4k6S5nyd+q/pd1gPVI9VDlV53SvtA9QB9L9A9+vqYtll9N+u4+kG2WCfWiLOqVfH0mRExVL/PBn3t3itzkpzlVzVvACeRRUNggoAEMhGabEABN0wmXOgO'
        b'98JWHgYwBsANcDXCAVA1msBACKhNTEpOADWpKXBd8mR4JhI0RJGATTmoE4CTw7NfnBk91RpNpjZLn20iuinhRW9XXhyPOXFp7w7k75rPxoZCnqu24Qs+Y8a4w5UhnavH'
        b'OSXTO9IShtyFLme6YMh3XBjy6TX6n7JcLmK5aV2xXBrxTyGuM/BkhsPRnHjPyTP1/z/uw9kSZqbKeJ+SmXdBEdtApzeoC2QabYG2cwzd8/Hde8c28nyX2fvMk/kuIqcr'
        b'znufHvSVe9DCjxDfYdnlDy/78VwHtgqcpXM/My96N/QDlxHPgXqw08Z3iOd6IpWWLFs44wZ3hCfCelgflQTqCecRtrPCOsx540CDyAdcLX1xzuvG+zafwXyphPk66GCR'
        b'nbL+b/lvD7rc6oL/brnw3zMr9ZQzRugqyumMkSfvI22Td4+zuuA8QoaERQyWxVmI2xDlOTmK292v2RajEeF/QZmTNf1biLLx6mbOhCM8/x1/Ah9jkqv78UoTIci7TxEE'
        b'71OfStzMeTpEjjIsBppgK7yC546ug812UWCjSFADLhNfVPSi+e1SILYbosel4DBPj5tXhGHzC9mOoAZehJfaKZIEUY8Dl0UyUDGmw6ExXRJgdqHFYHYaL1NXBDhX3BUB'
        b'dsqqtIcf6p9McbSTzrUPXd7pgsTOeD6NxDq99n9EYjpEYoYnklh7cPFzk5csNAyrYXqDrCQ2cmhYFxj8bHJ7/YcYhpBb3NgtiNwCFiOCew5yoz91d7NECxG5kZmwmkXg'
        b'ipPSwVMaPEhrTcOIXVNe6g5qwTEuqh37iuAmchwT2BUKt/BHmNl0jnY6GwGqhAmIjs8ilebCcxCbN+7CZ9FaJr9tVYdB75jzRUkNz5bf64LUjruQ2rPeKu/ZceGxKDNT'
        b'U5idmdnGZVqMBW0e+Jppn/Boc3csFNFrjLU4UwO+4BNzjBspm7O1TVxkLCzSGs1lbWK7/5JMe7aJbJ7CNkm77424EYi1QjQkAtOEkUgT+V75DVtYOLn+VqNLHmML+Ba7'
        b'cwwO5XT8ML08GRIb0unK+Lj38ujl1cvLU0xWQuaAm2AjCYFQesEb2M8Fz6fAuiRkfDJUKFgpWOEG1rjMjGA+Hk/ZNqFwnYjlw8jbutuWYdjGiWy0+1g2pRTvD4gdk9l4'
        b'jYXRgDUwJ41LieSc67gZDzra3MHxeRxd7jOOZeAcTaZm4CZQk9u+EBy22F13/BxEUiRDJUrw1MTeQSS2dBk4NNEWa/zMQOOFys6hxosmuoCawzGCe8cWg0+5ntjYvlXp'
        b'i6ywxoV3jpf2UpK4k++C3CksbrxLRpffG/hxJAnVjOgmohCmyCoyPaQf+9eOMlEFKej2ZwWjBd/4X875dUqQ/HL+9MzjfZryr6SvCt2pfG3E0Hn1EXtST4464jPYfCXu'
        b'6OzJU/49729BvwbeHR64tCxcPUMsyvd9u/dfGThGOtR3xKXBa4a+Xl6SMmLAitDuo0Jnl467wGX6HCk63Scr8w/6c6J+sw+rtCMS8++6fZcwJtyjZ266UVDR76vJJZKH'
        b'ppKi0J4fTznuHuBxZcWvSOsfH/qWO79R5Etwr5h4fW0u31nFxOkLK0hLR423xeLE9gu82XcCH3bj64HPI0E3l39Q8sOQwfzNkaqeVASOxRm7WLxPHE1ZYjB1VA4C52Bt'
        b'iiISn71p3+sLrk8SIXtvLTwIjpXBmilgi2AABVYPdIMHlBZS2I+zbIG/ulnj9o0T8G/Ic7eHCO+ZNNI/jN9+c9LUezeOZhMWoafVy1mSMnuBhB8fv2/L05e0jCLjM00m'
        b'JONzf3QgGp/FYXp+fMaMHPPs8Rn7b8v/7fjcS/vOXf/NuO0MOZ3DvbFhQP0oTxgtnSR/818jvgsOup78wzvh4tD7hgnTlh3z+/uHGzZMeaW/IO373rEBfzj6+e3Xevhs'
        b'+W9B64SjzI4+0x9qzram9Z83ZOxfSpcnzDmyb9TcjX3lh0TuitCFigtzXvo8/Lvof3z92efXh95YuKk16jBzc/7KM8vevB327zsplTHCm42fDZrpP0BzJ0/OEYtgMjzC'
        b'OB34MgquxH7qGXAtsePHTJ+K45nm9u7q3OZFZj7G6ExveDFcgc/FxMQgoNyjx8IrDLwIKsAB3le3BrTAC+FwXRh2x4XBZrz6beSw7M5B7r91k1fn1f1Gk9rFF469CU5y'
        b't5gjIYDeZP2hNy1j8GpEb9rY7BArbBuH4wucpO1v3nuWNp50IC5+wbddiOZtMueIHjxzAnfny8PDwFawWQnqnLSZILCHAycGgKtda4KjuwRNxy47L3S8octO+w7A9OAB'
        b'87qEAOb4s4ysID16S1/CkKOXEcD01ydT0o/Ty0X3eYb8aexzMGTcwt7vhx3M+k/E40Wf/Z8wZHrfXV6kKasy7KsaxqWMKuxuO3RHbUPE4C+lZnMaZcQnu5Mn63vY4hZ1'
        b'Z6N0yfn8zQFCG5LFpi/TR0+hyHrQNLBb0g7E4Bjcyc+/UaDWBmuPtATWZAXof/qIKz1JL4b0IbDmH5OEe/GGd3e+F0fqnkPstPfi3Nb/k16MH7HHSz//jQp+P8cDyRLF'
        b'HQJr7PQ7d9++vPLd88Pv9Bj8PcfFD0/tvfGN0Jc/u5L4+ZTV/3zwrWBCwc9HXhuV+s/p9//ERn34UmrQ5itRWQ8WeC+R59YZHsbWBv+c8O4ftK1DX//PGo+DzUce+3mV'
        b'/veHy31/GDeyvPf8pjlymsRHL0lhkrCagpAL7IQNlHgho10Orroox795syGCIxptO46EuOLICorj+JXMBEEwlkgJshhPtSMJz/7tQPKiG4A5wQcu9T9dwMca5y2FSAAM'
        b'XGNEKlsYvKzE8JGQYkcPFQcOdE90WRWJV5+Q/UpzEaJUC/h91fGJHxgzKplyhnxmNRz6zDbSpaFmGqeZTDXSCwMXMOVcOd5/XVBNmRl8JgDS7T2tgjxWI0DlCOZShmC8'
        b'83m+xFjEH7xDnuEjUQTzyE7nhrtWfODLeFIGzn/FyhobUSrioSw9hT4JydkF+F3CclE1bRXhfdo1onqUwyocTRXvRG9ZS/ILKvHhKqzxHXxOAH5HqQHVVkB2hsf5xZ3y'
        b'i1H+NpR/KsnPH3cz3pE71JG715NyN9J4l/hqIZ8D3aOs+FyCiLm2PeptB9pkWSmNWwDGXB5nJUokYbTaoqlGDNmzHgssZp1ihONcFkS/p/GI44dGbJuSY0jkIqMK06Wb'
        b'1mBZrDXikwvG4e9CvCO5RtsmnW3Q4w/EVuDzjuJJrn1nzfZiyQ7xifiCt5gxYt2/jc57wcX2bVJ8UohpCL802QsJI1MckUpiEm6Lz7vgT83wIYcZcGSJnL/TJ6ntr5js'
        b'IyqmyWZGmdGwTrIoiRztHRuGt0Mgu0DIgjlkTNSCcy7RH454CcwVVsok1tAzKXwGEul+hpwmgAUb6UJjjIMz6Tba9ATr3YM0KtNcmFlQaMiJZu3nYLLYLiTh8dZceISv'
        b'H2iIgjX8vpB4J5jm0SJqIFgjKIOnweFOR+s4nPKIHOh82ijF5p6GteKThmgNl0fhU2xQrQV++IgLuieFRTa+Q4xCoa0NWBY9ZgaUktVz3zB8YwRLdfqCAjnTRhva6Nwn'
        b'NQy3B7eLNHA4bpjENlwcOZ7EMgh96wuOIPOtljQInwONmpdK2orMuUtCamCwoAycAjefsnaa7nLt9NPPz+u0dlpIdV7d2r5g0LCiOL6UfZmmilS67hOX8ze7L3glMZj2'
        b'ZqnxqoQa3zT+Jj1WWJJII+qQqSJC9BpKT/uLBSYdevLrF5JvVW+RbbBOFn2reqharDOrq88f1zapH6hu66Le+wY9bVbjqMCHGoXvcfXtrDxdqN+q6pIWc/RH0UNjjkYn'
        b'UAnV64oaQ/vf3u2rG7w/188kkfZPismOZnMCqQWV/t/c34jUbEyaY2EVOE4WW8MtYJ9twTU4N5D4rcYg9eB6eKLC+RS5axa4B64Ce8z8mfBwB97fPUKJ7HG4PoJGaU4w'
        b'YE9PeCo5gKjx1oSe4ARZsQFrlsDdNCVczvQD+8CVF1+z3W1xoWbkcP5ghkyNPkdv7rgDsG2rLDHNn1YjpnvRxpsO1vp/tSobFzOetb+uwukHuKzMxke/givg5hTU5PpU'
        b'0DqUbI6Mz8bBh6rynQRWh1AjwEvC5bB1iQtoOM59xS45HiqwxKvkzz5hlG0CtSlbr0cVO0s5pHDns1NFudrSAr2uLJG1HRhFsWQ5aj+4rg+JgCCrxdKSwQmOcodrGHgF'
        b'3CjrGr2w2MaHkBAh6Iuj2HB1ym2VI/zBKI0v89UY61Spp2xz5mYx2CqY2o5hWEHhbYzV8yLCYb2jnqiWYC/cyZF95fbAHenP3WM6p6o9tb/csmKH8kdMzXHqMTzQM8Bq'
        b'eCppSEyCzRCd309AefVlRw0M/43dpfsN3YVqx4vS+R26i4SMrCschivIq5uxrIDyhKfYwaICl3BAxwFqWAxqaITqSIUq7WeljGFmjPpsJYNUCaqc5Y9UsjII45liCT7G'
        b'qCjWSuPDjchYC5RtIdGDh8QMHRY7fMTICRMnTZ4ydVp8QmJScooydfqMtJmzZs+Zmz4vg5cBWDHlVQQaaQP6EsS/cq5NyE8UtQmyc9VGU5sQb/kRE8sLfreOTY+J5Qcm'
        b'CzedHABMpJ2QbM7DhxMmwgtJQ2LtrgJZOhqhnmxc4uCuR0hqoxMNf6APId/XHBBBG28/gUJiYvkxKOjAU1GISs/j9/MDgA+bwENwmI2eCvZ2vQUlOR2adpwOjarz1G0n'
        b'n+t0aH673aOl4Jh9iTjcMjvFbQY8D1rS0OV8mgdoAOc5hgqFl7jFcP88fdZ+FWvCTfhg7ehvVbeRvOGP/pDq7id7ZbOU7DRbV9VDzvCRSTsDwvApww1486o1ChHlFsOA'
        b'A/BKL37B6P6h08MjQV1OxxWfJ8HNJ53vrDcVZpr1i7Ums3oxvxEHOebGGciXGN9yjAzT9RyDk+MYpy3uEqE3uJz0jN0uo8He8XhvsQaiSKAKKyITYJ1iaSZFDTQKVoyD'
        b'16e6xPu5+n9ZW7yfk/cXjaf7c4bWuown1gR8Oo1nNyVZYS+OnZqEJGsDrOOQXD43JZCRwNZZRHuoH+yH3aAySqHqtSHHnT8KGj1FNv0Q0DokmupHiZSgWkiDXfDgIt4F'
        b'eyl6MHp4YQgiA/QUbIOV4DwNLij0ZKM/60IWbhLkgQqyXwI4BdfzG+8F+VPRFKXanaOybnK3LYjcoAmlplNU6XGdirm0IobfcqEU3oDnwFlmnAdF4a0Cm8ANktgYKMZ7'
        b'KIj3ZakKvhoxjS/hEb/OMvTdSarkrUXZiEDIRlawIq84KQE0RwgprhfYDCppcKY7PEKy/GPYeDSW1HTpCpXRzZBt83u4j8P7B3hrYlU+P09mbSv4+fWa8Qv6qSIyQwdR'
        b'+oza65TpHnri96tySmNrIjdBuvZXjW5JyZ/ytMVL0uc/5m6sqV+l9f54jWJOUN/3Pwn9UvLqtBK/tzc1ev/zr3/2Ki77xnfJj6+9OqP0stFEBRyY9UAWvDWo55qfRIXF'
        b'jWVNgfp30i8df2PU+l8f327zDVsQCudvm3ine9Tbyh1f5X+dvHbw7qY57294uPzYxNUXf/fwg7nXB30xTPlTypsNLWsPPP5b+F/8h3zdeGhT689hA0pPLv05IaguxWBu'
        b'2bl0+d2Z/xj65YcZ7mFBBRs2TUma2ey5bevDn2vn/1L2w18qdvzQ+t8jK36lkyIm+Adtkwv5ve/qYV2h3fNAiRfCxpmMFtTNISEYQ+AmcM5JmYNXaXIqcCG8xDtD14Kj'
        b'xvaV5GULyfZy9dF87OFReAhcx/HQjmjoGLCeATXpngQB0gcYndeEaMBuhiJrQsDlhfyOq2vhPngliawYZ/JAPaigx02F515gy/T/gQvWowhJHG0mgp4RsdGDCejEdQSd'
        b'ZRzNO2I52pOVIg1SioCDo/vRDFmP7UPOQJTa1nEbf+cAKH63lDaJrtCYrc0kB/i1I9Zv2dOeMb5NUc77quB3WboEuHpZR4BLFw4Lj48II5HtGOYuRsdEC8B2jgqhObAF'
        b'HoarLLhi+alw70yq32BkXVF9xyzMtq/EFFJOhg7eOr6axoc11iBrCZ+xV40tQ4GVM0ZYBeiXQwJV4E/5olQ9UZr/p71vAY+iyhKuV1c/0uk8CCEJIYRHgJAHAiLyRoVI'
        b'CAQkCApKm6Q6IaTTHao7EEJHR0C7m7cKiIiCooLgA+ShIsr/Vzm+xsUZnXG0x51xZnbHQVHGcWZ0GGfdc86trnRDUNzdf3e+/1vy0VW36tZ9nnvuOeeeR0hYwpM2tHHw'
        b'HxEVMf7dapHF44VcoloXkZbAc8CQApTMyCOpOok9NRuBlBUFVc1izGcICutFofyMkKqLLwipSiTFRTYL5JZ3xLdymesorPP6gatgWlTdxYBldIwYs7S1tnpUFfeBmES8'
        b'rRyTgp72INAIWESgqcMTswc8qNwVxHCmy5uU4GL1J5hfVDwXBnmFBr6D92+bUOpMbMvdYjwmAAkvEAQBGAX0bEhcsX5EPw5c/lH9MfQsFJ3F+Az0MDkTVnFf/UFJP9Kk'
        b'bUqiBk35OYsYRQOKVIig5pBYjUVGhFmEYcYQgCIOMwndBLUOZldQJMghhkSML72EIqjhLFIJC+ApRXfG95BbrOEUC7EvcvW5IeNvmtTe4i0vmURUXZOvccLC/oNvHrJw'
        b'EfyWFON9+dBJN02aSCTyaWwsyZkMQRQwbEgzx+SAp1atXxyzNKr+ttaYBcU8cPH6l8PMEKUvxUSoJ2ZtRZU41RezwEjCB7Z4td9Gb6ejf0n42h3PvFuMCzdFKe6lgQJg'
        b'Miwh8eSvt0d//Q7y3Kg9jZ52tOgsokhvlWeRU00rB82HPfe4fsikLJIOf/fRXACtLWRxSH0zlkFdg0yEkwsMwesSoA2dnDoiJChAoYc4N9oVCfC2Aq/G2xkhAd4I7Xkh'
        b'FFBmdhJDAuWKvWB+eG7pnPnxr0IJXz3MvvIVhHi4Z+93XvjeOMGWqmO845xQWEjTA6NJ0PvPtCiCtU1ePKryeD0tMCmeZR7vt6zEmLNV9QTRyhXH/GDXUDtJhu0gRxgO'
        b'csZmE3IYcmtecaN2V3nJkOllxYw/XM/GnOf6aQ9bhugbru3evBwDPndpNQBq4haIHoliC8JQL7BsEZfIS6wLbPDMosj0zOqxLrEr1ngKyD4roDU0LrctcCj9MU4hpFMU'
        b'5xr7ghRlgJFOVVyQdhpxDCWKb5impMM3qUnPMpRMeOYyn0hKDyULnqQl5eqpZMOzdDIq5xZkKAPDIjAPaDZuX5CpFFGqQOkLqR7KIPhGhhYUKv0gnUVRMXoSnzM4ljIV'
        b'ZsTjC14NDJcJg0nhtRHJdgnZKTwuCtnx3mJwgDLMfCdblPzY09/AP/VTjgj8q7iuoHTTzTlOWFduWqcUoDvQWlvv+aHJSgkd+QltKz8/4wUcPzUWd1dcFCFcFkxCwldD'
        b'Az4jVBusbezesi5mb/XWNvnckOH1hAb0TGyAmaN7g75Mo2a/K74o49aFQszixs2AlsJFLPtwqfy4i4vsSE+sGT9Omhuzu06aG1zzSpclofr5tw86Vfazrm4mMTWmHXSr'
        b'Oe2I+NtvIDE1b8SunYZnLSxWbQhAoVlQr1BQTCCM55bmwBN7s9xarcghEa+A/HnFupoP5Cg29lU2F887H8rHmM00V2uKHdXn+GExfug5oXwY8+6L61TFOLoxfuU5y8qh'
        b'nRQ63HyFmy8L9+0AnlENBpY3wcY6mesyPCEH9jOogNaLiZrdgG5gb/aQb/z3xbj6G6EYGwUGysNIHblJ8Jj4TbXpJFTkzpP8EDTSGAaZoF+gGNWCETqYx1jQ57AVlkAb'
        b'EBFIP/iUuAodNj7mMGH+IocAKgaB/1fRYBax2cnwgyX+5xuo/g0bY8XCaoHCSWih+nfuojTVv8HP6aSm9Ti/aVBaEnSbIIjKohEAq4iEVEiEIB0BcoNAbeXjbcUQ3KG4'
        b'OBTPF3yBltpWaOE3ZrNlFvzAWBUxq4e14ZL0wVVc5J+KhtEux6Ki8x2Zif1gxScNstmNy1g3BLMbgtkNIbEbOOQ8ixG+hjpC7U/uRhP6dArGBx99/KnQ+UvTa1ehdO6L'
        b'5H5kntcPVv4FG4GpsRGBdkaANFeHxnGDWojkCQug3YkTZBwCBQUDmETzUEiE1T2ZEQeSivsunRGynqW43UBiNQU9LW53HHdN5b7b3aUqQaf+ap4OGVHIAcx6JS3WrsK7'
        b'n6NFiaBW/m19Y7PkG2rOaIUxo4Ii0oyKxoxK8bwmeaSKvEG7xufWwoYBzZsTZhnGImCOhdg1FoTML22qLYZHXyY/M0bFJTjIT0HyyJhVfUuk0/jimhsX3HW3h9rc7jq/'
        b'3+t2O6SuLTQruTKWwSDd55pzgfOAFVHkdxQdUCx0rgFJXx4J252wz9wrGFHGxeoKGJbfcCahuAKQcZMvGEtDCl3x1Htr42b0MVvQzw584/vBb6jROBF5XHcySFn1YGwj'
        b'l2TiLOd5a4RlqLig8QRIhWbjFQIWRdggEVfEM8UEFqS6OibVD7/ch5aJLDxSzO5pr/e2BZqWeWKpuIe5gcHEGgNfYNMKoWO+wIT+/elAFVEtj1gMdiAvbAvxrrmwV2n4'
        b'86vuuqaiJ6VMKX5cQNKK5I0C22SuffzYZERi8NMEDEj7EsRdpOWwiHWLtg4JYB7Y9tV4jM3ncjcJnZZOOWQJCc2yqtD6AFIRmH0hMJfdN/J4HW+8ARwhIxJf6grJ7PlS'
        b'13yuvRTqklC7AmorgDKtnTZ4IoeAlui0hmw4uCFrLw5yh4h9sXbaQ3b1pRAfOBhC7Qw75BDHcz4pZEd6BRiWUyEBfxXoCeSHEpoYZpKM42pcoOcsA5DgKrbHnLAugKVs'
        b'8iow5TFr0O9WmuqDpKhAewLsKkGArbqYHTPiIgoQockYnz9wJOOh/cZR7/cFmK1jjFfwlAMKjfH16ll8K9QrzJnW9PjHF9lMs6DSXlLcaxgKo4gXYu4A0wUnn0UxDGXS'
        b'8nEILNpB8oZrdIIIRSSMrVDk3GKhoqKYryjOPl8hm3rzWLw36sdm5z7nGMuNnDSjDpAGod2ehob2GsLNhIpUGX9SeAMIqSMJwcAuXd6XGBsMW6OJxpqziTbJabEJTotL'
        b'cjnTpXQpS86SM61ZDpsETyxkrz5Ev68uoG/Qn9c2VeobZuobSpZOL622cLmTpQp96/C5xSy8WIG2NyPBsEzfGFiIwTYxf7HMjVDkubX6XcXMn5l2t37X8CoMvrphZkh/'
        b'ErLwXMqtgn5Aez50ga8MUl5ymRgixG80WRQ+ltJS2+yJ0yVClx5MN0e5xoRe0YVnWVuez5oZYE3Rt06jpji0BwV9nUM/ksT8xjFXYC6XwPymU+BEVOwHVheYSgnYVp75'
        b'T1tgYYaZDaLB5sroRQ3yWBWnkgpXm+JS0tagFzbWo4yYc0pbS8sKo6UX0se0t6ACBmNfYMflExhMvovBZAIG+BVJ2CAZ2p9ytfoJZ+ymxB8Qx8nYTgstK+I9Gdy+TaPm'
        b'RnLdZxJPtPRk9ux8Dmkt/EyUTEpJ5gvgf0fPxC59X/c6aiF/0Z3TDtQJa8gUc0r5juyk6sws3RNnxhEmkR4GTMXFnlRjRbeQxKguxGJu97UJVeec11MzU/eVT6R5VHjg'
        b'A52oNUZUImB7dWCkixsX8BgTqCQB6KoROIsJzV1sKj0hBoYZognEESMCKYkgvLiUjvDN9C6qx8azSC4okOuuS5dE9iApzpr2LaSP1e32enxud03CGGadVyFl6F5qgd0I'
        b'co3c6gR0IOGecnFKC9+63fMS6rsAOinHd/QOj7orvqVnhLhv/JZaGEGHTXacv3ngIlL74xwOMDeDgfgzyNwR7N8xoX0h07j4hNpEh2wTnWK6HZC92Ia1LZO1F6q5QDHi'
        b'au3JoIH7EPEVaM9L+r3aVlv3iG8214X4tohLxCXSAouHqX+hTE/ySEusiINYig7mESnaFtiYFA4QIUOMdpKmOYiss8UyZ9Ut8dQHyXmgMUbfW1pEe+t3yYrqzSkRO3pd'
        b'WOmli4waL11ktLhru7kkHLTmknAQAYc3AcIKuunOxTCQeQSPnrFWpAc5g/cyeFAJuNBmh3oZ0+clXCSG6HACGwhvLfBWMbR9+SUy8XwLkJLs4vuwnK5OJZhrJXBzNuLb'
        b'CMJjjkrgDtqZXuvZ+AqIua4iSrEtaGi8mtzv90FtfsmUTAlA5rnoP8qoLj5mBhOZcv7aHMwnUnKMxMtPXqpd5Fk3YSG7qDAs6WbJQGI2iVFgTpGOP8bqJ9364Vn62ukz'
        b'0a2Wvm7GzKXePgmr9Gptr3WAfp9+oPtVmpewSokYoaNDIFAMzw+x3vF+xzHSNejldIbf39zWap5bWrgE9RhaeMZWFYGpNKYTcDxvIiQLI9ql4IpWj7oBb+2mCO4iG6ns'
        b'pTo7u7hG4K36f0vrytkH3RhBlpntuGCpDIVXHfGlAigQz6m1O6+akTDG2gHEgtpDbQZ9q2+sLC3Xj6GCrL6pvAzyb13q0HfoT+uHk46czEWMZcL+zZFsI5/WE0/cEqrB'
        b'kr69WhpBvo9DHXRcG3RvMckOgGg6kBNvmDkDQAdZ0ViKvws+iQP/voHSyqHnd0qmuhfzDUbnnaSI8IB2u/ZMhf6Stk4/qB+F5awf4vRntKPaoSTAkuOAtSgBsJSu4xe5'
        b'wUIHP/YFIunzyIDm8dDHBluARMc8omJVbEgPK3bFAfSunHDYY1tgpc3ARrjPFXMasz4T6Hq1uiLJ7YkpeHqEQ/WeJhhGhd8pAiMdF0INBKKXb0KtPGCWSdyOZLKgrjcF'
        b'TxNDgvEGiKpcDkhlCdndkBjw4R2lgZhWOGSzoR9MjCW054eEKXhkboEvLfFcxHQH53NdAskGeLORN8VXMsqBSxE2SVDVh/AE3nU9Y8d+MYeb5K/uWq+X4UUkBOIOMCjj'
        b'3wkmWlVPQ1O7G1X9iNuJCb7ApUm3sMCtUtxaThBQDUNAmEA/2RL5y06nmH1O4o/NcxyaiS7CPQ7/Vi5BgPMMTghifwCERgmPt1HewQN11im23x3C04+1TN6BR9uBK0kG'
        b'IpH0oqDdFxRCEh6As7NCxboBh3peXB6yRFJssMOE6BsEIZoSWG3yaphqKqManjsAOW3BPOyN8ZzWHNqRrBbYk/lQ43wuxFzHpVTHLDV4AhITp/qUmFSNccIt82q9bZ4L'
        b'dB4TTspQWqNIzTKBrMUgdEfhjI7maXMy7+MoqRuVTPJLeQznA2vpKEse7Xq/b5lHDZLYIZCoRcHchUKRJNs0d9O4/MWC8i2MWucxhC0BCr3HxC9fMRxCeFoMeJbGLH5V'
        b'8agovQu0eYNEPbd0CVW+7WjfldzC/ZIhUeB4p8FBOAC2BAEVTLPgPh+tpxw5fEfvb+ln0pmaKUXDpjTiEpxIcHRFpwiUBanBkD1SOcIaSZlFY9YddLoGuBIVLPApPpvP'
        b'zggWkxxUQFloTIYB88C029wNXtRu8NGQxeWC43BoJ+DPRP7bqYyr4P3rXQyUZJwRkHvb8xaRUdEFmwgBF7pxSzDMgt8QD93IwVMaYvUFQ7sY3jHhObwN0p0Id9OCgJNC'
        b'AlqWrOJJ3wCw12qeyDdYMLA8FBTh+dLjTzAPHigqFnYHT2BIs01RAR0gCm43A7Ds633NPv9yX6G5qxf2Lwr0PyevLArg+aKsZuBgfYkfyQyZqcPxCe6NjGoTuyhadSR/'
        b'wYqIpbp9qKmDDq2hgLdxSLMTYCrdkMhn87KQznfkJQ9t4qdJSAqBiWRICpd4bkcgIxjbtMDumrhOqX0Q08YxTMoQBeE3zPxLDkmE80sB50vGUQ3sCA1Q0oMCYv74di6r'
        b'FbwBGuok/KEFSAcVwIeiT3ggMK0JMhVbXGSq9sR1a2dCUuhLwnrsXr6Jjrw+7CJyYYxElGJm0lhdgMWNqsVqWAL2bpnPSWbDqQvXJpO1lxhktovUBT6Cu6uL1M3umd4X'
        b'eFFXG+qV6Uf0/dpefeMNAZO81Q/NZJ6oCnpJ2gvNevgCh+P4j+LTmrRIGrGacRqEef+PUyD45nzqA4lig/YgBROUxLFDkvSYbYa/vrmiyeup/ohV9eEkkwaJ6/+baClC'
        b'bCjCUyArKCAjtIo32ESB3tExXjYK4qQQMFFuC4njZBLNWdEuzG0zGEqp+lwPjL5bqPg9ht9+dMB2zloUKEclNpwtOtiWmwKYj5ZVzFpbF8Cj9JiNFN2UJjVmRVVwf1sw'
        b'ZnG3UNgaCuobs7oxh0dJPOGPSZhDvY7vjmxGWPhjF1g5iVDIJGJB5jsy4sN0oUQPR8iM+Lmei2s84npDe7f2ZSvSI7jiYHQQNc/nfPMME9JlPOAnnusYG0LcxTeL6sRV'
        b'+J2sTiPRFyuHb5bUm4JWFImtArpriU0xyrkRNeygBLQ4W5oOTKfExroGUvPjNmiW6tMZhM7q/W1ehQa6tp4iBhTiAH204z789/ikucV24GVgKGl4YpaWZhhcdTadIM2q'
        b'IX40ZvGoKqCdufjQOafNh9mNNwGvx9NqILyYFXYZKqruoqs4JmHtX0vGSR5HdpUCuTBwkE8aiWYADYE7Us2xx2+6N+IpNXCdOkgheESGIz7m6iBISfHxN8YFt0QLdYWB'
        b'hqUpYHbYorbAvSFY6YaNa/NhQ1ItCaJfNCvpSDMbynJ0L9WJax8hvZgoXam/uOgXXRV5AI31sHRJQNITIJJedm+1MjShNgRJQ9oqMGkrScxhYAw7XpItSeotOCpz4kOj'
        b'1nQ1rBv7FrcbsC0KEbMt5vm6jWhrmLrMhEYa2ZKUdPE/nmuTJTrNX3Zc1IWDE9dTNIfK0DSpoVmq9/oNL3VxjQ3J7Wmv70YOCqgFVmyfxAlznL+qWR7k8at4sjHubq+g'
        b'kcEaUSDEqR78WXwpMsrpkOmzOGtqk1wOV4YT5ZRWdiazatlcdLfkyJ6lb1xmBOpOXSI6tNtrk/YDq3Glvd0UeqDOtARcpyn4QLXEBZKSHmYxbsSwHLY1yCSMtMO+kMH4'
        b'VIpSgyczdtgjmLs1PJ9J5FAXF2fGpIrZUyqSsJ15SjWFQ5G0QRfQSTbygvEZQ8BSUBtYQhqN0hZFCMosZewJcUvZcymzV2BFIwqXFQXOpULCiNoNybjobC1NJ/oJba1t'
        b'9MScAU/Q3ar6lbZ6IOqd+LV73tQ5NZWzqmMp+I68ygJ2SnG7jcDWbjfTsHZjKJU4fdZ1iPYtE4h1D+mC8EzSp4Y1n4rVXsgtXkyaahwWnMuogVYUttT6yOcm+mZBFLC0'
        b'C5aZm4TzCUbsldn+YSY2EDoyqRlJr6vNxiBrYY8jhEjSnKEFM8oK4nShuigikfiT9LCBtRSBHSWFPjrIp/tOYDdCYi8O9YLpKezyS2SmuUDl8OqqCFCJimW1sCm9UwJm'
        b'1xoS2J6lcNdxc7gb4gpMMjNp/ILibBYV1UydfVXhF9hVpqjXDsy/g8jxmLC8zgCDmAy7fWtbkEYrZlHaWloDJEwijT460ItZluNJuyGjY1iMxpM+ERoWX7rtsLocPhlp'
        b'iSsXk22wTLb9SG5m0j6VxXek0PizhsXs0zzeZZ5gU32timHrmEkjTkJ9XLaUljgjXp7xQWjLh3wPXGVSFUIOiF8tGiuJxpfugesBulzENxE+aAH2z5JFthHo0IGle7O0'
        b'TZE77Yq108GEBJ0p7V/DbKeQeuYfOp1A3ztzuc7UkF19JZ4zlApziQKIHYq9M9VXQGkHpJ9TUuBtvHYb1r5UTW5NyBkCOjOHa+bUX2LZirMXl8u1fggluUIu/xklNeRq'
        b'tm7m1fEhF6sF7gtCTvjFkq0G1oASFVfIiiUqYqcd2uBibaAv4T2qRLMa8T0qaSjWkCWUGnLATm9fgr8pS5xKxgYZynOoKuZaqgJLLNN2m1l9Gv2Vn8ZZmHsa5/ujcPb7'
        b'p76s+fOkChJunBMnTJhA0xYT3YAz+LmG3nJhjL86Zr3G36Y2AcrhK1Ft1+dZ7m5nlxXFqUyV3UHqpt4mnyfAUFFLrdrY5AvEemCiti3oJxTmrgMM1Ryz4cMGvw9oWNXf'
        b'5lOY4B/BIibVe7zemHTDbH8gJs2YWjE3Jt1I99VTb5hbnMbgm06uJSpAIisSSyC4AmjgFGyAe7GnqXExFM1a48AMbi80x2PcA+cKVVhUD7QiJtcxEYnd19bipi+YWqyE'
        b'9/DU0x6kx98ZYDqFKTuSTvNVFoN/4IxQlk46lkgnEwhmbs9cFDoMpxrkZEPIp5wy5WBLTjKWHKok0YJLqCRJmCLHdyiVS15biL/8eXTEjFzMdEWIcmgQFBSJS8Kd04Zi'
        b'l9WG14pctKjgFTnEZzPlPgmVlHkuaDEkoLLJDYskB2VyXfu5vKtrVbT6LRzpbxhTiMpaheR+INDWon6BsFRyKdbQZeWFA4eVFCXRTKZUGBESGTa5OvmIwecnmTTBjoLK'
        b'n3Gjprxu+R60Z/LHdxKZ6+hLA4tNHzmmO3Om0+hY5Zw0tCgwlNZKNbDIP+YMaRvaySikXh0ToacxF0F2E7Dg9X6vXzXwNys8zpm9nbwHJ7sBfd1sJ8YXbrLEpU7ooIhs'
        b'61DEb2Bfo1giYVeSRDKOfNXQxUm6AG8geXU3b1STwP5/b+9GXYKAJihpoMUUBKRbbVKOK2tIGzoIztaO2gMprUtXao+KnKDv4Ps161Gibaurq1HJSmxDri1T33pjDaef'
        b'1B4gM7t5afiSuT2cLSIg2Da5bpmh9JwBNVc0rT+wSgxEgDhT37t35tymmh43Zn1a3Xh64JlxkrD2uet7lFSlzx5Y1//+3fzwW/7pp2caF2z47ZUjP76y6qOaOW3+iX/Y'
        b'NeHs50te+fiNypMr3/rns81fdYycXvhQ4OXJJS8/8mB6zYLBjx2d/ubiaM7H5cMPjKqr/ii64sWpZ94ecWjh/MiEjslnfpZat6s8/W9tm67cvTyy+vjU/LdrfnPwl4Ub'
        b'fz926dzlkfrjlfk/Pzrkc/VEzZYxK974QnJ8enDkKzV37a2ccVR/rNfKIXXHPz369WNvfZl708Gz0fcG+GcM2sP1Gv4L18Jb996i3LWpavvhjyrLNo8cdv+cdXc/t75k'
        b'3tgp7xa9sWnxip4/X/9E7ssTT0TShleuW3T63rufmHbfsZ6Pv3H7Tx8pH3zd6Kd+WzGuatjfj3xV1fFax+Tq6z++Lm/00h993FE37C+Pj5z42YK/De/YvuWdIeFfbB+d'
        b'8fobZ9vv3nZjw5y7R+XetSr/0Gel2Qffcx3ad/jJ3fcc2/njZ67Yk7Vt9sNPPdJrX8qfD/56VKi0+b3pXz2ovPb4awPe3/qqmuNptZac+R134tS0/MWLmv/y+Bfzfxb7'
        b'RBp3oiP7Q3/M07RiZrZn8p03LL3j+bmnG3eN6XXqk4bfrb5Bv7mmzwtb16/u0+Ns/0//eObdCc8P66EUHH5p5Q2Nd37ypFTyZl7BZ/V7Pq397TUP95y97arn9ftirwer'
        b'dpU+V7BpxCedp4o3Wd8L9tnReqL8ld8HnpjwfuOmgofVU02PeZ/+p5en++a1vbvohwM+2vPzj8M/PPNp9rEHjrw1vWTE1NOuZQ8Et9xfe2z/jGEr3yzaMGH8sb/ddezr'
        b'Ax882Zl/5V8Obr352V/0/ND+4Ni/btnq7vfsndcM/uTYMz/auHJNY/UvPf9y5SuBw++sv+fQiREtn1y5tOedy965d/vp4kXveZ85Yf3mvX9atOXRb5YFqx48/I37180j'
        b'H2041fFv9+4QV7yy/VcfLhz94olP3nts/ENfjwudVXOPZA8veyX3E+vX7afOrn914t4HNk/e9s3J1Osiu7jqvOMf2M4o4ktFn498eOTJkU++syHrrabUP/xx/aJQj8CO'
        b'the15pUpPd494H+mMTv1xENPj17WHNr7+utXjDr5Ydkof9sLd/1k99ZHJjb+ecy5cz3P7lv56pUPvb77/T9PlUeOfWfaD28ue+uVK7aOuu+bwpL3fvdY9Y+cz/7L6K8/'
        b'66j7qP7AjNiE/TteHPzbtBONa77seOGuURk5E05v/922PiNPpn017ZVr7xnz9z9d2bL2hQnDDjzxWb9xx0qsH7w/6fPom7OOx14b4/76syV3fTO1/dVFf/lZI59/6AfF'
        b'W4pTmMvw/Yv0NehjtFJbP2xaqR7Vwto2WNzanaJ2ZKl+J/OH87h2n7ZT24TeSPX1JdVlQ9FU+qigbdNP3soCUDyp3TMgKba19qxPNEJbS1dSqJoZ0lRUXXxQf+wC1cV5'
        b'2h2UZaG2Ud/PjkDtaOdb1lYrcGnaSdGtPa49EhyBNe3QN02HJpAlolEQ3uMpMXy9KX5OnFEEm+tYh7TgNvbZ9lu03V2SzaWVM6tK9Q3FdLqs7yxPOmC+rcrBpfcIonRC'
        b'O1CgPXe+AkBAe/p8DYDRM4Lo7Erb68oMlFMcoU1tXZWdd4Q9VXuU45brO+zasdqJNAstC4dnT76Y3FVfv4Act8/Qdy1GvKytHmrg5Ub9USCzvs8m8B1bxOj/wsL+f/kp'
        b'7se26X/0n7g8yeuvVYxQjx/AD1crkwX9pf85RJfdJTnhL8uRbsvukZUl8JfNFvi8bIEfWDpwXH6Oy5IzWRIEPoe/wjtkmZO32TA1KEPg+8P/gkKBz5Lhvy3PIfCZksBn'
        b'y11Xlx3vMdU/H6Wq2U74n4Z3WekFvMOPCt8uId2S1z+Ld+an8w6rk3eK+L4AvsznnQvhd5TAF/LOavVxU7yV6Ejlf6G4m58uohoH7RYuTqw+3J7oZAFxeYn2Qp62jnnZ'
        b'mzVDi2qbrJwrV9Qi+t4++qHypuVf7+YDBQBgp3KKyu5+3feLy9LvrKzcduKVv/leXTjv6fe3BCf8Kbfj08cLb5qbPaxpo+pq+8GuwCd7/vTja0+LbS/LwledO/tde80q'
        b'9x13Z9yWtWP266sfGfVObcHwmxtuPz08/KbzcJP25C2/vO8PK9/YYT/56M7H/rYn2GhPG9Lvg+NvzP+/Vdv+OLTqdvvcz+6Z/dfjt/Td8WHhl5oUfe/5SbcuXDu/483L'
        b'fr224bkfPTr8+mmB/beseuDLr67tWdyevX/flDNvv+LtP6vnC1dvXXbqt7/au37s2Nd2vd3w9xcv/+uUiq8Hj312m6dkZODIwS/Gv2V9UxjVXvq2fVPR8WfHPHXNmGbP'
        b'sQePOn6R+/PyV6+/eUDxHRveHTP2mXdveeHgu8r9C5sPzXzi6F9f3ri/9dUH/jRxz2en9i77Tf7Lv5x50/WfOtSWX004fuTMO6mHs9P+tPnjc9vXdkzZO2LCigkFnwy/'
        b'/s9rhnZMf/aP37S8+fvYH9cs2Lb38mPj9zz6r2Payobte8u7q/jlezuqc1949vWXCs8ePaWeXXpy0ZHfnOpsbj5W+tGCzyvcd/345//y3tFPv6r41duHXtqz1fW4/uWh'
        b'tZ9d3/jRv6kFJ4dcVbLwbO2uyhE/uX/15lV/ffcR/5KGhp+M+1lnx20fTj/Td+6m3z7uf3hT0MLbreUnB6TlfmXbPNW1Imv2yxlv7Nu9Nu/jxbuj2bHf715XcC7nlkj9'
        b'+stekWrebF1Vs/PX+b2eezk/pfSQltf7pl/njX7uh32u/sDfd647ddEzKyd9/k75rs6iies++NGk/v/687zROcVsa9Puy51lQNN6fV2pAU5zRO3+acP1h/QIxa5cpB3K'
        b'x0zGNv7cCm0jZsvQTojaPdpq/UlGhjyvbdFfMuNLchK82YgBJtFVYhClJjfVa6tLtKdKZdgfby+t4W/RjnkpvJV2yO8rqSobil6H9E1uI9jc+ip9nZXrV2PJrJWoHXn6'
        b'vfoh9MDN/D0tL032wC21klcYaYC+qQoy6euLMVuJzKWNFqfpO5ud+gEWD2+fdvtUfd2wafoGbOV6/eg0DLm3Tz9BYTH63qDdWaVvHCJwgg+ogl38RG2z9hgLFHw4GChB'
        b'196zLJw8Wbiqv2uOtpb82AQatQNEfQ0p4zm5XdBWaWuG68+XscCcx+ZVVuHb4soywacd4mzaSUEL6w/XUanLh2hI45UCaxryaBv4SdpBqAjfjB/cCsWuxTfaYW8OP1ff'
        b'p50k11jLtYi2sctPU56gb9NecNyk3U5d0J9arD9Gzuzgy85G/Thfkaq/REXeqG3P09fNKuehyLVWfTN/rX7IHUROfpz2pL4XqoukY5zF4qHT9G0wDEhVIR1VdLllir5G'
        b'u58Iwc6xy1OAzKwSMsscQ/S12tPaPonL016UtB3DteNEcmp3ag/OJG9XMCjlldpq7SEYNyAoey2WRgwQqJkr7HoE5mE6tmW79pD2El8xV1/FenCyeGiJHhmGsQz3temP'
        b'8vO1p/T91ANt//C5+rpKnDzhNu0BfQM/uWYxNQsIzHX9qggxwiQVyxP0zVyKdrugPwpk8x5yKXRboV9bN2tWWWXJ9AxtOzkNyxwnagdqtZ0MiCNLvVUsZvWsaiyDc90q'
        b'ajv1o1Ps+kNBlJ203girZd0wmeOBvX5kjL6noJR8DTXeoB+O+yEDoHJh7NXBRnTUnBpcXdrjzF+EVKw/WsdrLy0aS12dARC4pqqseDp8KNcIsKI2ZfsXMxdnh/Ujyxks'
        b'VwLo6IdXQH+2CwCqzzWy5fuktnEwTKdBAGvPTiT/ipnaalH/gb6mkrmkP4D0f1Ulei1l7XPpa8Wpy6u1R7TdNKSl+o6yKgrcKs3T90m8tkt/uIwxIEec2ibWrZkw5Cv0'
        b'aHEllK/fI2rH9XsB+GncN2j79U0lldqTQ4qHTQdoTdP3iPrt+lHtBzA8rAZtn761qmRaJaw4d3Merz1Uqh2hsZk2BnKtw6W/CVfjXfqd1/HaC/WVNNi1+u6UkukWjq/i'
        b'CmEWtmdrW1iNLw3TwwDgCF7orlEo0I9wKSFB36nt1reyRbcD8A+MOotZif6HDqTz2g79qTE06pen6LurgMMZNZIPLeGs+t2CPF7fSV8GZG2z6X5RykWvVuh+cbx2H4FQ'
        b'7+v1u+POD7Ut2gkKWI7uD3NradIWLNEPVZGb3vjydGm7RW3bnGtmz6HGD+tXkOhoEhaNvsdwiamHWwnT5dTrdyb6o9Sf1V6kmSV/lPmwzNHou2FaPWKVMlgnQ/Uorz2L'
        b'i/VuQCUzaFjWV5Vp+yVupnbAqt+u3aFvJlwLiGGz/nQKMpOt+LW2qqEKYIvL0neK+mPaMZhTdPFzuXZCfy5F3zisbHp1Gx0r6keR4MCsoxbK2lMCjA/sDzTU916/gpBf'
        b'+bSZ5Xz91dCZhzHiwZZr2Jp6BuBpF/lrxf1DhjV7HOD4MMDzFbU0Ik3aE9odJfrGGYC5S4u1VUVlMOc9CkT9Hhji24Moe7sBunS4ChcuVBvVntC3VZZOHwYVylwpZ9Hv'
        b'K9aepnyAwnZpzxpb2oZZxfqGhdrBSoBQ2LCyiyRRP+SkWbxR21mEfn1nzaKdxrqgHZr0DCyttgwC/DmTJAAPaFKRdnQZAicg8BlWLlc/LN2obdbvZiGWnu5pgTbph7Cc'
        b'hgkY4iZDh03xIe32KwgpXNdvCQ4MbWSS9oOby3hEsr2CKFTVdql6BBs6rKosV3vY2PzwgZXrPRB2T21vPsOFwJjeVFU5c+hMKydLgn6ffr9tpIHx7tCfKiCnr9DRyjJZ'
        b'26vvh9F/FEApR3/hUjWQDObyf55J+of7Mc9viWHbDT9ciiDY+PP/HMASMbUTdNQm8ZjHxd4YJxMG88b08gSHcQffCRhEyUZ+h7KSynRSeZQH3jjJ5tZGR4dOQRbbb+Mu'
        b'/CuUeSaZZjoFqGER8ATbWt3uLv4rLt7fzyf2D28Yx/Flot9KemeqEaRy6KaRHeIHXobfOvSuAn/ReZF5eCgSHQxXAa4CXEW4ZkfmNXBwvT4yrwmvjsg8tEKL9sX8eFAc'
        b'5cN8eF6DwKyfOjlUNPCKLVI0rcXSybfInUKLtRMP62TF5rW12Dslurd7HS0pnRa6d3idLamdMt2neF0taZ1WPAoMpkPpPeGaAdcecM2EawFce8AVjWNluPYLcZE0uKaF'
        b'6AgkmhIiK4RoOuTLgmsmXHvC1QXXbLgWhUi9MWoNSdH+ihztpYjRHMUZzVVSo70VVzRfSYv2UdI7bUpGp13JjOaFRIWL5KIWdnSA0iNarGRFy5We0VlKdnSm0is6W8mJ'
        b'XqvkRiuVvOhQpXe0VMmPlih9okOUgmiF0jc6QimMjlX6RScq/aOTlAHRK5WB0cuVougoZVB0gjI4OlkZEr1CKY6OV4ZGRysl0XFKaXSMUhYdqZRHhyvDolXKZdFhyvDo'
        b'dGVEtEYZGZ2mXB6dqoyKXqVcES1TRkevU66MzlHGRKsjjtVcdKAyNnp1sBfcZSjjojOU8dFrlAnRucrE6GUKH50SssKbwogQsoXsDThKWWFXuFe4b3hmg6RMUibD/DlC'
        b'jqiTFEe63JS6wmnhrHA25MwJ54bzwr3DBfBNv/DgcHl4WPiy8FXhqeGK8LTw9HBVuCY8N3w9wEM/5SqzPFvEFbFFilcLUXuYhT1n5Tqp5PRwRjgz3NMovQ+U3T9cFB4U'
        b'Lg4PDZeGR4RHhi8PjwpfER4dvjI8Jjw2PC48PjwhPDE8KTw5fHV4CtRcGZ4RngV1litXm3VaoE4L1SlDfawmLH9QuAS+uDZc2ZCiXGPmTg2L5OA9FfJlhnsYrSkMD4SW'
        b'DIaWXAM1VIdnN/RQpsS/6UyJuEIpVMMg+jYFakml8cyBEcqHrwfQ90Pg+5JwWXg4tLeCyrkuPKchV5lq1i5CW0UqSbrVgfPY6YwURZyRoRFnyBmpXC3QYT8+KaUnpezJ'
        b'rc5QCinQVDBP8uT5gc6qu9cGw02RWetEuGa7mhdEBxTcEj6uRG2oxp3rWRQYUlzYxBQzawvr2pq8wSZfsaDeTOZfCTvOxZwluRt8JCZDla+oxXQngae46hNxs5BiCbBb'
        b'oyfYoKIhgs3TXk+aK2TqjGfT/oaYM665Qxo7PLrCaAF0CHcOdKvc0qp6AgFIiV5/IxrEokaXepxj/oS406R6ge06jUogp3fiDxkKoFayX/EAUiVPBKjLHRNb/a0xB5Su'
        b'eBpq0UDA1uBmB6DMB02XpwITEcfkBionllLvd9eqjRThEkNzupuX+33eFeYjBzzyscJiTrgPBGsNl482SDV4axsDMSvcUWF2uvEFggF6SxroVMOyWrUrgXqumKLv6MZF'
        b'T9UAaR74/FSOF6awto59oHo8y9BzNiZQsYASlnqvp1aNyRSqY3hMrGtqJO1t9IrC4irEHBgImd0zTZvDxiQH1dp6D8ZLdLshe52bTaQV7lBTICa5VU9DzOVWmgK1dV6P'
        b'u762fjFTzQXAUJjbLuQzzwlDipMC2yFwIOlFsSXQ0CzuCh3dCkWYs7Fs8lLoIn+H5ESnk1+aP5/5eGowrUovMEv8LldBCJy/NRW9iARwxIHWbCNqdMnxNr4CbyJWQG9O'
        b'WFa52I4QD4hHaEB7hQKFgqSQFYMYKSRNKykkRRzNNnVVxNlpCQmRlGZBnQb3sm8IpTh1UcSZwnVaIsycTog4IpnwxgV9d/bCsZAjVkj3WS2E5EhP9K/pewqdlgS2wNOC'
        b'SHYDulTZjjpWUFMPqOkg5c+B7/OxPN8P4HnfSAblOxPJAHRjbS8ki6+cThvktUayIK8Em4RoGBK9BiMroVMVKlNutm3m1csiMnxpby+n0ntDzrgTFgeUYnwdssOdA+8o'
        b'uAwapthrODYSEZ7KicDXaZHUFMP2LCRG0ultag56iwWOUOFCKfguJAC6Te3FMZMo8nVpZx7nTR02Glkocx/MiCOSB/ULOEIhSxbaguSw8YD3/4fa3Cs+IqFkW2Tnf/I0'
        b'439eFv29xNUI258izFcTknYxQpVIVVS2kQUbqeFk4p8okeqjkwjhHCJmZT6bz+Ml0SW4gMzNx+9EBzyDdSOYSybD2INoyfxUMJaMC6a52FgyWYlLBt6KOHERCfapy5IW'
        b'EU5cCXwj0R2CvyUkBc5QDHg5gn/Zq8kOqhMAWV0VspJZiy0EtTHAgUWTN57zLY70jgyIDIKFkNtgATB+LWQH8J3d6YigMpkDyk0JOSK9YXG+B2CXlsLl4q4swr0L70NO'
        b'Wn5QUigF6MM0A3xTMAd7F3KM55Zum8/5fJGBkdRI7wYuMgD+D4L/fSNDGvhIBtYU6YtLLAsoTHieF+Ej6ZF0pMyarLTMLQjEsJwyQjboUSoAPFxDsDQirhyu0xXJBHoA'
        b'n7h6cbBsUolOSIGvSin2UzuVAPcN0OuNfKfFdwaeyJGhUGZaKC2SQ+8BMUB70yKFlCo0UgMpNdBIFVGqyEgVUKrASOXF20mp3pTqbaQGUGqAkRpEqUFGKp9S+UaqP6X6'
        b'G6k+lOpjpPpRqp+R6muOG6ZyKZWLqYY02CbKkLoPcRsRgSISgL5GBkdSocfpofTNQuuqkES/1s1CYD/BSy+EFygDxr4BnU0bvenFNZBvtkgPhDMoVST/ABKOPPmzwucl'
        b'IYlUH6WkbSfj/8mSLS7/B0Ab//2oaRBstYFVXagJNQEFm+FEWRZdLPiWJPDsT6YYJ2jrmwU5s+R4+GN0vpwuoQUw+n1yCpmiAxCWi7/YX6bgFNMB4WGQ5DzRKSIvb6Kz'
        b'uBtUQmfM6SEgLAmAx2agMznCJaAzMWKhnRwolYgdCHxAY0ynOskPT7fEyX+B/3oaxi1y3DSeDaOIA5HUoZR4h/ZjhyRYD0hyCICBM1knmBolOpVGBe9I+mpBLaU3Uojy'
        b'QgdTIxi+AldRGmCk1IiVpVBVPOLYNIjHclMimbjicKgIW4kWwKcR+2ig/cYnKIkDZgMcaSg64316xMaUnkPk+h1XY9K23f3w9fjvhdY9coJRkySQlbnVweeLeMfgyNEF'
        b'R1hAZnzYfUhJAtUXSUMq1xx2iQ27fxANek+gusQAG3ZMZ2MaKRjy5g0UIsDcdHrr2JRHA4fm49Yc0tXHVNIQA80WscK2BTQpbBeLQ2JgfZye5rF8CahD2D7bK0IW9QMM'
        b'JIjIEjYmC2wiMImd1hWOEOltwzaXJXFBrtmhnmLOUlhARPomB8tYun0+R0y2Cxj+HuGscK8GqxH5xNZVE1CNFtL0zo+k4rP492xjA5LBDquK2to+PmSBa4NZgx2FGvTt'
        b'DfAtPIM3dvNbsx1AhZbOT4ionWjakuSP1Qy+h4wHdBmGmSIIoGMFDNaCngv9pUh6km18gpskMSYE69STyCq+xn9vRxYxV1PA7a9rcC9XUcFZPSubdicS6UA7GDsCPDjy'
        b'4/+hGBG5/0gIXpcNY6KEJSMwhW9U/M4EVC5LEpnYo+4MWggiTybbXWKOFZ9mWl2GmDaTL85hAgbSxJ3Mke3/ioD6JD57Cn+exp+D5C2gHr23BNRDpGrf4W2qU5+h25ba'
        b'4GL1MBkmw42nFp35q0fIeKRJUQuoUGC+Y2JtHbDti2sDaL4csxr+h2LWQPym0euvA5a/OPW/ZsiK5/8DyNP/9+c/cgCBMNlhMbykcoIgnX/44LLk0HEBHg1ceDjB/qRu'
        b'/pzdPv2P/8nGfzMtO8VMqyTOGAUrUGxYgr+FTkm8LB/vxl+D61KwycQdCgL1s3pusajiaYuKOJWJ+tLUhzny5e9OlOi53cYSbalthXUaVDGuLhm8kt0+Owh5ghbi1PZ6'
        b'Tys67FXxPBKPRepr2wIetzuW5XYH2lpJEohiM7QGgacp7q6E+tNk9wsJ1qHjW/xKm9czkc5DUNwkCUAmCkAddXc4s8J42l8gZ6pxfb5/B+hH314='
    ))))
