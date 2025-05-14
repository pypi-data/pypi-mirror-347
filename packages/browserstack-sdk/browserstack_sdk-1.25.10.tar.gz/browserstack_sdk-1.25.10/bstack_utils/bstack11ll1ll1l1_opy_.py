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
import sys
import logging
import tarfile
import io
import os
import time
import requests
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bstack_utils.constants import bstack11ll1ll1l11_opy_, bstack11ll1ll1111_opy_
import tempfile
import json
bstack11l111l1111_opy_ = os.getenv(bstack11111l_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡊࡣࡋࡏࡌࡆࠤᰁ"), None) or os.path.join(tempfile.gettempdir(), bstack11111l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡦࡨࡦࡺ࡭࠮࡭ࡱࡪࠦᰂ"))
bstack11l111l1lll_opy_ = os.path.join(bstack11111l_opy_ (u"ࠥࡰࡴ࡭ࠢᰃ"), bstack11111l_opy_ (u"ࠫࡸࡪ࡫࠮ࡥ࡯࡭࠲ࡪࡥࡣࡷࡪ࠲ࡱࡵࡧࠨᰄ"))
logging.Formatter.converter = time.gmtime
def get_logger(name=__name__, level=None):
  logger = logging.getLogger(name)
  if level:
    logging.basicConfig(
      level=level,
      format=bstack11111l_opy_ (u"ࠬࠫࠨࡢࡵࡦࡸ࡮ࡳࡥࠪࡵࠣ࡟ࠪ࠮࡮ࡢ࡯ࡨ࠭ࡸࡣ࡛ࠦࠪ࡯ࡩࡻ࡫࡬࡯ࡣࡰࡩ࠮ࡹ࡝ࠡ࠯ࠣࠩ࠭ࡳࡥࡴࡵࡤ࡫ࡪ࠯ࡳࠨᰅ"),
      datefmt=bstack11111l_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࡕࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࡝ࠫᰆ"),
      stream=sys.stdout
    )
  return logger
