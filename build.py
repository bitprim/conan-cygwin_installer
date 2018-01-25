# #!/usr/bin/env python
# # -*- coding: utf-8 -*-


from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(username="bitprim", channel="stable", archs=["x86_64"])
    # builder.add_common_builds(shared_option_name="bitprim-conan-boost:shared")
    builder.add_common_builds()

    filtered_builds = []
    for settings, options, env_vars, build_requires in builder.builds:
        if settings["build_type"] == "Release":
            filtered_builds.append([settings, options, env_vars, build_requires])

    builder.builds = filtered_builds
    builder.run()



# from bincrafters import build_template_installer
# import os

# if __name__ == "__main__":

#     builder = build_template_installer.get_builder()

#     builder.add({"arch": os.environ["CONAN_ARCHS"]}, {}, {}, {})

#     builder.run()
