from tiktok_views_generator.processors.attach_proxy import AttachProxy
from tiktok_views_generator.processors.build_request import BuildRequest
from tiktok_views_generator.processors.mint_session import MintSession
from tiktok_views_generator.processors.resolve_video_id import ResolveVideoId

PROCESSORS = [
    ResolveVideoId(),
    MintSession(),
    AttachProxy(),
    BuildRequest(),
]

__all__ = ["PROCESSORS"]