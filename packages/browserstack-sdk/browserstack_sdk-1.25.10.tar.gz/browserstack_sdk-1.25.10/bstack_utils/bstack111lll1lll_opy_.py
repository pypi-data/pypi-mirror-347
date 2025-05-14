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
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11lllll1111_opy_, bstack11lllll1l11_opy_, bstack11111ll1_opy_, bstack111l1lllll_opy_, bstack11l1ll1ll1l_opy_, bstack11l1l1l11l1_opy_, bstack11l1l1111ll_opy_, bstack1l11l1lll_opy_, bstack11l11llll1_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack111l11l1lll_opy_ import bstack111l11ll1l1_opy_
import bstack_utils.bstack1l1l11111l_opy_ as bstack11l11lll1l_opy_
from bstack_utils.bstack11l111llll_opy_ import bstack1l1ll11l1l_opy_
import bstack_utils.accessibility as bstack11l1ll1l1_opy_
from bstack_utils.bstack1l1l1ll111_opy_ import bstack1l1l1ll111_opy_
from bstack_utils.bstack111lllllll_opy_ import bstack111ll1ll1l_opy_
bstack1111l1lll1l_opy_ = bstack11111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡥࡲࡰࡱ࡫ࡣࡵࡱࡵ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧḍ")
logger = logging.getLogger(__name__)
class bstack1111lll11_opy_:
    bstack111l11l1lll_opy_ = None
    bs_config = None
    bstack1lll111l1l_opy_ = None
    @classmethod
    @bstack111l1lllll_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11ll1l1ll11_opy_, stage=STAGE.bstack1l1llll11_opy_)
    def launch(cls, bs_config, bstack1lll111l1l_opy_):
        cls.bs_config = bs_config
        cls.bstack1lll111l1l_opy_ = bstack1lll111l1l_opy_
        try:
            cls.bstack1111l1lllll_opy_()
            bstack11lll1ll11l_opy_ = bstack11lllll1111_opy_(bs_config)
            bstack11llll1llll_opy_ = bstack11lllll1l11_opy_(bs_config)
            data = bstack11l11lll1l_opy_.bstack1111ll11ll1_opy_(bs_config, bstack1lll111l1l_opy_)
            config = {
                bstack11111l_opy_ (u"ࠨࡣࡸࡸ࡭࠭Ḏ"): (bstack11lll1ll11l_opy_, bstack11llll1llll_opy_),
                bstack11111l_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪḏ"): cls.default_headers()
            }
            response = bstack11111ll1_opy_(bstack11111l_opy_ (u"ࠪࡔࡔ࡙ࡔࠨḐ"), cls.request_url(bstack11111l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠵࠳ࡧࡻࡩ࡭ࡦࡶࠫḑ")), data, config)
            if response.status_code != 200:
                bstack1lll11l1_opy_ = response.json()
                if bstack1lll11l1_opy_[bstack11111l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭Ḓ")] == False:
                    cls.bstack1111ll1l1ll_opy_(bstack1lll11l1_opy_)
                    return
                cls.bstack1111l1ll1l1_opy_(bstack1lll11l1_opy_[bstack11111l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ḓ")])
                cls.bstack1111l1ll1ll_opy_(bstack1lll11l1_opy_[bstack11111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧḔ")])
                return None
            bstack1111ll1111l_opy_ = cls.bstack1111ll111l1_opy_(response)
            return bstack1111ll1111l_opy_, response.json()
        except Exception as error:
            logger.error(bstack11111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡨࡵࡪ࡮ࡧࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࡿࢂࠨḕ").format(str(error)))
            return None
    @classmethod
    @bstack111l1lllll_opy_(class_method=True)
    def stop(cls, bstack1111ll11lll_opy_=None):
        if not bstack1l1ll11l1l_opy_.on() and not bstack11l1ll1l1_opy_.on():
            return
        if os.environ.get(bstack11111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭Ḗ")) == bstack11111l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣḗ") or os.environ.get(bstack11111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩḘ")) == bstack11111l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥḙ"):
            logger.error(bstack11111l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡲࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩḚ"))
            return {
                bstack11111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧḛ"): bstack11111l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧḜ"),
                bstack11111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪḝ"): bstack11111l_opy_ (u"ࠪࡘࡴࡱࡥ࡯࠱ࡥࡹ࡮ࡲࡤࡊࡆࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥ࠮ࠣࡦࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡲ࡯ࡧࡩࡶࠣ࡬ࡦࡼࡥࠡࡨࡤ࡭ࡱ࡫ࡤࠨḞ")
            }
        try:
            cls.bstack111l11l1lll_opy_.shutdown()
            data = {
                bstack11111l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩḟ"): bstack1l11l1lll_opy_()
            }
            if not bstack1111ll11lll_opy_ is None:
                data[bstack11111l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠩḠ")] = [{
                    bstack11111l_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭ḡ"): bstack11111l_opy_ (u"ࠧࡶࡵࡨࡶࡤࡱࡩ࡭࡮ࡨࡨࠬḢ"),
                    bstack11111l_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࠨḣ"): bstack1111ll11lll_opy_
                }]
            config = {
                bstack11111l_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪḤ"): cls.default_headers()
            }
            bstack11l1ll11ll1_opy_ = bstack11111l_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡳࡵࡱࡳࠫḥ").format(os.environ[bstack11111l_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤḦ")])
            bstack1111ll11111_opy_ = cls.request_url(bstack11l1ll11ll1_opy_)
            response = bstack11111ll1_opy_(bstack11111l_opy_ (u"ࠬࡖࡕࡕࠩḧ"), bstack1111ll11111_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11111l_opy_ (u"ࠨࡓࡵࡱࡳࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡴ࡯ࡵࠢࡲ࡯ࠧḨ"))
        except Exception as error:
            logger.error(bstack11111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡳࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡕࡧࡶࡸࡍࡻࡢ࠻࠼ࠣࠦḩ") + str(error))
            return {
                bstack11111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨḪ"): bstack11111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨḫ"),
                bstack11111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫḬ"): str(error)
            }
    @classmethod
    @bstack111l1lllll_opy_(class_method=True)
    def bstack1111ll111l1_opy_(cls, response):
        bstack1lll11l1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1111ll1111l_opy_ = {}
        if bstack1lll11l1_opy_.get(bstack11111l_opy_ (u"ࠫ࡯ࡽࡴࠨḭ")) is None:
            os.environ[bstack11111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩḮ")] = bstack11111l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫḯ")
        else:
            os.environ[bstack11111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫḰ")] = bstack1lll11l1_opy_.get(bstack11111l_opy_ (u"ࠨ࡬ࡺࡸࠬḱ"), bstack11111l_opy_ (u"ࠩࡱࡹࡱࡲࠧḲ"))
        os.environ[bstack11111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨḳ")] = bstack1lll11l1_opy_.get(bstack11111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭Ḵ"), bstack11111l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪḵ"))
        logger.info(bstack11111l_opy_ (u"࠭ࡔࡦࡵࡷ࡬ࡺࡨࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡹ࡬ࡸ࡭ࠦࡩࡥ࠼ࠣࠫḶ") + os.getenv(bstack11111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬḷ")));
        if bstack1l1ll11l1l_opy_.bstack1111lll1l11_opy_(cls.bs_config, cls.bstack1lll111l1l_opy_.get(bstack11111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩḸ"), bstack11111l_opy_ (u"ࠩࠪḹ"))) is True:
            bstack111l111l1ll_opy_, build_hashed_id, bstack1111ll1l11l_opy_ = cls.bstack1111ll1l111_opy_(bstack1lll11l1_opy_)
            if bstack111l111l1ll_opy_ != None and build_hashed_id != None:
                bstack1111ll1111l_opy_[bstack11111l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪḺ")] = {
                    bstack11111l_opy_ (u"ࠫ࡯ࡽࡴࡠࡶࡲ࡯ࡪࡴࠧḻ"): bstack111l111l1ll_opy_,
                    bstack11111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧḼ"): build_hashed_id,
                    bstack11111l_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪḽ"): bstack1111ll1l11l_opy_
                }
            else:
                bstack1111ll1111l_opy_[bstack11111l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧḾ")] = {}
        else:
            bstack1111ll1111l_opy_[bstack11111l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨḿ")] = {}
        bstack1111ll1ll1l_opy_, build_hashed_id = cls.bstack1111ll11l1l_opy_(bstack1lll11l1_opy_)
        if bstack1111ll1ll1l_opy_ != None and build_hashed_id != None:
            bstack1111ll1111l_opy_[bstack11111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩṀ")] = {
                bstack11111l_opy_ (u"ࠪࡥࡺࡺࡨࡠࡶࡲ࡯ࡪࡴࠧṁ"): bstack1111ll1ll1l_opy_,
                bstack11111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭Ṃ"): build_hashed_id,
            }
        else:
            bstack1111ll1111l_opy_[bstack11111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬṃ")] = {}
        if bstack1111ll1111l_opy_[bstack11111l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭Ṅ")].get(bstack11111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩṅ")) != None or bstack1111ll1111l_opy_[bstack11111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨṆ")].get(bstack11111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫṇ")) != None:
            cls.bstack1111lll11l1_opy_(bstack1lll11l1_opy_.get(bstack11111l_opy_ (u"ࠪ࡮ࡼࡺࠧṈ")), bstack1lll11l1_opy_.get(bstack11111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ṉ")))
        return bstack1111ll1111l_opy_
    @classmethod
    def bstack1111ll1l111_opy_(cls, bstack1lll11l1_opy_):
        if bstack1lll11l1_opy_.get(bstack11111l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬṊ")) == None:
            cls.bstack1111l1ll1l1_opy_()
            return [None, None, None]
        if bstack1lll11l1_opy_[bstack11111l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ṋ")][bstack11111l_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨṌ")] != True:
            cls.bstack1111l1ll1l1_opy_(bstack1lll11l1_opy_[bstack11111l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨṍ")])
            return [None, None, None]
        logger.debug(bstack11111l_opy_ (u"ࠩࡗࡩࡸࡺࠠࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭Ṏ"))
        os.environ[bstack11111l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩṏ")] = bstack11111l_opy_ (u"ࠫࡹࡸࡵࡦࠩṐ")
        if bstack1lll11l1_opy_.get(bstack11111l_opy_ (u"ࠬࡰࡷࡵࠩṑ")):
            os.environ[bstack11111l_opy_ (u"࠭ࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࡣࡋࡕࡒࡠࡅࡕࡅࡘࡎ࡟ࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠪṒ")] = json.dumps({
                bstack11111l_opy_ (u"ࠧࡶࡵࡨࡶࡳࡧ࡭ࡦࠩṓ"): bstack11lllll1111_opy_(cls.bs_config),
                bstack11111l_opy_ (u"ࠨࡲࡤࡷࡸࡽ࡯ࡳࡦࠪṔ"): bstack11lllll1l11_opy_(cls.bs_config)
            })
        if bstack1lll11l1_opy_.get(bstack11111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫṕ")):
            os.environ[bstack11111l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩṖ")] = bstack1lll11l1_opy_[bstack11111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ṗ")]
        if bstack1lll11l1_opy_[bstack11111l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬṘ")].get(bstack11111l_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧṙ"), {}).get(bstack11111l_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫṚ")):
            os.environ[bstack11111l_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩṛ")] = str(bstack1lll11l1_opy_[bstack11111l_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩṜ")][bstack11111l_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫṝ")][bstack11111l_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨṞ")])
        else:
            os.environ[bstack11111l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ṟ")] = bstack11111l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦṠ")
        return [bstack1lll11l1_opy_[bstack11111l_opy_ (u"ࠧ࡫ࡹࡷࠫṡ")], bstack1lll11l1_opy_[bstack11111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪṢ")], os.environ[bstack11111l_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪṣ")]]
    @classmethod
    def bstack1111ll11l1l_opy_(cls, bstack1lll11l1_opy_):
        if bstack1lll11l1_opy_.get(bstack11111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪṤ")) == None:
            cls.bstack1111l1ll1ll_opy_()
            return [None, None]
        if bstack1lll11l1_opy_[bstack11111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫṥ")][bstack11111l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭Ṧ")] != True:
            cls.bstack1111l1ll1ll_opy_(bstack1lll11l1_opy_[bstack11111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ṧ")])
            return [None, None]
        if bstack1lll11l1_opy_[bstack11111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧṨ")].get(bstack11111l_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩṩ")):
            logger.debug(bstack11111l_opy_ (u"ࠩࡗࡩࡸࡺࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭Ṫ"))
            parsed = json.loads(os.getenv(bstack11111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫṫ"), bstack11111l_opy_ (u"ࠫࢀࢃࠧṬ")))
            capabilities = bstack11l11lll1l_opy_.bstack1111lll11ll_opy_(bstack1lll11l1_opy_[bstack11111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬṭ")][bstack11111l_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧṮ")][bstack11111l_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ṯ")], bstack11111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭Ṱ"), bstack11111l_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨṱ"))
            bstack1111ll1ll1l_opy_ = capabilities[bstack11111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨṲ")]
            os.environ[bstack11111l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩṳ")] = bstack1111ll1ll1l_opy_
            if bstack11111l_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫ࠢṴ") in bstack1lll11l1_opy_ and bstack1lll11l1_opy_.get(bstack11111l_opy_ (u"ࠨࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠧṵ")) is None:
                parsed[bstack11111l_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨṶ")] = capabilities[bstack11111l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩṷ")]
            os.environ[bstack11111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪṸ")] = json.dumps(parsed)
            scripts = bstack11l11lll1l_opy_.bstack1111lll11ll_opy_(bstack1lll11l1_opy_[bstack11111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪṹ")][bstack11111l_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬṺ")][bstack11111l_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ṻ")], bstack11111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫṼ"), bstack11111l_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࠨṽ"))
            bstack1l1l1ll111_opy_.bstack11lll1111_opy_(scripts)
            commands = bstack1lll11l1_opy_[bstack11111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨṾ")][bstack11111l_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪṿ")][bstack11111l_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࡙ࡵࡗࡳࡣࡳࠫẀ")].get(bstack11111l_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ẁ"))
            bstack1l1l1ll111_opy_.bstack11lll1l1l11_opy_(commands)
            bstack1l1l1ll111_opy_.store()
        return [bstack1111ll1ll1l_opy_, bstack1lll11l1_opy_[bstack11111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧẂ")]]
    @classmethod
    def bstack1111l1ll1l1_opy_(cls, response=None):
        os.environ[bstack11111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫẃ")] = bstack11111l_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬẄ")
        os.environ[bstack11111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬẅ")] = bstack11111l_opy_ (u"ࠩࡱࡹࡱࡲࠧẆ")
        os.environ[bstack11111l_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩẇ")] = bstack11111l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪẈ")
        os.environ[bstack11111l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫẉ")] = bstack11111l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦẊ")
        os.environ[bstack11111l_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨẋ")] = bstack11111l_opy_ (u"ࠣࡰࡸࡰࡱࠨẌ")
        cls.bstack1111ll1l1ll_opy_(response, bstack11111l_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤẍ"))
        return [None, None, None]
    @classmethod
    def bstack1111l1ll1ll_opy_(cls, response=None):
        os.environ[bstack11111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨẎ")] = bstack11111l_opy_ (u"ࠫࡳࡻ࡬࡭ࠩẏ")
        os.environ[bstack11111l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪẐ")] = bstack11111l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫẑ")
        os.environ[bstack11111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫẒ")] = bstack11111l_opy_ (u"ࠨࡰࡸࡰࡱ࠭ẓ")
        cls.bstack1111ll1l1ll_opy_(response, bstack11111l_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤẔ"))
        return [None, None, None]
    @classmethod
    def bstack1111lll11l1_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack11111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧẕ")] = jwt
        os.environ[bstack11111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩẖ")] = build_hashed_id
    @classmethod
    def bstack1111ll1l1ll_opy_(cls, response=None, product=bstack11111l_opy_ (u"ࠧࠨẗ")):
        if response == None or response.get(bstack11111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭ẘ")) == None:
            logger.error(product + bstack11111l_opy_ (u"ࠢࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠤẙ"))
            return
        for error in response[bstack11111l_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨẚ")]:
            bstack11l11llll11_opy_ = error[bstack11111l_opy_ (u"ࠩ࡮ࡩࡾ࠭ẛ")]
            error_message = error[bstack11111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫẜ")]
            if error_message:
                if bstack11l11llll11_opy_ == bstack11111l_opy_ (u"ࠦࡊࡘࡒࡐࡔࡢࡅࡈࡉࡅࡔࡕࡢࡈࡊࡔࡉࡆࡆࠥẝ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11111l_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࠨẞ") + product + bstack11111l_opy_ (u"ࠨࠠࡧࡣ࡬ࡰࡪࡪࠠࡥࡷࡨࠤࡹࡵࠠࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦẟ"))
    @classmethod
    def bstack1111l1lllll_opy_(cls):
        if cls.bstack111l11l1lll_opy_ is not None:
            return
        cls.bstack111l11l1lll_opy_ = bstack111l11ll1l1_opy_(cls.bstack1111l1llll1_opy_)
        cls.bstack111l11l1lll_opy_.start()
    @classmethod
    def bstack111l1llll1_opy_(cls):
        if cls.bstack111l11l1lll_opy_ is None:
            return
        cls.bstack111l11l1lll_opy_.shutdown()
    @classmethod
    @bstack111l1lllll_opy_(class_method=True)
    def bstack1111l1llll1_opy_(cls, bstack111lll1l1l_opy_, event_url=bstack11111l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭Ạ")):
        config = {
            bstack11111l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩạ"): cls.default_headers()
        }
        logger.debug(bstack11111l_opy_ (u"ࠤࡳࡳࡸࡺ࡟ࡥࡣࡷࡥ࠿ࠦࡓࡦࡰࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡶࡨࡷࡹ࡮ࡵࡣࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࡸࠦࡻࡾࠤẢ").format(bstack11111l_opy_ (u"ࠪ࠰ࠥ࠭ả").join([event[bstack11111l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨẤ")] for event in bstack111lll1l1l_opy_])))
        response = bstack11111ll1_opy_(bstack11111l_opy_ (u"ࠬࡖࡏࡔࡖࠪấ"), cls.request_url(event_url), bstack111lll1l1l_opy_, config)
        bstack11llll1l1l1_opy_ = response.json()
    @classmethod
    def bstack1l1l1l1l1_opy_(cls, bstack111lll1l1l_opy_, event_url=bstack11111l_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬẦ")):
        logger.debug(bstack11111l_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡆࡺࡴࡦ࡯ࡳࡸ࡮ࡴࡧࠡࡶࡲࠤࡦࡪࡤࠡࡦࡤࡸࡦࠦࡴࡰࠢࡥࡥࡹࡩࡨࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢầ").format(bstack111lll1l1l_opy_[bstack11111l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬẨ")]))
        if not bstack11l11lll1l_opy_.bstack1111ll1l1l1_opy_(bstack111lll1l1l_opy_[bstack11111l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ẩ")]):
            logger.debug(bstack11111l_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡏࡱࡷࠤࡦࡪࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣẪ").format(bstack111lll1l1l_opy_[bstack11111l_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨẫ")]))
            return
        bstack1llll111l_opy_ = bstack11l11lll1l_opy_.bstack1111ll1lll1_opy_(bstack111lll1l1l_opy_[bstack11111l_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩẬ")], bstack111lll1l1l_opy_.get(bstack11111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨậ")))
        if bstack1llll111l_opy_ != None:
            if bstack111lll1l1l_opy_.get(bstack11111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩẮ")) != None:
                bstack111lll1l1l_opy_[bstack11111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪắ")][bstack11111l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧẰ")] = bstack1llll111l_opy_
            else:
                bstack111lll1l1l_opy_[bstack11111l_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨằ")] = bstack1llll111l_opy_
        if event_url == bstack11111l_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪẲ"):
            cls.bstack1111l1lllll_opy_()
            logger.debug(bstack11111l_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡄࡨࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡵࡱࠣࡦࡦࡺࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣẳ").format(bstack111lll1l1l_opy_[bstack11111l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪẴ")]))
            cls.bstack111l11l1lll_opy_.add(bstack111lll1l1l_opy_)
        elif event_url == bstack11111l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬẵ"):
            cls.bstack1111l1llll1_opy_([bstack111lll1l1l_opy_], event_url)
    @classmethod
    @bstack111l1lllll_opy_(class_method=True)
    def bstack1l1lll1111_opy_(cls, logs):
        bstack1111ll1ll11_opy_ = []
        for log in logs:
            bstack1111ll111ll_opy_ = {
                bstack11111l_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭Ặ"): bstack11111l_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡍࡑࡊࠫặ"),
                bstack11111l_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩẸ"): log[bstack11111l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪẹ")],
                bstack11111l_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨẺ"): log[bstack11111l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩẻ")],
                bstack11111l_opy_ (u"ࠧࡩࡶࡷࡴࡤࡸࡥࡴࡲࡲࡲࡸ࡫ࠧẼ"): {},
                bstack11111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩẽ"): log[bstack11111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪẾ")],
            }
            if bstack11111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪế") in log:
                bstack1111ll111ll_opy_[bstack11111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫỀ")] = log[bstack11111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬề")]
            elif bstack11111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭Ể") in log:
                bstack1111ll111ll_opy_[bstack11111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧể")] = log[bstack11111l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨỄ")]
            bstack1111ll1ll11_opy_.append(bstack1111ll111ll_opy_)
        cls.bstack1l1l1l1l1_opy_({
            bstack11111l_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ễ"): bstack11111l_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧỆ"),
            bstack11111l_opy_ (u"ࠫࡱࡵࡧࡴࠩệ"): bstack1111ll1ll11_opy_
        })
    @classmethod
    @bstack111l1lllll_opy_(class_method=True)
    def bstack1111ll1llll_opy_(cls, steps):
        bstack1111l1lll11_opy_ = []
        for step in steps:
            bstack1111ll11l11_opy_ = {
                bstack11111l_opy_ (u"ࠬࡱࡩ࡯ࡦࠪỈ"): bstack11111l_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘ࡚ࡅࡑࠩỉ"),
                bstack11111l_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭Ị"): step[bstack11111l_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧị")],
                bstack11111l_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬỌ"): step[bstack11111l_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭ọ")],
                bstack11111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬỎ"): step[bstack11111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ỏ")],
                bstack11111l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨỐ"): step[bstack11111l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩố")]
            }
            if bstack11111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨỒ") in step:
                bstack1111ll11l11_opy_[bstack11111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩồ")] = step[bstack11111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪỔ")]
            elif bstack11111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫổ") in step:
                bstack1111ll11l11_opy_[bstack11111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬỖ")] = step[bstack11111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ỗ")]
            bstack1111l1lll11_opy_.append(bstack1111ll11l11_opy_)
        cls.bstack1l1l1l1l1_opy_({
            bstack11111l_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫỘ"): bstack11111l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬộ"),
            bstack11111l_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧỚ"): bstack1111l1lll11_opy_
        })
    @classmethod
    @bstack111l1lllll_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack1l11111ll1_opy_, stage=STAGE.bstack1l1llll11_opy_)
    def bstack1ll1ll11_opy_(cls, screenshot):
        cls.bstack1l1l1l1l1_opy_({
            bstack11111l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧớ"): bstack11111l_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨỜ"),
            bstack11111l_opy_ (u"ࠬࡲ࡯ࡨࡵࠪờ"): [{
                bstack11111l_opy_ (u"࠭࡫ࡪࡰࡧࠫỞ"): bstack11111l_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࠩở"),
                bstack11111l_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫỠ"): datetime.datetime.utcnow().isoformat() + bstack11111l_opy_ (u"ࠩ࡝ࠫỡ"),
                bstack11111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫỢ"): screenshot[bstack11111l_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪợ")],
                bstack11111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬỤ"): screenshot[bstack11111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ụ")]
            }]
        }, event_url=bstack11111l_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬỦ"))
    @classmethod
    @bstack111l1lllll_opy_(class_method=True)
    def bstack111lllll1_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l1l1l1l1_opy_({
            bstack11111l_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬủ"): bstack11111l_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭Ứ"),
            bstack11111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬứ"): {
                bstack11111l_opy_ (u"ࠦࡺࡻࡩࡥࠤỪ"): cls.current_test_uuid(),
                bstack11111l_opy_ (u"ࠧ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠦừ"): cls.bstack111llllll1_opy_(driver)
            }
        })
    @classmethod
    def bstack111lllll1l_opy_(cls, event: str, bstack111lll1l1l_opy_: bstack111ll1ll1l_opy_):
        bstack111ll1ll11_opy_ = {
            bstack11111l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪỬ"): event,
            bstack111lll1l1l_opy_.bstack111ll11l1l_opy_(): bstack111lll1l1l_opy_.bstack111l1l1l1l_opy_(event)
        }
        cls.bstack1l1l1l1l1_opy_(bstack111ll1ll11_opy_)
        result = getattr(bstack111lll1l1l_opy_, bstack11111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧử"), None)
        if event == bstack11111l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩỮ"):
            threading.current_thread().bstackTestMeta = {bstack11111l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩữ"): bstack11111l_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫỰ")}
        elif event == bstack11111l_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ự"):
            threading.current_thread().bstackTestMeta = {bstack11111l_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬỲ"): getattr(result, bstack11111l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ỳ"), bstack11111l_opy_ (u"ࠧࠨỴ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack11111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬỵ"), None) is None or os.environ[bstack11111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭Ỷ")] == bstack11111l_opy_ (u"ࠥࡲࡺࡲ࡬ࠣỷ")) and (os.environ.get(bstack11111l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩỸ"), None) is None or os.environ[bstack11111l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪỹ")] == bstack11111l_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦỺ")):
            return False
        return True
    @staticmethod
    def bstack1111lll111l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1111lll11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack11111l_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ỻ"): bstack11111l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫỼ"),
            bstack11111l_opy_ (u"࡛ࠩ࠱ࡇ࡙ࡔࡂࡅࡎ࠱࡙ࡋࡓࡕࡑࡓࡗࠬỽ"): bstack11111l_opy_ (u"ࠪࡸࡷࡻࡥࠨỾ")
        }
        if os.environ.get(bstack11111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨỿ"), None):
            headers[bstack11111l_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬἀ")] = bstack11111l_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩἁ").format(os.environ[bstack11111l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠦἂ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack11111l_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧἃ").format(bstack1111l1lll1l_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ἄ"), None)
    @staticmethod
    def bstack111llllll1_opy_(driver):
        return {
            bstack11l1ll1ll1l_opy_(): bstack11l1l1l11l1_opy_(driver)
        }
    @staticmethod
    def bstack1111lll1111_opy_(exception_info, report):
        return [{bstack11111l_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ἅ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1111ll111l_opy_(typename):
        if bstack11111l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢἆ") in typename:
            return bstack11111l_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨἇ")
        return bstack11111l_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢἈ")