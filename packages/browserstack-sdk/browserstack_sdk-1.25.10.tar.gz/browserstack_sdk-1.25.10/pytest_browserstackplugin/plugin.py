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
import atexit
import datetime
import inspect
import logging
import signal
import threading
from uuid import uuid4
from bstack_utils.measure import bstack1lll11ll11_opy_
from bstack_utils.percy_sdk import PercySDK
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1l11ll1111_opy_, bstack1ll11llll1_opy_, update, bstack1l111l11l_opy_,
                                       bstack11l11ll11_opy_, bstack1111ll11l_opy_, bstack1ll11lllll_opy_, bstack1llllll11l_opy_,
                                       bstack111l1l11l_opy_, bstack1l1ll11l11_opy_, bstack11l1l1l1_opy_, bstack1lll1l1lll_opy_,
                                       bstack1l1ll11111_opy_, getAccessibilityResults, getAccessibilityResultsSummary, perform_scan, bstack1lll1lll_opy_)
from browserstack_sdk.bstack1l11l1ll1_opy_ import bstack1llllll11_opy_
from browserstack_sdk._version import __version__
from bstack_utils import bstack11ll1ll1l1_opy_
from bstack_utils.capture import bstack11l111l111_opy_
from bstack_utils.config import Config
from bstack_utils.percy import *
from bstack_utils.constants import bstack1ll11ll11l_opy_, bstack1l1llllll_opy_, bstack1lll1l11l1_opy_, \
    bstack1l111l1l1l_opy_
from bstack_utils.helper import bstack11l11llll1_opy_, bstack11l1lll1lll_opy_, bstack111l11llll_opy_, bstack11l11l111_opy_, bstack1ll111l1lll_opy_, bstack1l11l1lll_opy_, \
    bstack11l11lll1ll_opy_, \
    bstack11l1ll1llll_opy_, bstack1lllll11l1_opy_, bstack1lll1lll11_opy_, bstack11ll11111ll_opy_, bstack11lll111ll_opy_, Notset, \
    bstack11llll11l_opy_, bstack11l1lllllll_opy_, bstack11l1l1llll1_opy_, Result, bstack11l1l1lll1l_opy_, bstack11ll11l1lll_opy_, bstack111l1lllll_opy_, \
    bstack111l1llll_opy_, bstack1lllll1111_opy_, bstack11ll11l11_opy_, bstack11l1l111l11_opy_
from bstack_utils.bstack11l11l1l1ll_opy_ import bstack11l11l11l11_opy_
from bstack_utils.messages import bstack1ll11l1l11_opy_, bstack11ll1111l_opy_, bstack1l11llllll_opy_, bstack1111l11l1_opy_, bstack11l1l1l1l1_opy_, \
    bstack1lll1llll1_opy_, bstack1l1l11l11l_opy_, bstack1ll1l111l1_opy_, bstack1llll111_opy_, bstack11l1l111_opy_, \
    bstack111ll1ll_opy_, bstack11lll1lll_opy_
from bstack_utils.proxy import bstack1l11ll11ll_opy_, bstack1l111lll1_opy_
from bstack_utils.bstack1ll1l1l1_opy_ import bstack111l1l11l11_opy_, bstack111l1l11111_opy_, bstack111l11ll1ll_opy_, bstack111l11lll1l_opy_, \
    bstack111l1l11l1l_opy_, bstack111l11lll11_opy_, bstack111l1l111ll_opy_, bstack1lllll1l1_opy_, bstack111l1l1l111_opy_
from bstack_utils.bstack11lll1l1l1_opy_ import bstack11111ll1l_opy_
from bstack_utils.bstack1l1111ll11_opy_ import bstack11l1llll_opy_, bstack1llll1111_opy_, bstack1lll1ll11l_opy_, \
    bstack111ll11l1_opy_, bstack1l1l1l111_opy_
