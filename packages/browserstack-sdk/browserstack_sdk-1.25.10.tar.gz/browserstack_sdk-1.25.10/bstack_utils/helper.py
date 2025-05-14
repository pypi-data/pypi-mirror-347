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
import collections
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import zipfile
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack11ll1l1l111_opy_, bstack1ll1ll111_opy_, bstack1ll111l1l_opy_, bstack1l11l1l11l_opy_,
                                    bstack11ll1l1111l_opy_, bstack11ll11lll11_opy_, bstack11ll1ll1111_opy_, bstack11ll1l1l11l_opy_)
from bstack_utils.measure import measure
from bstack_utils.messages import bstack1ll1ll1lll_opy_, bstack1lll1llll1_opy_
from bstack_utils.proxy import bstack1lll111l1_opy_, bstack1l11ll11ll_opy_
from bstack_utils.constants import *
from bstack_utils import bstack11ll1ll1l1_opy_
from browserstack_sdk._version import __version__
bstack1l11l11ll1_opy_ = Config.bstack1l11l111_opy_()
logger = bstack11ll1ll1l1_opy_.get_logger(__name__, bstack11ll1ll1l1_opy_.bstack1lllll11l1l_opy_())
def bstack11lllll1111_opy_(config):
    return config[bstack11111l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧᦲ")]
def bstack11lllll1l11_opy_(config):
    return config[bstack11111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩᦳ")]
def bstack1l1l1lll1l_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l1l1ll1l1_opy_(obj):
    values = []
    bstack11l1ll1ll11_opy_ = re.compile(bstack11111l_opy_ (u"ࡲࠣࡠࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࡜ࡥ࠭ࠧࠦᦴ"), re.I)
    for key in obj.keys():
        if bstack11l1ll1ll11_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11ll11l1ll1_opy_(config):
    tags = []
    tags.extend(bstack11l1l1ll1l1_opy_(os.environ))
    tags.extend(bstack11l1l1ll1l1_opy_(config))
    return tags
def bstack11l1ll1llll_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l1ll1lll1_opy_(bstack11l1l11l111_opy_):
    if not bstack11l1l11l111_opy_:
        return bstack11111l_opy_ (u"ࠨࠩᦵ")
    return bstack11111l_opy_ (u"ࠤࡾࢁࠥ࠮ࡻࡾࠫࠥᦶ").format(bstack11l1l11l111_opy_.name, bstack11l1l11l111_opy_.email)
def bstack11llll111ll_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11ll111lll1_opy_ = repo.common_dir
        info = {
            bstack11111l_opy_ (u"ࠥࡷ࡭ࡧࠢᦷ"): repo.head.commit.hexsha,
            bstack11111l_opy_ (u"ࠦࡸ࡮࡯ࡳࡶࡢࡷ࡭ࡧࠢᦸ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack11111l_opy_ (u"ࠧࡨࡲࡢࡰࡦ࡬ࠧᦹ"): repo.active_branch.name,
            bstack11111l_opy_ (u"ࠨࡴࡢࡩࠥᦺ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack11111l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡴࡦࡴࠥᦻ"): bstack11l1ll1lll1_opy_(repo.head.commit.committer),
            bstack11111l_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡵࡧࡵࡣࡩࡧࡴࡦࠤᦼ"): repo.head.commit.committed_datetime.isoformat(),
            bstack11111l_opy_ (u"ࠤࡤࡹࡹ࡮࡯ࡳࠤᦽ"): bstack11l1ll1lll1_opy_(repo.head.commit.author),
            bstack11111l_opy_ (u"ࠥࡥࡺࡺࡨࡰࡴࡢࡨࡦࡺࡥࠣᦾ"): repo.head.commit.authored_datetime.isoformat(),
            bstack11111l_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧᦿ"): repo.head.commit.message,
            bstack11111l_opy_ (u"ࠧࡸ࡯ࡰࡶࠥᧀ"): repo.git.rev_parse(bstack11111l_opy_ (u"ࠨ࠭࠮ࡵ࡫ࡳࡼ࠳ࡴࡰࡲ࡯ࡩࡻ࡫࡬ࠣᧁ")),
            bstack11111l_opy_ (u"ࠢࡤࡱࡰࡱࡴࡴ࡟ࡨ࡫ࡷࡣࡩ࡯ࡲࠣᧂ"): bstack11ll111lll1_opy_,
            bstack11111l_opy_ (u"ࠣࡹࡲࡶࡰࡺࡲࡦࡧࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦᧃ"): subprocess.check_output([bstack11111l_opy_ (u"ࠤࡪ࡭ࡹࠨᧄ"), bstack11111l_opy_ (u"ࠥࡶࡪࡼ࠭ࡱࡣࡵࡷࡪࠨᧅ"), bstack11111l_opy_ (u"ࠦ࠲࠳ࡧࡪࡶ࠰ࡧࡴࡳ࡭ࡰࡰ࠰ࡨ࡮ࡸࠢᧆ")]).strip().decode(
                bstack11111l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᧇ")),
            bstack11111l_opy_ (u"ࠨ࡬ࡢࡵࡷࡣࡹࡧࡧࠣᧈ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack11111l_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺࡳࡠࡵ࡬ࡲࡨ࡫࡟࡭ࡣࡶࡸࡤࡺࡡࡨࠤᧉ"): repo.git.rev_list(
                bstack11111l_opy_ (u"ࠣࡽࢀ࠲࠳ࢁࡽࠣ᧊").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11l1ll11111_opy_ = []
        for remote in remotes:
            bstack11l1l1lllll_opy_ = {
                bstack11111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᧋"): remote.name,
                bstack11111l_opy_ (u"ࠥࡹࡷࡲࠢ᧌"): remote.url,
            }
            bstack11l1ll11111_opy_.append(bstack11l1l1lllll_opy_)
        bstack11l1ll111ll_opy_ = {
            bstack11111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᧍"): bstack11111l_opy_ (u"ࠧ࡭ࡩࡵࠤ᧎"),
            **info,
            bstack11111l_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪࡹࠢ᧏"): bstack11l1ll11111_opy_
        }
        bstack11l1ll111ll_opy_ = bstack11l1l1l1ll1_opy_(bstack11l1ll111ll_opy_)
        return bstack11l1ll111ll_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack11111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡰࡲࡸࡰࡦࡺࡩ࡯ࡩࠣࡋ࡮ࡺࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡿࠥ᧐").format(err))
        return {}
def bstack11l1l1l1ll1_opy_(bstack11l1ll111ll_opy_):
    bstack11l1lll1ll1_opy_ = bstack11l1lllll11_opy_(bstack11l1ll111ll_opy_)
    if bstack11l1lll1ll1_opy_ and bstack11l1lll1ll1_opy_ > bstack11ll1l1111l_opy_:
        bstack11ll1111111_opy_ = bstack11l1lll1ll1_opy_ - bstack11ll1l1111l_opy_
        bstack11ll1111lll_opy_ = bstack11l1l11ll11_opy_(bstack11l1ll111ll_opy_[bstack11111l_opy_ (u"ࠣࡥࡲࡱࡲ࡯ࡴࡠ࡯ࡨࡷࡸࡧࡧࡦࠤ᧑")], bstack11ll1111111_opy_)
        bstack11l1ll111ll_opy_[bstack11111l_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡡࡰࡩࡸࡹࡡࡨࡧࠥ᧒")] = bstack11ll1111lll_opy_
        logger.info(bstack11111l_opy_ (u"ࠥࡘ࡭࡫ࠠࡤࡱࡰࡱ࡮ࡺࠠࡩࡣࡶࠤࡧ࡫ࡥ࡯ࠢࡷࡶࡺࡴࡣࡢࡶࡨࡨ࠳ࠦࡓࡪࡼࡨࠤࡴ࡬ࠠࡤࡱࡰࡱ࡮ࡺࠠࡢࡨࡷࡩࡷࠦࡴࡳࡷࡱࡧࡦࡺࡩࡰࡰࠣ࡭ࡸࠦࡻࡾࠢࡎࡆࠧ᧓")
                    .format(bstack11l1lllll11_opy_(bstack11l1ll111ll_opy_) / 1024))
    return bstack11l1ll111ll_opy_
def bstack11l1lllll11_opy_(bstack11l11lll_opy_):
    try:
        if bstack11l11lll_opy_:
            bstack11ll111ll11_opy_ = json.dumps(bstack11l11lll_opy_)
            bstack11l1l1l1l11_opy_ = sys.getsizeof(bstack11ll111ll11_opy_)
            return bstack11l1l1l1l11_opy_
    except Exception as e:
        logger.debug(bstack11111l_opy_ (u"ࠦࡘࡵ࡭ࡦࡶ࡫࡭ࡳ࡭ࠠࡸࡧࡱࡸࠥࡽࡲࡰࡰࡪࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡦࡲࡣࡶ࡮ࡤࡸ࡮ࡴࡧࠡࡵ࡬ࡾࡪࠦ࡯ࡧࠢࡍࡗࡔࡔࠠࡰࡤ࡭ࡩࡨࡺ࠺ࠡࡽࢀࠦ᧔").format(e))
    return -1
def bstack11l1l11ll11_opy_(field, bstack11l1l1lll11_opy_):
    try:
        bstack11ll11l11l1_opy_ = len(bytes(bstack11ll11lll11_opy_, bstack11111l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫ᧕")))
        bstack11l1l11ll1l_opy_ = bytes(field, bstack11111l_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬ᧖"))
        bstack11l1l11l1ll_opy_ = len(bstack11l1l11ll1l_opy_)
        bstack11l1ll11lll_opy_ = ceil(bstack11l1l11l1ll_opy_ - bstack11l1l1lll11_opy_ - bstack11ll11l11l1_opy_)
        if bstack11l1ll11lll_opy_ > 0:
            bstack11l1llllll1_opy_ = bstack11l1l11ll1l_opy_[:bstack11l1ll11lll_opy_].decode(bstack11111l_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭᧗"), errors=bstack11111l_opy_ (u"ࠨ࡫ࡪࡲࡴࡸࡥࠨ᧘")) + bstack11ll11lll11_opy_
            return bstack11l1llllll1_opy_
    except Exception as e:
        logger.debug(bstack11111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡵࡴࡸࡲࡨࡧࡴࡪࡰࡪࠤ࡫࡯ࡥ࡭ࡦ࠯ࠤࡳࡵࡴࡩ࡫ࡱ࡫ࠥࡽࡡࡴࠢࡷࡶࡺࡴࡣࡢࡶࡨࡨࠥ࡮ࡥࡳࡧ࠽ࠤࢀࢃࠢ᧙").format(e))
    return field
def bstack1lll11l1l1_opy_():
    env = os.environ
    if (bstack11111l_opy_ (u"ࠥࡎࡊࡔࡋࡊࡐࡖࡣ࡚ࡘࡌࠣ᧚") in env and len(env[bstack11111l_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤ᧛")]) > 0) or (
            bstack11111l_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡈࡐࡏࡈࠦ᧜") in env and len(env[bstack11111l_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧ᧝")]) > 0):
        return {
            bstack11111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᧞"): bstack11111l_opy_ (u"ࠣࡌࡨࡲࡰ࡯࡮ࡴࠤ᧟"),
            bstack11111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᧠"): env.get(bstack11111l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ᧡")),
            bstack11111l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᧢"): env.get(bstack11111l_opy_ (u"ࠧࡐࡏࡃࡡࡑࡅࡒࡋࠢ᧣")),
            bstack11111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᧤"): env.get(bstack11111l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨ᧥"))
        }
    if env.get(bstack11111l_opy_ (u"ࠣࡅࡌࠦ᧦")) == bstack11111l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᧧") and bstack11ll11l11_opy_(env.get(bstack11111l_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡆࡍࠧ᧨"))):
        return {
            bstack11111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᧩"): bstack11111l_opy_ (u"ࠧࡉࡩࡳࡥ࡯ࡩࡈࡏࠢ᧪"),
            bstack11111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᧫"): env.get(bstack11111l_opy_ (u"ࠢࡄࡋࡕࡇࡑࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥ᧬")),
            bstack11111l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᧭"): env.get(bstack11111l_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡍࡓࡇࠨ᧮")),
            bstack11111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤ᧯"): env.get(bstack11111l_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࠢ᧰"))
        }
    if env.get(bstack11111l_opy_ (u"ࠧࡉࡉࠣ᧱")) == bstack11111l_opy_ (u"ࠨࡴࡳࡷࡨࠦ᧲") and bstack11ll11l11_opy_(env.get(bstack11111l_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙ࠢ᧳"))):
        return {
            bstack11111l_opy_ (u"ࠣࡰࡤࡱࡪࠨ᧴"): bstack11111l_opy_ (u"ࠤࡗࡶࡦࡼࡩࡴࠢࡆࡍࠧ᧵"),
            bstack11111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᧶"): env.get(bstack11111l_opy_ (u"࡙ࠦࡘࡁࡗࡋࡖࡣࡇ࡛ࡉࡍࡆࡢ࡛ࡊࡈ࡟ࡖࡔࡏࠦ᧷")),
            bstack11111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᧸"): env.get(bstack11111l_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣ᧹")),
            bstack11111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᧺"): env.get(bstack11111l_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ᧻"))
        }
    if env.get(bstack11111l_opy_ (u"ࠤࡆࡍࠧ᧼")) == bstack11111l_opy_ (u"ࠥࡸࡷࡻࡥࠣ᧽") and env.get(bstack11111l_opy_ (u"ࠦࡈࡏ࡟ࡏࡃࡐࡉࠧ᧾")) == bstack11111l_opy_ (u"ࠧࡩ࡯ࡥࡧࡶ࡬࡮ࡶࠢ᧿"):
        return {
            bstack11111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᨀ"): bstack11111l_opy_ (u"ࠢࡄࡱࡧࡩࡸ࡮ࡩࡱࠤᨁ"),
            bstack11111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᨂ"): None,
            bstack11111l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᨃ"): None,
            bstack11111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᨄ"): None
        }
    if env.get(bstack11111l_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡃࡔࡄࡒࡈࡎࠢᨅ")) and env.get(bstack11111l_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡅࡒࡑࡒࡏࡔࠣᨆ")):
        return {
            bstack11111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᨇ"): bstack11111l_opy_ (u"ࠢࡃ࡫ࡷࡦࡺࡩ࡫ࡦࡶࠥᨈ"),
            bstack11111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᨉ"): env.get(bstack11111l_opy_ (u"ࠤࡅࡍ࡙ࡈࡕࡄࡍࡈࡘࡤࡍࡉࡕࡡࡋࡘ࡙ࡖ࡟ࡐࡔࡌࡋࡎࡔࠢᨊ")),
            bstack11111l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᨋ"): None,
            bstack11111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᨌ"): env.get(bstack11111l_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᨍ"))
        }
    if env.get(bstack11111l_opy_ (u"ࠨࡃࡊࠤᨎ")) == bstack11111l_opy_ (u"ࠢࡵࡴࡸࡩࠧᨏ") and bstack11ll11l11_opy_(env.get(bstack11111l_opy_ (u"ࠣࡆࡕࡓࡓࡋࠢᨐ"))):
        return {
            bstack11111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᨑ"): bstack11111l_opy_ (u"ࠥࡈࡷࡵ࡮ࡦࠤᨒ"),
            bstack11111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᨓ"): env.get(bstack11111l_opy_ (u"ࠧࡊࡒࡐࡐࡈࡣࡇ࡛ࡉࡍࡆࡢࡐࡎࡔࡋࠣᨔ")),
            bstack11111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᨕ"): None,
            bstack11111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᨖ"): env.get(bstack11111l_opy_ (u"ࠣࡆࡕࡓࡓࡋ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨᨗ"))
        }
    if env.get(bstack11111l_opy_ (u"ࠤࡆࡍᨘࠧ")) == bstack11111l_opy_ (u"ࠥࡸࡷࡻࡥࠣᨙ") and bstack11ll11l11_opy_(env.get(bstack11111l_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋࠢᨚ"))):
        return {
            bstack11111l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᨛ"): bstack11111l_opy_ (u"ࠨࡓࡦ࡯ࡤࡴ࡭ࡵࡲࡦࠤ᨜"),
            bstack11111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ᨝"): env.get(bstack11111l_opy_ (u"ࠣࡕࡈࡑࡆࡖࡈࡐࡔࡈࡣࡔࡘࡇࡂࡐࡌ࡞ࡆ࡚ࡉࡐࡐࡢ࡙ࡗࡒࠢ᨞")),
            bstack11111l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᨟"): env.get(bstack11111l_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᨠ")),
            bstack11111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᨡ"): env.get(bstack11111l_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡏࡄࠣᨢ"))
        }
    if env.get(bstack11111l_opy_ (u"ࠨࡃࡊࠤᨣ")) == bstack11111l_opy_ (u"ࠢࡵࡴࡸࡩࠧᨤ") and bstack11ll11l11_opy_(env.get(bstack11111l_opy_ (u"ࠣࡉࡌࡘࡑࡇࡂࡠࡅࡌࠦᨥ"))):
        return {
            bstack11111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᨦ"): bstack11111l_opy_ (u"ࠥࡋ࡮ࡺࡌࡢࡤࠥᨧ"),
            bstack11111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᨨ"): env.get(bstack11111l_opy_ (u"ࠧࡉࡉࡠࡌࡒࡆࡤ࡛ࡒࡍࠤᨩ")),
            bstack11111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᨪ"): env.get(bstack11111l_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᨫ")),
            bstack11111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᨬ"): env.get(bstack11111l_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡌࡈࠧᨭ"))
        }
    if env.get(bstack11111l_opy_ (u"ࠥࡇࡎࠨᨮ")) == bstack11111l_opy_ (u"ࠦࡹࡸࡵࡦࠤᨯ") and bstack11ll11l11_opy_(env.get(bstack11111l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࠣᨰ"))):
        return {
            bstack11111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᨱ"): bstack11111l_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡱࡩࡵࡧࠥᨲ"),
            bstack11111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᨳ"): env.get(bstack11111l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᨴ")),
            bstack11111l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᨵ"): env.get(bstack11111l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡍࡃࡅࡉࡑࠨᨶ")) or env.get(bstack11111l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡒࡌࡔࡊࡒࡉࡏࡇࡢࡒࡆࡓࡅࠣᨷ")),
            bstack11111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᨸ"): env.get(bstack11111l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᨹ"))
        }
    if bstack11ll11l11_opy_(env.get(bstack11111l_opy_ (u"ࠣࡖࡉࡣࡇ࡛ࡉࡍࡆࠥᨺ"))):
        return {
            bstack11111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᨻ"): bstack11111l_opy_ (u"࡚ࠥ࡮ࡹࡵࡢ࡮ࠣࡗࡹࡻࡤࡪࡱࠣࡘࡪࡧ࡭ࠡࡕࡨࡶࡻ࡯ࡣࡦࡵࠥᨼ"),
            bstack11111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᨽ"): bstack11111l_opy_ (u"ࠧࢁࡽࡼࡿࠥᨾ").format(env.get(bstack11111l_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡊࡔ࡛ࡎࡅࡃࡗࡍࡔࡔࡓࡆࡔ࡙ࡉࡗ࡛ࡒࡊࠩᨿ")), env.get(bstack11111l_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡕࡘࡏࡋࡇࡆࡘࡎࡊࠧᩀ"))),
            bstack11111l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᩁ"): env.get(bstack11111l_opy_ (u"ࠤࡖ࡝ࡘ࡚ࡅࡎࡡࡇࡉࡋࡏࡎࡊࡖࡌࡓࡓࡏࡄࠣᩂ")),
            bstack11111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᩃ"): env.get(bstack11111l_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦᩄ"))
        }
    if bstack11ll11l11_opy_(env.get(bstack11111l_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘࠢᩅ"))):
        return {
            bstack11111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᩆ"): bstack11111l_opy_ (u"ࠢࡂࡲࡳࡺࡪࡿ࡯ࡳࠤᩇ"),
            bstack11111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᩈ"): bstack11111l_opy_ (u"ࠤࡾࢁ࠴ࡶࡲࡰ࡬ࡨࡧࡹ࠵ࡻࡾ࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽࠣᩉ").format(env.get(bstack11111l_opy_ (u"ࠪࡅࡕࡖࡖࡆ࡛ࡒࡖࡤ࡛ࡒࡍࠩᩊ")), env.get(bstack11111l_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡁࡄࡅࡒ࡙ࡓ࡚࡟ࡏࡃࡐࡉࠬᩋ")), env.get(bstack11111l_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡑࡔࡒࡎࡊࡉࡔࡠࡕࡏ࡙ࡌ࠭ᩌ")), env.get(bstack11111l_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪᩍ"))),
            bstack11111l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᩎ"): env.get(bstack11111l_opy_ (u"ࠣࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧᩏ")),
            bstack11111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᩐ"): env.get(bstack11111l_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᩑ"))
        }
    if env.get(bstack11111l_opy_ (u"ࠦࡆࡠࡕࡓࡇࡢࡌ࡙࡚ࡐࡠࡗࡖࡉࡗࡥࡁࡈࡇࡑࡘࠧᩒ")) and env.get(bstack11111l_opy_ (u"࡚ࠧࡆࡠࡄࡘࡍࡑࡊࠢᩓ")):
        return {
            bstack11111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᩔ"): bstack11111l_opy_ (u"ࠢࡂࡼࡸࡶࡪࠦࡃࡊࠤᩕ"),
            bstack11111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᩖ"): bstack11111l_opy_ (u"ࠤࡾࢁࢀࢃ࠯ࡠࡤࡸ࡭ࡱࡪ࠯ࡳࡧࡶࡹࡱࡺࡳࡀࡤࡸ࡭ࡱࡪࡉࡥ࠿ࡾࢁࠧᩗ").format(env.get(bstack11111l_opy_ (u"ࠪࡗ࡞࡙ࡔࡆࡏࡢࡘࡊࡇࡍࡇࡑࡘࡒࡉࡇࡔࡊࡑࡑࡗࡊࡘࡖࡆࡔࡘࡖࡎ࠭ᩘ")), env.get(bstack11111l_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡒࡕࡓࡏࡋࡃࡕࠩᩙ")), env.get(bstack11111l_opy_ (u"ࠬࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠬᩚ"))),
            bstack11111l_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᩛ"): env.get(bstack11111l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠢᩜ")),
            bstack11111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᩝ"): env.get(bstack11111l_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤᩞ"))
        }
    if any([env.get(bstack11111l_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣ᩟")), env.get(bstack11111l_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐ᩠ࠥ")), env.get(bstack11111l_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡕࡒ࡙ࡗࡉࡅࡠࡘࡈࡖࡘࡏࡏࡏࠤᩡ"))]):
        return {
            bstack11111l_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᩢ"): bstack11111l_opy_ (u"ࠢࡂ࡙ࡖࠤࡈࡵࡤࡦࡄࡸ࡭ࡱࡪࠢᩣ"),
            bstack11111l_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᩤ"): env.get(bstack11111l_opy_ (u"ࠤࡆࡓࡉࡋࡂࡖࡋࡏࡈࡤࡖࡕࡃࡎࡌࡇࡤࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣᩥ")),
            bstack11111l_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᩦ"): env.get(bstack11111l_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᩧ")),
            bstack11111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᩨ"): env.get(bstack11111l_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᩩ"))
        }
    if env.get(bstack11111l_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡣࡷ࡬ࡰࡩࡔࡵ࡮ࡤࡨࡶࠧᩪ")):
        return {
            bstack11111l_opy_ (u"ࠣࡰࡤࡱࡪࠨᩫ"): bstack11111l_opy_ (u"ࠤࡅࡥࡲࡨ࡯ࡰࠤᩬ"),
            bstack11111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᩭ"): env.get(bstack11111l_opy_ (u"ࠦࡧࡧ࡭ࡣࡱࡲࡣࡧࡻࡩ࡭ࡦࡕࡩࡸࡻ࡬ࡵࡵࡘࡶࡱࠨᩮ")),
            bstack11111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᩯ"): env.get(bstack11111l_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡳࡩࡱࡵࡸࡏࡵࡢࡏࡣࡰࡩࠧᩰ")),
            bstack11111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᩱ"): env.get(bstack11111l_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨᩲ"))
        }
    if env.get(bstack11111l_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࠥᩳ")) or env.get(bstack11111l_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧᩴ")):
        return {
            bstack11111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᩵"): bstack11111l_opy_ (u"ࠧ࡝ࡥࡳࡥ࡮ࡩࡷࠨ᩶"),
            bstack11111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᩷"): env.get(bstack11111l_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦ᩸")),
            bstack11111l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᩹"): bstack11111l_opy_ (u"ࠤࡐࡥ࡮ࡴࠠࡑ࡫ࡳࡩࡱ࡯࡮ࡦࠤ᩺") if env.get(bstack11111l_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࡣࡒࡇࡉࡏࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡘ࡚ࡁࡓࡖࡈࡈࠧ᩻")) else None,
            bstack11111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᩼"): env.get(bstack11111l_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡇࡊࡖࡢࡇࡔࡓࡍࡊࡖࠥ᩽"))
        }
    if any([env.get(bstack11111l_opy_ (u"ࠨࡇࡄࡒࡢࡔࡗࡕࡊࡆࡅࡗࠦ᩾")), env.get(bstack11111l_opy_ (u"ࠢࡈࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔ᩿ࠣ")), env.get(bstack11111l_opy_ (u"ࠣࡉࡒࡓࡌࡒࡅࡠࡅࡏࡓ࡚ࡊ࡟ࡑࡔࡒࡎࡊࡉࡔࠣ᪀"))]):
        return {
            bstack11111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᪁"): bstack11111l_opy_ (u"ࠥࡋࡴࡵࡧ࡭ࡧࠣࡇࡱࡵࡵࡥࠤ᪂"),
            bstack11111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᪃"): None,
            bstack11111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢ᪄"): env.get(bstack11111l_opy_ (u"ࠨࡐࡓࡑࡍࡉࡈ࡚࡟ࡊࡆࠥ᪅")),
            bstack11111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ᪆"): env.get(bstack11111l_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥ᪇"))
        }
    if env.get(bstack11111l_opy_ (u"ࠤࡖࡌࡎࡖࡐࡂࡄࡏࡉࠧ᪈")):
        return {
            bstack11111l_opy_ (u"ࠥࡲࡦࡳࡥࠣ᪉"): bstack11111l_opy_ (u"ࠦࡘ࡮ࡩࡱࡲࡤࡦࡱ࡫ࠢ᪊"),
            bstack11111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᪋"): env.get(bstack11111l_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ᪌")),
            bstack11111l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᪍"): bstack11111l_opy_ (u"ࠣࡌࡲࡦࠥࠩࡻࡾࠤ᪎").format(env.get(bstack11111l_opy_ (u"ࠩࡖࡌࡎࡖࡐࡂࡄࡏࡉࡤࡐࡏࡃࡡࡌࡈࠬ᪏"))) if env.get(bstack11111l_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉࠨ᪐")) else None,
            bstack11111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᪑"): env.get(bstack11111l_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢ᪒"))
        }
    if bstack11ll11l11_opy_(env.get(bstack11111l_opy_ (u"ࠨࡎࡆࡖࡏࡍࡋ࡟ࠢ᪓"))):
        return {
            bstack11111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᪔"): bstack11111l_opy_ (u"ࠣࡐࡨࡸࡱ࡯ࡦࡺࠤ᪕"),
            bstack11111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ᪖"): env.get(bstack11111l_opy_ (u"ࠥࡈࡊࡖࡌࡐ࡛ࡢ࡙ࡗࡒࠢ᪗")),
            bstack11111l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᪘"): env.get(bstack11111l_opy_ (u"࡙ࠧࡉࡕࡇࡢࡒࡆࡓࡅࠣ᪙")),
            bstack11111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᪚"): env.get(bstack11111l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤ᪛"))
        }
    if bstack11ll11l11_opy_(env.get(bstack11111l_opy_ (u"ࠣࡉࡌࡘࡍ࡛ࡂࡠࡃࡆࡘࡎࡕࡎࡔࠤ᪜"))):
        return {
            bstack11111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᪝"): bstack11111l_opy_ (u"ࠥࡋ࡮ࡺࡈࡶࡤࠣࡅࡨࡺࡩࡰࡰࡶࠦ᪞"),
            bstack11111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᪟"): bstack11111l_opy_ (u"ࠧࢁࡽ࠰ࡽࢀ࠳ࡦࡩࡴࡪࡱࡱࡷ࠴ࡸࡵ࡯ࡵ࠲ࡿࢂࠨ᪠").format(env.get(bstack11111l_opy_ (u"࠭ࡇࡊࡖࡋ࡙ࡇࡥࡓࡆࡔ࡙ࡉࡗࡥࡕࡓࡎࠪ᪡")), env.get(bstack11111l_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡇࡓࡓࡘࡏࡔࡐࡔ࡜ࠫ᪢")), env.get(bstack11111l_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡘࡒࡤࡏࡄࠨ᪣"))),
            bstack11111l_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦ᪤"): env.get(bstack11111l_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢ࡛ࡔࡘࡋࡇࡎࡒ࡛ࠧ᪥")),
            bstack11111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᪦"): env.get(bstack11111l_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤࡘࡕࡏࡡࡌࡈࠧᪧ"))
        }
    if env.get(bstack11111l_opy_ (u"ࠨࡃࡊࠤ᪨")) == bstack11111l_opy_ (u"ࠢࡵࡴࡸࡩࠧ᪩") and env.get(bstack11111l_opy_ (u"ࠣࡘࡈࡖࡈࡋࡌࠣ᪪")) == bstack11111l_opy_ (u"ࠤ࠴ࠦ᪫"):
        return {
            bstack11111l_opy_ (u"ࠥࡲࡦࡳࡥࠣ᪬"): bstack11111l_opy_ (u"࡛ࠦ࡫ࡲࡤࡧ࡯ࠦ᪭"),
            bstack11111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᪮"): bstack11111l_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࡻࡾࠤ᪯").format(env.get(bstack11111l_opy_ (u"ࠧࡗࡇࡕࡇࡊࡒ࡟ࡖࡔࡏࠫ᪰"))),
            bstack11111l_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥ᪱"): None,
            bstack11111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᪲"): None,
        }
    if env.get(bstack11111l_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤ࡜ࡅࡓࡕࡌࡓࡓࠨ᪳")):
        return {
            bstack11111l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᪴"): bstack11111l_opy_ (u"࡚ࠧࡥࡢ࡯ࡦ࡭ࡹࡿ᪵ࠢ"),
            bstack11111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᪶"): None,
            bstack11111l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᪷"): env.get(bstack11111l_opy_ (u"ࠣࡖࡈࡅࡒࡉࡉࡕ࡛ࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠤ᪸")),
            bstack11111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲ᪹ࠣ"): env.get(bstack11111l_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤ᪺"))
        }
    if any([env.get(bstack11111l_opy_ (u"ࠦࡈࡕࡎࡄࡑࡘࡖࡘࡋࠢ᪻")), env.get(bstack11111l_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࡠࡗࡕࡐࠧ᪼")), env.get(bstack11111l_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡗࡊࡘࡎࡂࡏࡈ᪽ࠦ")), env.get(bstack11111l_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢࡘࡊࡇࡍࠣ᪾"))]):
        return {
            bstack11111l_opy_ (u"ࠣࡰࡤࡱࡪࠨᪿ"): bstack11111l_opy_ (u"ࠤࡆࡳࡳࡩ࡯ࡶࡴࡶࡩᫀࠧ"),
            bstack11111l_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨ᫁"): None,
            bstack11111l_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᫂"): env.get(bstack11111l_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ᫃")) or None,
            bstack11111l_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶ᫄ࠧ"): env.get(bstack11111l_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡉࡅࠤ᫅"), 0)
        }
    if env.get(bstack11111l_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨ᫆")):
        return {
            bstack11111l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ᫇"): bstack11111l_opy_ (u"ࠥࡋࡴࡉࡄࠣ᫈"),
            bstack11111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢ᫉"): None,
            bstack11111l_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫᫊ࠢ"): env.get(bstack11111l_opy_ (u"ࠨࡇࡐࡡࡍࡓࡇࡥࡎࡂࡏࡈࠦ᫋")),
            bstack11111l_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᫌ"): env.get(bstack11111l_opy_ (u"ࠣࡉࡒࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡃࡐࡗࡑࡘࡊࡘࠢᫍ"))
        }
    if env.get(bstack11111l_opy_ (u"ࠤࡆࡊࡤࡈࡕࡊࡎࡇࡣࡎࡊࠢᫎ")):
        return {
            bstack11111l_opy_ (u"ࠥࡲࡦࡳࡥࠣ᫏"): bstack11111l_opy_ (u"ࠦࡈࡵࡤࡦࡈࡵࡩࡸ࡮ࠢ᫐"),
            bstack11111l_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ᫑"): env.get(bstack11111l_opy_ (u"ࠨࡃࡇࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧ᫒")),
            bstack11111l_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ᫓"): env.get(bstack11111l_opy_ (u"ࠣࡅࡉࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡎࡂࡏࡈࠦ᫔")),
            bstack11111l_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ᫕"): env.get(bstack11111l_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣ᫖"))
        }
    return {bstack11111l_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥ᫗"): None}
def get_host_info():
    return {
        bstack11111l_opy_ (u"ࠧ࡮࡯ࡴࡶࡱࡥࡲ࡫ࠢ᫘"): platform.node(),
        bstack11111l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠣ᫙"): platform.system(),
        bstack11111l_opy_ (u"ࠢࡵࡻࡳࡩࠧ᫚"): platform.machine(),
        bstack11111l_opy_ (u"ࠣࡸࡨࡶࡸ࡯࡯࡯ࠤ᫛"): platform.version(),
        bstack11111l_opy_ (u"ࠤࡤࡶࡨ࡮ࠢ᫜"): platform.architecture()[0]
    }
def bstack11l11l111_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l1ll1ll1l_opy_():
    if bstack1l11l11ll1_opy_.get_property(bstack11111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࠫ᫝")):
        return bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪ᫞")
    return bstack11111l_opy_ (u"ࠬࡻ࡮࡬ࡰࡲࡻࡳࡥࡧࡳ࡫ࡧࠫ᫟")
def bstack11l1l1l11l1_opy_(driver):
    info = {
        bstack11111l_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ᫠"): driver.capabilities,
        bstack11111l_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧࠫ᫡"): driver.session_id,
        bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩ᫢"): driver.capabilities.get(bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ᫣"), None),
        bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᫤"): driver.capabilities.get(bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᫥"), None),
        bstack11111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࠧ᫦"): driver.capabilities.get(bstack11111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬ᫧"), None),
        bstack11111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪ᫨"):driver.capabilities.get(bstack11111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪ᫩"), None),
    }
    if bstack11l1ll1ll1l_opy_() == bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ᫪"):
        if bstack11l11l11ll_opy_():
            info[bstack11111l_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫ᫫")] = bstack11111l_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪ᫬")
        elif driver.capabilities.get(bstack11111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᫭"), {}).get(bstack11111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ᫮"), False):
            info[bstack11111l_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࠨ᫯")] = bstack11111l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ᫰")
        else:
            info[bstack11111l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪ᫱")] = bstack11111l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ᫲")
    return info
