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
from browserstack_sdk.bstack1l11l1ll1_opy_ import bstack1llllll11_opy_
from browserstack_sdk.bstack111l11l111_opy_ import RobotHandler
def bstack1llll1l1_opy_(framework):
    if framework.lower() == bstack11111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧᦦ"):
        return bstack1llllll11_opy_.version()
    elif framework.lower() == bstack11111l_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧᦧ"):
        return RobotHandler.version()
    elif framework.lower() == bstack11111l_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩᦨ"):
        import behave
        return behave.__version__
    else:
        return bstack11111l_opy_ (u"ࠪࡹࡳࡱ࡮ࡰࡹࡱࠫᦩ")
def bstack1ll111lll_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack11111l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ᦪ"))
        framework_version.append(importlib.metadata.version(bstack11111l_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᦫ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack11111l_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪ᦬"))
        framework_version.append(importlib.metadata.version(bstack11111l_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ᦭")))
    except:
        pass
    return {
        bstack11111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭᦮"): bstack11111l_opy_ (u"ࠩࡢࠫ᦯").join(framework_name),
        bstack11111l_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࠫᦰ"): bstack11111l_opy_ (u"ࠫࡤ࠭ᦱ").join(framework_version)
    }