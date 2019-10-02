import falcon
import yaml
import json
import os

from bel.Config import config
import bel.lang.bel_specification

import structlog

log = structlog.getLogger(__name__)

belspec_dir = config["bel"]["lang"]["specifications"]


class BelSpecResource(object):
    def on_get(self, req, resp, version=""):

        versions = bel.lang.bel_specification.get_bel_versions()
        if version:
            if version not in versions:
                description = f"No BEL Specification found for {version}"
                resp.media = {"title": "No BEL Spec found", "message": description}
                resp.status = falcon.HTTP_404

            version_underscores = version.replace(".", "_")
            fn = f"{belspec_dir}/bel_v{version_underscores}.yaml"
            with open(fn, "r") as f:
                belspec = yaml.load(f, Loader=yaml.SafeLoader)

            resp.media = {"belspec": belspec, "versions": versions}
            resp.status = falcon.HTTP_200
        else:
            resp.media = {"versions": versions}
            resp.status = falcon.HTTP_200

    def on_put(self, req, resp):
        """Save BEL Spec onto server"""

        force = req.get_param("force", False)
        belspec = req.media["belspec"]
        fn_version = belspec["version"].replace(".", "_")

        fn = f"{belspec_dir}/bel_v{fn_version}.yaml"
        with open(fn, "w") as f:
            yaml.dump(belspec, f, indent=2)

        bel.lang.bel_specification.update_specifications(force=force)

        resp.status = falcon.HTTP_204

    def on_delete(self, req, resp, version):
        """Delete version on server"""

        fn_version = version.replace(".", "_")
        yaml_fn = f"{belspec_dir}/bel_v{fn_version}.yaml"
        json_fn = f"{belspec_dir}/bel_v{fn_version}.json"
        ebnf_fn = f"{belspec_dir}/bel_v{fn_version}.ebnf"
        parser_fn = f"{belspec_dir}/bel_v{fn_version}_parser.py"

        if os.path.exists(yaml_fn):
            os.remove(yaml_fn)
        if os.path.exists(json_fn):
            os.remove(json_fn)
        if os.path.exists(ebnf_fn):
            os.remove(ebnf_fn)
        if os.path.exists(parser_fn):
            os.remove(parser_fn)

        # Update versions file
        version_fn = f"{belspec_dir}/versions.json"
        with open(version_fn, "r") as f:
            versions = json.load(f)

        versions = [v for v in versions if v != version]

        with open(version_fn, "w") as f:
            json.dump(versions, f, indent=4)

        resp.status = falcon.HTTP_200
        resp.media = {"versions": versions}
