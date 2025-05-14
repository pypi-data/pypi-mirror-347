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
import logging
from functools import wraps
from typing import Optional
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.bstack11ll1ll1l1_opy_ import get_logger
from bstack_utils.bstack1lll11ll11_opy_ import bstack1lllll11lll_opy_
bstack1lll11ll11_opy_ = bstack1lllll11lll_opy_()
logger = get_logger(__name__)
def measure(event_name: EVENTS, stage: STAGE, hook_type: Optional[str] = None, bstack1l1ll1ll_opy_: Optional[str] = None):
    bstack11111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡇࡩࡨࡵࡲࡢࡶࡲࡶࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡺࡨࡦࠢࡶࡸࡦࡸࡴࠡࡶ࡬ࡱࡪࠦ࡯ࡧࠢࡤࠤ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࡡ࡭ࡱࡱ࡫ࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࠢࡱࡥࡲ࡫ࠠࡢࡰࡧࠤࡸࡺࡡࡨࡧ࠱ࠎࠥࠦࠠࠡࠤࠥࠦ᱁")
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            label: str = event_name.value
            bstack1ll1ll111ll_opy_: str = bstack1lll11ll11_opy_.bstack11llll1lll1_opy_(label)
            start_mark: str = label + bstack11111l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ᱂")
            end_mark: str = label + bstack11111l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ᱃")
            result = None
            try:
                if stage.value == STAGE.bstack1ll111l1_opy_.value:
                    bstack1lll11ll11_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                elif stage.value == STAGE.END.value:
                    result = func(*args, **kwargs)
                    bstack1lll11ll11_opy_.end(label, start_mark, end_mark, status=True, failure=None,hook_type=hook_type,test_name=bstack1l1ll1ll_opy_)
                elif stage.value == STAGE.bstack1l1llll11_opy_.value:
                    start_mark: str = bstack1ll1ll111ll_opy_ + bstack11111l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ᱄")
                    end_mark: str = bstack1ll1ll111ll_opy_ + bstack11111l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ᱅")
                    bstack1lll11ll11_opy_.mark(start_mark)
                    result = func(*args, **kwargs)
                    bstack1lll11ll11_opy_.end(label, start_mark, end_mark, status=True, failure=None, hook_type=hook_type,test_name=bstack1l1ll1ll_opy_)
            except Exception as e:
                bstack1lll11ll11_opy_.end(label, start_mark, end_mark, status=False, failure=str(e), hook_type=hook_type,
                                       test_name=bstack1l1ll1ll_opy_)
            return result
        return wrapper
    return decorator