from bstack_utils.bstack111lllllll_opy_ import bstack11l111lll1_opy_
from bstack_utils.bstack11l111llll_opy_ import bstack1l1ll11l1l_opy_
import bstack_utils.accessibility as bstack11l1ll1l1_opy_
from bstack_utils.bstack111lll1lll_opy_ import bstack1111lll11_opy_
from bstack_utils.bstack1l1l1ll111_opy_ import bstack1l1l1ll111_opy_
from browserstack_sdk.__init__ import bstack1lll1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1ll11_opy_ import bstack1lll111l111_opy_
from browserstack_sdk.sdk_cli.bstack1111l1l1_opy_ import bstack1111l1l1_opy_, bstack1l1ll1llll_opy_, bstack1ll11lll11_opy_
from browserstack_sdk.sdk_cli.test_framework import bstack1l11l1l11l1_opy_, bstack1lll11l1ll1_opy_, bstack1ll1lll1lll_opy_
from browserstack_sdk.sdk_cli.cli import cli
from browserstack_sdk.sdk_cli.bstack1111l1l1_opy_ import bstack1111l1l1_opy_, bstack1l1ll1llll_opy_, bstack1ll11lll11_opy_
bstack1l11l111l_opy_ = None
bstack1ll1111111_opy_ = None
bstack1ll1lll1l1_opy_ = None
bstack1l1ll11l1_opy_ = None
bstack11lll1ll11_opy_ = None
bstack1l111l1l11_opy_ = None
bstack1l1l1111_opy_ = None
bstack1l1l111l1_opy_ = None
bstack11ll11ll_opy_ = None
bstack1l1ll1l111_opy_ = None
bstack1ll111111_opy_ = None
bstack1lll1111ll_opy_ = None
bstack1l1ll1ll1_opy_ = None
bstack1lll11l11l_opy_ = bstack11111l_opy_ (u"ࠧࠨὲ")
CONFIG = {}
bstack1lllll1ll_opy_ = False
bstack1l1l111ll_opy_ = bstack11111l_opy_ (u"ࠨࠩέ")
bstack11l1lll1ll_opy_ = bstack11111l_opy_ (u"ࠩࠪὴ")
bstack1l11ll111l_opy_ = False
bstack1lll1l1l1l_opy_ = []
bstack111l1l1ll_opy_ = bstack1ll11ll11l_opy_
bstack11111ll1111_opy_ = bstack11111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪή")
bstack1lll111111_opy_ = {}
bstack1lllll11ll_opy_ = None
bstack1l1111l1_opy_ = False
logger = bstack11ll1ll1l1_opy_.get_logger(__name__, bstack111l1l1ll_opy_)
store = {
    bstack11111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨὶ"): []
}
bstack1111l11l111_opy_ = False
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_111l11l11l_opy_ = {}
current_test_uuid = None
cli_context = bstack1l11l1l11l1_opy_(
    test_framework_name=bstack1lll111l11_opy_[bstack11111l_opy_ (u"ࠬࡖ࡙ࡕࡇࡖࡘ࠲ࡈࡄࡅࠩί")] if bstack11lll111ll_opy_() else bstack1lll111l11_opy_[bstack11111l_opy_ (u"࠭ࡐ࡚ࡖࡈࡗ࡙࠭ὸ")],
    test_framework_version=pytest.__version__,
    platform_index=-1,
)
def bstack1l111111_opy_(page, bstack1l11ll1ll1_opy_):
    try:
        page.evaluate(bstack11111l_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣό"),
                      bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬὺ") + json.dumps(
                          bstack1l11ll1ll1_opy_) + bstack11111l_opy_ (u"ࠤࢀࢁࠧύ"))
    except Exception as e:
        print(bstack11111l_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣὼ"), e)
def bstack1l1l111lll_opy_(page, message, level):
    try:
        page.evaluate(bstack11111l_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧώ"), bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ὾") + json.dumps(
            message) + bstack11111l_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩ὿") + json.dumps(level) + bstack11111l_opy_ (u"ࠧࡾࡿࠪᾀ"))
    except Exception as e:
        print(bstack11111l_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦᾁ"), e)
def pytest_configure(config):
    global bstack1l1l111ll_opy_
    global CONFIG
    bstack1l11l11ll1_opy_ = Config.bstack1l11l111_opy_()
    config.args = bstack1l1ll11l1l_opy_.bstack1111l11l11l_opy_(config.args)
    bstack1l11l11ll1_opy_.bstack1llll11l1l_opy_(bstack11ll11l11_opy_(config.getoption(bstack11111l_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᾂ"))))
    try:
        bstack11ll1ll1l1_opy_.bstack11l1111ll11_opy_(config.inipath, config.rootpath)
    except:
        pass
    if cli.is_running():
        bstack1111l1l1_opy_.invoke(bstack1l1ll1llll_opy_.CONNECT, bstack1ll11lll11_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᾃ"), bstack11111l_opy_ (u"ࠫ࠵࠭ᾄ")))
        config = json.loads(os.environ.get(bstack11111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡕࡎࡇࡋࡊࠦᾅ"), bstack11111l_opy_ (u"ࠨࡻࡾࠤᾆ")))
        cli.bstack1lll1l1ll1l_opy_(bstack1lll1lll11_opy_(bstack1l1l111ll_opy_, CONFIG), cli_context.platform_index, bstack1l111l11l_opy_)
    if cli.bstack1llll11lll1_opy_(bstack1lll111l111_opy_):
        cli.bstack1lll1l1l1l1_opy_()
        logger.debug(bstack11111l_opy_ (u"ࠢࡄࡎࡌࠤ࡮ࡹࠠࡢࡥࡷ࡭ࡻ࡫ࠠࡧࡱࡵࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࠨᾇ") + str(cli_context.platform_index) + bstack11111l_opy_ (u"ࠣࠤᾈ"))
        cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_.BEFORE_ALL, bstack1ll1lll1lll_opy_.PRE, config)
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    when = getattr(call, bstack11111l_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᾉ"), None)
    if cli.is_running() and when == bstack11111l_opy_ (u"ࠥࡧࡦࡲ࡬ࠣᾊ"):
        cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_.LOG_REPORT, bstack1ll1lll1lll_opy_.PRE, item, call)
    outcome = yield
    if cli.is_running():
        if when == bstack11111l_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࠥᾋ"):
            cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_.BEFORE_EACH, bstack1ll1lll1lll_opy_.POST, item, call, outcome)
        elif when == bstack11111l_opy_ (u"ࠧࡩࡡ࡭࡮ࠥᾌ"):
            cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_.LOG_REPORT, bstack1ll1lll1lll_opy_.POST, item, call, outcome)
        elif when == bstack11111l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᾍ"):
            cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_.AFTER_EACH, bstack1ll1lll1lll_opy_.POST, item, call, outcome)
        return # skip all existing bstack1111l11111l_opy_
    skipSessionName = item.config.getoption(bstack11111l_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᾎ"))
    plugins = item.config.getoption(bstack11111l_opy_ (u"ࠣࡲ࡯ࡹ࡬࡯࡮ࡴࠤᾏ"))
    report = outcome.get_result()
    bstack11111llll1l_opy_(item, call, report)
    if bstack11111l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠢᾐ") not in plugins or bstack11lll111ll_opy_():
        return
    summary = []
    driver = getattr(item, bstack11111l_opy_ (u"ࠥࡣࡩࡸࡩࡷࡧࡵࠦᾑ"), None)
    page = getattr(item, bstack11111l_opy_ (u"ࠦࡤࡶࡡࡨࡧࠥᾒ"), None)
    try:
        if (driver == None or driver.session_id == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None or cli.is_running()):
        bstack11111l1ll1l_opy_(item, report, summary, skipSessionName)
    if (page is not None):
        bstack11111l1l1ll_opy_(item, report, summary, skipSessionName)
def bstack11111l1ll1l_opy_(item, report, summary, skipSessionName):
    if report.when == bstack11111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᾓ") and report.skipped:
        bstack111l1l1l111_opy_(report)
    if report.when in [bstack11111l_opy_ (u"ࠨࡳࡦࡶࡸࡴࠧᾔ"), bstack11111l_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᾕ")]:
        return
    if not bstack1ll111l1lll_opy_():
        return
    try:
        if (str(skipSessionName).lower() != bstack11111l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᾖ") and not cli.is_running()):
            item._driver.execute_script(
                bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࠨࡡࡤࡶ࡬ࡳࡳࠨ࠺ࠡࠤࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨ࡮ࡢ࡯ࡨࠦ࠿ࠦࠧᾗ") + json.dumps(
                    report.nodeid) + bstack11111l_opy_ (u"ࠪࢁࢂ࠭ᾘ"))
        os.environ[bstack11111l_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧᾙ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack11111l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡱࡦࡸ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫࠺ࠡࡽ࠳ࢁࠧᾚ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11111l_opy_ (u"ࠨࡷࡢࡵࡻࡪࡦ࡯࡬ࠣᾛ")))
    bstack1lllllllll_opy_ = bstack11111l_opy_ (u"ࠢࠣᾜ")
    bstack111l1l1l111_opy_(report)
    if not passed:
        try:
            bstack1lllllllll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack11111l_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡩࡥ࡮ࡲࡵࡳࡧࠣࡶࡪࡧࡳࡰࡰ࠽ࠤࢀ࠶ࡽࠣᾝ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1lllllllll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack11111l_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᾞ")))
        bstack1lllllllll_opy_ = bstack11111l_opy_ (u"ࠥࠦᾟ")
        if not passed:
            try:
                bstack1lllllllll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11111l_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦᾠ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1lllllllll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩᾡ")
                    + json.dumps(bstack11111l_opy_ (u"ࠨࡰࡢࡵࡶࡩࡩࠧࠢᾢ"))
                    + bstack11111l_opy_ (u"ࠢ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࢀࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࠥᾣ")
                )
            else:
                item._driver.execute_script(
                    bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥ࠰ࠥࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡪࡡࡵࡣࠥ࠾ࠥ࠭ᾤ")
                    + json.dumps(str(bstack1lllllllll_opy_))
                    + bstack11111l_opy_ (u"ࠤ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࠧᾥ")
                )
        except Exception as e:
            summary.append(bstack11111l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡣࡱࡲࡴࡺࡡࡵࡧ࠽ࠤࢀ࠶ࡽࠣᾦ").format(e))
def bstack1111l111111_opy_(test_name, error_message):
    try:
        bstack11111llllll_opy_ = []
        bstack1llll1l1ll_opy_ = os.environ.get(bstack11111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᾧ"), bstack11111l_opy_ (u"ࠬ࠶ࠧᾨ"))
        bstack1l1111lll1_opy_ = {bstack11111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᾩ"): test_name, bstack11111l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᾪ"): error_message, bstack11111l_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧᾫ"): bstack1llll1l1ll_opy_}
        bstack1111l111lll_opy_ = os.path.join(tempfile.gettempdir(), bstack11111l_opy_ (u"ࠩࡳࡻࡤࡶࡹࡵࡧࡶࡸࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧᾬ"))
        if os.path.exists(bstack1111l111lll_opy_):
            with open(bstack1111l111lll_opy_) as f:
                bstack11111llllll_opy_ = json.load(f)
        bstack11111llllll_opy_.append(bstack1l1111lll1_opy_)
        with open(bstack1111l111lll_opy_, bstack11111l_opy_ (u"ࠪࡻࠬᾭ")) as f:
            json.dump(bstack11111llllll_opy_, f)
    except Exception as e:
        logger.debug(bstack11111l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡰࡦࡴࡶ࡭ࡸࡺࡩ࡯ࡩࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡱࡻࡷࡩࡸࡺࠠࡦࡴࡵࡳࡷࡹ࠺ࠡࠩᾮ") + str(e))
def bstack11111l1l1ll_opy_(item, report, summary, skipSessionName):
    if report.when in [bstack11111l_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᾯ"), bstack11111l_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᾰ")]:
        return
    if (str(skipSessionName).lower() != bstack11111l_opy_ (u"ࠧࡵࡴࡸࡩࠬᾱ")):
        bstack1l111111_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack11111l_opy_ (u"ࠣࡹࡤࡷࡽ࡬ࡡࡪ࡮ࠥᾲ")))
    bstack1lllllllll_opy_ = bstack11111l_opy_ (u"ࠤࠥᾳ")
    bstack111l1l1l111_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1lllllllll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack11111l_opy_ (u"࡛ࠥࡆࡘࡎࡊࡐࡊ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤ࡫ࡧࡩ࡭ࡷࡵࡩࠥࡸࡥࡢࡵࡲࡲ࠿ࠦࡻ࠱ࡿࠥᾴ").format(e)
                )
        try:
            if passed:
                bstack1l1l1l111_opy_(getattr(item, bstack11111l_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪ᾵"), None), bstack11111l_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧᾶ"))
            else:
                error_message = bstack11111l_opy_ (u"࠭ࠧᾷ")
                if bstack1lllllllll_opy_:
                    bstack1l1l111lll_opy_(item._page, str(bstack1lllllllll_opy_), bstack11111l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨᾸ"))
                    bstack1l1l1l111_opy_(getattr(item, bstack11111l_opy_ (u"ࠨࡡࡳࡥ࡬࡫ࠧᾹ"), None), bstack11111l_opy_ (u"ࠤࡩࡥ࡮ࡲࡥࡥࠤᾺ"), str(bstack1lllllllll_opy_))
                    error_message = str(bstack1lllllllll_opy_)
                else:
                    bstack1l1l1l111_opy_(getattr(item, bstack11111l_opy_ (u"ࠪࡣࡵࡧࡧࡦࠩΆ"), None), bstack11111l_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦᾼ"))
                bstack1111l111111_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack11111l_opy_ (u"ࠧ࡝ࡁࡓࡐࡌࡒࡌࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡹࡵࡪࡡࡵࡧࠣࡷࡪࡹࡳࡪࡱࡱࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࢁ࠰ࡾࠤ᾽").format(e))
def pytest_addoption(parser):
    parser.addoption(bstack11111l_opy_ (u"ࠨ࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥι"), default=bstack11111l_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨ᾿"), help=bstack11111l_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡦࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠢ῀"))
    parser.addoption(bstack11111l_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡕࡷࡥࡹࡻࡳࠣ῁"), default=bstack11111l_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤῂ"), help=bstack11111l_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥῃ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack11111l_opy_ (u"ࠧ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠢῄ"), action=bstack11111l_opy_ (u"ࠨࡳࡵࡱࡵࡩࠧ῅"), default=bstack11111l_opy_ (u"ࠢࡤࡪࡵࡳࡲ࡫ࠢῆ"),
                         help=bstack11111l_opy_ (u"ࠣࡆࡵ࡭ࡻ࡫ࡲࠡࡶࡲࠤࡷࡻ࡮ࠡࡶࡨࡷࡹࡹࠢῇ"))
def bstack111lllll11_opy_(log):
    if not (log[bstack11111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪῈ")] and log[bstack11111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫΈ")].strip()):
        return
    active = bstack111llll1ll_opy_()
    log = {
        bstack11111l_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪῊ"): log[bstack11111l_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫΉ")],
        bstack11111l_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩῌ"): bstack111l11llll_opy_().isoformat() + bstack11111l_opy_ (u"࡛ࠧࠩ῍"),
        bstack11111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ῎"): log[bstack11111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ῏")],
    }
    if active:
        if active[bstack11111l_opy_ (u"ࠪࡸࡾࡶࡥࠨῐ")] == bstack11111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩῑ"):
            log[bstack11111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬῒ")] = active[bstack11111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ΐ")]
        elif active[bstack11111l_opy_ (u"ࠧࡵࡻࡳࡩࠬ῔")] == bstack11111l_opy_ (u"ࠨࡶࡨࡷࡹ࠭῕"):
            log[bstack11111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩῖ")] = active[bstack11111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪῗ")]
    bstack1111lll11_opy_.bstack1l1lll1111_opy_([log])
def bstack111llll1ll_opy_():
    if len(store[bstack11111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨῘ")]) > 0 and store[bstack11111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩῙ")][-1]:
        return {
            bstack11111l_opy_ (u"࠭ࡴࡺࡲࡨࠫῚ"): bstack11111l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬΊ"),
            bstack11111l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ῜"): store[bstack11111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭῝")][-1]
        }
    if store.get(bstack11111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ῞"), None):
        return {
            bstack11111l_opy_ (u"ࠫࡹࡿࡰࡦࠩ῟"): bstack11111l_opy_ (u"ࠬࡺࡥࡴࡶࠪῠ"),
            bstack11111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ῡ"): store[bstack11111l_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫῢ")]
        }
    return None
