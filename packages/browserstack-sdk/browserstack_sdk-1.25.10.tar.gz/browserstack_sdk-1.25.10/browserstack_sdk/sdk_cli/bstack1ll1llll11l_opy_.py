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
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack11111l1111_opy_ import (
    bstack1111111l1l_opy_,
    bstack1111l11l11_opy_,
    bstack11111llll1_opy_,
    bstack111111ll1l_opy_,
    bstack11111l11l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll111111l_opy_ import bstack1lll11l11l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_, bstack1lll1ll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l11l11_opy_ import bstack1ll11l1l11l_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1ll111l1lll_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1llll1llll1_opy_(bstack1ll11l1l11l_opy_):
    bstack1l1l1ll11l1_opy_ = bstack11111l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡩࡸࡩࡷࡧࡵࡷࠧጎ")
    bstack1ll111llll1_opy_ = bstack11111l_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨጏ")
    bstack1l1l1ll1ll1_opy_ = bstack11111l_opy_ (u"ࠣࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥጐ")
    bstack1l1l1l1lll1_opy_ = bstack11111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤ጑")
    bstack1l1l1lll1l1_opy_ = bstack11111l_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡡࡵࡩ࡫ࡹࠢጒ")
    bstack1ll1111llll_opy_ = bstack11111l_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡦࡶࡪࡧࡴࡦࡦࠥጓ")
    bstack1l1l1lll11l_opy_ = bstack11111l_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠣጔ")
    bstack1l1l1ll11ll_opy_ = bstack11111l_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࠦጕ")
    def __init__(self):
        super().__init__(bstack1ll11l11lll_opy_=self.bstack1l1l1ll11l1_opy_, frameworks=[bstack1lll11l11l1_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1l111111_opy_((bstack1lll11l1ll1_opy_.BEFORE_EACH, bstack1ll1lll1lll_opy_.POST), self.bstack1l1l1111l11_opy_)
        TestFramework.bstack1ll1l111111_opy_((bstack1lll11l1ll1_opy_.TEST, bstack1ll1lll1lll_opy_.PRE), self.bstack1ll1l11l11l_opy_)
        TestFramework.bstack1ll1l111111_opy_((bstack1lll11l1ll1_opy_.TEST, bstack1ll1lll1lll_opy_.POST), self.bstack1ll1ll11111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1111l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll1lll_opy_,
        bstack1111111111_opy_: Tuple[bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1llll1l1l_opy_ = self.bstack1l1l11111ll_opy_(instance.context)
        if not bstack1l1llll1l1l_opy_:
            self.logger.debug(bstack11111l_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥ጖") + str(bstack1111111111_opy_) + bstack11111l_opy_ (u"ࠣࠤ጗"))
        f.bstack1llllllll1l_opy_(instance, bstack1llll1llll1_opy_.bstack1ll111llll1_opy_, bstack1l1llll1l1l_opy_)
        bstack1l1l111ll11_opy_ = self.bstack1l1l11111ll_opy_(instance.context, bstack1l1l1111l1l_opy_=False)
        f.bstack1llllllll1l_opy_(instance, bstack1llll1llll1_opy_.bstack1l1l1ll1ll1_opy_, bstack1l1l111ll11_opy_)
    def bstack1ll1l11l11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll1lll_opy_,
        bstack1111111111_opy_: Tuple[bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1111l11_opy_(f, instance, bstack1111111111_opy_, *args, **kwargs)
        if not f.bstack1111111l11_opy_(instance, bstack1llll1llll1_opy_.bstack1l1l1lll11l_opy_, False):
            self.__1l1l111l111_opy_(f,instance,bstack1111111111_opy_)
    def bstack1ll1ll11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll1lll_opy_,
        bstack1111111111_opy_: Tuple[bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1111l11_opy_(f, instance, bstack1111111111_opy_, *args, **kwargs)
        if not f.bstack1111111l11_opy_(instance, bstack1llll1llll1_opy_.bstack1l1l1lll11l_opy_, False):
            self.__1l1l111l111_opy_(f, instance, bstack1111111111_opy_)
        if not f.bstack1111111l11_opy_(instance, bstack1llll1llll1_opy_.bstack1l1l1ll11ll_opy_, False):
            self.__1l1l111ll1l_opy_(f, instance, bstack1111111111_opy_)
    def bstack1l1l1111ll1_opy_(
        self,
        f: bstack1lll11l11l1_opy_,
        driver: object,
        exec: Tuple[bstack111111ll1l_opy_, str],
        bstack1111111111_opy_: Tuple[bstack1111111l1l_opy_, bstack1111l11l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1ll1l1111ll_opy_(instance):
            return
        if f.bstack1111111l11_opy_(instance, bstack1llll1llll1_opy_.bstack1l1l1ll11ll_opy_, False):
            return
        driver.execute_script(
            bstack11111l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠢጘ").format(
                json.dumps(
                    {
                        bstack11111l_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥጙ"): bstack11111l_opy_ (u"ࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠢጚ"),
                        bstack11111l_opy_ (u"ࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣጛ"): {bstack11111l_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨጜ"): result},
                    }
                )
            )
        )
        f.bstack1llllllll1l_opy_(instance, bstack1llll1llll1_opy_.bstack1l1l1ll11ll_opy_, True)
    def bstack1l1l11111ll_opy_(self, context: bstack11111l11l1_opy_, bstack1l1l1111l1l_opy_= True):
        if bstack1l1l1111l1l_opy_:
            bstack1l1llll1l1l_opy_ = self.bstack1ll11l11l1l_opy_(context, reverse=True)
        else:
            bstack1l1llll1l1l_opy_ = self.bstack1ll11l1l111_opy_(context, reverse=True)
        return [f for f in bstack1l1llll1l1l_opy_ if f[1].state != bstack1111111l1l_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1llll1l111_opy_, stage=STAGE.bstack1l1llll11_opy_)
    def __1l1l111ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll1lll_opy_,
        bstack1111111111_opy_: Tuple[bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_],
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11111l_opy_ (u"ࠢࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠧጝ")).get(bstack11111l_opy_ (u"ࠣࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠧጞ")):
            bstack1l1llll1l1l_opy_ = f.bstack1111111l11_opy_(instance, bstack1llll1llll1_opy_.bstack1ll111llll1_opy_, [])
            if not bstack1l1llll1l1l_opy_:
                self.logger.debug(bstack11111l_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧጟ") + str(bstack1111111111_opy_) + bstack11111l_opy_ (u"ࠥࠦጠ"))
                return
            driver = bstack1l1llll1l1l_opy_[0][0]()
            status = f.bstack1111111l11_opy_(instance, TestFramework.bstack1l1l1l1llll_opy_, None)
            if not status:
                self.logger.debug(bstack11111l_opy_ (u"ࠦࡸ࡫ࡴࡠࡣࡦࡸ࡮ࡼࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡴ࠼ࠣࡲࡴࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴ࠭ࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨጡ") + str(bstack1111111111_opy_) + bstack11111l_opy_ (u"ࠧࠨጢ"))
                return
            bstack1l1l1l1ll11_opy_ = {bstack11111l_opy_ (u"ࠨࡳࡵࡣࡷࡹࡸࠨጣ"): status.lower()}
            bstack1l1l1ll111l_opy_ = f.bstack1111111l11_opy_(instance, TestFramework.bstack1l1l1ll1111_opy_, None)
            if status.lower() == bstack11111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧጤ") and bstack1l1l1ll111l_opy_ is not None:
                bstack1l1l1l1ll11_opy_[bstack11111l_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨጥ")] = bstack1l1l1ll111l_opy_[0][bstack11111l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬጦ")][0] if isinstance(bstack1l1l1ll111l_opy_, list) else str(bstack1l1l1ll111l_opy_)
            driver.execute_script(
                bstack11111l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࡽࠣጧ").format(
                    json.dumps(
                        {
                            bstack11111l_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦጨ"): bstack11111l_opy_ (u"ࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣጩ"),
                            bstack11111l_opy_ (u"ࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤጪ"): bstack1l1l1l1ll11_opy_,
                        }
                    )
                )
            )
            f.bstack1llllllll1l_opy_(instance, bstack1llll1llll1_opy_.bstack1l1l1ll11ll_opy_, True)
    @measure(event_name=EVENTS.bstack1l1lll11ll_opy_, stage=STAGE.bstack1l1llll11_opy_)
    def __1l1l111l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll1lll_opy_,
        bstack1111111111_opy_: Tuple[bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_]
    ):
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack11111l_opy_ (u"ࠢࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠧጫ")).get(bstack11111l_opy_ (u"ࠣࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥጬ")):
            test_name = f.bstack1111111l11_opy_(instance, TestFramework.bstack1l1l111l1ll_opy_, None)
            if not test_name:
                self.logger.debug(bstack11111l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡲࡦࡳࡥࠣጭ"))
                return
            bstack1l1llll1l1l_opy_ = f.bstack1111111l11_opy_(instance, bstack1llll1llll1_opy_.bstack1ll111llll1_opy_, [])
            if not bstack1l1llll1l1l_opy_:
                self.logger.debug(bstack11111l_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡷࡩࡸࡺࠬࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧጮ") + str(bstack1111111111_opy_) + bstack11111l_opy_ (u"ࠦࠧጯ"))
                return
            for bstack1l1ll1ll1ll_opy_, bstack1l1l1111lll_opy_ in bstack1l1llll1l1l_opy_:
                if not bstack1lll11l11l1_opy_.bstack1ll1l1111ll_opy_(bstack1l1l1111lll_opy_):
                    continue
                driver = bstack1l1ll1ll1ll_opy_()
                if not driver:
                    continue
                driver.execute_script(
                    bstack11111l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥጰ").format(
                        json.dumps(
                            {
                                bstack11111l_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨጱ"): bstack11111l_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣጲ"),
                                bstack11111l_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦጳ"): {bstack11111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢጴ"): test_name},
                            }
                        )
                    )
                )
            f.bstack1llllllll1l_opy_(instance, bstack1llll1llll1_opy_.bstack1l1l1lll11l_opy_, True)
    def bstack1ll111lll11_opy_(
        self,
        instance: bstack1lll1ll1lll_opy_,
        f: TestFramework,
        bstack1111111111_opy_: Tuple[bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1111l11_opy_(f, instance, bstack1111111111_opy_, *args, **kwargs)
        bstack1l1llll1l1l_opy_ = [d for d, _ in f.bstack1111111l11_opy_(instance, bstack1llll1llll1_opy_.bstack1ll111llll1_opy_, [])]
        if not bstack1l1llll1l1l_opy_:
            self.logger.debug(bstack11111l_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠢࡷࡳࠥࡲࡩ࡯࡭ࠥጵ"))
            return
        if not bstack1ll111l1lll_opy_():
            self.logger.debug(bstack11111l_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤጶ"))
            return
        for bstack1l1l111l11l_opy_ in bstack1l1llll1l1l_opy_:
            driver = bstack1l1l111l11l_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack11111l_opy_ (u"ࠧࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡘࡿ࡮ࡤ࠼ࠥጷ") + str(timestamp)
            driver.execute_script(
                bstack11111l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠦጸ").format(
                    json.dumps(
                        {
                            bstack11111l_opy_ (u"ࠢࡢࡥࡷ࡭ࡴࡴࠢጹ"): bstack11111l_opy_ (u"ࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥጺ"),
                            bstack11111l_opy_ (u"ࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧጻ"): {
                                bstack11111l_opy_ (u"ࠥࡸࡾࡶࡥࠣጼ"): bstack11111l_opy_ (u"ࠦࡆࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠣጽ"),
                                bstack11111l_opy_ (u"ࠧࡪࡡࡵࡣࠥጾ"): data,
                                bstack11111l_opy_ (u"ࠨ࡬ࡦࡸࡨࡰࠧጿ"): bstack11111l_opy_ (u"ࠢࡥࡧࡥࡹ࡬ࠨፀ")
                            }
                        }
                    )
                )
            )
    def bstack1l1lll1lll1_opy_(
        self,
        instance: bstack1lll1ll1lll_opy_,
        f: TestFramework,
        bstack1111111111_opy_: Tuple[bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1111l11_opy_(f, instance, bstack1111111111_opy_, *args, **kwargs)
        bstack1l1llll1l1l_opy_ = [d for _, d in f.bstack1111111l11_opy_(instance, bstack1llll1llll1_opy_.bstack1ll111llll1_opy_, [])] + [d for _, d in f.bstack1111111l11_opy_(instance, bstack1llll1llll1_opy_.bstack1l1l1ll1ll1_opy_, [])]
        keys = [
            bstack1llll1llll1_opy_.bstack1ll111llll1_opy_,
            bstack1llll1llll1_opy_.bstack1l1l1ll1ll1_opy_,
        ]
        bstack1l1llll1l1l_opy_ = [
            d for key in keys for _, d in f.bstack1111111l11_opy_(instance, key, [])
        ]
        if not bstack1l1llll1l1l_opy_:
            self.logger.debug(bstack11111l_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡸࡲࡦࡨ࡬ࡦࠢࡷࡳࠥ࡬ࡩ࡯ࡦࠣࡥࡳࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠢࡷࡳࠥࡲࡩ࡯࡭ࠥፁ"))
            return
        if f.bstack1111111l11_opy_(instance, bstack1llll1llll1_opy_.bstack1ll1111llll_opy_, False):
            self.logger.debug(bstack11111l_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡇࡇ࡚ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡥࡵࡩࡦࡺࡥࡥࠤፂ"))
            return
        self.bstack1ll1l11l1l1_opy_()
        bstack1l1l1l1l_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1ll1l111l1l_opy_)
        req.test_framework_name = TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1ll1l1ll1ll_opy_)
        req.test_framework_version = TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1ll1111ll11_opy_)
        req.test_framework_state = bstack1111111111_opy_[0].name
        req.test_hook_state = bstack1111111111_opy_[1].name
        req.test_uuid = TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1ll1l1111l1_opy_)
        for driver in bstack1l1llll1l1l_opy_:
            session = req.automation_sessions.add()
            session.provider = (
                bstack11111l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠤፃ")
                if bstack1lll11l11l1_opy_.bstack1111111l11_opy_(driver, bstack1lll11l11l1_opy_.bstack1l1l111l1l1_opy_, False)
                else bstack11111l_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࡤ࡭ࡲࡪࡦࠥፄ")
            )
            session.ref = driver.ref()
            session.hub_url = bstack1lll11l11l1_opy_.bstack1111111l11_opy_(driver, bstack1lll11l11l1_opy_.bstack1l1ll111ll1_opy_, bstack11111l_opy_ (u"ࠧࠨፅ"))
            session.framework_name = driver.framework_name
            session.framework_version = driver.framework_version
            session.framework_session_id = bstack1lll11l11l1_opy_.bstack1111111l11_opy_(driver, bstack1lll11l11l1_opy_.bstack1l1ll111111_opy_, bstack11111l_opy_ (u"ࠨࠢፆ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1ll1l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll1lll_opy_,
        bstack1111111111_opy_: Tuple[bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_],
        *args,
        **kwargs
    ):
        bstack1l1llll1l1l_opy_ = f.bstack1111111l11_opy_(instance, bstack1llll1llll1_opy_.bstack1ll111llll1_opy_, [])
        if not bstack1l1llll1l1l_opy_:
            self.logger.debug(bstack11111l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥፇ") + str(kwargs) + bstack11111l_opy_ (u"ࠣࠤፈ"))
            return {}
        if len(bstack1l1llll1l1l_opy_) > 1:
            self.logger.debug(bstack11111l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧፉ") + str(kwargs) + bstack11111l_opy_ (u"ࠥࠦፊ"))
            return {}
        bstack1l1ll1ll1ll_opy_, bstack1l1ll11llll_opy_ = bstack1l1llll1l1l_opy_[0]
        driver = bstack1l1ll1ll1ll_opy_()
        if not driver:
            self.logger.debug(bstack11111l_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨፋ") + str(kwargs) + bstack11111l_opy_ (u"ࠧࠨፌ"))
            return {}
        capabilities = f.bstack1111111l11_opy_(bstack1l1ll11llll_opy_, bstack1lll11l11l1_opy_.bstack1l1ll11ll1l_opy_)
        if not capabilities:
            self.logger.debug(bstack11111l_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨፍ") + str(kwargs) + bstack11111l_opy_ (u"ࠢࠣፎ"))
            return {}
        return capabilities.get(bstack11111l_opy_ (u"ࠣࡣ࡯ࡻࡦࡿࡳࡎࡣࡷࡧ࡭ࠨፏ"), {})
    def bstack1ll1ll1lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll1lll_opy_,
        bstack1111111111_opy_: Tuple[bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_],
        *args,
        **kwargs
    ):
        bstack1l1llll1l1l_opy_ = f.bstack1111111l11_opy_(instance, bstack1llll1llll1_opy_.bstack1ll111llll1_opy_, [])
        if not bstack1l1llll1l1l_opy_:
            self.logger.debug(bstack11111l_opy_ (u"ࠤࡪࡩࡹࡥࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡨࡷ࡯ࡶࡦࡴ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧፐ") + str(kwargs) + bstack11111l_opy_ (u"ࠥࠦፑ"))
            return
        if len(bstack1l1llll1l1l_opy_) > 1:
            self.logger.debug(bstack11111l_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦࡻ࡭ࡧࡱࠬࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢፒ") + str(kwargs) + bstack11111l_opy_ (u"ࠧࠨፓ"))
        bstack1l1ll1ll1ll_opy_, bstack1l1ll11llll_opy_ = bstack1l1llll1l1l_opy_[0]
        driver = bstack1l1ll1ll1ll_opy_()
        if not driver:
            self.logger.debug(bstack11111l_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣፔ") + str(kwargs) + bstack11111l_opy_ (u"ࠢࠣፕ"))
            return
        return driver