def bstack11l11l11ll_opy_():
    if bstack1l11l11ll1_opy_.get_property(bstack11111l_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪ᫳")):
        return True
    if bstack11ll11l11_opy_(os.environ.get(bstack11111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭᫴"), None)):
        return True
    return False
def bstack11111ll1_opy_(bstack11ll111l1l1_opy_, url, data, config):
    headers = config.get(bstack11111l_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ᫵"), None)
    proxies = bstack1lll111l1_opy_(config, url)
    auth = config.get(bstack11111l_opy_ (u"ࠧࡢࡷࡷ࡬ࠬ᫶"), None)
    response = requests.request(
            bstack11ll111l1l1_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1ll1l1l11_opy_(bstack11lllll1ll_opy_, size):
    bstack1ll111111l_opy_ = []
    while len(bstack11lllll1ll_opy_) > size:
        bstack1ll1l1l1l_opy_ = bstack11lllll1ll_opy_[:size]
        bstack1ll111111l_opy_.append(bstack1ll1l1l1l_opy_)
        bstack11lllll1ll_opy_ = bstack11lllll1ll_opy_[size:]
    bstack1ll111111l_opy_.append(bstack11lllll1ll_opy_)
    return bstack1ll111111l_opy_
def bstack11l1l1111ll_opy_(message, bstack11ll111l111_opy_=False):
    os.write(1, bytes(message, bstack11111l_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧ᫷")))
    os.write(1, bytes(bstack11111l_opy_ (u"ࠩ࡟ࡲࠬ᫸"), bstack11111l_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩ᫹")))
    if bstack11ll111l111_opy_:
        with open(bstack11111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠱ࡴ࠷࠱ࡺ࠯ࠪ᫺") + os.environ[bstack11111l_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫ᫻")] + bstack11111l_opy_ (u"࠭࠮࡭ࡱࡪࠫ᫼"), bstack11111l_opy_ (u"ࠧࡢࠩ᫽")) as f:
            f.write(message + bstack11111l_opy_ (u"ࠨ࡞ࡱࠫ᫾"))
def bstack1ll111l1lll_opy_():
    return os.environ[bstack11111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ᫿")].lower() == bstack11111l_opy_ (u"ࠪࡸࡷࡻࡥࠨᬀ")
def bstack11ll11l1l1_opy_(bstack11l1ll11ll1_opy_):
    return bstack11111l_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪᬁ").format(bstack11ll1l1l111_opy_, bstack11l1ll11ll1_opy_)
def bstack1l11l1lll_opy_():
    return bstack111l11llll_opy_().replace(tzinfo=None).isoformat() + bstack11111l_opy_ (u"ࠬࡠࠧᬂ")
def bstack11l1lllllll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack11111l_opy_ (u"࡚࠭ࠨᬃ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack11111l_opy_ (u"࡛ࠧࠩᬄ")))).total_seconds() * 1000
def bstack11l1l1lll1l_opy_(timestamp):
    return bstack11l1lll1lll_opy_(timestamp).isoformat() + bstack11111l_opy_ (u"ࠨ࡜ࠪᬅ")
def bstack11ll111llll_opy_(bstack11ll11l1l1l_opy_):
    date_format = bstack11111l_opy_ (u"ࠩࠨ࡝ࠪࡳࠥࡥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠧᬆ")
    bstack11l1l1ll11l_opy_ = datetime.datetime.strptime(bstack11ll11l1l1l_opy_, date_format)
    return bstack11l1l1ll11l_opy_.isoformat() + bstack11111l_opy_ (u"ࠪ࡞ࠬᬇ")
def bstack11l11lll1ll_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack11111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᬈ")
    else:
        return bstack11111l_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᬉ")
def bstack11ll11l11_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack11111l_opy_ (u"࠭ࡴࡳࡷࡨࠫᬊ")
def bstack11l11llllll_opy_(val):
    return val.__str__().lower() == bstack11111l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᬋ")
def bstack111l1lllll_opy_(bstack11l11llll11_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l11llll11_opy_ as e:
                print(bstack11111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࡾࢁࠥ࠳࠾ࠡࡽࢀ࠾ࠥࢁࡽࠣᬌ").format(func.__name__, bstack11l11llll11_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l1l1l1l1l_opy_(bstack11ll11l111l_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11ll11l111l_opy_(cls, *args, **kwargs)
            except bstack11l11llll11_opy_ as e:
                print(bstack11111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤᬍ").format(bstack11ll11l111l_opy_.__name__, bstack11l11llll11_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l1l1l1l1l_opy_
    else:
        return decorator
def bstack11l1l1l11l_opy_(bstack1111ll1l11_opy_):
    if os.getenv(bstack11111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ᬎ")) is not None:
        return bstack11ll11l11_opy_(os.getenv(bstack11111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧᬏ")))
    if bstack11111l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᬐ") in bstack1111ll1l11_opy_ and bstack11l11llllll_opy_(bstack1111ll1l11_opy_[bstack11111l_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᬑ")]):
        return False
    if bstack11111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᬒ") in bstack1111ll1l11_opy_ and bstack11l11llllll_opy_(bstack1111ll1l11_opy_[bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᬓ")]):
        return False
    return True
def bstack11lll111ll_opy_():
    try:
        from pytest_bdd import reporting
        bstack11l11llll1l_opy_ = os.environ.get(bstack11111l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡗࡖࡉࡗࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠤᬔ"), None)
        return bstack11l11llll1l_opy_ is None or bstack11l11llll1l_opy_ == bstack11111l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠢᬕ")
    except Exception as e:
        return False
def bstack1lll1lll11_opy_(hub_url, CONFIG):
    if bstack1lllll11l1_opy_() <= version.parse(bstack11111l_opy_ (u"ࠫ࠸࠴࠱࠴࠰࠳ࠫᬖ")):
        if hub_url:
            return bstack11111l_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨᬗ") + hub_url + bstack11111l_opy_ (u"ࠨ࠺࠹࠲࠲ࡻࡩ࠵ࡨࡶࡤࠥᬘ")
        return bstack1ll111l1l_opy_
    if hub_url:
        return bstack11111l_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᬙ") + hub_url + bstack11111l_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤᬚ")
    return bstack1l11l1l11l_opy_
def bstack11ll11111ll_opy_():
    return isinstance(os.getenv(bstack11111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨᬛ")), str)
def bstack11111lll_opy_(url):
    return urlparse(url).hostname
def bstack11ll1ll1_opy_(hostname):
    for bstack1ll11l1lll_opy_ in bstack1ll1ll111_opy_:
        regex = re.compile(bstack1ll11l1lll_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l11ll1l1l_opy_(bstack11l1l11l11l_opy_, file_name, logger):
    bstack11lll1ll1l_opy_ = os.path.join(os.path.expanduser(bstack11111l_opy_ (u"ࠪࢂࠬᬜ")), bstack11l1l11l11l_opy_)
    try:
        if not os.path.exists(bstack11lll1ll1l_opy_):
            os.makedirs(bstack11lll1ll1l_opy_)
        file_path = os.path.join(os.path.expanduser(bstack11111l_opy_ (u"ࠫࢃ࠭ᬝ")), bstack11l1l11l11l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack11111l_opy_ (u"ࠬࡽࠧᬞ")):
                pass
            with open(file_path, bstack11111l_opy_ (u"ࠨࡷࠬࠤᬟ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1ll1ll1lll_opy_.format(str(e)))
def bstack11l1l11111l_opy_(file_name, key, value, logger):
    file_path = bstack11l11ll1l1l_opy_(bstack11111l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᬠ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1ll1111l11_opy_ = json.load(open(file_path, bstack11111l_opy_ (u"ࠨࡴࡥࠫᬡ")))
        else:
            bstack1ll1111l11_opy_ = {}
        bstack1ll1111l11_opy_[key] = value
        with open(file_path, bstack11111l_opy_ (u"ࠤࡺ࠯ࠧᬢ")) as outfile:
            json.dump(bstack1ll1111l11_opy_, outfile)
def bstack1l1111l11l_opy_(file_name, logger):
    file_path = bstack11l11ll1l1l_opy_(bstack11111l_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᬣ"), file_name, logger)
    bstack1ll1111l11_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack11111l_opy_ (u"ࠫࡷ࠭ᬤ")) as bstack1llll1111l_opy_:
            bstack1ll1111l11_opy_ = json.load(bstack1llll1111l_opy_)
    return bstack1ll1111l11_opy_
def bstack111111ll_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack11111l_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡩ࡭ࡱ࡫࠺ࠡࠩᬥ") + file_path + bstack11111l_opy_ (u"࠭ࠠࠨᬦ") + str(e))
def bstack1lllll11l1_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack11111l_opy_ (u"ࠢ࠽ࡐࡒࡘࡘࡋࡔ࠿ࠤᬧ")
def bstack11llll11l_opy_(config):
    if bstack11111l_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᬨ") in config:
        del (config[bstack11111l_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᬩ")])
        return False
    if bstack1lllll11l1_opy_() < version.parse(bstack11111l_opy_ (u"ࠪ࠷࠳࠺࠮࠱ࠩᬪ")):
        return False
    if bstack1lllll11l1_opy_() >= version.parse(bstack11111l_opy_ (u"ࠫ࠹࠴࠱࠯࠷ࠪᬫ")):
        return True
    if bstack11111l_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᬬ") in config and config[bstack11111l_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᬭ")] is False:
        return False
    else:
        return True
def bstack1lll111ll1_opy_(args_list, bstack11ll11l1111_opy_):
    index = -1
    for value in bstack11ll11l1111_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack111lll1ll1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack111lll1ll1_opy_ = bstack111lll1ll1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack11111l_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᬮ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack11111l_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᬯ"), exception=exception)
    def bstack1111ll111l_opy_(self):
        if self.result != bstack11111l_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᬰ"):
            return None
        if isinstance(self.exception_type, str) and bstack11111l_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᬱ") in self.exception_type:
            return bstack11111l_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᬲ")
        return bstack11111l_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᬳ")
    def bstack11l1l11lll1_opy_(self):
        if self.result != bstack11111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ᬴࠭"):
            return None
        if self.bstack111lll1ll1_opy_:
            return self.bstack111lll1ll1_opy_
        return bstack11l1l1llll1_opy_(self.exception)
def bstack11l1l1llll1_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11ll11l1lll_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack11l11llll1_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1l1111l1ll_opy_(config, logger):
    try:
        import playwright
        bstack11l11ll11ll_opy_ = playwright.__file__
        bstack11ll111l1ll_opy_ = os.path.split(bstack11l11ll11ll_opy_)
        bstack11l1ll11l1l_opy_ = bstack11ll111l1ll_opy_[0] + bstack11111l_opy_ (u"ࠧ࠰ࡦࡵ࡭ࡻ࡫ࡲ࠰ࡲࡤࡧࡰࡧࡧࡦ࠱࡯࡭ࡧ࠵ࡣ࡭࡫࠲ࡧࡱ࡯࠮࡫ࡵࠪᬵ")
        os.environ[bstack11111l_opy_ (u"ࠨࡉࡏࡓࡇࡇࡌࡠࡃࡊࡉࡓ࡚࡟ࡉࡖࡗࡔࡤࡖࡒࡐ࡚࡜ࠫᬶ")] = bstack1l11ll11ll_opy_(config)
        with open(bstack11l1ll11l1l_opy_, bstack11111l_opy_ (u"ࠩࡵࠫᬷ")) as f:
            bstack1llll1lll_opy_ = f.read()
            bstack11l1lllll1l_opy_ = bstack11111l_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩᬸ")
            bstack11ll111l11l_opy_ = bstack1llll1lll_opy_.find(bstack11l1lllll1l_opy_)
            if bstack11ll111l11l_opy_ == -1:
              process = subprocess.Popen(bstack11111l_opy_ (u"ࠦࡳࡶ࡭ࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠣᬹ"), shell=True, cwd=bstack11ll111l1ll_opy_[0])
              process.wait()
              bstack11ll1111l11_opy_ = bstack11111l_opy_ (u"ࠬࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶࠥ࠿ࠬᬺ")
              bstack11l1l111111_opy_ = bstack11111l_opy_ (u"ࠨࠢࠣࠢ࡟ࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴ࡝ࠤ࠾ࠤࡨࡵ࡮ࡴࡶࠣࡿࠥࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠡࡿࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮ࠧࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹ࠭ࠩ࠼ࠢ࡬ࡪࠥ࠮ࡰࡳࡱࡦࡩࡸࡹ࠮ࡦࡰࡹ࠲ࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠩࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠬ࠮ࡁࠠࠣࠤࠥᬻ")
              bstack11l1l111l1l_opy_ = bstack1llll1lll_opy_.replace(bstack11ll1111l11_opy_, bstack11l1l111111_opy_)
              with open(bstack11l1ll11l1l_opy_, bstack11111l_opy_ (u"ࠧࡸࠩᬼ")) as f:
                f.write(bstack11l1l111l1l_opy_)
    except Exception as e:
        logger.error(bstack1lll1llll1_opy_.format(str(e)))
def bstack11111llll_opy_():
  try:
    bstack11l1l11llll_opy_ = os.path.join(tempfile.gettempdir(), bstack11111l_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨᬽ"))
    bstack11l1lll111l_opy_ = []
    if os.path.exists(bstack11l1l11llll_opy_):
      with open(bstack11l1l11llll_opy_) as f:
        bstack11l1lll111l_opy_ = json.load(f)
      os.remove(bstack11l1l11llll_opy_)
    return bstack11l1lll111l_opy_
  except:
    pass
  return []
def bstack111l1llll_opy_(bstack1l1ll1l1_opy_):
  try:
    bstack11l1lll111l_opy_ = []
    bstack11l1l11llll_opy_ = os.path.join(tempfile.gettempdir(), bstack11111l_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩᬾ"))
    if os.path.exists(bstack11l1l11llll_opy_):
      with open(bstack11l1l11llll_opy_) as f:
        bstack11l1lll111l_opy_ = json.load(f)
    bstack11l1lll111l_opy_.append(bstack1l1ll1l1_opy_)
    with open(bstack11l1l11llll_opy_, bstack11111l_opy_ (u"ࠪࡻࠬᬿ")) as f:
        json.dump(bstack11l1lll111l_opy_, f)
  except:
    pass
def bstack1lllll1111_opy_(logger, bstack11ll111ll1l_opy_ = False):
  try:
    test_name = os.environ.get(bstack11111l_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧᭀ"), bstack11111l_opy_ (u"ࠬ࠭ᭁ"))
    if test_name == bstack11111l_opy_ (u"࠭ࠧᭂ"):
        test_name = threading.current_thread().__dict__.get(bstack11111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࡂࡥࡦࡢࡸࡪࡹࡴࡠࡰࡤࡱࡪ࠭ᭃ"), bstack11111l_opy_ (u"ࠨ᭄ࠩ"))
    bstack11l11lllll1_opy_ = bstack11111l_opy_ (u"ࠩ࠯ࠤࠬᭅ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11ll111ll1l_opy_:
        bstack1llll1l1ll_opy_ = os.environ.get(bstack11111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᭆ"), bstack11111l_opy_ (u"ࠫ࠵࠭ᭇ"))
        bstack1l1111lll1_opy_ = {bstack11111l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᭈ"): test_name, bstack11111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᭉ"): bstack11l11lllll1_opy_, bstack11111l_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᭊ"): bstack1llll1l1ll_opy_}
        bstack11l1l111lll_opy_ = []
        bstack11l1ll1l11l_opy_ = os.path.join(tempfile.gettempdir(), bstack11111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧᭋ"))
        if os.path.exists(bstack11l1ll1l11l_opy_):
            with open(bstack11l1ll1l11l_opy_) as f:
                bstack11l1l111lll_opy_ = json.load(f)
        bstack11l1l111lll_opy_.append(bstack1l1111lll1_opy_)
        with open(bstack11l1ll1l11l_opy_, bstack11111l_opy_ (u"ࠩࡺࠫᭌ")) as f:
            json.dump(bstack11l1l111lll_opy_, f)
    else:
        bstack1l1111lll1_opy_ = {bstack11111l_opy_ (u"ࠪࡲࡦࡳࡥࠨ᭍"): test_name, bstack11111l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ᭎"): bstack11l11lllll1_opy_, bstack11111l_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ᭏"): str(multiprocessing.current_process().name)}
        if bstack11111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪ᭐") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l1111lll1_opy_)
  except Exception as e:
      logger.warn(bstack11111l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡳࡽࡹ࡫ࡳࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦ᭑").format(e))
def bstack1l1lll1l1l_opy_(error_message, test_name, index, logger):
  try:
    bstack11l11ll1ll1_opy_ = []
    bstack1l1111lll1_opy_ = {bstack11111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭᭒"): test_name, bstack11111l_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ᭓"): error_message, bstack11111l_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩ᭔"): index}
    bstack11l11ll1l11_opy_ = os.path.join(tempfile.gettempdir(), bstack11111l_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬ᭕"))
    if os.path.exists(bstack11l11ll1l11_opy_):
        with open(bstack11l11ll1l11_opy_) as f:
            bstack11l11ll1ll1_opy_ = json.load(f)
    bstack11l11ll1ll1_opy_.append(bstack1l1111lll1_opy_)
    with open(bstack11l11ll1l11_opy_, bstack11111l_opy_ (u"ࠬࡽࠧ᭖")) as f:
        json.dump(bstack11l11ll1ll1_opy_, f)
  except Exception as e:
    logger.warn(bstack11111l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡴࡲࡦࡴࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤ᭗").format(e))
def bstack111ll1l11_opy_(bstack11l111ll1_opy_, name, logger):
  try:
    bstack1l1111lll1_opy_ = {bstack11111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ᭘"): name, bstack11111l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ᭙"): bstack11l111ll1_opy_, bstack11111l_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ᭚"): str(threading.current_thread()._name)}
    return bstack1l1111lll1_opy_
  except Exception as e:
    logger.warn(bstack11111l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡨࡥࡩࡣࡹࡩࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢ᭛").format(e))
  return
def bstack11l1l111l11_opy_():
    return platform.system() == bstack11111l_opy_ (u"ࠫ࡜࡯࡮ࡥࡱࡺࡷࠬ᭜")
def bstack1ll1llll1_opy_(bstack11l1ll1l1l1_opy_, config, logger):
    bstack11ll11111l1_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack11l1ll1l1l1_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack11111l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡰࡹ࡫ࡲࠡࡥࡲࡲ࡫࡯ࡧࠡ࡭ࡨࡽࡸࠦࡢࡺࠢࡵࡩ࡬࡫ࡸࠡ࡯ࡤࡸࡨ࡮࠺ࠡࡽࢀࠦ᭝").format(e))
    return bstack11ll11111l1_opy_
def bstack11l1l1l111l_opy_(bstack11l1llll111_opy_, bstack11ll1111ll1_opy_):
    bstack11ll111111l_opy_ = version.parse(bstack11l1llll111_opy_)
    bstack11l1lll11l1_opy_ = version.parse(bstack11ll1111ll1_opy_)
    if bstack11ll111111l_opy_ > bstack11l1lll11l1_opy_:
        return 1
    elif bstack11ll111111l_opy_ < bstack11l1lll11l1_opy_:
        return -1
    else:
        return 0
def bstack111l11llll_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1lll1lll_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11l1l1l1111_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l1l11ll11_opy_(options, framework, bstack1llll111l_opy_={}):
    if options is None:
        return
    if getattr(options, bstack11111l_opy_ (u"࠭ࡧࡦࡶࠪ᭞"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack1l11ll1l11_opy_ = caps.get(bstack11111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᭟"))
    bstack11l11ll1lll_opy_ = True
    bstack1l11l1l1_opy_ = os.environ[bstack11111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭᭠")]
    if bstack11l11llllll_opy_(caps.get(bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩ࡜࠹ࡃࠨ᭡"))) or bstack11l11llllll_opy_(caps.get(bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡥࡷ࠴ࡥࠪ᭢"))):
        bstack11l11ll1lll_opy_ = False
    if bstack11llll11l_opy_({bstack11111l_opy_ (u"ࠦࡺࡹࡥࡘ࠵ࡆࠦ᭣"): bstack11l11ll1lll_opy_}):
        bstack1l11ll1l11_opy_ = bstack1l11ll1l11_opy_ or {}
        bstack1l11ll1l11_opy_[bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ᭤")] = bstack11l1l1l1111_opy_(framework)
        bstack1l11ll1l11_opy_[bstack11111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᭥")] = bstack1ll111l1lll_opy_()
        bstack1l11ll1l11_opy_[bstack11111l_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ᭦")] = bstack1l11l1l1_opy_
        bstack1l11ll1l11_opy_[bstack11111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ᭧")] = bstack1llll111l_opy_
        if getattr(options, bstack11111l_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪ᭨"), None):
            options.set_capability(bstack11111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᭩"), bstack1l11ll1l11_opy_)
        else:
            options[bstack11111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ᭪")] = bstack1l11ll1l11_opy_
    else:
        if getattr(options, bstack11111l_opy_ (u"ࠬࡹࡥࡵࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸࡾ࠭᭫"), None):
            options.set_capability(bstack11111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑ᭬ࠧ"), bstack11l1l1l1111_opy_(framework))
            options.set_capability(bstack11111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᭭"), bstack1ll111l1lll_opy_())
            options.set_capability(bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ᭮"), bstack1l11l1l1_opy_)
            options.set_capability(bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ᭯"), bstack1llll111l_opy_)
        else:
            options[bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫ᭰")] = bstack11l1l1l1111_opy_(framework)
            options[bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ᭱")] = bstack1ll111l1lll_opy_()
            options[bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡫ࡳࡵࡪࡸࡦࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ᭲")] = bstack1l11l1l1_opy_
            options[bstack11111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧ᭳")] = bstack1llll111l_opy_
    return options
def bstack11l1ll1111l_opy_(bstack11l1lll11ll_opy_, framework):
    bstack1llll111l_opy_ = bstack1l11l11ll1_opy_.get_property(bstack11111l_opy_ (u"ࠢࡑࡎࡄ࡝࡜ࡘࡉࡈࡊࡗࡣࡕࡘࡏࡅࡗࡆࡘࡤࡓࡁࡑࠤ᭴"))
    if bstack11l1lll11ll_opy_ and len(bstack11l1lll11ll_opy_.split(bstack11111l_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧ᭵"))) > 1:
        ws_url = bstack11l1lll11ll_opy_.split(bstack11111l_opy_ (u"ࠩࡦࡥࡵࡹ࠽ࠨ᭶"))[0]
        if bstack11111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭᭷") in ws_url:
            from browserstack_sdk._version import __version__
            bstack11l1lll1l11_opy_ = json.loads(urllib.parse.unquote(bstack11l1lll11ll_opy_.split(bstack11111l_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ᭸"))[1]))
            bstack11l1lll1l11_opy_ = bstack11l1lll1l11_opy_ or {}
            bstack1l11l1l1_opy_ = os.environ[bstack11111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ᭹")]
            bstack11l1lll1l11_opy_[bstack11111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ᭺")] = str(framework) + str(__version__)
            bstack11l1lll1l11_opy_[bstack11111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᭻")] = bstack1ll111l1lll_opy_()
            bstack11l1lll1l11_opy_[bstack11111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧࡶࡸ࡭ࡻࡢࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ᭼")] = bstack1l11l1l1_opy_
            bstack11l1lll1l11_opy_[bstack11111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ᭽")] = bstack1llll111l_opy_
            bstack11l1lll11ll_opy_ = bstack11l1lll11ll_opy_.split(bstack11111l_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩ᭾"))[0] + bstack11111l_opy_ (u"ࠫࡨࡧࡰࡴ࠿ࠪ᭿") + urllib.parse.quote(json.dumps(bstack11l1lll1l11_opy_))
    return bstack11l1lll11ll_opy_
def bstack11l1ll1ll1_opy_():
    global bstack11l1ll1l1l_opy_
    from playwright._impl._browser_type import BrowserType
    bstack11l1ll1l1l_opy_ = BrowserType.connect
    return bstack11l1ll1l1l_opy_
def bstack1llllllll1_opy_(framework_name):
    global bstack1lll11l11l_opy_
    bstack1lll11l11l_opy_ = framework_name
    return framework_name
def bstack11111lll1_opy_(self, *args, **kwargs):
    global bstack11l1ll1l1l_opy_
    try:
        global bstack1lll11l11l_opy_
        if bstack11111l_opy_ (u"ࠬࡽࡳࡆࡰࡧࡴࡴ࡯࡮ࡵࠩᮀ") in kwargs:
            kwargs[bstack11111l_opy_ (u"࠭ࡷࡴࡇࡱࡨࡵࡵࡩ࡯ࡶࠪᮁ")] = bstack11l1ll1111l_opy_(
                kwargs.get(bstack11111l_opy_ (u"ࠧࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷࠫᮂ"), None),
                bstack1lll11l11l_opy_
            )
    except Exception as e:
        logger.error(bstack11111l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡖࡈࡐࠦࡣࡢࡲࡶ࠾ࠥࢁࡽࠣᮃ").format(str(e)))
    return bstack11l1ll1l1l_opy_(self, *args, **kwargs)
def bstack11l1llll1ll_opy_(bstack11l1l1ll111_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack1lll111l1_opy_(bstack11l1l1ll111_opy_, bstack11111l_opy_ (u"ࠤࠥᮄ"))
        if proxies and proxies.get(bstack11111l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤᮅ")):
            parsed_url = urlparse(proxies.get(bstack11111l_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥᮆ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack11111l_opy_ (u"ࠬࡶࡲࡰࡺࡼࡌࡴࡹࡴࠨᮇ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack11111l_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡵࡲࡵࠩᮈ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack11111l_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪᮉ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack11111l_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫᮊ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1lll1l111l_opy_(bstack11l1l1ll111_opy_):
    bstack11l1ll111l1_opy_ = {
        bstack11ll1l1l11l_opy_[bstack11l1l1ll1ll_opy_]: bstack11l1l1ll111_opy_[bstack11l1l1ll1ll_opy_]
        for bstack11l1l1ll1ll_opy_ in bstack11l1l1ll111_opy_
        if bstack11l1l1ll1ll_opy_ in bstack11ll1l1l11l_opy_
    }
    bstack11l1ll111l1_opy_[bstack11111l_opy_ (u"ࠤࡳࡶࡴࡾࡹࡔࡧࡷࡸ࡮ࡴࡧࡴࠤᮋ")] = bstack11l1llll1ll_opy_(bstack11l1l1ll111_opy_, bstack1l11l11ll1_opy_.get_property(bstack11111l_opy_ (u"ࠥࡴࡷࡵࡸࡺࡕࡨࡸࡹ࡯࡮ࡨࡵࠥᮌ")))
    bstack11l1l1111l1_opy_ = [element.lower() for element in bstack11ll1ll1111_opy_]
    bstack11ll11l1l11_opy_(bstack11l1ll111l1_opy_, bstack11l1l1111l1_opy_)
    return bstack11l1ll111l1_opy_
def bstack11ll11l1l11_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack11111l_opy_ (u"ࠦ࠯࠰ࠪࠫࠤᮍ")
    for value in d.values():
        if isinstance(value, dict):
            bstack11ll11l1l11_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack11ll11l1l11_opy_(item, keys)
def bstack1l1lllll1l1_opy_():
    bstack11l1llll11l_opy_ = [os.environ.get(bstack11111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡏࡌࡆࡕࡢࡈࡎࡘࠢᮎ")), os.path.join(os.path.expanduser(bstack11111l_opy_ (u"ࠨࡾࠣᮏ")), bstack11111l_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᮐ")), os.path.join(bstack11111l_opy_ (u"ࠨ࠱ࡷࡱࡵ࠭ᮑ"), bstack11111l_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᮒ"))]
    for path in bstack11l1llll11l_opy_:
        if path is None:
            continue
        try:
            if os.path.exists(path):
                logger.debug(bstack11111l_opy_ (u"ࠥࡊ࡮ࡲࡥࠡࠩࠥᮓ") + str(path) + bstack11111l_opy_ (u"ࠦࠬࠦࡥࡹ࡫ࡶࡸࡸ࠴ࠢᮔ"))
                if not os.access(path, os.W_OK):
                    logger.debug(bstack11111l_opy_ (u"ࠧࡍࡩࡷ࡫ࡱ࡫ࠥࡶࡥࡳ࡯࡬ࡷࡸ࡯࡯࡯ࡵࠣࡪࡴࡸࠠࠨࠤᮕ") + str(path) + bstack11111l_opy_ (u"ࠨࠧࠣᮖ"))
                    os.chmod(path, 0o777)
                else:
                    logger.debug(bstack11111l_opy_ (u"ࠢࡇ࡫࡯ࡩࠥ࠭ࠢᮗ") + str(path) + bstack11111l_opy_ (u"ࠣࠩࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡭ࡧࡳࠡࡶ࡫ࡩࠥࡸࡥࡲࡷ࡬ࡶࡪࡪࠠࡱࡧࡵࡱ࡮ࡹࡳࡪࡱࡱࡷ࠳ࠨᮘ"))
            else:
                logger.debug(bstack11111l_opy_ (u"ࠤࡆࡶࡪࡧࡴࡪࡰࡪࠤ࡫࡯࡬ࡦࠢࠪࠦᮙ") + str(path) + bstack11111l_opy_ (u"ࠥࠫࠥࡽࡩࡵࡪࠣࡻࡷ࡯ࡴࡦࠢࡳࡩࡷࡳࡩࡴࡵ࡬ࡳࡳ࠴ࠢᮚ"))
                os.makedirs(path, exist_ok=True)
                os.chmod(path, 0o777)
            logger.debug(bstack11111l_opy_ (u"ࠦࡔࡶࡥࡳࡣࡷ࡭ࡴࡴࠠࡴࡷࡦࡧࡪ࡫ࡤࡦࡦࠣࡪࡴࡸࠠࠨࠤᮛ") + str(path) + bstack11111l_opy_ (u"ࠧ࠭࠮ࠣᮜ"))
            return path
        except Exception as e:
            logger.debug(bstack11111l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡩࡹࠦࡵࡱࠢࡩ࡭ࡱ࡫ࠠࠨࡽࡳࡥࡹ࡮ࡽࠨ࠼ࠣࠦᮝ") + str(e) + bstack11111l_opy_ (u"ࠢࠣᮞ"))
    logger.debug(bstack11111l_opy_ (u"ࠣࡃ࡯ࡰࠥࡶࡡࡵࡪࡶࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠧᮟ"))
    return None
@measure(event_name=EVENTS.bstack11ll1l11lll_opy_, stage=STAGE.bstack1l1llll11_opy_)
def bstack1llllll1111_opy_(binary_path, bstack1llll11111l_opy_, bs_config):
    logger.debug(bstack11111l_opy_ (u"ࠤࡆࡹࡷࡸࡥ࡯ࡶࠣࡇࡑࡏࠠࡑࡣࡷ࡬ࠥ࡬࡯ࡶࡰࡧ࠾ࠥࢁࡽࠣᮠ").format(binary_path))
    bstack11l1ll1l111_opy_ = bstack11111l_opy_ (u"ࠪࠫᮡ")
    bstack11l1l11l1l1_opy_ = {
        bstack11111l_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᮢ"): __version__,
        bstack11111l_opy_ (u"ࠧࡵࡳࠣᮣ"): platform.system(),
        bstack11111l_opy_ (u"ࠨ࡯ࡴࡡࡤࡶࡨ࡮ࠢᮤ"): platform.machine(),
        bstack11111l_opy_ (u"ࠢࡤ࡮࡬ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠧᮥ"): bstack11111l_opy_ (u"ࠨ࠲ࠪᮦ"),
        bstack11111l_opy_ (u"ࠤࡶࡨࡰࡥ࡬ࡢࡰࡪࡹࡦ࡭ࡥࠣᮧ"): bstack11111l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᮨ")
    }
    bstack11l1ll1l1ll_opy_(bstack11l1l11l1l1_opy_)
    try:
        if binary_path:
            bstack11l1l11l1l1_opy_[bstack11111l_opy_ (u"ࠫࡨࡲࡩࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᮩ")] = subprocess.check_output([binary_path, bstack11111l_opy_ (u"ࠧࡼࡥࡳࡵ࡬ࡳࡳࠨ᮪")]).strip().decode(bstack11111l_opy_ (u"࠭ࡵࡵࡨ࠰࠼᮫ࠬ"))
        response = requests.request(
            bstack11111l_opy_ (u"ࠧࡈࡇࡗࠫᮬ"),
            url=bstack11ll11l1l1_opy_(bstack11ll1llll1l_opy_),
            headers=None,
            auth=(bs_config[bstack11111l_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᮭ")], bs_config[bstack11111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᮮ")]),
            json=None,
            params=bstack11l1l11l1l1_opy_
        )
        data = response.json()
        if response.status_code == 200 and bstack11111l_opy_ (u"ࠪࡹࡷࡲࠧᮯ") in data.keys() and bstack11111l_opy_ (u"ࠫࡺࡶࡤࡢࡶࡨࡨࡤࡩ࡬ࡪࡡࡹࡩࡷࡹࡩࡰࡰࠪ᮰") in data.keys():
            logger.debug(bstack11111l_opy_ (u"ࠧࡔࡥࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡢࡪࡰࡤࡶࡾ࠲ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡤ࡬ࡲࡦࡸࡹࠡࡸࡨࡶࡸ࡯࡯࡯࠼ࠣࡿࢂࠨ᮱").format(bstack11l1l11l1l1_opy_[bstack11111l_opy_ (u"࠭ࡣ࡭࡫ࡢࡺࡪࡸࡳࡪࡱࡱࠫ᮲")]))
            if bstack11111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡕࡓࡎࠪ᮳") in os.environ:
                logger.debug(bstack11111l_opy_ (u"ࠣࡕ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡦ࡮ࡴࡡࡳࡻࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡧࡳࠡࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡔࡆࡎࡣࡇࡏࡎࡂࡔ࡜ࡣ࡚ࡘࡌࠡ࡫ࡶࠤࡸ࡫ࡴࠣ᮴"))
                data[bstack11111l_opy_ (u"ࠩࡸࡶࡱ࠭᮵")] = os.environ[bstack11111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅࡍࡓࡇࡒ࡚ࡡࡘࡖࡑ࠭᮶")]
            bstack11l1l1l1lll_opy_ = bstack11l1llll1l1_opy_(data[bstack11111l_opy_ (u"ࠫࡺࡸ࡬ࠨ᮷")], bstack1llll11111l_opy_)
            bstack11l1ll1l111_opy_ = os.path.join(bstack1llll11111l_opy_, bstack11l1l1l1lll_opy_)
            os.chmod(bstack11l1ll1l111_opy_, 0o777) # bstack11l1lll1l1l_opy_ permission
            return bstack11l1ll1l111_opy_
    except Exception as e:
        logger.debug(bstack11111l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡨࡴࡽ࡮࡭ࡱࡤࡨ࡮ࡴࡧࠡࡰࡨࡻ࡙ࠥࡄࡌࠢࡾࢁࠧ᮸").format(e))
    return binary_path
def bstack11l1ll1l1ll_opy_(bstack11l1l11l1l1_opy_):
    try:
        if bstack11111l_opy_ (u"࠭࡬ࡪࡰࡸࡼࠬ᮹") not in bstack11l1l11l1l1_opy_[bstack11111l_opy_ (u"ࠧࡰࡵࠪᮺ")].lower():
            return
        if os.path.exists(bstack11111l_opy_ (u"ࠣ࠱ࡨࡸࡨ࠵࡯ࡴ࠯ࡵࡩࡱ࡫ࡡࡴࡧࠥᮻ")):
            with open(bstack11111l_opy_ (u"ࠤ࠲ࡩࡹࡩ࠯ࡰࡵ࠰ࡶࡪࡲࡥࡢࡵࡨࠦᮼ"), bstack11111l_opy_ (u"ࠥࡶࠧᮽ")) as f:
                bstack11ll11l11ll_opy_ = {}
                for line in f:
                    if bstack11111l_opy_ (u"ࠦࡂࠨᮾ") in line:
                        key, value = line.rstrip().split(bstack11111l_opy_ (u"ࠧࡃࠢᮿ"), 1)
                        bstack11ll11l11ll_opy_[key] = value.strip(bstack11111l_opy_ (u"࠭ࠢ࡝ࠩࠪᯀ"))
                bstack11l1l11l1l1_opy_[bstack11111l_opy_ (u"ࠧࡥ࡫ࡶࡸࡷࡵࠧᯁ")] = bstack11ll11l11ll_opy_.get(bstack11111l_opy_ (u"ࠣࡋࡇࠦᯂ"), bstack11111l_opy_ (u"ࠤࠥᯃ"))
        elif os.path.exists(bstack11111l_opy_ (u"ࠥ࠳ࡪࡺࡣ࠰ࡣ࡯ࡴ࡮ࡴࡥ࠮ࡴࡨࡰࡪࡧࡳࡦࠤᯄ")):
            bstack11l1l11l1l1_opy_[bstack11111l_opy_ (u"ࠫࡩ࡯ࡳࡵࡴࡲࠫᯅ")] = bstack11111l_opy_ (u"ࠬࡧ࡬ࡱ࡫ࡱࡩࠬᯆ")
    except Exception as e:
        logger.debug(bstack11111l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡪࡩࡹࠦࡤࡪࡵࡷࡶࡴࠦ࡯ࡧࠢ࡯࡭ࡳࡻࡸࠣᯇ") + e)
@measure(event_name=EVENTS.bstack11ll1l1lll1_opy_, stage=STAGE.bstack1l1llll11_opy_)
def bstack11l1llll1l1_opy_(bstack11l1ll11l11_opy_, bstack11l1lll1111_opy_):
    logger.debug(bstack11111l_opy_ (u"ࠢࡅࡱࡺࡲࡱࡵࡡࡥ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺࠢࡩࡶࡴࡳ࠺ࠡࠤᯈ") + str(bstack11l1ll11l11_opy_) + bstack11111l_opy_ (u"ࠣࠤᯉ"))
    zip_path = os.path.join(bstack11l1lll1111_opy_, bstack11111l_opy_ (u"ࠤࡧࡳࡼࡴ࡬ࡰࡣࡧࡩࡩࡥࡦࡪ࡮ࡨ࠲ࡿ࡯ࡰࠣᯊ"))
    bstack11l1l1l1lll_opy_ = bstack11111l_opy_ (u"ࠪࠫᯋ")
    with requests.get(bstack11l1ll11l11_opy_, stream=True) as response:
        response.raise_for_status()
        with open(zip_path, bstack11111l_opy_ (u"ࠦࡼࡨࠢᯌ")) as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        logger.debug(bstack11111l_opy_ (u"ࠧࡌࡩ࡭ࡧࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࡪࡪࠠࡴࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࡰࡾ࠴ࠢᯍ"))
    with zipfile.ZipFile(zip_path, bstack11111l_opy_ (u"࠭ࡲࠨᯎ")) as zip_ref:
        bstack11ll1111l1l_opy_ = zip_ref.namelist()
        if len(bstack11ll1111l1l_opy_) > 0:
            bstack11l1l1l1lll_opy_ = bstack11ll1111l1l_opy_[0] # bstack11l11lll111_opy_ bstack11ll1lll11l_opy_ will be bstack11l1l1l11ll_opy_ 1 file i.e. the binary in the zip
        zip_ref.extractall(bstack11l1lll1111_opy_)
        logger.debug(bstack11111l_opy_ (u"ࠢࡇ࡫࡯ࡩࡸࠦࡳࡶࡥࡦࡩࡸࡹࡦࡶ࡮࡯ࡽࠥ࡫ࡸࡵࡴࡤࡧࡹ࡫ࡤࠡࡶࡲࠤࠬࠨᯏ") + str(bstack11l1lll1111_opy_) + bstack11111l_opy_ (u"ࠣࠩࠥᯐ"))
    os.remove(zip_path)
    return bstack11l1l1l1lll_opy_
def get_cli_dir():
    bstack11l1l111ll1_opy_ = bstack1l1lllll1l1_opy_()
    if bstack11l1l111ll1_opy_:
        bstack1llll11111l_opy_ = os.path.join(bstack11l1l111ll1_opy_, bstack11111l_opy_ (u"ࠤࡦࡰ࡮ࠨᯑ"))
        if not os.path.exists(bstack1llll11111l_opy_):
            os.makedirs(bstack1llll11111l_opy_, mode=0o777, exist_ok=True)
        return bstack1llll11111l_opy_
    else:
        raise FileNotFoundError(bstack11111l_opy_ (u"ࠥࡒࡴࠦࡷࡳ࡫ࡷࡥࡧࡲࡥࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡕࡇࡏࠥࡨࡩ࡯ࡣࡵࡽ࠳ࠨᯒ"))
def bstack1lll1ll111l_opy_(bstack1llll11111l_opy_):
    bstack11111l_opy_ (u"ࠦࠧࠨࡇࡦࡶࠣࡸ࡭࡫ࠠࡱࡣࡷ࡬ࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯࡙ࠥࡄࡌࠢࡥ࡭ࡳࡧࡲࡺࠢ࡬ࡲࠥࡧࠠࡸࡴ࡬ࡸࡦࡨ࡬ࡦࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽ࠳ࠨࠢࠣᯓ")
    bstack11l11lll1l1_opy_ = [
        os.path.join(bstack1llll11111l_opy_, f)
        for f in os.listdir(bstack1llll11111l_opy_)
        if os.path.isfile(os.path.join(bstack1llll11111l_opy_, f)) and f.startswith(bstack11111l_opy_ (u"ࠧࡨࡩ࡯ࡣࡵࡽ࠲ࠨᯔ"))
    ]
    if len(bstack11l11lll1l1_opy_) > 0:
        return max(bstack11l11lll1l1_opy_, key=os.path.getmtime) # get bstack11l11lll11l_opy_ binary
    return bstack11111l_opy_ (u"ࠨࠢᯕ")
def bstack1ll1l1l1l1l_opy_(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = bstack1ll1l1l1l1l_opy_(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d