def bstack1lllll11l1l_opy_():
  bstack11l111lll1l_opy_ = os.environ.get(bstack11111l_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡊࡐࡄࡖ࡞ࡥࡄࡆࡄࡘࡋࠧᰇ"), bstack11111l_opy_ (u"ࠣࡨࡤࡰࡸ࡫ࠢᰈ"))
  return logging.DEBUG if bstack11l111lll1l_opy_.lower() == bstack11111l_opy_ (u"ࠤࡷࡶࡺ࡫ࠢᰉ") else logging.INFO
def bstack1l1lll1ll11_opy_():
  global bstack11l111l1111_opy_
  if os.path.exists(bstack11l111l1111_opy_):
    os.remove(bstack11l111l1111_opy_)
  if os.path.exists(bstack11l111l1lll_opy_):
    os.remove(bstack11l111l1lll_opy_)
def bstack111l1lll_opy_():
  for handler in logging.getLogger().handlers:
    logging.getLogger().removeHandler(handler)
def bstack1l1ll1l11l_opy_(config, log_level):
  bstack11l111lllll_opy_ = log_level
  if bstack11111l_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬᰊ") in config and config[bstack11111l_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ᰋ")] in bstack11ll1ll1l11_opy_:
    bstack11l111lllll_opy_ = bstack11ll1ll1l11_opy_[config[bstack11111l_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᰌ")]]
  if config.get(bstack11111l_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁࡶࡶࡲࡇࡦࡶࡴࡶࡴࡨࡐࡴ࡭ࡳࠨᰍ"), False):
    logging.getLogger().setLevel(bstack11l111lllll_opy_)
    return bstack11l111lllll_opy_
  global bstack11l111l1111_opy_
  bstack111l1lll_opy_()
  bstack11l111ll11l_opy_ = logging.Formatter(
    fmt=bstack11111l_opy_ (u"ࠧࠦࠪࡤࡷࡨࡺࡩ࡮ࡧࠬࡷࠥࡡࠥࠩࡰࡤࡱࡪ࠯ࡳ࡞࡝ࠨࠬࡱ࡫ࡶࡦ࡮ࡱࡥࡲ࡫ࠩࡴ࡟ࠣ࠱ࠥࠫࠨ࡮ࡧࡶࡷࡦ࡭ࡥࠪࡵࠪᰎ"),
    datefmt=bstack11111l_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࡗࠩࡍࡀࠥࡎ࠼ࠨࡗ࡟࠭ᰏ"),
  )
  bstack11l111l11l1_opy_ = logging.StreamHandler(sys.stdout)
  file_handler = logging.FileHandler(bstack11l111l1111_opy_)
  file_handler.setFormatter(bstack11l111ll11l_opy_)
  bstack11l111l11l1_opy_.setFormatter(bstack11l111ll11l_opy_)
  file_handler.setLevel(logging.DEBUG)
  bstack11l111l11l1_opy_.setLevel(log_level)
  file_handler.addFilter(lambda r: r.name != bstack11111l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸ࠮ࡳࡧࡰࡳࡹ࡫࠮ࡳࡧࡰࡳࡹ࡫࡟ࡤࡱࡱࡲࡪࡩࡴࡪࡱࡱࠫᰐ"))
  logging.getLogger().setLevel(logging.DEBUG)
  bstack11l111l11l1_opy_.setLevel(bstack11l111lllll_opy_)
  logging.getLogger().addHandler(bstack11l111l11l1_opy_)
  logging.getLogger().addHandler(file_handler)
  return bstack11l111lllll_opy_
def bstack11l111lll11_opy_(config):
  try:
    bstack11l111l11ll_opy_ = set(bstack11ll1ll1111_opy_)
    bstack11l111l111l_opy_ = bstack11111l_opy_ (u"ࠪࠫᰑ")
    with open(bstack11111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡽࡲࡲࠧᰒ")) as bstack11l11l111l1_opy_:
      bstack11l111l1ll1_opy_ = bstack11l11l111l1_opy_.read()
      bstack11l111l111l_opy_ = re.sub(bstack11111l_opy_ (u"ࡷ࠭࡞ࠩ࡞ࡶ࠯࠮ࡅࠣ࠯ࠬࠧࡠࡳ࠭ᰓ"), bstack11111l_opy_ (u"࠭ࠧᰔ"), bstack11l111l1ll1_opy_, flags=re.M)
      bstack11l111l111l_opy_ = re.sub(
        bstack11111l_opy_ (u"ࡲࠨࡠࠫࡠࡸ࠱ࠩࡀࠪࠪᰕ") + bstack11111l_opy_ (u"ࠨࡾࠪᰖ").join(bstack11l111l11ll_opy_) + bstack11111l_opy_ (u"ࠩࠬ࠲࠯ࠪࠧᰗ"),
        bstack11111l_opy_ (u"ࡵࠫࡡ࠸࠺ࠡ࡝ࡕࡉࡉࡇࡃࡕࡇࡇࡡࠬᰘ"),
        bstack11l111l111l_opy_, flags=re.M | re.I
      )
    def bstack11l1111ll1l_opy_(dic):
      bstack11l11l1111l_opy_ = {}
      for key, value in dic.items():
        if key in bstack11l111l11ll_opy_:
          bstack11l11l1111l_opy_[key] = bstack11111l_opy_ (u"ࠫࡠࡘࡅࡅࡃࡆࡘࡊࡊ࡝ࠨᰙ")
        else:
          if isinstance(value, dict):
            bstack11l11l1111l_opy_[key] = bstack11l1111ll1l_opy_(value)
          else:
            bstack11l11l1111l_opy_[key] = value
      return bstack11l11l1111l_opy_
    bstack11l11l1111l_opy_ = bstack11l1111ll1l_opy_(config)
    return {
      bstack11111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨᰚ"): bstack11l111l111l_opy_,
      bstack11111l_opy_ (u"࠭ࡦࡪࡰࡤࡰࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᰛ"): json.dumps(bstack11l11l1111l_opy_)
    }
  except Exception as e:
    return {}
def bstack11l1111ll11_opy_(inipath, rootpath):
  log_dir = os.path.join(os.getcwd(), bstack11111l_opy_ (u"ࠧ࡭ࡱࡪࠫᰜ"))
  if not os.path.exists(log_dir):
    os.makedirs(log_dir)
  bstack11l111l1l11_opy_ = os.path.join(log_dir, bstack11111l_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡥࡲࡲ࡫࡯ࡧࡴࠩᰝ"))
  if not os.path.exists(bstack11l111l1l11_opy_):
    bstack11l11l11111_opy_ = {
      bstack11111l_opy_ (u"ࠤ࡬ࡲ࡮ࡶࡡࡵࡪࠥᰞ"): str(inipath),
      bstack11111l_opy_ (u"ࠥࡶࡴࡵࡴࡱࡣࡷ࡬ࠧᰟ"): str(rootpath)
    }
    with open(os.path.join(log_dir, bstack11111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࡣࡨࡵ࡮ࡧ࡫ࡪࡷ࠳ࡰࡳࡰࡰࠪᰠ")), bstack11111l_opy_ (u"ࠬࡽࠧᰡ")) as bstack11l111ll1l1_opy_:
      bstack11l111ll1l1_opy_.write(json.dumps(bstack11l11l11111_opy_))
def bstack11l111ll111_opy_():
  try:
    bstack11l111l1l11_opy_ = os.path.join(os.getcwd(), bstack11111l_opy_ (u"࠭࡬ࡰࡩࠪᰢ"), bstack11111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭ᰣ"))
    if os.path.exists(bstack11l111l1l11_opy_):
      with open(bstack11l111l1l11_opy_, bstack11111l_opy_ (u"ࠨࡴࠪᰤ")) as bstack11l111ll1l1_opy_:
        bstack11l111llll1_opy_ = json.load(bstack11l111ll1l1_opy_)
      return bstack11l111llll1_opy_.get(bstack11111l_opy_ (u"ࠩ࡬ࡲ࡮ࡶࡡࡵࡪࠪᰥ"), bstack11111l_opy_ (u"ࠪࠫᰦ")), bstack11l111llll1_opy_.get(bstack11111l_opy_ (u"ࠫࡷࡵ࡯ࡵࡲࡤࡸ࡭࠭ᰧ"), bstack11111l_opy_ (u"ࠬ࠭ᰨ"))
  except:
    pass
  return None, None
def bstack11l111l1l1l_opy_():
  try:
    bstack11l111l1l11_opy_ = os.path.join(os.getcwd(), bstack11111l_opy_ (u"࠭࡬ࡰࡩࠪᰩ"), bstack11111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡤࡱࡱࡪ࡮࡭ࡳ࠯࡬ࡶࡳࡳ࠭ᰪ"))
    if os.path.exists(bstack11l111l1l11_opy_):
      os.remove(bstack11l111l1l11_opy_)
  except:
    pass
def bstack1l1lll1111_opy_(config):
  from bstack_utils.helper import bstack1l11l11ll1_opy_
  global bstack11l111l1111_opy_
  try:
    if config.get(bstack11111l_opy_ (u"ࠨࡦ࡬ࡷࡦࡨ࡬ࡦࡃࡸࡸࡴࡉࡡࡱࡶࡸࡶࡪࡒ࡯ࡨࡵࠪᰫ"), False):
      return
    uuid = os.getenv(bstack11111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᰬ")) if os.getenv(bstack11111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᰭ")) else bstack1l11l11ll1_opy_.get_property(bstack11111l_opy_ (u"ࠦࡸࡪ࡫ࡓࡷࡱࡍࡩࠨᰮ"))
    if not uuid or uuid == bstack11111l_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᰯ"):
      return
    bstack11l1111llll_opy_ = [bstack11111l_opy_ (u"࠭ࡲࡦࡳࡸ࡭ࡷ࡫࡭ࡦࡰࡷࡷ࠳ࡺࡸࡵࠩᰰ"), bstack11111l_opy_ (u"ࠧࡑ࡫ࡳࡪ࡮ࡲࡥࠨᰱ"), bstack11111l_opy_ (u"ࠨࡲࡼࡴࡷࡵࡪࡦࡥࡷ࠲ࡹࡵ࡭࡭ࠩᰲ"), bstack11l111l1111_opy_, bstack11l111l1lll_opy_]
    bstack11l1111lll1_opy_, root_path = bstack11l111ll111_opy_()
    if bstack11l1111lll1_opy_ != None:
      bstack11l1111llll_opy_.append(bstack11l1111lll1_opy_)
    if root_path != None:
      bstack11l1111llll_opy_.append(os.path.join(root_path, bstack11111l_opy_ (u"ࠩࡦࡳࡳ࡬ࡴࡦࡵࡷ࠲ࡵࡿࠧᰳ")))
    bstack111l1lll_opy_()
    logging.shutdown()
    output_file = os.path.join(tempfile.gettempdir(), bstack11111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠰ࡰࡴ࡭ࡳ࠮ࠩᰴ") + uuid + bstack11111l_opy_ (u"ࠫ࠳ࡺࡡࡳ࠰ࡪࡾࠬᰵ"))
    with tarfile.open(output_file, bstack11111l_opy_ (u"ࠧࡽ࠺ࡨࡼࠥᰶ")) as archive:
      for file in filter(lambda f: os.path.exists(f), bstack11l1111llll_opy_):
        try:
          archive.add(file,  arcname=os.path.basename(file))
        except:
          pass
      for name, data in bstack11l111lll11_opy_(config).items():
        tarinfo = tarfile.TarInfo(name)
        bstack11l111ll1ll_opy_ = data.encode()
        tarinfo.size = len(bstack11l111ll1ll_opy_)
        archive.addfile(tarinfo, io.BytesIO(bstack11l111ll1ll_opy_))
    bstack1ll111l111_opy_ = MultipartEncoder(
      fields= {
        bstack11111l_opy_ (u"࠭ࡤࡢࡶࡤ᰷ࠫ"): (os.path.basename(output_file), open(os.path.abspath(output_file), bstack11111l_opy_ (u"ࠧࡳࡤࠪ᰸")), bstack11111l_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡸ࠮ࡩࡽ࡭ࡵ࠭᰹")),
        bstack11111l_opy_ (u"ࠩࡦࡰ࡮࡫࡮ࡵࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ᰺"): uuid
      }
    )
    response = requests.post(
      bstack11111l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡺࡶ࡬ࡰࡣࡧ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳ࠯ࡤ࡮࡬ࡩࡳࡺ࠭࡭ࡱࡪࡷ࠴ࡻࡰ࡭ࡱࡤࡨࠧ᰻"),
      data=bstack1ll111l111_opy_,
      headers={bstack11111l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪ᰼"): bstack1ll111l111_opy_.content_type},
      auth=(config[bstack11111l_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ᰽")], config[bstack11111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ᰾")])
    )
    os.remove(output_file)
    if response.status_code != 200:
      get_logger().debug(bstack11111l_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡵࡱ࡮ࡲࡥࡩࠦ࡬ࡰࡩࡶ࠾ࠥ࠭᰿") + response.status_code)
  except Exception as e:
    get_logger().debug(bstack11111l_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡧࡱࡨ࡮ࡴࡧࠡ࡮ࡲ࡫ࡸࡀࠧ᱀") + str(e))
  finally:
    try:
      bstack1l1lll1ll11_opy_()
      bstack11l111l1l1l_opy_()
    except:
      pass