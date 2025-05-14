# coding: UTF-8
import sys
bstack111l1_opy_ = sys.version_info [0] == 2
bstack11l11ll_opy_ = 2048
bstack1l1l1_opy_ = 7
def bstack11111l_opy_ (bstack11l11_opy_):
    global bstack11l1111_opy_
    bstack1l1lll_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111_opy_ = bstack11l11_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1lll_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l1llll_opy_] + bstack1l111_opy_ [bstack1l1llll_opy_:]
    if bstack111l1_opy_:
        bstack1l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11ll_opy_ - (bstack11ll111_opy_ + bstack1l1lll_opy_) % bstack1l1l1_opy_) for bstack11ll111_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1l1ll1_opy_ = str () .join ([chr (ord (char) - bstack11l11ll_opy_ - (bstack11ll111_opy_ + bstack1l1lll_opy_) % bstack1l1l1_opy_) for bstack11ll111_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1l1ll1_opy_)
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l1111l1l1_opy_
bstack1l11l11ll1_opy_ = Config.bstack1l11l111_opy_()
def bstack111l1l1l1ll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111l1l1l1l1_opy_(bstack111l1l1llll_opy_, bstack111l1l1ll1l_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111l1l1llll_opy_):
        with open(bstack111l1l1llll_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111l1l1l1ll_opy_(bstack111l1l1llll_opy_):
        pac = get_pac(url=bstack111l1l1llll_opy_)
    else:
        raise Exception(bstack11111l_opy_ (u"ࠬࡖࡡࡤࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠬᴫ").format(bstack111l1l1llll_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack11111l_opy_ (u"ࠨ࠸࠯࠺࠱࠼࠳࠾ࠢᴬ"), 80))
        bstack111l1l1ll11_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111l1l1ll11_opy_ = bstack11111l_opy_ (u"ࠧ࠱࠰࠳࠲࠵࠴࠰ࠨᴭ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111l1l1ll1l_opy_, bstack111l1l1ll11_opy_)
    return proxy_url
def bstack1ll11ll11_opy_(config):
    return bstack11111l_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᴮ") in config or bstack11111l_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᴯ") in config
def bstack1l11ll11ll_opy_(config):
    if not bstack1ll11ll11_opy_(config):
        return
    if config.get(bstack11111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᴰ")):
        return config.get(bstack11111l_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᴱ"))
    if config.get(bstack11111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᴲ")):
        return config.get(bstack11111l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᴳ"))
def bstack1lll111l1_opy_(config, bstack111l1l1ll1l_opy_):
    proxy = bstack1l11ll11ll_opy_(config)
    proxies = {}
    if config.get(bstack11111l_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᴴ")) or config.get(bstack11111l_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᴵ")):
        if proxy.endswith(bstack11111l_opy_ (u"ࠩ࠱ࡴࡦࡩࠧᴶ")):
            proxies = bstack1l111lll1_opy_(proxy, bstack111l1l1ll1l_opy_)
        else:
            proxies = {
                bstack11111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᴷ"): proxy
            }
    bstack1l11l11ll1_opy_.bstack1111ll11_opy_(bstack11111l_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫᴸ"), proxies)
    return proxies
def bstack1l111lll1_opy_(bstack111l1l1llll_opy_, bstack111l1l1ll1l_opy_):
    proxies = {}
    global bstack111l1l1lll1_opy_
    if bstack11111l_opy_ (u"ࠬࡖࡁࡄࡡࡓࡖࡔ࡞࡙ࠨᴹ") in globals():
        return bstack111l1l1lll1_opy_
    try:
        proxy = bstack111l1l1l1l1_opy_(bstack111l1l1llll_opy_, bstack111l1l1ll1l_opy_)
        if bstack11111l_opy_ (u"ࠨࡄࡊࡔࡈࡇ࡙ࠨᴺ") in proxy:
            proxies = {}
        elif bstack11111l_opy_ (u"ࠢࡉࡖࡗࡔࠧᴻ") in proxy or bstack11111l_opy_ (u"ࠣࡊࡗࡘࡕ࡙ࠢᴼ") in proxy or bstack11111l_opy_ (u"ࠤࡖࡓࡈࡑࡓࠣᴽ") in proxy:
            bstack111l1l1l11l_opy_ = proxy.split(bstack11111l_opy_ (u"ࠥࠤࠧᴾ"))
            if bstack11111l_opy_ (u"ࠦ࠿࠵࠯ࠣᴿ") in bstack11111l_opy_ (u"ࠧࠨᵀ").join(bstack111l1l1l11l_opy_[1:]):
                proxies = {
                    bstack11111l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᵁ"): bstack11111l_opy_ (u"ࠢࠣᵂ").join(bstack111l1l1l11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11111l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᵃ"): str(bstack111l1l1l11l_opy_[0]).lower() + bstack11111l_opy_ (u"ࠤ࠽࠳࠴ࠨᵄ") + bstack11111l_opy_ (u"ࠥࠦᵅ").join(bstack111l1l1l11l_opy_[1:])
                }
        elif bstack11111l_opy_ (u"ࠦࡕࡘࡏ࡙࡛ࠥᵆ") in proxy:
            bstack111l1l1l11l_opy_ = proxy.split(bstack11111l_opy_ (u"ࠧࠦࠢᵇ"))
            if bstack11111l_opy_ (u"ࠨ࠺࠰࠱ࠥᵈ") in bstack11111l_opy_ (u"ࠢࠣᵉ").join(bstack111l1l1l11l_opy_[1:]):
                proxies = {
                    bstack11111l_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᵊ"): bstack11111l_opy_ (u"ࠤࠥᵋ").join(bstack111l1l1l11l_opy_[1:])
                }
            else:
                proxies = {
                    bstack11111l_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᵌ"): bstack11111l_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᵍ") + bstack11111l_opy_ (u"ࠧࠨᵎ").join(bstack111l1l1l11l_opy_[1:])
                }
        else:
            proxies = {
                bstack11111l_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᵏ"): proxy
            }
    except Exception as e:
        print(bstack11111l_opy_ (u"ࠢࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦᵐ"), bstack11l1111l1l1_opy_.format(bstack111l1l1llll_opy_, str(e)))
    bstack111l1l1lll1_opy_ = proxies
    return proxies