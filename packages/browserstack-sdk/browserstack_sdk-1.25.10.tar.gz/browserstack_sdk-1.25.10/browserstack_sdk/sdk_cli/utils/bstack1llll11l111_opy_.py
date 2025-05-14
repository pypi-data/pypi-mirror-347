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
from typing import List, Dict, Any
from bstack_utils.bstack11ll1ll1l1_opy_ import get_logger
logger = get_logger(__name__)
class bstack1lll1111l11_opy_:
    bstack11111l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࡃࡶࡵࡷࡳࡲ࡚ࡡࡨࡏࡤࡲࡦ࡭ࡥࡳࠢࡳࡶࡴࡼࡩࡥࡧࡶࠤࡺࡺࡩ࡭࡫ࡷࡽࠥࡳࡥࡵࡪࡲࡨࡸࠦࡴࡰࠢࡶࡩࡹࠦࡡ࡯ࡦࠣࡶࡪࡺࡲࡪࡧࡹࡩࠥࡩࡵࡴࡶࡲࡱࠥࡺࡡࡨࠢࡰࡩࡹࡧࡤࡢࡶࡤ࠲ࠏࠦࠠࠡࠢࡌࡸࠥࡳࡡࡪࡰࡷࡥ࡮ࡴࡳࠡࡶࡺࡳࠥࡹࡥࡱࡣࡵࡥࡹ࡫ࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶ࡮࡫ࡳࠡࡨࡲࡶࠥࡺࡥࡴࡶࠣࡰࡪࡼࡥ࡭ࠢࡤࡲࡩࠦࡢࡶ࡫࡯ࡨࠥࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࡴ࠰ࠍࠤࠥࠦࠠࡆࡣࡦ࡬ࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡦࡰࡷࡶࡾࠦࡩࡴࠢࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡹࡵࠠࡣࡧࠣࡷࡹࡸࡵࡤࡶࡸࡶࡪࡪࠠࡢࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࡰ࡫ࡹ࠻ࠢࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡩ࡭ࡪࡲࡤࡠࡶࡼࡴࡪࠨ࠺ࠡࠤࡰࡹࡱࡺࡩࡠࡦࡵࡳࡵࡪ࡯ࡸࡰࠥ࠰ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡺࡦࡲࡵࡦࡵࠥ࠾ࠥࡡ࡬ࡪࡵࡷࠤࡴ࡬ࠠࡵࡣࡪࠤࡻࡧ࡬ࡶࡧࡶࡡࠏࠦࠠࠡࠢࠣࠤࠥࢃࠊࠡࠢࠣࠤࠧࠨࠢᔩ")
    _1l11111l1ll_opy_: Dict[str, Dict[str, Any]] = {}
    _1l11111lll1_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack1l11lll1l_opy_: str, key_value: str, bstack1l1111l1111_opy_: bool = False) -> None:
        if not bstack1l11lll1l_opy_ or not key_value or bstack1l11lll1l_opy_.strip() == bstack11111l_opy_ (u"ࠢࠣᔪ") or key_value.strip() == bstack11111l_opy_ (u"ࠣࠤᔫ"):
            logger.error(bstack11111l_opy_ (u"ࠤ࡮ࡩࡾࡥ࡮ࡢ࡯ࡨࠤࡦࡴࡤࠡ࡭ࡨࡽࡤࡼࡡ࡭ࡷࡨࠤࡲࡻࡳࡵࠢࡥࡩࠥࡴ࡯࡯࠯ࡱࡹࡱࡲࠠࡢࡰࡧࠤࡳࡵ࡮࠮ࡧࡰࡴࡹࡿࠢᔬ"))
        values: List[str] = bstack1lll1111l11_opy_.bstack1l11111llll_opy_(key_value)
        bstack1l11111ll1l_opy_ = {bstack11111l_opy_ (u"ࠥࡪ࡮࡫࡬ࡥࡡࡷࡽࡵ࡫ࠢᔭ"): bstack11111l_opy_ (u"ࠦࡲࡻ࡬ࡵ࡫ࡢࡨࡷࡵࡰࡥࡱࡺࡲࠧᔮ"), bstack11111l_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࡷࠧᔯ"): values}
        bstack1l1111l11ll_opy_ = bstack1lll1111l11_opy_._1l11111lll1_opy_ if bstack1l1111l1111_opy_ else bstack1lll1111l11_opy_._1l11111l1ll_opy_
        if bstack1l11lll1l_opy_ in bstack1l1111l11ll_opy_:
            bstack1l1111l111l_opy_ = bstack1l1111l11ll_opy_[bstack1l11lll1l_opy_]
            bstack1l11111ll11_opy_ = bstack1l1111l111l_opy_.get(bstack11111l_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࡸࠨᔰ"), [])
            for val in values:
                if val not in bstack1l11111ll11_opy_:
                    bstack1l11111ll11_opy_.append(val)
            bstack1l1111l111l_opy_[bstack11111l_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࡹࠢᔱ")] = bstack1l11111ll11_opy_
        else:
            bstack1l1111l11ll_opy_[bstack1l11lll1l_opy_] = bstack1l11111ll1l_opy_
    @staticmethod
    def bstack1l11l1ll1ll_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1lll1111l11_opy_._1l11111l1ll_opy_
    @staticmethod
    def bstack1l1111l1l11_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1lll1111l11_opy_._1l11111lll1_opy_
    @staticmethod
    def bstack1l11111llll_opy_(bstack1l1111l11l1_opy_: str) -> List[str]:
        bstack11111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡰ࡭࡫ࡷࡷࠥࡺࡨࡦࠢ࡬ࡲࡵࡻࡴࠡࡵࡷࡶ࡮ࡴࡧࠡࡤࡼࠤࡨࡵ࡭࡮ࡣࡶࠤࡼ࡮ࡩ࡭ࡧࠣࡶࡪࡹࡰࡦࡥࡷ࡭ࡳ࡭ࠠࡥࡱࡸࡦࡱ࡫࠭ࡲࡷࡲࡸࡪࡪࠠࡴࡷࡥࡷࡹࡸࡩ࡯ࡩࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡩࡽࡧ࡭ࡱ࡮ࡨ࠾ࠥ࠭ࡡ࠭ࠢࠥࡦ࠱ࡩࠢ࠭ࠢࡧࠫࠥ࠳࠾ࠡ࡝ࠪࡥࠬ࠲ࠠࠨࡤ࠯ࡧࠬ࠲ࠠࠨࡦࠪࡡࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᔲ")
        pattern = re.compile(bstack11111l_opy_ (u"ࡴࠪࠦ࠭ࡡ࡞ࠣ࡟࠭࠭ࠧࢂࠨ࡜ࡠ࠯ࡡ࠰࠯ࠧᔳ"))
        result = []
        for match in pattern.finditer(bstack1l1111l11l1_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack11111l_opy_ (u"࡙ࠥࡹ࡯࡬ࡪࡶࡼࠤࡨࡲࡡࡴࡵࠣࡷ࡭ࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣ࡭ࡳࡹࡴࡢࡰࡷ࡭ࡦࡺࡥࡥࠤᔴ"))