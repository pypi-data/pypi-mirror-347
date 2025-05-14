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
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.bstack1lll111l1l1_opy_ import bstack1lll1l1111l_opy_
from browserstack_sdk.sdk_cli.bstack11111l1111_opy_ import (
    bstack1111111l1l_opy_,
    bstack1111l11l11_opy_,
    bstack111111ll1l_opy_,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1lllllll111_opy_ import bstack1llllll1lll_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1l11llllll_opy_
from bstack_utils.helper import bstack1ll111l1lll_opy_
import threading
import os
import urllib.parse
class bstack1llll1l1lll_opy_(bstack1lll1l1111l_opy_):
    def __init__(self, bstack1lll1111lll_opy_):
        super().__init__()
        bstack1llllll1lll_opy_.bstack1ll1l111111_opy_((bstack1111111l1l_opy_.bstack1111l11ll1_opy_, bstack1111l11l11_opy_.PRE), self.bstack1l1ll111l1l_opy_)
        bstack1llllll1lll_opy_.bstack1ll1l111111_opy_((bstack1111111l1l_opy_.bstack1111l11ll1_opy_, bstack1111l11l11_opy_.PRE), self.bstack1l1ll1111ll_opy_)
        bstack1llllll1lll_opy_.bstack1ll1l111111_opy_((bstack1111111l1l_opy_.bstack11111l1l1l_opy_, bstack1111l11l11_opy_.PRE), self.bstack1l1ll11111l_opy_)
        bstack1llllll1lll_opy_.bstack1ll1l111111_opy_((bstack1111111l1l_opy_.bstack1111l111ll_opy_, bstack1111l11l11_opy_.PRE), self.bstack1l1ll11l1ll_opy_)
        bstack1llllll1lll_opy_.bstack1ll1l111111_opy_((bstack1111111l1l_opy_.bstack1111l11ll1_opy_, bstack1111l11l11_opy_.PRE), self.bstack1l1l1lllll1_opy_)
        bstack1llllll1lll_opy_.bstack1ll1l111111_opy_((bstack1111111l1l_opy_.QUIT, bstack1111l11l11_opy_.PRE), self.on_close)
        self.bstack1lll1111lll_opy_ = bstack1lll1111lll_opy_
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll111l1l_opy_(
        self,
        f: bstack1llllll1lll_opy_,
        bstack1l1ll11l111_opy_: object,
        exec: Tuple[bstack111111ll1l_opy_, str],
        bstack1111111111_opy_: Tuple[bstack1111111l1l_opy_, bstack1111l11l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11111l_opy_ (u"ࠤ࡯ࡥࡺࡴࡣࡩࠤቆ"):
            return
        if not bstack1ll111l1lll_opy_():
            self.logger.debug(bstack11111l_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢ࡯ࡥࡺࡴࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢቇ"))
            return
        def wrapped(bstack1l1ll11l111_opy_, launch, *args, **kwargs):
            response = self.bstack1l1ll111l11_opy_(f.platform_index, instance.ref(), json.dumps({bstack11111l_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪቈ"): True}).encode(bstack11111l_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦ቉")))
            if response is not None and response.capabilities:
                if not bstack1ll111l1lll_opy_():
                    browser = launch(bstack1l1ll11l111_opy_)
                    return browser
                bstack1l1ll111lll_opy_ = json.loads(response.capabilities.decode(bstack11111l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧቊ")))
                if not bstack1l1ll111lll_opy_: # empty caps bstack1l1ll11l1l1_opy_ bstack1l1l1llll1l_opy_ bstack1l1ll11ll11_opy_ bstack1lll11l1111_opy_ or error in processing
                    return
                bstack1l1ll11l11l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1ll111lll_opy_))
                f.bstack1llllllll1l_opy_(instance, bstack1llllll1lll_opy_.bstack1l1ll111ll1_opy_, bstack1l1ll11l11l_opy_)
                f.bstack1llllllll1l_opy_(instance, bstack1llllll1lll_opy_.bstack1l1ll11ll1l_opy_, bstack1l1ll111lll_opy_)
                browser = bstack1l1ll11l111_opy_.connect(bstack1l1ll11l11l_opy_)
                return browser
        return wrapped
    def bstack1l1ll11111l_opy_(
        self,
        f: bstack1llllll1lll_opy_,
        Connection: object,
        exec: Tuple[bstack111111ll1l_opy_, str],
        bstack1111111111_opy_: Tuple[bstack1111111l1l_opy_, bstack1111l11l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11111l_opy_ (u"ࠢࡥ࡫ࡶࡴࡦࡺࡣࡩࠤቋ"):
            self.logger.debug(bstack11111l_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠࡥ࡫ࡶࡴࡦࡺࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢቌ"))
            return
        if not bstack1ll111l1lll_opy_():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                if args and args[0].get(bstack11111l_opy_ (u"ࠩࡳࡥࡷࡧ࡭ࡴࠩቍ"), {}).get(bstack11111l_opy_ (u"ࠪࡦࡸࡖࡡࡳࡣࡰࡷࠬ቎")):
                    bstack1l1ll11lll1_opy_ = args[0][bstack11111l_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦ቏")][bstack11111l_opy_ (u"ࠧࡨࡳࡑࡣࡵࡥࡲࡹࠢቐ")]
                    session_id = bstack1l1ll11lll1_opy_.get(bstack11111l_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࡉࡥࠤቑ"))
                    f.bstack1llllllll1l_opy_(instance, bstack1llllll1lll_opy_.bstack1l1ll111111_opy_, session_id)
            except Exception as e:
                self.logger.debug(bstack11111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡤࡪࡵࡳࡥࡹࡩࡨࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠢࠥቒ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack1l1l1lllll1_opy_(
        self,
        f: bstack1llllll1lll_opy_,
        bstack1l1ll11l111_opy_: object,
        exec: Tuple[bstack111111ll1l_opy_, str],
        bstack1111111111_opy_: Tuple[bstack1111111l1l_opy_, bstack1111l11l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11111l_opy_ (u"ࠣࡥࡲࡲࡳ࡫ࡣࡵࠤቓ"):
            return
        if not bstack1ll111l1lll_opy_():
            self.logger.debug(bstack11111l_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡥࡲࡲࡳ࡫ࡣࡵࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢቔ"))
            return
        def wrapped(bstack1l1ll11l111_opy_, connect, *args, **kwargs):
            response = self.bstack1l1ll111l11_opy_(f.platform_index, instance.ref(), json.dumps({bstack11111l_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩቕ"): True}).encode(bstack11111l_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥቖ")))
            if response is not None and response.capabilities:
                bstack1l1ll111lll_opy_ = json.loads(response.capabilities.decode(bstack11111l_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦ቗")))
                if not bstack1l1ll111lll_opy_:
                    return
                bstack1l1ll11l11l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack1l1ll111lll_opy_))
                if bstack1l1ll111lll_opy_.get(bstack11111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬቘ")):
                    browser = bstack1l1ll11l111_opy_.bstack1l1ll1111l1_opy_(bstack1l1ll11l11l_opy_)
                    return browser
                else:
                    args = list(args)
                    args[0] = bstack1l1ll11l11l_opy_
                    return connect(bstack1l1ll11l111_opy_, *args, **kwargs)
        return wrapped
    def bstack1l1ll1111ll_opy_(
        self,
        f: bstack1llllll1lll_opy_,
        bstack1ll11l11ll1_opy_: object,
        exec: Tuple[bstack111111ll1l_opy_, str],
        bstack1111111111_opy_: Tuple[bstack1111111l1l_opy_, bstack1111l11l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11111l_opy_ (u"ࠢ࡯ࡧࡺࡣࡵࡧࡧࡦࠤ቙"):
            return
        if not bstack1ll111l1lll_opy_():
            self.logger.debug(bstack11111l_opy_ (u"ࠣࡔࡨࡸࡺࡸ࡮ࡪࡰࡪࠤ࡮ࡴࠠ࡯ࡧࡺࡣࡵࡧࡧࡦࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢቚ"))
            return
        def wrapped(bstack1ll11l11ll1_opy_, bstack1l1l1llllll_opy_, *args, **kwargs):
            contexts = bstack1ll11l11ll1_opy_.browser.contexts
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                                if bstack11111l_opy_ (u"ࠤࡤࡦࡴࡻࡴ࠻ࡤ࡯ࡥࡳࡱࠢቛ") in page.url:
                                    return page
                    else:
                        return bstack1l1l1llllll_opy_(bstack1ll11l11ll1_opy_)
        return wrapped
    def bstack1l1ll111l11_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        self.logger.debug(bstack11111l_opy_ (u"ࠥࡶࡪ࡭ࡩࡴࡶࡨࡶࡤࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱ࡭ࡹࡀࠠࠣቜ") + str(req) + bstack11111l_opy_ (u"ࠦࠧቝ"))
        try:
            r = self.bstack1lll11l11ll_opy_.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack11111l_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࡳࡶࡥࡦࡩࡸࡹ࠽ࠣ቞") + str(r.success) + bstack11111l_opy_ (u"ࠨࠢ቟"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11111l_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧበ") + str(e) + bstack11111l_opy_ (u"ࠣࠤቡ"))
            traceback.print_exc()
            raise e
    def bstack1l1ll11l1ll_opy_(
        self,
        f: bstack1llllll1lll_opy_,
        Connection: object,
        exec: Tuple[bstack111111ll1l_opy_, str],
        bstack1111111111_opy_: Tuple[bstack1111111l1l_opy_, bstack1111l11l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11111l_opy_ (u"ࠤࡢࡷࡪࡴࡤࡠ࡯ࡨࡷࡸࡧࡧࡦࡡࡷࡳࡤࡹࡥࡳࡸࡨࡶࠧቢ"):
            return
        if not bstack1ll111l1lll_opy_():
            return
        def wrapped(Connection, bstack1l1l1llll11_opy_, *args, **kwargs):
            return bstack1l1l1llll11_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack1llllll1lll_opy_,
        bstack1l1ll11l111_opy_: object,
        exec: Tuple[bstack111111ll1l_opy_, str],
        bstack1111111111_opy_: Tuple[bstack1111111l1l_opy_, bstack1111l11l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack11111l_opy_ (u"ࠥࡧࡱࡵࡳࡦࠤባ"):
            return
        if not bstack1ll111l1lll_opy_():
            self.logger.debug(bstack11111l_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡧࡱࡵࡳࡦࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢቤ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped