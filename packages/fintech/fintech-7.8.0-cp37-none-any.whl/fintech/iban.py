
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
        b'eJzNfAlc1EeWf/XJ0RzeoqC2wYPmFG/jEfEKyKmI8YhCA420QcA+VNQoCtggp+ABIiqeARQ5VIgXmfeys5NJMslsMhmXOTIzSTabZDLnbmY2Ozu7r6oaBCQzs///fj67'
        b'+Okfza+qXr169a7vq9/Pj9iAHxV9ltPHuoQu6WwL28G2KNIV6cpCtkVpUl1Up6saFZZp6WqTpoC9pLWGblWatOmaAsVRhcnFpCxQKFi6NpG5FRpcvs5wj1oREafflZNu'
        b'zzLpczL0tkyTPiHPlpmTrV9jzraZ0jL1uca0l4w7TKHu7hsyzda+vummDHO2yarPsGen2cw52Va9LUeflmlKe0lvzE7Xp1lMRptJz6lbQ93T/Jy8T6HPJProOP/pdHEw'
        b'h8KhdKgcaofGoXW4OFwdbg53h87h4fB0eDm8HSMcIx2jHKMdYxxjHeMc4x0+jgmOiQ5fh1/GJLFm15cnFbMC9vLk/dqDkwpYIjs4uYAp2KFJhyZvIumIdari0vqEp6SP'
        b'J31GcwbUQoCJzOAel+VK3ycnqBjdi2z1SvHYMS2F2f3p5g6swzYsxZL4mHVYjOXxBiyPSkoI0abOZjNXq7EnYa99LvWDwh3PUbcKrAyivlgRGYsVG2lAadi6DGyNDI7G'
        b'MiyLisHjURq2ByrdXsTTU8Ss819yYR6MzRo7IyXmV+mLmH0b3ZyJtXAKO90810US0TK4tjAqKRJuBmBx8NpYPJHoiiWRSUR98HQBkTFYERcTnxRADcVhxOi6yLVJASGR'
        b'UcEKaFYzG5SMnf/ikjTFAFXy6pPGmr+yHRleToEripUkcCUJXCEErhQCVxxSOgWeMVDgbvSJfUrgdVLgxw5o+dJH5I9ICZ4ZOJqJm3f2iV1g+vGHPe4tT5M3U2Lc2AgS'
        b'0mvmlKxtWTPlzWZvDaPf+oSgXR7309NYE8typ9trrT7qfxnFXEH385m/U94Nz1aeVWRxPl601MY6WIo3W54y+8eW9/ImMnG7ft/vfd+bHDBFmfAzxZ83paw5wXqZPYga'
        b'1vukk/BpAwMC8HhYZAgeh6YNAST/yuDQqJC1sRvhkYJle7sttfvaR1H/uHDstHoo2OiXGdYyOO1/yD6Gbm/G06OsFg2Dxj0MSxkU42kPO5eHGbqMVosL85/OsJzBcbim'
        b'tY+j+y/7QIsV75JOdSxkWMWgDNuxXDTNNuJ5K1SoGVRgM8NGBg3YaBdN0xhcpiYlgx54yPASg/NL8YLgYCndarXu1jBfFcNKmmkUlIkGKIfre6zYrmXRKQxPMajyChMN'
        b'a7F9h9WuYbF5DE8wKMUC6BCz4HG8hyVWTy3z5rNcYFC3Dk7Zx/Kt3gK1Vuwk3roPMzxDxPD8atGSHbTJCmU0ncPM8ByDs9iCDWIevLhojFVHPF/H4/QHUcsZJ+aBDuiG'
        b'i9a9Kgb34STD07TiCbsFNTLIu3ut3vTl1lgxpjYIT8t5sBCPYKcnsXA3g+FNBhcWSOFAyQro0dEmLMIrDFtoDF6Harmii3ASr0IpbRxUQaXClUGrwVs2PcA78MCKHQrm'
        b'QkvFagaVW0Ps43lTBZ7HY9hpJ4m+AtVC3icDxohF7cY7WKfDNg0b/TwxSRuh8BcbPhN7VNa9SqafK2gdx9r9gm+o3aqyYpeajbXT6hicgFp4IEaMgPx4q7eSzVGKGc7i'
        b'FYW4764djZ2uSjYZ7jFaEdSP3irYgpZw0ohOV9K2FtIpvE6Tb8T7YjWjNFiEnTYNX3ydmKdyMzQIcrvh3svY6UHWmCjGNPiPlQLIP+RD9xUM72IFLZSoxRE1H970aCk8'
        b'xE5sV5NSQz7Dy6TxI6BeSGAqqQmx4aZgKbsYtpLqs0TRsORZL7qt4Tp6UYjmUtIOyXgpdrhQk4pthyaGbaTM2EGKxbkbC0WRJGktc8kWGnfC6ivHVMAVbKT9Jv5asF6M'
        b'urRVGl3q89hD3HUqWPILjEwF6tk60RAxCTt4gwvzmy5U5PwEhVxQE1StoV0jYmehTXDdgJXEAjdtfDVup85VwTxHkSgYXD0QLMZAfTDc1xHnDO/DNYZ3iAFsgG7B9kJs'
        b'8tbt0bCX14l56vDcYSnUI9i2TId31SwpgmE7n6aJppnAmx7CUXhAbVoyO+xi2EkqzNkR650H9/AENZL4bsApMVsjdhgl93ehGcqtNlLiIjzLsJjBMbyIrVK/zuKNQB25'
        b'39GeQui1eAPa7ZPFoskOWqF0PlbBHSjTwGWoYiq8pIhHB56x+/LB3Tuoe+kePEne4rgGmucwdaYCjqDDZp/K20/BnQRn+2xJ5iA0a5gblCvHQwt0GVRy2bdpfDfpyn2o'
        b'oMCTw3LgKtTaR/CmmtlwOXpqDrn9VJYaZhMiXwH5eDYaLqzV8qCR7gv59pm8bzVUkgutwWJomQ9NGmMslOOVnSu1e+Dyllg216qhwHklXfRdk0eW6OzZiqfwpPg6l0zj'
        b'lHpGNPPDcrUbtFvsBr6Mhwq4LTvDXXiF946EVmdnLPFgfvBQrbJjoQgNcB2a8Fof7ZsDaN+g7tBiIuLVai0cg3JBHSvJa53Fmki4QUz3d5/NJ1JjQzDzC1FhNzTH2QOp'
        b'99wpeL+fbw1tdjdfJTzYqdOT/F7ZOJqt1bvooANr7ME8m1owesAqD5ODltThFpbzX800BwuxaHaPgPP2UB6RLFv6WSlXpUraZHDkXnZCKUkRrkF3JHZr8Y4HLXgGX3Db'
        b'LAo5fBBexyPONXABqdczX+xUUY5UjU32Z8VuwtmZAyRZPlREr8TyqW/EalPxQWAsOZ9brvAque4OewgNn2ABB5+otV9QEXhBBdVYgqfgWAbp11kWjhc0xE7ZWLkZV6CT'
        b'+g3cDLl1fOEUVktp72pU5MzbdtkDqH+GcuxwWtHEe5coaOccahdsofDAZYX3Rmx60vvJWvISn6gHm3tAA3Xc9O2zaMgWLJrZr6D9E5A0Lk8QBOaKXWezsVIDF+FqstDV'
        b'XXBuzGD165MW9Y3bTFzdVLsu2WgP5wu+6Us5wZMZ4AH9edI59oZk8obYdDJYK5ZNFyuhucom9I0i0eAZbMaT5E7zuGDhmB4ukWbF4kOX2VDrKSQbQEnr7cG2RpqyyQUL'
        b'tgTMl6uwwgVXLFNniL3bDu3kkp39STJuyUNU0cnVaY01bZyYAQvmmPp3rs+Y4ebMlSv1pEdc1ePxvEsoucVX7WHUfySeHPlEd6EYypxT9a9fcBUK9zU7R+AJ6TIewO2F'
        b'zkHNQ9zAPAPzm6kic2s2SkM9lmEaaKZyk29y1aiDVlL1uypKxi5TwsG5oUBSPW+IdohhczF/oHrs1kDtHLhjn87H3MJmz4EKzr9JR7DkOeanUuGtl6cIN4DNYylW1PQJ'
        b'cLBKYJcr6cRltQt54psCgUTAVe1gXtJIi58ooBo6PGIjVsHNGcyCp1yxKgN6BEcLQ8c/8TbOPV6pJ5aNbC5c1MAF8nYnhArtxAKKtE/E32dBS/KcnAlXMwfrNVC9IUOI'
        b'CE7gIzMn/9xSKZ0+l+TkSkVcee6cp1incVnoideFUlg24YVo4SOo22DVWCm8vC52PZS7TIWWJUJQcBraqOcAl0bQ6H7fAO7QSPjkMMyjhf3DxQhsHbrJswXvK7xoi9tp'
        b'CygknxGODy+FcccnlOuR1blep+Pzg6OkOuQ4r0m65ZCfNMjwn2ztdjv1dqjwHuRnCFw5hoL5I+lQz3sP6K7k/rSLlCw7TCrv6bDVTytkK9eATnRQ3zbiVrNW9IWTW/Y7'
        b'Nau5ry/cFvNTstkklOu2m4/0IRfIpq4O4wfxuLZPlcVuhuNZDZzf5yNcG/mMRiwbNEoyVJ/S5+nloBc0lP4fnyz1uHrtk3h2s0/DoM7/iZEnxLgsOgyXhcYk6KIHq5jw'
        b't1ACrQPWQzvao4FKLF0gV9NJTmPQKCxdr0xz6vIImqV7/kgonqeA+uXucVhgkBtGehPyVFB22tdRLGF+BhV2TU0QSmk/+NKAvZ1DyW+fXx/o2uyaXN/pYjNiXRc8vW/c'
        b'HVA8z6d9e1WFHZvgulCyaanLhvX9vHvEdrLzHrXXc9Mlzw44s/xp5RVpR+lootuqwlY4IiW/lvx60VP+OxPLB0g+2GUBNHrLQNq1Eh4MjBCDNOgk1Eod7tFgrX0O39hS'
        b'Cvqlg8TuFtcvdejcguVYuBMvb2GWlyjEEzPXZEzt3pA4RPPwCLWLJWtGOUP8DR4dj8NdoRTbdhITTyL83r4k50mGIbMcqNHY4FyemCZ+ru8w+m2mIU2D9LuRXFx0nghg'
        b'JFnXJwIoHzKU3OPueYoxzyS4uszHO7FSZq9Cpd+Q3ONuPBfbDU0qiSCWzR6vofB8DtukrzqyFR8MCJH9MuY7iFXYQzLuUKuhaLXYbgoAPVOHy1ZESCpaQbpxXO3qPVPm'
        b'sA48R8n90wrN9Wgr4Xu/xSp8+CJWCpG+GJb4dJYyN2bpYEPGGg2cI4x8zhAj0Xc39cznQCMyVcKMyVAjiwlXtqRbOby8HsXIdogZx1oxRBkMJVa8rWAm6BL1jAq8HyPh'
        b'f3k2tvGSSWCALJkkUYY6VgbW61BvhTIlC85keJ7BuexVAlX5xSy2WtQsl+M9B4PCFXBFIvwL5OK6RZ3llZGyzhKDJYLYDFqZgxdaEnklgVdafOGYxKk6uEbwnhGOriRI'
        b'TyjU8wUJVi7HjLS6KxncxUeCs1OUapQKah5YfsgKx9VkakcEHD23FetEyygoxB5ZuCmPloWbdbLS8zI+yLN6Ebnm/YQu+TqflfixjMR5RhZ07i6X9RySmyy1jI/Bc7Kg'
        b'c5m2ThR0dsFZwfeOnQd5OYdia6Ms6MD1YLkHDiydJAo6WWZZ0IlzE7wl4Ktwhhpc2LSXBfY/CSeWC94OLo3glZ5IDjd5qQceRokRoelwk9d5DuMxWechuH1PivoSnE2U'
        b'lZ5O7JalHuWzgtgzugNWjq1XQQHDBlpo1EHB14sJcJ/XeXKhRZZ5sD5PbnRNKlTxmgjpbaGsivjukku5TeKsse7VMON6sZRy5iuG7MV6OC7KJYv4rvF6CVsid43CNjZT'
        b'k4Jl0q7yUtPJ3Sukpp2IjeOFlBUBspBCnJfIaU4Rum2xeiuYYr4opZw7tEk2XIPyTaLIskU21M8MFw0bD0WLCst6OC8LLHDLX67lONwnC+YllvUvyAKLb4xA7qEUTU6T'
        b'TpMN7B8jBHAaXoESWcW4jA9HYqeHmkL9GoZXaSLanFYxle9U6BF1mUAXWZfBh14S0b/qOUUUZqCQ4I0ozKRuF+TG4AXyNZ2iJnHRT9A7C60rxe7sefYAdnq5sCwyT14H'
        b'uBwbIeTmmwld2MlVzR96GEkOrm0AaTt74UoKdu4mM6S94QKthOshgreXl2IttWjZtkNiq6uWQoNc0NVRobIwxGeWhSG8mSHI6d25HNwUXHNKZGXIrBE8TIczhL95bQhb'
        b'VsjSEJx1EU2BWoLPvDQE58moRG0IiseIpo0UDltFbQiu8qINrw6p/MRUAXhaSy0KtnyakHg1/yeF1wMFvE5IWp9qFEZXs2e3YN28FC4S63e0bDo+FBKvwzPwSLTNIodI'
        b'm+up5DbySPB+MRPrpUW0zYqRdagGLJJ1KLh+UDTZoSeImjS8TJgvyj2XXfGc1JfWF2JljQpaD8ki1YLlQrazUxWyRgV1ziJVQI40Y7iXqcM2LQWqTtFwDruDxJADm6FD'
        b'VK/gzChZvDqwWepxBV6CEzpXLZvGRM3oysYAQSvJjD28prWGL5UXtdABt8WQNeQwK3U22sCT04QG1fjaxJB09SxR7SLY5ix2ncMqKdPSzdN17lpGiR4Z3qukQc9guVA6'
        b'qDXpdHvULCOJUQoKp0KgUK7+BBS76vbQzpXAEVGTPRO8VYzI2rKP183wnkkWzqDGLEZMHouFom4Gl9bLwtlILHaaAzpyRdkMqt1l1WzZdFkXu431WCyLZqd4DVcUzRzS'
        b'kl88PFXnpWBJPCw8oLgBd/CSLPc9svvrvFTsuXH0lbz24mmiv8pngQ7bFYyyaSGxxhiQq4+dMokaVGQg3B920x7r8KFombUJi3RupDOPoFNMch1ql0tn9QrehBadnez+'
        b'+hqx0DNwNEAWl6sIupznBTts4xrPS3b+eFyq2k28gw06K+lGG8hdOK9MlMMepPtDKdcOSiZqGG0rgfHToQIcJpKI8qmxBoqdlTy46czxoHg+Vsfwyp0aOjdAaRJ7YZsW'
        b'L7iMNKiFCCdB8SEsjcGaiWuxTMVU+Iiy6FWYL/YK617Ek9F4PEbLlNsVxsSwnLliUMSM8dFYOh0rwrA8yMAPnzxGqMbmqZ2MYtHooDjo3hQSqWbq5QpoJrRQvSaNn/vw'
        b'Hy2TJ0fi1IifczqYOJDih1P8UErlcMtwcx5HqYvVBexlzX7tQbU4jtKI4yj1Ic0mlq5KZG6ZBvXPf6NkzF0/4GclP6m06o3Z4ohSn5Fj0e8xZpnTzba80EEdB/0RJQ9I'
        b'A1/KybbliMPOwL7jUb2ZqO0xmrOMqVmmYEHweZNll3MCKx83iFSqMfslfVpOukkcl3Kqgp7VvqvvGNaYlpZjz7bps+27Uk0WvdHi7GJK1xutg2jtNWVlhboPuvVsrtFi'
        b'3KU30zTP6jdkypNYfkSb2k8ldLgBqea0Z/kyd5j3mLKD5SjO4IqolYM4MGc/tSL+k0aCMe2z8SWYjGmZ+hzqZBl2IrE2S97AyWx9bJIo//Z5bPxQ2kktVB9rt9r4Grnc'
        b'E+ND5oTPn6+PiEmIjNDPHoZIumlY3qymXKNgLJB/C9SbSDXsRptJnHGnpGyw2E0pKYP4fZq2k38pcaFazrXoE83ZO7JM+tV2S44+wZi3y5Rts+ojLCbjEF4sJpvdkm19'
        b'tn9GfU52v5IG0901xiyruM2FvNdsHbKYQWfermzoEezIuDXyoASKx4tcsmCFTCU3QL04XV0/aQKblfKViqWkLElQHmTSmVfPp+SklH+rit7MNufhddH5haU6NmbDP7uw'
        b'ESlZ26PmyvPZhzFezM8vVE1kgjVhLkw4xDhohw5x5MdjHk8F4dIyg7cMCW0+2MXbVDyxk20HRcv0cOdhYKVFngVCizOY2xW7+VkgRblSeRhIUaxFuCAjdvNo7qnmbvmB'
        b'PA4kjNAsM2g4QsGEo4XuLHkguELmkGuS8JQul1x5DT8pfIV75Uook1HmJF6mkLmb2CgLFFG+ngZJUDQe8sUR4vx4cYBIo14Vrs53BiWlnVZyyU08iadcoxqvYoPM/s9H'
        b'Qp04XYQTPHnhx4uUwDuPZq/tImzAzxcXz5Cni4tWyYb2LWPE4aJvqDxchNvOA5ZOKICLOpIS+WYRn84/5zyKmgHHArGTVhtP6UQ9z9VUgpaBwtI1614XlqAVaXwl9LjK'
        b'HO4YPoBWnpeP4BGNp+WUYBUYVE4toGyHN04yyjaD3ZnKQskqMQ8eyZQTEXu1MgGv8NDymQ7wLIhPFYDHpOxqo5IEmNgzTkIJaIRGg1K0TYGWtaINX7XIxr3gkHvxYJXz'
        b'TLkjR54pJ8ENoXXvp7kwj1UqNdOnZDXt2MXsI/kk+Zvsc2ap2S4rJTMsdWmWOesXy5RWytjYdF/vpVURa1dGeByreeOtA7vueO+9qg/dts91fOiS/JzGyNqg8dN1v41o'
        b'+v3GFboVI/9hW+VvtEuO/f1v1JMb97GaYtP8ml/H//m5VanPpWZF/IJp9qzT97j9ccq0T4osHyfMCtseNs0zIjXiByUlaW6TPtla/8hxJun9P3/6OPZ3/keXfuTdlrXq'
        b'34vuNibnef3r5++UtPxhlmOS2ydTpr7j/07zvC9WFj+/raFnV2relwdv/Cnx3z7+TljDhYD/XH9o/8fluxuPPvzh+k8Lqmo//Na/Wpv+UPvOtNm/ef/urLe/8+GkPzd9'
        b'OeNbp4JeOPqu37H08Y9fm/jV4w8Xxvfuvt7VFLPb8frPHs3t3PndN5onZCU0z8s+UR96+7V34Y+fjV8XY/qg1tfgYuMbnPC8a9CIkSEBkSFKpoWzypAxQTb+DA+cdksK'
        b'Co0KDjSEYmUwZfBsNtb46NXbZ2O1jR9grsO7XtHxIYczoCReJAW6dUqsiMXbNq7w7sF6LM3FLiwJDAlVEOWjyjkc7tpE8aIWjiymrFc+0rJXPtKyB/LxSkggHg9TslB4'
        b'qMHbY54TpDzIjbRhKVzHa7HBUQTdmXau0sscZdMLS/ANj5YEyC9Uxoi8ZRIWUf6owu7VOoOyVxlgIDUlC3ATv/7mC3emX49dkmHJ2W/K1mfIZ6RCeZxd1usuvH4y/4N3'
        b's27k3vcwM6gVaoWr+HgplIpx9HsEfdwV/L6HuO+ucFVq+VXx5MrbtAof8Zv/5UV/qXmL0k9hceGeVDBj0Paq+Yy9KordvS7OSNir5qGr1yU52WLPTk7u1SUnp2WZjNn2'
        b'3ORkg/Yvr9GgtvDcy8KfpbFwi7Lwx7UsPCcT857ma+PHtiyf/dKP+FYqtOJq57KflT1Viv4CJaEDxC9lv9CLXAg/VcYmyuqjqQVL47AiPkq1WcO8clULM+CWXWhaBTjc'
        b'o/XYExMnc0gF021RYishwePCB+Vhx4T+vHOuWxjem5CmckY8vgqXvog3m/U/16TOUDuTRlWxipJGNSWNKpE0qkXSqDqkdiaNhZQ0PlYMTRrFQ20DskZLzi69sS/PG5zR'
        b'Dc7ehmRnG/5CEmkx7babLTJ1yDVZKJHcJXOcviftBkf5+L7gT4wErqcZzbtMqy2WHEugIGaklvThc0POL2dX5odDFzFsYuRclBwxdIXDTcGzyTVZxh16s8xp03IsFpM1'
        b'Nyc7nZIgkVRaM3PsWek8SZL5jshunRnt8OnQajNf8pPsizJto352iM2eS1mVM8cSUqPkMID3COYTGf5CcqR5KjnSxNk56sBqbFmGpUsWPf1YX0lM4NpgaN4gn/DjN+Jj'
        b'omIpkrdAiW7RfHh1g/kn/nFK61IiUzwt94uU0H8yGCONWRlZqb9M2f7a4289/lYV3K5adKwpy/904+n2gqbIlmONx8LLDbWNx6bWHpmjYsFuuqs3/tGgtD0j7AVbp+sC'
        b'yRCwBMti7SHYtlO6xSnQqcZbC/fY+PMc3gEJ0aFrySMSgHQa3ny4NRFuq7Ohzt+gHGTl3+TfhKn36uQznE/cmZd0Z+ncYY0Sbsvi/cQNaXpd+zSq18WpG9KPePALf+hy'
        b'0PQqC4/LFu5HZDfhXzjBHw7wLy2jBvoX/rgJdh200BLxGtQPWqZYIxbgaftSkVrNIXg8FO7yo/JC6IAyuBis2hY9Fyp2w024Fka3H7qzVKz2xIYNUCATjE4Cz0W6PV4K'
        b'pqCM8+A4bMl7QSYsN+HyYt2e3byhmE3B63jO3yYSOk9KpyqseBdv43nv2WqmxGrFOCwcLxxW4FK4YJ1NwlLksM14BbqmzRGJ0QKsmKrbs0dL1IoouQvDs1kBzkdmtNCO'
        b'jf1ODo5iWRhDh30iZ69QsT8a2+1DAHYItAui6eDYHUSeU8GUUKEIGbFyFOYPco/9gIA/sUF4mjtI+cin0uGa4drvJtV/0U3uIDf5H9+ErYV9D0bW3+gkuEPh3f86Qv0G'
        b'4MgH/6/jxrQswZbVZHsaKQ5hkMslJy3NTv4wO+1pRvuw4uqECP1KCtwW7i9XUVxIs+VYCP3l2lOzzNZMIpSaJ3o6/fdKQpMWY9ZT9FaQaYYO4M3IN8UuHvkOTFy5ITCY'
        b'fq1axX+tjF8fTr+JvcAVs1eIhpUrA4OfojhgTYRDc4ZFvHyRQs65EucS1XTuuvNyhwiQ//xNQbGfYk7u07GQ//xt8XDQ5v2PAW0FGw5oexPQ5sEELqetGu4B8QGRpGbP'
        b'cMHEDMcEsEk/6MO8VSmMALnfsqlmibF3s1EeL6gi6VvKktWGDInSJyqwSoD0zWw+HtmMJ7FC+BP37YehFIqhmCngHlOOVrjhHewSdJT+XuoPVAspf0uJaUvYSb5alvdO'
        b'YuEsftQbzvCEZzhU4RV5/wxW+MyhNc6m+PNgNuHXDkFmncfIud9VLGcsNyWmc188J8Pd/MLlVknEDLfCCVk6MVwH9nCETqlaAj88uZ7gAdWCzOJs92fLFAGMjUiJKbOk'
        b'sQ3miC+Pa6zt1KS/WTi9ItwLZnms/nJabO/R2k33do9rfVfxba9x0Ve8osZP21Rc9dZPVdMWq1w+a4zckpf34Ycffl32aMYvj4SvOOrdsUcVdPhs1arXxv/U+8allJg/'
        b'FurKntfU3L652P+k4Y2gtvS3Z7guWKIP/KB9bdW73g1//CK5+N6V/+huPh6ujwr68VuRzarm+RXHbI/OdoWmdyRu/bKnrv6tmz/4Vdd+CMnr8v/9uG0br945lW2Y/OWB'
        b'zOzDH/vNw3K7wVUgI6jENjgb5MRUIwhqE6zCU9hm40+DrIK2sQOjuwjteNfqjO7YgOU28YRHG5YLx074Kj4ESsKoXwiWQMVoLIt2YeF4URt1CMskCuqCeopgodAVjWWG'
        b'PqJsLDjUrpgPxTa+BzNz8T4BNgUcgSNMuUcRQVn7A8EwXsBmKONvPoTFc5bdsPCQMjACGwT+giY4TXyV9oEvi57gF/ZImIhFI8KisTy6HyV6z+IP8HXuIKxvUMj47/rf'
        b'glwyJXGTAIsihkhIZsmE5DBjfQiLX5WElLwEgvJSqJUcOT1DHx/nxzJ6QMryBOf0qsh5D8hU/hpEUg2ASGP6sxdO+1cDspeTE4dmL3AV66CHAJIrnJfwVMLkkehQQZkL'
        b'lBvkw8hQtR7OY2nMrsABNXe4N2PQqxv9EIc/7EARXJmh7H9FQ/GNr2g4a+Jff2+QE1svneA3ZOkZIskW4XZgWft/G9YM64X7pDPYC2tlRg8nNGRh3+SFfXTfmNFDPZNF'
        b'tsLnsYbXS/kjvSehjhfGTmwVT4LkToM6MiU8HotliVgcoxy1mqykKBh64CrU0XcDSxjhAnexwcW83W+P0rqYBm377J+/SAkegA02vdZd1VijiJxzdVZI9LT04I1Bxjij'
        b'9s1ZoSmfpWz6js9br/2jkiWu9PT39TVohJmPhGKPAa5j25SQgbhgncEm2K5ZjbeczicAKkVNZx2ziUyybXLO4JqOj957inp7Uo6Nv65FQP2+i26oB8EqbFG7wtVxNg7m'
        b'51JWXTQPL0ZzlzSg7rMNyqWlKYc1Z5cdJlu/MY/oM+ap3IhFSURhGffEWFWyFDE8mFDIRmGEfIwPmYl1lDTCfPa510Az5GvWQOGO6G3QOoRfH3z0FwxM6WB/s4EVkoE1'
        b'D9LPxNwss83ab0Xy4IBMRc/vZliMO8RBwBCL6rNKo37usAB3UOeAlfFJcRvWbw7Wr4xcvTI6MSmWkG9EXHTyyvhVq4P1EStFe3JcUuyK1esN3wyHhzMeEZVxonhTbUTK'
        b'PnNWkVcEs8+nmy8fzuZvqAXx99tKYtZFPgEkWG2AJneoyxvpRtcoKMlj0KB1h+LlWGKfxum1QZF14GAyGuHu5sCNyfiKGi5FRJg3Fr+mtK6j3l3B//5FyouvtZF1tBeE'
        b'F00taj8VVd14Ovpy47HGgqn1DyOvFoYXNdW1l7SrAp55oy2/qWD31LSQNM+09kkJxyZMS8Tu/LypK2epduhY6bKRb5V/YlDbRD29fv3ooCelTpd1IZk5AkvDKfVup+Lj'
        b'ZaweGD6hfa+NF7wPHHZ5EgLnKgPwnBfehZMyftbv3xkdhg+hjsfoAC1z81FC43poGaS5w1uGOwEK6wDoPabPOMJdFR7CPLwkAPf5fzAQPiZgkIH0DjIQHsG9VLQrkcGB'
        b'3m5xTyD2OLivHrvH3SBDWRJcXUcRai2ci8cygtqVYXBc2tLEw+pMH7w0vCk5y3HiJcP+ctxfMyeOM7cNLccNDFmibpVt3CUQzTCRiuMZfuKWa6IbFNEGx44oaVRZRpuN'
        b'4EmakcLOYKIigBnTZcXvKWA2iFY/SPtrGE1isv+LEVQxrBNwjbM/x63iCBbBN4fQbwig4BhFMfQWXhCO5IuJE1hbaJpAMmtnbJegZb8XlPPA+kKEPIdcApdFWPXfHiCi'
        b'KtYdGhxYh0TVq3BfvhXqoWU3LKTE+pSsfZ55zPx65niNdTO1eP/hXF+s7f65jLafp2RmxBi/mxG8/nPyLY+/1VYVXttYYFS8t+JY3Ii3z8GDqvbH1wqnF2lunJ9w43wS'
        b'+RvFK+fvaG8sK+I1Ok/2Lz8Zp9m6z6AVNbpUOJksI/H5Fwbm8c5QnII35EHHRTgHXQOS+HhRBseK6AmQT6M0bEGc9hC8miYSdI8ZruSdEhT9RzFwFu+LLDucH5XxyP3M'
        b'swNjt3o7FC6XAOAKZegPhAuD+tGDAQDchA4bf/h/E4myWwRuAnE9/awIPqZAtRob4Gx6X9L+12qGHiKik15zqxGea1yf51rN/ZWHwl0pQ7uHwjJxgO/q1XFfl5xj4fnA'
        b'AB827ITEjW+/N+NUnh3kzb4zqGbI0VUoYd6u6CeiDls+eIV4f6NBFRe3xqBYY1DGrTG//u1fMeu/EdFP1/8p6cQPE0evG+P49cP75mnLl195/Hc/bds75t3H69a9r9as'
        b'/g+PnWM0l7Q/uVP1z7+6tO7GRyrvj3/Q8w/30x3fX2Td8b1b5x2LJ5332zM6+5WAE4vSnvno16/Mb2wPr/Rt9nnv0x9rb7/36e9TvzU+e9SqLervZ19479G58GXnzrx+'
        b'3LL22t9ltoz5c3d53urYdV//Mt/n5htqz+3FC912Nl0+P81zbkfxjHHvxehu3m4vvBqctiho0xuBG9/73sQPOir+NSvFv/7xW+PudpR73e0saPhl6oIDj99c9pU15QrO'
        b'WfSdqV7vLXrp8VF/v6ul2fsXfnv3+nM/m3Z94dsTvmep2P69lz5Rjv/svR9ND33vnbEPt30y0Tx7ondug6/H7Ndjs8Pf2tXw5Qc/mvTlI92P/d90/UPeaystS34Rfvnr'
        b'T27/rvB6WXjrrc+neuxsdbj9bslHi8ICZr3x5j9ujx/79YvzdmxYtdbjqvZUyK6kzK5Vr8196dttsdFv15021o01tUxY9NXMkH2mpgxjUNeh0PSm47ZT0xcXfXDoetHW'
        b'T9f85OM/vd723RnPnSv2n/TJ6w1b/v6tY3lv169/6z/HLr79s/Lf3s36TeLijzb/3eJryucf9yxvf2bpbyu7Xj+w7Gc/+3x+/KeHFq2Y+dK/FBXWvP/juVNa8uI3Jh4M'
        b'fPPi/bc+XW97tPh3F67d/qqorvmfJhz56s7Z9x6u+eBj3w8LssZ8Pyz1as+E1PeXftlAFs2Nz4/MuIOCnIIFwhXFQv7W78WRIjl4BqoThGXh0cQhlnWLoLUo2RfPUA5I'
        b'zLF61CB3gPkhsjDwCIv3YyklEeUh2hfhItNuV/pDOVwTqbVHKNYGhULB2hAsjoqJ0zAdtCtJY28RyBdQu3bW+uhMbOfumLpgWRTvckuJzVbzf/Ns0+D13zsK/UY6GguP'
        b'HsNehJdwTU7OyjGmJycLD/ELbrf+SqVSMVehF2eeo5Su6nEK+c9VoyQrltf/e/9claMU/J+rYoyK1x38nlPSCsaMdqfV+Cj8ApSKid70GalU8IDE+pydMjl5gI/z/P+X'
        b'uMIyqd8h8om405PnNR/OGHpAiw1R2AilUEkAliI0+f1KFziOhcxrgmrSKLho/vsPP1db67jbThsRUrrUHZaPKfx01/yeNWOC1d//9uh943VphiW3E9ZnTpz6WeEbP33m'
        b'QOLe1dfe/aru35atWf3b1/In19i+/ab+YUzJ2XfLl1++872A0M/u//nmW2+4ffnTS2/++gedI18PePFPY8/uG3nu+5Mnls0+texPz/z6H76janr/zz9666N52he+eGdk'
        b'TGbd7oifVwe1mrt/fvr+Fy/Oefu5Iiz2/+6Pxk96x/DTtB8aPGWCfgXz4fYS6BH/PUc8rYfXwHTQocRXFONFlxV4DwpesvAEop334ZWskfhABY14FWslldvmBVIcPCSQ'
        b'4ZE4OqCBeY1STZ7mJtDzeOyCe9FRcAW6YwNjXZhWrXSd5SLQA1baRgWt1TBFNNuPLVhLdnjcxgtTcUsINAzJkqAiLJp8QAE66H4ZVqrY89DuQlPfJDJ8b1bjlcUDB2k3'
        b'8GFaNn6VOhAewCnhV6ATilOxE8vI3sMCdzudykS4AbV2NRxTYqvAJnB9np2Dq2gsdUn2Z+oQBdzEhz42nrtH0ddmERAFQ05mfA0ToF4N16AwU/iWxfCqL5YaqJdUFQWe'
        b'mc+816mS4HKy4GTe2oS+9mC+NoHiFEzPv9zRsL3QJOhsywikVOViUHwwZXGlcpPwkRK79uKZQShl0v+MA/ofvBCq+gYPZs4225wejL/BxTx5XkPYTKVWcB/A8dkIkevw'
        b'bMddNY3nQGGWyf1eYEqvKsuU3avmhyG9GgHue9WEF2y96nRzGl0Jq2T3qqw2S68mNc9msvaqU3NysnpV5mxbryaDHCj9shizd9Boc3au3darSsu09KpyLOm92gxzFiGZ'
        b'XtUuY26var85t1djtKaZzb2qTNM+6kLk3c1Wc7bVZsxOM/VqBVJJE8e2plybtXfkrpz0RQuSZbU13bzDbOvVWTPNGbZkE0cQvZ6EODKN5mxTerJpX1qvW3KylbBYbnJy'
        b'r9aebSdg8cS7ycVOsvBjRguvF1j463oWXsu2cLlZ+AvsFu6vLLzIYuEJsoVjRIt4EZS/AmXhzy9beC3KwpXOwt9dsizgF36mYOGVBAt/d8syj1/4O1aWhfzCs1sL13YL'
        b'Ny3LIn7hJTfLrH5fybfDvd9X/nHVAF8p2r527XvCp3dEcrLzuzN4fT0xY/D/kKTPzrHpeZspPc7gyp+9Sc9JI5nQF2NWFrn8yU7V4ckx3Xcn8Vts1r1mW2avNisnzZhl'
        b'7fUYiNQsS/sEOOAi9W+J/G+YlnEdFaUztVKtcuU6Fj2GxyXFfwHmzNNA'
    ))))
