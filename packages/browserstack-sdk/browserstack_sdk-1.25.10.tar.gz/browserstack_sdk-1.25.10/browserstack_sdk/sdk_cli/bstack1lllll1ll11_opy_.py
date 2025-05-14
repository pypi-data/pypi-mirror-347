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
from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack11111l1111_opy_ import bstack111111ll1l_opy_, bstack1111111l1l_opy_, bstack1111l11l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l1l1_opy_ import bstack1lll1l1111l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llll11l_opy_ import bstack1llll1llll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll111111l_opy_ import bstack1lll11l11l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll11l1ll1_opy_, bstack1lll1ll1lll_opy_, bstack1ll1lll1lll_opy_, bstack1ll1llll111_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1ll111l1lll_opy_, bstack1l1lllll1l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1ll1111l111_opy_ = [bstack11111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᆳ"), bstack11111l_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥᆴ"), bstack11111l_opy_ (u"ࠦࡨࡵ࡮ࡧ࡫ࡪࠦᆵ"), bstack11111l_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࠨᆶ"), bstack11111l_opy_ (u"ࠨࡰࡢࡶ࡫ࠦᆷ")]
bstack1l1lll1ll1l_opy_ = bstack1l1lllll1l1_opy_()
bstack1l1llll111l_opy_ = bstack11111l_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢᆸ")
bstack1l1llllllll_opy_ = {
    bstack11111l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡋࡷࡩࡲࠨᆹ"): bstack1ll1111l111_opy_,
    bstack11111l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡓࡥࡨࡱࡡࡨࡧࠥᆺ"): bstack1ll1111l111_opy_,
    bstack11111l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡑࡴࡪࡵ࡭ࡧࠥᆻ"): bstack1ll1111l111_opy_,
    bstack11111l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡈࡲࡡࡴࡵࠥᆼ"): bstack1ll1111l111_opy_,
    bstack11111l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡌࡵ࡯ࡥࡷ࡭ࡴࡴࠢᆽ"): bstack1ll1111l111_opy_
    + [
        bstack11111l_opy_ (u"ࠨ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬࡯ࡣࡰࡩࠧᆾ"),
        bstack11111l_opy_ (u"ࠢ࡬ࡧࡼࡻࡴࡸࡤࡴࠤᆿ"),
        bstack11111l_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦ࡫ࡱࡪࡴࠨᇀ"),
        bstack11111l_opy_ (u"ࠤ࡮ࡩࡾࡽ࡯ࡳࡦࡶࠦᇁ"),
        bstack11111l_opy_ (u"ࠥࡧࡦࡲ࡬ࡴࡲࡨࡧࠧᇂ"),
        bstack11111l_opy_ (u"ࠦࡨࡧ࡬࡭ࡱࡥ࡮ࠧᇃ"),
        bstack11111l_opy_ (u"ࠧࡹࡴࡢࡴࡷࠦᇄ"),
        bstack11111l_opy_ (u"ࠨࡳࡵࡱࡳࠦᇅ"),
        bstack11111l_opy_ (u"ࠢࡥࡷࡵࡥࡹ࡯࡯࡯ࠤᇆ"),
        bstack11111l_opy_ (u"ࠣࡹ࡫ࡩࡳࠨᇇ"),
    ],
    bstack11111l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡰࡥ࡮ࡴ࠮ࡔࡧࡶࡷ࡮ࡵ࡮ࠣᇈ"): [bstack11111l_opy_ (u"ࠥࡷࡹࡧࡲࡵࡲࡤࡸ࡭ࠨᇉ"), bstack11111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࡩࡥ࡮ࡲࡥࡥࠤᇊ"), bstack11111l_opy_ (u"ࠧࡺࡥࡴࡶࡶࡧࡴࡲ࡬ࡦࡥࡷࡩࡩࠨᇋ"), bstack11111l_opy_ (u"ࠨࡩࡵࡧࡰࡷࠧᇌ")],
    bstack11111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡤࡱࡱࡪ࡮࡭࠮ࡄࡱࡱࡪ࡮࡭ࠢᇍ"): [bstack11111l_opy_ (u"ࠣ࡫ࡱࡺࡴࡩࡡࡵ࡫ࡲࡲࡤࡶࡡࡳࡣࡰࡷࠧᇎ"), bstack11111l_opy_ (u"ࠤࡤࡶ࡬ࡹࠢᇏ")],
    bstack11111l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡪ࡮ࡾࡴࡶࡴࡨࡷ࠳ࡌࡩࡹࡶࡸࡶࡪࡊࡥࡧࠤᇐ"): [bstack11111l_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᇑ"), bstack11111l_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨᇒ"), bstack11111l_opy_ (u"ࠨࡦࡶࡰࡦࠦᇓ"), bstack11111l_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢᇔ"), bstack11111l_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥᇕ"), bstack11111l_opy_ (u"ࠤ࡬ࡨࡸࠨᇖ")],
    bstack11111l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡪ࡮ࡾࡴࡶࡴࡨࡷ࠳࡙ࡵࡣࡔࡨࡵࡺ࡫ࡳࡵࠤᇗ"): [bstack11111l_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࠤᇘ"), bstack11111l_opy_ (u"ࠧࡶࡡࡳࡣࡰࠦᇙ"), bstack11111l_opy_ (u"ࠨࡰࡢࡴࡤࡱࡤ࡯࡮ࡥࡧࡻࠦᇚ")],
    bstack11111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡳࡷࡱࡲࡪࡸ࠮ࡄࡣ࡯ࡰࡎࡴࡦࡰࠤᇛ"): [bstack11111l_opy_ (u"ࠣࡹ࡫ࡩࡳࠨᇜ"), bstack11111l_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࠤᇝ")],
    bstack11111l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦࡸ࡫࠯ࡵࡷࡶࡺࡩࡴࡶࡴࡨࡷ࠳ࡔ࡯ࡥࡧࡎࡩࡾࡽ࡯ࡳࡦࡶࠦᇞ"): [bstack11111l_opy_ (u"ࠦࡳࡵࡤࡦࠤᇟ"), bstack11111l_opy_ (u"ࠧࡶࡡࡳࡧࡱࡸࠧᇠ")],
    bstack11111l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴࡭ࡢࡴ࡮࠲ࡸࡺࡲࡶࡥࡷࡹࡷ࡫ࡳ࠯ࡏࡤࡶࡰࠨᇡ"): [bstack11111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᇢ"), bstack11111l_opy_ (u"ࠣࡣࡵ࡫ࡸࠨᇣ"), bstack11111l_opy_ (u"ࠤ࡮ࡻࡦࡸࡧࡴࠤᇤ")],
}
_1l1llllll11_opy_ = set()
class bstack1lll111l111_opy_(bstack1lll1l1111l_opy_):
    bstack1l1llllll1l_opy_ = bstack11111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡨࡪࡪࡸࡲࡦࡦࠥᇥ")
    bstack1ll111ll111_opy_ = bstack11111l_opy_ (u"ࠦࡎࡔࡆࡐࠤᇦ")
    bstack1l1llll1l11_opy_ = bstack11111l_opy_ (u"ࠧࡋࡒࡓࡑࡕࠦᇧ")
    bstack1ll1111l11l_opy_: Callable
    bstack1l1lll1l1ll_opy_: Callable
    def __init__(self, bstack1llllll11l1_opy_, bstack1lll1111lll_opy_):
        super().__init__()
        self.bstack1ll1ll1111l_opy_ = bstack1lll1111lll_opy_
        if os.getenv(bstack11111l_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡕ࠱࠲࡛ࠥᇨ"), bstack11111l_opy_ (u"ࠢ࠲ࠤᇩ")) != bstack11111l_opy_ (u"ࠣ࠳ࠥᇪ") or not self.is_enabled():
            self.logger.warning(bstack11111l_opy_ (u"ࠤࠥᇫ") + str(self.__class__.__name__) + bstack11111l_opy_ (u"ࠥࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩࠨᇬ"))
            return
        TestFramework.bstack1ll1l111111_opy_((bstack1lll11l1ll1_opy_.TEST, bstack1ll1lll1lll_opy_.PRE), self.bstack1ll1l11l11l_opy_)
        TestFramework.bstack1ll1l111111_opy_((bstack1lll11l1ll1_opy_.TEST, bstack1ll1lll1lll_opy_.POST), self.bstack1ll1ll11111_opy_)
        for event in bstack1lll11l1ll1_opy_:
            for state in bstack1ll1lll1lll_opy_:
                TestFramework.bstack1ll1l111111_opy_((event, state), self.bstack1ll11111lll_opy_)
        bstack1llllll11l1_opy_.bstack1ll1l111111_opy_((bstack1111111l1l_opy_.bstack1111l111ll_opy_, bstack1111l11l11_opy_.POST), self.bstack1l1lll11l1l_opy_)
        self.bstack1ll1111l11l_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1ll11111l1l_opy_(bstack1lll111l111_opy_.bstack1ll111ll111_opy_, self.bstack1ll1111l11l_opy_)
        self.bstack1l1lll1l1ll_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1ll11111l1l_opy_(bstack1lll111l111_opy_.bstack1l1llll1l11_opy_, self.bstack1l1lll1l1ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11111lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll1lll_opy_,
        bstack1111111111_opy_: Tuple[bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1lllll1ll_opy_() and instance:
            bstack1l1lll111ll_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1111111111_opy_
            if test_framework_state == bstack1lll11l1ll1_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1lll11l1ll1_opy_.LOG:
                bstack1l1l1l1l_opy_ = datetime.now()
                entries = f.bstack1ll1111111l_opy_(instance, bstack1111111111_opy_)
                if entries:
                    self.bstack1ll111lllll_opy_(instance, entries)
                    instance.bstack1ll1ll1l11_opy_(bstack11111l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࠦᇭ"), datetime.now() - bstack1l1l1l1l_opy_)
                    f.bstack1l1lll1ll11_opy_(instance, bstack1111111111_opy_)
                instance.bstack1ll1ll1l11_opy_(bstack11111l_opy_ (u"ࠧࡵ࠱࠲ࡻ࠽ࡳࡳࡥࡡ࡭࡮ࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺࡳࠣᇮ"), datetime.now() - bstack1l1lll111ll_opy_)
                return # bstack1ll111l1l11_opy_ not send this event with the bstack1ll1111ll1l_opy_ bstack1ll1111l1l1_opy_
            elif (
                test_framework_state == bstack1lll11l1ll1_opy_.TEST
                and test_hook_state == bstack1ll1lll1lll_opy_.POST
                and not f.bstack11111111ll_opy_(instance, TestFramework.bstack1ll111111ll_opy_)
            ):
                self.logger.warning(bstack11111l_opy_ (u"ࠨࡤࡳࡱࡳࡴ࡮ࡴࡧࠡࡦࡸࡩࠥࡺ࡯ࠡ࡮ࡤࡧࡰࠦ࡯ࡧࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࠦᇯ") + str(TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1ll111111ll_opy_)) + bstack11111l_opy_ (u"ࠢࠣᇰ"))
                f.bstack1llllllll1l_opy_(instance, bstack1lll111l111_opy_.bstack1l1llllll1l_opy_, True)
                return # bstack1ll111l1l11_opy_ not send this event bstack1ll111lll1l_opy_ bstack1l1lllllll1_opy_
            elif (
                f.bstack1111111l11_opy_(instance, bstack1lll111l111_opy_.bstack1l1llllll1l_opy_, False)
                and test_framework_state == bstack1lll11l1ll1_opy_.LOG_REPORT
                and test_hook_state == bstack1ll1lll1lll_opy_.POST
                and f.bstack11111111ll_opy_(instance, TestFramework.bstack1ll111111ll_opy_)
            ):
                self.logger.warning(bstack11111l_opy_ (u"ࠣ࡫ࡱ࡮ࡪࡩࡴࡪࡰࡪࠤ࡙࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡧࡴࡦ࠰ࡗࡉࡘ࡚ࠬࠡࡖࡨࡷࡹࡎ࡯ࡰ࡭ࡖࡸࡦࡺࡥ࠯ࡒࡒࡗ࡙ࠦࠢᇱ") + str(TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1ll111111ll_opy_)) + bstack11111l_opy_ (u"ࠤࠥᇲ"))
                self.bstack1ll11111lll_opy_(f, instance, (bstack1lll11l1ll1_opy_.TEST, bstack1ll1lll1lll_opy_.POST), *args, **kwargs)
            bstack1l1l1l1l_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1ll111ll1l1_opy_ = sorted(
                filter(lambda x: x.get(bstack11111l_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᇳ"), None), data.pop(bstack11111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᇴ"), {}).values()),
                key=lambda x: x[bstack11111l_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᇵ")],
            )
            if bstack1llll1llll1_opy_.bstack1ll111llll1_opy_ in data:
                data.pop(bstack1llll1llll1_opy_.bstack1ll111llll1_opy_)
            data.update({bstack11111l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᇶ"): bstack1ll111ll1l1_opy_})
            instance.bstack1ll1ll1l11_opy_(bstack11111l_opy_ (u"ࠢ࡫ࡵࡲࡲ࠿ࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᇷ"), datetime.now() - bstack1l1l1l1l_opy_)
            bstack1l1l1l1l_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1ll111l11l1_opy_)
            instance.bstack1ll1ll1l11_opy_(bstack11111l_opy_ (u"ࠣ࡬ࡶࡳࡳࡀ࡯࡯ࡡࡤࡰࡱࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶࡶࠦᇸ"), datetime.now() - bstack1l1l1l1l_opy_)
            self.bstack1ll1111l1l1_opy_(instance, bstack1111111111_opy_, event_json=event_json)
            instance.bstack1ll1ll1l11_opy_(bstack11111l_opy_ (u"ࠤࡲ࠵࠶ࡿ࠺ࡰࡰࡢࡥࡱࡲ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷࡷࠧᇹ"), datetime.now() - bstack1l1lll111ll_opy_)
    def bstack1ll1l11l11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll1lll_opy_,
        bstack1111111111_opy_: Tuple[bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1lll11ll11_opy_ import bstack1lllll11lll_opy_
        bstack1ll1ll111ll_opy_ = bstack1lllll11lll_opy_.bstack1ll1l11l111_opy_(EVENTS.bstack1l1ll1lll_opy_.value)
        self.bstack1ll1ll1111l_opy_.bstack1ll111lll11_opy_(instance, f, bstack1111111111_opy_, *args, **kwargs)
        bstack1lllll11lll_opy_.end(EVENTS.bstack1l1ll1lll_opy_.value, bstack1ll1ll111ll_opy_ + bstack11111l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᇺ"), bstack1ll1ll111ll_opy_ + bstack11111l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᇻ"), status=True, failure=None, test_name=None)
    def bstack1ll1ll11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll1lll_opy_,
        bstack1111111111_opy_: Tuple[bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll1ll1111l_opy_.bstack1l1lll1lll1_opy_(instance, f, bstack1111111111_opy_, *args, **kwargs)
        self.bstack1ll11111111_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1lllll111_opy_, stage=STAGE.bstack1l1llll11_opy_)
    def bstack1ll11111111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll1lll_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack11111l_opy_ (u"࡙ࠧ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡕࡧࡶࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡊࡼࡥ࡯ࡶࠣ࡫ࡗࡖࡃࠡࡥࡤࡰࡱࡀࠠࡏࡱࠣࡺࡦࡲࡩࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡨࡦࡺࡡࠣᇼ"))
            return
        bstack1l1l1l1l_opy_ = datetime.now()
        try:
            r = self.bstack1lll11l11ll_opy_.TestSessionEvent(req)
            instance.bstack1ll1ll1l11_opy_(bstack11111l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡࡷࡩࡸࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡧࡹࡩࡳࡺࠢᇽ"), datetime.now() - bstack1l1l1l1l_opy_)
            f.bstack1llllllll1l_opy_(instance, self.bstack1ll1ll1111l_opy_.bstack1ll1111llll_opy_, r.success)
            if not r.success:
                self.logger.info(bstack11111l_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᇾ") + str(r) + bstack11111l_opy_ (u"ࠣࠤᇿ"))
        except grpc.RpcError as e:
            self.logger.error(bstack11111l_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢሀ") + str(e) + bstack11111l_opy_ (u"ࠥࠦሁ"))
            traceback.print_exc()
            raise e
    def bstack1l1lll11l1l_opy_(
        self,
        f: bstack1lll11l11l1_opy_,
        _driver: object,
        exec: Tuple[bstack111111ll1l_opy_, str],
        _1l1ll1lll1l_opy_: Tuple[bstack1111111l1l_opy_, bstack1111l11l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1lll11l11l1_opy_.bstack1ll1l11llll_opy_(method_name):
            return
        if f.bstack1ll1l1l1111_opy_(*args) == bstack1lll11l11l1_opy_.bstack1ll111l1l1l_opy_:
            bstack1l1lll111ll_opy_ = datetime.now()
            screenshot = result.get(bstack11111l_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥሂ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack11111l_opy_ (u"ࠧ࡯࡮ࡷࡣ࡯࡭ࡩࠦࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣ࡭ࡲࡧࡧࡦࠢࡥࡥࡸ࡫࠶࠵ࠢࡶࡸࡷࠨሃ"))
                return
            bstack1ll111ll11l_opy_ = self.bstack1ll111l1ll1_opy_(instance)
            if bstack1ll111ll11l_opy_:
                entry = bstack1ll1llll111_opy_(TestFramework.bstack1l1llll1lll_opy_, screenshot)
                self.bstack1ll111lllll_opy_(bstack1ll111ll11l_opy_, [entry])
                instance.bstack1ll1ll1l11_opy_(bstack11111l_opy_ (u"ࠨ࡯࠲࠳ࡼ࠾ࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡥࡹࡧࡦࡹࡹ࡫ࠢሄ"), datetime.now() - bstack1l1lll111ll_opy_)
            else:
                self.logger.warning(bstack11111l_opy_ (u"ࠢࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡴࡦࡵࡷࠤ࡫ࡵࡲࠡࡹ࡫࡭ࡨ࡮ࠠࡵࡪ࡬ࡷࠥࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢࡺࡥࡸࠦࡴࡢ࡭ࡨࡲࠥࡨࡹࠡࡦࡵ࡭ࡻ࡫ࡲ࠾ࠢࡾࢁࠧህ").format(instance.ref()))
        event = {}
        bstack1ll111ll11l_opy_ = self.bstack1ll111l1ll1_opy_(instance)
        if bstack1ll111ll11l_opy_:
            self.bstack1l1lll11111_opy_(event, bstack1ll111ll11l_opy_)
            if event.get(bstack11111l_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨሆ")):
                self.bstack1ll111lllll_opy_(bstack1ll111ll11l_opy_, event[bstack11111l_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢሇ")])
            else:
                self.logger.info(bstack11111l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢ࡯ࡳ࡬ࡹࠠࡧࡱࡵࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡧࡹࡩࡳࡺࠢለ"))
    @measure(event_name=EVENTS.bstack1l1lll11l11_opy_, stage=STAGE.bstack1l1llll11_opy_)
    def bstack1ll111lllll_opy_(
        self,
        bstack1ll111ll11l_opy_: bstack1lll1ll1lll_opy_,
        entries: List[bstack1ll1llll111_opy_],
    ):
        self.bstack1ll1l11l1l1_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1111111l11_opy_(bstack1ll111ll11l_opy_, TestFramework.bstack1ll1l111l1l_opy_)
        req.execution_context.hash = str(bstack1ll111ll11l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1ll111ll11l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1ll111ll11l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1111111l11_opy_(bstack1ll111ll11l_opy_, TestFramework.bstack1ll1l1ll1ll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1111111l11_opy_(bstack1ll111ll11l_opy_, TestFramework.bstack1ll1111ll11_opy_)
            log_entry.uuid = TestFramework.bstack1111111l11_opy_(bstack1ll111ll11l_opy_, TestFramework.bstack1ll1l1111l1_opy_)
            log_entry.test_framework_state = bstack1ll111ll11l_opy_.state.name
            log_entry.message = entry.message.encode(bstack11111l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥሉ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack11111l_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢሊ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1lll11ll1_opy_
                log_entry.file_path = entry.bstack1lllllll_opy_
        def bstack1ll111l1111_opy_():
            bstack1l1l1l1l_opy_ = datetime.now()
            try:
                self.bstack1lll11l11ll_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1llll1lll_opy_:
                    bstack1ll111ll11l_opy_.bstack1ll1ll1l11_opy_(bstack11111l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥላ"), datetime.now() - bstack1l1l1l1l_opy_)
                elif entry.kind == TestFramework.bstack1l1llll11ll_opy_:
                    bstack1ll111ll11l_opy_.bstack1ll1ll1l11_opy_(bstack11111l_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦሌ"), datetime.now() - bstack1l1l1l1l_opy_)
                else:
                    bstack1ll111ll11l_opy_.bstack1ll1ll1l11_opy_(bstack11111l_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠ࡮ࡲ࡫ࠧል"), datetime.now() - bstack1l1l1l1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11111l_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢሎ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111l1ll1l_opy_.enqueue(bstack1ll111l1111_opy_)
    @measure(event_name=EVENTS.bstack1l1lll1l111_opy_, stage=STAGE.bstack1l1llll11_opy_)
    def bstack1ll1111l1l1_opy_(
        self,
        instance: bstack1lll1ll1lll_opy_,
        bstack1111111111_opy_: Tuple[bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_],
        event_json=None,
    ):
        self.bstack1ll1l11l1l1_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1ll1l111l1l_opy_)
        req.test_framework_name = TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1ll1l1ll1ll_opy_)
        req.test_framework_version = TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1ll1111ll11_opy_)
        req.test_framework_state = bstack1111111111_opy_[0].name
        req.test_hook_state = bstack1111111111_opy_[1].name
        started_at = TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1ll1111l1ll_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1l1lll111l1_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1ll111l11l1_opy_)).encode(bstack11111l_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤሏ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1ll111l1111_opy_():
            bstack1l1l1l1l_opy_ = datetime.now()
            try:
                self.bstack1lll11l11ll_opy_.TestFrameworkEvent(req)
                instance.bstack1ll1ll1l11_opy_(bstack11111l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟ࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡧࡹࡩࡳࡺࠢሐ"), datetime.now() - bstack1l1l1l1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11111l_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥሑ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111l1ll1l_opy_.enqueue(bstack1ll111l1111_opy_)
    def bstack1ll111l1ll1_opy_(self, instance: bstack111111ll1l_opy_):
        bstack1l1llll11l1_opy_ = TestFramework.bstack111111l1l1_opy_(instance.context)
        for t in bstack1l1llll11l1_opy_:
            bstack1l1llll1l1l_opy_ = TestFramework.bstack1111111l11_opy_(t, bstack1llll1llll1_opy_.bstack1ll111llll1_opy_, [])
            if any(instance is d[1] for d in bstack1l1llll1l1l_opy_):
                return t
    def bstack1l1lll1l1l1_opy_(self, message):
        self.bstack1ll1111l11l_opy_(message + bstack11111l_opy_ (u"ࠨ࡜࡯ࠤሒ"))
    def log_error(self, message):
        self.bstack1l1lll1l1ll_opy_(message + bstack11111l_opy_ (u"ࠢ࡝ࡰࠥሓ"))
    def bstack1ll11111l1l_opy_(self, level, original_func):
        def bstack1l1lll11lll_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            bstack1l1llll11l1_opy_ = TestFramework.bstack1ll111111l1_opy_()
            if not bstack1l1llll11l1_opy_:
                return return_value
            bstack1ll111ll11l_opy_ = next(
                (
                    instance
                    for instance in bstack1l1llll11l1_opy_
                    if TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1ll1l1111l1_opy_)
                ),
                None,
            )
            if not bstack1ll111ll11l_opy_:
                return
            entry = bstack1ll1llll111_opy_(TestFramework.bstack1ll11111ll1_opy_, message, level)
            self.bstack1ll111lllll_opy_(bstack1ll111ll11l_opy_, [entry])
            return return_value
        return bstack1l1lll11lll_opy_
    def bstack1l1lll11111_opy_(self, event: dict, instance=None) -> None:
        global _1l1llllll11_opy_
        levels = [bstack11111l_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦሔ"), bstack11111l_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨሕ")]
        bstack1ll111l11ll_opy_ = bstack11111l_opy_ (u"ࠥࠦሖ")
        if instance is not None:
            try:
                bstack1ll111l11ll_opy_ = TestFramework.bstack1111111l11_opy_(instance, TestFramework.bstack1ll1l1111l1_opy_)
            except Exception as e:
                self.logger.warning(bstack11111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡺࡻࡩࡥࠢࡩࡶࡴࡳࠠࡪࡰࡶࡸࡦࡴࡣࡦࠤሗ").format(e))
        bstack1l1ll1lllll_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack11111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬመ")]
                bstack1l1ll1lll11_opy_ = os.path.join(bstack1l1lll1ll1l_opy_, (bstack1l1llll111l_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1ll1lll11_opy_):
                    self.logger.info(bstack11111l_opy_ (u"ࠨࡄࡪࡴࡨࡧࡹࡵࡲࡺࠢࡱࡳࡹࠦࡰࡳࡧࡶࡩࡳࡺࠠࡧࡱࡵࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡖࡨࡷࡹࠦࡡ࡯ࡦࠣࡆࡺ࡯࡬ࡥࠢ࡯ࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠨሙ").format(bstack1l1ll1lll11_opy_))
                file_names = os.listdir(bstack1l1ll1lll11_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1ll1lll11_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l1llllll11_opy_:
                        self.logger.info(bstack11111l_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧሚ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1ll11111l11_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1ll11111l11_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack11111l_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦማ"):
                                entry = bstack1ll1llll111_opy_(
                                    kind=bstack11111l_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦሜ"),
                                    message=bstack11111l_opy_ (u"ࠥࠦም"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1lll11ll1_opy_=file_size,
                                    bstack1l1lllll11l_opy_=bstack11111l_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦሞ"),
                                    bstack1lllllll_opy_=os.path.abspath(file_path),
                                    bstack1llll1llll_opy_=bstack1ll111l11ll_opy_
                                )
                            elif level == bstack11111l_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤሟ"):
                                entry = bstack1ll1llll111_opy_(
                                    kind=bstack11111l_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣሠ"),
                                    message=bstack11111l_opy_ (u"ࠢࠣሡ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1lll11ll1_opy_=file_size,
                                    bstack1l1lllll11l_opy_=bstack11111l_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣሢ"),
                                    bstack1lllllll_opy_=os.path.abspath(file_path),
                                    bstack1ll111ll1ll_opy_=bstack1ll111l11ll_opy_
                                )
                            bstack1l1ll1lllll_opy_.append(entry)
                            _1l1llllll11_opy_.add(abs_path)
                        except Exception as bstack1l1lll1llll_opy_:
                            self.logger.error(bstack11111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡸࡡࡪࡵࡨࡨࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠧሣ").format(bstack1l1lll1llll_opy_))
        except Exception as e:
            self.logger.error(bstack11111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡲࡢ࡫ࡶࡩࡩࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠨሤ").format(e))
        event[bstack11111l_opy_ (u"ࠦࡱࡵࡧࡴࠤሥ")] = bstack1l1ll1lllll_opy_
class bstack1ll111l11l1_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1lll1l11l_opy_ = set()
        kwargs[bstack11111l_opy_ (u"ࠧࡹ࡫ࡪࡲ࡮ࡩࡾࡹࠢሦ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1ll1llll1_opy_(obj, self.bstack1l1lll1l11l_opy_)
def bstack1l1llll1111_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1ll1llll1_opy_(obj, bstack1l1lll1l11l_opy_=None, max_depth=3):
    if bstack1l1lll1l11l_opy_ is None:
        bstack1l1lll1l11l_opy_ = set()
    if id(obj) in bstack1l1lll1l11l_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1lll1l11l_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1lll1111l_opy_ = TestFramework.bstack1ll1111lll1_opy_(obj)
    bstack1ll111l111l_opy_ = next((k.lower() in bstack1l1lll1111l_opy_.lower() for k in bstack1l1llllllll_opy_.keys()), None)
    if bstack1ll111l111l_opy_:
        obj = TestFramework.bstack1l1llll1ll1_opy_(obj, bstack1l1llllllll_opy_[bstack1ll111l111l_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack11111l_opy_ (u"ࠨ࡟ࡠࡵ࡯ࡳࡹࡹ࡟ࡠࠤሧ")):
            keys = getattr(obj, bstack11111l_opy_ (u"ࠢࡠࡡࡶࡰࡴࡺࡳࡠࡡࠥረ"), [])
        elif hasattr(obj, bstack11111l_opy_ (u"ࠣࡡࡢࡨ࡮ࡩࡴࡠࡡࠥሩ")):
            keys = getattr(obj, bstack11111l_opy_ (u"ࠤࡢࡣࡩ࡯ࡣࡵࡡࡢࠦሪ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack11111l_opy_ (u"ࠥࡣࠧራ"))}
        if not obj and bstack1l1lll1111l_opy_ == bstack11111l_opy_ (u"ࠦࡵࡧࡴࡩ࡮࡬ࡦ࠳ࡖ࡯ࡴ࡫ࡻࡔࡦࡺࡨࠣሬ"):
            obj = {bstack11111l_opy_ (u"ࠧࡶࡡࡵࡪࠥር"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l1llll1111_opy_(key) or str(key).startswith(bstack11111l_opy_ (u"ࠨ࡟ࠣሮ")):
            continue
        if value is not None and bstack1l1llll1111_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1ll1llll1_opy_(value, bstack1l1lll1l11l_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1ll1llll1_opy_(o, bstack1l1lll1l11l_opy_, max_depth) for o in value]))
    return result or None