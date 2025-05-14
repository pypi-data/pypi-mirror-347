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
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack11ll1ll1l1_opy_ import get_logger
logger = get_logger(__name__)
bstack111l1ll1ll1_opy_: Dict[str, float] = {}
bstack111l1lll111_opy_: List = []
bstack111l1ll111l_opy_ = 5
bstack1lll1ll1_opy_ = os.path.join(os.getcwd(), bstack11111l_opy_ (u"ࠨ࡮ࡲ࡫ࠬᴒ"), bstack11111l_opy_ (u"ࠩ࡮ࡩࡾ࠳࡭ࡦࡶࡵ࡭ࡨࡹ࠮࡫ࡵࡲࡲࠬᴓ"))
logging.getLogger(bstack11111l_opy_ (u"ࠪࡪ࡮ࡲࡥ࡭ࡱࡦ࡯ࠬᴔ")).setLevel(logging.WARNING)
lock = FileLock(bstack1lll1ll1_opy_+bstack11111l_opy_ (u"ࠦ࠳ࡲ࡯ࡤ࡭ࠥᴕ"))
class bstack111l1ll1lll_opy_:
    duration: float
    name: str
    startTime: float
    worker: int
    status: bool
    failure: str
    details: Optional[str]
    entryType: str
    platform: Optional[int]
    command: Optional[str]
    hookType: Optional[str]
    cli: Optional[bool]
    def __init__(self, duration: float, name: str, start_time: float, bstack111l1ll1l1l_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack111l1ll1l1l_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack11111l_opy_ (u"ࠧࡳࡥࡢࡵࡸࡶࡪࠨᴖ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1lllll11lll_opy_:
    global bstack111l1ll1ll1_opy_
    @staticmethod
    def bstack1ll1l11l111_opy_(key: str):
        bstack1ll1ll111ll_opy_ = bstack1lllll11lll_opy_.bstack11llll1lll1_opy_(key)
        bstack1lllll11lll_opy_.mark(bstack1ll1ll111ll_opy_+bstack11111l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᴗ"))
        return bstack1ll1ll111ll_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack111l1ll1ll1_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack11111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࡀࠠࡼࡿࠥᴘ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1lllll11lll_opy_.mark(end)
            bstack1lllll11lll_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack11111l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣ࡯ࡪࡿࠠ࡮ࡧࡷࡶ࡮ࡩࡳ࠻ࠢࡾࢁࠧᴙ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack111l1ll1ll1_opy_ or end not in bstack111l1ll1ll1_opy_:
                logger.debug(bstack11111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸࡺࡡࡳࡶࠣ࡯ࡪࡿࠠࡸ࡫ࡷ࡬ࠥࡼࡡ࡭ࡷࡨࠤࢀࢃࠠࡰࡴࠣࡩࡳࡪࠠ࡬ࡧࡼࠤࡼ࡯ࡴࡩࠢࡹࡥࡱࡻࡥࠡࡽࢀࠦᴚ").format(start,end))
                return
            duration: float = bstack111l1ll1ll1_opy_[end] - bstack111l1ll1ll1_opy_[start]
            bstack111l1ll1l11_opy_ = os.environ.get(bstack11111l_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡌࡗࡤࡘࡕࡏࡐࡌࡒࡌࠨᴛ"), bstack11111l_opy_ (u"ࠦ࡫ࡧ࡬ࡴࡧࠥᴜ")).lower() == bstack11111l_opy_ (u"ࠧࡺࡲࡶࡧࠥᴝ")
            bstack111l1ll11l1_opy_: bstack111l1ll1lll_opy_ = bstack111l1ll1lll_opy_(duration, label, bstack111l1ll1ll1_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack11111l_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝ࠨᴞ"), 0), command, test_name, hook_type, bstack111l1ll1l11_opy_)
            del bstack111l1ll1ll1_opy_[start]
            del bstack111l1ll1ll1_opy_[end]
            bstack1lllll11lll_opy_.bstack111l1lll11l_opy_(bstack111l1ll11l1_opy_)
        except Exception as e:
            logger.debug(bstack11111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡥࡢࡵࡸࡶ࡮ࡴࡧࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࡀࠠࡼࡿࠥᴟ").format(e))
    @staticmethod
    def bstack111l1lll11l_opy_(bstack111l1ll11l1_opy_):
        os.makedirs(os.path.dirname(bstack1lll1ll1_opy_)) if not os.path.exists(os.path.dirname(bstack1lll1ll1_opy_)) else None
        bstack1lllll11lll_opy_.bstack111l1ll1111_opy_()
        try:
            with lock:
                with open(bstack1lll1ll1_opy_, bstack11111l_opy_ (u"ࠣࡴ࠮ࠦᴠ"), encoding=bstack11111l_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᴡ")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack111l1ll11l1_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack111l1ll11ll_opy_:
            logger.debug(bstack11111l_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠤࢀࢃࠢᴢ").format(bstack111l1ll11ll_opy_))
            with lock:
                with open(bstack1lll1ll1_opy_, bstack11111l_opy_ (u"ࠦࡼࠨᴣ"), encoding=bstack11111l_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᴤ")) as file:
                    data = [bstack111l1ll11l1_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack11111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡭ࡨࡽࠥࡳࡥࡵࡴ࡬ࡧࡸࠦࡡࡱࡲࡨࡲࡩࠦࡻࡾࠤᴥ").format(str(e)))
        finally:
            if os.path.exists(bstack1lll1ll1_opy_+bstack11111l_opy_ (u"ࠢ࠯࡮ࡲࡧࡰࠨᴦ")):
                os.remove(bstack1lll1ll1_opy_+bstack11111l_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢᴧ"))
    @staticmethod
    def bstack111l1ll1111_opy_():
        attempt = 0
        while (attempt < bstack111l1ll111l_opy_):
            attempt += 1
            if os.path.exists(bstack1lll1ll1_opy_+bstack11111l_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣᴨ")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11llll1lll1_opy_(label: str) -> str:
        try:
            return bstack11111l_opy_ (u"ࠥࡿࢂࡀࡻࡾࠤᴩ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack11111l_opy_ (u"ࠦࡊࡸࡲࡰࡴ࠽ࠤࢀࢃࠢᴪ").format(e))