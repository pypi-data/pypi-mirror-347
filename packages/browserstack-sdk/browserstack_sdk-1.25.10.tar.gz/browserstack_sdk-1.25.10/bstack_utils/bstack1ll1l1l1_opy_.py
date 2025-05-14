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
import re
from bstack_utils.bstack1l1111ll11_opy_ import bstack111l1l1111l_opy_
def bstack111l11lllll_opy_(fixture_name):
    if fixture_name.startswith(bstack11111l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᵑ")):
        return bstack11111l_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᵒ")
    elif fixture_name.startswith(bstack11111l_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᵓ")):
        return bstack11111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪᵔ")
    elif fixture_name.startswith(bstack11111l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᵕ")):
        return bstack11111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᵖ")
    elif fixture_name.startswith(bstack11111l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᵗ")):
        return bstack11111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪᵘ")
def bstack111l11llll1_opy_(fixture_name):
    return bool(re.match(bstack11111l_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࡾࡰࡳࡩࡻ࡬ࡦࠫࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧᵙ"), fixture_name))
def bstack111l11lll1l_opy_(fixture_name):
    return bool(re.match(bstack11111l_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᵚ"), fixture_name))
def bstack111l1l11l1l_opy_(fixture_name):
    return bool(re.match(bstack11111l_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᵛ"), fixture_name))
def bstack111l1l11ll1_opy_(fixture_name):
    if fixture_name.startswith(bstack11111l_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᵜ")):
        return bstack11111l_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᵝ"), bstack11111l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᵞ")
    elif fixture_name.startswith(bstack11111l_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᵟ")):
        return bstack11111l_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨᵠ"), bstack11111l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧᵡ")
    elif fixture_name.startswith(bstack11111l_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᵢ")):
        return bstack11111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᵣ"), bstack11111l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᵤ")
    elif fixture_name.startswith(bstack11111l_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᵥ")):
        return bstack11111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪᵦ"), bstack11111l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᵧ")
    return None, None
def bstack111l1l11111_opy_(hook_name):
    if hook_name in [bstack11111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᵨ"), bstack11111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᵩ")]:
        return hook_name.capitalize()
    return hook_name
def bstack111l11ll1ll_opy_(hook_name):
    if hook_name in [bstack11111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᵪ"), bstack11111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᵫ")]:
        return bstack11111l_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᵬ")
    elif hook_name in [bstack11111l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧᵭ"), bstack11111l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᵮ")]:
        return bstack11111l_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧᵯ")
    elif hook_name in [bstack11111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᵰ"), bstack11111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᵱ")]:
        return bstack11111l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᵲ")
    elif hook_name in [bstack11111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩᵳ"), bstack11111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩᵴ")]:
        return bstack11111l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᵵ")
    return hook_name
def bstack111l11lll11_opy_(node, scenario):
    if hasattr(node, bstack11111l_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᵶ")):
        parts = node.nodeid.rsplit(bstack11111l_opy_ (u"ࠦࡠࠨᵷ"))
        params = parts[-1]
        return bstack11111l_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧᵸ").format(scenario.name, params)
    return scenario.name
def bstack111l1l111l1_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack11111l_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᵹ")):
            examples = list(node.callspec.params[bstack11111l_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭ᵺ")].values())
        return examples
    except:
        return []
def bstack111l1l111ll_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack111l1l1l111_opy_(report):
    try:
        status = bstack11111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᵻ")
        if report.passed or (report.failed and hasattr(report, bstack11111l_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᵼ"))):
            status = bstack11111l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᵽ")
        elif report.skipped:
            status = bstack11111l_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᵾ")
        bstack111l1l1111l_opy_(status)
    except:
        pass
def bstack1lllll1l1_opy_(status):
    try:
        bstack111l1l11lll_opy_ = bstack11111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᵿ")
        if status == bstack11111l_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᶀ"):
            bstack111l1l11lll_opy_ = bstack11111l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᶁ")
        elif status == bstack11111l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᶂ"):
            bstack111l1l11lll_opy_ = bstack11111l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᶃ")
        bstack111l1l1111l_opy_(bstack111l1l11lll_opy_)
    except:
        pass
def bstack111l1l11l11_opy_(item=None, report=None, summary=None, extra=None):
    return