def pytest_runtest_logstart(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_.INIT_TEST, bstack1ll1lll1lll_opy_.PRE, nodeid, location)
def pytest_runtest_logfinish(nodeid, location):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_.INIT_TEST, bstack1ll1lll1lll_opy_.POST, nodeid, location)
def pytest_runtest_call(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_.TEST, bstack1ll1lll1lll_opy_.PRE, item)
        return
    try:
        global CONFIG
        item._11111lll1l1_opy_ = True
        bstack1111l111_opy_ = bstack11l1ll1l1_opy_.bstack11l111ll_opy_(bstack11l1ll1llll_opy_(item.own_markers))
        if not cli.bstack1llll11lll1_opy_(bstack1lll111l111_opy_):
            item._a11y_test_case = bstack1111l111_opy_
            if bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧΰ"), None):
                driver = getattr(item, bstack11111l_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪῤ"), None)
                item._a11y_started = bstack11l1ll1l1_opy_.bstack1lll1l11_opy_(driver, bstack1111l111_opy_)
        if not bstack1111lll11_opy_.on() or bstack11111ll1111_opy_ != bstack11111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪῥ"):
            return
        global current_test_uuid #, bstack11l11111l1_opy_
        bstack111l111ll1_opy_ = {
            bstack11111l_opy_ (u"ࠫࡺࡻࡩࡥࠩῦ"): uuid4().__str__(),
            bstack11111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩῧ"): bstack111l11llll_opy_().isoformat() + bstack11111l_opy_ (u"࡚࠭ࠨῨ")
        }
        current_test_uuid = bstack111l111ll1_opy_[bstack11111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬῩ")]
        store[bstack11111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬῪ")] = bstack111l111ll1_opy_[bstack11111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧΎ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _111l11l11l_opy_[item.nodeid] = {**_111l11l11l_opy_[item.nodeid], **bstack111l111ll1_opy_}
        bstack11111ll1l11_opy_(item, _111l11l11l_opy_[item.nodeid], bstack11111l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫῬ"))
    except Exception as err:
        print(bstack11111l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡨࡧ࡬࡭࠼ࠣࡿࢂ࠭῭"), str(err))
def pytest_runtest_setup(item):
    store[bstack11111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ΅")] = item
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_.BEFORE_EACH, bstack1ll1lll1lll_opy_.PRE, item, bstack11111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࠬ`"))
        return # skip all existing bstack1111l11111l_opy_
    global bstack1111l11l111_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11ll11111ll_opy_():
        atexit.register(bstack1l11l1111l_opy_)
        if not bstack1111l11l111_opy_:
            try:
                bstack11111l1ll11_opy_ = [signal.SIGINT, signal.SIGTERM]
                if not bstack11l1l111l11_opy_():
                    bstack11111l1ll11_opy_.extend([signal.SIGHUP, signal.SIGQUIT])
                for s in bstack11111l1ll11_opy_:
                    signal.signal(s, bstack11111ll1l1l_opy_)
                bstack1111l11l111_opy_ = True
            except Exception as e:
                logger.debug(
                    bstack11111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡵࡩ࡬࡯ࡳࡵࡧࡵࠤࡸ࡯ࡧ࡯ࡣ࡯ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡶࡸࡀࠠࠣ῰") + str(e))
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack111l1l11l11_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack11111l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ῱")
    try:
        if not bstack1111lll11_opy_.on():
            return
        uuid = uuid4().__str__()
        bstack111l111ll1_opy_ = {
            bstack11111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧῲ"): uuid,
            bstack11111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧῳ"): bstack111l11llll_opy_().isoformat() + bstack11111l_opy_ (u"ࠫ࡟࠭ῴ"),
            bstack11111l_opy_ (u"ࠬࡺࡹࡱࡧࠪ῵"): bstack11111l_opy_ (u"࠭ࡨࡰࡱ࡮ࠫῶ"),
            bstack11111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪῷ"): bstack11111l_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭Ὸ"),
            bstack11111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡯ࡣࡰࡩࠬΌ"): bstack11111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩῺ")
        }
        threading.current_thread().current_hook_uuid = uuid
        threading.current_thread().current_test_item = item
        store[bstack11111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨΏ")] = item
        store[bstack11111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩῼ")] = [uuid]
        if not _111l11l11l_opy_.get(item.nodeid, None):
            _111l11l11l_opy_[item.nodeid] = {bstack11111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬ´"): [], bstack11111l_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ῾"): []}
        _111l11l11l_opy_[item.nodeid][bstack11111l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ῿")].append(bstack111l111ll1_opy_[bstack11111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ ")])
        _111l11l11l_opy_[item.nodeid + bstack11111l_opy_ (u"ࠪ࠱ࡸ࡫ࡴࡶࡲࠪ ")] = bstack111l111ll1_opy_
        bstack11111ll11l1_opy_(item, bstack111l111ll1_opy_, bstack11111l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ "))
    except Exception as err:
        print(bstack11111l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡹࡥࡵࡷࡳ࠾ࠥࢁࡽࠨ "), str(err))
def pytest_runtest_teardown(item):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_.TEST, bstack1ll1lll1lll_opy_.POST, item)
        cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_.AFTER_EACH, bstack1ll1lll1lll_opy_.PRE, item, bstack11111l_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ "))
        return # skip all existing bstack1111l11111l_opy_
    try:
        global bstack1lll111111_opy_
        bstack1llll1l1ll_opy_ = 0
        if bstack1l11ll111l_opy_ is True:
            bstack1llll1l1ll_opy_ = int(os.environ.get(bstack11111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧ ")))
        if bstack1l1111111l_opy_.bstack111l1ll1l_opy_() == bstack11111l_opy_ (u"ࠣࡶࡵࡹࡪࠨ "):
            if bstack1l1111111l_opy_.bstack11llll1ll_opy_() == bstack11111l_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ "):
                bstack11111lll11l_opy_ = bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠪࡴࡪࡸࡣࡺࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ "), None)
                bstack1l111l1111_opy_ = bstack11111lll11l_opy_ + bstack11111l_opy_ (u"ࠦ࠲ࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ ")
                driver = getattr(item, bstack11111l_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭ "), None)
                bstack1l1l11llll_opy_ = getattr(item, bstack11111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ​"), None)
                bstack1lll11ll_opy_ = getattr(item, bstack11111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ‌"), None)
                PercySDK.screenshot(driver, bstack1l111l1111_opy_, bstack1l1l11llll_opy_=bstack1l1l11llll_opy_, bstack1lll11ll_opy_=bstack1lll11ll_opy_, bstack1ll111l1l1_opy_=bstack1llll1l1ll_opy_)
        if not cli.bstack1llll11lll1_opy_(bstack1lll111l111_opy_):
            if getattr(item, bstack11111l_opy_ (u"ࠨࡡࡤ࠵࠶ࡿ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨ‍"), False):
                bstack1llllll11_opy_.bstack1ll1111ll_opy_(getattr(item, bstack11111l_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ‎"), None), bstack1lll111111_opy_, logger, item)
        if not bstack1111lll11_opy_.on():
            return
        bstack111l111ll1_opy_ = {
            bstack11111l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ‏"): uuid4().__str__(),
            bstack11111l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ‐"): bstack111l11llll_opy_().isoformat() + bstack11111l_opy_ (u"ࠬࡠࠧ‑"),
            bstack11111l_opy_ (u"࠭ࡴࡺࡲࡨࠫ‒"): bstack11111l_opy_ (u"ࠧࡩࡱࡲ࡯ࠬ–"),
            bstack11111l_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫ—"): bstack11111l_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡇࡄࡇࡍ࠭―"),
            bstack11111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭‖"): bstack11111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭‗")
        }
        _111l11l11l_opy_[item.nodeid + bstack11111l_opy_ (u"ࠬ࠳ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨ‘")] = bstack111l111ll1_opy_
        bstack11111ll11l1_opy_(item, bstack111l111ll1_opy_, bstack11111l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ’"))
    except Exception as err:
        print(bstack11111l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡲࡶࡰࡷࡩࡸࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯࠼ࠣࡿࢂ࠭‚"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if bstack111l11lll1l_opy_(fixturedef.argname):
        store[bstack11111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧ‛")] = request.node
    elif bstack111l1l11l1l_opy_(fixturedef.argname):
        store[bstack11111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡧࡱࡧࡳࡴࡡ࡬ࡸࡪࡳࠧ“")] = request.node
    if not bstack1111lll11_opy_.on():
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_.SETUP_FIXTURE, bstack1ll1lll1lll_opy_.PRE, fixturedef, request)
        outcome = yield
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_.SETUP_FIXTURE, bstack1ll1lll1lll_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1111l11111l_opy_
    start_time = datetime.datetime.now()
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_.SETUP_FIXTURE, bstack1ll1lll1lll_opy_.PRE, fixturedef, request)
    outcome = yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_.SETUP_FIXTURE, bstack1ll1lll1lll_opy_.POST, fixturedef, request, outcome)
        return # skip all existing bstack1111l11111l_opy_
    try:
        fixture = {
            bstack11111l_opy_ (u"ࠪࡲࡦࡳࡥࠨ”"): fixturedef.argname,
            bstack11111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ„"): bstack11l11lll1ll_opy_(outcome),
            bstack11111l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ‟"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        current_test_item = store[bstack11111l_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤ࡯ࡴࡦ࡯ࠪ†")]
        if not _111l11l11l_opy_.get(current_test_item.nodeid, None):
            _111l11l11l_opy_[current_test_item.nodeid] = {bstack11111l_opy_ (u"ࠧࡧ࡫ࡻࡸࡺࡸࡥࡴࠩ‡"): []}
        _111l11l11l_opy_[current_test_item.nodeid][bstack11111l_opy_ (u"ࠨࡨ࡬ࡼࡹࡻࡲࡦࡵࠪ•")].append(fixture)
    except Exception as err:
        logger.debug(bstack11111l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡶࡩࡹࡻࡰ࠻ࠢࡾࢁࠬ‣"), str(err))
if bstack11lll111ll_opy_() and bstack1111lll11_opy_.on():
    def pytest_bdd_before_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_.STEP, bstack1ll1lll1lll_opy_.PRE, request, step)
            return
        try:
            _111l11l11l_opy_[request.node.nodeid][bstack11111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭․")].bstack1ll1l1ll11_opy_(id(step))
        except Exception as err:
            print(bstack11111l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴ࠿ࠦࡻࡾࠩ‥"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_.STEP, bstack1ll1lll1lll_opy_.POST, request, step, exception)
            return
        try:
            _111l11l11l_opy_[request.node.nodeid][bstack11111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ…")].bstack111llll1l1_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack11111l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪ‧"), str(err))
    def pytest_bdd_after_step(request, step):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_.STEP, bstack1ll1lll1lll_opy_.POST, request, step)
            return
        try:
            bstack111lllllll_opy_: bstack11l111lll1_opy_ = _111l11l11l_opy_[request.node.nodeid][bstack11111l_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ ")]
            bstack111lllllll_opy_.bstack111llll1l1_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack11111l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱࡻࡷࡩࡸࡺ࡟ࡣࡦࡧࡣࡸࡺࡥࡱࡡࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠬ "), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack11111ll1111_opy_
        try:
            if not bstack1111lll11_opy_.on() or bstack11111ll1111_opy_ != bstack11111l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭‪"):
                return
            if cli.is_running():
                cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_.TEST, bstack1ll1lll1lll_opy_.PRE, request, feature, scenario)
                return
            driver = bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩ‫"), None)
            if not _111l11l11l_opy_.get(request.node.nodeid, None):
                _111l11l11l_opy_[request.node.nodeid] = {}
            bstack111lllllll_opy_ = bstack11l111lll1_opy_.bstack111l111111l_opy_(
                scenario, feature, request.node,
                name=bstack111l11lll11_opy_(request.node, scenario),
                started_at=bstack1l11l1lll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack11111l_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷ࠱ࡨࡻࡣࡶ࡯ࡥࡩࡷ࠭‬"),
                tags=bstack111l1l111ll_opy_(feature, scenario),
                bstack11l11111ll_opy_=bstack1111lll11_opy_.bstack111llllll1_opy_(driver) if driver and driver.session_id else {}
            )
            _111l11l11l_opy_[request.node.nodeid][bstack11111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨ‭")] = bstack111lllllll_opy_
            bstack11111ll1ll1_opy_(bstack111lllllll_opy_.uuid)
            bstack1111lll11_opy_.bstack111lllll1l_opy_(bstack11111l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ‮"), bstack111lllllll_opy_)
        except Exception as err:
            print(bstack11111l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡢࡥࡦࡢࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳ࠿ࠦࡻࡾࠩ "), str(err))
def bstack1111l111ll1_opy_(bstack11l1111111_opy_):
    if bstack11l1111111_opy_ in store[bstack11111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬ‰")]:
        store[bstack11111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭‱")].remove(bstack11l1111111_opy_)
def bstack11111ll1ll1_opy_(test_uuid):
    store[bstack11111l_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ′")] = test_uuid
    threading.current_thread().current_test_uuid = test_uuid
@bstack1111lll11_opy_.bstack1111lll111l_opy_
def bstack11111llll1l_opy_(item, call, report):
    logger.debug(bstack11111l_opy_ (u"ࠫ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡴࡶࡤࡶࡹ࠭″"))
    global bstack11111ll1111_opy_
    bstack1l11l1lll1_opy_ = bstack1l11l1lll_opy_()
    if hasattr(report, bstack11111l_opy_ (u"ࠬࡹࡴࡰࡲࠪ‴")):
        bstack1l11l1lll1_opy_ = bstack11l1l1lll1l_opy_(report.stop)
    elif hasattr(report, bstack11111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࠬ‵")):
        bstack1l11l1lll1_opy_ = bstack11l1l1lll1l_opy_(report.start)
    try:
        if getattr(report, bstack11111l_opy_ (u"ࠧࡸࡪࡨࡲࠬ‶"), bstack11111l_opy_ (u"ࠨࠩ‷")) == bstack11111l_opy_ (u"ࠩࡦࡥࡱࡲࠧ‸"):
            logger.debug(bstack11111l_opy_ (u"ࠪ࡬ࡦࡴࡤ࡭ࡧࡢࡳ࠶࠷ࡹࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡳࡵࡣࡷࡩࠥ࠳ࠠࡼࡿ࠯ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࠮ࠢࡾࢁࠬ‹").format(getattr(report, bstack11111l_opy_ (u"ࠫࡼ࡮ࡥ࡯ࠩ›"), bstack11111l_opy_ (u"ࠬ࠭※")).__str__(), bstack11111ll1111_opy_))
            if bstack11111ll1111_opy_ == bstack11111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭‼"):
                _111l11l11l_opy_[item.nodeid][bstack11111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ‽")] = bstack1l11l1lll1_opy_
                bstack11111ll1l11_opy_(item, _111l11l11l_opy_[item.nodeid], bstack11111l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ‾"), report, call)
                store[bstack11111l_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭‿")] = None
            elif bstack11111ll1111_opy_ == bstack11111l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢ⁀"):
                bstack111lllllll_opy_ = _111l11l11l_opy_[item.nodeid][bstack11111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⁁")]
                bstack111lllllll_opy_.set(hooks=_111l11l11l_opy_[item.nodeid].get(bstack11111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫ⁂"), []))
                exception, bstack111lll1ll1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack111lll1ll1_opy_ = [call.excinfo.exconly(), getattr(report, bstack11111l_opy_ (u"࠭࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠬ⁃"), bstack11111l_opy_ (u"ࠧࠨ⁄"))]
                bstack111lllllll_opy_.stop(time=bstack1l11l1lll1_opy_, result=Result(result=getattr(report, bstack11111l_opy_ (u"ࠨࡱࡸࡸࡨࡵ࡭ࡦࠩ⁅"), bstack11111l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⁆")), exception=exception, bstack111lll1ll1_opy_=bstack111lll1ll1_opy_))
                bstack1111lll11_opy_.bstack111lllll1l_opy_(bstack11111l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⁇"), _111l11l11l_opy_[item.nodeid][bstack11111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ⁈")])
        elif getattr(report, bstack11111l_opy_ (u"ࠬࡽࡨࡦࡰࠪ⁉"), bstack11111l_opy_ (u"࠭ࠧ⁊")) in [bstack11111l_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭⁋"), bstack11111l_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࠪ⁌")]:
            logger.debug(bstack11111l_opy_ (u"ࠩ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡹࡴࡢࡶࡨࠤ࠲ࠦࡻࡾ࠮ࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦ࠭ࠡࡽࢀࠫ⁍").format(getattr(report, bstack11111l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ⁎"), bstack11111l_opy_ (u"ࠫࠬ⁏")).__str__(), bstack11111ll1111_opy_))
            bstack111llll111_opy_ = item.nodeid + bstack11111l_opy_ (u"ࠬ࠳ࠧ⁐") + getattr(report, bstack11111l_opy_ (u"࠭ࡷࡩࡧࡱࠫ⁑"), bstack11111l_opy_ (u"ࠧࠨ⁒"))
            if getattr(report, bstack11111l_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩ⁓"), False):
                hook_type = bstack11111l_opy_ (u"ࠩࡅࡉࡋࡕࡒࡆࡡࡈࡅࡈࡎࠧ⁔") if getattr(report, bstack11111l_opy_ (u"ࠪࡻ࡭࡫࡮ࠨ⁕"), bstack11111l_opy_ (u"ࠫࠬ⁖")) == bstack11111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ⁗") else bstack11111l_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ⁘")
                _111l11l11l_opy_[bstack111llll111_opy_] = {
                    bstack11111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ⁙"): uuid4().__str__(),
                    bstack11111l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⁚"): bstack1l11l1lll1_opy_,
                    bstack11111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ⁛"): hook_type
                }
            _111l11l11l_opy_[bstack111llll111_opy_][bstack11111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⁜")] = bstack1l11l1lll1_opy_
            bstack1111l111ll1_opy_(_111l11l11l_opy_[bstack111llll111_opy_][bstack11111l_opy_ (u"ࠫࡺࡻࡩࡥࠩ⁝")])
            bstack11111ll11l1_opy_(item, _111l11l11l_opy_[bstack111llll111_opy_], bstack11111l_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⁞"), report, call)
            if getattr(report, bstack11111l_opy_ (u"࠭ࡷࡩࡧࡱࠫ "), bstack11111l_opy_ (u"ࠧࠨ⁠")) == bstack11111l_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧ⁡"):
                if getattr(report, bstack11111l_opy_ (u"ࠩࡲࡹࡹࡩ࡯࡮ࡧࠪ⁢"), bstack11111l_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ⁣")) == bstack11111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⁤"):
                    bstack111l111ll1_opy_ = {
                        bstack11111l_opy_ (u"ࠬࡻࡵࡪࡦࠪ⁥"): uuid4().__str__(),
                        bstack11111l_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⁦"): bstack1l11l1lll_opy_(),
                        bstack11111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⁧"): bstack1l11l1lll_opy_()
                    }
                    _111l11l11l_opy_[item.nodeid] = {**_111l11l11l_opy_[item.nodeid], **bstack111l111ll1_opy_}
                    bstack11111ll1l11_opy_(item, _111l11l11l_opy_[item.nodeid], bstack11111l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⁨"))
                    bstack11111ll1l11_opy_(item, _111l11l11l_opy_[item.nodeid], bstack11111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⁩"), report, call)
    except Exception as err:
        print(bstack11111l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡥࡳࡪ࡬ࡦࡡࡲ࠵࠶ࡿ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࢁࡽࠨ⁪"), str(err))
def bstack1111l1111l1_opy_(test, bstack111l111ll1_opy_, result=None, call=None, bstack1111111l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack111lllllll_opy_ = {
        bstack11111l_opy_ (u"ࠫࡺࡻࡩࡥࠩ⁫"): bstack111l111ll1_opy_[bstack11111l_opy_ (u"ࠬࡻࡵࡪࡦࠪ⁬")],
        bstack11111l_opy_ (u"࠭ࡴࡺࡲࡨࠫ⁭"): bstack11111l_opy_ (u"ࠧࡵࡧࡶࡸࠬ⁮"),
        bstack11111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭⁯"): test.name,
        bstack11111l_opy_ (u"ࠩࡥࡳࡩࡿࠧ⁰"): {
            bstack11111l_opy_ (u"ࠪࡰࡦࡴࡧࠨⁱ"): bstack11111l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ⁲"),
            bstack11111l_opy_ (u"ࠬࡩ࡯ࡥࡧࠪ⁳"): inspect.getsource(test.obj)
        },
        bstack11111l_opy_ (u"࠭ࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ⁴"): test.name,
        bstack11111l_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭⁵"): test.name,
        bstack11111l_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨ⁶"): bstack1l1ll11l1l_opy_.bstack111ll1l1l1_opy_(test),
        bstack11111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬ⁷"): file_path,
        bstack11111l_opy_ (u"ࠪࡰࡴࡩࡡࡵ࡫ࡲࡲࠬ⁸"): file_path,
        bstack11111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⁹"): bstack11111l_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭⁺"),
        bstack11111l_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫ⁻"): file_path,
        bstack11111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⁼"): bstack111l111ll1_opy_[bstack11111l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ⁽")],
        bstack11111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ⁾"): bstack11111l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪⁿ"),
        bstack11111l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧ₀"): {
            bstack11111l_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩ₁"): test.nodeid
        },
        bstack11111l_opy_ (u"࠭ࡴࡢࡩࡶࠫ₂"): bstack11l1ll1llll_opy_(test.own_markers)
    }
    if bstack1111111l_opy_ in [bstack11111l_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨ₃"), bstack11111l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ₄")]:
        bstack111lllllll_opy_[bstack11111l_opy_ (u"ࠩࡰࡩࡹࡧࠧ₅")] = {
            bstack11111l_opy_ (u"ࠪࡪ࡮ࡾࡴࡶࡴࡨࡷࠬ₆"): bstack111l111ll1_opy_.get(bstack11111l_opy_ (u"ࠫ࡫࡯ࡸࡵࡷࡵࡩࡸ࠭₇"), [])
        }
    if bstack1111111l_opy_ == bstack11111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙࡫ࡪࡲࡳࡩࡩ࠭₈"):
        bstack111lllllll_opy_[bstack11111l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭₉")] = bstack11111l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨ₊")
        bstack111lllllll_opy_[bstack11111l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ₋")] = bstack111l111ll1_opy_[bstack11111l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨ₌")]
        bstack111lllllll_opy_[bstack11111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ₍")] = bstack111l111ll1_opy_[bstack11111l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ₎")]
    if result:
        bstack111lllllll_opy_[bstack11111l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ₏")] = result.outcome
        bstack111lllllll_opy_[bstack11111l_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧₐ")] = result.duration * 1000
        bstack111lllllll_opy_[bstack11111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬₑ")] = bstack111l111ll1_opy_[bstack11111l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ₒ")]
        if result.failed:
            bstack111lllllll_opy_[bstack11111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨₓ")] = bstack1111lll11_opy_.bstack1111ll111l_opy_(call.excinfo.typename)
            bstack111lllllll_opy_[bstack11111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫₔ")] = bstack1111lll11_opy_.bstack1111lll1111_opy_(call.excinfo, result)
        bstack111lllllll_opy_[bstack11111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪₕ")] = bstack111l111ll1_opy_[bstack11111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫₖ")]
    if outcome:
        bstack111lllllll_opy_[bstack11111l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ₗ")] = bstack11l11lll1ll_opy_(outcome)
        bstack111lllllll_opy_[bstack11111l_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨₘ")] = 0
        bstack111lllllll_opy_[bstack11111l_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ₙ")] = bstack111l111ll1_opy_[bstack11111l_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧₚ")]
        if bstack111lllllll_opy_[bstack11111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪₛ")] == bstack11111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫₜ"):
            bstack111lllllll_opy_[bstack11111l_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫ₝")] = bstack11111l_opy_ (u"࠭ࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠧ₞")  # bstack1111l111l11_opy_
            bstack111lllllll_opy_[bstack11111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ₟")] = [{bstack11111l_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ₠"): [bstack11111l_opy_ (u"ࠩࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷ࠭₡")]}]
        bstack111lllllll_opy_[bstack11111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩ₢")] = bstack111l111ll1_opy_[bstack11111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪ₣")]
    return bstack111lllllll_opy_
def bstack1111l111l1l_opy_(test, bstack111lll1l11_opy_, bstack1111111l_opy_, result, call, outcome, bstack11111l1llll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack111lll1l11_opy_[bstack11111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨ₤")]
    hook_name = bstack111lll1l11_opy_[bstack11111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩ₥")]
    hook_data = {
        bstack11111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ₦"): bstack111lll1l11_opy_[bstack11111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭₧")],
        bstack11111l_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ₨"): bstack11111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨ₩"),
        bstack11111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ₪"): bstack11111l_opy_ (u"ࠬࢁࡽࠨ₫").format(bstack111l1l11111_opy_(hook_name)),
        bstack11111l_opy_ (u"࠭ࡢࡰࡦࡼࠫ€"): {
            bstack11111l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬ₭"): bstack11111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ₮"),
            bstack11111l_opy_ (u"ࠩࡦࡳࡩ࡫ࠧ₯"): None
        },
        bstack11111l_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩ₰"): test.name,
        bstack11111l_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫ₱"): bstack1l1ll11l1l_opy_.bstack111ll1l1l1_opy_(test, hook_name),
        bstack11111l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ₲"): file_path,
        bstack11111l_opy_ (u"࠭࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠨ₳"): file_path,
        bstack11111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ₴"): bstack11111l_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ₵"),
        bstack11111l_opy_ (u"ࠩࡹࡧࡤ࡬ࡩ࡭ࡧࡳࡥࡹ࡮ࠧ₶"): file_path,
        bstack11111l_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ₷"): bstack111lll1l11_opy_[bstack11111l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ₸")],
        bstack11111l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ₹"): bstack11111l_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠳ࡣࡶࡥࡸࡱࡧ࡫ࡲࠨ₺") if bstack11111ll1111_opy_ == bstack11111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫ₻") else bstack11111l_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ₼"),
        bstack11111l_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡵࡻࡳࡩࠬ₽"): hook_type
    }
    bstack1111lll1ll1_opy_ = bstack111l1ll1l1_opy_(_111l11l11l_opy_.get(test.nodeid, None))
    if bstack1111lll1ll1_opy_:
        hook_data[bstack11111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤ࡯ࡤࠨ₾")] = bstack1111lll1ll1_opy_
    if result:
        hook_data[bstack11111l_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ₿")] = result.outcome
        hook_data[bstack11111l_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡢࡱࡸ࠭⃀")] = result.duration * 1000
        hook_data[bstack11111l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⃁")] = bstack111lll1l11_opy_[bstack11111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ⃂")]
        if result.failed:
            hook_data[bstack11111l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫ࠧ⃃")] = bstack1111lll11_opy_.bstack1111ll111l_opy_(call.excinfo.typename)
            hook_data[bstack11111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪ⃄")] = bstack1111lll11_opy_.bstack1111lll1111_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack11111l_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪ⃅")] = bstack11l11lll1ll_opy_(outcome)
        hook_data[bstack11111l_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳࡥࡩ࡯ࡡࡰࡷࠬ⃆")] = 100
        hook_data[bstack11111l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⃇")] = bstack111lll1l11_opy_[bstack11111l_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫ⃈")]
        if hook_data[bstack11111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⃉")] == bstack11111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ⃊"):
            hook_data[bstack11111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ⃋")] = bstack11111l_opy_ (u"࡙ࠪࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠫ⃌")  # bstack1111l111l11_opy_
            hook_data[bstack11111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬ⃍")] = [{bstack11111l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨ⃎"): [bstack11111l_opy_ (u"࠭ࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠪ⃏")]}]
    if bstack11111l1llll_opy_:
        hook_data[bstack11111l_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⃐")] = bstack11111l1llll_opy_.result
        hook_data[bstack11111l_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩ⃑")] = bstack11l1lllllll_opy_(bstack111lll1l11_opy_[bstack11111l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ⃒࠭")], bstack111lll1l11_opy_[bstack11111l_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨ⃓")])
        hook_data[bstack11111l_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ⃔")] = bstack111lll1l11_opy_[bstack11111l_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪ⃕")]
        if hook_data[bstack11111l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⃖")] == bstack11111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⃗"):
            hook_data[bstack11111l_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࡡࡷࡽࡵ࡫⃘ࠧ")] = bstack1111lll11_opy_.bstack1111ll111l_opy_(bstack11111l1llll_opy_.exception_type)
            hook_data[bstack11111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧ⃙ࠪ")] = [{bstack11111l_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ⃚࠭"): bstack11l1l1llll1_opy_(bstack11111l1llll_opy_.exception)}]
    return hook_data
def bstack11111ll1l11_opy_(test, bstack111l111ll1_opy_, bstack1111111l_opy_, result=None, call=None, outcome=None):
    logger.debug(bstack11111l_opy_ (u"ࠫࡸ࡫࡮ࡥࡡࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡆࡺࡴࡦ࡯ࡳࡸ࡮ࡴࡧࠡࡶࡲࠤ࡬࡫࡮ࡦࡴࡤࡸࡪࠦࡴࡦࡵࡷࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠣ࠱ࠥࢁࡽࠨ⃛").format(bstack1111111l_opy_))
    bstack111lllllll_opy_ = bstack1111l1111l1_opy_(test, bstack111l111ll1_opy_, result, call, bstack1111111l_opy_, outcome)
    driver = getattr(test, bstack11111l_opy_ (u"ࠬࡥࡤࡳ࡫ࡹࡩࡷ࠭⃜"), None)
    if bstack1111111l_opy_ == bstack11111l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⃝") and driver:
        bstack111lllllll_opy_[bstack11111l_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭⃞")] = bstack1111lll11_opy_.bstack111llllll1_opy_(driver)
    if bstack1111111l_opy_ == bstack11111l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕ࡮࡭ࡵࡶࡥࡥࠩ⃟"):
        bstack1111111l_opy_ = bstack11111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⃠")
    bstack111ll1ll11_opy_ = {
        bstack11111l_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⃡"): bstack1111111l_opy_,
        bstack11111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭⃢"): bstack111lllllll_opy_
    }
    bstack1111lll11_opy_.bstack1l1l1l1l1_opy_(bstack111ll1ll11_opy_)
    if bstack1111111l_opy_ == bstack11111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⃣"):
        threading.current_thread().bstackTestMeta = {bstack11111l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⃤"): bstack11111l_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨ⃥")}
    elif bstack1111111l_opy_ == bstack11111l_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦ⃦ࠪ"):
        threading.current_thread().bstackTestMeta = {bstack11111l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⃧"): getattr(result, bstack11111l_opy_ (u"ࠪࡳࡺࡺࡣࡰ࡯ࡨ⃨ࠫ"), bstack11111l_opy_ (u"ࠫࠬ⃩"))}
def bstack11111ll11l1_opy_(test, bstack111l111ll1_opy_, bstack1111111l_opy_, result=None, call=None, outcome=None, bstack11111l1llll_opy_=None):
    logger.debug(bstack11111l_opy_ (u"ࠬࡹࡥ࡯ࡦࡢ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡫ࠠࡩࡱࡲ࡯ࠥࡪࡡࡵࡣ࠯ࠤࡪࡼࡥ࡯ࡶࡗࡽࡵ࡫ࠠ࠮ࠢࡾࢁ⃪ࠬ").format(bstack1111111l_opy_))
    hook_data = bstack1111l111l1l_opy_(test, bstack111l111ll1_opy_, bstack1111111l_opy_, result, call, outcome, bstack11111l1llll_opy_)
    bstack111ll1ll11_opy_ = {
        bstack11111l_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ⃫ࠪ"): bstack1111111l_opy_,
        bstack11111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯⃬ࠩ"): hook_data
    }
    bstack1111lll11_opy_.bstack1l1l1l1l1_opy_(bstack111ll1ll11_opy_)
def bstack111l1ll1l1_opy_(bstack111l111ll1_opy_):
    if not bstack111l111ll1_opy_:
        return None
    if bstack111l111ll1_opy_.get(bstack11111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤ⃭ࠫ"), None):
        return getattr(bstack111l111ll1_opy_[bstack11111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥ⃮ࠬ")], bstack11111l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ⃯"), None)
    return bstack111l111ll1_opy_.get(bstack11111l_opy_ (u"ࠫࡺࡻࡩࡥࠩ⃰"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_.LOG, bstack1ll1lll1lll_opy_.PRE, request, caplog)
    yield
    if cli.is_running():
        cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_.LOG, bstack1ll1lll1lll_opy_.POST, request, caplog)
        return # skip all existing bstack1111l11111l_opy_
    try:
        if not bstack1111lll11_opy_.on():
            return
        places = [bstack11111l_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫ⃱"), bstack11111l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ⃲"), bstack11111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩ⃳")]
        logs = []
        for bstack11111llll11_opy_ in places:
            records = caplog.get_records(bstack11111llll11_opy_)
            bstack11111lll111_opy_ = bstack11111l_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⃴") if bstack11111llll11_opy_ == bstack11111l_opy_ (u"ࠩࡦࡥࡱࡲࠧ⃵") else bstack11111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⃶")
            bstack11111ll111l_opy_ = request.node.nodeid + (bstack11111l_opy_ (u"ࠫࠬ⃷") if bstack11111llll11_opy_ == bstack11111l_opy_ (u"ࠬࡩࡡ࡭࡮ࠪ⃸") else bstack11111l_opy_ (u"࠭࠭ࠨ⃹") + bstack11111llll11_opy_)
            test_uuid = bstack111l1ll1l1_opy_(_111l11l11l_opy_.get(bstack11111ll111l_opy_, None))
            if not test_uuid:
                continue
            for record in records:
                if bstack11ll11l1lll_opy_(record.message):
                    continue
                logs.append({
                    bstack11111l_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ⃺"): bstack11l1lll1lll_opy_(record.created).isoformat() + bstack11111l_opy_ (u"ࠨ࡜ࠪ⃻"),
                    bstack11111l_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⃼"): record.levelname,
                    bstack11111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⃽"): record.message,
                    bstack11111lll111_opy_: test_uuid
                })
        if len(logs) > 0:
            bstack1111lll11_opy_.bstack1l1lll1111_opy_(logs)
    except Exception as err:
        print(bstack11111l_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡩ࡯࡯ࡦࡢࡪ࡮ࡾࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ⃾"), str(err))
def bstack1ll1l111l_opy_(sequence, driver_command, response=None, driver = None, args = None):
    global bstack1l1111l1_opy_
    bstack1l1lll1ll_opy_ = bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ⃿"), None) and bstack11l11llll1_opy_(
            threading.current_thread(), bstack11111l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ℀"), None)
    bstack11111ll11_opy_ = getattr(driver, bstack11111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ℁"), None) != None and getattr(driver, bstack11111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨℂ"), None) == True
    if sequence == bstack11111l_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩ℃") and driver != None:
      if not bstack1l1111l1_opy_ and bstack1ll111l1lll_opy_() and bstack11111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ℄") in CONFIG and CONFIG[bstack11111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ℅")] == True and bstack1l1l1ll111_opy_.bstack11l1l1l111_opy_(driver_command) and (bstack11111ll11_opy_ or bstack1l1lll1ll_opy_) and not bstack1lll1lll_opy_(args):
        try:
          bstack1l1111l1_opy_ = True
          logger.debug(bstack11111l_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࢀࢃࠧ℆").format(driver_command))
          logger.debug(perform_scan(driver, driver_command=driver_command))
        except Exception as err:
          logger.debug(bstack11111l_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡷࡨࡧ࡮ࠡࡽࢀࠫℇ").format(str(err)))
        bstack1l1111l1_opy_ = False
    if sequence == bstack11111l_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭℈"):
        if driver_command == bstack11111l_opy_ (u"ࠨࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠬ℉"):
            bstack1111lll11_opy_.bstack1ll1ll11_opy_({
                bstack11111l_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨℊ"): response[bstack11111l_opy_ (u"ࠪࡺࡦࡲࡵࡦࠩℋ")],
                bstack11111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫℌ"): store[bstack11111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩℍ")]
            })
def bstack1l11l1111l_opy_():
    global bstack1lll1l1l1l_opy_
    bstack11ll1ll1l1_opy_.bstack111l1lll_opy_()
    logging.shutdown()
    bstack1111lll11_opy_.bstack111l1llll1_opy_()
    for driver in bstack1lll1l1l1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11111ll1l1l_opy_(*args):
    global bstack1lll1l1l1l_opy_
    bstack1111lll11_opy_.bstack111l1llll1_opy_()
    for driver in bstack1lll1l1l1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack11ll1ll1ll_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack111l111l_opy_(self, *args, **kwargs):
    bstack11ll11lll_opy_ = bstack1l11l111l_opy_(self, *args, **kwargs)
    bstack1lll11111_opy_ = getattr(threading.current_thread(), bstack11111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡚ࡥࡴࡶࡐࡩࡹࡧࠧℎ"), None)
    if bstack1lll11111_opy_ and bstack1lll11111_opy_.get(bstack11111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧℏ"), bstack11111l_opy_ (u"ࠨࠩℐ")) == bstack11111l_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪℑ"):
        bstack1111lll11_opy_.bstack111lllll1_opy_(self)
    return bstack11ll11lll_opy_
@measure(event_name=EVENTS.bstack1ll1l11l_opy_, stage=STAGE.bstack1ll111l1_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack11l11l11l_opy_(framework_name):
    from bstack_utils.config import Config
    bstack1l11l11ll1_opy_ = Config.bstack1l11l111_opy_()
    if bstack1l11l11ll1_opy_.get_property(bstack11111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧℒ")):
        return
    bstack1l11l11ll1_opy_.bstack1111ll11_opy_(bstack11111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡲࡵࡤࡠࡥࡤࡰࡱ࡫ࡤࠨℓ"), True)
    global bstack1lll11l11l_opy_
    global bstack1l1lllll1_opy_
    bstack1lll11l11l_opy_ = framework_name
    logger.info(bstack11lll1lll_opy_.format(bstack1lll11l11l_opy_.split(bstack11111l_opy_ (u"ࠬ࠳ࠧ℔"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack1ll111l1lll_opy_():
            Service.start = bstack1ll11lllll_opy_
            Service.stop = bstack1llllll11l_opy_
            webdriver.Remote.get = bstack11llll111_opy_
            webdriver.Remote.__init__ = bstack11ll1llll_opy_
            if not isinstance(os.getenv(bstack11111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖ࡙ࡕࡇࡖࡘࡤࡖࡁࡓࡃࡏࡐࡊࡒࠧℕ")), str):
                return
            WebDriver.close = bstack111l1l11l_opy_
            WebDriver.quit = bstack1l1ll1111l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.get_accessibility_results = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
            WebDriver.performScan = perform_scan
            WebDriver.perform_scan = perform_scan
        elif bstack1111lll11_opy_.on():
            webdriver.Remote.__init__ = bstack111l111l_opy_
        bstack1l1lllll1_opy_ = True
    except Exception as e:
        pass
    if os.environ.get(bstack11111l_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬ№")):
        bstack1l1lllll1_opy_ = eval(os.environ.get(bstack11111l_opy_ (u"ࠨࡕࡈࡐࡊࡔࡉࡖࡏࡢࡓࡗࡥࡐࡍࡃ࡜࡛ࡗࡏࡇࡉࡖࡢࡍࡓ࡙ࡔࡂࡎࡏࡉࡉ࠭℗")))
    if not bstack1l1lllll1_opy_:
        bstack11l1l1l1_opy_(bstack11111l_opy_ (u"ࠤࡓࡥࡨࡱࡡࡨࡧࡶࠤࡳࡵࡴࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠦ℘"), bstack111ll1ll_opy_)
    if bstack11l1lll1l_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._1ll1111l_opy_ = bstack1ll11l1ll_opy_
        except Exception as e:
            logger.error(bstack1lll1llll1_opy_.format(str(e)))
    if bstack11111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪℙ") in str(framework_name).lower():
        if not bstack1ll111l1lll_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack11l11ll11_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1111ll11l_opy_
            Config.getoption = bstack1l1l1llll1_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1l111lllll_opy_
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l11lllll_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack1l1ll1111l_opy_(self):
    global bstack1lll11l11l_opy_
    global bstack11llll1l1_opy_
    global bstack1ll1111111_opy_
    try:
        if bstack11111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫℚ") in bstack1lll11l11l_opy_ and self.session_id != None and bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩℛ"), bstack11111l_opy_ (u"࠭ࠧℜ")) != bstack11111l_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨℝ"):
            bstack11llll1111_opy_ = bstack11111l_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨ℞") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack11111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ℟")
            bstack1lllll1111_opy_(logger, True)
            if self != None:
                bstack111ll11l1_opy_(self, bstack11llll1111_opy_, bstack11111l_opy_ (u"ࠪ࠰ࠥ࠭℠").join(threading.current_thread().bstackTestErrorMessages))
        if not cli.bstack1llll11lll1_opy_(bstack1lll111l111_opy_):
            item = store.get(bstack11111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨ℡"), None)
            if item is not None and bstack11l11llll1_opy_(threading.current_thread(), bstack11111l_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ™"), None):
                bstack1llllll11_opy_.bstack1ll1111ll_opy_(self, bstack1lll111111_opy_, logger, item)
        threading.current_thread().testStatus = bstack11111l_opy_ (u"࠭ࠧ℣")
    except Exception as e:
        logger.debug(bstack11111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡳࡵࡣࡷࡹࡸࡀࠠࠣℤ") + str(e))
    bstack1ll1111111_opy_(self)
    self.session_id = None
@measure(event_name=EVENTS.bstack1l1ll1ll11_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack11ll1llll_opy_(self, command_executor,
             desired_capabilities=None, bstack11ll1l11_opy_=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack11llll1l1_opy_
    global bstack1lllll11ll_opy_
    global bstack1l11ll111l_opy_
    global bstack1lll11l11l_opy_
    global bstack1l11l111l_opy_
    global bstack1lll1l1l1l_opy_
    global bstack1l1l111ll_opy_
    global bstack11l1lll1ll_opy_
    global bstack1lll111111_opy_
    CONFIG[bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪ℥")] = str(bstack1lll11l11l_opy_) + str(__version__)
    command_executor = bstack1lll1lll11_opy_(bstack1l1l111ll_opy_, CONFIG)
    logger.debug(bstack1111l11l1_opy_.format(command_executor))
    proxy = bstack1l1ll11111_opy_(CONFIG, proxy)
    bstack1llll1l1ll_opy_ = 0
    try:
        if bstack1l11ll111l_opy_ is True:
            bstack1llll1l1ll_opy_ = int(os.environ.get(bstack11111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩΩ")))
    except:
        bstack1llll1l1ll_opy_ = 0
    bstack1111l1111_opy_ = bstack1l11ll1111_opy_(CONFIG, bstack1llll1l1ll_opy_)
    logger.debug(bstack1ll1l111l1_opy_.format(str(bstack1111l1111_opy_)))
    bstack1lll111111_opy_ = CONFIG.get(bstack11111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭℧"))[bstack1llll1l1ll_opy_]
    if bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨℨ") in CONFIG and CONFIG[bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩ℩")]:
        bstack1lll1ll11l_opy_(bstack1111l1111_opy_, bstack11l1lll1ll_opy_)
    if bstack11l1ll1l1_opy_.bstack111l111ll_opy_(CONFIG, bstack1llll1l1ll_opy_) and bstack11l1ll1l1_opy_.bstack1ll1ll111l_opy_(bstack1111l1111_opy_, options, desired_capabilities):
        threading.current_thread().a11yPlatform = True
        if not cli.bstack1llll11lll1_opy_(bstack1lll111l111_opy_):
            bstack11l1ll1l1_opy_.set_capabilities(bstack1111l1111_opy_, CONFIG)
    if desired_capabilities:
        bstack1l1ll1ll1l_opy_ = bstack1ll11llll1_opy_(desired_capabilities)
        bstack1l1ll1ll1l_opy_[bstack11111l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭K")] = bstack11llll11l_opy_(CONFIG)
        bstack11l1l111l1_opy_ = bstack1l11ll1111_opy_(bstack1l1ll1ll1l_opy_)
        if bstack11l1l111l1_opy_:
            bstack1111l1111_opy_ = update(bstack11l1l111l1_opy_, bstack1111l1111_opy_)
        desired_capabilities = None
    if options:
        bstack1l1ll11l11_opy_(options, bstack1111l1111_opy_)
    if not options:
        options = bstack1l111l11l_opy_(bstack1111l1111_opy_)
    if proxy and bstack1lllll11l1_opy_() >= version.parse(bstack11111l_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧÅ")):
        options.proxy(proxy)
    if options and bstack1lllll11l1_opy_() >= version.parse(bstack11111l_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧℬ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1lllll11l1_opy_() < version.parse(bstack11111l_opy_ (u"ࠩ࠶࠲࠽࠴࠰ࠨℭ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack1111l1111_opy_)
    logger.info(bstack1l11llllll_opy_)
    bstack1lll11ll11_opy_.end(EVENTS.bstack1ll1l11l_opy_.value, EVENTS.bstack1ll1l11l_opy_.value + bstack11111l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ℮"),
                               EVENTS.bstack1ll1l11l_opy_.value + bstack11111l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤℯ"), True, None)
    if bstack1lllll11l1_opy_() >= version.parse(bstack11111l_opy_ (u"ࠬ࠺࠮࠲࠲࠱࠴ࠬℰ")):
        bstack1l11l111l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1lllll11l1_opy_() >= version.parse(bstack11111l_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬℱ")):
        bstack1l11l111l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  bstack11ll1l11_opy_=bstack11ll1l11_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1lllll11l1_opy_() >= version.parse(bstack11111l_opy_ (u"ࠧ࠳࠰࠸࠷࠳࠶ࠧℲ")):
        bstack1l11l111l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack11ll1l11_opy_=bstack11ll1l11_opy_, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack1l11l111l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  bstack11ll1l11_opy_=bstack11ll1l11_opy_, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1l1ll1l1_opy_ = bstack11111l_opy_ (u"ࠨࠩℳ")
        if bstack1lllll11l1_opy_() >= version.parse(bstack11111l_opy_ (u"ࠩ࠷࠲࠵࠴࠰ࡣ࠳ࠪℴ")):
            bstack1l1ll1l1_opy_ = self.caps.get(bstack11111l_opy_ (u"ࠥࡳࡵࡺࡩ࡮ࡣ࡯ࡌࡺࡨࡕࡳ࡮ࠥℵ"))
        else:
            bstack1l1ll1l1_opy_ = self.capabilities.get(bstack11111l_opy_ (u"ࠦࡴࡶࡴࡪ࡯ࡤࡰࡍࡻࡢࡖࡴ࡯ࠦℶ"))
        if bstack1l1ll1l1_opy_:
            bstack111l1llll_opy_(bstack1l1ll1l1_opy_)
            if bstack1lllll11l1_opy_() <= version.parse(bstack11111l_opy_ (u"ࠬ࠹࠮࠲࠵࠱࠴ࠬℷ")):
                self.command_executor._url = bstack11111l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࠢℸ") + bstack1l1l111ll_opy_ + bstack11111l_opy_ (u"ࠢ࠻࠺࠳࠳ࡼࡪ࠯ࡩࡷࡥࠦℹ")
            else:
                self.command_executor._url = bstack11111l_opy_ (u"ࠣࡪࡷࡸࡵࡹ࠺࠰࠱ࠥ℺") + bstack1l1ll1l1_opy_ + bstack11111l_opy_ (u"ࠤ࠲ࡻࡩ࠵ࡨࡶࡤࠥ℻")
            logger.debug(bstack11ll1111l_opy_.format(bstack1l1ll1l1_opy_))
        else:
            logger.debug(bstack1ll11l1l11_opy_.format(bstack11111l_opy_ (u"ࠥࡓࡵࡺࡩ࡮ࡣ࡯ࠤࡍࡻࡢࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦℼ")))
    except Exception as e:
        logger.debug(bstack1ll11l1l11_opy_.format(e))
    bstack11llll1l1_opy_ = self.session_id
    if bstack11111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫℽ") in bstack1lll11l11l_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        item = store.get(bstack11111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩℾ"), None)
        if item:
            bstack1111l1111ll_opy_ = getattr(item, bstack11111l_opy_ (u"࠭࡟ࡵࡧࡶࡸࡤࡩࡡࡴࡧࡢࡷࡹࡧࡲࡵࡧࡧࠫℿ"), False)
            if not getattr(item, bstack11111l_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨ⅀"), None) and bstack1111l1111ll_opy_:
                setattr(store[bstack11111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡪࡶࡨࡱࠬ⅁")], bstack11111l_opy_ (u"ࠩࡢࡨࡷ࡯ࡶࡦࡴࠪ⅂"), self)
        bstack1lll11111_opy_ = getattr(threading.current_thread(), bstack11111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡗࡩࡸࡺࡍࡦࡶࡤࠫ⅃"), None)
        if bstack1lll11111_opy_ and bstack1lll11111_opy_.get(bstack11111l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ⅄"), bstack11111l_opy_ (u"ࠬ࠭ⅅ")) == bstack11111l_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧⅆ"):
            bstack1111lll11_opy_.bstack111lllll1_opy_(self)
    bstack1lll1l1l1l_opy_.append(self)
    if bstack11111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪⅇ") in CONFIG and bstack11111l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ⅈ") in CONFIG[bstack11111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬⅉ")][bstack1llll1l1ll_opy_]:
        bstack1lllll11ll_opy_ = CONFIG[bstack11111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭⅊")][bstack1llll1l1ll_opy_][bstack11111l_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ⅋")]
    logger.debug(bstack11l1l111_opy_.format(bstack11llll1l1_opy_))
@measure(event_name=EVENTS.bstack11lll111l_opy_, stage=STAGE.bstack1l1llll11_opy_, bstack1l1ll1ll_opy_=bstack1lllll11ll_opy_)
def bstack11llll111_opy_(self, url):
    global bstack11ll11ll_opy_
    global CONFIG
    try:
        bstack1llll1111_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack1llll111_opy_.format(str(err)))
    try:
        bstack11ll11ll_opy_(self, url)
    except Exception as e:
        try:
            bstack1llll11l_opy_ = str(e)
            if any(err_msg in bstack1llll11l_opy_ for err_msg in bstack1lll1l11l1_opy_):
                bstack1llll1111_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack1llll111_opy_.format(str(err)))
        raise e
def bstack1lll1l11ll_opy_(item, when):
    global bstack1lll1111ll_opy_
    try:
        bstack1lll1111ll_opy_(item, when)
    except Exception as e:
        pass
def bstack1l111lllll_opy_(item, call, rep):
    global bstack1l1ll1ll1_opy_
    global bstack1lll1l1l1l_opy_
    name = bstack11111l_opy_ (u"ࠬ࠭⅌")
    try:
        if rep.when == bstack11111l_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ⅍"):
            bstack11llll1l1_opy_ = threading.current_thread().bstackSessionId
            skipSessionName = item.config.getoption(bstack11111l_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩⅎ"))
            try:
                if (str(skipSessionName).lower() != bstack11111l_opy_ (u"ࠨࡶࡵࡹࡪ࠭⅏")):
                    name = str(rep.nodeid)
                    bstack111ll1l1l_opy_ = bstack11l1llll_opy_(bstack11111l_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪ⅐"), name, bstack11111l_opy_ (u"ࠪࠫ⅑"), bstack11111l_opy_ (u"ࠫࠬ⅒"), bstack11111l_opy_ (u"ࠬ࠭⅓"), bstack11111l_opy_ (u"࠭ࠧ⅔"))
                    os.environ[bstack11111l_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪ⅕")] = name
                    for driver in bstack1lll1l1l1l_opy_:
                        if bstack11llll1l1_opy_ == driver.session_id:
                            driver.execute_script(bstack111ll1l1l_opy_)
            except Exception as e:
                logger.debug(bstack11111l_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨ⅖").format(str(e)))
            try:
                bstack1lllll1l1_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack11111l_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ⅗"):
                    status = bstack11111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ⅘") if rep.outcome.lower() == bstack11111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ⅙") else bstack11111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬ⅚")
                    reason = bstack11111l_opy_ (u"࠭ࠧ⅛")
                    if status == bstack11111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ⅜"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack11111l_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭⅝") if status == bstack11111l_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ⅞") else bstack11111l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ⅟")
                    data = name + bstack11111l_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭Ⅰ") if status == bstack11111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬⅡ") else name + bstack11111l_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩⅢ") + reason
                    bstack1l1l1l1lll_opy_ = bstack11l1llll_opy_(bstack11111l_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩⅣ"), bstack11111l_opy_ (u"ࠨࠩⅤ"), bstack11111l_opy_ (u"ࠩࠪⅥ"), bstack11111l_opy_ (u"ࠪࠫⅦ"), level, data)
                    for driver in bstack1lll1l1l1l_opy_:
                        if bstack11llll1l1_opy_ == driver.session_id:
                            driver.execute_script(bstack1l1l1l1lll_opy_)
            except Exception as e:
                logger.debug(bstack11111l_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨⅧ").format(str(e)))
    except Exception as e:
        logger.debug(bstack11111l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩⅨ").format(str(e)))
    bstack1l1ll1ll1_opy_(item, call, rep)
notset = Notset()
def bstack1l1l1llll1_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1ll111111_opy_
    if str(name).lower() == bstack11111l_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭Ⅹ"):
        return bstack11111l_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨⅪ")
    else:
        return bstack1ll111111_opy_(self, name, default, skip)
def bstack1ll11l1ll_opy_(self):
    global CONFIG
    global bstack1l1l1111_opy_
    try:
        proxy = bstack1l11ll11ll_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack11111l_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭Ⅻ")):
                proxies = bstack1l111lll1_opy_(proxy, bstack1lll1lll11_opy_())
                if len(proxies) > 0:
                    protocol, bstack11ll1llll1_opy_ = proxies.popitem()
                    if bstack11111l_opy_ (u"ࠤ࠽࠳࠴ࠨⅬ") in bstack11ll1llll1_opy_:
                        return bstack11ll1llll1_opy_
                    else:
                        return bstack11111l_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦⅭ") + bstack11ll1llll1_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack11111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡱࡴࡲࡼࡾࠦࡵࡳ࡮ࠣ࠾ࠥࢁࡽࠣⅮ").format(str(e)))
    return bstack1l1l1111_opy_(self)
def bstack11l1lll1l_opy_():
    return (bstack11111l_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨⅯ") in CONFIG or bstack11111l_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪⅰ") in CONFIG) and bstack11l11l111_opy_() and bstack1lllll11l1_opy_() >= version.parse(
        bstack1l1llllll_opy_)
def bstack11l1l1l1l_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1lllll11ll_opy_
    global bstack1l11ll111l_opy_
    global bstack1lll11l11l_opy_
    CONFIG[bstack11111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩⅱ")] = str(bstack1lll11l11l_opy_) + str(__version__)
    bstack1llll1l1ll_opy_ = 0
    try:
        if bstack1l11ll111l_opy_ is True:
            bstack1llll1l1ll_opy_ = int(os.environ.get(bstack11111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨⅲ")))
    except:
        bstack1llll1l1ll_opy_ = 0
    CONFIG[bstack11111l_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣⅳ")] = True
    bstack1111l1111_opy_ = bstack1l11ll1111_opy_(CONFIG, bstack1llll1l1ll_opy_)
    logger.debug(bstack1ll1l111l1_opy_.format(str(bstack1111l1111_opy_)))
    if CONFIG.get(bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧⅴ")):
        bstack1lll1ll11l_opy_(bstack1111l1111_opy_, bstack11l1lll1ll_opy_)
    if bstack11111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧⅵ") in CONFIG and bstack11111l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪⅶ") in CONFIG[bstack11111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩⅷ")][bstack1llll1l1ll_opy_]:
        bstack1lllll11ll_opy_ = CONFIG[bstack11111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪⅸ")][bstack1llll1l1ll_opy_][bstack11111l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ⅹ")]
    import urllib
    import json
    if bstack11111l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ⅺ") in CONFIG and str(CONFIG[bstack11111l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧⅻ")]).lower() != bstack11111l_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪⅼ"):
        bstack1lll11ll1l_opy_ = bstack1lll1lll1_opy_()
        bstack1l111l111l_opy_ = bstack1lll11ll1l_opy_ + urllib.parse.quote(json.dumps(bstack1111l1111_opy_))
    else:
        bstack1l111l111l_opy_ = bstack11111l_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧⅽ") + urllib.parse.quote(json.dumps(bstack1111l1111_opy_))
    browser = self.connect(bstack1l111l111l_opy_)
    return browser
def bstack1l1111111_opy_():
    global bstack1l1lllll1_opy_
    global bstack1lll11l11l_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11111lll1_opy_
        if not bstack1ll111l1lll_opy_():
            global bstack11l1ll1l1l_opy_
            if not bstack11l1ll1l1l_opy_:
                from bstack_utils.helper import bstack11l1ll1ll1_opy_, bstack1llllllll1_opy_
                bstack11l1ll1l1l_opy_ = bstack11l1ll1ll1_opy_()
                bstack1llllllll1_opy_(bstack1lll11l11l_opy_)
            BrowserType.connect = bstack11111lll1_opy_
            return
        BrowserType.launch = bstack11l1l1l1l_opy_
        bstack1l1lllll1_opy_ = True
    except Exception as e:
        pass
def bstack11111ll11ll_opy_():
    global CONFIG
    global bstack1lllll1ll_opy_
    global bstack1l1l111ll_opy_
    global bstack11l1lll1ll_opy_
    global bstack1l11ll111l_opy_
    global bstack111l1l1ll_opy_
    CONFIG = json.loads(os.environ.get(bstack11111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡏࡏࡈࡌࡋࠬⅾ")))
    bstack1lllll1ll_opy_ = eval(os.environ.get(bstack11111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨⅿ")))
    bstack1l1l111ll_opy_ = os.environ.get(bstack11111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡉࡗࡅࡣ࡚ࡘࡌࠨↀ"))
    bstack1lll1l1lll_opy_(CONFIG, bstack1lllll1ll_opy_)
    bstack111l1l1ll_opy_ = bstack11ll1ll1l1_opy_.bstack1l1ll1l11l_opy_(CONFIG, bstack111l1l1ll_opy_)
    if cli.bstack1111llll1_opy_():
        bstack1111l1l1_opy_.invoke(bstack1l1ll1llll_opy_.CONNECT, bstack1ll11lll11_opy_())
        cli_context.platform_index = int(os.environ.get(bstack11111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩↁ"), bstack11111l_opy_ (u"ࠪ࠴ࠬↂ")))
        cli.bstack1lll1ll1ll1_opy_(cli_context.platform_index)
        cli.bstack1lll1l1ll1l_opy_(bstack1lll1lll11_opy_(bstack1l1l111ll_opy_, CONFIG), cli_context.platform_index, bstack1l111l11l_opy_)
        cli.bstack1lll1l1l1l1_opy_()
        logger.debug(bstack11111l_opy_ (u"ࠦࡈࡒࡉࠡ࡫ࡶࠤࡦࡩࡴࡪࡸࡨࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥↃ") + str(cli_context.platform_index) + bstack11111l_opy_ (u"ࠧࠨↄ"))
        return # skip all existing bstack1111l11111l_opy_
    global bstack1l11l111l_opy_
    global bstack1ll1111111_opy_
    global bstack1ll1lll1l1_opy_
    global bstack1l1ll11l1_opy_
    global bstack11lll1ll11_opy_
    global bstack1l111l1l11_opy_
    global bstack1l1l111l1_opy_
    global bstack11ll11ll_opy_
    global bstack1l1l1111_opy_
    global bstack1ll111111_opy_
    global bstack1lll1111ll_opy_
    global bstack1l1ll1ll1_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack1l11l111l_opy_ = webdriver.Remote.__init__
        bstack1ll1111111_opy_ = WebDriver.quit
        bstack1l1l111l1_opy_ = WebDriver.close
        bstack11ll11ll_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack11111l_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩↅ") in CONFIG or bstack11111l_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫↆ") in CONFIG) and bstack11l11l111_opy_():
        if bstack1lllll11l1_opy_() < version.parse(bstack1l1llllll_opy_):
            logger.error(bstack1l1l11l11l_opy_.format(bstack1lllll11l1_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1l1l1111_opy_ = RemoteConnection._1ll1111l_opy_
            except Exception as e:
                logger.error(bstack1lll1llll1_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1ll111111_opy_ = Config.getoption
        from _pytest import runner
        bstack1lll1111ll_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack11l1l1l1l1_opy_)
    try:
        from pytest_bdd import reporting
        bstack1l1ll1ll1_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack11111l_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩↇ"))
    bstack11l1lll1ll_opy_ = CONFIG.get(bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ↈ"), {}).get(bstack11111l_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ↉"))
    bstack1l11ll111l_opy_ = True
    bstack11l11l11l_opy_(bstack1l111l1l1l_opy_)
if (bstack11ll11111ll_opy_()):
    bstack11111ll11ll_opy_()
@bstack111l1lllll_opy_(class_method=False)
def bstack11111ll1lll_opy_(hook_name, event, bstack1l11lll11ll_opy_=None):
    if hook_name not in [bstack11111l_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬ↊"), bstack11111l_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩ↋"), bstack11111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬ↌"), bstack11111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ↍"), bstack11111l_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭↎"), bstack11111l_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ↏"), bstack11111l_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩ←"), bstack11111l_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭↑")]:
        return
    node = store[bstack11111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ→")]
    if hook_name in [bstack11111l_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬ↓"), bstack11111l_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ↔")]:
        node = store[bstack11111l_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧ↕")]
    elif hook_name in [bstack11111l_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧ↖"), bstack11111l_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫ↗")]:
        node = store[bstack11111l_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩ↘")]
    hook_type = bstack111l11ll1ll_opy_(hook_name)
    if event == bstack11111l_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬ↙"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_[hook_type], bstack1ll1lll1lll_opy_.PRE, node, hook_name)
            return
        uuid = uuid4().__str__()
        bstack111lll1l11_opy_ = {
            bstack11111l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ↚"): uuid,
            bstack11111l_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ↛"): bstack1l11l1lll_opy_(),
            bstack11111l_opy_ (u"ࠨࡶࡼࡴࡪ࠭↜"): bstack11111l_opy_ (u"ࠩ࡫ࡳࡴࡱࠧ↝"),
            bstack11111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭↞"): hook_type,
            bstack11111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧ↟"): hook_name
        }
        store[bstack11111l_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩ↠")].append(uuid)
        bstack11111l1lll1_opy_ = node.nodeid
        if hook_type == bstack11111l_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫ↡"):
            if not _111l11l11l_opy_.get(bstack11111l1lll1_opy_, None):
                _111l11l11l_opy_[bstack11111l1lll1_opy_] = {bstack11111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭↢"): []}
            _111l11l11l_opy_[bstack11111l1lll1_opy_][bstack11111l_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧ↣")].append(bstack111lll1l11_opy_[bstack11111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ↤")])
        _111l11l11l_opy_[bstack11111l1lll1_opy_ + bstack11111l_opy_ (u"ࠪ࠱ࠬ↥") + hook_name] = bstack111lll1l11_opy_
        bstack11111ll11l1_opy_(node, bstack111lll1l11_opy_, bstack11111l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ↦"))
    elif event == bstack11111l_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫ↧"):
        if cli.is_running():
            cli.test_framework.track_event(cli_context, bstack1lll11l1ll1_opy_[hook_type], bstack1ll1lll1lll_opy_.POST, node, None, bstack1l11lll11ll_opy_)
            return
        bstack111llll111_opy_ = node.nodeid + bstack11111l_opy_ (u"࠭࠭ࠨ↨") + hook_name
        _111l11l11l_opy_[bstack111llll111_opy_][bstack11111l_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ↩")] = bstack1l11l1lll_opy_()
        bstack1111l111ll1_opy_(_111l11l11l_opy_[bstack111llll111_opy_][bstack11111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭↪")])
        bstack11111ll11l1_opy_(node, _111l11l11l_opy_[bstack111llll111_opy_], bstack11111l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ↫"), bstack11111l1llll_opy_=bstack1l11lll11ll_opy_)
def bstack11111lll1ll_opy_():
    global bstack11111ll1111_opy_
    if bstack11lll111ll_opy_():
        bstack11111ll1111_opy_ = bstack11111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧ↬")
    else:
        bstack11111ll1111_opy_ = bstack11111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ↭")
@bstack1111lll11_opy_.bstack1111lll111l_opy_
def bstack11111lllll1_opy_():
    bstack11111lll1ll_opy_()
    if cli.is_running():
        try:
            bstack11l11l11l11_opy_(bstack11111ll1lll_opy_)
        except Exception as e:
            logger.debug(bstack11111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡵ࡯࡬ࡵࠣࡴࡦࡺࡣࡩ࠼ࠣࡿࢂࠨ↮").format(e))
        return
    if bstack11l11l111_opy_():
        bstack1l11l11ll1_opy_ = Config.bstack1l11l111_opy_()
        bstack11111l_opy_ (u"࠭ࠧࠨࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡇࡱࡵࠤࡵࡶࡰࠡ࠿ࠣ࠵࠱ࠦ࡭ࡰࡦࡢࡩࡽ࡫ࡣࡶࡶࡨࠤ࡬࡫ࡴࡴࠢࡸࡷࡪࡪࠠࡧࡱࡵࠤࡦ࠷࠱ࡺࠢࡦࡳࡲࡳࡡ࡯ࡦࡶ࠱ࡼࡸࡡࡱࡲ࡬ࡲ࡬ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡋࡵࡲࠡࡲࡳࡴࠥࡄࠠ࠲࠮ࠣࡱࡴࡪ࡟ࡦࡺࡨࡧࡺࡺࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡣࡧࡦࡥࡺࡹࡥࠡ࡫ࡷࠤ࡮ࡹࠠࡱࡣࡷࡧ࡭࡫ࡤࠡ࡫ࡱࠤࡦࠦࡤࡪࡨࡩࡩࡷ࡫࡮ࡵࠢࡳࡶࡴࡩࡥࡴࡵࠣ࡭ࡩࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡵࡴࠢࡺࡩࠥࡴࡥࡦࡦࠣࡸࡴࠦࡵࡴࡧࠣࡗࡪࡲࡥ࡯࡫ࡸࡱࡕࡧࡴࡤࡪࠫࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡮ࡡ࡯ࡦ࡯ࡩࡷ࠯ࠠࡧࡱࡵࠤࡵࡶࡰࠡࡀࠣ࠵ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠧࠨࠩ↯")
        if bstack1l11l11ll1_opy_.get_property(bstack11111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟࡮ࡱࡧࡣࡨࡧ࡬࡭ࡧࡧࠫ↰")):
            if CONFIG.get(bstack11111l_opy_ (u"ࠨࡲࡤࡶࡦࡲ࡬ࡦ࡮ࡶࡔࡪࡸࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ↱")) is not None and int(CONFIG[bstack11111l_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ↲")]) > 1:
                bstack11111ll1l_opy_(bstack1ll1l111l_opy_)
            return
        bstack11111ll1l_opy_(bstack1ll1l111l_opy_)
    try:
        bstack11l11l11l11_opy_(bstack11111ll1lll_opy_)
    except Exception as e:
        logger.debug(bstack11111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࡳࠡࡲࡤࡸࡨ࡮࠺ࠡࡽࢀࠦ↳").format(e))
bstack11111lllll1_opy_()