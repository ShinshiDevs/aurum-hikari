import os
import platform

from hikari import _about as about_hikari

import aurum

if __name__ == "__main__":
    print(
        f"Aurum {aurum.__version__} located at {os.path.abspath(os.path.dirname(aurum.__file__))} \n"
        f"hikari {about_hikari.__version__} \n"
        f"{platform.python_implementation()} {platform.python_version()} {platform.python_compiler()} \n"
        f"{platform.uname().version} {platform.platform()}"
    )
