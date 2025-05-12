import os

def dvfm_packages():
    libide_dir = os.path.dirname(__file__)

    return {
        "ide": os.path.join(libide_dir, "flow.dv"),
        "ide.dvt": os.path.join(libide_dir, "dvt_flow.dv"),
        "ide.vbl": os.path.join(libide_dir, "vbl_flow.dv")
    }
